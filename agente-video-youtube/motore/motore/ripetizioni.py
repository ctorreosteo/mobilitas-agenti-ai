"""Ripetizioni: le riprese doppie che la trascrizione intera e quella a blocchi non vedono.

Perche serve (YT_POSTURA_32, anteprima della fase 7b, note di Riccardo):

- la trascrizione intera APPIANA le riprese e sposta i tempi delle parole vicine;
- anche quella a blocchi le appiana quando la ripresa sta dentro un blocco solo
  (nessuna pausa da 0,2 s fra le due prese): «Qui c'è un collega- / qui c'è un
  collegamento» (sorgente 242,2-245,1) usciva come una frase pulita.

Qui il parlato si trascrive a **finestre corte** (3 s ogni 1,5 s), ognuna da sola:
una finestra cosi corta contiene le due prese e whisper le scrive tutte e due.
Poi si cercano:

1. dentro ogni finestra, una sequenza di 2 o piu parole ripetuta;
2. fra blocchi vicini (ognuno trascritto da solo), una sequenza di 2 o piu parole
   ripetuta entro 10 s.

Una sequenza conta solo se contiene almeno una parola piena (non solo «che non»,
«di un»). Le ripetizioni volute (retoriche) si dichiarano in regia.json ->
`ripetizioni_ok`: [{"parole": "che non", "t": 389.6, "motivo": "..."}] (`t` in
secondi sorgente, facoltativo; senza `t` vale ovunque).
"""
from .papere import toks, VUOTE
from . import trascrivi as T

WIN, STEP, ENTRO = 3.0, 1.5, 10.0


NUMERI = {'1': 'uno', '2': 'due', '3': 'tre', '4': 'quattro', '5': 'cinque', '6': 'sei', '7': 'sette', '8': 'otto',
          '9': 'nove', '10': 'dieci', '20': 'venti', '30': 'trenta', '100': 'cento', '1000': 'mille'}


def _num(w):
    """cifre e parole sono la stessa cosa («100» = «cento»)"""
    return [NUMERI.get(x, x) for x in w]


def finestre(intervalli, win=WIN, step=STEP):
    """finestre [a, d] che coprono ogni intervallo di parlato"""
    out = []
    for s, e in intervalli:
        a = s - 0.05
        while True:
            d = min(win, e + 0.05 - a)
            out.append((round(a, 3), round(max(d, 0.4), 3)))
            if a + win >= e + 0.05:
                break
            a += step
    return out


def unisci(blocchi, gap=0.6):
    out = []
    for s, e in sorted(blocchi):
        if out and s - out[-1][1] < gap:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def trascrivi_finestre(wav, intervalli, parallelo=4):
    fin = finestre(intervalli)
    testi = T.sonde(wav, fin, threads=3, parallelo=parallelo)
    return [[a, d, t] for (a, d), t in zip(fin, testi)]


def _piena(k):
    return any(w not in VUOTE and len(w) > 2 for w in k)


def dentro(testo, nmax=6):
    """le sequenze di 2..nmax parole ripetute dentro un testo breve (la piu lunga per posto)"""
    w = toks(testo)
    trovate = []
    for n in range(nmax, 1, -1):
        for i in range(len(w) - n + 1):
            k = tuple(w[i:i + n])
            if not _piena(k):
                continue
            for j in range(i + n, len(w) - n + 1):
                if tuple(w[j:j + n]) == k:
                    s = ' '.join(k)
                    if not any(s in x for x in trovate):
                        trovate.append(s)
                    break
    return trovate


def fra_blocchi(B, entro=ENTRO, nmax=6):
    """B = [[s, e, testo], ...] in ordine. Sequenze ripetute fra due blocchi
    DIVERSI entro `entro` s. -> [(t1, t2, parole)]"""
    parole = []
    for bi, (s, e, t) in enumerate(B):
        w = toks(t)
        for k, x in enumerate(w):
            parole.append((s + (e - s) * k / max(1, len(w)), bi, x))
    hits, visti = [], set()
    for n in range(nmax, 1, -1):
        for i in range(len(parole) - n + 1):
            seq = parole[i:i + n]
            if len({p[1] for p in seq}) != 1:
                continue
            k = tuple(p[2] for p in seq)
            if not _piena(k):
                continue
            for j in range(i + n, len(parole) - n + 1):
                if parole[j][0] - seq[0][0] > entro:
                    break
                seq2 = parole[j:j + n]
                if seq2[0][1] == seq[0][1] or len({p[1] for p in seq2}) != 1:
                    continue
                if tuple(p[2] for p in seq2) == k:
                    chiave = (round(seq[0][0]), round(seq2[0][0]))
                    s = ' '.join(k)
                    if not any(abs(a - chiave[0]) <= 1 and abs(b - chiave[1]) <= 1 and s in x
                               for a, b, x in visti):
                        visti.add((chiave[0], chiave[1], s))
                        hits.append((round(seq[0][0], 2), round(seq2[0][0], 2), s))
                    break
    return sorted(hits)


def ammessa(parole, t_src, ok):
    """True se la regia dichiara voluta questa ripetizione"""
    for r in ok:
        p = ' '.join(toks(r.get('parole', '')))
        if p and (p in parole or parole in p):
            if r.get('t') is None or t_src is None or abs(float(r['t']) - t_src) <= 4.0:
                return r.get('motivo', '')
    return None


def sotto_blocchi(env_db, blocchi, hop=0.010, fondo=None, min_len=0.5, prominenza=15.0, sopra_fondo=26.0):
    """spezza ogni blocco nelle micro-pause: minimi locali dell'inviluppo almeno
    `prominenza` dB sotto il picco a sinistra e a destra (entro 300 ms) e non piu di
    `sopra_fondo` dB sopra il fondo. Una ripresa che riparte senza pausa vera
    («Qui c'e un collega- / qui c'e un collegamento», 243,3 s) lascia proprio un
    minimo cosi. I pezzi restano di almeno `min_len` s (si tengono i minimi piu
    profondi). -> [[s, e], ...]"""
    import numpy as np
    db = np.convolve(env_db, np.ones(3) / 3, mode='same')
    fl = float(np.percentile(db, 12)) if fondo is None else fondo
    w = int(0.30 / hop)
    out = []
    for s, e in blocchi:
        i0, i1 = int(s / hop), int(e / hop)
        cand = []
        for i in range(i0 + 3, i1 - 3):
            if db[i] > db[i - 1] or db[i] > db[i + 1] or db[i] > fl + sopra_fondo:
                continue
            sx, dx = db[max(i0, i - w):i].max(), db[i + 1:min(i1, i + w)].max()
            if min(sx, dx) - db[i] >= prominenza:
                cand.append((db[i], i * hop))
        tagli = []
        for _, t in sorted(cand):
            pts = sorted(tagli + [t])
            lati = [s] + pts + [e]
            if all(b - a >= min_len for a, b in zip(lati, lati[1:])):
                tagli = pts
        lati = [s] + tagli + [e]
        out += [[round(a, 3), round(b, 3)] for a, b in zip(lati, lati[1:])]
    return out


# ------------------------------------------------------------------ controllo sul montato
def _muto(tg, a, b, limite):
    """il tratto [a, b] della sorgente non supera mai il limite (dB, inviluppo di Tagli)"""
    i, j = max(0, int(a / tg.HOP)), min(tg.m, int(b / tg.HOP))
    return j > i and float(tg.db[i:j].max()) <= limite


def sul_montato(P, E=None, scrivi=True):
    """Controllo «ripetizioni» del qc (fase 7b rivista). Il montato si ritrascrive
    pezzo per pezzo: i blocchi della sorgente spezzati nelle micro-pause
    (`sotto_blocchi`), riportati sul montato e trascritti ognuno da solo dalla voce
    montata. Poi, NON CONSEGNABILE se:
    - una sequenza di 2 o piu parole (con almeno una parola piena) si ripete entro
      10 s, dentro un pezzo o fra due pezzi, e la regia non la dichiara voluta
      (`ripetizioni_ok`);
    - una giunta butta via la coda o l'attacco di una parola (`edl.parole_tagliate`);
    - un pezzo parte o finisce a meta parola: energia alla giunta sopra il fondo +
      14 dB (`limite_giunta_db`).
    Torna (errori, righe del referto)."""
    from . import audio as A, edl as EDL
    from .progetto import ts
    E = E or P.leggi('edl.json')
    fps = P.fps
    env = A.inviluppo(P.asset('audio-16k-mono.wav'), 0.01)
    sb = sotto_blocchi(env, EDL.blocchi_solidi(P.leggi('blocchi.json')))
    pezzi = []                       # [montato_s, montato_e, sorgente_s]
    for sg in E['segmenti']:
        a, b = sg['in'], sg['in'] + sg['n'] / fps
        for s, e in sb:
            if e <= a + 0.05 or s >= b - 0.05:
                continue
            s2, e2 = max(s, a), min(e, b)
            pezzi.append([round(sg['edit_in'] + s2 - a, 3), round(sg['edit_in'] + e2 - a, 3), round(s2, 3)])
    wav = P.asset('voce-montata-16k.wav')
    testi = T.sonde(wav, [(s - 0.04, e - s + 0.08) for s, e, _ in pezzi], threads=3, parallelo=3)
    B = [[s, e, t] for (s, e, _), t in zip(pezzi, testi)]
    src_di = lambda t: next((p[2] + (t - p[0]) for p in pezzi if p[0] - 0.05 <= t <= p[1] + 0.05), None)
    ok = P.regia().get('ripetizioni_ok', [])
    trovate = []
    for s, e, t in B:
        for r in dentro(t):
            trovate.append((s, s, r, t))
    for t1, t2, r in fra_blocchi(B):
        if not any(abs(x[0] - t1) < 0.5 and r in x[2] for x in trovate):
            trovate.append((t1, t2, r, ' / '.join(b[2] for b in B if t1 - 0.1 <= b[0] <= t2 + 0.1)))
    righe, errori = [], 0
    for t1, t2, r, ctx in sorted(trovate):
        voluta = ammessa(r, src_di(t1), ok)
        if voluta is None:
            errori += 1
        righe.append(f"- {'ok, voluta' if voluta is not None else '**DA TAGLIARE**'} · {ts(t1)}"
                     + (f"-{ts(t2)}" if t2 != t1 else '') + f" (sorgente {src_di(t1) or 0:.2f}) · «{r}» · {ctx}"
                     + (f" · _{voluta}_" if voluta else ''))
    tagliate = [t for t in EDL.parole_tagliate(A.Tagli(P.asset('audio-16k-mono.wav')), E['giunte'])
                if t['i'] not in set(P.regia().get('giunte_ok', []))]
    # a meta parola: sopra il limite duro (fondo + 24 dB) sempre; fra il limite di
    # ascolto (+14) e il duro decide l'ascolto: ultima parola prima e prima parola
    # dopo la giunta, trascritte da sole sul montato, devono essere quelle della
    # sorgente (una parola monca esce diversa o sparisce)
    dubbie = [g for g in E['giunte'] if max(g['db_out'], g['db_in']) > E['limite_giunta_db']
              and g['i'] not in set(P.regia().get('giunte_ok', []))]
    meta, ascoltate = [], {}
    if dubbie:
        tg_ = A.Tagli(P.asset('audio-16k-mono.wav'))
        src = P.asset('audio-16k-asr.wav')
        fin = []
        for g in dubbie:
            fin += [(g['t'] - 1.4, 1.4), (g['t'], 1.4), (g['src_out'] - 1.4, 1.4), (g['src_in'], 1.4)]
        tx = T.sonde(wav, [f for k, f in enumerate(fin) if k % 4 < 2], threads=3, parallelo=3)
        ts_ = T.sonde(src, [f for k, f in enumerate(fin) if k % 4 >= 2], threads=3, parallelo=3)
        for k, g in enumerate(dubbie):
            mp, md, sp, sd = (_num(toks(x)) for x in (tx[2 * k], tx[2 * k + 1], ts_[2 * k], ts_[2 * k + 1]))
            # whisper sul bordo di una sonda a volte perde o aggiunge una parola: basta
            # che la prima (l'ultima) parola di una sia fra le prime (ultime) due dell'altra
            ok_fine = bool(mp and sp and (mp[-1] in sp[-2:] or sp[-1] in mp[-2:]))
            ok_inizio = bool(md and sd and (md[0] in sd[:2] or sd[0] in md[:2]))
            # un lato della sorgente tutto sotto il limite di ascolto e silenzio: li non
            # c'e una parola da troncare, e whisper sul vuoto inventa («Grazie»). Succede
            # quando la giunta cade dentro una pausa accorciata (G39 di YT_POSTURA_32, fase 7b)
            if _muto(tg_, g['src_out'] - 1.4, g['src_out'], E['limite_giunta_db']):
                ok_fine = True
            if _muto(tg_, g['src_in'], g['src_in'] + 1.4, E['limite_giunta_db']):
                ok_inizio = True
            ascoltate[g['i']] = (tx[2 * k], tx[2 * k + 1], ts_[2 * k], ts_[2 * k + 1])
            duro = max(g['db_out'], g['db_in']) > E['limite_duro_db'] and not g.get('oltre_soglia')
            if duro or not (ok_fine and ok_inizio):
                meta.append(g)
    errori += len(tagliate) + len(meta)
    L = [f"# Ripetizioni: {P.slug}", "",
         f"Montato ritrascritto pezzo per pezzo: **{len(B)} pezzi**, ognuno da solo "
         f"(blocchi spezzati nelle micro-pause). {len(E['giunte'])} giunte misurate.", "",
         f"**Esito: {'NON CONSEGNABILE' if errori else 'CONSEGNABILE'}** ({errori} da correggere)", "",
         "## Sequenze ripetute entro 10 s", ""] + (righe or ["- nessuna"]) + \
        ["", "## Parole tagliate alle giunte", ""] + \
        ([f"- G{t['i']:02d} {ts(t['t'])}: {t['voce_s'] * 1000:.0f} ms di voce buttati {t['lato']}" for t in tagliate] or ["- nessuna"]) + \
        ["", "## Pezzi che partono o finiscono a meta parola", ""] + \
        ([f"- **G{g['i']:02d}** {ts(g['t'])}: {g['db_out']}/{g['db_in']} dB; montato «{ascoltate.get(g['i'], ('',) * 4)[0]} | {ascoltate.get(g['i'], ('',) * 4)[1]}», sorgente «{ascoltate.get(g['i'], ('',) * 4)[2]} | {ascoltate.get(g['i'], ('',) * 4)[3]}»" for g in meta] or ["- nessuno"]) + \
        ["", f"Giunte sopra il limite di ascolto ({E['limite_giunta_db']} dB) ascoltate e pulite: "
         + (', '.join(f"G{i:02d} («{a} | {b}»)" for i, (a, b, c, d) in ascoltate.items() if i not in {g['i'] for g in meta}) or 'nessuna')] + \
        ["", "## Il montato pezzo per pezzo", ""] + [f"- {ts(s)} {t}" for s, e, t in B]
    if scrivi:
        P.controllo('ripetizioni.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    return errori, len(B), L


if __name__ == '__main__':
    import sys
    from .progetto import Progetto
    P_ = Progetto(sys.argv[1])
    n_err, n_b, _ = sul_montato(P_)
    print(f"ripetizioni: {n_b} pezzi, {n_err} da correggere -> controlli/ripetizioni.md")
    sys.exit(1 if n_err else 0)

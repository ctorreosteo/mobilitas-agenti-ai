"""Fase `papere`: trova papere, riprese doppie e regia a voce. Non taglia niente.

Il motore raccoglie le prove, l'agente decide. Sei segnali indipendenti, perche
nessuno basta da solo:

1. **sonda delle pause**: per ogni pausa sopra 1,2 s si trascrivono DA SOLI i 9 s
   prima e i 9 s dopo. Whisper non vede mai le due riprese insieme, quindi non le
   puo fondere. Se il DOPO ricomincia con le parole del PRIMA, e una ripresa doppia.
2. **parole di regia** ("ho sbagliato", "aspetta", "torna su", "stoppa"...).
3. **a-parte**: blocchi di parlato sotto 0,75 s isolati da silenzio lungo.
4. **ripetizioni**: lo stesso 4-gramma detto due volte entro 90 s.
5. **appianamento**: dove la trascrizione a finestre ha parole che quella intera
   non ha. E esattamente il punto in cui whisper ha riscritto una papera come
   frase corretta: in YT_TOFU_02 la papera a 13:39 stava solo li.
6. **copione** (se c'e `copione.md`): ogni frase del copione detta piu di una
   volta e una ripresa multipla; il parlato fuori copione e regia o papera.
7. **blocco contro blocco**: ogni blocco di parlato e trascritto da solo
   (`blocchi-testo.json`); se un blocco ricomincia come uno dei due precedenti,
   o li ripete, e una ripresa doppia. Prende anche quelle con pause di 0,8 s,
   che la sonda delle pause non guarda: in YT_TOFU_02 due erano uscite cosi nel v1.
8. **parola troncata** ("Si par...") e **attacco monco**: un blocco breve che e
   l'inizio del blocco dopo ("Si par..." / "si parte dal diaframma").
9. **interiezione o coda spuria isolata**: "no", "ok", "qua", un "di" sospeso
   fra due pause. Il "Si par... no" a 14:56 di YT_TOFU_02 e uscito nel v1 perche
   nessun segnale lo guardava.

Escono `data/papere.json` e `controlli/papere.md`, il referto che l'agente legge.
"""
import difflib
import re
import unicodedata

from .progetto import Progetto, ts
from . import trascrivi as T

PAUSA_SONDA = 1.2
SONDA = 9.0

REGIA = re.compile(
    r"\b((ho|hai|abbiamo) sbagliato|sbagliato io|aspetta|aspett\w|scusa\w*|torna (su|indietro|sopra)|tornare su|"
    r"stoppa|stop|rifaccio|rifacciamo|ricomincio|ricominciamo|riparto|ripartiamo|da capo|"
    r"un attimo|non mi ricordo|come si dice|vai ragazzi|vai pure|ok vai|okay|ciak|"
    r"abbiamo finito|ho finito|mi sa che|taglia|tagliamo|l'ho detto male|detto male|"
    r"non va bene|ancora una volta|un'altra volta|riprendiamo|ripeto)\b", re.I)
CONTEGGIO = re.compile(r"\b(uno|due|tre|quattro|1|2|3|4)\b[ ,]+(\b(due|tre|quattro|3|2|1|4)\b[ ,]+){2,}", re.I)
VUOTE = set("il lo la i gli le un uno una di a da in con su per tra fra e o ma che non si ci "
            "ti mi è e' del della dei delle al alla ai alle nel nella è".split())


def norm(t):
    t = unicodedata.normalize('NFD', t.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r"[^\w']", '', t)


def toks(s):
    return [x for x in (norm(w) for w in s.split()) if x]


def ripartenza(prima, dopo):
    """la frase con cui DOPO ricomincia cio che PRIMA aveva gia detto"""
    a, b = toks(prima)[-28:], toks(dopo)[:22]
    if len(a) < 3 or len(b) < 3:
        return None, 0.0
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    m = sm.find_longest_match(0, len(a), 0, len(b))
    piene = [w for w in a[m.a:m.a + m.size] if w not in VUOTE]
    if m.size >= 3 and len(piene) >= 2 and m.b <= 6:
        return ' '.join(a[m.a:m.a + m.size]), 1.0
    # versione sfumata: il DOPO riformula l'attacco del PRIMA
    head = b[:8]
    best = 0.0
    for i in range(0, max(1, len(a) - len(head) + 1)):
        r = difflib.SequenceMatcher(None, a[i:i + len(head)], head, autojunk=False).ratio()
        best = max(best, r)
    return (' '.join(head), best) if best >= 0.62 else (None, best)


def riattacco(a_txt, b_txt):
    """B ricomincia come A (stesso attacco) oppure riprende la coda di A"""
    a, b = toks(a_txt), toks(b_txt)
    if len(a) < 3 or len(b) < 3:
        return None, 0.0
    # stesso attacco: le prime 3+ parole uguali, con almeno 2 parole piene
    n = 0
    while n < min(len(a), len(b)) and a[n] == b[n]:
        n += 1
    if n >= 3 and sum(w not in VUOTE for w in a[:n]) >= 2:
        return ' '.join(a[:n]), 1.0
    # B riprende la coda di A ("...mancano ancora due ore e" / "mancano ancora due ore e mezza")
    sm = difflib.SequenceMatcher(None, a, b[:len(a) + 2], autojunk=False)
    m = sm.find_longest_match(0, len(a), 0, min(len(b), len(a) + 2))
    if m.size >= 4 and m.b <= 2 and sum(w not in VUOTE for w in a[m.a:m.a + m.size]) >= 2:
        return ' '.join(a[m.a:m.a + m.size]), 0.9
    # riformulazione dell'attacco (stessa frase detta con una parola diversa)
    k = min(len(a), len(b), 9)
    r = difflib.SequenceMatcher(None, a[:k], b[:k], autojunk=False).ratio()
    if k >= 5 and r >= 0.7:
        return ' '.join(b[:k]), 0.8
    return None, 0.0


def _solid(blocchi, min_block=0.12):
    # sotto 0,12 s un blocco e un respiro: per cercare le papere si ignora,
    # altrimenti un respiro spezza una pausa lunga in due pause corte
    return [b for b in blocchi if b[1] - b[0] >= min_block]


def _parole_in(W, a, b):
    return [w for w in W if w[1] > a and w[0] < b]


def _fmt_parole(W, a, b):
    ws = _parole_in(W, a, b)
    out, line = [], []
    for s, e, t in ws:
        line.append(f"[{s:.2f}] {t}")
        if len(line) == 8:
            out.append('    ' + ' '.join(line))
            line = []
    if line:
        out.append('    ' + ' '.join(line))
    return '\n'.join(out)


def appianamenti(Wf, Ws, min_len=4):
    """tratti presenti nella trascrizione a finestre e assenti in quella intera"""
    a = [norm(w[2]) for w in Wf]
    b = [norm(w[2]) for w in Ws]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ('delete', 'replace') and (i2 - i1) - (j2 - j1) >= min_len:
            seg = Wf[i1:i2]
            if seg[-1][1] - seg[0][0] > 0.8:
                out.append((seg[0][0], seg[-1][1], ' '.join(w[2] for w in seg)))
    return out


def ripetizioni(W, n=4, entro=90.0):
    nt = [norm(w[2]) for w in W]
    seen, out = {}, []
    for i in range(len(W) - n):
        key = tuple(nt[i:i + n])
        if any(not k for k in key) or sum(k not in VUOTE for k in key) < 2:
            continue
        if key in seen:
            j = seen[key]
            if 0 < W[i][0] - W[j][1] < entro:
                out.append((W[j][0], W[i][0] + 2.0, ' '.join(key)))
        seen[key] = i
    return out


def copione(P, W):
    path = P.p('copione.md')
    if not path.exists():
        return [], []
    testo = re.sub(r'(?m)^#.*$|\*|_|>', ' ', path.read_text(encoding='utf-8'))
    frasi = [f.strip() for f in re.split(r'(?<=[.!?])\s+', testo) if len(toks(f)) >= 5]
    nt = [norm(w[2]) for w in W]
    multiple, fuori = [], []
    usate = [False] * len(W)
    for f in frasi:
        ft = toks(f)
        k = len(ft)
        hits = []
        i = 0
        while i < len(W) - k // 2:
            win = nt[i:i + k]
            r = difflib.SequenceMatcher(None, ft, win, autojunk=False).ratio()
            if r >= 0.6:
                # allarga/stringi al massimo locale
                best, bi = r, i
                for d in range(1, 6):
                    if i + d < len(W):
                        r2 = difflib.SequenceMatcher(None, ft, nt[i + d:i + d + k], autojunk=False).ratio()
                        if r2 > best:
                            best, bi = r2, i + d
                hits.append((bi, best))
                for j in range(bi, min(len(W), bi + k)):
                    usate[j] = True
                i = bi + k
            else:
                i += 1
        if len(hits) > 1:
            multiple.append({'frase': f, 'prese': [
                {'s': W[h][0], 'e': W[min(len(W) - 1, h + k - 1)][1], 'somiglianza': round(r, 2)}
                for h, r in hits]})
    # parlato fuori copione: corse di parole non usate
    run = []
    for i, u in enumerate(usate + [True]):
        if not u and i < len(W):
            run.append(i)
        elif run:
            if len(run) >= 3:
                fuori.append((W[run[0]][0], W[run[-1]][1], ' '.join(W[j][2] for j in run)))
            run = []
    return multiple, fuori


def papere(slug):
    P = Progetto(slug)
    blocchi = P.leggi('blocchi.json')
    Wf = P.leggi('parole-finestre.json')
    Ws = P.leggi('parole-sorgente.json')
    dur = P.meta()['durata']
    asr = P.asset('audio-16k-asr.wav')
    solid = _solid(blocchi)
    seg = []   # (inizio, fine, tipo, peso, dettaglio)

    # 1+2. sonde delle pause
    pause = [(e1, s2) for (s1, e1), (s2, e2) in zip(solid, solid[1:]) if s2 - e1 > PAUSA_SONDA]
    print(f"sondo {len(pause)} pause sopra {PAUSA_SONDA}s (prima/dopo trascritti da soli)...")
    finestre = []
    for a, b in pause:
        finestre += [(max(0.0, a - SONDA), min(SONDA, a)), (b, SONDA)]
    testi = T.sonde(asr, finestre)
    sonde = []
    for k, (a, b) in enumerate(pause):
        prima, dopo = testi[2 * k], testi[2 * k + 1]
        frase, score = ripartenza(prima, dopo)
        tags = []
        if frase:
            tags.append(('ripresa doppia', 3.0 * score, f"ricomincia con «{frase}»"))
        for lato, txt in (('prima', prima), ('dopo', dopo)):
            for mm in REGIA.finditer(txt):
                tags.append(('regia', 2.0, f"«{mm.group(0)}» nel {lato.upper()}"))
        if b - a > 4.0:
            tags.append(('pausa lunga', 0.5, f"{b-a:.1f}s di silenzio"))
        sonde.append({'a': a, 'b': b, 'prima': prima, 'dopo': dopo, 'segnali': tags})
        for tipo, peso, det in tags:
            seg.append((max(0.0, a - 3.0), b + 3.0, tipo, peso, det))

    # 3. a-parte
    for i in range(1, len(solid) - 1):
        s, e = solid[i]
        if e - s < 0.75 and s - solid[i - 1][1] > 1.2 and solid[i + 1][0] - e > 1.2:
            parole = ' '.join(w[2] for w in _parole_in(Wf, s - 0.1, e + 0.1)) or '(non trascritto)'
            seg.append((s - 1, e + 1, 'a-parte', 1.5, f"blocco isolato di {e-s:.2f}s: «{parole}»"))

    # 2bis. regia nella trascrizione a finestre (prende anche quella senza pause)
    for i, (s, e, t) in enumerate(Wf):
        ctx = ' '.join(w[2] for w in Wf[max(0, i - 2):i + 4])
        mm = REGIA.search(ctx)
        if mm and norm(t) in toks(mm.group(0)):
            seg.append((s - 3, e + 3, 'regia', 1.5, f"«{mm.group(0)}»"))
    txt_all = ' '.join(w[2] for w in Wf)
    for mm in CONTEGGIO.finditer(txt_all):
        # il ciak "1 2 3 4 3 2 1" all'inizio
        pos = len(txt_all[:mm.start()].split())
        if pos < len(Wf):
            seg.append((Wf[pos][0] - 2, Wf[pos][0] + 6, 'ciak', 2.5, f"conteggio «{mm.group(0)[:40]}»"))

    # 4. ripetizioni
    for a, b, k in ripetizioni(Wf):
        seg.append((a, b, 'ripetizione', 1.0, f"«{k}» detto due volte"))

    # 5. appianamento
    for a, b, t in appianamenti(Wf, Ws):
        seg.append((a - 2, b + 2, 'appianata', 2.0,
                    f"solo nella trascrizione a finestre: «{t[:140]}»"))

    # 6. copione
    multiple, fuori = copione(P, Wf)
    for m in multiple:
        p0, p1 = m['prese'][0], m['prese'][-1]
        seg.append((p0['s'] - 1, p1['e'] + 1, 'copione: prese multiple', 3.0,
                    f"«{m['frase'][:90]}» detta {len(m['prese'])} volte: " +
                    ', '.join(f"{ts(p['s'])}-{ts(p['e'])} ({p['somiglianza']})" for p in m['prese'])))
    for a, b, t in fuori:
        seg.append((a - 1, b + 1, 'fuori copione', 1.5, f"«{t[:140]}»"))

    # 7. blocco contro blocco
    B = [b for b in P.leggi('blocchi-testo.json', []) if b[2]]
    for k in range(1, len(B)):
        for j in (k - 1, k - 2):
            if j < 0:
                continue
            frase, sc = riattacco(B[j][2], B[k][2])
            if frase:
                seg.append((B[j][0], B[k][1], 'blocco ripetuto', 3.0 * sc,
                            f"[{B[j][0]:.2f}] «{B[j][2][:90]}» → [{B[k][0]:.2f}] «{B[k][2][:90]}» "
                            f"(ricomincia con «{frase}»)"))
                break

    # 8. troncamenti e attacchi monchi
    for k, (bs, be, bt) in enumerate(B):
        if re.search(r'(\.\.\.|…)\s*$', bt) or re.search(r"\w-\s*$", bt):
            seg.append((bs - 0.5, be + 0.5, 'troncata', 2.5, f"[{bs:.2f}] «{bt[:90]}» finisce troncata"))
        for j in (k + 1, k + 2):      # anche con un "no" in mezzo
            if j >= len(B):
                break
            a_t, b_t = toks(bt), toks(B[j][2])
            ac = ''.join(a_t)
            if 1 <= len(a_t) <= 5 and len(ac) >= 4 and ''.join(b_t).startswith(ac[:-1]) and len(b_t) > len(a_t):
                seg.append((bs - 0.5, B[j][0] + 1, 'attacco monco', 2.5,
                            f"[{bs:.2f}] «{bt}» e l'inizio di [{B[j][0]:.2f}] «{B[j][2][:70]}»"))
                break
    # 9. interiezioni e code spurie isolate
    INTER = {'no', 'ok', 'okay', 'allora', 'dai', 'niente', 'eh', 'ehm', 'mh', 'cioe', 'quindi', 'boh',
             'qua', 'la', 'di', 'e', 'ma', 'si', 'aspetta', 'scusa', 'scusami', 'vai', 'perfetto', 'bene'}
    for k, (bs, be, bt) in enumerate(B):
        tt = toks(bt)
        if not tt or len(tt) > 2:
            continue
        prima = bs - B[k - 1][1] if k else 9.0
        dopo = B[k + 1][0] - be if k + 1 < len(B) else 9.0
        if all(t in INTER for t in tt) and (prima >= 0.6 or dopo >= 0.6):
            seg.append((bs - 0.5, be + 0.5, 'interiezione', 2.0,
                        f"[{bs:.2f}-{be:.2f}] «{bt}» isolato ({prima:.1f}s prima, {dopo:.1f}s dopo)"))
        elif be - bs < 0.5 and (prima >= 0.8 or dopo >= 0.8):
            seg.append((bs - 0.5, be + 0.5, 'coda spuria', 1.5,
                        f"[{bs:.2f}-{be:.2f}] «{bt}» breve e isolato ({prima:.1f}s prima, {dopo:.1f}s dopo)"))

    # testa e coda: tutto cio che precede la prima frase e segue l'ultima
    seg.append((0.0, min(dur, (Wf[0][0] if Wf else 0) + 14), 'testa', 1.0, "apertura del girato (ciak, saluti)"))
    seg.append((max(0.0, (Wf[-1][1] if Wf else dur) - 25), dur, 'coda', 1.0, "chiusura del girato"))

    # fusione in regioni
    seg.sort()
    regioni = []
    for s in seg:
        if regioni and s[0] <= regioni[-1]['b']:
            r = regioni[-1]
            r['b'] = max(r['b'], s[1])
            r['segnali'].append({'tipo': s[2], 'peso': round(s[3], 2), 'det': s[4]})
        else:
            regioni.append({'a': max(0.0, s[0]), 'b': min(dur, s[1]),
                            'segnali': [{'tipo': s[2], 'peso': round(s[3], 2), 'det': s[4]}]})
    for r in regioni:
        r['punteggio'] = round(sum(x['peso'] for x in r['segnali']), 2)
        r['tipi'] = sorted(set(x['tipo'] for x in r['segnali']))
    P.scrivi('papere.json', {'regioni': regioni, 'sonde': sonde, 'copione_multiple': multiple})
    _referto(P, regioni, sonde, Wf, Ws)
    forti = [r for r in regioni if r['punteggio'] >= 2.0]
    print(f"{len(regioni)} regioni sospette, {len(forti)} con punteggio >= 2 -> controlli/papere.md")
    if not P.p('copione.md').exists():
        print("  (nessun copione.md: il segnale 6 non ha girato)")


def _pause_in(blocchi, a, b, min_gap=0.3):
    sol = _solid(blocchi)
    out = [(e1, s2) for (_, e1), (s2, _) in zip(sol, sol[1:]) if s2 - e1 >= min_gap and e1 < b and s2 > a]
    return '  '.join(f"{x:.2f}→{y:.2f}" for x, y in out)


def _referto(P, regioni, sonde, Wf, Ws):
    blocchi = P.leggi('blocchi.json')
    L = [f"# Papere: {P.slug}", "",
         "Referto per decidere i tagli. Per ogni regione: i segnali, le sonde PRIMA/DOPO "
         "(trascritte da sole, quindi non appianate) e le parole con il tempo sorgente, "
         "per scegliere gli ancoraggi esatti in `regia.json`.", "",
         "Regola di lettura: se il DOPO ricomincia con le parole del PRIMA, e una ripresa "
         "doppia e si tiene la seconda; se contiene regia (\"ho sbagliato\", \"torna su\"), "
         "si toglie la regia e la ripresa monca che la precede.", ""]
    sonda_di = {round(s['a'], 2): s for s in sonde}
    for i, r in enumerate(sorted(regioni, key=lambda r: r['a'])):
        stelle = '★★★' if r['punteggio'] >= 4 else '★★' if r['punteggio'] >= 2 else '★'
        L.append(f"## R{i:02d} · {ts(r['a'])} → {ts(r['b'])} · {stelle} {r['punteggio']} · {', '.join(r['tipi'])}")
        L.append("")
        for x in r['segnali']:
            L.append(f"- **{x['tipo']}** — {x['det']}")
        for s in sonde:
            if r['a'] <= s['a'] <= r['b'] and s['segnali']:
                L.append("")
                L.append(f"Pausa {s['a']:.2f}s → {s['b']:.2f}s ({s['b']-s['a']:.1f}s)")
                L.append(f"> PRIMA: {s['prima']}")
                L.append(f">")
                L.append(f"> DOPO : {s['dopo']}")
        L.append("")
        L.append(f"Pause vere (inviluppo, oltre 0,3 s): {_pause_in(blocchi, r['a'], r['b']) or 'nessuna'}")
        L.append("")
        L.append("Blocchi di parlato, ognuno trascritto da solo (inizio-fine misurati: ancora qui i tagli):")
        for bs, be, bt in P.leggi('blocchi-testo.json', []):
            if be > r['a'] - 4 and bs < r['b'] + 4 and bt:
                L.append(f"    [{bs:8.2f}-{be:8.2f}] {bt}")
        L.append("")
        L.append("Parole (finestre), per i tagli dentro un blocco — tempi indicativi:")
        L.append(_fmt_parole(Wf, r['a'], r['b']) or '    (nessuna)')
        intera = ' '.join(w[2] for w in _parole_in(Ws, r['a'], r['b']))
        L.append("")
        L.append(f"Trascrizione intera nello stesso tratto: {intera[:600] or '(nessuna)'}")
        L.append("")
    P.controllo('papere.md').write_text('\n'.join(L), encoding='utf-8')

"""Fasi `edl` e `audio`: dalle decisioni di regia ai segmenti, e l'ascolto delle giunte.

`regia.json -> tagli` dice COSA togliere, con ancoraggi in secondi sorgente:
`da` = fine dell'ultimo parlato da tenere, `a` = inizio del parlato da cui si
riprende (`a: null` vuol dire fino in fondo). Qui si decide DOVE tagliare
esattamente:

1. l'ancoraggio si aggancia al confine del blocco di parlato misurato, se e
   vicino (i tempi per parola del DTW a volte collassano piu parole sullo
   stesso istante);
2. da li si cerca il primo istante di fondo di sala: tagliare sul confine del
   blocco tronca la coda della sillaba;
3. ogni segmento si quantizza sulla griglia dei frame d'uscita, cosi audio e
   video hanno la stessa durata al campione e 60 giunte non accumulano deriva.

Poi le pause troppo lunghe si accorciano secondo il profilo di ritmo.
"""
import re
import sys

from .progetto import Progetto, FPS, ts, ffmpeg
from . import audio as A
from . import trascrivi as T

RITMO = {
    # pausa_max: sopra questa la pausa si accorcia; resta: quanta ne rimane
    'calmo':   {'pausa_max': 1.30, 'resta': 0.65},
    'medio':   {'pausa_max': 0.85, 'resta': 0.45},
    'serrato': {'pausa_max': 0.60, 'resta': 0.32},
}
MIN_SEG = 1.0
SNAP = 0.35


def _ritmo(regia):
    r = regia.get('ritmo', 'medio')
    if isinstance(r, str):
        return dict(RITMO[r], nome=r)
    return dict(RITMO['medio'], **r, nome='personalizzato')


def costruisci(P, regia=None):
    regia = regia or P.regia()
    m = P.meta()
    dur = m['durata']
    num, den = (int(x) for x in m['fps_raw'].split('/'))
    src_fps = num / den
    tg = A.Tagli(P.asset('audio-16k-mono.wav'))
    solid = [b for b in P.leggi('blocchi.json') if b[1] - b[0] >= 0.12]
    ends = [b[1] for b in solid]
    starts = [b[0] for b in solid]
    R = _ritmo(regia)

    def snap(t, pool):
        near = min(pool, key=lambda x: abs(x - t)) if pool else t
        return near if abs(near - t) <= SNAP else t

    cuts = []
    for c in regia.get('tagli', []):
        da, a = c['da'], c.get('a')
        # esatto: il taglio cade dentro un blocco, su un micro-silenzio fra due
        # parole gia misurato a mano; non si cerca il fondo di sala
        # ("esatto": "da", "a" o true per entrambi)
        ex = c.get('esatto')
        if da <= 0.01:
            ca = 0.0
        elif ex in (True, 'da'):
            ca = da
        else:
            ca = tg.dopo(snap(da, ends), c.get('span', 0.6))
        if a is None:
            cb = dur
        elif ex in (True, 'a'):
            cb = a
        else:
            cb = tg.prima(snap(a, starts), c.get('span', 0.6))
        # rifinitura: il campione piu silenzioso vicino al punto trovato
        r = 0.03 if ex else 0.06
        if 0.0 < ca:
            ca = tg.quieto(ca, raggio=r)
        if cb < dur:
            cb = tg.quieto(cb, raggio=r)
        if cb <= ca:
            sys.exit(f"taglio incoerente: {c}")
        cuts.append({'in': round(ca, 3), 'out': round(cb, 3), 'motivo': c.get('motivo', ''),
                     'da': da, 'a': a})
    cuts.sort(key=lambda c: c['in'])

    keeps, pos = [], 0.0
    for c in cuts:
        if c['in'] > pos:
            keeps.append([pos, c['in']])
        pos = max(pos, c['out'])
    if pos < dur:
        keeps.append([pos, dur])

    tieni = [float(x) for x in regia.get('pause_da_tenere', [])]
    gaps = [(e1, s2) for (_, e1), (s2, _) in zip(solid, solid[1:]) if s2 - e1 > R['pausa_max']]
    segs, trimmed = [], []
    for ks, ke in keeps:
        cur = ks
        for gs, ge in gaps:
            if gs < ks or ge > ke or any(gs - 0.3 <= t <= ge + 0.3 for t in tieni):
                continue
            c1 = max(tg.dopo(gs, 0.6), gs + R['resta'] * 0.55)
            c2 = min(tg.prima(ge, 0.6), ge - R['resta'] * 0.45)
            # dentro la pausa possono esserci un respiro o un colpo sul tavolo:
            # si taglia sul punto piu silenzioso, senza uscire dalla pausa
            c1 = tg.quieto(c1, gs + 0.08, ge - 0.2)
            c2 = tg.quieto(c2, c1 + 0.1, ge - 0.08)
            if c2 - c1 < 0.15 or c1 - cur < MIN_SEG:
                continue
            segs.append([cur, c1])
            trimmed.append([round(c1, 3), round(c2, 3)])
            cur = c2
        if ke - cur > 0.05:
            segs.append([cur, ke])

    # griglia dei frame: inizio su un frame sorgente, durata in frame d'uscita
    out, t_edit = [], 0.0
    for a, b in segs:
        aq = round(a * src_fps) / src_fps
        n = max(1, int(round((b - aq) * FPS)))
        bq = aq + n / FPS
        out.append({'in': round(aq, 6), 'out': round(bq, 6), 'n': n, 'edit_in': round(t_edit, 6)})
        t_edit += n / FPS

    giunte = []
    for i in range(1, len(out)):
        s0, s1 = out[i - 1], out[i]
        kind = 'taglio' if any(abs(c['in'] - s0['out']) < 0.08 for c in cuts) else 'pausa'
        motivo = next((c['motivo'] for c in cuts if abs(c['in'] - s0['out']) < 0.08), '')
        giunte.append({'i': i, 't': round(s1['edit_in'], 3), 'src_out': s0['out'], 'src_in': s1['in'],
                       'db_out': round(tg.livello(s0['out'] - 0.012), 1),
                       'db_in': round(tg.livello(s1['in'] + 0.012), 1),
                       'tipo': kind, 'motivo': motivo})
    limite = tg.floor + 14.0          # sopra: da controllare
    limite_duro = tg.floor + 24.0     # sopra: il taglio e dentro una parola
    from .progetto import impronta, REGIA_DI
    edl = {'regia': impronta(regia, REGIA_DI['edl.json']), 'fps': FPS, 'src_fps': src_fps, 'durata_sorgente': dur, 'durata': round(t_edit, 6),
           'frame': sum(s['n'] for s in out), 'ritmo': R, 'fondo_db': round(tg.floor, 1),
           'limite_giunta_db': round(limite, 1), 'limite_duro_db': round(limite_duro, 1),
           'tagli': cuts, 'pause_accorciate': trimmed, 'segmenti': out, 'giunte': giunte}
    return edl


def edl(slug):
    P = Progetto(slug)
    E = costruisci(P)
    P.scrivi('edl.json', E)
    cut_s = sum(c['out'] - c['in'] for c in E['tagli'])
    pause_s = sum(b - a for a, b in E['pause_accorciate'])
    print(f"=== {len(E['tagli'])} tagli di regia (-{cut_s:.1f}s) ===")
    for c in E['tagli']:
        print(f"  {ts(c['in']):>9} -> {ts(c['out']):>9}  (-{c['out']-c['in']:5.1f}s)  {c['motivo'][:70]}")
    print(f"=== ritmo {E['ritmo']['nome']}: {len(E['pause_accorciate'])} pause oltre "
          f"{E['ritmo']['pausa_max']}s accorciate a {E['ritmo']['resta']}s (-{pause_s:.1f}s) ===")
    warn = [g for g in E['giunte'] if max(g['db_out'], g['db_in']) > E['limite_giunta_db']]
    bad = [g for g in warn if max(g['db_out'], g['db_in']) > E['limite_duro_db']]
    print(f"=== {len(E['giunte'])} giunte; energia residua massima "
          f"{max([max(g['db_out'], g['db_in']) for g in E['giunte']] or [-99]):.1f} dB "
          f"(limite {E['limite_giunta_db']} dB) ===")
    for g in warn:
        grave = g in bad
        print(f"  {'!!! DENTRO UNA PAROLA' if grave else '  da ascoltare'} giunta {g['i']} a {ts(g['t'])} "
              f"(sorgente {g['src_out']:.2f}/{g['src_in']:.2f}): {g['db_out']}/{g['db_in']} dB")
    print(f"sorgente {E['durata_sorgente']/60:.2f} min -> montato {E['durata']/60:.2f} min "
          f"({E['frame']} frame, {len(E['segmenti'])} segmenti) -> data/edl.json")
    if bad:
        sys.exit(1)


# ---------------------------------------------------------------- audio
def _grafo_audio(segs, catena):
    p = []
    for i, s in enumerate(segs):
        d = s['n'] / FPS
        p.append(f"[0:a]atrim=start={s['in']:.6f}:end={s['in'] + d:.6f},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d=0.010,afade=t=out:st={max(0, d - 0.010):.6f}:d=0.010[a{i}]")
    p.append(''.join(f"[a{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=0:a=1[cat]")
    p.append(f"[cat]{catena}[out]")
    return ';'.join(p)


def blocchi_montato(P, E, unisci=0.6, max_len=10.0):
    """I blocchi di parlato misurati sulla sorgente, riportati sul montato.

    Non si ricalcolano sull'audio montato: li le pause sono gia accorciate, il
    fondo di sala risulta 30 dB piu alto e la soglia finisce dentro le parole,
    spezzando proprio gli attacchi deboli ("Il", "La").
    """
    src = [b for b in P.leggi('blocchi.json') if b[1] - b[0] >= 0.12]
    out = []
    for sg in E['segmenti']:
        a, b = sg['in'], sg['in'] + sg['n'] / FPS
        for s, e in src:
            if e <= a or s >= b:
                continue
            out.append([sg['edit_in'] + max(s, a) - a, sg['edit_in'] + min(e, b) - a])
    pezzi = []
    for s, e in out:
        if pezzi and s - pezzi[-1][1] < unisci and e - pezzi[-1][0] <= max_len:
            pezzi[-1][1] = e
        else:
            pezzi.append([s, e])
    return [[round(s, 3), round(e, 3)] for s, e in pezzi]


def ripara_tempi(W):
    """il DTW a volte collassa piu parole sullo stesso istante: si ridistribuiscono
    fra la fine della parola prima e l'inizio di quella dopo, in proporzione alle lettere"""
    W = [list(w) for w in W]
    i = 0
    while i < len(W):
        j = i
        while j + 1 < len(W) and (W[j + 1][0] - W[i][0] < 0.04 or W[j][1] - W[j][0] < 0.03):
            j += 1
        if j > i:
            a = W[i][0]
            b = max(W[j][1], W[j + 1][0] - 0.02 if j + 1 < len(W) else W[j][1])
            if b - a < 0.08 * (j - i + 1):
                b = a + 0.08 * (j - i + 1)
            tot = sum(len(w[2]) for w in W[i:j + 1])
            t = a
            for w in W[i:j + 1]:
                d = (b - a) * len(w[2]) / tot
                w[0], w[1] = round(t, 3), round(t + d, 3)
                t += d
        i = j + 1
    return W


def audio(slug):
    P = Progetto(slug)
    E = P.leggi('edl.json')
    segs = E['segmenti']
    script = P.data('grafo-audio.txt')
    script.write_text(_grafo_audio(segs, A.CATENA_VOCE + ",aresample=48000"), encoding='utf-8')
    voce = P.asset('voce-montata.wav')
    print(f"monto l'audio: {len(segs)} segmenti, catena voce, -14 LUFS...")
    ffmpeg('-i', P.asset('audio-48k.wav'), '-/filter_complex', script, '-map', '[out]',
           '-c:a', 'pcm_s24le', '-ar', '48000', '-ac', '2', voce)
    ffmpeg('-i', voce, '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', P.asset('voce-montata-16k.wav'))
    got = A.loudness(voce)
    print(f"  {got['I']} LUFS, true peak {got['TP']} dBTP")

    wav16 = P.asset('voce-montata-16k.wav')
    bl = blocchi_montato(P, E)
    print(f"trascrivo il montato parola per parola, {len(bl)} pezzi ognuno da solo (per i sottotitoli)...")
    W = ripara_tempi(T.parole_a_blocchi(wav16, bl, prompt=T._prompt(P)))
    P.scrivi('parole-montato.json', W)
    print(f"  {len(W)} parole -> data/parole-montato.json")
    ascolta_giunte(P, E)


def ascolta_giunte(P, E):
    """Ogni giunta si ascolta in due modi, perche uno solo non basta:

    - 12 s attorno, trascritti da soli: la cucitura deve richiudersi in una frase;
    - 4 s prima e 4 s dopo, trascritti separatamente e confrontati. Una finestra
      lunga APPIANA la ripetizione: in YT_TOFU_02 v1 le sonde da 14 s davano tutte
      frasi pulite mentre il file conteneva "devi iniziare a pensare... devi
      iniziare a pensarlo". Con 2-4 s la ripetizione si sente.
    """
    from .papere import riattacco
    G = E['giunte']
    wav = P.asset('voce-montata-16k.wav')
    print(f"ascolto le {len(G)} giunte (12 s attorno + 4 s prima e 4 s dopo, ognuno da solo)...")
    fin = []
    for g in G:
        fin += [(max(0.0, g['t'] - 6.0), 12.0), (max(0.0, g['t'] - 4.0), 4.0), (g['t'], 4.0)]
    testi = T.sonde(wav, fin)
    L = [f"# Giunte: {P.slug}", "",
         "Per ogni giunta: la trascrizione indipendente di 12 s attorno, poi 4 s PRIMA e 4 s "
         "DOPO trascritti separatamente. Deve leggersi come una frase intera: niente parole "
         "ripetute a cavallo, niente parole monche, niente regia.", ""]
    sospette = 0
    for k, g in enumerate(G):
        t, pre, post = testi[3 * k:3 * k + 3]
        flag = []
        rip = _ripetizione(t) or _ripetizione(pre + ' ' + post)
        if rip:
            flag.append(f"RIPETE «{rip}»")
        ra, _ = riattacco(pre, post)
        if ra:
            flag.append(f"RIATTACCA «{ra}»")
        if re.search(r'(\.\.\.|…)\s*$', pre.strip()):
            flag.append("PRIMA TRONCATO")
        if max(g['db_out'], g['db_in']) > E['limite_giunta_db']:
            flag.append("ENERGIA ALTA")
        if T.ALLUCINAZIONI.search(t) or not t:
            flag.append("VUOTA")
        sospette += bool(flag)
        L.append(f"- **G{g['i']:02d}** {ts(g['t'])} · {g['tipo']} · {g['db_out']}/{g['db_in']} dB"
                 + (f" · **{' · '.join(flag)}**" if flag else ''))
        L.append(f"  {t}")
        L.append(f"  PRIMA: {pre} ⟂ DOPO: {post}")
        if g['motivo']:
            L.append(f"  _tolto: {g['motivo']}_")
    L.insert(4, f"**{len(G)} giunte ascoltate, {sospette} con segnali da controllare.**\n")
    P.controllo('giunte.md').write_text('\n'.join(L), encoding='utf-8')
    print(f"  {sospette} giunte con segnali su {len(G)} -> controlli/giunte.md")
    if not G:
        print("  ! zero giunte: o il montaggio non taglia niente o l'EDL non e stato letto")


def _ripetizione(t):
    from .papere import toks, VUOTE
    w = toks(t)
    for n in (5, 4, 3):
        seen = {}
        for i in range(len(w) - n + 1):
            k = tuple(w[i:i + n])
            if sum(x not in VUOTE for x in k) < 2:
                continue
            if k in seen and i - seen[k] >= n and i - seen[k] <= 14:
                return ' '.join(k)
            seen.setdefault(k, i)
    return None

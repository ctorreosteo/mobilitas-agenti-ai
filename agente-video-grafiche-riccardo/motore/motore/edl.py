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
import subprocess
import sys

from .progetto import Progetto, ts, ffmpeg
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
# code e attacchi: un micro-blocco di parlato (sotto MICRO) a meno di ATTACCATO da
# un blocco vero ne fa parte. In MR_POSTURA_01 la sillaba "-ra" di "postura"
# (59,87-59,95, 0,08 s) era scartata come rumore: la pausa dopo sembrava
# cominciare a 59,67 e il suo accorciamento la buttava via.
MICRO, ATTACCATO, RUMORE = 0.25, 0.40, 0.12
# un attacco vero e attaccato alla parola (occlusiva + vocale, < 0,15 s). In
# YT_POSTURA_32 (fase 7b rivista) un «T-» della prima presa a 0,31 s dalla ripresa
# veniva preso per l'attacco della parola dopo e restava nel montato: «T… Ti alzi»
ATTACCO = 0.15
# controllo "parola tagliata": voce nel tratto buttato accanto alla giunta.
# Taratura su MR_POSTURA_01 (v1): la coda "-ra" di "postura" (giunta 7) da 120 ms
# di voce chiusa a +25 dB; il frammento a 260 ms dalla fine in un taglio di regia
# (giunta 17, uno schiocco prima della ripresa scartata) da 50 ms. Soglia a meta.
CODA_FIN, CODA_DB, CODA_MIN = 0.40, 18.0, 0.080


def blocchi_solidi(B):
    """i blocchi di parlato su cui si decidono tagli e pause. Un micro-blocco che
    segue un blocco entro ATTACCATO e la sua coda (il blocco si allunga fino a
    lui); uno che precede un blocco entro ATTACCO (0,15 s) e il suo attacco. I
    micro-blocchi isolati sotto RUMORE restano rumore (colpi, respiri)."""
    B = sorted([list(b) for b in B])
    vero = lambda b: b[1] - b[0] >= MICRO
    out = []
    for b in B:                                   # code: in avanti
        if out and not vero(b) and out[-1][2] and b[0] - out[-1][1] <= ATTACCATO:
            out[-1][1] = max(out[-1][1], b[1])
        else:
            out.append([b[0], b[1], vero(b)])
    res = []
    for b in reversed(out):                       # attacchi: all'indietro
        if res and not b[2] and res[-1][2] and res[-1][0] - b[1] <= ATTACCO:
            res[-1][0] = min(res[-1][0], b[0])
        else:
            res.append(b)
    return [[round(a, 3), round(e, 3)] for a, e, _ in reversed(res) if e - a >= RUMORE]


def _frammenti(tg, a, b, lato):
    """ms di voce (sopra il fondo + CODA_DB) in [a, b] che sta tutta dentro la
    finestra dal lato lontano dalla giunta: un frammento chiuso, cioe una coda o un
    attacco buttati. Una voce che continua oltre la finestra e invece un'altra frase
    (la ripresa scartata di un taglio di regia) e non conta."""
    import numpy as np
    H = tg.HOP
    i0, i1 = max(0, int(round(a / H))), min(tg.m, int(round(b / H)))
    v = tg.db[i0:i1] > tg.floor + CODA_DB
    if not v.any():
        return 0.0, None
    tot, j = 0, 0
    while j < len(v):
        if not v[j]:
            j += 1
            continue
        k = j
        while k < len(v) and v[k]:
            k += 1
        aperto = (k == len(v)) if lato == 'fine' else (j == 0)
        if not aperto:
            tot += k - j
        j = k
    picco = float(tg.db[i0:i1].max() - tg.floor)
    return round(tot * H, 3), round(picco, 1)


def parole_tagliate(tg, giunte):
    """per ogni giunta, la voce nel tratto buttato subito dopo la fine tenuta e
    subito prima dell'inizio (CODA_FIN s). Whisper non basta: completa la parola
    anche quando manca la sillaba. Soglie e taratura: CODA_FIN, CODA_DB, CODA_MIN."""
    out = []
    for g in giunte:
        a, b = g['src_out'], g['src_in']
        w = min(CODA_FIN, (b - a) / 2)
        for lato, x0, x1 in (('fine', a, a + w), ('inizio', b - w, b)):
            ms, picco = _frammenti(tg, x0, x1, lato)
            if ms >= CODA_MIN:
                out.append({'i': g['i'], 't': g['t'], 'lato': lato, 'da': round(x0, 3), 'a': round(x1, 3),
                            'voce_s': ms, 'picco_db': picco})
    return out


def _ritmo(regia):
    r = regia.get('ritmo', 'medio')
    if isinstance(r, str):
        return dict(RITMO[r], nome=r)
    return dict(RITMO['medio'], **r, nome='personalizzato')


def costruisci(P, regia=None):
    regia = regia or P.regia()
    m = P.meta()
    fps = P.fps
    dur = m['durata']
    num, den = (int(x) for x in m['fps_raw'].split('/'))
    src_fps = num / den
    tg = A.Tagli(P.asset('audio-16k-mono.wav'))
    solid = blocchi_solidi(P.leggi('blocchi.json'))
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
        # estremi fuori dai respiri e dagli schiocchi (fase 7b rivista): la fine
        # tenuta torna prima del rumore, l'inizio tenuto va dopo
        # (mai verso la parola: la fine tenuta si allunga fino a dopo il rumore,
        # l'inizio tenuto parte prima del respiro)
        if 0.0 < ca and ex not in (True, 'da'):
            r_ = tg.respiro(ca)
            if r_:
                ca = tg.quieto(r_[1] + 0.02, raggio=0.02)
        if cb < dur and ex not in (True, 'a'):
            r_ = tg.respiro(cb)
            if r_:
                cb = tg.quieto(r_[0] - 0.02, raggio=0.02)
        if cb <= ca:
            sys.exit(f"taglio incoerente: {c}")
        cuts.append({'in': round(ca, 3), 'out': round(cb, 3), 'motivo': c.get('motivo', ''),
                     'da': da, 'a': a, 'oltre_soglia': c.get('oltre_soglia')})
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
            if ge <= ks or gs >= ke or any(gs - 0.3 <= t <= ge + 0.3 for t in tieni):
                continue
            # una pausa che attraversa un taglio (il taglio «esatto» parte dentro il
            # silenzio) si accorcia sul tratto tenuto: prima si saltava, e a 4:32 di
            # YT_POSTURA_32 restavano 4 s di silenzio (fase 7b, note di Riccardo)
            gs, ge = max(gs, ks), min(ge, ke)
            if ge - gs <= R['pausa_max']:
                continue
            c1 = max(tg.dopo(gs, 0.6), gs + R['resta'] * 0.55)
            c2 = min(tg.prima(ge, 0.6), ge - R['resta'] * 0.45)
            # dentro la pausa possono esserci un respiro o un colpo sul tavolo:
            # si taglia sul punto piu silenzioso, senza uscire dalla pausa
            c1 = tg.quieto(c1, gs + 0.08, ge - 0.2)
            c2 = tg.quieto(c2, c1 + 0.1, ge - 0.08)
            # un respiro dentro la pausa resta intero o si toglie intero, mai a meta
            # (fase 7b rivista, note di Riccardo sulle pause tagliate male)
            for lato in ('c1', 'c2'):
                t_ = c1 if lato == 'c1' else c2
                r_ = tg.respiro(t_)
                if r_ and gs < r_[0] and r_[1] < ge:
                    if lato == 'c1':
                        c1 = r_[0] - 0.02          # il respiro cade nel tratto tolto
                    else:
                        c2 = r_[1] + 0.02
            if c2 - c1 >= 0.15 and (tg.respiro(c1) or tg.respiro(c2)):
                c1, c2 = c1, c1                    # non si trova un punto pulito: la pausa resta
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
        n = max(1, int(round((b - aq) * fps)))
        bq = aq + n / fps
        out.append({'in': round(aq, 6), 'out': round(bq, 6), 'n': n, 'edit_in': round(t_edit, 6)})
        t_edit += n / fps

    giunte = []
    for i in range(1, len(out)):
        s0, s1 = out[i - 1], out[i]
        kind = 'taglio' if any(abs(c['in'] - s0['out']) < 0.08 for c in cuts) else 'pausa'
        motivo = next((c['motivo'] for c in cuts if abs(c['in'] - s0['out']) < 0.08), '')
        # «oltre_soglia»: la regia accetta un taglio nel parlato attaccato (nessun
        # silenzio fra le due parole), con il motivo; la sonda sul montato lo verifica
        oltre = next((c['oltre_soglia'] for c in cuts if abs(c['in'] - s0['out']) < 0.08 and c.get('oltre_soglia')), None)
        giunte.append({'i': i, 't': round(s1['edit_in'], 3), 'src_out': s0['out'], 'src_in': s1['in'],
                       'db_out': round(tg.livello(s0['out'] - 0.012), 1),
                       'db_in': round(tg.livello(s1['in'] + 0.012), 1),
                       'tipo': kind, 'motivo': motivo, **({'oltre_soglia': oltre} if oltre else {})})
    for t in parole_tagliate(tg, giunte):
        giunte[t['i'] - 1].setdefault('parola_tagliata', []).append(t)
    limite = tg.floor + 14.0          # sopra: da controllare
    limite_duro = tg.floor + 24.0     # sopra: il taglio e dentro una parola
    from .progetto import impronta, REGIA_DI
    edl = {'regia': impronta(regia, REGIA_DI['edl.json']), 'fps': fps, 'src_fps': src_fps, 'durata_sorgente': dur, 'durata': round(t_edit, 6),
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
    bad = [g for g in warn if max(g['db_out'], g['db_in']) > E['limite_duro_db'] and not g.get('oltre_soglia')]
    print(f"=== {len(E['giunte'])} giunte; energia residua massima "
          f"{max([max(g['db_out'], g['db_in']) for g in E['giunte']] or [-99]):.1f} dB "
          f"(limite {E['limite_giunta_db']} dB) ===")
    for g in warn:
        grave = g in bad
        if g.get('oltre_soglia'):
            print(f"    oltre la soglia, dichiarato in regia: giunta {g['i']} a {ts(g['t'])}: {g['oltre_soglia'][:70]}")
            continue
        print(f"  {'!!! DENTRO UNA PAROLA' if grave else '  da ascoltare'} giunta {g['i']} a {ts(g['t'])} "
              f"(sorgente {g['src_out']:.2f}/{g['src_in']:.2f}): {g['db_out']}/{g['db_in']} dB")
    for g in E['giunte']:
        for t in g.get('parola_tagliata', []):
            print(f"  !!! PAROLA TAGLIATA giunta {g['i']} a {ts(g['t'])}: {t['voce_s'] * 1000:.0f} ms di voce "
                  f"(+{t['picco_db']} dB) buttati {'dopo la fine' if t['lato'] == 'fine' else 'prima dell inizio'} "
                  f"(sorgente {t['da']:.2f}-{t['a']:.2f})")
    print(f"sorgente {E['durata_sorgente']/60:.2f} min -> montato {E['durata']/60:.2f} min "
          f"({E['frame']} frame, {len(E['segmenti'])} segmenti) -> data/edl.json")
    if bad:
        sys.exit(1)


# ---------------------------------------------------------------- audio
def _grafo_audio(segs, catena, fps):
    p = []
    for i, s in enumerate(segs):
        d = s['n'] / fps
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
    fps = P.fps
    src = blocchi_solidi(P.leggi('blocchi.json'))
    out = []
    for sg in E['segmenti']:
        a, b = sg['in'], sg['in'] + sg['n'] / fps
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


def controlla_parole_tagliate(P, E):
    """le giunte con voce buttata accanto (misurata ora sulla sorgente), tolte
    quelle che la regia dichiara volute in `giunte_ok`"""
    tg = A.Tagli(P.asset('audio-16k-mono.wav'))
    ok = set(P.regia().get('giunte_ok', []))
    return [t for t in parole_tagliate(tg, E['giunte']) if t['i'] not in ok]


PAUSA_LUNGA = 0.9


def pause_lunghe(P, E, voce=None, oltre=PAUSA_LUNGA):
    """i silenzi del montato sopra `oltre` secondi (fase 7b, note di Riccardo: 4 s
    muti a 4:32 di YT_POSTURA_32). Si misura la VOCE montata, non il mix (i suoni
    riempirebbero il silenzio), con la soglia di parlato della sorgente (fondo +
    22 dB, la stessa dei blocchi): la soglia del montato e piu alta, perche le
    pause accorciate alzano il suo fondo. Ogni silenzio torna con i tempi sorgente
    dei due lati; quelli in `regia.json -> pause_lunghe_ok` ({t: secondi sorgente,
    motivo}) sono voluti."""
    import numpy as np
    src = P.asset('audio-16k-mono.wav')
    _, _, soglia = A.blocchi(src)
    voce = voce or P.asset('voce-montata-16k.wav')
    if not voce.exists() or voce.stat().st_mtime < P.asset('voce-montata.wav').stat().st_mtime:
        ffmpeg('-i', P.asset('voce-montata.wav'), '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', voce)
    hop = 0.01
    db = A.inviluppo(voce, hop)
    muto = np.concatenate([[False], db <= soglia, [False]])
    d = np.diff(muto.astype(int))
    inizi, fini = np.where(d == 1)[0], np.where(d == -1)[0]
    segs = E['segmenti']

    def sorgente(t):
        s = max((s for s in segs if s['edit_in'] <= t + 1e-6), key=lambda s: s['edit_in'], default=segs[0])
        return s['in'] + (t - s['edit_in'])
    voluti = P.regia().get('pause_lunghe_ok', [])
    out = []
    for i, j in zip(inizi, fini):
        a, b = float(i * hop), float(j * hop)
        if b - a <= oltre or a < 0.05 or b > E['durata'] - 0.05:
            continue              # testa e coda del file non sono pause fra due frasi
        sa, sb = float(sorgente(a)), float(sorgente(max(a, b - 0.01)))
        ok = next((v for v in voluti if sa - 0.3 <= v['t'] <= sb + 0.3 and v.get('motivo')), None)
        out.append({'t': round(a, 2), 'fino': round(b, 2), 'durata': round(b - a, 2),
                    'src': [round(sa, 2), round(sb, 2)], 'motivo': ok['motivo'] if ok else None})
    return out, round(float(soglia), 1)


def audio(slug):
    P = Progetto(slug)
    E = P.leggi('edl.json')
    segs = E['segmenti']
    rotte = controlla_parole_tagliate(P, E)
    if rotte:
        for t in rotte:
            print(f"  !!! PAROLA TAGLIATA giunta {t['i']} a {ts(t['t'])}: {t['voce_s'] * 1000:.0f} ms di voce "
                  f"(+{t['picco_db']} dB) nel tratto buttato {'dopo la fine' if t['lato'] == 'fine' else 'prima dell inizio'} "
                  f"(sorgente {t['da']:.2f}-{t['a']:.2f})")
        sys.exit("la fase si ferma: una giunta butta via la coda o l'attacco di una parola. Ascolta il tratto; "
                 "se la voce e voluta (una ripresa scartata) metti il numero della giunta in `giunte_ok`, "
                 "altrimenti correggi il taglio in regia.json e rifai `edl`.")
    script = P.data('grafo-audio.txt')
    catena = A.catena_voce(P.meta())
    script.write_text(_grafo_audio(segs, catena + ",aresample=48000", P.fps), encoding='utf-8')
    voce = P.asset('voce-montata.wav')
    print(f"monto l'audio: {len(segs)} segmenti, catena voce, -14 LUFS...")
    ffmpeg('-i', P.asset('audio-48k.wav'), '-/filter_complex', script, '-map', '[out]',
           '-c:a', 'pcm_s24le', '-ar', '48000', '-ac', '2', voce)
    # una catena rotta puo uscire vuota senza errori di ffmpeg: si misura
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                          str(voce)], capture_output=True, text=True).stdout.strip()
    try:
        dv = float(out)
    except ValueError:            # file vuoto: ffprobe scrive N/A
        dv = 0.0
    if abs(dv - E['durata']) > 0.05:
        sys.exit(f"  !!! voce montata di {dv:.2f}s invece di {E['durata']:.2f}s (EDL): la catena voce "
                 f"ha perso audio. Catena: {catena}")
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

"""Tappa 1 dell'agente reel-grafiche: la radiografia di un ad già montato (fase 4, 04/11/2026).

È il procedimento della fase 0 (report/2026-11-03-fase0-radiografia-ad-cervicalgia.md) messo nel motore.

Il motore misura:
- i tagli: differenza fra fotogrammi a 270×480, picchi netti;
- per ogni inquadratura lo schema (A, B o C) e le finestre arrotondate, misurate sui pixel con la
  media del gradiente; il raggio è la media delle 8 stime d'angolo;
- i sottotitoli impressi: Apple Vision legge il testo, e inizio e fine li misura la maschera delle
  lettere bianche, perché Vision perde i fotogrammi con il fumo chiaro;
- la voce: whisper large-v3 su tutto l'audio, poi sonde brevi da 2,4 s o più dove la voce e l'SRT
  non coincidono; l'inizio delle parole si rifinisce sull'inviluppo a 20 ms;
- il confronto SRT ↔ video ↔ voce, i colori del fondo e le zone (zona sicura Meta, fessura dei
  sottotitoli, finestra grande per il modo «finestra»).

L'agente controlla. Guarda i provini, segna le animazioni 3D (`./mve reel-3d <slug> 3,9` oppure
`nessuna`) e corregge solo segnalando: il motore non cambia mai l'SRT né il video.
"""
import datetime
import difflib
import json
import statistics
import subprocess
import sys

import numpy as np

from . import reel_comune as C
from .reel_comune import W, H, SAFE

# Schemi del formato degli ads Mobilitas (fase 0): rettangoli attesi (x0, y0, x1, y1 inclusi) delle
# finestre, poi affinati sui pixel. Uno schema nuovo si aggiunge qui.
SCHEMI = {
    'A': [(30, 376, 1050, 923), (50, 1008, 522, 1491), (557, 1008, 1029, 1491)],
    'B': [(29, 374, 1051, 920), (29, 998, 1051, 1546)],
    'C': [(30, 445, 1049, 1469)],
}
FORZA_MIN = 25          # bordo medio minimo perché uno schema sia riconosciuto (fase 0: 60-130 quello giusto)
SOGLIA_TAGLIO = 15      # differenza media a 270x480 (fase 0: tagli 28-90, fotogrammi normali mediana 1,2, max 6)


# ---------------------------------------------------------------- tagli

def misura_tagli(video):
    w, h = 270, 480
    prev, d = None, []
    for a in C.fotogrammi_rgb(video, vf='scale=270:480:flags=area', w=w, h=h):
        a = a.astype(np.int16)
        if prev is not None:
            d.append(float(np.abs(a - prev).mean()))
        prev = a
    d = np.array(d)
    tagli = [i + 1 for i in range(len(d)) if d[i] > SOGLIA_TAGLIO and d[i] == d[max(0, i - 2):i + 3].max()]
    dubbi = [i + 1 for i in range(len(d)) if 6 < d[i] <= SOGLIA_TAGLIO]
    return tagli, {'mediana': round(float(np.median(d)), 2), 'picchi': [round(float(d[t - 1]), 1) for t in tagli],
                   'max_fuori_tagli': round(float(np.max(np.delete(d, [t - 1 for t in tagli]))) if len(tagli) < len(d) else 0, 2),
                   'dubbi_dissolvenza': dubbi}


# ---------------------------------------------------------------- finestre

def _gradienti(video, confini):
    """media del gradiente orizzontale e verticale per inquadratura (salta i 2 fotogrammi dopo il taglio)"""
    out, s, n = [], 0, 0
    gx = gy = None
    cnt = 0
    for a in C.fotogrammi_rgb(video):
        while n >= confini[s + 1]:
            out.append((gx / max(cnt, 1), gy / max(cnt, 1)))
            s += 1
            gx = None
        if gx is None:
            gx = np.zeros((H, W), np.float32); gy = np.zeros((H, W), np.float32); cnt = 0
        if n - confini[s] >= 2:
            a = a.astype(np.float32)
            gx[:, 1:] += np.abs(a[:, 1:] - a[:, :-1]).sum(2)
            gy[1:, :] += np.abs(a[1:] - a[:-1]).sum(2)
            cnt += 1
        n += 1
    out.append((gx / max(cnt, 1), gy / max(cnt, 1)))
    return out


def _picco(P, c, r=25):
    lo, hi = max(1, c - r), min(len(P) - 1, c + r + 1)
    i = lo + int(np.argmax(P[lo:hi]))
    return i, float(P[i])


def _affina(gx, gy, x0, y0, x1, y1):
    m = 90
    top, st = _picco(gy[:, x0 + m:x1 - m].mean(1), y0)
    bot, sb = _picco(gy[:, x0 + m:x1 - m].mean(1), y1 + 1)
    lef, sl = _picco(gx[y0 + m:y1 - m, :].mean(0), x0)
    rig, sr = _picco(gx[y0 + m:y1 - m, :].mean(0), x1 + 1)
    return (lef, top, rig - 1, bot - 1), (st + sb + sl + sr) / 4


def _raggio(gx, gy, r):
    x0, y0, x1, y1 = r
    stime = []
    D = np.arange(0, 140)
    for (cx, cy, sx, sy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        for asse in ('righe', 'colonne'):
            pos = []
            for d in D:
                if asse == 'righe':
                    y = cy + sy * d
                    xs = np.arange(cx - 3 * sx, cx + 130 * sx, sx) + (1 if sx < 0 else 0)
                    v = gx[y, np.clip(xs, 0, W - 1)]
                    pos.append(abs(int(xs[int(np.argmax(v))]) - (cx + (1 if sx < 0 else 0))))
                else:
                    x = cx + sx * d
                    ys = np.arange(cy - 3 * sy, cy + 130 * sy, sy) + (1 if sy < 0 else 0)
                    v = gy[np.clip(ys, 0, H - 1), x]
                    pos.append(abs(int(ys[int(np.argmax(v))]) - (cy + (1 if sy < 0 else 0))))
            pos = np.array(pos, float)
            best = None
            for R in np.arange(5, 130, 0.5):
                mod = np.where(D < R, R - np.sqrt(np.maximum(R ** 2 - (R - D) ** 2, 0)), 0)
                e = np.mean(np.minimum(np.abs(mod - pos), 15))
                if best is None or e < best[1]:
                    best = (R, e)
            stime.append(float(best[0]))
    # la mediana a volte sceglie una stima anomala in basso (fase 0, inquadratura 4): si scartano le stime
    # lontane piu di 10 px dalla mediana e si fa la media delle altre
    med = float(np.median(stime))
    buone = [s for s in stime if abs(s - med) <= 10] or stime
    return round(float(np.mean(buone)), 1), stime


def misura_finestre(video, confini):
    out = []
    for s, (gx, gy) in enumerate(_gradienti(video, confini)):
        prove = {}
        for nome, rr in SCHEMI.items():
            ff = [_affina(gx, gy, *r) for r in rr]
            prove[nome] = (float(np.mean([f[1] for f in ff])), [f[0] for f in ff])
        nome = max(prove, key=lambda k: prove[k][0])
        fin = []
        for r in prove[nome][1]:
            R, st = _raggio(gx, gy, r)
            x0, y0, x1, y1 = r
            fin.append({'x': x0, 'y': y0, 'w': x1 - x0 + 1, 'h': y1 - y0 + 1, 'x1': x1, 'y1': y1, 'raggio': R,
                        'raggi_8_stime': st})
        forza = {k: round(v[0], 1) for k, v in prove.items()}
        out.append({'n': s + 1, 'f0': confini[s], 'f1': confini[s + 1] - 1, 'schema': nome if forza[nome] >= FORZA_MIN else None,
                    'schema_probabile': nome, 'forza': forza, 'finestre': fin})
    return out


def rett_grafica(f):
    """il rettangolo di una grafica «finestra»: la finestra misurata (primo pixel dentro) allargata di 1 px
    per lato, cosi copre anche il bordo sfumato (fase 1 e 3: x28 y373 1024x549/550 r66-67)"""
    return {'x': f['x'] - 1, 'y': f['y'] - 1, 'w': f['w'] + 2, 'h': f['h'] + 2, 'r': round(f['raggio'])}


# ---------------------------------------------------------------- sottotitoli

def _testo_simile(a, b):
    a, b = ' '.join(C.parole_di(a)), ' '.join(C.parole_di(b))
    return difflib.SequenceMatcher(a=a, b=b).ratio()


def misura_sottotitoli(video, srt, fps, nf, L):
    """per ogni riga dell'SRT: testo letto a schermo (Vision), fotogrammi a schermo (maschera dei bianchi),
    riquadro delle lettere; poi la fascia dei sottotitoli e l'altezza delle lettere"""
    from PIL import Image
    # 1. tre fotogrammi interi per riga (meta, meta-5, meta+5): Vision trova la riga e il suo riquadro
    d = L / 'sott'; d.mkdir(exist_ok=True)
    for p in d.glob('*.png'):
        p.unlink()
    scelti = {}
    for r in srt:
        fa, fb = int(np.ceil(r['a'] * fps - 1e-6)), int(np.ceil(r['b'] * fps - 1e-6)) - 1
        m = (fa + fb) // 2
        scelti[r['n']] = sorted({max(fa, min(fb, k)) for k in (m - 5, m, m + 5)})
    tutti = sorted({f for v in scelti.values() for f in v})
    for f, im in C.estrai(video, tutti).items():
        im.save(d / f'f{f:05d}.png')
    letto = C.vision(d, L / 'sott-vision.json')
    out = []
    for r in srt:
        best = None
        for f in scelti[r['n']]:
            for o in letto.get(f'f{f:05d}.png', []):
                s = _testo_simile(o['t'], r['t'])
                if best is None or s > best[0]:
                    best = (s, f, o)
        out.append({'n': r['n'], 'srt': r['t'].strip(), 'srt_a': r['a'], 'srt_b': r['b'],
                    'srt_f0': int(np.ceil(r['a'] * fps - 1e-6)), 'srt_f1': int(np.ceil(r['b'] * fps - 1e-6)) - 1,
                    'letto': best[2]['t'] if best else None, 'somiglianza': round(best[0], 3) if best else 0,
                    'f_rif': best[1] if best else None,
                    'vision_box': [round(best[2]['x']), round(best[2]['y']), round(best[2]['x'] + best[2]['w']),
                                   round(best[2]['y'] + best[2]['h'])] if best else None})
    buoni = [o for o in out if o['somiglianza'] >= 0.8]
    if not buoni:
        return out, None
    fy0 = min(o['vision_box'][1] for o in buoni) - 12
    fy1 = max(o['vision_box'][3] for o in buoni) + 12
    # collaudo (04/11/2026): il ritaglio in YUV 4:2:0 vuole righe pari. Con un'altezza dispari ffmpeg ne toglie una,
    # i fotogrammi letti si sfasano e se ne perde uno (AD_REFLUSSO: fascia 913-1020, 107 righe)
    vy = [fy0 + 12, fy1 - 12]
    fy0 -= fy0 % 2
    fy1 += (fy1 - fy0) % 2
    # 2. maschera dei bianchi (R, G, B >= 235) nella fascia, su tutti i fotogrammi
    fascia = []
    for a in C.fotogrammi_rgb(video, vf=f'crop={W}:{fy1 - fy0}:0:{fy0}', h=fy1 - fy0):
        fascia.append(np.packbits(a.min(2) >= 235, axis=1))
    unp = lambda f: np.unpackbits(fascia[f], axis=1)[:, :W].astype(bool)
    for o in out:
        if not o['vision_box'] or o['somiglianza'] < 0.8:
            o['fotogrammi_misurati'] = None
            continue
        x0, y0, x1, y1 = o['vision_box']
        x0, x1 = max(0, x0 - 8), min(W, x1 + 8)
        ya, yb = max(0, y0 - fy0), min(fy1 - fy0, y1 - fy0)     # dentro il riquadro di Vision: fuori ci sono i bordi delle finestre
        ref = unp(o['f_rif'])[ya:yb, x0:x1]
        pres = {}
        for f in range(max(0, o['srt_f0'] - 25), min(nf - 1, o['srt_f1'] + 25) + 1):
            m = unp(f)[ya:yb, x0:x1]
            pres[f] = float((m & ref).sum() / max(1, (m | ref).sum()))
        a = b = o['f_rif']
        while a - 1 in pres and pres[a - 1] >= 0.5:
            a -= 1
        while b + 1 in pres and pres[b + 1] >= 0.5:
            b += 1
        righe = np.nonzero(ref.sum(1) >= 3)[0]
        cols = np.nonzero(ref.any(0))[0]
        box = [int(cols.min() + x0), int(righe.min() + ya + fy0), int(cols.max() + x0), int(righe.max() + ya + fy0)] if len(righe) else None
        # altezza delle lettere a meta contrasto (min(R,G,B) >= 128), come nella fase 1 («medicine» = 45 px)
        im = np.asarray(Image.open(d / f"f{o['f_rif']:05d}.png").convert('RGB'))[y0:y1, x0:x1].min(2) >= 128
        rr = np.nonzero(im.sum(1) >= 3)[0]
        o['altezza_meta_contrasto'] = int(rr.max() - rr.min() + 1) if len(rr) else None
        o.update({'fotogrammi_misurati': [a, b], 'inizio': round(a / fps, 3), 'fine': round((b + 1) / fps, 3),
                  'scarto_fotogrammi': [a - o['srt_f0'], b - o['srt_f1']], 'box_lettere': box,
                  'iou_min': round(min(pres[f] for f in range(a, b + 1)), 2)})
    # 3. altezza delle lettere: righe con ascendenti e senza discendenti (es. «medicine»), dalla cima
    # delle ascendenti alla linea di base
    alt = [o['altezza_meta_contrasto'] for o in out if o.get('altezza_meta_contrasto')
           and not set(o['srt']) & set('gjpqy,;') and set(o['srt']) & set('bdfhklt')]
    fascia_info = {'vision_y': vy,
                   'lettere_x': [min(o['box_lettere'][0] for o in out if o.get('box_lettere')),
                                 max(o['box_lettere'][2] for o in out if o.get('box_lettere'))],
                   'lettere_y': [min(o['box_lettere'][1] for o in out if o.get('box_lettere')),
                                 max(o['box_lettere'][3] for o in out if o.get('box_lettere'))],
                   'altezza_lettere_px': int(statistics.median(alt)) if alt else None, 'righe_per_altezza': len(alt),
                   'altezza_come': "riga con ascendenti e senza discendenti, dalla cima (punto della i o ascendente) alla linea di base, "
                                   "pixel con min(R,G,B) >= 128; mediana delle righe"}
    return out, fascia_info


# ---------------------------------------------------------------- voce

def _tok_confronto(w):
    """parola per l'allineamento voce <-> SRT: i numeri in lettere diventano cifre, «€49» -> «49», «euro»"""
    w = C.norm(w)
    if not w:
        return []
    if '€' in w:
        return [p for p in w.split('€') if p] + ['euro']
    return [C.NUMERI.get(w, C.ORDINALI.get(w, w))]


def _contiene(seq, sotto):
    """indice in cui la lista sotto compare di fila dentro seq, o None"""
    for i in range(len(seq) - len(sotto) + 1):
        if seq[i:i + len(sotto)] == sotto:
            return i
    return None


def _inviluppo(wav):
    """energia in dB ogni 20 ms (finestre da 20 ms) del wav mono 16 kHz"""
    import wave
    with wave.open(str(wav)) as fh:
        x = np.frombuffer(fh.readframes(fh.getnframes()), np.int16).astype(np.float32) / 32768
    n = 320
    k = len(x) // n
    e = np.sqrt((x[:k * n].reshape(k, n) ** 2).mean(1) + 1e-10)
    return 20 * np.log10(e)


def _rifinisci(a, env):
    """inizio di una parola rifinito sull'inviluppo: nella finestra [a-0.30, a+0.20] si cerca il punto piu
    basso prima di a, poi il primo blocco da 20 ms che sale di 12 dB sopra quel minimo (o sopra -45 dBFS)"""
    i0, i1, ia = max(0, int((a - 0.30) / 0.02)), min(len(env) - 1, int((a + 0.20) / 0.02)), int(a / 0.02)
    if i1 - i0 < 4:
        return a
    seg = env[i0:max(i0 + 1, min(ia + 1, i1))]
    imin = i0 + int(np.argmin(seg))
    soglia = max(env[imin] + 12, -45)
    for i in range(imin, i1 + 1):
        if env[i] >= soglia:
            return round(i * 0.02, 2)
    return a


def misura_voce(video, srt, L):
    from . import trascrivi as T
    wav = L / 'voce.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-map', '0:a', '-ac', '1', '-ar', '16000',
                    '-c:a', 'pcm_s16le', str(wav)], check=True)
    P = [{'a': a, 'b': b, 'orig': t, 'fonte': 'passata intera'} for a, b, t in T.parole(str(wav))]
    # token
    def tok(lista):
        out = []
        for i, p in enumerate(lista):
            for k in _tok_confronto(p['orig']):
                out.append(dict(p, w=k, i=i))
        return out
    S = [{'n': r['n'], 'w': k, 'orig': w} for r in srt for w in r['t'].split() for k in _tok_confronto(w)]
    V = tok(P)
    sonde = []
    # dove voce e SRT non coincidono: sonde brevi da 2,6 s (come nella fase 0) che partono poco prima del punto.
    # La sonda conferma l'SRT se dentro di lei si sentono, di fila, le parole dell'SRT del punto con una parola
    # sicura per lato; allora quelle parole (con i tempi della sonda) prendono il posto di quelle della passata intera
    (L / 'sonde').mkdir(exist_ok=True)
    sm = difflib.SequenceMatcher(a=[s['w'] for s in S], b=[v['w'] for v in V], autojunk=False)
    cambi = [op for op in sm.get_opcodes() if op[0] != 'equal']
    nuove = list(V)
    for op, i1, i2, j1, j2 in reversed(cambi):
        ta = V[j1 - 1]['b'] if j1 > 0 else 0.0
        ctx = [s['w'] for s in S[max(0, i1 - 1):i2 + 1]]
        atteso = [s['w'] for s in S[i1:i2]]
        prove = []
        esito = None
        for a in (ta - 0.6, ta - 1.2, ta - 0.1):
            a = max(0.0, a)
            clip = L / 'sonde' / f'sonda-{a:.2f}.wav'
            T.clip(str(wav), a, 2.6, str(clip))
            pw = [{'a': x, 'b': y, 'orig': t, 'fonte': f'sonda {a:.2f}-{a + 2.6:.2f} s'} for x, y, t in T.parole(str(clip), offset=a)]
            pt = tok(pw)
            k = _contiene([p['w'] for p in pt], ctx)
            prove.append(f"{a:.2f}-{a + 2.6:.2f} s: «{' '.join(p['orig'] for p in pw)}»")
            if k is not None:
                d0 = k + (1 if i1 > 0 else 0)
                esito = pt[d0:d0 + len(atteso)]
                break
        sonde.append({'punto': round(ta, 2), 'op': op, 'srt': ' '.join(s['orig'] for s in S[i1:i2]),
                      'passata_intera': ' '.join(v['orig'] for v in V[j1:j2]), 'contesto_srt': ' '.join(ctx), 'sonde': prove,
                      'esito': 'la sonda conferma l SRT: corretto' if esito is not None else 'nessuna sonda conferma: segnalato'})
        if esito is not None:
            nuove[j1:j2] = esito
    V = nuove
    sm = difflib.SequenceMatcher(a=[s['w'] for s in S], b=[v['w'] for v in V], autojunk=False)
    diff, mapp = [], {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for k in range(i2 - i1):
                mapp[i1 + k] = j1 + k
        else:
            diff.append({'op': op, 'srt': ' '.join(s['orig'] for s in S[i1:i2]), 'righe': sorted({s['n'] for s in S[i1:i2]}),
                         'voce': ' '.join(v['orig'] for v in V[j1:j2]), 't': V[j1]['a'] if j1 < len(V) else None})
    env = _inviluppo(wav)
    parole = []
    for k, v in enumerate(V):
        if k and V[k - 1]['i'] == v['i'] and V[k - 1]['orig'] == v['orig'] and V[k - 1]['fonte'] == v['fonte']:
            continue                         # «€49» -> due token, una parola
        parole.append({'a': v['a'], 'b': v['b'], 'a_inviluppo': _rifinisci(v['a'], env), 'parola': v['orig'], 'fonte': v['fonte']})
    righe = []
    for r in srt:
        idx = [i for i, s in enumerate(S) if s['n'] == r['n']]
        m = [mapp[i] for i in idx if i in mapp]
        righe.append({'n': r['n'], 'voce_a': V[m[0]]['a'] if m else None, 'voce_b': V[m[-1]]['b'] if m else None,
                      'scarto_inizio': round(V[m[0]]['a'] - r['a'], 2) if m else None,
                      'scarto_fine': round(V[m[-1]]['b'] - r['b'], 2) if m else None})
    return {'parole': parole, 'sonde': sonde, 'differenze_srt': diff, 'righe': righe, 'modello': str(T.WHISPER_MODEL.name)}


# ---------------------------------------------------------------- colori

PUNTI = {'alto centro (540,60)': (540, 60), 'alto centro (540,250)': (540, 250), 'alto sx (60,150)': (60, 150),
         'alto dx (1020,150)': (1020, 150), 'lato sx (12,700)': (12, 700), 'lato dx (1068,700)': (1068, 700),
         'lato sx (12,1300)': (12, 1300), 'lato dx (1068,1300)': (1068, 1300), 'basso centro (540,1650)': (540, 1650),
         'basso centro (540,1880)': (540, 1880), 'basso sx (60,1850)': (60, 1850), 'basso dx (1020,1850)': (1020, 1850)}


def misura_colori(video, fps):
    camp = {k: [] for k in PUNTI}
    for a in C.fotogrammi_rgb(video, vf=f"select='not(mod(n\\,{round(fps)}))'"):
        for k, (x, y) in PUNTI.items():
            camp[k].append(a[y - 2:y + 3, x - 2:x + 3].reshape(-1, 3).mean(0))
    return {k: {'mediana_rgb': [int(round(c)) for c in np.median(np.array(v), 0)], 'n': len(v)} for k, v in camp.items()}


# ---------------------------------------------------------------- fogli per l'agente

def fogli(video, inq, fps, nf, out):
    from PIL import Image, ImageDraw, ImageFont
    fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 30)
    out.mkdir(parents=True, exist_ok=True)
    for p in list(out.glob('provini-*.jpg')) + list(out.glob('inquadrature*.jpg')) + list((out / 'inquadrature').glob('*.jpg')
                                                                                         if (out / 'inquadrature').exists() else []):
        p.unlink()
    # provini 5x4, un fotogramma ogni 0,5 s con il tempo sopra
    passo = round(fps / 2)
    tiles = []
    for k, a in enumerate(C.fotogrammi_rgb(video, vf=f"select='not(mod(n\\,{passo}))',scale=270:480:flags=lanczos", w=270, h=480)):
        im = Image.fromarray(a.copy())
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 110, 40], fill=(255, 230, 0)); d.text((6, 3), f'{k * passo / fps:5.1f}s', font=fnt, fill=(0, 0, 0))
        tiles.append(im)
    for s in range(0, len(tiles), 20):
        g = tiles[s:s + 20]
        sh = Image.new('RGB', (270 * 5 + 12, 480 * 4 + 9), 'white')
        for i, im in enumerate(g):
            sh.paste(im, ((i % 5) * 273, (i // 5) * 483))
        sh.save(out / f'provini-{s // 20 + 1:02d}_{s * passo / fps:04.1f}-{(s + len(g) - 1) * passo / fps:04.1f}s.jpg', quality=88)
    # un fotogramma per inquadratura (inizio, meta, fine) con le finestre disegnate: serve per segnare le 3D
    (out / 'inquadrature').mkdir(exist_ok=True)
    righe = []
    tutti = C.estrai(video, [f for s in inq for f in (s['f0'] + 2, (s['f0'] + s['f1']) // 2, s['f1'])])
    for s in inq:
        terne = []
        for f in (s['f0'] + 2, (s['f0'] + s['f1']) // 2, s['f1']):
            im = tutti[f].copy()
            if f == (s['f0'] + s['f1']) // 2:
                im.save(out / 'inquadrature' / f"inquadratura-{s['n']:02d}_{s['schema'] or 'X'}_f{f:04d}.jpg", quality=88)
            d = ImageDraw.Draw(im)
            for w in s['finestre']:
                d.rounded_rectangle([w['x'], w['y'], w['x1'], w['y1']], radius=w['raggio'], outline=(255, 0, 255), width=4)
            d.rectangle([0, 0, 1079, 70], fill=(255, 230, 0))
            d.text((16, 6), f"inq {s['n']}  schema {s['schema'] or '?'}  f{f}  {f / fps:.2f}s", font=ImageFont.truetype(
                '/System/Library/Fonts/Supplemental/Arial Bold.ttf', 52), fill='black')
            terne.append(im.resize((360, 640)))
        righe.append(terne)
    for g in range(0, len(righe), 4):
        blocco = righe[g:g + 4]
        sh = Image.new('RGB', (360 * 3 * len(blocco) + 30 * (len(blocco) - 1), 640), 'white')
        for i, terna in enumerate(blocco):
            for j, im in enumerate(terna):
                sh.paste(im, (i * (360 * 3 + 30) + j * 360, 0))
        sh.save(out / f"inquadrature-{inq[g]['n']:02d}-{inq[g + len(blocco) - 1]['n']:02d}.jpg", quality=86)


# ---------------------------------------------------------------- la fase

def radiografia(slug):
    S = C.sorgente(slug)
    L = C.lavoro(slug, 'radiografia')
    V = S['video']
    D = C.cartella(slug)
    pr = C.probe(V)
    if (pr['larghezza'], pr['altezza']) != (W, H):
        sys.exit(f"{slug}: il video è {pr['larghezza']}x{pr['altezza']}, l'agente reel-grafiche lavora solo su 1080x1920")
    fps, nf = pr['fps'], pr['fotogrammi']
    print(f"{slug}: {nf} fotogrammi a {fps} fps, {pr['durata']:.3f} s")
    tagli, info_tagli = misura_tagli(V)
    print(f"  tagli: {len(tagli)} {tagli}")
    confini = [0] + tagli + [nf]
    inq = misura_finestre(V, confini)
    for s in inq:
        print(f"  inq {s['n']:2d} f{s['f0']}-{s['f1']} schema {s['schema'] or '?'} {s['forza']}")
    srt = C.leggi_srt(S['srt']) if S.get('srt') else []
    fonte_copy, testo = 'SRT', None
    if not srt:
        # fase 6 (05/11/2026): reel senza SRT. Il copy viene dai sottotitoli impressi letti da Vision e confermati
        # dalla voce (whisper); senza sottotitoli, dalla sola voce. Si segnala: l'agente lo controlla sulle sonde
        srt, fonte_copy, testo = _senza_srt(V, nf, fps, L)
    sott, fascia = misura_sottotitoli(V, srt, fps, nf, L) if fonte_copy != 'voce' else ([], None)
    print(f"  sottotitoli: {sum(1 for o in sott if o['somiglianza'] >= 0.8)}/{len(sott)} righe lette uguali all'SRT; fascia {fascia}")
    voce = misura_voce(V, srt, L)
    print(f"  voce: {len(voce['parole'])} parole, {len(voce['sonde'])} sonde, {len(voce['differenze_srt'])} differenze con l'SRT")
    mp3 = None
    if S.get('mp3'):
        mp3 = {'file': C.rel(S['mp3']), 'nota': "riferimento per la voce (solo in locale): non si usa per i tempi, che vengono dall'audio del video"}
    colori = misura_colori(V, fps)
    # zone
    for s in inq:
        if s['schema'] in ('A', 'B'):
            g = s['finestre'][0]
            s['finestra_grande'] = {k: g[k] for k in ('x', 'y', 'w', 'h', 'x1', 'y1', 'raggio')}
            s['rett_grafica'] = rett_grafica(g)
            s['fessura_sottotitoli'] = [g['y1'] + 1, min(f['y'] for f in s['finestre'][1:]) - 1]
        else:
            s['finestra_grande'] = s['rett_grafica'] = None
            s['fessura_sottotitoli'] = None
    parole_srt = [w for r in srt for w in C.parole_di(r['t'])]
    vecchia = C.leggi(D / 'radiografia.json', {}) if (D / 'radiografia.json').exists() else {}
    R = {'_cosa': "Radiografia dell'ad (./mve reel-radiografia). Misure del motore; animazioni_3d le segna l'agente (./mve reel-3d).",
         'slug': slug, 'data': f"{datetime.datetime.now():%d/%m/%Y %H:%M}", 'sorgente': {k: C.rel(v) if v else None for k, v in S.items()},
         'md5_video': C.md5_file(V), 'md5_audio': C.md5_audio(V), 'ffprobe': pr, 'fps': fps, 'fotogrammi': nf,
         'tagli': tagli, 'tagli_info': info_tagli, 'inquadrature': inq,
         'sottotitoli': {'righe': sott, 'fascia': fascia}, 'srt': srt, 'voce': voce, 'mp3': mp3, 'colori': colori,
         'zone': {'zona_sicura_meta': {'x': [SAFE[0], SAFE[2]], 'y': [SAFE[1], SAFE[3]],
                                       'fonte': 'guida Meta Instagram Reels (14% sopra, 35% sotto, 6% ai lati), verificata il 03/11/2026'},
                  'mai_testo_da_y': SAFE[3] + 1},
         'parole_dette': sorted(set(parole_srt)), 'numeri_detti': sorted(C.numeri_detti(parole_srt) | C.numeri_detti(
             [C.norm(p['parola']) for p in voce['parole']]), key=lambda x: int(x)),
         'animazioni_3d': vecchia.get('animazioni_3d') or {'stato': 'da segnare',
                                                            'come': "l'agente guarda radiografia/inquadrature-*.jpg e i provini, poi ./mve reel-3d <slug> <inquadrature|nessuna>"}}
    R['fonte_copy'] = {'SRT': 'SRT di inbox/', 'letto': "sottotitoli impressi letti da Apple Vision e confermati dalla voce (manca l'SRT: "
                       "copy da confermare sulle sonde)", 'voce': "solo voce (whisper): niente SRT e niente sottotitoli impressi, copy da "
                       "confermare dall'agente"}[fonte_copy]
    fogli(V, inq, fps, nf, D / 'radiografia')
    from . import reel_radiografia as RR
    RR.estendi(R, V, L, D, testo=testo)
    C.scrivi(D / 'radiografia.json', R)
    scrivi_md(R, D / 'radiografia.md')
    print(f"  -> {C.rel(D / 'radiografia.json')}, {C.rel(D / 'radiografia.md')}, fogli in {C.rel(D / 'radiografia')}/")
    if R['animazioni_3d'].get('stato') == 'segnate':
        print(f"  animazioni 3D gia segnate dall'agente (inquadrature {R['animazioni_3d']['inquadrature'] or 'nessuna'}): "
              "ricontrollale sui fogli nuovi")
    else:
        print("  ADESSO L'AGENTE: guarda i fogli delle inquadrature e segna le animazioni 3D con ./mve reel-3d "
              f"{slug} <n,n|nessuna>")


def _senza_srt(V, nf, fps, L):
    """(srt, fonte, testo): senza SRT si leggono i sottotitoli impressi (Vision ogni 3 fotogrammi) e si tengono le righe
    che la voce dice nello stesso momento; senza sottotitoli, frasi della voce spezzate sulle pause"""
    from . import trascrivi as T, reel_radiografia as RR
    wav = L / 'voce.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(V), '-map', '0:a', '-ac', '1', '-ar', '16000',
                    '-c:a', 'pcm_s16le', str(wav)], check=True)
    pv = [{'a': a, 'b': b, 'parola': t} for a, b, t in T.parole(str(wav))]
    testo = RR.leggi_testo(V, nf, L)
    sott, _ = RR.separa_sottotitoli(RR.tracce(testo), pv, fps)
    if sott:
        print(f"  manca l'SRT: {len(sott)} righe di sottotitoli lette a schermo e confermate dalla voce")
        return RR.srt_letto(sott, fps), 'letto', testo
    righe, cur = [], []
    for p in pv:
        if cur and (p['a'] - cur[-1]['b'] > 0.6 or len(cur) >= 8):
            righe.append(cur); cur = []
        cur.append(p)
    if cur:
        righe.append(cur)
    print(f"  manca l'SRT e non ci sono sottotitoli impressi: copy dalla sola voce ({len(righe)} frasi)")
    return [{'n': i + 1, 'a': r[0]['a'], 'b': r[-1]['b'], 't': ' '.join(p['parola'] for p in r)} for i, r in enumerate(righe)], 'voce', testo


def segna_3d(slug, inquadrature, nota=None):
    """./mve reel-3d <slug> 3,9 [--nota "..."] | nessuna: le inquadrature con le animazioni 3D, segnate dall'agente"""
    D = C.cartella(slug)
    R = C.leggi(D / 'radiografia.json')
    ns = [] if inquadrature.strip().lower() == 'nessuna' else [int(x) for x in inquadrature.split(',') if x.strip()]
    per = {s['n']: s for s in R['inquadrature']}
    for n in ns:
        if n not in per:
            sys.exit(f"inquadratura {n} non esiste (1-{len(per)})")
    R['animazioni_3d'] = {'stato': 'segnate', 'inquadrature': ns,
                          'fotogrammi': [[per[n]['f0'], per[n]['f1']] for n in ns],
                          'nota': nota or '', 'segnate_da': "l'agente, guardando i fogli delle inquadrature e i provini",
                          'data': f"{datetime.datetime.now():%d/%m/%Y %H:%M}"}
    C.scrivi(D / 'radiografia.json', R)
    scrivi_md(R, D / 'radiografia.md')
    print(f"{slug}: animazioni 3D nelle inquadrature {ns or 'nessuna'} -> radiografia.json")


def segna_tipo(slug, inquadrature, tipo, nota=None):
    """./mve reel-tipo <slug> 21,22 "persona in camera" [--nota "..."]: l'agente corregge il tipo di inquadratura proposto
    dal motore (tappa 2, 06/11/2026: un banner grafico del montaggio in basso faceva riconoscere lo «schema A» delle
    finestre su un frontman in piedi). Toglie lo schema e la finestra grande (niente modo «finestra» lì); resta scritto chi
    l'ha cambiato, da cosa e perché"""
    TIPI = ('persona in camera', 'B-roll pieno')
    if tipo not in TIPI:
        sys.exit(f"tipo «{tipo}»: uno di {', '.join(TIPI)}")
    D = C.cartella(slug)
    R = C.leggi(D / 'radiografia.json')
    per = {s['n']: s for s in R['inquadrature']}
    ns = [int(x) for x in inquadrature.split(',') if x.strip()]
    for n in ns:
        if n not in per:
            sys.exit(f"inquadratura {n} non esiste (1-{len(per)})")
        s = per[n]
        s['tipo_corretto'] = {'da': s.get('tipo'), 'schema_era': s.get('schema'), 'nota': nota or '',
                              'segnato_da': "l'agente, guardando i fogli delle inquadrature", 'data': f"{datetime.datetime.now():%d/%m/%Y %H:%M}"}
        s['tipo'] = tipo
        s['schema'] = None
        s['rett_grafica'] = None
        s['finestra_grande'] = None
    from . import reel_radiografia as RR
    if R.get('tipo_reel'):
        R['tipo_reel'] = dict(R['tipo_reel'], **{k: v for k, v in RR.tipo_reel(R['inquadrature']).items() if k in ('proposto', 'quote')})
    C.scrivi(D / 'radiografia.json', R)
    scrivi_md(R, D / 'radiografia.md')
    print(f"{slug}: inquadrature {ns} -> «{tipo}» (radiografia.json)")


def segna_scena(slug, tieni, nota=None):
    """./mve reel-scena <slug> "<regex>" [--nota]: le scritte del video che NON corrispondono a <regex> sono «di scena»
    (insegne sul muro, magliette, certificati: fanno parte della ripresa, non del montaggio) e non bloccano più le grafiche;
    quelle che corrispondono restano scritte del montaggio da non coprire (tappa 2, 06/11/2026: l'insegna MOBILITAS dietro
    il frontman occupava tutto lo spazio accanto alla testa). Ricalcola lo strato «scritte» di zone.npz; la radiografia
    tiene l'elenco e chi l'ha deciso"""
    import re
    from . import reel_radiografia as RR
    D = C.cartella(slug)
    R = C.leggi(D / 'radiografia.json')
    rx = re.compile(tieni, re.I)
    tutte = R.get('scritte_video_tutte') or R['scritte_video']
    resta = [q for q in tutte if rx.search(q['t'])]
    scena = [q for q in tutte if not rx.search(q['t'])]
    p = C.AGENTE / R['zone_libere']['file']
    Z = RR.carica_zone(p)
    nf = Z['scritte'].shape[0]
    Z['scritte'][:] = False
    for q in resta:
        r0, r1, c0, c1 = RR._celle(q['box'], 12)
        Z['scritte'][max(0, q['f0']):min(nf, q['f1'] + 1), r0:r1 + 1, c0:c1 + 1] = True
    RR.salva_zone(Z, p)
    R['scritte_video_tutte'] = tutte
    R['scritte_video'] = resta
    R['scritte_di_scena'] = {'regola': f"restano del montaggio solo quelle che corrispondono a /{tieni}/ (senza maiuscole)", 'nota': nota or '',
                             'quante': len(scena), 'esempi': sorted({q['t'] for q in scena})[:30],
                             'segnate_da': "l'agente, guardando i fogli", 'data': f"{datetime.datetime.now():%d/%m/%Y %H:%M}"}
    C.scrivi(D / 'radiografia.json', R)
    scrivi_md(R, D / 'radiografia.md')
    print(f"{slug}: {len(resta)} scritte del montaggio restano ({', '.join(sorted({q['t'] for q in resta}))}); {len(scena)} di scena")


def scrivi_md(R, out):
    fps = R['fps']
    L = [f"# Radiografia: {R['slug']}", '',
         f"Generata da `./mve reel-radiografia` il {R['data']}. Misure del motore, ricontrollate dall'agente sui fogli in `radiografia/`.", '',
         '## In breve', '',
         f"- {R['ffprobe']['larghezza']}×{R['ffprobe']['altezza']}, {fps} fps, {R['fotogrammi']} fotogrammi, {R['ffprobe']['durata']:.3f} s; "
         f"audio {R['ffprobe']['audio']['codec_name'] if R['ffprobe']['audio'] else 'nessuno'}, md5 del flusso `{R['md5_audio']}`.",
         f"- **{len(R['tagli'])} tagli** (differenza media fra fotogrammi: mediana {R['tagli_info']['mediana']}, picchi "
         f"{min(R['tagli_info']['picchi'] or [0])}–{max(R['tagli_info']['picchi'] or [0])}, fuori dai tagli al massimo {R['tagli_info']['max_fuori_tagli']}). "
         + (f"Possibili dissolvenze da guardare: {R['tagli_info']['dubbi_dissolvenza']}." if R['tagli_info']['dubbi_dissolvenza'] else 'Nessuna dissolvenza.')]
    sc = [s for s in R['inquadrature'] if not s['schema']]
    L.append(f"- **{len(R['inquadrature'])} inquadrature**, schemi " + ', '.join(f"{s['n']}:{s['schema'] or '?'}" for s in R['inquadrature'])
             + (f". **Schema non riconosciuto** nelle inquadrature {[s['n'] for s in sc]}: guardarle." if sc else '.'))
    a3 = R['animazioni_3d']
    L.append(f"- **Animazioni 3D:** " + (f"inquadrature {a3['inquadrature'] or 'nessuna'} (segnate dall'agente). {a3.get('nota', '')}"
                                          if a3.get('stato') == 'segnate' else '**DA SEGNARE** (`./mve reel-3d`)'))
    so = R['sottotitoli']['righe']; fa = R['sottotitoli']['fascia'] or {}
    uguali = [o for o in so if o['somiglianza'] >= 0.8]
    scarti = [o for o in uguali if o.get('scarto_fotogrammi') and o['scarto_fotogrammi'] != [0, 0]]
    L.append(f"- **Sottotitoli:** {len(so)} righe nell'SRT, {len(uguali)} lette a schermo uguali (Vision, somiglianza ≥ 0,8); "
             f"fascia delle lettere x {fa.get('lettere_x')}, y {fa.get('lettere_y')}; altezza lettere {fa.get('altezza_lettere_px')} px "
             f"(minimo per i testi delle grafiche: {round(1.5 * fa['altezza_lettere_px']) if fa.get('altezza_lettere_px') else '?'} px). "
             f"Tempi a schermo diversi dall'SRT: {len(scarti)} righe.")
    v = R['voce']
    L.append(f"- **Voce** ({v['modello']}): {len(v['parole'])} parole; {len(v['sonde'])} sonde brevi; differenze di testo voce ↔ SRT dopo le sonde: "
             f"{len(v['differenze_srt'])}.")
    sc_i = [r['scarto_inizio'] for r in v['righe'] if r['scarto_inizio'] is not None]
    if sc_i:
        L.append(f"- Voce ↔ SRT, tempi: inizio della voce meno inizio del sottotitolo, mediana {statistics.median(sc_i):+.2f} s "
                 f"(da {min(sc_i):+.2f} a {max(sc_i):+.2f}). Le grafiche si agganciano alla voce, non ai sottotitoli.")
    L.append(f"- **Parole dette** (dall'SRT): {len(R['parole_dette'])} diverse; numeri detti: {', '.join(R['numeri_detti']) or 'nessuno'}.")
    L += ['', '## Inquadrature', '', '| # | fotogrammi | tempo (s) | schema | finestra grande (x, y, l×a, r) | rettangolo per «finestra» | fessura sottotitoli | 3D |',
          '|---|---|---|---|---|---|---|---|']
    tre = set(a3.get('inquadrature', [])) if a3.get('stato') == 'segnate' else None
    for s in R['inquadrature']:
        g = s.get('finestra_grande'); r = s.get('rett_grafica')
        L.append(f"| {s['n']} | {s['f0']}–{s['f1']} | {s['f0'] / fps:.3f}–{(s['f1'] + 1) / fps:.3f} | {s['schema'] or '? (' + s['schema_probabile'] + ')'} | "
                 + (f"{g['x']}, {g['y']}, {g['w']}×{g['h']}, r {g['raggio']}" if g else '—') + ' | '
                 + (f"{r['x']}, {r['y']}, {r['w']}×{r['h']}, r {r['r']}" if r else '—') + ' | '
                 + (f"y {s['fessura_sottotitoli'][0]}–{s['fessura_sottotitoli'][1]}" if s.get('fessura_sottotitoli') else '—') + ' | '
                 + ('?' if tre is None else ('**sì**' if s['n'] in tre else 'no')) + ' |')
    L += ['', '## Sottotitoli e voce, riga per riga', '',
          '| riga | SRT (s) | a schermo (fotogrammi) | scarto | testo SRT | letto (Vision) | voce (s) |', '|---|---|---|---|---|---|---|']
    vr = {r['n']: r for r in v['righe']}
    for o in so:
        r = vr.get(o['n'], {})
        L.append(f"| {o['n']} | {o['srt_a']:.3f}–{o['srt_b']:.3f} | " + (f"{o['fotogrammi_misurati'][0]}–{o['fotogrammi_misurati'][1]}" if o.get('fotogrammi_misurati') else '—')
                 + f" | {o.get('scarto_fotogrammi', '—')} | {o['srt']} | " + ('=' if o['somiglianza'] >= 0.999 else f"{o['letto']} ({o['somiglianza']})")
                 + f" | " + (f"{r['voce_a']:.2f}–{r['voce_b']:.2f}" if r.get('voce_a') is not None else '—') + ' |')
    if v['sonde']:
        L += ['', '## Sonde brevi (dove la passata intera e l\'SRT non coincidevano)', '']
        for s in v['sonde']:
            L.append(f"- a {s['punto']:.2f} s: SRT «{s['srt']}», passata intera «{s['passata_intera']}» (contesto «{s['contesto_srt']}»): "
                     f"{s['esito']}. Sonde: " + '; '.join(s['sonde']) + '.')
    if v['differenze_srt']:
        L += ['', '## Differenze voce ↔ SRT rimaste (si segnalano, non si correggono)', '']
        for d in v['differenze_srt']:
            L.append(f"- righe {d['righe']}: SRT «{d['srt']}», voce «{d['voce']}» ({d['t']})")
    L += ['', '## Colori del fondo (mediana nel tempo, BT.709 range tv → RGB)', '']
    L += [f"- {k}: {v_['mediana_rgb']}" for k, v_ in R['colori'].items()]
    L += ['', '## Fogli', '', '- `radiografia/inquadrature-*.jpg`: inizio, metà e fine di ogni inquadratura con le finestre misurate in magenta: '
          '**qui si segnano le 3D**;', '- `radiografia/inquadrature/`: il fotogramma a metà di ogni inquadratura a piena risoluzione;',
          '- `radiografia/provini-*.jpg`: un fotogramma ogni 0,5 s.', '']
    from . import reel_radiografia as RR
    L += RR.md(R)
    out.write_text('\n'.join(L) + '\n', encoding='utf-8')

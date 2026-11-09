"""Zoom e spinte di camera leggeri sul video base (agente reel-grafiche, fase 6, 05/11/2026).

Regola di Riccardo (05/11/2026): pochi, morbidi, ingrandimento massimo intorno all'8-10%; mai se tagliano i
sottotitoli, le scritte del video o la testa della persona; colori sempre intatti.

Nel piano (`piano.json`, chiave `zoom`), uno per voce:

    {"nome": "z1", "f0": 120, "f1": 209, "scala": 1.07, "centro": [540, 650], "zona": "tutto" | "finestra",
     "rett": {...} (solo «finestra»: il rett_grafica dell'inquadratura), "curva": "spinta" | "respiro",
     "momento": "...", "perche": "..."}

- «spinta»: da 1 a `scala`, morbida (seno), e finisce sul taglio (f1 = ultimo fotogramma dell'inquadratura);
- «respiro»: sale a `scala` nel primo 45%, resta, torna a 1 nell'ultimo 30% (può finire prima del taglio);
- «tutto»: tutto il fotogramma; «finestra»: solo il contenuto della finestra (B-roll), dentro il suo rettangolo
  arrotondato, ristretto di 3 px; bordo, fondo, sottotitoli e altre finestre non cambiano.

Come: i fotogrammi si decodificano in YUV 4:2:0 e ogni piano (Y, U, V) si ricampiona con la stessa geometria
(bicubica, sotto il pixel): niente conversione di colore, i colori non cambiano. I fotogrammi senza zoom passano
identici. Esce un video intermedio senza perdite (x264 qp 0) in `.lavoro/<slug>/rendi/`, che prende il posto del
video base nella sovrapposizione: la codifica con perdita resta una sola.
"""
import math
import subprocess

import numpy as np

from . import reel_comune as C
from .reel_comune import W, H

SCALA_MAX = 1.10
VELOCITA_MAX = 0.05          # ingrandimento al secondo (8% in non meno di 1,6 s)
DURATA_MIN = 1.5
INSET = 3


def scala_al(z, f):
    """ingrandimento al fotogramma f (1 fuori dallo zoom)"""
    if f < z['f0'] or f > z['f1']:
        return 1.0
    u = (f - z['f0']) / max(1, z['f1'] - z['f0'])
    S = z['scala']
    if z.get('curva', 'spinta') == 'respiro':
        if u < 0.45:
            e = 0.5 - 0.5 * math.cos(math.pi * u / 0.45)
        elif u <= 0.70:
            e = 1.0
        else:
            e = 0.5 + 0.5 * math.cos(math.pi * (u - 0.70) / 0.30)
        return 1 + (S - 1) * e
    return 1 + (S - 1) * (0.5 - 0.5 * math.cos(math.pi * u))


def trasforma_box(z, f, box):
    """dove va un riquadro (x0, y0, x1, y1) del video base al fotogramma f"""
    s = scala_al(z, f)
    cx, cy = z['centro']
    return [cx + (box[0] - cx) * s, cy + (box[1] - cy) * s, cx + (box[2] - cx) * s, cy + (box[3] - cy) * s]


def indietro_box(z, f, box):
    """da dove viene (nel video base) un riquadro del fotogramma zoomato"""
    s = scala_al(z, f)
    cx, cy = z['centro']
    return [cx + (box[0] - cx) / s, cy + (box[1] - cy) / s, cx + (box[2] - cx) / s, cy + (box[3] - cy) / s]


def area(z):
    """il rettangolo che lo zoom cambia (x0, y0, x1, y1)"""
    if z.get('zona') == 'finestra':
        r = z['rett']
        return [r['x'] + INSET, r['y'] + INSET, r['x'] + r['w'] - 1 - INSET, r['y'] + r['h'] - 1 - INSET]
    return [0, 0, W - 1, H - 1]


def _maschera(z):
    """maschera morbida (0-1) del rettangolo arrotondato della finestra, a piena e mezza risoluzione"""
    from PIL import Image, ImageDraw
    if z.get('zona') != 'finestra':
        return None, None
    r = z['rett']
    big = Image.new('L', (W * 2, H * 2), 0)
    ImageDraw.Draw(big).rounded_rectangle([(r['x'] + INSET) * 2, (r['y'] + INSET) * 2, (r['x'] + r['w'] - INSET) * 2 - 1,
                                           (r['y'] + r['h'] - INSET) * 2 - 1], radius=max(1, (r.get('r', 60) - INSET) * 2), fill=255)
    m1 = np.asarray(big.resize((W, H), Image.BOX), np.float32) / 255
    m2 = np.asarray(big.resize((W // 2, H // 2), Image.BOX), np.float32) / 255
    return m1, m2


def _ricampiona(piano, s, cx, cy, mezza):
    from PIL import Image
    h, w = piano.shape
    if mezza:          # croma 4:2:0, campioni a sinistra in x e in mezzo in y (MPEG-2): centro nelle coordinate del piano
        cx, cy = cx / 2, (cy - 0.5) / 2
    a = 1 / s
    im = Image.fromarray(piano)
    out = im.transform((w, h), Image.AFFINE, (a, 0, cx * (1 - a), 0, a, cy * (1 - a)), resample=Image.BICUBIC)
    return np.asarray(out)


def applica(V, zoom, out, fps, nf):
    """il video base con gli zoom (senza perdite) -> out; ritorna {f: scala} dei fotogrammi cambiati"""
    per_f = {}
    for z in zoom:
        for f in range(z['f0'], z['f1'] + 1):
            s = scala_al(z, f)
            if abs(s - 1) > 1e-6:
                per_f[f] = (z, s)
    masks = {z['nome']: _maschera(z) for z in zoom}
    dec = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(V), '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-'], stdout=subprocess.PIPE)
    # le etichette di colore vanno anche sull'ingresso: se mancano, ffmpeg converte il range e i fotogrammi cambiano (prova del
    # 05/11/2026: fino a 12 livelli anche dove lo zoom non c'è)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', f'{W}x{H}', '-r', str(fps),
                            '-color_range', 'tv', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                            '-i', '-', '-c:v', 'libx264', '-qp', '0', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
                            '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', str(out)],
                           stdin=subprocess.PIPE)
    ny, nc = W * H, (W // 2) * (H // 2)
    f = 0
    while True:
        b = dec.stdout.read(ny + 2 * nc)
        if len(b) < ny + 2 * nc:
            break
        if f in per_f:
            z, s = per_f[f]
            cx, cy = z['centro']
            a = np.frombuffer(b, np.uint8)
            Y = a[:ny].reshape(H, W); U = a[ny:ny + nc].reshape(H // 2, W // 2); Vp = a[ny + nc:].reshape(H // 2, W // 2)
            Yz, Uz, Vz = _ricampiona(Y, s, cx, cy, False), _ricampiona(U, s, cx, cy, True), _ricampiona(Vp, s, cx, cy, True)
            m1, m2 = masks[z['nome']]
            if m1 is not None:
                Yz = np.round(Yz * m1 + Y * (1 - m1)).astype(np.uint8)
                Uz = np.round(Uz * m2 + U * (1 - m2)).astype(np.uint8)
                Vz = np.round(Vz * m2 + Vp * (1 - m2)).astype(np.uint8)
            b = Yz.tobytes() + Uz.tobytes() + Vz.tobytes()
        enc.stdin.write(b)
        f += 1
    enc.stdin.close()
    dec.wait(); enc.wait()
    if enc.returncode or f != nf:
        raise SystemExit(f"zoom: {f} fotogrammi letti su {nf}, codifica {enc.returncode}")
    return {f: s for f, (z, s) in per_f.items()}


def verifica(V, Vz, zoom, cambiati, nf):
    """1) i fotogrammi senza zoom sono identici bit per bit (md5 del fotogramma decodificato); 2) colori: nei fotogrammi con
    zoom, la media di Y, U e V della zona ingrandita è quella della zona del base da cui viene (stesso contenuto): la
    differenza (livelli) misura se i colori sono cambiati"""
    def md5s(v):
        # solo il video: con l'audio, framemd5 mette anche i pacchetti audio e gli indici scivolano (render del 05/11/2026)
        r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(v), '-map', '0:v:0', '-pix_fmt', 'yuv420p', '-f', 'framemd5', '-'],
                           capture_output=True, text=True)
        return [l.split(',')[-1].strip() for l in r.stdout.splitlines() if l and not l.startswith('#')]
    a, b = md5s(V), md5s(Vz)
    diversi = [f for f in range(min(len(a), len(b))) if a[f] != b[f]]
    fuori = sorted(set(diversi) - set(cambiati))
    ny, nc = W * H, (W // 2) * (H // 2)
    d1 = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(V), '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-'], stdout=subprocess.PIPE)
    d2 = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(Vz), '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-'], stdout=subprocess.PIPE)
    dmax = [0.0, 0.0, 0.0]
    f = 0
    while True:
        x, y = d1.stdout.read(ny + 2 * nc), d2.stdout.read(ny + 2 * nc)
        if len(x) < ny + 2 * nc or len(y) < ny + 2 * nc:
            break
        if f in cambiati:
            z = next(z for z in zoom if z['f0'] <= f <= z['f1'])
            A = area(z)
            rr = (z['rett'].get('r', 60) if z.get('zona') == 'finestra' else 0) + 8
            dentro = [A[0] + rr, A[1] + rr, A[2] - rr, A[3] - rr]       # senza gli angoli arrotondati
            da = indietro_box(z, f, dentro)
            p, q = np.frombuffer(x, np.uint8), np.frombuffer(y, np.uint8)
            piani = [(p[:ny].reshape(H, W), q[:ny].reshape(H, W), 1), (p[ny:ny + nc].reshape(H // 2, W // 2), q[ny:ny + nc].reshape(H // 2, W // 2), 2),
                     (p[ny + nc:].reshape(H // 2, W // 2), q[ny + nc:].reshape(H // 2, W // 2), 2)]
            for k, (pb, pz, sc) in enumerate(piani):
                o = pz[int(dentro[1] / sc):int(dentro[3] / sc), int(dentro[0] / sc):int(dentro[2] / sc)].astype(float)
                s_ = pb[int(round(da[1] / sc)):int(round(da[3] / sc)), int(round(da[0] / sc)):int(round(da[2] / sc))].astype(float)
                dmax[k] = max(dmax[k], abs(o.mean() - s_.mean()))
        f += 1
    d1.wait(); d2.wait()
    return {'fotogrammi': len(b), 'identici_fuori_dallo_zoom': not fuori, 'diversi_fuori_dallo_zoom': fuori[:20],
            'fotogrammi_con_zoom': len(cambiati),
            'differenza_media_max_livelli': {'Y': round(dmax[0], 3), 'U': round(dmax[1], 3), 'V': round(dmax[2], 3)},
            'come': "media di Y, U, V della zona ingrandita contro la zona del video base da cui viene (stesso contenuto)"}


def controlla(P, R, occupato_da_grafica):
    """errori e avvisi degli zoom del piano. occupato_da_grafica: {f: (nome, modo)} dalle grafiche del piano"""
    from . import reel_radiografia as RR
    err, avv = [], []
    zoom = P.get('zoom') or []
    if not zoom:
        return err, avv
    fps, nf = R['fps'], R['fotogrammi']
    inq_di = {f: s for s in R['inquadrature'] for f in range(s['f0'], s['f1'] + 1)}
    pers = C.leggi(C.AGENTE / R['persona']['file']) if R.get('persona') else None
    tre = {f for a, b in (R.get('animazioni_3d') or {}).get('fotogrammi', []) for f in range(a, b + 1)}
    for z in zoom:
        n = z.get('nome', '?')
        if not all(k in z for k in ('f0', 'f1', 'scala', 'centro')):
            err.append(f"zoom {n}: servono f0, f1, scala, centro"); continue
        if z['scala'] > SCALA_MAX + 1e-9 or z['scala'] < 1:
            err.append(f"zoom {n}: scala {z['scala']} (fra 1 e {SCALA_MAX})")
        dur = (z['f1'] - z['f0'] + 1) / fps
        if dur < DURATA_MIN:
            err.append(f"zoom {n}: dura {dur:.2f} s (almeno {DURATA_MIN}: morbido, non a scatto)")
        # 07/11/2026 (Riccardo): i sottotitoli impressi non si ingrandiscono: uno zoom su tutto il quadro mentre c'è una riga
        # di sottotitolo li toccherebbe (vale solo la zona «finestra», che non arriva alla fascia)
        if z.get('zona') != 'finestra':
            for o in R['sottotitoli'].get('righe') or []:
                fm = o.get('fotogrammi_misurati')
                if fm and fm[1] >= z['f0'] and fm[0] <= z['f1']:
                    err.append(f"zoom {n}: su tutto il quadro mentre c'è il sottotitolo «{o.get('srt', '')[:30]}»: i sottotitoli non si "
                               "ingrandiscono (solo zoom «finestra», o niente zoom)")
                    break
        sal = (z['scala'] - 1) / (dur * (0.45 if z.get('curva') == 'respiro' else 1))
        if sal > VELOCITA_MAX + 1e-9:
            err.append(f"zoom {n}: sale del {sal * 100:.1f}% al secondo (massimo {VELOCITA_MAX * 100:.0f}%: «non troppo hard»)")
        s0, s1 = inq_di.get(z['f0']), inq_di.get(z['f1'])
        if not s0 or s0 is not s1:
            err.append(f"zoom {n}: attraversa un taglio (fotogrammi {z['f0']}-{z['f1']})"); continue
        if z.get('curva', 'spinta') == 'spinta' and z['f1'] != s0['f1']:
            err.append(f"zoom {n}: una «spinta» finisce sul taglio (f1 {s0['f1']}), altrimenti torna di colpo a 1: usa «respiro»")
        if z.get('zona') == 'finestra':
            from .reel_radiografia_base import rett_grafica
            qq = [rett_grafica(w) for w in s0.get('finestre', [])] if s0.get('schema') else []
            if not z.get('rett') or not any(max(abs(z['rett'][k] - q[k]) for k in ('x', 'y', 'w', 'h')) <= 2 for q in qq):
                err.append(f"zoom {n}: «finestra» vuole il rettangolo di una finestra misurata dell'inquadratura {s0['n']} ({qq})")
                continue
        A = area(z)
        if not (A[0] <= z['centro'][0] <= A[2] and A[1] <= z['centro'][1] <= A[3]):
            err.append(f"zoom {n}: il centro {z['centro']} non è nella zona dello zoom {A}")
        # grafiche
        for f in range(z['f0'], z['f1'] + 1):
            g = occupato_da_grafica.get(f)
            if not g:
                continue
            nome, modo = g
            if modo in ('tutto schermo', 'finestra', 'persona'):
                err.append(f"zoom {n}: al fotogramma {f} c'è la grafica «{nome}» ({modo}): lo zoom non va sotto una grafica a finestra, "
                           "a tutto schermo o sulla persona")
                break
        if z.get('zona') != 'finestra' and set(range(z['f0'], z['f1'] + 1)) & tre:
            avv.append(f"zoom {n}: su un'inquadratura con le 3D: restano visibili? (controllato sotto: le finestre restano nel quadro)")
        # cosa non si deve tagliare
        def dentro(b):
            return b[0] >= A[0] - 0.5 and b[1] >= A[1] - 0.5 and b[2] <= A[2] + 0.5 and b[3] <= A[3] + 0.5
        tagli = []
        for f in range(z['f0'], z['f1'] + 1):
            cose = []
            for o in R['sottotitoli'].get('righe') or []:
                fm, bx = o.get('fotogrammi_misurati'), o.get('box_lettere')
                if fm and bx and fm[0] <= f <= fm[1]:
                    cose.append(('sottotitolo «' + o['srt'][:30] + '»', bx))
            for q in R.get('scritte_video') or []:
                if q['f0'] <= f <= q['f1']:
                    cose.append(('scritta «' + q['t'][:30] + '»', q['box']))
            if pers:
                cose += [('testa', t) for t in pers[f]['teste']]
            if z.get('zona') != 'finestra':
                cose += [('finestra', [w['x'], w['y'], w['x1'], w['y1']]) for w in s0.get('finestre', [])] if s0.get('schema') else []
            for nome, b in cose:
                if z.get('zona') == 'finestra' and not dentro(b):
                    # nella finestra contano solo le cose che stanno nella finestra
                    cxb, cyb = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
                    if not (A[0] <= cxb <= A[2] and A[1] <= cyb <= A[3]):
                        continue
                bt = trasforma_box(z, f, b)
                vis = [max(b[0], A[0]), max(b[1], A[1]), min(b[2], A[2]), min(b[3], A[3])]
                # tagliato = ora esce dalla zona, mentre prima ci stava (o ne esce di più)
                fuori_prima = max(0, A[0] - b[0]) + max(0, A[1] - b[1]) + max(0, b[2] - A[2]) + max(0, b[3] - A[3])
                fuori_dopo = max(0, A[0] - bt[0]) + max(0, A[1] - bt[1]) + max(0, bt[2] - A[2]) + max(0, bt[3] - A[3])
                if fuori_dopo > fuori_prima + 0.5:
                    tagli.append((f, nome, [round(v) for v in bt]))
        if tagli:
            f, nome, bt = tagli[0]
            err.append(f"zoom {n}: taglia {nome} al fotogramma {f} (diventa {bt}) e in altri {len(tagli) - 1} casi: cambia centro o scala")
    # pochi
    if len(zoom) > max(1, round(nf / fps / 8)):
        avv.append(f"{len(zoom)} zoom in {nf / fps:.0f} s: la regola dice «pochi» (circa uno ogni 8-10 s al massimo)")
    for a, b in zip(sorted(zoom, key=lambda z: z.get('f0', 0)), sorted(zoom, key=lambda z: z.get('f0', 0))[1:]):
        if b['f0'] <= a['f1']:
            err.append(f"zoom {a.get('nome')} e {b.get('nome')} si sovrappongono")
    return err, avv

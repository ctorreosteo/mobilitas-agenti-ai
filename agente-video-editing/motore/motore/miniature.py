"""Fase `miniature`: tre miniature YouTube 1280x720 dai fotogrammi migliori.

Lo scatto si sceglie misurando, non a occhio: fra tutti i campioni di
`volti.json` che cadono nel montato si tengono quelli con la qualita del volto
piu alta per Vision, occhi aperti e viso frontale, distanti almeno 20 s l'uno
dall'altro (espressioni diverse). Il testo viene da `regia.json -> miniatura`.

Composizione: soggetto a destra (taglio medio dal 4K), pannello navy a sinistra
che sfuma verso il soggetto, testo enorme in Montserrat 900. La miniatura si
legge a 160 px di larghezza: due righe, al massimo tre parole per riga.
"""
import numpy as np
from PIL import Image, ImageDraw

from . import stile as S
from . import colore
from .progetto import Progetto, ffmpeg, ts
from .grafica.render import sans, mono, tracked_width, draw_tracked

TW, TH = 1280, 720


def candidati(P, n=3, distanza=20.0):
    d = P.leggi('volti.json')
    E = P.leggi('edl.json')
    keep = [(s['in'], s['in'] + s['n'] / 29.97) for s in E['segmenti']]
    rows = []
    for c in d['campioni']:
        vv = [v for v in c['volti'] if v['conf'] > 0.8]
        if len(vv) != 1 or not any(a + 0.5 < c['t'] < b - 0.5 for a, b in keep):
            continue
        v = vv[0]
        occhi = min(v.get('occhio_sx', 0), v.get('occhio_dx', 0))
        if occhi < 0.30 or abs(v.get('yaw', 0)) > 0.2:
            continue
        rows.append((v.get('q', 0) + 0.15 * min(v.get('bocca', 0), 0.6), c['t'], v))
    rows.sort(reverse=True)
    scelti = []
    for sc, t, v in rows:
        if all(abs(t - x[1]) > distanza for x in scelti):
            scelti.append((sc, t, v))
        if len(scelti) == n:
            break
    return scelti


def miniature(slug):
    P = Progetto(slug)
    R = P.regia()
    m = P.meta()
    cfg = R.get('miniatura', {})
    righe = cfg.get('righe') or [R.get('titolo_lavoro', '').upper()]
    out = P.p('miniature')
    out.mkdir(exist_ok=True)
    scelti = candidati(P)
    if not scelti:
        raise SystemExit("nessun fotogramma con volto frontale e occhi aperti nel montato")
    files = []
    for k, (sc, t, v) in enumerate(scelti):
        W, H = m['larghezza'], m['altezza']
        z = 1.45
        cw, ch = int(W / z) // 2 * 2, int(H / z) // 2 * 2
        fx, fy = (v['x'] + v['w'] / 2) * W, (v['y'] + v['h'] / 2) * H
        # volto al 70% della larghezza e al 36% dell'altezza: il testo a sinistra non deve toccare i capelli
        x0 = int(min(max(0, fx - 0.70 * cw), W - cw)) // 2 * 2
        y0 = int(min(max(0, fy - 0.36 * ch), H - ch)) // 2 * 2
        vf = f"crop={cw}:{ch}:{x0}:{y0},scale={TW}:{TH}:flags=lanczos"
        c = colore.catena(m)
        vf += (',' + c if c else '') + ',format=rgb24'
        raw = out / f"_f{k}.png"
        ffmpeg('-ss', f"{t:.3f}", '-i', P.sorgente, '-frames:v', '1', '-vf', vf, raw)
        img = Image.open(raw).convert('RGBA')
        raw.unlink()
        files.append(_componi(img, righe, cfg.get('eyebrow'), out / f"miniatura-{k + 1}.jpg"))
        print(f"  miniatura {k + 1}: fotogramma sorgente {ts(t)} (qualita volto {v.get('q', 0):.2f})")
    strip = Image.new('RGB', (TW * len(files) // 2 + 8 * (len(files) + 1), TH // 2 + 16), (20, 20, 20))
    for k, f in enumerate(files):
        strip.paste(Image.open(f).resize((TW // 2, TH // 2)), (8 + k * (TW // 2 + 8), 8))
    strip.save(P.controllo('miniature.jpg'), quality=90)
    # la prova del pollice: come si vede nella griglia di YouTube
    small = Image.open(files[0]).resize((168, 94), Image.LANCZOS)
    small.save(P.controllo('miniatura-piccola.png'))
    print(f"-> miniature/ ({len(files)}), foglio in controlli/miniature.jpg, "
          f"prova a 168 px in controlli/miniatura-piccola.png")


def _componi(img, righe, eyebrow, path):
    W, H = img.size
    # pannello navy a sinistra che sfuma verso il soggetto (lo sfondo sfuma, il testo no)
    a = np.zeros((H, W), dtype=np.float32)
    x = np.arange(W)
    ramp = np.clip((0.62 - x / W) / 0.22, 0, 1) ** 1.2
    a[:] = 0.93 * ramp
    panel = np.zeros((H, W, 4), dtype=np.uint8)
    panel[..., :3] = S.NAVY_DEEP
    panel[..., 3] = (a * 255).astype(np.uint8)
    img.alpha_composite(Image.fromarray(panel, 'RGBA'))
    d = ImageDraw.Draw(img)
    maxw = int(W * 0.46)
    size = 150
    while size > 70:
        f = sans(size, 900)
        tr = -0.04 * size
        if max(tracked_width(f, r, tr) for r in righe) <= maxw:
            break
        size -= 6
    lh = int(size * 1.0)
    total = len(righe) * lh + (60 if eyebrow else 0)
    y = (H - total) // 2
    if eyebrow:
        fe = mono(30)
        draw_tracked(d, (60, y), eyebrow, fe, S.MINT + (255,), 0.2 * 30)
        y += 46
        d.rounded_rectangle([60, y, 150, y + 7], radius=3, fill=S.MINT + (255,))
        y += 24
    for i, r in enumerate(righe):
        col = S.PAPER if i < len(righe) - 1 else S.MINT
        draw_tracked(d, (56, y - int(size * 0.1)), r, f, col + (255,), tr)
        y += lh
    img.convert('RGB').save(path, quality=93)
    return path

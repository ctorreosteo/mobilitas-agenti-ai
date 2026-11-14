"""Prova veloce di UNA grafica del piano (07/11/2026): rende solo quella grafica e la mette sopra il video base in alcuni
istanti, in un foglio a misura di telefono (390 px per fotogramma). Un minuto invece dei quindici del render intero.

    ./mve reel-prova <slug> <grafica> <secondi...>     es. ./mve reel-prova AD_X benefici 1.2 4.5 6.0

Esce in `.lavoro/<slug>/prova/prova-<grafica>.jpg` (e il primo istante a piena grandezza, `prova-<grafica>-grande.png`).
Non è un controllo: i controlli veri li fa `reel-rendi`. Gli istanti fuori dalla grafica si saltano."""
import subprocess

import numpy as np

from . import reel_comune as C
from . import reel_rendi as AR

W, H = C.W, C.H          # il formato del reel (11/11/2026)


def _base(V, f):
    """il fotogramma f del video base in RGB pieno (BT.709, range tv -> pc, come il render)"""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(V), '-vf', f'select=eq(n\\,{f})', '-frames:v', '1', '-f', 'rawvideo',
                          '-pix_fmt', 'yuv420p', '-'], capture_output=True).stdout
    rgb = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'yuv420p', '-s', f'{W}x{H}', '-color_range', 'tv',
                          '-colorspace', 'bt709', '-i', '-', '-vf', 'scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], input=raw, capture_output=True).stdout
    return rgb


def prova(slug, grafica, tempi):
    from PIL import Image, ImageDraw, ImageFont
    from .stile import FONT_SANS
    D = C.cartella(slug)
    P = C.leggi(D / 'piano.json')
    P['slug'] = slug
    gg = [x for x in P['grafiche'] if x['nome'] == grafica]
    if not gg:
        raise SystemExit(f"{slug}: nel piano non c'è la grafica «{grafica}» (ci sono: {', '.join(x['nome'] for x in P['grafiche'])})")
    g = gg[0]
    R = C.leggi(D / 'radiografia.json')
    from . import reel_palco as RPal
    RPal.risolvi(P, R)           # 13/11/2026: "copre": "finestra" (il rettangolo misurato della finestra)
    fps = R['fps']
    L = C.lavoro(slug, 'prova')
    _, mov, _ = AR._mov(g, fps, L)
    V = C.AGENTE / R['sorgente']['video']
    fnt = ImageFont.truetype(FONT_SANS, 22)
    tiles, grande = [], None
    for t in [float(x) for x in tempi]:
        f = round(t * fps)
        k = f - g['f0']
        if k < 0 or k >= g['frames']:
            print(f"  {t:.2f} s: fuori dalla grafica ({g['f0'] / fps:.2f}–{(g['f0'] + g['frames']) / fps:.2f} s), saltato")
            continue
        im = Image.frombytes('RGB', (W, H), _base(V, f)).convert('RGBA')
        o = L / f'o{f}.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(mov), '-vf', f'select=eq(n\\,{k}),format=rgba', '-frames:v', '1', str(o)], check=True)
        im.alpha_composite(Image.open(o).convert('RGBA'))
        im = im.convert('RGB')
        grande = grande or im
        sm = im.resize(C.mini(390))
        d = ImageDraw.Draw(sm)
        d.rectangle([0, 0, 120, 26], fill=(255, 230, 0))
        d.text((4, 2), f'{t:.2f}s', font=fnt, fill='black')
        tiles.append(sm)
    if not tiles:
        raise SystemExit("nessun istante dentro la grafica")
    cols = min(3 if C.ORIZZONTALE else 6, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    tw, th = C.mini(390)
    foglio = Image.new('RGB', (cols * (tw + 2), rows * (th + 2)), 'white')
    for i, x in enumerate(tiles):
        foglio.paste(x, ((i % cols) * (tw + 2), (i // cols) * (th + 2)))
    out = L / f'prova-{grafica}.jpg'
    foglio.save(out, quality=88)
    grande.save(L / f'prova-{grafica}-grande.png')
    print(C.rel(out))

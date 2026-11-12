"""Tavole del campionario (fase 6b, 27/10/2026): cio che guarda il direttore artistico.

Per ogni modello, in campionario/v2/controlli/:
- `<nn>-tavola.jpg`: il fotogramma migliore a piena risoluzione, lo stesso ridotto a
  390 px di larghezza (un telefono in verticale che guarda un video orizzontale,
  a grandezza vera) e sei fotogrammi chiave in fila;
- `<nn>-telefono-390.png`: il fotogramma migliore a 390 px, da guardare al 100%;
- `<nn>-confronto.jpg`: il fotogramma migliore accanto alla reference piu vicina,
  se in `libreria/reference/` c'e un'immagine che comincia col numero del modello
  (`02-...jpg`). Senza reference il confronto non si fa e il rapporto lo dice.

Il fotogramma migliore e `migliore` della specifica (secondi del montato o ancora
su una parola); senza, il centro del primo elemento.
"""
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .progetto import AGENTE, LIBRERIA, RISORSE

FONT = RISORSE / 'fonts' / 'Montserrat-VF.ttf'
REFERENCE = LIBRERIA / 'reference'


def _f(corpo, peso=600):
    f = ImageFont.truetype(str(FONT), corpo)
    f.set_variation_by_axes([peso])
    return f


def fotogramma(video, t):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f"{max(0, t):.3f}", '-i', str(video), '-frames:v', '1',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
    return Image.frombytes('RGB', (1920, 1080), r.stdout[:1920 * 1080 * 3])


def reference_per(tag):
    if not REFERENCE.is_dir():
        return []
    n = tag[:2]
    return sorted(p for p in REFERENCE.iterdir()
                  if p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.webp') and p.name.startswith((tag, n + '-', n + '_')))


def tavola(video, tag, titolo, t_migliore, t_chiave, ctrl):
    ctrl.mkdir(parents=True, exist_ok=True)
    big = fotogramma(video, t_migliore)
    tel = big.resize((390, 219), Image.LANCZOS)
    tel.save(ctrl / f"{tag}-telefono-390.png")
    W = 1920
    chiavi = [fotogramma(video, t).resize((320, 180), Image.LANCZOS) for t in t_chiave[:6]]
    H = 70 + 1080 + 40 + 219 + 40 + 180 + 60
    sh = Image.new('RGB', (W, H), (0, 26, 61))
    d = ImageDraw.Draw(sh)
    d.text((24, 18), f"{tag} {titolo}  ·  fotogramma migliore a {t_migliore:.2f} s", font=_f(34, 700), fill=(244, 244, 244))
    sh.paste(big, (0, 70))
    y = 70 + 1080 + 40
    d.text((24, y - 34), "a 390 px di larghezza (telefono, grandezza vera):", font=_f(26), fill=(244, 244, 244))
    sh.paste(tel, (24, y))
    d.text((440, y + 10), "stesso fotogramma come appare su un telefono tenuto in verticale.", font=_f(26), fill=(170, 190, 215))
    d.text((440, y + 50), "Un testo di 60 px a 1920 diventa 12 px qui.", font=_f(26), fill=(170, 190, 215))
    y += 219 + 40
    d.text((24, y - 34), "momenti chiave:", font=_f(26), fill=(244, 244, 244))
    for k, (im, t) in enumerate(zip(chiavi, t_chiave)):
        sh.paste(im, (k * 320, y))
        d.text((k * 320 + 8, y + 184), f"{t:.2f} s", font=_f(22), fill=(244, 244, 244))
    sh.save(ctrl / f"{tag}-tavola.jpg", quality=86)
    refs = reference_per(tag)
    if refs:
        ref = Image.open(refs[0]).convert('RGB')
        ref.thumbnail((960, 540))
        conf = Image.new('RGB', (1920 + 40, 540 + 90), (0, 26, 61))
        dc = ImageDraw.Draw(conf)
        dc.text((20, 16), f"{tag} {titolo}: nostro fotogramma", font=_f(30, 700), fill=(244, 244, 244))
        dc.text((1000, 16), f"reference: {refs[0].name}", font=_f(30, 700), fill=(244, 244, 244))
        conf.paste(big.resize((960, 540), Image.LANCZOS), (20, 70))
        conf.paste(ref, (1000 + (960 - ref.width) // 2, 70 + (540 - ref.height) // 2))
        conf.save(ctrl / f"{tag}-confronto.jpg", quality=86)
        return refs[0].name
    return None

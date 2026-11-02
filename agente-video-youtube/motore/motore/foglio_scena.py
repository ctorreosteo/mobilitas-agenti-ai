"""Foglio dei momenti della scena (fase 6c): un fotogramma per momento dal video
consegnato (a meta del primo elemento, o a meta del momento se e solo camera),
ognuno con il suo doppio a 390 px (telefono). Serve a revisore visivo e
direttore artistico per guardare il master, non i pezzi.

    python -m motore.foglio_scena <slug> [video]
"""
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

from .progetto import Progetto, RISORSE

FONT = RISORSE / 'fonts' / 'Montserrat-VF.ttf'


def foglio(slug, video=None):
    P = Progetto(slug)
    S = P.leggi('scena.json')
    video = video or P.render(f"{slug}_FINALE.mp4")
    f = ImageFont.truetype(str(FONT), 22)
    f.set_variation_by_axes([700])
    tw, th = 640, 360
    righe = []
    for m in S['momenti']:
        a, b = m['pezzo']
        tt = [x for x in m.get('testi', [])]
        t = (tt[0]['s'] + min(tt[0]['e'], tt[0]['s'] + 2.5)) / 2 + 0.3 if tt else (a + b) / 2
        t = min(max(t, a + 0.1), b - 0.1)
        r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f"{t:.3f}", '-i', str(video), '-frames:v', '1',
                            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True)
        im = Image.frombytes('RGB', (1920, 1080), r.stdout[:1920 * 1080 * 3])
        righe.append((m['id'], t, [x['modello'] for x in tt] or ['camera'], im))
    cols = 3
    H = 40 + ((len(righe) + cols - 1) // cols) * (th + 219 + 50)
    sh = Image.new('RGB', (cols * (tw + 10) + 10, H), (0, 26, 61))
    d = ImageDraw.Draw(sh)
    for k, (nome, t, mod, im) in enumerate(righe):
        x, y = 10 + (k % cols) * (tw + 10), 40 + (k // cols) * (th + 219 + 50)
        sh.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
        sh.paste(im.resize((390, 219), Image.LANCZOS), (x, y + th + 4))
        d.text((x + 400, y + th + 10), f"{k:02d} {nome}", font=f, fill=(244, 244, 244))
        d.text((x + 400, y + th + 40), f"{t:.2f} s", font=f, fill=(170, 190, 215))
        d.text((x + 400, y + th + 70), ' + '.join(mod), font=f, fill=(114, 250, 147))
    out = P.controllo('scena-momenti.jpg')
    sh.save(out, quality=85)
    print(f"-> controlli/{out.name}")
    return out


if __name__ == '__main__':
    foglio(sys.argv[1], *(sys.argv[2:3]))

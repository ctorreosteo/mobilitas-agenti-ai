#!/usr/bin/env python3
"""Sceglie il lato di ogni card misurando quanto e occupata l'inquadratura.

La zona libera cambia da video a video e, dentro lo stesso video, da momento a
momento: nei primi secondi la presentatrice si sporge in avanti e sporca la
fascia alta di sinistra. Quindi il lato non si assume, si misura sui frame
veri della finestra in cui la card sta a schermo.
"""
import json, subprocess, sys, os, tempfile
sys.path.insert(0, 'scripts')
import numpy as np
from PIL import Image
import mobilitas_style as S

VID = sys.argv[1] if len(sys.argv) > 1 else 'renders/YT_TOFU_02_cut_clean.mp4'
BOX_W, BOX_H = S.CARD_BOX[2], S.CARD_BOX[3]
LEFT = (S.SAFE, S.CARD_BOX[1])
RIGHT = (S.W - S.SAFE - BOX_W, S.CARD_BOX[1])
PAD = 24   # un po' d'aria attorno alla card, deve restare libera anche quella


def grab(t, tmp):
    p = os.path.join(tmp, f"f{t:.2f}.png")
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', f"{t:.3f}",
                    '-i', VID, '-frames:v', '1', '-y', p], check=True)
    return np.asarray(Image.open(p).convert('L'), dtype=np.float32)


def busy(frames, x, y):
    """quanto e occupata la finestra: dettaglio spaziale + movimento nel tempo"""
    crops = [f[max(0, y - PAD):y + BOX_H + PAD, max(0, x - PAD):x + BOX_W + PAD]
             for f in frames]
    st = np.stack(crops)
    m = st.mean(axis=0)
    gx = np.abs(np.diff(m, axis=1, prepend=m[:, :1]))
    gy = np.abs(np.diff(m, axis=0, prepend=m[:1, :]))
    occ = (st.std(axis=0) > 8) | ((gx + gy) > 6)
    return float(occ.mean())


def main():
    plan = json.load(open('data/overlay.json'))
    items = [('card', c) for c in plan['cards']] \
        + [('opening', plan['opening']), ('chip', plan['chip'])]
    with tempfile.TemporaryDirectory() as tmp:
        for kind, c in items:
            ts = [c['s'] + 0.4, (c['s'] + c['e']) / 2, c['e'] - 0.4]
            frames = [grab(t, tmp) for t in ts]
            l, r = busy(frames, *LEFT), busy(frames, *RIGHT)
            c['side'] = 'left' if l <= r else 'right'
            label = c.get('eyebrow', kind)
            print(f"  {c['s']:7.2f}s {label:<16} sinistra {l*100:5.1f}%  "
                  f"destra {r*100:5.1f}%  -> {c['side']}")
    json.dump(plan, open('data/overlay.json', 'w'), indent=1, ensure_ascii=False)
    print("aggiornato data/overlay.json")


if __name__ == '__main__':
    main()

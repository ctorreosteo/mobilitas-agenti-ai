#!/usr/bin/env python3
"""Compone il livello grafico sopra i frame veri, per il controllo visivo."""
import subprocess, sys, os
sys.path.insert(0, 'scripts')
from PIL import Image
import render_overlay as R

OUT = 'snapshots/overlay'
VID = sys.argv[1] if len(sys.argv) > 1 else 'renders/YT_TOFU_02_cut_clean.mp4'
TIMES = [float(x) for x in sys.argv[2:]] or [2.0, 36.0, 174.0, 178.0, 274.0, 346.0, 460.0, 509.0, 735.0, 816.0]
import shutil
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT, exist_ok=True)
scene = R.Scene()
tiles = []
for t in TIMES:
    p = f"{OUT}/t{t:07.2f}.png"
    subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', f"{t:.3f}",
                    '-i', VID, '-frames:v', '1', '-y', p], check=True)
    bg = Image.open(p).convert('RGBA')
    bg.alpha_composite(scene.frame(t))
    bg.convert('RGB').resize((960, 540), Image.LANCZOS).save(p.replace('.png', '.jpg'), quality=88)
    os.remove(p)
    tiles.append(p.replace('.png', '.jpg'))
    print(f"  {t:8.2f}s -> {tiles[-1]}")
cols = 2
rows = -(-len(tiles) // cols)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-pattern_type', 'glob',
                '-i', f'{OUT}/*.jpg', '-filter_complex',
                f'tile={cols}x{rows}:margin=8:padding=6', '-frames:v', '1', '-y',
                'snapshots/overlay-sheet.jpg'], check=True)
print("-> snapshots/overlay-sheet.jpg")

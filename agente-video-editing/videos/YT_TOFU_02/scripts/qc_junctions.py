#!/usr/bin/env python3
"""Estrae i frame a cavallo di ogni giunta del montato, per il controllo visivo."""
import json, subprocess, sys, os

XF = round(5 / (30000 / 1001.0), 4)
MASTER = sys.argv[1] if len(sys.argv) > 1 else 'renders/YT_TOFU_02_master_1080p.mp4'
OUT = 'snapshots/junctions'
os.makedirs(OUT, exist_ok=True)

edl = json.load(open('data/edl.json'))
segs = [(s['in'], s['out']) for s in edl['segments']]
cuts = {round(c['in'], 2): c['reason'] for c in edl['cuts']}

acc, marks = 0.0, []
for i, (a, b) in enumerate(segs[:-1]):
    acc += (b - a) - (XF if i else 0)
    reason = next((r for t, r in cuts.items() if abs(t - b) < 0.05), 'pausa accorciata')
    marks.append((acc, b, reason))

tiles = []
for i, (t, src, reason) in enumerate(marks):
    for tag, tt in (('a', max(0, t - 0.5)), ('b', t + 0.5)):
        p = f"{OUT}/j{i:02d}{tag}.jpg"
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', f"{tt:.3f}",
                        '-i', MASTER, '-frames:v', '1', '-vf', 'scale=420:-2', '-y', p], check=True)
        tiles.append(p)
    print(f"giunta {i:02d}  montato {t:8.2f}s  <- sorgente {src:8.2f}s  {reason[:60]}")

cols = 6
rows = -(-len(tiles) // cols)
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-pattern_type', 'glob',
                '-i', f'{OUT}/*.jpg', '-filter_complex',
                f'tile={cols}x{rows}:margin=6:padding=4', '-frames:v', '1', '-y',
                'snapshots/junctions-sheet.jpg'], check=True)
print(f"\n{len(marks)} giunte -> snapshots/junctions-sheet.jpg")

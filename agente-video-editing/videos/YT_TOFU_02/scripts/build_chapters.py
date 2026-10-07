#!/usr/bin/env python3
"""Capitoli YouTube dagli stacchi gia pianificati, piu apertura e chiusura.

YouTube pretende che il primo capitolo parta da 00:00 e che ce ne siano almeno
tre, ognuno lungo almeno 10 s.
"""
import json

plan = json.load(open('data/overlay.json'))


def ts(t):
    m, s = divmod(int(t), 60)
    return f"{m}:{s:02d}"


rows = [(0.0, "Le 3 del pomeriggio")]
titles = {"MECCANISMO": "Il calo è meccanico, non metabolico",
          "IL CAFFÈ": "Il caffè non risolve, maschera",
          "COSA FARE": "Postura accumulata, non disciplina",
          "LA FRASE": "Il tuo cervello non si stanca, soffoca"}
for c in plan['chapters']:
    rows.append((c['s'] + 1.3, titles.get(c['eyebrow'], c['l1'])))
rows.append((plan['closing']['s'] - 40, "Nel prossimo video: non è ansia, è respirazione"))
rows.sort()

out = "\n".join(f"{ts(t)} {title}" for t, title in rows) + "\n"
open('renders/YT_TOFU_02_capitoli.txt', 'w').write(out)
print(out)

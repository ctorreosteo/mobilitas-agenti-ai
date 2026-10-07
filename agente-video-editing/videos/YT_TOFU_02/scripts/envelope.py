#!/usr/bin/env python3
"""Mappa parlato/silenzio dall'inviluppo RMS a 10 ms.

La soglia sta 20 dB sopra il fondo di sala misurato sul file, non a un valore
fisso: questa registrazione ha un fondo intorno ai -75 dBFS e un parlato che
arriva a -20, e le code di sillaba scendono sotto i -40 restando udibili.
Tagliare su una coda di sillaba tronca la parola, quindi i blocchi devono
comprendere anche quelle code.
"""
import numpy as np, wave, json, sys

HOP = 0.010
MIN_GAP = 0.20      # buchi piu corti non spezzano un blocco
MIN_SPEECH = 0.04   # sotto questa e un click, non una sillaba
MARGIN_DB = 22.0    # quanto sopra il fondo di sala mettere la soglia


def envelope():
    w = wave.open('assets/audio-16k-mono.wav')
    n, sr = w.getnframes(), w.getframerate()
    a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
    hop = int(HOP * sr)
    m = len(a) // hop
    rms = np.sqrt((a[:m * hop].reshape(m, hop) ** 2).mean(axis=1) + 1e-12)
    return 20 * np.log10(rms), m


def blocks():
    db, m = envelope()
    floor = np.percentile(db, 12)          # il fondo di sala
    thr = floor + MARGIN_DB
    voiced = db > thr
    out, i = [], 0
    while i < m:
        if not voiced[i]:
            i += 1
            continue
        j = i
        while j < m:
            if voiced[j]:
                j += 1
                continue
            k = j
            while k < m and not voiced[k]:
                k += 1
            if (k - j) * HOP < MIN_GAP and k < m:
                j = k
            else:
                break
        if (j - i) * HOP >= MIN_SPEECH:
            out.append((round(i * HOP, 3), round(j * HOP, 3)))
        i = j
    return out, floor, thr


if __name__ == '__main__':
    b, floor, thr = blocks()
    json.dump(b, open('data/speech-blocks.json', 'w'))
    print(f"fondo di sala {floor:.1f} dBFS, soglia {thr:.1f} dBFS")
    print(f"{len(b)} blocchi di parlato")
    if len(sys.argv) > 2:
        a, z = float(sys.argv[1]), float(sys.argv[2])
        for s, e in b:
            if e > a and s < z:
                print(f"  {s:8.2f} -> {e:8.2f}   ({e-s:5.2f}s)")

#!/usr/bin/env python3
"""Cerca papere e riprese doppie nella trascrizione a finestre.

Su un file intero whisper APPIANA le riprese doppie: al posto della papera
scrive una frase corretta che non e stata pronunciata. Succede almeno due volte
in questo girato. Le finestre corte non gliela lasciano fare, ma vanno ricucite
prendendo da ciascuna solo la parte centrale, dove l'allineamento e affidabile.
"""
import glob, os, re, sys, json

WIN, STEP, EDGE = 26, 20, 3.0


def stitch():
    words = []
    files = sorted(glob.glob('/private/tmp/claude-501/-Users-carlitos-video-editing/'
                             '7aa8e8d2-1fb8-440b-945d-2cd2fdeab552/scratchpad/win/w*.txt'))
    for i, f in enumerate(files):
        a = int(os.path.basename(f)[1:6])
        lo = a if i == 0 else a + EDGE
        hi = 1e9 if i == len(files) - 1 else a + STEP + EDGE
        for line in open(f):
            p = line.rstrip('\n').split('\t')
            if len(p) != 3:
                continue
            s, e, t = float(p[0]), float(p[1]), p[2].strip()
            if t and lo <= s < hi:
                words.append((s, e, t))
    return sorted(words)


def scan(W):
    norm = [re.sub(r"[^\wàèéìòùáíóúï']", '', t.lower()) for _, _, t in W]
    hits = []

    # 1. n-grammi ripetuti a breve distanza: la firma della ripresa doppia
    for N in (4,):
        seen = {}
        for i in range(len(W) - N):
            key = tuple(norm[i:i + N])
            if any(not k for k in key):
                continue
            if key in seen:
                j = seen[key]
                if 0 < W[i][0] - W[j][1] < 80:
                    hits.append(('ripetuta', W[j][0], W[i][0], ' '.join(key)))
            seen[key] = i

    # 2. parole troncate e interiezioni di regia
    mark = re.compile(r'\.\.\.$|^(no|ok|okay|ah|eh|dai|scusa|scusami|aspetta|aspetta,|niente)[,.!?]?$'
                      r'|sbagliat|scusam|aspett|riprendiam|ricomincia', re.I)
    for i, (s, e, t) in enumerate(W):
        if mark.search(t):
            hits.append(('marker', s, e, ' '.join(x[2] for x in W[max(0, i - 6):i + 7])))
    return hits


def group(hits):
    hits = sorted(hits, key=lambda h: h[1])
    out = []
    for h in hits:
        if out and h[1] - out[-1][-1] < 8:
            out[-1][-1] = max(out[-1][-1], h[2])
            out[-1][1].add(h[0])
            if len(out[-1][2]) < 3:
                out[-1][2].append(h[3])
        else:
            out.append([h[1], {h[0]}, [h[3]], h[2]])
    return out


if __name__ == '__main__':
    W = stitch()
    json.dump([[s, e, t] for s, e, t in W], open('data/words-windowed.json', 'w'),
              ensure_ascii=False)
    print(f"{len(W)} parole ricucite, fino a {W[-1][1]:.1f}s -> data/words-windowed.json\n")
    g = group(scan(W))
    print(f"=== {len(g)} regioni sospette ===")
    for start, kinds, ex, end in g:
        print(f"\n{start:8.2f} - {end:8.2f}  [{','.join(sorted(kinds))}]")
        for e in ex:
            print(f"    {e[:160]}")

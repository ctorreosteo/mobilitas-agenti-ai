#!/usr/bin/env python3
"""Ritempra la trascrizione sul montaggio e la impagina come SRT a corredo.

La trascrizione arriva parola per parola con allineamento DTW: qui le parole
vengono rimappate dal tempo sorgente al tempo montato, scartando quelle che
cadono dentro i tagli, e raggruppate in battute che si spezzano sulla
punteggiatura invece che sulla lunghezza.
"""
import json, re

WORDS_JSON = 'data/words-cut.json'
XF = round(5 / (30000 / 1001.0), 4)   # la dissolvenza usata nel montaggio
MAX_CHARS = 40
MAX_LINES = 2
MAX_DUR = 3.6
MIN_DUR = 1.1
GAP_BREAK = 0.55

# refusi del riconoscitore. L'audio non viene toccato: si corregge solo il testo.
FIXES = [
    (r"\ball'escrivania\b", "alla scrivania"),
    (r"\balla scrimania\b", "alla scrivania"),
    (r"\ball'iscrivania\b", "alla scrivania"),
    (r"\bti granlunga\b", "di gran lunga"),
    (r"\bun'inquinione\b", "un'opinione"),
    (r"\bgambia toracica\b", "gabbia toracica"),
    (r"\bsuddolo\b", "subdolo"),
    (r"\bTieni la stretta\b", "Tienila stretta"),
    (r"\bcervico dorsale\b", "cervico-dorsale"),
    (r"\bcali della capacità\b", "cali della capacità"),
]

# Il DTW colloca "davvero." ~0,8s dopo che il parlato e gia cessato (l'inviluppo
# RMS mette la fine a 1160,96s, il DTW a 1164,14s), quindi la parola cade fuori
# dall'ultimo segmento e sparirebbe dalla battuta di chiusura. L'audio del master
# la contiene: la si riattacca qui.
TAIL_FIX = ('iniziato a guardare quello che',
            'iniziato a guardare quello che succede davvero.')

SENT_END = re.compile(r'[.!?]["\')\]]?$')
SOFT_BREAK = re.compile(r'[,;:]$')


def load_words(path):
    """con -ml 1 -sow ogni segmento e una parola, con timing DTW."""
    d = json.load(open(path))
    W = []
    for seg in d['transcription']:
        t = seg['text'].strip()
        if t:
            W.append([seg['offsets']['from'] / 1000.0,
                      seg['offsets']['to'] / 1000.0, t])
    return W


def remap(words, segments):
    """tempo sorgente -> tempo montato.

    Ogni giunta e una dissolvenza di XF secondi in cui i due segmenti si
    sovrappongono: il montato e piu corto della somma dei segmenti di
    XF per ogni giunta, e i sottotitoli devono seguire quella compressione.
    """
    out, base = [], 0.0
    for i, seg in enumerate(segments):
        a, b = seg['in'], seg['out']
        for s, e, t in words:
            if e <= a or s >= b:
                continue
            # una parola tagliata a meta dalla giunta appartiene al segmento
            # in cui e stata pronunciata per piu della meta della sua durata
            if min(e, b) - max(s, a) < 0.5 * (e - s):
                continue
            out.append([max(s, a) - a + base, min(e, b) - a + base, t])
        base += (b - a) - XF
    return sorted(out)


def wrap(text):
    lines, cur = [], ''
    for w in text.split():
        cand = (cur + ' ' + w).strip()
        if len(cand) > MAX_CHARS and cur:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def group(words):
    cues, cur = [], []
    for w in words:
        if cur:
            gap = w[0] - cur[-1][1]
            dur = cur[-1][1] - cur[0][0]
            last = cur[-1][2]
            text = ' '.join(x[2] for x in cur)
            overflow = len(wrap(text + ' ' + w[2])) > MAX_LINES
            if (SENT_END.search(last) or overflow or dur >= MAX_DUR
                    or gap > GAP_BREAK
                    or (SOFT_BREAK.search(last) and dur >= 1.7)):
                cues.append(cur)
                cur = []
        cur.append(w)
    if cur:
        cues.append(cur)
    return cues


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace('.', ',')


def main():
    edl = json.load(open('data/edl.json'))
    XF = round(5 / (30000 / 1001.0), 4)
    segs = [(x['in'], x['out']) for x in edl['segments']]
    total = sum(b - a for a, b in segs) - XF * (len(segs) - 1)
    # words-cut.json e gia trascritto sul montato: nessuna rimappatura, nessuna
    # correzione di coda. Il file a corredo dice esattamente cio che si sente.
    mapped = [[w[0], w[1], w[2]] for w in load_words(WORDS_JSON)]
    cues = group(mapped)

    blocks, new_sentence = [], True
    for i, c in enumerate(cues, 1):
        start, end = c[0][0], c[-1][1]
        end = max(end, start + MIN_DUR)
        if i < len(cues):
            end = min(end, cues[i][0][0] - 0.04)
        end = min(max(end, start + 0.5), total - 0.05)

        text = re.sub(r'\s+([.,!?;:])', r'\1', ' '.join(x[2] for x in c))
        for pat, rep in FIXES:
            text = re.sub(pat, rep, text, flags=re.I)
        if new_sentence and text:
            text = text[0].upper() + text[1:]
        new_sentence = bool(SENT_END.search(text))

        if i == len(cues) and text.strip() == TAIL_FIX[0]:
            text = TAIL_FIX[1]
        blocks.append(f"{i}\n{ts(start)} --> {ts(end)}\n" + '\n'.join(wrap(text)))

    open('renders/YT_TOFU_02.srt', 'w').write('\n\n'.join(blocks) + '\n')
    dur = [c[-1][1] - c[0][0] for c in cues]
    print(f"{len(cues)} battute, durata media {sum(dur)/len(dur):.2f}s, "
          f"max {max(dur):.2f}s -> renders/YT_TOFU_02.srt")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Pianifica sottotitoli e infografiche sul tempo del montato.

Regola che vale per tutto il file: **niente testo inventato**. Ogni parola che
finisce a schermo o viene dalla trascrizione, oppure e un'etichetta strutturale
(MECCANISMO, CASO IN STUDIO, PROSSIMO VIDEO). Le glosse sotto i numeri
riformulano quello che dice, non aggiungono affermazioni cliniche.
"""
import json, re, sys
sys.path.insert(0, 'scripts')
import mobilitas_style as S

GROUP_MAX = 3          # parole per gruppo di sottotitolo
GROUP_GAP = 0.45       # una pausa piu lunga chiude il gruppo
GROUP_MAXDUR = 2.4

FIXES = [
    (r"\ball'escrivania\b|\balla scrimania\b|\ball'iscrivania\b", "alla scrivania"),
    (r"\bti granlunga\b|\bdi granlunga\b", "di gran lunga"),
    (r"\bun'inquinione\b", "un'opinione"),
    (r"\bgambia\b", "gabbia"),
    (r"\bsuddolo\b|\bsudolo\b", "subdolo"),
    (r"\bcalopo meridiano\b|\bcalo po meridiano\b", "calo pomeridiano"),
    (r"\bcosse\b", "coste"),
    (r"\bTieni la stretta\b|\bTieni rastretta\b", "Tienila stretta"),
    (r"\bTieni la vicina\b", "Tienila vicina"),
    (r"\bcervico dorsale\b", "cervico-dorsale"),
    (r"\bcalo dell'interesse\b", "calo delle tre"),
    (r"\bdell'E3\b", "delle tre"),
]


def load_words():
    d = json.load(open('data/words-cut.json'))
    W = []
    for s in d['transcription']:
        t = s['text'].strip()
        if t:
            W.append({'t': t, 's': s['offsets']['from'] / 1000.0,
                      'e': s['offsets']['to'] / 1000.0})
    for w in W:
        for pat, rep in FIXES:
            w['t'] = re.sub(pat, rep, w['t'], flags=re.I)
    return W


ACC = str.maketrans("àáâäèéêëìíîïòóôöùúûüç", "aaaaeeeeiiiioooouuuuc")


def norm(t):
    return re.sub(r"[^\w']", '', t.lower().translate(ACC))


def find(W, phrase, after=0.0):
    """primo istante in cui inizia la frase cercata"""
    target = [norm(x) for x in phrase.split()]
    n = len(target)
    for i in range(len(W) - n):
        if W[i]['s'] < after:
            continue
        if [norm(W[j]['t']) for j in range(i, i + n)] == target:
            return i
    return None


def groups(W):
    out, cur = [], []
    for w in W:
        if cur:
            gap = w['s'] - cur[-1]['e']
            dur = cur[-1]['e'] - cur[0]['s']
            ends = re.search(r'[.!?]$', cur[-1]['t'])
            if len(cur) >= GROUP_MAX or gap > GROUP_GAP or dur > GROUP_MAXDUR or ends:
                out.append(cur)
                cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    res = []
    for i, g in enumerate(out):
        s = g[0]['s']
        e = g[-1]['e'] + 0.12
        if i + 1 < len(out):
            e = min(e, out[i + 1][0]['s'] - 0.01)
        res.append({'s': round(s, 3), 'e': round(max(e, s + 0.30), 3),
                    'words': [{'t': w['t'], 's': round(w['s'], 3),
                               'e': round(w['e'], 3)} for w in g]})
    return res


CARDS = [
    ("il tuo cervello consuma", "OSSIGENO",     "20",    "%",   "dell'ossigeno che entra nel corpo se lo prende il cervello"),
    ("pesa il 2",               "PESO",         "2",     "%",   "quanto pesa il cervello sul totale del corpo"),
    ("si abbassa di 3",         "DIAFRAMMA",    "3-4",   "cm",  "di escursione a ogni respiro, quando è libero"),
    ("si muove di un",          "DOPO 5 ORE",   "1",     "cm",  "quello che resta dopo mezza giornata seduto"),
    ("30 o",                    "CAPACITÀ",     "30-40", "%",   "in meno rispetto alla mattina"),
    ("per 40 minuti",           "IL CAFFÈ",     "40",    "min", "poi cadi più in basso di dove eri partito"),
    ("ridotta di meta",         "IN STUDIO",    "50",    "%",   "di escursione in meno, in chi lavora seduto da anni"),
    ("lavorare otto ore",       "IL RISULTATO", "8",     "ore", "con la stessa testa delle nove del mattino"),
]

CHAPTERS = [
    ("meccanico non",     "MECCANISMO",    "MECCANICO,", "NON METABOLICO"),
    ("caffe non risolve", "IL CAFFÈ",   "NON RISOLVE,", "MASCHERA"),
    ("postura accumulata", "COSA FARE",    "POSTURA ACCUMULATA,", "NON DISCIPLINA"),
    ("il tuo cervello non", "LA FRASE",    "NON SI STANCA.", "SOFFOCA."),
]


def main():
    W = load_words()
    # la durata e quella del montato, non quella dell'ultima parola: il livello
    # grafico deve coprire tutti i frame, o overlay=shortest taglia la coda
    XF = round(5 / S.FPS, 4)
    segs = [(x['in'], x['out']) for x in json.load(open('data/edl.json'))['segments']]
    dur = sum(b - a for a, b in segs) - XF * (len(segs) - 1)
    caps = groups(W)

    cards = []
    for phrase, eyebrow, value, unit, sub in CARDS:
        i = find(W, phrase)
        if i is None:
            print(f"  ! card non ancorata: {phrase!r}")
            continue
        s = round(W[i]['s'] - 0.25, 3)
        cards.append({'s': s, 'e': round(s + 4.2, 3), 'eyebrow': eyebrow,
                      'value': value, 'unit': unit, 'sub': sub})

    chapters = []
    for phrase, eyebrow, l1, l2 in CHAPTERS:
        i = find(W, phrase, after=chapters[-1]['e'] + 20 if chapters else 0)
        if i is None:
            print(f"  ! stacco non ancorato: {phrase!r}")
            continue
        s = round(W[i]['s'] - 1.30, 3)
        chapters.append({'s': s, 'e': round(s + 1.75, 3),
                         'eyebrow': eyebrow, 'l1': l1, 'l2': l2})

    plan = {
        'fps': S.FPS, 'duration': round(dur, 3),
        'opening': {'s': 0.35, 'e': 5.60, 'eyebrow': "MOBILITAS · STUDIO OSTEOPATICO",
                    'l1': "LE 3 DEL POMERIGGIO,", 'l2': "SEMPRE LO STESSO PUNTO"},
        'chip': {'s': 34.0, 'e': 40.0, 'name': "MOBILITAS", 'role': "STUDIO OSTEOPATICO"},
        'closing': {'s': round(dur - 5.5, 3), 'e': round(dur, 3),
                    'eyebrow': "PROSSIMO VIDEO", 'l1': "NON È ANSIA.", 'l2': "È RESPIRAZIONE.",
                    'cta': "ISCRIVITI AL CANALE", 'brand': "MOBILITAS · STUDIO OSTEOPATICO"},
        'cards': cards, 'chapters': chapters, 'captions': caps,
    }
    json.dump(plan, open('data/overlay.json', 'w'), indent=1, ensure_ascii=False)
    print(f"durata {dur:.2f}s")
    print(f"{len(caps)} gruppi di sottotitolo (media {sum(c['e']-c['s'] for c in caps)/len(caps):.2f}s)")
    print(f"{len(cards)} card dato, {len(chapters)} stacchi di capitolo")
    for c in cards:
        print(f"   card {c['s']:7.2f}s  {c['value']}{c['unit']:<4} {c['eyebrow']}")
    for c in chapters:
        print(f"   stacco {c['s']:7.2f}s  {c['l1']} {c['l2']}")
    print("scritto data/overlay.json")


if __name__ == '__main__':
    main()

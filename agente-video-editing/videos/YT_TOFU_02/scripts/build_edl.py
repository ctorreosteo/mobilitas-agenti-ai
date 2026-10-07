#!/usr/bin/env python3
"""EDL di YT_TOFU_02.

Le papere sono state trovate sondando ogni pausa: per ogni buco di silenzio si
trascrivono separatamente i 9 secondi prima e i 9 dopo (scripts/gap_probe.sh).
Due clip distinte, cosi whisper non puo appianare la ripresa doppia riscrivendo
una frase corretta al posto della papera — cosa che su file intero fa, e in
questo girato l'ha fatta almeno tre volte.

Gli ancoraggi qui sotto sono in secondi sorgente e indicano l'ultima parola da
tenere e la prima da riprendere. Il punto di taglio esatto lo trova
cutpoints.quiet_after / quiet_before, cercando il primo istante in cui l'energia
e tornata al fondo di sala: i confini dei blocchi di parlato cadono troppo
presto e troncano la coda della sillaba.
"""
import json, sys
sys.path.insert(0, 'scripts')
from cutpoints import quiet_after, quiet_before, level

SRC_DUR = 1184.368333
FPS = 30000 / 1001.0

# (fine ultima parola da tenere, inizio prima parola da riprendere, span, motivo)
REMOVE = [
    (0.00,   12.96, 0.6, "ciak: 'buongiorno a tutti', '1 2 3 4 3 2 1, tofu 2'"),
    (112.62, 144.07, 0.6, "prima ripresa di 'Non sei pigro e non e il pranzo' + 'ho sbagliato, torna leggermente indietro'"),
    (234.21, 243.89, 0.6, "falso attacco 'Il calo delle tre e meccanico, non meccanico'"),
    (319.48, 346.88, 0.6, "falsa partenza 'Ecco cosa succede' + 'ho sbagliato, torna su un pochettino'"),
    (419.67, 427.58, 0.30, "falsa partenza 'Studi sulla meccanica respiratoria' + 'l'ho detto male, aspetta'"),
    (474.75, 475.00, 0.6, "SPECIALE: vedi sotto"),   # sostituito subito dopo
    (634.96, 684.96, 0.6, "papera lunga: 'no ho sbagliato / dai invece / parto da / scusami'"),
    (734.60, 747.30, 0.6, "vuoto di 9s + regia a voce 'il titolo e postura accumulata non disciplina'"),
    (804.08, 810.61, 0.6, "prima ripresa incompleta 'un problema di postura'"),
    (819.28, 840.61, 0.6, "falsa partenza 'in modo significativo' (voleva dire sintomatico) + 'aspetta'"),
    (910.87, 915.71, 0.6, "ripetizione 'si lavora sulla mobilita delle prime coste'"),
    (1056.07, 1102.50, 0.6, "'nel prossimo video' interrotto + regia 'torna su, e troppo lungo il periodo'"),
    (1161.43, None, 0.6, "'mi sa che abbiamo finito, c'e il conteggio parole' + 'naif' + coda muta"),
]
# la ripresa del caffe: si tiene la prima lettura di "Il caffe non risolve,
# maschera" e si scarta tutto quello che segue fino a "Adesso pensa onestamente"
# — in mezzo ci sono il tentativo interrotto, "no ho sbagliato" e lo scambio con
# la regia ("stoppa allora li", "vai ragazzi").
REMOVE[5] = (474.75, 519.95, 0.6,
             "'Adesso pensa...' interrotto, 'no ho sbagliato', regia ('stoppa allora li', 'vai ragazzi') e riprese doppie")

PAUSE_MAX = 1.80
PAUSE_KEEP = 0.80
MIN_SEG = 1.40
MIN_BLOCK = 0.12   # sotto questa un blocco e un respiro, non una parola


def main():
    blocks = [tuple(x) for x in json.load(open('data/speech-blocks.json'))]
    solid = [b for b in blocks if b[1] - b[0] >= MIN_BLOCK]

    cuts = []
    for a, b, span, why in REMOVE:
        ca = 0.0 if a <= 0.01 else quiet_after(a, span)
        cb = SRC_DUR if b is None else quiet_before(b, span)
        cuts.append((round(ca, 3), round(cb, 3), why))

    keeps, pos = [], 0.0
    for a, b, _ in cuts:
        if a > pos:
            keeps.append((pos, a))
        pos = max(pos, b)
    if pos < SRC_DUR:
        keeps.append((pos, SRC_DUR))

    gaps = [(e1, s2) for (s1, e1), (s2, _) in zip(solid, solid[1:]) if s2 - e1 > PAUSE_MAX]

    tight, trimmed = [], []
    for ks, ke in keeps:
        cursor = ks
        for gs, ge in gaps:
            if gs < ks or ge > ke:
                continue
            head = quiet_after(gs, 0.6)
            tail = quiet_before(ge, 0.6)
            if head - cursor < MIN_SEG:
                head = min(cursor + MIN_SEG, tail - 0.35)
            if tail - head < PAUSE_KEEP * 0.5 or head <= cursor:
                continue
            tight.append((cursor, head))
            trimmed.append((head, tail))
            cursor = tail
        if ke - cursor > 0.05:
            tight.append((cursor, ke))

    cut_s = sum(b - a for a, b, _ in cuts)
    pause_s = sum(b - a for a, b in trimmed)
    kept = sum(b - a for a, b in tight)

    print("=== papere e riprese doppie rimosse ===")
    for a, b, why in cuts:
        print(f"  {a:8.2f} -> {b:8.2f}  (-{b-a:6.2f}s)  {why}")
    print(f"  subtotale: -{cut_s:.1f}s")
    print(f"\n=== pause > {PAUSE_MAX}s accorciate === {len(trimmed)} pause, -{pause_s:.1f}s")

    print("\n=== energia residua a ogni giunta (deve stare sotto -55 dB) ===")
    worst = []
    for i, (a, b) in enumerate(tight):
        if i:
            worst.append((level(a), f"seg{i:02d} IN  {a:.2f}"))
        if i < len(tight) - 1:
            worst.append((level(b), f"seg{i:02d} OUT {b:.2f}"))
    worst.sort(reverse=True)
    for db, tag in worst[:6]:
        print(f"  {tag}: {db:6.1f} dB" + ("   <<< CONTROLLARE" if db > -55 else ""))

    print(f"\nsorgente {SRC_DUR/60:.1f} min -> montato {kept/60:.2f} min "
          f"({kept:.1f}s, {len(tight)} segmenti)")

    json.dump({'fps': FPS, 'source_duration': SRC_DUR,
               'cuts': [{'in': a, 'out': b, 'reason': w} for a, b, w in cuts],
               'pauses_trimmed': [{'in': round(a, 3), 'out': round(b, 3)} for a, b in trimmed],
               'segments': [{'in': round(a, 3), 'out': round(b, 3)} for a, b in tight]},
              open('data/edl.json', 'w'), indent=2, ensure_ascii=False)
    print("\nscritto data/edl.json")


if __name__ == '__main__':
    main()

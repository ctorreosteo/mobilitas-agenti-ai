#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dal minutaggio al budget di parole per ogni blocco di una VSL.

Uso:
    python3 vsl-budget.py 22                 # 22 minuti, pubblico tiepido
    python3 vsl-budget.py 8  --caldo         # pubblico gia consapevole (liv. 4-5)
    python3 vsl-budget.py 30 --freddo        # pubblico freddo (liv. 1-2)
    python3 vsl-budget.py 60 --webinar       # struttura a 3 segreti
    python3 vsl-budget.py 12 --wpm 130       # ritmo piu lento (dimostrazioni a schermo)

Costante: 150 parole al minuto. E' il ritmo di un testo scritto per essere
ascoltato, piu lento del parlato spontaneo. Con dimostrazioni a schermo: 130.
"""
import sys

# blocco: (nome, %standard, %freddo, %caldo, %webinar)
BLOCCHI = [
    ("1  Cold open",                    3,  3,  4,  2),
    ("2  Grande promessa",              3,  3,  5,  3),
    ("3  Qualificazione",               3,  2,  2,  3),
    ("4  Anticipo di prova",            3,  3,  4,  2),
    ("5  Storia",                      13, 16,  8, 11),
    ("6  Meccanismo del PROBLEMA",     16, 18, 17, 19),
    ("7  Reversal",                     4,  4,  3,  3),
    ("8  Meccanismo della SOLUZIONE",  14, 16, 10, 11),
    ("9  Prova",                       10, 12, 10, 10),
    ("10 Rivelazione del prodotto",     4,  3,  6,  3),
    ("11 Bullet / fascinations",        7,  6,  9,  5),
    ("12 Stack",                        5,  4,  7,  7),
    ("13 Ancoraggio e prezzo",          4,  3,  5,  4),
    ("14 Inversione del rischio",       4,  3,  4,  3),
    ("15 Urgenza reale",                2,  1,  2,  1),
    ("16 CTA",                          3,  2,  3,  7),
    ("17 Obiezioni e chiusure",         2,  1,  1,  6),
]

# autoverifica: ogni colonna deve sommare 100 e il reversal (blocco 7)
# deve cadere tra il 40% e il 55% della durata
for _c, _nome in ((1, "standard"), (2, "freddo"), (3, "caldo"), (4, "webinar")):
    _tot = sum(_b[_c] for _b in BLOCCHI)
    assert _tot == 100, "colonna %s somma %d invece di 100" % (_nome, _tot)
    _pre = sum(_b[_c] for _b in BLOCCHI[:6])
    assert 40 <= _pre <= 55, "colonna %s: reversal al %d%%" % (_nome, _pre)

BREVE = [  # sotto i 3 minuti restano solo i blocchi incomprimibili
    ("1  Cold open",                   12),
    ("2  Grande promessa",             10),
    ("6  Meccanismo del PROBLEMA",     18),
    ("8  Meccanismo della SOLUZIONE",  20),
    ("9  Prova",                       12),
    ("10 Prodotto + offerta",          14),
    ("14 Inversione del rischio",       6),
    ("16 CTA",                          8),
]

def mmss(sec):
    return "%d:%02d" % (int(sec) // 60, int(sec) % 60)

def main():
    arg = sys.argv[1:]
    if not arg:
        print(__doc__); return
    try:
        minuti = float(arg[0].replace(',', '.'))
    except ValueError:
        print("Primo argomento: i minuti. Esempio: vsl-budget.py 22"); return

    wpm = 150
    if '--wpm' in arg:
        wpm = int(arg[arg.index('--wpm') + 1])
    col, modo = 1, "tiepido (consapevolezza 2-3)"
    if '--freddo' in arg:  col, modo = 2, "FREDDO (consapevolezza 1-2)"
    if '--caldo' in arg:   col, modo = 3, "CALDO (consapevolezza 4-5)"
    if '--webinar' in arg: col, modo = 4, "WEBINAR / 3 segreti"

    tot_parole = int(minuti * wpm)
    breve = minuti < 3

    print("=" * 68)
    print("  VSL DA %g MINUTI  |  %s" % (minuti, modo))
    print("  %d parole totali  @  %d parole/minuto" % (tot_parole, wpm))
    print("=" * 68)

    if breve:
        print("  Sotto i 3 minuti restano solo i blocchi incomprimibili.\n")
        righe = [(n, p) for n, p in BREVE]
    else:
        righe = [(b[0], b[col]) for b in BLOCCHI]

    print("  %-32s %7s %8s %14s" % ("BLOCCO", "parole", "durata", "da -> a"))
    print("  " + "-" * 64)
    cursore = 0.0
    reversal_start = None
    for nome, pct in righe:
        parole = int(round(tot_parole * pct / 100.0))
        sec = parole / (wpm / 60.0)
        if nome.startswith("7 "):
            reversal_start = cursore
        print("  %-32s %7d %8s %6s -> %-6s" % (nome, parole, mmss(sec), mmss(cursore), mmss(cursore + sec)))
        cursore += sec
    print("  " + "-" * 64)
    print("  %-32s %7d %8s" % ("TOTALE", tot_parole, mmss(cursore)))

    # --- act-out ---
    passo = 105 if minuti >= 8 else 75
    tempi = []
    t = passo
    while t < cursore - 30:
        tempi.append(mmss(t)); t += passo
    print("\n  ACT-OUT — una riga che apre, prima di ogni cambio di sezione")
    print("  (%d in tutto, ogni ~%d secondi)" % (len(tempi), passo))
    if tempi:
        for i in range(0, len(tempi), 10):
            print("   " + "  ".join(tempi[i:i+10]))

    # --- controlli ---
    print("\n  CONTROLLI")
    if reversal_start is not None:
        pos = 100.0 * reversal_start / cursore
        esito = "OK" if 40 <= pos <= 55 else "FUORI POSTO - va tra il 40% e il 55%"
        print("   Reversal al %.0f%% (%s)   %s" % (pos, mmss(reversal_start), esito))
    print("   Semina dell'offerta: entro %s (primo terzo)" % mmss(cursore / 3))
    print("   Prova prima del prezzo: obbligatorio")
    print("   Punti di verifica ritenzione: 0:05, 0:30, %s (pitch), %s (prezzo)" %
          (mmss(cursore * 0.55), mmss(cursore * 0.75)))

    # --- avvisi ---
    avvisi = []
    if col == 2 and minuti < 15:
        avvisi.append("Pubblico FREDDO sotto i 15 minuti: non c'e spazio per costruire i due meccanismi.")
    if col == 3 and minuti > 15:
        avvisi.append("Pubblico CALDO sopra i 15 minuti: chi e gia convinto si annoia. Valuta di accorciare.")
    if col == 4 and minuti < 40:
        avvisi.append("Struttura webinar sotto i 40 minuti: i 3 segreti non ci stanno.")
    if breve:
        avvisi.append("Sotto i 3 minuti: niente storia, niente stack, niente obiezioni. "
                      "Se il claim e grande, questa durata non regge la prova che serve.")
    if avvisi:
        print("\n  AVVISI")
        for a in avvisi:
            print("   ! " + a)
    print()

if __name__ == '__main__':
    main()

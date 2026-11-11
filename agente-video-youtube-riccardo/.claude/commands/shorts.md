---
description: Sceglie e produce gli Shorts 9:16 di un video già montato (fuori dal flusso standard: solo se richiesto)
argument-hint: "<slug> [quanti]"
---

Produci gli Shorts del video `$ARGUMENTS` (skill `mobilitas-regia`, sezione 6).

1. Leggi il montato (`data/parole-montato.json`) e scegli 3-5 momenti che stanno in piedi da soli: attacco netto, chiusura che risolve, 25-75 s. Scrivili in `shorts` di `regia.json` con `da`, `a`, `hook` (due righe, la seconda in menta) e `titolo`.
2. `./mve shorts <slug>` (oppure `--solo 0,2` per rifarne solo alcuni).
3. Guarda `controlli/short<N>.jpg`: hook leggibile e sotto la barra, sottotitoli sopra l'interfaccia, volto intero nel verticale.
4. Riporta a chi li ha chiesti: file, durata, titolo proposto per ogni short. Gli Shorts non fanno parte della consegna standard: si fanno solo su richiesta esplicita.

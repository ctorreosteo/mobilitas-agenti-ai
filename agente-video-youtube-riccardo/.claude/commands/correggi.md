---
description: Applica una correzione segnalata su un video ("a 4:32 c'è una parola tagliata")
argument-hint: "<NOME> <cosa e dove>"
---

È stato segnalato: `$ARGUMENTS`.

1. Per ogni istante citato: `./mve dove <NOME> <m:ss>`. Ti dice il tempo sorgente, la giunta vicina, il pezzo di inquadratura e le parole attorno.
2. Verifica il difetto **sul file** (anteprima o consegnato) con una sonda breve (2-4 s) o un fotogramma: capisci cosa c'è prima di correggere.
3. Correggi nel posto giusto:
   - taglio sbagliato o papera rimasta → `tagli` in `regia.json`;
   - refuso nei sottotitoli → `correzioni`;
   - grafica → `scena.momenti` in `regia.json`;
   - inquadratura → `./mve monta <NOME> --solo <pezzo>` dopo aver capito perché è venuta male.
4. `./mve stato <NOME>` e rifai le fasi indicate. Se il video era già stato approvato, rifai l'anteprima e chiedi di nuovo l'ok prima del finale; poi QC CONSEGNABILE.
5. **Il difetto è un controllo che mancava.** In questa cartella il motore non si cambia: scrivi in `STATO.md`, sezione «Per il laboratorio», quale controllo l'avrebbe trovato. Lo aggiunge Riccardo in una versione nuova.
6. Aggiungi a `STATO.md` la correzione: cosa, dove, perché era sfuggito.

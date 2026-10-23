---
description: Applica una correzione segnalata da Carlos su un video consegnato ("a 4:32 c'è una parola tagliata")
argument-hint: "<slug> <cosa e dove>"
---

Carlos ha segnalato: `$ARGUMENTS`.

1. Per ogni istante citato: `./mve dove <slug> <m:ss>`. Ti dice il tempo sorgente, la giunta vicina, il pezzo di inquadratura e le parole attorno.
2. Verifica il difetto **sul file consegnato** con una sonda breve (2-4 s) o un fotogramma: capisci cosa c'è prima di correggere.
3. Correggi nel posto giusto:
   - taglio sbagliato o papera rimasta → `tagli` in `regia.json`;
   - refuso nei sottotitoli → `correzioni`;
   - grafica → `card`, `capitoli`, `enfasi`…;
   - inquadratura → `./mve monta <slug> --solo <pezzo>` dopo aver capito perché è venuta male.
4. `./mve stato <slug>` e rifai le fasi indicate, fino a QC CONSEGNABILE.
5. **Il difetto è un controllo che mancava.** Chiediti quale controllo del motore l'avrebbe trovato; se non c'è, aggiungilo (in `motore/`, in modo generale), verifica che sul banco di prova `YT_TOFU_02-v2` non rompa niente, e scrivilo nella skill giusta.
6. Aggiungi al `BRIEF.md` del video la correzione: cosa, dove, perché era sfuggito, quale controllo lo prende ora.

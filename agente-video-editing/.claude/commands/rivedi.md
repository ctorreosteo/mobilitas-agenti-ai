---
description: Revisione completa di un video già montato, con i tre revisori in parallelo, e correzione di quello che trovano
argument-hint: "<slug>"
---

Rivedi il video `$ARGUMENTS` come se lo vedessi per la prima volta.

1. `./mve stato $ARGUMENTS`: se qualcosa è DA RIFARE, rifallo prima.
2. Lancia **nello stesso messaggio** i subagenti `cacciatore-papere`, `regista` e `revisore-visivo` sullo slug.
3. Mentre lavorano, leggi tu `controlli/QC.md` e `controlli/giunte.md`.
4. Per ogni rilievo decidi: correggi (in `regia.json`, o nel motore se il difetto è del motore) oppure scarta con il motivo. Un rilievo dei revisori è un ingresso, non un ordine.
5. Rifai le fasi che `./mve stato` indica, fino a QC CONSEGNABILE.
6. Aggiorna il `BRIEF.md` del video con una sezione "Revisione del <data>": cosa è stato trovato, cosa è stato corretto, cosa è stato scartato e perché.

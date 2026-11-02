---
description: Edita un video da capo, dal girato in inbox/<NOME>/ all'anteprima da approvare e poi alla consegna (come «Edita il video <NOME>»)
argument-hint: "<NOME della cartella in inbox/>"
---

Edita il video `$ARGUMENTS` seguendo il flusso e i cancelli di `CLAUDE.md`: è la stessa cosa che scrivere «Edita il video $ARGUMENTS».

1. **Materiali.** `./mve stato` (senza nome): la riga di `inbox/$ARGUMENTS` deve avere ✓. Se manca girato, script, nome dell'osteopata o tipo di video, **chiedilo e fermati**. Se manca uno strumento, rimanda a `INSTALLAZIONE.md` e fermati.
2. **Stato.** Se `videos/$ARGUMENTS/STATO.md` esiste, è una ripresa: leggilo, lancia `./mve stato $ARGUMENTS` e riparti dalla prima fase non fatta. Se no: `./mve init inbox/$ARGUMENTS/` e crea `STATO.md`.
3. **Tagli**: prep, trascrivi, volti, papere; leggi trascrizione e referto, lancia `cacciatore-papere`, scrivi i tagli; edl, audio, giunte.
4. **Piano grafico** dal catalogo intero (`./mve catalogo $ARGUMENTS`, `motore/inserti/CATALOGO-MODELLI.md`), poi `regia.json → scena`.
5. **Grafiche e controlli**: grafica, inquadra, monta, scena; guarda le strisce, lancia `regista` e `revisore-visivo`; correggi.
6. **Anteprima**: `./mve finale $ARGUMENTS --anteprima`. Dai il percorso dell'anteprima e di `controlli/anteprima-momenti.md` e **fermati ad aspettare l'ok**.
7. Dopo l'ok: finale, qc (CONSEGNABILE), consegna, verifica sul disco, pulizia di `.lavoro/`.

Riporta: dove sono i file, durata del girato e del video, quante papere tolte, esito del QC, la scheda da far firmare all'osteopata, le proposte che chiedono una decisione.

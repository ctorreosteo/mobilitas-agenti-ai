---
description: Monta un video da capo: dal file di camera al video pubblicabile, con Shorts, miniature e pacchetto YouTube
argument-hint: "<file in inbox/ o slug esistente> [slug]"
---

Monta il video `$ARGUMENTS` seguendo le fasi e i cancelli di `CLAUDE.md`. Carlos vedrà solo il risultato finale: decidi, verifica e documenta.

1. **Avvio.** Se l'argomento è un file: `./mve init <file> [slug]`. Se è uno slug esistente: `./mve stato <slug>` e riparti dalla prima fase non fatta.
2. **Analisi**: `./mve prep`, `./mve trascrivi` (in background), `./mve volti`. Se `volti` dice STOP, guarda i fotogrammi indicati: se è un'altra persona fermati e chiedilo a Carlos.
3. **Papere**: `./mve papere`. Poi, **nello stesso messaggio**, lancia il subagente `cacciatore-papere` e leggi tu `data/trascrizione.txt` per intero e `controlli/papere.md` (skill `mobilitas-regia`). Confronta le due liste e scrivi `tagli` e `scartati` in `regia.json`.
4. **Taglio**: `./mve edl`, `./mve audio`. Leggi `controlli/giunte.md`; ogni giunta segnalata si corregge o va in `giunte_ok` con il motivo.
5. **Regia editoriale**: scrivi in `regia.json` enfasi, card, capitoli, apertura, chip, chiusura, correzioni, shorts, miniatura, youtube. Lancia il subagente `regista` e applica gli interventi che condividi.
6. **Immagine**: `./mve grafica`, `./mve inquadra`, `./mve monta` (in background), `./mve sagome`, `./mve anteprima`. Guarda tu `controlli/anteprima.jpg` e `controlli/inquadrature.jpg` e lancia `revisore-visivo`. Correggi prima del render lungo.
7. **Master**: `./mve suono`, `./mve finale` (in background), `./mve qc`. Il QC deve dire CONSEGNABILE. Guarda `controlli/giunte.jpg`.
8. **Derivati**: `./mve shorts`, `./mve miniature`; guarda i fogli (`controlli/short*.jpg`, `controlli/miniature.jpg`, `controlli/miniatura-piccola.png`).
9. **Consegna**: `./mve consegna`, poi scrivi `videos/<slug>/BRIEF.md`: messaggio, consegne, tagli con motivo, decisioni editoriali, proposte non applicate (es. cold open), esito QC, cose da sapere.
10. **Verifica sul disco** prima di dirlo pronto: `./mve stato <slug>` tutto ✓, `ls -la` e `ffprobe` dei file consegnati.

A Carlos riporti: dove sono i file, durata sorgente → montato, quante papere tolte, esito QC, le proposte che richiedono una sua decisione.

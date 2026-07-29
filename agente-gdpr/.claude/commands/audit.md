---
description: Analizza il codice di backend e frontend e raccoglie le evidenze GDPR in report/evidenze/
argument-hint: "[area: dati|flussi|accessi|log|conservazione|diritti|sicurezza]"
---

Esegui l'audit privacy del gestionale. Segui la skill `audit-privacy-codice`.

**Precondizione**: `workspace/mobilitas-backend` e `workspace/mobilitas-frontend` esistono.
Se non ci sono, esegui prima `/sync`.

**In questa fase non si modifica nulla, nemmeno i Markdown.**

## Procedura

1. Lancia **in parallelo, nello stesso messaggio**, i subagenti `auditor-backend` e
   `auditor-frontend`. Se `$ARGUMENTS` indica un'area, restringi il perimetro a quella e dillo
   nel prompt dei subagenti.
2. Mentre girano, leggi tu la documentazione privacy esistente
   (`workspace/mobilitas-backend/docs/privacy/*.md`) per sapere cosa il gestionale **dichiara**.
3. Raccogli i risultati e scrivi i file in `report/evidenze/` (01…08 come da skill), mantenendo
   il formato `[FATTO]` / `[ASSENTE]` / `[IPOTESI]` con `file:riga`.
4. Scrivi `report/evidenze/09-riconciliazione.md`: confronto tra ciò che il codice fa e ciò che
   `02-registro-trattamenti.md` e le due DPIA dichiarano. Per ogni divergenza indica la
   conseguenza: *aggiornare il documento* oppure *aprire una criticità* (o entrambe).
5. Annota commit sha di backend e frontend in cima a `09-riconciliazione.md`: serviranno al report.

## Chiusura

Riporta all'utente:
- quante evidenze per area, quante `[ASSENTE]`, quante `[IPOTESI]`;
- le **tre divergenze più gravi** trovate;
- l'elenco delle informazioni che solo il Titolare può fornire.

Poi indica i comandi successivi: `/aggiorna-docs` e `/report`.

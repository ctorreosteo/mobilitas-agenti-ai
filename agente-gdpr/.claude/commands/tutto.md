---
description: Ciclo completo — sync, audit, aggiornamento documentazione, report criticità, revisione
---

Esegui l'intero ciclo di conformità GDPR sul gestionale, nell'ordine, senza saltare passaggi.

1. **`/sync`** — verifica i due repository sul posto, li porta sul branch
   `gdpr/aggiornamento-docs`, annota i commit sha e il branch di partenza dell'utente.
2. **`/audit`** — `auditor-backend` e `auditor-frontend` in parallelo; evidenze in
   `report/evidenze/` + riconciliazione con i documenti privacy esistenti.
3. **`/aggiorna-docs`** — allinea e mette a norma i `.md`, partendo dal registro dei trattamenti.
4. **`/report`** — scrive `report/CRITICITA-GDPR.md` con ciò che manca da implementare.
5. **Revisione** — `revisore-gdpr` su documenti e report; correggi i bloccanti e rilancia la
   verifica sui punti corretti.

## Controlli di sicurezza obbligatori

Prima di consegnare, verifica per **ogni** repository del gestionale:

```bash
git -C /Users/carlitos/mobilitas-backend diff --stat main...gdpr/aggiornamento-docs
git -C /Users/carlitos/mobilitas-backend status --short
```

Devono comparire **solo file `.md`**. Se compare qualsiasi altra estensione, è un incidente:
ripristina il file, non committare, e segnalalo in cima al riepilogo finale.

## Riepilogo finale all'utente

1. Cosa è stato analizzato (repo, commit, numero di file, aree coperte).
2. Documentazione aggiornata: tabella file → cosa è cambiato.
3. Criticità: tabella per severità + elenco sintetico di CRITICA e ALTA.
4. Domande al Titolare: elenco numerato.
5. Comandi per revisionare e pubblicare (il push lo fa l'utente). Le modifiche sono già nel suo
   repo, sul branch `gdpr/aggiornamento-docs`:
   ```bash
   cd /Users/carlitos/mobilitas-backend
   git diff main...gdpr/aggiornamento-docs -- '*.md'
   git push origin gdpr/aggiornamento-docs
   git checkout main          # per tornare al proprio lavoro
   ```
   Idem per `mobilitas-frontend`.
6. **Su quale branch era l'utente** prima di `/sync`, in ciascun repo, così può tornarci.
7. Promemoria: **nessuna riga di codice è stata modificata**.

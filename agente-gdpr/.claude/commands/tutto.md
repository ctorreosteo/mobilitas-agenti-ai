---
description: Ciclo completo — sync, audit, aggiornamento documentazione, report criticità, revisione
---

Esegui l'intero ciclo di conformità GDPR sul gestionale, nell'ordine, senza saltare passaggi.

1. **`/sync`** — recupera backend e frontend in `workspace/`, prepara il branch
   `gdpr/aggiornamento-docs`, annota i commit sha.
2. **`/audit`** — `auditor-backend` e `auditor-frontend` in parallelo; evidenze in
   `report/evidenze/` + riconciliazione con i documenti privacy esistenti.
3. **`/aggiorna-docs`** — allinea e mette a norma i `.md`, partendo dal registro dei trattamenti.
4. **`/report`** — scrive `report/CRITICITA-GDPR.md` con ciò che manca da implementare.
5. **Revisione** — `revisore-gdpr` su documenti e report; correggi i bloccanti e rilancia la
   verifica sui punti corretti.

## Controlli di sicurezza obbligatori

Prima di consegnare, verifica per **ogni** repo del workspace:

```bash
git -C workspace/<repo> diff --stat main...gdpr/aggiornamento-docs
git -C workspace/<repo> status --short
```

Devono comparire **solo file `.md`**. Se compare qualsiasi altra estensione, è un incidente:
ripristina il file, non committare, e segnalalo in cima al riepilogo finale.

## Riepilogo finale all'utente

1. Cosa è stato analizzato (repo, commit, numero di file, aree coperte).
2. Documentazione aggiornata: tabella file → cosa è cambiato.
3. Criticità: tabella per severità + elenco sintetico di CRITICA e ALTA.
4. Domande al Titolare: elenco numerato.
5. Comandi per revisionare e portare le modifiche nei repo dell'utente (il push lo fa lui):
   ```bash
   AG=/Users/carlitos/mobilitas-agenti-ai/agente-gdpr
   git -C $AG/workspace/mobilitas-backend diff --stat main...gdpr/aggiornamento-docs

   cd /Users/carlitos/mobilitas-backend
   git fetch $AG/workspace/mobilitas-backend \
       gdpr/aggiornamento-docs:gdpr/aggiornamento-docs
   git diff main..gdpr/aggiornamento-docs -- '*.md'
   git push origin gdpr/aggiornamento-docs
   ```
   Idem per `mobilitas-frontend`. Il push dalla copia di lavoro è disabilitato.
6. Promemoria: **nessuna riga di codice è stata modificata**.

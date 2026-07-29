---
description: Aggiorna e mette a norma i file Markdown della documentazione privacy del gestionale
argument-hint: "[documento o area, es. registro | dpia | informative]"
---

Allinea la documentazione Markdown del gestionale al codice e ai requisiti GDPR.
Segui la skill `aggiorna-doc-privacy`.

**Precondizione**: `report/evidenze/` popolato da `/audit`. Se è vuoto, esegui prima `/audit`:
non si scrive documentazione privacy senza evidenze.

**Si modificano solo file `.md` dentro `workspace/`, sul branch `gdpr/aggiornamento-docs`.**

## Procedura

1. Determina il perimetro. Senza `$ARGUMENTS`, lavora su tutto, in quest'ordine:
   1. `docs/privacy/02-registro-trattamenti.md` (il documento cardine)
   2. `docs/privacy/01-ruoli-e-responsabilita.md`
   3. le due DPIA (`03-*`, `04-*`)
   4. i documenti mancanti da creare (informative, breach, diritti, conservazione, misure di
      sicurezza, fornitori, amministratori di sistema) — **solo quelli che servono davvero**
   5. documentazione tecnica che contiene affermazioni errate sul trattamento dei dati
   6. hub `docs/README.md` di backend e frontend
2. Delega a `redattore-doc` un documento (o un gruppo omogeneo) per invocazione, passando le
   evidenze pertinenti. Documenti indipendenti possono essere lavorati in parallelo; il registro
   dei trattamenti va fatto **per primo**, perché gli altri vi si appoggiano.
3. Dopo ogni redazione, verifica `git status --short`: **solo `.md`**. Se compare altro,
   fermati, ripristina con `git checkout -- <file>` e segnala l'accaduto.
4. Raccogli in una lista tutte le voci `[DA VERIFICARE]` / `[DA COMPILARE]` inserite e tutte le
   criticità emerse: serviranno a `/report`.
5. Lancia `revisore-gdpr` sui documenti modificati. Correggi i **bloccanti** tramite
   `redattore-doc` prima di chiudere.
6. Committa nel workspace, per ogni repo toccato:
   ```bash
   git add -A ':(glob)**/*.md'
   git status --short
   git commit -m "docs(privacy): allineamento GDPR <AAAA-MM-GG>"
   ```
   **Nessun push.**

## Chiusura

Riporta all'utente:
- tabella dei `.md` creati/modificati con una riga di descrizione;
- numero di punti lasciati aperti `[DA VERIFICARE]` / `[DA COMPILARE]`;
- il comando per revisionare il diff:
  `git -C workspace/<repo> diff main...gdpr/aggiornamento-docs -- '*.md'`;
- promemoria: le criticità non risolvibili con la documentazione vanno in `/report`.

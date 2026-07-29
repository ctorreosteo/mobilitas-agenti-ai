---
description: Recupera backend e frontend del gestionale in workspace/ e prepara il branch di lavoro
argument-hint: "[mobilitas-backend|mobilitas-frontend]"
---

Recupera il gestionale nel workspace di lavoro.

1. Leggi `config/repos.json` per conoscere modalità (`local-git` · `remote` · `local-copy`),
   repository e branch.
2. Esegui `./scripts/sync-repos.sh $ARGUMENTS` (senza argomenti = tutti i repo).
   Se fallisce per credenziali mancanti in modalità `remote` (i repo sono privati), **non**
   aggirare il problema: riporta l'errore e proponi `"mode": "local-git"`.
   Se in `local-git` lo script segnala modifiche non committate nel repo di origine, avvisa
   l'utente che l'audit userà lo stato committato e proponi `"mode": "local-copy"`.
3. Verifica l'esito e riporta in tabella, per ogni repo:
   - branch corrente (deve essere `gdpr/aggiornamento-docs`);
   - commit HEAD (sha breve + data), da annotare per il report;
   - numero di file `.md` presenti (esclusi `node_modules`, `target`, `dist`, `.venv`);
   - `git status --short` (deve essere pulito).
4. Se una copia di lavoro contiene modifiche non committate da una sessione precedente,
   segnalale **senza** cancellarle e chiedi all'utente come procedere.

Non modificare nulla in questa fase. Al termine indica il comando successivo: `/audit`.

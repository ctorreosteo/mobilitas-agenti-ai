---
description: Verifica i repository del gestionale sul posto e li porta sul branch di lavoro
argument-hint: "[mobilitas-backend|mobilitas-frontend]"
---

Prepara i repository del gestionale. **Si lavora sui repo reali, sul posto**: nessun clone,
nessuna copia, nessun `fetch`/`pull`/`push`/`reset`.

1. Leggi `config/repos.json` per conoscere percorsi (`path`), branch base e branch di lavoro.
2. Esegui `./scripts/prepara-repos.sh $ARGUMENTS` (senza argomenti = tutti i repo).
3. Verifica l'esito e riporta in tabella, per ogni repo:
   - branch corrente (deve essere `gdpr/aggiornamento-docs`);
   - **branch di partenza dell'utente**, da ricordargli a fine sessione;
   - commit HEAD (sha breve + data), da annotare per il report;
   - numero di file `.md` presenti (esclusi `node_modules`, `target`, `dist`, `.venv`);
   - `git status --short` (deve essere pulito).
4. Lo script **si rifiuta** di operare su un repo con modifiche non committate: non le tocca
   mai. Se succede, mostra all'utente l'elenco dei file pendenti e chiedi come procedere.
   **Non eseguire mai** `stash`, `reset` o `checkout -f` per sbloccare la situazione: sono
   modifiche sue, non tue, e l'hook te lo impedisce comunque.
5. Se lo script segnala `🚨 INCIDENTE` (il branch di lavoro modifica file non Markdown),
   **fermati**: riporta i file in cima alla risposta e non procedere con `/audit`.

Non modificare nulla in questa fase. Al termine indica il comando successivo: `/audit`.

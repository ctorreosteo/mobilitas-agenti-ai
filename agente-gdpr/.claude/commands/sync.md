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
4. Lo script **si rifiuta** di sincronizzare una copia di lavoro con modifiche non committate:
   non le cancella mai. Se succede, mostra all'utente l'elenco dei file pendenti e chiedi se
   committarli sul branch di documentazione o scartarli; non decidere al posto suo.
5. Se lo script segnala `🚨 INCIDENTE` (il branch di lavoro modifica file non Markdown),
   **fermati**: riporta i file in cima alla risposta e non procedere con `/audit`.
6. Se segnala che il branch di lavoro è indietro rispetto a `main`, riferiscilo: contiene lavoro
   di una sessione precedente e va deciso se ribasarlo prima di continuare.

Non modificare nulla in questa fase. Al termine indica il comando successivo: `/audit`.

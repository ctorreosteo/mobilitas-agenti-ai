# Agente dev rapido

La versione minima di `mobilitas-agente-dev-hq`: legge il task da ClickUp, lo implementa su frontend e backend, fa il commit. Niente piano, revisori, report o deploy.

```bash
cd /Users/carlitos/mobilitas-agenti-ai/mobilitas-agente-dev-rapido
claude
```

> Vai

oppure

> Lavora il task 869xxxxxx

Senza id prende i task con scadenza oggi, poi gli scaduti dal più vecchio.

Commit: `<Titolo breve> (CU-<task_id>)`, solo i file toccati dall'agente, mai push. A fine task lo sposta a `review` su ClickUp.

Tutte le istruzioni sono in [CLAUDE.md](CLAUDE.md).

# Agente dev rapido

La versione minima di `mobilitas-agente-dev-hq`: legge il task dalla lista HQ del gestionale, lo implementa su frontend e backend, fa il commit. Niente piano, revisori, report o deploy.

```bash
cd /Users/carlitos/mobilitas-agenti-ai/mobilitas-agente-dev-rapido
claude
```

> Vai

oppure

> Lavora il task 1234

Senza id prende i task con scadenza oggi, poi gli scaduti dal più vecchio.

Commit: `<Titolo breve> (HQ-<task_id>)`, solo i file toccati dall'agente, mai push. A fine task lo sposta a `In attesa` nel gestionale.

Serve un utente del gestionale che veda la lista HQ con livello almeno *Modifica*, con le credenziali in `~/.config/mobilitas-agente-dev/credenziali` (`HQ_USERNAME=`, `HQ_PASSWORD=`, `chmod 600`).

Tutte le istruzioni sono in [CLAUDE.md](CLAUDE.md).

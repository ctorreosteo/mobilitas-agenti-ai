# Agente dev rapido — sito web

Come `mobilitas-agente-dev-hq`, ma per il sito pubblico: legge il task dalla lista **Dev - sito web** del gestionale, lo implementa in `mobilitas-sito-web`, aggiorna la documentazione, fa il commit. Niente piano, revisori o report.

```bash
cd /Users/carlitos/mobilitas-agenti-ai/mobilitas-agente-dev-sito
claude
```

> Vai

oppure

> Lavora il task 1234

Senza id prende tutti i task aperti con scadenza fino a oggi: quelli di oggi e, insieme, gli scaduti non ancora fatti (dal più vecchio). All'avvio mostra l'elenco dei task che lavorerà, e a ogni cambio annuncia quello in corso (`Task 2/5 — 1234: …`).

Documentazione: a ogni task allinea la documentazione del sito, nello stesso commit del codice, e alla fine dice cosa ha aggiornato o perché non serviva.

Commit: `<task_id> - <spiegazione>`, solo i file toccati dall'agente, sempre nel repo di riferimento. Push e deploy li fa Carlos a mano. A fine task lo sposta a `In attesa` nel gestionale.

**Non può modificare il gestionale**, ed è bloccato anche nei permessi: un task che lo richiede viene saltato e segnalato. Dal gestionale cambia solo lo stato del proprio task.

Serve un utente del gestionale che veda la lista con livello almeno *Modifica*, con le credenziali in `~/.config/mobilitas-agente-dev/credenziali` (`HQ_USERNAME=`, `HQ_PASSWORD=`, `chmod 600`).

Tutte le istruzioni sono in [CLAUDE.md](CLAUDE.md).

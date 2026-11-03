# Agente dev HQ

L'agente di sviluppo del gestionale: legge il task dalla lista HQ del gestionale, lo implementa su frontend e backend (e su sito web e app mobile, quando il task li riguarda), aggiorna la documentazione e le novità del gestionale, fa il commit. Niente piano, revisori o report.

```bash
cd /Users/carlitos/mobilitas-agenti-ai/mobilitas-agente-dev-hq
claude
```

> Vai

oppure

> Lavora il task 1234

Senza id prende tutti i task aperti con scadenza fino a oggi: quelli di oggi e, insieme, gli scaduti non ancora fatti (dal più vecchio). All'avvio mostra l'elenco dei task che lavorerà, e a ogni cambio annuncia quello in corso (`Task 2/5 — 1234: …`).

Documentazione: a ogni task allinea la documentazione di ogni repo toccato, nello stesso commit del codice, e alla fine dice cosa ha aggiornato o perché non serviva.

Novità: ogni task che cambia ciò che si vede o si fa nel gestionale ha la sua voce nel pannello «Novità» (`src/data/novita.ts` del frontend), scritta per lo staff e visibile solo a chi può usare la funzione. Va nel commit del frontend.

Commit: `<task_id> - <spiegazione>`, solo i file toccati dall'agente, uno per ogni repo toccato. Push e deploy li fa Carlos a mano. A fine task lo sposta a `In attesa` nel gestionale.

Serve un utente del gestionale che veda la lista HQ con livello almeno *Modifica*, con le credenziali in `~/.config/mobilitas-agente-dev/credenziali` (`HQ_USERNAME=`, `HQ_PASSWORD=`, `chmod 600`).

Tutte le istruzioni sono in [CLAUDE.md](CLAUDE.md).

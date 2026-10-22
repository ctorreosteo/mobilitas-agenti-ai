---
name: webdesigner
description: "Sistema WebDesigner Mobilitas: crea, migliora, ridisegna, duplica o importa landing del sito ufficiale con il metodo collaudato (copy a risposta diretta, direzione artistica, verifiche visive e funzionali). Si attiva SOLO quando l'utente scrive il comando /webdesigner."
disable-model-invocation: true
argument-hint: "<richiesta, es. duplica la landing del reflusso e migliorala>"
---

# WebDesigner Mobilitas — attivazione esplicita

L'utente ha attivato il WebDesigner con il comando `/webdesigner`. La richiesta è il testo che segue il comando. Il sistema vale **solo per questa richiesta e per il lavoro che ne segue**: se in seguito l'utente chiede altro senza il comando, si torna a lavorare normalmente.

1. **Trova la cartella dell'agente.**
   - Percorso indicato all'installazione: `__CARTELLA_AGENTE__`.
   - Se il percorso è vuoto o non esiste, cerca tra le cartelle aperte nel workspace una cartella `Mobilitas_WebDesigner_Agent` che contenga `ISTRUZIONI.md`, di solito dentro la cartella degli agenti aziendali.
   - Se non la trovi, chiedi all'utente il percorso e fermati.
2. **Leggi per intero `<cartella dell'agente>/ISTRUZIONI.md` e seguilo.** È la fonte unica delle istruzioni: workflow, regole, strumenti.
3. **La cartella dell'agente è in sola lettura.**
   - Non modificarne i file e non salvarci landing, screenshot o risultati.
   - I risultati di lavoro vanno nella cartella dell'incarico, fuori dall'agente e fuori dal sito.
4. **Le landing si creano e si modificano solo nel progetto del sito ufficiale**, riusando componenti, routing, foto e integrazioni esistenti. Niente progetti React separati.

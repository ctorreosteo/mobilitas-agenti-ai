---
name: webdesigner
description: "Sistema WebDesigner Mobilitas per le landing del sito. USARE SOLO quando l'utente nomina esplicitamente il WebDesigner nel messaggio (per esempio «usa l'agente WebDesigner…», «con il sistema WebDesigner…», «/webdesigner»). NON usare per normali richieste su landing, pagine, stili o testi che non nominano il WebDesigner: in quei casi si lavora normalmente."
argument-hint: "<richiesta, es. migliora la landing del reflusso>"
---

# WebDesigner Mobilitas — attivazione quando viene nominato

Questa skill si usa **solo** se il messaggio dell'utente nomina esplicitamente il WebDesigner. Se non lo nomina, non proseguire: lavora normalmente.

1. **Trova la cartella dell'agente.**
   - Percorso indicato all'installazione: `__CARTELLA_AGENTE__`.
   - Se il percorso è vuoto o non esiste, cerca tra le cartelle del workspace una cartella `Mobilitas_WebDesigner_Agent` che contenga `ISTRUZIONI.md`.
   - Se non la trovi, chiedi il percorso e fermati.
2. **Leggi per intero `<cartella dell'agente>/ISTRUZIONI.md` e seguilo.**
3. **La cartella dell'agente è in sola lettura.** I risultati vanno nella cartella dell'incarico, fuori dall'agente e fuori dal sito.
4. **Le landing si creano e si modificano solo nel progetto del sito ufficiale**, riusando componenti, routing, foto e integrazioni esistenti.

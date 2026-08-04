# Scheda Operativa da Stanza — l'estratto che l'osteopata usa davvero

## Il problema che risolve

Una procedura da 6.000 parole è perfetta per studiare la sera. È **inutilizzabile durante la seduta**. L'osteopata ha le mani sul paziente e trenta secondi per ricordarsi il red flag, il test giusto e la sequenza. La Scheda Operativa è **una pagina**, la stessa struttura per ogni condizione, che vive plastificata sul lettino o come card sul tablet.

Ogni procedura completa genera **sempre** la sua Scheda Operativa. Non è opzionale: è il pezzo che rende la procedura usata invece che archiviata.

## Formato: una pagina, sei blocchi, sempre uguali

La forza è la **costanza**: l'osteopata sa esattamente dove guardare perché la scheda del reflusso ha la stessa mappa visiva di quella del ginocchio.

```
┌─────────────────────────────────────────────┐
│  [CONDIZIONE]           Scheda Operativa      │
│  Ancora: [Nome] · Scala: [NDI/ODI/VISA-A…]    │
├─────────────────────────────────────────────┤
│  1. RED FLAGS — STOP E INVIO                   │
│     • [segnale] → [specialista]                │
│     • [segnale] → [specialista]                │
├─────────────────────────────────────────────┤
│  2. È TRATTABILE SE… (criteri inclusione)      │
│     • [criterio 1]  • [criterio 2]  • …        │
├─────────────────────────────────────────────┤
│  3. TEST IN STANZA (0-10 prima/dopo)           │
│     1. [test] — [cosa cerchi]                  │
│     2. [test] — [cosa cerchi]                  │
│     3. [test] — [cosa cerchi]                  │
├─────────────────────────────────────────────┤
│  4. SEQUENZA DI TRATTAMENTO                     │
│     A [blocco] → B [blocco] → C [blocco]       │
│     (periferia → centro)                       │
├─────────────────────────────────────────────┤
│  5. ESERCIZI A CASA (con dose)                 │
│     • [esercizio] — [durata] × [frequenza]     │
│     • [esercizio] — [durata] × [frequenza]     │
├─────────────────────────────────────────────┤
│  6. COSA DIRE AL PAZIENTE (1 frase)            │
│     "[metafora + cosa faccio io]"              │
└─────────────────────────────────────────────┘
```

## Regole di compilazione

- **Ogni blocco è estratto dalla procedura completa, mai reinventato.** La scheda non aggiunge contenuto: lo comprime. Se un blocco è vuoto sulla scheda, manca nella procedura → torna e correggi la procedura.
- **Red flags in cima, sempre.** È il blocco per cui la scheda esiste: è quello che salva il paziente e lo studio. Va letto in mezzo secondo.
- **Se la procedura usa manovre a rischio, la scheda porta anche la sicurezza del gesto — non solo i red flag diagnostici.** Aggiungi, compatti, due presidi accanto ai red flag: (a) un rigo **"prima di toccare"** con il consenso al trattamento manuale + dati di salute (GDPR); (b) un blocco **"controindicazioni alle tecniche"** con lo screening pre-manovra chiave (es. addome profondo → AAA/anticoagulanti/gravidanza; dorso in estensione → osteoporosi; **cervicale alta → screening vascolare/neuro VBI**) e la **stop-rule intra-seduta con escalation 112**. È l'estratto del blocco "Controindicazioni e cautele" della procedura: la scheda non lo inventa, lo comprime.
- **Test con la scala 0-10** perché il valore prima/dopo è il dato che l'osteopata segna in cartella e mostra al paziente.
- **Esercizi con dose obbligatoria.** Mai "stretching cervicale": sempre "stretching sub-occipitali — 30 sec × 3, 2 volte al giorno". Questo si aggancia direttamente all'audit delle cartelle (vedi `integrazione-gestionale.md`): un esercizio senza durata e frequenza viene segnalato.
- **La frase al paziente è quella dello Script**, ridotta a una riga. Deve poter essere detta ad alta voce senza leggere.
- **Il modello dominante ipotizzato va scritto e ri-verificato.** Nel blocco 4 aggiungi un rigo "Modello dominante di questo paziente: ___" (è l'output del Motore Clinico: su quale modello agisci per primo) e la regola "se non risponde entro 3 sedute → ripesa il dominante". È ciò che porta la decisione clinica in stanza e in cartella, non solo un protocollo.
- **Massimo una pagina A4.** Se non ci sta, hai messo troppo. La scheda è un promemoria, non un riassunto.

## Produzione

La scheda si scrive come **secondo file markdown** (`scheda-<condizione>.md`) e si converte con lo stesso `build_docx.py`. Nome file di output: `Scheda_Operativa_<Condizione>.docx`. Va presentata **insieme** alla procedura completa: sono una coppia, non due consegne separate.

# Sistema-Libreria — da documenti sparsi a corpus coerente

Una procedura è utile. Venti procedure incoerenti sono un problema: se la procedura cervicale dice una cosa sui sub-occipitali e quella cefalea ne dice un'altra, l'osteopata non sa a chi credere e smette di fidarsi di tutte. L'obiettivo è un **corpus** dove ogni documento parla la stessa lingua e rimanda agli altri.

## 1. Nomenclatura e versioning

- File procedura: `Procedura_<Condizione>.docx` · Scheda: `Scheda_Operativa_<Condizione>.docx`.
- Ogni documento porta in intestazione: **condizione, ancora scientifica, data, versione** (v1.0, v1.1…).
- Quando una procedura si aggiorna (nuovo studio, tecnica rivista), sale la versione e si aggiorna la data. Le procedure cliniche invecchiano: una del 2024 senza il RESTORE 2023 è già vecchia.

## 2. L'indice maestro

Esiste un unico documento **Indice delle Procedure Mobilitas** che elenca tutte le condizioni coperte, con: ancora scientifica, scala di monitoraggio usata, data ultima revisione, e le condizioni correlate. È la mappa che il direttore usa per vedere cosa manca e cosa va aggiornato.

Quando crei una nuova procedura, **aggiorna l'indice** (o segnala a Carlos che va aggiornato). Una libreria senza indice è un cassetto.

## 3. Mappa delle comorbidità — il cross-referencing

I pazienti non arrivano con una diagnosi pulita. Chi ha cervicalgia spesso ha cefalea; chi ha lombalgia ha spesso problemi di anca o di appoggio; chi ha ATM ha spesso acufene e cervicale. Ogni procedura deve avere, in chiusura di Parte II, un rimando esplicito:

> **Condizioni spesso associate:** se il paziente presenta anche [X], vedi la Procedura [X]. I due quadri condividono [struttura/meccanismo comune] e vanno trattati insieme.

Coppie note da collegare sempre:
- Cervicalgia ↔ Cefalea cervicogenica ↔ Emicrania ↔ Acufene (asse cervico-cranico e DCN)
- Lombalgia ↔ Pubalgia ↔ Anca ↔ Appoggio podalico (catena inferiore)
- ATM ↔ Acufene ↔ Cervicale ↔ Cefalea (asse stomatognatico-cranico)
- Reflusso ↔ Dorsalgia ↔ Diaframma ↔ Ansia (asse viscero-emozionale)
- Vertigini ↔ Cervicale ↔ Cefalea (asse vestibolo-cervicale)

Questo è anche il meccanismo unico Mobilitas reso operativo: **il dolore non dipende dal punto che fa male**, e la libreria lo dimostra rimandando da una condizione all'altra.

## 4. Componenti condivisi — coerenza tra procedure

Alcuni elementi ricorrono in più procedure. Devono essere **identici** ovunque, non riscritti ogni volta con parole diverse:

- **Descrizione delle tecniche cardine** (inibizione sub-occipitali, release stretto toracico, pompaggio seni durali, tecniche diaframmatiche): stessa definizione, stesso nome, in ogni procedura che le usa.
- **Meccanismi trasversali** (sensibilizzazione centrale, asse HPA, gradiente pressorio toraco-cranico): stessa spiegazione di base, adattata alla condizione.
- **Struttura della Scheda Operativa**: identica al pixel.
- **Sezione red flags**: stesso registro, stesso livello di dettaglio.

Se una tecnica va spiegata diversamente in due procedure, o è un errore, o le due procedure hanno ragioni cliniche diverse — e in quel caso la differenza va **dichiarata**, non lasciata implicita.

## 5. Coerenza della voce

Tutte le procedure sono scritte dallo **stesso direttore**. Non devono suonare come autori diversi. Il DNA editoriale (`dna-editoriale.md`) è ciò che garantisce questo: rileggi sempre una procedura chiedendoti "suona come l'acufeni?". Se no, non è pronta.

## 6. La regola d'oro della libreria

> Ogni nuova procedura deve **rafforzare** le altre, non contraddirle. Prima di consegnare, chiediti: un osteopata che ha letto la procedura cervicale e poi legge questa, trova coerenza o confusione?

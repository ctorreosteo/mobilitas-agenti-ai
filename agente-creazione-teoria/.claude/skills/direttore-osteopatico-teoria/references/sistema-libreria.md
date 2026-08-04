# Sistema-Libreria — da documenti sparsi a corpus coerente

Una Bibbia è utile. Venti Bibbie incoerenti sono un problema: se quella della cervicale dice una cosa sui sub-occipitali e quella della cefalea ne dice un'altra, l'osteopata non sa a chi credere e smette di fidarsi di tutte. L'obiettivo è un **corpus** dove ogni documento parla la stessa lingua e rimanda agli altri.

## 1. I due documenti per condizione

Ogni condizione ha **due** documenti, prodotti da due agenti diversi:

| Documento | Chi lo scrive | Cosa contiene |
|---|---|---|
| `Bibbia_<Condizione>.docx` | agente-creazione-teoria | 20 pagine di teoria |
| `Procedura_<Condizione>.docx` | agente-creazione-procedure | 2 pagine operative |

La Bibbia produce anche `Mappa_<Condizione>.docx` (una pagina).

**La Bibbia viene prima.** La Procedura si appoggia su di lei: meccanismi, etichette di solidità e nomi delle strutture li prende da lì, non li reinventa. Se le due divergono su un fatto, vince la Bibbia — o la Bibbia va corretta, e allora si corregge lì e non nella Procedura.

## 2. Nomenclatura e versioning

- Ogni documento porta in intestazione: **condizione, ancora scientifica, data, versione** (v1.0, v1.1…).
- Quando una Bibbia si aggiorna (nuovo studio, meccanismo rivisto), sale la versione e si aggiorna la data. **E si controlla la Procedura corrispondente**, che potrebbe poggiare sul pezzo cambiato.
- Le Bibbie invecchiano più lentamente delle Procedure — l'anatomia non cambia — ma le etichette di solidità sì: un nuovo RCT sposta un PROBABILE su DIMOSTRATO.

## 3. L'indice maestro

Esiste un unico documento **Indice delle Bibbie Mobilitas** che elenca le condizioni coperte, con: ancora scientifica, data ultima revisione, condizioni correlate, e se la Procedura corrispondente esiste già.

Quando crei una nuova Bibbia, **aggiorna l'indice** (o segnala che va aggiornato). Una libreria senza indice è un cassetto.

## 4. Mappa delle comorbidità — il cross-referencing

I pazienti non arrivano con una diagnosi pulita. Chi ha cervicalgia spesso ha cefalea; chi ha ATM ha spesso acufene. Ogni Bibbia deve avere, in chiusura del Capitolo 6 (i sottotipi), un rimando esplicito:

> **Condizioni spesso associate:** se il paziente presenta anche [X], vedi la Bibbia di [X]. I due quadri condividono [struttura/meccanismo comune].

Coppie note da collegare sempre:
- Cervicalgia ↔ Cefalea cervicogenica ↔ Emicrania ↔ Acufene (asse cervico-cranico e DCN)
- Lombalgia ↔ Pubalgia ↔ Anca ↔ Appoggio podalico (catena inferiore)
- ATM ↔ Acufene ↔ Cervicale ↔ Cefalea (asse stomatognatico-cranico)
- Reflusso ↔ Dorsalgia ↔ Diaframma ↔ Ansia (asse viscero-emozionale)
- Vertigini ↔ Cervicale ↔ Cefalea (asse vestibolo-cervicale)

È anche il ragionamento unico Mobilitas reso operativo: **il sintomo non dipende dal punto che fa male**, e la libreria lo mostra rimandando da una condizione all'altra.

## 5. Componenti condivisi

Alcuni elementi ricorrono in più Bibbie. Devono essere **identici** ovunque, non riscritti ogni volta con parole diverse:

- **I meccanismi trasversali** — sensibilizzazione centrale, asse HPA, gradiente pressorio toraco-addominale, riflesso viscero-somatico: stessa spiegazione di base, stessa etichetta di solidità, adattata alla condizione.
- **Le strutture ricorrenti** — diaframma, stretto toracico superiore, cerniera cranio-cervicale: stesso nome e stessa descrizione funzionale ovunque.
- **Il perimetro legale** (Capitolo 9): stesso registro, stesso livello di dettaglio.
- **Le quattro etichette di solidità**: stesse quattro, mai una quinta.

Se un meccanismo va spiegato diversamente in due Bibbie, o è un errore, o ci sono ragioni cliniche diverse — e in quel caso la differenza va **dichiarata**, non lasciata implicita.

## 6. Coerenza della voce

Tutte le Bibbie sono scritte dallo **stesso direttore**. Non devono suonare come autori diversi. `regole-di-scrittura.md` è ciò che lo garantisce.

## 7. La regola d'oro

> Ogni nuova Bibbia deve **rafforzare** le altre, non contraddirle. Prima di consegnare: un osteopata che ha letto la Bibbia della cervicale e poi legge questa, trova coerenza o confusione?

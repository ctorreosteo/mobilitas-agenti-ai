# Teoria — Skill Direttore Osteopatico (Mobilitas / OsteoTouch)

Cartella di lavoro per la redazione e revisione delle **Bibbie teoriche** delle condizioni
trattate in studio.

## Cos'è una Bibbia

Venti pagine con **tutto quello che un osteopata deve sapere su una condizione per poterla
risolvere in poche sedute**. Cos'è, perché succede, quali meccanismi la tengono in piedi,
quanto è solido ciò che affermiamo, dove finisce il nostro campo, perché le mani possono
cambiare qualcosa.

**Non è una procedura operativa.** Tecniche, dosi da somministrare, sequenze e piano delle sedute
stanno in un documento separato di due pagine, prodotto da `agente-creazione-procedure`.

| La Bibbia (qui, ~20 pagine) | La Procedura (altro agente, 2 pagine) |
|---|---|
| Che cos'è, perché succede | Cosa fai alla prima seduta |
| Quali meccanismi la tengono in piedi | Quali tecniche, in che ordine |
| Come si riconosce il sottotipo | Quanti minuti per blocco |
| Perché le mani possono agire | Quali tecniche, con che dose |
| Perché un esercizio funziona, e cosa hanno misurato gli studi | Quale esercizio dai a *questo* paziente, e quando |
| Quanto è solido tutto questo | Come misuri e quando rivaluti |

Ogni Bibbia produce anche una **Mappa concettuale di sintesi**: una pagina, sei blocchi, quella
a cui si torna sei mesi dopo.

## Struttura

```
.claude/skills/                     skill di progetto (attive lavorando in questa cartella)
  direttore-osteopatico-teoria/     AUTORE — redige la Bibbia + la Mappa concettuale
    ├─ SKILL.md
    ├─ references/
    │   ├─ architettura-bibbia.md      i 15 capitoli e le 5 regole di struttura
    │   ├─ regole-di-scrittura.md      come si scrive (la leggibilità è un requisito)
    │   ├─ cinque-modelli-osteopatici.md  impalcatura del Capitolo 7
    │   ├─ motore-clinico.md           il ragionamento del Capitolo 8
    │   ├─ ancore-scientifiche.md      metodo di ricerca e verifica
    │   ├─ ancore-verificate.md        ancore già validate (cervicale, lombalgia, Achille)
    │   ├─ mappa-concettuale.md        spec del secondo deliverable
    │   ├─ sistema-libreria.md         coerenza del corpus
    │   ├─ revisione-e-sintesi.md      i sei livelli e la regola di triage
    │   ├─ rubrica-punteggio.md        cancello: sotto 90/100 non si consegna
    │   └─ checklist-qualita.md        cancello: un solo NO = si corregge
    └─ scripts/
        ├─ build_docx.py
        └─ verifica_conservazione.py   collaudo deterministico v5 vs v7

  direttore-osteopatico-specialista/       1º liv. — medico specialista di riferimento
  direttore-osteopatico-medico-generale/   1º liv. — MMG che invia i pazienti
  direttore-osteopatico-sicurezza-tecniche/ 1º liv. — dove la teoria porta a far male
  direttore-osteopatico-fisioterapista-ebp/ 1º liv. — scettico evidence-based
  direttore-osteopatico-compliance/        1º liv. — legale / deontologia / GDPR
  direttore-osteopatico-neolaureato/       1º liv. — comprensibilità alla prima lettura
  direttore-osteopatico-sistema-dominante/ 1º liv. — il ragionamento del Motore Clinico
  direttore-osteopatico-modelli/           1º liv. — uso e bilanciamento dei cinque modelli
  direttore-osteopatico-neuromodulazione/  1º liv. — il meccanismo neurofisiologico
  direttore-osteopatico-clinico-esperto/   1º liv. — "il paziente guarisce davvero?"
  direttore-osteopatico-strumenti-attivi/  1º liv. — respirazione, rinforzo, carico, educazione
  direttore-osteopatico-fedelta-bibbia/    2º liv. — audit contro l'architettura
  direttore-osteopatico-evidenza-estesa/   2º liv. — il Ricercatore: i tre cerchi dell'evidenza
  direttore-osteopatico-apprendimento/     3º liv. — il documento insegna o fa solo sapere?
  direttore-osteopatico-coerenza/          3º liv. — le nove giunture: il documento si contraddice?
  direttore-osteopatico-editor/            4º liv. — asciugatura
  direttore-osteopatico-chiarezza/         5º liv. — RISCRIVE tutto in linguaggio semplice
  direttore-osteopatico-italiano/          6º liv. — CORREGGE la lingua + metafore di servizio
  direttore-osteopatico-collaudo/          CANCELLO — conservazione v5→v7, script + semantica

bibbie-generate/
  _dati/livelli.json                manifesto: chi è autore e chi revisore, per livello
  _dati/problemi.json               materia prima (sintomi, obiezioni, red flag)
  _dati/deviazioni-dal-metodo.md    dove il metodo interno è stato trovato sbagliato
  _dati/registro-lingua.md          calchi ricorrenti e passaggi che restano oscuri
  _workflow/genera-bibbie.workflow.js
  <slug>/                           lavorazione in markdown, v1 → v7

outputs/<slug>/                     Bibbia_<Condizione>.docx + Mappa_<Condizione>.docx
```

## L'architettura della Bibbia — i 15 capitoli

| # | Capitolo | Cosa contiene |
|---|---|---|
| 0 | Come si usa questa Bibbia | Orientamento, etichette, "Buon nutrimento!" |
| 1 | Chi ti trova davanti | Il paziente reale, dai dati di `problemi.json` |
| 2 | Che cos'è davvero | Definizione, diffusione, storia naturale |
| 3 | Le strutture in gioco | Solo l'anatomia che conta, più una chicca |
| 4 | Come funziona quando funziona | Fisiologia normale |
| 5 | Cosa si rompe | **Il cuore.** 3-6 meccanismi, dal più solido al meno |
| 6 | Non è una condizione sola | I sottotipi come pattern |
| 7 | La lettura osteopatica | I cinque modelli, una sezione breve ciascuno |
| 8 | Come ragiono davanti a questo paziente | Il Motore Clinico |
| 9 | Dove finisce il nostro campo | Bandiere rosse, cancello, farmaci, perimetro legale |
| 10 | Cosa dice la scienza | I tre cerchi, studi verificati, cosa si può dire e cosa no, **«Quando la scienza tace»** |
| 11 | Perché le mani possono cambiare qualcosa | Razionale delle leve. **Niente protocolli** |
| 12 | Cosa può fare il paziente da solo | **CONDIZIONALE** — c'è solo se uno strumento attivo regge DIMOSTRATO o PROBABILE forte |
| 13 | Cosa dire al paziente | Script sotto 100 parole, risposte alle obiezioni |
| 14 | Cosa fare adesso | Il filo ricucito, le tre cose che cambi da lunedì, la chiusura che spinge |
| A | Glossario | Ogni termine tecnico, una riga |
| B | Le fonti | Bibliografia con link verificati |

**Lunghezza: 8.000–13.000 parole**, appendici escluse.

### Le tre regole che governano il contenuto scientifico

1. **I tre cerchi.** L'evidenza si cerca su tre livelli: *specifico* (quell'intervento su questa condizione), *trasversale* (tocco e terapia manuale sul meccanismo condiviso — regolazione autonomica, modulazione del dolore, interocezione, respiro, contesto), *fisiologico*. Cercare solo il primo produce Bibbie povere sulle condizioni poco studiate, che sono quasi tutte.

2. **La regola del ponte.** L'evidenza trasversale alza l'etichetta del **meccanismo**, mai quella della **leva** su questa condizione, e ogni fonte porta la frase che dichiara il salto. È il lucchetto che impedisce al primo punto di degenerare in *mechanism-mongering*.

3. **Il parametro di uno studio è un dato, non una prescrizione.** *"Nello studio hanno allenato per otto settimane"* sta nella Bibbia; *"fai fare otto settimane al paziente"* sta nella Procedura. Il criterio è il tempo verbale e il destinatario. Senza questa eccezione il confine espelleva dalla teoria proprio la leva con la migliore evidenza al mondo.

### Le cinque regole di struttura

Sono la parte che il vecchio impianto delle procedure sbagliava, e valgono in ogni capitolo.

1. **Un capitolo = una domanda.** Titoli in italiano corrente, mai "Parte III — Fisiopatologia". I capitoli si citano per nome, mai per numero.
2. **Apertura e chiusura fisse.** Ogni capitolo apre con `> **In una riga:**` (la tesi) e chiude con **Le tre cose da ricordare** (esattamente tre).
3. **L'incertezza esce dal testo.** La prosa afferma; l'onestà la porta un box separato `> **Quanto è solido:**` con una di quattro etichette — DIMOSTRATO / PROBABILE / IPOTESI / RAGIONAMENTO. È la cura del difetto capitale dei vecchi documenti: periodi in cui claim, qualificazione, citazione e istruzione stavano tutti insieme.
4. **Quattro soli tipi di box:** Definizione · Quanto è solido · Attenzione · Cosa cambia per te.
5. **Tabelle: massimo 4 colonne, massimo 8 parole per cella.** Se non ci sta, è prosa.

## Pipeline editoriale — sei livelli

Ruoli e livelli sono dichiarati in `bibbie-generate/_dati/livelli.json`: è l'unico file da
toccare per aggiungere, togliere o spostare un revisore.

1. **`teoria`** redige la v1 (Bibbia + Mappa).
2. **1º livello** — panel avversariale in parallelo sul contenuto (undici lenti) → **v2**.
3. **2º livello** — `fedelta-bibbia` (audit contro l'architettura) ed `evidenza-estesa`
   (il Ricercatore: allarga la base scientifica ai tre cerchi) → **v3**.
4. **3º livello** — `apprendimento` (il documento insegna o fa solo sapere?) e `coerenza`
   (l'ispettore delle giunture: due capitoli alla volta, si contraddicono?) → **v4**.
5. **4º livello** — `editor`: toglie ridondanza, riporta nel range → **v5**.
6. **5º livello** — `chiarezza`: **riscrive l'intero documento da capo** con lessico e sintassi
   semplici, senza perdere una sola informazione → **v6**.
7. **6º livello** — `italiano`: **corregge la lingua** frase per frase — calchi dall'inglese,
   nessi logici, pronomi vaghi, collocazioni — e inserisce le **metafore di servizio** → **v7**.
8. **Cancello** — `collaudo`: verifica che le due riscritture non abbiano perso niente →
   **v7 consegnabile**.

Gli ultimi due livelli non consigliano: producono il deliverable.

L'ordine non è invertibile, in nessuno dei due passaggi. **Si semplifica un testo già asciutto**
(4º→5º): l'asciugatura ri-comprimerebbe le frasi e annullerebbe il lavoro. E **si raddrizza la
lingua di un testo già semplificato** (5º→6º): una riscrittura integrale dopo la revisione di
lingua reintrodurrebbe i calchi appena tolti.

Analogamente, l'apprendimento sta **prima** dell'editor apposta: può chiedere qualche riga in
più, e l'editor asciuga il risultato.

### Perché esiste il sesto livello

Il difetto che sopravviveva a tutta la catena era **l'italiano**. Nessun revisore aveva la lingua
come mandato: il quinto livello accorcia le frasi e semplifica il lessico, ma una frase corta può
essere un calco perfetto dall'inglese; il neolaureato segnala che non capisce, ma non sa dire
perché.

Il risultato era un documento giusto, semplice e scritto in un italiano che nessun madrelingua
scriverebbe — periodi senza sintassi logica, pronomi appesi a una frase intera, nessi mancanti o
sbagliati. La divisione fra i due livelli è netta: **il quinto lavora sulla complessità, il sesto
sulla naturalezza.** Sono due difetti diversi, e risolverli nello stesso passaggio significa
risolverne male uno.

Il sesto livello **non riscrive**: passa frase per frase e corregge solo quelle che hanno un
difetto, entro un delta di lunghezza fra −3% e +5%. Se tocca più del 40% delle frasi, il workflow
lo segnala: o il quinto ha lavorato male, o il sesto ha riscritto.

### Le metafore di servizio

È l'unica cosa che il sesto livello ha licenza di **aggiungere**, e serve per i concetti che
restano difficili anche dopo la semplificazione — non perché scritti male, ma perché **astratti**:
il lettore non ha niente nella sua esperienza a cui agganciarli.

Da sei a otto in tutto il documento, massimo una per capitolo, sotto le venti parole, prese dalla
vita di tutti i giorni — la macchina, la casa, il lavoro, la cucina, il denaro. Sempre **dopo**
l'affermazione, mai prima: un'immagine senza il concetto davanti è un indovinello. **Mai** su una
bandiera rossa, su un criterio di invio o dentro un box di solidità, perché un'immagine ammorbidisce
un avvertimento.

La regola che le rende sicure per il collaudo, ed è anche il test di qualità:

> **Se togliendo la metafora si perde un'informazione, non era una metafora: era contenuto nuovo,
> e va tolta.**

Non vanno confuse con le **metafore d'ancoraggio** del capitolo sui meccanismi — una per meccanismo,
in grassetto, isolate su una riga, scelte dall'autore: quelle sono il cuore mnemonico del documento,
e il sesto livello non le tocca.

### Il cancello di conservazione

Fra il quinto e il sesto livello **ogni singola frase del documento cambia** — ed era il tratto
che nessuno verificava: il documento consegnato era l'unica versione mai controllata.

`collaudo` chiude quel buco. **Non è un settimo revisore** e non giudica la qualità, chiusa a
monte: confronta la **v5** con la **v7** e verifica la sola **conservazione**. Il confronto è con
la v5, non con la v6, perché la v5 è l'ultima versione con il contenuto approvato: così le due
riscritture si collaudano insieme.

Lo script deterministico (`verifica_conservazione.py`) gira **due volte, una per passaggio**:

| Passaggio | Delta ammesso | Identità minima |
|---|---|---|
| v5 → v6 (chiarezza) | −5% / +10% | nessuna: ogni frase deve cambiare |
| v6 → v7 (lingua) | −3% / +5% | **60% delle frasi identiche** |

Misurare due riscritture in blocco le lascia compensare: se la prima perde e la seconda aggiunge,
i conti tornano e la perdita non si vede. E la **soglia di identità** rende verificabile la regola
più importante del sesto livello — *correggi, non riscrivere*. Prima era l'agente a dichiarare
quante frasi aveva toccato, cioè un controllo che non controllava niente. Ora lo conta il codice,
e sotto il 60% è bloccante come alzare un'etichetta.

La **lettura semantica** si fa invece sull'intera catena, dalla v5 al documento finale: è lì che
l'inventario delle informazioni si conserva o si perde. Cerca ciò che nessun conteggio vede —
etichette riancorate a un altro claim, informazione persa per assorbimento, qualificazioni cadute,
verbi irrigiditi.

Ogni violazione dichiara **in quale dei due passaggi è nata**, così la riparazione va nel punto
giusto invece che a caso. Chi ha prodotto la finale fa fino a **due riparazioni chirurgiche**. Se
le perdite sono diffuse, si consegna la **v5**: meno scorrevole, ma accurata — l'accuratezza sta
sopra la leggibilità nella gerarchia del metodo.

### Il registro della lingua

Gli ultimi due livelli producono, oltre al documento, tre segnali che valgono più del documento:
i **calchi ricorrenti** (gli stessi errori che l'autore rifà su ogni Bibbia), i **passaggi non
semplificabili** e i **passaggi rimasti oscuri**. Finivano in una riga di log e svanivano.

Ora li accumula `_dati/registro-lingua.md`, sullo stesso modello del registro delle deviazioni:
il sesto livello lo legge **prima** di iniziare — sa già cosa cercare — e ci deposita **dopo**;
l'autore legge le «Correzioni attive» prima di scrivere la v1. La promozione di un pattern da
osservazione a regola è **umana**.

Il senso è aritmetico: correggere un calco a valle costa una passata su ogni Bibbia, correggerlo
a monte costa una riga in `regole-di-scrittura.md` e non torna mai più.

## Come si lancia

Il workflow `bibbie-generate/_workflow/genera-bibbie.workflow.js` accetta:

- uno o più slug: `["reflusso"]`, `["reflusso","cervicalgia"]`
- oppure `"tutte"` per l'intero elenco di `_dati/problemi.json`

È resiliente: retry sugli agenti critici e promozione della versione precedente se una sintesi
fallisce. Un singolo fallimento non aborta la catena.

## Note operative

- Le skill sono **project-scoped**: valgono solo dentro questa cartella.
- Il `name:` in ogni `SKILL.md` deve combaciare col nome della cartella.
- Le skill vengono caricate all'avvio sessione: dopo modifiche strutturali **riavvia la
  sessione** perché Claude Code le rilevi.

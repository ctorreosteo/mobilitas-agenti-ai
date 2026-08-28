# Feedback — Fisioterapista Evidence-Based

**LENTE:** Fisioterapista Evidence-Based
**CONDIZIONE:** Dolori mandibolari (disturbi temporo-mandibolari)
**DOCUMENTO REVISIONATO:** `v1-bibbia.md` (letto anche `v1-mappa.md` come termine di paragone interno)
**DATA:** 27 agosto 2026

---

## RICERCA SVOLTA

Ho recuperato l'abstract di tutte e 43 le fonti dell'Appendice B tramite l'API PubMed, in questa sessione. Ho verificato uno per uno: autore, anno, rivista, numerosità, popolazione, risultato numerico e conclusione. Ho controllato entrambe le ancore: **Susan Armijo-Olivo** esiste, è attiva, e le affiliazioni dichiarate (Alberta + Osnabrück) corrispondono a quelle degli articoli 2024-2025 che firma; **Birgitta Häggman-Henrikson** esiste, è a Malmö/Umeå, e firma la meta-analisi Eur J Pain 2025 sul colpo di frusta. Ho cercato in più la letteratura 2024-2026 su terapia manuale e ATM per vedere se qualcosa contraddicesse il documento: non ho trovato niente che lo smentisca.

**Esito complessivo delle citazioni: nessuna citazione inventata, nessun PMID sbagliato, nessuna rivista o anno errato.** È il documento con la bibliografia più pulita che mi sia capitato di controllare. I problemi che restano sono di *lettura* delle fonti, non di esistenza: una fonte riassunta al contrario, due numeri usati fuori dal loro disegno, e alcune etichette che stanno un gradino troppo in alto.

Ho recuperato anche il dato che manca al documento: la storia naturale del paziente *doloroso*, non solo di quello bloccato (Ohrbach, *Eur J Pain* 2020, PMID 31421009).

---

## AUDIT DELLE ETICHETTE

| Capitolo | Affermazione | Etichetta attuale | Etichetta corretta | Fonte che lo stabilisce |
|---|---|---|---|---|
| «Cosa si rompe», secondo meccanismo | L'assetto cranio-cervicale cambia apertura e soglia dolorosa dei masticatori | **DIMOSTRATO** | **PROBABILE** | La Touche 2011 (PMID 20733480): n=29, disegno a misure ripetute intra-soggetto, posture indotte, nessun gruppo di controllo, nessun cieco, misure nella stessa sessione. Studio unico. |
| «La lettura osteopatica», Biomeccanico-Strutturale | Stessa affermazione, stessa fonte | **DIMOSTRATO** | **PROBABILE** | Idem |
| «Come funziona quando funziona», punto 6 | La posizione della testa cambia quello che la mandibola può fare | **ASSENTE** | **PROBABILE** | Il box DIMOSTRATO sta prima, e copre Eriksson/Häggman-Henrikson. Il punto 6 resta nudo. |
| «Cosa può fare il paziente da solo», Strumento 2 | Esercizio mandibolare e stretching | **DIMOSTRATO** | **DIMOSTRATO**, ma sull'intervento *supervisionato* | Busse 2023 (PMID 38101929): la raccomandazione forte è per *supervised* jaw exercise and stretching. Il documento descrive un esercizio domiciliare. |
| «Cosa si rompe», quinto meccanismo | Carico allostatico come fattore di rischio prospettico | **DIMOSTRATO** | **DIMOSTRATO** — regge | Fillingim 2013 (PMID 24275225). L'etichetta è correttamente circoscritta a "come fattore di rischio prospettico", non alla catena causale descritta. Non toccare. |
| «Non è una condizione sola», sottotipo Collo dominante | Il test di flessione-rotazione positivo identifica il sottotipo | **ASSENTE** | **RAGIONAMENTO** | Nessuno studio di accuratezza del test in questa condizione. von Piekartz 2016 è trasversale e su TMD *acuto/subacuto*. |

---

## STORIA NATURALE

Il documento **la dichiara**, ed è un merito raro: Kurita 1998 è citato per esteso, con il numero giusto (43 su 100 asintomatici a due anni e mezzo su 40 pazienti), e «Che cos'è davvero» avverte esplicitamente di non intestarsi il tempo.

**Il problema è il denominatore.** Quel 43% viene da 40 pazienti con **dislocazione discale senza riduzione** — il blocco. Il paziente modale di questa Bibbia è il *muscolare da tensione diurna*, per il quale il documento non dà nessun dato di decorso spontaneo. E in un punto la restrizione cade: «Come ragiono davanti a questo paziente» apre con *"su questa condizione il tempo, da solo, migliora tre pazienti su quattro"*, senza la parola "bloccati" che c'è ovunque altrove. È la frase che il lettore memorizza, ed è quella sbagliata.

Il dato che manca esiste: nella coorte OPPERA, dei 147 casi di TMD doloroso di prima insorgenza riesaminati a sei mesi, **75 su 147 (51%) erano risolti** e 72 (49%) persistevano (Ohrbach, *Eur J Pain* 2020, PMID 31421009).

---

## ERRORI

### 1. La validità del DC/TMD sui quadri articolari è riassunta al contrario — e proprio sul sottotipo su cui la Bibbia mette il vincolo di tempo

**Capitolo:** «Che cos'è davvero», sezione *La definizione, e la prima cosa da correggere*

Il documento scrive: *"Per i quadri articolari — cioè per il disco e per il rumore — i criteri clinici non hanno validità sufficiente a fare una diagnosi e valgono solo come screening"*, e nel box «Cosa cambia per te» conclude che *"il pezzo del quadro che riconosci con le mani in modo affidabile è il dolore, non il disco"*.

**Prova.** Schiffman 2014 (PMID 24482784) dice un'altra cosa: *"valid diagnostic criteria for differentiating the most common pain-related TMD (sensitivity ≥ 0.86, specificity ≥ 0.98) **and for one intra-articular disorder (sensitivity of 0.80 and specificity of 0.97)**. Diagnostic criteria for **other** common intra-articular disorders lack adequate validity."* Quell'unico quadro intra-articolare validato è la **dislocazione discale senza riduzione con apertura limitata**: sensibilità 0,80, specificità 0,97. Cioè esattamente il **blocco recente** — il sottotipo su cui la Bibbia costruisce la riga GIALLA della tabella delle bandiere rosse, il "presto" del capitolo sui sottotipi, e la frase-chiave dell'anamnesi.

**Correzione.** Sostituire "i quadri articolari" con "gli **altri** quadri articolari", e aggiungere una riga: *"L'unica eccezione è la dislocazione discale senza riduzione con apertura limitata, i cui criteri clinici reggono (sensibilità 0,80, specificità 0,97): il blocco, a differenza del click e dell'artrosi, si riconosce con le mani."* Il box «Cosa cambia per te» va riscritto di conseguenza: il bersaglio resta dolore e funzione, ma il blocco entra fra i quadri clinicamente identificabili. La correzione rafforza il documento, non lo indebolisce.

### 2. DIMOSTRATO su uno studio unico, piccolo e senza controllo

**Capitolo:** «Cosa si rompe», secondo meccanismo — e «La lettura osteopatica», Biomeccanico-Strutturale

Entrambi i box portano **DIMOSTRATO** *(studi sull'uomo, solidi)* per l'affermazione che l'assetto cranio-cervicale cambia apertura e soglia dolorosa, e la sola fonte è La Touche 2011.

**Prova.** La Touche 2011 (PMID 20733480): 29 pazienti, disegno a misure ripetute su un solo gruppo, tre posture indotte sperimentalmente nella stessa seduta, nessun gruppo di controllo, nessuna cecità, esiti misurati dallo stesso operatore. Non è un RCT; è un esperimento intra-soggetto. In più, una parte dell'effetto sull'apertura massima è vincolo meccanico diretto della postura indotta, non fenomeno clinico: le F riportate (117-208) sono di quella grandezza per questo motivo. Uno studio unico di questo disegno non fa un DIMOSTRATO nella glossa che il documento si è dato ("studi sull'uomo, solidi").

**Correzione.** Portare entrambe le etichette a **PROBABILE** *(razionale forte, prove parziali)*, e aggiungere nella frase: *"misurato in una sola serie di 29 pazienti, senza gruppo di controllo, con posture indotte nella stessa seduta"*. Il DIMOSTRATO del documento sull'accoppiamento mandibola-collo (Eriksson 2000, Häggman-Henrikson 2013, tre studi dello stesso gruppo) **resta dov'è**: quello regge.

### 3. Il denominatore del blocco applicato a tutta la condizione

**Capitolo:** «Come ragiono davanti a questo paziente», riga di apertura

*"...perché su questa condizione il tempo, da solo, migliora tre pazienti su quattro."*

**Prova.** Kurita 1998 (PMID 9465168) ha seguito **40 pazienti con dislocazione discale senza riduzione**. Il 76% (43% asintomatici + 33% migliorati) riguarda loro. Non riguarda il paziente muscolare da tensione diurna, che il documento stesso indica come *"il quadro più frequente e quello con il maggiore spazio per te"*. Ovunque altrove il documento scrive correttamente "bloccati"; qui la parola cade, e cade nella frase di apertura di un capitolo.

**Correzione.** Due cose. Primo: ripristinare *"tre pazienti **bloccati** su quattro"*. Secondo — e conta di più — aggiungere in «Che cos'è davvero», accanto a Kurita, il dato che manca per il paziente modale: *"Nella coorte OPPERA, dei 147 casi di dolore mandibolare di prima insorgenza riesaminati a sei mesi, 75 su 147 erano risolti e 72 persistevano (Ohrbach, Eur J Pain 2020, PMID 31421009)."* Senza quel numero, metà del documento si attribuisce una fluttuazione di cui non ha dichiarato la dimensione.

---

## RISCHI

### 1. Un'affermazione senza etichetta in «Come funziona quando funziona»

Il punto 6 (La Touche 2011, posizione della testa) segue il box DIMOSTRATO che copre i punti 1-5 e resta **senza etichetta propria**. In un documento che dichiara *"se una frase non ha etichetta accanto, cercala: c'è"*, un'affermazione nuda in questa posizione si legge come coperta dal DIMOSTRATO precedente.
**Mitigazione:** box proprio, **PROBABILE**, con la frase sul disegno dello studio (vedi ERRORE 2).

### 2. Un intervallo fra interventi diversi presentato come intervallo di una stima

**Capitolo:** «Cosa può fare il paziente da solo», Strumento 2.
Il documento scrive che l'esercizio mandibolare con stretching migliora il dolore *"con una quota fra ventitré e trenta pazienti su cento in più che raggiungono il miglioramento minimo"*. In Yao 2023 (PMID 38101924) quel "23%-30%" **non è l'intervallo di confidenza di quell'intervento**: è la forbice fra le stime puntuali di **cinque interventi diversi** (*"Five interventions were less effective... showing RDs ranging between 23% and 30%"*). Un lettore lo legge come precisione, ed è dispersione fra bracci.
**Mitigazione:** o riportare la stima e l'IC del solo esercizio mandibolare con stretching, o scrivere esplicitamente *"in un gruppo di cinque interventi le cui stime vanno da 23 a 30 su 100"*. Il dato sulla **funzione fisica** (43 su 100, IC 33-51, certezza moderata) è invece esatto, ed è quello da mettere per primo.

### 3. La parola "supervisionato" cade fra la linea guida e i due strumenti attivi

**Capitolo:** «Cosa può fare il paziente da solo», Strumenti 1 e 2.
Il capitolo apre dicendo che tre strumenti hanno raccomandazione forte a favore. In Busse 2023 (PMID 38101929) le voci sono *supervised postural exercise* e *supervised jaw exercise and stretching*. Gli strumenti descritti dal documento sono un programma *"fatto a casa, senza attrezzi e con supervisione bassa"* e movimenti *"eseguiti dal paziente"*. La raccomandazione forte non copre automaticamente la versione non supervisionata.
**Mitigazione:** scrivere "supervisionato" dov'è nella fonte, e aggiungere una riga onesta: *"la raccomandazione forte riguarda l'esercizio supervisionato; quanto se ne conservi nella versione domiciliare non è stato misurato."* Nota che de Oliveira-Souza 2024 (PMID 39788575) aiuta qui — gli autori scrivono che gli esercizi cervicali *"require low therapeutic supervision"* — e quella frase va citata, perché è l'unico appiglio che il documento ha.

### 4. La Cochrane sul bite riassunta un grado più a proprio favore

**Capitoli:** «Come si usa questa Bibbia», blocco finale — e «Cosa dice la scienza».
Il documento dice che la revisione Cochrane *"non è riuscita a concludere niente su nessun esito"* e *"non conclude nulla"*. Singh 2024 (PMID 39282765) è inconclusiva **ma non muta**: *"Occlusal splints of the FHSS type may reduce muscle pain when chewing compared to no treatment (MD -1.97, 95% CI -2.37 to -1.57; 1 study, 84 participants), but the evidence is very uncertain."* Il solo segnale che c'è va **a favore** del bite, sull'esito muscolare, che è proprio il terreno del documento. Ometterlo è la scorciatoia più visibile del testo, ed è quella che un gnatologo informato userebbe per liquidare tutto il resto.
**Mitigazione:** una riga: *"il solo segnale emerso, a certezza molto bassa e da un unico studio su 84 pazienti, va a favore del dispositivo sul dolore muscolare masticando."* Il messaggio operativo — il bite non è la fine della storia, e non lo tocchi tu — non cambia di una virgola, e diventa inattaccabile.

### 5. Leung 2025 usato come misura di rischio, mentre non ha denominatore

**Capitoli:** «Le strutture in gioco» — e «Perché le mani possono cambiare qualcosa», seconda leva.
*"Gli eventi avversi gravi dopo procedure fisiche sul collo sono vascolari in cinquantotto casi su cento"*. Leung 2025 (PMID 39663097) è una raccolta di **334 casi pubblicati in 233 studi**, senza alcun denominatore di trattamenti eseguiti. Il 58% descrive *di cosa sono fatti gli eventi segnalati*, non *quanto spesso capitano*. Scritto "su cento", si legge come rischio. In più il documento estende la fonte dal **rachide cervicale** (l'oggetto della revisione) al **triangolo anteriore del collo e al pavimento della bocca**, che non sono il distretto studiato.
**Mitigazione:** aggiungere *"su casi pubblicati, senza denominatore di trattamenti eseguiti: il dato dice com'è composto ciò che viene segnalato, non con che frequenza accade"*, e riformulare la regola sul triangolo anteriore come **scelta prudenziale del metodo** (beneficio non misurato in questa condizione) invece che come rischio documentato in quel distretto. La condotta resta identica; la giustificazione diventa vera.

### 6. Le soglie dei marker: una popolazione sostituita, e un "sopra l'errore" mai verificato

**Capitolo:** «Come ragiono davanti a questo paziente», *I marker di questa condizione*.
Due cose. **(a)** Kropmans 1999 (PMID 10096454) calcola la differenza minima rilevabile di 5 mm per la **apertura massima** in **soggetti sani**; il documento la applica alla **apertura senza dolore** nei **pazienti**. E "3 mm su media di tre" aggiunge il "di tre" che nella fonte non c'è (l'abstract dice solo *"repeated measurements improved it to 3 mm"*). **(b)** Il documento dichiara che il +20% sulle due soglie algometriche è una convenzione *"scelta sopra l'errore dello strumento"* — ma l'errore dello strumento non viene mai dato. Per l'apertura la fonte c'è ed è citata; per l'algometria si afferma di essere sopra una soglia che non si nomina. È esattamente la mossa che il documento contesta altrove.
**Mitigazione:** dichiarare popolazione e variabile di Kropmans (*"soggetti sani, apertura massima"*); togliere "di tre" o dichiararlo come scelta del metodo; e sostituire *"scelte sopra l'errore dello strumento"* con *"convenzioni di questo metodo, non verificate contro l'errore di misura dell'algometro"* — oppure citare un MDC per la soglia dolorosa del massetere, se lo si trova.

### 7. Gomes 2008 citato solo per la metà che serve

**Capitoli:** «Come ragiono davanti a questo paziente» — e «Dove finisce il nostro campo», *Il cancello d'ingresso*.
Del lavoro di Gomes (PMID 18686497) il documento prende l'affidabilità inter-esaminatore (0,64 nei pazienti) e la usa bene. Omette la conclusione: *"The tests had low diagnostic validity to discriminate between patients and controls, with low positive predictive values."* Poi «Il cancello d'ingresso» mette **la soglia algometrica** fra i reperti che *"reggono"* e che fondano il mandato clinico. Fondare un mandato su un test di cui la fonte citata dichiara bassa validità discriminativa è attaccabile da chiunque legga l'abstract.
**Mitigazione:** aggiungere una riga in «Dove finisce il nostro campo»: *"la soglia algometrica regge come misura di cambiamento nello stesso paziente, presa da te prima e dopo; nella stessa fonte non regge come test per distinguere un paziente da un sano (bassa sensibilità, basso valore predittivo positivo)."* Distinzione corretta, e la difende.

### 8. Il test di flessione-rotazione ha un ruolo di smistamento e nessuna etichetta

**Capitoli:** «Non è una condizione sola» (sottotipo Collo dominante) — «Come ragiono davanti a questo paziente» (Road Map punto 4, Paziente B).
Il test decide un sottotipo, entra nella Road Map e determina cosa si tratta per primo nel Paziente B. Non porta etichetta, e non esiste uno studio di accuratezza del test in questa condizione. La fonte che regge il sottotipo, von Piekartz 2016 (PMID 27744136), è **trasversale** e su TMD **acuto/subacuto**, mentre il paziente della Bibbia ha dolore da almeno tre mesi.
**Mitigazione:** etichetta **RAGIONAMENTO** sul sottotipo Collo dominante, e una riga in «Cosa si rompe»: *"misurato in un disegno trasversale su disturbo acuto e subacuto; nel paziente cronico la stessa graduazione non è stata verificata."*

### 9. Un claim di evidenza senza citazione, e due fonti orfane in bibliografia

**Capitolo:** «Cosa si rompe», blocco finale.
*"Non ti autorizza a dire al paziente che il suo bruxismo notturno è la causa: quel nesso, misurato con strumenti oggettivi, si indebolisce molto."* È un'affermazione di evidenza, ed è **nuda**. Intanto in Appendice B ci sono due voci mai richiamate nel corpo: la **42** (Manfredini 2025, INfORM/IADR, PMID 39360749) e la **43** (Manfredini e Lobbezoo 2010, PMID 20451831) — e la 43 è precisamente la fonte che sosterrebbe quella frase: *"Studies based on more quantitative and specific methods to diagnose bruxism showed much lower association with TMD symptoms. Anterior tooth wear was not found to be a major risk factor for TMD."*
**Mitigazione:** attaccare PMID 20451831 alla frase, con quelle parole. E o si aggancia la 42 a qualcosa, o esce dalla bibliografia: una fonte elencata e mai usata è un numero che nessuno ha letto.

---

## PREFERENZE

### 1. L'ancora clinica si prende un primato che il documento stesso non le dà

«Cosa dice la scienza», *Le due ancore*: *"ed è sempre lei a firmare il risultato positivo più solido di questo documento"*. Il risultato positivo più solido del documento è la meta-analisi a rete di Yao e la linea guida di Busse, che Armijo-Olivo non firma. Lei firma la meta-analisi **negativa** (che è il suo valore, e il documento lo dice benissimo) e un RCT su 54 donne etichettato PROBABILE. Basta cambiare in *"ed è sempre lei a firmare l'unico studio controllato di questo documento che porta un risultato positivo suo"*.

### 2. Due numeri OPPERA arrotondati verso il comodo

«Cosa si rompe», quinto meccanismo: *"3.263 persone... seguite in media per due anni e otto mesi"*. In Fillingim 2013, i 3.263 sono gli arruolati; **2.737** hanno fornito il follow-up ed entrano nell'analisi. E la media è 2,8 anni, cioè due anni e dieci mesi. Nessuna delle due cose cambia una decisione, ma è il tipo di dettaglio su cui il documento è severo con sé stesso altrove.

---

## TIENE

Molto, e va detto perché è raro.

- **La bibliografia.** Quarantatré fonti, tutte reali, tutti i PMID corretti, tutti gli anni e le riviste corretti. I numeri che ho ricontrollato uno a uno — 43/33/25 di Kurita, 62,1% contro 36,2% di Câmara-Souza, 36% (31-40) e 32% (29-34) di Yao, 31,1%/25,9%/9,8% di Valesan, 133 casi di Barry, 334 casi di Leung, ES 0,33 di Michelotti, 0,64 di Gomes, 71% di Bartsch, 18,9%/26,8%/5,7% di Häggman-Henrikson — **sono tutti esatti**.
- **La raccomandazione condizionale contro il bite** è riportata correttamente come condizionale, con il limite giusto ("riguarda il dolore e non lo smalto"). Non toccare.
- **«Cosa possiamo dire, e cosa no»** è la sezione fatta per me, e non è timida. Il punto *"che il nostro tocco abbassi l'attivazione del sistema nervoso: dove è stata misurata, la direzione va dall'altra parte"* è il contrario di quello che la letteratura osteopatica di solito scrive, ed è documentato. Resta.
- **Le IPOTESI usate correttamente**: il riposizionamento del disco, il legamento disco-malleolare (con la prova contraria di Cheynet citata e nominata), il modello Respiratorio-Circolatorio dichiarato per metà non pertinente, l'inversione di direzione del comportamento diurno. Sono etichette oneste. Chi le ha scritte ha resistito a una tentazione ovvia.
- **Il RAGIONAMENTO su «Come ragiono davanti a questo paziente»** è messo dove deve stare, all'inizio del capitolo e su tutto il capitolo. Non ho obiezioni al Motore Clinico così qualificato.
- **La coppia Sessle/Bartsch dichiarata come animale**, con il box «Attenzione» che dice *"il salto è di specie, e non si attraversa in silenzio"*. Regge, e la conclusione che ne trae ("regge il razionale, non regge nessuna promessa sull'orecchio") è quella giusta.
- **Il DIMOSTRATO sul modello Comportamentale-Biopsicosociale**, con l'ammissione che è il modello con le prove migliori e che non è l'atto dell'osteopata. È la frase più scomoda del documento ed è quella che me lo fa prendere sul serio.

---

## VERDETTO: **Da correggere**

Il documento regge. Le fonti esistono e dicono quello che il documento dice, salvo un caso; le etichette sono oneste, salvo due; e la sezione dei limiti è scritta davvero, non per finta. Le correzioni sono tre chirurgiche — la validità del DC/TMD sul blocco, il DIMOSTRATO di La Touche portato a PROBABILE, il denominatore di Kurita rimesso al suo posto con la storia naturale del paziente doloroso accanto — più una serie di righe da aggiungere dove una fonte è stata riassunta un grado a proprio favore. Nessuna di queste tocca la struttura né il messaggio operativo. Corrette, questo documento sopravvive a dieci minuti di PubMed fatti da un ostile.

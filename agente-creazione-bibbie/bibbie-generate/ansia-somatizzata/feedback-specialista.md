# Feedback — Revisore Specialista (primo livello)

**LENTE:** Medico Specialista — Psichiatra (in Italia è lo specialista che gestisce di norma i disturbi d'ansia e il disturbo da sintomi somatici; la condizione non è in tabella nella skill, quindi lo dichiaro qui).
**CONDIZIONE:** ansia somatizzata
**DOCUMENTO REVISIONATO:** `/Users/carlitos/mobilitas-agenti-ai/agente-creazione-bibbie/bibbie-generate/ansia-somatizzata/v1-bibbia.md` (v1, 29 agosto 2026), con la Mappa `v1-mappa.md` come riscontro.
**VERDETTO:** Da correggere.

---

## RICERCA SVOLTA

Ho verificato in questa sessione, su PubMed (eutils/efetch), **tutte** le citazioni portanti del capitolo «Cosa dice la scienza» e dei box di solidità: Alonso 2018 (29356216, 9,8% / 27,6% / 9,8% — corretto), Rolfe e Burton 2013 (23440131 — vedi rilievo 7), Löwe 2022 (34776017, 12,9% IC 12,5-13,3 — corretto), Hornsveld 1996 (8684155, 115 pazienti, 85 positivi di cui 56 positivi anche al placebo, pCO2 scesa in 7 attacchi spontanei su 22 — corretto), Cadegiani 2016 (27557747 — corretto), Berthoud 2000 (11189015), Hoehn-Saric 1989 (2589925, EMG sì / autonomico no — corretto), Joseph 2005 (16129818, 5,8→10,3 ms/mmHg — corretto), Grassi 2013 (23107756 — corretto), Meuret 2010 (20873904 — corretto), Meuret 2008 (17681544), Gordon 2025 (39920074: depressione g=-0,47 e conduttanza cutanea g=+0,67 gli unici significativi — l'uso che ne fa il documento è corretto), Adams 2022 (35798125 — corretto), Chalmers 2014 (25071612, HF g=-0,29 / dominio del tempo g=-0,45), Hansen 2025 (40232939 — corretto), Fond 2014 (24705634, SMD 0,76 — corretto), Simon 2021 (32805013, 70,8% / 54,2% / 33,0% — vedi rilievo 11), Stubbs 2017 (28088704), Vicenzino 1998 (9777544, r=0,82), Chu 2023 (36690712, 0,21/100.000, due fratture costali in donne >60 osteoporotiche — corretto), Hall 2010 (20357415, MDC90 4,7° destra e 7° sinistra), Toussaint 2020 (32090765, MCID 4 punti — vedi rilievo 12), Fincham 2023 (36624160, k=12 n=785 g=-0,35 stress; k=20 g=-0,32 ansia — corretto), Goessl 2017 (28478782), Laborde 2022 (35623448), Fleet 1996 (8873507).

**Nessun PMID è inventato e nessun risultato è capovolto.** È il livello di verificabilità più alto che mi sia capitato di controllare in un documento non medico, e va detto.

Ho poi cercato quello che il documento *non* cita: la storia naturale quantificata dei disturbi d'ansia (Bruce 2005, HARP, PMID 15930067, verificato su PMC3272761), la letteratura sulla tachicardia parossistica sopraventricolare scambiata per panico (Lessmeier 1997, *Arch Intern Med*, PMID 9066458), l'ostruzione laringea inducibile come mimo di dispnea con spirometria normale (AAFP *Vocal Cord Dysfunction: Rapid Evidence Review* 2021; Delphi internazionale *JACI* 2023), NICE NG225 sull'autolesionismo, e il warning regolatorio su ideazione suicidaria negli under-25 nelle prime settimane di SSRI/SNRI.

---

## ERRORI

### 1. Manca la bandiera rossa che in questa condizione produce il ritardo diagnostico più documentato: le palpitazioni parossistiche a esordio e cessazione bruschi in assenza di cardiopatia nota

**Capitolo:** «Dove finisce il nostro campo» (tabella delle bandiere rosse) e «Che cos'è davvero» (sezione «Cosa dicono le etichette che porta»).

La tabella copre le palpitazioni solo alla riga *«Palpitazioni con cardiopatia nota»*. È il filtro sbagliato: esclude esattamente la popolazione a rischio, cioè la persona giovane, spesso donna, **senza** cardiopatia nota.

**Prova.** Lessmeier 1997 (*Arch Intern Med*, PMID 9066458), 107 pazienti consecutivi con TPSV da rientro documentata in elettrofisiologia: la TPSV **non era stata riconosciuta nel 55%** dei casi; nel 54% di quelli i sintomi erano stati attribuiti da medici non psichiatri a panico, ansia o stress; **il 67% soddisfaceva i criteri DSM-IV per disturbo di panico**. Quando la TPSV non era riconosciuta, l'attribuzione psichiatrica riguardava **il 65% delle donne contro il 32% degli uomini** (p<0,04). Dopo terapia guidata dall'elettrofisiologia i sintomi si sono risolti nell'86% e solo il 4% continuava a soddisfare i criteri di panico.

Il secondo pezzo dello stesso errore: nello stesso studio **l'Holter ha individuato la TPSV solo in 6 pazienti su 64 (9%), contro 8 su 17 (47%) con il registratore a eventi**. Il documento tratta l'Holter negativo come un accertamento che ha chiuso la partita cardiologica — in «Cosa ha già fatto» («Holter delle 24 ore, normale») e soprattutto nell'uscita **VERDE** del cancello, dove «gli accertamenti cardiologici richiesti per i sintomi presenti sono stati eseguiti e sono negativi» apre la via al trattamento. Con questi numeri, un Holter negativo in un paziente con palpitazioni a interruttore non è un accertamento negativo: è un accertamento con il 91% di falsi negativi.

**Correzione.**
1. Aggiungere una riga alla tabella: `Palpitazioni parossistiche a esordio e cessazione bruschi, o frequenza percepita molto alta, anche senza cardiopatia nota | Cardiologo | Invio, non attendere | GIALLO PRIORITARIO`.
2. Riscrivere il bullet «Elettrocardiogramma e Holter normali» in «Che cos'è davvero» aggiungendo la condotta: un Holter negativo non esclude una TPSV, e in presenza di episodi a esordio/cessazione bruschi serve un registratore a eventi o un loop recorder — richiesta che parte dal cardiologo, non da noi.
3. Nell'uscita VERDE, qualificare «accertamenti eseguiti e negativi»: per il sottotipo cardiocentrico un Holter negativo da solo non soddisfa la condizione.

---

### 2. La riga sui pensieri di farsi del male ha un solo destinatario e un solo tempo, e il documento omette il dato di suicidalità dello studio che cita di più

**Capitolo:** «Dove finisce il nostro campo» (tabella delle bandiere rosse; «Le tre cose da ricordare»).

La riga è: `Pensieri di farsi del male | Medico curante | Urgente, in giornata | ROSSO`. Un'unica riga copre l'intero spettro, dall'ideazione passiva («preferirei non svegliarmi») all'intento con piano e mezzi disponibili, e in entrambi i casi il canale è il medico curante — che il venerdì sera non c'è, e a cui il paziente arriva da solo.

**Prova.** NICE NG225 (*Self-harm: assessment, management and preventing recurrence*, 2022) colloca il rischio di suicidio **30-50 volte** più alto nell'anno successivo a una presentazione per autolesionismo, e non consente il rinvio differito quando c'è intento o atto recente. E soprattutto: **Fleet 1996 (PMID 8873507), lo studio che questa Bibbia cita tre volte, riporta che il 25% dei pazienti con disturbo di panico in pronto soccorso riferiva ideazione suicidaria contro il 5% degli altri.** Il documento estrae da quell'abstract il 25%, il 44% e il 98%, e lascia fuori l'unico dato dei quattro che riguarda la mortalità.

**Correzione.**
1. Spezzare la riga in due. `Pensieri di farsi del male, senza piano né intento | Medico curante | Urgente, in giornata | ROSSO`. `Intento, piano, mezzi disponibili, o atto recente | 112 o pronto soccorso, e non si lascia andare via da solo | 112 | ROSSO`.
2. Aggiungere il dato di Fleet sull'ideazione suicidaria accanto agli altri tre, in «La coesistenza fra ansia e cardiopatia» o nel box «Perché ci sei tu» del capitolo, con una riga di condotta: in questo quadro la domanda si fa, non si aspetta che la porti lui.

---

### 3. «Spirometria normale — esclude un'ostruzione» è falso, ed è falso proprio sul fenotipo che il documento descrive in copertina

**Capitolo:** «Che cos'è davvero» (sezione «Cosa dicono le etichette che porta») e «Cosa non è».

Il paziente ritratto dal Capitolo 1 è: nodo in gola, *«non riesco a fare un respiro pieno»*, difficoltà prevalentemente inspiratoria, esami negativi, spirometria normale. È la descrizione testuale dell'**ostruzione laringea inducibile** (ILO, già disfunzione delle corde vocali). La spirometria a riposo in questi pazienti è normale per definizione: l'ostruzione è extratoracica, inspiratoria ed episodica, e quando è visibile si vede come appiattimento del ramo inspiratorio della curva flusso-volume — non come un difetto ostruttivo. La diagnosi richiede laringoscopia durante provocazione.

**Prova.** *Vocal Cord Dysfunction: Rapid Evidence Review*, AAFP 2021; *Diagnosis of vocal cord dysfunction/inducible laryngeal obstruction: An International Delphi Consensus Study*, J Allergy Clin Immunol 2023. Entrambe le fonti riportano che l'ILO è comunemente attribuita ad ansia o asma e che la funzionalità respiratoria da sola non la conferma né la esclude; l'attribuzione all'ansia è segnalata dai pazienti come il danno principale del percorso — che è esattamente la tesi del Capitolo 1 di questa Bibbia, applicata contro di essa.

**Correzione.**
1. Riscrivere il bullet: *«Spirometria normale. Esclude un difetto ostruttivo delle vie aeree inferiori. Non esclude un'ostruzione laringea inducibile, che è inspiratoria, episodica e invisibile a riposo.»*
2. Aggiungere l'ILO all'elenco «Cosa non è», con la condotta: nodo in gola con dispnea prevalentemente inspiratoria, stridore o voce alterata durante l'episodio → invio pneumologico/ORL per laringoscopia in provocazione, prima di attribuire al tono cricofaringeo.
3. Il Capitolo 3 attribuisce il nodo in gola al cricofaringeo con una sicurezza che, senza il punto 2, diventa una spiegazione alternativa a una diagnosi mancata.

---

### 4. La storia naturale è descritta e non è quantificata, e senza il numero tutto il documento si intesta la parte discendente della curva

**Capitolo:** «Che cos'è davvero», sezione «Come evolve se non fai nulla».

Il documento dice la cosa giusta in modo qualitativo — decorso fluttuante, marker scelto prima, evitamento che si accumula — e per questo il capitolo è già metà del lavoro. Ma non dice **quanta** parte migliora da sola, in quanto tempo, in che percentuale. È l'unico dato che rende leggibile ogni miglioramento osservato in stanza, e manca.

**Prova.** Bruce 2005 (*Am J Psychiatry* 162:1179-87, PMID 15930067), coorte HARP, 711 pazienti seguiti prospetticamente 12 anni. Probabilità cumulativa di **remissione a 12 anni**: 0,82 per il disturbo di panico senza agorafobia, 0,58 per l'ansia generalizzata, 0,48 per il panico con agorafobia, 0,37 per la fobia sociale. Probabilità di **ricaduta dopo la remissione**: 0,56, 0,45, 0,58 e 0,39 rispettivamente.

Sono i numeri che chiudono la questione meglio di qualunque frase: quattro pazienti su cinque con panico senza agorafobia rimettono nell'arco dell'osservazione, e più della metà di loro ricade. Il primo dato dice perché il marker va scritto prima; il secondo dice perché il paziente che torna dopo otto mesi non è un fallimento del ciclo precedente.

**Correzione.** Inserire i quattro valori di remissione e i quattro di ricaduta in «Come evolve se non fai nulla», con la fonte, e legarli alla regola già presente («chi prende in carico un paziente nella parte discendente della sua curva si attribuisce un miglioramento che sarebbe arrivato lo stesso»). Aggiungere la clausola sulla ricaduta al capitolo «Cosa dire al paziente»: la ricomparsa a distanza è nella storia naturale, e va detta prima, non dopo.

---

## RISCHI

### 5. Il biofeedback della variabilità cardiaca porta DIMOSTRATO su una base che è tutta autoriferita

**Capitolo:** «Cosa può fare il paziente da solo», Strumento 3.
**Etichetta attuale:** DIMOSTRATO. **Etichetta corretta:** PROBABILE.

Goessl 2017 (PMID 28478782): 24 studi, 484 partecipanti, esiti di stress e ansia **tutti autocompilati**, nessuna cecità possibile su un intervento con un sensore visibile, controlli in larga parte passivi, e conclusione degli autori che serve una base meglio controllata. Il documento lo scrive nella glossa — ma la sua stessa regola dice che *«l'etichetta non si declina»*. Un g di 0,83 misurato con questionari autocompilati contro controllo passivo non è «studi sull'uomo, solidi»: è un razionale forte con prove parziali, che è la definizione di PROBABILE in questo documento.

**Perché è attaccabile.** È l'unico dei tre strumenti attivi a cui un lettore esterno può togliere l'etichetta senza discussione, e togliendola indebolisce anche gli altri due, che invece la reggono. Il respiro lento (Fincham, effetti piccoli, -0,32/-0,35, ma con cautela dichiarata dagli autori) e l'esercizio (Stubbs, -0,58, base stretta ma esiti clinici) stanno meglio in piedi.

**Mitigazione.** Portare l'etichetta a PROBABILE e lasciare la glossa dov'è. La sezione «Cosa non fa» — il paziente che compra il sensore e comincia a guardarsi il battito tutto il giorno — è ottima e va tenuta intatta.

---

### 6. Il passo che genera il sintomo nel primo meccanismo viaggia senza etichetta propria, e la prova contraria sta in un altro capitolo

**Capitolo:** «Cosa si rompe: i meccanismi», meccanismo 1 (e riflesso in «Che cos'è davvero», sezione «Cosa non è»).

Il box spezza correttamente l'etichetta fra il reperto (DIMOSTRATO, Grassi), la mediazione (DIMOSTRATO, Meuret) e la leva manuale (IPOTESI). Manca però l'etichetta sul passo 4 della catena: *«ogni piccola accelerazione del respiro porta il sistema oltre la soglia in cui compaiono testa leggera, formicolii e stretta al petto»*. È il passo che collega la riserva bassa al sintomo, ed è quello su cui esiste una prova contraria — **la stessa che il documento cita due capitoli prima**: Hornsveld 1996 (PMID 8684155) ha registrato una caduta di pCO2 in **7 attacchi spontanei su 22**, e dopo l'inizio dell'attacco, non prima, concludendo che *«hyperventilation seems a negligible factor in the experience of spontaneous symptoms»*.

**Perché è attaccabile.** Il documento smonta la sindrome da iperventilazione in «Cosa non è» e poi ricostruisce, in «Cosa si rompe», una catena causale che quella stessa fonte indebolisce — senza che le due pagine si tocchino. Un lettore che apre Hornsveld trova la contraddizione prima di trovare la spiegazione.

**Mitigazione.** Etichettare il passo 4 come **PROBABILE**, con la glossa e Hornsveld citato **nella stessa riga**, come impone la regola dichiarata al Capitolo 0. La distinzione da scrivere è netta e regge: la riserva bassa è misurata di base (Grassi), la caduta acuta di CO2 *durante* l'episodio no (Hornsveld). Sono due grandezze diverse, e il documento è già a un passo dal dirlo.

---

### 7. I tre esiti nulli di Rolfe e Burton sono attribuiti all'intera base di 14 studi, mentre due dei tre poggiano su due e tre studi

**Capitolo:** «Chi ti trova davanti» (sezione «Cosa nessuno ha guardato») e «Cosa fare adesso» («è stato provato quattordici volte in modo controllato»).

Il testo scrive: *«Su 14 studi randomizzati e 3.828 pazienti [...] gli esami diagnostici non hanno ridotto la preoccupazione per la salute, non hanno ridotto l'ansia generica e non hanno fatto sparire i sintomi»*. Nell'abstract verificato (PMID 23440131) i denominatori sono tre e diversi: **3 studi** per la preoccupazione di malattia (OR 0,87, IC 0,55-1,39), **2 studi** per l'ansia aspecifica (SMD 0,06, IC -0,16-0,28), **10 studi** per la persistenza dei sintomi (OR 0,99, IC 0,85-1,15).

**Perché è attaccabile.** È la sola inflazione di citazione che ho trovato nel documento, e cade nel capitolo di apertura, che è quello che un medico legge per primo. Un nullo su 2 studi con quell'intervallo di confidenza non è un nullo: è un'assenza di informazione. Il messaggio clinico regge lo stesso — sulla persistenza dei sintomi i 10 studi ci sono — ma va scritto con i suoi tre numeri.

**Mitigazione.** Riportare i tre denominatori separati; correggere «quattordici volte in modo controllato» del Capitolo 14 in «dieci volte, sulla persistenza dei sintomi».

---

### 8. La finestra di avvio di SSRI e SNRI è trattata come problema di attribuzione e non come finestra di sorveglianza

**Capitolo:** «Dove finisce il nostro campo», sezione «I farmaci che prende, e il prescrittore».

Il documento scrive che SSRI e SNRI «nelle prime settimane possono aumentare i sintomi somatici — un motivo in più per non attribuirsi né i peggioramenti né i miglioramenti che cadono in quella finestra». È corretto e insufficiente. In quella stessa finestra — primi 4-6 settimane, con il picco nel primo mese — la letteratura regolatoria (warning FDA recepito da EMA e MHRA, su 342 studi randomizzati e 99.231 adulti) documenta un aumento **età-dipendente** di ideazione e comportamento suicidario negli **under-25**, insieme ad agitazione e acatisia.

**Perché è attaccabile.** L'osteopata vede questo paziente ogni settimana, più spesso del prescrittore, e in questo documento è già l'unico a scrivere al curante. È il posto naturale in cui un peggioramento si nota — e il documento gli dice espressamente di *non* attribuirsi i peggioramenti in quella finestra, cioè, letto male, di non farci caso.

**Mitigazione.** Aggiungere una riga: in un paziente under-25 che ha iniziato o cambiato SSRI/SNRI da meno di sei settimane, l'agitazione nuova, l'irrequietezza motoria e qualunque pensiero di farsi del male non sono rumore da non attribuirsi — sono un'informazione che va al prescrittore in giornata. Collegarla esplicitamente alla riga rossa corretta al rilievo 2.

---

### 9. Si somministra il GAD-7, si scrive al curante, e la comorbidità che porta il rischio non viene mai cercata

**Capitolo:** «Dove finisce il nostro campo» (confine di atto, lettera al curante) e «Cosa dice la scienza».

La depressione compare in tutto il documento due volte, ed entrambe come dato altrui: l'effetto di -0,47 di Gordon 2025 e il nome della scala di Chalmers. Non esiste una riga che dica all'osteopata che il paziente che ha davanti ha una probabilità alta di avere anche un episodio depressivo, né uno strumento per accorgersene, né una parola nella lettera al curante — che contiene «quattro cose e nient'altro», e nessuna delle quattro è questa.

**Perché è attaccabile.** Bruce 2005 (PMID 15930067) mostra che il decorso di tutti e tre i disturbi peggiora con la depressione maggiore e con i disturbi da uso di alcol e sostanze in comorbidità: è la variabile prognostica principale della coorte. E il rischio del rilievo 2 vive lì. Un documento che misura l'ansia con una scala e non guarda la depressione sta selezionando la comorbidità meno pericolosa delle due.

**Mitigazione.** Due domande PHQ-2 accanto al GAD-7, con lo stesso statuto già dichiarato — misura di percorso, non diagnosi, si scrive con la data e si manda al curante — e una quinta voce nella lettera. Non serve altro, e non sconfina: il documento ha già stabilito che il punteggio «non si traduce in un nome».

---

### 10. «Cosa non è» è un elenco di miti da smontare, non una diagnosi differenziale

**Capitolo:** «Che cos'è davvero», sezione «Cosa non è».

Le quattro voci attuali — sindrome da iperventilazione, surrene affaticato, ipocondria, problema di volontà — sono tutte corrette e tutte utili, ma tre su quattro sono credenze del paziente, non condizioni alternative. Mancano le due categorie che il DSM-5 impone di escludere **prima** di attribuire il quadro all'ansia, e sono le due che l'osteopata può realmente intercettare:

- **Disturbo d'ansia indotto da sostanze o farmaci**, inclusa la caffeina e, all'opposto, l'astinenza da alcol o benzodiazepine. Il documento nomina «caffè oltre le tre tazze o alcol serale quotidiano» nel modello Neurologico come segnale da rinviare, ma non come possibile causa sufficiente del quadro.
- **Disturbo d'ansia dovuto ad altra condizione medica** — la casella in cui stanno la TPSV del rilievo 1, l'ipertiroidismo (già nella tabella rossa), l'ILO del rilievo 3.

Sull'ipocondria: il termine è stato ritirato dal DSM-5, che lo ha distribuito fra disturbo da sintomi somatici e **disturbo da ansia di malattia**, e quest'ultimo ha una variante *care-avoidant* che descrive con precisione il paziente della frase attuale («ha smesso di cercarla perché nessuno l'ha trovata»). Così com'è, la voce nega un'etichetta usando la definizione superata di quell'etichetta.

**Mitigazione.** Aggiungere le due categorie di esclusione come voci proprie, con la condotta (chi guarda, non cosa concludi). Riformulare la voce sull'ipocondria come «non è ipocondria nel senso in cui il paziente usa la parola», nominando il disturbo da ansia di malattia e la sua variante evitante.

---

### 11. Simon 2021 è citato tre volte e il braccio yoga non compare mai

**Capitolo:** «Non è una condizione sola: i sottotipi», «La lettura osteopatica» (Comportamentale), «Perché le mani possono cambiare qualcosa» (Leva 5) e «Cosa dire al paziente».

Lo studio è a **tre bracci**: terapia cognitivo-comportamentale 70,8%, **yoga Kundalini 54,2%**, educazione allo stress 33,0%. Il documento riporta sempre e solo il primo e il terzo. Lo yoga ha superato il controllo e non ha raggiunto la non inferiorità rispetto alla CBT — che è un risultato preciso e riportabile in una riga.

**Perché è attaccabile.** È l'omissione che un lettore ostile userebbe con più profitto, perché cade nel documento che scrive, a due capitoli di distanza: *«non dire al paziente che gli studi lo confermano [...] gli studi ci sono, e chi li apre trova il contrario»*. Qui chi apre lo studio trova un intervento corporeo attivo, con un effetto reale, tolto dal riassunto proprio nel capitolo che elenca cosa il paziente può fare da solo. E ne trova un secondo motivo: il Capitolo 12 ammette tre strumenti attivi «con studi randomizzati sull'esito clinico in persone con un quadro d'ansia in corso», e questo criterio lo yoga in Simon 2021 lo soddisfa.

**Mitigazione.** Riportare i tre bracci ovunque lo studio compare, e decidere esplicitamente sullo yoga: o entra nel Capitolo 12 come quarto strumento con la sua etichetta, o si scrive perché resta fuori. La seconda opzione è legittima; il silenzio no.

---

## PREFERENZE

### 12. Il MCID del GAD-7 viene da una coorte di depressione cronica, e la provenienza non è dichiarata

**Capitolo:** Appendice A (glossario) e Mappa concettuale.

Il documento scrive «Cambiamento minimo clinicamente importante: 4 punti». Il valore è corretto (Toussaint 2020, PMID 32090765: *«MCID was estimated 4 points on the GAD-7 total score»*), ma è stato stimato su **N=261 pazienti di uno studio multicentrico sulla depressione cronica**, ancorato al miglioramento della HRSD-24, e gli autori stessi chiudono raccomandando conferma «in populations and trials focusing on anxiety-specific treatment».

Il documento applica altrove, con rigore, la regola che ogni fonte presa da un'altra popolazione porta accanto la frase che dichiara il salto. Qui non lo fa, e sarebbe la stessa formula di sempre: *il salto è di popolazione*. Una riga in glossario e una nella Mappa.

---

## REGGEREBBE SULLA MIA SCRIVANIA?

Se un mio paziente mi portasse questo documento, la prima cosa che noterei è che è verificabile: ho controllato trenta citazioni e non ne ho trovata una inventata, una capovolta o una gonfiata nella direzione comoda. È l'opposto di quello che mi aspetto da un documento osteopatico, e cambia il tono della conversazione.

Quello che mi farebbe alzare il sopracciglio è tutto nella stessa zona: **il documento sa moltissimo di respiro e pochissimo di cardiologia dei sintomi somatici**. Le palpitazioni entrano nella tabella rossa solo se c'è già una cardiopatia, e l'Holter negativo chiude una porta che l'Holter non chiude — su un quadro in cui, nella serie di Lessmeier, due terzi dei pazienti con una TPSV documentata soddisfacevano i criteri di panico. La seconda cosa è il rischio suicidario compresso in una riga con un solo destinatario, in un documento che cita tre volte lo studio in cui un quarto di quei pazienti riferiva ideazione suicidaria. La terza è che si misura l'ansia e non si guarda la depressione.

Quello che invece mi farebbe pensare che in quello studio sanno di cosa parlano è il Capitolo 11 letto al contrario: apre dicendo cosa le mani **non** fanno, cita due meta-analisi negative sul proprio operato, e le mette nel consenso informato. Non ho mai visto un documento di terapia manuale mettere nel consenso il risultato negativo della meta-analisi sulla propria disciplina. A un professionista che scrive quella riga mando pazienti.

---

## TIENE — non toccare

- **Il Capitolo 11 nella sua struttura**, e in particolare il blocco «Cosa non possono fare le mani, detto per primo» e la terza riga del consenso. È l'architrave della difendibilità dell'intero documento.
- **Il trattamento di Hornsveld 1996 in «Cosa non è»**: smontare la sindrome da iperventilazione con lo studio in doppio cieco che l'ha smontata, e togliere il termine dal vocabolario, è la scelta più matura del documento. Il rilievo 6 chiede di estenderla, non di annacquarla.
- **Le due meta-analisi negative su di sé (Gordon 2025, Hansen 2025) tenute in quattro capitoli diversi**, con la lettura corretta del dato sulla conduttanza cutanea via Vicenzino 1998. Nessuna delle due va ammorbidita.
- **La regola del marker scelto e scritto prima di trattare**, motivata con il decorso fluttuante. Il rilievo 4 le mette sotto i numeri che le mancano; l'idea è già giusta.
- **Il divieto della manovra di provocazione dell'iperventilazione** e la riga di consenso sulla riproduzione in seduta delle sensazioni temute. Sono le due protezioni specifiche di questa condizione, e sono entrambe al posto giusto.

---

## MATERIALE FUORI PERIMETRO

Nessuno. Ho cercato tecniche, dosi, sequenze e piani di seduta: non ce ne sono. I parametri che compaiono sono parametri **di studio** (le quattro settimane di riaddestramento in Meuret 2008, le sei atti al minuto di Joseph 2005), attribuiti e al passato, e ogni strumento del Capitolo 12 si chiude con la riga «come e quando consegnarlo al tuo paziente sta nella Procedura». Il confine è tenuto con precisione.

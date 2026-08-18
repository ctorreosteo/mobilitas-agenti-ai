# Feedback — Revisore Fisioterapista Evidence-Based

**Documento revisionato:** `procedure-generate/["stitichezza"]/v1-draft.md` (v1.0) e la relativa `v1-scheda.md`.

**LENTE:** Fisioterapista Evidence-Based
**CONDIZIONE:** Stitichezza cronica funzionale

---

## RICERCA SVOLTA

Ho recuperato via NCBI E-utilities gli abstract integrali di **tutte e undici** le fonti citate dalla procedura: Huang 2025 (PMID 39531948), McClurg 2018/AMBER (30375324), Lämås 2009 (19217105), Orhan 2020 (32893023), Belvaux 2017 (28215390), Barba & Azpiroz 2015 (25500424), Chiarioni 2006 (16530506), Bharucha & Lacy 2020 (31945360), McClurg 2016/Parkinson (26826459), Boas Fernandes 2023 (37301564), Trieu 2023 (36989181). **Nessuna citazione è inventata; PMID, riviste, volumi e pagine corrispondono tutti.** È un risultato raro e va detto.

Ho poi cercato due aree che la procedura tocca senza sostenere: la **reliability della palpazione di mobilità sacro-iliaca** (Ribeiro 2021, *J Manipulative Physiol Ther* 44(4):307-318, PMID 33896601 — 28 studi, κ inter-esaminatore da −0,05 a 0,77, nessuno studio ha verificato la validità concorrente) e l'**esercizio nella stitichezza** (Gao 2019, *Scand J Gastroenterol* 54(2):169-177, PMID 30843436 — 9 RCT, 680 partecipanti, RR 1,97 IC 1,19-3,27, I²=91%, alto rischio di bias).

Gli errori che seguono **non** sono citazioni fasulle: sono tre punti in cui il numero riportato non è quello che la fonte dice, o è attribuito a qualcosa di diverso.

---

## ERRORI

### E1 — Il CSS non era l'outcome primario di AMBER

**Sezione:** Parte II §4 "Monitoraggio del risultato", primo punto.

**Problema.** La procedura scrive del Constipation Scoring System: *"È la scala usata dalla nostra ancora come outcome primario."* È falso, ed è verificabile in una riga di abstract. In AMBER (McClurg 2018, *Health Technol Assess* 22(58), PMID 30375324) il testo è esplicito: *"The primary outcome was the difference between the intervention and control groups in change in the **NBD score** from baseline to week 24. **Secondary outcomes** were measured via a bowel diary, adherence diary, **the Constipation Scoring System**, patient resource questionnaire and the EQ-5D-5L."* Il CSS era un secondario. Peggio: la procedura **si contraddice da sola**, perché nella tabella dei 5 studi cardine (Parte II) riporta correttamente *"Outcome primario non significativo (NBD score, p=0,056)"*. È l'unico punto del documento in cui una fonte viene fatta dire una cosa che non dice, e sta nella sezione che il junior usa per giustificare la scelta della scala davanti al medico inviante.

**Correzione.** Sostituire con: *"CSS (Agachan-Wexner, 0-30): outcome **secondario** in AMBER, dove il primario era il NBD score — una scala per disfunzione intestinale neurogena, non trasferibile alla stitichezza funzionale. Lo usiamo perché è validato sulla stitichezza cronica e copre gli otto item che ci servono, non perché lo abbia usato McClurg come endpoint principale."*

---

### E2 — Il +1,59 evacuazioni/settimana non è l'effetto del massaggio orario che insegniamo

**Sezione:** Parte 0 (modello Biomeccanico-Strutturale, "Evidenza/scope"); Parte I (dominanza biomeccanico-viscerale); Parte II (tabella studi cardine); Scheda §5.

**Problema.** La procedura attribuisce il **+1,59 ev/settimana** di Huang 2025 al *"massaggio addominale sul percorso del colon"*, cioè esattamente alla tecnica che poi prescrive (*"massaggio colico profondo in senso orario"*, 10-15 min/die). Ma quel MD è la **stima aggregata di tutte le tecniche di massaggio addominale** incluse nella meta-analisi, e la stessa meta-analisi contiene un'analisi per sottogruppo di tecnica che la procedura non riporta:

> *"Acupressure and aromatherapy massage had a greater effect on defecation frequency (SMD = 1.63; 95% CI 1.06, 2.21) than **circular massage (SMD = 0.90; 95% CI 0.57, 1.22)** or electric device massages (SMD = 0.83)."*

Il **massaggio circolare — il nostro — è il meno efficace dei tre nel dato che stiamo citando.** Vendere il pooled +1,59 come l'effetto atteso della manovra insegnata è evidenza gonfiata per selezione del sottogruppo favorevole: è precisamente il vizio che la procedura dichiara di voler evitare ("nessun claim gonfiato: è questo il lucchetto"). Nota accessoria dello stesso lavoro: il MD −21,53 h sul tempo di transito poggia su **df = 3, cioè quattro sole comparazioni**, con IC da −35,94 a −7,12 e I² 65%; la procedura lo usa in "Cosa fa l'osteopatia che il lassativo non fa" come uno dei tre pilastri, senza dire su quanti studi si regge. E la revisione include **studi quasi-sperimentali oltre agli RCT**, cosa mai dichiarata.

**Correzione.** Nei tre punti in cui compare il numero, scrivere: *"Huang 2025 stima +1,59 ev/settimana sull'insieme delle tecniche di massaggio addominale; il sottogruppo del **massaggio circolare** — quello che insegniamo — ha l'effetto più piccolo (SMD 0,90; IC 0,57-1,22). È comunque un effetto reale, ma è questo il numero nostro, non il +1,59."* Aggiungere in tabella: *"−21,5 h di transito su sole 4 comparazioni; revisione di RCT **e** studi quasi-sperimentali."*

---

### E3 — Belvaux 2017 è riportato solo per i risultati positivi, e metà del campione è la popolazione che diciamo di inviare

**Sezione:** Parte 0 (Biomeccanico); Parte I ("Cosa fa l'osteopatia…"); Parte II, tabella studi cardine, riga Belvaux.

**Problema.** Due omissioni nello stesso studio, che è **l'unico dato strumentale osteopatico** dell'intera procedura e quindi il più esposto.

1. **Selezione dei risultati.** La procedura elenca: *"transito oro-anale e colico destro/sinistro ridotti, frequenza e Bristol aumentati, punteggio KESS migliorato, meno dolore e gonfiore"*. Tutto vero. Ma l'abstract prosegue con una frase che la procedura non riporta: *"After OMT, **the intensity of constipation, and the Patient assessment of constipation symptoms score did not change**"*. Cioè: il transito strumentale è migliorato e i due **outcome riferiti dal paziente sulla stitichezza in quanto tale (PAC-SYM e intensità) sono rimasti fermi.** In uno studio non controllato, questa dissociazione è l'informazione più interessante del lavoro, e va nella direzione opposta a quella per cui è citato. Tacerla è cherry-picking su un pilota n=21.
2. **Popolazione.** *"Eleven patients had FC and 10 DD, as defined by Rome III criteria"*: **10 dei 21 avevano un disturbo defecatorio**, esattamente la categoria che la procedura classifica come *"Efficacia VARIABILE — coadiuvante, con invio"* e per cui ordina manometria e biofeedback. L'unico dato strumentale a sostegno del nostro lavoro è quindi per metà raccolto sui pazienti che diciamo di non trattare da soli.

**Correzione.** Riscrivere la riga della tabella: *"Belvaux 2017 — pilota **non controllato**, n=21 donne (11 stitichezza funzionale, **10 disturbo defecatorio**). Dopo OMT: transito oro-anale e colico ridotti, frequenza e Bristol aumentati, KESS migliorato; **ma intensità della stitichezza e PAC-SYM invariati**. Genera ipotesi, non prova efficacia — e metà del campione è la popolazione che noi inviamo."*

---

## RISCHI

### R1 — Barba 2015 è "eccellente" su una popolazione che non è la nostra, e la correzione è n=15

**Sezione:** Parte 0 (Respiratorio-Circolatorio, *"qui c'è un meccanismo di ottima qualità"*); Parte I (*"Meccanismo documentato in modo eccellente"*); Parte III §2; Parte IV, Sistema Respiratorio.

**Perché è attaccabile.** Il dato è riportato con precisione (contrazione diaframmatica +19% EMG e discesa 12±2 mm; girth −25±3 mm dopo biofeedback: tutto verificato). Il problema è a chi si applica. La coorte di Barba è di **45 pazienti con disturbi funzionali intestinali: 27 IBS-C, 15 gonfiore funzionale, 3 IBS alternante.** Nessun paziente con stitichezza cronica funzionale Rome-definita. E il braccio che dimostra la correggibilità è **n=15, mediana 2 sedute**, con controllo intra-soggetto (11 pazienti, una sessione di controllo pre-trattamento) — non un RCT. Su questo poggiano la metafora della siringa, il modello del torchio e l'intero blocco B della seduta. Un gastroenterologo apre l'abstract e vede "irritable bowel syndrome with constipation": la parola "eccellente" cade in dieci secondi, e con essa la credibilità delle qualificazioni oneste fatte altrove.

**Mitigazione.** Declassare l'aggettivo e dichiarare popolazione e numerosità: *"Barba 2015: meccanismo ben documentato della **distensione addominale funzionale** in pazienti con IBS-C e gonfiore funzionale (n=45; TC n=39, EMG n=32). Il braccio di correzione è **n=15 con biofeedback EMG**. La trasferibilità alla stitichezza funzionale pura è un'estrapolazione ragionevole, non un dato."* Mantenere — perché è già corretto — il vincolo che l'effetto atteso della rieducazione respiratoria è sul **gonfiore**, non sul transito.

---

### R2 — La palpazione è chiamata "parametro oggettivo", e sulla sacro-iliaca non lo è

**Sezione:** Parte 0, "Il metodo in tre mosse" §3 (*"rivaluti gli altri con un parametro oggettivo"*); Parte II §3, test 2 (*"È il parametro oggettivo del re-test respiratorio"*) e test 4 (mobilità sacro-iliaca, nutazione/contronutazione); Scheda §3.

**Perché è attaccabile.** L'intera architettura decisionale — individuazione del modello dominante, "prova della chiave di volta", bivio della 3ª seduta — è ancorata a misure palpatorie definite "oggettive": escursione diaframmatica alle coste basse, dolorabilità del punto colico, asimmetria sacro-iliaca. Sulla mobilità sacro-iliaca la letteratura è netta e sfavorevole: Ribeiro 2021 (*JMPT* 44(4):307-318, PMID 33896601), revisione sistematica di 28 studi e 15 test palpatori, riporta **κ inter-esaminatore da −0,05 a 0,77** e — dato decisivo — ***"No study included in this systematic review verified the concurrent validity of the tests."*** Un test senza validità concorrente verificata e con concordanza che scende sotto il caso non è un parametro oggettivo: è un'impressione riproducibile a volte dallo stesso operatore. È l'unico punto in cui questa procedura, altrove scrupolosa, usa il vocabolario della misurazione per qualcosa che non è misurato.

**Mitigazione.** Tre righe. (1) Sostituire ovunque "parametro oggettivo" con **"parametro di re-test, riproducibile dallo stesso operatore nella stessa seduta"**. (2) Aggiungere in Parte II §3, test 4: *"La palpazione di mobilità sacro-iliaca ha reliability inter-esaminatore da scarsa a discreta (Ribeiro 2021) e nessuna validità concorrente verificata: non può essere il solo criterio con cui scegli il dominante."* (3) Ancorare esplicitamente la decisione del bivio della 3ª seduta ai **numeri del diario** (evacuazioni/settimana, Bristol, sforzo 0-10) — le uniche misure del documento con proprietà metriche — e non alla palpazione.

---

### R3 — L'ancora scientifica ha come studio di punta un trial in SM, cioè nella popolazione che la procedura classifica "Efficacia NULLA"

**Sezione:** Intestazione; Parte I (tabella efficacia per eziologia, riga "secondaria/neurogena"); Parte II, tabella studi cardine e "Perché McClurg è la nostra garanzia".

**Perché è attaccabile.** Tre pieghe che un collega informato mette insieme in un minuto.

1. **Popolazione.** AMBER è su **disfunzione intestinale neurogena in sclerosi multipla**, e Parte I scrive: *"Stitichezza secondaria, a transito lento severa, **neurogena** o con red flag (**Efficacia NULLA — Invio**)"*. Il documento nomina "ancora scientifica" un'autrice il cui trial più grande è nella popolazione che il documento stesso esclude. La tabella dice "in SM", ma l'intestazione e la sezione "garanzia" no.
2. **Coerenza con Huang.** La procedura cita correttamente che nel sottogruppo neurogeno l'effetto è il più piccolo (SMD 0,68 vs 1,23 funzionale). Se l'effetto è minore proprio lì, non si può usare quella popolazione come vetrina metodologica per la stitichezza funzionale senza dichiarare il salto.
3. **Numeri e omissioni.** I secondari citati sono esatti (+0,62 ev/settimana, **IC 0,03-1,21**; +1,08 svuotamenti completi, IC 0,41-1,76) ma vengono da un trial che ha **mancato il primario**, con secondari multipli non corretti per molteplicità, e il limite inferiore dell'IC sulla frequenza è 0,03 evacuazioni/settimana — clinicamente nullo. Non è citato che l'analisi costo-utilità ha trovato l'intervento **dominato dal controllo** (−0,002 QALY, +£56,50).

Segnalo per contro che la sicurezza è affermata con una fonte che dice il contrario di quel che serve: Parte I scrive *"Nella patologia neurologica il massaggio ha buon profilo di sicurezza"* citando Huang, ma Huang scrive *"No adverse reactions were observed in the **non-neurogenic** bowel dysfunction group"* — cioè restringe l'assenza di eventi avversi proprio ai **non** neurogeni. L'affermazione regge su AMBER ("No adverse events were reported"), non su Huang: va spostata la fonte.

**Mitigazione.** In intestazione e in "Perché McClurg è la nostra garanzia" aggiungere una riga: *"AMBER è un trial in sclerosi multipla. Ci ancoriamo a McClurg per il **metodo** — la scala completa dell'evidenza su una singola tecnica, compresi i risultati scomodi — non perché il suo trial sia sulla nostra popolazione: la trasferibilità alla stitichezza funzionale è un'assunzione dichiarata."* Riportare l'IC del +0,62 e una riga sull'analisi economica. Spostare la citazione sulla sicurezza in neurologico da Huang ad AMBER.

---

### R4 — L'esercizio è dichiarato "leva a più alta evidenza" e resta l'unica prescrizione senza dose

**Sezione:** Parte 0 (Metabolico-Energetico); Parte IV, tabella di raccordo (*"si esercita come counseling e segnalazione"*); "Esercizi a casa"; Scheda §5.

**Perché è attaccabile.** La procedura scrive che il modello metabolico governa *"le leve a più alta evidenza dell'intero quadro"* e vi include l'**attività fisica** — poi non le assegna mai una dose, mentre assegna una dose precisa a tutto il resto (auto-massaggio 10-15 min × 1/die; respirazione 5 min × 2/die; quadrupedia 10 rip × 2/die; 5 minuti massimi sul WC). Il risultato è che la leva dichiarata più forte è l'unica lasciata a "movimento" generico. Per un fisioterapista è il buco più visibile del documento, perché è il terreno su cui saremmo d'accordo. Esiste evidenza citabile, imperfetta ma reale: Gao 2019 (*Scand J Gastroenterol* 54(2):169-177, PMID 30843436), 9 RCT e 680 partecipanti, **RR 1,97 (IC 1,19-3,27)** sul miglioramento sintomatico, sottogruppo aerobico RR 2,42 — con I²=91% e alto rischio di bias dichiarato dagli autori. Nota che questo non sconfina nel prescrittivo medico: camminare non è una terapia farmacologica, e la procedura già prescrive esercizi.

**Mitigazione.** Aggiungere un sesto punto in "Esercizi a casa" e in Scheda §5: *"**Cammino o attività aerobica leggera** — 20-30 min, 5 giorni/settimana (≈140 min/sett.), preferibilmente al mattino. Evidenza modesta e a rischio di bias elevato (Gao 2019: RR 1,97 sul miglioramento sintomatico, I² 91%), ma è a costo zero, agisce sulla leva che la Parte 0 dichiara la più forte, e senza una dose scritta il paziente non la fa."*

---

## PREFERENZE

### P1 — Trieu 2023: dire "espulsione simulata", non "espulsione"

**Sezione:** "Esercizi a casa", punto routine/posizione; Scheda §5.

La procedura scrive che lo sgabello *"non ha migliorato l'espulsione in uno studio randomizzato su costipati non selezionati"*. Il verdetto è corretto e l'uso di uno studio **negativo** contro un gadget popolare è merito, non difetto. Solo: Trieu 2023 ha misurato **tre test di espulsione del palloncino in ordine randomizzato** in 41 pazienti in un'unica sessione di laboratorio (*"did not improve subjective or objective measures of **simulated defecation**"*), non la defecazione reale nel tempo. Un sostenitore dello sgabello obietterà che un test di palloncino in seduta singola non esclude un beneficio su settimane d'uso. Basta una parola: *"non ha migliorato l'**espulsione simulata** (test del palloncino) in un crossover randomizzato…"*. La conclusione operativa — "prova individuale, non regola" — resta identica e diventa inattaccabile.

### P2 — Rome IV reso in modo impreciso, e manca la distinzione IBS-C

**Sezione:** Parte II §1, primo criterio di inclusione.

Due imprecisioni, entrambe a basso impatto perché la procedura dichiara esplicitamente *"non li applichi per diagnosticare"*. (a) Il qualificatore *"in più di un quarto delle defecazioni"* è messo a coprire tutta la lista, ma non si applica al criterio **"meno di tre evacuazioni spontanee a settimana"**, che in Rome IV è assoluto. (b) Mancano i due criteri accessori obbligatori: feci molli raramente presenti senza lassativi, e **criteri insufficienti per la sindrome dell'intestino irritabile**. Il secondo non è solo formale: la procedura non distingue mai **IBS-C** da stitichezza funzionale, pur citando Barba (coorte in larga parte IBS-C) e Chiarioni (stitichezza a transito normale da dissinergia). Sono binari gestionali diversi, e nel paziente con dolore addominale prevalente il messaggio "meno gonfiore, meno sforzo" va calibrato diversamente. Una riga in Parte II basterebbe.

---

## TIENE

**Non toccare queste parti — sono il motivo per cui il documento regge.**

- **La gestione di Boas Fernandes 2023 (PMID 37301564) è esemplare e va lasciata parola per parola.** La procedura anticipa e smonta da sola l'unica citazione che circola gonfiata come "prova della manipolazione viscerale nella stitichezza", notando che gli outcome erano dolore e disabilità lombare. Verificato: primari = NRS dolore e Oswestry. Un revisore che si autodenuncia una citazione abusabile prima che lo faccia un altro è raro.
- **Il paragrafo sul vago è corretto e — cosa più importante — è usato per restringere i claim, non per espanderli.** "Il sub-occipitale non è un accesso al sigma" e il richiamo alla via parasimpatica sacrale (S2-S4) eliminano in anticipo la sciocchezza più diffusa dell'osteopatia viscerale. Lo stesso vale per il rifiuto esplicito dei "meccanismi neuroendocrini" a favore di "down-regulation aspecifica, non una nostra esclusiva".
- **Chiarioni 2006 è riportato in modo impeccabile** (43/54, 80% vs 12/55, 22%; beneficio a 24 mesi) e la regola che ne discende è quella giusta: davanti alla dissinergia si **cede il caso** al trattamento superiore invece di competerci. È la scelta più difficile del documento ed è quella corretta.
- **"Non promettere mai la riduzione dei lassativi"** è sostenuto esattamente dalle due fonti citate (Huang: OR 0,43, p=0,15; Lämås: nessuna differenza a 8 settimane, *"complement to laxatives rather than a substitute"*), ed è ripetuto in intestazione, in Parte I e in chiusura di scheda. Perfetto.
- **La distinzione fra la mano dell'osteopata e quella del paziente** ("Distingui la mano tua da quella del paziente… la tua seduta settimanale non è ciò che è stato testato") è l'osservazione metodologicamente più acuta del documento, e ribalta correttamente la gerarchia mettendo l'auto-massaggio quotidiano al centro. Nessun altro documento osteopatico che ho letto ammette questo.
- **Le etichette "PLAUSIBILE non dimostrato" / "razionale meccanico, non efficacia provata" sul lavoro viscerale, mesenterico e sacrale sono integrità, non debolezza.** Il ragionamento del dominante è dichiarato ipotesi di lavoro e non venduto come provato: non chiedo di rimuoverlo. Chiedo solo, in Parte 0 §3, di correggere il **verbo** — *"Se cedono anche loro, **hai trovato** la lesione primaria"* → *"…il quadro **è compatibile con l'ipotesi** che quello sia il livello primario"*. È l'unica riga in cui il motore clinico scivola dall'ipotesi al fatto.

---

## VERDETTO

**Da correggere.**

Tre errori verificabili — il CSS attribuito come outcome primario di AMBER, il +1,59 attribuito alla tecnica che nella stessa meta-analisi rende meno, e Belvaux riportato senza i suoi due esiti negativi — sono tutti concentrati sui numeri che il documento usa per difendersi, e sono tutti riparabili in mezza giornata senza toccare l'impianto. Il resto è la procedura osteopatica meglio referenziata che mi sia capitato di revisionare: zero citazioni inventate su undici verificate, il trattamento con la migliore evidenza (biofeedback) esplicitamente ceduto a chi lo fa meglio, e la propria evidenza principale onestamente attribuita al paziente invece che alle proprie mani. Correggete i tre numeri e questo documento regge davanti a un gastroenterologo.

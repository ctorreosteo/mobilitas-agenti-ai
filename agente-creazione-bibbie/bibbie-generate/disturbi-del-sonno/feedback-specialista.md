# Feedback — Revisore Medico Specialista

**LENTE:** Medico Specialista — medico del sonno (in Italia: neurologo o pneumologo con competenza in medicina del sonno; la condizione non è in tabella e dichiaro io la specialità)
**CONDIZIONE:** disturbi del sonno / insonnia cronica dell'adulto
**DOCUMENTO REVISIONATO:** `bibbie-generate/disturbi-del-sonno/v1-bibbia.md` (v1, 31 agosto 2026), con la Mappa `v1-mappa.md` come riscontro.

---

## RICERCA SVOLTA

Ho verificato in questa sessione, tramite le API NCBI E-utilities, **tutte e 34 le fonti** dell'Appendice B: titolo, rivista, anno, numerosità e risultato letto nell'abstract. Ho controllato le due linee guida di riferimento (European Insomnia Guideline 2023, PMID 38016484, e AASM 2021, PMID 33164742) recuperando l'elenco completo delle raccomandazioni e dei gradi. Ho verificato la storia naturale (Morin 2009), l'epidemiologia (Ohayon 2002), le soglie dell'ISI (Morin 2011 e Yang 2009), lo STOP-Bang (Nagappa 2015), e ho letto per esteso gli studi su cui il documento appoggia le proprie leve (Popovich 2024, Li 2014, Stieven 2020, Gordon 2025, Yao 2023, Mazzeo 2020). Ho poi cercato la letteratura che il documento **non** cita e che avrebbe dovuto: menopausa, nicturia, rischio suicidario nell'insonnia, ipersonnie centrali, normativa italiana su apnee e idoneità alla guida.

**Esito dell'audit delle citazioni: nessun PMID inventato, nessun risultato gonfiato.** Tornano anche i numeri più facili da sbagliare — le 10,4 volte di Asih 2014, il −3,05 con d = −0,74 di HABIT, il valore predittivo negativo del 46% dello STOP-Bang, gli 8,4 punti dell'ISI, i 7,06 minuti della melatonina, il «did not confirm that HRV was reliably impaired» di Zhao 2023. È la parte del documento su cui non ho niente da dire, ed è raro.

I rilievi che seguono riguardano quindi **quello che manca**, non quello che è scritto male.

---

## ETICHETTE DA CORREGGERE

**1. «Cosa può fare il paziente da solo» — Strumento 1, il movimento nella giornata**
Affermazione: l'esercizio come strumento autogestito. Etichetta attuale: **DIMOSTRATO**. Etichetta corretta: **PROBABILE**.
Perché: la linea guida europea lo colloca fra le terapie *aggiuntive* con grado **B**, non A (Riemann 2023, PMID 38016484 — verificato); l'unico studio randomizzato su pazienti con insonnia ha **17** partecipanti (Reid 2010, PMID 20813580 — verificato: 17 adulti sedentari, età media 61,6 anni); la sintesi di 66 studi riguarda popolazioni miste e per l'esercizio *regolare* riporta benefici **piccoli** su durata ed efficienza (Kredlow 2015, PMID 25596964 — verificato). La glossa che il documento mette sotto l'etichetta dice esattamente questo: la glossa contraddice l'etichetta che le sta sopra.

**2. «Cosa si rompe» — Meccanismo 2, il letto ha imparato a significare veglia**
Affermazione: il condizionamento del letto come meccanismo. Etichetta attuale: **DIMOSTRATO**. Etichetta corretta: **spezzata** — DIMOSTRATO per l'efficacia del pacchetto cognitivo-comportamentale, **PROBABILE** per il condizionamento come causa.
Perché: la prova addotta è un'inferenza dalla risposta al trattamento («un meccanismo di cui si smonta con successo l'anello centrale è un meccanismo verificato»), non una misura del meccanismo. E il controllo dello stimolo nella AASM 2021 è **raccomandazione condizionale**, non forte: forte è solo la CBT-I multicomponente (verificato sull'abstract della linea guida). Il documento dichiara «condizionale» accanto al rilassamento in «Cosa può fare il paziente da solo» e lo tace qui, sulla stessa fonte: è una disclosure selettiva, ed è il tipo di asimmetria che un medico nota subito.

**3. «Cosa si rompe» — Meccanismo 4, e le due riprese in «I cinque modelli» (Metabolico-Energetico) e in «Come ragiono davanti a questo paziente»**
Affermazione: «chi aveva insonnia e lo stile di vita migliore si è fermato a 1,56, con **un intervallo che sfiora l'unità**».
Perché: verificato su Nordstoga 2024 (PMID 38241943), l'intervallo di confidenza è **0,97–2,50**, cioè **contiene** l'unità: il risultato non è statisticamente significativo. «Sfiora» trasforma un non-significativo in un quasi-significativo, e su quel confronto poggia il DIMOSTRATO del modello metabolico.
Correzione: scrivere l'intervallo per esteso e la parola «non significativo». Il DIMOSTRATO del modello metabolico regge sul braccio con lo stile di vita peggiore (3,57; IC 2,65–4,80), non sul contrasto fra i due.

**4. «Le strutture in gioco» e «Cosa si rompe» — Meccanismo 5, la mandibola che segue il risveglio**
Affermazione: l'attività ritmica dei masticatori segue il micro-risveglio. Etichetta attuale: **DIMOSTRATO**, retto da un solo studio con **8 bruxisti e 8 controlli** e con risvegli **evocati** sperimentalmente (Kato 2003, PMID 12651932 — verificato).
Perché: la direzione è corretta e io la confermo, ma non su quello studio da solo. Va affiancata la replica sui risvegli spontanei: Kato T, Rompré P, Montplaisir JY, Sessle BJ, Lavigne GJ, *Sleep bruxism: an oromotor activity secondary to micro-arousal*, J Dent Res 2001 — **PMID 11706956**, verificata in questa sessione: 10 bruxisti e 10 controlli, aumento dell'attività EEG corticale quattro secondi prima dell'inizio dell'attività sopraioidea nel **79%** degli episodi. Con quella fonte in riga il DIMOSTRATO regge; senza, l'etichetta corretta è PROBABILE.

---

## ERRORI

**1. Manca l'intera diagnosi differenziale medica e farmacologica dell'insonnia.**
Capitolo: «Che cos'è davvero» (sezione *Cosa non è*), con riflesso su «Dove finisce il nostro campo».

L'elenco copre apnea ostruttiva, gambe senza riposo, disturbo del ritmo circadiano, depressione e il costrutto del «surrene affaticato». Non c'è una riga su: **sintomi vasomotori della menopausa**, **nicturia**, **ipertiroidismo**, **reflusso e asma notturni**, e **farmaci che causano insonnia** (corticosteroidi, beta-agonisti, SSRI e SNRI, levotiroxina in eccesso, stimolanti, diuretici assunti la sera).

È l'omissione più costosa del documento perché quello che manca è una **conoscenza**: l'osteopata non saprà di doverla cercare, e attribuirà al meccanismo 1 — o al proprio reperto — un risveglio che ha una causa medica correggibile. L'aggravante è interna al testo: il paziente-vetrina di «Come ragiono davanti a questo paziente» è **«la donna di 52 anni che si sveglia alle tre»**, cioè l'età e la presentazione da manuale dell'insonnia perimenopausale.

Prova: Maki PM, Panay N, Simon JA, *Sleep disturbance associated with the menopause*, Menopause 2024, **PMID 38916279** (verificato): i disturbi del sonno sono fra i sintomi più comuni e invalidanti della transizione menopausale, con risvegli notturni frequenti e aumento del tempo sveglio dopo l'addormentamento, e derivano anche dai sintomi vasomotori. Sul secondo fronte: il risveglio ricorrente alle tre in un adulto sopra i cinquanta è, prima che iperattivazione, nicturia — nella meta-analisi su 5.396 anziani l'odds di nicturia in chi ha insonnia è **1,96 (IC 1,61–2,38)** (Verbakel et al., Minerva Urol Nephrol, **PMID 37955855**, verificato), e nei 1.424 soggetti fra 55 e 84 anni la nicturia è indicata come causa del sonno disturbato «quasi ogni notte» dal **53%** del campione, oltre quattro volte più del dolore che si ferma al 12% (Bliwise et al., Sleep Med 2009, **PMID 18703381**, verificato).

Correzione: aggiungere in *Cosa non è* un blocco «insonnia in comorbilità medica e da farmaci» con menopausa, nicturia, tiroide, reflusso e asma notturni, e la lista dei farmaci insonnizzanti; e in «Dove finisce il nostro campo» una riga che dica che l'elenco dei farmaci in corso si **raccoglie e si trasmette al curante senza commentarlo** — perfettamente coerente con la regola sul confine di atto che il documento ha già scritto bene.

**2. La riga sui pensieri di morte è sotto-classificata.**
Capitolo: «Dove finisce il nostro campo», tabella delle bandiere rosse, Blocco A (e identica nella Mappa).

Una sola riga — «Pensieri di morte o autolesivi | Medico curante | Urgente» — copre due situazioni cliniche diverse: il pensiero di morte passivo e l'ideazione suicidaria attiva con piano o intenzione. Mandare a casa da solo, con un invio «urgente» al curante, un paziente con ideazione attiva non è difendibile, e l'insonnia non è un contesto neutro in cui farlo.

Prova: nella meta-analisi su 39 studi e 147.753 soggetti, il disturbo del sonno è associato a ideazione suicidaria, tentativo e suicidio con rischi relativi da **1,95 (IC 1,41–2,69)** a **2,95 (IC 2,48–3,50)** negli studi non aggiustati, e la depressione non modera la relazione (Pigeon WR, Pinquart M, Conner K, *Meta-analysis of sleep disturbance and suicidal thoughts and behaviors*, J Clin Psychiatry 2012, **PMID 23059158**, verificato).

Correzione: spezzare la riga in due, restando dentro il vocabolario chiuso dei tempi. *Ideazione suicidaria attiva, con piano o intenzione, o autolesionismo recente* → **112**, e il paziente non lascia lo studio da solo. *Pensieri di morte passivi* → Medico curante, **Urgente**, con comunicazione scritta lo stesso giorno e verifica che il contatto sia avvenuto. Aggiornare identicamente la Mappa, che porta la stessa riga.

**3. «Colpi di sonno alla guida»: manca la frase da dire al paziente, e manca il quadro normativo italiano.**
Capitolo: «Dove finisce il nostro campo», Blocco A e la sezione *Come si leggono tre righe, per esteso*.

Il documento riconosce che è l'unica riga che riguarda la sicurezza di terzi e che non ammette un ciclo «intanto che aspetta»: bene. Ma non contiene l'unica cosa che protegge davvero nell'intervallo fra la seduta e la visita, cioè **dire al paziente di non mettersi alla guida finché non è stato valutato**. E il lettore non sa che in Italia questa non è una raccomandazione di buon senso ma una materia regolata: il **DM 22 dicembre 2015**, in vigore dal 28 gennaio 2016, recepisce la direttiva **2014/85/UE** e introduce l'apnea ostruttiva con sonnolenza diurna grave e non controllata fra le condizioni che vincolano rilascio e rinnovo della patente; il **decreto dirigenziale 3 febbraio 2016** ne definisce l'accertamento dell'idoneità. Un osteopata che ignora l'esistenza di quel percorso tratta la riga come un consiglio.

Correzione: aggiungere alla riga, per esteso come già si fa per le altre tre, la frase da dire al paziente e il rimando normativo — chiarendo che il giudizio di idoneità non è dell'osteopata e che il suo compito si esaurisce nell'informare e nel mandare.

---

## RISCHI

**1. Manca la domanda che separa il dolore notturno dalle gambe senza riposo.**
Capitolo: «Cosa si rompe» (Meccanismo 4) e «Come ragiono davanti a questo paziente» (Road Map).
Il paziente di «Chi ti trova davanti» dice *«non trovo la posizione, mi giro venti volte»*, e il documento lo instrada al meccanismo 4 — il pattern in cui dichiara di poter fare «molto». La sindrome delle gambe senza riposo si presenta esattamente così, è un cancello dichiarato dal documento stesso, e nella tabella delle bandiere sta nel tier più basso («Invio»). La domanda discriminante esiste nel testo (peggiora da fermo, migliora muovendosi, ritmo serale) ma non è mai agganciata al punto in cui si decide: la Road Map ha *«ti svegli perché fa male?»* e non ha questa.
Mitigazione: portare la domanda dentro la Road Map, accanto alla domanda 3, e dentro *Come si vede addosso al paziente* del meccanismo 4, come esclusione obbligatoria prima di dichiarare quel pattern.

**2. La sonnolenza diurna è insegnata solo come segnale di apnea, e manca la regola che la governa.**
Capitolo: «Che cos'è davvero» (*Cosa non è*) e «Non è una condizione sola: i pattern».
Il documento possiede già il dato che serve — nel meccanismo 1 scrive che l'insonne «non si addormenta neanche facendo un pisolino» — ma non lo converte mai nella regola clinica: **stanchezza sì, sonnolenza no; chi si addormenta di giorno non ha un'insonnia semplice e va guardato altrove.** Altrove significa anche narcolessia e ipersonnie centrali, che nel documento non compaiono in nessuna forma e che hanno un ritardo diagnostico misurato in anni, con l'insonnia e la depressione fra le etichette sbagliate più frequenti.
Mitigazione: una riga in *Cosa non è* e la regola esplicita nella Road Map. Costa tre righe e chiude un buco di riconoscimento.

**3. Lo studio di Stieven è di puntura secca, e il documento lo chiama «un intervento locale».**
Capitolo: «I cinque modelli» (Biomeccanico-Strutturale) e «Perché le mani possono cambiare qualcosa» (Meccanismo 4).
Verificato (PMID 32272030): il titolo è *Dry Needling Combined With Guideline-Based Physical Therapy Provides No Added Benefit in the Management of Chronic Neck Pain*, 116 pazienti, e la qualità del sonno è effettivamente fra gli esiti secondari a 1, 3 e 6 mesi — quindi l'attribuzione del risultato **non** è inventata, e questo va detto. Ma un ago non è un intervento manuale, e il documento stesso ricorda che l'osteopatia è definita da tecniche «esclusivamente manuali, non invasive ed esterne»: un risultato negativo ottenuto con un ago non è una prova contraria sul nostro gesto. Il rischio qui non è di gonfiare — è di sembrare evasivi proprio nel capitolo dove il documento costruisce la propria credibilità sulla trasparenza delle fonti.
Mitigazione: nominarlo per quello che è («puntura secca aggiunta alla fisioterapia») e declassarlo da «prove contrarie» a «prova indiretta, su un intervento diverso dal nostro».

---

## PREFERENZE

1. **«Cosa dice la scienza» — Popovich 2024.** Verificato: dopo una sola seduta si riducono **sonno e ansia**; al termine dell'intervento resta significativo il **dolore** (effetto di 0,8 deviazioni standard). Il documento scrive che al termine «la differenza ancora significativa riguardava dolore e ansia»: l'ansia va tolta, o confermata sul testo integrale invece che sull'abstract.
2. **«Dove finisce il nostro campo».** La soglia che fa partire il canale medico — «un ipnotico in corso da più di quattro settimane» — coincide esattamente con il limite di uso breve che la linea guida europea pone per benzodiazepine, agonisti del recettore benzodiazepinico e daridorexant (≤ 4 settimane, grado A). Scriverlo in riga trasforma una soglia interna in una soglia citabile davanti al curante.

---

## REGGEREBBE SULLA MIA SCRIVANIA?

Sì, con tre correzioni. Se un mio paziente me lo portasse, la prima cosa che mi alzerebbe il sopracciglio è che la donna di 52 anni che si sveglia alle tre venga spiegata con l'iperattivazione corticale e mai con le vampate: è l'ipotesi che un ginecologo o un medico del sonno fa per prima, e la sua assenza mi farebbe dubitare che chi ha scritto sappia dove finisce il territorio dell'insonnia primaria. La seconda è la riga sui pensieri di morte mandata al curante come «urgente». La terza è la guida, dove manca la frase che protegge il paziente e i terzi nelle settimane di attesa.

Quello che invece mi farebbe pensare che in quello studio sanno di cosa parlano è la frase «nessuna delle due ancore lavora in terapia manuale, e su questa condizione un'ancora di terapia manuale non esiste», seguita dalla decisione di citare comunque Zhao, Li e Gordon — cioè le tre fonti che smontano la spiegazione più comoda. E la riga sulla terapia ipnotica, detta prima che il paziente la chieda. Un documento che si toglie da solo il tappeto da sotto i piedi è un documento con cui posso condividere pazienti.

---

## TIENE

- **L'apparato bibliografico.** Trentaquattro fonti verificate una per una: nessun PMID inventato, nessun numero gonfiato, nessuna attribuzione falsa. Non toccare nulla qui se non le quattro etichette segnalate sopra.
- **Il capitolo dei meccanismi ordinato dal più solido al meno solido**, con la dichiarazione esplicita che la leva manuale è più debole proprio dove il meccanismo è più forte.
- **Il confine sulla terapia farmacologica**: la frase unica, l'istruzione a dirla prima che il paziente la chieda, e l'avvertenza sulla sospensione brusca delle benzodiazepine come evento avverso del nostro lavoro anche quando non l'abbiamo suggerita.
- **La distinzione reperto/diagnosi** e la formula «un reperto positivo giustifica il tuo lavoro, non sostituisce l'inquadramento medico», ripetuta al paziente nelle stesse parole.
- **Il triage a tre uscite** con le quattro condizioni scritte del GIALLO e il ROSSO senza eccezioni, e la lista delle bandiere dichiarata «rete, non filtro», con l'istruzione di scrivere in cartella che è stata passata in rassegna e mai che il paziente è negativo. È più severo del cancello binario, e va difeso.
- **Il rifiuto esplicito del «surrene affaticato»** e la rimozione della frase sul sistema neurovegetativo sregolato, sostituita da cose che si contano.

---

## VERDETTO

**Da correggere.**
Le fonti reggono e il perimetro è dichiarato meglio di quanto sia abituale; ma la diagnosi differenziale medica manca per intero e due righe del triage — ideazione suicidaria e guida — sono classificate sotto il loro rischio reale.

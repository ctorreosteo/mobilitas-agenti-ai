# LENTE: Fisioterapista Evidence-Based

**CONDIZIONE:** Lombalgia non specifica
**DOCUMENTO REVISIONATO:** `procedure-generate/["lombalgia"]/v1-draft.md` (con la relativa `v1-scheda.md`)
**Data:** 2026-08-18

---

## RICERCA SVOLTA

Verificate su PubMed (E-utilities, abstract integrali) tutte e sei le citazioni della tabella "studi cardine" più le sei di appoggio: Nguyen 2021 (PMID 33720272), Hancock/RESTORE 3 anni (PMID 40780241), Kent/RESTORE (PMID 37146623), Licciardone 2013 (PMID 23508598), Rubinstein 2019 (PMID 30867144), Brinjikji 2015 (PMID 25430861), Franke 2014 (PMID 25175885), Hayden 2021 (PMID 34580864), Saragiotto 2016 (PMID 26742533). Verificate inoltre le fonti citate nel corpo: Laslett 2005 (PMID 16038856), Kolar 2012 (PMID 22236541), Ostelo 2008 (PMID 18165753), Seffinger 2004 (PMID 15454722), Downie 2013 (PMID 24335669), Hill/STarT Back 2011 (PMID 21963002). Cercata la letteratura contraria e successiva: MATCH, la mancata replica statunitense dello STarT Back (Cherkin, *J Gen Intern Med* 2018, PMID 29790073); revisioni recenti su OMT e su manipolazione sacroiliaca (Bagagiolo 2025 PMID 40578898; Trager 2024 PMID 38353102; Sheppard 2026 PMID 42136223).

**Esito complessivo della verifica:** PMID, riviste, anni, volumi e numerosità campionarie sono **tutti corretti**. Nessuna citazione inventata. I problemi non sono di esistenza delle fonti ma di **cosa viene fatto dire alle fonti**: tre punti in cui il risultato attribuito non è quello dell'abstract, e una regola diagnostica riportata in una forma che in Laslett non esiste.

---

## ERRORI

### E1 — "Estremamente efficace" è smentito dalla tabella studi della procedura stessa
**Sezione:** Apertura (riga 9) + Parte I, "Efficacia basata sull'eziologia" (etichette *Efficacia BUONA*) + Parte 0, modello Biomeccanico (*Evidenza: BUONA*)

**Problema.** Il documento apre con *"L'osteopatia può essere estremamente efficace nel trattamento della lombalgia non specifica"* e distribuisce etichette *BUONA* a tre sottotipi su cinque. Nella stessa procedura, quaranta righe più sotto, si legge il contrario e si legge il vero: Nguyen 2021 — il **più grande RCT sham-controllato sull'OMT nella lombalgia** (n=400) — trova a 3 mesi una differenza media di **−3,4 punti QBPDS** (IC 95% −6,0 a −0,7) su una scala il cui MIC proposto da Ostelo 2008, **che la procedura stessa adotta come metro**, è di **20 punti**; e gli autori concludono testualmente *"the clinical relevance of this effect is questionable"*. Rubinstein 2019 conclude equivalenza, non superiorità, e dichiara l'evidenza contro sham **"low to very low quality... should be considered uncertain"**. La revisione sham-controllata più recente (Sheppard, *J Osteopath Med* 2026) poggia su sette trial e n≈378: certezza GRADE moderata, effetto a ≤6 settimane. Nulla di tutto questo autorizza "estremamente efficace": è esattamente il claim che un collega informato demolisce in due minuti, e la procedura si demolisce da sola perché il contrappeso ce l'ha già dentro.

**Correzione.** Sostituire l'apertura con la formulazione che il documento usa già a riga 249 e che è corretta: *"effetti da piccoli a moderati sulla tecnica isolata, sovrapponibili alle altre terapie raccomandate; effetti ampi quando la tecnica sta dentro un percorso che rimette in movimento la persona"*. Declassare l'etichetta del modello biomeccanico da **BUONA** a **MODERATA** (è il GRADE di Rubinstein per l'equivalenza) e riformulare "Efficacia BUONA" in "**Efficacia attesa: moderata / responsività prevedibile in seduta**", che è ciò che i dati sostengono.

---

### E2 — Rubinstein 2019 è citato per un risultato che Rubinstein non riporta
**Sezione:** Parte I, "Cosa fa l'osteopatia che il farmaco e il referto non fanno", primo punto (riga 138)

**Problema.** Il testo afferma: *"Mobilizzazione e manipolazione producono riduzione del dolore e guadagno funzionale a breve termine documentati negli RCT (Rubinstein 2019; Licciardone 2013)"*. Le due fonti dicono cose opposte e nessuna delle due sostiene la coppia:
- **Rubinstein 2019** sul dolore a breve termine vs terapie raccomandate: MD **−3,17, IC 95% −7,85 a 1,51** → l'intervallo attraversa lo zero, **nessuna riduzione dimostrata**. Il vantaggio c'è solo sulla **funzione** ed è piccolo (SMD −0,25).
- **Licciardone 2013** trova il vantaggio sul **dolore** (RR 1,38 e 1,41) ma scrive esplicitamente che *"back-specific functioning, general health, work disability... did not differ between patients receiving OMT and sham OMT"* → **nessun guadagno funzionale**.

Il claim "dolore **e** funzione" è costruito prendendo da ciascuna fonte la metà che conviene e scartando la metà che smentisce. È mechanism-mongering applicato alla bibliografia, ed è il tipo di errore che squalifica l'intero apparato di citazioni agli occhi di chi le apre.

**Correzione.** Riscrivere il punto in due frasi separate e attribuite correttamente: *"La terapia manuale produce un piccolo guadagno funzionale a breve termine rispetto alle altre terapie raccomandate (Rubinstein 2019, SMD −0,25); sul dolore l'effetto vs sham è documentato ma modesto (Licciardone 2013), mentre lo stesso trial non trova differenze sulla funzione. Le due cose non arrivano insieme: prometterle insieme non è sostenuto."*

---

### E3 — Il cluster di Laslett è riportato in una forma che nello studio non esiste
**Sezione:** Parte II, "Test clinici", punto 3 — e Scheda Operativa, sezione 3, punto 3

**Problema.** Draft e scheda scrivono: *"≥3 positivi su 5 (distraction, thigh thrust, compression, sacral thrust, Gaenslen)"*. Laslett 2005 (*Man Ther* 10(3):207-18, n=48, criterio di riferimento blocco anestetico intrarticolare) riporta due compositi, e nessuno dei due è questo:
1. **≥3 su SEI test** — Gaenslen destro e Gaenslen sinistro contano come due test distinti — sensibilità **94%**, specificità **78%**;
2. **≥2 dei quattro migliori** (distraction, thigh thrust, compression, sacral thrust, **senza** Gaenslen), AUC 0,842.

Con 5 test e soglia 3 si sta applicando una regola con proprietà diagnostiche ignote. Manca inoltre la condizione di applicabilità che Laslett pone: il cluster vale **dopo aver escluso la centralizzazione** con il test di movimenti ripetuti, altrimenti la specificità crolla perché il dolore discogeno provoca falsi positivi. Va anche detto che la letteratura successiva ridimensiona il tutto: Trager 2024 (*J Man Manip Ther*, 16 RCT) non trova effetto significativo della terapia manuale sacroiliaca sul dolore.

**Correzione.** Portare in draft e scheda la formulazione esatta: **"≥3 su 6 (Gaenslen dx e sx contano separatamente) oppure ≥2 dei 4 migliori senza Gaenslen"**, aggiungere *"da applicare solo dopo aver escluso la centralizzazione"*, e aggiungere una riga onesta: *"orienta, non diagnostica; specificità 78% su n=48."*

---

## RISCHI

### R1 — RESTORE è presentato come "garanzia" senza uno solo dei suoi limiti
**Sezione:** Parte II, "Perché O'Sullivan è la nostra garanzia" + Parte 0, modello Comportamentale

**Perché è attaccabile.** La sezione elenca affiliazioni, "rigore metodologico", "non un case series" — e tace tutto ciò che un revisore aprirebbe per primo. Dall'abstract del follow-up a 3 anni: *"Physiotherapists and patients were not masked"*. L'outcome primario (RMDQ) è **auto-riferito**. Il comparatore è la **cura abituale**, non un controllo d'attenzione: in un trial non cieco con outcome soggettivo, questo confonde effetto specifico ed effetto d'aspettativa. Il dato a 3 anni poggia su **312 su 492 (63%)** e solo tra i **359 che a 1 anno avevano acconsentito a essere ricontattati**: selezione a due stadi. Infine l'entità: **−4,6 RMDQ** a 13 settimane, **−3,5 / −4,1** a 3 anni, dolore **−1,0 / −1,5 NRS** — tutte **sotto** le soglie (5 RMDQ, 2 NRS) che la procedura adotta come metro a riga 196. La procedura non commette un errore tecnico — le soglie di Ostelo sono individuali, non differenze tra gruppi — ma non lo spiega, e così espone il lettore a una contraddizione apparente che non saprà difendere.

**Mitigazione.** Aggiungere tre righe sotto "Rigore metodologico": *"Limiti dichiarati: nessuna cecità di pazienti e terapisti, outcome primario auto-riferito, comparatore cura abituale; a 3 anni 312/492 valutati (63%). Le soglie di Ostelo (5 RMDQ, 2 NRS) misurano il cambiamento del singolo paziente, non la differenza media fra gruppi: un −4,6 tra gruppi è un effetto ampio per questa condizione, non un fallimento."*

### R2 — Nguyen 2021 riportato con il numero sbagliato al momento sbagliato
**Sezione:** Parte II, tabella "I 6 studi cardine", riga Nguyen

**Perché è attaccabile.** La tabella scrive *"Effetto piccolo a 3 e 12 mesi (differenza media −3,4 punti)"*. Il dato reale: **−3,4** (IC −6,0 a −0,7) **a 3 mesi**, **−4,3** (IC −7,6 a −1,0) **a 12 mesi**. Il valore è attribuito a un tempo a cui non appartiene. L'errore qui **sottostima** l'OMT, quindi non è disonesto — ma è comunque una citazione che non corrisponde alla fonte, e chi la controlla non distingue fra un errore che gonfia e uno che sminuisce: perde fiducia in tutta la tabella. Manca inoltre il numero che spiega davvero la frase "rilevanza clinica discutibile": il MIC della QBPDS è **20 punti** (Ostelo 2008, la stessa fonte già citata a riga 196), quindi la differenza vale **circa un sesto** della soglia.

**Mitigazione.** Correggere in *"−3,4 a 3 mesi e −4,3 a 12 mesi sulla QBPDS (MIC proposto: 20 punti) — da cui il giudizio di rilevanza clinica discutibile degli autori stessi."* Aggiungere il MIC della QBPDS alla riga 196, dove oggi compaiono solo RMDQ, ODI, NRS e VAS.

### R3 — Il bersaglio dichiarato numero uno non ha nessuno strumento di misura
**Sezione:** Parte I, "I Tre Livelli di Successo" (livello 2) + Parte II, "Monitoraggio del risultato" + Scheda, riga finale

**Perché è attaccabile.** La procedura afferma che il secondo livello — la paura del movimento — *"è quello che decide se il terzo arriva"*, costruisce su di esso l'intero blocco C e l'ancora RESTORE. Poi misura RMDQ, VAS e il gesto guida: **nessuno dei tre misura paura, evitamento o catastrofizzazione**. Il bersaglio principale è l'unico non quantificato, e la sua modifica resta un'impressione del terapista. È la critica più facile da muovere: si dichiara che il fattore decisivo è psicologico e si valuta solo con strumenti di dolore e disabilità. Peraltro la procedura ha già in casa la soluzione — cita lo STarT Back — ma lo relega a "opzionale".

**Mitigazione.** Aggiungere un **TSK-11** o un **FABQ** (o, se si vuole un solo strumento, lo **STarT Back somministrato basale e alla 6ª**) al blocco "Monitoraggio del risultato" e alla riga finale della scheda, con la stessa logica prima/dopo già usata per l'RMDQ. Un solo questionario, una sola riga in più in cartella.

### R4 — L'esercizio ha la migliore evidenza del documento ed è l'unica leva senza regola di progressione
**Sezione:** Parte III, "Esercizi a casa" + "Il piano delle 6 sedute" + Scheda, sezione 5

**Perché è attaccabile.** La procedura riconosce correttamente che l'esercizio è la leva a più alta evidenza (Hayden 2021: MD **−15,2** su 0-100, differenza clinicamente importante) e assegna dosi precise a ogni esercizio — cosa che la maggior parte dei documenti simili non fa, e va riconosciuta. Ma nelle sei sedute **non esiste un criterio di avanzamento**: la tabella dice "progredisci" alla 3ª e "aggiungi il 4° esercizio" alla 2ª, senza dire **quando** e **di quanto**. Negli RCT di Hayden l'effetto viene da programmi **progressivi e supervisionati**: una dose fissa per sei settimane non riproduce l'intervento che genera quel −15,2. Va inoltre segnalato che Hayden dichiara certezza **moderata** (GRADE), non alta, e che nella stessa revisione l'esercizio **non risulta superiore alla terapia manuale** (MD 1,0; IC −3,1 a 5,1): dato utile, perché protegge la procedura dall'accusa di gerarchizzare a caso.

**Mitigazione.** Aggiungere una regola di progressione in due righe, del tipo: *"se il gesto guida è eseguito senza dolore per tre giorni consecutivi, aumenta di 2 ripetizioni o di 5 minuti di cammino; se il dolore post-esercizio supera 24 ore, torna alla dose precedente."* E correggere l'etichetta del modello metabolico da *ALTA* a *"la più alta del documento — certezza GRADE moderata"*.

---

## PREFERENZE

### P1 — Lo STarT Back andrebbe presentato con la sua mancata replica
**Sezione:** Parte II, "Monitoraggio del risultato", stratificazione prognostica

Il testo dice, correttamente, che nel trial di Hill 2011 la gestione stratificata ha migliorato gli esiti a 4 e 12 mesi. Due precisazioni che rendono il punto inattaccabile: le differenze erano **1,81 RMDQ a 4 mesi e 1,06 a 12 mesi** (effect size 0,32 e 0,19), e **MATCH** — la replica pragmatica statunitense su sei ambulatori di cure primarie (Cherkin, *J Gen Intern Med* 2018) — **non ha trovato alcun effetto** su esiti clinici né su utilizzo di risorse. Lo strumento resta ottimo come **predittore** di cronicizzazione (validato anche negli USA: Suri 2018, rischio persistente 22% / 62% / 80% nei tre strati) — ed è per questo che va tenuto. Suggerirei di usarlo dichiaratamente come **stratificatore prognostico**, non come garanzia che il trattamento stratificato funzioni.

### P2 — Seffinger dice un po' meno di quanto gli si fa dire sui reperi
**Sezione:** Parte 0, modello Biomeccanico, "Ciò che NON regge"

Il testo scrive che *"la palpazione posizionale dei reperi e dei tessuti molli ha affidabilità inter-operatore da bassa a nulla"*. Seffinger 2004 è netto sui tessuti molli (*"soft tissue paraspinal palpatory diagnostic tests are not reliable"*), ma sui **reperi ossei** i 12 articoli di qualità più alta trovavano affidabilità accettabile (K ≥ 0,40), semplicemente inferiore a quella dei test di provocazione e non sempre riproducibile. La conclusione operativa della procedura — usare i test di provocazione, non la palpazione posizionale — **resta corretta**; è solo la formulazione "da bassa a nulla" a essere più forte della fonte. Questione di precisione, non di sostanza: decide il direttore.

---

## TIENE — non toccare

- **La sezione "Cosa questi studi permettono di dire — e cosa no" (righe 245-249) è la parte migliore del documento** e va lasciata intatta. Dichiara che l'OMT non è superiore ad altri trattamenti, che le mani non "riprogrammano il sistema nervoso", che il core stability non è l'esercizio corretto e che una disfunzione posizionale palpata non è la causa del dolore. Il paragrafo "Il contrappeso onesto", che mette Nguyen 2021 in mano al lettore prima che glielo citi un altro, è integrità intellettuale rara in un documento interno.
- **Le qualificazioni dei meccanismi non dimostrati sono corrette e vanno difese**: "*down-regulation aspecifica, dichiarata come tale*"; Kolar presentato come caso-controllo 18 vs 29, "associazione, non causa"; "l'effetto della mano non è stato testato"; il divieto esplicito di dire "riprogrammo il sistema nervoso". Questo è il modo giusto di tenere un razionale clinico senza venderlo come prova.
- **La nota sulla soglia del respiro** (abbandono del ">16 atti/min" per la variazione intra-paziente sulla baseline) corregge un errore fisiologico che circola nella professione: è un miglioramento reale.
- **Licciardone 2013 è riportato con la sua stessa smentita** ("*funzione, salute generale e disabilità lavorativa non differivano dal sham*"): citazione esatta e onesta.
- **Il numero di sedute è giustificato nell'evidenza** (Licciardone 6 in 8 settimane, Nguyen 6 in 12, RESTORE fino a 7 in 12 più booster a 26). È raro e va tenuto: nessun ciclo inventato.
- **Il bivio della 3ª seduta e la regola del non-responder** ("*il non-responder è un'informazione, non un invito a spingere di più*") sono buona pratica clinica e buona protezione dal bias di conferma.
- **Brinjikji 2015 è riportato con i numeri esatti** (37% dei ventenni, 96% degli ottantenni, bulging 30-84%) e usato per lo scopo giusto: ricollocare l'imaging, non sminuirlo.

---

## VERDETTO: **Da correggere**

Le fonti esistono tutte, i PMID sono tutti corretti e il documento contiene già, al suo interno, la versione onesta di sé stesso. Servono tre correzioni puntuali — l'apertura "estremamente efficace", la coppia Rubinstein/Licciardone a riga 138, la regola di Laslett — e quattro aggiunte brevi. Nessuna riscrittura.

# Feedback — Revisore Specialista (PRIMO livello)

**LENTE:** Medico Specialista — Neurologo, centro cefalee
**CONDIZIONE:** Emicrania episodica e cronica, in paziente già inquadrato
**DOCUMENTI REVISIONATI:** `v1-draft.md` (procedura) e `v1-scheda.md` (scheda operativa) in `procedure-generate/["emicrania"]/`

---

## RICERCA SVOLTA

Ho verificato i criteri ICHD-3 per la cefalea da uso eccessivo di farmaci (8.2 e sottotipi) e per l'emicrania con aura (1.2), la lista SNNOOP10 originale (Do et al., *Neurology* 2019, PMID 30587518), la soglia EHF/EMA per l'indicazione alla profilassi, e la letteratura su dissezione arteriosa cervicale nell'emicranico. Ho controllato una per una le citazioni della procedura su PubMed: **Posadzki, Klimek, Ernst 2024** (*Syst Rev* 13:296, PMID 39614402 — esiste, conferma il raddoppio del rischio di eventi avversi e l'efficacia non provata), **Tolentino et al. 2025** (*Musculoskelet Sci Pract* 78:103360, PMID 40460766 — esiste, RCT a 3 bracci n=75, multimodale superiore nel mantenimento al follow-up), **Al-Khazali 2022** (*Cephalalgia* 42(7):663-673, PMID 35166137), **Luedtke 2018**, **Szikszay 2019**, **Luedtke 2016**, **Falsiroli Maistrello 2018**, **Cerritelli 2015**, **Lemmens 2019**, **Beier 2022**, **Bartsch & Goadsby 2002/2003**, **Benatto 2019/2022**. **Nessuna citazione risulta inventata e nessun risultato risulta gonfiato nell'attribuzione.** È un fatto che va detto: è la parte del documento che regge meglio. I rilievi che seguono non riguardano la bibliografia, riguardano i criteri clinici e i trigger di invio.

Segnalo per completezza che su Posadzki 2024 esiste un commentary critico pubblicato su *Systematic Reviews* (2025) sui limiti metodologici della meta-analisi. Non cambia la conclusione operativa della procedura (niente thrust), ma il documento la presenta come dato pacifico.

---

## ERRORI

### 1. La soglia di sospetto per la cefalea da uso eccessivo di farmaci è sbagliata, e sbagliata nella direzione pericolosa

**Sezione:** Parte I — "Sospetto uso eccessivo di sintomatici"; Parte II — Red flags, ultimo punto; Parte II §2 tabella; Scheda §1, ultimo punto.

La procedura definisce il sospetto MOH come **"≥15 giorni/mese di cefalea con assunzione frequente di farmaci"**, e ripete la stessa formula in quattro punti diversi, scheda inclusa. Non è il criterio.

ICHD-3 8.2 richiede cefalea ≥15 giorni/mese **più** overuso regolare per >3 mesi, con soglie **diverse per classe di farmaco**:
- **triptani, ergotaminici, oppioidi, analgesici di combinazione, e combinazioni di più classi: ≥10 giorni/mese** (8.2.1, 8.2.2, 8.2.4, 8.2.5, 8.2.6);
- **analgesici semplici (paracetamolo, FANS, ASA): ≥15 giorni/mese** (8.2.3).

Conseguenza concreta: il paziente che prende un triptano 11 giorni al mese — il profilo MOH più comune e più recuperabile che vedo in ambulatorio — **non fa scattare nessun trigger in questa procedura**, e riceve sei sedute manuali mentre il circolo continua. La procedura fa anche giustamente della conta dei giorni-farmaco il suo "test 6", ma non dice mai all'osteopata di **chiedere quale farmaco**, il che rende la conta inutilizzabile per lo scopo dichiarato. Manca inoltre il criterio temporale (>3 mesi).

**Correzione.** Riscrivere il trigger in tutti e quattro i punti, scheda inclusa: *"Conta i giorni-farmaco separando le classi. Segnala al medico se, per più di 3 mesi: triptani / ergotaminici / oppioidi / analgesici di combinazione ≥10 giorni al mese, oppure FANS o paracetamolo ≥15 giorni al mese. Soglia di allerta precoce: 8 giorni/mese di triptano."* Nel test 6 aggiungere la domanda esplicita: *"quale farmaco, quante volte, da quanti mesi"*.

**Prova:** ICHD-3 8.2, 8.2.2 (triptani, ≥10 gg/mese), 8.2.3 (analgesici non oppioidi, ≥15 gg/mese) — ichd-3.org.

---

### 2. La lista red flag dichiara SNNOOP10 come riferimento ma ne omette almeno tre voci, incluse quelle che qui contano di più

**Sezione:** Parte II — "Red flags e criteri di invio medico"; Scheda §1.

Il documento scrive: *"Il riferimento internazionale per questa lista è la SNNOOP10"*. La lista costruita non la copre. Mancano:

- **Papilledema e sindrome da ipertensione endocranica** — nella pratica: **acufene pulsante sincrono col polso, oscuramenti visivi transitori (pochi secondi, spesso al cambio di postura), visione appannata progressiva, diplopia orizzontale**. È il pezzo più grave, perché l'ipertensione endocranica idiopatica ha una cefalea clinicamente indistinguibile dall'emicrania, colpisce donne giovani, e i sintomi che la smascherano sono proprio quelli accompagnatori. Aggravante interna al documento: la riga sulle "condizioni spesso associate" (Parte III) manda l'osteopata a trattare gli **acufeni** con la procedura dedicata, senza mai dire che **un acufene pulsante in un cefalalgico non si tratta, si manda**. Quello è ritardo diagnostico con perdita visiva potenzialmente irreversibile.
- **Occhio dolente con segni autonomici** (lacrimazione, iniezione congiuntivale, ptosi, midriasi fissa) → glaucoma acuto ad angolo chiuso e cefalee trigemino-autonomiche. Assente del tutto.
- **Nuovo farmaco all'esordio della cefalea** (nitrati, inibitori della PDE5, contraccettivo ormonale appena iniziato) — voce esplicita della SNNOOP10, assente.

**Correzione.** Aggiungere tre righe alla lista di Parte II e alla Scheda §1:
1. *"Acufene pulsante sincrono col polso, oscuramenti visivi di pochi secondi, visione che si appanna progressivamente, diplopia → sospetta ipertensione endocranica: invio, e nessun trattamento dell'acufene."*
2. *"Occhio rosso e dolente con lacrimazione, ptosi o pupilla alterata → urgenza oculistica/neurologica."*
3. *"Cefalea comparsa dopo l'inizio di un nuovo farmaco → medico."*
Inoltre correggere il rimando alle procedure correlate: *"acufene → prima escludi che sia pulsante"*.

**Prova:** Do TP et al., *Neurology* 2019;92(3):134-144, lista SNNOOP10 (voci: papilledema; painful eye with autonomic features; new drug at onset of headache). Letteratura IIH: cefalea indistinguibile dall'emicrania, discriminata dai sintomi accompagnatori (acufene pulsante, oscuramenti visivi transitori).

---

### 3. I criteri sull'aura non contengono l'unico elemento che distingue un'aura da un TIA — e in compenso escludono pazienti che non andrebbero esclusi

**Sezione:** Parte II — Red flags, 3° punto; Parte I — "Aura frequente, atipica o prolungata (Efficacia NULLA — Invio)"; Scheda §1, 3° punto.

Due difetti opposti nello stesso blocco.

**a) Manca il criterio discriminante.** La procedura segnala aura >60 minuti, aura sempre omolaterale, deficit che non si risolvono. Tutto corretto, tutto insufficiente. Il criterio che ICHD-3 usa per separare aura emicranica e ischemia è il **modo di esordio**: l'aura emicranica **si diffonde gradualmente in ≥5 minuti** e i sintomi si succedono l'uno all'altro; il TIA esordisce **improvvisamente e simultaneamente**, con fenomeni prevalentemente negativi. Un paziente che descrive un deficit visivo o sensitivo comparso di colpo, tutto insieme, e risolto in 20 minuti, rientra in tutti i parametri "tranquillizzanti" di questa procedura e viene messo sul lettino. Mancano anche, come voci esplicite, l'**aura con deficit motorio** (emiplegica) e l'**aura del tronco encefalico** (disartria, vertigine, diplopia, ipoacusia, atassia, alterazione della coscienza) — che questa procedura, per giunta, elenca altrove come sintomi dello screening vascolare, senza collegare le due cose.

**b) L'esclusione è troppo larga nell'altra direzione.** *"Aura frequente… Efficacia NULLA — Invio"* e *"sull'aura non abbiamo né mandato né dati"* rimandano indietro pazienti che non hanno alcun problema: circa un terzo degli emicranici ha aura, e un'**aura tipica, stereotipata, stabile da anni e già inquadrata dal neurologo non è una bandiera rossa** — è parte della diagnosi che la procedura dichiara di accettare. Così scritta, la regola produce invii inutili e, per il paziente, il messaggio "sei un caso troppo complicato" da parte del terzo professionista di fila.

**Correzione.** Sostituire il punto con: *"Aura da inviare: esordio improvviso e simultaneo (non graduale in ≥5 minuti), durata >60 minuti, sempre dallo stesso lato, deficit motorio (forza), sintomi del tronco (disartria, diplopia, vertigine, atassia, ipoacusia), prima aura in assoluto, o aura diversa dalla solita. Aura tipica, stereotipata e già inquadrata dal neurologo non è una controindicazione al trattamento."* Riclassificare la voce di Parte I da "Efficacia NULLA — Invio" a "Aura **atipica, nuova o prolungata** — Invio", lasciando l'aura tipica dentro i candidabili.

**Prova:** ICHD-3 1.2, criterio C (diffusione graduale ≥5 min; ogni sintomo 5-60 min; specificità 96-98% nel distinguere aura da TIA); ICHD-3 1.2.3 aura del tronco encefalico, 1.2.3.1 emiplegica.

---

## RISCHI

### 1. Nessun trigger che verifichi se il paziente ha mai ricevuto una profilassi

**Sezione:** Parte I — "Gestione delle aspettative"; Parte III §4; "Follow-up" e "Il piano delle 6 sedute".

La procedura è scrupolosa nel dire che profilassi e sintomatici sono del neurologo, che non si tocca il farmaco, che si rinforza l'aderenza. Bene. Ma l'unico trigger medico che prevede è la red flag e il sospetto MOH. Risultato: un paziente con **10 giorni-emicrania al mese, mai messo in profilassi**, attraversa sei sedute, un "mantenimento diradato" e una relazione al medico senza che nessuno alzi la mano. Dal mio lato della scrivania quello è un paziente sotto-trattato, e non lo è per colpa vostra ma il documento vi rende complici passivi. La soglia EHF/EMA per l'indicazione alla profilassi (inclusi gli anti-CGRP) è **≥4 giorni-emicrania al mese**: è un dato che la vostra stessa raccolta con il diario produce spontaneamente.

**Mitigazione.** Aggiungere in prima visita e nel bilancio della 6ª seduta: *"Se il diario mostra ≥4 giorni-emicrania al mese e il paziente non è in profilassi (o non gli è mai stata proposta), scrivilo nella relazione al medico inviante. Non è una raccomandazione terapeutica — è un dato che il neurologo deve avere."* Nella Scheda, una riga nel box finale.

### 2. La griglia "Efficacia MODERATA" contraddice l'evidenza che il documento stesso cita tre righe dopo

**Sezione:** Parte I — "Efficacia basata sull'eziologia".

Il documento assegna **"Efficacia MODERATA"** alla dominanza biomeccanica cervicale e alla dominanza stomatognatica. Nella stessa riga della prima cita Falsiroli Maistrello con "qualità dell'evidenza dichiarata **molto bassa** dagli autori stessi", e in Parte II ricorda che la meta-analisi della propria ancora ha **GRADE basso** con riduzioni sotto la rilevanza clinica. Per la dominanza stomatognatica non c'è **nessuno** studio di efficacia sull'emicrania citato: il "MODERATA" è appeso al nulla. Aggiungo che nessuno studio ha mai testato l'efficacia stratificata per "pattern di dominanza": è una griglia interna, non un dato. Su tutto il resto questa procedura è disciplinata al punto da essere quasi un manuale di come si scrive un documento onesto — e poi si autoinfligge l'unico punto in cui un neurologo può dire "ecco, gonfiano".

**Mitigazione.** Rinominare la colonna in **"Priorità clinica"** o **"Trattabilità del carico"**, oppure mantenere le etichette di efficacia ma riferirle esplicitamente all'outcome misurato e alla qualità GRADE reale (es. *"Impatto (HIT-6): segnale positivo, evidenza molto bassa"*). E aggiungere una riga: *"Questi pattern sono uno strumento di scelta, non sottogruppi con efficacia dimostrata."*

### 3. Lo screening vascolare pre-cervicale è presentato come un filtro che non è, in una popolazione a rischio basale aumentato

**Sezione:** Parte II — "Controindicazioni", blocco "Prima di ogni lavoro cervicale alto"; Scheda §1-bis.

Due problemi. Primo: nessun questionario o test posizionale pre-manipolativo ha accuratezza diagnostica validata per escludere una dissezione — la formulazione *"Anche una sola positività → niente lavoro cervicale"* suggerisce implicitamente che la negatività autorizzi. Secondo, e specifico di questa condizione: vertigine, fotopsie, parestesie e disturbi del linguaggio **fanno parte del fenotipo emicranico**. Applicata alla lettera, questa lista rimanda indietro ogni emicrania con aura e ogni emicrania vestibolare; applicata con buon senso, non filtra niente. Il documento se ne accorge (*"nel dubbio non tratti e mandi"*) ma non risolve.

Va inoltre detto quello che il documento non dice: **l'emicrania in sé è associata a un rischio aumentato di dissezione arteriosa cervicale** (OR pooled ~1,74; 95% CI 1,38-2,19 su 11 studi e 9.857 pazienti; una meta-analisi precedente OR 2,06). Questo rafforza la vostra regola sul thrust — e vale la pena scriverlo, perché è l'argomento che convince un neurologo che il no-thrust non è prudenza generica.

**Mitigazione.** Riformulare in due criteri distinti: (a) *"sintomi neurologici **nuovi, diversi dal solito, o in evoluzione** → stop e invio"*; (b) *"sintomi stereotipati, identici a quelli già descritti al neurologo e documentati in cartella → non sono un criterio di esclusione"*. Aggiungere la riga: *"Nessun test pre-manipolativo esclude una dissezione. Il filtro vero è l'anamnesi: cervicalgia o cefalea **inusuale** a esordio brusco in un emicranico noto = dissezione fino a prova contraria, anche senza Horner."* E citare l'OR nel blocco che motiva l'esclusione del thrust.

---

## PREFERENZE

### 1. Il cut-off del Flexion-Rotation Test viene da un'altra popolazione

**Sezione:** Parte II §1 (criteri di inclusione), §3 test n.1; Scheda §2.

Il valore *"< 32° o differenza ≥ 10°"* è stato derivato e validato per la **cefalea cervicogenica**. Szikszay 2019 dimostra che il FRT discrimina emicranici e sani **a livello di gruppo** (differenza media in meta-analisi), non che quel cut-off abbia accuratezza diagnostica nel singolo emicranico. Il documento è già corretto nel dire che non è un test diagnostico; converrebbe essere altrettanto espliciti sul cut-off: usarlo come **valore di riferimento prima/dopo dello stesso paziente**, non come soglia di candidabilità dicotomica.

### 2. HIT-6 senza differenza minima clinicamente rilevante

**Sezione:** Parte II §4 "Monitoraggio del risultato"; tabella "cosa aspettarsi", riga 3-5 sedute.

"HIT-6 in calo" senza una soglia dichiarata rende chiamabile successo un calo di 1 punto. In letteratura la differenza minima importante intra-paziente è stimata fra **2,5 e 6 punti** (Smelt 2014; Coeytaux ~3,7). Vale la pena scriverlo accanto alla scala: protegge l'osteopata dall'auto-illusione e rende il dato leggibile per me.

---

## TIENE

Non toccare queste, sono la ragione per cui continuerei a ricevere pazienti da questo studio: **l'esclusione esplicita del thrust cervicale ad alta velocità**, motivata e non contrattata; il rifiuto scritto dei claim di meccanismo (drenaggio venoso cranico, tono vagale, ossitocina, "sensibilizzazione centrale ridotta") con la formula corretta "riduzione dell'input nocicettivo cervicale"; il confine "la diagnosi è atto medico, non la pongo e non la metto in dubbio"; la frase **"non puoi dire che la terapia manuale riduce il numero di attacchi in modo clinicamente rilevante"**, che pochissimi documenti di questo tipo hanno il coraggio di scrivere; il rinforzo dell'assunzione **precoce** del triptano e dell'aderenza al piano del neurologo; il blocco D con l'esercizio aerobico come leva a evidenza migliore. La bibliografia è verificabile e verificata.

---

## VERDETTO: Da correggere

Impianto scientifico e perimetro di scope tra i più solidi che mi siano capitati in un documento osteopatico; ma i tre criteri che decidono se un paziente viene mandato dal medico o messo sul lettino — soglia MOH, red flag da ipertensione endocranica, discriminazione aura/TIA — sono formulati in modo che lascia passare i casi sbagliati. Sono correzioni di poche righe, e senza quelle non firmerei l'invio.

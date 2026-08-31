# Feedback — Revisore di 3º livello · Coerenza (l'Ispettore delle Giunture)

**LENTE:** Coerenza interna — l'Ispettore delle Giunture
**CONDIZIONE:** epicondilite laterale (tendinopatia laterale di gomito)
**DOCUMENTO REVISIONATO:** `bibbie-generate/epicondilite/v3-intermedia.md` (v3 intermedia, sintesi 2º livello, 31 agosto 2026), con `mappa-v3.md` come riscontro incrociato.
**Estensione:** 24.271 parole, 1.148 righe. Architettura verificata: 15 capitoli, 15 aperture «In una riga», 15 chiusure «Le tre cose da ricordare», 15 slot «Perché ci sei tu».

---

## LE NOVE GIUNTURE

| # | Coppia | Esito | Nota |
|---|---|---|---|
| 1 | Ragionamento × Leve | **INCOERENTE** | Il caso canonico (attivazione) è chiuso benissimo in entrambe le direzioni. Cede su un altro punto: Cap 8 nega il carico al paziente con soglia bassa, che Cap 12 e lo stesso Cap 8 dichiarano lavorabile sotto soglia. |
| 2 | Meccanismi × Leve | **COERENTE** | Cap 11 ha cinque sezioni intestate ai cinque meccanismi di Cap 5, per nome e nello stesso ordine. Il meccanismo 1 dichiara l'assenza di leva («su niente, direttamente») invece di tacerla. |
| 3 | Meccanismi × Strumenti attivi | **SFASATO** | I tre strumenti agganciano per nome i meccanismi 1, 2 e 3. Sul 4 (catena a monte) e sul 5 (nervo) Cap 12 tace, e il silenzio si legge come dimenticanza proprio dove il lettore è più tentato di inventare. |
| 4 | Leve × Strumenti (seduta/ripetizione) | **COERENTE** | È la giuntura meglio chiusa del documento. Cap 11: «La funzione della mano è aprire la finestra; il lavoro che dura lo fa il carico», e il Meccanismo 4 spiega *perché* si conta in settimane e non in sedute. Nessun guadagno di allenamento attribuito alla tecnica. |
| 5 | Scienza × Etichette (ponte + uniformità) | **SFASATO** | La regola del ponte è rispettata fonte per fonte, con la frase-ponte al punto d'uso e non solo alla citazione. Due nei: un conteggio interno che non torna, e uno studio cervicale che regge il DIMOSTRATO di un modello che non governa quel distretto. |
| 6 | Limiti di campo × Cosa dire al paziente | **COERENTE** | La convivenza reperto/inquadramento arriva al paziente con le **stesse identiche parole** del GIALLO, e il documento lo dichiara («E la convivenza, con le stesse parole del triage»). Le bandiere rosse di casa sono dichiarate come «l'altra metà» di quelle d'ingresso, non come un elenco parziale. |
| 7 | Gli slot «Perché ci sei tu» | **COERENTE** | Quindici, letti in fila. Nessun dato ripetuto fra due slot. Almeno quattro **restringono** (Cap 2 chirurgia, Cap 3 nervo, Cap 10 chirurgia finta, Cap 12 certezza bassa). Il terzo elemento è sempre specifico, mai «non ti autorizza a promettere» generico. |
| 8 | Il lessico | **INCOERENTE** | Le sette parole del metodo hanno tutte box e Glossario. Ma **«piano» porta cinque significati diversi**, due dei quali dentro la stessa pagina della regola dei marker; e **«lesione primaria» non ha nessuna comparsa operativa**, contro quello che Cap 0 promette. |
| 9 | Sottotipi × Leve × Triage | **COERENTE con un neo** | I due sottotipi «invio, e lavoro accanto» risultano tali in Cap 11 (il nervo: «un test che risponde meglio non sostituisce l'invio») e nel triage (formicolio → GIALLO PRIORITARIO, tre settimane). Il neo è una cella di tabella più povera della prosa che la circonda. |

---

## ERRORI — il documento afferma due cose incompatibili

### E1 · Giuntura 1 — «il carico non è lavorabile» contro il carico sotto soglia

**Capitolo A dice** (Cap 8, «Perché si indaga dall'alto», riga 486):
> «Il piano alto rende inefficace il lavoro sui piani sotto: sopra la soglia individuale il carico **peggiora** il sintomo per almeno mezz'ora, e sotto si comporta come il non fare niente (Coombes, 2016). **Finché la soglia è bassa, il carico non è lavorabile.**»

**Capitolo B dice** — e sono tre voci concordi:
- Cap 8 stesso, l'insegnante (riga 478): «A questo aggiungi carico **sotto** la sua soglia di dolore, perché sopra peggiora e sotto no (Coombes, 2016).»
- Cap 12 (riga 899): «Sul sottotipo con dolore allargato **i tre strumenti restano validi**, ma cambia il punto di partenza: la soglia individuale è più bassa.»
- Cap 6 (riga 138): «Su questo paziente hai **più** da fare, non meno.»

**Il nodo.** Lo stesso studio (Coombes, 2016) viene letto in due direzioni opposte. In Cap 8 «sotto si comporta come il non fare niente» diventa l'argomento per **non** caricare; in Cap 12 lo stesso risultato è l'argomento per caricare **in sicurezza** sotto soglia. E Coombes 2016 misura il dolore riferito subito dopo una singola seduta sperimentale, non l'adattamento del tessuto in settimane: non è una misura di inefficacia del carico progressivo.

**QUALE LATO CORREGGERE: A (Cap 8).**
**Perché:** vince la formulazione ancorata al dato. Cap 12 dichiara PROBABILE il carico progressivo su trenta randomizzati ed è la leva con le prove migliori dell'intero documento; Cap 8 nega quella leva proprio al sottotipo che il documento presenta tre volte come «quello in cui hai più da fare». È la classe di difetto per cui questo ruolo esiste: il lettore crede al capitolo del ragionamento, perché è quello che ha in mano col paziente davanti, e sottrae al paziente sensibilizzato l'intervento meglio sostenuto.

**Come:** sostituire l'ultima frase con —
> «Finché la soglia è bassa, la finestra di carico lavorabile è stretta: si lavora **sotto** quella soglia, e allargarla è il primo obiettivo.»

**Costo: +8 parole nette.**

---

### E2 · Giuntura 5 — un conteggio che non torna nel capitolo dell'onestà

**Il documento dice** (Cap 10, «Quando la scienza tace», punto 2, riga 740):
> «su **sette** oggetti gli studi esistono e sono negativi — rinforzo scapolare aggiunto, PRP, chirurgia contro chirurgia finta, braccio fisioterapia del trial dell'ancora, beneficio mantenuto di mano ed esercizio nella Cochrane, esercizio consegnato senza accompagnamento, e l'ipoalgesia da mobilizzazione testata su dolore indotto in soggetti sani. **Quattro dei sette colpiscono l'intervento di casa.**»

**Il nodo.** Dei sette elencati, solo due — PRP e chirurgia — sono esterni al nostro intervento. Gli altri **cinque** colpiscono l'intervento di casa. Il conteggio contraddice l'elenco che lo precede di una riga, e lo fa nel punto in cui il documento sta rivendicando di elencare i dati negativi «per nome invece che omessi».

**QUALE LATO CORREGGERE: il numero, non l'elenco.**
**Perché:** l'elenco è verificabile e corretto, il numero no. E correggerlo in alto rafforza la rivendicazione invece di indebolirla.

**Come:** «**Cinque dei sette** colpiscono l'intervento di casa».

**Costo: 0 parole.**

---

## RISCHI — non si contraddicono, ma si sfasano

### R1 · Giuntura 8 — «piano» porta cinque significati

**Cosa non combacia.** La parola *piano* è usata nel documento per cinque cose diverse, tre delle quali nello stesso capitolo:

| Riga | Uso | Significato |
|---|---|---|
| 174 | «il piano che decide quanta strada deve fare la mano» | livello anatomico (spalla-scapola) |
| 456 | «quale dei **cinque piani** comanda» | i cinque meccanismi |
| 486 | «il piano alto rende inefficace il lavoro sui piani sotto» | gerarchia fra meccanismi |
| 494-524, tabella | «tocchi un solo piano», «Piano che hai trattato» | il bersaglio trattato (gomito, collo, spalla, gesto) |
| 594 | «su due piani distinti» | registro (clinico / professionale) |

Il punto in cui costa davvero è la **regola di verifica**: «il marker appartiene a **un piano che non hai trattato**». Se *piano* è il meccanismo, la regola dice una cosa; se è la regione trattata — come nella tabella immediatamente sotto — ne dice un'altra. Le due letture non danno lo stesso marker, e il lettore non ha modo di sapere quale vale. La regola operativa più importante del capitolo poggia su una parola bivalente.

**Cosa lo allineerebbe.** Riservare *piano* al **bersaglio trattato** (che è l'uso della tabella dei marker, dove la parola è ormai tecnica) e usare *meccanismo* per i cinque. Quattro sostituzioni puntuali: riga 456 «quale dei cinque **meccanismi** comanda»; riga 486 «Il **meccanismo che comanda** rende inefficace il lavoro su quelli sotto»; riga 528 «si promuove il **meccanismo** successivo»; riga 554 «quale **meccanismo** comanda». Allineare di conseguenza la definizione di *sistema dominante* (riga 458 e Glossario): «il **meccanismo** che, in questo paziente, sta consumando più capacità di adattamento degli altri». Riga 594 (*due piani distinti*) è un uso comune ma troppo vicino: meglio *due registri distinti*.

**Costo: 0 parole** (solo sostituzioni).

---

### R2 · Giuntura 3 — due meccanismi su cinque non compaiono in «Cosa può fare il paziente da solo»

**Cosa non combacia.** Cap 12 aggancia ogni strumento a un meccanismo per nome, come deve: strumento 1 → meccanismi 1 e 3; strumento 2 → 3 e 2; strumento 3 → 3. Il **meccanismo 4** (la catena a monte) e il **meccanismo 5** (il nervo) non compaiono mai. La chiusura del capitolo cita solo le leve del Metabolico (fumo, cortisone, glicemia, sonno, fluorochinoloni).

Non è una contraddizione: la decisione è già presa altrove, in Cap 11 («Il rinforzo scapolare aggiunto ha un randomizzato negativo: resta un bersaglio di ragionamento, non una leva»). È una decisione presa nel capitolo sbagliato per il lettore. Chi arriva a Cap 12 avendo appena letto in Cap 5 che spalla e scapola sono **misurate alterate**, e in Cap 8 che la finestra di posizione è il bersaglio dell'elettricista, prescrive esercizi scapolari a casa — cioè esattamente la cosa su cui questo documento ha l'unico randomizzato negativo dedicato.

**Cosa lo allineerebbe.** Portare la conclusione di Cap 11 nel punto d'uso, con il materiale già presente. Dopo l'elenco dei tre strumenti:
> «Sul quarto meccanismo — la catena a monte — non c'è uno strumento attivo in questo elenco, ed è una scelta e non una dimenticanza: l'unico randomizzato che ha aggiunto il rinforzo scapolare al trattamento locale non ha trovato differenze (Day, 2021, PMID 33440342). Sul quinto — il nervo — non c'è nulla che il paziente faccia da solo: lì la misura che decide è elettrofisiologica.»

**Costo: +52 parole.**

---

### R3 · Giuntura 2/6 — lo stop dei fluorochinoloni non arriva al punto d'uso, e il rinvio manda dalla parte sbagliata

**Cosa non combacia.** Cap 9 (riga 586) contiene un divieto secco e ben scritto:
> «su quel paziente **il carico progressivo di «Cosa può fare il paziente da solo» non si apre finché il curante non risponde**.»

Cap 12, che è il capitolo nominato in quel divieto, non lo riporta. Anzi, rinvia altrove (riga 899): «fumo, cortisone sistemico, glicemia, sonno, fluorochinoloni: stanno nel modello Metabolico-Energetico, **con lo scope già scritto lì**». E il Metabolico (Cap 7, riga 429) dice soltanto: «si valutano, si nominano e si rinviano al curante: con le mani non si lavorano» — nessuno stop sul carico.

Il rinvio è quindi un **indirizzo sbagliato**: manda il lettore in un capitolo dove la regola non c'è, per una regola che esiste in un terzo capitolo. Chi apre Cap 12 per insegnare il carico non incontra mai il divieto.

**QUALE LATO CORREGGERE: Cap 12.** Cap 9 è il posto giusto per la regola — è il cancello — e la formulazione è già precisa. Manca la copia al punto d'uso.

**Cosa lo allineerebbe.** In Cap 12, dentro lo strumento 1, una riga:
> «Un'eccezione che non si negozia: con un fluorochinolone in corso o nell'ultimo mese questo strumento **non si apre** finché il curante non risponde («Dove finisce il nostro campo»).»

**Costo: +26 parole.**

---

## PREFERENZE — sfasamenti minori, correzione a costo quasi nullo

### P1 · Giuntura 5 — uno studio cervicale regge il DIMOSTRATO del modello Biomeccanico

Cap 7, Biomeccanico-Strutturale, box `Quanto è solido`: «**DIMOSTRATO** l'effetto **immediato**, misurato contro placebo e contro controllo (Vicenzino, 1996, PMID 9252000; Paungmali, 2003, PMID 12665408)». Ma **Vicenzino 1996 è una mobilizzazione cervicale** (il *contralateral lateral glide*, come Cap 9 dichiara per esteso), e fra gli «Attori» del Biomeccanico il rachide cervicale non c'è: sta fra gli attori del **Neurologico**, che cita gli stessi due studi per il proprio DIMOSTRATO. Lo stesso studio regge l'etichetta di due modelli, uno dei quali non governa quel distretto.

**Correggere: il Biomeccanico.** Togliere Vicenzino 1996 dal suo box e lasciare Paungmali 2003 (mobilizzazione con movimento di gomito), che è del distretto giusto. L'etichetta non cambia e non si perde nessuna prova: Vicenzino 1996 resta dov'è già, nel Neurologico e in Cap 11.
**Costo: −6 parole.**

### P2 · Giuntura 9 — la cella «Abbastanza» è più povera della prosa che la circonda

Cap 6, tabella dei sottotipi: «Dolore allargato | Bilaterale, freddo, paura | Sistema del dolore | **Abbastanza**». Dodici righe più sotto lo stesso capitolo scrive: «Su questo paziente hai **più** da fare, non meno: solo con leve diverse», e Cap 8 lo ripete. La cella, letta da sola — ed è la riga che finisce nella tabella riassuntiva — dice il contrario. La `mappa-v3.md` ha già la formulazione giusta: «**Abbastanza — leve diverse, non meno**».

**Correggere: la Bibbia, allineandola alla mappa.**
**Costo: +4 parole.**

### P3 · Giuntura 8 — «lesione primaria» non ha una comparsa operativa

Cap 0 promette: «Ciascuna [delle sette parole del metodo] compare in un box `Definizione` **alla sua prima comparsa operativa — quella in cui regge una regola di condotta**». Per *lesione primaria* la promessa non è mantenuta: il termine compare tre volte in tutto il documento — nella dichiarazione di Cap 0, nel box di Cap 8 (riga 490) e nel Glossario — e mai in una frase che lo usi. Il box galleggia fra la regola tolta e la prova della chiave di volta senza agganciare niente. Il lavoro concettuale c'è, ma sotto un altro nome: «Il gomito, su questa condizione, è quasi sempre il punto in cui un **compenso** ha ceduto».

**Correggere: agganciare il box alla frase che già fa quel lavoro**, chiudendola con la clausola di condotta che il box promette — es. «…e la **lesione primaria** che si ricostruisce sta a monte del gomito: si scrive in cartella come ipotesi, con la data, mai come fatto.»
**Costo: +18 parole.**

---

## PROPOSTA DI DECIMA GIUNTURA

**«Bibbia × Mappa concettuale».** Ricorre due volte in questo documento e in una sola direzione: la mappa è **più completa** della Bibbia nel punto in cui le due divergono (cella «Abbastanza — leve diverse, non meno»; e la mappa §7 riporta la regola tolta con la sua motivazione, che nella Bibbia sta in un paragrafo separato). La mappa è il documento che l'osteopata apre due minuti prima del paziente, e a sei mesi è l'unico che rilegge (Cap 0, passi 4 e 6): una divergenza in quella direzione significa che il lettore esperto legge una versione e il lettore che studia ne legge un'altra. Merita un controllo fisso a coppie, perché la mappa viene scritta per ultima e quasi mai rivista quando la Bibbia cambia.

---

## LE SEI FASI DELL'APPRENDIMENTO — mappa di riscontro

*(La mappa a sei fasi appartiene al mandato gemello di 3º livello, l'apprendimento. La riporto perché richiesta, giudicata solo per quanto la coerenza fra capitoli la tocca; il giudizio pieno spetta a quella lente.)*

| Fase | Dove vive | Esito |
|---|---|---|
| **Perché** | Cap 2 «Che cos'è davvero», Cap 4 «Come funziona quando funziona», Cap 5 meccanismi | **Presente** — e il passo 6 di Cap 4 («si costruisce in mesi, si smonta in poche settimane») è il perno causale che regge metà documento |
| **Cosa** | Cap 1, Cap 3 strutture, Cap 5, Cap 6 sottotipi | **Presente** |
| **Come** | Cap 7 modelli, Cap 8 ragionamento, Cap 11 leve | **Presente** — indebolito nel punto di E1 |
| **Pratica** | Cap 8 (tre pazienti-tipo), Cap 12 strumenti, Cap 13 script e obiezioni | **Presente, con un buco** — i meccanismi 4 e 5 non arrivano alla pratica del paziente (R2) |
| **Feedback** | Cap 8: quattro marker, soglie con provenienza dichiarata, tabella «quale marker decide», «quando il marker non si muove» | **Presente e forte** — è la parte più solida dell'impianto didattico |
| **Autonomia** | Cap 0 «Come si studia» (sei passi), Cap 14 «Le tre cose che cambi da lunedì» | **Presente** — con criterio di padronanza esplicito: «chiudi il documento e parla» |

---

## DA PROTEGGERE DALL'EDITOR (4º livello)

Otto ripetizioni che **non** sono ridondanze. Ognuna è una giuntura tenuta chiusa da una ripetizione deliberata: toglierla riapre la giuntura.

1. **La frase della convivenza, identica in Cap 9 e Cap 13.** «Io lavoro sul carico e sulla componente meccanica che ho trovato. Il dolore va comunque inquadrato dal tuo/suo medico, e nel frattempo io non aspetto.» È la giuntura 6 chiusa, e il documento dichiara perché la ripete («E la convivenza, con le stesse parole del triage»). Riscriverla in una delle due sedi la rompe. **Intoccabile.**
2. **«Sopra la soglia peggiora, sotto no» (Coombes 2016), ripetuto in Cap 7, Cap 8, Cap 9 (consenso), Cap 12 e mappa.** È l'unica regola che attraversa attivazione, carico, consenso informato e sicurezza: vive in quattro capitoli perché serve in quattro decisioni diverse.
3. **«Il tendine si costruisce in mesi e si smonta in poche settimane», ripetuto verbatim in Cap 4, Cap 12, Cap 13 e mappa.** Trasporta lo stesso concetto fra tre registri — fisiologia, strumento, parole al paziente. La ripetizione *è* la funzione.
4. **Le frasi-ponte sui salti** («il salto è di sede / di popolazione / di intervento / di erogatore e di composizione»), ripetute a ogni fonte dei cerchi 2 e 3. Sembrano una formula ricorrente; sono la regola del ponte in atto, e l'unica cosa che tiene le etichette oneste al punto d'uso.
5. **La glossa che accompagna ogni etichetta** — «DIMOSTRATO *(studi sull'uomo, solidi)*» e le altre tre — a ogni singolo box. **Intoccabile** per mandato.
6. **«L'invio non chiude il tuo lavoro, lo affianca»**, in Cap 6, Cap 8 e mappa. È ciò che impedisce di leggere due sottotipi su cinque come un capolinea, ed è la giuntura 9.
7. **Cap 11, Meccanismo 4: «E la ragione del tempo va scritta, altrimenti resta un numero».** Sono trentacinque parole che chiudono da sole la giuntura 4 — l'errore che gli osteopati fanno più spesso, attribuire alla tecnica un guadagno che appartiene alla ripetizione. Sembra una digressione; è una saldatura.
8. **La regola del metodo tolta e non attenuata** («non trattare il punto in cui il paziente sente»), in Cap 8 e ripetuta nella mappa §7 con la motivazione. Una regola disapplicata in silenzio si legge come una dimenticanza: la dichiarazione esplicita è ciò che la rende una scelta.

---

## BILANCIO PAROLE

Documento: **24.271 parole**. Budget di crescita netta a disposizione (5%): **1.213 parole**.

| Rilievo | Intervento | Parole |
|---|---|---|
| E1 | Riscrittura di una frase in Cap 8 | **+8** |
| E2 | «Quattro» → «Cinque» in Cap 10 | **0** |
| R1 | Sostituzioni *piano* → *meccanismo* (5 punti) | **0** |
| R2 | Riga sui meccanismi 4 e 5 in Cap 12 | **+52** |
| R3 | Riga sui fluorochinoloni in Cap 12, strumento 1 | **+26** |
| P1 | Rimozione di Vicenzino 1996 dal box Biomeccanico | **−6** |
| P2 | Completamento cella tabella Cap 6 | **+4** |
| P3 | Clausola operativa per *lesione primaria* in Cap 8 | **+18** |
| | **Totale netto** | **+102 parole · +0,42%** |

Nessuna aggiunta di contenuto clinico: quattro rilievi su otto costano zero o meno di zero, e i tre che aggiungono testo **spostano** materiale già presente (Day 2021 da Cap 11, lo stop dei fluorochinoloni da Cap 9, la ricostruzione a monte da Cap 8) portandolo al suo punto d'uso. Margine residuo per l'editor: **1.111 parole**.

---

## TIENE

Sette giunture su nove reggono, e tre reggono in modo notevole. La **giuntura 4** — l'effetto della seduta contro l'effetto della ripetizione, quella che gli osteopati sbagliano più spesso — non è solo coerente: è dichiarata, spiegata e motivata («ciò che porta l'effetto oltre la seduta non è l'escursione guadagnata, che da sola non persiste»). La **giuntura 6** è chiusa con la stessa frase parola per parola in due capitoli, e il documento dice ad alta voce che lo sta facendo. La **giuntura 7**, che nessun altro revisore legge in fila, regge su tutti e tre i criteri: quindici slot, nessun dato ripetuto fra due di essi, quattro che restringono lo spazio invece di allargarlo. E il caso canonico della giuntura 1 — la leva dell'attivazione negata dal ragionamento e dichiarata dalle leve — qui **non si verifica**: Cap 8 e Cap 11 la chiamano con lo stesso nome, la agganciano allo stesso meccanismo e allo stesso studio, e Cap 8 arriva a spiegare *perché* le due convergono sullo stesso sistema inibitorio. È l'esito atteso di una sintesi fatta bene.

---

## VERDETTO: **Sfasato**

Il documento non si contraddice come impianto: si contraddice in un punto, e in tre punti si sfasa. La contraddizione unica siede però esattamente sulla giuntura 1, ed è del tipo peggiore — il capitolo del ragionamento nega al paziente sensibilizzato la leva con le prove migliori dell'intero documento, mentre altri tre punti del testo gliela concedono. Corretta quella frase e sistemato il conteggio di Cap 10, la Bibbia è coerente.

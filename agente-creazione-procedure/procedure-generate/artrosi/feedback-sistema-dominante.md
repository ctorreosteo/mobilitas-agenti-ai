# Feedback — Revisore Sistema Dominante (Motore Clinico)

LENTE: Motore Clinico — ragionamento del Sistema Dominante (aderenza al metodo)
CONDIZIONE: Artrosi (ginocchio e anca)
DOCUMENTI REVISIONATI: `procedure-generate/["artrosi"]/v1-draft.md` (procedura) e `v1-scheda.md` (scheda operativa), v1.0

---

## VERIFICA DI ADERENZA AL METODO

Il motore c'è, ha una sezione dedicata ("Come decido su quale modello agire per primo") e non è un elenco di tecniche: c'è l'iceberg, c'è la prova della chiave di volta, c'è una road map, c'è il modificatore-trauma, ci sono i segnali di dominanza per tutti e cinque i modelli. Ma il motore gira a vuoto in tre punti: **dichiara una gerarchia che non ordina mai**, **non fa cambiare la seduta per tre modelli su cinque**, e **lascia il livello più alto — lo stato di allarme — senza un blocco di trattamento**, degradandolo a modificatore di dose. Il risultato è che la procedura sa diagnosticare il dominante nei casi facili (anca rigida, sensibilizzato franco) e si blocca esattamente nei casi in cui il ragionamento del dominante servirebbe: il paziente co-positivo su tre modelli.

Sul CP/CC: l'inversione dichiarata in Parte 0 ("nell'artrosi la regola *non trattare il CP* va sospesa, tratta bersaglio **e** catena") è motivata bene ed è ancorata a Deyle. Non è un errore — è l'unico punto in cui il documento contraddice il metodo consapevolmente e con argomento. Ma la lista dei CC che dà nella stessa riga non ricompare mai nelle sezioni operative.

---

## ERRORI — il ragionamento è assente o invertito

### E1. La gerarchia è dichiarata ma non è mai ordinata
**Sezione:** Parte 0 → "Come decido su quale modello agire per primo" → paragrafo *"Dove c'è più evidenza ≠ chi comanda qui"*.

Il testo dice: *"Si indaga dall'alto verso il basso: il dominante è il modello più a monte disfunzionale — quello che, se non lo tocchi, tiene in ostaggio gli altri."* Ma **da nessuna parte il documento dice quale dei cinque modelli sta più a monte.** I cinque modelli non hanno una gerarchia intrinseca: senza un ordine esplicito, "dall'alto verso il basso" è un'istruzione vuota. Peggio, il documento ne implica tre diversi e incompatibili:

- l'esposizione di Parte 0 apre col **Biomeccanico** e chiude col **Comportamentale**;
- la Road Map ordina **neurologico → respiratorio-circolatorio → biomeccanico → metabolico+comportamentale**;
- Parte I ("Efficacia basata sull'eziologia") elenca **biomeccanico → comportamentale → metabolico → neurologico → anca → red flag**.

Tre ordini diversi in tre sezioni dello stesso documento. Il junior non ha modo di sapere quale seguire.

**Correzione:** scrivere, in una riga dentro quel paragrafo, l'ordine di comando valido per questa condizione e motivarlo in mezza riga ciascuno — per esempio: *neurologico (allarme/sensibilizzazione) → comportamentale (credenza che governa il carico) → metabolico (carico assoluto) → respiratorio-circolatorio (versamento che inibisce il muscolo) → biomeccanico (distribuzione del carico)*. Poi **riordinare con quella sequenza** l'esposizione di Parte 0, i sottotipi di Parte I e la Road Map, così che le tre liste dicano la stessa cosa. Riportare la Road Map ordinata anche nella scheda, che oggi non ha nessun percorso decisionale (§4 dice solo "segue il dominante").

### E2. Il dominante identificato non cambia la seduta per tre modelli su cinque
**Sezione:** Parte III → "Strategia di trattamento", premessa + "La prima seduta, montata (≈50 min)"; Parte III → "Il piano delle 6 sedute"; scheda §4.

La procedura promette che *"la sequenza segue il dominante, non un ordine fisso"*, poi fornisce **due sole varianti**: `Biomeccanico-dominante: A (15') → B (10') → C (10')` e `Sensibilizzato: educazione e dosi basse → B a range ridotto → A → C conservativo`. Non esiste una variante per il **comportamentale-dominante**, per il **metabolico-dominante**, per il **respiratorio-circolatorio-dominante**. E la tabella delle 6 sedute è identica qualunque sia il dominante.

È l'errore più costoso perché colpisce proprio il modello che il documento stesso definisce *"il moltiplicatore del danno funzionale"* e *"il livello che decide se il risultato dura"*: il paziente kinesiofobico riceve la sequenza biomeccanica di default, con il counseling in coda dopo gli esercizi e la paura al **passo 5** della Road Map, dietro alla catena adiacente. Un dominante che non cambia l'ordine della seduta, il tempo assegnato e cosa si consegna a casa **non è un dominante: è un'etichetta**.

**Correzione:** aggiungere tre righe di variante accanto alle due esistenti, con la stessa granularità (blocco che va per primo, minuti, cosa si consegna):
- *Comportamentale-dominante:* mappa delle attività perse + chair-stand dimostrato prima/dopo (10') → esposizione graduata al gesto temuto (10') → A ridotto (10') → B breve, solo per rendere tollerabile il gesto → obiettivo concreto a due settimane. Il tempo maggiore va al blocco C, non ad A.
- *Metabolico-dominante:* counseling e rinvio strutturati **all'inizio** della seduta (non in coda), aspettativa dichiarata al paziente ("le mie mani qui valgono poco finché non si muove la leva"), ciclo più corto, criterio di chiusura esplicito.
- *Respiratorio-circolatorio-dominante (articolazione versata):* scarico e carico ciclico → **niente rinforzo oggi** → rivalutazione del versamento alla seduta successiva prima di aprire il blocco C.

Poi spostare, nella Road Map, la domanda su paura/credenza dal passo 5 al passo che le compete secondo l'ordine fissato in E1, e sdoppiare l'attuale passo 5 (che oggi impacchetta insieme peso, sonno e paura — due modelli diversi in un passo solo).

### E3. Il livello più alto — lo stato di allarme — non ha un blocco di trattamento
**Sezione:** Parte 0 → "Il modello Neurologico"; Road Map passo 2; Parte IV → "Reset Neuro-Meccanico".

Nel documento il "Neurologico" è ridotto a **guadagno nocicettivo/sensibilizzazione**. Manca completamente l'altra faccia, che nel metodo è il Comandante Supremo: lo **stato di allarme autonomico**, con i suoi segnali operativi (respiro accelerato, tessuti che rimbalzano ogni correzione, il paziente che non "stacca", sonno che non ristora). Conseguenze concrete:

- i "Segnali di dominanza" del modello Neurologico (Parte 0) elencano solo dolore diffuso, allodinia, sonno frammentato: **nessun segno rilevabile con le mani in trenta secondi**;
- la Road Map al passo 2 risponde all'allarme **abbassando la dose** (*"dosi basse, tecniche indolori, educazione prima delle mani"*): è una precauzione, non un trattamento del livello. Nel metodo il passo 1 è *calmare il sistema*, non *toccarlo di meno*;
- il "Reset Neuro-Meccanico" di Parte IV, malgrado il nome, è un blocco articolare e di tessuti molli: differenziazione anca/ginocchio, mobilizzazione grado I-II, inibizione, isometrie, due frasi di educazione. Non c'è un solo item diretto al tono autonomico;
- l'unico strumento che agisce lì — *"contatto calmo e non doloroso, down-regulation aspecifica"* — è **archiviato nel blocco Psico-Emotivo** (Riattivazione e Co-regolazione, punto 3) e non viene mai richiamato dal passo neurologico della Road Map. Lo strumento esiste, è al piano sbagliato e nessuno lo va a prendere.

**Correzione:** (a) aggiungere ai "Segnali di dominanza" del modello Neurologico i marker rilevabili in stanza — frequenza respiratoria a riposo, tessuto che rimbalza a ogni correzione, il paziente che non lascia il peso sul lettino; (b) trasformare il passo 2 della Road Map da regola di dose in **azione**: contatto lento sostenuto, lavoro respiratorio/diaframmatico, decubito comodo, prima di qualunque mobilizzazione, con re-test del respiro e del rimbalzo tissutale; (c) spostare o duplicare il punto "down-regulation aspecifica" dentro il Reset Neuro-Meccanico, mantenendo la formulazione onesta già usata (effetto aspecifico, nessun meccanismo neuroendocrino rivendicato — nulla qui chiede un claim in più).

---

## RISCHI — il ragionamento c'è ma è incompleto

### R1. "Misura ogni livello" non ha strumenti per tre livelli su cinque, e non c'è tie-break
**Sezione:** Parte 0 → "Il metodo, in tre mosse", mossa 2.

La mossa 2 ordina: *"Misura ogni livello… cerca il livello più disfunzionale, non il primo che trovi"*. Ma gli strumenti elencati subito dopo sono **tutti biomeccanici**: ROM di anca/ginocchio/caviglia, forza di quadricipite e abduttori, chair-stand, qualità del passo. Non c'è un marker per il neurologico (soglia/allodinia, dolorabilità sul lato sano, qualità del sonno), né per il comportamentale (attività perse contate, disponibilità a caricare, un indice di kinesiofobia), né per il metabolico (peso registrato, variazione, sarcopenia). Con questi strumenti il "livello più disfunzionale" risulterà **sempre** il biomeccanico, per costruzione.

Aggravante: manca la regola di priorità quando più modelli sono positivi insieme — cioè il caso normale (paziente di 95 kg, anca rigida, che ha smesso di camminare per paura). Il documento dice cosa fare se uno domina, non come si sceglie fra tre.

**Correzione:** dare a ogni livello un marker misurabile e annotabile, uno solo, alla mossa 2 (es. neurologico = dolorabilità pressoria sul lato sano sì/no + sonno; comportamentale = numero di attività abbandonate + il paziente carica quando il test dice che tollera sì/no; metabolico = peso e variazione negli ultimi 12 mesi; respiratorio-circolatorio = sweep test, già presente). Aggiungere una riga di tie-break coerente con l'ordine di E1: *a parità di positività vince il modello più a monte; se restano due, decide la prova della chiave di volta.*

### R2. La prova della chiave di volta non misura la cascata
**Sezione:** Parte 0 → mossa 3; scheda §4, riga "Come lo identifichi".

La scheda definisce correttamente il dominante come *"quello la cui correzione dà la cascata più ampia al re-test"*. Poi però il test operativo che entrambi i documenti prescrivono è: tratti in prova e **ri-misuri chair-stand + VAS**. Sono due misure di **esito**, non una cascata: dicono se il paziente è migliorato, non se gli altri livelli hanno ceduto. Nel metodo la prova serve a vedere se, liberato il sospetto primario, **anche gli altri marker si sbloccano** — è così che si distingue il dominante dal compenso.

**Correzione:** dopo il trattamento in prova, ri-misurare **i marker degli altri livelli**, non solo l'esito: knee-to-wall e rotazione interna d'anca (biomeccanico), attivazione del quadricipite / versamento (circolatorio), dolorabilità sul lato sano (neurologico), disponibilità a fare il gesto temuto (comportamentale). Regola in una riga: *se cede solo il tuo bersaglio, hai trattato un compenso; se cedono anche gli altri, era il dominante.* Chair-stand e VAS restano l'esito, non la prova.

### R3. Il segnale di dominanza metabolica è mal attribuito e contraddice la regola di ri-pesatura
**Sezione:** Parte 0 → "Il modello Metabolico-Energetico", *Segnali di dominanza*.

Fra i segnali di dominanza metabolica il documento mette *"ogni progresso manuale che evapora in una settimana"*. Nel metodo quello è il segnale generico di **dominante sbagliato** — l'iceberg: *"lavora sulla punta senza toccare il sommerso e il paziente sta meglio una settimana, poi torna"*, come il documento stesso scrive tre paragrafi sopra; ed è, in forma specifica (recidiva identica a 24h), il segnale di resistenza viscerale. La procedura si contraddice: alla tabella delle sedute e al "bivio della 3ª seduta" dice giustamente *"se non arriva risposta entro tre sedute, l'ipotesi sul dominante era sbagliata"*. Con l'attribuzione attuale, il junior il cui paziente ricade a una settimana conclude "è il peso", parte col counseling e **non ripesa mai il dominante**.

**Correzione:** togliere quella riga dai segnali metabolici e spostarla fra i criteri di ri-pesatura del dominante (bivio della 3ª seduta). Sostituirla con segnali propri del metabolico: correlazione del sintomo con le variazioni di peso documentate, sarcopenia obiettivabile, sonno non ristoratore che precede il peggioramento, comorbilità metaboliche note.

### R4. Il modificatore-trauma è fuori dalla Road Map e fuori dalla scheda
**Sezione:** Parte 0 → "Cerca in anamnesi il modificatore-trauma" (paragrafo isolato, dopo la Road Map); scheda §2-§3.

Il paragrafo è corretto e ben scritto — la distorsione mai riabilitata, la meniscectomia, la domanda *"che incidenti, distorsioni o interventi hai avuto, anche da giovane?"*, il segnale del tessuto denso e poco mobile lontano dal dolore. Ma **non è uno dei cinque passi della Road Map** e non compare da nessuna parte nella scheda operativa. Il junior che in stanza segue i cinque passi (l'unica cosa che riesce a seguire mentre ha le mani addosso) non chiede mai di quel trauma. Ed è ironico, perché il trauma distale è proprio ciò che rende vera la tesi centrale della procedura: il carico arriva storto per un motivo che sta lontano dal ginocchio.

**Correzione:** inserire il trauma come passo esplicito della Road Map, prima del passo sulla catena (*"C'è un vecchio trauma o una cicatrice? → tessuto denso, poco mobile, spesso lontano dal dolore; chiedi degli incidenti di tutta la vita, non degli ultimi mesi"*), e aggiungere la domanda d'anamnesi nella scheda, in §2 o §3.

### R5. CC/CP resta nominale nelle sezioni operative
**Sezione:** Parte 0 → mossa 3 (lista dei CC); Parte III → blocchi A/B; Parte IV → Reset Neuro-Meccanico.

I Centri di Coordinazione sono nominati una volta sola, in coda alla mossa 3 (TFL/tratto ileotibiale, vasto laterale, popliteo, tricipite surale al ginocchio; glutei, piriforme, ileopsoas, quadrato dei lombi all'anca) e **non ricompaiono mai** nelle sezioni che dicono cosa fare con le mani. Nel blocco B e nel Reset Neuro-Meccanico l'inibizione dei tessuti molli elenca invece *"vasto laterale, popliteo, zampa d'oca, glutei"*: la zampa d'oca è, nella stessa procedura (test 5), un **sito di dolorabilità** — cioè un CP, trattato direttamente senza che il documento lo dichiari. L'inversione dichiarata in Parte 0 copre l'articolazione bersaglio, non l'estensione silenziosa ai punti dolenti periarticolari. Manca inoltre il **re-test immediato CC→CP**: l'unico re-test previsto (chair-stand prima/dopo) è a fine seduta.

**Correzione:** nei blocchi A/B e in Parte IV marcare accanto a ogni punto se è **CC di sequenza** o **CP sintomatico**, e imporre dopo ogni CC il re-test immediato del gesto doloroso ("liberato questo, il gesto migliora adesso o no?"). Se non migliora, si cambia CC o piano — non si insiste sul CP.

---

## PREFERENZE — raffinamenti del metodo

### P1. La componente viscero-somatica non viene mai interrogata per anca e lombare
Nel nuovo impianto il viscerale non è un modello a sé, ma la domanda resta parte dell'indagine — e per l'anca e il rachide lombare non è peregrina (ileopsoas che si ritensiona di seduta in seduta, ritmo digestivo o urinario, recidiva identica a 24h). Basterebbe una domanda in anamnesi e una riga fra i criteri di ri-pesatura del dominante alla 3ª seduta.

### P2. "Leggi a chi parli" non è agganciata alla decisione
I tre stati (in difesa / emotivo / razionale) sono descritti bene ma restano un consiglio relazionale. Nel metodo sono **parte dell'indagine**: il paziente emotivo sposta il sospetto sul comportamentale, quello in difesa sul livello di allarme. Aggiungere mezza riga per stato che dica quale sospetto rafforza e quale variante di seduta attiva (aggancio diretto a E2).

---

## TIENE

- **La ricerca del colpevole lontano dalla scena del crimine è il punto forte del documento**: catena adiacente, nervo otturatorio che porta il dolore d'anca al ginocchio mediale, catena controlaterale, la caviglia rigida da una distorsione di vent'anni fa. Il "trattare la causa e non il sintomo" qui è sostanza, non slogan.
- **L'inversione della regola CP è dichiarata, motivata e circoscritta** ("tratta il bersaglio **e** la catena, non al posto della catena"). È il modo corretto di contraddire il metodo: consapevolmente, con un argomento e con un limite.
- **Il non-responder è gestito come segnale, non come invito a spingere**: bivio della 3ª seduta, ri-pesatura del dominante, ricontatto del medico. Il campo "Modello dominante di questo paziente: ______" nella scheda è un buon vincolo — costringe a scrivere una tesi prima di trattare.

---

## IL SISTEMA DOMINANTE DI QUESTA PROCEDURA

Provando a ricostruire il ragionamento con questo documento e nient'altro: davanti a un paziente con anca rigida, dorsiflessione ridotta e dolore che cambia se modifico l'assetto, arrivo senza esitazioni al **biomeccanico** e so cosa fare, con che ordine e con che tempi. Davanti a un paziente con dolore diffuso, allodinia e sonno rotto arrivo al **neurologico**, ma da lì la procedura mi dice solo di abbassare la dose — non di trattare quel livello. Davanti al paziente vero — 95 kg, anca rigida, ha smesso di camminare per paura, ricade a una settimana — **il documento non mi porta a una risposta**: tutti e tre i modelli sono positivi, non c'è un ordine che li ranghi, la mossa 2 misura solo il biomeccanico, la prova della chiave di volta misura l'esito e non la cascata, e comunque per due di quei tre modelli la seduta resterebbe identica. Il motore c'è ed è ben scritto; è la trasmissione che manca — fra la diagnosi del dominante e ciò che cambia in stanza.

---

**VERDETTO: Metodo presente ma incompleto.**
Il ragionamento del sistema dominante è esposto, non elencato, e in un punto contraddice il metodo con argomento — ma dichiara una gerarchia che non ordina, misura un livello su cinque, e per tre modelli su cinque la diagnosi del dominante non cambia una sola riga della seduta.

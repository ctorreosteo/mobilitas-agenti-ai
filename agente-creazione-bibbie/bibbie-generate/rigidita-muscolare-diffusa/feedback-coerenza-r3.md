# Feedback — Revisore di 3º livello: Coerenza interna (l'Ispettore delle Giunture)

**LENTE:** Coerenza interna — l'Ispettore delle Giunture
**CONDIZIONE:** Rigidità muscolare diffusa
**DOCUMENTO REVISIONATO:** `bibbie-generate/rigidita-muscolare-diffusa/v3-intermedia.md` (24.346 parole) + `mappa-v3.md` (1.428 parole)
**Data:** 1 settembre 2026

---

## LE NOVE GIUNTURE

| # | Giuntura | Esito | Nota |
|---|---|---|---|
| 1 | Ragionamento (C8) × Leve (C11) | **COERENTE, con uno sfasamento** | Il caso canonico è stato patchato bene: il paziente B con driver «livello di attivazione» riceve la stessa frase in C8 e in C11 («la leva ce l'hai... IPOTESI, né una di più né una di meno»), e C8 chiude con «hai **più** da fare, non meno». Nessuna leva negata. Resta un disallineamento sui **marker** (R1). |
| 2 | Meccanismi (C5) × Leve (C11) | **COERENTE** | C11 ha cinque sezioni intestate ai cinque meccanismi per nome e nello stesso ordine. Nessuna leva orfana. Il meccanismo 5 dichiara esplicitamente «su niente che duri». Il meccanismo 4 rimanda il proprio effetto durevole al meccanismo 2, invece di rivendicarlo. |
| 3 | Meccanismi (C5) × Strumenti attivi (C12) | **COERENTE, con un silenzio** | Ogni strumento aggancia un meccanismo per nome (S1→1 e 3, S2→1 e 2, S3→2, S4→1 «e su nessun altro», S5→3). Il meccanismo 4 non ha strumento attivo e il silenzio non è dichiarato (P2). |
| 4 | Leve (C11) × Strumenti (C12) — seduta vs ripetizione | **COERENTE** | È la giuntura meglio tenuta del documento. «Il ciclo si muove, il singolo contatto no» (C11) regge in C12 (programmi 6-24 settimane, detraining di Bidonde), e il «Perché ci sei tu» di C5 attribuisce esplicitamente il calo di Nitta all'esercizio del paziente e non alla mano. |
| 5 | Scienza (C10) × Etichette | **INCOERENTE — due errori** | Un'etichetta sfasata sulla stessa affermazione (E1) e la regola del ponte enunciata in forma assoluta in C10 e violata tre volte in C11 (E2). |
| 6 | Limiti di campo (C9) × Cosa dire al paziente (C13) | **COERENTE sul reperto, SFASATA sul consenso** | La convivenza reperto/inquadramento arriva al paziente **con le stesse parole** in C9 (frase del giallo) e in C13 (script): controllo superato in modo esemplare. Ma una delle quattro righe di consenso di C9 non compare in C13 (R2). |
| 7 | I quindici slot «Perché ci sei tu» | **COERENTE** | Quindici slot, quindici presenti, tutti con i tre elementi e con il terzo mai generico. Almeno cinque **restringono** (C0, C6 «Su questo pattern non ci sei», C8, C10 «Non ti autorizza a dire che funziona», C12). Il documento non sta vendendo. Un solo dato compare in due slot (P3). |
| 8 | Il lessico | **INCOERENTE** | I termini canonici del metodo tengono (marker, reperto disfunzionale, disfunzione somatica, compenso, sistema dominante: una definizione, un significato, e *lesione primaria* correttamente assente e dichiarata assente). Cedono tre voci non canoniche fra testo e Glossario (R3). |
| 9 | Sottotipi (C6) × Leve (C11) × Triage (C9) | **COERENTE sul pattern E, AMBIGUA sull'apertura** | Il pattern E è un'uscita in tutti e tre i punti, senza eccezioni. Il pattern C non è più «puoi poco» in nessun capitolo (correzione applicata bene ovunque). Ma l'«In una riga» di C6 promette un pattern «su cui puoi meno di quanto vorresti» e non lo nomina (P1). |

---

## ERRORI — il documento afferma due cose incompatibili

### E1 · Giuntura 5 — la stessa affermazione porta due etichette diverse

- **Capitolo 5, meccanismo 4 dice:** «**DIMOSTRATO** *(studi sull'uomo, solidi)* che lo scorrimento fra gli strati sia ridotto di circa un quinto nella **lombalgia cronica**: 71 pazienti contro 50 controlli, ecografia dinamica (Langevin, PMID 21929806).»
- **Capitolo 7, Biomeccanico dice:** «**PROBABILE** *(razionale forte, prove parziali)* che lo scorrimento fra gli strati fasciali sia ridotto nella lombalgia cronica (Langevin, PMID 21929806).»
- **E la Mappa dice:** «Tessuto che non scorre — **PROBABILE il reperto**, IPOTESI la leva.»

Stessa affermazione, stessa fonte, stessa restrizione di popolazione, due etichette. È lo sfasamento che la giuntura 5 chiama «il più insidioso», perché ogni singola occorrenza sembra corretta.

**QUALE LATO CORREGGERE: il Capitolo 5.**
**Perché:** due occorrenze su tre dicono PROBABILE, e la fonte è **uno** studio trasversale, su una popolazione diversa, con le correlazioni funzionali significative **solo nei maschi** (limite che il Capitolo 3 dichiara e che il Capitolo 5 non ripete). «Studi sull'uomo, solidi» è al plurale: la definizione dell'etichetta non è soddisfatta.
**Come:** in C5 meccanismo 4, sostituire `DIMOSTRATO *(studi sull'uomo, solidi)*` con `PROBABILE *(razionale forte, prove parziali)*`. Il resto della riga — «Non pazienti con rigidità diffusa, ed è un confronto fra gruppi, non una causa» — resta identico e regge già l'etichetta più bassa.
**Costo: +2 parole.**

> Se l'autore intendeva due cose diverse (il *reperto* misurato in C5, il *trasferimento* alla rigidità diffusa in C7), allora è la formulazione di C5 a essere incompleta: deve dire di che cosa esattamente è DIMOSTRATO. Ma le due frasi affermano oggi la stessa identica proposizione, quindi la correzione minima è l'allineamento.

---

### E2 · Giuntura 5 — la regola del ponte è enunciata come assoluta e violata tre volte

- **Capitolo 10 dice** (box «Attenzione», il criterio che separa i due conteggi): «Massaggio, rilascio miofasciale e manipolazione toracica stanno nel cerchio 2, insieme alle loro centinaia di pazienti: sono interventi diversi su popolazioni diverse, e **alzano l'etichetta del meccanismo, mai quella della nostra leva su questa condizione**.»
- **Capitolo 11 dice**, su tre leve su cinque, esattamente il contrario:
  - meccanismo 3: «**PROBABILE** sull'**effetto**: nella fibromialgia il massaggio... (Li, PMID 24586677). Il rilascio miofasciale ha effetti grandi sul dolore... (Yuan, PMID 25457196). **È l'etichetta manuale più alta del documento, ed è la ragione per cui il pattern C prende "abbastanza" e non "poco".**»
  - meccanismo 4: «**PROBABILE** che un **ciclo** di lavoro manuale riduca la rigidità misurata» (Jelen, PMID 39253625 — massaggio, donne giovani sane).
  - meccanismo 4: «**PROBABILE** sull'escursione» (Yang, PMID 38759063 — manipolazione toracica, pazienti con dolore cervicale).

Tutte e tre le etichette sono **etichette di leva su questa condizione**, e tutte e tre poggiano su fonti che C10 colloca nel cerchio 2. Non è un dettaglio bibliografico: dalla prima dipende la colonna «Quanto puoi fare» del pattern C, cioè una decisione clinica.

**QUALE LATO CORREGGERE: il Capitolo 10.**
**Perché:** il resto del documento è costruito sulle etichette di C11 — il pattern C, la Road Map, la Mappa, il «Perché ci sei tu» di C11 — e quelle etichette sono già accompagnate ovunque dalla frase-ponte che dichiara il salto («Pazienti con fibromialgia, non tutti quelli con rigidità diffusa»). Abbassarle sarebbe una decisione di evidenza, chiusa al 2º livello. È la formulazione **assoluta** di C10 a essere l'anomalia: lo stesso capitolo, venti righe più sotto, già ammette il contrario quando scrive che i settantaquattro pazienti sono «il c1 **delle nostre mani**, che è un sottoinsieme del c1», e quando nella tabella degli studi cardine attribuisce a Jelen (`c2`) il diritto di autorizzare una frase su un ciclo manuale.
**Come:** riformulare la clausola finale del box di C10 così che dica ciò che il documento pratica davvero — il cerchio 2 può reggere l'etichetta dell'**effetto di un intervento vicino**, dichiarato con la sua frase-ponte, ma non l'etichetta del **nostro pacchetto osteopatico su questa condizione**, che resta ferma ai settantaquattro pazienti. Proposta: «...sono interventi diversi su popolazioni diverse: possono reggere l'etichetta dell'**effetto misurato su quell'intervento**, dichiarato con la sua frase-ponte, mai quella del **trattamento osteopatico** su questa condizione, che resta ai settantaquattro pazienti.»
**Costo: +22 parole** (sostituzione di 18 parole con 40).

---

## RISCHI — non si contraddicono, ma si sfasano

### R1 · Giuntura 1 — il marker che decide e lo strumento che non lo vede

**Cosa non combacia.** Il Capitolo 11 avverte, in un box «Per te» esplicito: «Su **Yang**, l'effetto sulla rotazione cervicale (SMD 0,23) sta **sotto** la soglia di dieci gradi che usi per quel marker: **non rimisurare la rotazione cervicale per verificare *questa* leva**, perché lo strumento non è abbastanza fine per vederla.» Il Capitolo 8, nella tabella «Quale marker verifica quale piano», assegna la **rotazione cervicale attiva** come marker che decide su **due righe su cinque** (tronco/catena posteriore/lombare; bacino e arto inferiore) e la usa nel paziente-esempio A («il marker che rimisuri a fine seduta è la rotazione cervicale»). Se un effetto *diretto* sul distretto cervicale non raggiunge la soglia dichiarata, un effetto *remoto* la raggiunge ancora meno: il lettore che segue C8 alla lettera concluderà «il piano non era quello» in casi in cui lo strumento non poteva vedere niente.

**Quale lato allineare: il Capitolo 8.** L'avvertenza di C11 è ancorata al dato ed è già scritta; C8 la ignora perché è stata scritta prima. Non si tocca la soglia (è una decisione di evidenza) e non si tocca la regola del marker fuori piano (regge).

**Cosa lo allineerebbe.** Sotto la tabella «Quale marker verifica quale piano», una riga che porti lì la stessa avvertenza già presente in C11: che la rotazione cervicale ha una soglia di dieci gradi che le dimensioni d'effetto note della leva manuale non raggiungono, quindi un re-test negativo su quel marker non falsifica l'ipotesi di piano — e che quando il piano trattato è il tronco o il bacino il marker che pesa resta l'inter-seduta (tempo di sblocco). **Costo: +35 parole**, spostate da C11 e dal box «Attenzione» che già dice «il tempo di sblocco della mattina dopo vale più di qualunque misura di fine seduta».

---

### R2 · Giuntura 6 — una riga di consenso che al paziente non viene mai detta

**Cosa non combacia.** Il Capitolo 9, «Cosa dichiari nel consenso», impone quattro righe, e la terza è: «Che **l'evidenza di terapia manuale su questa presentazione è scarsa e a breve termine**, e che **la leva con le prove migliori è l'attività fisica**.» Il Capitolo 13 — l'unico posto in cui il documento mette in bocca all'osteopata le frasi da dire — non la contiene: né nello script, né nelle quattro obiezioni, né nell'elenco «Cosa non promettere mai, **e cosa dire sempre**», che ne raccoglie tre (non promettere che passi, non promettere che non torni, non dire «non hai niente») più l'obbligo sulla convivenza reperto/inquadramento. Lo script dice «ti do il modo di non farle richiudere»: è un'allusione al movimento, non la dichiarazione richiesta.

È la stessa classe di difetto che la giuntura 6 intercetta sul reperto — dove il documento invece è esemplare, perché la frase del giallo e lo script coincidono quasi parola per parola. Qui l'obbligo è dichiarato fra colleghi e non arriva al paziente: una gerarchia di leve dichiarata solo nel consenso non è una gerarchia dichiarata.

**Quale lato allineare: il Capitolo 13.** C9 è il lato ancorato (è l'obbligo di consenso, ed è coerente con C0, C10 e C12, dove la stessa frase compare tre volte). C13 va completato, non C9 alleggerito.

**Cosa lo allineerebbe.** Aggiungere all'elenco «cosa dire sempre» di C13 la quarta voce, con le parole già usate in C12: che la leva con le prove migliori su questa condizione non è la mano ma il movimento, e che è per questo che una parte della seduta si spende a insegnarlo. **Costo: +25 parole.**

---

### R3 · Giuntura 8 — tre voci in cui una parola non ha un solo significato

Tre difetti distinti, tutti nella stessa giuntura, tutti a costo quasi zero.

**a) «Catena» ha tre significati.** Il Glossario la definisce in un solo senso — «un insieme di strutture collegate che si influenzano a distanza». Nel testo compare **sei volte** come intestazione della sequenza causale di un meccanismo («La catena:», C4 e C5), una volta come «la catena biochimica con cui si racconta» (C5, meccanismo 4), e una sola volta nel senso del Glossario, «catena posteriore» (tabella marker di C8). Il senso definito è quello meno usato.
→ **Correzione:** rinominare le intestazioni `La catena:` in `La sequenza:` (C4 e le cinque di C5) e lasciare *catena* al senso del Glossario. **Costo: 0 parole.**

**b) Un termine del Glossario che nel testo non esiste.** «**Modulazione condizionata del dolore**» compare **solo** a Glossario. Il testo chiama la stessa cosa «**freno discendente**» (5 occorrenze, con un paragrafo intestato in C3) e «**modulazione discendente**» (3 occorrenze, dentro i box di O'Brien). Il termine più usato e più portante del documento non ha voce a Glossario; quello che ce l'ha non è mai usato. È il controllo che la giuntura 8 chiede in entrambe le direzioni.
→ **Correzione:** intestare la voce del Glossario a «**Freno discendente (modulazione discendente, modulazione condizionata del dolore)**», tenendo il testo della definizione che c'è già. **Costo: +6 parole.**

**c) «Livello tonico» contro «livello di attivazione di fondo».** Il Glossario definisce «Effetto di stato / **livello tonico**»; il testo dice quasi sempre «**livello di attivazione di fondo**» (C10, C11), una volta «livello di attivazione tonico» (C11) e una volta «attività tonica» (C11, meccanismo 4). Sono la stessa grandezza, e su di essa poggia l'etichetta IPOTESI del meccanismo 2 e la lettura delle due componenti della conduttanza cutanea: è esattamente il tipo di concetto su cui una variante lessicale costa comprensione.
→ **Correzione:** intestare la voce a «Effetto di stato / **livello di attivazione di fondo (livello tonico)**» e usare quella forma nelle tre occorrenze di C11. **Costo: +4 parole.**

---

## PREFERENZE (max 3)

**P1 · Giuntura 9 — l'«In una riga» del Capitolo 6 non nomina il pattern.** Dice: «cinque pattern, uno dei quali non è un bersaglio ma un cancello — e **su un altro puoi meno di quanto vorresti**». Il pattern non viene nominato, e i due che il lettore sceglierebbe sono entrambi negati altrove: su **C** il capitolo stesso scrive «la frase corretta **non** è "qui la tua mano conta poco"», e su **B** il Capitolo 8 chiude con «è quello in cui hai **più** da fare, non meno». Per esclusione è il pattern **A** — margine «Molto», ma quasi tutto fuori dalla seduta. È un residuo della sintesi che ha promosso C da «poco» ad «abbastanza» senza rileggere l'apertura.
→ **Correzione:** nominarlo. «...e sul più frequente, il pattern A, quasi tutto quello che puoi fare sta fuori dalla seduta». **Costo: +6 parole.**

**P2 · Giuntura 3 — il meccanismo 4 non ha strumento attivo, e il silenzio non è dichiarato.** Quattro meccanismi su cinque hanno uno strumento del Capitolo 12 che li aggancia per nome; il meccanismo 4 no. Il documento è per il resto scrupoloso nel dichiarare le assenze (la metà circolatoria «qui non pesa, e lo dichiaro perché non sembri dimenticata»; il meccanismo 5 «su niente che duri»; l'educazione al dolore «controllata e non apre uno strumento»). Qui il silenzio si legge come dimenticanza.
→ **Correzione:** una clausola in C12, con il materiale già presente in C5 (dove il passo 5 della catena dice che la riduzione di ampiezza toglie il movimento che scioglierebbe il meccanismo 1): dire che sul meccanismo 4 il paziente da solo agisce solo per via indiretta, attraverso l'ampiezza degli Strumenti 1 e 2. **Costo: +15 parole.**

**P3 · Giuntura 7 — un dato in due slot.** Lo slot di C8 usa Walton (algometro 0,79-0,90) «contro un kappa che sulla durezza palpata scende sotto il caso»; lo slot di C14 è interamente quel kappa (Beynon, PMID 30524705). Il dato di Beynon regge quindi due slot su quindici. È l'unico caso, ed è difendibile come contrasto — ma la regola dei quindici slot è «nessun dato ripetuto».
→ **Correzione:** in C8 sostituire il comparatore con una formula che non porti il dato («contro un reperto la cui affidabilità non migliora addestrandosi»), lasciando il numero al solo slot di C14. **Costo: 0 parole.**

---

## PROPOSTA DI DECIMA GIUNTURA

**«Le soglie dichiarate dei marker» × «Le dimensioni d'effetto dichiarate delle leve».**

Qui ricorre tre volte, e non è coperta da nessuna delle nove: la rotazione cervicale ha soglia 10° e la leva manuale che le corrisponde vale SMD 0,23 (R1); il tempo di sblocco ha soglia −30% e l'esercizio che dovrebbe muoverlo porta ~8 punti su 100 da un solo studio; la soglia di pressione dolorosa ha soglia «da definire» ed è l'unico marker che misura ciò che definisce il pattern C. Un documento che dichiara sia le soglie sia le dimensioni d'effetto può, senza accorgersene, consegnare al lettore uno strumento di verifica che nessuna delle sue leve può far scattare — e il lettore leggerà quel silenzio come «l'ipotesi era sbagliata» invece che come «lo strumento non vede».

**Cosa controllerebbe:** per ogni marker con soglia dichiarata, esiste nel capitolo delle leve o degli strumenti almeno un effetto dichiarato che quella soglia la supera? Se no, va detto **accanto alla soglia**, non trenta pagine dopo.

---

## MAPPA DELLE SEI FASI DELL'APPRENDIMENTO

*(mandato del revisore gemello di 3º livello, non mio: la riporto perché richiesta, senza trarne rilievi.)*

| Fase | Stato | Dove vive |
|---|---|---|
| **Perché** (senso, motivazione) | **Presente** | C0 «Che documento è», C1 intero, C14 chiusura. Il documento apre con il paziente, non con la fisiologia. |
| **Cosa** (contenuto) | **Presente** | C2-C7, con etichette su ogni affermazione portante. |
| **Come** (procedura di ragionamento) | **Presente** | C8: ordine di interrogazione, prova della chiave di volta, Road Map in sei passi. |
| **Pratica** (esercizio guidato) | **Presente** | I quattro pazienti di C8, ciascuno con «Che cosa fai»; i sei passi di «Come si studia» in C0. |
| **Feedback** (criteri di verifica) | **Presente e forte** | Cinque marker con soglia e provenienza della soglia, tabella marker×piano, revisione a sei settimane, «se i marker non si sono mossi non è una rinuncia: è un'informazione». |
| **Autonomia** (criteri di padronanza) | **Debole** | Esiste un criterio ed è buono (C0 punto 3: «chiudi il documento e parla... di' i cinque meccanismi e i cinque pattern»), ma verifica il **richiamo**, non la **decisione**: si può recitare i cinque meccanismi e non saper condurre il triage. Il documento non dice mai come il lettore riconosce di essere pronto a decidere da solo. Non è materia mia e non produce un rilievo qui. |

---

## DA PROTEGGERE DALL'EDITOR (4º livello)

Queste ripetizioni **hanno funzione**: sono la struttura portante delle giunture che tengono. Toglierle farebbe rientrare il documento nel numero e lo farebbe uscire dalla coerenza.

1. **Le frasi-ponte su ogni fonte del cerchio 2** — «Pazienti con fibromialgia, non tutti quelli con rigidità diffusa», «in donne giovani sane», «lavoratori con dolore regionale». All'editor sembreranno boilerplate ripetuto venti volte. Sono l'unica cosa che impedisce a un'etichetta di migrare da un capitolo all'altro, e sono la ragione per cui la giuntura 5 cede in due punti soltanto invece che in dieci.
2. **Il filo «il massaggio mi dura tre giorni»**, che attraversa C1 (come lo racconta lui) → C1 «tre cose da ricordare» (è un dato clinico) → C5 → C11 (una sezione intera intestata alla frase) → C13 (obiezione con risposta). È lo stesso dato ripetuto cinque volte, ed è la spina dorsale didattica del documento: la ripetizione **è** l'insegnamento.
3. **La metafora del miele nel barattolo**, identica in C5, C13 e nella Mappa. Deve restare **identica**: è la frase che il lettore dirà al paziente.
4. **Il terzo elemento «Non ti autorizza a...» in tutti e quindici gli slot.** Sono quindici righe che sembrano ridondanti e sono l'unica ragione per cui questo documento non sta vendendo.
5. **Le dichiarazioni di rimozione e di assenza** — «la regola *non trattare il punto in cui il paziente sente* qui viene **tolta**, e lo dichiaro perché una rimozione silenziosa è indistinguibile da una dimenticanza»; «la metà circolatoria qui non pesa, e lo dichiaro perché non sembri dimenticata»; «*Lesione primaria* qui non compare, e per questo non sta nemmeno a Glossario». Cancellarle riporterebbe il documento a un'omissione muta.
6. **La doppia dichiarazione di lunghezza** (intestazione + box «Attenzione» in C12, voci D-019, D-065, D-085 del registro deviazioni). Sono la traccia della decisione, non un vezzo.
7. **La ripetizione della regola sulla durezza palpata** in C8, C9, C13 e C14: è l'unica regola del documento che contraddice l'abitudine del lettore, e quattro passaggi sono il minimo per scardinarla.
8. **La frase della convivenza reperto/inquadramento**, che compare quasi identica in C9 (triage giallo) e in C13 (script). È l'unico punto in cui il documento supera la giuntura 6 in modo esemplare **proprio perché** si ripete alla lettera.

---

## BILANCIO PAROLE

| Rilievo | Intervento | Costo |
|---|---|---|
| E1 | Sostituzione di etichetta in C5 | **+2** |
| E2 | Riformulazione della clausola del ponte in C10 | **+22** |
| R1 | Nota sotto la tabella marker×piano in C8 (materiale spostato da C11) | **+35** |
| R2 | Quarta voce in «cosa dire sempre» di C13 (parole già in C12) | **+25** |
| R3a | Rinomina `La catena:` → `La sequenza:` (6 occorrenze) | **0** |
| R3b | Rinomina voce di Glossario | **+6** |
| R3c | Rinomina voce di Glossario e 3 occorrenze in C11 | **+4** |
| P1 | Nominare il pattern nell'«In una riga» di C6 | **+6** |
| P2 | Clausola in C12 sul meccanismo 4 (materiale già in C5) | **+15** |
| P3 | Sostituzione del comparatore nello slot di C8 | **0** |
| | **TOTALE** | **+115 parole** |

**Crescita netta: +115 su 24.346 = +0,47%.** Budget: ≤ 5%. Rientrato con ampio margine.
Cinque interventi su dieci sono **spostamenti o rinomine a costo zero o quasi**; nessuno introduce contenuto clinico nuovo. Nessun taglio proposto: l'asciugatura è del 4º livello, e i punti elencati sopra vanno protetti da quella passata.

---

## TIENE

Le giunture 2, 3, 4, 6 e 7 sono solide, e la 4 — effetto della singola seduta contro effetto della ripetizione, quella che gli osteopati sbagliano più spesso — è tenuta meglio di quanto sia normale vedere: «il ciclo si muove, il singolo contatto no» è scritto in C11, ripetuto in C12 e reso operativo nel «Perché ci sei tu» di C5, che attribuisce il calo elastografico all'esercizio del paziente e non alla mano. Anche la giuntura 1, quella per cui questo ruolo esiste, **tiene**: il caso canonico — il paziente il cui driver è il livello di attivazione — è stato riconciliato in modo esplicito e con la stessa etichetta in entrambi i capitoli, e C8 arriva a scrivere che su quel paziente «hai **più** da fare, non meno». Non è un caso: è una sintesi fatta bene.

Le due incoerenze vere stanno tutte e due nella giuntura 5, cioè fra il capitolo dell'evidenza e i capitoli che portano le etichette — la giuntura che più risente delle sintesi ripetute, perché ogni feedback di 2º livello tocca un'etichetta senza rileggere le altre occorrenze della stessa affermazione.

---

## VERDETTO: **Sfasato**

Il documento non si contraddice sul ragionamento clinico, che è dove il danno sarebbe stato grave: si sfasa sulle etichette, in due punti circoscritti e correggibili con ventiquattro parole complessive, e su tre voci di lessico che costano quasi nulla.

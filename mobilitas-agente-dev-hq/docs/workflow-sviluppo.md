# Il workflow di sviluppo

Perché l'agente è fatto così. La procedura operativa sta nella skill `dev-hq-orchestratore`; qui c'è il ragionamento dietro.

---

## Il problema di partenza

Sviluppare sul gestionale ha tre caratteristiche che il workflow deve affrontare, e che non sono negoziabili perché sono fatti del progetto:

**1. La specifica è un titolo.** Nella lista HQ, 6 task su 100 hanno una descrizione. Nessuno ha priorità o tag. `Pagamenti - bug note che non si cancellano` è una richiesta completa. Il lavoro di capire *cosa* fare è grande almeno quanto quello di farlo — quindi merita una fase sua.

**2. Il lavoro attraversa due repo.** Frontend React e backend Spring. Un campo nuovo in UI non esiste finché il DTO, il service e il controller non lo portano. La giuntura fra i due è il posto dove nascono i bug che nessun compilatore vede: TypeScript e Java compilano felici mentre si scambiano dati diversi.

**3. Non c'è una rete, e quella che sembra esserci è rotta.** Zero test nel backend, Vitest non cablato nel frontend. Restano `typecheck`, `lint`, `build` e `compile`, che verificano se il codice *sta in piedi*, non se *fa la cosa giusta*. Tutto ciò che è semantico — un colore che sparisce in un tema, un flusso senza stato di errore, un chiamante non aggiornato — non lo trova nessuna macchina.

E c'è un aggravante misurato: **sul frontend quei gate sono già rossi su albero pulito**, 318 errori di `typecheck` e 894 problemi di `lint` accumulati nel tempo. Un revisore che riportasse l'output grezzo produrrebbe ~1200 falsi positivi a ogni giro, e alla terza volta nessuno leggerebbe più i report — il modo più efficace di rendere inutile una revisione. Per questo l'orchestratore **fotografa la linea di base prima di sviluppare** e poi confronta: contano solo gli errori nuovi. Il backend, che compila pulito, è l'unico gate dove ogni output è un segnale vero.

I revisori esistono per il punto 3. La fase di piano esiste per il punto 1. La mappa dei due repo esiste per il punto 2.

---

## Perché il piano è una fase separata

Il modo tipico di fallire un task qui non è scrivere codice sbagliato: è **scrivere codice corretto che risolve un problema leggermente diverso.**

Con una specifica di quattro parole, la distanza fra "il problema" e "un problema vicino" è tutta interpretazione. Se l'interpretazione resta implicita, si scopre sbagliata dopo l'implementazione — quando costa.

Il piano la rende esplicita, in un documento breve che si legge in un minuto e si corregge in trenta secondi. È l'unico punto del workflow dove un fraintendimento costa quanto una frase.

Da qui la regola: **il piano si scrive prima che si apra un editor.** Non però che si approvi: l'agente lo salva su file e parte da solo. L'approvazione preventiva è stata tolta di proposito — bloccava l'agente su ogni task in attesa di un sì, e il costo di quell'attesa era più alto del rischio che copriva.

Il piano resta però un documento vero, salvato in `/tmp/dev-hq-piani/<task-id>.md`, e serve a due lettori: il revisore logica in Fase 4, che senza metro non può giudicare se il lavoro è quello giusto, e Carlos in Fase 5, che ci trova le assunzioni. Le assunzioni si scrivono in una sezione separata proprio per questo: si controllano a lavoro fatto, ed è lì che si vede subito se una era sbagliata.

Il controllo però non è sparito: si è spostato. Al posto tuo il piano lo legge **`revisore-piano`**, che lo confronta col task grezzo e col codice vero, e l'agente corregge finché ottiene un `APPROVATO`. È il revisore col miglior rapporto costo/beneficio del sistema — gira su mezza pagina invece che su un diff, e intercetta il difetto più caro di tutti: **aver capito male il task**. Senza di lui, togliere la tua approvazione avrebbe lasciato l'interpretazione senza nessun controllo fino a Fase 4, quando il lavoro è già fatto.

Anche sull'ambiguità grossa — un pomeriggio contro due settimane — l'agente non si ferma: **sceglie la lettura più reversibile** e rende visibile il bivio, nel piano e nel report. Il ragionamento è che una scelta sbagliata ma piccola costa un pomeriggio, mentre una domanda in attesa costa la giornata intera; e il bivio scritto nel report ti arriva comunque, solo dopo invece che prima.

---

## Perché revisori separati e non uno solo

Un revisore unico con molti mandati non li esegue tutti: converge sul primo difetto interessante e scrive quello. È il fallimento classico della revisione generica — «ho guardato il codice, mi sembra a posto».

Revisori separati, con **elenchi chiusi** di verifiche, producono liste diverse. L'elenco chiuso è deliberato: *"cerca problemi estetici"* produce rilievi vaghi, *"per ogni colore introdotto verifica che regga nei tre temi"* produce rilievi verificabili.

Girano **in parallelo e isolati** perché sono indipendenti: se vedessero i rilievi degli altri, convergerebbero sull'inquadramento del primo invece di trovare cose diverse. Il costo in token è un contesto ciascuno; il beneficio sono punti di vista che restano distinti.

E girano **sempre tutti**, anche sui task piccoli, perché sono gli interventi piccoli quelli che passano senza che nessuno guardi.

### La divisione dei mandati

I confini sono tagliati in modo che non si sovrappongano — ogni revisore ha una classe di difetti che **solo lui** può trovare:

| Revisore | La domanda | Difetto che solo lui vede |
|----------|-----------|---------------------------|
| Estetico | Questo **appartiene** al prodotto? | Un colore che sparisce nel tema silvia; il ventunesimo date picker diverso |
| UX | Si può **usare**? | Un salvataggio senza stato di caricamento che crea record doppi |
| Logica | Fa **quello che il task chiedeva**? | Codice corretto che risolve il problema sbagliato |
| Regressioni | Cosa si è rotto **altrove**? | Un chiamante fuori dal diff che nessuno ha guardato |
| Sicurezza | Questo è **lecito**? | Un endpoint clinico che non finisce nell'audit |
| Documentazione *(Fase 5)* | I doc dicono ancora il **vero**? | Un catalogo che il diff ha reso falso |
| Performance | **Regge** quando i dati crescono? | Una query che con 500 visite ne diventa 501 |
| **Impatto sistemico** | Il **sistema** ha ancora senso? | Un job che manda un messaggio in più, tre salti più in là |
| Piano *(Fase 2)* | Il piano ha capito il **task giusto**? | Un fraintendimento, mentre costa una frase |

Il revisore regressioni è l'unico che guarda il codice **non** nel diff, ed è il più importante in assenza di test: è letteralmente l'unica cosa che sta fra una modifica e una regressione in produzione.

Il revisore sicurezza è l'unico che apre i documenti di accountability GDPR. Il gestionale tratta **dati sanitari su larga scala** — rischio dichiarato alto — e ha un audit clinico che scatta per *path matching*: un endpoint clinico nuovo non registrato nel matcher non produce alcuna traccia, **e non fallisce**. Nessun compilatore, nessun test e nessuno degli altri sei vedrebbe mai quel buco.

### Un salto contro molti salti

`revisore-regressioni` e `revisore-impatto-sistemico` sembrano lo stesso revisore e non lo sono. Il confine è la **distanza**.

Il primo parte dai **simboli** che il diff ha cambiato e cerca i chiamanti con `grep`: **un salto**, meccanico, esaustivo. Trova ciò che non compila più o riceve dati diversi.

Il secondo parte dai **concetti** toccati e percorre i flussi end-to-end attraverso i due repo: **molti salti**, semantico, selettivo. Trova ciò che **compila benissimo e ha smesso di avere senso** — il diff cambia come si calcola lo stato di una visita, il service viene aggiornato, e un job notturno che legge quello stato manda un WhatsApp a un paziente per una visita che non esiste. Nessun chiamante diretto è rotto. Nessun compilatore protesta.

Il rischio del secondo è annegare: «tutto il codice» non si legge. Per questo il suo metodo è vincolato — mappa i concetti toccati, sceglie due o tre flussi completi, li percorre davvero, e **dichiara quali ha scelto**. Due flussi percorsi valgono più di venti sfiorati.

### Perché alcuni revisori sono divisi FE/BE

Logica e performance esistono in due versioni, frontend e backend. Non è simmetria per bellezza: **le due metà sono discipline diverse.**

Soft delete `attivo`, transazioni, migrazioni Flyway, N+1 su associazioni lazy e `BigDecimal` sugli importi non hanno niente in comune con stato React, dipendenze di `useEffect`, refetch di cache già piene e date costruite a `T12:00:00`. Un revisore unico che tenesse dentro entrambe farebbe male tutte e due, perché per essere efficace un elenco di verifiche deve essere corto e specifico.

Non sono divisi, invece: **regressioni** — il suo valore sta proprio nell'attraversare il confine, e dividerlo lo accecherebbe dove serve di più; **sicurezza** — il baricentro è schiacciato sul backend (audit, permessi, query, log, segreti) e la metà frontend sarebbe troppo magra per un contesto suo; **documentazione** — è lavoro meccanico, dividerlo raddoppia il costo senza aggiungere profondità.

### Il costo, detto onestamente

Nove revisori a ogni giro. Su un ciclo da tre giri sono ventisette revisioni, più il revisore del piano prima e quello della documentazione dopo.

Tre cose lo tengono sostenibile:

**Il gating per repo.** Sei revisori su nove girano su un repo solo, e chiudono in una riga se il diff non lo tocca. Un task di solo backend ne spegne quattro. La divisione FE/BE **non ha aumentato il costo: lo ha reso proporzionale al diff.**

**Il gating per materia.** Un cambio di CSS non impegna performance; un task senza dati personali non impegna sicurezza.

**Il mandato stretto del correttivo.** Solo gli ERRORE, nessuna miglioria colta al volo: così il diff non gonfia fra un giro e l'altro, e il conto degli ERRORE scende invece di spostarsi.

---

## Perché i revisori non correggono

Un revisore che sistema da sé quello che trova sembra efficiente, e invece rompe il ciclo in tre modi.

**Porta via la prova.** Corretto il difetto, non resta niente da verificare: nessuno può più controllare che la correzione fosse quella giusta, né che il difetto fosse reale.

**Confonde i ruoli.** Chi giudica non deve essere chi esegue: un revisore che ha appena scritto una riga la giudicherà bene al giro dopo. La separazione fra chi trova e chi corregge è ciò che rende il secondo giro un controllo vero.

**Fa collidere più scrittori.** Sette revisori in parallelo che modificano gli stessi file si sovrascrivono a vicenda.

Per questo i revisori producono un **referto** e si fermano lì, e a correggere è un passaggio di sviluppo separato — l'unico che scrive.

## Perché il ciclo gira fino al 100%

Un giro solo di revisione non basta: **le correzioni sono codice nuovo**, e il codice nuovo può rompere ciò che era già stato approvato. Correggere un colore per il revisore estetico può togliere un contrasto che il revisore UX aveva accettato.

Quindi ogni giro rilancia **tutti**, non solo quelli che avevano trovato qualcosa: l'approvazione al 100% ha senso solo se tutti hanno visto lo **stesso stato del codice**, quello finale. Un'approvazione a pezzi, data su versioni diverse, non è un'approvazione.

## Perché la documentazione sta fuori dal ciclo

`revisore-documentazione` è l'unico che non partecipa ai giri: gira **dopo**, a codice definitivo, come ultimo passo prima della consegna.

Il motivo è che la documentazione descrive il codice finale, e **durante il ciclo il codice finale non esiste ancora**. Dentro la Fase 4 avrebbe fatto riscrivere i cataloghi a ogni giro, inseguendo un bersaglio che si spostava: lavoro rifatto tre volte e buttato due. I suoi rilievi sarebbero anche stati i più deboli del giro — quelli che si è tentati di saltare, in mezzo a difetti veri di sicurezza e logica.

C'è poi la proprietà che rende questa collocazione **sicura**, e che nessun altro revisore possiede: le sue correzioni toccano **solo file `.md`**. Non possono rompere niente di ciò che i nove hanno appena approvato, quindi non invalidano il 100% e non fanno ripartire il ciclo. È l'unica correzione che si può fare dopo l'approvazione senza rimetterla in discussione — ed è esattamente il criterio per cui sta in fondo invece che dentro.

La regola che protegge l'invariante: in quella fase **si scrive solo documentazione**. Se emerge che servirebbe una modifica al codice, non si fa — si annota nel report come lavoro successivo. Il codice ha superato nove revisori: toccarlo lì significherebbe buttare via quell'approvazione.

Il correttivo ha un mandato stretto — solo gli ERRORE, nessuna miglioria colta al volo — proprio perché ogni riga in più è materiale nuovo da revisionare, che allontana il 100% invece di avvicinarlo.

**E se non converge?** È il rischio strutturale di un ciclo che pretende l'unanimità, e va risolto **senza di te** — un ciclo che si ferma ad aspettare una risposta è un fallimento tanto quanto il codice rotto: blocca la giornata e non produce niente.

Il protocollo sta in `references/stallo.md` e poggia su tre idee.

**Riconoscere lo stallo misurandolo, non sentendolo.** L'agente registra i rilievi giro per giro e cerca tre segnali: ripetizione, oscillazione (correggi A, si rompe B, correggi B, si rirompe A), o conto fermo per due giri. L'oscillazione è la più insidiosa perché il numero *sembra* muoversi — 4 → 3 → 4 → 3 — e senza traccia puntuale la si scambia per progresso. Più un tetto secco: **5 giri**.

**Una gerarchia che decide i conflitti al posto di un umano.** Quando due revisori si contraddicono, vince quello più in alto in un ordine fisso — sicurezza, logica, regressioni/impatto, UX, performance, estetico, documentazione — e il rilievo dell'altro viene declassato a DUBBIO con la motivazione scritta. Non serve un arbitro: serve un ordine di precedenza, e ce l'ha. Un ERRORE di sicurezza non si declassa mai.

**Tre uscite invece di una domanda.** *Consegna con riserva* quando resta un rilievo di UX, performance, estetica o documentazione — il caso normale: un attrito di UX non giustifica buttare via un intervento che funziona ed è sicuro. *Consegna parziale* quando il rilievo è di logica o regressioni ed è isolabile. *Abbandono protetto* quando è di sicurezza, o non isolabile: lì non consegnare è la decisione giusta, perché codice che espone dati clinici è peggio di nessun codice.

**La precauzione che rende sicure le ultime due.** Annullare significa toccare file, e l'albero può contenere modifiche tue che non c'entrano niente — è già successo durante la costruzione di questo agente. Quindi a inizio Fase 3 l'agente fotografa `git status`, e al momento di annullare salva sempre il proprio lavoro come patch e ripristina **solo** i file che compaiono adesso e non comparivano prima, con `git restore`. Senza quella fotografia, annullare gli è vietato: ripiega sulla consegna con riserva.

Poi passa al task successivo: uno stallo su un task non ferma la giornata.

---

## Perché l'estetico controlla tre temi

Perché sono tre, e il terzo non lo prova nessuno.

`:root` chiaro, `.dark` (blu aziendale, **default del prodotto**), `.silvia` (nero puro). Il conteggio racconta la storia: **2630 varianti `dark:` contro 929 `silvia:`**. Ogni componente che gestisce la seconda e non la terza è UI rotta per chi usa silvia.

C'è poi una trappola strutturale del tema dark che vale la pena conoscere anche fuori dalla revisione: in `.dark`, sette token di superficie — `card`, `popover`, `primary`, `secondary`, `muted`, `accent` — valgono **tutti `#002552`, lo stesso colore dello sfondo**. In dark la profondità non esiste come colore: esiste solo come bordo. Un blocco che si stacca dal fondo in chiaro e in silvia, in dark è piatto.

Il secondo mandato dell'estetico — riusare le primitive — nasce da un caso reale e misurabile: `DatePickerInput` è la primitive canonica ed è usata in 13 file; in altri **20** c'è un `<input type="date">` grezzo, che prende l'aspetto dal sistema operativo e non somiglia a nient'altro nel gestionale. Nessuno l'ha deciso: è successo un file alla volta, ogni volta perché era più veloce. Il revisore ferma il ventunesimo.

---

## ERRORE e DUBBIO

Due sole etichette, perché tre sono troppe e una non basta.

- **ERRORE** — si corregge prima di consegnare. Non si negozia.
- **DUBBIO** — si valuta. Se non si corregge, si scrive perché.

Il DUBBIO serve a far dire ai revisori le cose incerte **senza** che ognuna diventi un blocco. Un revisore che può marcare solo ERRORE tace sulle cose di cui non è sicuro — e sono spesso quelle giuste.

Ogni rilievo deve portare uno **scenario concreto**: input, passi, risultato atteso, risultato reale. Un rilievo senza scenario non è verificabile, e non essendo verificabile non è discutibile.

La distinzione regge il ciclo: **è l'ERRORE, e solo l'ERRORE, a decidere se si fa un altro giro.** Zero ERRORE da tutti = approvato al 100%, si consegna. Un DUBBIO lasciato aperto non blocca la consegna: viene motivato e finisce nel report, dove Carlos lo vede.

Senza questa asimmetria il ciclo non chiuderebbe mai — c'è sempre qualcosa che si potrebbe fare meglio, e un revisore che può marcare solo ERRORE trasformerebbe ogni preferenza in un blocco.

---

## Cosa ha insegnato il primo task

Il workflow è stato corretto dopo la prima esecuzione reale (869cng430). Vale la pena registrare **perché** quei difetti erano invisibili a priori: sono tutti casi in cui uno strumento dava una risposta **plausibile ma incompleta**, senza segnalare nulla.

**`git diff` mente per omissione.** Non mostra i file nuovi né le modifiche in staging. Sul task reale restituiva zero righe mentre il lavoro c'era tutto — bastava che qualcuno avesse fatto `git add`. Se la Fase 4 fosse partita in quel momento, nove revisori avrebbero ricevuto un diff vuoto e approvato all'unanimità un lavoro che non avevano visto. **Il 100% sarebbe stato una firma in bianco.** Ora il diff si costruisce con `git diff HEAD` più il contenuto dei file non tracciati, e prima di consegnarlo si verifica che il conto dei file torni.

**`cd` è pericoloso con due repository.** La working directory persiste fra i comandi: un `cd` fatto prima fa leggere il repo sbagliato senza alcun errore. È successo due volte in una sola esecuzione, e una volta ha prodotto un elenco di file toccati completamente sbagliato. Ora la regola è `git -C`, e subshell per i comandi che non lo supportano.

**Il confronto con la linea di base era troppo ingenuo.** Confrontare per numero di riga segnala come nuovi tutti gli errori che il diff ha semplicemente spostato più in basso: tre segnalati, due falsi. Ora si confronta per testo, e il lint per conteggio di regola.

**E il difetto peggiore non era nel codice ma nello schema.** Il vincolo `CHECK` generato da Hibernate sulle colonne enum non è definito da nessuna migrazione: esiste solo nel database. In dev nessuno se ne accorge; in prod (`ddl-auto=validate`) l'applicazione parte regolarmente e il primo salvataggio del valore nuovo fallisce. Lo ha trovato `revisore-piano` — prima che fosse scritta una riga di codice, che è esattamente il momento in cui costa meno.

Da qui due aggiunte: una ricetta per i task che estendono un enum, e l'uso del **database come strumento di verifica**, per rispondere alle domande che il codice non risponde — quali vincoli esistono, cosa c'è davvero nei dati — e per provare le migrazioni in una transazione da annullare.

Il filo comune: **verificare invece di assumere**, soprattutto quando la frase che si sta per scrivere comincia con «non serve» o «è già gestito».

## Dove finisce il report, e perché su file

L'agente non committa e non scrive su ClickUp. Sono due scelte deliberate — ma insieme creano un problema: **senza una traccia scritta da lui, di una giornata di lavoro non resta niente.**

Il terminale non basta. L'agente lavora in autonomia su più task di seguito, e l'output scorre: quando arrivi a leggere, il report del primo task è già lontano. E se la sessione si chiude, è perso.

Per questo la consegna scrive sempre **su file**, in `report/`: un report per task, il piano accanto, e a fine giornata un riepilogo con tutti gli esiti. Se del lavoro è stato annullato, patch e archivio dei file nuovi finiscono lì con lo stesso prefisso — `/tmp` viene ripulito, e una patch persa è lavoro perso davvero.

Il caso in cui questo conta di più è lo **stallo risolto in autonomia**: il file è la sola cosa che ti dice che una decisione è stata presa al posto tuo, quale, e con che rischio residuo. Senza, l'autonomia diventa opacità.

## Perché non committa mai

Il workflow arriva fino alla working tree e si ferma.

Non è una precauzione contro l'agente: è che **cosa entra in git è una decisione di prodotto**, e la prende Carlos. Un commit automatico toglierebbe il punto in cui una persona guarda il diff prima che diventi storia.

Il divieto è scritto in due posti che si rinforzano: nella skill dell'orchestratore, e come `deny` in `.claude/settings.json` — dove sono negati anche `push`, `branch`, `checkout`, `reset`, `rebase`, `merge` e `stash`. La skill dice cosa fare; i permessi impediscono di sbagliare.

Stesso principio su ClickUp: **sola lettura.** Niente `POST`, `PUT`, `DELETE`. L'agente non chiude task, non cambia stato, non commenta. Lo stato di un task riflette quello che una persona ha deciso, e un agente che sposta le colonne fa perdere la fiducia nella board.

---

## Il limite noto: la scadenza

Il workflow parte dai task **con scadenza oggi**, come richiesto. Va detto chiaramente che nella lista HQ, così com'è, **quasi nessun task ha una scadenza**: 3 su 100.

Il filtro tornerà quasi sempre vuoto. L'agente non lo aggira di iniziativa — dichiara la selezione vuota, mostra gli scaduti ancora aperti, e chiede. Scegliere da solo fra un centinaio di task senza scadenza sarebbe lavoro buttato nella maggior parte dei casi.

Perché l'agente lavori un task, quel task ha bisogno di una scadenza su ClickUp. È un cambio di abitudine sulla board, non una modifica al codice — ed è la sola cosa che serve perché la Fase 1 diventi utile.

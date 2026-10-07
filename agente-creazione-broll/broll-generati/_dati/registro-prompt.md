# Registro dei prompt

Quello che i video già girati hanno insegnato, così che il prossimo non rinasca con gli
stessi difetti. Lo legge il regista prima di pianificare e chi scrive i prompt prima di
scrivere; lo scrive il collaudo dopo.

Il conto è aritmetico: correggere un difetto a valle costa una passata su ogni video,
correggerlo qui costa una riga e non torna più.

---

## Correzioni attive

Difetti già visti più di una volta. **Si evitano in partenza, non si correggono dopo.**

Le ha promosse Carlos il 2026-09-29, guardando il primo render (`colon-irritabile-torino`).
Non sono ipotesi: sono cose viste nell'immagine e nel video consegnati.

### 0. La scena deve POLARIZZARE, o non vale i crediti

*(promossa da Carlos il 2026-09-29, guardando il video v1)*

Il difetto più caro di tutti, e quello che il primo video ha mostrato meglio: una donna
stanca davanti a un piatto di riso è una scena che funzionerebbe **identica** per la
lombalgia, l'emicrania, la menopausa o la depressione. Chi la guarda pensa «eh sì, capita».
Non pensa **«come fanno a saperlo»** — ed è quella la sola reazione che compra attenzione.

La prova del nove è una domanda sola: **funzionerebbe per un'altra condizione?** Se sì, non
è una scena, è uno stato d'animo. Il collaudo ora lo verifica (`SCENA_GENERICA`).

Il metodo, ora scritto nel prompt del marketer:

1. **Parti dai pain point specifici, non dalla condizione.** «Colon irritabile» è una
   diagnosi, non un dolore. I pain point sono cosa quella persona non può più fare, a cosa
   rinuncia, cosa nasconde, cosa teme che gli altri pensino.
2. **Cerca la conseguenza sulla vita, non il sintomo.** Il sintomo è medicina e non vende.
   Il dolore fisico è quello che il paziente racconta al medico; quello che non racconta a
   nessuno è la rinuncia — e la vergogna vende più del dolore, perché il dolore si sopporta
   e la vergogna no.
3. **Scegli un momento datato**, con un'ora, un luogo e una decisione. «Il momento in cui,
   prima di accettare l'invito, controlla mentalmente dove sono i bagni» è una scena; «una
   donna in ansia» non è nemmeno inquadrabile.
4. **Trova il dettaglio privato**: la cosa che il target fa e non dice. È quasi sempre lì
   che sta la scena più forte, ed è quasi sempre quella che nessun concorrente mostra
   perché sembra troppo piccola.
5. **Nomina chi si esclude.** Se non riesci a dire chi, vedendola, capisce che non lo
   riguarda, la scena è generica.

### 0-bis. Prima le immagini in lotto, il video solo alla fine

*(errore di processo, 2026-09-29: e costato 1,30 USD di video buttati su un solo b-roll)*

| | crediti | USD |
|---|---|---|
| immagine (`soul-cinema`) | 0,088 | **0,006** |
| video (`kling-3-std-i2v`) | 5,175 | **0,324** |

Il video è il **98% del costo**. Ogni generazione è un'estrazione, e giudicare una
formulazione su una sola estrazione è quello che fa buttare i video.

**Il metodo è: `--solo-immagini` con più varianti in un lotto, si guardano tutte, si sceglie,
e solo allora si paga un video.** Sei immagini costano 0,036 USD, cioè un decimo di un solo
video. Due o tre estrazioni per formulazione, perché la varianza fra un'estrazione e l'altra
è il vero avversario.

### 0-ter. I divieti non funzionano: il difetto va reso impossibile, non vietato

*(misurato su 8 estrazioni, 2026-09-29)*

`no hand on the abdomen` era scritto nei vincoli negativi. La mano sulla pancia è uscita
**5 volte su 8**. Rafforzare il divieto non ha spostato niente: nel terzo giro la frase
«entrambe le mani stanno basse e lontane dal corpo, nessuna tocca lo stomaco, non è incinta
e non deve mai leggersi come incinta» era la **prima** del blocco soggetto, ed è uscita
uguale tre volte su tre.

Quello che ha funzionato è stato **dare alle mani un lavoro**: una sulla tracolla o dentro
la borsa, l'altra che tiene il telefono in basso. Occupate, il difetto non si presenta più.

**La regola generale:** quando un modello ha un prior visivo forte, non lo si batte
vietando. Lo si batte occupando il posto — un gesto concreto al posto del gesto sbagliato,
oppure un'inquadratura in cui il difetto non è proprio inquadrabile.

### 1. Il protagonista ha SEMPRE fra i 40 e i 60 anni

La regola esisteva già in `casting-e-guardaroba.md`, e il video è uscito lo stesso con una
protagonista di 34 anni. Il motivo è strutturale, non una svista: la `descrizione_fissa`
la scrive la **regia**, che quel riferimento non lo apre mai — lo legge solo chi scrive i
prompt, e a quel punto l'età è già decisa e va copiata alla lettera.

Ora il vincolo è scritto anche nel prompt della regia e nel collaudo (`ETA_FUORI_TARGET`).
Chi scrive il prompt mette l'età **come numero** (`a 52-year-old Italian woman`): l'aggettivo
«middle-aged» produce trentacinquenni.

**Pubblico 35-60, in scena 40-60.** Non è una contraddizione: si rappresenta il centro del
bersaglio, non il suo bordo più giovane. Chi ha 38 anni si riconosce in una cinquantenne;
chi ne ha 55 non si riconosce in una trentacinquenne, e per di più legge il problema come
roba da giovani.

### 2. Guardaroba: mai l'abbigliamento da casa

Felpa, tuta, pantaloni morbidi, ciabatte, coda disfatta. Sembra che vestire male il
protagonista renda la scena più vera: fa il contrario. Legge come **persona che si è
arresa**, e una persona arresa non è credibile come qualcuno che prenoterà un trattamento.

Il registro è la via di mezzo: una persona curata in una giornata normale, che fra un'ora
esce di casa. Né tuta né completo. Il dolore si legge da postura, viso e luce — non dai
vestiti.

### 3. Lo sfondo è metà del lavoro, e la città entra dalla finestra

Uno sfondo piatto o anonimo — un muro, un elettrodomestico in acciaio, una porta chiusa —
abbassa il ceto percepito quanto un capo sbagliato, e fa sembrare la scena povera invece
che vera. Dietro il soggetto ci vuole sempre qualcosa da guardare, a fuoco morbido.

Quando la città di riferimento deve vedersi, il posto è la **finestra o la vetrata**:
sfondo urbano sfocato ma leggibile. Nel primo render la finestra dava su un muro scuro e di
Torino non è arrivato niente.

Il registro di default resta il **tessuto**, ma «tessuto» non vuol dire «mai un landmark»:
vedi la correzione 7 — uno per video ci va, e lasciarlo a zero è una scelta da motivare.

### 4. Ogni oggetto deve dimostrare qualcosa

Una tazzina di caffè sporca accanto a un piatto di riso in bianco: nessuno beve un caffè
macchiato durante una dieta in bianco. Non è «vissuto», è disordine — e il disordine
incoerente è uno dei segnali più forti che l'immagine è generata.

Passa gli oggetti uno per uno e chiedi di ciascuno **cosa dimostra**. Se la risposta è
«riempie», si toglie. Tre oggetti coerenti battono otto oggetti sparsi.

### 5. La scena deve DIMOSTRARE, non illustrare

Se la scena raddoppia quello che la voce sta già dicendo, si può togliere senza perdere
niente — e allora non valeva i crediti. Deve fare un'affermazione che la voce **non** sta
facendo, e che chi guarda accetta perché la vede.

Per questo dal 2026-09-29 il workflow ha una fase **Strategia** prima della Regia: un
marketer decide la proposizione che ogni scena deve rendere innegabile, e il regista
piazza i b-roll su quell'ordine. Il regista sa dove si perde l'attenzione; non sa cosa
conviene dimostrare per vendere.

### 6. Gli pseudo-glifi arrivano lo stesso — confermato sul campo

I negativi espliciti (`no letters, no numbers, no words anywhere in frame`) **non bastano**:
nel primo render il quaderno è uscito pieno di forme che leggono come parole, nel terzo
basso, cioè il punto più visibile del 9:16.

La formula «descrivi il senso invece delle parole» (`dense uniform ink marks that have no
letterforms`, righe sbarrate) ha **ridotto** il problema, non l'ha risolto.

La conseguenza operativa: **un oggetto scritto va tenuto fuori fuoco o fuori campo**, non
solo vietato a parole. Se il testo è necessario alla scena, mettilo a bordo inquadratura o
in sfocato, mai nitido nel terzo che si guarda per primo. E l'immagine si guarda sempre
**prima** di mandarla in I2V: in video non si corregge più.

**La fonte che nessuno controlla è il prompt stesso** *(vista su colon-irritabile-torino-v2,
2026-09-29)*. Le fonti in scena — insegna, etichetta, schermo — vengono neutralizzate una per
una, e poi nel testo resta scritto `at 20:50 on a Thursday evening`: una cifra nel prompt è
un invito a disegnare cifre esattamente come un orologio in scena, anche se i negativi le
vietano. **Orari, date, prezzi e numeri civici si scrivono a parole** — `just before nine in
the evening` — e il conto delle fonti si fa sul prompt, non solo sull'inquadratura.

### 7. Torino è il default, e vale sugli esterni quanto sugli arredi

*(decisa da Carlos il 2026-09-29, dopo il piano di `colon-irritabile-torino-v2`)*

Parole di Carlos: *«Il default della città, se non specificato, deve essere sempre Torino.
Sia come arredamenti, sia come cose esterne (es: Mole, Monte dei Cappuccini, Superga,
piazza San Carlo, via Roma, ecc.)».*

La prima metà era già nel workflow: `citta.json` ha `predefinita: "torino"`, e senza città
al lancio si applica quella, senza chiedere niente a nessuno. La metà che mancava è la
seconda: **la città si deve vedere anche fuori.** Nel piano v2 gli arredi erano torinesi al
millimetro — portici, lampioni in ghisa, intonaci ocra, tram verde, trattoria con boiserie
scura e marmo — ma il budget di un landmark era stato speso a **zero** per prudenza di
regia. Da oggi zero non è un default: è una scelta che va motivata nel piano, e la motivazione
la valuta Carlos.

Come si applica, senza rompere il tetto di `citta.json`:

1. **Gli interni si descrivono sempre**, in ogni b-roll, anche quando sono sfocati oltre una
   vetrata e anche quando sono un abitacolo. Un ambiente non descritto non resta neutro: lo
   riempie il default americano del modello. È già successo due volte (l'abitacolo, la sala
   del ristorante) proprio perché erano fuori fuoco e nessuno li guardava.
2. **Un landmark per video, dall'elenco di `citta.json`**, sull'inquadratura che può
   portarlo. Il tetto resta uno: due landmark spostano il registro da «questa è la mia vita»
   a pubblicità turistica.
3. **Se la quota di b-roll è 1, quel b-roll è anche l'inquadratura di ambientazione**: il
   landmark ci entra come sfondo lontano e sfocato, non al centro del quadro. Se davvero non
   ci sta — primo piano stretto, interno cieco — il piano lo scrive e dice perché.
4. **Su tutto il resto si usa il registro «tessuto»**: portici con volte a botte, facciate
   ocra, persiane verdi a libro, viali alberati, colline a est, nebbia bassa. È il livello
   che fa riconoscere la città a chi ci vive senza insospettire chi non ci vive.

Nota tecnica che rende la regola obbligatoria: il modello immagine in uso lavora **solo da
prompt testuale**, non accetta immagini di riferimento. Torino esiste soltanto se è scritta a
parole, in ogni singolo prompt.

---

## Osservazioni

Notate una volta sola. Diventano correzioni attive quando si ripetono, e **la promozione
la decide Carlos.**

### La descrizione del personaggio va copiata in inglese, non ritradotta
*(colon-irritabile-torino, 2026-09-29)*

La `descrizione_fissa` del piano e in italiano, i prompt sono in inglese: chi scrive il
secondo b-roll con la stessa persona traduce di nuovo, e due traduzioni diverse danno due
persone diverse. La regola della skill — «copiare alla lettera» — riguarda l'italiano del
piano e non basta. **Dal secondo prompt in poi si ricopia la formulazione inglese gia
scritta nel primo**, parola per parola, non la si ritraduce.

Qui non e ancora successo niente: il video aveva un prompt solo, quindi la discontinuita
era impossibile. E una trappola vista in anticipo, non un difetto misurato.

**Seconda registrazione, stesso motivo** *(colon-irritabile-torino-v2, 2026-09-29)*: anche
questo piano esce con un solo b-roll e `serve_soul_id: false`, quindi la trappola resta
armata e non scattata. Vale la pena scriverlo qui perche il momento in cui scattera e
prevedibile: la prima volta che Carlos alza la quota su uno script gia pianificato, il
secondo prompt nasce dall'italiano del piano e non dall'inglese del primo prompt.

### Quota 1 su novanta secondi: il meccanismo resta scoperto per costruzione
*(colon-irritabile-torino, 2026-09-29)*

Con un solo b-roll disponibile la regia lo spende sul pain d'apertura — che e la scelta
giusta — e tutto il blocco meccanismo (circa venticinque secondi di parlato astratto, tre
salti di scala anatomica) resta senza un visual, insieme al beat della vergogna sociale,
che e il punto piu convertibile dello script. Non e un errore di regia: e aritmetica della
quota, e si ripetera identica ogni volta che si lancia con quota 1 uno script di questa
lunghezza.

**La conseguenza e una decisione di Carlos al lancio, non della regia:** se la copertura
del meccanismo conta, la quota va alzata prima, non recuperata dopo.

**Ripetuta: seconda registrazione sullo stesso script** *(colon-irritabile-torino-v2,
2026-09-29)*. Non e piu un'ipotesi — e aritmetica confermata, e per la regola di questo file
sarebbe da promuovere a correzione attiva: **la promozione la decide Carlos.**

Due cose imparate su dove va il b-roll numero due, valide per qualunque script con un blocco
meccanismo:

- **Il secondo b-roll va sul beat dell'assoluzione, non sul meccanismo.** L'assoluzione e la
  scena che dice «ci ha provato per anni con metodo, il metodo ha fallito, non lei»: e quella
  che rende accettabile la spiegazione fisica che arriva subito dopo, e che disinnesca
  l'obiezione «prima devo capire cosa mi fa male». Il meccanismo senza immagini resta noioso;
  l'assoluzione senza immagini resta affidata alla sola voce, e non tiene.
- **Il meccanismo non si copre a meta.** Se ha tre salti di scala anatomica, chiede tre
  infografiche, una per salto: una sola produce due meta che non si parlano. O si finanzia
  intero, o si lascia scoperto apposta.

### L'esito del workflow descrive il piano, non il disco
*(colon-irritabile-torino, 2026-09-29)*

Il workflow ha restituito `esito: "generato"` mentre sul disco non c'era **nessun file**, e
l'agente di consegna ha scritto nell'indice una causa inventata — «si e fermato al cancello
di spesa con `autorizza_spesa=false`» — quando la spesa era autorizzata e la fase 8 era
partita davvero, morendo su un `403` di rete.

Due lezioni distinte:

1. **Prima di dire che un video esiste si guarda `outputs/<slug>/` con `ls`**: senza
   `immagini/`, `video/` e `manifest.json` non c'e niente da montare.
2. **Un agente che diagnostica un fallimento puo inventare la causa piu plausibile invece
   di leggerla.** La causa vera sta nell'output del comando, non nel racconto di chi lo ha
   lanciato.

### Una formula per il quaderno senza lettere — da verificare al primo render
*(colon-irritabile-torino, 2026-09-29)*

I modelli immagine producono pseudo-glifi anche quando il testo e vietato dai negativi. Il
prompt ha provato a togliere al modello il motivo di scriverli, descrivendo il senso
invece delle parole: `dense uniform ink marks that have no letterforms`, righe sbarrate,
«si legge come un diario tenuto per mesi dal ritmo delle righe e dalle cancellature, mai
dalle parole».

**Se funziona vale per ogni oggetto scritto** (referti, agende, etichette). Non lo sappiamo
ancora: nessuna immagine e stata generata. Al primo render si guarda l'immagine **prima**
di mandarla in I2V — un quaderno di lettere finte diventa il difetto piu visibile del
video, e in I2V non si corregge piu.

### L'oggetto che qualifica la condizione non si toglie per prudenza
*(colon-irritabile-torino-v2, 2026-09-29)*

Chi scriveva il prompt aveva sostituito il portapillole indicato dal marketer con una
generica pochette di stoffa, per paura che leggesse «malata». Risultato: `SCENA_GENERICA`
al collaudo. Alla domanda «cosa dimostra?», la pochette risponde «riempie» — e le salviette
accanto leggono come raffreddore o come pianto. Era sparito l'unico oggetto in cui il target
si riconosce.

**Il rimedio non e togliere l'oggetto, e sceglierne la versione neutra**: portapillole bianco
opaco, senza stampe, con i negativi rinforzati contro le scatole di farmaci. La paura di
sembrare medicali si paga con una scena che non appartiene a nessuno.

Stesso giro, secondo caso, piu sottile: la vetrata del ristorante diceva «sagome di persone
ai tavoli», cioe **evento sociale**, non **pasto**. La scena polarizzava su chi ha paura
della gente invece che su chi ha paura di mangiare fuori. **L'ancoraggio va all'oggetto del
timore, non al contesto**: piatti gia serviti, cestini del pane, calici pieni, il pasto gia
cominciato.

Corollario sul livello a cui si polarizza: portapillole + pasto gia servito polarizzano sulla
**famiglia digestiva** (celiachia, intolleranze, colon irritabile), non sulla singola
condizione. Va bene, purche l'ancoraggio sia esplicito e leggibile nel render: **se
nell'immagine l'ancora non si legge, si rigenera il T2I, non si ritocca il video.**

### Nel 9:16 lo sguardo all'indietro produce nuche
*(colon-irritabile-torino-v2, 2026-09-29)*

`three-quarter frontal` insieme a `gaze turned back over her shoulder` e una richiesta che il
modello puo risolvere con una testa girata via — e il verticale pretende il volto nel terzo
alto, dove non c'e niente da guardare se non il volto.

**La correzione sta nel blocco SUBJECT, non nell'inquadratura**: `her head turned only
slightly, her face still clearly readable to camera`. Cambiare l'inquadratura per risolvere
un problema di posa butta via tutto il resto della composizione.

### L'oggetto che porta la scena sta nel terzo medio, mai nel basso
*(colon-irritabile-torino-v2, 2026-09-29)*

Due istruzioni di composizione si contraddicono facilmente: «nothing legible placed in the
lower third» (regola del 9:16) e «l'oggetto che dimostra la condizione deve vedersi». Gli
oggetti tenuti in mano stanno all'altezza della vita: con un taglio a meta coscia la vita
cade nel terzo medio e va bene, ma se il modello inquadra piu largo l'oggetto scivola in
basso.

**Si controlla sull'immagine, prima dell'I2V.** E se il video e `locked-off` — che e la
scelta giusta dopo la carrellata che stringeva troppo — quel piazzamento resta congelato per
tutta la durata: non c'e movimento che lo rimetta a posto.

---

## Limiti dei modelli scoperti sul campo

Cose che la documentazione non dice e che si imparano generando. Quando una voce qui
riguarda la scelta di un modello, va riportata anche in `modelli-higgsfield.json`, nel
campo `limiti` di quel modello: è lì che la legge chi sceglie.

Gli avvertimenti sui modelli che girano nei collaudi — per esempio «soul-cinema tende a
drammatizzare» — arrivano dal catalogo, non dal campo: **non si copiano qui**, o questa
sezione diventa un doppione di `modelli-higgsfield.json` e smette di dire quello che serve,
cioe cosa e successo davvero generando.

### soul-cinema — elencare i terzi produce un trittico, non una composizione
*(colon-irritabile-torino-v2, 2026-09-29, misurato sull'immagine consegnata)*

La prima riga del prompt era: `her face in the upper third, the blurred restaurant window
behind her in the middle third, nothing legible placed in the lower third`. SOUL Cinema
l'ha letta come **istruzione di layout**, non come guida compositiva, e ha consegnato tre
bande orizzontali nette: mezzobusto sotto i portici, sala del ristorante a tutta larghezza
che taglia il busto, fondo nero con le gambe. Il video ha ereditato lo split.

Due sintomi collaterali dello stesso errore: la vetrata doveva essere sfocata a dodici metri
ed è a fuoco pieno (era un pannello a sé, non uno sfondo), e il tram verde che doveva passare
in fondo alla strada è finito **dentro la sala**, dietro i commensali.

**La formulazione veniva dalle nostre skill** («volto nel terzo alto»), che ora è corretta:
i terzi sono una guida per chi scrive, non parole da mettere nel prompt. Mai più di un
«third» per frase; il resto si scrive in linguaggio da macchina da presa — piano, obiettivo,
distanza in metri, profondità di campo. Il collaudo ora li conta (`COMPOSIZIONE_A_FASCE`).

### soul-cinema — su donna 40-60 in ambiente italiano tende alla mano sulla pancia, che legge INCINTA
*(colon-irritabile-torino-v2, 2026-09-29, 5 estrazioni su 8)*

Prior fortissimo: donna sui cinquanta + portico o interno italiano + maglia di lana attillata
+ disagio trattenuto → mano appoggiata sull'addome. Su una condizione digestiva il
fraintendimento e doppio: legge come sintomo (che non vende) e, con un maglione teso e la
mano che lo culla, **legge come gravidanza**.

Non si corregge a parole. Si corregge occupando le mani con un oggetto, o inquadrando dal
petto in su. Vale la pena ricordarlo su qualunque condizione addominale: colon irritabile,
gonfiore, reflusso, dolore mestruale.

### kling-3-std-i2v — la carrellata stringe molto piu di quanto le chiedi
*(colon-irritabile-torino, 2026-09-29, misurato sui fotogrammi 0 e 145)*

Il prompt chiedeva `a very slow push-in of roughly five percent across the whole shot`. Sul
girato la scala cambia di molto piu del cinque per cento: piatto e quaderno, che occupavano
il terzo basso al primo fotogramma, escono quasi del tutto dall'inquadratura all'ultimo.

**La conseguenza sul piano:** quello che deve restare visibile fino alla fine non si mette
ai bordi del quadro. O si tiene al centro, o si scrive `locked-off, no push-in, no zoom`
e si accetta un'immagine ferma — che su sei secondi non e un problema.

### kling-3-std-i2v — un gesto verso il torso finisce piu in alto di dove lo mandi
*(colon-irritabile-torino, 2026-09-29)*

Chiesto: la mano che si posa `flat and open just below her sternum`. Ottenuto: la mano sul
petto, che legge come cuore o respiro — su un video di colon irritabile e un errore di
organo.

**Come si scrive per ottenere la pancia:** il punto va ancorato a un riferimento visibile,
non a un osso. `low on the abdomen, below the navel, at the waistband` funziona meglio di
qualsiasi riferimento allo sterno, perche il modello vede la cintura e non vede lo sterno.

### kling-3-std-i2v — gli anelli si duplicano sulla mano che si muove
*(colon-irritabile-torino, 2026-09-29)*

Nell'immagine sorgente l'anello era uno solo, sulla mano destra. Nel video la mano che sale
ne porta uno anch'essa: due anelli dove ce n'era uno. Piccolo, ma e il tipo di dettaglio
che fa dire «e fatto con l'AI» a chi guarda due volte.

**Conseguenza:** i gioielli si mettono su una mano che nel prompt I2V **non si muove**, o
non si mettono.

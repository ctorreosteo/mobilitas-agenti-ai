---
name: mobilitas-reel
description: Procedura dell'agente reel-grafiche che aggiunge grafiche e infografiche a qualsiasi reel verticale 9:16 di @Studio_Mobilitas già montato (ads con finestre, ads con frontman, reel MOFU, reel solo B-roll; con o senza sottotitoli impressi e SRT). Copre la tappa 0 (studio delle reference nuove), la radiografia, il piano con il sistema di forme (pannello sotto il volto, fascia alta, badge, tendina e grafiche piene brevi) e lo stile approvato, i sottotitoli impressi che non si toccano, il render con zoom ed effetti sonori, i controlli automatici, il voto del direttore, il fermo sull'anteprima e la consegna, con i comandi ./mve reel-*. Usala per ogni nuovo reel in inbox/, per correggere un piano, per studiare una reference nuova, o quando un controllo va capito.
---

# mobilitas-reel (agente reel-grafiche)

Le regole sono in `CLAUDE.md` e vengono prima di questa skill. Qui c'è il **come**. Il sistema di forme, il modello
`infografica_reel`, la radiografia e lo studio delle reference sono in [references/reel.md](references/reel.md): **leggilo
prima di scrivere un piano**. I comandi sono `./mve reel-*`.

In breve, quello che non si discute:
- **sottotitoli impressi mai toccati**: per ogni fotogramma o fascia identica all'originale (video fermo, grafiche intorno) o
  grafica piena senza sottotitoli (nessuna copia, mai mezza riga). Il controllo `reel_sottotitoli.py` blocca il render;
- **stile approvato** e **più forme** scelte per inquadratura (di solito 2 o 3 nel reel, passaggi legati); grafiche piene al
  massimo 3, 4 s l'una;
- **infografiche vere** (l'oggetto è il protagonista, il testo è un'etichetta), solo parole dette, niente promesse, niente
  cifre non dette, anatomia solo Servier;
- il volto non si copre; grafiche e animazioni del montaggio non si coprono né si duplicano;
- **fermo sull'anteprima**: decide Riccardo.

## Le tappe e il fermo sull'anteprima

| tappa | chi | comando | esce | cancello |
|---|---|---|---|---|
| 0. reference (obbligatoria) | agente | `./mve reel-reference`; se ci sono reference nuove o con il nome fuori regola: rinominarle e fare lo **studio completo** ([references/reel.md](references/reel.md), sezione 8) | schede, ritmo, catalogo, linguaggio, modelli nuovi «in prova» | «TAPPA 0: OK». `reel-init` e `reel-coda --avanza` si fermano finché resta una reference da studiare (una scheda senza il suo video va bene) |
| init | motore | `./mve reel-init inbox/<SLUG>/` | `videos/<slug>/reel.json` | tappa 0 OK; video 1080×1920 (l'SRT può mancare) |
| 1. radiografia | motore, poi agente | `./mve reel-radiografia <slug>`, poi `./mve reel-3d <slug> <n,n\|nessuna>` | `radiografia.json`, `radiografia.md`, `radiografia/` | l'agente guarda **tutti** i fogli e segna le 3D |
| 2. piano | agente, poi motore | scrivi `piano.json`, poi `./mve reel-piano <slug>`; prove veloci con `./mve reel-prova <slug> <grafica> <secondi…>` | `piano/tavola.jpg`, `piano/piano.md` | 0 errori → avanti (niente fermata sul piano) |
| 3. rendi | motore, poi agente | `./mve reel-rendi <slug>`, voti con il subagente `direttore-reel` e `./mve reel-voto` | `anteprime/`, `controlli/` | 0 errori, letture di Vision guardate, voti → **FERMO: l'ANTEPRIMA a Riccardo** |
| | Riccardo | guarda l'anteprima: dice cosa migliorare (si corregge il piano e si rifà un'anteprima nuova, da capo con controlli e direttore) oppure dà l'ok in chat → `./mve reel-approva <slug> anteprime` | `approvazioni.json` (con l'md5 del video) | |
| 4. consegna | motore | `./mve reel-consegna <slug>` | `consegna/` + `consegna.md`, copia in `consegne/` | md5 della copia = file approvato |

- **`./mve reel-stato <slug>`** dice in ogni momento la tappa, a chi tocca e il comando dopo.
- **Le approvazioni le dà solo Riccardo.** `reel-approva` si lancia solo dopo il suo ok scritto in chat, mai per scelta tua.
  Un'approvazione vale per il file che ha visto: se il video cambia dopo l'ok, l'md5 non torna più e lo stato torna indietro.
- `./mve reel-approva <slug> piano` serve solo se Riccardo chiede di vedere un piano prima del render.
- Consegna = copia del file approvato, mai un render nuovo.

### Modalità coda

Con più reel in `inbox/`: prima la tappa 0 (`./mve reel-reference` e lo studio delle reference nuove), poi
`./mve reel-coda --avanza` fa le tappe del motore un reel dopo l'altro (init, radiografia, controllo del piano, render) e si
ferma a ogni punto che tocca a te o a Riccardo. Il tuo giro, finché `./mve reel-coda` mostra «tocca a: agente»:

1. prendi il primo reel della tabella che tocca a te;
2. fai la sua tappa: segnare le 3D, scrivere o correggere il piano, guardare le letture di Vision, far votare il direttore;
3. rilancia `./mve reel-coda --avanza`;
4. quando il reel arriva a «tocca a: riccardo», passa al successivo.

Alla fine scrivi l'elenco in `report/AAAA-MM-GG-coda.md`, con il percorso di ogni file da guardare.

**Ogni reel ha la sua cartella di lavoro** `.lavoro/<slug>/`: il motore ci manda anche i temporanei di Python, di
HyperFrames e di Chrome. Un reel non tocca i file di un altro. A consegna fatta `./mve reel-pulisci <slug>` svuota solo quella.

## Tappa 1: radiografia

Il motore misura, tu controlli. Apri con Read:

- `radiografia.md`: tagli, inquadrature (finestre, persona in camera, B-roll pieno), sottotitoli, voce, tipo di reel proposto;
- `radiografia/inquadrature-*.jpg`: inizio, metà e fine di ogni inquadratura, con le finestre misurate in magenta;
- `radiografia/persona-*.jpg`: persona, teste, mani, sottotitoli, scritte, celle libere;
- i provini ogni 0,5 s.

Cosa controllare:

- **Animazioni del montaggio** (anatomia 3D con muscoli evidenziati, oggetti 3D come pastiglie che cadono): le segni tu,
  guardando ogni inquadratura: `./mve reel-3d <slug> 3,9 --nota "collo e cervicale; mandibola e torace"` oppure `nessuna`,
  con la nota di cosa hai guardato. Senza questo passo il piano non passa. Lì le nostre forme restano chiuse.
- **Tipo d'inquadratura**: se è sbagliato (un banner del montaggio fa riconoscere uno «schema A» su un frontman),
  `./mve reel-tipo <slug> 21,22 "persona in camera" --nota "..."`.
- **Scritte del video**: quelle «di scena» (insegne, magliette, certificati) non bloccano le grafiche:
  `./mve reel-scena <slug> "<regex delle scritte del montaggio da non coprire>" --nota "..."`.
- **Schemi** degli ads a finestre: A (grande in alto + due piccole), B (due grandi), C (una quadrata, i sottotitoli dentro).
  Uno schema «?» vuol dire che il formato è nuovo: guardalo e chiedi.
- **Tagli**: devono essere netti; le «possibili dissolvenze» vanno guardate. Un passaggio rapido del montaggio dentro
  un'inquadratura (la persona che si alza, uno stacco a frusta) non è un taglio: guarda i volti fotogramma per fotogramma in
  `radiografia/persona.json` prima di mettere una forma lì.
- **Sottotitoli contro SRT**: le righe lette diverse dall'SRT si **segnalano e non si correggono**; il copy vero è quello detto
  e sottotitolato. Senza SRT il motore legge i sottotitoli impressi (Vision) e li conferma con whisper.
- **Voce**: le sonde brevi correggono la passata intera di whisper; il sottotitolo può anticipare o ritardare la voce: **le
  grafiche si agganciano alla voce** (`voce.parole[].a_inviluppo`).
- **Altezza delle lettere dei sottotitoli**: da qui viene il corpo minimo dei nostri testi (1,5 volte).

## Tappa 2: il piano

Prima di scrivere, leggi `radiografia.md`, [references/reel.md](references/reel.md) (sezione 0: forme, modello, controlli),
`motore/inserti/CATALOGO-MODELLI.md` e [references/modelli-ads.md](references/modelli-ads.md).
[references/esempio-piano-AD_CERVICALGIA.json](references/esempio-piano-AD_CERVICALGIA.json) è il piano del caso della
regressione (modelli a finestra degli ads).

### Cosa mettere e cosa no

- **Grafiche dove la voce dice qualcosa che una grafica chiarisce**: un elenco annunciato («tre benefici») → indicatore e
  card; cose negate («non trovi un professionista tutto fare») → lista che si barra; due durate → barre a confronto; un
  meccanismo → disegno Servier che cambia sulle parole; il tema → card con il disegno. Non si copre tutto il reel: dove il
  montaggio ha le sue grafiche (3D, banner, prezzo) o la voce fa una promessa, le forme restano chiuse, e il piano lo scrive in
  `senza_grafica` con il motivo.
- **Solo parole dette**: ogni parola scritta sta nell'SRT (o nei sottotitoli letti), e lo controlla il motore. Fanno eccezione
  solo + = €. Le cifre solo se dette e **già giuste dal primo fotogramma**.
- **È comunicazione sanitaria**: obiettivi, non garanzie. Niente spunte, niente «risolvi» o «guarisci».
- **Anatomia** solo da disegni Servier di `libreria/anatomia/`, mai dove il video ha già le 3D.
- **Niente B-roll aggiunti**, niente foto di pazienti.

### Varietà fra i reel

Gli ads di una campagna hanno spesso lo stesso schema di copy, ma non devono sembrare lo stesso video con le parole cambiate.

- **Lo storico** è `libreria/uso-modelli-reel.json`: per ogni reel consegnato, momento per momento, modello, modo e
  impaginazione, più i momenti lasciati senza grafica. `reel-consegna` aggiunge il reel da solo.
- **Ogni grafica ha il suo `momento`** ([references/momenti-ads.md](references/momenti-ads.md)) e la sua `impaginazione` in una riga.
- **Per un momento già coperto in un altro reel** scegli un modello, una forma o una composizione diversi. Se tieni lo stesso
  modello, cambia almeno impaginazione o forma e scrivi `"varieta": {"cambia": "...", "come": "...", "perche": "..."}`; un
  modello già usato per lo stesso momento in due reel o più: un altro modello, o le alternative scartate in
  `varieta.alternative`. `reel-piano` lo controlla e mette in `piano/piano.md` la tabella «prima → ora».
- **Si usa tutto il catalogo** e tutte le reference di `libreria/reference/`. Un modello nuovo nasce come variante «in prova».
- Restano uguali: brand, colori, Montserrat, stile approvato.

### Testi accorciati

Un testo accorciato non deve mai cambiare il significato del copy. «niente pastiglie in più» resta «pastiglie in più»:
«pastiglie» da sola, barrata, sembrerebbe «smetti le medicine».

- Ogni grafica ha `"testi_detti": [{"scritto": [...], "detto": "...", "senso": "..."}]`, una riga per ogni testo scritto.
- `detto` è la frase intera come è detta. `reel-piano` controlla che sia una frase contigua dell'SRT e che le parole scritte
  stiano lì dentro nello stesso ordine.
- `senso` lo scrivi tu: perché il testo, letto da solo e con la sua grafica (barrato, verde, dopo un «=»), dice la stessa cosa
  della frase. Le trappole: barrare una parola che la voce non nega del tutto; togliere il «solo», il «più», il «senza» che
  danno il senso; un risultato che, staccato da «pensato per», diventa una promessa; una frase riferita senza virgolette
  («solo conviverci» senza virgolette sembra un consiglio); due negazioni insieme («non trovi» + «tutto fare» barrato).
- **Mai «il tuo / la tua» insieme al disturbo**: a schermo solo il tema («dolore al collo»), anche se la voce dice «il tuo».

### «pensato per»

Opzione delle grafiche che mostrano un risultato, quando la voce lo dice: una riga sopra i termini, non verde. **Diventa
obbligatoria quando il risultato, letto da solo, sembra una promessa** (per esempio «ridurre gli attacchi»). Nel dubbio si
mette. Va scritta in `testi_detti` come le altre.

### Grafiche proposte (modello non ancora costruito)

Una grafica con un modello che il catalogo non ha ancora si scrive senza `elementi`, con `"proposta"`:

```json
{"nome": "beneficio", "momento": "beneficio", "proposta": {"da_modello": "connettore", "nuovo_id": "connettore-finestra",
  "reference": ["gadzhi-11"], "come": "..."}, "catalogo": "connettore-finestra", "modo": "finestra", "f0": 0, "frames": 0,
  "testi": [{"testo": "pensato per", "t": 0.1}], "testi_detti": [...], "impaginazione": "...", "voce": "...", "perche": "..."}
```

`reel-piano` controlla tempi, modo, 3D, sovrapposizioni, parole e testi detti come per le altre, e nella tavola disegna una
bozza statica. Il modello si costruisce come variante «in prova» (`motore/inserti/scene/<nome>_ads.*`, voce nel catalogo,
`catalogo.identifica`), poi si scrivono gli `elementi`; si mostra a Riccardo nell'anteprima.

### Mai card o riquadri vuoti

Una card, un riquadro o un pannello in attesa della sua frase non resta mai vuoto: ha un segnaposto estetico («?» con i
puntini, la cifra a contorno, un'icona sottile). Il direttore lo controlla.

### Aggancio nei primi secondi

Leggibile dal primo fotogramma (niente decifrazione, niente testo che nasce sfocato al fotogramma 0: è quello che si vede
mentre si scorre); solo parole dette, senza «il tuo».

### Forme e geometria

Le forme e il modello sono in [references/reel.md](references/reel.md), sezione 0. In più, per gli ads a finestre:

- **pannello al posto di una finestra** (`modo: "finestra"`): dentro la finestra grande in alto degli schemi A e B, al posto del
  B-roll, con lo stesso rettangolo e gli stessi angoli (`rett` = `rett_grafica` dell'inquadratura nella radiografia); se la
  grafica attraversa un taglio, una lista `[{da, x, y, w, h, r}]` che cambia sul fotogramma del taglio (se la finestra cambia
  di 1–2 px, un rettangolo che copra tutte e due); finestre in basso, sottotitoli e fondo restano intatti; niente nella fessura
  dei sottotitoli;
- **grafica piena** (`modo: "tutto schermo"` o una forma piena del sistema di forme): solo quando il contenuto riempie lo
  schermo, breve (al massimo 4 s, 3 per reel), mai sulle inquadrature con le 3D; copre tutta la riga dei sottotitoli per tutta
  la sua durata (caso (b)). La fascia trasparente per i sottotitoli non si usa;
- la striscia libera sopra le finestre non si usa.

### I tempi sulla voce

Tutti i tempi in `elementi` sono in secondi dall'inizio della pagina (`f0`).

- **Entrata**: un testo compare sulla sua parola (`a_inviluppo`), al massimo 1–2 fotogrammi prima; una grafica entra 1
  fotogramma prima della prima parola, o sul taglio d'inquadratura più vicino. `reel-piano` segnala gli scarti oltre 0,5 s:
  quelli voluti si scrivono in `perche` (per esempio una frase che resta sul pannello dopo un passaggio rapido del montaggio).
- **Uscita**: sul taglio d'inquadratura o sul fotogramma prima della grafica dopo, a taglio (le dissolvenze raddoppiano
  l'immagine). Due grafiche non si sovrappongono mai.
- **Mai lo stesso modello due volte di fila** (lo controlla il motore), tranne il sistema di forme (`infografica_reel` in modo
  palco), che resta lo stesso per tutto il reel per scelta.

### Lezioni dei modelli (errori visti davvero)

- **Uscite**: l'animazione d'uscita finisce sull'ultimo fotogramma reso; si esce a taglio.
- **Entrate**: niente primo fotogramma vuoto; il fondo e i primi pezzi sono già pieni al taglio.
- **Velo e maschere**: le card in secondo piano sotto un velo opaco (#001A3D, 45–60%), non trasparenti; una maschera sopra una
  parola che brilla taglia il bagliore in un rettangolo.
- **Decifrazioni**: solo lettere della stessa larghezza; «i», «l», «j» non si rimescolano (una «l» provvisoria sembra un «1»);
  le cifre non si decifrano mai.
- **Corpo e larghezza**: misura le righe con PIL a peso 800 prima di scrivere il piano (Montserrat 800 è ~10% più larga del
  peso normale); un «colpo di scala» del 3% può portare il testo fuori dalla zona sicura (tienilo all'1,5% o spezza la riga).
- **Due momenti della stessa grafica non si sovrappongono.**
- **Modulo** (chiusura): campi vuoti, senza etichette né dati; il pulsante usa solo una parola detta («compila»).
- **Ombre**: l'ombra di una forma o di una card non arriva sulla fascia dei sottotitoli (le card del pannello basso finiscono
  ~70 px sopra la riga; nei fotogrammi di passaggio della tendina niente ombra). Il controllo dei sottotitoli lo trova.

Dopo `./mve reel-piano <slug>`: correggi tutti gli **errori**, guarda tu `piano/tavola.jpg` con Read, prova le grafiche più
delicate con `./mve reel-prova` e guarda i fogli, poi vai al render (niente fermata sul piano).

## Tappa 3: rendi, controlli, voto

`./mve reel-rendi <slug>` (circa 15 minuti per un reel di 75 s). Le grafiche già rese restano in cache
(`.lavoro/<slug>/rendi/mov/`, chiave = md5 della pagina). I controlli sono in `controlli/controlli.md`; un errore ferma la tappa.

| controllo | come | limite |
|---|---|---|
| audio | md5 del flusso della versione senza effetti; prova che, tolti gli effetti, l'audio è l'originale | identico; residuo al livello della ricodifica |
| **sottotitoli** | `reel_sottotitoli.controlla` su ogni fotogramma con una riga: (a) base identico nella fascia e alfa delle grafiche ≤ 6, più un controllo largo sul finito; (b) alfa ≥ 250 su almeno il 99,5% della riga e Vision che non legge parole della riga nella parte di video visibile | ogni fotogramma (a) o (b); i tratti (b) nel report |
| video fuori dalle grafiche | SSIM sui fotogrammi senza grafiche | ≥ 0,99 (sui video di camera la sola ricodifica perde ~0,01: il motore misura una ricodifica pulita e accetta fino a 0,008 in meno) |
| sovrapposizioni, 3D, finestra | canale alfa del MOV, fotogramma per fotogramma | 0 fotogrammi in comune; niente forme sulle 3D; alfa 0 fuori dalla finestra |
| zoom | fotogrammi fuori dallo zoom identici bit per bit; colori della zona ingrandita | ≤ 1 livello |
| lettere intere e zona sicura | variante «solo testo» fotografata su ogni fotogramma visibile | testo in x 65–1014, y 269–1247 |
| cifre non dette | testo letto dalla pagina (`reel_dom.mjs`) su ogni fotogramma, anche per un solo fotogramma | 0 |
| solo parole dette | ogni parola ferma almeno 3 fotogrammi deve stare nell'SRT | 0 parole fuori |
| corpo | corpo effettivo dei testi fermi | ≥ minimo |
| cifre secondo Vision | Apple Vision su ogni fotogramma con grafiche del video finito; una lettura è spiegata se la pagina mostra quella cifra nello stesso punto | quelle non spiegate le guardi tu |

**Le letture di Vision non spiegate** sono ritagliate in `controlli/cifre-da-guardare/`. Aprile con Read, una per una. Di
solito sono letture sbagliate (un «?» letto «2», un «€» sfocato letto «3», un retino letto «s888», l'insegna MOBILITAS del
montaggio letta «1AZIONE»). Se è così: `./mve reel-guardato <slug> "f1959:3" "€ sfocato letto come 3"`. Se invece c'è davvero
una cifra non detta, è un errore: correggi il modello o il piano.

**Anteprima per Riccardo** (la fa `reel-rendi` in `anteprime/`): `<slug>_lavoro-intero.mp4` (con effetti),
`<slug>_lavoro-intero-senza-effetti.mp4`, la copia `-ZONE-META`, la tavola `<slug>_tavola-scene-reference.jpg`, le anteprime
±3 s e i provini. L'affiancato originale | nuovo si fa con ffmpeg (`hstack` dei due video ridotti a 540×960, con
un'etichetta sopra ognuno, audio della versione con gli effetti) in `anteprime/<slug>_confronto-originale-vs-nuovo.mp4`.

**Voto del direttore artistico**:

1. per ogni grafica, lancia il subagente `direttore-reel` con il prompt di `.lavoro/<slug>/direttore/<grafica>/PROMPT.md`
   (dentro: provino, foglio a 390 px, fotogrammi interi, la tavola scena ↔ reference, le reference citate); poi il reel intero
   con `.lavoro/<slug>/direttore/_insieme/PROMPT.md`. Lanciali in parallelo;
2. registra il voto con `./mve reel-voto <slug> <grafica> <voto> --giro 1 --nota "..."`;
3. se il voto è sotto 7, correggi quello che il direttore indica e fai il giro 2 (l'ultimo). Se resta sotto 7, decide Riccardo;
4. un ritocco dopo il voto cambia la pagina: il voto non vale più; le correzioni di esecuzione dopo il giro 2 si fanno e si
   scrivono come «non rivotate». Non c'è un giro 3: `reel-stato` mette una grafica ritoccata dopo il giro 2 fra quelle che
   decide Riccardo, anche se il suo ultimo voto era 7 o più (motore, 09/11/2026).

Il parere del direttore è un ingresso: controlla che i fotogrammi citati mostrino quello che dice. **Il direttore resta cieco**:
nel suo prompt non si mettono le scelte già approvate. Dopo il voto dividi le sue osservazioni con l'elenco di
[references/scelte-approvate.md](references/scelte-approvate.md):

- **difetti di esecuzione**: si correggono;
- **scelte già approvate da Riccardo**: non si toccano e si scrivono a parte nel report.

Un voto sotto 7 dato solo per scelte approvate non chiede un giro 2: lo riporti a Riccardo. Quando Riccardo approva una scelta
nuova, aggiungila all'elenco. Poi **fermati**: scrivi a Riccardo l'esito dei controlli, i tratti senza sottotitoli, i voti e i
percorsi dei file da guardare.

## Tappa 4: consegna

Solo dopo l'ok di Riccardo sull'anteprima e `./mve reel-approva <slug> anteprime`, lancia `./mve reel-consegna <slug>`. Copia
il file approvato (e la versione senza effetti), controlla l'md5 e scrive `consegna.md` con grafiche, controlli, voti e date.
I file si chiamano `<slug>_infografiche.mp4`; se il nome consegnato deve essere diverso dallo slug di lavoro (per esempio senza
«-prova_…»), prima della consegna si scrive `"nome_consegna": "AD_CERV_26"` in `videos/<slug>/reel.json` (vale anche per
`reel-stato`).
Mette anche una copia in `consegne/` (stesso nome, md5 identico): è la cartella con tutti i video finiti. L'ok di Riccardo
sull'anteprima vale anche come sua decisione sui voti rimasti sotto 7 e sulle grafiche ritoccate dopo il giro 2. Prima di dire «consegnato», controlla sul disco con
`ls -la` e `md5` e leggi `consegna.md`. Poi `./mve reel-pulisci <slug>`.

## Varianti e modelli «in prova»

- Una voce del catalogo con `"in_prova": true` è un modello o una variante che aspetta l'ok di Riccardo (per esempio
  `infografica-*`; `equazione-finestra-v2`, `etichette-barrate-finestra-v2`,
  `chiusura-9x16-v2`).
- **I piani nuovi la usano al posto del modello di partenza**: `reel-piano` lo accetta e lo segnala come IN PROVA; se un piano
  usa ancora il modello di partenza, avvisa di usare la variante.
- Nel messaggio a Riccardo scrivi quali grafiche usano modelli in prova: diventano «attivi» con il suo ok sull'anteprima.
- Un modello nuovo si prova su un reel già fatto, in uno slug di prova con `"laboratorio": true` nel piano:
  `./mve reel-rendi <slug> --laboratorio` (anteprima senza approvazione, non si consegna), controlli, voto del direttore.

## Render e regressione

- **Render**: HyperFrames in un solo processo, con la GPU (`reel_grafiche.WORKERS`, `reel_grafiche.GPU`); non si cambia senza l'ok di Riccardo.
  Le piccole differenze fra due render vanno bene, perché la consegna è sempre la copia del file approvato. Chrome senza GPU
  dà file identici, ma taglia i bagliori grandi con uno scalino netto: non si usa.
- **Regressione**: `./mve reel-regressione` rifà da zero il caso fisso `campionario/regressione/reel/AD_CERVICALGIA_AI-Barontini/`
  (il video è in `sorgente/`) e lo confronta con il riferimento: radiografia, ogni fotogramma, audio, controlli, sottotitoli.
  Circa 15 minuti.
  - **Quando**: dopo ogni modifica a `reel*.py`, `reel_dom.mjs`, `*.swift` o ai modelli `*_ads*`, `*_reel*`.
  - **Esiti**: **OK** (tutto uguale o solo arrotondamenti: scarti fino a 2 livelli sulle medie 8×8 delle grafiche); **CAMBIATO**
    (guarda `ultimo/ESITO.md` e spiega ogni differenza; se il cambio è voluto, `./mve reel-regressione --riferimento` e lo
    scrivi nel report); **ROTTO** (correggi subito).
  - Il caso usa i modelli approvati di partenza, non le varianti in prova: misura che il motore non cambi.

## Catalogo e file condivisi

- Il catalogo **si aggiunge e non si toglie**: niente si cancella o si declassa senza l'ok di Riccardo.
- Un modello nuovo nasce come file nuovo in `motore/inserti/scene/<nome>_ads.*` o `_reel.*`, senza toccare quello di partenza,
  con una voce nel catalogo e le righe in `catalogo.identifica`.
- File condivisi con l'agente video YouTube (`_scena.js`, `_scena.html`, `scena.py`, `brand.json`, `impagina.py`,
  `inserti.py`): non si toccano.

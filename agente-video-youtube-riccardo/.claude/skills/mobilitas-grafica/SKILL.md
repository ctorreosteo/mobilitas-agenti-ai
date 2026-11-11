---
name: mobilitas-grafica
description: Come si producono grafica, suono e formati derivati dei video @Studio_Mobilitas — sottotitoli karaoke, card che sanno dov'è il volto, titoli che passano dietro la presentatrice (sagoma Apple Vision), sound design sintetizzato, Shorts 9:16 dal 4K, miniature scelte sulla qualità del volto. Renderer Pillow che scrive RGBA nella pipe di ffmpeg. Usala quando un video deve uscire con grafica, suoni, Shorts o miniature, o quando qualcosa di questo va corretto.
---

# mobilitas-grafica

Lo stile lo detta `mobilitas-style`; qui c'è come si produce. Le decisioni (quali card, quali titoli, quali Shorts) sono in `regia.json` (skill `mobilitas-regia`).

## Il catalogo dei modelli: nessun modello si dimentica (fase 7c, Riccardo 01/11/2026)

**Ogni piano grafico parte dal catalogo intero**: `motore/inserti/CATALOGO-MODELLI.md` (da leggere) e `CATALOGO-MODELLI.json` (lo legge il motore). Dentro ci sono tutti i modelli costruiti finora (campionari v1, v2, v3, MR_POSTURA_01, YT_POSTURA_32) con: famiglia, cosa fa, quando usarlo e quando no, condizioni, reference, ultimo voto, un fotogramma d'esempio (`motore/inserti/catalogo/<id>.jpg`) e lo stato.

| stato | cosa vuol dire |
|---|---|
| **attivo** | si usa |
| **variante** | versione precedente di un modello migliorato: resta disponibile (es. `luce: 'classica'`, `fondo: 'velo'`, `forma: 'maiuscolo'`) |
| **vietato** | non si usa: oggi solo la sagoma vettoriale e il telefono con la sagoma |

Regole:
- **si aggiunge e basta**: un modello nuovo entra nel catalogo prima di essere usato (il motore rifiuta un modello che non c'è). Niente si cancella o si declassa senza l'ok di Riccardo;
- per ogni video si sceglie **per occasione** (la colonna «quando usarlo»), si **mescolano le famiglie**, non si usa tutto in ogni video, **mai lo stesso modello due volte di fila**. `./mve scena` lo controlla con `catalogo.controlla()` ed esce se il piano non lo rispetta; `./mve catalogo <slug>` stampa il catalogo e l'uso;
- **condizioni misurate dal motore** (`scena.condizioni()`, fra i controlli di ogni scena):
  - `zona_libera` (connettore, riga di icone): sotto l'elemento al massimo il 10% di mani (Vision), oggetti e modellini. Nelle inquadrature con la scrivania la parte bassa non è libera: si alza l'elemento sopra il piano del tavolo o si stringe l'inquadratura;
  - `vetro_zona_ricca` (vetro con più luce): sotto il pannello luminanza media > 80 o dettaglio > 40 (davanti a pianta o scrivania, non sul muro scuro);
  - `tempo_detto` (linea del tempo): lui dice un tempo o una durata mentre la linea è a schermo;
- l'uso di ogni video si registra in `libreria/uso-modelli.json` (lo scrive `scena`);
- **regressione**: in `campionario/regressione/` c'è un caso per ogni modello attivo (spec congelata in `casi/`, fotogrammi chiave in `riferimento/` e `ultimo/`). **Dopo ogni modifica ai pezzi condivisi** (`_scena.js`, `_scena.html`, `scena.py`, `brand.json`, `impagina.py`) si lancia `./mve regressione tutti` e si legge `REGRESSIONE.md`: un modello vecchio ROTTO (costruzione fallita o controllo che non passa) si corregge subito; CAMBIATO vuol dire fotogrammi diversi dal riferimento: si guarda il foglio e, se il cambio è voluto, si rifà il riferimento con `--riferimento`.

### Brand dal sito nei modelli (fase 7c)

Valori in `brand.json` (`fondo_scuro`, `titoli`, `etichette`, `loghi.pittogramma`), variabili CSS in `assets/comune.css` (`--fondo-sito`, `--grad-titolo`, `--panna70`, `--abisso`), classi in `_scena.html`:
- `.fondo-sito`: le scene scure a tutto schermo (card accese, linea del tempo, schermata piena, chiusura, schermata finale, anatomia piena) e `fondo_brand()` del compositore;
- titoli (`titolo_dietro`, `schermata` piena): minuscolo con il punto finale, 900, -0,045 em, interlinea 0,92, parola chiave `.grad` (verde → azzurro). `titolo_dietro.dati.chiave` = le parole in gradiente (default l'ultima riga); `forma: 'maiuscolo'` = la variante di YT_POSTURA_32. L'azzurro solo dentro il gradiente;
- `.eyebrow`: maiuscolo spaziato 0,22 em, 700, verde, con il filetto davanti, almeno 30 px: solo etichette strutturali brevi;
- `.sec`: testo secondario panna al 70%;
- `.pittogramma`: il pittogramma (non ricolorato) su un disco panna: nella schermata finale accanto al logo e nel chip (`chip.stile: 'v3'`, Pillow).

Scontorno dei render dell'app (`inserti.scontorna_render`): `titolo: false` per i render senza titolo in alto, `tieni_bianco: true` per tenere le card bianche che galleggiano sul fondo (si scrivono nella schermata del telefono in regia).

Schermate dell'app con dati di persone (nome, sigla, pagamenti, importi) o frasi sulla salute: si usano (Riccardo, 02/11/2026: «utilizzale tutte, in maniera estetica e minimale») con quelle righe sfocate, `sfoca: [[x0, y0, x1, y1], ...]` in px del file. Più schermate nello stesso telefono cambiano sul posto, ognuna sulle sue parole.

## Perché Pillow in pipe

Questo `ffmpeg` non ha **né `libass` né `drawtext`**: il testo va rasterizzato fuori. Un compositore a browser su 24.000 frame sarebbe lento e dipenderebbe dalla rete. Il livello grafico si genera con Pillow e va **dritto nella pipe di ffmpeg** come RGBA grezzo (`motore/grafica/render.py`). Regge perché gli sprite si disegnano una volta sola e ogni banda di sottotitolo una volta per parola attiva.

## Le fasi

| fase | cosa | esce |
|---|---|---|
| `grafica` | ancora ogni elemento a una frase del montato | `data/grafica.json` |
| `inquadra` | sceglie il lato di card, apertura e chip **sul volto**, nel taglio in cui cadono | lati in `grafica.json` |
| `sagome` | sagoma della persona (Vision) nei frame dei titoli dietro | `data/sagome/` |
| `anteprima` | grafica sopra i frame veri del montato | `controlli/anteprima.jpg` |
| `suono` | sound design e mix | `assets/mix-finale.wav` |
| `inserti` | grafiche HyperFrames del piano (MOV con alfa) | `inserti/*.mov`, `data/inserti.json` |
| `finale` | montato + inserti + grafica in pipe + mix; `--anteprima`: 960x540 veloce + foglio dei momenti + tempi | `renders/<slug>_FINALE.mp4` / `_anteprima.mp4` |
| `shorts`, `miniature` | formati derivati | `shorts/`, `miniature/` |

`grafica` riscrive `grafica.json` da capo: dopo `grafica` va sempre rifatto `inquadra` (`./mve stato` lo dice).

## Versione 2 della grafica (27/10/2026)

Tutto si decide in `regia.json` (schema in `mobilitas-regia/references/schema.md`) e si ancora alle frasi, come le card.

- **Sottotitoli variante B** (`"sottotitoli": "chiave"`): niente sottotitoli parola per parola; solo le `frasi_chiave`, su un pannello laterale a tutta altezza (Pillow, `frase_chiave_sprite`): frase in Montserrat 300, parola chiave in 800 verde, freccia opzionale. La persona va dal lato opposto (`persona`). Una frase chiave si accorcia da sola se entra un inserto. L'SRT completo per YouTube esce comunque (il QC lo controlla).
- **Chip v2** (`"stile": "v2"`, `fino`): nome 300 e ruolo 500, filetto verde, in basso a sinistra, sul nome.
- **Inserti HyperFrames** (fase `inserti`, `motore/motore/inserti.py`): un MOV ProRes 4444 con alfa per inserto, da modelli riusabili in `motore/inserti/modelli/` (`aggancio`, `numero`, `sagoma`, `prodotto`, `telefono`, `primadopo`, `lista`, `scelte`, `modulo`, `chiusura`). Ogni modello è un `.js` (+ `.css`) che legge `window.DATI` e chiude con `chiudi()`; `_base.html`, `_comune.js` e lo stile generato da `brand.json` sono comuni. I tempi interni (voci, passi, scelte) si danno come frasi e diventano `t` relativi. `finale` li sovrappone al montato, sotto il livello Pillow.
  - Materiali: `P.materiale()` (prima `inbox/<SLUG>/materiali/`, poi `libreria/`); quelli in `materiali_vietati` fermano la fase.
  - `telefono`: render "da App Store" → `scontorna_render()` toglie il fondo chiaro collegato ai bordi e il titolo; schermate piatte (`"tipo": "piatta"`) → il telefono lo disegna il modello.
  - `primadopo`: punti posturali da Apple Vision (`visione.posa`), linea blu notte e verticale panna sulla foto chiara; a schermo solo le etichette date.
  - Regole: versione fissata, `motore/inserti/.casa/` come casa di HyperFrames (stato, cronologia e temporanei restano nel laboratorio), GSAP e font locali. Cache sul contenuto.
- **Continuità dei pannelli** (`piano._continuita`, in `grafica`, una volta per Pillow e HyperFrames): fra due elementi di fila (meno di 0,35 s, anche sovrapposti):
  - stesso lato → il pannello resta fermo, cambia solo il testo (dissolvenza 0,2 s); niente pannello che esce e rientra;
  - inserto a tutto schermo (senza `lato`, es. `primadopo`) → si entra e si esce a taglio netto, niente dissolvenza sopra un'altra inquadratura;
  - lati opposti → la frase chiave entra 0,28 s dopo lo stacco d'inquadratura (`ritardo`).
  I flag `entra`/`esce`/`ritardo` finiscono in `grafica.json`; ogni modello li rispetta (`muoviPannello`, `chiudi`). Il prodotto è escluso come primo elemento: il suo pannello è già uscito.
- **Pannelli**: blu notte pieno (niente vetro), 760 px; il testo dentro sta a `--margine` (110 px) dal bordo dello schermo e va a capo bilanciato (`text-wrap: balance` negli inserti, `_righe_bilanciate` in Pillow): niente parola sola sull'ultima riga. Testi da leggere almeno 40-44 px (si guardano anche sul telefono).
- **Modelli, opzioni utili**: `prodotto.etichetta_pos` (`basso_sx|basso_dx|alto_sx|alto_dx`: l'etichetta va dove nel B-roll non ci sono teste; si guarda il fotogramma); `modulo.freccia` (verso la descrizione: il modulo non si compila nel video); `sagoma.gradi` (piega massima, default 16); `numero` conta da quando il pannello si ferma fino all'istante in cui dice il numero.
- **B-roll** (`broll`): clip della libreria solo fra le utilizzabili, `pieno`, `affiancati` o `sequenza`; li monta `monta` (rallentati a 83% se 30 fps su 25, muti). Affiancati: ritaglio centrale 960 px di ciascuna, con un filetto blu notte di 6 px in mezzo. Prima di sceglierle **si guardano i fotogrammi**: l'indice non vede i marchi piccoli sull'intimo (in MR_POSTURA_01_v2 V20_Pistorio-13, FV_De Rosa-1 e V15_Audino-1 li avevano) né le insegne che si sommano fra due clip affiancate. I nomi dell'indice sono in NFD (macOS): regia può scriverli normalmente, il confronto è normalizzato.
- **Barra d'avanzamento**: sottile, in panna, in basso. C'è di default (video lunghi); nei mid-roll si toglie con `"barra_avanzamento": false` in regia (decisione di Riccardo, 27/10/2026: un mid-roll sta dentro un altro video, la barra non serve).
- **Suono**: ogni elemento nuovo ha il suo: fruscio all'entrata (dal lato del pannello; niente fruscio se il pannello c'è già), tic a ogni tempo interno, colpo su aggancio e chiusura, conteggio del numero, salita sulla sagoma, fruscio sui B-roll. 12-18 dB sotto la voce.

## Livello 3: la grafica dentro la scena (campionario, 27/10/2026)

La v2 copriva l'85% del tempo con lo stesso schema (persona tagliata di lato + pannello blu piatto): sembrava una presentazione. Il livello si alza con **mestiere e varietà, non con più grafica**: presentatore spesso a tutto schermo con la camera sempre un po' in movimento, grafiche più rare ma grandi e dentro la scena, un suono su ogni movimento. Regole del brand per il video in `motore/motore/brand.json` → `video` (decisione di Riccardo).

### Regole di mestiere (valgono per ogni modello)

- **Entrate di 8-12 frame** (a 25 fps: 0,32-0,48 s) con easing deciso: `expo.out`, oppure `back.out(1.0)` per un rimbalzo leggero (3,7%: il massimo è 5%). Costanti in `motore/inserti/scene/_scena.js`: `ENTRA` 10 frame, `ENTRA_GRANDE` 13, `ESCE` 6, `SFASA` 2,5, `RIMBALZO`.
- **Parole sfalsate di 2-3 frame** quando entrano insieme; quando lui le dice una per una, ognuna entra **sulla sua parola**.
- **Uscite più corte** delle entrate (6 frame, `power2.in`, con un filo di sfocatura).
- **Sfocatura di movimento sugli spostamenti veloci**: la camera la fa da sé (ritagli mediati dentro l'otturatore, mai attraverso un taglio); gli strati HyperFrames hanno `data-motion-blur="on"`. Eccezione: un elemento con `overflow: hidden` che si muove dentro (rulli) va escluso (`data-motion-blur="off"`), perché il renderer lo disegna fuori dal ritaglio.
- **Ogni elemento parte sulla sua parola (±2 frame)** e resta leggibile **almeno 1 s**. Le ancore si scrivono come frase (`{"w": "di te", "i": 1}`) e si agganciano all'attacco vero della voce (`scena.attacco`: salita di almeno 9 dB in 25 ms entro ±80 ms da whisper). Su MR_POSTURA_01 whisper sta entro ±60 ms sugli attacchi netti.
- **Mai più di 2 elementi insieme; il volto non si copre mai** (fuori dalle schermate piene, che sostituiscono il quadro). `scena.controlla` misura tutte e tre le cose. Il testo sul busto si scrive con `"sotto_volto": true`: il motore misura il punto più basso della testa (Vision) per tutta la durata dell'elemento e lo mette 24 px sotto. Un'altezza fissa non basta: in MR_POSTURA_01 lui si china e il mento scende di 60 px (il controllo l'ha trovato: 5,3% di copertura).
- **Testo grande per il telefono**: almeno 60 px a 1080p, 120+ per le parole chiave (pesi 700-900).
- **Il verde solo sul blu** anche qui: sul video nudo il testo è panna con ombra morbida; la parola chiave si distingue per peso e corpo. Il verde va su bottoni, card, schermate blu.
- **HyperFrames sposta la timeline senza eventi**: niente `onUpdate`/`onComplete` per cambiare ciò che si vede. Un conteggio si fa con un `tl.set` per frame; un attributo si anima con `attr`.

### Il motore: `motore/motore/scena.py`

Un pezzo vero del montato (uno o più intervalli, in secondi del montato) si ricompone dal 4K in cinque passi: **piatto** (frame dal 4K con la camera viva e il look; ritaglio sub-pixel Lanczos), **sagome** (Vision, solo se servono), **strati HyperFrames** `dietro` e `davanti` (MOV con alfa, modelli in `motore/inserti/scene/`), **composizione** (effetti di piatto → strato dietro ritagliato dalla sagoma con l'ombra morbida di lui sopra → strato davanti), **suono** (voce montata + `sfx.py`, -14 LUFS). Oggi lo usa `./mve campionario <slug>` con `campionario/campionario.json`; non è ancora collegato a `regia.json` né a `finale`.

| capacità | dove | cosa si scrive |
|---|---|---|
| camera viva | `scena.Camera` | `camera.base {z, cx, cy}`, `spinta` (0,02-0,04), `mosse` [{t, dur, z, cx, cy, ease}] o `{t, taglio: true}`. `z` sul 4K intero, mai oltre 2 |
| transizione a spinta | `piatto: {tipo: spinta, t, dur, dir}` + un taglio di camera allo stesso `t` | A esce di lato, B (l'inquadratura dopo il taglio) entra; sfocatura sulla velocità |
| transizione a zoom | tre mosse: zoom dentro `power4.in` fino al taglio, taglio a pari zoom, zoom fuori `expo.out` | |
| sfondo sfocato, scurito, luce | `piatto: sfoca_sfondo / scurisci (sfondo, basso, tutto) / luce` | con la sagoma: la persona resta nitida |
| look | `look: caldo / profondo` | LUT 3D generata in `.cache/`, vignetta a parte |
| strati | `elementi: [{modello, strato: dietro/davanti, s, e, dati, pieno}]` | `pieno: true` = schermata intera (esclusa dal controllo del volto) |

Modelli (`motore/inserti/scene/<nome>.js|css`, funzione `MODELLI.<nome>(box, x, d)`): `parole` (frase sul corpo), `numero_dietro`, `schermata` (tipografica a tutto schermo), `card` (fluttuanti vicino alle mani), `telefono3d`, `confronto` (prima/dopo con cursore; verifica la data EXIF), `cta`, `lista_attesa`, `etichetta` (solo campionario). I suoni di ogni modello sono in `scena.SUONI_MODELLI`.

### Suoni (`motore/motore/sfx.py`)

Sintetizzati, seconda generazione: corpo + transitorio, stereo che segue il movimento, coda di stanza, **3 varianti per nome che si ruotano** (lo stesso fruscio a ogni stacco è il segno del montaggio in serie). Nomi: `whoosh`, `swish`, `pop`, `click`, `tick`, `impact`, `riser`, `thump`, `scan`. Il livello si scrive in dB **rispetto alla voce** (RMS della finestra di 100 ms più forte) e il picco del suono cade un frame dopo l'immagine. Musica: solo se c'è un file con licenza; si abbassa da sola sotto la voce (sidechain).

### Verifica: strisce dell'entrata

Per ogni modello `campionario/controlli/<n>-striscia-*.jpg` (frame presi per indice da tutto il pezzo decodificato: `select` di ffmpeg a volte ne perdeva uno): un fotogramma ogni 2 frame dell'entrata, con lo scarto in frame dall'ancora, sotto l'inviluppo della voce con le parole; il riquadro rosso è la testa (`"volto": true`). Si guardano tutte prima di mostrare un modello.

### Livello 3, seconda iterazione (fase 6b, 27/10/2026)

Note di Riccardo sulla v1: elementi troppo piccoli, numero coperto, card "pillola da web", frase sul corpo che era un sottotitolo travestito, CTA "modulo a fil di ferro". Cosa vale da qui in poi (`./mve campionario <slug> --v2`, specifica in `campionario/v2/campionario.json`):

- **Si misura, non si stima a occhio** (`motore/motore/impagina.py`, font e pesi veri via PIL; la pagina usa le stesse regole: `line-height: 1`, cifre in celle fisse, posizioni assolute):
  - `numero_dietro`: posto e corpo li sceglie `piazza_numero` sulle sagome di tutta la durata: la persona copre **al massimo il 12%** del numero e **mai la prima cifra** (margine di 14 px attorno alla sagoma); "più di" sta sopra il primo glifo, allineato a lui; l'etichetta sotto, a sinistra o a destra dove è libera. Dopo il render `controlla` misura la copertura vera (alfa × sagoma, limite 15%). Su MR_POSTURA_01: 900 a sinistra con l'ultimo zero dietro la testa, 8% coperto, prima cifra 0,02%;
  - `card`: corpo del titolo uguale per tutto il gruppo, il massimo per cui la parola più lunga (o il titolo intero con `una_riga`) sta dentro i margini fissi; mai sotto 60 px. Il posto lo sceglie `piazza_card`: **mai sopra una mano** (Vision, +24 px) **o la testa** (+30 px) in tutto il tempo in cui la card è a schermo, sul lato `zona`, il più vicino alla mano da cui parte. Se non c'è posto il motore si ferma: si accorcia la card nel tempo o la si stringe, non si sposta a occhio;
  - `parole` a battute: una o due parole enormi (peso 900, fino a 260 px) per battuta, centrate sul busto e sotto il punto più basso della testa (`piazza_battute`);
  - `cta`, `lista_attesa`: ogni riga al corpo massimo che sta nella colonna (`adatta_colonna`).
- **Mani di Vision** (`visione mani`, nuovo comando in `motore/swift/visione.swift`): centro, riquadro e polso di ogni mano su ogni secondo frame del piatto. Servono a far partire la card dalla mano vera (un filo sottile la lega alla mano per 0,8 s) e al controllo "mani mai coperte" (pixel con alfa > 0,5, non l'ombra).
- **Mani davanti alla scritta** (`"mani_davanti": true`): la scritta sul busto sta fra il busto e le mani. Matte = sagoma × zona delle mani di Vision (+46 px) × pelle (la divisa blu notte resta dietro). Si misura quanta scritta coprono (limite 20%): oltre, la parola non si legge.
- **In tutti**: `fuoco` sull'elemento (lo sfondo si sfoca e scende del 20%, lui del 6-8%: la messa a fuoco va sulla grafica); `colpo` (punch-in del 3-5% in 0,14 s che torna piano lasciandone il 40%, insieme a un impatto); **parallasse** fra gli strati (la pagina riceve la camera di ogni frame: dietro 0,9, davanti 1,12, card 1,06 ciascuna dal suo ingresso, stacchi pieni 0); **maschere** (`maschera`, `rivela`, `nascondi` in `_scena.js`: il testo sale da dietro un bordo fermo, nascosto al 135% perché i puntini delle i non spuntino) al posto delle dissolvenze.
- **Finestra** (`piatto: {tipo: finestra, s, e, scala, x, y}`): il quadro diventa una finestra con angoli tondi, bordo panna 14% e ombra sul fondo del brand; spazio pulito per un momento forte (CTA). Gli elementi sopra sono `pieno`.
- **Suoni**: dalla libreria `libreria/sfx` (Pixabay, licenza nel catalogo) `whoosh`, `click`, `pop`; `impact` ibrido (sub della libreria + corpo sintetizzato sopra 150 Hz, bilanciati sull'energia: il sub da solo dal telefono non si sente); il resto sintetizzato. `sfx.suono(nome, seme, fonte='sintesi'|'libreria')` forza una fonte; il confronto A/B è `campionario/v2/10-suoni.mp4`.
- **Tavole** (`motore/motore/tavole.py`): per ogni modello il fotogramma migliore (`migliore` nella specifica), lo stesso a 390 px (telefono) e sei momenti chiave; il confronto con la reference se in `libreria/reference/` c'è un'immagine che comincia col numero del modello. Il subagente "direttore artistico" vota sulle tavole e sulle strisce.

### Il video intero: fase `scena` (fase 6c, 28/10/2026)

`./mve scena <slug> [--solo id,id]` (`motore/motore/video_scena.py`) ricompone il montato pulito dai **momenti** di `regia.json` → `scena.momenti`. Ogni momento è un pezzo contiguo del montato, scritto come una voce del campionario (camera, piatto, elementi, strisce). Poi `finale` e `qc` restano quelli di sempre. Con la scena `suono` e `anteprima` non servono: il mix unico (voce + tutti i suoni dei momenti + B-roll e chip, -14 LUFS) lo scrive `scena`. Il primo uso è MR_POSTURA_01_v3.

- **Copertura:** i momenti e i B-roll (da `monta`) coprono il montato senza buchi né sovrapposizioni, sulla griglia dei frame; la fase si ferma se non è così. Il montato di `monta` resta in `renders/<slug>_pulito_monta.mp4`.
- **Regole di regia:**
  - mai lo stesso modello due volte di fila;
  - lui a tutto schermo con la camera viva dove non serve grafica: nella v3, 6 momenti su 18;
  - la stessa chiamata all'azione non si ripete (il direttore artistico la segnala).
- **Confini dei momenti** sull'attacco vero della voce, non sull'inizio di whisper: una schermata che entra 5 frame prima della voce si vede.
- **Ancore:** una parola che compare più volte (es. «studio») si aggancia con `dopo`, altrimenti prende la prima occorrenza.
- **Controlli in più, nati dalla revisione della v3:**
  - strato davanti dentro la zona sicura (96/54 px; i movimenti che attraversano il bordo per scelta si guardano a mano);
  - nessun elemento sparito mentre è a schermo. Un `fromTo` con `immediateRender: false` deve avere l'opacità anche nell'arrivo, perché il render può saltare oltre l'inizio dell'animazione;
  - schermate: le righe si misurano tenendo conto dell'avanzamento al 107%.
- **Card dietro la persona** (`"strato": "dietro"`, card con `"dietro": true`): le mani le passano davanti. Il vincolo è «persona al massimo sul 10% della card, mai sul testo», misurato fotogramma per fotogramma, invece di «lontano dalle mani». Serve quando lui gesticola e una card davanti non trova posto.
- **Frase sul corpo:** `mani_max` (0-0,18) è il tetto delle mani sopra le lettere. Per le chiamate all'azione si usa 0: le mani restano davanti al busto ma passano dietro le lettere.
- **Revisione:** `python -m motore.foglio_scena <slug>` (dalla cartella `motore/`) produce `controlli/scena-momenti.jpg`, un fotogramma per momento dal master con la versione a 390 px. Revisore visivo e direttore artistico guardano quello e le strisce `scena-NN-<id>-K.jpg`.

### Video lungo: modelli nuovi della fase 7b (YT_POSTURA_32, 28/10/2026)

Cinque modelli in `motore/inserti/scene/`, con i loro suoni in `scena.SUONI_MODELLI`:

| modello | cosa fa | dati |
|---|---|---|
| `frase_chiave` | variante B dei sottotitoli dentro la scena: pannello blu a tutta altezza su un lato, la frase detta (peso 400, chiave 800 menta). La persona la sposta la camera del momento (`z 1.32, cx 0.379, cy 0.38`: testa intera, lui a destra). Escluso dal controllo della zona sicura, come le schermate | `lato`, `larghezza`, `corpo`, `margine`, `parole [{testo, chiave}]` |
| `titolo_dietro` | titolo di capitolo nello strato `dietro`. Con `auto: true` lo impagina `impagina.piazza_titolo`: corpo e posto misurati sulle sagome di tutta la durata, lui copre il 4-12% delle lettere, mai la prima, nessuna riga oltre il 20%, sopra il piano del tavolo (`y_max` 760: Vision conta come primo piano anche gli oggetti sul tavolo). Se non trova posto ripiega su un titolo leggibile non coperto e lo segnala | `linee`, `auto`, `corpo_max`, `corpo_min` |
| `anatomia` | disegno Servier di `libreria/anatomia/` ricolorato al render (`anatomia.ricolora`; il file resta l'originale), ritagliato e mai deformato, con sopra solo forme semplici nelle coordinate del disegno ORIGINALE: `alone`, `asse` (ruota), `freccia`, `numero`, `arco`, `linea` (si spezza), `contorno`. Etichette a schermo con le sue parole; attribuzione CC BY 4.0 | `disegno`, `alto`, `taglio`, `x`, `y`, `pannello`, `segni`, `etichette`, `attribuzione` |
| `tentativi` | lista che si allunga e torna fra le animazioni, con trattini e non spunte. Una voce ripresa da prima va dichiarata con `richiama` (istanti in cui l'ha detta), sennò il controllo dei contenuti la segnala | `x`, `y`, `larghezza`, `corpo`, `voci [{testo, t, nuova, sotto, sotto_t}]` |
| `sagoma` | sagoma posturale vettoriale (`anatomia.PROFILO`, non anatomia) in un «vetro»: la pancia va avanti o rientra, il bacino resta fermo | `x`, `y`, `larghezza`, `altezza`, `stati [{t, pancia, dur}]`, `freccia`, `bacino_t` |

Altro:
- `telefono3d` accetta schermate generate (`genera: foto_sagoma`, nessuna persona vera) e `cambio: dissolvenza` per la stessa foto che cambia;
- in un dizionario di `dati`, la chiave `w` fa scambiare l'oggetto per un'ancora: larghezze e altezze si chiamano `larghezza` e `altezza`;
- i tempi che il motore porta dal montato al momento sono le chiavi di `scena.TEMPI` (`s`, `e`, `t`, `arrivo`, `etichetta_t`, `t_ruota`, …). Un tempo dentro una lista si scrive come oggetto `{t: …}`;
- un'etichetta o card ferma accanto a lui va con `prof: 0`: con `prof: 1` cresce con la spinta della camera ed esce dalla zona sicura;
- frasi sul corpo: una battuta esce dopo la prima parola della successiva (lo strato non resta vuoto); le righe sopra i 1400 px entrano con un colpo al 103% invece che al 110%; con una negazione nella frase `mani_max: 0`, perché una mano sul «non» capovolge il senso.

**Superato dalla fase 7b rivista:** il modello `sagoma` (figura umana disegnata da noi) e le «foto» generate del telefono (`genera: foto_sagoma`) sono vietati. Restano nel motore solo per rifare l'anteprima vecchia: non si usano più.

## Linguaggio grafico Mobilitas (fase 7b rivista, 28/10/2026)

Viene dallo studio di `libreria/reference/` (14 clip; una riga per clip in `libreria/reference/catalogo.md`). I valori sono in `brand.json` → `video.linguaggio`, `video.regole_testo` e `video.servier_varieta`.

Le reference fissano **il livello**, non sono modelli da copiare. Per ogni video si sceglie cosa serve al contenuto e si inventano anche grafiche nuove, purché dello stesso livello.

**Prima di ogni video:** se in `libreria/reference/` ci sono file che il catalogo non ha, li guardi (fotogrammi a 10-12 al secondo), aggiungi le righe al catalogo e aggiorni linguaggio e regole. Nomi: `<fonte>-NN` (`martell-09.mov`, `nomecanale-01.mov`). Le reference non escono dal laboratorio.

### Due mondi che si alternano

- **Accanto a lui.** Punch-in o spostamento di camera quando arriva l'elemento, e il lato libero si riempie: liste, fumetti, card, vetro, foto vere. Mai sul volto o sulle mani.
- **Scena scura a tutto schermo.**
  - Fondo blu profondo → blu notte con una texture sottile: grana fine e curve di livello panna al 4-6%.
  - La camera si muove fra gli elementi: avanza lenta (circa 5% in 7 s) o scorre fra due punti in 0,8 s.
  - Ci si entra con un taglio netto o con un lampo di luce di 3-4 frame, mai con una dissolvenza lunga.
  - Nessuno dei due mondi per più di 2-3 momenti di fila.

### Le famiglie

| famiglia | come | reference |
|---|---|---|
| frase parola per parola | ogni parola nasce panna al 35% e sfocata, piena in 2-3 frame sulla voce, con il suo bagliore; la chiave in verde (sul blu) o in 900 | martell-07, martell-01 |
| lista voce per voce | segno (punto verde luminoso o icona) e testo che si scrive da sinistra in 4-6 frame, senza pannello, con ombra | gadzhi-04 |
| etichette luminose barrate | pillole blu notte con bordo e bagliore verdi; una riga le barra da sinistra in 3 frame sulla parola che le smonta | martell-01 |
| fumetti | panna a gradiente leggero, coda, ombra di contatto e luce interna, testo blu notte 700; nascono sfocati a 0,85 e sono nitidi in 4 frame; quelli di prima salgono | martell-05 |
| card con spessore | blu notte, bordo superiore chiaro, ombra di contatto più ombra morbida, texture fine; una ogni 0,25 s | gadzhi-06 |
| vetro | pannello smerigliato che sfoca lo studio vero, bordo panna sottile con riflesso; il contenuto arriva dopo il bordo | martell-06 |
| numeri | cifre che scorrono come un contachilometri e frenano sulla parola | gadzhi-03, martell-02 |
| anatomia | disegno Servier in una card (modelli approvati: l'animazione del meccanismo e la card della colonna dell'anteprima 7b) o in una scena scura con la camera sulla parte nominata | martell-07 per la scena |
| oggetti veri | iPhone realistico (fonte approvata), foto vere con il viso tagliato fuori | martell-06 |

### Movimento, luce, sincronia

- **Entrata:** 0,25-0,4 s (6-10 frame a 25 fps), con la sfocatura che si scioglie, `power3.out`. Rimbalzo solo su fumetti e pillole (`back.out` ≤ 1,4).
- **Uscita:** con lo stacco, o in 4-6 frame.
- **Sfasamento** fra elementi della stessa famiglia: 0,25 s.
- **Luce:**
  - sulle scene scure gli elementi emettono luce, con un bagliore dello stesso colore in due strati (8-12 px e 30-50 px);
  - quando arriva un elemento grande sopra di lui, lo sfondo si scurisce del 20-30% e si sfoca in 3 frame.
- **Sincronia:** nessun elemento arriva prima della sua parola.
- **Colore:** un solo accento forte per video, per noi il verde `#72FA93` come luce e accento, solo sul blu. Il resto è panna e blu.

### Regole (valgono sempre)

- **Nessun testo esce dal quadro** in nessun fotogramma, entrate comprese. Il motore lo misura su ogni frame (`scena.fuori_quadro`).
- **Scritte bianche sulla scena:** ombra morbida forte dietro (`0 4px 14px` e `0 0 44px` in blu profondo).
- **Numeri delle animazioni:** solo accanto alla parte del corpo, mai nel testo. Si scrive «la schiena bassa si inarca di più», non «1 la schiena…».
- **Attribuzione Servier:** una riga, dentro i margini della card.
- **Vietate le figure umane disegnate da noi** (sagome, profili, icone di persona). Il corpo si mostra solo con disegni Servier anatomicamente corretti o con riprese e foto vere.
- **Servier:**
  - alterna uomo e donna e cambia vista (scheletro intero, colonna, bacino, muscoli), mai la stessa figura due volte di fila;
  - se il tema è generico, solo le ossa, senza il contorno del corpo;
  - quello che manca si scarica da smart.servier.com, con licenza e attribuzione nel catalogo.

  Limite (28/10/2026): l'uomo c'è solo di fronte; di profilo ci sono solo la donna e lo scheletro neutro.
- **Telefono:** solo un iPhone realistico di ultima generazione, con dentro solo contenuti veri. La fonte del modello si propone con la licenza e si approva prima di scaricarla.
- **Foto dei pazienti:**
  - solo con il consenso del catalogo;
  - viso tagliato fuori;
  - «prima» e «dopo» dalla data EXIF;
  - a schermo solo PRIMA e DOPO, o niente.

### I modelli del linguaggio (fase 7b rivista, `motore/inserti/scene/`)

| modello | famiglia | dati principali |
|---|---|---|
| `fumetti` | fumetti di chat accanto a lui; nascono sfocati a 0,85, i precedenti salgono | `x`, `y` (fondo della pila, all'altezza delle spalle), `corpo`, `lato`, `voci [{righe, t, larg}]` |
| `etichette_luce` | pillole blu con bordo e bagliore verdi; `barra_t` la barra sulla parola; `accesa: false` = richiamo, si barra 3 frame dopo l'atterraggio | `x`, `y`, `corpo`, `voci [{testo, t, larg, barra_t, sotto, sotto_t}]` |
| `card_spessore` | card una sotto l'altra con un ritaglio Servier (`disegno`, `ritaglio`, `alto`, `luce`) e testo con `*parola chiave*`; attribuzione dentro l'ultima card | `x`, `y`, `larghezza`, `altezza`, `img_larghezza`, `carte [...]` |
| `frase_luce` | frase parola per parola sulla voce, `a_capo` sulle parole dove la frase va a capo; facoltativo `vetro` (bordo e riflesso; lo studio sfocato lo fa l'effetto di piatto `vetro` con la stessa geometria) | `x`, `y`, `larghezza`, `corpo`, `peso`, `parole [{testo, t, chiave, a_capo}]` |
| `foto_card` | foto di `libreria/prima-dopo` in una card: consenso controllato sul catalogo, «prima» e «dopo» sulla data EXIF (`confronta_con`), viso tagliato con `ritaglio`; anelli verdi su un contorno blu profondo | `foto`, `ritaglio`, `x`, `y`, `larghezza`, `altezza`, `anelli [{ox, oy, orx, ory, t}]` (px originali) |
| `anatomia` (esteso) | `pannello.trama` (curve di livello e grana: scena scura); a tutto schermo entra a taglio netto con un lampo panna; `camera_scena [{t, scala, x, y, dur}]`; etichette con `parole` (parola per parola); `ritaglio` e `sfuma_bordi` sul disegno; `modo: 'muscoli'` per le tavole dei muscoli | come prima |

Effetti di piatto nuovi (`scena.componi`):
- `vetro`: rettangolo arrotondato con lo studio sfocato e velato (`tinta`, `chiaro`, `raggio_sf`). `guadagno` schiarisce lo studio dietro il vetro;
- `lampo`: luce piena per pochi frame.

**Frase chiave B (vetro), versione scelta da Riccardo il 29/10.** Il vetro *schiarisce* lo studio (`guadagno` 1,38, `tinta` chiara, `chiaro` 0,10) invece di scurirlo: sul muro scuro, velato di blu, diventava un riquadro scuro. Ha un bordo di luce panna all'82% e si misura sul testo, che lo riempie (padding 0,62 × corpo). Si costruisce con `vetro()` in `.lavoro/anteprima_v2_spec.py`, con il punch-in a taglio netto e il lato alternato.

`anatomia`: nelle scene scure senza finestra c'è una luce blu morbida dietro la figura (`an-luce`; `luce: false` la toglie). Con la finestra di lui accanto non serve.

`mani_minimo` (px) su un elemento con `mani_davanti`: i pezzi di mano più stretti di così non passano davanti alle lettere, mentre la mano intera sì. È nato da un dito che bucava la «p» di «sporge»; per «La pancia sporge» si usa 41.

Regole che il motore ora misura:
- **niente fuori dal quadro**: pixel pieni dello strato sul bordo di 3 px, su ogni frame (`scena.fuori_quadro`). Nelle scene piene, dove lo strato copre tutto, si misurano i testi con il font vero (etichette e attribuzione);
- **titolo dietro**: la prima lettera di ogni parola libera, l'ultima coperta al massimo al 15%, le altre al 30% (`impagina.piazza_titolo`). Prima si leggeva «PARTIAM», poi «PARTIAMC»: il limite al 50% non bastava;
- **frase sul corpo**: le parole possono avere `scala` e `peso` (gerarchia «La pancia **sporge**»), e `piazza_battute` le misura parola per parola.

Lezioni del campione (voto del direttore artistico):
- un elemento accanto a lui non scende sotto il bordo del tavolo (y ≤ 840): altrimenti taglia gli oggetti sul tavolo e sembra un errore;
- quando arriva un elemento grande, lo sfondo si scurisce del 20-25% (`scurisci` `sfondo`, rampa 0,12 s);
- gli effetti sulla persona (`fuoco`) partono dopo lo spostamento della camera: durante lo spostamento la sagoma non tiene e il volto si sfoca per qualche frame;
- l'interlinea in `px()` va passata come stringa: un numero diventa «1.08px» e le righe finiscono una sopra l'altra;
- il vetro su un muro scuro diventa nebbia; il velo di blu profondo lo rende un riquadro scuro. Mai sul volto.
- sulle foto vere niente `hue-rotate` né filtri che spostano la tinta: nel campione la pelle di una paziente è diventata blu-verde. Solo saturazione e luminosità;
- nei punch-in in cui un effetto separa la persona dallo sfondo (`fuoco`, `scurisci sfondo`), la camera fa un taglio netto, non uno spostamento;
- il vetro su un muro scuro: **superato** (29/10). Il vetro ora schiarisce, con il bordo di luce: vedi sopra;
- in ogni frase chiave c'è una parola verde nei primi 0,5-1,5 s, non solo alla fine;
- un titolo dietro lungo («Sul davanti dell'anca») su tre righe non trova posto: va su due righe («Sul davanti / dell'anca»), con `corpo_min` 96;
- voto del direttore sul campione dopo tre giri: 7 su tutto, nessun 8. Per l'8 mancano soprattutto luce e presenza negli elementi (pillole, fumetti, la frase sul corpo, la figura delle scene scure).

### Famiglie nuove dalle reference del 30/10/2026 (`gadzhi-07` … `gadzhi-15`)

Studio completo in `libreria/reference/catalogo.md` («cosa portano di nuovo»). Le prove sono nel campionario v3 (`campionario/v3/`). **Dalla fase 7c (Riccardo) tutti e nove sono attivi**, con le condizioni del catalogo; etichette con più luce e schermata su fondo blu sono la versione principale, le vecchie restano varianti. Lui nel cerchio: la finestra si compone sopra gli strati del disegno, così lo scheletro entra mentre lui si stringe.

- **card che si accendono**: card 3D in prospettiva con cifra gigante a contorno, che arrivano nascoste (scansione luminosa) e si accendono una alla volta quando lui le nomina: bordo, testo che si decifra, riempimento di luce verde con riflesso e colpo di scala;
- **testo che si decifra**: lettere che si rimescolano (caratteri seminati, deterministici) e si fermano sulla parola detta, in 6-8 frame;
- **linea del tempo luminosa**: un nodo che disegna la linea mentre la percorre, la camera che lo segue, fondo a retino di punti. Solo con tempi detti da lui, mai dati inventati;
- **equazione detta**: testo piccolo laterale, i termini scritti mentre lui li dice, gli operatori (+, =, →) in verde come etichette strutturali; esce cancellandosi all'indietro;
- **connettore**: due etichette unite da una linea luminosa che si disegna dal centro, con un segno al centro;
- **riga di icone in basso**: icone lineari (mai figure umane) che si disegnano una alla volta, fondo scurito dal basso;
- **lui in un cerchio**: il quadro si stacca, diventa un rettangolo tondo e poi un cerchio nell'angolo, mentre dietro compare la scena scura.

Le regole di sempre valgono anche qui: testi dentro il quadro, nessuna sovrapposizione, lettere intere, ogni parola detta, anatomia solo Servier con l'attribuzione.

## Sottotitoli

Gruppi da 2-3 parole, chiusi da punteggiatura di fine frase, pausa oltre 0,45 s o 2,4 s di durata. La parola attiva è in menta con una barretta sotto. Si spengono durante i titoli e la chiusura (dicono le stesse parole).

Le parole vengono da `parole-montato.json`, trascritto a pezzi da 10 s: la versione su file intero perdeva la prima parola di molte frasi (in YT_TOFU_02 143 parole su 2161). Il QC controlla che i sottotitoli coprano almeno il 99% delle parole.

Le correzioni di trascrizione (`correzioni` in regia) toccano solo il testo, mai l'audio. Oltre all'impresso si consegna l'SRT (`consegna`): massimo 2 righe da 42 caratteri, e mai una battuta di una parola sola (si unisce alla precedente o alla successiva).

## Card

Ancorate alla frase, 0,25 s prima, per 4,2 s. Una card che cadrebbe durante un titolo aspetta che esca. Il lato lo sceglie `inquadra`: proietta il riquadro della testa (volto di Vision + capelli) nel taglio in cui la card sta a schermo e prende il lato con più margine. Il margine minimo sta in `grafica.json` (`margine_volto`, in px) e il QC fallisce se una card tocca la testa.

## Titoli dietro

Il capitolo si scrive a tutta larghezza e si ritaglia con la sagoma della persona: passa dietro di lei. Per costruzione non le copre mai il volto.

- Entra sulla parola d'ancoraggio, le righe salgono una dopo l'altra (0,45 s, 0,12 s di sfasamento), dura 2,6-4 s.
- Lo sfondo dietro si scurisce (navy, alfa 120) per il contrasto della menta sul teal.
- L'eyebrow sta **sopra** la persona, allineato alla prima riga: dietro la testa sparirebbe.
- **La posizione si misura.** Le righe vanno all'altezza e allo spostamento orizzontale in cui la persona nasconde meno lettere della **parola peggiore** (non della media: "NON M▒▒BOLICO" non si legge anche con il 20% medio coperto). Il renderer stampa la percentuale per ogni titolo. Sopra il 30% conviene accorciare il titolo o cambiarlo.
- Il taglio durante il titolo è **largo**: al medio la persona è più larga e nasconde un terzo in più.
- Le sagome si calcolano sul montato pulito: se cambia l'inquadratura, vanno rifatte (`sagome`).

## Stacchi pieni

Con `"dietro": false` il capitolo è una scheda piena navy di 1,75 s che entra 1,3 s prima della frase e cade sulla pausa. Resta per i video in cui la sagoma non si può usare (più persone, sfondo complicato).

## Sound design (`suono`)

Sintetizzato con numpy, niente stock: whoosh all'ingresso delle card (nel panorama dal lato della card), tick sul numero, salita + colpo basso sui titoli dietro, fruscio corto sui punch-in d'enfasi, colpo morbido su apertura e chiusura. Tutto 10-16 dB sotto la voce. Musica solo se c'è un file in `assets/musica/`: in loop a −30 LUFS, con sidechain sotto la voce.

## Shorts

Fuori dal flusso standard dal 30/10/2026 (si consegnano solo video, SRT e youtube.txt): la fase resta e si usa solo se Riccardo la chiede.

Dalle `shorts` di regia. Ritaglio verticale dal 4K (1215x2160 a tutta altezza → 1080x1920 senza perdita), due tagli alternati (pieno e stretto 1,22) a ogni giunta e circa ogni 6 s, volto centrato. Hook in alto sotto i 260 px della barra di Shorts, barra di avanzamento sotto l'hook, sottotitoli da 84 px con base a y 1300 (sopra i ~420 px dell'interfaccia in basso), 1,6 s finali con "IL VIDEO COMPLETO È SUL CANALE". Audio dalla voce già montata, a −14 LUFS. Foglio di controllo: `controlli/short<N>.jpg`.

## Miniature

Fuori dal flusso standard dal 30/10/2026, come gli Shorts.

Tre varianti 1280x720 dai fotogrammi con la qualità del volto più alta per Vision, occhi aperti e viso frontale, a 20 s l'uno dall'altro. Soggetto a destra (taglio 1,45 dal 4K), pannello navy che sfuma a sinistra, due righe in Montserrat 900 (l'ultima in menta). `controlli/miniatura-piccola.png` è la miniatura a 168 px, come appare nella griglia di YouTube: va guardata.

## Verifica

### Tappa 3 (YT_POSTURA_32, 30/10/2026): tre controlli nuovi in ogni scena

Ogni difetto segnalato da Riccardo sull'anteprima v2 è diventato un controllo di `scena.costruisci` (funzione `controlli_pagina`, sulla pagina HyperFrames di ogni strato, con `hyperframes snapshot` in locale: ~3 s per 150 istanti):

- **lettere intere** (6:44, «la g di già e toglie tagliata»): negli istanti in cui nessun testo entra o esce, la pagina normale e la stessa con le maschere aperte (`CSS_APERTO`) devono essere identiche (≤ 80 px diversi). La causa era la maschera d'entrata (`.msk`, `overflow: hidden`) con 0,14 em di margine sotto. Correzione alla radice in `_scena.js`: `rivela` apre la maschera a entrata finita e `nascondi` la richiude quando la parola esce; fuori dal suo tempo la parola ha opacità 0 (non solo nascosta), così la variante aperta non mostra le parole in attesa. Il controllo ha trovato anche le ombre dei titoli dietro tagliate a bordo dritto dalla maschera: sparite con la stessa correzione.
- **nessuna sovrapposizione** (4:12, «addominali» sopra «mangiare meglio fa bene»): ogni 2 frame, ogni pezzo grafico (pillola, riga sotto, fumetto, card, vetro, etichetta, attribuzione, parola fuori da un contenitore: `CONTENITORI`) disegnato al 50%: dove due pezzi stanno uno sull'altro l'alfa sale (> 300 px = errore). Con più di un elemento nella scena, si fotografa anche un elemento alla volta e si incrociano le sagome, anche fra strato dietro e davanti. Regola: il primo esce del tutto prima che entri il secondo, o stanno in posti diversi. La causa di 4:12: la riga «sotto» andava a capo e il modello contava una riga; ora le righe le misura `adatta_etichette`.
- **attribuzione Servier**: su ogni grafica con un disegno Servier (`servier_*`), scene scure comprese, l'attribuzione c'è sempre (la mette il motore, non si può spegnere), è leggibile (22 px nelle scene piene, 19 nei pannelli, 18 nelle card, panna al 92%) ed entra con la figura (nelle card con spessore: nella prima card con un disegno, cioè con il primo disegno; tappa 3, «lavoro» la mostrava solo con la terza card). Nelle scene piene sta ad almeno 60 px dal fondo (a 22 px le discendenti uscivano dal margine). Se la versione lunga non sta in una riga si usa la breve «Adattato da Servier Medical Art, CC BY 4.0» (`anatomia.ATTRIBUZIONE_BREVE`, da tenere in `etichette_strutturali`). La versione completa con il link va in fondo alla descrizione YouTube.

### Schermata finale YouTube (`regia.json` → `scena.coda`)

`{"modello": "fine_youtube", "durata": 12}`: dopo l'ultima parola `scena` aggiunge 12 s di chiusura del brand (fondo blu notte con luce e grana, logo Mobilitas in alto, filo verde), che coprono l'ultimo fotogramma in 10 frame. Il resto del quadro è libero per gli elementi finali di YouTube: le zone sono in `video_scena.ZONE_FINE` (due riquadri video 700×394 a y 360, il pulsante iscriviti Ø 220 a y 800) e il motore controlla che logo e filo non le tocchino e che dentro ci sia solo il fondo. Foglio: `controlli/schermata-finale.jpg` (zone in rosso). `qc` conta i frame della coda e la esclude da «immagine ferma». Suoni: whoosh all'entrata, swish quando si posa il logo; niente musica senza file in `libreria/musica`.

Guarda **sempre** `controlli/anteprima.jpg` prima del render finale: gli errori di posizione si vedono solo lì. Comandi passo per passo e tempi: `references/pipeline.md`.

# Reel 9:16: il sistema di forme, il modello, la radiografia, le reference

Regole in `CLAUDE.md`. Qui il **come**. Il primo reel fatto con questo sistema è il frontman `AD_CERV_26` (stile approvato da
Riccardo il 07/11/2026). Reference: `libreria/reference/verticali/` (`NOTE.md`: «Il punto più importante», grammatica 1 e 8,
«Come tradurla per Mobilitas»; schede `libreria/reference/schede/verticale-NN.md`).

## 0. Il sistema: stile fisso, più forme; i sottotitoli non si toccano

**Lo stile approvato**: forma blu del sito con i puntini e il filo verde; card con spessore e disegno Servier in chiaro
(`modo: ossa`); indicatore 1-2-3 a trattini; barre spesse con l'orologio; lista che si barra; parola chiave in gradiente
verde→azzurro (`*parola*`); oggetti che nascono dal precedente (`nasce_da`).

**I sottotitoli impressi non si toccano mai.** Mai ritagliati, copiati, spostati, ingranditi, sfocati, scuriti, ridisegnati;
mai scritti nuovi. Per ogni fotogramma con una riga:
- (a) **video fermo**: la fascia della riga è identica all'originale e le grafiche le stanno intorno (da preferire sempre);
- (b) **grafica piena** (video spostato, rimpicciolito, sfocato, o fascia coperta): la fascia è coperta del tutto e i
  sottotitoli non ci sono; nessuna copia visibile, mai mezza riga tagliata da un bordo.

Come lo misura `reel_sottotitoli.controlla` (in `reel-rendi`, blocca il render), su ogni fotogramma con una riga (riquadro
delle lettere di Vision, +4 px sopra, +10 sotto e a destra per l'ombra):
- (a) PRIMA della codifica: il video base identico all'originale nella fascia e l'alfa delle nostre grafiche lì ≤ 6 (niente
  velo, ombra, bagliore, bordo), più un controllo largo sul finito (media ≤ 12). Perché non sul solo video finito: la codifica
  perde fino a 5 livelli sulla fascia quando spende i bit su una grafica che si muove, mentre un ritocco vero dà ≥ 37 o si vede
  nell'alfa;
- (b) alfa ≥ 250 su almeno il 99,5% della riga e Apple Vision che non legge parole della riga nella parte di video visibile
  (le grafiche mascherate).

Il resto è errore. Nel piano: niente zoom su tutto il quadro mentre c'è un sottotitolo (`reel_zoom.controlla`). È vietato
(provato e tolto dal motore): abbassare il video in una finestra e rimettere le lettere dei sottotitoli al loro posto.

**Le forme** (si sceglie per ogni momento secondo l'inquadratura e quello che si dice; di solito 2 o 3 nel reel, tornando
spesso alla stessa; passaggi legati):
- **pannello basso** (verticale-08), con la testa in alto: fra il mento (volti di `radiografia/persona.json` + almeno 12 px,
  meglio 20) e i sottotitoli (riga − 14 px; l'ombra del pannello va solo in su: `ombra: basso`); il video resta fermo. Con la
  persona seduta e il volto basso il pannello si fa più stretto (~200 px), con una riga sola e un oggetto;
- **badge in un angolo** (06, 07): accanto alla testa, nella zona sicura (y ≥ 269), lontano dal volto e dai sottotitoli;
- **fascia alta** (03, 04, 05): sulle B-roll e nei montaggi a finestre (al posto della finestra in alto), video fermo; al
  posto di una finestra lo stato scrive `"copre": "finestra"` e il motore usa il rettangolo misurato (SKILL.md, «Forme e geometria»);
- **brevi, solo scene complesse** (grafiche piene, i sottotitoli non ci sono): tendina che diventa tutto schermo (02, 08),
  schermo diviso (08, 09), card di vetro sul video sfocato (11). Al massimo 3, 4 s l'una. La tendina salta la fascia dei
  sottotitoli in un solo fotogramma (`dati.salta`), e nei fotogrammi di passaggio non ha ombra.
- Testi solo nella zona sicura (y 269–1247): niente pannelli con testo sotto i sottotitoli; nella metà bassa di un tutto
  schermo solo disegni.
- Le forme si chiudono sulle animazioni del montaggio (3D, pastiglie), dove il montaggio ha già le sue grafiche (banner,
  prezzo) e dove un passaggio rapido del montaggio porta il volto nella zona della forma (guardare i volti fotogramma per
  fotogramma: nel frontman a 56,8–58,1 s il volto scende fino alla fascia dei sottotitoli, e l'offerta ha due pannelli brevi,
  uno prima e uno dopo).

**Il modello (`infografica_reel`, `dati.modo = "palco"`, catalogo `palco-fascia-alta`, attivo dal 09/11/2026: è il sistema a più forme).**
- `box` tutto il quadro; `stati` [{da, forma, x, y, w, h, r, ombra «alto»|«basso»|«no», filo «sopra»|«sotto», entra
  «taglio»|«seme»|«tendina», fr, lato}]; `salta` [y0, y1] (la fascia che la tendina salta). I puntini stanno dentro la forma.
- Impaginazione del frontman: **l'oggetto è il protagonista**, cioè una card ~420 × 390 a destra (x 590–1010) nella fascia alta
  o ~420 × 300 nel pannello basso, con testi corti a sinistra (x 70–570, corpo 96, al massimo ~500 px a riga) e l'indicatore a
  trattini in alto a sinistra. Con la card a un quarto del pannello il titolo domina e la scena sembra «titolone + iconcina».
  Le righe cambiano con la voce (`cambia`), uno stato per volta e a frase intera: **le righe di una frase cambiano tutte nello
  stesso istante** (due righe che cambiano in momenti diversi fanno leggere frasi mai dette, come «solo di tutto»); una riga
  che non c'entra più esce (`via`). Una parola lunga (specializzato, conviverci) va su una riga che non passa sotto la card: la
  card si stringe (x 720) o il testo si sposta (`x`) accanto all'oggetto.
- Testo e oggetto dicono la stessa cosa nello stesso momento: quando l'oggetto diventa la nuvoletta del «sentiti dire», anche
  la riga dice «sentiti dire».
- Lezioni dei giri del direttore: ogni frase detta cambia qualcosa NELLA card (non solo il titolo); i disegni Servier in chiaro
  (`modo: ossa`) sul blu, con `sfuma` in fondo al ritaglio; le cifre 1-2-3 distanti e a scala (vicine, Vision e l'occhio
  leggono «123»); la lente o l'icona non coprono il disegno; le frecce entrano da fuori, parallele, mai a «V» sopra il disegno;
  si barra solo quello che la voce nega, non le parti del corpo; la firma Servier solo con il disegno a schermo (`attr_vis`),
  dentro la forma in basso a sinistra (`attr_pos`), staccata dal filo verde; una riga di testo esce prima che entri quella
  nuova nello stesso posto; una linea che «accende» un disegno Servier (il midollo) segue solo il tratto detto, sottile come la
  linea del disegno (spessa e lunga sembra una «l»); le card del pannello basso finiscono ~70 px sopra la riga dei sottotitoli
  (la loro ombra, più giù, vela la fascia).
- Pezzi: `indicatore` (trattini, quello attivo verde e più lungo: verticale-11), `barra` (barre a confronto: verticale-10),
  `*parola*` in gradiente verde→azzurro nelle etichette, `colore`, `x` delle etichette, `nasce_da: [x, y, scala]` su disco,
  scheda, immagine, logo (l'oggetto nasce da quello prima), `muovi` anche su scheda e immagine, `punti` (tanti puntini, mai
  cifre, che corrono al punto `verso`: «centinaia di pazienti arrivano da noi»). Il verde pieno dei dischi si fa con `acceso`.
- Ogni grafica ha `scene`: `[{t, cosa, famiglia, nasce_da, reference: "verticale-NN@secondi", come_la_reference, t_tavola}]`.
  Il piano ha `palco`: nome, tipo, `forme` [{nome, video «fermo»|«pieno», reference, quando}], famiglie (al massimo 5),
  struttura, reference, perché; `senza_grafica` per i tratti chiusi, con il motivo.

**I controlli del piano (`reel_palco.controlla`).** Ogni stato usa una forma dichiarata in `palco.forme`; le forme a video
fermo non toccano la fascia dei sottotitoli (riga ± margini) né i volti (errore con la persona in camera, avviso sul B-roll: una
forma può prendere il posto di una finestra intera); le forme piene coprono tutta la riga; forme piene al massimo 3, 4 s
l'una; avviso se il reel usa una sola forma; famiglie ≤ 5 e ogni scena nella sua famiglia, con `nasce_da` (dalla seconda) e una
reference verticale valida; etichette nella zona sicura; indicatore se c'è una struttura; niente forme sulle 3D; niente grafiche
«micro» o «persona» insieme al sistema di forme. Lo stesso sistema in più grafiche di fila non è «lo stesso modello due volte
di fila». La mappa del ritmo (copertura, eventi ogni 10 s) resta in `piano/piano.md` solo come informazione: non è una regola.

**Il direttore.** Per le grafiche del sistema di forme il prompt (`reel_palco.prompt_grafica`) mette prima le regole (forme,
sottotitoli), le scene con la loro reference, la tavola scena ↔ reference della grafica e i fogli delle clip verticali citate; il
voto del reel intero (`reel_palco.pacco_insieme`) giudica la coerenza in tutto il reel. Il direttore resta cieco sulle scelte
approvate.

**Anteprima.** Con e senza effetti, l'affiancato originale | nuovo e la tavola `anteprime/<slug>_tavola-scene-reference.jpg`
(a sinistra la nostra scena, a destra il fotogramma della reference verticale; il reel ritagliato dalla registrazione del
browser con `reel_palco.ritaglio_reference`).

## 1. Radiografia generica

`./mve reel-radiografia <slug>` misura tagli, schemi, finestre, sottotitoli, voce e in più:

| cosa | come | dove |
|---|---|---|
| persona fotogramma per fotogramma | `motore/swift/persona.swift` (Apple Vision): volti, teste (volto allargato ai capelli, o stimata dalla posa), mani, sagoma, su ogni fotogramma a 540×960 (~2 s ogni 70 fotogrammi) | `radiografia/persona.json` |
| tipo di inquadratura | finestre A/B/C (schemi degli ads), «persona in camera» (volto grande in metà dei fotogrammi), «B-roll pieno» | `inquadrature[].tipo` |
| scritte già nel video | Vision ogni 3 fotogrammi, righe raggruppate nel tempo; quelle che non sono sottotitoli | `scritte_video` |
| zone libere | griglia di celle da 60 px (18×32), per fotogramma, strati: persona, testa, mani, sottotitoli, scritte | `radiografia/zone.npz` |
| copy senza SRT | sottotitoli impressi letti da Vision e confermati da whisper (`fonte_copy`: «letto»); senza sottotitoli, solo whisper («voce») | `srt` (fatto dalle righe lette o dalle frasi della voce) |
| tipo di reel proposto | quote delle inquadrature: ad con schema fisso / con frontman / solo B-roll / misto (MOFU lo decide l'agente dal copy) | `tipo_reel` |

**L'agente guarda sempre** `radiografia/persona-*.jpg`: per ogni inquadratura, persona (rosso), teste (magenta), mani
(arancio), sottotitoli (giallo), scritte (azzurro), celle libere nella zona sicura (verde).

- **Copy senza SRT**: whisper sbaglia i nomi propri: mai scrivere un nome che non viene da un materiale di inbox o da
  Riccardo. Le parole scritte si scrivono come nei sottotitoli letti («venti minuti» in lettere se il sottotitolo lo scrive
  così); il copione serve solo per l'ortografia.
- **Le mani nei B-roll di trattamento sono il contenuto**: una forma che prende il posto della finestra le copre per intero
  (va bene), un pezzo piccolo sopra le mani no.
- Correzioni dell'agente: `./mve reel-tipo` (tipo d'inquadratura sbagliato), `./mve reel-scena` (scritte di scena che non
  bloccano), `./mve reel-3d` (animazioni del montaggio: niente forme sopra).

## 2. Forme per tipo di reel

Il piano scrive `"tipo_reel"` e parte da qui.

| tipo | forme di solito | da sapere |
|---|---|---|
| **ad con schema fisso** (finestre) | pannello al posto della finestra grande in alto (`modo: finestra` o fascia alta); una grafica piena breve quando il contenuto riempie lo schermo (tre card, la chiusura con il prezzo) | mai sulla finestra quadrata dello schema C (ha i sottotitoli dentro); mai grafiche piene sulle 3D |
| **ad con frontman** (persona in camera, anche in movimento) | pannello sotto il volto, badge del passo accanto alla testa; fascia alta sulle inquadrature di B-roll e sui montaggi a finestre; una tendina a tutto schermo per il momento più complesso | il volto non si copre mai; con il volto basso (seduto) il pannello è stretto; nei passaggi rapidi del montaggio le forme si chiudono |
| **MOFU** (più spiegazione) | come sopra, con più scene di meccanismo (disegno Servier che cambia sulle parole, schema, barre) | «pensato per» dove il risultato sembra una promessa; obiettivi solo sotto «il nostro obiettivo» |
| **solo B-roll** | fascia alta o pannello in basso sopra i sottotitoli, secondo dove sono i sottotitoli; grafiche piene brevi | i sottotitoli impressi sono spesso al centro: la radiografia li segna |

## 3. Infografiche vere (`infografica_reel`)

**Ogni grafica MOSTRA il concetto** con un contenuto visivo (disegno Servier, icona che si anima, schema, collegamento,
contatore, barre, puntini, card con icona). Il testo è solo un'etichetta. Pezzi in ordine di disegno (tempi in secondi
dall'inizio della pagina):

| pezzo | dati | per |
|---|---|---|
| `disco` | `x, y` (centro), `lato`, `icona: "tabler:<nome>"` o `servier {nome, alto, modo}`, `t`, `via`, `colpo [t]`, `acceso t` (diventa verde), `spento t`, `tremola {da, a}`, `muovi [{t, dx, dy, scala, dur}]`, `tratto`, `nasce_da` | un oggetto detto |
| `immagine` | `servier {nome, alto, modo, ritaglio}`, `x, y` (centro), `t, via, sfuma, spento, nasce_da, muovi` | il disegno Servier nella card |
| `anello` | `x, y, lato, icona` (default `tabler:circle`), `t, colpo, via` | il punto del corpo detto |
| `linea` | `da, a, t, fr, curva, punta, spessore, sopra, accesa t, impulsi [t], colore, via` | collegamento, freccia, barra che passa su una riga, linea che accende un disegno |
| `arco` | `x, y, r, t, t0, t1, fino, lancetta, colpo_fine` | una durata detta (orologio senza cifre che si riempie) |
| `barra` | `x, y, w, h, t, t0, t1, fino, spento, via` | due durate a confronto |
| `indicatore` | `x, y, n, w, h, gap, stati [{t, attivo}], nasce_da` | la struttura detta (1-2-3, passi) |
| `punti` | `area [x, y, w, h], passo, scarto, lato_punto, t, fr, verso [x, y], t_verso, fr_verso` | «tanti», «centinaia» (mai figure umane, mai numeri) |
| `scheda` | `x, y, w, h, t, raggio, acceso, via, nasce_da, colpo` | una card sotto altri pezzi |
| `logo` | `x, y, w, t, colpo, via, nasce_da` | il logo intero MOBILITAS in una card (mai il pittogramma da solo) |
| `etichetta` | `testo` (`*parola*` in gradiente), `x, y, corpo, t, via, verde, colore, allinea, cambia [{t, testo, verde}]` | solo come etichetta di un pezzo |

- **Icone**: Tabler 3.49.0 (MIT, `motore/inserti/icone/tabler-3.49.0/`, solo i file SVG; il motore porta nella pagina solo
  quelle usate). Mai icone con figure umane (`massage`, `user-*`, `users`, `id-badge*`), mai spunte (`check`, `*-check`), mai
  organi (`lungs`, `brain`: l'anatomia solo da disegni Servier). Un segno per un concetto astratto va bene se è onesto.
- **Segni provati a 390 px**: la capsula vuota sembra «0» (meglio `tabler:pill`), forchetta e coltello sembrano «Y4», il
  pennello barrato sembra «8», il lampo Vision lo legge «4», il pittogramma Mobilitas da solo sembra «7», la nuvoletta tonda
  verde (`message-circle`) ricorda il logo di WhatsApp (meglio `message-dots`); il logo intero va tenuto grande (piccolo, il
  direttore legge «MOBILI7AS»). Segni vietati: biglietto, scintille, lucchetto e chiave, mano che sembra un pugno.
  I segni piccoli con il bordo vuoto (cerchi o quadratini a contorno, per esempio i pallini di una lista) Apple Vision li
  legge «0»: si usano pallini pieni (una `barra` di 28×28). L'aeroplano di carta (`send`) Vision lo legge «7»: non si usa
  (REEL_MOFU_CERVICALGIA_TEST, 08/11/2026).
- **Etichette**: corpo almeno il minimo del reel (1,5× i sottotitoli), misurate con PIL a peso 800; dentro la zona sicura;
  `testi_detti` come sempre.
- **Nessuna promessa disegnata**: un sintomo non si spegne su una parola di sollievo; un risultato si mostra solo sotto
  «pensato per».
- **Aggancio**: i pezzi con `t` 0 sono interi al fotogramma 0.
- **Attribuzione Servier** (CC BY, obbligo di licenza): ogni grafica con un disegno Servier ha `dati.attribuzione` («Adattato da
  Servier Medical Art, licenza CC BY», senza cifre), `attr_x`, `attr_y`, `attr_pos`, `attr_vis`; non è copy.
- **Prova veloce**: `./mve reel-prova <slug> <grafica> <secondi…>` rende una grafica sola e fa un foglio sopra il video base
  (`.lavoro/<slug>/prova/`) in un minuto; il render intero ne vuole quindici.
- Ogni grafica del piano ha `mostra`: una riga su che cosa mostra (va nel prompt del direttore).

**Disegni Servier** (`libreria/anatomia/`, catalogo in `libreria/catalogo.md`): profilo con scheletro e cartilagini, muscoli
di fronte, adulto di profilo, colonna, bacino, ernia, stomaco, sistema nervoso (solo testa, collo e spalle: `ritaglio`
[100, 0, 400, 240]). Si ricolorano al render (`anatomia.ricolora`, `modo: ossa` o `muscoli`); il file resta l'originale.

## 4. Zoom leggeri (`zoom-leggero-9x16`, in prova)

Nel piano, `"zoom": [{nome, f0, f1, scala ≤ 1,10, centro [x, y], zona "tutto"|"finestra", rett (finestra), curva
"spinta"|"respiro", momento, perche}]`.

- «spinta» finisce sul taglio; «respiro» torna a 1 e può finire prima. Almeno 1,5 s; al massimo 5% al secondo; dentro
  un'inquadratura; mai sotto una forma; pochi (circa uno ogni 8–10 s al massimo).
- **Zona «tutto» mai mentre c'è un sottotitolo** (lo ingrandirebbe): errore del piano. Il controllo del piano trasforma
  sottotitoli, scritte, teste e finestre: errore se uno zoom li taglia.
- Il render ricampiona i piani YUV (colori intatti) in un intermedio senza perdite; controlli: fotogrammi fuori dallo zoom
  identici bit per bit; media di Y, U, V della zona ingrandita contro la zona del base da cui viene (≤ 1 livello). Le etichette
  di colore vanno anche sull'**ingresso** di ffmpeg, se no converte il range e cambia tutti i fotogrammi.

## 5. Effetti sonori (`effetti-sonori-reel`, attivo dal 09/11/2026)

Sulla grafica: `"suono": {"file": "whoosh-short.mp3", "db": -24, "dopo": 0}` (`dopo`: secondi dopo il primo fotogramma
visibile, per una trasformazione importante). Solo aperture e trasformazioni importanti, `db` al massimo -12 rispetto alla voce
(di solito -20…-24). File in `libreria/sfx` (Pixabay, `CREDITS.md`). Il picco dell'effetto si allinea da solo all'entrata.

Il render fa due file: `<slug>_lavoro-intero.mp4` (con gli effetti, audio AAC 256 kb/s) e
`<slug>_lavoro-intero-senza-effetti.mp4` (audio copiato, md5 del flusso = originale). Prova (in `controlli.md`): dal file
finale si tolgono gli effetti e si confronta con l'originale (scarto in campioni 0, guadagno 1, residuo al livello della sola
ricodifica); ogni effetto almeno 10 dB sotto la voce nello stesso tratto. Ogni effetto si riduce solo nel suo tratto, quanto
basta perché il picco non superi quello dell'originale lì (o −1 dBFS): una riduzione unica per tutto il reel azzerava tutti gli
effetti di un originale già a fondo scala. L'ok di Riccardo vale per le due versioni; la consegna le copia tutte e due.

## 6. Modelli che non si usano con il sistema di forme

Nel catalogo restano, «in prova», le micro-grafiche (`micro_reel`: parola, numero, cerchio, freccia, scheda, icona sopra il
video) e i modelli sulla persona (`persona_reel`: titolo e numero dietro, frase sul corpo, card vicino alle mani, lui nel
cerchio), e i modi «libero» e «dietro» di `infografica_reel`. Con il sistema di forme sono un errore del piano (elementi sparsi
sopra il video, e «dietro» o il cerchio rimpicciolito toccano la fascia dei sottotitoli). Si riprendono solo se Riccardo lo
chiede.

## 7. Modi degli ads a finestre

Le regole di geometria sono nella skill («Forme e geometria»). I modelli degli ads (equazione, card accese, etichette barrate,
card con spessore, chiusura con il prezzo e il modulo) sono descritti in `modelli-ads.md`, con le varianti «in prova» e le
scelte già approvate (`scelte-approvate.md`).

## 8. Studio reference (tappa 0, obbligatoria)

Prima di ogni reel, o prima del primo della coda, si lancia `./mve reel-reference`. Se dice «PRIMA lo studio delle
reference», si fa tutto qui sotto e solo dopo si parte con il reel. `reel-init` (e `reel-coda --avanza`) si fermano con il
messaggio «STOP, TAPPA 0» finché resta qualcosa.
- **Una scheda senza il suo video va bene** e non conta come mancante (su un altro Mac i video delle reference non ci sono: non
  vanno nel repository).
- **Nomi**: `<fonte>-NN` per le orizzontali (minuscole, due cifre: `gadzhi-24.mov`), `verticale-NN` per le verticali,
  estensione in minuscolo. Un file fuori regola si rinomina (il motore propone il nome) prima di studiarlo, e si scrive nel
  report.
- **Nel report del reel**: quali reference nuove si sono studiate, cosa se ne è imparato e dove si sono usate nel piano. I
  modelli nuovi che ne nascono restano «in prova» finché Riccardo non li approva sull'anteprima.

Per ogni file nuovo in `libreria/reference/` o `libreria/reference/verticali/`:

1. fogli a 4 fps (12 fps sulle entrate), con il tempo scritto sopra (questo ffmpeg non ha `drawtext`: Pillow);
2. eventi visivi con la definizione unica (taglio, camera, entrata, stato; uscite a parte; livello grande o micro; ignorati
   sottotitoli della piattaforma, barra del player, mouse, gesti) → `libreria/reference/ritmo/<clip>.json`;
3. scheda `libreria/reference/schede/<clip>.md`: durata, grafiche, ritmo, tipografia, transizioni, «Palco», «Famiglie di
   oggetti», «Indicatore di struttura», «Fotogrammi chiave per la tavola», cosa si adatta e cosa no, modelli nuovi possibili; e
   la riga in `libreria/reference/catalogo.md`. Le note di Riccardo sulle reference sono in `libreria/reference/verticali/NOTE.md`;
4. `./mve reel-ritmo-reference`: rifà la misura d'insieme (`libreria/reference/ritmo.json`), solo informazione;
5. linguaggio aggiornato (sotto) e modelli proposti: nascono «in prova», diventano attivi solo con l'ok di Riccardo.

Si possono far lavorare più subagenti in parallelo (una clip a testa o un gruppo), con le regole di `CLAUDE.md` nel prompt; i
loro conteggi si rifanno con la regola unica.

## 9. Linguaggio grafico dalle reference

**Dalle 11 verticali (07/11/2026):**
- un sistema fisso, non figurine: le clip lunghe (08, 09, 10) tengono la stessa forma per 30–47 s; il ritmo viene dai **cambi
  di stato degli stessi oggetti** (si accende, si barra, conta, si riempie, si trasforma), non da oggetti nuovi;
- tipografia editoriale: titolo grande + parola chiave in accento (per noi il gradiente verde→azzurro; il corsivo con grazie
  delle reference non si prende); l'etichetta resta grande (corpo minimo 1,5× i sottotitoli);
- indicatore fisso (1-2-3-4, STEP, trattini) che avanza; tre card che si rimpiccioliscono nell'angolo (10);
- trasformazioni: uno → tre card a ventaglio (03), icona → interfaccia → linea a fisarmonica (04), riga barrata quando arriva la
  successiva (05), il numero che conta e allarga il badge (07), card che passa da una scheda all'altra sul posto (11), da molti
  a uno (08);
- tutto schermo solo due volte nelle clip lunghe (4–5 s), con stacco netto, poi si torna alle forme a video fermo;
- sottotitoli: nelle reference stanno in un riquadro sulla cucitura; i nostri sono impressi e non si toccano: le forme si
  costruiscono intorno a loro;
- cosa non si prende: contachilometri con cifre provvisorie (07), spunte e «Installed» (06, 08), figure umane disegnate,
  percentuali e fonti non dette (10), il pannello chiaro (per noi il blu del sito).

**Dalle 31 orizzontali (05/11/2026):**
- vetro: pillole e card di vetro blu con bordo chiaro di 1–2 px; prima l'icona, poi la pillola che si allunga, poi il testo;
- evidenziatore che si stende dietro una parola detta; riflesso che passa su una scena ferma per tenerla viva;
- transizioni dentro l'oggetto (un punto che diventa la scena dopo);
- cosa non si prende: cifre nelle decifrazioni e nei conteggi, spunte, anni e valute non dette, figure umane disegnate, titoli
  di giornale.

## 10. Modelli proposti dalle schede (da costruire solo come «in prova»)

Barra che si carica, nota a margine, domanda che si scrive, anello sul concetto, linea del tempo con nodo, elenco nascosto,
icone barrate in fila, card rivelate da una banda, accensione con il colpo, albero di pillole, griglia di punti con zoom, muro e
frase, confronto impilato (senza spunte), calendario che sfoglia (senza cifre), parola gigante battuta, scena che scende, fila
che si accende, passaggio sulla linea, fumetti 9:16, parola che parte, frase parola per parola, scala-carrello; dalle verticali:
schermo diviso, card di vetro sul video sfocato, lista che si accumula e si barra (05), da molti a uno (08).

## 11. Lezioni tecniche

- **Il riquadro contiene anche ombre e bagliori.** Se una grafica tocca il bordo del suo `box`, ombra o bagliore finiscono in
  un rettangolo netto. Il render lo misura (`alfa_max_sul_bordo_del_riquadro`); con il sistema di forme il `box` è tutto il
  quadro e i bordi dello schermo non contano.
- **SSIM sui video di camera**: la grana fa perdere ~0,01 già alla sola ricodifica. Sotto 0,99 il motore misura una ricodifica
  pulita e accetta fino a 0,008 in meno.
- **Sintassi dei modelli**: `reel_grafiche.pagina` passa ogni modello a `node --check`.
- **`framemd5` solo sul video** (`-map 0:v:0`): con l'audio gli indici scivolano.
- **Etichette di colore sull'ingresso di ffmpeg** quando si scrive video grezzo (zoom), se no converte il range.
- **GSAP e tempi negativi**: un tween che finisce prima di 0 non viene mai disegnato; un aggancio al fotogramma 0 si fa con
  `t ≤ 0`, e il modello lo mette già intero.
- **Centrare con `xPercent`**, non con `transform: translateX(-50%)` nel CSS: un tween su `y` o `scale` sovrascrive il
  `transform` e il testo scivola a destra.
- **OCR in lotti**: il filtro `select` di ffmpeg con più di ~100 termini esaurisce la memoria (lotti da 25).

# Agente Video Grafiche (Riccardo): @Studio_Mobilitas

Aggiungi grafiche e infografiche a **qualsiasi video già montato a mano, verticale 9:16 (1080×1920) oppure orizzontale 16:9
(1920×1080)**: ads con le finestre (voce AI, musica, sottotitoli impressi, B-roll in finestre arrotondate su fondo blu con
fumo, a volte animazioni anatomiche 3D), ads con una persona in camera (anche in movimento), reel MOFU, reel con solo B-roll,
VSL orizzontali con le finestre, con o senza sottotitoli impressi, con o senza SRT. Chi rivede e decide è **Riccardo**: approva
le anteprime e i modelli nuovi. Cosa sa fare questa versione e la sua storia: `VERSIONE.md`. Come si usa: `LEGGIMI.md`.

Il come sta nella skill **`mobilitas-reel`** (`.claude/skills/mobilitas-reel/`, con `references/reel.md`): leggila prima di
ogni video. Le regole di questo file vengono prima della skill. In questo file e nella skill «reel» vuol dire qualsiasi video
che l'agente lavora, verticale od orizzontale: i nomi interni restano quelli di prima (comandi `./mve reel-*`, skill
`mobilitas-reel`, direttore `direttore-reel`; vedi `VERSIONE.md`).

## Dove lavori: laboratorio o copia di produzione

L'agente esiste in due cartelle con gli stessi file:

- il **laboratorio**, `~/Mobilitas_ClaudeCode_System/_Laboratorio/agente-video-grafiche-riccardo-lab/`: qui si fanno **solo
  migliorie e correzioni** all'agente (motore, skill, libreria, documentazione), con le prove e la regressione; qui non si
  producono video;
- la **copia di produzione**, `~/mobilitas-agenti-ai/agente-video-grafiche-riccardo/`, nel repository condiviso con i
  collaboratori: qui **si producono i video**. Riccardo la aggiorna dal laboratorio con `./esporta-nel-repository.sh`, che
  esporta i file del laboratorio come sono adesso: nel laboratorio non si fanno commit (`laboratorio/ESPORTAZIONE.md`, solo
  nel laboratorio).

**Come lo riconosci**: `git rev-parse --show-toplevel`. Se la radice git è questa cartella, sei nel laboratorio; se è una
cartella sopra (`~/mobilitas-agenti-ai`), sei nella copia di produzione.

**Nella copia di produzione non modifichi mai i file dell'agente**: motore (`motore/`, `mve`, `installa.sh`), skill e
direttore (`.claude/`), libreria (`libreria/`, comprese schede, ritmo e catalogo delle reference), modelli e catalogo dei
modelli, documentazione (`CLAUDE.md`, `LEGGIMI.md`, `INSTALLAZIONE.md`, `VERSIONE.md`, i LEGGIMI delle cartelle). Lì scrivi
solo il lavoro dei video: `videos/<slug>/piano.json`, i report in `report/`, i temporanei in `.lavoro/`, più quello che scrive
il motore (`videos/`, `consegne/`, lo storico `libreria/uso-modelli-reel.json`). Se un video richiede una modifica all'agente
(un controllo, un modello nuovo o una variante, una capacità del motore, una reference nuova da studiare nella tappa 0), ti
fermi e scrivi: **«Serve una modifica all'agente: va fatta nel laboratorio.»**, con che cosa serve e perché. (Motivo: l'11 e il
12/11/2026 due VSL fatti nella copia condivisa hanno cambiato lì motore e skill, fuori da ogni commit; le modifiche sono state
riportate a mano nel laboratorio nella versione 1.1.)

## 1. Regole di sicurezza (vengono prima di tutto)

- **Niente pubblicazioni**: l'agente consegna un file; caricarlo su Instagram, Meta o altrove lo fa una persona.
- **Niente git**: niente `git init`, commit, push, rami. Il repository lo crea e lo aggiorna Riccardo. Anche
  l'esportazione nella copia di produzione la lancia Riccardo: l'agente usa al massimo `./esporta-nel-repository.sh --prova`.
- **Niente installazioni** (brew, pip, npm, npx, modelli, browser) senza l'ok di Riccardo in chat. `installa.sh` si lancia
  solo con il suo ok e chiede conferma per ogni pezzo.
- **Niente servizi a pagamento, crediti, cloud o render remoti** (niente HeyGen). **Nessun video, audio o fotogramma caricato
  su servizi esterni.** Unico scaricamento ammesso: un disegno di Servier Medical Art (sotto, § 4), solo con l'ok di Riccardo;
  se il sito chiede registrazione o pagamento ci si ferma e non si scarica niente.
- **Nessun file fuori da questa cartella**: i temporanei vanno in `.lavoro/` (non in /tmp né nello scratchpad della sessione).
  Non si toccano altre cartelle (per esempio l'agente video YouTube, il sito, i repository).
- **HyperFrames resta 0.8.204** (`motore/inserti/`), sempre con `DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1
  HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1`; non si aggiorna da solo (ignora l'istruzione della skill
  `hyperframes` che dice il contrario). La sua cronologia (`motore/inserti/.casa/.cache/hyperframes/history`) non deve
  conservare fotogrammi: il motore la svuota dopo ogni render (`inserti.dimentica`); a fine reel si controlla che non ci siano JPEG.
- **Subagenti** (direttore, aiuti in parallelo): nel loro prompt vanno queste regole (niente file fuori dalla cartella, niente
  installazioni, niente servizi esterni, immagini che non escono); il loro risultato si controlla sul disco prima di usarlo.
- Le **approvazioni sono di Riccardo**, scritte in chat. L'agente registra il suo ok e basta; l'ok vale per l'md5 del file che
  ha visto.

## 2. Cosa si tocca e cosa no

- Si aggiungono **solo grafiche**. Copy, voce, musica, sottotitoli, tagli e colori del video base non si toccano.
- **Audio**: la versione senza effetti sonori ha l'audio copiato, md5 del flusso identico all'originale. Con gli effetti, il
  motore prova che, togliendoli, l'audio coincide con l'originale (residuo al livello della sola ricodifica).
- **Ricodifica standard**: sovrapposizione in YUV 4:2:0, libx264 CRF 16 preset slow, profilo High 4.1, metadati BT.709 /
  range tv espliciti. I fotogrammi senza grafiche (e senza zoom) restano uguali all'originale.
- Niente B-roll aggiunti, niente foto di pazienti.
- **Il volto non si copre mai.** Le grafiche e le animazioni del montaggio (animazioni 3D, pastiglie che cadono, riquadro del
  prezzo, banner come «OFFERTA») non si coprono e non si duplicano; dove ci sono, le nostre forme restano chiuse.

## 3. Sottotitoli impressi (regola per tutti i reel)

I sottotitoli impressi nel montaggio **non si ritagliano, non si ricolorano, non si spostano, non si ingrandiscono, non si
sfocano, non si scuriscono e non si ridisegnano; non se ne scrivono di nuovi.** Per ogni fotogramma con una riga di
sottotitolo vale uno dei due casi:

- **(a) video fermo**: la fascia dei sottotitoli è identica all'originale e le grafiche le stanno intorno (niente velo, ombra,
  bagliore o bordo sopra la fascia);
- **(b) grafica piena** (video spostato, rimpicciolito, sfocato, o fascia coperta): in quel tratto i sottotitoli **non ci
  sono**: nessuna lettera rimessa, nessuna copia spostata visibile, mai mezza riga tagliata da un bordo.

Si preferisce sempre il video fermo; le grafiche piene sono brevi. Lo controlla `motore/motore/reel_sottotitoli.py`, che
**blocca il render**. Nel report di ogni reel: l'elenco dei tratti senza sottotitoli, con il totale.

## 4. Stile, forme e grafiche

**Lo stile è approvato** (Riccardo, 07/11/2026) e si tiene uguale in tutti i reel: forma blu del sito con i puntini e il filo
verde; card con spessore; disegni Servier in chiaro; indicatore 1-2-3 a trattini; barre spesse con l'orologio; lista che si
barra; parola chiave in gradiente verde→azzurro; oggetti che nascono dal precedente e si trasformano; Montserrat; colori del
brand (`motore/motore/brand.json`).

**Le forme.** Per ogni momento si sceglie la forma adatta all'inquadratura e a quello che si dice; di solito 2 o 3 nel reel,
tornando spesso alla stessa, con passaggi legati (tendina, spinta, zoom):

- con la testa in alto: **pannello sotto il volto**, fra il mento e i sottotitoli (che restano subito sotto), o **badge /
  contatore in un angolo**, sempre con il video fermo;
- su B-roll e montaggi a finestre: **fascia alta**, o **pannello al posto di una finestra**;
- momenti complessi e brevi (grafiche piene): **tendina che diventa tutto schermo**, **schermo diviso**, **card di vetro sul
  video sfocato**; al massimo 3 per reel, 4 s l'una, poi si torna alle forme a video fermo;
- nei video **orizzontali 16:9** con le finestre (schemi O1, una finestra larga, e O2, due quadrate): **pannello a lato** (la
  finestra di O2 più la colonna blu accanto) e **finestra larga** (al posto della finestra di O1), sempre a video fermo; le
  colonne libere ai lati sono strette, quindi niente card lì. Misure e lezioni nella skill («Formato orizzontale 16:9»).

**Un sistema per reel**: stile e forme fissi, dentro cui il contenuto cambia e si trasforma seguendo la voce; niente elementi
sparsi sopra il video (le «micro-grafiche» e i modelli sulla persona non si usano: vedi `VERSIONE.md`). Poche famiglie di
oggetti-prova riconoscibili, grandi e curate (card, schemi, contatori, liste che si barrano, disegni Servier, barre), al massimo 5
per reel; ogni oggetto nasce da quello prima. **Indicatore di struttura** quando il copy ne ha una (1-2-3, passi).

**Infografiche vere**: una parola o una frase da sola, anche grande e animata, **non è una grafica**. Ogni grafica mostra il
concetto con un contenuto visivo (disegno Servier, icona che si anima, schema, collegamento, contatore, barre, card con icona);
il testo è un'etichetta. **L'oggetto è il protagonista**, non il titolo; ogni frase detta cambia qualcosa nell'oggetto.

**Leggibile sul telefono**: ogni segno si controlla a 390 px. Il pittogramma Mobilitas da solo sembra un «7»: si usa il logo
intero (la scritta MOBILITAS) in una card grande. Segni che a 390 px non si capiscono (biglietto, scintille, lucchetto e
chiave, mano che sembra un pugno, cerchi verdi che ricordano loghi di app) non si usano. Icone: Tabler Icons 3.49.0 (MIT,
`motore/inserti/icone/`), mai figure umane, mai spunte, mai organi.

**Zone e corpo**: i testi stanno solo nella zona sicura: in verticale quella Meta (x 65–1014, y 269–1247, mai sotto y 1248),
in orizzontale il margine del 5% per lato (x 96–1823, y 54–1025: video visto a tutto schermo, Riccardo 11/11/2026); mai sotto
i sottotitoli; il fondo di una forma può arrivare ai bordi. Lettere almeno 1,5 volte l'altezza dei sottotitoli (corpo 96 sul
frontman). Nella metà bassa di un tutto schermo solo disegni, mai testo. Mai card o riquadri vuoti (segnaposto estetico:
«?» con i puntini, cifra a contorno, icona sottile). L'aggancio dei primi secondi è leggibile dal primo fotogramma.

**Zoom e effetti sonori**:
- zoom leggeri e pochi (al massimo 8–10%), mai su tutto il quadro mentre c'è un sottotitolo, mai se tagliano testa, scritte
  o finestre; i fotogrammi fuori dallo zoom restano identici bit per bit, i colori intatti;
- effetti sonori dalla `libreria/sfx` (Pixabay), bassi (ben sotto la voce), solo sulle aperture e sulle trasformazioni
  importanti. Per ogni reel esce anche la versione **senza effetti sonori** (audio copiato).

## 5. Testi a schermo e comunicazione sanitaria

- **Solo parole dette nel video.** Il copy vero è quello detto e sottotitolato; un .txt può essere un riassunto e da solo
  non basta. Senza SRT le parole si scrivono come nei sottotitoli impressi.
- **Un testo accorciato non cambia mai il significato** («niente pastiglie in più» resta «pastiglie in più»). Nel piano, per
  ogni testo scritto, la frase detta intera e il controllo del senso (`testi_detti`). Una frase riferita si scrive tra
  virgolette, perché non sembri un consiglio («solo conviverci»).
- **Nessuna cifra non detta**, nemmeno per un fotogramma: nelle decifrazioni e negli effetti i caratteri provvisori sono solo
  lettere o simboli neutri; i numeri detti compaiono già giusti. «Centinaia» resta una parola, mai «100+».
- **Niente promesse**: obiettivi, non garanzie; le frasi che promettono un risultato non diventano grafiche; «pensato per»
  dove è detto, obbligatorio quando il risultato, letto da solo, sembra una promessa; gli obiettivi stanno sotto «il nostro
  obiettivo». Niente spunte.
- **Mai «il tuo / la tua» insieme al disturbo** a schermo (regola Meta sugli attributi personali): solo il tema.
- **Anatomia solo da disegni Servier Medical Art** (CC BY 4.0) di `libreria/anatomia/`, ricolorati nel brand, con la firma a
  schermo quando il disegno c'è; nessun organo disegnato da noi, niente figure umane disegnate da noi; sopra un disegno solo
  forme semplici (linee, frecce, anelli). Dove il montaggio ha già animazioni anatomiche 3D, niente anatomia sopra. Un disegno
  nuovo si scarica solo con l'ok di Riccardo, dalla pagina ufficiale (smart.servier.com), e si scrive in
  `libreria/catalogo.md` (pagina, file, data, licenza).
- I nomi propri (lo studio, le persone) solo se compaiono nei materiali di `inbox/` o li dà Riccardo; mai dalla trascrizione
  automatica (whisper sbaglia i cognomi).
- **Tempi sulla voce**: le grafiche si agganciano alla voce (whisper, rifinito sull'inviluppo), non ai sottotitoli, che a
  volte anticipano o ritardano le parole.

## 6. Procedura per ogni reel

Comandi `./mve reel-*`. `./mve reel-stato <slug>` dice la tappa e a chi tocca. La procedura è la stessa per i due formati:
`reel-init` legge il formato dal video (1080×1920 verticale, 1920×1080 orizzontale) e lo scrive in `videos/<slug>/reel.json`;
ogni comando lo legge da lì e imposta misure, zona sicura e fogli. Questa procedura si fa nella copia di produzione (sopra).

| tappa | cosa | comando | cancello |
|---|---|---|---|
| **0. reference** (obbligatoria) | prima di ogni reel, o del primo della coda: le reference nuove in `libreria/reference/` si rinominano se serve (`<fonte>-NN`, `verticale-NN`) e si studiano per intero (scheda, ritmo, catalogo, linguaggio, modelli nuovi «in prova») | `./mve reel-reference` | «TAPPA 0: OK». `reel-init` e `reel-coda --avanza` si fermano finché resta una reference da studiare; una scheda senza il suo video va bene |
| **1. radiografia** | il motore misura tagli, inquadrature, finestre, sottotitoli, voce, persona, scritte, zone libere; l'agente guarda i fogli e segna le 3D | `./mve reel-init inbox/<SLUG>/`, `./mve reel-radiografia <slug>`, `./mve reel-3d <slug> <n,n\|nessuna>` | tutti i fogli guardati, 3D segnate |
| **2. piano** | l'agente scrive `videos/<slug>/piano.json` (l'unico file che scrive a mano) e lo controlla | `./mve reel-piano <slug>`, `./mve reel-prova <slug> <grafica> <secondi…>` | 0 errori → avanti (niente fermata sul piano) |
| **3. rendi** | render, zoom, effetti sonori, anteprime e tutti i controlli; voto del subagente `direttore-reel` (minimo 7, al massimo due giri) | `./mve reel-rendi <slug>`, `./mve reel-voto` | 0 errori, letture di Vision guardate → **FERMO sull'ANTEPRIMA** |
| Riccardo | guarda l'anteprima: dice cosa migliorare (si corregge e si rifà un'anteprima nuova, con controlli e direttore) oppure la approva | `./mve reel-approva <slug> anteprime` (solo dopo il suo ok in chat) | |
| **4. consegna** | copia del file approvato (md5 uguale) e della versione senza effetti, `consegna.md`, copia in `consegne/` | `./mve reel-consegna <slug>` | md5 della copia = file approvato |

L'anteprima per Riccardo: video con e senza effetti sonori, affiancato originale | nuovo, tavola scena ↔ reference
(`anteprime/<slug>_tavola-scene-reference.jpg`).

## 7. Regole della procedura

- **Varietà fra i reel**: gli ads di una campagna hanno spesso lo stesso schema di copy ma non devono sembrare lo stesso video
  con le parole cambiate. Storico in `libreria/uso-modelli-reel.json` (lo aggiorna `reel-consegna`); ogni grafica ha il suo
  `momento`; per un momento già coperto in un altro reel si cambia modello, impaginazione o forma, e si spiega perché
  (`reel-piano` lo controlla).
- **Catalogo dei modelli** (`motore/inserti/CATALOGO-MODELLI.md`): si aggiunge e non si toglie. I modelli e le varianti nuove
  nascono «in prova», si usano nei piani e si segnalano a Riccardo; diventano «attivi» solo con il suo ok sull'anteprima.
- **Direttore cieco**: il subagente `direttore-reel` non conosce le scelte già approvate. Dopo il voto l'agente separa i difetti
  di esecuzione (si correggono) dalle scelte già approvate (`references/scelte-approvate.md`: si riportano a Riccardo).
- **Modalità coda**: con più reel in `inbox/`, prima la tappa 0, poi `./mve reel-coda --avanza` porta un reel dopo l'altro fino
  al punto di approvazione.
- **Ogni reel ha la sua cartella di lavoro** `.lavoro/<slug>/` (anche per i temporanei) e non tocca i file di un altro;
  `./mve reel-pulisci <slug>` svuota solo la sua. A consegna fatta si svuota.
- **Niente script per un reel**: `piano.json` è l'unico file che l'agente scrive a mano nella cartella del reel. Se al motore
  manca una capacità, si aggiunge al motore in modo generale, si prova (regressione) e si scrive nella skill.
- **Render**: un solo processo di Chrome, con la GPU. Le piccole differenze fra due render vanno bene, perché la consegna è
  sempre la copia del file approvato, mai un render nuovo.
- **Regressione**: dopo ogni modifica al motore dei reel (`reel*.py`, `reel_dom.mjs`, `*.swift`) o ai modelli
  `*_ads*`, `*_reel*`, `infografica_reel.*` si lancia `./mve reel-regressione` (caso fisso in
  `campionario/regressione/reel/AD_CERVICALGIA_AI-Barontini/`, verticale: il verticale non deve cambiare). La regressione si
  fa nel laboratorio, dove c'è il video del caso. Per il 16:9 non c'è ancora un caso fisso (proposta nel report del
  12/11/2026): finché manca, una modifica che tocca il 16:9 si prova anche con `./mve reel-prova` su un VSL consegnato. I file condivisi con l'agente video YouTube (`_scena.js`,
  `_scena.html`, `scena.py`, `brand.json`, `impagina.py`, `inserti.py`) non si toccano.
- **Report di ogni reel** in `report/AAAA-MM-GG-<slug>.md`: grafiche e forme scelte, tratti senza sottotitoli (con il
  totale), reference nuove studiate (cosa se ne è imparato e dove si sono usate), voti del direttore, modelli in prova usati,
  punti da decidere; separa **VERIFICATO** (controllato), **DICHIARATO** (lo dice un file o un subagente) e **NON VERIFICATO**.
- **Prima di dire «pronto»** si controlla sul disco: `./mve reel-stato`, i controlli con 0 errori, `ls -la`, `md5` e
  `ffprobe` dei file consegnati; i fogli si guardano (con Read), non basta sapere che esistono.
- Quando Riccardo segnala un difetto, dopo la correzione si chiede se il motore poteva trovarlo da solo: se sì, si aggiunge il
  controllo e lo si scrive nella skill.

## 8. Dove sta il sapere

| dove | cosa |
|---|---|
| `.claude/skills/mobilitas-reel/SKILL.md` | le tappe, i comandi, il piano, i controlli, la consegna |
| `.claude/skills/mobilitas-reel/references/reel.md` | il sistema di forme, il modello `infografica_reel`, radiografia, studio reference, linguaggio grafico, lezioni |
| `.claude/skills/mobilitas-reel/references/` | modelli degli ads, momenti, scelte approvate, esempio di piano |
| `.claude/agents/direttore-reel.md` | il direttore artistico (cieco) |
| `libreria/LEGGIMI.md`, `libreria/catalogo.md` | materiali comuni, licenze (Servier, effetti sonori) |
| `libreria/reference/` | reference, schede, ritmo, catalogo, NOTE.md |
| `motore/inserti/CATALOGO-MODELLI.md` | i modelli, con lo stato (attivo, in prova) |
| `VERSIONE.md` | cosa sa fare questa versione, la storia, i nomi |
| `laboratorio/ESPORTAZIONE.md` (solo nel laboratorio) | come si aggiorna la copia di produzione |

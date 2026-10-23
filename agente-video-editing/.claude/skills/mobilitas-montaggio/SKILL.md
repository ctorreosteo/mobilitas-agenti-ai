---
name: mobilitas-montaggio
description: Il motore di montaggio dei video @Studio_Mobilitas (./mve), dal .MOV di camera al montato pulito — colore HLG->BT.709 senza zscale, trascrizione a blocchi, i nove segnali del cacciatore di papere, EDL sulla griglia dei frame, punti di taglio sul fondo di sala, ascolto delle giunte, inquadrature dinamiche dal 4K con il volto di Apple Vision, audio a -14 LUFS. Usala per qualsiasi montaggio del canale, prima di toccare ffmpeg o il motore.
---

# mobilitas-montaggio

Il girato del canale arriva come ripresa unica: la presentatrice si ferma, si corregge a voce ("ho sbagliato", "torna su un pochettino") e rifà la battuta. Montare vuol dire soprattutto **trovare e togliere quei punti**, e la parte difficile è trovarli, non tagliarli.

Tutto passa da `./mve <fase> <slug>`. Il codice sta in `motore/motore/`; un modulo per fase, con il perché scritto in testa al file.

## Sorgente e colore (`init`, `prep`)

Attese dalla camera: 3840x2160 HEVC Main10 a 59.94, HLG BT.2020 con RPU Dolby Vision, `rotation: -180`, audio molto basso (−26/−29 LUFS con picchi oltre 0 dBFS). `init` collega il file (non lo sposta) e scrive `meta.json`; `prep` estrae tre audio (analisi, riconoscimento normalizzato a −20, master 48k/24 bit) e mappa i blocchi di parlato.

`ffmpeg` di Homebrew **non ha `zscale` né `libplacebo`** e `colorspace` non conosce l'HLG: la conversione è un LUT 3D precalcolato una volta sola (`motore/colore.py`, in `.cache/`). In coda alla catena serve `setparams=…bt709`: i flag `-color_*` da soli lasciano il file taggato `arib-std-b67`. Il QC lo controlla.

Il 59.94 si decima 2:1 esatto con `fps=30000/1001`: nessun judder.

## Trascrivere (`trascrivi`)

Tre trascrizioni, per tre usi:

| file | come | serve a |
|---|---|---|
| `parole-sorgente.json` | intera, DTW | confronto (segnale "appianata") |
| `parole-finestre.json` | finestre 26 s ogni 20 s | ripetizioni, regia |
| `blocchi-testo.json` → `trascrizione.txt` | **ogni blocco di parlato da solo** | leggere, decidere, ancorare i tagli |

**Whisper appiana le riprese doppie** quando vede le due prese insieme: su file intero, e anche su finestre da 9-14 s, scrive una frase corretta mai pronunciata. Trascritto blocco per blocco (fra due pause misurate) non può farlo. I blocchi hanno inizio e fine misurati sull'inviluppo, quindi sono anche i punti a cui ancorare i tagli.

Flag che contano: `-mc 0` (senza, degenera in loop), `-dtw large.v3`, `-ml 1 -sow`. Su clip brevissime whisper scrive "Grazie." sui rumori: il motore li filtra.

## Volti (`volti`)

`motore/swift/visione.swift` (Apple Vision, compilato al primo uso) traccia il volto ogni 0,5 s: riquadro, qualità dello scatto, orientamento, apertura degli occhi. 20 minuti in 45 s. Serve a centrare le inquadrature, a mettere le card dalla parte libera e a scegliere le miniature.

È anche il **controllo terzi**: un secondo volto che resta in scena per almeno 1,5 s è STOP. I campioni isolati (in YT_TOFU_02: le mani giunte, due volte) vengono elencati come avviso: guardali comunque.

## Trovare le papere (`papere`)

Nove segnali indipendenti (dettaglio in `references/papere.md`):

1. sonda delle pause (PRIMA/DOPO trascritti da soli)
2. parole di regia
3. a-parte (blocco breve isolato)
4. ripetizioni (4-grammi entro 90 s)
5. appianamento (parole che solo le finestre hanno)
6. copione (se c'è `copione.md`)
7. **blocco contro blocco**: un blocco che ricomincia come uno dei due precedenti
8. parola troncata e attacco monco ("Si par…" / "si parte")
9. interiezione o coda spuria isolata ("no", "qua", un "di")

Banco di prova: YT_TOFU_02, 13 papere trovate a mano nella v1 più 5 che la v1 aveva consegnato senza vederle. Il cacciatore v2 le trova **tutte e 18** in automatico; restano 3 falsi allarmi forti, tutti ripetizioni retoriche, che l'agente scarta leggendo.

## Punti di taglio (`edl`)

**Non si taglia sul confine del blocco**: la coda della sillaba scende per 100-200 ms restando udibile ("toracica" troncata nella v1). L'ancoraggio di regia si aggancia al confine di blocco più vicino, poi si cerca il primo istante a fondo di sala (+10 dB, inviluppo 5 ms con media a 30 ms) e infine il campione più silenzioso entro ±60 ms. Dentro una pausa ci può essere un colpo sul tavolo (−37 dB a 3:24 di YT_TOFU_02): la rifinitura lo evita.

Ogni segmento si **quantizza sulla griglia dei frame**: inizio su un frame sorgente, durata in frame interi d'uscita. Audio e video durano uguale al campione e 46 giunte non accumulano deriva. Il QC controlla che i frame del file consegnato siano esattamente quelli dell'EDL.

Energia residua a ogni giunta: oltre `fondo + 14 dB` è "da ascoltare", oltre `fondo + 24 dB` è "dentro una parola" e la fase si ferma.

Ritmo: le pause sopra `pausa_max` si accorciano a `resta` (profili in `mobilitas-regia`).

## Ascoltare le giunte (`audio`)

`audio` monta solo la voce (catena sotto), la trascrive in tempo montato e ascolta ogni giunta **due volte**: 12 s attorno, e 4 s prima + 4 s dopo trascritti separatamente e confrontati (`riattacco`, ripetizioni, troncamenti). La finestra lunga da sola non basta: appiana. Esce `controlli/giunte.md`. Si fa **prima** del render video: un errore costa 2 minuti invece di 15.

Le parole del montato (per i sottotitoli) si trascrivono a pezzi da 10 s costruiti dai blocchi della sorgente: il DTW su file intero perde la prima parola di molte frasi ("tuo cervello consuma"), e i blocchi ricalcolati sull'audio montato si spezzano sugli attacchi deboli perché lì il fondo di sala è 30 dB più alto.

## Audio

Catena voce (`audio.CATENA_VOCE`): passa-alto 75 Hz, `afftdn`, EQ (−1,5 dB a 220 Hz, +1,5 dB a 3,2 kHz), de-esser, compressione 2,5:1, `loudnorm=I=-14:TP=-1.5:LRA=9`, limiter. La riduzione di rumore viene **prima** della normalizzazione: alzare di 15 dB alza anche il fondo. Ogni segmento ha una dissolvenza di 10 ms ai bordi: su fondo di sala non si sente, e toglie i click.

Il mix finale (voce + sound design + musica opzionale) si riporta a −14 con un guadagno lineare, non con un secondo `loudnorm`, e un limiter a −2,2 dBFS di campione (il true peak sfora il campione di circa mezzo dB).

## Inquadrature (`inquadra`, `monta`)

Dal 4K si ricavano tre tagli senza perdita: largo (1,0), medio (1,28), stretto (1,62), più varianti (1,12 / 1,42 / 1,80) per quando due pezzi forzati allo stesso taglio si toccano su una giunta. Ogni ritaglio è centrato sul volto mediano del pezzo. La grammatica è in testa a `inquadra.py`: cambio di taglio a ogni giunta, largo per card e apertura, largo per i titoli dietro, stretto sulle enfasi, altrimenti alternanza largo/medio circa ogni 9 s su una pausa fra due frasi.

**Lo stacco con cambio di taglio sostituisce la dissolvenza della v1.** Sulla macchina fissa la dissolvenza di 5 frame si leggeva come un salto morbido; lo stacco fra due tagli diversi non si vede.

`monta` renderizza ogni pezzo da solo dal 4K (videotoolbox in decodifica, crop, lanczos, LUT, x264 CRF 14), due alla volta, con cache sul contenuto, e li concatena senza ricodifica. 13 minuti in 6 minuti. `--solo 3,7` rifà solo quei pezzi. Esce anche `controlli/inquadrature.jpg`, un fotogramma per pezzo.

## Verifica (sul file consegnato)

`qc` controlla il master, non i dati: codec, tag colore, frame contro EDL, durata audio, loudness, true peak, frame neri, immagine ferma, card sul volto, sagome, copertura dei sottotitoli, e **riascolta tutte le giunte sul file finale** con sonde da 4 s. Esce `controlli/QC.md` con CONSEGNABILE o NON CONSEGNABILE.

## Ambiente

Cosa c'è e cosa manca su questa macchina: `references/ambiente.md`.

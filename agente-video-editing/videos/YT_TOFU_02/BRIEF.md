---
progetto: YT_TOFU_02
canale: youtube.com/@Studio_Mobilitas
lingua: it
girato: videos/YT_TOFU_02/YT_TOFU_02.MOV
consegna: renders/YT_TOFU_02_FINAL_1080p.mp4 — 1920x1080 @ 29.97p, sottotitoli e grafica impressi
durata_sorgente: 19m44s
durata_montata: 13m40s
tipo: talking-head TOFU, divulgazione osteopatica
---

## Messaggio

Il calo delle tre del pomeriggio non e metabolico ne mentale: e meccanico. Ore
di postura seduta comprimono il diaframma, la respirazione diventa alta e corta,
e il cervello — che si prende il 20% dell'ossigeno — smette di riceverne
abbastanza. Il caffe non risolve, maschera, e peggiora la meccanica. Chiusura su
iscrizione e aggancio al video successivo (ansia = respirazione).

Frase chiave: **"Il tuo cervello non si stanca, soffoca."**

## Consegne

| file | cosa |
|---|---|
| `renders/YT_TOFU_02_FINAL_1080p.mp4` | **il video da pubblicare**: montato, gradato, con sottotitoli karaoke e infografiche impressi |
| `renders/YT_TOFU_02_cut_clean.mp4` | lo stesso montaggio senza grafica, per rifare il pacchetto grafico da capo |
| `renders/YT_TOFU_02.srt` | sottotitoli a corredo, per la traccia YouTube |
| `renders/YT_TOFU_02_capitoli.txt` | capitoli da incollare in descrizione |

## Sorgente

- 3840x2160, HEVC Main10, 59.94p, HLG BT.2020 con RPU Dolby Vision profilo 8.4
- `rotation: -180` nei metadati (ffmpeg la applica in decodifica)
- audio AAC 48 kHz stereo, **-29,5 LUFS integrati con true peak a +1,8 dBFS**
- 9,0 GB, una sola ripresa continua con le papere dentro

## Lavorazione

Le scelte tecniche ricorrenti sono ora codificate nelle skill di progetto
`.claude/skills/mobilitas-style`, `mobilitas-montaggio`, `mobilitas-grafica`.
Qui resta solo cio che e specifico di questo video.

### Colore

HLG BT.2020 -> SDR BT.709 con LUT 3D a 65 nodi (`scripts/make_hlg_lut.py`),
perche questo ffmpeg non ha `zscale` ne `libplacebo` e il filtro `colorspace`
non conosce `arib-std-b67`. Nessuna correzione creativa sopra: la luce di studio
e piatta e uniforme.

### Formato

4K60 -> 1080p29.97, decimazione 2:1 esatta senza judder.

### Montaggio — `data/edl.json`

13 tagli di papere e riprese doppie (**-4m56s**) piu 20 pause oltre 1,8s
accorciate (**-1m03s**). Giunte a dissolvenza di 5 frame, 31 in tutto.

| sorgente | durata | cosa |
|---|---|---|
| 00:00 - 00:12 | 12,9s | "buongiorno a tutti", ciak "1 2 3 4 3 2 1, tofu 2" |
| 01:52 - 02:24 | 31,2s | prima ripresa di "Non sei pigro e non e il pranzo" + correzione |
| 03:54 - 04:03 | 9,5s | falso attacco "Il calo delle tre e meccanico, non meccanico" |
| 05:19 - 05:46 | 27,1s | falsa partenza "Ecco cosa succede" + "ho sbagliato, torna su" |
| 06:59 - 07:07 | 7,7s | falsa partenza "Studi sulla meccanica" + "l'ho detto male, aspetta" |
| 07:54 - 08:39 | 44,9s | "Adesso pensa..." interrotto, "no ho sbagliato" e lo scambio con la regia ("stoppa allora li", "vai ragazzi") |
| 10:35 - 11:24 | 49,6s | papera lunga: "dai invece ho sbagliato / parto da / scusami" |
| 12:14 - 12:27 | 12,5s | vuoto + regia a voce "il titolo e postura accumulata non disciplina" |
| 13:24 - 13:30 | 6,3s | prima ripresa incompleta "un problema di postura" |
| 13:39 - 14:00 | 21,1s | falsa partenza "in modo significativo" (voleva dire sintomatico) + "aspetta" |
| 15:11 - 15:15 | 4,5s | ripetizione "si lavora sulla mobilita delle prime coste" |
| 17:36 - 18:22 | 46,2s | "nel prossimo video" interrotto + regia "torna su, e troppo lungo il periodo" |
| 19:21 - fine | 22,8s | "mi sa che abbiamo finito, c'e il conteggio parole" + "naif" + coda muta |

Delle due riprese di ogni battuta si tiene quella buona indicata dalla
presentatrice. Nel caso del caffe (07:54) si tiene la **prima** lettura di
"Il caffe non risolve, maschera" e si scarta la serie di ritentativi che segue.

Una sola cosa e stata tenuta pur essendo al confine: **"Postura accumulata, non
disciplina."** — la presentatrice prima la annuncia ("il titolo e...") e poi la
recita; la seconda regge come stacco di capitolo, l'annuncio e stato tolto.

### Audio

Passa-alto 75 Hz, riduzione di rumore FFT, de-esser, compressione 2,5:1,
`loudnorm` a **-14 LUFS / -1,5 dBTP**, limiter. La riduzione di rumore viene
prima della normalizzazione perche alzare di 15 dB alza anche il fondo.

### Grafica impressa

Renderer Pillow che scrive RGBA grezzo nella pipe di ffmpeg
(`scripts/render_overlay.py`): questo ffmpeg non ha ne `libass` ne `drawtext`.

- **sottotitoli karaoke** — 759 gruppi da 2-3 parole, parola attiva in menta con
  barretta sotto, scrim locale navy, base a y 1004
- **8 card dato**, ancorate alla frase e non a un tempo scritto a mano:
  20% dell'ossigeno · 2% del peso · 3-4 cm di escursione · 1 cm dopo 5 ore ·
  30-40% di capacita in meno · 40 minuti di caffe · 50% in studio · 8 ore di resa
- **4 stacchi di capitolo**: MECCANICO NON METABOLICO · NON RISOLVE MASCHERA ·
  POSTURA ACCUMULATA NON DISCIPLINA · NON SI STANCA SOFFOCA
- **lockup d'apertura** e **chip identita** (MOBILITAS · STUDIO OSTEOPATICO,
  letto dal cartoncino in inquadratura), **closing** e **barra di avanzamento**

Il lato delle card e stato misurato sui frame veri (`scripts/place_cards.py`):
la fascia alta sinistra e libera allo 0,0-0,8%, la destra sta fra il 1,5% e il
4,8%, quindi tutte le card vanno a sinistra.

Nessuna parola a schermo e inventata: viene dalla trascrizione oppure e
un'etichetta strutturale.

## Come sono state trovate le papere

Whisper, su file intero, **appiana le riprese doppie**: al posto della papera
scrive una frase corretta che non e stata pronunciata. In questo girato lo ha
fatto almeno tre volte, e la papera a 13:39 non compare in nessuna trascrizione
lunga.

Il metodo che ha funzionato: per ognuna delle 46 pause sopra 1,5 s, trascrivere
**separatamente** i 9 secondi prima e i 9 dopo (`scripts/gap_probe.sh`). Due clip
distinte, quindi whisper non vede mai le due riprese insieme e non puo fonderle.
Se il "DOPO" ricomincia con le parole del "PRIMA", e una ripresa doppia.

## Correzioni dopo la prima consegna

L'utente ha segnalato una parola troncata. Erano due difetti:

1. **"toracica" tagliata a meta** (giunta a 625,01s sorgente). Il rilevatore di
   parlato chiudeva il blocco a -34 dB, ma la coda della sillaba scende sotto
   quella soglia restando udibile. Ora il punto di taglio e il primo istante in
   cui l'energia torna al fondo di sala (`scripts/cutpoints.py`), e `build_edl.py`
   stampa l'energia residua di ogni giunta: deve stare sotto -55 dB.
2. **Una frase ripetuta due volte** ("Devi iniziare a pensarlo come quello che e
   davvero, un problema di postura", a 09:28 del primo montaggio). Era una
   ripresa doppia che nessuna trascrizione lunga mostrava. Trovata con il sondaggio
   delle pause, insieme ad altre due mai viste prima.

Tutte e 31 le giunte del nuovo montaggio sono state riverificate ritrascrivendo
14 s attorno a ognuna: ognuna si richiude in una frase intera.

## Da sapere

- Nessun volto di terzi nel girato.
- In inquadratura ci sono gia marchio e QR Mobilitas sulla scrivania.
- L'intermedio gradato `assets/intermediate-1080p-sdr.mp4` (2,7 GB) si puo
  cancellare a lavoro chiuso: si rigenera dal LUT e dal comando nella skill.

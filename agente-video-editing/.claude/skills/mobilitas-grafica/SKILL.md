---
name: mobilitas-grafica
description: Come si producono grafica, suono e formati derivati dei video @Studio_Mobilitas — compositore che vede il video (vetro smerigliato, colore che si spegne, spinte di camera), dieci tipi di infografica sincronizzati alla voce, sottotitoli cinetici, card che sanno dov'è il volto, titoli che passano dietro la presentatrice (sagoma Apple Vision), sound design sintetizzato, Shorts 9:16 dal 4K, miniature scelte sulla qualità del volto. Renderer Pillow che compone il fotogramma e lo passa in pipe a ffmpeg. Usala quando un video deve uscire con grafica, suoni, Shorts o miniature, o quando qualcosa di questo va corretto.
---

# mobilitas-grafica

Lo stile lo detta `mobilitas-style`; qui c'è come si produce. Le decisioni (quali card, quali titoli, quali Shorts) sono in `regia.json` (skill `mobilitas-regia`).

## Perché Pillow in pipe, e perché compone tutto il fotogramma

Questo `ffmpeg` non ha **né `libass` né `drawtext`**: il testo va rasterizzato fuori. Un compositore a browser su 24.000 frame sarebbe lento e dipenderebbe dalla rete.

Da v4 il renderer **compone il fotogramma intero**: legge il montato pulito da ffmpeg (RGB, matrice BT.709 dichiarata in ingresso e in uscita: senza, la pelle cambia tono), ci disegna sopra e scrive RGB grezzo all'encoder (`motore/grafica/render.py`, `monta.finale`). Vedere il video serve a tre cose che un livello trasparente non può fare:

- **vetro smerigliato**: sotto ogni pannello il video sfocato e velato di navy, con ombra e filo di luce;
- **colore che si spegne** dietro di lei durante i titoli: la stanza va in blu notte, lei resta a colori (la sagoma);
- **spinta di camera**: +5,5% sui titoli (sale in 1,2 s, torna nell'uscita), +3,5% lineare sulle enfasi.

Moduli: `grafica/base.py` (primitive: testo, icone, tela sovracampionata, vetro), `grafica/info.py` (i dieci tipi di infografica), `grafica/render.py` (scena, sottotitoli, titoli dietro, apertura e chiusura, compositore).

## Le fasi

| fase | cosa | esce |
|---|---|---|
| `grafica` | ancora ogni elemento a una frase del montato | `data/grafica.json` |
| `inquadra` | sceglie il lato di card, apertura e chip **sul volto**, nel taglio in cui cadono | lati in `grafica.json` |
| `sagome` | sagoma della persona (Vision) nei frame dei titoli dietro | `data/sagome/` |
| `anteprima` | grafica sopra i frame veri del montato | `controlli/anteprima.jpg` |
| `suono` | sound design e mix | `assets/mix-finale.wav` |
| `finale` | montato + grafica in pipe + mix | `renders/<slug>_FINALE.mp4` |
| `shorts`, `miniature` | formati derivati | `shorts/`, `miniature/` |

`grafica` riscrive `grafica.json` da capo: dopo `grafica` va sempre rifatto `inquadra` (`./mve stato` lo dice).

## Sottotitoli cinetici

Gruppi da 2-3 parole, chiusi da punteggiatura di fine frase, pausa oltre 0,45 s o 2,4 s di durata. Niente pillola di fondo: testo paper con contorno navy e ombra morbida. Ogni parola **entra quando viene detta** (rimbalzo piccolo, 0,16 s); la parola attiva è navy su una **pillola menta che scivola** dalla parola precedente in 0,09 s. Nelle frasi di `enfasi` il corpo cresce di 1,28x e la scena si vela di navy ai bordi. Si spengono durante i titoli e la chiusura (dicono le stesse parole).

Le parole vengono da `parole-montato.json`, trascritto a pezzi da 10 s: la versione su file intero perdeva la prima parola di molte frasi (in YT_TOFU_02 143 parole su 2161). Il QC controlla che i sottotitoli coprano almeno il 99% delle parole.

Le correzioni di trascrizione (`correzioni` in regia) toccano solo il testo, mai l'audio. Oltre all'impresso si consegna l'SRT (`consegna`).

## Infografiche (card)

Dieci tipi, scelti in regia con `tipo` (campi in `mobilitas-regia/references/schema.md`): `numero` (contatore con `barra`, `anello`, `punti`, `batteria`), `barre`, `orologio`, `icone`, `lista`, `catena`, `citazione`, `anatomia`, `postura`, `curva`. Ogni infografica disegna solo il contenuto; il pannello di vetro lo mette la scena.

- **Le voci seguono la voce.** Ogni voce con `frase` diventa `t` (secondi dall'ingresso) nella fase `grafica`, ed entra quando lei la dice. La card dura fino all'ultima voce + `coda`.
- **Testata comune**: eyebrow battuto a macchina, filo menta che si disegna. Poi ogni tipo ha il suo ingresso: il numero conta (0,95 s) e il grafico si riempie insieme, le voci di lista scivolano e i segni rimbalzano, i nodi della catena si collegano con una goccia di luce, l'orologio gira fino all'ora e lo spicchio del tempo che manca si apre, l'anatomia respira (periodo 3,4 s) e la misura compare quando la dice, la figura seduta si affloscia lasciando il fantasma della postura eretta, la curva si disegna in modo da arrivare a ogni etichetta mentre lei la pronuncia.
- **Le misure si leggono, non si inventano**: scale, quadranti e assi portano solo numeri ed etichette strutturali.
- Finito l'ingresso il contenuto si congela in uno sprite; quelli che si muovono sempre (anatomia, orologio, catena, curva, punto che pulsa) no.
- **Lato e volto**: `inquadra` chiede a `info.misura` larghezza e altezza vere, proietta la testa nel taglio e sceglie il lato con più margine; due card a schermo insieme vanno su lati opposti; `lato` in regia vince. Il QC fallisce se una card tocca la testa.
- **Prova dei tipi**: `controlli/movimento.jpg` mostra il primo di ogni tipo a tre istanti del suo tempo a schermo.
- Il numero ha la scala per unità (`%` 0-100, `cm` 0-1,25x, `min` 0-60); `prima` fa scendere il numero lasciando il fantasma; `riferimento` sui `punti` disegna a contorno l'altra quantità ("2% del peso" contro "20% dell'ossigeno").

## Scene a tutto schermo (`grafica/scene.py`)

La "Motion in casa": stacchi animati generati dalla regia (`scene`), tre tipi (`parole`, `numero`,
`confronto`). Composizione: il video sotto si rimpicciolisce a 160x90, si sfoca e si vela di navy all'80%
(lei continua a muoversi dietro il vetro); sopra, un bagliore menta che deriva, una griglia di punti che
scorre in parallasse, la vignetta; il contenuto deriva di +2,5% per tutta la scena.

- **Ingresso** (0,5 s): zoomata dentro il video fino a +22% che dissolve nel vetro, con un lampo menta
  del 10% a metà. A inizio video non c'è un video da cui entrare: la scena parte già piena.
- **Uscita** (0,45 s): la scena dissolve e il video atterra da +10%.
- `parole`: ogni parola arriva grande (1,35x) e si posa con un rimbalzo quando la dice; le righe già
  dette scendono al 50%; parole chiave in menta con bagliore; `spegne` tremola e resta al 22%, `barra`
  traccia una riga paper, `sottolinea` una riga menta. Il corpo parte da 168 px e scende finché la frase
  sta in 4 righe da 1560 px. I sottotitoli si spengono (le parole sono già la scena).
- `numero`: 300 px che contano in 1,4 s, unità che rimbalza, lampo e alone fermo, grafico da 420 px.
- `confronto`: divisore che si disegna dall'alto, ogni lato entra sulla sua frase, segni e barre proporzionali.
- Avanzamento e sottotitoli restano sopra la scena; card e apertura sotto una scena non si vedono
  (`grafica` lo segnala).
- Suono: risucchio e colpo basso all'ingresso, soffio che scende all'uscita, pop sulle parole, tick e colpo sul numero.

## Titoli dietro

Il capitolo si scrive grande e si ritaglia con la sagoma della persona: passa dietro di lei. Per costruzione non le copre mai il volto.

- **Il layout si misura sulla sagoma**, sulla **parola peggiore** (non sulla media: "NON M▒▒BOLICO" non si legge anche con il 20% medio coperto). Candidati: due righe al centro (fino a 250 px, ogni riga può scorrere di ±260 px), colonna a sinistra, colonna a destra (le parole impilate, allineate al bordo, a due corpi). La colonna vince solo se legge davvero meglio (penalità sul corpo più piccolo). In YT_TOFU_02 il centro lasciava coperte il 22-33% delle parole peggiori, le colonne 0-8%. Il renderer stampa layout, corpo e copertura per ogni titolo: sopra il 30% conviene accorciare il titolo.
- In colonna la seconda riga torna **gigante, a solo contorno**, dall'altra parte della stanza (l'"eco"): resta la scala monumentale, e la parola è già a schermo.
- Ingresso: le lettere salgono una a una con rimbalzo (0,028 s di sfasamento, 0,42 s per lettera), la seconda riga 0,12 s dopo; una **lama di luce menta** inclinata attraversa la stanza in 0,62 s, dietro di lei; un filo menta si disegna sotto l'ultima riga. Uscita: tutto sale e svanisce in 0,35 s.
- Lo sfondo dietro si scurisce (navy, alfa 125) per il contrasto della menta sul teal.
- L'eyebrow porta il numero del capitolo (`02 · IL CAFFÈ`), sta **sopra** la persona, si batte a macchina.
- Il taglio durante il titolo è **largo**: al medio la persona è più larga e nasconde un terzo in più.
- Le sagome si calcolano sul montato pulito: se cambia l'inquadratura, vanno rifatte (`sagome`).

## Apertura, chip, chiusura, avanzamento

- Apertura e chip: pannello a tendina, eyebrow a macchina, righe che salgono ciascuna da una feritoia.
- Chiusura: trama di fili menta che scorre, titolo che cade lettera per lettera, bordo della CTA che si disegna in senso orario e poi pulsa.
- Avanzamento: barra a segmenti, uno per capitolo; il segmento corrente è più acceso.

## Stacchi pieni

Con `"dietro": false` il capitolo è una scheda piena navy di 1,75 s che entra 1,3 s prima della frase e cade sulla pausa. Resta per i video in cui la sagoma non si può usare (più persone, sfondo complicato).

## Sound design (`suono`)

Sintetizzato con numpy, niente stock: whoosh all'ingresso delle card (nel panorama dal lato della card), tick del contatore che rallentano con il numero e un tick acuto quando si ferma, salita + colpo basso + sibilo della lama sui titoli dietro, fruscio corto sui punch-in d'enfasi, colpo morbido su apertura e chiusura. Tutto 10-16 dB sotto la voce. Musica solo se c'è un file in `assets/musica/`: in loop a −30 LUFS, con sidechain sotto la voce.

## Shorts

Dalle `shorts` di regia. Ritaglio verticale dal 4K (1215x2160 a tutta altezza → 1080x1920 senza perdita), due tagli alternati (pieno e stretto 1,22) a ogni giunta e circa ogni 6 s, volto centrato. Hook in alto sotto i 260 px della barra di Shorts, barra di avanzamento sotto l'hook, sottotitoli da 84 px con base a y 1300 (sopra i ~420 px dell'interfaccia in basso), 1,6 s finali con "IL VIDEO COMPLETO È SUL CANALE". Audio dalla voce già montata, a −14 LUFS. Foglio di controllo: `controlli/short<N>.jpg`.

## Miniature

Tre varianti 1280x720 dai fotogrammi con la qualità del volto più alta per Vision, occhi aperti e viso frontale, a 20 s l'uno dall'altro. Soggetto a destra (taglio 1,45 dal 4K), pannello navy che sfuma a sinistra, due righe in Montserrat 900 (l'ultima in menta). `controlli/miniatura-piccola.png` è la miniatura a 168 px, come appare nella griglia di YouTube: va guardata.

## Verifica

Guarda **sempre** `controlli/anteprima.jpg` (elementi a ingresso finito) e `controlli/movimento.jpg` (primo titolo, prima card, apertura, chiusura e un sottotitolo a più istanti dell'ingresso) prima del render finale: gli errori di posizione e di animazione si vedono solo lì. Comandi passo per passo e tempi: `references/pipeline.md`.

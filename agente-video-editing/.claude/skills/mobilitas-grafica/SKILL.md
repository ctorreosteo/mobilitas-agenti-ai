---
name: mobilitas-grafica
description: Come si producono grafica, suono e formati derivati dei video @Studio_Mobilitas — sottotitoli karaoke, card che sanno dov'è il volto, titoli che passano dietro la presentatrice (sagoma Apple Vision), sound design sintetizzato, Shorts 9:16 dal 4K, miniature scelte sulla qualità del volto. Renderer Pillow che scrive RGBA nella pipe di ffmpeg. Usala quando un video deve uscire con grafica, suoni, Shorts o miniature, o quando qualcosa di questo va corretto.
---

# mobilitas-grafica

Lo stile lo detta `mobilitas-style`; qui c'è come si produce. Le decisioni (quali card, quali titoli, quali Shorts) sono in `regia.json` (skill `mobilitas-regia`).

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
| `finale` | montato + grafica in pipe + mix | `renders/<slug>_FINALE.mp4` |
| `shorts`, `miniature` | formati derivati | `shorts/`, `miniature/` |

`grafica` riscrive `grafica.json` da capo: dopo `grafica` va sempre rifatto `inquadra` (`./mve stato` lo dice).

## Sottotitoli

Gruppi da 2-3 parole, chiusi da punteggiatura di fine frase, pausa oltre 0,45 s o 2,4 s di durata. La parola attiva è in menta con una barretta sotto. Si spengono durante i titoli e la chiusura (dicono le stesse parole).

Le parole vengono da `parole-montato.json`, trascritto a pezzi da 10 s: la versione su file intero perdeva la prima parola di molte frasi (in YT_TOFU_02 143 parole su 2161). Il QC controlla che i sottotitoli coprano almeno il 99% delle parole.

Le correzioni di trascrizione (`correzioni` in regia) toccano solo il testo, mai l'audio. Oltre all'impresso si consegna l'SRT (`consegna`).

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

Dalle `shorts` di regia. Ritaglio verticale dal 4K (1215x2160 a tutta altezza → 1080x1920 senza perdita), due tagli alternati (pieno e stretto 1,22) a ogni giunta e circa ogni 6 s, volto centrato. Hook in alto sotto i 260 px della barra di Shorts, barra di avanzamento sotto l'hook, sottotitoli da 84 px con base a y 1300 (sopra i ~420 px dell'interfaccia in basso), 1,6 s finali con "IL VIDEO COMPLETO È SUL CANALE". Audio dalla voce già montata, a −14 LUFS. Foglio di controllo: `controlli/short<N>.jpg`.

## Miniature

Tre varianti 1280x720 dai fotogrammi con la qualità del volto più alta per Vision, occhi aperti e viso frontale, a 20 s l'uno dall'altro. Soggetto a destra (taglio 1,45 dal 4K), pannello navy che sfuma a sinistra, due righe in Montserrat 900 (l'ultima in menta). `controlli/miniatura-piccola.png` è la miniatura a 168 px, come appare nella griglia di YouTube: va guardata.

## Verifica

Guarda **sempre** `controlli/anteprima.jpg` prima del render finale: gli errori di posizione si vedono solo lì. Comandi passo per passo e tempi: `references/pipeline.md`.

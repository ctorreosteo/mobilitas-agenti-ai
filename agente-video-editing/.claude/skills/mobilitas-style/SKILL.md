---
name: mobilitas-style
description: La bibbia visiva dei video di @Studio_Mobilitas — palette, tipografia, zone sicure, inquadrature, titoli dietro, Shorts, miniature, suono, movimento e divieti. Va letta prima di disegnare qualsiasi grafica, sottotitolo, card o closing per un video del canale, e prima di cambiare i valori in motore/motore/stile.py.
---

# mobilitas-style

Lo stile non e decorazione: la grafica e **strumentazione clinica sopra una
conversazione**. Il girato e il soggetto, la grafica commenta. Tutto cio che e
"voce" e geometrico e caldo, tutto cio che e "misura" e monospaziato e freddo.

La bibbia vive in due posti che devono restare allineati:

- questo documento, per il perche;
- `motore/motore/stile.py`, per i valori che il motore legge (uno solo per tutti i video).

Chi cambia lo stile cambia **il modulo**, non i singoli renderer.

## Palette

| token | valore | ruolo |
|---|---|---|
| `NAVY` | `#002552` | riempimento delle card |
| `NAVY_DEEP` | `#001730` | scrim dei sottotitoli, schede piene, closing |
| `MINT` | `#72FB93` | **unico accento**: parola attiva, numeri, avanzamento |
| `PAPER` | `#EDF3F0` | testo primario (mai bianco puro) |
| `MUTED` | `#8FA8BE` | glosse e etichette secondarie |

Navy e verde vengono dal cartoncino Mobilitas che sta in inquadratura, non da
una scelta astratta. Il fondo scena e un teal che va da `#4798A5` a sinistra a
`#0098BA` a destra: per questo le card sono scure (staccano) e **l'accento non
puo essere ciano** (si confonderebbe col fondo).

## Tipografia

- **Montserrat** 900/800/600 — la voce parlata: sottotitoli, titoli, numeri.
- **IBM Plex Mono** Bold — la voce dello strumento: etichette, unita, CTA.

Sans + mono, mai due sans. La tensione fra divulgazione (Montserrat, umanista)
e referto (Plex Mono, tecnico) *e* il contenuto.

I font vanno presi in TTF completo da Google Fonts. **Non usare i woff2 nella
cache di hyperframes**: sono sottoinsiemi per pagina, a cui mancano lettere
(`J`, `K`) e accenti, e Pillow disegna i glifi mancanti come vuoti, senza
errore. Vedi `references/font.md`.

Corpi a 1080p in `SIZE`: sottotitolo 62 (80 nelle frasi di enfasi), numero card 128,
glossa 30, scala 20, stacco 92, eyebrow mono 26. Il tracking dell'eyebrow e +0.22em, quello dei titoli -0.03em.

## Pannelli e icone

- **Vetro smerigliato**: il video dietro sfocato e velato di navy (`VETRO_VELO` 0,66), raggio 26,
  ombra navy morbida, filo di luce che sfuma dall'alto verso il basso, un trattino menta
  nell'angolo in alto a sinistra. Non e un gradient sul testo: e il fondo del pannello.
- **Icone**: Material Symbols Rounded, a contorno (peso 500), menta; piene solo quando contano
  qualcosa (`icone`). Mai icone decorative accanto al testo: un'icona sta in un nodo, in un anello o in un conteggio.
- **Figure** (anatomia, postura): linee paper a bassa opacita per la struttura, menta solo per
  cio di cui lei sta parlando (il diaframma, i punti numerati). Stilizzate, mai realistiche.
- **Dati**: menta pieno = il valore, menta velato = l'intervallo (30-40), contorno = il riferimento
  o il fantasma, paper al 30% = il resto della scala.

## Zone sicure

Si misurano, **non si assumono**: cambiano con la posizione del soggetto e con
il taglio di camera. `inquadra` proietta la testa (volto di Vision + capelli) nel
taglio in cui ogni card sta a schermo e sceglie il lato con piu margine.

- card, lockup, chip: fascia alta, da y 150, larghezza 560, lato sinistro o destro
- rail sottotitoli: centrato, base a y 1004, sopra il piano scrivania
- margine title-safe: 96 px per lato
- set tipico (YT_TOFU_02): presentatrice al centro, cartoncino QR in basso a
  sinistra, modello anatomico in basso a destra; nel taglio largo la fascia alta
  sinistra resta libera con 45-120 px di margine dalla testa

## Inquadrature

Tre tagli dalla stessa camera 4K: **largo** (tutto il quadro), **medio** (1,28x,
volto al 34% dell'altezza), **stretto** (1,62x, volto al 38%). Il medio taglia
il piano della scrivania a meta: e voluto, il set resta riconoscibile nel largo.

- a ogni giunta il taglio cambia: niente dissolvenze sulle giunte
- largo quando a schermo c'e una card, il lockup, il chip o un titolo dietro
- stretto solo sulle frasi di enfasi (5-9 per video)
- nessun taglio sopra 2x: oltre si scende sotto i pixel nativi

## Titoli dietro

Il capitolo e un titolo gigante (Montserrat 900, fino a 250 px, tracking
-0.045em) che passa dietro la presentatrice: prima riga paper, seconda menta,
eyebrow mono menta sopra con il numero del capitolo, sfondo velato di navy,
filo menta sotto. Quando la testa al centro mangerebbe le parole, il titolo va
in colonna su un lato e la seconda riga torna gigante a solo contorno
dall'altra parte (l'eco). Una lama di luce menta attraversa la stanza dietro di lei. E la firma visiva del canale:
la grafica sta *nello* spazio della stanza, non sopra la persona.

## Shorts

1080x1920. Hook in alto (Montserrat 900, 72 px, scrim navy) sotto i 260 px della
barra; sottotitoli 84 px con base a y 1300; niente testo negli ultimi 420 px.
Chiusura di 1,6 s: "IL VIDEO COMPLETO È SUL CANALE".

## Miniature

1280x720. Soggetto a destra, pannello navy a sinistra che sfuma verso di lei,
due righe al massimo, tre parole per riga, l'ultima in menta. Deve leggersi a
168 px di larghezza.

## Suono

Il suono e parte dello stile: whoosh morbidi e colpi bassi sintetizzati, mai
effetti comici, mai sopra la voce (10-16 dB sotto). Niente musica senza licenza.

## Movimento

Tutto entra, niente compare. Ma ogni movimento finisce presto (entro ~1,6 s) e poi
sta fermo: il movimento accompagna la voce, non le fa concorrenza.

- parola del sottotitolo: entra quando viene detta, scala 0,62 → 1 con rimbalzo (`ease_out_back`) + salita, 0,16 s
- parola attiva: pillola menta che scivola dalla parola precedente, 0,09 s
- card: tendina dal lato (`ease_out_expo`) + salita 26 px, 0,42 s; numero che conta 0,95 s; uscita 0,30 s
- etichette mono: scritte a macchina, 0,03 s a carattere, con cursore menta
- titolo dietro: lettere che salgono con rimbalzo, 0,028 s di sfasamento; lama di luce 0,62 s; uscita 0,35 s verso l'alto
- enfasi: velo navy ai bordi, 0,35 s dentro e fuori; spinta di camera lineare fino a +3,5%
- titolo dietro: la stanza si spegne in blu notte (lei resta a colori), spinta +5,5% in 1,2 s
- voci delle infografiche: entrano sulla parola che le pronuncia, mai prima
- stacco di capitolo: 0,30 s dentro / 0,30 s fuori, secco
- barra di avanzamento: lineare, a segmenti per capitolo

Il rimbalzo è uno solo (`ease_out_back` con k 1,7): mai elastici, mai oscillazioni ripetute.
Il bagliore menta (lampo sul numero, pulsazione della CTA) è un alone *sotto* il testo,
non un gradient sul testo.

## Divieti

- **niente testo inventato**: ogni parola a schermo viene dalla trascrizione
  oppure e un'etichetta strutturale (`MECCANISMO`, `IN STUDIO`, `PROSSIMO VIDEO`).
  Le glosse sotto i numeri riformulano quello che dice, non aggiungono
  affermazioni cliniche.
- nessun secondo accento oltre alla menta
- niente gradient sul testo, niente ciano, niente viola
- niente bianco puro
- non coprire mai il volto con una card: le schede piene sono ammesse solo come
  stacco di capitolo, brevi, e cadono su una pausa
- niente gradient sul testo; lo sfondo delle miniature puo sfumare, il testo no

## Formato di consegna

1920x1080 a 30000/1001, H.264 High, yuv420p, tag bt709/bt709/bt709,
audio AAC 192k a -14 LUFS / -1,5 dBTP. Il 4K non e il formato del canale.

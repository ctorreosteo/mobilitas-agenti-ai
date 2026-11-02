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

**Dal 27/10/2026 la fonte è `motore/motore/brand.json`** (i valori del sito), letta da `stile.py` e dagli inserti HyperFrames: si cambia lì, non nei renderer.

| token | valore | ruolo |
|---|---|---|
| `NAVY` (blu notte) | `#002552` | pannelli, card, chip |
| `NAVY_DEEP` (blu profondo) | `#001A3D` | pannelli grandi, numero gigante, chiusura, fondo del prima/dopo |
| `MINT` (verde) | `#72FA93` | **unico accento, solo sopra il blu** (pannello, card, bottone, schermata blu): parola chiave, numeri, frecce. Mai sul video nudo, mai sul panna. Sul video nudo il testo è panna con ombra morbida e la chiave si distingue per peso e corpo |
| `PAPER` (panna) | `#F4F4F4` | testo primario; barra d'avanzamento |
| `MUTED` | panna al 70% sul blu (fase 7c; prima 76%) | testo secondario |

Navy e verde vengono dal cartoncino Mobilitas che sta in inquadratura, non da
una scelta astratta. Il fondo scena e un teal che va da `#4798A5` a sinistra a
`#0098BA` a destra: per questo le card sono scure (staccano) e **l'accento non
puo essere ciano** (si confonderebbe col fondo).

**Dal 01/11/2026 (fase 7c, Riccardo) il video segue il sito** (letto il 30/10/2026, `report/brand-sito-video.md`):
- fondo delle scene scure, schermate e schermata finale: `blu_abisso` `#000F2B` con il radiale del sito `radial-gradient(120% 80% at 50% 0%, #00346F 0%, #002552 45%, #000F2B 100%)`;
- titoli in minuscolo con il punto, parola chiave in gradiente verde → azzurro (`#72FA93` → `#38BDF8`): l'azzurro **solo dentro quel gradiente**, mai come luce o testo pieno;
- testo secondario panna al 70%;
- maiuscolo spaziato solo per etichette strutturali brevi (≥ 30 px);
- pittogramma della «T» su un disco panna (non ricolorato): schermata finale e chip;
- **no** al rosso corallo del sito e ai badge verdi dei numeri.

## Tipografia

- **Solo Montserrat** (brand, dal 27/10/2026): pesi del sito (misurati il 30/10/2026): titoli 900, h3 800, corpo 400-500, etichette 700, pulsanti 800; nel video 800-900 per le parole grandi. IBM Plex Mono non si usa più (in `render.mono()` ora c'è Montserrat 500). Maiuscolo spaziato solo per le etichette strutturali brevi (`.eyebrow`, fase 7c); i testi in regia si scrivono con la maiuscola iniziale, non tutto maiuscolo.

I font vanno presi in TTF completo da Google Fonts. **Non usare i woff2 nella
cache di hyperframes**: sono sottoinsiemi per pagina, a cui mancano lettere
(`J`, `K`) e accenti, e Pillow disegna i glifi mancanti come vuoti, senza
errore. Vedi `references/font.md`.

Corpi a 1080p in `SIZE`: sottotitolo 62, numero card 128, stacco 92, etichetta 26. Frase chiave sul pannello: 72 (300 + 800). Numero gigante: 290 in peso 200 (a 330 «900» usciva dalla zona sicura). Chip v2: nome 52/300, ruolo 36/500. Ogni testo che va letto: almeno 40-44 px (il video si guarda anche sul telefono).

**Pannello laterale** (`PANNELLO_W` = 760 px, a tutta altezza): ospita frasi chiave e inserti; la persona sta al terzo opposto (taglio "lato" di `inquadra`). Blu notte **pieno**, mai trasparente (niente vetro: in trasparenza si vedevano oggetti e il volto). Il testo resta a 110 px dal bordo dello schermo (`PANNELLO_MARGINE`) e a 96 px da sopra e sotto. Fra due elementi di fila sullo stesso lato il pannello non esce e rientra: cambia solo il testo.

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
eyebrow mono menta sopra, sfondo velato di navy. E la firma visiva del canale:
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

Regole di mestiere del livello 3 (entrate 8-12 frame, rimbalzo max 5%, parole sfalsate 2-3 frame, uscite più corte, ogni elemento sulla sua parola ±2 frame e leggibile almeno 1 s, mai più di 2 elementi insieme, testo ≥ 60 px e chiavi ≥ 120 px): `mobilitas-grafica`, sezione «Livello 3». Valori qui sotto: quelli della v1-v2 (Pillow).


- gruppo sottotitolo: dissolvenza + salita 14 px, 0,16 s
- parola attiva: colore verso menta + barretta menta sotto, 0,09 s
- card: tendina da sinistra (`ease_out_expo`) + salita 26 px, 0,42 s; uscita 0,30 s
- stacco di capitolo: 0,30 s dentro / 0,30 s fuori, secco
- barra di avanzamento: lineare su tutta la durata

## Divieti

- **niente testo inventato**: ogni parola a schermo viene dalla trascrizione
  oppure e un'etichetta strutturale (`MECCANISMO`, `IN STUDIO`, `PROSSIMO VIDEO`).
  Le glosse sotto i numeri riformulano quello che dice, non aggiungono
  affermazioni cliniche.
- nessun secondo accento oltre al verde, e il verde solo su blu
- niente bagliori, neon, gradienti decorativi, maiuscolo urlato (dalle reference si prendono le tecniche, non l'estetica). **Dal 27/10/2026 nel video sono ammesse** (decisione di Riccardo, `brand.json` → `video`): ombre morbide, sfondo sfocato dietro la persona, luce morbida del brand sulla parete, testo e oggetti davanti o dietro di lui (sagoma di Vision), oggetti semplici in prospettiva, pesi 700-900 per le parole chiave grandi
- niente gradient sul testo (unica eccezione dal 01/11/2026: la parola chiave dei titoli, verde → azzurro come il sito), niente ciano fuori da quel gradiente, niente viola
- niente bianco puro
- non coprire mai il volto con una card: le schede piene sono ammesse solo come
  stacco di capitolo, brevi, e cadono su una pausa
- niente gradient sul testo; lo sfondo delle miniature puo sfumare, il testo no

## Formato di consegna

1920x1080 al frame rate del progetto (`fps_uscita`: 29,97 dalla iPhone, 25 dalla A6700), H.264 High, yuv420p, tag bt709/bt709/bt709, range tv, audio AAC 192k a -14 LUFS / -1,5 dBTP. Il 4K non e il formato del canale.

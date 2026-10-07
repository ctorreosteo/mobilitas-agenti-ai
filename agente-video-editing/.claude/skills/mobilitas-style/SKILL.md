---
name: mobilitas-style
description: La bibbia visiva dei video di @Studio_Mobilitas — palette, tipografia, zone sicure, movimento e divieti. Va letta prima di disegnare qualsiasi grafica, sottotitolo, card o closing per un video del canale; e prima di cambiare i valori in scripts/mobilitas_style.py.
---

# mobilitas-style

Lo stile non e decorazione: la grafica e **strumentazione clinica sopra una
conversazione**. Il girato e il soggetto, la grafica commenta. Tutto cio che e
"voce" e geometrico e caldo, tutto cio che e "misura" e monospaziato e freddo.

La bibbia vive in due posti che devono restare allineati:

- questo documento, per il perche;
- `videos/<slug>/scripts/mobilitas_style.py`, per i valori che i renderer leggono.

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

Corpi a 1080p in `SIZE`: sottotitolo 62, numero card 128, stacco 92, eyebrow
mono 26. Il tracking dell'eyebrow e +0.22em, quello dei titoli -0.03em.

## Zone sicure

Si misurano sul montato, **non si assumono**: cambiano da video a video con la
posizione del soggetto. `scripts/place_cards.py` campiona i frame nella finestra
di ogni card e sceglie il lato piu libero.

Per YT_TOFU_02 (presentatrice al centro, cartoncino QR in basso a sinistra,
modello anatomico in basso a destra):

- soggetto stabile fra x 720 e 1320
- fasce alte libere: sinistra x 96-680, destra x 1240-1824, entrambe y 150-550
- **la fascia alta si sporca nei primi secondi**, quando si sporge in avanti:
  l'apertura va misurata a parte
- rail sottotitoli: centrato, base a y 1004, sopra il piano scrivania
- margine title-safe: 96 px per lato

## Movimento

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
- nessun secondo accento oltre alla menta
- niente gradient sul testo, niente ciano, niente viola
- niente bianco puro
- non coprire mai il volto con una card: le schede piene sono ammesse solo come
  stacco di capitolo, brevi, e cadono su una pausa

## Formato di consegna

1920x1080 a 30000/1001, H.264 High, yuv420p, tag bt709/bt709/bt709,
audio AAC 192k a -14 LUFS / -1,5 dBTP. Il 4K non e il formato del canale.

# frame.md — verità di design

Talking-head di divulgazione clinica, 3840×2160 @30fps. Il girato è l'unico
soggetto; la grafica è **strumentazione clinica sopra una conversazione**, mai
decorazione.

## Concetto

*Un referto che commenta un discorso.* Il parlato è caldo e diretto; i dati che
lo sostengono arrivano come letture di uno strumento. Tutto ciò che è "voce"
è geometrico e umano, tutto ciò che è "misura" è monospaziato e freddo.

## Palette

| token | valore | ruolo |
|---|---|---|
| `--navy` | `#002552` | base brand, card piene, stacco |
| `--navy-deep` | `#001730` | scrim, fondo closing |
| `--mint` | `#72FB93` | **unico accento**: parola attiva, dati, progress |
| `--paper` | `#EDF3F0` | testo primario (mai `#fff` puro, virato menta) |
| `--muted` | `#8FA8BE` | etichette secondarie |

Derivata come registro cromatico dal canale di riferimento; esposta come
variabile `accent` per la sostituzione col brand dell'utente.

## Tipografia

- **Montserrat** 900/700 — voce parlata: sottotitoli, titoli card. Geometrica,
  calda, leggibile in movimento.
- **IBM Plex Mono** 700 — voce strumento: etichette, numeri, contatori, CTA.

La tensione è il contenuto: *divulgazione* (Montserrat, umanista, amichevole)
contro *referto* (Plex Mono, tecnico, misurato). Sans + mono, mai due sans.
Contrasto di peso estremo: 900 contro 400 mono.

| elemento | dimensione | peso | tracking |
|---|---|---|---|
| parola sottotitolo | 132px | 900 | −0.03em |
| titolo card | 108px | 900 | −0.035em |
| numero card | 190px | 900 | −0.04em |
| eyebrow mono | 34px | 700 | +0.24em |
| sub card | 46px | 700 | −0.01em |
| nome identità | 64px | 900 | −0.02em |

## Layout e zone sicure

Il soggetto sta stabilmente a **sinistra/centro** inquadratura per tutta la
durata (verificato su contact sheet a 1 frame ogni 4s). Ne consegue:

- **terzo destro** (x da 2380px) → card concetto, zona libera
- **basso centro** (bottom 220px) → rail sottotitoli, sopra il torso
- **alto sinistra** → chip identità, solo nella finestra 6,0–10,5s
- margini title-safe: 5% per lato, nulla a filo bordo

## Motion

- gruppo sottotitolo: fade + salita 26px, 0,16s `power2.out`
- parola attiva: colore → menta + scale 1,07, 0,09s `power1.out`
- card: wipe `clip-path` da sinistra + salita, 0,42s `expo.out`; uscita 0,3s
- stacco "E COME?": 0,3s dentro / 0,3s fuori, secco
- progress bar: `scaleX` lineare sull'intera durata
- ambient: vignetta che respira (ciclo 11s, finito), hairline menta che pulsa

## Trattamento del girato

Correzione conservativa via contratto canonico `data-color-grading` — mai filtri
CSS. Solleva il corridoio buio dei primi 10s senza bruciare la stanza chiara:
`shadows +0.10`, `contrast +0.06`, `vibrance +0.10`, `temperature +0.03`,
vignetta 0.18 feather 0.70, grana 0.04.

## Divieti

- niente logo o nome del canale di riferimento
- niente testo inventato: ogni parola a schermo viene dalla trascrizione o è
  un'etichetta strutturale ("MECCANISMO", "CASO CLINICO")
- niente gradient text, niente cyan/viola, niente card-grid identiche
- nessun secondo accento oltre alla menta

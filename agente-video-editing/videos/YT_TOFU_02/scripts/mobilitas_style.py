#!/usr/bin/env python3
"""La bibbia visiva del canale, come codice.

Un solo posto in cui stanno colori, tipografia, zone sicure e tempi di
animazione. Chi cambia lo stile del canale cambia questo file, non i renderer.
Riferimento: .claude/skills/mobilitas-style/
"""

W, H = 1920, 1080
FPS = 30000 / 1001.0
SAFE = 96                      # margine title-safe, 5%

# ---- colore -----------------------------------------------------------------
# Navy e verde vengono dal cartoncino Mobilitas che sta in inquadratura; il
# fondo scena e un teal che va da #4798A5 a sinistra a #0098BA a destra, quindi
# le card devono essere scure per staccare e l'accento non puo essere ciano.
NAVY       = (0, 37, 82)
NAVY_DEEP  = (0, 23, 48)
MINT       = (114, 251, 147)
PAPER      = (237, 243, 240)
MUTED      = (143, 168, 190)

# ---- tipografia -------------------------------------------------------------
# Due voci: Montserrat e il parlato (geometrica, calda), IBM Plex Mono e lo
# strumento (etichette, numeri, unita). Mai due sans.
FONT_SANS = 'assets/fonts/Montserrat-VF.ttf'
FONT_MONO = 'assets/fonts/IBMPlexMono-Bold.ttf'

SIZE = {
    'caption':      62,   # parola del sottotitolo
    'card_value':  128,   # numero grande
    'card_unit':    40,
    'card_sub':     34,
    'eyebrow':      26,   # etichetta mono
    'chapter':      92,
    'chapter_sub':  40,
    'hook':         54,
    'chip_name':    46,
    'chip_role':    24,
}
TRACK = {'eyebrow': 0.22, 'caption': -0.015, 'chapter': -0.03}   # in em

# ---- zone sicure ------------------------------------------------------------
# Misurate sul montato: la presentatrice occupa x 720-1320 per tutta la durata,
# il cartoncino QR sta in basso a sinistra e il modello anatomico in basso a
# destra. Restano liberi la fascia alta sinistra e la fascia alta destra.
CARD_BOX    = (SAFE, 150, 560, 400)        # x, y, larghezza, altezza massima
CAPTION_BOT = 1004                         # base del blocco sottotitoli
CAPTION_MAXW = 1400
CHIP_POS    = (SAFE, 150)
PROGRESS_H  = 6

# ---- movimento --------------------------------------------------------------
CAP_IN      = 0.16   # salita + dissolvenza del gruppo
CAP_RISE    = 14
WORD_IN     = 0.09   # passaggio della parola attiva
CARD_IN     = 0.42   # tendina da sinistra + salita
CARD_OUT    = 0.30
CARD_RISE   = 26
CHAPTER_IN  = 0.30
CHAPTER_OUT = 0.30


def ease_out_expo(t):
    return 1.0 if t >= 1 else 1 - pow(2, -10 * t)


def ease_out_cubic(t):
    return 1 - pow(1 - min(max(t, 0.0), 1.0), 3)

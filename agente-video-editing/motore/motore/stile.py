"""La bibbia visiva del canale, come codice.

Un solo posto in cui stanno colori, tipografia, zone e tempi di animazione.
Chi cambia lo stile del canale cambia questo file, non i renderer.
Il perche di ogni valore sta in .claude/skills/mobilitas-style/.
"""
from .progetto import RISORSE, FPS

W, H = 1920, 1080
SAFE = 96                      # margine title-safe, 5%

# ---- colore -----------------------------------------------------------------
# Navy e verde vengono dal cartoncino Mobilitas che sta in inquadratura; il
# fondo scena e un teal, quindi le card devono essere scure per staccare e
# l'accento non puo essere ciano.
NAVY = (0, 37, 82)
NAVY_DEEP = (0, 23, 48)
MINT = (114, 251, 147)
PAPER = (237, 243, 240)
MUTED = (143, 168, 190)

# ---- tipografia -------------------------------------------------------------
FONT_SANS = str(RISORSE / 'fonts/Montserrat-VF.ttf')
FONT_MONO = str(RISORSE / 'fonts/IBMPlexMono-Bold.ttf')
# icone: Material Symbols Rounded (Apache 2.0), sottoinsieme; i nomi in risorse/icone.txt
FONT_ICONE = str(RISORSE / 'fonts/MaterialSymbolsRounded-sub.ttf')
ICONE = str(RISORSE / 'icone.txt')

SIZE = {
    'caption': 62,
    'card_value': 128,
    'card_unit': 40,
    'card_sub': 30,
    'card_scala': 20,       # etichette della scala sotto il numero
    'eyebrow': 26,
    'chapter': 92,
    'chapter_sub': 40,
    'behind': 250,          # titolo dietro la presentatrice
    'hook': 54,
    'chip_name': 46,
    'chip_role': 24,
}
TRACK = {'eyebrow': 0.22, 'caption': -0.015, 'chapter': -0.03, 'behind': -0.045}

# ---- vetro ------------------------------------------------------------------
# i pannelli sono vetro smerigliato: il video dietro sfocato, velato di navy
VETRO_VELO = 0.66           # quanto navy sul video sfocato
VETRO_RAGGIO = 26
VETRO_OMBRA = 120           # alfa dell'ombra sotto il pannello

# ---- zone -------------------------------------------------------------------
CARD_W, CARD_TOP = 560, 150
CAPTION_BOT = 1004
CAPTION_MAXW = 1400
PROGRESS_H = 6

# ---- movimento --------------------------------------------------------------
CAP_IN = 0.16
CAP_RISE = 14
CARD_IN = 0.42
CARD_OUT = 0.30
CARD_RISE = 26
CHAPTER_IN = 0.30
CHAPTER_OUT = 0.30
BEHIND_IN = 0.45            # il titolo dietro sale dal basso, lettera per lettera
BEHIND_OUT = 0.35
BEHIND_CHAR = 0.028         # sfasamento fra una lettera e la successiva
BEHIND_DROP = 0.42          # quanto ci mette una lettera ad atterrare
LAMA = 0.62                 # la lama di luce che attraversa la stanza
CAP_POP = 0.16              # una parola del sottotitolo entra quando viene detta
CAP_FORTE = 1.28            # corpo dei sottotitoli nelle frasi di enfasi
COUNT_T0, COUNT_DUR = 0.22, 0.95   # il numero della card conta fino al valore
TYPE_CHAR = 0.03            # scrittura a macchina delle etichette mono

# ---- inquadrature -----------------------------------------------------------
# Fattore di ingrandimento sul fotogramma 4K intero. 2.0 e il limite: oltre si
# scende sotto i pixel nativi del 1080p.
FRAMING = {'largo': 1.0, 'medio': 1.28, 'stretto': 1.62}
# dove cade il centro del volto nell'inquadratura (frazione dell'altezza)
FACE_Y = {'largo': None, 'medio': 0.34, 'stretto': 0.38}

# ---- shorts -----------------------------------------------------------------
SW, SH = 1080, 1920
SHORT_SAFE_TOP = 260        # sopra c'e l'interfaccia di Shorts/Reels
SHORT_SAFE_BOT = 420        # sotto ci sono titolo, pulsanti, descrizione
SHORT_CAPTION_Y = 1470      # base dei sottotitoli verticali: sotto il mento, sopra i 420 px dell'interfaccia
SHORT_BAND = 470            # fascia navy in alto con l'hook: il video sta sotto
# il volto, nel verticale a tutta altezza, sta al 24% dall'alto: proprio dove
# va l'hook. Sopra la testa non c'e girato, quindi l'hook ha la sua fascia
SIZE_SHORT = {'caption': 84, 'hook': 72, 'eyebrow': 30}


def ease_out_expo(t):
    t = min(max(t, 0.0), 1.0)
    return 1.0 if t >= 1 else 1 - pow(2, -10 * t)


def ease_out_back(t, k=1.7):
    """arriva, supera di poco e torna: il rimbalzo delle lettere"""
    t = min(max(t, 0.0), 1.0) - 1
    return 1 + (k + 1) * t ** 3 + k * t ** 2


def ease_out_cubic(t):
    return 1 - pow(1 - min(max(t, 0.0), 1.0), 3)


def ease_in_out(t):
    t = min(max(t, 0.0), 1.0)
    return 3 * t * t - 2 * t * t * t


__all__ = ['FPS']

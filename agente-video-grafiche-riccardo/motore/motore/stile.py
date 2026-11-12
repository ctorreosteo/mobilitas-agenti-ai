"""La bibbia visiva del canale, come codice.

Un solo posto in cui stanno colori, tipografia, zone e tempi di animazione.
Chi cambia lo stile del canale cambia questo file, non i renderer.
Il perche di ogni valore sta in .claude/skills/mobilitas-style/.
"""
import json
from pathlib import Path

from .progetto import RISORSE

W, H = 1920, 1080
SAFE = 96                      # margine title-safe, 5%

# ---- colore -----------------------------------------------------------------
# Dal brand unico (motore/brand.json, gli stessi valori del sito), che vale anche
# per gli inserti HyperFrames. Il verde va SOLO sopra un pannello blu: mai sul
# video nudo, mai sul panna.
BRAND = json.loads((Path(__file__).parent / 'brand.json').read_text(encoding='utf-8'))
_C = BRAND['colori']
NAVY = tuple(_C['blu_notte']['rgb'])
NAVY_DEEP = tuple(_C['blu_profondo']['rgb'])
MINT = tuple(_C['verde']['rgb'])
PAPER = tuple(_C['panna']['rgb'])
# testo secondario: panna al 70% sul blu notte, gia composto (fase 7c: come il corpo del sito; prima 76%)
_SEC = BRAND['trasparenze']['testo_secondario_su_blu']['opacita']
MUTED = tuple(int(round(_SEC * p + (1 - _SEC) * n)) for p, n in zip(PAPER, NAVY))
PITTOGRAMMA = Path(__file__).resolve().parents[2] / BRAND['loghi']['pittogramma']['file']

# ---- tipografia -------------------------------------------------------------
# Solo Montserrat (brand): il vecchio IBM Plex Mono e il maiuscolo spaziato sono
# vietati. FONT_MONO resta come nome per i renderer, ma punta a Montserrat.
FONT_SANS = str(RISORSE / 'fonts/Montserrat-VF.ttf')
FONT_MONO = FONT_SANS
PESO = {'display': 300, 'chiave': 800, 'etichetta': 500, 'corpo': 400}

SIZE = {
    'caption': 62,
    'card_value': 128,
    'card_unit': 40,
    'card_sub': 34,
    'eyebrow': 26,
    'chapter': 92,
    'chapter_sub': 40,
    'behind': 250,          # titolo dietro la presentatrice
    'hook': 54,
    'chip_name': 46,
    'chip_role': 24,
    'chip_role_v2': 36,                 # ruolo del chip v2: leggibile anche sul telefono
}
TRACK = {'eyebrow': 0.0, 'caption': -0.015, 'chapter': -0.03, 'behind': -0.045}   # niente maiuscolo spaziato

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

# ---- inquadrature -----------------------------------------------------------
# Fattore di ingrandimento sul fotogramma 4K intero. 2.0 e il limite: oltre si
# scende sotto i pixel nativi del 1080p.
FRAMING = {'largo': 1.0, 'medio': 1.28, 'stretto': 1.62}
# dove cade il centro del volto nell'inquadratura (frazione dell'altezza)
FACE_Y = {'largo': None, 'medio': 0.34, 'stretto': 0.38}
# taglio "lato": la persona al terzo sinistro o destro, per lasciare spazio a un
# pannello sul lato opposto (frase chiave, numero, telefono...)
FRAMING_LATO = 1.33
LATO_X = {'lato_sx': 1 / 3, 'lato_dx': 2 / 3}     # dove cade il centro del volto, in larghezza
PANNELLO_W = 760                                    # larghezza del pannello sul lato libero
PANNELLO_MARGINE = 110                              # margine interno dal bordo dello schermo (zona sicura 96 px + aria)

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


def ease_out_cubic(t):
    return 1 - pow(1 - min(max(t, 0.0), 1.0), 3)


def ease_in_out(t):
    t = min(max(t, 0.0), 1.0)
    return 3 * t * t - 2 * t * t * t


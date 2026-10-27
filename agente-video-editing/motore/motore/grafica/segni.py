"""I segni sopra il girato: la grammatica di Dan Martell.

| tipo | cosa |
|---|---|
| `parola` | la parola chiave sbatte accanto a lei: arriva grande, una passata di evidenziatore menta le scorre sotto, la camera prende il colpo |
| `cerchio` | un cerchio a pennarello che si disegna attorno a una cosa nel set (`dove`) |
| `riquadro` | un riquadro a pennarello, un po' storto, attorno a `dove` |
| `freccia` | una freccia curva che parte dall'etichetta e arriva su `dove` |

Il pennarello e un TRATTO, non un font: le scritte restano Montserrat e Plex Mono.
Il tratto trema come quello di una mano (rumore fisso per segno, non per frame:
un segno che vibra a ogni fotogramma sembra un errore) e si disegna nel tempo.

`dove` e in coordinate della SORGENTE, da 0 a 1 (`./mve griglia` le mostra): il
segno segue il taglio di camera di ogni pezzo e la spinta, e resta sulla cosa.
"""
import math

import numpy as np
from PIL import Image, ImageDraw

from .. import stile as S
from .base import sans, mono, testo, tracked_width, fade_paste, scala_px, Tela, _cl

T_DISEGNO = 0.55        # quanto ci mette il pennarello a chiudere il segno
T_USCITA = 0.30
TRATTO = 10              # spessore del pennarello a 1080p


def _tremito(n, seme, ampiezza):
    """rumore liscio e fisso: la mano che trema, uguale in ogni fotogramma"""
    rng = np.random.default_rng(seme)
    k = rng.normal(0, 1, 7)
    x = np.linspace(0, 1, n)
    out = np.zeros(n)
    for i, a in enumerate(k):
        out += a * np.sin(2 * math.pi * (i + 1) * x + rng.uniform(0, 6.28)) / (i + 1)
    return out * ampiezza / max(1e-6, np.abs(out).max())


def tratto_cerchio(cx, cy, rx, ry, seme):
    """un giro e un pezzo: il pennarello supera il punto di partenza, come a mano"""
    n = 90
    a0 = -2.2
    ang = a0 + np.linspace(0, 2 * math.pi * 1.12, n)
    j = _tremito(n, seme, 0.06)
    # la seconda parte del giro scivola un poco verso l'esterno
    r = 1 + j + np.linspace(0, 0.07, n)
    return [(cx + rx * r[i] * math.cos(ang[i]), cy + ry * r[i] * math.sin(ang[i])) for i in range(n)]


def tratto_riquadro(x0, y0, x1, y1, seme):
    rng = np.random.default_rng(seme)
    w, h = x1 - x0, y1 - y0
    d = lambda: rng.uniform(-0.035, 0.035)
    pts = [(x0 + w * d(), y0 + h * d()), (x1 + w * d(), y0 + h * d()), (x1 + w * d(), y1 + h * d()),
           (x0 + w * d(), y1 + h * d()), (x0 + w * (0.10 + d()), y0 + h * (0.06 + d()))]
    out = []
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        for k in range(18):
            q = k / 18
            out.append((ax + (bx - ax) * q, ay + (by - ay) * q))
    out.append(pts[-1])
    j = _tremito(len(out), seme + 1, 3.0)
    return [(x + j[i], y - j[i] * 0.6) for i, (x, y) in enumerate(out)]


def tratto_freccia(ax, ay, bx, by, seme):
    """curva da (ax, ay) a (bx, by), con la pancia di lato; torna anche le due alette"""
    n = 40
    mx, my = (ax + bx) / 2, (ay + by) / 2
    L = math.hypot(bx - ax, by - ay)
    nx, ny = -(by - ay) / max(1, L), (bx - ax) / max(1, L)
    piega = 0.22 * L * (1 if seme % 2 else -1)
    cx, cy = mx + nx * piega, my + ny * piega
    j = _tremito(n, seme, 2.5)
    pts = []
    for i in range(n):
        q = i / (n - 1)
        x = (1 - q) ** 2 * ax + 2 * (1 - q) * q * cx + q * q * bx
        y = (1 - q) ** 2 * ay + 2 * (1 - q) * q * cy + q * q * by
        pts.append((x + j[i] * nx, y + j[i] * ny))
    # le alette: indietro dalla punta, a +-28 gradi dalla direzione d'arrivo
    dx, dy = pts[-1][0] - pts[-4][0], pts[-1][1] - pts[-4][1]
    a = math.atan2(dy, dx)
    lung = min(46, L * 0.25)
    ali = [[(bx, by), (bx - lung * math.cos(a + s * 0.5), by - lung * math.sin(a + s * 0.5))] for s in (1, -1)]
    return pts, ali


def disegna_tratto(im, pts, p, col=S.MINT, w=TRATTO, alpha=255):
    """il tratto fino alla frazione p della sua lunghezza, con un'ombra navy per
    staccare dal girato chiaro"""
    if p <= 0 or len(pts) < 2:
        return
    seg = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    tot = sum(seg)
    lim, acc, out = tot * min(1.0, p), 0.0, [pts[0]]
    for (a, b), L in zip(zip(pts, pts[1:]), seg):
        if acc + L >= lim:
            q = (lim - acc) / max(1e-6, L)
            out.append((a[0] + (b[0] - a[0]) * q, a[1] + (b[1] - a[1]) * q))
            break
        out.append(b)
        acc += L
    if len(out) < 2:
        return
    x0 = min(x for x, _ in out) - w * 3
    y0 = min(y for _, y in out) - w * 3
    x1 = max(x for x, _ in out) + w * 3
    y1 = max(y for _, y in out) + w * 3
    t = Tela(x1 - x0, y1 - y0)
    loc = [(x - x0, y - y0) for x, y in out]
    t.linea([(x + 2, y + 4) for x, y in loc], S.NAVY_DEEP + (110,), w + 4)
    t.linea(loc, col + (255,), w)
    fade_paste(im, t.fine(), (x0, y0), alpha)


# ------------------------------------------------------------------- parola
class Parola:
    """la parola che sbatte: evidenziatore menta, scritta navy, colpo di camera"""
    MAXW = 540

    def __init__(self, c):
        self.c = c
        txt = c['testo'].upper()
        size = c.get('corpo', 150)
        while size > 70 and tracked_width(sans(size, 900), txt, -0.035 * size) > self.MAXW:
            size -= 6
        self.size = size
        f = sans(size, 900)
        self.sp, self.pad = testo(txt, f, S.NAVY_DEEP + (255,), -0.035 * size, top=-int(size * 0.12))
        self.tw = tracked_width(f, txt, -0.035 * size)
        self.w = int(self.tw + 60)
        self.h = int(size * 1.25)
        # l'evidenziatore: un nastro a bordi irregolari, un poco inclinato
        hw, hh = self.w, int(size * 0.98)
        rng = np.random.default_rng(len(txt) * 31 + size)
        sup = [(x, 6 + rng.uniform(-5, 5)) for x in np.linspace(0, hw, 14)]
        inf = [(x, hh - 6 + rng.uniform(-5, 5)) for x in np.linspace(hw, 0, 14)]
        t = Tela(hw, hh)
        t.poligono(sup + inf, fill=S.MINT + (255,))
        self.nastro = t.fine().rotate(-1.6, Image.BICUBIC, expand=True)
        self.etichetta = None
        if c.get('eyebrow'):
            self.etichetta = testo(c['eyebrow'], mono(32), S.PAPER + (255,), 0.22 * 32, ombra=4)

    def misura(self):
        return self.w, self.h + (44 if self.etichetta else 0)

    def colpo(self):
        """istante in cui la parola atterra (la camera prende il colpo)"""
        return self.c['s'] + 0.20

    def disegna(self, im, t):
        c = self.c
        tl = t - c['s']
        if tl < 0 or t >= c['e']:
            return
        a = _cl((c['e'] - t) / T_USCITA)
        x0 = S.SAFE if c.get('side', 'left') == 'left' else S.W - S.SAFE - self.w
        y0 = S.CARD_TOP + 90
        if self.etichetta:
            sp, pad = self.etichetta
            fade_paste(im, sp, (x0 + 10 - pad, y0 - 50 - pad), int(255 * a * _cl(tl / 0.2)))
        # la passata di evidenziatore, da sinistra a destra
        pn = S.ease_out_cubic((tl - 0.04) / 0.22)
        if pn > 0:
            n = self.nastro
            wn = max(1, int(n.width * pn))
            fade_paste(im, n.crop((0, 0, wn, n.height)), (x0 - 10, y0 + self.size * 0.10), int(240 * a))
        # la parola arriva da piu vicino e sbatte
        q = _cl((tl - 0.06) / 0.14)
        if q > 0:
            k = 1.55 - 0.55 * S.ease_out_cubic(q)
            sp = scala_px(self.sp, k)
            cx, cy = x0 + 30 + self.tw / 2, y0 + self.size * 0.62
            fade_paste(im, sp, (cx - sp.width / 2, cy - sp.height / 2), int(255 * a * min(1, q * 1.6)))


# -------------------------------------------------------- segni sul set
class Marca:
    """cerchio, riquadro, freccia su un punto della sorgente; etichetta mono accanto"""

    def __init__(self, c):
        self.c = c
        self.seme = int(c['s'] * 1000) % 9973
        self.etichetta = None
        if c.get('testo'):
            self.etichetta = testo(c['testo'].upper(), sans(46, 900), S.PAPER + (255,), -0.02 * 46, ombra=6)

    def disegna(self, im, t, mappa):
        """`mappa(u, v) -> (x, y)` porta la sorgente nel quadro d'uscita di questo fotogramma"""
        c = self.c
        tl = t - c['s']
        if tl < 0 or t >= c['e']:
            return
        a = int(255 * _cl((c['e'] - t) / T_USCITA))
        p = S.ease_in_out(tl / T_DISEGNO)
        d = c['dove']
        if len(d) == 4:
            (x0, y0), (x1, y1) = mappa(d[0], d[1]), mappa(d[2], d[3])
        else:
            cx, cy = mappa(d[0], d[1])
            r = c.get('raggio', 110)
            x0, y0, x1, y1 = cx - r, cy - r, cx + r, cy + r
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        tipo = c['tipo']
        if tipo == 'cerchio':
            disegna_tratto(im, tratto_cerchio(cx, cy, (x1 - x0) / 2 * 1.12, (y1 - y0) / 2 * 1.12, self.seme), p, alpha=a)
        elif tipo == 'riquadro':
            disegna_tratto(im, tratto_riquadro(x0 - 14, y0 - 14, x1 + 14, y1 + 14, self.seme), p, alpha=a)
        # l'etichetta sta dove dice `etichetta` (default: sopra a sinistra), la freccia parte da li
        if self.etichetta:
            sp, pad = self.etichetta
            ex, ey = c.get('etichetta_dove') and mappa(*c['etichetta_dove']) or (x0 - 40 - sp.width, y0 - 140)
            ex = min(max(S.SAFE, ex), S.W - S.SAFE - sp.width)
            ey = min(max(S.SAFE, ey), S.H - 200)
            q = _cl((tl - (0.0 if tipo == 'freccia' else T_DISEGNO * 0.7)) / 0.25)
            fade_paste(im, sp, (ex - pad, ey - pad + (1 - q) * 10), int(a * q))
            if tipo == 'freccia':
                ax = ex + sp.width / 2
                ay = ey + sp.height - pad + 14
                # la punta si ferma prima della cosa, non ci finisce sopra
                L = math.hypot(cx - ax, cy - ay)
                k = max(0.0, (L - (x1 - x0) * 0.55) / max(1, L))
                pts, ali = tratto_freccia(ax, ay, ax + (cx - ax) * k, ay + (cy - ay) * k, self.seme)
                pf = S.ease_in_out((tl - 0.15) / T_DISEGNO)
                disegna_tratto(im, pts, pf, alpha=a)
                if pf >= 1:
                    pa = _cl((tl - 0.15 - T_DISEGNO) / 0.12)
                    for al in ali:
                        disegna_tratto(im, al, pa, alpha=a)


TIPI = {'parola': Parola, 'cerchio': Marca, 'riquadro': Marca, 'freccia': Marca}


def crea(c):
    if c['tipo'] not in TIPI:
        raise SystemExit(f"tipo di segno sconosciuto: «{c['tipo']}» (tipi: {', '.join(TIPI)})")
    return TIPI[c['tipo']](c)


def misura(c):
    """quanto spazio occupa la parola accanto a lei: `inquadra` sceglie il lato"""
    return Parola(c).misura()

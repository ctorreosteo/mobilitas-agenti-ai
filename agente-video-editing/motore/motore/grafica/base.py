"""Le primitive di disegno della grafica: font, testo con contorno e ombra,
incolla con alfa, scrittura a macchina, lettere che cadono, icone, vetro.

Le usano il renderer del video (`render`), le infografiche (`info`), gli Shorts
e le miniature. Niente qui sa cosa sia un video: solo come si disegna.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .. import stile as S

_fonts = {}


def sans(size, weight=900):
    k = ('s', size, weight)
    if k not in _fonts:
        f = ImageFont.truetype(S.FONT_SANS, size)
        f.set_variation_by_axes([weight])
        _fonts[k] = f
    return _fonts[k]


def mono(size):
    k = ('m', size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(S.FONT_MONO, size)
    return _fonts[k]


def tracked_width(font, text, track_px):
    return sum(font.getlength(c) for c in text) + track_px * max(0, len(text) - 1)


def draw_tracked(d, xy, text, font, fill, track_px, stroke=0, stroke_fill=None):
    x, y = xy
    for c in text:
        if stroke:
            d.text((x, y), c, font=font, fill=stroke_fill, stroke_width=stroke, stroke_fill=stroke_fill)
        else:
            d.text((x, y), c, font=font, fill=fill)
        x += font.getlength(c) + track_px
    return x


def char_x(font, text, track_px):
    """ascissa d'inizio di ogni carattere, piu la fine: per scrivere a macchina"""
    xs, x = [], 0.0
    for c in text:
        xs.append(x)
        x += font.getlength(c) + track_px
    return xs + [x - track_px]


def rounded(size, radius, fill):
    im = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=fill)
    return im


def wrap_to(font, text, track, maxw):
    lines, cur = [], ''
    for word in text.split():
        t = (cur + ' ' + word).strip()
        if tracked_width(font, t, track) > maxw and cur:
            lines.append(cur)
            cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def testo(text, font, fill, track=0.0, stroke=0, stroke_fill=None, ombra=0, top=0):
    """sprite di una scritta con contorno e ombra morbida; il testo parte da (pad, pad + top)"""
    pad = stroke + ombra * 2 + 4
    asc, desc = font.getmetrics()
    w = int(tracked_width(font, text, track)) + 2 * pad + 2
    h = asc + desc + 2 * pad
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if stroke:
        draw_tracked(d, (pad, pad + top), text, font, None, track, stroke, stroke_fill)
    draw_tracked(d, (pad, pad + top), text, font, fill, track)
    if ombra:
        sh = Image.new('RGBA', (w, h), S.NAVY_DEEP + (0,))
        a = im.getchannel('A').filter(ImageFilter.GaussianBlur(ombra)).point(lambda v: v * 150 // 255)
        sh.putalpha(a)
        out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        out.alpha_composite(sh, (0, max(1, ombra // 2)))
        out.alpha_composite(im)
        im = out
    return im, pad


def bagliore(sprite, raggio, colore, forza=1.0):
    """alone di un colore attorno a uno sprite (non e un gradient sul testo: sta sotto)"""
    pad = raggio * 2
    w, h = sprite.width + 2 * pad, sprite.height + 2 * pad
    a = Image.new('L', (w, h), 0)
    a.paste(sprite.getchannel('A'), (pad, pad))
    a = a.filter(ImageFilter.GaussianBlur(raggio)).point(lambda v: min(255, int(v * 1.6 * forza)))
    g = Image.new('RGBA', (w, h), colore + (0,))
    g.putalpha(a)
    return g, pad


def fade_paste(base, sprite, box, alpha):
    if alpha <= 2:
        return
    if alpha >= 253:
        base.alpha_composite(sprite, (int(box[0]), int(box[1])))
        return
    a = sprite.getchannel('A').point(lambda v: v * alpha // 255)
    s = sprite.copy()
    s.putalpha(a)
    base.alpha_composite(s, (int(box[0]), int(box[1])))


def paste_clip(base, sprite, box, alpha=255):
    """incolla anche se lo sprite esce dal quadro (alpha_composite non lo accetta)"""
    x, y = int(box[0]), int(box[1])
    x0, y0 = max(0, -x), max(0, -y)
    x1, y1 = min(sprite.width, base.width - x), min(sprite.height, base.height - y)
    if x1 <= x0 or y1 <= y0:
        return
    if (x0, y0, x1, y1) != (0, 0, sprite.width, sprite.height):
        sprite = sprite.crop((x0, y0, x1, y1))
    fade_paste(base, sprite, (x + x0, y + y0), alpha)


def scala_px(sprite, k):
    if abs(k - 1) < 0.01:
        return sprite
    return sprite.resize((max(1, int(sprite.width * k)), max(1, int(sprite.height * k))), Image.BILINEAR)


def _cl(t):
    return min(max(t, 0.0), 1.0)


class Macchina:
    """etichetta mono che si scrive a macchina, con il cursore che lampeggia"""

    def __init__(self, text, font, color, track):
        self.sp, self.pad = testo(text, font, color + (255,), track)
        self.xs = char_x(font, text, track)
        self.n = len(text)
        self.h = font.size
        self.color = color

    def disegna(self, dst, xy, tl, alpha=255, cursore=True):
        k = min(self.n, max(0, int(tl / S.TYPE_CHAR) + 1)) if tl >= 0 else 0
        if k <= 0:
            return
        wx = int(self.pad + self.xs[k]) if k < self.n else self.sp.width
        fade_paste(dst, self.sp.crop((0, 0, wx, self.sp.height)), (xy[0] - self.pad, xy[1] - self.pad), alpha)
        fine = self.n * S.TYPE_CHAR
        if cursore and tl < fine + 0.5 and (tl < fine or int(tl * 6) % 2 == 0):
            x = xy[0] + (self.xs[k] if k < self.n else self.xs[-1]) + 4
            ImageDraw.Draw(dst).rectangle([x, xy[1] + 2, x + int(self.h * 0.42), xy[1] + self.h],
                                          fill=self.color + (min(255, alpha),))


class Lettere:
    """una riga che entra lettera per lettera: ogni lettera sale dal basso e
    atterra con un piccolo rimbalzo. Finito l'ingresso si usa la riga intera."""

    def __init__(self, text, font, color, track, top_off):
        self.text, self.font = text, font
        h = int(font.size * 1.32)
        pad = 6
        self.chars = []
        x = 0.0
        for c in text:
            cw = font.getlength(c)
            if c.strip():
                im = Image.new('RGBA', (int(cw) + 2 * pad + 2, h), (0, 0, 0, 0))
                ImageDraw.Draw(im).text((pad, top_off), c, font=font, fill=color + (255,))
                self.chars.append((im, x - pad))
            x += cw + track
        self.w = x - track
        self.riga = Image.new('RGBA', (int(self.w) + 2 * pad + 2, h), (0, 0, 0, 0))
        draw_tracked(ImageDraw.Draw(self.riga), (pad, top_off), text, font, color + (255,), track)
        self.pad = pad
        self.passo = min(S.BEHIND_CHAR, 0.5 / max(1, len(self.chars)))
        self.fine = self.passo * len(self.chars) + S.BEHIND_DROP

    def disegna(self, dst, xy, tl, alpha=255, caduta=None):
        caduta = caduta if caduta is not None else self.font.size * 0.7
        x0, y0 = xy
        if tl >= self.fine:
            paste_clip(dst, self.riga, (x0 - self.pad, y0), alpha)
            return
        for i, (im, dx) in enumerate(self.chars):
            p = (tl - i * self.passo) / S.BEHIND_DROP
            if p <= 0:
                break
            dy = (1 - S.ease_out_back(p)) * caduta
            paste_clip(dst, im, (x0 + dx, y0 + dy), int(alpha * _cl(p * 2.2)))




# ------------------------------------------------------------------- icone
_mappa_icone = None


def font_icone(size, pieno=0, peso=500):
    k = ('i', size, pieno, peso)
    if k not in _fonts:
        f = ImageFont.truetype(S.FONT_ICONE, size)
        f.set_variation_by_axes([pieno, 0, min(48, max(20, size)), peso])
        _fonts[k] = f
    return _fonts[k]


_icone_cache = {}


def icona(nome, size, colore, pieno=0, peso=500):
    """un'icona Material Symbols centrata in un quadrato size x size"""
    global _mappa_icone
    k = (nome, size, colore, pieno, peso)
    if k in _icone_cache:
        return _icone_cache[k]
    if _mappa_icone is None:
        _mappa_icone = dict(l.split() for l in open(S.ICONE, encoding='utf-8') if l.strip())
    if nome not in _mappa_icone:
        raise SystemExit(f"icona «{nome}» non c'e nel sottoinsieme (risorse/icone.txt): "
                         f"vedi risorse/fonts/MaterialSymbols-LICENZA.txt per aggiungerla")
    f = font_icone(size, pieno, peso)
    tmp = Image.new('RGBA', (size * 2, size * 2), (0, 0, 0, 0))
    ImageDraw.Draw(tmp).text((size // 2, size // 2), chr(int(_mappa_icone[nome], 16)), font=f,
                             fill=tuple(colore[:3]) + (colore[3] if len(colore) > 3 else 255,))
    bb = tmp.getbbox()
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    if bb:
        g = tmp.crop(bb)
        im.alpha_composite(g, ((size - g.width) // 2, (size - g.height) // 2))
    _icone_cache[k] = im
    return im


# ----------------------------------------------------------- disegno vettoriale
class Tela:
    """disegno sovracampionato (k volte) e poi ridotto: linee e archi senza scalini"""

    def __init__(self, w, h, k=2):
        self.w, self.h, self.k = int(w), int(h), k
        self.im = Image.new('RGBA', (self.w * k, self.h * k), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def _p(self, pts):
        return [(x * self.k, y * self.k) for x, y in pts]

    def linea(self, pts, col, w, tondi=True):
        pts = self._p(pts)
        self.d.line(pts, fill=col, width=max(1, int(w * self.k)), joint='curve')
        if tondi:
            r = w * self.k / 2
            for x, y in (pts[0], pts[-1]):
                self.d.ellipse([x - r, y - r, x + r, y + r], fill=col)

    def tratteggio(self, a, b, col, w, pieno=10, vuoto=8):
        (x0, y0), (x1, y1) = a, b
        L = math.hypot(x1 - x0, y1 - y0)
        if L < 1:
            return
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        s = 0.0
        while s < L:
            e = min(L, s + pieno)
            self.linea([(x0 + ux * s, y0 + uy * s), (x0 + ux * e, y0 + uy * e)], col, w, tondi=False)
            s += pieno + vuoto

    def cerchio(self, cx, cy, r, fill=None, outline=None, w=1):
        k = self.k
        self.d.ellipse([(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k], fill=fill, outline=outline,
                       width=max(1, int(w * k)))

    def arco(self, cx, cy, r, a0, a1, col, w, tondi=True):
        """gradi alla maniera di Pillow: 0 = ore 3, senso orario"""
        if a1 - a0 < 0.3:
            return
        k = self.k
        self.d.arc([(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k], a0, a1, fill=col,
                   width=max(1, int(w * k)))
        if tondi:
            for a in (a0, a1):
                x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
                self.cerchio(x, y, w / 2 - 0.3, fill=col)

    def spicchio(self, cx, cy, r, a0, a1, col):
        k = self.k
        if a1 - a0 > 0.3:
            self.d.pieslice([(cx - r) * k, (cy - r) * k, (cx + r) * k, (cy + r) * k], a0, a1, fill=col)

    def poligono(self, pts, fill=None, outline=None, w=1):
        self.d.polygon(self._p(pts), fill=fill)
        if outline:
            self.linea(list(pts) + [pts[0]], outline, w, tondi=False)

    def rett(self, x0, y0, x1, y1, r, fill=None, outline=None, w=1):
        k = self.k
        self.d.rounded_rectangle([x0 * k, y0 * k, x1 * k, y1 * k], radius=r * k, fill=fill, outline=outline,
                                 width=max(1, int(w * k)))

    def fine(self):
        return self.im.resize((self.w, self.h), Image.LANCZOS)


def curva_liscia(pts, n=16):
    """Catmull-Rom: una curva morbida che passa per tutti i punti"""
    if len(pts) < 3:
        return list(pts)
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            t = j / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[a]) + (-p0[a] + p2[a]) * t + (2 * p0[a] - 5 * p1[a] + 4 * p2[a] - p3[a]) * t2
                                    + (-p0[a] + 3 * p1[a] - 3 * p2[a] + p3[a]) * t3) for a in (0, 1)))
    out.append(pts[-1])
    return out


# --------------------------------------------------------------------- vetro
_ombre, _bordi, _maschere = {}, {}, {}


def _maschera(w, h, r):
    k = (w, h, r)
    if k not in _maschere:
        if len(_maschere) > 300:
            _maschere.clear()
        m = Image.new('L', (w * 2, h * 2), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w * 2 - 1, h * 2 - 1], radius=r * 2, fill=255)
        _maschere[k] = m.resize((w, h), Image.LANCZOS)
    return _maschere[k]


def ombra_pannello(w, h, r):
    k = (w, h, r)
    if k not in _ombre:
        if len(_ombre) > 60:
            _ombre.clear()
        P = 44
        a = Image.new('L', (w + 2 * P, h + 2 * P), 0)
        ImageDraw.Draw(a).rounded_rectangle([P, P, P + w, P + h], radius=r, fill=S.VETRO_OMBRA)
        im = Image.new('RGBA', a.size, S.NAVY_DEEP + (0,))
        im.putalpha(a.filter(ImageFilter.GaussianBlur(18)))
        _ombre[k] = (im, P)
    return _ombre[k]


def bordo_pannello(w, h, r):
    """filo di luce: piu chiaro in alto, quasi spento in basso; e un angolo menta"""
    k = (w, h, r)
    if k not in _bordi:
        if len(_bordi) > 300:
            _bordi.clear()
        t = Tela(w, h)
        t.rett(1, 1, w - 1, h - 1, r, outline=S.PAPER + (255,), w=1.6)
        im = t.fine()
        grad = np.linspace(90, 14, h).astype(np.float32)[:, None]
        a = np.asarray(im.getchannel('A'), np.float32) * grad / 255
        im.putalpha(Image.fromarray(a.astype(np.uint8), 'L'))
        d = ImageDraw.Draw(im)
        d.line([(r, 1), (min(w - r, r + 64), 1)], fill=S.MINT + (230,), width=3)
        _bordi[k] = im
    return _bordi[k]


def vetro(base, box, r=None, alpha=255, video=True):
    """pannello di vetro smerigliato su `base`: il fotogramma sotto sfocato e velato
    di navy, ombra morbida, filo di luce. Senza video (livello trasparente) e un
    pannello navy pieno."""
    r = S.VETRO_RAGGIO if r is None else r
    x, y, w, h = (int(round(v)) for v in box)
    if w < 4 or h < 4 or alpha <= 2:
        return
    om, P = ombra_pannello(w, h, r)
    paste_clip(base, om, (x - P, y - P + 14), int(alpha * 0.9))
    m = _maschera(w, h, min(r, w // 2))
    if alpha < 253:
        m = m.point(lambda v: v * alpha // 255)
    if video:
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(base.width, x + w), min(base.height, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        reg = base.crop((x0, y0, x1, y1)).convert('RGB')
        rw, rh = reg.size
        sm = reg.resize((max(1, rw // 8), max(1, rh // 8)), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2.2))
        sm = sm.resize((rw, rh), Image.BILINEAR)
        tinta = Image.blend(sm, Image.new('RGB', (rw, rh), S.NAVY), S.VETRO_VELO)
        base.paste(tinta, (x0, y0), m.crop((x0 - x, y0 - y, x1 - x, y1 - y)))
    else:
        piena = Image.new('RGBA', (w, h), S.NAVY + (0,))
        piena.putalpha(m.point(lambda v: v * 238 // 255))
        paste_clip(base, piena, (x, y))
    paste_clip(base, bordo_pannello(w, h, min(r, w // 2)), (x, y), alpha)

"""Le scene a tutto schermo: lo stacco animato, alla maniera di Claude Motion, ma
generato dal motore e sincronizzato alla voce.

Una scena copre il quadro per 4-8 s: la camera entra nel video, il video si
sfoca e si vela di navy (lei continua a muoversi dietro il vetro), e la sua
frase diventa la protagonista. Poi si torna nel video. La voce non si ferma mai.

| tipo | cosa |
|---|---|
| `parole` | tipografia cinetica: ogni parola esplode quando la dice; `chiave` in menta, `effetti` per parola: `spegne`, `barra`, `sottolinea` |
| `numero` | numero eroe che conta (da 0 o da `prima`), con `grafico`: `anello`, `punti`, `barra` |
| `confronto` | schermo diviso: due `voci` che entrano quando le dice, `segno` si/no, barre proporzionali da `misura` |

Regola di sempre: le parole a schermo sono le sue.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .. import stile as S
from .base import (sans, mono, tracked_width, testo, bagliore, fade_paste, paste_clip, scala_px, Macchina,
                   Tela, icona, _cl)
from .info import conta, _numeri, pop
from .piano import norm

T_IN, T_OUT = 0.5, 0.45


def _sfocato(base):
    """il video dietro il vetro: rimpicciolito, sfocato, velato di navy"""
    sm = base.convert('RGB').resize((160, 90), Image.BILINEAR).filter(ImageFilter.GaussianBlur(2.5))
    sm = sm.resize((S.W, S.H), Image.BICUBIC)
    return Image.blend(sm, Image.new('RGB', (S.W, S.H), S.NAVY_DEEP), 0.80).convert('RGBA')


def _zoom(im, z, cy=0.45):
    if z <= 1.0005:
        return im
    w, h = int(S.W / z), int(S.H / z)
    x0, y0 = (S.W - w) // 2, int((S.H - h) * cy)
    return im.crop((x0, y0, x0 + w, y0 + h)).resize((S.W, S.H), Image.BILINEAR)


_FONDO = {}


def _fondo_vivo():
    """bagliore menta e griglia di punti: si disegnano una volta, poi derivano"""
    if not _FONDO:
        y, x = np.ogrid[:S.H, :S.W]
        r = np.sqrt(((x - S.W * 0.5) / (S.W * 0.42)) ** 2 + ((y - S.H * 0.5) / (S.H * 0.55)) ** 2)
        a = (np.clip(1 - r, 0, 1) ** 2.2 * 46).astype(np.uint8)
        g = Image.new('RGBA', (S.W, S.H), S.MINT + (0,))
        g.putalpha(Image.fromarray(a, 'L'))
        _FONDO['glow'] = g.resize((int(S.W * 1.3), int(S.H * 1.3)), Image.BILINEAR)
        P = 48
        dots = Image.new('RGBA', (S.W + P * 2, S.H + P * 2), (0, 0, 0, 0))
        d = ImageDraw.Draw(dots)
        for yy in range(0, S.H + P * 2, P):
            for xx in range(0, S.W + P * 2, P):
                d.ellipse([xx - 1.6, yy - 1.6, xx + 1.6, yy + 1.6], fill=S.PAPER + (26,))
        _FONDO['punti'] = (dots, P)
        rr = np.sqrt(((x - S.W / 2) / (S.W / 2)) ** 2 + ((y - S.H / 2) / (S.H / 2)) ** 2)
        v = (np.clip((rr - 0.6) / 0.8, 0, 1) ** 1.5 * 200).astype(np.uint8)
        vi = Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (0,))
        vi.putalpha(Image.fromarray(v, 'L'))
        _FONDO['vign'] = vi
    return _FONDO


class Scena:
    """la parte comune: fondo vivo, ingresso e uscita attraverso il video"""

    def __init__(self, c):
        self.c = c
        self.s, self.e = c['s'], c['e']
        self.costruisci()

    def costruisci(self):
        pass

    def contenuto(self, im, tl):
        pass

    def attiva(self, t):
        return self.s <= t < self.e

    def componi(self, base, t, video=True):
        tl = t - self.s
        F = _fondo_vivo()
        fondo = _sfocato(base) if video else Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (255,))
        # il fondo respira: il bagliore deriva, la griglia scorre piano
        gx = -S.W * 0.15 + math.sin(tl * 0.7) * 60
        gy = -S.H * 0.15 + math.cos(tl * 0.5) * 40
        paste_clip(fondo, F['glow'], (gx, gy))
        dots, P = F['punti']
        off = int(tl * 14) % P
        fondo.alpha_composite(dots.crop((off, off, off + S.W, off + S.H)))
        lay = Image.new('RGBA', (S.W, S.H), (0, 0, 0, 0))
        self.contenuto(lay, tl)
        # la camera deriva dentro la scena
        lay = _zoom(lay, 1.0 + 0.025 * _cl(tl / max(1.0, self.e - self.s)), 0.5)
        fondo.alpha_composite(lay)
        fondo.alpha_composite(F['vign'])
        # a inizio video non c'e un video da cui entrare: la scena parte gia piena
        q_in = 1.0 if self.s < 0.05 else S.ease_in_out(_cl(tl / T_IN))
        q_out = S.ease_in_out(_cl((self.e - t) / T_OUT))
        if q_in < 1:
            # si entra nel video: zoomata e dissolvenza nel vetro, con un lampo menta
            z = _zoom(base, 1.0 + 0.22 * q_in)
            out = Image.blend(z, fondo, q_in)
            lampo = 1 - abs(q_in - 0.55) / 0.25
            if lampo > 0:
                out = Image.blend(out, Image.new('RGBA', (S.W, S.H), S.MINT + (255,)), 0.10 * lampo)
            return out
        if q_out < 1:
            # si torna nel video: la scena si allontana, il video atterra da un poco piu vicino
            z = _zoom(base, 1.0 + 0.10 * q_out)
            return Image.blend(z, fondo, q_out)
        return fondo


# ------------------------------------------------------------------- parole
class Parole(Scena):
    """La frase esplode parola per parola, a tutto schermo. Le righe gia dette si
    attenuano, la riga che sta dicendo resta piena; le parole `chiave` sono menta,
    con il loro `effetto`."""
    MAXW = 1560

    def costruisci(self):
        c = self.c
        words = c['testo'].split()
        tempi = c['parole_t']
        chiave = {norm(k) for k in c.get('chiave', [])}
        effetti = {norm(k): v for k, v in (c.get('effetti') or {}).items()}
        size = 168
        while True:
            f = sans(size, 900)
            tr = -0.03 * size
            sp = f.getlength(' ') + tr
            righe, cur, x = [], [], 0.0
            for i, wd in enumerate(words):
                ww = tracked_width(f, wd.upper(), tr)
                if cur and x + ww > self.MAXW:
                    righe.append(cur)
                    cur, x = [], 0.0
                cur.append((i, wd, ww))
                x += ww + sp
            righe.append(cur)
            if len(righe) <= 4 or size <= 80:
                break
            size -= 8
        self.size = size
        lh = int(size * 1.02)
        y0 = (S.H - len(righe) * lh) / 2 - size * 0.06
        self.parole = []
        for li, r in enumerate(righe):
            wtot = sum(w for _, _, w in r) + sp * (len(r) - 1)
            x = (S.W - wtot) / 2
            for i, wd, ww in r:
                k = norm(wd)
                col = S.MINT if k in chiave or k in effetti else S.PAPER
                spr, pad = testo(wd.upper(), f, col + (255,), tr, top=-int(size * 0.12))
                g = bagliore(spr, 22, S.MINT, 0.7) if col == S.MINT else None
                self.parole.append({'t': tempi[i], 'x': x, 'y': y0 + li * lh, 'w': ww, 'sp': spr, 'pad': pad,
                                    'riga': li, 'eff': effetti.get(k), 'glow': g, 'chiave': col == S.MINT})
                x += ww + sp
        self.inizio_riga = {}
        for p in self.parole:
            self.inizio_riga.setdefault(p['riga'], p['t'])
        if c.get('eyebrow'):
            self.eye = Macchina(c['eyebrow'], mono(30), S.MINT, 0.2 * 30)
            self.eye_y = y0 - 70
        else:
            self.eye = None

    def contenuto(self, im, tl):
        d = ImageDraw.Draw(im)
        if self.eye:
            ew = self.eye.sp.width
            self.eye.disegna(im, ((S.W - ew) / 2, self.eye_y), tl - 0.3, cursore=False)
        # la riga che sta dicendo: l'ultima iniziata
        riga_ora = max([r for r, t0 in self.inizio_riga.items() if tl >= t0 - 0.05], default=0)
        for p in self.parole:
            u = tl - p['t'] + 0.06
            if u < 0:
                continue
            q = _cl(u / 0.24)
            k = 1.35 - 0.35 * S.ease_out_back(q)              # arriva grande e si posa
            a = min(1.0, q * 2.2)
            if p['riga'] < riga_ora:
                a *= 0.5
            if p['eff'] == 'spegne' and u > 0.3:
                # la parola si spegne: un tremolio, poi resta fioca
                v = (u - 0.3) / 0.45
                a *= 0.16 if v >= 1 else (0.2 if int(v * 8) % 2 else 1.0) * (1 - 0.7 * v)
            sp = p['sp']
            s2 = scala_px(sp, k)
            cx, cy = p['x'] + p['w'] / 2, p['y'] + self.size * 0.55
            if p['glow'] and 0 < u < 0.9 and p['eff'] != 'spegne':
                g, gp = p['glow']
                fade_paste(im, g, (p['x'] - p['pad'] - gp, p['y'] - p['pad'] - gp), int(200 * (1 - u / 0.9)))
            fade_paste(im, s2, (cx - s2.width / 2, cy - s2.height / 2 + (1 - q) * 18), int(255 * a))
            if p['eff'] == 'barra' and u > 0.35:
                pb = S.ease_out_cubic((u - 0.35) / 0.3)
                yb = p['y'] + self.size * 0.50
                d.rounded_rectangle([p['x'] - 8, yb - 7, p['x'] - 8 + (p['w'] + 16) * pb, yb + 7], radius=7,
                                    fill=S.PAPER + (int(240 * a),))
            if p['eff'] == 'sottolinea' and u > 0.3:
                pb = S.ease_out_expo((u - 0.3) / 0.45)
                yb = p['y'] + self.size * 0.86
                d.rounded_rectangle([p['x'], yb, p['x'] + p['w'] * pb, yb + 12], radius=6, fill=S.MINT + (int(255 * a),))


# ------------------------------------------------------------------- numero
class Numero(Scena):
    """Il numero eroe: conta fino al valore (o scende da `prima`), gigante, con
    l'unita; sotto le sue parole (`testo`); a destra il grafico a scala di scena."""
    G = 420

    def costruisci(self):
        c = self.c
        self.f = sans(300, 900)
        self.vw = self.f.getlength(c['valore'])
        self.unit, self.up = testo(c.get('unita', ''), sans(120, 900), S.PAPER + (255,))
        g = c.get('grafico')
        self.graf = g
        larg = self.vw + 24 + self.unit.width + (self.G + 120 if g else 0)
        self.x0 = (S.W - larg) / 2
        self.y0 = 250
        self.nums = {}
        lab = c.get('testo', '')
        f_l = sans(54, 800)
        self.lab = []
        x = self.x0
        for wd in lab.split():
            sp, pad = testo(wd, f_l, S.PAPER + (255,))
            self.lab.append((sp, pad, x))
            x += f_l.getlength(wd + ' ')
        if c.get('eyebrow'):
            self.eye = Macchina(c['eyebrow'], mono(30), S.MINT, 0.2 * 30)
        else:
            self.eye = None
        fin, fp = self._num(c['valore'])
        self.glow = bagliore(fin, 30, S.MINT, 0.8)
        v = _numeri(c['valore'])
        self.v = v[-1] if v else 0.0
        self.vlo = v[0] if v else 0.0
        self.t_label = (c.get('voci') or [{}])[0].get('t', 1.4) if c.get('voci') else 1.4

    def _num(self, s):
        if s not in self.nums:
            self.nums[s] = testo(s, self.f, S.MINT + (255,), -6, top=-40)
        return self.nums[s]

    def contenuto(self, im, tl):
        c = self.c
        T0, D = 0.45, 1.4
        p = S.ease_out_expo((tl - T0) / D)
        if self.eye:
            self.eye.disegna(im, (self.x0 + 8, self.y0 - 60), tl - 0.35, cursore=False)
        if tl >= T0:
            s = c['valore'] if tl >= T0 + D else conta(c['valore'], p, c.get('prima'))
            sp, pad = self._num(s)
            g = (tl - T0 - D) / 0.7
            gl, gp = self.glow
            if g >= 0:
                fade_paste(im, gl, (self.x0 - pad - gp, self.y0 - pad - gp), int(90 + 150 * max(0.0, 1 - g)))
            fade_paste(im, sp, (self.x0 - pad, self.y0 - pad), int(255 * _cl((tl - T0) / 0.15)))
            pu = _cl((tl - T0 - D * 0.5) / 0.35)
            if pu > 0:
                u = scala_px(self.unit, pop(pu))
                fade_paste(im, u, (self.x0 + self.vw + 24 - self.up, self.y0 + 300 - 150 - self.up + self.unit.height - u.height),
                           int(255 * min(1, pu * 2)))
        for k, (sp, pad, x) in enumerate(self.lab):
            q = _cl((tl - self.t_label - k * 0.06) / 0.3)
            if q > 0:
                fade_paste(im, sp, (x - pad, self.y0 + 330 - pad + (1 - S.ease_out_cubic(q)) * 16), int(255 * q))
        if self.graf:
            gx = self.x0 + self.vw + 24 + self.unit.width + 120
            gy = self.y0 + 10
            pg = p if tl >= T0 else 0.0
            self._grafico(im, gx, gy, pg, _cl((tl - 0.3) / 0.4))

    def _grafico(self, im, x, y, p, a):
        G = self.G
        t = Tela(G, G)
        if self.graf == 'anello':
            r, lw = G / 2 - 24, 34
            t.arco(G / 2, G / 2, r, 0, 360, S.PAPER + (40,), lw, tondi=False)
            ang = 360 * min(1.0, self.v / 100 * p)
            if ang > 0.5:
                t.arco(G / 2, G / 2, r, -90, -90 + ang, S.MINT + (255,), lw)
        elif self.graf == 'punti':
            passo = G / 10
            rif = _numeri((self.c.get('riferimento') or {}).get('valore'))
            rif = rif[0] if rif else None
            for k in range(100):
                cx, cy = passo * (k % 10 + 0.5), passo * (k // 10 + 0.5)
                rr = passo * 0.34
                if k < self.v * p - 0.5:
                    t.cerchio(cx, cy, rr, fill=S.MINT + (255,))
                elif rif is not None and k < rif:
                    t.cerchio(cx, cy, rr - 2, outline=S.MINT + (200,), w=3)
                else:
                    t.cerchio(cx, cy, rr * 0.6, fill=S.PAPER + (40,))
        im_g = t.fine()
        if self.c.get('icona') and self.graf == 'anello':
            ic = icona(self.c['icona'], 150, S.MINT)
            im_g.alpha_composite(ic, ((G - 150) // 2, (G - 150) // 2))
        fade_paste(im, scala_px(im_g, 0.85 + 0.15 * S.ease_out_back(a)), (x, y), int(255 * a))


# ---------------------------------------------------------------- confronto
class Confronto(Scena):
    """Schermo diviso: `voci` (due) con `etichetta`, `testo` grande, `sotto`,
    `segno` si/no, `misura` per le barre proporzionali; ogni lato entra quando lo dice."""

    def costruisci(self):
        c = self.c
        self.lati = []
        mis = [float(v['misura']) for v in c['voci'] if v.get('misura') is not None]
        mx = max(mis) if mis else None
        for i, v in enumerate(c['voci'][:2]):
            cx = S.W * (0.27 if i == 0 else 0.73)
            size = 150
            while sans(size, 900).getlength(v['testo']) > S.W * 0.40 and size > 60:
                size -= 6
            big, bp = testo(v['testo'], sans(size, 900), ((S.MINT if v.get('segno') != 'no' else S.PAPER) + (255,)), -3,
                            top=-int(size * 0.12))
            sotto = testo(v['sotto'], sans(44, 700), S.MUTED + (255,)) if v.get('sotto') else None
            eti = Macchina(v.get('etichetta', ''), mono(30), S.MINT, 0.2 * 30)
            self.lati.append({'t': v.get('t', 0.5 + i * 1.5), 'cx': cx, 'big': (big, bp), 'size': size, 'sotto': sotto,
                              'eti': eti, 'segno': v.get('segno'), 'f': (float(v['misura']) / mx) if mx and v.get('misura') is not None else None})
        self.ic = {'si': icona('check', 64, S.NAVY_DEEP, peso=700), 'no': icona('close', 60, S.PAPER, peso=600)}

    def contenuto(self, im, tl):
        d = ImageDraw.Draw(im)
        # il divisore si disegna dall'alto
        pd = S.ease_out_expo((tl - T_IN) / 0.7)
        if pd > 0:
            d.rounded_rectangle([S.W / 2 - 2, 170, S.W / 2 + 2, 170 + (S.H - 340) * pd], radius=2, fill=S.MINT + (200,))
        for L in self.lati:
            u = tl - L['t']
            if u < -0.1:
                continue
            q = _cl(u / 0.35)
            cx = L['cx']
            y = 300
            L['eti'].disegna(im, (cx - L['eti'].sp.width / 2, y - 80), u, cursore=False)
            big, bp = L['big']
            b2 = scala_px(big, 1.3 - 0.3 * S.ease_out_back(q))
            fade_paste(im, b2, (cx - b2.width / 2, y + L['size'] * 0.5 - b2.height / 2), int(255 * min(1, q * 2)))
            yb = y + L['size'] + 40
            if L['segno'] in ('si', 'no'):
                pq = _cl((u - 0.3) / 0.3)
                if pq > 0:
                    r = 52 * pop(pq)
                    by = yb + 50
                    if L['segno'] == 'si':
                        d.ellipse([cx - r, by - r, cx + r, by + r], fill=S.MINT + (255,))
                    else:
                        d.ellipse([cx - r, by - r, cx + r, by + r], outline=S.PAPER + (220,), width=5)
                    ic = scala_px(self.ic[L['segno']], pop(pq))
                    fade_paste(im, ic, (cx - ic.width / 2, by - ic.height / 2), int(255 * min(1, pq * 2)))
                yb += 120
            if L['sotto']:
                sp, pad = L['sotto']
                fade_paste(im, sp, (cx - sp.width / 2, yb - pad), int(255 * _cl((u - 0.4) / 0.3)))
                yb += 70
            if L['f'] is not None:
                pb = S.ease_out_expo((u - 0.5) / 1.0)
                W_ = S.W * 0.36
                x0 = cx - W_ / 2
                d.rounded_rectangle([x0, yb + 20, x0 + W_, yb + 48], radius=14, fill=S.PAPER + (30,))
                L_ = max(28, W_ * L['f'] * pb) if pb > 0 else 0
                if L_:
                    d.rounded_rectangle([x0, yb + 20, x0 + L_, yb + 48], radius=14,
                                        fill=(S.MINT if L['segno'] != 'no' else S.PAPER) + (255,))


TIPI = {'parole': Parole, 'numero': Numero, 'confronto': Confronto}


def crea(c):
    tipo = c.get('tipo', 'parole')
    if tipo not in TIPI:
        raise SystemExit(f"tipo di scena sconosciuto: «{tipo}» (tipi: {', '.join(TIPI)})")
    return TIPI[tipo](c)

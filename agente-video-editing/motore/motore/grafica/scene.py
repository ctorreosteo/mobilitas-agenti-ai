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
| `passi` | il framework a passi (Martell): numeri che si accendono uno dopo l'altro, legati da un filo |
| `ciclo` | il circolo: nodi su un anello, frecce che si chiudono, poi una goccia di luce che gira |
| `matrice` | 2x2 con gli assi; i quadranti entrano quando li dice, `acceso` si riempie di menta |
| `piramide` | strati dal basso verso l'alto, l'ultimo detto acceso |
| `richiamo` | lo stesso framework che torna, breve, con acceso il pezzo di cui sta parlando |

Dove sta lei (`lei`):

- `dietro` (default): il video si sfoca dietro il vetro, la scena prende tutto il quadro;
- `finestra` (Martell): il quadro si rimpicciolisce in una finestra di lato e lei continua a parlare
  li dentro; la grafica prende il resto. Il volto non sparisce: la scena puo durare di piu;
- `davanti` (Gadzhi): lei esce dalla stanza. La sagoma resta in primo piano, scivola su un lato con
  un filo di luce menta, la grafica sta dietro e accanto a lei. Servono le sagome (`./mve sagome`).

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


def _frusta(a, b, q):
    """lo strappo laterale (Gadzhi): da a verso b, il quadro scivola e si sfoca in orizzontale"""
    s = math.sin(math.pi * q)
    out = Image.blend(a, b, S.ease_in_out(q))
    k = 1 + int(34 * s)
    if k > 1:
        out = out.resize((max(1, S.W // k), S.H), Image.BILINEAR).resize((S.W, S.H), Image.BILINEAR)
    sh = int(140 * s * (1 if q < 0.5 else -1))
    if sh:
        sp = out
        out = Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (255,))
        out.paste(sp, (-sh, 0))
    return out


class Sagome:
    """la sagoma della persona al frame n del montato (da `./mve sagome`), ammorbidita nel tempo"""

    def __init__(self, cartella):
        self.dir = cartella
        self.cache = {}

    def __call__(self, n):
        if self.dir is None:
            return None
        if n in self.cache:
            return self.cache[n]
        acc, k = None, 0
        for m in (n - 1, n, n + 1):
            p = self.dir / f"f{m:06d}.png"
            if p.exists():
                a = np.asarray(Image.open(p).convert('L'), dtype=np.float32)
                acc = a if acc is None else acc + a
                k += 1
        res = None
        if acc is not None:
            res = Image.fromarray((acc / k).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
            if res.size != (S.W, S.H):
                res = res.resize((S.W, S.H), Image.BILINEAR)
        if len(self.cache) > 4:
            self.cache.clear()
        self.cache[n] = res
        return res


# la finestra di Martell: verticale 4:5, sul lato in cui sta lei
FIN_W, FIN_H = 600, 750
# i framework stanno sopra i sottotitoli
BASSO = S.CAPTION_BOT - 130


class Scena:
    """la parte comune: fondo vivo, dove sta lei, ingresso e uscita attraverso il video.

    `area` e la fascia orizzontale in cui impagina il contenuto. I tipi `nativo`
    impaginano da soli dentro l'area; gli altri disegnano a tutto quadro e, quando
    lei occupa un lato, si rimpiccioliscono nella fascia libera."""
    nativo = False

    def __init__(self, c, sagome=None):
        self.c = c
        self.s, self.e = c['s'], c['e']
        self.lei = c.get('lei', 'dietro')
        self.lato = c.get('lato', 'destra')
        self.sagome = sagome
        self.dx = 0.0
        if self.lei == 'davanti':
            from ..progetto import FPS
            m = sagome(int(round((self.s + self.e) / 2 * FPS))) if sagome else None
            if m is None:
                print(f"  ! scena a {self.s:.1f}s: «lei davanti» senza sagome (./mve sagome): resta dietro il vetro")
                self.lei = 'dietro'
            else:
                # quanto deve scivolare per stare al centro del suo lato
                col = np.asarray(m, np.float32).sum(axis=0)
                cx = float((col * np.arange(S.W)).sum() / max(1.0, col.sum()))
                meta = S.W * (0.76 if self.lato == 'destra' else 0.24)
                self.dx = meta - cx
        if self.lei == 'dietro':
            self.area = (S.SAFE, S.W - S.SAFE)
        elif self.lei == 'finestra':
            self.fin = ((S.W - S.SAFE - FIN_W) if self.lato == 'destra' else S.SAFE, (S.H - FIN_H) // 2 - 10)
            self.area = (S.SAFE, self.fin[0] - 70) if self.lato == 'destra' else (self.fin[0] + FIN_W + 70, S.W - S.SAFE)
        else:
            self.area = (S.SAFE, int(S.W * 0.55)) if self.lato == 'destra' else (int(S.W * 0.45), S.W - S.SAFE)
        self.costruisci()

    def costruisci(self):
        pass

    def contenuto(self, im, tl):
        pass

    def attiva(self, t):
        return self.s <= t < self.e

    def _strato(self, tl):
        lay = Image.new('RGBA', (S.W, S.H), (0, 0, 0, 0))
        self.contenuto(lay, tl)
        if not self.nativo and self.lei != 'dietro':
            # il contenuto pensato a tutto quadro entra nella fascia libera
            x0, x1 = self.area
            k = (x1 - x0) / (S.W - 2 * S.SAFE)
            sm = lay.resize((int(S.W * k), int(S.H * k)), Image.BILINEAR)
            lay = Image.new('RGBA', (S.W, S.H), (0, 0, 0, 0))
            lay.alpha_composite(sm, (int((x0 + x1) / 2 - sm.width / 2), int(S.H / 2 - sm.height / 2)))
        # la camera deriva dentro la scena
        return _zoom(lay, 1.0 + 0.025 * _cl(tl / max(1.0, self.e - self.s)), 0.5)

    def componi(self, base, t, video=True, n=None):
        tl = t - self.s
        F = _fondo_vivo()
        fondo = _sfocato(base) if video else Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (255,))
        # il fondo respira: il bagliore deriva, la griglia scorre piano
        gx = -S.W * 0.15 + math.sin(tl * 0.7) * 60 + (S.W * 0.18 * (-1 if self.lato == 'destra' else 1) if self.lei != 'dietro' else 0)
        gy = -S.H * 0.15 + math.cos(tl * 0.5) * 40
        paste_clip(fondo, F['glow'], (gx, gy))
        dots, P = F['punti']
        off = int(tl * 14) % P
        fondo.alpha_composite(dots.crop((off, off, off + S.W, off + S.H)))
        fondo.alpha_composite(F['vign'])
        # a inizio video non c'e un video da cui entrare: la scena parte gia piena
        q_in = 1.0 if self.s < 0.05 else S.ease_in_out(_cl(tl / T_IN))
        q_out = S.ease_in_out(_cl((self.e - t) / T_OUT))
        q = min(q_in, q_out)
        lay = self._strato(tl)
        if self.lei == 'finestra' and video:
            return self._finestra(base, fondo, lay, t, tl)
        if self.lei == 'davanti' and video:
            return self._davanti(base, fondo, lay, q, n)
        fondo.alpha_composite(lay)
        frusta = self.c.get('ingresso') == 'frusta'
        if q_in < 1:
            if frusta:
                return _frusta(base, fondo, q_in)
            # si entra nel video: zoomata e dissolvenza nel vetro, con un lampo menta
            z = _zoom(base, 1.0 + 0.22 * q_in)
            out = Image.blend(z, fondo, q_in)
            lampo = 1 - abs(q_in - 0.55) / 0.25
            if lampo > 0:
                out = Image.blend(out, Image.new('RGBA', (S.W, S.H), S.MINT + (255,)), 0.10 * lampo)
            return out
        if q_out < 1:
            if frusta:
                return _frusta(fondo, base, 1 - q_out)
            # si torna nel video: la scena si allontana, il video atterra da un poco piu vicino
            z = _zoom(base, 1.0 + 0.10 * q_out)
            return Image.blend(z, fondo, q_out)
        return fondo

    def _finestra(self, base, fondo, lay, t, tl):
        """Martell: il quadro si stringe in una finestra di lato e lei resta li a parlare"""
        q_in = 1.0 if self.s < 0.05 else S.ease_in_out(_cl(tl / 0.62))
        q_out = S.ease_in_out(_cl((self.e - t) / 0.55))
        q = min(q_in, q_out)
        fx, fy = self.fin
        # il riquadro passa dal quadro intero alla finestra
        x0, y0 = fx * q, fy * q
        w = S.W + (FIN_W - S.W) * q
        h = S.H + (FIN_H - S.H) * q
        out = fondo
        fade_paste(out, lay, (0, 0), int(255 * _cl((q - 0.35) / 0.65)))
        # cosa entra nella finestra: il quadro tagliato al suo rapporto, attorno al centro
        rw = min(S.W, S.H * w / h)
        src = base.crop((int((S.W - rw) / 2), 0, int((S.W + rw) / 2), S.H)).resize((max(2, int(w)), max(2, int(h))), Image.BILINEAR)
        r = int(4 + 28 * q)
        from .base import _maschera, ombra_pannello
        if q > 0.02:
            om, P = ombra_pannello(int(w), int(h), r)
            paste_clip(out, om, (x0 - P, y0 - P + 18), int(255 * q))
        m = _maschera(int(w), int(h), r)
        src = src.convert('RGBA')
        src.putalpha(m)
        paste_clip(out, src, (x0, y0))
        if q > 0.02:
            t_ = Tela(int(w), int(h))
            t_.rett(1.5, 1.5, w - 1.5, h - 1.5, r, outline=S.MINT + (int(200 * q),), w=3)
            paste_clip(out, t_.fine(), (x0, y0))
        return out

    def _davanti(self, base, fondo, lay, q, n):
        """Gadzhi: lei esce dalla stanza, scivola sul suo lato, la grafica sta dietro di lei"""
        m = self.sagome(n) if (self.sagome and n is not None) else None
        fondo.alpha_composite(lay)
        if m is None:
            return Image.blend(base, fondo, q) if q < 1 else fondo
        if q < 1:
            # la stanza senza di lei: dove c'era lei c'e gia il fondo, cosi mentre scivola
            # non lascia il suo fantasma nel punto di partenza
            vuota = Image.composite(fondo, base.convert('RGBA'), m.filter(ImageFilter.MaxFilter(15)))
            out = Image.blend(vuota, fondo, q)
        else:
            out = fondo
        dx = int(self.dx * S.ease_in_out(q))
        lei = base.convert('RGBA')
        lei.putalpha(m)
        if q > 0.02:
            # ombra navy e filo di luce menta: la staccano dalla grafica
            om = Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (0,))
            om.putalpha(m.filter(ImageFilter.GaussianBlur(26)).point(lambda v: int(v * 0.75 * q)))
            paste_clip(out, om, (dx - 26, 14))
            al = Image.new('RGBA', (S.W, S.H), S.MINT + (0,))
            al.putalpha(m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(9))
                        .point(lambda v: int(min(255, v * 1.1) * 0.62 * q)))
            paste_clip(out, al, (dx, 0))
        paste_clip(out, lei, (dx, 0))
        return out


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


# --------------------------------------------------------------- framework
def _righe(txt, f, maxw):
    """a capo sulle parole, al massimo tre righe"""
    righe, cur = [], ''
    for wd in txt.split():
        prova = (cur + ' ' + wd).strip()
        if cur and f.getlength(prova) > maxw:
            righe.append(cur)
            cur = wd
        else:
            cur = prova
    return (righe + [cur])[:3]


def _blocco(txt, size, maxw, col, peso=800, centro=False):
    """sprite di un testo a capo; rimpicciolisce il corpo finche sta in tre righe"""
    while size > 26:
        f = sans(size, peso)
        r = _righe(txt, f, maxw)
        if ' '.join(r) == ' '.join(txt.split()) and all(f.getlength(x) <= maxw for x in r):
            break
        size -= 2
    lh = int(size * 1.12)
    w = int(max(f.getlength(x) for x in r)) + 16
    im = Image.new('RGBA', (w, lh * len(r) + int(size * 0.35)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i, x in enumerate(r):
        ox = (w - f.getlength(x)) / 2 if centro else 0
        d.text((ox + 4, i * lh), x, font=f, fill=col + (255,))
    return im


class Framework(Scena):
    """La parte comune ai framework di Martell: eyebrow e titolo in testa all'area,
    voci che entrano quando le dice, la voce corrente accesa.

    Nel `richiamo` tutte le voci ci sono gia (fioche) e si accende solo la voce
    `richiamo` (da 1): lo spettatore ritrova la mappa e sa dove si trova."""
    nativo = True

    def testata(self):
        c = self.c
        x0, x1 = self.area
        self.ax0, self.ax1 = x0, x1
        self.aw = x1 - x0
        self.acx = (x0 + x1) / 2
        self.ric = c.get('richiamo')
        self.voci = list(c.get('voci', []))
        if self.ric:
            for i, v in enumerate(self.voci):
                v['t'] = 0.25 + 0.05 * i
        y = 150
        self.eye = None
        if c.get('eyebrow'):
            self.eye = Macchina(c['eyebrow'], mono(28), S.MINT, 0.2 * 28)
            self.eye_xy = (self.acx - self.eye.sp.width / 2, y)
            y += 54
        self.tit = None
        if c.get('titolo'):
            self.tit = _blocco(c['titolo'].upper(), 58, self.aw, S.PAPER, 900, centro=True)
            self.tit_xy = (self.acx - self.tit.width / 2, y)
            y += self.tit.height + 10
        self.y_corpo = y + 30

    def corrente(self, tl):
        if self.ric:
            return self.ric - 1 if tl > 0.55 else None
        attive = [i for i, v in enumerate(self.voci) if tl >= v.get('t', 0.6 + i)]
        return attive[-1] if attive else None

    def u(self, i, tl):
        return tl - self.voci[i].get('t', 0.6 + i * 1.2)

    def disegna_testata(self, im, tl):
        if self.eye:
            self.eye.disegna(im, self.eye_xy, tl - 0.25, cursore=False)
        if self.tit:
            q = _cl((tl - 0.3) / 0.35)
            fade_paste(im, self.tit, (self.tit_xy[0], self.tit_xy[1] + (1 - S.ease_out_cubic(q)) * 20), int(255 * q))

    def tono(self, i, cur):
        """(colore, alfa) di una voce: accesa, gia detta, o fioca nel richiamo"""
        if i == cur:
            return S.MINT, 255
        if self.ric:
            return S.PAPER, 105
        return S.PAPER, 190 if cur is not None and i < cur else 255


class Passi(Framework):
    """I passi numerati: in colonna nell'area stretta, in fila a tutto quadro (fino a 4)."""

    def costruisci(self):
        self.testata()
        n = len(self.voci)
        self.fila = self.aw > 1400 and n <= 4
        if self.fila:
            self.r = 70
            self.cy = self.y_corpo + 150
            self.cxs = [self.ax0 + self.aw * (i + 0.5) / n for i in range(n)]
        else:
            alto = BASSO - self.y_corpo
            self.passo = min(190, alto / max(1, n))
            self.r = min(44, self.passo * 0.32)
            self.cx = self.ax0 + 50
            self.cys = [self.y_corpo + self.passo * (i + 0.5) for i in range(n)]
        self.sp = []
        for v in self.voci:
            if self.fila:
                self.sp.append({k: _blocco(v['testo'], 50, self.aw / n - 60, col, 800, centro=True) for k, col in
                                (('p', S.PAPER), ('m', S.MINT))})
            else:
                self.sp.append({k: _blocco(v['testo'], min(60, int(self.passo * 0.40)), self.aw - 170, col, 800)
                                for k, col in (('p', S.PAPER), ('m', S.MINT))})
        fn = sans(80 if self.fila else int(self.r * 1.3), 900)
        self.num = [testo(str(i + 1), fn, S.NAVY_DEEP + (255,), top=-8) for i in range(n)]
        self.num_m = [testo(str(i + 1), fn, S.MINT + (255,), top=-8) for i in range(n)]

    def contenuto(self, im, tl):
        self.disegna_testata(im, tl)
        cur = self.corrente(tl)
        d = ImageDraw.Draw(im)
        for i in range(len(self.voci)):
            u = self.u(i, tl)
            if u < 0:
                continue
            p = pop(_cl(u / 0.32))
            col, a = self.tono(i, cur)
            if self.fila:
                cx, cy = self.cxs[i], self.cy
            else:
                cx, cy = self.cx, self.cys[i]
            # il filo dal passo precedente
            if i > 0:
                pf = S.ease_out_expo(u / 0.45)
                if self.fila:
                    xa, xb = self.cxs[i - 1] + self.r + 12, cx - self.r - 12
                    d.rounded_rectangle([xa, cy - 3, xa + (xb - xa) * pf, cy + 3], radius=3, fill=S.MINT + (150,))
                else:
                    ya, yb = self.cys[i - 1] + self.r + 10, cy - self.r - 10
                    d.rounded_rectangle([cx - 3, ya, cx + 3, ya + (yb - ya) * pf], radius=3, fill=S.MINT + (150,))
            r = self.r * p
            if i == cur:
                g = int(90 * (0.6 + 0.4 * math.sin(tl * 4)))
                d.ellipse([cx - r - 14, cy - r - 14, cx + r + 14, cy + r + 14], fill=S.MINT + (g // 3,))
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=S.MINT + (255,))
                sp, pad = self.num[i]
            else:
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=S.NAVY_DEEP + (220,), outline=S.MINT + (a,), width=4)
                sp, pad = self.num_m[i]
            s2 = scala_px(sp, p)
            fade_paste(im, s2, (cx - s2.width / 2, cy - s2.height / 2 + 2), a)
            q = _cl((u - 0.08) / 0.32)
            bl = self.sp[i]['m' if i == cur else 'p']
            if self.fila:
                fade_paste(im, bl, (cx - bl.width / 2, cy + self.r + 34 + (1 - S.ease_out_cubic(q)) * 24), int(a * q))
            else:
                fade_paste(im, bl, (cx + self.r + 40 + (1 - S.ease_out_cubic(q)) * 40, cy - min(bl.height, 70) / 2 - 6), int(a * q))


class Ciclo(Framework):
    """Il circolo: nodi su un anello, la freccia arriva al nodo quando lo dice, poi
    l'anello si chiude (`chiude`: la frase, o subito dopo l'ultimo) e una goccia di
    luce comincia a girare. Il circolo vizioso che non si ferma."""

    def costruisci(self):
        self.testata()
        n = len(self.voci)
        self.n = n
        alto = BASSO - self.y_corpo
        # sopra il nodo in alto e sotto quelli in basso ci vanno le etichette
        self.R = min(self.aw * 0.30, (alto - 230) / 2, 290)
        self.cx, self.cy = self.acx, self.y_corpo + 115 + self.R
        self.rn = 58
        self.ang = [-90 + 360 * i / n for i in range(n)]
        self.lab = []
        for v in self.voci:
            self.lab.append({k: _blocco(v['testo'], 46 if self.aw >= 1300 else 40, 380 if self.aw >= 1300 else 300,
                                        col, 800, centro=True) for k, col in
                             (('p', S.PAPER), ('m', S.MINT))})
        self.ic = [icona(v['icona'], 62, S.MINT) if v.get('icona') else None for v in self.voci]
        self.icn = [icona(v['icona'], 62, S.NAVY_DEEP) if v.get('icona') else None for v in self.voci]
        self.num = [testo(str(i + 1), sans(52, 900), S.MINT + (255,), top=-6) for i in range(n)]
        self.numn = [testo(str(i + 1), sans(52, 900), S.NAVY_DEEP + (255,), top=-6) for i in range(n)]
        ultimo = max([v.get('t', 0) for v in self.voci] + [0])
        self.t_chiude = 0.5 if self.ric else self.c.get('chiude_t', ultimo + 0.9)
        self.centro = _blocco(self.c['centro'].upper(), 46, self.R * 1.25, S.MINT, 900, centro=True) if self.c.get('centro') else None
        self.gap = math.degrees(math.asin(min(0.9, (self.rn + 16) / self.R)))

    def _arco(self, t, i, j, p, a):
        a0 = self.ang[i] + self.gap
        a1 = self.ang[j] + (360 if j <= i else 0) - self.gap
        if p <= 0:
            return
        e = a0 + (a1 - a0) * p
        t.arco(self.cx, self.cy, self.R, a0, e, S.MINT + (a,), 6)
        # la punta
        r = math.radians(e)
        px, py = self.cx + self.R * math.cos(r), self.cy + self.R * math.sin(r)
        tx, ty = -math.sin(r), math.cos(r)        # tangente, nel verso della freccia
        nx, ny = math.cos(r), math.sin(r)
        L = 22
        t.poligono([(px + tx * 8, py + ty * 8), (px - tx * L + nx * 13, py - ty * L + ny * 13),
                    (px - tx * L - nx * 13, py - ty * L - ny * 13)], fill=S.MINT + (a,))

    def contenuto(self, im, tl):
        self.disegna_testata(im, tl)
        cur = self.corrente(tl)
        t = Tela(S.W, S.H)
        # l'anello di fondo, fioco: la forma si capisce subito
        pa = S.ease_out_expo((tl - 0.2) / 0.8)
        if pa > 0:
            t.arco(self.cx, self.cy, self.R, -90, -90 + 360 * pa, S.PAPER + (34,), 2, tondi=False)
        for i in range(self.n):
            j = (i + 1) % self.n
            if j == 0:
                p = S.ease_in_out((tl - self.t_chiude) / 0.6)
            else:
                p = S.ease_in_out(self.u(j, tl) / 0.5)
            self._arco(t, i, j, p, 120 if self.ric else 230)
        chiuso = tl > self.t_chiude + 0.6
        # la goccia di luce gira sull'anello chiuso
        gira = None
        if chiuso:
            gira = (-90 + (tl - self.t_chiude - 0.6) * 150) % 360
            r = math.radians(gira)
            gx, gy = self.cx + self.R * math.cos(r), self.cy + self.R * math.sin(r)
            for k, rr in ((60, 22), (120, 13), (255, 7)):
                t.cerchio(gx, gy, rr, fill=S.MINT + (k,))
        im.alpha_composite(t.fine())
        d = ImageDraw.Draw(im)
        for i in range(self.n):
            u = self.u(i, tl)
            if u < 0:
                continue
            p = pop(_cl(u / 0.32))
            col, a = self.tono(i, cur)
            r_ = math.radians(self.ang[i])
            nx, ny = self.cx + self.R * math.cos(r_), self.cy + self.R * math.sin(r_)
            vicino = gira is not None and abs(((gira - self.ang[i]) + 180) % 360 - 180) < 14
            k = p * (1.08 if vicino else 1.0)
            r = self.rn * k
            acceso = i == cur
            if acceso:
                d.ellipse([nx - r - 12, ny - r - 12, nx + r + 12, ny + r + 12], fill=S.MINT + (50,))
                d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=S.MINT + (255,))
            else:
                d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=S.NAVY_DEEP + (235,), outline=S.MINT + (a,), width=4)
            ic = (self.icn if acceso else self.ic)[i]
            if ic is not None:
                s2 = scala_px(ic, k)
                fade_paste(im, s2, (nx - s2.width / 2, ny - s2.height / 2), a)
            else:
                sp, pad = (self.numn if acceso else self.num)[i]
                s2 = scala_px(sp, k)
                fade_paste(im, s2, (nx - s2.width / 2, ny - s2.height / 2 + 2), a)
            # l'etichetta sta fuori dall'anello, nella direzione del nodo
            bl = self.lab[i]['m' if acceso else 'p']
            q = _cl((u - 0.1) / 0.3)
            ox, oy = math.cos(r_), math.sin(r_)
            lx = nx + ox * (self.rn + 24) - bl.width / 2 + ox * bl.width / 2
            ly = ny + oy * (self.rn + 22) - bl.height / 2 + oy * bl.height / 2
            if oy < -0.7:
                # il nodo in alto: l'etichetta a fianco, sopra c'e la testata
                lx, ly = nx + self.rn + 26, ny - bl.height / 2 + 4
            if self.aw < 1300 and oy >= -0.7:
                # area stretta (lei accanto): l'etichetta sotto il nodo, non verso di lei
                lx, ly = nx - bl.width / 2, ny + self.rn + 30
            lx = min(max(self.ax0 - 40, lx), self.ax1 - bl.width)
            fade_paste(im, bl, (lx, ly + (1 - S.ease_out_cubic(q)) * 14), int(a * q))
        if self.centro is not None and tl > self.t_chiude:
            q = _cl((tl - self.t_chiude - 0.2) / 0.35)
            s2 = scala_px(self.centro, pop(q))
            fade_paste(im, s2, (self.cx - s2.width / 2, self.cy - s2.height / 2), int(255 * min(1, q * 2)))


class Matrice(Framework):
    """2x2: gli assi si disegnano, i quadranti (in alto a sinistra, in alto a destra,
    in basso a sinistra, in basso a destra) entrano quando li dice; la voce con
    `acceso` si riempie di menta. `asse_x` e `asse_y` sono etichette mono."""

    def costruisci(self):
        self.testata()
        alto = BASSO - self.y_corpo
        self.G = min(self.aw - 140, alto - 20, 760)
        self.x0 = self.acx - self.G / 2 + 20
        self.y0 = self.y_corpo + (alto - self.G) / 2
        cw = self.G / 2
        self.lab = [{k: _blocco(v['testo'], 44, cw - 50, col, 800, centro=True) for k, col in
                     (('p', S.PAPER), ('n', S.NAVY_DEEP))} for v in self.voci]
        c = self.c
        self.ax = testo(c['asse_x'].upper(), mono(24), S.MUTED + (255,), 0.2 * 24) if c.get('asse_x') else None
        self.ay = testo(c['asse_y'].upper(), mono(24), S.MUTED + (255,), 0.2 * 24) if c.get('asse_y') else None

    def contenuto(self, im, tl):
        self.disegna_testata(im, tl)
        G, x0, y0 = self.G, self.x0, self.y0
        cw = G / 2
        d = ImageDraw.Draw(im)
        cur = self.corrente(tl)
        acc = [i for i, v in enumerate(self.voci) if v.get('acceso') or (self.ric and i == self.ric - 1)]
        for i in range(min(4, len(self.voci))):
            u = self.u(i, tl)
            if u < 0:
                continue
            q = _cl(u / 0.3)
            cx0 = x0 + (i % 2) * cw + 8
            cy0 = y0 + (i // 2) * cw + 8
            pieno = i in acc and (self.ric or u > 0.5)
            k = pop(q)
            w_ = (cw - 16) * k
            mx, my = cx0 + (cw - 16) / 2, cy0 + (cw - 16) / 2
            fill = S.MINT + (240,) if pieno else S.PAPER + ((14 if i != cur else 30),)
            d.rounded_rectangle([mx - w_ / 2, my - w_ / 2, mx + w_ / 2, my + w_ / 2], radius=18, fill=fill,
                                outline=None if pieno else S.PAPER + (60 if i == cur else 30,), width=2)
            bl = self.lab[i]['n' if pieno else 'p']
            a = 255 if (pieno or i == cur or not self.ric) else 120
            fade_paste(im, bl, (mx - bl.width / 2, my - bl.height / 2 + (1 - S.ease_out_cubic(q)) * 14), int(a * q))
        # gli assi sopra i quadranti: la croce che li divide
        p = S.ease_out_expo((tl - 0.3) / 0.6)
        if p > 0:
            mx, my = x0 + G / 2, y0 + G / 2
            d.rounded_rectangle([mx - 3, my - G / 2 * p - 20, mx + 3, my + G / 2 * p + 20], radius=3, fill=S.MINT + (220,))
            d.rounded_rectangle([mx - G / 2 * p - 20, my - 3, mx + G / 2 * p + 20, my + 3], radius=3, fill=S.MINT + (220,))
            qa = _cl((tl - 0.7) / 0.3)
            if self.ax:
                sp, pad = self.ax
                fade_paste(im, sp, (x0 + G - sp.width - pad, y0 + G + 16 - pad), int(255 * qa))
            if self.ay:
                sp, pad = self.ay
                r = sp.rotate(90, expand=True)
                fade_paste(im, r, (x0 - 22 - r.width, y0 + 8), int(255 * qa))


class Piramide(Framework):
    """Gli strati dal basso: la prima voce e la base. L'ultimo strato detto e acceso."""

    def costruisci(self):
        self.testata()
        n = len(self.voci)
        alto = BASSO - self.y_corpo
        self.Hp = min(alto, n * 160)
        self.Bw = min(self.aw - 40, 980)
        self.yb = self.y_corpo + (alto + self.Hp) / 2
        self.lh = self.Hp / n
        self.lab = []
        for i, v in enumerate(self.voci):
            wt = self._larg(i, 0.5) - 90
            self.lab.append({k: _blocco(v['testo'], 46, max(160, wt), col, 800, centro=True) for k, col in
                             (('p', S.PAPER), ('n', S.NAVY_DEEP))})

    def _larg(self, i, f):
        """larghezza della piramide all'altezza dello strato i (f = frazione dentro lo strato)"""
        h = (i + 1 - f) * self.lh
        # tronca: la cima resta larga abbastanza per due parole
        return self.Bw * (1 - h / (self.Hp * 1.6))

    def contenuto(self, im, tl):
        self.disegna_testata(im, tl)
        cur = self.corrente(tl)
        t = Tela(S.W, S.H)
        cx = self.acx
        disegni = []
        for i in range(len(self.voci)):
            u = self.u(i, tl)
            if u < 0:
                continue
            q = S.ease_out_cubic(_cl(u / 0.4))
            yb = self.yb - i * self.lh - (1 - q) * -40
            yt = yb - self.lh + 10
            wb, wt = self._larg(i, 1.0), self._larg(i, 0.0)
            acceso = i == cur
            fill = S.MINT + (int(240 * q),) if acceso else S.PAPER + (int((22 if not self.ric else 12) * q),)
            t.poligono([(cx - wb / 2, yb), (cx + wb / 2, yb), (cx + wt / 2, yt), (cx - wt / 2, yt)], fill=fill,
                       outline=None if acceso else S.PAPER + (int(70 * q),), w=2)
            disegni.append((i, u, q, (yb + yt) / 2, acceso))
        im.alpha_composite(t.fine())
        for i, u, q, ym, acceso in disegni:
            bl = self.lab[i]['n' if acceso else 'p']
            a = 255 if (acceso or not self.ric) else 120
            fade_paste(im, bl, (cx - bl.width / 2, ym - bl.height / 2 + 4), int(a * q))


TIPI = {'parole': Parole, 'numero': Numero, 'confronto': Confronto,
        'passi': Passi, 'ciclo': Ciclo, 'matrice': Matrice, 'piramide': Piramide}


def crea(c, sagome=None):
    tipo = c.get('tipo', 'parole')
    if tipo not in TIPI:
        raise SystemExit(f"tipo di scena sconosciuto: «{tipo}» (tipi: {', '.join(TIPI)}, richiamo)")
    return TIPI[tipo](c, sagome)

"""Le infografiche: tutto cio che in regia sta sotto `card`, scelto con `tipo`.

Ogni infografica disegna solo il suo contenuto, su fondo trasparente: il
pannello di vetro sotto lo mette la scena (`render.Scene`), che vede il video.
Ogni voce di un'infografica puo ancorarsi a una frase (`frase`): la fase
`grafica` la traduce in `t`, secondi dall'ingresso della card, e la voce entra
quando lei la dice. Senza `frase` le voci entrano una dopo l'altra.

Regola di sempre: niente testo inventato. Le scritte sono parole sue o
etichette strutturali; i numeri delle scale e degli orologi sono solo misure.

| tipo | cosa |
|---|---|
| `numero` | contatore + `grafico`: `barra`, `anello`, `punti`, `batteria` |
| `barre` | confronto di misure, anche sproporzionate |
| `orologio` | quadrante che gira fino all'ora detta, settore del tempo che manca |
| `icone` | icone che si contano una a una, le ultime a fantasma |
| `lista` | voci con ✓, ✗ o numero; `annulla` le barra tutte insieme |
| `catena` | causa -> effetto, nodo per nodo |
| `citazione` | la frase a karaoke dentro le virgolette |
| `anatomia` | gabbia toracica, polmoni, diaframma che respira; zone numerate |
| `postura` | figura seduta che si affloscia; zone numerate |
| `curva` | andamento disegnato nel tempo, con etichette |
"""
import math
import re

from PIL import Image, ImageDraw, ImageFilter

from .. import stile as S
from .base import (sans, mono, tracked_width, char_x, wrap_to, testo, bagliore, fade_paste, paste_clip,
                   scala_px, Macchina, Tela, icona, curva_liscia, _cl)

PAD = 34
NUM = re.compile(r'\d+(?:[.,]\d+)?')


def _numeri(s):
    return [float(x.replace(',', '.')) for x in NUM.findall(s or '')]


def conta(valore, p, prima=None):
    """il valore a schermo quando il conteggio e alla frazione p (da 0, o da `prima`)"""
    tgt = NUM.findall(valore)
    pre = _numeri(prima)
    src = [max(pre)] * len(tgt) if pre else [0.0] * len(tgt)
    it = iter(range(len(tgt)))

    def rep(m):
        i = next(it)
        dec = len(m.group().replace(',', '.').split('.')[1]) if re.search(r'[.,]', m.group()) else 0
        v = src[i] + (float(m.group().replace(',', '.')) - src[i]) * p
        s = f"{v:.{dec}f}"
        return s.replace('.', ',') if ',' in m.group() else s
    return NUM.sub(rep, valore)


def pop(p):
    """scala di un elemento che entra: da 0,4 a 1 con un rimbalzo"""
    return 0.4 + 0.6 * S.ease_out_back(p)


class Info:
    """la testata comune (eyebrow a macchina + filo menta) e il congelamento finale"""
    W = S.CARD_W
    stabile = 1e9            # le infografiche che si muovono sempre non si congelano

    def __init__(self, c):
        self.c = c
        self.w = int(c.get('larghezza') or self.W)
        self.finale = None
        if c.get('eyebrow'):
            es = S.SIZE['eyebrow']
            self.eye = Macchina(c['eyebrow'], mono(es), S.MINT, S.TRACK['eyebrow'] * es)
            self.y_rule = PAD + es + 14
            self.y0 = self.y_rule + 6 + 24
        else:
            self.eye = None
            self.y0 = PAD
        self.costruisci()

    def costruisci(self):
        self.h = self.y0 + PAD

    def voce_t(self, v, i, passo=0.45, inizio=0.45):
        t = v.get('t') if isinstance(v, dict) else None
        return t if t is not None else inizio + i * passo

    def testata(self, im, tl):
        if not self.eye:
            return
        self.eye.disegna(im, (PAD, PAD), tl - 0.10, cursore=False)
        rw = 84 * S.ease_out_expo((tl - 0.20) / 0.45)
        if rw > 1:
            ImageDraw.Draw(im).rounded_rectangle([PAD, self.y_rule, PAD + rw, self.y_rule + 5], radius=2,
                                                 fill=S.MINT + (255,))

    def disegna(self, im, tl):
        pass

    def sprite(self, tl):
        if self.finale is not None and tl >= self.stabile:
            return self.finale
        im = Image.new('RGBA', (self.w, self.h), (0, 0, 0, 0))
        self.testata(im, tl)
        self.disegna(im, tl)
        if tl >= self.stabile:
            self.finale = im
        return im


def _parole_a_capo(font, text, maxw, lh, x0, y0, colore):
    """sprite per parola, gia a posto: (sprite, x, y, indice)"""
    out, k = [], 0
    for li, ln in enumerate(wrap_to(font, text, 0, maxw)):
        x = x0
        for wd in ln.split():
            sp, pad = testo(wd, font, colore + (255,))
            out.append((sp, x - pad, y0 + li * lh - pad, k))
            x += font.getlength(wd + ' ')
            k += 1
    return out, len(wrap_to(font, text, 0, maxw))


# ------------------------------------------------------------------- numero
BAR_H = 12


def scala(c):
    """la scala misurata sotto il numero: percentuale, centimetri o minuti"""
    u = (c.get('unit') or '').strip().lower()
    v, pre = _numeri(c['value']), _numeri(c.get('prima'))
    if not v:
        return None
    top = max(v + pre)
    if u == '%':
        mx, passo, etich = 100.0, 10, [(0, '0'), (50, '50'), (100, '100%')]
    elif u == 'cm':
        mx = float(max(2, math.ceil(top * 1.25)))
        passo, etich = 1, [(0, '0'), (mx, f"{mx:g} cm")]
    elif u in ('min', "'"):
        mx = 60.0 if top <= 50 else float(math.ceil(top * 1.2 / 30) * 30)
        passo, etich = 10, [(0, '0'), (mx / 2, f"{mx / 2:g}"), (mx, f"{mx:g} min")]
    else:
        return None
    return {'mx': mx, 'passo': passo, 'etichette': etich, 'v': v, 'pre': max(pre) if pre else None}


class Numero(Info):
    """Il numero che conta fino al valore, con il suo grafico:

    - `barra` (default): scala misurata (%, cm, min); con `prima` il tratto di partenza resta come fantasma
    - `anello`: anello che si chiude fino alla percentuale, con `icona` al centro
    - `punti`: cento punti che si accendono; `riferimento: {"valore": "20", "etichetta": "OSSIGENO"}`
      disegna a contorno l'altra quantita, per il confronto
    - `batteria`: una batteria che si carica fino alla percentuale
    """
    G = 150

    def costruisci(self):
        c = self.c
        self.f_val = sans(S.SIZE['card_value'], 900)
        self.top_val = -int(S.SIZE['card_value'] * 0.16)
        self.vw = self.f_val.getlength(c['value'])
        self.unit, self.unit_pad = testo(c['unit'], sans(S.SIZE['card_unit'], 800), S.PAPER + (255,))
        self.nums = {}
        fin, fp = self._num(c['value'])
        self.glow, self.glow_pad = bagliore(fin, 16, S.MINT, 0.8)
        self.glow_fermo = self.glow.copy()
        self.glow_fermo.putalpha(self.glow.getchannel('A').point(lambda v: v * 70 // 255))
        g = c.get('grafico') or 'barra'
        self.sc = scala(c) if g == 'barra' else None
        vals = _numeri(c['value'])
        self.v = vals[-1] if vals else 0.0
        self.vlo = vals[0] if vals else 0.0
        self.grafico = g if (g != 'barra' or self.sc) else None
        y_val = self.y0
        y = y_val + S.SIZE['card_value'] + 8
        # anello e batteria stanno accanto al numero, se c'e posto; se no sotto
        self.lato = False
        if g in ('anello', 'batteria'):
            libero = self.w - 2 * PAD - (self.vw + 12 + self.unit.width)
            self.lato = libero >= self.G + 16
            if not self.lato:
                y += self.G + 16
        elif g == 'barra' and self.sc:
            y += 62
        elif g == 'punti':
            self.passo = (self.w - 2 * PAD) / 20
            self.y_punti = y + 6
            y += int(self.passo * 5) + 12
            if c.get('riferimento'):
                self.y_legenda = y
                y += 34
        else:
            y += 6
        self.y_val, self.y_graf = y_val, y_val + S.SIZE['card_value'] + 14
        f_sub = sans(S.SIZE['card_sub'], 600)
        lh = int(S.SIZE['card_sub'] * 1.32)
        self.gloss, n = _parole_a_capo(f_sub, c.get('sub') or '', self.w - 2 * PAD, lh, PAD, y, S.MUTED)
        self.h = y + n * lh + PAD - 6
        self.f_sc = mono(S.SIZE['card_scala'])
        self.t_glossa = 0.62
        self.stabile = max(S.COUNT_T0 + S.COUNT_DUR + 0.5, self.t_glossa + len(self.gloss) * 0.035 + 0.3,
                           len(c['eyebrow']) * S.TYPE_CHAR + 0.7)

    def _num(self, s):
        if s not in self.nums:
            if len(self.nums) > 80:
                self.nums.clear()
            self.nums[s] = testo(s, self.f_val, S.MINT + (255,), top=self.top_val)
        return self.nums[s]

    # -- grafici -------------------------------------------------------------
    def _barra(self, d, p):
        sc = self.sc
        x0, x1 = PAD, self.w - PAD
        y = self.y_graf
        X = lambda v: x0 + (x1 - x0) * min(1.0, v / sc['mx'])
        d.rounded_rectangle([x0, y, x1, y + BAR_H], radius=BAR_H // 2, fill=S.PAPER + (34,))
        if sc['pre'] is not None:
            d.rounded_rectangle([x0, y, X(sc['pre']), y + BAR_H], radius=BAR_H // 2, fill=S.MUTED + (110,))
        src = sc['pre'] if sc['pre'] is not None else 0.0
        lo = src + (sc['v'][0] - src) * p
        hi = src + (sc['v'][-1] - src) * p
        if X(hi) - x0 > 2:
            d.rounded_rectangle([x0, y, max(x0 + BAR_H, X(hi)), y + BAR_H], radius=BAR_H // 2, fill=S.MINT + (120,))
        if X(lo) - x0 > 2:
            d.rounded_rectangle([x0, y, max(x0 + BAR_H, X(lo)), y + BAR_H], radius=BAR_H // 2, fill=S.MINT + (255,))
        xm = max(x0 + BAR_H / 2, X(hi))
        r = BAR_H * 0.95
        d.ellipse([xm - r, y + BAR_H / 2 - r, xm + r, y + BAR_H / 2 + r], fill=S.MINT + (255,))
        d.ellipse([xm - r * 0.4, y + BAR_H / 2 - r * 0.4, xm + r * 0.4, y + BAR_H / 2 + r * 0.4], fill=S.NAVY + (255,))
        v = 0.0
        while v <= sc['mx'] + 1e-6:
            xt = X(v)
            mag = any(abs(v - e) < 1e-6 for e, _ in sc['etichette'])
            d.line([(xt, y + BAR_H + 5), (xt, y + BAR_H + (14 if mag else 9))], fill=S.MUTED + (170,), width=2)
            v += sc['passo']
        for v, lab in sc['etichette']:
            lw = self.f_sc.getlength(lab)
            xt = X(v) - (0 if v == 0 else lw if v >= sc['mx'] else lw / 2)
            d.text((xt, y + BAR_H + 17), lab, font=self.f_sc, fill=S.MUTED + (220,))

    def _pos_lato(self):
        if self.lato:
            return self.w - PAD - self.G, self.y_val - 4
        return PAD, self.y_graf

    def _anello(self, im, p):
        G = self.G
        x, y = self._pos_lato()
        t = Tela(G, G)
        r, lw = G / 2 - 10, 14
        t.arco(G / 2, G / 2, r, 0, 360, S.PAPER + (40,), lw, tondi=False)
        a = 360 * min(1.0, self.v / 100 * p)
        if a > 0.5:
            t.arco(G / 2, G / 2, r, -90, -90 + a, S.MINT + (255,), lw)
        im.alpha_composite(t.fine(), (int(x), int(y)))
        if self.c.get('icona'):
            ic = icona(self.c['icona'], 58, S.MINT)
            fade_paste(im, ic, (x + (G - 58) / 2, y + (G - 58) / 2), int(255 * _cl(p * 2)))

    def _batteria(self, im, p):
        G = self.G
        x, y = self._pos_lato()
        bw, bh = G - 14, int(G * 0.56)
        oy = (G - bh) / 2
        t = Tela(G, G)
        t.rett(2, oy, bw, oy + bh, 14, outline=S.PAPER + (200,), w=5)
        t.rett(bw + 3, oy + bh * 0.32, G - 2, oy + bh * 0.68, 4, fill=S.PAPER + (200,))
        livello = min(1.0, self.v / 100 * p)
        iw = (bw - 16) * livello
        if iw > 2:
            t.rett(10, oy + 8, 10 + iw, oy + bh - 8, 8, fill=S.MINT + (255,))
        for k in range(1, 5):          # i segmenti
            xs = 10 + (bw - 16) * k / 5
            if xs < 10 + iw:
                t.linea([(xs, oy + 8), (xs, oy + bh - 8)], S.NAVY + (255,), 3, tondi=False)
        im.alpha_composite(t.fine(), (int(x), int(y)))

    def _punti(self, im, p):
        c, passo = self.c, self.passo
        rif = _numeri((c.get('riferimento') or {}).get('valore'))
        rif = rif[0] if rif else None
        accesi_hi = self.v * p
        accesi_lo = self.vlo * p
        t = Tela(self.w, int(passo * 5) + 4)
        r = passo * 0.33
        for k in range(100):
            col, row = k // 5, k % 5
            cx, cy = PAD + passo * (col + 0.5), passo * (row + 0.5) + 2
            if k < accesi_lo - 0.5 or (k < accesi_hi - 0.5 and accesi_lo == accesi_hi):
                t.cerchio(cx, cy, r, fill=S.MINT + (255,))
            elif k < accesi_hi - 0.5:
                t.cerchio(cx, cy, r, fill=S.MINT + (130,))
            elif rif is not None and k < rif:
                t.cerchio(cx, cy, r - 1, outline=S.MINT + (190,), w=2.2)
            else:
                t.cerchio(cx, cy, r * 0.7, fill=S.PAPER + (34,))
        im.alpha_composite(t.fine(), (0, int(self.y_punti)))
        if c.get('riferimento') and p > 0.3:
            a = int(255 * _cl((p - 0.3) / 0.4))
            d = ImageDraw.Draw(im)
            f = self.f_sc
            y = self.y_legenda
            x = PAD
            d.ellipse([x, y + 4, x + 14, y + 18], fill=S.MINT + (a,))
            lab = f"{c['value']}{c['unit']} {c['eyebrow']}"
            d.text((x + 22, y), lab, font=f, fill=S.PAPER + (a,))
            x += 22 + f.getlength(lab) + 30
            d.ellipse([x, y + 4, x + 14, y + 18], outline=S.MINT + (a,), width=2)
            R = c['riferimento']
            d.text((x + 22, y), f"{R['valore']}{c['unit']} {R.get('etichetta', '')}".strip(), font=f,
                   fill=S.MUTED + (a,))

    def disegna(self, im, tl):
        c = self.c
        pc = S.ease_out_expo((tl - S.COUNT_T0) / S.COUNT_DUR)
        if tl >= S.COUNT_T0:
            fine = tl >= S.COUNT_T0 + S.COUNT_DUR
            s = c['value'] if fine else conta(c['value'], pc, c.get('prima'))
            sp, pad = self._num(s)
            gx, gy = PAD - pad - self.glow_pad, self.y_val - pad - self.glow_pad
            g = (tl - S.COUNT_T0 - S.COUNT_DUR) / 0.5
            if fine:
                fade_paste(im, self.glow_fermo, (gx, gy), 255)
            if 0 <= g < 1:
                fade_paste(im, self.glow, (gx, gy), int(200 * (1 - g) ** 1.5))
            fade_paste(im, sp, (PAD - pad, self.y_val - pad), int(255 * _cl((tl - S.COUNT_T0) / 0.12)))
            pu = _cl((tl - S.COUNT_T0 - S.COUNT_DUR * 0.55) / 0.3)
            if pu > 0:
                u = scala_px(self.unit, 0.6 + 0.4 * S.ease_out_back(pu))
                fade_paste(im, u, (PAD + self.vw + 12 - self.unit_pad,
                                   self.y_val + S.SIZE['card_value'] - S.SIZE['card_unit'] - 14 - self.unit_pad
                                   + self.unit.height - u.height), int(255 * min(1, pu * 2)))
        pg = pc if tl >= S.COUNT_T0 else 0.0
        pb = _cl((tl - 0.12) / 0.3)
        if self.grafico and pb > 0:
            lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
            if self.grafico == 'barra':
                self._barra(ImageDraw.Draw(lay), pg)
            elif self.grafico == 'anello':
                self._anello(lay, pg)
            elif self.grafico == 'batteria':
                self._batteria(lay, pg)
            elif self.grafico == 'punti':
                self._punti(lay, pg)
            fade_paste(im, lay, (0, 0), int(255 * pb))
        for sp, x, y, k in self.gloss:
            p = _cl((tl - self.t_glossa - k * 0.035) / 0.24)
            if p > 0:
                fade_paste(im, sp, (x, y + (1 - S.ease_out_cubic(p)) * 12), int(255 * p))


# -------------------------------------------------------------------- barre
class Barre(Info):
    """Confronto di misure: `voci: [{etichetta, testo, misura, frase}]`. La barra e
    proporzionale a `misura`; il `testo` e quello che si legge (le sue parole).
    Funziona anche con proporzioni assurde: 10 anni contro 10 secondi diventa una
    barra piena contro un punto."""

    def costruisci(self):
        V = self.c['voci']
        self.mx = max(float(v['misura']) for v in V)
        self.f_lab = mono(20)
        self.f_val = sans(60, 900)
        y = self.y0
        self.righe = []
        for i, v in enumerate(V):
            acc = v.get('accento', i == len(V) - 1)
            lab = Macchina(v.get('etichetta', ''), self.f_lab, S.MUTED, 0.14 * 20)
            val, vp = testo(v['testo'], self.f_val, (S.MINT if acc else S.PAPER) + (255,), -1.5, top=-8)
            self.righe.append({'t': self.voce_t(v, i, 0.9), 'lab': lab, 'val': (val, vp), 'y': y,
                               'f': float(v['misura']) / self.mx, 'acc': acc})
            y += 26 + 66 + 26 + 30
        self.h = y - 30 + PAD
        # una barra troppo corta diventa un punto che pulsa: allora non si congela
        corta = any(r['f'] * (self.w - 2 * PAD) < 20 for r in self.righe)
        self.stabile = 1e9 if corta else max(r['t'] for r in self.righe) + 1.4

    def disegna(self, im, tl):
        d = ImageDraw.Draw(im)
        x0, x1 = PAD, self.w - PAD
        for r in self.righe:
            u = tl - r['t']
            if u < -0.05:
                continue
            y = r['y']
            r['lab'].disegna(im, (x0, y), u, cursore=False)
            sp, pad = r['val']
            pv = _cl((u - 0.08) / 0.3)
            if pv > 0:
                fade_paste(im, sp, (x0 - pad, y + 28 - pad + (1 - S.ease_out_cubic(pv)) * 14), int(255 * pv))
            yb = y + 26 + 66 + 6
            d.rounded_rectangle([x0, yb, x1, yb + 20], radius=10, fill=S.PAPER + (26,))
            p = S.ease_out_expo((u - 0.25) / 0.9)
            L = (x1 - x0) * r['f'] * p
            col = S.MINT if r['acc'] else S.PAPER
            if L >= 20:
                d.rounded_rectangle([x0, yb, x0 + L, yb + 20], radius=10, fill=col + (255,))
            elif p > 0:
                # troppo piccola per una barra: un punto che pulsa
                k = 1 + 0.25 * math.sin(u * 7)
                rr = 9 * k
                d.ellipse([x0 + 10 - rr, yb + 10 - rr, x0 + 10 + rr, yb + 10 + rr], fill=col + (255,))


# ----------------------------------------------------------------- orologio
def _hm(s):
    h, m = s.split(':')
    return int(h) % 12 + int(m) / 60


class Orologio(Info):
    """Quadrante che gira fino all'ora detta (da `prima`, o dalle 12), ora digitale
    che scorre, `testo` sotto (le sue parole: "LE TRE MENO DIECI"). `fino` e
    `settore_testo` accendono lo spicchio del tempo che manca."""
    D = 200

    def costruisci(self):
        c = self.c
        self.ora = _hm(c['ora'])
        self.da = _hm(c['prima']) if c.get('prima') else self.ora - 0.75
        self.fino = _hm(c['fino']) if c.get('fino') else None
        if self.fino is not None and self.fino < self.ora:
            self.fino += 12
        x = PAD + self.D + 30
        self.xr = x
        self.f_ora = sans(76, 900)
        self.h24 = int(c['ora'].split(':')[0])
        f_t = sans(30, 800)
        self.testo_, n = _parole_a_capo(f_t, c.get('testo', ''), self.w - x - PAD, 36, x, self.y0 + 96, S.PAPER)
        self.sett = None
        if c.get('settore_testo'):
            self.sett = Macchina(c['settore_testo'], mono(19), S.MINT, 0.12 * 19)
            self.y_sett = self.y0 + 96 + n * 36 + 12
        self.h = self.y0 + max(self.D, 96 + n * 36 + (48 if self.sett else 0)) + PAD
        # lo spicchio arriva quando lei dice quanto manca (`voci: [{frase}]`)
        voci = c.get('voci') or []
        self.t_sett = self.voce_t(voci[0], 0, inizio=1.4) if voci else 1.4

    def _quadrante(self, h, tl, ps):
        D = self.D
        t = Tela(D, D)
        c = D / 2
        r = D / 2 - 6
        t.cerchio(c, c, r, fill=S.NAVY_DEEP + (150,), outline=S.PAPER + (110,), w=3)
        if self.fino is not None and ps > 0:
            a0 = self.ora * 30 - 90
            a1 = a0 + (self.fino - self.ora) * 30 * ps
            t.spicchio(c, c, r - 10, a0, a1, S.MINT + (70,))
            t.arco(c, c, r - 4, a0, a1, S.MINT + (255,), 5)
        for k in range(60):
            a = math.radians(k * 6 - 90)
            big = k % 5 == 0
            q = k % 15 == 0
            r0 = r - (22 if q else 15 if big else 9)
            t.linea([(c + r0 * math.cos(a), c + r0 * math.sin(a)), (c + (r - 6) * math.cos(a), c + (r - 6) * math.sin(a))],
                    S.PAPER + ((230 if q else 160) if big else 50,), 4 if q else 3 if big else 1.5)
        ah = math.radians(h * 30 - 90)
        am = math.radians((h % 1) * 360 - 90)
        t.linea([(c, c), (c + r * 0.50 * math.cos(ah), c + r * 0.50 * math.sin(ah))], S.PAPER + (255,), 9)
        t.linea([(c, c), (c + r * 0.80 * math.cos(am), c + r * 0.80 * math.sin(am))], S.MINT + (255,), 6)
        asec = math.radians(tl * 36 - 90)          # la lancetta dei secondi corre (accelerata)
        t.linea([(c - r * 0.12 * math.cos(asec), c - r * 0.12 * math.sin(asec)),
                 (c + r * 0.86 * math.cos(asec), c + r * 0.86 * math.sin(asec))], S.MINT + (200,), 2)
        t.cerchio(c, c, 9, fill=S.MINT + (255,))
        t.cerchio(c, c, 3.5, fill=S.NAVY + (255,))
        return t.fine()

    def disegna(self, im, tl):
        p = S.ease_out_expo((tl - 0.15) / 1.3)
        h = self.da + (self.ora - self.da) * p
        ps = S.ease_in_out((tl - self.t_sett) / 0.8)
        q = _cl(tl / 0.35)
        fade_paste(im, scala_px(self._quadrante(h, tl, ps), 0.85 + 0.15 * S.ease_out_back(q)) if q < 1
                   else self._quadrante(h, tl, ps), (PAD, self.y0), int(255 * q))
        # l'ora digitale scorre con le lancette (sul quadrante delle 24 ore che lei intende)
        hh = h + (self.h24 - self.h24 % 12)
        mins = int(round(hh * 60))
        s = f"{(mins // 60) % 24:d}:{mins % 60:02d}"
        sp, pad = testo(s, self.f_ora, S.MINT + (255,), -2, top=-10)
        fade_paste(im, sp, (self.xr - pad, self.y0 - pad), int(255 * _cl((tl - 0.15) / 0.2)))
        for sp, x, y, k in self.testo_:
            pt = _cl((tl - 1.0 - k * 0.06) / 0.25)
            if pt > 0:
                fade_paste(im, sp, (x, y + (1 - S.ease_out_cubic(pt)) * 10), int(255 * pt))
        if self.sett:
            self.sett.disegna(im, (self.xr, self.y_sett), tl - self.t_sett - 0.2, cursore=False)


# -------------------------------------------------------------------- icone
class Icone(Info):
    """`icona`, `n` piene che entrano una a una (o sulle `voci` ancorate), `fantasma`
    a contorno; sotto ognuna il suo numero, sotto la riga il `testo`."""

    def costruisci(self):
        c = self.c
        self.n, self.nf = int(c['n']), int(c.get('fantasma', 0))
        tot = self.n + self.nf
        self.I = int(min(92, (self.w - 2 * PAD) / tot - 14))
        self.passo = (self.w - 2 * PAD) / tot
        voci = c.get('voci') or []
        self.tempi = [self.voce_t(voci[i] if i < len(voci) else {}, i, 0.22, 0.35) for i in range(tot)]
        self.y_ic = self.y0
        self.f_n = mono(20)
        f_t = sans(30, 800)
        y = self.y_ic + self.I + 40
        self.testo_, n = _parole_a_capo(f_t, c.get('testo', ''), self.w - 2 * PAD, 36, PAD, y, S.PAPER)
        self.h = y + n * 36 + PAD - 4
        self.piena = icona(c['icona'], self.I, S.MINT, pieno=1)
        self.vuota = icona(c['icona'], self.I, S.PAPER + (110,), pieno=0, peso=300)
        self.glow, self.gp = bagliore(self.piena, 12, S.MINT, 0.7)
        self.stabile = max(self.tempi) + 1.2

    def disegna(self, im, tl):
        d = ImageDraw.Draw(im)
        for i, t0 in enumerate(self.tempi):
            u = tl - t0
            if u < 0:
                continue
            p = _cl(u / 0.35)
            fant = i >= self.n
            sp = self.vuota if fant else self.piena
            cx = PAD + self.passo * (i + 0.5)
            s2 = scala_px(sp, pop(p))
            if not fant and u < 0.6:
                fade_paste(im, self.glow, (cx - self.glow.width / 2, self.y_ic + self.I / 2 - self.glow.height / 2),
                           int(220 * (1 - u / 0.6)))
            fade_paste(im, s2, (cx - s2.width / 2, self.y_ic + self.I / 2 - s2.height / 2), int(255 * min(1, p * 2)))
            lab = f"{i + 1}{'?' if fant else ''}"
            lw = self.f_n.getlength(lab)
            d.text((cx - lw / 2, self.y_ic + self.I + 8), lab, font=self.f_n,
                   fill=(S.MUTED if fant else S.MINT) + (int(255 * p),))
        tt = self.tempi[-1] + 0.3
        for sp, x, y, k in self.testo_:
            pt = _cl((tl - tt - k * 0.05) / 0.25)
            if pt > 0:
                fade_paste(im, sp, (x, y + (1 - S.ease_out_cubic(pt)) * 10), int(255 * pt))


# -------------------------------------------------------------------- lista
class Lista(Info):
    """`voci: [{testo, segno, frase}]`: `segno` "si" (✓ menta), "no" (✗ e testo
    barrato), assente (numero). `annulla` (una frase) barra tutte le voci insieme,
    quando lei dice che erano il problema sbagliato."""

    def costruisci(self):
        c = self.c
        self.f = sans(c.get('corpo', 32), 800)
        lh = int(self.f.size * 1.22)
        self.M = 42
        x_t = PAD + self.M + 16
        y = self.y0 + 2
        self.voci = []
        for i, v in enumerate(c['voci']):
            righe = wrap_to(self.f, v['testo'], 0, self.w - x_t - PAD)
            sprites = []
            for li, ln in enumerate(righe):
                sp, pad = testo(ln, self.f, S.PAPER + (255,))
                spm, _ = testo(ln, self.f, S.MUTED + (255,))
                sprites.append((sp, spm, pad, x_t, y + li * lh, self.f.getlength(ln)))
            self.voci.append({'t': self.voce_t(v, i), 'segno': v.get('segno'), 'righe': sprites, 'y': y,
                              'hh': len(righe) * lh, 'n': i + 1})
            y += max(self.M, len(righe) * lh) + 16
        self.h = y - 16 + PAD
        self.annulla = c.get('annulla_t')
        self.f_n = mono(19)
        self.ic = {'si': icona('check', 28, S.NAVY_DEEP, peso=700), 'no': icona('close', 26, S.MUTED, peso=600)}
        fine = max(v['t'] for v in self.voci) + 0.9
        if self.annulla is not None:
            fine = max(fine, self.annulla + len(self.voci) * 0.09 + 0.6)
        self.stabile = fine

    def disegna(self, im, tl):
        d = ImageDraw.Draw(im)
        M = self.M
        for k, v in enumerate(self.voci):
            u = tl - v['t']
            if u < 0:
                continue
            p = _cl(u / 0.32)
            dx = (1 - S.ease_out_cubic(p)) * -26
            a = int(255 * p)
            barra = None
            if v['segno'] == 'no':
                barra = _cl((u - 0.35) / 0.3)
            if self.annulla is not None:
                pa = _cl((tl - self.annulla - k * 0.09) / 0.3)
                barra = max(barra or 0, pa) if pa > 0 else barra
            spenta = barra is not None and barra > 0.5
            # il marcatore
            q = pop(_cl(u / 0.3))
            cx, cy = PAD + M / 2 + dx, v['y'] + min(v['hh'], M) / 2 + 2
            r = M / 2 * q
            if v['segno'] == 'si':
                d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=S.MINT + (a,))
                ic = scala_px(self.ic['si'], q)
                fade_paste(im, ic, (cx - ic.width / 2, cy - ic.height / 2), a)
            elif v['segno'] == 'no':
                d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=S.MUTED + (a,), width=3)
                ic = scala_px(self.ic['no'], q)
                fade_paste(im, ic, (cx - ic.width / 2, cy - ic.height / 2), a)
            else:
                d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=S.MINT + (a,), width=3)
                lab = f"{v['n']:02d}"
                lw = self.f_n.getlength(lab)
                d.text((cx - lw / 2, cy - 12), lab, font=self.f_n, fill=S.MINT + (a,))
            for sp, spm, pad, x, y, lw in v['righe']:
                fade_paste(im, spm if spenta else sp, (x - pad + dx, y - pad), a)
                if barra:
                    yy = y + self.f.size * 0.62
                    d.line([(x + dx - 4, yy), (x + dx - 4 + (lw + 8) * S.ease_out_cubic(barra), yy)],
                           fill=S.PAPER + (int(230 * p),), width=4)


# ------------------------------------------------------------------- catena
class Catena(Info):
    """Causa -> effetto: `voci: [{testo, icona, frase}]`. Ogni nodo entra quando lei
    lo dice; il filo che lo collega al precedente si disegna con una goccia di luce."""
    D = 64

    def costruisci(self):
        c = self.c
        self.f = sans(c.get('corpo', 29), 800)
        lh = int(self.f.size * 1.2)
        D = self.D
        x_t = PAD + D + 20
        y = self.y0
        self.nodi = []
        for i, v in enumerate(c['voci']):
            righe = wrap_to(self.f, v['testo'], 0, self.w - x_t - PAD)
            hh = len(righe) * lh
            sprites = []
            ty = y + max(0, (D - hh) / 2)
            for li, ln in enumerate(righe):
                sp, pad = testo(ln, self.f, (S.MINT if i == len(c['voci']) - 1 else S.PAPER) + (255,))
                sprites.append((sp, pad, x_t, ty + li * lh))
            ic = icona(v['icona'], 36, S.MINT) if v.get('icona') else None
            self.nodi.append({'t': self.voce_t(v, i, 0.8), 'y': y, 'righe': sprites, 'ic': ic, 'n': i + 1})
            y += max(D, hh) + 38
        self.h = y - 38 + PAD
        self.f_n = mono(22)
        self.stabile = 1e9          # il nodo attivo pulsa

    def disegna(self, im, tl):
        D = self.D
        d = ImageDraw.Draw(im)
        cx = PAD + D / 2
        ultimo = max([k for k, n in enumerate(self.nodi) if tl >= n['t']], default=-1)
        for k, n in enumerate(self.nodi):
            u = tl - n['t']
            if u < 0:
                continue
            if k > 0:              # il filo dal nodo precedente
                y0 = self.nodi[k - 1]['y'] + D + 4
                y1 = n['y'] - 4
                pf = S.ease_in_out(u / 0.35)
                ye = y0 + (y1 - y0) * pf
                d.line([(cx, y0), (cx, ye)], fill=S.MINT + (200,), width=3)
                if pf < 1:
                    d.ellipse([cx - 6, ye - 6, cx + 6, ye + 6], fill=S.MINT + (255,))
                else:
                    d.polygon([(cx - 7, y1 - 9), (cx + 7, y1 - 9), (cx, y1)], fill=S.MINT + (220,))
            p = _cl((u - 0.25) / 0.35)
            if p <= 0:
                continue
            q = pop(p)
            cy = n['y'] + D / 2
            r = D / 2 * q
            if k == ultimo:
                pul = 0.5 + 0.5 * math.sin(tl * 5)
                rr = r + 4 + 5 * pul
                d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=S.MINT + (int(90 * pul),), width=3)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=S.NAVY_DEEP + (220,), outline=S.MINT + (255,), width=3)
            if n['ic']:
                ic = scala_px(n['ic'], q)
                fade_paste(im, ic, (cx - ic.width / 2, cy - ic.height / 2), int(255 * min(1, p * 2)))
            else:
                lab = str(n['n'])
                lw = self.f_n.getlength(lab)
                d.text((cx - lw / 2, cy - 14), lab, font=self.f_n, fill=S.MINT + (int(255 * p),))
            for sp, pad, x, y in n['righe']:
                fade_paste(im, sp, (x - pad + (1 - S.ease_out_cubic(p)) * 20, y - pad), int(255 * p))


# ---------------------------------------------------------------- citazione
class Citazione(Info):
    """La frase a karaoke dentro le virgolette: ogni parola si accende quando lei
    la dice. `testo` deve essere la frase come la dice; i tempi li mette `grafica`
    (`parole_t`)."""

    def costruisci(self):
        c = self.c
        f = sans(c.get('corpo', 44), 800)
        lh = int(f.size * 1.18)
        self.q, self.qp = testo('“', sans(170, 900), S.MINT + (255,), top=-30)
        y = self.y0 + 64
        self.parole = []
        words = c['testo'].split()
        tempi = c.get('parole_t') or [0.3 + i * 0.25 for i in range(len(words))]
        x, li = PAD, 0
        sp_w = f.getlength(' ')
        for i, wd in enumerate(words):
            ww = f.getlength(wd)
            if x + ww > self.w - PAD and x > PAD:
                x, li = PAD, li + 1
            st = {k: testo(wd, f, col + (255,)) for k, col in (('off', S.PAPER), ('on', S.MINT))}
            self.parole.append({'t': tempi[i], 'x': x, 'y': y + li * lh, 'st': st, 'w': ww})
            x += ww + sp_w
        self.h = y + (li + 1) * lh + 30 + PAD
        self.qc, _ = testo('”', sans(110, 900), S.MINT + (255,), top=-20)
        self.y_fine = y + (li + 1) * lh - 30
        self.stabile = self.parole[-1]['t'] + 1.0

    def disegna(self, im, tl):
        pq = _cl(tl / 0.4)
        q = scala_px(self.q, pop(pq))
        fade_paste(im, q, (PAD - 10 - self.qp, self.y0 - 30 - self.qp), int(255 * min(1, pq * 2)))
        for w in self.parole:
            u = tl - w['t']
            if u < -0.6:
                a, k = 60, 'off'
            elif u < 0:
                a, k = int(60 + 30 * (1 + u / 0.6)), 'off'
            elif u < 0.45:
                a, k = 255, 'on'
            else:
                a, k = 255, 'off'
            sp, pad = w['st'][k]
            dy = -4 * math.sin(math.pi * _cl(u / 0.3)) if 0 <= u < 0.3 else 0
            fade_paste(im, sp, (w['x'] - pad, w['y'] - pad + dy), a)
        pf = _cl((tl - self.parole[-1]['t'] - 0.2) / 0.3)
        if pf > 0:
            q2 = scala_px(self.qc, pop(pf))
            fade_paste(im, q2, (self.w - PAD - q2.width + 14, self.y_fine), int(255 * min(1, pf * 2)))


# ------------------------------------------------------------- legenda zone
class _ConZone(Info):
    """parte comune di anatomia e postura: zone numerate sulla figura che si
    accendono quando lei le nomina, e la legenda sotto"""
    HF = 380

    def _zone(self, y_leg):
        self.f_z = sans(27, 800)
        self.f_n = mono(18)
        self.zone = []
        y = y_leg
        for i, z in enumerate(self.c.get('zone', [])):
            # la voce lunga va a capo: oltre il pannello non si legge
            righe = [testo(r, self.f_z, S.PAPER + (255,)) for r in wrap_to(self.f_z, z['testo'], 0, self.w - 2 * PAD - 40)]
            self.zone.append({'t': self.voce_t(z, i, 0.9, 0.9), 'z': z['zona'], 'righe': righe, 'y': y, 'n': i + 1})
            y += 38 + 32 * (len(righe) - 1)
        return y

    def _marcatore(self, t, x, y, n, u, attiva):
        p = _cl(u / 0.35)
        if p <= 0:
            return
        q = pop(p)
        if attiva:
            pul = 0.5 + 0.5 * math.sin(u * 6)
            R = 22 + 10 * pul
            t.cerchio(x, y, R, outline=S.MINT + (int(140 * (1 - pul) + 40),), w=3)
        r = 15 * q
        t.cerchio(x, y, r, fill=S.MINT + (255,))
        return (x, y, n, p)

    def _numeri_su(self, im, marks, ox, oy):
        d = ImageDraw.Draw(im)
        for x, y, n, p in marks:
            lab = str(n)
            lw = self.f_n.getlength(lab)
            d.text((ox + x - lw / 2, oy + y - 12), lab, font=self.f_n, fill=S.NAVY_DEEP + (int(255 * p),))

    def _legenda(self, im, tl):
        d = ImageDraw.Draw(im)
        for z in self.zone:
            u = tl - z['t']
            if u < 0:
                continue
            p = _cl(u / 0.3)
            y = z['y']
            d.ellipse([PAD, y + 4, PAD + 26, y + 30], fill=S.MINT + (int(255 * p),))
            lab = str(z['n'])
            lw = self.f_n.getlength(lab)
            d.text((PAD + 13 - lw / 2, y + 5), lab, font=self.f_n, fill=S.NAVY_DEEP + (int(255 * p),))
            for k, (sp, pad) in enumerate(z['righe']):
                fade_paste(im, sp, (PAD + 40 - pad + (1 - S.ease_out_cubic(p)) * 16, y + 32 * k - pad), int(255 * p))


# ----------------------------------------------------------------- anatomia
def respiro(tl, periodo=3.4):
    """0 = espirazione (diaframma alto), 1 = inspirazione (diaframma basso)"""
    return (1 - math.cos(2 * math.pi * tl / periodo)) / 2


class Anatomia(_ConZone):
    """Vista frontale stilizzata: gabbia toracica, sterno, polmoni e diaframma che
    respira. `respiro: {escursione, etichetta}` (1.0 = la corsa piena, "3-4 CM"),
    `fantasma: {escursione, etichetta}` disegna tratteggiata la corsa di confronto.
    `zone: [{zona, testo, frase}]` con zona in diaframma, coste, sterno, cervicale,
    polmoni_bassi."""
    AMP = 44            # px di corsa per escursione 1.0

    def costruisci(self):
        self.fw = self.w - 2 * PAD
        self.cx = self.fw / 2 - 56
        self.top0 = 250
        y = self.y0 + self.HF + 8
        self.h = self._zone(y) + PAD - 6
        r = self.c.get('respiro') or {}
        self.esc = float(r.get('escursione', 1.0))
        fa = self.c.get('fantasma') or {}
        self.esc_f = float(fa['escursione']) if fa else None
        self.f_mis = sans(30, 900)
        self.f_mis2 = mono(17)
        self.etich = r.get('etichetta')
        self.etich_f = fa.get('etichetta') if fa else None
        # la misura compare quando lei la dice (`voci: [{frase}]`)
        voci = self.c.get('voci') or []
        self.t_mis = self.voce_t(voci[0], 0, inizio=0.5) if voci else 0.5

    def _dome(self, b, esc):
        """punti della cupola: si abbassa e si appiattisce in inspirazione"""
        cx, Wd = self.cx, 160
        top = self.top0 + esc * self.AMP * b
        k = 74 - 26 * esc * b
        pts = []
        for i in range(41):
            x = cx - Wd + 2 * Wd * i / 40
            u = (x - cx) / Wd
            y = top + k * u * u + 9 * math.exp(-((x - cx) / 36) ** 2)
            pts.append((x, y))
        return pts

    def disegna(self, im, tl):
        cx = self.cx
        t = Tela(self.fw, self.HF)
        ap = _cl(tl / 0.6)
        b = respiro(max(0.0, tl - 0.4)) if tl > 0.4 else 0.0
        dome = self._dome(b, self.esc)
        A = lambda a: int(a * ap)
        # colonna e collo
        t.tratteggio((cx, 30), (cx, self.HF - 20), S.PAPER + (A(40),), 3, 8, 7)
        for s in (-1, 1):
            t.linea([(cx + s * 26, 0), (cx + s * 30, 40)], S.PAPER + (A(110),), 3)
            t.linea([(cx + s * 12, 50), (cx + s * 120, 36), (cx + s * 150, 44)], S.PAPER + (A(150),), 5)
        # polmoni: il fondo segue la cupola
        dmap = {round(x): y for x, y in dome}

        def fondo(x):
            xs = min(dmap, key=lambda k: abs(k - x))
            return dmap[xs] - 6
        for s in (-1, 1):
            pts = [(cx + s * 34, 70), (cx + s * 62, 48), (cx + s * 96, 58), (cx + s * 132, 110), (cx + s * 150, 180)]
            xs = [cx + s * (150 - i * 116 / 10) for i in range(11)]
            pts += [(x, fondo(x) + (0 if abs(x - cx) > 60 else 0)) for x in xs]
            pts += [(cx + s * 30, fondo(cx + s * 34) - 30), (cx + s * 28, 130)]
            pts = curva_liscia(pts, 6)
            t.poligono(pts, fill=S.MINT + (A(34),))
            t.linea(pts + [pts[0]], S.MINT + (A(150),), 3, tondi=False)
        # costole e sterno
        for k in range(7):
            yk = 70 + k * 26
            hw = 112 + 10 * min(k, 4) - (k - 4) * 6 * (k > 4)
            for s in (-1, 1):
                pts = [(cx + s * 16, yk)]
                for j in range(1, 9):
                    u = j / 8
                    pts.append((cx + s * (16 + hw * math.sin(u * math.pi / 2)), yk + 8 + 34 * u ** 1.7))
                t.linea(pts, S.PAPER + (A(95),), 4)
        t.rett(cx - 11, 58, cx + 11, 196, 8, fill=S.PAPER + (A(150),))
        # il fantasma: la corsa di confronto
        mx = cx + 182
        if self.esc_f is not None:
            g = self._dome(1.0, self.esc_f)
            for a, b_ in zip(g[::2], g[1::2]):
                t.linea([a, b_], S.MINT + (A(110),), 3, tondi=False)
        # la cupola del diaframma
        t.linea(dome, S.MINT + (255 if ap >= 1 else A(255),), 8)
        # la misura: dove sta in alto, dove arriva in basso
        y_alto = self.top0 + 9
        y_basso = y_alto + self.esc * self.AMP
        y_cur = dome[20][1]
        pm = _cl((tl - self.t_mis) / 0.4)
        A = lambda a: int(a * ap * pm)
        if self.etich and pm > 0:
            t.tratteggio((cx + 40, y_alto), (mx + 10, y_alto), S.PAPER + (A(120),), 2, 6, 6)
            t.tratteggio((cx + 40, y_basso), (mx + 10, y_basso), S.MINT + (A(160),), 2, 6, 6)
            t.linea([(mx, y_alto), (mx, y_cur)], S.MINT + (A(255),), 4)
            t.cerchio(mx, y_cur, 7, fill=S.MINT + (A(255),))
        marks = []
        pos = {'diaframma': (cx, dome[20][1] - 2), 'coste': (cx + 78, 66), 'sterno': (cx, 124),
               'cervicale': (cx, 18), 'polmoni_bassi': (cx - 100, 214)}
        attiva = max([z['n'] for z in self.zone if tl >= z['t']], default=0)
        for z in self.zone:
            if tl >= z['t'] and z['z'] in pos:
                x, y = pos[z['z']]
                m = self._marcatore(t, x, y, z['n'], tl - z['t'], z['n'] == attiva)
                if m:
                    marks.append(m)
        im.alpha_composite(t.fine(), (PAD, self.y0))
        self._numeri_su(im, marks, PAD, self.y0)
        if self.etich:
            # la misura sta a destra della freccia, a meta della corsa
            sp, pad = testo(self.etich, self.f_mis, S.MINT + (255,))
            fade_paste(im, sp, (PAD + mx + 14 - pad, self.y0 + (y_alto + y_basso) / 2 - 18 - pad),
                       int(255 * pm))
        if self.etich_f:
            sp, pad = testo(self.etich_f, self.f_mis2, S.MUTED + (255,), 2)
            fade_paste(im, sp, (PAD + cx - 160 - pad, self.y0 + self._dome(1.0, self.esc_f)[0][1] + 10 - pad),
                       int(255 * _cl((tl - self.t_mis - 0.1) / 0.4)))
        self._legenda(im, tl)


# ------------------------------------------------------------------ postura
# figura seduta di profilo, guarda a destra: (x, y) nel riquadro 492 x 380
_ERETTA = {'bacino': (128, 246), 'lombare': (122, 204), 'torace': (120, 156), 'spalla': (124, 118),
           'collo': (128, 98), 'testa': (134, 64), 'gomito': (168, 186), 'mano': (300, 196),
           'ginocchio': (262, 246), 'piede': (268, 344)}
_AFFLOSCIATA = {'bacino': (152, 246), 'lombare': (146, 210), 'torace': (152, 160), 'spalla': (176, 128),
                'collo': (192, 112), 'testa': (226, 92), 'gomito': (214, 192), 'mano': (330, 196),
                'ginocchio': (276, 244), 'piede': (282, 344)}


class Postura(_ConZone):
    """Figura seduta davanti allo schermo che si affloscia: la sagoma eretta resta
    come fantasma tratteggiato. `zone: [{zona, testo, frase}]` con zona in testa,
    spalle, lombare, bacino, diaframma."""

    def costruisci(self):
        self.fw = self.w - 2 * PAD
        y = self.y0 + self.HF + 8
        self.h = self._zone(y) + PAD - 6

    @staticmethod
    def _corpo(t, P, col, w, testa_piena=True):
        sp = curva_liscia([P['bacino'], P['lombare'], P['torace'], P['spalla'], P['collo']], 8)
        t.linea(sp, col, w)
        t.linea([P['bacino'], P['ginocchio'], P['piede']], col, w * 0.9)
        t.linea([P['spalla'], P['gomito'], P['mano']], col, w * 0.7)
        hx, hy = P['testa']
        if testa_piena:
            t.cerchio(hx, hy, 25, fill=col)
        else:
            t.cerchio(hx, hy, 25, outline=col, w=3)

    def disegna(self, im, tl):
        t = Tela(self.fw, self.HF)
        ap = _cl(tl / 0.5)
        m = S.ease_in_out((tl - 0.5) / 1.4)
        P = {k: (a[0] + (_AFFLOSCIATA[k][0] - a[0]) * m, a[1] + (_AFFLOSCIATA[k][1] - a[1]) * m)
             for k, a in _ERETTA.items()}
        A = lambda a: int(a * ap)
        # sedia, scrivania, schermo
        t.linea([(84, 252), (232, 252)], S.MUTED + (A(200),), 7)
        t.linea([(88, 252), (70, 122)], S.MUTED + (A(200),), 7)
        t.linea([(100, 256), (100, 350)], S.MUTED + (A(150),), 5)
        t.linea([(220, 256), (220, 350)], S.MUTED + (A(150),), 5)
        t.linea([(318, 206), (478, 206)], S.MUTED + (A(200),), 7)
        t.rett(392, 84, 466, 156, 8, outline=S.PAPER + (A(170),), w=4)
        t.linea([(429, 156), (429, 204)], S.PAPER + (A(170),), 4)
        # la sagoma eretta resta come fantasma
        if m > 0.05:
            sp = curva_liscia([_ERETTA[k] for k in ('bacino', 'lombare', 'torace', 'spalla', 'collo')], 8)
            for a, b in zip(sp[::2], sp[1::2]):
                t.linea([a, b], S.MINT + (int(140 * m),), 3, tondi=False)
            t.cerchio(*_ERETTA['testa'], 25, outline=S.MINT + (int(140 * m),), w=2)
        self._corpo(t, P, S.PAPER + (A(235),), 24)
        # lo sguardo verso lo schermo
        hx, hy = P['testa']
        t.tratteggio((hx + 26, hy + 4), (392, 124), S.PAPER + (A(60),), 2, 5, 6)
        marks = []
        pos = {'testa': P['testa'], 'spalle': P['spalla'], 'lombare': ((P['lombare'][0] + 80) / 2, P['lombare'][1]),
               'bacino': P['bacino'], 'diaframma': ((P['torace'][0] + P['lombare'][0]) / 2 + 22, 186)}
        attiva = max([z['n'] for z in self.zone if tl >= z['t']], default=0)
        for z in self.zone:
            if tl >= z['t'] and z['z'] in pos:
                x, y = pos[z['z']]
                if z['z'] == 'lombare':       # il vuoto fra la schiena e lo schienale
                    t.tratteggio((80, y), (P['lombare'][0] - 12, y), S.MINT + (200,), 3, 5, 5)
                mk = self._marcatore(t, x, y, z['n'], tl - z['t'], z['n'] == attiva)
                if mk:
                    marks.append(mk)
        im.alpha_composite(t.fine(), (PAD, self.y0))
        self._numeri_su(im, marks, PAD, self.y0)
        self._legenda(im, tl)


# -------------------------------------------------------------------- curva
class Curva(Info):
    """Un andamento disegnato nel tempo: `valori` (0-1, a passi uguali), `base`
    (un livello tratteggiato, con `base_testo`), `etichette: [{x, testo, frase}]`
    (x da 0 a 1) che compaiono sul punto quando lei le dice. La linea avanza in
    modo da arrivare a ogni etichetta mentre lei la pronuncia. `asse_x`, `asse_y`:
    etichette strutturali degli assi."""
    HC = 250

    def costruisci(self):
        c = self.c
        self.x0, self.x1 = PAD + 26, self.w - PAD - 6
        self.yA, self.yB = self.y0 + 8, self.y0 + self.HC
        V = c['valori']
        X = lambda i: self.x0 + (self.x1 - self.x0) * i / (len(V) - 1)
        Y = lambda v: self.yB - (self.yB - self.yA) * v
        self.pts = curva_liscia([(X(i), Y(v)) for i, v in enumerate(V)], 20)
        self.Y = Y
        self.etich = []
        for i, e in enumerate(c.get('etichette', [])):
            sp, pad = testo(e['testo'], sans(23, 800), S.PAPER + (255,))
            self.etich.append({'x': float(e['x']), 't': self.voce_t(e, i, 1.2, 1.0), 'sp': sp, 'pad': pad})
        # quando la linea arriva a ogni x: alle etichette, nel momento in cui le dice
        kf = [(0.0, 0.35)] + sorted((e['x'], e['t']) for e in self.etich)
        kf.append((1.0, max(kf[-1][1] + 1.4, 2.4)))
        self.kf = kf
        self.f_ax = mono(17)
        self.h = self.yB + 34 + PAD - 4
        self.stabile = 1e9
        grad = Image.new('L', (1, self.HC), 0)
        for y in range(self.HC):
            grad.putpixel((0, y), int(120 * (1 - y / self.HC) ** 1.3))
        self.grad = grad.resize((self.w, self.HC))

    def _xp(self, tl):
        kf = self.kf
        if tl <= kf[0][1]:
            return 0.0
        for (xa, ta), (xb, tb) in zip(kf, kf[1:]):
            if tl <= tb:
                return xa + (xb - xa) * S.ease_in_out((tl - ta) / max(0.05, tb - ta))
        return 1.0

    def _y_at(self, x):
        best = min(self.pts, key=lambda p: abs(p[0] - x))
        return best[1]

    def disegna(self, im, tl):
        c = self.c
        d = ImageDraw.Draw(im)
        ap = _cl(tl / 0.4)
        for k in range(1, 4):
            y = self.yA + (self.yB - self.yA) * k / 4
            d.line([(self.x0, y), (self.x1, y)], fill=S.PAPER + (int(18 * ap),), width=1)
        d.line([(self.x0, self.yA), (self.x0, self.yB), (self.x1, self.yB)], fill=S.PAPER + (int(90 * ap),), width=2)
        if c.get('asse_y'):
            d.text((self.x0 + 8, self.yA - 4), c['asse_y'], font=self.f_ax, fill=S.MUTED + (int(220 * ap),))
        if c.get('asse_x'):
            lw = self.f_ax.getlength(c['asse_x'])
            d.text((self.x1 - lw, self.yB + 8), c['asse_x'], font=self.f_ax, fill=S.MUTED + (int(220 * ap),))
        t = Tela(self.w, self.h)
        if c.get('base') is not None:
            yb = self.Y(float(c['base']))
            if c.get('base_testo'):
                # a destra, sopra la linea: la curva li e gia lontana (salita o scesa)
                lw = self.f_ax.getlength(c['base_testo'])
                d.text((self.x1 - lw, yb - 24), c['base_testo'], font=self.f_ax, fill=S.MUTED + (int(230 * ap),))
            t.tratteggio((self.x0, yb), (self.x1, yb), S.PAPER + (int(140 * ap),), 2, 9, 7)
        xp = self.x0 + (self.x1 - self.x0) * self._xp(tl)
        vis = [p for p in self.pts if p[0] <= xp]
        if len(vis) >= 2:
            area = vis + [(vis[-1][0], self.yB), (vis[0][0], self.yB)]
            m = Image.new('L', im.size, 0)
            ImageDraw.Draw(m).polygon(area, fill=255)
            fill = Image.new('RGBA', im.size, S.MINT + (0,))
            g = Image.new('L', im.size, 0)
            g.paste(self.grad, (0, int(self.yA)))
            from PIL import ImageChops
            fill.putalpha(ImageChops.multiply(m, g))
            im.alpha_composite(fill)
            t.linea(vis, S.MINT + (255,), 6)
        lin = t.fine()
        glow, gp = bagliore(lin, 8, S.MINT, 0.5)
        im.alpha_composite(glow.crop((gp, gp, gp + im.width, gp + im.height)))
        im.alpha_composite(lin)
        if len(vis) >= 2 and self._xp(tl) < 1:
            x, y = vis[-1]
            d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=S.MINT + (255,))
            d.ellipse([x - 16, y - 16, x + 16, y + 16], outline=S.MINT + (110,), width=2)
        for e in self.etich:
            u = tl - e['t']
            if u < 0:
                continue
            p = _cl(u / 0.35)
            x = self.x0 + (self.x1 - self.x0) * e['x']
            y = self._y_at(x)
            d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=S.PAPER + (int(255 * p),), outline=S.MINT + (int(255 * p),), width=3)
            sp = e['sp']
            bw, bh = sp.width - 2 * e['pad'] + 28, sp.height - 2 * e['pad'] + 6
            sopra = y - bh - 22 > self.yA - 30
            if c.get('base') is not None and y > self.Y(float(c['base'])):
                sopra = False          # sotto la linea di partenza l'etichetta va sotto: sopra c'e la sua scritta
            bx = min(max(x - bw / 2, PAD), self.w - PAD - bw)
            by = y - bh - 18 if sopra else y + 18
            by += (1 - S.ease_out_cubic(p)) * (10 if sopra else -10)
            d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=bh // 2, fill=S.NAVY_DEEP + (int(235 * p),),
                                outline=S.MINT + (int(255 * p),), width=2)
            fade_paste(im, sp, (bx + 14 - e['pad'], by + 1 - e['pad']), int(255 * p))


TIPI = {'numero': Numero, 'barre': Barre, 'orologio': Orologio, 'icone': Icone, 'lista': Lista,
        'catena': Catena, 'citazione': Citazione, 'anatomia': Anatomia, 'postura': Postura, 'curva': Curva}


def crea(c):
    tipo = c.get('tipo', 'numero')
    if tipo not in TIPI:
        raise SystemExit(f"tipo di card sconosciuto: «{tipo}» (tipi: {', '.join(TIPI)})")
    return TIPI[tipo](c)


def misura(c):
    """larghezza e altezza del pannello: `inquadra` le usa per la distanza dal volto"""
    i = crea(c)
    return i.w, i.h

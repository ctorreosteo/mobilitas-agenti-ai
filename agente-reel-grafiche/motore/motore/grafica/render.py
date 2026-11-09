"""Il livello grafico, disegnato con Pillow e riversato in RGBA grezzo su stdout.

Questo ffmpeg non ha ne libass ne drawtext: il testo va rasterizzato fuori. Il
livello va dritto nella pipe di ffmpeg, senza file intermedi. Regge 24.000 frame
perche gli sprite si disegnano una volta sola e ogni banda di sottotitolo una
volta per parola attiva: da un frame all'altro cambia solo cosa si incolla.

Novita v2: i **titoli dietro**. Il titolo si scrive a tutta larghezza e si
ritaglia con la sagoma della persona (Vision, `data/sagome/`): passa dietro di
lei, non le copre mai il volto, e lo sfondo dietro si scurisce un poco per il
contrasto.

    python -m motore.grafica.render <slug> [secondi]    -> RGBA su stdout
"""
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .. import stile as S
from ..progetto import Progetto, ffmpeg

_fonts = {}


def sans(size, weight=900):
    k = ('s', size, weight)
    if k not in _fonts:
        f = ImageFont.truetype(S.FONT_SANS, size)
        f.set_variation_by_axes([weight])
        _fonts[k] = f
    return _fonts[k]


def mono(size):
    """etichette: dal 27/10/2026 Montserrat 500 (brand), non piu un monospaziato"""
    return sans(size, S.PESO['etichetta'])


def tracked_width(font, text, track_px):
    return sum(font.getlength(c) for c in text) + track_px * max(0, len(text) - 1)


def draw_tracked(d, xy, text, font, fill, track_px):
    x, y = xy
    for c in text:
        d.text((x, y), c, font=font, fill=fill)
        x += font.getlength(c) + track_px
    return x


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


# ---------------------------------------------------------------- sottotitoli
CAP_PAD_X, CAP_PAD_Y = 34, 20


class Sottotitoli:
    def __init__(self, caps, size=None, maxw=None):
        self.caps = caps
        self.size = size or S.SIZE['caption']
        self.maxw = maxw or S.CAPTION_MAXW
        self.cache = {}
        self.ci = 0

    def sprite(self, gi, active):
        key = (gi, active)
        if key in self.cache:
            return self.cache[key]
        g = self.caps[gi]
        f = sans(self.size, 900)
        track = S.TRACK['caption'] * self.size
        space = f.getlength(' ') + track
        widths = [tracked_width(f, w['t'], track) for w in g['words']]
        total = sum(widths) + space * (len(widths) - 1)
        h = int(self.size * 1.30)
        im = Image.new('RGBA', (int(total) + CAP_PAD_X * 2, h + CAP_PAD_Y * 2 + 10), (0, 0, 0, 0))
        im.alpha_composite(rounded(im.size, 20, S.NAVY_DEEP + (196,)))
        d = ImageDraw.Draw(im)
        x = CAP_PAD_X
        y = CAP_PAD_Y - int(self.size * 0.10)
        for i, w in enumerate(g['words']):
            col = S.MINT if i == active else S.PAPER
            draw_tracked(d, (x, y), w['t'], f, col + (255,), track)
            if i == active:
                d.rounded_rectangle([x, CAP_PAD_Y + h - 6, x + widths[i], CAP_PAD_Y + h - 1],
                                    radius=3, fill=S.MINT + (255,))
            x += widths[i] + space
        if len(self.cache) > 40:
            self.cache.clear()
        self.cache[key] = im
        return im

    def disegna(self, base, t, cx, bottom, nascosti=()):
        caps = self.caps
        if not caps or any(a <= t < b for a, b in nascosti):
            return
        while self.ci + 1 < len(caps) and caps[self.ci]['e'] < t:
            self.ci += 1
        while self.ci > 0 and caps[self.ci]['s'] > t:
            self.ci -= 1
        g = caps[self.ci]
        if not (g['s'] - 0.05 <= t < g['e']):
            return
        active = -1
        for i, w in enumerate(g['words']):
            if w['s'] - 0.02 <= t < w['e'] + 0.06:
                active = i
                break
            if t >= w['e']:
                active = i
        sp = self.sprite(self.ci, active)
        p = min(max((t - g['s']) / S.CAP_IN, 0.0), 1.0)
        rise = int(S.CAP_RISE * (1 - S.ease_out_cubic(p)))
        fade_paste(base, sp, (int(cx - sp.width / 2), bottom - sp.height + rise), int(255 * p))


# ---------------------------------------------------------------------- card
def card_sprite(c):
    w = S.CARD_W
    pad = 34
    f_eye, f_val, f_unit, f_sub = mono(S.SIZE['eyebrow']), sans(S.SIZE['card_value'], 900), \
        sans(S.SIZE['card_unit'], 800), sans(S.SIZE['card_sub'], 600)
    track_e = S.TRACK['eyebrow'] * S.SIZE['eyebrow']
    sub_lines = wrap_to(f_sub, c['sub'], 0, w - pad * 2)
    h = pad + S.SIZE['eyebrow'] + 16 + 6 + 26 + S.SIZE['card_value'] + 18 \
        + len(sub_lines) * int(S.SIZE['card_sub'] * 1.35) + pad
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    im.alpha_composite(rounded((w, h), 26, S.NAVY + (238,)))
    d = ImageDraw.Draw(im)
    y = pad
    draw_tracked(d, (pad, y), c['eyebrow'], f_eye, S.MINT + (255,), track_e)
    y += S.SIZE['eyebrow'] + 16
    d.rounded_rectangle([pad, y, pad + 84, y + 5], radius=2, fill=S.MINT + (255,))
    y += 26
    vw = f_val.getlength(c['value'])
    d.text((pad, y - int(S.SIZE['card_value'] * 0.16)), c['value'], font=f_val, fill=S.MINT + (255,))
    d.text((pad + vw + 12, y + S.SIZE['card_value'] - S.SIZE['card_unit'] - 14),
           c['unit'], font=f_unit, fill=S.PAPER + (255,))
    y += S.SIZE['card_value'] + 18
    for ln in sub_lines:
        d.text((pad, y), ln, font=f_sub, fill=S.MUTED + (255,))
        y += int(S.SIZE['card_sub'] * 1.35)
    return im


def chapter_sprite(c):
    """scheda piena navy: solo per i capitoli NON dietro"""
    im = Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (238,))
    d = ImageDraw.Draw(im)
    f_eye = mono(S.SIZE['eyebrow'] + 6)
    f_t = sans(S.SIZE['chapter'], 900)
    track_e = S.TRACK['eyebrow'] * (S.SIZE['eyebrow'] + 6)
    ew = tracked_width(f_eye, c['eyebrow'], track_e)
    y = S.H // 2 - 150
    draw_tracked(d, ((S.W - ew) / 2, y), c['eyebrow'], f_eye, S.MINT + (255,), track_e)
    y += S.SIZE['eyebrow'] + 30
    d.rounded_rectangle([S.W / 2 - 60, y, S.W / 2 + 60, y + 6], radius=3, fill=S.MINT + (255,))
    y += 42
    for i, ln in enumerate((c['l1'], c['l2'])):
        tw = tracked_width(f_t, ln, S.TRACK['chapter'] * S.SIZE['chapter'])
        draw_tracked(d, ((S.W - tw) / 2, y), ln, f_t, (S.PAPER if i == 0 else S.MINT) + (255,),
                     S.TRACK['chapter'] * S.SIZE['chapter'])
        y += int(S.SIZE['chapter'] * 1.16)
    return im


# ------------------------------------------------------------ titoli dietro
class Dietro:
    """Titolo gigante dietro la persona. Due righe, la prima in paper e la seconda
    in menta, che salgono dal basso una dopo l'altra; sopra, l'eyebrow mono."""

    def __init__(self, c, sagome, fps):
        self.c = c
        self.fps = fps
        self.sagome = sagome
        maxw = S.W - 2 * S.SAFE
        size = S.SIZE['behind']
        lines = [c['l1'], c['l2']]
        while True:
            f = sans(size, 900)
            tr = S.TRACK['behind'] * size
            if max(tracked_width(f, l, tr) for l in lines) <= maxw or size < 90:
                break
            size -= 6
        self.size, self.f, self.tr = size, f, tr
        self.lh = lh = int(size * 0.98)
        self.mask_cache = {}
        # ogni riga si disegna parola per parola, per sapere dove sta ogni parola
        self.righe = []
        for i, l in enumerate(lines):
            words, x, sp = [], 0.0, f.getlength(' ') + tr
            for wd in l.split():
                ww = tracked_width(f, wd, tr)
                words.append((wd, x, ww))
                x += ww + sp
            self.righe.append((l, words, x - sp, (S.PAPER if i == 0 else S.MINT)))
        # dove comincia davvero il disegno delle lettere nella riga (bordo alto delle maiuscole)
        prova = Image.new('L', (S.W, lh + int(size * 0.3)), 0)
        draw_tracked(ImageDraw.Draw(prova), (0, -int(size * 0.12)), self.righe[0][0], f, 255, tr)
        self.glyph_top = prova.getbbox()[1] if prova.getbbox() else 0
        self.eb_h = S.SIZE['eyebrow'] + 8
        top, dx, self.coperto = self._posizione()
        self.lines = []
        for i, (l, words, w, col) in enumerate(self.righe):
            im = Image.new('RGBA', (S.W, lh + int(size * 0.3)), (0, 0, 0, 0))
            draw_tracked(ImageDraw.Draw(im), ((S.W - w) / 2 + dx[i], -int(size * 0.12)), l, f, col + (255,), tr)
            self.lines.append((im, top + i * lh))
        imgs = [(None, self.righe[0][2])]
        self.dx0 = dx[0]
        # l'eyebrow sta SOPRA la persona (non mascherato), allineato a sinistra
        # della prima riga: dietro la testa sparirebbe
        fe = mono(S.SIZE['eyebrow'] + 8)
        tre = S.TRACK['eyebrow'] * (S.SIZE['eyebrow'] + 8)
        ew = tracked_width(fe, c['eyebrow'], tre)
        eb = Image.new('RGBA', (int(ew) + 4, S.SIZE['eyebrow'] + 30), (0, 0, 0, 0))
        draw_tracked(ImageDraw.Draw(eb), (2, 0), c['eyebrow'], fe, S.MINT + (255,), tre)
        x_eb = int((S.W - imgs[0][1]) / 2 + self.dx0) + 8
        self.eyebrow = (eb, (x_eb, top + self.glyph_top - 22 - self.eb_h))

    def _posizione(self):
        """dove mettere le righe perche la persona nasconda meno lettere possibile.

        Si misura sulle sagome vere della finestra del titolo. Il criterio e la
        PAROLA PEGGIORE, non la media: "NON M..BOLICO" non si legge anche se in
        media e coperto solo il 20%. Ogni riga puo scorrere in orizzontale, cosi
        la testa tende a cadere sugli spazi fra le parole.
        """
        n0, n1 = int(round(self.c['s'] * self.fps)), int(round(self.c['e'] * self.fps))
        ms = [self.maschera(n) for n in (n0 + 2, (n0 + n1) // 2, n1 - 3)]
        ms = [m for m in ms if m is not None]
        default = int(S.H * 0.40 - self.lh)
        if not ms:
            return default, [0] * len(self.righe), None
        m = np.maximum.reduce(ms)
        h_txt = int(self.size * 0.72)          # altezza delle maiuscole
        best = None
        y_min = 44 + self.eb_h + 22 - self.glyph_top        # spazio per l'eyebrow sopra
        for top in range(max(int(S.H * 0.05), y_min), int(S.H * 0.72) - 2 * self.lh, 12):
            dxs, worst_all = [], 0.0
            for i, (l, words, w, _) in enumerate(self.righe):
                y = top + i * self.lh + int(self.size * 0.02)
                prof = m[y:y + h_txt].mean(axis=0)            # copertura per colonna
                cum = np.concatenate([[0.0], np.cumsum(prof)])
                lim = int((S.W - w) / 2 - S.SAFE // 2)
                bw = None
                for dx in range(-min(260, lim), min(260, lim) + 1, 16):
                    x0 = (S.W - w) / 2 + dx
                    worst = 0.0
                    for _, wx, ww in words:
                        a_, b_ = int(x0 + wx), int(x0 + wx + ww)
                        a_, b_ = max(0, a_), min(S.W, b_)
                        worst = max(worst, (cum[b_] - cum[a_]) / max(1, b_ - a_))
                    sc = worst + 0.0004 * abs(dx) / 16
                    if bw is None or sc < bw[0]:
                        bw = (sc, dx, worst)
                dxs.append(bw[1])
                worst_all = max(worst_all, bw[2])
            score = worst_all + 0.0003 * (top - S.H * 0.05) / 12
            if best is None or score < best[0]:
                best = (score, top, dxs, worst_all)
        return best[1], best[2], round(best[3], 3)

    def maschera(self, n):
        """sagoma della persona al frame n del montato, ammorbidita nel tempo e nello spazio"""
        if n in self.mask_cache:
            return self.mask_cache[n]
        acc, k = None, 0
        for m in (n - 1, n, n + 1):
            p = self.sagome / f"f{m:06d}.png"
            if p.exists():
                a = np.asarray(Image.open(p).convert('L'), dtype=np.float32)
                acc = a if acc is None else acc + a
                k += 1
        if acc is None:
            res = None
        else:
            im = Image.fromarray((acc / k).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.6))
            res = np.asarray(im, dtype=np.float32) / 255.0
        if len(self.mask_cache) > 6:
            self.mask_cache.clear()
        self.mask_cache[n] = res
        return res

    def disegna(self, base, t, n):
        c = self.c
        if not (c['s'] <= t < c['e']):
            return
        layer = Image.new('RGBA', (S.W, S.H), (0, 0, 0, 0))
        uscita = min(1.0, (c['e'] - t) / S.BEHIND_OUT)
        # velo navy sullo sfondo, per il contrasto della menta sul teal
        dim = int(120 * min(1.0, (t - c['s']) / 0.25) * uscita)
        layer.paste(S.NAVY_DEEP + (dim,), (0, 0, S.W, S.H))
        for i, (im, y) in enumerate(self.lines):
            p = S.ease_out_expo((t - c['s'] - i * 0.12) / S.BEHIND_IN)
            if p <= 0:
                continue
            dy = int((1 - p) * self.size * 0.55)
            a = int(255 * min(1.0, p * 1.6) * uscita)
            fade_paste(layer, im, (0, y + dy), a)
        m = self.maschera(n)
        if m is not None:
            arr = np.asarray(layer, dtype=np.float32)
            arr[..., 3] *= (1.0 - m)
            layer = Image.fromarray(arr.astype(np.uint8), 'RGBA')
        pe = S.ease_out_cubic((t - c['s'] - 0.05) / 0.3)
        fade_paste(layer, self.eyebrow[0], self.eyebrow[1], int(255 * pe * uscita))
        base.alpha_composite(layer)


def lockup_sprite(c):
    f_eye, f_t = mono(S.SIZE['eyebrow']), sans(S.SIZE['hook'], 900)
    track_e = S.TRACK['eyebrow'] * S.SIZE['eyebrow']
    track_t = S.TRACK['chapter'] * S.SIZE['hook']
    maxw = S.CARD_W - 68
    lines, mark = [], []
    for i, ln in enumerate((c['l1'], c['l2'])):
        for w_ in wrap_to(f_t, ln, track_t, maxw):
            lines.append(w_)
            mark.append(i)
    # l'eyebrow non si taglia: se non entra si stringe la spaziatura, poi il corpo
    es = S.SIZE['eyebrow']
    while tracked_width(f_eye, c['eyebrow'], track_e) > maxw and es > 16:
        if track_e > 0.10 * es:
            track_e = 0.10 * es
        else:
            es -= 1
            f_eye = mono(es)
            track_e = 0.10 * es
    w = int(max(tracked_width(f_eye, c['eyebrow'], track_e),
                max(tracked_width(f_t, l, track_t) for l in lines))) + 68
    h = 34 + S.SIZE['eyebrow'] + 18 + 6 + 26 + len(lines) * int(S.SIZE['hook'] * 1.10) + 30
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    im.alpha_composite(rounded((w, h), 26, S.NAVY_DEEP + (216,)))
    d = ImageDraw.Draw(im)
    y = 34
    draw_tracked(d, (34, y), c['eyebrow'], f_eye, S.MINT + (255,), track_e)
    y += S.SIZE['eyebrow'] + 18
    d.rounded_rectangle([34, y, 118, y + 5], radius=2, fill=S.MINT + (255,))
    y += 26
    for i, ln in enumerate(lines):
        draw_tracked(d, (34, y), ln, f_t, (S.PAPER if mark[i] == 0 else S.MINT) + (255,), track_t)
        y += int(S.SIZE['hook'] * 1.10)
    return im


def chip_v3_sprite(c):
    """chip del brand dal sito (fase 7c, Riccardo): il pittogramma (non ricolorato) su un
    disco panna a sinistra, nome in Montserrat 700, ruolo in 500 al 70%, pannello blu notte"""
    f_n, f_r = sans(52, 700), sans(S.SIZE['chip_role_v2'], 500)
    h = 104 + S.SIZE['chip_role_v2']
    D = h - 36
    x_t = 18 + D + 30
    w = int(max(f_n.getlength(c['name']), f_r.getlength(c['role']))) + x_t + 44
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    im.alpha_composite(rounded((w, h), h // 2, S.NAVY + (255,)))
    k = 4   # disco disegnato a 4x e ridotto: bordo pulito
    disco = Image.new('RGBA', (D * k, D * k), (0, 0, 0, 0))
    ImageDraw.Draw(disco).ellipse([0, 0, D * k - 1, D * k - 1], fill=S.PAPER + (255,))
    pg = Image.open(S.PITTOGRAMMA).convert('RGBA')
    pg = pg.crop(pg.getbbox())
    lato = int(D * k * 0.80)
    pg.thumbnail((lato, lato), Image.LANCZOS)
    disco.alpha_composite(pg, ((D * k - pg.width) // 2, (D * k - pg.height) // 2))
    im.alpha_composite(disco.resize((D, D), Image.LANCZOS), (18, 18))
    d = ImageDraw.Draw(im)
    d.text((x_t, 22), c['name'], font=f_n, fill=S.PAPER + (255,))
    d.text((x_t + 2, 90), c['role'], font=f_r, fill=S.MUTED + (255,))
    return im


def chip_v2_sprite(c):
    """chip del brand: nome in Montserrat 300, ruolo in 500 al 76%, filetto verde,
    pannello blu notte. Niente maiuscolo spaziato."""
    f_n, f_r = sans(52, 300), sans(S.SIZE['chip_role_v2'], 500)
    w = int(max(f_n.getlength(c['name']), f_r.getlength(c['role']))) + 62 + 44
    h = 104 + S.SIZE['chip_role_v2']
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    im.alpha_composite(rounded((w, h), 18, S.NAVY + (255,)))
    d = ImageDraw.Draw(im)
    d.rectangle([34, 36, 38, h - 36], fill=S.MINT + (255,))
    d.text((62, 26), c['name'], font=f_n, fill=S.PAPER + (255,))
    d.text((64, 92), c['role'], font=f_r, fill=S.MUTED + (255,))
    return im


def _righe_bilanciate(parole, size, maxw):
    """a capo bilanciato: lo stesso numero di righe del primo a capo possibile,
    ma con le righe di lunghezza simile (niente parola sola sull'ultima riga)"""
    def a_capo(lim):
        righe, cur, lw = [], [], 0
        for p, k in parole:
            pw = sans(size, 800 if k else 300).getlength(p + ' ')
            if cur and lw + pw > lim:
                righe.append(cur)
                cur, lw = [], 0
            cur.append((p, k))
            lw += pw
        return righe + ([cur] if cur else [])
    righe = a_capo(maxw)
    lo, hi = maxw * 0.4, maxw
    for _ in range(14):
        mid = (lo + hi) / 2
        if len(a_capo(mid)) <= len(righe):
            hi = mid
        else:
            lo = mid
    return a_capo(hi)


def frase_chiave_sprite(c):
    """sottotitolo variante B: il testo del pannello a tutta altezza sul lato libero
    (la persona e spostata dall'altro), la frase in Montserrat 300 e la parola chiave
    in 800 verde. Con 'freccia' una freccia verso il basso (la descrizione). Il
    pannello (blu notte pieno) lo disegna la scena: cosi fra due elementi di fila
    sullo stesso lato il pannello resta e cambia solo il testo."""
    w, h = S.PANNELLO_W, S.H
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    size, x0 = 72, 96
    maxw = w - x0 - S.PANNELLO_MARGINE
    testo, chiave = c['testo'], c.get('chiave') or ''
    i = testo.lower().rfind(chiave.lower()) if chiave else -1
    parole = [(p, False) for p in testo[:i].split()] + [(p, True) for p in testo[i:].split()] if i >= 0 \
        else [(p, False) for p in testo.split()]
    righe = _righe_bilanciate(parole, size, maxw)
    lh = int(size * 1.2)
    y = int(h * 0.42 - len(righe) * lh / 2)
    for r in righe:
        x = x0
        for p, k in r:
            f = sans(size, 800 if k else 300)
            d.text((x, y), p, font=f, fill=(S.MINT if k else S.PAPER) + (255,))
            x += f.getlength(p + ' ')
        y += lh
    if c.get('freccia'):
        cx, y0 = x0 + 30, y + 60
        d.line([(cx, y0), (cx, y0 + 110)], fill=S.MINT + (255,), width=8)
        d.line([(cx - 26, y0 + 82), (cx, y0 + 112), (cx + 26, y0 + 82)], fill=S.MINT + (255,), width=8, joint='curve')
    return im


def chip_sprite(c):
    f_n, f_r = sans(S.SIZE['chip_name'], 900), mono(S.SIZE['chip_role'])
    track_r = S.TRACK['eyebrow'] * S.SIZE['chip_role']
    w = int(max(f_n.getlength(c['name']), tracked_width(f_r, c['role'], track_r))) + 64
    h = 30 + S.SIZE['chip_name'] + 14 + S.SIZE['chip_role'] + 30
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    im.alpha_composite(rounded((w, h), 20, S.NAVY_DEEP + (216,)))
    d = ImageDraw.Draw(im)
    d.text((32, 24), c['name'], font=f_n, fill=S.PAPER + (255,))
    draw_tracked(d, (32, 30 + S.SIZE['chip_name'] + 12), c['role'], f_r, S.MINT + (255,), track_r)
    return im


def closing_sprite(c):
    im = Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (246,))
    d = ImageDraw.Draw(im)
    f_eye, f_t, f_cta, f_br = mono(S.SIZE['eyebrow'] + 6), sans(S.SIZE['chapter'], 900), \
        mono(S.SIZE['chapter_sub']), mono(S.SIZE['eyebrow'])
    tr = S.TRACK['eyebrow']
    y = S.H // 2 - 210
    ew = tracked_width(f_eye, c['eyebrow'], tr * (S.SIZE['eyebrow'] + 6))
    draw_tracked(d, ((S.W - ew) / 2, y), c['eyebrow'], f_eye, S.MINT + (255,), tr * (S.SIZE['eyebrow'] + 6))
    y += S.SIZE['eyebrow'] + 34
    d.rounded_rectangle([S.W / 2 - 60, y, S.W / 2 + 60, y + 6], radius=3, fill=S.MINT + (255,))
    y += 46
    for i, ln in enumerate((c['l1'], c['l2'])):
        tw = tracked_width(f_t, ln, S.TRACK['chapter'] * S.SIZE['chapter'])
        draw_tracked(d, ((S.W - tw) / 2, y), ln, f_t, (S.PAPER if i == 0 else S.MINT) + (255,),
                     S.TRACK['chapter'] * S.SIZE['chapter'])
        y += int(S.SIZE['chapter'] * 1.16)
    y += 34
    cw = tracked_width(f_cta, c['cta'], tr * S.SIZE['chapter_sub'])
    box_w, box_h = cw + 96, S.SIZE['chapter_sub'] + 56
    d.rounded_rectangle([(S.W - box_w) / 2, y, (S.W + box_w) / 2, y + box_h],
                        radius=14, outline=S.MINT + (255,), width=4)
    draw_tracked(d, ((S.W - cw) / 2, y + 26), c['cta'], f_cta, S.MINT + (255,), tr * S.SIZE['chapter_sub'])
    y += box_h + 46
    bw = tracked_width(f_br, c['brand'], tr * S.SIZE['eyebrow'])
    draw_tracked(d, ((S.W - bw) / 2, y), c['brand'], f_br, S.MUTED + (255,), tr * S.SIZE['eyebrow'])
    return im


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


def _x(c, w):
    return S.SAFE if c.get('side', 'left') == 'left' else S.W - S.SAFE - w


class Scene:
    """Tiene gli sprite gia disegnati: si costruiscono una volta sola."""

    def __init__(self, P):
        plan = P.leggi('grafica.json')
        self.plan = plan
        self.fps = P.fps
        sag = P.p('data', 'sagome')
        self.cards = [(c, card_sprite(c)) for c in plan['cards']]
        self.full = [(c, chapter_sprite(c)) for c in plan['capitoli'] if not c['dietro']]
        self.dietro = [Dietro(c, sag, self.fps) for c in plan['capitoli'] if c['dietro']]
        self.lock = (plan['opening'], lockup_sprite(plan['opening'])) if plan.get('opening') else None
        self.chip = None
        if plan.get('chip'):
            st = plan['chip'].get('stile')
            sp = chip_v3_sprite if st == 'v3' else chip_v2_sprite if st == 'v2' else chip_sprite
            self.chip = (plan['chip'], sp(plan['chip']))
        self.chiave = [(c, frase_chiave_sprite(c)) for c in plan.get('frasi_chiave', [])]
        self.close = (plan['closing'], closing_sprite(plan['closing'])) if plan.get('closing') else None
        self.subs = Sottotitoli(plan['captions'])
        self.nascosti = [(c['s'], c['e']) for c in plan['capitoli']]
        if plan.get('closing'):
            self.nascosti.append((plan['closing']['s'], plan['closing']['e']))
        for d in self.dietro:
            sys.stderr.write(f"  titolo dietro «{d.c['l1']} {d.c['l2']}»: parola peggiore coperta "
                             f"{'?' if d.coperto is None else f'{d.coperto*100:.0f}%'}\n")
        self.dur = plan['duration']
        self.barra = plan.get('barra', True)

    def frame(self, n):
        t = n / self.fps
        base = Image.new('RGBA', (S.W, S.H), (0, 0, 0, 0))
        for d in self.dietro:
            d.disegna(base, t, n)
        # sottotitoli variante B: frasi chiave sul pannello laterale (entra dal suo lato)
        for c, sp in self.chiave:
            # entra/esce False: l'elemento prima o dopo usa lo stesso pannello, che
            # resta fermo (cambia solo il testo); ritardo: aspetta lo stacco d'inquadratura
            t0 = c['s'] + c.get('ritardo', 0.0)
            if not (t0 <= t < c['e']):
                continue
            fuori = -sp.width if c['lato'] == 'sx' else sp.width
            p = S.ease_out_expo((t - t0) / 0.5) if c.get('entra', True) else 1.0
            q = S.ease_out_cubic(max(0.0, (t - (c['e'] - 0.32)) / 0.32)) if c.get('esce', True) else 0.0
            x0 = 0 if c['lato'] == 'sx' else S.W - sp.width
            x = int(x0 + fuori * (1 - p) + fuori * q)
            ImageDraw.Draw(base).rectangle([x, 0, x + sp.width - 1, S.H], fill=S.NAVY + (255,))
            a = 1.0
            if not c.get('entra', True):
                a = min(a, (t - t0) / 0.25)
            if not c.get('esce', True):
                a = min(a, (c['e'] - t) / 0.2)
            fade_paste(base, sp, (x, 0), int(255 * max(0.0, min(1.0, a))))
        dd = ImageDraw.Draw(base)
        # barra d'avanzamento in panna (il verde va solo sul blu), tranne nei mid-roll
        if self.barra:
            dd.rectangle([0, S.H - S.PROGRESS_H, S.W, S.H], fill=S.PAPER + (40,))
            dd.rectangle([0, S.H - S.PROGRESS_H, int(S.W * t / self.dur), S.H], fill=S.PAPER + (170,))

        for item in (self.lock, self.chip):
            if not item:
                continue
            c, sp = item
            if item is self.chip and c.get('stile') in ('v2', 'v3'):
                if c['s'] <= t < c['e']:
                    a = min((t - c['s']) / 0.35, (c['e'] - t) / 0.3, 1.0)
                    rise = int(18 * (1 - S.ease_out_expo((t - c['s']) / 0.45)))
                    fade_paste(base, sp, (S.SAFE, 760 + rise), int(255 * max(a, 0)))
                continue
            if c['s'] <= t < c['e']:
                a = min((t - c['s']) / 0.45, (c['e'] - t) / 0.45, 1.0)
                rise = int(S.CARD_RISE * (1 - S.ease_out_expo((t - c['s']) / S.CARD_IN)))
                fade_paste(base, sp, (_x(c, sp.width), S.CARD_TOP + rise), int(255 * max(a, 0)))

        for c, sp in self.cards:
            if not (c['s'] <= t < c['e']):
                continue
            rev = S.ease_out_expo((t - c['s']) / S.CARD_IN)
            rise = int(S.CARD_RISE * (1 - rev))
            a = 255 if t < c['e'] - S.CARD_OUT else int(255 * max(0.0, (c['e'] - t) / S.CARD_OUT))
            wv = max(1, int(sp.width * rev))
            if c.get('side', 'left') == 'left':
                fade_paste(base, sp.crop((0, 0, wv, sp.height)), (S.SAFE, S.CARD_TOP + rise), a)
            else:
                fade_paste(base, sp.crop((sp.width - wv, 0, sp.width, sp.height)),
                           (S.W - S.SAFE - wv, S.CARD_TOP + rise), a)

        for c, sp in self.full + ([self.close] if self.close else []):
            if not (c['s'] <= t < c['e']):
                continue
            a = min(S.ease_out_cubic((t - c['s']) / S.CHAPTER_IN),
                    S.ease_out_cubic((c['e'] - t) / S.CHAPTER_OUT), 1.0)
            fade_paste(base, sp, (0, 0), int(255 * max(a, 0)))

        self.subs.disegna(base, t, S.W / 2, S.CAPTION_BOT, self.nascosti)
        return base


def stream(slug, limite=None):
    P = Progetto(slug)
    scene = Scene(P)
    total = P.leggi('edl.json')['frame']
    if limite:
        total = min(total, int(limite * P.fps) + 2)
    out = sys.stdout.buffer
    t0 = time.time()
    try:
        for n in range(total):
            out.write(scene.frame(n).tobytes())
            if n % 1800 == 0 and n:
                el = time.time() - t0
                sys.stderr.write(f"\n  grafica: frame {n}/{total}, {n/el:.0f} fps, "
                                 f"restano {(total-n)/(n/el)/60:.1f} min\n")
        out.flush()
    except BrokenPipeError:
        pass        # ffmpeg ha chiuso la pipe (es. -t): normale


def anteprima(slug, tempi=None):
    """compone la grafica sopra i frame veri del montato pulito: va guardata
    PRIMA del render lungo, gli errori di posizione si vedono solo li"""
    P = Progetto(slug)
    if not tempi:
        G0 = P.leggi('grafica.json')
        if G0.get('inserti') or G0.get('frasi_chiave') or G0.get('broll'):
            # grafica v2: inserti HyperFrames e B-roll non sono nel livello Pillow; il
            # foglio (un fotogramma per elemento) si fa sulla composizione vera, la
            # stessa di `finale --anteprima`
            from ..monta import finale
            return finale(slug, anteprima=True)
    scene = Scene(P)
    G = scene.plan
    video = P.render(f"{slug}_pulito.mp4")
    if not tempi:
        tempi = [2.0]
        if G.get('chip'):
            tempi.append(G['chip']['s'] + 2.0)
        tempi += [c['s'] + 1.5 for c in G['cards']]
        tempi += [c['s'] + 0.35 for c in G['capitoli']] + [c['s'] + 1.4 for c in G['capitoli']]
        tempi += [c['s'] + 0.6 for c in G['enfasi'][:3]]
        if G.get('closing'):
            c = G['closing']
            tempi.append(min(c['s'] + 2.5, (c['s'] + c['e']) / 2))   # chiusure corte: a meta
    # oltre l'ultimo frame ffmpeg non estrae niente (e non da errore)
    ultimo = (G['frames'] - 1) / P.fps
    tempi = sorted({round(min(max(0.0, t), ultimo), 2) for t in tempi})
    out = P.controllo('anteprima')
    out.mkdir(exist_ok=True)
    for f in out.glob('*.jpg'):
        f.unlink()
    tiles = []
    for t in sorted(tempi):
        n = int(round(t * P.fps))
        png = out / f"t{t:07.2f}.png"
        ffmpeg('-ss', f"{n / P.fps:.4f}", '-i', video, '-frames:v', '1', png)
        if not png.exists():
            sys.exit(f"anteprima: nessun fotogramma a {t:.2f}s in {video.name}")
        bg = Image.open(png).convert('RGBA')
        bg.alpha_composite(scene.frame(n))
        jpg = png.with_suffix('.jpg')
        bg.convert('RGB').resize((960, 540), Image.LANCZOS).save(jpg, quality=88)
        png.unlink()
        tiles.append(jpg)
    cols = 3
    rows = -(-len(tiles) // cols)
    ffmpeg('-pattern_type', 'glob', '-i', str(out / '*.jpg'), '-filter_complex',
           f'tile={cols}x{rows}:margin=8:padding=6', '-frames:v', '1', P.controllo('anteprima.jpg'))
    print(f"{len(tiles)} fotogrammi -> controlli/anteprima.jpg (singoli in controlli/anteprima/)")


if __name__ == '__main__':
    stream(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else None)

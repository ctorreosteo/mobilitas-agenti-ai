"""Il livello grafico, disegnato con Pillow e riversato in RGBA grezzo su stdout.

Questo ffmpeg non ha ne libass ne drawtext: il testo va rasterizzato fuori. Il
livello va dritto nella pipe di ffmpeg, senza file intermedi. Regge 24.000 frame
perche le parti ferme si disegnano una volta sola: si anima solo cio che si
muove, e quando un elemento ha finito di entrare si congela in uno sprite.

v3, tutto si muove:

- **titoli dietro**: il layout (due righe al centro, colonna a sinistra, colonna
  a destra) si sceglie sulla sagoma, sulla parola peggiore; le lettere cadono una
  a una, una lama di luce attraversa la stanza dietro di lei, un filo menta si
  disegna sotto l'ultima riga;
- **infografiche**: il numero conta fino al valore (o da `prima`), una scala
  misurata si riempie insieme, l'eyebrow si batte a macchina, la glossa sale
  parola per parola;
- **sottotitoli cinetici**: le parole entrano quando vengono dette, la parola
  attiva sta su una pillola menta che scivola; nelle frasi di enfasi il corpo
  cresce e la scena si vela ai bordi;
- avanzamento a capitoli, apertura, chip e chiusura animati.

    python -m motore.grafica.render <slug> [secondi]    -> RGBA su stdout
"""
import math
import subprocess
import sys
import time

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .. import stile as S
from ..progetto import Progetto, FPS, ffmpeg
from .base import *          # noqa: F401,F403  (shorts e miniature le prendono da qui)
from .base import _cl
from .info import crea, misura
from . import scene as SC
from . import segni as SG

# ---------------------------------------------------------------- sottotitoli
class Sottotitoli:
    """Sottotitoli cinetici: niente pillola di fondo, testo paper con contorno navy
    e ombra. Le parole del gruppo entrano quando vengono dette (rimbalzo piccolo),
    la parola attiva e navy su una pillola menta che scivola di parola in parola.
    Nei tratti `forti` (le frasi di enfasi) il corpo cresce."""

    def __init__(self, caps, size=None, maxw=None, forti=()):
        self.caps = caps
        self.size = size or S.SIZE['caption']
        self.maxw = maxw or S.CAPTION_MAXW
        self.forti = list(forti)
        self.cache = {}
        self.pills = {}
        self.ci = 0

    def _layout(self, gi):
        if gi in self.cache:
            return self.cache[gi]
        g = self.caps[gi]
        forte = any(a - 0.05 <= g['s'] < b for a, b in self.forti)
        size = int(self.size * (S.CAP_FORTE if forte else 1.0))
        while True:
            f = sans(size, 900)
            track = S.TRACK['caption'] * size
            space = f.getlength(' ') * 1.15 + track
            widths = [tracked_width(f, w['t'], track) for w in g['words']]
            total = sum(widths) + space * (len(widths) - 1)
            if total <= self.maxw or size <= 30:
                break
            size -= 2
        stroke = max(3, int(size * 0.075))
        parole, x = [], -total / 2
        for w, ww in zip(g['words'], widths):
            nor = testo(w['t'], f, S.PAPER + (255,), track, stroke, S.NAVY_DEEP + (255,), ombra=max(4, size // 10))
            att = testo(w['t'], f, S.NAVY_DEEP + (255,), track)
            parole.append({'x': x, 'w': ww, 'n': nor, 'a': att, 's': w['s'], 'e': w['e']})
            x += ww + space
        L = {'size': size, 'parole': parole}
        if len(self.cache) > 30:
            self.cache.clear()
        self.cache[gi] = L
        return L

    def _pill(self, w, h):
        k = (w, h)
        if k not in self.pills:
            if len(self.pills) > 200:
                self.pills.clear()
            self.pills[k] = rounded((w, h), int(h * 0.26), S.MINT + (255,))
        return self.pills[k]

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
        L = self._layout(self.ci)
        size, P = L['size'], L['parole']
        active = 0
        for i, w in enumerate(P):
            if t >= w['s'] - 0.02:
                active = i
        y0 = bottom - int(size * 1.18) - 10          # origine del testo
        # pillola: scivola dalla parola precedente all'attiva in 0,09 s
        px = lambda i: (cx + P[i]['x'] - size * 0.16, P[i]['w'] + size * 0.32)
        xa, wa = px(active)
        if active > 0:
            q = S.ease_out_cubic((t - (P[active]['s'] - 0.02)) / 0.09)
            xb, wb = px(active - 1)
            xa, wa = xb + (xa - xb) * q, wb + (wa - wb) * q
        pa = _cl((t - (P[0]['s'] - 0.05)) / S.CAP_POP)
        ph = int(size * 1.02)
        pill = self._pill(int(wa), ph)
        k = 0.7 + 0.3 * S.ease_out_back(pa)
        pill = scala_px(pill, k)
        paste_clip(base, pill, (xa + (wa - pill.width) / 2, y0 + size * 0.15 + (ph - pill.height) / 2),
                   int(255 * min(1, pa * 2)))
        for i, w in enumerate(P):
            p = _cl((t - (w['s'] - 0.05)) / S.CAP_POP)
            if p <= 0:
                continue
            sp, pad = w['a'] if i == active else w['n']
            k = 0.62 + 0.38 * S.ease_out_back(p)
            dy = (1 - S.ease_out_cubic(p)) * size * 0.22
            # si scala attorno al centro della parola, sulla linea di base
            ax, ay = pad + w['w'] / 2, pad + size * 0.97
            x = cx + w['x'] + w['w'] / 2 - ax * k
            y = y0 + size * 0.97 - ay * k + dy
            paste_clip(base, scala_px(sp, k), (x, y), int(255 * min(1, p * 2.5)))


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
def lama_sprite():
    """la lama di luce menta, inclinata, alta tutto il quadro"""
    lw, k = 460, 0.30
    x = np.arange(lw) - lw / 2
    a = 70 * np.exp(-(x / (lw * 0.20)) ** 2) + 150 * np.exp(-(x / 5.0) ** 2)
    row = np.clip(a, 0, 255).astype(np.uint8)
    alpha = Image.fromarray(np.tile(row, (S.H, 1)), 'L')
    im = Image.new('RGBA', (lw, S.H), S.MINT + (0,))
    im.putalpha(alpha)
    out_w = lw + int(k * S.H)
    return im.transform((out_w, S.H), Image.AFFINE, (1, k, -k * S.H, 0, 1, 0), Image.BILINEAR)


_LAMA = None


def eco_sprite(text):
    """la parola gigante a solo contorno, larga quanto il quadro"""
    size = 460
    while True:
        f = sans(size, 900)
        tr = S.TRACK['behind'] * size
        if tracked_width(f, text, tr) <= S.W - 2 * S.SAFE or size <= 120:
            break
        size -= 10
    w, h = int(tracked_width(f, text, tr)) + 40, int(size * 1.15)
    piena, bordo = Image.new('L', (w, h), 0), Image.new('L', (w, h), 0)
    sw = max(3, size // 90)
    draw_tracked(ImageDraw.Draw(bordo), (20, -int(size * 0.12)), text, f, None, tr, sw, 255)
    draw_tracked(ImageDraw.Draw(piena), (20, -int(size * 0.12)), text, f, 255, tr)
    a = np.clip(np.asarray(bordo, np.int16) - np.asarray(piena, np.int16), 0, 255) * 0.55
    im = Image.new('RGBA', (w, h), S.MINT + (0,))
    im.putalpha(Image.fromarray(a.astype(np.uint8), 'L'))
    return im


class Dietro:
    """Titolo gigante dietro la persona.

    Il layout si sceglie sulla sagoma: due righe al centro (prima paper, seconda
    menta), oppure una colonna a sinistra o a destra quando la testa sta al centro
    e mangerebbe le parole. Si misura la PAROLA PEGGIORE, non la media: "NON
    M..BOLICO" non si legge anche se in media e coperto solo il 20%.
    """

    def __init__(self, c, sagome, indice=None):
        global _LAMA
        self.c = c
        self.sagome = sagome
        self.mask_cache = {}
        n0, n1 = int(round(c['s'] * FPS)), int(round(c['e'] * FPS))
        ms = [self.maschera(n) for n in (n0 + 2, (n0 + n1) // 2, n1 - 3)]
        ms = [m for m in ms if m is not None]
        self.mask_cache.clear()
        m = np.maximum.reduce(ms) if ms else None
        self.eb_h = S.SIZE['eyebrow'] + 8
        cands = [self._centro(m)]
        if m is not None:
            for lato in ('sinistra', 'destra'):
                r = self._colonna(m, lato, cands[0]['size'])
                if r:
                    cands.append(r)
        best = min(cands, key=lambda r: r['score'])
        self.layout, self.size, self.coperto = best['nome'], best['size'], best['worst']
        f, tr, gt = best['f'], best['tr'], best['gt']
        self.righe = []
        for ln in best['righe']:
            self.righe.append((Lettere(ln['text'], f, ln['col'], tr, -int(self.size * 0.12)), ln['x'], ln['y']))
        # filo menta sotto l'ultima riga
        ul = best['righe'][-1]
        self.filo = (ul['x'], ul['y'] + gt + best['caph'] + int(self.size * 0.11), ul['w'],
                     max(7, int(self.size * 0.045)))
        # eyebrow sopra la prima riga, fuori dalla maschera: dietro la testa sparirebbe
        fe = mono(S.SIZE['eyebrow'] + 8)
        tre = S.TRACK['eyebrow'] * (S.SIZE['eyebrow'] + 8)
        eb = f"{indice:02d} · {c['eyebrow']}" if indice else c['eyebrow']
        self.eyebrow = Macchina(eb, fe, S.MINT, tre)
        r0 = best['righe'][0]
        ew = tracked_width(fe, eb, tre)
        x_eb = r0['x'] + r0['w'] - ew - 6 if best['nome'] == 'destra' else r0['x'] + 8
        self.eb_xy = (int(x_eb), int(r0['y'] + gt - 22 - self.eb_h))
        self.ingresso = max(l.fine + i * 0.12 for i, (l, _, _) in enumerate(self.righe))
        # in colonna il titolo e piu piccolo: la seconda riga torna gigante, solo
        # contorno, dall'altra parte della stanza (e una parola gia a schermo)
        self.eco = eco_sprite(c['l2']) if self.layout != 'centro' else None
        if _LAMA is None:
            _LAMA = lama_sprite()

    # -- layout --------------------------------------------------------------
    @staticmethod
    def _metriche(size):
        f = sans(size, 900)
        bb = f.getbbox('MEH')
        return f, S.TRACK['behind'] * size, bb[1] - int(size * 0.12), bb[3] - bb[1]

    @staticmethod
    def _parole(f, tr, text):
        words, x, sp = [], 0.0, f.getlength(' ') + tr
        for wd in text.split():
            ww = tracked_width(f, wd, tr)
            words.append((wd, x, ww))
            x += ww + sp
        return words, x - sp

    @staticmethod
    def _peggiore(Rc, righe, gt, caph):
        """copertura della parola piu coperta, dalle somme cumulate della maschera"""
        worst = 0.0
        for r in righe:
            y0 = max(0, int(r['y'] + gt))
            y1 = min(S.H, y0 + caph)
            if y1 <= y0:
                continue
            prof = (Rc[y1] - Rc[y0]) / (y1 - y0)
            cum = np.concatenate([[0.0], np.cumsum(prof)])
            for _, wx, ww in r['words']:
                a_, b_ = max(0, int(r['x'] + wx)), min(S.W, int(r['x'] + wx + ww))
                if b_ > a_:
                    worst = max(worst, (cum[b_] - cum[a_]) / (b_ - a_))
        return worst

    def _centro(self, m):
        c = self.c
        texts = [(c['l1'], S.PAPER), (c['l2'], S.MINT)]
        size = S.SIZE['behind']
        while True:
            f, tr, gt, caph = self._metriche(size)
            if max(tracked_width(f, t, tr) for t, _ in texts) <= S.W - 2 * S.SAFE or size < 90:
                break
            size -= 6
        lh = int(size * 0.98)
        righe = []
        for t, col in texts:
            words, w = self._parole(f, tr, t)
            righe.append({'text': t, 'col': col, 'words': words, 'w': w, 'x': (S.W - w) / 2, 'y': 0})
        base = {'nome': 'centro', 'size': size, 'f': f, 'tr': tr, 'gt': gt, 'caph': caph, 'righe': righe}
        if m is None:
            for i, r in enumerate(righe):
                r['y'] = int(S.H * 0.40 - lh) + i * lh
            return dict(base, worst=None, score=0.0)
        Rc = np.vstack([np.zeros((1, S.W), np.float32), np.cumsum(m, axis=0)])
        y_min = 44 + self.eb_h + 22 - gt
        best = None
        for top in range(max(int(S.H * 0.05), y_min), int(S.H * 0.72) - 2 * lh, 12):
            dxs, worst_all = [], 0.0
            for i, r in enumerate(righe):
                lim = int((S.W - r['w']) / 2 - S.SAFE // 2)
                bw = None
                for dx in range(-min(260, lim), min(260, lim) + 1, 16):
                    rr = dict(r, x=(S.W - r['w']) / 2 + dx, y=top + i * lh)
                    wv = self._peggiore(Rc, [rr], gt, caph)
                    sc = wv + 0.0004 * abs(dx) / 16
                    if bw is None or sc < bw[0]:
                        bw = (sc, dx, wv)
                dxs.append(bw[1])
                worst_all = max(worst_all, bw[2])
            score = worst_all + 0.0003 * (top - S.H * 0.05) / 12
            if best is None or score < best[0]:
                best = (score, top, dxs, worst_all)
        for i, r in enumerate(righe):
            r['x'], r['y'] = (S.W - r['w']) / 2 + best[2][i], best[1] + i * lh
        return dict(base, worst=round(best[3], 3), score=best[3])

    def _colonna(self, m, lato, size_centro):
        """tutte le parole impilate su un lato, allineate al bordo del quadro"""
        c = self.c
        Rc = np.vstack([np.zeros((1, S.W), np.float32), np.cumsum(m, axis=0)])
        best = None
        for frac in (0.40, 0.48, 0.56):
            colw = S.W * frac - S.SAFE
            size = S.SIZE['behind']
            while size >= 90:
                f, tr, gt, caph = self._metriche(size)
                testi = [(ln, S.PAPER) for ln in wrap_to(f, c['l1'], tr, colw)] + \
                        [(ln, S.MINT) for ln in wrap_to(f, c['l2'], tr, colw)]
                lh = int(size * 0.96)
                if all(tracked_width(f, t, tr) <= colw for t, _ in testi) and len(testi) * lh <= S.H * 0.70:
                    break
                size -= 6
            if size < 90:
                continue
            # anche un po' piu piccolo: a volte basta a togliere una lettera da dietro la testa
            for sz in (size, int(size * 0.88)):
                best = self._prova_colonna(Rc, lato, sz, colw, size_centro, best)
        return best

    def _prova_colonna(self, Rc, lato, size, colw, size_centro, best):
        c = self.c
        f, tr, gt, caph = self._metriche(size)
        testi = [(ln, S.PAPER) for ln in wrap_to(f, c['l1'], tr, colw)] + \
                [(ln, S.MINT) for ln in wrap_to(f, c['l2'], tr, colw)]
        lh = int(size * 0.96)
        righe = []
        for t, col in testi:
            words, w = self._parole(f, tr, t)
            x = S.SAFE if lato == 'sinistra' else S.W - S.SAFE - w
            righe.append({'text': t, 'col': col, 'words': words, 'w': w, 'x': x, 'y': 0})
        y_min = 44 + self.eb_h + 22 - gt
        for top in range(max(int(S.H * 0.05), y_min), int(S.H * 0.80) - len(righe) * lh, 12):
            for i, r in enumerate(righe):
                r['y'] = top + i * lh
            wv = self._peggiore(Rc, righe, gt, caph)
            # una colonna vince solo se legge davvero meglio: il centro e piu grande
            score = wv + 0.22 * max(0.0, 1 - size / size_centro) + 0.0003 * (top - S.H * 0.05) / 12
            if best is None or score < best['score']:
                best = {'nome': lato, 'size': size, 'f': f, 'tr': tr, 'gt': gt, 'caph': caph,
                        'righe': [dict(r) for r in righe], 'worst': round(float(wv), 3), 'score': score}
        return best

    # -- sagome --------------------------------------------------------------
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

    # -- disegno -------------------------------------------------------------
    def disegna(self, base, t, n, video=False):
        c = self.c
        if not (c['s'] <= t < c['e']):
            return
        tl = t - c['s']
        layer = Image.new('RGBA', (S.W, S.H), (0, 0, 0, 0))
        uscita = _cl((c['e'] - t) / S.BEHIND_OUT)
        m = self.maschera(n)
        if video and m is not None:
            # la stanza si spegne e diventa blu notte, lei resta a colori
            k = 0.88 * _cl(tl / 0.3) * uscita
            arr = np.asarray(base.convert('RGB'), dtype=np.float32)
            lum = arr @ np.array([0.299, 0.587, 0.114], np.float32)
            spento = lum[..., None] * 0.62 + np.array(S.NAVY_DEEP, np.float32) * 0.55
            w = (k * (1.0 - m))[..., None]
            base.paste(Image.fromarray((arr + (spento - arr) * w).astype(np.uint8), 'RGB'))
        # velo navy sullo sfondo, per il contrasto della menta sul teal
        dim = int((70 if video else 125) * _cl(tl / 0.25) * uscita)
        layer.paste(S.NAVY_DEEP + (dim,), (0, 0, S.W, S.H))
        # la lama di luce attraversa la stanza, dietro di lei
        if tl < S.LAMA:
            q = S.ease_in_out(tl / S.LAMA)
            paste_clip(layer, _LAMA, (-_LAMA.width + (S.W + _LAMA.width) * q, 0))
        if self.eco is not None:
            k = 1.0 + 0.07 * (tl / max(0.1, c['e'] - c['s']))
            sp = scala_px(self.eco, k)
            pe = S.ease_out_cubic((tl - 0.15) / 0.6)
            paste_clip(layer, sp, ((S.W - sp.width) / 2, S.H * 0.52 - sp.height / 2 + (1 - pe) * 60),
                       int(255 * pe * uscita))
        su = int((1 - uscita) ** 2 * self.size * 0.22)
        for i, (lett, x, y) in enumerate(self.righe):
            lett.disegna(layer, (x, y - su), tl - i * 0.12, int(255 * uscita))
        fx, fy, fw, fth = self.filo
        pw = fw * S.ease_out_expo((tl - self.ingresso * 0.6) / 0.55)
        if pw > 2:
            fil = rounded((int(pw), fth), fth // 2, S.MINT + (255,))
            fade_paste(layer, fil, (fx, fy - su), int(255 * uscita))
        if m is not None:
            arr = np.asarray(layer, dtype=np.float32)
            arr[..., 3] *= (1.0 - m)
            layer = Image.fromarray(arr.astype(np.uint8), 'RGBA')
        self.eyebrow.disegna(layer, self.eb_xy, tl - 0.05, int(255 * uscita))
        base.alpha_composite(layer)


# ---------------------------------------------------- apertura, chip, chiusura
class Lockup:
    """pannello in alto (apertura e chip): eyebrow a macchina, filo, righe che
    salgono da una feritoia ciascuna"""

    def __init__(self, c, chip=False):
        self.c = c
        self.finale = None
        if chip:
            f_t, size = sans(S.SIZE['chip_name'], 900), S.SIZE['chip_name']
            righe = [(c['name'], S.PAPER)]
            eye_txt, es = c['role'], S.SIZE['chip_role']
        else:
            f_t, size = sans(S.SIZE['hook'], 900), S.SIZE['hook']
            eye_txt, es = c['eyebrow'], S.SIZE['eyebrow']
            track_t = S.TRACK['chapter'] * size
            righe = []
            for i, ln in enumerate((c['l1'], c['l2'])):
                for w_ in wrap_to(f_t, ln, track_t, S.CARD_W - 68):
                    righe.append((w_, S.PAPER if i == 0 else S.MINT))
        track_t = S.TRACK['chapter'] * size
        maxw = S.CARD_W - 68
        f_eye = mono(es)
        track_e = S.TRACK['eyebrow'] * es
        # l'eyebrow non si taglia: se non entra si stringe la spaziatura, poi il corpo
        while tracked_width(f_eye, eye_txt, track_e) > maxw and es > 16:
            if track_e > 0.10 * es:
                track_e = 0.10 * es
            else:
                es -= 1
                f_eye = mono(es)
                track_e = 0.10 * es
        self.eye = Macchina(eye_txt, f_eye, S.MINT, track_e)
        self.lh = int(size * 1.10)
        self.righe = [testo(t, f_t, col + (255,), track_t, top=-int(size * 0.08)) for t, col in righe]
        w = int(max(tracked_width(f_eye, eye_txt, track_e),
                    max(tracked_width(f_t, t, track_t) for t, _ in righe))) + 68
        self.chip = chip
        if chip:
            self.y_righe = 24
            self.y_eye = 24 + self.lh + 8
            h = self.y_eye + es + 30
        else:
            self.y_eye = 34
            self.y_rule = 34 + es + 18
            self.y_righe = self.y_rule + 6 + 22
            h = self.y_righe + len(righe) * self.lh + 26
        self.panel = rounded((w, h), 24, S.NAVY_DEEP + (222,))
        ImageDraw.Draw(self.panel).line([(24, 1), (w - 24, 1)], fill=S.PAPER + (36,), width=2)
        self.t_righe = 0.10 if chip else 0.30
        self.stabile = max(self.t_righe + len(self.righe) * 0.09 + 0.6, len(eye_txt) * S.TYPE_CHAR + 0.9)

    @property
    def height(self):
        return self.panel.height

    @property
    def width(self):
        return self.panel.width

    def sprite(self, tl):
        if self.finale is not None and tl >= self.stabile:
            return self.finale
        im = self.panel.copy()
        if not self.chip:
            rw = 84 * S.ease_out_expo((tl - 0.18) / 0.45)
            if rw > 1:
                ImageDraw.Draw(im).rounded_rectangle([34, self.y_rule, 34 + rw, self.y_rule + 5], radius=2,
                                                     fill=S.MINT + (255,))
        self.eye.disegna(im, (34 if not self.chip else 32, self.y_eye), tl - (0.08 if not self.chip else 0.35),
                         cursore=False)
        x = 34 if not self.chip else 32
        for i, (sp, pad) in enumerate(self.righe):
            p = S.ease_out_expo((tl - self.t_righe - i * 0.09) / 0.55)
            if p <= 0:
                continue
            y = self.y_righe + i * self.lh
            dy = int((1 - p) * self.lh)
            vis = self.lh + 6 - dy                 # la feritoia: sotto la riga non si vede
            if vis > 0:
                fade_paste(im, sp.crop((0, pad, sp.width, min(sp.height, pad + vis))), (x - pad, y + dy), 255)
        if tl >= self.stabile:
            self.finale = im
        return im


def lockup_sprite(c):
    return Lockup(c).sprite(99)


def chip_sprite(c):
    return Lockup(c, chip=True).sprite(99)


class Chiusura:
    """schermata finale: trama di fili menta che scorre, eyebrow a macchina,
    titolo che cade lettera per lettera, CTA con il bordo che si disegna e poi pulsa"""

    def __init__(self, c):
        self.c = c
        trama = Image.new('RGBA', (S.W + 2 * S.H, S.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(trama)
        for x in range(0, S.W + 2 * S.H, 54):
            d.line([(x, S.H), (x + S.H, 0)], fill=S.MINT + (16,), width=2)
        self.trama = trama
        self.fondo = Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (246,))
        tr = S.TRACK['eyebrow']
        fe = mono(S.SIZE['eyebrow'] + 6)
        self.eye = Macchina(c['eyebrow'], fe, S.MINT, tr * (S.SIZE['eyebrow'] + 6))
        self.eye_w = tracked_width(fe, c['eyebrow'], tr * (S.SIZE['eyebrow'] + 6))
        size = S.SIZE['chapter'] + 18
        f_t = sans(size, 900)
        trt = S.TRACK['chapter'] * size
        self.righe = [Lettere(ln, f_t, col, trt, -int(size * 0.10))
                      for ln, col in ((c['l1'], S.PAPER), (c['l2'], S.MINT))]
        self.lh = int(size * 1.12)
        f_cta = mono(S.SIZE['chapter_sub'])
        cw = tracked_width(f_cta, c['cta'], tr * S.SIZE['chapter_sub'])
        self.box = (int(cw + 96), S.SIZE['chapter_sub'] + 56)
        self.cta, self.cta_pad = testo(c['cta'], f_cta, S.MINT + (255,), tr * S.SIZE['chapter_sub'])
        cta_box = Image.new('RGBA', self.box, (0, 0, 0, 0))
        ImageDraw.Draw(cta_box).rounded_rectangle([0, 0, self.box[0] - 1, self.box[1] - 1], radius=14,
                                                  outline=S.MINT + (255,), width=4)
        self.glow, self.glow_pad = bagliore(cta_box, 18, S.MINT, 0.9)
        f_br = mono(S.SIZE['eyebrow'])
        self.brand, self.brand_pad = testo(c['brand'], f_br, S.MUTED + (255,), tr * S.SIZE['eyebrow'])
        y = S.H // 2 - 230
        self.y_eye = y
        self.y_rule = y + S.SIZE['eyebrow'] + 34
        self.y_t = self.y_rule + 40
        self.y_box = self.y_t + 2 * self.lh + 40
        self.y_brand = self.y_box + self.box[1] + 46

    def frame(self, tl, alpha):
        im = self.fondo.copy()
        off = int(tl * 22) % 54
        im.alpha_composite(self.trama.crop((S.H - off, 0, S.H - off + S.W, S.H)))
        d = ImageDraw.Draw(im)
        self.eye.disegna(im, ((S.W - self.eye_w) / 2, self.y_eye), tl - 0.15)
        rw = 60 * S.ease_out_expo((tl - 0.25) / 0.5)
        if rw > 1:
            d.rounded_rectangle([S.W / 2 - rw, self.y_rule, S.W / 2 + rw, self.y_rule + 6], radius=3,
                                fill=S.MINT + (255,))
        for i, l in enumerate(self.righe):
            l.disegna(im, ((S.W - l.w) / 2, self.y_t + i * self.lh), tl - 0.30 - i * 0.18)
        bx, by = (S.W - self.box[0]) / 2, self.y_box
        pb = S.ease_in_out((tl - 1.0) / 0.6)
        if pb > 0:
            if pb >= 1:
                pulse = 0.5 + 0.5 * math.sin((tl - 1.6) * 2 * math.pi / 1.3)
                fade_paste(im, self.glow, (bx - self.glow_pad, by - self.glow_pad), int(70 + 120 * pulse))
            # il bordo si disegna in senso orario, dal centro in alto
            W_, H_ = self.box
            per = 2 * (W_ + H_)
            L = per * pb
            seg = [((W_ / 2, 0), (W_, 0)), ((W_, 0), (W_, H_)), ((W_, H_), (0, H_)), ((0, H_), (0, 0)),
                   ((0, 0), (W_ / 2, 0))]
            for (x0, y0), (x1, y1) in seg:
                ln = abs(x1 - x0) + abs(y1 - y0)
                if L <= 0:
                    break
                f = min(1.0, L / ln)
                d.line([(bx + x0, by + y0), (bx + x0 + (x1 - x0) * f, by + y0 + (y1 - y0) * f)],
                       fill=S.MINT + (255,), width=4)
                L -= ln
            pt = _cl((tl - 1.35) / 0.3)
            fade_paste(im, self.cta, ((S.W - self.cta.width) / 2, by + 26 - self.cta_pad), int(255 * pt))
        pbr = _cl((tl - 1.7) / 0.4)
        fade_paste(im, self.brand, ((S.W - self.brand.width) / 2, self.y_brand - self.brand_pad), int(255 * pbr))
        if alpha < 253:
            im.putalpha(im.getchannel('A').point(lambda v: v * alpha // 255))
        return im


def closing_sprite(c):
    return Chiusura(c).frame(5.0, 255)


def vignetta():
    """velo navy ai bordi per le frasi di enfasi: lo sguardo va al centro"""
    y, x = np.ogrid[:S.H, :S.W]
    r = np.sqrt(((x - S.W / 2) / (S.W / 2)) ** 2 + ((y - S.H * 0.45) / (S.H / 2)) ** 2)
    a = (np.clip((r - 0.55) / 0.85, 0, 1) ** 1.4 * 175).astype(np.uint8)
    im = Image.new('RGBA', (S.W, S.H), S.NAVY_DEEP + (0,))
    im.putalpha(Image.fromarray(a, 'L'))
    return im


def _spinta_box(z, dx=0.0, dy=0.0):
    w, h = int(round(S.W / z)), int(round(S.H / z))
    x0 = min(max(0, (S.W - w) // 2 + int(dx)), S.W - w)
    y0 = min(max(0, int((S.H - h) * 0.42) + int(dy)), S.H - h)
    return x0, y0, w, h


def spinta(base, z, dx=0.0, dy=0.0):
    """push-in di camera: il quadro si ingrandisce di z attorno al centro;
    (dx, dy) e la scossa del colpo"""
    if z <= 1.0005:
        return base
    x0, y0, w, h = _spinta_box(z, dx, dy)
    return base.crop((x0, y0, x0 + w, y0 + h)).resize((S.W, S.H), Image.BILINEAR)


class Grana:
    """la pellicola (Gadzhi): grana fine di luminanza, sei tele che si alternano.
    `forza` da 0 a 1; 0,5 e gia visibile su uno schermo grande, sul telefono quasi no"""

    def __init__(self, forza):
        rng = np.random.default_rng(11)
        sig = 9.0 * forza
        self.tele = []
        for _ in range(6):
            g = rng.normal(0, sig, (S.H // 2, S.W // 2)).astype(np.float32)
            g = np.asarray(Image.fromarray(g, 'F').resize((S.W, S.H), Image.BILINEAR), np.float32)
            self.tele.append(np.clip(g, -40, 40).astype(np.int16)[..., None])

    def applica(self, im, n):
        a = np.asarray(im.convert('RGB'), np.int16) + self.tele[n % 6]
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')


class Scene:
    """Compone il fotogramma: video, titoli dietro, spinta di camera, pannelli in
    vetro, sottotitoli. Le parti ferme si disegnano una volta sola.

    `frame(n, sfondo)`: con `sfondo` (il fotogramma del montato pulito) esce il
    fotogramma finito; senza, un livello trasparente (i pannelli diventano pieni)."""

    def __init__(self, P):
        plan = P.leggi('grafica.json')
        self.plan = plan
        sag = P.p('data', 'sagome')
        self.cards = [(c, crea(c)) for c in plan['cards']]
        self.full = [(c, chapter_sprite(c)) for c in plan['capitoli'] if not c['dietro']]
        self.dietro = [Dietro(c, sag, i + 1) for i, c in enumerate(plan['capitoli']) if c['dietro']]
        self.lock = (plan['opening'], Lockup(plan['opening'])) if plan.get('opening') else None
        self.chip = (plan['chip'], Lockup(plan['chip'], chip=True)) if plan.get('chip') else None
        self.close = (plan['closing'], Chiusura(plan['closing'])) if plan.get('closing') else None
        self.sagome = SC.Sagome(sag if sag.is_dir() else None)
        self.scene = [SC.crea(c, self.sagome) for c in plan.get('scene', [])]
        self.segni = [SG.crea(c) for c in plan.get('segni', [])]
        self.colpi = [g.colpo() for g in self.segni if isinstance(g, SG.Parola)]
        fin = plan.get('finitura') or {}
        self.grana = Grana(float(fin['grana'])) if fin.get('grana') else None
        self.pezzi, self.src_wh = [], (S.W, S.H)
        if any(not isinstance(g, SG.Parola) for g in self.segni) and P.data('inquadratura.json').exists():
            I = P.leggi('inquadratura.json')
            self.pezzi, self.src_wh = I['pezzi'], tuple(I['sorgente'])
        self.enfasi = [(c['s'], c['e']) for c in plan.get('enfasi', [])]
        self.vign = vignetta() if self.enfasi else None
        self.subs = Sottotitoli(plan['captions'], forti=self.enfasi)
        self.nascosti = [(c['s'], c['e']) for c in plan['capitoli']]
        self.nascosti += [(c['s'] + 0.2, c['e']) for c in plan['cards'] if c.get('tipo') == 'citazione']
        self.nascosti += [(c['s'] + (0 if c['s'] < 0.05 else 0.3), c['e'] - 0.2) for c in plan.get('scene', []) if c['tipo'] == 'parole']
        if plan.get('closing'):
            self.nascosti.append((plan['closing']['s'], plan['closing']['e']))
        for d in self.dietro:
            sys.stderr.write(f"  titolo dietro «{d.c['l1']} {d.c['l2']}»: layout {d.layout}, corpo {d.size}, "
                             f"parola peggiore coperta {'?' if d.coperto is None else f'{d.coperto*100:.0f}%'}\n")
        self.dur = plan['duration']
        tagli = sorted(c['s'] for c in plan['capitoli'])
        self.segmenti = list(zip([0.0] + tagli, tagli + [self.dur]))

    def _avanzamento(self, base, t):
        dd = ImageDraw.Draw(base)
        y0, y1 = S.H - S.PROGRESS_H, S.H
        for a, b in self.segmenti:
            x0 = S.W * a / self.dur + (4 if a > 0 else 0)
            x1 = S.W * b / self.dur - (4 if b < self.dur else 0)
            cur = a <= t < b
            dd.rectangle([x0, y0, x1, y1], fill=S.PAPER + (70 if cur else 46,))
            xt = min(x1, S.W * t / self.dur)
            if xt > x0:
                dd.rectangle([x0, y0 - (2 if cur else 0), xt, y1],
                             fill=S.MINT + (255 if cur else 200,))

    def _zoom(self, t):
        """quanto spingere la camera: sui titoli dietro e, piano, sulle enfasi"""
        for d in self.dietro:
            c = d.c
            if c['s'] <= t < c['e']:
                su = S.ease_out_cubic((t - c['s']) / 1.2)
                giu = S.ease_in_out(_cl((c['e'] - t) / S.BEHIND_OUT))
                return 1.0 + 0.055 * su * giu
        for a, b in self.enfasi:
            if a <= t < b:
                return 1.0 + 0.035 * (t - a) / max(0.5, b - a)
        return 1.0

    def _colpo(self, t):
        """la camera prende il colpo della parola: un pugno di zoom e una scossa che si spegne"""
        for tc in self.colpi:
            u = t - tc
            if 0 <= u < 0.32:
                k = math.exp(-u * 11)
                return 0.045 * k, 11 * k * math.sin(u * 95), 7 * k * math.cos(u * 77)
        return 0.0, 0.0, 0.0

    def _mappa(self, n, z, dx, dy):
        """dalla sorgente (0-1) al quadro d'uscita del frame n: taglio del pezzo, poi spinta"""
        p = next((p for p in self.pezzi if p['f0'] <= n < p['f0'] + p['n']), None)
        x0, y0, cw, ch = p['crop'] if p else (0, 0) + self.src_wh
        sx0, sy0, sw, sh = _spinta_box(z, dx, dy) if z > 1.0005 else (0, 0, S.W, S.H)

        def f(u, v):
            px = (u * self.src_wh[0] - x0) * S.W / cw
            py = (v * self.src_wh[1] - y0) * S.H / ch
            return (px - sx0) * S.W / sw, (py - sy0) * S.H / sh
        return f

    def frame(self, n, sfondo=None):
        t = n / FPS
        video = sfondo is not None
        base = sfondo.convert('RGBA') if video else Image.new('RGBA', (S.W, S.H), (0, 0, 0, 0))
        for a, b in self.enfasi:
            if a <= t < b:
                v = min(_cl((t - a) / 0.35), _cl((b - t) / 0.35))
                fade_paste(base, self.vign, (0, 0), int(255 * v))
                break
        for d in self.dietro:
            d.disegna(base, t, n, video)
        # la scena a tutto schermo: sopra il video, sotto avanzamento e sottotitoli
        sc = next((x for x in self.scene if x.attiva(t)), None)
        z, dx, dy = self._zoom(t), 0.0, 0.0
        if sc and sc.lei == 'davanti':
            z = 1.0              # la sagoma e calcolata sul quadro senza spinta
        pz, dx, dy = self._colpo(t)
        z += pz
        if video:
            base = spinta(base, z, dx, dy)
        if sc:
            base = sc.componi(base, t, video, n)
            self._avanzamento(base, t)
            self.subs.disegna(base, t, S.W / 2, S.CAPTION_BOT, self.nascosti)
            return self.grana.applica(base, n) if (self.grana and video) else base
        self._avanzamento(base, t)
        if self.segni:
            mappa = self._mappa(n, z, dx, dy) if video else self._mappa(n, 1.0, 0, 0)
            for g in self.segni:
                if g.c['s'] <= t < g.c['e']:
                    g.disegna(base, t) if isinstance(g, SG.Parola) else g.disegna(base, t, mappa)

        for item in (self.lock, self.chip):
            if not item:
                continue
            c, lk = item
            if c['s'] <= t < c['e']:
                tl = t - c['s']
                rev = S.ease_out_expo(tl / S.CARD_IN)
                rise = int(S.CARD_RISE * (1 - rev))
                a = min(1.0, (c['e'] - t) / S.CARD_OUT)
                self._pannello(base, lk.sprite(tl), c, rev, rise, int(255 * max(a, 0)), video)

        for c, ig in self.cards:
            if not (c['s'] <= t < c['e']):
                continue
            tl = t - c['s']
            rev = S.ease_out_expo(tl / S.CARD_IN)
            rise = int(S.CARD_RISE * (1 - rev))
            a = 255 if t < c['e'] - S.CARD_OUT else int(255 * max(0.0, (c['e'] - t) / S.CARD_OUT))
            self._pannello(base, ig.sprite(tl), c, rev, rise, a, video)

        for c, sp in self.full:
            if not (c['s'] <= t < c['e']):
                continue
            a = min(S.ease_out_cubic((t - c['s']) / S.CHAPTER_IN),
                    S.ease_out_cubic((c['e'] - t) / S.CHAPTER_OUT), 1.0)
            fade_paste(base, sp, (0, 0), int(255 * max(a, 0)))
        if self.close:
            c, ch = self.close
            if c['s'] <= t < c['e']:
                a = min(S.ease_out_cubic((t - c['s']) / S.CHAPTER_IN), 1.0)
                base.alpha_composite(ch.frame(t - c['s'], int(255 * a)))

        self.subs.disegna(base, t, S.W / 2, S.CAPTION_BOT, self.nascosti)
        return self.grana.applica(base, n) if (self.grana and video) else base

    @staticmethod
    def _pannello(base, sp, c, rev, rise, a, video):
        """il pannello di vetro si apre come una tendina dal lato in cui sta, e intanto sale"""
        wv = max(1, int(sp.width * rev))
        y = S.CARD_TOP + rise
        if c.get('side', 'left') == 'left':
            x, crop = S.SAFE, (0, 0, wv, sp.height)
        else:
            x, crop = S.W - S.SAFE - wv, (sp.width - wv, 0, sp.width, sp.height)
        vetro(base, (x, y, wv, sp.height), alpha=a, video=video)
        fade_paste(base, sp.crop(crop), (x, y), a)


def _decoder(video, limite=None):
    """i fotogrammi del montato pulito in RGB, con la matrice BT.709 dichiarata
    (senza, swscale userebbe la 601 e la pelle cambierebbe tono)"""
    cmd = ['ffmpeg', '-v', 'error', '-nostdin', '-i', str(video)]
    if limite:
        cmd += ['-t', str(limite)]
    cmd += ['-vf', 'scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int',
            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=S.W * S.H * 3 * 2)


def stream(slug, limite=None):
    """compone il video finito: legge il montato pulito, scrive RGB grezzo su stdout"""
    P = Progetto(slug)
    scene = Scene(P)
    total = P.leggi('edl.json')['frame']
    if limite:
        total = min(total, int(limite * FPS) + 2)
    dec = _decoder(P.render(f"{slug}_pulito.mp4"), limite)
    out = sys.stdout.buffer
    nb = S.W * S.H * 3
    t0 = time.time()
    try:
        for n in range(total):
            buf = dec.stdout.read(nb)
            if len(buf) < nb:
                sys.stderr.write(f"\n  !!! il montato pulito finisce al frame {n} invece di {total}\n")
                break
            fr = scene.frame(n, Image.frombuffer('RGB', (S.W, S.H), buf, 'raw', 'RGB', 0, 1))
            out.write(fr.convert('RGB').tobytes())
            if n % 1800 == 0 and n:
                el = time.time() - t0
                sys.stderr.write(f"\n  grafica: frame {n}/{total}, {n/el:.0f} fps, "
                                 f"restano {(total-n)/(n/el)/60:.1f} min\n")
        out.flush()
    except BrokenPipeError:
        pass        # ffmpeg ha chiuso la pipe (es. -t): normale
    finally:
        dec.kill()


def _foglio(P, out_name, tempi, scene, video, cols=3):
    out = P.controllo(out_name)
    out.mkdir(exist_ok=True)
    for f in out.glob('*.jpg'):
        f.unlink()
    for t in tempi:
        n = int(round(t * FPS))
        png = out / f"t{t:07.2f}.png"
        ffmpeg('-ss', f"{n / FPS:.4f}", '-i', video, '-frames:v', '1', '-vf',
               'scale=in_color_matrix=bt709:in_range=tv', png)
        bg = Image.open(png).convert('RGB')
        scene.frame(n, bg).convert('RGB').resize((960, 540), Image.LANCZOS).save(png.with_suffix('.jpg'), quality=88)
        png.unlink()
    rows = -(-len(tempi) // cols)
    ffmpeg('-pattern_type', 'glob', '-i', str(out / '*.jpg'), '-filter_complex',
           f'tile={cols}x{rows}:margin=8:padding=6', '-frames:v', '1', P.controllo(out_name + '.jpg'))


def anteprima(slug, tempi=None):
    """compone la grafica sopra i frame veri del montato pulito: va guardata
    PRIMA del render lungo, gli errori di posizione si vedono solo li.

    Oltre ad `anteprima.jpg` (ogni elemento a ingresso finito) scrive
    `movimento.jpg`: il primo titolo dietro, le prime infografiche, l'apertura e
    la chiusura a piu istanti dell'ingresso, per vedere le animazioni senza il render."""
    P = Progetto(slug)
    scene = Scene(P)
    G = scene.plan
    video = P.render(f"{slug}_pulito.mp4")
    if not tempi:
        tempi = [2.0]
        if G.get('chip'):
            tempi.append(G['chip']['s'] + 2.0)
        for c in G['cards']:
            # a ingresso finito: dopo l'ultima voce, se ne ha
            vt = [v.get('t') for k in ('voci', 'zone', 'etichette') for v in c.get(k, []) if v.get('t') is not None]
            tempi.append(c['s'] + min(c['e'] - c['s'] - 0.4, max([2.2] + [x + 1.0 for x in vt])))
        tempi += [c['s'] + 1.6 for c in G['capitoli']]
        tempi += [c['e'] - 0.7 for c in G.get('scene', [])]
        tempi += [c['s'] + 0.6 for c in G['enfasi'][:3]]
        tempi += [c['s'] + 0.9 for c in G.get('segni', [])]
        if G.get('closing'):
            tempi.append(G['closing']['s'] + 2.8)
        moto = []
        dietro = [c for c in G['capitoli'] if c['dietro']]
        if dietro:
            moto += [dietro[0]['s'] + x for x in (0.12, 0.30, 0.55, 1.0)]
        visti = set()
        for c in G['cards']:
            tipo = c.get('tipo', 'numero')
            if tipo in visti:
                continue
            visti.add(tipo)
            d = c['e'] - c['s']
            moto += [c['s'] + d * x for x in (0.08, 0.3, 0.6)]
        prime, viste = [], set()
        for c in G.get('scene', []):
            k = (c['tipo'], c.get('lei', 'dietro'), bool(c.get('richiamo')))
            if k not in viste:
                viste.add(k)
                prime.append(c)
        for c in G.get('segni', [])[:3]:
            moto += [c['s'] + x for x in (0.1, 0.22, 0.45, 0.9)]
        for c in prime[:6]:
            d = c['e'] - c['s']
            moto += [c['s'] + x for x in (0.2, 0.45, 0.9)] + [c['s'] + d * 0.6, c['e'] - 0.25]
        if G.get('opening'):
            moto += [G['opening']['s'] + x for x in (0.25, 0.6, 1.0)]
        if G.get('closing'):
            moto += [G['closing']['s'] + x for x in (0.5, 1.2)]
        caps = [g for g in G['captions'] if len(g['words']) == 3][5:6]
        for g in caps:
            moto += [g['words'][k]['s'] + 0.04 for k in range(3)]
        _foglio(P, 'movimento', sorted(moto), scene, video, cols=4)
        print(f"{len(moto)} fotogrammi di movimento -> controlli/movimento.jpg")
    _foglio(P, 'anteprima', sorted(tempi), scene, video)
    print(f"{len(tempi)} fotogrammi -> controlli/anteprima.jpg (singoli in controlli/anteprima/)")


if __name__ == '__main__':
    stream(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else None)

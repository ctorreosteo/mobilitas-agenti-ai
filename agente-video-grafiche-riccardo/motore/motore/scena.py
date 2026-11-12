"""Composizione a strati: la grafica "dentro la scena" (fase 6a, campionario, 27/10/2026).

La v2 metteva la grafica SOPRA il montato (pannelli piatti, persona tagliata di
lato). Qui un pezzo vero del montato si ricompone dal 4K in cinque passi:

1. **piatto**: i frame dal 4K (stessa decimazione di `monta`) con la **camera
   viva** (spinta lenta continua, zoom rapidi sulle parole, tagli, transizioni a
   spinta e a zoom) ritagliata al sub-pixel con Lanczos, sfocatura di movimento sui
   movimenti veloci (piu ritagli mediati dentro l'otturatore), e il **look**;
2. **sagome**: Apple Vision sulla persona, solo se servono (strato dietro, sfondo
   sfocato o scurito dietro di lui);
3. **strati HyperFrames**: `dietro` (fra la parete e la persona) e `davanti`,
   due MOV con alfa dagli stessi modelli (`motore/inserti/scene/`);
4. **composizione**: piatto -> effetti di piatto -> strato dietro, ritagliato
   dalla sagoma e con l'ombra morbida della persona sopra -> strato davanti;
5. **suono**: voce montata + effetti di `sfx.py` (+ musica, se c'e, che si
   abbassa da sola sotto la voce), a -14 LUFS.

Ogni tempo della specifica e in secondi del **montato** (numero o ancora su una
parola: `{"w": "di te", "i": 1}`); qui si converte nel tempo del pezzo.
Le regole di mestiere (entrate, sfasamenti, uscite, dimensioni, volto) sono in
`mobilitas-grafica`, sezione "Livello 3"; i controlli automatici stanno in
`controlla()`.
"""
import hashlib
import json
import math
import re
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .progetto import AGENTE, LIBRERIA, RISORSE, Progetto, ffmpeg, leggi, scrivi
from . import sfx as SFX
from .impagina import piazza_numero, misura_card, piazza_card, piazza_battute, adatta_colonna, apertura_schermata, adatta_schermata, Mani, lega_mani

W_OUT, H_OUT = 1920, 1080
SCENE = AGENTE / 'motore' / 'inserti' / 'scene'
LAVORO = AGENTE / '.lavoro' / 'scena'
FONT = RISORSE / 'fonts' / 'Montserrat-VF.ttf'


# ------------------------------------------------------------------ curve
def _back(s):
    return lambda p: 1 + (s + 1) * (p - 1) ** 3 + s * (p - 1) ** 2


EASE = {
    'lineare': lambda p: p,
    'sine.inOut': lambda p: 0.5 - 0.5 * math.cos(math.pi * p),
    'power2.inOut': lambda p: 2 * p * p if p < 0.5 else 1 - (-2 * p + 2) ** 2 / 2,
    'power3.inOut': lambda p: 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2,
    'power2.out': lambda p: 1 - (1 - p) ** 2,
    'power3.out': lambda p: 1 - (1 - p) ** 3,
    'power3.in': lambda p: p ** 3,
    'power4.in': lambda p: p ** 4,
    'expo.out': lambda p: 1.0 if p >= 1 else (1 - 2 ** (-10 * p)) / (1 - 2 ** -10),
    'expo.in': lambda p: 0.0 if p <= 0 else (2 ** (10 * (p - 1)) - 2 ** -10) / (1 - 2 ** -10),
    'expo.inOut': lambda p: 0.5 * (2 ** (20 * p - 10)) if p < 0.5 else 1 - 0.5 * 2 ** (-20 * p + 10),
    # rimbalzo leggero: back.out(1.0) supera il bersaglio del 4% e torna (regola: max 5%)
    'back.out': _back(1.0),
}


def ease(nome, p):
    return EASE[nome](min(1.0, max(0.0, p)))


# ------------------------------------------------------------------ tempi
class Tempo:
    """Il pezzo: uno o piu intervalli del montato messi di fila (un taglio fra
    l'uno e l'altro). Tre orologi: montato, pezzo (uscita), sorgente (via EDL)."""

    def __init__(self, P, pezzi):
        self.P, self.fps = P, P.fps
        self.pezzi = []
        o = 0
        for a, b in pezzi:
            fa, fb = int(round(a * self.fps)), int(round(b * self.fps))
            self.pezzi.append((fa, fb, o))
            o += fb - fa
        self.n = o
        self.durata = o / self.fps
        self.E = P.leggi('edl.json')

    def out(self, t_m):
        """montato -> pezzo; un tempo fuori dai pezzi va sul bordo piu vicino"""
        f = t_m * self.fps
        best = None
        for fa, fb, o in self.pezzi:
            if fa - 1e-6 <= f <= fb + 1e-6:
                return (o + f - fa) / self.fps
            d = min(abs(f - fa), abs(f - fb))
            if best is None or d < best[0]:
                best = (d, (o + min(max(f, fa), fb) - fa) / self.fps)
        return best[1]

    def montato(self, t_o):
        f = t_o * self.fps
        for fa, fb, o in self.pezzi:
            if o <= f < o + fb - fa + 1e-6:
                return (fa + f - o) / self.fps
        fa, fb, o = self.pezzi[-1]
        return fb / self.fps

    def tagli(self):
        """istanti del pezzo in cui c'e un taglio (fra pezzi o giunta dell'EDL)"""
        out = [o / self.fps for fa, fb, o in self.pezzi[1:]]
        for g in self.E['giunte']:
            f = g['t'] * self.fps
            for fa, fb, o in self.pezzi:
                if fa < f < fb:
                    out.append((o + f - fa) / self.fps)
        return sorted(out)

    def corse(self):
        """corse di frame consecutivi dentro lo stesso segmento EDL:
        [(frame_uscita_0, n, sorgente_in)]"""
        res = []
        segs = [(int(round(s['edit_in'] * self.fps)), s['n'], s['in']) for s in self.E['segmenti']]
        for fa, fb, o in self.pezzi:
            f = fa
            while f < fb:
                for e0, n, src in segs:
                    if e0 <= f < e0 + n:
                        k = min(fb, e0 + n) - f
                        res.append((o + f - fa, k, src + (f - e0) / self.fps))
                        f += k
                        break
                else:
                    sys.exit(f"frame {f} del montato fuori dall'EDL")
        return res

    def sorgente(self, t_o):
        f = t_o * self.fps
        for o, k, src in self.corse():
            if o <= f < o + k + 1e-6:
                return src + (f - o) / self.fps
        return None


# ------------------------------------------------------------------ ancore
def _inviluppo(P):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(P.asset('voce-montata.wav')), '-ac', '1', '-ar', '16000',
                        '-f', 'f32le', '-'], capture_output=True)
    x = np.frombuffer(r.stdout, dtype='<f4')
    hop = 80
    n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)   # 5 ms


def attacco(env, t, finestra=0.08):
    """aggancia l'inizio di una parola (whisper, +-60 ms) al punto in cui la voce sale
    davvero: la salita piu ripida dell'inviluppo entro +-80 ms, se c'e una salita netta
    (almeno 9 dB in 25 ms); altrimenti resta il tempo di whisper"""
    i0, i1 = int((t - finestra) / 0.005), int((t + finestra) / 0.005)
    if i0 < 5 or i1 + 5 >= len(env):
        return t
    d = env[i0 + 5:i1 + 5] - env[i0:i1]
    k = int(d.argmax())
    if d[k] < 9:
        return t
    return round((i0 + k + 1) * 0.005, 3)


class Ancore:
    def __init__(self, P):
        from .grafica import piano as G
        self.G = G
        self.W = G.parole(P, P.regia())
        self.env = _inviluppo(P)
        self.usate = []

    def __call__(self, a):
        if isinstance(a, (int, float)):
            return float(a)
        i = self.G.ancora(self.W, a['w'], a.get('dopo', 0.0), 'campionario') + a.get('i', 0)
        w = self.W[i]
        if a.get('fine'):
            t = w['e']
        else:
            t = attacco(self.env, w['s']) if a.get('aggancia', True) else w['s']
        self.usate.append({'parola': w['t'], 'whisper': w['s'], 't': t})
        return round(t + a.get('d', 0.0), 3)


TEMPI = {'s', 'e', 't', 't_ruota', 't_spezza', 't_figura', 'sotto_t', 'sotto_e', 'barra_t', 'bacino_t', 'arrivo', 'etichetta_t'}   # tempi del montato da portare nel pezzo


def risolvi(x, anc, tempo):
    """ogni ancora {"w": ...} e ogni numero sotto 's', 'e', 't' (montato) -> tempo del pezzo"""
    if isinstance(x, list):
        return [risolvi(v, anc, tempo) for v in x]
    if not isinstance(x, dict):
        return x
    out = {}
    for k, v in x.items():
        # un'ancora e {"w": <frase>}: un dict con una larghezza numerica "w" (card_accese) non lo e
        if (k in TEMPI and isinstance(v, (int, float))) or (isinstance(v, dict) and isinstance(v.get('w'), str)):
            out[k] = round(tempo.out(anc(v)), 4)
        else:
            out[k] = risolvi(v, anc, tempo)
    return out


# ------------------------------------------------------------------ camera
class Camera:
    """z: ingrandimento sul 4K intero (1 = tutto il quadro; mai oltre 2, sotto i pixel
    nativi); cx, cy: centro, in frazioni del quadro sorgente. `spinta`: avvicinamento
    lento continuo su tutto il pezzo (0.03 = 3%). `mosse`: [{t, dur, z|cx|cy, ease}]
    o tagli netti [{t, taglio: true, ...}]."""

    def __init__(self, spec, durata, sw=3840, sh=2160):
        b = spec.get('base', {})
        self.base = (b.get('z', 1.0), b.get('cx', 0.5), b.get('cy', 0.5))
        self.spinta = spec.get('spinta', 0.0)
        self.mosse = sorted(spec.get('mosse', []), key=lambda m: m['t'])
        # colpi: piccoli punch-in insieme a un impatto (sale in 0,14 s, poi torna
        # piano e ne resta una parte: non "respira")
        self.colpi = sorted(spec.get('colpi', []), key=lambda c: c['t'])
        self.durata, self.sw, self.sh = durata, sw, sh

    def colpo(self, t):
        k = 1.0
        for c in self.colpi:
            d = t - c['t']
            if d < 0:
                continue
            su, giu, resta = c.get('su', 0.14), c.get('giu', 1.4), c.get('resta', 0.4)
            g = ease('expo.out', d / su) if d < su else 1 - (1 - resta) * ease('sine.inOut', (d - su) / giu)
            k *= 1 + c.get('a', 0.045) * g
        return k

    def stato(self, t, fino=None):
        z, cx, cy = self.base
        for m in self.mosse:
            if m['t'] > t + 1e-9 or (fino is not None and m['t'] >= fino):
                break
            if m.get('taglio'):
                z, cx, cy = m.get('z', z), m.get('cx', cx), m.get('cy', cy)
                continue
            e = ease(m.get('ease', 'expo.out'), (t - m['t']) / m['dur'])
            if 'z' in m:
                z = z * (m['z'] / z) ** e
            cx = cx + (m.get('cx', cx) - cx) * e
            cy = cy + (m.get('cy', cy) - cy) * e
        z *= (1 + self.spinta * ease('sine.inOut', t / self.durata)) * self.colpo(t)
        return z, cx, cy

    def box(self, t, fino=None):
        z, cx, cy = self.stato(t, fino)
        z = max(1.0, min(z, 2.0))
        w, h = self.sw / z, self.sh / z
        x0 = min(max(cx * self.sw - w / 2, 0), self.sw - w)
        y0 = min(max(cy * self.sh - h / 2, 0), self.sh - h)
        return (x0, y0, w, h)


def _spost(b1, b2):
    """spostamento massimo (px d'uscita) degli angoli fra due ritagli"""
    k = W_OUT / b1[2]
    c1 = np.array([b1[0], b1[1], b1[0] + b1[2], b1[1] + b1[3]])
    c2 = np.array([b2[0], b2[1], b2[0] + b2[2], b2[1] + b2[3]])
    return float(np.abs(c1 - c2).max() * k)


def ritaglia(im, box, cam=None, t=None, fps=25, fino=None, blur=True):
    """ritaglio sub-pixel con Lanczos; sui movimenti veloci media di piu ritagli
    dentro l'otturatore (180 gradi): la sfocatura di movimento della camera"""
    x0, y0, w, h = box
    if blur and cam is not None:
        dt = 0.25 / fps
        # l'otturatore non attraversa mai un taglio: si campiona solo dal lato di t
        a, b = t - dt, t + dt
        for m in cam.mosse:
            if m.get('taglio') and (fino is None or m['t'] < fino):
                if a < m['t'] <= t + 1e-9:
                    a = m['t']
                elif t < m['t'] <= b:
                    b = m['t'] - 1e-4
        b1, b2 = cam.box(a, fino), cam.box(b, fino)
        d = _spost(b1, b2)
        n = int(min(17, math.ceil(d / 2.0)))   # fino a 17 ritagli: niente scalini sugli zoom forti
        if n >= 2:
            acc = None
            for k in range(n):
                tt = a + (b - a) * k / (n - 1)
                bx = cam.box(tt, fino)
                img = np.asarray(im.resize((W_OUT, H_OUT), Image.LANCZOS,
                                           box=(bx[0], bx[1], bx[0] + bx[2], bx[1] + bx[3])), dtype=np.float32)
                acc = img if acc is None else acc + img
            return acc / n
    return np.asarray(im.resize((W_OUT, H_OUT), Image.LANCZOS, box=(x0, y0, x0 + w, y0 + h)), dtype=np.float32)


# ------------------------------------------------------------------ look
def _cube(nome):
    """i look come LUT 3D (operazioni di colore puntuali); la vignetta e a parte"""
    from .progetto import CACHE
    path = CACHE / f"look-{nome}-v2.cube"
    if path.exists():
        return path
    CACHE.mkdir(exist_ok=True)
    N = 33
    g = np.linspace(0, 1, N)
    bb, gg, rr = np.meshgrid(g, g, g, indexing='ij')       # .cube: il rosso varia piu in fretta
    rgb = np.stack([rr, gg, bb], -1).reshape(-1, 3)
    out = LOOK[nome](rgb)
    out = np.clip(out, 0, 1)
    with open(str(path) + '.tmp', 'w') as fh:
        fh.write(f"# look {nome}\nLUT_3D_SIZE {N}\n")
        np.savetxt(fh, out, fmt='%.6f')
    os.replace(str(path) + '.tmp', path)
    return path


def _hsv(rgb):
    mx, mn = rgb.max(1), rgb.min(1)
    d = mx - mn + 1e-9
    r, g, b = rgb[:, 0], rgb[:, 1], rgb[:, 2]
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = (mx - mn) / (mx + 1e-9)
    return h, s, mx


def _curva(x, contrasto, pivot=0.42):
    """curva a S morbida attorno al pivot, neri e bianchi fermi"""
    y = pivot + (x - pivot) * contrasto
    k = np.clip(x / pivot, 0, 1)
    lo = pivot * (k ** contrasto)
    k2 = np.clip((1 - x) / (1 - pivot), 0, 1)
    hi = 1 - (1 - pivot) * (k2 ** contrasto)
    return np.where(x < pivot, lo, hi) * 0.75 + np.clip(y, 0, 1) * 0.25


def _satura(rgb, quanto, maschera):
    l = rgb @ np.array([0.2126, 0.7152, 0.0722])
    return rgb + (rgb - l[:, None]) * (quanto * maschera)[:, None]


def look_caldo(rgb):
    """A, "caldo naturale": contrasto +12% a S, pelle un filo piu calda (+6% saturazione),
    verdi della pianta -25% (il verde del brand resta l'unico verde forte)"""
    h, s, v = _hsv(rgb)
    pelle = np.exp(-0.5 * ((h - 22) / 14) ** 2) * np.clip(s * 3, 0, 1) * np.clip(v * 2, 0, 1)
    verdi = np.exp(-0.5 * ((h - 110) / 28) ** 2) * np.clip(s * 2, 0, 1)
    x = _satura(rgb, 0.06, pelle)
    x = _satura(x, -0.25, verdi)
    x = x + np.array([0.006, 0.003, -0.004]) * pelle[:, None]
    x = _curva(np.clip(x, 0, 1), 1.12)
    return x * np.array([1.012, 1.0, 0.985])


def look_profondo(rgb):
    """B, "profondo": contrasto +20%, ombre verso il blu notte del brand (split
    toning leggero), pelle protetta (non prende il blu), verdi -35%"""
    h, s, v = _hsv(rgb)
    pelle = np.exp(-0.5 * ((h - 22) / 14) ** 2) * np.clip(s * 3, 0, 1) * np.clip(v * 2, 0, 1)
    verdi = np.exp(-0.5 * ((h - 110) / 28) ** 2) * np.clip(s * 2, 0, 1)
    x = _satura(rgb, -0.35, verdi)
    x = _satura(x, 0.06, pelle)
    x = _curva(np.clip(x, 0, 1), 1.20)
    l = x @ np.array([0.2126, 0.7152, 0.0722])
    ombra = np.clip(1 - l / 0.45, 0, 1) ** 1.5 * (1 - pelle)
    blu = np.array([0.0, 37 / 255, 82 / 255])
    x = x + (blu * 0.55 - x * 0.08) * (ombra * 0.22)[:, None]
    return x


LOOK = {'caldo': look_caldo, 'profondo': look_profondo}
VIGNETTA = {'caldo': 0.14, 'profondo': 0.22}


def _vignetta(quanto):
    y, x = np.mgrid[0:H_OUT, 0:W_OUT].astype(np.float32)
    d = np.sqrt(((x - W_OUT / 2) / (W_OUT / 2)) ** 2 + ((y - H_OUT * 0.45) / (H_OUT / 2)) ** 2) / math.sqrt(2)
    return (1 - quanto * np.clip((d - 0.35) / 0.65, 0, 1) ** 1.8)[..., None].astype(np.float32)


# ------------------------------------------------------------------ immagine
def _sfoca(a, r):
    """sfocatura gaussiana approssimata: tre passate di media mobile per asse"""
    if r < 0.5:
        return a
    k = max(1, int(round(r * 1.2)))
    out = a.astype(np.float32)
    for asse in (0, 1):
        for _ in range(3):
            c = np.cumsum(np.pad(out, [(k + 1, k) if i == asse else (0, 0) for i in range(out.ndim)], mode='edge'),
                          axis=asse, dtype=np.float32)
            sl_a = [slice(None)] * out.ndim
            sl_b = [slice(None)] * out.ndim
            sl_a[asse] = slice(2 * k + 1, None)
            sl_b[asse] = slice(0, -(2 * k + 1))
            out = (c[tuple(sl_a)] - c[tuple(sl_b)]) / (2 * k + 1)
    return out


def _mosso_x(a, px):
    """sfocatura di movimento orizzontale di `px` pixel"""
    k = int(round(px / 2))
    if k < 1:
        return a
    c = np.cumsum(np.pad(a, [(0, 0), (k + 1, k), (0, 0)], mode='edge'), axis=1, dtype=np.float32)
    return (c[:, 2 * k + 1:] - c[:, :-(2 * k + 1)]) / (2 * k + 1)


def _sposta(m, dx, dy):
    out = np.zeros_like(m)
    H, W = m.shape[:2]
    xs, xd = (slice(0, W - dx), slice(dx, W)) if dx >= 0 else (slice(-dx, W), slice(0, W + dx))
    ys, yd = (slice(0, H - dy), slice(dy, H)) if dy >= 0 else (slice(-dy, H), slice(0, H + dy))
    out[yd, xd] = m[ys, xs]
    return out


def _attivo(fx, t):
    """peso 0..1 di un effetto di piatto al tempo t (rampa in entrata e in uscita)"""
    s, e, r = fx['s'], fx['e'], fx.get('rampa', 0.3)
    if t < s or t >= e:
        return 0.0
    return min(1.0, (t - s) / r if r else 1.0, (e - t) / r if r else 1.0)


# ------------------------------------------------------------------ passo 1: piatto
def piatto(P, tempo, cam, spec, cartella):
    """i frame del pezzo dal 4K, con camera, transizioni e look. PNG in `cartella`"""
    meta = P.meta()
    sw, sh = meta['larghezza'], meta['altezza']
    look = spec.get('look')
    trans = [fx for fx in spec.get('piatto', []) if fx['tipo'] == 'spinta']
    vf = [f"fps={P.fps_str}"]
    if look:
        vf.append(f"lut3d=file={_cube(look)}:interp=tetrahedral")
    vf.append("format=rgb24")
    vign = _vignetta(VIGNETTA[look]) if look else None
    cartella.mkdir(parents=True, exist_ok=True)
    fps = P.fps
    for o, k, src in tempo.corse():
        pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-hwaccel', 'videotoolbox', '-ss', f"{src:.6f}",
                               '-i', str(P.sorgente), '-frames:v', str(k), '-an', '-vf', ','.join(vf),
                               '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
        for j in range(k):
            buf = pr.stdout.read(sw * sh * 3)
            if len(buf) < sw * sh * 3:
                sys.exit(f"piatto: frame mancante a {o + j}")
            im = Image.frombuffer('RGB', (sw, sh), buf, 'raw', 'RGB', 0, 1)
            f = o + j
            t = f / fps
            tr = next((x for x in trans if abs(t - x['t']) < x['dur'] / 2), None)
            if tr is None:
                a = ritaglia(im, cam.box(t), cam, t, fps)
            else:
                a = _spinta(im, cam, tr, t, fps)
            if vign is not None:
                a = a * vign
            Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8)).save(cartella / f"f{f:06d}.png",
                                                                            compress_level=1)
        pr.wait()
    return cartella


def _spinta(im, cam, tr, t, fps):
    """transizione a spinta: il quadro A esce di lato mentre B (l'inquadratura dopo il
    taglio a tr.t) entra spingendolo, con sfocatura di movimento sulla velocita"""
    T, d = tr['t'], tr['dur']
    p0 = (t - (T - d / 2)) / d
    p = ease(tr.get('ease', 'expo.inOut'), p0)
    dp = (ease(tr.get('ease', 'expo.inOut'), p0 + 0.25 / (d * fps)) -
          ease(tr.get('ease', 'expo.inOut'), p0 - 0.25 / (d * fps)))
    A = ritaglia(im, cam.box(min(t, T - 1e-4), fino=T), blur=False)
    B = ritaglia(im, cam.box(max(t, T)), blur=False)
    dx = int(round(p * W_OUT)) * (1 if tr.get('dir', 'sx') == 'dx' else -1)
    out = np.empty_like(A)
    if dx <= 0:
        x = -dx
        out[:, :W_OUT - x] = A[:, x:]
        out[:, W_OUT - x:] = B[:, :x]
    else:
        out[:, dx:] = A[:, :W_OUT - dx]
        out[:, :dx] = B[:, W_OUT - dx:]
    pan = tr.get('pannello')
    scia = abs(dp) * W_OUT * tr.get('scia', 1.0)
    out = _mosso_x(out, scia)
    if pan:
        # una lastra blu notte passa davanti alla spinta, piu veloce (parallasse) e un
        # frame in anticipo: bordo d'attacco netto, scia solo sul bordo di coda, ombra
        # morbida sul video davanti a lei
        pw = int(W_OUT * pan.get('larghezza', 0.38))
        v = pan.get('velocita', 1.5)
        pa = ease(tr.get('ease', 'expo.inOut'), p0 + 1 / (d * fps))
        q = min(1.0, max(0.0, (pa - 0.5) * v + 0.5))
        sx = tr.get('dir', 'sx') == 'sx'
        x0 = W_OUT - q * (W_OUT + pw) if sx else -pw + q * (W_OUT + pw)
        xs = np.arange(W_OUT, dtype=np.float32)
        coda = max(2.0, scia * 1.5)
        if sx:      # si muove verso sinistra: attacco a sinistra (netto), coda a destra
            al = np.clip(xs - x0 + 1, 0, 1) * np.clip((x0 + pw - xs) / coda, 0, 1)
            om = np.clip(1 - (x0 - xs) / 90, 0, 1) * (xs < x0)
        else:
            al = np.clip(x0 + pw - xs + 1, 0, 1) * np.clip((xs - x0) / coda, 0, 1)
            om = np.clip(1 - (xs - x0 - pw) / 90, 0, 1) * (xs > x0 + pw)
        out = out * (1 - 0.45 * om ** 1.5)[None, :, None]
        col = np.array(pan.get('colore', [0, 37, 81]), np.float32)
        out = out * (1 - al)[None, :, None] + col * al[None, :, None]
    return out


# ------------------------------------------------------------------ passo 2: sagome
def sagome(piatti, cartella):
    from .visione import binario
    cartella.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([str(binario()), 'sagome', str(piatti), str(cartella)], stderr=subprocess.PIPE, text=True)
    if r.returncode:
        sys.exit(f"sagome fallite: {r.stderr[-300:]}")
    n_p = len(list(piatti.glob('*.png')))
    n_s = len(list(cartella.glob('*.png')))
    if n_s < n_p:
        sys.exit(f"sagome: {n_s} su {n_p} frame")
    return cartella


class Sagome:
    """sagoma al frame f, media su 3 frame e ammorbidita (come i titoli dietro)"""

    def __init__(self, cartella, n):
        self.c, self.n, self.cache = cartella, n, {}

    def raw(self, f):
        f = min(max(f, 0), self.n - 1)
        if f not in self.cache:
            if len(self.cache) > 8:
                self.cache.pop(min(self.cache))
            self.cache[f] = np.asarray(Image.open(self.c / f"f{f:06d}.png").convert('L'), dtype=np.float32) / 255
        return self.cache[f]

    def __call__(self, f, tagli_f=()):
        vic = [g for g in (f - 1, f, f + 1)
               if 0 <= g < self.n and not any(min(f, g) < c <= max(f, g) for c in tagli_f)]
        m = sum(self.raw(g) for g in vic) / len(vic)
        return _sfoca(m[..., None], 1.4)[..., 0]


# ------------------------------------------------------------------ passo 3: strati
def ambiente_hf():
    from .inserti import ambiente
    return ambiente()


def strato_html(spec, strato, cartella, materiali):
    """la pagina HyperFrames di uno strato: tutti gli elementi di quello strato"""
    from .inserti import _css_brand, GSAP, LOGO, PITTOGRAMMA
    if cartella.exists():
        shutil.rmtree(cartella)
    (cartella / 'assets').mkdir(parents=True)
    for f in (FONT, GSAP, LOGO, PITTOGRAMMA):
        shutil.copy2(f, cartella / 'assets' / f.name)
    shutil.copy2(SCENE / '_scena.js', cartella / 'assets' / 'scena.js')
    (cartella / 'assets' / 'comune.css').write_text(_css_brand(), encoding='utf-8')
    for nome, src in materiali.items():
        shutil.copy2(src, cartella / 'assets' / nome)
    el = [x for x in spec['elementi'] if x.get('strato', 'davanti') == strato]
    modelli = sorted({x['modello'] for x in el})
    stile = '\n'.join((SCENE / f"{m}.css").read_text(encoding='utf-8') for m in modelli if (SCENE / f"{m}.css").exists())
    script = '\n'.join((SCENE / f"{m}.js").read_text(encoding='utf-8') for m in modelli)
    durata = spec['_frames'] / spec['_fps']
    dati = {'durata': durata, 'fps': spec['_fps'], 'strato': strato, 'elementi': el, 'cam': spec.get('_cam', [])}
    html = (SCENE / '_scena.html').read_text(encoding='utf-8') \
        .replace('/*__STILE__*/', stile).replace('/*__MODELLI__*/', script) \
        .replace('__DURATA__', f"{durata:.6f}").replace('__DATI__', json.dumps(dati, ensure_ascii=False)) \
        .replace('__MB__', 'data-motion-blur="on"' if spec.get('mosso_hf', True) else '')
    (cartella / 'index.html').write_text(html, encoding='utf-8')
    return cartella


def render_strato(cartella, out, fps_str, frames):
    from .inserti import HF
    tmp = out.with_suffix('.tmp.mov')
    from .inserti import dimentica
    r = subprocess.run([str(HF), 'render', str(cartella), '--fps', fps_str, '--format', 'mov', '-o', str(tmp),
                        '--quiet'], env=ambiente_hf(), capture_output=True, text=True)
    dimentica(cartella)          # la cronologia di HyperFrames non tiene copie (foto dei pazienti)
    if r.returncode or not tmp.exists():
        sys.exit(f"render HyperFrames fallito ({cartella.name}):\n{(r.stderr or r.stdout)[-1500:]}")
    pr = subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries',
                         'stream=nb_read_packets,pix_fmt', '-of', 'json', str(tmp)], capture_output=True, text=True)
    s = json.loads(pr.stdout)['streams'][0]
    if int(s['nb_read_packets']) != frames:
        sys.exit(f"{cartella.name}: {s['nb_read_packets']} frame invece di {frames}")
    os.replace(tmp, out)


class Strato:
    """legge un MOV con alfa frame per frame (RGBA a 16 bit -> float)"""

    def __init__(self, mov):
        self.pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(mov), '-f', 'rawvideo', '-pix_fmt', 'rgba64le',
                                    '-'], stdout=subprocess.PIPE)
        self.sz = W_OUT * H_OUT * 8

    def __next__(self):
        b = self.pr.stdout.read(self.sz)
        if len(b) < self.sz:
            raise StopIteration
        a = np.frombuffer(b, dtype='<u2').reshape(H_OUT, W_OUT, 4).astype(np.float32) / 65535
        return a[..., :3] * 255, a[..., 3:4]


# ------------------------------------------------------------------ passo 4: composizione
MISURE = {}


def componi(P, spec, tempo, cart, out_video, audio, mani=None):
    MISURE.clear()
    n, fps = tempo.n, P.fps
    piatti = cart / 'piatto'
    ha_sag = (cart / 'sagome').is_dir()
    sag = Sagome(cart / 'sagome', n) if ha_sag else None
    tagli_f = [int(round(t * fps)) for t in tempo.tagli()]
    dietro = Strato(cart / 'dietro.mov') if (cart / 'dietro.mov').exists() else None
    davanti = Strato(cart / 'davanti.mov') if (cart / 'davanti.mov').exists() else None
    fx = [x for x in spec.get('piatto', []) if x['tipo'] != 'spinta']
    ombra = spec.get('ombra', {'dx': 26, 'dy': 14, 'raggio': 22, 'quanto': 0.55})
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s',
                            f"{W_OUT}x{H_OUT}", '-framerate', P.fps_str, '-i', '-', '-i', str(audio),
                            '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,'
                                   'setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-profile:v', 'high',
                            '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                            '-color_range', 'tv', '-g', '50', '-c:a', 'aac', '-b:a', '192k',
                            '-frames:v', str(n), '-t', f"{n / fps:.6f}",
                            '-movflags', '+faststart', str(out_video)], stdin=subprocess.PIPE)
    yy = np.linspace(0, 1, H_OUT, dtype=np.float32)[:, None, None]
    # elementi con le mani davanti (la scritta sta fra il busto e le mani)
    mani_davanti = [(x['s'], x['e']) for x in spec['elementi'] if x.get('mani_davanti')]
    mani_max = min([x.get('mani_max', 0.18) for x in spec['elementi'] if x.get('mani_davanti')] or [0.18])
    # pezzi di mano piu stretti di `mani_minimo` px non passano davanti alle lettere
    # (fase 7b: un dito bucava la «p» di «sporge»; la mano intera resta davanti)
    mani_min = max([int(x.get('mani_minimo', 0)) for x in spec['elementi'] if x.get('mani_davanti')] or [0])
    for f in range(n):
        t = f / fps
        a = np.asarray(Image.open(piatti / f"f{f:06d}.png"), dtype=np.float32)
        m = sag(f, tagli_f)[..., None] if sag else None
        for x in fx:
            w = _attivo(x, t)
            if w <= 0:
                continue
            if x['tipo'] in ('sfoca_sfondo', 'fuoco'):
                inv = 1 - m
                bl = _sfoca(a * inv, x.get('raggio', 8) * w) / np.maximum(_sfoca(inv, x.get('raggio', 8) * w), 1e-3)
                a = a * m + bl * inv
                if x['tipo'] == 'fuoco':
                    # la messa a fuoco va sulla grafica: lo sfondo scende di piu, lui appena
                    a = a * (1 - w * (x.get('scuro', 0.22) * inv + x.get('scuro_persona', 0.06) * m))
            elif x['tipo'] == 'finestra':
                continue                          # dopo gli strati dietro (vedi sotto)
            elif x['tipo'] == 'sfoca_tutto':
                a = _sfoca(a, x.get('raggio', 30) * w) * (1 - x.get('scuro', 0.5) * w)
            elif x['tipo'] == 'scurisci':
                q = x.get('quanto', 0.3) * w
                dove = x.get('dove', 'sfondo')
                if dove == 'sfondo':
                    a = a * (1 - q * (1 - m))
                elif dove == 'basso':
                    g = np.clip((yy - x.get('da', 0.45)) / (1 - x.get('da', 0.45)), 0, 1) ** 1.3
                    a = a * (1 - q * g)
                else:
                    a = a * (1 - q)
            elif x['tipo'] == 'velo':
                # campionario v3 (direttore): velo blu del brand sotto le grafiche sul girato, cosi il
                # verde sta sempre sul blu; 'dove' basso (gradiente dal basso) o radiale (ellisse)
                col = np.array(x.get('colore', [0, 26, 61]), np.float32)
                if x.get('dove', 'basso') == 'basso':
                    g = np.clip((yy - x.get('da', 0.58)) / (1 - x.get('da', 0.58)), 0, 1) ** 1.1
                else:
                    g = _velo_ellisse(x['cx'], x['cy'], x['rx'], x['ry'])
                q = x.get('quanto', 0.72) * w * g
                a = a * (1 - q) + col * q
            elif x['tipo'] == 'vetro':
                # fase 7b rivista (reference martell-06): pannello di vetro smerigliato,
                # lo studio vero si vede sfocato e un poco schiarito dentro un
                # rettangolo arrotondato; bordo, riflesso e testo li disegna lo strato
                # davanti (modello `vetro`). Anche una mano che ci passa dietro si sfoca.
                x0, y0, ww, hh = int(x['x']), int(x['y']), int(x['larghezza']), int(x['altezza'])
                r_ = int(x.get('raggio_sf', 26))
                pad = 3 * r_
                X0, Y0 = max(0, x0 - pad), max(0, y0 - pad)
                X1, Y1 = min(W_OUT, x0 + ww + pad), min(H_OUT, y0 + hh + pad)
                bl = _sfoca(a[Y0:Y1, X0:X1], r_)[y0 - Y0:y0 - Y0 + hh, x0 - X0:x0 - X0 + ww]
                # `guadagno` (fase 7b, scelta B di Riccardo): il vetro schiarisce lo studio
                # dietro invece di scurirlo, come in martell-06 (sul muro scuro era un riquadro scuro)
                bl = np.clip(bl * x.get('guadagno', 1.0), 0, 255)
                tinta = np.array(x.get('tinta', [214, 226, 238]), np.float32)
                bl = bl * (1 - x.get('chiaro', 0.16)) + tinta * x.get('chiaro', 0.16)
                mk = _maschera_tonda(ww, hh, int(x.get('raggio', 40))) * w
                a[y0:y0 + hh, x0:x0 + ww] = a[y0:y0 + hh, x0:x0 + ww] * (1 - mk) + bl * mk
            elif x['tipo'] == 'lampo':
                # passaggio fra i due mondi: un lampo di luce di 3-4 frame (reference martell-02)
                col = np.array(x.get('colore', [244, 244, 244]), np.float32)
                q = x.get('quanto', 0.85) * w
                a = a * (1 - q) + col * q
            elif x['tipo'] == 'luce':
                # luce morbida colorata sulla parete (dietro di lui): profondita, non un pannello
                cx, cy, r = x['x'] * W_OUT, x['y'] * H_OUT, x['r'] * W_OUT
                g = _luce_cache(cx, cy, r)
                col = np.array(x.get('colore', [0, 37, 82]), np.float32)
                q = x.get('quanto', 0.5) * w * g * ((1 - m) if m is not None else 1)
                a = a * (1 - q) + col * q
        # fase 7c (Riccardo): «lui nel cerchio» con la finestra SOPRA gli strati del disegno, cosi lo
        # scheletro entra mentre lui si stringe (prima la finestra si componeva sotto lo strato davanti)
        cerchio = next(((x, _finestra_p(x, t)) for x in fx if x['tipo'] == 'finestra' and x.get('cerchio')
                        and _finestra_p(x, t)), None)
        if cerchio:
            sorgente, a = a, fondo_brand().copy()
        if dietro is not None:
            rgb, al = next(dietro)
            if al.max() > 0.002 and cerchio:
                a = rgb * al + a * (1 - al)
            elif al.max() > 0.002:
                if ombra.get('quanto', 0) > 0:
                    sh = _sfoca(_sposta(m[..., 0], ombra['dx'], ombra['dy'])[..., None], ombra['raggio'])
                    rgb = rgb * (1 - ombra['quanto'] * sh)
                comp = rgb * al + a * (1 - al)
                a = a * m + comp * (1 - m)
        for x in fx:
            if x['tipo'] == 'finestra' and not x.get('cerchio'):
                a = _finestra(a, x, t)
        if davanti is not None:
            rgb, al = next(davanti)
            if al.max() > 0.002:
                prima = a
                a = rgb * al + a * (1 - al)
                if not cerchio and m is not None and mani is not None and any(s_ <= t < e_ for s_, e_ in mani_davanti):
                    mt = matte_mani(prima, m, mani.al(f))
                    if mt is not None and mani_min > 1:
                        k_ = mani_min | 1
                        ap = np.asarray(Image.fromarray((mt[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(k_))
                                        .filter(ImageFilter.MaxFilter(k_)), np.float32)[..., None] / 255
                        mt = np.minimum(mt, _sfoca(ap, 1.5))
                    if mt is not None:
                        pieno = al > 0.5
                        area = float(pieno.sum())
                        if area > 2000:
                            cop = float((mt * pieno).sum()) / area
                            # tetto: le mani non nascondono piu del 18% delle lettere; oltre,
                            # sulle lettere diventano un poco trasparenti (la parola si legge)
                            if cop > mani_max:
                                mt = mt * (1 - pieno * (1 - mani_max / cop))
                                cop = float((mt * pieno).sum()) / area
                            MISURE.setdefault('mani_serie', []).append((cop, area, round(t, 2)))
                        a = a * (1 - mt) + prima * mt
        if cerchio:
            xc, (pc, mc) = cerchio
            a = _finestra_cerchio(sorgente, xc, pc, mc, sfondo=a)
        enc.stdin.write(np.clip(a + 0.5, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()
    if enc.returncode:
        sys.exit("encoder fallito")


def matte_mani(img, m, mani, allarga=46):
    """le mani (e gli avambracci) davanti alla grafica: sagoma della persona x zone
    delle mani di Vision (allargate) x pelle (la divisa blu notte resta dietro).
    Bordi ammorbiditi di 1,5 px."""
    if not mani:
        return None
    zona = np.zeros((H_OUT, W_OUT), np.float32)
    for h in mani:
        a0, b0, a1, b1 = [int(round(v)) for v in h['box']]
        zona[max(0, b0 - allarga):min(H_OUT, b1 + allarga), max(0, a0 - allarga):min(W_OUT, a1 + allarga)] = 1
    if zona.max() == 0:
        return None
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    pelle = ((r > 70) & (r > g) & (r > b) & (r - g > 10) & (mx - mn > 18)).astype(np.float32)
    mt = zona * m[..., 0] * pelle
    # chiude i buchi (unghie, riflessi) e ammorbidisce
    mt = np.asarray(Image.fromarray((mt * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(5))
                    .filter(ImageFilter.MinFilter(3)), np.float32) / 255
    mt = mt * m[..., 0]
    return _sfoca(mt[..., None], 1.5)


_FONDO = {}


def fondo_brand():
    """fondo del brand per la finestra: il fondo del sito (blu abisso con la luce radiale
    dall'alto, fase 7c), vignetta, grana fine fissa (seminata)"""
    if 'f' not in _FONDO:
        y, x = np.mgrid[0:H_OUT, 0:W_OUT].astype(np.float32)
        # fase 7c: il fondo del sito, radial-gradient(120% 80% at 50% 0%, #00346F 0%, #002552 45%, #000F2B 100%)
        d0 = np.sqrt(((x - W_OUT / 2) / (1.2 * W_OUT)) ** 2 + (y / (0.8 * H_OUT)) ** 2)
        c0, c1, c2 = (np.array(v, np.float32) for v in ([0, 52, 111], [0, 37, 82], [0, 15, 43]))
        k1 = np.clip(d0 / 0.45, 0, 1)[..., None]
        k2 = np.clip((d0 - 0.45) / 0.55, 0, 1)[..., None]
        a = np.where(d0[..., None] < 0.45, c0 + (c1 - c0) * k1, c1 + (c2 - c1) * k2)
        d = np.sqrt(((x - W_OUT / 2) / (W_OUT / 2)) ** 2 + ((y - H_OUT / 2) / (H_OUT / 2)) ** 2) / math.sqrt(2)
        a = a * (1 - 0.35 * np.clip((d - 0.4) / 0.6, 0, 1) ** 1.6)[..., None]
        rng = np.random.default_rng(7)
        a = a + rng.normal(0, 1.6, (H_OUT, W_OUT, 1)).astype(np.float32)
        _FONDO['f'] = a
    return _FONDO['f']


def _velo_ellisse(cx, cy, rx, ry):
    k = ('velo', cx, cy, rx, ry)
    if k not in _FONDO:
        y, x = np.mgrid[0:H_OUT, 0:W_OUT].astype(np.float32)
        d = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
        _FONDO[k] = (np.clip(1 - d, 0, 1) ** 0.8)[..., None]
    return _FONDO[k]


def _maschera_tonda(w, h, r):
    k = ('m', w, h, r)
    if k not in _FONDO:
        m = Image.new('L', (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
        _FONDO[k] = np.asarray(m, np.float32)[..., None] / 255
    return _FONDO[k]


def _finestra_p(x, t):
    """(progresso 0-1, sfocatura di movimento) della finestra al tempo t, o None se spenta"""
    s, e = x['s'], x['e']
    di, du = x.get('entra', 0.5), x.get('esce', 0.4)
    if t < s or t >= e + du:
        return None
    cv = 'power3.inOut' if x.get('cerchio') else 'expo.inOut'
    p = ease(cv, (t - s) / di) if t < s + di else (1.0 if t < e else 1 - ease(cv, (t - e) / du))
    if p <= 0.001:
        return None
    mov = 0.0 if s + di <= t < e else math.sin(math.pi * min(1.0, max(0.0, p)))
    return p, mov * x.get('mosso', 10)


def _finestra(a, x, t):
    """il quadro diventa una finestra (angoli tondi, ombra morbida) sul fondo del
    brand: spazio grande e pulito per un momento forte (CTA). Entra e esce con
    expo; x, y = centro della finestra, scala = lato rispetto al quadro"""
    s, e = x['s'], x['e']
    di, du = x.get('entra', 0.5), x.get('esce', 0.4)
    if t < s or t >= e + du:
        return a
    cv = 'power3.inOut' if x.get('cerchio') else 'expo.inOut'
    p = ease(cv, (t - s) / di) if t < s + di else (1.0 if t < e else 1 - ease(cv, (t - e) / du))
    if p <= 0.001:
        return a
    if x.get('cerchio'):
        # sfocatura di movimento proporzionale alla velocita (piu forte a meta corsa)
        mov = 0.0 if s + di <= t < e else math.sin(math.pi * min(1.0, max(0.0, p)))
        return _finestra_cerchio(a, x, p, mov * x.get('mosso', 10))
    sc = 1 + (x.get('scala', 0.6) - 1) * p
    cx = W_OUT / 2 + (x.get('x', 640) - W_OUT / 2) * p
    cy = H_OUT / 2 + (x.get('y', 540) - H_OUT / 2) * p
    w, h = int(round(W_OUT * sc)), int(round(H_OUT * sc))
    r = int(round(x.get('raggio', 34) * p))
    im = Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    if x.get('inclina'):
        return _finestra_inclinata(im, x, p, cx, cy, w, h, r)
    out = fondo_brand().copy()
    # ombra morbida sotto la finestra (cresce con p)
    om = np.zeros((H_OUT, W_OUT), np.float32)
    oy = int(28 * p)
    om[max(0, y0 + oy):min(H_OUT, y0 + oy + h), max(0, x0):min(W_OUT, x0 + w)] = 1
    om = _sfoca(om[..., None], 34)
    out = out * (1 - 0.6 * p * om)
    msk = _maschera_tonda(w, h, max(r, 1)) if r > 0 else np.ones((h, w, 1), np.float32)
    ya, yb, xa, xb = max(0, y0), min(H_OUT, y0 + h), max(0, x0), min(W_OUT, x0 + w)
    src = np.asarray(im, np.float32)[ya - y0:yb - y0, xa - x0:xb - x0]
    mm = msk[ya - y0:yb - y0, xa - x0:xb - x0]
    # bordo sottile panna al 14%, come le card
    out[ya:yb, xa:xb] = src * mm + out[ya:yb, xa:xb] * (1 - mm)
    if r > 2:
        stretta = Image.fromarray((mm[..., 0] * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(5))
        anello = mm - np.asarray(stretta, np.float32)[..., None] / 255
        out[ya:yb, xa:xb] = out[ya:yb, xa:xb] * (1 - 0.14 * anello) + 244 * 0.14 * anello
    return out


def _finestra_cerchio(a, x, p, mosso=0.0, sfondo=None):
    """campionario v3 (reference gadzhi-09): il quadro di lui si stacca, diventa un
    rettangolo tondo e poi un cerchio nell'angolo (diametro `diametro` px, centro x/y),
    con un anello di luce verde; il suo volto resta al centro (`fuoco` = frazioni del
    quadro, `zoom` finale sul volto). Dietro, il fondo del brand."""
    D = x.get('diametro', 380)
    w = W_OUT * (1 - p) + D * p
    h = H_OUT * (1 - p) + D * p
    cx = W_OUT / 2 + (x.get('x', 1600) - W_OUT / 2) * p
    cy = H_OUT / 2 + (x.get('y', 800) - H_OUT / 2) * p
    r = min(w, h) / 2 * (p ** 0.8)
    fx, fy = x.get('fuoco', [0.5, 0.42])
    z = 1 + (x.get('zoom', 1.5) - 1) * p
    # ritaglio della sorgente con l'aspetto della finestra, centrato sul volto
    A = w / h
    ch = H_OUT / z
    cw = min(W_OUT, ch * A)
    ch = cw / A
    sx = min(max(fx * W_OUT * (1 - p) + fx * W_OUT * p - cw / 2, 0), W_OUT - cw) if p > 0 else 0
    sx = min(max(W_OUT / 2 * (1 - p) + fx * W_OUT * p - cw / 2, 0), W_OUT - cw)
    sy = min(max(H_OUT / 2 * (1 - p) + fy * H_OUT * p - ch / 2, 0), H_OUT - ch)
    src = Image.fromarray(np.clip(a + 0.5, 0, 255).astype(np.uint8)).crop(
        (int(sx), int(sy), int(sx + cw), int(sy + ch)))
    wi, hi = max(2, int(round(w))), max(2, int(round(h)))
    im = np.asarray(src.resize((wi, hi), Image.LANCZOS), np.float32)
    if mosso > 0.8:
        im = _sfoca(im, mosso)
    x0, y0 = int(round(cx - wi / 2)), int(round(cy - hi / 2))
    out = fondo_brand().copy() if sfondo is None else sfondo.copy()
    msk = _maschera_tonda(wi, hi, max(1, int(round(r)))) if r >= 1 else np.ones((hi, wi, 1), np.float32)
    # ombra morbida
    om = np.zeros((H_OUT, W_OUT), np.float32)
    ya, yb, xa, xb = max(0, y0), min(H_OUT, y0 + hi), max(0, x0), min(W_OUT, x0 + wi)
    om[min(H_OUT, ya + 24):min(H_OUT, yb + 24), xa:xb] = msk[ya - y0:yb - y0, xa - x0:xb - x0, 0][:max(0, min(H_OUT, yb + 24) - min(H_OUT, ya + 24))]
    out = out * (1 - 0.55 * p * _sfoca(om[..., None], 30))
    mm = msk[ya - y0:yb - y0, xa - x0:xb - x0]
    out[ya:yb, xa:xb] = im[ya - y0:yb - y0, xa - x0:xb - x0] * mm + out[ya:yb, xa:xb] * (1 - mm)
    # anello di luce verde (2 strati: stretto e largo), cresce con p
    if p > 0.05 and r > 4:
        anello = np.zeros((H_OUT, W_OUT), np.float32)
        pad = np.pad(mm[..., 0], 8)            # margine: l'erosione deve vedere il bordo anche sui lati dritti
        stretta = np.asarray(Image.fromarray((pad * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(9)), np.float32)[8:-8, 8:-8] / 255
        anello[ya:yb, xa:xb] = np.clip(mm[..., 0] - stretta, 0, 1)
        verde = np.array([114, 250, 147], np.float32)
        largo = _sfoca(anello[..., None], 18)[..., 0]
        q = (0.95 * anello + 0.55 * np.clip(largo * 2.2, 0, 1)) * p
        out = out * (1 - q[..., None]) + verde * q[..., None]
    return out


def _coeff_prospettiva(dst, src):
    """coefficienti di PIL.Image.transform(PERSPECTIVE): per ogni punto d'uscita il
    punto d'ingresso (dst: 4 angoli d'uscita, src: 4 angoli d'ingresso)"""
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B.append(v)
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def _finestra_inclinata(im, x, p, cx, cy, w, h, r):
    """la finestra ruotata di `inclina` gradi attorno all'asse verticale: il lato
    verso il testo (destra) si allontana. Angoli tondi, bordo panna 14%, ombra lunga."""
    ang = math.radians(x['inclina'] * p)
    # prospettiva leggibile: il lato lontano si accorcia del tan(angolo) x 1,1 della
    # sua altezza (5 gradi: circa il 10%, 22 px per lato su una finestra di 454 px)
    d = w * (1 - math.cos(ang)) * 0.5 + w * math.tan(ang) * 0.12
    x0, x1 = cx - w / 2 + d * 0.3, cx + w / 2 - d
    y0, y1 = cy - h / 2, cy + h / 2
    dy = h * math.tan(ang) * 0.55
    quad = [(x0, y0), (x1, y0 + dy), (x1, y1 - dy), (x0, y1)]
    rgba = im.convert('RGBA')
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=max(r, 1), fill=255)
    rgba.putalpha(m)
    bordo = Image.new('L', (w, h), 0)
    ImageDraw.Draw(bordo).rounded_rectangle([0, 0, w - 1, h - 1], radius=max(r, 1), outline=255, width=2)
    pann = Image.new('RGBA', (w, h), (244, 244, 244, 0))
    pann.putalpha(bordo.point(lambda v: int(v * 0.14)))
    rgba = Image.alpha_composite(rgba, pann)
    co = _coeff_prospettiva(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    lay = rgba.transform((W_OUT, H_OUT), Image.PERSPECTIVE, co, Image.BICUBIC)
    L = np.asarray(lay, np.float32)
    al = L[..., 3:4] / 255
    out = fondo_brand().copy()
    om = _sfoca(_sposta(al[..., 0], 26, 40)[..., None], 46)
    out = out * (1 - 0.62 * p * om)
    return L[..., :3] * al + out * (1 - al)


_LUCI = {}


def _luce_cache(cx, cy, r):
    k = (round(cx), round(cy), round(r))
    if k not in _LUCI:
        y, x = np.mgrid[0:H_OUT, 0:W_OUT].astype(np.float32)
        d2 = ((x - cx) ** 2 + (y - cy) ** 2) / (r * r)
        _LUCI[k] = np.exp(-d2 * 1.6)[..., None]
    return _LUCI[k]


# ------------------------------------------------------------------ passo 5: suono
def _voce(P, tempo):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(P.asset('voce-montata.wav')), '-ac', '2', '-ar', '48000',
                        '-f', 'f32le', '-'], capture_output=True)
    v = np.frombuffer(r.stdout, dtype='<f4').reshape(-1, 2)
    pezzi = []
    for fa, fb, o in tempo.pezzi:
        a, b = int(fa / tempo.fps * 48000), int(fb / tempo.fps * 48000)
        x = v[a:b].copy()
        k = 240                                   # 5 ms di dissolvenza ai tagli
        if len(tempo.pezzi) > 1:
            x[:k] *= np.linspace(0, 1, k)[:, None]
            x[-k:] *= np.linspace(1, 0, k)[:, None]
        pezzi.append(x)
    return np.concatenate(pezzi).astype(np.float64)


def _rif_voce(v):
    m = v.mean(1)
    w = 4800
    n = len(m) // w
    e = 10 * np.log10((m[:n * w].reshape(n, w) ** 2).mean(1) + 1e-12)
    e = e[e > e.max() - 30]
    return float(np.median(e))


def mix(P, tempo, eventi, out_wav, musica=None, coda=0.0):
    """voce + effetti (ognuno a `db` rispetto alla voce, col picco un frame dopo
    l'immagine) (+ musica a -30 LUFS che si abbassa sotto la voce) -> -14 LUFS.
    `coda`: secondi dopo la voce (la schermata finale), solo effetti"""
    from . import audio as A
    v = _voce(P, tempo)
    n = int(round((tempo.durata + coda) * 48000)) + 480        # 10 ms di margine: l'encoder taglia ai frame
    v = np.pad(v, ((0, max(0, n - len(v))), (0, 0)))[:n]
    rif = _rif_voce(v)
    bus = np.zeros((n + 48000 * 3, 2))
    giri = {}
    log = []
    for ev in sorted(eventi, key=lambda e: e['t']):
        seme = ev.get('seme')
        if seme is None:
            seme = giri.get(ev['nome'], 0)
            giri[ev['nome']] = seme + 1
        x = SFX.suono(ev['nome'], seme, **ev.get('kw', {}))
        x = x * 10 ** ((rif + ev.get('db', -14) - SFX.rms_forte(x)) / 20)
        if ev.get('pan'):
            p = ev['pan']
            x = x * np.array([math.cos((p + 1) * math.pi / 4), math.sin((p + 1) * math.pi / 4)]) * math.sqrt(2)
        if ev.get('allinea', 'picco') == 'picco':
            t0 = ev['t'] + 1 / tempo.fps - SFX.picco_s(x)
        else:
            t0 = ev['t']
        i = int(round(t0 * 48000))
        if i < 0:
            x, i = x[-i:], 0
        j = min(len(bus), i + len(x))
        bus[i:j] += x[:j - i]
        log.append({'nome': ev['nome'], 'seme': seme, 't': round(ev['t'], 3), 'db': ev.get('db', -14),
                    'perche': ev.get('perche', '')})
    tmp = out_wav.with_suffix('.tmp.wav')
    _wav(tmp, v + bus[:n])
    if musica:
        tmpm = out_wav.with_suffix('.m.wav')
        fc = (f"[1:a]aloop=loop=-1:size=2e9,atrim=0:{tempo.durata:.3f},loudnorm=I=-30:TP=-6,"
              f"afade=t=in:d=0.6,afade=t=out:st={max(0, tempo.durata - 1.0):.3f}:d=1.0[m];"
              f"[0:a]asplit=2[v][vk];[m][vk]sidechaincompress=threshold=0.04:ratio=6:attack=25:release=450[md];"
              f"[v][md]amix=inputs=2:normalize=0:duration=first[mx]")
        ffmpeg('-i', tmp, '-stream_loop', '-1', '-i', musica, '-filter_complex', fc, '-map', '[mx]',
               '-c:a', 'pcm_s24le', '-ar', '48000', tmpm)
        os.replace(tmpm, tmp)
    # -14 LUFS con il picco vero sotto -1 dBTP anche dopo l'AAC (tappa 3: guadagno e poi
    # limitatore abbassavano il volume a -15,3 LUFS; si ripete finche torna, al massimo 5 volte).
    # Il limitatore lavora a 4x (picco vero) con il tetto a -3 dBFS: sul master di YT_POSTURA_32 l'AAC
    # aggiungeva 1,1 dB (mix a -2,0 -> master a -0,9 dBTP, sopra il limite di -1)
    got = A.loudness(tmp)
    g = -14.0 - got['I']
    for _ in range(8):
        ffmpeg('-i', tmp, '-af', f"volume={g:.2f}dB,aresample=192000,alimiter=limit=0.708:attack=2:release=60:level=disabled,"
               "aresample=48000", '-c:a', 'pcm_s24le', '-ar', '48000', out_wav)
        got = A.loudness(out_wav)
        if abs(got['I'] + 14.0) <= 0.1:
            break
        g += 1.3 * (-14.0 - got['I'])     # il limitatore si mangia parte del guadagno: si spinge un po' di piu
    tmp.unlink()
    return log, got


def _wav(path, x):
    import wave
    x = np.clip(x, -1, 1)
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(48000)
        w.writeframes((x * 32767).astype('<i2').tobytes())


# ------------------------------------------------------------------ volto
class Volto:
    """riquadro della testa (volto di Vision + capelli) in px d'uscita, al tempo t"""

    def __init__(self, P, tempo, cam):
        d = P.leggi('volti.json')
        self.c = [(c['t'], max((v for v in c['volti'] if v['conf'] > 0.5), key=lambda v: v['w'] * v['h'],
                               default=None)) for c in d['campioni']]
        self.c = [(t, v) for t, v in self.c if v]
        self.tempo, self.cam = tempo, cam
        m = P.meta()
        self.sw, self.sh = m['larghezza'], m['altezza']

    def box(self, t):
        ts = self.tempo.sorgente(t)
        if ts is None:
            return None
        ts_ = [c[0] for c in self.c]
        i = int(np.searchsorted(ts_, ts))
        i = min(max(i, 1), len(self.c) - 1)
        (t0, a), (t1, b) = self.c[i - 1], self.c[i]
        k = 0 if t1 == t0 else min(1, max(0, (ts - t0) / (t1 - t0)))
        v = {q: a[q] + (b[q] - a[q]) * k for q in ('x', 'y', 'w', 'h')}
        # capelli sopra (40% dell'altezza del volto) e un margine ai lati
        x0, y0 = (v['x'] - 0.12 * v['w']) * self.sw, (v['y'] - 0.40 * v['h']) * self.sh
        x1, y1 = (v['x'] + 1.12 * v['w']) * self.sw, (v['y'] + 1.05 * v['h']) * self.sh
        bx = self.cam.box(t)
        s = W_OUT / bx[2]
        return ((x0 - bx[0]) * s, (y0 - bx[1]) * s, (x1 - bx[0]) * s, (y1 - bx[1]) * s)


# ------------------------------------------------------------------ controlli
def controlla(P, spec, tempo, cart, volto, mani=None):
    """le regole di mestiere misurabili: volto mai coperto dallo strato davanti, al
    massimo 2 elementi insieme, ogni elemento leggibile almeno 1 s"""
    fps = P.fps
    esiti = []
    el = spec['elementi']
    # 1) al massimo 2 elementi insieme (i figli di un elemento contano a parte)
    pezzi = []
    for x in el:
        if x['modello'] == 'etichetta':
            continue                              # etichetta di servizio del campionario
        for c in x.get('dati', {}).get('card') or x.get('dati', {}).get('battute') or [{'s': x['s'], 'e': x['e']}]:
            pezzi.append((c['s'], c['e'], x['modello']))
    mx, quando = 0, None
    for f in range(tempo.n):
        t = f / fps
        k = sum(1 for s, e, _ in pezzi if s <= t < e)
        if k > mx:
            mx, quando = k, t
    esiti.append(('al massimo 2 elementi insieme', f"massimo {mx} (a {quando:.2f} s)" if quando is not None else "0",
                  mx <= 2))
    # 2) leggibile almeno 1 s
    corti = [f"{m} {e - s:.2f} s" for s, e, m in pezzi if e - s < 1.0]
    esiti.append(('ogni elemento a schermo almeno 1 s', ', '.join(corti) or 'tutti', not corti))
    # 2b) strato dietro: quanta parte la persona ne copre davvero (alfa renderizzato x sagoma)
    if (cart / 'dietro.mov').exists() and (cart / 'sagome').is_dir():
        sag = Sagome(cart / 'sagome', tempo.n)
        st = Strato(cart / 'dietro.mov')
        arrivi = [x['dati'].get('arrivo', x['s']) for x in el if x.get('strato') == 'dietro']
        t_ok = min(arrivi) if arrivi else 0
        peggio, dove = 0.0, None
        for f in range(tempo.n):
            _, al = next(st)
            if f / fps < t_ok:
                continue
            sa = float(al.sum())
            if sa < 500:
                continue
            c = float((al[..., 0] * sag.raw(f)).sum()) / sa
            if c > peggio:
                peggio, dove = c, f / fps
        esiti.append(('strato dietro coperto dalla persona al massimo il 15%',
                      f"massimo {peggio * 100:.1f}%" + (f" a {dove:.2f} s" if dove is not None else ''), peggio <= 0.15))
    # 2c) zona sicura (fase 6c, dal revisore visivo: testo dell'aggancio oltre il bordo,
    # card a 70 px dal bordo): pixel coperti davvero (alfa > 0,5) dello strato davanti
    # fuori dai 96 px laterali e dai 54 sopra e sotto, schermate piene escluse
    if (cart / 'davanti.mov').exists():
        # il pannello della frase chiave (variante B) arriva al bordo apposta: come le schermate
        fuori, quando = fuori_zona(cart / 'davanti.mov', [(x['s'], x['e']) for x in el
                                                          if x.get('pieno') or x['modello'] == 'frase_chiave'], fps, tempo.n)
        esiti.append(('strato davanti dentro la zona sicura (96/54 px)',
                      f"massimo {fuori} px fuori" + (f" a {quando:.2f} s" if quando is not None else ''), fuori <= 400))
    # 2c-bis) nessun testo fuori dal quadro, entrate comprese (fase 7b rivista: «La
    # pancia sporge» toccava il bordo destro mentre entrava e la zona sicura, con la
    # sua tolleranza di 400 px, lo lasciava passare). Su ogni frame, pixel pieni
    # dello strato sul bordo del quadro (3 px): devono essere zero. Esenti solo le
    # schermate piene, il pannello della frase chiave e gli elementi con "al_bordo"
    for strato in ('davanti', 'dietro'):
        mov = cart / f"{strato}.mov"
        if not mov.exists():
            continue
        esenti = [(x['s'], x['e']) for x in el if x.get('pieno') or x.get('al_bordo')
                  or x['modello'] in ('frase_chiave',)]
        n_fr, px, quando = fuori_quadro(mov, esenti, fps, tempo.n)
        esiti.append((f"strato {strato}: niente fuori dal quadro, su ogni frame",
                      f"{n_fr} frame sul bordo" + (f" (massimo {px} px, primo a {quando:.2f} s)" if n_fr else ''),
                      n_fr == 0))
    # 2c-ter) testi delle scene piene (fase 7b rivista: l'attribuzione Servier usciva dal
    # bordo destro dentro una scena a tutto schermo, dove lo strato e pieno fino al
    # bordo e il controllo sui pixel non vede niente): si misurano con il font vero
    from .impagina import larghezza as _larg
    fuori_t = []
    for x in el:
        d = x.get('dati', {})
        if x['modello'] != 'anatomia':
            continue
        for t in d.get('etichette', []):
            if 'x' not in t:
                continue
            w = t.get('larghezza') or (_larg(t['testo'], t.get('peso', 700), t.get('corpo', 56)) if t.get('testo') else 0)
            if t['x'] < 96 or t['x'] + w > W_OUT - 96 or t.get('y', 100) < 54:
                fuori_t.append(f"«{(t.get('testo') or '')[:24]}» {t['x']}+{int(w)}")
        ap = d.get('attr_pos') or {}
        if d.get('attribuzione') and 'left' in ap:
            w = _larg(d['attribuzione'], 600, int(d.get('attr_corpo', 22)))
            if ap['left'] + w > W_OUT - 96:
                fuori_t.append(f"attribuzione {ap['left']}+{int(w)}")
            if ap.get('bottom', 60) < 58:          # il riquadro del testo comprende le discendenti
                fuori_t.append(f"attribuzione a {ap['bottom']} px dal fondo")
    esiti.append(('testi delle scene piene dentro il quadro (misurati)', ', '.join(fuori_t) or 'tutti', not fuori_t))
    # 2c-quater) attribuzione Servier (tappa 3, Riccardo): su OGNI grafica con un disegno
    # Servier, scene scure comprese, leggibile (almeno 18 px) e in una riga che entra
    senza = []
    for x in el:
        d = x.get('dati', {})
        if not (_servier(d.get('disegno')) or any(_servier(c.get('disegno')) for c in d.get('carte', []))):
            continue
        a = d.get('attribuzione')
        if not a or 'Servier' not in a or 'CC BY' not in a:
            senza.append(f"{x['modello']}: manca")
        elif d.get('attr_corpo', 22) < 18:
            senza.append(f"{x['modello']}: {d.get('attr_corpo')} px")
    if any(_servier(x.get('dati', {}).get('disegno')) or any(_servier(c.get('disegno')) for c in x.get('dati', {}).get('carte', []))
           for x in el):
        esiti.append(('attribuzione Servier su ogni disegno Servier (≥ 18 px)', ', '.join(senza) or 'presente', not senza))
    # 2d) nessun elemento sparito (fase 6c: il secondo telefono del 09 non compariva
    # piu e nessun controllo lo vedeva): mentre un elemento e a schermo (lontano
    # dall'entrata e dall'uscita) il suo strato non e mai vuoto
    for strato in ('davanti', 'dietro'):
        mov = cart / f"{strato}.mov"
        vivi = [(x['s'] + 0.5, x['e'] - 0.4) for x in el
                if x.get('strato', 'davanti') == strato and x['modello'] != 'etichetta' and x['e'] - x['s'] > 1.0]
        if not mov.exists() or not vivi:
            continue
        st = Strato(mov)
        vuoti = []
        for f in range(tempo.n):
            try:
                _, al = next(st)
            except StopIteration:
                break
            t = f / fps
            if any(a <= t < b for a, b in vivi) and float((al > 0.5).sum()) < 2000:
                vuoti.append(round(t, 2))
        esiti.append((f"strato {strato}: nessun elemento sparito mentre e a schermo",
                      f"{len(vuoti)} frame vuoti" + (f" da {vuoti[0]:.2f} s" if vuoti else ''), not vuoti))
    # 3) volto: copertura dello strato davanti nel riquadro della testa
    if (cart / 'davanti.mov').exists():
        pieni = [(x['s'], x['e']) for x in el if x.get('pieno')]
        mani_d = [(x['s'], x['e']) for x in el if x.get('mani_davanti')]
        st = Strato(cart / 'davanti.mov')
        peggio, dove, tot = 0.0, None, 0
        peggio_m, dove_m, tot_m = 0.0, None, 0
        for f in range(tempo.n):
            t = f / fps
            _, al = next(st)
            if any(s - 0.5 / P.fps <= t < e for s, e in pieni):
                continue
            if mani is not None and f % 2 == 0 and not any(s <= t < e for s, e in mani_d):
                for h in mani.al(f):
                    a0, b0, a1, b1 = [int(round(v)) for v in h['box']]
                    a0, b0, a1, b1 = max(0, a0 - 16), max(0, b0 - 16), min(W_OUT, a1 + 16), min(H_OUT, b1 + 16)
                    if a1 > a0 and b1 > b0:
                        c = float((al[b0:b1, a0:a1] > 0.5).mean())   # coperto davvero, non l'ombra
                        tot_m += 1
                        if c > peggio_m:
                            peggio_m, dove_m = c, t
            b = volto.box(t)
            if b is None:
                continue
            x0, y0, x1, y1 = [int(round(v)) for v in b]
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W_OUT, x1), min(H_OUT, y1)
            if x1 <= x0 or y1 <= y0:
                continue
            c = float((al[y0:y1, x0:x1] > 0.5).mean())
            tot += 1
            if c > peggio:
                peggio, dove = c, t
        if mani is not None:
            esiti.append(('mani mai coperte (strato davanti, fuori dagli stacchi pieni)',
                          f"copertura massima {peggio_m * 100:.1f}%" + (f" a {dove_m:.2f} s" if dove_m is not None else '')
                          + f" su {tot_m} mani", peggio_m <= 0.03))
        esiti.append(('volto mai coperto (strato davanti, fuori dagli stacchi pieni)',
                      f"copertura massima {peggio * 100:.1f}%" + (f" a {dove:.2f} s" if dove is not None else '')
                      + f" su {tot} frame", peggio <= 0.02))
    return esiti


# ------------------------------------------------------------------ controlli sulla pagina (tappa 3)
# I pezzi grafici: contenitori (la pillola, il fumetto, la card, il vetro, l'etichetta) e
# parole fuori da un contenitore. Le parole dentro un contenitore fanno parte di lui.
CONTENITORI = '.el-pill, .el-sotto, .fu, .cs, .fl-vetro, .fc, .an-et, .an-attr, .tt-voce, .v3-pezzo'
DENTRO = '.el-pill, .el-sotto, .fu, .cs, .fl-vetro, .fc, .an-et, .an-attr, .tt-voce, .sc-fondo, .v3-pezzo, .v3-fondo'
CSS_PEZZI = (
    "#scena *{visibility:hidden!important;filter:none!important;backdrop-filter:none!important}"
    ".msk>*,.msk>* *{visibility:visible!important;color:#f00!important;-webkit-text-fill-color:#f00!important;"
    "text-shadow:none!important;background:none!important}.msk>*{opacity:.5!important}"
    f":is({DENTRO}) .msk>*,:is({DENTRO}) .msk>* *{{visibility:hidden!important}}"
    f"{CONTENITORI.replace(', ', ',')}{{visibility:visible!important;background:rgba(255,0,0,.5)!important;"
    "background-image:none!important;border-color:transparent!important;box-shadow:none!important;"
    "color:transparent!important;-webkit-text-fill-color:transparent!important;text-shadow:none!important}"
    f":is({CONTENITORI}) *{{visibility:hidden!important}}")
CSS_APERTO = ".msk{overflow:visible!important}.an-attr,.cs-attr,.cs-tx{overflow:visible!important;text-overflow:clip!important}"
SOVRAPPOSTI_MAX = 300     # px (a frame) sopra i quali due pezzi si sovrappongono davvero (sotto: bordi antialias)
TAGLIATI_MAX = 80         # px diversi fra il testo con e senza maschere


def _variante(src, nome, css):
    d = src.parent / f"{src.name}-{nome}"
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir()
    os.symlink((src / 'assets').resolve(), d / 'assets')
    html = (src / 'index.html').read_text(encoding='utf-8')
    (d / 'index.html').write_text(html.replace('</style>', css + '\n</style>', 1), encoding='utf-8')
    return d


def _scatti(d, tempi):
    """fotografie della pagina agli istanti dati (HyperFrames snapshot, in locale) -> png in ordine"""
    from .inserti import HF, dimentica
    out = d / 'snap'
    r = subprocess.run([str(HF), 'snapshot', str(d), '--at', ','.join(f"{t:.3f}" for t in tempi), '--no-end',
                        '-o', str(out)], env=ambiente_hf(), capture_output=True, text=True, timeout=1200)
    dimentica(d)
    if r.returncode:
        sys.exit(f"snapshot HyperFrames fallito ({d.name}):\n{(r.stderr or r.stdout)[-1200:]}")
    fs = sorted(out.glob('frame-*.png'), key=lambda f: int(f.name.split('-')[1]))
    if len(fs) != len(tempi):
        sys.exit(f"snapshot {d.name}: {len(fs)} fotografie invece di {len(tempi)}")
    return fs


def _alfa(f):
    return np.asarray(Image.open(f).convert('RGBA'))[..., 3]


def _tempi_fermi(el, n, fps):
    """istanti in cui nessun testo dello strato sta entrando o uscendo: li si confronta
    il testo con e senza maschere (durante un'entrata la maschera taglia apposta)"""
    ent, usc = [], []

    def scan(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    if k in ('t', 's', 'sotto_t', 'barra_t', 'etichetta_t', 'arrivo', 't_figura', 't_titolo'):
                        ent.append(v)
                    elif k in ('e', 'sotto_e'):
                        usc.append(v)
                else:
                    scan(v)
        elif isinstance(o, list):
            for v in o:
                scan(v)
    scan(el)
    ok = [f / fps for f in range(0, n, 2)
          if all(not (a - 0.12 <= f / fps <= a + 0.9) for a in ent) and all(not (b - 0.5 <= f / fps <= b + 0.12) for b in usc)]
    tempi = set()
    for x in el:
        c = [t for t in ok if x['s'] <= t < x['e']]
        if c:
            tempi.update({c[0], c[len(c) // 2], c[-1]})
    return sorted(tempi)


def controlli_pagina(spec, cart, tempo):
    """tappa 3, dalle note di Riccardo:
    - «lettere intere»: a entrata finita ogni testo e identico allo stesso testo disegnato
      senza maschere (6:44: la maschera tagliava la «g» di «già» e «toglie»);
    - «nessuna sovrapposizione»: due pezzi grafici non stanno mai uno sull'altro, ne
      dentro lo stesso elemento (4:12: «addominali» sopra «mangiare meglio fa bene»),
      ne fra elementi diversi o fra strato dietro e davanti: il primo esce del tutto
      prima che entri il secondo, oppure stanno in posti diversi.
    Si fotografa la pagina HyperFrames di ogni strato (ogni 2 frame per le sovrapposizioni)."""
    fps, n = tempo.fps, tempo.n
    esiti, tagliati, sovr, sovr_el = [], [], [], []
    passo = [f / fps for f in range(0, n, 2)]
    maschere = {}                       # (strato, k) -> [mask a meta risoluzione per istante]
    prove = cart / 'controlli-pagina'
    shutil.rmtree(prove, ignore_errors=True)
    prove.mkdir()
    for strato in ('dietro', 'davanti'):
        src = cart / f"hf-{strato}"
        el = [x for x in spec['elementi'] if x.get('strato', 'davanti') == strato]
        if not el or not src.is_dir():
            continue
        # lettere intere
        tf = _tempi_fermi(el, n, fps)
        if tf:
            a_ = _scatti(_variante(src, 'normale', ''), tf)
            b_ = _scatti(_variante(src, 'aperto', CSS_APERTO), tf)
            for t, fa, fb in zip(tf, a_, b_):
                A = np.asarray(Image.open(fa).convert('RGBA'), np.int16)
                B = np.asarray(Image.open(fb).convert('RGBA'), np.int16)
                dm = np.abs(A - B).max(-1) > 40
                k = int(dm.sum())
                if k > TAGLIATI_MAX:
                    ys, xs = np.nonzero(dm)
                    tagliati.append(f"{strato} {t:.2f} s: {k} px a x {xs.min()}-{xs.max()}, y {ys.min()}-{ys.max()}")
                    Image.fromarray((dm * 255).astype(np.uint8)).save(prove / f"lettere-{strato}-{t:05.2f}.png")
        # pezzi dello stesso strato uno sull'altro (ogni pezzo al 50%: dove sono due, l'alfa sale)
        fs = _scatti(_variante(src, 'pezzi', CSS_PEZZI), passo)
        peggio = (0, None)
        for t, f in zip(passo, fs):
            k = int((_alfa(f) > 160).sum())
            if k > peggio[0]:
                peggio = (k, t)
            if k > SOVRAPPOSTI_MAX and len(sovr) < 6:
                ys, xs = np.nonzero(_alfa(f) > 160)
                sovr.append(f"{strato} {t:.2f} s: {k} px a x {xs.min()}-{xs.max()}, y {ys.min()}-{ys.max()}")
                Image.fromarray(np.asarray(Image.open(f).convert('RGBA'))).save(prove / f"pezzi-{strato}-{t:05.2f}.png")
        # un elemento alla volta, per le sovrapposizioni fra elementi (anche fra i due strati)
        if len(spec['elementi']) > 1:
            for k, x in enumerate(el):
                css = f'#scena>.el:not([data-k="{k}"]){{opacity:0!important}}'
                fs = _scatti(_variante(src, f"el{k}", css), passo)
                maschere[(strato, k, x['modello'])] = [np.asarray(Image.fromarray(_alfa(f)).reduce(2)) > 128 for f in fs]
        for v in src.parent.glob(f"{src.name}-*"):
            shutil.rmtree(v, ignore_errors=True)
    chiavi = list(maschere)
    for i in range(len(chiavi)):
        for j in range(i + 1, len(chiavi)):
            for t, a, b in zip(passo, maschere[chiavi[i]], maschere[chiavi[j]]):
                k = int((a & b).sum()) * 4
                if k > SOVRAPPOSTI_MAX:
                    sovr_el.append(f"{chiavi[i][2]} ({chiavi[i][0]}) e {chiavi[j][2]} ({chiavi[j][0]}) a {t:.2f} s: {k} px")
                    break
    if not any(prove.iterdir()):
        prove.rmdir()
    esiti.append(('lettere intere: a entrata finita ogni testo come senza maschere',
                  '; '.join(tagliati[:4]) or 'nessuna differenza', not tagliati))
    esiti.append(('nessuna sovrapposizione fra i pezzi di uno strato (ogni 2 frame)',
                  '; '.join(sovr[:4]) or 'nessuna', not sovr))
    if maschere:
        esiti.append(('nessuna sovrapposizione fra elementi (anche dietro/davanti)', '; '.join(sovr_el[:4]) or 'nessuna',
                      not sovr_el))
    return esiti


# ------------------------------------------------------------------ condizioni del catalogo (fase 7c)
ZONA_OCCUPATA_MAX = 0.10     # frazione di pixel occupati (mani, oggetti) sotto un elemento a «zona libera»
TEMPI_DETTI = re.compile(r"\b(sera|sere|notte|notti|giorn\w*|settiman\w*|mes[ei]|ann[oi]|or[ae]|minut\w*|second\w*|ieri|oggi|domani"
                         r"|mattin\w*|pomeriggio|ogni|sempre|volt[ae]|quando|dopo|prima)\b", re.I)


def _occupati(rgb):
    """pixel di oggetti: saturi e chiari (modellini rossi e gialli) o bianchi (plastica). Il legno della
    scrivania (bruno, poco chiaro) non conta; le mani si misurano con Vision a parte"""
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = np.maximum(np.maximum(r, g), b), np.minimum(np.minimum(r, g), b)
    sat = (mx - mn) / np.maximum(mx, 1)
    return ((sat > 0.55) & (mx > 150)) | (mn > 200)


def condizioni(P, spec, tempo, cart):
    """le condizioni dei modelli del catalogo, misurate (fase 7c, Riccardo 01/11/2026):
    - zona_libera (connettore, riga di icone): sotto l'elemento niente mani, oggetti o modellini;
    - vetro_zona_ricca (vetro con piu luce): il vetro sta davanti a una zona chiara o ricca;
    - tempo_detto (linea del tempo): lui dice un tempo o una durata mentre l'elemento e a schermo."""
    from . import catalogo as CAT
    cat = CAT.per_id()
    fps, esiti = P.fps, []
    for x in spec['elementi']:
        if x.get('modello') == 'etichetta':
            continue
        cond = cat.get(CAT.identifica(x), {}).get('condizioni', [])
        if 'zona_libera' in cond and (cart / 'davanti.mov').exists():
            from .impagina import Mani as _Mani
            mani = _Mani(cart, tempo.n)
            st, peggio, quando = Strato(cart / 'davanti.mov'), 0.0, None
            for f in range(tempo.n):
                try:
                    _, al = next(st)
                except StopIteration:
                    break
                t = f / fps
                if f % 5 or not (x['s'] + 0.6 <= t < x['e'] - 0.3):
                    continue
                m = al[..., 0] > 0.3
                if m.sum() < 500:
                    continue
                ys, xs = np.nonzero(m)
                y0, y1, x0, x1 = max(0, ys.min() - 16), min(H_OUT, ys.max() + 16), max(0, xs.min() - 16), min(W_OUT, xs.max() + 16)
                rgb = np.asarray(Image.open(cart / 'piatto' / f"f{f:06d}.png").convert('RGB'), np.float32)[y0:y1, x0:x1]
                occ = _occupati(rgb)
                for h in mani.al(f):          # le mani di Vision dentro la zona dell'elemento
                    a0, b0, a1, b1 = [int(round(v)) for v in h['box']]
                    occ[max(0, b0 - y0):max(0, b1 - y0), max(0, a0 - x0):max(0, a1 - x0)] = True
                q = float(occ.mean())
                if q > peggio:
                    peggio, quando = q, t
            esiti.append((f"zona libera sotto «{x['modello']}» (mani, oggetti: al massimo {int(ZONA_OCCUPATA_MAX * 100)}%)",
                          f"massimo {peggio * 100:.1f}%" + (f" a {quando:.2f} s" if quando is not None else ''), peggio <= ZONA_OCCUPATA_MAX))
        if 'vetro_zona_ricca' in cond:
            v = next((p for p in spec.get('piatto', []) if p['tipo'] == 'vetro'), None)
            if v:
                f = int(round((v['s'] + v['e']) / 2 * fps))
                rgb = np.asarray(Image.open(cart / 'piatto' / f"f{min(f, tempo.n - 1):06d}.png").convert('RGB'), np.float32)
                reg = rgb[int(v['y']):int(v['y'] + v['altezza']), int(v['x']):int(v['x'] + v['larghezza'])]
                lum = reg @ np.array([0.2126, 0.7152, 0.0722], np.float32)
                ok = lum.mean() > 80 or lum.std() > 40
                esiti.append(("vetro davanti a una zona chiara o ricca (luminanza media > 80 o dettaglio > 40)",
                              f"media {lum.mean():.0f}, dettaglio {lum.std():.0f}", ok))
        if 'tempo_detto' in cond:
            from .grafica.piano import parole
            a, b = tempo.montato(x['s']) - 1.0, tempo.montato(x['e'])
            dette = ' '.join(w['t'] for w in parole(P, P.regia()) if a <= w['s'] < b)
            trov = TEMPI_DETTI.findall(dette) + re.findall(r'\b\d+\b', dette)
            esiti.append(("la linea del tempo ha un tempo o una durata detti", ', '.join(sorted(set(trov)))[:60] or 'nessuno',
                          bool(TEMPI_DETTI.search(dette))))
    return esiti


def fuori_quadro(mov, esenti, fps, n, b=3):
    """frame in cui lo strato (alfa > 0,5) tocca il bordo del quadro: qualcosa e tagliato"""
    st = Strato(mov)
    k_fr, peggio, primo = 0, 0, None
    for f in range(n):
        try:
            _, al = next(st)
        except StopIteration:
            break
        t = f / fps
        if any(a - 0.5 / fps <= t < e for a, e in esenti):   # mezzo frame: l'inizio del pezzo e arrotondato al frame
            continue
        m = al[..., 0] > 0.5
        k = int(m[:b].sum() + m[-b:].sum() + m[b:-b, :b].sum() + m[b:-b, -b:].sum())
        if k:
            k_fr += 1
            peggio = max(peggio, k)
            primo = t if primo is None else primo
    return k_fr, peggio, primo


def fuori_zona(mov, pieni, fps, n, sx=96, sy=54):
    """pixel dello strato (alfa > 0,5) fuori dalla zona sicura: il massimo per frame"""
    st = Strato(mov)
    peggio, quando = 0, None
    for f in range(n):
        try:
            _, al = next(st)
        except StopIteration:
            break
        t = f / fps
        if any(a - 0.5 / fps <= t < b for a, b in pieni):
            continue
        m = al[..., 0] > 0.5
        k = int(m[:sy].sum() + m[-sy:].sum() + m[sy:-sy, :sx].sum() + m[sy:-sy, -sx:].sum())
        if k > peggio:
            peggio, quando = k, t
    return peggio, quando


def striscia(video, t0, out_png, P, env_tempo, titolo, passo=2, prima=4, dopo=26, ancore=(), volto=None):
    """fotogrammi dell'entrata (uno ogni `passo` frame) con frame, scarto dall'ancora,
    e sotto l'inviluppo della voce con le parole e gli istanti dei fotogrammi"""
    fps = P.fps
    f0 = int(round(t0 * fps))
    frames = list(range(f0 - prima, f0 + dopo + 1, passo))
    tw, th = 384, 216
    cols = 6
    rows = math.ceil(len(frames) / cols)
    # tutto il pezzo decodificato in piccolo, poi i frame per indice (select a volte ne perde uno)
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-vf', f"scale={tw}:{th}", '-f', 'rawvideo',
                        '-pix_fmt', 'rgb24', '-'], capture_output=True)
    tutti = np.frombuffer(r.stdout, np.uint8).reshape(-1, th, tw, 3)
    fnt = ImageFont.truetype(str(FONT), 18)
    fnt.set_variation_by_axes([600])
    fnt2 = ImageFont.truetype(str(FONT), 22)
    fnt2.set_variation_by_axes([700])
    env_h = 150
    sheet = Image.new('RGB', (cols * tw, rows * (th + 26) + env_h + 50), (0, 26, 61))
    d = ImageDraw.Draw(sheet)
    d.text((10, 8), titolo, font=fnt2, fill=(244, 244, 244))
    for k, f in enumerate(frames):
        x, y = (k % cols) * tw, 40 + (k // cols) * (th + 26)
        if 0 <= f < len(tutti):
            im = Image.fromarray(tutti[f])
            if volto is not None:
                b = volto.box(f / fps)
                if b:
                    dd = ImageDraw.Draw(im)
                    s = tw / W_OUT
                    dd.rectangle([b[0] * s, b[1] * s, b[2] * s, b[3] * s], outline=(255, 80, 80))
            sheet.paste(im, (x, y))
        dfr = f - f0
        d.text((x + 6, y + th + 2), f"f{f}  {f / fps:.2f}s  {'+' if dfr >= 0 else ''}{dfr} fr", font=fnt,
               fill=(114, 250, 147) if dfr == 0 else (244, 244, 244))
    # inviluppo della voce sotto
    env, tmap = env_tempo
    y0 = 40 + rows * (th + 26) + 8
    W = cols * tw
    ta, tb = frames[0] / fps, frames[-1] / fps
    pts = []
    for i in range(W):
        tt = ta + (tb - ta) * i / (W - 1)
        tm = tmap(tt)
        j = int(tm / 0.005)
        v = env[j] if 0 <= j < len(env) else -80
        pts.append((i, y0 + env_h - (min(max(v, -60), 0) + 60) / 60 * env_h))
    d.line(pts, fill=(244, 244, 244), width=2)
    for f in frames:
        xi = (f / fps - ta) / (tb - ta) * (W - 1)
        d.line([(xi, y0), (xi, y0 + 8)], fill=(150, 170, 190))
    xi = (t0 - ta) / (tb - ta) * (W - 1)
    d.line([(xi, y0), (xi, y0 + env_h)], fill=(114, 250, 147), width=2)
    for nome, ta_ in ancore:
        if ta <= ta_ <= tb:
            xi = (ta_ - ta) / (tb - ta) * (W - 1)
            d.line([(xi, y0 + env_h - 30), (xi, y0 + env_h)], fill=(255, 200, 80), width=2)
            d.text((xi + 3, y0 + env_h + 4), nome, font=fnt, fill=(255, 200, 80))
    sheet.save(out_png, quality=88)
    return out_png


# ------------------------------------------------------------------ suoni dei modelli
def suoni_camera(cam, tempo):
    """un suono su ogni movimento di camera: zoom rapido = fruscio corto + colpo
    leggero all'arrivo; taglio con cambio di taglio = fruscio corto"""
    ev = []
    for m in cam.mosse:
        if m.get('muto'):
            continue
        if m.get('taglio'):
            continue
        if m['dur'] <= 0.6 and m.get('z'):
            ev.append({'nome': 'swish', 't': m['t'] + 0.04, 'db': -15, 'perche': 'zoom rapido'})
            if m.get('colpo', True):
                ev.append({'nome': 'impact', 't': m['t'] + 0.06, 'db': -19, 'kw': {'peso': 0.6},
                           'perche': 'arrivo dello zoom'})
    return ev


def suoni_piatto(spec):
    ev = []
    for fx in spec.get('piatto', []):
        if fx['tipo'] == 'spinta':
            ev.append({'nome': 'whoosh', 't': fx['t'], 'db': -11, 'kw': {'direzione': -1 if fx.get('dir', 'sx') == 'sx' else 1},
                       'perche': 'transizione a spinta'})
    return ev


# ------------------------------------------------------------------ un pezzo
def costruisci(P, spec, uscita, anc, rifai=False):
    """un modello del campionario: spec risolta -> mp4 + controlli"""
    t_0 = time.time()
    tempo = Tempo(P, spec['pezzi'])
    spec = risolvi(spec, anc, tempo)
    spec['_frames'], spec['_fps'] = tempo.n, P.fps
    for x in spec['elementi']:
        if 'e' not in x:
            sys.exit(f"{spec['nome']}: elemento {x['modello']} senza fine")
    espandi(spec)
    cam = Camera(spec.get('camera', {}), tempo.durata)
    # la camera di ogni frame va anche alla pagina HyperFrames (parallasse)
    spec['_cam'] = [[round(v, 2) for v in cam.box(f / P.fps)[:3]] for f in range(tempo.n)]
    # testo sul busto: mai piu in alto del punto piu basso della testa (Vision, con
    # la barba e un margine) in tutta la durata dell'elemento -> il volto non si copre
    volto_ = Volto(P, tempo, cam)
    for x in spec['elementi']:
        d = x.get('dati', {})
        if x['modello'] == 'schermata':
            adatta_schermata(x)
        if x['modello'] == 'schermata' and d.get('centra_prima'):
            apertura_schermata(x, d.get('centra_prima'))
        if x['modello'] in ('cta', 'lista_attesa') and 'larghezza' in d:
            adatta_colonna(x)
        if x['modello'] == 'etichette_luce':
            adatta_etichette(x)
        if x['modello'] == 'titolo_dietro' and d.get('larghezza_max'):
            # corpo misurato sul font vero (900, tracking -0,035 em, maiuscole):
            # la riga piu lunga sta nella larghezza data
            from .impagina import larghezza as _larg
            c = d.get('corpo_max', 240)
            # fase 7c: forma del sito (minuscolo con il punto, -0,045 em) o maiuscolo (variante)
            from .impagina import forma_titolo
            righe_, tr_, _ = forma_titolo(d)
            while c > 60 and max(_larg(r, 900, c, tr_) for r in righe_) > d['larghezza_max']:
                c -= 2
            d['corpo'] = c
        if x['modello'] == 'parole' and d.get('battute'):
            piazza_battute(x, volto_, P.fps)
        if d.get('sotto_volto') and 'y' in d:
            fondi = [b[3] for f in range(int(x['s'] * P.fps), int(x['e'] * P.fps) + 1)
                     for b in [volto_.box(f / P.fps)] if b]
            if fondi:
                d['y_spec'] = d['y']
                d['y'] = int(max(d['y'], max(fondi) + d.get('margine_volto', 24)))
    chiave = hashlib.sha1(json.dumps([spec, VERSIONE], sort_keys=True).encode()).hexdigest()[:10]
    cart = LAVORO / spec.get('cartella', f"{spec['n']:02d}-{spec['nome']}")
    cart.mkdir(parents=True, exist_ok=True)
    # 1. piatto (cache sulla parte che lo riguarda)
    chiave_p = hashlib.sha1(json.dumps([spec['pezzi'], [[o, k, round(s, 3)] for o, k, s in tempo.corse()],
                                        spec.get('camera'), spec.get('look'),
                                        [x for x in spec.get('piatto', []) if x['tipo'] == 'spinta'],
                                        VERSIONE_PIATTO]).encode()).hexdigest()[:10]
    segno = cart / 'piatto.chiave'
    if rifai or not segno.exists() or segno.read_text() != chiave_p:
        shutil.rmtree(cart / 'piatto', ignore_errors=True)
        shutil.rmtree(cart / 'sagome', ignore_errors=True)
        piatto(P, tempo, cam, spec, cart / 'piatto')
        segno.write_text(chiave_p)
    t_p = time.time() - t_0
    # 2. sagome se servono
    serve = any(x.get('strato') == 'dietro' or x.get('mani') or x.get('libero') for x in spec['elementi']) or \
        any(fx['tipo'] in ('sfoca_sfondo', 'luce', 'fuoco') or
            (fx['tipo'] == 'scurisci' and fx.get('dove', 'sfondo') == 'sfondo')
            for fx in spec.get('piatto', []))
    if serve and not (cart / 'sagome').is_dir():
        sagome(cart / 'piatto', cart / 'sagome')
    # mani (Vision) se un elemento deve partire dalla mano o non coprirla
    mani_ = None
    if any(x.get('mani') for x in spec['elementi']):
        mani_ = Mani(cart, tempo.n)
    # impaginazione misurata sulle sagome vere (numero dietro: chi copre cosa)
    for x in spec['elementi']:
        if x['modello'] == 'numero_dietro' and x['dati'].get('auto', True):
            piazza_numero(x, Sagome(cart / 'sagome', tempo.n), P.fps)
        if x['modello'] == 'titolo_dietro' and x['dati'].get('auto'):
            from .impagina import piazza_titolo
            piazza_titolo(x, Sagome(cart / 'sagome', tempo.n), P.fps)
        if x['modello'] == 'card':
            misura_card(x)
            if mani_ is not None:
                piazza_card(x, mani_, volto_, Sagome(cart / 'sagome', tempo.n), P.fps)
        if x.get('mani') and mani_ is not None:
            lega_mani(x, mani_, P.fps)
    t_s = time.time() - t_0 - t_p
    # 3. strati
    materiali = prepara_materiali(P, spec, cart)
    for strato in ('dietro', 'davanti'):
        mov = cart / f"{strato}.mov"
        if not any(x.get('strato', 'davanti') == strato for x in spec['elementi']):
            if mov.exists():
                mov.unlink()
            continue
        d = strato_html(spec, strato, cart / f"hf-{strato}", materiali)
        # l'impronta tiene anche il motore della pagina (_scena.js non e dentro index.html)
        h = hashlib.sha1((d / 'index.html').read_bytes() + (SCENE / '_scena.js').read_bytes()
                         + json.dumps(sorted(materiali)).encode()).hexdigest()[:10]
        seg = cart / f"{strato}.chiave"
        if rifai or not mov.exists() or not seg.exists() or seg.read_text() != h:
            render_strato(d, mov, P.fps_str, tempo.n)
            seg.write_text(h)
    t_h = time.time() - t_0 - t_p - t_s
    # 3b. controlli sulla pagina (tappa 3): lettere intere, nessuna sovrapposizione
    esiti_pagina = controlli_pagina(spec, cart, tempo)
    t_h = time.time() - t_0 - t_p - t_s
    # 5. suono (prima della composizione: l'encoder lo prende insieme ai frame)
    eventi = suoni_camera(cam, tempo) + suoni_piatto(spec) + _s_finestra(spec) + list(spec.get('suoni', []))
    for x in spec['elementi']:
        eventi += SUONI_MODELLI.get(x['modello'], lambda x: [])(x)
    musica = spec.get('musica')
    wav = cart / 'mix.wav'
    log, loud = mix(P, tempo, eventi, wav, musica)
    # 4. composizione
    uscita.parent.mkdir(parents=True, exist_ok=True)
    componi(P, spec, tempo, cart, uscita, wav, mani_)
    t_c = time.time() - t_0
    volto = Volto(P, tempo, cam)
    esiti = controlla(P, spec, tempo, cart, volto, mani_) + esiti_pagina + condizioni(P, spec, tempo, cart)
    if MISURE.get('mani_serie'):
        # solo i frame con la scritta intera (in entrata e in uscita le lettere sono
        # dentro le maschere: poca area, percentuale gonfiata)
        amax = max(a for _, a, _ in MISURE['mani_serie'])
        c, _, q = max((x for x in MISURE['mani_serie'] if x[1] >= 0.6 * amax), key=lambda x: x[0])
        esiti.append(('mani davanti alla scritta: coprono al massimo il 20% delle lettere',
                      f"massimo {c * 100:.1f}% a {q:.2f} s", c <= 0.20))
    rapporto = {'n': spec['n'], 'nome': spec['nome'], 'file': str(uscita.relative_to(AGENTE)),
                'durata': round(tempo.durata, 3), 'frame': tempo.n, 'pezzi_montato': spec['pezzi'],
                'tagli': [round(t, 3) for t in tempo.tagli()], 'ancore': anc.usate[:],
                'suoni': log, 'loudness': loud, 'eventi': eventi,
                'controlli': [{'cosa': a, 'valore': b, 'ok': c} for a, b, c in esiti],
                'misure': [{'modello': x['modello'], **{k: v for k, v in x['dati'].items() if k.startswith('_')}}
                           for x in spec['elementi'] if any(k.startswith('_') for k in x.get('dati', {}))],
                'tempi_s': {'piatto': round(t_p, 1), 'sagome': round(t_s, 1), 'hyperframes': round(t_h, 1),
                            'totale': round(t_c, 1)}}
    return rapporto, tempo, cam, volto, spec


VERSIONE = 2
VERSIONE_PIATTO = 3


def espandi(spec):
    """le regole "in tutti" della fase 6b, dagli elementi alla scena:
    - `fuoco` (true o {raggio, scuro}): mentre l'elemento e a schermo lo sfondo si
      sfoca e scende un poco (la messa a fuoco va sulla grafica);
    - `colpo` (true o {t, a}): un piccolo punch-in della camera insieme al suono
      d'impatto, all'arrivo dell'elemento (o a `t`)."""
    cam = spec.setdefault('camera', {})
    for x in spec['elementi']:
        f = x.get('fuoco')
        if f:
            f = f if isinstance(f, dict) else {}
            spec.setdefault('piatto', []).append({
                'tipo': 'fuoco', 's': f.get('s', x['s']), 'e': f.get('e', x['e']), 'raggio': f.get('raggio', 7),
                'scuro': f.get('scuro', 0.22), 'scuro_persona': f.get('scuro_persona', 0.06),
                'rampa': f.get('rampa', 0.35)})
        c = x.get('colpo')
        if c:
            lista = c if isinstance(c, list) else [c]
            for c in lista:
                c = c if isinstance(c, dict) else {}
                t = c.get('t', x['s'] + c.get('d', 0.0))
                cam.setdefault('colpi', []).append({'t': t, 'a': c.get('a', 0.045)})
                if c.get('suono', 'impact'):
                    spec.setdefault('suoni', []).append({
                        'nome': c.get('suono', 'impact'), 't': t, 'db': c.get('db', -14),
                        'perche': f"colpo di camera ({x['modello']})"})


def prepara_materiali(P, spec, cart):
    """immagini degli elementi: render dell'app scontornati, foto prima/dopo con i
    punti posturali di Vision. Restano dentro il laboratorio (.lavoro)."""
    from .inserti import scontorna_render, _foto
    mat = {}
    for x in spec['elementi']:
        d = x.get('dati', {})
        for k, s in enumerate(d.get('schermate', [])):
            if s.get('genera') == 'foto_sagoma':
                # «foto di lato» disegnata con la sagoma posturale: nessuna persona vera
                from .anatomia import foto_sagoma
                nome = f"foto-sagoma-{int(bool(s.get('anelli')))}.png"
                dst = cart / 'mat' / nome
                dst.parent.mkdir(exist_ok=True)
                foto_sagoma(dst, anelli=bool(s.get('anelli')))
                s['src'] = f"assets/{nome}"
                s['w'], s['h'] = Image.open(dst).size
                mat[nome] = dst
                continue
            src = P.materiale(s['file'])
            if src is None:
                sys.exit(f"materiale non trovato: {s['file']}")
            if src.name in set(P.regia().get('materiali_vietati', [])):
                sys.exit(f"{src.name} e fra i materiali vietati in regia")
            zone = s.get('sfoca') or []
            nome = f"app-{src.stem}" + (f"-s{hashlib.sha1(json.dumps(zone).encode()).hexdigest()[:6]}" if zone else '') + ".png"
            dst = cart / 'mat' / nome
            dst.parent.mkdir(exist_ok=True)
            if not dst.exists():
                if zone:
                    # fase 7c (Riccardo 02/11: tutte le foto dell'app): righe sfocate dove la schermata mostra un nome
                    # o dati di una persona, importi o frasi sulla salute (`sfoca`: [[x0, y0, x1, y1], ...] in px del file)
                    im = Image.open(src).convert('RGB')
                    for x0, y0, x1, y1 in zone:
                        reg = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(14))
                        im.paste(reg, (x0, y0))
                    tmp = cart / 'mat' / f"sfocata-{src.stem}.png"
                    im.save(tmp)
                    scontorna_render(tmp, dst, titolo=s.get('titolo', True), tieni_bianco=s.get('tieni_bianco', False))
                    tmp.unlink()
                else:
                    scontorna_render(src, dst, titolo=s.get('titolo', True), tieni_bianco=s.get('tieni_bianco', False))
            s['src'] = f"assets/{nome}"
            s['w'], s['h'] = Image.open(dst).size
            mat[nome] = dst
        if x['modello'] == 'anatomia':
            # disegno Servier ricolorato nel brand (il file in libreria resta l'originale)
            from .anatomia import ricolora, ATTRIBUZIONE
            img, sc = ricolora(d['disegno'], d['alto'], d.get('taglio'), d.get('sfuma', 140), d.get('ritaglio'),
                               d.get('modo', 'ossa'), d.get('sfuma_bordi', 0))
            nome = f"an-{hashlib.sha1(json.dumps([d['disegno'], d['alto'], d.get('taglio'), d.get('sfuma', 140), d.get('ritaglio'), d.get('modo'), d.get('sfuma_bordi', 0)]).encode()).hexdigest()[:8]}.png"
            dst = cart / 'mat' / nome
            dst.parent.mkdir(exist_ok=True)
            img.save(dst)
            orig = Image.open(LIBRERIA / 'anatomia' / d['disegno']).size
            rt = d.get('ritaglio') or [0, 0, orig[0], orig[1]]
            d.update({'src': f"assets/{nome}", 'w': img.width, 'h': img.height, 'scala': sc,
                      'vx': rt[0], 'vy': rt[1], 'vw': rt[2] - rt[0],
                      'vh': (d.get('taglio') - rt[1]) if d.get('taglio') else rt[3] - rt[1]})
            # tappa 3 (Riccardo): l'attribuzione Servier compare su OGNI grafica con un disegno
            # Servier, scene scure comprese; la lunga se entra in una riga, se no la breve
            if _servier(d.get('disegno')) or d.get('attribuzione'):
                spazio = (d['pannello']['larghezza'] - 44) if d.get('pannello') and d['pannello'].get('larghezza', W_OUT) < W_OUT \
                    else W_OUT - 2 * (d.get('attr_pos') or {}).get('left', 96)
                corpo = 19 if d.get('pannello') and d['pannello'].get('larghezza', W_OUT) < W_OUT else 22
                d['attr_corpo'] = corpo
                # a 22 px le discendenti scendevano sotto i 54 px del margine basso (meccanismo, bottom 46)
                if d.get('attr_pos') and 'bottom' in d['attr_pos']:
                    d['attr_pos'] = dict(d['attr_pos'], bottom=max(d['attr_pos']['bottom'], 60))
                d['attribuzione'] = _attribuzione(spazio, corpo)
            mat[nome] = dst
        if x['modello'] == 'card_spessore':
            # ritagli di disegni Servier dentro le card (ricolorati, mai deformati)
            from .anatomia import ricolora, ATTRIBUZIONE
            for c in d.get('carte', []):
                if not c.get('disegno'):
                    continue
                img, sc = ricolora(c['disegno'], c['alto'], None, 140, c.get('ritaglio'), c.get('modo', 'ossa'))
                nome = f"cs-{hashlib.sha1(json.dumps([c['disegno'], c['alto'], c.get('ritaglio'), c.get('modo')]).encode()).hexdigest()[:8]}.png"
                dst = cart / 'mat' / nome
                dst.parent.mkdir(exist_ok=True)
                img.save(dst)
                c.update({'src': f"assets/{nome}", 'w': img.width, 'h': img.height})
                mat[nome] = dst
            if any(_servier(c.get('disegno')) for c in d.get('carte', [])) or d.get('attribuzione'):
                d['attr_corpo'] = 18
                d['attribuzione'] = _attribuzione(d.get('larghezza', 672) - 44, 18)
        if x['modello'] == 'foto_card':
            # foto vera di un paziente: solo con il consenso nel catalogo, il viso
            # tagliato fuori (`ritaglio` in px originali, dopo la rotazione EXIF);
            # resta dentro il laboratorio (.lavoro) e la cronologia di HyperFrames si
            # cancella dopo il render (inserti.dimentica)
            from PIL import ImageOps
            src = P.materiale(d['foto'])
            if src is None or src.parent.name != 'prima-dopo':
                sys.exit(f"foto_card: {d['foto']} non e in libreria/prima-dopo")
            _consenso(src)
            if d.get('confronta_con'):
                altra = P.materiale(d['confronta_con'])
                prima, dopo = (src, altra) if '_prima_' in src.name else (altra, src)
                _verifica_prima_dopo(prima, dopo)
            im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
            x0, y0, x1, y1 = d['ritaglio']
            im = im.crop((x0, y0, x1, y1))
            sc = max(d['larghezza'] / im.width, d['altezza'] / im.height)
            im = im.resize((int(round(im.width * sc)), int(round(im.height * sc))), Image.LANCZOS)
            nome = f"foto-{hashlib.sha1(json.dumps([d['foto'], d['ritaglio'], d['larghezza'], d['altezza']]).encode()).hexdigest()[:8]}.jpg"
            dst = cart / 'mat' / nome
            dst.parent.mkdir(exist_ok=True)
            im.save(dst, quality=90)
            ox, oy = (d['larghezza'] - im.width) / 2, (d['altezza'] - im.height) / 2
            for a in d.get('anelli', []):
                # anelli in px originali -> px della card
                if 'ox' in a:
                    a.update({'cx': round((a.pop('ox') - x0) * sc + ox), 'cy': round((a.pop('oy') - y0) * sc + oy),
                              'rx': round(a.pop('orx') * sc), 'ry': round(a.pop('ory') * sc)})
            d.update({'src': f"assets/{nome}", 'w': im.width, 'h': im.height})
            mat[nome] = dst
        if x['modello'] == 'sagoma':
            from . import anatomia as A
            d.update({'profilo': A.PROFILO, 'testa': list(A.TESTA), 'naso': A.NASO, 'braccio': A.BRACCIO,
                      'bacino': [list(q) for q in A.LINEA_BACINO] if d.get('bacino', True) else None})
        if x['modello'] == 'confronto':
            from .visione import posa
            srcs = [P.materiale(d['foto_prima']), P.materiale(d['foto_dopo'])]
            if None in srcs:
                sys.exit("foto prima/dopo non trovate")
            _verifica_prima_dopo(srcs[0], srcs[1])
            punti = posa([str(s) for s in srcs])
            for chi, src in zip(('prima', 'dopo'), srcs):
                nome = f"pd-{chi}.jpg"
                dst = cart / 'mat' / nome
                dst.parent.mkdir(exist_ok=True)
                w, h = _foto(src, dst)
                from PIL import ImageOps
                ow, oh = ImageOps.exif_transpose(Image.open(src)).size
                pp = punti[str(src)]['punti']
                if not pp or any(q is None for q in pp):
                    sys.exit(f"Vision non trova tutti i punti posturali in {src.name}")
                d[chi] = {'src': f"assets/{nome}", 'w': w, 'h': h, 'ow': ow, 'oh': oh, 'punti': pp}
                mat[nome] = dst
    return mat


def _servier(nome):
    return bool(nome) and Path(str(nome)).name.lower().startswith('servier')


def _attribuzione(spazio, corpo):
    """il testo dell'attribuzione Servier che entra in `spazio` px in una riga"""
    from .anatomia import ATTRIBUZIONE, ATTRIBUZIONE_BREVE
    from .impagina import larghezza as _larg
    for testo in (ATTRIBUZIONE, ATTRIBUZIONE_BREVE):
        if _larg(testo, 600, corpo) * 1.07 + 8 <= spazio:
            return testo
    return ATTRIBUZIONE_BREVE


def adatta_etichette(x):
    """etichette_luce: quante righe fa il «sotto» (fase 7b, 4:12: «mangiare meglio fa bene»
    andava a capo, il modello contava una riga e la pillola dopo ci finiva sopra)"""
    from .impagina import larghezza as _larg
    d = x['dati']
    corpo = d.get('corpo', 56)
    c2 = d.get('corpo_sotto') or round(corpo * 0.62)
    larg = d.get('larghezza_sotto', 700)
    for v in d.get('voci', []):
        if not v.get('sotto'):
            continue
        righe, cur = 1, ''
        for w in v['sotto'].split():
            prova = (cur + ' ' + w).strip()
            if cur and _larg(prova, 600, c2) * 1.07 + 4 > larg:
                righe, cur = righe + 1, w
            else:
                cur = prova
        v['righe_sotto'] = max(righe, v.get('righe_sotto', 1))


def _consenso(src):
    """una foto di paziente si usa solo con il consenso scritto segnato nel catalogo"""
    import re as _re
    cod = src.name.split('_')[0]
    cat = (LIBRERIA / 'catalogo.md').read_text(encoding='utf-8')
    riga = next((r for r in cat.splitlines() if r.startswith(f"| {cod} |")), None)
    celle = [c.strip() for c in riga.split('|')] if riga else []
    if len(celle) < 4 or not _re.match(r"s[iì]\b", celle[3], _re.I):
        sys.exit(f"{src.name}: nessun consenso scritto nel catalogo per {cod}: la foto non si usa")


def _verifica_prima_dopo(prima, dopo):
    """prima e dopo si decidono dalla data di scatto (EXIF), mai dall'aspetto"""
    def dto(p):
        ex = Image.open(p).getexif().get_ifd(0x8769)
        return ex.get(36867), ex.get(37521) or '0'
    a, b = dto(prima), dto(dopo)
    if not a[0] or not b[0]:
        sys.exit(f"data di scatto mancante in {prima.name} o {dopo.name}: chiedere a Riccardo")
    if (a[0], a[1]) >= (b[0], b[1]):
        sys.exit(f"{prima.name} ({a[0]}) non e precedente a {dopo.name} ({b[0]}): chiedere a Riccardo")


# suoni dei modelli: si leggono dai dati dell'elemento (tempi gia nel pezzo)
def _s_parole(x):
    d, ev = x['dati'], []
    if d.get('battute'):
        for b in d['battute']:
            for k, p in enumerate(b['parole']):
                ev.append({'nome': 'swish', 't': p['t'], 'db': -18 if k == 0 else -20, 'perche': f"sale «{p['testo']}»"})
            ev.append({'nome': 'swish', 't': b['e'] - 0.2, 'db': -24, 'perche': 'la battuta esce'})
        return ev
    for k, w in enumerate(p for r in d['righe'] for p in r):
        if w.get('chiave'):
            ev.append({'nome': 'pop', 't': w['t'], 'db': -14, 'perche': f"parola chiave «{w['testo']}»"})
            ev.append({'nome': 'impact', 't': w['t'], 'db': -20, 'kw': {'peso': 0.5}, 'perche': 'parola chiave'})
        else:
            ev.append({'nome': 'swish', 't': w['t'], 'db': -21, 'perche': f"parola «{w['testo']}»"})
    return ev


def _s_numero(x):
    d = x['dati']
    ev = [{'nome': 'riser', 't': d['arrivo'] - 0.02, 'db': -18, 'kw': {'dur': 0.6}, 'allinea': 'picco',
           'perche': 'il numero sale'},
          {'nome': 'impact', 't': d['arrivo'], 'db': -12, 'perche': 'il numero arriva sulla parola'}]
    return ev


def _s_schermata(x):
    d = x['dati']
    ev = [{'nome': 'whoosh', 't': x['s'] + 0.05, 'db': -12, 'perche': 'entra la schermata'}]
    for w in d.get('parole', []):
        ev.append({'nome': 'pop' if w.get('chiave') else 'click', 't': w['t'], 'db': -15 if w.get('chiave') else -19,
                   'perche': f"parola «{w['testo']}»"})
    ev.append({'nome': 'swish', 't': x['e'] - 0.05, 'db': -16, 'perche': 'esce la schermata'})
    return ev


def _s_card(x):
    ev = []
    for c in x['dati']['card']:
        dirz = 1 if (c.get('zona') or c.get('lato')) == 'dx' else -1
        nome = c.get('titolo') or c.get('testo')
        if c.get('mano'):
            ev.append({'nome': 'tick', 't': c['s'] - 2 / 25, 'db': -22, 'pan': 0.3 * dirz, 'perche': f"filo dalla mano («{nome}»)"})
        ev.append({'nome': 'whoosh', 't': c['s'] + 0.06, 'db': -17, 'kw': {'direzione': dirz, 'dur': 0.36},
                   'pan': 0.4 * dirz, 'perche': f"entra «{nome}»"})
        ev.append({'nome': 'pop', 't': c['s'] + 0.22, 'db': -16, 'pan': 0.3 * dirz, 'perche': 'la card si posa'})
        if c.get('sotto_t') is not None:
            ev.append({'nome': 'click', 't': c['sotto_t'], 'db': -21, 'pan': 0.3 * dirz, 'perche': 'arriva il sottotitolo'})
    return ev


def _s_telefono(x):
    d = x['dati']
    ev = [{'nome': 'whoosh', 't': x['s'] + 0.10, 'db': -11, 'kw': {'direzione': -1}, 'pan': 0.4,
           'perche': 'entra il telefono'},
          {'nome': 'thump', 't': x['s'] + 0.42, 'db': -15, 'pan': 0.4, 'perche': 'il telefono si posa'}]
    for s in d['schermate'][1:]:
        if d.get('cambio') == 'dissolvenza':
            ev.append({'nome': 'tick', 't': s['t'] + 0.1, 'db': -18, 'pan': 0.4, 'perche': 'cambia la schermata'})
            continue
        ev.append({'nome': 'whoosh', 't': s['t'] + 0.05, 'db': -15, 'kw': {'direzione': -1, 'dur': 0.34}, 'pan': 0.4,
                   'perche': 'scorre la schermata'})
        ev.append({'nome': 'click', 't': s['t'] + 0.22, 'db': -18, 'pan': 0.4, 'perche': 'la schermata si ferma'})
    return ev


def _s_confronto(x):
    d = x['dati']
    return [{'nome': 'whoosh', 't': x['s'] + 0.02, 'db': -12, 'perche': 'entra il prima/dopo'},
            {'nome': 'scan', 't': d['cursore']['t'] + d['cursore']['dur'] * 0.5, 'db': -16,
             'kw': {'dur': d['cursore']['dur'] + 0.2}, 'perche': 'il cursore scorre'},
            {'nome': 'tick', 't': d['linee']['t'] + 0.18, 'db': -18, 'perche': 'la linea si disegna'},
            {'nome': 'swish', 't': x['e'] - 0.04, 'db': -16, 'perche': 'esce'}]


def _s_cta(x):
    d = x['dati']
    ev = []
    for r in d['righe']:
        for p in r['parole']:
            ev.append({'nome': 'swish', 't': p['t'], 'db': -18, 'perche': f"sale «{p['testo']}»"})
    f = d['freccia']
    ev.append({'nome': 'whoosh', 't': f['t'] + 0.02, 'db': -16, 'kw': {'dur': 0.3}, 'perche': 'la freccia cade'})
    ev.append({'nome': 'pop', 't': f['t'] + 0.3, 'db': -14, 'perche': 'la freccia si posa'})
    for k in range(f.get('rimbalzi', 3)):
        tt = f['t'] + 0.62 + k * 0.56
        if tt + 0.5 > x['e'] - 0.24:
            break
        ev.append({'nome': 'tick', 't': tt + 0.17, 'db': -19, 'perche': 'rimbalzo verso la descrizione'})
    return ev


def _s_lista(x):
    d = x['dati']
    ev = [{'nome': 'swish', 't': d['titolo']['t'], 'db': -16, 'perche': 'sale il titolo'}]
    for v in d['voci']:
        ev.append({'nome': 'swish', 't': v['t'], 'db': -20, 'perche': f"sale «{v['testo']}»"})
        ev.append({'nome': 'pop', 't': v['t'] + 0.2, 'db': -15, 'perche': 'la spunta si posa'})
    return ev


def _s_finestra(spec):
    ev = []
    for fx in spec.get('piatto', []):
        if fx['tipo'] == 'finestra':
            ev.append({'nome': 'whoosh', 't': fx['s'] + 0.12, 'db': -12, 'kw': {'dur': 0.5}, 'perche': 'il quadro diventa finestra'})
            ev.append({'nome': 'thump', 't': fx['s'] + fx.get('entra', 0.5) - 0.06, 'db': -16, 'perche': 'la finestra si posa'})
            ev.append({'nome': 'whoosh', 't': fx['e'] + 0.1, 'db': -15, 'kw': {'dur': 0.4}, 'perche': 'torna a tutto schermo'})
    return ev


def _s_frase_chiave(x):
    dirz = -1 if x['dati'].get('lato', 'sx') == 'sx' else 1
    return [{'nome': 'whoosh', 't': x['s'] + 0.04, 'db': -17, 'kw': {'direzione': -dirz, 'dur': 0.34}, 'pan': 0.4 * dirz,
             'perche': 'entra il pannello della frase chiave'},
            {'nome': 'swish', 't': x['e'] - 0.3, 'db': -21, 'pan': 0.4 * dirz, 'perche': 'esce il pannello'}]


def _s_titolo(x):
    return [{'nome': 'whoosh', 't': x['s'] + 0.02, 'db': -15, 'kw': {'dur': 0.5}, 'perche': f"titolo dietro «{' '.join(x['dati']['linee'])}»"},
            {'nome': 'thump', 't': x['s'] + 0.42, 'db': -17, 'perche': 'il titolo si posa'}]


def _s_anatomia(x):
    d = x['dati']
    ev = [{'nome': 'whoosh', 't': d.get('t_figura', x['s']) + 0.04, 'db': -16, 'kw': {'dur': 0.42}, 'perche': 'entra il disegno'}]
    for g in d.get('segni', []):
        if g.get('neutro'):
            continue
        ev.append({'nome': 'pop' if g['tipo'] == 'numero' else 'tick', 't': g['t'] + 0.06, 'db': -19 if g['tipo'] != 'numero' else -17,
                   'perche': f"segno {g['tipo']}"})
        if g['tipo'] == 'asse' and g.get('ang'):
            ev.append({'nome': 'riser', 't': g.get('t_ruota', g['t'] + 0.32), 'db': -24, 'kw': {'dur': g.get('dur', 1.2)},
                       'perche': "l'asse del bacino ruota"})
    return ev


def _s_tentativi(x):
    ev = [{'nome': 'swish', 't': x['s'] + 0.02, 'db': -19, 'perche': 'torna la lista dei tentativi'}]
    for v in x['dati']['voci']:
        if v.get('nuova'):
            ev.append({'nome': 'click', 't': v['t'] + 0.06, 'db': -17, 'perche': f"si aggiunge «{v['testo']}»"})
    return ev


def _s_sagoma(x):
    d = x['dati']
    ev = [{'nome': 'whoosh', 't': x['s'] + 0.04, 'db': -16, 'kw': {'dur': 0.45}, 'perche': 'entra il vetro con la sagoma'}]
    for st in d.get('stati', [])[1:]:
        ev.append({'nome': 'swish', 't': st['t'] + 0.04, 'db': -21, 'perche': f"la pancia {'va avanti' if st['pancia'] > 0.5 else 'rientra'}"})
    return ev


def _s_fumetti(x):
    return [{'nome': 'pop', 't': v['t'] + 0.03, 'db': -16, 'perche': f"fumetto «{' '.join(v['righe'])[:30]}»"}
            for v in x['dati']['voci']] + [{'nome': 'swish', 't': x['e'] - 0.28, 'db': -21, 'perche': 'escono i fumetti'}]


def _s_etichette_luce(x):
    ev = []
    for v in x['dati']['voci']:
        ev.append({'nome': 'whoosh' if v.get('accesa', True) else 'tick', 't': v['t'] + 0.02, 'db': -18,
                   'kw': {'dur': 0.3} if v.get('accesa', True) else {}, 'perche': f"etichetta «{v['testo']}»"})
        if v.get('barra_t') is not None and v.get('accesa', True):
            ev.append({'nome': 'click', 't': v['barra_t'] + 0.04, 'db': -16, 'perche': f"«{v['testo']}» barrata"})
    return ev


def _s_card_spessore(x):
    return [{'nome': 'click', 't': c['t'] + 0.05, 'db': -17, 'perche': f"card «{c['testo'].replace('|', ' ')[:30]}»"} for c in x['dati']['carte']]


def _s_frase_luce(x):
    d = x['dati']
    ev = [{'nome': 'swish', 't': (d.get('vetro') or {}).get('t', x['s']), 'db': -20, 'perche': 'entra la frase'}]
    ev += [{'nome': 'tick', 't': p['t'] + 0.03, 'db': -22, 'perche': f"parola chiave «{p['testo']}»"}
           for p in d.get('parole', []) if p.get('chiave')]
    return ev


def _s_foto_card(x):
    return [{'nome': 'whoosh', 't': x['s'] + 0.03, 'db': -16, 'kw': {'dur': 0.4}, 'perche': 'entra la foto'}] + \
        [{'nome': 'tick', 't': a['t'] + 0.06, 'db': -18, 'perche': 'anello'} for a in x['dati'].get('anelli', [])]


def _s_card_accese(x):
    d = x['dati']
    ev = [{'nome': 'whoosh', 't': x['s'] + 0.02, 'db': -16, 'perche': 'taglio sulla scena scura'},
          {'nome': 'scan', 't': d['t_entra'], 'db': -20, 'perche': 'le card entrano con la scansione'}]
    for c in d['carte']:
        ev += [{'nome': 'swish', 't': c['t_pre'] - 0.45, 'db': -24, 'perche': 'la camera va sulla card'},
               {'nome': 'tick', 't': c['t_chiave'] - 0.18, 'db': -22, 'perche': 'il testo si decifra'},
               {'nome': 'impact', 't': c['t_chiave'] + 0.05, 'db': -17, 'perche': 'la card si accende'}]
    return ev


def _s_linea_tempo(x):
    d = x['dati']
    ev = [{'nome': 'whoosh', 't': x['s'] + 0.02, 'db': -16, 'perche': 'taglio sulla scena scura'},
          {'nome': 'pop', 't': d['num']['t'], 'db': -15, 'perche': 'nasce il nodo'},
          {'nome': 'riser', 't': d['t_via'], 'db': -22, 'kw': {'dur': max(0.4, d['t_arrivo'] - d['t_via'])}, 'allinea': 'inizio',
           'perche': 'il nodo disegna la linea'},
          {'nome': 'impact', 't': d['t_arrivo'], 'db': -17, 'perche': 'la linea arriva'}]
    ev += [{'nome': 'swish', 't': p['t'], 'db': -22, 'perche': 'entra la pillola'} for p in d.get('pillole', [])]
    return ev


def _s_equazione(x):
    d = x['dati']
    ev = [{'nome': 'tick', 't': r['t'] - 0.04, 'db': -20, 'perche': 'si decifra un termine'} for r in d['righe']]
    if d.get('barra'):
        ev.append({'nome': 'pop', 't': d['barra']['t'], 'db': -19, 'perche': 'cresce la barra'})
    return ev


def _s_connettore(x):
    d = x['dati']
    ev = [{'nome': 'tick', 't': d.get('t_sx', d.get('t_alto')), 'db': -20, 'perche': 'la prima etichetta'},
          {'nome': 'tick', 't': d.get('t_dx', d.get('t_basso')), 'db': -20, 'perche': 'la seconda etichetta'},
          {'nome': 'whoosh', 't': d['t_linea'], 'db': -21, 'kw': {'dur': 0.3}, 'perche': 'la linea si disegna'},
          {'nome': 'pop', 't': d['t_linea'] + 0.14, 'db': -16, 'perche': 'nasce il nodo'}]
    return ev


def _s_riga_icone(x):
    return [{'nome': 'pop', 't': v['t'], 'db': -17, 'perche': f"icona «{v['testo']}»"} for v in x['dati']['voci']]


SUONI_MODELLI = {'card_accese': _s_card_accese, 'linea_tempo': _s_linea_tempo, 'equazione': _s_equazione,
                 'connettore': _s_connettore, 'riga_icone': _s_riga_icone, 'frase_chiave': _s_frase_chiave, 'fumetti': _s_fumetti, 'etichette_luce': _s_etichette_luce,
                 'card_spessore': _s_card_spessore, 'frase_luce': _s_frase_luce, 'foto_card': _s_foto_card, 'titolo_dietro': _s_titolo, 'anatomia': _s_anatomia,
                 'tentativi': _s_tentativi, 'sagoma': _s_sagoma,
                 'parole': _s_parole, 'numero_dietro': _s_numero, 'schermata': _s_schermata,
                 'card': _s_card, 'telefono3d': _s_telefono, 'confronto': _s_confronto, 'cta': _s_cta,
                 'chiusura': lambda x: [{'nome': 'whoosh', 't': x['s'] + 0.08, 'db': -13, 'perche': 'schermata di chiusura'},
                                        {'nome': 'pop', 't': x['s'] + 0.75, 'db': -15, 'perche': 'la freccia si posa'}],
                 'lista_attesa': _s_lista}


# ------------------------------------------------------------------ fase
def campionario(slug, solo=None, rifai=None, v2=None):
    """./mve campionario <slug> [--v2] [--solo 3,5]: i modelli di
    campionario/campionario.json (v1) o campionario/v2/campionario.json (v2)"""
    P = Progetto(slug)
    dest = AGENTE / 'campionario' / ('v2' if v2 else '')
    dest = dest if v2 else AGENTE / 'campionario'
    C = leggi(dest / 'campionario.json')
    if C['slug'] != slug:
        sys.exit(f"campionario.json e scritto per {C['slug']}")
    solo = {s.strip() for s in solo.split(',')} if solo else None
    anc = Ancore(P)
    ctrl = dest / 'controlli'
    ctrl.mkdir(parents=True, exist_ok=True)
    tutti = leggi(ctrl / 'campionario.json') if (ctrl / 'campionario.json').exists() else {}
    for sp in C['modelli']:
        tag = f"{sp['n']:02d}" + sp.get('sub', '')
        if solo and tag not in solo and str(sp['n']) not in solo and f"{sp['n']}{sp.get('sub', '')}" not in solo:
            continue
        if sp.get('tipo') == 'suoni':
            r = palette_suoni(P, sp, dest)
            tutti[tag] = r
            print(f"  {tag} {sp['nome']}: {r['file']}")
            continue
        anc.usate.clear()
        nome = f"{tag}-{sp['nome']}.mp4"
        print(f"{tag} {sp['nome']}...")
        rap, tempo, cam, volto, spr = costruisci(P, json.loads(json.dumps(sp)), dest / nome, anc, bool(rifai))
        env_map = (anc.env, tempo.montato)
        strisce = []
        for k, st in enumerate(spr.get('strisce', [])):
            png = ctrl / f"{tag}-striscia-{k + 1}.jpg"
            ancore = [(u['parola'], tempo.out(u['t'])) for u in rap['ancore']]
            striscia(dest / nome, st['t'], png, P, env_map, f"{tag} {sp['nome']} — {st.get('cosa', '')}",
                     passo=st.get('passo', 2), prima=st.get('prima', 4), dopo=st.get('dopo', 26), ancore=ancore,
                     volto=volto if st.get('volto') else None)
            strisce.append(str(png.relative_to(AGENTE)))
        rap['strisce'] = strisce
        if v2:
            from .tavole import tavola
            el = [x for x in spr['elementi'] if x['modello'] != 'etichetta']
            tm = spr.get('migliore')
            if isinstance(tm, dict):
                tm = tempo.out(anc(tm))
            elif tm is None:
                tm = (el[0]['s'] + el[0]['e']) / 2 if el else tempo.durata / 2
            a = max(0.0, el[0]['s'] - 0.2) if el else 0.0
            b = min(tempo.durata - 0.05, max(x['e'] for x in el)) if el else tempo.durata - 0.05
            chiavi = [a + (b - a) * k / 5 for k in range(6)]
            rap['reference'] = tavola(dest / nome, tag, TITOLI.get(sp['nome'], sp['nome']), tm, chiavi, ctrl)
            rap['tavola'] = f"campionario/v2/controlli/{tag}-tavola.jpg"
            rap['migliore_s'] = round(tm, 2)
        tutti[tag] = rap
        for c in rap['controlli']:
            print(f"     {'ok ' if c['ok'] else 'NO '} {c['cosa']}: {c['valore']}")
        print(f"     -> {nome}  {rap['durata']} s, {rap['loudness']['I']} LUFS, {rap['tempi_s']['totale']} s")
    scrivi(ctrl / 'campionario.json', tutti)
    if not solo or 'assembla' in solo:
        assembla(P, C, dest, 'campionario-v2.mp4' if v2 else 'campionario.mp4')


# ------------------------------------------------------------------ palette dei suoni
def palette_suoni(P, sp, dest):
    """10-suono: ogni suono della libreria sintetizzata, uno dopo l'altro, col nome
    a schermo (per approvarli a orecchio)"""
    fps = P.fps
    voci = sp['voci']
    passo = sp.get('passo', 1.3)
    dur = 0.8 + passo * len(voci) + 0.6
    n = int(round(dur * fps))
    sr = 48000
    bus = np.zeros((int(dur * sr) + sr * 3, 2))
    righe = []
    for k, v in enumerate(voci):
        t = 0.8 + k * passo
        x = SFX.suono(v['nome'], v.get('seme', 0), fonte=v.get('fonte'), **v.get('kw', {}))
        x = x * 10 ** ((-20 + v.get('db', 0) - SFX.rms_forte(x)) / 20)
        i = int((t + 1 / fps - SFX.picco_s(x)) * sr)
        bus[i:i + len(x)] += x
        righe.append((t, v['etichetta']))
    bus = bus[:int(dur * sr)]
    cart = LAVORO / f"{sp['n']:02d}-{sp['nome']}"
    cart.mkdir(parents=True, exist_ok=True)
    wav = cart / 'suoni.wav'
    _wav(wav, bus / max(1.0, np.abs(bus).max() / 0.84))
    font_g = ImageFont.truetype(str(FONT), 96)
    font_g.set_variation_by_axes([800])
    font_p = ImageFont.truetype(str(FONT), 44 if len(voci) <= 12 else 38)
    font_p.set_variation_by_axes([500])
    out = dest / f"{sp['n']:02d}-{sp['nome']}.mp4"
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080',
                            '-framerate', P.fps_str, '-i', '-', '-i', str(wav), '-vf',
                            'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv', '-c:v', 'libx264',
                            '-crf', '18', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                            '-color_range', 'tv', '-c:a', 'aac', '-b:a', '192k', '-shortest', str(out)],
                           stdin=subprocess.PIPE)
    cache = {}
    for f in range(n):
        t = f / fps
        att = max([k for k, (tt, _) in enumerate(righe) if tt - 0.04 <= t] or [-1])
        if att not in cache:
            im = Image.new('RGB', (1920, 1080), (0, 26, 61))
            d = ImageDraw.Draw(im)
            d.text((160, 70), sp.get('titolo', "Suoni del campionario"), font=font_p, fill=(244, 244, 244))
            for k, (tt, et) in enumerate(righe):
                y = 150 + k * min(62, 860 // max(1, len(righe)))
                col = (114, 250, 147) if k == att else (244, 244, 244) if k < att else (110, 130, 160)
                d.text((160, y), et, font=font_p, fill=col)
            cache[att] = im.tobytes()
        enc.stdin.write(cache[att])
    enc.stdin.close()
    enc.wait()
    return {'n': sp['n'], 'nome': sp['nome'], 'file': str(out.relative_to(AGENTE)), 'durata': round(n / fps, 2),
            'voci': [v['etichetta'] for v in voci]}


# ------------------------------------------------------------------ assemblaggio
def _cartello(P, testo_n, titolo, out, dur=1.2):
    """cartello del campionario: numero in verde sul blu profondo, nome in panna"""
    im = Image.new('RGB', (W_OUT, H_OUT), (0, 26, 61))
    d = ImageDraw.Draw(im)
    fn = ImageFont.truetype(str(FONT), 300)
    fn.set_variation_by_axes([800])
    ft = ImageFont.truetype(str(FONT), 84)
    ft.set_variation_by_axes([500])
    d.text((200, 250), testo_n, font=fn, fill=(114, 250, 147))
    d.text((210, 640), titolo, font=ft, fill=(244, 244, 244))
    png = out.with_suffix('.png')
    im.save(png)
    ffmpeg('-loop', '1', '-framerate', P.fps_str, '-i', png, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
           '-t', f"{dur:.2f}", '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv', '-c:v', 'libx264',
           '-crf', '16', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
           '-color_range', 'tv', '-c:a', 'aac', '-b:a', '192k', '-shortest', out)
    png.unlink()


def _unisci(P, files, out):
    ins = []
    for f in files:
        ins += ['-i', str(f)]
    n = len(files)
    fc = ''.join(f"[{k}:v][{k}:a]" for k in range(n)) + f"concat=n={n}:v=1:a=1[vc][a];[vc]setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[v]"
    ffmpeg(*ins, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '16',
           '-preset', 'medium', '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709',
           '-color_trc', 'bt709', '-color_range', 'tv', '-r', P.fps_str, '-c:a', 'aac', '-b:a', '192k',
           '-movflags', '+faststart', out)


TITOLI = {'camera-viva': 'Camera viva', 'numero-dietro': 'Numero gigante dietro di lui',
          'frase-sul-corpo': 'Frase sul corpo', 'schermata-tipografica': 'Schermata tipografica',
          'card-fluttuanti': 'Card vicino alle mani', 'telefono-prospettiva': 'Telefono in prospettiva',
          'prima-dopo-cursore': 'Prima/dopo con cursore', 'cta-lista-attesa': 'Link e lista d\'attesa',
          'transizione-spinta': 'Transizione a spinta', 'transizione-zoom': 'Transizione a zoom',
          'suoni': 'Suoni', 'colore': 'Due look a confronto'}


def assembla(P, C, dest, nome_out='campionario.mp4'):
    """i gruppi (11a+b+c -> 11-colore.mp4) e campionario.mp4 con i cartelli"""
    tmp = LAVORO / '_assembla'
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    gruppi = {}
    for sp in C['modelli']:
        if sp.get('gruppo'):
            gruppi.setdefault(sp['gruppo'], []).append(dest / f"{sp['n']:02d}{sp.get('sub', '')}-{sp['nome']}.mp4")
    for g, files in gruppi.items():
        if all(f.exists() for f in files):
            _unisci(P, files, dest / f"{g}.mp4")
    seq, visti = [], set()
    for sp in C['modelli']:
        tag = f"{sp['n']:02d}{sp.get('sub', '')}"
        if sp.get('gruppo'):
            if sp['gruppo'] in visti:
                continue
            visti.add(sp['gruppo'])
            f, nome, num = dest / f"{sp['gruppo']}.mp4", 'colore', str(sp['n'])
        else:
            f, nome, num = dest / f"{tag}-{sp['nome']}.mp4", sp['nome'], f"{sp['n']}{sp.get('sub', '')}"
        if not f.exists():
            print(f"  manca {f.name}: non entra nel campionario")
            continue
        c = tmp / f"c-{tag}.mp4"
        _cartello(P, num, TITOLI.get(nome, nome), c)
        seq += [c, f]
    _unisci(P, seq, dest / nome_out)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"-> {(dest / nome_out).relative_to(AGENTE)} ({len(seq) // 2} modelli)")

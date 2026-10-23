"""Apple Vision: dove sta il volto, quanto e buono lo scatto, dove sta la persona.

Il lavoro vero lo fa `motore/swift/visione.swift`, compilato al primo uso in
`.cache/visione`. Da qui escono tre cose che prima si stimavano a occhio:

- la **traccia del volto** sulla sorgente (`data/volti.json`): centra i punch-in,
  sposta le card dalla parte libera, sceglie i fotogrammi delle miniature;
- il **controllo terzi**: piu di un volto in inquadratura e l'unico stop
  assoluto della produzione;
- le **sagome** della persona sul montato, per i titoli che passano dietro.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from bisect import bisect_left
from pathlib import Path

import numpy as np

from .progetto import AGENTE, CACHE, Progetto, scrivi, leggi, ffmpeg, FPS

SWIFT = AGENTE / 'motore/swift/visione.swift'
BIN = CACHE / 'visione'


def binario():
    if not BIN.exists() or BIN.stat().st_mtime < SWIFT.stat().st_mtime:
        CACHE.mkdir(exist_ok=True)
        print("compilo motore/swift/visione.swift...")
        subprocess.run(['swiftc', '-O', '-suppress-warnings', str(SWIFT), '-o', str(BIN)],
                       check=True)
    return BIN


def _run(*args):
    r = subprocess.run([str(binario())] + [str(a) for a in args], stderr=subprocess.PIPE, text=True)
    if r.returncode:
        sys.exit(f"visione fallita: {r.stderr[-400:]}")


def volti(slug, passo=0.5):
    P = Progetto(slug)
    out = P.data('volti.json')
    m = P.meta()
    _run('volti', P.sorgente, passo, out)
    d = leggi(out)
    c = d['campioni']
    n = [len(x['volti']) for x in c]
    con = sum(1 for k in n if k >= 1)
    multi = [x['t'] for x in c if len([v for v in x['volti'] if v['conf'] > 0.8 and v['w'] > 0.03]) > 1]
    print(f"{len(c)} campioni ogni {passo}s: volto trovato nel {con/len(c)*100:.1f}%")
    # un volto di terzi resta in scena; un campione isolato e quasi sempre una
    # mano o un oggetto (in YT_TOFU_02 le mani giunte, due volte in 20 minuti)
    corse, cur = [], []
    for t in multi:
        if cur and t - cur[-1] > passo * 1.5:
            corse.append(cur)
            cur = []
        cur.append(t)
    if cur:
        corse.append(cur)
    lunghe = [c for c in corse if c[-1] - c[0] >= 1.5]
    m['volti_terzi'] = [[round(c[0], 2), round(c[-1], 2)] for c in lunghe]
    m['volti_isolati'] = [round(c[0], 2) for c in corse if c not in lunghe]
    scrivi(P.p('meta.json'), m)
    if lunghe:
        print(f"  !!! STOP: un secondo volto resta in scena in {len(lunghe)} tratti ("
              f"{', '.join(f'{c[0]:.1f}-{c[-1]:.1f}s' for c in lunghe[:6])}). "
              f"Volti di terzi: e l'unico stop assoluto, va chiesto a Carlos.")
    elif corse:
        print(f"  secondo volto solo in {len(corse)} campioni isolati "
              f"({', '.join(f'{c[0]:.1f}s' for c in corse[:6])}): quasi certamente mani o oggetti, "
              f"controllali con un'occhiata")
    else:
        print("  nessun volto di terzi")


class Traccia:
    """Volto principale nel tempo sorgente, in pixel della sorgente."""

    def __init__(self, P):
        d = P.leggi('volti.json')
        m = P.meta()
        self.W, self.H = m['larghezza'], m['altezza']
        self.t, self.box, self.q = [], [], []
        for c in d['campioni']:
            vv = [v for v in c['volti'] if v['conf'] > 0.5]
            if not vv:
                continue
            v = max(vv, key=lambda v: v['w'] * v['h'])
            self.t.append(c['t'])
            self.box.append((v['x'] * self.W, v['y'] * self.H, v['w'] * self.W, v['h'] * self.H))
            self.q.append(v)
        self.box = np.array(self.box) if self.box else np.zeros((0, 4))

    def finestra(self, a, b):
        i0, i1 = bisect_left(self.t, a), bisect_left(self.t, b)
        return self.box[i0:i1], self.q[i0:i1]

    def mediana(self, a, b):
        """riquadro mediano (x, y, w, h) in [a, b]; None se il volto non c'e"""
        bx, _ = self.finestra(a, b)
        if len(bx) == 0:
            # finestra troppo corta: il campione piu vicino
            if not self.t:
                return None
            i = min(range(len(self.t)), key=lambda k: abs(self.t[k] - (a + b) / 2))
            return tuple(self.box[i])
        return tuple(np.median(bx, axis=0))

    def inviluppo(self, a, b):
        """il riquadro che contiene il volto in tutta la finestra (per le collisioni)"""
        bx, _ = self.finestra(a, b)
        if len(bx) == 0:
            m = self.mediana(a, b)
            return m
        x0, y0 = bx[:, 0].min(), bx[:, 1].min()
        x1, y1 = (bx[:, 0] + bx[:, 2]).max(), (bx[:, 1] + bx[:, 3]).max()
        return (x0, y0, x1 - x0, y1 - y0)


def estrai_frame(video, t0, t1, cartella, scala=None):
    """tutti i frame di [t0, t1) come PNG numerati dal frame del montato"""
    os.makedirs(cartella, exist_ok=True)
    n0 = int(round(t0 * FPS))
    vf = f"scale={scala}" if scala else "null"
    ffmpeg('-ss', f"{n0 / FPS:.4f}", '-i', video, '-frames:v', str(int(round((t1 - t0) * FPS))),
           '-vf', vf, '-start_number', str(n0), os.path.join(cartella, 'f%06d.png'))


def sagome(slug):
    """sagome della persona sul montato pulito, nelle finestre dei titoli dietro"""
    from .grafica import piano as G
    P = Progetto(slug)
    plan = P.leggi('grafica.json')
    finestre = [(c['s'], c['e']) for c in plan['capitoli'] if c.get('dietro')]
    if not finestre:
        print("nessun titolo dietro in regia: niente sagome da calcolare")
        return
    video = P.render(f"{slug}_pulito.mp4")
    dst = P.p('data', 'sagome')
    shutil.rmtree(dst, ignore_errors=True)
    dst.mkdir()
    for a, b in finestre:
        with tempfile.TemporaryDirectory() as tmp:
            estrai_frame(video, a, b, tmp)
            _run('sagome', tmp, dst)
    n = len(list(dst.glob('*.png')))
    attese = sum(int(round((b - a) * FPS)) for a, b in finestre)
    print(f"{n} sagome su {attese} frame attesi -> data/sagome/")
    if n < attese * 0.98:
        sys.exit("  !!! mancano sagome: i titoli dietro uscirebbero sopra la persona")

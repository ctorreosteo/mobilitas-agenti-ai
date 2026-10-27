"""Dove sta ogni file di un video, e come si leggono e scrivono i dati.

Un video e una cartella `videos/<slug>/`. L'unico file scritto a mano (dall'agente)
e `regia.json`: tutto il resto lo genera il motore e si puo rigenerare.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

AGENTE = Path(__file__).resolve().parents[2]
VIDEOS = AGENTE / 'videos'
RISORSE = Path(__file__).resolve().parent / 'risorse'
CACHE = AGENTE / '.cache'
WHISPER_MODEL = Path.home() / '.cache/hyperframes/whisper/models/ggml-large-v3.bin'

FPS_NUM, FPS_DEN = 30000, 1001
FPS = FPS_NUM / FPS_DEN


class Progetto:
    def __init__(self, slug):
        self.slug = slug
        self.dir = VIDEOS / slug
        if not self.dir.is_dir():
            sys.exit(f"video '{slug}' non trovato in {VIDEOS}")
        for sub in ('assets', 'data', 'renders', 'controlli'):
            (self.dir / sub).mkdir(exist_ok=True)

    # ---- percorsi -----------------------------------------------------------
    def p(self, *parts):
        return self.dir.joinpath(*parts)

    @property
    def sorgente(self):
        m = self.meta()
        return self.p(m['sorgente'])

    def asset(self, name):
        return self.p('assets', name)

    def data(self, name):
        return self.p('data', name)

    def render(self, name):
        return self.p('renders', name)

    def controllo(self, name):
        return self.p('controlli', name)

    # ---- json ---------------------------------------------------------------
    def meta(self):
        return leggi(self.p('meta.json'))

    def regia(self):
        path = self.p('regia.json')
        if not path.exists():
            sys.exit("manca regia.json: e il file delle decisioni, va scritto prima di questa fase")
        return leggi(path)

    def leggi(self, name, default=None):
        path = self.data(name)
        if not path.exists():
            if default is not None:
                return default
            sys.exit(f"manca data/{name}: lancia prima la fase che lo genera")
        return leggi(path)

    def scrivi(self, name, obj):
        scrivi(self.data(name), obj)


def leggi(path):
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def scrivi(path, obj, indent=1):
    tmp = str(path) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        json.dump(obj, fh, indent=indent, ensure_ascii=False)
    os.replace(tmp, path)


def esegui(cmd, **kw):
    """ffmpeg & co: fallisce forte, con il comando in chiaro."""
    r = subprocess.run([str(c) for c in cmd], **kw)
    if r.returncode != 0:
        sys.exit(f"comando fallito ({r.returncode}): {' '.join(str(c) for c in cmd)[:400]}")
    return r


def ffmpeg(*args, quiet=True, **kw):
    base = ['ffmpeg', '-hide_banner', '-nostdin', '-y']
    base += ['-loglevel', 'error'] if quiet else ['-loglevel', 'error', '-stats']
    return esegui(base + list(args), **kw)


def ts(t):
    """secondi -> m:ss.cc, per i referti"""
    m, s = divmod(max(t, 0.0), 60)
    return f"{int(m)}:{s:05.2f}"


def frame_q(t):
    """quantizza un tempo sulla griglia dei frame d'uscita (29.97)"""
    return round(round(t * FPS) / FPS, 6)


# le parti di regia.json che ogni fase usa: se cambiano solo le altre, la fase
# non va rifatta (stato.py confronta queste impronte, non la data del file)
REGIA_DI = {
    'edl.json': ('tagli', 'ritmo', 'pause_da_tenere'),
    'grafica.json': ('card', 'capitoli', 'enfasi', 'apertura', 'chip', 'chiusura', 'correzioni',
                     'capitolo_iniziale', 'capitolo_finale', 'scene', 'segni', 'finitura'),
}


def impronta(regia, chiavi):
    import hashlib
    sub = {k: regia.get(k) for k in chiavi}
    return hashlib.sha1(json.dumps(sub, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]

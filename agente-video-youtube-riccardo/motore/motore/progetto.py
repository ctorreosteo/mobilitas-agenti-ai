"""Dove sta ogni file di un video, e come si leggono e scrivono i dati.

Un video e una cartella `videos/<slug>/`. L'unico file scritto a mano (dall'agente)
e `regia.json`: tutto il resto lo genera il motore e si puo rigenerare.
"""
import json
import os
import subprocess
import sys
from fractions import Fraction
from functools import cached_property
from pathlib import Path

AGENTE = Path(__file__).resolve().parents[2]

# Regola del laboratorio (CLAUDE.md): nessun file fuori dalla cartella del
# laboratorio. Ogni cartella temporanea del motore (clip delle sonde, fotogrammi per
# le sagome, punti di posa...) va in .lavoro/tmp, non in quella di sistema; vale
# anche per i programmi lanciati dal motore (TMPDIR). Trovato il 28/10/2026 dal
# cacciatore di papere: prima tempfile scriveva nella cartella temporanea di macOS.
import tempfile as _tempfile
_TMP = AGENTE / '.lavoro' / 'tmp'
_TMP.mkdir(parents=True, exist_ok=True)
_tempfile.tempdir = str(_TMP)
os.environ['TMPDIR'] = str(_TMP)
VIDEOS = AGENTE / 'videos'
RISORSE = Path(__file__).resolve().parent / 'risorse'
CACHE = AGENTE / '.cache'
# materiali: quelli di un solo video in inbox/<SLUG>/materiali/, quelli comuni in libreria/
INBOX = AGENTE / 'inbox'
LIBRERIA = AGENTE / 'libreria'


def _modello_whisper():
    """il modello large-v3 di whisper.cpp. Si cerca, in ordine: MVE_WHISPER_MODEL,
    `.modelli/` nella cartella dell'agente (dove lo mette installa.sh), la cache di
    HyperFrames nella casa dell'utente (dove sta in laboratorio)."""
    for p in (os.environ.get('MVE_WHISPER_MODEL'), AGENTE / '.modelli' / 'ggml-large-v3.bin',
              Path.home() / '.cache/hyperframes/whisper/models/ggml-large-v3.bin'):
        if p and Path(p).is_file():
            return Path(p)
    return AGENTE / '.modelli' / 'ggml-large-v3.bin'


WHISPER_MODEL = _modello_whisper()


def ram_gb():
    """memoria del Mac in GB (sysctl hw.memsize); 0 se non si legge"""
    try:
        return int(subprocess.run(['sysctl', '-n', 'hw.memsize'], capture_output=True,
                                  text=True).stdout.strip()) / 2 ** 30
    except (ValueError, OSError):
        return 0


def lavori(n):
    """quanti lavori pesanti insieme, al posto di n (pensato per 32 GB e oltre).
    Misure del 02/11/2026: whisper large-v3 3,9 GB per istanza, un render
    HyperFrames con la composizione 3,3 GB. Da 32 GB in su: n; da 16 a 31 GB: la
    meta (arrotondata in su); sotto i 16 GB: uno alla volta. MVE_LAVORI=<k> lo
    forza (k al massimo, mai piu di n)."""
    forzato = os.environ.get('MVE_LAVORI')
    if forzato and forzato.isdigit() and int(forzato) > 0:
        return max(1, min(n, int(forzato)))
    ram = ram_gb()
    if ram >= 31 or ram == 0:
        return n
    if ram >= 15:
        return max(1, -(-n // 2))
    return 1


def fps_uscita(fps_raw):
    """frame rate d'uscita dal frame rate della sorgente ('num/den', come r_frame_rate).

    Sopra i 30 fps l'uscita e la meta esatta (59,94 -> 29,97; 50 -> 25): si decima
    2:1, un frame si e uno no, nessun judder. Fino a 30 fps resta uguale alla
    sorgente. Torna una stringa 'num/den' per ffmpeg (-framerate, fps=) e per il QC.
    """
    f = Fraction(fps_raw)
    if f > 30:
        f /= 2
    return f"{f.numerator}/{f.denominator}"


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

    # ---- materiali ----------------------------------------------------------
    def cartelle_materiali(self):
        """dove cercare i materiali, nell'ordine: quelli del video (meta.json ->
        materiali, altrimenti inbox/<slug>/materiali/), poi la libreria comune"""
        mp = self.p('meta.json')
        m = leggi(mp) if mp.exists() else {}
        propri = Path(m['materiali']) if m.get('materiali') else INBOX / self.slug / 'materiali'
        return [c for c in (propri, LIBRERIA) if c.is_dir()]

    def materiale(self, nome):
        """un materiale per nome o percorso relativo ('render_1.png', 'logo/logo_verde.png').
        Vince il primo trovato nell'ordine di cartelle_materiali(); dentro una cartella
        un nome che compare piu volte e un errore, non una scelta a caso."""
        for c in self.cartelle_materiali():
            diretto = c / nome
            if diretto.is_file():
                return diretto
            trovati = sorted(q for q in c.rglob('*') if q.is_file() and q.name == Path(nome).name)
            if len(trovati) == 1:
                return trovati[0]
            if len(trovati) > 1:
                sys.exit(f"materiale '{nome}' ambiguo in {c}: " + ', '.join(str(q.relative_to(c)) for q in trovati))
        return None

    # ---- frame rate d'uscita ------------------------------------------------
    @cached_property
    def fps_str(self):
        """'num/den' del montato: lo scrive `init` in meta.json; per i progetti
        nati prima si ricava dalla sorgente con la stessa regola"""
        m = self.meta()
        return m.get('fps_uscita') or fps_uscita(m['fps_raw'])

    @cached_property
    def fps(self):
        return float(Fraction(self.fps_str))

    @cached_property
    def gop(self):
        """parametri x264: un keyframe ogni 2 s, minimo ogni secondo"""
        return f"keyint={round(2 * self.fps)}:min-keyint={round(self.fps)}"

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

    @property
    def tipo(self):
        """'youtube' o 'mid-roll': da regia.json (`tipo`), poi da info.txt (meta.json ->
        info.tipo); senza nessuno dei due, 'youtube'. Decide cosa va in consegna/."""
        r = self.regia() if self.p('regia.json').exists() else {}
        m = self.meta() if self.p('meta.json').exists() else {}
        t = (r.get('tipo') or m.get('info', {}).get('tipo') or 'youtube').lower()
        return 'mid-roll' if t.replace(' ', '-') in ('mid-roll', 'midroll') else 'youtube'

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


def frame_q(t, fps):
    """quantizza un tempo sulla griglia dei frame d'uscita (fps = Progetto.fps)"""
    return round(round(t * fps) / fps, 6)


# le parti di regia.json che ogni fase usa: se cambiano solo le altre, la fase
# non va rifatta (stato.py confronta queste impronte, non la data del file)
REGIA_DI = {
    'edl.json': ('tagli', 'ritmo', 'pause_da_tenere'),
    'grafica.json': ('card', 'capitoli', 'enfasi', 'apertura', 'chip', 'chiusura', 'correzioni',
                     'capitolo_iniziale', 'capitolo_finale', 'sottotitoli', 'frasi_chiave', 'inserti',
                     'broll', 'materiali_vietati', 'etichette_strutturali', 'barra_avanzamento'),
}


def impronta(regia, chiavi):
    import hashlib
    sub = {k: regia.get(k) for k in chiavi}
    return hashlib.sha1(json.dumps(sub, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]

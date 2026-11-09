"""Effetti sonori sintetizzati in casa, seconda generazione (fase 6a, 27/10/2026).

Quelli di `suono.py` (v1-v2) erano rumore filtrato secco, mono, sempre uguale:
si sentivano "sintetici". Qui ogni suono ha:
- un **corpo** (tono o rumore sagomato) e un **transitorio** separati;
- **stereo vero**: il fruscio attraversa il panorama nella direzione del movimento;
- una **coda di riverbero** corta (stanza piccola, IR sintetica), che lo mette
  nello spazio invece che "dentro le cuffie";
- **varianti**: ogni nome ha 3 prese diverse (seme diverso, piccole differenze di
  tono e durata), da ruotare: lo stesso fruscio a ogni stacco e il primo segno
  di un montaggio fatto in serie.

Niente stock e niente licenze. Tutti i suoni escono stereo, float, con il picco
a 1: il livello si decide dove si mettono (`scena.mix`, in dB rispetto alla voce).

Nomi: whoosh, swish, pop, click, tick, impact, riser, thump, scan.
"""
import numpy as np

SR = 48000


def _rng(seme):
    return np.random.default_rng(1009 + seme * 7919)


def _env(n, picco=0.5, salita=1.6, discesa=2.2):
    """inviluppo asimmetrico: sale fino a `picco` (frazione) e ricade"""
    t = np.linspace(0, 1, n)
    a = np.clip(t / max(picco, 1e-3), 0, 1) ** salita
    b = np.clip((1 - t) / max(1 - picco, 1e-3), 0, 1) ** discesa
    return np.where(t < picco, a, b)


def _banda(x, f0, f1, q=0.8, fmid=None):
    """rumore attraverso una banda che scorre da f0 a f1 (passando per fmid)"""
    n = len(x)
    hop, win = 256, 1024
    w = np.hanning(win)
    out = np.zeros(n + win)
    norm = np.zeros(n + win)
    freqs = np.fft.rfftfreq(win, 1 / SR)
    pad = np.concatenate([x, np.zeros(win)])
    for i in range(0, n, hop):
        p = i / max(1, n)
        if fmid:
            fc = f0 * (fmid / f0) ** (p / 0.6) if p < 0.6 else fmid * (f1 / fmid) ** ((p - 0.6) / 0.4)
        else:
            fc = f0 * (f1 / f0) ** p
        g = np.exp(-0.5 * (np.log(np.maximum(freqs, 1) / fc) / q) ** 2)
        spec = np.fft.rfft(pad[i:i + win] * w) * g
        out[i:i + win] += np.fft.irfft(spec) * w
        norm[i:i + win] += w * w
    return out[:n] / np.maximum(norm[:n], 1e-3)


def _fft_filtro(x, basso=None, alto=None):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.ones_like(f)
    if alto:
        g *= 1 / np.sqrt(1 + (alto / np.maximum(f, 1)) ** 4)
    if basso:
        g *= 1 / np.sqrt(1 + (f / basso) ** 4)
    return np.fft.irfft(X * g, len(x))


_IR = {}


def _ir(durata=0.55, seme=0):
    """risposta all'impulso stereo di una stanza piccola: rumore che decade e si scurisce"""
    k = (round(durata, 3), seme)
    if k not in _IR:
        r = _rng(900 + seme)
        n = int(durata * SR)
        t = np.arange(n) / SR
        dec = np.exp(-t * 6.9 / durata)
        ch = []
        for c in range(2):
            z = r.standard_normal(n) * dec
            # le alte decadono prima: due bande con decadimenti diversi
            alte = _fft_filtro(z, alto=2500) * np.exp(-t * 9 / durata)
            basse = _fft_filtro(z, basso=2500)
            ch.append(basse + 0.6 * alte)
        ir = np.stack(ch, 1)
        ir[:int(0.008 * SR)] = 0          # pre-delay
        _IR[k] = ir / np.abs(ir).sum(0).max() * 6
    return _IR[k]


def _riverbero(st, mix=0.16, durata=0.55, seme=0):
    ir = _ir(durata, seme)
    n = len(st) + len(ir)
    out = np.zeros((n, 2))
    out[:len(st)] += st
    for c in range(2):
        L = 1 << int(np.ceil(np.log2(n)))
        y = np.fft.irfft(np.fft.rfft(st[:, c], L) * np.fft.rfft(ir[:, c], L), L)[:n]
        out[:, c] += mix * y
    return out


def _pan(x, p):
    """p scalare o array (-1 sinistra, +1 destra), potenza costante"""
    a = (np.asarray(p) + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], axis=1)


def _fine(st, rev=0.16, durata=0.55, seme=0):
    st = _riverbero(st, rev, durata, seme) if rev else st
    # coda morbida contro i click di troncamento
    m = min(len(st), int(0.004 * SR))
    st[:m] *= np.linspace(0, 1, m)[:, None]
    st[-m:] *= np.linspace(1, 0, m)[:, None]
    return st / (np.abs(st).max() + 1e-9)


# ------------------------------------------------------------------ suoni
def whoosh(seme=0, dur=None, direzione=1, f0=None, f1=None, aria=True):
    """fruscio di un oggetto che passa: banda che sale e ricade un poco, picco al 62%,
    attraversa il panorama nella direzione del movimento, coda di stanza"""
    r = _rng(seme)
    dur = dur or (0.42, 0.48, 0.38)[seme % 3]
    f0 = f0 or (220, 260, 190)[seme % 3]
    f1 = f1 or (700, 850, 600)[seme % 3]
    n = int(dur * SR)
    corpo = _banda(r.standard_normal(n), f0, f1, q=0.6, fmid=(1300, 1550, 1150)[seme % 3])
    corpo *= _env(n, 0.62, 2.0, 1.6)
    st = _pan(corpo, np.linspace(-0.7 * direzione, 0.7 * direzione, n))
    if aria:
        sib = _banda(r.standard_normal(n), 3200, 5200, q=0.5) * _env(n, 0.66, 3.0, 2.5) * 0.18
        st += _pan(sib, np.linspace(-0.5 * direzione, 0.5 * direzione, n))
    return _fine(st, 0.22, 0.6, seme)


def swish(seme=0, direzione=1):
    """fruscio corto e alto per una parola che entra"""
    r = _rng(50 + seme)
    n = int((0.16, 0.19, 0.14)[seme % 3] * SR)
    x = _banda(r.standard_normal(n), 900, 3200, q=0.55) * _env(n, 0.45, 1.5, 2.5)
    return _fine(_pan(x, np.linspace(-0.3 * direzione, 0.3 * direzione, n)), 0.12, 0.35, seme)


def pop(seme=0, f=None):
    """bolla: tono che scende di una quinta in 30 ms, piu un transitorio leggero"""
    r = _rng(100 + seme)
    f = f or (520, 580, 470)[seme % 3]
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    fi = f * (1 + 0.6 * np.exp(-t / 0.012))
    x = np.sin(2 * np.pi * np.cumsum(fi) / SR) * np.exp(-t / 0.028)
    x += 0.25 * np.sin(2 * np.pi * np.cumsum(fi * 2.01) / SR) * np.exp(-t / 0.012)
    cl = r.standard_normal(n) * np.exp(-t / 0.0015) * 0.35
    x += _fft_filtro(cl, alto=1500)
    return _fine(_pan(x, 0.0), 0.10, 0.3, seme)


def click(seme=0):
    """click d'interfaccia, secco e piccolo"""
    r = _rng(200 + seme)
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    f = (2900, 3300, 2600)[seme % 3]
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.004)
    x += 0.6 * np.sin(2 * np.pi * f * 0.42 * t) * np.exp(-t / 0.006)
    x += _fft_filtro(r.standard_normal(n) * np.exp(-t / 0.0012), alto=2000) * 0.6
    return _fine(_pan(x, 0.0), 0.08, 0.25, seme)


def tick(seme=0, f=None):
    """legnetto corto: per i conteggi e le voci che si spuntano"""
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    f = f or (1900, 2100, 1750)[seme % 3]
    x = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.010) + 0.5 * np.sin(2 * np.pi * f * 1.78 * t) * np.exp(-t / 0.005)
    return _fine(_pan(x, 0.0), 0.08, 0.25, seme)


def impact(seme=0, peso=1.0):
    """colpo: sub che scende (58 -> 40 Hz) con saturazione morbida, corpo di rumore
    scuro e transitorio; coda di stanza piu lunga"""
    r = _rng(300 + seme)
    dur = 1.1
    n = int(dur * SR)
    t = np.arange(n) / SR
    f0, f1 = (58, 62, 54)[seme % 3], 40
    ph = 2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t / 0.15)) / SR
    sub = 0.4 * np.tanh(2.5 * np.sin(ph) * np.exp(-t / (0.26 * peso))) / np.tanh(2.5)
    # armoniche e corpo fra 150 e 600 Hz: sul telefono il sub non c'e, si sente questo
    sub += 0.35 * np.sin(2 * ph) * np.exp(-t / 0.12)
    sub += 1.0 * np.sin(2 * np.pi * np.cumsum(175 * (1 + 0.6 * np.exp(-t / 0.015))) / SR) * np.exp(-t / 0.10)
    sub += 0.5 * np.sin(2 * np.pi * np.cumsum(260 * (1 + 0.5 * np.exp(-t / 0.02))) / SR) * np.exp(-t / 0.05)
    corpo = _fft_filtro(r.standard_normal(n), basso=900, alto=150) * np.exp(-t / 0.06) * 1.6
    tr = _fft_filtro(r.standard_normal(n), alto=2500) * np.exp(-t / 0.003) * 0.7
    x = sub + corpo + tr
    st = _pan(x, 0.0)
    st[:, 1] = np.roll(st[:, 1], int(0.0007 * SR))      # un filo di larghezza
    return _fine(st, 0.28, 0.9, seme)


def riser(seme=0, dur=0.9):
    """salita: rumore che apre verso l'alto e cresce, finisce di netto (va prima di un colpo)"""
    r = _rng(400 + seme)
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    x = _banda(r.standard_normal(n), 300, 3800, q=0.6) * (t ** 2.2)
    ton = np.sin(2 * np.pi * np.cumsum(180 * (1 + 2.0 * t ** 2)) / SR) * (t ** 3) * 0.25
    st = _pan(x + ton, 0.0)
    st[:, 0] *= 1 - 0.15 * np.sin(2 * np.pi * 3 * t)
    st[:, 1] *= 1 + 0.15 * np.sin(2 * np.pi * 3 * t)
    st[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))[:, None]
    return st / (np.abs(st).max() + 1e-9)


def thump(seme=0):
    """appoggio morbido di un oggetto (il telefono che arriva)"""
    r = _rng(500 + seme)
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * np.cumsum(95 + 60 * np.exp(-t / 0.02)) / SR) * np.exp(-t / 0.06)
    x += 0.8 * np.sin(2 * np.pi * np.cumsum(330 + 120 * np.exp(-t / 0.01)) / SR) * np.exp(-t / 0.03)
    x += _fft_filtro(r.standard_normal(n), basso=1400, alto=200) * np.exp(-t / 0.015) * 1.2
    return _fine(_pan(x, 0.0), 0.15, 0.4, seme)


def scan(seme=0, dur=0.9, direzione=1):
    """passata leggera, per una linea che si disegna o un cursore che scorre"""
    r = _rng(600 + seme)
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    x = _banda(r.standard_normal(n), 1100, 3200, q=0.45) * (0.4 + 0.6 * np.sin(np.pi * t) ** 1.2)
    x *= 0.85 + 0.15 * np.sin(2 * np.pi * 22 * t)
    return _fine(_pan(x, np.linspace(-0.6 * direzione, 0.6 * direzione, n)), 0.15, 0.4, seme)


SUONI = {'whoosh': whoosh, 'swish': swish, 'pop': pop, 'click': click, 'tick': tick,
         'impact': impact, 'riser': riser, 'thump': thump, 'scan': scan}


# ------------------------------------------------------------------ libreria (fase 6b)
# Confronto del 27/10/2026 fra i 19 effetti Pixabay di libreria/sfx e i sintetizzati
# (misure in report/2026-10-27-campionario-v2.md; l'ascolto lo fa Riccardo):
# - dalla libreria: whoosh (registrato, scuro e d'aria: il sintetizzato era piu
#   "rumore"), click e pop (registrati, naturali);
# - impact IBRIDO: il sub della libreria (impact-bass-1, tutto sotto 150 Hz: dal
#   telefono non si sente) + il corpo sintetizzato sopra 150 Hz (si sente ovunque);
# - restano sintetizzati: swish, tick, riser (quello di Pixabay ha il picco a meta,
#   non alla fine), thump, scan; esclusi glitch, chime, sparkle, ping, notification,
#   error (fuori dal tono del brand) e impact-bass-2 (satura il 10% dei campioni).
from pathlib import Path as _Path
LIB = _Path(__file__).resolve().parents[2] / 'libreria' / 'sfx'
LIBRERIA_SFX = {'whoosh': 'whoosh.mp3', 'click': 'click.mp3', 'pop': 'pop.mp3', 'impact': 'impact-bass-1.mp3'}
IBRIDI = {'impact'}
_CARICATI = {}


def _carica(nome_file):
    if nome_file not in _CARICATI:
        import subprocess
        r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(LIB / nome_file), '-ac', '2', '-ar', str(SR),
                            '-f', 'f32le', '-'], capture_output=True)
        x = np.frombuffer(r.stdout, '<f4').reshape(-1, 2).astype(np.float64)
        # via il silenzio iniziale (fino a 5 ms prima dell'attacco a -30 dB dal picco)
        m = np.abs(x).max(1)
        i = int(np.argmax(m > m.max() * 10 ** (-30 / 20)))
        x = x[max(0, i - int(0.005 * SR)):]
        _CARICATI[nome_file] = x / (np.abs(x).max() + 1e-9)
    return _CARICATI[nome_file]


def _intona(x, k):
    """cambio d'intonazione (e di durata) per ricampionamento: k > 1 piu acuto"""
    if abs(k - 1) < 1e-3:
        return x
    n = int(len(x) / k)
    t = np.arange(n) * k
    return np.stack([np.interp(t, np.arange(len(x)), x[:, c]) for c in (0, 1)], 1)


def da_libreria(nome, seme=0, dur=None, peso=1.0, **_):
    x = _intona(_carica(LIBRERIA_SFX[nome]), (1.0, 0.96, 1.04)[seme % 3])
    if dur:                                       # accorcia con una coda morbida
        n = min(len(x), int((dur + 0.15) * SR))
        x = x[:n].copy()
        k = int(min(n * 0.4, 0.12 * SR))
        x[-k:] *= np.linspace(1, 0, k)[:, None] ** 1.5
    if nome == 'impact' and peso != 1.0:
        x = x[:int(len(x) * min(1.0, 0.5 + 0.5 * peso))]
    return x


def suono(nome, seme=0, fonte=None, **kw):
    """fonte: None = la scelta del confronto (libreria dove c'e), 'sintesi', 'libreria'"""
    if fonte != 'sintesi' and nome in LIBRERIA_SFX and (LIB / LIBRERIA_SFX[nome]).exists():
        x = da_libreria(nome, seme, **kw)
        if nome in IBRIDI and fonte != 'libreria':
            y = SUONI[nome](seme=seme, **{k: v for k, v in kw.items() if k in ('peso',)})
            corpo = np.stack([_fft_filtro(y[:, c], alto=150) for c in (0, 1)], 1)
            n = max(len(x), len(corpo))
            # bilanciati sull'energia: il corpo (sopra 150 Hz) vale quanto il sub
            x = x / (np.sqrt((x ** 2).mean()) + 1e-9)
            corpo = corpo / (np.sqrt((corpo ** 2).mean()) + 1e-9)
            x = np.pad(x, ((0, n - len(x)), (0, 0))) * 1.0 + np.pad(corpo, ((0, n - len(corpo)), (0, 0))) * 1.1
            x = x / (np.abs(x).max() + 1e-9)
        return x
    return SUONI[nome](seme=seme, **kw)


def picco_s(x):
    """dove cade il picco del suono, in secondi dall'inizio (si allinea al fotogramma)"""
    return float(np.abs(x).max(1).argmax()) / SR


def rms_forte(x, finestra=0.1):
    """RMS (dB) della finestra di 100 ms piu forte: la misura con cui si confrontano voce e suoni"""
    m = x.mean(1) if x.ndim == 2 else x
    w = int(finestra * SR)
    if len(m) <= w:
        return 20 * np.log10(np.sqrt((m ** 2).mean()) + 1e-12)
    c = np.cumsum(np.concatenate([[0], m ** 2]))
    e = (c[w:] - c[:-w]) / w
    return 10 * np.log10(e.max() + 1e-12)

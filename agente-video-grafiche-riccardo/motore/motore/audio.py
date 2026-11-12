"""Inviluppo, blocchi di parlato, punti di taglio e loudness.

Due soglie diverse, per due mestieri diversi:

- i **blocchi** (parlato/silenzio) stanno 22 dB sopra il fondo di sala: servono a
  trovare le pause, quindi devono comprendere le code di sillaba;
- i **punti di taglio** cercano il primo istante in cui l'energia e tornata al
  fondo di sala (+10 dB). Il confine del blocco cade dove l'energia scende sotto
  soglia, ma la coda della sillaba continua a scendere per 100-200 ms restando
  udibile: tagliare li tronca la parola. E successo su "toracica" in YT_TOFU_02.
"""
import re
import subprocess
import sys
import wave

import numpy as np

_cache = {}


def _pcm(path):
    key = ('pcm', str(path))
    if key not in _cache:
        w = wave.open(str(path))
        n, sr = w.getnframes(), w.getframerate()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
        _cache[key] = (a, sr)
    return _cache[key]


def inviluppo(path, hop=0.010):
    a, sr = _pcm(path)
    h = int(hop * sr)
    m = len(a) // h
    rms = np.sqrt((a[:m * h].reshape(m, h) ** 2).mean(axis=1) + 1e-12)
    return 20 * np.log10(rms)


def blocchi(path, min_gap=0.20, min_speech=0.04, margin_db=22.0, hop=0.010):
    db = inviluppo(path, hop)
    floor = float(np.percentile(db, 12))
    thr = floor + margin_db
    voiced = db > thr
    m = len(db)
    out, i = [], 0
    while i < m:
        if not voiced[i]:
            i += 1
            continue
        j = i
        while j < m:
            if voiced[j]:
                j += 1
                continue
            k = j
            while k < m and not voiced[k]:
                k += 1
            if (k - j) * hop < min_gap and k < m:
                j = k
            else:
                break
        if (j - i) * hop >= min_speech:
            out.append([round(i * hop, 3), round(j * hop, 3)])
        i = j
    return out, floor, thr


class Tagli:
    """Punti di taglio sul fondo di sala, su inviluppo a 5 ms con media a 30 ms
    (le occlusive lasciano micro-buchi dentro la parola)."""
    HOP = 0.005

    def __init__(self, path):
        db = inviluppo(path, self.HOP)
        self.db = np.convolve(db, np.ones(6) / 6, mode='same')
        self.floor = float(np.percentile(self.db, 12))
        self.q = self.floor + 10.0
        self.m = len(self.db)

    def dopo(self, t, span=0.6):
        """primo istante di silenzio vero a partire da t (chiude un segmento)"""
        i0 = max(0, int(t / self.HOP))
        i1 = min(self.m, int((t + span) / self.HOP))
        for i in range(i0, i1):
            if self.db[i] < self.q:
                return round(i * self.HOP + 0.05, 3)
        seg = self.db[i0:i1]
        return round((i0 + int(np.argmin(seg))) * self.HOP + 0.05, 3) if len(seg) else t

    def prima(self, t, span=0.6):
        """ultimo istante di silenzio vero prima di t (apre un segmento)"""
        i1 = min(self.m, int(t / self.HOP))
        i0 = max(0, int((t - span) / self.HOP))
        for i in range(i1 - 1, i0 - 1, -1):
            if self.db[i] < self.q:
                return round(i * self.HOP - 0.05, 3)
        seg = self.db[i0:i1]
        return round((i0 + int(np.argmin(seg))) * self.HOP - 0.05, 3) if len(seg) else t

    def quieto(self, t, lo=None, hi=None, raggio=0.08):
        """il campione piu silenzioso entro raggio da t, senza uscire da [lo, hi]"""
        a = max(t - raggio, lo if lo is not None else -1e9)
        b = min(t + raggio, hi if hi is not None else 1e9)
        i0, i1 = max(0, int(a / self.HOP)), min(self.m, int(b / self.HOP) + 1)
        if i1 <= i0:
            return t
        return round((i0 + int(np.argmin(self.db[i0:i1]))) * self.HOP, 3)

    def respiro(self, t, min_len=0.06, raggio=0.6):
        """il tratto sopra la soglia di taglio (fondo + 10 dB) che contiene t, se c'e:
        un respiro, uno schiocco o la coda di una parola. -> (inizio, fine) o None"""
        i = int(t / self.HOP)
        if not (0 <= i < self.m) or self.db[i] < self.q:
            return None
        a = i
        lim = int(raggio / self.HOP)
        while a > 0 and self.db[a - 1] >= self.q and i - a < lim:
            a -= 1
        b = i
        while b < self.m - 1 and self.db[b + 1] >= self.q and b - i < lim:
            b += 1
        if (b - a) * self.HOP < min_len:
            return None
        return round(a * self.HOP, 3), round((b + 1) * self.HOP, 3)

    def livello(self, t):
        return float(self.db[max(0, min(self.m - 1, int(t / self.HOP)))])

    def silenzio(self, a, b):
        """quota di [a,b] che sta sotto la soglia di taglio"""
        i0, i1 = int(a / self.HOP), int(b / self.HOP)
        seg = self.db[i0:i1]
        return float((seg < self.q).mean()) if len(seg) else 1.0


def loudness(path, start=None, dur=None):
    cmd = ['ffmpeg', '-hide_banner', '-nostdin']
    if start is not None:
        cmd += ['-ss', str(start)]
    if dur is not None:
        cmd += ['-t', str(dur)]
    cmd += ['-i', str(path), '-vn', '-af', 'ebur128=peak=true', '-f', 'null', '-']
    err = subprocess.run(cmd, capture_output=True, text=True).stderr
    summ = err[err.rfind('Summary:'):]

    def grab(label):
        m = re.search(label + r':\s+(-?[\d.]+|-inf)', summ)
        return float(m.group(1)) if m and m.group(1) != '-inf' else None
    return {'I': grab('I'), 'LRA': grab('LRA'), 'TP': grab('Peak')}


def clipping(path, canali, sr, soglia=0.999, unisci=0.5, max_tratti=200):
    """Campioni a fondo scala nella sorgente, letti nel formato nativo (niente
    ricampionamento: interpolare sposterebbe proprio i campioni tosati).

    `campioni_fondo_scala` conta ogni canale; corse e tratti contano istanti
    (basta un canale a fondo scala). Un istante da solo puo essere un picco
    legittimo; due o piu di fila (una "corsa", la cima piatta dell'onda) sono clipping. Le corse vicine
    (entro `unisci` s) diventano un tratto. Si legge a blocchi da 10 s: 20 minuti
    stereo in float32 sarebbero 460 MB in memoria.
    """
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'error', '-i', str(path),
           '-map', '0:a:0', '-vn', '-f', 'f32le', '-acodec', 'pcm_f32le', '-']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    passo = sr * canali * 4 * 10
    pieni, pos, resto = [], 0, b''
    campioni = 0
    while True:
        buf = resto + proc.stdout.read(passo)
        if len(buf) < 4 * canali:
            break
        n = len(buf) // (4 * canali) * 4 * canali
        buf, resto = buf[:n], buf[n:]
        x = np.frombuffer(buf, dtype=np.float32).reshape(-1, canali)
        p = np.abs(x) >= soglia
        campioni += int(p.sum())
        # basta un canale a fondo scala; si tengono solo gli indici, che sono pochi
        pieni.append(np.flatnonzero(p.any(axis=1)) + pos)
        pos += len(x)
    if proc.wait():
        sys.exit(f"ffmpeg non riesce a leggere l'audio di {path}")
    corse = _corse(np.concatenate(pieni) if pieni else np.array([], dtype=np.int64))
    tratti = []
    for s, n in corse:
        a, b = s / sr, (s + n) / sr
        if tratti and a - tratti[-1]['e'] <= unisci:
            tratti[-1]['e'] = round(b, 3)
            tratti[-1]['corse'] += 1
            tratti[-1]['istanti'] += n
        else:
            tratti.append({'s': round(a, 3), 'e': round(b, 3), 'corse': 1, 'istanti': n})
    return {'soglia_dbfs': round(20 * np.log10(soglia), 3),
            'campioni_fondo_scala': campioni,
            'corse': len(corse),
            'corsa_max_istanti': max((n for _, n in corse), default=0),
            'durata_s': round(pos / sr, 3),
            'tratti_totali': len(tratti),
            'tratti': tratti[:max_tratti]}


def _corse(idx, minimo=2):
    """[inizio, lunghezza] delle sequenze di indici consecutivi lunghe almeno `minimo`"""
    if not len(idx):
        return []
    rotture = np.flatnonzero(np.diff(idx) != 1) + 1
    out = []
    for g in np.split(idx, rotture):
        if len(g) >= minimo:
            out.append([int(g[0]), len(g)])
    return out


def catena_voce(meta):
    """La catena voce di questa sorgente: CATENA_VOCE, preceduta da
    - `adeclip` se `prep` ha trovato clipping (corse di campioni a fondo scala):
      ricostruisce le cime tosate, e va per primo, sul segnale ancora intero;
    - un guadagno negativo se la voce arriva piu alta del livello a cui la catena
      e tarata (RIF_LUFS). Soglia del compressore e riduzione di rumore lavorano su
      livelli assoluti: su una voce a -14 LUFS il compressore schiaccerebbe 10 dB.
      Sotto RIF_LUFS non si tocca niente: i girati a -26/-29 restano come prima.
    """
    parti = []
    if (meta.get('clipping') or {}).get('corse'):
        parti.append(DECLIP)
    I = (meta.get('lufs_sorgente') or {}).get('I')
    if I is not None and I > RIF_LUFS:
        parti.append(f"volume={RIF_LUFS - I:.1f}dB")
    return ','.join(parti + [CATENA_VOCE])


# Catena voce. Tarata su sorgenti intorno a -26/-29 LUFS (RIF_LUFS e il bordo alto):
# alzarle di 15 dB alza anche il fondo, per questo la riduzione di rumore viene PRIMA
# della normalizzazione. Le sorgenti piu alte si riportano a RIF_LUFS (catena_voce).
RIF_LUFS = -26.0
# adeclip con i valori di default (threshold=10) sulla A6700 di MR_POSTURA_01 ricostruiva
# il 46% dei campioni tosati; con threshold=5 l'80%, toccando pochi campioni vicini
# (threshold=2: 90%, ma il doppio di campioni toccati fuori dalle corse).
# All'avvio adeclip riscrive la prima finestra (~40 ms) anche senza clipping: 100 ms
# di silenzio davanti, tolti subito dopo, la lasciano intatta; durata identica.
# asetpts=N/SR/TB prima di atrim: dentro il grafo di `audio` (dopo concat) adeclip
# emette timestamp che atrim scartava tutti, e la voce montata usciva vuota.
DECLIP = ("adelay=delays=100:all=1,adeclip=threshold=5,"
          "asetpts=N/SR/TB,atrim=start=0.1,asetpts=PTS-STARTPTS")
CATENA_VOCE = ("highpass=f=75,"
               "afftdn=nr=10:nf=-34:tn=1,"
               "equalizer=f=220:t=q:w=1.2:g=-1.5,"      # meno rimbombo di stanza
               "equalizer=f=3200:t=q:w=1.4:g=1.5,"      # presenza
               "deesser=i=0.3,"
               "acompressor=threshold=-20dB:ratio=2.5:attack=12:release=200:makeup=2,"
               "loudnorm=I=-14:TP=-1.5:LRA=9,"
               "alimiter=limit=0.89:level=disabled")

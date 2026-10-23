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


# Catena voce. La sorgente arriva intorno a -29 LUFS: alzarla di 15 dB alza anche
# il fondo, per questo la riduzione di rumore viene PRIMA della normalizzazione.
CATENA_VOCE = ("highpass=f=75,"
               "afftdn=nr=10:nf=-34:tn=1,"
               "equalizer=f=220:t=q:w=1.2:g=-1.5,"      # meno rimbombo di stanza
               "equalizer=f=3200:t=q:w=1.4:g=1.5,"      # presenza
               "deesser=i=0.3,"
               "acompressor=threshold=-20dB:ratio=2.5:attack=12:release=200:makeup=2,"
               "loudnorm=I=-14:TP=-1.5:LRA=9,"
               "alimiter=limit=0.89:level=disabled")

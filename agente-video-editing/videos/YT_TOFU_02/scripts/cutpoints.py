#!/usr/bin/env python3
"""Trova il punto esatto dove tagliare: il primo istante di silenzio vero.

I timestamp del riconoscitore si smarginano dentro le pause e i confini dei
blocchi di parlato stanno dove l'energia scende sotto soglia, non dove la
parola finisce davvero: una coda di sillaba continua a scendere per altri
100-200 ms restando udibile. Tagliare li tronca la parola. Qui si cerca invece
il primo campione in cui l'energia e tornata al fondo di sala.
"""
import numpy as np, wave

HOP = 0.005
_cache = {}


def curve():
    if 'db' not in _cache:
        w = wave.open('assets/audio-16k-mono.wav')
        n, sr = w.getnframes(), w.getframerate()
        a = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768.0
        hop = int(HOP * sr)
        m = len(a) // hop
        rms = np.sqrt((a[:m * hop].reshape(m, hop) ** 2).mean(axis=1) + 1e-12)
        db = 20 * np.log10(rms)
        # media mobile su 30 ms: le occlusive lasciano micro-buchi dentro la parola
        k = 6
        db = np.convolve(db, np.ones(k) / k, mode='same')
        _cache['db'] = db
        _cache['floor'] = float(np.percentile(db, 12))
        _cache['m'] = m
    return _cache['db'], _cache['floor'], _cache['m']


def quiet_after(t, span=1.2):
    """primo istante di silenzio a partire da t (per chiudere un segmento)"""
    db, floor, m = curve()
    q = floor + 10.0
    i0 = max(0, int(t / HOP))
    i1 = min(m, int((t + span) / HOP))
    for i in range(i0, i1):
        if db[i] < q:
            return round(i * HOP + 0.05, 3)
    seg = db[i0:i1]
    return round((i0 + int(np.argmin(seg))) * HOP + 0.05, 3) if len(seg) else t


def quiet_before(t, span=1.2):
    """ultimo istante di silenzio prima di t (per aprire un segmento)"""
    db, floor, m = curve()
    q = floor + 10.0
    i1 = min(m, int(t / HOP))
    i0 = max(0, int((t - span) / HOP))
    for i in range(i1 - 1, i0 - 1, -1):
        if db[i] < q:
            return round(i * HOP - 0.05, 3)
    seg = db[i0:i1]
    return round((i0 + int(np.argmin(seg))) * HOP - 0.05, 3) if len(seg) else t


def level(t):
    db, floor, m = curve()
    return float(db[max(0, min(m - 1, int(t / HOP)))])

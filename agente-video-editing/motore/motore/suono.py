"""Fase `suono`: sound design sintetizzato in casa, e musica se c'e.

Il v1 usciva muto fra una parola e l'altra. Qui ogni elemento grafico ha il suo
suono, sintetizzato con numpy (niente stock, niente licenze):

- **whoosh** quando entra una card, spostato nel panorama dal lato della card;
- **tick** del contatore della card, che rallentano con il numero e chiudono
  con un tick piu acuto quando si ferma;
- **salita + colpo basso** quando entra un titolo dietro, e un sibilo chiaro
  per la lama di luce che attraversa la stanza;
- **pop** morbido per ogni voce che entra in un'infografica (lista, catena, zone),
  e un fruscio che scende quando una lista viene barrata;
- **fruscio corto** sui punch-in di enfasi;
- colpo morbido su apertura e chiusura.

Tutto resta 10-16 dB sotto la voce: si sente come rifinitura, non come effetto.

**Musica**: solo se c'e un file in `assets/musica/` (con licenza: e una scelta di
Carlos, non dell'agente). Va in loop sotto la voce a -30 LUFS e si abbassa da
sola quando lei parla (sidechain).

Esce `assets/mix-finale.wav`: voce + suoni (+ musica) a -14 LUFS, true peak -1,5.
"""
import wave

import numpy as np

from .progetto import Progetto, FPS, ffmpeg
from . import audio as A
from . import stile as S

SR = 48000
RNG = np.random.default_rng(7)


def _env(n, att, rel_pow=2.0):
    t = np.linspace(0, 1, n)
    a = max(1, int(n * att))
    e = np.ones(n)
    e[:a] = np.linspace(0, 1, a) ** 1.5
    e[a:] = (1 - np.linspace(0, 1, n - a)) ** rel_pow
    return e


def _banda(noise, f0, f1, q=0.9):
    """rumore filtrato da una banda che scorre da f0 a f1 (STFT a blocchi)"""
    n = len(noise)
    hop, win = 256, 512
    w = np.hanning(win)
    out = np.zeros(n + win)
    freqs = np.fft.rfftfreq(win, 1 / SR)
    for i in range(0, n - win, hop):
        fc = f0 * (f1 / f0) ** (i / max(1, n - win))
        g = np.exp(-0.5 * (np.log(np.maximum(freqs, 1) / fc) / q) ** 2)
        spec = np.fft.rfft(noise[i:i + win] * w) * g
        out[i:i + win] += np.fft.irfft(spec) * w
    return out[:n]


def whoosh(dur=0.42, f0=380, f1=3600, att=0.62):
    n = int(dur * SR)
    x = _banda(RNG.standard_normal(n), f0, f1) * _env(n, att)
    return x / (np.abs(x).max() + 1e-9)


def tick(f=1750):
    n = int(0.07 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * (f - 500 * t / 0.07) * t) * np.exp(-t * 70)
    x[:48] += RNG.standard_normal(48) * np.linspace(1, 0, 48) * 0.5
    return x / np.abs(x).max()


def pop(f=1300):
    """un pop corto e tondo: una voce che entra in un'infografica"""
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * (f * 0.6 + f * 0.8 * np.exp(-t * 60)) * t) * np.exp(-t * 45)
    return x / np.abs(x).max()


def colpo(dur=0.9, f0=92, f1=44):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(f0 * (f1 / f0) ** (t / dur)) / SR
    x = np.sin(ph) * np.exp(-t * 5.5)
    x += _banda(RNG.standard_normal(n), 900, 200, q=0.7) * np.exp(-t * 28) * 0.35
    return x / np.abs(x).max()


def salita(dur=0.55):
    x = whoosh(dur, 250, 5200, att=0.92)
    return x


def _pan(x, p):
    """p da -1 (sinistra) a +1 (destra), legge a potenza costante"""
    a = (p + 1) * np.pi / 4
    return np.stack([x * np.cos(a), x * np.sin(a)], axis=1)


def _db(d):
    return 10 ** (d / 20)


def suono(slug):
    P = Progetto(slug)
    G = P.leggi('grafica.json')
    I = P.leggi('inquadratura.json')['pezzi']
    E = P.leggi('edl.json')
    n = int(E['frame'] / FPS * SR) + SR
    bus = np.zeros((n, 2))
    eventi = []

    def metti(x, t, gain_db, pan=0.0):
        i = int(t * SR)
        if i < 0:
            x, i = x[-i:], 0
        y = _pan(x, pan) * _db(gain_db)
        j = min(n, i + len(y))
        bus[i:j] += y[:j - i]
        eventi.append((round(t, 2), gain_db))

    w = whoosh()
    for c in G['cards']:
        side = -0.55 if c.get('side', 'left') == 'left' else 0.55
        metti(w, c['s'] - 0.12, -27, side)
        if c.get('tipo', 'numero') == 'numero':
            # il contatore: tick che rallentano con il numero (stessa curva del renderer),
            # poi un tick piu acuto quando si ferma
            for k in range(1, 8):
                x = -np.log2(1 - k / 8) / 10
                metti(tick(1500 + 60 * k), c['s'] + S.COUNT_T0 + S.COUNT_DUR * x, -38 + k * 0.6, side)
            metti(tick(2300), c['s'] + S.COUNT_T0 + S.COUNT_DUR, -31, side)
        # ogni voce che entra (lista, catena, zone, etichette): un pop morbido
        for k in ('voci', 'zone', 'etichette'):
            for i, v in enumerate(c.get(k, [])):
                if v.get('t') is not None:
                    metti(pop(1200 + 90 * (i % 5)), c['s'] + v['t'], -33, side)
        if c.get('annulla_t') is not None:
            metti(whoosh(0.35, 1500, 300, att=0.3), c['s'] + c['annulla_t'], -30, side)
    for c in G['capitoli']:
        if c['dietro']:
            metti(salita(), c['s'] - 0.50, -29)
            metti(colpo(), c['s'] + 0.02, -21)
            # la lama di luce che attraversa la stanza
            metti(whoosh(S.LAMA, 900, 7000, att=0.5), c['s'], -31)
        else:
            metti(whoosh(0.5, 300, 4200), c['s'] - 0.15, -26)
            metti(colpo(), c['s'] + 0.25, -23)
    corto = whoosh(0.24, 600, 5000, att=0.5)
    for p in I:
        if p['framing'].startswith('stretto'):
            metti(corto, p['edit_in'] - 0.10, -33)
    if G.get('opening'):
        metti(colpo(1.2, 80, 40), G['opening']['s'] - 0.05, -24)
        metti(w, G['opening']['s'] + 0.05, -29, -0.5)
    if G.get('chip'):
        metti(whoosh(0.35, 500, 4000), G['chip']['s'] - 0.10, -31, -0.5)
    if G.get('closing'):
        metti(whoosh(0.6, 250, 3000), G['closing']['s'] - 0.25, -26)
        metti(colpo(1.4, 70, 36), G['closing']['s'] + 0.05, -22)
        metti(tick(2100), G['closing']['s'] + 1.6, -30)          # il bordo della CTA si chiude

    peak = np.abs(bus).max()
    if peak > 0.5:
        bus *= 0.5 / peak
    sfx = P.asset('sfx.wav')
    _scrivi_wav(sfx, bus)
    print(f"{len(eventi)} suoni sintetizzati -> assets/sfx.wav")

    musica = sorted(p for p in P.asset('musica').glob('*') if p.suffix.lower() in
                    ('.wav', '.mp3', '.m4a', '.aac', '.flac')) if P.asset('musica').is_dir() else []
    voce = P.asset('voce-montata.wav')
    durata = E['frame'] / FPS
    tmp = P.asset('mix-tmp.wav')
    if musica:
        print(f"musica: {musica[0].name} (in loop, -30 LUFS, si abbassa sotto la voce)")
        fc = (f"[2:a]aloop=loop=-1:size=2e9,atrim=0:{durata:.3f},loudnorm=I=-30:TP=-6,"
              f"afade=t=in:d=2,afade=t=out:st={durata - 4:.3f}:d=4[m];"
              f"[0:a]asplit=2[v][vk];[m][vk]sidechaincompress=threshold=0.04:ratio=6:attack=25:release=450[md];"
              f"[v][1:a][md]amix=inputs=3:normalize=0:duration=first[mx]")
        ffmpeg('-i', voce, '-i', sfx, '-stream_loop', '-1', '-i', musica[0], '-filter_complex', fc,
               '-map', '[mx]', '-c:a', 'pcm_s24le', '-ar', '48000', tmp)
    else:
        print("musica: nessun file in assets/musica/, si esce con voce e suoni")
        ffmpeg('-i', voce, '-i', sfx, '-filter_complex',
               '[0:a][1:a]amix=inputs=2:normalize=0:duration=first[mx]',
               '-map', '[mx]', '-c:a', 'pcm_s24le', '-ar', '48000', tmp)
    # guadagno lineare per tornare a -14 (un secondo loudnorm cambierebbe la dinamica)
    got = A.loudness(tmp)
    g = -14.0 - got['I']
    out = P.asset('mix-finale.wav')
    ffmpeg('-i', tmp, '-af', f"volume={g:.2f}dB,alimiter=limit=0.78:level=disabled",
           '-c:a', 'pcm_s24le', '-ar', '48000', out)
    tmp.unlink()
    fin = A.loudness(out)
    print(f"-> assets/mix-finale.wav: {fin['I']} LUFS, true peak {fin['TP']} dBTP")


def _scrivi_wav(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype('<i2')
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())

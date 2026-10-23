"""Fase `shorts`: dai momenti scelti in regia, verticali 9:16 dal 4K.

Un ritaglio verticale a tutta altezza del 4K e 1215x2160: scende a 1080x1920
senza perdere un pixel. Ogni short:

- parte e finisce su frasi intere (`da` / `a` in regia, ancorate al montato),
  quindi eredita tutti i tagli delle papere;
- alterna due tagli verticali (pieno e stretto) a ogni giunta e circa ogni 6 s;
- ha l'hook in alto (fuori dall'interfaccia di Shorts e Reels), i sottotitoli
  grandi al centro-basso, e 1,6 s finali con il rimando al video completo;
- esce a -14 LUFS.

Le zone sicure contano: in basso Shorts mette titolo, pulsanti e descrizione
(~420 px), in alto la barra (~260 px).
"""
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import sys
import time

import numpy as np
from PIL import Image, ImageDraw

from . import stile as S
from . import colore, audio as A
from .progetto import Progetto, FPS, ffmpeg, ts
from .visione import Traccia
from .grafica import piano as GP
from .grafica.render import (sans, mono, tracked_width, draw_tracked, rounded, fade_paste,
                             wrap_to, Sottotitoli)
from .inquadra import candidati
from .monta import X264, _conta_frame

ZV = {'v_pieno': 1.0, 'v_stretto': 1.22}
FACE_YV = {'v_pieno': None, 'v_stretto': 0.30}
CHIUSURA = 1.6


def _intervallo(W, s):
    i0 = GP.ancora(W, s['da'], cosa='short da')
    i1 = GP.ancora(W, s['a'], W[i0]['s'], cosa='short a')
    i1 = i1 + len(s['a'].split()) - 1
    j = GP.fine_frase(W, i1, max_dur=8.0)
    return round(W[i0]['s'] - 0.12, 3), round(W[j]['e'] + 0.35, 3)


def piano_short(P, s, E, tr, W):
    t0, t1 = _intervallo(W, s)
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    seg_f0 = [int(round(x['edit_in'] * FPS)) for x in E['segmenti']]
    parti = []
    for k, sg in enumerate(E['segmenti']):
        a, b = seg_f0[k], seg_f0[k] + sg['n']
        lo, hi = max(a, f0), min(b, f1)
        if hi > lo:
            parti.append({'seg': k, 'f0': lo, 'n': hi - lo,
                          'src_in': round(sg['in'] + (lo - a) / FPS, 6)})
    # cambi di taglio dentro le parti lunghe, ogni ~6 s su una pausa
    C = [int(round(c * FPS)) for c in candidati(W) if t0 < c < t1]
    pezzi = []
    for p in parti:
        cuts = [p['f0']]
        for c in C:
            if cuts[-1] + 5 * FPS < c < p['f0'] + p['n'] - 3 * FPS:
                cuts.append(c)
        cuts.append(p['f0'] + p['n'])
        for a, b in zip(cuts, cuts[1:]):
            pezzi.append({'f0': a, 'n': b - a, 'src_in': round(p['src_in'] + (a - p['f0']) / FPS, 6)})
    m = P.meta()
    SW_, SH_ = m['larghezza'], m['altezza']
    fr = 'v_stretto'
    for p in pezzi:
        fr = 'v_pieno' if fr == 'v_stretto' else 'v_stretto'
        p['framing'] = fr
        z = ZV[fr]
        ch = int(round(SH_ / z / 2)) * 2
        cw = int(round(ch * S.SW / (S.SH - S.SHORT_BAND) / 2)) * 2
        face = tr.mediana(p['src_in'], p['src_in'] + p['n'] / FPS)
        fx, fy, fw, fh = face if face else (SW_ / 2, SH_ / 3, 0, 0)
        x0 = fx + fw / 2 - cw / 2
        y0 = (fy + fh / 2) - FACE_YV[fr] * ch if FACE_YV[fr] else 0
        x0 = int(round(min(max(0, x0), SW_ - cw) / 2)) * 2
        y0 = int(round(min(max(0, y0), SH_ - ch) / 2)) * 2
        p['crop'] = [x0, y0, cw, ch]
    parole = [w for w in W if t0 <= w['s'] < t1]
    caps = _gruppi_v(parole, t0)
    return {'t0': t0, 't1': t1, 'durata': round((f1 - f0) / FPS + CHIUSURA, 3),
            'frame': f1 - f0 + int(round(CHIUSURA * FPS)), 'pezzi': pezzi, 'captions': caps,
            'hook': s['hook'], 'titolo': s['titolo']}


def _gruppi_v(W, t0):
    """in verticale due parole per gruppo, piu grandi"""
    out, cur = [], []
    for w in W:
        w = dict(w, s=round(w['s'] - t0, 3), e=round(w['e'] - t0, 3))
        if cur:
            gap = w['s'] - cur[-1]['e']
            ends = cur[-1]['t'][-1:] in '.!?'
            if len(cur) >= 2 or gap > 0.4 or ends or w['e'] - cur[0]['s'] > 1.6:
                out.append(cur)
                cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    res = []
    for i, g in enumerate(out):
        s, e = g[0]['s'], g[-1]['e'] + 0.1
        if i + 1 < len(out):
            e = min(e, out[i + 1][0]['s'] - 0.01)
        res.append({'s': s, 'e': max(e, s + 0.25), 'words': g})
    return res


class ScenaV:
    def __init__(self, plan):
        self.plan = plan
        self.subs = Sottotitoli(plan['captions'], size=S.SIZE_SHORT['caption'], maxw=S.SW - 120)
        self.hook = self._hook(plan['hook'])
        self.fine = self._fine()
        self.dur_parlato = plan['durata'] - CHIUSURA

    def _hook(self, righe):
        # ogni riga dell'hook sta su una linea sola, dentro la fascia: se non entra
        # si riduce il corpo (in YT_TOFU_02 "IL CAFFÈ NON RISOLVE." andava a capo
        # e la terza riga finiva sopra la barra di avanzamento)
        maxw = S.SW - 2 * 80 - 60
        alto = S.SHORT_BAND - S.SHORT_SAFE_TOP - 24
        size = S.SIZE_SHORT['hook']
        while True:
            f = sans(size, 900)
            tr = S.TRACK['chapter'] * size
            if (all(tracked_width(f, r, tr) <= maxw for r in righe)
                    and len(righe) * int(size * 1.08) + 44 <= alto) or size <= 44:
                break
            size -= 2
        lines = [(r, i) for i, r in enumerate(righe)]
        w = int(max(tracked_width(f, l, tr) for l, _ in lines)) + 64
        h = len(lines) * int(size * 1.08) + 44
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        # sta sulla fascia navy: niente scrim
        d = ImageDraw.Draw(im)
        y = 20
        for l, i in lines:
            lw = tracked_width(f, l, tr)
            draw_tracked(d, ((w - lw) / 2, y - int(size * 0.08)), l, f,
                         (S.PAPER if i == 0 else S.MINT) + (255,), tr)
            y += int(size * 1.08)
        return im

    def _fine(self):
        im = Image.new('RGBA', (S.SW, S.SH), S.NAVY_DEEP + (244,))
        d = ImageDraw.Draw(im)
        fe = mono(S.SIZE_SHORT['eyebrow'])
        tre = S.TRACK['eyebrow'] * S.SIZE_SHORT['eyebrow']
        ft = sans(76, 900)
        y = S.SH // 2 - 160
        for txt, font, col, tr in (("MOBILITAS · STUDIO OSTEOPATICO", fe, S.MINT, tre),):
            w = tracked_width(font, txt, tr)
            draw_tracked(d, ((S.SW - w) / 2, y), txt, font, col + (255,), tr)
        y += 70
        d.rounded_rectangle([S.SW / 2 - 60, y, S.SW / 2 + 60, y + 6], radius=3, fill=S.MINT + (255,))
        y += 50
        for i, l in enumerate(("IL VIDEO COMPLETO", "È SUL CANALE")):
            w = tracked_width(ft, l, -2)
            draw_tracked(d, ((S.SW - w) / 2, y), l, ft, (S.PAPER if i == 0 else S.MINT) + (255,), -2)
            y += 92
        return im

    def frame(self, n):
        t = n / FPS
        base = Image.new('RGBA', (S.SW, S.SH), (0, 0, 0, 0))
        if t < self.dur_parlato:
            p = S.ease_out_expo(t / 0.5)
            # l'hook al centro della parte di fascia sotto la barra di Shorts
            y_hook = S.SHORT_SAFE_TOP + max(0, (S.SHORT_BAND - S.SHORT_SAFE_TOP - 16 - self.hook.height) // 2)
            fade_paste(base, self.hook, ((S.SW - self.hook.width) // 2, y_hook + int((1 - p) * 24)),
                       int(255 * min(1, p * 1.5)))
            self.subs.disegna(base, t, S.SW / 2, S.SHORT_CAPTION_Y)
            # la barra di avanzamento e il filo fra fascia e video
            y = S.SHORT_BAND - 6
            dd = ImageDraw.Draw(base)
            dd.rectangle([0, y, S.SW, y + 6], fill=S.PAPER + (50,))
            dd.rectangle([0, y, int(S.SW * t / self.dur_parlato), y + 6], fill=S.MINT + (235,))
        else:
            a = S.ease_out_cubic((t - self.dur_parlato) / 0.3)
            fade_paste(base, self.fine, (0, 0), int(255 * a))
        return base


def _render_overlay(plan, out_pipe):
    sc = ScenaV(plan)
    for n in range(plan['frame']):
        out_pipe.write(sc.frame(n).tobytes())


def shorts(slug, solo=None, limite=None):
    P = Progetto(slug)
    R = P.regia()
    E = P.leggi('edl.json')
    tr = Traccia(P)
    meta = P.meta()
    W = GP.parole(P, R)          # gia nel formato {'s', 'e', 't'}, con le correzioni
    lista = R.get('shorts', [])
    if not lista:
        print("nessuno short in regia.json")
        return
    idx = [int(x) for x in solo.split(',')] if solo else range(len(lista))
    cartella = P.p('shorts')
    cartella.mkdir(exist_ok=True)
    pezzi_dir = P.render('pezzi-v')
    pezzi_dir.mkdir(exist_ok=True)
    piani = []
    for i in idx:
        s = lista[i]
        pl = piano_short(P, s, E, tr, W)
        print(f"short {i}: {ts(pl['t0'])} -> {ts(pl['t1'])} ({pl['durata']:.1f}s, {len(pl['pezzi'])} pezzi) "
              f"«{s['titolo']}»")
        if pl['durata'] > 180:
            print("  ! oltre 3 minuti: Shorts non lo accetta come short")
        vf_base = []
        files = []
        for k, p in enumerate(pl['pezzi']):
            x, y, w, h = p['crop']
            key = hashlib.sha1(json.dumps([p['src_in'], p['n'], p['crop'], 2, S.SHORT_BAND]).encode()).hexdigest()[:12]
            f = pezzi_dir / f"v-{key}.mp4"
            files.append(f)
            if f.exists():
                continue
            vh = S.SH - S.SHORT_BAND
            vf = f"fps=30000/1001,crop={w}:{h}:{x}:{y},scale=1080:{vh}:flags=lanczos"
            c = colore.catena(meta)
            vf += (',' + c if c else '')
            vf += f",format=yuv420p,pad=1080:1920:0:{S.SHORT_BAND}:color=0x{bytes(S.NAVY_DEEP).hex()}," + colore.filtro_finale()
            ffmpeg('-hwaccel', 'videotoolbox', '-ss', f"{p['src_in']:.6f}", '-i', P.sorgente,
                   '-frames:v', str(p['n']), '-an', '-vf', vf, *X264, '-preset', 'fast', '-crf', '14', f)
        # coda: l'ultimo frame tenuto per la chiusura
        lst = pezzi_dir / f"lista-{i}.txt"
        lst.write_text(''.join(f"file '{f.name}'\n" for f in files))
        base = pezzi_dir / f"base-{i}.mp4"
        ffmpeg('-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', base)
        # audio: la voce gia montata e trattata, nello stesso intervallo
        voce = pezzi_dir / f"voce-{i}.wav"
        d_parl = (pl['frame'] - int(round(CHIUSURA * FPS))) / FPS
        ffmpeg('-ss', f"{pl['t0']:.4f}", '-t', f"{d_parl:.4f}", '-i', P.asset('voce-montata.wav'),
               '-af', f"afade=t=in:d=0.04,afade=t=out:st={d_parl - 0.25:.3f}:d=0.25,apad=pad_dur={CHIUSURA}",
               '-c:a', 'pcm_s24le', voce)
        g = -14.0 - (A.loudness(voce)['I'] or -14.0)
        nome = f"{slug}_short{i + 1}.mp4"
        out = cartella / nome
        cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-y', '-loglevel', 'error',
               '-i', str(base), '-i', str(voce),
               '-f', 'rawvideo', '-pixel_format', 'rgba', '-video_size', f'{S.SW}x{S.SH}',
               '-framerate', '30000/1001', '-i', '-',
               '-filter_complex', f"[0:v]tpad=stop_mode=clone:stop_duration={CHIUSURA}[b];"
                                  f"[b][2:v]overlay=format=auto,{colore.filtro_finale()}[v];"
                                  f"[1:a]volume={g:.2f}dB,alimiter=limit=0.78:level=disabled[a]",
               '-map', '[v]', '-map', '[a]', *X264, '-preset', 'medium', '-crf', '17',
               '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart',
               '-frames:v', str(pl['frame']), str(out)]
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        try:
            _render_overlay(pl, proc.stdin)
        except BrokenPipeError:
            pass
        proc.stdin.close()
        if proc.wait():
            sys.exit(f"short {i} fallito")
        for f in (base, voce, lst):
            f.unlink()
        n = _conta_frame(out)
        print(f"  -> shorts/{nome}: {n} frame, {A.loudness(out)['I']} LUFS")
        pl['file'] = nome
        piani.append(pl)
        _foglio(P, out, i)
    P.scrivi('shorts.json', [{k: v for k, v in p.items() if k != 'captions'} for p in piani])


def _foglio(P, video, i):
    tmp = P.controllo(f'short{i + 1}')
    tmp.mkdir(exist_ok=True)
    for f in tmp.glob('*.jpg'):
        f.unlink()
    d = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                              str(video)], capture_output=True, text=True).stdout.strip())
    for k, t in enumerate(np.linspace(0.8, d - 0.4, 6)):
        ffmpeg('-ss', f"{t:.2f}", '-i', video, '-frames:v', '1', '-vf', 'scale=270:-2', tmp / f"s{k}.jpg")
    ffmpeg('-pattern_type', 'glob', '-i', str(tmp / 's*.jpg'), '-filter_complex', 'tile=6x1:margin=4:padding=3',
           '-frames:v', '1', P.controllo(f'short{i + 1}.jpg'))

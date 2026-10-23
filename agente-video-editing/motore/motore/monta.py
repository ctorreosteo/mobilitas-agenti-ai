"""Fasi `monta` e `finale`.

`monta`: ogni pezzo di `inquadratura.json` si renderizza da solo dalla sorgente
4K (ritaglio, ridimensionamento, colore) e i pezzi si concatenano senza
ricodificare. Pezzi separati vuol dire tre cose: si renderizzano in parallelo,
un pezzo uguale non si rifa (cache sul contenuto), e una correzione di
inquadratura costa secondi invece di un render intero.

`finale`: montato pulito + livello grafico in pipe (RGBA grezzo) + voce e
sound design mixati -> master.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import sys
import time

from .progetto import Progetto, FPS, ffmpeg, esegui
from . import colore, audio as A

X264 = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
        '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']


def _vf(p, meta):
    x, y, w, h = p['crop']
    parts = ['fps=30000/1001']
    if [x, y, w, h] != [0, 0, meta['larghezza'], meta['altezza']]:
        parts.append(f"crop={w}:{h}:{x}:{y}")
    parts.append("scale=1920:1080:flags=lanczos")
    c = colore.catena(meta)
    if c:
        parts.append(c)
    parts.append(colore.filtro_finale())
    return ','.join(parts)


def _chiave(p, meta, crf):
    s = json.dumps([p['src_in'], p['n'], p['crop'], meta['colore'], meta['sorgente'], crf, 2])
    return hashlib.sha1(s.encode()).hexdigest()[:12]


def _conta_frame(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets',
                        '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', str(path)],
                       capture_output=True, text=True)
    return int((r.stdout.strip().split(',')[0]) or 0)


def monta(slug, solo=None, crf=14):
    P = Progetto(slug)
    meta = P.meta()
    I = P.leggi('inquadratura.json')['pezzi']
    E = P.leggi('edl.json')
    cartella = P.render('pezzi')
    cartella.mkdir(exist_ok=True)
    solo = {int(x) for x in solo.split(',')} if solo else None
    todo = []
    for k, p in enumerate(I):
        p['file'] = f"p{k:03d}-{_chiave(p, meta, crf)}.mp4"
        path = cartella / p['file']
        forza = solo is not None and k in solo
        if forza and path.exists():
            path.unlink()
        if not path.exists():
            todo.append((k, p))

    # i nomi dei pezzi si scrivono PRIMA del render: se si scrivessero dopo,
    # inquadratura.json risulterebbe piu recente del montato e `stato` lo darebbe da rifare
    P.scrivi('inquadratura.json', {'sorgente': [meta['larghezza'], meta['altezza']], 'pezzi': I})

    def one(kp):
        k, p = kp
        out = cartella / p['file']
        tmp = cartella / (p['file'] + '.tmp.mp4')
        ffmpeg('-hwaccel', 'videotoolbox', '-ss', f"{p['src_in']:.6f}", '-i', P.sorgente,
               '-frames:v', str(p['n']), '-an', '-vf', _vf(p, meta), *X264,
               '-preset', 'fast', '-crf', str(crf),
               '-x264-params', 'keyint=60:min-keyint=30:bframes=3:ref=3', tmp)
        n = _conta_frame(tmp)
        if n != p['n']:
            tmp.unlink()
            raise RuntimeError(f"pezzo {k}: {n} frame invece di {p['n']}")
        os.replace(tmp, out)
        return k

    t0 = time.time()
    print(f"{len(I)} pezzi, {len(todo)} da renderizzare dal 4K ({len(I) - len(todo)} gia pronti in cache)...")
    done = 0
    with cf.ThreadPoolExecutor(2) as ex:
        for k in ex.map(one, todo):
            done += 1
            if done % 10 == 0 or done == len(todo):
                el = time.time() - t0
                print(f"  {done}/{len(todo)} pezzi, {el/60:.1f} min")
    lista = cartella / 'lista.txt'
    lista.write_text(''.join(f"file '{p['file']}'\n" for p in I))
    video = P.render(f"{slug}_pulito_video.mp4")
    ffmpeg('-f', 'concat', '-safe', '0', '-i', lista, '-c', 'copy', video)
    out = P.render(f"{slug}_pulito.mp4")
    ffmpeg('-i', video, '-i', P.asset('voce-montata.wav'), '-map', '0:v', '-map', '1:a',
           '-c:v', 'copy', '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', out)
    video.unlink()
    n = _conta_frame(out)
    print(f"-> renders/{out.name}: {n} frame (attesi {E['frame']})")
    if n != E['frame']:
        sys.exit("  !!! il numero di frame non torna con l'EDL: audio e video non sono allineati")
    # pulizia dei pezzi orfani di render precedenti
    validi = {p['file'] for p in I}
    for f in cartella.glob('p*.mp4'):
        if f.name not in validi:
            f.unlink()
    foglio_inquadrature(P, out, I)


def foglio_inquadrature(P, video, I):
    """un fotogramma per pezzo, in un foglio: il colpo d'occhio sul ritmo delle camere"""
    tmp = P.controllo('inquadrature')
    tmp.mkdir(exist_ok=True)
    for f in tmp.glob('*.jpg'):
        f.unlink()

    def grab(kp):
        k, p = kp
        t = p['edit_in'] + min(1.0, p['n'] / FPS / 2)
        ffmpeg('-ss', f"{t:.3f}", '-i', video, '-frames:v', '1', '-vf',
               f"scale=384:-2,drawbox=x=0:y=0:w=iw:h=18:color=black@0.6:t=fill", tmp / f"q{k:03d}.jpg")

    with cf.ThreadPoolExecutor(6) as ex:
        list(ex.map(grab, enumerate(I)))
    cols = 8
    rows = -(-len(I) // cols)
    ffmpeg('-pattern_type', 'glob', '-i', str(tmp / 'q*.jpg'), '-filter_complex',
           f'tile={cols}x{rows}:margin=4:padding=3', '-frames:v', '1', P.controllo('inquadrature.jpg'))
    print(f"-> controlli/inquadrature.jpg ({len(I)} pezzi, uno per riquadro)")


def finale(slug, limite=None):
    from .grafica import render as R
    P = Progetto(slug)
    E = P.leggi('edl.json')
    pulito = P.render(f"{slug}_pulito.mp4")
    mix = P.asset('mix-finale.wav')
    if not mix.exists():
        sys.exit("manca assets/mix-finale.wav: lancia prima `suono`")
    out = P.render(f"{slug}_FINALE.mp4" if not limite else f"{slug}_prova.mp4")
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-y', '-loglevel', 'error', '-stats',
           '-i', str(pulito), '-i', str(mix),
           '-f', 'rawvideo', '-pixel_format', 'rgba', '-video_size', '1920x1080',
           '-framerate', '30000/1001', '-i', '-',
           '-filter_complex', f"[0:v][2:v]overlay=format=auto:shortest=0:eof_action=pass,{colore.filtro_finale()}[v]",
           '-map', '[v]', '-map', '1:a', *X264, '-preset', os.environ.get('PRESET', 'medium'),
           '-crf', os.environ.get('CRF', '17'), '-x264-params', 'keyint=60:min-keyint=30:bframes=3:ref=4',
           '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2', '-movflags', '+faststart']
    if limite:
        cmd += ['-t', str(limite)]
    cmd.append(str(out))
    env = dict(os.environ)
    gen = subprocess.Popen([sys.executable, '-m', 'motore.grafica.render', slug] +
                           ([str(limite)] if limite else []), stdout=subprocess.PIPE, env=env)
    rc = subprocess.call(cmd, stdin=gen.stdout)
    gen.stdout.close()
    gen.wait()
    if rc:
        sys.exit(f"render finale fallito ({rc})")
    print(f"-> renders/{out.name}")

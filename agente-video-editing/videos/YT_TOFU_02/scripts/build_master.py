#!/usr/bin/env python3
"""Monta il master 1080p dall'EDL.

Ogni giunta e una dissolvenza di 5 frame invece di uno stacco secco: la
macchina e fissa e il soggetto si sposta durante le pause, quindi lo stacco
netto si leggerebbe come uno scatto. 5 frame bastano a coprirlo senza che la
dissolvenza si noti come effetto.
"""
import json, os, subprocess, sys

FPS = 30000 / 1001.0
XF = round(5 / FPS, 4)          # 5 frame
FADE_IO = 0.6                   # apertura e chiusura del montato

VIDEO_SRC = 'assets/intermediate-1080p-sdr.mp4'
AUDIO_SRC = 'assets/audio-48k.wav'


def build(segs, out_path, preview=False, overlay=False):
    p, vl, al = [], [], []
    for i, (a, b) in enumerate(segs):
        p.append(f"[0:v]trim=start={a:.4f}:end={b:.4f},setpts=PTS-STARTPTS,fps={FPS:.6f}[v{i}]")
        p.append(f"[1:a]atrim=start={a:.4f}:end={b:.4f},asetpts=PTS-STARTPTS[a{i}]")
        vl.append(f"v{i}")
        al.append(f"a{i}")

    # catena di dissolvenze
    dur = [b - a for a, b in segs]
    acc = dur[0]
    cur_v, cur_a = vl[0], al[0]
    for i in range(1, len(segs)):
        off = acc - XF
        nv, na = f"vx{i}", f"ax{i}"
        p.append(f"[{cur_v}][{vl[i]}]xfade=transition=fade:duration={XF}:offset={off:.4f}[{nv}]")
        p.append(f"[{cur_a}][{al[i]}]acrossfade=d={XF}:c1=tri:c2=tri[{na}]")
        cur_v, cur_a = nv, na
        acc += dur[i] - XF

    total = acc
    p.append(f"[{cur_v}]setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709,"
             f"fade=t=in:st=0:d={FADE_IO},fade=t=out:st={total-FADE_IO:.3f}:d={FADE_IO},"
             f"format=yuv420p[vout]")
    p.append(f"[{cur_a}]highpass=f=75,"
             "afftdn=nr=10:nf=-34:tn=1,"
             "deesser=i=0.3,"
             "acompressor=threshold=-20dB:ratio=2.5:attack=12:release=200:makeup=2,"
             "loudnorm=I=-14:TP=-1.5:LRA=9,"
             "alimiter=limit=0.89:level=disabled,"
             f"afade=t=in:st=0:d=0.25,afade=t=out:st={total-0.5:.3f}:d=0.5,"
             "aresample=48000[aout]")

    if overlay:
        # il livello grafico arriva in RGBA grezzo su una pipe: questo ffmpeg non
        # ha ne libass ne drawtext, il testo va rasterizzato fuori
        p[-2] = p[-2].replace('[vout]', '[vbase]')
        p.append(f"[vbase][2:v]overlay=shortest=0:format=auto,format=yuv420p[vout]")

    script = 'data/filtergraph.txt'
    open(script, 'w').write(';'.join(p))

    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-stats',
           '-i', VIDEO_SRC, '-i', AUDIO_SRC]
    if overlay:
        cmd += ['-f', 'rawvideo', '-pixel_format', 'rgba',
                '-video_size', f'{1920}x{1080}', '-framerate', '30000/1001', '-i', '-']
    cmd += ['-/filter_complex', script,
           '-map', '[vout]', '-map', '[aout]',
           '-c:v', 'libx264',
           '-preset', 'veryfast' if preview else os.environ.get('PRESET', 'fast'),
           '-crf', '20' if preview else os.environ.get('CRF', '17'),
           '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '4.1',
           '-x264-params', 'keyint=60:min-keyint=30:bframes=3:ref=4',
           '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
           '-color_range', 'tv',
           '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
           '-movflags', '+faststart']
    if os.environ.get('LIMIT_T'):
        cmd += ['-t', os.environ['LIMIT_T']]
    cmd += ['-y', out_path]
    print(f"{len(segs)} segmenti, durata attesa {total:.2f}s ({total/60:.2f} min)")
    if not overlay:
        return subprocess.call(cmd)
    gen = subprocess.Popen(['.venv/bin/python', 'scripts/render_overlay.py'],
                           stdout=subprocess.PIPE)
    rc = subprocess.call(cmd, stdin=gen.stdout)
    gen.stdout.close()
    gen.wait()
    return rc


if __name__ == '__main__':
    edl = json.load(open('data/edl.json'))
    segs = [(s['in'], s['out']) for s in edl['segments']]
    if '--preview' in sys.argv:
        segs = segs[:6]
    sys.exit(build(segs, sys.argv[1], preview='--preview' in sys.argv,
                   overlay='--overlay' in sys.argv))

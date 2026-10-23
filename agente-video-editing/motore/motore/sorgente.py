"""Fasi `init` e `prep`: dal file di camera a un progetto pronto da analizzare."""
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from .progetto import VIDEOS, Progetto, scrivi, ffmpeg, esegui
from . import audio, colore


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_streams',
                          '-show_format', str(path)], capture_output=True, text=True)
    d = json.loads(out.stdout)
    v = next(s for s in d['streams'] if s['codec_type'] == 'video')
    a = next((s for s in d['streams'] if s['codec_type'] == 'audio'), None)
    rot = 0
    for sd in v.get('side_data_list', []):
        if 'rotation' in sd:
            rot = int(sd['rotation'])
    w, h = int(v['width']), int(v['height'])
    if abs(rot) % 180 == 90:
        w, h = h, w
    num, den = (int(x) for x in v['r_frame_rate'].split('/'))
    trc = v.get('color_transfer', '')
    colore_ = 'hlg' if trc == 'arib-std-b67' else 'pq' if trc == 'smpte2084' else 'sdr'
    return {
        'larghezza': w, 'altezza': h, 'rotazione': rot,
        'fps': round(num / den, 3), 'fps_raw': v['r_frame_rate'],
        'codec': v['codec_name'], 'profilo': v.get('profile'), 'pix_fmt': v.get('pix_fmt'),
        'colore': colore_, 'trc': trc, 'primarie': v.get('color_primaries', ''),
        'durata': float(d['format']['duration']),
        'audio': bool(a), 'audio_canali': a.get('channels') if a else 0,
        'peso_gb': round(int(d['format']['size']) / 1e9, 2),
    }


def init(file, slug=None):
    src = Path(file).expanduser().resolve()
    if not src.exists():
        sys.exit(f"file non trovato: {src}")
    slug = slug or re.sub(r'[^\w-]+', '-', src.stem).strip('-')
    d = VIDEOS / slug
    d.mkdir(parents=True, exist_ok=True)
    link = d / f"sorgente{src.suffix}"
    if src.parent != d:
        if link.is_symlink() or link.exists():
            link.unlink()
        os.symlink(src, link)            # mai spostare il girato: si collega
    else:
        link = src
    info = probe(src)
    meta = {'slug': slug, 'sorgente': link.name, 'originale': str(src),
            'creato': datetime.datetime.now().isoformat(timespec='seconds'), **info}
    scrivi(d / 'meta.json', meta)
    print(f"progetto {slug}: {info['larghezza']}x{info['altezza']} {info['fps']}p "
          f"{info['codec']} {info['colore'].upper()}, {info['durata']/60:.1f} min, "
          f"rotazione {info['rotazione']}")
    if info['altezza'] < 2160:
        print("  ! sorgente sotto il 4K: i punch-in verranno limitati per non ingrandire oltre i pixel nativi")
    return slug


def prep(slug):
    P = Progetto(slug)
    src = P.sorgente
    m = P.meta()
    # analisi: mono 16k grezzo (per l'inviluppo il livello vero conta)
    if not P.asset('audio-16k-mono.wav').exists():
        ffmpeg('-i', src, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le',
               P.asset('audio-16k-mono.wav'))
    # riconoscimento: normalizzato a -20, o whisper puo degenerare in loop
    if not P.asset('audio-16k-asr.wav').exists():
        ffmpeg('-i', src, '-vn', '-af', 'highpass=f=70,loudnorm=I=-20:TP=-2', '-ac', '1',
               '-ar', '16000', '-c:a', 'pcm_s16le', P.asset('audio-16k-asr.wav'))
    # master: 48k a 24 bit, nessun trattamento (la catena voce sta nel montaggio)
    if not P.asset('audio-48k.wav').exists():
        ffmpeg('-i', src, '-vn', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s24le',
               P.asset('audio-48k.wav'))
    if m['colore'] == 'hlg':
        print(f"LUT HLG -> BT.709: {colore.lut_hlg()}")
    blocchi, floor, thr = audio.blocchi(P.asset('audio-16k-mono.wav'))
    P.scrivi('blocchi.json', blocchi)
    lufs = audio.loudness(P.asset('audio-48k.wav'))
    m.update({'fondo_sala_db': round(floor, 1), 'soglia_parlato_db': round(thr, 1),
              'lufs_sorgente': lufs})
    scrivi(P.p('meta.json'), m)
    print(f"audio: {lufs['I']} LUFS, true peak {lufs['TP']} dBTP; fondo di sala {floor:.1f} dBFS")
    print(f"{len(blocchi)} blocchi di parlato -> data/blocchi.json")

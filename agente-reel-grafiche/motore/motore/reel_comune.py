"""Pezzi comuni dell'agente reel-grafiche (fase 4, 04/11/2026): dove stanno i file di un ad, la cartella di
lavoro privata, le parole dette, Apple Vision per il testo.

Regola di costruzione (Riccardo, 04/11/2026): ogni ad lavora solo in `videos/<slug>/` e in
`.lavoro/<slug>/`. Un ad non legge né scrive i file di lavoro di un altro, così due ad possono
andare in parallelo; ognuno svuota solo la sua cartella. Il catalogo dei modelli qui si legge e basta.

File di un ad (`videos/<slug>/`):
- `reel.json`: da dove viene il video (lo scrive `reel-init`);
- `radiografia.json` / `radiografia.md` / `radiografia/`: le misure (`reel-radiografia`); il blocco
  `animazioni_3d` lo scrive l'agente con `reel-3d` dopo aver guardato i provini;
- `piano.json`: le grafiche. È **l'unico file che l'agente scrive a mano**;
- `piano/`: tavola visiva e riepilogo (`reel-piano`);
- `approvazioni.json`: le approvazioni di Riccardo, legate all'md5 di quello che ha visto (`reel-approva`);
- `anteprime/`, `controlli/`: video di lavoro, anteprime, provini, controlli automatici (`reel-rendi`);
- `voti.json`: voti del direttore artistico (`reel-voto`); `verifiche.json`: le letture di Vision
  guardate dall'agente (`reel-guardato`);
- `consegna/`: il video consegnato e `consegna.md` (`reel-consegna`).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from .progetto import AGENTE, CACHE, INBOX, VIDEOS

W, H = 1080, 1920
SAFE = (65, 269, 1014, 1247)          # zona sicura Meta per i testi, x0 y0 x1 y1 inclusi (14% sopra, 35% sotto, 6% ai lati)
TESTO_SWIFT = AGENTE / 'motore' / 'swift' / 'testo.swift'


def cartella(slug):
    return VIDEOS / slug


def lavoro(slug, *parti):
    """la cartella di lavoro privata dell'ad: .lavoro/<slug>/... (creata). Anche i temporanei di
    Python e dei programmi lanciati da qui vanno nella sua tmp/, non in quella comune"""
    d = AGENTE / '.lavoro' / slug
    t = d / 'tmp'
    t.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(t)
    os.environ['TMPDIR'] = str(t)
    p = d.joinpath(*parti) if parti else d
    p.mkdir(parents=True, exist_ok=True)
    return p


def leggi(p, default=None):
    p = Path(p)
    if not p.exists():
        if default is not None:
            return default
        sys.exit(f"manca {p.relative_to(AGENTE) if p.is_relative_to(AGENTE) else p}")
    return json.loads(p.read_text(encoding='utf-8'))


def scrivi(p, obj):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding='utf-8')
    os.replace(tmp, p)


def md5_file(p):
    h = hashlib.md5()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def sorgente(slug):
    """i file dell'ad (assoluti): video, srt, mp3 (se c'è)"""
    a = leggi(cartella(slug) / 'reel.json')
    return {k: (AGENTE / v if v else None) for k, v in a['sorgente'].items()}


def rel(p):
    p = Path(p)
    return str(p.relative_to(AGENTE)) if p.is_absolute() and p.is_relative_to(AGENTE) else str(p)


def probe(video):
    r = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-show_entries',
                                   'stream=index,codec_type,codec_name,profile,width,height,pix_fmt,r_frame_rate,nb_read_packets,'
                                   'color_space,color_transfer,color_primaries,color_range,sample_rate,channels,bit_rate:format=duration,size',
                                   '-of', 'json', str(video)], capture_output=True, text=True, check=True).stdout)
    v = next(s for s in r['streams'] if s['codec_type'] == 'video')
    a = next((s for s in r['streams'] if s['codec_type'] == 'audio'), None)
    n, d = v['r_frame_rate'].split('/')
    fps = int(n) // int(d) if int(n) % int(d) == 0 else round(int(n) / int(d), 6)   # 30, non 30.0 (HyperFrames lo rifiuta)
    return {'larghezza': v['width'], 'altezza': v['height'], 'fps': fps, 'fotogrammi': int(v['nb_read_packets']),
            'durata': float(r['format']['duration']), 'video': {k: v.get(k) for k in ('codec_name', 'profile', 'pix_fmt', 'color_space',
                                                                                         'color_transfer', 'color_primaries', 'color_range')},
            'audio': {k: a.get(k) for k in ('codec_name', 'profile', 'sample_rate', 'channels', 'bit_rate')} if a else None,
            'byte': int(r['format']['size'])}


def md5_audio(f):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-map', '0:a', '-c', 'copy', '-f', 'md5', '-'],
                       capture_output=True, text=True, check=True)
    return r.stdout.strip().split('=')[-1]


def fotogrammi_rgb(video, vf=None, w=W, h=H):
    """generatore di fotogrammi RGB (numpy) dal video, con la conversione BT.709 range tv esplicita"""
    import numpy as np
    f = 'scale=in_color_matrix=bt709:in_range=tv:out_range=full:flags=accurate_rnd+full_chroma_int'
    vf = f"{vf},{f}" if vf else f
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(video), '-vf', vf, '-fps_mode', 'passthrough',
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = w * h * 3
    try:
        while True:
            b = p.stdout.read(n)
            if len(b) < n:
                break
            yield np.frombuffer(b, np.uint8).reshape(h, w, 3)
    finally:
        if p.poll() is None:
            p.kill()             # chi legge si e fermato prima della fine: niente «broken pipe»
        p.wait()


def estrai(video, frames, scala=None):
    """{f: PIL RGB} per i fotogrammi dati, in una sola passata (un'espressione select con centinaia di termini
    manda ffmpeg fuori memoria: si decodifica tutto e si tengono quelli chiesti)"""
    from PIL import Image
    voluti = set(frames)
    if not voluti:
        return {}
    w, h = scala or (W, H)
    out = {}
    vf = f"scale={w}:{h}:flags=lanczos" if scala else None
    for k, a in enumerate(fotogrammi_rgb(video, vf=vf, w=w, h=h)):
        if k in voluti:
            out[k] = Image.fromarray(a.copy())
        if k >= max(voluti):
            break
    return out


def fotogramma(video, f, out=None):
    """un fotogramma (numero f) come immagine PIL RGB"""
    from PIL import Image
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-vf',
                        f'select=eq(n\\,{f}),scale=in_color_matrix=bt709:in_range=tv:out_range=full', '-frames:v', '1',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    im = Image.frombytes('RGB', (W, H), b)
    if out:
        im.save(out)
    return im


# ---------------------------------------------------------------- Apple Vision (testo)

def vision_bin():
    """testo.swift compilato una volta in .cache/ (si ricompila solo se cambia il sorgente)"""
    h = md5_file(TESTO_SWIFT)[:10]
    b = CACHE / f'reel-testo-{h}'
    if not b.exists():
        CACHE.mkdir(exist_ok=True)
        tmp = CACHE / f'reel-testo-{h}.{os.getpid()}'
        env = dict(os.environ, TMPDIR=os.environ.get('TMPDIR', str(CACHE)))
        subprocess.run(['swiftc', '-O', '-suppress-warnings', str(TESTO_SWIFT), '-o', str(tmp)], check=True, env=env,
                       capture_output=True)
        os.replace(tmp, b)
    return b


def vision(cartella_png, out_json, y_offset=0):
    """Apple Vision (accurato, it-IT, senza correzione) su ogni PNG della cartella -> {file: [righe]}"""
    subprocess.run([str(vision_bin()), str(cartella_png), str(out_json), str(y_offset)], check=True, capture_output=True,
                   env={'TMPDIR': os.environ.get('TMPDIR', '/nonesiste'), 'PATH': '/usr/bin:/bin'})
    return {x['file']: x.get('obs', []) for x in json.loads(Path(out_json).read_text())}


# ---------------------------------------------------------------- parole dette

NUMERI = {'due': '2', 'tre': '3', 'quattro': '4', 'cinque': '5', 'sei': '6', 'sette': '7', 'otto': '8', 'nove': '9',
          'dieci': '10', 'venti': '20', 'trenta': '30', 'cento': '100'}
ORDINALI = {'primo': '1', 'prima': '1', 'secondo': '2', 'seconda': '2', 'terzo': '3', 'terza': '3', 'quarto': '4',
            'quarta': '4', 'quinto': '5', 'quinta': '5'}
SIMBOLI_AMMESSI = set('+=€')


def norm(w):
    """una parola come si confronta: minuscole, senza punteggiatura ai lati (restano lettere accentate,
    apostrofi interni, cifre, €)"""
    w = w.lower().replace('’', "'").replace('‘', "'")
    return re.sub(r"^[^\w€]+|[^\w€]+$", '', w)


def parole_di(testo):
    """le parole di un testo, normalizzate; «un'ora» dà anche «un» e «ora»; «€49» dà «€49», «49» ed «euro»"""
    out = []
    for w in re.split(r'\s+', testo.replace('|', ' ').replace('*', ' ')):
        k = norm(w)
        if not k:
            continue
        out.append(k)
        if "'" in k:
            out += [p for p in k.split("'") if p]
        if '€' in k:
            out += [p for p in k.split('€') if p] + ['euro']
    return out


def numeri_detti(parole):
    """i numeri che la voce dice: cifre scritte nell'SRT, numeri e ordinali in lettere"""
    n = set()
    for w in parole:
        n |= set(re.findall(r'\d+', w))
        if w in NUMERI:
            n.add(NUMERI[w])
        if w in ORDINALI:
            n.add(ORDINALI[w])
    return n


def leggi_srt(p):
    """[{n, a, b, t}] dall'SRT (tempi in secondi)"""
    txt = Path(p).read_text(encoding='utf-8-sig').replace('\r\n', '\n')
    out = []
    for blocco in re.split(r'\n\s*\n', txt.strip()):
        r = blocco.strip().split('\n')
        if len(r) < 2:
            continue
        m = re.match(r'(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)', r[1])
        if not m:
            continue
        g = [int(x) for x in m.groups()]
        a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000
        b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
        out.append({'n': int(r[0]), 'a': round(a, 3), 'b': round(b, 3), 't': ' '.join(r[2:])})
    return out


def trova_inbox():
    """gli ad in inbox/: cartelle con un video 9:16 e un SRT"""
    out = []
    for d in sorted(p for p in INBOX.iterdir() if p.is_dir()) if INBOX.exists() else []:
        mp4 = sorted(d.glob('*.mp4')) + sorted(d.glob('*.mov'))
        srt = sorted(d.glob('*.srt'))
        if not mp4:
            continue
        try:
            pr = probe(mp4[0])
        except subprocess.CalledProcessError:
            continue
        if (pr['larghezza'], pr['altezza']) != (W, H):
            continue
        out.append({'slug': d.name, 'cartella': d, 'video': mp4[0], 'srt': srt[0] if srt else None,
                    'mp3': (sorted(d.glob('*.mp3')) or [None])[0]})
    return out

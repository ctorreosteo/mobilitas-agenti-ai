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

from .progetto import Progetto, ffmpeg, esegui, lavori
from . import colore, audio as A
from . import stile as S

FILETTO = 6           # px del filetto blu notte fra due clip affiancate

X264 = ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
        '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']


def _vf(p, meta, fps_str):
    x, y, w, h = p['crop']
    parts = [f'fps={fps_str}']
    if [x, y, w, h] != [0, 0, meta['larghezza'], meta['altezza']]:
        parts.append(f"crop={w}:{h}:{x}:{y}")
    parts.append("scale=1920:1080:flags=lanczos")
    c = colore.catena(meta)
    if c:
        parts.append(c)
    parts.append(colore.filtro_finale())
    return ','.join(parts)


def _broll_cmd(p, fps, fps_str, out, crf):
    """un pezzo di B-roll dalla libreria. Fino a 1,25x l'uscita (30 -> 25) ogni
    fotogramma sorgente diventa un fotogramma d'uscita: rallentato, nessuno scartato.
    Oltre (50 -> 25) o sotto, velocita normale. Sempre muto."""
    from fractions import Fraction
    from .progetto import LIBRERIA
    b = p['broll']
    ins, rami = [], []
    for k, c in enumerate(b['clip']):
        src_fps = float(Fraction(c['fps']))
        lento = 1.0 < src_fps / fps <= 1.25
        passo = 1 / src_fps if lento else 1 / fps
        start = c['src_in'] + b['offset'] * passo
        start = max(0.0, min(start, c['durata'] - p['n'] * passo - 0.05))
        ins += ['-ss', f"{start:.4f}", '-i', str(LIBRERIA / c['file'])]
        vel = f"setpts=N/({fps_str}*TB)" if lento else f"fps={fps_str}"
        if b['layout'] == 'affiancati':
            rami.append(f"[{k}:v]{vel},scale=-2:1080:flags=lanczos,crop=960:1080:(iw-960)/2:0[c{k}]")
        else:
            rami.append(f"[{k}:v]{vel},scale=1920:1080:flags=lanczos,crop=1920:1080[c{k}]")
    if b['layout'] == 'affiancati':
        n = len(b['clip'])
        # un filetto blu notte fra le clip: senza, i due quadri si fondono (cartelli, sfondi)
        blu = S.BRAND['colori']['blu_notte']['hex'].replace('#', '0x')
        fil = ''.join(f",drawbox=x={k * 1920 // n - FILETTO // 2}:y=0:w={FILETTO}:h=1080:color={blu}@1:t=fill"
                      for k in range(1, n))
        rami.append(''.join(f"[c{k}]" for k in range(n)) + f"hstack=inputs={n}{fil}[st]")
        ultimo = 'st'
    else:
        ultimo = 'c0'
    rami.append(f"[{ultimo}]format=yuv420p,{colore.filtro_finale()}[v]")
    return ins + ['-filter_complex', ';'.join(rami), '-map', '[v]', '-frames:v', str(p['n']), '-an',
                  '-r', fps_str, *X264, '-preset', 'fast', '-crf', str(crf)]


def _chiave(p, meta, crf):
    s = json.dumps([p['src_in'], p['n'], p['crop'], meta['colore'], meta['sorgente'], crf, 2]
                   + ([p['broll'], FILETTO] if p.get('broll') else []))
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
        if p.get('broll'):
            ffmpeg(*_broll_cmd(p, P.fps, P.fps_str, tmp, crf), '-x264-params', f'{P.gop}:bframes=3:ref=3', tmp)
        else:
            ffmpeg('-hwaccel', 'videotoolbox', '-ss', f"{p['src_in']:.6f}", '-i', P.sorgente,
                   '-frames:v', str(p['n']), '-an', '-vf', _vf(p, meta, P.fps_str), *X264,
                   '-preset', 'fast', '-crf', str(crf),
                   '-x264-params', f'{P.gop}:bframes=3:ref=3', tmp)
        n = _conta_frame(tmp)
        if n != p['n']:
            tmp.unlink()
            raise RuntimeError(f"pezzo {k}: {n} frame invece di {p['n']}")
        os.replace(tmp, out)
        return k

    t0 = time.time()
    print(f"{len(I)} pezzi, {len(todo)} da renderizzare dal 4K ({len(I) - len(todo)} gia pronti in cache)...")
    done = 0
    with cf.ThreadPoolExecutor(lavori(2)) as ex:
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
        t = p['edit_in'] + min(1.0, p['n'] / P.fps / 2)
        ffmpeg('-ss', f"{t:.3f}", '-i', video, '-frames:v', '1', '-vf',
               f"scale=384:-2,drawbox=x=0:y=0:w=iw:h=18:color=black@0.6:t=fill", tmp / f"q{k:03d}.jpg")

    with cf.ThreadPoolExecutor(lavori(6)) as ex:
        list(ex.map(grab, enumerate(I)))
    cols = 8
    rows = -(-len(I) // cols)
    ffmpeg('-pattern_type', 'glob', '-i', str(tmp / 'q*.jpg'), '-filter_complex',
           f'tile={cols}x{rows}:margin=4:padding=3', '-frames:v', '1', P.controllo('inquadrature.jpg'))
    print(f"-> controlli/inquadrature.jpg ({len(I)} pezzi, uno per riquadro)")


def finale(slug, limite=None, anteprima=False):
    """master: montato pulito + inserti HyperFrames (MOV con alfa, ognuno al suo
    istante) + livello Pillow in pipe (sopra a tutto: sottotitoli, chip) + mix.
    Con --anteprima: stesso montaggio a 960x540, codifica veloce, piu il foglio
    dei momenti principali e l'elenco dei tempi: e la versione da approvare."""
    from .grafica import render as R
    P = Progetto(slug)
    E = P.leggi('edl.json')
    pulito = P.render(f"{slug}_pulito.mp4")
    mix = P.asset('mix-finale.wav')
    if not mix.exists():
        sys.exit("manca assets/mix-finale.wav: lancia prima `suono`")
    U = P.leggi('inserti.json', []) if P.data('inserti.json').exists() else []
    G = P.leggi('grafica.json')
    if G.get('inserti') and len(U) != len(G['inserti']):
        sys.exit("gli inserti non tornano con il piano grafico: lancia prima `inserti`")
    nome = f"{slug}_anteprima.mp4" if anteprima else (f"{slug}_prova.mp4" if limite else f"{slug}_FINALE.mp4")
    out = P.render(nome)
    ingressi, rami, cur = [], [], '0:v'
    for k, u in enumerate(U):
        ingressi += ['-i', str(P.p(u['file']))]
        rami.append(f"[{k + 3}:v]setpts=PTS-STARTPTS+{int(round(u['s'] * P.fps))}/({P.fps_str}*TB)[i{k}];"
                    f"[{cur}][i{k}]overlay=format=auto:eof_action=pass:shortest=0[o{k}]")
        cur = f"o{k}"
    coda = f"[{cur}][2:v]overlay=format=auto:shortest=0:eof_action=pass,{colore.filtro_finale()}"
    if anteprima:
        coda += ",scale=960:540:flags=bicubic"
    fc = ';'.join(rami + [coda + '[v]'])
    qual = (['-preset', 'veryfast', '-crf', '23'] if anteprima else
            ['-preset', os.environ.get('PRESET', 'medium'), '-crf', os.environ.get('CRF', '17')])
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-y', '-loglevel', 'error', '-stats',
           '-i', str(pulito), '-i', str(mix),
           '-f', 'rawvideo', '-pixel_format', 'rgba', '-video_size', '1920x1080',
           '-framerate', P.fps_str, '-i', '-', *ingressi,
           '-filter_complex', fc,
           '-map', '[v]', '-map', '1:a', *X264, *qual, '-x264-params', f'{P.gop}:bframes=3:ref=4',
           '-c:a', 'aac', '-b:a', '128k' if anteprima else '192k', '-ar', '48000', '-ac', '2',
           '-movflags', '+faststart']
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
    if anteprima:
        foglio_anteprima(P, out, G)
        if P.data('scena.json').exists():
            from .schede import anteprima_momenti
            anteprima_momenti(P, out)
        from .qc import controlli_contenuto
        righe = controlli_contenuto(P, G)
        for n, at, m, e in righe:
            print(f"  {e:<7} {n:<36} {m}")
        print("-> controlli/contenuto.md" + ("" if all(r[3] != 'ERRORE' for r in righe) else "  !!! ci sono ERRORI"))


def elementi(G):
    """tutto cio che compare a schermo oltre alla persona, in ordine di tempo"""
    el = []
    if G.get('chip'):
        el.append(('chip', G['chip']['s'], G['chip']['e'], f"{G['chip']['name']} / {G['chip']['role']}"))
    for c in G.get('frasi_chiave', []):
        el.append(('frase chiave', c['s'], c['e'], c['testo']))
    for x in G.get('inserti', []):
        el.append((f"inserto {x['modello']}", x['s'], x['e'], ' · '.join(x.get('testi', [])[:4])))
    for b in G.get('broll', []):
        el.append((f"B-roll {b['layout']}", b['s'], b['e'], ' + '.join(c['file'] for c in b['clip'])))
    for c in G.get('cards', []):
        el.append(('card', c['s'], c['e'], f"{c['value']}{c['unit']} {c['eyebrow']}"))
    return sorted(el, key=lambda e: e[1])


def foglio_anteprima(P, video, G):
    """un fotogramma per elemento (a meta, o a 1,5 s dall'inizio se e lungo) e
    l'elenco dei tempi, per guardare l'anteprima con il piano a fianco"""
    from PIL import Image, ImageDraw
    from .grafica.render import sans
    from .progetto import ts
    el = elementi(G)
    cart = P.controllo('anteprima')
    cart.mkdir(exist_ok=True)
    for f in cart.glob('*.jpg'):
        f.unlink()
    tiles = []
    for k, (tipo, s, e, testo) in enumerate(el):
        t = s + min(1.5, (e - s) / 2) if e - s > 3 else (s + e) / 2
        f = cart / f"a{k:02d}-{t:07.2f}.jpg"
        ffmpeg('-ss', f"{t:.3f}", '-i', video, '-frames:v', '1', f)
        tiles.append((f, f"{ts(t)}  {tipo}"))
    cols, w, h = 4, 480, 270
    rows = -(-len(tiles) // cols)
    sheet = Image.new('RGB', (cols * (w + 8) + 8, rows * (h + 44) + 8), (0, 26, 61))
    d = ImageDraw.Draw(sheet)
    for i, (f, lab) in enumerate(tiles):
        x, y = 8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 44)
        sheet.paste(Image.open(f).convert('RGB').resize((w, h)), (x, y))
        d.text((x + 2, y + h + 8), lab, font=sans(22, 500), fill=(244, 244, 244))
    sheet.save(P.controllo('anteprima.jpg'), quality=86)
    L = [f"# Anteprima {P.slug}: dove compare ogni elemento", "",
         f"File: `renders/{video.name}`. Tempi del montato (m:ss.cc).", "",
         "| da | a | elemento | testo o materiale |", "|---|---|---|---|"]
    L += [f"| {ts(s)} | {ts(e)} | {tipo} | {testo} |" for tipo, s, e, testo in el]
    P.controllo('anteprima-tempi.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print(f"-> controlli/anteprima.jpg ({len(tiles)} momenti), controlli/anteprima-tempi.md")

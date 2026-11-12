"""Infografiche sopra un reel 9:16 gia montato (laboratorio, fase 1, 03/11/2026).

Modulo nuovo: non cambia niente del flusso 16:9. Riusa i pezzi condivisi senza modificarli
(`scene/_scena.html` con la misura del quadro sostituita al volo, `scene/_scena.js`, i modelli
di `scene/`), HyperFrames 0.8.204 in locale con le variabili di `inserti.ambiente()`.

Catena: dati della grafica -> pagina HyperFrames 1080x1920 -> MOV ProRes 4444 con alfa ->
sovrapposizione al video base in YUV 4:2:0 (i pixel fuori dalla grafica restano quelli del video),
libx264 CRF 16 preset slow, metadati BT.709, audio copiato (regola di fase 0).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

from .inserti import FONT, GSAP, LOGO, PITTOGRAMMA, HF, ambiente, dimentica, _css_brand
from .progetto import AGENTE

SCENE = AGENTE / 'motore' / 'inserti' / 'scene'
from .reel_comune import W, H          # il formato del reel (9:16 o 16:9, 11/11/2026)
ENC = ['-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-profile:v', 'high', '-level:v', '4.1',
       '-pix_fmt', 'yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
       '-color_range', 'tv']


def pagina(elementi, frames, fps, cartella, mosso=True):
    """la pagina HyperFrames del reel (W×H: 9:16 o 16:9) con gli elementi dati (tempi in secondi dall'inizio della pagina)"""
    if cartella.exists():
        shutil.rmtree(cartella)
    (cartella / 'assets').mkdir(parents=True)
    for f in (FONT, GSAP, LOGO, PITTOGRAMMA):
        shutil.copy2(f, cartella / 'assets' / f.name)
    shutil.copy2(SCENE / '_scena.js', cartella / 'assets' / 'scena.js')
    (cartella / 'assets' / 'comune.css').write_text(_css_brand(), encoding='utf-8')
    elementi = _servier(elementi, cartella / 'assets')
    _pittogramma_parti(elementi, cartella / 'assets')
    modelli = sorted({x['modello'] for x in elementi} | {d for x in elementi for d in x.get('usa', [])})
    _sintassi(modelli)
    stile = '\n'.join((SCENE / f"{m}.css").read_text(encoding='utf-8') for m in modelli if (SCENE / f"{m}.css").exists())
    script = _tabler(elementi) + '\n'.join((SCENE / f"{m}.js").read_text(encoding='utf-8') for m in modelli)
    if (W, H) != (1080, 1920):
        # 16:9 (11/11/2026): i modelli dei reel sono scritti sul quadro 1080x1920; qui il quadro diventa quello del reel
        # (il verticale resta identico byte per byte, quindi la cache e la regressione non cambiano)
        script = script.replace('const QW = 1080, QH = 1920', f'const QW = {W}, QH = {H}')
        stile = stile.replace('width: 1080px; height: 1920px', f'width: {W}px; height: {H}px')
    durata = frames / fps
    dati = {'durata': durata, 'fps': fps, 'strato': 'davanti', 'elementi': elementi, 'cam': []}
    base = (SCENE / '_scena.html').read_text(encoding='utf-8')
    assert 'data-width="1920" data-height="1080"' in base
    html = base.replace('data-width="1920" data-height="1080"', f'data-width="{W}" data-height="{H}"') \
        .replace('/*__STILE__*/', stile).replace('/*__MODELLI__*/', script) \
        .replace('__DURATA__', f"{durata:.6f}").replace('__DATI__', json.dumps(dati, ensure_ascii=False)) \
        .replace('__MB__', 'data-motion-blur="on"' if mosso else '')
    (cartella / 'index.html').write_text(html, encoding='utf-8')
    return cartella


_SINTASSI_OK = set()


def _sintassi(modelli):
    """fase 6 (05/11/2026): un errore di sintassi in un modello fermava HyperFrames con un messaggio oscuro
    («MODELLI[x.modello] is not a function»); qui si controlla ogni modello con node --check, una volta per versione"""
    import hashlib
    for m in modelli:
        f = SCENE / f"{m}.js"
        if not f.exists():
            continue
        h = hashlib.md5(f.read_bytes()).hexdigest()
        if h in _SINTASSI_OK:
            continue
        r = subprocess.run(['node', '--check', str(f)], capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"modello {f.name}: errore di sintassi\n{r.stderr[-800:]}")
        _SINTASSI_OK.add(h)


def _servier(elementi, assets):
    """collaudo (04/11/2026): un elemento con `dati.servier` {nome, alto, modo} usa un disegno Servier di
    libreria/anatomia, ricolorato nel brand (anatomia.ricolora) e copiato negli assets della pagina; il modello lo trova
    in `dati.src` con le misure in `dati.img_w`, `dati.img_h`.
    Fase 6, giro 4: lo stesso per ogni dizionario annidato con la chiave `servier` (i pezzi di un'infografica, le icone
    delle voci): il dizionario riceve src, img_w, img_h"""
    import copy
    out = copy.deepcopy(elementi)
    from .anatomia import ricolora
    k = [0]

    def giro(o):
        if isinstance(o, dict):
            sv = o.get('servier')
            if isinstance(sv, dict) and sv.get('nome'):
                im, _ = ricolora(sv['nome'], sv['alto'], modo=sv.get('modo', 'ossa'), ritaglio=sv.get('ritaglio'))
                nome = f"servier-{k[0]}-{Path(sv['nome']).stem}.png"
                k[0] += 1
                im.save(assets / nome)
                o.update({'src': f"assets/{nome}", 'img_w': im.width, 'img_h': im.height})
            for v in o.values():
                giro(v)
        elif isinstance(o, list):
            for v in o:
                giro(v)
    for x in out:
        giro(x.get('dati') or {})
    return out


TABLER = AGENTE / 'motore' / 'inserti' / 'icone' / 'tabler-3.49.0' / 'icons' / 'outline'


def _tabler(elementi):
    """fase 6, giro 4 (Riccardo 05/11/2026: libreria di icone open source, versione fissata): ogni stringa
    «tabler:<nome>» nei dati porta nella pagina i tracciati dell'icona Tabler 3.49.0 (MIT, motore/inserti/icone/),
    in `TABLER[nome]` (lista di «d», viewBox 24×24, tratto 2). Solo le icone usate; un nome che non c'è ferma il render"""
    import re
    nomi = set(re.findall(r'"tabler:([a-z0-9-]+)"', json.dumps(elementi)))
    if not nomi:
        return ''
    out = {}
    for n in sorted(nomi):
        f = TABLER / f"{n}.svg"
        if not f.exists():
            sys.exit(f"icona Tabler «{n}» non trovata in {TABLER}")
        out[n] = [d for d in re.findall(r'<path[^>]*\sd="([^"]+)"', f.read_text(encoding='utf-8')) if d != 'M0 0h24v24H0z']
    return f"const TABLER = {json.dumps(out)};\n"


def _pittogramma_parti(elementi, assets):
    """fase 6, giro 4: il pittogramma Mobilitas che «si compone» (disco, poi la barra, poi il segno) ha bisogno di due
    livelli dello stesso file: il disco senza il verde e il solo verde. Si separano i pixel (niente ricolore: sovrapposti
    tornano il pittogramma originale) e si scrivono negli assets della pagina"""
    if '"pittogramma"' not in json.dumps(elementi):
        return
    import numpy as np
    from PIL import Image
    im = np.array(Image.open(PITTOGRAMMA).convert('RGBA')).astype(np.int16)
    r, g, b, a = im[..., 0], im[..., 1], im[..., 2], im[..., 3]
    verde = (g > r + 40) & (g > b + 10) & (a > 0)
    blu = im.copy()
    # il disco: dove c'era il verde si mette il blu del disco (mediana dei pixel blu pieni)
    pieni = (a == 255) & ~verde
    blu[verde, :3] = np.median(im[pieni][:, :3], axis=0).astype(np.int16)
    blu[verde, 3] = 255
    segno = im.copy()
    segno[~verde, 3] = 0
    Image.fromarray(blu.astype(np.uint8)).save(assets / 'pittogramma-disco.png')
    Image.fromarray(segno.astype(np.uint8)).save(assets / 'pittogramma-segno.png')


def _env(tmpdir=None):
    """le variabili di HyperFrames (inserti.ambiente); con tmpdir i suoi temporanei vanno nella cartella di
    lavoro dell'ad (fase 4: ogni ad ha la sua)"""
    env = ambiente()
    if tmpdir:
        Path(tmpdir).mkdir(parents=True, exist_ok=True)
        env['TMPDIR'] = str(tmpdir)
    return env


# render (fase 5, Riccardo 04/11/2026): un solo processo di Chrome.
# - con --workers auto due render della stessa pagina differiscono di sottopixel (fase 4: 90 fotogrammi su 234 nella
#   chiusura, fino a 53 livelli dopo la codifica);
# - con 1 processo e la GPU restano differenze di 1 livello su poche decine di pixel in alcuni fotogrammi (fase 5:
#   24 fotogrammi su 234 nella chiusura; 0 nelle etichette);
# - con 1 processo e Chrome senza GPU (--no-browser-gpu, SwiftShader) i due file sono identici bit per bit, MA i
#   bagliori grandi escono tagliati da uno scalino netto (fase 5: etichette f1090, a y 763 e x 763; lo ha visto il
#   direttore). Per questo resta la GPU: la regressione confronta i livelli delle grafiche con tolleranza di 1.
WORKERS = '1'
GPU = []                       # ['--no-browser-gpu'] = identico bit per bit ma con lo scalino sui bagliori
IMPOSTAZIONI = f"workers={WORKERS} gpu={'no' if GPU else 'si'}"   # entra nella chiave della cache dei MOV


def rendi(cartella, out, fps, frames, tmpdir=None, workers=None):
    """MOV con alfa (ProRes 4444, yuva444p12le) dalla pagina, in locale"""
    tmp = Path(out).with_suffix('.tmp.mov')
    r = subprocess.run([str(HF), 'render', str(cartella), '--fps', str(fps), '--format', 'mov', '-o', str(tmp),
                        '--workers', str(workers or WORKERS), *GPU, '--quiet'], env=_env(tmpdir), capture_output=True, text=True)
    dimentica(cartella)
    if r.returncode or not tmp.exists():
        sys.exit(f"render HyperFrames fallito ({cartella.name}):\n{(r.stderr or r.stdout)[-1500:]}")
    pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0',
                                    '-show_entries', 'stream=nb_read_packets,pix_fmt,codec_name,width,height,'
                                    'color_space,color_transfer,color_primaries,color_range', '-of', 'json', str(tmp)],
                                   capture_output=True, text=True).stdout)['streams'][0]
    if int(pr['nb_read_packets']) != frames or (pr['width'], pr['height']) != (W, H):
        sys.exit(f"{cartella.name}: {pr}")
    tmp.replace(out)
    return pr


def scatti(cartella, tempi, out, tmpdir=None, cifre=3):
    """fotografie della pagina (PNG con alfa) agli istanti dati"""
    r = subprocess.run([str(HF), 'snapshot', str(cartella), '--at', ','.join(f"{t:.{cifre}f}" for t in tempi), '--no-end',
                        '-o', str(out)], env=_env(tmpdir), capture_output=True, text=True, timeout=3600)
    dimentica(cartella)
    if r.returncode:
        sys.exit(f"snapshot fallito:\n{(r.stderr or r.stdout)[-1200:]}")
    return sorted(Path(out).glob('frame-*.png'), key=lambda f: int(f.name.split('-')[1]))


def sovrapponi(video, mov, f0, out, fps=30, matrice='bt709'):
    """il MOV sopra il video dal fotogramma f0: grafica convertita in YUV BT.709 range tv in modo
    esplicito, sovrapposizione in YUV 4:2:0, audio copiato"""
    fc = (f"[1:v]setpts=PTS-STARTPTS+{f0}/({fps}*TB),scale=in_color_matrix={matrice}:out_color_matrix=bt709:"
          f"in_range=tv:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuva420p[g];"
          f"[0:v][g]overlay=x=0:y=0:format=yuv420:eof_action=pass:shortest=0[v]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-i', str(mov), '-filter_complex', fc,
                    '-map', '[v]', '-map', '0:a', *ENC, '-c:a', 'copy', '-fps_mode', 'passthrough',
                    '-movflags', '+faststart', str(out)], check=True)


def sovrapponi_molti(video, strati, out, fps=30, ss=None, t=None, audio='copy', audio_da=None):
    """piu MOV sopra il video, in una sola codifica: strati = [(mov, f0), ...] (f0 = fotogramma del
    video dove comincia il MOV). ss/t: solo un tratto (anteprima; f0 restano quelli del video intero).
    audio_da (fase 6): l'audio viene da un altro file (il video base originale, quando `video` è il base con gli zoom,
    che non ha audio).
    Fase 6, modelli sulla persona: uno strato può essere (mov, f0, extra) con extra = {'frames': n, 'maschera': video
    della sagoma (grigio, n fotogrammi) -> dopo la grafica si rimette sopra la persona del video base (la grafica passa
    «dietro»); 'pip': {'scala', 'x', 'y'} -> sotto la grafica si mette il video base rimpicciolito (lui nel cerchio)}.
    Senza extra la catena dei filtri è identica a prima."""
    off = round(ss * fps) if ss else 0
    fc, cur = [], '0:v'
    ext = [(k, x[2]) for k, x in enumerate(strati, start=1) if len(x) > 2 and x[2]]
    copie = sum(int(bool(e.get('maschera'))) + int(bool(e.get('pip'))) for _, e in ext)
    if copie:
        fc.append('[0:v]split=' + str(copie + 1) + '[b0]' + ''.join(f'[bx{i}]' for i in range(copie)))
        cur = 'b0'
    nb, nm, maschere = 0, 0, []
    for k, x in enumerate(strati, start=1):
        mov, f0 = x[0], x[1]
        e = x[2] if len(x) > 2 and x[2] else {}
        st = f"setpts=PTS-STARTPTS+{f0 - off}/({fps}*TB)"
        tr = f"trim=start_frame={max(0, f0 - off)}:end_frame={max(0, f0 - off) + e.get('frames', 0)}"
        if e.get('pip'):
            q = e['pip']
            fc.append(f"[bx{nb}]{tr},{st},scale=round(iw*{q['scala']}/2)*2:round(ih*{q['scala']}/2)*2:flags=lanczos[pip{k}]")
            fc.append(f"[{cur}][pip{k}]overlay=x={q['x']}:y={q['y']}:format=yuv420:eof_action=pass:shortest=0[pv{k}]")
            cur = f"pv{k}"; nb += 1
        fc.append(f"[{k}:v]setpts=PTS-STARTPTS+{f0 - off}/({fps}*TB),scale=in_color_matrix=bt709:out_color_matrix=bt709:"
                  f"in_range=tv:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuva420p[g{k}]")
        fc.append(f"[{cur}][g{k}]overlay=x=0:y=0:format=yuv420:eof_action=pass:shortest=0[v{k}]")
        cur = f"v{k}"
        if e.get('maschera'):
            mi = len(strati) + 1 + nm
            maschere.append(e['maschera'])
            fc.append(f"[bx{nb}]{tr},{st}[pb{k}]")
            fc.append(f"[{mi}:v]{st},format=gray[m{k}]")
            fc.append(f"[pb{k}][m{k}]alphamerge,format=yuva420p[pp{k}]")
            fc.append(f"[{cur}][pp{k}]overlay=x=0:y=0:format=yuv420:eof_action=pass:shortest=0[vp{k}]")
            cur = f"vp{k}"; nb += 1; nm += 1
    ing = (['-ss', str(ss)] if ss else []) + (['-t', str(t)] if t else []) + ['-i', str(video)]
    for x in strati:
        ing += ['-i', str(x[0])]
    for m in maschere:
        ing += ['-i', str(m)]
    ma = '0:a'
    if audio_da:
        ing += ['-i', str(audio_da)]
        ma = f"{len(strati) + len(maschere) + 1}:a"
    aud = ['-c:a', 'copy'] if audio == 'copy' else ['-c:a', 'aac', '-b:a', '192k']
    if not strati:
        fc, cur = ['[0:v]null[v0]'], 'v0'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ing, '-filter_complex', ';'.join(fc), '-map', f'[{cur}]', '-map', ma,
                    *ENC, *aud, '-fps_mode', 'passthrough', '-movflags', '+faststart', str(out)], check=True)


def md5_audio(f):
    return subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-map', '0:a', '-c', 'copy', '-f', 'md5', '-'],
                          capture_output=True, text=True).stdout.strip().split('=')[-1]

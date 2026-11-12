"""Fase `inserti`: le grafiche animate (HyperFrames) del piano, una per inserto.

Ogni voce di `grafica.json -> inserti` (da `regia.json -> inserti`) usa un
modello riusabile di `motore/inserti/modelli/<modello>.js|.css`, montato su
`_base.html` con `_comune.js` e uno stile comune generato da `brand.json`. Il
modello riceve `window.DATI`: testi, tempi relativi all'inizio dell'inserto
(risolti dalle frasi), materiali gia preparati, lato del pannello.

Esce un MOV ProRes 4444 con alfa per inserto, alla frequenza del progetto e
lungo esattamente i suoi frame, in `videos/<slug>/inserti/`; `finale` li
sovrappone al montato sotto il livello Pillow (sottotitoli, chip). Cache sul
contenuto: un inserto che non cambia non si rifa.

Regole (CLAUDE.md, Modalita laboratorio): HyperFrames versione fissata in
`motore/inserti/package.json`, telemetria e aggiornamenti spenti, niente cloud.
In piu, ogni comando gira con la "casa" spostata dentro il laboratorio
(`motore/inserti/.casa/`): configurazione, cronologia e temporanei di
HyperFrames non escono dal laboratorio (la cronologia copia i file dei progetti,
e nei progetti ci possono essere foto di pazienti).

Modelli: aggancio, numero, sagoma, prodotto, telefono, primadopo, lista,
scelte, modulo, chiusura. Un modello nuovo = un .js (+ .css) che legge DATI e
chiude con chiudi().
"""
import concurrent.futures as cf
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from .progetto import AGENTE, LIBRERIA, RISORSE, Progetto, scrivi, ts, lavori as _lavori

BASE = AGENTE / 'motore' / 'inserti'
MODELLI = BASE / 'modelli'
HF = BASE / 'node_modules' / '.bin' / 'hyperframes'
GSAP = BASE / 'node_modules' / 'hyperframes' / 'dist' / 'vendor' / 'npm' / 'gsap@3.15.0' / 'dist' / 'gsap.min.js'
CASA = BASE / '.casa'
FONT = RISORSE / 'fonts' / 'Montserrat-VF.ttf'
LOGO = LIBRERIA / 'logo' / 'logo_verde.png'
PITTOGRAMMA = LIBRERIA / 'logo' / 'pittogramma-sfondo-trasparente.png'  # fase 7c: su un disco panna, mai ricolorato
VERSIONE_MODELLI = 2


def ambiente():
    """variabili per ogni comando HyperFrames: niente telemetria, niente
    aggiornamenti, e tutto lo stato dentro il laboratorio"""
    for d in (CASA / '.cache', CASA / 'tmp'):
        d.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, HOME=str(CASA), XDG_CACHE_HOME=str(CASA / '.cache'), TMPDIR=str(CASA / 'tmp'),
               DO_NOT_TRACK='1', HYPERFRAMES_NO_TELEMETRY='1', HYPERFRAMES_NO_UPDATE_CHECK='1',
               HYPERFRAMES_SKIP_SKILLS='1', HYPERFRAMES_EXTRACT_CACHE_DIR='off')
    # il browser gia scaricato si usa in sola lettura (evita 197 MB in piu)
    vero = Path(os.path.expanduser('~')) / '.cache' / 'hyperframes' / 'chrome'
    for b in sorted(vero.glob('chrome-headless-shell/*/*/chrome-headless-shell')):
        env['HYPERFRAMES_BROWSER_PATH'] = str(b)
    return env


def _css_brand():
    from . import stile as S
    c = S.BRAND['colori']
    return f'''@font-face {{ font-family: "MontserratMobilitas"; src: url("Montserrat-VF.ttf") format("truetype");
  font-weight: 100 900; font-style: normal; }}
:root {{ --blu: {c['blu_notte']['hex']}; --profondo: {c['blu_profondo']['hex']}; --panna: {c['panna']['hex']};
  --verde: {c['verde']['hex']}; --panna76: rgba(244,244,244,0.70); --filetto: rgba(244,244,244,0.14);
  --abisso: {c['blu_abisso']['hex']}; --fondo-sito: {S.BRAND['fondo_scuro']['css']};
  --grad-titolo: {S.BRAND['titoli']['gradiente_css']};
  --panna70: rgba(244,244,244,{S.BRAND['trasparenze']['testo_secondario_su_blu']['opacita']});
  --margine: {S.PANNELLO_MARGINE}px; }}
html, body {{ margin: 0; background: transparent; }}
#root {{ position: absolute; inset: 0; overflow: hidden; }}
#scena {{ position: absolute; inset: 0; font-family: "MontserratMobilitas"; color: var(--panna);
  -webkit-font-smoothing: antialiased; text-wrap: balance; }}
.pannello {{ position: absolute; top: 0; bottom: 0; width: {S.PANNELLO_W}px; background: var(--blu); }}
.pannello.sx {{ left: 0; }}
.pannello.dx {{ right: 0; }}
.k {{ font-weight: 800; color: var(--verde); }}
.logo {{ display: block; height: auto; }}
'''


# ------------------------------------------------------------------ materiali
def scontorna_render(src, dst, titolo=True, tieni_bianco=False):
    """un'immagine "da App Store" (telefono su fondo chiaro, titolo in alto) ->
    PNG con solo il telefono, fondo trasparente. Si toglie il fondo chiaro
    collegato ai bordi (non i chiari dentro lo schermo) e la fascia del titolo
    (titolo=False per i render senza titolo: fase 7c, intro-app.png ne perdeva la cima)."""
    from PIL import Image, ImageDraw, ImageFilter
    im = Image.open(src).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    cand = ((lum > 150) & (sat < 70))
    if tieni_bianco:
        # le card bianche che galleggiano sul fondo (bianco puro, il fondo e grigio caldo 242-248) restano
        cand &= ~(a.min(axis=2) >= 251)
    cand = cand.astype(np.uint8) * 255
    m = Image.fromarray(cand, 'L').copy()      # copia: l'immagine da numpy e in sola lettura
    W, H = m.size
    for seme in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1), (W // 2, H - 1), (0, H // 2), (W - 1, H // 2)]:
        if m.getpixel(seme) == 255:
            ImageDraw.floodfill(m, seme, 128)
    fondo = np.asarray(m) == 128
    alfa = Image.fromarray(np.where(fondo, 0, 255).astype(np.uint8), 'L').filter(ImageFilter.GaussianBlur(1.2))
    # fascia del titolo: righe scure in alto, fino al primo vuoto lungo
    scuro = (lum < 150).mean(axis=1)
    y, vuoto, fine_titolo = 0, 0, 0
    while titolo and y < H // 3:
        if scuro[y] > 0.002:
            fine_titolo, vuoto = y, 0
        else:
            vuoto += 1
            if fine_titolo and vuoto > 60:
                break
        y += 1
    out = im.convert('RGBA')
    out.putalpha(alfa)
    out = out.crop((0, fine_titolo + 30, W, H))
    bbox = out.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    out = out.crop(bbox) if bbox else out
    out.save(dst)
    return out.size


def _foto(src, dst, alt=1600):
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    im.thumbnail((alt * 3, alt))
    im.save(dst, quality=90)
    return im.size


# ------------------------------------------------------------------ preparazione
def _prepara(P, x, fps, vietati, ultima_parola):
    d = P.p('inserti', x['id'])
    if d.exists():
        shutil.rmtree(d)
    (d / 'assets').mkdir(parents=True)
    for f in (FONT, GSAP, LOGO, MODELLI / '_comune.js'):
        shutil.copy2(f, d / 'assets' / f.name.replace('_comune', 'comune'))
    (d / 'assets' / 'comune.css').write_text(_css_brand(), encoding='utf-8')
    frames = int(round((x['e'] - x['s']) * fps))
    dati = json.loads(json.dumps(x['dati']))
    dati['durata'] = round(frames / fps, 6)
    materiali = []
    if x['modello'] == 'telefono':
        for k, s in enumerate(dati.get('schermate', [])):
            src = P.materiale(s['file'])
            if src is None:
                sys.exit(f"inserto {x['id']}: materiale non trovato: {s['file']}")
            if src.name in vietati:
                sys.exit(f"inserto {x['id']}: {src.name} e fra i materiali vietati in regia")
            nome = f"s{k + 1}.png"
            if s.get('tipo', 'render') == 'render':
                scontorna_render(src, d / 'assets' / nome)
            else:
                shutil.copy2(src, d / 'assets' / nome)
            s['src'] = f"assets/{nome}"
            materiali.append(str(src))
    if x['modello'] == 'primadopo':
        from .visione import posa
        srcs = {}
        for k in ('foto_prima', 'foto_dopo'):
            src = P.materiale(dati[k])
            if src is None:
                sys.exit(f"inserto {x['id']}: foto non trovata: {dati[k]}")
            if src.name in vietati:
                sys.exit(f"inserto {x['id']}: {src.name} e fra i materiali vietati in regia")
            srcs[k] = src
        punti = posa([str(s) for s in srcs.values()])
        for k, src in srcs.items():
            chi = k.split('_')[1]
            w, h = _foto(src, d / 'assets' / f"{chi}.jpg")
            pp = punti[str(src)]['punti']
            if not pp or any(q is None for q in pp):
                sys.exit(f"inserto {x['id']}: Vision non trova tutti i punti posturali in {src.name}")
            dati[chi] = {'src': f"assets/{chi}.jpg", 'w': w, 'h': h, 'punti': pp}
            materiali.append(str(src))
    if dati.get('pieno_dopo_ultima'):
        dati['pieno'] = {'t': round(ultima_parola + 0.15 - x['s'], 3)}
    stile = (MODELLI / f"{x['modello']}.css").read_text(encoding='utf-8') \
        if (MODELLI / f"{x['modello']}.css").exists() else ''
    script = (MODELLI / f"{x['modello']}.js").read_text(encoding='utf-8')
    html = (MODELLI / '_base.html').read_text(encoding='utf-8') \
        .replace('/*__STILE__*/', stile).replace('/*__SCRIPT__*/', script) \
        .replace('__DURATA__', f"{dati['durata']:.6f}") \
        .replace('__DATI__', json.dumps(dati, ensure_ascii=False))
    (d / 'index.html').write_text(html, encoding='utf-8')
    h = hashlib.sha1()
    h.update(html.encode())
    for f in sorted((d / 'assets').iterdir()):
        h.update(f.name.encode())
        h.update(f.read_bytes())
    h.update(f"{fps}|{VERSIONE_MODELLI}".encode())
    return d, frames, h.hexdigest()[:12], materiali


STORIA = CASA / '.cache' / 'hyperframes' / 'history'


def dimentica(d=None):
    """la cronologia di HyperFrames copia ogni file del progetto (foto comprese) in
    .casa/.cache/hyperframes/history. Al motore non serve (non si edita in Studio) e
    non deve conservare foto dei pazienti (CLAUDE.md): dopo ogni render si cancella
    la voce di quel progetto; senza argomento, tutte le voci che contengono immagini
    JPEG o che vengono da progetti che non esistono piu."""
    if not STORIA.is_dir():
        return 0
    via = 0
    for v in STORIA.iterdir():
        pj = v / 'project.json'
        if not v.is_dir() or not pj.exists():
            continue
        try:
            dir_ = Path(json.loads(pj.read_text())['dir'])
        except (ValueError, KeyError):
            dir_ = None
        if d is not None:
            togli = dir_ is not None and dir_.resolve() == Path(d).resolve()
        else:
            togli = dir_ is None or not dir_.exists() or any(
                f.is_file() and f.open('rb').read(3) == b'\xff\xd8\xff' for f in (v / 'blobs').rglob('*'))
        if togli:
            shutil.rmtree(v, ignore_errors=True)
            via += 1
    return via


def _render(d, out, fps_str, frames):
    tmp = out.with_suffix('.tmp.mov')
    cmd = [str(HF), 'render', str(d), '--fps', fps_str, '--format', 'mov', '-o', str(tmp), '--quiet']
    r = subprocess.run(cmd, env=ambiente(), capture_output=True, text=True)
    dimentica(d)
    if r.returncode or not tmp.exists():
        sys.exit(f"render HyperFrames fallito per {d.name}:\n{(r.stderr or r.stdout)[-1500:]}")
    pr = subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries',
                         'stream=nb_read_packets,pix_fmt,r_frame_rate', '-of', 'json', str(tmp)],
                        capture_output=True, text=True)
    s = json.loads(pr.stdout)['streams'][0]
    if int(s['nb_read_packets']) != frames or s['pix_fmt'] != 'yuva444p12le':
        sys.exit(f"{d.name}: {s['nb_read_packets']} frame {s['pix_fmt']} invece di {frames} yuva444p12le")
    os.replace(tmp, out)


def inserti(slug, solo=None):
    P = Progetto(slug)
    G = P.leggi('grafica.json')
    ins = G.get('inserti', [])
    if not ins:
        print("nessun inserto in regia")
        P.scrivi('inserti.json', [])
        return
    # la continuita fra inserti e frasi chiave (entra/esce) la decide `grafica` (piano._continuita)
    W = P.leggi('parole-montato.json')
    vietati = set(G.get('materiali_vietati', []))
    solo = {int(v) for v in solo.split(',')} if solo else None
    lavori, uscita = [], []
    for k, x in enumerate(ins):
        d, frames, chiave, mat = _prepara(P, x, P.fps, vietati, W[-1][1])
        out = P.p('inserti', f"{x['id']}-{chiave}.mov")
        if solo is not None and (k + 1) in solo and out.exists():
            out.unlink()
        if not out.exists():
            lavori.append((d, out, frames))
        uscita.append({'id': x['id'], 'modello': x['modello'], 'file': f"inserti/{out.name}", 's': x['s'],
                       'e': round(x['s'] + frames / P.fps, 6), 'frames': frames, 'materiali': mat})
    t0 = time.time()
    print(f"{len(ins)} inserti, {len(lavori)} da renderizzare con HyperFrames ({len(ins) - len(lavori)} in cache)...")
    with cf.ThreadPoolExecutor(_lavori(2)) as ex:
        for f in ex.map(lambda a: _render(a[0], a[1], P.fps_str, a[2]), lavori):
            pass
    validi = {Path(u['file']).name for u in uscita}
    for f in P.p('inserti').glob('*.mov'):
        if f.name not in validi:
            f.unlink()
    P.scrivi('inserti.json', uscita)
    for u in uscita:
        print(f"   {ts(u['s']):>9}  {u['id']:<14} {u['frames']:4d} frame")
    print(f"-> data/inserti.json, MOV in inserti/ ({time.time() - t0:.0f} s)")

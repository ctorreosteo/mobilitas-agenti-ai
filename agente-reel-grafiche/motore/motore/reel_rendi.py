"""Tappa 3 dell'agente reel-grafiche: render, sovrapposizione, anteprime e controlli automatici (fase 4, 04/11/2026).

Parte quando il piano passa i controlli (fase 6, giro 4, Riccardo 05/11/2026: niente fermata sul piano; prima era
l'approvazione di Riccardo legata all'md5 di `piano.json`).

Esce:
- `anteprime/<slug>_lavoro-intero.mp4`: il video con tutte le grafiche, ricodifica standard e audio copiato;
- `anteprime/<slug>_lavoro-intero-ZONE-META.mp4`: la stessa con le zone dell'interfaccia Meta in grigio;
- per ogni grafica, l'anteprima ±3 s e il provino ogni 0,25 s;
- `controlli/controlli.json` + `controlli.md`;
- in `.lavoro/<slug>/direttore/<grafica>/` i fogli e il prompt per il direttore artistico.

I controlli sono quelli delle fasi 1–3, resi generali:
1. audio: md5 del flusso uguale all'originale;
2. video uguale fuori dalle grafiche: SSIM sui fotogrammi senza grafiche e, nelle grafiche «finestra», fuori
   dalla finestra (minimo 0,99; la sola ricodifica dà circa 0,995);
3. nessuna sovrapposizione fra grafiche, niente «tutto schermo» sulle 3D, niente «finestra» fuori dalla
   finestra (canale alfa del MOV fotogramma per fotogramma);
4. lettere intere e nella zona sicura: variante «solo testo» della pagina (sfondi, bordi, ombre, immagini e
   filtri spenti) fotografata su ogni fotogramma visibile; il testo resta in x 65–1014, y 269–1247, e nel
   modo «finestra» anche dentro la finestra;
5. testo visibile letto dalla pagina (`reel_dom.mjs`) su ogni fotogramma:
   - nessuna cifra non detta, neanche per un fotogramma;
   - «solo parole dette»: ogni parola che resta a schermo almeno 3 fotogrammi è nell'SRT (esclusi + = € e i
     numeri detti); le lettere provvisorie delle decifrazioni durano un fotogramma e non contano come parole;
   - corpo effettivo dei testi fermi almeno quello minimo;
6. nessuna cifra non detta secondo Apple Vision, su tutti i fotogrammi con grafiche del video finito. Una
   cifra letta da Vision è spiegata se nello stesso punto la pagina mostra quella cifra; le altre vanno
   guardate dall'agente (ritaglio in `controlli/cifre-da-guardare/`) e segnate con `./mve reel-guardato`.

Poi il voto del direttore artistico (minimo 7, al massimo due giri) e **ci si ferma**: le anteprime aspettano
l'approvazione di Riccardo (`./mve reel-approva <slug> anteprime`).
"""
import datetime
import hashlib
import json
import re
import shutil
import subprocess
import sys

import numpy as np

from . import reel_grafiche, reel_comune as C, reel_piano_base
from .reel_comune import W, H, SAFE

SSIM_MIN = 0.99
STABILE = 3            # fotogrammi di fila perche un testo conti come parola scritta
CSS_SOLO_TESTO = ("*,*::before,*::after{background:none!important;background-color:transparent!important;"
                  "border-color:transparent!important;box-shadow:none!important;text-shadow:none!important;"
                  "outline-color:transparent!important;filter:none!important;-webkit-mask-image:none!important;"
                  "mask-image:none!important}*::before,*::after{visibility:hidden!important}"
                  "img,svg,canvas,video{visibility:hidden!important}"
                  ".grad{color:#fff!important;-webkit-text-fill-color:#fff!important}\n")
PUPPETEER = C.AGENTE / 'motore' / 'inserti' / 'node_modules' / 'puppeteer-core' / 'lib' / 'puppeteer' / 'puppeteer-core.js'
DOM_JS = C.AGENTE / 'motore' / 'motore' / 'reel_dom.mjs'


def _approvato(D, cosa, file):
    a = C.leggi(D / 'approvazioni.json', {}).get(cosa)
    if cosa == 'piano':
        from .reel_flusso import piano_approvato
        return piano_approvato(D.name)[0], a
    return bool(a) and a.get('md5') == C.md5_file(file), a


# ---------------------------------------------------------------- render

def _mov(g, fps, L):
    pg = reel_grafiche.pagina(g['elementi'], g['frames'], fps, L / f"pagina-{g['nome']}")
    # chiave della cache: i file della pagina e le impostazioni del render (fase 5)
    h = hashlib.md5(b''.join(p.read_bytes() for p in sorted(pg.rglob('*')) if p.is_file()) + reel_grafiche.IMPOSTAZIONI.encode()).hexdigest()[:12]
    (L / 'mov').mkdir(exist_ok=True)
    mov = L / 'mov' / f"{g['nome']}-{h}.mov"
    if not mov.exists():
        print(f"  render {g['nome']} ({g['frames']} fotogrammi)...", flush=True)
        reel_grafiche.rendi(pg, mov, fps, g['frames'], tmpdir=L / 'tmp-hf')
    return pg, mov, h


def _estrai(video, frames, scala=None):
    return C.estrai(video, frames, scala)


def _provino(video, f0, f1, fps, out):
    from PIL import Image, ImageDraw, ImageFont
    fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 24)
    tt = sorted(set([f0 - 1] + [round(f0 + k * 0.25 * fps) for k in range(int((f1 - f0) / (0.25 * fps)) + 1)] + [f1, f1 + 1]))
    im = _estrai(video, [f for f in tt if f >= 0], (270, 480))
    tiles = []
    for f in tt:
        if f not in im:
            continue
        x = im[f]; d = ImageDraw.Draw(x)
        d.rectangle([0, 0, 168, 30], fill=(255, 230, 0)); d.text((4, 2), f'{f / fps:6.3f}s f{f}', font=fnt, fill='black')
        tiles.append(x)
    cols = 8; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new('RGB', (cols * 273, rows * 483), 'white')
    for i, x in enumerate(tiles):
        sh.paste(x, ((i % cols) * 273, (i // cols) * 483))
    sh.save(out, quality=88)


def zone_meta(full, out):
    g = '0x9A9A9A@0.45'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(full), '-vf',
                    f'drawbox=x=0:y=0:w={W}:h={SAFE[1]}:color={g}:t=fill,drawbox=x=0:y={SAFE[3] + 1}:w={W}:h={H - SAFE[3] - 1}:color={g}:t=fill,'
                    f'drawbox=x=0:y={SAFE[1]}:w={SAFE[0]}:h={SAFE[3] - SAFE[1] + 1}:color={g}:t=fill,'
                    f'drawbox=x={SAFE[2] + 1}:y={SAFE[1]}:w={W - SAFE[2] - 1}:h={SAFE[3] - SAFE[1] + 1}:color={g}:t=fill',
                    *reel_grafiche.ENC, '-c:a', 'copy', '-movflags', '+faststart', str(out)], check=True)


def _extra(g):
    """fase 6: «dietro» (la persona torna sopra la grafica) e «pip» (lui nel cerchio) dai dati della grafica"""
    d = {}
    for x in g['elementi']:
        dd = x.get('dati') or {}
        if dd.get('dietro'):
            d['dietro'] = True
        if dd.get('pip'):
            d['pip'] = dd['pip']
    return d


def sagome(V, g, L, fps):
    """la sagoma della persona sui fotogrammi della grafica (Apple Vision, accurata, piena risoluzione: visione.swift
    `sagome` del motore, usato senza cambiarlo), media su 3 fotogrammi e ammorbidita, in un video grigio senza perdite"""
    from PIL import Image, ImageFilter
    from .visione import binario
    d = L / f"sagome-{g['nome']}"
    if d.exists():
        shutil.rmtree(d)
    (d / 'in').mkdir(parents=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(V), '-vf', f"select='between(n,{g['f0']},{g['f0'] + g['frames'] - 1})',"
                    "scale=in_color_matrix=bt709:in_range=tv:out_range=full", '-fps_mode', 'passthrough', '-start_number', '0',
                    str(d / 'in' / 'f%05d.png')], check=True)
    subprocess.run([str(binario()), 'sagome', str(d / 'in'), str(d / 'm')], check=True, capture_output=True)
    fs = sorted((d / 'm').glob('*.png'))
    if len(fs) != g['frames']:
        sys.exit(f"{g['nome']}: sagome {len(fs)} su {g['frames']} fotogrammi")
    A = [np.asarray(Image.open(f).convert('L'), np.float32) for f in fs]
    (d / 'm2').mkdir()
    for i in range(len(A)):
        m = (A[max(0, i - 1)] + A[i] + A[min(len(A) - 1, i + 1)]) / 3
        Image.fromarray(m.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.5)).save(d / 'm2' / f"f{i:05d}.png")
    out = L / f"sagoma-{g['nome']}.mkv"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(fps), '-i', str(d / 'm2' / 'f%05d.png'), '-c:v', 'ffv1', '-pix_fmt', 'gray',
                    str(out)], check=True)
    shutil.rmtree(d)
    return out


def coperto(mov, maschera, frames):
    """per ogni fotogramma: quanta parte della grafica (alfa) sta sotto la persona (sagoma)"""
    p1 = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(mov), '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(maschera), '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
    out = []
    for _ in range(frames):
        a, m = p1.stdout.read(W * H * 4), p2.stdout.read(W * H)
        if len(a) < W * H * 4 or len(m) < W * H:
            break
        al = np.frombuffer(a, np.uint8)[3::4].astype(np.float32) / 255
        mm = np.frombuffer(m, np.uint8).astype(np.float32) / 255
        out.append(float((al * mm).sum() / al.sum()) if al.sum() > 50 else 0.0)
    p1.kill(); p2.kill()
    return out


# ---------------------------------------------------------------- controlli

def _rett_al(dati, tr):
    rr = dati.get('rett')
    if rr is None:
        return None
    rr = rr if isinstance(rr, list) else [dict(rr, da=0)]
    # i modelli cambiano rettangolo 1 ms prima di `da` (tl.set a da - EPS, EPS = 0,001)
    return [q for q in rr if q.get('da', 0) <= tr + 0.0011][-1]


def _zona(g, tr):
    """il rettangolo in cui la grafica deve stare al tempo tr: la finestra («finestra»), il riquadro dati.box («micro»,
    «persona»: fase 6), o None («tutto schermo»)"""
    dati = g['elementi'][0].get('dati') or {}
    if g['modo'] == 'finestra':
        return _rett_al(dati, tr)
    if g['modo'] in ('micro', 'persona', 'palco'):
        b = next(((x.get('dati') or {}).get('box') for x in g['elementi'] if (x.get('dati') or {}).get('box')), None)
        return dict(b, r=0) if b else None
    return None


def alfa(g, mov, fps, pf=None):
    """per ogni fotogramma del MOV: copertura media dell'alfa e, nel modo «finestra», l'alfa massimo fuori
    dalla finestra (rettangolo dei dati allargato di 1 px)"""
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(mov), '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
    dati = g['elementi'][0].get('dati') or {}
    cop, fuori, tagli = [], [], []
    bande = {}
    k = 0
    n = W * H * 4
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        a = np.frombuffer(b, np.uint8)[3::4].reshape(H, W)
        cop.append(float(a.mean() / 255))
        if pf and (g['f0'] + k) in pf:
            # 07/11/2026: quanto le grafiche coprono la fascia dei sottotitoli (reel_sottotitoli)
            from . import reel_sottotitoli as RSo
            bande[g['f0'] + k] = RSo.copertura(a, pf[g['f0'] + k])
        r = _zona(g, k / fps)
        if r:
            m = a.copy()
            m[max(0, r['y'] - 1):r['y'] + r['h'] + 1, max(0, r['x'] - 1):r['x'] + r['w'] + 1] = 0
            fuori.append(int(m.max()))
            if g['modo'] in ('micro', 'persona', 'palco'):
                # fase 6 (direttore sulla prova persona): una grafica che tocca il bordo del suo riquadro è tagliata
                # (bagliore o ombra che finiscono in un rettangolo, angoli della card dritti)
                x0, y0, x1, y1 = r['x'], r['y'], r['x'] + r['w'] - 1, r['y'] + r['h'] - 1
                # giro 5: un lato del riquadro che coincide con il bordo dello schermo non è un taglio della grafica: lì un
                # bagliore che esce dallo schermo va bene; conta solo una forma piena tagliata (alfa sopra 160)
                lati = [(y0 == 0, a[y0, x0:x1 + 1]), (y1 == H - 1, a[y1, x0:x1 + 1]), (x0 == 0, a[y0:y1 + 1, x0]), (x1 == W - 1, a[y0:y1 + 1, x1])]
                # 07/11/2026: il pannello del palco arriva apposta ai bordi dello schermo; conta solo il lato dentro (sotto)
                bordo = max((0 if g['modo'] == 'palco' else int(v.max())) if schermo and (g['modo'] == 'palco' or int(v.max()) > 160)
                            else int(v.max()) for schermo, v in lati)
                tagli.append(bordo)
        k += 1
    p.wait()
    alfa.tagli = tagli
    alfa.bande = bande
    return cop, fuori


def _corse(fs):
    out = []
    for f in sorted(fs):
        if out and f == out[-1][1] + 1:
            out[-1][1] = f
        else:
            out.append([f, f])
    return out


def ssim(a, b, frames, crop=None, L=None, nome='ssim'):
    """SSIM medio e minimo fra due video sui fotogrammi dati (stessi numeri di fotogramma), con ritaglio opzionale"""
    if not frames:
        return None
    sel = '+'.join(f'between(n,{x},{y})' for x, y in _corse(frames))
    cr = f",crop={crop[2]}:{crop[3]}:{crop[0]}:{crop[1]}" if crop else ''
    stats = L / f'{nome}.log'
    fc = (f"[0:v]select='{sel}'{cr},settb=1/30,setpts=N[a];[1:v]select='{sel}'{cr},settb=1/30,setpts=N[b];"
          f"[a][b]ssim=stats_file={stats}")
    r = subprocess.run(['ffmpeg', '-v', 'info', '-i', str(a), '-i', str(b), '-filter_complex', fc, '-f', 'null', '-'],
                       capture_output=True, text=True)
    m = re.search(r'All:([0-9.]+)', r.stderr)
    per = [float(x) for x in re.findall(r'All:([0-9.]+)', stats.read_text())] if stats.exists() else []
    return {'fotogrammi': len(per), 'medio': float(m.group(1)) if m else None, 'minimo': min(per) if per else None,
            'ritaglio': crop, '_fotogrammi': frames}


def solo_testo(g, vis, fps, L):
    """riquadro del testo (alfa > 40) su ogni fotogramma visibile della variante «solo testo»"""
    from PIL import Image
    pg = reel_grafiche.pagina(g['elementi'], g['frames'], fps, L / f"pagina-{g['nome']}-testo")
    h = (pg / 'index.html').read_text(encoding='utf-8')
    (pg / 'index.html').write_text(h.replace('</style>', CSS_SOLO_TESTO + '</style>', 1), encoding='utf-8')
    sd = L / f"testo-{g['nome']}"
    if sd.exists():
        shutil.rmtree(sd)
    rel = [f - g['f0'] for f in vis]
    fs = reel_grafiche.scatti(pg, [k / fps + 0.0005 for k in rel], sd, tmpdir=L / 'tmp-hf', cifre=4)
    out = {}
    for k, p in zip(rel, fs):
        al = np.asarray(Image.open(p).convert('RGBA'))[..., 3] > 40
        ys, xs = np.nonzero(al)
        out[g['f0'] + k] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None
    shutil.rmtree(sd)
    return out


def dom(g, fps, L):
    """testo visibile nella pagina, fotogramma per fotogramma (due istanti per fotogramma: k/fps e +0,5 ms)"""
    from .inserti import ambiente
    pg = L / f"pagina-{g['nome']}"
    env = ambiente()
    env['TMPDIR'] = str(L / 'tmp')
    out = L / f"dom-{g['nome']}.json"
    prof = L / 'chrome-profilo'
    r = subprocess.run(['node', str(DOM_JS), str(pg), str(out), str(fps), str(g['frames']), env['HYPERFRAMES_BROWSER_PATH'],
                        str(prof), str(PUPPETEER)], env=env, capture_output=True, text=True, timeout=1800)
    shutil.rmtree(prof, ignore_errors=True)
    if r.returncode:
        sys.exit(f"lettura del testo della pagina fallita ({g['nome']}): {r.stderr[-800:]}")
    return json.loads(out.read_text())['frames']


def controlla_testo_dom(g, frames_dom, vis, R, cmin):
    detti, numeri = set(R['parole_dette']), set(R['numeri_detti'])
    cifre_err, parole_err, corpo_err = [], [], []
    storia = {}          # (nodo, testo) -> fotogrammi
    for f in sorted(vis):
        k = f - g['f0']
        for istante in frames_dom[k]:
            for x in istante:
                for c in re.findall(r'\d+', x['t']):
                    if c not in numeri:
                        cifre_err.append({'f': f, 'testo': x['t'], 'cifra': c, 'dove': x['v']})
                storia.setdefault((x['i'], x['t']), set()).add(f)
    scritte = {}
    for (i, t), fs in storia.items():
        lunghe = [c for c in _corse(fs) if c[1] - c[0] + 1 >= STABILE]
        if not lunghe:
            continue
        scritte.setdefault(t, []).append(lunghe[0][0])
        # collaudo (04/11/2026): l'attribuzione Servier (classe reel-attr) e un obbligo di licenza, non copy: niente
        # controllo di parole e corpo (le cifre si controllano lo stesso, e non ce ne sono)
        if any('reel-attr' in x.get('c', '') for f in fs for ist in frames_dom[f - g['f0']] for x in ist if x['i'] == i and x['t'] == t):
            continue
        for w in C.parole_di(t):
            if w in C.SIMBOLI_AMMESSI or re.fullmatch(r'\d+', w):
                continue
            if w not in detti:
                parole_err.append({'parola': w, 'testo': t, 'da_f': lunghe[0][0]})
        fsz = max(x['fs'] for f in fs for ist in frames_dom[f - g['f0']] for x in ist if x['i'] == i and x['t'] == t)
        if fsz < cmin - 0.5 and re.search(r'[0-9A-Za-zÀ-ÿ€]', t):      # i segni (puntini delle card vuote, «?») non sono testo
            corpo_err.append({'testo': t, 'corpo_effettivo': fsz, 'minimo': cmin})
    # una cifra provvisoria vista due volte di seguito per lo stesso fotogramma conta una volta
    viste = {(e['f'], e['testo'], e['cifra']) for e in cifre_err}
    cifre_err = [e for e in cifre_err if (e['f'], e['testo'], e['cifra']) in viste and not viste.discard((e['f'], e['testo'], e['cifra']))]
    return {'cifre_non_dette': cifre_err, 'parole_non_dette': parole_err, 'corpo_sotto_minimo': corpo_err,
            'testi_scritti': sorted(scritte, key=lambda t: min(scritte[t]))}


def vision_cifre(final, per_f, frames_dom_tutti, numeri, L, D, verifiche):
    """Apple Vision su ogni fotogramma con grafiche; per_f: {f: (grafica, zona [x0,y0,x1,y1])}"""
    from PIL import Image
    oc = L / 'ocr'
    risultati, letti, righe = [], 0, 0
    fr = sorted(per_f)
    cartella_guarda = D / 'controlli' / 'cifre-da-guardare'
    if cartella_guarda.exists():
        shutil.rmtree(cartella_guarda)
    for i in range(0, len(fr), 150):
        lotto = fr[i:i + 150]
        if oc.exists():
            shutil.rmtree(oc)
        oc.mkdir()
        sel = '+'.join(f'between(n,{x},{y})' for x, y in _corse(lotto))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(final), '-vf', f"select='{sel}',scale=in_color_matrix=bt709:in_range=tv:out_range=full",
                        '-fps_mode', 'passthrough', '-frame_pts', '1', str(oc / 'f%05d.png')], check=True)
        r = C.vision(oc, L / 'ocr.json')
        for nomefile, obs in r.items():
            f = int(re.search(r'(\d+)', nomefile).group(1))
            if f not in per_f:
                continue
            letti += 1
            nome, z = per_f[f]
            for o in obs:
                cx, cy = o['x'] + o['w'] / 2, o['y'] + o['h'] / 2
                if not (z[0] <= cx <= z[2] and z[1] <= cy <= z[3]):
                    continue                       # fuori dalla grafica: è il video base (sottotitoli, B-roll)
                righe += 1
                ds = re.findall(r'\d+', o['t'])
                if not ds:
                    continue
                box = [o['x'] - 15, o['y'] - 15, o['x'] + o['w'] + 15, o['y'] + o['h'] + 15]
                testi = [x for ist in frames_dom_tutti.get(f, []) for x in ist
                         if x['v'][0] < box[2] and x['v'][2] > box[0] and x['v'][1] < box[3] and x['v'][3] > box[1]]
                cifre_pagina = {c for x in testi for c in re.findall(r'\d', x['t'])}
                spiegata = all(set(d) <= cifre_pagina and d in numeri for d in ds)
                chiave = f"f{f}:{o['t']}"
                e = {'f': f, 'grafica': nome, 'letto': o['t'], 'box': [round(v) for v in (o['x'], o['y'], o['w'], o['h'])],
                     'pagina': ' / '.join(x['t'] for x in testi), 'spiegata': spiegata}
                if not spiegata:
                    (L / 'ritagli').mkdir(exist_ok=True)
                    im = Image.open(oc / nomefile)
                    x0, y0 = max(0, int(o['x']) - 120), max(0, int(o['y']) - 120)
                    e['ritaglio'] = str(L / 'ritagli' / f"f{f:05d}_{len(risultati)}.png")
                    im.crop((x0, y0, min(W, int(o['x'] + o['w']) + 120), min(H, int(o['y'] + o['h']) + 120))).save(e['ritaglio'])
                risultati.append(e)
    shutil.rmtree(oc, ignore_errors=True)
    # le letture non spiegate si raggruppano: stessa grafica, stesso testo letto, fotogrammi di fila (buchi fino a 2),
    # stesso punto (centro entro 40 px). Si guarda un ritaglio per gruppo (quello di meta)
    gruppi = []
    for e in sorted((e for e in risultati if not e['spiegata']), key=lambda e: (e['grafica'], e['letto'], e['f'])):
        c = (e['box'][0] + e['box'][2] / 2, e['box'][1] + e['box'][3] / 2)
        q = gruppi[-1] if gruppi else None
        if q and q['grafica'] == e['grafica'] and q['letto'] == e['letto'] and e['f'] - q['f1'] <= 3 and \
                abs(c[0] - q['c'][0]) < 40 and abs(c[1] - q['c'][1]) < 40:
            q['f1'] = e['f']; q['n'] += 1; q['membri'].append(e)
        else:
            gruppi.append({'grafica': e['grafica'], 'letto': e['letto'], 'f0': e['f'], 'f1': e['f'], 'c': c, 'n': 1, 'membri': [e],
                           'box': e['box'], 'pagina': e['pagina']})
    for q in gruppi:
        q['chiave'] = f"f{q['f0']}-{q['f1']}:{q['letto']}" if q['f1'] > q['f0'] else f"f{q['f0']}:{q['letto']}"
        m = q['membri'][len(q['membri']) // 2]
        cartella_guarda.mkdir(parents=True, exist_ok=True)
        q['ritaglio'] = C.rel(cartella_guarda / f"{q['chiave'].replace(':', '_').replace('/', '_')}.png".replace('€', 'E'))
        shutil.copy2(m['ritaglio'], C.AGENTE / q['ritaglio'])
        q['guardato'] = verifiche.get('cifre', {}).get(q['chiave'])
        q['c'] = [round(v) for v in q['c']]
        del q['membri']
    shutil.rmtree(L / 'ritagli', ignore_errors=True)
    for e in risultati:
        e.pop('ritaglio', None)
    return {'fotogrammi_letti': letti, 'righe_nelle_grafiche': righe, 'righe_con_cifre': len(risultati),
            'spiegate': sum(1 for e in risultati if e['spiegata']), 'non_spiegate': sum(1 for e in risultati if not e['spiegata']),
            'da_guardare': [q for q in gruppi if not q['guardato']], 'guardate': [q for q in gruppi if q['guardato']]}


# ---------------------------------------------------------------- direttore

def pacco_direttore(slug, g, info_g, final, vis, R, L):
    """fogli e prompt per il direttore artistico (subagente direttore-reel)"""
    from PIL import Image, ImageDraw, ImageFont
    from . import catalogo as K
    fps = R['fps']
    d = C.lavoro(slug, 'direttore') / g['nome']         # .lavoro/<slug>/direttore/<grafica>/
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    vs = sorted(vis)
    dodici = [vs[round(i * (len(vs) - 1) / 11)] for i in range(12)]
    im = _estrai(final, dodici, (390, 693))
    fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20)
    sh = Image.new('RGB', (6 * 396, 2 * 699), 'white')
    for i, f in enumerate(dodici):
        x = im[f]; dr = ImageDraw.Draw(x); dr.rectangle([0, 0, 150, 26], fill=(255, 230, 0)); dr.text((4, 2), f'{f / fps:.2f}s f{f}', font=fnt, fill='black')
        sh.paste(x, ((i % 6) * 396, (i // 6) * 699))
    sh.save(d / f"{g['nome']}_telefono-390px.jpg", quality=88)
    cinque = [vs[round(i * (len(vs) - 1) / 4)] for i in range(5)]
    for f, x in _estrai(final, cinque).items():
        x.save(d / f"{g['nome']}_f{f}.png")
    if info_g['modo'] == 'palco':
        # 07/11/2026 («nuova direzione»): il direttore giudica prima di tutto la coerenza del palco e il confronto con le
        # reference verticali (a quale clip assomiglia ogni scena, ed è allo stesso livello?)
        from . import reel_palco as RPal
        prov = sorted((C.cartella(slug) / 'anteprime').glob(f"provino-{g['nome']}-*.jpg"))
        return RPal.prompt_grafica(slug, g, info_g, d, final, vis, fps, prov, [d / (g['nome'] + '_telefono-390px.jpg')],
                                   [d / f"{g['nome']}_f{f}.png" for f in cinque])
    cat = K.per_id().get(info_g['catalogo'], {})
    refs = []
    for rid in re.findall(r'([a-z]+)-(\d+(?:/\d+)*)', cat.get('reference', '')):
        for num in rid[1].split('/'):
            src = C.AGENTE / 'libreria' / 'reference' / f"{rid[0]}-{num}.mov"
            if not src.exists():
                continue
            durata = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(src)],
                                          capture_output=True, text=True).stdout.strip() or 0)
            tiles = []
            for k in range(24):
                b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f"{durata * (k + 0.5) / 24:.2f}", '-i', str(src), '-frames:v', '1',
                                    '-vf', 'scale=240:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
                if b:
                    import io
                    tiles.append(Image.open(io.BytesIO(b)).convert('RGB'))
            if tiles:
                tw, th = tiles[0].size
                s2 = Image.new('RGB', (8 * (tw + 4), 3 * (th + 4)), 'white')
                for i, t in enumerate(tiles):
                    s2.paste(t, ((i % 8) * (tw + 4), (i // 8) * (th + 4)))
                p = d / f"reference-{rid[0]}-{num}.jpg"; s2.save(p, quality=85); refs.append(p)
    es = None
    base = K.per_id().get(cat.get('variante_di') or '', {})
    if base.get('esempio') and (C.AGENTE / base['esempio']).exists():
        es = d / f"esempio-{base['id']}.jpg"
        shutil.copy2(C.AGENTE / base['esempio'], es)
    prov = sorted((C.cartella(slug) / 'anteprime').glob(f"provino-{g['nome']}-*.jpg"))
    righe = [f"Sei il DIRETTORE ARTISTICO dei video di Studio Mobilitas (osteopatia). Voti UNA infografica («{g['nome']}», modello "
             f"«{info_g['catalogo']}», modo «{info_g['modo']}») sopra un reel verticale già montato. Rispondi in italiano.", '',
             "REGOLE (obbligatorie): sola lettura (non creare, modificare o cancellare file); non installare nulla; niente web né "
             f"caricamenti; niente git; non usare /tmp. Solo dentro {C.AGENTE}. Immagini con Read. Le persone nei B-roll non vanno "
             "descritte oltre il necessario.", '', 'CONTESTO',
             f"Video {W}x{H}, voce AI, sottotitoli impressi, B-roll in finestre arrotondate su fondo blu. Voce: {g.get('voce', '(vedi piano)')}.",
             f"Tempi: " + ', '.join(f"{a / fps:.2f}–{(b + 1) / fps:.2f} s" for a, b in _corse(vis)) + (' (apparizioni a taglio, in mezzo il video base)' if len(_corse(vis)) > 1 else '') + '.',
             f"Perché questa grafica: {g.get('perche', '')}",
             f"Vincoli: testi nella zona sicura Meta x {SAFE[0]}–{SAFE[2]}, y {SAFE[1]}–{SAFE[3]}; lettere almeno 1,5 volte i sottotitoli; "
             "solo parole dette; mai cifre non dette; brand blu notte, verde #72FA93, panna; solo Montserrat; sono professionisti sanitari: "
             "niente promesse; mai «il tuo/la tua» insieme al disturbo; mai card, riquadri o pannelli vuoti (in attesa della frase serve un "
             "segnaposto estetico: «?» con i puntini, cifra a contorno o icona sottile). PAROLE E SOTTOTITOLI (Riccardo, 05/11/2026): le "
             "parole nelle grafiche vanno bene anche con i sottotitoli impressi, se sono GRANDI, nella finestra grande o lontane dalla fascia "
             "dei sottotitoli, e a tempo con la voce; segnala «due cose da leggere» SOLO quando due testi grandi si fanno concorrenza nello "
             "stesso momento (una parola grande che ripete la voce mentre c'è il sottotitolo NON è un difetto); è un difetto una piccola "
             "etichetta di testo vicino ai sottotitoli. SOLO TESTO = BOCCIATA (Riccardo, 05/11/2026): una parola o una frase da sola, "
             "anche grande e animata, NON è una grafica. Ogni grafica deve MOSTRARE il concetto con un contenuto visivo (icona o "
             "illustrazione che si anima, diagramma, collegamento fra elementi, contatore, piccola scena con più elementi, disegno "
             "Servier, card con icona); il testo è solo un'etichetta. Se questa grafica è fatta solo di testo, il voto è sotto 7. "
             "Controlla anche che il contenuto visivo dica davvero la cosa detta (un'icona a caso accanto a una parola non basta). "
             "SOPRA IL VIDEO (Riccardo, 06/11/2026): le grafiche si appoggiano sul video, persona e B-roll restano visibili il più "
             "possibile; pannelli pieni solo per momenti forti e brevi (al massimo 2–3 nel reel); icone grandi con profondità e luce "
             "(vetro, card con spessore, bagliore); ogni segno si capisce subito a 390 px (un segno che sembra una cifra è grave); "
             "nella metà bassa di un tutto schermo niente testo."
             + (f" Che cosa dichiara di mostrare il piano: {g['mostra']}." if g.get('mostra') else '')
             + (" È una MICRO-GRAFICA (il livello che riempie i tratti fra le infografiche grandi, densità «piena»): deve notarsi e "
                "leggersi sul telefono (foglio a 390 px), grande e presente nella finestra (niente badge piccoli negli angoli), stare nel "
                "suo riquadro senza coprire volti, mani, sottotitoli o scritte del video." if info_g['modo'] == 'micro' else '')
             + (" È una grafica SULLA PERSONA in camera: controlla che non copra il volto (salvo quando passa dietro di lei) e che "
                "il ritaglio della persona sia pulito." if info_g['modo'] == 'persona' else ''), '', 'DA GUARDARE (Read):']
    righe += [f"- provino ogni 0,25 s: {C.rel(p)}" for p in prov]
    righe += [f"- telefono 390 px (12 momenti): {C.rel(d / (g['nome'] + '_telefono-390px.jpg'))}",
              f"- piena risoluzione: " + ', '.join(C.rel(d / f"{g['nome']}_f{f}.png") for f in cinque)]
    righe += [f"- reference: {C.rel(p)} (24 fotogrammi; la riga in libreria/reference/catalogo.md)" for p in refs]
    if es:
        righe.append(f"- esempio del modello di partenza: {C.rel(es)}")
    righe += ['', "RESTITUISCI: voto 1–10 (minimo 7), motivo in 4–6 frasi (leggibilità sul telefono, gerarchia, luce e presenza rispetto "
              "alla reference, equilibrio 9:16, ritmo sulla voce, tono sanitario), difetti con il fotogramma, al massimo 3 correzioni "
              "concrete, di esecuzione o di impostazione. Severo e preciso; non inventare."]
    (d / 'PROMPT.md').write_text('\n'.join(righe) + '\n', encoding='utf-8')
    return d / 'PROMPT.md'


# ---------------------------------------------------------------- la fase

def rendi(slug, solo=None, laboratorio=False):
    D = C.cartella(slug)
    R = C.leggi(D / 'radiografia.json')
    P = C.leggi(D / 'piano.json')
    ok, a = _approvato(D, 'piano', D / 'piano.json')
    if laboratorio and not P.get('laboratorio'):
        sys.exit(f"{slug}: --laboratorio solo per un piano di laboratorio (\"laboratorio\": true), non per un ad vero")
    if laboratorio:
        print("  LABORATORIO: anteprima di prova senza approvazione del piano (non si consegna)")
    # fase 6, giro 4 (Riccardo, 05/11/2026): il piano non si approva più a parte; basta che passi i controlli (qui sotto).
    # L'ok di Riccardo è sull'anteprima (md5 del video), prima della consegna
    err, avv, info = reel_piano_base.controlla(slug, P, R)
    if err:
        sys.exit(f"{slug}: il piano non passa i controlli:\n  " + '\n  '.join(err))
    fps, nf = R['fps'], R['fotogrammi']
    V = C.AGENTE / R['sorgente']['video']
    L = C.lavoro(slug, 'rendi')
    A = D / 'anteprime'; A.mkdir(exist_ok=True)
    K = D / 'controlli'; K.mkdir(exist_ok=True)
    per_info = {x['nome']: x for x in info['grafiche']}
    G = sorted(P['grafiche'], key=lambda g: g['f0'])
    strati = []
    for g in G:
        pg, mov, h = _mov(g, fps, L)
        strati.append((g, mov, h))
    full = A / f"{slug}_lavoro-intero.mp4"
    senza = A / f"{slug}_lavoro-intero-senza-effetti.mp4"
    # fase 6: zoom leggeri sul video base (intermedio senza perdite), poi le grafiche sopra; effetti sonori a parte
    Vb, zoom_info = V, None
    if P.get('zoom'):
        from . import reel_zoom as RZ
        Vb = L / 'base-zoom.mkv'
        print(f"  zoom leggeri sul video base ({len(P['zoom'])})...", flush=True)
        cambiati = RZ.applica(V, P['zoom'], Vb, fps, nf)
        zoom_info = RZ.verifica(V, Vb, P['zoom'], cambiati, nf)
        zoom_info['zoom'] = [{k: z.get(k) for k in ('nome', 'f0', 'f1', 'scala', 'centro', 'zona', 'curva')} for z in P['zoom']]
    # 07/11/2026 (Riccardo, sera): il video non si abbassa più e i sottotitoli non si ricompongono (vedi reel_sottotitoli)
    eventi_sfx = []
    if any(g.get('suono') for g in G):
        from . import reel_suono as RS
        vis0 = {}
        for g, mov, h in strati:
            cop, _ = alfa(g, mov, fps)
            vis0[g['nome']] = {g['f0'] + k for k, c in enumerate(cop) if c > 0.0005}
        eventi_sfx = RS.eventi_dal_piano(P, vis0, fps)
    # fase 6: modelli sulla persona («dietro»: la sagoma; «pip»: lui nel cerchio)
    extra, dietro_info = {}, {}
    for g, m, _ in strati:
        e = _extra(g)
        if not e:
            continue
        x = {'frames': g['frames']}
        if e.get('dietro'):
            print(f"  sagoma della persona per «{g['nome']}» (Apple Vision)...", flush=True)
            x['maschera'] = sagome(Vb, g, L, fps)
            cp = coperto(m, x['maschera'], g['frames'])
            dietro_info[g['nome']] = {'coperto_medio': round(float(np.mean([c for c in cp if c > 0] or [0])), 3), 'coperto_max': round(max(cp or [0]), 3)}
        if e.get('pip'):
            x['pip'] = e['pip']
        extra[g['nome']] = x
    print("  sovrapposizione di tutte le grafiche...", flush=True)
    base_out = senza if eventi_sfx else full
    reel_grafiche.sovrapponi_molti(Vb, [(m, g['f0'], extra.get(g['nome'])) if g['nome'] in extra else (m, g['f0']) for g, m, _ in strati],
                         base_out, fps, audio_da=V if Vb != V else None)
    prova_sfx = None
    if eventi_sfx:
        print(f"  effetti sonori ({len(eventi_sfx)}) e prova che, tolti, l'audio è l'originale...", flush=True)
        prova_sfx = RS.mixa(senza, V, eventi_sfx, full, L)
    elif senza.exists():
        senza.unlink()
    zone_meta(full, A / f"{slug}_lavoro-intero-ZONE-META.mp4")
    out = {'slug': slug, 'data': f"{datetime.datetime.now():%d/%m/%Y %H:%M}", 'md5_piano': C.md5_file(D / 'piano.json'),
           'video': C.rel(full), 'md5_video': C.md5_file(full), 'grafiche': {}, 'errori': [], 'da_guardare': []}
    # 1. audio e file (con gli effetti sonori l'audio copiato è quello della versione «senza effetti»)
    ma, mo = C.md5_audio(senza if eventi_sfx else full), C.md5_audio(V)
    pr = C.probe(full)
    out['audio'] = {'md5_finale': ma, 'md5_originale': mo, 'identico': ma == mo}
    if ma != mo:
        out['errori'].append(f"audio diverso dall'originale ({ma} / {mo})")
    if eventi_sfx:
        out['video_senza_effetti'] = C.rel(senza)
        out['md5_video_senza_effetti'] = C.md5_file(senza)
        out['effetti_sonori'] = prova_sfx
        if not prova_sfx['esito']:
            out['errori'].append(f"effetti sonori: tolti gli effetti l'audio non torna l'originale (scarto {prova_sfx['scarto_campioni']} campioni, "
                                 f"guadagno {prova_sfx['guadagno_voce']}, residuo {prova_sfx['residuo_senza_effetti_db']} dB contro "
                                 f"{prova_sfx['rumore_della_sola_ricodifica_db']} dB della sola ricodifica)")
        for e in prova_sfx['effetti']:
            if e['rms_effetto_db'] > e['rms_voce_stesso_tratto_db'] - 10:
                out['errori'].append(f"effetto «{e['file']}» su {e['grafica']}: {e['rms_effetto_db']} dB contro la voce {e['rms_voce_stesso_tratto_db']} dB "
                                     "nello stesso tratto (deve stare almeno 10 dB sotto)")
    if dietro_info:
        out['dietro'] = dietro_info
        for n, q in dietro_info.items():
            if q['coperto_medio'] > 0.25:
                out['errori'].append(f"{n}: la persona copre in media il {q['coperto_medio']:.0%} della grafica che le passa dietro (massimo 25%: "
                                     "deve restare leggibile)")
    if zoom_info:
        out['zoom'] = zoom_info
        if not zoom_info['identici_fuori_dallo_zoom']:
            out['errori'].append(f"zoom: fotogrammi cambiati fuori dagli zoom {zoom_info['diversi_fuori_dallo_zoom']}")
        if max(zoom_info['differenza_media_max_livelli'].values()) > 1.0:
            out['errori'].append(f"zoom: i colori medi cambiano di {zoom_info['differenza_media_max_livelli']} livelli")
    out['file'] = pr
    if pr['fotogrammi'] != nf or pr['video']['color_space'] != 'bt709' or pr['video']['color_range'] != 'tv':
        out['errori'].append(f"file finale: {pr['fotogrammi']} fotogrammi (attesi {nf}), {pr['video']}")
    # 2-3. alfa
    cmin = info['corpo_minimo']
    tre = {f for x, y in (R.get('animazioni_3d') or {}).get('fotogrammi', []) for f in range(x, y + 1)}
    visibili, per_f, dom_tutti = {}, {}, {}
    from . import reel_sottotitoli as RSo
    pf_sott = RSo.per_fotogramma(R)
    coperture = {}
    for g, mov, h in strati:
        cop, fuori = alfa(g, mov, fps, pf_sott)
        for f_, v_ in alfa.bande.items():
            coperture[f_] = max(coperture.get(f_, (0.0, 0.0)), v_)
        vis = {g['f0'] + k for k, c in enumerate(cop) if c > 0.0005}
        visibili[g['nome']] = vis
        o = {'catalogo': per_info[g['nome']]['catalogo'], 'modo': g['modo'], 'mov': C.rel(mov), 'hash_pagina': h,
             'visibile': _corse(vis), 'tempi': [[round(x / fps, 3), round((y + 1) / fps, 3)] for x, y in _corse(vis)]}
        tg = getattr(alfa, 'tagli', [])
        if g['modo'] in ('micro', 'persona', 'palco') and tg:
            o['alfa_max_sul_bordo_del_riquadro'] = max(tg)
            if max(tg) > 24:
                out['errori'].append(f"{g['nome']}: la grafica tocca il bordo del suo riquadro (alfa {max(tg)}): bagliore, ombra o forma "
                                     "tagliati in un rettangolo; allarga il riquadro o rimpicciolisci")
        if _zona(g, 0):
            o['alfa_max_fuori_finestra'] = max(fuori) if fuori else 0
            if o['alfa_max_fuori_finestra'] > 2:
                out['errori'].append(f"{g['nome']}: alfa {o['alfa_max_fuori_finestra']} fuori dalla finestra")
        if g['modo'] == 'tutto schermo' and vis & tre:
            out['errori'].append(f"{g['nome']}: tutto schermo sulle 3D, fotogrammi {_corse(vis & tre)}")
        out['grafiche'][g['nome']] = o
        for f in vis:
            r = _zona(g, (f - g['f0']) / fps)
            per_f[f] = (g['nome'], [r['x'], r['y'], r['x'] + r['w'] - 1, r['y'] + r['h'] - 1] if r else [0, 0, W - 1, H - 1])
    nomi = list(visibili)
    for i, x in enumerate(nomi):
        for y in nomi[i + 1:]:
            s = visibili[x] & visibili[y]
            if s:
                out['errori'].append(f"{x} e {y} si sovrappongono: fotogrammi {_corse(s)}")
    # passaggi fra grafiche vicine
    ordine = sorted(((min(v), max(v), k) for k, v in visibili.items() if v))
    out['passaggi'] = [{'da': a[2], 'a': b[2], 'ultimo': a[1], 'primo': b[0], 'video_base_in_mezzo': b[0] - a[1] - 1}
                       for a, b in zip(ordine, ordine[1:]) if b[0] - a[1] - 1 < 15]
    # 4-5. solo testo e testo della pagina
    for g, mov, h in strati:
        o = out['grafiche'][g['nome']]
        vis = visibili[g['nome']]
        print(f"  controlli del testo: {g['nome']} ({len(vis)} fotogrammi)...", flush=True)
        bb = solo_testo(g, vis, fps, L)
        tut = [b for b in bb.values() if b]
        o['testo_ingombro'] = [min(b[0] for b in tut), min(b[1] for b in tut), max(b[2] for b in tut), max(b[3] for b in tut)] if tut else None
        fz = [(f, b) for f, b in bb.items() if b and (b[0] < SAFE[0] or b[1] < SAFE[1] or b[2] > SAFE[2] or b[3] > SAFE[3])]
        if _zona(g, 0):
            for f, b in bb.items():
                r = _zona(g, (f - g['f0']) / fps)
                if b and (b[0] < r['x'] or b[1] < r['y'] or b[2] > r['x'] + r['w'] - 1 or b[3] > r['y'] + r['h'] - 1):
                    fz.append((f, b))
        o['testo_fuori'] = fz[:20]
        o['testo_fotogrammi_misurati'] = len(bb)
        if fz:
            out['errori'].append(f"{g['nome']}: testo fuori dalla zona sicura o dalla finestra in {len(fz)} fotogrammi (primo f{fz[0][0]} {fz[0][1]})")
        fd = dom(g, fps, L)
        for f in vis:
            dom_tutti[f] = fd[f - g['f0']]
        td = controlla_testo_dom(g, fd, vis, R, cmin)
        o['pagina'] = td
        for e in td['cifre_non_dette'][:10]:
            out['errori'].append(f"{g['nome']}: cifra non detta «{e['cifra']}» in «{e['testo']}» al fotogramma {e['f']}")
        for e in td['parole_non_dette']:
            out['errori'].append(f"{g['nome']}: «{e['parola']}» (in «{e['testo']}», dal fotogramma {e['da_f']}) non è nell'SRT")
        for e in td['corpo_sotto_minimo']:
            out['errori'].append(f"{g['nome']}: «{e['testo']}» a corpo {e['corpo_effettivo']}, minimo {e['minimo']}")
    # 1 bis. i sottotitoli impressi non si toccano (Riccardo, 07/11/2026): o fascia uguale all'originale, o coperta del tutto
    print("  sottotitoli: fascia uguale all'originale o coperta del tutto...", flush=True)
    so = RSo.controlla(full, V, R, coperture, [(g['f0'], g['frames'], m) for g, m, _ in strati], fps, L, Vb=Vb)
    out['sottotitoli'] = so
    out['errori'] += so['errori']
    # 2. SSIM
    print("  SSIM fuori dalle grafiche...", flush=True)
    tutte = set().union(*visibili.values()) if visibili else set()
    fuori = [f for f in range(nf) if f not in tutte]
    out['ssim'] = {'senza_grafiche': ssim(full, Vb, fuori, L=L, nome='ssim-fuori')}
    for g, mov, h in strati:
        if not _zona(g, 0):
            continue
        vis = sorted(visibili[g['nome']])
        if g['modo'] == 'finestra':
            rr_ = g['elementi'][0]['dati']['rett']
            rr_ = [rr_] if isinstance(rr_, dict) else rr_
        else:
            rr_ = [_zona(g, 0)]
        ys = min(q['y'] for q in rr_)
        ye = max(q['y'] + q['h'] for q in rr_)
        # giro 5: un'infografica sopra il video con il riquadro a tutto fotogramma non ha zone «sopra» o «sotto» da misurare
        if ys - 2 >= 16:
            out['ssim'][f"{g['nome']}: sopra la finestra"] = ssim(full, Vb, vis, crop=(0, 0, W, ys - 2), L=L, nome=f"ssim-{g['nome']}-sopra")
        if H - ye - 2 >= 16:
            out['ssim'][f"{g['nome']}: sotto la finestra"] = ssim(full, Vb, vis, crop=(0, ye + 2, W, (H - ye - 2) // 2 * 2), L=L, nome=f"ssim-{g['nome']}-sotto")
    # fase 6: un video di camera con la grana perde più di 0,01 di SSIM già con la sola ricodifica (prova con la persona:
    # 0,983-0,989). Sotto 0,99 si misura la stessa SSIM su una ricodifica pulita del base (stessi fotogrammi, stesso
    # ritaglio): è errore solo se il video di lavoro perde più di 0,008 rispetto a quella. Perché 0,008: nella prova con la
    # persona i fotogrammi senza grafica sono identici bit per bit alla ricodifica pulita, e in quelli con la grafica
    # (alfa 0 fuori dal riquadro, misurato) x264 spende i bit sulla grafica e il resto perde ~0,006 sul girato con la grana
    rif = None
    for k, s in out['ssim'].items():
        if s and s['medio'] is not None and s['medio'] < SSIM_MIN:
            if rif is None:
                rif = L / 'ricodifica.mp4'
                if not rif.exists():
                    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(Vb), '-an', *reel_grafiche.ENC, '-fps_mode', 'passthrough', str(rif)], check=True)
            fr = s.pop('_fotogrammi')
            b = ssim(rif, Vb, fr, crop=s['ritaglio'], L=L, nome='ssim-rif')
            s['ricodifica_pulita'] = b['medio']
            s['soglia'] = round(min(SSIM_MIN, b['medio'] - 0.008), 5)
            if s['medio'] < s['soglia']:
                out['errori'].append(f"SSIM {k}: {s['medio']:.5f} sotto {s['soglia']} (ricodifica pulita {b['medio']:.5f})")
    for s in out['ssim'].values():
        if s:
            s.pop('_fotogrammi', None)
    # 6. Vision
    print(f"  Apple Vision su {len(per_f)} fotogrammi con grafiche...", flush=True)
    verifiche = C.leggi(D / 'verifiche.json', {})
    out['vision'] = vision_cifre(full, per_f, dom_tutti, set(R['numeri_detti']), L, D, verifiche)
    for q in out['vision']['da_guardare']:
        out['da_guardare'].append(f"Vision legge «{q['letto']}» nei fotogrammi {q['f0']}-{q['f1']} ({q['n']}, {q['grafica']}, la pagina lì mostra "
                                  f"«{q['pagina']}»): guardare {q['ritaglio']} e segnare con ./mve reel-guardato {slug} \"{q['chiave']}\" \"motivo\"")
    out['avvisi_piano'] = avv
    # anteprime e provini
    print("  anteprime e provini...", flush=True)
    for g, mov, h in strati:
        vis = visibili[g['nome']]
        f0, f1 = min(vis), max(vis)
        a_, b_ = max(0, f0 / fps - 3), min(nf / fps, (f1 + 1) / fps + 3)
        for vecchio in list(A.glob(f"{slug}_{g['nome']}-anteprima-*.mp4")) + list(A.glob(f"provino-{g['nome']}-*.jpg")):
            vecchio.unlink()
        # fase 6: l'anteprima si taglia dal video di lavoro (con zoom ed effetti sonori, se ci sono)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{a_:.3f}", '-t', f"{b_ - a_:.3f}", '-i', str(full), *reel_grafiche.ENC, '-c:a', 'aac',
                        '-b:a', '192k', '-movflags', '+faststart', str(A / f"{slug}_{g['nome']}-anteprima-{a_:.1f}-{b_:.1f}s.mp4")], check=True)
        _provino(full, f0, f1, fps, A / f"provino-{g['nome']}-{f0 / fps:.2f}-{(f1 + 1) / fps:.2f}s-ogni-0,25s.jpg")
    # pacchi del direttore
    out['direttore'] = {}
    per_g = {g['nome']: g for g in G}
    for n in visibili:
        out['direttore'][n] = C.rel(pacco_direttore(slug, per_g[n], per_info[n], full, visibili[n], R, L))
    C.scrivi(K / 'controlli.json', out)
    if P.get('palco'):
        # 07/11/2026: la tavola che mette accanto a ogni scena il fotogramma della reference verticale da cui nasce, e il voto
        # del reel intero sulla coerenza del palco
        from . import reel_palco as RPal
        tav = A / f"{slug}_tavola-scene-reference.jpg"
        RPal.tavola(slug, full, tav)
        out['tavola_reference'] = C.rel(tav)
        out['direttore']['_insieme'] = C.rel(RPal.pacco_insieme(slug, full, tav))
        C.scrivi(K / 'controlli.json', out)
    elif P.get('densita') == 'piena':
        from . import reel_piano as RP
        out['direttore']['_insieme'] = C.rel(RP.pacco_insieme(slug))
        C.scrivi(K / 'controlli.json', out)
    scrivi_md(out, R, K / 'controlli.md')
    for e in out['errori']:
        print('  ERRORE', e)
    for e in out['da_guardare']:
        print('  da guardare', e)
    print(f"{slug}: {C.rel(full)} ({len(out['errori'])} errori, {len(out['da_guardare'])} da guardare). Controlli: {C.rel(K / 'controlli.md')}")
    if out['errori']:
        sys.exit(1)
    print("  ADESSO: voto del direttore artistico per ogni grafica (subagente direttore-reel con il PROMPT.md di "
          f".lavoro/{slug}/direttore/<grafica>/), ./mve reel-voto; poi QUI CI SI FERMA: l'ANTEPRIMA va a Riccardo, che dice cosa "
          "migliorare (si rifà un'anteprima nuova) o la approva (./mve reel-approva <slug> anteprime, poi la consegna).")


def scrivi_md(o, R, out):
    fps = R['fps']
    L = [f"# Controlli automatici: {o['slug']}", '', f"`./mve reel-rendi` del {o['data']}. Video: `{o['video']}` (md5 `{o['md5_video']}`), "
         f"piano md5 `{o['md5_piano']}`.", '',
         f"**Esito: {'NESSUN ERRORE' if not o['errori'] else str(len(o['errori'])) + ' ERRORI'}**, {len(o['da_guardare'])} cose da guardare.", '']
    L += [f"- ERRORE: {e}" for e in o['errori']]
    L += [f"- da guardare: {e}" for e in o['da_guardare']]
    L += ['', '## File e audio', '',
          f"- {o['file']['fotogrammi']} fotogrammi, {o['file']['larghezza']}×{o['file']['altezza']}, {o['file']['video']}",
          f"- audio: md5 del flusso `{o['audio']['md5_finale']}`, originale `{o['audio']['md5_originale']}`: "
          f"{'**identico**' if o['audio']['identico'] else '**DIVERSO**'}" + (f" (è la versione senza effetti sonori: `{o['video_senza_effetti']}`, md5 "
          f"`{o['md5_video_senza_effetti']}`)" if o.get('video_senza_effetti') else '')]
    if o.get('effetti_sonori'):
        e = o['effetti_sonori']
        L += ['', '## Effetti sonori (fase 6)', '',
              f"- {len(e['effetti'])} effetti, codifica {e['codifica']}, voce (RMS del parlato) {e['voce_rms_db']} dB; picco del mix {e['picco_mix']} dBFS.",
              f"- **Prova** (tolti gli effetti dal file finale e confrontato con l'audio originale): scarto {e['scarto_campioni']} campioni, guadagno "
              f"{e['guadagno_voce']}, residuo {e['residuo_senza_effetti_db']} dB ({e['residuo_sotto_il_segnale_db']} dB sotto il segnale); la sola "
              f"ricodifica dell'originale dà {e['rumore_della_sola_ricodifica_db']} dB (differenza {e['differenza_dal_rumore_di_codifica_db']:+.1f} dB): "
              f"**{'l audio è l originale' if e['esito'] else 'NON TORNA'}**.", '',
              '| grafica | effetto | t (s) | sotto la voce (richiesto) | RMS effetto | RMS voce nello stesso tratto |', '|---|---|---|---|---|---|']
        L += [f"| {d['grafica']} | {d['file']} | {d['t']:.2f} | {d['db_sotto_voce']} dB | {d['rms_effetto_db']} dB | {d['rms_voce_stesso_tratto_db']} dB |"
              for d in e['effetti']]
    if o.get('zoom'):
        z = o['zoom']
        L += ['', '## Zoom sul video base (fase 6)', '',
              f"- {len(z['zoom'])} zoom, {z['fotogrammi_con_zoom']} fotogrammi cambiati; fuori dagli zoom i fotogrammi del base sono "
              f"{'**identici bit per bit**' if z['identici_fuori_dallo_zoom'] else '**DIVERSI** ' + str(z['diversi_fuori_dallo_zoom'])}; "
              f"colori medi: differenza massima {z['differenza_media_max_livelli']} livelli."]
        L += [f"  - {q['nome']}: f{q['f0']}–{q['f1']}, scala {q['scala']}, centro {q['centro']}, {q.get('zona') or 'tutto'}, {q.get('curva') or 'spinta'}" for q in z['zoom']]
    L += ['', '## Grafiche', '',
          '| grafica | modello | modo | visibile (fotogrammi) | tempi (s) | testo: ingombro, fuori zona | cifre non dette (pagina) | parole non dette | corpo |',
          '|---|---|---|---|---|---|---|---|---|']
    for n, g in o['grafiche'].items():
        p = g.get('pagina', {})
        L.append(f"| {n} | `{g['catalogo']}` | {g['modo']} | " + ', '.join(f"{a}–{b}" for a, b in g['visibile']) + ' | '
                 + ', '.join(f"{a:.3f}–{b:.3f}" for a, b in g['tempi']) + f" | {g.get('testo_ingombro')}, {len(g.get('testo_fuori', []))} su "
                 f"{g.get('testo_fotogrammi_misurati')} | {len(p.get('cifre_non_dette', []))} | {len(p.get('parole_non_dette', []))} | "
                 f"{'ok' if not p.get('corpo_sotto_minimo') else p['corpo_sotto_minimo']} |")
    L += ['', '**Testi scritti** (fermi almeno 3 fotogrammi, letti dalla pagina):', '']
    for n, g in o['grafiche'].items():
        L.append(f"- {n}: " + ' / '.join(f"«{t}»" for t in g.get('pagina', {}).get('testi_scritti', [])))
    L += ['', '## Video uguale fuori dalle grafiche (SSIM)', '']
    for k, s in o['ssim'].items():
        if s and s.get('medio') is not None:
            L.append(f"- {k}: medio {s['medio']:.5f}, minimo {s['minimo']:.5f} su {s['fotogrammi']} fotogrammi"
                     + (f" (sotto 0,99: ricodifica pulita {s['ricodifica_pulita']:.5f}, soglia {s['soglia']})" if s.get('soglia') else ''))
    v = o['vision']
    L += ['', '## Apple Vision: cifre', '', f"- fotogrammi letti {v['fotogrammi_letti']}, righe dentro le grafiche {v['righe_nelle_grafiche']}, "
          f"con cifre {v['righe_con_cifre']}, spiegate dalla pagina {v['spiegate']}, guardate dall'agente {len(v['guardate'])}, "
          f"da guardare {len(v['da_guardare'])}"]
    L[-1] = L[-1].replace('guardate dall', 'gruppi guardati dall').replace('da guardare', 'gruppi da guardare')
    L += [f"  - {q['chiave']} ({q['n']} fotogrammi, {q['grafica']}, pagina «{q['pagina']}»): {q['guardato']}" for q in v['guardate']]
    L += [f"  - DA GUARDARE {q['chiave']} ({q['n']} fotogrammi, {q['grafica']}, pagina «{q['pagina']}»): `{q['ritaglio']}`" for q in v['da_guardare']]
    L += ['', '## Passaggi fra grafiche vicine', '']
    L += [f"- {p['da']} → {p['a']}: ultimo {p['ultimo']}, primo {p['primo']}, video base in mezzo {p['video_base_in_mezzo']} fotogrammi"
          for p in o['passaggi']] or ['- nessuna grafica vicina a un\'altra']
    if o.get('avvisi_piano'):
        L += ['', '## Dal piano (da guardare)', ''] + [f"- {a}" for a in o['avvisi_piano']]
    L += ['', '## Direttore artistico', ''] + [f"- {n}: `{p}`" for n, p in o['direttore'].items()]
    out.write_text('\n'.join(L) + '\n', encoding='utf-8')

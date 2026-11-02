"""Fase `libreria`: l'indice del B-roll comune (libreria/broll/<tema>/...).

Non riguarda un video: `./mve libreria`. Rilanciabile: rifa solo i file nuovi o
cambiati (dimensione o data diverse), e un file spostato o duplicato si
riconosce dall'hash, senza rianalizzarlo.

Per ogni clip:
- tecnica: durata, risoluzione, fps, codec, hash SHA-1 (i file identici sono
  una clip sola: si tiene il primo in ordine di percorso, gli altri sono
  `doppioni`);
- volti (Apple Vision, ogni 0,5 s): quanti al massimo, quanto grandi (altezza
  del volto sull'altezza del quadro), in che quota dei campioni;
- movimento: lo spostamento globale dell'immagine fra due fotogrammi
  (correlazione di fase a 320x180, con interpolazione sub-pixel) misura il
  movimento di camera in % della larghezza al secondo; la sua parte veloce, tolta
  la media su 0,5 s, e il tremolio (camera a mano). La differenza media fra
  fotogrammi misura quanto cambia l'immagine (anche per chi si muove in scena),
  la varianza del laplaciano la nitidezza (bassa = mosso o sfocato);
- il tratto piu stabile di 3-6 s (minimo movimento + tremolio di camera).

Descrizioni: `./mve libreria` prepara fogli da 16 clip (4x4, il fotogramma
centrale con il numero) in libreria/.indice/fogli/. Chi li guarda scrive
libreria/.indice/descrizioni/<tema>.json, una voce per clip:
  {"num": 3, "id": "<id del foglio>", "parte": "collo", "azione": "...",
   "inquadratura": "dettaglio|medio|largo", "difetti": "...", "voto": 1-5}
Le descrizioni restano legate all'id (hash), non al numero: sopravvivono ai
rilanci. Escono libreria/indice.json (per il motore) e libreria/indice.md.

Esclusioni: libreria/.indice/esclusioni.json, una voce per clip esclusa
({"id", "file", "motivi": [...], "fonti": [...]}), legata all'id. Nell'indice la
clip resta (con `esclusa`: i motivi), ma il motore sceglie il B-roll solo con
`utilizzabili()`, che non la restituisce mai.
"""
import concurrent.futures as cf
import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import numpy as np

from .progetto import LIBRERIA, RISORSE, leggi, scrivi, lavori

BROLL = LIBRERIA / 'broll'
INDICE = LIBRERIA / '.indice'
VIDEO = {'.mp4', '.mov', '.m4v', '.mxf'}
W_M, H_M = 320, 180            # risoluzione dell'analisi del movimento
VERSIONE = 1                   # si alza quando cambia l'analisi: rifa tutto


# ------------------------------------------------------------------ tecnica
def _sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as fh:
        for b in iter(lambda: fh.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def _probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_streams', '-show_format',
                        str(p)], capture_output=True, text=True)
    d = json.loads(r.stdout or '{}')
    v = next((s for s in d.get('streams', []) if s.get('codec_type') == 'video'), None)
    if not v:
        return None
    return {'durata': round(float(d['format'].get('duration') or 0), 3), 'w': int(v['width']),
            'h': int(v['height']), 'fps': v.get('r_frame_rate'), 'codec': v.get('codec_name'),
            'audio': any(s.get('codec_type') == 'audio' for s in d['streams'])}


def _shift(fa, fb):
    """spostamento (dx, dy) in pixel fra due fotogrammi gia trasformati, con picco sub-pixel"""
    R = fa * np.conj(fb)
    R /= np.abs(R) + 1e-9
    r = np.fft.ifft2(R).real
    y, x = np.unravel_index(np.argmax(r), r.shape)
    H, W = r.shape

    def sub(m, n, ax):
        a = r[(m - 1) % n, x] if ax == 0 else r[y, (m - 1) % n]
        b = r[m, x] if ax == 0 else r[y, m]
        c_ = r[(m + 1) % n, x] if ax == 0 else r[y, (m + 1) % n]
        den = a - 2 * b + c_
        return m + (0.5 * (a - c_) / den if abs(den) > 1e-12 else 0.0)
    yy, xx = sub(y, H, 0), sub(x, W, 1)
    if yy > H / 2:
        yy -= H
    if xx > W / 2:
        xx -= W
    return xx, yy


def _movimento(p, fps):
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'error', '-i', str(p), '-an',
           '-vf', f'scale={W_M}:{H_M}:flags=area,format=gray', '-f', 'rawvideo', '-']
    raw = subprocess.run(cmd, capture_output=True).stdout
    F = np.frombuffer(raw, np.uint8).reshape(-1, H_M, W_M).astype(np.float32)
    n = len(F)
    if n < 3:
        return None
    win = np.outer(np.hanning(H_M), np.hanning(W_M)).astype(np.float32)
    sh, prec = [], np.fft.fft2((F[0] - F[0].mean()) * win)
    for f in F[1:]:                       # due trasformate alla volta: 600 tutte insieme sono 550 MB
        cur = np.fft.fft2((f - f.mean()) * win)
        sh.append(_shift(prec, cur))
        prec = cur
    sh = np.array(sh)                                                             # px/frame
    vel = np.hypot(sh[:, 0], sh[:, 1]) * fps / W_M * 100                         # % larghezza/s
    k = max(1, int(round(fps / 2)))
    media = np.vstack([np.convolve(sh[:, j], np.ones(k) / k, mode='same') for j in (0, 1)]).T
    trem = np.hypot(*(sh - media).T) * fps / W_M * 100
    diff = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2))
    lap = F[:, :-2, 1:-1] + F[:, 2:, 1:-1] + F[:, 1:-1, :-2] + F[:, 1:-1, 2:] - 4 * F[:, 1:-1, 1:-1]
    nit = lap.reshape(n, -1).var(axis=1)
    # tratto piu stabile: finestra di 6 s (o la clip intera se piu corta), minimo
    # di movimento + tremolio di camera
    score = vel + 2 * trem
    L = int(round(min(6.0, (n - 1) / fps) * fps))
    if L < 1:
        return None
    cs = np.concatenate([[0], np.cumsum(score)])
    medie = (cs[L:] - cs[:-L]) / L
    i0 = int(np.argmin(medie))
    return {
        'camera_pct_s': round(float(np.median(vel)), 1),
        'camera_pct_s_p90': round(float(np.percentile(vel, 90)), 1),
        'tremolio_pct_s': round(float(np.median(trem)), 1),
        'diff_media': round(float(diff.mean()), 2),
        'diff_p95': round(float(np.percentile(diff, 95)), 2),
        'nitidezza': round(float(np.median(nit)), 1),
        'stabile': {'s': round(i0 / fps, 2), 'e': round((i0 + L) / fps, 2),
                    'camera_pct_s': round(float(np.mean(vel[i0:i0 + L])), 1),
                    'tremolio_pct_s': round(float(np.mean(trem[i0:i0 + L])), 1)},
    }


def _volti(p):
    from .visione import binario
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'v.json'
        r = subprocess.run([str(binario()), 'volti', str(p), '0.5', str(out)],
                           capture_output=True, text=True)
        if r.returncode or not out.exists():
            return {'errore': (r.stderr or 'visione senza uscita')[-200:]}
        c = json.loads(out.read_text())['campioni']
    vv = [[v for v in x['volti'] if v['conf'] > 0.6 and v['w'] > 0.02] for x in c]
    alt = [v['h'] for x in vv for v in x]
    return {'max': max((len(x) for x in vv), default=0),
            'quota': round(sum(1 for x in vv if x) / len(vv), 2) if vv else 0.0,
            'altezza_max': round(max(alt), 3) if alt else 0.0,
            'altezza_mediana': round(float(np.median(alt)), 3) if alt else 0.0}


def _fotogramma(p, durata, dst):
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-loglevel', 'error', '-y', '-ss',
                    f'{durata / 2:.3f}', '-i', str(p), '-frames:v', '1', '-vf', 'scale=480:-2',
                    '-q:v', '3', str(dst)], check=False)


def _analizza(args):
    """una clip (gira in un processo a parte): tutto tranne i volti"""
    p, h = args
    info = _probe(p)
    if not info:
        return {'errore': 'nessun flusso video'}
    fps = float(Fraction(info['fps'])) if info['fps'] else 30.0
    info['movimento'] = _movimento(p, fps)
    _fotogramma(p, info['durata'], INDICE / 'fotogrammi' / f'{h[:12]}.jpg')
    return info


# ------------------------------------------------------------------ fogli
def _fogli(tema, clips):
    from PIL import Image, ImageDraw, ImageFont
    cart = INDICE / 'fogli'
    cart.mkdir(parents=True, exist_ok=True)
    for f in cart.glob(f'{tema}-*.jpg'):
        f.unlink()
    font = ImageFont.truetype(str(RISORSE / 'fonts/Montserrat-VF.ttf'), 34)
    font.set_variation_by_axes([800])
    tw, th = 480, 270
    for k in range(0, len(clips), 16):
        gruppo = clips[k:k + 16]
        im = Image.new('RGB', (tw * 4 + 5 * 6, th * 4 + 5 * 6), (20, 20, 20))
        d = ImageDraw.Draw(im)
        for i, c in enumerate(gruppo):
            x, y = 6 + (i % 4) * (tw + 6), 6 + (i // 4) * (th + 6)
            fp = INDICE / 'fotogrammi' / f"{c['id']}.jpg"
            if fp.exists():
                t = Image.open(fp).convert('RGB')
                t.thumbnail((tw, th))
                im.paste(t, (x + (tw - t.width) // 2, y + (th - t.height) // 2))
            lab = f"{c['num']}"
            bw = d.textlength(lab, font=font) + 20
            d.rectangle([x, y, x + bw, y + 46], fill=(0, 0, 0))
            d.text((x + 10, y + 4), lab, font=font, fill=(114, 250, 147))
        im.save(cart / f'{tema}-{k // 16 + 1:02d}.jpg', quality=88)
    # la legenda del foglio: numero -> id e file
    scrivi(cart / f'{tema}.json', [{'num': c['num'], 'id': c['id'], 'file': c['file'],
                                    'durata': c['durata']} for c in clips])
    return -(-len(clips) // 16)


# ------------------------------------------------------------------ indice
def libreria():
    if not BROLL.is_dir():
        sys.exit(f"manca {BROLL}")
    if not any(p.suffix.lower() in VIDEO for p in BROLL.rglob('*')):
        print("libreria/broll/ e vuota: niente da catalogare (senza B-roll il video esce senza B-roll)")
        return
    INDICE.mkdir(exist_ok=True)
    cache_p = INDICE / 'tecnica.json'
    cache = leggi(cache_p) if cache_p.exists() else {}
    if cache.get('_versione') != VERSIONE:
        cache = {'_versione': VERSIONE}
    temi = sorted(d.name for d in BROLL.iterdir() if d.is_dir() and any(
        f.suffix.lower() in VIDEO for f in d.rglob('*')))          # cartelle vuote: ignorate
    files = sorted(p for t in temi for p in (BROLL / t).rglob('*') if p.is_file() and p.suffix.lower() in VIDEO)
    print(f"{len(files)} clip in {len(temi)} cartelle ({', '.join(temi)})")

    # 1. hash, solo dove dimensione o data sono cambiate
    per_hash = {v['hash']: v for k, v in cache.items() if not k.startswith('_') and 'hash' in v}
    voci, da_fare, riusate = {}, [], 0
    for p in files:
        rel = str(p.relative_to(LIBRERIA))
        st = p.stat()
        old = cache.get(rel)
        if old and old.get('byte') == st.st_size and old.get('mtime') == int(st.st_mtime):
            voci[rel] = old
            continue
        h = _sha1(p)
        base = {'byte': st.st_size, 'mtime': int(st.st_mtime), 'hash': h}
        if h in per_hash and 'tecnica' in per_hash[h]:
            voci[rel] = dict(per_hash[h], **base)                    # stesso contenuto: si riusa
            riusate += 1
        else:
            voci[rel] = base
            da_fare.append((rel, p, h))
    print(f"  {len(files) - len(da_fare)} gia analizzate ({riusate} ricontrollate: cambiate, spostate o "
          f"doppie, stesso contenuto), {len(da_fare)} da analizzare")

    # 2. analisi tecnica (processi) e volti (Vision, thread)
    if da_fare:
        uniche = {}
        for rel, p, h in da_fare:
            uniche.setdefault(h, (rel, p))
        t0 = datetime.datetime.now()
        with cf.ProcessPoolExecutor(lavori(max(2, (os.cpu_count() or 4) - 4))) as ex:
            tec = dict(zip(uniche, ex.map(_analizza, [(p, h) for h, (_, p) in uniche.items()], chunksize=4)))
        print(f"  movimento e fotogrammi: {(datetime.datetime.now() - t0).total_seconds():.0f} s")
        t0 = datetime.datetime.now()
        with cf.ThreadPoolExecutor(lavori(4)) as ex:
            vol = dict(zip(uniche, ex.map(_volti, [p for _, p in uniche.values()])))
        print(f"  volti (Vision): {(datetime.datetime.now() - t0).total_seconds():.0f} s")
        for rel, p, h in da_fare:
            voci[rel]['tecnica'] = tec[h]
            voci[rel]['volti'] = vol[h]
    scrivi(cache_p, dict(voci, _versione=VERSIONE))

    # 3. una clip per contenuto; numeri per cartella; descrizioni per id
    gruppi = {}
    for rel in sorted(voci):
        gruppi.setdefault(voci[rel]['hash'], []).append(rel)
    descr = {}
    for f in sorted((INDICE / 'descrizioni').glob('*.json')) if (INDICE / 'descrizioni').is_dir() else []:
        for x in leggi(f):
            if x.get('id'):
                descr[x['id']] = {k: x.get(k) for k in ('parte', 'azione', 'inquadratura', 'difetti', 'voto')}
    escl_p = INDICE / 'esclusioni.json'
    escluse = {e['id']: e['motivi'] for e in leggi(escl_p)} if escl_p.exists() else {}
    clips, per_tema = [], {t: [] for t in temi}
    for h, rels in gruppi.items():
        rel = rels[0]
        v = voci[rel]
        t = v['tecnica'] or {}
        c = {'id': h[:12], 'file': rel, 'tema': rel.split('/')[1], 'doppioni': rels[1:], 'hash': h,
             'durata': t.get('durata'), 'w': t.get('w'), 'h': t.get('h'), 'fps': t.get('fps'),
             'codec': t.get('codec'), 'audio': t.get('audio'), 'movimento': t.get('movimento'),
             'volti': v.get('volti'), 'errore': t.get('errore'), 'descrizione': descr.get(h[:12]),
             'esclusa': escluse.get(h[:12])}
        per_tema[c['tema']].append(c)
    for tema in temi:
        per_tema[tema].sort(key=lambda c: c['file'])
        for i, c in enumerate(per_tema[tema], 1):
            c['num'] = i
            clips.append(c)
    fogli = {tema: _fogli(tema, per_tema[tema]) for tema in temi}

    # 4. uscite
    riass = {}
    for tema in temi:
        cc = per_tema[tema]
        dd = [c['durata'] or 0 for c in cc]
        riass[tema] = {'clip': len(cc), 'doppioni_tolti': sum(len(c['doppioni']) for c in cc),
                       'durata_min': round(sum(dd) / 60, 1),
                       'mediana_s': round(float(np.median(dd)), 1) if dd else 0,
                       'descritte': sum(1 for c in cc if c['descrizione']),
                       'escluse': sum(1 for c in cc if c['esclusa']), 'fogli': fogli[tema]}
    scrivi(LIBRERIA / 'indice.json', {
        'generato': datetime.datetime.now().isoformat(timespec='seconds'), 'versione': VERSIONE,
        'unita': {'camera_pct_s': '% della larghezza del quadro al secondo',
                  'volti.altezza': "frazione dell'altezza del quadro",
                  'stabile': "secondi dall'inizio della clip"},
        'cartelle': riass, 'clip': clips})
    _md(temi, per_tema, riass)
    nd = sum(1 for c in clips if not c['descrizione'])
    orfane = set(escluse) - {c['id'] for c in clips}
    print(f"   {sum(1 for c in clips if c['esclusa'])} clip escluse (libreria/.indice/esclusioni.json)"
          + (f"; {len(orfane)} esclusioni senza clip (file tolti?)" if orfane else ""))
    print(f"-> libreria/indice.json, libreria/indice.md ({len(clips)} clip uniche, "
          f"{sum(r['doppioni_tolti'] for r in riass.values())} doppioni)")
    print(f"   fogli in libreria/.indice/fogli/ ({sum(fogli.values())});"
          f" {nd} clip senza descrizione" + (" -> libreria/.indice/descrizioni/<tema>.json" if nd else ""))


def da_catalogare():
    """le clip di libreria/broll/ che l'indice non conosce ancora o che non hanno una
    descrizione: prima di scegliere un B-roll si lancia ./mve libreria e si
    descrivono (v1.0: ogni collaboratore mette i suoi B-roll, l'agente li cataloga da solo)"""
    if not BROLL.is_dir():
        return []
    files = sorted(str(p.relative_to(LIBRERIA)) for p in BROLL.rglob('*')
                   if p.is_file() and p.suffix.lower() in VIDEO and not p.name.startswith('.'))
    if not files or not (LIBRERIA / 'indice.json').exists():
        return files
    d = leggi(LIBRERIA / 'indice.json')
    pronte = {c['file'] for c in d['clip'] if c.get('descrizione')}
    pronte |= {x for c in d['clip'] if c.get('descrizione') for x in c.get('doppioni', [])}
    return [f for f in files if f not in pronte]


def utilizzabili(voto_min=4, tema=None, indice=None):
    """le clip che il motore puo scegliere: mai le escluse, mai quelle senza
    descrizione o con voto sotto voto_min. L'unico modo previsto per scegliere B-roll.
    Senza indice (libreria vuota o mai catalogata): nessuna."""
    if indice is None and not (LIBRERIA / 'indice.json').exists():
        return []
    d = indice or leggi(LIBRERIA / 'indice.json')
    return [c for c in d['clip'] if not c.get('esclusa') and c.get('descrizione')
            and (c['descrizione'].get('voto') or 0) >= voto_min and (tema is None or c['tema'] == tema)
            and not c.get('errore')]


def _md(temi, per_tema, riass):
    L = ["# Indice del B-roll", "",
         "Generato da `./mve libreria`: non modificarlo a mano (le descrizioni stanno in "
         "`.indice/descrizioni/`). Camera e tremolio in % della larghezza del quadro al secondo; "
         "volti: quanti al massimo / altezza massima del volto sul quadro; stabile: il tratto di "
         "3-6 s con meno movimento di camera.", ""]
    L += ["| cartella | clip | doppioni tolti | escluse | durata | mediana | descritte |",
          "|---|---|---|---|---|---|---|"]
    L += [f"| {t} | {r['clip']} | {r['doppioni_tolti']} | {r['escluse']} | {r['durata_min']} min | "
          f"{r['mediana_s']} s | {r['descritte']} |" for t, r in riass.items()]
    for t in temi:
        L += ["", f"## {t}", "",
              "| n | file | durata | volti | camera | tremolio | stabile | parte | cosa succede | inquadratura | difetti | voto |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for c in per_tema[t]:
            m, v, d = c['movimento'] or {}, c['volti'] or {}, c['descrizione'] or {}
            st = m.get('stabile') or {}
            L.append(f"| {c['num']} | {c['file'].split('/', 2)[2]}{' (+' + str(len(c['doppioni'])) + ' doppione)' if c['doppioni'] else ''} "
                     f"| {(c['durata'] or 0):.1f} s | {v.get('max', '?')} / {v.get('altezza_max', 0):.2f} "
                     f"| {m.get('camera_pct_s', '?')} | {m.get('tremolio_pct_s', '?')} "
                     f"| {st.get('s', '?')}–{st.get('e', '?')} s | {d.get('parte') or ''} | {d.get('azione') or ''} "
                     f"| {d.get('inquadratura') or ''} | {d.get('difetti') or ''} | "
                     + (f"**ESCLUSA**: {'; '.join(c['esclusa'])}" if c['esclusa'] else f"{d.get('voto') or ''}") + " |")
    (LIBRERIA / 'indice.md').write_text('\n'.join(L) + '\n', encoding='utf-8')

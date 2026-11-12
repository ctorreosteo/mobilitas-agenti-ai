"""Radiografia generica dell'agente reel-grafiche (fase 6, 05/11/2026).

Si aggiunge alla radiografia di base (`reel_radiografia_base.radiografia`), che resta quella di prima per tagli,
finestre, sottotitoli e voce. Qui si misura quello che serve per un reel verticale qualsiasi:

- **persona fotogramma per fotogramma** (Apple Vision, `motore/swift/persona.swift`): volti, cima della testa,
  mani, sagoma; anche quando la persona si muove, e anche le persone dentro le finestre degli ads;
- **tipo di inquadratura**: finestre (schemi A, B, C degli ads), persona in camera, B-roll pieno. Le animazioni
  3D le segna sempre l'agente (`./mve reel-3d`);
- **sottotitoli impressi senza SRT**: Apple Vision legge il testo ogni 3 fotogrammi; una riga è un sottotitolo
  se le sue parole sono quelle della voce in quel momento (whisper). Con le righe lette si fa un SRT «letto»
  che prende il posto di quello mancante (si segnala: il copy vero resta da confermare);
- **scritte già presenti nel video**: le righe di testo lette che non sono sottotitoli, con il riquadro e i
  fotogrammi;
- **zone libere fotogramma per fotogramma**: una griglia di celle da 60 px (18 × 32) con cinque strati
  (persona, testa, mani, sottotitoli, scritte), in `radiografia/zone.npz`, più il riepilogo per inquadratura.

Il motore misura, l'agente guarda i fogli `radiografia/persona-*.jpg` (persona, testa, mani, sottotitoli,
scritte e celle libere disegnati sopra il fotogramma).
"""
import difflib
import json
import os
import re
import shutil
import statistics
import subprocess

import numpy as np

from . import reel_comune as C
from .reel_comune import W, H, SAFE

PERSONA_SWIFT = C.AGENTE / 'motore' / 'swift' / 'persona.swift'
CELLA = 60
GC, GR = W // CELLA, H // CELLA          # 18 colonne e 32 righe in verticale, 32 e 18 in orizzontale
STRATI = ('persona', 'testa', 'mani', 'sottotitoli', 'scritte')
PASSO_OCR = 3                            # Vision sul testo ogni 3 fotogrammi (0,1 s a 30 fps)


def persona_bin():
    h = C.md5_file(PERSONA_SWIFT)[:10]
    b = C.CACHE / f'reel-persona-{h}'
    if not b.exists():
        C.CACHE.mkdir(exist_ok=True)
        tmp = C.CACHE / f'reel-persona-{h}.{os.getpid()}'
        subprocess.run(['swiftc', '-O', '-suppress-warnings', str(PERSONA_SWIFT), '-o', str(tmp)], check=True,
                       capture_output=True, env=dict(os.environ, TMPDIR=os.environ.get('TMPDIR', str(C.CACHE))))
        os.replace(tmp, b)
    return b


# ---------------------------------------------------------------- persona

def _testa(volto, teste):
    """riquadro della testa (px a 1080x1920) da un volto: capelli sopra (0,7 volte l'altezza del volto), orecchie ai lati"""
    x, y, w, h = volto['x'] * W, volto['y'] * H, volto['w'] * W, volto['h'] * H
    return [x - 0.35 * w, y - 0.7 * h, x + 1.35 * w, y + 1.15 * h]


def _testa_da_posa(p):
    """senza volto (persona di spalle o di profilo): la testa stimata da naso, occhi, orecchie e collo"""
    pts = [v for k, v in p.items() if k in ('naso', 'occhio_sx', 'occhio_dx', 'orecchio_sx', 'orecchio_dx') and v[2] > 0.3]
    if len(pts) < 2:
        return None
    xs, ys = [v[0] * W for v in pts], [v[1] * H for v in pts]
    largo = max(max(xs) - min(xs), 60)
    collo = p.get('collo')
    giu = collo[1] * H if collo and collo[2] > 0.3 else max(ys) + largo * 0.8
    return [min(xs) - 0.5 * largo, min(ys) - 1.1 * largo, max(xs) + 0.5 * largo, giu]


def misura_persona(V, nf, L):
    """per ogni fotogramma: volti, teste, mani (px a 1080x1920), sagoma (copertura, riquadro) e la maschera a 270x480"""
    d = L / 'persona'
    if d.exists():
        shutil.rmtree(d)
    (d / 'f').mkdir(parents=True)
    pw, ph = C.mini(540)          # 540x960 in verticale, 960x540 in orizzontale
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(V), '-vf', f'scale={pw}:{ph}:flags=area', '-fps_mode', 'passthrough',
                    '-q:v', '3', '-start_number', '0', str(d / 'f' / 'f%05d.jpg')], check=True)
    subprocess.run([str(persona_bin()), str(d / 'f'), str(d / 'persona.json'), str(d / 'm')], check=True, capture_output=True,
                   env={'TMPDIR': os.environ.get('TMPDIR', str(L)), 'PATH': '/usr/bin:/bin'})
    shutil.rmtree(d / 'f')
    righe = {int(re.search(r'(\d+)', x['file']).group(1)): x for x in json.loads((d / 'persona.json').read_text())}
    out = []
    for f in range(nf):
        x = righe.get(f) or {'volti': [], 'mani': [], 'teste': [], 'sagoma': {'copertura': 0}}
        volti = [v for v in x['volti'] if v['conf'] > 0.5]
        teste = [_testa(v, x['teste']) for v in volti]
        if not volti:
            teste += [t for t in (_testa_da_posa(p) for p in x['teste']) if t]
        mani = [[b[0] * W - 15, b[1] * H - 15, b[2] * W + 15, b[3] * H + 15] for b in (m['box'] for m in x['mani'])]
        sg = x['sagoma']
        out.append({'volti': [[round(v['x'] * W), round(v['y'] * H), round((v['x'] + v['w']) * W), round((v['y'] + v['h']) * H)] for v in volti],
                    'teste': [[round(c) for c in t] for t in teste], 'mani': [[round(c) for c in m] for m in mani],
                    'copertura': round(sg.get('copertura', 0), 3),
                    'sagoma': [round(sg['box'][0] * W), round(sg['box'][1] * H), round(sg['box'][2] * W), round(sg['box'][3] * H)] if sg.get('box') else None,
                    'maschera': str(d / 'm' / sg['maschera']) if sg.get('maschera') else None})
    return out


# ---------------------------------------------------------------- testo nel video

def leggi_testo(V, nf, L, passo=PASSO_OCR):
    """Vision su un fotogramma ogni `passo`: {f: [righe]} (riquadri in px)"""
    oc = L / 'ocr'
    out = {}
    fr = list(range(0, nf, passo))
    for i in range(0, len(fr), 120):
        lotto = fr[i:i + 120]
        if oc.exists():
            shutil.rmtree(oc)
        oc.mkdir()
        sel = '+'.join(f'eq(n\\,{f})' for f in lotto) if len(lotto) < 3 else f"between(n\\,{lotto[0]}\\,{lotto[-1]})*not(mod(n-{lotto[0]}\\,{passo}))"
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(V), '-vf', f"select='{sel}',scale=in_color_matrix=bt709:in_range=tv:out_range=full",
                        '-fps_mode', 'passthrough', '-frame_pts', '1', str(oc / 'f%05d.png')], check=True)
        r = C.vision(oc, L / 'ocr.json')
        for nome, obs in r.items():
            f = int(re.search(r'(\d+)', nome).group(1))
            out[f] = [o for o in obs if o.get('conf', 1) >= 0.3 and len(C.parole_di(o['t'])) > 0]
    shutil.rmtree(oc, ignore_errors=True)
    return out


def _simile(a, b):
    return difflib.SequenceMatcher(a=' '.join(C.parole_di(a)), b=' '.join(C.parole_di(b))).ratio()


def tracce(testo, passo=PASSO_OCR):
    """righe lette raggruppate nel tempo: stesso testo (simile ≥ 0,8) e stesso punto (centro entro 50 px), con buchi
    fino a 2 letture -> [{t, box, f0, f1, n}]"""
    tr = []
    aperte = []
    for f in sorted(testo):
        for o in testo[f]:
            c = (o['x'] + o['w'] / 2, o['y'] + o['h'] / 2)
            m = None
            for q in aperte:
                if f - q['f1'] <= 3 * passo and abs(q['c'][0] - c[0]) < 50 and abs(q['c'][1] - c[1]) < 50 and _simile(q['t'], o['t']) >= 0.8:
                    m = q
                    break
            if m:
                m['f1'] = f; m['n'] += 1
                m['box'] = [min(m['box'][0], o['x']), min(m['box'][1], o['y']), max(m['box'][2], o['x'] + o['w']), max(m['box'][3], o['y'] + o['h'])]
                if len(o['t']) > len(m['t']):
                    m['t'] = o['t']
            else:
                q = {'t': o['t'], 'c': c, 'f0': f, 'f1': f, 'n': 1, 'box': [o['x'], o['y'], o['x'] + o['w'], o['y'] + o['h']], 'h': o['h']}
                tr.append(q); aperte.append(q)
        aperte = [q for q in aperte if f - q['f1'] <= 3 * passo]
    for q in tr:
        q['box'] = [round(v) for v in q['box']]
        q['f0'] = max(0, q['f0'] - passo // 2 - 1); q['f1'] = q['f1'] + passo // 2 + 1
        del q['c']
    return tr


def separa_sottotitoli(tr, parole_voce, fps, righe_srt=None):
    """una traccia è un sottotitolo se le sue parole sono dette dalla voce nello stesso momento (±1,5 s) o se è una
    riga dell'SRT; le altre sono scritte del video"""
    sott, scritte = [], []
    for q in tr:
        pw = C.parole_di(q['t'])
        if not pw:
            continue
        a, b = q['f0'] / fps - 1.5, (q['f1'] + 1) / fps + 1.5
        vicine = {C.norm(p['parola']) for p in parole_voce if a <= p['a'] <= b}
        quota = sum(1 for w in pw if w in vicine) / len(pw)
        srt = max((_simile(q['t'], r['t']) for r in (righe_srt or []) if r['a'] - 1 <= q['f0'] / fps <= r['b'] + 1), default=0)
        q['quota_voce'] = round(quota, 2)
        if (quota >= 0.6 and len(pw) >= 1 and q['n'] >= 2) or srt >= 0.8:
            sott.append(q)
        elif q['n'] >= 2:                          # una lettura sola è quasi sempre rumore (fumo, B-roll mosso)
            scritte.append(q)
    return sott, scritte


def srt_letto(sott, fps):
    """un SRT fatto dalle righe lette (quando l'SRT non c'è): una riga per traccia, in ordine di tempo"""
    out = []
    for i, q in enumerate(sorted(sott, key=lambda q: q['f0']), start=1):
        out.append({'n': i, 'a': round(q['f0'] / fps, 3), 'b': round((q['f1'] + 1) / fps, 3), 't': q['t']})
    return out


# ---------------------------------------------------------------- zone

def _celle(box, margine=0):
    x0, y0, x1, y1 = box
    c0, c1 = int(max(0, x0 - margine) // CELLA), int(min(W - 1, x1 + margine) // CELLA)
    r0, r1 = int(max(0, y0 - margine) // CELLA), int(min(H - 1, y1 + margine) // CELLA)
    return r0, r1, c0, c1


def zone(pers, righe_sott, scritte, nf):
    """griglia (nf, 32, 18) per strato: True = occupato"""
    from PIL import Image
    Z = {k: np.zeros((nf, GR, GC), bool) for k in STRATI}
    for f, p in enumerate(pers):
        if p['maschera'] and p['copertura'] > 0.002:
            m = np.asarray(Image.open(p['maschera']).convert('L').resize((GC * 10, GR * 10), Image.BILINEAR)) > 127
            Z['persona'][f] = m.reshape(GR, 10, GC, 10).mean((1, 3)) >= 0.25
        for t in p['teste']:
            r0, r1, c0, c1 = _celle(t, 10)
            Z['testa'][f, r0:r1 + 1, c0:c1 + 1] = True
        for m in p['mani']:
            r0, r1, c0, c1 = _celle(m)
            Z['mani'][f, r0:r1 + 1, c0:c1 + 1] = True
    for o in righe_sott:
        fm, bx = o.get('fotogrammi_misurati'), o.get('box_lettere')
        if not fm or not bx:
            continue
        r0, r1, c0, c1 = _celle(bx, 16)
        Z['sottotitoli'][max(0, fm[0] - 1):min(nf, fm[1] + 2), r0:r1 + 1, c0:c1 + 1] = True
    for q in scritte:
        r0, r1, c0, c1 = _celle(q['box'], 12)
        Z['scritte'][max(0, q['f0']):min(nf, q['f1'] + 1), r0:r1 + 1, c0:c1 + 1] = True
    return Z


def salva_zone(Z, out):
    np.savez_compressed(out, **{k: np.packbits(v, axis=-1) for k, v in Z.items()}, gc=GC, gr=GR, cella=CELLA)


def carica_zone(p):
    z = np.load(p)
    return {k: np.unpackbits(z[k], axis=-1)[..., :int(z['gc'])].astype(bool) for k in STRATI}


def _rett_libero(lib):
    """il rettangolo di celle libere più grande (istogramma per righe): (area, r0, c0, r1, c1)"""
    best = (0, 0, 0, -1, -1)
    hgt = [0] * lib.shape[1]
    for r in range(lib.shape[0]):
        for c in range(lib.shape[1]):
            hgt[c] = hgt[c] + 1 if lib[r, c] else 0
        st = []
        for c in range(lib.shape[1] + 1):
            h = hgt[c] if c < lib.shape[1] else 0
            s = c
            while st and st[-1][1] >= h:
                s, hh = st.pop()
                a = hh * (c - s)
                if a > best[0]:
                    best = (a, r - hh + 1, s, r, c - 1)
            st.append((s, h))
    return best


def sicura():
    """celle tutte dentro la zona sicura Meta per i testi"""
    s = np.zeros((GR, GC), bool)
    for r in range(GR):
        for c in range(GC):
            s[r, c] = c * CELLA >= SAFE[0] and (c + 1) * CELLA - 1 <= SAFE[2] and r * CELLA >= SAFE[1] and (r + 1) * CELLA - 1 <= SAFE[3]
    return s


def riepilogo_inquadrature(inq, pers, Z, fps):
    """tipo di inquadratura e zone libere per ognuna"""
    S = sicura()
    for s in inq:
        fs = range(s['f0'], s['f1'] + 1)
        n = len(fs)
        con_volto = [f for f in fs if any((v[3] - v[1]) >= 0.06 * max(W, H) for v in pers[f]["volti"])]
        piccoli = [f for f in fs if pers[f]['volti'] and f not in con_volto]
        cop = statistics.median(pers[f]['copertura'] for f in fs)
        if s.get('schema'):
            tipo = f"finestre {s['schema']}"
        elif len(con_volto) >= 0.5 * n or (cop >= 0.12 and len(con_volto) + len(piccoli) >= 0.5 * n):
            tipo = 'persona in camera'
        else:
            tipo = 'B-roll pieno'
        cx = [((t[0] + t[2]) / 2, (t[1] + t[3]) / 2) for f in fs for t in pers[f]['teste'][:1]]
        mov = round(float(np.hypot(np.std([c[0] for c in cx]), np.std([c[1] for c in cx]))), 1) if len(cx) >= 3 else None
        occ = np.zeros((n, GR, GC), bool)
        for k in ('testa', 'mani', 'sottotitoli', 'scritte'):
            occ |= Z[k][s['f0']:s['f1'] + 1]
        quota = 1 - occ.mean(0)
        lib = (quota >= 0.95) & S
        a, r0, c0, r1, c1 = _rett_libero(lib)
        s['tipo'] = tipo
        s['persona'] = {'fotogrammi_con_volto_grande': len(con_volto), 'fotogrammi_con_volti_piccoli': len(piccoli),
                        'copertura_sagoma_mediana': round(cop, 3), 'movimento_testa_px': mov,
                        'teste_max': max((len(pers[f]['teste']) for f in fs), default=0)}
        s['zone_libere'] = {'celle_libere_zona_sicura': int(lib.sum()), 'celle_zona_sicura': int(S.sum()),
                            'rettangolo_libero_max': [c0 * CELLA, r0 * CELLA, (c1 + 1) * CELLA - 1, (r1 + 1) * CELLA - 1] if a else None}
    return inq


def tipo_reel(inq):
    fr = lambda t: sum(s['f1'] - s['f0'] + 1 for s in inq if s['tipo'].startswith(t))
    tot = sum(s['f1'] - s['f0'] + 1 for s in inq)
    q = {'finestre': fr('finestre') / tot, 'persona': fr('persona') / tot, 'broll': fr('B-roll') / tot}
    if q['finestre'] >= 0.6:
        t = 'ad con schema fisso'
    elif q['persona'] >= 0.4:
        t = 'ad o reel con frontman'
    elif q['broll'] >= 0.6:
        t = 'reel solo B-roll'
    else:
        t = 'misto'
    return {'proposto': t, 'quote': {k: round(v, 2) for k, v in q.items()},
            'nota': "proposta del motore dalle inquadrature; MOFU (più spiegazione) lo decide l'agente dal copy, in piano.json «tipo_reel»"}


# ---------------------------------------------------------------- fogli

def fogli(V, inq, pers, Z, sott_righe, scritte, fps, out):
    """per ogni inquadratura il fotogramma a metà con persona (rosso), teste (magenta), mani (arancio), sottotitoli
    (giallo), scritte (azzurro) e le celle libere nella zona sicura (verde)"""
    from PIL import Image, ImageDraw, ImageFont
    fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 44)
    for p in out.glob('persona-*.jpg'):
        p.unlink()
    S = sicura()
    mezzi = [(s['f0'] + s['f1']) // 2 for s in inq]
    im = C.estrai(V, mezzi)
    tiles = []
    for s, f in zip(inq, mezzi):
        x = im[f].convert('RGBA')
        ov = Image.new('RGBA', x.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        occ = Z['testa'][f] | Z['mani'][f] | Z['sottotitoli'][f] | Z['scritte'][f]
        for r in range(GR):
            for c in range(GC):
                if S[r, c] and not occ[r, c]:
                    d.rectangle([c * CELLA + 3, r * CELLA + 3, (c + 1) * CELLA - 4, (r + 1) * CELLA - 4], outline=(60, 230, 90, 150), width=2)
                if Z['persona'][f][r, c]:
                    d.rectangle([c * CELLA, r * CELLA, (c + 1) * CELLA - 1, (r + 1) * CELLA - 1], fill=(255, 40, 40, 55))
        for t in pers[f]['teste']:
            d.rectangle(t, outline=(255, 0, 255, 255), width=6)
        for m in pers[f]['mani']:
            d.rectangle(m, outline=(255, 150, 0, 255), width=5)
        for o in sott_righe:
            fm, bx = o.get('fotogrammi_misurati'), o.get('box_lettere')
            if fm and bx and fm[0] <= f <= fm[1]:
                d.rectangle(bx, outline=(255, 230, 0, 255), width=5)
        for q in scritte:
            if q['f0'] <= f <= q['f1']:
                d.rectangle(q['box'], outline=(0, 200, 255, 255), width=5)
        d.rectangle([0, 0, W - 1, 64], fill=(255, 230, 0, 255))
        d.text((12, 6), f"inq {s['n']} · {s['tipo']} · f{f}", font=fnt, fill=(0, 0, 0, 255))
        tiles.append(Image.alpha_composite(x, ov).convert('RGB').resize(C.mini(360), Image.LANCZOS))
    tw, th = C.mini(360)
    for g in range(0, len(tiles), 10):
        blocco = tiles[g:g + 10]
        sh = Image.new('RGB', (5 * (tw + 6), ((len(blocco) + 4) // 5) * (th + 6)), 'white')
        for i, t in enumerate(blocco):
            sh.paste(t, ((i % 5) * (tw + 6), (i // 5) * (th + 6)))
        sh.save(out / f"persona-{inq[g]['n']:02d}-{inq[g + len(blocco) - 1]['n']:02d}.jpg", quality=85)


# ---------------------------------------------------------------- la tappa

def estendi(R, V, L, D, testo=None):
    """aggiunge alla radiografia R (già con tagli, inquadrature, sottotitoli, voce) persona, tipi, scritte, zone"""
    fps, nf = R['fps'], R['fotogrammi']
    print("  persona fotogramma per fotogramma (Apple Vision)...", flush=True)
    pers = misura_persona(V, nf, L)
    if testo is None:
        print("  testo nel video (Apple Vision ogni 3 fotogrammi)...", flush=True)
        testo = leggi_testo(V, nf, L)
    tr = tracce(testo)
    sott_tr, scritte = separa_sottotitoli(tr, R['voce']['parole'], fps, R.get('srt'))
    # con l'SRT i sottotitoli sono quelli misurati dalla radiografia degli ads; le tracce che somigliano a una riga
    # dell'SRT non sono scritte
    righe = R['sottotitoli']['righe']
    Z = zone(pers, righe, scritte, nf)
    salva_zone(Z, D / 'radiografia' / 'zone.npz')
    riepilogo_inquadrature(R['inquadrature'], pers, Z, fps)
    C.scrivi(D / 'radiografia' / 'persona.json', [{k: v for k, v in p.items() if k != 'maschera'} for p in pers])
    R['persona'] = {'file': C.rel(D / 'radiografia' / 'persona.json'), 'come': "Apple Vision (motore/swift/persona.swift) su ogni fotogramma a 540x960 (960x540 in orizzontale)",
                    'fotogrammi_con_volto': sum(1 for p in pers if p['volti']), 'fotogrammi_con_mani': sum(1 for p in pers if p['mani'])}
    R['scritte_video'] = [{k: q[k] for k in ('t', 'box', 'f0', 'f1', 'n')} for q in scritte]
    R['zone_libere'] = {'file': C.rel(D / 'radiografia' / 'zone.npz'), 'cella_px': CELLA, 'griglia': [GC, GR], 'strati': list(STRATI),
                        'come': "per fotogramma, celle occupate da persona (sagoma ≥ 25%), testa (volto allargato, capelli), mani, "
                                "sottotitoli (+16 px), scritte del video (+12 px)"}
    R['tipo_reel'] = tipo_reel(R['inquadrature'])
    fogli(V, R['inquadrature'], pers, Z, righe, scritte, fps, D / 'radiografia')
    return R


def md(R):
    """righe da aggiungere a radiografia.md"""
    if 'tipo_reel' not in R:
        return []
    fps = R['fps']
    L = ['', '## Reel: tipo, persona, scritte, zone libere (radiografia generica, fase 6)', '',
         f"- **Tipo proposto dal motore:** {R['tipo_reel']['proposto']} (quote {R['tipo_reel']['quote']}). {R['tipo_reel']['nota']}.",
         f"- **Copy:** {R.get('fonte_copy', 'SRT')}.",
         f"- **Persona** ({R['persona']['come']}): volto in {R['persona']['fotogrammi_con_volto']} fotogrammi, mani in "
         f"{R['persona']['fotogrammi_con_mani']}; dati per fotogramma in `{R['persona']['file']}`.",
         f"- **Scritte già nel video** (non sottotitoli): {len(R['scritte_video'])}.",
         f"- **Zone libere:** `{R['zone_libere']['file']}` ({R['zone_libere']['come']}).", '',
         '| # | tipo | volto grande (fotogrammi) | sagoma (mediana) | movimento testa (px) | celle libere nella zona sicura | rettangolo libero più grande |',
         '|---|---|---|---|---|---|---|']
    for s in R['inquadrature']:
        p, z = s['persona'], s['zone_libere']
        L.append(f"| {s['n']} | {s['tipo']} | {p['fotogrammi_con_volto_grande']}/{s['f1'] - s['f0'] + 1} | {p['copertura_sagoma_mediana']} | "
                 f"{p['movimento_testa_px'] if p['movimento_testa_px'] is not None else '—'} | {z['celle_libere_zona_sicura']}/{z['celle_zona_sicura']} | "
                 f"{z['rettangolo_libero_max'] or '—'} |")
    if R['scritte_video']:
        L += ['', '**Scritte già nel video:**', '']
        L += [f"- «{q['t']}» f{q['f0']}–{q['f1']} ({q['f0'] / fps:.2f}–{(q['f1'] + 1) / fps:.2f} s), riquadro {q['box']}" for q in R['scritte_video'][:60]]
    L += ['', '- `radiografia/persona-*.jpg`: per ogni inquadratura, persona (rosso), teste (magenta), mani (arancio), sottotitoli (giallo), '
          'scritte (azzurro), celle libere nella zona sicura (verde): **da guardare**.']
    return L

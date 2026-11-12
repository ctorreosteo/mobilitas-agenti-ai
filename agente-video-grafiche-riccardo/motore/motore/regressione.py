"""Regressione dei modelli del catalogo (fase 7c, Riccardo 01/11/2026).

In `campionario/regressione/casi/` c'e un caso per ogni modello attivo di
`motore/inserti/CATALOGO-MODELLI.json`: la spec congelata (copiata dalla regia di un
video, dal campionario v2 o v3) e lo slug del montato su cui si costruisce.

    ./mve regressione tutti [--solo id1,id2] [--riferimento] [--accetta id1,id2]

Per ogni caso il motore ricostruisce la scena con i pezzi condivisi di adesso
(`_scena.js`, `_scena.html`, `scena.py`, `brand.json`), salva i fotogrammi chiave in
`campionario/regressione/ultimo/<id>.jpg` e li confronta con
`campionario/regressione/riferimento/<id>.jpg`:
- ROTTO: la costruzione fallisce o un controllo del motore non passa -> si corregge subito;
- CAMBIATO: i controlli passano ma i fotogrammi sono diversi dal riferimento -> si guarda
  il foglio e, se il cambio e voluto, si rifà il riferimento con `--riferimento`;
- OK: uguale al riferimento.
Esito in `campionario/regressione/REGRESSIONE.md` e `esito.json`. Si rifà dopo ogni
modifica ai pezzi condivisi. I video restano in `.lavoro/regressione/` (si svuota).
"""
import json
import sys
import time
import traceback

import numpy as np
from PIL import Image, ImageDraw

from .progetto import AGENTE, Progetto
from . import scena as S

R = AGENTE / 'campionario' / 'regressione'
CASI = R / 'casi'
LAV = AGENTE / '.lavoro' / 'regressione'
TW, TH = 480, 270
SOGLIA = 6.0          # differenza media (0-255) oltre la quale un fotogramma e "cambiato"
SPECIALI = ('chip', 'schermata-finale-youtube', 'b-roll')


def _tempi(spr, durata):
    el = [x for x in spr['elementi'] if x.get('modello') != 'etichetta']
    fin = [p for p in spr.get('piatto', []) if p['tipo'] == 'finestra']
    t = []
    if el:
        a = el[0]
        t += [a['s'] + min(0.5, (a['e'] - a['s']) * 0.25), (a['s'] + a['e']) / 2, a['e'] - 0.35]
        t += [(x['s'] + x['e']) / 2 for x in el[1:3]]
    for p in fin[:1]:
        t.append((p['s'] + p['e']) / 2)
    if not t:
        t = [durata * k / 5 for k in range(1, 5)]
    t = sorted({round(min(max(v, 0.1), durata - 0.1), 2) for v in t})
    return t[:5]


def _foglio(img_t, titolo, out):
    w = len(img_t) * (TW + 6) + 6
    im = Image.new('RGB', (w, TH + 64), (0, 26, 61))
    d = ImageDraw.Draw(im)
    from .tavole import _f
    d.text((8, 8), titolo, font=_f(22, 700), fill=(244, 244, 244))
    for k, (t, fr) in enumerate(img_t):
        im.paste(fr.resize((TW, TH)), (6 + k * (TW + 6), 40))
        d.text((10 + k * (TW + 6), 44), f"{t:.2f} s", font=_f(18, 700), fill=(114, 250, 147))
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=88)
    return im


def _confronta(id_):
    a, b = R / 'riferimento' / f"{id_}.jpg", R / 'ultimo' / f"{id_}.jpg"
    if not a.exists():
        return None
    A, B = np.asarray(Image.open(a), np.float32), np.asarray(Image.open(b), np.float32)
    if A.shape != B.shape:
        return [999.0]
    n = (A.shape[1] - 6) // (TW + 6)
    return [round(float(np.abs(A[40:40 + TH, 6 + k * (TW + 6):6 + k * (TW + 6) + TW]
                               - B[40:40 + TH, 6 + k * (TW + 6):6 + k * (TW + 6) + TW]).mean()), 2) for k in range(n)]


def _caso(c):
    P = Progetto(c['slug'])
    anc = S.Ancore(P)
    spec = json.loads(json.dumps(c['spec']))
    spec.update({'n': 0, 'nome': c['id'], 'cartella': f"regressione/{c['id']}"})
    spec['pezzi'] = [[round(round((anc(v) if isinstance(v, dict) else v) * P.fps) / P.fps, 4) for v in pz]
                     for pz in spec['pezzi']]
    out = LAV / f"{c['id']}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    anc.usate.clear()
    rap, tempo, cam, volto, spr = S.costruisci(P, spec, out, anc)
    tempi = _tempi(spr, tempo.durata)
    from .tavole import fotogramma
    return out, [(t, fotogramma(out, t)) for t in tempi], rap['controlli'], rap['tempi_s']['totale']


def _speciale(id_):
    """i modelli che non passano da `costruisci`: chip (Pillow), schermata finale, B-roll"""
    from .tavole import fotogramma
    P = Progetto('YT_POSTURA_32')
    G = P.leggi('grafica.json')
    video = P.p('consegna') / 'YT_POSTURA_32.mp4'
    if id_ == 'chip':
        from .grafica import render as GR
        t = G['chip']['s'] + 1.0
        fr = fotogramma(video, t).convert('RGBA')
        sp = GR.chip_v3_sprite(G['chip'])
        from . import stile as ST
        fr.alpha_composite(sp, (ST.SAFE, 760))
        return None, [(t, fr.convert('RGB'))], [{'cosa': 'chip v3 disegnato (pittogramma su disco panna)', 'valore': f"{sp.width}x{sp.height}", 'ok': sp.width > 0}], 0.0
    if id_ == 'schermata-finale-youtube':
        from . import video_scena as VS
        LAV.mkdir(parents=True, exist_ok=True)
        out = LAV / 'schermata-finale.mp4'
        t0 = time.time()
        _, n, rap = VS.schermata_finale(P, {'durata': 4.0}, video, 'regressione', out=out,
                                        png=R / 'controlli' / 'schermata-finale.jpg')
        return out, [(t, fotogramma(out, t)) for t in (0.2, 1.2, 3.0)], rap['controlli'], round(time.time() - t0, 1)
    if id_ == 'b-roll':
        b = G['broll'][0]
        t = (b['s'] + b['e']) / 2
        return None, [(t, fotogramma(video, t))], [{'cosa': 'B-roll dal montato (non usa i pezzi condivisi)', 'valore': 'fotogramma', 'ok': True}], 0.0
    raise KeyError(id_)


def accetta(ids):
    """i casi CAMBIATI gia guardati: i fotogrammi di adesso diventano il riferimento (senza ricostruire)"""
    import shutil
    esito_p = R / 'esito.json'
    esito = json.loads(esito_p.read_text())
    for id_ in ids:
        if esito.get(id_, {}).get('stato') != 'CAMBIATO':
            print(f"  {id_}: non e CAMBIATO ({esito.get(id_, {}).get('stato')}), salto")
            continue
        shutil.copy2(R / 'ultimo' / f"{id_}.jpg", R / 'riferimento' / f"{id_}.jpg")
        esito[id_].update({'stato': 'OK', 'accettato': time.strftime('%Y-%m-%d %H:%M'), 'differenza_accettata': esito[id_].get('differenza')})
        print(f"  {id_}: riferimento aggiornato")
    esito_p.write_text(json.dumps(esito, ensure_ascii=False, indent=1))
    from . import catalogo as CAT
    attivi = [m['id'] for m in CAT.carica()['modelli'] if m['stato'] == 'attivo']
    casi = [json.loads(q.read_text()) for q in sorted(CASI.glob('*.json'))]
    coperti = {m for c in casi for m in c['modelli']} | set(SPECIALI)
    _md(esito, [a for a in attivi if a not in coperti])


def regressione(slug='tutti', solo=None, riferimento=None, accetta_=None):
    if accetta_:
        return accetta([s.strip() for s in accetta_.split(',')])
    (R / 'controlli').mkdir(parents=True, exist_ok=True)
    casi = [json.loads(p.read_text()) for p in sorted(CASI.glob('*.json'))]
    ids = [c['id'] for c in casi] + list(SPECIALI)
    sel = {s.strip() for s in solo.split(',')} if solo else None
    esito_p = R / 'esito.json'
    esito = json.loads(esito_p.read_text()) if esito_p.exists() else {}
    from . import catalogo as CAT
    attivi = [m['id'] for m in CAT.carica()['modelli'] if m['stato'] == 'attivo']
    coperti = {m for c in casi for m in c['modelli']} | set(SPECIALI)
    mancano = [a for a in attivi if a not in coperti]
    for id_ in ids:
        if sel and id_ not in sel:
            continue
        c = next((c for c in casi if c['id'] == id_), None)
        print(f"{id_}...", flush=True)
        try:
            out, frames, controlli, sec = _caso(c) if c else _speciale(id_)
            dest = R / ('riferimento' if riferimento else 'ultimo') / f"{id_}.jpg"
            _foglio(frames, f"{id_}  ·  {', '.join(c['modelli']) if c else id_}", dest)
            if riferimento:
                _foglio(frames, f"{id_}  ·  {', '.join(c['modelli']) if c else id_}", R / 'ultimo' / f"{id_}.jpg")
            no = [x for x in controlli if not x['ok']]
            diff = _confronta(id_)
            stato = 'ROTTO' if no else ('CAMBIATO' if diff and max(diff) > SOGLIA else 'OK')
            esito[id_] = {'stato': stato, 'modelli': c['modelli'] if c else [id_], 'controlli': f"{len(controlli) - len(no)}/{len(controlli)}",
                          'non_passano': [f"{x['cosa']}: {x['valore']}" for x in no], 'differenza': diff,
                          'secondi': sec, 'quando': time.strftime('%Y-%m-%d %H:%M'), 'nota': c.get('nota', '') if c else ''}
        except SystemExit as e:
            esito[id_] = {'stato': 'ROTTO', 'errore': str(e), 'quando': time.strftime('%Y-%m-%d %H:%M')}
        except Exception:
            esito[id_] = {'stato': 'ROTTO', 'errore': traceback.format_exc()[-600:], 'quando': time.strftime('%Y-%m-%d %H:%M')}
        print(f"   {esito[id_]['stato']} {esito[id_].get('controlli', '')} {esito[id_].get('non_passano', '') or esito[id_].get('errore', '')}", flush=True)
        esito_p.write_text(json.dumps(esito, ensure_ascii=False, indent=1))
    from .inserti import dimentica
    dimentica()
    _md(esito, mancano)
    rotti = [k for k, v in esito.items() if v['stato'] == 'ROTTO']
    if rotti:
        sys.exit(f"regressione: ROTTI {', '.join(rotti)}")


def _md(esito, mancano):
    righe = ["# Regressione dei modelli\n",
             "Generato da `./mve regressione tutti`. Un caso per ogni modello attivo del catalogo; "
             "fotogrammi chiave in `ultimo/` (adesso) e `riferimento/` (approvati).\n",
             "| caso | modelli | stato | controlli | differenza dal riferimento | quando |", "|---|---|---|---|---|---|"]
    for k, v in sorted(esito.items()):
        d = v.get('differenza')
        righe.append(f"| {k} | {', '.join(v.get('modelli', []))} | **{v['stato']}** | {v.get('controlli', '—')} | "
                     f"{'—' if not d else ' / '.join(f'{x:.1f}' for x in d)} | {v.get('quando', '')} |")
    pr = [(k, v) for k, v in sorted(esito.items()) if v.get('non_passano') or v.get('errore')]
    if pr:
        righe += ["", "## Da correggere", ""]
        for k, v in pr:
            righe.append(f"- **{k}**: " + ('; '.join(v.get('non_passano', [])) or v.get('errore', '').strip().splitlines()[-1]))
    if mancano:
        righe += ["", f"**Modelli attivi senza caso:** {', '.join(mancano)}"]
    (R / 'REGRESSIONE.md').write_text('\n'.join(righe) + '\n', encoding='utf-8')

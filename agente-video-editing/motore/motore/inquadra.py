"""Fase `inquadra`: quale taglio di camera ha ogni pezzo del montato.

La sorgente e 4K e si consegna in 1080p: c'e margine per ingrandire fino a 2x
senza scendere sotto i pixel nativi. Da una camera fissa escono cosi tre tagli
(largo, medio, stretto) centrati sul volto tracciato da Vision, ed e come avere
tre camere.

La grammatica:

- **a ogni giunta il taglio cambia.** Lo stacco secco con cambio di inquadratura
  non si vede; la dissolvenza della v1 si vedeva come "salto morbido";
- **largo quando serve spazio**: card, apertura, chip identita hanno bisogno
  della fascia libera accanto al soggetto;
- **largo sui titoli dietro**: piu piccola e la persona, meno lettere nasconde
  (al medio la parola peggiore perdeva un terzo delle lettere);
- **stretto sulle frasi chiave** scelte in regia (`enfasi`);
- fuori da questi casi si alterna largo e medio, cambiando su una pausa fra due
  frasi circa ogni 9 s; nessun pezzo sotto 1 s.

Le card prendono il lato lontano dal volto, misurato nel taglio in cui cadono:
il difetto "card sul viso" sparisce per costruzione.
"""
import re
import sys

from .progetto import Progetto, FPS, ts
from . import stile as S
from .visione import Traccia

VARIANTI = {'largo': 'largo_b', 'medio': 'medio_b', 'stretto': 'stretto_b'}
Z = dict(S.FRAMING, largo_b=1.12, medio_b=1.42, stretto_b=1.80)
FACE_Y = dict(S.FACE_Y, largo_b=None, medio_b=0.35, stretto_b=0.40)
PRIO = {'largo': 3, 'medio': 2, 'stretto': 1}
PEZZO_MAX = 13.0
PEZZO_TIPICO = 9.0
PEZZO_MIN = 1.0


def candidati(W):
    """punti buoni per cambiare taglio dentro una ripresa: poco prima che riparta
    il parlato, dopo una pausa fra due frasi"""
    out = []
    for a, b in zip(W, W[1:]):
        gap = b['s'] - a['e']
        if gap >= 0.35 or (gap >= 0.20 and re.search(r'[.!?;:,]$', a['t'])):
            out.append(round(max(a['e'] + 0.04, b['s'] - 0.12), 3))
    return out


def _crop(face, fr, W, H, zmax):
    z = min(Z[fr], zmax)
    if z <= 1.001 or face is None:
        return [0, 0, W, H], 1.0
    cw = int(round(W / z / 2)) * 2
    ch = int(round(H / z / 2)) * 2
    fx, fy, fw, fh = face
    cx = fx + fw / 2
    cy = fy + fh / 2
    x0 = cx - cw / 2
    fyr = FACE_Y.get(fr)
    y0 = cy - (fyr * ch if fyr else (cy / H) * ch)
    x0 = int(round(min(max(0, x0), W - cw) / 2)) * 2
    y0 = int(round(min(max(0, y0), H - ch) / 2)) * 2
    return [x0, y0, cw, ch], round(W / cw, 3)


def inquadra(slug):
    P = Progetto(slug)
    E = P.leggi('edl.json')
    G = P.leggi('grafica.json')
    W = P.leggi('parole-montato.json')
    W = [{'s': w[0], 'e': w[1], 't': w[2]} for w in W]
    m = P.meta()
    SW_, SH_ = m['larghezza'], m['altezza']
    zmax = max(1.0, SH_ / 1080) * (1.0 if SH_ >= 2160 else 1.12)
    tr = Traccia(P)
    segs = E['segmenti']
    dur = E['durata']
    J = [s['edit_in'] for s in segs[1:]]
    C = candidati(W)

    forz = []   # (s, e, framing)
    if G.get('opening'):
        forz.append((0.0, G['opening']['e'] + 0.3, 'largo'))
    if G.get('chip'):
        forz.append((G['chip']['s'] - 0.2, G['chip']['e'] + 0.3, 'largo'))
    for c in G['cards']:
        forz.append((c['s'] - 0.1, c['e'] + 0.1, 'largo'))
    for c in G['capitoli']:
        if c['dietro']:
            forz.append((c['s'] - 0.05, c['e'] + 0.05, 'largo'))
    for c in G['enfasi']:
        forz.append((c['s'], c['e'], c['livello']))

    def snap(t, verso):
        pool = [x for x in C + J if (x <= t + 0.05 if verso < 0 else x >= t - 0.05) and abs(x - t) <= 0.8]
        return min(pool, key=lambda x: abs(x - t)) if pool else t

    B = set(J)
    for s, e, fr in forz:
        if fr == 'stretto':
            B.update([s, e])          # gia su un confine di parola
        else:
            B.update([snap(s, -1), snap(e, +1)])
    B = sorted(b for b in B if 0.5 < b < dur - 0.5)

    # spezza i pezzi troppo lunghi sulle pause fra le frasi
    pts = [0.0] + B + [dur]
    extra = []
    for a, b in zip(pts, pts[1:]):
        t = a
        while b - t > PEZZO_MAX:
            target = t + PEZZO_TIPICO
            cand = [x for x in C if t + 5.0 < x < b - 4.0]
            if not cand:
                break
            x = min(cand, key=lambda x: abs(x - target))
            extra.append(x)
            t = x
    B = sorted(set(B + extra))

    # frame interi, e niente pezzi minuscoli (le giunte restano)
    Jf = {int(round(j * FPS)) for j in J}
    bf = sorted({int(round(b * FPS)) for b in B} | Jf)
    total = E['frame']
    pulito = []
    for f in bf:
        prev = pulito[-1] if pulito else 0
        if f - prev < PEZZO_MIN * FPS and f not in Jf:
            continue
        if f - prev < PEZZO_MIN * FPS and pulito and pulito[-1] not in Jf:
            pulito.pop()
        pulito.append(f)
    bf = [f for f in pulito if 0 < f < total]
    edges = [0] + bf + [total]

    def forzato(a, b):
        best = None
        for s, e, fr in forz:
            ov = min(b, e) - max(a, s)
            if ov > 0.5 * (b - a) or (s >= a and e <= b):
                if best is None or PRIO[fr] > PRIO[best]:
                    best = fr
        return best

    pezzi = []
    prev, giro = None, 0
    for k, (f0, f1) in enumerate(zip(edges, edges[1:])):
        a, b = f0 / FPS, f1 / FPS
        fr = forzato(a, b)
        if fr is None:
            if prev in ('largo', 'largo_b'):
                fr = 'medio'
            elif prev in ('medio', 'medio_b'):
                fr = 'largo'
            else:
                giro += 1
                fr = 'medio' if giro % 2 else 'largo'
        base = lambda x: x.replace('_b', '') if x else x
        if prev and base(fr) == base(prev):
            fr = prev.replace('_b', '') if prev.endswith('_b') else VARIANTI[base(fr)]
        pezzi.append({'f0': f0, 'n': f1 - f0, 'framing': fr})
        prev = fr

    # sorgente e ritaglio di ogni pezzo
    seg_f0 = [int(round(s['edit_in'] * FPS)) for s in segs]
    for p in pezzi:
        k = max(i for i, f in enumerate(seg_f0) if f <= p['f0'])
        sg = segs[k]
        p['seg'] = k
        p['edit_in'] = round(p['f0'] / FPS, 6)
        p['src_in'] = round(sg['in'] + (p['f0'] - seg_f0[k]) / FPS, 6)
        if p['f0'] + p['n'] > seg_f0[k] + sg['n']:
            sys.exit(f"pezzo a cavallo di una giunta: {p}")
        face = tr.mediana(p['src_in'], p['src_in'] + p['n'] / FPS)
        p['crop'], p['z'] = _crop(face, p['framing'], SW_, SH_, zmax)

    _lati(G, pezzi, tr, SW_, SH_)
    P.scrivi('grafica.json', G)
    P.scrivi('inquadratura.json', {'sorgente': [SW_, SH_], 'pezzi': pezzi})

    from collections import Counter
    cnt = Counter(p['framing'].replace('_b', '') for p in pezzi)
    lens = [p['n'] / FPS for p in pezzi]
    print(f"{len(pezzi)} pezzi (durata media {sum(lens)/len(lens):.1f}s, min {min(lens):.1f}s, "
          f"max {max(lens):.1f}s): " + ', '.join(f"{k} {v}" for k, v in cnt.most_common()))
    print(f"  {len(J)} giunte, tutte con cambio di taglio; {len(extra)} cambi dentro le riprese lunghe")
    print("-> data/inquadratura.json, lati delle card in data/grafica.json")


def _faccia_out(tr, p, a, b, SW_, SH_):
    """riquadro del volto nell'immagine d'uscita 1920x1080 durante [a, b] (tempo montato)"""
    sa = p['src_in'] + (a - p['edit_in'])
    sb = p['src_in'] + (b - p['edit_in'])
    f = tr.inviluppo(sa, sb)
    med = tr.mediana(sa, sb)
    if f is None or med is None:
        return None
    x0, y0, cw, ch = p['crop']
    k = S.W / cw
    # testa intera, non solo il volto: il riquadro di Vision prende la faccia;
    # i capelli aggiungono circa un terzo della larghezza ai lati e mezza altezza
    # sopra. Il margine si misura sul volto mediano, non sull'unione dei campioni
    # (che e larga perche lei si muove)
    fx, fy, fw, fh = f
    mw, mh = med[2], med[3]
    hx0, hy0 = fx - mw * 0.30, fy - mh * 0.55
    hx1, hy1 = fx + fw + mw * 0.30, fy + fh + mh * 0.25
    return ((hx0 - x0) * k, (hy0 - y0) * k, (hx1 - x0) * k, (hy1 - y0) * k)


def _lati(G, pezzi, tr, SW_, SH_):
    """per ogni elemento in alto: il lato libero, misurato sul volto nel suo taglio"""
    # le misure vengono dal renderer: la card con la scala e piu alta di un tempo
    from .grafica.render import Lockup
    from .grafica.info import misura
    items = [('card', c) + misura(c) for c in G['cards']]
    if G.get('opening'):
        lk = Lockup(G['opening'])
        items.append(('apertura', G['opening'], lk.width, lk.height))
    if G.get('chip'):
        lk = Lockup(G['chip'], chip=True)
        items.append(('chip', G['chip'], lk.width, lk.height))
    for c in G['cards']:
        c.pop('side', None)
    for kind, c, w, card_h in items:
        heads = []
        for p in pezzi:
            a, b = max(c['s'], p['edit_in']), min(c['e'], p['edit_in'] + p['n'] / FPS)
            if b > a:
                h = _faccia_out(tr, p, a, b, SW_, SH_)
                if h:
                    heads.append(h)
        top, bot = S.CARD_TOP, S.CARD_TOP + card_h
        boxes = {'left': (S.SAFE, S.SAFE + w), 'right': (S.W - S.SAFE - w, S.W - S.SAFE)}
        dist = {}
        for side, (x0, x1) in boxes.items():
            d = 1e9
            for hx0, hy0, hx1, hy1 in heads:
                if hy1 < top or hy0 > bot:
                    continue
                d = min(d, hx0 - x1 if side == 'left' else x0 - hx1)
            dist[side] = d
        side = 'left' if dist['left'] >= dist['right'] - 40 else 'right'
        # due card a schermo insieme vanno su lati opposti; `lato` in regia decide da solo
        accanto = [o for o in G['cards'] if o is not c and o.get('side') and o['s'] < c['e'] and c['s'] < o['e']]
        if accanto and kind == 'card':
            occupato = {o['side'] for o in accanto}
            if side in occupato and len(occupato) == 1:
                side = 'right' if side == 'left' else 'left'
        if c.get('lato'):
            side = {'sinistra': 'left', 'destra': 'right'}.get(c['lato'], c['lato'])
        c['side'] = side
        c['margine_volto'] = round(dist[side], 1) if dist[side] < 1e8 else None
        if dist[side] < 0:
            c['conflitto'] = True
            print(f"  !!! {kind} a {ts(c['s'])}: si sovrappone alla testa da entrambi i lati")
        else:
            c.pop('conflitto', None)

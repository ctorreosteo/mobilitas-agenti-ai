"""Impaginazione misurata (fase 6b, 27/10/2026): dove e quanto grande, deciso sui
pixel veri invece che a occhio.

- `piazza_numero`: il numero dietro la persona. Si cerca, sulle sagome di Vision
  di tutta la durata, la posizione e il corpo piu grandi per cui la persona copre
  al massimo il 12% del numero e mai il primo carattere (stesso principio dei
  titoli dietro: conta la cifra peggiore, non la media). "più di" e l'etichetta
  stanno legati al numero e anche loro fuori dalla persona.
- `misura_card`: testo delle card misurato con il font vero (Montserrat, pesi
  veri): il corpo del titolo e quello per cui la parola piu lunga sta dentro i
  margini fissi, mai sotto 60 px; altezza della card calcolata, testo centrato.
- `Mani`, `lega_mani`: le mani di Vision sui frame del piatto (coordinate
  d'uscita): la card parte dalla mano vera e il controllo verifica che non la copra.

Le misure del browser e quelle di PIL coincidono perche la pagina usa le stesse
regole: line-height 1, cifre in celle di larghezza fissa, posizioni assolute.
"""
import json
import math
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .progetto import RISORSE

FONT = RISORSE / 'fonts' / 'Montserrat-VF.ttf'
W, H = 1920, 1080
SAFE_X, SAFE_Y = 96, 54
# Montserrat: ascender 968, descender 251 (unita/1000). Con line-height: 1 la linea
# di base sta a (1 - 1.219)/2 + 0.968 = 0.8585 em dal bordo alto del box.
BASE = 0.8585
CELLA = 0.66                 # larghezza della cella di ogni cifra (em)

_F = {}


def font(peso, corpo):
    k = (peso, int(round(corpo)))
    if k not in _F:
        f = ImageFont.truetype(str(FONT), k[1])
        f.set_variation_by_axes([peso])
        _F[k] = f
    return _F[k]


def larghezza(testo, peso, corpo, track=0.0):
    """larghezza in px come la disegna il browser (letter-spacing in em)"""
    return font(peso, corpo).getlength(testo) + track * corpo * len(testo)


# ------------------------------------------------------------------ numero dietro
def _maschera_numero(testo, corpo, peso=800):
    """alfa delle cifre (celle fisse, glifo centrato) con l'angolo alto-sinistro
    del box di riga in (0, 0); restituisce anche la maschera della sola prima cifra"""
    f = font(peso, corpo)
    cw = CELLA * corpo
    w, h = int(cw * len(testo)) + 4, int(corpo * 1.0) + 4
    tutto = Image.new('L', (w, h), 0)
    primo = Image.new('L', (w, h), 0)
    for i, ch in enumerate(testo):
        x = i * cw + (cw - f.getlength(ch)) / 2
        ImageDraw.Draw(tutto).text((x, BASE * corpo), ch, font=f, fill=255, anchor='ls')
        if i == 0:
            ImageDraw.Draw(primo).text((x, BASE * corpo), ch, font=f, fill=255, anchor='ls')
    return np.asarray(tutto, np.float32) / 255, np.asarray(primo, np.float32) / 255


def _riduci(a, k):
    h, w = a.shape[0] // k * k, a.shape[1] // k * k
    return a[:h, :w].reshape(h // k, k, w // k, k).mean((1, 3))


def unione(sag, f0, f1, passo=2, allarga=0):
    u = np.zeros((H, W), np.float32)
    for f in range(f0, f1 + 1, passo):
        u = np.maximum(u, sag.raw(f))
    if allarga:
        u = np.asarray(Image.fromarray((u * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(allarga * 2 + 1)),
                       np.float32) / 255
    return u


def piazza_numero(x, sag, fps):
    """sceglie x, y, corpo del numero (e la posizione di prefisso ed etichetta)"""
    d = x['dati']
    testo = str(d['valore'])
    f0 = int(round(d.get('arrivo', x['s']) * fps))
    f1 = int(round(x['e'] * fps)) - 1
    U = unione(sag, max(0, int(round(x['s'] * fps))), f1)
    Ug = unione(sag, max(0, int(round(x['s'] * fps))), f1, allarga=14)   # margine attorno alla persona
    K = 4
    U4, Ug4 = _riduci(U, K), _riduci(Ug, K)
    cum = np.pad(U4, ((1, 0), (1, 0))).cumsum(0).cumsum(1)

    def box(x0, y0, x1, y1):                      # copertura media di un rettangolo (px pieni)
        a, b = max(0, int(x0 / K)), min(U4.shape[1], int(x1 / K) + 1)
        c, e = max(0, int(y0 / K)), min(U4.shape[0], int(y1 / K) + 1)
        if b <= a or e <= c:
            return 1.0
        return float(cum[e, b] - cum[c, b] - cum[e, a] + cum[c, a]) / ((b - a) * (e - c))

    max_cop = d.get('copertura_max', 0.13)
    best = None
    for corpo in range(d.get('corpo_max', 620), d.get('corpo_min', 300) - 1, -20):
        G, G1 = _maschera_numero(testo, corpo)
        G4, G14 = _riduci(G, K), _riduci(G1, K)
        sg, sg1 = G4.sum(), G14.sum()
        gh, gw = G4.shape
        ps = max(64, round(corpo * 0.22))           # "più di"
        ls = max(64, round(corpo * 0.17))           # etichetta
        righe_et = str(d.get('etichetta', '')).split('\n') if d.get('etichetta') else []
        w_et = max([larghezza(r, 600, ls) for r in righe_et] or [0])
        h_et = ls * (1 + 1.08 * (len(righe_et) - 1)) if righe_et else 0
        cap = 0.70 * corpo                           # altezza delle cifre
        top_g = BASE * corpo - cap                   # bordo alto delle cifre nel box
        pre_h = ps * 0.95 + corpo * 0.06 if d.get('prefisso') else 0
        cands = []
        for yy in range(0, U4.shape[0] - gh, 3):
            y = yy * K
            if y + top_g - pre_h < SAFE_Y or y + BASE * corpo + 0.16 * corpo + h_et > H - SAFE_Y:
                continue
            fin = U4[yy:yy + gh]
            fing = Ug4[yy:yy + gh]
            for xx in range((SAFE_X + 48) // K, (W - SAFE_X - 48) // K - gw, 3):
                c1 = float((G14 * fing[:, xx:xx + gw]).sum() / sg1)
                if c1 > 0.004:
                    continue
                c = float((G4 * fin[:, xx:xx + gw]).sum() / sg)
                if c > max_cop:
                    continue
                cands.append((c, xx * K, y))
        if not cands:
            continue
        valide = []
        for c, X, Y in cands:
            g0 = X + (CELLA * corpo - font(800, corpo).getlength(testo[0])) / 2      # bordo del primo glifo
            # prefisso sopra il primo glifo, allineato a lui
            if d.get('prefisso'):
                wp = larghezza(d['prefisso'], 600, ps)
                pb = Y + top_g - corpo * 0.06                 # linea di base del prefisso
                if box(g0, pb - ps * 0.75, g0 + wp, pb + ps * 0.2) > 0.02:
                    continue
            # etichetta sotto: allineata al primo glifo, o a destra se li c'e la persona
            eb = Y + BASE * corpo + 0.16 * corpo + ls * 0.75   # base della prima riga
            gr = X + CELLA * corpo * len(testo) - (CELLA * corpo - font(800, corpo).getlength(testo[-1])) / 2
            al = None
            for lato, ex in (('sx', g0), ('dx', gr - w_et)):
                if not righe_et or box(ex, eb - ls * 0.75, ex + w_et, eb - ls * 0.75 + h_et) <= 0.02:
                    if ex >= SAFE_X and ex + w_et <= W - SAFE_X:
                        al = (lato, ex)
                        break
            if al is None:
                continue
            # si preferisce un po' di sovrapposizione (si vede che e dietro) e la vicinanza alla persona
            sc = -abs(c - d.get('copertura_obiettivo', 0.10))
            valide.append((sc, c, X, Y, g0, al, eb))
        if valide:
            sc, c, X, Y, g0, al, eb = max(valide)
            best = (corpo, c, X, Y, g0, al, eb, ps, ls)
            break
    if best is None:
        sys.exit("numero dietro: nessuna posizione in cui la persona copra al massimo il "
                 f"{max_cop * 100:.0f}% e mai la prima cifra")
    corpo, c, X, Y, g0, (lato, ex), eb, ps, ls = best
    d.update({'x': int(X), 'top': int(Y), 'corpo': corpo, 'cella': CELLA,
              'pre': {'x': round(g0), 'top': round(Y + (BASE * corpo - 0.70 * corpo) - corpo * 0.06 - BASE * ps),
                      'corpo': ps},
              'et': {'x': round(ex), 'top': round(eb - BASE * ls), 'corpo': ls, 'allinea': lato,
                     'w': round(max([larghezza(r, 600, ls) for r in str(d.get('etichetta', '')).split('\n')] or [0]))},
              '_copertura': round(c, 3)})
    # copertura vera per cifra, sulla durata dopo l'arrivo (per il rapporto)
    G, G1 = _maschera_numero(testo, corpo)
    Ua = unione(sag, f0, f1)
    gh, gw = G.shape
    fin = Ua[int(Y):int(Y) + gh, int(X):int(X) + gw]
    d['_misura'] = {'corpo': corpo, 'coperto_tot': round(float((G * fin).sum() / G.sum()), 3),
                    'coperto_prima_cifra': round(float((G1 * fin).sum() / G1.sum()), 4)}
    return d


# ------------------------------------------------------------------ card
def _a_capo(testo, peso, corpo, larg, track):
    righe, cur = [], ''
    for p in testo.split():
        prova = (cur + ' ' + p).strip()
        if cur and larghezza(prova, peso, corpo, track) > larg:
            righe.append(cur)
            cur = p
        else:
            cur = prova
    if cur:
        righe.append(cur)
    return righe


def misura_card(x):
    """per ogni card: corpi e righe di titolo e sottotitolo, altezza; il testo sta
    sempre dentro i margini fissi (si prova con la parola piu lunga)"""
    d = x['dati']
    L = d.get('larghezza', 620)
    M = d.get('margine', 56)
    dentro = L - 2 * M
    # un corpo solo per tutto il gruppo (sistema coerente): quello per cui la parola
    # piu lunga di tutte le card sta dentro i margini
    parole_t = [p for c in d['card'] for p in c['titolo'].split()]
    lunga = max(parole_t, key=lambda p: larghezza(p, 800, 100, -0.02))
    ts = min(d.get('corpo_titolo', 84), int(dentro / larghezza(lunga, 800, 1000, -0.02) * 1000))
    # una card col titolo su una riga sola (`una_riga`): il corpo comune scende quanto basta
    for c in d['card']:
        if c.get('una_riga'):
            dc = c.get('larghezza', L) - 2 * M
            ts = min(ts, int(dc / larghezza(c['titolo'], 800, 1000, -0.02) * 1000))
    if ts < 60:
        sys.exit(f"card: la parola «{lunga}» non sta in {dentro} px nemmeno a 60 px; card piu larghe")
    parole_s = [p for c in d['card'] for p in c.get('sotto', '').split()]
    ss_g = None
    if parole_s:
        lunga_s = max(parole_s, key=lambda p: larghezza(p, 500, 100))
        ss_g = max(60, min(d.get('corpo_sotto', 62), int(dentro / larghezza(lunga_s, 500, 1000) * 1000)))
    for c in d['card']:
        tt = c['titolo']
        Lc = c.get('larghezza', L)
        rt = _a_capo(tt, 800, ts, Lc - 2 * M, -0.02)
        ss = rs = None
        if c.get('sotto'):
            ss = ss_g
            rs = _a_capo(c['sotto'], 500, ss, c.get('larghezza', L) - 2 * M, 0)
            if max(larghezza(r, 500, ss) for r in rs) > c.get('larghezza', L) - 2 * M:
                sys.exit(f"card «{tt}»: il sottotitolo non sta dentro i margini")
        ic = d.get('icona', 104)
        Mv = d.get('margine_v', 40)
        h = Mv + ic + 22 + ts * 1.04 * len(rt) + ((14 + ss * 1.12 * len(rs)) if rs else 0) + Mv - 4
        c.update({'righe_t': rt, 'ts': ts, 'righe_s': rs or [], 'ss': ss, 'h': int(round(h)), 'w': Lc,
                  'margine': M, 'icona_px': ic,
                  '_larghezza_max_riga': round(max([larghezza(r, 800, ts, -0.02) for r in rt] +
                                                   [larghezza(r, 500, ss) for r in (rs or [])]), 1)})
    return d


# ------------------------------------------------------------------ mani
class Mani:
    """mani di Vision sui frame del piatto (uno ogni 2), in px d'uscita"""

    def __init__(self, cart, n, passo=2):
        from .visione import binario
        js = cart / 'mani.json'
        if not js.exists() or js.stat().st_mtime < (cart / 'piatto.chiave').stat().st_mtime:
            r = subprocess.run([str(binario()), 'mani', str(cart / 'piatto'), str(js), str(passo)],
                               stderr=subprocess.PIPE, text=True)
            if r.returncode:
                sys.exit(f"mani fallite: {r.stderr[-300:]}")
        self.n = n
        self.f = {}
        for rr in json.loads(js.read_text()):
            f = int(rr['file'][1:7])
            self.f[f] = [{'x': h['x'] * W, 'y': h['y'] * H, 'lato': h['lato'],
                          'box': [h['box'][0] * W, h['box'][1] * H, h['box'][2] * W, h['box'][3] * H]}
                         for h in rr['mani']]
        self.chiavi = sorted(self.f)

    def al(self, f):
        if not self.chiavi:
            return []
        k = min(self.chiavi, key=lambda c: abs(c - f))
        return self.f[k] if abs(k - f) <= 2 else []


def lega_mani(x, mani, fps):
    """ogni card (o l'elemento) prende la mano piu vicina al suo arrivo: da li parte"""
    d = x['dati']
    for c in d.get('card', [d]):
        if 'x' not in c or 's' not in c:
            continue
        f = int(round(c['s'] * fps))
        cx = c['x'] + c.get('w', 600) / 2
        cy = c['y'] + c.get('h', 300) / 2
        cand = [h for g in range(f - 3, f + 4) for h in mani.al(g)]
        if cand:
            h = min(cand, key=lambda h: (h['x'] - cx) ** 2 + (h['y'] - cy) ** 2)
            # il filo parte appena fuori dalla mano (24 px oltre il suo riquadro), verso la card
            hx, hy = h['x'], h['y']
            a0, b0, a1, b1 = h['box']
            dx, dy = cx - hx, cy - hy
            n = math.hypot(dx, dy) or 1
            k = 0
            while k < 600 and a0 - 24 <= hx + dx / n * k <= a1 + 24 and b0 - 24 <= hy + dy / n * k <= b1 + 24:
                k += 4
            c['mano'] = [round(hx + dx / n * k), round(hy + dy / n * k)]


def piazza_card(x, mani, volto, sag, fps):
    """posto di ogni card senza x/y: mai sopra una mano (Vision, +24 px) o la testa
    (+30 px) in tutto il tempo in cui e a schermo; sul lato `zona` (sx/dx); il piu
    vicino possibile alla mano da cui parte, con poca sovrapposizione al corpo"""
    d = x['dati']
    for c in d['card']:
        if 'x' in c and 'y' in c:
            continue
        if c.get('dietro') or x.get('strato') == 'dietro':
            _piazza_dietro(c, volto, sag, fps)
            continue
        w, h = c['w'], c['h']
        # dall'arrivo del filo a meta dell'uscita (poi la card e gia piccola e trasparente)
        f0, f1 = int(round(c['s'] * fps)) - 3, int((c['e'] - 0.12) * fps)
        vieta = np.zeros((H // 8 + 1, W // 8 + 1), bool)
        for f in range(max(0, f0), f1 + 1):
            for m in mani.al(f):
                a0, b0, a1, b1 = m['box']
                vieta[max(0, int((b0 - 24) / 8)):int((b1 + 24) / 8) + 1, max(0, int((a0 - 24) / 8)):int((a1 + 24) / 8) + 1] = True
            b = volto.box(f / fps)
            if b:
                vieta[max(0, int((b[1] - 30) / 8)):int((b[3] + 30) / 8) + 1, max(0, int((b[0] - 30) / 8)):int((b[2] + 30) / 8) + 1] = True
        cum = np.pad(vieta.astype(np.int32), ((1, 0), (1, 0))).cumsum(0).cumsum(1)
        U = _riduci(unione(sag, max(0, f0), f1, passo=3), 8)
        cu = np.pad(U, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
        mano0 = [m for g in range(f0, f0 + 7) for m in mani.al(g)]
        zona = c.get('zona', 'sx')
        best = None
        # 24 px in piu dei margini sicuri: l'inclinazione (8 gradi) e il fluttuare allargano la card
        mx, my = SAFE_X + 24, SAFE_Y + 24
        xs = sorted(set(list(range(mx, W - mx - w + 1, 8)) + [W - mx - w]))
        ys = sorted(set(list(range(my, H - my - h + 1, 8)) + [H - my - h]))
        for X in xs:
            if (zona == 'sx' and X + w / 2 > W / 2) or (zona == 'dx' and X + w / 2 < W / 2):
                continue
            for Y in ys:
                a, b, cc, e = X // 8, (X + w) // 8, Y // 8, (Y + h) // 8
                if cum[e, b] - cum[cc, b] - cum[e, a] + cum[cc, a] > 0:
                    continue
                corpo = (cu[e, b] - cu[cc, b] - cu[e, a] + cu[cc, a]) / max(1, (b - a) * (e - cc))
                cx, cy = X + w / 2, Y + h / 2
                dm = min([math.hypot(m['x'] - cx, m['y'] - cy) for m in mano0] or [0])
                sc = dm / 1000 + corpo * 0.8 + c.get('alto', 0.0) * Y / 1000
                if best is None or sc < best[0]:
                    best = (sc, X, Y, corpo)
        if best is None:
            sys.exit(f"card «{c['titolo']}»: nessun posto libero da mani e volto ({w}x{h}, zona {zona}); card piu piccola")
        c['x'], c['y'] = best[1], best[2]
        c['_corpo_coperto'] = round(float(best[3]), 3)
    return d


def _piazza_dietro(c, volto, sag, fps):
    """card DIETRO la persona (fase 6c): le mani e la spalla le passano davanti da
    sole, quindi il vincolo non e piu "lontano dalle mani" ma "la persona ne copre al
    massimo il 10% e mai il testo", fotogramma per fotogramma; mai dietro la testa.
    Si preferisce un po' di sovrapposizione (si vede che e dietro) vicino a lui."""
    w, h = c['w'], c['h']
    f0, f1 = int(round(c['s'] * fps)), int((c['e'] - 0.12) * fps)
    K = 8
    fr = list(range(max(0, f0), f1 + 1, 2))
    M = np.stack([_riduci(sag.raw(f), K) for f in fr])                     # (n, 135, 240)
    cum = np.pad(M, ((0, 0), (1, 0), (1, 0))).cumsum(1).cumsum(2)
    teste = [volto.box(f / fps) for f in fr]
    teste = [t for t in teste if t]

    def cop(X0, Y0, X1, Y1):
        a, b, cc, e = int(X0 // K), int(X1 // K), int(Y0 // K), int(Y1 // K)
        if b <= a or e <= cc:
            return np.zeros(len(fr))
        return (cum[:, e, b] - cum[:, cc, b] - cum[:, e, a] + cum[:, cc, a]) / ((b - a) * (e - cc))

    mx = c.get('dietro_max', 0.10)
    m_ = c.get('margine', 46)
    zona = c.get('zona', 'dx')
    best = None
    for X in range(SAFE_X, W - SAFE_X - w + 1, 8):
        if (zona == 'sx' and X + w / 2 > W / 2) or (zona == 'dx' and X + w / 2 < W / 2):
            continue
        for Y in range(SAFE_Y, H - SAFE_Y - h + 1, 8):
            if any(not (X + w < t[0] - 30 or X > t[2] + 30 or Y + h < t[1] - 30 or Y > t[3] + 30) for t in teste):
                continue
            tot = cop(X, Y, X + w, Y + h)
            if tot.max() > mx:
                continue
            testo = cop(X + m_, Y + h * 0.36, X + w - m_, Y + h - 30)
            if testo.max() > 0.01:
                continue
            sc = abs(tot.max() - c.get('dietro_obiettivo', 0.07)) + 0.0002 * abs(Y - c.get('y_pref', Y))
            if best is None or sc < best[0]:
                best = (sc, X, Y, float(tot.max()), float(testo.max()))
    if best is None:
        sys.exit(f"card «{c['titolo']}» dietro: nessun posto in cui la persona ne copra al massimo il "
                 f"{mx * 100:.0f}% e mai il testo")
    c['x'], c['y'] = best[1], best[2]
    c['_dietro_coperto'] = round(best[3], 3)
    c['_testo_coperto'] = round(best[4], 4)


def piazza_battute(x, volto, fps):
    """frase sul corpo a battute (una o due parole enormi per volta): corpo che fa
    stare la riga in `larghezza` (max `corpo_max`, peso 900), centro sul busto (centro
    della testa nella battuta), bordo alto sotto il punto piu basso della testa"""
    d = x['dati']
    for b in d['battute']:
        testo = ' '.join(p['testo'] for p in b['parole'])
        # gerarchia (fase 7b rivista): una parola puo avere `scala` (es. 0,5): si misura
        # parola per parola al suo corpo e al suo peso
        def _lw(cc):
            ps = b['parole']
            return sum(larghezza(p['testo'], p.get('peso', 900), cc * p.get('scala', 1.0), -0.03) for p in ps) + \
                larghezza(' ', 900, cc, 0) * 0.6 * (len(ps) - 1)
        testo_w = _lw(1000)
        c = min(b.get('corpo_max', d.get('corpo_max', 260)),
                int(d.get('larghezza', 1560) / testo_w * 1000))
        if c < 120:
            sys.exit(f"battuta «{testo}»: corpo {c} troppo piccolo per una frase sul corpo")
        boxes = [volto.box(f / fps) for f in range(int(b['s'] * fps), int(b['e'] * fps) + 1)]
        boxes = [q for q in boxes if q]
        cx = float(np.mean([(q[0] + q[2]) / 2 for q in boxes])) if boxes else W / 2
        w = _lw(c)
        # la riga entra con un colpo di scala al 110% (parole.js): anche allora dentro la zona sicura
        k = 1.03 if w > 1400 else 1.10        # righe larghe: colpo piu piccolo
        cx = min(max(cx, SAFE_X + k * w / 2), W - SAFE_X - k * w / 2)
        fondo = max(q[3] for q in boxes) if boxes else H * 0.5
        # bordo alto delle lettere (BASE - 0,72 em sotto il bordo del box) sotto il mento + margine
        top = fondo + d.get('margine_volto', 56) - (BASE - 0.72) * c
        top = min(top, H - SAFE_Y - BASE * c - 0.06 * c)
        b.update({'corpo': c, 'cx': round(cx), 'top': round(top), '_larghezza': round(w)})
    return d


def adatta_colonna(x):
    """testo di una colonna (CTA, lista): ogni riga al corpo massimo che sta nella
    larghezza della colonna (font e pesi veri), mai sotto 60 px"""
    d = x['dati']
    L = d['larghezza']
    for r in d.get('righe', []):
        testo = ' '.join(p['testo'] for p in r['parole'])
        r['corpo'] = min(r.get('corpo_max', 200), int(L / larghezza(testo, r.get('peso', 900), 1000, -0.03) * 1000))
        if r['corpo'] < 60:
            sys.exit(f"«{testo}» non sta in {L} px")
    if d.get('titolo'):
        t = d['titolo']
        t['corpo'] = min(t.get('corpo_max', 150), int(L / larghezza(t['testo'], 900, 1000, -0.03) * 1000))
    if d.get('voci'):
        spazio = L - d.get('spunta', 84) - 28
        lunga = max(d['voci'], key=lambda v: larghezza(v['testo'], 700, 100))
        d['corpo_voci'] = min(d.get('corpo_voci_max', 80), int(spazio / larghezza(lunga['testo'], 700, 1000) * 1000))
        if d['corpo_voci'] < 60:
            sys.exit(f"«{lunga['testo']}» non sta nella colonna a 60 px")
    return d


def apertura_schermata(x, scala=1.6):
    """schermata tipografica: la prima parola entra al centro dello schermo a `scala`
    e scivola al suo posto quando arriva la seconda. Calcola lo spostamento con il
    font vero (la pagina scala il blocco attorno a (x, 540))."""
    d = x['dati']
    righe, cur = [], []
    for p in d['parole']:
        if p.get('a_capo') and cur:
            righe.append(cur)
            cur = []
        cur.append(p)
    righe.append(cur)
    alt = [max(d.get('corpo_chiave', 230) if p.get('chiave') else d.get('corpo', 124) for p in r) for r in righe]
    Htot = sum(alt)
    p0 = d['parole'][0]
    c0 = d.get('corpo_chiave', 230) if p0.get('chiave') else d.get('corpo', 124)
    w0 = larghezza(p0['testo'], 800 if p0.get('chiave') else 400, c0, -0.015)
    x0 = d.get('x', 220)
    cy0 = H / 2 - Htot / 2 + alt[0] / 2
    s = min(scala, (W - 2 * SAFE_X) / w0)
    d['apertura'] = {'s': round(s, 3), 'tx': round(W / 2 - x0 - s * w0 / 2, 1), 'ty': round(-s * (cy0 - H / 2), 1)}
    return d


def adatta_schermata(x):
    """schermata tipografica: nessuna riga esce dai margini. Se una riga e piu larga
    dello spazio fra `x` e il margine destro, corpo e corpo della chiave scendono
    insieme (stessa proporzione)."""
    d = x['dati']
    x0 = d.get('x', 220)
    # la schermata avanza piano fino al 107% attorno al 30% della larghezza: si misura
    # lo spazio come sara alla fine
    piv = 0.30 * W
    disp = (W - SAFE_X - piv) / d.get('avanza', 1.07) + piv - x0 - 8
    righe, cur = [], []
    for p in d['parole']:
        if p.get('a_capo') and cur:
            righe.append(cur)
            cur = []
        cur.append(p)
    righe.append(cur)
    c, ck = d.get('corpo', 124), d.get('corpo_chiave', 230)

    def larg(r, c, ck):
        tot = 0
        for p in r:
            k = p.get('chiave')
            cc = ck if k else c
            tot += larghezza(p['testo'], 800 if k else 400, cc, -0.035 if k else -0.015) + 0.22 * cc
        return tot

    peggio = max(larg(r, c, ck) / disp for r in righe)
    if peggio > 1:
        d['corpo'], d['corpo_chiave'] = int(c / peggio), int(ck / peggio)
    d['_righe_px'] = [round(larg(r, d.get('corpo', c), d.get('corpo_chiave', ck))) for r in righe]
    return d


# ------------------------------------------------------------------ titoli dietro (fase 7b)
def _maschera_righe(linee, corpo, track=-0.035, lh=0.98):
    """maschera delle lettere di un blocco di righe in maiuscolo (allineate a sinistra),
    come le disegna titolo_dietro.js (peso 900, line-height 0,98, tracking -0,035 em).
    Torna (maschera, maschera della prima lettera, larghezza, altezza)."""
    f = font(900, corpo)
    # fase 7c: le righe arrivano gia nella forma a schermo (forma_titolo); qui non si cambia piu il maiuscolo
    wl = [sum(f.getlength(ch) + track * corpo for ch in r) for r in linee]
    w, h = int(max(wl)) + 4, int(round(len(linee) * lh * corpo)) + 4
    m = Image.new('L', (w, h), 0)
    p = Image.new('L', (w, h), 0)
    d, dp = ImageDraw.Draw(m), ImageDraw.Draw(p)
    base = ((lh - 1.219) / 2 + 0.968) * corpo
    _maschera_righe.lettere = []          # riquadri (x0, y0, x1, y1) di ogni lettera
    for i, r in enumerate(linee):
        x = 0.0
        for k, ch in enumerate(r):
            d.text((x, i * lh * corpo + base), ch, font=f, fill=255, anchor='ls')
            if i == 0 and k == 0:
                dp.text((x, base), ch, font=f, fill=255, anchor='ls')
            if ch.strip():
                prima_l = k == 0 or not r[k - 1].strip()
                ultima_l = k == len(r) - 1 or (k + 1 < len(r) and not r[k + 1].strip())
                lim = 0.02 if prima_l else (0.15 if ultima_l else 0.30)
                _maschera_righe.lettere.append((int(x), int(i * lh * corpo), int(x + f.getlength(ch)),
                                                int((i + 1) * lh * corpo), lim))
            x += f.getlength(ch) + track * corpo
    return np.asarray(m, np.float32) / 255, np.asarray(p, np.float32) / 255, w, h


def forma_titolo(d):
    """(righe come stanno a schermo, tracking, interlinea) del titolo dietro: forma del sito
    (fase 7c: minuscolo con il punto, -0,045 em, 0,92) o maiuscolo (variante, -0,035 em, 0,98)"""
    if d.get('forma') == 'maiuscolo':
        return [r.upper() for r in d['linee']], -0.035, 0.98
    n = len(d['linee'])
    return [r.lower() + ('.' if k == n - 1 and not r.rstrip()[-1:] in '.!?…' else '') for k, r in enumerate(d['linee'])], -0.045, 0.92


def piazza_titolo(x, sag, fps):
    """il titolo di capitolo passa davvero dietro la persona: corpo e posto scelti sulle
    sagome di tutta la durata. Lui copre fra `copertura_min` e `copertura_max` delle
    lettere (si vede che e dietro, ma si legge), mai la prima lettera, nessuna riga oltre
    il 20%, la prima lettera di ogni parola libera, l'ultima al massimo al 15%, le altre al
    30%; tutto dentro la zona sicura. Si preferisce il corpo piu grande."""
    d = x['dati']
    f0, f1 = max(0, int(round(x['s'] * fps))), int(round(x['e'] * fps)) - 1
    U = unione(sag, f0, f1)
    Ug = unione(sag, f0, f1, allarga=14)
    K = 4
    U4, Ug4 = _riduci(U, K), _riduci(Ug, K)
    cmin, cmax = d.get('copertura_min', 0.04), d.get('copertura_max', 0.12)
    for corpo in range(d.get('corpo_max', 250), d.get('corpo_min', 160) - 1, -10):
        righe_, tr_, lh_ = forma_titolo(d)
        G, G1, w, h = _maschera_righe(righe_, corpo, tr_, lh_)
        lettere = [(a // K, b // K, max(a // K + 1, c // K), max(b // K + 1, e // K), bo) for a, b, c, e, bo in _maschera_righe.lettere]
        if w > W - 2 * SAFE_X:
            continue
        G4, G14 = _riduci(G, K), _riduci(G1, K)
        gh, gw = G4.shape
        sg, sg1 = G4.sum(), G14.sum()
        righe = [(int(i * lh_ * corpo / K), int((i + 1) * lh_ * corpo / K)) for i in range(len(d['linee']))]
        cands = []
        # sulla parete: sopra il piano del tavolo (gli oggetti sul tavolo Vision li conta come primo piano)
        y_max = d.get('y_max', 760)
        for yy in range(SAFE_Y // K, min((H - SAFE_Y), y_max) // K - gh, 3):
            fin, fing = U4[yy:yy + gh], Ug4[yy:yy + gh]
            for xx in range(SAFE_X // K, (W - SAFE_X) // K - gw, 3):
                if float((G14 * fing[:, xx:xx + gw]).sum() / sg1) > 0.004:
                    continue
                win = G4 * fin[:, xx:xx + gw]
                c = float(win.sum() / sg)
                if not cmin <= c <= cmax:
                    continue
                if any(G4[a:b].sum() and win[a:b].sum() / G4[a:b].sum() > 0.20 for a, b in righe):
                    continue
                # lettere (fase 7b rivista: la «O» di PARTIAMO spariva dietro la testa e si
                # leggeva «PARTIAM», poi «PARTIAMC»): la prima lettera di ogni parola libera,
                # l'ultima coperta al massimo al 15%, le altre al 30%
                if any(G4[b:e, a:c].sum() > 0 and win[b:e, a:c].sum() / G4[b:e, a:c].sum() > lim
                       for a, b, c, e, lim in lettere):
                    continue
                cy = (yy + gh / 2) * K
                cands.append((-abs(c - 0.08) - abs(cy - d.get('y_preferita', 380)) / 1500, c, xx * K, yy * K))
        if cands:
            sc, c, X, Y = max(cands)
            d.update({'corpo': corpo, 'allinea': 'sx', 'x': X, 'y': round(Y + h / 2), '_copertura': round(c, 3)})
            return d
    if cmin > 0 and not d.get('_ripiego'):
        # nessun posto in cui passi dietro e si legga: il titolo resta leggibile e scoperto (si segnala)
        print(f"  ! titolo dietro «{' '.join(d['linee'])}»: non trova un posto dietro di lui "
              f"(copertura {cmin:.0%}-{cmax:.0%}); resta sulla parete, non coperto")
        d.update({'copertura_min': 0.0, '_ripiego': True})
        return piazza_titolo(x, sag, fps)
    raise SystemExit(f"titolo dietro «{' '.join(d['linee'])}»: nessun posto leggibile sulla parete")

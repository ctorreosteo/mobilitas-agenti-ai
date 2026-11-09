"""Controlli del piano per i reel (fase 6, 05/11/2026): zone delle micro-grafiche e dei modelli sulla persona, mappa
del ritmo.

07/11/2026 (Riccardo): copertura e ritmo qui sotto sono SOLO INFORMAZIONE (tolte come regole); micro-grafiche e modelli sulla
persona non si usano con il sistema di forme (reel_palco). Storia: ritmo (regola del 05/11/2026, superata): densità «piena», un cambiamento visivo ogni 2–3 s circa, su due livelli
(infografiche grandi e micro-grafiche); mai due cose da leggere nello stesso momento. L'obiettivo in numeri viene
dalla misura delle reference (`libreria/reference/ritmo.json`, `./mve reel-ritmo-reference`): eventi visivi
ogni 10 s e pausa più lunga.

Un evento visivo del reel si conta come nelle reference:
- un taglio del video base (non quelli coperti da una grafica a tutto schermo);
- l'entrata di una grafica o di una sua apparizione;
- ogni testo che compare dopo l'entrata (voce di lista, parola, termine dell'equazione);
- gli eventi di stato scritti nel piano (`eventi`: [{t, cosa}], per esempio una barra o un'accensione);
- l'inizio di una micro-grafica;
- l'inizio di uno zoom.
Gli eventi a meno di 0,25 s l'uno dall'altro contano una volta.

Giro 3 (Riccardo, 05/11/2026): quella misura conta anche i tagli del video base (la versione pubblicata era già a 6,2
ogni 10 s senza nessuna grafica in più). Da ora il controllo misura solo il NOSTRO strato grafico:
- copertura: la parte del reel con almeno una nostra grafica a schermo (obiettivo: almeno 85%);
- eventi nostri: entrata di una grafica o di una sua apparizione, testo nuovo dentro una grafica, evento di stato
  scritto nel piano; niente tagli, niente zoom. Mai più di 3 s fra due eventi nostri (dall'inizio del reel alla fine).
La misura di prima (con tagli e zoom) resta come informazione accanto.

Giro 4 (Riccardo, 05/11/2026): «una parola o una frase da sola, anche grande e animata, NON è una grafica e non conta
nella copertura. Ogni grafica deve MOSTRARE il concetto con un contenuto visivo: icona o illustrazione che si anima,
diagramma, collegamento fra elementi, contatore, piccola scena con più elementi, disegno Servier, card con icona. Il
testo è solo un'etichetta. Copertura e ritmo contano solo queste grafiche». Ogni grafica del piano ha un contenuto
(`contenuto()`): «visivo» (conta), «testo» (solo parole: non conta), «segno» (cerchio, freccia, sottolineatura sul
video: non conta). La copertura e gli eventi nostri si misurano solo sulle grafiche «visivo».
"""
import json
from pathlib import Path

import numpy as np

from . import reel_comune as C
from .reel_comune import W, H, SAFE

RITMO = C.AGENTE / 'libreria' / 'reference' / 'ritmo.json'
FUSIONE = 0.25
# giro 3 (Riccardo, 05/11/2026): il nostro strato grafico
STRATO = {'copertura_min': 0.85, 'pausa_max_s': 3.0,
          'fonte': "Riccardo, 05/11/2026 (giri 3 e 4): almeno l'85% del reel con una nostra grafica VERA a schermo (un "
                   "contenuto visivo: icona, diagramma, collegamento, contatore, scena, Servier, card con icona; una parola o una "
                   "frase da sola non conta); una grafica nuova (entrata o cambio) almeno ogni 2-3 s"}


# giro 4: che cosa mostra ogni modello. «visivo» conta nella copertura e nel ritmo; «testo» e «segno» no.
CONTENUTO = {
    'connettore-finestra': ('visivo', 'collegamento fra elementi: due etichette unite da una linea con il nodo'),
    'card-accese-9x16-carrello': ('visivo', 'card con la cifra nel medaglione e le icone «?»; carrello di camera'),
    'card-accese-9x16': ('visivo', 'card con la cifra che si accendono'),
    'card-con-spessore-9x16': ('visivo', 'card con spessore e icona'),
    'anatomia-scena-9x16': ('visivo', 'disegno Servier'), 'anatomia-scena': ('visivo', 'disegno Servier'),
    'fumetto-finestra': ('visivo', 'piccola scena: fumetto di chat con i puntini, poi la frase'),
    'riga-icone-9x16': ('visivo', 'icone che si disegnano'),
    'chiusura-9x16': ('visivo', 'scena: prezzo, modulo con il pulsante, marchio'),
    'chiusura-9x16-v2': ('visivo', 'scena: prezzo, modulo con il pulsante, marchio'),
    'infografica-finestra': ('visivo', 'infografica: icone che si animano, collegamenti, scena'),
    'infografica-9x16': ('visivo', 'infografica: icone che si animano, collegamenti, scena'),
    'infografica-cerchio-9x16': ('visivo', 'infografica a tutto schermo con lui nel cerchio'),
    'palco-fascia-alta': ('visivo', 'il palco: oggetti-prova che si trasformano seguendo la voce (card, Servier, lista, barre, indicatore)'),
    'infografica-sopra': ('visivo', 'infografica sopra il video (B-roll visibile): icone grandi, collegamenti, card con icona'),
    'infografica-persona': ('visivo', 'infografica sulla persona: icone, collegamenti, card con icona, anche dietro di lei'),
    'etichette-barrate-finestra-centrate-icone': ('visivo', "card con icona: l'oggetto e la parola barrati insieme"),
    'parole-finestra-icone': ('visivo', "icona (o disegno Servier) davanti a ogni parola, che si accende con lei"),
    'micro-icona': ('visivo', 'icona che si disegna in un disco'),
    'micro-scheda': ('visivo', 'card con icona'),
    'micro-parola': ('testo', 'parola in una pillola'), 'micro-parole': ('testo', 'parole in pannelli'),
    'micro-numero': ('testo', 'cifra detta da sola'),
    'micro-cerchio': ('segno', 'cerchio su un dettaglio del video'), 'micro-freccia': ('segno', 'freccia sul video'),
}


def contenuto(idg):
    """(«visivo»|«testo»|«segno», perché) per un id del catalogo; i modelli non classificati valgono «testo» (non contano)"""
    if idg in CONTENUTO:
        return CONTENUTO[idg]
    if idg and idg.startswith(('etichette-barrate', 'parole-finestra', 'equazione', 'aggancio', 'titolo-dietro', 'numero-dietro',
                               'frase-sul-corpo')):
        return ('testo', 'parole o frasi dette, senza un contenuto visivo')
    return ('testo', 'modello non classificato: vale come testo finché non si classifica in reel_piano.CONTENUTO')


def obiettivo():
    """{ogni_10s, pausa_max_s, fonte} dalla misura delle reference (se non c'è, la regola di Riccardo: uno ogni 2-3 s)"""
    if RITMO.exists():
        r = json.loads(RITMO.read_text())
        return r['obiettivo']
    return {'ogni_10s': 4.0, 'pausa_max_s': 3.0, 'fonte': "regola di Riccardo (05/11/2026): un cambiamento ogni 2-3 s; reference non ancora misurate"}


_ZONE = {}


def _zone(R):
    from . import reel_radiografia as RR
    p = C.AGENTE / R['zone_libere']['file']
    k = (str(p), p.stat().st_mtime)
    if k not in _ZONE:
        _ZONE.clear()
        _ZONE[k] = RR.carica_zone(p)
    return _ZONE[k]


def _box(g):
    for x in g.get('elementi') or []:
        b = (x.get('dati') or {}).get('box')
        if b:
            return b, x.get('dati') or {}
    return None, {}


# giro 5 (Riccardo, 06/11/2026: «le grafiche si appoggiano SUL video»): un'infografica sopra il B-roll (infografica_reel,
# modo libero) non copre il suo riquadro intero ma solo i suoi pezzi; si controlla pezzo per pezzo, ognuno nel suo tempo
_FONT = {}


def _larghezza(testo, corpo):
    from PIL import ImageFont
    if corpo not in _FONT:
        f = ImageFont.truetype(str(C.AGENTE / 'motore' / 'motore' / 'risorse' / 'fonts' / 'Montserrat-VF.ttf'), corpo)
        try:
            f.set_variation_by_axes([800])
        except Exception:
            pass
        _FONT[corpo] = f
    return _FONT[corpo].getlength(testo) * 0.98


def pezzi_sopra(dati, durata):
    """[(tipo, [x0, y0, x1, y1], t0, t1, con_testo)] dei pezzi di un'infografica sopra il video (bagliore compreso)"""
    out = []
    for p in dati.get('pezzi') or []:
        tp, t0 = p.get('tipo'), float(p.get('t', 0) or 0)
        t1 = float(p['via']) if p.get('via') is not None else durata
        if tp in ('disco', 'pittogramma', 'anello'):
            m = p.get('lato', 160) / 2 * 1.12
            t0 = min(t0, float(p['prima'])) if p.get('prima') is not None else t0
            out.append((tp, [p['x'] - m, p['y'] - m, p['x'] + m, p['y'] + m + 10], t0, t1, False))
        elif tp == 'logo':
            W = p.get('w', 520); H = round(W / 7.27); pad = round(H * 0.55)
            out.append((tp, [p['x'] - W / 2 - pad, p['y'] - H / 2 - pad, p['x'] + W / 2 + pad, p['y'] + H / 2 + pad + 10], t0, t1, False))
        elif tp == 'etichetta':
            cp = p.get('corpo', 84); lh = round(cp * 1.2)
            stati = [p.get('testo', '')] + [c.get('testo', '') for c in p.get('cambia') or []]
            w = max(_larghezza(t, cp) for t in stati) + (2 * round(cp * p.get('pad', 0.42)) if p.get('pillola') else 0)
            h = lh + (round(cp * 0.28) if p.get('pillola') else 0)
            al = p.get('allinea', 'centro')
            x0 = p['x'] if al == 'sx' else (p['x'] - w if al == 'dx' else p['x'] - w / 2)
            out.append((tp, [x0, p['y'] - h / 2, x0 + w, p['y'] + h / 2 + 4], t0, t1, True))
        elif tp == 'linea':
            sp = p.get('spessore', 7) + 6
            (xa, ya), (xb, yb) = p['da'], p['a']
            t0 = min(t0, float(p['prima'])) if p.get('prima') is not None else t0
            out.append((tp, [min(xa, xb) - sp, min(ya, yb) - sp, max(xa, xb) + sp, max(ya, yb) + sp], t0, t1, False))
        elif tp == 'arco':
            r = p.get('r', 100) + p.get('spessore', 14)
            out.append((tp, [p['x'] - r, p['y'] - r, p['x'] + r, p['y'] + r], t0, t1, False))
        elif tp == 'punti':
            x, y, w, h = p['area']
            out.append((tp, [x, y, x + w, y + h], t0, t1, False))
        elif tp in ('scheda', 'immagine') and p.get('w'):
            out.append((tp, [p['x'], p['y'], p['x'] + p['w'], p['y'] + p.get('h', p['w'])], t0, t1, False))
    return [(tp, [int(round(v)) for v in b], t0, t1, tx) for tp, b, t0, t1, tx in out]


def controlla_sopra(g, R, vis, f0, fps, dati):
    """infografica sopra il video: ogni pezzo, nel suo tempo, fuori da volti/teste, sottotitoli, scritte del video e striscia
    sopra le finestre; i testi nella zona sicura Meta e almeno al corpo minimo del reel (1,5× i sottotitoli). Le mani del
    B-roll sono un avviso (giro 3)"""
    from . import reel_radiografia as RR
    from .reel_piano_base import corpo_minimo
    err, avv = [], []
    n = g['nome']
    Z = _zone(R)
    inq_di = {f: s for s in R['inquadrature'] for f in range(s['f0'], s['f1'] + 1)}
    durata = g['frames'] / fps
    cmin, _ = corpo_minimo(R)
    # le teste si controllano sui riquadri veri di Apple Vision (volto allargato con i capelli, +10 px), non sulle celle da 60 px
    pj = C.AGENTE / Path(R['zone_libere']['file']).parent / 'persona.json'
    pers = json.loads(pj.read_text()) if pj.exists() else None
    teste = [x.get('teste') or [] for x in pers] if pers else None
    manip = [x.get('mani') or [] for x in pers] if pers else None
    tocca = lambda b, t, m: b[0] < t[2] + m and b[2] > t[0] - m and b[1] < t[3] + m and b[3] > t[1] - m
    trov, mani = {}, []
    for k, (tp, b, t0, t1, tx) in enumerate(pezzi_sopra(dati, durata)):
        nome = f"{tp} {k} {b}"
        if tx and (b[0] < SAFE[0] or b[1] < SAFE[1] or b[2] > SAFE[2] or b[3] > SAFE[3]):
            err.append(f"{n}: il testo {nome} esce dalla zona sicura Meta {list(SAFE)}")
        fs = [f for f in sorted(vis) if f0 + t0 * fps - 0.5 <= f < f0 + t1 * fps]
        r0, r1, c0, c1 = RR._celle([max(0, b[0]), max(0, b[1]), min(1079, b[2]), min(1919, b[3])])
        for f in fs:
            for st in ('sottotitoli', 'scritte') + (() if teste is not None else ('testa',)):
                if Z[st][f, r0:r1 + 1, c0:c1 + 1].any():
                    trov.setdefault((st, nome), []).append(f)
            if teste is not None and f < len(teste) and any(tocca(b, t, 10) for t in teste[f]):
                trov.setdefault(('un volto (testa)', nome), []).append(f)
            s = inq_di.get(f)
            # con la persona in camera le mani non si coprono (riquadri veri); nei B-roll è un avviso (giro 3)
            if (s or {}).get('tipo') == 'persona in camera' and manip is not None:
                if f < len(manip) and any(tocca(b, t, 6) for t in manip[f]):
                    trov.setdefault(('le mani della persona in camera', nome), []).append(f)
            elif Z['mani'][f, r0:r1 + 1, c0:c1 + 1].any():
                mani.append(f)
            if s and s.get('schema') and b[1] < min(w['y'] for w in s['finestre']) - 4:
                trov.setdefault(('la striscia sopra le finestre (non si usa)', nome), []).append(f)
    for (st, nome), fs in trov.items():
        err.append(f"{n}: il pezzo {nome} copre {st} in {len(fs)} fotogrammi (primo f{fs[0]}): spostalo")
    if mani:
        avv.append(f"{n}: i pezzi passano sopra le mani del B-roll in {len(set(mani))} fotogrammi (primo f{min(mani)}): ammesso (giro 3), "
                   "da guardare che il gesto resti leggibile")
    cc = [p.get('corpo', 84) for p in dati.get('pezzi') or [] if p.get('tipo') == 'etichetta']
    if cc and min(cc) < cmin:
        err.append(f"{n}: etichetta a corpo {min(cc)}: almeno {cmin} (1,5× i sottotitoli)")
    sc = [q for q in R.get('scritte_video') or [] if set(range(q['f0'], q['f1'] + 1)) & vis]
    if sc and cc:
        avv.append(f"{n}: mentre c'è la grafica, nel video c'è già la scritta «{sc[0]['t']}» (f{sc[0]['f0']}-{sc[0]['f1']}): "
                   "due cose da leggere insieme?")
    return err, avv


def controlla_zona(g, R, vis, f0, fps, zoom):
    """micro e persona: il riquadro della grafica (dati.box {x, y, w, h}) dentro la zona sicura e, su ogni fotogramma
    visibile, fuori da teste, mani, sottotitoli e scritte del video (con lo zoom, nel punto del video base da cui viene)"""
    from . import reel_radiografia as RR, reel_zoom as RZ
    err, avv = [], []
    n, modo = g['nome'], g['modo']
    if not R.get('zone_libere'):
        return [f"{n}: «{modo}» vuole la radiografia generica (zone libere): rifare ./mve reel-radiografia"], []
    b, dati = _box(g)
    if not b:
        return [f"{n}: «{modo}» senza dati.box {{x, y, w, h}} (il riquadro che la grafica occupa, bagliore compreso)"], []
    if dati.get('modo') == 'libero' and not dati.get('dietro') and any(x.get('modello') == 'infografica_reel' for x in g.get('elementi') or []):
        return controlla_sopra(g, R, vis, f0, fps, dati)
    bx = [b['x'], b['y'], b['x'] + b['w'] - 1, b['y'] + b['h'] - 1]
    con_testo = bool([t for x in g.get('elementi') or [] for t in _testi(x)])
    if modo == 'micro' and con_testo and (bx[0] < SAFE[0] or bx[1] < SAFE[1] or bx[2] > SAFE[2] or bx[3] > SAFE[3]):
        err.append(f"{n}: il riquadro {bx} esce dalla zona sicura Meta {list(SAFE)} (vale per i testi)")
    if modo == 'micro' and not con_testo:
        # un segno senza testo (cerchio, freccia, icona) può uscire dalla zona sicura, ma resta dentro una finestra
        # (giro 3: anche le finestre piccole, «nelle finestre piccole icone e segni»)
        for f in sorted(vis)[:1]:
            s0 = next((q for q in R['inquadrature'] if q['f0'] <= f <= q['f1']), None)
            fin = (s0 or {}).get('finestre') or [] if (s0 or {}).get('schema') else []
            if fin and not any(bx[0] >= w0['x'] and bx[1] >= w0['y'] and bx[2] <= w0['x1'] and bx[3] <= w0['y1'] for w0 in fin):
                err.append(f"{n}: il segno {bx} non sta dentro una finestra ({[[w0['x'], w0['y'], w0['x1'], w0['y1']] for w0 in fin]})")
    if modo == 'micro':
        e2, a2 = _grandezza(g, R, vis, bx, dati, con_testo)
        err += e2; avv += a2
    Z = _zone(R)
    inq_di = {f: s for s in R['inquadrature'] for f in range(s['f0'], s['f1'] + 1)}
    tre = {f for a, c in (R.get('animazioni_3d') or {}).get('fotogrammi', []) for f in range(a, c + 1)}
    # tappa 2 (06/11/2026): «dietro» la persona intera (mani comprese) torna sopra la grafica: né testa né mani bloccano
    strati = ['sottotitoli', 'scritte'] + ([] if dati.get('dietro') else ['mani', 'testa'])
    # (la card «vicino alle mani» sta accanto alle mani, non sopra: le mani restano da non coprire; voto del direttore
    # sulla prova del 05/11/2026)
    if modo == 'micro' and dati.get('tipo') in ('cerchio', 'freccia'):
        strati.remove('mani')        # un cerchio o una freccia circondano o indicano le mani, non le coprono
    # giro 3 (Riccardo, 05/11/2026: «la finestra grande è la tela principale», micro-grafiche grandi): nei B-roll le mani del
    # terapista riempiono quasi sempre la finestra grande; una micro-grafica grande (parola, parole, scheda, icona, numero) può
    # passarci sopra: è un avviso da guardare, non un errore. I volti non si coprono mai; con la persona in camera le mani restano
    # da non coprire.
    grande = modo == 'micro' and (dati.get('tipo') in ('parola', 'parole', 'scheda', 'icona', 'numero') or dati.get('modo') == 'libero')
    trov = {}
    mani_broll = []
    corpo = []
    for f in sorted(vis):
        z = next((z for z in zoom if z['f0'] <= f <= z['f1']), None)
        bb = RZ.indietro_box(z, f, bx) if z and (z.get('zona') != 'finestra' or _dentro(bx, RZ.area(z))) else bx
        r0, r1, c0, c1 = RR._celle(bb)
        for k in strati:
            if Z[k][f, r0:r1 + 1, c0:c1 + 1].any():
                if k == 'mani' and grande and (inq_di.get(f) or {}).get('tipo') != 'persona in camera':
                    mani_broll.append(f)
                    continue
                trov.setdefault(k, []).append(f)
        if modo == 'micro':
            corpo.append(Z['persona'][f, r0:r1 + 1, c0:c1 + 1].mean())
        s = inq_di.get(f)
        if s and s.get('schema') and bx[1] < min(w['y'] for w in s['finestre']):
            trov.setdefault('la striscia sopra le finestre (non si usa)', []).append(f)
        if f in tre and s and s.get('schema'):
            for w in s['finestre'][1:]:
                if bx[0] < w['x1'] and bx[2] > w['x'] and bx[1] < w['y1'] and bx[3] > w['y']:
                    trov.setdefault('finestre con le 3D', []).append(f)
        if modo == 'persona' and s and s.get('tipo') != 'persona in camera':
            trov.setdefault(f"inquadratura {s['n']} che non è «persona in camera»", []).append(f)
    for k, fs in trov.items():
        err.append(f"{n}: il riquadro {bx} copre {k} in {len(fs)} fotogrammi (primo f{fs[0]}): spostalo nelle zone libere "
                   "(radiografia/persona-*.jpg)")
    if mani_broll:
        avv.append(f"{n}: il riquadro {bx} passa sopra le mani del B-roll in {len(mani_broll)} fotogrammi (primo f{mani_broll[0]}): "
                   "ammesso per le micro-grafiche grandi (giro 3), da guardare che il gesto resti leggibile")
    if corpo and float(np.mean(corpo)) > 0.35:
        avv.append(f"{n}: la micro-grafica sta per il {np.mean(corpo) * 100:.0f}% sulla sagoma della persona: va bene solo se è voluto")
    # giro 2 della fase 6 (direttore): il testo di una micro esce quando la sua frase detta è finita (+0,6 s), se no resta
    # sopra i sottotitoli successivi (due cose da leggere insieme). Con «via» conta l'uscita del testo
    if modo == 'micro' and g.get('testi_detti'):
        vie = [v for x in g.get('elementi') or [] for v in _vie(x.get('dati') or {})]
        fine_testo = f0 / fps + max(vie) if vie else (f0 + g['frames']) / fps
        fine = max((_fine_frase(R, q.get('detto', ''), f0 / fps) or 0) for q in g['testi_detti'])
        # direttore, giro 2 (m-studio): anche 0,5 s di troppo sono due cose da leggere se nel frattempo arriva il sottotitolo
        # dopo: il limite è il primo sottotitolo che compare dopo la fine della frase
        dopo = [o['fotogrammi_misurati'][0] / fps for o in (R['sottotitoli'].get('righe') or [])
                if o.get('fotogrammi_misurati') and fine and o['fotogrammi_misurati'][0] / fps > fine - 0.05]
        lim = min([fine + 0.6] + dopo) if fine else None
        if lim and fine_testo > lim + 1e-6:
            err.append(f"{n}: il testo resta fino a {fine_testo:.2f} s, la sua frase detta finisce a {fine:.2f} s e il sottotitolo dopo "
                       f"compare a {min(dopo) if dopo else fine + 0.6:.2f} s: farlo uscire entro {lim:.2f} s («via» sull'etichetta o "
                       "grafica più corta); dopo può restare solo un segno senza testo")
    # una cosa da leggere per volta: le scritte già nel video
    sc = [q for q in R.get('scritte_video') or [] if set(range(q['f0'], q['f1'] + 1)) & vis]
    if sc and any(t for x in g.get('elementi') or [] for t in _testi(x)):
        avv.append(f"{n}: mentre c'è la grafica, nel video c'è già la scritta «{sc[0]['t']}» (f{sc[0]['f0']}-{sc[0]['f1']}): "
                   "due cose da leggere insieme?")
    return err, avv


# giro 3 (Riccardo, 05/11/2026): «micro-grafiche grandi e visibili: devono notarsi sul telefono (foglio a 390 px), niente badge
# negli angoli»; «sì alle parole anche con i sottotitoli impressi, purché GRANDI, nella finestra o lontane dalla fascia dei
# sottotitoli; no alle piccole etichette di testo vicino ai sottotitoli»
MICRO_CORPO_MIN = 110            # px a 1080: ~40 px sul telefono a 390 px di larghezza
MICRO_AREA_MIN = 0.15            # il riquadro occupa almeno il 15% della finestra in cui sta (niente badge)
MICRO_LONTANO_SOTTOTITOLI = 150  # px dalla fascia dei sottotitoli, per un testo fuori dalla finestra grande
MICRO_ICONA_MIN = {'grande': 180, 'piccola': 140}
MICRO_CERCHIO_MIN = {'grande': 100, 'piccola': 90}
_CORPO_DEFAULT = {'parola': 88, 'scheda': 112, 'parole': 120, 'numero': 220}


def _corpi_micro(d):
    """i corpi effettivi dei testi di una micro-grafica (con i valori di default del modello)"""
    from .reel_piano_base import corpi
    out = [c for _, c in corpi(d)]
    t = d.get('tipo')
    if t in _CORPO_DEFAULT and 'corpo' not in d and (d.get('testo') or d.get('righe')):
        out.append(_CORPO_DEFAULT[t])
    for o in d.get('righe') or []:
        if 'corpo' not in o and 'corpo' not in d:
            out.append(_CORPO_DEFAULT.get(t, 88))
    e = d.get('etichetta')
    if isinstance(e, dict) and 'corpo' not in e:
        out.append(84)
    return out


def _grandezza(g, R, vis, bx, d, con_testo):
    err, avv = [], []
    n = g['nome']
    fascia = ((R.get('sottotitoli') or {}).get('fascia') or {}).get('vision_y')
    area = (bx[2] - bx[0] + 1) * (bx[3] - bx[1] + 1)
    cxy = ((bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2)
    viste = sorted({s['n']: s for f in vis for s in R['inquadrature'] if s['f0'] <= f <= s['f1']}.values(), key=lambda s: s['f0'])
    for s in viste:
        fin = s.get('finestre') or [] if s.get('schema') else []
        dove = next((i for i, w in enumerate(fin) if w['x'] <= cxy[0] <= w['x1'] and w['y'] <= cxy[1] <= w['y1']), None)
        if fin and dove is None:
            continue                                  # lo dice già il controllo delle finestre
        w = fin[dove] if fin else {'x': SAFE[0], 'y': SAFE[1], 'x1': SAFE[2], 'y1': SAFE[3]}
        tipo_f = 'grande' if (not fin or dove == 0) else 'piccola'
        aw = (w['x1'] - w['x'] + 1) * (w['y1'] - w['y'] + 1)
        if d.get('tipo') == 'cerchio':
            if (d.get('r') or 0) < MICRO_CERCHIO_MIN[tipo_f]:
                err.append(f"{n}: cerchio di raggio {d.get('r')} nella finestra {tipo_f} dell'inquadratura {s['n']}: almeno "
                           f"{MICRO_CERCHIO_MIN[tipo_f]} px, se no sul telefono non si nota")
        elif d.get('tipo') != 'freccia' and area < MICRO_AREA_MIN * aw:
            err.append(f"{n}: il riquadro {bx} è il {area / aw * 100:.0f}% della finestra {tipo_f} dell'inquadratura {s['n']} (almeno "
                       f"{MICRO_AREA_MIN * 100:.0f}%): niente badge piccoli, la micro-grafica deve notarsi sul telefono")
        if d.get('tipo') == 'icona' and (d.get('lato') or 0) < MICRO_ICONA_MIN[tipo_f]:
            err.append(f"{n}: icona di lato {d.get('lato')} nella finestra {tipo_f}: almeno {MICRO_ICONA_MIN[tipo_f]} px")
        if con_testo:
            nella_grande = bool(fin) and dove == 0 and s.get('schema') in ('A', 'B')
            if not nella_grande and fascia:
                dist = max(fascia[0] - bx[3], bx[1] - fascia[1], 0)
                if dist < MICRO_LONTANO_SOTTOTITOLI:
                    err.append(f"{n}: testo a {dist} px dalla fascia dei sottotitoli (y {fascia[0]}–{fascia[1]}) nell'inquadratura {s['n']}, "
                               f"fuori dalla finestra grande: almeno {MICRO_LONTANO_SOTTOTITOLI} px (niente piccole etichette vicino ai sottotitoli)")
    if con_testo:
        cc = _corpi_micro(d)
        if cc and min(cc) < MICRO_CORPO_MIN:
            err.append(f"{n}: testo a corpo {min(cc)}: nelle micro-grafiche almeno {MICRO_CORPO_MIN} (si deve leggere sul telefono a 390 px)")
    return err, avv


def _vie(d):
    out = []
    if isinstance(d, dict):
        for k, v in d.items():
            if k == 'via' and isinstance(v, (int, float)):
                out.append(v)
            else:
                out += _vie(v)
    elif isinstance(d, list):
        for v in d:
            out += _vie(v)
    return out


def _fine_frase(R, detto, t0):
    """quando la voce finisce la frase detta: l'ultima parola della frase, la prima volta dopo t0 - 1 s"""
    pw = [w for w in C.parole_di(detto) if w not in C.SIMBOLI_AMMESSI]
    if not pw:
        return None
    ult = pw[-1]
    for v in R['voce']['parole']:
        if v['a'] >= t0 - 1.0 and C.norm(v['parola']) == ult:
            return v['b']
    return None


def _dentro(b, A):
    return A[0] <= (b[0] + b[2]) / 2 <= A[2] and A[1] <= (b[1] + b[3]) / 2 <= A[3]


def _testi(x):
    from .reel_piano_base import testi
    return [t['testo'] for t in testi(x.get('dati') or {})]


# ---------------------------------------------------------------- ritmo

def eventi(P, R, righe, solo_nostri=False):
    """[(fotogramma, tipo, cosa)] degli eventi visivi del reel con le grafiche del piano (solo_nostri: senza tagli né zoom)"""
    fps = R['fps']
    tutto = set()
    for r in righe:
        if r['modo'] == 'tutto schermo':
            for a, b in r['intervalli']:
                tutto |= set(range(a + 1, b + 1))
    ev = [] if solo_nostri else [(t, 'taglio', 'taglio del video') for t in R['tagli'] if t not in tutto]
    per = {g['nome']: g for g in P['grafiche']}
    for r in righe:
        g = per[r['nome']]
        liv = 'micro' if r['modo'] == 'micro' else 'grande'
        for a, b in r['intervalli']:
            ev.append((a, f'entrata {liv}', r['nome']))
        a0 = r['intervalli'][0][0]
        vis = {f for a, b in r['intervalli'] for f in range(a, b + 1)}
        for t in r['aggancio']:
            f = round(t['t'] * fps)
            if f - a0 > FUSIONE * fps and f in vis:
                ev.append((f, f'testo {liv}', f"{r['nome']}: «{t['testo']}»"))
        for e in g.get('eventi') or []:
            ev.append((g['f0'] + round(e['t'] * fps), f'stato {liv}', f"{r['nome']}: {e.get('cosa', '')}"))
    for z in ([] if solo_nostri else P.get('zoom') or []):
        if 'f0' in z:
            ev.append((z['f0'], 'zoom', z.get('nome', 'zoom')))
    ev.sort()
    fusi = []
    for e in ev:
        if fusi and e[0] - fusi[-1][0] < FUSIONE * fps:
            fusi[-1] = (fusi[-1][0], fusi[-1][1] + '+' + e[1], fusi[-1][2] + ' + ' + e[2])
        else:
            fusi.append(e)
    return fusi


def strato(P, R, righe):
    """il nostro strato grafico (giro 3): copertura ed eventi nostri, senza tagli né zoom. Giro 4: solo le grafiche con un
    contenuto visivo («visivo»); quelle di solo testo e i segni restano fuori dal conto e si elencano"""
    fps, nf = R['fps'], R['fotogrammi']
    fuori = [{'nome': r['nome'], 'catalogo': r['catalogo'], 'contenuto': contenuto(r['catalogo'])[0], 'perche': contenuto(r['catalogo'])[1],
              'tempo': r['tempo']} for r in righe if contenuto(r['catalogo'])[0] != 'visivo']
    righe = [r for r in righe if contenuto(r['catalogo'])[0] == 'visivo']
    vis = set()
    for r in righe:
        for a, b in r['intervalli']:
            vis |= set(range(max(0, a), min(nf - 1, b) + 1))
    # tappa 2 (06/11/2026): le animazioni del montaggio segnate come 3D (anatomia 3D, pastiglie che cadono) sono grafiche del
    # video che non si coprono: escono dal conto. La copertura si misura sul resto del reel e il tempo dentro di loro non
    # conta nelle pause (il ritmo lo tengono loro)
    esc = {f for a, b in ((R.get('animazioni_3d') or {}).get('fotogrammi') or []) for f in range(a, b + 1)}
    vis -= esc
    utili = nf - len(esc)
    ev = [e for e in eventi(P, R, righe, solo_nostri=True)]
    tt = [0.0] + [f / fps for f, _, _ in ev] + [nf / fps]
    pause = [(round(a, 2), round(b, 2), round(b - a - sum(1 for f in esc if a * fps <= f < b * fps) / fps, 2)) for a, b in zip(tt, tt[1:])]
    buchi, a = [], None
    for f in range(nf + 1):
        if f < nf and f not in vis and f not in esc:
            a = f if a is None else a
        elif a is not None:
            buchi.append((round(a / fps, 2), round(f / fps, 2), round((f - a) / fps, 2))); a = None
    out = {'obiettivo': STRATO, 'copertura': round(len(vis) / max(1, utili), 4), 'scoperto_s': round((utili - len(vis)) / fps, 2), 'buchi': buchi,
           'esclusi_3d_s': round(len(esc) / fps, 2),
           'eventi': [{'f': f, 't': round(f / fps, 2), 'tipo': t, 'cosa': c} for f, t, c in ev],
           'ogni_10s': round(len(ev) / (nf / fps) * 10, 2), 'pausa_max_s': max(p[2] for p in pause),
           'pause_lunghe': [p for p in pause if p[2] > STRATO['pausa_max_s'] + 1e-9], 'errori': [], 'informazioni': [], 'non_contano': fuori}
    # 07/11/2026 (Riccardo, «nuova direzione»): tolta la regola della copertura 85% e della novità ogni 2-3 s. Le misure restano
    # come informazione (mappa del ritmo), non sono più errori né avvisi
    if out['copertura'] < STRATO['copertura_min']:
        out['informazioni'].append(f"strato grafico: copertura {out['copertura'] * 100:.1f}% (almeno {STRATO['copertura_min'] * 100:.0f}%), "
                             f"{out['scoperto_s']} s senza nostre grafiche; buchi più lunghi: "
                             + ', '.join(f"{a:.1f}–{b:.1f} s" for a, b, d in sorted(buchi, key=lambda q: -q[2])[:5]))
    for a, b, d in out['pause_lunghe']:
        out['informazioni'].append(f"strato grafico: {d:.1f} s senza una grafica nuova o un cambio ({a:.2f}–{b:.2f} s), massimo {STRATO['pausa_max_s']} s")
    return out


def ritmo(P, R, righe):
    fps, nf = R['fps'], R['fotogrammi']
    ob = obiettivo()
    ev = eventi(P, R, righe)
    dur = nf / fps
    tt = [0.0] + [f / fps for f, _, _ in ev] + [dur]
    pause = [(round(a, 2), round(b, 2), round(b - a, 2)) for a, b in zip(tt, tt[1:])]
    lunghe = [p for p in pause if p[2] > ob['pausa_max_s'] + 1e-9]
    finestre = []
    for s in range(0, int(dur) - 9 if dur >= 10 else 1):
        finestre.append(sum(1 for f, _, _ in ev if s <= f / fps < s + 10))
    out = {'obiettivo': ob, 'eventi': [{'f': f, 't': round(f / fps, 2), 'tipo': t, 'cosa': c} for f, t, c in ev],
           'ogni_10s': round(len(ev) / dur * 10, 2), 'micro': sum(1 for _, t, _ in ev if 'micro' in t),
           'pausa_max_s': max(p[2] for p in pause), 'pause_lunghe': lunghe,
           'finestra_10s_min': min(finestre) if finestre else len(ev), 'avvisi': [], 'errori': []}
    # giro 3: il controllo è sul nostro strato (copertura ed eventi nostri); la misura con i tagli resta un'informazione
    out['strato'] = strato(P, R, righe)
    out['errori'] = list(out['strato']['errori'])
    return out


def confronto(P):
    """lo strato grafico di un altro slug (piano.json «confronto», per esempio la versione pubblicata), per la tavola e il report"""
    q = P.get('confronto')
    if not q:
        return None
    from . import reel_piano_base as AP
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        _, _, inf = AP.controlla(q)
    return dict(inf['ritmo']['strato'], slug=q)


def _md_strato(st, titolo):
    ob = st['obiettivo']
    return [f"- **{titolo}**: copertura **{st['copertura'] * 100:.1f}%** (obiettivo ≥ {ob['copertura_min'] * 100:.0f}%; "
            f"{st['scoperto_s']} s senza nostre grafiche), eventi nostri {len(st['eventi'])} = **{st['ogni_10s']} ogni 10 s**, "
            f"intervallo più lungo fra due eventi nostri **{st['pausa_max_s']} s** (massimo {ob['pausa_max_s']} s)"
            + (f"; oltre il massimo: " + ', '.join(f"{a:.1f}–{b:.1f} s" for a, b, _ in st['pause_lunghe']) if st['pause_lunghe'] else '')
            + (f"; animazioni del montaggio escluse dal conto: {st['esclusi_3d_s']} s" if st.get('esclusi_3d_s') else '')
            + (f"; **non contano** (solo testo o segni): " + ', '.join(f"{q['nome']} (`{q['catalogo']}`, {q['contenuto']})" for q in st.get('non_contano', []))
               if st.get('non_contano') else '')]


def md_ritmo(rt, P, info):
    ob = rt['obiettivo']
    st = rt['strato']
    L = ['', '## Mappa del ritmo', '',
         f"Densità del piano: **{P.get('densita', 'normale')}**. Il controllo misura solo il **nostro strato grafico**: "
         f"{st['obiettivo']['fonte']}.", '']
    L += _md_strato(st, 'questo piano')
    cf = info.get('confronto')
    if cf:
        L += _md_strato(cf, f"confronto: {cf['slug']}")
    L += ['', f"Buchi senza nostre grafiche: " + (', '.join(f"{a:.1f}–{b:.1f} s ({d:.1f})" for a, b, d in st['buchi']) or 'nessuno'), '',
          f"Per informazione, la misura di prima (con i tagli del video base e gli zoom, come nelle reference: obiettivo {ob['ogni_10s']} "
          f"ogni 10 s): {len(rt['eventi'])} eventi, {rt['ogni_10s']} ogni 10 s, pausa più lunga {rt['pausa_max_s']} s.", '',
          '| t (s) | evento nostro | cosa |', '|---|---|---|']
    L += [f"| {e['t']:.2f} | {e['tipo']} | {e['cosa']} |" for e in st['eventi']]
    return L


def _riga_strato(d, X, y, st, nf, fps, etichetta, fnt):
    """una riga della mappa: copertura (verde chiaro), buchi (rosa), eventi nostri (blu grandi, verdi micro), pause lunghe"""
    cop = [(round(a * fps), round(b * fps)) for a, b, _ in st['buchi']]
    d.rectangle([X(0), y, X(nf), y + 34], fill=(200, 238, 210))
    for a, b in cop:
        d.rectangle([X(a), y, X(b), y + 34], fill=(255, 205, 205))
    for a, b, _ in st['pause_lunghe']:
        d.rectangle([X(a * fps), y + 36, X(b * fps), y + 42], fill=(220, 40, 40))
    for e in st['eventi']:
        c = (40, 90, 200) if 'grande' in e['tipo'] else (20, 140, 70)
        d.line([X(e['f']), y + 3, X(e['f']), y + 31], fill=c, width=3)
    d.text((X(0), y + 44), f"{etichetta}: copertura {st['copertura'] * 100:.0f}% (min {st['obiettivo']['copertura_min'] * 100:.0f}%), "
           f"{st['ogni_10s']} eventi nostri ogni 10 s, intervallo max {st['pausa_max_s']} s (max {st['obiettivo']['pausa_max_s']})",
           font=fnt, fill='black')


def striscia_ritmo(R, info, P, wpx=1620):
    """la mappa del ritmo del NOSTRO strato (giro 3): copertura, buchi ed eventi nostri; sotto, se c'è, il confronto (per
    esempio la versione pubblicata)"""
    from PIL import Image, ImageDraw, ImageFont
    f = lambda s: ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', s)
    rt = info['ritmo']
    nf, fps = R['fotogrammi'], R['fps']
    cf = info.get('confronto')
    im = Image.new('RGB', (wpx, 108 + (74 if cf else 0)), (250, 250, 250))
    d = ImageDraw.Draw(im)
    X = lambda fr: 10 + (wpx - 20) * fr / nf
    d.text((10, 4), "NOSTRO STRATO GRAFICO (solo grafiche vere, giro 4) · verde chiaro = una nostra grafica a schermo, rosa = buco · "
           "righe: blu grande, verde micro · rosso sotto = più di 3 s senza novità", font=f(16), fill='black')
    _riga_strato(d, X, 28, rt['strato'], nf, fps, 'QUESTO PIANO', f(17))
    if cf:
        _riga_strato(d, X, 102, cf, nf, fps, f"CONFRONTO {cf['slug']}", f(17))
    return im


# ---------------------------------------------------------------- posto libero

def posto(slug, f0, f1, w, h, n=6):
    """./mve reel-posto <slug> <f0> <f1> <w> <h>: i riquadri w×h liberi in tutti i fotogrammi f0-f1 (niente teste, mani,
    sottotitoli, scritte), dentro la zona sicura; prima quelli dentro la finestra grande e lontani dalla sagoma"""
    from . import reel_radiografia as RR
    R = C.leggi(C.cartella(slug) / 'radiografia.json')
    Z = _zone(R)
    f0, f1, w, h = int(f0), int(f1), int(w), int(h)
    occ = np.zeros(Z['testa'].shape[1:], bool)
    for k in ('testa', 'mani', 'sottotitoli', 'scritte'):
        occ |= Z[k][f0:f1 + 1].any(0)
    pers = Z['persona'][f0:f1 + 1].mean(0)
    s = next((q for q in R['inquadrature'] if q['f0'] <= f0 <= q['f1']), None)
    fin = (s or {}).get('finestra_grande')
    cand = []
    for y in range(SAFE[1], SAFE[3] - h + 2, 10):
        for x in range(SAFE[0], SAFE[2] - w + 2, 10):
            if s and s.get('schema') and y < min(w_['y'] for w_ in s['finestre']):
                continue                      # la striscia sopra le finestre non si usa (CLAUDE.md)
            r0, r1, c0, c1 = RR._celle([x, y, x + w - 1, y + h - 1])
            if occ[r0:r1 + 1, c0:c1 + 1].any():
                continue
            nella = bool(fin and x >= fin['x'] + 20 and y >= fin['y'] + 20 and x + w <= fin['x1'] - 20 and y + h <= fin['y1'] - 20)
            cand.append((not nella, float(pers[r0:r1 + 1, c0:c1 + 1].mean()), abs(y - (fin['y'] + 40 if fin else 400)), x, y))
    cand.sort()
    print(f"{slug} f{f0}-{f1} ({f0 / R['fps']:.2f}-{(f1 + 1) / R['fps']:.2f} s), inquadratura {s and s['n']} ({s and s.get('tipo')}), riquadro {w}x{h}:")
    scelti = []
    for c in cand:
        if all(abs(c[3] - q[3]) > w / 2 or abs(c[4] - q[4]) > h / 2 for q in scelti):
            scelti.append(c)
        if len(scelti) >= n:
            break
    for c in scelti:
        print(f"  box {{\"x\": {c[3]}, \"y\": {c[4]}, \"w\": {w}, \"h\": {h}}}  {'nella finestra grande' if not c[0] else 'fuori dalla finestra'}, sagoma {c[1]:.0%}")
    if not scelti:
        print("  nessun posto libero per tutto il tratto: accorcia il tratto o rimpicciolisci")


# ---------------------------------------------------------------- direttore: il reel intero

def pacco_insieme(slug):
    """fase 6: a densità «piena» il direttore vota anche il reel intero (ritmo, due cose da leggere insieme, troppo o troppo
    poco): fogli a 390 px ogni 0,5 s e la mappa del ritmo -> .lavoro/<slug>/direttore/_insieme/PROMPT.md"""
    from PIL import Image, ImageDraw, ImageFont
    import shutil
    D = C.cartella(slug)
    R = C.leggi(D / 'radiografia.json')
    K = C.leggi(D / 'controlli' / 'controlli.json')
    ctl = C.leggi(D / 'piano' / 'controllo.json')
    fps, nf = R['fps'], R['fotogrammi']
    full = C.AGENTE / K['video']
    d = C.lavoro(slug, 'direttore') / '_insieme'
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    passo = round(fps / 2)
    fs = list(range(0, nf, passo))
    im = C.estrai(full, fs, (390, 693))
    fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20)
    fogli = []
    for k in range(0, len(fs), 24):
        sh = Image.new('RGB', (8 * 396, 3 * 699), 'white')
        for i, f in enumerate(fs[k:k + 24]):
            x = im[f]; dr = ImageDraw.Draw(x); dr.rectangle([0, 0, 110, 26], fill=(255, 230, 0)); dr.text((4, 2), f'{f / fps:.1f}s', font=fnt, fill='black')
            sh.paste(x, ((i % 8) * 396, (i // 8) * 699))
        p = d / f"reel-390px-{fs[k] / fps:04.1f}s.jpg"
        sh.save(p, quality=85); fogli.append(p)
    rt = ctl['info']['ritmo']
    righe = [f"Sei il DIRETTORE ARTISTICO dei reel di Studio Mobilitas (osteopatia). Questa volta voti il REEL INTERO «{slug}» (non una grafica): "
             "il ritmo delle grafiche a densità «piena». Rispondi in italiano.", '',
             "REGOLE (obbligatorie): sola lettura; non installare nulla; niente web né caricamenti; niente git; non usare /tmp. Solo dentro "
             f"{C.AGENTE}. Immagini con Read. Le persone nei B-roll non vanno descritte oltre il necessario.", '',
             "CONTESTO: reel verticale 9:16 già montato (voce, sottotitoli impressi, B-roll). Sopra ci sono infografiche (icone che si "
             "animano, collegamenti, scene, card, disegni Servier) ed eventualmente zoom leggeri dentro la finestra grande. Regole (Riccardo): "
             "copertura e ritmo misurati sotto sono solo informazione (non c'è un minimo: un tratto senza grafiche va bene se c'è un "
             "motivo); i sottotitoli impressi non si toccano mai (fascia identica all'originale o coperta del tutto, mai mezza riga); SOLO TESTO "
             "= BOCCIATO: una parola o una frase da sola, anche grande e animata, non è una grafica e non conta (ogni grafica deve MOSTRARE "
             "il concetto: icona o illustrazione che si anima, diagramma, collegamento, contatore, scena, Servier, card con icona); segnala "
             "ogni tratto in cui a schermo c'è solo testo; persona e B-roll restano visibili il più possibile, grafiche piene solo in 2–3 "
             "momenti forti e brevi, icone grandi con profondità e luce, ogni segno si capisce subito a 390 px; «due cose da leggere» è un "
             "difetto solo quando due testi grandi si fanno concorrenza; niente promesse sanitarie; solo parole dette.", '',
             f"Il nostro strato grafico, misurato: copertura {rt['strato']['copertura'] * 100:.0f}%, {len(rt['strato']['eventi'])} eventi nostri "
             f"({rt['strato']['ogni_10s']} ogni 10 s), intervallo più lungo {rt['strato']['pausa_max_s']} s.", '',
             'DA GUARDARE (Read), un fotogramma ogni 0,5 s a misura di telefono:']
    righe += [f"- {C.rel(p)}" for p in fogli]
    righe += [f"- tavola del piano (mappa del ritmo in alto): {C.rel(D / 'piano' / 'tavola.jpg')} (guarda solo la parte in alto: le due strisce)", '',
              "RESTITUISCI: voto 1–10 (minimo 7) del reel intero; motivo in 4–6 frasi (il reel è davvero pieno e tiene l'attenzione? ci sono "
              "tratti morti o affollamenti? tratti di solo testo? le immagini dicono davvero la cosa detta? due testi grandi in concorrenza? "
              "si legge sul telefono? coerenza fra le grafiche? tono sanitario); "
              "i momenti problematici con il tempo; al massimo 3 correzioni concrete. Severo e preciso; non inventare."]
    (d / 'PROMPT.md').write_text('\n'.join(righe) + '\n', encoding='utf-8')
    return d / 'PROMPT.md'

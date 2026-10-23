"""Fase `grafica`: il piano di tutto cio che va a schermo, sul tempo del montato.

Regola che vale per tutto il file: **niente testo inventato**. Ogni parola a
schermo o viene dalla trascrizione, oppure e un'etichetta strutturale scritta in
regia (MECCANISMO, IN STUDIO, PROSSIMO VIDEO). Le glosse sotto i numeri
riformulano quello che dice, non aggiungono affermazioni cliniche.

Ogni elemento si ancora a una FRASE, non a un tempo: se il montaggio cambia, il
piano si rigenera e resta sincronizzato. Un ancoraggio che non si trova ferma la
fase: va corretto in regia, non ignorato.
"""
import re
import sys
import unicodedata

from ..progetto import Progetto, FPS, ts

GROUP_MAX = 3
GROUP_GAP = 0.45
GROUP_MAXDUR = 2.4


NUMERI = {'uno': '1', 'un': '1', 'una': '1', 'due': '2', 'tre': '3', 'quattro': '4', 'cinque': '5',
          'sei': '6', 'sette': '7', 'otto': '8', 'nove': '9', 'dieci': '10', 'venti': '20',
          'trenta': '30', 'quaranta': '40', 'cinquanta': '50', 'sessanta': '60', 'cento': '100'}


def norm(t):
    """per confrontare: minuscole, senza accenti, cifre e lettere equivalenti
    ("otto" = "8", "caffè" = "caffe", "20%" = "20")"""
    t = unicodedata.normalize('NFD', t.lower())
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    t = re.sub(r"[^\w']", '', t)
    return NUMERI.get(t, t)


def parole(P, regia):
    W = [list(w) for w in P.leggi('parole-montato.json')]
    fixes = [(re.compile(r'\b(?:' + a + r')\b', re.I), b) for a, b in regia.get('correzioni', [])]
    # le correzioni possono coprire piu parole: si applicano sul testo ricucito
    # e si ridistribuiscono sulle parole, tenendo i tempi
    out = []
    i = 0
    while i < len(W):
        done = False
        for n in (3, 2, 1):
            if i + n > len(W):
                continue
            chunk = ' '.join(w[2] for w in W[i:i + n])
            for rx, rep in fixes:
                m = rx.search(chunk)
                if m and m.start() == 0 and m.end() >= len(chunk.rstrip('.,;:!?')):
                    tail = chunk[m.end():]
                    new = rx.sub(rep, chunk, count=1)
                    nw = new.split()
                    a, b = W[i][0], W[i + n - 1][1]
                    for k, t in enumerate(nw):
                        out.append([a + (b - a) * k / len(nw), a + (b - a) * (k + 1) / len(nw), t])
                    i += n
                    done = True
                    break
            if done:
                break
        if not done:
            out.append(W[i])
            i += 1
    return [{'t': t, 's': round(s, 3), 'e': round(e, 3)} for s, e, t in out]


def trova(W, frase, dopo=0.0):
    """indice della prima parola della frase, dopo il tempo dato"""
    target = [norm(x) for x in frase.split() if norm(x)]
    n = len(target)
    for i in range(len(W) - n + 1):
        if W[i]['s'] < dopo:
            continue
        if [norm(W[j]['t']) for j in range(i, i + n)] == target:
            return i
    return None


def ancora(W, frase, dopo=0.0, cosa=''):
    i = trova(W, frase, dopo)
    if i is None:
        sys.exit(f"ancoraggio non trovato ({cosa}): «{frase}» — correggi la frase in regia.json "
                 f"(cerca in data/parole-montato.json come e stata trascritta)")
    return i


def fine_frase(W, i, max_dur=6.0):
    """fine della frase che contiene la parola i: punteggiatura o pausa"""
    t0 = W[i]['s']
    for j in range(i, len(W)):
        if re.search(r'[.!?;:]$', W[j]['t']) or (j + 1 < len(W) and W[j + 1]['s'] - W[j]['e'] > 0.30):
            return j
        if W[j]['e'] - t0 > max_dur:
            return j
    return len(W) - 1


def inizio_frase(W, i, max_back=4.0):
    for j in range(i, 0, -1):
        if W[j]['s'] - W[j - 1]['e'] > 0.25 or re.search(r'[.!?;:]$', W[j - 1]['t']):
            return j
        if W[i]['s'] - W[j]['s'] > max_back:
            return j
    return 0


def gruppi(W, nascosti):
    out, cur = [], []
    for w in W:
        if any(a <= w['s'] < b for a, b in nascosti):
            if cur:
                out.append(cur)
                cur = []
            continue
        if cur:
            gap = w['s'] - cur[-1]['e']
            dur = cur[-1]['e'] - cur[0]['s']
            ends = re.search(r'[.!?]$', cur[-1]['t'])
            if len(cur) >= GROUP_MAX or gap > GROUP_GAP or dur > GROUP_MAXDUR or ends:
                out.append(cur)
                cur = []
        cur.append(w)
    if cur:
        out.append(cur)
    res = []
    for i, g in enumerate(out):
        s = g[0]['s']
        e = g[-1]['e'] + 0.12
        if i + 1 < len(out):
            e = min(e, out[i + 1][0]['s'] - 0.01)
        res.append({'s': round(s, 3), 'e': round(max(e, s + 0.30), 3), 'words': g})
    return res


def piano(slug):
    P = Progetto(slug)
    R = P.regia()
    E = P.leggi('edl.json')
    dur = E['durata']
    W = parole(P, R)

    cards = []
    for c in R.get('card', []):
        i = ancora(W, c['frase'], cosa='card')
        s = round(W[i]['s'] - 0.25, 3)
        cards.append({'s': s, 'e': round(s + c.get('durata', 4.2), 3), 'eyebrow': c['eyebrow'],
                      'value': c['valore'], 'unit': c['unita'], 'sub': c['glossa'], 'frase': c['frase']})

    capitoli, dopo = [], 0.0
    for c in R.get('capitoli', []):
        i = ancora(W, c['frase'], dopo, 'capitolo')
        if c.get('dietro'):
            # il titolo dietro entra con la frase che lo pronuncia e resta mentre la dice
            j1 = fine_frase(W, i, max_dur=3.4)
            s = round(W[i]['s'] - 0.08, 3)
            e = round(min(max(W[j1]['e'] + 0.55, s + 2.6), s + 4.0), 3)
        else:
            # la scheda piena cade sulla pausa prima della frase, poi si alza
            s = round(W[i]['s'] - 1.30, 3)
            e = round(s + 1.75, 3)
        capitoli.append({'s': s, 'e': e, 'eyebrow': c['eyebrow'], 'l1': c['l1'], 'l2': c['l2'],
                         'dietro': bool(c.get('dietro')), 'titolo_youtube': c.get('titolo_youtube'),
                         'frase': c['frase']})
        dopo = e + 10

    # una card non entra mentre c'e un titolo: aspetta che esca
    for c in cards:
        for t in capitoli:
            if t['s'] - 0.2 < c['s'] < t['e'] + 0.15:
                shift = t['e'] + 0.15 - c['s']
                c['s'], c['e'] = round(c['s'] + shift, 3), round(c['e'] + shift, 3)
                print(f"  card {c['eyebrow']} spostata di {shift:.2f}s: entrava sul titolo {t['l1']}")

    enfasi = []
    for c in R.get('enfasi', []):
        i = ancora(W, c['frase'], cosa='enfasi')
        j = fine_frase(W, i, max_dur=c.get('max', 5.0))
        enfasi.append({'s': round(W[i]['s'] - 0.05, 3), 'e': round(W[j]['e'] + 0.15, 3),
                       'livello': c.get('livello', 'stretto'), 'frase': c['frase']})

    ap = R.get('apertura')
    opening = dict(ap, s=0.35, e=5.6) if ap else None
    chip = None
    if R.get('chip'):
        c = R['chip']
        s = W[ancora(W, c['frase'], cosa='chip')]['s'] if c.get('frase') else 30.0
        chip = {'s': round(s, 3), 'e': round(s + 6.0, 3), 'name': c['name'], 'role': c['role']}
    closing = None
    if R.get('chiusura'):
        # la scheda piena non copre l'ultima frase: parte dopo l'ultima parola.
        # Serve una coda muta in fondo al girato (l'ultimo taglio `da` piu tardi)
        s0 = max(W[-1]['e'] + 0.35, dur - 5.5)
        if dur - s0 < 3.5:
            print(f"  ! la chiusura avrebbe solo {dur - s0:.1f}s dopo l'ultima parola: sposta l'ultimo "
                  f"taglio di regia ({'da'}) di {3.5 - (dur - s0) + 1.0:.1f}s piu avanti, sulla coda muta")
            s0 = min(s0, dur - 1.5)
        closing = dict(R['chiusura'], s=round(s0, 3), e=round(dur, 3))

    finale = None
    if R.get('capitolo_finale'):
        cf = R['capitolo_finale']
        i = ancora(W, cf['frase'], dopo=dur * 0.6, cosa='capitolo finale')
        finale = {'s': W[i]['s'], 'titolo': cf['titolo']}

    nascosti = [(c['s'] + 0.1, c['e'] - 0.1) for c in capitoli]
    if closing:
        nascosti.append((closing['s'] + 0.3, closing['e']))
    caps = gruppi(W, nascosti)

    from ..progetto import impronta, REGIA_DI
    plan = {'regia': impronta(R, REGIA_DI['grafica.json']), 'fps': FPS, 'duration': round(dur, 6), 'frames': E['frame'],
            'opening': opening, 'chip': chip, 'closing': closing, 'cards': cards,
            'capitoli': capitoli, 'enfasi': enfasi, 'finale': finale,
            'capitolo_iniziale': R.get('capitolo_iniziale', 'Introduzione'),
            'captions': caps}
    P.scrivi('grafica.json', plan)
    print(f"durata {dur:.2f}s, {len(caps)} gruppi di sottotitolo")
    for c in cards:
        print(f"   card    {ts(c['s']):>9}  {c['value']}{c['unit']:<4} {c['eyebrow']}")
    for c in capitoli:
        print(f"   {'dietro' if c['dietro'] else 'stacco'}  {ts(c['s']):>9}  {c['l1']} {c['l2']}  ({c['e']-c['s']:.1f}s)")
    for c in enfasi:
        print(f"   enfasi  {ts(c['s']):>9}  «{c['frase']}» ({c['e']-c['s']:.1f}s)")
    print("-> data/grafica.json (i lati delle card li decide `inquadra`, sul volto)")

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


VOCI = ('voci', 'zone', 'etichette')


def card(W, c):
    """una card di regia -> elemento del piano. Le voci con `frase` prendono `t`,
    i secondi dall'ingresso della card in cui lei la dice"""
    tipo = c.get('tipo', 'numero')
    i = ancora(W, c['frase'], cosa=f'card {tipo}')
    s = round(W[i]['s'] - 0.25, 3)
    out = {k: v for k, v in c.items() if k not in ('valore', 'unita', 'glossa')}
    out.update({'tipo': tipo, 's': s, 'eyebrow': c.get('eyebrow', '')})
    if tipo == 'numero':
        out.update({'value': c['valore'], 'unit': c['unita'], 'sub': c['glossa']})
    fine = 0.0
    for k in VOCI:
        voci = []
        for v in c.get(k, []):
            v = dict(v)
            if v.get('frase'):
                j = ancora(W, v['frase'], dopo=W[i]['s'] - 1.5, cosa=f"{tipo} «{v.get('testo', v['frase'])}»")
                v['t'] = round(W[j]['s'] - s, 3)
                fine = max(fine, v['t'])
            voci.append(v)
        if voci:
            out[k] = voci
    if c.get('annulla'):
        j = ancora(W, c['annulla'], dopo=W[i]['s'], cosa=f'{tipo} annulla')
        out['annulla_t'] = round(W[j]['s'] - s, 3)
        fine = max(fine, out['annulla_t'] + 0.8)
    if tipo == 'citazione':
        # le parole della frase, una per una: il karaoke dentro le virgolette
        n = len(c['testo'].split())
        j = ancora(W, ' '.join(c['testo'].split()[:4]), dopo=W[i]['s'] - 1.5, cosa='citazione')
        if [norm(w['t']) for w in W[j:j + n]] != [norm(x) for x in c['testo'].split()]:
            sys.exit(f"citazione: «{c['testo']}» non e la frase come la dice "
                     f"(trascritta: «{' '.join(w['t'] for w in W[j:j + n])}»)")
        out['parole_t'] = [round(w['s'] - s, 3) for w in W[j:j + n]]
        fine = max(fine, out['parole_t'][-1])
    dur = c.get('durata') or max(4.2, fine + c.get('coda', 2.6))
    out['e'] = round(s + dur, 3)
    return out


FRAMEWORK = ('passi', 'ciclo', 'matrice', 'piramide')
# il volto resta visibile: la scena puo durare di piu
DURATA_MAX = {'dietro': 9.0, 'finestra': 30.0, 'davanti': 24.0}


def richiamo(W, c, ids):
    """il framework che torna: stesse voci della scena `di`, gia tutte a schermo,
    acceso il pezzo `acceso` (da 1). Breve, e di default con lei in finestra."""
    if c.get('di') not in ids:
        sys.exit(f"richiamo: nessuna scena con id «{c.get('di')}» (scene con id: {', '.join(ids) or 'nessuna'})")
    rif = ids[c['di']]
    n = len(rif.get('voci', []))
    if not 1 <= c.get('acceso', 0) <= n:
        sys.exit(f"richiamo di «{c['di']}»: `acceso` va da 1 a {n}")
    i = ancora(W, c['frase'], cosa=f"richiamo {c['di']}")
    s = round(W[i]['s'] - 0.30, 3)
    out = {k: v for k, v in rif.items() if k in ('tipo', 'eyebrow', 'titolo', 'centro', 'asse_x', 'asse_y')}
    out['voci'] = [{k: v for k, v in x.items() if k in ('testo', 'icona', 'acceso')} for x in rif['voci']]
    out.update({'richiamo': c['acceso'], 'di': c['di'], 'frase': c['frase'], 's': s,
                'e': round(s + c.get('durata', 3.2), 3), 'lei': c.get('lei', 'finestra'),
                'lato': c.get('lato', rif.get('lato', 'destra')), 'ingresso': c.get('ingresso')})
    return out


def scena(W, c):
    """una scena a tutto schermo: entra 0,45 s prima della frase (la zoomata nel
    video), esce dopo l'ultima parola o voce"""
    tipo = c.get('tipo', 'parole')
    i = ancora(W, c['frase'], cosa=f'scena {tipo}')
    out = dict(c, tipo=tipo)
    s = round(W[i]['s'] - 0.45, 3)
    if c.get('lei') == 'finestra':
        s = round(W[i]['s'] - 0.62, 3)       # il quadro si stringe nella finestra
    fine = W[i]['e']
    if tipo == 'parole':
        parole_ = c['testo'].split()
        n = len(parole_)
        j = ancora(W, ' '.join(parole_[:4]), dopo=W[i]['s'] - 1.5, cosa='scena parole')
        if [norm(w['t']) for w in W[j:j + n]] != [norm(x) for x in parole_]:
            sys.exit(f"scena: «{c['testo']}» non e la frase come la dice "
                     f"(trascritta: «{' '.join(w['t'] for w in W[j:j + n])}»)")
        s = round(max(0.0, W[j]['s'] - 0.45), 3)
        out['parole_t'] = [round(w['s'] - s, 3) for w in W[j:j + n]]
        fine = W[j + n - 1]['e']
    voci = []
    for v in c.get('voci', []):
        v = dict(v)
        if v.get('frase'):
            k = ancora(W, v['frase'], dopo=W[i]['s'] - 1.5, cosa=f"scena {tipo} «{v.get('testo', v['frase'])}»")
            v['t'] = round(W[k]['s'] - s, 3)
            # nei framework la voce resta finche finisce di dirla
            fine = max(fine, W[fine_frase(W, k, 3.5)]['e'] if tipo in FRAMEWORK else W[k]['e'])
        voci.append(v)
    if voci:
        out['voci'] = voci
    if c.get('chiude'):
        k = ancora(W, c['chiude'], dopo=W[i]['s'], cosa=f'scena {tipo} chiude')
        out['chiude_t'] = round(W[k]['s'] - s, 3)
        fine = max(fine, W[k]['e'] + 1.2)
    if tipo in FRAMEWORK and not voci:
        sys.exit(f"scena {tipo} a {ts(s)}: servono le `voci`, ognuna con la sua `frase`")
    out['s'] = s
    out['e'] = round(c['durata'] + s if c.get('durata') else max(fine + c.get('coda', 0.8), s + 3.5), 3)
    lim = DURATA_MAX.get(c.get('lei', 'dietro'), 9.0)
    if out['e'] - s > lim:
        print(f"  ! scena a {ts(s)} lunga {out['e'] - s:.1f}s: con lei {c.get('lei', 'dietro')} "
              f"oltre {lim - 1:.0f} s sparisce troppo a lungo")
    return out


def segno(W, c):
    """un segno sopra il girato. `parola`: `testo` dev'essere detto nella `frase`,
    e la parola sbatte quando lo dice; gli altri entrano sulla `frase`"""
    tipo = c.get('tipo', 'parola')
    i = ancora(W, c['frase'], cosa=f'segno {tipo}')
    out = dict(c, tipo=tipo)
    if tipo == 'parola':
        j = trova(W, c['testo'], dopo=W[i]['s'] - 0.05)
        if j is None or W[j]['s'] - W[i]['s'] > 6:
            sys.exit(f"segno parola: «{c['testo']}» non e detto nella frase «{c['frase']}»")
        out['s'] = round(W[j]['s'] - 0.12, 3)
        out['e'] = round(out['s'] + c.get('durata', 1.9), 3)
    else:
        if not c.get('dove'):
            sys.exit(f"segno {tipo} a «{c['frase']}»: manca `dove` (coordinate 0-1 della sorgente, ./mve griglia)")
        out['s'] = round(W[i]['s'] - 0.05, 3)
        out['e'] = round(out['s'] + c.get('durata', 2.6), 3)
    return out


def piano(slug):
    P = Progetto(slug)
    R = P.regia()
    E = P.leggi('edl.json')
    dur = E['durata']
    W = parole(P, R)

    cards = []
    for c in R.get('card', []):
        cards.append(card(W, c))

    scene, ids = [], {}
    for c in R.get('scene', []):
        if c.get('tipo') == 'richiamo':
            continue
        x = scena(W, c)
        scene.append(x)
        if c.get('id'):
            ids[c['id']] = x
    scene += [richiamo(W, c, ids) for c in R.get('scene', []) if c.get('tipo') == 'richiamo']
    scene.sort(key=lambda c: c['s'])
    for a_, b_ in zip(scene, scene[1:]):
        if b_['s'] < a_['e']:
            sys.exit(f"due scene si sovrappongono a {ts(b_['s'])}: spostane una")
        # il richiamo e breve e torna apposta: non conta nella distanza fra scene
        if b_['s'] - a_['e'] < 15 and not (a_.get('richiamo') or b_.get('richiamo')):
            print(f"  ! due scene a {b_['s'] - a_['e']:.0f}s l'una dall'altra ({ts(a_['s'])}, {ts(b_['s'])}): "
                  f"almeno 15 s, o il video diventa una presentazione")

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

    cards.sort(key=lambda c: c['s'])
    for a_, b_ in zip(cards, cards[1:]):
        if b_['s'] < a_['e'] and not (a_.get('lato') and b_.get('lato') and a_['lato'] != b_['lato']):
            print(f"  ! card a {ts(b_['s'])} entra mentre c'e ancora quella a {ts(a_['s'])}: "
                  f"`inquadra` le mette su lati opposti, se il volto lo permette")

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
    # durante la citazione e la scena di parole le parole sono gia a schermo
    nascosti += [(c['s'] + 0.2, c['e']) for c in cards if c['tipo'] == 'citazione']
    nascosti += [(c['s'] + (0 if c['s'] < 0.05 else 0.3), c['e'] - 0.2) for c in scene if c['tipo'] == 'parole']
    for sc in scene:
        for c in cards:
            if c['s'] < sc['e'] and sc['s'] < c['e']:
                print(f"  ! la card {c['eyebrow'] or c['tipo']} a {ts(c['s'])} e sotto la scena a {ts(sc['s'])}: non si vedra")
        for c in capitoli:
            if c['s'] < sc['e'] and sc['s'] < c['e']:
                sys.exit(f"scena a {ts(sc['s'])} sopra il titolo «{c['l1']}»: spostala")
    if closing:
        nascosti.append((closing['s'] + 0.3, closing['e']))
    caps = gruppi(W, nascosti)

    segni = sorted((segno(W, c) for c in R.get('segni', [])), key=lambda c: c['s'])
    for g in segni:
        for x in scene + capitoli:
            if g['s'] < x['e'] and x['s'] < g['e']:
                sys.exit(f"segno {g['tipo']} a {ts(g['s'])} sotto una scena o un titolo: spostalo")
        for c in cards:
            if g['tipo'] == 'parola' and g['s'] < c['e'] and c['s'] < g['e']:
                print(f"  ! parola «{g['testo']}» a {ts(g['s'])} insieme alla card {c['eyebrow'] or c['tipo']}: "
                      f"`inquadra` le mette su lati opposti, ma due cose accanto a lei sono troppe")

    from ..progetto import impronta, REGIA_DI
    plan = {'regia': impronta(R, REGIA_DI['grafica.json']), 'fps': FPS, 'duration': round(dur, 6), 'frames': E['frame'],
            'opening': opening, 'chip': chip, 'closing': closing, 'cards': cards,
            'capitoli': capitoli, 'enfasi': enfasi, 'finale': finale, 'scene': scene, 'segni': segni,
            'finitura': R.get('finitura', {}),
            'capitolo_iniziale': R.get('capitolo_iniziale', 'Introduzione'),
            'captions': caps}
    P.scrivi('grafica.json', plan)
    print(f"durata {dur:.2f}s, {len(caps)} gruppi di sottotitolo")
    for c in cards:
        cosa = f"{c['value']}{c['unit']}" if c['tipo'] == 'numero' else c['tipo']
        print(f"   card    {ts(c['s']):>9}  {cosa:<10} {c['eyebrow']}  ({c['e']-c['s']:.1f}s)")
    for c in capitoli:
        print(f"   {'dietro' if c['dietro'] else 'stacco'}  {ts(c['s']):>9}  {c['l1']} {c['l2']}  ({c['e']-c['s']:.1f}s)")
    for c in scene:
        cosa = f"richiamo {c['di']} #{c['richiamo']}" if c.get('richiamo') else c['tipo']
        print(f"   SCENA   {ts(c['s']):>9}  {cosa:<10} «{c.get('testo') or c.get('valore') or c['frase']}» "
              f"lei {c.get('lei', 'dietro')} ({c['e']-c['s']:.1f}s)")
    for c in segni:
        print(f"   segno   {ts(c['s']):>9}  {c['tipo']:<10} «{c.get('testo', '')}»")
    for c in enfasi:
        print(f"   enfasi  {ts(c['s']):>9}  «{c['frase']}» ({c['e']-c['s']:.1f}s)")
    print("-> data/grafica.json (i lati delle card li decide `inquadra`, sul volto)")

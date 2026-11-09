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

from ..progetto import Progetto, ts

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
                    if len(nw) == n:
                        # stesse parole, altra grafia o punteggiatura: ognuna tiene il suo tempo
                        # (tappa 3: «vetro partiamo» -> «vetro. Partiamo» spostava le ancore di 0,2 s)
                        out += [[W[i + k][0], W[i + k][1], t] for k, t in enumerate(nw)]
                    else:
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


# ---------------------------------------------------------------- v2: elementi nuovi
# Le chiavi di testo che vanno a schermo, in qualsiasi elemento: il QC le
# confronta con la trascrizione (niente testo inventato).
CHIAVI_TESTO = ('testo', 'titolo', 'etichetta', 'prefisso', 'domanda', 'risposta', 'nome', 'ruolo')
OPPOSTO = {'sx': 'dx', 'dx': 'sx'}


def _t(W, frase, dopo, cosa):
    return W[ancora(W, frase, dopo, cosa)]['s']


def _intervallo(W, v, dur, cosa, anticipo=0.12, coda=0.35):
    """[s, e] di un elemento: parte sulla sua frase, finisce sulla frase `fino`
    (esclusa), dopo `durata` secondi, oppure a fine frase"""
    i = ancora(W, v['frase'], v.get('dopo', 0.0), cosa)
    s = W[i]['s'] - v.get('anticipo', anticipo)
    if v.get('fino'):
        e = _t(W, v['fino'], W[i]['s'] + 0.01, cosa + ' (fino)') - 0.08
    elif v.get('fino') is None and 'fino' in v:
        e = dur                                       # fino in fondo
    elif v.get('durata'):
        e = s + v['durata']
    else:
        e = W[fine_frase(W, i, max_dur=v.get('max', 8.0))]['e'] + coda
    return round(max(0.0, s), 3), round(min(dur, e), 3)


def _risolvi(x, W, s, cosa):
    """dentro un elemento: ogni dizionario con 'frase' riceve 't', il suo istante
    relativo all'inizio dell'elemento (le voci di un'etichetta, i passi di una lista)"""
    if isinstance(x, list):
        return [_risolvi(v, W, s, cosa) for v in x]
    if isinstance(x, dict):
        y = {k: _risolvi(v, W, s, cosa) for k, v in x.items()}
        if 'frase' in x:
            y['t'] = round(_t(W, x['frase'], s - 0.5, cosa) - s, 3)
        return y
    return x


def testi_a_schermo(x):
    """tutte le stringhe che un elemento mette a schermo"""
    out = []
    if isinstance(x, list):
        for v in x:
            out += testi_a_schermo(v)
    elif isinstance(x, dict):
        for k, v in x.items():
            if k in CHIAVI_TESTO and isinstance(v, str) and v.strip():
                out.append(v)
            elif isinstance(v, (list, dict)):
                out += testi_a_schermo(v)
    return out


def _frasi_chiave(W, R, dur):
    """sottotitoli variante B: solo le frasi chiave, accanto alla persona spostata"""
    out = []
    for k, v in enumerate(R.get('frasi_chiave', [])):
        s, e = _intervallo(W, v, dur, 'frase chiave', anticipo=0.08)
        i = ancora(W, v['frase'], v.get('dopo', 0.0), 'frase chiave')
        testo = v.get('testo') or ' '.join(w['t'] for w in W[i:fine_frase(W, i) + 1])
        lato = v.get('lato', 'sx')
        out.append({'id': f"fc{k + 1:02d}", 's': s, 'e': e, 'testo': testo, 'chiave': v.get('chiave', ''),
                    'lato': lato, 'persona': v.get('persona', OPPOSTO[lato]), 'freccia': bool(v.get('freccia')),
                    'frase': v['frase']})
    return out


def _inserti(W, R, dur):
    out = []
    for k, v in enumerate(R.get('inserti', [])):
        cosa = f"inserto {v['modello']}"
        s, e = _intervallo(W, v, dur, cosa)
        dati = {kk: _risolvi(vv, W, s, cosa) for kk, vv in v.items()
                if kk not in ('modello', 'frase', 'fino', 'durata', 'persona', 'persona_fino', 'dopo', 'anticipo')}
        x = {'id': f"{k + 1:02d}-{v['modello']}", 'modello': v['modello'], 's': s, 'e': e,
             'frase': v['frase'], 'dati': dati, 'testi': testi_a_schermo(dati)}
        if v.get('persona'):
            pe = _t(W, v['persona_fino'], W[ancora(W, v['frase'], v.get('dopo', 0.0), cosa)]['s'], cosa) - 0.08 \
                if v.get('persona_fino') else e
            x['persona'] = {'lato': v['persona'], 's': s, 'e': round(min(e, pe), 3)}
        out.append(x)
    return out


def _broll(W, R, dur):
    """intervalli di B-roll: la persona non si vede, al suo posto clip della libreria
    (una a tutto schermo, due affiancate, o una sequenza che divide l'intervallo)"""
    from ..libreria import utilizzabili
    import unicodedata
    nfc = lambda t: unicodedata.normalize('NFC', t)      # i nomi di macOS sono in NFD ("Farò")
    usabili = {nfc(c['file']): c for c in utilizzabili(voto_min=1)}
    out = []
    for k, v in enumerate(R.get('broll', [])):
        s, e = _intervallo(W, v, dur, 'broll', anticipo=0.04)
        clip = [nfc(c) for c in (v['clip'] if isinstance(v['clip'], list) else [v['clip']])]
        for c in clip:
            if c not in usabili:
                sys.exit(f"broll: {c} non e fra le clip utilizzabili della libreria (esclusa, senza "
                         f"descrizione o inesistente): scegline un'altra con libreria.utilizzabili()")
        lay = v.get('layout', 'pieno')
        tratti = v.get('tratto') or [usabili[c]['movimento']['stabile']['s'] for c in clip]
        if lay == 'sequenza':
            passo = (e - s) / len(clip)
            for j, c in enumerate(clip):
                out.append({'id': f"b{k + 1:02d}{chr(97 + j)}", 's': round(s + j * passo, 3),
                            'e': round(s + (j + 1) * passo, 3), 'layout': 'pieno',
                            'clip': [{'file': usabili[c]['file'], 'src_in': tratti[j], 'fps': usabili[c]['fps'],
                                      'durata': usabili[c]['durata']}]})
        else:
            out.append({'id': f"b{k + 1:02d}", 's': s, 'e': e, 'layout': lay,
                        'clip': [{'file': usabili[c]['file'], 'src_in': t, 'fps': usabili[c]['fps'], 'durata': usabili[c]['durata']}
                                 for c, t in zip(clip, tratti)]})
    return out


# un pannello che esce e subito rientra sfarfalla: fra due elementi di fila (meno
# di CONTIGUI secondi, anche sovrapposti) il passaggio si risolve qui, una volta
# per tutti i renderer (frasi chiave Pillow e inserti HyperFrames)
CONTIGUI = 0.35
STACCO = 0.28           # fotogrammi puliti fra uno stacco d'inquadratura e un pannello dal lato opposto
SENZA_PANNELLO_FINALE = ('prodotto',)    # il pannello della scheda esce prima (si riduce in etichetta)


def _continuita(chiave, inserti):
    """stesso lato: il pannello resta, cambia il testo (esce/entra False, nessuna
    sovrapposizione). Inserto a tutto schermo (senza lato): si entra e si esce a
    taglio netto. Lati opposti: il pannello nuovo aspetta STACCO dopo lo stacco."""
    el = [('fc', c, c['lato']) for c in chiave] + \
         [('ins', x, x['dati'].get('lato')) for x in inserti]
    el.sort(key=lambda v: v[1]['s'])
    passaggi = []

    def flag(tipo, x, k, v):
        (x if tipo == 'fc' else x['dati'])[k] = v

    for (ta, a, la), (tb, b, lb) in zip(el, el[1:]):
        gap = b['s'] - a['e']
        if not (-1.0 < gap < CONTIGUI):
            continue
        ma, mb = a.get('modello'), b.get('modello')
        if la and lb and la == lb:
            if ma in SENZA_PANNELLO_FINALE or ma == 'chiusura':
                continue
            a['e'] = b['s']
            flag(ta, a, 'esce', False)
            flag(tb, b, 'entra', False)
            passaggi.append(f"{a['id']}->{b['id']} stesso pannello")
        elif not la or not lb:
            a['e'] = b['s']
            if not lb:
                flag(ta, a, 'esce', False)
                flag(tb, b, 'entra', False)
            else:
                flag(ta, a, 'esce', False)
            passaggi.append(f"{a['id']}->{b['id']} taglio netto")
        elif tb == 'fc' and gap < STACCO:
            b['ritardo'] = round(STACCO - max(gap, 0.0), 3)
            passaggi.append(f"{a['id']}->{b['id']} lato opposto, entra {b['ritardo']}s dopo lo stacco")
        a['e'] = round(a['e'], 3)
    for x in inserti:
        if x.get('persona'):
            x['persona']['e'] = round(min(x['persona']['e'], x['e']), 3)
    return passaggi


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
        e = (_t(W, c['fino'], s + 0.01, 'chip (fino)') - 0.10) if c.get('fino') else s + c.get('durata', 6.0)
        chip = {'s': round(s, 3), 'e': round(e, 3), 'name': c['name'], 'role': c['role'],
                'stile': c.get('stile', 'v1')}
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
    chiave = _frasi_chiave(W, R, dur)
    inserti = _inserti(W, R, dur)
    broll = _broll(W, R, dur)
    # una frase chiave lascia il posto all'inserto che entra dopo di lei
    for c in chiave:
        dopo = [x['s'] for x in inserti if c['s'] < x['s'] < c['e']]
        if dopo:
            c['e'] = round(min(dopo) - 0.05, 3)
    for p in _continuita(chiave, inserti):
        print(f"  continuita: {p}")
    # dove la persona va spostata di lato: decide `inquadra`
    persona = [{'s': x['s'], 'e': x['e'], 'lato': x['persona'], 'da': x['id']} for x in chiave]
    persona += [dict(x['persona'], da=x['id']) for x in inserti if x.get('persona')]
    persona.sort(key=lambda x: x['s'])
    # variante B: niente sottotitoli parola per parola (le frasi chiave li sostituiscono;
    # l'SRT completo esce comunque per YouTube)
    caps = [] if R.get('sottotitoli') == 'chiave' else gruppi(W, nascosti)

    from ..progetto import impronta, REGIA_DI
    plan = {'regia': impronta(R, REGIA_DI['grafica.json']), 'fps': P.fps, 'duration': round(dur, 6), 'frames': E['frame'],
            'opening': opening, 'chip': chip, 'closing': closing, 'cards': cards,
            'capitoli': capitoli, 'enfasi': enfasi, 'finale': finale,
            'capitolo_iniziale': R.get('capitolo_iniziale', 'Introduzione'),
            'sottotitoli': R.get('sottotitoli', 'parole'), 'frasi_chiave': chiave,
            # barra d'avanzamento: si dei video lunghi, no nei mid-roll (`"barra_avanzamento": false`)
            'barra': R.get('barra_avanzamento', True), 'inserti': inserti,
            'broll': broll, 'persona': persona, 'materiali_vietati': R.get('materiali_vietati', []),
            'etichette_strutturali': R.get('etichette_strutturali', []), 'captions': caps}
    P.scrivi('grafica.json', plan)
    print(f"durata {dur:.2f}s, {len(caps)} gruppi di sottotitolo")
    for c in cards:
        print(f"   card    {ts(c['s']):>9}  {c['value']}{c['unit']:<4} {c['eyebrow']}")
    for c in capitoli:
        print(f"   {'dietro' if c['dietro'] else 'stacco'}  {ts(c['s']):>9}  {c['l1']} {c['l2']}  ({c['e']-c['s']:.1f}s)")
    for c in enfasi:
        print(f"   enfasi  {ts(c['s']):>9}  «{c['frase']}» ({c['e']-c['s']:.1f}s)")
    for c in chiave:
        print(f"   chiave  {ts(c['s']):>9}  «{c['testo']}» ({c['e']-c['s']:.1f}s, testo a {c['lato']})")
    for x in inserti:
        print(f"   inserto {ts(x['s']):>9}  {x['modello']:<10} ({x['e']-x['s']:.1f}s)"
              + (f" persona a {x['persona']['lato']}" if x.get('persona') else ''))
    for b in broll:
        print(f"   broll   {ts(b['s']):>9}  {b['layout']:<10} ({b['e']-b['s']:.1f}s) "
              + ' + '.join(c['file'].split('/')[-1] for c in b['clip']))
    print("-> data/grafica.json (i lati delle card li decide `inquadra`, sul volto)")

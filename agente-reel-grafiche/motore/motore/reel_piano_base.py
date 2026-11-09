"""Tappa 2 dell'agente reel-grafiche: il piano delle grafiche (fase 4, 04/11/2026).

L'agente scrive `videos/<slug>/piano.json` seguendo la skill `mobilitas-reel`. È l'unico file che scrive a
mano. `./mve reel-piano <slug>` lo controlla contro le regole di CLAUDE.md e la radiografia, poi fa la tavola
visiva per Riccardo (`piano/tavola.jpg`) e il riepilogo (`piano/piano.md`). **Qui si ferma**: si va avanti solo
dopo `./mve reel-approva <slug> piano`, che lega l'ok di Riccardo all'md5 del piano che ha visto.

Forma del piano (i tempi dentro `elementi` sono in secondi dall'inizio della pagina, cioè dal fotogramma f0):

    {"slug": "...", "grafiche": [
       {"nome": "equazione", "catalogo": "equazione-finestra", "modo": "finestra" | "tutto schermo",
        "f0": 376, "frames": 165, "voce": "«...» (12,57-18,00 s)", "perche": "...",
        "elementi": [{"modello": "equazione_ads", "usa": [...], "s": 0, "e": 5.5, "dati": {...}}]}]}

Errori (il piano non passa):
- modello non nel catalogo, non attivo, vietato, o lo stesso modello due volte di fila;
- `catalogo` diverso da quello che il motore riconosce negli elementi, o modo diverso da quello del modello;
- grafica fuori dal video, o due grafiche che si sovrappongono;
- «finestra» su un'inquadratura senza finestra grande (schema C), o con un rettangolo diverso da quello misurato;
- «tutto schermo» su un'inquadratura con le animazioni 3D (e animazioni 3D non ancora segnate);
- una parola scritta che non compare nell'SRT (esclusi + = €) o una cifra non detta;
- corpo del testo sotto il minimo (1,5 volte le lettere dei sottotitoli).
- (dal collaudo, 04/11/2026) grafica senza `momento`; lo stesso modello già usato per lo stesso momento in un altro ad
  dello storico (`libreria/uso-modelli-reel.json`) senza `varieta` che dica cosa cambia (modo o impaginazione) e perché;
- (dal collaudo) un testo scritto senza la sua riga in `testi_detti` ({scritto, detto, senso}): `detto` deve essere
  una frase contigua dell'SRT, le parole di `scritto` devono stare in `detto` nello stesso ordine, `senso` dice perché
  il significato non cambia.
Avvisi: testo che compare a più di 0,5 s dalla sua parola nella voce (da guardare, non da correggere per forza).
"""
import datetime
import json
import math
import re
import sys

from . import reel_comune as C
from .reel_comune import W, H

MODI = ('finestra', 'tutto schermo', 'micro', 'persona', 'palco')   # fase 6 (05/11/2026): micro-grafiche e modelli sulla persona;
# 07/11/2026 («nuova direzione» di Riccardo): il palco del reel (reel_palco.py)
K_LETTERA = 0.81        # altezza di «medicine» (punto della i -> linea di base) / corpo in Montserrat (fase 1: corpo 88 -> 72 px)
CHIAVI_TESTO = ('testo', 'chiave', 'cifra', 'num', 'op')


def testi(dati, base=''):
    """i testi che una grafica scrive: [{testo, t, dove}] (t in secondi dalla pagina, se c'è)"""
    out = []
    if isinstance(dati, dict):
        for k, v in dati.items():
            if k.startswith('_'):
                continue
            if k in CHIAVI_TESTO and isinstance(v, str):
                t = dati.get('t_' + k, dati.get('t'))
                out.append({'testo': v, 't': t if isinstance(t, (int, float)) else None, 'dove': f"{base}.{k}"})
            elif k == 'titolo' and isinstance(v, str):
                out.append({'testo': v, 't': dati.get('t'), 'dove': f"{base}.{k}"})
            else:
                out += testi(v, f"{base}.{k}")
    elif isinstance(dati, list):
        for i, v in enumerate(dati):
            out += testi(v, f"{base}[{i}]")
    return out


def corpi(dati, base=''):
    """i corpi del testo dichiarati nei dati: [(dove, corpo)]"""
    out = []
    if isinstance(dati, dict):
        for k, v in dati.items():
            if k.startswith('_'):
                continue
            if k.startswith('corpo') and isinstance(v, (int, float)):
                out.append((f"{base}.{k}", v))
            else:
                out += corpi(v, f"{base}.{k}")
    elif isinstance(dati, list):
        for i, v in enumerate(dati):
            out += corpi(v, f"{base}[{i}]")
    return out


def intervalli(g, fps):
    """i fotogrammi in cui la grafica può essere visibile, secondo il piano: le apparizioni, o tutta la pagina"""
    out = []
    if g.get('proposta'):
        ap = g.get('apparizioni') or [{'s': 0, 'e': g['frames'] / fps}]
        return sorted((g['f0'] + round(a['s'] * fps), g['f0'] + round(a['e'] * fps) - 1) for a in ap)
    for x in g['elementi']:
        ap = (x.get('dati') or {}).get('apparizioni')
        if ap:
            out += [(g['f0'] + round(a['s'] * fps), g['f0'] + round(a['e'] * fps) - 1) for a in ap]
        else:
            out.append((g['f0'] + round(x.get('s', 0) * fps), g['f0'] + min(g['frames'], round(x.get('e', g['frames'] / fps) * fps)) - 1))
    return sorted(out)


def firma(P, fps):
    """quello che Riccardo approva di un piano (regola del 04/11/2026: «il mio ok resta valido se, costruendo i
    modelli, tempi, testi e modo non cambiano»): per ogni grafica nome, modo, fotogrammi visibili e i testi scritti con
    il loro tempo. Una proposta e il modello costruito con gli stessi testi e tempi hanno la stessa firma."""
    out = []
    for g in sorted(P['grafiche'], key=lambda g: g['f0']):
        if g.get('proposta'):
            tt = [(t['testo'], t.get('t')) for t in g.get('testi', [])]
        else:
            tt = [(t['testo'], t['t']) for x in g.get('elementi', []) for t in testi(x.get('dati') or {})]
        tt = sorted({(a, round(b, 3)) for a, b in tt if b is not None and re.search(r'[0-9A-Za-zÀ-ÿ]', a)})
        out.append({'nome': g['nome'], 'modo': g.get('modo'), 'f0': g['f0'], 'frames': g['frames'],
                    'visibile': [list(v) for v in intervalli(g, fps)], 'testi': [list(v) for v in tt]})
    return out


def corpo_minimo(R):
    h = (R['sottotitoli'].get('fascia') or {}).get('altezza_lettere_px')
    return (math.ceil(1.5 * h / K_LETTERA), h) if h else (84, None)


def parole_scritte(t):
    """le parole di un testo di grafica da confrontare con l'SRT, e le cifre che contiene"""
    pw = [w for w in C.parole_di(t) if w not in C.SIMBOLI_AMMESSI]
    return pw, re.findall(r'\d+', t)


STORICO = C.AGENTE / 'libreria' / 'uso-modelli-reel.json'


def storico():
    """{ad: voce} dello storico, senza le chiavi di commento («_cosa»)"""
    S = C.leggi(STORICO, {}) if STORICO.exists() else {}
    return {k: v for k, v in S.items() if not k.startswith('_') and isinstance(v, dict)}


def canonico(idg, cat):
    """una variante «in prova» che corregge un difetto vale come il suo modello di partenza (stesso aspetto)"""
    m = cat.get(idg)
    while m and m.get('in_prova') and m.get('variante_di') in cat:
        idg = m['variante_di']
        m = cat.get(idg)
    return idg


def _seq(t):
    return [w for w in C.parole_di(t) if w not in C.SIMBOLI_AMMESSI]


def _seqp(t):
    """come _seq, senza le cifre (si controllano con i numeri detti: «3» sulla card vale «terzo»)"""
    return [w for w in _seq(t) if not re.fullmatch(r'\d+', w)]


def _contigua(a, b):
    return any(b[i:i + len(a)] == a for i in range(len(b) - len(a) + 1)) if a else False


SENSO = {'non', 'solo', 'più', 'senza', 'niente', 'meno', 'anche', 'mai', 'nessuno', 'nemmeno', 'neanche', 'ma'}


def _tolte(a, b):
    """le parole «del senso» (non, solo, più, senza…) di b che stanno accanto ad a o fra le sue parole e che a lascia
    fuori: «pastiglie» in «niente pastiglie in più» lascia fuori «niente» e «più»"""
    if not a:
        return []
    for i in range(len(b)):
        if b[i] != a[0]:
            continue
        pos, j = [i], i
        for w in a[1:]:
            j = next((k for k in range(j + 1, len(b)) if b[k] == w), None)
            if j is None:
                break
            pos.append(j)
        if len(pos) == len(a):
            vicine = set(range(pos[0] - 2, pos[-1] + 3)) - set(pos)
            out = []
            for k in sorted(vicine):
                if 0 <= k < len(b) and b[k] in SENSO and b[k] not in out and b[k] not in a:
                    out.append(b[k])
            return out
    return []


def _in_ordine(a, b):
    it = iter(b)
    return all(w in it for w in a)


def controlla(slug, P=None, R=None):
    D = C.cartella(slug)
    R = R or C.leggi(D / 'radiografia.json')
    P = P or C.leggi(D / 'piano.json')
    from . import catalogo as K
    cat = K.per_id()
    fps, nf = R['fps'], R['fotogrammi']
    err, avv, info = [], [], []
    detti, numeri = set(R['parole_dette']), set(R['numeri_detti'])
    a3 = R.get('animazioni_3d') or {}
    if a3.get('stato') != 'segnate':
        err.append("animazioni 3D non ancora segnate nella radiografia (./mve reel-3d)")
    tre = {f for a, b in a3.get('fotogrammi', []) for f in range(a, b + 1)}
    inq_di = {}
    for s in R['inquadrature']:
        for f in range(s['f0'], s['f1'] + 1):
            inq_di[f] = s
    cmin, hs = corpo_minimo(R)
    voce = R['voce']['parole']
    nomi = [g['nome'] for g in P['grafiche']]
    if len(set(nomi)) != len(nomi):
        err.append("due grafiche con lo stesso nome")
    occupati = {}
    righe = []
    # collaudo (04/11/2026): varietà fra gli ads e testi accorciati. Il caso fisso della regressione ha il piano
    # congelato di prima della regola, e i piani di laboratorio rifanno un ad già approvato: lì sono solo avvisi.
    # fase 6: un piano di laboratorio con "regole_piene" (il confronto AD_REFLUSSO-piena) ha momento e testi_detti obbligatori;
    # la varietà resta solo per gli ads veri (un confronto rifà un ad già fatto)
    nuove_regole = (not slug.startswith('_regressione') and not P.get('laboratorio')) or bool(P.get('regole_piene'))
    manca = err.append if nuove_regole else avv.append
    # solo gli ads PRECEDENTI (ordine dello storico): un ad non si confronta con quelli venuti dopo
    S0 = storico()
    chiavi = list(S0)
    prima_di = chiavi[:chiavi.index(slug)] if slug in chiavi else chiavi
    ST = {k: S0[k] for k in prima_di if not slug.startswith(k + '-')}
    srt_seq = _seq(' '.join(r['t'] for r in R.get('srt', [])))
    for g in sorted(P['grafiche'], key=lambda g: g['f0']):
        n = g['nome']
        pro = g.get('proposta')
        if pro:
            # collaudo (04/11/2026): modello per gli ads non ancora costruito. Si controlla tutto quello che si vede
            # (tempi, modo, 3D, finestra, parole, testi detti); il modello nasce dopo l'ok di Riccardo
            idg = g.get('catalogo') or pro.get('nuovo_id')
            m = None
            base = cat.get(pro.get('da_modello'))
            if not base:
                err.append(f"{n}: proposta da «{pro.get('da_modello')}», che non è nel catalogo")
            elif base['stato'] == 'vietato':
                err.append(f"{n}: proposta da «{pro.get('da_modello')}», che è vietato")
            if idg in cat:
                err.append(f"{n}: «{idg}» c'è già nel catalogo: niente proposta, usa il modello")
            for r in pro.get('reference', []):
                if not (C.AGENTE / 'libreria' / 'reference' / f"{r}.mov").exists():
                    err.append(f"{n}: reference «{r}» non è in libreria/reference/")
            avv.append(f"{n}: PROPOSTA «{idg}» da «{pro.get('da_modello')}» ({', '.join(pro.get('reference', []))}): si costruisce solo dopo l'ok di Riccardo al piano")
        elif not g.get('elementi'):
            err.append(f"{n}: nessun elemento")
            continue
        else:
            ids = [K.identifica(x) for x in g['elementi']]
            idg = ids[0]
            if g.get('catalogo') != idg:
                err.append(f"{n}: il piano dice catalogo «{g.get('catalogo')}», gli elementi sono «{idg}»")
            m = cat.get(idg)
        if not m and not pro:
            err.append(f"{n}: «{idg}» non è nel catalogo")
        elif m and m['stato'] == 'vietato':
            err.append(f"{n}: «{idg}» è vietato")
        elif m and m['stato'] != 'attivo':
            if m.get('in_prova'):
                avv.append(f"{n}: «{idg}» è IN PROVA (variante corretta, diventa attiva solo con l'ok di Riccardo): dirlo nel piano")
            elif not P.get('laboratorio'):
                err.append(f"{n}: «{idg}» è {m['stato']}, non attivo (in produzione solo modelli attivi o in prova)")
        if m and m['stato'] == 'attivo':
            nuove = [v['id'] for v in cat.values() if v.get('in_prova') and v.get('variante_di') == idg and v.get('corregge', True)]
            if nuove:
                avv.append(f"{n}: per «{idg}» c'è la variante in prova «{nuove[0]}» che corregge un difetto: usare quella")
        modo = g.get('modo')
        if modo not in MODI:
            err.append(f"{n}: modo «{modo}» (deve essere uno di {', '.join(MODI)})")
        if m and modo:
            mm = (m['motore'].get('dati') or {}).get('modo')
            atteso = mm if mm in ('micro', 'persona', 'palco') else ('finestra' if ('finestra' in idg or mm == 'finestra') else 'tutto schermo')
            if idg == 'palco-fascia-alta':
                atteso = 'palco'
            if modo != atteso:
                err.append(f"{n}: il modello «{idg}» è da «{atteso}», il piano dice «{modo}»")
        f0, f1 = g['f0'], g['f0'] + g['frames'] - 1
        if f0 < 0 or f1 >= nf:
            err.append(f"{n}: fotogrammi {f0}-{f1} fuori dal video (0-{nf - 1})")
        iv = intervalli(g, fps)
        vis = {f for a, b in iv for f in range(a, b + 1)}
        for k, fs in occupati.items():
            if vis & fs:
                err.append(f"{n} e {k} si sovrappongono nei fotogrammi {min(vis & fs)}-{max(vis & fs)}")
        occupati[n] = vis
        inqs = sorted({inq_di[f]['n'] for f in vis if f in inq_di})
        if modo == 'tutto schermo' and vis & tre:
            err.append(f"{n}: «tutto schermo» sulle animazioni 3D (fotogrammi {min(vis & tre)}-{max(vis & tre)})")
        # produzione (04/11/2026, direttore su AD_COLON): una riga di sottotitolo su due righe può salire dentro il
        # rettangolo della finestra; la grafica la coprirebbe (mai una grafica sopra i sottotitoli)
        if modo == 'finestra':
            for rg in (R['sottotitoli'].get('righe') or []):
                fm, bx = rg.get('fotogrammi_misurati'), rg.get('box_lettere')
                if not fm or not bx:
                    continue
                comuni = sorted(set(range(fm[0], fm[1] + 1)) & vis)
                if not comuni:
                    continue
                f = comuni[0]
                rr0 = None
                for x in (g.get('elementi') or []):
                    rr0 = (x.get('dati') or {}).get('rett')
                q = inq_di[f].get('rett_grafica') if f in inq_di else None
                if isinstance(rr0, list):
                    tr = (f - f0) / fps
                    rr0 = [r_ for r_ in rr0 if r_.get('da', 0) <= tr + 0.0011][-1]
                r = rr0 or q
                if r and bx[1] < r['y'] + r['h'] and bx[3] > r['y'] and bx[0] < r['x'] + r['w'] and bx[2] > r['x']:
                    err.append(f"{n}: la finestra (fino a y {r['y'] + r['h']}) copre il sottotitolo «{rg['srt']}» (lettere da y {bx[1]}) "
                               f"nei fotogrammi {comuni[0]}-{comuni[-1]}: accorciare la grafica o cambiare modo")
        if modo == 'finestra' and pro:
            for f in sorted(vis):
                s_ = inq_di.get(f)
                if not s_ or not s_.get('rett_grafica'):
                    err.append(f"{n}: «finestra» al fotogramma {f}, inquadratura {s_ and s_['n']} senza finestra grande (schema {s_ and s_['schema']})")
                    break
        if modo == 'finestra' and not pro:
            for x in g['elementi']:
                rr = (x.get('dati') or {}).get('rett')
                if rr is None:
                    err.append(f"{n}: «finestra» senza rett")
                    continue
                rr = rr if isinstance(rr, list) else [dict(rr, da=0)]
                for f in sorted(vis):
                    s = inq_di.get(f)
                    if not s or not s.get('rett_grafica'):
                        err.append(f"{n}: «finestra» al fotogramma {f}, inquadratura {s and s['n']} senza finestra grande (schema {s and s['schema']})")
                        break
                    tr = (f - f0) / fps
                    r = [q for q in rr if q.get('da', 0) <= tr + 0.0011][-1]   # i modelli cambiano 1 ms prima di da
                    q = s['rett_grafica']
                    dd = max(abs(r['x'] - q['x']), abs(r['y'] - q['y']), abs(r['w'] - q['w']), abs(r['h'] - q['h']), abs(r.get('r', q['r']) - q['r']))
                    if dd > 2:
                        err.append(f"{n}: al fotogramma {f} il rettangolo {r} è lontano {dd} px dalla finestra misurata {q} (inquadratura {s['n']})")
                        break
        if modo in ('micro', 'persona') and not pro:
            from . import reel_piano as RP
            e2, a2 = RP.controlla_zona(g, R, vis, f0, fps, P.get('zoom') or [])
            err += e2; avv += a2
        # testi
        if pro:
            tt = [{'testo': t['testo'], 't': t.get('t'), 'dove': f"testi[{i}]", 'el': 0} for i, t in enumerate(g.get('testi', []))]
            if not tt:
                err.append(f"{n}: proposta senza «testi» ({{testo, t}} in secondi dalla pagina)")
        else:
            tt = [dict(t, el=i) for i, x in enumerate(g['elementi']) for t in testi(x.get('dati') or {})]
        for t in tt:
            pw, cif = parole_scritte(t['testo'])
            for w in pw:
                if re.fullmatch(r'\d+', w):
                    continue
                if w not in detti:
                    err.append(f"{n}: «{w}» (in «{t['testo']}», {t['dove']}) non è una parola dell'SRT")
            for c in cif:
                if c not in numeri:
                    err.append(f"{n}: cifra «{c}» (in «{t['testo']}») non detta")
        # testi accorciati: la frase detta intera accanto, e il senso
        td = g.get('testi_detti') or []
        visti = []
        for q in td:
            sc = q.get('scritto')
            for s1 in (sc if isinstance(sc, list) else [sc]):
                visti.append(_seq(s1 or ''))
                if not _in_ordine(_seqp(s1 or ''), _seq(q.get('detto', ''))):
                    err.append(f"{n}: testi_detti «{s1}»: le parole non stanno in «{q.get('detto')}» nello stesso ordine")
            # le righe di uno stesso testo (lista in «scritto») si controllano insieme
            insieme = ' '.join(sc if isinstance(sc, list) else [sc or ''])
            if _in_ordine(_seqp(insieme), _seq(q.get('detto', ''))):
                tolte = _tolte(_seqp(insieme), _seq(q.get('detto', '')))
                if tolte:
                    avv.append(f"{n}: «{insieme}» lascia fuori " + ', '.join(f"«{w}»" for w in tolte)
                               + f" (da «{q.get('detto')}»): il senso scritto in testi_detti deve spiegare perché non cambia")
            if not _contigua(_seq(q.get('detto', '')), srt_seq):
                err.append(f"{n}: testi_detti: «{q.get('detto')}» non è una frase dell'SRT (va copiata intera, come è detta)")
            if not (q.get('senso') or '').strip():
                err.append(f"{n}: testi_detti «{sc}»: manca «senso» (perché il significato non cambia)")
        for t in tt:
            w = _seq(t['testo'])
            if w and not all(re.fullmatch(r'\d+', x) for x in w) and w not in visti:
                manca(f"{n}: «{t['testo']}» ({t['dove']}) senza la sua riga in testi_detti (frase detta intera e senso)")
        # varietà fra gli ads
        mom = g.get('momento')
        prima = []
        if not mom:
            manca(f"{n}: manca «momento» (serve per lo storico e la varietà fra i reel)")
        elif not P.get('laboratorio'):
            for ad, voce_st in ST.items():
                for q in voce_st.get('grafiche', []):
                    if q.get('momento') != mom:
                        continue
                    prima.append(dict(q, ad=ad))
                    # una proposta vale come il modello da cui nasce
                    if canonico(q['catalogo'], cat) == canonico(pro['da_modello'] if pro else idg, cat):
                        v = g.get('varieta') or {}
                        if v.get('cambia') not in ('modo', 'impaginazione') or not (v.get('perche') or '').strip() or not (v.get('come') or '').strip():
                            err.append(f"{n}: «{idg}» è lo stesso modello usato per «{mom}» in {ad}: scegli un'alternativa del catalogo, "
                                       "o scrivi varieta {cambia: modo|impaginazione, come, perche}")
                        elif v['cambia'] == 'modo' and q.get('modo') == modo:
                            err.append(f"{n}: varieta dice che cambia il modo, ma era «{q.get('modo')}» anche in {ad}")
            # fase 6 (05/11/2026, riga di icone per l'obiettivo in 3 ads su 4): un modello già usato per lo stesso momento in
            # due ads o più non basta cambiarlo di impaginazione: si sceglie un'alternativa, o si scrivono le alternative
            # del catalogo scartate e perché (varieta.alternative)
            stessi = [q for q in prima if canonico(q['catalogo'], cat) == canonico(pro['da_modello'] if pro else idg, cat)]
            if len({q['ad'] for q in stessi}) >= 2 and not (g.get('varieta') or {}).get('alternative'):
                err.append(f"{n}: «{idg}» è già stato usato per «{mom}» in {len({q['ad'] for q in stessi})} reel "
                           f"({', '.join(sorted({q['ad'] for q in stessi}))}): scegli un altro modello, o scrivi in varieta.alternative "
                           "le alternative del catalogo scartate e perché")
        for dove, c in ([('corpo', g['corpo'])] if pro and g.get('corpo') else []) + ([(f"testi[{i}].corpo", t['corpo']) for i, t in enumerate(g.get('testi', [])) if pro and t.get('corpo')]) + [d for x in (g.get('elementi') or []) for d in corpi(x.get('dati') or {})]:
            if c < cmin:
                err.append(f"{n}: corpo {c} in {dove} sotto il minimo {cmin} (1,5 volte i sottotitoli, {hs} px)")
        # aggancio alla voce
        agg = []
        for t in tt:
            if t['t'] is None:
                continue
            ta = f0 / fps + t['t']
            pw = [w for w in C.parole_di(t['testo']) if w not in C.SIMBOLI_AMMESSI]
            if not pw:
                continue
            def uguale(a, b):
                return a == b or C.NUMERI.get(a) == b or C.ORDINALI.get(a) == b or a.replace('€', '') == b
            cand = [v for v in voce if uguale(C.norm(v['parola']), pw[0])]
            if not cand:
                agg.append({'testo': t['testo'], 't': round(ta, 3), 'voce': None, 'scarto': None})
                continue
            v = min(cand, key=lambda v: abs(v['a_inviluppo'] - ta))
            sc = round(ta - v['a_inviluppo'], 2)
            agg.append({'testo': t['testo'], 't': round(ta, 3), 'voce': v['parola'], 'voce_t': v['a_inviluppo'], 'scarto': sc})
            if abs(sc) > 0.5:
                avv.append(f"{n}: «{t['testo']}» compare a {ta:.2f} s, la voce dice «{v['parola']}» a {v['a_inviluppo']:.2f} s "
                           f"(scarto {sc:+.2f} s): da guardare")
        righe.append({'nome': n, 'catalogo': idg, 'stato_catalogo': 'PROPOSTA, da costruire' if pro else (m and ('in prova' if m.get('in_prova') else m['stato'])), 'modo': modo,
                      'proposta': pro, 'f0': f0, 'f1': f1,
                      'tempo': [round(f0 / fps, 3), round((f1 + 1) / fps, 3)], 'intervalli': iv, 'inquadrature': inqs,
                      'testi': [t['testo'] for t in tt], 'aggancio': agg, 'voce': g.get('voce', ''), 'perche': g.get('perche', ''),
                      'momento': mom, 'prima': prima, 'varieta': g.get('varieta'), 'impaginazione': g.get('impaginazione', ''),
                      'testi_detti': td})
    # fase 6: zoom, effetti sonori, ritmo
    from . import reel_zoom as RZ, reel_suono as RS, reel_piano as RP
    occ = {}
    for r_ in righe:
        for a_, b_ in r_['intervalli']:
            for f in range(a_, b_ + 1):
                occ[f] = (r_['nome'], r_['modo'])
    e2, a2 = RZ.controlla(P, R, occ); err += e2; avv += a2
    e2, a2 = RS.controlla(P); err += e2; avv += a2
    from . import reel_palco as RPal
    e2, a2 = RPal.controlla(dict(P, slug=slug), R); err += e2; avv += a2
    ritmo = RP.ritmo(P, R, righe)
    avv += ritmo['avvisi']
    if ritmo.get('errori'):
        for e_ in ritmo['errori']:
            (err.append if P.get('densita') == 'piena' else avv.append)(e_)
    # lo stesso modello due volte di fila
    # fase 6: le micro-grafiche si ripetono per natura; giro 4: l'infografica è un motore di scene (la varietà la dà la
    # composizione, scritta in «impaginazione»)
    # 07/11/2026: il palco è lo stesso per tutto il reel per definizione (un palco per reel)
    grandi = [r_ for r_ in righe if r_['modo'] not in ('micro', 'palco') and not str(r_['catalogo']).startswith('infografica-')]
    for a, b in zip(grandi, grandi[1:]):
        if a['catalogo'] == b['catalogo']:
            err.append(f"{b['nome']}: «{b['catalogo']}» due volte di fila (dopo {a['nome']})")
    # i momenti coperti negli altri ads e lasciati senza grafica qui
    usati = {r['momento'] for r in righe}
    scoperti = [dict(q, ad=ad) for ad, v in ST.items() for q in v.get('grafiche', []) if q.get('momento') not in usati]
    senza = P.get('senza_grafica') or []
    info = {'corpo_minimo': cmin, 'altezza_sottotitoli_px': hs, 'grafiche': righe, 'scoperti': scoperti, 'senza_grafica': senza,
            'ritmo': ritmo, 'confronto': RP.confronto(P)}
    return err, avv, info


# ---------------------------------------------------------------- tavola

def _strip(R, info, wpx=1620):
    """striscia del tempo: inquadrature (schema, 3D), sottotitoli, grafiche"""
    from PIL import Image, ImageDraw, ImageFont
    f = lambda s: ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', s)
    nf, fps = R['fotogrammi'], R['fps']
    im = Image.new('RGB', (wpx, 250), (250, 250, 250))
    d = ImageDraw.Draw(im)
    X = lambda fr: 10 + (wpx - 20) * fr / nf
    tre = {n for n in (R.get('animazioni_3d') or {}).get('inquadrature', [])}
    col = {'A': (200, 215, 240), 'B': (210, 235, 210), 'C': (240, 225, 200), None: (220, 220, 220)}
    for s in R['inquadrature']:
        d.rectangle([X(s['f0']), 40, X(s['f1'] + 1) - 1, 90], fill=col.get(s['schema']), outline=(120, 120, 120))
        d.text((X(s['f0']) + 4, 44), f"{s['n']}{s['schema'] or '?'}", font=f(20), fill='black')
        if s['n'] in tre:
            d.rectangle([X(s['f0']), 70, X(s['f1'] + 1) - 1, 90], fill=(230, 80, 80))
            d.text((X(s['f0']) + 4, 70), '3D', font=f(16), fill='white')
    for o in R['sottotitoli']['righe']:
        if o.get('fotogrammi_misurati'):
            a, b = o['fotogrammi_misurati']
            d.rectangle([X(a), 100, X(b + 1) - 1, 110], fill=(150, 150, 150))
    for i, g in enumerate(info['grafiche']):
        c = (40, 170, 90) if g['modo'] == 'finestra' else (40, 90, 200)
        for a, b in g['intervalli']:
            d.rectangle([X(a), 125 + (i % 2) * 50, X(b + 1) - 1, 165 + (i % 2) * 50], fill=c)
        d.text((X(g['intervalli'][0][0]) + 3, 130 + (i % 2) * 50), g['nome'], font=f(18), fill='white')
    for s in range(0, int(nf / fps) + 1, 5):
        d.line([X(s * fps), 30, X(s * fps), 36], fill='black')
        d.text((X(s * fps) - 8, 8), f"{s}s", font=f(18), fill='black')
    d.text((wpx - 560, 228), 'verde = finestra, blu = tutto schermo, rosso = 3D, grigio = sottotitoli', font=f(16), fill='black')
    return im


FONT = C.AGENTE / 'motore' / 'motore' / 'risorse' / 'fonts' / 'Montserrat-VF.ttf'
VERDE, PANNA, NOTTE = (114, 250, 147, 255), (244, 244, 244, 255), (0, 26, 61, 255)


def bozza(G, R, t, f):
    """bozza statica di una grafica proposta al tempo t (s dalla pagina): la zona della grafica (finestra o tutto
    schermo) e i testi già comparsi, in Montserrat, con le icone come riquadri. Non è il modello: serve a Riccardo per
    vedere dove sta e cosa dice."""
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if not any(a['s'] <= t < a['e'] for a in (G.get('apparizioni') or [{'s': 0, 'e': G['frames'] / R['fps']}])):
        return im
    if G['modo'] == 'finestra':
        s = next((q for q in R['inquadrature'] if q['f0'] <= f <= q['f1']), None)
        q = (s or {}).get('rett_grafica') or {'x': 28, 'y': 373, 'w': 1024, 'h': 549, 'r': 67}
        d.rounded_rectangle([q['x'], q['y'], q['x'] + q['w'], q['y'] + q['h']], radius=q['r'], fill=NOTTE)
        cx = q['x'] + q['w'] / 2
    else:
        d.rectangle([0, 0, W, H], fill=NOTTE)
        cx = W / 2
    for ic in G.get('bozza_icone', []):
        if ic.get('t', 0) <= t:
            x, y, l = ic['x'], ic['y'], ic.get('lato', 140)
            d.rounded_rectangle([x, y, x + l, y + l], radius=24, outline=VERDE, width=6)
            fi = ImageFont.truetype(str(FONT), 26)
            d.text((x + l / 2, y + l / 2), ic['nome'], font=fi, fill=VERDE, anchor='mm')
    for tx in G.get('testi', []):
        if tx.get('t', 0) > t or ('via' in tx and tx['via'] <= t):
            continue
        fo = ImageFont.truetype(str(FONT), tx.get('corpo', G.get('corpo', 84)))
        try:
            fo.set_variation_by_axes([tx.get('peso', 700)])
        except Exception:
            pass
        col = VERDE if tx.get('chiave') else PANNA
        x = tx.get('x', cx)
        anc = 'lm' if 'x' in tx else 'mm'
        d.text((x, tx.get('y', 640)), tx['testo'], font=fo, fill=col, anchor=anc)
        if tx.get('barra_t') is not None and tx['barra_t'] <= t:
            bb = d.textbbox((x, tx.get('y', 640)), tx['testo'], font=fo, anchor=anc)
            ym = (bb[1] + bb[3]) / 2
            d.rectangle([bb[0] - 10, ym - 5, bb[2] + 10, ym + 5], fill=PANNA)
    return im


def tavola(slug, P, R, info, out):
    """per ogni grafica, i momenti chiave fotografati sopra il fotogramma vero del video"""
    from PIL import Image, ImageDraw, ImageFont
    from . import reel_grafiche
    fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20)
    fps = R['fps']
    L = C.lavoro(slug, 'piano')
    V = C.AGENTE / R['sorgente']['video']
    righe_img = []
    per = {g['nome']: g for g in P['grafiche']}
    for g in info['grafiche']:
        G = per[g['nome']]
        momenti = {g['intervalli'][0][0] + 2}
        for a in g['aggancio']:
            f = round(a['t'] * fps) + round(0.6 * fps)
            momenti.add(f)
        for a, b in g['intervalli']:
            momenti.add(b)
        vis = [f for a, b in g['intervalli'] for f in range(a, b + 1)]
        momenti = sorted({min(vis, key=lambda v: abs(v - m)) for m in momenti})
        if len(momenti) > 8:
            momenti = [momenti[round(i * (len(momenti) - 1) / 7)] for i in range(8)]
        if G.get('proposta'):
            fs = [bozza(G, R, (m - G['f0']) / fps, m) for m in momenti]
        else:
            pg = reel_grafiche.pagina(G['elementi'], G['frames'], fps, L / f"pagina-{g['nome']}")
            sd = L / f"scatti-{g['nome']}"
            if sd.exists():
                import shutil
                shutil.rmtree(sd)
            fs = reel_grafiche.scatti(pg, [(m - G['f0']) / fps + 0.0005 for m in momenti], sd, tmpdir=L / 'tmp-hf', cifre=4)
        tiles = []
        basi = C.estrai(V, momenti)
        for m, p in zip(momenti, fs):
            base = basi[m].convert('RGBA')
            gr = p if not isinstance(p, (str, type(L))) else Image.open(p).convert('RGBA')
            im = Image.alpha_composite(base, gr).convert('RGB').resize((270, 480), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            d.rectangle([0, 0, 150, 26], fill=(255, 230, 0)); d.text((4, 2), f"{m / fps:6.2f}s f{m}", font=fnt, fill='black')
            tiles.append(im)
        riga = Image.new('RGB', (1620, 540), 'white')
        d = ImageDraw.Draw(riga)
        d.text((6, 4), ("BOZZA (modello da costruire, da " + G['proposta'].get('da_modello', '') + ", ref " + ', '.join(G['proposta'].get('reference', [])) + ")  ·  " if G.get('proposta') else '')
               + f"{g['nome']}  ·  {g['catalogo']}  ·  {g['modo']}  ·  {g['tempo'][0]:.2f}-{g['tempo'][1]:.2f} s  ·  inq {g['inquadrature']}",
               font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 24), fill='black')
        for i, t in enumerate(tiles[:6]):
            riga.paste(t, (i * 270, 50))
        righe_img.append(riga)
        if len(tiles) > 6:
            r2 = Image.new('RGB', (1620, 500), 'white')
            for i, t in enumerate(tiles[6:]):
                r2.paste(t, (i * 270, 10))
            righe_img.append(r2)
    strip = _strip(R, info)
    from . import reel_piano as RP
    rs = RP.striscia_ritmo(R, info, P)
    s2 = Image.new('RGB', (1620, strip.height + rs.height), 'white'); s2.paste(strip, (0, 0)); s2.paste(rs, (0, strip.height)); strip = s2
    tot = Image.new('RGB', (1620, strip.height + sum(r.height for r in righe_img)), 'white')
    tot.paste(strip, (0, 0))
    y = strip.height
    for r in righe_img:
        tot.paste(r, (0, y)); y += r.height
    out.parent.mkdir(parents=True, exist_ok=True)
    tot.save(out, quality=86)


def piano(slug):
    D = C.cartella(slug)
    R = C.leggi(D / 'radiografia.json')
    P = C.leggi(D / 'piano.json')
    err, avv, info = controlla(slug, P, R)
    out = D / 'piano'
    out.mkdir(exist_ok=True)
    md5 = C.md5_file(D / 'piano.json')
    L = [f"# Piano delle grafiche: {slug}", '', f"Controllato da `./mve reel-piano` il {datetime.datetime.now():%d/%m/%Y %H:%M}. "
         f"md5 di `piano.json`: `{md5}`.", '',
         f"Corpo minimo dei testi: {info['corpo_minimo']} (lettere dei sottotitoli {info['altezza_sottotitoli_px']} px × 1,5).", '',
         '| grafica | modello | modo | fotogrammi | tempo (s) | inquadrature | testi |', '|---|---|---|---|---|---|---|']
    for g in info['grafiche']:
        L.append(f"| {g['nome']} | `{g['catalogo']}` ({g['stato_catalogo']}) | {g['modo']} | "
                 + ', '.join(f"{a}–{b}" for a, b in g['intervalli']) + f" | {g['tempo'][0]:.3f}–{g['tempo'][1]:.3f} | {g['inquadrature']} | "
                 + ' / '.join(f"«{t}»" for t in g['testi']) + ' |')
    L += ['', '## Aggancio alla voce', '', '| grafica | testo | compare (s) | parola nella voce (s) | scarto |', '|---|---|---|---|---|']
    for g in info['grafiche']:
        for a in g['aggancio']:
            L.append(f"| {g['nome']} | «{a['testo']}» | {a['t']:.2f} | " + (f"«{a['voce']}» {a['voce_t']:.2f} | {a['scarto']:+.2f}" if a['voce'] else '— | —') + ' |')
    L += ['', '## Varietà fra i reel (storico `libreria/uso-modelli-reel.json`)', '',
          '| momento | prima (ad: modello, modo, impaginazione) | ora | cosa cambia |', '|---|---|---|---|']
    for g in info['grafiche']:
        pr = '<br>'.join(f"{q['ad']}: `{q['catalogo']}`, {q.get('modo')}, {q.get('impaginazione', '')}" for q in g['prima']) or '—'
        v = g['varieta']
        L.append(f"| {g['momento'] or '—'} | {pr} | `{g['catalogo']}`, {g['modo']}, {g['impaginazione']} | "
                 + (f"stesso modello: cambia {v['cambia']} ({v['come']}); perché: {v['perche']}" if v else ('modello diverso' if g['prima'] else 'momento nuovo')) + ' |')
    for q in info['scoperti']:
        ss = [x for x in info['senza_grafica'] if x.get('momento') == q.get('momento')]
        L.append(f"| {q.get('momento')} | {q['ad']}: `{q['catalogo']}`, {q.get('modo')}, {q.get('impaginazione', '')} | nessuna grafica | "
                 + (ss[0].get('perche', '') if ss else '(perché non scritto)') + ' |')
    L += ['', '## Testi accorciati e frase detta', '', '| grafica | scritto | detto | senso |', '|---|---|---|---|']
    for g in info['grafiche']:
        for q in g['testi_detti']:
            sc = q.get('scritto')
            L.append(f"| {g['nome']} | " + ' / '.join(f"«{x}»" for x in (sc if isinstance(sc, list) else [sc])) + f" | «{q.get('detto')}» | {q.get('senso')} |")
    from . import reel_piano as RP
    L += RP.md_ritmo(info['ritmo'], P, info)
    L += ['', '## Perché', '']
    L += [f"- **{g['nome']}**: {g['perche'] or '(non scritto)'} {('Voce: ' + g['voce']) if g['voce'] else ''}" for g in info['grafiche']]
    L += ['', '## Esito', '']
    L += [f"- ERRORE: {e}" for e in err] or ['- nessun errore']
    L += [f"- da guardare: {a}" for a in avv]
    if not err:
        tavola(slug, P, R, info, out / 'tavola.jpg')
        L += ['', f"**Tavola visiva:** `piano/tavola.jpg`. Niente fermata sul piano (Riccardo, 05/11/2026): avanti con `./mve reel-rendi {slug}`; "
              "ci si ferma sull'anteprima."]
    (out / 'piano.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    C.scrivi(out / 'controllo.json', {'md5_piano': md5, 'errori': err, 'avvisi': avv, 'info': info,
                                       'data': f"{datetime.datetime.now():%d/%m/%Y %H:%M}"})
    for e in err:
        print('  ERRORE', e)
    for a in avv:
        print('  da guardare', a)
    if err:
        sys.exit(f"{slug}: il piano ha {len(err)} errori (piano/piano.md)")
    print(f"{slug}: piano a posto ({len(info['grafiche'])} grafiche, {len(avv)} da guardare). Tavola: {C.rel(out / 'tavola.jpg')}")
    # fase 6, giro 4 (Riccardo, 05/11/2026): niente fermata sul piano; ci si ferma sull'anteprima
    print(f"  ADESSO: ./mve reel-rendi {slug}" + (' --laboratorio' if P.get('laboratorio') else '') + " (niente fermata sul piano: ci si ferma sull'anteprima)")

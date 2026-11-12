"""Fase `qc`: controlli sul FILE CONSEGNATO, non sui dati che l'hanno prodotto.

Esce `controlli/QC.md` con una riga per controllo (atteso, misurato, esito) e un
verdetto: CONSEGNABILE o NON CONSEGNABILE. Un contatore a zero dove ci si
aspetta qualcosa non e un esito pulito: e un controllo che non ha girato, e
conta come errore.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from .progetto import Progetto, ts, ffmpeg
from . import audio as A
from . import trascrivi as T


def _probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_streams',
                        '-show_format', str(path)], capture_output=True, text=True)
    return json.loads(r.stdout)


def _rileva(path, filtro, chiave):
    err = subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-i', str(path), '-vf', filtro,
                          '-an', '-f', 'null', '-'], capture_output=True, text=True).stderr
    return re.findall(chiave, err)


def qc(slug, file=None):
    P = Progetto(slug)
    E = P.leggi('edl.json')
    G = P.leggi('grafica.json')
    path = P.render(file or f"{slug}_FINALE.mp4")
    if not path.exists():
        sys.exit(f"manca {path.name}: lancia prima `finale`")
    righe = []

    def check(nome, atteso, misurato, ok, grave=True):
        righe.append((nome, atteso, misurato, 'OK' if ok else ('ERRORE' if grave else 'AVVISO')))

    d = _probe(path)
    v = next(s for s in d['streams'] if s['codec_type'] == 'video')
    a = next((s for s in d['streams'] if s['codec_type'] == 'audio'), None)
    check('codec video', 'h264 High', f"{v['codec_name']} {v.get('profile')}",
          v['codec_name'] == 'h264' and v.get('profile') == 'High')
    check('risoluzione', '1920x1080', f"{v['width']}x{v['height']}", (v['width'], v['height']) == (1920, 1080))
    check('frame rate', f"{P.fps_str} (progetto)", v['r_frame_rate'], v['r_frame_rate'] == P.fps_str)
    check('pixel', 'yuv420p', v.get('pix_fmt'), v.get('pix_fmt') == 'yuv420p')
    tags = (v.get('color_primaries'), v.get('color_transfer'), v.get('color_space'))
    check('tag colore', 'bt709/bt709/bt709', '/'.join(str(x) for x in tags), tags == ('bt709',) * 3)
    # range limitato (16-235): un file `pc` su YouTube esce slavato o con i neri chiusi
    check('range colore', 'tv', v.get('color_range'), v.get('color_range') == 'tv')
    check('audio', 'aac 48 kHz stereo',
          f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']} ch" if a else 'assente',
          bool(a) and a['codec_name'] == 'aac' and a['sample_rate'] == '48000' and a['channels'] == 2)

    nf = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets',
                         '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', str(path)],
                        capture_output=True, text=True).stdout.strip().split(',')[0]
    nf = int(nf or 0)
    # la schermata finale YouTube (tappa 3) viene dopo l'ultima parola: frame in piu dell'EDL
    coda = (P.leggi('scena.json').get('coda') or {}) if P.data('scena.json').exists() and P.regia().get('scena', {}).get('coda') else {}
    nc = coda.get('frame', 0)
    if P.regia().get('scena', {}).get('coda'):
        check('schermata finale YouTube', f"{P.regia()['scena']['coda'].get('durata', 12):.0f} s dopo l'ultima parola",
              f"{nc / P.fps:.2f} s", abs(nc / P.fps - P.regia()['scena']['coda'].get('durata', 12)) < 0.05)
        for c in coda.get('controlli', []):
            check(f"schermata finale: {c['cosa']}", 'ok', c['valore'], c['ok'])
    check('frame', f"{E['frame'] + nc} (EDL" + (f" + {nc} di schermata finale)" if nc else ")"), nf, nf == E['frame'] + nc)
    da = float(a.get('duration', 0)) if a else 0
    check('durata audio', f"{E['durata'] + nc / P.fps:.2f}s", f"{da:.2f}s", abs(da - E['durata'] - nc / P.fps) < 0.08)

    L = A.loudness(path)
    check('loudness', '-14 ±1 LUFS', f"{L['I']} LUFS", L['I'] is not None and abs(L['I'] + 14) <= 1.0)
    check('true peak', '≤ -1.0 dBTP', f"{L['TP']} dBTP", L['TP'] is not None and L['TP'] <= -1.0)

    neri = _rileva(path, 'blackdetect=d=0.4:pix_th=0.03', r'black_start:([\d.]+)')
    neri = [float(x) for x in neri if float(x) > 0.5]
    check('frame neri', 'nessuno (oltre l\'apertura)', len(neri) or 'nessuno', not neri)
    fermi = [float(x) for x in _rileva(path, 'freezedetect=n=-62dB:d=2.5', r'freeze_start: ([\d.]+)')]
    # le schede piene (chiusura, stacchi) sono ferme per definizione
    pieni = [(c['s'] - 0.5, c['e'] + 0.5) for c in G['capitoli'] if not c['dietro']]
    if G.get('closing'):
        pieni.append((G['closing']['s'] - 0.5, G['closing']['e'] + 0.5))
    if nc:
        pieni.append((coda['s'] - 0.5, coda['s'] + nc / P.fps + 1))
    fermi = [t for t in fermi if not any(a <= t <= b for a, b in pieni)]
    check('immagine ferma', 'nessun tratto oltre 2,5 s (schede escluse)',
          ', '.join(ts(t) for t in fermi) or 'nessuno', not fermi, grave=False)

    conf = [c for c in G['cards'] if c.get('conflitto')]
    for k in ('opening', 'chip'):
        if G.get(k) and G[k].get('conflitto'):
            conf.append(G[k])
    marg = [c.get('margine_volto') for c in G['cards'] if c.get('margine_volto') is not None]
    if G['cards'] or G.get('opening') or (G.get('chip') and (G.get('chip') or {}).get('stile') not in ('v2', 'v3')):
        check('card sul volto', '0 sovrapposte', f"{len(conf)} sovrapposte, margine minimo "
              f"{min(marg):.0f} px" if marg else f"{len(conf)} sovrapposte", not conf and bool(marg))

    sag = len(list(P.p('data', 'sagome').glob('*.png'))) if P.p('data', 'sagome').is_dir() else 0
    att = sum(int(round((c['e'] - c['s']) * P.fps)) for c in G['capitoli'] if c['dietro'])
    check('sagome titoli dietro', f"{att} frame", sag, sag >= att * 0.98 if att else True)

    words = P.leggi('parole-montato.json')
    nasc = [(c['s'] + 0.1, c['e'] - 0.1) for c in G['capitoli']]
    if G.get('closing'):
        nasc.append((G['closing']['s'] + 0.3, G['closing']['e']))
    vis = [w for w in words if not any(x <= w[0] < y for x, y in nasc)]
    capw = sum(len(c['words']) for c in G['captions'])
    if G.get('sottotitoli') != 'chiave':
        check('copertura sottotitoli', '≥ 99% delle parole', f"{capw}/{len(vis)}",
              len(vis) > 0 and capw >= 0.99 * len(vis))

    # le parole dei sottotitoli contro i blocchi trascritti da soli: la copertura
    # sopra confronta i sottotitoli con la stessa trascrizione da cui vengono, e
    # non vede una parola che whisper ha perso ("ti senti nuovo" per "ti senti di nuovo")
    mancanti, nref = _parole_mancanti(P, E, G) if G.get('sottotitoli') != 'chiave' else ([], 0)
    if G.get('sottotitoli') != 'chiave':
        check('parole perse', '≤ 1% rispetto ai blocchi', f"{len(mancanti)} su {nref}",
              nref > 0 and len(mancanti) <= 0.01 * nref, grave=len(mancanti) > 0.01 * nref)
        if mancanti:
            righe[-1] = righe[-1][:3] + ('AVVISO' if len(mancanti) <= 0.01 * nref else 'ERRORE',)
    # contenuto (B-roll, testi, materiali, SRT, pannelli): gli stessi controlli dell'anteprima
    righe += controlli_contenuto(P, G)

    # ascolto delle giunte SUL FILE CONSEGNATO, con sonde brevi
    from .papere import riattacco
    from .edl import _ripetizione
    G_ = E['giunte']
    tmp = P.asset('qc-16k.wav')
    ffmpeg('-i', path, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', tmp)
    fin = []
    for g in G_:
        fin += [(max(0.0, g['t'] - 4.0), 4.0), (g['t'], 4.0)]
    testi = T.sonde(tmp, fin)
    tmp.unlink()
    sosp = []
    voluti = set(P.regia().get('giunte_ok', []))
    for k, g in enumerate(G_):
        pre, post = testi[2 * k], testi[2 * k + 1]
        r, _ = riattacco(pre, post)
        rip = _ripetizione(pre + ' ' + post)
        if (r or rip) and g['i'] not in voluti:
            sosp.append(f"G{g['i']:02d} {ts(g['t'])}: «{pre[-60:]}» ⟂ «{post[:60]}»")
    check('giunte ascoltate', f"{len(G_)}", f"{len(G_)} ascoltate, {len(sosp)} con ripetizioni",
          len(G_) > 0 and not sosp)
    # voce buttata accanto alla giunta (coda o attacco di una parola): whisper la
    # completa anche quando manca, quindi si misura l'energia sulla sorgente
    from .edl import controlla_parole_tagliate
    tagliate = controlla_parole_tagliate(P, E)
    check('parole tagliate alle giunte', '0', f"{len(tagliate)} su {len(G_)}", len(G_) > 0 and not tagliate)
    # ripetizioni (fase 7b rivista): il montato ritrascritto pezzo per pezzo
    from .ripetizioni import sul_montato
    n_rip, n_pezzi, _ = sul_montato(P, E)
    check('ripetizioni, parole tagliate, pezzi a meta parola (controlli/ripetizioni.md)', '0',
          f"{n_rip} su {n_pezzi} pezzi ritrascritti", n_pezzi > 0 and n_rip == 0)

    # pause lunghe (fase 7b): nessun silenzio della voce sopra 0,9 s, salvo i voluti
    from .edl import pause_lunghe, PAUSA_LUNGA
    pause, soglia_p = pause_lunghe(P, E)
    pl_no = [p for p in pause if not p['motivo']]
    check(f'pause lunghe (silenzi della voce oltre {PAUSA_LUNGA} s, sotto {soglia_p} dB)', '0 non dichiarate',
          f"{len(pl_no)} non dichiarate, {len(pause) - len(pl_no)} volute", not pl_no)

    _foglio_giunte(P, path, G_)

    errori = [r for r in righe if r[3] == 'ERRORE']
    esito = 'CONSEGNABILE' if not errori else 'NON CONSEGNABILE'
    out = [f"# QC: {path.name}", "", f"**Esito: {esito}**", "",
           "| controllo | atteso | misurato | esito |", "|---|---|---|---|"]
    out += [f"| {n} | {at} | {m} | {e} |" for n, at, m, e in righe]
    if mancanti:
        out += ["", "## Parole che mancano nei sottotitoli", "",
                "Si recuperano con una voce in `correzioni` (es. `[\"ti senti nuovo\", \"ti senti di nuovo\"]`).", ""]
        out += [f"- {m}" for m in mancanti]
    if tagliate:
        out += ["", "## Parole tagliate alle giunte", ""]
        out += [f"- G{t['i']:02d} {ts(t['t'])}: {t['voce_s'] * 1000:.0f} ms di voce (+{t['picco_db']} dB) buttati "
                f"{'dopo la fine' if t['lato'] == 'fine' else 'prima dell inizio'} (sorgente {t['da']:.2f}-{t['a']:.2f})"
                for t in tagliate]
    if pause:
        out += ["", "## Pause lunghe", ""]
        out += [f"- {ts(p['t'])}-{ts(p['fino'])}: {p['durata']:.2f} s (sorgente {p['src'][0]:.2f}-{p['src'][1]:.2f}) · "
                + (f"voluta: {p['motivo']}" if p['motivo'] else "**DA ACCORCIARE** (o in `pause_lunghe_ok` con il motivo)")
                for p in pause]
    if sosp:
        out += ["", "## Giunte da riascoltare", ""] + [f"- {s}" for s in sosp]
        out += ["", "Se una ripetizione e voluta (retorica), aggiungi il numero della giunta a "
                "`giunte_ok` in regia.json."]
    out += ["", "Fogli da guardare: `controlli/giunte.jpg` (±0,4 s a ogni giunta), "
            "`controlli/inquadrature.jpg`, `controlli/anteprima.jpg`."]
    P.controllo('QC.md').write_text('\n'.join(out), encoding='utf-8')
    for n, at, m, e in righe:
        print(f"  {e:<7} {n:<24} {m}")
    print(f"\n{esito} -> controlli/QC.md")
    if errori:
        sys.exit(1)


def controlli_contenuto(P, G=None, scrivi_file=True):
    """controlli sul CONTENUTO, prima ancora del master (girano anche con
    `finale --anteprima`): B-roll solo fra le clip utilizzabili, ogni testo a
    schermo detto nel suo intorno (o etichetta strutturale dichiarata), nessun
    materiale vietato, SRT completo, nessun pannello sulla testa."""
    from .grafica import piano as GP
    from .libreria import utilizzabili
    from . import consegna as C
    G = G or P.leggi('grafica.json')
    R = P.regia()
    W = GP.parole(P, R)
    righe, dettagli = [], []

    def check(nome, atteso, misurato, ok, grave=True):
        righe.append((nome, atteso, misurato, 'OK' if ok else ('ERRORE' if grave else 'AVVISO')))

    # B-roll
    usabili = {c['file']: c for c in utilizzabili(voto_min=1)}
    clip = [c['file'] for b in G.get('broll', []) for c in b['clip']]
    fuori = [c for c in clip if c not in usabili]
    basse = [c for c in clip if c in usabili and usabili[c]['descrizione']['voto'] < 4]
    check('B-roll: clip escluse o fuori indice', '0', f"{len(fuori)} su {len(clip)}", not fuori)
    check('B-roll: voto sotto 4', '0', f"{len(basse)}", not basse, grave=False)
    dettagli += [f"- B-roll non utilizzabile: {c}" for c in fuori] + [f"- B-roll con voto < 4: {c}" for c in basse]

    # testi a schermo: detti nel loro intorno, o etichette strutturali dichiarate
    strutt = {' '.join(GP.norm(x) for x in e.split()) for e in G.get('etichette_strutturali', [])}
    voci = []
    if G.get('chip'):
        voci += [(G['chip']['s'], G['chip']['e'], t) for t in (G['chip']['name'], G['chip']['role'])]
    voci += [(c['s'], c['e'], c['testo']) for c in G.get('frasi_chiave', [])]
    for x in G.get('inserti', []):
        voci += [(x['s'], x['e'], t) for t in x.get('testi', [])]
        if x['modello'] == 'numero':
            voci.append((x['s'], x['e'], str(x['dati'].get('valore'))))
    voci += [(c['s'], c['e'], f"{c['value']} {c['sub']}") for c in G.get('cards', [])]
    # i testi dei momenti della scena (fase 6c): stessi controlli
    # `richiama` (in regia, sull'elemento): gli istanti in cui lui ha detto quelle parole,
    # quando l'elemento le riprende piu avanti (la lista dei tentativi che torna)
    richiami = {}
    if P.data('scena.json').exists():
        for m in P.regia().get('scena', {}).get('momenti', []):
            for x in m.get('elementi', []):
                if x.get('richiama'):
                    richiami.setdefault((m['id'], x['modello']), []).extend(x['richiama'])
        for m in P.leggi('scena.json')['momenti']:
            for x in m.get('testi', []):
                voci += [(x['s'], x['e'], t, richiami.get((m['id'], x['modello']), [])) for t in x['testi']]
    non_detti, riformulati = [], []
    for v in voci:
        s, e, testo = v[:3]
        rich = v[3] if len(v) > 3 else []
        tok = [GP.norm(x) for x in testo.split() if GP.norm(x)]
        if len(tok) > 1 and tok[0].isdigit():
            tok = tok[1:]                              # numero d'elenco in testa alla riga: struttura
        if ' '.join(tok) in strutt:
            continue
        intorno = [GP.norm(w['t']) for w in W if s - 15 <= w['s'] <= e + 15 or any(r - 10 <= w['s'] <= r + 10 for r in rich)]
        it = iter(intorno)
        if all(any(t == v for v in it) for t in tok):
            continue                                   # detto, in quest'ordine
        if all(t in intorno for t in tok):
            riformulati.append(f"{ts(s)} «{testo}»")   # parole sue, in un altro ordine
        else:
            mancano = [t for t in tok if t not in intorno]
            non_detti.append(f"{ts(s)} «{testo}» (non dette: {', '.join(mancano)})")
    check('testo a schermo detto (o etichetta)', '0 non detti', f"{len(non_detti)} su {len(voci)}", not non_detti)
    check('testo riformulato con le sue parole', 'da guardare', f"{len(riformulati)}", not riformulati, grave=False)
    dettagli += [f"- testo non detto: {t}" for t in non_detti]
    dettagli += [f"- riformulato (parole sue, ordine diverso): {t}" for t in riformulati]

    # materiali vietati (regia -> materiali_vietati)
    vietati = set(G.get('materiali_vietati', []))
    usati = []
    for x in G.get('inserti', []):
        for k in ('schermate',):
            usati += [Path(s['file']).name for s in x['dati'].get(k, [])]
        usati += [Path(x['dati'][k]).name for k in ('foto_prima', 'foto_dopo') if x['dati'].get(k)]
    if P.data('inserti.json').exists():
        usati += [Path(m).name for u in P.leggi('inserti.json') for m in u.get('materiali', [])]
    for m in R.get('scena', {}).get('momenti', []):
        for x in m.get('elementi', []):
            d = x.get('dati', {})
            usati += [Path(sc['file']).name for sc in d.get('schermate', []) if sc.get('file')]   # le «foto» generate non hanno file
            usati += [Path(d[k]).name for k in ('foto_prima', 'foto_dopo') if d.get(k)]
    proibiti = sorted({u for u in usati if u in vietati})
    check('materiali vietati usati', '0', f"{len(proibiti)} (vietati: {len(vietati)})", not proibiti)
    dettagli += [f"- materiale vietato: {u}" for u in proibiti]

    # SRT completo per YouTube (anche con i sottotitoli variante B)
    testo, n = C.srt(W, G['duration'])
    if scrivi_file:
        P.p('consegna').mkdir(exist_ok=True)
        (P.p('consegna') / f"{P.slug}.srt").write_text(testo, encoding='utf-8')
    parole_srt = sum(len(r.split()) for r in testo.split('\n')
                     if r.strip() and '-->' not in r and not r.strip().isdigit())
    check('SRT completo', f"{len(W)} parole", f"{parole_srt} parole, {n} battute", parole_srt >= 0.99 * len(W))

    # pannelli e testa: nei tagli "lato" la testa sta dal lato opposto al pannello
    if P.data('inquadratura.json').exists():
        from . import stile as S
        sotto = []
        for p in P.leggi('inquadratura.json')['pezzi']:
            if p['framing'].startswith('lato') and p.get('testa'):
                x0, _, x1, _ = p['testa']
                libero = (0, S.W - S.PANNELLO_W) if p['framing'].startswith('lato_sx') else (S.PANNELLO_W, S.W)
                if x0 < libero[0] - 10 or x1 > libero[1] + 10:
                    sotto.append(f"{ts(p['edit_in'])} {p['framing']}: testa {x0:.0f}-{x1:.0f} px, libero {libero}")
        check('testa sotto un pannello', '0', f"{len(sotto)}", not sotto)
        dettagli += [f"- {s}" for s in sotto]

    if scrivi_file:
        L = [f"# Controlli di contenuto: {P.slug}", "", "| controllo | atteso | misurato | esito |", "|---|---|---|---|"]
        L += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in righe]
        if dettagli:
            L += ["", "## Dettagli", ""] + dettagli
        P.controllo('contenuto.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    return righe


def _parole_mancanti(P, E, G):
    import difflib
    from .papere import norm
    from .grafica.piano import parole
    B = P.leggi('blocchi-testo.json', [])
    tok = lambda t: [norm(x) for x in t.replace('-', ' ').split() if norm(x)]
    ref = []
    for s, e, t in B:
        if t and any(sg['in'] - 0.05 <= s and e <= sg['in'] + sg['n'] / P.fps + 0.05 for sg in E['segmenti']):
            ref += tok(t)
    # le parole del montato con le correzioni: sotto i titoli i sottotitoli si
    # spengono apposta, quindi il confronto si fa sulle parole, non sui gruppi
    capw = [dict(w, t=x) for w in parole(P, P.regia()) for x in w['t'].replace('-', ' ').split()]
    hyp = [norm(w['t']) for w in capw]
    keep = [i for i, h in enumerate(hyp) if h]
    hyp = [hyp[i] for i in keep]
    out = []
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    for op, a, b, c, d in sm.get_opcodes():
        # "tieni la" contro "tienila": stesse lettere, grafia diversa
        if op == 'replace' and ''.join(ref[a:b]) == ''.join(hyp[c:d]):
            continue
        if op == 'delete' or (op == 'replace' and b - a > d - c):
            j = keep[min(c, len(keep) - 1)] if keep else 0
            t = capw[j]['s'] if capw else 0
            ctx = ' '.join(w['t'] for w in capw[max(0, j - 3):j + 3])
            out.append(f"{ts(t)}: manca «{' '.join(ref[a:b])}» — sottotitolo: «{ctx}»")
    return out, len(ref)


def _foglio_giunte(P, video, G_):
    out = P.controllo('giunte')
    out.mkdir(exist_ok=True)
    for f in out.glob('*.jpg'):
        f.unlink()
    for g in G_:
        for tag, t in (('a', g['t'] - 0.4), ('b', g['t'] + 0.4)):
            ffmpeg('-ss', f"{max(0, t):.3f}", '-i', video, '-frames:v', '1', '-vf', 'scale=320:-2',
                   out / f"g{g['i']:02d}{tag}.jpg")
    ffmpeg('-pattern_type', 'glob', '-i', str(out / '*.jpg'), '-filter_complex',
           'tile=8x' + str(-(-2 * len(G_) // 8)) + ':margin=4:padding=3', '-frames:v', '1',
           P.controllo('giunte.jpg'))

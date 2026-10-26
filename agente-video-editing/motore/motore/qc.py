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

from .progetto import Progetto, FPS, ts, ffmpeg
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
    check('frame rate', '30000/1001', v['r_frame_rate'], v['r_frame_rate'] == '30000/1001')
    check('pixel', 'yuv420p', v.get('pix_fmt'), v.get('pix_fmt') == 'yuv420p')
    tags = (v.get('color_primaries'), v.get('color_transfer'), v.get('color_space'))
    check('tag colore', 'bt709/bt709/bt709', '/'.join(str(x) for x in tags), tags == ('bt709',) * 3)
    check('audio', 'aac 48 kHz stereo',
          f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']} ch" if a else 'assente',
          bool(a) and a['codec_name'] == 'aac' and a['sample_rate'] == '48000' and a['channels'] == 2)

    nf = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets',
                         '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', str(path)],
                        capture_output=True, text=True).stdout.strip().split(',')[0]
    nf = int(nf or 0)
    check('frame', f"{E['frame']} (EDL)", nf, nf == E['frame'])
    da = float(a.get('duration', 0)) if a else 0
    check('durata audio', f"{E['durata']:.2f}s", f"{da:.2f}s", abs(da - E['durata']) < 0.08)

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
    fermi = [t for t in fermi if not any(a <= t <= b for a, b in pieni)]
    check('immagine ferma', 'nessun tratto oltre 2,5 s (schede escluse)',
          ', '.join(ts(t) for t in fermi) or 'nessuno', not fermi, grave=False)

    conf = [c for c in G['cards'] if c.get('conflitto')]
    for k in ('opening', 'chip'):
        if G.get(k) and G[k].get('conflitto'):
            conf.append(G[k])
    marg = [c.get('margine_volto') for c in G['cards'] if c.get('margine_volto') is not None]
    check('card sul volto', '0 sovrapposte', f"{len(conf)} sovrapposte, margine minimo "
          f"{min(marg):.0f} px" if marg else f"{len(conf)} sovrapposte", not conf and bool(marg))

    sag = len(list(P.p('data', 'sagome').glob('*.png'))) if P.p('data', 'sagome').is_dir() else 0
    att = sum(int(round((c['e'] - c['s']) * FPS)) for c in G['capitoli'] if c['dietro'])
    check('sagome titoli dietro', f"{att} frame", sag, sag >= att * 0.98 if att else True)

    words = P.leggi('parole-montato.json')
    nasc = [(c['s'] + 0.1, c['e'] - 0.1) for c in G['capitoli']]
    if G.get('closing'):
        nasc.append((G['closing']['s'] + 0.3, G['closing']['e']))
    vis = [w for w in words if not any(x <= w[0] < y for x, y in nasc)]
    # una parola e a schermo se sta in un sottotitolo, oppure se la mostra gia la
    # grafica (scena di parole, citazione): li i sottotitoli si spengono apposta
    capw = sum(len(c['words']) for c in G['captions'])
    capw += sum(len(c.get('parole_t', [])) for c in G.get('scene', []) + G['cards'])
    check('copertura sottotitoli', '≥ 99% delle parole', f"{capw}/{len(vis)}",
          len(vis) > 0 and capw >= 0.99 * len(vis))

    # le parole dei sottotitoli contro i blocchi trascritti da soli: la copertura
    # sopra confronta i sottotitoli con la stessa trascrizione da cui vengono, e
    # non vede una parola che whisper ha perso ("ti senti nuovo" per "ti senti di nuovo")
    mancanti, nref = _parole_mancanti(P, E, G)
    check('parole perse', '≤ 1% rispetto ai blocchi', f"{len(mancanti)} su {nref}",
          nref > 0 and len(mancanti) <= 0.01 * nref, grave=len(mancanti) > 0.01 * nref)
    if mancanti:
        righe[-1] = righe[-1][:3] + ('AVVISO' if len(mancanti) <= 0.01 * nref else 'ERRORE',)

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


def _parole_mancanti(P, E, G):
    import difflib
    from .papere import norm
    from .grafica.piano import parole
    B = P.leggi('blocchi-testo.json', [])
    tok = lambda t: [norm(x) for x in t.replace('-', ' ').split() if norm(x)]
    ref = []
    for s, e, t in B:
        if t and any(sg['in'] - 0.05 <= s and e <= sg['in'] + sg['n'] / FPS + 0.05 for sg in E['segmenti']):
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

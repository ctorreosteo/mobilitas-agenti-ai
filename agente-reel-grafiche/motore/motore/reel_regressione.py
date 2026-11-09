"""Regressione dell'agente reel-grafiche (fase 5, 04/11/2026): l'esempio fisso AD_CERVICALGIA_AI-Barontini.

    ./mve reel-regressione [--riferimento]

Il caso sta in `campionario/regressione/reel/AD_CERVICALGIA_AI-Barontini/`:
- `caso.json`: da dove viene il video (inbox/) e le animazioni 3D segnate;
- `piano.json`: il piano approvato da Riccardo (fasi 1-4), congelato;
- `verifiche.json`: le letture di Vision gia guardate (due gruppi di letture sbagliate);
- `riferimento/`: cosa deve uscire: misure della radiografia, fotogrammi (md5 di ogni fotogramma), audio, controlli,
  e il video di riferimento per misurare le differenze.

Il comando rifà tutto da zero con il procedimento di adesso, in uno slug temporaneo `videos/_regressione-reel-<caso>/`:
radiografia, 3D dal caso, controllo del piano, approvazione del piano congelato (solo se l'md5 e quello del caso),
render e controlli. Poi confronta con il riferimento ed esce con:
- OK: radiografia uguale, video uguale fotogramma per fotogramma, audio uguale, 0 errori;
- CAMBIATO: tutto passa ma qualcosa e diverso dal riferimento (si guarda `ultimo/ESITO.md`; se il cambio e voluto e
  guardato, si rifà il riferimento con --riferimento);
- ROTTO: una tappa fallisce o i controlli danno errori -> si corregge subito.
L'esito resta in `ultimo/`; lo slug temporaneo e .lavoro/<slug>/ si cancellano alla fine.
Si lancia dopo ogni modifica al motore dei reel (reel*.py, reel_dom.mjs) o ai modelli *_ads*.
"""
import datetime
import json
import shutil
import subprocess
import sys

from . import reel_comune as C

CASO = 'AD_CERVICALGIA_AI-Barontini'
R = C.AGENTE / 'campionario' / 'regressione' / 'reel' / CASO


BLOCCO = 8                        # i livelli delle grafiche si confrontano anche a blocchi di 8x8 pixel (media RGBA)
ARROTONDAMENTO_BLOCCHI = 2        # differenza massima fra le medie dei blocchi (0-255) che conta come arrotondamento
# Tolleranza per il rumore di render (Riccardo, 05/11/2026: «sì a una tolleranza per il rumore della GPU, misurala e scrivila»).
# Misura del 05/11/2026 (report/2026-11-05-fase6-dati/rumore-render.md): la chiusura del caso, resa 3 volte di fila, esce identica
# bit per bit, ma differisce dal riferimento del 04/11 in 33 fotogrammi con blocchi 8x8 fino a 6 livelli (bordi di logo, bottone e
# freccia spostati di una frazione di pixel; SSIM del video su quei fotogrammi >= 0,9977); alle 10:35 erano 234 fotogrammi, sempre
# fino a 6 livelli (SSIM minimo 0,9961). Uno spostamento vero di 1 pixel dà blocchi da 21 a 31 livelli, di 2 pixel da 43 a 61.
# Soglia: fino a 8 livelli è rumore di render (non conta), oltre è un cambiamento vero; il video deve restare a SSIM >= 0,995.
RUMORE_BLOCCHI = 8
RUMORE_SSIM_VIDEO = 0.995


def _livello(mov):
    """md5 di ogni fotogramma del MOV e medie RGBA a blocchi di 8x8 (uint8): bastano per distinguere gli
    arrotondamenti della GPU (1 livello su pochi pixel) da un cambio vero, senza tenere i MOV (300 MB l'uno)"""
    import numpy as np
    W, H = C.W, C.H
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(mov), '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], stdout=subprocess.PIPE)
    import hashlib
    md5, blocchi = [], []
    while True:
        b = p.stdout.read(W * H * 4)
        if len(b) < W * H * 4:
            break
        md5.append(hashlib.md5(b).hexdigest())
        a = np.frombuffer(b, np.uint8).reshape(H // BLOCCO, BLOCCO, W // BLOCCO, BLOCCO, 4).mean((1, 3))
        blocchi.append(np.round(a).astype(np.uint8))
    p.wait()
    return md5, np.stack(blocchi)


def _diff_max(a, b, frames):
    """differenza massima (RGB, 0-255) fra due video sui fotogrammi dati, in streaming"""
    import numpy as np
    m = 0
    for k, (x, y) in enumerate(zip(C.fotogrammi_rgb(a), C.fotogrammi_rgb(b))):
        if k in frames:
            m = max(m, int(np.abs(x.astype(np.int16) - y.astype(np.int16)).max()))
    return m


def _framemd5(video):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-map', '0:v', '-f', 'framemd5', '-'],
                         capture_output=True, text=True, check=True).stdout
    return [l.split(',')[-1].strip() for l in out.split('\n') if l and not l.startswith('#')]


def _misure(Rd):
    """le misure della radiografia che devono restare uguali"""
    return {'fotogrammi': Rd['fotogrammi'], 'tagli': Rd['tagli'],
            'inquadrature': [[s['n'], s['f0'], s['f1'], s['schema'], [[f['x'], f['y'], f['w'], f['h'], f['raggio']] for f in s['finestre']]]
                             for s in Rd['inquadrature']],
            'sottotitoli': [[o['n'], o.get('fotogrammi_misurati'), o['somiglianza'] >= 0.8] for o in Rd['sottotitoli']['righe']],
            'altezza_lettere_px': Rd['sottotitoli']['fascia']['altezza_lettere_px'],
            'voce_parole': len(Rd['voce']['parole']), 'voce_differenze': len(Rd['voce']['differenze_srt']),
            'voce_tempi': [[p['parola'], p['a'], p['a_inviluppo']] for p in Rd['voce']['parole']],
            'numeri_detti': Rd['numeri_detti'], 'md5_audio': Rd['md5_audio']}


def _controlli(K):
    return {'errori': K['errori'], 'audio_identico': K['audio']['identico'],
            'grafiche': {n: {'visibile': g['visibile'], 'testo_ingombro': g.get('testo_ingombro'),
                             'testi_scritti': g.get('pagina', {}).get('testi_scritti')} for n, g in K['grafiche'].items()},
            'ssim': {k: round(v['medio'], 5) for k, v in K['ssim'].items() if v},
            'vision': {'fotogrammi_letti': K['vision']['fotogrammi_letti']}}


def regressione(riferimento=False):
    from . import reel_flusso as F, reel_radiografia_base as RG, reel_piano_base as AP, reel_rendi as AR
    caso = C.leggi(R / 'caso.json')
    slug = f"_regressione-reel-{CASO}"
    D = C.cartella(slug)
    if D.exists():
        shutil.rmtree(D)
    D.mkdir(parents=True)
    U = R / 'ultimo'
    if U.exists():
        shutil.rmtree(U)
    U.mkdir(parents=True)
    esito = {'caso': CASO, 'data': f"{datetime.datetime.now():%d/%m/%Y %H:%M}", 'tappe': {}, 'differenze': []}
    stato = 'OK'
    try:
        C.scrivi(D / 'reel.json', {'_cosa': 'slug temporaneo della regressione dei reel (si cancella alla fine)', 'slug': slug,
                                  'creato': esito['data'], 'sorgente': caso['sorgente']})
        RG.radiografia(slug)
        esito['tappe']['radiografia'] = 'ok'
        RG.segna_3d(slug, ','.join(str(n) for n in caso['animazioni_3d']), nota=caso.get('nota_3d', ''))
        shutil.copy2(R / 'piano.json', D / 'piano.json')
        if C.md5_file(D / 'piano.json') != caso['md5_piano']:
            raise RuntimeError("piano.json del caso diverso da quello congelato (md5)")
        AP.piano(slug)
        esito['tappe']['piano'] = 'ok'
        F.approva(slug, 'piano', da=f"regressione: piano congelato del caso {CASO} (approvato da Riccardo nelle fasi 1-4)")
        if (R / 'verifiche.json').exists():
            shutil.copy2(R / 'verifiche.json', D / 'verifiche.json')
        AR.rendi(slug)
        esito['tappe']['rendi'] = 'ok'
    except SystemExit as e:
        if e.code not in (None, 0):
            stato = 'ROTTO'
            esito['errore'] = str(e.code)
    except Exception as e:
        stato = 'ROTTO'
        esito['errore'] = f"{type(e).__name__}: {e}"
    if stato == 'OK':
        Rd = C.leggi(D / 'radiografia.json')
        K = C.leggi(D / 'controlli' / 'controlli.json')
        full = D / 'anteprime' / f"{slug}_lavoro-intero.mp4"
        mis, ctl, fm = _misure(Rd), _controlli(K), _framemd5(full)
        livelli = {n: _livello(C.AGENTE / g['mov']) for n, g in K['grafiche'].items()}
        shutil.copy2(D / 'controlli' / 'controlli.md', U / 'controlli.md')
        shutil.copy2(D / 'radiografia.md', U / 'radiografia.md')
        if (D / 'piano' / 'tavola.jpg').exists():
            shutil.copy2(D / 'piano' / 'tavola.jpg', U / 'tavola.jpg')
        if (D / 'controlli' / 'cifre-da-guardare').exists():          # i ritagli da guardare restano (lo slug si cancella)
            shutil.copytree(D / 'controlli' / 'cifre-da-guardare', U / 'cifre-da-guardare')
        if K['errori']:
            stato = 'ROTTO'
            esito['errore'] = f"{len(K['errori'])} errori nei controlli"
        if riferimento:
            RF = R / 'riferimento'
            if RF.exists():
                shutil.rmtree(RF)
            RF.mkdir()
            C.scrivi(RF / 'radiografia.json', mis)
            C.scrivi(RF / 'controlli.json', ctl)
            (RF / 'fotogrammi.md5').write_text('\n'.join(fm) + '\n')
            import numpy as np
            for n, (md5, bl) in livelli.items():
                np.savez_compressed(RF / f"livello-{n}.npz", md5=np.array(md5), blocchi=bl)
            shutil.copy2(full, RF / 'riferimento.mp4')
            C.scrivi(RF / 'video.json', {'md5_video': C.md5_file(full), 'md5_audio': K['audio']['md5_finale'], 'fotogrammi': len(fm),
                                         'data': esito['data']})
            esito['riferimento'] = 'rifatto da questa esecuzione'
        else:
            RF = R / 'riferimento'
            mr, cr = C.leggi(RF / 'radiografia.json'), C.leggi(RF / 'controlli.json')
            fr = (RF / 'fotogrammi.md5').read_text().split()
            vr = C.leggi(RF / 'video.json')
            for k in mr:
                if mis.get(k) != mr[k]:
                    esito['differenze'].append(f"radiografia: «{k}» diverso dal riferimento")
            for k in cr:
                a, b = ctl.get(k), cr[k]
                if k == 'vision':                 # i gruppi di letture sbagliate cambiano con la codifica: non si confrontano
                    a, b = {'fotogrammi_letti': a['fotogrammi_letti']}, {'fotogrammi_letti': b['fotogrammi_letti']}
                if a != b:
                    esito['differenze'].append(f"controlli: «{k}» diverso dal riferimento")
            # Vision: le letture sbagliate di Vision cambiano da un'esecuzione all'altra (la codifica cambia di poco i pixel):
            # conta solo che non resti niente da guardare
            esito['vision_gruppi'] = [q['chiave'] for q in K['vision']['guardate']]
            if K['vision']['da_guardare']:
                esito['differenze'].append(f"Vision: {len(K['vision']['da_guardare'])} letture nuove da guardare (ultimo/cifre-da-guardare/): "
                                           + ', '.join(q['chiave'] for q in K['vision']['da_guardare']))
            diversi = [i for i, (a, b) in enumerate(zip(fm, fr)) if a != b]
            if len(fm) != len(fr):
                esito['differenze'].append(f"video: {len(fm)} fotogrammi, riferimento {len(fr)}")
            # i livelli delle grafiche: identici, arrotondati o cambiati
            import numpy as np
            arrotondate, spiegati = [], set()
            for n, (md5, bl) in livelli.items():
                if not (RF / f"livello-{n}.npz").exists():
                    esito['differenze'].append(f"grafica {n}: manca nel riferimento")
                    continue
                z = np.load(RF / f"livello-{n}.npz")
                rmd5 = list(z['md5'])
                if len(md5) != len(rmd5):
                    esito['differenze'].append(f"grafica {n}: {len(md5)} fotogrammi, riferimento {len(rmd5)}")
                    continue
                dif = [i for i, (a, b) in enumerate(zip(md5, rmd5)) if a != b]
                if not dif:
                    continue
                dm = int(np.abs(bl[dif].astype(np.int16) - z['blocchi'][dif].astype(np.int16)).max())
                f0 = K['grafiche'][n]['visibile'][0][0] if K['grafiche'][n]['visibile'] else 0
                g0 = [g for g in C.leggi(R / 'piano.json')['grafiche'] if g['nome'] == n][0]['f0']
                if dm <= ARROTONDAMENTO_BLOCCHI:
                    arrotondate.append(f"{n}: {len(dif)} fotogrammi del livello con differenze di arrotondamento (blocchi 8x8 al massimo {dm})")
                    spiegati |= {g0 + i for i in dif}
                elif dm <= RUMORE_BLOCCHI:
                    arrotondate.append(f"{n}: {len(dif)} fotogrammi del livello con rumore di render (blocchi 8x8 al massimo {dm}, soglia "
                                       f"{RUMORE_BLOCCHI}: spostamenti sotto il pixel; 1 pixel vero ne dà almeno 21), dal fotogramma {g0 + dif[0]}")
                    spiegati |= {g0 + i for i in dif}
                else:
                    esito['differenze'].append(f"grafica {n}: {len(dif)} fotogrammi del livello cambiati (blocchi 8x8 fino a {dm} livelli), "
                                               f"dal fotogramma {g0 + dif[0]} del video")
            if arrotondate:
                esito['arrotondamenti'] = arrotondate
            if diversi:
                s = AR.ssim(full, RF / 'riferimento.mp4', diversi, L=C.lavoro(slug), nome='ssim-regressione')
                esito['video_diversi'] = {'fotogrammi': len(diversi), 'da': diversi[0], 'a': diversi[-1], 'ssim': s['medio'], 'ssim_min': s['minimo']}
                msg = (f"video: {len(diversi)} fotogrammi diversi dal riferimento ({diversi[0]}-{diversi[-1]}), SSIM su quelli "
                       f"{s['medio']:.5f} (minimo {s['minimo']:.5f})")
                # la codifica x264 propaga una differenza in avanti (e fino a qualche fotogramma indietro, per i B): un fotogramma diverso del
                # video e spiegato se, da quando la grafica arrotondata cambia, non ci sono differenze vere nei livelli
                inizio = min(spiegati) if spiegati else None
                if (inizio is not None and min(diversi) >= inizio - 16 and not [d for d in esito['differenze'] if d.startswith('grafica')]
                        and s['minimo'] >= RUMORE_SSIM_VIDEO):
                    esito['video_arrotondato'] = msg + ": conseguenza degli arrotondamenti dei livelli (la codifica li propaga)"
                else:
                    esito['differenze'].append(msg)
            esito['fotogrammi_identici'] = len(fm) - len(diversi)
            esito['md5_video_uguale'] = C.md5_file(full) == vr['md5_video']
            if K['audio']['md5_finale'] != vr['md5_audio']:
                esito['differenze'].append('audio diverso dal riferimento')
            if esito['differenze'] and stato == 'OK':
                stato = 'CAMBIATO'
            if esito['differenze'] or esito.get('arrotondamenti'):
                # per guardare le differenze: il video e i livelli di questa esecuzione restano in ultimo/
                shutil.copy2(full, U / 'video.mp4')
                for n, (md5, bl) in livelli.items():
                    np.savez_compressed(U / f"livello-{n}.npz", md5=np.array(md5), blocchi=bl)
        esito['fotogrammi'] = len(fm)
    esito['stato'] = stato
    C.scrivi(U / 'esito.json', esito)
    L = [f"# Regressione dei reel: {CASO}", '', f"{esito['data']}: **{stato}**", '']
    L += [f"- tappa {k}: {v}" for k, v in esito['tappe'].items()]
    if esito.get('errore'):
        L.append(f"- ERRORE: {esito['errore']}")
    if 'fotogrammi_identici' in esito:
        L.append(f"- video: {esito['fotogrammi_identici']} fotogrammi su {esito['fotogrammi']} identici al riferimento; "
                 f"md5 del file {'uguale' if esito['md5_video_uguale'] else 'diverso'}")
    L += [f"- DIVERSO: {d}" for d in esito['differenze']]
    if esito.get('vision_gruppi') is not None:
        L.append(f"- Vision: letture sbagliate gia guardate in questa esecuzione: {', '.join(esito['vision_gruppi']) or 'nessuna'}")
    for a in esito.get('arrotondamenti', []):
        L.append(f"- arrotondamento (non conta): {a}")
    if esito.get('video_arrotondato'):
        L.append(f"- video (non conta): {esito['video_arrotondato']}")
    if esito.get('riferimento'):
        L.append(f"- riferimento: {esito['riferimento']}")
    (U / 'ESITO.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    print('\n'.join(L))
    # lo slug temporaneo e la sua cartella di lavoro si cancellano (l'esito resta in ultimo/)
    shutil.rmtree(D, ignore_errors=True)
    shutil.rmtree(C.AGENTE / '.lavoro' / slug, ignore_errors=True)
    if stato == 'ROTTO':
        sys.exit(1)

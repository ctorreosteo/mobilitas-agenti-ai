"""I sottotitoli impressi non si toccano (Riccardo, 07/11/2026). Controllo automatico che blocca il render.

Regola: i sottotitoli sono quelli impressi nel montaggio. Non si ritagliano, non si ricolorano, non si spostano, non si
ingrandiscono, non si sfocano, non si scuriscono, non si ridisegnano; non se ne scrivono di nuovi. Per ogni fotogramma con
una riga di sottotitolo vale una delle due:

(a) VIDEO FERMO: la fascia della riga (il riquadro delle lettere letto da Vision, con l'ombra) è uguale all'originale.
    Si misura PRIMA della codifica, come le verifiche dello zoom: il video base della sovrapposizione è identico
    all'originale nella fascia (bit per bit) e l'alfa delle nostre grafiche lì non supera ALFA_LIBERA (niente velo, ombra,
    bagliore o bordo). Sul video finito resta un controllo largo (media ≤ MEDIA_FINALE_MAX), contro gli errori della catena.
    Perché non solo sul finito: la codifica perde di più nei fotogrammi in cui spende i bit su una grafica che si muove
    (AD_CERVICALGIA, fumo e equazione animata: fascia non toccata fino a 5,3 di media), mentre i ritocchi veri danno ≥ 37
    (lettere rimesse sul frontman, 07/11/2026) o si vedono nell'alfa.
(b) GRAFICA PIENA: la fascia è coperta del tutto dalle nostre grafiche (alfa ≥ 250 su almeno il 99,5% del riquadro: il
    controllo con le coordinate, niente mezza riga tagliata da un bordo) E, nella parte di video che resta visibile (dove
    l'alfa delle grafiche è < 128), Apple Vision non legge nessuna parola della riga di quel momento (nessuna copia
    spostata visibile).

Tutto il resto è un errore: fascia velata, sfocata, scurita, coperta a metà, o copia visibile.
"""
import re
import shutil
import subprocess

import numpy as np

from . import reel_comune as C
from .reel_comune import W, H

ALFA_LIBERA = 6
MEDIA_FINALE_MAX = 12.0
COPERTA_ALFA = 250
COPERTA_QUOTA = 0.995
OCR_PASSO = 3


def righe(R):
    """[(f0, f1, riquadro con l'ombra, testo)] delle righe di sottotitolo lette dalla radiografia"""
    out = []
    for rg in (R.get('sottotitoli') or {}).get('righe') or []:
        fm, bx = rg.get('fotogrammi_misurati'), rg.get('box_lettere')
        if not fm or not bx:
            continue
        # le lettere con il loro bordo e l'ombra dura (4 px in basso a destra); sopra non c'è ombra: 4 px (con 14 px si toccava
        # il bordo della finestra del montaggio, che non è un sottotitolo)
        q = [max(0, bx[0] - 6), max(0, bx[1] - 4), min(W, bx[2] + 10), min(H, bx[3] + 10)]
        out.append((fm[0], fm[1], q, rg.get('srt') or rg.get('letto') or ''))
    return out


def per_fotogramma(R):
    d = {}
    for a, b, q, t in righe(R):
        for f in range(a, b + 1):
            d.setdefault(f, []).append((q, t))
    return d


def copertura(alfa_frame, riquadri):
    """quota del riquadro più scoperto con alfa ≥ COPERTA_ALFA (0-1) e alfa massimo, per un fotogramma RGBA del MOV"""
    q_min, massimo = 1.0, 0.0
    for q, _ in riquadri:
        a = alfa_frame[q[1]:q[3], q[0]:q[2]]
        if a.size == 0:
            continue
        q_min = min(q_min, float((a >= COPERTA_ALFA).mean()))
        massimo = max(massimo, float(a.max()))
    return q_min, massimo


def _parole(t):
    return {w for w in re.findall(r"[a-zàèéìòù]+", t.lower()) if len(w) >= 3}


def controlla(final, V, R, coperture, movs, fps, L, Vb=None):
    """coperture: {f: (quota coperta, alfa massimo)} sui riquadri delle righe (dalle nostre grafiche); Vb: il video base della
    sovrapposizione se non è l'originale (zoom);
    movs: [(f0 della grafica, fotogrammi, mov)] per mascherare le grafiche prima di Vision. Ritorna il verdetto"""
    pf = per_fotogramma(R)
    nf = R['fotogrammi']
    a_ok, b_cand, err = [], [], []
    p1 = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(V), '-map', '0:v:0', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(final), '-map', '0:v:0', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'], stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(Vb), '-map', '0:v:0', '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                          stdout=subprocess.PIPE) if Vb and str(Vb) != str(V) else None
    misure = {}
    f = 0
    while True:
        x, y = p1.stdout.read(W * H), p2.stdout.read(W * H)
        z = p3.stdout.read(W * H) if p3 else None
        if len(x) < W * H or len(y) < W * H:
            break
        if f in pf:
            X = np.frombuffer(x, np.uint8).reshape(H, W).astype(np.int16)
            Y = np.frombuffer(y, np.uint8).reshape(H, W).astype(np.int16)
            Z = np.frombuffer(z, np.uint8).reshape(H, W).astype(np.int16) if z and len(z) == W * H else None
            peggio, base_uguale = (0.0, 0.0), True
            for q, _ in pf[f]:
                d = np.abs(X[q[1]:q[3], q[0]:q[2]] - Y[q[1]:q[3], q[0]:q[2]])
                if d.size:
                    peggio = max(peggio, (float(d.mean()), float(np.percentile(d, 99.5))))
                if Z is not None and not np.array_equal(X[q[1]:q[3], q[0]:q[2]], Z[q[1]:q[3], q[0]:q[2]]):
                    base_uguale = False
            misure[f] = peggio
            _, alfa_max = coperture.get(f, (0.0, 0.0))
            if base_uguale and alfa_max <= ALFA_LIBERA and peggio[0] <= MEDIA_FINALE_MAX:
                a_ok.append(f)
            else:
                cq, _ = coperture.get(f, (0.0, 0.0))
                if cq >= COPERTA_QUOTA:
                    b_cand.append(f)
                else:
                    err.append((f, round(peggio[0], 1), round(cq, 3), alfa_max))
        f += 1
    p1.wait(); p2.wait()
    if p3:
        p3.wait()
    # (b) Vision sulla parte di video visibile (le nostre grafiche mascherate in nero)
    letture = []
    ocr = sorted(set(b_cand[::OCR_PASSO]) | {g[0] for g in C_corse(b_cand)} | {g[1] for g in C_corse(b_cand)}) if b_cand else []
    if ocr:
        from PIL import Image
        oc = L / 'ocr-sottotitoli'
        if oc.exists():
            shutil.rmtree(oc)
        oc.mkdir(parents=True)
        for i in range(0, len(ocr), 25):            # con 120 termini il filtro select di ffmpeg esaurisce la memoria
            lotto = ocr[i:i + 25]
            sel = '+'.join(f'eq(n\\,{k})' for k in lotto)
            tmp = oc / 'f'
            tmp.mkdir(exist_ok=True)
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(final), '-vf', f"select='{sel}',scale=in_color_matrix=bt709:in_range=tv:out_range=full",
                            '-fps_mode', 'passthrough', '-frame_pts', '1', str(tmp / 'f%05d.png')], check=True)
            for k in lotto:
                p = tmp / f'f{k:05d}.png'
                if not p.exists():
                    continue
                im = np.asarray(Image.open(p).convert('RGB')).copy()
                for g0, n_g, mov in movs:
                    j = k - g0
                    if j < 0 or j >= n_g:
                        continue          # solo le grafiche a schermo in quel fotogramma
                    # salto diretto al fotogramma (i MOV delle grafiche sono tutti fotogrammi chiave): niente decodifica dall'inizio
                    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{j / fps:.4f}', '-i', str(mov), '-frames:v', '1', '-vf', 'format=rgba',
                                        '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], capture_output=True).stdout
                    if len(b) == W * H * 4:
                        al = np.frombuffer(b, np.uint8)[3::4].reshape(H, W)
                        im[al >= 128] = 0
                Image.fromarray(im).save(p)
            r = C.vision(tmp, L / 'ocr-sottotitoli.json')
            for nome, obs in r.items():
                k = int(re.search(r'(\d+)', nome).group(1))
                parole = set().union(*(_parole(t) for _, t in pf.get(k, [])))
                for o in obs:
                    comuni = _parole(o['t']) & parole
                    if comuni:
                        letture.append({'f': k, 'letto': o['t'], 'parole': sorted(comuni)})
            shutil.rmtree(tmp)
        shutil.rmtree(oc, ignore_errors=True)
    letti = {e['f'] for e in letture}
    b_ok = [f for f in b_cand if not any(abs(f - g) <= OCR_PASSO for g in letti)]
    errori = []
    for a_, b_ in C_corse([e[0] for e in err]):
        es = [e for e in err if a_ <= e[0] <= b_]
        errori.append(f"sottotitoli toccati nei fotogrammi {a_}-{b_} ({(a_) / fps:.2f}–{(b_ + 1) / fps:.2f} s): la fascia non resta "
                      f"libera (alfa delle grafiche fino a {max(e[3] for e in es):.0f}, video finito diverso fino a {max(e[1] for e in es)} di media) "
                      f"e le grafiche non la coprono del tutto (coperta al {min(e[2] for e in es) * 100:.0f}%): niente velo, sfocatura o mezza riga")
    for e in letture[:10]:
        errori.append(f"sottotitolo visibile fuori posto al fotogramma {e['f']}: Vision legge «{e['letto']}» nella parte di video visibile "
                      f"({', '.join(e['parole'])})")
    return {'fotogrammi_con_sottotitoli': len(pf), 'misurati': len(misure), 'a_fascia_uguale': len(a_ok), 'b_coperta': len(b_ok),
            'b_vision_letti': len(ocr), 'senza_sottotitoli': [[round(a_ / fps, 3), round((b_ + 1) / fps, 3)] for a_, b_ in C_corse(b_ok)],
            'senza_sottotitoli_s': round(len(b_ok) / fps, 2), 'errori': errori, 'letture': letture[:20],
            'soglie': {'alfa_libera': ALFA_LIBERA, 'media_finale_max': MEDIA_FINALE_MAX, 'coperta_alfa': COPERTA_ALFA, 'coperta_quota': COPERTA_QUOTA},
            'come': __doc__.split('\n\n')[1].strip()}


def C_corse(fs):
    out = []
    for f in sorted(fs):
        if out and f == out[-1][1] + 1:
            out[-1][1] = f
        else:
            out.append([f, f])
    return out

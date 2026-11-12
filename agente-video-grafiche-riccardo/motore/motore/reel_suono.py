"""Effetti sonori sotto le grafiche importanti (agente reel-grafiche, fase 6, 05/11/2026).

Regola di Riccardo (05/11/2026): effetti dalla libreria `libreria/sfx` (Pixabay, licenza in CREDITS.md), a volume
basso, ben sotto la voce, solo sulle entrate delle grafiche importanti (non sulle micro-grafiche). Voce e musica
restano quelle originali, e si dimostra; per ogni reel c'è anche la versione «senza effetti sonori».

Nel piano, sulla grafica: `"suono": {"file": "whoosh-short.mp3", "db": -20, "anticipo": 0.05}`:
- `db`: livello dell'effetto rispetto alla voce (RMS dell'effetto nella sua parte forte contro RMS della voce
  parlata), al massimo -12 dB; di solito -18…-24;
- l'effetto parte sul primo fotogramma visibile della grafica meno `anticipo` secondi (default 0).

Come si fa e come si dimostra:
1. l'audio originale e gli effetti si decodificano in float alla frequenza e ai canali dell'originale;
2. mix = originale + somma degli effetti con il guadagno calcolato; picco sotto -1 dBFS (se no, gli effetti si
   abbassano);
3. si codifica in AAC 256 kb/s (l'originale è AAC: una codifica in più è inevitabile quando si aggiunge un suono)
   e si mette accanto al video già fatto, che si copia (`-c:v copy`);
4. **prova**: si decodifica il file finale, si tolgono gli effetti (stessa traccia, stesso guadagno) e si confronta
   con l'originale: il residuo (RMS) deve essere al livello del solo rumore di codifica, cioè quello che resta
   ricodificando l'originale da solo con lo stesso codificatore. Si misura anche lo scarto in campioni
   (correlazione) e il guadagno: devono essere 0 e 1;
5. la versione «senza effetti» ha l'audio copiato: md5 del flusso identico all'originale.
"""
import json
import subprocess

import numpy as np

from . import reel_comune as C

SFX = C.AGENTE / 'libreria' / 'sfx'
DB_MAX = -12.0
BITRATE = '256k'


def _decodifica(f, sr, ch):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-map', '0:a:0', '-f', 'f32le', '-ac', str(ch), '-ar', str(sr), '-'],
                       capture_output=True, check=True).stdout
    return np.frombuffer(b, np.float32).reshape(-1, ch).astype(np.float64)


def _rms_db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


def livello_voce(a, sr):
    """RMS (dB) del parlato: media dei blocchi da 400 ms sopra -45 dBFS"""
    m = a.mean(1)
    n = int(0.4 * sr)
    k = len(m) // n
    r = np.sqrt((m[:k * n].reshape(k, n) ** 2).mean(1) + 1e-12)
    db = 20 * np.log10(r)
    att = r[db > -45]
    return float(20 * np.log10(np.sqrt(np.mean(att ** 2)))) if len(att) else -30.0


def _parte_forte(x, sr):
    """RMS (dB) dell'effetto nella sua parte forte: blocchi da 50 ms entro 20 dB dal più forte"""
    m = x.mean(1)
    n = int(0.05 * sr)
    k = max(1, len(m) // n)
    r = np.sqrt((m[:k * n].reshape(k, n) ** 2).mean(1) + 1e-12)
    top = r.max()
    f = r[r >= top / 10]
    return float(20 * np.log10(np.sqrt(np.mean(f ** 2))))


def traccia_effetti(eventi, n, sr, ch, voce_db):
    """la traccia degli effetti (stessa lunghezza dell'originale) e il dettaglio per evento"""
    tr = np.zeros((n, ch))
    det = []
    for e in eventi:
        x = _decodifica(SFX / e['file'], sr, ch)
        db = min(float(e.get('db', -20)), DB_MAX)
        g = 10 ** ((voce_db + db - _parte_forte(x, sr)) / 20)
        # il picco dell'effetto cade sull'entrata della grafica (prova del 05/11/2026: il whoosh cinematico ha la parte
        # forte dopo ~1 s e arrivava in ritardo): si anticipa della distanza fra l'inizio del file e il blocco più forte
        m = x.mean(1); nb = int(0.05 * sr); kb = max(1, len(m) // nb)
        picco = float(np.argmax(np.sqrt((m[:kb * nb].reshape(kb, nb) ** 2).mean(1))) * 0.05)
        ant = min(picco, 1.5) if e.get('allinea', 'picco') == 'picco' else 0.0
        i0 = max(0, int(round((e['t'] - ant) * sr)))
        i1 = min(n, i0 + len(x))
        tr[i0:i1] += x[:i1 - i0] * g
        det.append({'grafica': e.get('grafica'), 'file': e['file'], 't': round(e['t'] - ant, 3), 'picco_s': round(picco, 2), 'db_sotto_voce': db,
                    'guadagno': round(g, 4), 'durata_s': round(len(x) / sr, 2)})
    return tr, det


def mixa(video_senza, orig, eventi, out, L):
    """out = video_senza (video copiato) + audio originale con gli effetti (AAC). Ritorna la prova."""
    pr = C.probe(orig)
    sr, ch = int(pr['audio']['sample_rate']), int(pr['audio']['channels'])
    a = _decodifica(orig, sr, ch)
    voce_db = livello_voce(a, sr)
    tr, det = traccia_effetti(eventi, len(a), sr, ch, voce_db)
    # si abbassano solo gli effetti, mai la voce. 07/11/2026: effetto per effetto, nel suo tratto. Prima la riduzione era una
    # sola per tutto il reel e, con un originale già a fondo scala (AD_CERV_26: picco +0,1 dB), azzerava tutti gli effetti.
    # Ora nel tratto di ogni effetto il picco del mix non supera quello dell'originale nello stesso tratto (o -1 dBFS, se
    # l'originale lì sta sotto): l'effetto si riduce solo quanto serve
    lim = 10 ** (-1 / 20)
    rids = []
    for d in det:
        i0 = max(0, int(round(d['t'] * sr))); i1 = min(len(a), i0 + int(round(d['durata_s'] * sr)) + 1)
        if i1 <= i0:
            continue
        aa, tt = a[i0:i1], tr[i0:i1].copy()
        tetto = max(lim, float(np.abs(aa).max()))
        r = 1.0
        if float(np.abs(aa + tt).max()) > tetto:
            lo, hi = 0.0, 1.0
            for _ in range(30):
                mid = (lo + hi) / 2
                if float(np.abs(aa + mid * tt).max()) <= tetto:
                    lo = mid
                else:
                    hi = mid
            r = lo
        tr[i0:i1] = tt * r
        d['riduzione_per_il_picco'] = round(r, 3)
        rids.append(r)
    rid = min(rids) if rids else 1.0
    mix = a + tr
    wav = L / 'mix.f32'
    wav.write_bytes(mix.astype(np.float32).tobytes())
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video_senza), '-f', 'f32le', '-ar', str(sr), '-ac', str(ch), '-i', str(wav),
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', BITRATE, '-movflags', '+faststart', str(out)], check=True)
    wav.unlink()
    # prova
    y = _decodifica(out, sr, ch)
    n = min(len(y), len(a))
    y, a2, tr2 = y[:n], a[:n], tr[:n]
    resto = y - tr2                      # il file finale senza gli effetti
    scarto = _scarto(resto.mean(1), a2.mean(1))
    gain = float(np.dot(resto.ravel(), a2.ravel()) / np.dot(a2.ravel(), a2.ravel()))
    res_db = _rms_db(resto - a2)
    # il rumore della sola codifica: l'originale ricodificato da solo con lo stesso codificatore
    rif = L / 'ricodifica.m4a'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(orig), '-map', '0:a:0', '-c:a', 'aac', '-b:a', BITRATE, str(rif)], check=True)
    z = _decodifica(rif, sr, ch)[:n]
    base_db = _rms_db(z - a2[:len(z)])
    rif.unlink()
    sig_db = _rms_db(a2)
    # quanto stanno sotto la voce, effetto per effetto (finestra dell'effetto)
    for d in det:
        i0 = int((d['t'] + d.get('picco_s', 0) - 0.3) * sr); i0 = max(0, i0); i1 = min(n, i0 + int(0.8 * sr))   # intorno al picco
        d['rms_effetto_db'] = round(_rms_db(tr2[i0:i1]), 1)
        d['rms_voce_stesso_tratto_db'] = round(_rms_db(a2[i0:i1]), 1)
    prova = {'frequenza': sr, 'canali': ch, 'voce_rms_db': round(voce_db, 1), 'segnale_rms_db': round(sig_db, 1),
             'scarto_campioni': scarto, 'guadagno_voce': round(gain, 5),
             'residuo_senza_effetti_db': round(res_db, 1), 'residuo_sotto_il_segnale_db': round(sig_db - res_db, 1),
             'rumore_della_sola_ricodifica_db': round(base_db, 1),
             'differenza_dal_rumore_di_codifica_db': round(res_db - base_db, 1),
             'riduzione_effetti_per_il_picco': round(rid, 3), 'picco_mix': round(20 * np.log10(np.abs(a + tr).max() + 1e-12), 2),
             'effetti': det, 'codifica': f"aac {BITRATE}"}
    prova['esito'] = bool(scarto == 0 and abs(gain - 1) < 0.01 and res_db - base_db < 3.0)
    return prova


def _scarto(x, y, m=2048):
    """lo scarto (campioni) che rende x più simile a y, entro ±m, sui primi 20 s"""
    n = min(len(x), len(y), 44100 * 20)
    x, y = x[:n], y[:n]
    best = (0, -1e18)
    for k in range(-m, m + 1, 1):
        if k >= 0:
            c = float(np.dot(x[k:], y[:n - k]))
        else:
            c = float(np.dot(x[:n + k], y[-k:]))
        if c > best[1]:
            best = (k, c)
    return best[0]


def eventi_dal_piano(P, visibili, fps):
    """[{t, file, db, grafica}] dalle grafiche con «suono»: t = primo fotogramma visibile - anticipo"""
    out = []
    for g in P['grafiche']:
        s = g.get('suono')
        if not s:
            continue
        vis = visibili.get(g['nome'])
        if not vis:
            continue
        # 07/11/2026 (palco): «dopo» = secondi dopo il primo fotogramma visibile (una trasformazione dentro il palco, per esempio
        # «tre benefici»: la scena nuova è l'entrata importante)
        out.append({'t': min(vis) / fps + float(s.get('dopo', 0)) - float(s.get('anticipo', 0)), 'file': s['file'], 'db': s.get('db', -20),
                    'grafica': g['nome']})
    return out


def controlla(P):
    err, avv = [], []
    manif = json.loads((SFX / 'manifest.json').read_text())
    files = {v['file'] for v in manif.values()}
    n = 0
    for g in P['grafiche']:
        s = g.get('suono')
        if not s:
            continue
        n += 1
        # giro 5: un'infografica sopra il video è una grafica importante anche se sta nel livello delle micro
        if g.get('modo') == 'micro' and g.get('catalogo') != 'infografica-sopra':
            err.append(f"{g['nome']}: effetto sonoro su una micro-grafica (solo sulle entrate delle grafiche importanti)")
        if s.get('file') not in files:
            err.append(f"{g['nome']}: effetto «{s.get('file')}» non è in libreria/sfx")
        if float(s.get('db', -20)) > DB_MAX:
            err.append(f"{g['nome']}: effetto a {s.get('db')} dB dalla voce (al massimo {DB_MAX}: ben sotto la voce)")
    grandi = sum(1 for g in P['grafiche'] if g.get('modo') != 'micro' or g.get('catalogo') == 'infografica-sopra')
    if n > grandi:
        err.append("più effetti che grafiche importanti")
    return err, avv

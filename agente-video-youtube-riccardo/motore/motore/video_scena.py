"""Fase `scena` (fase 6c, 28/10/2026): il video intero con la grafica dentro la scena.

Fino alla v2 il montato era "lui da un lato + pannello" e gli inserti si
sovrapponevano. Qui il montato pulito si ricompone dai **momenti** di
`regia.json` → `scena.momenti`: ogni momento e un pezzo contiguo del montato con
la sua camera viva, i suoi effetti di piatto e i suoi elementi, scritto come nel
campionario (`campionario/v2/campionario.json`) e costruito dallo stesso motore
(`scena.costruisci`). Fra un momento e l'altro non ci sono buchi: dove non serve
una grafica il momento ha solo la camera (lui a tutto schermo).

I B-roll restano quelli di `monta` (`regia.json` → `broll`): i loro fotogrammi si
prendono dal montato pulito di `monta`.

Uscite:
- `renders/<slug>_pulito.mp4`: il montato ricomposto (video) + la voce, al posto
  di quello di `monta`, cosi `finale` ci mette sopra chip e mix come sempre;
- `assets/mix-finale.wav`: voce + i suoni di tutti i momenti (gli stessi del
  campionario: libreria e sintesi) + i fruscii dei B-roll, -14 LUFS, in un mix solo
  (niente salti di volume fra un momento e l'altro);
- `data/scena.json`: i momenti risolti (tempi, modelli, testi a schermo, misure,
  controlli) per `qc`, per il report e per la revisione.

    ./mve scena <slug> [--solo 3,7]   (poi: finale, qc)
"""
import json
import os
import shutil
import subprocess
import sys

from .progetto import Progetto, ffmpeg
from . import scena as S


def _testi(x):
    """le parole che un elemento mette a schermo (per il controllo dei contenuti)"""
    d = x.get('dati', {})
    out = []
    for b in d.get('battute', []):
        out.append(' '.join(p['testo'] for p in b['parole']))
    for r in d.get('righe', []):
        if isinstance(r, dict) and 'parole' in r:
            out.append(' '.join(p['testo'] for p in r['parole']))
        elif isinstance(r, dict):                  # equazione: {op, testo}
            out.append(' '.join(t for t in (r.get('op'), r.get('testo')) if t))
        else:
            out.append(' '.join(p['testo'] for p in r))
    for p in d.get('parole', []):
        out.append(p['testo'])
    for c in d.get('card', []):
        out.append(c.get('titolo', c.get('testo', '')))
        if c.get('sotto'):
            out.append(c['sotto'])
    if d.get('titolo'):
        tt = d['titolo']
        if isinstance(tt, dict) and 'testo' in tt:
            out.append(tt['testo'])
        elif isinstance(tt, dict):                 # card accese: {occ, tit}
            out.append(' '.join(t for t in (tt.get('occ'), tt.get('tit')) if t))
        else:
            out.append(tt)
    for v in d.get('voci', []):
        if v.get('testo'):
            out.append(v['testo'])
        elif v.get('righe'):                       # fumetti
            out.append(' '.join(v['righe']))
    for t in d.get('etichette', []):
        out.append(t['testo'] if t.get('testo') else ' '.join(p['testo'] for p in t.get('parole', [])))
    for c in d.get('carte', []):                   # card con spessore; card accese {pre, chiave, dopo}
        if 'testo' in c:
            out.append(c['testo'].replace('*', '').replace('|', ' '))
        else:
            out.append(' '.join([c.get('pre', ''), c.get('chiave', '')] + list(c.get('dopo', []))).strip())
    if x['modello'] == 'frase_luce':
        out.append(' '.join(p['testo'] for p in d.get('parole', [])))
    if x['modello'] == 'frase_chiave':
        out.append(' '.join(p['testo'] for p in d.get('parole', [])))
    if x['modello'] == 'titolo_dietro':
        out.append(' '.join(d['linee']))
    for v in d.get('voci', []):
        if v.get('sotto'):
            out.append(v['sotto'])
    if x['modello'] == 'numero_dietro':
        out += [d.get('prefisso', ''), str(d['valore']), str(d.get('etichetta', '')).replace('\n', ' ')]
    if x['modello'] == 'confronto':
        out += ['PRIMA', 'DOPO']
    if x['modello'] in ('connettore',):
        out += [' '.join(d.get('sinistra', [])), ' '.join(d.get('destra', [])), (d.get('pp') or {}).get('testo', '')]
    return [t for t in out if t]


def _tessere(P, R, momenti):
    """i momenti e i B-roll devono coprire il montato senza buchi e senza sovrapposizioni"""
    fps, N = P.fps, P.leggi('edl.json')['frame']
    G = P.leggi('grafica.json')
    pezzi = [('broll', int(round(b['s'] * fps)), int(round(b['e'] * fps))) for b in G.get('broll', [])]
    for m in momenti:
        a, b = m['pezzi'][0]
        pezzi.append((m['id'], int(round(a * fps)), int(round(b * fps))))
    pezzi.sort(key=lambda p: p[1])
    cur = 0
    for nome, a, b in pezzi:
        if a != cur:
            sys.exit(f"scena: {'buco' if a > cur else 'sovrapposizione'} prima di «{nome}» (frame {cur} -> {a})")
        cur = b
    if cur != N:
        sys.exit(f"scena: i momenti finiscono a {cur} invece che a {N} frame")
    return pezzi


# zone della schermata finale lasciate libere per gli elementi di YouTube (px a 1920x1080):
# due riquadri video 16:9 e il pulsante iscriviti (tondo). Riccardo li posiziona in YouTube
# Studio sopra queste zone; qui dentro il motore non mette niente.
ZONE_FINE = [('video 1', 150, 360, 700, 394), ('video 2', 1070, 360, 700, 394), ('iscriviti', 850, 800, 220, 220)]


def schermata_finale(P, coda, ultimo, slug, out=None, png=None):
    """la coda di `durata` s dopo l'ultima parola: modello HyperFrames `fine_youtube` sopra
    l'ultimo fotogramma del montato (che scompare sotto il fondo in 10 frame). Controlli:
    logo e filo fuori dalle zone, dentro la zona sicura; nelle zone solo il fondo."""
    import hashlib
    import numpy as np
    from PIL import Image, ImageDraw
    fps = P.fps
    n = int(round(coda.get('durata', 12.0) * fps))
    lw = 860
    lh = round(lw * 676 / 4915)
    dati = {'logo': {'x': (1920 - lw) // 2, 'y': 150, 'larghezza': lw},
            'filo': {'x': 760, 'y': 150 + lh + 36, 'larghezza': 400}}
    spec = {'elementi': [{'modello': coda.get('modello', 'fine_youtube'), 's': 0.0, 'e': n / fps, 'pieno': True, 'prof': 0,
                          'dati': dati}], '_frames': n, '_fps': fps, 'mosso_hf': False}
    cart = S.LAVORO / slug / ('_coda' if out is None else '_coda-regressione')
    cart.mkdir(parents=True, exist_ok=True)
    d = S.strato_html(spec, 'davanti', cart / 'hf', {})
    mov = cart / 'coda.mov'
    h = hashlib.sha1((d / 'index.html').read_bytes()).hexdigest()[:10]
    seg = cart / 'coda.chiave'
    if not mov.exists() or not seg.exists() or seg.read_text() != h:
        S.render_strato(d, mov, P.fps_str, n)
        seg.write_text(h)
    # l'ultimo fotogramma del montato (yuv bt709 tv -> rgb pieno, come lo legge `componi`)
    W_, H_ = S.W_OUT, S.H_OUT
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-sseof', '-0.6', '-i', str(ultimo), '-vf',
                          'scale=in_color_matrix=bt709:in_range=tv:out_range=full,format=rgb24', '-f', 'rawvideo', '-'],
                         capture_output=True).stdout
    ultimo_f = np.frombuffer(raw[-W_ * H_ * 3:], np.uint8).reshape(H_, W_, 3).astype(np.float32)
    out = out or P.render('scena') / 'zz-schermata-finale.mp4'
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f"{W_}x{H_}",
                            '-framerate', P.fps_str, '-i', '-',
                            '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,'
                                   'setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv',
                            '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-profile:v', 'high',
                            '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                            '-color_range', 'tv', '-g', '50', '-an', '-frames:v', str(n), str(out)], stdin=subprocess.PIPE)
    st = S.Strato(mov)
    controllo = None
    for f in range(n):
        rgb, al = next(st)
        a = rgb * al + ultimo_f * (1 - al)
        if f == n // 2:
            controllo = a.copy()
        enc.stdin.write(np.clip(a + 0.5, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close()
    enc.wait()
    if enc.returncode:
        sys.exit("schermata finale: encoder fallito")
    # controlli
    esiti = []
    # fase 7c: il pittogramma su un disco panna accanto al logo (il gruppo resta centrato, come in fine_youtube.js)
    D_ = round(lh * 1.4)
    sp_ = (D_ + 40) / 2
    box = [('logo', round(dati['logo']['x'] + sp_), dati['logo']['y'], round(lw * 1.02), round(lh * 1.02)),
           ('pittogramma', round(dati['logo']['x'] - sp_), round(dati['logo']['y'] + lh / 2 - D_ / 2), D_, D_),
           ('filo', dati['filo']['x'], dati['filo']['y'], dati['filo']['larghezza'], 2)]
    tocca = [f"{b[0]} su {z[0]}" for b in box for z in ZONE_FINE
             if b[1] < z[1] + z[3] and z[1] < b[1] + b[3] and b[2] < z[2] + z[4] and z[2] < b[2] + b[4]]
    esiti.append(('logo, pittogramma e filo fuori dalle zone di YouTube', ', '.join(tocca) or 'fuori', not tocca))
    fuori = [b[0] for b in box if b[1] < 96 or b[1] + b[3] > W_ - 96 or b[2] < 54 or b[2] + b[4] > H_ - 54]
    esiti.append(('logo, pittogramma e filo dentro la zona sicura', ', '.join(fuori) or 'dentro', not fuori))
    lum = controllo @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    chiari = {z[0]: int((lum[z[2]:z[2] + z[4], z[1]:z[1] + z[3]] > 90).sum()) for z in ZONE_FINE}
    esiti.append(('nelle zone di YouTube solo il fondo (pixel chiari a meta coda)',
                  ', '.join(f"{k} {v}" for k, v in chiari.items()), not any(chiari.values())))
    im = Image.fromarray(np.clip(controllo, 0, 255).astype(np.uint8))
    dr = ImageDraw.Draw(im)
    for nome, x, y, w, h_ in ZONE_FINE:
        if nome == 'iscriviti':
            dr.ellipse([x, y, x + w, y + h_], outline=(255, 80, 80), width=4)
        else:
            dr.rectangle([x, y, x + w, y + h_], outline=(255, 80, 80), width=4)
        dr.text((x + 12, y + 10), nome, fill=(255, 80, 80))
    dr.rectangle([96, 54, W_ - 96, H_ - 54], outline=(255, 210, 0), width=2)
    im.save(png or P.controllo('schermata-finale.jpg'), quality=88)
    for c in esiti:
        print(f"     {'ok ' if c[2] else 'NO '} schermata finale: {c[0]}: {c[1]}")
    rap = {'s': round(P.leggi('edl.json')['frame'] / fps, 3), 'frame': n, 'durata': n / fps, 'zone': ZONE_FINE,
           'controlli': [{'cosa': a, 'valore': b, 'ok': c} for a, b, c in esiti]}
    return out, n, rap


def scena(slug, solo=None):
    P = Progetto(slug)
    R = P.regia()
    if not R.get('scena'):
        sys.exit("regia.json non ha la sezione `scena`")
    momenti = R['scena']['momenti']
    fps = P.fps
    # i tempi dei momenti possono essere ancore: si risolvono sul montato
    anc = S.Ancore(P)
    for m in momenti:
        if len(m['pezzi']) != 1:
            sys.exit(f"momento {m['id']}: un solo pezzo contiguo")
        m['pezzi'] = [[round(anc(v), 3) if isinstance(v, dict) else v for v in m['pezzi'][0]]]
    pezzi = _tessere(P, R, momenti)
    # catalogo dei modelli (fase 7c): niente vietati, mai lo stesso modello due volte di fila
    from . import catalogo as CAT
    prob = CAT.controlla(momenti)
    if prob:
        sys.exit("scena: il piano grafico non rispetta il catalogo:\n  " + "\n  ".join(prob))
    solo = {s.strip() for s in solo.split(',')} if solo else None
    dest = P.render('scena')
    dest.mkdir(exist_ok=True)
    rapporti, eventi = [], []
    for k, m in enumerate(momenti):
        spec = json.loads(json.dumps(m))
        spec.update({'n': k, 'nome': m['id'], 'cartella': f"{slug}/{k:02d}-{m['id']}", 'strisce': m.get('strisce', [])})
        out = dest / f"{k:02d}-{m['id']}.mp4"
        anc.usate.clear()
        if solo and m['id'] not in solo and str(k) not in solo and out.exists() and (dest / f"{k:02d}.json").exists():
            rap = json.loads((dest / f"{k:02d}.json").read_text())
        else:
            print(f"{k:02d} {m['id']} ({m['pezzi'][0][0]:.2f}-{m['pezzi'][0][1]:.2f})...")
            rap, tempo, cam, volto, spr = S.costruisci(P, spec, out, anc)
            rap['testi'] = [{'modello': x['modello'], 's': round(x['s'] + m['pezzi'][0][0], 2),
                             'e': round(x['e'] + m['pezzi'][0][0], 2), 'testi': _testi(x)}
                            for x in spr['elementi'] if x['modello'] != 'etichetta']
            # strisce di controllo dell'entrata, come nel campionario
            strisce = []
            for j, st in enumerate(spr.get('strisce', [])):
                png = P.controllo(f"scena-{k:02d}-{m['id']}-{j + 1}.jpg")
                ancore = [(u['parola'], tempo.out(u['t'])) for u in rap['ancore']]
                S.striscia(out, st['t'], png, P, (anc.env, tempo.montato),
                           f"{k:02d} {m['id']} — {st.get('cosa', '')}", passo=st.get('passo', 2),
                           prima=st.get('prima', 4), dopo=st.get('dopo', 26), ancore=ancore,
                           volto=volto if st.get('volto') else None)
                strisce.append(png.name)
            rap['strisce'] = strisce
            (dest / f"{k:02d}.json").write_text(json.dumps(rap, ensure_ascii=False, indent=1, default=float))
            for c in rap['controlli']:
                print(f"     {'ok ' if c['ok'] else 'NO '} {c['cosa']}: {c['valore']}")
        a0 = m['pezzi'][0][0]
        for ev in rap.get('eventi', []):
            e2 = dict(ev)
            e2['t'] = round(ev['t'] + a0, 4)
            eventi.append(e2)
        rap['id'], rap['pezzo'] = m['id'], m['pezzi'][0]
        rapporti.append(rap)
    # suoni del video intero che non appartengono a un momento (B-roll, chip)
    for ev in R['scena'].get('suoni', []):
        e2 = dict(ev)
        e2['t'] = round(anc(ev['t']) if isinstance(ev['t'], dict) else ev['t'], 4)
        eventi.append(e2)
    G = P.leggi('grafica.json')
    for b in G.get('broll', []):
        eventi.append({'nome': 'whoosh', 't': b['s'] + 0.02, 'db': -18, 'kw': {'dur': 0.32}, 'perche': 'stacco sul B-roll'})
    if G.get('chip'):
        eventi.append({'nome': 'swish', 't': G['chip']['s'] + 0.05, 'db': -22, 'perche': 'entra il chip'})
    # video: momenti + B-roll dal montato di monta, uno dopo l'altro (stessa codifica)
    lav = S.LAVORO / slug / '_unisci'
    shutil.rmtree(lav, ignore_errors=True)
    lav.mkdir(parents=True)
    pulito_monta = P.render(f"{slug}_pulito_monta.mp4")
    pulito = P.render(f"{slug}_pulito.mp4")
    if not pulito_monta.exists():
        if not pulito.exists():
            sys.exit("manca il montato di `monta` (servono i B-roll): lancia prima ./mve monta")
        os.replace(pulito, pulito_monta)
    # il montato di `monta` deve essere quello dell'EDL di adesso: i B-roll si prendono da li
    # per numero di frame (fase 7b: dopo i tagli nuovi c'era ancora quello vecchio, 10469 frame
    # contro 10304, e i B-roll sarebbero usciti spostati). Un `monta` piu recente lo sostituisce.
    from .monta import _conta_frame
    if pulito.exists() and pulito.stat().st_mtime > pulito_monta.stat().st_mtime \
            and _conta_frame(pulito) == P.leggi('edl.json')['frame']:
        os.replace(pulito, pulito_monta)
    if _conta_frame(pulito_monta) != P.leggi('edl.json')['frame']:
        sys.exit(f"renders/{pulito_monta.name} non e il montato dell'EDL di adesso "
                 f"({_conta_frame(pulito_monta)} frame contro {P.leggi('edl.json')['frame']}): lancia ./mve monta")
    lista = []
    for nome, a, b in pezzi:
        if nome == 'broll':
            f = lav / f"broll-{a:05d}.mp4"
            ffmpeg('-i', pulito_monta, '-vf', f"select='between(n\\,{a}\\,{b - 1})',setpts=N/({P.fps_str}*TB)",
                   '-frames:v', str(b - a), '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium',
                   '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-r', P.fps_str,
                   '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', f)
        else:
            k = next(i for i, m in enumerate(momenti) if m['id'] == nome)
            f = dest / f"{k:02d}-{nome}.mp4"
        lista.append(f)
    # schermata finale YouTube dopo l'ultima parola (tappa 3): regia.json -> scena.coda
    coda, nc = R['scena'].get('coda'), 0
    if coda:
        f, nc, rap_coda = schermata_finale(P, coda, lista[-1], slug)
        lista.append(f)
        t_c = P.leggi('edl.json')['frame'] / fps
        eventi.append({'nome': 'whoosh', 't': t_c + 0.04, 'db': -16, 'kw': {'dur': 0.4}, 'perche': 'entra la schermata finale'})
        eventi.append({'nome': 'swish', 't': t_c + 0.5, 'db': -24, 'perche': 'il logo si posa'})
    (lav / 'lista.txt').write_text(''.join(f"file '{f}'\n" for f in lista))
    video = lav / 'video.mp4'
    ffmpeg('-f', 'concat', '-safe', '0', '-i', lav / 'lista.txt', '-an', '-c:v', 'copy', video)
    ffmpeg('-i', video, '-i', P.asset('voce-montata.wav'), '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
           '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', pulito)
    from .monta import _conta_frame
    n = _conta_frame(pulito)
    N = P.leggi('edl.json')['frame'] + nc
    print(f"-> renders/{pulito.name}: {n} frame (attesi {N}" + (f", di cui {nc} di schermata finale)" if nc else ")"))
    if n != N:
        sys.exit("  !!! il numero di frame non torna con l'EDL")
    N -= nc
    # mix unico: voce + tutti i suoni, -14 LUFS
    tempo = S.Tempo(P, [[0, N / fps]])
    musica = next(iter(sorted((S.LIBRERIA / 'musica').glob('*.wav')) + sorted((S.LIBRERIA / 'musica').glob('*.mp3'))), None) \
        if R['scena'].get('musica', True) else None
    log, loud = S.mix(P, tempo, eventi, P.asset('mix-finale.wav'), str(musica) if musica else None, coda=nc / fps)
    print(f"-> assets/mix-finale.wav: {len(log)} suoni, {loud['I']} LUFS" + (f", musica {musica.name}" if musica else ", senza musica"))
    CAT.registra_uso(slug, momenti)
    P.scrivi('scena.json', {'momenti': rapporti, 'suoni': log, 'loudness': loud, 'musica': musica.name if musica else None,
                            'coda': rap_coda if coda else None})
    shutil.rmtree(lav, ignore_errors=True)

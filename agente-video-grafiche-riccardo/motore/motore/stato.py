"""Fase `stato`: cosa e fatto, cosa e da rifare, qual e la prossima fase.

Una fase e da rifare quando un suo ingresso e piu recente della sua uscita
(per esempio: regia.json cambiata dopo l'EDL). Nessuna fase si fida del valore
di ritorno di un'altra: qui si guarda il disco.
"""
from pathlib import Path

from .progetto import Progetto, leggi, impronta, REGIA_DI

# fase, uscite, ingressi (percorsi relativi alla cartella del video; {s} = slug)
CATENA = [
    ('prep',      ['data/blocchi.json', 'assets/audio-48k.wav'], []),
    ('trascrivi', ['data/parole-finestre.json', 'data/blocchi-testo.json'], ['data/blocchi.json']),
    ('volti',     ['data/volti.json'], []),
    ('papere',    ['data/papere.json', 'controlli/papere.md'], ['data/blocchi-testo.json']),
    ('REGIA',     ['regia.json'], ['data/papere.json']),
    ('edl',       ['data/edl.json'], ['regia.json', 'data/blocchi.json']),
    ('audio',     ['assets/voce-montata.wav', 'data/parole-montato.json', 'controlli/giunte.md'], ['data/edl.json']),
    ('grafica',   ['data/grafica.json'], ['regia.json', 'data/parole-montato.json']),
    ('inquadra',  ['data/inquadratura.json'], ['data/grafica.json', 'data/volti.json']),
    ('monta',     ['renders/{s}_pulito.mp4'], ['data/inquadratura.json', 'assets/voce-montata.wav']),
    ('inserti',   ['data/inserti.json'], ['data/grafica.json', 'data/inquadratura.json']),
    ('scena',     ['data/scena.json', 'renders/{s}_pulito.mp4'], ['regia.json']),
    ('sagome',    ['data/sagome'], ['renders/{s}_pulito.mp4']),
    ('anteprima', ['controlli/anteprima.jpg'], ['renders/{s}_pulito.mp4', 'data/grafica.json']),
    ('suono',     ['assets/mix-finale.wav'], ['data/inquadratura.json', 'assets/voce-montata.wav']),
    ('finale',    ['renders/{s}_FINALE.mp4'], ['renders/{s}_pulito.mp4', 'assets/mix-finale.wav', 'data/sagome',
                                               'data/inserti.json']),
    ('qc',        ['controlli/QC.md'], ['renders/{s}_FINALE.mp4']),
    ('consegna',  ['consegna/youtube.txt', 'consegna/{s}.srt', 'consegna/{s}.mp4', 'consegna/validazione-animazioni.md'],
                  ['regia.json', 'data/grafica.json', 'renders/{s}_FINALE.mp4']),
]
# fuori dal flusso standard (Riccardo, 30/10/2026: si consegnano solo video, SRT e youtube.txt);
# le fasi restano nel motore e si lanciano solo se richieste
FUORI_FLUSSO = ['shorts', 'miniature']


def stato(slug):
    P = Progetto(slug)
    prossima = None
    for fase, outs, ins in CATENA:
        if fase == 'consegna' and P.tipo == 'mid-roll':
            outs = [o for o in outs if not o.endswith('youtube.txt')]      # mid-roll: solo video e SRT
        paths = [P.p(o.format(s=slug)) for o in outs]
        if fase == 'sagome':
            G = P.leggi('grafica.json', {}) if P.data('grafica.json').exists() else {}
            if not any(c.get('dietro') for c in G.get('capitoli', [])):
                print(f"  ·  {fase:<10} non serve (nessun titolo dietro)")
                continue
        con_scena = bool(P.regia().get('scena')) if P.p('regia.json').exists() else False
        if fase == 'scena' and not con_scena:
            print(f"  ·  {fase:<10} non serve (nessuna scena in regia)")
            continue
        if fase in ('suono', 'anteprima') and con_scena:
            print(f"  ·  {fase:<10} non serve (il mix e la revisione li fa `scena`)")
            continue
        if fase == 'inserti':
            G = P.leggi('grafica.json', {}) if P.data('grafica.json').exists() else {}
            if not G.get('inserti'):
                print(f"  ·  {fase:<10} non serve (nessun inserto in regia)")
                continue
        manca = [p for p in paths if not p.exists()]
        if manca:
            stato_ = 'DA FARE'
        else:
            t_out = min(p.stat().st_mtime for p in paths)
            nuovi = []
            for i in ins:
                q = P.p(i.format(s=slug))
                if not q.exists() or q.stat().st_mtime <= t_out + 1:
                    continue
                # per regia.json conta solo la parte che la fase usa
                base = outs[0].split('/')[-1]
                if i == 'regia.json' and base in REGIA_DI:
                    fatta = leggi(paths[0]).get('regia')
                    if fatta == impronta(leggi(q), REGIA_DI[base]):
                        continue
                nuovi.append(i)
            stato_ = f"DA RIFARE ({', '.join(nuovi)} piu recente)" if nuovi else 'fatto'
        segno = '✓' if stato_ == 'fatto' else '→' if prossima is None else ' '
        print(f"  {segno}  {fase:<10} {stato_}")
        if stato_ != 'fatto' and prossima is None:
            prossima = fase
    if prossima == 'REGIA':
        print("\nprossimo passo: leggere controlli/papere.md e data/trascrizione.txt, scrivere regia.json")
    elif prossima:
        print(f"\nprossima fase: ./mve {prossima} {slug}")
    else:
        print("\ntutto fatto: controlla controlli/QC.md, consegna/ e la scheda da far firmare "
              "(consegna/validazione-animazioni.md)")
    print(f"(fuori dal flusso, solo su richiesta: {', '.join(FUORI_FLUSSO)})")


def dove(slug, tempo):
    """un istante del video consegnato (m:ss o secondi) -> tempo sorgente, segmento,
    pezzo di inquadratura e parole attorno. Serve a tradurre un "a 4:32 c'e un
    problema" nel punto esatto da correggere in regia.json."""
    from .progetto import ts
    P = Progetto(slug)
    fps = P.fps
    t = sum(float(x) * 60 ** i for i, x in enumerate(reversed(str(tempo).split(':'))))
    E = P.leggi('edl.json')
    seg = max((s for s in E['segmenti'] if s['edit_in'] <= t), key=lambda s: s['edit_in'])
    k = E['segmenti'].index(seg)
    src = seg['in'] + (t - seg['edit_in'])
    print(f"montato {ts(t)} -> sorgente {src:.2f}s ({ts(src)}), segmento {k} "
          f"[{seg['in']:.2f} - {seg['in'] + seg['n'] / fps:.2f}]")
    for g in E['giunte']:
        if abs(g['t'] - t) < 3:
            print(f"  giunta G{g['i']:02d} a {ts(g['t'])} ({g['t'] - t:+.2f}s): {g['tipo']} {g['motivo']}")
    if P.data('inquadratura.json').exists():
        for i, p in enumerate(P.leggi('inquadratura.json')['pezzi']):
            if p['edit_in'] <= t < p['edit_in'] + p['n'] / fps:
                print(f"  pezzo {i}: {p['framing']} (z {p['z']}), {ts(p['edit_in'])} - "
                      f"{ts(p['edit_in'] + p['n'] / fps)}  -> `./mve monta {slug} --solo {i}` per rifarlo")
    W = P.leggi('parole-montato.json')
    near = [w for w in W if t - 4 < w[0] < t + 4]
    print("  parole: " + ' '.join(('»' if abs(w[0] - t) < 0.3 else '') + w[2] for w in near))
    B = P.leggi('blocchi-testo.json', [])
    for b in B:
        if b[1] > src - 4 and b[0] < src + 4 and b[2]:
            print(f"  sorgente [{b[0]:.2f}-{b[1]:.2f}] {b[2]}")


def panoramica():
    """./mve stato senza slug: i video, le cartelle in inbox, gli strumenti, RAM e disco.
    Non scrive niente: serve a capire se la macchina e pronta (anche a installa.sh)."""
    import os
    import shutil
    import subprocess
    from .progetto import AGENTE, VIDEOS, INBOX, LIBRERIA, WHISPER_MODEL, ram_gb, lavori
    from .sorgente import GIRATO, TESTO, INFO, leggi_info

    def riga(ok, cosa, dettaglio=''):
        print(f"  {'✓' if ok else '✗'}  {cosa:<28} {dettaglio}")
        return ok

    print("video (videos/):")
    vv = sorted(d.name for d in VIDEOS.iterdir() if d.is_dir()) if VIDEOS.is_dir() else []
    print('  ' + (', '.join(vv) if vv else 'nessun video'))
    print("\ninbox/ (una cartella per video: girato, script, info.txt, materiali/):")
    cc = sorted(d for d in INBOX.iterdir() if d.is_dir()) if INBOX.is_dir() else []
    if not cc:
        print('  vuota')
    for d in cc:
        g = [p.name for p in d.iterdir() if p.is_file() and p.suffix.lower() in GIRATO]
        t = [p.name for p in d.iterdir() if p.is_file() and p.suffix.lower() in TESTO
             and p.name.lower() not in (INFO, 'leggimi.md') and not p.name.startswith('.')]
        info, manca = leggi_info(d)
        problemi = ([] if len(g) == 1 else ['nessun girato' if not g else f"{len(g)} girati"]) + \
                   ([] if len(t) == 1 else ['nessuno script' if not t else f"{len(t)} testi"]) + \
                   [f"info.txt: {m}" for m in manca]
        riga(not problemi, d.name, '; '.join(problemi) or f"{info.get('tipo')}, {info.get('osteopata')}")

    print("\nstrumenti:")
    ok = True
    for nome in ('ffmpeg', 'ffprobe', 'whisper-cli', 'node', 'swiftc'):
        ok &= riga(bool(shutil.which(nome)), nome, shutil.which(nome) or 'manca: vedi INSTALLAZIONE.md')
    if shutil.which('node'):
        v = subprocess.run(['node', '-v'], capture_output=True, text=True).stdout.strip()
        ok &= riga(int(v.lstrip('v').split('.')[0] or 0) >= 22, 'node 22 o piu', v)
    ok &= riga(WHISPER_MODEL.is_file(), 'modello whisper large-v3',
               f"{WHISPER_MODEL.stat().st_size / 1e9:.1f} GB" if WHISPER_MODEL.is_file() else f"manca ({WHISPER_MODEL.name})")
    base = AGENTE / 'motore' / 'inserti'
    hf = base / 'node_modules' / 'hyperframes' / 'package.json'
    if hf.is_file():
        import json
        vh = json.loads(hf.read_text())['version']
        ok &= riga(vh == '0.8.204', 'HyperFrames 0.8.204', vh)
    else:
        ok &= riga(False, 'HyperFrames 0.8.204', 'manca motore/inserti/node_modules')
    chrome = list((base / '.casa' / '.cache' / 'hyperframes' / 'chrome').glob('**/chrome-headless-shell')) + \
        list((Path.home() / '.cache' / 'hyperframes' / 'chrome').glob('**/chrome-headless-shell'))
    ok &= riga(bool(chrome), 'browser di render', 'pronto' if chrome else "manca: lo scarica installa.sh")
    try:
        import numpy, PIL, fontTools  # noqa: F401
        ok &= riga(True, 'Python: pillow, numpy, fonttools', PIL.__version__)
    except ImportError as e:
        ok &= riga(False, 'Python: pillow, numpy, fonttools', str(e))

    print("\nmacchina:")
    ram = ram_gb()
    riga(ram >= 16, f"RAM {ram:.0f} GB", f"lavori in parallelo: trascrizione {lavori(3)}, render {lavori(2)}"
         + ('' if ram >= 16 else ' (sotto i 16 GB: funziona, ma lento)'))
    st = os.statvfs(AGENTE)
    libero = st.f_bavail * st.f_frsize / 1e9
    riga(libero >= 150, f"disco libero {libero:.0f} GB", 'servono 150 GB per un video YouTube lungo, 60 per un mid-roll')

    print("\nlibreria:")
    from .libreria import BROLL, VIDEO, da_catalogare
    clip = [p for p in BROLL.rglob('*') if p.is_file() and p.suffix.lower() in VIDEO] if BROLL.is_dir() else []
    nuove = da_catalogare()
    riga(not nuove, f"B-roll: {len(clip)} clip", f"{len(nuove)} da catalogare: ./mve libreria" if nuove else 'tutte catalogate')
    pd = [p for p in (LIBRERIA / 'prima-dopo').glob('*') if p.is_file() and p.suffix.lower() in ('.jpg', '.jpeg', '.png', '.heic')]
    riga(True, f"prima-dopo: {len(pd)} foto", 'si usano solo con il consenso scritto nel catalogo')
    mu = [p for p in (LIBRERIA / 'musica').glob('*') if p.suffix.lower() in ('.wav', '.mp3')]
    riga(True, f"musica: {len(mu)} brani", 'senza brani, niente musica' if not mu else 'solo con licenza nel catalogo')
    print("\n" + ("pronto." if ok else "manca qualcosa: vedi INSTALLAZIONE.md (o lancia ./installa.sh)."))

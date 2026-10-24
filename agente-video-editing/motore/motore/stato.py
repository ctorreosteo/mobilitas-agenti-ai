"""Fase `stato`: cosa e fatto, cosa e da rifare, qual e la prossima fase.

Una fase e da rifare quando un suo ingresso e piu recente della sua uscita
(per esempio: regia.json cambiata dopo l'EDL). Nessuna fase si fida del valore
di ritorno di un'altra: qui si guarda il disco.
"""
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
    ('sagome',    ['data/sagome'], ['renders/{s}_pulito.mp4']),
    ('anteprima', ['controlli/anteprima.jpg'], ['renders/{s}_pulito.mp4', 'data/grafica.json']),
    ('suono',     ['assets/mix-finale.wav'], ['data/inquadratura.json', 'assets/voce-montata.wav']),
    ('finale',    ['renders/{s}_FINALE.mp4'], ['renders/{s}_pulito.mp4', 'assets/mix-finale.wav', 'data/sagome']),
    ('qc',        ['controlli/QC.md'], ['renders/{s}_FINALE.mp4']),
    ('shorts',    ['shorts'], ['regia.json', 'assets/voce-montata.wav']),
    ('miniature', ['miniature'], ['regia.json', 'data/volti.json']),
    ('consegna',  ['consegna/youtube.md'], ['regia.json', 'data/grafica.json']),
]


def _data(p):
    """data di un'uscita; per una cartella quella del file piu recente dentro:
    la data della cartella non cambia quando si riscrive un file che c'era gia
    (gli Shorts rifatti risultavano "DA RIFARE")"""
    if p.is_dir():
        return max((f.stat().st_mtime for f in p.iterdir()), default=p.stat().st_mtime)
    return p.stat().st_mtime


def stato(slug):
    P = Progetto(slug)
    prossima = None
    for fase, outs, ins in CATENA:
        paths = [P.p(o.format(s=slug)) for o in outs]
        if fase == 'sagome':
            G = P.leggi('grafica.json', {}) if P.data('grafica.json').exists() else {}
            if not any(c.get('dietro') for c in G.get('capitoli', [])):
                print(f"  ·  {fase:<10} non serve (nessun titolo dietro)")
                continue
        manca = [p for p in paths if not p.exists()]
        if manca:
            stato_ = 'DA FARE'
        else:
            t_out = min(_data(p) for p in paths)
            nuovi = []
            for i in ins:
                q = P.p(i.format(s=slug))
                if not q.exists() or _data(q) <= t_out + 1:
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
        print("\ntutto fatto: controlla controlli/QC.md e consegna/youtube.md")


def dove(slug, tempo):
    """un istante del video consegnato (m:ss o secondi) -> tempo sorgente, segmento,
    pezzo di inquadratura e parole attorno. Serve a tradurre un "a 4:32 c'e un
    problema" nel punto esatto da correggere in regia.json."""
    from .progetto import FPS, ts
    P = Progetto(slug)
    t = sum(float(x) * 60 ** i for i, x in enumerate(reversed(str(tempo).split(':'))))
    E = P.leggi('edl.json')
    seg = max((s for s in E['segmenti'] if s['edit_in'] <= t), key=lambda s: s['edit_in'])
    k = E['segmenti'].index(seg)
    src = seg['in'] + (t - seg['edit_in'])
    print(f"montato {ts(t)} -> sorgente {src:.2f}s ({ts(src)}), segmento {k} "
          f"[{seg['in']:.2f} - {seg['in'] + seg['n'] / FPS:.2f}]")
    for g in E['giunte']:
        if abs(g['t'] - t) < 3:
            print(f"  giunta G{g['i']:02d} a {ts(g['t'])} ({g['t'] - t:+.2f}s): {g['tipo']} {g['motivo']}")
    if P.data('inquadratura.json').exists():
        for i, p in enumerate(P.leggi('inquadratura.json')['pezzi']):
            if p['edit_in'] <= t < p['edit_in'] + p['n'] / FPS:
                print(f"  pezzo {i}: {p['framing']} (z {p['z']}), {ts(p['edit_in'])} - "
                      f"{ts(p['edit_in'] + p['n'] / FPS)}  -> `./mve monta {slug} --solo {i}` per rifarlo")
    W = P.leggi('parole-montato.json')
    near = [w for w in W if t - 4 < w[0] < t + 4]
    print("  parole: " + ' '.join(('»' if abs(w[0] - t) < 0.3 else '') + w[2] for w in near))
    B = P.leggi('blocchi-testo.json', [])
    for b in B:
        if b[1] > src - 4 and b[0] < src + 4 and b[2]:
            print(f"  sorgente [{b[0]:.2f}-{b[1]:.2f}] {b[2]}")

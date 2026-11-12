"""Fase `versione`: una nuova versione di un video, dallo stesso girato e con gli stessi tagli.

    ./mve versione <slug> <slug_nuovo>

Serve quando cambia la grafica e il montaggio deve restare identico, per
confrontare le due versioni: la v1 non si tocca. Si copiano (con le date
originali, cosi `stato` le vede gia fatte) le analisi e il montaggio audio:
`meta.json`, `copione.md`, `regia.json`, `data/` tranne il piano grafico e le
inquadrature, l'audio in `assets/`, i referti di papere e giunte. Il girato si
ricollega, non si copia. Da `grafica` in poi tutto si rifa nella versione nuova.
"""
import shutil
import sys

from .progetto import VIDEOS, leggi, scrivi

NON_COPIARE_DATI = {'grafica.json', 'inquadratura.json', 'inserti.json', 'sagome', 'shorts.json'}
ASSET = ('audio-16k-mono.wav', 'audio-16k-asr.wav', 'audio-48k.wav', 'voce-montata.wav', 'voce-montata-16k.wav')
CONTROLLI = ('papere.md', 'giunte.md')


def versione(slug, nuovo):
    src, dst = VIDEOS / slug, VIDEOS / nuovo
    if not src.is_dir():
        sys.exit(f"video '{slug}' non trovato")
    if dst.exists():
        sys.exit(f"{dst} esiste gia: scegli un altro nome (una versione non si sovrascrive)")
    for sub in ('assets', 'data', 'renders', 'controlli'):
        (dst / sub).mkdir(parents=True)
    m = leggi(src / 'meta.json')
    link = src / m['sorgente']
    (dst / m['sorgente']).symlink_to(link.resolve() if link.is_symlink() else link)
    for f in ('copione.md', 'regia.json'):
        if (src / f).exists():
            shutil.copy2(src / f, dst / f)
    n = 0
    for p in sorted((src / 'data').iterdir()):
        if p.name in NON_COPIARE_DATI:
            continue
        (shutil.copytree if p.is_dir() else shutil.copy2)(p, dst / 'data' / p.name)
        n += 1
    for a in ASSET:
        if (src / 'assets' / a).exists():
            shutil.copy2(src / 'assets' / a, dst / 'assets' / a)
    for c in CONTROLLI:
        if (src / 'controlli' / c).exists():
            shutil.copy2(src / 'controlli' / c, dst / 'controlli' / c)
    m.update({'slug': nuovo, 'versione_di': slug})
    scrivi(dst / 'meta.json', m)
    # meta.json non e ingresso di nessuna fase: riscriverlo non fa rifare niente
    print(f"{nuovo}: nuova versione di {slug} (stesso girato, stessi tagli; {n} file di analisi copiati)")
    print(f"  la grafica si decide in {nuovo}/regia.json; poi ./mve stato {nuovo}")

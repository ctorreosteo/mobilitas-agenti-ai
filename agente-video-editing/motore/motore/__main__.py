"""mve — il motore di montaggio dei video @Studio_Mobilitas.

    ./mve <fase> <slug> [opzioni]

L'ordine delle fasi e quello di CLAUDE.md. `./mve stato <slug>` dice cosa e
fatto, cosa e da rifare e qual e la prossima fase.
"""
import argparse
import importlib
import sys

FASI = {
    # fase: (modulo, funzione, descrizione)
    'init':       ('sorgente',     'init',        "crea il progetto da un file di camera"),
    'prep':       ('sorgente',     'prep',        "estrae l'audio, prepara il colore, mappa il parlato"),
    'trascrivi':  ('trascrivi',    'trascrivi',   "trascrizione intera e a finestre della sorgente"),
    'volti':      ('visione',      'volti',       "traccia il volto sulla sorgente (Apple Vision)"),
    'papere':     ('papere',       'papere',      "cerca papere e riprese doppie, scrive il referto"),
    'edl':        ('edl',          'edl',         "regia.json -> EDL con punti di taglio sul fondo di sala"),
    'audio':      ('edl',          'audio',       "monta solo l'audio, lo trascrive, ascolta le giunte"),
    'grafica':    ('grafica.piano', 'piano',      "piano di sottotitoli, card, stacchi sul montato"),
    'inquadra':   ('inquadra',     'inquadra',    "sceglie l'inquadratura di ogni pezzo"),
    'monta':      ('monta',        'monta',       "renderizza il montato pulito dal 4K"),
    'sagome':     ('visione',      'sagome',      "sagoma della persona per i titoli dietro"),
    'anteprima':  ('grafica.render', 'anteprima', "grafica sopra i frame veri, contact sheet"),
    'suono':      ('suono',        'suono',       "sound design sintetizzato e musica opzionale"),
    'finale':     ('monta',        'finale',      "master con grafica e suono"),
    'qc':         ('qc',           'qc',          "controlli automatici sul file consegnato"),
    'shorts':     ('shorts',       'shorts',      "Shorts verticali 9:16 dal 4K"),
    'miniature':  ('miniature',    'miniature',   "miniature YouTube"),
    'consegna':   ('consegna',     'consegna',    "SRT, capitoli, pacchetto YouTube"),
    'stato':      ('stato',        'stato',       "cosa e fatto e qual e la prossima fase"),
    'dove':       ('stato',        'dove',        "un istante del video consegnato -> sorgente, giunta, pezzo"),
    'griglia':    ('stato',        'griglia',     "fotogramma della sorgente con la griglia 0-1, per i `dove` dei segni"),
}


def main(argv=None):
    ap = argparse.ArgumentParser(prog='mve', description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='fase', required=True)
    for k, (_, _, d) in FASI.items():
        sp = sub.add_parser(k, help=d)
        if k == 'init':
            sp.add_argument('file')
            sp.add_argument('slug', nargs='?')
        else:
            sp.add_argument('slug')
        if k in ('dove', 'griglia'):
            sp.add_argument('tempo', help="m:ss o secondi del video consegnato")
        if k == 'monta':
            sp.add_argument('--solo', help="pezzi da rifare, es. 3,7,12")
        if k in ('finale', 'shorts'):
            sp.add_argument('--limite', type=float, help="solo i primi N secondi (prova)")
        if k == 'anteprima':
            sp.add_argument('tempi', nargs='*', type=float)
        if k == 'shorts':
            sp.add_argument('--solo', help="indici degli short da fare, es. 0,2")
    a = ap.parse_args(argv)
    mod, fn, _ = FASI[a.fase]
    f = getattr(importlib.import_module(f'motore.{mod}'), fn)
    kw = {k: v for k, v in vars(a).items() if k not in ('fase',) and v is not None}
    if a.fase == 'init':
        f(kw['file'], kw.get('slug'))
        return 0
    slug = kw.pop('slug')
    f(slug, **kw)
    return 0


if __name__ == '__main__':
    sys.exit(main())

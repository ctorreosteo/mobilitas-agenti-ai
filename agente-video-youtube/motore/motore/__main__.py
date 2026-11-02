"""mve — il motore di montaggio dei video @Studio_Mobilitas.

    ./mve <fase> <slug> [opzioni]

L'ordine delle fasi e quello di CLAUDE.md. `./mve stato <slug>` dice cosa e
fatto, cosa e da rifare e qual e la prossima fase.
"""
import argparse
import datetime
import importlib
import os
import sys
import time

# fasi che non cambiano niente di un video: non vanno in tempi.md
SOLO_LETTURA = {'stato', 'dove', 'materiali', 'catalogo', 'libreria', 'regressione', 'campionario'}


def _byte(cartella, visti=None):
    """spazio occupato (i collegamenti fisici una volta sola, i simbolici no)"""
    visti = set() if visti is None else visti
    tot = 0
    for radice, _, files in os.walk(cartella):
        for n in files:
            try:
                st = os.lstat(os.path.join(radice, n))
            except OSError:
                continue
            if (st.st_dev, st.st_ino) in visti:
                continue
            visti.add((st.st_dev, st.st_ino))
            tot += st.st_size
    return tot


def _gb(b):
    return f"{b / 1e9:.1f} GB"


def registra_tempo(slug, fase, secondi, esito):
    """una riga in videos/<slug>/tempi.md: quanto e durata la fase e quanto spazio occupa il lavoro"""
    from .progetto import AGENTE, VIDEOS
    d = VIDEOS / slug
    if not d.is_dir():
        return
    p = d / 'tempi.md'
    if not p.exists():
        p.write_text(f"# Tempi e spazio: {slug}\n\nUna riga per ogni fase lanciata con `./mve` (la scrive il motore). "
                     "«cartella del video» non conta il girato (è un collegamento a inbox/).\n\n"
                     "| data e ora | fase | durata | esito | cartella del video | .lavoro | disco libero |\n"
                     "|---|---|---|---|---|---|---|\n", encoding='utf-8')
    st = os.statvfs(d)
    m, s = divmod(int(round(secondi)), 60)
    riga = (f"| {datetime.datetime.now():%d/%m/%Y %H:%M} | {fase} | {m}:{s:02d} | {esito} | {_gb(_byte(d))} | "
            f"{_gb(_byte(AGENTE / '.lavoro'))} | {_gb(st.f_bavail * st.f_frsize)} |\n")
    with open(p, 'a', encoding='utf-8') as fh:
        fh.write(riga)

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
    'inserti':    ('inserti',      'inserti',     "grafiche animate HyperFrames del piano (MOV con alfa)"),
    'scena':      ('video_scena',  'scena',       "montato ricomposto dai momenti di regia.json (grafica dentro la scena) + mix"),
    'sagome':     ('visione',      'sagome',      "sagoma della persona per i titoli dietro"),
    'anteprima':  ('grafica.render', 'anteprima', "grafica sopra i frame veri, contact sheet"),
    'suono':      ('suono',        'suono',       "sound design sintetizzato e musica opzionale"),
    'finale':     ('monta',        'finale',      "master con grafica e suono"),
    'qc':         ('qc',           'qc',          "controlli automatici sul file consegnato"),
    'shorts':     ('shorts',       'shorts',      "Shorts verticali 9:16 dal 4K"),
    'miniature':  ('miniature',    'miniature',   "miniature YouTube"),
    'consegna':   ('consegna',     'consegna',    "SRT, capitoli, pacchetto YouTube (mid-roll: solo video e SRT), scheda di validazione"),
    'validazione': ('schede',      'validazione', "scheda da far firmare a un osteopata (consegna/validazione-animazioni.md)"),
    'stato':      ('stato',        'stato',       "cosa e fatto e qual e la prossima fase (senza slug: video, inbox, strumenti, RAM, disco)"),
    'libreria':   ('libreria',     'libreria',    "indice del B-roll comune (libreria/): tecnica, volti, movimento, fogli"),
    'versione':   ('versione',     'versione',    "nuova versione di un video: stesso girato, stessi tagli (la grafica si rifa)"),
    'materiali':  ('sorgente',     'materiali',   "materiali del video e della libreria, nell'ordine di ricerca"),
    'dove':       ('stato',        'dove',        "un istante del video consegnato -> sorgente, giunta, pezzo"),
    'campionario': ('scena',       'campionario', "modelli premium su pezzi veri (campionario[/v2]/campionario.json)"),
    'catalogo':   ('catalogo',     'catalogo',    "catalogo dei modelli (attivi, varianti, vietati) e uso nei video precedenti"),
    'regressione': ('regressione', 'regressione', "un esempio per ogni modello attivo (campionario/regressione/): `./mve regressione tutti`"),
}


def main(argv=None):
    ap = argparse.ArgumentParser(prog='mve', description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='fase', required=True)
    for k, (_, _, d) in FASI.items():
        sp = sub.add_parser(k, help=d)
        if k == 'libreria':
            continue                      # non riguarda un video: niente slug
        if k == 'init':
            sp.add_argument('file', help="file di camera, o la cartella inbox/<SLUG>/ (girato, copione e materiali/)")
            sp.add_argument('slug', nargs='?')
            sp.add_argument('--copione', help="testo del video (.md o .txt) -> copione.md")
        elif k in ('stato', 'catalogo'):
            sp.add_argument('slug', nargs='?')
        else:
            sp.add_argument('slug')
        if k in ('consegna', 'validazione'):
            sp.add_argument('--rifai', action='store_true', default=None,
                            help="riscrive validazione-animazioni.md anche se c'e gia (attenzione: firme perse)")
        if k == 'versione':
            sp.add_argument('nuovo', help="slug della nuova versione, es. <slug>_v2")
        if k == 'dove':
            sp.add_argument('tempo', help="m:ss o secondi del video consegnato")
        if k == 'campionario':
            sp.add_argument('--solo', help="modelli da fare, es. 2,5,09a")
            sp.add_argument('--rifai', action='store_true', default=None, help="ignora la cache")
            sp.add_argument('--v2', action='store_true', default=None, help="campionario v2 (campionario/v2/)")
        if k == 'regressione':
            sp.add_argument('--solo', help="casi da rifare, es. connettore,chip")
            sp.add_argument('--riferimento', action='store_true', default=None,
                            help="i fotogrammi di adesso diventano il riferimento (dopo averli guardati)")
            sp.add_argument('--accetta', dest='accetta_', help="casi CAMBIATI guardati: ultimo/ diventa riferimento/ senza ricostruire")
        if k in ('monta', 'inserti', 'scena'):
            sp.add_argument('--solo', help="pezzi o inserti da rifare, es. 3,7,12")
        if k in ('finale', 'shorts'):
            sp.add_argument('--limite', type=float, help="solo i primi N secondi (prova)")
        if k == 'finale':
            sp.add_argument('--anteprima', action='store_true', default=None,
                            help="versione da approvare: 960x540, veloce, con foglio dei momenti e tempi")
        if k == 'anteprima':
            sp.add_argument('tempi', nargs='*', type=float)
        if k == 'shorts':
            sp.add_argument('--solo', help="indici degli short da fare, es. 0,2")
    a = ap.parse_args(argv)
    mod, fn, _ = FASI[a.fase]
    f = getattr(importlib.import_module(f'motore.{mod}'), fn)
    kw = {k: v for k, v in vars(a).items() if k not in ('fase',) and v is not None}
    if a.fase == 'libreria':
        f()
        return 0
    t0 = time.time()
    if a.fase == 'init':
        slug = f(kw['file'], kw.get('slug'), kw.get('copione'))
        registra_tempo(slug, 'init', time.time() - t0, 'ok')
        return 0
    slug = kw.pop('slug', None)
    if slug is None:
        if a.fase == 'stato':
            from .stato import panoramica
            panoramica()
        else:
            f()
        return 0
    if a.fase in SOLO_LETTURA:
        f(slug, **kw)
        return 0
    esito = 'interrotta'
    try:
        f(slug, **kw)
        esito = 'ok'
    except SystemExit as e:
        esito = 'ok' if e.code in (None, 0) else 'errore'
        raise
    except Exception:
        esito = 'errore'
        raise
    finally:
        try:
            registra_tempo(slug, a.fase + (' --anteprima' if kw.get('anteprima') else ''), time.time() - t0, esito)
        except Exception as e:                 # la riga dei tempi non deve mai far fallire la fase
            print(f"  (tempi.md non aggiornato: {e})", file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())

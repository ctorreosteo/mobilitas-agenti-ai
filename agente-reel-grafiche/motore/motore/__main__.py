"""mve — il motore dell'agente reel-grafiche di @Studio_Mobilitas: grafiche e infografiche sopra un reel 9:16 già montato.

    ./mve reel-<comando> <slug> [opzioni]      (./mve -h per l'elenco)

Le tappe sono quelle di CLAUDE.md (§ 6). `./mve reel-stato <slug>` dice la tappa e a chi tocca; senza slug, la coda.
"""
import argparse
import datetime
import importlib
import os
import sys
import time

# comandi che non cambiano niente di un reel: non vanno in tempi.md
SOLO_LETTURA = {'reel-prova', 'reel-stato', 'reel-reference', 'reel-posto'}


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
    # comando: (modulo, funzione, descrizione)
    # agente reel-grafiche (nato nel laboratorio, fase 4, 04/11/2026; la storia dei nomi è in VERSIONE.md)
    'reel-init':        ('reel_flusso', 'init', "reel: nuovo reel da inbox/<SLUG>/ (video 1080x1920 + SRT), videos/<slug>/reel.json"),
    'reel-radiografia': ('reel_radiografia_base', 'radiografia', "reel tappa 1: tagli, finestre, sottotitoli, voce, zone -> radiografia.json"),
    'reel-3d':          ('reel_radiografia_base', 'segna_3d', "reel: l'agente segna le inquadrature con le animazioni 3D (n,n | nessuna)"),
    'reel-tipo':        ('reel_radiografia_base', 'segna_tipo', "reel: l'agente corregge il tipo di inquadratura (n,n «persona in camera»|«B-roll pieno»)"),
    'reel-scena':       ('reel_radiografia_base', 'segna_scena', "reel: le scritte di scena (insegne, magliette) non bloccano le grafiche; resta solo «tieni»"),
    'reel-piano':       ('reel_piano_base', 'piano', "reel tappa 2: controlla piano.json e fa la tavola visiva (niente fermata: avanti col render)"),
    'reel-approva':     ('reel_flusso', 'approva', "reel: registra l'ok di Riccardo (piano | anteprime), legato all'md5"),
    'reel-rendi':       ('reel_rendi', 'rendi', "reel tappa 3: render, anteprime, zone Meta, controlli automatici, pacchi del direttore"),
    'reel-voto':        ('reel_flusso', 'voto', "reel: voto del direttore artistico per una grafica"),
    'reel-guardato':    ('reel_flusso', 'guardato', "reel: una lettura di Vision guardata sull'immagine dall'agente"),
    'reel-consegna':    ('reel_flusso', 'consegna', "reel tappa 4: copia approvata in consegna/ + consegna.md"),
    'reel-stato':       ('reel_flusso', 'stato', "reel: dove sta un reel e cosa viene dopo (senza slug: la coda)"),
    'reel-coda':        ('reel_flusso', 'coda', "reel: la coda di inbox/; --avanza fa le tappe del motore fino al primo fermo"),
    'reel-pulisci':     ('reel_flusso', 'pulisci', "reel: svuota .lavoro/<slug>/ (solo quella)"),
    'reel-regressione': ('reel_regressione', 'regressione', "reel: rifà da zero l'esempio fisso AD_CERVICALGIA e lo confronta col riferimento"),
    'reel-reference':   ('reel_reference', 'stato', "reel: procedura «studio reference»: quali reference hanno la scheda e quali no"),
    'reel-posto':       ('reel_piano', 'posto', "reel: dove sta libero un riquadro w×h in un tratto di fotogrammi (zone libere della radiografia)"),
    'reel-prova':       ('reel_prova', 'prova', "reel: prova veloce di UNA grafica del piano sopra il video base, in alcuni istanti (foglio in .lavoro/<slug>/prova/)"),
    'reel-ritmo-reference': ('reel_reference', 'ritmo', "reel: ritmo delle reference (eventi visivi ogni 10 s) dalle schede -> libreria/reference/ritmo.json"),
}


def main(argv=None):
    ap = argparse.ArgumentParser(prog='mve', description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='fase', required=True)
    for k, (_, _, d) in FASI.items():
        sp = sub.add_parser(k, help=d)
        if k in ('reel-reference', 'reel-ritmo-reference'):
            continue                      # non riguarda un reel: niente slug
        if k == 'reel-coda':
            sp.add_argument('--avanza', action='store_true', default=None, help="fa le tappe del motore, un reel dopo l'altro")
            continue
        if k == 'reel-regressione':
            sp.add_argument('--riferimento', action='store_true', default=None,
                            help="il risultato di adesso diventa il riferimento (dopo averlo guardato)")
            continue
        if k == 'reel-init':
            sp.add_argument('file', help="la cartella inbox/<SLUG>/ (o il video dentro)")
            sp.add_argument('slug', nargs='?')
            continue
        if k == 'reel-stato':
            sp.add_argument('slug', nargs='?')
        else:
            sp.add_argument('slug')
        if k == 'reel-posto':
            for a_ in ('f0', 'f1', 'w', 'h'):
                sp.add_argument(a_)
        if k == 'reel-prova':
            sp.add_argument('grafica', help="nome della grafica nel piano")
            sp.add_argument('tempi', nargs='+', help="secondi del reel, es. 1.2 4.5 6.0")
        if k == 'reel-3d':
            sp.add_argument('inquadrature', help="numeri delle inquadrature con le 3D, es. 3,9; oppure nessuna")
            sp.add_argument('--nota')
        if k == 'reel-tipo':
            sp.add_argument('inquadrature', help="numeri delle inquadrature, es. 21,22")
            sp.add_argument('tipo', help="«persona in camera» o «B-roll pieno»")
            sp.add_argument('--nota')
        if k == 'reel-scena':
            sp.add_argument('tieni', help="espressione delle scritte del montaggio da tenere (le altre sono di scena)")
            sp.add_argument('--nota')
        if k == 'reel-approva':
            sp.add_argument('cosa', choices=['piano', 'anteprime'])
            sp.add_argument('--da', help="chi approva e dove (default: Riccardo, in chat)")
        if k == 'reel-voto':
            sp.add_argument('grafica'); sp.add_argument('voto')
            sp.add_argument('--giro'); sp.add_argument('--nota')
        if k == 'reel-guardato':
            sp.add_argument('chiave', help="f<fotogramma>:<testo letto>, come in controlli.md"); sp.add_argument('motivo')
        if k == 'reel-rendi':
            sp.add_argument('--laboratorio', action='store_true', default=None,
                            help="anteprima di laboratorio senza approvazione del piano (solo piani con \"laboratorio\": true)")
        if k == 'reel-consegna':
            sp.add_argument('--prova', action='store_true', default=None, help="prova del comando in .lavoro/<slug>/ (senza approvazione)")
    a = ap.parse_args(argv)
    mod, fn, _ = FASI[a.fase]
    f = getattr(importlib.import_module(f'motore.{mod}'), fn)
    kw = {k: v for k, v in vars(a).items() if k not in ('fase',) and v is not None}
    fase = a.fase
    if fase in ('reel-reference', 'reel-ritmo-reference'):
        f()
        return 0
    if fase in ('reel-coda', 'reel-regressione'):
        f(**kw)
        return 0
    if fase == 'reel-init':
        slug = f(kw['file'], kw.get('slug'))
        registra_tempo(slug, a.fase, time.time() - t0 if 't0' in dir() else 0, 'ok')
        return 0
    t0 = time.time()
    slug = kw.pop('slug', None)
    if slug is None:
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

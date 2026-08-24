#!/usr/bin/env python3
"""
Collaudo deterministico di un atto difensivo: confronta DUE versioni e verifica
CONSERVAZIONE e INTEGRITA' DELLE CITAZIONI.

Non giudica la qualita'. Verifica che, cambiando le parole, non sia cambiato
quello che l'atto dice, cita e prova.

Va eseguito DUE VOLTE, una per passaggio, perche' due riscritture misurate in
blocco si compensano a vicenda — se la prima perde e la seconda aggiunge, i
conti tornano e la perdita non si vede:

  v5 -> v6 (chiarezza)  --delta-min -5 --delta-max 10
  v6 -> v7 (lingua)     --delta-min -3 --delta-max 5 --min-identita 60

Il riconoscimento dei riferimenti sta in riferimenti.py, condiviso con l'hook
che blocca le citazioni in scrittura: se i due riconoscessero forme diverse,
il cancello e l'hook si coprirebbero le spalle a vicenda solo per finta.

Per il collaudo di UNA versione sola — struttura, domande, etichette, allegati,
piede — serve invece verifica_atto.py.

Uso:
  verifica_citazioni.py PRIMA.md DOPO.md [--registro registro-fonti.md]
                        [--delta-min -5] [--delta-max 10] [--min-identita 0]
                        [--passaggio CHIAREZZA]

Uscita: 0 se nessun bloccante, 1 se ce ne sono.
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from riferimenti import (ETICHETTE, RE_PAS, RE_PERSONA, RE_PIEDE, allegati, articoli,
                         citazioni, date, etichette, importi, normalizza, norme,
                         registro_livelli)

# Verbi che si irrigidiscono tipicamente in una riscrittura: la frase corta e'
# piu' assertiva per costruzione, e "risulterebbe" diventa "risulta" senza che
# nessuno lo decida.
VERBI_CAUTI = ('risulterebbe', 'sembrerebbe', 'parrebbe', 'potrebbe', 'appare',
               'e compatibile', 'sarebbe', 'avrebbe', 'e verosimile',
               'si ritiene', 'consta', 'salvo verifica', 'nella maggior parte dei casi')


def leggi(p: str) -> str:
    f = Path(p)
    if not f.exists():
        print(f"ERRORE: file non trovato: {p}", file=sys.stderr)
        sys.exit(2)
    return f.read_text(encoding='utf-8')


def parole(t: str) -> int:
    return len(t.split())


def frasi(t: str):
    """Spezza in frasi, ignorando righe di tabella e titoli."""
    corpo = [r.strip() for r in t.splitlines()
             if r.strip() and not r.strip().startswith(('#', '|', '---'))]
    grezze = re.split(r'(?<=[.!?;:])\s+', ' '.join(corpo))
    return [normalizza(f) for f in grezze if len(f.split()) >= 4]


def titoli(t: str):
    return [normalizza(r.lstrip('#').strip()) for r in t.splitlines() if r.strip().startswith('#')]


def verbi_cauti(t: str):
    n = normalizza(t)
    return {v: n.count(normalizza(v)) for v in VERBI_CAUTI if n.count(normalizza(v)) > 0}


def main():
    ap = argparse.ArgumentParser(description='Collaudo di conservazione e citazioni di un atto.')
    ap.add_argument('prima')
    ap.add_argument('dopo')
    ap.add_argument('--registro', default=None,
                    help='registro-fonti.md: le sentenze citate vanno confrontate con questo')
    ap.add_argument('--delta-min', type=float, default=-5.0)
    ap.add_argument('--delta-max', type=float, default=10.0)
    ap.add_argument('--min-identita', type=float, default=0.0,
                    help='percentuale minima di frasi identiche (0 = nessuna soglia)')
    ap.add_argument('--passaggio', default='NON DICHIARATO',
                    help='CHIAREZZA (v5->v6) o LINGUA (v6->v7)')
    a = ap.parse_args()

    A, B = leggi(a.prima), leggi(a.dopo)
    bloccanti, avvisi = [], []
    blocca = lambda tipo, msg: bloccanti.append(f"[{tipo}] {msg}")
    avvisa = lambda tipo, msg: avvisi.append(f"[{tipo}] {msg}")

    # --- lunghezza -----------------------------------------------------------
    pa, pb = parole(A), parole(B)
    delta = ((pb - pa) / pa * 100) if pa else 0.0
    if delta < a.delta_min:
        blocca('DELTA_LUNGHEZZA',
               f"{delta:+.1f}% (minimo {a.delta_min:+.0f}%): sotto la soglia si e' perso contenuto")
    elif delta > a.delta_max:
        blocca('DELTA_LUNGHEZZA',
               f"{delta:+.1f}% (massimo {a.delta_max:+.0f}%): sopra la soglia si e' aggiunto contenuto")

    # --- identita' delle frasi ----------------------------------------------
    fa, fb = frasi(A), frasi(B)
    setb = set(fb)
    identiche = sum(1 for f in fa if f in setb)
    quota = (identiche / len(fa) * 100) if fa else 0.0
    if a.min_identita > 0 and quota < a.min_identita:
        blocca('HA_RISCRITTO_INVECE_DI_CORREGGERE',
               f"solo il {quota:.0f}% delle frasi e' rimasto identico (minimo {a.min_identita:.0f}%): "
               f"e' una riscrittura, non una revisione di lingua")

    # --- citazioni -----------------------------------------------------------
    sa, sb = citazioni(A), citazioni(B)
    for s in sorted(sa - sb):
        blocca('CITAZIONE_PERSA', f"citazione n. {s} presente PRIMA e assente DOPO")
    for s in sorted(sb - sa):
        blocca('CITAZIONE_COMPARSA',
               f"citazione n. {s} COMPARSA nella riscrittura: non e' mai passata da una verifica")

    if a.registro:
        liv = registro_livelli(a.registro)
        if liv is None:
            avvisa('REGISTRO_ASSENTE', f"registro non trovato: {a.registro}")
        else:
            for s in sorted(sb):
                stato = liv.get(s)
                if stato is None:
                    blocca('CITAZIONE_NON_REGISTRATA',
                           f"n. {s} citata nell'atto e assente dal registro delle fonti")
                elif stato != 'CONFERMATA':
                    blocca('CITAZIONE_NON_CONFERMATA',
                           f"n. {s} registrata come {stato}: il principio si cita, il numero no")

    ara, arb = articoli(A), articoli(B)
    for x in sorted(ara - arb):
        blocca('ARTICOLO_PERSO', f"{x} presente PRIMA e assente DOPO")
    for x in sorted(arb - ara):
        avvisa('ARTICOLO_COMPARSO', f"{x} comparso DOPO: verificare che sia corretto")

    la, lb = norme(A), norme(B)
    for x in sorted(la - lb):
        blocca('NORMA_PERSA', f"{x} presente PRIMA e assente DOPO")
    for x in sorted(lb - la):
        avvisa('NORMA_COMPARSA', f"{x} comparsa DOPO: verificare")

    # --- etichette di prova --------------------------------------------------
    ea, eb = etichette(A), etichette(B)
    for k in ETICHETTE:
        if eb[k] < ea[k]:
            blocca('ETICHETTA_PERSA', f"{k}: {ea[k]} PRIMA, {eb[k]} DOPO")
    if eb['PROVATO'] > ea['PROVATO'] and (eb['ALLEGABILE'] < ea['ALLEGABILE']
                                          or eb['DOCUMENTABILE'] < ea['DOCUMENTABILE']):
        blocca('ETICHETTA_ALZATA',
               f"PROVATO passa da {ea['PROVATO']} a {eb['PROVATO']} mentre le etichette piu' basse "
               f"calano: un fatto e' stato promosso")
    if eb['NON SOSTENIBILE'] > 0:
        blocca('NON_SOSTENIBILE_IN_ATTO',
               f"{eb['NON SOSTENIBILE']} occorrenze di NON SOSTENIBILE: non deve stare in un atto")

    # --- allegati, date, importi ---------------------------------------------
    for nome, fa_, fb_, tipo in (
        ('allegato', allegati(A), allegati(B), 'ALLEGATO_PERSO'),
        ('data', date(A), date(B), 'DATA_PERSA'),
        ('importo', importi(A), importi(B), 'IMPORTO_PERSO'),
    ):
        for x in sorted(fa_ - fb_, key=str):
            blocca(tipo, f"{nome} {x} presente PRIMA e assente DOPO")
        for x in sorted(fb_ - fa_, key=str):
            avvisa(tipo.replace('PERSO', 'COMPARSO'), f"{nome} {x} comparso DOPO")

    # --- struttura -----------------------------------------------------------
    ta, tb = titoli(A), titoli(B)
    if len(ta) != len(tb):
        avvisa('STRUTTURA_ALTERATA', f"titoli: {len(ta)} PRIMA, {len(tb)} DOPO")
    for t in ta:
        if t not in tb and not difflib.get_close_matches(t, tb, n=1, cutoff=0.75):
            blocca('SEZIONE_PERSA', f"sezione \"{t}\" presente PRIMA e non ritrovata DOPO")

    # --- verbi irrigiditi ----------------------------------------------------
    va, vb = verbi_cauti(A), verbi_cauti(B)
    for v, n in va.items():
        m = vb.get(v, 0)
        if m < n:
            avvisa('VERBO_IRRIGIDITO',
                   f"\"{v}\": {n} occorrenze PRIMA, {m} DOPO. Verificare che l'atto non affermi "
                   f"piu' di quanto provi")

    # --- cio' che una riscrittura non puo' INTRODURRE ------------------------
    # Il collaudo verifica la conservazione, non la qualita': se un difetto c'era
    # gia' nella v5 non e' un suo rilievo. Ma se compare adesso, e' nato qui.
    for tipo, rx, spiega in (
        ('PAS_INTRODOTTA', RE_PAS,
         "una riscrittura ha introdotto il lessico dell'alienazione parentale, che non ha "
         "ingresso nel processo: si torna alle condotte documentate"),
        ('ATTACCO_ALLA_PERSONA_INTRODOTTO', RE_PERSONA,
         "una riscrittura ha trasformato una condotta in una qualificazione della persona: "
         "e' il difetto che rende conflittuale chi deposita l'atto"),
    ):
        ma, mb = rx.search(A), rx.search(B)
        if mb and not ma:
            blocca(tipo, f"\"{' '.join(mb.group(0).split())[:80]}\" — {spiega}")

    # --- piede ---------------------------------------------------------------
    if not RE_PIEDE.search(B):
        blocca('PIEDE_MANCANTE',
               "manca la clausola sulla revisione del difensore iscritto all'albo")

    # --- rapporto ------------------------------------------------------------
    print('=' * 78)
    print(f"COLLAUDO  {Path(a.prima).name}  ->  {Path(a.dopo).name}")
    print(f"Passaggio: {a.passaggio}")
    print('=' * 78)
    print(f"Parole:            {pa} -> {pb}  ({delta:+.1f}%)   "
          f"[ammesso {a.delta_min:+.0f}% / {a.delta_max:+.0f}%]")
    print(f"Frasi identiche:   {identiche}/{len(fa)}  ({quota:.0f}%)"
          + (f"   [minimo {a.min_identita:.0f}%]" if a.min_identita else "   [nessuna soglia]"))
    print(f"Citazioni:         {len(sa)} -> {len(sb)}")
    print(f"Articoli:          {len(ara)} -> {len(arb)}")
    print(f"Allegati:          {len(allegati(A))} -> {len(allegati(B))}")
    print(f"Date:              {len(date(A))} -> {len(date(B))}")
    print("Etichette:         " + '  '.join(f"{k}:{ea[k]}->{eb[k]}" for k in ETICHETTE))
    print()

    if bloccanti:
        print(f"BLOCCANTI ({len(bloccanti)}) — nate nel passaggio {a.passaggio}")
        for b in bloccanti:
            print(f"  {b}")
        print()
    if avvisi:
        print(f"AVVISI ({len(avvisi)})")
        for v in avvisi:
            print(f"  {v}")
        print()

    if bloccanti:
        print("ESITO: NON DEPOSITABILE — le violazioni bloccanti vanno riparate.")
        return 1
    print("ESITO: nessuna violazione bloccante. Resta la lettura semantica del collaudatore.")
    return 0


if __name__ == '__main__':
    sys.exit(main())

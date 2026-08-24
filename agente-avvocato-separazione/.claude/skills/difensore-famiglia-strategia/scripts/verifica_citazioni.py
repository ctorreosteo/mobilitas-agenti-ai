#!/usr/bin/env python3
"""
Collaudo deterministico di un atto difensivo: confronta due versioni e verifica
CONSERVAZIONE e INTEGRITA' DELLE CITAZIONI.

Non giudica la qualita'. Verifica che, cambiando le parole, non sia cambiato
quello che l'atto dice, cita e prova.

Va eseguito DUE VOLTE, una per passaggio, perche' due riscritture misurate in
blocco si compensano a vicenda:

  v5 -> v6 (chiarezza)  --delta-min -5 --delta-max 10
  v6 -> v7 (lingua)     --delta-min -3 --delta-max 5 --min-identita 60

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
import unicodedata
from pathlib import Path

# ----------------------------------------------------------------------------
# Estrattori. Ogni elemento che l'atto NON puo' perdere ha il suo pattern.
# ----------------------------------------------------------------------------

# "Cass. n. 1234/2020", "Cassazione 1234/2020", "n. 1234/2020", "sent. 1234/2020"
RE_SENTENZA = re.compile(
    r'(?:Cass(?:azione)?\.?(?:\s+(?:civ|pen|SS\.?UU|Sez\.?\s*Un)\.?)?|sent(?:enza)?\.?|ord(?:inanza)?\.?)'
    r'[\s,]*n?\.?\s*(\d{1,6})\s*/\s*(\d{4})',
    re.IGNORECASE)

# "art. 337-ter c.c.", "artt. 574 e 574-bis c.p.", "art. 473-bis.39 c.p.c."
RE_ARTICOLO = re.compile(
    r'artt?\.\s*([0-9]+(?:[\-\.][a-zA-Z0-9]+)*)\s*(?:e\s*([0-9]+(?:[\-\.][a-zA-Z0-9]+)*)\s*)?'
    r'(c\.c\.|c\.p\.c\.|c\.p\.p\.|c\.p\.|Cost\.)',
    re.IGNORECASE)

# "L. 76/2016", "D.Lgs. 149/2022", "D.L. 117/2025", "DPR 131/2021"
RE_LEGGE = re.compile(
    r'\b(L\.|D\.?Lgs\.?|D\.?L\.?|D\.?P\.?R\.?|D\.?P\.?C\.?M\.?)\s*n?\.?\s*(\d{1,4})\s*/\s*(\d{4})',
    re.IGNORECASE)

# Etichette di prova
ETICHETTE = ('PROVATO', 'DOCUMENTABILE', 'ALLEGABILE', 'NON SOSTENIBILE')
RE_ETICHETTA = re.compile(r'\b(NON SOSTENIBILE|PROVATO|DOCUMENTABILE|ALLEGABILE)\b')

# "all. 8", "allegato 12", "all. 4, 5"
RE_ALLEGATO = re.compile(r'\ball(?:egat[oi])?\.?\s*n?\.?\s*((?:\d+\s*[,e]\s*)*\d+)', re.IGNORECASE)

# Date: 14/03/2026, 14 marzo 2026
MESI = ('gennaio febbraio marzo aprile maggio giugno luglio agosto '
        'settembre ottobre novembre dicembre')
RE_DATA_NUM = re.compile(r'\b(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})\b')
RE_DATA_TXT = re.compile(r'\b(\d{1,2})\s+(' + '|'.join(MESI.split()) + r')\s+(\d{4})\b', re.IGNORECASE)

# Importi e percentuali
RE_IMPORTO = re.compile(r'(?:€|euro)\s*([\d.]+(?:,\d{1,2})?)|([\d.]+(?:,\d{1,2})?)\s*(?:€|euro)', re.IGNORECASE)
RE_PERCENT = re.compile(r'\b(\d{1,3}(?:,\d+)?)\s*%')

# Verbi che si irrigidiscono tipicamente in una riscrittura
VERBI_CAUTI = ('risulterebbe', 'sembrerebbe', 'parrebbe', 'potrebbe', 'appare',
               'è compatibile', 'e compatibile', 'sarebbe', 'avrebbe',
               'è verosimile', 'si ritiene', 'consta')

PIEDE = 'difensore iscritto all’albo'
PIEDE_ALT = "difensore iscritto all'albo"


def norm(s: str) -> str:
    """Normalizza per il confronto: minuscole, spazi collassati, apostrofi unificati."""
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('’', "'").replace('‘', "'")
    s = re.sub(r'\s+', ' ', s)
    return s.strip().lower()


def leggi(p: str) -> str:
    f = Path(p)
    if not f.exists():
        print(f"ERRORE: file non trovato: {p}", file=sys.stderr)
        sys.exit(2)
    return f.read_text(encoding='utf-8')


def parole(t: str) -> int:
    return len(t.split())


def frasi(t: str):
    """Spezza in frasi, ignorando le righe di tabella e i titoli."""
    corpo = []
    for riga in t.splitlines():
        r = riga.strip()
        if not r or r.startswith('#') or r.startswith('|') or r.startswith('---'):
            continue
        corpo.append(r)
    testo = ' '.join(corpo)
    grezze = re.split(r'(?<=[.!?;:])\s+', testo)
    return [norm(f) for f in grezze if len(f.split()) >= 4]


def sentenze(t: str):
    return {f"{m.group(1)}/{m.group(2)}" for m in RE_SENTENZA.finditer(t)}


def articoli(t: str):
    out = set()
    for m in RE_ARTICOLO.finditer(t):
        codice = m.group(3).lower().replace(' ', '')
        out.add(f"art. {m.group(1)} {codice}")
        if m.group(2):
            out.add(f"art. {m.group(2)} {codice}")
    return out


def leggi_rif(t: str):
    return {f"{m.group(1).upper().replace('.', '')} {m.group(2)}/{m.group(3)}"
            for m in RE_LEGGE.finditer(t)}


def etichette(t: str):
    """Conta le etichette per tipo."""
    c = dict.fromkeys(ETICHETTE, 0)
    for m in RE_ETICHETTA.finditer(t):
        c[m.group(1)] += 1
    return c


def allegati(t: str):
    out = set()
    for m in RE_ALLEGATO.finditer(t):
        for n in re.findall(r'\d+', m.group(1)):
            out.add(int(n))
    return out


def date(t: str):
    out = set()
    for m in RE_DATA_NUM.finditer(t):
        g, ms, a = int(m.group(1)), int(m.group(2)), m.group(3)
        a = ('20' + a) if len(a) == 2 else a
        out.add(f"{g:02d}/{ms:02d}/{a}")
    mesi = MESI.split()
    for m in RE_DATA_TXT.finditer(t):
        g = int(m.group(1))
        ms = mesi.index(m.group(2).lower()) + 1
        out.add(f"{g:02d}/{ms:02d}/{m.group(3)}")
    return out


def importi(t: str):
    out = set()
    for m in RE_IMPORTO.finditer(t):
        v = m.group(1) or m.group(2)
        if v:
            out.add(v.replace('.', '').replace(',', '.'))
    for m in RE_PERCENT.finditer(t):
        out.add(m.group(1) + '%')
    return out


def titoli(t: str):
    return [norm(r.lstrip('#').strip()) for r in t.splitlines() if r.strip().startswith('#')]


def verbi_cauti(t: str):
    n = norm(t)
    return {v: n.count(norm(v)) for v in VERBI_CAUTI if n.count(norm(v)) > 0}


def registro_sentenze(p: str):
    """Numeri di sentenza presenti nel registro delle fonti verificate."""
    f = Path(p)
    if not f.exists():
        return None
    testo = f.read_text(encoding='utf-8')
    # esclude la sezione delle fonti NON trovate
    tagli = re.split(r'^##\s+Fonti cercate e NON trovate', testo, flags=re.MULTILINE)
    return sentenze(tagli[0])


# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description='Collaudo di conservazione e citazioni di un atto.')
    ap.add_argument('prima')
    ap.add_argument('dopo')
    ap.add_argument('--registro', default=None,
                    help='registro-fonti.md: se indicato, le sentenze citate vanno confrontate')
    ap.add_argument('--delta-min', type=float, default=-5.0)
    ap.add_argument('--delta-max', type=float, default=10.0)
    ap.add_argument('--min-identita', type=float, default=0.0,
                    help='percentuale minima di frasi identiche (0 = nessuna soglia)')
    ap.add_argument('--passaggio', default='NON DICHIARATO',
                    help='CHIAREZZA (v5->v6) o LINGUA (v6->v7)')
    a = ap.parse_args()

    A, B = leggi(a.prima), leggi(a.dopo)
    bloccanti, avvisi = [], []

    def blocca(tipo, msg):
        bloccanti.append(f"[{tipo}] {msg}")

    def avvisa(tipo, msg):
        avvisi.append(f"[{tipo}] {msg}")

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
    sa, sb = sentenze(A), sentenze(B)
    for s in sorted(sa - sb):
        blocca('CITAZIONE_PERSA', f"sentenza n. {s} presente PRIMA e assente DOPO")
    for s in sorted(sb - sa):
        blocca('CITAZIONE_COMPARSA',
               f"sentenza n. {s} COMPARSA nella riscrittura: non e' mai stata verificata")

    if a.registro:
        reg = registro_sentenze(a.registro)
        if reg is None:
            avvisa('REGISTRO_ASSENTE', f"registro non trovato: {a.registro}")
        else:
            for s in sorted(sb - reg):
                blocca('CITAZIONE_NON_REGISTRATA',
                       f"sentenza n. {s} citata nell'atto e NON presente nel registro come verificata")

    ara, arb = articoli(A), articoli(B)
    for x in sorted(ara - arb):
        blocca('ARTICOLO_PERSO', f"{x} presente PRIMA e assente DOPO")
    for x in sorted(arb - ara):
        avvisa('ARTICOLO_COMPARSO', f"{x} comparso DOPO: verificare che sia corretto")

    la, lb = leggi_rif(A), leggi_rif(B)
    for x in sorted(la - lb):
        blocca('NORMA_PERSA', f"{x} presente PRIMA e assente DOPO")
    for x in sorted(lb - la):
        avvisa('NORMA_COMPARSA', f"{x} comparsa DOPO: verificare")

    # --- etichette di prova --------------------------------------------------
    ea, eb = etichette(A), etichette(B)
    for k in ETICHETTE:
        if eb[k] < ea[k]:
            blocca('ETICHETTA_PERSA', f"{k}: {ea[k]} PRIMA, {eb[k]} DOPO")
    # un'etichetta piu' alta e meno etichette basse = probabile innalzamento
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
        if t not in tb:
            close = difflib.get_close_matches(t, tb, n=1, cutoff=0.75)
            if not close:
                blocca('SEZIONE_PERSA', f"sezione \"{t}\" presente PRIMA e non ritrovata DOPO")

    # --- verbi irrigiditi ----------------------------------------------------
    va, vb = verbi_cauti(A), verbi_cauti(B)
    for v, n in va.items():
        m = vb.get(v, 0)
        if m < n:
            avvisa('VERBO_IRRIGIDITO',
                   f"\"{v}\": {n} occorrenze PRIMA, {m} DOPO. Verificare che l'atto non affermi "
                   f"piu' di quanto provi")

    # --- piede ---------------------------------------------------------------
    nb = norm(B)
    if norm(PIEDE) not in nb and norm(PIEDE_ALT) not in nb:
        blocca('PIEDE_MANCANTE',
               "manca la clausola sulla revisione del difensore iscritto all'albo")

    # --- rapporto ------------------------------------------------------------
    print('=' * 74)
    print(f"COLLAUDO  {Path(a.prima).name}  ->  {Path(a.dopo).name}")
    print(f"Passaggio: {a.passaggio}")
    print('=' * 74)
    print(f"Parole:            {pa} -> {pb}  ({delta:+.1f}%)   "
          f"[ammesso {a.delta_min:+.0f}% / {a.delta_max:+.0f}%]")
    print(f"Frasi identiche:   {identiche}/{len(fa)}  ({quota:.0f}%)"
          + (f"   [minimo {a.min_identita:.0f}%]" if a.min_identita else "   [nessuna soglia]"))
    print(f"Sentenze:          {len(sa)} -> {len(sb)}")
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

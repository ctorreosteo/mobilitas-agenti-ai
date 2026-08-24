#!/usr/bin/env python3
"""
Collaudo deterministico di UN atto — la checklist di qualita', fatta eseguire a
una macchina invece che dichiarare a chi ha scritto l'atto.

## Perche' esiste

Il metodo aveva due cancelli di qualita': una rubrica con un punteggio e una
checklist di si'/no. Li compilava lo stesso modello che aveva scritto l'atto,
subito dopo averlo scritto. Un controllo del genere non e' debole: e' assente.
Chi ha appena scritto "PROVATO" accanto a un fatto risponde "si'" alla domanda
"ogni etichetta e' corretta?", perche' se avesse pensato il contrario avrebbe
scritto un'altra etichetta.

Questo script verifica quello che si puo' verificare contando e confrontando —
il piede, le domande in prima pagina, le glosse delle etichette, gli allegati
citati e non mappati, i documenti che il rito pretende nell'atto introduttivo,
le citazioni non confermate, la lunghezza. Non e' il giudizio sull'atto: e' il
pavimento sotto al giudizio.

## Cosa NON fa, e perche' lo dichiara

Non decide se una data e' quella giusta, se un'etichetta e' meritata, se una
domanda e' opportuna. Le cose che una macchina non puo' accertare restano
AVVISI, con scritto accanto che vanno guardate a mano. Un cancello che finge di
sapere piu' di quanto sa produce la stessa illusione della checklist che ha
sostituito.

Uso:
  verifica_atto.py ATTO.md [--tipo ricorso|comparsa|memoria|reclamo|istanza]
                   [--registro registro-fonti.md] [--prove prove.md]
                   [--timeline timeline.md]
                   [--min-pagine 8] [--max-pagine 15] [--parole-pagina 450]

Uscita: 0 se nessun bloccante, 1 se ce ne sono.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from riferimenti import (RE_PAS, RE_PERSONA, RE_PIEDE, allegati, citazioni,
                         etichette, date, normalizza, registro_livelli)

# Gli atti introduttivi hanno un contenuto obbligatorio che il rito unificato ha
# spostato tutto in avanti: cio' che manca qui non si recupera dopo.
# Verificato il 24/08/2026 su artt. 473-bis.12 e 473-bis.16 c.p.c.
INTRODUTTIVI = ('ricorso', 'comparsa')

GLOSSE = {
    'PROVATO': (r'document[oi]\s+in\s+atti', r'in\s+atti', r'allegat'),
    'DOCUMENTABILE': (r'da\s+acquisire', r'documento\s+esistente', r'acquisizione'),
    'ALLEGABILE': (r'per\s+testi', r'presunzion', r'prova\s+orale', r'testimoni'),
}

BUROCRATESE = (
    r'in\s+ordine\s+a\b', r'porre\s+in\s+essere', r'si\s+rappresenta\s+che',
    r'provvedere\s+al\s+versamento', r'all[\'’]?uopo', r'de\s+quo',
    r'a\s+far\s+data\s+da', r'ebbene', r'orbene', r'per\s+quanto\s+sopra\s+esposto',
    r'e[\'’]?\s+stato\s+provveduto', r'venir[ee]\s+in\s+rilievo',
)


def leggi(p, obbligatorio=True):
    f = Path(p)
    if not f.exists():
        if obbligatorio:
            print(f"ERRORE: file non trovato: {p}", file=sys.stderr)
            sys.exit(2)
        return None
    return f.read_text(encoding='utf-8')


def righe_utili(testo):
    """Le righe di prosa: niente titoli, niente tabelle, niente separatori."""
    return [r.strip() for r in testo.splitlines()
            if r.strip() and not r.strip().startswith(('#', '|', '---', ':--'))]


def periodi(testo):
    grezzi = re.split(r'(?<=[.!?])\s+', ' '.join(righe_utili(testo)))
    return [g for g in grezzi if len(g.split()) >= 3]


def main():
    ap = argparse.ArgumentParser(description="Collaudo deterministico di un atto.")
    ap.add_argument('atto')
    ap.add_argument('--tipo', default='ricorso')
    ap.add_argument('--registro', default=None)
    ap.add_argument('--prove', default=None, help='mappa delle prove: prove.md')
    ap.add_argument('--timeline', default=None, help='cronologia: timeline.md')
    ap.add_argument('--min-pagine', type=float, default=8.0)
    ap.add_argument('--max-pagine', type=float, default=15.0)
    ap.add_argument('--parole-pagina', type=int, default=450)
    a = ap.parse_args()

    T = leggi(a.atto)
    N = normalizza(T)
    bloccanti, avvisi = [], []
    blocca = lambda tipo, msg: bloccanti.append(f"[{tipo}] {msg}")
    avvisa = lambda tipo, msg: avvisi.append(f"[{tipo}] {msg}")

    parole = len(T.split())
    pagine = parole / a.parole_pagina

    # --- 1. il piede ---------------------------------------------------------
    if not RE_PIEDE.search(T):
        blocca('PIEDE_MANCANTE',
               "manca la clausola sulla revisione del difensore iscritto all'albo. "
               "E' il confine fra materiale difensivo e atto processuale, e non ha eccezioni")

    # --- 2. i tre difetti che non entrano in un atto -------------------------
    if 'NON SOSTENIBILE' in T:
        blocca('NON_SOSTENIBILE_IN_ATTO',
               "l'etichetta NON SOSTENIBILE compare nell'atto. Significa che nulla sorregge il "
               "fatto: la controparte lo smonta e con quello contamina i fatti veri accanto")
    m = RE_PAS.search(T)
    if m:
        blocca('PAS_INVOCATA',
               f"\"{' '.join(m.group(0).split())}\" — la PAS non ha ingresso nel processo "
               f"italiano. Si scrivono condotte ostative documentate e si chiede "
               f"l'art. 473-bis.39 c.p.c.")
    m = RE_PERSONA.search(T)
    if m:
        blocca('ATTACCO_ALLA_PERSONA',
               f"\"{' '.join(m.group(0).split())[:90]}\" — si attaccano le condotte con le date, "
               f"mai la persona: il giudice difende la persona, e il tono e' materiale probatorio "
               f"a carico di chi deposita")

    # --- 3. le domande in prima pagina --------------------------------------
    prima_pagina = ' '.join(T.split()[:int(a.parole_pagina * 1.3)])
    ha_titolo = re.search(r'(?:^|\n)#{1,4}[^\n]*\b(domand|conclusion|chiede|voglia)',
                          T[:len(prima_pagina) + 400], re.IGNORECASE)
    ha_elenco = re.search(r'(?:^|\n)\s*(?:\d+[.)]|[a-h][.)])\s+\S', T[:len(prima_pagina) + 400])
    if not (ha_titolo and ha_elenco):
        blocca('DOMANDE_NON_IN_PRIMA_PAGINA',
               "nella prima pagina non si trovano insieme un titolo di domande/conclusioni e un "
               "elenco numerato. Il giudice che arriva a pagina sei senza sapere cosa chiedi ha "
               "letto male le prime cinque, e le domande vanno numerate per poter essere copiate "
               "nel dispositivo")

    # --- 4. la sezione sull'interesse del minore -----------------------------
    if not re.search(r'interesse\s+(?:del|superiore\s+del)\s+minor', N):
        blocca('INTERESSE_DEL_MINORE_ASSENTE',
               "l'atto non contiene la sezione sull'interesse del minore. E' il criterio che la "
               "legge riconosce al giudice e la sede in cui ogni domanda va tradotta: una domanda "
               "che non si traduce e' una domanda dell'adulto")

    # --- 5. le etichette e le loro glosse ------------------------------------
    conteggio = etichette(T)
    for riga in T.splitlines():
        r = riga.strip()
        if not r or r.startswith('|'):
            continue
        for et, forme in GLOSSE.items():
            if re.search(r'\b' + et + r'\b', r) and not any(
                    re.search(f, r, re.IGNORECASE) for f in forme):
                blocca('ETICHETTA_SENZA_GLOSSA',
                       f"\"{et}\" senza glossa in: \"{r[:80]}\". A pagina otto nessuno ricorda la "
                       f"differenza fra DOCUMENTABILE e ALLEGABILE: la glossa si ripete ogni volta")
                break

    if conteggio['DOCUMENTABILE'] and not re.search(r'istanza\s+di\s+acquisizione|si\s+chiede.{0,40}acquisi', N):
        avvisa('DOCUMENTABILE_SENZA_ISTANZA',
               f"{conteggio['DOCUMENTABILE']} fatti DOCUMENTABILE e nessuna istanza di "
               f"acquisizione: l'etichetta sta in un atto solo con l'istanza accanto")
    if conteggio['ALLEGABILE'] and not re.search(r'istruttor|prova\s+per\s+test|si\s+chiede.{0,40}testi', N):
        avvisa('ALLEGABILE_SENZA_ISTRUTTORIA',
               f"{conteggio['ALLEGABILE']} fatti ALLEGABILE e nessuna richiesta istruttoria: "
               f"l'etichetta sta in un atto solo con la richiesta a corredo")

    # --- 6. gli allegati -----------------------------------------------------
    citati = allegati(T)
    if citati and not re.search(r'indice\s+(?:degli\s+)?allegat|elenco\s+(?:degli\s+)?allegat', N):
        blocca('INDICE_ALLEGATI_MANCANTE',
               f"{len(citati)} allegati richiamati e nessun indice. Un faldone senza indice viene "
               f"sfogliato, non letto")
    prove = leggi(a.prove, obbligatorio=False) if a.prove else None
    if prove is not None:
        mappati = allegati(prove)
        orfani = sorted(citati - mappati)
        if orfani:
            blocca('ALLEGATO_NON_MAPPATO',
                   f"allegati richiamati nell'atto e assenti dalla mappa delle prove: "
                   f"{', '.join('all. ' + str(x) for x in orfani)}")
        inutilizzati = sorted(mappati - citati)
        if inutilizzati:
            avvisa('ALLEGATO_NON_RICHIAMATO',
                   f"documenti mappati e mai richiamati nell'atto: "
                   f"{', '.join('all. ' + str(x) for x in inutilizzati)}")

    # --- 7. cio' che il rito pretende nell'atto introduttivo -----------------
    if a.tipo.lower() in INTRODUTTIVI:
        if 'piano genitoriale' not in N:
            blocca('PIANO_GENITORIALE_ASSENTE',
                   "l'atto introduttivo non menziona il piano genitoriale, che il rito pretende "
                   "allegato quando ci sono figli minori (artt. 473-bis.12 e 473-bis.16 c.p.c.). "
                   "Ed e' anche la sede in cui un padre preparato si distingue: orari, nido, "
                   "pediatra, chi accompagna, come si gestiscono le malattie")
        mancanti = [nome for nome, rx in (
            ('dichiarazioni dei redditi degli ultimi tre anni', r'dichiarazion\w*\s+d\w+\s+redditi'),
            ('estratti conto degli ultimi tre anni', r'estratti\s+conto'),
        ) if not re.search(rx, N)]
        if mancanti:
            blocca('DOCUMENTAZIONE_ECONOMICA_ASSENTE',
                   f"non risultano allegati: {'; '.join(mancanti)}. Il rito li pretende con l'atto, "
                   f"non quando il giudice li chiede: un introduttivo senza documenti economici "
                   f"parte perdendo sul mantenimento")

    # --- 8. le citazioni -----------------------------------------------------
    citate = citazioni(T)
    if a.registro:
        liv = registro_livelli(a.registro)
        if liv is None:
            avvisa('REGISTRO_ASSENTE', f"registro non trovato: {a.registro}")
        else:
            for c in sorted(citate):
                stato = liv.get(c)
                if stato is None:
                    blocca('CITAZIONE_NON_REGISTRATA',
                           f"n. {c} citata e assente dal registro delle fonti verificate")
                elif stato != 'CONFERMATA':
                    blocca('CITAZIONE_NON_CONFERMATA',
                           f"n. {c} registrata come {stato}: si cita il principio, non il numero")

    # --- 9. le date ----------------------------------------------------------
    tl = leggi(a.timeline, obbligatorio=False) if a.timeline else None
    if tl is not None:
        fuori = sorted(date(T) - date(tl))
        if fuori:
            avvisa('DATA_FUORI_CRONOLOGIA',
                   f"date presenti nell'atto e non nella cronologia: {', '.join(fuori)}. "
                   f"Alcune saranno date di norme o di provvedimenti, ed e' corretto; ogni data "
                   f"di un FATTO che non sta in timeline.md non deve entrare in un atto. "
                   f"Vanno guardate a mano, una per una")

    # --- 10. lunghezza e forma ----------------------------------------------
    if pagine > a.max_pagine:
        blocca('TROPPO_LUNGO',
               f"{pagine:.1f} pagine stimate (massimo {a.max_pagine:.0f}). Oltre le venti l'atto "
               f"perde piu' di quanto guadagna: le parti forti annegano")
    elif pagine < a.min_pagine:
        avvisa('MOLTO_CORTO',
               f"{pagine:.1f} pagine stimate (minimo indicativo {a.min_pagine:.0f}): verifica che "
               f"non manchi una sezione")

    per = periodi(T)
    if per:
        lunghezze = [len(p.split()) for p in per]
        media = sum(lunghezze) / len(lunghezze)
        lunghi = [p for p in per if len(p.split()) > 35]
        if media > 25:
            avvisa('PERIODI_LUNGHI',
                   f"media di {media:.0f} parole per periodo (obiettivo 20, massimo 35)")
        if lunghi:
            avvisa('PERIODO_OLTRE_35_PAROLE',
                   f"{len(lunghi)} periodi oltre le 35 parole. Il primo: "
                   f"\"{' '.join(lunghi[0].split()[:14])}...\"")

    trovato_buro = sorted({re.search(b, N).group(0) for b in BUROCRATESE if re.search(b, N)})
    if trovato_buro:
        avvisa('BUROCRATESE', f"{len(trovato_buro)} formule da sostituire: {', '.join(trovato_buro)}")

    # --- rapporto ------------------------------------------------------------
    print('=' * 78)
    print(f"COLLAUDO DELL'ATTO  {Path(a.atto).name}   (tipo: {a.tipo})")
    print('=' * 78)
    print(f"Lunghezza:     {parole} parole  ~ {pagine:.1f} pagine   "
          f"[range {a.min_pagine:.0f}-{a.max_pagine:.0f}]")
    print(f"Etichette:     " + '  '.join(f"{k}:{v}" for k, v in conteggio.items()))
    print(f"Allegati:      {len(citati)} richiamati")
    print(f"Citazioni:     {len(citate)}"
          + (f"  ({', '.join('n. ' + c for c in sorted(citate))})" if citate else ''))
    print()

    if bloccanti:
        print(f"BLOCCANTI ({len(bloccanti)})")
        for b in bloccanti:
            print(f"  {b}")
        print()
    if avvisi:
        print(f"AVVISI ({len(avvisi)}) — da guardare a mano, non bloccano")
        for v in avvisi:
            print(f"  {v}")
        print()

    if bloccanti:
        print("ESITO: NON DEPOSITABILE. Nessun bloccante si supera con una motivazione: "
              "si corregge l'atto.")
        return 1
    print("ESITO: nessun bloccante. Restano la rubrica, la checklist e il giudizio umano — "
          "questo script e' il pavimento, non il soffitto.")
    return 0


if __name__ == '__main__':
    sys.exit(main())

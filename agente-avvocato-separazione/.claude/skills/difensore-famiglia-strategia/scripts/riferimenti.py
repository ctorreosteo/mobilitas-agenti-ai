#!/usr/bin/env python3
"""
Estrattori dei riferimenti di un atto — modulo condiviso.

Esiste per una ragione sola: l'hook che blocca le citazioni non verificate e lo
script di collaudo devono riconoscere ESATTAMENTE le stesse citazioni. Finche'
la stessa espressione regolare stava copiata in due file, bastava che una delle
due copie invecchiasse perche' una citazione inventata passasse dal cancello
mentre l'altro giurava di controllarla.

## Come si riconosce una citazione, e perche' non basta un'espressione sola

Una citazione italiana ha molte forme, e quella che un modello linguistico
produce piu' spesso e' anche la piu' difficile da riconoscere:

    Cass. civ., sez. I, 12 marzo 2020, n. 9764

fra la parola "Cass." e il numero ci sono una sezione e una data. Un'espressione
che pretenda il numero subito dopo la parola non la vede — e non vederla
significa lasciarla entrare in un atto.

Il riconoscimento avviene quindi in due tempi:

  1. si cerca il NOME DI UN'AUTORITA' o di un TIPO DI PROVVEDIMENTO;
  2. si guarda in una FINESTRA di testo che segue, e vi si cerca il numero,
     con l'anno preso dal numero stesso ("n. 9764/2019") oppure dalla data che
     lo precede ("12 marzo 2020, n. 9764").

## E perche' serve un guardiano dei falsi positivi

Ogni atto contiene numeri che NON sono citazioni e che stanno accanto al nome
di un tribunale: il numero di ruolo generale, i numeri di allegato, i richiami
a leggi e decreti. Segnalarli come sentenze inventate produrrebbe un cancello
che blocca il lavoro legittimo — e un cancello che blocca tutto viene spento,
che e' peggio di non averlo. Da qui l'elenco ESCLUSIONI.
"""

import re
import unicodedata
from pathlib import Path

# ----------------------------------------------------------------------------
# 1. Citazioni giurisprudenziali
# ----------------------------------------------------------------------------

# Le autorita' e i tipi di provvedimento che aprono una citazione.
# Le abbreviazioni portano il punto obbligatorio e le parole intere il confine:
# senza questo, "Tribunale ordinario" contiene "ord" e ogni riga che lo nomina
# diventerebbe l'inizio di una citazione immaginaria.
AUTORITA = (
    r'Cass(?:azione)?\.?|'
    r'S\.?S\.?\s*U\.?U\.?\b|Sezioni\s+Unite\b|'
    r'Corte\s+cost(?:ituzionale)?\.?|Consulta\b|'
    r'Corte\s+(?:d[\'’]?\s*)?[Aa]ppello\b|App\.|'
    r'Trib\.|Tribunal[ei]\b|'
    r'Corte\s+EDU\b|CEDU\b|Corte\s+di\s+giustizia\b|'
    r'Cons(?:iglio)?\.?\s+(?:di\s+)?Stato\b|'
    r'sent\.|sentenz[ae]\b|ord\.|ordinanz[ae]\b|'
    r'decr\.|decret[oi]\b|provv\.|provvediment[oi]\b'
)
RE_AUTORITA = re.compile(r'\b(?:' + AUTORITA + r')', re.IGNORECASE)

# Quanto testo si guarda dopo il nome dell'autorita' prima di rinunciare.
FINESTRA = 90

# Il numero, con l'anno attaccato ("9764/2019", "9764 del 2019") o senza.
RE_NUM_ANNO = re.compile(r'\bn?\.?\s*(\d{1,6})\s*(?:/|\s+del\s+)\s*((?:19|20)\d{2})\b')
RE_NUM_SOLO = re.compile(r'\bn\.\s*(\d{1,6})\b')
RE_ANNO = re.compile(r'\b((?:19|20)\d{2})\b')

# I numeri che stanno accanto a un tribunale e NON sono sentenze.
# Senza questo elenco il numero di ruolo generale di ogni atto verrebbe
# scambiato per una citazione inventata.
ESCLUSIONI = re.compile(
    r'(?:'
    r'R\.?\s*G\.?(?:\s*N\.?\s*R\.?)?|n\.?\s*r\.?\s*g\.?|ruolo\s+generale|'
    r'reg\.?\s*gen\.?|repert(?:orio)?\.?|protocoll|'
    r'all(?:egat[oi])?\.?|doc(?:umento)?\.?|'
    r'L\.|Legge|D\.?\s*Lgs\.?|D\.?\s*L\.?|D\.?P\.?R\.?|D\.?P\.?C\.?M\.?|'
    r'art(?:t)?\.?|comma|co\.|'
    r'proc(?:edimento)?\.?\s*(?:pen|civ)?\.?|R\.?\s*G\.?N\.?R\.?'
    r')\s*[\s\.:n°]*$',
    re.IGNORECASE)


def _norm_key(numero: str, anno: str) -> str:
    return f"{int(numero)}/{anno}"


def citazioni(testo: str) -> set:
    """Le citazioni giurisprudenziali del testo, come chiavi "numero/anno".

    Una citazione senza anno ricavabile entra come "numero/senza-anno": e'
    inverificabile per costruzione, e un riferimento inverificabile in un atto
    e' un problema, non un dettaglio.
    """
    trovate = set()
    for m in RE_AUTORITA.finditer(testo):
        coda = testo[m.end():m.end() + FINESTRA]
        # una riga vuota chiude il periodo: oltre, il numero non appartiene piu'
        # a questa autorita'
        taglio = coda.find('\n\n')
        if taglio != -1:
            coda = coda[:taglio]

        na = RE_NUM_ANNO.search(coda)
        ns = RE_NUM_SOLO.search(coda)
        cand = na if na and (not ns or na.start() <= ns.start()) else ns
        if not cand:
            continue

        # Il numero e' preceduto da qualcosa che lo rende un'altra cosa?
        if ESCLUSIONI.search(coda[:cand.start()] + ' '):
            continue

        numero = cand.group(1)
        if cand is na:
            trovate.add(_norm_key(numero, cand.group(2)))
        else:
            # niente anno attaccato: lo si cerca nella data che precede il numero,
            # dentro la stessa finestra ("12 marzo 2020, n. 9764")
            anni = RE_ANNO.findall(coda[:cand.start()])
            trovate.add(_norm_key(numero, anni[-1]) if anni else f"{int(numero)}/senza-anno")
    return trovate


# ----------------------------------------------------------------------------
# 2. Norme
# ----------------------------------------------------------------------------

RE_ARTICOLO = re.compile(
    r'artt?\.\s*([0-9]+(?:[\-\.][a-zA-Z0-9]+)*)\s*(?:e\s*([0-9]+(?:[\-\.][a-zA-Z0-9]+)*)\s*)?'
    r'(c\.c\.|c\.p\.c\.|c\.p\.p\.|c\.p\.|Cost\.)',
    re.IGNORECASE)

RE_LEGGE = re.compile(
    r'\b(L\.|D\.?Lgs\.?|D\.?L\.?|D\.?P\.?R\.?|D\.?P\.?C\.?M\.?)\s*n?\.?\s*(\d{1,4})\s*/\s*(\d{4})',
    re.IGNORECASE)


def articoli(testo: str) -> set:
    out = set()
    for m in RE_ARTICOLO.finditer(testo):
        codice = m.group(3).lower().replace(' ', '')
        out.add(f"art. {m.group(1)} {codice}")
        if m.group(2):
            out.add(f"art. {m.group(2)} {codice}")
    return out


def norme(testo: str) -> set:
    return {f"{m.group(1).upper().replace('.', '')} {m.group(2)}/{m.group(3)}"
            for m in RE_LEGGE.finditer(testo)}


# ----------------------------------------------------------------------------
# 3. Il registro delle fonti
# ----------------------------------------------------------------------------

LIVELLI = ('CONFERMATA', 'PARZIALE', 'NON TROVATA', 'NON CONFERMATO')


def registro_livelli(percorso) -> dict:
    """Mappa "numero/anno" -> livello di conferma, leggendo il registro.

    Il registro si legge SEZIONE PER SEZIONE, non tagliandolo in due. Chi
    aggiunge fonti scrive in append, e un giorno scrivera' dopo la sezione
    delle fonti non trovate: un parser che si limita a tagliare li' butterebbe
    via, in silenzio, tutte le fonti registrate dopo quel punto — e in silenzio
    e' il modo peggiore.
    """
    f = Path(percorso)
    if not f.exists():
        return None
    testo = f.read_text(encoding='utf-8')

    livelli = {}
    sezione_valida = True
    for riga in testo.splitlines():
        r = riga.strip()
        if r.startswith('#'):
            titolo = r.lstrip('#').strip().lower()
            sezione_valida = 'non trovate' not in titolo and 'non confermate' not in titolo
            continue
        if not sezione_valida:
            for k in citazioni(r):
                livelli.setdefault(k, 'NON TROVATA')
            continue
        trovate = citazioni(r)
        if not trovate:
            continue
        su = r.upper()
        livello = next((l for l in LIVELLI if l in su), 'PARZIALE')
        if livello == 'NON CONFERMATO':
            livello = 'NON TROVATA'
        for k in trovate:
            # non si retrocede una fonte gia' registrata come confermata
            if livelli.get(k) != 'CONFERMATA':
                livelli[k] = livello
    return livelli


def citabili(percorso) -> set:
    """Le sole citazioni che possono entrare in un atto CON IL NUMERO."""
    liv = registro_livelli(percorso)
    if liv is None:
        return None
    return {k for k, v in liv.items() if v == 'CONFERMATA'}


# ----------------------------------------------------------------------------
# 4. Etichette, allegati, date, importi
# ----------------------------------------------------------------------------

ETICHETTE = ('PROVATO', 'DOCUMENTABILE', 'ALLEGABILE', 'NON SOSTENIBILE')
RE_ETICHETTA = re.compile(r'\b(NON SOSTENIBILE|PROVATO|DOCUMENTABILE|ALLEGABILE)\b')
RE_ALLEGATO = re.compile(r'\ball(?:egat[oi])?\.?\s*n?\.?\s*((?:\d+\s*[,e]\s*)*\d+)', re.IGNORECASE)

MESI = ('gennaio febbraio marzo aprile maggio giugno luglio agosto '
        'settembre ottobre novembre dicembre').split()
RE_DATA_NUM = re.compile(r'\b(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})\b')
RE_DATA_TXT = re.compile(r'\b(\d{1,2})\s+(' + '|'.join(MESI) + r')\s+(\d{4})\b', re.IGNORECASE)

RE_IMPORTO = re.compile(r'(?:€|euro)\s*([\d.]+(?:,\d{1,2})?)|([\d.]+(?:,\d{1,2})?)\s*(?:€|euro)',
                        re.IGNORECASE)
RE_PERCENT = re.compile(r'\b(\d{1,3}(?:,\d+)?)\s*%')


def etichette(testo: str) -> dict:
    c = dict.fromkeys(ETICHETTE, 0)
    for m in RE_ETICHETTA.finditer(testo):
        c[m.group(1)] += 1
    return c


def allegati(testo: str) -> set:
    out = set()
    for m in RE_ALLEGATO.finditer(testo):
        for n in re.findall(r'\d+', m.group(1)):
            out.add(int(n))
    return out


def date(testo: str) -> set:
    out = set()
    for m in RE_DATA_NUM.finditer(testo):
        g, ms, a = int(m.group(1)), int(m.group(2)), m.group(3)
        if not (1 <= g <= 31 and 1 <= ms <= 12):
            continue
        a = ('20' + a) if len(a) == 2 else a
        out.add(f"{g:02d}/{ms:02d}/{a}")
    for m in RE_DATA_TXT.finditer(testo):
        ms = MESI.index(m.group(2).lower()) + 1
        out.add(f"{int(m.group(1)):02d}/{ms:02d}/{m.group(3)}")
    return out


def importi(testo: str) -> set:
    out = set()
    for m in RE_IMPORTO.finditer(testo):
        v = m.group(1) or m.group(2)
        if v:
            out.add(v.replace('.', '').replace(',', '.'))
    for m in RE_PERCENT.finditer(testo):
        out.add(m.group(1) + '%')
    return out


# ----------------------------------------------------------------------------
# 5. Difetti che non devono entrare in un atto
# ----------------------------------------------------------------------------

# La PAS non ha ingresso nel processo italiano: invocarla non fa perdere quel
# punto, colloca l'atto — e chi lo firma — dalla parte di chi psicologizza
# invece di documentare.
RE_PAS = re.compile(
    r'\b(?:P\.?A\.?S\.?\b(?!\s*(?:sato|sare))|'
    r'sindrome\s+da?\s+alienazione|alienazione\s+parentale|'
    r'genitore\s+alienante|madre\s+alienante|figlio\s+alienato|'
    r'alienazione\s+genitoriale)',
    re.IGNORECASE)

# L'attacco alla persona invece che alla condotta. E' l'errore piu' costoso in
# questa materia: sposta il giudizio dal comportamento documentato alla persona,
# e il giudice difende la persona.
RE_PERSONA = re.compile(
    r'\b(?:madre|resistente|convenuta|signora|ex|controparte)\b[^.\n]{0,40}\b'
    r'(?:manipolatri|ostruttiv|instabile|inaffidabil|incapace|narcisist|'
    r'anaffettiv|immatur|bugiard|menzogner|vendicativ|malevol|isteric|'
    r'squilibrat|disturbat|egoist|inadeguat|patologic)',
    re.IGNORECASE)

RE_PIEDE = re.compile(r'difensore\s+iscritto\s+all[\'’]\s*albo', re.IGNORECASE)


def normalizza(s: str) -> str:
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('’', "'").replace('‘', "'")
    return re.sub(r'\s+', ' ', s).strip().lower()

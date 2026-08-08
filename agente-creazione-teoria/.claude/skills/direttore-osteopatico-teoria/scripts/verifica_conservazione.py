#!/usr/bin/env python3
"""
Collaudo di conservazione — v5 (asciugata) contro la FINALE (riscritta in chiaro e ripulita nella lingua).

Non giudica la qualita': quella e' gia' stata decisa dai cinque livelli di revisione.
Verifica UNA cosa sola: che la riscrittura integrale del quinto livello e la revisione
di lingua del sesto non abbiano perso, alterato o gonfiato niente. E' il controllo della clausola "L'INVIOLABILE".

Quasi tutti i controlli sono DIFFERENZIALI (v5 contro finale): non richiedono di sapere
come e' formattato il documento, solo che le due versioni dicano le stesse cose.
Questo li rende immuni al fatto che il formato reale delle Bibbie non e' ancora fissato.

Si fa girare UNA VOLTA PER PASSAGGIO, non una volta sola sulla coppia estrema.
Due riscritture misurate in blocco si compensano a vicenda: se la prima perde e la
seconda aggiunge, i conti tornano e la perdita non si vede.

Uso:
    # 1) la riscrittura di chiarezza (v5 -> v6): ogni frase cambia, nessuna identita' attesa
    python3 verifica_conservazione.py v5-intermedia.md v6-chiarezza.md \
        --etichetta "chiarezza" --delta-min -5 --delta-max 10 --json collaudo-chiarezza.json

    # 2) la revisione di lingua (v6 -> v7): deve CORREGGERE, non riscrivere
    python3 verifica_conservazione.py v6-chiarezza.md v7-finale.md \
        --etichetta "lingua" --delta-min -3 --delta-max 5 --min-identita 60 \
        --json collaudo-lingua.json

Opzioni:
    --etichetta NOME    nome del passaggio, per l'intestazione del rapporto
    --delta-min N       variazione di lunghezza minima ammessa, in % (default -5)
    --delta-max N       variazione di lunghezza massima ammessa, in % (default 10)
    --min-identita N    percentuale minima di frasi rimaste IDENTICHE fra i due file.
                        Serve solo per una passata che dichiara di correggere e non
                        riscrivere: sotto quella soglia ha riscritto, e lo dice il
                        conteggio invece dell'agente stesso.
    --json PATH         salva il rapporto

Exit code:
    0 = nessuna violazione bloccante
    1 = almeno una violazione bloccante
    2 = errore d'uso (file mancante)
"""

import sys
import re
import json
from collections import Counter
from pathlib import Path

# ---------------------------------------------------------------- costanti

ETICHETTE = ["DIMOSTRATO", "PROBABILE", "IPOTESI", "RAGIONAMENTO"]
# ordine di forza: alzare un'etichetta e' la violazione piu' grave possibile
FORZA = {"RAGIONAMENTO": 0, "IPOTESI": 1, "PROBABILE": 2, "DIMOSTRATO": 3}

BOX_AMMESSI = ["Definizione", "Quanto è solido", "Attenzione", "Cosa cambia per te"]

PAROLE_MIN, PAROLE_MAX = 8000, 13000
# Default = budget della riscrittura di chiarezza. Ogni passaggio ha il suo, e si passa
# da riga di comando: misurare due riscritture con una sola forbice le lascia compensare.
DELTA_MIN, DELTA_MAX = -5.0, 10.0
GLOSSARIO_MAX = 40
SCRIPT_MAX_PAROLE = 100
TABELLA_MAX_COLONNE = 4
TABELLA_MAX_PAROLE_CELLA = 8

# materiale operativo che in una Bibbia non puo' entrare
OPERATIVO = [
    (r"\b\d+\s*(?:x|per)\s*\d+\b", "ripetizioni o serie"),
    (r"\b\d+\s*(?:minuti|minuto|min\b|secondi|sec\b)", "durata di una tecnica"),
    (r"\b\d+\s*(?:serie|ripetizioni|rip\b)", "dose di esercizio"),
    (r"\b(?:1[ao]|2[ao]|3[ao]|prima|seconda|terza)\s+seduta\b.{0,40}\b(?:si esegue|si fa|esegui|tratta)", "piano di seduta"),
]

# promesse di esito: la compliance le vieta, e una riscrittura puo' reintrodurle
PROMESSE = [
    (r"\bcura\s+(?:l|il|la|lo|gli|le)\b", "«cura» come verbo su una condizione"),
    (r"\brisolve\s+definitivamente\b", "«risolve definitivamente»"),
    (r"\belimina\s+(?:il|la|lo|i|le)\s+(?:sintom|dolor|problem)", "«elimina il sintomo»"),
    (r"\bguarigione\s+(?:garantita|certa|assicurata)\b", "guarigione garantita"),
    (r"\bnel\s+100%\s+dei\s+casi\b", "assoluto sui casi"),
]


# ---------------------------------------------------------------- estrattori

def leggi(p):
    return Path(p).read_text(encoding="utf-8")


def conta_parole(t):
    # esclude le appendici dal conteggio, come prescrive l'architettura
    corpo = re.split(r"^#{1,3}\s*Appendice\s+A\b", t, flags=re.M | re.I)[0]
    return len(re.findall(r"\b[\w'àèéìòùÀÈÉÌÒÙ]+\b", corpo))


def etichette(t):
    """Ogni etichetta di solidita', con le 12 parole che la seguono (l'ancora al claim)."""
    out = []
    for m in re.finditer(
        r">\s*\*\*Quanto\s+è\s+solido[:.]?\*\*\s*[:\-—]?\s*(" + "|".join(ETICHETTE) + r")\b(.{0,120})",
        t, flags=re.I):
        out.append((m.group(1).upper(), " ".join(m.group(2).split())[:120]))
    return out


def pmid_e_link(t):
    ids = set(re.findall(r"\bPMID[:\s]*(\d{6,9})\b", t, flags=re.I))
    ids |= set(re.findall(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d{6,9})", t, flags=re.I))
    return ids


def citazioni(t):
    """Autore + anno: 'Shore, 2016' / 'Shore (2016)' / 'Shore et al. 2016'."""
    pat = r"\b([A-ZÀ-Ý][a-zà-ÿ]{2,})\s*(?:et\s+al\.?)?[,\s]*\(?((?:19|20)\d{2})\)?"
    return set((a, y) for a, y in re.findall(pat, t))


def numeri(t):
    """Percentuali e misure: sono i dati che una riscrittura non puo' toccare."""
    out = Counter()
    for m in re.findall(r"\b\d+(?:[.,]\d+)?\s*%", t):
        out[m.replace(" ", "")] += 1
    for m in re.findall(r"\b\d+(?:[.,]\d+)?\s*(?:mm|cm|mg|ml|Hz|dB|anni|mesi|settimane|giorni)\b", t, flags=re.I):
        out[m.replace(" ", "").lower()] += 1
    return out


def titoli(t):
    return [re.sub(r"\s+", " ", m.group(2)).strip()
            for m in re.finditer(r"^(#{1,4})\s+(.+?)\s*$", t, flags=re.M)]


def marcatori(t):
    return {
        "in_una_riga": len(re.findall(r">\s*\*\*In una riga[:.]?\*\*", t, flags=re.I)),
        "tre_cose": len(re.findall(r"\*\*Le tre cose da ricordare\*\*", t, flags=re.I)),
    }


def blocchi_chiusura(t):
    """Per ogni chiusura di capitolo: (n_bullet, ha_lo_slot_perche_ci_sei_tu).

    Lo standard e' «Le tre cose da ricordare, piu' una»: QUATTRO bullet, e il quarto
    apre con «Perche' ci sei tu». Lo slot e' il pezzo piu' facile da perdere in una
    riscrittura, perche' somiglia a una chiusura retorica ed e' invece l'unico punto
    in cui il documento dichiara il proprio spazio con un dato.
    """
    out = []
    for m in re.finditer(r"\*\*Le tre cose da ricordare[^*]*\*\*(.*?)(?=^#{1,4}\s|\Z)",
                         t, flags=re.S | re.M | re.I):
        blocco = m.group(1)
        bullets = re.findall(r"^\s*[-*+]\s+(.{0,60})", blocco, flags=re.M)
        slot = any(re.match(r"\**\s*Perch[ée]\s+ci\s+sei\s+tu", b, flags=re.I) for b in bullets)
        out.append((len(bullets), slot))
    return out


def tipi_box(t):
    return Counter(re.sub(r"[:.]$", "", m.strip())
                   for m in re.findall(r"^>\s*\*\*([^*]{2,40}?)[:.]?\*\*", t, flags=re.M))


def tabelle(t):
    """(n_colonne, max parole in una cella) per ogni riga di tabella markdown."""
    out = []
    for riga in t.splitlines():
        r = riga.strip()
        if not (r.startswith("|") and r.count("|") >= 2):
            continue
        celle = [c.strip() for c in r.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in celle if c):
            continue  # riga separatrice
        out.append((len(celle), max((len(c.split()) for c in celle), default=0), r[:70]))
    return out


def glossario(t):
    m = re.search(r"^#{1,3}\s*Appendice\s+A\b(.*?)(?=^#{1,3}\s*Appendice\s+B\b|\Z)",
                  t, flags=re.S | re.M | re.I)
    if not m:
        return None
    return len(re.findall(r"^\s*(?:[-*+]\s+|\*\*)\S", m.group(1), flags=re.M))


def frasi(t):
    """Frasi normalizzate. E' l'unita' su cui si misura quanto una passata ha toccato.

    Serve al controllo di IDENTITA': il sesto livello dichiara di correggere frase per
    frase e non di riscrivere, ma quella dichiarazione la fa l'agente su se stesso e
    non vale niente. Qui la stessa cosa la conta il codice.
    """
    corpo = re.sub(r"^\s*[#>|*+-]+\s*", " ", t, flags=re.M)
    pezzi = re.split(r"(?<=[.!?:;])\s+|\n{2,}", corpo)
    out = []
    for p in pezzi:
        s = " ".join(p.split())
        if len(s.split()) >= 5:          # sotto le 5 parole non e' una frase: e' un'etichetta
            out.append(s)
    return out


def identita(a, b):
    """Percentuale di frasi di `a` che ricompaiono IDENTICHE in `b`."""
    fa, fb = Counter(frasi(a)), Counter(frasi(b))
    tot = sum(fa.values())
    if not tot:
        return None
    uguali = sum((fa & fb).values())
    return round(100.0 * uguali / tot, 1)


# Termini canonici del metodo che devono avere una voce a Glossario quando usati.
# Solo quelli non ambigui: "catena" e "compenso" sono parole italiane comuni e
# produrrebbero falsi positivi, e li lascia ai revisori.
LESSICO = ["marker", "disfunzione somatica", "reperto disfunzionale",
           "sistema dominante", "lesione primaria"]
LESSICO_MIN = 2          # sotto due usi non e' ancora un termine portante


def lessico_senza_glossario(t):
    """Termini del metodo usati nel corpo e assenti dal Glossario.

    E' il difetto che questo controllo nasce per intercettare: «marker» comparso
    sedici volte in una Bibbia, mai definito e mai a Glossario — mentre reggeva
    tre regole del metodo. Un termine che regge una regola e non e' definito
    rende inapplicabile la regola.
    """
    corpo = re.split(r"^#{1,3}\s*Appendice\s+A\b", t, flags=re.M | re.I)[0]
    m = re.search(r"^#{1,3}\s*Appendice\s+A\b(.*?)(?=^#{1,3}\s*Appendice\s+B\b|\Z)",
                  t, flags=re.S | re.M | re.I)
    gloss = m.group(1) if m else ""
    fuori = []
    for x in LESSICO:
        usi = len(re.findall(re.escape(x), corpo, flags=re.I))
        if usi >= LESSICO_MIN and not re.search(re.escape(x), gloss, flags=re.I):
            fuori.append(f"{x} ({usi} usi)")
    return fuori


def triage(t):
    """Gli elementi del cancello a tre uscite che una riscrittura tende a fondere.

    E' la sezione piu' lunga e piu' strutturata del documento, quindi la piu' esposta
    a essere compattata: due uscite che diventano una, le quattro condizioni del GIALLO
    che diventano tre, i tempi delle bandiere rosse assorbiti nella prosa.
    """
    return {
        "uscite": len(re.findall(r"\b(ROSSO|GIALLO|VERDE)\b", t)),
        "tempi": len(re.findall(r"\b(112|Urgente|Invio,?\s+non\s+attendere|Invio\s+programmato|Invio)\b", t, flags=re.I)),
    }


def righe_per_te(t):
    """Le righe «Per te:» che chiudono un dato numerico.

    Sono il pezzo piu' fragile del documento: hanno l'aria di un commento, e la
    riscrittura tende ad accorparle nella frase precedente o a toglierle. Ma sono
    il motivo per cui quel numero e' nel documento — senza, il numero e' decorazione.
    """
    return len(re.findall(r"\*\*Per te[:.]?\*\*", t, flags=re.I))


def script_paziente(t):
    """Lo script del capitolo 13: il blocco in corsivo sotto l'intestazione «Lo script».

    La misura e' ancorata alla sezione, non all'intero documento: una coppia
    virgoletta+asterisco distante inghiottiva mezza Bibbia e faceva sembrare lo
    script lungo migliaia di parole. Fuori dalla sezione, e come rete di sicurezza,
    i gruppi catturati non possono attraversare un a capo.
    """
    sez = re.search(r"^#{1,4}\s*Lo\s+script\b[^\n]*\n(.*?)(?=^#{1,4}\s|\Z)",
                    t, flags=re.S | re.M | re.I)
    testo = sez.group(1) if sez else t

    cand = (re.findall(r'\*\s*"([^"\n]{40,})"\s*\*', testo)
            + re.findall(r'"\s*\*([^*\n]{40,})\*\s*"', testo)
            + re.findall(r"\*_([^_\n]{40,})_\*", testo))
    if not cand:
        cand = re.findall(r"^\s*>?\s*\*([^*\n]{200,})\*\s*$", testo, flags=re.M)
    if not cand:
        return None
    return max(len(c.split()) for c in cand)


# ---------------------------------------------------------------- controlli

class Rapporto:
    def __init__(self):
        self.voci = []

    def add(self, grave, codice, msg, dettaglio=None):
        self.voci.append({
            "severita": "BLOCCANTE" if grave else "AVVISO",
            "codice": codice,
            "messaggio": msg,
            "dettaglio": dettaglio or [],
        })

    @property
    def bloccanti(self):
        return [v for v in self.voci if v["severita"] == "BLOCCANTE"]


def verifica(v5, v6, delta_min=DELTA_MIN, delta_max=DELTA_MAX, min_identita=None):
    r = Rapporto()

    # --- 1. ETICHETTE DI SOLIDITA' — il controllo piu' importante di tutti ---
    e5, e6 = etichette(v5), etichette(v6)
    c5, c6 = Counter(x[0] for x in e5), Counter(x[0] for x in e6)

    if len(e6) < len(e5):
        r.add(True, "ETICHETTE_PERSE",
              f"La v6 ha {len(e5) - len(e6)} etichette di solidità in meno della v5 "
              f"({len(e5)} → {len(e6)}). Ogni etichetta persa è un'affermazione ora presentata come certa.")

    for et in ETICHETTE:
        if c6[et] > c5[et]:
            piu_forte = [x for x in ETICHETTE if FORZA[x] < FORZA[et]]
            calate = [x for x in piu_forte if c6[x] < c5[x]]
            if calate:
                r.add(True, "ETICHETTA_ALZATA",
                      f"{et} è passata da {c5[et]} a {c6[et]} mentre {', '.join(calate)} è calata: "
                      f"un'affermazione è stata promossa a un grado di certezza superiore.")

    # ancoraggio: l'etichetta è ancora attaccata allo stesso claim?
    ctx5 = {(l, c[:60]) for l, c in e5}
    ctx6 = {(l, c[:60]) for l, c in e6}
    orfane = sorted(ctx5 - ctx6)[:8]
    if orfane and len(e5) == len(e6):
        r.add(False, "ETICHETTE_RIANCORATE",
              f"{len(ctx5 - ctx6)} etichette seguono un testo diverso dalla v5. "
              "Può essere solo riformulazione — va guardato dal collaudatore semantico.",
              [f"{l}: …{c}" for l, c in orfane])

    # --- 2. FONTI ---
    p5, p6 = pmid_e_link(v5), pmid_e_link(v6)
    if p5 - p6:
        r.add(True, "PMID_PERSI", f"{len(p5 - p6)} riferimenti PubMed spariti nella riscrittura.",
              sorted(p5 - p6))
    if p6 - p5:
        r.add(True, "PMID_INVENTATI", f"{len(p6 - p5)} riferimenti PubMed compaiono solo nella v6.",
              sorted(p6 - p5))

    q5, q6 = citazioni(v5), citazioni(v6)
    perse = sorted(q5 - q6)[:10]
    if perse:
        r.add(False, "CITAZIONI_PERSE", f"{len(q5 - q6)} coppie autore-anno non ricompaiono nella v6.",
              [f"{a} {y}" for a, y in perse])

    # --- 3. NUMERI ---
    n5, n6 = numeri(v5), numeri(v6)
    mancanti = {k: v for k, v in (n5 - n6).items()}
    if mancanti:
        r.add(True, "NUMERI_PERSI",
              f"{len(mancanti)} valori numerici della v5 non si ritrovano nella v6.",
              [f"{k} (×{v})" for k, v in list(mancanti.items())[:12]])
    nuovi = {k: v for k, v in (n6 - n5).items()}
    if nuovi:
        r.add(True, "NUMERI_INVENTATI",
              f"{len(nuovi)} valori numerici compaiono solo nella v6.",
              [f"{k} (×{v})" for k, v in list(nuovi.items())[:12]])

    # --- 4. ARCHITETTURA ---
    t5, t6 = titoli(v5), titoli(v6)
    if len(t6) != len(t5):
        r.add(True, "TITOLI_DIVERSI",
              f"La v5 ha {len(t5)} titoli, la v6 ne ha {len(t6)}: la riscrittura ha cambiato la struttura.")
    else:
        cambiati = [(a, b) for a, b in zip(t5, t6) if a != b]
        if cambiati:
            r.add(False, "TITOLI_RIFORMULATI",
                  f"{len(cambiati)} titoli sono stati riformulati (ammesso solo se il senso è identico).",
                  [f"«{a}» → «{b}»" for a, b in cambiati[:8]])

    m5, m6 = marcatori(v5), marcatori(v6)
    for k, nome in [("in_una_riga", "aperture «In una riga»"), ("tre_cose", "chiusure «Le tre cose da ricordare»")]:
        if m6[k] < m5[k]:
            r.add(True, "APERTURE_CHIUSURE_PERSE",
                  f"{nome}: da {m5[k]} a {m6[k]}. L'architettura le impone in ogni capitolo.")

    ch5, ch6 = blocchi_chiusura(v5), blocchi_chiusura(v6)
    sbagliati = [n for n, _ in ch6 if n != 4]
    if sbagliati:
        r.add(True, "CHIUSURA_NON_TRE_PIU_UNA",
              f"{len(sbagliati)} chiusure non hanno esattamente quattro bullet: {sbagliati}. "
              f"Lo standard e' «Le tre cose da ricordare, piu' una»: tre cose piu' lo slot «Perche' ci sei tu».")

    slot5 = sum(1 for _, s in ch5 if s)
    slot6 = sum(1 for _, s in ch6 if s)
    senza = sum(1 for _, s in ch6 if not s)
    if senza:
        r.add(True, "SLOT_PERCHE_CI_SEI_TU_ASSENTE",
              f"{senza} chiusure su {len(ch6)} non hanno lo slot «Perche' ci sei tu» come ultimo bullet.")
    if slot6 < slot5:
        r.add(True, "SLOT_PERCHE_CI_SEI_TU_PERSO",
              f"{slot5 - slot6} slot «Perche' ci sei tu» sono spariti nella riscrittura ({slot5} → {slot6}). "
              f"E' l'unico punto in cui il documento dichiara il proprio spazio con un dato: non si accorpa.")

    b6 = tipi_box(v6)
    intrusi = {k: v for k, v in b6.items()
               if not any(k.lower().startswith(a.lower()[:10]) for a in BOX_AMMESSI)
               and not k.lower().startswith("in una riga")}
    if intrusi:
        r.add(False, "BOX_NON_PREVISTI",
              f"{len(intrusi)} tipi di box fuori dai quattro ammessi.",
              [f"«{k}» (×{v})" for k, v in list(intrusi.items())[:8]])

    # --- 5. TABELLE ---
    fuori = [(c, p, s) for c, p, s in tabelle(v6)
             if c > TABELLA_MAX_COLONNE or p > TABELLA_MAX_PAROLE_CELLA]
    if fuori:
        r.add(True, "TABELLE_FUORI_SPECIFICA",
              f"{len(fuori)} righe di tabella superano {TABELLA_MAX_COLONNE} colonne "
              f"o {TABELLA_MAX_PAROLE_CELLA} parole per cella.",
              [f"{c} col / {p} parole: {s}" for c, p, s in fuori[:8]])

    # --- 6. LUNGHEZZA ---
    w5, w6 = conta_parole(v5), conta_parole(v6)
    delta = ((w6 - w5) / w5 * 100) if w5 else 0.0
    if not (delta_min <= delta <= delta_max):
        r.add(True, "DELTA_FUORI_RANGE",
              f"La versione dopo varia del {delta:+.1f}% rispetto a quella prima ({w5} → {w6} parole). "
              f"Ammesso solo fra {delta_min:+.0f}% e {delta_max:+.0f}%: "
              f"{'sotto significa informazione tagliata' if delta < 0 else 'sopra significa contenuto aggiunto'}.")
    # AVVISO, non bloccante: la lunghezza NON e' una questione di conservazione.
    # Questo script verifica che fra due versioni non si sia perso niente. Se il documento
    # sia lungo 12.000 o 17.000 parole e' un giudizio di qualita', e vive nella checklist
    # e nella rubrica, dove e' gia' presente. Tenerlo qui come bloccante produceva l'assurdo
    # osservato al primo giro reale: un documento conservato perfettamente veniva dichiarato
    # NON CONSEGNABILE per un difetto ereditato dalla versione in ingresso, che nessuna
    # riparazione chirurgica puo' correggere — e i due giri di riparazione si bruciavano
    # senza toccare i difetti veri.
    if not (PAROLE_MIN <= w6 <= PAROLE_MAX):
        r.add(False, "PAROLE_FUORI_RANGE",
              f"Il documento ha {w6} parole (appendici escluse): fuori dal range {PAROLE_MIN}–{PAROLE_MAX}. "
              f"Non e' un difetto di conservazione: se il superamento c'era gia' in ingresso, "
              f"il rilievo appartiene al livello di asciugatura, non a chi ha riscritto.")

    # --- 6-bis. IDENTITA' — ha corretto o ha riscritto? ---
    # Si applica solo a una passata che dichiara di correggere frase per frase.
    # E' il controllo che sostituisce l'autodichiarazione dell'agente su se stesso.
    ident = identita(v5, v6)
    if min_identita is not None and ident is not None and ident < min_identita:
        r.add(True, "HA_RISCRITTO_INVECE_DI_CORREGGERE",
              f"Solo il {ident}% delle frasi e' rimasto identico (soglia {min_identita}%). "
              f"Questa passata doveva correggere i difetti, non riscrivere il documento: "
              f"una seconda riscrittura integrale raddoppia la deriva che il collaudo esiste per fermare.")

    # --- 6-ter. LE RIGHE «PER TE» ---
    pt5, pt6 = righe_per_te(v5), righe_per_te(v6)
    if pt6 < pt5:
        r.add(True, "PER_TE_PERSE",
              f"{pt5 - pt6} righe «Per te» sono sparite ({pt5} → {pt6}). "
              f"Sono la conseguenza operativa di un dato numerico: senza, quel numero "
              f"e' decorazione e andrebbe cancellato, non lasciato nudo.")

    # --- 6-quater. IL CANCELLO A TRE USCITE ---
    tg5, tg6 = triage(v5), triage(v6)
    if tg6["uscite"] < tg5["uscite"]:
        r.add(True, "TRIAGE_COMPATTATO",
              f"I marcatori delle tre uscite del cancello calano da {tg5['uscite']} a {tg6['uscite']}. "
              f"ROSSO, GIALLO e VERDE non si fondono: in ciascuna il comportamento e' diverso.")
    if tg6["tempi"] < tg5["tempi"]:
        r.add(True, "TEMPI_INVIO_PERSI",
              f"{tg5['tempi'] - tg6['tempi']} indicazioni di tempo per le bandiere rosse sono sparite "
              f"({tg5['tempi']} → {tg6['tempi']}). Un'urgenza assorbita nella prosa non si esegue.")

    # --- 6-quinquies. IL LESSICO DEL METODO ---
    nudi = lessico_senza_glossario(v6)
    if nudi:
        r.add(True, "LESSICO_DEL_METODO_NUDO",
              f"{len(nudi)} termini canonici del metodo sono usati nel testo e non hanno "
              f"una voce a Glossario. Vanno definiti col testo fisso di lessico-del-metodo.md.",
              nudi)

    # --- 7. GLOSSARIO E SCRIPT ---
    g6 = glossario(v6)
    if g6 is None:
        r.add(True, "GLOSSARIO_ASSENTE", "Appendice A (Glossario) non trovata nella v6.")
    elif g6 > GLOSSARIO_MAX:
        r.add(False, "GLOSSARIO_TROPPO_LUNGO",
              f"Il glossario ha {g6} termini (max {GLOSSARIO_MAX}): la Bibbia è scritta troppo tecnica.")

    s6 = script_paziente(v6)
    if s6 and s6 > SCRIPT_MAX_PAROLE:
        r.add(True, "SCRIPT_TROPPO_LUNGO",
              f"Lo script per il paziente ha {s6} parole (max {SCRIPT_MAX_PAROLE}).")

    # --- 8. CONFINE E COMPLIANCE — cose che una riscrittura puo' reintrodurre ---
    for pat, nome in OPERATIVO:
        hit = re.findall(pat, v6, flags=re.I)
        nuovi_hit = len(hit) - len(re.findall(pat, v5, flags=re.I))
        if hit and nuovi_hit > 0:
            r.add(True, "MATERIALE_OPERATIVO",
                  f"La v6 introduce {nuovi_hit} occorrenze di {nome}: è materia di Procedura, non di Bibbia.",
                  [str(h) for h in hit[:5]])

    for pat, nome in PROMESSE:
        if re.search(pat, v6, flags=re.I) and not re.search(pat, v5, flags=re.I):
            r.add(True, "PROMESSA_INTRODOTTA",
                  f"La v6 introduce una promessa di esito che la v5 non aveva: {nome}.")

    return r, {"parole_prima": w5, "parole_dopo": w6, "delta_pct": round(delta, 1),
               "identita_pct": ident, "per_te_prima": pt5, "per_te_dopo": pt6,
               "slot_prima": slot5, "slot_dopo": slot6,
               "uscite_prima": tg5["uscite"], "uscite_dopo": tg6["uscite"],
               "etichette_prima": len(e5), "etichette_dopo": len(e6),
               "pmid_prima": len(p5), "pmid_dopo": len(p6)}


# ---------------------------------------------------------------- main

def opzione(nome, default=None, numerica=True):
    """Legge --nome VALORE da riga di comando."""
    if nome not in sys.argv:
        return default
    i = sys.argv.index(nome)
    if i + 1 >= len(sys.argv):
        return default
    val = sys.argv[i + 1]
    if not numerica:
        return val
    try:
        return float(val)
    except ValueError:
        return default


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    # i valori delle opzioni non sono file: vanno tolti dai posizionali
    valori = set()
    for nome in ("--json", "--etichetta", "--delta-min", "--delta-max", "--min-identita"):
        if nome in sys.argv:
            i = sys.argv.index(nome)
            if i + 1 < len(sys.argv):
                valori.add(sys.argv[i + 1])
    args = [a for a in args if a not in valori]

    if len(args) < 2:
        print(__doc__)
        return 2
    for p in args[:2]:
        if not Path(p).is_file():
            print(f"ERRORE: file non trovato: {p}")
            return 2

    etichetta = opzione("--etichetta", "passaggio", numerica=False)
    dmin = opzione("--delta-min", DELTA_MIN)
    dmax = opzione("--delta-max", DELTA_MAX)
    ident_min = opzione("--min-identita", None)

    v5, v6 = leggi(args[0]), leggi(args[1])
    rap, stat = verifica(v5, v6, dmin, dmax, ident_min)

    print("=" * 72)
    print(f"COLLAUDO DI CONSERVAZIONE — passaggio «{etichetta}»")
    print(f"  {Path(args[0]).name}  →  {Path(args[1]).name}")
    print("=" * 72)
    print(f"parole    {stat['parole_prima']} → {stat['parole_dopo']}  ({stat['delta_pct']:+.1f}%)"
          f"   [ammesso {dmin:+.0f}% … {dmax:+.0f}%]")
    print(f"etichette {stat['etichette_prima']} → {stat['etichette_dopo']}     "
          f"PMID {stat['pmid_prima']} → {stat['pmid_dopo']}     "
          f"«Per te» {stat['per_te_prima']} → {stat['per_te_dopo']}     "
          f"«Perché ci sei tu» {stat['slot_prima']} → {stat['slot_dopo']}")
    if stat["identita_pct"] is not None:
        soglia = f"   [minimo {ident_min:.0f}%]" if ident_min is not None else "   (nessuna soglia: riscrittura attesa)"
        print(f"frasi identiche {stat['identita_pct']}%{soglia}")
    print("-" * 72)

    if not rap.voci:
        print(f"NESSUNA VIOLAZIONE. Il passaggio «{etichetta}» ha conservato tutto.")
    for v in sorted(rap.voci, key=lambda x: x["severita"] != "BLOCCANTE"):
        print(f"\n[{v['severita']}] {v['codice']}\n  {v['messaggio']}")
        for d in v["dettaglio"]:
            print(f"    · {d}")

    print("\n" + "=" * 72)
    esito = "NON CONSEGNABILE" if rap.bloccanti else "CONSEGNABILE"
    print(f"ESITO: {esito}  —  {len(rap.bloccanti)} bloccanti, "
          f"{len(rap.voci) - len(rap.bloccanti)} avvisi")
    print("=" * 72)

    if "--json" in sys.argv:
        i = sys.argv.index("--json")
        if i + 1 < len(sys.argv):
            Path(sys.argv[i + 1]).write_text(
                json.dumps({"passaggio": etichetta, "esito": esito,
                            "statistiche": stat, "violazioni": rap.voci},
                           ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if rap.bloccanti else 0


if __name__ == "__main__":
    sys.exit(main())

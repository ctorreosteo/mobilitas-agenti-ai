#!/usr/bin/env python3
"""
Collaudo di conservazione — v5 (asciugata) contro v6 (riscritta in chiaro).

Non giudica la qualita': quella e' gia' stata decisa dai cinque livelli di revisione.
Verifica UNA cosa sola: che la riscrittura integrale del quinto livello non abbia
perso, alterato o gonfiato niente. E' il controllo della clausola "L'INVIOLABILE".

Quasi tutti i controlli sono DIFFERENZIALI (v5 contro v6): non richiedono di sapere
come e' formattato il documento, solo che le due versioni dicano le stesse cose.
Questo li rende immuni al fatto che il formato reale delle Bibbie non e' ancora fissato.

Uso:
    python3 verifica_conservazione.py <v5.md> <v6.md> [--json rapporto.json]

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

PAROLE_MIN, PAROLE_MAX = 8000, 12000
DELTA_MIN, DELTA_MAX = -5.0, 10.0          # la riscrittura puo' variare solo qui dentro
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


def blocchi_tre_cose(t):
    """Per ogni chiusura, quanti bullet la seguono. Devono essere esattamente tre."""
    out = []
    for m in re.finditer(r"\*\*Le tre cose da ricordare\*\*(.*?)(?=^#{1,4}\s|\Z)",
                         t, flags=re.S | re.M | re.I):
        out.append(len(re.findall(r"^\s*[-*+]\s+\S", m.group(1), flags=re.M)))
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


def script_paziente(t):
    """Lo script del capitolo 12: il blocco in corsivo piu' lungo del documento."""
    cand = re.findall(r'"\s*\*(.+?)\*\s*"', t, flags=re.S) + re.findall(r"\*_(.+?)_\*", t, flags=re.S)
    if not cand:
        cand = re.findall(r"^\s*>?\s*\*([^*\n]{200,})\*\s*$", t, flags=re.M)
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


def verifica(v5, v6):
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

    sbagliati = [n for n in blocchi_tre_cose(v6) if n != 3]
    if sbagliati:
        r.add(True, "TRE_COSE_NON_TRE",
              f"{len(sbagliati)} chiusure non hanno esattamente tre bullet: {sbagliati}.")

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
    if not (DELTA_MIN <= delta <= DELTA_MAX):
        r.add(True, "DELTA_FUORI_RANGE",
              f"La v6 varia del {delta:+.1f}% rispetto alla v5 ({w5} → {w6} parole). "
              f"Ammesso solo fra {DELTA_MIN:+.0f}% e {DELTA_MAX:+.0f}%: "
              f"{'sotto significa informazione tagliata' if delta < 0 else 'sopra significa contenuto aggiunto'}.")
    if not (PAROLE_MIN <= w6 <= PAROLE_MAX):
        r.add(True, "PAROLE_FUORI_RANGE",
              f"La v6 ha {w6} parole (appendici escluse): fuori dal range {PAROLE_MIN}–{PAROLE_MAX}.")

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

    return r, {"parole_v5": w5, "parole_v6": w6, "delta_pct": round(delta, 1),
               "etichette_v5": len(e5), "etichette_v6": len(e6),
               "pmid_v5": len(p5), "pmid_v6": len(p6)}


# ---------------------------------------------------------------- main

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    for p in args[:2]:
        if not Path(p).is_file():
            print(f"ERRORE: file non trovato: {p}")
            return 2

    v5, v6 = leggi(args[0]), leggi(args[1])
    rap, stat = verifica(v5, v6)

    print("=" * 72)
    print("COLLAUDO DI CONSERVAZIONE — v5 (asciugata) contro v6 (riscritta)")
    print("=" * 72)
    print(f"parole   {stat['parole_v5']} → {stat['parole_v6']}  ({stat['delta_pct']:+.1f}%)")
    print(f"etichette {stat['etichette_v5']} → {stat['etichette_v6']}     "
          f"PMID {stat['pmid_v5']} → {stat['pmid_v6']}")
    print("-" * 72)

    if not rap.voci:
        print("NESSUNA VIOLAZIONE. La riscrittura ha conservato tutto.")
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
                json.dumps({"esito": esito, "statistiche": stat, "violazioni": rap.voci},
                           ensure_ascii=False, indent=2), encoding="utf-8")

    return 1 if rap.bloccanti else 0


if __name__ == "__main__":
    sys.exit(main())

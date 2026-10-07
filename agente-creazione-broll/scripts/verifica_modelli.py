#!/usr/bin/env python3
"""Controlla il catalogo dei modelli contro la documentazione viva di Higgsfield.

Perche' esiste: il catalogo e' una fotografia, e i modelli su Higgsfield cambiano ogni
poche settimane. Senza questo script l'unico modo di scoprire che un endpoint non esiste
piu' e' un 404 a meta' di una generazione gia' pagata a meta'.

Cosa fa, e cosa NON fa:
  - per ogni modello del catalogo con un endpoint, apre la sua pagina di documentazione
    e verifica che l'endpoint dichiarato sia ancora scritto li' dentro;
  - elenca i modelli presenti nel catalogo Higgsfield ma assenti dal nostro file: sono
    le occasioni (o il nuovo predefinito) che stiamo perdendo;
  - dice se il file ha superato la sua scadenza.

Non aggiorna niente da solo. La documentazione avverte che il catalogo autorevole sta in
console (dietro account) e che l'assenza di un modello dallo spec pubblico NON prova che
il modello non esista. Quindi qui si REFERTA, e la decisione resta umana.

Uso:  verifica_modelli.py [--catalogo ../broll-generati/_dati/modelli-higgsfield.json]
"""

import argparse
import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path

DOCS = "https://docs.higgsfield.ai/docs"
INDICI = {"immagine": f"{DOCS}/models/image-generation.md", "video": f"{DOCS}/models/video-generation.md"}


def pagina(url):
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            return r.read().decode(errors="replace")
    except Exception as e:
        return f"__ERRORE__ {type(e).__name__}: {e}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalogo", default=str(Path(__file__).resolve().parent.parent
                                             / "broll-generati/_dati/modelli-higgsfield.json"))
    a = p.parse_args()
    cat = json.loads(Path(a.catalogo).read_text())

    print(f"Catalogo: {a.catalogo}")
    aggiornato = dt.date.fromisoformat(cat["aggiornato_il"])
    eta = (dt.date.today() - aggiornato).days
    scadenza = int(cat.get("scadenza_giorni", 30))
    stato_eta = "SCADUTO" if eta > scadenza else "valido"
    print(f"Aggiornato il {aggiornato} — {eta} giorni fa ({stato_eta}, scadenza {scadenza} giorni)\n")

    problemi, note = [], []
    print("— Endpoint dichiarati —")
    for chiave, m in cat["modelli"].items():
        if not m.get("endpoint"):
            print(f"  ·  {chiave:<22} nessun endpoint (disponibile_su_api={m.get('disponibile_su_api')})")
            if m.get("disponibile_su_api"):
                problemi.append(f"{chiave}: dichiarato disponibile ma senza endpoint")
            continue
        testo = pagina(m["doc"]) if m.get("doc", "").startswith("http") else "__ERRORE__ doc non indicata"
        if testo.startswith("__ERRORE__"):
            print(f"  ?  {chiave:<22} doc non raggiungibile — {testo[12:80]}")
            note.append(f"{chiave}: documentazione non raggiungibile, verifica a mano")
        elif m["endpoint"] in testo:
            print(f"  ok {chiave:<22} {m['endpoint']}")
        else:
            print(f"  !! {chiave:<22} {m['endpoint']} NON compare piu' nella sua pagina")
            problemi.append(f"{chiave}: endpoint '{m['endpoint']}' assente dalla doc {m['doc']}")

    print("\n— Catalogo Higgsfield: cosa c'e' che noi non abbiamo —")
    conosciute = set()
    for m in cat["modelli"].values():
        if m.get("famiglia"):
            conosciute.add(m["famiglia"])
        d = m.get("doc", "")
        if "/docs/models/" in d:
            conosciute.add(re.search(r"/docs/models/([a-z0-9-]+)", d).group(1))
    for tipo, url in INDICI.items():
        testo = pagina(url)
        if testo.startswith("__ERRORE__"):
            note.append(f"indice {tipo} non raggiungibile")
            continue
        famiglie = sorted(set(re.findall(r'/docs/models/([a-z0-9-]+)(?:["/])', testo)))
        nuove = [f for f in famiglie if f not in conosciute and f not in ("image-generation", "video-generation")]
        print(f"  {tipo}: {len(famiglie)} famiglie documentate; non nel nostro catalogo -> {', '.join(nuove) or 'nessuna'}")

    print("\n— Referto —")
    if eta > scadenza:
        print(f"  · il catalogo ha {eta} giorni: va riletto e ridatato prima del prossimo lancio")
    for x in problemi:
        print(f"  !! {x}")
    for x in note:
        print(f"  ?  {x}")
    if not problemi and eta <= scadenza:
        print("  Nessun problema bloccante: gli endpoint dichiarati esistono ancora.")
    print("\n  Il catalogo autorevole sta in console.higgsfield.ai, dietro account. L'assenza di un")
    print("  modello dalla doc pubblica non prova che non esista: verifica li' prima di cancellarlo.")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())

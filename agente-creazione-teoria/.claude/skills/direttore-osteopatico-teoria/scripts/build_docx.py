#!/usr/bin/env python3
"""
Converte una Bibbia teorica Mobilitas (o la sua Mappa concettuale) da markdown a .docx.

Uso:
    python build_docx.py v7-finale.md "Reflusso Gastroesofageo" --slug reflusso
    python build_docx.py mappa-finale.md "Reflusso Gastroesofageo" --slug reflusso
    python build_docx.py v7-finale.md "Reflusso" -o /percorso/esplicito/Bibbia_Reflusso.docx

Senza -o il file finisce in <repo>/outputs/<slug>/, una sottocartella per condizione.
Lo slug si deduce dal titolo; passa --slug per allinearlo a bibbie-generate/<slug>/.

Il tipo di documento si deduce dal nome del file sorgente: se contiene "mappa" viene
trattato come Mappa concettuale (una pagina, niente indice), altrimenti come Bibbia.

Dopo la conversione verifica sempre il risultato:
    soffice --headless --convert-to pdf output.docx
    pdftoppm -jpeg -r 100 output.pdf page && ls page-*.jpg
e poi GUARDA le immagini. Tabelle spezzate e heading persi si vedono solo così.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# Range di una Bibbia teorica, appendici escluse (vedi architettura-bibbia.md).
MIN_PAROLE = 8000
MAX_PAROLE = 13000


def word_count(md_path: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    text = re.sub(r"[#*_>|`\-]", " ", text)
    return len(text.split())


def is_mappa(md_path: Path) -> bool:
    return "mappa" in md_path.name.lower()


def build(md_path: Path, titolo: str, out_path: Path) -> None:
    if not md_path.exists():
        sys.exit(f"File non trovato: {md_path}")

    out_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "pandoc",
        str(md_path),
        "-o", str(out_path),
        "--from", "markdown+pipe_tables+raw_html",
        "--metadata", "author=Mobilitas — Direzione Osteopatica",
        "--metadata", "lang=it-IT",
    ]

    # La Mappa concettuale è una pagina: niente TOC, niente titolo di copertina.
    if not is_mappa(md_path):
        cmd += ["--toc", "--toc-depth=2",
                "--metadata", f"title=Bibbia Teorica — {titolo}"]

    ref = Path(__file__).parent / "reference.docx"
    if ref.exists():
        cmd += ["--reference-doc", str(ref)]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"pandoc ha fallito:\n{result.stderr}")

    wc = word_count(md_path)
    print(f"OK  -> {out_path}")
    print(f"Parole: {wc}")
    if not is_mappa(md_path):
        if wc < MIN_PAROLE:
            print(f"ATTENZIONE: sotto le {MIN_PAROLE:,} parole. E' un riassunto, non una Bibbia.")
        elif wc > MAX_PAROLE + 1000:
            print(f"ATTENZIONE: oltre le {MAX_PAROLE:,} parole. Nessuno la finisce.")
    elif wc > 700:
        print("ATTENZIONE: la Mappa concettuale deve stare in una pagina.")
    print("Ora renderizza il .docx in immagini e GUARDALE prima di consegnare.")


# <repo>/.claude/skills/direttore-osteopatico-teoria/scripts/build_docx.py -> <repo>
REPO = Path(__file__).resolve().parents[4]
OUTPUTS = REPO / "outputs"


def slugify(titolo: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", titolo.lower()).strip("-")


def main() -> None:
    p = argparse.ArgumentParser(description="Build Bibbia teorica Mobilitas -> docx")
    p.add_argument("markdown", type=Path, help="File markdown sorgente")
    p.add_argument("titolo", help="Nome della condizione, es. 'Reflusso Gastroesofageo'")
    p.add_argument("-o", "--output", type=Path, default=None, help="Path di output .docx")
    p.add_argument("--slug", default=None,
                   help="Sottocartella sotto outputs/ (default: dedotto dal titolo). "
                        "Usa lo stesso slug di bibbie-generate/<slug>/ per tenerli allineati.")
    args = p.parse_args()

    out = args.output
    if out is None:
        # Bibbia e Mappa convivono nella stessa cartella: il nome del file deve
        # distinguerle, altrimenti la seconda conversione sovrascrive la prima.
        nome = re.sub(r"[^A-Za-z0-9]+", "_", args.titolo).strip("_")
        prefisso = "Mappa" if is_mappa(args.markdown) else "Bibbia"
        out = OUTPUTS / (args.slug or slugify(args.titolo)) / f"{prefisso}_{nome}.docx"

    build(args.markdown, args.titolo, out)


if __name__ == "__main__":
    main()

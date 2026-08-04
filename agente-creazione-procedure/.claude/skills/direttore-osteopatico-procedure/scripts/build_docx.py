#!/usr/bin/env python3
"""
Converte una procedura clinica Mobilitas da markdown a .docx.

Uso:
    python build_docx.py procedura-reflusso.md "Reflusso Gastroesofageo"
    python build_docx.py scheda-reflusso.md "Reflusso Gastroesofageo" --slug reflusso-gastrico
    python build_docx.py procedura-reflusso.md "Reflusso" -o /percorso/esplicito/Procedura_Reflusso.docx

Senza -o il file finisce in <repo>/outputs/<slug>/, una sottocartella per condizione.
Lo slug si deduce dal titolo; passa --slug per allinearlo a procedure-generate/<slug>/.

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


def word_count(md_path: Path) -> int:
    text = md_path.read_text(encoding="utf-8")
    text = re.sub(r"[#*_>|`\-]", " ", text)
    return len(text.split())


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

    # La Scheda Operativa è una pagina: niente TOC, niente titolo di copertina.
    is_scheda = "scheda" in md_path.name.lower()
    if not is_scheda:
        cmd += ["--toc", "--toc-depth=2",
                "--metadata", f"title=Procedura Clinica — {titolo}"]

    ref = Path(__file__).parent / "reference.docx"
    if ref.exists():
        cmd += ["--reference-doc", str(ref)]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"pandoc ha fallito:\n{result.stderr}")

    wc = word_count(md_path)
    print(f"OK  -> {out_path}")
    print(f"Parole: {wc}")
    if wc < 4500:
        print("ATTENZIONE: sotto le 4.500 parole. E' una dispensa, non una procedura.")
    elif wc > 8000:
        print("ATTENZIONE: sopra le 8.000 parole. Nessuno la legge fino in fondo.")
    print("Ora renderizza il .docx in immagini e GUARDALE prima di consegnare.")


# <repo>/.claude/skills/direttore-osteopatico-procedure/scripts/build_docx.py -> <repo>
REPO = Path(__file__).resolve().parents[4]
OUTPUTS = REPO / "outputs"


def slugify(titolo: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", titolo.lower()).strip("-")


def main() -> None:
    p = argparse.ArgumentParser(description="Build procedura clinica Mobilitas -> docx")
    p.add_argument("markdown", type=Path, help="File markdown sorgente")
    p.add_argument("titolo", help="Nome della condizione, es. 'Reflusso Gastroesofageo'")
    p.add_argument("-o", "--output", type=Path, default=None, help="Path di output .docx")
    p.add_argument("--slug", default=None,
                   help="Sottocartella sotto outputs/ (default: dedotto dal titolo). "
                        "Usa lo stesso slug di procedure-generate/<slug>/ per tenerli allineati.")
    args = p.parse_args()

    out = args.output
    if out is None:
        # La scheda e la procedura convivono nella stessa cartella: il nome del file
        # deve distinguerle, altrimenti la seconda conversione sovrascrive la prima.
        nome = re.sub(r"[^A-Za-z0-9]+", "_", args.titolo).strip("_")
        prefisso = "Scheda_Operativa" if "scheda" in args.markdown.name.lower() else "Procedura"
        out = OUTPUTS / (args.slug or slugify(args.titolo)) / f"{prefisso}_{nome}.docx"

    build(args.markdown, args.titolo, out)


if __name__ == "__main__":
    main()

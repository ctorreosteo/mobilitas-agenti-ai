#!/usr/bin/env python3
"""Hook PreToolUse — impedisce all'agente GDPR di modificare il codice del gestionale.

Regole:
  * dentro workspace/  → consentiti SOLO i file .md
  * dentro agente-gdpr/ (fuori da workspace/) → tutto consentito (report, config, appunti)
  * fuori dalla cartella dell'agente → consentito solo lo scratchpad temporaneo

Uscita 2 = operazione bloccata; il messaggio su stderr torna al modello.
"""
import json
import os
import sys
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = AGENT_ROOT / "workspace"
TMP_OK = ("/tmp/", "/private/tmp/", "/var/folders/")


def blocca(msg: str) -> None:
    sys.stderr.write(msg)
    sys.exit(2)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)  # payload illeggibile: non interferire

    tool_input = payload.get("tool_input") or {}
    raw = (
        tool_input.get("file_path")
        or tool_input.get("notebook_path")
        or tool_input.get("path")
        or ""
    )
    if not raw:
        sys.exit(0)

    cwd = payload.get("cwd") or os.getcwd()
    path = Path(raw)
    if not path.is_absolute():
        path = Path(cwd) / path
    try:
        path = path.resolve()
    except Exception:
        path = Path(os.path.abspath(str(path)))

    s = str(path)
    is_md = path.suffix.lower() in (".md", ".markdown")

    if s.startswith(str(WORKSPACE) + os.sep):
        if is_md:
            sys.exit(0)
        blocca(
            f"🚫 BLOCCATO — stavi per scrivere su un file del gestionale che non è Markdown:\n"
            f"   {s}\n\n"
            "L'agente GDPR non modifica MAI il codice: dentro workspace/ sono consentiti solo i file .md.\n"
            "Azione corretta: NON tentare vie alternative (sed, redirezioni, patch). "
            "Registra il problema come criticità in report/CRITICITA-GDPR.md, indicando file:riga, "
            "articolo GDPR violato, rischio e intervento suggerito, e lascia che sia l'utente a "
            "decidere se implementarlo.\n"
        )

    if s.startswith(str(AGENT_ROOT) + os.sep) or s == str(AGENT_ROOT):
        sys.exit(0)

    if any(s.startswith(p) for p in TMP_OK):
        sys.exit(0)

    blocca(
        f"🚫 BLOCCATO — scrittura fuori dalla cartella dell'agente:\n   {s}\n\n"
        f"L'agente GDPR scrive solo dentro {AGENT_ROOT} (e file .md dentro workspace/).\n"
        "I repository locali dell'utente non vanno toccati: usa le copie in workspace/.\n"
    )


if __name__ == "__main__":
    main()

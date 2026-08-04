#!/usr/bin/env python3
"""Hook PreToolUse — impedisce all'agente GDPR di modificare il codice del gestionale.

L'agente lavora DIRETTAMENTE nei repository reali (config/repos.json → "path"),
quindi la protezione non può più essere "non scrivere fuori da casa tua": deve
distinguere, dentro i repo dell'utente, i Markdown da tutto il resto.

Regole (whitelist):
  * dentro un repo del gestionale  → consentiti SOLO i file .md
  * dentro agente-gdpr/            → tutto consentito (report, config, appunti)
  * scratchpad temporaneo          → consentito
  * qualunque altro percorso       → bloccato

Uscita 2 = operazione bloccata; il messaggio su stderr torna al modello.
"""
import json
import os
import sys
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[2]
CONFIG = AGENT_ROOT / "config" / "repos.json"
TMP_OK = ("/tmp/", "/private/tmp/", "/var/folders/")


def blocca(msg: str) -> None:
    sys.stderr.write(msg)
    sys.exit(2)


def repos_gestionale():
    """Percorsi dei repository del gestionale. None se la config è illeggibile."""
    try:
        dati = json.loads(CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return None
    percorsi = []
    for r in dati.get("repos", []):
        p = r.get("path")
        if p:
            try:
                percorsi.append(str(Path(p).expanduser().resolve()))
            except Exception:
                percorsi.append(os.path.abspath(os.path.expanduser(p)))
    return percorsi or None


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
    dentro_agente = s == str(AGENT_ROOT) or s.startswith(str(AGENT_ROOT) + os.sep)

    repos = repos_gestionale()
    if repos is None:
        # fail closed: senza config non so quali repo proteggere
        if dentro_agente or any(s.startswith(p) for p in TMP_OK):
            sys.exit(0)
        blocca(
            "🚫 BLOCCATO — config/repos.json illeggibile: non posso sapere quali repository\n"
            "   proteggere, quindi consento scritture solo dentro la cartella dell'agente.\n"
            f"   percorso richiesto: {s}\n"
        )

    for repo in repos:
        if s == repo or s.startswith(repo + os.sep):
            if is_md:
                sys.exit(0)
            blocca(
                f"🚫 BLOCCATO — stavi per scrivere su un file del gestionale che non è Markdown:\n"
                f"   {s}\n\n"
                "L'agente GDPR non modifica MAI il codice: nei repository del gestionale sono\n"
                "consentiti solo i file .md.\n"
                "Azione corretta: NON tentare vie alternative (sed, redirezioni, patch, python -c). "
                "Registra il problema come criticità in report/CRITICITA-GDPR.md, indicando file:riga, "
                "articolo GDPR violato, rischio e intervento suggerito, e lascia che sia l'utente a "
                "decidere se implementarlo.\n"
            )

    if dentro_agente:
        sys.exit(0)

    if any(s.startswith(p) for p in TMP_OK):
        sys.exit(0)

    blocca(
        f"🚫 BLOCCATO — scrittura fuori dal perimetro consentito:\n   {s}\n\n"
        f"L'agente GDPR scrive solo dentro {AGENT_ROOT}\n"
        "e, limitatamente ai file .md, dentro i repository elencati in config/repos.json.\n"
    )


if __name__ == "__main__":
    main()

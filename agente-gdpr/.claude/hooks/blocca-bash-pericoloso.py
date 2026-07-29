#!/usr/bin/env python3
"""Hook PreToolUse su Bash — chiude le vie laterali per modificare il codice.

Blocca:
  * git push / git remote set-url --push (nessuna pubblicazione automatica)
  * riscritture in-place (sed -i, perl -i, patch, git apply) su workspace/
  * redirezioni  >  >>  o `tee` verso file non .md dentro workspace/
  * rm / mv / cp / chmod / truncate su file non .md dentro workspace/

Uscita 2 = comando bloccato.
"""
import json
import re
import sys

MD_EXT = (".md", ".markdown")

REDIR = re.compile(r">>?\s*([^\s;|&<>]+)")
INPLACE = re.compile(r"\b(sed\s+(-[a-zA-Z]*\s+)*-i|perl\s+-[a-zA-Z]*i|patch\b|git\s+apply\b)")
MUTANTI = re.compile(r"(?:^|[;&|]\s*|\s)(rm|mv|cp|tee|truncate|chmod|chown|dd|install)\s")
TOKEN_WS = re.compile(r"[^\s;|&'\"]*workspace/[^\s;|&'\"]*")


def blocca(motivo: str, comando: str) -> None:
    sys.stderr.write(
        f"🚫 BLOCCATO — {motivo}\n"
        f"   comando: {comando.strip()[:300]}\n\n"
        "L'agente GDPR non modifica il codice del gestionale e non pubblica nulla.\n"
        "Se il problema è reale, va scritto in report/CRITICITA-GDPR.md, non risolto qui.\n"
    )
    sys.exit(2)


def non_md(tok: str) -> bool:
    """True se il token punta a un file del workspace che non è Markdown."""
    if "workspace/" not in tok:
        return False
    base = tok.rstrip("/").split("/")[-1]
    if "." not in base:          # directory o path senza estensione
        return True
    return not base.lower().endswith(MD_EXT)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    cmd = (payload.get("tool_input") or {}).get("command") or ""
    if not cmd:
        sys.exit(0)

    if re.search(r"\bgit\s+(-C\s+\S+\s+)?push\b", cmd):
        blocca("push vietato: le modifiche restano locali e le pubblica l'utente", cmd)

    if re.search(r"\bgit\s+remote\s+set-url\s+--push\b", cmd):
        blocca("riabilitare il push sulle copie di lavoro non è consentito", cmd)

    if INPLACE.search(cmd) and "workspace/" in cmd:
        blocca("riscrittura in-place di file del gestionale", cmd)

    for target in REDIR.findall(cmd):
        if non_md(target):
            blocca(f"redirezione verso un file non-Markdown del gestionale ({target})", cmd)

    if MUTANTI.search(cmd):
        for tok in TOKEN_WS.findall(cmd):
            if non_md(tok):
                blocca(f"comando che altera file del gestionale ({tok})", cmd)

    sys.exit(0)


if __name__ == "__main__":
    main()

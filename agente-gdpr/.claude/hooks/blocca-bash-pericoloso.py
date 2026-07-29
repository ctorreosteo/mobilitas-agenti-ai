#!/usr/bin/env python3
"""Hook PreToolUse su Bash — chiude le vie laterali per modificare il codice.

L'hook su Write|Edit lavora a whitelist ed è la difesa primaria; questo copre Bash,
dove la scrittura può avvenire in molti modi indiretti.

Blocca:
  * git push / git clean / git remote set-url --push (nessuna pubblicazione, nessuna pulizia)
  * riscritture in-place (sed -i, perl -i, awk -i inplace, patch, git apply, ed, ex, vi/vim -c)
  * interpreti che eseguono codice inline o heredoc con intento di scrittura
    (python, node, deno, bun, ruby, perl, php, osascript)
  * redirezioni  >  >>  >|  o `tee` verso file non .md dentro workspace/
  * rm / mv / cp / ln / chmod / truncate / dd … su file non .md dentro workspace/
  * find … -delete / -exec su workspace/

Quando la shell si trova già dentro workspace/ valgono anche i percorsi nudi,
non solo quelli che contengono la stringa "workspace/".

Uscita 2 = comando bloccato.
"""
import json
import re
import sys

MD_EXT = (".md", ".markdown")

GIT_PUSH = re.compile(
    r"\bgit\s+(?:(?:-c|-C|--git-dir|--work-tree|--exec-path)(?:=\S+|\s+\S+)\s+)*push\b"
)
GIT_CLEAN = re.compile(
    r"\bgit\s+(?:(?:-c|-C|--git-dir|--work-tree|--exec-path)(?:=\S+|\s+\S+)\s+)*clean\b"
)
GIT_SET_URL = re.compile(
    r"\bgit\s+(?:(?:-c|-C|--git-dir|--work-tree|--exec-path)(?:=\S+|\s+\S+)\s+)*remote\s+set-url\b"
)

INPLACE = re.compile(
    r"\b(?:sed\s+(?:-[a-zA-Z]*\s+)*-i"
    r"|perl\s+-[a-zA-Z]*i"
    r"|awk\s+-i\s+inplace"
    r"|git\s+apply\b"
    r"|vim?\s+-[a-zA-Z]*[cs]\b)"
)
# ed/ex/patch solo in posizione di comando: sono parole comuni nei messaggi di commit italiani
COMANDO_EDIT = re.compile(r"(?:^|[;&|]\s*)(?:ed|ex|patch)\s")

INTERPRETE = re.compile(
    r"\b(?:python[0-9.]*|node|deno|bun|ruby|perl|php|osascript)\b"
    r"[^;&|]*?(?:\s-[ecprE]\b|\seval\b|<<)"
)

# indizi di scrittura dentro il codice inline di un interprete
SCRITTURA = re.compile(
    r"""(?x)
      \b(?:writeFile|appendFile|createWriteStream|copyFile|truncate
         |rm|rmdir|unlink|rename|mkdir)(?:Sync)?\s*\(
    | \bopen\s*\([^)]*['"][rbt]*[wax]\+?[rbt]*['"]
    | \.\s*write_text\s*\( | \.\s*write_bytes\s*\(
    | \bshutil\s*\.\s*(?:copy|copy2|move|rmtree)
    | \bos\s*\.\s*(?:remove|unlink|rename|replace|rmdir|truncate)
    | \bFile\s*\.\s*(?:write|delete|rename)
    | \bIO\s*\.\s*write | \bFileUtils\b
    """
)

MUTANTI = re.compile(
    r"(?:^|[;&|]\s*|\s)(rm|mv|cp|tee|truncate|chmod|chown|dd|install|ln|shred|unlink)\s"
)
FIND_DISTRUTTIVO = re.compile(r"\bfind\b[^;&|]*?(?:-delete\b|-exec\b)")

REDIR = re.compile(r">\|?>?\s*([^\s;|&<>]+)")
TOKEN_WS = re.compile(r"[^\s;|&'\"]*workspace/[^\s;|&'\"]*")
CD_WS = re.compile(r"\bcd\s+[^\s;&|]*workspace(?:/|\s|$)")
NAVIGAZIONE = re.compile(r"\b(?:cd|pushd|git\s+-C)\s+[^\s;&|]+")

# token che sembra un percorso di file: ha un'estensione breve oppure contiene "/"
ESTENSIONE = re.compile(r"\.[A-Za-z0-9]{1,8}$")
TOKEN_NUDO = re.compile(r"[^\s;|&'\"<>]+")


def blocca(motivo: str, comando: str) -> None:
    sys.stderr.write(
        f"🚫 BLOCCATO — {motivo}\n"
        f"   comando: {comando.strip()[:300]}\n\n"
        "L'agente GDPR non modifica il codice del gestionale e non pubblica nulla.\n"
        "Non cercare vie alternative: se il problema è reale va scritto in\n"
        "report/CRITICITA-GDPR.md (file:riga, articolo GDPR, rischio, intervento suggerito),\n"
        "e sarà l'utente a decidere se implementarlo.\n"
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


def nudo_sospetto(tok: str) -> bool:
    """Come non_md, ma per percorsi relativi quando la shell è già dentro workspace/."""
    tok = tok.strip("'\"").rstrip("/")
    if not tok or tok.startswith("-"):
        return False
    base = tok.split("/")[-1]
    if base.lower().endswith(MD_EXT):
        return False
    if ESTENSIONE.search(base):  # file con estensione non-Markdown
        return True
    return "/" in tok            # directory o percorso senza estensione


def senza_navigazione(cmd: str) -> str:
    """Toglie gli argomenti di cd/pushd/git -C: sono destinazioni, non bersagli."""
    return NAVIGAZIONE.sub(" ", cmd)


def bersagli(cmd: str, dentro_ws: bool) -> list:
    """Percorsi di file del gestionale, non Markdown, toccati dal comando."""
    cmd = senza_navigazione(cmd)
    trovati = [t for t in TOKEN_WS.findall(cmd) if non_md(t)]
    if dentro_ws:
        trovati += [t for t in TOKEN_NUDO.findall(cmd) if nudo_sospetto(t)]
    return trovati


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    cmd = (payload.get("tool_input") or {}).get("command") or ""
    if not cmd:
        sys.exit(0)

    cwd = payload.get("cwd") or ""
    dentro_ws = "/workspace/" in (cwd.rstrip("/") + "/") or bool(CD_WS.search(cmd))
    tocca_ws = "workspace" in cmd or dentro_ws

    if GIT_PUSH.search(cmd):
        blocca("push vietato: le modifiche restano locali e le pubblica l'utente", cmd)

    if GIT_SET_URL.search(cmd):
        blocca("cambiare l'origin delle copie di lavoro non è consentito", cmd)

    if GIT_CLEAN.search(cmd) and tocca_ws:
        blocca("git clean cancellerebbe anche i documenti privacy non ancora committati", cmd)

    if (INPLACE.search(cmd) or COMANDO_EDIT.search(cmd)) and tocca_ws:
        blocca("riscrittura in-place di file del gestionale", cmd)

    if FIND_DISTRUTTIVO.search(cmd) and tocca_ws:
        blocca("find distruttivo sul gestionale: l'audit è di sola lettura", cmd)

    if INTERPRETE.search(cmd) and SCRITTURA.search(cmd) and tocca_ws:
        blocca(
            "codice inline che scrive su file del gestionale "
            "(python/node/… non sono una scorciatoia per aggirare il blocco)",
            cmd,
        )

    for target in REDIR.findall(cmd):
        if non_md(target) or (dentro_ws and nudo_sospetto(target)):
            blocca(f"redirezione verso un file non-Markdown del gestionale ({target})", cmd)

    if MUTANTI.search(cmd):
        colpiti = bersagli(cmd, dentro_ws)
        if colpiti:
            blocca(f"comando che altera file del gestionale ({colpiti[0]})", cmd)

    sys.exit(0)


if __name__ == "__main__":
    main()

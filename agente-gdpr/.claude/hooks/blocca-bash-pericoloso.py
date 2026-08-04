#!/usr/bin/env python3
"""Hook PreToolUse su Bash — chiude le vie laterali per modificare il codice.

L'agente lavora direttamente nei repository reali dell'utente (config/repos.json →
"path"): oltre alle scritture, qui vanno fermati anche i comandi git che
distruggerebbero lavoro non suo (reset --hard, clean, stash, rebase, amend) e
quelli che rastrellerebbero le sue modifiche in corso dentro un commit di
documentazione (commit -a, add -A senza filtro sui .md).

Blocca:
  * git push / clean / stash / rebase / reset --hard / commit --amend / branch -D
    / filter-branch / update-ref / worktree / reflog / remote set-url
  * git commit -a|--all   e   git add senza alcun riferimento a .md
  * riscritture in-place (sed -i, perl -i, awk -i inplace, patch, git apply, ed, ex, vi -c)
  * interpreti con codice inline o heredoc e intento di scrittura
    (python -c, node -e, ruby, perl, php, osascript, heredoc)
  * redirezioni  >  >>  >|  o `tee` verso file non .md del gestionale
  * rm / mv / cp / ln / chmod / truncate / dd … su file non .md del gestionale
  * find … -delete / -exec sul gestionale

Vale anche per i percorsi nudi, quando la shell è già dentro un repo del gestionale.
Uscita 2 = comando bloccato.
"""
import json
import os
import re
import sys
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[2]
CONFIG = AGENT_ROOT / "config" / "repos.json"
MD_EXT = (".md", ".markdown")

G = r"\bgit\s+(?:(?:-c|-C|--git-dir|--work-tree|--exec-path)(?:=\S+|\s+\S+)\s+)*"

GIT_PUSH = re.compile(G + r"push\b")
GIT_DISTRUTTIVI = re.compile(
    G + r"(?:clean|stash|rebase|filter-branch|update-ref|worktree|reflog"
        r"|remote\s+set-url|cherry-pick|revert)\b"
)
GIT_RESET_DURO = re.compile(G + r"reset\b[^;&|]*--(?:hard|merge|keep)\b")
GIT_AMEND = re.compile(G + r"commit\b[^;&|]*--amend\b")
GIT_COMMIT_TUTTO = re.compile(G + r"commit\b[^;&|]*(?:\s--all\b|\s-[a-zA-Z]*a[a-zA-Z]*\b)")
GIT_BRANCH_DEL = re.compile(G + r"branch\b[^;&|]*\s-[dD]\b")
GIT_ADD = re.compile(G + r"add\b")

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
NAVIGAZIONE = re.compile(r"\b(?:cd|pushd|git\s+-C)\s+[^\s;&|]+")
ESTENSIONE = re.compile(r"\.[A-Za-z0-9]{1,8}$")
TOKEN = re.compile(r"[^\s;|&'\"<>]+")


def blocca(motivo: str, comando: str) -> None:
    sys.stderr.write(
        f"🚫 BLOCCATO — {motivo}\n"
        f"   comando: {comando.strip()[:300]}\n\n"
        "L'agente GDPR lavora nei repository reali dell'utente: non modifica il codice,\n"
        "non pubblica nulla e non tocca il lavoro non committato.\n"
        "Se il problema è reale va scritto in report/CRITICITA-GDPR.md (file:riga,\n"
        "articolo GDPR, rischio, intervento suggerito), non risolto qui.\n"
    )
    sys.exit(2)


def repos_gestionale():
    """(percorsi assoluti, marcatori riconoscibili nei comandi)."""
    try:
        dati = json.loads(CONFIG.read_text(encoding="utf-8"))
    except Exception:
        return [], []
    percorsi = []
    for r in dati.get("repos", []):
        p = r.get("path")
        if not p:
            continue
        try:
            percorsi.append(str(Path(p).expanduser().resolve()))
        except Exception:
            percorsi.append(os.path.abspath(os.path.expanduser(p)))
    marcatori = percorsi + [os.path.basename(p) + "/" for p in percorsi]
    return percorsi, marcatori


def non_md(tok: str) -> bool:
    """Il token è un percorso che non è un file Markdown?"""
    base = tok.rstrip("/").split("/")[-1]
    if "." not in base:      # directory o percorso senza estensione
        return True
    return not base.lower().endswith(MD_EXT)


def nudo_sospetto(tok: str) -> bool:
    """Percorso relativo pericoloso, quando la shell è già dentro un repo."""
    tok = tok.strip("'\"").rstrip("/")
    if not tok or tok.startswith("-"):
        return False
    base = tok.split("/")[-1]
    if base.lower().endswith(MD_EXT):
        return False
    if ESTENSIONE.search(base):
        return True
    return "/" in tok


def bersagli(cmd: str, marcatori, dentro_repo: bool) -> list:
    """Percorsi di file del gestionale, non Markdown, toccati dal comando."""
    cmd = NAVIGAZIONE.sub(" ", cmd)   # cd/git -C indicano una destinazione, non un bersaglio
    trovati = []
    for grezzo in TOKEN.findall(cmd):
        tok = grezzo.strip("'\"")
        if not tok:
            continue
        if any(m in tok for m in marcatori):
            if non_md(tok):
                trovati.append(tok)
        elif dentro_repo and nudo_sospetto(tok):
            trovati.append(tok)
    return trovati


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    cmd = (payload.get("tool_input") or {}).get("command") or ""
    if not cmd:
        sys.exit(0)

    percorsi, marcatori = repos_gestionale()
    cwd = (payload.get("cwd") or "").rstrip("/")
    dentro_repo = any(cwd == p or cwd.startswith(p + os.sep) for p in percorsi)
    tocca_repo = dentro_repo or any(m in cmd for m in marcatori)

    # ── git: pubblicazione e comandi che distruggono lavoro non nostro ──────
    if GIT_PUSH.search(cmd):
        blocca("push vietato: le modifiche restano locali e le pubblica l'utente", cmd)

    if tocca_repo:
        if GIT_DISTRUTTIVI.search(cmd):
            blocca("comando git che può distruggere lavoro non committato dell'utente", cmd)
        if GIT_RESET_DURO.search(cmd):
            blocca("reset distruttivo su un repository di lavoro dell'utente", cmd)
        if GIT_AMEND.search(cmd):
            blocca("riscrivere un commit esistente dell'utente non è consentito", cmd)
        if GIT_BRANCH_DEL.search(cmd):
            blocca("cancellare un branch dell'utente non è consentito", cmd)
        if GIT_COMMIT_TUTTO.search(cmd):
            blocca(
                "commit -a/--all rastrellerebbe anche le modifiche in corso dell'utente: "
                "aggiungi esplicitamente i soli .md",
                cmd,
            )
        if GIT_ADD.search(cmd) and ".md" not in cmd:
            blocca(
                "git add senza filtro sui Markdown: usa la forma "
                "git add -A ':(glob)**/*.md'",
                cmd,
            )

    # ── scritture indirette sul codice ─────────────────────────────────────
    if (INPLACE.search(cmd) or COMANDO_EDIT.search(cmd)) and tocca_repo:
        blocca("riscrittura in-place di file del gestionale", cmd)

    if FIND_DISTRUTTIVO.search(cmd) and tocca_repo:
        blocca("find distruttivo sul gestionale: l'audit è di sola lettura", cmd)

    if INTERPRETE.search(cmd) and SCRITTURA.search(cmd) and tocca_repo:
        blocca(
            "codice inline che scrive su file del gestionale "
            "(python/node/… non sono una scorciatoia per aggirare il blocco)",
            cmd,
        )

    for target in REDIR.findall(cmd):
        t = target.strip("'\"")
        if any(m in t for m in marcatori):
            if non_md(t):
                blocca(f"redirezione verso un file non-Markdown del gestionale ({t})", cmd)
        elif dentro_repo and nudo_sospetto(t):
            blocca(f"redirezione verso un file non-Markdown del gestionale ({t})", cmd)

    if MUTANTI.search(cmd):
        colpiti = bersagli(cmd, marcatori, dentro_repo)
        if colpiti:
            blocca(f"comando che altera file del gestionale ({colpiti[0]})", cmd)

    sys.exit(0)


if __name__ == "__main__":
    main()

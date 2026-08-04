#!/usr/bin/env python3
"""Suite di test degli hook di protezione dell'agente GDPR.

L'agente lavora direttamente nei repository reali: questi test verificano che il
codice resti intoccabile, che il lavoro non committato dell'utente sia al sicuro
e che il flusso legittimo (audit in lettura, scrittura dei .md) non venga bloccato.
"""
import json
import subprocess
import sys

ROOT = "/Users/carlitos/mobilitas-agenti-ai/agente-gdpr"
BASH = f"{ROOT}/.claude/hooks/blocca-bash-pericoloso.py"
FILE = f"{ROOT}/.claude/hooks/blocca-modifiche-codice.py"

AG = ROOT
BE = "/Users/carlitos/mobilitas-backend"
FE = "/Users/carlitos/mobilitas-frontend"

BLOCCA, PASSA = 2, 0


def run(hook, payload):
    p = subprocess.run(["python3", hook], input=json.dumps(payload),
                       capture_output=True, text=True)
    return p.returncode


casi_bash = [
    # ── pubblicazione ──────────────────────────────────────────────────────
    (BLOCCA, "git push",                f"git -C {BE} push origin main", AG),
    (BLOCCA, "git -c ... push",         "git -c user.name=x push", AG),
    (BLOCCA, "cd + push",               f"cd {BE} && git push", AG),
    (BLOCCA, "push da dentro il repo",  "git push origin gdpr/aggiornamento-docs", BE),

    # ── comandi git che distruggono lavoro dell'utente ─────────────────────
    (BLOCCA, "git reset --hard",        f"git -C {BE} reset --hard origin/main", AG),
    (BLOCCA, "git clean -fd",           f"git -C {BE} clean -fd", AG),
    (BLOCCA, "git stash",               "git stash", BE),
    (BLOCCA, "git rebase",              f"git -C {FE} rebase main", AG),
    (BLOCCA, "git commit --amend",      "git commit --amend -m x", BE),
    (BLOCCA, "git commit -a",           "git commit -a -m 'docs'", BE),
    (BLOCCA, "git commit -am",          "git commit -am 'docs'", BE),
    (BLOCCA, "git branch -D",           f"git -C {BE} branch -D main", AG),
    (BLOCCA, "git add -A senza filtro", "git add -A", BE),
    (BLOCCA, "git add .",               "git add .", BE),
    (BLOCCA, "git remote set-url",      f"git -C {BE} remote set-url origin x", AG),
    (BLOCCA, "git cherry-pick",         "git cherry-pick abc123", BE),

    # ── scritture indirette sul codice ─────────────────────────────────────
    (BLOCCA, "sed -i su java",          f"sed -i '' s/a/b/ {BE}/src/A.java", AG),
    (BLOCCA, "perl -pi",                f"perl -pi -e s/a/b/ {BE}/src/A.java", AG),
    (BLOCCA, "awk -i inplace",          f"awk -i inplace '{{print}}' {BE}/A.java", AG),
    (BLOCCA, "git apply",               f"git apply x.diff --directory {BE}", AG),
    (BLOCCA, "cat > java",              f"cat > {BE}/src/A.java", AG),
    (BLOCCA, "redirezione >|",          f"echo x >| {BE}/pom.xml", AG),
    (BLOCCA, "append >>",               f"echo x >> {FE}/package.json", AG),
    (BLOCCA, "tee",                     f"echo x | tee {BE}/src/A.java", AG),
    (BLOCCA, "python -c write",         f"python3 -c \"open('{BE}/A.java','w').write('x')\"", AG),
    (BLOCCA, "python heredoc",          f"python3 << EOF\nopen('{BE}/A.java','w')\nEOF", AG),
    (BLOCCA, "node writeFileSync",      f"node -e 'require(\"fs\").writeFileSync(\"{BE}/A.java\",\"x\")'", AG),
    (BLOCCA, "node rmSync",             f"node -e 'require(\"fs\").rmSync(\"{BE}/A.java\")'", AG),
    (BLOCCA, "ruby File.write",         f"ruby -e 'File.write(\"{BE}/A.java\",\"x\")'", AG),
    (BLOCCA, "python os.remove",        f"python3 -c \"import os; os.remove('{BE}/A.java')\"", AG),
    (BLOCCA, "ln -sf",                  f"ln -sf /dev/null {BE}/src/A.java", AG),
    (BLOCCA, "rm java",                 f"rm {BE}/src/A.java", AG),
    (BLOCCA, "rm -rf directory",        f"rm -rf {BE}/src", AG),
    (BLOCCA, "mv java",                 f"mv {BE}/A.java {BE}/B.java", AG),
    (BLOCCA, "chmod",                   f"chmod 777 {BE}/mvnw", AG),
    (BLOCCA, "find -delete",            f"find {BE} -name '*.java' -delete", AG),
    (BLOCCA, "find -exec rm",           f"find {FE} -name '*.ts' -exec rm {{}} \\;", AG),
    (BLOCCA, "path per basename",       "rm mobilitas-backend/src/A.java", "/Users/carlitos"),
    (BLOCCA, "ed in posizione comando", f"ed {BE}/A.java", AG),

    # ── cwd già dentro il repo: contano i percorsi nudi ────────────────────
    (BLOCCA, "cwd repo: rm nudo",       "rm src/A.java", BE),
    (BLOCCA, "cwd repo: sed -i",        "sed -i '' s/a/b/ src/A.java", BE),
    (BLOCCA, "cwd repo: redirezione",   "echo x > pom.xml", BE),
    (BLOCCA, "cwd repo: rm dir",        "rm -rf src/main", BE),

    # ── falsi positivi: DEVONO passare ─────────────────────────────────────
    (PASSA, "rg ricerca",               f"rg -n 'class' {BE}/src", AG),
    (PASSA, "grep ricerca",             f"grep -rn 'localStorage' {FE}/src", AG),
    (PASSA, "find md",                  f"find {BE} -name '*.md'", AG),
    (PASSA, "ls",                       f"ls -la {BE}/docs/privacy", AG),
    (PASSA, "head su java (lettura)",   f"head -50 {BE}/src/A.java", AG),
    (PASSA, "git status",               f"git -C {BE} status --short", AG),
    (PASSA, "git diff branch",          f"git -C {BE} diff --stat main...gdpr/aggiornamento-docs", AG),
    (PASSA, "git log",                  f"git -C {BE} log --oneline -5", AG),
    (PASSA, "git add solo md",          "git add -A ':(glob)**/*.md'", BE),
    (PASSA, "git add file md",          "git add docs/privacy/02-registro-trattamenti.md", BE),
    (PASSA, "git commit italiano",      "git commit -m 'docs(privacy): registro aggiornato ed allineato'", BE),
    (PASSA, "git checkout ripristino",  f"git -C {BE} checkout main -- src/A.java", AG),
    (PASSA, "git checkout branch",      f"git -C {BE} checkout gdpr/aggiornamento-docs", AG),
    (PASSA, "cd repo + cp fra md",      f"cd {BE} && cp docs/privacy/02.md docs/privacy/02-bak.md", AG),
    (PASSA, "copia report nei docs",    f"cp report/CRITICITA-GDPR.md {BE}/docs/privacy/99-criticita.md", AG),
    (PASSA, "script di preparazione",   "./scripts/prepara-repos.sh", AG),
    (PASSA, "jq su config",             "jq -r '.branchLavoro' config/repos.json", AG),
    (PASSA, "mkdir evidenze",           "mkdir -p report/evidenze", AG),
    (PASSA, "scrittura report md",      "echo '# report' > report/evidenze/01-inventario-dati.md", AG),
    (PASSA, "redirez. /dev/null",       f"rg -n x {BE} 2>/dev/null", AG),
    (PASSA, "python lettura",           "python3 -c \"print(open('config/repos.json').read())\"", AG),
    (PASSA, "wc su md",                 f"wc -l {BE}/docs/privacy/02-registro-trattamenti.md", AG),
    (PASSA, "rm fuori dal gestionale",  "rm -rf /private/tmp/claude-501/scratch/x", AG),
    (PASSA, "git add nel repo agente",  "git add report/CRITICITA-GDPR.md", AG),
]

casi_file = [
    (BLOCCA, "java nel backend",     f"{BE}/src/main/java/A.java"),
    (BLOCCA, "json nel frontend",    f"{FE}/package.json"),
    (BLOCCA, "properties",           f"{BE}/src/main/resources/application-prod.properties"),
    (BLOCCA, "migrazione sql",       f"{BE}/src/main/resources/db/migration/V1__init.sql"),
    (BLOCCA, "senza estensione",     f"{BE}/Dockerfile"),
    (BLOCCA, "apps script",          f"{BE}/apps-script-cartella-clinica.gs"),
    (BLOCCA, "env frontend",         f"{FE}/.env"),
    (BLOCCA, "percorso relativo ..", "../../mobilitas-backend/pom.xml"),
    (BLOCCA, "home utente",          "/Users/carlitos/.zshrc"),
    (PASSA,  "md nel backend",       f"{BE}/docs/privacy/02-registro-trattamenti.md"),
    (PASSA,  "md nuovo nel backend", f"{BE}/docs/privacy/08-politica-conservazione.md"),
    (PASSA,  "md nel frontend",      f"{FE}/docs/privacy/README.md"),
    (PASSA,  "md maiuscolo",         f"{BE}/docs/README.MD"),
    (PASSA,  "report criticita",     f"{AG}/report/CRITICITA-GDPR.md"),
    (PASSA,  "evidenze",             f"{AG}/report/evidenze/01-inventario-dati.md"),
    (PASSA,  "config dell'agente",   f"{AG}/config/repos.json"),
    (PASSA,  "scratchpad",           "/private/tmp/claude-501/x/scratch/note.txt"),
]

falliti = 0
print("═══ hook Bash ═══")
for atteso, desc, cmd, cwd in casi_bash:
    got = run(BASH, {"tool_input": {"command": cmd}, "cwd": cwd})
    if got != atteso:
        falliti += 1
        print(f"  ✗ {desc:<28} atteso={'BLOCCA' if atteso == 2 else 'PASSA'} "
              f"ottenuto={'BLOCCA' if got == 2 else 'PASSA'}")
        print(f"      {cmd!r} (cwd={cwd})")
print(f"  {len(casi_bash)} casi, {len(casi_bash) - falliti} ok")

f2 = 0
print("═══ hook Write/Edit ═══")
for atteso, desc, path in casi_file:
    got = run(FILE, {"tool_input": {"file_path": path}, "cwd": AG})
    if got != atteso:
        f2 += 1
        print(f"  ✗ {desc:<28} atteso={'BLOCCA' if atteso == 2 else 'PASSA'} "
              f"ottenuto={'BLOCCA' if got == 2 else 'PASSA'}  {path}")
print(f"  {len(casi_file)} casi, {len(casi_file) - f2} ok")

tot = falliti + f2
print(f"\n{'✅ TUTTI I TEST PASSATI' if tot == 0 else f'❌ {tot} TEST FALLITI'}")
sys.exit(1 if tot else 0)

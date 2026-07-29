#!/usr/bin/env python3
"""Suite di test degli hook di protezione dell'agente GDPR."""
import json, subprocess, sys

ROOT = "/Users/carlitos/mobilitas-agenti-ai/agente-gdpr"
BASH = f"{ROOT}/.claude/hooks/blocca-bash-pericoloso.py"
FILE = f"{ROOT}/.claude/hooks/blocca-modifiche-codice.py"
AG = ROOT
WS = f"{AG}/workspace/mobilitas-backend"

def run(hook, payload):
    p = subprocess.run(["python3", hook], input=json.dumps(payload),
                       capture_output=True, text=True)
    return p.returncode

BLOCCA, PASSA = 2, 0

casi_bash = [
    # (attesa, descrizione, comando, cwd)
    (BLOCCA, "git push",                 "git -C workspace/mobilitas-backend push origin main", AG),
    (BLOCCA, "git -c ... push",          "git -c user.name=x push origin main", AG),
    (BLOCCA, "git --git-dir=... push",   "git --git-dir=workspace/x/.git push", AG),
    (BLOCCA, "cd + push",                "cd workspace/mobilitas-backend && git push", AG),
    (BLOCCA, "git clean nel workspace",  "git -C workspace/mobilitas-backend clean -fd", AG),
    (BLOCCA, "git remote set-url",       "git -C workspace/mobilitas-backend remote set-url origin x", AG),
    (BLOCCA, "sed -i su java",           "sed -i '' s/a/b/ workspace/mobilitas-backend/A.java", AG),
    (BLOCCA, "perl -pi",                 "perl -pi -e s/a/b/ workspace/mobilitas-backend/A.java", AG),
    (BLOCCA, "awk -i inplace",           "awk -i inplace '{print}' workspace/mobilitas-backend/A.java", AG),
    (BLOCCA, "patch",                    "patch -p1 < x.diff # workspace", AG),
    (BLOCCA, "git apply",                "git apply x.diff --directory workspace/mobilitas-backend", AG),
    (BLOCCA, "cat > java",               "cat > workspace/mobilitas-backend/A.java", AG),
    (BLOCCA, "redirezione >| ",          "echo x >| workspace/mobilitas-backend/A.java", AG),
    (BLOCCA, "append >>",                "echo x >> workspace/mobilitas-backend/pom.xml", AG),
    (BLOCCA, "tee",                      "echo x | tee workspace/mobilitas-backend/A.java", AG),
    (BLOCCA, "python -c write",          "python3 -c \"open('workspace/mobilitas-backend/A.java','w').write('x')\"", AG),
    (BLOCCA, "python heredoc",           "python3 << EOF\nopen('workspace/mobilitas-backend/A.java','w')\nEOF", AG),
    (BLOCCA, "python write_text",        "python3 -c \"Path('workspace/x/A.java').write_text('x')\"", AG),
    (BLOCCA, "node writeFileSync",       "node -e 'require(\"fs\").writeFileSync(\"workspace/x/A.java\",\"x\")'", AG),
    (BLOCCA, "node fs.rmSync",           "node -e 'require(\"fs\").rmSync(\"workspace/x/A.java\")'", AG),
    (BLOCCA, "ruby -e write",            "ruby -e 'File.write(\"workspace/x/A.java\",\"x\")'", AG),
    (BLOCCA, "python os.remove",         "python3 -c \"import os; os.remove('workspace/x/A.java')\"", AG),
    (BLOCCA, "ln -sf",                   "ln -sf /dev/null workspace/mobilitas-backend/A.java", AG),
    (BLOCCA, "rm java",                  "rm workspace/mobilitas-backend/A.java", AG),
    (BLOCCA, "rm -rf directory",         "rm -rf workspace/mobilitas-backend/src", AG),
    (BLOCCA, "mv java",                  "mv workspace/x/A.java workspace/x/B.java", AG),
    (BLOCCA, "chmod",                    "chmod 777 workspace/mobilitas-backend/mvnw", AG),
    (BLOCCA, "find -delete",             "find workspace/mobilitas-backend -name '*.java' -delete", AG),
    (BLOCCA, "find -exec rm",            "find workspace -name '*.ts' -exec rm {} \\;", AG),
    (BLOCCA, "cwd dentro ws: rm nudo",   "rm A.java", WS),
    (BLOCCA, "cwd dentro ws: sed -i",    "sed -i '' s/a/b/ src/A.java", WS),
    (BLOCCA, "cwd dentro ws: redirez.",  "echo x > pom.xml", WS),
    (BLOCCA, "cwd dentro ws: rm dir",    "rm -rf src/main", WS),
    (BLOCCA, "ed in posizione comando",  "ed workspace/mobilitas-backend/A.java", AG),

    # ── falsi positivi: DEVONO passare ──────────────────────────────────────
    (PASSA, "rg ricerca",                "rg -n 'class' workspace/mobilitas-backend/src", AG),
    (PASSA, "grep ricerca",              "grep -rn 'localStorage' workspace/mobilitas-frontend/src", AG),
    (PASSA, "find md",                   "find workspace/mobilitas-backend -name '*.md'", AG),
    (PASSA, "ls",                        "ls -la workspace/mobilitas-backend/docs/privacy", AG),
    (PASSA, "head su java (lettura)",    "head -50 workspace/mobilitas-backend/src/A.java", AG),
    (PASSA, "git status",                "git -C workspace/mobilitas-backend status --short", AG),
    (PASSA, "git diff branch",           "git -C workspace/mobilitas-backend diff --stat main...gdpr/aggiornamento-docs", AG),
    (PASSA, "git log",                   "git -C workspace/mobilitas-backend log --oneline -5", AG),
    (PASSA, "git add solo md",           "git add -A ':(glob)**/*.md'", WS),
    (PASSA, "git commit italiano",       "git commit -m 'docs(privacy): registro aggiornato ed allineato al codice'", WS),
    (PASSA, "git checkout ripristino",   "git -C workspace/mobilitas-backend checkout main -- src/A.java", AG),
    (PASSA, "copia report in docs",      "cp report/CRITICITA-GDPR.md workspace/mobilitas-backend/docs/privacy/99-criticita-e-gap-aperti.md", AG),
    (PASSA, "cd ws + cp fra md",         "cd workspace/mobilitas-backend && cp docs/privacy/02.md docs/privacy/02-bak.md", AG),
    (PASSA, "script di sync",            "./scripts/sync-repos.sh", AG),
    (PASSA, "jq su config",              "jq -r '.mode' config/repos.json", AG),
    (PASSA, "mkdir evidenze",            "mkdir -p report/evidenze", AG),
    (PASSA, "scrittura report md",       "echo '# report' > report/evidenze/01-inventario-dati.md", AG),
    (PASSA, "redirez. /dev/null",        "rg -n x workspace/mobilitas-backend 2>/dev/null", AG),
    (PASSA, "python lettura",            "python3 -c \"print(open('config/repos.json').read())\"", AG),
    (PASSA, "wc file md",                "wc -l workspace/mobilitas-backend/docs/privacy/02-registro-trattamenti.md", AG),
    (PASSA, "rm fuori dal workspace",    "rm -rf /private/tmp/claude-501/scratch/x", AG),
]

casi_file = [
    (BLOCCA, "java nel workspace",   f"{AG}/workspace/mobilitas-backend/A.java"),
    (BLOCCA, "json nel workspace",   f"{AG}/workspace/mobilitas-frontend/package.json"),
    (BLOCCA, "path relativo ..",     "../../mobilitas-backend/pom.xml"),
    (BLOCCA, "repo utente",          "/Users/carlitos/mobilitas-backend/pom.xml"),
    (BLOCCA, "senza estensione",     f"{AG}/workspace/mobilitas-backend/Dockerfile"),
    (BLOCCA, "home utente",          "/Users/carlitos/.zshrc"),
    (PASSA,  "md nel workspace",     f"{AG}/workspace/mobilitas-backend/docs/privacy/02.md"),
    (PASSA,  "md maiuscolo",         f"{AG}/workspace/mobilitas-backend/docs/README.MD"),
    (PASSA,  "report criticita",     f"{AG}/report/CRITICITA-GDPR.md"),
    (PASSA,  "evidenze",             f"{AG}/report/evidenze/01-inventario-dati.md"),
    (PASSA,  "config dell'agente",   f"{AG}/config/repos.json"),
    (PASSA,  "scratchpad",           "/private/tmp/claude-501/x/scratch/note.txt"),
]

falliti = 0
print("═══ hook Bash ═══")
for atteso, desc, cmd, cwd in casi_bash:
    got = run(BASH, {"tool_input": {"command": cmd}, "cwd": cwd})
    ok = (got == atteso)
    falliti += not ok
    if not ok:
        print(f"  ✗ {desc:<28} atteso={'BLOCCA' if atteso==2 else 'PASSA'} ottenuto={'BLOCCA' if got==2 else 'PASSA'}")
        print(f"      {cmd!r} (cwd={cwd})")
print(f"  {len(casi_bash)} casi, {len(casi_bash)-falliti} ok")

f2 = 0
print("═══ hook Write/Edit ═══")
for atteso, desc, path in casi_file:
    got = run(FILE, {"tool_input": {"file_path": path}, "cwd": AG})
    ok = (got == atteso)
    f2 += not ok
    if not ok:
        print(f"  ✗ {desc:<28} atteso={'BLOCCA' if atteso==2 else 'PASSA'} ottenuto={'BLOCCA' if got==2 else 'PASSA'}  {path}")
print(f"  {len(casi_file)} casi, {len(casi_file)-f2} ok")

tot = falliti + f2
print(f"\n{'✅ TUTTI I TEST PASSATI' if tot==0 else f'❌ {tot} TEST FALLITI'}")
sys.exit(1 if tot else 0)

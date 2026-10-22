#!/bin/sh
# Verifica statica dell'installazione (nessuna rete, nessun servizio, nessun credito, nessun file scritto nell'agente):
#   A. integrità (test/MANIFESTO.sha256) e file attesi;   B. percorsi: niente percorsi assoluti né riferimenti al laboratorio;
#   C. skill e agenti validi;   D. dipendenze;   E. nessun segreto;   F. configurazione;
#   G. attivazione SOLO esplicita: nessun file che Cursor o Claude Code caricano da soli, skill di richiamo corretta.
# Uso: test/verifica-installazione.sh
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
OK=0; KO=0; AV=0
esito() { if [ "$1" = 0 ]; then OK=$((OK+1)); echo "OK   $2"; else KO=$((KO+1)); echo "NO   $2"; fi; }
avviso() { AV=$((AV+1)); echo "--   $1"; }
echo "Verifica dell'installazione — $(date '+%d/%m/%Y %H:%M')"
testo() { find . \( -path '*/node_modules' -o -path ./.git \) -prune -o -type f ! -name .DS_Store ! -name '*.woff2' ! -name '*.png' ! -name '*.jpg' ! -path './skills/impeccable/scripts/bin/*' ! -path ./test/MANIFESTO.sha256 -print; }

# A
if [ -f test/MANIFESTO.sha256 ]; then
  d="$(shasum -a 256 -c test/MANIFESTO.sha256 2>/dev/null | grep -v ': OK$')"
  [ -z "$d" ]; esito $? "A1. integrità: $(wc -l < test/MANIFESTO.sha256 | tr -d ' ') file confrontati con il manifesto"
  [ -n "$d" ] && echo "$d" | head -10 | sed 's/^/     /'
  extra="$(find . \( -path '*/node_modules' -o -path ./.git \) -prune -o -type f ! -name .DS_Store ! -path ./config/mobilitas.json ! -path ./test/MANIFESTO.sha256 -print | sort | comm -23 - "$(f=$(mktemp); sed 's/^[0-9a-f]*  //' test/MANIFESTO.sha256 | sort > "$f"; echo "$f")")"
  [ -z "$extra" ]; esito $? "A2. nessun file estraneo nella cartella dell'agente${extra:+: $(echo $extra | head -c 300)}"
else esito 1 "A1. manca test/MANIFESTO.sha256 (tools/setup/manifesto.sh)"; fi
m=""; for f in README.md ISTRUZIONI.md config/mobilitas.example.json regole/sicurezza.md regole/contenuti-sanitari.md regole/direzione-estetica.md \
  workflow/fasi-comuni.md workflow/nuova-landing.md workflow/redesign.md workflow/ottimizzazione.md workflow/duplicazione.md workflow/importazione.md workflow/controllo-qualita.md \
  integrazioni/cursor-e-claude-code.md integrazioni/playwright.md integrazioni/superdesign.md integrazioni/skill-e-dipendenze.md \
  templates/collegamento/comando/SKILL.md templates/collegamento/nominato/SKILL.md tools/setup/collega.sh tools/setup/proteggi.sh \
  tools/incarico/nuovo.sh tools/incarico/registro.cjs tools/sito/avvia.sh tools/sito/vite-prova.sh tools/sito/dipendenze.mjs tools/playwright/protezione-test.js; do [ -f "$f" ] || m="$m $f"; done
[ -z "$m" ]; esito $? "A3. file principali presenti${m:+ — mancano:$m}"

# B
abs="$(testo | xargs grep -n -E '/Users/|/home/[a-z]|riccardonoto' 2>/dev/null | grep -v '^./test/verifica-installazione.sh')"
[ -z "$abs" ]; esito $? "B1. nessun percorso assoluto di una macchina"; [ -n "$abs" ] && echo "$abs" | head -5 | sed 's/^/     /'
lab="$(testo | grep -v -E '^./(riferimenti|licenze|skills|agenti)/|^./test/verifica-installazione.sh' | xargs grep -n -E '_Laboratorio|_d[0-9]+[a-z]?-|cefalea-d11|cervicalgia-d[0-9]|mobilitas-sito-web-test|_taste-lab|LAB/|nuovo-laboratorio|lab-guard' 2>/dev/null)"
[ -z "$lab" ]; esito $? "B2. nessun riferimento operativo al laboratorio o al vecchio modello a copie"; [ -n "$lab" ] && echo "$lab" | head -5 | sed 's/^/     /'
rel="$(grep -rn --exclude-dir=node_modules -E '\.\./\.\./\.\.' tools templates 2>/dev/null)"
[ -z "$rel" ]; esito $? "B3. nessun percorso relativo che esca dalla cartella dell'agente"
sl="$(find . -path '*/node_modules' -prune -o -type l -print)"; [ -z "$sl" ]; esito $? "B4. nessun collegamento simbolico"

# C
for d in skills/*/; do n="$(basename "$d")"; nome="$(sed -n '2,12p' "$d/SKILL.md" | sed -n 's/^name: *//p' | head -1)"
  [ "$(head -1 "$d/SKILL.md")" = "---" ] && [ "$nome" = "$n" ] && grep -q '^description:' "$d/SKILL.md"; esito $? "C. skill $n valida"; done
for f in agenti/*.md; do n="$(basename "$f" .md)"; [ "$(sed -n 's/^name: *//p' "$f" | head -1)" = "$n" ]; esito $? "C. agente $n valido"; done
[ -x skills/impeccable/scripts/bin/darwin-arm64/impeccable ]; esito $? "C. motore Impeccable incluso ed eseguibile (macOS arm64)"

# D (eventuali scritture degli strumenti finiscono in una cartella temporanea, non nella cartella di lavoro reale)
T="$(cd "$(mktemp -d "${TMPDIR:-/tmp}/webdesigner-verifica.XXXXXX")" && pwd)"
node -e "const c=JSON.parse(require('fs').readFileSync('config/mobilitas.example.json','utf8'));c.lavoro.cartella='$T';require('fs').writeFileSync('$T/config.json',JSON.stringify(c))"
command -v node >/dev/null && [ "$(node -p 'process.versions.node.split(".")[0]')" -ge 18 ]; esito $? "D1. Node.js $(node -v 2>/dev/null)"
for c in npm python3 git rsync curl; do command -v $c >/dev/null; esito $? "D2. $c disponibile"; done
[ -d "/Applications/Google Chrome.app" ] || command -v google-chrome >/dev/null 2>&1; esito $? "D3. Google Chrome installato"
pv="$(node -p "require('./tools/playwright/node_modules/playwright-core/package.json').version" 2>/dev/null)"; [ -n "$pv" ]; esito $? "D4. Playwright locale: ${pv:-non installato (tools/setup/installa.sh)}"
sv="$(node -p "require('./tools/superdesign/node_modules/@superdesign/cli/package.json').version" 2>/dev/null)"; [ "$sv" = "0.14.0" ]; esito $? "D5. Superdesign CLI locale: ${sv:-non installata}"
if [ "$(uname -s)-$(uname -m)" = "Darwin-arm64" ]; then iv="$(MOBILITAS_CONFIG="$T/config.json" sh tools/impeccable.sh "$T" --version 2>/dev/null)"; [ -n "$iv" ]; esito $? "D6. Impeccable si avvia confinato: $iv"
else avviso "D6. piattaforma $(uname -s)-$(uname -m): serve IMPECCABLE_BIN"; fi
rm -rf "$T"

# E
sec="$(testo | xargs grep -n -I -E 'BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|sk-[A-Za-z0-9]{20,}|sk_live_[0-9A-Za-z]{10,}|ghp_[A-Za-z0-9]{30,}|xox[bap]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|"(access_?token|refresh_?token|api_?key|password|secret)" *: *"[^"]{8,}"' 2>/dev/null | grep -v '^./test/verifica-installazione.sh')"
[ -z "$sec" ]; esito $? "E1. nessuna chiave, token o password nei file"
envf="$(find . -path ./test/fixture -prune -o -path '*/node_modules' -prune -o \( -name '.env' -o -name '.env.*' -o -name '*.pem' -o -name '*.key' -o -name 'credentials*' \) -print)"
[ -z "$envf" ]; esito $? "E2. nessun file di credenziali${envf:+: $envf}"

# F
node tools/lib/config.cjs file >/dev/null 2>&1; esito $? "F1. configurazione leggibile ($(node tools/lib/config.cjs file 2>/dev/null))"
L="$(node tools/lib/config.cjs get lavoro.cartella)"; S="$(node tools/lib/config.cjs get sito.cartella)"
case "$L/" in "$ROOT"/*) esito 1 "F2. lavoro.cartella è dentro l'agente: va spostata";; *) [ -n "$S" ] && case "$L/" in "$S"/*) esito 1 "F2. lavoro.cartella è dentro il sito";; *) esito 0 "F2. cartella di lavoro fuori dall'agente e dal sito: $L";; esac || esito 0 "F2. cartella di lavoro fuori dall'agente: $L";; esac
[ -n "$S" ] && [ -f "$S/package.json" ] && echo "--   F3. sito collegato: $S" || avviso "F3. sito non collegato in configurazione: l'agente usa la cartella del sito aperta nel workspace (o --sito)"
[ "$(node tools/lib/config.cjs get integrazioni.superdesign.abilitato)" = "true" ] && echo "--   F4. Superdesign abilitato" || avviso "F4. Superdesign non abilitato"

# G
auto="$(find . -path '*/node_modules' -prune -o \( -name AGENTS.md -o -name CLAUDE.md -o -name CLAUDE.local.md -o -name .cursorrules -o -name .mcp.json -o -type d \( -name .cursor -o -name .claude -o -name .agents -o -name .codex -o -name .grok \) \) -print)"
[ -z "$auto" ]; esito $? "G1. nessun file caricato in automatico da Cursor o Claude Code (AGENTS.md, CLAUDE.md, .cursor, .claude, .agents, .mcp.json…)${auto:+: $auto}"
C1=templates/collegamento/comando/SKILL.md; C2=templates/collegamento/nominato/SKILL.md
grep -q '^disable-model-invocation: true' $C1 && grep -q '^name: webdesigner' $C1 && grep -q 'ISTRUZIONI.md' $C1; esito $? "G2. skill di richiamo «comando»: solo con /webdesigner (disable-model-invocation: true), rimanda a ISTRUZIONI.md"
! grep -q 'disable-model-invocation' $C2 && grep -q 'USARE SOLO quando' $C2 && grep -q '^name: webdesigner' $C2; esito $? "G3. variante «nominato»: invocabile dal modello solo quando il WebDesigner è nominato"
grep -q 'Solo quando l.utente ha \*\*attivato esplicitamente\*\*' ISTRUZIONI.md; esito $? "G4. ISTRUZIONI.md limita il sistema alle richieste con attivazione esplicita"

echo "Totale: $OK superati, $KO non superati, $AV avvisi"
[ "$KO" = 0 ]

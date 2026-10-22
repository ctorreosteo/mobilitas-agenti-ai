#!/bin/sh
# Installazione LOCALE dell'agente: nulla di globale, nulla fuori da questa cartella.
#   - Playwright (tools/playwright) e Superdesign CLI (tools/superdesign) con npm ci dalle versioni bloccate nei
#     package-lock; script di installazione dei pacchetti disattivati, nessun browser scaricato (si usa Chrome di sistema);
#   - cache npm in <lavoro>/.stato/npm-cache (non in ~/.npm, non nella cartella dell'agente);
#   - config/mobilitas.json creato dall'esempio, se manca.
# Scarica i pacchetti dal registro npm: è un accesso esterno, da fare con il consenso di chi installa.
# In alternativa, senza rete: installa.sh --cache-offline <cartella-cache-npm-esistente>
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
OFFLINE=""
[ "${1:-}" = "--cache-offline" ] && OFFLINE="${2:?cartella della cache}"

MANCA=0
ok() { printf '  ok   %s\n' "$1"; }
ko() { printf '  NO   %s\n' "$1"; MANCA=1; }
echo "Prerequisiti:"
if command -v node >/dev/null && [ "$(node -p 'process.versions.node.split(".")[0]')" -ge 18 ]; then ok "Node $(node -v)"; else ko "Node 18 o successivo"; fi
if command -v npm >/dev/null; then ok "npm $(npm -v)"; else ko "npm"; fi
for c in python3 git rsync curl; do if command -v $c >/dev/null; then ok "$c"; else ko "$c"; fi; done
if [ -d "/Applications/Google Chrome.app" ] || command -v google-chrome >/dev/null 2>&1; then ok "Google Chrome"; else ko "Google Chrome (serve ai test visivi)"; fi
if command -v sips >/dev/null; then ok "sips (ritagli foto)"; else echo "  --   sips assente: ritagli foto manuali"; fi
[ "$MANCA" = 0 ] || { echo "Mancano prerequisiti: installali e riprova." >&2; exit 3; }

export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 NO_UPDATE_NOTIFIER=1
for p in playwright superdesign; do
  echo "Pacchetti locali in tools/$p ..."
  if [ -n "$OFFLINE" ]; then
    npm ci --prefix "tools/$p" --ignore-scripts --no-audit --no-fund --offline --cache "$OFFLINE"
  else
    npm ci --prefix "tools/$p" --ignore-scripts --no-audit --no-fund --cache "$(node tools/lib/config.cjs stato npm-cache)"
  fi
done

if [ ! -f config/mobilitas.json ]; then
  cp config/mobilitas.example.json config/mobilitas.json
  echo "Creato config/mobilitas.json: compila i percorsi (README, sezione Configurazione)."
fi
chmod +x tools/*.sh tools/*/*.sh test/*.sh skills/impeccable/scripts/impeccable 2>/dev/null || true
echo "Fatto. Verifica con: test/verifica-installazione.sh"

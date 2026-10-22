#!/bin/sh
# Server Playwright MCP per le catture dei siti di riferimento (lanciato da cattura-riferimento.mjs, non dalle sessioni).
# - riusa playwright-core installato in tools/playwright (nessun download, nessun npx);
# - Chrome di sistema, headless, profilo isolato in memoria, service worker bloccati, file temporanei in <lavoro>/.stato/taste;
# - tutto il traffico passa dalla guardia dei riferimenti: rifiuta di partire se la guardia non risponde.
# Uso: avvia-mcp.sh <cartella-uscita>
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${1:?cartella di uscita}"
MCP="$ROOT/tools/playwright/node_modules/playwright-core/lib/entry/mcp.js"
[ -f "$MCP" ] || { echo "Playwright MCP non trovato: esegui tools/setup/installa.sh" >&2; exit 3; }
PG="$(node "$ROOT/tools/lib/config.cjs" get porte.guardia_riferimenti)"
curl -fsS --max-time 2 "http://127.0.0.1:$PG/__guard/health" >/dev/null 2>&1 || { echo "Guardia dei riferimenti non attiva su 127.0.0.1:$PG: avvio rifiutato (tools/taste/guardia.sh avvia)." >&2; exit 1; }
RT="$(node "$ROOT/tools/lib/config.cjs" stato taste)"
mkdir -p "$RT/tmp" "$RT/s" "$OUT"
# Configurazione del browser generata a ogni avvio dalla configurazione dell'agente.
node -e '
const { carica } = require(process.argv[1] + "/tools/lib/config.cjs");
const cfg = carica(); const port = process.argv[2];
const blocked = ["http://localhost:*", "http://127.0.0.1:*", "http://[::1]:*"];
// Primo livello nel browser (stesso formato già collaudato); i sottodomini li ferma comunque la guardia.
for (const d of cfg.domini_protetti || []) blocked.push("https://" + d, "https://www." + d);
const conf = { browser: { browserName: "chromium", isolated: true,
  launchOptions: { channel: "chrome", headless: true, proxy: { server: "http://127.0.0.1:" + port },
    args: ["--force-webrtc-ip-handling-policy=disable_non_proxied_udp", "--webrtc-ip-handling-policy=disable_non_proxied_udp", "--disable-quic"] },
  contextOptions: { viewport: { width: 1440, height: 900 }, serviceWorkers: "block" },
  initScript: [process.argv[1] + "/tools/taste/pagina-init.js"] },
  network: { blockedOrigins: blocked } };
require("fs").writeFileSync(process.argv[3], JSON.stringify(conf, null, 2));
' "$ROOT" "$PG" "$RT/mcp-browser.json"
cd "$RT"
export NO_UPDATE_NOTIFIER=1 TMPDIR="$RT/tmp" PLAYWRIGHT_BROWSERS_PATH="$RT/browsers"
# Relativo di proposito: il percorso assoluto può superare il limite dei socket Unix.
export PWTEST_SOCKETS_DIR="s"
exec node "$MCP" --config "$RT/mcp-browser.json" --output-dir "$OUT" --block-service-workers

#!/bin/sh
# Genera la configurazione Vite "di prova" dell'incarico, FUORI dal sito (in <incarico>/runtime/vite.prova.config.mjs).
# Eredita la configurazione del sito (plugin, alias, base) e cambia solo ciò che serve alla sicurezza delle prove:
#   - ascolto solo su 127.0.0.1 e porta fissa dell'incarico (il sito può essere configurato su 0.0.0.0);
#   - nessun proxy: in prova /api non raggiunge il gestionale (la guardia del browser lo nega comunque);
#   - cache di Vite nella cartella dell'incarico: nulla viene scritto nel sito;
#   - dipendenze analizzate tutte all'avvio (optimizeDeps.entries su tutto src/): niente ricaricamenti della pagina
#     a metà delle misure quando si visita un percorso nuovo.
# Il file viene riscritto solo se cambia (riscriverlo farebbe riavviare il server già acceso).
# Il codice delle landing e le loro integrazioni restano quelli reali del sito: cambia solo il server di prova.
# Uso: vite-prova.sh <cartella-incarico>   (stampa il percorso del file generato)
set -eu
INC="$(cd "${1:?uso: vite-prova.sh <cartella-incarico>}" && pwd)"
get() { node -e "console.log(require('$INC/incarico.json')['$1'])"; }
SITO="$(get sito)"; PD="$(get porta_sviluppo)"
BASE=""
for f in vite.config.js vite.config.mjs vite.config.ts vite.config.mts; do [ -f "$SITO/$f" ] && BASE="$SITO/$f" && break; done
OUT="$INC/runtime/vite.prova.config.mjs"; TMP="$OUT.nuovo"
mkdir -p "$INC/runtime"
if [ -n "$BASE" ]; then IMPORT="import base from '$BASE'"; else IMPORT="const base = {}"; fi
cat > "$TMP" <<EOF
// Generato da tools/sito/vite-prova.sh per l'incarico. Non modifica il sito: lo eredita e ne cambia solo il server di prova.
$IMPORT
const modo = process.argv.includes('build') ? 'build' : 'serve'
const b = typeof base === 'function' ? await base({ command: modo, mode: modo === 'build' ? 'production' : 'development' }) : base
export default {
  ...b,
  root: '$SITO',
  cacheDir: '$INC/runtime/vite-cache',
  server: { ...(b.server || {}), host: '127.0.0.1', port: $PD, strictPort: true, open: false, proxy: {} },
  optimizeDeps: { ...(b.optimizeDeps || {}), entries: ['index.html', 'src/**/*.{js,jsx,ts,tsx}'] },
}
EOF
if [ -f "$OUT" ] && cmp -s "$TMP" "$OUT"; then rm -f "$TMP"; else mv "$TMP" "$OUT"; fi
echo "$OUT"

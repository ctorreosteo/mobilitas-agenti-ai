#!/bin/sh
# Build di prova del sito con le modifiche dell'incarico, per verificare che compili come in produzione.
# L'uscita va in <incarico>/runtime/build (mai in dist/ del sito); nessun deploy.
# Uso: build-prova.sh <cartella-incarico>
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
INC="$(cd "${1:?uso: build-prova.sh <cartella-incarico>}" && pwd)"
SITO="$(node -e "console.log(require('$INC/incarico.json').sito)")"
[ -x "$SITO/node_modules/.bin/vite" ] || { echo "Nel sito mancano le dipendenze (node_modules)." >&2; exit 3; }
CONF="$(sh "$ROOT/tools/sito/vite-prova.sh" "$INC")"
cd "$SITO"
./node_modules/.bin/vite build --config "$CONF" --outDir "$INC/runtime/build" --emptyOutDir > "$INC/runtime/build.log" 2>&1 \
  && { echo "Build di prova riuscita: $INC/runtime/build"; tail -4 "$INC/runtime/build.log"; } \
  || { echo "Build di prova FALLITA: vedi $INC/runtime/build.log" >&2; tail -20 "$INC/runtime/build.log" >&2; exit 1; }

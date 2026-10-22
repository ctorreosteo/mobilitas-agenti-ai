#!/bin/sh
# OCR locale (Vision di macOS) di immagini, es. per trovare tra gli screenshot ufficiali le recensioni su un tema.
# Nessun servizio esterno: compila ocr.swift alla prima esecuzione in <lavoro>/.stato (serve swiftc, Xcode Command Line Tools).
# Stampa "file<TAB>testo" per ogni immagine. Uso: ocr.sh <immagine> [immagine ...]
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
BIN="$(node "$ROOT/tools/lib/config.cjs" stato)/ocr"
if [ ! -x "$BIN" ] || [ "$ROOT/tools/immagini/ocr.swift" -nt "$BIN" ]; then
  command -v swiftc >/dev/null || { echo "swiftc non disponibile: installa gli Xcode Command Line Tools (richiede autorizzazione)." >&2; exit 3; }
  swiftc -O "$ROOT/tools/immagini/ocr.swift" -o "$BIN"
fi
exec "$BIN" "$@"

#!/bin/sh
# Lanciatore confinato di Impeccable (skill in skills/impeccable).
# - lavora nella cartella del progetto indicata (il sito): Impeccable legge lì PRODUCT.md, DESIGN.md e .impeccable/;
# - cartella utente confinata in <lavoro>/.stato/impeccable-home: nulla nella HOME reale né nella cartella dell'agente;
# - telemetria spenta, controllo aggiornamenti dirottato su una porta locale chiusa;
# - motore: il binario incluso (macOS arm64). Su altre piattaforme il lanciatore della skill lo scaricherebbe da
#   GitHub: è un accesso esterno, quindi qui ci si ferma, a meno che IMPECCABLE_BIN indichi un motore già installato.
# Uso: tools/impeccable.sh <cartella-progetto> <comando> [opzioni]
#   es. tools/impeccable.sh <sito> context --target src/pages/ReflussoV2.jsx
#       tools/impeccable.sh <sito> detect --json src/pages/ReflussoV2.jsx
#       tools/impeccable.sh <sito> embed-prompt public/reflusso-v2/a.jpg --prompt "Foto reale dello studio, ritaglio di ..."
set -eu
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROG="$(cd "${1:?uso: impeccable.sh <cartella-progetto> <comando> [opzioni]}" && pwd)"; shift
SKILL="$ROOT/skills/impeccable"
case "$(uname -s)-$(uname -m)" in
  Darwin-arm64) ;;
  *) echo "impeccable.sh: motore incluso solo per macOS arm64. Su questa piattaforma serve il download da GitHub: chiedi l'autorizzazione e imposta IMPECCABLE_BIN." >&2
     [ -n "${IMPECCABLE_BIN:-}" ] || exit 3 ;;
esac
IH="$(node "$ROOT/tools/lib/config.cjs" stato impeccable-home)"
cd "$PROG"
export HOME="$IH" IMPECCABLE_HOME="$IH/.impeccable" \
       IMPECCABLE_NO_TELEMETRY=1 DO_NOT_TRACK=1 IMPECCABLE_UPDATE_HOST=http://127.0.0.1:9 \
       IMPECCABLE_SKILL_DIR="$SKILL"
exec "$SKILL/scripts/impeccable" "$@"

#!/bin/sh
# Lanciatore di Superdesign CLI (installato in locale in tools/superdesign/node_modules).
# - credenziali e configurazione in <lavoro>/.stato/superdesign (mai nella cartella dell'agente);
# - telemetria spenta;
# - comandi gratuiti sempre consentiti; i comandi che possono consumare crediti partono SOLO se:
#     1. integrazioni.superdesign.abilitato = true in config/mobilitas.json, e
#     2. la variabile SD_TETTO_CREDITI contiene il tetto autorizzato dal titolare per questa richiesta.
#   Ogni comando a pagamento viene registrato in <lavoro>/.stato/superdesign-registro.log.
# - "init" è sempre vietato: installerebbe file di configurazione nel progetto.
# Uso: tools/superdesign/sd.sh <comando> [opzioni]
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CFG="node $ROOT/tools/lib/config.cjs"
BIN="$ROOT/tools/superdesign/node_modules/.bin/superdesign"
[ -x "$BIN" ] || { echo "Superdesign non installato: esegui tools/setup/installa.sh" >&2; exit 3; }
CRED="$($CFG stato superdesign)"; chmod 700 "$CRED"
REG="$($CFG stato)/superdesign-registro.log"
export SUPERDESIGN_CONFIG_DIR="$CRED" DO_NOT_TRACK=1 SUPERDESIGN_TELEMETRY_DISABLED=1 NO_UPDATE_NOTIFIER=1

CMD="${1:-}"
case "$CMD" in
  ""|-V|--version|-h|--help|help|login|logout|create-project|fetch-design-nodes|get-design|list-models|search-prompts|get-prompts|revert-design-draft)
    exec "$BIN" "$@" ;;
  init)
    echo "sd.sh: 'init' non è consentito (scriverebbe file di configurazione nel progetto)." >&2; exit 5 ;;
esac

# Da qui: comandi che possono consumare crediti.
[ "$($CFG get integrazioni.superdesign.abilitato)" = "true" ] || { echo "sd.sh: Superdesign non abilitato (integrazioni.superdesign.abilitato in config/mobilitas.json)." >&2; exit 6; }
case "${SD_TETTO_CREDITI:-}" in
  ''|*[!0-9]*) echo "sd.sh: '$CMD' può consumare crediti. Serve l'autorizzazione del titolare: SD_TETTO_CREDITI=<tetto> tools/superdesign/sd.sh $CMD ..." >&2; exit 7 ;;
esac
printf '%s\t%s\ttetto=%s\t%s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$CMD" "$SD_TETTO_CREDITI" "$(pwd)" >> "$REG"
exec "$BIN" "$@"

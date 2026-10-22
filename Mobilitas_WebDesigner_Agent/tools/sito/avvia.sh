#!/bin/sh
# Avvia in prova il sito ufficiale per un incarico, tutto su 127.0.0.1:
#   - server di sviluppo del sito con la configurazione di prova (tools/sito/vite-prova.sh): nessun proxy verso il
#     gestionale, cache fuori dal sito;
#   - guardia di rete per il browser automatico: consente solo il server di prova, solo GET/HEAD, mai /api/;
#   - con --visore, server statico delle bozze (cartella visore/ dell'incarico).
# Log e pid nella cartella dell'incarico. Non installa nulla: servono le dipendenze già presenti nel sito.
# Uso: avvia.sh <cartella-incarico> [--visore]
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
INC="$(cd "${1:?uso: avvia.sh <cartella-incarico> [--visore]}" && pwd)"
VISORE="${2:-}"
get() { node -e "console.log(require('$INC/incarico.json')['$1'])"; }
SITO="$(get sito)"; PD="$(get porta_sviluppo)"; PG="$(get porta_guardia)"; PV="$(get porta_visore)"
R="$INC/runtime"; mkdir -p "$R"
attivo() { curl -fsS --max-time 1 "$1" >/dev/null 2>&1; }

if attivo "http://127.0.0.1:$PD/"; then echo "Server di prova già attivo su $PD"
else
  [ -x "$SITO/node_modules/.bin/vite" ] || { echo "Nel sito mancano le dipendenze (node_modules): installarle è un'operazione sul sito, chiedi l'autorizzazione." >&2; exit 3; }
  CONF="$(sh "$ROOT/tools/sito/vite-prova.sh" "$INC")"
  (cd "$SITO" && nohup ./node_modules/.bin/vite --config "$CONF" > "$R/sviluppo.log" 2>&1 & echo $! > "$R/sviluppo.pid")
fi
if attivo "http://127.0.0.1:$PG/__guard/health"; then echo "Guardia già attiva su $PG"
else
  nohup node "$ROOT/tools/playwright/guardia-locale.mjs" --porta "$PG" --consenti "localhost:$PD,127.0.0.1:$PD" --log "$R/guardia.log" > "$R/guardia.out" 2>&1 &
  echo $! > "$R/guardia.pid"
fi
if [ "$VISORE" = "--visore" ] && ! attivo "http://127.0.0.1:$PV/"; then
  nohup python3 -I -m http.server "$PV" --bind 127.0.0.1 -d "$INC/visore" > "$R/visore.log" 2>&1 &
  echo $! > "$R/visore.pid"
fi
i=0; while [ $i -lt 180 ]; do attivo "http://127.0.0.1:$PD/" && attivo "http://127.0.0.1:$PG/__guard/health" && break; sleep 0.5; i=$((i+1)); done
attivo "http://127.0.0.1:$PD/" && echo "Sito in prova: http://localhost:$PD/<percorso-della-landing>" || { echo "Il server di prova non risponde: vedi $R/sviluppo.log" >&2; exit 1; }
attivo "http://127.0.0.1:$PG/__guard/health" && echo "Guardia:       127.0.0.1:$PG (solo localhost:$PD, sola lettura, /api negato)" || { echo "Guardia non attiva: vedi $R/guardia.out" >&2; exit 1; }
[ "$VISORE" = "--visore" ] && echo "Visore bozze:  http://127.0.0.1:$PV/"
exit 0

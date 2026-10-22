#!/bin/sh
# Avvia o ferma la guardia dei riferimenti in background. Uso: guardia.sh avvia [--test] | ferma | stato
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PG="$(node "$ROOT/tools/lib/config.cjs" get porte.guardia_riferimenti)"
ST="$(node "$ROOT/tools/lib/config.cjs" stato taste)"
PID="$ST/guardia.pid"
stato() { curl -fsS --max-time 1 "http://127.0.0.1:$PG/__guard/health" 2>/dev/null; }
case "${1:-stato}" in
  avvia)
    if stato >/dev/null; then echo "Guardia già attiva: $(stato)"; exit 0; fi
    nohup node "$ROOT/tools/taste/guardia-riferimenti.mjs" ${2:-} >> "$ST/guardia.out" 2>&1 &
    echo $! > "$PID"
    for i in 1 2 3 4 5 6 7 8 9 10; do stato >/dev/null && break; sleep 0.3; done
    stato && echo || { echo "Guardia non partita: vedi $ST/guardia.out" >&2; exit 1; } ;;
  ferma)
    [ -f "$PID" ] && kill "$(cat "$PID")" 2>/dev/null && rm -f "$PID" && echo "Guardia fermata." || echo "Guardia non attiva." ;;
  *) stato && echo || echo "Guardia non attiva su $PG." ;;
esac

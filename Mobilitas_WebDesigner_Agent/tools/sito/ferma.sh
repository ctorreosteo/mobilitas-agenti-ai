#!/bin/sh
# Ferma i servizi avviati da avvia.sh per un incarico (solo i processi registrati nei suoi file .pid).
# Uso: ferma.sh <cartella-incarico>
set -u
INC="$(cd "${1:?uso: ferma.sh <cartella-incarico>}" && pwd)"
for s in sviluppo guardia visore; do
  f="$INC/runtime/$s.pid"
  if [ -f "$f" ] && kill "$(cat "$f")" 2>/dev/null; then echo "$s fermato"; else echo "$s non attivo"; fi
  rm -f "$f"
done

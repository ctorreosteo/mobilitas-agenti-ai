#!/bin/sh
# Rende la cartella dell'agente di SOLA LETTURA sul disco (o la riapre), come protezione in più rispetto alle istruzioni:
# un editor o un agente che provasse a modificarne i file riceverebbe un errore di permessi.
#   on     toglie il permesso di scrittura a tutti i file e le cartelle dell'agente (dipendenze installate comprese)
#   off    lo ripristina per il proprietario (serve per aggiornare il pacchetto, reinstallare, cambiare la configurazione)
#   stato  dice se la cartella è protetta
# Non riguarda la cartella di lavoro né il sito. Uso: tools/setup/proteggi.sh on|off|stato
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
case "${1:-stato}" in
  on)  chmod -R a-w "$ROOT"; echo "Cartella dell'agente in sola lettura: $ROOT" ;;
  off) chmod -R u+w "$ROOT"; echo "Cartella dell'agente di nuovo modificabile dal proprietario: $ROOT" ;;
  stato)
    n="$(find "$ROOT" -perm -u+w 2>/dev/null | wc -l | tr -d ' ')"
    [ "$n" = 0 ] && echo "Protetta: nessun file scrivibile." || echo "Non protetta: $n elementi scrivibili (tools/setup/proteggi.sh on per proteggerla)." ;;
  *) echo "uso: proteggi.sh on|off|stato" >&2; exit 2 ;;
esac

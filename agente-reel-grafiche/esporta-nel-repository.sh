#!/bin/bash
# Copia l'agente reel-grafiche nel repository condiviso con Carlos (~/mobilitas-agenti-ai/agente-reel-grafiche).
#
#   ./esporta-nel-repository.sh          esporta l'ultimo commit di questa cartella nel repository condiviso
#   ./esporta-nel-repository.sh --prova  stessa esportazione in .lavoro/esporta/, senza toccare il repository condiviso
#
# Esporta solo i file dell'ultimo commit (git archive HEAD): niente .git, niente video, niente di quello che il
# .gitignore esclude. Non fa mai commit, push o pull: quelli si fanno a mano con Fork.

set -euo pipefail

NOME="agente-reel-grafiche"
REPO="$HOME/mobilitas-agenti-ai"
DEST="$REPO/$NOME"

ferma() { echo; echo "FERMO: $*" >&2; exit 1; }

PROVA=0
case "${1:-}" in
  "") ;;
  --prova) PROVA=1 ;;
  -h|--help) sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
  *) ferma "opzione sconosciuta «$1». Si usa senza opzioni oppure con --prova." ;;
esac

# --- questa cartella: deve essere la radice di un repository git con almeno un commit ---
QUI="$(cd "$(dirname "$0")" && pwd -P)"
cd "$QUI"
RADICE="$(git rev-parse --show-toplevel 2>/dev/null || true)"
[ -n "$RADICE" ] && [ "$(cd "$RADICE" && pwd -P)" = "$QUI" ] \
  || ferma "lo script va lanciato dalla cartella 03 dell'agente (la radice del suo repository git), non da una copia."
git rev-parse --verify --quiet HEAD >/dev/null || ferma "in questa cartella non c'è ancora nessun commit."
COMMIT="$(git log -1 --format='%h «%s» (%cd)' --date=format:'%d/%m/%Y %H:%M')"

# --- controlli prima dell'esportazione vera ---
if [ "$PROVA" -eq 0 ]; then
  [ -d "$REPO" ] || ferma "non trovo $REPO."
  REPO_RADICE="$(git -C "$REPO" rev-parse --show-toplevel 2>/dev/null || true)"
  [ -n "$REPO_RADICE" ] && [ "$(cd "$REPO_RADICE" && pwd -P)" = "$(cd "$REPO" && pwd -P)" ] \
    || ferma "$REPO non è un repository git."
  if [ -n "$(git status --porcelain)" ]; then
    echo "File con modifiche non ancora nel commit:" >&2
    git status --short | head -20 >&2 || true
    ferma "prima fai il commit della 03 in Fork"
  fi
fi

# --- esportazione in una cartella di appoggio dentro questa cartella (.lavoro è escluso dal .gitignore) ---
APPOGGIO="$QUI/.lavoro/esporta"
STAGE="$APPOGGIO/$NOME"
rm -rf -- "$STAGE"
mkdir -p "$STAGE"
git archive --format=tar HEAD | tar -x -C "$STAGE"

# --- controlli sulla copia, prima di toccare il repository condiviso ---
ATTESI="$(git ls-tree -r HEAD | wc -l | tr -d ' ')"
FILE="$(find "$STAGE" \( -type f -o -type l \) | wc -l | tr -d ' ')"
[ "$FILE" = "$ATTESI" ] || ferma "la copia ha $FILE file, l'ultimo commit ne ha $ATTESI."

VIDEO="$(find "$STAGE" -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' -o -iname '*.webm' \))"
if [ -n "$VIDEO" ]; then
  echo "$VIDEO" | sed "s|^$STAGE/|  |" >&2
  ferma "nell'ultimo commit ci sono dei video (sopra): non si esporta niente. Toglili dal commit e riprova."
fi
[ ! -e "$STAGE/.git" ] || ferma "nella copia c'è una cartella .git."

# file nel commit che il .gitignore della 03 escluderebbe: nel repository condiviso non arriverebbero
ESCLUSI="$(git ls-files -c -i --exclude-standard)"

# --- sostituzione della cartella nel repository condiviso ---
if [ "$PROVA" -eq 0 ]; then
  [ "$DEST" = "$HOME/mobilitas-agenti-ai/agente-reel-grafiche" ] || ferma "percorso di destinazione inatteso: $DEST"
  if [ -d "$DEST" ] && [ -n "$(git -C "$REPO" status --porcelain -- "$NOME")" ]; then
    echo "Attenzione: in $DEST c'erano modifiche non ancora nel commit del repository condiviso;"
    echo "vengono sostituite dalla copia della 03 (di solito è un'esportazione precedente non ancora pubblicata)."
  fi
  rm -rf -- "$DEST"
  mv "$STAGE" "$DEST"
  rmdir "$APPOGGIO" 2>/dev/null || true
  CARTELLA="$DEST"
  # file della copia che il repository condiviso ignorerebbe (per esempio per il suo .gitignore)
  IGNORATI="$(git -C "$REPO" status --porcelain --ignored -- "$NOME" | sed -n 's/^!! //p')"
else
  CARTELLA="$STAGE"
  IGNORATI=""
fi

# --- riepilogo ---
FILE="$(find "$CARTELLA" \( -type f -o -type l \) | wc -l | tr -d ' ')"
BYTE="$(find "$CARTELLA" -type f -exec stat -f %z {} + | awk '{s+=$1} END {print s+0}')"
DIM="$(awk -v b="$BYTE" 'BEGIN {printf "%.1f MB", b/1048576}') di contenuto ($(du -sh "$CARTELLA" | cut -f1 | tr -d ' ') su disco)"
VIDEO_DOPO="$(find "$CARTELLA" -type f \( -iname '*.mp4' -o -iname '*.mov' -o -iname '*.m4v' -o -iname '*.webm' \) | wc -l | tr -d ' ')"

echo
if [ "$PROVA" -eq 1 ]; then
  echo "PROVA (il repository condiviso non è stato toccato)"
fi
echo "Commit esportato: $COMMIT"
echo "Cartella:         $CARTELLA"
echo "File:             $FILE"
echo "Dimensione:       $DIM"
if [ "$VIDEO_DOPO" = "0" ]; then
  echo "Video:            nessun file .mp4, .mov, .m4v o .webm"
else
  ferma "nella cartella esportata ci sono $VIDEO_DOPO video."
fi
if [ -n "$ESCLUSI" ]; then
  echo
  echo "Attenzione: questi file sono nel commit ma il .gitignore li esclude (nel repository condiviso non arriverebbero):"
  echo "$ESCLUSI" | sed 's/^/  /'
fi
if [ -n "$IGNORATI" ]; then
  echo
  echo "Attenzione: il repository condiviso ignora questi file della copia (Fork non li mostrerà):"
  echo "$IGNORATI" | sed 's/^/  /'
fi
echo
if [ "$PROVA" -eq 1 ]; then
  echo "Era una prova: per esportare davvero lancia ./esporta-nel-repository.sh senza --prova."
else
  echo "Ora apri mobilitas-agenti-ai in Fork: Pull, Stage, Commit, Push"
fi

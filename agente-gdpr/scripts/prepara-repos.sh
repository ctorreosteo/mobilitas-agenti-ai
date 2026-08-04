#!/usr/bin/env bash
# Prepara i repository del gestionale per il lavoro dell'agente GDPR.
#
# NON clona e NON copia nulla: l'agente lavora direttamente nelle cartelle reali
# indicate in config/repos.json → "path". Questo script si limita a:
#   * verificare che i repo esistano e siano repository git;
#   * rifiutarsi di procedere se hai modifiche non committate (non le tocca mai);
#   * portare il repo sul branch di documentazione, ricordandoti da dove venivi;
#   * verificare che quel branch contenga SOLO modifiche a file .md.
#
# Non esegue fetch, pull, push, reset: il tuo repository resta sotto il tuo controllo.
#
# Uso:  ./scripts/prepara-repos.sh [nome-repo ...]
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$ROOT/config/repos.json"

command -v jq >/dev/null || { echo "❌ serve jq (brew install jq)"; exit 1; }
[ -f "$CONFIG" ] || { echo "❌ config non trovata: $CONFIG"; exit 1; }

BRANCH_LAVORO="$(jq -r '.branchLavoro' "$CONFIG")"
FILTRO=("$@")
ESITO=0

vuole() {
  [ ${#FILTRO[@]} -eq 0 ] && return 0
  local n="$1" f
  for f in "${FILTRO[@]}"; do [ "$f" = "$n" ] && return 0; done
  return 1
}

echo "▶ i repository vengono usati sul posto — branch di lavoro: $BRANCH_LAVORO"

while read -r repo; do
  NOME="$(jq -r '.nome'   <<<"$repo")"
  PATH_REPO="$(jq -r '.path'   <<<"$repo")"
  BRANCH="$(jq -r '.branch' <<<"$repo")"

  vuole "$NOME" || continue
  echo ""
  echo "═══ $NOME ═══"
  echo "→ $PATH_REPO"

  if [ ! -d "$PATH_REPO" ]; then
    echo "❌ cartella inesistente — correggi \"path\" in config/repos.json"
    ESITO=1; continue
  fi
  if ! git -C "$PATH_REPO" rev-parse --git-dir >/dev/null 2>&1; then
    echo "❌ non è un repository git: senza git non c'è modo di isolare né annullare le modifiche"
    ESITO=1; continue
  fi

  PARTENZA="$(git -C "$PATH_REPO" branch --show-current 2>/dev/null)"

  # Modifiche in corso: si segnalano, non si toccano. Cambiare branch qui sarebbe invasivo.
  if [ -n "$(git -C "$PATH_REPO" status --porcelain 2>/dev/null)" ]; then
    echo "⚠️  hai modifiche non committate su '$PARTENZA': NON tocco nulla."
    git -C "$PATH_REPO" status --short 2>/dev/null | head -20 | sed 's/^/     /'
    echo "   Committale o mettile da parte tu, poi rilancia /sync."
    echo "   L'agente non esegue né stash né reset sul tuo lavoro."
    ESITO=1; continue
  fi

  if [ "$PARTENZA" != "$BRANCH_LAVORO" ]; then
    if git -C "$PATH_REPO" rev-parse --verify --quiet "refs/heads/$BRANCH_LAVORO" >/dev/null; then
      git -C "$PATH_REPO" checkout --quiet "$BRANCH_LAVORO" || {
        echo "❌ non riesco a passare a $BRANCH_LAVORO"; ESITO=1; continue; }
      echo "→ passato a $BRANCH_LAVORO (esisteva già)"
    else
      if ! git -C "$PATH_REPO" rev-parse --verify --quiet "refs/heads/$BRANCH" >/dev/null; then
        echo "❌ branch base '$BRANCH' inesistente in questo repo"; ESITO=1; continue
      fi
      git -C "$PATH_REPO" checkout --quiet -b "$BRANCH_LAVORO" "$BRANCH" || {
        echo "❌ non riesco a creare $BRANCH_LAVORO"; ESITO=1; continue; }
      echo "→ creato $BRANCH_LAVORO a partire da $BRANCH"
    fi
    echo "   eri su '$PARTENZA' — per tornarci: git -C $PATH_REPO checkout $PARTENZA"
  fi

  # il branch di documentazione può contenere SOLO modifiche a file Markdown
  NON_MD="$(git -C "$PATH_REPO" diff --name-only "$BRANCH...$BRANCH_LAVORO" 2>/dev/null \
            | grep -viE '\.(md|markdown)$')"
  if [ -n "$NON_MD" ]; then
    echo "🚨 INCIDENTE: $BRANCH_LAVORO modifica file NON Markdown del gestionale:"
    printf '%s\n' "$NON_MD" | sed 's/^/     /'
    echo "   Ripristinali prima di proseguire:"
    echo "   git -C $PATH_REPO checkout $BRANCH -- <file>"
    ESITO=1
  fi

  AVANTI="$(git -C "$PATH_REPO" rev-list --count "$BRANCH..$BRANCH_LAVORO" 2>/dev/null || echo 0)"
  SHA="$(git -C "$PATH_REPO" rev-parse --short HEAD 2>/dev/null || echo '-')"
  MD=$(find "$PATH_REPO" -name '*.md' \
        -not -path '*/node_modules/*' -not -path '*/.git/*' \
        -not -path '*/target/*' -not -path '*/dist/*' -not -path '*/.venv/*' 2>/dev/null | wc -l | tr -d ' ')
  echo "✔ branch $(git -C "$PATH_REPO" branch --show-current) — HEAD $SHA — $MD file .md — $AVANTI commit di documentazione oltre $BRANCH"
done < <(jq -c '.repos[]' "$CONFIG")

echo ""
if [ "$ESITO" -eq 0 ]; then
  echo "✅ Repository pronti. Nessun push: pubblichi tu, quando il diff ti convince."
else
  echo "⚠️  Uscita con errori: rileggi i messaggi sopra prima di procedere con /audit."
fi
exit "$ESITO"

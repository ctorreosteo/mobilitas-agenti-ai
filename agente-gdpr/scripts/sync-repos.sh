#!/usr/bin/env bash
# Recupera backend e frontend del gestionale dentro workspace/.
# Non modifica mai i repository di origine e non esegue push.
#
# Modalità (config/repos.json → "mode"):
#   local-git   (default) git clone dal repo locale  → copia indipendente, con storia git
#   remote                git clone da GitHub        → richiede credenziali (SSH o gh auth)
#   local-copy            rsync della working tree   → include anche le modifiche non committate
#
# Uso:  ./scripts/sync-repos.sh [nome-repo ...]
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$ROOT/config/repos.json"
WS="$ROOT/workspace"

command -v jq >/dev/null || { echo "❌ serve jq (brew install jq)"; exit 1; }
[ -f "$CONFIG" ] || { echo "❌ config non trovata: $CONFIG"; exit 1; }

MODE="$(jq -r '.mode' "$CONFIG")"
BRANCH_LAVORO="$(jq -r '.branchLavoro' "$CONFIG")"
mkdir -p "$WS"

FILTRO=("$@")
ESITO=0

vuole() {
  [ ${#FILTRO[@]} -eq 0 ] && return 0
  local n="$1" f
  for f in "${FILTRO[@]}"; do [ "$f" = "$n" ] && return 0; done
  return 1
}

echo "▶ modalità: $MODE — branch di lavoro: $BRANCH_LAVORO"

while read -r repo; do
  NOME="$(jq -r '.nome'      <<<"$repo")"
  REMOTE="$(jq -r '.remote'  <<<"$repo")"
  BRANCH="$(jq -r '.branch'  <<<"$repo")"
  LOCALE="$(jq -r '.localPath' <<<"$repo")"
  DEST="$WS/$NOME"

  vuole "$NOME" || continue
  echo ""
  echo "═══ $NOME ═══"

  case "$MODE" in
    remote)
      SORGENTE="$REMOTE" ;;
    local-git|local-copy)
      SORGENTE="$LOCALE"
      if [ ! -d "$LOCALE" ]; then
        echo "❌ path locale assente: $LOCALE — salto (usa \"mode\":\"remote\" o correggi config)"
        ESITO=1; continue
      fi
      SPORCO="$(git -C "$LOCALE" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
      if [ "$MODE" = "local-git" ] && [ "${SPORCO:-0}" != "0" ]; then
        echo "ℹ️  il repo di origine ha $SPORCO file non committati: l'audit userà lo stato COMMITTATO."
        echo "   Per includere anche le modifiche in corso usa \"mode\": \"local-copy\"."
      fi
      ;;
    *)
      echo "❌ mode non valido: $MODE (attesi: local-git | remote | local-copy)"; exit 1 ;;
  esac

  if [ "$MODE" = "local-copy" ]; then
    echo "→ snapshot rsync da $LOCALE"
    mkdir -p "$DEST"
    rsync -a --delete \
      --exclude '.git' --exclude 'node_modules' --exclude 'target' \
      --exclude 'dist' --exclude '.venv' --exclude 'build' --exclude 'coverage' \
      "$LOCALE/" "$DEST/" || { echo "❌ rsync fallito"; ESITO=1; continue; }
    if [ ! -d "$DEST/.git" ]; then
      git -C "$DEST" init -q
      git -C "$DEST" add -A >/dev/null 2>&1
      git -C "$DEST" -c user.email=agente-gdpr@local -c user.name="agente-gdpr" \
        commit -qm "snapshot working tree $NOME" >/dev/null 2>&1
      git -C "$DEST" branch -M main >/dev/null 2>&1
    fi
  else
    if [ -d "$DEST/.git" ]; then
      echo "→ aggiorno la copia esistente da $SORGENTE"
      git -C "$DEST" fetch --quiet origin "$BRANCH" 2>/dev/null || {
        echo "❌ fetch fallito (credenziali o sorgente non raggiungibile)"; ESITO=1; continue; }
      git -C "$DEST" checkout --quiet "$BRANCH" 2>/dev/null
      git -C "$DEST" reset --hard --quiet "origin/$BRANCH"
    else
      echo "→ clone da $SORGENTE"
      rm -rf "$DEST"
      if ! git clone --quiet --branch "$BRANCH" "$SORGENTE" "$DEST" 2>&1 | sed 's/^/   /'; then
        echo "❌ clone fallito."
        [ "$MODE" = "remote" ] && echo "   Suggerimento: autenticati (gh auth login / chiave SSH) oppure usa \"mode\": \"local-git\"."
        ESITO=1; continue
      fi
    fi
  fi

  # branch di lavoro: qui finiranno SOLO le modifiche ai file .md
  if git -C "$DEST" rev-parse --verify --quiet "$BRANCH_LAVORO" >/dev/null; then
    git -C "$DEST" checkout --quiet "$BRANCH_LAVORO"
  else
    git -C "$DEST" checkout --quiet -b "$BRANCH_LAVORO"
  fi

  # nessun push accidentale dalla copia di lavoro
  git -C "$DEST" remote set-url --push origin PUSH_DISABILITATO_DALL_AGENTE_GDPR 2>/dev/null || true

  SHA="$(git -C "$DEST" rev-parse --short HEAD 2>/dev/null || echo '-')"
  MD=$(find "$DEST" -name '*.md' \
        -not -path '*/node_modules/*' -not -path '*/.git/*' \
        -not -path '*/target/*' -not -path '*/dist/*' -not -path '*/.venv/*' 2>/dev/null | wc -l | tr -d ' ')
  echo "✔ workspace/$NOME — branch $(git -C "$DEST" branch --show-current) — HEAD $SHA — $MD file .md"
done < <(jq -c '.repos[]' "$CONFIG")

echo ""
if [ "$ESITO" -eq 0 ]; then
  echo "✅ Sync completato. Push disabilitato sulle copie di lavoro."
else
  echo "⚠️  Sync completato con errori: rileggi i messaggi sopra prima di procedere con /audit."
fi
exit "$ESITO"

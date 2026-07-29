#!/usr/bin/env bash
# Recupera backend e frontend del gestionale dentro workspace/.
# Non modifica mai i repository di origine, non esegue push e non distrugge mai
# il lavoro già prodotto sul branch di documentazione.
#
# Modalità (config/repos.json → "mode"):
#   local-git   (default) git clone/fetch dal repo locale  → copia indipendente, con storia git
#   remote                git clone/fetch da GitHub        → richiede credenziali (SSH o gh auth)
#   local-copy            rsync della working tree         → include le modifiche non committate
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

case "$MODE" in
  local-git|remote|local-copy) ;;
  *) echo "❌ mode non valido: $MODE (attesi: local-git | remote | local-copy)"; exit 1 ;;
esac

mkdir -p "$WS"

FILTRO=("$@")
ESITO=0

# identità usata solo per i commit tecnici dentro workspace/ (snapshot e merge)
GIT_ID=(-c user.email=agente-gdpr@local -c user.name=agente-gdpr)

vuole() {
  [ ${#FILTRO[@]} -eq 0 ] && return 0
  local n="$1" f
  for f in "${FILTRO[@]}"; do [ "$f" = "$n" ] && return 0; done
  return 1
}

# Working tree senza modifiche non committate?
pulito() { [ -z "$(git -C "$1" status --porcelain 2>/dev/null)" ]; }

# Segnala le modifiche pendenti e rifiuta di procedere: non si cancella mai il lavoro altrui.
rifiuta_se_sporco() {  # $1=dest  $2=nome repo
  pulito "$1" && return 0
  echo "⚠️  workspace/$2 ha modifiche non committate: NON tocco nulla."
  git -C "$1" status --short 2>/dev/null | sed 's/^/     /'
  echo "   Committale sul branch di lavoro oppure scartale, poi rilancia /sync."
  return 1
}

# Porta la copia di lavoro sul branch di documentazione, creandolo se assente.
su_branch_lavoro() {  # $1=dest  $2=branch base
  if git -C "$1" rev-parse --verify --quiet "refs/heads/$BRANCH_LAVORO" >/dev/null; then
    git -C "$1" checkout --quiet "$BRANCH_LAVORO"
  else
    git -C "$1" checkout --quiet -b "$BRANCH_LAVORO" "$2"
  fi
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

  if [ "$MODE" = "remote" ]; then
    SORGENTE="$REMOTE"
  else
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
  fi

  # ───────────────────────────────────────────────────────────── local-copy ──
  if [ "$MODE" = "local-copy" ]; then
    if [ -d "$DEST/.git" ]; then
      # Ri-sincronizzazione: lo snapshot va aggiornato sul branch base e poi
      # portato sul branch di lavoro con un merge, così i .md prodotti restano.
      rifiuta_se_sporco "$DEST" "$NOME" || { ESITO=1; continue; }
      git -C "$DEST" checkout --quiet "$BRANCH" || {
        echo "❌ non riesco a tornare sul branch base $BRANCH"; ESITO=1; continue; }
    else
      if [ -e "$DEST" ]; then
        echo "⚠️  $DEST esiste ma non è un repository git: lo ricreo da zero."
        rm -rf "$DEST"
      fi
      mkdir -p "$DEST"
    fi

    echo "→ snapshot rsync da $LOCALE"
    rsync -a --delete \
      --exclude '.git' --exclude 'node_modules' --exclude 'target' \
      --exclude 'dist' --exclude '.venv' --exclude 'build' --exclude 'coverage' \
      "$LOCALE/" "$DEST/" || { echo "❌ rsync fallito"; ESITO=1; continue; }

    if [ ! -d "$DEST/.git" ]; then
      git -C "$DEST" init -q
      git -C "$DEST" checkout --quiet -b "$BRANCH" 2>/dev/null \
        || git -C "$DEST" branch -M "$BRANCH" >/dev/null 2>&1
    fi

    git -C "$DEST" add -A >/dev/null 2>&1
    if ! pulito "$DEST"; then
      git -C "$DEST" "${GIT_ID[@]}" commit -qm "snapshot working tree $NOME" >/dev/null 2>&1
    fi

    ESISTEVA=0
    git -C "$DEST" rev-parse --verify --quiet "refs/heads/$BRANCH_LAVORO" >/dev/null && ESISTEVA=1
    su_branch_lavoro "$DEST" "$BRANCH" || {
      echo "❌ non riesco a preparare il branch $BRANCH_LAVORO"; ESITO=1; continue; }

    # il branch di lavoro deve vedere il codice aggiornato senza perdere i .md già scritti
    if [ "$ESISTEVA" = "1" ]; then
      if ! git -C "$DEST" "${GIT_ID[@]}" merge --quiet --no-edit "$BRANCH" >/dev/null 2>&1; then
        git -C "$DEST" merge --abort >/dev/null 2>&1
        echo "❌ conflitto tra il nuovo snapshot e i .md già scritti su $BRANCH_LAVORO."
        echo "   Risolvilo a mano in workspace/$NOME, oppure elimina il branch per ripartire:"
        echo "   git -C workspace/$NOME branch -D $BRANCH_LAVORO"
        ESITO=1; continue
      fi
    fi

  # ─────────────────────────────────────────────────────── local-git/remote ──
  else
    if [ -d "$DEST/.git" ]; then
      echo "→ aggiorno la copia esistente da $SORGENTE"
      rifiuta_se_sporco "$DEST" "$NOME" || { ESITO=1; continue; }

      # Ci si sposta PRIMA sul branch di lavoro: così l'aggiornamento del branch
      # base avviene per sola scrittura di ref, senza reset del working tree e
      # senza alcuna possibilità di azzerare il lavoro già committato.
      su_branch_lavoro "$DEST" "$BRANCH" || {
        echo "❌ non riesco a preparare il branch $BRANCH_LAVORO"; ESITO=1; continue; }

      if ! git -C "$DEST" fetch --quiet origin \
             "+refs/heads/$BRANCH:refs/remotes/origin/$BRANCH" \
             "+refs/heads/$BRANCH:refs/heads/$BRANCH"; then
        echo "❌ fetch fallito (credenziali o sorgente non raggiungibile)"
        [ "$MODE" = "remote" ] && echo "   Suggerimento: gh auth login / chiave SSH, oppure \"mode\": \"local-git\"."
        ESITO=1; continue
      fi
    else
      if [ -e "$DEST" ]; then
        echo "⚠️  $DEST esiste ma non è un repository git: lo ricreo da zero."
      fi
      rm -rf "$DEST"
      echo "→ clone da $SORGENTE"
      if ! git clone --quiet --branch "$BRANCH" "$SORGENTE" "$DEST" 2>&1 | sed 's/^/   /'; then
        echo "❌ clone fallito."
        [ "$MODE" = "remote" ] && echo "   Suggerimento: autenticati (gh auth login / chiave SSH) oppure usa \"mode\": \"local-git\"."
        ESITO=1; continue
      fi
      su_branch_lavoro "$DEST" "$BRANCH" || {
        echo "❌ non riesco a preparare il branch $BRANCH_LAVORO"; ESITO=1; continue; }
    fi

    DIETRO="$(git -C "$DEST" rev-list --count "$BRANCH_LAVORO..$BRANCH" 2>/dev/null || echo 0)"
    if [ "${DIETRO:-0}" != "0" ]; then
      echo "ℹ️  $BRANCH_LAVORO è indietro di $DIETRO commit rispetto a $BRANCH (lavoro di una sessione precedente)."
      echo "   Per allinearlo senza perdere i .md: git -C workspace/$NOME rebase $BRANCH"
    fi
  fi

  # nessun push accidentale dalla copia di lavoro
  git -C "$DEST" remote set-url --push origin PUSH_DISABILITATO_DALL_AGENTE_GDPR 2>/dev/null || true

  # il branch di lavoro può contenere SOLO modifiche a file Markdown
  NON_MD="$(git -C "$DEST" diff --name-only "$BRANCH...$BRANCH_LAVORO" 2>/dev/null \
            | grep -viE '\.(md|markdown)$')"
  if [ -n "$NON_MD" ]; then
    echo "🚨 INCIDENTE: $BRANCH_LAVORO modifica file NON Markdown del gestionale:"
    printf '%s\n' "$NON_MD" | sed 's/^/     /'
    echo "   Ripristinali prima di proseguire: git -C workspace/$NOME checkout $BRANCH -- <file>"
    ESITO=1
  fi

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

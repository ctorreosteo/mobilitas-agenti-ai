#!/bin/sh
# Collega il WebDesigner a Cursor (o Claude Code) installando UNA skill di richiamo "webdesigner" nella radice di una
# cartella del workspace. Per impostazione predefinita NON scrive nulla: mostra dove andrebbe il file e il suo contenuto.
# Scrive solo con --scrivi (da usare quando il titolare lo autorizza).
#
#   --dove <cartella>        radice in cui installare: il sito, la cartella degli agenti aziendali, oppure ~ (personale)
#   --strumento cursor|claude    cursor → <dove>/.cursor/skills/webdesigner/ (predefinito)
#                                claude → <dove>/.claude/skills/webdesigner/ (letto da Claude Code e anche da Cursor)
#   --variante comando|nominato  comando  → si attiva solo con /webdesigner (predefinito, deterministico)
#                                nominato → anche quando il WebDesigner viene nominato a parole (decide il modello)
#   --percorso-assoluto      scrive nel file il percorso di questa cartella dell'agente (utile per un'installazione
#                            personale; da evitare se il file viene condiviso via Git con altri)
#   --scrivi                 esegue davvero l'installazione (rifiuta di sovrascrivere un file esistente)
# Uso: tools/setup/collega.sh --dove <cartella> [--strumento cursor|claude] [--variante comando|nominato] [--percorso-assoluto] [--scrivi]
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
DOVE=""; STR="cursor"; VAR="comando"; ASS=0; SCRIVI=0
while [ $# -gt 0 ]; do case "$1" in
  --dove) DOVE="$2"; shift 2;; --strumento) STR="$2"; shift 2;; --variante) VAR="$2"; shift 2;;
  --percorso-assoluto) ASS=1; shift;; --scrivi) SCRIVI=1; shift;; *) echo "argomento sconosciuto: $1" >&2; exit 2;; esac; done
[ -n "$DOVE" ] || { echo "Indica --dove <cartella radice del workspace>." >&2; exit 2; }
DOVE="$(cd "$DOVE" && pwd)"
case "$DOVE/" in "$ROOT"/*) echo "Non si installa dentro la cartella dell'agente: va nella radice di una cartella del workspace (sito, agenti aziendali o cartella personale)." >&2; exit 3;; esac
case "$STR" in cursor) SUB=".cursor/skills/webdesigner";; claude) SUB=".claude/skills/webdesigner";; *) echo "--strumento: cursor o claude" >&2; exit 2;; esac
case "$VAR" in comando|nominato) ;; *) echo "--variante: comando o nominato" >&2; exit 2;; esac
DEST="$DOVE/$SUB/SKILL.md"
if [ "$ASS" = 1 ]; then P="$ROOT"; else P=""; fi
CONTENUTO="$(sed "s#__CARTELLA_AGENTE__#${P:-(non indicato: cercala tra le cartelle del workspace)}#" "$ROOT/templates/collegamento/$VAR/SKILL.md")"

echo "Destinazione: $DEST"
echo "Variante: $VAR ($( [ "$VAR" = comando ] && echo 'solo con /webdesigner' || echo 'anche quando il WebDesigner è nominato'))"
[ "$STR" = claude ] && echo "Nota: Cursor legge anche .claude/skills (estensioni di terze parti attive). Non installare entrambe le varianti nella stessa radice."
if [ "$SCRIVI" = 0 ]; then
  echo "PROVA: nessun file scritto. Contenuto che verrebbe installato:"; echo "-----"; echo "$CONTENUTO"; echo "-----"
  echo "Per installare davvero: aggiungi --scrivi (solo con l'autorizzazione del titolare, se la destinazione è il sito)."
  exit 0
fi
[ -e "$DEST" ] && { echo "Esiste già $DEST: non lo sovrascrivo. Spostalo o rimuovilo a mano se vuoi reinstallare." >&2; exit 4; }
for v in .cursor/skills/webdesigner .claude/skills/webdesigner; do [ "$v" != "$SUB" ] && [ -e "$DOVE/$v" ] && echo "ATTENZIONE: esiste già $DOVE/$v: in Cursor avresti due skill webdesigner." >&2; done
mkdir -p "$DOVE/$SUB"
printf '%s\n' "$CONTENUTO" > "$DEST"
echo "Installato: $DEST"

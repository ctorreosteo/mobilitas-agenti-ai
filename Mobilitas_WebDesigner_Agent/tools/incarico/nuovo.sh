#!/bin/sh
# Apre un incarico: crea la cartella di lavoro FUORI dall'agente e fuori dal sito, assegna le porte locali
# e registra lo stato iniziale del sito (Git e impronte), che a fine lavoro serve a dimostrare cosa è cambiato.
# Il sito viene soltanto letto. Le landing si creano nel sito; qui vanno brief, bozze, screenshot e resoconti.
# Uso: nuovo.sh <nome-incarico> [--sito <cartella-del-sito>]      es. nuovo.sh reflusso-v2
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CFG="node $ROOT/tools/lib/config.cjs"
NOME="${1:-}"; shift || true
SITO=""
while [ $# -gt 0 ]; do case "$1" in --sito) SITO="$2"; shift 2;; *) echo "argomento sconosciuto: $1" >&2; exit 2;; esac; done
echo "$NOME" | grep -Eq '^[a-z0-9][a-z0-9-]{1,48}$' || { echo "Nome non valido: minuscole, cifre e trattini (es. reflusso-v2)." >&2; exit 2; }
[ -n "$SITO" ] || SITO="$($CFG get sito.cartella)"
[ -n "$SITO" ] || { echo "Sito non collegato: compila sito.cartella in config/mobilitas.json (oppure usa --sito)." >&2; exit 3; }
SITO="$(cd "$SITO" && pwd)"
[ -f "$SITO/package.json" ] || { echo "$SITO non sembra il progetto React del sito (manca package.json)." >&2; exit 3; }
case "$SITO/" in "$ROOT"/*) echo "Il sito non può stare dentro la cartella dell'agente." >&2; exit 3;; esac
LAVORO="$($CFG get lavoro.cartella)"
case "$LAVORO/" in "$ROOT"/*|"$SITO"/*) echo "lavoro.cartella non può stare dentro l'agente o dentro il sito." >&2; exit 3;; esac
DEST="$LAVORO/$(date +%Y-%m-%d)-$NOME"
[ -e "$DEST" ] && { echo "Esiste già: $DEST" >&2; exit 4; }
PD="$($CFG porta-libera porte.sviluppo)"; PG="$($CFG porta-libera porte.guardia)"; PV="$($CFG porta-libera porte.visore)"
mkdir -p "$DEST/brief" "$DEST/bozze" "$DEST/visore/foto" "$DEST/visore/recensioni" "$DEST/report/screenshot" "$DEST/scartate" "$DEST/runtime"
cp -R "$ROOT/tools/superdesign/visore/vendor" "$DEST/visore/vendor"
IMP="$(sh "$ROOT/tools/sito/impronta.sh" "$SITO")"
cat > "$DEST/incarico.json" <<EOF
{
  "nome": "$NOME",
  "creato": "$(date '+%Y-%m-%dT%H:%M:%S%z')",
  "sito": "$SITO",
  "impronta_sito_iniziale": "$IMP",
  "porta_sviluppo": $PD,
  "porta_guardia": $PG,
  "porta_visore": $PV
}
EOF
cp "$ROOT/templates/incarico/LEGGIMI.md" "$DEST/LEGGIMI.md"
node "$ROOT/tools/incarico/registro.cjs" inizio "$DEST"
echo "Incarico aperto: $DEST"
echo "  sito: $SITO (impronta iniziale $IMP)"
echo "  porte: sviluppo $PD · guardia $PG · visore $PV (solo 127.0.0.1)"

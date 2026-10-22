#!/bin/sh
# Ritagli e ridimensionamenti locali delle foto REALI (sips di macOS). Nessuna immagine generata.
# Legge da stdin una riga per ritaglio:
#   <nome> <file-sorgente-relativo> <altezza> <larghezza> <offsetY> <offsetX> <larghezze-finali separate da virgola>
# es.:  tempie-dettaglio bruxismo/bruxismo5.JPG 2625 2100 0 200 640,800,1000
# Scrive <nome>-<larghezza>.jpg (JPEG qualità 80) e stampa la riga di provenienza da salvare in _fonti.txt.
# Uso: ritagli.sh <cartella-foto-sorgente> <cartella-uscita> < elenco.txt
set -eu
SRC="${1:?uso: ritagli.sh <cartella-foto-sorgente> <cartella-uscita> < elenco.txt}"; OUT="${2:?cartella di uscita}"
command -v sips >/dev/null || { echo "sips non disponibile (serve macOS)." >&2; exit 3; }
mkdir -p "$OUT"; TMP="$(mktemp -d "${TMPDIR:-/tmp}/ritagli.XXXXXX")"
while read -r nome src h w y x larghezze; do
  case "$nome" in ''|\#*) continue;; esac
  # Ordine di sips: -c altezza larghezza --cropOffset Y X
  sips -s format jpeg -c "$h" "$w" --cropOffset "$y" "$x" "$SRC/$src" --out "$TMP/$nome.jpg" >/dev/null
  for lw in $(echo "$larghezze" | tr ',' ' '); do
    sips --resampleWidth "$lw" -s format jpeg -s formatOptions 80 "$TMP/$nome.jpg" --out "$OUT/$nome-$lw.jpg" >/dev/null
  done
  echo "$nome <= $src, ritaglio ${w}x${h} offset x=$x y=$y, larghezze $larghezze ($(date +%d/%m/%Y))"
done
rm -rf "$TMP"

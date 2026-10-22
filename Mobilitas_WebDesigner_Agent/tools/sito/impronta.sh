#!/bin/sh
# Impronta di una cartella: SHA-256 aggregato di tutti i file (prime 20 cifre), in ordine stabile.
# Serve a dimostrare che una cartella (sito ufficiale, landing precedenti) non è cambiata.
# Esclude sempre node_modules, .git, cache di Vite, dist e .DS_Store.
# Uso: impronta.sh <cartella> [sottocartella-da-escludere ...]   es. impronta.sh ~/sito lab
set -eu
DIR="${1:?uso: impronta.sh <cartella> [sottocartella-da-escludere ...]}"; shift
cd "$DIR"
ESCLUSE="./node_modules ./.git ./.vite ./.vite-lab ./dist"
for x in "$@"; do ESCLUSE="$ESCLUSE ./${x#./}"; done
set --
for p in $ESCLUSE; do [ $# -gt 0 ] && set -- "$@" -o; set -- "$@" -path "$p"; done
find . \( "$@" \) -prune -o -type f ! -name .DS_Store -print0 | sort -z | xargs -0 shasum -a 256 | shasum -a 256 | cut -c1-20

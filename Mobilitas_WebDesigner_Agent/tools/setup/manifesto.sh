#!/bin/sh
# Manifesto d'integrità: SHA-256 di ogni file del pacchetto (escluse le parti locali: config/mobilitas.json,
# node_modules, runtime/, laboratori/, test/risultati/, .DS_Store). Scrive test/MANIFESTO.sha256.
# Da rigenerare SOLO quando si modifica volutamente il pacchetto (nuova versione); la verifica è in test/verifica-installazione.sh.
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
find . \( -path ./runtime -o -path ./laboratori -o -path ./tools/playwright/node_modules -o -path ./tools/superdesign/node_modules -o -path ./test/risultati -o -path ./.git \) -prune \
  -o -type f ! -name .DS_Store ! -path ./config/mobilitas.json ! -path ./test/MANIFESTO.sha256 -print0 \
  | sort -z | xargs -0 shasum -a 256 > test/MANIFESTO.sha256
echo "test/MANIFESTO.sha256: $(wc -l < test/MANIFESTO.sha256 | tr -d ' ') file"

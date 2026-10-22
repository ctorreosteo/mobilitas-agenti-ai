#!/bin/sh
# Test d'integrazione con un sito React/Vite vero (il sito collegato o una sua copia), SENZA modificarlo:
#   - incarico in una cartella di lavoro temporanea; stato Git e impronta del sito registrati;
#   - sito avviato con la configurazione di prova (127.0.0.1, nessun proxy verso il gestionale, cache fuori dal sito);
#   - catture, misure e controlli funzionali su landing esistenti, con le integrazioni reali (popup di prenotazione)
#     ma con la protezione iniettata e la guardia: nessun dato inviato;
#   - build di prova con uscita nella cartella di lavoro;
#   - alla fine: stato Git, impronta e cache del sito invariati, cartella dell'agente invariata.
# Uso: test/test-sito-reale.sh <cartella-sito> [--percorsi /reflusso,/cervicalgia] [--ambito main]
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
SITO="${1:?uso: test-sito-reale.sh <cartella-sito> [--percorsi /a,/b] [--ambito selettore]}"; shift
SITO="$(cd "$SITO" && pwd)"; PERCORSI="/reflusso"; AMBITO="main"
while [ $# -gt 0 ]; do case "$1" in --percorsi) PERCORSI="$2"; shift 2;; --ambito) AMBITO="$2"; shift 2;; *) shift;; esac; done
[ -x "$SITO/node_modules/.bin/vite" ] || { echo "Il sito non ha le dipendenze installate: questo test non installa nulla." >&2; exit 2; }
BASE="$(cd "$(mktemp -d "${TMPDIR:-/tmp}/webdesigner-sito.XXXXXX")" && pwd)"
LOG="$BASE/esito.txt"; : > "$LOG"; OK=0; KO=0
esito() { if [ "$1" = 0 ]; then OK=$((OK+1)); echo "OK   $2" | tee -a "$LOG"; else KO=$((KO+1)); echo "NO   $2" | tee -a "$LOG"; fi; }
porta() { node -e "const n=require('net');const s=n.createServer().listen(0,'127.0.0.1',()=>{console.log(s.address().port);s.close()})"; }
echo "Test con sito reale — $(date '+%d/%m/%Y %H:%M') — $SITO — percorsi $PERCORSI" | tee -a "$LOG"
node -e "
const c=JSON.parse(require('fs').readFileSync('config/mobilitas.example.json','utf8'));
c.sito.cartella='$SITO'; c.lavoro.cartella='$BASE/lavoro';
c.porte={sviluppo:$(porta),guardia:$(porta),visore:$(porta),guardia_riferimenti:$(porta)};
require('fs').writeFileSync('$BASE/config.json', JSON.stringify(c,null,2));"
export MOBILITAS_CONFIG="$BASE/config.json"
IMP_AG0="$(sh tools/sito/impronta.sh "$ROOT")"
GIT0="$(git -C "$SITO" status --porcelain --untracked-files=all 2>/dev/null | shasum | cut -c1-12)"
VITECACHE0="$(ls -la "$SITO/node_modules/.vite" 2>/dev/null | shasum | cut -c1-12)"

sh tools/incarico/nuovo.sh integrazione > "$BASE/nuovo.out" 2>&1; esito $? "incarico aperto ($(grep -c 'già modificati' "$BASE/nuovo.out") avviso sui file già modificati da altri)"
INC="$(ls -d "$BASE"/lavoro/*-integrazione | head -1)"
sh tools/sito/avvia.sh "$INC" > "$BASE/avvia.out" 2>&1; r=$?
esito $r "sito avviato in prova: $(grep -o 'http://localhost:[0-9]*' "$BASE/avvia.out" | head -1) (solo 127.0.0.1)"
ascolto="$(lsof -nP -iTCP:"$(node -e "console.log(require('$INC/incarico.json').porta_sviluppo)")" -sTCP:LISTEN 2>/dev/null | awk 'NR>1{print $9}' | sort -u | tr '\n' ' ')"
echo "$ascolto" | grep -q '127.0.0.1' && ! echo "$ascolto" | grep -q '\*:'; esito $? "il server di prova ascolta solo in locale: $ascolto"
sleep 2
node tools/playwright/cattura.cjs --incarico "$INC" --percorso "$PERCORSI" --ambito "$AMBITO" > "$BASE/cattura.out" 2>&1; r=$?
err="$(node -e "const fs=require('fs');const d='$INC/report/screenshot';let n=0;for(const f of fs.readdirSync(d).filter(f=>f.endsWith('-misure.json'))){const r=JSON.parse(fs.readFileSync(d+'/'+f));for(const v of Object.values(r))if(v&&v.erroriJs)n+=v.erroriJs.length}console.log(n)")"
[ $r = 0 ] && [ "$err" = 0 ]; esito $? "le landing si aprono e si misurano a 1440/390/375 senza errori JS (errori: $err)"
sed -n '/DA CONTROLLARE/,/^http/p' "$BASE/cattura.out" | grep -v '^http' | head -12 | sed 's/^/     /' | tee -a "$LOG"
node tools/playwright/controlli.cjs --incarico "$INC" --percorso "$PERCORSI" --ambito "$AMBITO" > "$BASE/controlli.out" 2>&1
grep -E 'prenotazione|protezione' "$BASE/controlli.out" | sed 's/^/     /' | tee -a "$LOG"
scritture="$(node -e "const fs=require('fs');let n=0,ok=0,tot=0;for(const f of fs.readdirSync('$INC/report').filter(f=>f.startsWith('controlli-'))){const r=JSON.parse(fs.readFileSync('$INC/report/'+f));for(const k of ['1440x900','390x844']){const p=r[k].protezione;n+=p.scritturePartite.length;tot++;if(p.attiva)ok++}}console.log(n+' '+ok+'/'+tot)")"
[ "${scritture%% *}" = 0 ]; esito $? "nessuna scrittura partita dal browser, protezione attiva in ${scritture#* } viste (popup reale aperto e provato solo a campi vuoti)"
grep -q '"DENY"' "$INC/runtime/guardia.log" && ! grep '"ALLOW"' "$INC/runtime/guardia.log" | grep -q '/api/'; esito $? "guardia: richieste esterne negate ($(grep -c '"DENY"' "$INC/runtime/guardia.log")), nessun /api consentito"
sh tools/sito/build-prova.sh "$INC" > "$BASE/build.out" 2>&1; esito $? "build di prova riuscita con uscita nella cartella di lavoro (non in dist/ del sito)"
sh tools/sito/ferma.sh "$INC" > /dev/null 2>&1
node tools/incarico/registro.cjs verifica "$INC" > "$BASE/verifica.out" 2>&1; r=$?
grep -q "durante l'incarico (0)" "$BASE/verifica.out" && [ $r = 0 ]; esito $? "sito invariato secondo il registro: 0 file cambiati, file protetti intatti"
GIT1="$(git -C "$SITO" status --porcelain --untracked-files=all 2>/dev/null | shasum | cut -c1-12)"
VITECACHE1="$(ls -la "$SITO/node_modules/.vite" 2>/dev/null | shasum | cut -c1-12)"
IMP1="$(sh tools/sito/impronta.sh "$SITO")"; IMP0="$(node -e "console.log(require('$INC/incarico.json').impronta_sito_iniziale)")"
[ "$GIT0" = "$GIT1" ] && [ "$IMP0" = "$IMP1" ] && [ "$VITECACHE0" = "$VITECACHE1" ] && [ ! -e "$SITO/dist.prova" ]
esito $? "stato Git, impronta ($IMP1) e cache di Vite del sito invariati"
[ "$IMP_AG0" = "$(sh tools/sito/impronta.sh "$ROOT")" ]; esito $? "cartella dell'agente invariata"
echo "Totale: $OK superati, $KO non superati" | tee -a "$LOG"
echo "Esito e risultati: $BASE (catture in $INC/report/screenshot)"
[ "$KO" = 0 ]

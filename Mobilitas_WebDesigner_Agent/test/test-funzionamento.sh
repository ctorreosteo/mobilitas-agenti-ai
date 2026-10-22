#!/bin/sh
# Test di funzionamento dell'agente, tutti in locale: niente crediti Superdesign, niente accessi esterni, niente sito reale.
# Usa una configurazione temporanea: cartella di lavoro e sito finto in una cartella temporanea (fuori dall'agente).
#   0. la cartella dell'agente NON cambia durante le prove (impronta prima/dopo);
#   1–2. guardia dei riferimenti (politica offline e guardia attiva);
#   3. incarico: cartella di lavoro fuori dall'agente, stato Git del sito registrato; rifiuto di lavorare dentro l'agente;
#   4. dipendenze di una landing (route, esclusivi/condivisi, foto, integrazioni);
#   5. duplicazione simulata nel sito finto: originale preservato, modifiche elencate, file protetti sorvegliati;
#   6. catture, misure, controlli e prestazioni su una pagina statica, con protezione iniettata e guardia locale;
#   7. prova negativa: un «canarino» locale non riceve nulla; senza guardia gli script non partono;
#   8. configurazione Vite di prova: 127.0.0.1, nessun proxy, cache fuori dal sito;
#   9. Superdesign bloccato senza abilitazione e tetto; 10. Impeccable confinato; 11. ritagli e OCR;
#   12. skill di richiamo: prova a vuoto, installazione in una radice temporanea, rifiuti; 13. sola lettura sul disco.
# Uso: test/test-funzionamento.sh   (riepilogo anche in <lavoro di prova>/esito.txt, stampato a fine esecuzione)
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BASE="$(cd "$(mktemp -d "${TMPDIR:-/tmp}/webdesigner-prova.XXXXXX")" && pwd)"
LAVORO="$BASE/lavoro"; SITO="$BASE/sito"; mkdir -p "$LAVORO"
LOG="$BASE/esito.txt"; : > "$LOG"
OK=0; KO=0; PIDS=""
esito() { if [ "$1" = 0 ]; then OK=$((OK+1)); echo "OK   $2" | tee -a "$LOG"; else KO=$((KO+1)); echo "NO   $2" | tee -a "$LOG"; fi; }
fine() { for p in $PIDS; do kill "$p" 2>/dev/null; done; chmod -R u+w "$BASE" 2>/dev/null; }
trap fine EXIT INT TERM
porta() { node -e "const n=require('net');const s=n.createServer().listen(0,'127.0.0.1',()=>{console.log(s.address().port);s.close()})"; }
attendi() { i=0; while [ $i -lt 30 ]; do curl -fsS --max-time 1 "$1" >/dev/null 2>&1 && return 0; sleep 0.3; i=$((i+1)); done; return 1; }
echo "Test di funzionamento — $(date '+%d/%m/%Y %H:%M') — prove in $BASE" | tee -a "$LOG"
IMP_AGENTE_0="$(sh tools/sito/impronta.sh "$ROOT")"; FILE_AGENTE_0="$(find "$ROOT" -path "$ROOT/tools/*/node_modules" -prune -o -print | wc -l | tr -d ' ')"

# Sito finto come repository Git (temporaneo, con identità di prova solo per questo repository).
cp -R test/fixture/sito-prova "$SITO"
git -C "$SITO" init -q && git -C "$SITO" add -A && git -C "$SITO" -c user.name=prova -c user.email=prova@example.invalid commit -q -m "sito finto"
PR="$(porta)"
node -e "
const c=JSON.parse(require('fs').readFileSync('config/mobilitas.example.json','utf8'));
c.sito.cartella='$SITO'; c.lavoro.cartella='$LAVORO';
c.porte={sviluppo:$(porta),guardia:$(porta),visore:$(porta),guardia_riferimenti:$PR};
require('fs').writeFileSync('$BASE/config.json', JSON.stringify(c,null,2));"
export MOBILITAS_CONFIG="$BASE/config.json"

# 1–2
node test/test-politica-riferimenti.mjs > "$BASE/politica.txt" 2>&1; esito $? "1. politica della guardia dei riferimenti: $(tail -1 "$BASE/politica.txt")"
node tools/taste/guardia-riferimenti.mjs --test > "$BASE/guardia-rif.out" 2>&1 & PIDS="$PIDS $!"
if attendi "http://127.0.0.1:$PR/__guard/health"; then
  c1="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 -x "http://127.0.0.1:$PR" https://www.studiomobilitas.it/ 2>/dev/null)"
  c2="$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 -x "http://127.0.0.1:$PR" http://localhost:5173/ 2>/dev/null)"
  [ "$c1" != 200 ] && [ "$c2" = 403 ] && [ -f "$LAVORO/.stato/taste/guardia.log" ]; esito $? "2. guardia dei riferimenti: dominio protetto rifiutato ($c1), localhost negato ($c2), registro nello stato di lavoro"
else esito 1 "2. guardia dei riferimenti non partita"; fi

# 3
sh tools/incarico/nuovo.sh reflusso-v2 > "$BASE/nuovo.out" 2>&1; r=$?
INC="$(ls -d "$LAVORO"/*-reflusso-v2 2>/dev/null | head -1)"
[ $r = 0 ] && [ -f "$INC/incarico.json" ] && [ -f "$INC/runtime/registro.json" ] && [ -f "$INC/visore/vendor/tailwind-play.js" ]; esito $? "3a. incarico aperto fuori dall'agente: $(basename "${INC:-?}") con stato Git registrato"
node -e "const c=require('$BASE/config.json');c.lavoro.cartella='$ROOT/lavori-prova';require('fs').writeFileSync('$BASE/config-dentro.json',JSON.stringify(c))"
MOBILITAS_CONFIG="$BASE/config-dentro.json" sh tools/incarico/nuovo.sh dentro > "$BASE/dentro.out" 2>&1; r=$?
[ $r = 3 ] && [ ! -e "$ROOT/lavori-prova" ]; esito $? "3b. rifiutata una cartella di lavoro dentro l'agente (uscita $r)"

# 4
node tools/sito/dipendenze.mjs "$SITO" src/pages/Reflusso.jsx --json "$INC/brief/dipendenze.json" > "$BASE/dip.out" 2>&1
node -e "
const d=require('$INC/brief/dipendenze.json');
const ok=d.percorsi.includes('/reflusso') && d.dipendenze.some(x=>x.file.endsWith('reflusso/Sezione.jsx')&&x.tipo==='esclusivo')
 && d.risorsePublic.some(x=>x.percorso==='/reflusso/foto.jpg'&&x.esiste) && d.integrazioni.some(x=>/prenotazione/.test(x.tipo));
process.exit(ok?0:1)"; esito $? "4. dipendenze: route /reflusso, sezione esclusiva, popup di prenotazione riconosciuto, foto in public"

# 5 Duplicazione simulata: copia della pagina e della sezione esclusiva, una route in più.
node tools/incarico/registro.cjs preserva "$INC" src/pages/Reflusso.jsx src/pages/reflusso/Sezione.jsx > /dev/null
mkdir -p "$SITO/src/pages/reflusso-v2"
sed 's/Reflusso()/ReflussoV2()/; s#./reflusso/Sezione#./reflusso-v2/Sezione#' "$SITO/src/pages/Reflusso.jsx" > "$SITO/src/pages/ReflussoV2.jsx"
cp "$SITO/src/pages/reflusso/Sezione.jsx" "$SITO/src/pages/reflusso-v2/Sezione.jsx"
python3 -I - "$SITO/src/App.jsx" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
s=s.replace("import Reflusso from './pages/Reflusso'\n","import Reflusso from './pages/Reflusso'\nimport ReflussoV2 from './pages/ReflussoV2'\n")
s=s.replace('<Route path="/reflusso" element={<Layout hideWhatsApp><Reflusso /></Layout>} />','<Route path="/reflusso" element={<Layout hideWhatsApp><Reflusso /></Layout>} />\n        <Route path="/reflusso-v2" element={<Layout hideWhatsApp><ReflussoV2 /></Layout>} />')
open(p,'w').write(s)
PY
node tools/incarico/registro.cjs verifica "$INC" > "$BASE/verifica1.out" 2>&1; r=$?
[ $r = 0 ] && grep -q 'ReflussoV2.jsx' "$BASE/verifica1.out" && grep -q 'App.jsx' "$BASE/verifica1.out" && grep -q 'preservate (2 file invariati)' "$BASE/verifica1.out" && [ -f "$INC/report/modifiche.txt" ]
esito $? "5a. duplicazione: copia e route elencate, originale preservato, esito OK"
diff_r="$(git -C "$SITO" diff -U0 src/App.jsx | grep '^[-+][^-+]' | tr '\n' ' ')"
echo "$diff_r" | grep -q '^+import ReflussoV2' && ! echo "$diff_r" | grep -q '^-\|  -'; esito $? "5b. routing: solo aggiunte (import e route della copia)"
echo '// modifica non autorizzata' >> "$SITO/src/components/BookingPopup.jsx"
echo '// modifica all originale' >> "$SITO/src/pages/Reflusso.jsx"
node tools/incarico/registro.cjs verifica "$INC" > "$BASE/verifica2.out" 2>&1; r=$?
[ $r = 1 ] && grep -q 'File protetti MODIFICATI: src/components/BookingPopup.jsx' "$BASE/verifica2.out" && grep -q 'File da preservare MODIFICATI: src/pages/Reflusso.jsx' "$BASE/verifica2.out"
esito $? "5c. rilevate le modifiche vietate: popup di prenotazione (protetto) e landing originale"
grep -q '.env.local' "$INC/runtime/registro.json"; esito $? "5d. file .env.* del sito sorvegliati come protetti"

# 6–7 Pagina statica dietro la guardia, con protezione iniettata.
PS="$(porta)"; PG="$(porta)"; PC="$(porta)"
mkdir -p "$BASE/statico"; cp test/fixture/landing-prova/index.html "$BASE/statico/"
sed "s/__CANARINO__/$PC/g" test/fixture/landing-prova/negativa.html > "$BASE/statico/negativa.html"
python3 -I -m http.server "$PS" --bind 127.0.0.1 -d "$BASE/statico" > "$BASE/statico.log" 2>&1 & PIDS="$PIDS $!"
node tools/playwright/guardia-locale.mjs --porta "$PG" --consenti "localhost:$PS" --log "$BASE/guardia.log" --canarino "$PC" > "$BASE/guardia.out" 2>&1 & PIDS="$PIDS $!"
attendi "http://127.0.0.1:$PS/" && attendi "http://127.0.0.1:$PG/__guard/health"
U="http://localhost:$PS/index.html"
node tools/playwright/cattura.cjs --url "$U" --guardia "$PG" --uscita "$INC/report/screenshot" --prefisso prova > "$BASE/cattura.out" 2>&1; r=$?
n="$(ls "$INC/report/screenshot"/prova-*.png 2>/dev/null | wc -l | tr -d ' ')"
att="$(node -e "const r=require('$INC/report/screenshot/prova-misure.json');console.log(Object.values(r).filter(v=>v&&v.protezioneProva&&v.protezioneProva.attiva).length)" 2>/dev/null)"
[ $r = 0 ] && [ "$n" = 6 ] && [ "$att" = 3 ] && grep -q 'Nessun problema' "$BASE/cattura.out"; esito $? "6a. catture e misure a 1440/390/375: $n immagini, protezione di prova attiva in $att viste su 3, nessun problema"
node tools/playwright/controlli.cjs --url "$U" --guardia "$PG" --uscita "$INC/report" > "$BASE/controlli.out" 2>&1; r=$?
esito $r "6b. controlli funzionali: $(grep '^Totale' "$BASE/controlli.out")"
node tools/playwright/prestazioni.cjs --url "$U" --guardia "$PG" --uscita "$INC/report" > "$BASE/prest.out" 2>&1
[ "$(grep -c lcpMs "$BASE/prest.out")" = 4 ] && [ -f "$INC/report/prestazioni.json" ]; esito $? "6c. prestazioni: 4 misure, file nella cartella dell'incarico"
node tools/playwright/colonne.cjs "$INC/report/screenshot/prova-390x844-pagina-intera.png" "$INC/report/colonne.png" 3 300 >/dev/null 2>&1 \
 && node tools/playwright/confronto.cjs "$INC/report/confronto.png" 300 "A=$INC/report/screenshot/prova-390x844-prima-schermata.png" "B=$INC/report/screenshot/prova-375x667-prima-schermata.png" >/dev/null 2>&1
esito $? "6d. colonne e confronto affiancato"
node tools/playwright/cattura.cjs --url "http://localhost:$PS/negativa.html" --guardia "$PG" --uscita "$BASE/negativa" --prefisso negativa --viewport 390x844 > "$BASE/negativa.out" 2>&1
sleep 1
hits="$(cat "$BASE/guardia.log.canarino" 2>/dev/null | wc -l | tr -d ' ')"; negati="$(grep -c '"DENY"' "$BASE/guardia.log")"
bloccati="$(node -e "const r=require('$BASE/negativa/negativa-misure.json');console.log(r['negativa-390x844'].protezioneProva.bloccati.length)" 2>/dev/null)"
[ "$hits" = 0 ] && [ "$negati" -gt 0 ] && [ "${bloccati:-0}" -gt 0 ]; esito $? "7a. prova negativa: canarino raggiunto $hits volte; $bloccati tentativi fermati nel browser, $negati dalla guardia"
out="$(node tools/playwright/cattura.cjs --url "$U" --guardia "$(porta)" --uscita "$BASE/x" 2>&1)"; r=$?
[ $r != 0 ] && echo "$out" | grep -q 'avvio rifiutato'; esito $? "7b. senza guardia attiva gli script rifiutano di partire"
out="$(node tools/playwright/cattura.cjs --url "$U" --guardia "$PG" --viewport 390x844 2>&1)"
echo "$out" | grep -q "$LAVORO/.stato/prove"; esito $? "7c. senza incarico né --uscita, i risultati vanno nello stato di lavoro (non nell'agente)"

# 8
CONF="$(sh tools/sito/vite-prova.sh "$INC")"
grep -q "host: '127.0.0.1'" "$CONF" && grep -q 'proxy: {}' "$CONF" && grep -q "cacheDir: '$INC/runtime/vite-cache'" "$CONF" && case "$CONF" in "$INC"/*) true;; *) false;; esac
esito $? "8. configurazione Vite di prova nella cartella dell'incarico: 127.0.0.1, nessun proxy, cache fuori dal sito"

# 9
v="$(sh tools/superdesign/sd.sh --version 2>&1)"; [ "$v" = "0.14.0" ] && [ -d "$LAVORO/.stato/superdesign" ]; esito $? "9a. Superdesign locale $v, credenziali nello stato di lavoro"
sh tools/superdesign/sd.sh create-design-draft --project-id prova -p prova > /dev/null 2>&1; r1=$?
sh tools/superdesign/sd.sh init > /dev/null 2>&1; r2=$?
node -e "const c=require('$BASE/config.json');c.integrazioni.superdesign.abilitato=true;require('fs').writeFileSync('$BASE/config-sd.json',JSON.stringify(c))"
MOBILITAS_CONFIG="$BASE/config-sd.json" sh tools/superdesign/sd.sh create-design-draft --project-id prova -p prova > /dev/null 2>&1; r3=$?
[ $r1 = 6 ] && [ $r2 = 5 ] && [ $r3 = 7 ]; esito $? "9b. comandi a crediti bloccati (non abilitato: $r1; abilitato senza tetto: $r3), init vietato ($r2): nessuna chiamata al servizio"

# 10
iv="$(sh tools/impeccable.sh "$BASE/statico" --version 2>&1)"; r=$?
sh tools/impeccable.sh "$BASE/statico" detect --json index.html > "$BASE/detect.json" 2>/dev/null
[ $r = 0 ] && node -e "JSON.parse(require('fs').readFileSync('$BASE/detect.json','utf8'))" 2>/dev/null && [ -d "$LAVORO/.stato/impeccable-home" ]
esito $? "10. Impeccable $iv dalla nuova posizione (skills/), rilevatore funzionante, cartella utente nello stato di lavoro"

# 11
if command -v sips >/dev/null; then
  printf 'ritaglio-prova prova-1440x900-prima-schermata.png 400 800 0 0 320,640\n' | sh tools/immagini/ritagli.sh "$INC/report/screenshot" "$INC/scartate/ritagli" > "$BASE/ritagli.out" 2>&1
  [ -f "$INC/scartate/ritagli/ritaglio-prova-640.jpg" ]; esito $? "11a. ritagli delle foto (sips)"
fi
if command -v swiftc >/dev/null; then
  sh tools/immagini/ocr.sh "$INC/report/screenshot/prova-1440x900-prima-schermata.png" > "$BASE/ocr.out" 2>&1
  grep -q 'Prenota la prima visita' "$BASE/ocr.out" && [ -x "$LAVORO/.stato/ocr" ]; esito $? "11b. OCR locale, programma compilato nello stato di lavoro"
fi

# 12 Skill di richiamo
RADICE="$BASE/radice-workspace"; mkdir -p "$RADICE"
sh tools/setup/collega.sh --dove "$RADICE" > "$BASE/collega0.out" 2>&1
[ ! -e "$RADICE/.cursor" ] && grep -q 'PROVA: nessun file scritto' "$BASE/collega0.out"; esito $? "12a. collega.sh senza --scrivi: nessun file scritto"
sh tools/setup/collega.sh --dove "$RADICE" --scrivi > /dev/null 2>&1
S="$RADICE/.cursor/skills/webdesigner/SKILL.md"
[ -f "$S" ] && grep -q '^disable-model-invocation: true' "$S" && grep -q '^name: webdesigner' "$S" && ! grep -q '__CARTELLA_AGENTE__' "$S"
esito $? "12b. installata in una radice temporanea: .cursor/skills/webdesigner, disable-model-invocation: true"
sh tools/setup/collega.sh --dove "$RADICE" --scrivi > /dev/null 2>&1; r1=$?
sh tools/setup/collega.sh --dove "$ROOT/skills" --scrivi > /dev/null 2>&1; r2=$?
[ $r1 = 4 ] && [ $r2 = 3 ] && [ ! -e "$ROOT/skills/.cursor" ]; esito $? "12c. rifiuta di sovrascrivere ($r1) e di installare dentro l'agente ($r2)"
sh tools/setup/collega.sh --dove "$RADICE" --strumento claude --variante nominato --percorso-assoluto --scrivi > "$BASE/collega3.out" 2>&1
grep -q "$ROOT" "$RADICE/.claude/skills/webdesigner/SKILL.md" && ! grep -q 'disable-model-invocation' "$RADICE/.claude/skills/webdesigner/SKILL.md" && grep -q 'due skill webdesigner' "$BASE/collega3.out"
esito $? "12d. variante «nominato» per Claude Code con percorso assoluto, con avviso di doppione in Cursor"

# 13 Sola lettura sul disco (su una copia dell'agente)
COPIA="$BASE/copia-agente"; rsync -a --exclude node_modules "$ROOT/" "$COPIA/"
sh "$COPIA/tools/setup/proteggi.sh" on > /dev/null
( echo x >> "$COPIA/ISTRUZIONI.md" ) 2>/dev/null; w1=$?; ( touch "$COPIA/nuovo.txt" ) 2>/dev/null; w2=$?
st="$(sh "$COPIA/tools/setup/proteggi.sh" stato)"
sh "$COPIA/tools/setup/proteggi.sh" off > /dev/null; ( touch "$COPIA/nuovo.txt" ) 2>/dev/null; w3=$?
[ $w1 != 0 ] && [ $w2 != 0 ] && [ $w3 = 0 ] && echo "$st" | grep -q '^Protetta'; esito $? "13. proteggi.sh: con «on» modifiche e file nuovi rifiutati, con «off» di nuovo scrivibile (su una copia)"

# 0 Cartella dell'agente invariata
IMP_AGENTE_1="$(sh tools/sito/impronta.sh "$ROOT")"; FILE_AGENTE_1="$(find "$ROOT" -path "$ROOT/tools/*/node_modules" -prune -o -print | wc -l | tr -d ' ')"
[ "$IMP_AGENTE_0" = "$IMP_AGENTE_1" ] && [ "$FILE_AGENTE_0" = "$FILE_AGENTE_1" ]; esito $? "0. cartella dell'agente invariata dopo tutte le prove (impronta $IMP_AGENTE_0, $FILE_AGENTE_1 elementi)"

echo "Totale: $OK superati, $KO non superati" | tee -a "$LOG"
echo "Esito completo: $LOG"
[ "$KO" = 0 ]

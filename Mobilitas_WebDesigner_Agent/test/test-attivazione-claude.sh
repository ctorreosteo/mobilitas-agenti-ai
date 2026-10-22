#!/bin/sh
# Test dell'attivazione esplicita in Claude Code, in sessioni pulite (solo impostazioni di progetto, strumenti in sola lettura):
# crea un workspace temporaneo con un sito finto e la skill di richiamo installata (variante «comando»), poi:
#   A. richiesta su una landing SENZA nominare il WebDesigner  → il sistema non deve attivarsi (ISTRUZIONI.md non letto);
#   B. «/webdesigner …»                                         → deve leggere ISTRUZIONI.md e scegliere il workflow giusto;
#   C. «Usa l'agente WebDesigner …» senza comando               → informativo: con la variante «comando» non è garantito.
# Verifica anche che le skill interne del pacchetto (impeccable, taste…) NON siano registrate nella sessione.
# Consuma una piccola quantità di utilizzo di Claude (tre sessioni brevi): parte solo con --esegui. Nessun file modificato.
# Uso: test/test-attivazione-claude.sh --esegui [--modello sonnet]
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
[ "${1:-}" = "--esegui" ] || { echo "Avvia tre brevi sessioni di Claude Code (consuma utilizzo). Per eseguirlo: test/test-attivazione-claude.sh --esegui"; exit 2; }
MODELLO="sonnet"; [ "${2:-}" = "--modello" ] && MODELLO="${3:-sonnet}"
command -v claude >/dev/null || { echo "Comando claude non trovato." >&2; exit 3; }
BASE="$(cd "$(mktemp -d "${TMPDIR:-/tmp}/webdesigner-attivazione.XXXXXX")" && pwd)"
SITO="$BASE/sito"; cp -R "$ROOT/test/fixture/sito-prova" "$SITO"
sh "$ROOT/tools/setup/collega.sh" --dove "$SITO" --strumento claude --percorso-assoluto --scrivi > /dev/null
IMP0="$(sh "$ROOT/tools/sito/impronta.sh" "$ROOT")"
sessione() { # $1 nome, $2 richiesta
  ( cd "$SITO" && claude -p "$2" --setting-sources project --model "$MODELLO" --max-turns 10 --add-dir "$ROOT" \
      --allowedTools "Read Glob Grep" --disallowedTools "Bash Write Edit NotebookEdit WebFetch WebSearch" \
      --output-format stream-json --verbose ) > "$BASE/$1.jsonl" 2> "$BASE/$1.err"
}
sessione A "Migliora la landing del reflusso (src/pages/Reflusso.jsx): proponi un titolo più incisivo. Non modificare file e non eseguire comandi: rispondi solo con il titolo proposto e una riga di motivazione."
sessione B "/webdesigner migliora la landing del reflusso. Non modificare nulla e non eseguire comandi: dimmi solo quale workflow del pacchetto useresti (nome del file) e cosa mi chiederesti prima di iniziare."
sessione C "Usa l'agente WebDesigner per migliorare la landing del reflusso. Non modificare nulla e non eseguire comandi: dimmi solo quale workflow useresti e cosa mi chiederesti."
node - "$BASE" "$ROOT" <<'JS'
const fs = require('fs');
const [base, root] = process.argv.slice(2);
const leggi = n => fs.readFileSync(`${base}/${n}.jsonl`, 'utf8').split('\n').filter(Boolean).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
const analisi = n => {
  const r = leggi(n);
  const init = r.find(x => x.type === 'system' && x.subtype === 'init') || {};
  const letture = r.filter(x => x.type === 'assistant').flatMap(x => (x.message?.content || []).filter(c => c.type === 'tool_use')).map(c => `${c.name} ${c.input?.file_path || c.input?.pattern || c.input?.path || ''}`);
  const fine = [...r].reverse().find(x => x.type === 'result') || {};
  return { init, letture, testo: String(fine.result || ''), esito: fine.subtype, skill: init.skills || init.slash_commands || [] };
};
const A = analisi('A'), B = analisi('B'), C = analisi('C');
const lette = s => s.letture.some(l => l.includes('ISTRUZIONI.md'));
const controlli = [
  ['skill di richiamo «webdesigner» disponibile nella sessione', JSON.stringify(A.skill).includes('webdesigner')],
  ['skill interne del pacchetto NON registrate (impeccable, taste, emil-design-eng)', !/"(impeccable|taste|emil-design-eng)"/.test(JSON.stringify(A.skill))],
  ['A. senza comando: ISTRUZIONI.md non letto', !lette(A)],
  ['A. senza comando: nessun riferimento al WebDesigner nella risposta', !/webdesigner|ISTRUZIONI/i.test(A.testo)],
  ['B. con /webdesigner: ISTRUZIONI.md letto', lette(B)],
  ['B. con /webdesigner: workflow ottimizzazione scelto', /ottimizzazione/i.test(B.testo)],
];
let ok = 0; const out = [`Attivazione in Claude Code — ${new Date().toLocaleString('it-IT')} — modello ${A.init.model || '?'}, versione ${A.init.claude_code_version || '?'}`];
for (const [n, v] of controlli) { if (v) ok++; out.push(`${v ? 'OK  ' : 'NO  '} ${n}`); }
out.push(`--   C. «Usa l'agente WebDesigner…» senza comando (informativo): ISTRUZIONI.md ${lette(C) ? 'letto' : 'NON letto'}`);
out.push(`Totale: ${ok}/${controlli.length}`, '', '--- A (letture: ' + (A.letture.join('; ') || 'nessuna') + ')', A.testo, '', '--- B (letture: ' + (B.letture.join('; ') || 'nessuna') + ')', B.testo, '', '--- C (letture: ' + (C.letture.join('; ') || 'nessuna') + ')', C.testo);
fs.writeFileSync(`${base}/esito.txt`, out.join('\n') + '\n');
console.log(out.slice(0, controlli.length + 3).join('\n'));
process.exit(ok === controlli.length ? 0 : 1);
JS
r=$?
[ "$IMP0" = "$(sh "$ROOT/tools/sito/impronta.sh" "$ROOT")" ] && echo "OK   cartella dell'agente invariata" || { echo "NO   cartella dell'agente modificata"; r=1; }
echo "Dettagli e risposte complete: $BASE/esito.txt"
exit $r

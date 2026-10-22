#!/usr/bin/env node
// Dipendenze di una landing del sito (sola lettura), per duplicarla o modificarla senza rompere altro:
//   - albero degli import locali (componenti, sezioni, dati, stili) a partire dal file della pagina;
//   - per ognuno: ESCLUSIVO (usato solo da questa landing) o CONDIVISO (importato anche da altre parti del sito);
//   - risorse di public/ citate nel codice (foto, video, recensioni);
//   - righe del routing che montano la pagina (percorso attuale);
//   - integrazioni riconoscibili (popup di prenotazione, chiamate di rete, tracciamento, WhatsApp).
// Uso: node dipendenze.mjs <cartella-sito> <file-pagina-relativo> [--json <uscita.json>]
//      es. node dipendenze.mjs ~/sito src/pages/Reflusso.jsx --json <incarico>/brief/dipendenze-reflusso.json
import fs from 'node:fs';
import path from 'node:path';

const [sitoArg, paginaArg, ...resto] = process.argv.slice(2);
if (!sitoArg || !paginaArg) { console.error('uso: dipendenze.mjs <cartella-sito> <file-pagina> [--json uscita.json]'); process.exit(2); }
const SITO = path.resolve(sitoArg);
const SRC = path.join(SITO, 'src');
const jsonOut = resto[0] === '--json' ? resto[1] : null;
const EST = ['', '.jsx', '.js', '.tsx', '.ts', '.mjs', '/index.jsx', '/index.js', '/index.tsx', '/index.ts'];
const CODICE = /\.(jsx?|tsx?|mjs)$/;

const leggi = f => { try { return fs.readFileSync(f, 'utf8'); } catch { return ''; } };
function importDi(file) {
  const s = leggi(file);
  const out = new Set();
  for (const re of [/import\s+(?:[^'"]*?\s+from\s+)?['"]([^'"]+)['"]/g, /import\(\s*['"]([^'"]+)['"]\s*\)/g, /require\(\s*['"]([^'"]+)['"]\s*\)/g, /import\.meta\.glob\(\s*['"]([^'"]+)['"]/g]) {
    let m; while ((m = re.exec(s))) out.add(m[1]);
  }
  return [...out];
}
function risolvi(da, spec) {
  if (!spec.startsWith('.') && !spec.startsWith('/')) return null; // pacchetto npm
  if (spec.includes('*')) return null; // glob: segnalato a parte
  const base = spec.startsWith('/') ? path.join(SITO, spec) : path.resolve(path.dirname(da), spec);
  for (const e of EST) { const f = base + e; if (fs.existsSync(f) && fs.statSync(f).isFile()) return f; }
  return null;
}
function tuttiIFile(dir, acc = []) {
  for (const n of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, n.name);
    if (n.isDirectory()) tuttiIFile(p, acc); else if (CODICE.test(n.name) || n.name.endsWith('.css')) acc.push(p);
  }
  return acc;
}

const pagina = path.resolve(SITO, paginaArg);
if (!fs.existsSync(pagina)) { console.error('File della pagina non trovato: ' + pagina); process.exit(3); }
// Albero degli import locali della pagina.
const albero = new Map(); const pacchetti = new Set(); const glob = [];
(function visita(f) {
  if (albero.has(f)) return;
  albero.set(f, []);
  if (!CODICE.test(f)) return;
  for (const spec of importDi(f)) {
    if (spec.includes('*')) { glob.push({ da: path.relative(SITO, f), spec }); continue; }
    const r = risolvi(f, spec);
    if (r) { albero.get(f).push(r); visita(r); } else if (!spec.startsWith('.')) pacchetti.add(spec.split('/').slice(0, spec.startsWith('@') ? 2 : 1).join('/'));
  }
})(pagina);
// Chi importa cosa, in tutto src/ (per distinguere esclusivi e condivisi).
const importatori = new Map();
for (const f of tuttiIFile(SRC)) for (const spec of importDi(f)) {
  const r = risolvi(f, spec); if (!r) continue;
  if (!importatori.has(r)) importatori.set(r, new Set());
  importatori.get(r).add(f);
}
const dentro = new Set(albero.keys());
const voci = [...albero.keys()].filter(f => f !== pagina).map(f => {
  const fuori = [...(importatori.get(f) || [])].filter(i => !dentro.has(i));
  return { file: path.relative(SITO, f), tipo: fuori.length ? 'condiviso' : 'esclusivo', ancheIn: fuori.map(i => path.relative(SITO, i)).slice(0, 5) };
});
// Risorse di public/ citate nel codice dell'albero.
const risorse = new Set();
for (const f of dentro) {
  const s = leggi(f);
  let m; const re = /['"`(](\/[^'"`)\s]+\.(?:jpe?g|png|webp|avif|gif|svg|mp4|webm|mov|pdf|woff2?))['"`)]/gi;
  while ((m = re.exec(s))) risorse.add(m[1]);
}
const pub = path.join(SITO, 'public');
const elencoRisorse = [...risorse].sort().map(r => ({ percorso: r, esiste: fs.existsSync(path.join(pub, decodeURI(r))) }));
// Routing: righe che citano il componente della pagina.
const nomeComp = path.basename(pagina).replace(/\.(jsx?|tsx?)$/, '');
const routing = [];
for (const f of tuttiIFile(SRC).filter(f => CODICE.test(f))) {
  const righe = leggi(f).split('\n');
  righe.forEach((r, i) => {
    const route = /<Route\b/.test(r) && new RegExp(`<${nomeComp}\\b|\\{\\s*${nomeComp}\\s*\\}`).test(r);
    const imp = new RegExp(`import\\s+${nomeComp}\\b[^\\n]*from\\s+['"]`).test(r);
    if (route || imp) routing.push({ file: path.relative(SITO, f), riga: i + 1, percorso: route ? (r.match(/path=["'{`]+([^"'`}]+)/) || [])[1] || null : null, testo: r.trim().slice(0, 160) });
  });
}
// Integrazioni riconoscibili nell'albero.
const integrazioni = [];
const segni = [[/BookingPopup|Prenotazione|prenot/i, 'prenotazione (popup/modulo)'], [/fetch\(|axios|XMLHttpRequest/, 'chiamate di rete'], [/\bfbq\(|gtag\(|clarity\(|dataLayer/, 'tracciamento'], [/wa\.me|whatsapp/i, 'WhatsApp'], [/API_BASE|\/api\//, 'API del gestionale']];
for (const f of dentro) { const s = leggi(f); for (const [re, n] of segni) if (re.test(s)) integrazioni.push({ file: path.relative(SITO, f), tipo: n }); }

const percorsi = routing.map(r => r.percorso).filter(Boolean);
const out = { sito: SITO, pagina: path.relative(SITO, pagina), componente: nomeComp, percorsi, routing, dipendenze: voci, pacchetti: [...pacchetti].sort(), importGlob: glob, risorsePublic: elencoRisorse, integrazioni };
if (jsonOut) { fs.mkdirSync(path.dirname(path.resolve(jsonOut)), { recursive: true }); fs.writeFileSync(jsonOut, JSON.stringify(out, null, 2)); }
console.log(`Pagina: ${out.pagina} (componente ${nomeComp})`);
console.log(`Percorso: ${percorsi.join(', ') || 'non trovato'}`);
console.log(`Routing: ${routing.length ? routing.map(r => `${r.file}:${r.riga}  ${r.testo}`).join('\n         ') : 'nessuna riga trovata'}`);
console.log(`Dipendenze locali: ${voci.length} (${voci.filter(v => v.tipo === 'esclusivo').length} esclusive, ${voci.filter(v => v.tipo === 'condiviso').length} condivise)`);
for (const v of voci) console.log(`  ${v.tipo === 'esclusivo' ? 'ESCLUSIVA ' : 'condivisa '} ${v.file}${v.ancheIn.length ? '  (anche in ' + v.ancheIn.join(', ') + ')' : ''}`);
if (glob.length) console.log(`Import con glob (verificare a mano): ${glob.map(g => `${g.da}: ${g.spec}`).join('; ')}`);
console.log(`Risorse public citate: ${elencoRisorse.length}${elencoRisorse.some(r => !r.esiste) ? ' (alcune non trovate: ' + elencoRisorse.filter(r => !r.esiste).map(r => r.percorso).join(', ') + ')' : ''}`);
console.log(`Integrazioni: ${[...new Set(integrazioni.map(i => `${i.tipo} (${i.file})`))].join('; ') || 'nessuna riconosciuta'}`);
console.log(`Pacchetti npm usati: ${out.pacchetti.join(', ') || '—'}`);

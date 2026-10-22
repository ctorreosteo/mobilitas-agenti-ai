// Registro dello stato del sito per un incarico: serve a dimostrare cosa è cambiato nel sito durante il lavoro,
// che i file protetti non sono stati toccati e che la landing originale (in una duplicazione) è rimasta identica.
// Solo lettura sul sito: legge file e `git status`, non esegue mai comandi Git che modificano qualcosa.
//
//   node registro.cjs inizio <incarico>                 fotografia iniziale (stato Git, impronte dei file protetti e già modificati)
//   node registro.cjs preserva <incarico> <file...>     aggiunge file del sito da preservare (es. la landing originale e le sue dipendenze)
//   node registro.cjs verifica <incarico>               confronto con la fotografia: file cambiati, protetti, preservati → report/modifiche.txt
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');
const { carica, leggiIncarico } = require('../lib/config.cjs');

const [cmd, dir, ...resto] = process.argv.slice(2);
if (!cmd || !dir) { console.error('uso: registro.cjs inizio|preserva|verifica <cartella-incarico> [file...]'); process.exit(2); }
const inc = leggiIncarico(dir);
const SITO = inc.sito;
const fileReg = path.join(inc.cartella, 'runtime', 'registro.json');
const hash = f => { const p = path.join(SITO, f); return fs.existsSync(p) && fs.statSync(p).isFile() ? crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex') : null; };
const git = argv => { try { return execFileSync('git', ['-C', SITO, ...argv], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] }); } catch { return null; } };
// Elenco "stato Git" come mappa percorso -> codice (porcelain v1, percorsi non tracciati espansi).
function statoGit() {
  const out = git(['status', '--porcelain', '--untracked-files=all']);
  if (out === null) return null;
  const m = {};
  for (const r of out.split('\n').filter(Boolean)) { const p = r.slice(3).replace(/^"|"$/g, ''); m[p.includes(' -> ') ? p.split(' -> ')[1] : p] = r.slice(0, 2); }
  return m;
}
// Espande i modelli semplici della configurazione (.env.*) sui file realmente presenti nella radice.
function protetti() {
  const cfg = carica();
  const elenco = (cfg.sito && cfg.sito.file_da_non_modificare) || [];
  const out = new Set();
  for (const e of elenco) {
    if (!e.includes('*')) { out.add(e); continue; }
    const re = new RegExp('^' + e.split('*').map(s => s.replace(/[.+?^${}()|[\]\\]/g, '\\$&')).join('.*') + '$');
    const d = path.dirname(e) === '.' ? '' : path.dirname(e);
    try { for (const f of fs.readdirSync(path.join(SITO, d))) if (re.test(path.join(d, f))) out.add(path.join(d, f)); } catch {}
  }
  return [...out];
}
const leggi = () => JSON.parse(fs.readFileSync(fileReg, 'utf8'));
const scrivi = r => { fs.mkdirSync(path.dirname(fileReg), { recursive: true }); fs.writeFileSync(fileReg, JSON.stringify(r, null, 2)); };

if (cmd === 'inizio') {
  const st = statoGit();
  const r = {
    quando: new Date().toISOString(),
    git: st === null ? null : { head: (git(['rev-parse', 'HEAD']) || '').trim() || null, ramo: (git(['branch', '--show-current']) || '').trim(), stato: st },
    giaModificati: {}, protetti: {}, preservati: {},
  };
  for (const f of Object.keys(st || {})) r.giaModificati[f] = hash(f);
  for (const f of protetti()) r.protetti[f] = hash(f);
  scrivi(r);
  console.log(st === null ? 'Il sito non è un repository Git: verranno confrontate solo le impronte.' : `Stato Git registrato: ramo ${r.git.ramo || '(staccato)'}, ${Object.keys(st).length} file già modificati o non tracciati prima di iniziare.`);
  if (Object.keys(st || {}).length) console.log('ATTENZIONE: il sito ha già modifiche non salvate (di altri). Non vanno toccate:\n  ' + Object.keys(st).slice(0, 20).join('\n  '));
} else if (cmd === 'preserva') {
  const r = leggi();
  for (const f of resto) { const rel = path.isAbsolute(f) ? path.relative(SITO, f) : f; r.preservati[rel] = hash(rel); }
  scrivi(r);
  console.log(`File da preservare registrati: ${Object.keys(r.preservati).length}`);
} else if (cmd === 'verifica') {
  const r = leggi();
  const st = statoGit() || {};
  const righe = [], problemi = [];
  const nuovi = Object.keys(st).filter(f => !(f in r.giaModificati));
  const toccatiPrima = Object.keys(r.giaModificati).filter(f => hash(f) !== r.giaModificati[f]);
  righe.push(`File cambiati nel sito durante l'incarico (${nuovi.length}):`, ...nuovi.map(f => `  ${st[f]} ${f}`));
  if (toccatiPrima.length) { righe.push('File che erano GIÀ modificati prima di iniziare e ora sono diversi:', ...toccatiPrima.map(f => '  ' + f)); problemi.push('modificati file che erano già in lavorazione da altri'); }
  const prot = Object.keys(r.protetti).filter(f => hash(f) !== r.protetti[f]);
  righe.push(prot.length ? `File protetti MODIFICATI: ${prot.join(', ')}` : `File protetti invariati (${Object.keys(r.protetti).length}).`);
  if (prot.length) problemi.push('file protetti modificati');
  const pres = Object.keys(r.preservati).filter(f => hash(f) !== r.preservati[f]);
  if (Object.keys(r.preservati).length) righe.push(pres.length ? `File da preservare MODIFICATI: ${pres.join(', ')}` : `Landing originale e dipendenze preservate (${Object.keys(r.preservati).length} file invariati).`);
  if (pres.length) problemi.push('landing originale modificata');
  const head = (git(['rev-parse', 'HEAD']) || '').trim() || null;
  if (r.git && head !== r.git.head) { righe.push(`ATTENZIONE: il commit corrente è cambiato (${r.git.head} → ${head}).`); problemi.push('commit cambiato'); }
  righe.push(problemi.length ? `ESITO: DA CONTROLLARE (${problemi.join('; ')})` : 'ESITO: OK');
  fs.mkdirSync(path.join(inc.cartella, 'report'), { recursive: true });
  fs.writeFileSync(path.join(inc.cartella, 'report', 'modifiche.txt'), righe.join('\n') + '\n');
  console.log(righe.join('\n'));
  process.exitCode = problemi.length ? 1 : 0;
} else { console.error('comando sconosciuto'); process.exit(2); }

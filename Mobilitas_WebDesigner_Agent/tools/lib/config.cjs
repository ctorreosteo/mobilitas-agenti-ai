// Configurazione dell'agente WebDesigner Mobilitas.
// Legge config/mobilitas.json (locale) oppure, se manca, config/mobilitas.example.json. MOBILITAS_CONFIG indica un file
// alternativo (usato dai test). Percorsi relativi = dalla cartella dell'agente; "~" = cartella utente.
// Gli strumenti non scrivono MAI nella cartella dell'agente: i risultati vanno nella cartella dell'incarico, lo stato
// (cache, log, credenziali) in <lavoro.cartella>/.stato.
//
// Uso da terminale (per gli script .sh):
//   node tools/lib/config.cjs get <chiave.annidata>     valore (i percorsi noti vengono risolti)
//   node tools/lib/config.cjs lista <chiave>            un elemento per riga
//   node tools/lib/config.cjs stato [sottocartella]     cartella di stato (creata se manca)
//   node tools/lib/config.cjs porta-libera <chiave>     prima porta libera a partire dal valore
//   node tools/lib/config.cjs file                      quale file di configurazione è in uso
const fs = require('fs');
const os = require('os');
const net = require('net');
const path = require('path');

const ROOT = path.resolve(__dirname, '../..');
const PERCORSI = new Set(['sito.cartella', 'documentazione.cartella', 'brand.cartella', 'brand.linee_guida', 'lavoro.cartella']);

function carica() {
  const locale = process.env.MOBILITAS_CONFIG ? path.resolve(process.env.MOBILITAS_CONFIG) : path.join(ROOT, 'config/mobilitas.json');
  const file = fs.existsSync(locale) ? locale : path.join(ROOT, 'config/mobilitas.example.json');
  const cfg = JSON.parse(fs.readFileSync(file, 'utf8'));
  Object.defineProperty(cfg, '_file', { value: file.startsWith(ROOT) ? path.relative(ROOT, file) : file });
  return cfg;
}

function risolvi(p) {
  if (!p) return '';
  const espanso = String(p).replace(/^~(?=\/|$)/, os.homedir());
  return path.isAbsolute(espanso) ? espanso : path.resolve(ROOT, espanso);
}

function prendi(cfg, chiave) {
  const v = chiave.split('.').reduce((o, k) => (o == null ? undefined : o[k]), cfg);
  return PERCORSI.has(chiave) && typeof v === 'string' ? risolvi(v) : v;
}

// Cartella di stato: <lavoro>/.stato[/sotto]. Rifiuta di stare dentro la cartella dell'agente.
function stato(sotto = '') {
  const lavoro = prendi(carica(), 'lavoro.cartella');
  if (!lavoro) throw new Error('lavoro.cartella non configurata');
  const dir = path.join(lavoro, '.stato', sotto);
  if ((dir + path.sep).startsWith(ROOT + path.sep)) throw new Error('la cartella di lavoro non può stare dentro la cartella dell\'agente');
  fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  return dir;
}

// Incarico creato da tools/incarico/nuovo.sh: legge incarico.json.
function leggiIncarico(dir) {
  const cartella = path.resolve(dir);
  const f = path.join(cartella, 'incarico.json');
  if (!fs.existsSync(f)) throw new Error(`${cartella} non è una cartella di incarico (manca incarico.json)`);
  return { ...JSON.parse(fs.readFileSync(f, 'utf8')), cartella };
}

// --chiave valore e --interruttore
function args(argv = process.argv.slice(2)) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) { out._.push(a); continue; }
    const k = a.slice(2);
    if (i + 1 < argv.length && !argv[i + 1].startsWith('--')) out[k] = argv[++i];
    else out[k] = true;
  }
  return out;
}

const libera = porta => new Promise(res => {
  const s = net.createServer().once('error', () => res(false)).once('listening', () => s.close(() => res(true)));
  s.listen(porta, '127.0.0.1');
});

// Indirizzo della pagina e porta della guardia: da --url/--guardia oppure da --incarico + --percorso (es. /reflusso-v2).
function bersaglio(a) {
  if (a.url) return { url: a.url, guardia: a.guardia ? Number(a.guardia) : null };
  if (!a.incarico || !a.percorso) throw new Error('indica --url <indirizzo> oppure --incarico <cartella-incarico> --percorso </percorso-della-landing>');
  const inc = leggiIncarico(a.incarico);
  const percorsi = String(a.percorso).split(',').map(p => `http://localhost:${inc.porta_sviluppo}${p.startsWith('/') ? p : '/' + p}`);
  return { url: percorsi.join(','), guardia: inc.porta_guardia, incarico: inc };
}

module.exports = { ROOT, carica, risolvi, prendi, stato, leggiIncarico, args, libera, bersaglio };

if (require.main === module) {
  const [cmd, chiave] = process.argv.slice(2);
  const cfg = carica();
  (async () => {
    if (cmd === 'file') return console.log(cfg._file);
    if (cmd === 'get') { const v = prendi(cfg, chiave); return console.log(v == null ? '' : typeof v === 'object' ? JSON.stringify(v) : v); }
    if (cmd === 'lista') return (prendi(cfg, chiave) || []).forEach(v => console.log(v));
    if (cmd === 'stato') return console.log(stato(chiave || ''));
    if (cmd === 'porta-libera') {
      // Salta anche le porte assegnate ad altri incarichi, anche se in questo momento i loro servizi sono spenti.
      const lavoro = prendi(cfg, 'lavoro.cartella');
      const usate = new Set();
      if (lavoro && fs.existsSync(lavoro)) for (const d of fs.readdirSync(lavoro)) {
        try { const l = leggiIncarico(path.join(lavoro, d)); [l.porta_sviluppo, l.porta_guardia, l.porta_visore].forEach(n => usate.add(Number(n))); } catch {}
      }
      const base = Number(prendi(cfg, chiave));
      for (let p = base; p < base + 80; p++) if (!usate.has(p) && await libera(p)) return console.log(p);
      console.error('nessuna porta libera'); process.exit(1);
    }
    console.error('uso: config.cjs get|lista|stato|porta-libera <chiave> | file'); process.exit(2);
  })().catch(e => { console.error(e.message); process.exit(1); });
}

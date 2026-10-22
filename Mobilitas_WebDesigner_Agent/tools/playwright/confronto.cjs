// Affianca due o più immagini con un'etichetta sopra ciascuna (es. bozza e React, prima e dopo), alla stessa larghezza.
// Nessuna rete: immagini inline, ogni richiesta bloccata.
// Uso: node confronto.cjs <uscita.png> <larghezza-colonna> "<etichetta>=<immagine.png>" "<etichetta>=<immagine.png>" ...
const fs = require('fs');
const path = require('path');
const { avvia } = require('./lib.cjs');

const [out, col, ...coppie] = process.argv.slice(2);
if (!out || !col || coppie.length < 2) { console.error('uso: confronto.cjs <uscita.png> <larghezza> "Bozza=a.png" "React=b.png" ...'); process.exit(2); }
const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const blocchi = coppie.map(c => {
  const i = c.indexOf('=');
  const [etichetta, file] = [c.slice(0, i), c.slice(i + 1)];
  const tipo = /\.jpe?g$/i.test(file) ? 'jpeg' : 'png';
  return `<figure style="margin:0;width:${+col}px"><figcaption style="font:600 16px/1.4 system-ui;padding:0 0 8px">${esc(etichetta)}</figcaption><img style="width:100%;display:block;outline:1px solid #888" src="data:image/${tipo};base64,${fs.readFileSync(file).toString('base64')}"></figure>`;
}).join('');
(async () => {
  const browser = await avvia();
  const page = await browser.newPage({ viewport: { width: 400, height: 400 } });
  await page.route('**/*', r => r.abort());
  await page.setContent(`<body style="margin:0;padding:16px;display:flex;gap:16px;align-items:flex-start;background:#ddd;width:max-content">${blocchi}</body>`, { waitUntil: 'load' });
  await page.screenshot({ path: path.resolve(out), fullPage: true });
  await browser.close();
  console.log('scritto', out);
})();

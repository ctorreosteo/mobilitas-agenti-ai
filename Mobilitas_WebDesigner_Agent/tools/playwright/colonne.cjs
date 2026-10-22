// Divide una cattura a pagina intera in N colonne affiancate, per leggere una pagina lunga in un'unica immagine.
// Nessuna rete: immagine inline, ogni richiesta bloccata.
// Uso: node colonne.cjs <cattura.png> <uscita.png> [colonne=4] [larghezza-colonna=360]
const fs = require('fs');
const path = require('path');
const { avvia } = require('./lib.cjs');

const [src, out, n = '4', col = '360'] = process.argv.slice(2);
if (!src || !out) { console.error('uso: colonne.cjs <cattura.png> <uscita.png> [colonne] [larghezza-colonna]'); process.exit(2); }
const data = `data:image/png;base64,${fs.readFileSync(src).toString('base64')}`;
(async () => {
  const browser = await avvia();
  const page = await browser.newPage({ viewport: { width: 400, height: 400 } });
  await page.route('**/*', r => r.abort());
  await page.setContent(`<body style="margin:0;background:#bbb"><img id="i" src="${data}"></body>`, { waitUntil: 'load' });
  const { w, h } = await page.evaluate(() => { const i = document.getElementById('i'); return { w: i.naturalWidth, h: i.naturalHeight }; });
  const N = +n, C = +col, scale = C / w, sliceH = Math.ceil(h / N);
  const cols = Array.from({ length: N }, (_, k) => `<div style="width:${C}px;height:${Math.ceil(sliceH * scale)}px;overflow:hidden;position:relative;outline:1px solid #888"><img src="${data}" style="position:absolute;left:0;top:${-k * sliceH * scale}px;width:${C}px"></div>`).join('');
  await page.setContent(`<body style="margin:0;padding:12px;display:flex;gap:12px;align-items:flex-start;background:#bbb;width:max-content">${cols}</body>`, { waitUntil: 'load' });
  await page.screenshot({ path: path.resolve(out), fullPage: true });
  await browser.close();
  console.log('scritto', out, { w, h, N, C });
})();

// Screenshot e misure di una bozza HTML (es. Superdesign) servita dal visore locale, con le foto reali locali.
// Guardia nel browser: ogni richiesta che non va al visore viene bloccata e registrata; solo GET.
// Uso: node cattura-bozza.cjs --incarico <cartella> --pagina <file.html> --prefisso <nome>   (visore avviato con tools/sito/avvia.sh <incarico> --visore)
//      oppure --origine http://127.0.0.1:<porta> --pagina <file.html> --prefisso <nome> --uscita <dir>
const fs = require('fs');
const path = require('path');
const { args, avvia, contesto, viewports, wait } = require('./lib.cjs');
const { leggiIncarico, stato } = require('../lib/config.cjs');

const a = args();
const inc = a.incarico ? leggiIncarico(a.incarico) : null;
const ORIGIN = a.origine || (inc && `http://127.0.0.1:${inc.porta_visore}`);
if (!ORIGIN || !a.pagina) { console.error('uso: cattura-bozza.cjs --incarico <cartella> --pagina <file.html> --prefisso <nome>'); process.exit(2); }
const prefisso = a.prefisso || 'bozza';
const out = path.resolve(a.uscita || (inc ? path.join(inc.cartella, 'report/screenshot') : stato('prove')));
fs.mkdirSync(out, { recursive: true });

(async () => {
  const browser = await avvia();
  const report = {};
  for (const [width, height] of viewports(a.viewport)) {
    const ctx = await contesto(browser, [width, height]);
    const bloccate = [], errori = [], nonGet = [];
    await ctx.route('**/*', route => {
      const req = route.request();
      if (!req.url().startsWith(ORIGIN + '/')) { bloccate.push(req.url()); return route.abort('blockedbyclient'); }
      if (req.method() !== 'GET') { nonGet.push(`${req.method()} ${req.url()}`); return route.abort('blockedbyclient'); }
      return route.continue();
    });
    const page = await ctx.newPage();
    page.on('pageerror', e => errori.push(String(e)));
    await page.goto(`${ORIGIN}/${a.pagina}`, { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await wait(800);
    await page.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight / 2) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); });
    await wait(1200);
    const tag = `${prefisso}-${width}x${height}`;
    await page.screenshot({ path: `${out}/${tag}-prima-schermata.png` });
    await page.screenshot({ path: `${out}/${tag}-pagina-intera.png`, fullPage: true });
    report[tag] = await page.evaluate(() => {
      const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0; };
      const txt = [...document.querySelectorAll('body *')].filter(el => vis(el) && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
      const small = txt.filter(el => parseFloat(getComputedStyle(el).fontSize) < 14);
      const ctas = [...document.querySelectorAll('a,button')].filter(vis).map(el => { const r = el.getBoundingClientRect(); return { testo: el.textContent.trim().replace(/\s+/g, ' ').slice(0, 50), top: Math.round(r.top + scrollY), h: Math.round(r.height), w: Math.round(r.width) }; });
      const prenota = ctas.filter(c => /prenot/i.test(c.testo));
      return {
        altezzaPagina: document.documentElement.scrollHeight,
        overflowX: document.documentElement.scrollWidth - innerWidth,
        font: [...new Set(txt.map(el => getComputedStyle(el).fontFamily.split(',')[0].replace(/"/g, '')))],
        h1: [...document.querySelectorAll('h1')].map(h => `${getComputedStyle(h).fontWeight} ${parseFloat(getComputedStyle(h).fontSize)}px «${h.textContent.trim().replace(/\s+/g, ' ').slice(0, 60)}»`),
        sezioni: document.querySelectorAll('section').length,
        prenotaNellaPrimaSchermata: prenota.filter(c => c.top + c.h <= innerHeight).map(c => `${c.testo} (alto ${c.top}px)`),
        bersagliSotto44: ctas.filter(c => c.h < 44).map(c => `${c.testo || '[senza testo]'} ${c.w}x${c.h}`),
        testoSotto14: small.length,
        immaginiRotte: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src),
        segnapostoRimasti: [...document.images].filter(i => /placehold\.co/.test(i.src)).length,
      };
    });
    Object.assign(report[tag], { richiesteBloccate: [...new Set(bloccate)], richiesteNonGet: nonGet, erroriJs: errori });
    await ctx.close();
  }
  await browser.close();
  const file = path.join(out, `${prefisso}-misure.json`);
  fs.writeFileSync(file, JSON.stringify(report, null, 2));
  console.log(JSON.stringify(report, null, 2));
})().catch(e => { console.error(e); process.exit(1); });

// Testo visibile in una pagina HyperFrames, fotogramma per fotogramma (agente reel-grafiche, fase 4, 04/11/2026).
// Apre la pagina nel Chrome di render (sola lettura, lo stesso di HyperFrames), porta la timeline della scena a
// ogni fotogramma e scrive, per ogni nodo di testo visibile: testo, opacità effettiva, riquadro visibile
// (tagliato dai contenitori con overflow nascosto) e corpo effettivo (font-size per la scala delle trasformazioni).
// Niente rete: la pagina e i suoi file sono locali.
// Uso: node reel_dom.mjs <cartella pagina> <out.json> <fps> <fotogrammi> <chrome> <profilo> <puppeteer-core.js>
import { pathToFileURL } from 'node:url';
import fs from 'node:fs';

const [, , dir, out, fpsS, nS, chrome, profilo, pup] = process.argv;
const { default: puppeteer } = await import(pathToFileURL(pup).href);
const fps = Number(fpsS), n = Number(nS);
const browser = await puppeteer.launch({ protocolTimeout: 120000,
  executablePath: chrome, headless: true, userDataDir: profilo,
  args: ['--no-first-run', '--no-default-browser-check', '--disable-background-networking', '--disable-component-update',
    '--disable-sync', '--metrics-recording-only', '--disable-default-apps', '--allow-file-access-from-files'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
// niente rete: la pagina e locale (l'intercettazione delle richieste blocca i file locali: si usa il modo offline)
await page.setOfflineMode(true);
page.on('pageerror', (e) => console.error('errore nella pagina:', e.message));
// la registrazione delle timeline la crea il runtime di HyperFrames, che qui non c'è
await page.evaluateOnNewDocument(() => { window.__timelines = window.__timelines || {}; });
await page.goto(pathToFileURL(dir + '/index.html').href, { waitUntil: 'load' });
for (let i = 0; ; i++) {
  if (await page.evaluate(() => !!(window.__timelines && window.__timelines.scena))) break;
  if (i > 300) { console.error('la timeline della scena non si registra'); await browser.close(); process.exit(2); }
  await new Promise((r) => setTimeout(r, 100));
}
await page.evaluate(() => document.fonts.ready);
const frames = [];
for (let k = 0; k < n; k++) {
  const r = await page.evaluate((tt) => {
    const tl = window.__timelines.scena;
    const leggi = () => {
      const res = [];
      const w = document.createTreeWalker(document.getElementById('root'), NodeFilter.SHOW_TEXT);
      let nodo, idx = -1;
      while ((nodo = w.nextNode())) {
        idx++;
        const s = nodo.nodeValue;
        if (!s || !s.trim()) continue;
        const e = nodo.parentElement;
        const cs = getComputedStyle(e);
        if (cs.visibility === 'hidden') continue;
        let op = 1, sc = 1, x = e, nascosto = false;
        const rg = document.createRange(); rg.selectNodeContents(nodo);
        const b = rg.getBoundingClientRect();
        let vis = { x0: b.left, y0: b.top, x1: b.right, y1: b.bottom };
        while (x && x !== document.documentElement) {
          const c = getComputedStyle(x);
          if (c.display === 'none') { nascosto = true; break; }
          op *= parseFloat(c.opacity);
          if (c.transform && c.transform !== 'none') { const m = new DOMMatrix(c.transform); sc *= Math.hypot(m.a, m.b); }
          if (x !== e && (c.overflow !== 'visible' || c.overflowX !== 'visible' || c.overflowY !== 'visible')) {
            const q = x.getBoundingClientRect();
            vis = { x0: Math.max(vis.x0, q.left), y0: Math.max(vis.y0, q.top), x1: Math.min(vis.x1, q.right), y1: Math.min(vis.y1, q.bottom) };
          }
          x = x.parentElement;
        }
        if (nascosto || op < 0.02) continue;
        if (vis.x1 - vis.x0 < 1 || vis.y1 - vis.y0 < 1) continue;
        res.push({ i: idx, t: s, op: Math.round(op * 1000) / 1000, fs: Math.round(parseFloat(cs.fontSize) * sc * 10) / 10,
          b: [Math.round(b.left), Math.round(b.top), Math.round(b.right), Math.round(b.bottom)],
          v: [Math.round(vis.x0), Math.round(vis.y0), Math.round(vis.x1), Math.round(vis.y1)], c: e.className || '' });
      }
      return res;
    };
    tl.pause(); tl.seek(tt[0], false); const a = leggi();
    tl.seek(tt[1], false); const b = leggi();
    return [a, b];
  }, [k / fps, k / fps + 0.0005]);
  frames.push(r);
}
fs.writeFileSync(out, JSON.stringify({ fps, frames }));
await browser.close();

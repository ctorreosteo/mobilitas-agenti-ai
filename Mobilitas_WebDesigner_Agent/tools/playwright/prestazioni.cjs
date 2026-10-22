// Misura comparativa delle prestazioni (sola lettura): LCP, fotogrammi durante uno scorrimento continuo
// (28 px per fotogramma), peso di immagini e script. Sul server di sviluppo conta il confronto tra versioni,
// non il valore assoluto. Due passaggi per viewport (390 e 1440).
// Uso: node prestazioni.cjs --incarico <cartella> --percorso /a[,/b]  oppure  --url "<a>[,<b>]" [--guardia porta]
// Uscita: <incarico>/report/prestazioni.json (o --uscita); mai nella cartella dell'agente.
const fs = require('fs');
const path = require('path');
const { args, bersaglio, avvia, contesto, fontRoute, wait, uscita } = require('./lib.cjs');

const a = args();
const b = bersaglio(a);
const URLS = String(b.url).split(',');

(async () => {
  const browser = await avvia({ guardia: b.guardia });
  const righe = [];
  for (const vp of [[390, 844], [1440, 900]]) for (const URL of URLS) for (let giro = 0; giro < 2; giro++) {
    const ctx = await contesto(browser, vp);
    const page = await ctx.newPage(); await fontRoute({ page });
    await page.goto(URL); await page.evaluate(() => document.fonts.ready); await wait(1500);
    const lcp = await page.evaluate(() => new Promise(res => { let v = 0; new PerformanceObserver(l => { for (const e of l.getEntries()) v = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true }); setTimeout(() => res(Math.round(v)), 300); }));
    const fotogrammi = await page.evaluate(() => new Promise(res => { const H = document.documentElement.scrollHeight - innerHeight; const d = []; let last = performance.now(); let y = 0; const step = () => { const now = performance.now(); d.push(now - last); last = now; y += 28; scrollTo(0, y); if (y < H && d.length < 600) requestAnimationFrame(step); else res(d.slice(2)); }; requestAnimationFrame(step); }));
    fotogrammi.sort((x, y) => x - y); const q = p => Math.round((fotogrammi[Math.floor(fotogrammi.length * p)] || 0) * 10) / 10;
    const risorse = await page.evaluate(() => { const r = performance.getEntriesByType('resource'); const img = r.filter(x => x.initiatorType === 'img' || /\.(jpe?g|png|webp|avif|gif|svg)(\?|$)/.test(x.name)); const js = r.filter(x => x.initiatorType === 'script' || /\.(jsx?|mjs)(\?|$)/.test(x.name)); return { kBImmagini: Math.round(img.reduce((s, x) => s + (x.transferSize || x.encodedBodySize || 0), 0) / 1024), kBJs: Math.round(js.reduce((s, x) => s + (x.decodedBodySize || 0), 0) / 1024), altezza: document.documentElement.scrollHeight }; });
    righe.push({ viewport: vp[0], url: URL, giro, lcpMs: lcp, p50: q(0.5), p95: q(0.95), max: q(0.999), oltre33ms: fotogrammi.filter(f => f > 33.4).length, ...risorse });
    await ctx.close();
  }
  await browser.close();
  for (const r of righe) console.log(JSON.stringify(r));
  fs.writeFileSync(path.join(uscita(a, b), 'prestazioni.json'), JSON.stringify(righe, null, 2));
})().catch(e => { console.error(e); process.exit(1); });

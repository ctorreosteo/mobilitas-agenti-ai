// Screenshot e misure di una o più pagine a 1440×900, 390×844 e 375×667 (prima schermata + pagina intera).
// Misure: errori JS, richieste non in lettura partite, richieste bloccate, sbordamento orizzontale, testo sotto 14 px,
// bersagli sotto 44 px, H1, immagini rotte, font, pulsante di prenotazione nella prima schermata, protezione di prova attiva.
//
// Uso:
//   node cattura.cjs --incarico <cartella-incarico> --percorso /reflusso-v2            (più percorsi: "/reflusso,/reflusso-v2")
//   node cattura.cjs --url <indirizzo> [--guardia <porta>] --uscita <cartella>
//   Opzioni: --riduci-movimento  --viewport 1440x900,390x844  --cta "<selettore>" (predefinito: link e pulsanti con «prenot»)
//            --ambito "<selettore>" limita le misure di testo e bersagli alla landing (escludendo Header e Footer del sito)
//            --attesa <ms> dopo il caricamento (predefinito 1600)  --prefisso <nome>
// Uscita: <incarico>/report/screenshot (oppure --uscita). Mai nella cartella dell'agente.
const fs = require('fs');
const path = require('path');
const { args, bersaglio, avvia, contesto, riscalda, scorriTutta, viewports, fontRoute, wait, uscita, nomeDa } = require('./lib.cjs');

const a = args();
const b = bersaglio(a);
const URLS = b.url.split(',');
const riduci = !!a['riduci-movimento'];
const outDir = uscita(a, b, 'screenshot');
const ambito = a.ambito || 'body';
const cta = a.cta || '';

async function misura(browser, url, prefisso) {
  const report = { url, ambito, riduciMovimento: riduci, quando: new Date().toISOString() };
  for (const [width, height] of viewports(a.viewport)) {
    const ctx = await contesto(browser, [width, height], { riduci });
    const page = await ctx.newPage();
    await fontRoute({ page });
    const errori = [], nonGet = [], fallite = [];
    page.on('pageerror', e => errori.push(String(e)));
    page.on('request', r => { if (!['GET', 'HEAD'].includes(r.method())) nonGet.push(`${r.method()} ${r.url()}`); });
    page.on('requestfailed', r => fallite.push(`${r.url()} (${r.failure()?.errorText})`));
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await wait(Number(a.attesa || 1600));
    const tag = `${prefisso}-${width}x${height}`;
    await page.screenshot({ path: `${outDir}/${tag}-prima-schermata.png` });
    // Misure prese in cima alla pagina, prima di scorrere (la prima schermata vera).
    const misure = await page.evaluate(({ ambito, cta }) => {
      const vis = el => { const s = getComputedStyle(el); const r = el.getBoundingClientRect(); return s.display !== 'none' && s.visibility !== 'hidden' && r.width > 0 && r.height > 0; };
      const root = document.querySelector(ambito) || document.body;
      const tutti = [...root.querySelectorAll('*')];
      const testo = tutti.filter(el => vis(el) && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && !el.closest('.sr-only, .pm-sr, [aria-hidden="true"]'));
      const piccolo = testo.filter(el => parseFloat(getComputedStyle(el).fontSize) < 14).map(el => `${getComputedStyle(el).fontSize} «${el.textContent.trim().slice(0, 40)}»`);
      const bersagli = [...root.querySelectorAll('a, button, summary, [role="button"], input, select, textarea')].filter(vis).map(el => { const r = el.getBoundingClientRect(); return { t: (el.textContent.trim() || el.getAttribute('aria-label') || el.name || '').replace(/\s+/g, ' ').slice(0, 44), w: Math.round(r.width), h: Math.round(r.height) }; });
      const pulsanti = (cta ? [...document.querySelectorAll(cta)] : [...document.querySelectorAll('a, button')].filter(el => /prenot/i.test(el.textContent))).filter(vis);
      const primo = pulsanti.map(x => { const r = x.getBoundingClientRect(); return { testo: x.textContent.trim().replace(/\s+/g, ' ').slice(0, 50), top: Math.round(r.top + scrollY), bottom: Math.round(r.bottom + scrollY), h: Math.round(r.height) }; }).sort((x, y) => x.top - y.top)[0] || null;
      const fuori = tutti.filter(el => { const r = el.getBoundingClientRect(); return vis(el) && (r.right > innerWidth + 1 || r.left < -1) && getComputedStyle(el).position !== 'fixed' && !el.closest('[data-scorre], [data-scroll-x]'); }).map(el => (typeof el.className === 'string' && el.className) || el.tagName).slice(0, 10);
      return {
        altezzaPagina: document.documentElement.scrollHeight,
        overflowX: document.documentElement.scrollWidth - innerWidth,
        fuoriSchermo: fuori,
        h1: [...document.querySelectorAll('h1')].map(h => `${getComputedStyle(h).fontWeight} ${parseFloat(getComputedStyle(h).fontSize)}px «${h.textContent.trim().replace(/\s+/g, ' ').slice(0, 60)}»`),
        titoli: [...root.querySelectorAll('h2, h3')].filter(vis).slice(0, 30).map(h => `${h.tagName} ${getComputedStyle(h).fontWeight} ${parseFloat(getComputedStyle(h).fontSize)}px «${h.textContent.trim().replace(/\s+/g, ' ').slice(0, 40)}»`),
        primoPulsantePrenota: primo,
        prenotaNellaPrimaSchermata: !!primo && primo.bottom <= innerHeight,
        testoSotto14: piccolo,
        bersagliSotto44: bersagli.filter(t => t.h < 44 || t.w < 24),
        fontPagina: getComputedStyle(root).fontFamily,
        protezioneProva: window.__testGuard ? { attiva: window.__testGuard.active, bloccati: window.__testGuard.blocked.map(x => `${x.kind} ${x.detail}`).slice(0, 20) } : 'ASSENTE',
      };
    }, { ambito, cta });
    // Pagina intera a densità 1×: a 2× una pagina lunga supera il limite di Chrome (16.384 px).
    const intera = width < 500 ? await contesto(browser, [width, height], { riduci, densita: 1 }) : null;
    const p2 = intera ? await intera.newPage() : page;
    if (intera) { await fontRoute({ page: p2 }); await p2.goto(url, { waitUntil: 'networkidle' }); await p2.evaluate(() => document.fonts.ready); }
    await scorriTutta(p2);
    await p2.screenshot({ path: `${outDir}/${tag}-pagina-intera.png`, fullPage: true });
    if (intera) await intera.close();
    await scorriTutta(page);
    const dopo = await page.evaluate(() => ({
      immaginiRotte: [...document.images].filter(i => i.complete && i.naturalWidth === 0).map(i => i.src),
      fontCaricati: [...document.fonts].filter(f => f.status === 'loaded').map(f => `${f.family} ${f.weight}`).filter((v, i, x) => x.indexOf(v) === i),
    }));
    report[tag] = { ...misure, ...dopo, erroriJs: errori, richiesteNonGet: nonGet, richiesteFallite: fallite };
    await ctx.close();
  }
  return report;
}

(async () => {
  const browser = await avvia({ guardia: b.guardia });
  let problemiTot = 0;
  for (const url of URLS) {
    const prefisso = (a.prefisso ? a.prefisso + (URLS.length > 1 ? '-' : '') : '') + (URLS.length > 1 || !a.prefisso ? nomeDa(url) : '') + (riduci ? '-riduci' : '');
    await riscalda(browser, url);
    const report = await misura(browser, url, prefisso);
    const file = path.join(outDir, `${prefisso}-misure.json`);
    fs.writeFileSync(file, JSON.stringify(report, null, 2));
    // Le richieste fallite verso altre origini sono quelle fermate dalla guardia (tracciamento, gestionale): sono attese.
    const origine = new URL(url).origin;
    const problemi = [];
    for (const [k, r] of Object.entries(report)) if (typeof r === 'object' && r && 'overflowX' in r) {
      if (r.erroriJs.length) problemi.push(`${k}: ${r.erroriJs.length} errori JS`);
      const interne = r.richiesteFallite.filter(x => x.startsWith(origine) && !/\/api\//.test(x));
      if (interne.length) problemi.push(`${k}: ${interne.length} risorse del sito non caricate (${interne.slice(0, 3).join(', ')})`);
      if (r.overflowX > 0) problemi.push(`${k}: sbordamento orizzontale ${r.overflowX}px`);
      if (r.testoSotto14.length) problemi.push(`${k}: ${r.testoSotto14.length} testi sotto 14 px`);
      if (r.bersagliSotto44.length) problemi.push(`${k}: ${r.bersagliSotto44.length} bersagli sotto 44 px`);
      if (r.h1.length !== 1) problemi.push(`${k}: ${r.h1.length} H1`);
      if (!r.prenotaNellaPrimaSchermata) problemi.push(`${k}: pulsante di prenotazione fuori dalla prima schermata`);
      if (r.immaginiRotte.length) problemi.push(`${k}: ${r.immaginiRotte.length} immagini rotte`);
      if (r.protezioneProva === 'ASSENTE') problemi.push(`${k}: protezione di prova non attiva`);
    }
    problemiTot += problemi.length;
    console.log(`${url}\n  screenshot e misure: ${file}`);
    console.log(problemi.length ? '  DA CONTROLLARE:\n    ' + problemi.join('\n    ') : '  Nessun problema rilevato dalle misure automatiche.');
  }
  await browser.close();
  process.exitCode = 0; // le misure non bocciano: vanno lette (controllo-qualita.md)
})().catch(e => { console.error(e); process.exit(1); });

// Base comune degli script di prova. Chrome di sistema (channel 'chrome'), nessun browser scaricato.
// - Se è indicata una guardia, tutto il traffico del browser passa da lì (anche il loopback); lo script rifiuta di partire
//   se la guardia non risponde.
// - In ogni scheda viene iniettata protezione-test.js prima degli script della pagina: nessun dato verso servizi reali.
// - Nessuno script scrive nella cartella dell'agente: l'uscita predefinita è la cartella dell'incarico o, senza incarico,
//   la cartella di stato (<lavoro>/.stato).
const fs = require('fs');
const path = require('path');
const http = require('http');

const PW = path.join(__dirname, 'node_modules/playwright-core');
if (!fs.existsSync(PW)) { console.error('Playwright non installato: esegui tools/setup/installa.sh'); process.exit(3); }
const { chromium } = require(PW);
const fontRoute = require('./font-route.cjs').default;
const { args, bersaglio, stato } = require('../lib/config.cjs');
const PROTEZIONE = path.join(__dirname, 'protezione-test.js');

const VIEWPORTS = [[1440, 900], [390, 844], [375, 667]];
const wait = ms => new Promise(r => setTimeout(r, ms));

function salute(porta) {
  return new Promise(res => {
    const req = http.get({ host: '127.0.0.1', port: porta, path: '/__guard/health', timeout: 1500 }, r => { r.resume(); res(r.statusCode === 200); });
    req.on('error', () => res(false)); req.on('timeout', () => { req.destroy(); res(false); });
  });
}

async function avvia({ guardia } = {}) {
  if (guardia) {
    if (!(await salute(guardia))) { console.error(`Guardia di rete non attiva su 127.0.0.1:${guardia}: avvio rifiutato (tools/sito/avvia.sh).`); process.exit(4); }
    return chromium.launch({ channel: 'chrome', headless: true, proxy: { server: `http://127.0.0.1:${guardia}`, bypass: '<-loopback>' } });
  }
  return chromium.launch({ channel: 'chrome', headless: true });
}

async function contesto(browser, [width, height], { riduci = false, densita, protezione = true } = {}) {
  const mobile = width < 500;
  const ctx = await browser.newContext({
    viewport: { width, height }, deviceScaleFactor: densita || (mobile ? 2 : 1), isMobile: mobile, hasTouch: mobile,
    serviceWorkers: 'block', reducedMotion: riduci ? 'reduce' : 'no-preference',
  });
  if (protezione) await ctx.addInitScript({ path: PROTEZIONE });
  return ctx;
}

// Riscaldamento: il server di sviluppo, al primo accesso, ottimizza le dipendenze e può RICARICARE la pagina.
// Si apre ogni indirizzo due volte (con la stessa protezione delle prove) prima di misurare.
async function riscalda(browser, url) {
  const ctx = await contesto(browser, [1440, 900]);
  const page = await ctx.newPage();
  await fontRoute({ page });
  for (let i = 0; i < 2; i++) { try { await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 }); } catch {} await wait(2500); }
  await ctx.close();
}

// Scorre tutta la pagina (immagini pigre, animazioni all'ingresso), forza il caricamento delle immagini, torna in cima.
async function scorriTutta(page, passo, tentativi = 2) {
  try {
    const H = await page.evaluate(() => document.documentElement.scrollHeight);
    const h = page.viewportSize().height;
    for (let y = 0; y < H; y += Math.round(passo || h * 0.7)) { await page.evaluate(v => scrollTo(0, v), y); await wait(90); }
    await page.evaluate(() => Promise.all([...document.images].map(i => { i.loading = 'eager'; return i.decode().catch(() => {}); })));
    await page.evaluate(() => scrollTo(0, 0)); await wait(400);
  } catch (e) {
    // Ricaricamento della pagina durante lo scorrimento (server di sviluppo): si attende e si riprova.
    if (!tentativi || !/context was destroyed|navigation/i.test(String(e))) throw e;
    await page.waitForLoadState('networkidle').catch(() => {}); await wait(1500);
    return scorriTutta(page, passo, tentativi - 1);
  }
}

// Cartella di uscita: --uscita, oppure <incarico>/report[/sotto], oppure <lavoro>/.stato/prove[/sotto].
function uscita(a, b, sotto = '') {
  const dir = a.uscita ? path.resolve(a.uscita) : b.incarico ? path.join(b.incarico.cartella, 'report', sotto) : path.join(stato('prove'), sotto);
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}
const nomeDa = url => (new URL(url).pathname.replace(/^\/|\/$/g, '').replace(/[^a-z0-9]+/gi, '-') || 'home').toLowerCase();
const viewports = s => (s ? String(s).split(',').map(v => v.split('x').map(Number)) : VIEWPORTS);

module.exports = { chromium, fontRoute, args, bersaglio, avvia, contesto, riscalda, scorriTutta, viewports, wait, uscita, nomeDa, VIEWPORTS };

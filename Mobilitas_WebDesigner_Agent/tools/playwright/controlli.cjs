// Controlli funzionali di una o più landing del sito, a 1440×900 e 390×844, con le integrazioni REALI della pagina
// ma senza che parta alcun dato: protezione di prova nel browser + guardia di rete.
//   1. prenotazione: il pulsante apre il modulo (popup del sito); l'invio a campi vuoti mostra gli errori e non spedisce
//      nulla. Fuoco ed Esc vengono annotati (il popup è un componente condiviso del sito: i suoi limiti si segnalano);
//   2. domande frequenti: <details> e pulsanti aria-expanded si aprono con clic e con Invio;
//   3. tastiera: gli elementi della landing raggiunti con Tab hanno un anello di fuoco visibile;
//   4. barra mobile (390): nascosta in cima, visibile dopo lo scorrimento (se presente);
//   5. protezione di prova attiva e nessuna scrittura partita dal browser;
//   6. riduci movimento: nessuna animazione infinita in corso.
// Mai inviati moduli compilati: nessun dato di prova raggiunge il gestionale.
// Uso: node controlli.cjs --incarico <cartella> --percorso /reflusso-v2[,/reflusso]  oppure  --url <indirizzo> [--guardia porta]
//   Opzioni: --cta "<selettore>"  --barra "<selettore>"  --ambito "<selettore della landing>" (es. main)
const fs = require('fs');
const path = require('path');
const { args, bersaglio, avvia, contesto, riscalda, fontRoute, wait, uscita, nomeDa } = require('./lib.cjs');

const a = args();
const b = bersaglio(a);
const URLS = b.url.split(',');
const outDir = uscita(a, b);
const CTA = a.cta || '';
const BARRA = a.barra || '.pm-bar, [data-barra-mobile]';
const AMBITO = a.ambito || 'body';
const DIALOGO = 'dialog[open], [role="dialog"]:visible, [aria-modal="true"]:visible';

async function prova(browser, url, vp) {
  const ris = {};
  const ctx = await contesto(browser, vp);
  const page = await ctx.newPage();
  await fontRoute({ page });
  const richieste = []; page.on('request', r => richieste.push({ m: r.method(), u: r.url() }));
  const errori = []; page.on('pageerror', e => errori.push(String(e)));
  const apri = async () => { await page.goto(url, { waitUntil: 'networkidle' }); await page.evaluate(() => document.fonts.ready); await wait(1200); };
  const inputVisibili = () => page.evaluate(() => [...document.querySelectorAll('form input, form textarea, form select')].filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== 'hidden'; }).length);
  await apri();

  // 1. Prenotazione
  const trigger = CTA ? page.locator(CTA).first() : page.locator('button, a[href^="#"], a[role="button"]').filter({ hasText: /prenot/i }).first();
  if (!(await trigger.count())) ris.prenotazione = { esito: 'non presente' };
  else {
    const prima = await inputVisibili();
    await trigger.scrollIntoViewIfNeeded(); await trigger.click(); await wait(800);
    const dialogo = (await page.locator(DIALOGO).count()) > 0;
    const campi = await inputVisibili();
    const r = { aperta: dialogo || campi > prima, semanticaDialogo: dialogo, campiVisibili: campi };
    if (r.aperta) {
      r.fuocoDentro = await page.evaluate(() => { const d = document.querySelector('dialog[open], [role="dialog"], [aria-modal="true"]'); return d ? d.contains(document.activeElement) : document.activeElement?.closest('form') != null; });
      const prima2 = richieste.length;
      const form = dialogo ? page.locator(DIALOGO).first() : page.locator('form:visible').last();
      const invio = form.locator('button[type="submit"], input[type="submit"], button:not([type])').first();
      if (await invio.count() && !(await invio.isEnabled())) {
        // Il modulo impedisce l'invio a campi vuoti (pulsante disabilitato): è già la validazione. Nessun clic.
        r.invioDisabilitatoACampiVuoti = true;
        r.scrittureDopoInvio = [];
      } else if (await invio.count()) {
        await invio.click({ timeout: 5000 }); await wait(700);
        r.erroriMostrati = await page.locator('[aria-invalid="true"], [role="alert"], .error, [class*="error"], [class*="errore"], :invalid').count();
        r.scrittureDopoInvio = richieste.slice(prima2).filter(x => x.m !== 'GET' && x.m !== 'HEAD').map(x => `${x.m} ${x.u}`);
        r.bloccatiDallaProtezione = await page.evaluate(() => window.__testGuard ? window.__testGuard.blocked.filter(x => !/^(fbq|gtag|clarity)$/.test(x.kind)).map(x => `${x.kind} ${x.detail}`) : []);
      }
      await page.keyboard.press('Escape'); await wait(600);
      r.chiusaConEsc = (await page.locator(DIALOGO).count()) === 0 && (await inputVisibili()) <= prima;
    }
    // Esito: si apre e a campi vuoti non spedisce nulla. Fuoco ed Esc sono note sul componente condiviso.
    r.esito = r.aperta && !(r.scrittureDopoInvio || []).length ? 'OK' : 'NO';
    r.note = [r.aperta && !r.fuocoDentro ? 'il fuoco non entra nel modulo' : '', r.aperta && !r.chiusaConEsc ? 'Esc non chiude il modulo' : '', r.aperta && r.erroriMostrati === 0 && !r.invioDisabilitatoACampiVuoti ? 'nessun messaggio di errore visibile a campi vuoti' : '', r.invioDisabilitatoACampiVuoti ? 'invio disabilitato finché i campi sono vuoti' : ''].filter(Boolean);
    ris.prenotazione = r;
  }

  // 2. Domande frequenti
  await apri();
  const det = page.locator(`${AMBITO} details > summary`);
  const esp = page.locator(`${AMBITO} button[aria-expanded]`);
  if (!(await det.count()) && !(await esp.count())) ris.domande = { esito: 'non presente' };
  else {
    const r = {};
    if (await det.count()) {
      const s = det.first(); await s.scrollIntoViewIfNeeded();
      await s.click(); await wait(400); r.detailsClic = await s.evaluate(el => el.parentElement.open);
      await s.click(); await wait(400);
      await s.focus(); await page.keyboard.press('Enter'); await wait(400); r.detailsInvio = await s.evaluate(el => el.parentElement.open);
    }
    if (await esp.count()) {
      const x = esp.first(); await x.scrollIntoViewIfNeeded();
      const prima = await x.getAttribute('aria-expanded');
      await x.click(); await wait(400); r.espandibileClic = (await x.getAttribute('aria-expanded')) !== prima;
      await x.focus(); await page.keyboard.press('Enter'); await wait(400); r.espandibileInvio = (await x.getAttribute('aria-expanded')) === prima;
    }
    r.esito = Object.values(r).every(Boolean) ? 'OK' : 'NO';
    ris.domande = r;
  }

  // 3. Tastiera
  await apri();
  const fuochi = [];
  for (let i = 0; i < 16; i++) {
    await page.keyboard.press('Tab'); await wait(60);
    fuochi.push(await page.evaluate(ambito => {
      const el = document.activeElement; if (!el || el === document.body) return null;
      const s = getComputedStyle(el);
      const visibile = (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || (s.boxShadow && s.boxShadow !== 'none');
      return { el: `${el.tagName.toLowerCase()} «${(el.textContent || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 30)}»`, visibile, dentro: !!el.closest(ambito) };
    }, AMBITO));
  }
  const raggiunti = fuochi.filter(Boolean);
  const dentro = raggiunti.filter(f => f.dentro);
  ris.tastiera = {
    raggiuntiNellaLanding: dentro.length,
    senzaAnello: dentro.filter(f => !f.visibile).map(f => f.el),
    fuoriAmbitoSenzaAnello: [...new Set(raggiunti.filter(f => !f.dentro && !f.visibile).map(f => f.el))], // Header/Footer del sito: si segnalano
    esito: !dentro.length ? 'non presente' : dentro.every(f => f.visibile) ? 'OK' : 'NO',
  };

  // 4. Barra mobile
  if (vp[0] < 500) {
    await apri();
    const statoBarra = () => page.evaluate(sel => { const x = document.querySelector(sel); if (!x) return 'assente'; const s = getComputedStyle(x); const r = x.getBoundingClientRect(); return s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) < 0.1 || r.top >= innerHeight ? 'nascosta' : 'visibile'; }, BARRA);
    const inizio = await statoBarra();
    if (inizio === 'assente') ris.barraMobile = { esito: 'non presente' };
    else {
      await page.evaluate(() => scrollTo(0, innerHeight * 1.6)); await wait(700);
      const dopo = await statoBarra();
      ris.barraMobile = { inizio, dopoScorrimento: dopo, esito: dopo === 'visibile' ? 'OK' : 'NO' };
    }
  }

  // 5. Protezione e rete
  const origine = new URL(url).origin;
  const fontLocale = u => /^https:\/\/fonts\.googleapis\.com\/css2\?family=Montserrat/.test(u) || u.startsWith('https://fonts.gstatic.com/s/montserrat/local/');
  const scritture = richieste.filter(x => x.m !== 'GET' && x.m !== 'HEAD').map(x => `${x.m} ${x.u}`);
  const esterne = [...new Set(richieste.filter(x => !x.u.startsWith(origine) && !/^(data|blob):/.test(x.u) && !fontLocale(x.u)).map(x => new URL(x.u).host))];
  const attiva = await page.evaluate(() => !!(window.__testGuard && window.__testGuard.active));
  ris.protezione = { attiva, scritturePartite: scritture, esternePresenti: esterne, esito: attiva && !scritture.length ? 'OK' : 'NO' };
  ris.erroriJs = errori;
  await ctx.close();

  // 6. Riduci movimento
  const rctx = await contesto(browser, vp, { riduci: true });
  const rp = await rctx.newPage(); await fontRoute({ page: rp });
  await rp.goto(url, { waitUntil: 'networkidle' }); await wait(1200);
  await rp.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight * 0.7) { scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); } });
  const infinite = await rp.evaluate(() => document.getAnimations().filter(an => an.playState === 'running' && an.effect?.getTiming?.().iterations === Infinity).map(an => an.animationName || an.transitionProperty || 'animazione'));
  ris.riduciMovimento = { animazioniInfinite: infinite, esito: infinite.length ? 'NO' : 'OK' };
  await rctx.close();
  return ris;
}

(async () => {
  const browser = await avvia({ guardia: b.guardia });
  let ok = 0, tot = 0;
  const righe = [];
  for (const url of URLS) {
    await riscalda(browser, url);
    const report = { url, quando: new Date().toISOString() };
    for (const vp of [[1440, 900], [390, 844]]) report[`${vp[0]}x${vp[1]}`] = await prova(browser, url, vp);
    let okU = 0, totU = 0;
    righe.push(url);
    for (const [tag, r] of Object.entries(report)) if (typeof r === 'object') for (const [k, v] of Object.entries(r)) {
      if (!v || !v.esito) continue;
      if (v.esito === 'non presente') { righe.push(`  ${tag} ${k}: non presente`); continue; }
      totU++; if (v.esito === 'OK') okU++;
      righe.push(`  ${tag} ${k}: ${v.esito}${v.note && v.note.length ? ' (note: ' + v.note.join('; ') + ')' : ''}`);
    }
    report.riepilogo = `${okU}/${totU} controlli superati`;
    righe.push(`  ${report.riepilogo}`);
    ok += okU; tot += totU;
    const file = path.join(outDir, `controlli-${nomeDa(url)}.json`);
    fs.writeFileSync(file, JSON.stringify(report, null, 2));
    righe.push(`  dettagli: ${file}`);
  }
  await browser.close();
  console.log(righe.join('\n') + `\nTotale: ${ok}/${tot} controlli superati`);
  process.exitCode = ok === tot ? 0 : 1;
})().catch(e => { console.error(e); process.exit(1); });

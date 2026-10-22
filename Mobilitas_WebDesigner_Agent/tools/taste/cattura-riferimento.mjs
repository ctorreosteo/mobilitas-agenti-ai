// Fase 1 di Taste (Capture) senza registrare server MCP nella sessione: avvia il Playwright MCP isolato
// (avvia-mcp.sh, dietro la guardia dei riferimenti) e segue SKILL.md di Taste: viewport 1440×900, navigazione,
// attesa 3 s, schermata, pagina intera (≤ 5400 px) oppure metà + piè di pagina, extract.js. In più, come supporto:
// campionamento delle animazioni durante lo scorrimento e una schermata a 390×844.
// Nessun clic, nessun modulo, nessuna scrittura. Le fasi 2–4 (analisi) le svolge l'agente leggendo i file prodotti.
// Uso: node cattura-riferimento.mjs <url> [cartella-uscita]   (predefinita: <lavoro>/.stato/taste/catture/<dominio>; meglio la cartella dell'incarico)
import { spawn } from 'node:child_process';
import dns from 'node:dns/promises';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { decide } from './policy-lib.mjs';
import { politica } from './politica.mjs';

const require = createRequire(import.meta.url);
const { ROOT, stato } = require('../lib/config.cjs');
const url = process.argv[2];
if (!url || !/^https?:\/\//.test(url)) { console.error('uso: cattura-riferimento.mjs <url> [cartella-uscita]'); process.exit(2); }
const domain = new URL(url).hostname.replace(/^www\./, '');
const out = path.resolve(process.argv[3] || path.join(stato('taste/catture'), domain));
fs.mkdirSync(out, { recursive: true });
const policy = politica();
const log = [];
const say = m => { log.push(m); console.log(m); };

// Controllo preliminare: guardia attiva, destinazione consentita dalla stessa politica.
const health = await fetch(`http://127.0.0.1:${policy.proxyPort}/__guard/health`).then(r => r.json()).catch(() => null);
if (!health || health.policy !== 'riferimenti') { console.error('Guardia dei riferimenti non attiva con la politica "riferimenti" (tools/taste/guardia.sh avvia): mi fermo.'); process.exit(2); }
const host = new URL(url).hostname;
let d = decide(policy, { method: 'CONNECT', host, port: 443, addresses: null });
let addresses = [];
if (d.needsResolve) { addresses = (await dns.lookup(host, { all: true }).catch(() => [])).map(a => a.address); d = decide(policy, { method: 'CONNECT', host, port: 443, addresses }); }
say(`controllo preliminare: ${host}:443 → ${d.allow ? 'CONSENTITO' : 'NEGATO'} (${d.reason})`);
if (!d.allow) process.exit(3);

const proc = spawn(path.join(ROOT, 'tools/taste/avvia-mcp.sh'), [out], { stdio: ['pipe', 'pipe', 'inherit'] });
let buf = ''; let id = 0; const pending = new Map();
proc.stdout.on('data', c => { buf += c; let i; while ((i = buf.indexOf('\n')) >= 0) { const line = buf.slice(0, i); buf = buf.slice(i + 1); try { const m = JSON.parse(line); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } } catch {} } });
const call = (method, params) => new Promise((res, rej) => { const n = ++id; pending.set(n, res); proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', id: n, method, params }) + '\n'); setTimeout(() => rej(new Error('timeout ' + method)), 120000); });
const tool = async (name, args = {}) => { const r = await call('tools/call', { name, arguments: args }); return { error: !!(r.error || r.result?.isError), text: r.error ? JSON.stringify(r.error) : (r.result.content || []).map(c => c.text || '').join('\n') }; };
const result = text => { const m = text.match(/### Result\s*\n([\s\S]*?)(\n### |$)/); const raw = (m ? m[1] : text).trim(); try { return JSON.parse(raw); } catch { return raw; } };

try {
  await call('initialize', { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'cattura-riferimento', version: '1.0' } });
  proc.stdin.write(JSON.stringify({ jsonrpc: '2.0', method: 'notifications/initialized', params: {} }) + '\n');
  await tool('browser_resize', { width: 1440, height: 900 });
  const nav = await tool('browser_navigate', { url });
  const title = (nav.text.match(/Page Title: (.*)/) || [])[1];
  say(`navigazione: ${nav.error ? 'ERRORE ' + nav.text.slice(0, 200) : 'ok'} — titolo: ${title}`);
  if (nav.error) throw new Error('navigazione fallita');
  await tool('browser_wait_for', { time: 3 });
  const shots = [];
  const shot = async (name, extra = {}) => { const r = await tool('browser_take_screenshot', { type: 'jpeg', filename: name, ...extra }); shots.push(name + (r.error ? ' (ERRORE)' : '')); };
  await shot(`${domain}-viewport.jpeg`);
  const height = result((await tool('browser_evaluate', { function: '() => document.documentElement.scrollHeight' })).text);
  say(`altezza pagina: ${height}px`);
  const motion = result((await tool('browser_evaluate', { function: `async () => {
    const H = document.documentElement.scrollHeight, out = [];
    for (let y = 0; y <= H; y += Math.round(innerHeight * 0.75)) {
      window.scrollTo(0, y); await new Promise(r => setTimeout(r, 450));
      const a = document.getAnimations();
      const hidden = [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); if (r.bottom < 0 || r.top > innerHeight || r.width < 40 || r.height < 20) return false; const s = getComputedStyle(e); return parseFloat(s.opacity) < 0.2 && (e.innerText || '').trim().length > 0; }).length;
      out.push({ y, animazioni: a.length, nomi: [...new Set(a.map(x => x.animationName || x.transitionProperty || 'web-animation'))].slice(0, 5), testoNonAncoraVisibile: hidden });
    }
    window.scrollTo(0, 0);
    const vids = [...document.querySelectorAll('video')].map(v => ({ autoplay: v.autoplay, muted: v.muted, loop: v.loop, w: v.clientWidth, h: v.clientHeight }));
    const sticky = [...document.querySelectorAll('body *')].filter(e => ['sticky', 'fixed'].includes(getComputedStyle(e).position) && e.getBoundingClientRect().height > 20).map(e => e.tagName.toLowerCase() + '.' + String(e.className).split(' ')[0]).slice(0, 8);
    const libs = { gsap: !!window.gsap, lenis: !!window.lenis || !!document.querySelector('.lenis'), swiper: !!document.querySelector('.swiper'), canvas: document.querySelectorAll('canvas').length };
    return { campioni: out, video: vids, elementiFissi: sticky, librerie: libs };
  }` })).text);
  if (height <= 5400) await shot(`${domain}-fullpage.jpeg`, { fullPage: true });
  else {
    await tool('browser_evaluate', { function: '() => window.scrollTo(0, document.documentElement.scrollHeight * 0.5)' });
    await tool('browser_wait_for', { time: 1 }); await shot(`${domain}-mid.jpeg`);
    await tool('browser_evaluate', { function: '() => window.scrollTo(0, document.documentElement.scrollHeight)' });
    await tool('browser_wait_for', { time: 1 }); await shot(`${domain}-footer.jpeg`);
    await tool('browser_evaluate', { function: '() => window.scrollTo(0, 0)' });
  }
  // Estrattore DOM di Taste, passato per intero come chiede SKILL.md.
  const extractor = fs.readFileSync(path.join(ROOT, 'skills/taste/references/extract.js'), 'utf8').replace(/;\s*$/, '');
  const ex = await tool('browser_evaluate', { function: extractor });
  const domData = result(ex.text);
  fs.writeFileSync(path.join(out, `${domain}.dom.json`), JSON.stringify(domData, null, 2));
  say(`extract.js: ${ex.error ? 'ERRORE ' + ex.text.slice(0, 300) : (typeof domData === 'object' ? 'ok' : 'risultato non JSON')}`);
  await tool('browser_resize', { width: 390, height: 844 });
  await tool('browser_navigate', { url });
  await tool('browser_wait_for', { time: 3 });
  await shot(`${domain}-mobile-390.jpeg`);
  fs.writeFileSync(path.join(out, `${domain}.capture.json`), JSON.stringify({ url, domain, title, height, shots, motion, log, when: new Date().toISOString() }, null, 2));
  say(`file in ${out}: ${shots.join(', ')}`);
  await tool('browser_close', {});
} catch (e) {
  say('ERRORE: ' + e.message); process.exitCode = 1;
} finally {
  proc.kill();
  setTimeout(() => process.exit(), 300);
}

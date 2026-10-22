#!/usr/bin/env node
// Guardia di rete per l'analisi dei siti di riferimento (Taste). Unica uscita del browser:
// - navigazione esterna consentita solo su 80/443 e solo GET/HEAD in chiaro;
// - sempre negati: domini protetti (config domini_protetti, con i sottodomini), localhost, loopback, reti private
//   e qualunque nome che risolva verso questi indirizzi (la guardia risolve i nomi da sé e si collega all'IP verificato);
// - registro di ogni tentativo in <lavoro>/.stato/taste/guardia.log.
// Uso: node guardia-riferimenti.mjs [--test]   (--test: politica di prova, all'esterno solo example.com)
import http from 'node:http';
import net from 'node:net';
import dns from 'node:dns/promises';
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { decide } from './policy-lib.mjs';
import { politica } from './politica.mjs';

const require = createRequire(import.meta.url);
const { stato } = require('../lib/config.cjs');
const policy = politica({ test: process.argv.includes('--test') });
const logFile = path.join(stato('taste'), 'guardia.log');
fs.mkdirSync(path.dirname(logFile), { recursive: true });
const log = entry => fs.appendFileSync(logFile, JSON.stringify({ t: new Date().toISOString(), policy: policy.name, ...entry }) + '\n');

async function resolve(host) {
  if (net.isIP(host)) return [host];
  try { return (await dns.lookup(host, { all: true, verbatim: true })).map(a => a.address); } catch { return []; }
}

const server = http.createServer(async (req, res) => {
  if (!/^http:\/\//i.test(req.url)) {
    if (req.url === '/__guard/health') { res.writeHead(200, { 'content-type': 'application/json' }); res.end(JSON.stringify({ ok: true, policy: policy.name, mode: policy.mode })); return; }
    res.writeHead(404); res.end(); return;
  }
  let url;
  try { url = new URL(req.url); } catch { res.writeHead(400); res.end(); return; }
  const host = url.hostname.replace(/^\[|\]$/g, '');
  const port = Number(url.port || 80);
  // Prima le regole che non richiedono DNS: un dominio vietato non viene nemmeno risolto.
  let addresses = [];
  let d = decide(policy, { method: req.method, host, port, path: url.pathname, addresses: null });
  if (d.needsResolve) { addresses = await resolve(host); d = decide(policy, { method: req.method, host, port, path: url.pathname, addresses }); }
  log({ kind: 'http', method: req.method, target: `${host}:${port}`, path: url.pathname, addresses, decision: d.allow ? 'ALLOW' : 'DENY', reason: d.reason });
  if (!d.allow) { res.writeHead(403, { 'content-type': 'text/plain', 'x-guard': 'denied' }); res.end('Bloccato dalla guardia dei riferimenti: ' + d.reason); return; }
  const headers = { ...req.headers }; delete headers['proxy-connection'];
  const up = http.request({ host: net.isIP(host) ? host : addresses[0], port, method: req.method, path: url.pathname + url.search, headers }, r => { res.writeHead(r.statusCode, r.headers); r.pipe(res); });
  up.on('error', () => { if (!res.headersSent) res.writeHead(502); res.end(); });
  req.pipe(up);
});

server.on('connect', async (req, socket, head) => {
  socket.on('error', () => {});
  const raw = String(req.url);
  const i = raw.lastIndexOf(':');
  const host = raw.slice(0, i).replace(/^\[|\]$/g, '').toLowerCase();
  const port = Number(raw.slice(i + 1));
  let addresses = [];
  let d = decide(policy, { method: 'CONNECT', host, port, addresses: null });
  if (d.needsResolve) { addresses = await resolve(host); d = decide(policy, { method: 'CONNECT', host, port, addresses }); }
  log({ kind: 'connect', method: 'CONNECT', target: `${host}:${port}`, addresses, decision: d.allow ? 'ALLOW' : 'DENY', reason: d.reason });
  if (!d.allow) { socket.end('HTTP/1.1 403 Forbidden\r\nX-Guard: denied\r\n\r\n'); return; }
  const up = net.connect(port, net.isIP(host) ? host : addresses[0], () => {
    socket.write('HTTP/1.1 200 Connection Established\r\n\r\n');
    if (head.length) up.write(head);
    up.pipe(socket); socket.pipe(up);
  });
  up.on('error', () => socket.destroy());
  socket.on('close', () => up.destroy());
});

server.listen(policy.proxyPort, '127.0.0.1', () => {
  log({ kind: 'start', mode: policy.mode });
  console.log(`guardia dei riferimenti su 127.0.0.1:${policy.proxyPort} (politica ${policy.name}, modalità ${policy.mode})`);
});

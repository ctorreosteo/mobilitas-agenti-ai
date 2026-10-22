#!/usr/bin/env node
// Guardia di rete per i test visivi (proxy su 127.0.0.1). È l'unica uscita del browser automatico:
// consente solo le destinazioni elencate (di norma il server di prova del sito), solo GET e HEAD, mai /api/.
// Tutto il resto viene rifiutato e registrato. Se la guardia è spenta il browser non raggiunge nulla
// (gli script di test rifiutano di partire).
//
// Uso: node guardia-locale.mjs --porta 8910 --consenti localhost:5310[,127.0.0.1:5310] [--log file] [--canarino 8999]
//   --canarino avvia anche un server "canarino" (mai consentito) per i controlli negativi: ogni richiesta
//   che gli arriva è una protezione fallita e viene registrata in <log>.canarino.
import http from 'node:http';
import net from 'node:net';
import fs from 'node:fs';
import path from 'node:path';

const a = {};
for (let i = 2; i < process.argv.length; i += 2) a[process.argv[i].replace(/^--/, '')] = process.argv[i + 1];
const porta = Number(a.porta);
if (!porta || !a.consenti) { console.error('uso: guardia-locale.mjs --porta <n> --consenti host:porta[,host:porta] [--log file] [--canarino porta]'); process.exit(2); }
const allow = new Set(a.consenti.split(',').map(s => s.trim().toLowerCase()).filter(Boolean));
const methods = new Set(['GET', 'HEAD']);
const denyPaths = ['/api/'];
const logFile = path.resolve(a.log || 'guardia.log');
fs.mkdirSync(path.dirname(logFile), { recursive: true });
const log = (entry, file = logFile) => fs.appendFileSync(file, JSON.stringify({ t: new Date().toISOString(), ...entry }) + '\n');

const proxy = http.createServer((req, res) => {
  if (!/^http:\/\//i.test(req.url)) {
    if (req.url === '/__guard/health') {
      res.writeHead(200, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ ok: true, guardia: 'locale', allow: [...allow], methods: [...methods] }));
      return;
    }
    res.writeHead(404); res.end(); return;
  }
  let url;
  try { url = new URL(req.url); } catch { log({ kind: 'http', method: req.method, target: 'invalid', decision: 'DENY' }); res.writeHead(400); res.end(); return; }
  const target = `${url.hostname}:${url.port || 80}`.toLowerCase();
  const allowed = allow.has(target) && methods.has(req.method) && !denyPaths.some(p => url.pathname.startsWith(p));
  log({ kind: 'http', method: req.method, target, path: url.pathname, decision: allowed ? 'ALLOW' : 'DENY' });
  if (!allowed) { res.writeHead(403, { 'content-type': 'text/plain', 'x-guard': 'denied' }); res.end('Bloccato dalla guardia di rete WebDesigner'); return; }
  const headers = { ...req.headers }; delete headers['proxy-connection'];
  const up = http.request({ host: url.hostname, port: url.port || 80, method: req.method, path: url.pathname + url.search, headers }, r => { res.writeHead(r.statusCode, r.headers); r.pipe(res); });
  up.on('error', () => { if (!res.headersSent) res.writeHead(502); res.end(); });
  req.pipe(up);
});

// HTTPS e WebSocket arrivano come CONNECT host:porta (il server di sviluppo usa il WebSocket per l'aggiornamento a caldo).
proxy.on('connect', (req, socket, head) => {
  const target = String(req.url).toLowerCase();
  const allowed = allow.has(target);
  log({ kind: 'connect', method: 'CONNECT', target, decision: allowed ? 'ALLOW' : 'DENY' });
  socket.on('error', () => {});
  if (!allowed) { socket.end('HTTP/1.1 403 Forbidden\r\nX-Guard: denied\r\n\r\n'); return; }
  const i = target.lastIndexOf(':');
  const up = net.connect(Number(target.slice(i + 1)), target.slice(0, i).replace(/^\[|\]$/g, ''), () => {
    socket.write('HTTP/1.1 200 Connection Established\r\n\r\n');
    if (head.length) up.write(head);
    up.pipe(socket); socket.pipe(up);
  });
  up.on('error', () => socket.destroy());
  socket.on('close', () => up.destroy());
});

proxy.listen(porta, '127.0.0.1', () => {
  log({ kind: 'start', allow: [...allow] });
  console.log(`guardia di rete su 127.0.0.1:${porta}; consentiti: ${[...allow].join(', ')}`);
});

if (a.canarino) {
  const canary = http.createServer((req, res) => {
    log({ kind: 'request', method: req.method, path: req.url }, logFile + '.canarino');
    res.writeHead(200, { 'content-type': 'text/plain', 'access-control-allow-origin': '*' }); res.end('CANARINO');
  });
  canary.on('upgrade', (req, socket) => { log({ kind: 'upgrade', path: req.url }, logFile + '.canarino'); socket.destroy(); });
  canary.listen(Number(a.canarino), '127.0.0.1', () => console.log(`canarino su 127.0.0.1:${a.canarino} (mai consentito)`));
}

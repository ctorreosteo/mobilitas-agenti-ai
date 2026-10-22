// Politica della guardia dei riferimenti, costruita dalla configurazione (unica fonte dei domini protetti).
//   riferimenti: navigazione esterna consentita (80/443, GET/HEAD), tranne domini protetti, loopback e reti private;
//   test: stesse regole, ma all'esterno passa soltanto example.com e in locale solo la pagina di prova indicata.
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { carica, prendi } = require('../lib/config.cjs');

export function politica({ test = false, paginaProva = '127.0.0.1:8796' } = {}) {
  const cfg = carica();
  const base = {
    proxyPort: Number(prendi(cfg, 'porte.guardia_riferimenti') || 8990),
    allowPorts: [80, 443],
    methods: ['GET', 'HEAD'],
    denyHosts: (cfg.domini_protetti || []).map(d => String(d).toLowerCase()),
  };
  return test
    ? { ...base, name: 'test', mode: 'allowlist', allowHosts: ['example.com'], allowLocal: [paginaProva] }
    : { ...base, name: 'riferimenti', mode: 'denylist', allowLocal: [] };
}

// Verifica offline delle decisioni della guardia dei riferimenti (nessuna richiesta di rete).
// La politica viene costruita dalla configurazione (domini_protetti), come in esercizio.
import { decide } from '../tools/taste/policy-lib.mjs';
import { politica } from '../tools/taste/politica.mjs';

const rif = politica();
const test = politica({ test: true, paginaProva: '127.0.0.1:8796' });
const pub = ['93.184.215.14'];
const cases = [
  [rif, 'sito di riferimento HTTPS', { method: 'CONNECT', host: 'www.awwwards.com', port: 443, addresses: pub }, true],
  [rif, 'sito di riferimento HTTP GET', { method: 'GET', host: 'example.org', port: 80, addresses: pub }, true],
  [rif, 'POST in chiaro', { method: 'POST', host: 'example.org', port: 80, addresses: pub }, false],
  [rif, 'porta non standard', { method: 'CONNECT', host: 'example.org', port: 8443, addresses: pub }, false],
  [rif, 'localhost:5173', { method: 'GET', host: 'localhost', port: 5173, addresses: null }, false],
  [rif, '127.0.0.1:5310', { method: 'GET', host: '127.0.0.1', port: 5310, addresses: null }, false],
  [rif, '[::1]', { method: 'GET', host: '::1', port: 80, addresses: null }, false],
  [rif, '0.0.0.0', { method: 'GET', host: '0.0.0.0', port: 80, addresses: null }, false],
  [rif, 'rete locale 192.168.1.20', { method: 'GET', host: '192.168.1.20', port: 80, addresses: null }, false],
  [rif, 'rete locale 10.0.0.5', { method: 'CONNECT', host: '10.0.0.5', port: 443, addresses: null }, false],
  [rif, 'IPv4 in IPv6 ::ffff:127.0.0.1', { method: 'GET', host: '::ffff:127.0.0.1', port: 80, addresses: null }, false],
  [rif, 'nome pubblico che risolve a 127.0.0.1', { method: 'CONNECT', host: 'localtest.me', port: 443, addresses: ['127.0.0.1'] }, false],
  [rif, 'nome che risolve anche alla rete locale', { method: 'CONNECT', host: 'evil.example', port: 443, addresses: ['93.184.215.14', '192.168.1.20'] }, false],
  [rif, 'nome non risolto', { method: 'CONNECT', host: 'nonexistent.invalid', port: 443, addresses: [] }, false],
  [test, 'test: pagina di prova locale', { method: 'GET', host: '127.0.0.1', port: 8796, addresses: null }, true],
  [test, 'test: altra porta locale', { method: 'GET', host: '127.0.0.1', port: 8797, addresses: null }, false],
  [test, 'test: example.com', { method: 'CONNECT', host: 'example.com', port: 443, addresses: pub }, true],
  [test, 'test: qualsiasi altro sito', { method: 'CONNECT', host: 'www.awwwards.com', port: 443, addresses: pub }, false],
];
// Ogni dominio protetto della configurazione: radice, www, sottodominio, maiuscole con punto finale. Più un dominio simile ma diverso.
for (const d of rif.denyHosts) {
  for (const h of [d, 'www.' + d, 'qualcosa.' + d, d.toUpperCase() + '.']) cases.push([rif, `protetto: ${h}`, { method: 'CONNECT', host: h, port: 443, addresses: pub }, false]);
  cases.push([test, `test, protetto prima della lista: ${d}`, { method: 'CONNECT', host: d, port: 443, addresses: pub }, false]);
}
if (rif.denyHosts.length) cases.push([rif, 'dominio simile ma diverso', { method: 'CONNECT', host: 'non' + rif.denyHosts[0], port: 443, addresses: pub }, true]);

let ok = 0;
for (const [policy, label, target, expected] of cases) {
  let d = decide(policy, target);
  if (d.needsResolve) d = decide(policy, { ...target, addresses: pub });
  const pass = d.allow === expected;
  if (pass) ok++;
  console.log(`${pass ? 'OK  ' : 'FAIL'} [${policy.name}] ${label} -> ${d.allow ? 'consentito' : 'negato'} (${d.reason})`);
}
console.log(`\n${ok}/${cases.length} casi corretti`);
process.exit(ok === cases.length ? 0 : 1);

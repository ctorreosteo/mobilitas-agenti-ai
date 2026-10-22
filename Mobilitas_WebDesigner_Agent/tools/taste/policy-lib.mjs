// Decisioni del proxy di guardia Taste. Funzione pura, verificabile senza rete.
import net from 'node:net';

const PRIVATE_V4 = [
  ['0.0.0.0', 8], ['10.0.0.0', 8], ['100.64.0.0', 10], ['127.0.0.0', 8], ['169.254.0.0', 16],
  ['172.16.0.0', 12], ['192.168.0.0', 16], ['198.18.0.0', 15], ['224.0.0.0', 4], ['240.0.0.0', 4],
];
const toInt = ip => ip.split('.').reduce((a, b) => (a << 8) + Number(b), 0) >>> 0;

export function isPrivateAddress(ip) {
  if (net.isIPv4(ip)) {
    const n = toInt(ip);
    return PRIVATE_V4.some(([base, bits]) => (n & (bits === 0 ? 0 : (~0 << (32 - bits)) >>> 0)) === (toInt(base) & ((~0 << (32 - bits)) >>> 0)));
  }
  if (net.isIPv6(ip)) {
    const v = ip.toLowerCase();
    if (v === '::' || v === '::1') return true;
    if (v.startsWith('::ffff:')) return isPrivateAddress(v.slice(7));
    return /^(fc|fd|fe8|fe9|fea|feb|ff)/.test(v);
  }
  return true; // indirizzo non riconosciuto: trattato come privato, quindi negato
}

const hostMatches = (host, rule) => host === rule || host.endsWith('.' + rule);

// target: { method, host, port, path, addresses: [ip...] } — addresses = risoluzione DNS fatta dal proxy.
export function decide(policy, target) {
  const host = String(target.host || '').toLowerCase().replace(/^\[|\]$/g, '').replace(/\.$/, '');
  const port = Number(target.port);
  const key = `${host}:${port}`;
  if ((policy.allowLocal || []).includes(key))
    return { allow: true, reason: 'origine di test consentita' };
  if (['localhost', 'localhost.localdomain'].includes(host) || host.endsWith('.localhost'))
    return { allow: false, reason: 'loopback (localhost)' };
  if (net.isIP(host) && isPrivateAddress(host))
    return { allow: false, reason: 'indirizzo privato o loopback' };
  const denied = (policy.denyHosts || []).find(rule => hostMatches(host, rule));
  if (denied)
    return { allow: false, reason: `dominio vietato (${denied})` };
  if (!(policy.allowPorts || [80, 443]).includes(port))
    return { allow: false, reason: `porta ${port} non consentita` };
  if (target.method && target.method !== 'CONNECT' && !(policy.methods || ['GET', 'HEAD']).includes(target.method))
    return { allow: false, reason: `metodo ${target.method} non consentito` };
  if (policy.mode === 'allowlist' && !(policy.allowHosts || []).some(rule => hostMatches(host, rule)))
    return { allow: false, reason: 'fuori dalla lista consentita (modalità test)' };
  if (target.addresses === null)
    return { allow: true, needsResolve: true, reason: 'da risolvere' };
  if ((target.addresses || []).some(isPrivateAddress))
    return { allow: false, reason: 'il nome risolve verso un indirizzo privato o loopback' };
  if (!net.isIP(host) && !(target.addresses || []).length)
    return { allow: false, reason: 'nome non risolto' };
  return { allow: true, reason: 'consentito' };
}

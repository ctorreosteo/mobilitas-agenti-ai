// Protezione iniettata SOLO nel browser di prova (Playwright addInitScript), prima di qualunque script della pagina.
// Non fa parte delle landing: il codice del sito resta quello reale, con le sue integrazioni. Durante le prove impedisce
// che partano dati verso servizi reali (gestionale, tracciamento), qualunque componente venga eseguito:
//   - fetch e XMLHttpRequest: solo letture GET/HEAD verso la stessa origine, mai /api/;
//   - sendBeacon bloccato; invio nativo dei moduli bloccato (i gestori React continuano a funzionare);
//   - WebSocket solo verso la stessa origine (aggiornamento a caldo del server di sviluppo);
//   - fbq, gtag, clarity predefiniti come funzioni vuote modificabili: lo snippet del Meta Pixel non si carica,
//     gli altri script di tracciamento possono definirsi ma le loro richieste vengono fermate dalla guardia di rete.
// I tentativi bloccati restano in window.__testGuard.blocked, letti dai controlli.
(() => {
  const blocked = [];
  const record = (kind, detail) => { blocked.push({ kind, detail: String(detail).slice(0, 200), at: Date.now() }); };
  const sameOriginRead = (method, url) => {
    let t; try { t = new URL(url, location.href); } catch { return false; }
    if (t.protocol === 'data:' || t.protocol === 'blob:') return true;
    return ['GET', 'HEAD'].includes(String(method || 'GET').toUpperCase()) && t.origin === location.origin && !t.pathname.startsWith('/api/');
  };
  for (const name of ['fbq', 'gtag', 'clarity']) {
    Object.defineProperty(window, name, { value: function testNoop(...args) { record(name, args.map(a => (typeof a === 'string' ? a : typeof a)).join(', ')); }, writable: true, configurable: true });
  }
  const nativeFetch = window.fetch.bind(window);
  window.fetch = (input, init = {}) => {
    const url = typeof input === 'string' || input instanceof URL ? String(input) : input.url;
    const method = init.method || (typeof input === 'object' && 'method' in input ? input.method : 'GET');
    if (!sameOriginRead(method, url)) { record(`fetch ${String(method).toUpperCase()}`, url); return Promise.reject(new TypeError('[prova] richiesta bloccata: nessun dato verso servizi reali durante i test')); }
    return nativeFetch(input, init);
  };
  const nativeOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method, url, ...rest) {
    if (!sameOriginRead(method, url)) { record(`xhr ${String(method).toUpperCase()}`, url); throw new DOMException('[prova] richiesta bloccata', 'SecurityError'); }
    return nativeOpen.call(this, method, url, ...rest);
  };
  if (navigator.sendBeacon) navigator.sendBeacon = url => { record('sendBeacon', url); return false; };
  const NativeWS = window.WebSocket;
  window.WebSocket = function (url, protocols) {
    let t; try { t = new URL(url, location.href); } catch { t = null; }
    if (!t || t.host !== location.host) { record('websocket', url); throw new DOMException('[prova] WebSocket bloccato', 'SecurityError'); }
    return new NativeWS(url, protocols);
  };
  window.WebSocket.prototype = NativeWS.prototype;
  Object.assign(window.WebSocket, { CONNECTING: 0, OPEN: 1, CLOSING: 2, CLOSED: 3 });
  document.addEventListener('submit', e => { e.preventDefault(); record('submit nativo', e.target?.getAttribute?.('action') || '(senza action)'); }, true);
  Object.defineProperty(window, '__testGuard', { value: Object.freeze({ active: true, blocked }), configurable: false });
})();

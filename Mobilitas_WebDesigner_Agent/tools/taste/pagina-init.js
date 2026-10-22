// Eseguito in ogni pagina prima dei suoi script (browser.initScript di Playwright MCP).
// Le pagine analizzate da Taste vengono solo lette: nessuna scrittura verso server.
(() => {
  const blocked = [];
  const note = (kind, url) => { blocked.push({ kind, url: String(url).slice(0, 160) }); };
  const readOnly = m => ['GET', 'HEAD'].includes(String(m || 'GET').toUpperCase());
  const nativeFetch = window.fetch;
  window.fetch = function (input, init) {
    const method = (init && init.method) || (input && typeof input === 'object' && 'method' in input ? input.method : 'GET');
    if (!readOnly(method)) { note('fetch ' + method, typeof input === 'string' ? input : input && input.url); return Promise.reject(new TypeError('[taste] richiesta di scrittura bloccata')); }
    return nativeFetch.apply(this, arguments);
  };
  const nativeOpen = XMLHttpRequest.prototype.open;
  XMLHttpRequest.prototype.open = function (method, url) {
    if (!readOnly(method)) { note('xhr ' + method, url); throw new DOMException('[taste] richiesta di scrittura bloccata', 'SecurityError'); }
    return nativeOpen.apply(this, arguments);
  };
  if (navigator.sendBeacon) navigator.sendBeacon = url => { note('sendBeacon', url); return false; };
  document.addEventListener('submit', e => { e.preventDefault(); note('submit', e.target && e.target.action); }, true);
  Object.defineProperty(window, '__tasteGuard', { value: Object.freeze({ active: true, blocked }), configurable: false });
})();

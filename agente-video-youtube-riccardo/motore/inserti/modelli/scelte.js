// Due scelte una sotto l'altra sul pannello: ciascuna si accende quando la dice.
// DATI: lato, scelte [{t, domanda, risposta}]
const lato = D.lato || 'dx';
const p = pannello(lato);
muoviPannello(p, lato);
const box = el('div', 'scelte', p);
const FRECCIA = '<svg viewBox="0 0 54 30"><path d="M3 15 H47 M35 4 L49 15 L35 26" fill="none" ' +
  'stroke="rgba(244,244,244,0.45)" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>';
(D.scelte || []).forEach((s, i) => {
  const c = el('div', 'scelta', box);
  el('div', 'domanda', c, esc(s.domanda));
  const r = el('div', 'risposta', c, FRECCIA + '<span class="rr">' + esc(s.risposta) + '</span>');
  const t = Math.max(0.2, s.t || 0);
  tl.fromTo(c, { opacity: 0, y: 30 }, { opacity: 0.5, y: 0, duration: 0.4, ease: 'power3.out' }, i === 0 ? 0.2 : 0.35);
  tl.to(c, { opacity: 1, borderColor: 'rgba(114,250,147,0.9)', duration: 0.35 }, t);
  tl.to(r.querySelector('.rr'), { color: '#72FA93', fontWeight: 800, duration: 0.3 }, t + 0.25);
  tl.to(r.querySelector('path'), { attr: { stroke: '#72FA93' }, duration: 0.3 }, t + 0.25);
  molla(c, t + 0.25);
});
chiudi();

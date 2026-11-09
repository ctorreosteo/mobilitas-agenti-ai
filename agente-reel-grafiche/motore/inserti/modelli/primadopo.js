// Prima/dopo: le due foto affiancate su blu profondo, con la linea posturale
// (orecchio-spalla-anca-ginocchio-caviglia, punti di Apple Vision) e la verticale
// dalla caviglia. A schermo solo le etichette PRIMA e DOPO.
// DATI: prima/dopo {src, w, h, punti [[x,y,conf] x5]}, etichette {prima: {testo}, dopo: {testo}}
const NS = 'http://www.w3.org/2000/svg';
// D.entra / D.esce false: si entra o si esce a taglio netto (un pannello e appena
// uscito o sta per entrare: niente dissolvenza sopra un'altra inquadratura)
if (D.entra !== false) tl.fromTo(SCENA, { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0);
if (D.esce !== false) tl.to(SCENA, { opacity: 0, duration: 0.3 }, T - 0.32);
const H = 860;
const lati = [D.prima, D.dopo];
const larg = lati.map((f) => Math.round(H * f.w / f.h));
const gap = 40;
let x0 = Math.round((1920 - larg[0] - larg[1] - gap) / 2);
['prima', 'dopo'].forEach((k, i) => {
  const f = D[k];
  const box = el('div', 'foto');
  box.style.left = x0 + 'px';
  box.style.width = larg[i] + 'px';
  const im = el('img', '', box);
  im.src = f.src;
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', `0 0 ${larg[i]} ${H}`);
  box.appendChild(svg);
  const pts = f.punti.filter((q) => q).map(([x, y]) => [x * larg[i], y * H]);
  const ax = pts[pts.length - 1][0];
  const v = document.createElementNS(NS, 'line');
  Object.entries({ x1: ax, y1: pts[0][1] - 40, x2: ax, y2: pts[pts.length - 1][1], stroke: '#F4F4F4',
    'stroke-width': 3, 'stroke-dasharray': '10 9', opacity: 0.9 }).forEach(([a, b]) => v.setAttribute(a, b));
  svg.appendChild(v);
  const pl = document.createElementNS(NS, 'polyline');
  pl.setAttribute('points', pts.map((q) => q.join(',')).join(' '));
  Object.entries({ fill: 'none', stroke: '#002552', 'stroke-width': 7, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' })
    .forEach(([a, b]) => pl.setAttribute(a, b));
  svg.appendChild(pl);
  let lun = 0;
  for (let j = 1; j < pts.length; j++) lun += Math.hypot(pts[j][0] - pts[j - 1][0], pts[j][1] - pts[j - 1][1]);
  pl.setAttribute('stroke-dasharray', lun);
  const cerchi = pts.map(([x, y]) => {
    const c = document.createElementNS(NS, 'circle');
    Object.entries({ cx: x, cy: y, r: 10, fill: '#002552', stroke: '#F4F4F4', 'stroke-width': 4 }).forEach(([a, b]) => c.setAttribute(a, b));
    svg.appendChild(c);
    return c;
  });
  const lab = el('div', 'lab', box, esc((D.etichette && D.etichette[k] && D.etichette[k].testo) || k.toUpperCase()));
  // dopo un taglio netto (entra false) le foto arrivano subito: niente schermo blu vuoto
  const t = (D.entra === false ? 0.0 : 0.25) + i * 0.3;
  tl.fromTo(box, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.45, ease: 'power3.out' }, t);
  tl.fromTo(v, { opacity: 0 }, { opacity: 0.9, duration: 0.3 }, t + 0.35);
  tl.fromTo(pl, { attr: { 'stroke-dashoffset': lun } }, { attr: { 'stroke-dashoffset': 0 }, duration: 0.6, ease: 'power2.inOut' }, t + 0.4);
  cerchi.forEach((c, j) => tl.fromTo(c, { opacity: 0 }, { opacity: 1, duration: 0.15 }, t + 0.4 + j * 0.1));
  entra(lab, t + 0.2, 10);
  x0 += larg[i] + gap;
});
chiudi();

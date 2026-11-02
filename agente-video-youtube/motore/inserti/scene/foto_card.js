// Foto vera in una card (fase 7b rivista): una foto di `libreria/prima-dopo` con il
// consenso nel catalogo, il viso tagliato fuori dal motore (`ritaglio`). Card blu
// come quella della colonna; la foto avanza piano (1,04 -> 1); anelli verdi
// luminosi che si disegnano sulle parole. Nessun testo sulla foto (solo PRIMA e
// DOPO sarebbero ammessi).
// d: x, y, larghezza, altezza, raggio, src, w, h (foto gia ritagliata, in px della card),
//    anelli [{cx, cy, rx, ry, t}] (px della card), avanza
MODELLI.foto_card = function (box, x, d) {
  const k = el('div', 'fc', box);
  px(k, { left: d.x, top: d.y, width: d.larghezza, height: d.altezza, borderRadius: d.raggio || 34 });
  const fw = el('div', 'fc-foto', k);
  const im = el('img', '', fw);
  im.src = d.src;
  px(im, { width: d.w, height: d.h, left: (d.larghezza - d.w) / 2, top: (d.altezza - d.h) / 2 });
  el('div', 'fc-velo', k);
  gsap.set(k, { opacity: 0, scale: 0.92, y: 40, filter: 'blur(12px)' });
  tl.to(k, { opacity: 1, duration: 5 * FR, ease: 'power1.out' }, x.s);
  tl.to(k, { scale: 1, y: 0, filter: 'blur(0px)', duration: 8 * FR, ease: 'power3.out' }, x.s);
  if (d.avanza !== false) tl.fromTo(im, { scale: 1.06 }, { scale: 1.0, duration: Math.max(0.5, x.e - x.s), ease: 'none' }, x.s);
  const S = svg('svg', { viewBox: `0 0 ${d.larghezza} ${d.altezza}`, width: d.larghezza, height: d.altezza, class: 'fc-svg' }, k);
  (d.anelli || []).forEach((a) => {
    // sotto l'anello un contorno blu profondo: il verde poggia sul blu (regola del brand)
    const b = svg('ellipse', { cx: a.cx, cy: a.cy, rx: a.rx, ry: a.ry, fill: 'none', 'stroke-width': 13,
      pathLength: 1, 'stroke-dasharray': '1 1', class: 'fc-sotto' }, S);
    const e = svg('ellipse', { cx: a.cx, cy: a.cy, rx: a.rx, ry: a.ry, fill: 'none', stroke: '#72FA93', 'stroke-width': 6,
      pathLength: 1, 'stroke-dasharray': '1 1', class: 'fc-anello' }, S);
    [b, e].forEach((n) => { gsap.set(n, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(n, { attr: { 'stroke-dashoffset': 0 }, duration: 14 * FR, ease: 'power2.out' }, a.t); });
  });
  tl.to(k, { opacity: 0, scale: 0.97, filter: 'blur(6px)', duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
};

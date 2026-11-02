// Connettore (campionario v3, reference gadzhi-11): due cose dette che vanno insieme,
// basse, una a sinistra e una a destra di lui, unite da una linea luminosa che si disegna
// dal centro verso i due capi; al centro, sul busto (mai sul volto), nasce un nodo con
// due anelli intrecciati e sotto le sue parole. Il fondo si scurisce di blu dal basso
// (effetto di piatto `velo`). Esce al contrario.
// d: y, xs, xd, sinistra [righe], t_sx, destra [righe], t_dx, t_linea, pp {testo, t}, t_via
MODELLI.connettore = function (box, x, d) {
  const Y = d.y || 860, xs = d.xs || 760, xd = d.xd || 1160, xm = (xs + xd) / 2;
  const scrivi = (righe, t0, seme, sx) => {
    const e = el('div', 'cn-et v3-pezzo' + (sx ? ' cn-sx' : ''), box);
    const h = righe.length * 70;
    px(e, sx ? { left: xs - 760, width: 760, top: Y - h / 2 - 4 } : { left: xd, top: Y - h / 2 - 4 });
    righe.forEach((r, i) => {
      const rr = el('div', 'cn-r', e);
      const v = decifra(rr, r, t0 + i * 3 * FR, 8, seme + i);
      cancella(rr, v, r, d.t_via + 4 * FR, 5);
    });
  };
  scrivi(d.sinistra, d.t_sx, 300, true);
  scrivi(d.destra, d.t_dx, 310, false);
  const S = svg('svg', { width: 1920, height: 1080, viewBox: '0 0 1920 1080', class: 'cn-svg' }, box);
  [[xm - 52, xs + 24], [xm + 52, xd - 24]].forEach(([a, b]) => {
    const l = svg('line', { x1: a, y1: Y, x2: b, y2: Y, stroke: '#A9FFBE', 'stroke-width': 6, 'stroke-linecap': 'round', class: 'cn-linea' }, S);
    gsap.set(l, { scaleX: 0, transformOrigin: `${a}px ${Y}px` });
    tl.to(l, { scaleX: 1, duration: 6 * FR, ease: 'power3.out' }, d.t_linea);
    tl.to(l, { scaleX: 0, duration: 4 * FR, ease: 'power2.in' }, d.t_via);
  });
  const nodo = el('div', 'cn-nodo v3-pezzo', box);
  px(nodo, { left: xm, top: Y });
  const ic = svg('svg', { viewBox: '0 0 54 54', class: 'cn-ico' }, nodo);
  [[20, 27], [34, 27]].forEach(([cx, cy]) => svg('circle', { cx, cy, r: 13, fill: 'none', stroke: '#A9FFBE', 'stroke-width': 4 }, ic));
  gsap.set(nodo, { scale: 0, opacity: 0 });
  tl.to(nodo, { scale: 1, opacity: 1, duration: 4 * FR, ease: 'back.out(2)' }, d.t_linea + 4 * FR);
  tl.to(nodo, { scale: 0, opacity: 0, duration: 3 * FR, ease: 'power2.in' }, d.t_via - 2 * FR);
  if (d.pp) {
    const pp = el('div', 'cn-pp v3-pezzo', box);
    px(pp, { left: xm, top: Y + 86 });
    const v = decifra(pp, d.pp.testo, d.pp.t - FR, 9, 330);
    cancella(pp, v, d.pp.testo, d.t_via - 4 * FR, 5);
  }
};

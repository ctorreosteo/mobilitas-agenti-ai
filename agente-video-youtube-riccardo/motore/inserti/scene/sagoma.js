// Sagoma posturale di profilo (fase 7b), dentro un "vetro" scuro: e il riflesso di
// chi guarda, la sera, nella finestra. Forme semplici (non anatomia, non un
// paziente): il profilo viene dal motore (`anatomia.PROFILO`), con la pancia che
// va avanti o rientra; il bacino e la schiena restano fermi (asse del bacino).
// d: x, y, larghezza, altezza (vetro), profilo [[x0,y,x1]], testa [cx,cy,r], naso, braccio,
//    bacino [[x,y],[x,y]], stati [{t, pancia, dur}], freccia {t, e}, bacino_t
MODELLI.sagoma = function (box, x, d) {
  const v = el('div', 'sg-vetro', box);
  v.setAttribute('data-motion-blur', 'off');
  px(v, { left: d.x, top: d.y, width: d.larghezza, height: d.altezza });
  el('div', 'sg-riflesso', v);
  const S = svg('svg', { viewBox: '-20 0 340 830', class: 'sg-svg' }, v);
  const col = '#3A6FA8', chiaro = '#5584B8', verde = '#72FA93';
  svg('circle', { cx: d.testa[0], cy: d.testa[1], r: d.testa[2], fill: col }, S);
  svg('path', { d: 'M' + d.naso.map((q) => q.join(' ')).join(' L') + ' Z', fill: col }, S);
  const corpo = svg('path', { fill: col }, S);
  svg('polyline', { points: d.braccio.map((q) => q.join(',')).join(' '), fill: 'none', stroke: chiaro, 'stroke-width': 34,
    'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, S);
  // Catmull-Rom chiusa, come `anatomia.liscia`
  function percorso(p) {
    const P = d.profilo.map((q) => [q[0] + (q[2] - q[0]) * p, q[1]]);
    const n = P.length;
    let s = `M${P[0][0].toFixed(1)} ${P[0][1].toFixed(1)}`;
    for (let i = 0; i < n; i++) {
      const p0 = P[(i - 1 + n) % n], p1 = P[i], p2 = P[(i + 1) % n], p3 = P[(i + 2) % n];
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      s += ` C${c1[0].toFixed(1)} ${c1[1].toFixed(1)} ${c2[0].toFixed(1)} ${c2[1].toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`;
    }
    return s + ' Z';
  }
  const stati = d.stati || [{ t: x.s, pancia: 1 }];
  tl.set(corpo, { attr: { d: percorso(stati[0].pancia) } }, 0);
  for (let i = 1; i < stati.length; i++) {
    const a = stati[i - 1].pancia, b = stati[i].pancia, n = Math.max(2, Math.round((stati[i].dur || 0.6) * FPS));
    for (let f = 1; f <= n; f++) {
      const u = f / n, e = u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
      tl.set(corpo, { attr: { d: percorso(a + (b - a) * e) } }, stati[i].t + f * FR);
    }
  }
  if (d.bacino) {
    const b = svg('line', { x1: d.bacino[0][0], y1: d.bacino[0][1], x2: d.bacino[1][0], y2: d.bacino[1][1], stroke: verde,
      'stroke-width': 7, 'stroke-linecap': 'round' }, S);
    gsap.set(b, { opacity: 0 });
    tl.to(b, { opacity: 1, duration: 8 * FR }, d.bacino_t !== undefined ? d.bacino_t : x.s + 0.4);
  }
  if (d.freccia) {
    // freccia sulla pancia: compare quando sporge, sparisce quando la tira dentro
    const f = svg('path', { d: 'M262 392 L322 392 M302 374 L324 392 L302 410', fill: 'none', stroke: verde, 'stroke-width': 9,
      'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, S);
    gsap.set(f, { opacity: 0 });
    (d.freccia.su || []).forEach((q) => tl.fromTo(f, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 10 * FR, ease: 'expo.out', immediateRender: false }, q.t));
    (d.freccia.giu || []).forEach((q) => tl.to(f, { opacity: 0, x: -20, duration: 8 * FR, ease: 'power2.in' }, q.t));
  }
  tl.fromTo(v, { opacity: 0, x: 60, rotationY: -14 }, { opacity: 1, x: 0, rotationY: -6, duration: ENTRA_GRANDE, ease: 'expo.out' }, x.s);
  tl.to(v, { opacity: 0, x: 40, duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
};

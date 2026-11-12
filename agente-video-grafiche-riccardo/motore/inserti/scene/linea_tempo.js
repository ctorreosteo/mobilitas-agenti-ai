// Linea del tempo luminosa (campionario v3, reference gadzhi-07): scena scura con il retino
// di punti; un nodo verde nasce sulla parola con il numero dentro, poi DISEGNA la linea
// mentre la percorre (scia luminosa sotto, una tacca per ogni sera che passa); la camera
// segue il nodo, inclinata, con la sfocatura di movimento, e alla fine torna larga.
// Le pillole sono le sue parole. d: y, x0, x1, nodo, num {t, sotto}, t_via, t_arrivo,
// t_largo, tacche, pillole [{testo, t, x, y}]
MODELLI.linea_tempo = function (box, x, d) {
  const fondo = el('div', 'lt-fondo v3-fondo', box);
  const retW = el('div', 'lt-ret', fondo);
  retino(retW, { w: 2600, h: 1400, passo: 18, seme: 33, verdi: 0.35, curve: [[230, 0.0024, 1.1, 0.55], [150, 0.0035, 3.0, 0.2]], larga: 160 });
  el('div', 'lt-vigna', fondo);
  const dur = x.e - x.s;
  tl.fromTo(retW, { x: 0 }, { x: -260, duration: dur, ease: 'none' }, x.s);
  gsap.set(fondo, { opacity: x.s <= FR ? 1 : 0 });
  if (x.s > FR) tl.set(fondo, { opacity: 1 }, x.s);
  const cam = el('div', 'lt-cam', fondo);
  const Y = d.y || 600, X0 = d.x0 || 300, X1 = d.x1 || 1560;
  const viaD = d.t_arrivo - d.t_via;
  // scia sotto la linea, cresce con il nodo
  const scia = el('div', 'lt-scia', cam);
  px(scia, { left: X0, top: Y, width: X1 - X0 });
  gsap.set(scia, { scaleX: 0, transformOrigin: '0% 0%' });
  tl.to(scia, { scaleX: 1, duration: viaD, ease: 'power1.inOut' }, d.t_via);
  const S = svg('svg', { width: 1920, height: 1080, viewBox: '0 0 1920 1080', class: 'lt-svg' }, cam);
  svg('line', { x1: X0, y1: Y, x2: X1 + 120, y2: Y, class: 'lt-base', 'stroke-width': 2 }, S);
  const lin = svg('line', { x1: X0, y1: Y, x2: X1, y2: Y, stroke: '#A9FFBE', 'stroke-width': 8, 'stroke-linecap': 'round', class: 'lt-linea', pathLength: 1 }, S);
  lin.setAttribute('stroke-dasharray', '1 1');
  gsap.set(lin, { attr: { 'stroke-dashoffset': 1 } });
  tl.to(lin, { attr: { 'stroke-dashoffset': 0 }, duration: viaD, ease: 'power1.inOut' }, d.t_via);
  const n = d.tacche || 30;
  for (let k = 0; k < n; k++) {
    const f = (k + 0.5) / n, xx = X0 + (X1 - X0) * f;
    const tk = svg('line', { x1: xx, y1: Y - 24, x2: xx, y2: Y + 24, stroke: '#8DFFA9', 'stroke-width': 5, 'stroke-linecap': 'round', class: 'lt-tacca' }, S);
    gsap.set(tk, { opacity: 0, scaleY: 0.2, transformOrigin: `${xx}px ${Y}px` });
    const u = f < 0.5 ? Math.sqrt(f / 2) : 1 - Math.sqrt((1 - f) / 2);
    tl.to(tk, { opacity: d.tacche_op || 0.3, scaleY: 1, duration: 3 * FR, ease: 'back.out(2)' }, d.t_via + viaD * u);
  }
  // nodo con il numero (solo cifre nello scramble)
  const nodo = el('div', 'lt-nodo v3-pezzo', cam);
  px(nodo, { left: X0, top: Y });
  const nt = el('div', 'lt-nodo-t', nodo);
  gsap.set(nodo, { scale: 0, opacity: 0 });
  tl.to(nodo, { scale: 1, opacity: 1, duration: 4 * FR, ease: 'back.out(2.2)' }, d.num.t - FR);
  decifra(nt, d.nodo || '', d.num.t - FR, 6, 9);
  tl.to(nodo, { x: X1 - X0, duration: viaD, ease: 'power1.inOut' }, d.t_via);
  if (d.num.sotto) {
    // «addominali» viaggia con il nodo, sotto di lui: «100» dice sempre cento di cosa (direttore)
    // pezzo a se (il controllo delle sovrapposizioni lo misura), segue il nodo
    const so = el('div', 'lt-sotto v3-pezzo', cam);
    px(so, { left: X0 - 260, top: Y + 80 });
    decifra(so, d.num.sotto, d.num.t + 2 * FR, 12, 10);
    tl.to(so, { x: X1 - X0, duration: viaD, ease: 'power1.inOut' }, d.t_via);
  }
  (d.pillole || []).forEach((p) => {
    const pl = el('div', 'lt-pill v3-pezzo', cam, esc(p.testo));
    px(pl, { left: p.x, top: p.y });
    gsap.set(pl, { opacity: 0, x: -140, filter: 'blur(14px)' });
    tl.to(pl, { opacity: 1, duration: 2 * FR }, p.t);
    tl.to(pl, { x: 0, filter: 'blur(0px)', duration: 5 * FR, ease: 'power3.out' }, p.t);
  });
  // camera: inclinata e stretta sul nodo, lo segue con la sfocatura di movimento, poi torna larga
  const cs = d.cam_scala || 1.15;
  gsap.set(cam, { transformOrigin: '0px 0px', transformPerspective: 1600 });
  const segui = (xx, s, rx) => ({ x: 960 - xx * s, y: 540 - Y * s + 30, scale: s, rotationX: rx });
  gsap.set(cam, segui(X0 + 300, 1.0, 16));
  tl.to(cam, Object.assign({ duration: d.t_via - d.num.t + 0.2, ease: 'sine.inOut' }, segui(X0 + 300, cs, 14)), d.num.t - 0.2);
  tl.to(cam, Object.assign({ duration: viaD, ease: 'power1.inOut' }, segui(X1 - 300, cs, 10)), d.t_via);
  tl.to(cam, { filter: 'blur(3px)', duration: viaD * 0.3, ease: 'power1.in' }, d.t_via + viaD * 0.15);
  tl.to(cam, { filter: 'blur(0px)', duration: viaD * 0.3, ease: 'power1.out' }, d.t_via + viaD * 0.55);
  tl.to(cam, { x: 0, y: 0, scale: 1, rotationX: 0, duration: 0.6, ease: 'sine.inOut' }, d.t_largo || d.t_arrivo);
  tl.set(fondo, { opacity: 0 }, x.e);
};

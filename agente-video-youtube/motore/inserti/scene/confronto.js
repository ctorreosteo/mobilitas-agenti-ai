// Prima/dopo a tutto schermo con cursore di confronto. Le due foto sono allineate
// sulla caviglia (Vision) alla stessa scala; il DOPO sta sotto, il PRIMA sopra e
// si ritira dietro la linea che scorre da sinistra a destra. Le linee posturali
// (orecchio-spalla-anca-ginocchio-caviglia) si disegnano: sul PRIMA all'entrata,
// sul DOPO mentre il cursore lo scopre. A schermo solo PRIMA e DOPO (catalogo).
// d: prima/dopo {src, w, h, punti}, cursore {t, dur, modo ('meta': fermo a meta, poi una corsa fino a `fino`)}, linee {t}, alto (px)
MODELLI.confronto = function (box, x, d) {
  const H = d.alto || 960;
  const P = d.prima, Q = d.dopo;
  // stessa scala dei pixel ORIGINALI (stessa camera): k px a schermo per px di camera.
  // `zoom` stringe sulla persona (centro fra orecchio e caviglia), la finestra non
  // esce mai dalla foto
  const k = H * (d.zoom || 1) / P.oh;
  const Wf = P.ow * k, Hf = P.oh * k;
  const W = Math.min(Math.round(Wf), d.larghezza_max || 1000);
  const cxp = (P.punti[0][0] + P.punti[4][0]) / 2 * Wf, cyp = (P.punti[0][1] + P.punti[4][1]) / 2 * Hf;
  const sx = Math.min(0, Math.max(W - Wf, W / 2 - cxp)), sy = Math.min(0, Math.max(H - Hf, H / 2 - cyp));
  const ax = sx + P.punti[4][0] * Wf, ay = sy + P.punti[4][1] * Hf;
  const bx = Q.punti[4][0] * Q.ow * k, by = Q.punti[4][1] * Q.oh * k;
  const fondo = el('div', 'cf-fondo', box);
  const sf = el('img', 'cf-sfocato', fondo);
  sf.src = P.src;
  const fin = el('div', 'cf-fin', fondo);
  px(fin, { width: W, height: H, left: 960 - W / 2, top: (1080 - H) / 2 });
  function strato(F, ox, oy, cls) {
    const g = el('div', 'cf-strato ' + cls, fin);
    const i = el('img', '', g);
    i.src = F.src;
    px(i, { width: F.ow * k, height: F.oh * k, left: ox, top: oy });
    const v = svg('svg', { viewBox: `0 0 ${W} ${H}`, class: 'cf-svg' }, g);
    const pts = F.punti.map((p) => [ox + p[0] * F.ow * k, oy + p[1] * F.oh * k]);
    const dpath = pts.map((p, k) => (k ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ');
    const lung = pts.slice(1).reduce((a, p, k) => a + Math.hypot(p[0] - pts[k][0], p[1] - pts[k][1]), 0);
    // filo a piombo dalla caviglia (riferimento), poi la linea del corpo
    const piombo = svg('line', { x1: pts[4][0], y1: pts[4][1], x2: pts[4][0], y2: 20, class: 'cf-piombo' }, v);
    const linea = svg('path', { d: dpath, class: 'cf-linea', 'stroke-dasharray': lung, 'stroke-dashoffset': lung }, v);
    const punti = pts.map((p) => svg('circle', { cx: p[0], cy: p[1], r: 14, class: 'cf-punto' }, v));
    return { g, linea, lung, punti, piombo };
  }
  const B = strato(Q, ax - bx, ay - by, 'cf-dopo');
  const A = strato(P, sx, sy, 'cf-prima');
  // fase 6b: si legge da sinistra a destra: PRIMA a sinistra del cursore, DOPO a destra
  const etA = el('div', 'cf-et cf-et-prima', fin, 'PRIMA');
  const etB = el('div', 'cf-et cf-et-dopo', fin, 'DOPO');
  const cur = el('div', 'cf-cur', fin);
  const man = el('div', 'cf-maniglia', cur, '<span>&lsaquo;</span><span>&rsaquo;</span>');
  // entrata a taglio sulla parola: la card si posa (scala 0,92 -> 1, inclinazione 6 -> 0)
  gsap.set(fondo, { opacity: 0 });
  tl.set(fondo, { opacity: 1 }, x.s);
  gsap.set(fin, { transformPerspective: 1600 });
  tl.fromTo(fin, { scale: 0.92, rotationY: -6, y: 30 }, { scale: 1, rotationY: 0, y: 0, duration: 12 * FR, ease: 'expo.out' }, x.s);
  tl.to(fin, { scale: 1.02, duration: x.e - x.s - 12 * FR, ease: 'none' }, x.s + 12 * FR);
  tl.fromTo(sf, { scale: 1.25 }, { scale: 1.15, duration: x.e - x.s, ease: 'none' }, x.s);
  // etichette: scoprono il riquadro con una tendina (fase 6b, niente dissolvenza)
  tl.fromTo(etA, { clipPath: 'inset(100% 0% 0% 0% round 14px)' }, { clipPath: 'inset(0% 0% 0% 0% round 14px)',
    duration: 9 * FR, ease: 'expo.out' }, x.s + 3 * FR);
  // linee del PRIMA
  const tL = d.linee.t;
  [A, B].forEach((S, k) => {
    const t = k === 0 ? tL : d.cursore.t + d.cursore.dur * 0.35;
    tl.fromTo(S.piombo, { opacity: 0 }, { opacity: 1, duration: 6 * FR, ease: 'power1.out' }, t);
    tl.to(S.linea, { attr: { 'stroke-dashoffset': 0 }, duration: 0.55, ease: 'power2.inOut' }, t + 2 * FR);
    S.punti.forEach((c, j) => tl.fromTo(c, { attr: { r: 0 } }, { attr: { r: 14 }, duration: 8 * FR, ease: RIMBALZO },
      t + 2 * FR + j * 2 * FR));
  });
  // il cursore: entra dal bordo sinistro e scorre fino al bordo destro
  const c0 = d.cursore.t, cd = d.cursore.dur;
  if (d.cursore.modo === 'meta') {
    // fase 7c (direttore): il cursore e gia a meta dall'entrata, PRIMA e DOPO si leggono sempre;
    // poi una sola corsa lenta fino a `fino` (frazione da sinistra) e resta fermo
    const fino = d.cursore.fino === undefined ? 0.15 : d.cursore.fino;
    const da = d.cursore.da === undefined ? 0.5 : d.cursore.da;
    gsap.set(cur, { x: W * da, opacity: 0 });
    gsap.set(A.g, { clipPath: `inset(0px ${W * (1 - da)}px 0px 0px)` });
    tl.to(cur, { opacity: 1, duration: 6 * FR }, x.s + 6 * FR);
    gsap.set(etB, { clipPath: 'inset(100% 0% 0% 0% round 14px)' });
    tl.to(etB, { clipPath: 'inset(0% 0% 0% 0% round 14px)', duration: 9 * FR, ease: 'expo.out' }, x.s + 5 * FR);
    tl.to(cur, { x: W * fino, duration: cd, ease: 'power2.inOut' }, c0);
    tl.to(A.g, { clipPath: `inset(0px ${W * (1 - fino)}px 0px 0px)`, duration: cd, ease: 'power2.inOut' }, c0);
    tl.set(fondo, { opacity: 0 }, x.e);
    return;
  }
  gsap.set(cur, { x: W, opacity: 0 });
  tl.to(cur, { opacity: 1, duration: 4 * FR }, c0 - 4 * FR);
  // va fino al bordo sinistro (si vede tutto il DOPO), poi torna a meta e resta: il confronto
  const corsa = cd * 0.78, ritorno = 10 * FR;
  tl.fromTo(cur, { x: W }, { x: 0, duration: corsa, ease: 'power2.inOut' }, c0);
  tl.to(cur, { x: W / 2, duration: ritorno, ease: 'power3.inOut' }, c0 + corsa + 2 * FR);
  tl.fromTo(A.g, { clipPath: 'inset(0px 0px 0px 0px)' }, { clipPath: `inset(0px ${W}px 0px 0px)`, duration: corsa,
    ease: 'power2.inOut' }, c0);
  tl.to(A.g, { clipPath: `inset(0px ${W / 2}px 0px 0px)`, duration: ritorno, ease: 'power3.inOut' }, c0 + corsa + 2 * FR);
  // le etichette salgono e scendono in verticale: mai una parola tagliata a meta in larghezza
  tl.to(etA, { clipPath: 'inset(0% 0% 100% 0% round 14px)', duration: 5 * FR, ease: 'power3.in' }, c0 + 2 * FR);
  tl.to(etA, { clipPath: 'inset(0% 0% 0% 0% round 14px)', duration: 8 * FR, ease: 'expo.out' }, c0 + corsa + 6 * FR);
  gsap.set(etB, { clipPath: 'inset(100% 0% 0% 0% round 14px)' });
  tl.to(etB, { clipPath: 'inset(0% 0% 0% 0% round 14px)', duration: 9 * FR, ease: 'expo.out' }, c0 + cd * 0.2);

  tl.set(fondo, { opacity: 0 }, x.e);
};

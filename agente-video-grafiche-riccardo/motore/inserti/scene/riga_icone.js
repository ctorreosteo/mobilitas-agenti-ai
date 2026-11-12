// Riga di icone in basso (campionario v3, reference gadzhi-14): icone lineari verdi
// (oggetti e luoghi, mai figure umane) che si disegnano una alla volta sulla parola, con
// l'etichetta che si decifra sotto; il fondo si scurisce dal basso (effetto di piatto).
// Escono insieme scomponendosi (scala e sfocatura).
// d: y, voci [{icona, testo, t, x}]
const ICONE_V3 = {
  mare: ['M8 52 q10 -10 20 0 t20 0 t20 0 t20 0 t20 0', 'M8 72 q10 -10 20 0 t20 0 t20 0 t20 0 t20 0', 'M8 92 q10 -10 20 0 t20 0 t20 0 t20 0 t20 0'],
  piscina: ['M30 66 V26 a14 14 0 0 1 28 0', 'M62 66 V26 a14 14 0 0 1 28 0', 'M30 40 h32', 'M30 56 h32',
    'M4 80 q10 -10 20 0 t20 0 t20 0 t20 0 t20 0', 'M4 98 q10 -10 20 0 t20 0 t20 0 t20 0 t20 0'],
  spiaggia: ['M54 30 a14 14 0 1 0 0.01 0', 'M54 6 v8', 'M54 50 v8', 'M30 32 h8', 'M70 32 h8', 'M37 15 l6 6', 'M65 43 l6 6', 'M71 15 l-6 6', 'M43 43 l-6 6',
    'M4 78 h100', 'M14 96 q20 -12 40 0 t40 0'],
};
MODELLI.riga_icone = function (box, x, d) {
  const Y = d.y || 760;
  (d.voci || []).forEach((v, i) => {
    const g = el('div', 'ri-v v3-pezzo', box);
    px(g, { left: v.x, top: Y });
    const s = svg('svg', { viewBox: '0 0 108 108', class: 'ri-ico' }, g);
    (ICONE_V3[v.icona] || []).forEach((dd, k) => {
      const p = svg('path', { d: dd, fill: 'none', stroke: '#8DFFA9', 'stroke-width': 5, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', pathLength: 1 }, s);
      p.setAttribute('stroke-dasharray', '1 1');
      gsap.set(p, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(p, { attr: { 'stroke-dashoffset': 0 }, duration: 10 * FR, ease: 'power2.out' }, v.t - 2 * FR + k * 1 * FR);
    });
    gsap.set(s, { scale: 0.8, opacity: 0 });
    tl.to(s, { opacity: 1, duration: 2 * FR }, v.t - 2 * FR);
    tl.to(s, { scale: 1, duration: 8 * FR, ease: 'back.out(1.8)' }, v.t - 2 * FR);
    const et = el('div', 'ri-et', g);
    decifra(et, v.testo, v.t + 2 * FR, 7, 400 + i);
    // uscita insieme, scomponendosi
    tl.to(g, { opacity: 0, scale: 0.86, filter: 'blur(10px)', duration: 6 * FR, ease: 'power2.in' }, x.e - 6 * FR + i * FR);
  });
};

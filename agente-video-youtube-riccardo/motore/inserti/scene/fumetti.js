// Fumetti di chat accanto a lui (fase 7b rivista, reference martell-05): uno per
// frase, con le sue parole, sull'istante in cui le dice. Ogni fumetto nasce come
// una macchia chiara sfocata e scalata a 0,85, in 4 frame e nitido e pieno con
// un piccolo rimbalzo; quelli di prima salgono. Escono tutti insieme.
// d: x (bordo sinistro), y (fondo della pila), corpo, voci [{righe:[...], t, larg}],
//    spazio, lato ('sx' = coda verso sinistra, cioe verso di lui)
MODELLI.fumetti = function (box, x, d) {
  const corpo = d.corpo || 58, pad = d.pad || Math.round(corpo * 0.55), sp = d.spazio || 26;
  const lh = Math.round(corpo * 1.14);
  const alt = (v) => v.righe.length * lh + 2 * pad;
  const pila = el('div', 'fu-pila', box);
  const voci = d.voci || [];
  voci.forEach((v, i) => {
    const h = alt(v);
    const f = el('div', 'fu', pila);
    px(f, { left: d.x, width: v.larg + 2 * pad + 8, height: h, top: d.y - h, fontSize: corpo, lineHeight: lh + 'px',
      padding: `${pad}px ${pad + 4}px` });
    v.righe.forEach((r) => el('div', 'fu-r', f, esc(r)));
    const coda = svg('svg', { viewBox: '0 0 40 40', class: 'fu-coda' + (d.lato === 'dx' ? ' fu-coda-dx' : '') }, f);
    svg('path', { d: 'M40 0 C30 18 18 30 0 38 C18 36 34 30 40 22 Z', fill: '#E1E7EE' }, coda);
    gsap.set(f, { opacity: 0, scale: 0.85, filter: 'blur(14px)', transformOrigin: d.lato === 'dx' ? '100% 100%' : '0% 100%' });
    tl.to(f, { opacity: 1, duration: 4 * FR, ease: 'power1.out' }, v.t);
    tl.to(f, { scale: 1, filter: 'blur(0px)', duration: 0.36, ease: 'back.out(1.4)' }, v.t);
    // i fumetti dopo questo lo spingono su
    let su = 0;
    voci.slice(i + 1).forEach((w) => {
      su += alt(w) + sp;
      tl.to(f, { y: -su, duration: 0.32, ease: 'power3.out' }, w.t);
    });
  });
  tl.to(pila, { opacity: 0, scale: 0.97, filter: 'blur(10px)', duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
};

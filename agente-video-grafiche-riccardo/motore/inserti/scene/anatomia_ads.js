// Scena anatomica a tutto schermo per gli ads 9:16 (laboratorio, collaudo AD_REFLUSSO, 04/11/2026). Modello
// nuovo, da anatomia (che resta com'e) e dalla reference martell-07: fondo del sito con il retino, un disegno Servier
// Medical Art ricolorato nel brand (lo prepara il motore: dati.servier -> dati.src) fermo al centro, mai deformato,
// due frecce verdi generiche «da fuori» che premono verso il disegno sulla parola, una riga sopra e due sotto.
// Nessuna etichetta anatomica che non sia detta. Attribuzione Servier in basso (classe reel-attr: obbligo di licenza,
// fuori dal controllo delle parole dette; senza cifre).
// d: servier {nome, alto, modo}, fig_y, righe [{testo, t, y, corpo, chiave}], frecce {t, y, da, a, lungo}, attribuzione
MODELLI.anatomia_ads = function (box, x, d) {
  const QW = 1080, EPS = 0.001;
  const vis = el('div', 'ana-vis', box);
  gsap.set(vis, { opacity: 0 });
  tl.set(vis, { opacity: 1 }, x.s);           // entra a taglio, gia piena
  tl.set(vis, { opacity: 0 }, x.e - EPS);     // esce a taglio
  const fondo = el('div', 'ana-fondo', vis);
  const ret = el('div', 'ana-ret', fondo);
  retino(ret, { w: 1500, h: 2300, passo: 18, seme: 47, verdi: 0.25, curve: [[200, 0.0028, 0.7, 0.30], [170, 0.0034, 2.4, 0.74]], larga: 160 });
  tl.fromTo(ret, { x: 0, y: 0 }, { x: -50, y: -40, duration: x.e - x.s, ease: 'none' }, x.s);
  // il disegno: fermo, con una luce blu dietro e una lenta salita (camera, martell-07)
  const w = d.img_w, h = d.img_h, fx = (QW - w) / 2, fy = d.fig_y;
  const luce = el('div', 'ana-luce', vis);
  px(luce, { left: fx - 120, top: fy - 100, width: w + 240, height: h + 200 });
  const fig = el('img', 'ana-fig', vis);
  fig.src = d.src;
  px(fig, { left: fx, top: fy, width: w, height: h });
  tl.fromTo([fig, luce], { y: 10, scale: 1 }, { y: -10, scale: 1.02, duration: x.e - x.s, ease: 'none' }, x.s);
  // frecce «da fuori»: una a sinistra e una a destra, puntate verso il disegno; entrano e premono sulla parola
  if (d.frecce) {
    const F = d.frecce, L = F.lungo || 170;
    [[-1, F.da], [1, F.a]].forEach(([lato, xx]) => {
      const c = el('div', 'ana-freccia', vis);
      px(c, { left: xx - L / 2, top: F.y - 40, width: L, height: 80 });
      const s = svg('svg', { width: L, height: 80, viewBox: `0 0 ${L} 80` }, c);
      // punta verso il centro dello schermo
      const p = lato < 0 ? `M 8 40 L ${L - 30} 40 M ${L - 58} 14 L ${L - 26} 40 L ${L - 58} 66`
                         : `M ${L - 8} 40 L 30 40 M 58 14 L 26 40 L 58 66`;
      svg('path', { d: p, fill: 'none', stroke: '#72FA93', 'stroke-width': 14, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, s);
      gsap.set(c, { opacity: 0, x: lato * -70 });
      tl.to(c, { opacity: 1, x: 0, duration: 6 * FR, ease: 'power3.out' }, F.t);
      // spinta verso il disegno, due volte, sulla voce
      [0, 1].forEach((k) => {
        const t0 = F.t + 8 * FR + k * 0.55;
        tl.to(c, { x: lato * -26, duration: 5 * FR, ease: 'power2.in' }, t0);
        tl.to(c, { x: 0, duration: 7 * FR, ease: 'power2.out' }, t0 + 5 * FR);
      });
    });
  }
  // le righe dette: entrano intere (opacita, salita, sfocatura), mai da una maschera
  (d.righe || []).forEach((r) => {
    const rg = el('div', 'ana-riga' + (r.chiave ? ' ana-k' : ''), vis);
    px(rg, { top: r.y, fontSize: r.corpo || 88 });
    const sp = el('span', '', rg, esc(r.testo));
    gsap.set(sp, { opacity: 0, y: 26, filter: 'blur(10px)' });
    tl.to(sp, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 8 * FR, ease: 'expo.out' }, r.t);
  });
  if (d.attribuzione) {
    const a = el('div', 'reel-attr', vis, esc(d.attribuzione));
    px(a, { left: d.attr_x || 96, top: d.attr_y || 1200 });
  }
};

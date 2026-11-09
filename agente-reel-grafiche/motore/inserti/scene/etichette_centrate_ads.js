// Etichette barrate centrate per gli ads 9:16, modo «finestra» (laboratorio, AD_REFLUSSO, 04/11/2026). Modello
// nuovo sopra etichette_ads2 (che resta com'e, con etichette_luce ed etichette_ads): stesso fondo a taglio, stesse
// pillole luminose, stessa barra panna piena (resta all'85%, pillola barrata al 55%), pillole nitide fino al taglio.
// Cambiano:
//  - impaginazione: le pillole sono centrate nella finestra (in orizzontale ognuna, in verticale il blocco), la prima
//    entra da sinistra, la seconda da destra (si alternano);
//  - entrata: una pillola che ha t sul primo fotogramma c'e gia, intera e piena, e scivola al suo posto (difetto visto
//    dal direttore in etichette_ads2: 6-7 fotogrammi di finestra vuota all'entrata);
//  - la barra resta dentro il contorno della pillola (rientra di mezzo margine per lato).
// Va caricato con usa: ["etichette_luce", "etichette_ads", "etichette_ads2"]. Dati come etichette_ads2 (rett, corpo,
// spazio, voci [{testo, t, barra_t, larg}], luce, barra, barra_px, barra_resta, barrata); x e y si calcolano qui.
MODELLI.etichette_centrate_ads = function (box, x, d) {
  const EPS = 0.001;
  const r = d.rett;
  const corpo = d.corpo || 56, h = Math.round(corpo * 1.9), padx = Math.round(corpo * 0.62), sp = d.spazio || 30;
  const voci = d.voci || [];
  const alto = voci.length * h + (voci.length - 1) * sp;
  const y0 = d.y !== undefined ? d.y : Math.round(r.y + (r.h - alto) / 2);
  MODELLI.etichette_ads2(box, x, Object.assign({}, d, { x: 0, y: y0 }));
  const cx = r.x + r.w / 2;
  [...box.querySelectorAll('.el-g')].forEach((g, i) => {
    const v = voci[i];
    if (!v) return;
    const p = g.querySelector('.el-pill');
    // fase 6, giro 4 (variante in prova «-icone»): un'icona Tabler a sinistra del testo, dentro la pillola; la barra la
    // attraversa insieme al testo (si nega l'oggetto: la pastiglia, il manubrio). Senza icona il modello resta com'era
    if (v.icona) {
      // giro 4 (direttore, 5/10: verde su verde invisibile): icona grande, tratto pieno blu notte sulla pillola verde
      const L = Math.round(h * 0.76), gap = Math.round(corpo * 0.26);
      const n = String(v.icona).replace(/^tabler:/, '');
      const s = svg('svg', { viewBox: '0 0 24 24', width: L, height: L }, p);
      s.setAttribute('class', 'ec-ic');
      px(s, { left: padx, top: (h - L) / 2 });
      ((typeof TABLER !== 'undefined' && TABLER[n]) || []).forEach((dd) => svg('path', { d: dd, fill: 'none', stroke: '#001A3D',
        'stroke-width': 2.3, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, s));
      px(p, { paddingLeft: padx + L + gap, width: (v.larg || 0) + 2 * padx + L + gap });
    }
    const w = p.offsetWidth;
    // al centro della finestra
    px(g, { left: Math.round(cx - w / 2) });
    // entrata nuova: da sinistra la prima, da destra la seconda (al posto di quella di etichette_luce)
    tl.getTweensOf(g).forEach((tw) => tw.kill());
    const lato = i % 2 === 0 ? -1 : 1;
    if (v.t <= x.s + EPS) {
      // c'e gia sul primo fotogramma: intera, piena, appena spostata e appena sfocata, poi si ferma
      // direttore (AD_EMICRANIA, giro 1): al primo fotogramma la pillola spostata di 60 px toccava il bordo della
      // finestra e il bagliore era tagliato: ora c'e gia al suo posto, nitida, con un piccolo colpo di scala
      gsap.set(g, { opacity: 1, x: 0, filter: 'blur(0px)', scale: 0.97 });
      tl.to(g, { scale: 1, duration: 6 * FR, ease: 'power2.out' }, x.s);
    } else {
      gsap.set(g, { opacity: 0, x: 90 * lato, filter: 'blur(12px)' });
      tl.to(g, { opacity: 1, duration: 4 * FR, ease: 'power1.out' }, v.t);
      tl.to(g, { x: 0, filter: 'blur(0px)', duration: 8 * FR, ease: 'power3.out' }, v.t);
    }
    // la barra rientra di mezzo margine per lato: resta dentro il contorno arrotondato e copre tutto il testo
    const b = g.querySelector('.ea-barra');
    if (b) px(b, { left: Math.round(padx / 2), width: w - 2 * Math.round(padx / 2) });
  });
};

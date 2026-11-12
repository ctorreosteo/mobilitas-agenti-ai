// Grafiche sulla persona in camera, per i reel 9:16 (agente reel-grafiche, fase 6, 05/11/2026). Modello nuovo, IN PROVA,
// adattato dal catalogo YouTube (titolo dietro, numero dietro, frase sul corpo, card vicino alle mani, lui nel cerchio),
// che resta com'è. Il «dietro» lo fa il motore: dopo la grafica rimette sopra la persona del video base con la sua sagoma
// (Apple Vision), quando `dietro: true`. Il «lui nel cerchio» lo fa il motore con `pip`: sotto la grafica, che ha un foro
// tondo, mette il video base rimpicciolito.
// Reference: martell-02 (titolo enorme dietro la testa, parola enorme davanti sulla maglia, ombra doppia e bagliore),
// gadzhi-03/18 (numero grande), gadzhi-02/19 (card piccola di vetro accanto a lui), gadzhi-09 (lui nel cerchio).
// d: box {x, y, w, h} (tutto quello che si vede sta qui dentro; «cerchio»: tutto il quadro), tipo:
//    "titolo": righe [{testo, t, verde}], y (centro del blocco), corpo; dietro: true
//    "numero": testo (cifra detta), t, y, corpo; dietro: true
//    "frase": righe [{testo, t, verde}], y, corpo (davanti, sul corpo, mai sul volto)
//    "card": testo, t, icona, corpo (davanti, vicino alle mani: vicino_mani: true)
//    "cerchio": c [x, y], r (il foro), t_anello, righe [{testo, t, verde}] (in alto), corpo; pip {scala, x, y} per il motore
//    uscita "taglio" | "rapida"
MODELLI.persona_reel = function (box, x, d) {
  const EPS = 0.001, B = d.box || { x: 0, y: 0, w: 1080, h: 1920 };
  const clip = el('div', 'per-clip', box);
  px(clip, { left: B.x, top: B.y, width: B.w, height: B.h });
  const dentro = el('div', 'per-dentro', clip);
  px(dentro, { left: -B.x, top: -B.y });
  gsap.set(clip, { opacity: 0 });
  tl.set(clip, { opacity: 1 }, x.s);
  if (d.uscita === 'rapida') tl.to(dentro, { opacity: 0, filter: 'blur(8px)', duration: 4 * FR, ease: 'power2.in' }, x.e - 4 * FR);
  tl.set(clip, { opacity: 0 }, x.e - EPS);
  const cx = B.x + B.w / 2;
  const blocco = (righe, y, cp, cls, entra) => {
    const lh = Math.round(cp * 1.02), tot = righe.length * lh;
    righe.forEach((r, i) => {
      const e = el('div', 'per-riga ' + cls + (r.verde ? ' per-v' : ''), dentro, esc(r.testo));
      px(e, { fontSize: cp, lineHeight: lh + 'px', top: y - tot / 2 + i * lh, left: cx }); gsap.set(e, { xPercent: -50 });
      entra(e, r.t, i);
    });
  };
  if (d.tipo === 'titolo') {
    // il titolo sale da dietro le spalle, sfocato, e si ferma (martell-02): ogni riga sulla sua parola
    blocco(d.righe, d.y, d.corpo || 170, 'per-tit', (e, t) => {
      tl.fromTo(e, { opacity: 0, y: 70, filter: 'blur(14px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 6 * FR, ease: 'power3.out',
        immediateRender: true }, t);
    });
  } else if (d.tipo === 'numero') {
    const cp = d.corpo || 700;
    const n = el('div', 'per-riga per-num', dentro, esc(d.testo));
    px(n, { fontSize: cp, lineHeight: Math.round(cp * 0.9) + 'px', top: d.y - Math.round(cp * 0.45), left: cx }); gsap.set(n, { xPercent: -50 });
    tl.fromTo(n, { opacity: 0, scale: 1.18, filter: 'blur(16px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 6 * FR, ease: 'power3.out',
      immediateRender: true }, d.t);
  } else if (d.tipo === 'frase') {
    // parola enorme davanti, sul corpo: bianca con l'ombra doppia, leggibile anche su una maglia chiara (martell-02)
    blocco(d.righe, d.y, d.corpo || 130, 'per-fra', (e, t) => {
      // direttore (prova del 05/11/2026): nitida entro 0,1 s, con un colpo di scala 1,12 -> 1
      tl.fromTo(e, { opacity: 0.4, scale: 1.12, filter: 'blur(6px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 3 * FR, ease: 'power3.out',
        immediateRender: true }, t);
    });
  } else if (d.tipo === 'card') {
    // card di vetro accanto alle mani (gadzhi-02, gadzhi-19): icona nel disco verde a sinistra, una o due righe (la parola
    // chiave in verde). Direttore (prova del 05/11/2026): vetro più chiaro con il filo verde, così si stacca da una divisa
    // blu; entra quasi a taglio (2 fotogrammi di sfocatura), già leggibile; mai vuota
    const cp = d.corpo || 84, righe = d.righe || [{ testo: d.testo }];
    const lh = Math.round(cp * 1.04), pad = Math.round(cp * 0.3), ic = d.icona ? Math.round(lh * Math.min(2, righe.length) * 0.92) : 0;
    const h = righe.length * lh + 2 * pad;
    const c = el('div', 'per-card', dentro);
    px(c, { height: h, borderRadius: Math.round(cp * 0.42), left: B.x + 22, top: B.y + (B.h - h) / 2, paddingLeft: pad + (ic ? ic + pad : 0),
      paddingRight: Math.round(cp * 0.5), paddingTop: pad });
    righe.forEach((r) => { const w = el('div', 'per-cw' + (r.verde ? ' per-cw-v' : ''), c, esc(r.testo)); px(w, { fontSize: cp, lineHeight: lh + 'px' }); });
    if (d.icona) {
      const ICONE = Object.assign({}, typeof RIA_ICONE !== 'undefined' ? RIA_ICONE : {}, typeof MIC_ICONE !== 'undefined' ? MIC_ICONE : {});
      const dc = el('div', 'per-disco', c);
      px(dc, { width: ic, height: ic, left: pad, top: (h - ic) / 2 });
      const sv = svg('svg', { viewBox: '0 0 108 108', width: ic * 0.66, height: ic * 0.66 }, dc);
      px(sv, { position: 'absolute', left: ic * 0.17, top: ic * 0.17 });
      (ICONE[d.icona] || []).forEach((dd) => svg('path', { d: dd, fill: 'none', stroke: '#001A3D', 'stroke-width': 7, 'stroke-linecap': 'round',
        'stroke-linejoin': 'round' }, sv));
    }
    tl.fromTo(c, { opacity: 0.5, x: d.da_destra ? 24 : -24, filter: 'blur(6px)' }, { opacity: 1, x: 0, filter: 'blur(0px)', duration: 2 * FR,
      ease: 'power3.out', immediateRender: true }, d.t);
    fluttua(c, d.t + 2 * FR, x.e, 4, 2.6);
  } else if (d.tipo === 'cerchio') {
    // fondo del brand con un foro tondo: dentro il motore mette lui, rimpicciolito (pip). L'anello verde si traccia sul foro.
    const [c0, c1] = d.c, r = d.r;
    const f = el('div', 'per-fondo fondo-sito', dentro);
    px(f, { left: 0, top: 0, width: 1080, height: 1920 });
    const m = `radial-gradient(circle ${r}px at ${c0}px ${c1}px, transparent ${r - 0.5}px, #000 ${r + 0.5}px)`;
    f.style.webkitMaskImage = m; f.style.maskImage = m;
    const s = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920 }, dentro);
    s.setAttribute('class', 'per-svg');
    const p = svg('circle', { cx: c0, cy: c1, r: r + 6, fill: 'none', stroke: '#72FA93', 'stroke-width': 10, pathLength: 1,
      transform: `rotate(-90 ${c0} ${c1})` }, s);
    p.setAttribute('stroke-dasharray', '1 1');
    // direttore (prova del 05/11/2026): il cerchio non resta mai senza anello; con t_anello assente l'anello è intero dal
    // primo fotogramma
    if (d.t_anello !== undefined && d.t_anello > x.s) {
      gsap.set(p, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(p, { attr: { 'stroke-dashoffset': 0 }, duration: 4 * FR, ease: 'power2.out' }, d.t_anello);
    }
    blocco(d.righe || [], d.y || 520, d.corpo || 120, 'per-tit per-tit-s', (e, t) => {
      tl.fromTo(e, { opacity: 0, y: 30, filter: 'blur(10px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 5 * FR, ease: 'power3.out',
        immediateRender: true }, t);
    });
  }
};

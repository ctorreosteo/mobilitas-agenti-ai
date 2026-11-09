// Fumetto di chat per gli ads 9:16, nella finestra (laboratorio, AD_REFLUSSO, 04/11/2026). Modello nuovo, da
// fumetti (che resta com'e), reference martell-05. Una frase che altri hanno detto ai pazienti: un solo fumetto chiaro
// (panna -> grigio, coda, ombra, luce interna, testo blu notte pieno), senza nomi, loghi, avatar o spunte. Prima i tre
// puntini dell'attesa («…», disegnati), che nascono da una macchia sfocata e si mettono a fuoco in 5 fotogrammi; sulla
// parola il fumetto si allarga nella frase: nasce sfocato e scalato a 0,85 e in 0,33 s e nitido, con un piccolo
// rimbalzo. Fondo pieno della finestra a taglio all'entrata e all'uscita, alfa 0 fuori dal rettangolo.
// d: rett {x, y, w, h, r} o [{da, ...}], x (bordo sinistro del fumetto), y (fondo del fumetto), corpo, pad,
//    attesa {testo: «…», t, via, larg, alt}, frase {testo, t, larg}
MODELLI.fumetto_ads = function (box, x, d) {
  const EPS = 0.001;
  const clip = el('div', 'ffa-clip', box);
  const fondo = el('div', 'ffa-fondo fondo-sito', clip);
  const dentro = el('div', 'ffa-dentro', clip);
  const RR = Array.isArray(d.rett) ? d.rett : [Object.assign({ da: 0 }, d.rett)];
  const metti = (R, t) => {
    const a = { left: R.x + 'px', top: R.y + 'px', width: R.w + 'px', height: R.h + 'px', borderRadius: R.r + 'px' };
    const f = { width: R.w + 'px', height: R.h + 'px' }, dd = { left: -R.x + 'px', top: -R.y + 'px' };
    if (t === undefined) { gsap.set(clip, a); gsap.set(fondo, f); gsap.set(dentro, dd); }
    else { tl.set(clip, a, t - EPS); tl.set(fondo, f, t - EPS); tl.set(dentro, dd, t - EPS); }
  };
  metti(RR[0]);
  RR.slice(1).forEach((R) => metti(R, R.da));
  gsap.set(clip, { opacity: 0 });
  tl.set(clip, { opacity: 1 }, x.s);                // entra a taglio, con i puntini gia li
  tl.set(clip, { opacity: 0 }, x.e - EPS);          // esce a taglio sull'ultimo fotogramma
  el('div', 'ffa-alone', dentro);

  const corpo = d.corpo || 96, pad = d.pad || 46, lh = Math.round(corpo * 1.18);
  const X = d.x, Y = d.y;
  // coda a punta fuori dall'angolo in basso a sinistra (l'angolo del fumetto e quasi dritto, la coda lo continua);
  // sfumata come il fondo del fumetto, con un id per istanza
  let nc = 0;
  const coda = (f) => {
    const id = 'ffa-g' + (nc++) + '-' + Math.round(x.s * 1000);
    const s = svg('svg', { viewBox: '0 0 34 48', class: 'ffa-coda' }, f);
    const g = svg('linearGradient', { id: id, x1: 0, y1: 0, x2: 0, y2: 1 }, svg('defs', {}, s));
    svg('stop', { offset: 0, 'stop-color': '#E2E6EB' }, g);
    svg('stop', { offset: 1, 'stop-color': '#D0D7DF' }, g);
    svg('path', { d: 'M34 0 C34 24 22 40 0 48 L34 48 Z', fill: `url(#${id})` }, s);
  };
  // i puntini dell'attesa
  const A = d.attesa;
  if (A) {
    const w = A.larg || 330, h = A.alt || (lh + 2 * pad), dp = A.punto || 30, sp = A.passo || 62;
    const f = el('div', 'ffa ffa-attesa', dentro);
    px(f, { left: X, top: Y - h, width: w, height: h });
    coda(f);
    const dots = [];
    for (let k = 0; k < 3; k++) {
      const p = el('div', 'ffa-punto', f);
      px(p, { left: w / 2 + (k - 1) * sp - dp / 2, top: h / 2 - dp / 2, width: dp, height: dp });
      dots.push(p);
    }
    gsap.set(f, { transformOrigin: '0% 100%' });
    tl.fromTo(f, { opacity: 0.8, scale: 0.85, filter: 'blur(10px)' },
      { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 5 * FR, ease: 'back.out(1.4)', immediateRender: true }, A.t);
    // i puntini saltano in fila, come chi sta scrivendo (segmenti finiti, niente repeat)
    const via = A.via !== undefined ? A.via : x.e;
    dots.forEach((p, k) => {
      gsap.set(p, { opacity: 0.45 });
      for (let t = A.t + 6 * FR + k * 4 * FR; t + 12 * FR <= via; t += 18 * FR) {
        tl.to(p, { y: -12, opacity: 1, duration: 5 * FR, ease: 'power2.out' }, t);
        tl.to(p, { y: 0, opacity: 0.45, duration: 7 * FR, ease: 'power2.in' }, t + 5 * FR);
      }
    });
    tl.set(f, { opacity: 0 }, via);
  }
  // la frase
  const F = d.frase;
  if (F) {
    const w = F.larg + 2 * pad, h = lh + 2 * pad;
    const f = el('div', 'ffa ffa-frase', dentro);
    px(f, { left: X, top: Y - h, width: w, height: h, padding: `${pad}px`, fontSize: corpo, lineHeight: lh + 'px' });
    el('div', 'ffa-t', f, esc(F.testo));
    coda(f);
    gsap.set(f, { opacity: 0, transformOrigin: '0% 100%' });
    tl.fromTo(f, { opacity: 0.6, scale: 0.85, filter: 'blur(12px)' },
      { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 10 * FR, ease: 'back.out(1.4)', immediateRender: false }, F.t);
  }
};

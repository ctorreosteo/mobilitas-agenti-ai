// Aggancio dei primi secondi per gli ads 9:16 (laboratorio, prova su AD_COLON, 04/11/2026; reference martell-02,
// gadzhi-04, martell-07). Righe dette, una parola chiave nel gradiente del brand, il pittogramma Mobilitas in un disco.
// Regola dell'aggancio: al fotogramma 0 tutto quello che c'e e gia pieno e fermo (niente decifrazione, niente
// sfocatura): e il fotogramma che si vede mentre si scorre. Le righe successive entrano in 4 fotogrammi (salita breve),
// e lasciano il posto alle nuove a taglio (via). Modo «finestra» (rett, lista {da} o rettangolo) o «tutto».
// d: modo, rett, righe [{testo, t, via, y, corpo, grad, chiave}], disco {t, via, y, lato}
MODELLI.aggancio_ads = function (box, x, d) {
  const QW = 1080, QH = 1920, EPS = 0.001;
  const clip = el('div', 'agg-clip', box);
  const fondo = el('div', 'agg-fondo fondo-sito', clip);
  const dentro = el('div', 'agg-dentro', clip);
  if (d.modo === 'finestra') {
    const R = d.rett;
    px(clip, { left: R.x, top: R.y, width: R.w, height: R.h }); clip.style.borderRadius = R.r + 'px';
    px(fondo, { width: R.w, height: R.h }); px(dentro, { left: -R.x, top: -R.y });
  } else {
    px(clip, { left: 0, top: 0, width: QW, height: QH }); px(fondo, { width: QW, height: QH }); px(dentro, { left: 0, top: 0 });
    const ret = el('div', 'agg-ret', fondo);
    retino(ret, { w: 1500, h: 2300, passo: 18, seme: 71, verdi: 0.3, curve: [[220, 0.0030, 0.6, 0.30], [180, 0.0036, 2.2, 0.76]], larga: 170 });
    tl.fromTo(ret, { x: 0, y: 0 }, { x: -40, y: -30, duration: x.e - x.s, ease: 'none' }, x.s);
  }
  gsap.set(clip, { opacity: 1 });                    // c'e dal primo fotogramma
  tl.set(clip, { opacity: 0 }, x.e - EPS);           // esce a taglio
  const subito = (t) => t <= x.s + EPS;
  if (d.disco) {
    const D = d.disco, L = D.lato || 128;
    // disco panna del brand, pittogramma mai ricolorato
    const c = el('div', 'pittogramma agg-disco', dentro); px(c, { left: (QW - L) / 2, top: D.y, width: L, height: L });
    const im = el('img', '', c); im.src = 'assets/pittogramma-sfondo-trasparente.png';
    if (subito(D.t)) gsap.set(c, { opacity: 1 });
    else { gsap.set(c, { opacity: 0, scale: 0.8 }); tl.to(c, { opacity: 1, scale: 1, duration: 5 * FR, ease: 'back.out(1.6)' }, D.t); }
    if (D.via !== undefined) tl.set(c, { opacity: 0 }, D.via);
  }
  (d.righe || []).forEach((r) => {
    const rg = el('div', 'agg-riga' + (r.grad ? ' agg-grad' : '') + (r.chiave ? ' agg-k' : ''), dentro);
    px(rg, { top: r.y, fontSize: r.corpo || 96 });
    const sp = el('span', '', rg, esc(r.testo));
    if (subito(r.t)) gsap.set(sp, { opacity: 1 });
    else {
      // giro 2 (direttore): ogni riga entra a taglio sulla sua parola, piena, con un piccolo colpo di scala
      gsap.set(sp, { opacity: 0 });
      tl.set(sp, { opacity: 1 }, r.t);
      tl.fromTo(sp, { scale: 1.06 }, { scale: 1, duration: 5 * FR, ease: 'power2.out', immediateRender: false }, r.t);
    }
    if (r.via !== undefined) tl.set(sp, { opacity: 0 }, r.via);
  });
};

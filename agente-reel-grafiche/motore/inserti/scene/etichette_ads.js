// Etichette barrate per gli ads 9:16 (laboratorio, fase 1, 03/11/2026). Modello nuovo:
// non tocca etichette_luce, lo chiama. Aggiunge il fondo del brand e il posto della grafica:
//   d.modo = 'finestra': il fondo riempie la finestra del video base (d.rett: x, y, w, h, r in px
//            del quadro 1080x1920), al posto del B-roll; tutto resta dentro quel rettangolo arrotondato;
//   d.modo = 'pieno':    il fondo copre tutto il quadro; d.fascia = [y0, y1] (facoltativa) resta
//            trasparente dalla riga y0 alla riga y1 comprese (i sottotitoli del video base si vedono).
// Le pillole sono quelle di etichette_luce (d.x, d.y, d.corpo, d.spazio, d.voci, d.luce, d.barra),
// in coordinate del quadro. Il fondo entra in d.entra_fr frame (4) ed esce con le pillole (ESCE).
MODELLI.etichette_ads = function (box, x, d) {
  const W = 1080, H = 1920;
  let dentro;
  if (d.modo === 'finestra') {
    const r = d.rett;
    const clip = el('div', 'ea-clip', box);
    px(clip, { left: r.x, top: r.y, width: r.w, height: r.h, borderRadius: r.r });
    const fondo = el('div', 'ea-fondo fondo-sito', clip);
    px(fondo, { left: 0, top: 0, width: r.w, height: r.h });
    dentro = el('div', 'ea-dentro', clip);
    px(dentro, { left: -r.x, top: -r.y, width: W, height: H });
    gsap.set(clip, { opacity: 0 });
    tl.to(clip, { opacity: 1, duration: (d.entra_fr || 4) * FR, ease: 'power1.out' }, x.s);
    tl.to(clip, { opacity: 0, duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
  } else {
    const tutto = el('div', 'ea-tutto', box);
    px(tutto, { left: 0, top: 0, width: W, height: H });
    if (d.fascia) {
      // maschera a scalini netti: righe y0..y1 comprese trasparenti
      const a = d.fascia[0], b = d.fascia[1] + 1;
      const m = `linear-gradient(to bottom, #000 0px, #000 ${a}px, transparent ${a}px, transparent ${b}px, #000 ${b}px, #000 ${H}px)`;
      tutto.style.webkitMaskImage = m;
      tutto.style.maskImage = m;
    }
    const fondo = el('div', 'ea-fondo fondo-sito', tutto);
    px(fondo, { left: 0, top: 0, width: W, height: H });
    dentro = el('div', 'ea-dentro', tutto);
    px(dentro, { left: 0, top: 0, width: W, height: H });
    gsap.set(fondo, { opacity: 0 });
    tl.to(fondo, { opacity: 1, duration: (d.entra_fr || 4) * FR, ease: 'power1.out' }, x.s);
    tl.to(fondo, { opacity: 0, duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
  }
  // le pillole: etichette_luce com'e, nel suo strato (la sua uscita muove solo le pillole)
  MODELLI.etichette_luce(dentro, x, d);
  // giro 2 (direttore, fase 1): sul telefono la barra deve dire «niente». Al posto della barra del modello
  // (che si spegne con la pillola) una barra panna piena, lunga quanto la pillola, con il suo alone, che
  // resta all'85% quando la pillola barrata scende (al 55%, non al 38%). Solo dentro etichette_ads.
  const FR_ = FR;
  [...dentro.querySelectorAll('.el-g')].forEach((g, i) => {
    const v = (d.voci || [])[i];
    if (!v || v.barra_t === undefined) return;
    const p = g.querySelector('.el-pill');
    const b = el('div', 'ea-barra', g);
    const hb = d.barra_px || 10;
    px(b, { left: 0, top: Math.round(p.offsetHeight / 2 - hb / 2), width: p.offsetWidth, height: hb, borderRadius: hb / 2 });
    gsap.set(b, { scaleX: 0, transformOrigin: '0% 50%' });
    tl.to(b, { scaleX: 1, duration: 3.5 * FR_, ease: 'power2.out' }, v.barra_t);
    tl.to(b, { opacity: d.barra_resta || 0.85, duration: 6 * FR_, ease: 'power2.out' }, v.barra_t + 5 * FR_);
    tl.to(p, { opacity: d.barrata || 0.55, filter: 'saturate(0.35)', duration: 6 * FR_, ease: 'power2.out', overwrite: true },
      v.barra_t + 5 * FR_);
  });
};

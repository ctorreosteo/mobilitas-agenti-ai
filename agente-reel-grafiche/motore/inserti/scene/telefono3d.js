// Telefono grande in prospettiva (strato davanti): entra dal basso con parallasse
// (luce dietro e ombra sotto vanno piu piano del telefono), poi le schermate
// scorrono verso l'alto una dopo l'altra; alla fine scende e esce.
// d: schermate [{src, t, w, h}], x (centro), y (centro), alto (px), cambio ('scorre' | 'dissolvenza'),
//    entrata ('posto': nasce dove sta, senza attraversare il bordo; fase 7c)
MODELLI.telefono3d = function (box, x, d) {
  const alto = d.alto || 930;
  const st = el('div', 'tf-stage', box);
  px(st, { left: d.x - 600, top: d.y - alto / 2, width: 1200, height: alto });
  const luce = el('div', 'tf-luce', st);
  const ombra = el('div', 'tf-ombra', st);
  const telefoni = (d.schermate || []).map((s) => {
    const w = el('div', 'tf-tel', st);
    const larg = Math.round(alto * s.w / s.h);
    px(w, { width: larg, height: alto, left: 600 - larg / 2, top: 0 });
    const i = el('img', '', w);
    i.src = s.src;
    gsap.set(w, { opacity: 0, transformPerspective: 1600 });
    return w;
  });
  const t0 = x.s;
  // fase 7c: entrata «sul posto» (d.entrata = 'posto'): il telefono nasce dove sta, piccolo, ruotato e
  // sfocato, senza attraversare il bordo del quadro; luce e ombra in proporzione al telefono
  const POSTO = d.entrata === 'posto';
  if (POSTO) {
    const k = alto / 930;
    px(luce, { left: 600 - 450 * k, top: 60 * k, width: 900 * k, height: 820 * k });
    px(ombra, { left: 600 - 270 * k, bottom: -40 * k, width: 540 * k, height: 90 * k });
    // fase 7c (direttore v4): un alone verde tenue dietro il telefono, cosi non sembra incollato al muro scuro
    luce.style.background = 'radial-gradient(closest-side, rgba(114,250,147,0.34), rgba(114,250,147,0.16) 38%, rgba(0,52,112,0.22) 62%, rgba(0,26,61,0))';
  }
  // parallasse in entrata: luce (lenta), ombra (media), telefono (veloce)
  tl.fromTo(luce, { opacity: 0, x: 160, scale: 0.7 }, { opacity: 1, x: 0, scale: 1, duration: 0.9, ease: 'power3.out' }, t0);
  tl.fromTo(ombra, { opacity: 0, x: 220, scaleX: 0.6 }, { opacity: 1, x: 0, scaleX: 1, duration: 0.7, ease: 'power3.out' }, t0 + 0.04);
  const p0 = telefoni[0];
  if (POSTO) tl.fromTo(p0, { opacity: 0, y: 46, x: 30, scale: 0.84, rotation: 5, rotationY: -40, rotationX: 12, filter: 'blur(12px)' },
    { opacity: 1, y: 0, x: 0, scale: 1, rotation: 0, rotationY: -18, rotationX: 4, filter: 'blur(0px)',
      duration: ENTRA_GRANDE + 4 * FR, ease: 'expo.out', immediateRender: false }, t0);
  else tl.fromTo(p0, { opacity: 1, y: 980, x: 260, rotation: 12, rotationY: -38, rotationX: 14, filter: 'blur(6px)' },
    { opacity: 1, y: 0, x: 0, rotation: 0, rotationY: -10, rotationX: 4, filter: 'blur(0px)',
      duration: ENTRA_GRANDE + 3 * FR, ease: 'expo.out', immediateRender: false }, t0);
  // vivo ma fermo: la rotazione si assesta piano fino al cambio
  const cambi = (d.schermate || []).map((s) => s.t).slice(1);
  const fine0 = cambi.length ? cambi[0] : x.e - ESCE * 2;
  tl.to(p0, { rotationY: POSTO ? -10 : -5, rotationX: 2, duration: Math.max(0.4, fine0 - t0 - 0.6), ease: 'sine.inOut' }, t0 + 0.6);
  // fase 7c: riflesso che attraversa il vetro (d.riflesso_t), mascherato dalla sagoma del telefono
  if (POSTO && d.riflesso_t !== undefined) {
    const s0 = d.schermate[0];
    const rf = el('div', 'tf-riflesso', p0);
    rf.style.webkitMaskImage = `url(${s0.src})`; rf.style.maskImage = `url(${s0.src})`;
    const banda = el('div', 'tf-banda', rf);
    gsap.set(banda, { xPercent: -160, rotation: 18 });
    tl.to(banda, { xPercent: 260, duration: 0.7, ease: 'power2.inOut' }, d.riflesso_t);
  }
  telefoni.slice(1).forEach((w, k) => {
    const prev = telefoni[k];
    const t = d.schermate[k + 1].t;
    if (POSTO) {
      // fase 7c (direttore v4): due render con il telefono in pose diverse non si sovrappongono: quello prima
      // esce sfocandosi in 4 frame, il nuovo entra sul posto mentre l'altro finisce (2 frame insieme, sfocati: mai vuoto)
      tl.to(prev, { opacity: 0, scale: 0.96, filter: 'blur(8px)', duration: 4 * FR, ease: 'power2.in' }, t - 3 * FR);
      tl.fromTo(w, { opacity: 0, y: 0, x: 0, scale: 0.96, rotation: 0, rotationY: -14, rotationX: 3, filter: 'blur(8px)' },
        { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 6 * FR, ease: 'power2.out', immediateRender: false }, t - 2 * FR);
      const fine = k + 2 < telefoni.length ? d.schermate[k + 2].t : x.e - ESCE * 2;
      tl.to(w, { rotationY: -9, rotationX: 2, duration: Math.max(0.4, fine - t - 0.3), ease: 'sine.inOut' }, t + 7 * FR);
      return;
    }
    if (d.cambio === 'dissolvenza') {
      // stessa foto che cambia (es. compaiono gli anelli): il telefono resta fermo, la schermata nuova si dissolve sopra
      tl.fromTo(w, { opacity: 0, y: 0, x: 0, rotation: 0, rotationY: -5, rotationX: 2 },
        { opacity: 1, duration: 8 * FR, ease: 'power2.out', immediateRender: false }, t);
      tl.set(prev, { opacity: 0 }, t + 8 * FR);
      const fine = k + 2 < telefoni.length ? d.schermate[k + 2].t : x.e - ESCE * 2;
      tl.to(w, { rotationY: -3, rotationX: 1, duration: Math.max(0.4, fine - t - 0.4), ease: 'sine.inOut' }, t + 0.3);
      return;
    }
    // scorre: quello prima sale ed esce, il nuovo sale da sotto (stesso verso, stessa velocita al taglio)
    tl.to(prev, { y: -1150, rotationX: 22, scale: 0.94, duration: 12 * FR, ease: 'power3.in' }, t - 6 * FR);
    // resta nascosto fino al suo momento (prima era gia "acceso" fuori quadro, sotto il bordo)
    tl.fromTo(w, { opacity: 1, y: 1150, rotationX: -22, rotationY: -4, scale: 0.94 },
      { opacity: 1, y: 0, rotationX: 3, rotationY: -8, scale: 1, duration: ENTRA_GRANDE + 2 * FR, ease: 'expo.out',
        immediateRender: false }, t + 3 * FR);   // opacita anche nell'arrivo: il render puo saltare oltre l'inizio
    const fine = k + 2 < telefoni.length ? d.schermate[k + 2].t : x.e - ESCE * 2;
    tl.to(w, { rotationY: -4, rotationX: 1, duration: Math.max(0.4, fine - t - 0.7), ease: 'sine.inOut' }, t + 0.7);
  });
  const ultimo = telefoni[telefoni.length - 1];
  if (POSTO) tl.to(ultimo, { opacity: 0, y: 24, scale: 0.92, filter: 'blur(8px)', duration: ESCE * 2, ease: 'power2.in' }, x.e - ESCE * 2);
  else tl.to(ultimo, { y: 1100, rotation: -6, duration: ESCE * 2, ease: 'power3.in' }, x.e - ESCE * 2);
  tl.to([luce, ombra], { opacity: 0, duration: ESCE * 2, ease: 'power2.in' }, x.e - ESCE * 2);
};

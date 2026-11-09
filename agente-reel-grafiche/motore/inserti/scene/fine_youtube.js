// Schermata finale YouTube (tappa 3, Riccardo 30/10/2026): dopo l'ultima parola, 12 s di
// chiusura del brand. Fondo blu notte con la luce e la grana delle schermate, il logo
// Mobilitas in alto e un filo verde sotto. Il resto del quadro resta LIBERO per gli
// elementi finali di YouTube (due riquadri video e il pulsante iscriviti): niente testo,
// niente oggetti (le zone sono in d.zone e le controlla il motore, qui non si disegnano).
// Il fondo copre l'ultimo fotogramma in 10 frame; poi niente sta fermo: la luce scorre
// piano e il logo si avvicina appena (1,00 -> 1,02) per tutti i 12 s.
// d: logo {x, y, larghezza}, filo {x, y, larghezza}
MODELLI.fine_youtube = function (box, x, d) {
  const fondo = el('div', 'fy-fondo', box);
  const luce = el('div', 'fy-luce', fondo);
  const luce2 = el('div', 'fy-luce2', fondo);
  el('div', 'fy-vigna', fondo);
  const grana = el('canvas', 'fy-grana', fondo);
  grana.width = 960; grana.height = 540;
  const g = grana.getContext('2d');
  const im = g.createImageData(960, 540);
  let s = 24680;
  for (let i = 0; i < im.data.length; i += 4) {
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    const v = (s >> 16) & 255;
    im.data[i] = im.data[i + 1] = im.data[i + 2] = v;
    im.data[i + 3] = 255;
  }
  g.putImageData(im, 0, 0);
  const logo = el('img', 'fy-logo', fondo);
  logo.src = 'assets/logo_verde.png';
  // fase 7c (Riccardo): il pittogramma (non ricolorato) su un disco panna accanto al logo;
  // il gruppo disco + logo resta centrato dove stava il logo
  const lh = d.logo.larghezza * 676 / 4915;
  const pg = d.pittogramma === false ? null : Object.assign({ d: Math.round(lh * 1.4), gap: 40 }, d.pittogramma || {});
  const sposta = pg ? (pg.d + pg.gap) / 2 : 0;
  px(logo, { left: d.logo.x + sposta, top: d.logo.y, width: d.logo.larghezza });
  let disco = null;
  if (pg) {
    disco = el('div', 'pittogramma v3-pezzo', fondo);
    px(disco, { left: d.logo.x - sposta, top: d.logo.y + lh / 2 - pg.d / 2, width: pg.d, height: pg.d });
    const pi = el('img', '', disco);
    pi.src = 'assets/pittogramma-sfondo-trasparente.png';
    gsap.set(disco, { opacity: 0, scale: 0.7, filter: 'blur(8px)' });
    tl.to(disco, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 12 * FR, ease: 'back.out(1.4)' }, x.s + 6 * FR);
  }
  const filo = el('div', 'fy-filo', fondo);
  px(filo, { left: d.filo.x, top: d.filo.y, width: d.filo.larghezza });
  const dur = x.e - x.s;
  gsap.set(fondo, { opacity: 0 });
  tl.to(fondo, { opacity: 1, duration: 10 * FR, ease: 'power2.inOut' }, x.s);
  gsap.set(logo, { opacity: 0, y: 26, filter: 'blur(10px)', transformOrigin: '50% 50%' });
  tl.to(logo, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 16 * FR, ease: 'expo.out' }, x.s + 8 * FR);
  tl.fromTo(logo, { scale: 1.0 }, { scale: 1.02, duration: dur - 8 * FR, ease: 'none', immediateRender: false }, x.s + 8 * FR);
  gsap.set(filo, { scaleX: 0, transformOrigin: '50% 50%' });
  tl.to(filo, { scaleX: 1, duration: 14 * FR, ease: 'expo.out' }, x.s + 16 * FR);
  tl.fromTo(luce, { xPercent: -9, opacity: 0.7 }, { xPercent: 9, opacity: 1, duration: dur, ease: 'sine.inOut' }, x.s);
  tl.fromTo(luce2, { xPercent: 6 }, { xPercent: -6, duration: dur, ease: 'sine.inOut' }, x.s);
  for (let t = x.s, k = 0; t < x.e; t += 2 * FR, k++) {
    tl.set(grana, { x: ((k * 37) % 23) - 11, y: ((k * 53) % 19) - 9 }, t);
  }
};

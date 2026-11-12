// Chiusura, secondo tempo (fase 6c): dopo l'ultima parola il quadro lascia il posto
// a una schermata piena del brand: marchio, "Link in descrizione" e la freccia verde
// che scende verso la descrizione. Etichette strutturali, nessuna parola nuova.
// Entra con una tendina dal basso (maschera), il contenuto sale da dietro le maschere.
// d: titolo, t_titolo, freccia {t, rimbalzi}
MODELLI.chiusura = function (box, x, d) {
  const f = el('div', 'ch-fondo', box);
  const c = el('div', 'ch-col', f);
  const SITO = d.forma !== 'classica';     // fase 7c: forma del sito e pittogramma su disco panna
  let disco = null;
  if (SITO) {
    disco = el('div', 'pittogramma ch-pitto', c);
    const pi = el('img', '', disco);
    pi.src = 'assets/pittogramma-sfondo-trasparente.png';
  }
  const logo = el('img', 'ch-logo', c);
  logo.src = 'assets/logo_verde.png';
  const tit = el('div', 'ch-tit', c);
  const t0 = d.titolo || 'Link in descrizione';
  const ts = el('span', '', tit);
  if (SITO) {
    const pz = esc(t0.toLowerCase() + (/[.!?…]$/.test(t0) ? '' : '.')).split(' ');
    pz[pz.length - 1] = `<span class="grad">${pz[pz.length - 1]}</span>`;
    ts.innerHTML = pz.join(' ');
  } else ts.innerHTML = esc(t0);
  maschera(ts);
  gsap.set(ts, { yPercent: 135 });
  const fw = el('div', 'ch-freccia', c);
  frecciaGiu(fw, '#72FA93', 10);
  tl.fromTo(f, { clipPath: 'inset(100% 0% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 10 * FR, ease: 'expo.inOut' }, x.s);
  tl.fromTo(logo, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 10 * FR, ease: 'expo.out' }, x.s + 5 * FR);
  if (disco) tl.fromTo(disco, { opacity: 0, scale: 0.7, filter: 'blur(8px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 12 * FR, ease: 'back.out(1.4)' }, x.s + 3 * FR);
  rivela(ts, (d.t_titolo || x.s) + 7 * FR, { dur: 10 * FR });
  tl.fromTo(fw, { opacity: 0, y: -80 }, { opacity: 1, y: 0, duration: 12 * FR, ease: 'back.out(1.2)' }, x.s + 12 * FR);
  for (let k = 0; k < 4; k++) {
    const t = x.s + 12 * FR + 0.6 + k * 0.56;
    if (t + 0.5 > x.e) break;
    tl.to(fw, { y: 40, duration: 0.17, ease: 'power2.in' }, t);
    tl.to(fw, { y: 0, duration: 0.33, ease: 'back.out(1.0)' }, t + 0.17);
  }
};

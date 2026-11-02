// Card con spessore accanto a lui (fase 7b rivista, reference gadzhi-06): card blu
// notte una sotto l'altra, ognuna sulla parola che la nomina (sfasamento minimo
// 0,25 s). Spessore = bordo superiore chiaro + ombra di contatto + ombra morbida;
// una texture fine. Dentro, facoltativo, un ritaglio di disegno Servier (il motore
// lo ricolora: `disegno`, `ritaglio`, `alto`) con una luce verde sulla zona, e il
// testo con le sue parole.
// d: x, y, larghezza, altezza (di ogni card), spazio, corpo,
//    carte [{testo, t, src, w, h, luce: {cx, cy, rx, ry} (px nella card), sotto, icona (senza disegno: icona su disco)}],
//    attribuzione, icona_px
MODELLI.card_spessore = function (box, x, d) {
  const W = d.larghezza, H = d.altezza, sp = d.spazio || 26, corpo = d.corpo || 54;
  const imgW = d.img_larghezza || Math.round(H * 0.86);
  let ultima = null;   // tappa 3: la card che porta l'attribuzione = la PRIMA con un disegno
  (d.carte || []).forEach((c, i) => {
    const y = d.y + i * (H + sp);
    const k = el('div', 'cs', box);
    if (c.src && !ultima) ultima = k;
    px(k, { left: d.x, top: y, width: W, height: H });
    el('div', 'cs-trama', k);
    if (c.src) {
      const w = el('div', 'cs-img', k);
      px(w, { left: 18, top: 14, width: imgW, height: H - 28 });
      if (c.luce) {
        const l = el('div', 'cs-luce', w);
        px(l, { left: c.luce.cx - c.luce.rx, top: c.luce.cy - c.luce.ry, width: 2 * c.luce.rx, height: 2 * c.luce.ry });
        gsap.set(l, { opacity: 0, scale: 0.6 });
        tl.to(l, { opacity: 1, scale: 1, duration: 12 * FR, ease: 'expo.out' }, c.t + 0.15);
      }
      const im = el('img', '', w);
      im.src = c.src;
      px(im, { width: c.w, height: c.h, left: (imgW - c.w) / 2, top: (H - 28 - c.h) / 2 });
    }
    // fase 7c (direttore v4): senza disegno, un'icona lineare verde su un disco blu notte a sinistra (c.icona)
    let sx = 40;
    if (!c.src && c.icona) {
      const D = d.icona_px || 76;
      const disco = el('div', 'cs-disco', k);
      px(disco, { left: 24, top: (H - D) / 2, width: D, height: D });
      const ic = icona(c.icona, disco, 'cs-ico');
      disegna(ic, c.t + 4 * FR, 12 * FR);
      sx = 24 + D + 24;
    }
    const t = el('div', 'cs-tx', k);
    px(t, { left: c.src ? imgW + 44 : sx, right: 34, fontSize: corpo });
    t.innerHTML = esc(c.testo).replace(/\*([^*]+)\*/g, '<b>$1</b>').replace(/\|/g, '<br>');   // «|» = a capo sulla frase
    gsap.set(k, { opacity: 0, y: 26, scale: 0.94, filter: 'blur(10px)', transformOrigin: '50% 0%' });
    tl.to(k, { opacity: 1, duration: 5 * FR, ease: 'power1.out' }, c.t);
    tl.to(k, { y: 0, scale: 1, filter: 'blur(0px)', duration: 8 * FR, ease: 'power3.out' }, c.t);
  });
  if (d.attribuzione && ultima) {
    // una riga, dentro i margini della card (regola 7b rivista); il testo della card
    // sale per lasciarle posto. Sta nella prima card con un disegno Servier: entra con il
    // primo disegno (tappa 3: nella terza arrivava 3 s dopo i primi due disegni)
    ultima.classList.add('cs-ultima');
    const a = el('div', 'cs-attr', ultima, esc(d.attribuzione));
    px(a, { left: 22, right: 22, bottom: 8 });
  }
  tl.to(box, { opacity: 0, y: -16, filter: 'blur(6px)', duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
};

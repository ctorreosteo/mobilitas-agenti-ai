// Card di design vicino alle mani (strato davanti), fase 6b.
// Blu notte con bordo sottile panna al 14%, angoli ampi, ombra morbida che le
// stacca dal fondo; icona lineare (si disegna) al posto del numero; titolo pieno e
// sottotitolo leggero, centrati, misurati con il font vero (impagina.misura_card:
// la parola piu lunga sta dentro i margini fissi). Entrano dalla mano vera (Vision):
// un filo sottile la lega alla mano per un attimo, poi la card si posa con scala da
// 0,9 e una sfocatura che si scioglie; il contenuto sale da dietro le maschere.
// Posizioni scelte fuori da mani e volto (il controllo lo misura).
// d: card [{titolo, sotto, icona, s, e, x, y, w, h, righe_t, ts, righe_s, ss,
//    margine, icona_px, mano: [x, y]}], raggio
MODELLI.card = function (box, x, d) {
  const R = d.raggio || 44;
  (d.card || []).forEach((c) => {
    // tre livelli: parallasse (dal suo ingresso) > entrata > card che fluttua
    const par = el('div', 'cd-par', box);
    parallasseSu(par, c.s, c.s, c.e, d.prof === undefined ? 1.06 : d.prof);
    const pos = el('div', 'cd-pos', par);
    px(pos, { left: c.x, top: c.y, width: c.w, height: c.h });
    const k = el('div', 'cd', pos);
    k.style.borderRadius = R + 'px';
    k.style.padding = '0 ' + c.margine + 'px';
    const ic = el('div', 'cd-ic', k);
    px(ic, { width: c.icona_px, height: c.icona_px, marginBottom: c.gap_icona || 22 });
    const s = icona(c.icona || 'lista', ic);
    tl.fromTo(ic, { scale: 0.6 }, { scale: 1, duration: 11 * FR, ease: RIMBALZO }, c.s + 4 * FR);
    const righe = [];
    c.righe_t.forEach((r) => {
      const g = el('div', 'cd-t', k);
      g.style.fontSize = c.ts + 'px';
      const t = el('span', '', g, esc(r));
      maschera(t);
      righe.push(t);
    });
    c.righe_s.forEach((r, i) => {
      const g = el('div', 'cd-s' + (i === 0 ? ' cd-s0' : ''), k);
      g.style.fontSize = c.ss + 'px';
      const t = el('span', '', g, esc(r));
      maschera(t);
      righe.push(t);
    });
    // origine della trasformazione verso la mano: la card "esce" da li
    // nasce sulla mano (Vision, posizione all'arrivo) piccola e sfocata e vola al suo
    // posto su una curva in 9 frame: il legame con la mano e il movimento stesso
    const verso = (c.x + c.w / 2) < 960 ? 1 : -1;      // il lato vicino a lui va piu lontano
    gsap.set(k, { opacity: 0, transformPerspective: 1500, rotationY: verso * 8, transformOrigin: '50% 50%' });
    const t0 = c.s - 4 * FR;          // il volo si vede (4+ fotogrammi) e a +2 il titolo si legge
    const dx = c.mano ? c.mano[0] - (c.x + c.w / 2) : 0, dy = c.mano ? c.mano[1] - (c.y + c.h / 2) : 160;
    tl.fromTo(k, { opacity: 0, filter: 'blur(16px)' }, { opacity: 1, filter: 'blur(0px)', duration: 7 * FR, ease: 'power2.out' }, t0);
    tl.fromTo(pos, { x: dx, scale: 0.3 }, { x: 0, scale: 1, duration: 8 * FR, ease: 'power3.out' }, t0);
    tl.fromTo(pos, { y: dy }, { y: 0, duration: 8 * FR, ease: 'power2.out' }, t0);
    disegna(s, t0 + 3 * FR, 14 * FR);
    const nt = c.righe_t.length;
    righe.forEach((r, i) => {
      const ts = i >= nt && c.sotto_t !== undefined ? c.sotto_t + (i - nt) * 2.5 * FR : t0 + i * 2 * FR;
      rivela(r, ts, { dur: 7 * FR });
    });
    fluttua(k, t0 + 14 * FR, c.e - ESCE, 5, 3.2);
    // uscita piu corta: si stringe un poco, si sfoca, sparisce
    tl.to(k, { opacity: 0, scale: 0.95, filter: 'blur(10px)', duration: ESCE, ease: 'power2.in' }, c.e - ESCE);
  });
};

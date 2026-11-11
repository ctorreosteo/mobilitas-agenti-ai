// La lista dei tentativi (fase 7b): una colonna che si allunga e torna fra le
// animazioni. Trattini, non spunte: i tentativi non sono traguardi. Le voci che
// c'erano gia entrano insieme all'inizio, quella nuova sulla sua parola; sotto
// una voce puo stare una riga piccola (le sue parole).
// d: x, y (alto), larghezza, corpo, voci [{testo, t, sotto, nuova}], strato dietro di solito
MODELLI.tentativi = function (box, x, d) {
  const col = el('div', 'tt-col', box);
  px(col, { left: d.x, top: d.y, width: d.larghezza || 560 });
  const fondo = el('div', 'tt-fondo', col);
  const righe = [];
  d.voci.forEach((v, k) => {
    const r = el('div', 'tt-voce', col);
    const tr = el('div', 'tt-tratto', r);
    const t = el('div', 'tt-et', r);
    t.style.fontSize = (d.corpo || 58) + 'px';
    t.style.maxWidth = ((d.larghezza || 560) - 60) + 'px';
    const s = el('span', '', t, esc(v.testo));
    maschera(s);
    gsap.set(s, { yPercent: 135 });
    const ti = v.nuova ? v.t : x.s + (2 + 3 * k) * FR;
    tl.fromTo(tr, { scaleX: 0 }, { scaleX: 1, duration: 8 * FR, ease: 'expo.out' }, ti);
    rivela(s, ti + 2 * FR, { dur: 10 * FR });
    righe.push(tr, s);
    if (v.sotto) {
      const so = el('div', 'tt-sotto', col);
      so.style.fontSize = Math.round((d.corpo || 58) * 0.68) + 'px';
      so.style.width = ((d.larghezza || 560) - 170) + 'px';
      const ss = el('span', '', so, esc(v.sotto));
      maschera(ss);
      gsap.set(ss, { yPercent: 135 });
      rivela(ss, v.sotto_t !== undefined ? v.sotto_t : ti + 8 * FR, { dur: 10 * FR });
      righe.push(ss);
    }
  });
  tl.fromTo(fondo, { opacity: 0, scaleY: 0.9 }, { opacity: 1, scaleY: 1, duration: ENTRA, ease: 'expo.out' }, x.s);
  righe.slice().reverse().forEach((s, k) => tl.to(s, { opacity: 0, y: 24, duration: ESCE, ease: 'power3.in' }, x.e - ESCE - k * 0.5 * FR));
  tl.to(fondo, { opacity: 0, duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
};

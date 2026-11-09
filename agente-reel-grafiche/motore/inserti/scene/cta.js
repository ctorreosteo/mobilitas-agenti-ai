// Invito all'azione, fase 6b: un momento forte. Il quadro e gia diventato una
// finestra a sinistra (effetto di piatto `finestra`); a destra, sul fondo del brand,
// "Link in descrizione" enorme (righe misurate sulla colonna), parola per parola da
// dietro le maschere, poi una freccia verde grande che cade e rimbalza verso il basso,
// dove sta la descrizione. Il verde sta sul blu del fondo.
// d: x, larghezza, centro_y, righe [{parole [{testo, t}], corpo, peso}], freccia {t, rimbalzi, alto}
MODELLI.cta = function (box, x, d) {
  const col = el('div', 'ct-col', box);
  px(col, { left: d.x, width: d.larghezza, top: 0, height: 1080 });
  const blocco = el('div', 'ct-blocco', col);
  const parole = [];
  const SITO = d.forma !== 'classica';     // fase 7c: minuscolo con il punto, l'ultima parola in gradiente
  const nr = d.righe.length;
  d.righe.forEach((r, ir) => {
    const g = el('div', 'ct-riga', blocco);
    g.style.fontSize = r.corpo + 'px';
    g.style.fontWeight = r.peso || 900;
    r.parole.forEach((p, i) => {
      if (i) g.appendChild(document.createTextNode(' '));
      const ultima = ir === nr - 1 && i === r.parole.length - 1;
      let tx = SITO ? p.testo.toLowerCase() : p.testo;
      if (SITO && ultima && !/[.!?…]$/.test(tx)) tx += '.';
      const s = el('span', 'ct-w' + (SITO && ultima ? ' grad' : ''), g, esc(tx));
      maschera(s);
      gsap.set(s, { yPercent: 135 });
      rivela(s, p.t, { dur: 10 * FR });
      parole.push(s);
    });
  });
  const f = d.freccia;
  const fw = el('div', 'ct-freccia', blocco);
  const A = f.alto || 190;
  px(fw, { width: A * 0.72, height: A });
  const sv = svg('svg', { viewBox: '0 0 80 110' }, fw);
  svg('path', { d: 'M40 8 L40 96 M12 68 L40 98 L68 68', fill: 'none', stroke: '#72FA93', 'stroke-width': 10,
    'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, sv);
  // cade dall'alto con un rimbalzo, poi rimbalza verso il basso (giu veloce, su morbido)
  tl.fromTo(fw, { opacity: 0, y: -140 }, { opacity: 1, y: 0, duration: 12 * FR, ease: 'back.out(1.2)' }, f.t);
  for (let k = 0; k < (f.rimbalzi || 3); k++) {
    const t = f.t + 0.62 + k * 0.56;
    if (t + 0.5 > x.e - ESCE) break;
    tl.to(fw, { y: 46, duration: 0.17, ease: 'power2.in' }, t);
    tl.to(fw, { y: 0, duration: 0.33, ease: 'back.out(1.0)' }, t + 0.17);
  }
  // esce in un blocco solo (niente parole che si scontrano)
  tl.to(blocco, { y: -40, opacity: 0, filter: 'blur(6px)', duration: ESCE, ease: 'power3.in' }, x.e - ESCE);
};

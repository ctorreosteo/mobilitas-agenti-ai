// Lista d'attesa, fase 6b (nella stessa finestra della CTA): niente modulo a fil di
// ferro. Titolo enorme e, sotto, le cose che dice di lasciare, ognuna sulla sua
// parola: sale da dietro la maschera e la spunta verde si posa con un rimbalzo e
// si disegna. Nessun dato inventato.
// d: x, larghezza, centro_y, titolo {testo, t, corpo}, voci [{testo, t}], corpo_voci, spunta
MODELLI.lista_attesa = function (box, x, d) {
  const col = el('div', 'la-col', box);
  px(col, { left: d.x, width: d.larghezza, top: 0, height: 1080 });
  const b = el('div', 'la-blocco', col);
  const tit = el('div', 'la-tit', b);
  tit.style.fontSize = d.titolo.corpo + 'px';
  // fase 7c: forma del sito (minuscolo con il punto, l'ultima parola in gradiente); forma: 'classica' = come prima
  let tt = d.forma === 'classica' ? esc(d.titolo.testo) : esc(d.titolo.testo.toLowerCase() + (/[.!?…]$/.test(d.titolo.testo) ? '' : '.'));
  if (d.forma !== 'classica') { const pz = tt.split(' '); pz[pz.length - 1] = `<span class="grad">${pz[pz.length - 1]}</span>`; tt = pz.join(' '); }
  const ts = el('span', '', tit);
  ts.innerHTML = tt;
  maschera(ts);
  gsap.set(ts, { yPercent: 135 });
  rivela(ts, d.titolo.t, { dur: 11 * FR });
  const filo = el('div', 'la-filo', b);
  tl.fromTo(filo, { scaleX: 0 }, { scaleX: 1, duration: 14 * FR, ease: 'expo.out' }, d.titolo.t + 4 * FR);
  const tutti = [ts];
  d.voci.forEach((v) => {
    const r = el('div', 'la-voce', b);
    const sp = el('div', 'la-spunta', r);
    px(sp, { width: d.spunta || 84, height: d.spunta || 84 });
    const s = svg('svg', { viewBox: '0 0 40 40' }, sp);
    const segno = svg('path', { d: 'M10 21 L17 28 L30 13', class: 'la-segno', pathLength: 1,
      'stroke-dasharray': '1 1', 'stroke-dashoffset': 1 }, s);
    const t = el('div', 'la-et', r);
    t.style.fontSize = d.corpo_voci + 'px';
    const tt = el('span', '', t, esc(v.testo));
    maschera(tt);
    gsap.set(tt, { yPercent: 135 });
    // la riga c'e gia (spenta, cerchio vuoto) insieme al titolo; sulla parola si accende
    const tr = d.titolo.t + (6 + 3 * d.voci.indexOf(v)) * FR;
    rivela(tt, tr, { dur: 9 * FR });
    gsap.set(t, { opacity: 0.6 });
    tl.to(t, { opacity: 1, duration: 6 * FR, ease: 'power2.out' }, v.t);
    gsap.set(sp, { scale: 1, backgroundColor: 'rgba(114,250,147,0)', boxShadow: 'inset 0 0 0 4px rgba(244,244,244,0.45)', opacity: 0 });
    tl.to(sp, { opacity: 1, duration: 6 * FR }, tr + 2 * FR);
    tl.to(sp, { backgroundColor: '#72FA93', boxShadow: 'inset 0 0 0 0px rgba(244,244,244,0)', duration: 6 * FR, ease: 'power2.out' }, v.t + 2 * FR);
    tl.fromTo(sp, { scale: 1 }, { scale: 1.12, duration: 4 * FR, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }, v.t + 2 * FR);
    tl.to(segno, { attr: { 'stroke-dashoffset': 0 }, duration: 8 * FR, ease: 'power2.out' }, v.t + 7 * FR);
    tutti.push(tt, sp);
  });
  tutti.slice().reverse().forEach((s, k) => tl.to(s, { opacity: 0, y: 30, duration: ESCE, ease: 'power3.in' }, x.e - ESCE - k * 0.5 * FR));
  tl.to(filo, { scaleX: 0, duration: ESCE, ease: 'power3.in' }, x.e - ESCE);
};

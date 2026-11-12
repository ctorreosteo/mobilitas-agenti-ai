// Frase chiave, variante B dei sottotitoli (fase 7b): pannello blu a tutta altezza
// su un lato, la persona sta dall'altro (la camera del momento la sposta). La
// frase e detta da lui, parola per parola; la parola chiave e in menta 800.
// Le righe salgono da dietro la maschera, sfalsate; il pannello entra e esce di lato.
// d: lato (sx|dx), larghezza, corpo, parole [{testo, chiave}], margine
MODELLI.frase_chiave = function (box, x, d) {
  const lato = d.lato || 'sx';
  const L = d.larghezza || 760;
  const pan = el('div', 'fk-pan', box);
  px(pan, { width: L, top: 0, height: 1080 });
  pan.style[lato === 'sx' ? 'left' : 'right'] = '0px';
  const fil = el('div', 'fk-filo', pan);
  const testo = el('div', 'fk-testo', pan);
  px(testo, { left: d.margine || 96, right: (d.margine || 96) - 10 });
  testo.style.fontSize = (d.corpo || 64) + 'px';
  const parole = (d.parole || []).map((p) => {
    const s = el('span', p.chiave ? 'fk-chiave' : 'fk-p', testo, esc(p.testo));
    testo.appendChild(document.createTextNode(' '));
    return s;
  });
  const dir = lato === 'sx' ? -1 : 1;
  tl.fromTo(pan, { xPercent: 100 * dir }, { xPercent: 0, duration: ENTRA_GRANDE, ease: 'expo.out' }, x.s);
  tl.fromTo(fil, { scaleY: 0 }, { scaleY: 1, duration: 16 * FR, ease: 'expo.out' }, x.s + 4 * FR);
  parole.forEach((s, k) => {
    tl.fromTo(s, { opacity: 0, y: 26, filter: 'blur(8px)' },
      { opacity: 1, y: 0, filter: 'blur(0px)', duration: ENTRA, ease: 'expo.out', immediateRender: true },
      x.s + 6 * FR + k * 1.2 * FR);
  });
  tl.to(parole, { opacity: 0, duration: ESCE, ease: 'power2.in' }, x.e - ESCE * 2);
  tl.to(pan, { xPercent: 100 * dir, duration: ESCE * 1.5, ease: 'power3.in' }, x.e - ESCE * 1.5);
};

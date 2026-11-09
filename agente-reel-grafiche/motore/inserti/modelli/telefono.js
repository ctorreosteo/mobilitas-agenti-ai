// App: le schermate entrano a ventaglio una dopo l'altra sul pannello. Accetta
// render gia scontornati (tipo 'render', il telefono c'e gia) e schermate piatte
// (tipo 'piatta': il telefono lo disegna il modello). DATI: lato, schermate
// [{src, tipo, t}], chiave {t, testo}
const lato = D.lato || 'dx';
const p = pannello(lato);
muoviPannello(p, lato);
const sch = (D.schermate || []);
const n = sch.length;
sch.forEach((s, i) => {
  const box = el('div', 'schermata ' + (s.tipo === 'piatta' ? 'piatta' : 'render'), p);
  const im = el('img', '', box);
  im.src = s.src;
  const t = Math.max(0.25, s.t || 0.25 + i * 1.6);
  // posizione finale: le precedenti scivolano indietro e a sinistra
  tl.fromTo(box, { xPercent: 30, x: 200, opacity: 0, rotation: 6, scale: 0.94 },
    { xPercent: -50, x: 0, opacity: 1, rotation: 0, scale: 1, duration: 0.6, ease: 'expo.out' }, t);
  for (let j = i + 1; j < n; j++) {
    const tj = Math.max(0.25, sch[j].t || 0.25 + j * 1.6);
    const k = j - i;
    tl.to(box, { x: -110 * k, scale: 1 - 0.07 * k, opacity: k > 1 ? 0 : 0.55, rotation: -4 * k,
      duration: 0.55, ease: 'expo.out' }, tj);
  }
  box.style.zIndex = 10 + i;
});
if (D.chiave) {
  const ch = el('div', 'chiave', p, frase(D.chiave.testo, true));
  ch.style.zIndex = 50;
  entra(ch, Math.max(0.3, D.chiave.t - 0.05));
}
chiudi();

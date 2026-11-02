// Frase parola per parola (fase 7b rivista, reference martell-07 e martell-01):
// ogni parola nasce panna al 35% e sfocata e in 3 frame diventa piena, sulla voce.
// La parola chiave e piu pesante e verde (solo su fondo blu: con `chiave_verde`
// false resta panna 900). Ombra morbida forte dietro (regola delle scritte
// bianche sulla scena). Facoltativo `vetro`: pannello smerigliato dietro la frase
// (bordo e riflesso qui; la sfocatura dello studio la fa il compositore, effetto
// di piatto `vetro` con la stessa geometria).
// d: x, y, larghezza, corpo, peso, interlinea, allinea, chiave_verde,
//    parole [{testo, t, chiave}], vetro {x, y, larghezza, altezza, raggio, t, rampa}
MODELLI.frase_luce = function (box, x, d) {
  if (d.vetro) {
    const v = d.vetro;
    const g = el('div', 'fl-vetro' + (v.forte ? ' fl-forte' : ''), box);   // v3: più luce
    px(g, { left: v.x, top: v.y, width: v.larghezza, height: v.altezza, borderRadius: v.raggio || 40 });
    const rf = el('div', 'fl-riflesso', g);
    if (v.forte) {
      // v3: il riflesso passa sul vetro quando arriva (luce che lo attraversa)
      const tv = v.t !== undefined ? v.t : x.s;
      tl.fromTo(rf, { xPercent: 0 }, { xPercent: 900, duration: 10 * FR, ease: 'power2.inOut', immediateRender: false }, tv + 0.1);
      // alone verde solo in entrata, poi scende
      tl.fromTo(g, { boxShadow: 'inset 0 2px 0 rgba(244,244,244,0.55), inset 0 0 60px rgba(0,26,61,0.2), 0 0 26px rgba(114,250,147,0.45), 0 30px 70px rgba(0,8,22,0.45)' },
        { boxShadow: 'inset 0 2px 0 rgba(244,244,244,0.55), inset 0 0 60px rgba(0,26,61,0.2), 0 0 22px rgba(114,250,147,0.15), 0 30px 70px rgba(0,8,22,0.45)',
          duration: 0.6, ease: 'power2.out', immediateRender: false }, tv + 0.35);
      const fl = el('div', 'fl-filo', g);
      gsap.set(fl, { scaleX: 0, transformOrigin: '0% 50%' });
      tl.to(fl, { scaleX: 1, duration: 0.5, ease: 'power3.out' }, (v.t !== undefined ? v.t : x.s));
    }
    gsap.set(g, { opacity: 0 });
    tl.to(g, { opacity: 1, duration: v.rampa || 0.3, ease: 'power2.out' }, v.t !== undefined ? v.t : x.s);
    tl.to(g, { opacity: 0, duration: v.rampa || 0.3, ease: 'power2.in' }, x.e - (v.rampa || 0.3));
  }
  const f = el('div', 'fl-frase' + (d.allinea === 'dx' ? ' fl-dx' : d.allinea === 'centro' ? ' fl-centro' : ''), box);
  px(f, { left: d.x, top: d.y, width: d.larghezza, fontSize: d.corpo || 80, lineHeight: String(d.interlinea || 1.08) });
  f.style.fontWeight = d.peso || 600;
  (d.parole || []).forEach((p) => {
    if (p.a_capo) el('br', '', f);
    const w = el('span', 'fl-w' + (p.chiave ? (d.chiave_verde === false ? ' fl-k fl-kp' : ' fl-k') : ''), f, esc(p.testo));
    gsap.set(w, { opacity: 0.0, filter: 'blur(10px)', y: 10 });
    tl.to(w, { opacity: 0.35, duration: 1 * FR }, Math.max(0, p.t - 1 * FR));
    tl.to(w, { opacity: 1, filter: 'blur(0px)', y: 0, duration: 3 * FR + 0.04, ease: 'power2.out' }, p.t);
    f.appendChild(document.createTextNode(' '));
  });
  tl.to(f, { opacity: 0, y: -10, filter: 'blur(8px)', duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
};

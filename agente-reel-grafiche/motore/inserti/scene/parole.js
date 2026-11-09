// Frase sul corpo (strato davanti), fase 6b: una o due parole ENORMI per volta
// (peso 900), sul busto sotto il volto, a battute. Ogni parola sale da dietro la sua
// maschera sulla parola detta; la riga arriva con un piccolo colpo di scala; ombra
// morbida di profondita (fuori dalle maschere, cosi non si taglia). Escono
// scendendo dentro le maschere. Corpo, centro e altezza li misura il motore
// (impagina.piazza_battute) sul font vero e sul volto di Vision.
// d: battute [{parole: [{testo, t}], s, e, corpo, cx, top, chiave}]
MODELLI.parole = function (box, x, d) {
  d.battute.forEach((b) => {
    const riga = el('div', 'pa-riga', box);
    px(riga, { top: b.top, left: b.cx - 960, width: 1920, fontSize: b.corpo });
    const dentro = el('div', 'pa-dentro', riga);
    const parole = b.parole.map((p, i) => {
      if (i) {
        const sp = el('span', '', dentro, ' ');
        const q = b.parole[i - 1].scala || 1;
        if (q < 1) sp.style.fontSize = q + 'em';
      }
      const s = el('span', 'pa-w', dentro, esc(p.testo));
      if (p.scala) s.style.fontSize = p.scala + 'em';
      if (p.peso) s.style.fontWeight = p.peso;
      maschera(s);
      gsap.set(s, { yPercent: 135 });
      rivela(s, p.t, { dur: 9 * FR });
      // fase 7c (direttore): il primo frame della salita mostrava solo le cime delle aste («U» -> «- -»):
      // la parola nasce sfocata e trasparente e in 5 frame diventa piena
      tl.fromTo(s, { opacity: 0, filter: 'blur(9px)' }, { opacity: 1, filter: 'blur(0px)', duration: 5 * FR, ease: 'power2.out', immediateRender: false }, p.t);
      return s;
    });
    // colpo di scala della riga sulla prima parola e pressione sulla chiave
    gsap.set(dentro, { transformOrigin: '50% 60%' });
    tl.fromTo(dentro, { scale: (b._larghezza || 0) > 1400 ? 1.03 : 1.10 }, { scale: 1, duration: 12 * FR, ease: 'expo.out' }, b.parole[0].t);
    if (b.chiave !== undefined) {
      tl.fromTo(dentro, { scale: 1.05 }, { scale: 1, duration: 10 * FR, ease: 'power3.out', immediateRender: false }, b.chiave);
    }
    parole.slice().reverse().forEach((s, k) => nascondi(s, b.e - ESCE - k * FR, { dir: 'giu' }));
  });
};

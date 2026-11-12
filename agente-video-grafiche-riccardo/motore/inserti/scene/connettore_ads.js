// Connettore detto per gli ads 9:16, nella finestra (laboratorio, AD_REFLUSSO, 04/11/2026). Modello nuovo, da
// connettore (che resta com'e), reference gadzhi-11 e gadzhi-13. In testa una riga panna che resta per tutta la grafica
// («pensato per»); sotto, due etichette dette in colonna (riquadri a pillola dal bordo luminoso) unite da una linea verde
// verticale che si disegna dal centro, con un nodo luminoso in mezzo (gadzhi-11 in verticale). Poi le etichette escono in
// 2 fotogrammi e, solo dopo, entra il risultato in verde con la barra che cresce a scatti sotto (gadzhi-13): mai due stati
// sovrapposti. Fondo pieno della finestra a taglio all'entrata e all'uscita, alfa 0 fuori dal rettangolo, che cambia sul
// taglio d'inquadratura come in equazione_ads2. Niente decifrazioni (nessun carattere provvisorio).
// d: rett [{da, x, y, w, h, r}], testa {testo, t, y, corpo}, etichette [{testo, t, y}], larghezza, altezza, raggio, corpo,
//    nodo {t, y, lato}, t_via, risultato [{testo, t, y, corpo, verde, luce}], barra {t, y, larghezza}
MODELLI.connettore_ads = function (box, x, d) {
  const QW = 1080, EPS = 0.001;
  const clip = el('div', 'cfa-clip', box);
  const fondo = el('div', 'cfa-fondo fondo-sito', clip);
  const dentro = el('div', 'cfa-dentro', clip);
  const RR = Array.isArray(d.rett) ? d.rett : [Object.assign({ da: 0 }, d.rett)];
  const metti = (R, t) => {
    const a = { left: R.x + 'px', top: R.y + 'px', width: R.w + 'px', height: R.h + 'px', borderRadius: R.r + 'px' };
    const f = { width: R.w + 'px', height: R.h + 'px' }, dd = { left: -R.x + 'px', top: -R.y + 'px' };
    if (t === undefined) { gsap.set(clip, a); gsap.set(fondo, f); gsap.set(dentro, dd); }
    else { tl.set(clip, a, t - EPS); tl.set(fondo, f, t - EPS); tl.set(dentro, dd, t - EPS); }
  };
  metti(RR[0]);
  RR.slice(1).forEach((R) => metti(R, R.da));      // sul taglio d'inquadratura la finestra cambia di 1-5 px
  gsap.set(clip, { opacity: 0 });
  tl.set(clip, { opacity: 1 }, x.s);                // entra a taglio con il fondo gia pieno
  tl.set(clip, { opacity: 0 }, x.e - EPS);          // esce a taglio sull'ultimo fotogramma
  el('div', 'cfa-alone', dentro);                   // luce morbida dietro il contenuto (statica)

  const corpo = d.corpo || 84, H = d.altezza || 100, L = d.larghezza || 930;
  // una riga di testo centrata (nessuna maschera: lettere e bagliori interi)
  const riga = (cls, y, cp) => {
    const r = el('div', 'cfa-riga ' + cls, dentro);
    const lh = Math.round(cp * 1.2);
    px(r, { top: y - lh / 2, height: lh, lineHeight: lh + 'px', fontSize: cp });
    return r;
  };
  // entrata: c'e gia dal suo tempo (opacita parziale), si mette a fuoco in pochi fotogrammi con un rimbalzo piccolo
  const nasce = (e, t, o) => {
    o = o || {};
    tl.fromTo(e, { opacity: o.op0 === undefined ? 0.45 : o.op0, scale: o.da || 0.92, filter: `blur(${o.blur || 8}px)` },
      { opacity: 1, scale: 1, filter: 'blur(0px)', duration: (o.fr || 5) * FR, ease: o.ease || 'back.out(1.4)',
        immediateRender: false }, t);
  };

  // «pensato per»: panna, in testa per tutta la grafica
  if (d.testa) {
    const r = riga('cfa-testa', d.testa.y, d.testa.corpo || corpo);
    const s = el('span', 'cfa-t', r, esc(d.testa.testo));
    gsap.set(s, { opacity: 0 });
    tl.set(s, { opacity: 1 }, d.testa.t);
    nasce(s, d.testa.t, { op0: 0.7, blur: 5, da: 0.97, fr: 4, ease: 'expo.out' });
  }

  // le etichette in colonna, con la linea e il nodo: escono insieme in 2 fotogrammi prima del risultato
  const fase1 = el('div', 'cfa-fase1', dentro);
  const tVia = d.t_via !== undefined ? d.t_via : x.e;
  const pezzi = [];
  (d.etichette || []).forEach((e) => {
    const p = el('div', 'cfa-et', fase1);
    px(p, { left: (QW - L) / 2, top: e.y - H / 2, width: L, height: H, lineHeight: H + 'px', fontSize: corpo,
      borderRadius: d.raggio !== undefined ? d.raggio : H / 2 });
    el('span', 'cfa-et-t', p, esc(e.testo));
    gsap.set(p, { opacity: 0 });
    tl.set(p, { opacity: 1 }, e.t);
    nasce(p, e.t, { op0: 0.4, blur: 10, da: 0.9, fr: 6 });
    // un lampo sul bordo quando arriva (la luce si posa)
    tl.fromTo(p, { boxShadow: '0 0 34px rgba(141,255,169,1), 0 0 110px rgba(114,250,147,0.7), inset 0 0 40px rgba(114,250,147,0.7)' },
      { boxShadow: '0 0 16px rgba(141,255,169,0.85), 0 0 56px rgba(114,250,147,0.4), inset 0 0 24px rgba(114,250,147,0.4)',
        duration: 12 * FR, ease: 'power2.out', immediateRender: false }, e.t);
    pezzi.push(p);
  });
  if (d.nodo && d.etichette && d.etichette.length >= 2) {
    const yA = d.etichette[0].y + H / 2, yB = d.etichette[1].y - H / 2, ym = d.nodo.y, lato = d.nodo.lato || 56;
    const su = el('div', 'cfa-linea', fase1), giu = el('div', 'cfa-linea', fase1);
    px(su, { left: QW / 2 - 4, top: yA, height: ym - yA });
    px(giu, { left: QW / 2 - 4, top: ym, height: yB - ym });
    gsap.set(su, { scaleY: 0, transformOrigin: '50% 100%' });     // dal centro verso le due etichette
    gsap.set(giu, { scaleY: 0, transformOrigin: '50% 0%' });
    tl.to([su, giu], { scaleY: 1, duration: 6 * FR, ease: 'power3.out' }, d.nodo.t + 2 * FR);
    const n = el('div', 'cfa-nodo', fase1);
    px(n, { left: QW / 2 - lato / 2, top: ym - lato / 2, width: lato, height: lato });
    const ic = svg('svg', { viewBox: '0 0 54 54', class: 'cfa-ico' }, n);
    [[20, 27], [34, 27]].forEach(([cx, cy]) => svg('circle', { cx, cy, r: 12, fill: 'none', stroke: '#A9FFBE', 'stroke-width': 4.5 }, ic));
    gsap.set(n, { scale: 0, opacity: 0 });
    tl.to(n, { scale: 1, opacity: 1, duration: 5 * FR, ease: 'back.out(2.2)' }, d.nodo.t + 4 * FR);
    tl.fromTo(n, { filter: 'brightness(1.6)' }, { filter: 'brightness(1)', duration: 10 * FR, ease: 'power2.out', immediateRender: false },
      d.nodo.t + 8 * FR);
  }
  // uscita della prima fase: 2 fotogrammi che finiscono prima del risultato (nessun fotogramma con i due stati)
  const t1 = (d.risultato && d.risultato.length ? Math.min(tVia, d.risultato[0].t) : tVia) - 2 * FR;
  tl.to(fase1, { opacity: 0, y: -26, scale: 0.96, filter: 'blur(6px)', duration: 2 * FR, ease: 'power2.in' }, t1);
  tl.set(fase1, { display: 'none' }, t1 + 2 * FR);

  // il risultato in verde, poi la barra che cresce a scatti con la punta chiara
  (d.risultato || []).forEach((r) => {
    const cp = r.corpo || corpo;
    const rg = riga('cfa-ris', r.y, cp);
    const s = el('span', 'cfa-t' + (r.verde ? ' cfa-k' : ''), rg, esc(r.testo));
    gsap.set(s, { opacity: 0 });
    tl.set(s, { opacity: 1 }, r.t);
    nasce(s, r.t, { op0: 0.35, blur: 10, da: 0.9, fr: 6, ease: 'back.out(1.3)' });
    if (r.luce !== undefined) {
      tl.fromTo(rg, { filter: 'brightness(1)' }, { filter: 'brightness(1.4)', duration: 3 * FR, ease: 'power2.out', immediateRender: false }, r.luce);
      tl.to(rg, { filter: 'brightness(1)', duration: 9 * FR, ease: 'power2.out' }, r.luce + 3 * FR);
    }
  });
  if (d.barra) {
    const b = el('div', 'cfa-barra', dentro);
    px(b, { left: (QW - d.barra.larghezza) / 2, top: d.barra.y - 5, width: d.barra.larghezza });
    el('div', 'cfa-punta', b);
    // cresce in larghezza (la punta resta tonda), a scatti come una barra di avanzamento
    gsap.set(b, { width: 0, opacity: 0 });
    tl.set(b, { opacity: 1 }, d.barra.t);
    [0.25, 0.5, 0.75, 1.0].forEach((v, k) => tl.to(b, { width: d.barra.larghezza * v, duration: 3 * FR, ease: 'power2.out' },
      d.barra.t + k * 5 * FR));
  }
};

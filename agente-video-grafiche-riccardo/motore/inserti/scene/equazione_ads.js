// Equazione detta per gli ads 9:16, nella finestra (laboratorio, fase 3, 04/11/2026). Modello nuovo,
// rifatto su equazione (che resta com'e): i termini detti si decifrano sulla voce, + e = verdi come etichette
// strutturali, il risultato con la parola chiave in verde; esce cancellandosi all'indietro. Cambiano: il posto
// (la finestra grande in alto del video base, al posto del B-roll, con il rettangolo che cambia sul taglio
// d'inquadratura), le righe centrate una sotto l'altra, e la decifrazione: caratteri provvisori solo lettere,
// della stessa larghezza, niente aste sole (regola: mai numeri non detti, nemmeno per un fotogramma).
// d: rett [{da, x, y, w, h, r}] (da = tempo da cui vale), righe [{op, testo, t, chiave, y}], corpo, t_via,
//    cancella_fr, sfalsa_fr, entra_fr
function eqDecifra(cont, testo, t0, nf, seme) {
  const r = semi(seme || testo.length * 31 + 7);
  const insieme = (c) => /[tfr]/.test(c) ? 'tfr' : /[mw]/.test(c) ? 'mw' : 'acenosuvxz';
  nf = Math.max(nf, 12);
  const vero = el('span', 'dc-vero', cont, esc(testo));
  gsap.set(vero, { opacity: 0 });
  for (let k = 0; k < nf; k++) {
    const fermi = Math.floor(testo.length * (k + 1) / (nf + 1));
    let s = '';
    for (let i = 0; i < testo.length; i++) {
      const c = testo[i], cs = insieme(c);
      s += (i < fermi || c === ' ' || /[0-9ilj]/.test(c) || /[^A-Za-zÀ-ÿ]/.test(c)) ? c : cs[Math.floor(r() * cs.length)];
    }
    const sp = el('span', 'dc-strato', cont, esc(s));
    gsap.set(sp, { opacity: 0 });
    tl.set(sp, { opacity: 1 }, t0 + k * FR);
    tl.set(sp, { opacity: 0 }, t0 + (k + 1) * FR);
  }
  tl.set(vero, { opacity: 1 }, t0 + nf * FR);
  return vero;
}

MODELLI.equazione_ads = function (box, x, d) {
  const QW = 1080, QH = 1920, EPS = 0.001;
  const R0 = d.rett[0];
  const clip = el('div', 'eqa-clip', box);
  const fondo = el('div', 'eqa-fondo fondo-sito', clip);
  const dentro = el('div', 'eqa-dentro', clip);
  const metti = (R, t) => {
    const a = { left: R.x + 'px', top: R.y + 'px', width: R.w + 'px', height: R.h + 'px', borderRadius: R.r + 'px' };
    const f = { width: R.w + 'px', height: R.h + 'px' }, dd = { left: -R.x + 'px', top: -R.y + 'px' };
    if (t === undefined) { gsap.set(clip, a); gsap.set(fondo, f); gsap.set(dentro, dd); }
    else { tl.set(clip, a, t - EPS); tl.set(fondo, f, t - EPS); tl.set(dentro, dd, t - EPS); }
  };
  metti(R0);
  d.rett.slice(1).forEach((R) => metti(R, R.da));          // sul taglio d'inquadratura la finestra cambia di 1-2 px
  gsap.set(clip, { opacity: 0 });
  tl.to(clip, { opacity: 1, duration: (d.entra_fr || 4) * FR, ease: 'power1.out' }, x.s);
  tl.set(clip, { opacity: 0 }, x.e - EPS);   // esce a taglio: dopo c'e la grafica successiva o il video
  // giro 2 (direttore): il blocco resta centrato nella finestra in ogni stato, sale quando arrivano le righe
  const gruppo = el('div', 'eqa-gruppo', dentro);
  if (d.centra && d.centra.length) {
    gsap.set(gruppo, { y: d.centra[0].dy });
    d.centra.slice(1).forEach((c) => tl.to(gruppo, { y: c.dy, duration: 8 * FR, ease: 'power2.inOut' }, c.t));
  }
  const corpo = d.corpo || 84, n = d.righe.length;
  const sf = (d.sfalsa_fr || 2) * FR, nc = d.cancella_fr || 4;
  d.righe.forEach((r, i) => {
    const riga = el('div', 'eqa-riga', gruppo);
    px(riga, { top: r.y, fontSize: corpo, height: Math.round(corpo * 1.1), lineHeight: Math.round(corpo * 1.1) + 'px' });
    const via = d.t_via + (n - 1 - i) * sf;                 // esce l'ultima riga per prima
    if (r.op) {
      const op = el('span', 'eqa-op', riga, esc(r.op));
      gsap.set(op, { opacity: 0, scale: 0.5 });
      tl.to(op, { opacity: 1, scale: 1, duration: 4 * FR, ease: 'back.out(2)' }, r.t_op !== undefined ? r.t_op : r.t - FR);
      tl.to(op, { opacity: 0, duration: 2 * FR }, via);
    }
    if (r.testo) {
      const t = el('span', 'eqa-t' + (r.chiave ? ' eqa-k' : ''), riga);
      const v = eqDecifra(t, r.testo, r.t, 12, 200 + i);
      cancella(t, v, r.testo, via, nc);
      // giro 2: un colpo di luce sul risultato (scala 1,00 -> 1,05 -> 1,00 e bagliore che sale)
      if (r.luce !== undefined) {
        tl.fromTo(riga, { scale: 1 }, { scale: 1.05, duration: 3 * FR, ease: 'power2.out', immediateRender: false }, r.luce);
        tl.to(riga, { scale: 1, duration: 6 * FR, ease: 'back.out(1.4)' }, r.luce + 3 * FR);
        tl.fromTo(t, { filter: 'brightness(1)' }, { filter: 'brightness(1.45)', duration: 3 * FR, ease: 'power2.out', immediateRender: false }, r.luce);
        tl.to(t, { filter: 'brightness(1)', duration: 9 * FR, ease: 'power2.out' }, r.luce + 3 * FR);
      }
    }
  });
  // giro 2: barra luminosa sotto il risultato che cresce a scatti con la punta chiara (gadzhi-13), esce con il testo
  if (d.barra) {
    const b = el('div', 'eqa-barra', gruppo);
    px(b, { left: (QW - d.barra.larghezza) / 2, top: d.barra.y, width: d.barra.larghezza });
    el('div', 'eqa-testa', b);
    gsap.set(b, { scaleX: 0, transformOrigin: '0% 50%' });
    [0.3, 0.55, 0.8, 1.0].forEach((v, k) => tl.to(b, { scaleX: v, duration: 3 * FR, ease: 'power2.out' }, d.barra.t + k * 5 * FR));
    tl.to(b, { scaleX: 0, duration: 4 * FR, ease: 'power2.in' }, d.t_via - FR);
  }
};

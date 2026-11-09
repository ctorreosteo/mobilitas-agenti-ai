// Equazione detta per gli ads 9:16, nella finestra: variante 2 (laboratorio, fase 5, 04/11/2026). Copia di
// equazione_ads (che resta com'e, approvata e consegnata) con una sola correzione, dal direttore della fase 4: la
// finestra entrava sfumando in 4 fotogrammi e il primo termine decifrato compariva sopra il B-roll (f377-380 di
// AD_CERVICALGIA). Qui il fondo pieno entra a taglio al primo fotogramma e nessun termine parte prima del fotogramma
// dopo (d.attesa_fr, 1). Giro 3: uscita a parole intere, con t_via calcolato (quello del piano si ignora).
// Il resto e identico. Va caricato con usa: ["equazione_ads"] (classi eqa-* e eqDecifra).
// stati dell'uscita a parole: i tagli di cancella() riportati all'ultima parola intera, senza doppioni e senza il vuoto
function statiParole(testo, nf) {
  const out = [];
  for (let k = 0; k < nf; k++) {
    let s = testo.slice(0, Math.floor(testo.length * (nf - k - 1) / nf));
    if (s.length < testo.length && testo[s.length] !== ' ') s = s.slice(0, Math.max(0, s.lastIndexOf(' ')));
    s = s.trim();
    if (s && s !== testo && out[out.length - 1] !== s) out.push(s);
  }
  return out;
}
function cancellaParole(cont, vero, testo, t1, nf) {
  const st = statiParole(testo, nf);
  tl.set(vero, { opacity: 0 }, t1);
  st.forEach((s, k) => {
    const sp = el('span', 'dc-strato', cont, esc(s));
    gsap.set(sp, { opacity: 0 });
    tl.set(sp, { opacity: 1 }, t1 + k * FR);
    tl.set(sp, { opacity: 0 }, t1 + (k + 1) * FR);
  });
}

MODELLI.equazione_ads2 = function (box, x, d) {
  // fase 5: nessun termine prima che il fondo sia pieno (al primo fotogramma dopo l'entrata)
  const TF = x.s + (d.attesa_fr !== undefined ? d.attesa_fr : 1) * FR;
  d = Object.assign({}, d, { righe: d.righe.map((r) => Object.assign({}, r,
    r.t !== undefined ? { t: Math.max(r.t, TF) } : {}, r.t_op !== undefined ? { t_op: Math.max(r.t_op, TF) } : {})) });
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
  tl.set(clip, { opacity: 1 }, x.s);          // fase 5: entra a taglio, con il fondo gia pieno (niente testo sopra il B-roll)
  tl.set(clip, { opacity: 0 }, x.e - EPS);   // esce a taglio: dopo c'e la grafica successiva o il video
  // giro 2 (direttore): il blocco resta centrato nella finestra in ogni stato, sale quando arrivano le righe
  const gruppo = el('div', 'eqa-gruppo', dentro);
  if (d.centra && d.centra.length) {
    gsap.set(gruppo, { y: d.centra[0].dy });
    d.centra.slice(1).forEach((c) => tl.to(gruppo, { y: c.dy, duration: 8 * FR, ease: 'power2.inOut' }, c.t));
  }
  const corpo = d.corpo || 84, n = d.righe.length;
  const sf = (d.sfalsa_fr || 2) * FR, nc = d.cancella_fr || 4;
  // giro 3 (fase 5): l'uscita finiva su una parola a meta («sciog», f534-540 di AD_CERVICALGIA). Ora si cancella a
  // parole intere, e t_via si calcola qui: l'ultimo stato della prima riga (che esce per ultima) cade sull'ultimo
  // fotogramma della grafica, cosi il taglio arriva su parole intere e mai su una finestra vuota
  const r0 = d.righe.find((r) => r.testo);
  const stati0 = r0 ? statiParole(r0.testo, nc).length : 1;
  const i0 = d.righe.indexOf(r0);
  const ultimo = Math.round(x.e / FR - 1) * FR;
  d = Object.assign({}, d, { t_via: ultimo - (stati0 - 1) * FR - (n - 1 - i0) * sf });
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
      cancellaParole(t, v, r.testo, via, nc);
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

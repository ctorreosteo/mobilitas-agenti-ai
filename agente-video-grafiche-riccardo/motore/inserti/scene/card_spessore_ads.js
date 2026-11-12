// Card con spessore per gli ads 9:16, a tutto schermo a momenti (laboratorio, fase 3, 04/11/2026). Modello
// nuovo rifatto su card_spessore (che resta com'e): card blu notte con bordo superiore chiaro, ombra di contatto e
// trama, una sotto l'altra, ognuna sulla frase che la nomina. In piu: il titolo (resta visibile con le card), le
// `apparizioni` a taglio come i B-roll (in mezzo torna il video base), il velo blu opaco sulle card gia dette e il
// riepilogo con tutte piene. Niente icone e niente numeri: sono obiettivi, non un elenco ordinato ne garanzie.
// d: apparizioni [{s, e}], titolo {testo, chiave, t, t_chiave, y, corpo, y_centro, t_sale}, x, y, larghezza, altezza,
//    spazio, corpo, carte [{testo ('*verde*|a capo'), t}], velo, t_riepilogo
MODELLI.card_spessore_ads = function (box, x, d) {
  const QW = 1080, EPS = 0.001;
  const vis = el('div', 'csa-vis', box);
  gsap.set(vis, { opacity: 0 });
  (d.apparizioni || []).forEach((a) => { tl.set(vis, { opacity: 1 }, a.s - EPS); tl.set(vis, { opacity: 0 }, a.e - EPS); });
  const fondo = el('div', 'ca-fondo csa-fondo', vis);
  const retW = el('div', 'csa-ret', fondo);
  retino(retW, { w: 1500, h: 2300, passo: 18, seme: 47, verdi: 0.3, curve: [[220, 0.0030, 0.7, 0.34], [180, 0.0036, 2.2, 0.80]], larga: 170 });
  el('div', 'ca-vigna', fondo);
  tl.fromTo(retW, { x: 0, y: 0 }, { x: -70, y: -50, duration: x.e - x.s, ease: 'none' }, x.s);
  // titolo: «il nostro» panna, «obiettivo» verde, sale da dietro la maschera parola per parola; prima al centro,
  // poi sale in alto quando arriva la prima card
  const T = d.titolo;
  const tit = el('div', 'csa-tit', vis); px(tit, { top: T.y, fontSize: T.corpo || 96 });
  // giro 2 (direttore): le prime parole ci sono gia al taglio (niente fotogramma vuoto); la parola chiave entra
  // senza maschera (la maschera tagliava il suo bagliore in un rettangolo); il filetto sta sotto la parola chiave
  const pz = T.testo.split(' '), parole = [];
  let ultima = null;
  pz.forEach((p, i) => {
    const chiave = i === pz.length - 1 && T.chiave;
    const s = el('span', 'csa-parola' + (chiave ? ' csa-k' : ''), tit, esc(p));
    if (chiave) {
      ultima = s;
      gsap.set(s, { opacity: 0, y: 24, filter: 'blur(10px)' });
      tl.to(s, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 9 * FR, ease: 'expo.out' }, T.t_chiave !== undefined ? T.t_chiave : T.t);
    } else if (T.subito) {
      gsap.set(s, { opacity: 1 });
    } else { maschera(s); gsap.set(s, { yPercent: 135 }); rivela(s, T.t + i * 3 * FR, { dur: 9 * FR }); }
    parole.push(s);
    if (i < pz.length - 1) el('span', '', tit, ' ');
  });
  const filo = el('div', 'csa-filo', ultima || tit);
  tl.fromTo(filo, { scaleX: 0 }, { scaleX: 1, duration: 14 * FR, ease: 'expo.out' }, (T.t_chiave || T.t) + 4 * FR);
  if (T.y_centro !== undefined) {
    gsap.set(tit, { y: T.y_centro - T.y });
    tl.to(tit, { y: 0, duration: 10 * FR, ease: 'power3.inOut' }, T.t_sale);
  }
  // le card
  const W = d.larghezza, H = d.altezza, sp = d.spazio || 24, corpo = d.corpo || 84;
  const carte = [], veli = [];
  const LUCE = '0 4px 6px rgba(0,8,22,0.55), 0 30px 64px rgba(0,8,22,0.55), 0 0 0 1px rgba(114,250,147,0.35), 0 0 30px rgba(114,250,147,0.35), 0 18px 60px rgba(114,250,147,0.22)';
  const SPENTA = '0 4px 6px rgba(0,8,22,0.55), 0 30px 64px rgba(0,8,22,0.55), 0 0 0 1px rgba(0,14,36,0.4)';
  (d.carte || []).forEach((c, i) => {
    const k = el('div', 'cs csa-card', vis);
    px(k, { left: d.x, top: d.y + i * (H + sp), width: W, height: H });
    el('div', 'cs-trama', k);
    const t = el('div', 'cs-tx csa-tx', k);
    px(t, { left: 44, right: 36, fontSize: corpo });
    t.innerHTML = esc(c.testo).replace(/\*([^*]+)\*/g, '<b>$1</b>').replace(/\|/g, '<br>');
    const velo = el('div', 'csa-velo', k); gsap.set(velo, { opacity: 0 }); veli.push(velo);
    gsap.set(k, { opacity: 0, y: 26, scale: 0.94, filter: 'blur(10px)', transformOrigin: '50% 0%' });
    if (d.t_gusci !== undefined) {
      // prima della frase la card c'e gia, vuota e spenta (lo schermo non resta vuoto); sulla frase si accende e
      // il testo entra
      const tg = d.t_gusci + i * (d.gusci_passo !== undefined ? d.gusci_passo : 3 * FR);
      // la card spenta e opaca: sopra ha il velo blu (il retino non passa), che si toglie quando si accende
      tl.to(k, { opacity: 1, y: 0, scale: 1, filter: 'blur(0px)', duration: 8 * FR, ease: 'power3.out' }, tg);
      gsap.set(velo, { opacity: d.guscio || 0.6 });
      gsap.set(t, { opacity: 0, y: 18, filter: 'blur(8px)' });
      tl.to(velo, { opacity: 0, duration: 5 * FR, ease: 'power1.out' }, c.t);
      tl.to(t, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 8 * FR, ease: 'power3.out' }, c.t);
      tl.fromTo(k, { scale: 1 }, { scale: 1.015, duration: 4 * FR, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }, c.t);
      // giro 2: accendersi e un cambio di luce della card, non solo del testo
      tl.to(k, { borderTopColor: 'rgba(160,255,185,0.95)', boxShadow: LUCE, duration: 6 * FR, ease: 'power2.out' }, c.t);
    } else {
      tl.to(k, { opacity: 1, duration: 5 * FR, ease: 'power1.out' }, c.t);
      tl.to(k, { y: 0, scale: 1, filter: 'blur(0px)', duration: 8 * FR, ease: 'power3.out' }, c.t);
    }
    carte.push(k);
  });
  // le card gia dette scendono sotto un velo blu opaco quando arriva la nuova (a scena nascosta se serve)
  (d.carte || []).forEach((c, i) => {
    const ts = c.t_stato !== undefined ? c.t_stato : c.t;
    veli.forEach((v, j) => { if (j < i) tl.to(v, { opacity: d.velo || 0.45, duration: 4 * FR, ease: 'power2.out' }, ts); });
    carte.forEach((k, j) => { if (j < i) tl.to(k, { borderTopColor: 'rgba(244,244,244,0.62)', boxShadow: SPENTA, duration: 4 * FR }, ts); });
  });
  if (d.t_riepilogo !== undefined) {
    veli.forEach((v) => tl.to(v, { opacity: 0, duration: 6 * FR }, d.t_riepilogo));
    carte.forEach((k) => tl.to(k, { borderTopColor: 'rgba(160,255,185,0.95)', boxShadow: LUCE, duration: 6 * FR }, d.t_riepilogo));
  }
};

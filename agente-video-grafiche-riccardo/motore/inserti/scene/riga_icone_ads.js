// Riga di icone per gli ads 9:16, a tutto schermo a momenti (laboratorio, AD_REFLUSSO, 04/11/2026). Modello nuovo
// rifatto su riga_icone (che resta com'e): icone lineari verdi (oggetti, mai figure umane, nessuna scritta) che si
// disegnano con il tratto sulla loro frase (gadzhi-14) e si accendono una per volta (gadzhi-09). Cambiano il quadro
// (1080x1920) e l'impaginazione, che riempie la zona sicura: titolo in alto (c'e dal primo fotogramma, l'ultima parola
// verde), tre riquadri grandi in fila (vuoti e spenti dall'apertura, l'icona si disegna nel suo), sotto un pannello
// grande con la frase dell'icona accesa e una punta che indica il riquadro acceso. Le icone gia dette vanno sotto un
// velo blu opaco; la frase precedente lascia il posto alla nuova a taglio. Niente decifrazioni (nessun carattere
// provvisorio). La scena c'e solo nelle `apparizioni` (a taglio, come i B-roll); in mezzo torna il video base.
// d: apparizioni [{s, e}], titolo {testo, chiave, t, y, corpo}, riquadri {y, lato, spazio}, pannello {y, h, x, w},
//    corpo, righe_y [y1, y2] (centri delle due righe), riga_y (centro della riga sola), t_gusci, gusci_passo, guscio,
//    velo, t_riepilogo, voci [{icona, t, t_stato, via, righe [{testo, t, verde}], entra_fr}]
const RIA_ICONE = {
  // letto visto di fianco: testiera, materasso, cuscino, coperta, piedi, luna
  letto: ['M14 30 V88', 'M14 70 H96 V88', 'M14 58 H96 V70', 'M22 46 h16 a6 6 0 0 1 0 12 h-16 a6 6 0 0 1 0 -12 Z',
    'M46 58 c2 -8 8 -12 16 -12 H88 a8 8 0 0 1 8 8 V58', 'M80 14 a12 12 0 1 0 12 18 a9 9 0 0 1 -12 -18 Z'],
  // sveglia: cassa tonda, lancette, campane, piedini
  sveglia: ['M54 28 a32 32 0 1 0 0.01 0', 'M54 42 V60 L66 68', 'M16 34 a16 16 0 0 1 22 -20', 'M92 34 a16 16 0 0 0 -22 -20',
    'M32 86 L24 98', 'M76 86 L84 98'],
  // fetta di pizza: spicchio, crosta, condimento a puntini
  pizza: ['M54 98 L14 24 Q54 2 94 24 Z', 'M20 34 Q54 16 88 34', 'M44 42 h0.01', 'M64 45 h0.01', 'M54 60 h0.01', 'M53 78 h0.01'],
  // AD_EMICRANIA (04/11/2026): calendario (giorni a puntini, niente cifre), valigia, lampadina accesa
  calendario: ['M18 26 H90 V92 H18 Z', 'M18 44 H90', 'M38 14 V34', 'M70 14 V34', 'M36 60 h0.01', 'M54 60 h0.01', 'M72 60 h0.01',
    'M36 78 h0.01', 'M54 78 h0.01'],
  valigia: ['M18 40 H90 V92 H18 Z', 'M42 40 V30 a4 4 0 0 1 4 -4 H62 a4 4 0 0 1 4 4 V40', 'M36 40 V92', 'M72 40 V92'],
  lampadina: ['M54 18 a24 24 0 0 0 -14 43 c3 3 5 7 5 12 H63 c0 -5 2 -9 5 -12 a24 24 0 0 0 -14 -43 Z', 'M45 84 H63', 'M48 94 H60',
    'M12 42 H20', 'M88 42 H96', 'M22 14 L28 20', 'M86 14 L80 20'],
  // AD_BRUXISMO (04/11/2026): luna con le stelle a puntini, alba sull'orizzonte, dente
  luna: ['M66 14 a38 38 0 1 0 28 64 a30 30 0 0 1 -28 -64 Z', 'M26 22 h0.01', 'M18 46 h0.01', 'M40 10 h0.01'],
  alba: ['M8 80 H100', 'M24 80 a30 30 0 0 1 60 0', 'M54 26 V38', 'M22 44 L30 52', 'M86 44 L78 52', 'M8 62 H18', 'M90 62 H100'],
  dente: ['M34 16 c-14 0 -22 10 -20 26 c2 16 8 26 10 44 c1 9 4 14 9 14 c6 0 7 -9 9 -20 c2 -9 5 -13 12 -13 c7 0 10 4 12 13 c2 11 3 20 9 20 c5 0 8 -5 9 -14 c2 -18 8 -28 10 -44 c2 -16 -6 -26 -20 -26 c-8 0 -12 4 -20 4 c-8 0 -12 -4 -20 -4 Z'],
};

MODELLI.riga_icone_ads = function (box, x, d) {
  const QW = 1080, EPS = 0.001;
  const TG = d.t_gusci !== undefined ? d.t_gusci : 0.3, PG = d.gusci_passo !== undefined ? d.gusci_passo : 0.2;
  const vis = el('div', 'ria-vis', box);
  gsap.set(vis, { opacity: 0 });
  (d.apparizioni || []).forEach((a) => { tl.set(vis, { opacity: 1 }, a.s - EPS); tl.set(vis, { opacity: 0 }, a.e - EPS); });
  // fondo blu notte con il retino che scorre piano (attenuato sotto la zona sicura) e la vignettatura
  const fondo = el('div', 'ria-fondo fondo-sito', vis);
  const retW = el('div', 'ria-ret', fondo);
  retino(retW, { w: 1500, h: 2300, passo: 18, seme: 63, verdi: 0.3, curve: [[220, 0.0030, 1.1, 0.30], [180, 0.0036, 2.9, 0.78]], larga: 170 });
  el('div', 'ria-vigna', fondo);
  tl.fromTo(retW, { x: 0, y: 0 }, { x: -70, y: -50, duration: x.e - x.s, ease: 'none' }, x.s);

  // titolo: c'e intero dal primo fotogramma; l'ultima parola verde, con il filetto che cresce sotto
  const T = d.titolo;
  const tit = el('div', 'ria-tit', vis);
  px(tit, { top: T.y, fontSize: T.corpo || 96 });
  const pz = T.testo.split(' ');
  let ultima = null;
  pz.forEach((p, i) => {
    const k = i === pz.length - 1 && T.chiave;
    const s = el('span', 'ria-parola' + (k ? ' ria-k' : ''), tit, esc(p));
    if (k) ultima = s;
    if (i < pz.length - 1) el('span', '', tit, ' ');
  });
  gsap.set(tit, { opacity: 0 });
  tl.set(tit, { opacity: 1 }, T.t);
  if (ultima) {
    const filo = el('div', 'ria-filo', ultima);
    gsap.set(filo, { scaleX: 0 });
    tl.to(filo, { scaleX: 1, duration: 14 * FR, ease: 'expo.out' }, T.t + 3 * FR);
  }

  // i riquadri delle icone, in fila
  const R = d.riquadri || {};
  const lato = R.lato || 290, spR = R.spazio || 22, yR = R.y || 456;
  const voci = d.voci || [];
  const n = voci.length;
  const x0 = Math.round((QW - (n * lato + (n - 1) * spR)) / 2);
  const centri = [];
  const riq = [], veli = [];
  const ACCESO = '0 0 0 3px rgba(141,255,169,0.95), 0 0 30px rgba(114,250,147,0.6), 0 0 90px rgba(114,250,147,0.28), 0 30px 60px rgba(0,8,22,0.55)';
  const SPENTO = '0 0 0 2px rgba(141,255,169,0.22), 0 30px 60px rgba(0,8,22,0.55)';
  voci.forEach((v, i) => {
    const xr = x0 + i * (lato + spR);
    centri.push(xr + lato / 2);
    const k = el('div', 'ria-riq', vis);
    px(k, { left: xr, top: yR, width: lato, height: lato });
    el('div', 'ria-trama', k);
    const s = svg('svg', { viewBox: '0 0 108 108', class: 'ria-ico' }, k);
    const ic = Math.round(lato * 0.7);
    px(s, { left: (lato - ic) / 2, top: (lato - ic) / 2, width: ic, height: ic });
    (RIA_ICONE[v.icona] || []).forEach((dd, j) => {
      const p = svg('path', { d: dd, fill: 'none', stroke: '#8DFFA9', 'stroke-width': /h0\.01$/.test(dd) ? 9 : 5,
        'stroke-linecap': 'round', 'stroke-linejoin': 'round', pathLength: 1 }, s);
      p.setAttribute('stroke-dasharray', '1 1');
      gsap.set(p, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(p, { attr: { 'stroke-dashoffset': 0 }, duration: 12 * FR, ease: 'power2.out' }, v.t - 2 * FR + j * FR);
    });
    // prima del tratto l'icona non c'e (i puntini a lunghezza zero si vedrebbero nei riquadri vuoti)
    // direttore (AD_REFLUSSO, giro 1): con d.icone_subito le icone ci sono gia intere, sotto il velo, dal loro guscio
    // (niente riquadri vuoti, niente tratti a meta che sembrano caratteri); sulla frase si accendono
    if (d.icone_subito) {
      s.querySelectorAll('path').forEach((pp) => { tl.killTweensOf(pp); gsap.set(pp, { attr: { 'stroke-dashoffset': 0 } }); });
      gsap.set(s, { opacity: 1 });
    } else {
      gsap.set(s, { opacity: 0 });
      tl.set(s, { opacity: 1 }, v.t - 2 * FR);
    }
    const velo = el('div', 'ria-velo', k);
    gsap.set(velo, { opacity: d.guscio || 0.55 });
    veli.push(velo);
    const tg = TG + i * PG;
    if (d.icone_subito) gsap.set(k, { opacity: 1, y: 0, scale: 1, boxShadow: SPENTO });   // gia al loro posto al taglio
    else {
      gsap.set(k, { opacity: 0, y: 30, scale: 0.94, boxShadow: SPENTO });
      tl.to(k, { opacity: 1, y: 0, scale: 1, duration: 9 * FR, ease: 'power3.out' }, tg);
    }
    // sulla frase il riquadro si accende: il velo si toglie, il bordo prende luce, colpo di scala dell'1,5%
    const ta = v.t_stato !== undefined ? v.t_stato : v.t - 2 * FR;
    tl.to(velo, { opacity: 0, duration: 3 * FR, ease: 'power1.out' }, ta);
    tl.to(k, { boxShadow: ACCESO, borderColor: 'rgba(214,255,224,0.95)', duration: 4 * FR, ease: 'power2.out' }, ta);
    // direttore (AD_BRUXISMO): con d.acceso_pieno la tessera accesa si riempie di verde e l'icona diventa blu notte
    // (reference gadzhi-09); quando si accende la successiva torna blu sotto il velo
    if (d.acceso_pieno) {
      const fine = i + 1 < (d.voci || []).length ? ((d.voci[i + 1].t_stato !== undefined ? d.voci[i + 1].t_stato : d.voci[i + 1].t - 2 * FR)) : null;
      const pieno = document.createElement('div');
      pieno.className = 'ria-pieno';
      k.insertBefore(pieno, s);
      gsap.set(pieno, { opacity: 0 });
      tl.to(pieno, { opacity: 1, duration: 3 * FR, ease: 'power2.out' }, ta);
      tl.to(s.querySelectorAll('path'), { attr: { stroke: '#001A3D' }, duration: 3 * FR }, ta);
      if (fine !== null) {
        tl.to(pieno, { opacity: 0, duration: 3 * FR }, fine);
        tl.to(s.querySelectorAll('path'), { attr: { stroke: '#8DFFA9' }, duration: 3 * FR }, fine);
      }
    }
    tl.fromTo(k, { scale: 1 }, { scale: 1.015, duration: 3 * FR, ease: 'power2.out', immediateRender: false }, ta + FR);
    tl.to(k, { scale: 1, duration: 6 * FR, ease: 'back.out(1.4)' }, ta + 4 * FR);
    riq.push(k);
  });
  // le icone gia dette scendono sotto il velo quando si accende la nuova
  voci.forEach((v, i) => {
    const ta = v.t_stato !== undefined ? v.t_stato : v.t - 2 * FR;
    for (let j = 0; j < i; j++) {
      tl.to(veli[j], { opacity: d.velo || 0.5, duration: 4 * FR, ease: 'power2.out' }, ta);
      tl.to(riq[j], { boxShadow: SPENTO, borderColor: 'rgba(244,244,244,0.25)', duration: 4 * FR }, ta);
    }
  });
  if (d.t_riepilogo !== undefined) {
    veli.forEach((v) => tl.to(v, { opacity: 0, duration: 6 * FR }, d.t_riepilogo));
    riq.forEach((k) => tl.to(k, { boxShadow: ACCESO, borderColor: 'rgba(214,255,224,0.95)', duration: 6 * FR }, d.t_riepilogo));
  }

  // il pannello della frase, con la punta sotto il riquadro acceso
  const P = d.pannello || {};
  const pw = P.w || (n * lato + (n - 1) * spR), pxx = P.x !== undefined ? P.x : x0, py = P.y || 800, ph = P.h || 430;
  const pan = el('div', 'ria-pan', vis);
  px(pan, { left: pxx, top: py, width: pw, height: ph });
  el('div', 'ria-trama', pan);
  // AD_EMICRANIA: con pannello.sopra il pannello sta sopra i riquadri e la punta indica in giu
  const punta = el('div', 'ria-punta' + (P.sopra ? ' ria-punta-giu' : ''), vis);
  px(punta, { left: 0, top: P.sopra ? py + ph - 2 : py - 22 });
  gsap.set(pan, { opacity: 0, y: 30, scale: 0.97 });
  // direttore (AD_REFLUSSO, giro 1): con d.pannello_su_voce il pannello entra sulla prima frase, non vuoto prima
  const tp = d.pannello_su_voce && voci.length ? (voci[0].t_stato !== undefined ? voci[0].t_stato : voci[0].t - 2 * FR) : TG + n * PG;
  tl.to(pan, { opacity: 1, y: 0, scale: 1, duration: 10 * FR, ease: 'power3.out' }, tp);
  gsap.set(punta, { opacity: 0, x: centri[0] - 26 });
  voci.forEach((v, i) => {
    const ta = v.t_stato !== undefined ? v.t_stato : v.t - 2 * FR;
    if (i === 0) {
      tl.set(punta, { x: centri[0] - 26 }, ta);
      tl.to(punta, { opacity: 1, duration: 3 * FR }, ta);
    } else tl.to(punta, { x: centri[i] - 26, duration: 8 * FR, ease: 'power3.inOut' }, ta);
    tl.to(pan, { boxShadow: '0 0 0 2px rgba(141,255,169,0.55), 0 0 40px rgba(114,250,147,0.22), 0 30px 70px rgba(0,8,22,0.55)',
      duration: 4 * FR }, ta);
  });

  // le frasi: una riga sola al centro del pannello, due righe ai loro posti; la prima riga verde
  const corpo = d.corpo || 100;
  const ry = d.righe_y || [py + Math.round(ph / 2) - 65, py + Math.round(ph / 2) + 65];
  const r1 = d.riga_y || py + Math.round(ph / 2);
  voci.forEach((v) => {
    const righe = v.righe || [];
    righe.forEach((r, j) => {
      const cy = righe.length === 1 ? r1 : ry[j];
      const verde = r.verde !== undefined ? r.verde : j === 0;
      const w = el('div', 'ria-frase' + (verde ? ' ria-k' : ''), vis, esc(r.testo));
      px(w, { top: cy - Math.round(corpo * 0.6), fontSize: corpo, height: Math.round(corpo * 1.2), lineHeight: Math.round(corpo * 1.2) + 'px' });
      const nf = v.entra_fr || 8;
      // la frase c'e gia intera sul suo fotogramma (niente pannello vuoto al cambio): entra a taglio e si assesta
      gsap.set(w, { opacity: 0, y: 20, filter: 'blur(4px)' });
      tl.set(w, { opacity: 1 }, r.t - EPS);
      tl.to(w, { y: 0, filter: 'blur(0px)', duration: nf * FR, ease: 'expo.out' }, r.t - EPS);
      if (v.via !== undefined) tl.set(w, { opacity: 0 }, v.via - EPS);
    });
  });
};

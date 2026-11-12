// Chiusura per gli ads 9:16: variante 2 (laboratorio, fase 5, 04/11/2026). Copia di chiusura_ads (che resta
// com'e, approvata e consegnata) con una sola correzione, dal direttore della fase 4: «ci vediamo» saliva da una
// maschera e per un fotogramma si vedevano solo l'asta della «d» e il punto della «i» (segni staccati sopra «compila»,
// f2028 di AD_CERVICALGIA). Qui entra intero con opacita, salita e sfocatura, come la parola chiave dell'obiettivo.
// Giro 3 (fase 5, ok di Riccardo per un ultimo giro): lo stesso per le righe della lista e per «a soli», che salivano
// da una maschera e per qualche fotogramma erano tagliate a meta («gli ultimi», f1848).
// Va caricato con usa: ["card_accese", "chiusura_ads"] (classi cha-* e ca-*).
MODELLI.chiusura_ads2 = function (box, x, d) {
  const QW = 1080, QH = 1920;
  const fondo = el('div', 'cha-fondo ca-fondo', box);
  const retW = el('div', 'cha-ret', fondo);
  retino(retW, { w: 1500, h: 2300, passo: 18, seme: 33, verdi: 0.3, curve: [[220, 0.0030, 1.1, 0.32], [180, 0.0036, 2.9, 0.78]], larga: 170 });
  el('div', 'ca-vigna', fondo);
  tl.fromTo(retW, { x: 0, y: 0 }, { x: -60, y: -50, duration: x.e - x.s, ease: 'none' }, x.s);
  const centro = (cls, parent) => { const e = el('div', 'cha-riga ' + (cls || ''), parent || box); return e; };
  const via = (els, t) => els.forEach((e, k) => tl.to(e, { opacity: 0, y: -40, filter: 'blur(6px)', duration: ESCE, ease: 'power2.in' }, t + k * 0.5 * FR));
  // 1. lista: «stiamo riservando» + righe spente che si accendono sulla loro parola
  const L = d.lista, l1 = [];
  let y = L.y;
  const tit = centro('cha-tit'); px(tit, { top: y, fontSize: L.titolo.corpo || 84 });
  const ts = el('span', '', tit, esc(L.titolo.testo));
  if (L.titolo.subito) gsap.set(ts, { opacity: 1 });   // c'e gia al taglio (niente fotogramma vuoto)
  else { maschera(ts); gsap.set(ts, { yPercent: 135 }); rivela(ts, L.titolo.t, { dur: 10 * FR }); }
  l1.push(tit);
  y += Math.round((L.titolo.corpo || 84) * 1.1) + 30;
  const filo = el('div', 'cha-filo', box); px(filo, { top: y });
  tl.fromTo(filo, { scaleX: 0 }, { scaleX: 1, duration: 14 * FR, ease: 'expo.out' }, L.titolo.t + 4 * FR); l1.push(filo);
  y += 8 + 40;
  L.righe.forEach((r, i) => {
    const c = r.corpo || 88;
    const rg = centro('cha-lista' + (r.chiave ? ' cha-k' : '')); px(rg, { top: y, fontSize: c });
    // fase 5, giro 3: la riga entra intera, senza maschera (dalla maschera «gli ultimi» si vedeva tagliato a meta,
    // f1848 di AD_CERVICALGIA)
    const sp = el('span', '', rg, esc(r.testo));
    gsap.set(sp, { display: 'inline-block', opacity: 0, y: 26, filter: 'blur(10px)' });
    tl.to(sp, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 9 * FR, ease: 'expo.out' }, L.titolo.t + (6 + 3 * i) * FR);   // la riga c'e gia, spenta
    gsap.set(rg, { opacity: 0.32 });
    tl.to(rg, { opacity: 1, duration: 6 * FR, ease: 'power2.out' }, r.t);
    tl.fromTo(rg, { scale: 1 }, { scale: 1.03, duration: 4 * FR, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }, r.t);
    l1.push(rg);
    y += Math.round(c * 1.1) + (r.dopo || 20);
  });
  via(l1, L.via);
  // 2. prezzo detto: «a soli» e «€49» (compare gia giusto, con un colpo di scala)
  const P = d.prezzo;
  const pre = centro('cha-pre'); px(pre, { top: P.y, fontSize: P.pre.corpo || 96 });
  // fase 5, giro 3: anche «a soli» entra intero, senza maschera
  const ps = el('span', '', pre, esc(P.pre.testo));
  gsap.set(ps, { display: 'inline-block', opacity: 0, y: 26, filter: 'blur(10px)' });
  tl.to(ps, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 9 * FR, ease: 'expo.out' }, P.pre.t);
  const cif = centro('cha-prezzo'); px(cif, { top: P.y + Math.round((P.pre.corpo || 96) * 1.1) + 10, fontSize: P.cifra.corpo || 280 });
  const cs = el('span', '', cif, esc(P.cifra.testo));
  gsap.set(cif, { opacity: 0, scale: 0.6, filter: 'blur(14px)' });
  tl.to(cif, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 9 * FR, ease: 'back.out(1.6)' }, P.cifra.t);
  tl.to(pre, { opacity: 0, y: -30, duration: ESCE, ease: 'power2.in' }, P.su.t);
  // il prezzo sale e si rimpicciolisce sopra il modulo, poi esce con lui
  tl.to(cif, { y: P.su.dy, scale: P.su.scala, duration: 10 * FR, ease: 'power3.inOut' }, P.su.t);
  // 3. modulo stilizzato: pannello con campi vuoti che si evidenziano, il pulsante «compila»
  const M = d.modulo;
  const pan = el('div', 'cha-pannello', box); px(pan, { left: M.x, top: M.y, width: M.w, height: M.h });
  gsap.set(pan, { opacity: 0, y: 60 });
  tl.to(pan, { opacity: 1, y: 0, duration: 9 * FR, ease: 'expo.out' }, M.t);
  const campi = M.campi.map((t, i) => {
    const b = el('div', 'cha-campo', pan); px(b, { top: M.campo_y0 + i * M.campo_passo, height: M.campo_h });
    const cur = el('div', 'cha-cursore', b); gsap.set(cur, { opacity: 0 });
    gsap.set(b, { opacity: 0, x: -30 });
    tl.to(b, { opacity: 1, x: 0, duration: 7 * FR, ease: 'power3.out' }, M.t + i * FR);   // giro 2: entrano con il pannello
    tl.to(b, { borderColor: 'rgba(114,250,147,0.95)', boxShadow: '0 0 18px rgba(114,250,147,0.45)', duration: 3 * FR }, t);
    const fine = i + 1 < M.campi.length ? M.campi[i + 1] : M.via;
    for (let k = 0; t + k * 0.25 < fine; k++) tl.set(cur, { opacity: k % 2 === 0 ? 1 : 0 }, t + k * 0.25);
    tl.set(cur, { opacity: 0 }, fine);
    if (i + 1 < M.campi.length) tl.to(b, { borderColor: 'rgba(244,244,244,0.25)', boxShadow: '0 0 0 rgba(0,0,0,0)', duration: 3 * FR }, fine);
    return b;
  });
  // giro 2 (direttore): il pulsante e un pezzo a se, sopra il pannello; quando il modulo esce resta e scende sotto il
  // marchio, e la freccia nasce da lui: la chiamata all'azione e un gesto solo, dal modulo al pulsante dell'ad
  const bot = el('div', 'cha-bottone', box);
  px(bot, { left: M.x + 50, width: M.w - 100, top: M.y + M.bottone.y, height: M.bottone.h, fontSize: M.bottone.corpo || 72, lineHeight: M.bottone.h + 'px' });
  el('span', '', bot, esc(M.bottone.testo));
  gsap.set(bot, { opacity: 0, scale: 0.9 });
  tl.to(bot, { opacity: 1, scale: 1, duration: 6 * FR, ease: 'back.out(1.6)' }, M.t);
  tl.fromTo(bot, { scale: 1 }, { scale: 1.06, duration: 4 * FR, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }, M.bottone.t);
  tl.to([pan, cif], { opacity: 0, y: '-=40', filter: 'blur(6px)', duration: ESCE, ease: 'power2.in' }, M.via);
  tl.to(bot, { y: d.marchio.bottone_y - (M.y + M.bottone.y), duration: 10 * FR, ease: 'power3.inOut' }, M.via);
  // 4. marchio: «ci vediamo», il logo (in Mobilitas) e la freccia verso il pulsante dell'ad
  const K = d.marchio;
  if (K.disco_y !== undefined) {
    const disco = el('div', 'pittogramma cha-disco', box); px(disco, { left: (QW - K.disco) / 2, top: K.disco_y, width: K.disco, height: K.disco });
    const pi = el('img', '', disco); pi.src = 'assets/pittogramma-sfondo-trasparente.png';
    gsap.set(disco, { opacity: 0, scale: 0.7, filter: 'blur(8px)' });
    tl.to(disco, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 12 * FR, ease: 'back.out(1.4)' }, K.testo.t + 2 * FR);
  }
  const cv = centro('cha-ci'); px(cv, { top: K.y, fontSize: K.testo.corpo || 110 });
  // fase 5: «ci vediamo» entra intero, senza maschera (dalla maschera spuntavano prima solo l'asta della «d» e il
  // punto della «i», segni staccati sopra «compila» a f2028 di AD_CERVICALGIA)
  const cvs = el('span', '', cv, esc(K.testo.testo));
  gsap.set(cvs, { display: 'inline-block', opacity: 0, y: 26, filter: 'blur(10px)' });
  tl.to(cvs, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 9 * FR, ease: 'expo.out' }, K.testo.t);
  const logo = el('img', 'cha-logo', box); logo.src = 'assets/logo_verde.png';
  px(logo, { left: (QW - K.logo_w) / 2, top: K.logo_y, width: K.logo_w });
  gsap.set(logo, { opacity: 0, y: 30, filter: 'blur(10px)' });
  tl.to(logo, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 10 * FR, ease: 'expo.out' }, K.logo_t);
  const fw = el('div', 'cha-freccia', box); px(fw, { left: (QW - (K.freccia_w || 110)) / 2, top: K.freccia_y, width: K.freccia_w || 110 });
  frecciaGiu(fw, '#72FA93', K.freccia_tratto || 10);
  gsap.set(fw, { opacity: 0, y: -60 });
  tl.to(fw, { opacity: 1, y: 0, duration: 10 * FR, ease: 'back.out(1.2)' }, K.freccia_t);
  for (let k = 0; k < 6; k++) {
    const t = K.freccia_t + 10 * FR + 0.1 + k * 0.5;
    if (t + 0.45 > x.e) break;
    tl.to(fw, { y: K.rimbalzo || 34, duration: 0.17, ease: 'power2.in' }, t);
    tl.to(fw, { y: 0, duration: 0.28, ease: 'back.out(1.0)' }, t + 0.17);
  }
};

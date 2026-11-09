// Card accese con carrello di camera per gli ads 9:16 (laboratorio, 04/11/2026; catalogo
// `card-accese-9x16-carrello`, variante di `card-accese-9x16`; reference gadzhi-08, gadzhi-12, gadzhi-15).
// Stesso linguaggio di card_accese_ads (card blu notte con trama, bordo luminoso, «?» con i puntini finche la card
// aspetta la sua parola, accensione verde con riflesso e colpo di scala, velo blu opaco).
// Giro 3 (direttore e Riccardo, 04/11/2026): il carrello si vede. Le tre card dei motivi stanno su un binario in
// prospettiva leggera: la card attiva grande al centro, le vicine ai lati (in parte fuori quadro) ruotate verso il
// centro e sotto il velo blu: quelle gia dette restano accese (verdi, velate), quelle future sono blu. Sotto ogni card
// tre tacche ricordano dove siamo (le dette verdi). Mai card vuote: la card in attesa mostra «?» e i puntini; sulla
// parola «?» -> cifra gia giusta (mai decifrata). Il passaggio fra le card avviene a scena nascosta (al taglio la
// camera e gia sulla card nuova, ferma); dopo l'entrata il binario scorre appena e la camera avanza piano.
// Apparizione 1 (annuncio): «3 motivi» intero dal primo fotogramma e sotto le tre card del binario viste larghe, in
// ventaglio (gadzhi-08), tutte con «?» e i puntini.
// Testo solo sulla card attiva (le vicine sono velate e senza testo: niente testo fuori dalla zona sicura); sotto
// y 1248 solo il corpo e lo spessore delle card. La frase si decifra in 8 fotogrammi a sole lettere (niente «z», che
// somiglia a una cifra; i/l/j e cifre non si rimescolano; nessuno strato e una parola vera).
// d: apparizioni [{s, e}] (la prima e l'annuncio, poi una per card), titolo {testo, t}, carte [{num, t_num, chiave,
//    t_chiave}], corpo, corpo_titolo, corpo_cifra, decifra_fr (8), velo, lucine [t], geo {} (misure, facoltative).
//    I campi di impaginazione dei giri 1-2 (x, y, w, h, passo, r_medaglione, y_medaglione, y_chiave, slot, carrello)
//    si ignorano.
const CCR_PAROLE = new Set(('a e o i da di la le lo li il un una uno del dal dalle dallo dalla sale sola sole soli solo sala ' +
  'sani sano cane cani cena cene casa case cosa cose come con non noi voi suo sua sue tra fra fa fan sa so se si ' +
  'ne no na va vi ce ci te ti me mi mia mio mai mani mano meno mare more amo ama ami ore ora oro era ero ano ' +
  'prima primo prime prora sera seta sete seme sono suono stato stomaco senza retta resta resto sento senta ' +
  'tutto tutti nuovo nuova nave nevi neve vino vena vene vane vano vaso vasi mascella masse massa ' +
  'cura cure duro dura dure muro mura uomo uova sarà sara tema temi rete reti rosa rose rana rane ' +
  'intestino intesa inteso intera intero interno interna testa testo teste tetto tetti costa costo conto ' +
  'sento senno sono suoi nostro nostra noto nota note neo neon nano nana sula sul sulla sullo nulla ' +
  'sec seno sene seco secco seconda secondo cena ceno').split(' '));
function ccrDecifra(cont, testo, t0, nf, seme) {
  const insieme = (c) => /[tfr]/.test(c) ? 'tfr' : /[mw]/.test(c) ? 'mw' : 'acenosuvx';
  const fisso = (c) => c === ' ' || /[0-9iljz]/.test(c) || /[^A-Za-zÀ-ÿ]/.test(c);
  const strati = (sm) => {
    const r = semi(sm), out = [];
    for (let k = 0; k < nf; k++) {
      const fermi = Math.floor(testo.length * (k + 1) / (nf + 1));
      let s = '';
      for (let i = 0; i < testo.length; i++) {
        const c = testo[i];
        s += (i < fermi || fisso(c)) ? c : insieme(c)[Math.floor(r() * insieme(c).length)];
      }
      out.push(s);
    }
    return out;
  };
  const vere = testo.split(/[\s']+/);
  let st = null;
  for (let p = 0; p < 80 && !st; p++) {
    const prova = strati(seme + p * 101);
    if (prova.every((s) => s.split(/[\s']+/).every((w, j) => w === vere[j] || !CCR_PAROLE.has(w.toLowerCase())))) st = prova;
  }
  st = st || strati(seme);
  const vero = el('span', 'dc-vero', cont, esc(testo));
  gsap.set(vero, { opacity: 0 });
  st.forEach((s, k) => {
    const sp = el('span', 'dc-strato', cont, esc(s));
    gsap.set(sp, { opacity: 0 });
    tl.set(sp, { opacity: 1 }, t0 + k * FR);
    tl.set(sp, { opacity: 0 }, t0 + (k + 1) * FR);
  });
  tl.set(vero, { opacity: 1 }, t0 + nf * FR);
  return vero;
}

MODELLI.card_carrello_ads = function (box, x, d) {
  const EPS = 0.001;
  const G = Object.assign({
    w: 760, h: 1340, y: 268,              // card attiva (x centrata): testo fino a y ~1150, corpo fino a 1558
    yM: 330, rM: 225, yK: 625, yT: 1062,  // medaglione (centro, raggio), frase, tacche: dentro la card
    dx: 520, sv: 0.84, rot: 14,           // vicine: distanza dal centro, scala, rotazione verso il centro
    deriva: 22,                           // scorrimento del binario dopo l'entrata (px)
    // annuncio
    yTit: 300, fy: 540, fw: 292, fh: 1000, fgap: 42, frot: 16, frM: 104, fyM: 250, fyK: 470,
  }, d.geo || {});
  const corpo = d.corpo || 112, corpoT = d.corpo_titolo || 160, corpoC = d.corpo_cifra || 420;
  const NF = Math.max(4, Math.min(8, d.decifra_fr || 8));
  const lh = Math.round(corpo * 1.16);
  const AP = d.apparizioni || [];
  const N = (d.carte || []).length;
  const vis = el('div', 'caa-vis', box);
  // entra ed esce a taglio; acceso 10 ms prima del taglio (gli scatti di HyperFrames non vedevano un set 1 ms prima),
  // dallo stato iniziale se l'apparizione parte da 0
  gsap.set(vis, { opacity: AP[0] && AP[0].s <= FR / 2 ? 1 : 0 });
  AP.forEach((a) => {
    if (a.s > FR / 2) tl.set(vis, { opacity: 1 }, a.s - 0.01);
    tl.set(vis, { opacity: 0 }, a.e - EPS);
  });
  const fondo = el('div', 'ca-fondo caa-fondo', vis);
  const par = el('div', 'ccr-par', fondo);
  const retW = el('div', 'ccr-ret', par);
  retino(retW, { w: 2000, h: 2300, passo: 18, seme: 33, verdi: 0.3,
    curve: [[220, 0.0030, 0.9, 0.30], [180, 0.0034, 2.6, 0.80]], larga: 170 });
  el('div', 'ca-vigna', fondo);
  tl.fromTo(retW, { x: 0, y: 0 }, { x: -60, y: -70, duration: x.e - x.s, ease: 'none' }, x.s);
  const cam = el('div', 'ccr-cam', vis);
  const ALONE = '0 0 0 2px rgba(214,255,224,0.9), 0 0 18px rgba(114,250,147,0.75), 0 0 40px rgba(114,250,147,0.45), 0 0 90px rgba(114,250,147,0.18), 0 40px 90px rgba(0,8,22,0.6)';
  const ACCESO = '0 0 0 2px rgba(141,255,169,0.95), 0 0 34px rgba(114,250,147,0.65), 0 0 110px rgba(114,250,147,0.32), 0 40px 90px rgba(0,8,22,0.6)';
  const SPENTO = '0 0 0 2px rgba(141,255,169,0.28), 0 4px 8px rgba(0,8,22,0.6), 0 40px 90px rgba(0,8,22,0.6)';
  const punti = (parent, n, cls) => { const r = el('div', cls, parent); for (let i = 0; i < n; i++) el('i', '', r); return r; };
  const lucina = (rifl, t, forte) => {
    tl.set(rifl, { opacity: forte || 0.22 }, t);
    tl.fromTo(rifl, { xPercent: 0 }, { xPercent: 420, duration: forte ? 6 * FR : 0.7, ease: forte ? 'power2.inOut' : 'sine.inOut', immediateRender: false }, t);
    tl.set(rifl, { opacity: 0 }, t + (forte ? 6 * FR : 0.7));
  };
  const pulsa = (e, t0, t1, amp) => {
    let tp = t0;
    while (tp + 0.5 <= t1) {
      tl.to(e, { scale: amp || 1.08, duration: 0.25, ease: 'sine.inOut' }, tp);
      tl.to(e, { scale: 1, duration: 0.25, ease: 'sine.inOut' }, tp + 0.25);
      tp += 0.5;
    }
  };
  // un pezzo = spessore + card; dentro la card: trama, luce verde, riflesso, forme, testi, velo
  const pezzo = (parent, w, h) => {
    const p = el('div', 'ccr-pezzo', parent);
    px(p, { width: w, height: h });
    gsap.set(p, { transformPerspective: 1700 });
    const sp = el('div', 'ccr-spessore', p);
    px(sp, { top: h - 40, height: 70 });
    const k = el('div', 'ca-card ccr-card', p);
    px(k, { left: 0, top: 0, width: w, height: h });
    gsap.set(k, { color: '#F4F4F4', boxShadow: SPENTO, transformOrigin: '50% 40%' });
    el('div', 'ca-trama', k);
    const luce = el('div', 'ca-luce', k);
    el('div', 'ca-onda', luce); el('div', 'ca-onda2', luce); el('div', 'ca-onda3', luce);
    gsap.set(luce, { opacity: 0 });
    const rifl = el('div', 'ca-riflesso', k);
    gsap.set(rifl, { opacity: 0 });
    const forme = el('div', 'ccr-forme', k);
    const testi = el('div', 'ccr-testi', k);
    const velo = el('div', 'caa-velo', k);
    gsap.set(velo, { opacity: 0 });
    return { p, k, luce, rifl, forme, testi, velo };
  };
  const medaglione = (C, w, yM, rM) => {
    const an = el('div', 'ccr-anello', C.forme);
    px(an, { left: w / 2 - rM, top: yM - rM, width: 2 * rM, height: 2 * rM });
    const alo = el('div', 'ccr-alone', an);
    const onda = el('div', 'ccr-onda', C.forme);
    px(onda, { left: w / 2 - rM, top: yM - rM, width: 2 * rM, height: 2 * rM });
    gsap.set(onda, { opacity: 0, transformOrigin: '50% 50%' });
    return { an, alo, onda };
  };
  const segno = (C, w, yM, cs, testo, cls) => {
    const s = el('div', 'ccr-cifra ' + (cls || ''), C.testi, esc(testo));
    px(s, { top: yM - cs * 0.5, width: w, fontSize: cs, height: cs });
    gsap.set(s, { transformOrigin: '50% 50%' });
    return s;
  };
  // ================= apparizione 1: titolo e le tre card in ventaglio
  const fan = el('div', 'ccr-fan', cam);
  const T = d.titolo || { testo: '', t: 0 };
  const tt = el('div', 'caa-titolo ccr-tit', fan);
  px(tt, { top: G.yTit, fontSize: corpoT });
  const m = /^(\d+)\s+(.*)$/.exec(T.testo);
  // titolo intero e fermo dal primo fotogramma del taglio (la cifra e detta, gia giusta)
  if (m) { el('span', 'caa-tcifra', tt, esc(m[1])); el('span', 'caa-tsp', tt, ' '); }
  el('span', 'caa-ttesto', tt, esc(m ? m[2] : T.testo));
  const fx0 = (1080 - (N * G.fw + (N - 1) * G.fgap)) / 2;
  const ventaglio = [];
  for (let j = 0; j < N; j++) {
    const C = pezzo(fan, G.fw, G.fh);
    px(C.p, { left: fx0 + j * (G.fw + G.fgap), top: G.fy });
    gsap.set(C.p, { rotationY: G.frot * (1 - j) * (N === 3 ? 1 : 0), transformOrigin: '50% 50%' });
    const M = medaglione(C, G.fw, G.fyM, G.frM);
    gsap.set(M.an, { borderColor: 'rgba(141,255,169,0.85)' });
    const q = segno(C, G.fw, G.fyM, Math.round(G.frM * 1.25), '?', 'ccr-q');
    punti(C.forme, 4, 'ccr-punti ccr-punti-f').style.top = G.fyK + 'px';
    punti(C.forme, 3, 'ccr-punti ccr-punti-f').style.top = (G.fyK + 60) + 'px';
    tacche(C, G.fw, G.fh - 150, -1);
    ventaglio.push({ C, M, q });
    if (AP[0]) {
      pulsa(q, AP[0].s + 0.5 + j * 0.18, AP[0].e, 1.12);
      (d.lucine || [1.3, 2.2]).forEach((t0) => lucina(C.rifl, t0 + j * 0.22));
    }
  }
  // tre tacche sotto il contenuto: quelle gia dette verdi, quella attiva lunga e luminosa (forme, niente testo)
  function tacche(C, w, y, att) {
    const r = el('div', 'ccr-tacche', C.forme);
    px(r, { top: y, width: w });
    for (let j = 0; j < N; j++) el('i', j < att ? 'gia' : j === att ? 'ora' : '', r);
    return r;
  }
  // ================= apparizioni 2..: il binario
  const bin = el('div', 'ccr-bin', cam);
  const corsia = el('div', 'ccr-corsia', bin);         // scorre appena dopo l'entrata
  const carte = (d.carte || []).map((c, i) => {
    const C = pezzo(corsia, G.w, G.h);
    px(C.p, { left: (1080 - G.w) / 2, top: G.y });
    gsap.set(C.p, { transformOrigin: '50% 50%' });
    const M = medaglione(C, G.w, G.yM, G.rM);
    const q = segno(C, G.w, G.yM, Math.round(corpoC * 0.86), '?', 'ccr-q');
    const cif = segno(C, G.w, G.yM, corpoC, c.num);
    gsap.set(cif, { opacity: 0 });
    // frase su due righe bilanciate
    const p = c.chiave.split(' ');
    let righe = [c.chiave];
    if (p.length > 1 && !d.una_riga) {
      let best = null;
      for (let k = 1; k < p.length; k++) {
        const a = p.slice(0, k).join(' '), b = p.slice(k).join(' ');
        if (!best || Math.max(a.length, b.length) < best[0]) best = [Math.max(a.length, b.length), a, b];
      }
      righe = [best[1], best[2]];
    }
    const yk = G.yK + (righe.length === 1 ? lh / 2 : 0);
    const pz = el('div', 'ccr-pz', C.forme);
    px(pz, { top: yk, width: G.w });
    righe.forEach((r) => px(punti(pz, Math.max(4, Math.round(r.length * 0.45)), 'ccr-punti ccr-punti-k'), { height: lh }));
    const chi = el('div', 'ccr-chiave', C.testi);
    px(chi, { top: yk, width: G.w, fontSize: corpo });
    tacche(C, G.w, G.yT, i);
    return { C, M, q, cif, pz, chi, righe, c };
  });
  // la disposizione del binario con la card `att` al centro (a scena nascosta: niente movimento visibile)
  const disponi = (att, t) => {
    carte.forEach((K, j) => {
      const o = j - att, ao = Math.abs(o);
      tl.set(K.C.p, { x: o * G.dx, scale: ao ? G.sv : 1, rotationY: -Math.sign(o) * G.rot, zIndex: 10 - ao,
        opacity: ao > 1 ? 0 : 1 }, t);
      tl.set(K.C.velo, { opacity: ao ? (d.velo || 0.55) : 0 }, t);
      tl.set(K.C.testi, { opacity: ao ? 0 : 1 }, t);    // le vicine non hanno testo (velate, in parte fuori quadro)
    });
  };
  gsap.set(fan, { opacity: 1 });
  gsap.set(bin, { opacity: 0 });
  carte.forEach((K, j) => gsap.set(K.C.p, { x: j * G.dx, scale: j ? G.sv : 1, rotationY: -Math.sign(j) * G.rot, zIndex: 10 - j, opacity: j > 1 ? 0 : 1 }));
  gsap.set(cam, { scale: 1, transformOrigin: '50% 45%' });
  AP.forEach((a, k) => {
    const tz = a.s - 2 * FR;
    if (k === 1) { tl.set(fan, { opacity: 0 }, tz); tl.set(bin, { opacity: 1 }, tz); }
    if (k >= 1 && carte[k - 1]) disponi(k - 1, tz);
    // dopo l'entrata: la camera avanza piano e il binario scorre appena (la card e ferma al taglio)
    tl.fromTo(cam, { scale: 1 }, { scale: 1.02, duration: a.e - a.s, ease: 'none', immediateRender: false }, a.s);
    tl.fromTo(par, { x: -k * 70 }, { x: -k * 70 - 20, duration: a.e - a.s, ease: 'none', immediateRender: false }, a.s);
    if (k >= 1) tl.fromTo(corsia, { x: 0 }, { x: -G.deriva, duration: a.e - a.s, ease: 'sine.inOut', immediateRender: false }, a.s);
  });
  // ================= la card attiva: «?» e puntini, poi la cifra, la frase, l'accensione
  carte.forEach((K, i) => {
    const a = AP[i + 1], { C, M, q, cif, pz, chi, righe, c } = K;
    const tn = c.t_num, tk = c.t_chiave;
    gsap.set(M.an, { borderColor: 'rgba(141,255,169,0.9)', boxShadow: '0 0 26px rgba(114,250,147,0.45), inset 0 0 40px rgba(114,250,147,0.22)' });
    gsap.set(M.alo, { opacity: 0.8 });
    if (a) {
      tl.set(C.k, { boxShadow: ACCESO }, a.s - 2 * FR);
      pulsa(q, a.s + 3 * FR, tn - FR, 1.08);
      if (tn - a.s > 8 * FR) lucina(C.rifl, a.s + 2 * FR);
    }
    // sulla parola del numero: «?» -> cifra, netto, con un colpo di scala e un'onda di luce dentro la card
    tl.set(q, { opacity: 0 }, tn);
    tl.set(cif, { opacity: 1 }, tn);
    tl.fromTo(cif, { scale: 1.14 }, { scale: 1, duration: 9 * FR, ease: 'expo.out', immediateRender: false }, tn);
    tl.fromTo(M.an, { scale: 0.95 }, { scale: 1, duration: 10 * FR, ease: 'back.out(1.6)', immediateRender: false }, tn);
    tl.set(M.onda, { opacity: 0.9 }, tn);
    tl.fromTo(M.onda, { scale: 1 }, { scale: 1.2, duration: 9 * FR, ease: 'power2.out', immediateRender: false }, tn);
    tl.to(M.onda, { opacity: 0, duration: 9 * FR, ease: 'power1.in' }, tn);
    tl.to(M.alo, { opacity: 0.35, duration: 4 * FR, ease: 'power2.out' }, tn);
    // la frase si decifra (8 fotogrammi, sole lettere) e finisce sulla parola chiave
    tl.set(pz, { opacity: 0 }, tk - NF * FR);
    righe.forEach((r, j) => {
      const rg = el('div', 'ccr-riga', chi);
      px(rg, { height: lh });
      ccrDecifra(el('span', 'ccr-rv', rg), r, tk - NF * FR, NF, 50 + i * 7 + j);
    });
    // accensione netta, in un fotogramma (niente mezzo tono «petrolio» ne testo panna sul verde): luce verde, testo blu
    // notte, riflesso, colpo di scala 1,5%
    const tf = tk + 3 * FR - FR;
    tl.set(C.luce, { opacity: 1 }, tf + FR);
    tl.set(C.k, { color: '#002552', boxShadow: ALONE }, tf + FR);
    tl.set(cif, { color: '#002552', textShadow: 'none' }, tf + FR);
    tl.set(M.an, { borderColor: 'rgba(0,37,82,0.85)', boxShadow: 'none', backgroundImage: 'none', backgroundColor: 'rgba(0,37,82,0.06)' }, tf + FR);
    tl.set(M.alo, { opacity: 0 }, tf + FR);
    const tc = C.forme.querySelector('.ccr-tacche');
    Array.from(tc.children).forEach((e, j) => tl.set(e, { backgroundColor: j === i ? '#002552' : 'rgba(0,37,82,0.35)', boxShadow: 'none' }, tf + FR));
    lucina(C.rifl, tf + 2 * FR, 1);
    tl.fromTo(C.k, { scale: 1 }, { scale: 1.015, duration: 3 * FR, ease: 'power2.out', immediateRender: false }, tf);
    tl.to(C.k, { scale: 1, duration: 6 * FR, ease: 'back.out(1.4)' }, tf + 3 * FR);
  });
};

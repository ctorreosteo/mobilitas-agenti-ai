// Card che si accendono per gli ads 9:16 (laboratorio, fase 2, 03/11/2026). Modello nuovo,
// rifatto su card_accese (che resta com'e, a 1920x1080): stesse card blu notte con trama, scansione
// d'entrata, testo che si decifra, riempimento di luce verde con riflesso e colpo di scala, contrasto
// di stato (le altre al 42%) e riepilogo. Cambiano il quadro (1080x1920, card una sotto l'altra), i
// numeri (nel riquadro, niente cifre giganti a contorno: il «1» si leggeva come una freccia) e il tempo:
// la scena e visibile solo nelle `apparizioni` (tutto schermo), in mezzo torna il video base.
// d: apparizioni [{s, e, esce: 'sfuma'|'taglio'}], titolo {cifra, testo, t}, t_entra, x, y, w, h, gap,
//    rot, corpo, corpo_titolo, y_titolo, carte [{num, t_num, chiave, t_chiave}], t_riepilogo
// decifra con caratteri della stessa larghezza (fase 2, «lettere intere»): con quella di _scena.js le
// lettere provvisorie («m», «w») allargavano «solo con le mani» oltre il bordo della card
function decifraStretto(cont, testo, t0, nf, seme) {
  const r = semi(seme || testo.length * 31 + 7);
  // giro 3 (Riccardo): a schermo mai numeri non detti, nemmeno per un fotogramma. I caratteri provvisori sono
  // solo lettere minuscole; una cifra del testo vero non si rimescola (compare gia giusta)
  // giro 3b (direttore): niente aste sole provvisorie (una «l» di sfuggita sembra un «1»): «i», «l», «j» non si
  // rimescolano, «t», «f», «r» si scambiano fra loro
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

MODELLI.card_accese_ads = function (box, x, d) {
  const QW = 1080, QH = 1920, EPS = 0.001;
  const vis = el('div', 'caa-vis', box);
  gsap.set(vis, { opacity: 0 });
  (d.apparizioni || []).forEach((a) => {
    tl.set(vis, { opacity: 1 }, a.s - EPS);                     // entra a taglio, come i B-roll del video
    if (a.esce === 'sfuma') tl.to(vis, { opacity: 0, duration: 5 * FR, ease: 'power2.in' }, a.e - 5 * FR - EPS);
    else tl.set(vis, { opacity: 0 }, a.e - EPS);
  });
  const fondo = el('div', 'ca-fondo caa-fondo', vis);
  const retW = el('div', 'caa-ret', fondo);
  retino(retW, { w: 1500, h: 2300, passo: 18, seme: 21, verdi: 0.3,
    curve: [[220, 0.0030, 0.3, 0.30], [180, 0.0036, 2.4, 0.80]], larga: 170 });
  el('div', 'ca-vigna', fondo);
  tl.fromTo(retW, { x: 0, y: 0 }, { x: -80, y: -60, duration: x.e - x.s, ease: 'none' }, x.s);
  // titolo: «3 motivi» (detto: «ecco tre motivi»), la cifra in verde
  const tt = el('div', 'caa-titolo', vis);
  px(tt, { top: d.y_titolo || 300, fontSize: d.corpo_titolo || 132 });
  const c3 = el('span', 'caa-tcifra', tt);
  // il «3» e detto («tre motivi»): compare gia giusto, senza rimescolarsi (giro 3)
  c3.innerHTML = esc(d.titolo.cifra);
  gsap.set(c3, { opacity: 0 });
  tl.set(c3, { opacity: 1 }, d.titolo.t);
  el('span', 'caa-tsp', tt, ' ');
  const tm = el('span', 'caa-ttesto', tt);
  decifraStretto(tm, d.titolo.testo, d.titolo.t, 8, 5);
  // le card, una sotto l'altra
  const scena = el('div', 'caa-scena', vis);
  const W = d.w || 940, H = d.h || 230, gap = d.gap || 36, rot = d.rot === undefined ? 7 : d.rot;
  const X = d.x !== undefined ? d.x : (QW - W) / 2;
  const corpo = d.corpo || 88;
  const n = d.carte.length, carte = [], accese = [], veli = [], accesaDa = [];
  // alone della card accesa (giro 3, direttore): bagliore verde morbido ~30-40 px fuori dal bordo
  const ALONE = '0 0 0 2px rgba(214,255,224,0.9), 0 0 18px rgba(114,250,147,0.75), 0 0 40px rgba(114,250,147,0.45), 0 0 90px rgba(114,250,147,0.18), 0 40px 90px rgba(0,8,22,0.6)';
  const SPENTO = '0 0 0 2px rgba(141,255,169,0.25), 0 4px 8px rgba(0,8,22,0.6), 0 40px 90px rgba(0,8,22,0.6)';
  d.carte.forEach((c, i) => {
    const cy = d.y + i * (H + gap);
    const k = el('div', 'ca-card caa-card', scena);
    carte.push(k);
    px(k, { left: X, top: cy, width: W, height: H });
    gsap.set(k, { rotationX: rot * (1 - i) * (n === 3 ? 1 : 0), transformOrigin: '50% 50%', color: '#F4F4F4' });
    el('div', 'ca-trama', k);
    const luce = el('div', 'ca-luce', k);
    el('div', 'ca-onda', luce); el('div', 'ca-onda2', luce); el('div', 'ca-onda3', luce);
    gsap.set(luce, { opacity: 0 });
    const rifl = el('div', 'ca-riflesso', k);
    gsap.set(rifl, { opacity: 0 });
    // giro 2 (direttore): la card in secondo piano si copre di blu opaco, non diventa trasparente
    const velo = el('div', 'caa-velo', k);
    gsap.set(velo, { opacity: 0 });
    veli.push(velo);
    // giro 2: riflesso tenue che scorre sulle card spente (apertura: niente schermo fermo)
    (d.lucine || []).forEach((tl0) => {
      const t1 = tl0 + i * 0.22;
      tl.set(rifl, { opacity: 0.22 }, t1);
      tl.fromTo(rifl, { xPercent: 0 }, { xPercent: 420, duration: 0.7, ease: 'sine.inOut', immediateRender: false }, t1);
      tl.set(rifl, { opacity: 0 }, t1 + 0.7);
    });
    const ico = el('div', 'ca-ico caa-ico', k);
    const icoT = el('div', 'ca-ico-t caa-ico-t', ico, '?');
    const icoN = el('div', 'ca-ico-t caa-ico-t', ico, esc(c.num));
    gsap.set(icoN, { opacity: 0 });
    if (d.pulsa) {
      let tp = d.pulsa[0] + i * 0.18;
      while (tp + 0.5 < Math.min(d.pulsa[1], c.t_num)) {
        tl.to(icoT, { scale: 1.12, duration: 0.25, ease: 'sine.inOut' }, tp);
        tl.to(icoT, { scale: 1, duration: 0.25, ease: 'sine.inOut' }, tp + 0.25);
        tp += 0.9;
      }
    }
    const chi = el('div', 'caa-chiave', k);
    px(chi, { fontSize: corpo, height: Math.round(corpo * 1.2), marginTop: -Math.round(corpo * 0.6) });
    const pun = el('span', 'ca-punti caa-punti', chi, '• • • • • • •');
    // entrata: banda di scansione che sale (come card_accese)
    const te = d.t_entra + i * 2 * FR, de = 12 * FR;
    gsap.set(k, { clipPath: 'inset(100% 0% 0% 0% round 34px)' });
    tl.to(k, { clipPath: 'inset(0% 0% 0% 0% round 34px)', duration: de, ease: 'power2.inOut' }, te);
    tl.set(k, { clipPath: 'none' }, te + de + FR);   // giro 3: senza maschera l'alone della card accesa si vede
    const banda = el('div', 'ca-banda', k);
    const tele = [0, 1, 2].map((j) => {
      const cv = el('canvas', '', banda);
      cv.width = 230; cv.height = 48;
      const g = cv.getContext('2d');
      const r = semi(100 + i * 10 + j);
      for (let yy = 0; yy < 48; yy += 3) {
        for (let xx = 0; xx < 230; xx += 3) {
          const v = r() * (1 - Math.abs(yy - 24) / 26);
          if (v < 0.25) continue;
          g.fillStyle = `rgba(${r() < 0.5 ? '114,250,147' : '185,255,200'},${Math.min(1, v * 1.2)})`;
          g.fillRect(xx, yy, 3, 3);
        }
      }
      gsap.set(cv, { opacity: 0 });
      return cv;
    });
    gsap.set(banda, { y: H - 48, opacity: 0 });
    tl.set(banda, { opacity: 1 }, te);
    tl.to(banda, { y: -96, duration: de, ease: 'power2.inOut' }, te);
    tl.set(banda, { opacity: 0 }, te + de);
    for (let f = 0; f * FR < de; f++) tele.forEach((cv, j) => tl.set(cv, { opacity: j === f % 3 ? 1 : 0 }, te + f * FR));
    tele.forEach((cv) => tl.set(cv, { opacity: 0 }, te + de));
    tl.fromTo(k, { filter: 'brightness(1.8)' }, { filter: 'brightness(1)', duration: 8 * FR, ease: 'power2.out' }, te + de - 4 * FR);
    // sulla parola del numero («primo», «secondo», «terzo»): il bordo si accende, «?» -> cifra
    tl.to(k, { boxShadow: '0 0 0 2px rgba(141,255,169,0.95), 0 0 34px rgba(114,250,147,0.65), 0 0 110px rgba(114,250,147,0.32), 0 40px 90px rgba(0,8,22,0.6)',
      duration: 4 * FR, ease: 'power2.out' }, c.t_num - 2 * FR);
    tl.set(icoT, { opacity: 0 }, c.t_num);
    tl.set(icoN, { opacity: 1 }, c.t_num);
    // il testo si decifra e finisce sulla parola chiave
    tl.set(pun, { opacity: 0 }, c.t_chiave - 12 * FR);
    decifraStretto(chi, c.chiave, c.t_chiave - 12 * FR, 12, 50 + i);
    const tf = c.t_chiave + 3 * FR;
    accese.push(c.t_stato !== undefined ? c.t_stato : c.t_num - 4 * FR);   // il cambio di stato a scena nascosta
    tl.to(luce, { opacity: 0.55, duration: FR, ease: 'none' }, tf);
    tl.to(luce, { opacity: 1, duration: 2 * FR, ease: 'power1.out' }, tf + FR);
    tl.to(k, { color: '#002552', duration: 2 * FR }, tf + FR);
    tl.to(ico, { borderColor: '#002552', backgroundColor: '#002552', boxShadow: '0 4px 12px rgba(0,37,82,0.35)', duration: 2 * FR }, tf + FR);
    tl.to(k, { boxShadow: ALONE, duration: 3 * FR }, tf + FR);
    accesaDa.push(tf);
    tl.set(rifl, { opacity: 1 }, tf + 2 * FR);
    tl.fromTo(rifl, { xPercent: 0 }, { xPercent: 420, duration: 6 * FR, ease: 'power2.inOut', immediateRender: false }, tf + 2 * FR);
    tl.set(rifl, { opacity: 0 }, tf + 8 * FR);
    tl.fromTo(k, { scale: 1 }, { scale: 1.04, duration: 3 * FR, ease: 'power2.out', immediateRender: false }, tf);
    tl.to(k, { scale: 1, duration: 6 * FR, ease: 'back.out(1.4)' }, tf + 3 * FR);
  });
  // contrasto di stato: sulla parola del numero la card nominata resta piena, le altre al 42%;
  // nel riepilogo tornano tutte piene
  accese.forEach((t, i) => {
    veli.forEach((v, j) => tl.to(v, { opacity: j === i ? 0 : (d.velo || 0.48), duration: 4 * FR, ease: 'power2.out' }, t));
    // l'alone cala sulle card accese che passano in secondo piano
    carte.forEach((k, j) => { if (j !== i && accesaDa[j] !== undefined && accesaDa[j] < t) tl.to(k, { boxShadow: SPENTO, duration: 4 * FR }, t); });
  });
  if (d.t_riepilogo !== undefined) {
    veli.forEach((v) => tl.to(v, { opacity: 0, duration: 6 * FR }, d.t_riepilogo));
    carte.forEach((k) => tl.to(k, { boxShadow: ALONE, duration: 6 * FR }, d.t_riepilogo));
  }
};

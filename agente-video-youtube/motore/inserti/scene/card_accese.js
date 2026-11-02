// Card che si accendono (campionario v3, reference gadzhi-08/09/12/15): scena scura a
// tutto schermo, tre card in prospettiva con la cifra gigante a contorno. Arrivano
// NASCOSTE («?» e punti) con una banda di scansione luminosa che sale; quando lui nomina
// una cosa, la camera ci va, il bordo si accende, il testo si decifra sulla parola e la
// card si riempie di luce verde (testo blu notte sopra il verde, regola del brand) con
// un riflesso e un colpo di scala. Alla fine la camera torna indietro: tutte accese.
// d: titolo {occ, t_occ, tit, t_tit}, t_entra, x0, y, w, h, gap, rot,
//    carte [{pre, t_pre, chiave, t_chiave, dopo: [righe], t_dopo}], t_fine_cam
MODELLI.card_accese = function (box, x, d) {
  const fondo = el('div', 'ca-fondo v3-fondo', box);
  const retW = el('div', 'ca-ret', fondo);
  retino(retW, { w: 2400, h: 1400, passo: 18, seme: 21, verdi: 0.3,
    curve: [[260, 0.0022, 0.3, 0.35], [200, 0.0029, 2.4, 0.82]], larga: 170 });
  el('div', 'ca-vigna', fondo);
  const dur = x.e - x.s;
  tl.fromTo(retW, { x: 0, y: 0 }, { x: -120, y: -30, duration: dur, ease: 'none' }, x.s);
  gsap.set(fondo, { opacity: x.s <= FR ? 1 : 0 });
  if (x.s > FR) tl.set(fondo, { opacity: 1 }, x.s);
  // titolo in alto (fermo: la camera non lo muove)
  const tt = el('div', 'ca-titolo v3-pezzo', fondo);
  const r1 = el('div', 'ca-riga1', tt);
  const o1 = el('span', 'ca-occ', r1);
  decifra(o1, d.titolo.occ, d.titolo.t_occ, 6, 3);
  const r2 = el('div', 'ca-riga', tt);
  const o2 = el('span', 'ca-tit', r2);
  decifra(o2, d.titolo.tit, d.titolo.t_tit, 8, 5);
  // la camera (contenitore delle card)
  const cam = el('div', 'ca-cam', fondo);
  const scena = el('div', 'ca-scena', cam);
  const W = d.w || 500, H = d.h || 640, gap = d.gap || 40, rot = d.rot === undefined ? 18 : d.rot;
  const carte = [], accese = [];
  const n = d.carte.length;
  const x0 = d.x0 !== undefined ? d.x0 : (1920 - (n * W + (n - 1) * gap)) / 2;
  const centri = [];
  d.carte.forEach((c, i) => {
    const cx = x0 + i * (W + gap);
    centri.push(cx + W / 2);
    const k = el('div', 'ca-card v3-pezzo', scena);
    carte.push(k);
    px(k, { left: cx, top: d.y || 330, width: W, height: H });
    gsap.set(k, { rotationY: rot * (1 - i) * (n === 3 ? 1 : 0), transformOrigin: '50% 50%', color: '#F4F4F4' });
    el('div', 'ca-trama', k);
    const luce = el('div', 'ca-luce', k);
    el('div', 'ca-onda', luce);
    el('div', 'ca-onda2', luce);
    el('div', 'ca-onda3', luce);
    gsap.set(luce, { opacity: 0 });
    const rifl = el('div', 'ca-riflesso', k);
    gsap.set(rifl, { opacity: 0 });
    const cif = el('div', 'ca-cifra', k, String(i + 1));
    const cifP = el('div', 'ca-cifra-p', k, String(i + 1));
    gsap.set(cifP, { opacity: 0 });
    if (d.cifre === false) gsap.set([cif, cifP], { display: 'none' });   // fase 7c: senza cifre a contorno
    const ico = el('div', 'ca-ico', k);
    const icoT = el('div', 'ca-ico-t', ico, '?');
    const tx = el('div', 'ca-testo', k);
    const pre = el('div', 'ca-pre', tx);
    const pun1 = el('span', 'ca-punti', pre, '• • • • •');
    const chi = el('div', 'ca-chiave', tx);
    const pun2 = el('span', 'ca-punti', chi, '• • • • • • •');
    gsap.set(pun2, { y: 26 });
    // entrata: banda di scansione che sale (3 trame di rumore che si alternano a ogni frame)
    const te = d.t_entra + i * 2 * FR, de = 12 * FR;
    gsap.set(k, { clipPath: 'inset(100% 0% 0% 0% round 34px)' });
    tl.to(k, { clipPath: 'inset(0% 0% 0% 0% round 34px)', duration: de, ease: 'power2.inOut' }, te);
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
    for (let f = 0; f * FR < de; f++) {
      tele.forEach((cv, j) => tl.set(cv, { opacity: j === f % 3 ? 1 : 0 }, te + f * FR));
    }
    tele.forEach((cv) => tl.set(cv, { opacity: 0 }, te + de));
    tl.fromTo(k, { filter: 'brightness(1.8)' }, { filter: 'brightness(1)', duration: 8 * FR, ease: 'power2.out' }, te + de - 4 * FR);
    // accensione sulla parola
    const ta = c.t_pre - 4 * FR;
    tl.to(k, { boxShadow: '0 0 0 2px rgba(141,255,169,0.95), 0 0 34px rgba(114,250,147,0.65), 0 0 110px rgba(114,250,147,0.32), 0 40px 90px rgba(0,8,22,0.6)',
      duration: 4 * FR, ease: 'power2.out' }, ta);
    tl.set(pun1, { opacity: 0 }, c.t_pre - FR);
    decifra(pre, c.pre, c.t_pre - FR, 8, 40 + i);
    tl.set(pun2, { opacity: 0 }, c.t_chiave - 10 * FR);
    decifra(chi, c.chiave, c.t_chiave - 10 * FR, 12, 50 + i);
    (c.dopo || []).forEach((riga, j) => {
      const dd = el('div', 'ca-dopo2', tx);
      decifra(dd, riga, (c.t_dopo !== undefined ? c.t_dopo : c.t_chiave) + j * 3 * FR, 10, 60 + i * 3 + j);
    });
    // il numero del riquadro non si rimescola (direttore): «?» -> cifra, netto
    const icoN = el('div', 'ca-ico-t', ico, String(i + 1));
    gsap.set(icoN, { opacity: 0 });
    tl.set(icoT, { opacity: 0 }, c.t_chiave - 2 * FR);
    tl.set(icoN, { opacity: 1 }, c.t_chiave - 2 * FR);
    const tf = c.t_chiave + 3 * FR;
    accese.push(tf);
    tl.to(luce, { opacity: 0.55, duration: FR, ease: 'none' }, tf);
    tl.to(luce, { opacity: 1, duration: 2 * FR, ease: 'power1.out' }, tf + FR);
    tl.to(k, { color: '#002552', duration: 2 * FR }, tf + FR);
    // riquadro del numero sulla card accesa: blu notte pieno con la cifra verde (non sparisce sul verde)
    tl.to(ico, { borderColor: '#002552', backgroundColor: '#002552', boxShadow: '0 4px 12px rgba(0,37,82,0.35)', duration: 2 * FR }, tf + FR);
    tl.to(cif, { opacity: 0, duration: 2 * FR }, tf + FR);
    tl.to(cifP, { opacity: 0.35, duration: 3 * FR }, tf + FR);
    tl.to(k, { boxShadow: '0 0 0 2px rgba(214,255,224,0.9), 0 0 24px rgba(114,250,147,0.55), 0 0 80px rgba(114,250,147,0.25), 0 40px 90px rgba(0,8,22,0.6)', duration: 3 * FR }, tf + FR);
    tl.set(rifl, { opacity: 1 }, tf + 2 * FR);
    tl.fromTo(rifl, { xPercent: 0 }, { xPercent: 420, duration: 6 * FR, ease: 'power2.inOut', immediateRender: false }, tf + 2 * FR);
    tl.set(rifl, { opacity: 0 }, tf + 8 * FR);
    tl.fromTo(k, { scale: 1 }, { scale: 1.05, duration: 3 * FR, ease: 'power2.out', immediateRender: false }, tf);
    tl.to(k, { scale: 1, duration: 6 * FR, ease: 'back.out(1.4)' }, tf + 3 * FR);
  });
  // contrasto di stato (direttore v3): quando una card si accende le altre scendono al 42%,
  // alla fine tornano tutte piene (riepilogo, come gadzhi-15)
  accese.forEach((tf, i) => {
    carte.forEach((k, j) => tl.to(k, { opacity: j === i ? 1 : 0.42, duration: 4 * FR, ease: 'power2.out' }, tf - 4 * FR));
  });
  carte.forEach((k) => tl.to(k, { opacity: 1, duration: 6 * FR }, d.t_fine_cam));
  // camera: va sulla card nominata, poi torna larga
  const fuoco = (i) => ({ x: (960 - centri[i]) * 0.55, y: -20, scale: 1.1 });
  d.carte.forEach((c, i) => {
    tl.to(cam, Object.assign({ duration: 0.55, ease: 'sine.inOut' }, fuoco(i)), c.t_pre - 0.5);
  });
  tl.to(cam, { x: 0, y: 0, scale: 1, duration: 0.7, ease: 'sine.inOut' }, d.t_fine_cam);
  tl.set(fondo, { opacity: 0 }, x.e);
};

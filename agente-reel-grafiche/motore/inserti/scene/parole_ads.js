// Parole dette che si accendono, per gli ads 9:16, nella finestra (laboratorio, AD_REFLUSSO, 04/11/2026). Modello
// nuovo, da schermata (che resta com'e), reference martell-07 e martell-03. Una riga d'apertura panna c'e dal primo
// fotogramma (le sue parole si mettono a fuoco in fila nei primi fotogrammi); sotto, le parole dette arrivano una per
// una sulla voce: ognuna nasce grigia e sfocata e in 3 fotogrammi diventa piena, verde, con il bagliore (martell-07); le
// tre si accendono una dopo l'altra in colonna dal centro (martell-03, senza figure). Dietro, una griglia di punti con
// alone appena visibile e una camera che avanza lenta (scala 1 -> 1,025). Fondo pieno della finestra a taglio
// all'entrata e all'uscita, alfa 0 fuori dal rettangolo. Niente decifrazioni.
// d: rett {x, y, w, h, r} o [{da, ...}], apertura {testo, t, y, corpo}, parole [{testo, t, y, corpo, verde}], corpo,
//    camera (scala finale), accendi_fr
MODELLI.parole_ads = function (box, x, d) {
  const QW = 1080, EPS = 0.001;
  const clip = el('div', 'pfa-clip', box);
  const fondo = el('div', 'pfa-fondo fondo-sito', clip);
  const dentro = el('div', 'pfa-dentro', clip);
  const RR = Array.isArray(d.rett) ? d.rett : [Object.assign({ da: 0 }, d.rett)];
  const metti = (R, t) => {
    const a = { left: R.x + 'px', top: R.y + 'px', width: R.w + 'px', height: R.h + 'px', borderRadius: R.r + 'px' };
    const f = { width: R.w + 'px', height: R.h + 'px' }, dd = { left: -R.x + 'px', top: -R.y + 'px' };
    if (t === undefined) { gsap.set(clip, a); gsap.set(fondo, f); gsap.set(dentro, dd); }
    else { tl.set(clip, a, t - EPS); tl.set(fondo, f, t - EPS); tl.set(dentro, dd, t - EPS); }
  };
  metti(RR[0]);
  RR.slice(1).forEach((R) => metti(R, R.da));
  gsap.set(clip, { opacity: 0 });
  tl.set(clip, { opacity: 1 }, x.s);                // entra a taglio con il fondo e l'apertura gia pieni
  tl.set(clip, { opacity: 0 }, x.e - EPS);          // esce a taglio sull'ultimo fotogramma

  // griglia di punti con l'alone, ferma: la muove solo la camera
  const R0 = RR[0];
  const g = el('canvas', 'pfa-griglia', dentro);
  g.width = R0.w; g.height = R0.h;
  px(g, { left: R0.x, top: R0.y, width: R0.w, height: R0.h });
  const c = g.getContext('2d'), passo = 34;
  for (let yy = passo / 2; yy < R0.h; yy += passo) {
    for (let xx = passo / 2; xx < R0.w; xx += passo) {
      const dx = (xx - R0.w / 2) / (R0.w / 2), dy = (yy - R0.h * 0.55) / (R0.h / 2);
      const v = Math.max(0, 1 - Math.sqrt(dx * dx * 0.8 + dy * dy));
      if (v <= 0.03) continue;
      c.fillStyle = `rgba(114,250,147,${0.05 + 0.16 * v})`;
      c.beginPath(); c.arc(xx, yy, 1.6 + 1.6 * v, 0, 6.2832); c.fill();
    }
  }
  const cam = el('div', 'pfa-cam', dentro);
  const cy = R0.y + R0.h / 2;
  gsap.set(cam, { transformOrigin: `540px ${cy}px` });
  gsap.set(g, { transformOrigin: `${R0.w / 2}px ${R0.h / 2}px` });
  tl.fromTo([cam, g], { scale: 1 }, { scale: d.camera || 1.025, duration: x.e - x.s, ease: 'none', immediateRender: false }, x.s);

  const corpo = d.corpo || 96;
  const riga = (y, cp) => {
    const r = el('div', 'pfa-riga', cam);
    const lh = Math.round(cp * 1.2);
    px(r, { top: y - lh / 2, height: lh, lineHeight: lh + 'px', fontSize: cp });
    return r;
  };
  // apertura: c'e dal primo fotogramma; le parole passano da grigie a panna in fila (1 fotogramma l'una)
  let apertura = null;
  if (d.apertura) {
    const r = riga(d.apertura.y, d.apertura.corpo || 84);
    apertura = r;
    const pp = d.apertura.testo.split(' ');
    pp.forEach((w, k) => {
      const s = el('span', 'pfa-w pfa-ap', r, esc(w));
      if (k < pp.length - 1) r.appendChild(document.createTextNode(' '));
      const t0 = d.apertura.t + k * FR;
      tl.fromTo(s, { color: '#B4BCC8', filter: 'blur(1.5px)', opacity: 0.9 },
        { color: '#F4F4F4', filter: 'blur(0px)', opacity: 1, duration: 3 * FR, ease: 'power2.out', immediateRender: true }, t0);
    });
  }
  // le parole dette: grigie e sfocate al loro tempo, piene e verdi con il bagliore in 3 fotogrammi
  const nf = d.accendi_fr || 3;
  // direttore (AD_EMICRANIA, giro 1): una riga sola per volta ha la luce piena; le righe gia dette scendono (opacita
  // d.attenua, 0,62) e perdono il bagliore quando arriva la successiva; le righe panna non hanno alone verde
  const att = d.attenua === undefined ? 0.62 : d.attenua;
  const fatte = [];
  (d.parole || []).forEach((p, i) => {
    const r = riga(p.y, p.corpo || corpo);
    const s = el('span', 'pfa-w pfa-p' + (p.verde ? ' pfa-k' : ''), r, esc(p.testo));
    // fase 6, giro 4 (variante in prova «-icone»): un disco con l'icona davanti alla parola, nel colore della parola (nasce
    // grigio e si accende con lei); icona Tabler («tabler:...») o disegno Servier («servier»). Senza icona: com'era
    if (p.icona || p.src) {
      const cp = p.corpo || corpo, L = Math.round(cp * 1.08);
      const dsc = el('span', 'pfa-disco', null);
      s.insertBefore(dsc, s.firstChild);
      px(dsc, { width: L, height: L, marginRight: Math.round(cp * 0.3), borderRadius: L / 2, verticalAlign: Math.round(-L * 0.22) + 'px' });
      if (p.src) {
        const im = el('img', 'pfa-img', dsc); im.src = p.src;
        const k = Math.min(L * 0.78 / p.img_w, L * 0.78 / p.img_h);
        px(im, { width: p.img_w * k, height: p.img_h * k, left: (L - p.img_w * k) / 2, top: (L - p.img_h * k) / 2 });
      } else {
        const n = String(p.icona).replace(/^tabler:/, ''), li = Math.round(L * 0.62);
        const ic = svg('svg', { viewBox: '0 0 24 24', width: li, height: li }, dsc);
        ic.setAttribute('class', 'pfa-ic');
        px(ic, { left: (L - li) / 2, top: (L - li) / 2 });
        ((typeof TABLER !== 'undefined' && TABLER[n]) || []).forEach((dd) => svg('path', { d: dd, fill: 'none', stroke: 'currentColor',
          'stroke-width': 2, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, ic));
      }
    }
    gsap.set(s, { opacity: 0 });
    tl.fromTo(s, { opacity: 0.55, color: '#7D879A', scale: 0.96, filter: 'blur(9px)', textShadow: '0 0 0 rgba(114,250,147,0)' },
      { opacity: 1, color: p.verde ? '#72FA93' : '#F4F4F4', scale: 1, filter: 'blur(0px)',
        textShadow: p.verde ? '0 0 2px #0B1E3A, 0 0 30px rgba(114,250,147,1), 0 0 80px rgba(114,250,147,0.6)'
          : '0 0 2px #0B1E3A, 0 0 26px rgba(244,244,244,0.45), 0 6px 22px rgba(0,8,22,0.7)',
        duration: nf * FR, ease: 'power2.out', immediateRender: false }, p.t);
    // il bagliore si posa
    tl.to(s, { textShadow: p.verde ? '0 0 2px #0B1E3A, 0 0 22px rgba(114,250,147,0.8), 0 0 60px rgba(114,250,147,0.4)'
      : '0 0 2px #0B1E3A, 0 0 16px rgba(244,244,244,0.3), 0 6px 22px rgba(0,8,22,0.7)',
      duration: 10 * FR, ease: 'power2.out' }, p.t + nf * FR);
    // p.gruppo (direttore, AD_BRUXISMO): le righe dello stesso gruppo (una frase su due righe) non si attenuano fra loro
    if (att < 1) fatte.forEach((q) => { if (p.gruppo === undefined || q._gruppo !== p.gruppo) tl.to(q, { opacity: att,
      textShadow: '0 0 2px #0B1E3A, 0 6px 22px rgba(0,8,22,0.7)', duration: 6 * FR, ease: 'power2.out' }, p.t); });
    s._gruppo = p.gruppo;
    // d.attenua_apertura: la riga d'apertura («pensato per») scende di un gradino quando arriva la prima riga verde
    if (d.attenua_apertura && p.verde && !fatte.some((q) => q._verde) && apertura) tl.to(apertura, { opacity: d.attenua_apertura,
      duration: 6 * FR, ease: 'power2.out' }, p.t);
    s._verde = !!p.verde;
    fatte.push(s);
  });
};

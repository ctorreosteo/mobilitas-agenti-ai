// Micro-grafiche per i reel 9:16 (agente reel-grafiche, fase 6, 05/11/2026). Modello nuovo, IN PROVA: il livello
// piccolo della densità «piena» (un cambiamento visivo ogni 2-3 s), fra un'infografica grande e l'altra. Sta sopra
// il video base, dentro il suo riquadro `box` (alfa 0 fuori: il motore lo controlla), lontano da volti, mani,
// sottotitoli e scritte del video (zone libere della radiografia). Reference: gadzhi-17 (pillola con la parola
// chiave, evidenziatore che si stende), gadzhi-19 (pillola di vetro con l'icona: icona, poi la pillola che si
// allunga, poi il testo in ~4 fotogrammi), gadzhi-14 (icona che si disegna con il tratto), gadzhi-18 (numero detto
// grande, già giusto), gadzhi-02 (nota a margine piccola, non copre niente), gadzhi-13 (frecce).
// Niente contenitori vuoti: la pillola nasce con la sua parola. Niente decifrazioni. Uscita a taglio (default) o
// rapida (4 fotogrammi, `uscita: "rapida"`).
// d: box {x, y, w, h}, tipo "parola" | "icona" | "numero" | "freccia" | "cerchio",
//    parola: testo, t, corpo (>= minimo), verde (pillola verde, testo blu notte), icona (nome, a sinistra), evidenzia (t:
//            l'evidenziatore verde si stende dietro la parola), allinea "sx" | "dx" | "centro"
//    icona: icona (nome), t, lato, etichetta {testo, t, corpo}
//    numero: testo (cifra detta), t, corpo, etichetta {testo, t, corpo}
//    freccia: da [x, y], a [x, y], t (si disegna in 6 fotogrammi), punta (px)
//    cerchio: c [x, y], r, t (si disegna in 8 fotogrammi), etichetta {testo, t, corpo, lato "sopra"|"sotto"}
//    uscita "taglio" | "rapida"
// Giro 3 (Riccardo, 05/11/2026: «micro-grafiche grandi e visibili, niente badge negli angoli; negli ads con le finestre la
// finestra grande è la tela principale»): due forme grandi, che riempiono il riquadro nella finestra grande.
//    scheda: card di vetro con il disco dell'icona a sinistra e le righe a destra (gadzhi-19, in grande);
//            icona, t (entrata: card e icona insieme), righe [{testo, t, verde, corpo}] (ogni riga compare sulla sua parola)
//    parole: parole chiave grandi in pannelli di vetro impilati, ognuna sulla sua parola detta (gadzhi-17, kinetic);
//            righe [{testo, t, verde, corpo}], allinea "sx" | "dx" | "centro" (default centro), sottolinea {riga, t}
const MIC_ICONE = {
  // oggetti lineari, mai figure umane; senza scritte né cifre
  fiamma: ['M54 98 c-22 0 -34 -16 -30 -36 c3 -14 14 -22 16 -38 c10 8 14 18 12 28 c6 -4 9 -10 9 -18 c14 12 23 28 21 42 c-2 14 -12 22 -28 22 Z',
    'M54 98 c-9 0 -14 -7 -12 -16 c2 -7 8 -10 9 -18 c8 6 15 14 14 22 c-1 7 -5 12 -11 12'],
  piatto: ['M54 26 a34 34 0 1 0 0.01 0', 'M54 42 a18 18 0 1 0 0.01 0', 'M12 22 V48 a6 6 0 0 0 12 0 V22', 'M18 48 V96', 'M96 22 c-8 6 -10 18 -10 30 H96 V96'],
  pillola: ['M30 78 L78 30 a17 17 0 0 0 -24 -24 L6 54 a17 17 0 0 0 24 24 Z', 'M30 30 L54 54'],
  goccia: ['M54 12 C40 34 26 50 26 66 a28 28 0 0 0 56 0 C82 50 68 34 54 12 Z', 'M42 70 a12 12 0 0 0 12 12'],
  orologio: ['M54 18 a36 36 0 1 0 0.01 0', 'M54 32 V54 L70 64'],
  domanda: ['M38 38 a16 16 0 1 1 22 15 c-4 2 -6 5 -6 10 V70', 'M54 86 h0.01'],
  stella: ['M54 14 L64 42 L94 42 L70 60 L79 90 L54 72 L29 90 L38 60 L14 42 L44 42 Z'],
  freccia_su: ['M54 92 V18', 'M30 42 L54 18 L78 42'],
};

MODELLI.micro_reel = function (box, x, d) {
  const EPS = 0.001;
  const B = d.box;
  const clip = el('div', 'mic-clip', box);
  px(clip, { left: B.x, top: B.y, width: B.w, height: B.h });
  const dentro = el('div', 'mic-dentro', clip);
  px(dentro, { left: -B.x, top: -B.y });
  gsap.set(clip, { opacity: 0 });
  tl.set(clip, { opacity: 1 }, x.s);
  if (d.uscita === 'rapida') {
    tl.to(dentro, { opacity: 0, scale: 0.96, filter: 'blur(6px)', duration: 4 * FR, ease: 'power2.in' }, x.e - 4 * FR);
    tl.set(clip, { opacity: 0 }, x.e - EPS);
  } else {
    tl.set(clip, { opacity: 0 }, x.e - EPS);
  }
  const ICONE = Object.assign({}, typeof RIA_ICONE !== 'undefined' ? RIA_ICONE : {}, MIC_ICONE);
  const disegnaIcona = (nome, cx, cy, lato, t, dove) => {
    const s = svg('svg', { viewBox: '0 0 108 108', width: lato, height: lato }, dove);
    s.setAttribute('class', 'mic-ic');
    px(s, { left: cx - lato / 2, top: cy - lato / 2 });
    (ICONE[nome] || []).forEach((dd, j) => {
      const p = svg('path', { d: dd, fill: 'none', stroke: '#8DFFA9', 'stroke-width': /h0\.01$/.test(dd) ? 10 : 6,
        'stroke-linecap': 'round', 'stroke-linejoin': 'round', pathLength: 1 }, s);
      p.setAttribute('stroke-dasharray', '1 1');
      if (t <= 0) return;
      gsap.set(p, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(p, { attr: { 'stroke-dashoffset': 0 }, duration: 10 * FR, ease: 'power2.out' }, t + j * FR);
    });
    return s;
  };
  const testo = (o, cls, x0, y0, allinea, dove) => {
    // «|» va a capo; o.vetro: la scritta sta in un pannellino di vetro blu (leggibile anche su un fondo chiaro)
    const righe = String(o.testo).split('|');
    const verdi = o.verde === true ? righe.map((_, i) => i) : (o.verde || []);
    const r = el('div', 'mic-t ' + (cls || '') + (o.vetro ? ' mic-vetro' : ''), dove,
      righe.map((x, i) => verdi.includes(i) ? `<span class="mic-tv">${esc(x)}</span>` : esc(x)).join('<br>'));
    // via: il testo esce quando la sua frase è finita (direttore, 05/11/2026: mai due cose da leggere col sottotitolo dopo)
    if (o.via !== undefined) tl.set(r, { opacity: 0 }, o.via);
    const cp = o.corpo || 88, lh = Math.round(cp * 1.15), pv = o.vetro ? Math.round(cp * 0.22) : 0;
    px(r, { fontSize: cp, lineHeight: lh + 'px', top: y0 - Math.round(lh / 2) - pv });
    if (o.vetro) px(r, { padding: `${pv}px ${Math.round(cp * 0.42)}px`, borderRadius: Math.round(cp * 0.4), textAlign: 'center' });
    if (allinea === 'dx') px(r, { right: 1080 - x0 }); else if (allinea === 'centro') { px(r, { left: x0 }); gsap.set(r, { xPercent: -50 }); }
    else px(r, { left: x0 });
    return r;
  };
  const cx = B.x + B.w / 2, cy = B.y + B.h / 2;
  // margine interno per ombre e bagliori (fase 6: il riquadro tagliava l'ombra in un rettangolo; il render lo controlla)
  const M = d.margine === undefined ? 22 : d.margine;
  // aggancio (fase 6): con t <= 0 la micro-grafica è già intera al primo fotogramma (un tween che finisce prima di 0 non
  // viene mai disegnato: nella prima prova la pillola compariva solo al fotogramma 12)
  const intera = d.t !== undefined && d.t <= 0;

  if (d.tipo === 'parola') {
    // pillola di vetro (o verde) che si allunga con la parola dentro; icona tonda a sinistra (gadzhi-19)
    const cp = d.corpo || 88, h = Math.round(cp * 1.5), pad = Math.round(cp * 0.42);
    const ic = d.icona ? h : 0;
    const pil = el('div', 'mic-pil' + (d.verde ? ' mic-pil-v' : ''), dentro);
    const lab = el('span', 'mic-pw' + (d.verde ? ' mic-pw-v' : ''), pil, esc(d.testo));
    px(lab, { fontSize: cp, lineHeight: h + 'px' });
    px(pil, { height: h, borderRadius: h / 2, paddingLeft: pad + (ic ? ic * 0.86 : 0), paddingRight: pad, top: cy - h / 2 });
    const al = d.allinea || 'sx';
    if (al === 'dx') px(pil, { right: 1080 - (B.x + B.w) + M }); else if (al === 'centro') { px(pil, { left: cx }); gsap.set(pil, { xPercent: -50 }); }
    else px(pil, { left: B.x + M });
    if (d.icona) {
      const disco = el('div', 'mic-disco', pil);
      px(disco, { width: h - 14, height: h - 14, left: 7, top: 7 });
      disegnaIcona(d.icona, (h - 14) / 2, (h - 14) / 2, (h - 14) * 0.72, d.t - 3 * FR, disco);
      if (!intera) {
        gsap.set(disco, { scale: 0.6, opacity: 0 });
        tl.to(disco, { scale: 1, opacity: 1, duration: 4 * FR, ease: 'back.out(1.6)' }, d.t - 3 * FR);
      }
    }
    // la pillola si allunga da sinistra e la parola si mette a fuoco: insieme, mai la pillola vuota
    if (!intera) {
      // giro 2 (direttore): il primo fotogramma visibile mostra già l'inizio della parola, mai il solo bordo della pillola
      tl.fromTo(pil, { clipPath: `inset(0 100% 0 0 round ${h / 2}px)` }, { clipPath: `inset(0 0% 0 0 round ${h / 2}px)`, duration: 4 * FR,
        ease: 'power3.out', immediateRender: true }, d.t - 2 * FR);
      tl.fromTo(lab, { opacity: 0.5, filter: 'blur(4px)' }, { opacity: 1, filter: 'blur(0px)', duration: 3 * FR, ease: 'power2.out',
        immediateRender: true }, d.t - 2 * FR);
    }
    // colpo: un piccolo colpo di scala sulla parola detta (aggancio già intero dal fotogramma 0)
    if (d.colpo !== undefined) {
      tl.to(pil, { scale: 1.05, duration: 2 * FR, ease: 'power2.out' }, d.colpo);
      tl.to(pil, { scale: 1, duration: 4 * FR, ease: 'power2.inOut' }, d.colpo + 2 * FR);
    }
    if (d.evidenzia !== undefined) {
      const ev = el('div', 'mic-ev', pil);
      px(ev, { left: pad * 0.6 + (ic ? ic * 0.86 : 0), right: pad * 0.6, top: h * 0.56, height: h * 0.26 });
      gsap.set(ev, { scaleX: 0, transformOrigin: 'left center' });
      tl.to(ev, { scaleX: 1, duration: 6 * FR, ease: 'power2.inOut' }, d.evidenzia);
    }
  } else if (d.tipo === 'icona') {
    // disco con l'icona e, sotto, la parola detta: il blocco intero sta al centro del riquadro
    const lato = d.lato || Math.min(B.w, B.h) * 0.8;
    const E = d.etichetta, cpe = E ? (E.corpo || 84) : 0, lhe = Math.round(cpe * 1.15);
    const he = E ? String(E.testo).split('|').length * lhe + (E.vetro ? 2 * Math.round(cpe * 0.22) : 0) : 0;
    const gap = E ? 22 : 0, tot = lato + gap + he, top = cy - tot / 2;
    const disco = el('div', 'mic-disco mic-disco-g', dentro);
    px(disco, { width: lato, height: lato, left: cx - lato / 2, top: top, borderRadius: lato / 2 });
    // giro 2 (direttore): niente disco vuoto al primo fotogramma: il disco c'è dall'entrata e il tratto è già partito
    disegnaIcona(d.icona, lato / 2, lato / 2, lato * 0.66, d.t - 4 * FR, disco);
    // giro 3: colpo sul disco (un piccolo battito sulla parola detta: un cambio visibile senza testo)
    if (d.colpo !== undefined) {
      // giro 3 (direttore: il battito del 6% non si vedeva): +12% con un lampo del bordo verde, ritorno in 6 fotogrammi
      tl.to(disco, { scale: 1.12, boxShadow: 'inset 0 0 0 6px #72FA93, 0 0 26px rgba(114, 250, 147, 0.75)', duration: 3 * FR, ease: 'power2.out' }, d.colpo);
      tl.to(disco, { scale: 1, boxShadow: 'inset 0 0 0 3px rgba(114, 250, 147, 0.55), 0 0 14px rgba(114, 250, 147, 0.25)', duration: 6 * FR, ease: 'power2.inOut' }, d.colpo + 3 * FR);
    }
    if (E) {
      const r = testo(E, 'mic-et', cx, top + lato + gap + he / 2, 'centro', dentro);
      if (E.vetro) px(r, { top: top + lato + gap });
      else px(r, { top: top + lato + gap });
      tl.fromTo(r, { opacity: 0, filter: 'blur(8px)', y: 10 }, { opacity: 1, filter: 'blur(0px)', y: 0, duration: 4 * FR, ease: 'power2.out',
        immediateRender: true }, E.t);
    }
  } else if (d.tipo === 'numero') {
    // la cifra detta, già giusta dal primo fotogramma: entra con un colpo di scala e il bagliore
    const cp = d.corpo || 220;
    const dy = d.etichetta ? -Math.round((d.etichetta.corpo || 84) * 0.6) : 0;
    const n = testo({ testo: d.testo, corpo: cp }, 'mic-num', cx, cy + dy, 'centro', dentro);
    tl.fromTo(n, { opacity: 0.6, scale: 1.1, filter: 'blur(4px)' }, { opacity: 1, scale: 1, filter: 'blur(0px)', duration: 3 * FR,
      ease: 'power3.out', immediateRender: true }, d.t - 2 * FR);
    if (d.etichetta) {
      const r = testo(d.etichetta, 'mic-et', cx, cy + dy + cp * 0.5 + Math.round((d.etichetta.corpo || 84) * 0.55), 'centro', dentro);
      tl.fromTo(r, { opacity: 0, filter: 'blur(8px)' }, { opacity: 1, filter: 'blur(0px)', duration: 4 * FR, ease: 'power2.out',
        immediateRender: true }, d.etichetta.t);
    }
  } else if (d.tipo === 'scheda') {
    // card di vetro grande: disco con l'icona che si disegna + righe che compaiono sulla voce; mai vuota (nasce con l'icona
    // e la prima riga entra entro 3 fotogrammi)
    const R_ = d.righe || [], cp = d.corpo || 112, lh = Math.round(cp * 1.12);
    const W_ = B.w - 2 * M, H_ = B.h - 2 * M, pad = Math.round(cp * 0.42);
    const card = el('div', 'mic-scheda', dentro);
    px(card, { left: B.x + M, top: B.y + M, width: W_, height: H_, borderRadius: Math.round(Math.min(56, H_ * 0.22)) });
    const lato = Math.min(H_ - 2 * pad, Math.round(cp * 1.9));
    const disco = el('div', 'mic-disco mic-disco-g', card);
    px(disco, { width: lato, height: lato, left: pad, top: (H_ - lato) / 2, borderRadius: lato / 2 });
    disegnaIcona(d.icona, lato / 2, lato / 2, lato * 0.66, intera ? 0 : d.t, disco);
    const tx = pad * 2 + lato, blocco = R_.length * lh;
    R_.forEach((o, i) => {
      const r = el('div', 'mic-t mic-sr' + (o.verde ? ' mic-tv' : ''), card, esc(o.testo));
      const c = o.corpo || cp;
      px(r, { left: tx, top: (H_ - blocco) / 2 + i * lh, fontSize: c, lineHeight: lh + 'px' });
      if (!(intera && (o.t || 0) <= 0)) tl.fromTo(r, { opacity: 0, x: -18, filter: 'blur(6px)' }, { opacity: 1, x: 0, filter: 'blur(0px)',
        duration: 4 * FR, ease: 'power3.out', immediateRender: true }, o.t - FR);
      if (o.via !== undefined) tl.to(r, { opacity: 0, duration: 3 * FR }, o.via - 3 * FR);
    });
    if (!intera) {
      tl.fromTo(card, { opacity: 0, scale: 0.92 }, { opacity: 1, scale: 1, duration: 5 * FR, ease: 'back.out(1.4)', immediateRender: true }, d.t - 2 * FR);
    }
  } else if (d.tipo === 'parole') {
    // parole chiave grandi, ognuna nel suo pannello di vetro, impilate al centro del riquadro; ognuna entra sulla sua parola
    const R_ = d.righe || [], cp = d.corpo || 120;
    const hs = R_.map(o => Math.round((o.corpo || cp) * 1.42)), gap = Math.round(cp * 0.16);
    const tot = hs.reduce((a, b) => a + b, 0) + gap * (R_.length - 1);
    // giro 3 (direttore): «alto» tiene il blocco in cima al riquadro, per lasciare libero il soggetto del B-roll sotto
    let y = d.verticale === 'alto' ? B.y + M : cy - tot / 2;
    const al = d.allinea || 'centro';
    R_.forEach((o, i) => {
      const c = o.corpo || cp, h = hs[i];
      const r = el('div', 'mic-pp' + (o.verde ? ' mic-pp-v' : ''), dentro, esc(o.testo));
      px(r, { top: y, height: h, lineHeight: h + 'px', fontSize: c, borderRadius: Math.round(h * 0.3), padding: `0 ${Math.round(c * 0.36)}px` });
      if (al === 'sx') px(r, { left: B.x + M }); else if (al === 'dx') px(r, { right: 1080 - (B.x + B.w) + M });
      else { px(r, { left: cx }); gsap.set(r, { xPercent: -50 }); }
      if (!(intera && (o.t || 0) <= 0)) {
        // entra a taglio (giro 3, direttore: niente dissolvenza, mai lettere trasparenti sopra il B-roll), già piena, con un piccolo
        // colpo di scala che si assesta in 3 fotogrammi
        gsap.set(r, { opacity: 0 });
        tl.set(r, { opacity: 1 }, o.t - FR);
        tl.fromTo(r, { scale: 1.07 }, { scale: 1, duration: 3 * FR, ease: 'power2.out', immediateRender: false }, o.t - FR);
      }
      if (o.via !== undefined) tl.to(r, { opacity: 0, duration: 3 * FR }, o.via - 3 * FR);
      if (d.sottolinea && d.sottolinea.riga === i) {
        const ev = el('div', 'mic-sott', r);
        gsap.set(ev, { scaleX: 0, transformOrigin: 'left center' });
        tl.to(ev, { scaleX: 1, duration: 6 * FR, ease: 'power2.inOut' }, d.sottolinea.t);
      }
      y += h + gap;
    });
  } else if (d.tipo === 'freccia' || d.tipo === 'cerchio') {
    const s = svg('svg', { viewBox: '0 0 1080 1920', width: 1080, height: 1920 }, dentro);
    s.setAttribute('class', 'mic-svg');
    let p;
    if (d.tipo === 'freccia') {
      const [x0, y0] = d.da, [x1, y1] = d.a, ang = Math.atan2(y1 - y0, x1 - x0), L = d.punta || 34;
      const pd = `M${x0} ${y0} L${x1} ${y1} M${x1 - L * Math.cos(ang - 0.5)} ${y1 - L * Math.sin(ang - 0.5)} L${x1} ${y1} L${x1 - L * Math.cos(ang + 0.5)} ${y1 - L * Math.sin(ang + 0.5)}`;
      p = svg('path', { d: pd, fill: 'none', stroke: '#8DFFA9', 'stroke-width': 9, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', pathLength: 1 }, s);
      p.setAttribute('stroke-dasharray', '1 1');
      gsap.set(p, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(p, { attr: { 'stroke-dashoffset': 0 }, duration: 6 * FR, ease: 'power2.out' }, d.t);
    } else {
      const [c0, c1] = d.c, r = d.r;
      // l'anello parte da in alto a sinistra e si chiude con un piccolo sorpasso, come un segno a mano
      // giro 2 (direttore): giro chiuso, un poco oltre l'inizio (370°), come un segno a mano; tratto più presente
      const ry = r * (d.schiaccia || 0.96), a0 = -2.35, pts = [];
      for (let k = 0; k <= 74; k++) { const a = a0 + (k / 74) * 2 * Math.PI * 1.028; pts.push(`${(c0 + r * Math.cos(a)).toFixed(1)} ${(c1 + ry * Math.sin(a)).toFixed(1)}`); }
      const pd = 'M' + pts.join(' L');
      p = svg('path', { d: pd, fill: 'none', stroke: '#8DFFA9', 'stroke-width': 10, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', pathLength: 1 }, s);
      p.setAttribute('stroke-dasharray', '1 1');
      gsap.set(p, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(p, { attr: { 'stroke-dashoffset': 0 }, duration: 8 * FR, ease: 'power2.inOut' }, d.t);
      if (d.etichetta) {
        const sopra = (d.etichetta.lato || 'sopra') === 'sopra', cpe = d.etichetta.corpo || 84;
        const y = sopra ? c1 - r - cpe * 0.75 : c1 + r + cpe * 0.75;
        const tt = testo(d.etichetta, 'mic-et', c0, y, 'centro', dentro);
        tl.fromTo(tt, { opacity: 0, filter: 'blur(8px)' }, { opacity: 1, filter: 'blur(0px)', duration: 4 * FR, ease: 'power2.out',
          immediateRender: true }, d.etichetta.t);
      }
    }
  }
};

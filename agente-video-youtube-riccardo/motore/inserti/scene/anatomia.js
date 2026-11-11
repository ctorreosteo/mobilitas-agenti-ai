// Animazione anatomica (fase 7b): un disegno Servier Medical Art ricolorato nel
// brand (il motore lo prepara: `anatomia.ricolora`), fermo, e sopra solo forme
// semplici disegnate da noi, ognuna sulla parola che la nomina. Il disegno non si
// deforma mai. Coordinate dei segni: pixel del disegno ORIGINALE (come nei bozzetti
// approvati); il motore passa `scala` e la posizione.
// d: src, w, h, x, y (alto-sinistra a schermo), scala, vw, vh,
//    pannello {x, y, larghezza, altezza, raggio, colore} (facoltativo: card blu), t_figura,
//    segni [{tipo: alone|asse|freccia|numero|arco|linea|contorno, t, e, ...}],
//    etichette [{testo, x, y, corpo, peso, colore, t, e, ancora}], attribuzione
MODELLI.anatomia = function (box, x, d) {
  const verde = '#72FA93', panna = '#F4F4F4';
  const tf = d.t_figura !== undefined ? d.t_figura : x.s;
  if (d.pannello) {
    const p = el('div', 'an-pan', box);
    px(p, { left: d.pannello.x, top: d.pannello.y, width: d.pannello.larghezza, height: d.pannello.altezza });
    if (d.pannello.raggio !== undefined) p.style.borderRadius = d.pannello.raggio + 'px';
    if (d.pannello.colore) p.style.background = d.pannello.colore;
    if (d.pannello.trama) trama(p, d.pannello.larghezza, d.pannello.altezza, d.pannello.trama);
    else el('div', 'an-grana', p);
    if (x.pieno && d.pannello.larghezza >= 1920) {
      // scena scura a tutto schermo: taglio netto con un lampo panna di 3 frame (reference martell-02)
      p.classList.add('an-pieno');
      tl.set(p, { opacity: 1 }, x.s);
      gsap.set(p, { opacity: 0 });
      const l = el('div', 'an-lampo', box);
      gsap.set(l, { opacity: 0 });
      tl.set(l, { opacity: 0.85 }, x.s);
      tl.to(l, { opacity: 0, duration: 4 * FR, ease: 'power2.out' }, x.s + FR);
    } else {
      tl.fromTo(p, { opacity: 0, scale: 0.94, y: 40, filter: 'blur(12px)' },
        { opacity: 1, scale: 1, y: 0, filter: 'blur(0px)', duration: 8 * FR, ease: 'power3.out' }, x.s);
    }
    tl.to(p, { opacity: 0, scale: 0.97, duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
  }
  // camera della scena scura (reference martell-07): figura e segni si muovono
  // insieme; le etichette restano ferme sullo schermo
  const cam = el('div', 'an-cam', box);
  // scena scura: una luce blu morbida dietro la figura (ritocco del direttore, fase 7b:
  // «la figura blu su blu resta piatta»); entra e esce con la figura
  let luce = null;
  if (x.pieno && d.luce !== false && d.pannello && d.pannello.larghezza >= 1920) {
    const R = Math.round(Math.max(d.w, d.h) * (d.luce_r || 0.62));
    luce = el('div', 'an-luce', cam);
    px(luce, { left: Math.round(d.x + d.w / 2 - R), top: Math.round(d.y + d.h * (d.luce_y || 0.42) - R), width: 2 * R, height: 2 * R });
  }
  const fig = el('div', 'an-fig', cam);
  px(fig, { left: d.x, top: d.y, width: d.w, height: d.h });
  const im = el('img', '', fig);
  im.src = d.src;
  px(im, { width: d.w, height: d.h });
  const S = svg('svg', { viewBox: `${d.vx || 0} ${d.vy || 0} ${d.vw} ${d.vh}`, width: d.w, height: d.h, class: 'an-svg' }, fig);
  const defs = svg('defs', {}, S);
  const blur = svg('filter', { id: 'an-sf', x: '-60%', y: '-60%', width: '220%', height: '220%' }, defs);
  svg('feGaussianBlur', { stdDeviation: 14 / d.scala }, blur);
  const k = 1 / d.scala;            // 1 px a schermo, in coordinate del disegno
  tl.fromTo(fig, { opacity: 0, y: 40, filter: 'blur(6px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: ENTRA_GRANDE, ease: 'expo.out' }, tf);
  if (luce) {
    gsap.set(luce, { opacity: 0 });
    tl.to(luce, { opacity: 1, duration: ENTRA_GRANDE, ease: 'power2.out' }, tf);
    tl.to(luce, { opacity: 0, duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
  }
  tl.to(fig, { opacity: 0, y: -16, duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
  if (d.camera_scena && d.camera_scena.length) {
    gsap.set(cam, { transformOrigin: '0px 0px' });
    d.camera_scena.forEach((m) => {
      tl.to(cam, { scale: m.scala || 1, x: m.x || 0, y: m.y || 0, duration: m.dur || 0.8, ease: m.ease || 'power2.inOut' }, m.t);
    });
  }
  const fine = (g) => (g.e !== undefined ? g.e : null);
  const spegni = (n, g) => { if (fine(g) !== null) tl.to(n, { opacity: 0, duration: ESCE, ease: 'power2.in' }, g.e - ESCE); };
  (d.segni || []).forEach((g) => {
    if (g.tipo === 'alone') {
      const gr = svg('g', { transform: `rotate(${g.ang || 0} ${g.cx} ${g.cy})` }, S);
      const e = svg('ellipse', { cx: g.cx, cy: g.cy, rx: g.rx, ry: g.ry, fill: g.colore || verde, filter: 'url(#an-sf)' }, gr);
      gsap.set(e, { opacity: 0, transformOrigin: `${g.cx}px ${g.cy}px` });
      tl.fromTo(e, { opacity: 0, scale: 0.7 }, { opacity: g.q || 0.55, scale: 1, duration: 12 * FR, ease: 'expo.out', immediateRender: false }, g.t);
      (g.pulsa || []).forEach((q) => { const tp = q.t;
        tl.to(e, { opacity: Math.min(0.9, (g.q || 0.55) + 0.3), scale: 1.08, duration: 8 * FR, ease: 'sine.inOut' }, tp);
        tl.to(e, { opacity: g.q || 0.55, scale: 1, duration: 10 * FR, ease: 'sine.inOut' }, tp + 8 * FR);
      });
      if (g.accorcia) tl.to(e, { attr: { ry: g.ry * g.accorcia.k }, duration: g.accorcia.dur || 0.8, ease: 'power2.inOut' }, g.accorcia.t);
      spegni(e, g);
    } else if (g.tipo === 'asse') {
      // asse del bacino: linea che ruota attorno al centro; `neutro` = tratteggiata ferma
      const gr = svg('g', { transform: `translate(${g.cx} ${g.cy})` }, S);
      const ln = svg('line', { x1: -g.L, y1: 0, x2: g.L, y2: 0, stroke: g.neutro ? 'rgba(244,244,244,0.55)' : verde,
        'stroke-width': (g.neutro ? 4 : 7) * k, 'stroke-linecap': 'round' }, gr);
      if (g.neutro) ln.setAttribute('stroke-dasharray', `${12 * k} ${10 * k}`);
      gsap.set(ln, { opacity: 0, rotation: 0, svgOrigin: '0 0' });
      tl.fromTo(ln, { opacity: 0 }, { opacity: 1, duration: 8 * FR, immediateRender: false }, g.t);
      if (g.ang) tl.fromTo(ln, { rotation: g.da || 0 }, { rotation: g.ang, duration: g.dur || 1.2, ease: 'power2.inOut', svgOrigin: '0 0', immediateRender: false }, g.t_ruota !== undefined ? g.t_ruota : g.t + 8 * FR);
      spegni(ln, g);
    } else if (g.tipo === 'freccia') {
      const gr = svg('g', {}, S);
      const ang = Math.atan2(g.y1 - g.y0, g.x1 - g.x0), h = 30 * k;
      const p = svg('path', { d: `M${g.x0} ${g.y0} L${g.x1} ${g.y1} M${g.x1 + h * Math.cos(ang + 2.5)} ${g.y1 + h * Math.sin(ang + 2.5)} L${g.x1} ${g.y1} L${g.x1 + h * Math.cos(ang - 2.5)} ${g.y1 + h * Math.sin(ang - 2.5)}`,
        fill: 'none', stroke: g.colore || verde, 'stroke-width': 9 * k, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', pathLength: 1, 'stroke-dasharray': '1 1' }, gr);
      gsap.set(p, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(p, { attr: { 'stroke-dashoffset': 0 }, duration: 12 * FR, ease: 'power2.out' }, g.t);
      if (g.accorcia) {
        const mx = g.x0 + (g.x1 - g.x0) * g.accorcia.k, my = g.y0 + (g.y1 - g.y0) * g.accorcia.k;
        tl.to(gr, { x: mx - g.x1, y: my - g.y1, duration: g.accorcia.dur || 0.6, ease: 'power2.inOut' }, g.accorcia.t);
      }
      spegni(p, g);
    } else if (g.tipo === 'numero') {
      const gr = svg('g', { transform: `translate(${g.x} ${g.y})` }, S);
      const inner = svg('g', {}, gr);
      svg('circle', { r: 30 * k, fill: verde }, inner);
      const tx = svg('text', { 'text-anchor': 'middle', 'dominant-baseline': 'central', 'font-size': 40 * k, 'font-weight': 800, fill: '#002551' }, inner);
      tx.textContent = g.n;
      gsap.set(inner, { scale: 0, svgOrigin: '0 0' });
      tl.to(inner, { scale: 1, duration: ENTRA, ease: RIMBALZO }, g.t);
      spegni(inner, g);
    } else if (g.tipo === 'arco') {
      const a0 = g.a0 * Math.PI / 180, a1 = g.a1 * Math.PI / 180;
      const p = svg('path', { d: `M${g.cx + g.r * Math.cos(a0)} ${g.cy + g.r * Math.sin(a0)} A${g.r} ${g.r} 0 0 ${a1 > a0 ? 1 : 0} ${g.cx + g.r * Math.cos(a1)} ${g.cy + g.r * Math.sin(a1)}`,
        fill: 'none', stroke: verde, 'stroke-width': 6 * k, 'stroke-linecap': 'round', pathLength: 1, 'stroke-dasharray': '1 1' }, S);
      gsap.set(p, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(p, { attr: { 'stroke-dashoffset': 0 }, duration: 14 * FR, ease: 'power2.out' }, g.t);
      spegni(p, g);
    } else if (g.tipo === 'linea') {
      // linea che si disegna (da), poi passa per frame alla forma `a` (es. si spezza)
      const pl = svg('polyline', { points: g.da.map((q) => q.join(',')).join(' '), fill: 'none', stroke: g.colore || panna,
        'stroke-width': (g.spessore || 5) * k, 'stroke-linecap': 'round', 'stroke-linejoin': 'round', pathLength: 1, 'stroke-dasharray': '1 1' }, S);
      gsap.set(pl, { attr: { 'stroke-dashoffset': 1 } });
      tl.to(pl, { attr: { 'stroke-dashoffset': 0 }, duration: 14 * FR, ease: 'power2.out' }, g.t);
      if (g.a) {
        const n = Math.max(2, Math.round((g.dur || 0.8) * FPS));
        for (let f = 0; f <= n; f++) {
          const u = f / n, e = u < 0.5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2;
          const pts = g.da.map((q, i) => [q[0] + (g.a[i][0] - q[0]) * e, q[1] + (g.a[i][1] - q[1]) * e]);
          tl.set(pl, { attr: { points: pts.map((q) => q.join(',')).join(' '), stroke: e > 0.5 ? verde : (g.colore || panna) } }, g.t_spezza + f * FR);
        }
      }
      spegni(pl, g);
    } else if (g.tipo === 'contorno') {
      const e = svg('ellipse', { cx: g.cx, cy: g.cy, rx: g.rx, ry: g.ry, fill: 'none', stroke: panna, 'stroke-width': 4 * k,
        'stroke-dasharray': `${12 * k} ${10 * k}` }, S);
      gsap.set(e, { opacity: 0 });
      tl.to(e, { opacity: 0.9, duration: 10 * FR }, g.t);
      spegni(e, g);
    }
  });
  (d.etichette || []).forEach((t) => {
    if (t.parole) {
      // parola per parola sulla voce (famiglia «frase parola per parola»)
      const f = el('div', 'an-et an-par', box);
      px(f, { left: t.x, top: t.y, width: t.larghezza || 800, whiteSpace: 'normal' });
      f.style.fontSize = (t.corpo || 60) + 'px';
      f.style.fontWeight = t.peso || 700;
      t.parole.forEach((p) => {
        if (p.a_capo) el('br', '', f);
        const w = el('span', 'an-w' + (p.chiave ? ' an-k' : ''), f, esc(p.testo));
        gsap.set(w, { opacity: 0, filter: 'blur(10px)', y: 8 });
        // una parola gia detta prima della scena entra con la scena, non prima (fase 7b:
        // «la parte bassa» compariva sopra di lui 2 frame prima del taglio sulla scena scura)
        const tw = Math.max(p.t, tf, x.s);
        tl.to(w, { opacity: 0.35, duration: FR }, Math.max(0, x.s, tw - FR));
        tl.to(w, { opacity: 1, filter: 'blur(0px)', y: 0, duration: 3 * FR + 0.04, ease: 'power2.out' }, tw);
        f.appendChild(document.createTextNode(' '));
      });
      tl.to(f, { opacity: 0, filter: 'blur(6px)', duration: ESCE, ease: 'power2.in' }, (t.e !== undefined ? t.e : x.e) - ESCE);
      return;
    }
    const r = el('div', 'an-et', box);
    px(r, { left: t.x, top: t.y });
    if (t.larghezza) px(r, { width: t.larghezza, whiteSpace: 'normal' });
    r.style.fontSize = (t.corpo || 56) + 'px';
    r.style.fontWeight = t.peso || 700;
    r.style.color = t.colore === 'verde' ? verde : panna;
    const s = el('span', '', r, esc(t.testo));
    maschera(s);
    gsap.set(s, { yPercent: 135 });
    rivela(s, t.t, { dur: 10 * FR });
    nascondi(s, (t.e !== undefined ? t.e : x.e) - ESCE, { dir: 'su' });
  });
  if (d.attribuzione) {
    const a = el('div', 'an-attr', box, esc(d.attribuzione));
    if (d.attr_pos) px(a, d.attr_pos);
    else if (d.pannello) {
      // una riga, dentro i margini della card (regola 7b rivista)
      px(a, { left: d.pannello.x + 22, top: d.pannello.y + d.pannello.altezza - 40, fontSize: d.attr_corpo || 19 });
    }
    tl.fromTo(a, { opacity: 0 }, { opacity: 0.92, duration: 8 * FR }, tf);   // tappa 3: con la figura, leggibile
    tl.to(a, { opacity: 0, duration: ESCE }, x.e - ESCE);
  }
};

// texture delle scene scure: curve di livello panna al 4-6% (deterministiche) e grana fine
function trama(p, W, H, q) {
  const S = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, class: 'an-trama' }, p);
  const cx = W * 0.62, cy = H * 0.46;
  for (let k = 1; k <= 16; k++) {
    const r = 60 + k * 70;
    let dd = '';
    for (let i = 0; i <= 120; i++) {
      const a = i / 120 * Math.PI * 2;
      const w = 1 + 0.11 * Math.sin(3 * a + k * 0.7) + 0.07 * Math.sin(5 * a - k * 1.3) + 0.04 * Math.sin(9 * a + k);
      const X = cx + Math.cos(a) * r * 1.35 * w, Y = cy + Math.sin(a) * r * 0.9 * w;
      dd += (i ? 'L' : 'M') + X.toFixed(1) + ' ' + Y.toFixed(1);
    }
    svg('path', { d: dd + 'Z', fill: 'none', stroke: 'rgba(244,244,244,' + (q || 0.05) + ')', 'stroke-width': 1.6 }, S);
  }
  el('div', 'an-grana', p);
}

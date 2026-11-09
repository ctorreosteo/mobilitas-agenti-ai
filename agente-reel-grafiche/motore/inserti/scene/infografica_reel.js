// Infografiche vere per i reel 9:16 (agente reel-grafiche, fase 6, giro 4, 05/11/2026). Modello nuovo, IN PROVA.
// Regola di Riccardo (05/11/2026): «una parola o una frase da sola, anche grande e animata, NON è una grafica: ogni grafica
// deve MOSTRARE il concetto con un contenuto visivo (icona o illustrazione che si anima, diagramma, collegamento fra
// elementi, contatore, piccola scena con più elementi, disegno Servier, card con icona). Il testo è solo un'etichetta».
// Il modello è un piccolo motore di scene: il piano mette i pezzi (dischi con icona, pittogramma Mobilitas che si
// compone, linee che collegano con impulsi di luce, arco che si riempie, punti che arrivano, card, disegni Servier) e
// le etichette dette; la camera si sposta fra le parti della scena (carrello, gadzhi-07 e gadzhi-12).
// Reference: gadzhi-14 (icone lineari che si disegnano), gadzhi-11 e gadzhi-21 (connettore, albero «una cosa → tre»),
// gadzhi-05 (anello che si riempie), gadzhi-07 (nodo luminoso che percorre la linea, camera che segue), gadzhi-22 e
// martell-03 (tante persone come punti, mai figure umane), gadzhi-09 e gadzhi-15 (accensione con il colpo).
// Fondo pieno (blu del brand con la griglia di punti) a taglio all'entrata e all'uscita; alfa 0 fuori dal rettangolo.
// Icone: Tabler 3.49.0 (MIT, motore/inserti/icone/; «tabler:<nome>») o il pittogramma; mai figure umane, mai spunte,
// mai organi disegnati da noi (l'anatomia solo da disegni Servier, «servier»). Niente decifrazioni, niente cifre provvisorie.
// d: modo "finestra" (rett {x,y,w,h,r} o [{da,...}]) | "tutto"; griglia (default true); camera [{t, dur, x, y, scala}]
//    (sposta la scena: x, y in px, scala attorno al centro del rettangolo); pezzi [...], in ordine di disegno:
//    disco      {x, y (centro), lato, icona "tabler:..." | "pittogramma", servier {nome, alto, modo}, t, via, colpo [t],
//                acceso t (si riempie di verde, l'icona diventa blu notte), spento t (si abbassa), tremola {da, a} (la
//                fiamma che non se ne va), pieno (disco verde dall'inizio)}
//    pittogramma {x, y, lato, t, via, colpo [t]}: il pittogramma Mobilitas che si compone (disco, barra, segno), mai ricolorato
//    anello     {x, y, lato, icona "tabler:rosette", t, via}: un contorno grande che si disegna attorno a un pezzo (badge)
//    etichetta  {testo, x, y, corpo, t, via, verde, allinea "centro"|"sx"|"dx", cambia [{t, testo}]}
//    linea      {da [x,y], a [x,y], t, fr (fotogrammi per disegnarsi, 8), curva (px), punta, impulsi [t], accesa t, via, debole}
//    arco       {x, y, r, t, t0, t1 (si riempie da t0 a t1), lancetta, spessore, via}
//    punti      {area [x,y,w,h], n, seme, t, fr (comparsa), verso [x,y], t_verso, fr_verso}
//    scheda     {x, y, w, h, t, via, acceso t, raggio}
//    (giro 5) etichetta.pad: margine della pillola in corpi (0,42 di default); d.attribuzione (testo), attr_x, attr_y: l'attribuzione
//    Servier (CC BY, obbligo di licenza, classe reel-attr) per tutta la grafica, quando c'è un disegno Servier
//    (07/11/2026) d.modo "palco": lo stile fisso del reel in PIÙ FORME (fascia alta, pannello basso, tutto schermo, badge), in
//    d.stati [{da, forma, x, y, w, h, r, ombra, filo, entra «taglio»|«seme»|«tendina»}]; il video sotto non si tocca.
//    Pezzi nuovi: indicatore {x, y, n, w, h, gap, stati [{t, attivo}]} (trattini, verticale-11), barra {x, y, w, h, t, t0, t1,
//    fino, spento} (barre a confronto, verticale-10); etichetta: *parola chiave* in gradiente verde→azzurro, colore;
//    nasce_da [x, y, scala] su disco, scheda, immagine, logo (l'oggetto nasce da quello prima: trasformazione, non comparsa)
MODELLI.infografica_reel = function (box, x, d) {
  const QW = 1080, QH = 1920, EPS = 0.001;
  const clip = el('div', 'inf-clip', box);
  const fondo = el('div', 'inf-fondo fondo-sito', clip);
  const dentro = el('div', 'inf-dentro', clip);
  let R0, PAN = null, PAN_FILO = null;
  const SUL_VIDEO = d.modo === 'libero';
  if (d.modo === 'libero') {
    // tappa 2 (06/11/2026): sulla persona in camera, senza pannello (si vede il video), dentro dati.box; con dati.dietro il
    // motore rimette la persona sopra (sagoma di Apple Vision). Le etichette stanno in card blu notte (mai verde sul video nudo)
    const B = d.box || { x: 0, y: 0, w: QW, h: QH };
    R0 = { x: B.x, y: B.y, w: B.w, h: B.h, r: 0 };
    px(clip, { left: B.x, top: B.y, width: B.w, height: B.h }); px(dentro, { left: -B.x, top: -B.y });
    fondo.style.display = 'none';
  } else if (d.modo === 'palco') {
    // 07/11/2026 sera (Riccardo): stile fisso, PIÙ FORME. La forma (fondo del sito, puntini, filo verde) passa per d.stati
    // [{da, forma, x, y, w, h, r, ombra «alto»|«basso»|«no», filo «sopra»|«sotto», entra «taglio»|«seme»|«tendina», fr, lato}];
    // il video sotto resta fermo (i sottotitoli non si toccano: o la fascia è libera, o una forma piena la copre tutta)
    R0 = { x: 0, y: 0, w: QW, h: QH, r: 0 };
    px(clip, { left: 0, top: 0, width: QW, height: QH });
    clip.style.overflow = 'visible';
    fondo.style.display = 'none';
    PAN = el('div', 'inf-palco fondo-sito', clip);
    el('div', 'inf-palco-punti', PAN);
    clip.insertBefore(PAN, dentro);
    px(dentro, { left: 0, top: 0 });
    PAN_FILO = el('div', 'inf-palco-filo', clip);
  } else if (d.modo === 'tutto') {
    R0 = { x: 0, y: 0, w: QW, h: QH, r: 0 };
    px(clip, { left: 0, top: 0, width: QW, height: QH }); px(fondo, { width: QW, height: QH }); px(dentro, { left: 0, top: 0 });
    if (d.foro) {
      // tappa 2: «lui nel cerchio» (gadzhi-09): un foro tondo nel fondo; sotto il motore mette il video rimpicciolito (dati.pip)
      const [c0, c1] = d.foro.c, r = d.foro.r;
      const m = `radial-gradient(circle ${r}px at ${c0}px ${c1}px, transparent ${r - 0.5}px, #000 ${r + 0.5}px)`;
      clip.style.webkitMaskImage = m; clip.style.maskImage = m;
    }
  } else {
    const RR = Array.isArray(d.rett) ? d.rett : [Object.assign({ da: 0 }, d.rett)];
    const metti = (R, t) => {
      const a = { left: R.x + 'px', top: R.y + 'px', width: R.w + 'px', height: R.h + 'px', borderRadius: R.r + 'px' };
      const f = { width: R.w + 'px', height: R.h + 'px' }, dd = { left: -R.x + 'px', top: -R.y + 'px' };
      if (t === undefined) { gsap.set(clip, a); gsap.set(fondo, f); gsap.set(dentro, dd); }
      else { tl.set(clip, a, t - EPS); tl.set(fondo, f, t - EPS); tl.set(dentro, dd, t - EPS); }
    };
    metti(RR[0]);
    RR.slice(1).forEach((R) => metti(R, R.da));      // sul taglio d'inquadratura la finestra cambia di 1-5 px
    R0 = RR[0];
  }
  gsap.set(clip, { opacity: 0 });
  if (d.attribuzione) {
    const a = el('div', 'reel-attr inf-attr', dentro, esc(d.attribuzione));
    px(a, { left: d.attr_x || 70, top: d.attr_y || 893 });
    // 07/11/2026 sera: la firma segue la forma del momento (attr_pos [[t, x, y], ...])
    (d.attr_pos || []).forEach(([tp, xx, yy]) => { if (tp <= x.s + EPS) px(a, { left: xx, top: yy }); else tl.set(a, { left: xx, top: yy }, tp - EPS); });
    // 07/11/2026 (direttore): l'attribuzione Servier solo quando c'è un disegno Servier a schermo (attr_vis [[t0, t1], ...])
    if (d.attr_vis) {
      gsap.set(a, { opacity: d.attr_vis.some(([a0]) => a0 <= x.s + EPS) ? 0.92 : 0 });
      d.attr_vis.forEach(([a0, a1]) => { if (a0 > x.s + EPS) tl.set(a, { opacity: 0.92 }, a0); if (a1 !== undefined && a1 < x.e) tl.set(a, { opacity: 0 }, a1); });
    }
  }
  tl.set(clip, { opacity: 1 }, x.s);                // entra a taglio con il fondo e i primi pezzi già pieni
  tl.set(clip, { opacity: 0 }, x.e - EPS);          // esce a taglio sull'ultimo fotogramma
  const intero = (t) => t === undefined || t <= x.s + EPS;
  if (PAN && d.stati) {
    const OMBRA = { alto: 'inset 0 -2px 0 rgba(141,255,169,0.35), 0 12px 0 rgba(0,14,36,0.55), 0 22px 40px rgba(0,8,22,0.6)',
      // il pannello basso sta sopra i sottotitoli: l'ombra va solo in su (finisce entro 8 px sotto il bordo)
      basso: 'inset 0 2px 0 rgba(141,255,169,0.35), 0 -16px 24px rgba(0,8,22,0.55)', no: 'none' };
    const geo = (q) => ({ left: q.x, top: q.y, width: q.w, height: q.h, borderRadius: q.r === undefined ? 40 : q.r, boxShadow: OMBRA[q.ombra || 'alto'] });
    const filo = (q) => q.filo === 'sopra' ? { left: q.x + 60, top: q.y - 1, width: q.w - 120, height: 3, opacity: 1 }
      : q.filo === 'sotto' ? { left: q.x + 60, top: q.y + q.h - 2, width: q.w - 120, height: 3, opacity: 1 } : { opacity: 0 };
    const ease = (u) => 0.5 - 0.5 * Math.cos(Math.PI * Math.min(1, Math.max(0, u)));
    d.stati.forEach((q, i) => {
      const t = q.da || 0, n = q.fr || 7;
      const metti = (props, ff, tt) => { if (tt <= x.s + EPS) { gsap.set(PAN, props); gsap.set(PAN_FILO, ff); } else { tl.set(PAN, props, tt - EPS); tl.set(PAN_FILO, ff, tt - EPS); } };
      if (i === 0 || !q.entra || q.entra === 'taglio') { metti(geo(q), filo(q), t); return; }
      if (q.entra === 'seme') {
        // cresce dal suo bordo (lato «basso»: dal bordo in basso verso l'alto) in n fotogrammi, già con lo stile finale
        const g = geo(q), h0 = 6, y0 = q.lato === 'basso' ? q.y + q.h - h0 : q.y;
        metti(Object.assign({}, g, { top: y0, height: h0 }), Object.assign(filo(q), { opacity: 0 }), t);
        tl.to(PAN, { top: q.y, height: q.h, duration: n * FR, ease: 'power3.out' }, t);
        tl.set(PAN_FILO, filo(q), t + n * FR);
        return;
      }
      if (q.entra === 'tendina') {
        // dalla forma di prima a questa, fotogramma per fotogramma; il bordo in basso salta la fascia dei sottotitoli
        // (d.salta [y0, y1]) in un solo fotogramma: mai mezza riga coperta
        const p = d.stati[i - 1];
        for (let k = 1; k <= n; k++) {
          const u = ease(k / n), top = p.y + (q.y - p.y) * u;
          let bot = (p.y + p.h) + ((q.y + q.h) - (p.y + p.h)) * u;
          if (d.salta && k < n && bot > d.salta[0] - 6) bot = d.salta[0] - 6;
          const props = { left: p.x + (q.x - p.x) * u, top, width: p.w + (q.w - p.w) * u, height: bot - top,
            // (render F2) nei fotogrammi di passaggio niente ombra: arrivava sulla fascia dei sottotitoli (alfa 72)
            borderRadius: (p.r === undefined ? 40 : p.r) + ((q.r === undefined ? 40 : q.r) - (p.r === undefined ? 40 : p.r)) * u, boxShadow: OMBRA[k < n ? 'no' : (q.ombra || 'alto')] };
          metti(props, k < n ? { opacity: 0 } : filo(q), t + (k - 1) * FR);
        }
      }
    });
  }

  // griglia di punti con l'alone (come parole_ads), ferma: la sposta solo la camera
  const cam = el('div', 'inf-cam', dentro);
  const cxR = R0.x + R0.w / 2, cyR = R0.y + R0.h / 2;
  gsap.set(cam, { transformOrigin: `${cxR}px ${cyR}px` });
  if (d.griglia !== false && d.modo !== 'libero' && d.modo !== 'palco') {
    const m = 400, g = el('canvas', 'inf-griglia', cam);
    const gw = R0.w + 2 * m, gh = R0.h + 2 * m;
    g.width = gw; g.height = gh;
    px(g, { left: R0.x - m, top: R0.y - m, width: gw, height: gh });
    const c = g.getContext('2d'), passo = 34;
    for (let yy = passo / 2; yy < gh; yy += passo) {
      for (let xx = passo / 2; xx < gw; xx += passo) {
        const dx = (xx - gw / 2) / (R0.w * 0.7), dy = (yy - gh / 2) / (R0.h * 0.7);
        const v = Math.max(0, 1 - Math.sqrt(dx * dx + dy * dy));
        if (v <= 0.03) continue;
        c.fillStyle = `rgba(114,250,147,${0.04 + 0.12 * v})`;
        c.beginPath(); c.arc(xx, yy, 1.5 + 1.4 * v, 0, 6.2832); c.fill();
      }
    }
  }
  if (d.modo !== 'libero' && d.modo !== 'palco') el('div', 'inf-alone', cam);
  if (d.camera0) gsap.set(cam, { x: d.camera0.x || 0, y: d.camera0.y || 0, scale: d.camera0.scala || 1 });
  (d.camera || []).forEach((k) => {
    tl.to(cam, { x: k.x || 0, y: k.y || 0, scale: k.scala || 1, duration: (k.dur || 0.6), ease: k.ease || 'power2.inOut' }, k.t);
  });

  // il livello delle linee e degli archi (sotto i dischi)
  const S = svg('svg', { viewBox: `0 0 ${QW} ${QH}`, width: QW, height: QH }, cam);
  S.setAttribute('class', 'inf-svg');
  const sopra = el('div', 'inf-sopra', cam);
  // giro 5: un secondo livello di linee SOPRA i pezzi (frecce su un disegno Servier: linea.sopra)
  const S2 = svg('svg', { viewBox: `0 0 ${QW} ${QH}`, width: QW, height: QH }, cam);
  S2.setAttribute('class', 'inf-svg');

  const esce = (e, t) => {
    if (t === undefined) return;
    tl.to(e, { opacity: 0, scale: 0.9, duration: 3 * FR, ease: 'power2.in' }, t - 3 * FR);
    tl.set(e, { display: 'none' }, t);
  };
  const nasce = (e, t, o) => {
    o = o || {};
    if (intero(t)) return;
    gsap.set(e, { opacity: 0 });
    tl.set(e, { opacity: 1 }, t);
    tl.fromTo(e, { scale: o.da || 0.6, x: o.dx || 0, y: o.dy || 0 }, { scale: 1, x: 0, y: 0, duration: (o.fr || 5) * FR, ease: o.ease || 'back.out(1.7)',
      immediateRender: false }, t);
  };
  // 07/11/2026: l'oggetto nasce da quello prima (trasformazione): parte dal punto nasce_da [x, y, scala], piccolo, e va al suo posto
  const da_dove = (p, cx, cy, o) => {
    o = o || {};
    if (!p.nasce_da) return o;
    return Object.assign(o, { dx: p.nasce_da[0] - cx, dy: p.nasce_da[1] - cy, da: p.nasce_da[2] || 0.35, fr: 9, ease: 'power3.out' });
  };
  const colpo = (e, t) => {
    tl.to(e, { scale: 1.14, duration: 3 * FR, ease: 'power2.out' }, t);
    tl.to(e, { scale: 1, duration: 6 * FR, ease: 'power2.inOut' }, t + 3 * FR);
    // giro 4, direttore: niente lampo di luminosità (sul blu notte faceva un disco azzurro): un alone verde che si posa
    tl.fromTo(e, { filter: 'drop-shadow(0 0 26px rgba(141,255,169,1))' }, { filter: 'drop-shadow(0 0 0px rgba(141,255,169,0))', duration: 10 * FR,
      ease: 'power2.out', immediateRender: false }, t);
  };
  // un'icona Tabler che si disegna con il tratto (gadzhi-14); intera se t è sull'entrata
  const icona = (nome, dove, lato, t, colore, tratto) => {
    const s = svg('svg', { viewBox: '0 0 24 24', width: lato, height: lato }, dove);
    s.setAttribute('class', 'inf-ic');
    const n = String(nome).replace(/^tabler:/, '');
    const pp = (typeof TABLER !== 'undefined' && TABLER[n]) || [];
    pp.forEach((dd, j) => {
      const p = svg('path', { d: dd, fill: 'none', stroke: colore || '#8DFFA9', 'stroke-width': tratto || 1.9, 'stroke-linecap': 'round',
        'stroke-linejoin': 'round', pathLength: 1 }, s);
      p.setAttribute('stroke-dasharray', '1 1');
      if (intero(t)) return;
      // nascosto finché non parte (il tondo della punta del tratto lascerebbe un puntino)
      // giro 4, direttore: mai un disco vuoto al primo fotogramma: il tratto parte già a metà e si chiude in 7 fotogrammi
      gsap.set(p, { attr: { 'stroke-dashoffset': 0.5 }, opacity: 0 });
      tl.set(p, { opacity: 1 }, t);
      tl.to(p, { attr: { 'stroke-dashoffset': 0 }, duration: 7 * FR, ease: 'power2.out' }, t);
    });
    return s;
  };
  // il pittogramma Mobilitas che si compone: disco, barra dal centro, segno dall'alto (livelli separati dallo stesso file)
  const pittogramma = (dove, lato, t) => {
    const w = el('div', 'inf-pitto', dove);
    px(w, { width: lato * 2.75, height: lato * 2.75, left: -lato * 0.875, top: -lato * 0.875 });  // il disco è 0,364 del file
    const a = el('img', 'inf-pitto-l', w); a.src = 'assets/pittogramma-disco.png';
    const b = el('img', 'inf-pitto-l', w); b.src = 'assets/pittogramma-segno.png';
    if (!intero(t)) {
      gsap.set(b, { clipPath: 'inset(39.5% 50% 60.5% 50%)' });
      tl.to(b, { clipPath: 'inset(39.5% 41.5% 57.5% 41.5%)', duration: 4 * FR, ease: 'power3.out' }, t + 2 * FR);
      tl.to(b, { clipPath: 'inset(39.5% 41.5% 37.5% 41.5%)', duration: 7 * FR, ease: 'power2.inOut' }, t + 6 * FR);
      tl.set(b, { clipPath: 'none' }, t + 13 * FR);
    }
    return w;
  };

  // muovi [{t, dx, dy, scala, dur}]: un pezzo che si sposta nella scena (spostamenti relativi alla sua posizione)
  const muovi = (e, p) => (p.muovi || []).forEach((m) => tl.to(e, { x: m.dx || 0, y: m.dy || 0, scale: m.scala || 1,
    duration: m.dur || 0.5, ease: m.ease || 'power2.inOut' }, m.t));
  if (d.foro) {
    const sa = svg('svg', { viewBox: `0 0 ${QW} ${QH}`, width: QW, height: QH }, box);
    sa.setAttribute('class', 'inf-svg inf-foro');
    const [c0, c1] = d.foro.c, r = d.foro.r;
    svg('circle', { cx: c0, cy: c1, r: r + 6, fill: 'none', stroke: '#72FA93', 'stroke-width': 10 }, sa).setAttribute('class', 'inf-linea');
    gsap.set(sa, { opacity: 0 }); tl.set(sa, { opacity: 1 }, x.s); tl.set(sa, { opacity: 0 }, x.e - EPS);
  }
  (d.pezzi || []).forEach((p) => {
    const T0 = p.t === undefined ? x.s : p.t;
    if (p.tipo === 'disco' || p.tipo === 'pittogramma') {
      const L = p.lato || 160;
      const w = el('div', 'inf-disco' + (p.tipo === 'pittogramma' ? ' inf-disco-p' : '') + (p.pieno ? ' inf-acceso' : ''), sopra);
      px(w, { left: p.x - L / 2, top: p.y - L / 2, width: L, height: L, borderRadius: L / 2 });
      let ic = null;
      if (p.tipo === 'pittogramma' || p.icona === 'pittogramma') {
        // il pittogramma è un disco già suo: niente disco nostro sotto (mai ricolorato)
        w.classList.add('inf-disco-p');
        const inner = el('div', 'inf-pitto-box', w);
        px(inner, { left: 0, top: 0, width: L, height: L });
        pittogramma(inner, L, T0);
      } else if (p.servier && p.src) {
        const im = el('img', 'inf-servier', w); im.src = p.src;
        const s = Math.min(L * 0.74 / p.img_w, L * 0.74 / p.img_h);
        px(im, { width: p.img_w * s, height: p.img_h * s, left: (L - p.img_w * s) / 2, top: (L - p.img_h * s) / 2 });
      } else if (p.icona) {
        const li = L * (p.scala_icona || 0.66);
        // giro 4: con «prima» (segnaposto) l'icona c'è già, spenta insieme al disco, e si accende sulla parola
        ic = icona(p.icona, w, li, p.prima !== undefined ? p.prima : T0, p.pieno ? '#001A3D' : null, p.tratto);
        px(ic, { left: (L - li) / 2, top: (L - li) / 2 });
        if (p.specchio) gsap.set(ic, { scaleX: -1 });   // giro 5: l'icona specchiata (la barra di divieto la attraversa)
      }
      // giro 5 (direttore): sul video un disco spento resta opaco (un velo blu notte sopra l'icona), mai trasparente
      const velo = SUL_VIDEO ? el('div', 'inf-velo', w) : null;
      if (velo) gsap.set(velo, { opacity: 0 });
      if (p.prima !== undefined && velo) {
        gsap.set(w, { opacity: intero(p.prima) ? 1 : 0 });
        gsap.set(velo, { opacity: 1 });
        if (!intero(p.prima)) tl.set(w, { opacity: 1 }, p.prima);
        tl.set(velo, { opacity: 0 }, T0);
        tl.fromTo(w, { scale: 0.86 }, { scale: 1, duration: 5 * FR, ease: 'back.out(1.7)', immediateRender: false }, T0);
      } else if (p.prima !== undefined) {
        // giro 4, direttore: il posto c'è già (disco spento, senza icona) e si accende sulla sua parola: mai la finestra vuota
        gsap.set(w, { opacity: intero(p.prima) ? 0.3 : 0 });
        if (!intero(p.prima)) tl.set(w, { opacity: 0.3 }, p.prima);
        tl.set(w, { opacity: 1 }, T0);
        tl.fromTo(w, { scale: 0.86 }, { scale: 1, duration: 5 * FR, ease: 'back.out(1.7)', immediateRender: false }, T0);
      } else nasce(w, T0, da_dove(p, p.x, p.y));
      if (p.cala !== undefined) {
        if (velo) tl.to(velo, { opacity: 0.55, duration: 4 * FR, ease: 'power2.out' }, p.cala);
        else tl.to(w, { opacity: 0.55, duration: 4 * FR, ease: 'power2.out' }, p.cala);
      }
      if (p.tremola && ic) {
        // la fiamma che non se ne va: piccole oscillazioni seminate (mai ferme), dal basso
        gsap.set(ic, { transformOrigin: '50% 85%' });
        const rnd = semi(p.seme || 7), a = p.tremola.da === undefined ? x.s : p.tremola.da, b = p.tremola.a === undefined ? x.e : p.tremola.a;
        for (let t = a; t < b - 2 * FR; t += 4 * FR) {
          tl.to(ic, { scaleY: 1 + 0.09 * rnd(), scaleX: 1 - 0.05 * rnd(), rotation: (rnd() - 0.5) * 7, duration: 4 * FR, ease: 'sine.inOut' }, t);
        }
      }
      if (p.acceso !== undefined) {
        // si accende: un disco verde pieno sotto l'icona (livello già nel DOM, solo opacità: si può saltare a ogni fotogramma)
        const luce = el('div', 'inf-luce', w);
        w.insertBefore(luce, w.firstChild);
        gsap.set(luce, { opacity: 0 });
        tl.set(luce, { opacity: 1 }, p.acceso);
        if (ic) tl.set(ic.querySelectorAll('path'), { attr: { stroke: '#001A3D' } }, p.acceso);
        colpo(w, p.acceso);
      }
      if (p.spento !== undefined) {
        if (velo) tl.to(velo, { opacity: 0.72, duration: 6 * FR, ease: 'power2.out' }, p.spento);
        else tl.to(w, { opacity: 0.4, filter: 'saturate(0.3)', duration: 6 * FR, ease: 'power2.out' }, p.spento);
      }
      if (p.barra !== undefined) {
        // tappa 2: il segno di divieto sull'oggetto (barra panna diagonale che attraversa il disco, gadzhi-08)
        const bs = svg('svg', { viewBox: `0 0 ${L} ${L}`, width: L, height: L }, w);
        bs.setAttribute('class', 'inf-barra');
        const q = svg('line', { x1: L * 0.16, y1: L * 0.84, x2: L * 0.84, y2: L * 0.16, stroke: '#F4F4F4', 'stroke-width': Math.max(8, L * 0.07),
          'stroke-linecap': 'round', pathLength: 1 }, bs);
        q.setAttribute('stroke-dasharray', '1 1');
        if (intero(p.barra)) gsap.set(q, { attr: { 'stroke-dashoffset': 0 } });
        else { gsap.set(q, { attr: { 'stroke-dashoffset': 1 }, opacity: 0 }); tl.set(q, { opacity: 1 }, p.barra);
          tl.to(q, { attr: { 'stroke-dashoffset': 0 }, duration: 4 * FR, ease: 'power2.out' }, p.barra); }
      }
      (p.colpo || []).forEach((t) => colpo(w, t));
      if (p.muovi) { const mv = el('div', 'inf-mv', sopra); sopra.insertBefore(mv, w); mv.appendChild(w); gsap.set(mv, { transformOrigin: `${p.x}px ${p.y}px` }); muovi(mv, p); }
      esce(w, p.via);
    } else if (p.tipo === 'anello') {
      const L = p.lato || 300;
      const s = svg('svg', { viewBox: '0 0 24 24', width: L, height: L }, sopra);
      s.setAttribute('class', 'inf-anello');
      px(s, { left: p.x - L / 2, top: p.y - L / 2 });
      const n = String(p.icona || 'tabler:rosette').replace(/^tabler:/, '');
      ((typeof TABLER !== 'undefined' && TABLER[n]) || []).forEach((dd) => {
        const q = svg('path', { d: dd, fill: 'none', stroke: '#8DFFA9', 'stroke-width': p.spessore || 0.7, 'stroke-linecap': 'round',
          'stroke-linejoin': 'round', pathLength: 1 }, s);
        q.setAttribute('stroke-dasharray', '1 1');
        if (intero(T0)) return;
        gsap.set(q, { attr: { 'stroke-dashoffset': 1 }, opacity: 0 });
        tl.set(q, { opacity: 1 }, T0);
        tl.to(q, { attr: { 'stroke-dashoffset': 0 }, duration: (p.fr || 12) * FR, ease: 'power2.inOut' }, T0);
      });
      if (p.ruota) tl.fromTo(s, { rotation: 0 }, { rotation: p.ruota, duration: x.e - T0, ease: 'none', immediateRender: false }, T0);
      (p.colpo || []).forEach((t) => colpo(s, t));
      esce(s, p.via);
    } else if (p.tipo === 'etichetta') {
      // cambia [{t, testo, verde}]: uno stato per elemento (niente testo riscritto durante il tempo); il vecchio esce in
      // 2 fotogrammi e il nuovo entra subito dopo (mai due stati insieme)
      const stati = [{ t: T0, testo: p.testo, verde: p.verde }].concat(p.cambia || []);
      stati.forEach((st, k) => {
        const cp = p.corpo || 84, lh = Math.round(cp * 1.2);
        const html = esc(st.testo).replace(/\*([^*]+)\*/g, '<span class="inf-chiave">$1</span>');
        const r = el('div', 'inf-et' + (st.verde ? ' inf-et-v' : '') + (p.pillola ? ' inf-pill' : '') + (p.peso ? ' inf-et-' + p.peso : ''), sopra, html);
        px(r, { top: p.y - lh / 2, height: lh, lineHeight: lh + 'px', fontSize: cp });
        if (p.colore) r.style.color = p.colore;
        if (p.spaziatura !== undefined) r.style.letterSpacing = p.spaziatura;
        // giro 5: sul video l'etichetta sta in una pillola blu notte con il filo verde (il verde mai sul video nudo)
        if (p.pillola) px(r, { top: p.y - lh / 2 - Math.round(cp * 0.14), height: lh + Math.round(cp * 0.28), lineHeight: (lh + Math.round(cp * 0.28)) + 'px',
          padding: `0 ${Math.round(cp * (p.pad !== undefined ? p.pad : 0.42))}px`, borderRadius: Math.round(cp * 0.45) });
        const al = p.allinea || 'centro';
        if (al === 'sx') px(r, { left: p.x }); else if (al === 'dx') px(r, { right: QW - p.x });
        else { px(r, { left: p.x }); gsap.set(r, { xPercent: -50 }); }
        if (!intero(st.t)) {
          // entra già piena, con un piccolo assestamento (sul nostro fondo pieno: mai lettere trasparenti sul video)
          gsap.set(r, { opacity: 0 });
          tl.set(r, { opacity: 1 }, st.t);
          tl.fromTo(r, { y: 14, filter: 'blur(5px)' }, { y: 0, filter: 'blur(0px)', duration: 4 * FR, ease: 'power3.out', immediateRender: false }, st.t);
        }
        const dopo = stati[k + 1];
        if (dopo) { tl.to(r, { opacity: 0, duration: 2 * FR, ease: 'power2.in' }, dopo.t - 2 * FR); tl.set(r, { display: 'none' }, dopo.t); }
        else {
          // giro 4, direttore: la parola già detta scende di tono quando arriva la nuova (una cosa per volta la più forte)
          if (p.cala !== undefined && SUL_VIDEO && p.pillola) {
            // giro 5 (direttore): la pillola già detta resta opaca (velo blu notte), le linee non la rigano
            const v = el('div', 'inf-velo inf-velo-pill', r);
            gsap.set(v, { opacity: 0 });
            tl.to(v, { opacity: 0.6, duration: 4 * FR, ease: 'power2.out' }, p.cala);
          } else if (p.cala !== undefined) tl.to(r, { opacity: 0.55, textShadow: '0 0 2px #0B1E3A, 0 4px 14px rgba(0,8,22,0.8)', duration: 4 * FR,
            ease: 'power2.out' }, p.cala);
          esce(r, p.via);
        }
      });
    } else if (p.tipo === 'linea') {
      const [x0, y0] = p.da, [x1, y1] = p.a;
      let pd;
      if (p.curva) {
        const mx = (x0 + x1) / 2, my = (y0 + y1) / 2, L = Math.hypot(x1 - x0, y1 - y0) || 1;
        const nx = -(y1 - y0) / L, ny = (x1 - x0) / L;
        pd = `M${x0} ${y0} Q${mx + nx * p.curva} ${my + ny * p.curva} ${x1} ${y1}`;
      } else pd = `M${x0} ${y0} L${x1} ${y1}`;
      const g = svg('g', {}, p.sopra ? S2 : S);
      if (p.prima !== undefined) {
        // il ramo c'è già, sottile e spento, prima di accendersi (segnaposto)
        const fq = svg('path', { d: pd, fill: 'none', stroke: 'rgba(141,255,169,0.4)', 'stroke-width': 5, 'stroke-linecap': 'round',
          'stroke-dasharray': '8 12' }, g);
        if (!intero(p.prima)) { gsap.set(fq, { opacity: 0 }); tl.set(fq, { opacity: 1 }, p.prima); }
      }
      const q = svg('path', { d: pd, fill: 'none', stroke: p.colore || (p.debole ? 'rgba(141,255,169,0.45)' : '#8DFFA9'), 'stroke-width': p.spessore || 7,
        'stroke-linecap': 'round', pathLength: 1 }, g);
      q.setAttribute('class', 'inf-linea');
      q.setAttribute('stroke-dasharray', '1 1');
      if (!intero(T0)) {
        gsap.set(q, { attr: { 'stroke-dashoffset': 1 }, opacity: 0 });
        tl.set(q, { opacity: 1 }, T0);
        tl.to(q, { attr: { 'stroke-dashoffset': 0 }, duration: (p.fr || 8) * FR, ease: 'power2.inOut' }, T0);
      }
      if (p.punta) {
        const ang = Math.atan2(y1 - y0, x1 - x0), L = p.punta === true ? 30 : p.punta;
        const h = svg('path', { d: `M${x1 - L * Math.cos(ang - 0.55)} ${y1 - L * Math.sin(ang - 0.55)} L${x1} ${y1} L${x1 - L * Math.cos(ang + 0.55)} ${y1 - L * Math.sin(ang + 0.55)}`,
          fill: 'none', stroke: '#8DFFA9', 'stroke-width': p.spessore || 7, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
        h.setAttribute('class', 'inf-linea');
        if (!intero(T0)) { gsap.set(h, { opacity: 0 }); tl.set(h, { opacity: 1 }, T0 + (p.fr || 8) * FR); }
      }
      if (p.accesa !== undefined) {
        tl.to(q, { attr: { stroke: '#B8FFCA', 'stroke-width': (p.spessore || 7) * 1.6 }, duration: 4 * FR, ease: 'power2.out' }, p.accesa);
      }
      // impulsi: un punto di luce che percorre la linea (gadzhi-07), in 8 fotogrammi
      (p.impulsi || []).forEach((t) => {
        // giro 4, direttore: l'impulso si deve vedere sul telefono (≥ 40 px con l'alone)
        const c = svg('circle', { cx: x0, cy: y0, r: Math.max(17, (p.spessore || 7) * 2.4), fill: '#E6FFEC' }, g);
        c.setAttribute('class', 'inf-impulso');
        gsap.set(c, { opacity: 0 });
        const o = { k: 0 };
        tl.set(c, { opacity: 1 }, t);
        tl.to(o, { k: 1, duration: 8 * FR, ease: 'power1.inOut', onUpdate: () => {
          const pt = q.getPointAtLength(o.k * q.getTotalLength());
          c.setAttribute('cx', pt.x); c.setAttribute('cy', pt.y);
        } }, t);
        tl.set(c, { opacity: 0 }, t + 8 * FR);
      });
      if (p.via !== undefined) { tl.to(g, { opacity: 0, duration: 3 * FR }, p.via - 3 * FR); tl.set(g, { display: 'none' }, p.via); }
    } else if (p.tipo === 'arco') {
      // l'anello che si riempie (gadzhi-05) con la lancetta che gira: un giro intero = la durata detta, senza cifre
      const r = p.r || 150, sp = p.spessore || 16;
      const g = svg('g', {}, S);
      const traccia = svg('circle', { cx: p.x, cy: p.y, r, fill: 'none', stroke: 'rgba(141,255,169,0.22)', 'stroke-width': sp }, g);
      const pieno = svg('circle', { cx: p.x, cy: p.y, r, fill: 'none', stroke: '#8DFFA9', 'stroke-width': sp, 'stroke-linecap': 'round',
        pathLength: 1, transform: `rotate(-90 ${p.x} ${p.y})` }, g);
      pieno.setAttribute('class', 'inf-linea');
      pieno.setAttribute('stroke-dasharray', '1 1');
      gsap.set(pieno, { attr: { 'stroke-dashoffset': 1 }, opacity: 0 });
      tl.set(pieno, { opacity: 1 }, p.t0 + FR);
      // p.fino: fin dove si riempie (1 = giro intero; tappa 2: «20 minuti» = un terzo)
      const fino = p.fino === undefined ? 1 : p.fino;
      tl.to(pieno, { attr: { 'stroke-dashoffset': 1 - fino }, duration: p.t1 - p.t0, ease: 'power1.inOut' }, p.t0);
      // le tacche delle ore, solo segni (niente cifre)
      for (let k = 0; k < 12; k++) {
        const a = k / 12 * 2 * Math.PI, r1 = r - sp * 1.6, r2 = r - sp * (k % 3 === 0 ? 2.8 : 2.2);
        svg('line', { x1: p.x + r1 * Math.sin(a), y1: p.y - r1 * Math.cos(a), x2: p.x + r2 * Math.sin(a), y2: p.y - r2 * Math.cos(a),
          stroke: 'rgba(244,244,244,0.55)', 'stroke-width': 4, 'stroke-linecap': 'round' }, g);
      }
      if (p.lancetta !== false) {
        const l = svg('line', { x1: p.x, y1: p.y, x2: p.x, y2: p.y - r * 0.62, stroke: '#F4F4F4', 'stroke-width': 9, 'stroke-linecap': 'round' }, g);
        svg('circle', { cx: p.x, cy: p.y, r: 11, fill: '#F4F4F4' }, g);
        gsap.set(l, { svgOrigin: `${p.x} ${p.y}`, rotation: 0 });
        tl.to(l, { rotation: 360 * (p.fino === undefined ? 1 : p.fino), duration: p.t1 - p.t0, ease: 'power1.inOut' }, p.t0);
      }
      if (!intero(T0)) { gsap.set(g, { opacity: 0 }); tl.set(g, { opacity: 1 }, T0);
        tl.fromTo(g, { scale: 0.7, svgOrigin: `${p.x} ${p.y}` }, { scale: 1, duration: 5 * FR, ease: 'back.out(1.6)', immediateRender: false }, T0); }
      if (p.colpo_fine) {
        tl.fromTo(pieno, { attr: { 'stroke-width': sp } }, { attr: { 'stroke-width': sp * 1.6 }, duration: 3 * FR, ease: 'power2.out', immediateRender: false }, p.t1);
        tl.to(pieno, { attr: { 'stroke-width': sp }, duration: 6 * FR, ease: 'power2.inOut' }, p.t1 + 3 * FR);
      }
      if (p.via !== undefined) { tl.to(g, { opacity: 0, duration: 3 * FR }, p.via - 3 * FR); tl.set(g, { display: 'none' }, p.via); }
    } else if (p.tipo === 'punti') {
      // tante persone come punti (gadzhi-22, martell-03 senza figure): compaiono a ondate, poi arrivano tutti al punto «verso»
      const [ax, ay, aw, ah] = p.area, rnd = semi(p.seme || 5);
      const fr = p.fr || 14;
      const pts = [];
      // giro 4, direttore: griglia regolare (gadzhi-22) con un piccolo scarto seminato: niente grumi né anelli che ricordino cifre
      const pos = [];
      if (p.passo) {
        for (let yy = ay; yy <= ay + ah; yy += p.passo) for (let xx = ax; xx <= ax + aw; xx += p.passo) pos.push([xx + (rnd() - 0.5) * (p.scarto || 6), yy + (rnd() - 0.5) * (p.scarto || 6)]);
      } else for (let k = 0; k < (p.n || 120); k++) pos.push([ax + rnd() * aw, ay + rnd() * ah]);
      const n = pos.length;
      if (p.verso) pos.sort((A, B) => Math.hypot(A[0] - p.verso[0], A[1] - p.verso[1]) - Math.hypot(B[0] - p.verso[0], B[1] - p.verso[1]));
      for (let k = 0; k < n; k++) {
        const c = el('div', 'inf-punto', sopra);
        const [xx, yy] = pos[k], s = p.lato_punto || 14;
        if (p.tenue) c.style.opacity = p.tenue;
        px(c, { left: xx - s / 2, top: yy - s / 2, width: s, height: s });
        const t = T0 + rnd() * fr * FR;
        if (!intero(T0)) { gsap.set(c, { opacity: 0, scale: 0 }); tl.to(c, { opacity: 1, scale: 1, duration: 3 * FR, ease: 'back.out(2)' }, t); }
        pts.push([c, xx, yy]);
      }
      if (p.verso && p.deriva) {
        // giro 4, direttore: i punti si muovono dal primo fotogramma (una lenta deriva verso il punto d'arrivo)
        pts.forEach(([c, xx, yy]) => tl.to(c, { x: (p.verso[0] - xx) * p.deriva, y: (p.verso[1] - yy) * p.deriva, duration: Math.max(0.1, p.t_verso - T0),
          ease: 'none' }, T0));
      }
      if (p.verso) {
        const [vx, vy] = p.verso, fv = p.fr_verso || 14;
        // a ondate, dal più vicino al più lontano; ognuno corre al punto e sparisce dentro (niente punti vaganti)
        pts.forEach(([c, xx, yy], k) => {
          const t = p.t_verso + (k / n) * fv * FR;
          tl.to(c, { x: vx - xx, y: vy - yy, scale: 0.3, duration: 9 * FR, ease: 'power2.in' }, t);
          tl.set(c, { opacity: 0 }, t + 9 * FR);
        });
      }
    } else if (p.tipo === 'logo') {
      // giro 5: il logo intero MOBILITAS (il pittogramma da solo, a 390 px, si leggeva come un «7») in una card con spessore
      const W = p.w || 520, H = Math.round(W / 7.27), pad = Math.round(H * 0.55);
      const c = el('div', 'inf-scheda inf-logo', sopra);
      px(c, { left: p.x - W / 2 - pad, top: p.y - H / 2 - pad, width: W + 2 * pad, height: H + 2 * pad, borderRadius: Math.round(pad * 0.9) });
      const im = el('img', 'inf-logo-img', c); im.src = 'assets/logo_verde.png';
      px(im, { left: pad, top: pad, width: W, height: H });
      nasce(c, T0, p.nasce_da ? da_dove(p, p.x, p.y) : { da: 0.85, fr: 5, ease: 'back.out(1.5)' });
      (p.colpo || []).forEach((t) => colpo(c, t));
      if (p.muovi) { const mv = el('div', 'inf-mv', sopra); sopra.insertBefore(mv, c); mv.appendChild(c); gsap.set(mv, { transformOrigin: `${p.x}px ${p.y}px` }); muovi(mv, p); }
      esce(c, p.via);
    } else if (p.tipo === 'immagine' && p.src) {
      // tappa 2: un disegno Servier libero nella scena (ricolorato nel brand dal motore), centrato in x, y
      const im = el('img', 'inf-servier', sopra); im.src = p.src;
      px(im, { left: p.x - p.img_w / 2, top: p.y - p.img_h / 2, width: p.img_w, height: p.img_h });
      // giro 5 (direttore): un disegno «spento» resta (si abbassa), non sparisce
      if (p.spento !== undefined) tl.to(im, { opacity: 0.35, duration: 6 * FR, ease: 'power2.out' }, p.spento);
      if (p.sfuma) {
        // tappa 2 (direttore): niente taglio netto in fondo al ritaglio: il disegno sfuma nel fondo
        const m = `linear-gradient(to bottom, #000 calc(100% - ${p.sfuma}px), transparent)`;
        im.style.webkitMaskImage = m; im.style.maskImage = m;
      }
      nasce(im, T0, p.nasce_da ? da_dove(p, p.x, p.y) : { da: 0.9, fr: 6, ease: 'power3.out' });
      if (p.muovi) { const mv = el('div', 'inf-mv', sopra); sopra.insertBefore(mv, im); mv.appendChild(im); gsap.set(mv, { transformOrigin: `${p.x}px ${p.y}px` }); muovi(mv, p); }
      if (p.pulsa) p.pulsa.forEach((t) => colpo(im, t));
      esce(im, p.via);
    } else if (p.tipo === 'indicatore') {
      // 07/11/2026: l'indicatore di struttura (verticale-11: trattini; verticale-08: 1-2-3-4): n trattini, quello attivo verde,
      // più lungo e con la luce, quelli fatti panna, quelli che verranno appena accennati
      const n = p.n || 3, w = p.w || 92, h = p.h || 16, gap = p.gap || 18, lungo = p.lungo || 1.7;
      const g = el('div', 'inf-ind', sopra);
      px(g, { left: p.x, top: p.y - h / 2, width: n * w * lungo + (n - 1) * gap, height: h });
      const seg = [];
      for (let k = 0; k < n; k++) { const q = el('div', 'inf-ind-s', g); px(q, { left: k * (w + gap), top: 0, width: w, height: h, borderRadius: h / 2 }); seg.push(q); }
      const metti = (att, t) => {
        let xx = 0;
        seg.forEach((q, k) => {
          const L = k === att ? w * lungo : w;
          const css = { left: xx, width: L, backgroundColor: k === att ? '#72FA93' : (k < att ? 'rgba(244,244,244,0.78)' : 'rgba(244,244,244,0.22)'),
            boxShadow: k === att ? '0 0 14px rgba(141,255,169,0.9), 0 0 36px rgba(114,250,147,0.45)' : '0 0 0 rgba(0,0,0,0)' };
          if (t === undefined) gsap.set(q, css); else tl.to(q, Object.assign({ duration: 6 * FR, ease: 'power3.out' }, css), t);
          xx += L + gap;
        });
      };
      const st = p.stati || [{ t: T0, attivo: 0 }];
      metti(st[0].attivo);
      st.slice(1).forEach((s) => metti(s.attivo, s.t));
      nasce(g, T0, { da: 0.8, fr: 6, ease: 'power3.out' });
      esce(g, p.via);
    } else if (p.tipo === 'barra') {
      // 07/11/2026: la barra che si riempie a confronto (verticale-10): pista panna tenue, riempimento verde con la luce, da t0 a t1
      // fino a «fino» (0-1, la parte detta); spento: si abbassa (panna) quando la voce la mette da parte
      const g = el('div', 'inf-bar', sopra);
      px(g, { left: p.x, top: p.y - p.h / 2, width: p.w, height: p.h, borderRadius: p.h / 2 });
      const f = el('div', 'inf-bar-f', g);
      px(f, { left: 0, top: 0, width: p.w, height: p.h, borderRadius: p.h / 2 });
      gsap.set(f, { scaleX: intero(p.t0) ? (p.fino === undefined ? 1 : p.fino) : 0.0001, transformOrigin: '0% 50%' });
      if (!intero(p.t0)) tl.to(f, { scaleX: p.fino === undefined ? 1 : p.fino, duration: Math.max(2 * FR, p.t1 - p.t0), ease: 'power2.inOut' }, p.t0);
      if (p.spento !== undefined) tl.to(f, { backgroundColor: 'rgba(244,244,244,0.45)', boxShadow: '0 0 0 rgba(0,0,0,0)', duration: 6 * FR }, p.spento);
      (p.colpo || []).forEach((t) => colpo(g, t));
      nasce(g, T0, p.nasce_da ? da_dove(p, p.x + p.w / 2, p.y) : { da: 0.9, fr: 5, ease: 'power3.out' });
      esce(g, p.via);
    } else if (p.tipo === 'scheda') {
      const c = el('div', 'inf-scheda', sopra);
      px(c, { left: p.x, top: p.y, width: p.w, height: p.h, borderRadius: p.raggio || 34 });
      nasce(c, T0, p.nasce_da ? da_dove(p, p.x + p.w / 2, p.y + p.h / 2) : { da: 0.85, fr: 5, ease: 'back.out(1.4)' });
      if (p.muovi) { const mv = el('div', 'inf-mv', sopra); sopra.insertBefore(mv, c); mv.appendChild(c); gsap.set(mv, { transformOrigin: `${p.x + p.w / 2}px ${p.y + p.h / 2}px` }); muovi(mv, p); }
      if (p.spento !== undefined) {
        // giro 5 (direttore): la card si spegne davvero (velo blu notte opaco), non resta uguale
        const v = el('div', 'inf-velo inf-velo-pill', c);
        gsap.set(v, { opacity: 0 });
        tl.to(v, { opacity: 0.75, duration: 6 * FR, ease: 'power2.out' }, p.spento);
      }
      if (p.acceso !== undefined) {
        const luce = el('div', 'inf-scheda-luce', c);
        gsap.set(luce, { opacity: 0 });
        tl.to(luce, { opacity: 1, duration: 3 * FR, ease: 'power2.out' }, p.acceso);
        colpo(c, p.acceso);
      }
      esce(c, p.via);
    }
  });
};

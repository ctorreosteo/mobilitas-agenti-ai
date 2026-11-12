// Sagoma posturale stilizzata di profilo (guarda a destra): una figura piena con
// testa, naso e braccio. Dietro resta il suo "fantasma" dritto; sulla frase la
// schiena si curva e la testa va avanti, e la linea orecchio-spalla-anca-
// ginocchio-caviglia si piega con lei. Non e un paziente: e lo schema del concetto.
// DATI: lato, piega {t, testo}, chiave {t, testo}, gradi (piega massima, default 16)
const lato = D.lato || 'dx';
const p = pannello(lato);
muoviPannello(p, lato);
const NS = 'http://www.w3.org/2000/svg';
const svg = document.createElementNS(NS, 'svg');
svg.setAttribute('viewBox', '0 60 480 680');
svg.setAttribute('class', 'figura');
p.appendChild(svg);
function s(tag, attrs, parent) {
  const e = document.createElementNS(NS, tag);
  Object.entries(attrs).forEach(([k, v]) => e.setAttribute(k, v));
  (parent || svg).appendChild(e);
  return e;
}
// colori pieni (panna sul blu notte): fantasma 14%, figura 32%, braccio 42%
const FANTASMA = '#224269', CORPO = '#4D6684', BRACCIO = '#667D98';
// scheletro dritto: dal basso verso l'alto
const J = { piede: [282, 736], caviglia: [232, 726], ginocchio: [236, 582], anca: [232, 430], lombare: [232, 352],
  torace: [230, 272], c7: [234, 204], testa: [240, 132] };
// quota della piega per segmento (somma 1,2: la testa va avanti piu del busto)
const QUOTA = { lombare: 0.15, torace: 0.35, c7: 0.30, testa: 0.40 };
const CATENA = ['lombare', 'torace', 'c7', 'testa'];
function piega(a) {
  const P = Object.assign({}, J);
  let ang = 0, prev = J.anca, prevN = J.anca;
  CATENA.forEach((k) => {
    ang += a * QUOTA[k];
    const r = ang * Math.PI / 180, dx = J[k][0] - prev[0], dy = J[k][1] - prev[1];
    // rotazione oraria (y verso il basso): un segmento che sale va verso destra
    const q = [prevN[0] + dx * Math.cos(r) - dy * Math.sin(r), prevN[1] + dx * Math.sin(r) + dy * Math.cos(r)];
    prev = J[k]; prevN = q; P[k] = q; P['ang_' + k] = ang;
  });
  P.spalla = [P.c7[0] + (P.torace[0] - P.c7[0]) * 0.3, P.c7[1] + (P.torace[1] - P.c7[1]) * 0.3];
  return P;
}
function figura(colore, braccio) {
  const g = s('g', {});
  const lin = (w, col) => s('polyline', { fill: 'none', stroke: col, 'stroke-width': w, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
  const parti = { piede: lin(30, colore), gamba: lin(60, colore), busto: lin(100, colore), collo: lin(40, colore),
    testa: s('circle', { r: 50, fill: colore }, g), naso: s('path', { fill: colore }, g),
    braccio: braccio ? lin(36, braccio) : null };
  return parti;
}
function disegna(f, P) {
  const pt = (q) => q.map((v) => v.toFixed(1)).join(',');
  f.piede.setAttribute('points', [J.caviglia, J.piede].map(pt).join(' '));
  f.gamba.setAttribute('points', [J.caviglia, J.ginocchio, J.anca].map(pt).join(' '));
  f.busto.setAttribute('points', [J.anca, P.lombare, P.torace, P.c7].map(pt).join(' '));
  f.collo.setAttribute('points', [P.c7, P.testa].map(pt).join(' '));
  f.testa.setAttribute('cx', P.testa[0]); f.testa.setAttribute('cy', P.testa[1]);
  // naso: un piccolo triangolo davanti alla testa, ruotato con lei
  const r = (P.ang_testa || 0) * Math.PI / 180;
  const rot = ([x, y]) => [P.testa[0] + x * Math.cos(r) - y * Math.sin(r), P.testa[1] + x * Math.sin(r) + y * Math.cos(r)];
  const n = [rot([44, -16]), rot([66, 6]), rot([44, 14])];
  f.naso.setAttribute('d', 'M' + n.map(pt).join(' L') + ' Z');
  if (f.braccio) {
    // il braccio pende dalla spalla (gravita), con il gomito appena avanti
    const sp = P.spalla;
    f.braccio.setAttribute('points', [sp, [sp[0] + 10, sp[1] + 130], [sp[0] + 26, sp[1] + 246]].map(pt).join(' '));
  }
}
// fantasma dritto, verticale di riferimento, figura
const fantasma = figura(FANTASMA, null);
disegna(fantasma, piega(0));
s('line', { x1: J.caviglia[0], y1: 70, x2: J.caviglia[0], y2: 740, stroke: 'rgba(244,244,244,0.35)', 'stroke-width': 3, 'stroke-dasharray': '10 10' });
const corpo = figura(CORPO, BRACCIO);
const linea = s('polyline', { points: '', fill: 'none', stroke: '#72FA93', 'stroke-width': 6, 'stroke-linejoin': 'round', 'stroke-linecap': 'round' });
const punti = [0, 1, 2, 3, 4].map(() => s('circle', { r: 10, fill: '#002552', stroke: '#72FA93', 'stroke-width': 5 }));
const stato = { a: 0 };
function aggiorna() {
  const P = piega(stato.a);
  disegna(corpo, P);
  const r = (P.ang_testa || 0) * Math.PI / 180;
  const orecchio = [P.testa[0] + 4 * Math.cos(r) + 4 * Math.sin(r), P.testa[1] + 4 * Math.sin(r) - 4 * Math.cos(r)];
  const pts = [orecchio, P.spalla, J.anca, J.ginocchio, J.caviglia];
  linea.setAttribute('points', pts.map((q) => q.join(',')).join(' '));
  pts.forEach((q, i) => { punti[i].setAttribute('cx', q[0]); punti[i].setAttribute('cy', q[1]); });
}
aggiorna();
tl.fromTo(svg, { opacity: 0 }, { opacity: 1, duration: 0.5 }, 0.2);
const piccolo = el('div', 'piccolo', p, esc((D.piega && D.piega.testo) || ''));
const tp = Math.max(0.5, (D.piega && D.piega.t) || 0.6);
entra(piccolo, tp - 0.1);
tl.to(stato, { a: D.gradi || 16, duration: 2.6, ease: 'sine.inOut', onUpdate: aggiorna }, tp);
const ch = el('div', 'chiave', p, frase((D.chiave && D.chiave.testo) || '', true));
entra(ch, Math.max(0.6, (D.chiave && D.chiave.t) || 0) - 0.05);
chiudi();

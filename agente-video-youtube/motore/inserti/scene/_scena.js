// Scene "dentro la scena" (fase 6a, livello alzato in 6b): piu elementi in una pagina, uno strato
// (dietro o davanti). Ogni modello e MODELLI.<nome>(box, x, d): x.s / x.e sono
// inizio e fine dell'elemento nel tempo del pezzo, d i suoi dati (tempi gia nel
// pezzo). Una sola timeline in pausa; niente timer, niente casuale non seminato.
//
// Regole di mestiere (skill mobilitas-grafica, "Livello 3"), qui come costanti:
// entrate di 8-12 frame con easing deciso (expo.out, o back.out(1.0) = rimbalzo
// del 3,7%), parole sfalsate di 2-3 frame, uscite piu corte (6 frame).
const DATI = window.SCENA_DATI;
const T = DATI.durata;
const FPS = DATI.fps || 25;
const FR = 1 / FPS;
const ENTRA = 10 * FR;        // 0,40 s
const ENTRA_GRANDE = 13 * FR; // oggetti grandi (telefono, schermate)
const ESCE = 6 * FR;          // 0,24 s
const SFASA = 2.5 * FR;       // fra parole che entrano insieme
const RIMBALZO = 'back.out(1.0)';
const SCENA = document.getElementById('scena');
const tl = gsap.timeline({ paused: true });
const MODELLI = {};

function el(tag, cls, parent, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  (parent || SCENA).appendChild(e);
  return e;
}

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function px(e, props) {
  Object.entries(props).forEach(([k, v]) => { e.style[k] = typeof v === 'number' ? v + 'px' : v; });
  return e;
}

// una parola che entra: da sfocata, un po' piu in basso e piccola, a ferma
function entraParola(e, t, o) {
  o = o || {};
  tl.fromTo(e, { opacity: 0, y: o.dy === undefined ? 34 : o.dy, scale: o.da === undefined ? 0.92 : o.da,
    filter: 'blur(' + (o.blur === undefined ? 12 : o.blur) + 'px)' },
  { opacity: 1, y: 0, scale: 1, filter: 'blur(0px)', duration: o.dur || ENTRA, ease: o.ease || 'expo.out' },
  Math.max(0, t));
}

// uscita: piu corta dell'entrata, accelera, con un filo di sfocatura
function esceVia(e, t, o) {
  o = o || {};
  tl.to(e, { opacity: 0, y: o.dy === undefined ? -12 : o.dy, scale: o.a === undefined ? 0.97 : o.a,
    filter: 'blur(' + (o.blur === undefined ? 8 : o.blur) + 'px)', duration: o.dur || ESCE,
    ease: 'power2.in' }, Math.max(0, t));
}

// fluttuare leggero (oggetti vicino alle mani): segmenti sine finiti, nessun repeat
function fluttua(e, da, a, ampiezza, periodo) {
  const amp = ampiezza || 7, per = periodo || 2.8;
  let t = da, su = true;
  while (t + per / 2 < a) {
    tl.to(e, { y: su ? -amp : amp * 0.6, rotation: su ? 0.5 : -0.4, duration: per / 2, ease: 'sine.inOut' }, t);
    t += per / 2;
    su = !su;
  }
}

function svg(tag, attrs, parent) {
  const e = document.createElementNS('http://www.w3.org/2000/svg', tag);
  Object.entries(attrs || {}).forEach(([k, v]) => e.setAttribute(k, v));
  if (parent) parent.appendChild(e);
  return e;
}

function frecciaGiu(parent, colore, spessore) {
  const s = svg('svg', { viewBox: '0 0 80 110', class: 'freccia-svg' }, parent);
  svg('path', { d: 'M40 8 L40 96 M12 68 L40 98 L68 68', fill: 'none', stroke: colore || '#72FA93',
    'stroke-width': spessore || 11, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, s);
  return s;
}

// ---------------------------------------------------------------- maschere (6b)
// Rivelazione: il contenuto sale (o scorre) da dietro un bordo fermo invece di
// dissolversi. La maschera e un wrapper con overflow nascosto e sfocatura di
// movimento spenta (quella di HyperFrames disegnerebbe fuori dal bordo).
function maschera(e, cls) {
  const w = document.createElement('span');
  w.className = 'msk' + (cls ? ' ' + cls : '');
  w.setAttribute('data-motion-blur', 'off');
  e.parentNode.insertBefore(w, e);
  w.appendChild(e);
  return w;
}

// tappa 3: la maschera serve solo mentre la parola entra o esce. A entrata finita si apre
// (overflow visibile): il testo fermo e identico a quello disegnato senza maschere, con
// accenti, discendenti e ombre interi (6:44: la «g» di «già» e «toglie» era tagliata;
// le ombre dei titoli dietro avevano i bordi dritti della maschera)
function _msk(e) {
  const m = e.parentNode;
  return m && m.classList && m.classList.contains('msk') ? m : null;
}

function rivela(e, t, o) {
  o = o || {};
  const dir = o.dir || 'su';
  const da = { su: { yPercent: 135 }, giu: { yPercent: -135 }, sx: { xPercent: -110 }, dx: { xPercent: 110 } }[dir];
  const t0 = Math.max(0, t), dur = o.dur || ENTRA;
  const m = _msk(e);
  tl.fromTo(e, Object.assign({ rotation: o.ruota || 0 }, da),
    { xPercent: 0, yPercent: 0, rotation: 0, duration: dur, ease: o.ease || 'expo.out' }, t0);
  // l'opacita a parte: prima di entrare la parola non c'e (0, non solo nascosta dalla
  // maschera), cosi il controllo «lettere intere» puo aprire le maschere senza vederla
  tl.fromTo(e, { opacity: m ? 0 : 1 }, { opacity: 1, duration: 0.001 }, t0);
  if (m) {
    tl.set(m, { overflow: 'hidden' }, t0);
    tl.set(m, { overflow: 'visible' }, t0 + dur);
  }
}

function nascondi(e, t, o) {
  o = o || {};
  const a = { su: { yPercent: -135 }, giu: { yPercent: 135 }, sx: { xPercent: -110 }, dx: { xPercent: 110 } }[o.dir || 'su'];
  const m = _msk(e);
  if (m) tl.set(m, { overflow: 'hidden' }, Math.max(0, t));
  tl.to(e, Object.assign({ duration: o.dur || ESCE, ease: 'power3.in' }, a), Math.max(0, t));
  if (m) tl.set(e, { opacity: 0 }, Math.max(0, t) + (o.dur || ESCE));   // uscita: la parola non c'e piu
}

// icone lineari (tratto unico, angoli tondi), viewBox 48x48
const ICONE = {
  mani: ['M14 30 V17 a3 3 0 0 1 6 0 V27', 'M20 25 V12 a3 3 0 0 1 6 0 V26', 'M26 25 V14 a3 3 0 0 1 6 0 V28',
    'M32 27 V19 a3 3 0 0 1 6 0 V31 c0 8 -6 13 -13 13 h-2 c-4 0 -6.5 -1.4 -8.6 -3.5 L8.5 34.6 a3 3 0 0 1 4.2 -4.2 L14 31.6'],
  postura: ['M20.5 8 a3.5 3.5 0 1 0 7 0 a3.5 3.5 0 1 0 -7 0', 'M24 13 V29', 'M14 17 L24 14 L34 17', 'M18 42 L24 29 L30 42',
    'M40 4 V44'],
  telefono: ['M15 4 h18 a4 4 0 0 1 4 4 v32 a4 4 0 0 1 -4 4 h-18 a4 4 0 0 1 -4 -4 v-32 a4 4 0 0 1 4 -4 Z',
    'M21 9 h6', 'M23 38 h2'],
  dialogo: ['M8 9 h32 a4 4 0 0 1 4 4 v17 a4 4 0 0 1 -4 4 h-17 l-9 7 v-7 h-6 a4 4 0 0 1 -4 -4 v-17 a4 4 0 0 1 4 -4 Z',
    'M16 21.5 h0.01', 'M24 21.5 h0.01', 'M32 21.5 h0.01'],
  lista: ['M10 12 l3 3 l6 -6', 'M24 12 h14', 'M10 26 l3 3 l6 -6', 'M24 26 h14', 'M10 40 h0.01', 'M24 40 h14'],
  // fase 7c: appuntamenti e visite (oggetto, niente figure umane)
  calendario: ['M10 12 h28 a4 4 0 0 1 4 4 v22 a4 4 0 0 1 -4 4 h-28 a4 4 0 0 1 -4 -4 v-22 a4 4 0 0 1 4 -4 Z',
    'M6 20 h36', 'M16 7 v8', 'M32 7 v8', 'M17 30 l4 4 l9 -9'],
};

function icona(nome, parent, cls) {
  const s = svg('svg', { viewBox: '0 0 48 48', class: 'icona ' + (cls || '') }, parent);
  (ICONE[nome] || []).forEach((d, k) => {
    const p = svg('path', { d: d, fill: 'none', stroke: 'currentColor', 'stroke-width': 3,
      'stroke-linecap': 'round', 'stroke-linejoin': 'round', pathLength: 1 }, s);
    if (nome === 'postura' && k === 4) p.setAttribute('stroke-dasharray', '0.04 0.035');
  });
  return s;
}

// l'icona si disegna (tratto che corre), sfalsata per tratto
function disegna(s, t, dur) {
  [...s.querySelectorAll('path')].forEach((p, k) => {
    if (p.getAttribute('stroke-dasharray')) {
      tl.fromTo(p, { opacity: 0 }, { opacity: 1, duration: 6 * FR }, t + k * 2 * FR);
      return;
    }
    p.setAttribute('stroke-dasharray', '1 1');
    tl.fromTo(p, { attr: { 'stroke-dashoffset': 1 } }, { attr: { 'stroke-dashoffset': 0 }, duration: dur || 14 * FR,
      ease: 'power2.out' }, t + k * 2 * FR);
  });
}

// ---------------------------------------------------------------- parallasse (6b)
// Gli strati seguono la camera del piatto con una profondita: 1 = incollato alla
// scena, <1 piu lontano (dietro: 0,9), >1 piu vicino (davanti: 1,12), 0 = fermo
// sullo schermo (stacchi pieni). Riferimento: la camera all'ingresso dell'elemento.
const CAM = DATI.cam || [];
function parallasse(box, x) {
  const k = x.prof !== undefined ? x.prof : (x.pieno ? 0 : (DATI.strato === 'dietro' ? 0.9 : 1.12));
  if (!k || !CAM.length) return;
  const n = CAM.length;
  const fr = Math.max(0, Math.min(n - 1, Math.round(x.s * FPS)));
  const r = CAM[fr];
  gsap.set(box, { transformOrigin: '0px 0px' });
  const fA = Math.max(0, Math.floor(x.s * FPS) - 2), fB = Math.min(n - 1, Math.ceil(x.e * FPS) + 2);
  for (let f = fA; f <= fB; f++) {
    const c = CAM[f];
    const s = 1920 / c[2];
    const a = Math.pow(r[2] / c[2], k);
    tl.set(box, { x: (r[0] - c[0]) * s * k, y: (r[1] - c[1]) * s * k, scale: a }, f * FR);
  }
}

// parallasse su un nodo qualsiasi, con il suo riferimento (es. ogni card dal suo ingresso)
function parallasseSu(nodo, tRef, tA, tB, k) {
  if (!k || !CAM.length) return;
  const n = CAM.length;
  const r = CAM[Math.max(0, Math.min(n - 1, Math.round(tRef * FPS)))];
  gsap.set(nodo, { transformOrigin: '0px 0px' });
  for (let f = Math.max(0, Math.floor(tA * FPS) - 2); f <= Math.min(n - 1, Math.ceil(tB * FPS) + 2); f++) {
    const c = CAM[f];
    const s = 1920 / c[2];
    tl.set(nodo, { x: (r[0] - c[0]) * s * k, y: (r[1] - c[1]) * s * k, scale: Math.pow(r[2] / c[2], k) }, f * FR);
  }
}

// ---------------------------------------------------------------- campionario v3 (30/10/2026)
// numeri casuali seminati: ogni render e identico (contratto HyperFrames)
function semi(n) {
  let s = (Math.floor(n) * 2654435761) >>> 0 || 1;
  return () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; };
}
const CIFRARIO = 'ABCDEFGHKLMNPRSTUVZ0123456789#%@$&*';

// testo che si decifra (reference gadzhi-08/09/12): in `nf` frame da t0 le lettere passano
// da caratteri casuali alla parola, fermandosi da sinistra; uno strato per frame (scatti,
// niente dissolvenze), poi il testo vero. Prima di t0 non c'e niente.
function decifra(cont, testo, t0, nf, seme, cls, insieme) {
  const r = semi(seme || testo.length * 31 + 7);
  // i caratteri casuali somigliano al testo (direttore v3): cifre sui numeri, minuscole sulle
  // parole minuscole; cosi la larghezza resta quella della parola e nessuno strato esce dal posto
  // simboli, cifre e maiuscole come in gadzhi-09 («CO%@$01»); sui numeri solo cifre. Almeno 12 frame
  // (0,5 s: 6 frame a 12 fps della reference), le lettere vere si fissano da sinistra
  // insieme 'minuscole' (fase 7c): lettere provvisorie minuscole, larghe quanto la parola vera
  // (le maiuscole e i simboli allargano le parole lunghe di un terzo: «giorno dopo giorno» usciva dal quadro)
  const set = (c) => /[0-9]/.test(c) ? '0123456789'
    : (insieme === 'minuscole' ? 'acemnorsuvxz' : '#%@$*0123456789ABCDEHKNPRSTUZ');
  nf = Math.max(nf, 12);
  const vero = el('span', 'dc-vero' + (cls ? ' ' + cls : ''), cont, esc(testo));
  gsap.set(vero, { opacity: 0 });
  for (let k = 0; k < nf; k++) {
    const fermi = Math.floor(testo.length * (k + 1) / (nf + 1));
    let s = '';
    for (let i = 0; i < testo.length; i++) {
      const c = testo[i];
      const cs = set(c);
      s += (i < fermi || c === ' ' || /[^0-9A-Za-zÀ-ÿ]/.test(c)) ? c : cs[Math.floor(r() * cs.length)];
    }
    const sp = el('span', 'dc-strato' + (cls ? ' ' + cls : ''), cont, esc(s));
    gsap.set(sp, { opacity: 0 });
    tl.set(sp, { opacity: 1 }, t0 + k * FR);
    tl.set(sp, { opacity: 0 }, t0 + (k + 1) * FR);
  }
  tl.set(vero, { opacity: 1 }, t0 + nf * FR);
  return vero;
}

// uscita all'indietro (gadzhi-10): il testo si cancella dalla fine, carattere per carattere
function cancella(cont, vero, testo, t1, nf, cls) {
  tl.set(vero, { opacity: 0 }, t1);
  for (let k = 0; k < nf; k++) {
    const s = testo.slice(0, Math.floor(testo.length * (nf - k - 1) / nf));
    if (!s.trim()) continue;
    const sp = el('span', 'dc-strato' + (cls ? ' ' + cls : ''), cont, esc(s));
    gsap.set(sp, { opacity: 0 });
    tl.set(sp, { opacity: 1 }, t1 + k * FR);
    tl.set(sp, { opacity: 0 }, t1 + (k + 1) * FR);
  }
}

// retino di punti (gadzhi-07/08): una fascia sinuosa di punti panna/verdi sul fondo scuro,
// punti piu grandi al centro della fascia. Statico: lo muove il chiamante (x/y lenti).
function retino(parent, o) {
  o = o || {};
  const W = o.w || 2400, H = o.h || 1400, passo = o.passo || 16;
  const c = el('canvas', 'v3-retino', parent);
  c.width = W; c.height = H;
  const g = c.getContext('2d');
  const r = semi(o.seme || 11);
  for (let y = passo / 2; y < H; y += passo) {
    for (let x = passo / 2; x < W; x += passo) {
      // distanza da due curve sinuose (la fascia)
      let d = 1e9;
      for (const [a, f, ph, y0] of (o.curve || [[220, 0.0026, 0.4, 0.42], [170, 0.0031, 2.1, 0.78]])) {
        d = Math.min(d, Math.abs(y - (H * y0 + a * Math.sin(x * f + ph))));
      }
      const v = Math.max(0, 1 - d / (o.larga || 150));
      if (v <= 0.02) continue;
      const rad = passo * 0.36 * Math.pow(v, 0.7) * (0.75 + 0.25 * r());
      g.fillStyle = r() < (o.verdi || 0.35) ? `rgba(114,250,147,${0.55 * v})` : `rgba(244,244,244,${0.38 * v})`;
      g.beginPath(); g.arc(x, y, rad, 0, 6.2832); g.fill();
    }
  }
  return c;
}

function avvia() {
  DATI.elementi.forEach((x, i) => {
    const box = el('div', 'el el-' + x.modello);
    box.style.zIndex = 10 + i;
    box.setAttribute('data-k', i);   // tappa 3: i controlli fotografano un elemento alla volta
    MODELLI[x.modello](box, x, x.dati || {});
    parallasse(box, x);
  });
  tl.set({}, {}, T);
  window.__timelines['scena'] = tl;
}

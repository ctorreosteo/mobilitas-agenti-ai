// Funzioni comuni dei modelli di inserto (HyperFrames). Ogni modello legge
// window.DATI (testi, tempi relativi all'inizio dell'inserto, materiali), costruisce
// la scena e registra UNA timeline in pausa: tutto cio che si vede e funzione del
// tempo della timeline (niente timer, niente casuale).
const D = window.DATI;
const T = D.durata;
const SCENA = document.getElementById('scena');
const tl = gsap.timeline({ paused: true });

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

// testo con la parola chiave in peso pieno (verde: sta sempre su un pannello blu)
function frase(testo, chiave) {
  if (chiave === true) return '<span class="k">' + esc(testo) + '</span>';
  if (!chiave) return esc(testo);
  const i = testo.toLowerCase().lastIndexOf(String(chiave).toLowerCase());
  if (i < 0) return esc(testo);
  return esc(testo.slice(0, i)) + '<span class="k">' + esc(testo.slice(i, i + chiave.length)) +
    '</span>' + esc(testo.slice(i + chiave.length));
}

function pannello(lato, larghezza) {
  const p = el('div', 'pannello ' + (lato || 'dx'));
  if (larghezza) p.style.width = larghezza + 'px';
  return p;
}

// il pannello entra dal suo lato e, a fine inserto, esce. D.entra / D.esce false
// (li decide `grafica`) quando l'elemento prima o dopo usa lo stesso pannello: il
// pannello resta fermo e cambia solo il contenuto, che dissolve (vedi chiudi)
function muoviPannello(p, lato) {
  const fuori = lato === 'sx' ? -100 : 100;
  if (D.entra !== false) tl.fromTo(p, { xPercent: fuori }, { xPercent: 0, duration: 0.55, ease: 'expo.out' }, 0);
  if (D.esce !== false) tl.to(p, { xPercent: fuori, duration: 0.34, ease: 'power2.in' }, Math.max(0, T - 0.36));
}

// freccia verso il basso (la descrizione), verde su blu; con `ondeggia` si muove piano
function freccia(parent, cls, t, ondeggia) {
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 70 120');
  svg.setAttribute('class', cls || 'freccia');
  parent.appendChild(svg);
  const a = document.createElementNS(NS, 'path');
  Object.entries({ d: 'M35 6 L35 104 M10 80 L35 108 L60 80', fill: 'none', stroke: '#72FA93', 'stroke-width': 8,
    'stroke-linecap': 'round', 'stroke-linejoin': 'round' }).forEach(([k, v]) => a.setAttribute(k, v));
  svg.appendChild(a);
  tl.fromTo(svg, { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.45, ease: 'power3.out' }, Math.max(0, t));
  if (ondeggia) {
    for (let k = 0; t + 0.6 + k * 0.9 < T - 0.4; k++) {
      tl.to(svg, { y: 14, duration: 0.45, ease: 'sine.inOut' }, t + 0.6 + k * 0.9);
      tl.to(svg, { y: 0, duration: 0.45, ease: 'sine.inOut' }, t + 1.05 + k * 0.9);
    }
  }
  return svg;
}

function entra(e, t, dy) {
  tl.fromTo(e, { opacity: 0, y: dy === undefined ? 28 : dy },
    { opacity: 1, y: 0, duration: 0.45, ease: 'power3.out' }, Math.max(0, t));
}

function esce(e, t, dur) {
  tl.to(e, { opacity: 0, duration: dur || 0.25, ease: 'power1.in' }, Math.max(0, t));
}

function logo(parent, larghezza) {
  const i = el('img', 'logo', parent);
  i.src = 'assets/logo_verde.png';
  if (larghezza) i.style.width = larghezza + 'px';
  return i;
}

// una pressione a molla sulla parola che conta
function molla(e, t) {
  tl.fromTo(e, { scale: 0.96 }, { scale: 1, duration: 0.6, ease: 'back.out(2.2)' }, Math.max(0, t));
}

function chiudi() {
  // il pannello passa all'elemento dopo: il contenuto dissolve, il blu resta
  if (D.esce === false) {
    document.querySelectorAll('.pannello > *').forEach((e) =>
      tl.to(e, { opacity: 0, duration: 0.2, ease: 'power1.in' }, Math.max(0, T - 0.22)));
  }
  tl.set({}, {}, T);
  window.__timelines['inserto'] = tl;
}

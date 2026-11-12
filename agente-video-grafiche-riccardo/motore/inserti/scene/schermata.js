// Schermata tipografica a tutto schermo (1-2 s), su blu profondo con la trama del
// brand: il marchio Mobilitas gigante quasi invisibile che scorre piano, una luce
// morbida e una grana fine (seminata: ogni render e identico). Le parole entrano
// sulla parola detta; la chiave in verde (sta sul blu) e peso 800.
// d: parole [{testo, t, chiave, a_capo}], x (sinistra del testo), corpo, corpo_chiave
MODELLI.schermata = function (box, x, d) {
  // fase 7c: fondo blu vero e la principale; la classica sul velo con fondo: 'velo'
  const PIENO = d.fondo !== 'velo';
  const fondo = el('div', 'sc-fondo' + (PIENO ? ' sc-pieno' : ''), box);   // v3: fondo blu vero
  if (PIENO) {
    const rw = el('div', 'sc-ret', fondo);
    retino(rw, { w: 2400, h: 1400, passo: 18, seme: 51, verdi: 0.3, curve: [[240, 0.0023, 0.9, 0.7]], larga: 150 });
    tl.fromTo(rw, { x: 0 }, { x: -140, duration: x.e - x.s, ease: 'none' }, x.s);
  }
  const luce = el('div', 'sc-luce', fondo);
  const marchio = el('img', 'sc-marchio', fondo);
  marchio.src = 'assets/logo_verde.png';
  const grana = el('canvas', 'sc-grana', fondo);
  grana.width = 960; grana.height = 540;
  const g = grana.getContext('2d');
  const im = g.createImageData(960, 540);
  let s = 12345;
  for (let i = 0; i < im.data.length; i += 4) {
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    const v = (s >> 16) & 255;
    im.data[i] = im.data[i + 1] = im.data[i + 2] = v;
    im.data[i + 3] = 255;
  }
  g.putImageData(im, 0, 0);
  const testo = el('div', 'sc-testo', fondo);
  px(testo, { left: d.x || 220 });
  let riga = el('div', 'sc-riga', testo);
  const parole = [];
  d.parole.forEach((p, k) => {
    if (p.a_capo) riga = el('div', 'sc-riga', testo);
    // fase 7c: sul fondo pieno minuscolo con il punto finale e la chiave in gradiente (come il sito)
    let tx = p.testo;
    if (PIENO) {
      tx = tx.toLowerCase();
      if (k === d.parole.length - 1 && !/[.!?…]$/.test(tx)) tx += '.';
    }
    const w = el('span', 'sc-w' + (p.chiave ? ' sc-k' + (PIENO ? ' grad' : '') : ''), riga, esc(tx));
    w.style.fontSize = (p.chiave ? (d.corpo_chiave || 230) : (d.corpo || 124)) + 'px';
    gsap.set(w, { opacity: 0 });
    parole.push([w, p]);
  });
  // fase 7c (direttore v4): «poche persone.» -> il gradiente ripartiva a ogni parola. Le chiavi di fila sulla
  // stessa riga condividono un gradiente: ogni parola ne mostra il suo pezzo (misurato sul layout vero)
  if (PIENO) {
    const gruppi = [];
    let g0 = null;
    parole.forEach(([w, p], i) => {
      if (p.chiave && g0 && !p.a_capo && parole[i - 1][1].chiave) g0.push(w);
      else if (p.chiave) { g0 = [w]; gruppi.push(g0); } else g0 = null;
    });
    // larghezze stimate in em dai caratteri (0,6 em a lettera a 900, 0,22 em di spazio fra le parole): niente
    // misure nel browser, che al caricamento della pagina potrebbe non avere ancora il font
    gruppi.filter((g) => g.length > 1).forEach((g) => {
      const lw = g.map((w) => w.textContent.length * 0.6);
      const tot = lw.reduce((a, b) => a + b, 0) + 0.22 * (g.length - 1);
      let off = 0;
      g.forEach((w, i) => {
        w.style.backgroundSize = tot.toFixed(3) + 'em 100%';
        w.style.backgroundPosition = (-off).toFixed(3) + 'em 0';
        off += lw[i] + 0.22;
      });
    });
  }
  // il fondo entra a taglio (sulla prima parola) con un leggero assestamento di scala
  // se la schermata apre il pezzo (x.s = 0) e visibile gia sul primo frame
  gsap.set(fondo, { opacity: x.s <= FR ? 1 : 0 });
  if (x.s > FR) tl.set(fondo, { opacity: 1 }, x.s);
  // fase 6b: la schermata non sta mai ferma: il testo avanza piano (100 -> 107%) e la
  // filigrana va dall'altra parte (parallasse fra i due piani)
  const avanza = el('div', '', fondo);
  avanza.style.cssText = 'position:absolute;inset:0';
  avanza.appendChild(testo);
  tl.fromTo(avanza, { scale: 1.0 }, { scale: 1.07, duration: x.e - x.s, ease: 'none', transformOrigin: '30% 50%' }, x.s);
  tl.fromTo(marchio, { x: 0, scale: 1.0 }, { x: -40, scale: 1.02, duration: x.e - x.s, ease: 'none' }, x.s);
  tl.fromTo(luce, { xPercent: -8, opacity: 0.6 }, { xPercent: 6, opacity: 1, duration: x.e - x.s, ease: 'sine.inOut' }, x.s);
  // grana viva: si sposta a scatti ogni 2 frame (come la grana vera)
  for (let t = x.s, k = 0; t < x.e; t += 2 * FR, k++) {
    tl.set(grana, { x: ((k * 37) % 23) - 11, y: ((k * 53) % 19) - 9 }, t);
  }
  // la prima parola riempie lo schermo: entra a 1,3x e si posa al suo posto
  // mentre arrivano le altre (8 frame, ease-in-out)
  const p1 = d.parole[1];
  const ap = d.apertura || { s: 1.3, tx: 0, ty: 0 };
  gsap.set(testo, { transformOrigin: '0% 50%', scale: ap.s, x: ap.tx, y: ap.ty });
  if (p1) tl.fromTo(testo, { scale: ap.s, x: ap.tx, y: ap.ty }, { scale: 1.0, x: 0, y: 0, duration: 8 * FR,
    ease: 'power3.inOut', immediateRender: false }, p1.t - 4 * FR);
  // fase 6b: ogni parola sale da dietro la sua maschera (niente dissolvenze);
  // la chiave sale e poi si posa con una pressione di scala
  if (PIENO) {
    // v3 (direttore, reference martell-07): niente maschere; ogni parola nasce panna al 35% e
    // sfocata e in 3 frame diventa piena con la sua luce; la scena avanza piano (1,00 -> 1,05)
    parole.forEach(([w, p]) => {
      gsap.set(w, { opacity: 0 });
      const t0 = p === d.parole[0] ? Math.max(x.s, p.t - FR) : p.t;
      // la chiave in gradiente porta la sua luce verde nel filtro (il tween non deve cancellarla)
      const luce = p.chiave ? ' drop-shadow(0 0 22px rgba(114,250,147,0.55)) drop-shadow(0 0 70px rgba(114,250,147,0.25))' : '';
      tl.fromTo(w, { opacity: 0.35, filter: 'blur(10px)' + luce }, { opacity: 1, filter: 'blur(0px)' + luce, duration: 3 * FR, ease: 'power2.out', immediateRender: false }, t0);
      if (p.chiave) {
        tl.fromTo(w, { scale: 1 }, { scale: 1.06, duration: 2 * FR, ease: 'power2.out', immediateRender: false, transformOrigin: '0% 70%' }, t0);
        tl.to(w, { scale: 1, duration: 2 * FR, ease: 'power2.in' }, t0 + 2 * FR);
      }
    });
    tl.fromTo(fondo, { scale: 1.0, y: 0 }, { scale: 1.05, y: -20, duration: x.e - x.s, ease: 'none' }, x.s);
    tl.set(fondo, { opacity: 0 }, x.e);
    return;
  }
  parole.forEach(([w, p]) => {
    gsap.set(w, { opacity: 1 });
    const m = maschera(w);
    gsap.set(w, { yPercent: 135 });
    // la prima parola e gia a meta salita sul taglio (niente fotogramma blu vuoto)
    const t0 = p === d.parole[0] ? Math.max(x.s - 1 * FR, p.t - 1 * FR) : p.t;
    rivela(w, t0, { dur: p.chiave ? 9 * FR : 6 * FR });
    if (p.chiave) {
      gsap.set(m, { transformOrigin: '0% 70%' });
      tl.fromTo(m, { scale: 1.08 }, { scale: 1, duration: 12 * FR, ease: 'expo.out' }, p.t + 4 * FR);
    }
  });
  // esce a taglio: l'ultimo frame e pieno (l'uscita la fa il piatto che torna)
  tl.set(fondo, { opacity: 0 }, x.e);
};

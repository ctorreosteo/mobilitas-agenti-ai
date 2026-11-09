// Numero gigante dietro la persona (strato dietro: la composizione lo ritaglia con
// la sagoma di Vision e ci getta sopra l'ombra morbida di lui).
// Fase 6b: posizione e corpo li sceglie il motore sulle sagome vere
// (impagina.piazza_numero): la persona copre al massimo il 12% e mai la prima
// cifra. "più di" e l'etichetta sono legati al numero (stesso bordo, distanze
// fisse). Ogni cifra sta in una cella di larghezza fissa: conta senza ballare e
// Python sa dove cade ogni glifo. Entra a fuoco (sfocato e piu grande -> nitido) e
// conta un valore per frame fino al valore esatto sulla parola.
// d: valore, da, prefisso, etichetta ("\n" = a capo), arrivo, etichetta_t,
//    x, top, corpo, cella, pre {x, top, corpo}, et {x, top, corpo, allinea, w}
MODELLI.numero_dietro = function (box, x, d) {
  const corpo = d.corpo, cw = d.cella * corpo;
  const testo = String(d.valore), n = testo.length;
  const w = el('div', 'nd-wrap', box);
  // luce morbida sulla parete dietro il numero: profondita, non un pannello
  const luce = el('div', 'nd-luce', w);
  px(luce, { left: d.x - corpo * 0.5, top: d.top - corpo * 0.45, width: cw * n + corpo, height: corpo * 1.9 });
  const num = el('div', 'nd-num', w);
  px(num, { left: d.x, top: d.top, fontSize: corpo });
  const celle = [];
  for (let i = 0; i < n; i++) {
    const c = el('span', 'nd-c', num);
    c.style.width = cw + 'px';
    celle.push(c);
  }
  const fine = Number(d.valore);
  const da = d.da !== undefined ? Number(d.da) : Math.round(fine / 9);
  const scrivi = (v) => {
    const s = String(Math.round(v)).padStart(n, ' ');
    return s;
  };
  const s0 = scrivi(da);
  celle.forEach((c, i) => { c.textContent = s0[i] === ' ' ? '\u00a0' : s0[i]; });
  gsap.set(num, { transformOrigin: '0% 70%' });
  tl.fromTo(num, { opacity: 0, scale: 1.12, filter: 'blur(24px)' },
    { opacity: 1, scale: 1, filter: 'blur(0px)', duration: ENTRA_GRANDE, ease: 'expo.out' }, x.s);
  tl.fromTo(luce, { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.8, ease: 'power3.out' }, x.s);
  // conteggio: un valore per frame (power3.out) fino all'arrivo, l'ultimo e esatto
  const nfr = Math.max(2, Math.round((d.arrivo - x.s) / FR));
  let prima = s0;
  for (let k = 1; k <= nfr; k++) {
    const p = k / nfr;
    const s = scrivi(k === nfr ? fine : da + (fine - da) * (1 - Math.pow(1 - p, 3)));
    celle.forEach((c, i) => { if (s[i] !== prima[i]) tl.set(c, { textContent: s[i] === ' ' ? '\u00a0' : s[i] }, x.s + k * FR); });
    prima = s;
  }
  // arrivo: pressione di scala (4%) insieme al colpo di camera e all'impatto
  tl.fromTo(num, { scale: 1.04 }, { scale: 1, duration: 10 * FR, ease: 'power3.out', immediateRender: false }, d.arrivo);
  // "più di": sale da dietro il bordo, attaccato alla prima cifra
  const parti = [num, luce];
  if (d.prefisso) {
    const pr = el('div', 'nd-pre', w);
    px(pr, { left: d.pre.x, top: d.pre.top, fontSize: d.pre.corpo });
    const t = el('span', '', pr, esc(d.prefisso));
    maschera(t);
    rivela(t, x.s - 1 * FR, { dur: 8 * FR });      // sulla parola «più» (regola: +-2 frame)
    parti.push(pr);
  }
  if (d.etichetta) {
    const righe = String(d.etichetta).split('\n');
    righe.forEach((r, i) => {
      const e = el('div', 'nd-et', w);
      px(e, { left: d.et.x, top: d.et.top + i * 1.08 * d.et.corpo, fontSize: d.et.corpo, width: d.et.w + 4 });
      e.style.textAlign = d.et.allinea === 'dx' ? 'right' : 'left';
      const t = el('span', '', e, esc(r));
      maschera(t);
      rivela(t, (d.etichetta_t || d.arrivo + 4 * FR) + i * 3 * FR);
      parti.push(e);
    });
  }
  esceVia(w, x.e - ESCE * 1.4, { dy: 0, a: 1.03, blur: 18, dur: ESCE * 1.4 });
};

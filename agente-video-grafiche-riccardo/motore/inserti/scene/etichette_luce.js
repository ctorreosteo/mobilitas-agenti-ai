// Etichette luminose barrate (fase 7b rivista, reference martell-01): i tentativi
// come pillole blu notte con bordo e bagliore verdi, una sotto l'altra. Ognuna
// entra da sinistra in 4 frame con la sfocatura che si scioglie, sulla parola che
// la nomina; una riga panna la barra da sinistra in 3 frame sulla frase che dice
// che non cambia il bacino, e la pillola si spegne. Sotto, facoltativa, una riga
// piccola con le sue parole.
// d: x, y, corpo, spazio, voci [{testo, t, larg, barra_t, sotto, sotto_t, sotto_e, accesa}]
//    accesa: false = arriva gia spenta e barrata (richiamo di una voce detta prima)
MODELLI.etichette_luce = function (box, x, d) {
  // fase 7c: la versione «più luce» e la principale; la classica (blu che si spegne) con luce: 'classica'
  const FORTE = d.luce !== 'classica';
  const corpo = d.corpo || 56, padx = Math.round(corpo * 0.62), h = Math.round(corpo * 1.9);
  const sp = d.spazio || 30;
  let y = d.y;
  (d.voci || []).forEach((v) => {
    const g = el('div', 'el-g', box);
    px(g, { left: d.x, top: y });
    const p = el('div', 'el-pill' + (FORTE ? ' el-forte' : ''), g);   // v3: più luce e spessore
    px(p, { height: h, paddingLeft: padx, paddingRight: padx, fontSize: corpo, lineHeight: h + 'px', width: v.larg + 2 * padx });
    const spento = FORTE ? el('div', 'el-spento', p) : null;
    if (spento) gsap.set(spento, { opacity: 0 });
    const tx = el('span', 'el-tx', p, esc(v.testo));
    const riga = el('div', 'el-barra' + (FORTE && d.barra === 'panna' ? ' el-barra-panna' : ''), p);
    const t0 = v.t;
    // `accesa: false` = richiamo di una voce gia smontata: arriva accesa e si barra 3 frame
    // dopo l'atterraggio (si vede barrare), poi si spegne
    if (v.accesa === false && v.barra_t === undefined) v.barra_t = t0 + 0.34 + 3 * FR;
    const spenta = false;
    gsap.set(g, { opacity: 0, x: -90, filter: 'blur(12px)' });
    tl.to(g, { opacity: 1, duration: 5 * FR, ease: 'power1.out' }, t0);
    tl.to(g, { x: 0, filter: 'blur(0px)', duration: 8 * FR, ease: 'power3.out' }, t0);
    gsap.set(riga, { scaleX: spenta ? 1 : 0, transformOrigin: '0% 50%' });
    if (!spenta && v.barra_t !== undefined) {
      tl.to(riga, { scaleX: 1, duration: 3.5 * FR, ease: 'power2.out' }, v.barra_t);
      // barrata resta leggibile sul muro scuro (direttore, fase 7b): bordo e bagliore verdi attenuati, non spenti
      if (!FORTE) tl.to(p, { borderColor: 'rgba(114,250,147,0.5)', boxShadow: FORTE
        ? '0 6px 0 #00132E, 0 0 12px rgba(114,250,147,0.3), 0 0 0 rgba(114,250,147,0), 0 24px 44px rgba(0,10,28,0.5), inset 0 2px 0 rgba(255,255,255,0.18), inset 0 0 0 rgba(0,0,0,0)'
        : '0 0 12px rgba(114,250,147,0.35), 0 0 40px rgba(114,250,147,0.18), 0 3px 6px rgba(0,10,28,0.5), 0 18px 40px rgba(0,10,28,0.4)', duration: FORTE ? 2 * FR : 6 * FR }, v.barra_t + 2 * FR);
      if (!FORTE) tl.to(tx, { opacity: 0.8, duration: 6 * FR }, v.barra_t + 2 * FR);
      // v3 (direttore, giro 3): come in martell-01 la pillola barrata resta accesa; la barra e l'informazione
      // fase 7c (direttore v4): d.barra = 'panna' -> barra panna di 6 px che sporge di 10 px per lato, poi la
      // pillola barrata scende al 35% e perde colore (sulla pillola verde la barra blu notte sul testo blu notte non si vedeva)
      if (FORTE && d.barra === 'panna') {
        tl.to(p, { opacity: 0.38, filter: 'saturate(0.25)', duration: 6 * FR, ease: 'power2.out' }, v.barra_t + 5 * FR);
      }
    }
    let alto = h;
    if (v.sotto) {
      const s = el('div', 'el-sotto', g, esc(v.sotto));
      px(s, { top: h + 14, fontSize: d.corpo_sotto || Math.round(corpo * 0.62), width: d.larghezza_sotto || 700 });
      gsap.set(s, { opacity: 0, y: 12 });
      tl.to(s, { opacity: 1, y: 0, duration: 0.3, ease: 'power3.out' }, v.sotto_t !== undefined ? v.sotto_t : t0 + 0.3);
      if (v.sotto_e !== undefined) tl.to(s, { opacity: 0, duration: ESCE }, v.sotto_e - ESCE);
      alto += (v.righe_sotto || 1) * Math.round((d.corpo_sotto || corpo * 0.62) * 1.2) + 14;
    }
    y += alto + sp;
  });
  tl.to(box, { opacity: 0, x: -60, filter: 'blur(8px)', duration: ESCE, ease: 'power2.in' }, x.e - ESCE);
};

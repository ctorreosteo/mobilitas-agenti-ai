// Titolo di capitolo che passa dietro la persona (fase 7b, nella scena): una o due
// righe enormi a tutta larghezza nello strato `dietro`; il motore le ritaglia con
// la sagoma di lui. Entrano salendo da dietro un bordo fermo, escono in alto.
// d: linee [testo], corpo, y (centro del blocco), allinea (sx|dx: da un lato, a x px dal bordo, come il numero dietro), larghezza_max
// fase 7c: forma 'sito' (default): minuscolo con il punto finale, `chiave` (parole) in gradiente
//   verde -> azzurro (default: l'ultima riga); forma 'maiuscolo' = la versione di YT_POSTURA_32
MODELLI.titolo_dietro = function (box, x, d) {
  const SITO = d.forma !== 'maiuscolo';
  const b = el('div', 'td-blocco' + (d.allinea ? ' td-' + d.allinea : '') + (SITO ? ' td-sito' : ''), box);
  if (d.allinea === 'sx') px(b, { left: d.x || 110, right: 'auto' });
  if (d.allinea === 'dx') px(b, { right: d.x || 110, left: 'auto' });
  px(b, { top: (d.y || 420) - (d.linee.length * (d.corpo || 240) * (SITO ? 0.92 : 0.98)) / 2 });
  const linee = SITO ? d.linee.map((r, k) => {
    let t = r.toLowerCase();
    if (k === d.linee.length - 1 && !/[.!?…]$/.test(t)) t += '.';
    return t;
  }) : d.linee;
  const chiave = SITO ? (d.chiave ? [].concat(d.chiave).map((c) => c.toLowerCase()) : null) : null;
  const spans = linee.map((r, k) => {
    const riga = el('div', 'td-riga', b);
    riga.style.fontSize = (d.corpo || 240) + 'px';
    const s = el('span', '', riga);
    if (!SITO) s.innerHTML = esc(r);
    else if (!chiave) s.innerHTML = k === linee.length - 1 ? `<span class="grad">${esc(r)}</span>` : esc(r);
    else s.innerHTML = r.split(' ').map((w) => chiave.includes(w.replace(/[.,!?…]/g, '')) ? `<span class="grad">${esc(w)}</span>` : esc(w)).join(' ');
    maschera(s);
    gsap.set(s, { yPercent: 135 });
    return s;
  });
  spans.forEach((s, k) => rivela(s, x.s + k * 3 * FR, { dur: 13 * FR }));
  spans.slice().reverse().forEach((s, k) => nascondi(s, x.e - ESCE - k * 2 * FR, { dir: 'su' }));
  // l'ombra larga delle lettere restava in parte dentro la maschera dopo l'uscita (alfa 5%,
  // «residuo» nello strato dietro di dieta e lavoro, fase 7b): a fine titolo si spegne il blocco
  tl.to(b, { opacity: 0, duration: 2 * FR, ease: 'power1.in' }, x.e - 2 * FR);
};

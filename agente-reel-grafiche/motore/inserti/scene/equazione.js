// Equazione detta (campionario v3, reference gadzhi-10 e gadzhi-13): testo piccolo e
// laterale accanto a lui; ogni termine si decifra mentre lui lo dice, gli operatori
// (+, =) sono etichette strutturali verdi; sotto il risultato una barra luminosa cresce a
// scatti con la punta piu chiara. Esce cancellandosi all'indietro, ultima riga per prima.
// d: x, y, righe [{op, testo, t, chiave}], barra {t, larghezza}, t_via, decifra ('minuscole': lettere provvisorie strette)
MODELLI.equazione = function (box, x, d) {
  const g = el('div', 'eq v3-pezzo', box);
  px(g, { left: d.x, top: d.y });
  const vere = [];
  d.righe.forEach((r, i) => {
    const riga = el('div', 'eq-riga', g);
    if (r.op) {
      const op = el('div', 'eq-op', riga, esc(r.op));
      gsap.set(op, { opacity: 0, scale: 0.5 });
      tl.to(op, { opacity: 1, scale: 1, duration: 4 * FR, ease: 'back.out(2)' }, r.t - FR);
      tl.to(op, { opacity: 0, duration: 2 * FR }, d.t_via + (d.righe.length - 1 - i) * 5 * FR);
    }
    const t = el('span', 'eq-t' + (r.chiave ? ' eq-k' : ''), riga);
    const v = decifra(t, r.testo, r.t - FR, 7, 200 + i, undefined, d.decifra);   // d.decifra: 'minuscole' per i termini lunghi
    cancella(t, v, r.testo, d.t_via + (d.righe.length - 1 - i) * 5 * FR, 6);
    vere.push(t);
  });
  if (d.barra) {
    const b = el('div', 'eq-barra', g);
    px(b, { left: 0, top: d.righe.length * 84 + 8, width: d.barra.larghezza || 520 });
    el('div', 'eq-testa', b);
    gsap.set(b, { scaleX: 0, transformOrigin: '0% 50%' });
    // cresce a scatti (gadzhi-13): quattro passi con una pausa breve fra l'uno e l'altro
    [0.3, 0.55, 0.8, 1.0].forEach((v, k) => tl.to(b, { scaleX: v, duration: 3 * FR, ease: 'power2.out' }, d.barra.t + k * 5 * FR));
    tl.to(b, { scaleX: 0, duration: 4 * FR, ease: 'power2.in' }, d.t_via - 2 * FR);
  }
};

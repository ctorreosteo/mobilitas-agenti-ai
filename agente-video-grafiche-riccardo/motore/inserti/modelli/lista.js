// Lista d'attesa in piu tempi: a ogni passo cambia la frase sul pannello; il
// passo "lista" disegna le righe vuote, "primo" accende la prima, "freccia"
// indica in basso, verso la descrizione. DATI: lato, passi [{t, testo, chiave,
// lista, primo, freccia}]
const lato = D.lato || 'dx';
const p = pannello(lato);
muoviPannello(p, lato);
const passi = D.passi || [];
let righe = null;
passi.forEach((ps, i) => {
  const t = Math.max(0.2, ps.t || 0);
  const fine = i + 1 < passi.length ? Math.max(t + 0.5, passi[i + 1].t - 0.12) : T - 0.3;
  const f = el('div', 'frase-passo', p, frase(ps.testo, ps.chiave));
  entra(f, t);
  if (i + 1 < passi.length) esce(f, fine, 0.18);
  if (ps.lista && !righe) {
    righe = el('div', 'lista', p);
    for (let k = 0; k < 5; k++) {
      const r = el('div', 'riga-lista', righe, '<span class="segno"></span><span class="tratto"></span>');
      r.querySelector('.tratto').style.width = (240 + ((k * 97) % 190)) + 'px';
      tl.fromTo(r, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.35, ease: 'power3.out' }, t + 0.25 + k * 0.09);
    }
  }
  if (ps.primo && righe) {
    const r0 = righe.children[0];
    tl.to(r0.querySelector('.segno'), { backgroundColor: '#72FA93', borderColor: '#72FA93', duration: 0.3 }, t + 0.1);
    tl.to(r0.querySelector('.tratto'), { backgroundColor: '#72FA93', duration: 0.3 }, t + 0.1);
    molla(r0, t + 0.1);
  }
  if (ps.freccia) freccia(p, 'freccia', t + 0.1, true);
});
chiudi();

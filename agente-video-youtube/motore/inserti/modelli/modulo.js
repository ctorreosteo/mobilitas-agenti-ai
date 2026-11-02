// Modulo stilizzato: campi vuoti che si evidenziano quando li nomina (nessun
// dato finto). DATI: lato, campi [{t, etichetta}], freccia (true: in basso,
// verso il link in descrizione: il modulo non si compila nel video)
const lato = D.lato || 'dx';
const p = pannello(lato);
muoviPannello(p, lato);
const campi = D.campi || [];
campi.forEach((c, i) => {
  const box = el('div', 'campo', p);
  box.style.top = (260 + i * 230) + 'px';
  el('div', 'lab', box, esc(c.etichetta));
  const b = el('div', 'box', box, '<span class="cursore"></span>');
  entra(box, 0.25 + i * 0.12);
  const t = Math.max(0.3, c.t || 0);
  const fine = i + 1 < campi.length ? Math.max(t + 0.6, campi[i + 1].t) : T - 0.4;
  tl.to(b, { borderColor: 'rgba(114,250,147,0.95)', duration: 0.3 }, t);
  const cur = b.querySelector('.cursore');
  for (let k = 0; t + k * 0.5 < fine; k++) tl.set(cur, { opacity: k % 2 === 0 ? 1 : 0 }, t + k * 0.5);
  tl.set(cur, { opacity: 0 }, fine);
  if (i + 1 < campi.length) tl.to(b, { borderColor: 'rgba(244,244,244,0.22)', duration: 0.3 }, fine);
});
if (D.freccia) freccia(p, 'freccia', 0.6, true);
chiudi();

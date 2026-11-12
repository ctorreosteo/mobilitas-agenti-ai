// Aggancio: la frase d'apertura scritta accanto alla persona, con il logo.
// DATI: lato, righe [{testo, chiave (true = tutta in evidenza), t}]
const lato = D.lato || 'sx';
const p = pannello(lato);
muoviPannello(p, lato);
const lg = logo(p, 300);
entra(lg, 0.15, 12);
const box = el('div', 'righe', p);
(D.righe || []).forEach((r) => {
  const e = el('div', 'riga', box, frase(r.testo, r.chiave));
  entra(e, Math.max(0.18, r.t || 0));
  if (r.chiave) molla(e, Math.max(0.18, r.t || 0) + 0.1);
});
chiudi();

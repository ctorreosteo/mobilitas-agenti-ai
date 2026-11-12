// Inserto di prodotto: prima una scheda con logo e titolo accanto alla persona,
// poi (riduci.t, di solito quando parte il B-roll) la scheda esce e resta
// un'etichetta in un angolo con le voci del percorso, che si accendono quando le
// nomina. DATI: lato, titolo {t, testo, chiave}, etichetta, etichetta_pos
// (basso_sx | basso_dx | alto_sx | alto_dx), voci [{testo, t}], riduci {t}
const lato = D.lato || 'dx';
const rid = Math.max(1.0, (D.riduci && D.riduci.t) || 4);
const p = pannello(lato);
const fuori = lato === 'sx' ? -100 : 100;
if (D.entra !== false) tl.fromTo(p, { xPercent: fuori }, { xPercent: 0, duration: 0.55, ease: 'expo.out' }, 0);
// la scheda e uscita prima dello stacco sul B-roll (che parte ~0,04 s prima della frase)
tl.to(p, { xPercent: fuori, duration: 0.34, ease: 'power2.in' }, rid - 0.5);
const lg = logo(p, 280);
entra(lg, 0.15, 12);
const ti = el('div', 'titolo', p, frase(D.titolo.testo, D.titolo.chiave));
entra(ti, Math.max(0.2, D.titolo.t - 0.05));
molla(ti, Math.max(0.3, D.titolo.t + 0.4));
// etichetta
const box = el('div', 'etichetta-box ' + (D.etichetta_pos || 'basso_sx'));
el('div', 'nome', box, esc(D.etichetta || ''));
tl.fromTo(box, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.45, ease: 'power3.out' }, rid);
(D.voci || []).forEach((v) => {
  const r = el('div', 'voce', box, '<span class="pallino"></span><span>' + esc(v.testo) + '</span>');
  const tv = Math.max(rid + 0.1, v.t);
  tl.to(r, { color: '#F4F4F4', duration: 0.3 }, tv);
  tl.to(r.querySelector('.pallino'), { backgroundColor: '#72FA93', borderColor: '#72FA93', duration: 0.3 }, tv);
  molla(r, tv);
});
tl.to(box, { opacity: 0, duration: 0.3 }, T - 0.32);
chiudi();

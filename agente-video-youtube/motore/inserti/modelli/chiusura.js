// Chiusura in due tempi: pannello accanto alla persona che saluta, poi (pieno.t,
// dopo l'ultima parola) il pannello si allarga a tutto schermo e il blocco di
// testo, a larghezza fissa, scivola al centro. DATI: lato, titolo, voci [{testo}], pieno {t}
const lato = D.lato || 'dx';
const p = pannello(lato);
const fuori = lato === 'sx' ? -100 : 100;
if (D.entra !== false) tl.fromTo(p, { xPercent: fuori }, { xPercent: 0, duration: 0.6, ease: 'expo.out' }, 0);
const t0 = D.entra === false ? 0.0 : 0.25;
const c = el('div', 'cont', p);
const lg = logo(c, 360);
entra(lg, t0, 12);
const ti = el('div', 'titolo', c, frase(D.titolo, true));
entra(ti, t0 + 0.15);
const vv = el('div', 'voci', c, (D.voci || []).map((v) => '<div>' + esc(v.testo) + '</div>').join(''));
entra(vv, t0 + 0.35);
freccia(c, 'freccia', t0 + 0.55, false);
const tp = D.pieno && D.pieno.t ? Math.min(D.pieno.t, T - 0.8) : null;
if (tp !== null) {
  // a fine animazione il pannello parte da x 0 e il blocco (left 96, largo 554) e al centro
  const dx = (1920 - 554) / 2 - 96;
  tl.to(p, { width: 1920, duration: 0.6, ease: 'expo.inOut' }, tp);
  tl.to(c, { x: dx, duration: 0.6, ease: 'expo.inOut' }, tp);
}
chiudi();

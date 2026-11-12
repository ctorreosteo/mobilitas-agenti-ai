// Etichetta di servizio del campionario (non va nei video): il nome della variante
// in alto a sinistra, per confrontare look e versioni.
// d: testo
MODELLI.etichetta = function (box, x, d) {
  const e = el('div', 'et-servizio', box, esc(d.testo));
  gsap.set(e, { opacity: 1 });
};

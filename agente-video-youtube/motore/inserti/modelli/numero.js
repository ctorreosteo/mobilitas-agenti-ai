// Numero vero gigante: sale da 0 al valore detto e resta. DATI: lato, prefisso,
// valore (numero), etichetta, conta {t}: quando lo dice (il conteggio arriva li)
const lato = D.lato || 'dx';
const p = pannello(lato);
muoviPannello(p, lato);
const pre = el('div', 'prefisso', p, esc(D.prefisso || ''));
const v = el('div', 'valore', p, '0');
const et = el('div', 'etichetta', p, esc(D.etichetta || ''));
const fil = el('div', 'filetto', p);
// prefisso e numero entrano insieme quando il pannello si ferma; il conteggio
// parte subito e arriva al valore quando lo pronuncia
const t0 = D.entra === false ? 0.15 : 0.45;
const arrivo = Math.max(t0 + 0.8, ((D.conta && D.conta.t) || 0) + 0.25);
entra(pre, t0 - 0.1);
entra(v, t0 - 0.1, 18);
const c = { n: 0 };
tl.to(c, { n: D.valore, duration: arrivo - t0, ease: 'power2.out',
  onUpdate: () => { v.textContent = Math.round(c.n).toLocaleString('it-IT'); } }, t0);
tl.set(v, { textContent: Number(D.valore).toLocaleString('it-IT') }, arrivo + 0.01);
molla(v, arrivo);
entra(et, arrivo - 0.3);
entra(fil, arrivo - 0.1, 0);
chiudi();

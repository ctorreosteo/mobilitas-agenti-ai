# Controllo qualità

È l'ultimo passo prima della consegna (F8). Si ripete dopo ogni correzione successiva alla revisione finale. Gli esiti si riportano come sono: un controllo fallito si dice, uno saltato si dichiara con il motivo.

**Prima di tutto:** `AG/tools/sito/avvia.sh INC`. Sito in prova su `127.0.0.1`, senza proxy verso il gestionale, più la guardia di rete. Negli script, `/x` è la route della landing. Dopo una duplicazione si passano entrambe le route: `--percorso /originale,/copia`.

## I 12 punti

| # | Controllo | Comando | Soglia |
|---|---|---|---|
| 1 | Errori e rete | `node AG/tools/playwright/cattura.cjs --incarico INC --percorso /x --ambito "<radice della landing>"` | 0 errori JS, 0 risorse del sito non caricate, protezione di prova attiva. Le richieste verso tracciamento e gestionale risultano bloccate: è atteso |
| 2 | Impaginazione a 1440, 390 e 375 | stesso comando, più la lettura delle catture | Nessuno sbordamento orizzontale, un solo H1 |
| 3 | Leggibilità | stesso comando | Nessun testo della landing sotto 14 px; contrasto ≥ 4.5:1 per il corpo e ≥ 3:1 per i testi grandi |
| 4 | Pulsante nella prima schermata | stesso comando | Prenotazione visibile senza scorrere a 390×844 **e** a 375×667 |
| 5 | Bersagli | stesso comando | Bersagli toccabili alti almeno 44 px |
| 6 | Funzioni | `node AG/tools/playwright/controlli.cjs --incarico INC --percorso /x --ambito "<radice>"` | Popup di prenotazione che si apre e, a campi vuoti, non invia nulla; domande frequenti, tastiera, barra mobile, protezione: tutti OK. Le note sul popup condiviso si riportano |
| 7 | Riduci movimento | `cattura.cjs … --riduci-movimento`, più il punto 6 di `controlli.cjs` | Nessuna animazione infinita, nessun contenuto nascosto |
| 8 | Prestazioni | `node AG/tools/playwright/prestazioni.cjs --incarico INC --percorso /x` | Immagini sotto ~1 MB su telefono, nessun fotogramma oltre 33 ms con continuità; confronto con la versione precedente o con l'originale |
| 9 | Design | `AG/tools/impeccable.sh SITO detect --json <file-della-landing>`; provenienza delle foto con `embed-prompt --scan` | Nessun anti-pattern non dichiarato; foto con origine |
| 10 | Compila come in produzione | `AG/tools/sito/build-prova.sh INC` | Build riuscita. L'uscita va nella cartella dell'incarico, mai in `dist/` del sito |
| 11 | Contenuti | Testi della landing confrontati con la tabella «Verifica dei dati» | Ogni dato con la sua fonte, nessuna affermazione inventata |
| 12 | Perimetro e integrità del sito | `node AG/tools/incarico/registro.cjs verifica INC`; dopo una duplicazione anche `git -C SITO diff -U0 <file-di-routing>` | Cambiati solo i file della landing più la sua route; file protetti, file già modificati da altri e originale preservato intatti; nessun commit nuovo |

## Lettura delle catture

Le misure automatiche non bastano. Guarda le catture in `INC/report/screenshot/`:

- prima schermata;
- pagina intera. Per le pagine lunghe usa `node AG/tools/playwright/colonne.cjs <pagina-intera.png> INC/report/colonne.png 4 360`.

Cerca gerarchia, ritmo, foto tagliate male, righe orfane, sovrapposizioni e fasce fisse che coprono troppo su telefono. Se c'è una bozza approvata, affiancala con `confronto.cjs` e dichiara che la fedeltà è giudicata a occhio.

## Limiti da dichiarare sempre

- I test usano l'emulazione dei dispositivi, non telefoni reali.
- Le prestazioni sono misurate sul server di sviluppo.
- **L'invio reale di una prenotazione al gestionale non è verificato.** Nelle prove nessun dato parte, apposta. Va verificato dal titolare con una sua procedura prima della pubblicazione.

L'esito di ogni punto va in `INC/report/consegna.md`, con i numeri, per esempio «Controlli funzionali: 22/22».

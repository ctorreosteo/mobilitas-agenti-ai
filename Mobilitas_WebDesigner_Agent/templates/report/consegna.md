# [Landing]: resoconto ([data])

**Attivazione:** `/webdesigner` — richiesta: «[…]»
**Workflow:** [nuova landing / ottimizzazione / redesign / duplicazione + … / importazione]
**Sito:** `[cartella del sito]` · ramo `[ramo]` · nessun commit fatto
**Route:** `/[percorso]` (in prova: http://localhost:[porta]/[percorso]). Duplicazione: originale `/[…]` invariato.
**Incarico:** `[cartella di lavoro]`

## File nel sito

Esito di `registro.cjs verifica`:

| Stato | File |
|---|---|
| nuovo | `src/pages/[…].jsx` |
| modificato | `src/App.jsx` (solo route e import della landing) |
| nuovo | `public/[landing]/…` |

- File protetti: invariati.
- File già modificati da altri prima dell'incarico: invariati / elenco.
- Originale preservato (duplicazione): sì / no.

## Percorso

| Fase | Esito |
|---|---|
| Verifica dei dati | [offerta, recensioni, sedi; decisioni del titolare] |
| Strategia e copy | `brief/strategia-e-copy.md` |
| Direzione | [direzione scelta e da chi] |
| Bozza visiva | [modello, crediti usati, saldo prima e dopo; oppure «non usata» con il motivo] |
| Costruzione | [file principali] |
| Revisione finale | Giro 1: [fix/ship, n correzioni]. Giro 2: [ship] |

## Integrazioni

- **Popup di prenotazione:** componente del sito, invariato.
- **WhatsApp e tracciamento:** come le altre landing.
- **Prove:** nessun dato inviato. Il server di prova era senza proxy, con la protezione nel browser e la guardia di rete.
- **Da verificare a mano dal titolare:** invio reale di una prenotazione al gestionale.

## Controllo qualità (workflow/controllo-qualita.md)

| # | Controllo | Esito |
|---|---|---|
| 1 | Errori e rete | |
| 2 | Impaginazione a 1440, 390 e 375 | |
| 3 | Leggibilità | |
| 4 | Pulsante nella prima schermata | |
| 5 | Bersagli | |
| 6 | Funzioni | [x/y] |
| 7 | Riduci movimento | |
| 8 | Prestazioni | |
| 9 | Design | |
| 10 | Build di prova | |
| 11 | Contenuti | |
| 12 | Perimetro e integrità del sito | |

**Limiti:**
- emulazione, non telefoni reali;
- prestazioni misurate sul server di sviluppo;
- invio reale non verificato.

## Testi da approvare

1. […]

## Problemi aperti e decisioni per la pubblicazione

1. […] (per esempio tracciamento distinto per la copia, note sui componenti condivisi)

## Screenshot

`report/screenshot/`: [file principali]

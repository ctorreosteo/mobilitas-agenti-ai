# Integrazione Playwright: prove sul sito reale senza inviare dati

Le landing usano le integrazioni reali del sito: popup di prenotazione collegato al gestionale, WhatsApp, tracciamento. Le prove le fotografano e le misurano **senza che nessun dato raggiunga i servizi reali**. Il codice delle landing non contiene simulazioni: le protezioni stanno solo nell'ambiente di prova.

## Installazione

- `playwright-core` 1.64 (tramite `@playwright/cli` 0.1.22) e `@fontsource-variable/montserrat` 5.3.0, installati in locale in `tools/playwright/node_modules` da `tools/setup/installa.sh`. È un'operazione di configurazione, non si fa durante una landing.
- **Browser:** Chrome di sistema (`channel: 'chrome'`). Nessun browser scaricato.

## Le quattro protezioni delle prove

1. **Server di prova del sito** (`tools/sito/avvia.sh` + `vite-prova.sh`). Eredita la configurazione Vite del sito (plugin, alias), ma:
   - ascolta solo su `127.0.0.1` sulla porta dell'incarico, anche se il sito è configurato su `0.0.0.0`;
   - **non ha il proxy** verso il gestionale (`/api`);
   - tiene la cache nella cartella dell'incarico.

   Il file di configurazione di prova sta nella cartella dell'incarico: **nel sito non viene scritto nulla**.
2. **Protezione iniettata nel browser** (`protezione-test.js`, aggiunta da Playwright prima degli script della pagina). Non fa parte della landing.
   - fetch e XMLHttpRequest: solo letture verso la stessa origine e mai `/api/`;
   - sendBeacon e invio nativo dei moduli bloccati;
   - WebSocket solo verso la stessa origine;
   - `fbq`, `gtag`, `clarity` predefiniti come funzioni vuote, quindi il Meta Pixel non si carica.
3. **Guardia di rete** (`guardia-locale.mjs`): unica uscita del browser, anche verso il loopback. Consente solo il server di prova, in GET e HEAD, mai `/api/`. Registro in `INC/runtime/guardia.log`.
4. **Avvio rifiutato** se la guardia non risponde.

Gli script non compilano né inviano moduli. Il controllo del popup lo apre e prova l'invio **a campi vuoti**: verifica la validazione e che non parta nulla.

**Conseguenza:** l'invio reale di una prenotazione al gestionale non è verificabile dalle prove automatiche. Lo verifica il titolare, con una sua procedura, prima della pubblicazione.

## Script

Si lanciano con `node <agente>/tools/playwright/<script>`. Indirizzo e guardia si ricavano da `--incarico INC --percorso /x`. Con più percorsi separati da virgola, ad esempio originale e copia, li prova tutti.

| Script | Cosa fa | Uscita (mai nella cartella dell'agente) |
|---|---|---|
| `cattura.cjs` | Prima schermata e pagina intera a 1440×900, 390×844 e 375×667, con misure: errori, risorse del sito non caricate, sbordamenti, testo < 14 px, bersagli < 44 px, H1, prenotazione nella prima schermata, immagini, font, protezione attiva e tentativi bloccati. Opzioni: `--ambito`, `--riduci-movimento`, `--cta`, `--viewport`, `--prefisso` | `INC/report/screenshot/` |
| `controlli.cjs` | Popup di prenotazione (apertura, invio a vuoto senza invii, note su fuoco ed Esc), domande frequenti, tastiera (nell'`--ambito`), barra mobile, protezione e rete, riduci movimento | `INC/report/controlli-<percorso>.json` |
| `prestazioni.cjs` | LCP, fotogrammi durante lo scorrimento, peso di immagini e script, con confronto tra percorsi | `INC/report/prestazioni.json` |
| `cattura-bozza.cjs` | Catture e misure di una bozza nel visore dell'incarico | `INC/report/screenshot/` |
| `colonne.cjs`, `confronto.cjs` | Pagina lunga in colonne; immagini affiancate con etichetta | percorso indicato |

Strumenti collegati in `tools/sito/`:

- `build-prova.sh`: build di produzione con uscita in `INC/runtime/build`, mai in `dist/` del sito;
- `dipendenze.mjs`: dipendenze, route e integrazioni di una landing.

## Limiti

- Dispositivi emulati in Chrome, non telefoni reali.
- Prestazioni misurate sul server di sviluppo: contano i confronti.
- **Componenti condivisi del sito:** i loro limiti di accessibilità (per esempio un menu senza anello di fuoco) vengono riportati come note, non corretti.
- **Note sul popup:** fuoco ed Esc dipendono dal componente del sito.

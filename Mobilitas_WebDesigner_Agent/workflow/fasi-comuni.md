# Fasi comuni

I workflow usano queste fasi, in quest'ordine. Ognuno indica quali fasi servono e cosa cambia.

**Convenzioni:**
- `AG` = cartella dell'agente, in sola lettura.
- `SITO` = progetto del sito ufficiale.
- `INC` = cartella dell'incarico, nella cartella di lavoro.
- `/x` = percorso (route) della landing.
- ⛔ = punto di arresto: serve una decisione o un'autorizzazione del titolare.

## F0 · Preparazione

1. **Apri l'incarico.**
   ```sh
   AG/tools/incarico/nuovo.sh <nome> [--sito SITO]
   ```
   Lo script registra lo stato Git del sito e le impronte dei file protetti, e assegna le porte. Se elenca file già modificati da altri, non toccarli e dillo all'utente.
2. **Analizza le dipendenze** della landing da modificare o duplicare, oppure, per una landing nuova, della landing esistente più simile, che fa da modello di riferimento:
   ```sh
   node AG/tools/sito/dipendenze.mjs SITO <file-pagina> --json INC/brief/dipendenze.json
   ```
   Ne ricavi:
   - la route attuale;
   - i file esclusivi e quelli condivisi;
   - le foto in `public/`;
   - le integrazioni (popup di prenotazione, WhatsApp, tracciamento);
   - il modo in cui la route viene montata, per esempio dentro `Layout`.
3. **Avvia il sito in prova.**
   ```sh
   AG/tools/sito/avvia.sh INC
   ```
   Il server gira solo su `127.0.0.1`, senza proxy verso il gestionale e con la cache nella cartella dell'incarico. La guardia di rete serve al browser automatico. Se nel sito mancano le dipendenze ⛔: installarle modifica il sito.

## F1 · Dati verificati

1. Cerca nel codice del sito, in sola lettura, offerta, durata, prezzi, numero di recensioni, sedi, telefono e WhatsApp. Usa `grep -rn` su `src/`.
2. Annota ogni dato, con file e riga, nella tabella «Verifica dei dati» di `INC/brief/strategia-e-copy.md` (modello `AG/templates/brief/`). Applica `regole/contenuti-sanitari.md`.
3. Dati discordanti o mancanti ⛔: chiedili tutti insieme, con le varianti trovate e una raccomandazione.
4. Recensioni per tema: cerca negli screenshot del sito con `AG/tools/immagini/ocr.sh`. Usa solo quelle reali.

## F2 · Strategia e copy

Scrivi `INC/brief/strategia-e-copy.md` dal modello:

- pubblico;
- grande idea e promessa senza garanzie;
- testi sezione per sezione;
- formulazioni ammorbidite;
- elenco «Testi da approvare».

Il materiale del titolare è la fonte: accorcia e rendi concreto, senza aggiungere fatti.

## F3 · Direzione artistica

1. **Riferimenti.** Parti da `regole/direzione-estetica.md` e da `AG/riferimenti/taste/`. Se servono riferimenti esterni nuovi, usa `AG/tools/taste/` (mai i domini protetti) e salva le catture in `INC/`.
2. **Tre direzioni radicalmente diverse.** Per ciascuna:
   - idea;
   - prima schermata a 390×844;
   - composizioni;
   - foto;
   - elemento firma;
   - rischi.
3. **Scelta.** Indica la tua scelta motivata e scrivi tutto in `INC/brief/direzione.md` (modello `AG/templates/brief/direzione.md`).
4. **Approvazione** ⛔. Se il titolare ha già indicato la direzione, salta la proposta.
5. **Contratto di direzione** (THESIS, OWN-WORLD, STORY, FIRST VIEWPORT, FORM): resta in `INC/brief/direzione.md`.
   - **File di Impeccable nel sito.** Impeccable può tenere contesto e contratti nel sito (`PRODUCT.md`, `DESIGN.md`, `.impeccable/`). Si creano o si modificano solo se il titolare lo approva ⛔, perché sono file nuovi nel repository.
   - **Senza approvazione:** usa Impeccable con `--target` sul file della pagina e passa il contratto al revisore come documento dell'incarico.

## F4 · Bozza visiva (facoltativa)

Utile per una direzione nuova (nuova landing, redesign).

1. Scrivi il brief testuale in `INC/brief/prompt-superdesign.txt` dal modello: testi esatti, foto come segnaposto `placehold.co`.
2. Chiedi l'autorizzazione con il costo atteso e un tetto ⛔ (`integrazioni/superdesign.md`).
3. Salva la bozza in `INC/bozze/`, localizzala in `INC/visore/` con le foto reali e catturala con `cattura-bozza.cjs`.
4. Mostra le catture al titolare ⛔, se la bozza deve essere approvata.

## F5 · Costruzione nel sito

Lavora solo nel perimetro della landing (`ISTRUZIONI.md`, «Perimetro delle modifiche al sito»).

1. **Struttura come le landing esistenti.** Prendi a modello la landing più simile:
   - come importa il popup di prenotazione;
   - come usa WhatsApp e i dati delle recensioni;
   - come viene montata nel routing.

   Usa gli **stessi componenti condivisi, senza modificarli**.
2. **File nuovi.**
   - Pagina in `sito.cartella_pagine`, ad esempio `src/pages/ReflussoV2.jsx`.
   - Le sezioni proprie, se servono, in una cartella dedicata, ad esempio `src/pages/reflusso-v2/`.
   - Il foglio di stile della landing, partendo da `AG/templates/pagina/stile-landing.css`, scoped su `.pm-scope`.
3. **Testi.** In un unico posto della landing, per esempio un file di contenuti nella sua cartella, con la fonte annotata accanto ai dati.
4. **Foto.** In `public/<nome-landing>/`:
   - ritagli con `AG/tools/immagini/ritagli.sh`, in più larghezze per `srcset`;
   - provenienza incorporata con `AG/tools/impeccable.sh SITO embed-prompt <file> --prompt "<origine e ritaglio>"`;
   - elenco delle fonti in `INC/brief/fonti-foto.txt`.
5. **Route.** Aggiungi una riga di route e il relativo import nel file di routing, montata come le landing simili (stesso wrapper).
6. **Requisiti tecnici:**
   - mobile prima di tutto;
   - un solo H1;
   - pulsante principale nella prima schermata;
   - testo ≥ 14 px;
   - bersagli ≥ 44 px;
   - `MotionConfig reducedMotion="user"` se usi Motion.
7. **Bozza come riferimento.** Rispetta la direzione, ma correggi ciò che nella bozza è sbagliato, come testi inventati o griglie rotte, e dichiaralo.

## F6 · Rifinitura

1. **Impeccable.** Esegui `AG/tools/impeccable.sh SITO detect --json <file-della-landing>` e leggi `AG/skills/impeccable/reference/craft-floor.md` prima di ritoccare l'interfaccia. Correggi i problemi veri e dichiara quelli voluti.
2. **Movimento.** Segui le skill di Emil (`AG/skills/review-animations/SKILL.md`):
   - uscite più rapide delle entrate;
   - `ease-out` per le entrate;
   - solo `transform` e `opacity`;
   - niente testi nascosti in attesa dello scorrimento.
3. **Un giro di misure e catture** a 1440, 390 e 375 (`controllo-qualita.md`, punti 1–5). Correggi tutto in un blocco.

## F7 · Revisione finale

1. Le catture finali vanno in `INC/report/screenshot/`.
2. Esegui la revisione seguendo `AG/agenti/impeccable-finish-reviewer.md`, al massimo 2 giri.
   - Pacchetto: richiesta, contratto, catture, bozza approvata se c'è, risultati del rilevatore.
   - È un passaggio separato e senza modifiche; poi applichi le correzioni.
   - Riporta per intero le dichiarazioni che il revisore richiede.
3. **DESIGN.md del sito:** si aggiorna con `AG/agenti/impeccable-documenter.md` solo se il titolare lo approva ⛔. Altrimenti le note di design della landing vanno in `INC/report/design.md`.

## F8 · Controllo qualità

Segui `workflow/controllo-qualita.md` per intero.

## F9 · Consegna

1. **Verifica dello stato del sito:**
   ```sh
   node AG/tools/incarico/registro.cjs verifica INC
   ```
   Elenca i file cambiati nel sito e controlla che file protetti, file già modificati da altri e originali preservati siano intatti.
2. **Resoconto:** `INC/report/consegna.md`, dal modello `AG/templates/report/consegna.md`.
3. **Messaggio all'utente:**
   - indirizzo di prova;
   - route definitiva;
   - file creati e modificati nel sito;
   - decisioni prese;
   - testi da approvare;
   - problemi aperti;
   - esito dei controlli;
   - crediti usati;
   - cosa resta da verificare a mano, come l'invio reale di una prenotazione.
4. `AG/tools/sito/ferma.sh INC`, a meno che l'utente debba guardare la pagina.
5. Commit e pubblicazione li decide il titolare: non proporli come passo automatico.

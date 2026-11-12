# Versione 1.1 — 12/11/2026

**Agente Video Grafiche (Riccardo)**: lo stesso agente della 1.0, che ora lavora sui video **verticali 9:16** e sugli
**orizzontali 16:9**, con un nome nuovo e una regola nuova fra laboratorio e produzione.

## Cosa cambia

- **Formato orizzontale 16:9 (1920×1080)**, nato l'11 e il 12/11/2026 lavorando `VSL_BRUXISMO_AI_01` e `VSL_CERVICALGIA_AI_01`
  (consegnati) nella copia condivisa. Quelle modifiche, fuori da ogni commit, sono state portate qui tutte (14 file, diff
  identico byte per byte; l'elenco con gli hash è in `laboratorio/portate-1.1.txt`, solo nel laboratorio):
  - il formato sta in `videos/<slug>/reel.json` («formato», lo scrive `reel-init` dal video); `./mve` lo legge prima di
    caricare il motore (`reel_comune.FORMATI`: misure, zona sicura; `C.mini()` per miniature e fogli «telefono»);
  - zona sicura del 16:9: margine del 5% per lato, testi in x 96–1823, y 54–1025 (Riccardo, 11/11/2026: visto a tutto schermo);
  - radiografia con gli schemi delle finestre O1 (una larga) e O2 (due quadrate), fogli girati, punti del fondo e griglia
    delle zone in proporzione; pagina HyperFrames e `reel_dom.mjs` sul quadro del video (il verticale resta identico byte per
    byte);
  - forme del 16:9: «pannello a lato» e «finestra larga»; reference orizzontali (`gadzhi-NN`, `martell-NN`) valide nei 16:9;
    una reference vale con la sua scheda anche senza il video;
  - due controlli nuovi del piano (per tutti i formati): firma Servier dentro la zona sicura; ombra «alto» troppo vicina a una
    riga di sottotitolo (`OMBRA_ALTO_PX`);
  - `infografica_reel.js`: la barra «spento» ora si abbassa davvero (il gradiente copriva il colore);
  - lezioni nella skill: tempi negativi nei pezzi (fotogrammi di video scoperto), anelli con `"icona": "tabler:circle"`;
  - coda: un video di un altro formato fa le sue tappe in un `./mve` a parte.
  Regressione del verticale (`./mve reel-regressione`, 12/11/2026): **OK**, il verticale non cambia.
- **Nome nuovo.** Nome visibile: **Agente Video Grafiche (Riccardo)**. Il laboratorio è
  `_Laboratorio/agente-video-grafiche-riccardo-lab` (prima `~/Mobilitas_ClaudeCode_System/03_Agente_Reel_Grafiche`), la copia
  di produzione `~/mobilitas-agenti-ai/agente-video-grafiche-riccardo` (prima `agente-reel-grafiche`): stessi nomi
  dell'agente video YouTube, il laboratorio ha solo `-lab` in più. **I nomi interni restano**: comandi `./mve reel-*`, skill
  `mobilitas-reel`, direttore `direttore-reel`, file del motore `reel_*.py`, i nomi dei modelli e lo storico
  `libreria/uso-modelli-reel.json`. «Reel» resta il nome interno di qualsiasi video che l'agente lavora.
- **Laboratorio e produzione** (regola in `CLAUDE.md` e nella skill): nel laboratorio solo migliorie e correzioni; i video
  si fanno nella copia di produzione, dove l'agente non modifica mai i propri file. La riconosce dalla radice git (non è la
  sua cartella); se un video richiede una modifica scrive «Serve una modifica all'agente: va fatta nel laboratorio.».
- **Esportazione nuova** (`./esporta-nel-repository.sh`, solo nel laboratorio; spiegazione in `laboratorio/ESPORTAZIONE.md`):
  esporta i file del laboratorio come sono adesso, senza commit nel laboratorio; prima cancellava e ricreava tutta la cartella di destinazione (si sarebbero persi video, consegne e installazione); ora
  aggiorna solo i file dell'agente, non tocca mai il lavoro e l'installazione (md5 controllato prima e dopo), avvisa se c'è un
  video non consegnato, si ferma se in produzione c'è una modifica non salvata, e una volta sola sposta inbox, video,
  consegne, report e storico dalla cartella vecchia `agente-reel-grafiche` alla nuova. Copia anche, con conferma, i video
  finiti dei laboratori nelle consegne di produzione.
- **Storico unito**: `libreria/uso-modelli-reel.json` del laboratorio ha ora tutti i 9 video fatti (7 del laboratorio e
  dell'agente ads, più le 2 VSL); l'esportazione aggiunge allo storico di produzione quelli che mancano.
- `LEGGIMI.md`: sezione «Aggiornamento alla 1.1» per i collaboratori.

## Da fare (1.1)

- **Prova fissa per il 16:9**: la regressione ha solo il caso verticale. Proposta nel report del 12/11/2026 (da una delle due
  VSL approvate), da decidere con Riccardo.

# Versione 1.0 — 07/11/2026 (agente reel-grafiche)

Prima versione dell'agente reel-grafiche di @Studio_Mobilitas, uscita dal laboratorio di Riccardo dopo il test sul frontman
`AD_CERV_26` (stile, forme e sottotitoli approvati il 07/11/2026). Sta accanto all'agente video YouTube, che resta com'è: è
una cartella diversa, con una copia propria del motore.

## Cosa sa fare

- **Aggiunge grafiche e infografiche a qualsiasi reel verticale 9:16 già montato**: ads con le finestre (voce AI, B-roll in
  finestre, animazioni 3D), ads con una persona in camera (anche in movimento), reel MOFU, reel con solo B-roll; con o senza
  sottotitoli impressi, con o senza SRT (senza SRT legge i sottotitoli con Apple Vision e li conferma con whisper).
- **Tappa 0, studio delle reference**: prima di ogni reel controlla `libreria/reference/`; le reference nuove si rinominano e
  si studiano (scheda, ritmo, catalogo, linguaggio) prima di partire. `reel-init` si ferma finché resta qualcosa da studiare.
- **Radiografia generica**: tagli, inquadrature, finestre, persona fotogramma per fotogramma (volti, teste, mani, sagoma),
  sottotitoli impressi, scritte del video, zone libere, voce.
- **Il sistema di forme** (modello `palco-fascia-alta`, attivo dal 09/11/2026): stile fisso approvato e forme scelte per inquadratura
  (pannello sotto il volto, fascia alta, badge, pannello al posto di una finestra; brevi: tendina a tutto schermo, schermo
  diviso, card di vetro), con oggetti che si trasformano, indicatore di struttura, disegni Servier.
- **Sottotitoli impressi mai toccati**: un controllo automatico (`reel_sottotitoli.py`) blocca il render se la fascia di un
  sottotitolo non è identica all'originale o coperta del tutto.
- **Controlli automatici**: audio identico (md5) e prova degli effetti sonori, video uguale fuori dalle grafiche, zona sicura
  Meta, lettere intere, cifre non dette (pagina e Apple Vision), solo parole dette, zoom, sovrapposizioni e 3D.
- **Direttore artistico cieco** (subagente `direttore-reel`), al massimo due giri, con la tavola scena ↔ reference.
- **Anteprima per Riccardo** (con e senza effetti sonori, affiancato, tavola) e **consegna** come copia del file approvato
  (md5), anche in `consegne/`.
- **Prova veloce** di una grafica: `./mve reel-prova`.
- **Regressione**: `./mve reel-regressione` sul caso fisso AD_CERVICALGIA.

Strumenti, uguali all'agente video YouTube: ffmpeg, whisper.cpp con il modello large-v3, Python 3.12 (pillow 13.0.0, numpy
2.5.4, fonttools 4.67.0, brotli 1.2.1), Node, HyperFrames 0.8.204, Apple Vision (swiftc). Libreria: disegni Servier Medical Art
(CC BY 4.0), 19 effetti sonori Pixabay, logo, 42 reference (31 orizzontali, 11 verticali) con schede e ritmo, icone Tabler
3.49.0 (MIT).

## Storia (dal laboratorio)

- **03/11/2026, fase 0**: il laboratorio nasce come copia del laboratorio YouTube; radiografia del primo ad
  (AD_CERVICALGIA_AI-Barontini).
- **03–04/11, fasi 1–3**: le prime grafiche degli ads con le finestre (etichette barrate, card dei 3 motivi, equazione, card
  dell'obiettivo, chiusura con il prezzo); modi «finestra» e «tutto schermo»; grafiche agganciate alla voce, non ai sottotitoli.
- **04/11, fase 4**: l'agente ripetibile (comandi `ads-*`, stato, coda, approvazioni legate all'md5, consegna come copia);
  varietà fra gli ads; testi accorciati senza cambiare il senso; «pensato per»; mai «il tuo» + disturbo.
- **04/11, fase 5**: varianti «in prova», render con la GPU in un processo, regressione. Consegnati AD_CERVICALGIA,
  AD_REFLUSSO, AD_EMICRANIA, AD_BRUXISMO, AD_COLON.
- **05/11, fase 6**: l'agente diventa «reel-grafiche» (comandi `reel-*`): qualsiasi reel 9:16, radiografia generica,
  procedura «studio reference», zoom leggeri, effetti sonori con la versione senza effetti. Giro 3: densità «piena» con
  micro-grafiche (copertura 85%, una novità ogni 3 s). Giro 4: solo infografiche vere (niente grafiche di solo testo), icone
  Tabler, niente fermata sul piano.
- **06/11, giro 5**: le grafiche si appoggiano sul video; estetica con profondità; logo intero al posto del pittogramma; test
  sul frontman.
- **07/11, mattina**: «un palco per reel» dallo studio delle 11 reference verticali; tolte copertura 85% e novità ogni 2–3 s.
  Provato il video abbassato con le lettere dei sottotitoli rimesse: vietato la sera stessa.
- **07/11, sera**: stile del frontman approvato; sottotitoli mai toccati (controllo che blocca il render); più forme invece di
  un pannello solo.
- **07/11, notte**: ultimi ritocchi del frontman (offerta, disegno Servier del sistema nervoso); tappa 0 obbligatoria per le
  reference; comando `reel-prova`; uscita dal laboratorio (questa cartella).
- **08/11/2026, nome definitivo** (prima del primo commit): tolto il vecchio nome «agente ads», l'agente si chiama
  agente reel-grafiche. Restano solo i comandi `./mve reel-*`: tolti gli alias `ads-*` e, dall'elenco di `./mve`, i comandi
  dell'agente video YouTube (i loro moduli restano nel motore, perché i reel ne usano alcuni). Il file di ogni reel
  `ads.json` diventa `reel.json`; lo storico `libreria/uso-modelli-ads.json` diventa `libreria/uso-modelli-reel.json` (stesso
  contenuto); il caso della regressione passa da `campionario/regressione/ads/` a `campionario/regressione/reel/`. File del
  motore rinominati senza cambiare quello che fanno: `ads.py` → `reel_grafiche.py`, `ads_comune.py` → `reel_comune.py`,
  `ads_flusso.py` → `reel_flusso.py`, `ads_piano.py` → `reel_piano_base.py`, `ads_radiografia.py` →
  `reel_radiografia_base.py`, `ads_regressione.py` → `reel_regressione.py`, `ads_rendi.py` → `reel_rendi.py`,
  `ads_dom.mjs` → `reel_dom.mjs`; la classe dell'attribuzione Servier nei modelli `ads-attr` → `reel-attr`. I nomi dei
  modelli (`etichette_ads`, `card_accese_ads`…) restano quelli del catalogo. Report: `report/2026-11-08-nome-reel-grafiche.md`.
- **09/11/2026, primo reel consegnato** (`REEL_MOFU_CERVICALGIA_TEST`). `reel-stato` non chiede più un giro 3 del direttore:
  una grafica ritoccata dopo il giro 2 («non rivotata») la decide Riccardo sull'anteprima, come i voti rimasti sotto 7.
  Con l'ok di Riccardo diventano attivi nel catalogo il sistema di forme (`palco-fascia-alta`) e gli effetti sonori
  (`effetti-sonori-reel`); nella skill, la nota sui segni vuoti letti «0» e sull'icona `send` letta «7».

## Regole superate (non valgono più)

- Copertura del reel ≥ 85% e una novità ogni 2–3 s: tolte il 07/11 (restano solo come informazione nella mappa del ritmo).
- Densità «piena» con micro-grafiche sopra il video e modelli sulla persona (titolo dietro, frase sul corpo, card vicino alle
  mani, lui nel cerchio): sostituiti dal sistema di forme; i modelli restano nel catalogo «in prova» ma non si usano.
- «Un palco per reel» con un pannello solo: diventato il sistema a più forme.
- Video abbassato in una finestra con i sottotitoli rimessi al loro posto: vietato (07/11 sera), codice tolto.
- Fermata sul piano: tolta il 05/11 (ci si ferma sull'anteprima).

## Da fare

- **Card vuote dell'emicrania** (AD_EMICRANIA_AI-Agazzi, grafica dei 3 motivi, consegnata con voto 6 accettato da Riccardo):
  le card con spessore restano in attesa senza segnaposto finché arriva la cifra con la frase. Da correggere con un segnaposto
  estetico se il reel si rifà. Manca anche il controllo automatico «testo dentro la card» (nel giro 2 una frase era tagliata
  dal bordo: l'aveva visto il direttore, non il motore).
- **Logo che sembra un «7»**: il pittogramma da solo e la T stilizzata della scritta MOBILITAS, piccoli, a 390 px si leggono
  «7» («MOBILI7AS»). Si usa il logo intero e grande; da decidere con Riccardo una versione del logo per i reel.
- **Regressione YouTube non fattibile qui**: la regressione dei modelli 16:9 condivisi (`./mve regressione tutti`) è un
  comando dell'agente video YouTube e ha bisogno del video `YT_POSTURA_32`; in questa cartella non c'è più. Le modifiche ai
  file condivisi (`brand.json` e simili) vanno provate nell'agente video YouTube.
- Modelli «in prova» da approvare: le infografiche e gli zoom. Il sistema di forme (`palco-fascia-alta`) e gli effetti sonori
  sono attivi dal 09/11/2026.

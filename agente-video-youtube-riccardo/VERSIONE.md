# Versione 1.1 — 11/11/2026

**Cambio di nome.** La cartella si chiama `agente-video-youtube-riccardo` (prima
`agente-video-youtube`). Il laboratorio da cui arriva si chiama
`agente-video-youtube-riccardo-lab`: stessi nomi, il laboratorio ha solo `-lab` in
più. Il motore, i modelli e le regole non cambiano.

- Nomi aggiornati in `CLAUDE.md`, `LEGGIMI.md`, `INSTALLAZIONE.md`, `installa.sh`,
  nei tre subagenti (`.claude/agents/`) e nella skill `mobilitas-grafica`
  (`references/pipeline.md`).
- **`installa.sh`**: se accanto c'è ancora la vecchia `agente-video-youtube`, chiede
  «Sposto B-roll, inbox e video nella cartella nuova? [s/N]» e sposta tutto quello
  che git ignora (B-roll con indice, `inbox/`, `videos/`, `uso-modelli.json`, musica,
  modello whisper, HyperFrames installato), tranne `.venv` e `.lavoro`. Non
  sovrascrive e non cancella niente; nei video spostati riscrive sulla cartella
  nuova il collegamento al girato e i percorsi nei `.json` del motore, conservando
  le date dei file (`./mve stato` non chiede di rifare fasi). Alla fine dice che la
  vecchia cartella si può cestinare.
- **`installa.sh`**: un `.venv` creato in un'altra cartella si riconosce
  (`.venv/pyvenv.cfg`) e si ricrea con gli stessi pacchetti
  (`motore/requirements.lock`), dopo una conferma.

Provata l'11/11/2026 su una copia finta (percorso con spazio e apostrofo): 15
elementi spostati, un doppione e un file personale lasciati e segnalati, girato e
materiali raggiungibili dal video spostato, date dei file invariate.

# Versione 1.0.1 — 02/11/2026

**Correzione di `installa.sh`.** Nella prova finale di 30 secondi la voce sintetica
non partiva: la frase da leggere contiene un apostrofo («dell'agente») e lo script
la passava dentro un `eval` fra apostrofi, che si rompevano (`unmatched '`). Senza
`voce.wav` fallivano anche trascrizione e video: 3 controlli su 5.

- Ogni controllo della prova ora è una funzione, con testi e percorsi passati come
  argomenti: niente `eval` su testo libero (vale anche per una cartella con un
  apostrofo nel nome).
- La prova dice quanti controlli sono riusciti («5 controlli su 5»).
- Nuovo: `./installa.sh --prova` rifà solo la prova, senza controllare né
  installare niente.

Provata il 02/11/2026 su un M3 Max: 5 controlli su 5 in 14 s. Il resto della v1.0
(qui sotto) non cambia.

# Versione 1.0 — 02/11/2026

Prima versione per i collaboratori dell'agente video YouTube di @Studio_Mobilitas.
Viene dal laboratorio di Riccardo, dopo i video di prova YT_POSTURA_32 (YouTube,
6:50) e MR_POSTURA_01_v4 (mid-roll, 1:52), approvati da Riccardo.

Sta accanto a `agente-video-editing` (l'agente di Carlos), che resta com'è: è una
cartella diversa, con un motore che si è sviluppato a parte.

## Cosa contiene

- **Il motore** (`mve`, `motore/motore/`): dal girato al video consegnato, con
  la grafica dentro la scena.
- **Le grafiche HyperFrames**: modelli e scene (`motore/inserti/`), versione
  fissata **0.8.204** (`package.json` e `package-lock.json`, senza `node_modules`:
  li installa `installa.sh`).
- **Il catalogo dei modelli**: tutti i **55**, ognuno con il suo stato: **32
  attivi, 20 varianti, 3 vietati**, con descrizione, condizioni d'uso, voto e un
  fotogramma d'esempio (`motore/inserti/CATALOGO-MODELLI.md`).
- **Il brand** (`motore/motore/brand.json`) e il **linguaggio grafico**
  (`libreria/reference/linguaggio-grafico.md`, con il catalogo delle reference in
  `libreria/reference/catalogo.md`).
- **Le skill e i subagenti** (`.claude/`): regia, montaggio, grafica, stile;
  cacciatore di papere, regista, revisore visivo; le skill HyperFrames della
  versione fissata.
- **La libreria comune**: logo e pittogramma, i disegni anatomici di Servier
  Medical Art (con attribuzione), i 19 effetti sonori Pixabay (con crediti).
- **I permessi** (`.claude/settings.json`), uguali al laboratorio: chiede prima di
  installare e prima di `rm -r`; vietati `git commit`, `git push`, `sudo` e la
  cancellazione di `inbox/`.
- **Documenti**: `LEGGIMI.md` (come si usa), `INSTALLAZIONE.md` e `installa.sh`,
  questo file.

### Novità del motore in questa versione

- `init` legge `inbox/<NOME>/info.txt` (nome dell'osteopata, tipo di video) e
  dice cosa manca.
- **Consegna per tipo**: YouTube = video, SRT e `youtube.txt`; mid-roll = video e
  SRT; sempre `validazione-animazioni.md` da far firmare a un osteopata (anche
  `./mve validazione <NOME>`).
- **Anteprima da approvare**: `./mve finale <NOME> --anteprima` scrive anche
  `controlli/anteprima-momenti.md` e `.jpg` (i momenti con tempi, modelli e parole
  a schermo, più i punti da decidere).
- **`tempi.md`**: ogni fase scrive la sua durata e lo spazio disco usato.
- **Meno lavori in parallelo con poca RAM** (misure: whisper 3,9 GB, una grafica
  3,3 GB); `MVE_LAVORI=1` per forzare un lavoro alla volta.
- `./mve stato` senza nome: video, cartelle di `inbox/`, strumenti, RAM, disco,
  B-roll da catalogare. `./mve catalogo` senza nome.
- Il modello whisper si cerca anche in `.modelli/` (dove lo mette `installa.sh`).
- La libreria B-roll vuota non blocca niente; le clip nuove si contano e si
  catalogano al primo uso.

## Cosa non contiene, e perché

| cosa | perché |
|---|---|
| i video di prova, i report, i campionari, gli esempi di non regressione | sono il lavoro del laboratorio: pesano decine di GB e contengono il girato. `./mve regressione` e `./mve campionario` si usano solo in laboratorio |
| le foto dei pazienti e i fotogrammi che le contengono | privacy: le foto non escono dal Mac in cui sono state messe. Nel catalogo dei modelli 3 esempi mostravano una foto di un paziente (`inserto-primadopo`, `prima-dopo-cursore`, `foto-card`): ora hanno un'immagine neutra |
| il B-roll del laboratorio | ogni collaboratore mette il suo; contiene persone riprese con un consenso dato per il laboratorio. Per prudenza anche i 2 esempi del catalogo con persone svestite durante un trattamento (`b-roll`, `inserto-prodotto`) hanno un'immagine neutra |
| i video delle reference (Iman Gadzhi, Dan Martell) | sono registrazioni dello schermo di altri canali, solo per studio: non si distribuiscono. Restano il catalogo scritto e il linguaggio grafico |
| musica | serve una licenza: ognuno mette i suoi brani |
| `node_modules`, `.venv`, il browser di render, il modello whisper (3,1 GB) | si installano sul Mac con `installa.sh` |
| `.lavoro/`, `.cache/` | spazio di lavoro e programmi compilati: si rigenerano |

Nella cartella i contenuti di `libreria/broll`, `prima-dopo`, `musica`, di
`inbox/` e di `videos/` restano sul Mac di chi li mette: il repository tiene solo
i loro `LEGGIMI.md` (vedi `.gitignore`).

## Le versioni successive

Modelli grafici nuovi, reference nuove e correzioni del motore si sviluppano e si
provano in laboratorio e arrivano con una versione nuova, che **aggiunge senza
togliere**: nessun modello si cancella o si declassa senza l'ok di Riccardo.

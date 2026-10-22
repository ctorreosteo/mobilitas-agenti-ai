# Agente WebDesigner Mobilitas

Sistema per creare, migliorare, ridisegnare, **duplicare** e importare le landing del **sito ufficiale** Mobilitas. Usa il metodo messo a punto in laboratorio: copy a risposta diretta con prudenza sanitaria, direzione artistica, bozza visiva facoltativa, verifiche visive e funzionali.

**Tre regole di fondo:**

- **Si attiva solo su richiesta esplicita:** `/webdesigner <richiesta>`. Senza comando, Cursor lavora normalmente.
- **Le landing stanno solo nel sito ufficiale**, con i suoi componenti, il routing, le foto e le integrazioni reali (popup di prenotazione collegato al gestionale).
- **Questa cartella è in sola lettura durante il lavoro.** Contiene istruzioni, workflow, skill, strumenti e configurazione. I risultati vanno in una cartella di lavoro esterna.

## Esempi

```
/webdesigner crea una landing da zero per la fisioterapia sportiva
/webdesigner migliora la landing del reflusso
/webdesigner duplica la landing del reflusso e usa il WebDesigner per migliorarla
/webdesigner rifai completamente il design della landing cervicalgia
/webdesigner importa questa landing e ottimizzala: <file>
```

## Contenuto

```
Mobilitas_WebDesigner_Agent/
├── ISTRUZIONI.md            Istruzioni dell'agente (fonte unica). Nessuno strumento lo carica da solo
├── README.md · THIRD_PARTY_NOTICES.md · licenze/
├── config/                  mobilitas.example.json → mobilitas.json (locale)
├── workflow/                fasi-comuni, nuova-landing, ottimizzazione, redesign, duplicazione, importazione, controllo-qualita
├── regole/                  sicurezza, contenuti-sanitari, direzione-estetica
├── integrazioni/            cursor-e-claude-code, playwright, superdesign, skill-e-dipendenze
├── skills/                  impeccable, taste, 6 skill di Emil Kowalski (non registrate: si leggono dopo l'attivazione)
├── agenti/                  revisore finale e documentatore di Impeccable (passaggi separati)
├── templates/
│   ├── collegamento/        skill di richiamo «webdesigner» (varianti comando e nominato)
│   ├── pagina/              foglio di stile base della landing, font Montserrat facoltativi
│   ├── brief/ · report/ · incarico/
├── tools/
│   ├── incarico/            apertura dell'incarico e registro dello stato del sito
│   ├── sito/                server di prova, build di prova, dipendenze di una landing, impronta
│   ├── playwright/          catture, controlli, prestazioni, protezione di prova, guardia di rete
│   ├── superdesign/ · taste/ · immagini/ · impeccable.sh
│   ├── setup/               installa, collega (Cursor/Claude Code), proteggi (sola lettura), manifesto
│   └── lib/                 configurazione
├── riferimenti/taste/       analisi di siti di riferimento
└── test/                    verifica, funzionamento, sito reale, attivazione in Claude Code
```

## Installazione

È un'operazione di configurazione, non si fa durante il lavoro sulle landing.

```sh
cd Mobilitas_WebDesigner_Agent
tools/setup/installa.sh          # pacchetti locali dal registro npm (accesso esterno); --cache-offline <cache> senza rete
test/verifica-installazione.sh   # controllo statico
test/test-funzionamento.sh       # prove locali complete, senza rete né crediti
```

Niente installazioni globali e nessuna modifica a `~/.cursor`, `~/.claude` o al sistema. Requisiti:

- macOS su Apple Silicon (verificato su 27.0.1);
- Node 18+;
- Google Chrome;
- python3, git, rsync, curl.

Per i dettagli vedi `integrazioni/skill-e-dipendenze.md`.

## Configurazione: `config/mobilitas.json`

| Chiave | A cosa serve | Se vuoto |
|---|---|---|
| `sito.cartella` | Progetto del sito ufficiale | L'agente usa la cartella del sito aperta nel workspace e la conferma con l'utente |
| `sito.file_da_non_modificare`, `sito.componenti_condivisi`, `sito.file_routing`, `sito.cartella_pagine` | Perimetro e struttura del sito | Valori predefiniti del sito attuale |
| `lavoro.cartella` | Cartella di lavoro esterna, una sottocartella per incarico, più `.stato/` con cache, log e credenziali Superdesign | `~/Mobilitas_WebDesigner_Lavori` |
| `documentazione.cartella`, `brand.cartella` | Documentazione aziendale, risorse del brand (solo lettura) | Codice del sito e `regole/direzione-estetica.md` |
| `integrazioni.superdesign.abilitato` | Bozze visive a crediti, sempre con autorizzazione | Disattivato |
| `porte` | Porte locali di server di prova, guardia, visore | — |
| `domini_protetti` | Domini di produzione (sito, hosting, backend, webhook) che la guardia non visita mai, sottodomini compresi | Nessun dominio protetto. Nell'esempio `backend-esempio.invalid` è un segnaposto: in `config/mobilitas.json` va sostituito con il dominio reale del backend |

## Collegamento a Cursor (non ancora installato)

Cursor carica skill, regole e `AGENTS.md` **solo dalla radice** delle cartelle del workspace. Per questo il pacchetto non contiene nulla che si attivi da solo. Il richiamo avviene con una skill `webdesigner` (`disable-model-invocation: true`) da installare in **una** di queste posizioni:

- la radice del sito;
- la radice della cartella degli agenti aziendali;
- la cartella personale `~/.cursor/skills`.

```sh
tools/setup/collega.sh --dove <radice>            # prova: mostra cosa farebbe
tools/setup/collega.sh --dove <radice> --scrivi   # installa (con autorizzazione)
```

Vantaggi e svantaggi delle tre posizioni, verifiche fatte e variante «nominato»: `integrazioni/cursor-e-claude-code.md`.

## Sicurezza in breve

- **Nel sito:** solo i file della landing, la sua route e le sue foto. Mai componenti condivisi, popup di prenotazione, API, credenziali, tracciamento, dipendenze o altre landing senza autorizzazione.
- **Git e pubblicazione:** nessun commit, push o deploy. A fine lavoro l'agente elenca i file cambiati.
- **Prove:** sul sito vero ma **senza inviare dati**. Server di prova senza proxy verso il gestionale, protezione nel browser, guardia di rete. L'invio reale di una prenotazione lo verifica il titolare.
- **Crediti Superdesign:** solo con autorizzazione e tetto.
- **Cartella dell'agente:** sola lettura. Per renderla tale anche sul disco: `tools/setup/proteggi.sh on`.

Il testo completo è in `regole/sicurezza.md`.

## Spostare la cartella

1. Copia escludendo le parti locali:
   ```sh
   rsync -a --exclude node_modules --exclude config/mobilitas.json Mobilitas_WebDesigner_Agent/ <destinazione>/Mobilitas_WebDesigner_Agent/
   ```
2. Nella nuova posizione:
   - esegui `tools/setup/installa.sh`;
   - compila `config/mobilitas.json`;
   - esegui `test/verifica-installazione.sh`;
   - se vuoi, proteggi la cartella con `tools/setup/proteggi.sh on`.
3. Se la skill di richiamo è stata installata con `--percorso-assoluto`, reinstallala. Senza quell'opzione trova da sola la cartella fra quelle del workspace.

Credenziali e risultati non stanno nella cartella dell'agente: restano in `lavoro.cartella`.

## Test

Vedi `test/LEGGIMI.md`.

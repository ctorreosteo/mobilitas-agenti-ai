# Agente dev HQ — sviluppo del gestionale Mobilitas

Agente che porta un task ClickUp da una riga di titolo a codice revisionato, su frontend e backend del gestionale, **senza mai committare**.

## Come si usa

```bash
cd /Users/carlitos/mobilitas-agenti-ai/mobilitas-agente-dev-hq
claude
```

Poi:

> Lavora i task di oggi

L'orchestratore parte da solo. In alternativa, `/dev-hq-orchestratore`.

I due repo del gestionale sono già dichiarati come directory aggiuntive in `.claude/settings.json`: l'agente lavora da qui e scrive lì.

## Le cinque fasi

| Fase | Cosa succede | Si ferma? |
|------|--------------|-----------|
| 1 | Legge i task con scadenza **oggi**; se non ce ne sono, prende gli **scaduti** dal più vecchio | No |
| 2 | Scrive il **piano d'azione**, lo fa revisionare, corregge finché è approvato | No — nessuna approvazione umana |
| 3 | Sviluppa su frontend e backend | No |
| 4 | **Ciclo revisione → correzione**, finché i nove revisori approvano al 100% | No |
| 5 | **Allinea la documentazione** sul codice ormai definitivo | No |
| 6 | Scrive il report in `report/` e lo stampa. **Nessun commit** | Fine |

Un task alla volta, sequenziale. **Non si ferma mai a chiederti niente:** se non trova task in scadenza chiude la sessione con un riepilogo, e se un ciclo si impunta applica il protocollo di uscita qui sotto.

### Il ciclo della Fase 4

```
        ┌──────────────────────────────┐
        ▼                              │
  4A · i 9 revisori in parallelo       │
      (SOLA LETTURA, non toccano nulla)│
        │                              │
        ├── zero ERRORE ──▶ Fase 5     │
        │                              │
        └── almeno un ERRORE           │
                │                      │
                ▼                      │
  4B · sviluppo correttivo ────────────┘
      (l'unico che scrive)
```

I revisori **non correggono**: producono un referto. A correggere è un passaggio di sviluppo separato. Si gira finché **tutti e nove** tornano con zero ERRORE sullo stesso stato del codice.

### Se il ciclo non converge, esce da solo

**L'agente non ti chiede mai di sbloccarlo.** Se il ciclo si impunta — stesso rilievo due volte, un rilievo risolto che riappare, il conto degli ERRORE che non scende, o **5 giri** raggiunti — scatta un protocollo automatico:

1. **Una gerarchia decide i conflitti.** `sicurezza` → `logica` → `regressioni`/`impatto` → `ux` → `performance` → `estetico` → `documentazione`. Vince chi sta più in alto; il rilievo dell'altro viene declassato a DUBBIO con scritto perché. Un ERRORE di sicurezza non si declassa mai.
2. **Sceglie una delle tre uscite**, in base a chi ha sollevato il rilievo rimasto:

| Uscita | Quando | Risultato |
|---|---|---|
| **A — Consegna con riserva** | UX, performance, estetico, doc | Consegna, dichiarando cosa resta aperto. **Il caso normale** |
| **B — Consegna parziale** | Logica/regressioni, se isolabile | Annulla solo quel pezzo, consegna il resto |
| **C — Abbandono protetto** | Sicurezza, o problema non isolabile | Salva la patch, ripristina, task non consegnato |

3. **Passa al task successivo.** Uno stallo non ferma la giornata.

Tutto finisce nel report, in evidenza: uscita usata, rilievo rimasto, regola applicata, **rischio residuo in una frase**.

**Quando annulla, non tocca il tuo lavoro:** all'inizio registra quali file erano già modificati, salva sempre una patch in `/tmp/dev-hq-abbandonati/`, e ripristina solo i file che ha scritto lui. Senza quella registrazione, annullare gli è vietato.

## Gli undici revisori

Nessuno di loro modifica un file: producono referti. Ogni rilievo è **ERRORE** (blocca l'avanzamento) o **DUBBIO** (si valuta e si motiva).

Sono disposti su tre momenti: **uno prima** dello sviluppo, **nove durante**, **uno dopo**.

### Prima dello sviluppo — Fase 2

| Revisore | Guarda |
|----------|--------|
| `revisore-piano` | Che il piano abbia capito il task, prima che diventi codice |

È il più economico del sistema: legge mezza pagina e intercetta il fraintendimento finché costa una frase.

### Nel ciclo — Fase 4

Girano in parallelo, un subagent ciascuno, sullo stesso diff. Sono indipendenti: nessuno vede i rilievi degli altri.

| Revisore | Guarda | Gira su |
|----------|--------|---------|
| `revisore-estetico` | Colori nei **tre** temi, riuso delle primitive | FE |
| `revisore-ux` | Che il flusso si possa usare davvero | FE |
| `revisore-logica-frontend` | Che il codice React faccia ciò che il task chiedeva | FE |
| `revisore-logica-backend` | Che il codice Java faccia ciò che il task chiedeva | BE |
| `revisore-performance-frontend` | Refetch, chiamate nei cicli, liste non paginate | FE |
| `revisore-performance-backend` | N+1, query senza limite, lavoro in memoria | BE |
| `revisore-sicurezza` | Audit clinico, permessi, PII nei log, GDPR | FE + BE |
| `revisore-regressioni` | Chi chiamava ciò che è cambiato — **un salto** | FE + BE |
| `revisore-impatto-sistemico` | Effetti a **più salti**, incoerenze, invarianti | FE + BE |

**Nove non costano nove.** Sei girano su un repo solo: un task di solo backend ne fa chiudere quattro in una riga. E ogni revisore chiude subito quando la materia non lo riguarda — un cambio di CSS non impegna performance.

### Dopo il ciclo — Fase 5

| Revisore | Guarda | Gira su |
|----------|--------|---------|
| `revisore-documentazione` | Cataloghi e contratti resi falsi dal diff | FE + BE |

Gira **da solo, alla fine**, sul codice ormai definitivo. Dentro il ciclo avrebbe fatto riscrivere i cataloghi a ogni giro inseguendo un codice che cambiava sotto. E siccome le sue correzioni toccano solo file `.md`, **non possono rompere ciò che i nove hanno approvato**: è l'unica cosa che si può sistemare dopo il 100% senza rimetterlo in discussione.

**Regressioni ≠ impatto sistemico.** Il primo parte dai simboli cambiati e cerca i chiamanti: **un salto**, meccanico. Il secondo parte dai concetti e percorre i flussi end-to-end: **molti salti**, semantico. Uno trova ciò che non compila più; l'altro ciò che compila benissimo e ha smesso di avere senso.

## Struttura

```
report/                            i report, uno per task + riepilogo giornaliero
.claude/
  settings.json                    permessi; git commit/push negati
  skills/
    dev-hq-orchestratore/          il workflow
      references/
        clickup.md                 API, token, campi
        mappa-gestionale.md        i due repo
        piano-azione.md            come si scrive il piano
        ricetta-enum.md            aggiungere un valore a un enum senza dimenticare pezzi
        diff-completo.md           il diff da dare ai revisori (git diff non basta)
        verifiche.md               i gate, il confronto con la baseline, il database
        stallo.md                  come esce da solo se il ciclo si impunta
    revisore-piano/                gira in Fase 2, prima dello sviluppo
    revisore-estetico/
      references/design-system.md  i tre temi, le 29 primitives
    revisore-ux/
    revisore-logica-frontend/
    revisore-logica-backend/
    revisore-performance-frontend/
    revisore-performance-backend/
    revisore-sicurezza/
      references/impianto-privacy.md  GDPR, audit clinico, RBAC
    revisore-regressioni/
    revisore-impatto-sistemico/
    revisore-documentazione/
docs/
  workflow-sviluppo.md             il workflow per esteso
```

## Dove finisce il lavoro

L'agente **non committa e non scrive su ClickUp**, quindi la sola traccia di cosa ha fatto è quella che produce lui:

| File | Contiene |
|---|---|
| `report/<data>-<task-id>.md` | Il report del task: cosa ha fatto, come verificarlo, cosa resta aperto |
| `report/<data>-<task-id>-piano.md` | Il piano su cui ha lavorato |
| `report/<data>-riepilogo.md` | La giornata in una tabella: task, esiti, decisioni che aspettano te |

Se ha abbandonato del lavoro, lì accanto trovi anche la patch e l'archivio dei file nuovi, per recuperarlo.

Il report va **sempre su file, non solo a schermo**: l'agente lavora in autonomia su più task di seguito, e il terminale scorre. Senza il file, i report dei primi task sparirebbero prima che tu li legga.

## Lezioni dalla prima esecuzione

L'agente è stato corretto sulla base del primo task vero (869cng430, «Aggiungere visita rimandata»). Le quattro cose che ha imparato:

| Problema trovato | Correzione |
|---|---|
| **`git diff` non mostra i file nuovi né le modifiche in staging** — sul task reale restituiva **0 righe** mentre il lavoro c'era tutto: i revisori avrebbero approvato il vuoto | Il diff si costruisce con `git diff HEAD` più il contenuto dei file `??` — [diff-completo.md](.claude/skills/dev-hq-orchestratore/references/diff-completo.md) |
| **`cd` fra due repo fa leggere quello sbagliato**, senza errori. È successo due volte | Regola: `git -C <path>`, mai `cd`; subshell per `npm` e `./mvnw` |
| **Il confronto con la baseline per numero di riga** dava 3 errori nuovi, **2 dei quali falsi** | Si confronta per testo (typecheck) e per regola (lint) |
| **I task "aggiungi un valore a un enum" dimenticano pezzi** — il vincolo `CHECK` a database avrebbe rotto la feature **solo in produzione** | [ricetta-enum.md](.claude/skills/dev-hq-orchestratore/references/ricetta-enum.md): l'elenco dei posti da toccare, la verifica del vincolo, la migrazione Flyway |

Ha anche scoperto che **il database è interrogabile** (`docker exec postgres psql`): serve a verificare i vincoli prima di scrivere il piano, e a provare le migrazioni in una transazione da annullare.

## Tre cose da sapere prima di usarlo

**La scadenza di oggi è quasi sempre vuota.** Nella lista HQ solo 3 task su 100 hanno una scadenza. Il filtro "oggi" tornerà quasi sempre zero: allora l'agente ripiega sui task **scaduti e ancora aperti**, dal più vecchio. Se non ce ne sono nemmeno di quelli, chiude la sessione con un riepilogo — non lavora mai un task senza scadenza di sua iniziativa, perché sceglierne uno a caso fra cento è lavoro buttato. Se vuoi che lavori un task preciso, **mettigli una scadenza su ClickUp.**

**I task sono titoli.** 6 descrizioni su 100, nessuna priorità, nessun tag. Per questo la Fase 2 esiste ed è la più importante: è dove il titolo diventa un intervento definito, leggendo il codice.

**Non ci sono test automatici, e i gate del frontend sono già rossi.** Zero test nel backend, Vitest non cablato nel frontend. Su albero pulito `npm run typecheck` dà **318 errori** e `npm run lint` **894 problemi**: debito pregresso, non regressioni. Per questo l'agente fotografa la linea di base *prima* di sviluppare e poi confronta — contano solo gli errori nuovi. Il backend invece compila pulito, quindi lì ogni errore è del diff.

## Vincoli

- **Mai commit, push, branch.** Negati anche a livello di permessi.
- **Su ClickUp si legge soltanto.** Nessuna scrittura, nessun cambio di stato.
- **Il token ClickUp non si stampa e non si copia** in file o report. Vive in `mobilitas-backend/src/main/resources/application-local.properties`.

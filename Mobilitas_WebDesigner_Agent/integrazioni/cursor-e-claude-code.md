# Cursor e Claude Code: attivazione esplicita del WebDesigner

## Architettura di lavoro

In Cursor un **workspace con due cartelle**:

1. il **sito ufficiale** Mobilitas, cioè la destinazione delle landing;
2. la cartella degli **agenti aziendali**, che contiene `Mobilitas_WebDesigner_Agent/`.

Il WebDesigner deve attivarsi **solo su richiesta esplicita**. Senza richiesta, Cursor lavora normalmente.

## Cosa ho verificato nel codice di Cursor 3.23.23 (20/10/2026)

L'ho verificato leggendo il codice dell'app installata (runtime dell'agente e workbench). Non è stato un test interattivo.

| Comportamento | Cosa fa Cursor | Conseguenza per il WebDesigner |
|---|---|---|
| Skill di progetto | Per **ogni** cartella del workspace cerca le skill in `<radice>/.cursor/skills`, `<radice>/.agents/skills` e, con le estensioni di terze parti attive (impostazione predefinita), anche `<radice>/.claude/skills`, `.codex/skills`, `.grok/skills`. Solo nella **radice** della cartella, non nelle sottocartelle | Una skill dentro `AGENTI/Mobilitas_WebDesigner_Agent/…` **non viene caricata**. Va installata nella radice di una cartella del workspace o nella cartella personale `~/.cursor/skills` |
| `disable-model-invocation: true` | Le skill con questa opzione vengono **escluse dall'elenco che il modello vede**: si usano solo quando l'utente le richiama con il comando `/nome` | È il meccanismo di attivazione esplicita, nativo e deterministico |
| `AGENTS.md` | Quello nella radice di ogni cartella del workspace è una regola **sempre attiva**. Quelli nelle sottocartelle sono riconosciuti come regole della sottocartella | Il pacchetto **non contiene più** `AGENTS.md`: le istruzioni stanno in `ISTRUZIONI.md`, che nessuno strumento carica da solo |
| `CLAUDE.md`, `CLAUDE.local.md` | Trattati come `AGENTS.md` quando sono attive le estensioni di terze parti | Il pacchetto **non contiene più** `CLAUDE.md` |
| `.cursor/rules` | Letto nella radice di ogni cartella del workspace | Il pacchetto **non contiene più** regole |

Il workspace con più cartelle, da solo, non basta. Aprire la cartella degli agenti non attiva il WebDesigner, ed è quello che si vuole. Serve però una skill di richiamo installata in una radice.

## Il pacchetto non si attiva da solo

- Niente `AGENTS.md`, `CLAUDE.md`, `.cursor/` o `.claude/` nel pacchetto. La verifica dell'installazione lo controlla (punto G).
- Skill e agenti stanno in `skills/` e `agenti/`, cartelle normali che nessuno strumento esplora. Vengono letti solo dopo l'attivazione, seguendo `ISTRUZIONI.md`.
- La skill Impeccable, la cui descrizione si attiverebbe su qualunque lavoro di interfaccia, non è registrata: non può attivarsi da sola su una landing.

## Meccanismo di richiamo: la skill `webdesigner`

È un unico file, `SKILL.md`, con due varianti in `templates/collegamento/`.

| Variante | Come si attiva | Affidabilità | Rischio di attivazione non voluta |
|---|---|---|---|
| **`comando`** (consigliata) | Solo con `/webdesigner <richiesta>` nella chat di Cursor (`disable-model-invocation: true`) | Deterministica: è l'utente a richiamarla | Nessuno: il modello non la vede |
| `nominato` | Con `/webdesigner` **oppure** quando il messaggio nomina il WebDesigner a parole («usa l'agente WebDesigner…») | Dipende dal modello, che decide in base alla descrizione | Basso ma non nullo |

Con la variante `comando`, una frase come «Usa l'agente WebDesigner per migliorare la landing del reflusso» **senza** `/webdesigner` non è garantita: il modello non conosce la skill. Va scritta come `/webdesigner migliora la landing del reflusso`. Cursor completa il comando mentre si digita.

La skill si limita a trovare la cartella dell'agente e a far leggere `ISTRUZIONI.md`. Tutto il resto, cioè workflow, regole e strumenti, sta nel pacchetto. Aggiornare il pacchetto quindi non richiede di reinstallarla.

### Dove installarla: scegline una sola

| Posizione | Vantaggi | Svantaggi |
|---|---|---|
| **Radice del sito**: `<sito>/.cursor/skills/webdesigner/` | Nativa; vale per tutti quelli che aprono il sito; si può versionare con il sito | È un file nuovo nel repository del sito, da approvare e da salvare in Git (decisione del titolare) |
| **Radice della cartella degli agenti**: `<AGENTI>/.cursor/skills/webdesigner/` | Non tocca il sito; funziona quando la cartella degli agenti è aperta nel workspace | Aggiunge una cartella `.cursor/` nella directory degli agenti, condivisa con gli altri agenti: da concordare |
| **Personale**: `~/.cursor/skills/webdesigner/` | Non tocca né il sito né la cartella degli agenti; vale in ogni progetto della persona | Configurazione personale per ciascun collaboratore; da installare su ogni computer |

**Installazione** (non ancora eseguita), dalla cartella dell'agente:

```sh
tools/setup/collega.sh --dove <radice-scelta>                  # PROVA: mostra destinazione e contenuto, non scrive
tools/setup/collega.sh --dove <radice-scelta> --scrivi         # installa la variante «comando» per Cursor
#   opzioni: --variante nominato · --strumento claude (per .claude/skills) · --percorso-assoluto (per l'installazione personale)
```

**Dopo l'installazione:** riapri la finestra di Cursor e controlla in Impostazioni → Rules/Skills che compaia `webdesigner`. Poi prova le richieste della lista in `test/LEGGIMI.md`.

### Due cartelle nel workspace: cosa deve essere aperto

- **Il sito:** sempre, perché è la destinazione.
- **La cartella degli agenti:** consigliata. La skill trova `Mobilitas_WebDesigner_Agent` fra le cartelle del workspace e l'agente di Cursor può leggerne i file. Se non è aperta, serve `--percorso-assoluto` all'installazione, ma l'accesso a file fuori dal workspace dipende dai permessi dell'agente di Cursor: **non verificato**.

## Claude Code

Claude Code ha lo stesso meccanismo: le skill con `disable-model-invocation: true` si richiamano solo con `/webdesigner`.

- **Dove:** si installa in `<radice>/.claude/skills/webdesigner/` oppure in `~/.claude/skills/webdesigner/` (`collega.sh --strumento claude`).
- **Attenzione:** Cursor legge anche `.claude/skills`. Non installare entrambe le varianti nella stessa radice, altrimenti in Cursor comparirebbero due skill `webdesigner`.
- **Prova:** ho verificato questo meccanismo in Claude Code con una sessione pulita (`test/test-attivazione-claude.sh`). In Cursor non è stato possibile provarlo, perché manca un'interfaccia a riga di comando.

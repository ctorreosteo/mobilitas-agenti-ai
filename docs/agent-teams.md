# Orchestrare team di sessioni Claude Code

> Coordinare più istanze di Claude Code che lavorano insieme come un team, con
> attività condivise, messaggistica tra agenti e gestione centralizzata.

**Indice completo della documentazione:** https://code.claude.com/docs/llms.txt
(usare questo file per scoprire tutte le pagine disponibili prima di esplorare oltre)

> ⚠️ **Sperimentale, disabilitato di default.** Abilitare con
> `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` in `settings.json` o nell'ambiente.
> Senza quella variabile, nessun team viene configurato all'avvio della sessione.

I team di agenti permettono di coordinare più istanze di Claude Code. Una sessione
è il **team lead** (coordina il lavoro, assegna attività, sintetizza i risultati).
I **compagni di team** lavorano indipendentemente, ognuno nel proprio context window,
e comunicano direttamente tra loro. A differenza dei subagents (che riferiscono solo
al main agent), puoi interagire direttamente con i singoli compagni di team.

> Documentazione a partire da v2.1.178. Con `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`
> impostato, generare un compagno di team non richiede più un passaggio di
> configurazione, e la pulizia avviene automaticamente all'uscita della sessione.
> I tool `TeamCreate`/`TeamDelete` non esistono più. `team_name` sul tool Agent è
> accettato ma ignorato; il campo `team_name` negli hook payload è deprecato.

## Quando utilizzare i team di agenti

Più efficaci per attività in cui l'esplorazione parallela aggiunge valore reale:

* **Ricerca e revisione**: più compagni investigano aspetti diversi, poi condividono
  e mettono in discussione i risultati reciproci.
* **Nuovi moduli o funzionalità**: ognuno possiede un pezzo separato senza interferire.
* **Debug con ipotesi concorrenti**: testano teorie diverse in parallelo e convergono.
* **Coordinamento tra livelli**: frontend, backend, test, ciascuno posseduto da uno.

Aggiungono overhead di coordinamento e usano molti più token di una singola sessione.
Per attività sequenziali, modifiche dello stesso file o lavoro con molte dipendenze,
una singola sessione o i subagents sono più efficaci.

### Confronto con i subagents

|                    | Subagents                                            | Team di agenti                                    |
| :----------------- | :--------------------------------------------------- | :------------------------------------------------ |
| **Context**        | Proprio; i risultati tornano al chiamante            | Proprio; completamente indipendente               |
| **Comunicazione**  | Riportano i risultati solo al main agent             | I compagni si messaggiano direttamente            |
| **Coordinamento**  | Il main agent gestisce tutto il lavoro               | Elenco di attività condiviso con auto-coordinamento |
| **Migliore per**   | Attività focalizzate dove conta solo il risultato    | Lavoro complesso che richiede discussione         |
| **Costo in token** | Inferiore: risultati sintetizzati nel contesto       | Superiore: ogni compagno è un'istanza separata    |

Subagents = worker veloci e focalizzati che riportano indietro. Team = compagni che
devono condividere risultati, mettersi in discussione e coordinarsi autonomamente.

## Abilitare i team di agenti

```json
// settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Avviare il primo team di agenti

Descrivi il compito e i compagni desiderati in linguaggio naturale. Esempio:

```text
Sto progettando uno strumento CLI che aiuta gli sviluppatori a tracciare i commenti
TODO nel loro codebase. Genera tre compagni di team per esplorare questo da diversi
angoli: uno su UX, uno su architettura tecnica, uno che gioca l'avvocato del diavolo.
```

Claude popola un elenco di attività condiviso, genera i compagni, li fa esplorare e
sintetizza i risultati. Il terminale del lead elenca i compagni nel pannello agente:

* **Frecce su/giù**: selezionare un compagno di team
* **Invio**: aprire la trascrizione del compagno e messaggiarlo direttamente
* **Escape**: interrompere il turno corrente del compagno selezionato

Dalla v2.1.199 la riga di un compagno inattivo resta finché qualsiasi compagno o
subagente lavora ancora. Quando tutti gli agenti sono inattivi, le righe inattive si
nascondono dopo 30s e riappaiono al turno successivo (il compagno resta indirizzabile).
Con >3 compagni inattivi, le righe oltre le prime tre si comprimono in una riga tipo
`2 idle agents`; selezionala + Invio per espandere, Esc per comprimere.

## Controllare il team di agenti

### Scegliere una modalità di visualizzazione

* **In-process** (default): tutti i compagni nel terminale principale. Frecce su/giù
  per selezionare, Invio per visualizzare, digita per messaggiare. Funziona in qualsiasi
  terminale, nessuna configurazione extra.
* **Split panes**: ogni compagno nel proprio riquadro. Richiede tmux o iTerm2.

Default `"in-process"`. `"auto"` abilita split panes dentro tmux o iTerm2 con CLI `it2`,
altrimenti in-process. `"tmux"` abilita split-pane e rileva tmux/iTerm2. Dalla v2.1.186
`"iterm2"` usa split panes nativi iTerm2 (richiede CLI `it2`).

```json
// ~/.claude/settings.json
{ "teammateMode": "auto" }
```

```bash
claude --teammate-mode auto
```

> `tmux -CC` in iTerm2 è il punto di ingresso suggerito in tmux. Per iTerm2: installa
> la CLI `it2` e abilita l'API Python in iTerm2 → Settings → General → Magic.

### Specificare compagni di team e modelli

```text
Spawn 4 teammates to refactor these modules in parallel. Use Sonnet for each teammate.
```

I compagni **non** ereditano la selezione `/model` del lead di default. Imposta
**Default teammate model** in `/config` (scegli **Default (leader's model)** per seguirlo).
Dalla v2.1.186 i compagni ereditano il livello di sforzo del lead.

### Richiedere l'approvazione del piano per i compagni di team

```text
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

Il compagno lavora in modalità piano di sola lettura finché il lead approva. Se rifiutato,
rivede in base al feedback e riinvia. Il lead decide autonomamente; per influenzarlo dai
criteri nel prompt (es. "approva solo piani con copertura test").

### Parlare direttamente con i compagni di team

Ogni compagno è una sessione Claude Code completa e indipendente.

* **In-process**: frecce su/giù per selezionare, Invio per visualizzare, digita per
  messaggiare. `x` sul compagno selezionato per fermarlo. Ctrl+T per l'elenco attività.
* **Split-pane**: clicca nel riquadro per interagire.

Mentre visualizzi un compagno in-process, testo semplice e skills vanno a lui, ma i
comandi integrati vengono eseguiti nella sessione del lead. Modello e fast mode sono
fissi alla generazione: `/model` e `/fast` cambiano solo il lead (dalla v2.1.199 mostra
un avviso). `/effort` si applica comunque ai turni successivi del compagno visualizzato.

### Assegnare e rivendicare attività

Stati attività: **in sospeso**, **in corso**, **completate**. Le attività possono
dipendere da altre (una in sospeso con dipendenze non risolte non può essere rivendicata).

* **Il lead assegna**: gli dici quale attività a quale compagno.
* **Auto-rivendicazione**: dopo aver completato, un compagno raccoglie la prossima
  attività non assegnata e non bloccata.

La rivendicazione usa file locking per prevenire race condition.

### Spegnere i compagni di team

```text
Ask the researcher teammate to shut down
```

Il compagno può approvare (uscita graceful) o rifiutare con spiegazione. Le directory
condivise del team vengono pulite automaticamente all'uscita della sessione.

### Applicare quality gate con hooks

* `TeammateIdle`: quando un compagno sta per andare inattivo. Exit code 2 → feedback,
  lo mantiene al lavoro.
* `TaskCreated`: quando un'attività sta per essere creata. Exit code 2 → previene + feedback.
* `TaskCompleted`: quando un'attività sta per essere completata. Exit code 2 → previene + feedback.

## Come funzionano i team di agenti

### Come Claude avvia i team

Il team si forma quando il primo compagno viene generato (sessione principale = lead):

* **Tu richiedi compagni**: dai un compito adatto al parallelo e chiedi compagni esplicitamente.
* **Claude propone compagni**: suggerisce di generarli; tu confermi prima che proceda.

Claude non genera compagni senza la tua approvazione.

### Architettura

| Componente             | Ruolo                                                              |
| :--------------------- | :----------------------------------------------------------------- |
| **Team lead**          | Sessione principale che genera compagni e coordina il lavoro       |
| **Compagni di team**   | Istanze Claude Code separate che lavorano su attività assegnate    |
| **Elenco di attività** | Elenco condiviso che i compagni rivendicano e completano           |
| **Mailbox**            | Sistema di messaggistica per comunicazione tra agenti              |

Mailbox = file JSON in `~/.claude/teams/{team-name}/inboxes/{agent-name}.json`. Claude
Code convalida ogni voce; voci malformate vengono segnalate come errori e rimosse, i
messaggi validi consegnati. (Prima della v2.1.207 una voce malformata bloccava la
consegna con errore ripetuto ogni secondo.)

Le dipendenze delle attività sono gestite automaticamente: al completamento di un'attività,
le attività bloccate si sbloccano.

Nome del team derivato dalla sessione: `session-` + primi 8 caratteri dell'ID sessione.

* **Config team**: `~/.claude/teams/{team-name}/config.json` (rimossa a fine sessione)
* **Elenco attività**: `~/.claude/tasks/{team-name}/` (persiste; sessioni riprese
  mantengono le attività; conservazione governata da `cleanupPeriodDays`)

⚠️ Non modificare `config.json` manualmente né pre-autorizzarlo: contiene stato di runtime
(ID sessione, ID riquadri tmux) sovrascritto ad ogni aggiornamento. Non esiste equivalente
a livello di progetto (`.claude/teams/teams.json` è trattato come file ordinario).
L'array `members` in config contiene nome, ID agente e tipo di ogni compagno.

### Utilizzare definizioni di subagent per i compagni di team

Puoi riferire un tipo di subagent (progetto, utente, plugin, CLI) alla generazione:

```text
Genera un compagno di team utilizzando il tipo di agente security-reviewer per
controllare il modulo di autenticazione.
```

Il compagno onora `tools` allowlist e `model` della definizione; il corpo si aggiunge al
system prompt (non lo sostituisce). Gli strumenti di coordinamento (`SendMessage`, gestione
attività) sono sempre disponibili anche se `tools` limita altri strumenti.

> I campi frontmatter `skills` e `mcpServers` di una definizione subagent **non** si
> applicano quando eseguita come compagno di team: i compagni caricano skills e MCP
> server dalle impostazioni progetto/utente, come una sessione regolare.

### Permessi

I compagni iniziano con le impostazioni di permesso del lead (incluso
`--dangerously-skip-permissions`). Dopo la generazione puoi cambiare le modalità dei
singoli compagni, ma non impostarle per-compagno alla generazione.

Con `SendMessage`, il ricevente è informato che il messaggio proviene da un'altra sessione
Claude, non da te. Un compagno non può approvare un prompt di permesso per tuo conto né
aggirare un diniego inoltrandolo. In modalità auto, un'approvazione inoltrata è trattata
come input non attendibile. I prompt di permesso risalgono al lead (approvi lì).
L'approvazione del piano è l'eccezione: il lead la concede senza prompt separato per te.

### Context e comunicazione

Ogni compagno ha il proprio context window. Alla generazione carica lo stesso contesto di
progetto di una sessione regolare (CLAUDE.md, MCP server, skills) + il prompt di generazione.
La cronologia della conversazione del lead **non** viene trasferita.

* **Consegna automatica dei messaggi**: consegnati automaticamente ai destinatari; il lead
  non fa polling.
* **Notifiche di inattività**: al termine, il compagno notifica automaticamente il lead.
  Dalla v2.1.198 un compagno la cui sessione termina per errore API notifica l'errore
  invece di sembrare terminare normalmente.
* **Elenco attività condiviso**: tutti vedono lo stato e rivendicano il lavoro disponibile.
* **Messaggistica**: invia a un compagno per nome; per tutti, un messaggio per destinatario.

Il lead assegna un nome a ogni compagno alla generazione. Per nomi prevedibili, dì al lead
come chiamarli nell'istruzione di generazione.

### Utilizzo dei token

I team usano molti più token: ogni compagno ha il proprio context window e l'uso scala con
il numero di compagni attivi. Per ricerca/revisione/nuove funzionalità di solito ne vale
la pena; per routine, una singola sessione è più conveniente.

## Esempi di casi d'uso

### Revisione del codice parallela

```text
Spawn three teammates to review PR #142:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

### Investigare con ipotesi concorrenti

```text
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

La struttura del dibattito combatte l'ancoraggio: con più investigatori indipendenti che
cercano di confutarsi, la teoria che sopravvive è più probabilmente la causa reale.

## Best practices

* **Fornire contesto sufficiente**: i compagni caricano il contesto di progetto ma non la
  cronologia del lead. Includi i dettagli dell'attività nel prompt di generazione.
* **Dimensione del team appropriata**: inizia con **3-5 compagni**. Costi token scalano
  linearmente; l'overhead di coordinamento aumenta; rendimenti decrescenti. Tre focalizzati
  spesso superano cinque dispersi.
* **Dimensionare le attività**: né troppo piccole (overhead > beneficio) né troppo grandi
  (troppo lavoro senza check-in). Giuste = unità auto-contenute con deliverable chiaro.
  Punta a **5-6 attività per compagno**.
* **Aspettare che finiscano**: se il lead inizia a implementare invece di delegare:
  `Aspetta che i tuoi compagni di team completino le loro attività prima di procedere`.
* **Iniziare con ricerca e revisione**: compiti con confini chiari senza scrivere codice.
* **Evitare conflitti di file**: ogni compagno possiede un set diverso di file.
* **Monitorare e sterzare**: controlla il progresso, reindirizza approcci che non funzionano,
  sintetizza i risultati man mano.

## Troubleshooting

* **Compagni non appaiono**: in-process appaiono nel pannello agente (frecce su/giù +
  Invio). Una riga sparita dopo inattività è nascosta, non interrotta (messaggiala per
  nome per riportarla). Verifica che il compito sia abbastanza complesso. Per split panes:
  `which tmux`; per iTerm2 verifica CLI `it2` + API Python.
* **Troppi prompt di permesso**: pre-approva le operazioni comuni nelle impostazioni di
  permesso prima di generare i compagni.
* **Compagni si fermano su errori**: selezionali (Invio in-process / clic in split), dai
  istruzioni aggiuntive o genera un sostituto. Dalla v2.1.198 un messaggio dal lead o da un
  compagno riattiva un compagno in-process in attesa di retry API (riprova subito).
* **Lead si spegne prima del completamento**: digli di continuare; o di aspettare i compagni
  prima di procedere.
* **Sessioni tmux orfane**: `tmux ls` poi `tmux kill-session -t <session-name>`.

## Limitazioni (sperimentale)

* **Nessuna ripresa sessione con compagni in-process**: `/resume` e `/rewind` non li
  ripristinano. Dopo il resume, di' al lead di generare nuovi compagni.
* **Lo stato dell'attività può ritardare**: a volte non vengono marcate completate,
  bloccando le dipendenti. Aggiorna manualmente o spingi il compagno.
* **L'arresto può essere lento**: finiscono la richiesta/tool call corrente prima di spegnersi.
* **Un team per sessione**, limitato a quella sessione. Niente team denominati aggiuntivi.
* **Nessun team annidato**: i compagni non possono generare propri compagni. Solo il lead.
* **Nessun subagent in background da compagni in-process**: i loro subagent girano in
  primo piano; `run_in_background` o `background: true` restituisce errore.
* **Il lead è fisso** per tutta la durata. Niente promozione/trasferimento di leadership.
* **Permessi impostati alla generazione**: tutti partono con la modalità del lead.
* **Split panes richiedono tmux o iTerm2**: non supportati nel terminale integrato di
  VS Code, Windows Terminal o Ghostty.

> **`CLAUDE.md` funziona normalmente**: i compagni leggono i `CLAUDE.md` dalla loro
> directory di lavoro. Usalo per guida specifica del progetto a tutti i compagni.

## Prossimi passi / approcci correlati

* **Subagents** (delega leggera): agenti helper per ricerca/verifica nella tua sessione.
* **Git worktrees** (sessioni parallele manuali): più sessioni Claude Code senza
  coordinamento automatico.
* **Confronto subagent vs agent team**: vedi features-overview per una suddivisione.

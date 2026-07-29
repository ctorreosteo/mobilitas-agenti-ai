# agente-gdpr — Conformità GDPR di MobilitasHQ

Agente Claude Code che **recupera** backend e frontend del gestionale MobilitasHQ,
ne verifica la conformità al GDPR, **aggiorna la documentazione Markdown** perché sia a norma
e **segnala in un file MD separato** tutto ciò che manca da implementare.

> **Non modifica in alcun modo il codice.** Solo file `.md` e report. Un hook di sicurezza
> blocca a livello di harness qualsiasi scrittura su file di codice.

---

## Avvio rapido

```bash
cd /Users/carlitos/mobilitas-agenti-ai/agente-gdpr
claude
```

> L'agente va avviato **da questa cartella**: hook, permessi, skill e subagenti sono
> definiti in `agente-gdpr/.claude/` e non vengono caricati se apri Claude Code dalla
> cartella padre.

Poi, in sessione:

```
/sync              # clona/aggiorna backend e frontend in workspace/
/audit             # analizza il codice ed estrae le evidenze privacy
/aggiorna-docs     # allinea e mette a norma i .md del gestionale
/report            # scrive report/CRITICITA-GDPR.md
```

Oppure tutto in una volta:

```
/tutto
```

---

## Struttura

```
agente-gdpr/
├── CLAUDE.md                 # istruzioni permanenti dell'agente (regole + metodo)
├── config/repos.json         # quali repo recuperare e come
├── scripts/
│   ├── sync-repos.sh         # clone/fetch dei repo nel workspace (mai distruttivo)
│   └── test-hooks.py         # verifica che le protezioni siano attive
├── workspace/                # copie di lavoro (git-ignored) — SOLA LETTURA tranne i .md
│   ├── mobilitas-backend/
│   └── mobilitas-frontend/
├── report/
│   ├── CRITICITA-GDPR.md     # ⬅ output principale: cosa manca da implementare
│   └── evidenze/             # tracce grezze dell'audit (file:riga)
└── .claude/
    ├── settings.json         # permessi + hook di protezione del codice
    ├── hooks/                # blocca-modifiche-codice.py · blocca-bash-pericoloso.py
    ├── skills/               # competenze GDPR e di metodo
    ├── agents/               # subagenti (audit BE/FE, redazione, revisione)
    └── commands/             # /sync /audit /aggiorna-docs /report /tutto
```

## Cosa recupera

Da `config/repos.json` (modificabile):

| Repo | Ruolo | Origine |
|------|-------|---------|
| `mobilitas-backend` | backend gestionale (Java 21 / Spring Boot / PostgreSQL) | `https://github.com/ctorreosteo/mobilitas.git` |
| `mobilitas-frontend` | frontend gestionale (React + Vite + TS) | `https://github.com/ctorreosteo/mobilitas-frontend.git` |

Modalità di recupero, in `config/repos.json` → `mode`:

| Modalità | Cosa fa | Quando usarla |
|----------|---------|---------------|
| `local-git` **(default)** | `git clone` dal repo locale: copia indipendente con storia git, **originale mai toccato**, nessuna credenziale richiesta | uso normale |
| `remote` | `git clone` da GitHub | da un'altra macchina o per lavorare sull'ultimo `origin/main`; i repo sono **privati**, serve autenticazione (chiave SSH o `gh auth login`) |
| `local-copy` | snapshot `rsync` della working tree | quando vuoi auditare anche le **modifiche non ancora committate** |

In `local-git` l'audit analizza lo **stato committato**: se il repo di origine ha modifiche
pendenti, lo script te lo dice.

Il sync è **idempotente e non distruttivo**: se la copia di lavoro ha modifiche non committate,
lo script le elenca e si ferma su quel repo invece di sovrascriverle. In `local-copy` il nuovo
snapshot viene portato sul branch di documentazione con un merge, così i `.md` già scritti
restano; un eventuale conflitto viene segnalato e il merge annullato.

## Come arrivano nei tuoi repo le modifiche ai `.md`

L'agente lavora sul branch `gdpr/aggiornamento-docs` dentro `workspace/`, **non pusha mai** e il
push dalla copia di lavoro è disabilitato. Per portarti le modifiche:

```bash
AG=/Users/carlitos/mobilitas-agenti-ai/agente-gdpr

# 1. revisiona il diff (devono comparire solo file .md)
git -C $AG/workspace/mobilitas-backend diff --stat main...gdpr/aggiornamento-docs

# 2. porta il branch nel tuo repo
cd /Users/carlitos/mobilitas-backend
git fetch $AG/workspace/mobilitas-backend \
    gdpr/aggiornamento-docs:gdpr/aggiornamento-docs
git diff main..gdpr/aggiornamento-docs -- '*.md'

# 3. se ti convince, pubblichi tu
git push origin gdpr/aggiornamento-docs
```

Stessa procedura per `mobilitas-frontend`.

## Garanzie di sicurezza

1. **Hook `PreToolUse`** su `Write|Edit|MultiEdit|NotebookEdit`: lavora a *whitelist* — consente
   solo `.md` dentro `workspace/` e qualunque file dentro `agente-gdpr/`. Tutto il resto,
   percorsi relativi e `..` inclusi, è bloccato.
2. **Hook `PreToolUse` su Bash**: chiude le vie laterali — `git push`, `git clean`,
   `git remote set-url`, riscritture in-place (`sed -i`, `perl -i`, `awk -i inplace`, `patch`,
   `git apply`, `ed`), redirezioni (`>`, `>>`, `>|`, `tee`), comandi mutanti
   (`rm`, `mv`, `cp`, `ln`, `chmod`, `dd`…), `find -delete`/`-exec`, e **codice inline di
   interpreti** (`python -c`, `node -e`, heredoc, `ruby`, `perl`, `php`) con intento di
   scrittura. Vale anche per i percorsi nudi, quando la shell è già dentro `workspace/`.
3. **Deny list** in `.claude/settings.json` sulle estensioni di codice (difesa ridondante).
4. **Sync non distruttivo**: `sync-repos.sh` rifiuta di operare su una copia di lavoro con
   modifiche non committate e non esegue mai `reset --hard` sul branch di documentazione.
   A fine sync verifica che il branch di lavoro tocchi **solo** file `.md` e, in caso
   contrario, segnala un incidente ed esce con codice ≠ 0.
5. **Regola prima in `CLAUDE.md`**: le criticità del codice si *segnalano*, non si correggono.

Le protezioni 1 e 2 sono coperte da una suite di test (67 casi: blocchi attesi **e** falsi
positivi sul flusso legittimo di lavoro):

```bash
./scripts/test-hooks.py
```

Va rieseguita dopo ogni modifica agli hook.

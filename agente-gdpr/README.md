# agente-gdpr — Conformità GDPR di MobilitasHQ

Agente Claude Code che analizza backend e frontend del gestionale MobilitasHQ, ne verifica la
conformità al GDPR, **aggiorna la documentazione Markdown** perché sia a norma e **segnala in un
file MD separato** tutto ciò che manca da implementare.

> **Non modifica in alcun modo il codice.** Solo file `.md` e report. Due hook di sicurezza
> bloccano a livello di harness qualsiasi scrittura su file di codice.

L'agente lavora **direttamente nei repository reali**, sul posto:

- `/Users/carlitos/mobilitas-backend`
- `/Users/carlitos/mobilitas-frontend`

Nessuna copia, nessun clone: i `.md` aggiornati compaiono già nei tuoi repo, su un branch
dedicato che puoi revisionare e pubblicare tu.

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
/sync              # verifica i repo e li porta sul branch di lavoro
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
├── config/repos.json         # dove stanno i repo e qual è il branch di lavoro
├── scripts/
│   ├── prepara-repos.sh      # verifica i repo e prepara il branch (non clona, non pulla)
│   └── test-hooks.py         # verifica che le protezioni siano attive
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

## Su cosa lavora

Da `config/repos.json` (modificabile):

| Repo | Ruolo | Percorso |
|------|-------|----------|
| `mobilitas-backend` | backend gestionale (Java 21 / Spring Boot / PostgreSQL) | `/Users/carlitos/mobilitas-backend` |
| `mobilitas-frontend` | frontend gestionale (React + Vite + TS) | `/Users/carlitos/mobilitas-frontend` |

L'audit analizza lo **stato attuale della tua working tree**, incluse le modifiche non ancora
committate: è il codice vero, non un'istantanea.

`/sync` **non** esegue clone, fetch, pull, push o reset. Si limita a verificare i repo e a
portarli sul branch `gdpr/aggiornamento-docs`. Se hai modifiche non committate si **ferma** e te
le elenca, senza toccarle: sei tu a decidere se committarle o metterle da parte. Ti ricorda
anche su quale branch eri, per tornarci.

## Come revisionare e pubblicare le modifiche ai `.md`

Le modifiche sono già nel tuo repo, sul branch `gdpr/aggiornamento-docs`. L'agente **non pusha
mai**:

```bash
cd /Users/carlitos/mobilitas-backend

# 1. revisiona il diff (devono comparire solo file .md)
git diff main...gdpr/aggiornamento-docs --stat
git diff main...gdpr/aggiornamento-docs -- '*.md'

# 2. se ti convince, pubblichi tu
git push origin gdpr/aggiornamento-docs

# 3. per tornare al tuo lavoro
git checkout main
```

Stessa procedura per `mobilitas-frontend`. Se il diff mostra un file che non è `.md`, è un
incidente: segnalalo e ripristinalo con `git checkout main -- <file>`.

## Garanzie di sicurezza

1. **Hook `PreToolUse`** su `Write|Edit|MultiEdit|NotebookEdit`: lavora a *whitelist* — nei due
   repository consente **solo** i `.md`, dentro `agente-gdpr/` consente tutto, altrove blocca.
   Percorsi relativi e `..` vengono risolti prima del controllo. Se `config/repos.json` è
   illeggibile fallisce **chiuso**.
2. **Hook `PreToolUse` su Bash**: chiude le vie laterali — riscritture in-place (`sed -i`,
   `perl -i`, `awk -i inplace`, `patch`, `git apply`, `ed`), redirezioni (`>`, `>>`, `>|`,
   `tee`), comandi mutanti (`rm`, `mv`, `cp`, `ln`, `chmod`, `dd`…), `find -delete`/`-exec` e
   **codice inline di interpreti** (`python -c`, `node -e`, heredoc, `ruby`, `perl`, `php`) con
   intento di scrittura. Vale anche per i percorsi nudi, quando la shell è già dentro un repo.
3. **Protezione del tuo lavoro in corso** — poiché l'agente opera nei repo che usi davvero,
   l'hook Bash blocca anche `git push`, `reset --hard`, `clean`, `stash`, `rebase`,
   `commit --amend`, `cherry-pick`, `branch -D`, `commit -a` (rastrellerebbe le tue modifiche
   in un commit di documentazione) e `git add` non filtrato sui `.md`.
4. **Deny list** in `.claude/settings.json` sulle estensioni di codice (difesa ridondante).
5. **Regola prima in `CLAUDE.md`**: le criticità del codice si *segnalano*, non si correggono.

Le protezioni 1-3 sono coperte da una suite di test (84 casi: blocchi attesi **e** falsi
positivi sul flusso legittimo di lavoro):

```bash
./scripts/test-hooks.py
```

Va rieseguita dopo ogni modifica agli hook o ai percorsi in `config/repos.json`.

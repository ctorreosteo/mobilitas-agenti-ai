# Skill incluse e dipendenze

## Skill (`skills/`, copie non modificate, non registrate: si leggono solo dopo l'attivazione del WebDesigner)

| Skill | Origine e versione | Licenza | Uso nell'agente |
|---|---|---|---|
| `impeccable` | Paul Bakaus, skill 4.5.2, lanciatore 0.1.14, motore 4.0.0 (binario macOS arm64 incluso) | Apache-2.0 | Contratto di direzione, `context`, rilevatore `detect`, provenienza dei raster (`embed-prompt`), procedure di critique, audit e polish, `craft-floor.md` |
| `taste` | Sen Lin, `senlindesign/taste-skill` v1.1.0 (commit 6dce223), senza la cartella `docs/` (sito promozionale) | MIT | Analisi dei siti di riferimento: token e «Taste DNA» |
| `emil-design-eng` | Emil Kowalski, `emilkowalski/skills` | MIT | Filosofia di rifinitura e animazione |
| `animate` | idem | MIT | Costruire un'animazione nell'ordine giusto |
| `review-animations` | idem | MIT | Revisione severa delle animazioni |
| `find-animation-opportunities` | idem | MIT | Dove serve movimento e dove no (sola lettura) |
| `apple-design` | idem | MIT | Gesti, molle, fogli trascinabili |
| `mobile-native` | idem | MIT | Dettagli da app su telefono: tocco, 100vh, zoom degli input, aree sicure |

Le sei skill di Emil Kowalski sono quelle usate nelle landing di laboratorio. Le altre del suo repository (Swift, Expo, Sonner, prototipi) non servono a questo agente e non sono incluse.

## Agenti (`agenti/`, dalla skill Impeccable; si eseguono come passaggi separati seguendone il testo)

| Agente | Quando |
|---|---|
| `impeccable-finish-reviewer` | Revisione finale, al massimo 2 giri |
| `impeccable-documenter` | DESIGN.md dalla build finita |
| `impeccable-asset-producer` | Pulizia di immagini da una bozza approvata (raro) |
| `impeccable-manual-edit-applier` | Modifiche dalla modalità «live» di Impeccable (non usata nel laboratorio) |

## Uso confinato di Impeccable

La skill chiede di eseguire `<skill>/scripts/impeccable <comando>`. In questo pacchetto si usa invece `tools/impeccable.sh <cartella-progetto> <comando>`, che:

- esegue il comando nella cartella del sito, dove Impeccable cerca PRODUCT.md, DESIGN.md e `.impeccable/`. Quei file nel sito si creano solo con l'approvazione del titolare;
- confina la cartella utente in `<lavoro>/.stato/impeccable-home`;
- spegne telemetria e controllo aggiornamenti;
- usa il motore incluso per macOS arm64. Su altre piattaforme il lanciatore originale lo scaricherebbe da GitHub, quindi `impeccable.sh` si ferma e chiede `IMPECCABLE_BIN`.

**Funzioni che richiedono un server di decisione o la generazione di immagini** (`serve-question`, `live`, `generate-image`): nel laboratorio non sono state usate. La scelta della direzione si fa con il titolare, nel testo della conversazione.

## Uso di Taste senza registrare server MCP

La skill presuppone un server Playwright MCP registrato nella sessione, con `claude mcp add` globale. Qui non si registra nulla. Si procede così:

1. `tools/taste/guardia.sh avvia`: avvia la guardia dei riferimenti, che nega i domini protetti, il loopback e le reti private.
2. `node tools/taste/cattura-riferimento.mjs <url> INC/riferimenti/<dominio>`: esegue la fase 1 di Taste (cattura ed `extract.js`) con un server MCP locale avviato dallo script, in Chrome headless con profilo in memoria.
3. Fasi 2–4: l'agente legge i file prodotti e segue `references/step2–4` della skill. Scrive `<dominio>.md` e `<dominio>.json` nella cartella dell'incarico, mai nella cartella dell'agente.
4. **Esportazione: sempre «Skip».** Le altre opzioni scriverebbero `CLAUDE.md`, `.cursor/rules` e altri file di configurazione.
5. `tools/taste/guardia.sh ferma` a fine lavoro.

## Dipendenze esterne

| Dipendenza | Versione verificata | Obbligatoria | Note |
|---|---|---|---|
| macOS | verificato 27.0.1 (arm64) | per Impeccable, `sips`, OCR | Su altri sistemi: Impeccable va procurato a parte (`IMPECCABLE_BIN`); ritagli e OCR manuali |
| Node.js | 24.15 (min. 18) | sì | Script, Playwright, Superdesign CLI |
| npm | 11.12 | sì | Solo installazioni locali (`npm ci --prefix`) |
| Google Chrome | stabile installato | sì | Browser dei test e delle catture |
| python3 | di sistema | sì | Visore locale delle bozze, localizzazione |
| git, rsync, curl | di sistema | sì | Laboratorio, Git locale, controlli di salute |
| swiftc (Xcode Command Line Tools) | — | no | Solo per l'OCR delle recensioni |
| Account Superdesign | piano del titolare | no | Solo per le bozze; accesso fatto da una persona |
| Cursor o Claude Code | Cursor 3.23.23; Claude Code 2.1.303 | sì (uno dei due) | Attivazione con la skill `webdesigner` (`integrazioni/cursor-e-claude-code.md`) |

**Dipendenze npm locali:**
- `tools/playwright/package-lock.json`: `@playwright/cli` 0.1.22, `playwright-core` 1.64.0-alpha, Montserrat 5.3.0;
- `tools/superdesign/package-lock.json`: `@superdesign/cli` 0.14.0 e le sue dipendenze.

**Il sito (React 19, Vite 7, Tailwind 4, framer-motion, lucide-react):** le dipendenze stanno nel progetto del sito e devono essere già installate per le prove. L'agente non ne aggiunge né ne installa senza autorizzazione.

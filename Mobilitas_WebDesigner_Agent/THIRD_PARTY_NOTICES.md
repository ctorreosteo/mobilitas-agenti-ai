# Componenti di terze parti

Il pacchetto ridistribuisce i componenti qui sotto senza modificarli. Le uniche eccezioni sono quelle indicate. Il testo delle licenze è in `licenze/`.

| Componente | Dove | Licenza | Testo | Note |
|---|---|---|---|---|
| Impeccable (skill 4.5.2, lanciatore 0.1.14, motore 4.0.0, agenti) | `skills/impeccable/`, `agenti/impeccable-*.md` | Apache-2.0 (LICENSE del repository `pbakaus/impeccable`) | `licenze/impeccable-apache-2.0.txt`, avviso NOTICE in `licenze/impeccable-NOTICE.md` | Copyright 2025 Paul Bakaus. Incluso, senza modifiche, il binario macOS arm64 del motore (ridistribuzione consentita da Apache-2.0, sez. 4) |
| Platform Design Skills (ehmo), da cui Impeccable deriva | `skills/impeccable/reference/ios.md`, `skills/impeccable/reference/android.md` | MIT | `licenze/platform-design-skills-MIT.txt` | Segnalato nel NOTICE di Impeccable. Opera originale: github.com/ehmo/platform-design-skills |
| Taste (v1.1.0, commit 6dce223) | `skills/taste/` | MIT | `licenze/taste-skill-MIT.txt` | Autore Sen Lin. Esclusa la cartella `docs/` (sito promozionale con immagini) |
| Skill di Emil Kowalski: emil-design-eng, animate, review-animations, find-animation-opportunities, apple-design, mobile-native | `skills/<nome>/` | MIT | `licenze/emil-kowalski-skills-MIT.txt` | Sei skill su quindici del repository `emilkowalski/skills` |
| Montserrat variabile (woff2, @fontsource-variable/montserrat 5.3.0) | `templates/pagina/fonts/`, `tools/superdesign/visore/vendor/fonts/` | SIL OFL 1.1 | `licenze/montserrat-OFL-1.1.txt` (copia anche accanto ai file) | |
| Iconify Icon 1.0.7 | `tools/superdesign/visore/vendor/iconify-icon.min.js` | MIT | intestazione del file | Solo per visualizzare in locale le bozze Superdesign |
| Tailwind CSS Play CDN (v3.0) | `tools/superdesign/visore/vendor/tailwind-play.js` | MIT | `licenze/tailwindcss-MIT.txt` | Solo per visualizzare le bozze in locale. La fonte esatta del download non è registrata nel laboratorio: il contenuto è riconosciuto come Tailwind CSS v3.0 |
| Guardia dei riferimenti e politica (`tools/taste/policy-lib.mjs`, `pagina-init.js`) | `tools/taste/` | interno Mobilitas | — | Scritti per il WebDesigner Mobilitas |

**Installati da npm, non ridistribuiti** (`tools/setup/installa.sh`):

- `@playwright/cli` 0.1.22 e `playwright-core` 1.64.0-alpha, Apache-2.0;
- `@superdesign/cli` 0.14.0, MIT, con le sue dipendenze (axios, commander, dotenv, open, ora, posthog-node: licenze nei rispettivi pacchetti).

**Servizi esterni:** Superdesign è un servizio a pagamento, regolato dai termini del fornitore e dal piano dell'account del titolare. Nessuna credenziale è inclusa.

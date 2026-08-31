# Mappa del gestionale

Due repository, un prodotto. Un task quasi mai vive in uno solo.

---

## Frontend — `/Users/carlitos/mobilitas-frontend`

React 19 · Vite · TypeScript · Tailwind CSS v4 · shadcn/ui (New York) · React Router 7

### Dove stanno le cose

| Path | Contiene |
|------|----------|
| `src/pages/*.tsx` | Entry di route. Naming `PascalCase.tsx` |
| `src/components/*.tsx` | Componenti di dominio (tabelle, sheet, dialog). Naming `kebab-case.tsx` |
| `src/components/ui/` | **Solo** primitives shadcn/Radix — 29 file. Niente logica di business |
| `src/services/*-service.ts` | Un dominio ≈ un file. HTTP via `apiClient`, mapper al bordo |
| `src/hooks/` | Filtri persistenti, WebSocket, policy UI |
| `src/contexts/` | Stato davvero globale: auth, studio, disponibilità, badge |
| `src/lib/` | Utility pure — `utils.ts` (`cn()`), `toast.ts`, `*-access.ts` |
| `src/types/` | Tipi condivisi |
| `src/style/index.css` | **I tre temi.** 1168 righe |

### Doc da leggere prima di toccare

| File | Quando |
|------|--------|
| `docs/conventions.md` | Sempre. È il contratto di stile |
| `docs/ui-and-components.md` | Qualsiasi cosa visiva |
| `docs/architecture.md` | Task strutturali |
| `docs/routing-and-roles.md` | Permessi, guard, sidebar |
| `docs/services-catalog.md` | Chiamate API |
| `docs/pages-catalog.md` | Trovare la page giusta |
| `docs/state-and-storage.md` | Chiavi `localStorage` |
| `docs/howto-add-feature.md` | Feature nuova end-to-end |

### Verifiche

```bash
npm run typecheck   # tsc -b
npm run lint        # eslint .
npm run build       # smoke artefatto
npm run dev         # smoke manuale
```

**Attenzione: entrambi i gate sono già rossi su albero pulito** — 318 errori di `typecheck` (in maggioranza `TS6133`, import inutilizzati) e 894 problemi di `lint`. Contano solo gli errori **nuovi**: vedi [verifiche.md](verifiche.md).

**Vitest non è cablato.** I file in `src/test/` importano `vitest` ma non esiste script `test` né la dipendenza. Sono **specifiche di riferimento** da leggere, non una suite da lanciare.

---

## Backend — `/Users/carlitos/mobilitas-backend`

Spring Boot · Java · Maven · package base `it.mobilitas.hq`

### Dove stanno le cose

| Path (`src/main/java/it/mobilitas/hq/`) | Contiene | Peso |
|------|----------|------|
| `controllers/` | Endpoint REST | ~72 |
| `services/` | Logica di dominio | ~152 |
| `repositories/` | Accesso dati | ~90 |
| `models/` | Entità | ~101 |
| `dto/` | Request/response | ~237 |
| `jobs/` | Job schedulati | ~50 |
| `mappers/` | Entità ↔ DTO |  |
| `security/` | Auth, ruoli |  |
| `config/` | Configurazione |  |
| `ai/`, `googlebusiness/`, `audit/`, `migration/` | Moduli verticali |  |

Config: `src/main/resources/application*.properties`. Molti valori operativi stanno a **database** nella tabella `Config` (vedi `ConfigRepository`) — se un comportamento non si spiega col codice, cerca la config key.

### Doc da leggere prima di toccare

| File | Quando |
|------|--------|
| `docs/guides/CONVENTIONS.md` | Sempre |
| `docs/guides/MODULES.md` | Orientarsi fra i moduli |
| `docs/guides/ARCHITECTURE.md` | Task strutturali |
| `docs/guides/DATA_FLOWS.md` | Flussi end-to-end |
| `docs/guides/DOMAIN_STATES.md` | Stati ed enum di dominio |
| `docs/guides/AUTH_AND_SECURITY.md` | Ruoli e permessi |
| `docs/guides/ERROR_HANDLING.md` | Errori |
| `docs/guides/INTEGRATIONS.md` | ClickUp, FIC, Qonto, Google |
| `docs/reference/API_DOCUMENTATION.md` | Contratti endpoint |
| `docs/reference/DATABASE_DOCUMENTATION.md` | Schema |
| `docs/reference/CONFIG_KEYS.md` | Config a database |
| `docs/reference/JOBS.md` | Job schedulati |

### Verifiche

```bash
./mvnw -q -DskipTests compile
./mvnw -q -DskipTests package
```

**Zero test.** `src/test/` non contiene alcun file Java. Il compilatore è tutta la rete meccanica che esiste — ma parte **pulito**, quindi qualsiasi output dopo un diff è un segnale vero.

---

## La giuntura fra i due

È dove nascono i bug che nessun compilatore vede: TypeScript e Java compilano felici mentre si scambiano dati diversi.

Controlla sempre, quando un task attraversa il confine:

- **Nomi dei campi** DTO Java ↔ interfacce TS. Un `dataInizio` che diventa `startDate` rompe in silenzio.
- **Envelope di risposta.** Molti endpoint tornano `{ success, message, data, error }`. Lo unwrap sta nel service frontend. Un endpoint nuovo che non segue l'envelope va gestito diversamente — e va notato.
- **Enum.** Gli enum di dominio esistono in Java **e** in TypeScript. Un valore aggiunto da un lato solo produce uno stato che il frontend non sa disegnare.
- **Ruoli.** Il backend accetta sia `ADMIN` sia `ROLE_ADMIN` — il frontend deve normalizzare. Un permesso nuovo va allineato su `App.tsx`, `app-sidebar.tsx` e i bottoni della page.
- **Date.** ISO `YYYY-MM-DD` in UI e API. Attenzione ai fusi: il frontend costruisce le date a `T12:00:00` di proposito, per non slittare di un giorno.

---

## Cosa non usare come modello

`src/pages/Calendario.tsx` è un monolite storico. Funziona, ma non è il pattern da imitare: se un task ti porta lì, segui i pattern degli sheet moderni (visite, pazienti, spese) e non estendere il monolite più del necessario.

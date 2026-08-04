---
name: mappa-gestionale
description: Mappa di orientamento nei due repository del gestionale MobilitasHQ (backend Java/Spring Boot e frontend React/Vite) — dove vivono entità, controller, job, integrazioni esterne, migrazioni, documentazione. Usa questa skill prima di iniziare qualsiasi ricerca nel codice, per non sprecare passaggi e per non dimenticare aree che contengono dati personali.
---

# Dove sta cosa in MobilitasHQ

Tutto il lavoro avviene su `/Users/carlitos/mobilitas-backend` e `/Users/carlitos/mobilitas-frontend`.
Escludi sempre da ricerche e conteggi: `node_modules/`, `target/`, `dist/`, `.venv/`, `build/`, `.git/`.

## Backend — `/Users/carlitos/mobilitas-backend`

Stack: Java 21 · Spring Boot 3.4 · PostgreSQL/Cloud SQL · Flyway · JWT · Cloud Run.
Package radice: `it.mobilitas.hq` in `src/main/java/it/mobilitas/hq/`.

| Package / path | Contenuto | Rilevanza privacy |
|----------------|-----------|-------------------|
| `models/` | entità JPA | **prima fonte**: quali dati personali esistono davvero |
| `repositories/` | query | join che uniscono dati clinici e amministrativi |
| `services/` | logica di dominio | dove i dati si spostano, si esportano, si inviano |
| `controllers/` | endpoint REST | superficie esposta, ruoli richiesti, endpoint pubblici |
| `dto/` | contratti API | over-fetching: dati personali restituiti e non necessari |
| `security/` | JWT, filtri, ruoli | art. 32: autenticazione e autorizzazione |
| `audit/` | tracciamento | art. 32 + linee guida dossier sanitario: chi ha visto cosa |
| `ai/` | integrazione Claude/Whisper/voce | artt. 9, 35, 44-49: cosa esce verso i fornitori AI |
| `jobs/` | cron e job schedulati | art. 5(1)(e): esistono job di cancellazione/purge? |
| `config/` | configurazione | segreti, CORS, region, toggle |
| `mappers/`, `dto/` | conversione entità → DTO | quali campi personali attraversano il confine dell'API |
| `util/`, `utils/` | helper trasversali | formattazione/anonimizzazione, generazione di export |
| `exception/` | gestione errori | messaggi di errore che espongono dati personali |
| `src/main/resources/db/migration/` | **Flyway `V*.sql`** | schema reale: colonne con dati personali, indici, vincoli. Contiene anche dati inseriti via migrazione (**attenzione**: nomi di persone dentro le migration) |
| `src/main/resources/application*.properties` | config per profilo (`local`, `dev`, `uat`, `prod`) | chiavi, endpoint, livelli di log: **confronta i profili**, `prod` è quello che conta |
| `env.example` | variabili attese | elenco dei fornitori |
| `docs/` | documentazione (hub `docs/README.md`) | oggetto degli aggiornamenti |
| `docs/privacy/` | 01 ruoli · 02 registro · 03 DPIA audio · 04 DPIA AI | base da aggiornare |
| `apps-script-cartella-clinica.gs` | Apps Script cartelle cliniche su Drive | flusso di dati sanitari fuori dal DB |
| `logs/`, `scripts/`, `data/` | operatività | possibili dati reali fuori dal DB |

### Comandi utili (sola lettura)

```bash
WS=/Users/carlitos/mobilitas-backend
rg -n "class .*Entity|@Entity" $WS/src/main/java --glob '!target'      # entità
rg -n "@RestController|@RequestMapping" $WS/src/main/java              # endpoint
rg -n "@Scheduled|@EnableScheduling" $WS/src/main/java                 # job
rg -n "permitAll|@PreAuthorize|hasRole|hasAuthority" $WS/src/main/java # autorizzazioni
rg -n "log\.(info|debug|warn|error)" $WS/src/main/java | rg -i "paziente|cartella|anamnesi|email|telefono|codiceFiscale|prompt"
rg -n "RestTemplate|WebClient|HttpClient|api\.|https://" $WS/src/main/java | rg -i "anthropic|openai|elevenlabs|google|fattureincloud|sumup|paypal|qonto|mailchimp|clickup|smshosting"
rg -n "delete|purge|cleanup|retention|scadenza" $WS/src/main/java -i
```

## Frontend — `/Users/carlitos/mobilitas-frontend`

Stack: React + Vite + TypeScript, Firebase Hosting.

| Path | Contenuto | Rilevanza privacy |
|------|-----------|-------------------|
| `src/services/` | chiamate API per dominio (`cartelle-cliniche-service.ts`, `pazienti-*`, `messaggi-service.ts`, `assistente-vocale-service.ts`, …) | quali dati il client richiede e riceve |
| `src/pages/`, `src/components/` | schermate e componenti | quali dati vengono mostrati e a chi |
| `src/contexts/`, `src/hooks/` | stato applicativo | dati clinici tenuti in memoria/contesto |
| `src/lib/`, `src/constants/`, `src/config/` | client API, storage, costanti | **localStorage/sessionStorage con dati personali o token** |
| `src/mock/`, `src/data/`, `src/examples/`, `src/test/` | dati fittizi e fixture | **verificare che non siano dati reali di pazienti** |
| `src/types/` | tipi dei DTO | mappa dei campi personali lato client |
| `index.html`, `src/main.tsx` | bootstrap | script di terze parti, analytics, cookie |
| `docs/` | documentazione (hub `docs/README.md`) | oggetto degli aggiornamenti |
| `*.md` in root | stub storici e doc feature | vanno mantenuti coerenti |
| `.env*`, `firebase.json`, `deploy-firebase-hosting.sh` | configurazione | chiavi esposte al client (tutto ciò che sta in `VITE_*` è **pubblico**) |

### Comandi utili (sola lettura)

```bash
WS=/Users/carlitos/mobilitas-frontend
rg -n "localStorage|sessionStorage|document.cookie" $WS/src
rg -n "console\.(log|debug|info)" $WS/src | rg -i "paziente|cartella|anamnesi|token|email|telefono"
rg -n "VITE_[A-Z_]+" $WS/src $WS/.env.example 2>/dev/null
rg -n "<script|googletagmanager|analytics|hotjar|facebook|clarity" $WS/index.html $WS/src
rg -n "role|ruolo|isAdmin|canView|permission" $WS/src --glob '!*.test.*' | head -50
```

> Regola: il frontend **non** è una misura di sicurezza. Un controllo di ruolo presente solo in
> React va segnalato come criticità se il corrispondente endpoint backend non lo replica.

## Documentazione: dove scrivere

| Repo | Hub | Cartella privacy |
|------|-----|------------------|
| backend | `docs/README.md` | `docs/privacy/` |
| frontend | `docs/README.md` | `docs/privacy/` (da creare se assente) |

Convenzione del progetto (da `docs/guides/CONVENTIONS.md`): **ogni nuovo file Markdown in `docs/`
va aggiunto all'hub `docs/README.md`**, e i link relativi devono risolvere.

# L'impianto privacy del gestionale

Riassunto operativo per la revisione. Fonti: `mobilitas-backend/docs/privacy/` e `docs/guides/AUTH_AND_SECURITY.md`.

---

## Il contesto legale in una riga

OsteoTouch SRL tratta **dati relativi alla salute su larga scala**, con trasferimenti extra-UE verso fornitori AI e cloud. Rischio inerente dichiarato: **alto**, ridotto ad accettabile dalle misure sotto.

Dati sanitari = categoria particolare (art. 9 GDPR). Non sono "dati un po' più delicati": hanno un regime a parte.

## I documenti

| Doc | Contiene |
|-----|----------|
| `01-ruoli-e-responsabilita.md` | RBAC di dettaglio |
| `02-registro-trattamenti.md` | Ogni trattamento previsto — un flusso nuovo va previsto qui |
| `03-dpia-01-audio-whisper-t2.md` | DPIA trascrizione audio |
| `04-dpia-02-ai-clinica-anthropic-t3.md` | DPIA AI clinica |
| `05-ai-act-classificazione-sistemi.md` | Classificazione AI Act |
| `06-informative.md` · `07-diritti-interessati.md` | Informative e diritti |
| `08-violazioni-dati.md` | Procedura data breach |
| `09-misure-sicurezza.md` | **Misure art. 32 in essere** — il documento che il codice non deve smentire |
| `10-trasferimenti-extra-ue.md` | Trasferimenti fuori UE |

`09` è un **atto di accountability**: descrive le misure *effettivamente in essere*. Ogni riga è una dichiarazione fatta al Garante.

---

## Le misure che il codice deve rispettare

| Misura | Implementazione dichiarata |
|--------|----------------------------|
| Password | BCrypt; mai in chiaro, nemmeno all'ADMIN |
| Rotazione password | Trimestrale, blocco API se scaduta (`CambioPasswordTrimestraleFilter`) |
| JWT | HS256, scadenza 24 h, stateless |
| MFA | Su Google Workspace. **Il gestionale non ha MFA nativa** |
| RBAC | Segreteria e marketing **non** accedono al contenuto della cartella; tirocinanti esclusi dal clinico non proprio; pazienti solo ai propri dati |
| **Audit clinico** | Ogni accesso a path clinici → `audit_accessi_clinici` (utente, paziente, risorsa, esito, IP). Retention **730 giorni**, purge `PurgeAuditRetentionJob` alle 03:15 |
| Audit account | Azioni ADMIN su account terzi → `audit_azioni_account`. **Nessuna impersonificazione** |
| Audit API | `ApiActivityAuditFilter` + `SensitiveDataRedactor` |
| **Log AI** | Solo metadati (modello, lunghezze). **Mai** prompt, trascrizioni, output |
| **Audio** | Non persistito su DB né storage dopo Whisper; temp ffmpeg eliminati |
| **ClickUp** | Solo sintesi AI. **Divieto di incollare la cartella integrale** |
| Webhook pagamenti | Qonto verificato con firma HMAC |
| Reset password | Token monouso, hash SHA-256, scadenza 2 ore |
| Cifratura | TLS in transito; a riposo lato Google Cloud, regione `europe-west1` |
| Ambienti | `prod`: `ddl-auto=validate` |
| **Segreti** | Env / Secret Manager / tabella `config`; **non in repository** |

Dichiarate come **non ancora native**: MFA sul gestionale, cifratura column-level, HSM per la chiave JWT. Non segnalarle come difetti: sono già ammesse.

⚠️ **Discrepanza nota:** `src/main/resources/application-local.properties` è tracciato da git e contiene segreti committati (ClickUp, Anthropic, password DB, Qonto), in contraddizione con l'ultima riga della tabella. Debito preesistente: non è compito del revisore risolverlo, ma **un segreto aggiunto lì dal diff è ERRORE**.

---

## L'audit clinico in dettaglio

Il pezzo che genera più difetti, perché fallisce **in silenzio**.

Componenti in `src/main/java/it/mobilitas/hq/audit/`:

| File | Ruolo |
|------|-------|
| `ClinicalAccessAuditPathMatcher` | **L'elenco dei path considerati clinici** |
| `ClinicalAccessAuditInterceptor` | Intercetta le richieste che combaciano |
| `ClinicalAccessAuditRecorder` | Registra l'evento |
| `AuditAccessoClinicoPersister` | Scrive a database |
| `ClinicalAccessAuditConstants` · `Descriptor` · `Event` · `HttpSupport` | Supporto |
| `SensitiveDataRedactor` | Redazione campi sensibili |
| `ApiActivityAuditFilter` | Audit API generale |

Entità: `AuditAccessoClinico` (`utenteId`, `pazienteId`, `tipoRisorsa`, `risorsaId`, `azione`, `endpoint`, esito, IP), con gli enum `TipoRisorsaClinicaAudit`, `AzioneAccessoClinico`, `EsitoAccessoClinico`.

### Path già registrati (estratto)

```
/paziente/{id}                                    /api/pazienti/{id}
/visita/{id}                                      /osservazioni/{id}
/feedback-visite/{id}                             /migra-cartella-clinica-paziente/{id}
/api/cartelle-cliniche/visita/*                   /api/cartelle-cliniche/trascrivi-audio
/api/cartelle-cliniche/organizza-sezione-da-audio
/api/cartelle-cliniche/visita/*/compila-sezione-da-audio
/api/cartelle-cliniche/analisi-qualitativa/paziente/*
/api/cartelle-cliniche/paziente/*/export          /api/cartelle-cliniche/paziente/*/export-simulato
/api/cartelle-cliniche/paziente/*/visite          /api/pazienti/*/crea-cartella-clinica
/api/visite/*/referto-osteopatico                 /api/visite/*/feedback-visita-ai
/api/feedback-visite/*/approva
/api/cartelle-tirocinanti/visita/*                /api/cartelle-tirocinanti/osservazioni[/*]
```

**Il modo di fallire:** aggiungere un endpoint clinico e non registrarlo qui. Nessun errore, nessun test rosso, nessun audit. Oppure rinominare un path già coperto, facendolo uscire dal matcher.

---

## Le entità clinicamente sensibili

`Paziente` · `PazienteFic` · `PazienteMailchimp` · `CartellaClinica` · `CartellaClinicaColloquio` · `CartellaTirocinante` — e tutto ciò che vi si aggancia: visite, referti, osservazioni, feedback clinici, analisi AI, trascrizioni.

Se il diff tocca una di queste, tutte e sette le verifiche sono in gioco.

---

## Autorizzazione: come funziona qui

- **ADMIN accede a tutto.** I check di dominio valutano `utente.isAdmin()` **prima** di qualsiasi esclusione (es. tirocinante). Invertire l'ordine rompe l'admin o salta un'esclusione.
- `RoleHierarchy` (`AdminRoleHierarchy`): ADMIN implica i ruoli HQ, **non** implica PAZIENTE / app mobile.
- Access service di dominio: `cartellaClinicaAccessService.canAccess`, `colloquioCartellaClinicaAccessService`, `corsiAccessService.canAccessFormazione` / `canManageFormazione`.
- Regola della doc: **verificare sempre annotazione sul controller *e* check nel service.**

## Checklist ufficiale per ogni endpoint nuovo

Da `docs/guides/AUTH_AND_SECURITY.md`:

1. Deve essere pubblico? Se sì → `requestMatchers` in `SecurityConfig` **e** documentato lì + API doc.
2. Ruolo minimo / access service?
3. **Path clinico → audit matcher?**
4. Non loggare password/token in chiaro.

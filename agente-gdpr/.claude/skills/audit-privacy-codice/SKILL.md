---
name: audit-privacy-codice
description: Metodo per analizzare il codice del gestionale alla ricerca di evidenze di conformità o non conformità GDPR — inventario dei dati personali, mappa dei flussi verso terzi, controlli di accesso, log, conservazione, diritti dell'interessato. Usa questa skill durante /audit, prima di scrivere qualsiasi documento o criticità. Produce evidenze file:riga, non opinioni.
---

# Audit privacy del codice — metodo

**Il codice è la fonte di verità.** La documentazione può mentire, il codice no.
Ogni affermazione che finirà in un documento o nel report deve avere una **evidenza**:
`percorso/file.java:123` + una riga di citazione.

> **Sola lettura.** Durante l'audit non si modifica nulla, nemmeno i `.md`.
> Se trovi un difetto: annotalo, non correggerlo.

## Output dell'audit

Scrivi in `report/evidenze/` un file per area:

```
report/evidenze/
├── 01-inventario-dati.md        # entità → campi personali → categoria (comune / art. 9)
├── 02-flussi-esterni.md         # ogni uscita di dati verso terzi
├── 03-accessi-e-ruoli.md        # chi può vedere cosa, dove è applicato il controllo
├── 04-log-e-audit.md            # cosa finisce nei log, cosa è tracciato
├── 05-conservazione.md          # job, purge, soft-delete, backup
├── 06-diritti-interessato.md    # export, cancellazione, rettifica, opposizione
├── 07-sicurezza.md              # auth, cifratura, segreti, endpoint pubblici
└── 08-frontend.md               # storage locale, script terzi, controlli solo client
```

Formato di ogni riga di evidenza:

```markdown
- **[FATTO]** Le trascrizioni audio sono salvate in `trascrizione_visita.testo`
  — `src/main/java/it/mobilitas/hq/models/TrascrizioneVisita.java:34`
  → dato art. 9; nessun job di cancellazione trovato (vedi 05).
```

Usa tre marcatori e non confonderli mai:

| Marcatore | Significato |
|-----------|-------------|
| `[FATTO]` | verificato nel codice, con file:riga |
| `[ASSENTE]` | **cercato e non trovato** — indica anche *come* hai cercato |
| `[IPOTESI]` | plausibile ma non verificabile dal codice (es. clausole contrattuali, config di produzione) |

`[IPOTESI]` non può mai diventare un'affermazione in un documento privacy: diventa
`[DA VERIFICARE]` nel documento e una voce nel report.

## Le otto passate

### 1. Inventario dei dati personali

Parti dalle **entità JPA** e dalle **migrazioni Flyway** (lo schema reale).
Per ogni entità: quali campi identificano una persona, quali rivelano lo stato di salute.

Attenzione ai dati sanitari **impliciti**: il solo fatto che una persona sia paziente di uno
studio osteopatico è un dato relativo alla salute. Quindi lo sono anche: appuntamento, causale di
pagamento, riga di fattura, titolo dell'evento in calendario, task ClickUp che nomina il paziente.

Classifica ogni campo: `identificativo` · `contatto` · `amministrativo/fiscale` ·
`art. 9 (salute)` · `tecnico`. Segnala i campi **liberi** (note, descrizioni) dove può finire
qualunque cosa: sono un rischio strutturale di minimizzazione.

### 2. Flussi verso l'esterno

Ogni chiamata HTTP in uscita, ogni SDK, ogni webhook. Per ciascuno rispondi a:
**quali campi partono · verso chi · in quale paese · con quale base di trasferimento ·
quanto restano lì**. I primi due li trovi nel codice; gli ultimi tre quasi mai ⇒ `[ASSENTE]`.

Cerca in particolare cosa viene messo dentro i **prompt AI**: se il prompt include nome, data di
nascita, contatti del paziente, è un problema di minimizzazione da documentare nella DPIA.

### 3. Accessi e ruoli

Per ogni endpoint che restituisce dati clinici: esiste un controllo **server-side**?
Il controllo è per **ruolo** o anche per **appartenenza** (l'osteopata X vede solo i suoi
pazienti)? Un ruolo amministrativo che può leggere le cartelle cliniche va segnalato e motivato.
Cerca gli `permitAll` e verificane la legittimità uno per uno.

### 4. Log e audit trail

Due domande opposte:
- **Cosa non deve esserci e c'è**: dati personali/sanitari nei log applicativi, nei messaggi di
  errore, negli stack trace inviati al client, nei log delle chiamate AI.
- **Cosa deve esserci e manca**: tracciamento degli accessi alle cartelle cliniche, log degli
  amministratori di sistema (≥ 6 mesi), immodificabilità, retention dei log.

### 5. Conservazione

Cerca job schedulati, `@Scheduled`, cron, procedure di purge, campi `deleted_at`/`attivo`.
Per ogni categoria di dato dell'inventario rispondi: **esiste un meccanismo che la cancella?**
Se il registro dei trattamenti dichiara un termine e non esiste il meccanismo → criticità.
Verifica anche: file su GCS e Drive, allegati, audio, backup, ambienti di test.

### 6. Diritti dell'interessato

Cerca endpoint o procedure per: export completo dei dati di un paziente, cancellazione,
rettifica, opposizione a comunicazioni, revoca del consenso e sua propagazione ai sistemi terzi
(Mailchimp, SMS, WhatsApp). Verifica se il "delete" è **soft** e cosa resta.

### 7. Sicurezza

Segui la checklist in `gdpr-normativa/references/04-sicurezza-e-breach.md`.
Segnala **fatti**, non giudizi: "il token JWT ha durata 30 giorni (`JwtService.java:41`)"
è utile; "la sicurezza è debole" non lo è.

Segreti: cerca chiavi, token e password committati. **Se ne trovi, non riportarli nel report:**
scrivi solo file:riga e la natura del segreto, e segnala la necessità di rotazione come criticità
CRITICA.

### 8. Frontend

Storage locale (token, dati clinici in cache), script di terze parti, cookie, dati reali nei
mock, controlli di ruolo presenti solo lato client, variabili `VITE_*` (pubbliche per
definizione: se una di esse è una chiave di un servizio, è un incidente).

## Riconciliazione finale

Ultimo passo dell'audit, in `report/evidenze/09-riconciliazione.md`: confronta l'inventario reale
con `docs/privacy/02-registro-trattamenti.md` e con le due DPIA esistenti.

| Esito | Conseguenza |
|-------|-------------|
| Nel codice, non nel registro | **aggiorna il registro** (documentazione) |
| Nel registro, non nel codice | verifica se è stato dismesso → aggiorna il registro; se doveva esserci → criticità |
| In entrambi ma **divergenti** | il documento va corretto sulla realtà **e** si apre una criticità se la realtà è non conforme |
| Nel documento come misura implementata, ma assente nel codice | **criticità ALTA**: dichiarazione non veritiera in un documento di accountability |

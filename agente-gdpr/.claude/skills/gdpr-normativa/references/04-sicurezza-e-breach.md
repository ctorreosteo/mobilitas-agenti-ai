# Sicurezza (art. 32) e violazioni (artt. 33-34)

## Art. 32 — misure tecniche e organizzative adeguate

Il testo cita esplicitamente:

- **pseudonimizzazione e cifratura**;
- capacità di assicurare **riservatezza, integrità, disponibilità e resilienza** dei sistemi;
- capacità di **ripristinare** tempestivamente disponibilità e accesso in caso di incidente;
- **procedura per testare, verificare e valutare regolarmente** l'efficacia delle misure.

L'adeguatezza si valuta rispetto a stato dell'arte, costi, natura del trattamento e **rischio per
i diritti degli interessati**. Su dati sanitari l'asticella è alta.

### Checklist di verifica sul gestionale (evidenza = file:riga)

| Area | Cosa cercare | Non conformità tipica |
|------|--------------|------------------------|
| Autenticazione | robustezza password, scadenza/rotazione, MFA per ruoli amministrativi, durata e revoca dei JWT, refresh token | assenza di MFA per chi accede a dati sanitari; JWT di lunga durata non revocabili |
| Autorizzazione | controlli per ruolo **lato server** su ogni endpoint che espone dati clinici; segregazione per sede/professionista | controllo solo lato frontend; endpoint che restituisce cartelle di tutti i pazienti a ruoli non clinici |
| Cifratura in transito | HTTPS/TLS forzato, HSTS, WebSocket su WSS | endpoint http, mixed content |
| Cifratura at-rest | DB, storage oggetti, backup; gestione delle chiavi | backup non cifrati; file clinici in bucket con ACL larghe |
| Segreti | uso di secret manager, assenza di chiavi in repo/env committati, rotazione | API key in `application.properties` o in file `.env` versionati |
| **Log** | i log applicativi contengono nome, email, telefono, codice fiscale, **testo clinico**, prompt AI, trascrizioni? | log di debug che stampano il payload della cartella clinica |
| **Audit trail** | tracciamento di *chi ha visto quale cartella e quando*, immodificabile, con retention | accessi ai dati clinici non tracciati (requisito rafforzato dalle linee guida dossier sanitario) |
| Amministratori di sistema | designazioni, elenco, **log accessi AdS ≥ 6 mesi**, verifica annuale | nessun log AdS distinto |
| Backup e ripristino | frequenza, cifratura, **test di restore documentato**, retention allineata al registro | backup conservati per sempre, vanificando la retention dichiarata |
| Resilienza | monitoring, alerting, RTO/RPO dichiarati | nessun obiettivo definito |
| Sviluppo sicuro | validazione input, protezione da IDOR sugli id di paziente/cartella, rate limiting su endpoint pubblici, gestione degli upload | endpoint pubblici (webhook) senza verifica di firma |
| Ambienti | dati di produzione copiati in test/UAT? | dataset clinico reale in ambiente di test = trattamento non previsto |
| Cancellazione | soft-delete vs cancellazione effettiva, purge dei file su storage e su Drive | record "cancellato" che resta in tabella e su Drive indefinitamente |

## Artt. 33-34 — violazione dei dati personali

| Obbligo | Contenuto |
|---------|-----------|
| Art. 33(1) | Notifica al **Garante entro 72 ore** dal momento in cui il titolare ne viene a conoscenza, salvo che sia improbabile un rischio per i diritti e le libertà |
| Art. 33(2) | Il **responsabile** deve informare il titolare **senza ingiustificato ritardo** ⇒ deve essere scritto nei DPA |
| Art. 33(3) | Contenuti minimi della notifica: natura, categorie e numero approssimativo di interessati e di record, contatti DPO, conseguenze probabili, misure adottate/proposte |
| Art. 33(5) | **Registro delle violazioni** interno, obbligatorio **anche** per le violazioni non notificate, con motivazione della non notifica |
| Art. 34 | Comunicazione **all'interessato** senza ingiustificato ritardo se il rischio è **elevato**; non dovuta se i dati erano cifrati in modo adeguato o se sono state adottate misure successive che scongiurano il rischio |

Con dati sanitari la soglia del "rischio elevato" si raggiunge facilmente: la procedura deve
essere scritta, con ruoli, tempi e un canale di segnalazione interno.

### Cosa deve esistere come documento

1. **Procedura di gestione data breach**: rilevazione → qualificazione entro X ore → valutazione
   del rischio → notifica → comunicazione → lezioni apprese.
2. **Registro delle violazioni** (template compilabile).
3. **Modello di notifica** al Garante e di comunicazione agli interessati.
4. Contatti e responsabilità nominative (chi decide la notifica).

Se questi documenti non esistono nella `docs/privacy/` del gestionale, è una criticità **ALTA**
di natura documentale: si può **creare il documento** (è Markdown) e segnalare che va validato e
adottato formalmente.

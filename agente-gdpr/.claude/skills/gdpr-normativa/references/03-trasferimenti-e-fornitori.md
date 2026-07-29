# Responsabili esterni e trasferimenti extra-UE

## Art. 28 — contratto con il responsabile (DPA)

Ogni fornitore che tratta dati personali per conto del Titolare deve avere un **atto giuridico
scritto** con i contenuti minimi dell'art. 28(3):

- oggetto, durata, natura e finalità del trattamento; tipo di dati; categorie di interessati;
- trattamento **solo su istruzione documentata** del titolare, anche per i trasferimenti;
- impegno di **riservatezza** delle persone autorizzate;
- misure di sicurezza ex art. 32;
- disciplina dei **sub-responsabili** (autorizzazione scritta specifica o generale + preavviso);
- assistenza al titolare per: risposta ai diritti (artt. 12-22), notifica di data breach
  (artt. 33-34), DPIA (artt. 35-36);
- **cancellazione o restituzione** dei dati a fine servizio;
- disponibilità delle informazioni per **audit e ispezioni**.

### Checklist per il registro dei responsabili

Per ogni fornitore, la documentazione deve riportare: nome legale, servizio, **categorie di dati
trattati** (sanitari? sì/no), **paese di trattamento**, base per il trasferimento, **DPA firmato
sì/no + data e versione**, sub-responsabili noti, misure aggiuntive.

> Se il DPA non è verificabile, si scrive `[DA VERIFICARE — reperire DPA firmato]` nel documento
> **e** si apre una criticità. Non si scrive mai "DPA sottoscritto" senza prova.

## Artt. 44-49 — trasferimenti verso paesi terzi

Ordine di preferenza delle basi:

1. **Decisione di adeguatezza** (art. 45). Per gli USA esiste l'**EU-US Data Privacy Framework**
   (decisione della Commissione del 10 luglio 2023): vale **solo** per le organizzazioni
   effettivamente **certificate** e per le categorie di dati incluse nella certificazione.
   Va verificato caso per caso sull'elenco ufficiale DPF `[verificare alla data dell'audit]`.
2. **Garanzie adeguate** (art. 46): **Clausole Contrattuali Standard** (decisione di esecuzione
   UE 2021/914), BCR, codici di condotta.
3. **Deroghe** (art. 49): eccezionali, non ripetitive, non strutturali. **Non** sono una base
   valida per un flusso continuativo verso un fornitore cloud.

Con le SCC serve un **Transfer Impact Assessment** (raccomandazioni EDPB 01/2020): valutazione
della legislazione del paese terzo e delle **misure supplementari** (cifratura, pseudonimizzazione,
policy anti-disclosure, trasparenza sulle richieste delle autorità).

## Fornitori di MobilitasHQ da istruire nella documentazione

Elenco di partenza da `docs/guides/INTEGRATIONS.md` — **va riverificato sul codice a ogni audit**,
perché la lista cambia:

| Fornitore | Dati potenzialmente coinvolti | Nodo privacy da verificare |
|-----------|-------------------------------|-----------------------------|
| Google Cloud (Cloud Run, Cloud SQL, GCS) | tutti, inclusi sanitari | DPA + region dei dati (EU?), sub-processor, cifratura |
| Google Workspace / Drive / Docs / Apps Script | **cartelle cliniche** | region, condivisione, permessi dei file, chi accede |
| Gmail | comunicazioni con pazienti | contenuto clinico nelle email |
| Google Calendar / Contacts | appuntamenti = dato sanitario indiretto | il titolo evento rivela la prestazione? |
| Google Business Profile | recensioni | risposte pubbliche che confermano lo stato di paziente ⇒ divieto |
| **Anthropic (Claude)** | testo clinico, anamnesi | DPA, no-training, retention del prompt, base del trasferimento, regione |
| **OpenAI (Whisper)** | **audio della visita** | idem + retention audio + DPA |
| **ElevenLabs** | voce, testo dell'assistente | idem |
| Vertex/Gemini | eventuale, se attivato | region EU configurata? |
| FattureInCloud | dati fiscali del paziente | divieto SdI su prestazioni sanitarie |
| SumUp / PayPal / Qonto | pagamenti | il causale rivela la prestazione? |
| Mailchimp | contatti marketing | segregazione dai dati clinici, base consenso |
| SMSHosting | numeri, testo SMS | contenuto clinico nei messaggi |
| ClickUp | task operativi | dati di paziente dentro i task? |
| Cloudflare Stream | video sito | immagini di persone ⇒ liberatorie |
| DocuSign / Zapier | consensi, bridge dati | quali dati transitano nel bridge |

## Regole di scrittura per la documentazione

- Nel registro: colonna **"trasferimento extra-UE"** con paese e **base giuridica specifica**
  (DPF / SCC / adeguatezza), mai un generico "sì".
- Per i fornitori AI serve una riga in più: **il fornitore usa i dati per addestrare i modelli?**
  Se sì o se non verificabile ⇒ criticità **CRITICA** su dati sanitari.
- Un fornitore che tratta **dati sanitari** e non ha DPA verificabile ⇒ criticità **ALTA**
  minimo, con impatto su artt. 28 e 9.

# Articoli GDPR chiave — requisito operativo e verifica nel gestionale

Regolamento (UE) 2016/679.

## Principi e responsabilità

| Art. | Requisito | Verifica sul gestionale |
|------|-----------|--------------------------|
| 5(1)(a) | Liceità, correttezza, **trasparenza** | esiste informativa aggiornata per pazienti, dipendenti, lead, utenti sito? |
| 5(1)(b) | Limitazione della finalità | i dati clinici sono usati per marketing/analytics? controlla export e job |
| 5(1)(c) | **Minimizzazione** | campi personali raccolti e non usati; payload API sovradimensionati; log con dati identificativi |
| 5(1)(d) | Esattezza | esistono flussi di rettifica; dati importati da fonti esterne |
| 5(1)(e) | **Limitazione della conservazione** | tempi definiti *per trattamento* + job che li applicano davvero |
| 5(1)(f) | Integrità e riservatezza | rimanda ad art. 32 |
| 5(2) | **Accountability** | ogni misura dichiarata deve essere dimostrabile con documenti/evidenze |
| 24 | Misure del Titolare | politiche interne, formazione, revisione periodica |
| 25 | **Privacy by design e by default** | i default del sistema sono i più protettivi? (es. visibilità cartella limitata all'osteopata curante) |
| 26 | Contitolarità | più soggetti giuridici che decidono insieme finalità/mezzi |
| 29 / 2-quaterdecies Codice | Persone autorizzate | designazioni scritte, istruzioni, ruoli applicativi coerenti |
| 37-39 | DPO | obbligatorio se trattamento **su larga scala** di dati art. 9 — motivare la valutazione, non darla per scontata (Cons. 91: il singolo professionista sanitario non è "larga scala") |

## Basi giuridiche

| Art. | Uso tipico in MobilitasHQ |
|------|---------------------------|
| 6(1)(b) | esecuzione del contratto: prenotazione, pagamento, fatturazione |
| 6(1)(c) | obblighi di legge: fiscali, Sistema TS, conservazione contabile |
| 6(1)(f) | legittimo interesse: sicurezza informatica, recupero crediti, alcune comunicazioni di servizio — richiede **LIA documentata** |
| 6(1)(a) | consenso: marketing, newsletter, recensioni, uso promozionale di immagini |
| **9(2)(h)** | **finalità di cura**: base per i dati sanitari, con art. 9(3) (segreto professionale) |
| 9(2)(a) | consenso esplicito: solo per finalità ulteriori rispetto alla cura |
| 9(2)(f) | difesa in giudizio |

> Errore frequente da segnalare: chiedere il consenso privacy "per curare" e usarlo come base
> giuridica. Per la cura la base è 9(2)(h)+6(1)(b)/(c); il consenso raccolto va tenuto separato
> e riferito alle sole finalità ulteriori.

## Informativa e diritti

| Art. | Requisito | Verifica |
|------|-----------|----------|
| 12 | Forma concisa, trasparente, accessibile; risposta entro **1 mese** (prorogabile di 2) | esiste procedura e tracciamento delle richieste? |
| 13 | Informativa per dati raccolti presso l'interessato | contenuti completi: titolare, DPO, finalità, basi, destinatari, trasferimenti, conservazione, diritti, reclamo al Garante, natura obbligatoria/facoltativa |
| 14 | Dati raccolti da terzi (es. lead da portali, Google Business) | spesso mancante: verificare |
| 15 | Accesso + **copia dei dati** | endpoint o procedura manuale documentata |
| 16 | Rettifica | |
| 17 | Cancellazione — **limitata** dai obblighi di conservazione sanitaria/fiscale | il sistema fa soft-delete: documentare che non è cancellazione |
| 18 | Limitazione | esiste un modo di "congelare" un record? |
| 19 | Notifica ai destinatari | |
| 20 | Portabilità (solo dati forniti, base consenso/contratto, formato interoperabile) | export strutturato disponibile? |
| 21 | Opposizione (incl. marketing, sempre) | opt-out effettivo su email/SMS/WhatsApp |
| 22 | Decisioni automatizzate e profilazione | l'AI clinica **suggerisce** o **decide**? se supporta il professionista, documentare l'intervento umano |

## Organizzazione e sicurezza

| Art. | Requisito |
|------|-----------|
| 28 | Responsabili del trattamento: contratto scritto con contenuti minimi, autorizzazione sub-responsabili, istruzioni documentate, audit |
| 30 | **Registro dei trattamenti** — contenuti obbligatori: finalità, categorie di interessati e di dati, destinatari (anche extra-UE), trasferimenti + garanzie, **termini di cancellazione previsti**, descrizione generale delle misure di sicurezza |
| 32 | Sicurezza adeguata al rischio (vedi `04-sicurezza-e-breach.md`) |
| 33 | Notifica violazione al Garante entro **72 ore** dalla conoscenza, salvo rischio improbabile |
| 34 | Comunicazione all'interessato senza ingiustificato ritardo se **rischio elevato** |
| 35 | DPIA (vedi `05-dpia-e-ai.md`) |
| 36 | Consultazione preventiva se il rischio residuo resta elevato |
| 44-49 | Trasferimenti extra-UE (vedi `03-trasferimenti-e-fornitori.md`) |

## Sanzioni (per calibrare la severità nel report)

- Art. 83(4): fino a **10 M€ o 2%** del fatturato mondiale — es. violazioni artt. 25, 28, 30, 32-36.
- Art. 83(5): fino a **20 M€ o 4%** — es. violazioni artt. 5, 6, 9, 12-22, 44-49.

Una criticità che tocca art. 9, art. 32 su dati sanitari o trasferimenti extra-UE senza garanzie
non può essere classificata sotto **ALTA**.

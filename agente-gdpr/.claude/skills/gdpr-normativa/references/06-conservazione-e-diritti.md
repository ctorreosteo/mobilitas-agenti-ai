# Conservazione, informative e diritti dell'interessato

## Conservazione (art. 5(1)(e) + art. 30(1)(f))

Il registro dei trattamenti deve indicare, ove possibile, i **termini ultimi previsti per la
cancellazione** delle diverse categorie di dati. Il test di conformità è in tre passi:

1. Il **termine** è dichiarato e **motivato** (norma, prescrizione, necessità clinica)?
2. Esiste un **meccanismo** che lo applica (job schedulato, procedura manuale con responsabile e
   periodicità)?
3. Il meccanismo copre **tutte le copie**: DB, storage oggetti, Drive/Docs, backup, log, code,
   sistemi di terzi, export, ambienti non di produzione?

Se manca il punto 2 o 3, il termine dichiarato è una **dichiarazione non veritiera** in un
documento di accountability: criticità **ALTA**.

### Griglia di riferimento (da adattare e motivare, non da copiare)

| Categoria | Termine indicativo | Fonte del criterio |
|-----------|--------------------|--------------------|
| Cartella clinica / documentazione osteopatica | lungo periodo, es. 10 anni dall'ultima prestazione | tutela della salute + prescrizione decennale (art. 2946 c.c.) |
| Audio visita e trascrizione grezza | **giorni**: fino alla produzione del documento clinico | minimizzazione, art. 5(1)(c)-(e) |
| Prompt/risposte AI e log correlati | breve, definito | minimizzazione |
| Fatture, contabilità | 10 anni | art. 2220 c.c. |
| Dati Sistema TS e opposizioni | secondo normativa fiscale | obbligo di legge |
| Appuntamenti e agenda | allineato alla cartella | |
| Lead / contatti non convertiti | 12-24 mesi | motivare |
| Consensi e revoche | per tutta la durata + prescrizione, come prova | accountability art. 5(2) |
| CV e candidature | breve (es. 12 mesi) | |
| Log applicativi | motivato; **AdS ≥ 6 mesi** | Provv. Garante 27/11/2008 |
| Backup | ciclo definito e **allineato** alla retention dei dati | |
| Messaggi con pazienti (email/WhatsApp/SMS) | definito | contengono potenzialmente dati sanitari |

## Informative (artt. 13-14)

Servono informative **distinte per categoria di interessato**:

| Interessato | Note |
|-------------|------|
| Paziente | finalità di cura, AI e registrazione audio (se usate), Sistema TS e opposizione, comunicazioni di servizio, conservazione, diritti |
| Lead / contatto dal sito | art. 13; se il contatto arriva da terzi (portali, Google) serve **art. 14** |
| Dipendente / collaboratore | dati di presenza, valutazioni, eventuale monitoraggio |
| Candidato | |
| Utente del gestionale (operatore) | log e tracciamento accessi |

Contenuti obbligatori da controllare uno per uno: identità e contatti del titolare, contatti del
DPO (se nominato), **finalità e base giuridica per ciascuna**, legittimi interessi se invocati,
**destinatari o categorie di destinatari**, **trasferimenti extra-UE + garanzia applicata e come
ottenerne copia**, periodo di conservazione o criteri, elenco dei diritti, diritto di **revocare
il consenso** senza pregiudicare la liceità precedente, **diritto di reclamo al Garante**,
natura obbligatoria o facoltativa del conferimento e conseguenze del rifiuto, esistenza di
**processi decisionali automatizzati** con logica e conseguenze.

> Un'informativa che parla di "consenso al trattamento dei dati per finalità di cura" è
> normativamente sbagliata: vedi `02-dati-sanitari-italia.md`.

## Gestione delle richieste (artt. 12, 15-22)

Deve esistere una **procedura documentata** con:

- canale di ricezione (email dedicata) e **registro delle richieste**;
- verifica dell'identità del richiedente (art. 12(6)) senza raccolta eccessiva;
- **1 mese** per rispondere, prorogabile di **2** con motivazione comunicata entro il primo mese;
- gratuità, salvo richieste manifestamente infondate o eccessive (art. 12(5));
- indicazione dei limiti: la cancellazione (art. 17) **non** si applica dove esiste obbligo di
  conservazione o esigenza di difesa in giudizio — e questo va spiegato all'interessato;
- ambito tecnico della risposta: quali sistemi vanno interrogati per una richiesta di accesso
  (DB, Drive, email, WhatsApp, backup?) — se non è mappato, la risposta sarà incompleta.

### Verifica tecnica corrispondente

- Esiste un **export completo** dei dati di un paziente (art. 15/20)?
- Esiste una procedura di **cancellazione effettiva** che copra tutte le repliche?
- Il **soft-delete** del gestionale è documentato come *sospensione dell'uso* e non come
  cancellazione? Spacciare il soft-delete per cancellazione è una criticità.
- Le **revoche** del consenso propagano davvero (marketing, Mailchimp, SMS)?

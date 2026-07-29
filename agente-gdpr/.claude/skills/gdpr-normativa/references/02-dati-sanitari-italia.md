# Disciplina italiana dei dati sanitari

## Fonte principale

**D.lgs 196/2003** (Codice in materia di protezione dei dati personali), come modificato dal
**D.lgs 101/2018** per l'adeguamento al GDPR.

| Articolo Codice | Contenuto rilevante |
|-----------------|---------------------|
| art. 2-septies | **Misure di garanzia** per dati genetici, biometrici e **relativi alla salute** — adottate dal Garante, con verifica biennale. È il gancio normativo delle misure tecniche richieste su un gestionale clinico |
| art. 2-quaterdecies | Designazione delle **persone autorizzate** al trattamento sotto l'autorità del titolare/responsabile |
| art. 75 | Trattamento per **finalità di cura**: da parte o sotto la responsabilità di un professionista soggetto a **segreto professionale** — non richiede consenso |
| art. 79-82 | Modalità in ambito sanitario (informativa, dignità, riservatezza nei locali) |
| art. 99 | Conservazione per scopi di archivio/ricerca/statistica oltre la finalità originaria |
| art. 166-167 | Sanzioni amministrative e illeciti penali (trattamento illecito di dati) |

## Provvedimenti e linee guida del Garante da tenere presenti

| Provvedimento | Perché rileva per MobilitasHQ |
|---------------|-------------------------------|
| **Chiarimenti sul trattamento in ambito sanitario, 7 marzo 2019 (n. 55)** | Conferma che **per la cura non serve il consenso** (art. 9(2)(h) + art. 75). Il consenso serve per: refertazione online, consultazione del dossier da parte di altri professionisti, marketing, ricerca. Da citare ogni volta che la documentazione parla di "consenso al trattamento" |
| **Misure di garanzia dati genetici/biometrici/salute, 5 giugno 2019 (n. 146)** | Prescrizioni tecniche e organizzative specifiche |
| **Linee guida dossier sanitario, 4 giugno 2015** | Rilevante perché il gestionale aggrega lo storico clinico del paziente: consenso specifico all'alimentazione/consultazione, **oscuramento** di singoli eventi clinici, tracciamento degli accessi, informativa dedicata |
| **Provvedimento amministratori di sistema, 27 novembre 2008** (mod. 25 giugno 2009) | Designazione nominativa degli AdS, elenco aggiornato, **log degli accessi degli AdS conservati almeno 6 mesi, inalterabili e completi**, verifica annuale dell'operato. Applicabile anche se lo sviluppatore/amministratore coincide con il Titolare: la verifica va comunque documentata |
| **Linee guida cookie, 10 giugno 2021 (n. 231)** | Rileva per il sito e per eventuali script di analytics nel frontend; non per il gestionale interno se non usa cookie non tecnici |
| **Linee guida email marketing / soft spam** | Rileva per comunicazioni ai pazienti via email/SMS/WhatsApp: base giuridica, opt-out, separazione dalle comunicazioni di servizio |
| **Elenco tipologie di trattamento soggette a DPIA, 11 ottobre 2018 (n. 467)** | Vedi `05-dpia-e-ai.md` |

> Le numerazioni e le date sopra sono stabili. Ciò che cambia nel tempo (proroghe, nuovi
> provvedimenti su AI e sanità) va segnalato come `[verificare aggiornamenti]`.

## Comunicazioni al paziente

- **WhatsApp/SMS/email di servizio** (promemoria appuntamento): riconducibili all'esecuzione del
  rapporto di cura, ma vanno **informati** e va evitato di inserire **contenuto clinico** nel
  messaggio. Un promemoria che cita la patologia è una comunicazione di dati sanitari su canale
  non controllato → criticità.
- **WhatsApp Business**: il fornitore è extra-UE; se il gestionale invia messaggi via provider,
  quel provider è responsabile ex art. 28 e va nel registro.
- **Marketing/recensioni**: base consenso, opt-out documentato, separazione dei database.

## Fisco e sanità — due punti che un gestionale sbaglia spesso

1. **Divieto di fatturazione elettronica per prestazioni sanitarie verso persone fisiche.**
   Le fatture relative a prestazioni sanitarie rese a persone fisiche **non vanno trasmesse al
   Sistema di Interscambio** (norma introdotta con l'art. 10-bis del DL 119/2018 e più volte
   prorogata). Il gestionale integra FattureInCloud: va verificato che le fatture sanitarie
   siano emesse **fuori SdI** o marcate correttamente.
   `[verificare la proroga vigente alla data dell'audit]`
2. **Sistema Tessera Sanitaria** — invio delle spese sanitarie per il 730 precompilato:
   trattamento basato su **obbligo di legge**, con **diritto di opposizione dell'assistito**
   che deve essere raccolto, registrato e rispettato. Verificare che il gestionale gestisca e
   conservi l'opposizione.

## Conservazione della documentazione sanitaria

Non esiste un termine unico per lo studio privato. Criteri difendibili da documentare nel
registro dei trattamenti:

| Categoria | Criterio |
|-----------|----------|
| Documentazione clinica (cartella osteopatica) | conservazione prolungata per tutela sanitaria del paziente e difesa in giudizio; motivare il termine scelto (spesso 10 anni dall'ultima prestazione, per analogia con la prescrizione della responsabilità contrattuale, art. 2946 c.c.) |
| Documenti contabili e fatture | **10 anni** (art. 2220 c.c. e norme fiscali) |
| Audio della visita / trascrizione grezza | dato **strumentale**: va cancellato appena prodotto il documento clinico definitivo. Conservarlo indefinitamente è una violazione dell'art. 5(1)(e) |
| Dati di lead / contatti non diventati pazienti | termine breve (es. 12-24 mesi), motivato |
| Log tecnici e di audit | ≥ 6 mesi per gli AdS; per il resto termine motivato e proporzionato |
| Candidature / CV | termine breve e definito |

> Regola: **ogni categoria di dato nel registro deve avere un termine e un job/processo che lo
> applica.** Termine dichiarato senza meccanismo che lo esegue = criticità (art. 5(2) + 5(1)(e)).

## Altre norme da valutare (non dare per applicabili)

- **NIS2** (D.lgs 138/2024): il settore sanitario è incluso, ma si applicano soglie
  dimensionali. Valutare e documentare l'esito, non assumerlo.
- **Codice deontologico** della professione e obblighi di segreto professionale.
- **EHDS** (Reg. UE 2025/327 sullo Spazio europeo dei dati sanitari): impatti futuri,
  da citare solo come orizzonte.

---
name: report-criticita
description: Formato, tassonomia di severità e regole di scrittura del report delle criticità GDPR — ciò che manca da implementare nel gestionale e non può essere risolto con la sola documentazione. Usa questa skill durante /report o ogni volta che devi registrare un gap trovato durante l'audit.
---

# Report criticità — `report/CRITICITA-GDPR.md`

È l'output che l'utente ha chiesto esplicitamente: **un file MD separato** con tutto ciò che
manca da implementare. Non contiene modifiche al codice, solo segnalazioni.

Copia il file, a fine lavorazione, anche in
`/Users/carlitos/mobilitas-backend/docs/privacy/99-criticita-e-gap-aperti.md`.

## Cosa va nel report

| Va nel report | Non va nel report |
|---------------|--------------------|
| Requisito normativo non implementato nel codice | ciò che si risolve aggiornando un `.md` (fallo e basta) |
| Misura dichiarata nei documenti ma inesistente | opinioni di stile o refactoring |
| Informazione che solo il Titolare può fornire (DPA, contratti, decisioni) | bug funzionali senza rilevanza privacy |
| Rischio che richiede una decisione (es. cambiare fornitore, cifrare, introdurre MFA) | suggerimenti generici tipo "migliorare la sicurezza" |
| Verifica che non è possibile fare dal codice | |

## Severità

| Livello | Criterio | Esempi |
|---------|----------|--------|
| **CRITICA** | Violazione in atto su dati art. 9, o esposizione concreta di dati sanitari, o trasferimento extra-UE senza alcuna base | segreto committato ancora valido; endpoint clinico senza autorizzazione; audio inviato a fornitore USA senza DPA né base di trasferimento |
| **ALTA** | Obbligo GDPR non soddisfatto, senza esposizione immediata | nessun tracciamento degli accessi alle cartelle; nessun meccanismo che applichi la retention dichiarata; DPA non reperibile per un fornitore che tratta dati sanitari; procedura data breach assente |
| **MEDIA** | Obbligo soddisfatto parzialmente o in modo non dimostrabile | valutazione "non larga scala" non motivata; export dati paziente solo manuale; log senza retention definita |
| **BASSA** | Buona prassi non adottata, rischio limitato | assenza di test di restore documentato; naming che rende difficile la mappatura dei dati |
| **DA VERIFICARE** | Non decidibile dal codice: serve un'informazione dal Titolare | region effettiva dei bucket in produzione; contenuto dei contratti; configurazione di Cloud Run |

Regola di calibrazione: una criticità che tocca **art. 9**, **art. 32 su dati sanitari** o
**artt. 44-49** non può stare sotto **ALTA**.

## Struttura del file

```markdown
# Criticità GDPR — MobilitasHQ

> **Data audit**: AAAA-MM-GG · **Commit backend**: <sha> · **Commit frontend**: <sha>
> **Perimetro**: backend + frontend del gestionale. Nessuna modifica al codice è stata apportata.
> Documento tecnico da validare con DPO/consulente privacy: non costituisce parere legale.

## Sintesi

| Severità | Numero | Aree principali |
|----------|--------|-----------------|
| CRITICA | n | … |
| ALTA | n | … |
| MEDIA | n | … |
| BASSA | n | … |
| DA VERIFICARE | n | … |

## Cosa è stato risolto in questa sessione (documentazione)
Elenco dei .md aggiornati/creati, con una riga di descrizione.

## Criticità aperte
<una scheda per criticità, ordinate per severità>

## Domande al Titolare
<elenco numerato delle informazioni che servono per chiudere le voci DA VERIFICARE>

## Metodo e limiti dell'audit
Cosa è stato analizzato, cosa no (es. configurazione di produzione, contratti, backup reali).
```

## Scheda della singola criticità

```markdown
### [CRITICA] GDPR-007 — Audio della visita conservato senza termine

| | |
|---|---|
| **Severità** | CRITICA |
| **Articoli** | art. 5(1)(c) e (e), art. 9, art. 32 |
| **Area** | Conservazione · Cartelle cliniche |
| **Componente** | backend |

**Fatto rilevato**
L'entità `RegistrazioneVisita` salva il file audio su GCS e non esiste alcun job che lo elimini
dopo la generazione del documento clinico.
Evidenza: `src/main/java/it/mobilitas/hq/models/RegistrazioneVisita.java:28`;
ricerca `@Scheduled` in `jobs/` → nessun purge (`[ASSENTE]`).

**Perché è un problema**
L'audio è un dato relativo alla salute (art. 9) e strumentale alla produzione della cartella:
conservarlo senza termine viola la limitazione della conservazione (art. 5(1)(e)) e amplia
l'impatto di un'eventuale violazione.

**Cosa manca da implementare** *(indicazione, NON implementata dall'agente)*
1. Definire il termine (proposta: cancellazione entro N giorni dalla validazione del documento).
2. Job schedulato di purge su DB **e** su storage, con log dell'esito.
3. Allineare `docs/privacy/02-registro-trattamenti.md` una volta implementato.

**Chi decide** Titolare (termine) → sviluppo (job).
**Stato** aperta · **Rilevata** AAAA-MM-GG
```

## Regole di scrittura

- **ID stabili** `GDPR-001`, `GDPR-002`… Se una criticità già presente resta aperta in un audit
  successivo, **conserva il suo ID** e aggiorna lo stato (`aperta` / `in corso` / `chiusa il …`).
- Ogni scheda deve avere almeno **una evidenza `file:riga`** oppure una ricerca `[ASSENTE]`
  esplicita ("cercato X in Y, nessun risultato"). Senza evidenza, la voce non entra.
- **Mai incollare segreti, dati di pazienti reali o estratti di cartelle** nel report: cita solo
  il percorso e la natura del dato.
- Ordina per severità, poi per componente.
- Il tono è fattuale: descrivi cosa manca, non colpevolizzare l'implementazione.
- Se una criticità è stata **risolta scrivendo documentazione**, non va tra le aperte: va nella
  sezione "cosa è stato risolto".
- Chiudi sempre con **"Domande al Titolare"**: è la parte che sblocca il lavoro successivo.

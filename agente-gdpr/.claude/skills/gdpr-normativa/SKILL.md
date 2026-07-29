---
name: gdpr-normativa
description: Corpo normativo di riferimento per la conformità privacy di un gestionale sanitario italiano — GDPR (Reg. UE 2016/679), Codice Privacy (D.lgs 196/2003 come mod. da 101/2018), provvedimenti e linee guida del Garante, trasferimenti extra-UE, sicurezza e data breach, DPIA e AI Act, conservazione e diritti dell'interessato. Usa questa skill ogni volta che devi citare un requisito, valutare se una pratica del gestionale è conforme, scrivere una sezione di documentazione privacy o classificare una criticità.
---

# Normativa privacy applicabile a MobilitasHQ

Fonti in ordine di forza: **GDPR** → **Codice Privacy italiano** → **provvedimenti/linee guida del
Garante** → **prassi EDPB** → norme settoriali (fisco, Sistema TS, AI Act).

## Regola d'uso

1. Cita sempre **articolo e comma** (`art. 30(1)(f) GDPR`), mai "la normativa richiede".
2. Se una regola dipende da una **proroga annuale** o da una decisione di adeguatezza in
   evoluzione (fatturazione sanitaria, EU-US DPF), scrivilo esplicitamente:
   `[verificare norma vigente alla data]`. **Non inventare la scadenza.**
3. Distingui sempre **obbligo di legge** da **buona prassi**: nel report le due cose hanno
   severità diversa.
4. Non produci consulenza legale: produci documentazione tecnica da far validare a DPO/legale.

## Perché qui quasi tutto è "categoria particolare"

MobilitasHQ tratta **dati relativi alla salute** (art. 4(15) e art. 9 GDPR): anamnesi, diagnosi
osteopatiche, audio della visita, trascrizioni, referti. Conseguenze automatiche:

- serve una base giuridica **doppia**: art. 6 **e** art. 9;
- per la finalità di cura vale art. 9(2)(h) + art. 9(3) (segreto professionale) e **non serve
  consenso** (Garante, chiarimenti 7 marzo 2019, n. 55) — il consenso serve per finalità
  *ulteriori* (marketing, refertazione online, ricerca);
- si applicano le **misure di garanzia** ex art. 2-septies Codice Privacy
  (Provv. Garante n. 146 del 5 giugno 2019);
- la DPIA (art. 35) è di regola **obbligatoria** (dati sanitari su larga scala / trattamenti
  dell'elenco Garante n. 467/2018);
- il rischio di una violazione è per definizione **elevato** ⇒ notifica e comunicazione agli
  interessati vanno pianificate.

## Riferimenti dettagliati

| File | Contenuto |
|------|-----------|
| `references/01-articoli-chiave-gdpr.md` | Articoli GDPR con il requisito operativo e cosa cercare nel codice |
| `references/02-dati-sanitari-italia.md` | Codice Privacy, provvedimenti Garante, Sistema TS, fatturazione sanitaria |
| `references/03-trasferimenti-e-fornitori.md` | Art. 28 (DPA), artt. 44-49, EU-US DPF, SCC, TIA, fornitori AI |
| `references/04-sicurezza-e-breach.md` | Art. 32, amministratori di sistema, log, backup, artt. 33-34 |
| `references/05-dpia-e-ai.md` | Art. 35, elenco Garante 467/2018, AI Act (Reg. UE 2024/1689) |
| `references/06-conservazione-e-diritti.md` | Retention, artt. 12-22, informative, tempi di risposta |

## Mappa rapida requisito → dove si verifica nel gestionale

| Requisito | Dove cercare l'evidenza |
|-----------|--------------------------|
| Art. 5(1)(c) minimizzazione | entity/DTO: campi personali non necessari, log verbosi |
| Art. 5(1)(e) limitazione conservazione | job di purge, soft-delete, backup retention |
| Art. 9 base giuridica | flussi di raccolta consenso, informativa, accettazione DocuSign |
| Art. 15/17/20 diritti | endpoint di export/cancellazione, procedura manuale documentata |
| Art. 25 privacy by design/default | default dei flag, visibilità dati per ruolo |
| Art. 28 responsabili | integrazioni esterne (`INTEGRATIONS.md`) → DPA firmato? |
| Art. 30 registro | `docs/privacy/02-registro-trattamenti.md` vs trattamenti reali nel codice |
| Art. 32 sicurezza | JWT/ruoli, cifratura at-rest/in-transit, audit trail, gestione segreti |
| Art. 33/34 breach | procedura documentata, registro violazioni, monitoraggio |
| Art. 35 DPIA | `docs/privacy/03-*`, `04-*` vs trattamenti AI/audio effettivi |
| Artt. 44-49 trasferimenti | chiamate a vendor USA (Anthropic, OpenAI, Google, ElevenLabs) |

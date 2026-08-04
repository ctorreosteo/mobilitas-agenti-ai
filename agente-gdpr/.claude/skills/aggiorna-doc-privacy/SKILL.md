---
name: aggiorna-doc-privacy
description: Come aggiornare e mettere a norma i file Markdown del gestionale MobilitasHQ — quali documenti toccare, quali creare, stile e intestazioni da rispettare, come inserire i riferimenti normativi, come marcare ciò che non è verificabile. Usa questa skill ogni volta che stai per scrivere o modificare un .md nei repository del gestionale.
---

# Aggiornare la documentazione perché sia a norma

Si modificano **solo file `.md`**, solo dentro i repository del gestionale
(`/Users/carlitos/mobilitas-backend`, `/Users/carlitos/mobilitas-frontend`), solo sul branch
`gdpr/aggiornamento-docs`. Nessun file di codice, in nessuna circostanza.

Sono i repository di lavoro dell'utente: non toccare mai il suo lavoro non committato.

## Principio guida

Un documento privacy è un **atto di accountability** (art. 5(2)): quello che c'è scritto deve
essere vero e dimostrabile. Perciò:

- si scrive solo ciò che risulta dalle **evidenze** raccolte in `report/evidenze/`;
- ciò che non è verificabile dal codice si marca `[DA VERIFICARE — <cosa serve>]` oppure
  `[DA COMPILARE — chiedere al Titolare]`, **e** genera una voce nel report criticità;
- **non si cancella** un'informazione scomoda: se una misura dichiarata non esiste, il documento
  va corretto (togliendo l'affermazione falsa) e il gap va nel report;
- non si inventano mai: date di firma, versioni di DPA, nomi di consulenti, esiti di audit,
  certificazioni, tempi di conservazione non deliberati.

## Documenti da mantenere allineati (backend, `docs/privacy/`)

| File | Cosa aggiornare a ogni audit |
|------|------------------------------|
| `01-ruoli-e-responsabilita.md` | tabella art. 28 dei fornitori realmente usati dal codice; ruoli applicativi coerenti con `Ruolo.TipoRuolo`; amministratori di sistema; valutazione DPO motivata |
| `02-registro-trattamenti.md` | **il cuore**: un trattamento per riga con finalità, base art. 6 **e** art. 9, categorie di interessati e di dati, destinatari, trasferimenti + garanzia, **termini di conservazione**, misure di sicurezza |
| `03-dpia-01-audio-whisper-t2.md` | flusso audio reale, campi inviati, retention lato fornitore, misure |
| `04-dpia-02-ai-clinica-anthropic-t3.md` | prompt reali, dati inclusi, supervisione umana, no-training, rischio residuo |

## Documenti che spesso mancano e vanno creati (sono `.md`, quindi consentiti)

| Nuovo file proposto | Contenuto |
|---------------------|-----------|
| `05-informative.md` | testi delle informative per paziente, lead, dipendente, candidato, operatore |
| `06-procedura-data-breach.md` | rilevazione, qualificazione, notifica 72h, comunicazione, registro violazioni |
| `07-procedura-diritti-interessati.md` | canale, verifica identità, tempi, sistemi da interrogare, modelli di risposta |
| `08-politica-conservazione.md` | matrice categoria → termine → base → meccanismo tecnico che lo applica |
| `09-misure-di-sicurezza.md` | misure art. 32 **effettivamente implementate**, con evidenza |
| `10-fornitori-e-trasferimenti.md` | registro responsabili ex art. 28 + basi di trasferimento extra-UE |
| `11-amministratori-di-sistema.md` | designazioni, log accessi, verifica annuale (Provv. Garante 27/11/2008) |
| `12-formazione-e-autorizzati.md` | designazione autorizzati ex art. 2-quaterdecies, istruzioni, formazione |
| `99-criticita-e-gap-aperti.md` | **copia del report criticità**, per farlo viaggiare con i docs |

Crea solo i documenti che servono davvero, con contenuto reale: un documento vuoto o generico
è peggio della sua assenza, perché simula conformità.

## Convenzioni redazionali del progetto

Rispetta lo stile già presente nei documenti esistenti.

1. **Intestazione di stato** in cima, come negli altri documenti:

```markdown
# <Titolo>

> **Stato documento**: allineato al codice backend al <AAAA-MM-GG>.
> **Ambito**: <perimetro del documento>.

Hub tecnico: [docs/README.md](../README.md). <altri link pertinenti>
```

2. **Tabella di testata** con Documento / Titolare / Versione / Ultimo aggiornamento /
   Sistema di riferimento (come in `01-ruoli-e-responsabilita.md`).
3. **Riferimenti normativi espliciti** per articolo, in una riga dedicata sotto la testata.
4. **Nota di validazione** dove serve: *"Documento interno di governance, da far validare al
   consulente privacy / DPO prima dell'adozione."*
5. Italiano, tono tecnico-giuridico, tabelle brevi, niente prosa decorativa.
6. **Link relativi corretti**: da `docs/privacy/` verso `docs/guides/` si scrive `../guides/…`.
7. **Ogni nuovo `.md` in `docs/` va aggiunto all'hub `docs/README.md`** (convenzione del repo).
8. Aggiorna la **data** e la **versione** dei documenti che modifichi; nella riga versione
   annota in una frase *cosa* è cambiato.

## Frontend

Se `/Users/carlitos/mobilitas-frontend/docs/privacy/` non esiste, crealo con un `README.md` che rimanda
alla documentazione privacy del backend (fonte unica) e contenga solo ciò che è specifico del
client: storage locale, token, script di terze parti, dati mostrati per ruolo, cookie.
Aggiorna anche l'hub `docs/README.md` del frontend.

## Cosa NON fare

- Non riscrivere da zero un documento esistente: **aggiornalo** conservando struttura e contenuti
  validi. Il diff deve essere leggibile e revisionabile.
- Non spostare o rinominare file esistenti.
- Non modificare `.md` che non c'entrano con la privacy **se non** per le parti che contengono
  affermazioni sbagliate su trattamento dei dati (es. una guida che suggerisce di loggare il
  payload della cartella clinica).
- Non toccare `README.md` di root se non per aggiungere il rimando alla sezione privacy.
- Non annunciare come "conforme" ciò che è solo "documentato".

## Chiusura del lavoro

Al termine, nel repository toccato:

```bash
git add -A ':(glob)**/*.md'   # il filtro è obbligatorio: 'git add -A' nudo è bloccato dall'hook
git status --short            # deve contenere SOLO file .md
git commit -m "docs(privacy): allineamento GDPR <AAAA-MM-GG>"
```

Mai `git commit -a`: rastrellerebbe le modifiche in corso dell'utente dentro un commit di
documentazione.

Se `git status` mostra un file non `.md`, **fermati**: qualcosa ha modificato il codice.
Ripristinalo con `git checkout -- <file>` e segnala l'accaduto all'utente.
Il push lo fa l'utente.

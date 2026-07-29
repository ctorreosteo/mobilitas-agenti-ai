---
description: Scrive o aggiorna report/CRITICITA-GDPR.md con tutto ciò che manca da implementare
argument-hint: "[--aggiorna per conservare gli ID esistenti]"
---

Compila il report delle criticità GDPR. Segui la skill `report-criticita`.

**Il report segnala: non implementa e non corregge nulla.**

## Procedura

1. Se `report/CRITICITA-GDPR.md` esiste già, **leggilo prima**: gli ID (`GDPR-001`…) vanno
   conservati per le criticità ancora aperte, e va aggiornato lo stato di quelle risolte
   (`chiusa il <data> — <come>`). Nuove criticità continuano la numerazione.
2. Raccogli il materiale: `report/evidenze/*` (in particolare le `[ASSENTE]` e le `[IPOTESI]`),
   le divergenze di `09-riconciliazione.md`, le criticità segnalate da `redattore-doc`, i punti
   `[DA VERIFICARE]` lasciati nei documenti.
3. Escludi ciò che è già stato risolto aggiornando la documentazione: quello va nella sezione
   "Cosa è stato risolto in questa sessione".
4. Scrivi una **scheda per criticità** nel formato della skill: severità, articoli, area,
   componente, fatto rilevato **con evidenza `file:riga`**, perché è un problema, cosa manca da
   implementare (indicazione, non implementazione), chi decide, stato.
5. Calibra le severità con la regola: art. 9 / art. 32 su dati sanitari / artt. 44-49 ⇒ mai
   sotto ALTA. Ordina per severità.
6. Compila la sezione **"Domande al Titolare"**: l'elenco puntuale delle informazioni mancanti
   (DPA firmati, region dei bucket, decisioni sui termini di conservazione, contratti, nomine).
7. Compila **"Metodo e limiti dell'audit"**: cosa non è stato verificabile dal codice
   (configurazione di produzione, contratti, backup reali, permessi effettivi su Drive).
8. Copia il file in `workspace/mobilitas-backend/docs/privacy/99-criticita-e-gap-aperti.md`
   (è un `.md`, quindi consentito) e registralo nell'hub `docs/README.md`.
9. Lancia `revisore-gdpr` sul report per verificare evidenze e severità. Correggi i bloccanti.

## Vincoli di igiene

- Mai incollare segreti, chiavi, dati di pazienti o estratti di cartelle cliniche.
- Ogni scheda deve avere almeno una evidenza `file:riga` o una ricerca `[ASSENTE]` esplicita.

## Chiusura

Mostra all'utente la tabella di sintesi per severità, le **criticità CRITICA e ALTA** in forma
sintetica (una riga ciascuna) e il percorso del file.

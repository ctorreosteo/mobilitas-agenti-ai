# DPIA (art. 35) e intelligenza artificiale

## Quando la DPIA è obbligatoria

**Art. 35(1)**: quando il trattamento può presentare un **rischio elevato** per i diritti e le
libertà, in particolare con nuove tecnologie.

**Art. 35(3)** — casi tipici: valutazione sistematica basata su trattamento automatizzato
(profilazione) con effetti giuridici; trattamento **su larga scala di dati art. 9**;
sorveglianza sistematica di zone accessibili al pubblico.

**Elenco del Garante n. 467 dell'11 ottobre 2018** — tra le tipologie che richiedono DPIA:

- trattamenti valutativi/di scoring su larga scala;
- **trattamenti di dati sanitari** riferiti a soggetti vulnerabili, con **modalità innovative**
  (es. IoT, AI, app);
- trattamenti effettuati mediante l'uso di **tecnologie innovative** (riconoscimento vocale,
  intelligenza artificiale) combinati con dati particolari;
- trattamenti sistematici di dati biometrici o genetici;
- interconnessione di banche dati.

⇒ Per MobilitasHQ, **audio della visita → Whisper** e **testo clinico → Claude** ricadono nel
perimetro. Le DPIA esistenti (`03-dpia-01-audio-whisper-t2.md`, `04-dpia-02-ai-clinica-anthropic-t3.md`)
vanno **mantenute allineate al codice**, non riscritte.

## Contenuti minimi di una DPIA (art. 35(7))

1. **Descrizione sistematica** dei trattamenti previsti e delle finalità, incluso l'eventuale
   legittimo interesse.
2. **Necessità e proporzionalità** rispetto alle finalità.
3. **Valutazione dei rischi** per i diritti e le libertà degli interessati.
4. **Misure previste** per affrontare i rischi (garanzie, misure di sicurezza, meccanismi che
   dimostrano la conformità), tenuto conto dei diritti degli interessati.

Da aggiungere in coda, come buona prassi: **rischio residuo**, decisione se procedere,
data di riesame, esito della consultazione del DPO (art. 35(2)) e — se il rischio residuo resta
elevato — la **consultazione preventiva** del Garante (art. 36).

### Elementi che una DPIA su AI clinica deve contenere e che spesso mancano

- **Flusso dato per dato**: cosa esce dal perimetro, in quale forma, verso quale endpoint,
  in quale regione, per quanto tempo è conservato dal fornitore.
- **Pseudonimizzazione prima dell'invio**: il prompt contiene nome, data di nascita, contatti?
  Se sì, giustificare la necessità o segnalare la mancata minimizzazione (art. 5(1)(c)).
- **No-training**: impegno contrattuale del fornitore a non usare i dati per addestrare modelli.
- **Retention lato fornitore** e possibilità di zero-retention.
- **Supervisione umana**: l'output AI è una **bozza** rivista dal professionista. Va scritto e
  va verificato che il codice non renda l'output finale senza revisione ⇒ altrimenti si entra
  nell'art. 22.
- **Accuratezza e allucinazioni**: rischio di contenuto clinico errato nel fascicolo del paziente
  (art. 5(1)(d)) e misure di mitigazione.
- **Trascrizioni e audio residui**: dove restano, quando vengono cancellati.
- **Diritti dell'interessato** sull'output AI e informativa dedicata (trasparenza).

## AI Act — Regolamento (UE) 2024/1689

Non sostituisce il GDPR: si aggiunge. Punti da considerare per il gestionale:

| Tema | Nota operativa |
|------|----------------|
| **Alfabetizzazione AI (art. 4)** | Chi usa il sistema per conto del deployer deve avere un livello sufficiente di competenza sull'AI. Applicabile dal 2 febbraio 2025 ⇒ prevedere formazione documentata |
| **Ruolo** | Lo studio è **deployer** di sistemi AI di terzi (Anthropic, OpenAI, ElevenLabs); se sviluppa e mette in servizio un proprio sistema con il proprio marchio, può assumere obblighi da **provider**. Va valutato e scritto |
| **Alto rischio (Allegato III)** | Valutare se l'uso configura un sistema ad alto rischio; la semplice generazione di bozze documentali sotto supervisione umana tipicamente non lo è, ma la valutazione va **motivata**, non omessa |
| **Trasparenza (art. 50)** | Contenuti generati da AI e interazione con sistemi conversazionali vanno resi riconoscibili: l'assistente vocale deve dichiarare di essere un sistema AI |
| **Tempistiche** | Applicazione scaglionata (divieti e alfabetizzazione dal 2025, GPAI dal 2025, alto rischio dal 2026-2027) — `[verificare lo stato di applicazione alla data dell'audit]` |

## Come valutare "larga scala"

Non è definito numericamente. Criteri EDPB (WP248 rev.01): numero di interessati, volume e
varietà dei dati, durata, estensione geografica. Un singolo studio con un bacino locale di
pazienti **non** è automaticamente "larga scala" — ma la valutazione va **scritta e motivata**,
perché da essa dipendono l'obbligo di DPO (art. 37(1)(c)) e parte degli obblighi di DPIA.
Un documento che afferma "non siamo larga scala" senza motivazione è una criticità **MEDIA**.

# Architettura della Bibbia — struttura, capitolo per capitolo

Questo file è la specifica della **struttura fissa**. Va rispettata nell'ordine.

## Cos'è una Bibbia e cosa non è

Una Bibbia è **tutto quello che devi sapere su una condizione per poterla risolvere in poche sedute**. Venti pagine di conoscenza, non di istruzioni.

| La Bibbia risponde a | La Procedura (documento separato, 2 pagine) risponde a |
|---|---|
| Che cos'è, perché succede | Cosa fai alla prima seduta |
| Quali meccanismi la tengono in piedi | Quali tecniche, in che ordine |
| Come si riconosce il sottotipo | Quanti minuti per blocco |
| Perché le mani possono agire | Quali esercizi, con che dose |
| Quanto è solido tutto questo | Come misuri e quando rivaluti |

**Confine netto:** la Bibbia arriva fino al **razionale della leva** ("il collo può agire sull'acufene perché C2 proietta sul nucleo cocleare, e questo è quanto è solido"). Si ferma **prima** del gesto ("inibizione dei sub-occipitali, 3 minuti"). Se ti ritrovi a scrivere una sequenza, dei minuti o una dose, sei uscito dalla Bibbia.

Chiusura obbligatoria del Capitolo 11: *"Il come si fa non è qui. Sta nella Procedura di [condizione]: due pagine, tecniche, dosi e piano delle sedute."*

---

## Le cinque regole di struttura che tengono in piedi il documento

Sono la parte che il vecchio impianto sbagliava. Valgono in **ogni** capitolo.

### 1. Un capitolo = una domanda

I titoli sono domande in italiano corrente, non etichette. **"Cosa si rompe"**, non "Parte III — Fisiopatologia". Il lettore che scorre l'indice deve capire cosa troverà senza aprire il capitolo.

I capitoli si citano **per nome**, mai per numero: *"come hai visto in «Cosa si rompe»"*, mai *"vedi §5.2"*.

### 2. Ogni capitolo si apre e si chiude uguale

**Apertura — `> **In una riga:** …`** — la tesi del capitolo in una frase sola, prima di qualunque spiegazione. È l'unica cosa che il lettore di fretta leggerà: deve bastargli.

**Chiusura — `**Le tre cose da ricordare**`** — esattamente tre bullet, una riga ciascuno. Non un riassunto: le tre cose che cambiano il tuo comportamento in stanza.

### 3. L'incertezza esce dal testo

È la regola più importante, e la cura del difetto capitale delle vecchie procedure: **frasi in cui il claim, la qualificazione, la citazione e l'istruzione stavano tutti nello stesso periodo**, illeggibili.

D'ora in poi la prosa **afferma**, pulita e diretta. L'onestà la porta un'etichetta separata, su una riga a sé:

```
Il collo può alzare o abbassare il volume dell'acufene. L'informazione dei
muscoli cervicali alti entra nella via uditiva al primo relè, il nucleo
cocleare dorsale, e ne cambia il guadagno.

> **Quanto è solido:** PROBABILE — dimostrato nell'animale (Shore, Nat Rev
> Neurol 2016). Nell'uomo il ponte è un ragionamento, non una prova.
```

Le quattro etichette, e nient'altro:

| Etichetta | Quando si usa |
|---|---|
| **DIMOSTRATO** | RCT o revisioni sistematiche solide, fonte citata |
| **PROBABILE** | razionale forte + evidenza parziale, indiretta o solo animale |
| **IPOTESI** | meccanismo fisiologico coerente, nessuno studio diretto sul punto |
| **RAGIONAMENTO** | cornice clinica interna (Motore Clinico, CC/CP, lesione primaria) — si scrive "si ipotizza", mai come fatto |

Ogni meccanismo, ogni leva e ogni modello ne porta **una**. Un'affermazione senza etichetta è un'affermazione presentata come certa: se non lo è, è un claim gonfiato.

### 4. Quattro soli tipi di box

Sempre come blockquote, sempre con la stessa apertura in grassetto. Non inventarne altri: la prevedibilità grafica è metà della leggibilità.

- `> **Definizione.** …` — un termine tecnico spiegato in parole comuni, alla prima comparsa.
- `> **Quanto è solido.** …` — l'etichetta di evidenza (regola 3).
- `> **Attenzione.** …` — sicurezza, limite di campo, cosa non è tuo.
- `> **Cosa cambia per te.** …` — la conseguenza pratica di quello che hai appena letto.

### 5. Le tabelle sono griglie, non paragrafi in gabbia

**Massimo 4 colonne. Massimo 8 parole per cella. Nessuna eccezione.** Se il contenuto non ci sta, non è una tabella: è prosa. La tabella dei cinque modelli della vecchia procedura acufeni aveva celle da 150 parole — è il modo più efficace conosciuto per rendere illeggibile un'informazione importante.

---

## I capitoli

### Capitolo 0 — Come si usa questa Bibbia

Mezza pagina. Serve a orientare, non a introdurre.

- **A chi parla:** l'osteopata del team.
- **Cosa c'è qui e cosa no:** la tabella Bibbia/Procedura di apertura, in due righe.
- **Come si leggono le etichette:** le quattro etichette di solidità, spiegate una volta per tutte.
- **Due modi di leggerla:** i capitoli da leggere in venti minuti prima del primo paziente; quelli da studiare con calma.
- Chiusura fissa: **"Buon nutrimento!"**

Niente saluti, niente premesse sull'importanza della condizione.

### Capitolo 1 — Chi ti trova davanti

**Scopo:** rendere concreto prima di rendere astratto. Il lettore deve riconoscere un paziente vero prima di leggere un meccanismo.

Fonte obbligatoria: i campi `sintomi`, `soluzioni_provate`, `farmaci`, `esami_strumentali`, `ads_pain_points`, `obiezioni_specifiche` del problema in `_dati/problemi.json`. Sono la voce reale del paziente: si usano, non si parafrasano in linguaggio clinico.

Contenuto:
- **Come lo racconta lui** — le parole che usa davvero, tra virgolette.
- **Cosa ha già fatto** — esami, farmaci, tentativi, e cosa gli hanno detto. È il percorso che spiega perché arriva stanco e diffidente.
- **Cosa nessuno ha guardato** — il buco del percorso standard, dichiarato senza denigrare nessuno.
- **Le tre domande che ti farà** — poste qui, con la risposta rimandata al capitolo che la contiene.

### Capitolo 2 — Che cos'è davvero

- **Definizione** medica corrente, con la fonte.
- **Quanto è diffusa**, chi colpisce, come evolve se non fai nulla (storia naturale — serve a non prendersi meriti che sono della fluttuazione spontanea).
- **Cosa dicono le etichette diagnostiche** che il paziente porta, e cosa **non** dicono. La diagnosi è atto medico: qui si spiega come si legge un referto, non come si formula.
- **Cosa non è**: le condizioni che le somigliano e con cui si confonde.

### Capitolo 3 — Le strutture in gioco

L'anatomia che conta per **questa** condizione, e nient'altro. Il lettore ha una laurea: non gli spieghi cos'è il diaframma, gli spieghi cosa fa il diaframma **qui**.

Per ogni struttura, tre righe secche: **cos'è → cosa fa → perché conta in questa condizione**. Da 4 a 8 strutture. Il criterio di inclusione è uno: se non compare in nessun meccanismo del Capitolo 5, non entra.

È il capitolo delle **chicche anatomiche** — il nervo di Jacobson, il legamento di Pinto, i legamenti sospensori: quelle che fanno dire *"questa non la sapevo"*. Una o due, non dieci.

### Capitolo 4 — Come funziona quando funziona

La fisiologia normale della funzione coinvolta. Non si capisce un guasto senza conoscere il funzionamento.

Una catena di eventi in ordine, numerata, in linguaggio da clinico. Chiude con la frase-cerniera che apre il capitolo successivo: **"Questo è il sistema che funziona. Ora vediamo dove si rompe."**

### Capitolo 5 — Cosa si rompe: i meccanismi

**Il cuore della Bibbia.** Da 3 a 6 meccanismi, mai di più.

Ogni meccanismo ha **sempre** la stessa struttura, nello stesso ordine:

1. **Titolo che dice il meccanismo**, non che lo etichetta ("Il guadagno alzato troppo", non "Meccanismo 2: central gain").
2. **La catena, in tre-cinque passaggi numerati.** Da cosa parte a dove arriva.
3. **`> Quanto è solido:`** l'etichetta + una riga di motivo + la fonte.
4. **Come si vede addosso al paziente** — i segni concreti che ti fanno sospettare che sia questo a comandare.
5. **Una metafora**, in grassetto, isolata su una riga. Una sola per meccanismo, fisica e concreta.

I meccanismi si ordinano dal **più solido al meno solido**, non dal più suggestivo. Un lettore critico che parte dal migliore è disposto a seguirti anche sul quarto.

### Capitolo 6 — Non è una condizione sola: i sottotipi

Da 3 a 6 sottotipi, presentati come **pattern**, non come etichette diagnostiche.

Tabella d'apertura a 4 colonne (`Sottotipo | Segnale che lo riconosce | Meccanismo che comanda | Quanto puoi fare`), poi un paragrafo per sottotipo che aggiunge quello che la tabella non può contenere.

**Almeno un sottotipo deve essere di quelli su cui puoi poco**, con detto chiaramente a chi va mandato. Se sono tutti trattabili, stai vendendo.

### Capitolo 7 — La lettura osteopatica: i cinque modelli

L'**impalcatura** della professione applicata alla condizione. Fonte: `cinque-modelli-osteopatici.md`, da leggere prima di scrivere questo capitolo.

**Una sezione breve per modello** — Biomeccanico-Strutturale, Respiratorio-Circolatorio, Neurologico, Metabolico-Energetico, Comportamentale-Biopsicosociale — ciascuna con quattro voci brevi e nient'altro:

- **Cosa governa qui**
- **Gli attori** (le strutture del Capitolo 3)
- **I segnali che ti dicono che pesa in questo paziente**
- **`> Quanto è solido:`**

**Non una tabella unica.** Cinque sezioni da dieci righe si leggono; una tabella con cinque celle da 150 parole no.

Vincoli di scope: il viscerale **non è un modello a sé** (sta nel Biomeccanico per la meccanica e nel Neurologico per il riflesso); il Trauma **non è un modello** (è un modificatore che si cerca in anamnesi). Dichiarare l'evidenza onesta di ogni modello, compresi i deboli: il modello debole dichiarato rafforza la corazza, non la indebolisce.

### Capitolo 8 — Come ragiono davanti a questo paziente

Il **Motore Clinico** (`motore-clinico.md`): il ragionamento del Sistema Dominante, che decide **su quale modello agire per primo in questo paziente**. Va scritto come ragionamento clinico, mai come prova — etichetta `RAGIONAMENTO`, sempre.

Contenuto, in quest'ordine:
1. **La punta e il sommerso** applicati alla condizione, con due o tre pazienti-tipo che hanno lo stesso sintomo e sommersi diversi.
2. **Perché si indaga dall'alto:** il corpo sacrifica il comfort per le funzioni vitali; il dominante è il piano più alto che risulta disfunzionale.
3. **La prova della chiave di volta:** tratti in prova, poi rivaluti — e **il marker che decide appartiene a un piano che non hai toccato**. Questo dettaglio è ciò che distingue una verifica da un auto-inganno.
4. **La Road Map**, 5 o 6 passi numerati, in ordine di priorità.
5. **I tre stati del paziente** (in difesa / emotivo / razionale) e cosa cambia nel modo di parlargli.

### Capitolo 9 — Dove finisce il nostro campo

Il capitolo che rende la Bibbia consegnabile. Obbligatorio, mai accorciato.

- **Le bandiere rosse**, in elenco, ciascuna con **a chi si manda** e **con che urgenza**. Non annacquate, non generiche.
- **Il cancello d'ingresso:** cosa deve essere già stato fatto dal medico prima che tu apra un ciclo.
- **Cosa fanno i farmaci** che il paziente prende, e perché non li commenti mai. Nessuna valutazione, nessun suggerimento di modifica: decide il prescrittore.
- **Il perimetro legale:** DPR 131/2021 (tecniche esclusivamente manuali, non invasive, esterne; diagnosi riservata al medico), status di professione sanitaria (DPCM 2026), consenso informato e dati di salute (art. 9 GDPR).
- **Cosa succede se sbagli campo** — detto una volta, senza drammatizzare.

### Capitolo 10 — Cosa dice la scienza

- **L'ancora scientifica:** chi è, dove lavora, cosa ha cambiato. Un ricercatore **reale, vivente, verificato**, il più autorevole in terapia manuale su questa condizione.
- **Gli studi cardine**, in tabella a 3 colonne: `Autore, anno (link PubMed) | Cosa ha misurato | Cosa ti autorizza a fare`. La terza colonna è la sola che conta: non riassumi l'abstract, dici cosa cambia per te. Da 4 a 7 studi. Tutti verificati sul web in questa sessione.
- **Cosa possiamo dire e cosa no** — due elenchi affiancati, brutalmente espliciti. È la sezione che ti fa reggere davanti a uno specialista.
- **Dove la letteratura è sottile**, dichiarato. Su molte condizioni non esiste un ricercatore-ancora: in quel caso si dichiara, si sceglie il gruppo di ricerca più vicino e si abbassa il tono di tutte le etichette. Una Bibbia onesta su un'evidenza povera vale più di una gonfiata.

### Capitolo 11 — Perché le mani possono cambiare qualcosa

Il razionale delle leve. **Nessun protocollo, nessuna dose, nessuna sequenza, nessun minuto.**

Struttura fissa: si riprendono **i meccanismi del Capitolo 5, uno per uno**, e per ciascuno si dice:

- **Su cosa può agire una mano** (quale struttura, quale via)
- **Che effetto ci si aspetta** — un effetto sul sistema, non "sciogliere la tensione"
- **`> Quanto è solido:`** l'etichetta, di nuovo, perché qui la tentazione di gonfiare è massima
- **In quanto tempo si vedrebbe**, se l'effetto c'è

Poi, sempre:
- **Cosa fa l'osteopata che il resto del percorso non fa** — tre punti sui **meccanismi**, mai sulle persone.
- **Cosa non possono fare le mani** su questa condizione, detto per primo se il limite è importante.
- La chiusura obbligatoria che rimanda alla Procedura.

### Capitolo 12 — Cosa dire al paziente

Conoscenza, non copione di vendita.

- **Lo script di spiegazione:** massimo 100 parole, interamente in corsivo, tra virgolette, pronto da recitare, con la metafora centrale della Bibbia e **zero parole tecniche**.
- **Le obiezioni e le risposte oneste:** le `obiezioni_specifiche` da `problemi.json`, ciascuna con una risposta che non promette l'esito.
- **Cosa non promettere mai**, in tre righe.

### Appendice A — Glossario

Ogni termine tecnico comparso nella Bibbia, in ordine alfabetico, **una riga ciascuno**, in parole comuni. Se un termine è nel testo e non è qui, o è qui e non è nel testo, il glossario è sbagliato.

È anche il collaudo del documento: se il glossario supera i 40 termini, la Bibbia è scritta troppo tecnica.

### Appendice B — Le fonti

Bibliografia completa: autore, anno, titolo, rivista, **link PubMed verificato**. Nell'ordine in cui compaiono nel testo.

---

## Lunghezza e distribuzione

**8.000–12.000 parole** — circa venti pagine. Sotto le 7.000 non è una Bibbia, è un riassunto. Sopra le 13.000 nessuno la finisce.

| Capitolo | Quota |
|---|---|
| 0–1 (uso, paziente) | ~8% |
| 2–3 (cos'è, strutture) | ~14% |
| 4 (fisiologia normale) | ~8% |
| 5 (meccanismi) | ~20% |
| 6 (sottotipi) | ~8% |
| 7 (cinque modelli) | ~12% |
| 8 (ragionamento) | ~10% |
| 9 (limiti di campo) | ~7% |
| 10 (scienza) | ~8% |
| 11–12 (leve, paziente) | ~5% |

Le appendici non contano nel totale.

---

## Il secondo deliverable

Ogni Bibbia produce anche la **Mappa concettuale di sintesi** — una pagina, specifica in `mappa-concettuale.md`. Non è un riassunto: è lo schema che tieni accanto mentre studi e a cui torni sei mesi dopo.

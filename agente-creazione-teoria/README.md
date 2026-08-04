# Teoria — Skill Direttore Osteopatico (Mobilitas / OsteoTouch)

Cartella di lavoro per la redazione e revisione delle **Bibbie teoriche** delle condizioni
trattate in studio.

## Cos'è una Bibbia

Venti pagine con **tutto quello che un osteopata deve sapere su una condizione per poterla
risolvere in poche sedute**. Cos'è, perché succede, quali meccanismi la tengono in piedi,
quanto è solido ciò che affermiamo, dove finisce il nostro campo, perché le mani possono
cambiare qualcosa.

**Non è una procedura operativa.** Tecniche, dosi, sequenze e piano delle sedute stanno in un
documento separato di due pagine, prodotto da `agente-creazione-procedure`.

| La Bibbia (qui, ~20 pagine) | La Procedura (altro agente, 2 pagine) |
|---|---|
| Che cos'è, perché succede | Cosa fai alla prima seduta |
| Quali meccanismi la tengono in piedi | Quali tecniche, in che ordine |
| Come si riconosce il sottotipo | Quanti minuti per blocco |
| Perché le mani possono agire | Quali esercizi, con che dose |
| Quanto è solido tutto questo | Come misuri e quando rivaluti |

Ogni Bibbia produce anche una **Mappa concettuale di sintesi**: una pagina, sei blocchi, quella
a cui si torna sei mesi dopo.

## Struttura

```
.claude/skills/                     skill di progetto (attive lavorando in questa cartella)
  direttore-osteopatico-teoria/     AUTORE — redige la Bibbia + la Mappa concettuale
    ├─ SKILL.md
    ├─ references/
    │   ├─ architettura-bibbia.md      i 13 capitoli e le 5 regole di struttura
    │   ├─ regole-di-scrittura.md      come si scrive (la leggibilità è un requisito)
    │   ├─ cinque-modelli-osteopatici.md  impalcatura del Capitolo 7
    │   ├─ motore-clinico.md           il ragionamento del Capitolo 8
    │   ├─ ancore-scientifiche.md      metodo di ricerca e verifica
    │   ├─ ancore-verificate.md        ancore già validate (cervicale, lombalgia, Achille)
    │   ├─ mappa-concettuale.md        spec del secondo deliverable
    │   ├─ sistema-libreria.md         coerenza del corpus
    │   ├─ revisione-e-sintesi.md      i cinque livelli e la regola di triage
    │   ├─ rubrica-punteggio.md        cancello: sotto 90/100 non si consegna
    │   └─ checklist-qualita.md        cancello: un solo NO = si corregge
    └─ scripts/
        ├─ build_docx.py
        └─ verifica_conservazione.py   collaudo deterministico v5 vs v6

  direttore-osteopatico-specialista/       1º liv. — medico specialista di riferimento
  direttore-osteopatico-medico-generale/   1º liv. — MMG che invia i pazienti
  direttore-osteopatico-sicurezza-tecniche/ 1º liv. — dove la teoria porta a far male
  direttore-osteopatico-fisioterapista-ebp/ 1º liv. — scettico evidence-based
  direttore-osteopatico-compliance/        1º liv. — legale / deontologia / GDPR
  direttore-osteopatico-neolaureato/       1º liv. — comprensibilità alla prima lettura
  direttore-osteopatico-sistema-dominante/ 1º liv. — il ragionamento del Motore Clinico
  direttore-osteopatico-modelli/           1º liv. — uso e bilanciamento dei cinque modelli
  direttore-osteopatico-neuromodulazione/  1º liv. — il meccanismo neurofisiologico
  direttore-osteopatico-clinico-esperto/   1º liv. — "il paziente guarisce davvero?"
  direttore-osteopatico-fedelta-bibbia/    2º liv. — audit contro l'architettura
  direttore-osteopatico-apprendimento/     3º liv. — il documento insegna o fa solo sapere?
  direttore-osteopatico-editor/            4º liv. — asciugatura
  direttore-osteopatico-chiarezza/         5º liv. — RISCRIVE tutto in linguaggio semplice
  direttore-osteopatico-collaudo/          CANCELLO — conservazione v5→v6, script + semantica

bibbie-generate/
  _dati/livelli.json                manifesto: chi è autore e chi revisore, per livello
  _dati/problemi.json               materia prima (sintomi, obiezioni, red flag)
  _dati/deviazioni-dal-metodo.md    dove il metodo interno è stato trovato sbagliato
  _workflow/genera-bibbie.workflow.js
  <slug>/                           lavorazione in markdown, v1 → v6

outputs/<slug>/                     Bibbia_<Condizione>.docx + Mappa_<Condizione>.docx
```

## L'architettura della Bibbia — i 13 capitoli

| # | Capitolo | Cosa contiene |
|---|---|---|
| 0 | Come si usa questa Bibbia | Orientamento, etichette, "Buon nutrimento!" |
| 1 | Chi ti trova davanti | Il paziente reale, dai dati di `problemi.json` |
| 2 | Che cos'è davvero | Definizione, diffusione, storia naturale |
| 3 | Le strutture in gioco | Solo l'anatomia che conta, più una chicca |
| 4 | Come funziona quando funziona | Fisiologia normale |
| 5 | Cosa si rompe | **Il cuore.** 3-6 meccanismi, dal più solido al meno |
| 6 | Non è una condizione sola | I sottotipi come pattern |
| 7 | La lettura osteopatica | I cinque modelli, una sezione breve ciascuno |
| 8 | Come ragiono davanti a questo paziente | Il Motore Clinico |
| 9 | Dove finisce il nostro campo | Bandiere rosse, cancello, farmaci, perimetro legale |
| 10 | Cosa dice la scienza | Ancora, studi verificati, cosa si può dire e cosa no |
| 11 | Perché le mani possono cambiare qualcosa | Razionale delle leve. **Niente protocolli** |
| 12 | Cosa dire al paziente | Script sotto 100 parole, risposte alle obiezioni |
| A | Glossario | Ogni termine tecnico, una riga |
| B | Le fonti | Bibliografia con link verificati |

**Lunghezza: 8.000–12.000 parole**, appendici escluse.

### Le cinque regole di struttura

Sono la parte che il vecchio impianto delle procedure sbagliava, e valgono in ogni capitolo.

1. **Un capitolo = una domanda.** Titoli in italiano corrente, mai "Parte III — Fisiopatologia". I capitoli si citano per nome, mai per numero.
2. **Apertura e chiusura fisse.** Ogni capitolo apre con `> **In una riga:**` (la tesi) e chiude con **Le tre cose da ricordare** (esattamente tre).
3. **L'incertezza esce dal testo.** La prosa afferma; l'onestà la porta un box separato `> **Quanto è solido:**` con una di quattro etichette — DIMOSTRATO / PROBABILE / IPOTESI / RAGIONAMENTO. È la cura del difetto capitale dei vecchi documenti: periodi in cui claim, qualificazione, citazione e istruzione stavano tutti insieme.
4. **Quattro soli tipi di box:** Definizione · Quanto è solido · Attenzione · Cosa cambia per te.
5. **Tabelle: massimo 4 colonne, massimo 8 parole per cella.** Se non ci sta, è prosa.

## Pipeline editoriale — cinque livelli

Ruoli e livelli sono dichiarati in `bibbie-generate/_dati/livelli.json`: è l'unico file da
toccare per aggiungere, togliere o spostare un revisore.

1. **`teoria`** redige la v1 (Bibbia + Mappa).
2. **1º livello** — panel avversariale in parallelo sul contenuto (dieci lenti) → **v2**.
3. **2º livello** — `fedelta-bibbia`, audit contro l'architettura → **v3**.
4. **3º livello** — `apprendimento`: il documento insegna o fa solo sapere? → **v4**.
5. **4º livello** — `editor`: toglie ridondanza, riporta nel range → **v5**.
6. **5º livello** — `chiarezza`: **riscrive l'intero documento da capo** con lessico e sintassi
   semplici, senza perdere una sola informazione → **v6**.
7. **Cancello** — `collaudo`: verifica che la riscrittura non abbia perso niente → **v6 consegnabile**.

Il quinto livello non è un revisore che consiglia: è un riscrittore che produce il deliverable.
L'ordine 4º→5º non è invertibile: **si semplifica un testo già asciutto, non si asciuga un testo
già semplificato** — l'asciugatura ri-comprimerebbe le frasi e annullerebbe il lavoro.

Analogamente, l'apprendimento sta **prima** dell'editor apposta: può chiedere qualche riga in
più, e l'editor asciuga il risultato.

### Il cancello di conservazione

La riscrittura del quinto livello è l'unico passaggio della catena in cui **ogni singola frase
cambia** — ed era l'unico che nessuno verificava: il documento consegnato era l'unica versione
mai controllata.

`collaudo` chiude quel buco. **Non è un sesto revisore** e non giudica la qualità, chiusa a
monte: confronta v5 e v6 e verifica la sola **conservazione**. Gira in due strati — uno script
deterministico (`verifica_conservazione.py`: etichette, PMID, numeri, struttura, tabelle,
lunghezza, promesse e materiale operativo introdotti) e un collaudatore semantico per ciò che
nessun conteggio vede: etichette riancorate a un altro claim, informazione persa per
assorbimento, qualificazioni cadute, verbi irrigiditi.

Se trova violazioni, il riscrittore fa fino a **due riparazioni chirurgiche**. Se le perdite
sono diffuse, si consegna la **v5**: meno scorrevole, ma accurata — l'accuratezza sta sopra la
leggibilità nella gerarchia del metodo.

## Come si lancia

Il workflow `bibbie-generate/_workflow/genera-bibbie.workflow.js` accetta:

- uno o più slug: `["reflusso"]`, `["reflusso","cervicalgia"]`
- oppure `"tutte"` per l'intero elenco di `_dati/problemi.json`

È resiliente: retry sugli agenti critici e promozione della versione precedente se una sintesi
fallisce. Un singolo fallimento non aborta la catena.

## Note operative

- Le skill sono **project-scoped**: valgono solo dentro questa cartella.
- Il `name:` in ogni `SKILL.md` deve combaciare col nome della cartella.
- Le skill vengono caricate all'avvio sessione: dopo modifiche strutturali **riavvia la
  sessione** perché Claude Code le rilevi.

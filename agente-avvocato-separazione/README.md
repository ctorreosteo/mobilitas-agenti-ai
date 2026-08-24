# Difensore — famiglia di fatto, civile e penale

Cartella di lavoro per la difesa di **un uomo che ha cessato una convivenza di fatto** (mai
matrimonio) con la madre di suo figlio, e che va difeso su due fronti che sono uno solo: il
procedimento civile sul bambino e ogni fronte penale connesso.

## Il caso

| Elemento | Valore | Conseguenza |
|---|---|---|
| Coppia **non sposata** | convivenza *more uxorio* | Nessun assegno alla ex. Ma nessuna tutela patrimoniale per lui |
| **Un figlio** riconosciuto | ~12 mesi | Rito unico `artt. 473-bis ss. c.p.c.` |
| Rottura a **~4 mesi** dal parto | convivenza brevissima dopo la nascita | «Non c'è mai stato accudimento paterno»: il primo colpo da parare |
| Bambino **sotto i 3 anni** | prassi contraria ai pernottamenti | **Il campo di battaglia principale** |

**Il rischio che il cliente non vede:** se la casa dove vive il bambino è sua, l'`art. 337-sexies
c.c.` può assegnarla alla madre collocataria **anche se ne è l'unico proprietario e anche senza
matrimonio**. Si presidia prima, non dopo.

## Le tre idee che reggono l'agente

**1. Nessuna fonte non verificata.** Il numero di una sentenza è il punto in cui un modello
linguistico inventa con la massima verosimiglianza. Una citazione inesistente in un atto non fa
perdere quel punto: fa perdere la credibilità su tutto l'atto, comprese le venti affermazioni
vere. Ogni riferimento si verifica sul web e si registra in `fascicolo/_dati/registro-fonti.md`;
**un hook impedisce materialmente** che una citazione non registrata entri in un atto.

**2. Nessun fatto senza documento.** Ogni fatto porta la sua etichetta, fuori dalla prosa —
`PROVATO` · `DOCUMENTABILE` · `ALLEGABILE` · `NON SOSTENIBILE` — e l'ultima **non entra mai in un
atto**. Un'affermazione falsa costa più di dieci affermazioni mancanti: la controparte la smonta
e con quella contamina i fatti veri che le stanno accanto.

**3. Il perimetro è tattica, non moralismo.** Sei condotte non si consigliano mai — registrazioni
e accessi illeciti, trattenimento del minore, sospensione del mantenimento, occultamento di
redditi, prove fabbricate, denunce strumentali. Non perché siano brutte: perché **trasformano un
padre con ragione in un indagato**, e sono anche quelle che funzionano peggio. Un secondo hook le
blocca in scrittura.

## Struttura

```
CLAUDE.md                         la costituzione: caso, regole non negoziabili, metodo
scripts/test-hooks.py             collauda le protezioni: 9 casi, blocca e passa

.claude/
  settings.json                   permessi + i due hook
  hooks/
    blocca-citazioni-non-verificate.py   nessun numero di sentenza fuori dal registro
    blocca-condotte-illecite.py          le sei condotte fuori perimetro
  agents/
    ricercatore-giurisprudenza.md  cerca e VERIFICA, poi registra in append
    verificatore-citazioni.md      controlla una per una le citazioni di un atto
    redattore-atti.md              scrive il singolo atto
    avvocato-avversario.md         scrive l'atto della controparte contro di noi
  commands/
    /fascicolo  /strategia  /atto  /penale  /udienza  /tutto
  skills/
    difensore-famiglia-strategia/  AUTORE — strategia, atti, briefing
      ├─ SKILL.md
      ├─ references/
      │   ├─ verifica-delle-fonti.md        il protocollo. Si legge per primo
      │   ├─ quadro-normativo.md            cosa si applica a una coppia mai sposata
      │   ├─ rito-e-processo.md             il rito unico, e l'udienza che decide tutto
      │   ├─ figlio-infra-triennale.md      IL CUORE: il bambino ha un anno
      │   ├─ affidamento-e-collocamento.md  dove si vince davvero
      │   ├─ mantenimento-e-spese.md        i numeri, e la trappola dei quindici anni
      │   ├─ casa-familiare.md              il rischio patrimoniale maggiore
      │   ├─ convivenza-senza-matrimonio.md cosa non si può chiedere, e cosa sì
      │   ├─ penale-della-famiglia.md       i reati, da entrambi i lati
      │   ├─ prove-e-trappole.md            cosa prova cosa, e le nove trappole
      │   ├─ architettura-atto.md           la forma del deliverable
      │   ├─ rubrica-punteggio.md           cancello: sotto 90/100 non si consegna
      │   └─ checklist-qualita.md           cancello: un solo NO = si corregge
      └─ scripts/verifica_citazioni.py      collaudo deterministico v5 vs finale

    difensore-famiglia-avversario/         1º liv. — l'avvocato della madre
    difensore-famiglia-giudice/            1º liv. — chi decide
    difensore-famiglia-pubblico-ministero/ 1º liv. — l'accusa
    difensore-famiglia-curatore-minore/    1º liv. — il bambino, contro entrambi
    difensore-famiglia-ctu/                1º liv. — lo psicologo che valuta
    difensore-famiglia-penalista/          1º liv. — l'esposizione penale
    difensore-famiglia-patrimoniale/       1º liv. — i numeri
    difensore-famiglia-prove/              1º liv. — ogni fatto ha il suo documento?
    difensore-famiglia-cliente/            1º liv. — cosa farà il cliente
    difensore-famiglia-deontologia/        1º liv. — il perimetro lecito
    difensore-famiglia-fonti/              2º liv. — le citazioni reggono?
    difensore-famiglia-cassazione/         2º liv. — il ricercatore: allarga la base
    difensore-famiglia-coerenza/           3º liv. — l'ispettore delle giunture
    difensore-famiglia-editor/             4º liv. — asciugatura
    difensore-famiglia-chiarezza/          5º liv. — RISCRIVE in italiano leggibile
    difensore-famiglia-italiano-giuridico/ 6º liv. — la lingua, frase per frase
    difensore-famiglia-collaudo/           CANCELLO — citazioni e conservazione

fascicolo/
  _dati/
    caso.json                     i FATTI. Primo file che ogni agente legge
    livelli.json                  manifesto: chi rivede, e a quale livello
    registro-fonti.md             le uniche fonti citabili. Solo append
    timeline.md                   cronologia unica, civile e penale. Solo append
    deviazioni-dal-metodo.md      dove questo metodo è stato trovato sbagliato
  prove/                          i documenti del fascicolo
  _workflow/genera-difesa.workflow.js
  <pratica>/                      lavorazione, v1 → v7 + prove.md + briefing.md
```

## La pipeline — sei livelli e un cancello

Ruoli e livelli stanno in `fascicolo/_dati/livelli.json`: è l'unico file da toccare per spostare
un revisore.

1. **`strategia`** redige la v1 (atto + mappa delle prove + briefing).
2. **1º livello** — dieci lenti **in parallelo**, e sono le persone vere che decideranno o
   attaccheranno: avvocato della madre, giudice, PM, curatore del minore, CTU, penalista,
   patrimoniale, prove, cliente, deontologia → **v2**
3. **2º livello** — `fonti` **poi** `cassazione`, in quest'ordine → **v3**
4. **3º livello** — `coerenza`: contraddizioni interne, col fascicolo, fra civile e penale → **v4**
5. **4º livello** — `editor`: asciugatura → **v5**
6. **5º livello** — `chiarezza`: **riscrive l'atto da capo** in italiano leggibile → **v6**
7. **6º livello** — `italiano-giuridico`: la lingua, frase per frase → **v7**
8. **Cancello** — `collaudo`: citazioni e conservazione, contro la v5 → **depositabile**

### Perché il secondo livello è sequenziale

`fonti` **ripulisce**, `cassazione` **amplia**. Invertirli significa costruire su una base marcia
e raddoppiare il lavoro di entrambi. È l'unico livello che non gira in parallelo, ed è voluto.

### Perché il cliente è un revisore di primo livello

Perché è la prima causa di sconfitta in questa materia, davanti a qualunque argomento giuridico.
Gli atti si perdono raramente per una massima sbagliata e quasi sempre perché l'assistito ha
mandato quarantatré messaggi in una notte, si è presentato sotto casa o ha sospeso il bonifico per
ritorsione.

La lente `cliente` non giudica l'atto: **prevede cosa farà il cliente dopo averlo letto**, e
pretende che il briefing lo disinneschi prima. Un atto tecnicamente perfetto che spinge il cliente
a una condotta autolesiva è un atto fallito.

### Il cancello

Il quinto livello riscrive **ogni frase** e il sesto ne ritocca molte: è l'unico tratto in cui
tutto il testo cambia, ed è anche quello in cui una citazione può cambiare numero, un'etichetta
può salire da `ALLEGABILE` a `PROVATO`, un allegato può finire sotto un fatto diverso e una domanda
può cambiare portata.

`collaudo` chiude quel buco. Non giudica la qualità — chiusa a monte — e confronta la **v5** con la
**finale**. Gira in due strati:

**(a) Lo script deterministico**, `verifica_citazioni.py`, **due volte, una per passaggio**:

| Passaggio | Delta ammesso | Identità minima |
|---|---|---|
| v5 → v6 (chiarezza) | −5% / +10% | nessuna: ogni frase deve cambiare |
| v6 → v7 (lingua) | −3% / +5% | **60% delle frasi identiche** |

Misurare due riscritture in blocco le lascia compensare: se la prima perde e la seconda aggiunge, i
conti tornano e la perdita non si vede. E la soglia di identità rende **verificabile** la regola più
importante del sesto livello — *correggi, non riscrivere* — che prima era un'autodichiarazione,
cioè un controllo che non controllava niente.

Lo script confronta anche ogni sentenza citata con il registro: **una citazione comparsa in una
riscrittura è bloccante sempre**, anche se il numero fosse per caso giusto, perché non è mai
passata da una verifica.

**(b) Il collaudatore semantico**, che cerca ciò che nessun conteggio vede: etichette riancorate a
un altro fatto, allegati che ora sostengono un fatto diverso, informazione persa per assorbimento,
qualificazioni cadute, verbi irrigiditi, e **domande con la portata cambiata**.

Zero bloccanti, o non si deposita. Se le perdite sono diffuse si consegna la **v5**: meno
scorrevole, ma verificata. In un atto l'accuratezza sta sopra la leggibilità, sempre.

## Come si lancia

```bash
# collauda le protezioni prima di lavorare
./scripts/test-hooks.py
```

Poi, in sessione: `/fascicolo` → `/strategia` → `/atto` → `/penale` → `/udienza`, oppure `/tutto`.

Il workflow `fascicolo/_workflow/genera-difesa.workflow.js` accetta:

- una o più pratiche: `["ricorso-affidamento"]`
- oppure `{ pratiche: ["..."], tipo: "memoria" }`

È resiliente: retry sugli agenti critici, promozione della versione precedente se una sintesi
fallisce, e ripresa dal primo anello mancante. **L'esito finale si decide guardando il disco**, non
i report degli agenti.

## Cosa NON è

Non è l'avvocato che deposita. **Produce materiale difensivo che un avvocato reale rivede, firma e
deposita**, e ogni deliverable lo dichiara nel piede — lo script del collaudo verifica che la
clausola ci sia.

**Una data verificata il 23/08/2026:** l'entrata in funzione del *Tribunale per le persone, per i
minorenni e per le famiglie* è prorogata al **31 ottobre 2026** (`D.L. 117/2025`). Fino ad allora
la competenza resta del **Tribunale ordinario**. Siamo a ridosso: **riverificala prima di ogni atto
introduttivo.**

## Note operative

- Le skill sono **project-scoped**: valgono solo dentro questa cartella.
- Il `name:` in ogni `SKILL.md` deve combaciare col nome della cartella.
- Le skill si caricano all'avvio: dopo modifiche strutturali **riavvia la sessione**.
- `registro-fonti.md` e `timeline.md` sono **solo append**: più agenti ci scrivono in parallelo.

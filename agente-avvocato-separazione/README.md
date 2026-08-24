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

## Le quattro idee che reggono l'agente

**1. Nessuna fonte non verificata.** Il numero di una sentenza è il punto in cui un modello
linguistico inventa con la massima verosimiglianza. Una citazione inesistente in un atto non fa
perdere quel punto: fa perdere la credibilità su tutto l'atto, comprese le venti affermazioni
vere. Ogni riferimento si verifica sul web e si registra in `fascicolo/_dati/registro-fonti.md`;
**un hook impedisce materialmente** che entri in un atto una citazione che non sia registrata
come `CONFERMATA` — e la riconosce nella forma in cui gli atti italiani la scrivono davvero,
*«Cass. civ., sez. I, 12 marzo 2020, n. 9764»*, non solo nella forma comoda.

**2. Nessun fatto senza documento, e nessun fatto dedotto.** Ogni fatto porta la sua etichetta,
fuori dalla prosa — `PROVATO` · `DOCUMENTABILE` · `ALLEGABILE` · `NON SOSTENIBILE` — e l'ultima
**non entra mai in un atto**. Un'affermazione falsa costa più di dieci affermazioni mancanti: la
controparte la smonta e con quella contamina i fatti veri che le stanno accanto. E ciò che il
fascicolo non sa non si indovina: `caso.json` nasce pieno di `null`, e un modello che deve scrivere
un ricorso senza il reddito dell'assistito non si ferma — scrive una cifra verosimile, perché la
cifra verosimile è ciò che sa produrre. **Un reddito dedotto vale quanto una sentenza inventata**, e
`verifica_caso.py` impedisce che l'atto parta prima dei fatti.

**3. Il perimetro è tattica, non moralismo.** Otto condotte non si consigliano mai —
registrazioni e accessi illeciti, trattenimento del minore, sospensione del mantenimento,
occultamento di redditi, prove fabbricate, denunce strumentali, **istruzione di un testimone**,
**distruzione di prove**. Non perché siano brutte: perché **trasformano un padre con ragione in un
indagato**, e sono anche quelle che funzionano peggio. Un secondo hook le blocca in scrittura,
nella *forma consiglio* e non nella semplice menzione — perché il briefing deve poter scrivere
«non sospendere mai il bonifico».

**4. Ciò che nessuno verifica non esiste.** Tre hook e tre script fanno rispettare in modo
meccanico quello che il metodo dichiara. Una regola ripetuta in cinque documenti e verificata da
nessuno vale finché il modello se la ricorda, cioè finché il contesto non si riempie — che è
esattamente il momento in cui si scrive l'atto finale. Il terzo hook blocca PAS, `NON SOSTENIBILE`
e attacchi alla persona dentro un atto; `verifica_atto.py` collauda il piede, le domande in prima
pagina, le glosse, gli allegati e il contenuto che il rito pretende; `verifica_caso.py` è l'unico
che guarda **a monte**, e ferma l'atto prima che sia scritto se i fatti non ci sono o si
contraddicono. `./scripts/test-hooks.py` prova tutto su **64 casi, e metà sono falsi positivi da
non commettere**: un cancello che blocca il lavoro legittimo viene spento, ed è peggio di non
averlo.

## Struttura

```
CLAUDE.md                         la costituzione: caso, regole non negoziabili, metodo
scripts/test-hooks.py             collauda le protezioni: 64 casi, blocca e passa

.claude/
  settings.json                   permessi + i tre hook
  hooks/
    blocca-citazioni-non-verificate.py   solo le fonti CONFERMATE entrano in un atto
    blocca-condotte-illecite.py          le otto condotte fuori perimetro
    blocca-difetti-di-atto.py            PAS, NON SOSTENIBILE, attacco alla persona
  agents/
    ricercatore-giurisprudenza.md  cerca e VERIFICA, poi registra in append
    verificatore-citazioni.md      controlla una per una le citazioni di un atto
    redattore-atti.md              scrive il singolo atto
    avvocato-avversario.md         scrive l'atto della controparte contro di noi
  commands/
    /fascicolo  /strategia  /atto  /penale  /udienza  /tutto
    /reclamo    dieci giorni perentori: prima si contano, poi si decide
    /accordo    la proposta conciliativa e la strada per chiuderla
    /verifica   tutti i cancelli deterministici su una pratica
  skills/
    difensore-famiglia-strategia/  AUTORE — strategia, atti, briefing
      ├─ SKILL.md
      ├─ references/
      │   ├─ verifica-delle-fonti.md        il protocollo. Si legge per primo
      │   ├─ quadro-normativo.md            cosa si applica a una coppia mai sposata
      │   ├─ rito-e-processo.md             il rito unico, e l'udienza che decide tutto
      │   ├─ termini-e-adempimenti.md       cosa si perde per sempre, e quando
      │   ├─ figlio-infra-triennale.md      IL CUORE: il bambino ha un anno
      │   ├─ affidamento-e-collocamento.md  dove si vince davvero
      │   ├─ mantenimento-e-spese.md        i numeri, e la trappola dei quindici anni
      │   ├─ casa-familiare.md              il rischio patrimoniale maggiore
      │   ├─ convivenza-senza-matrimonio.md cosa non si può chiedere, e cosa sì
      │   ├─ accordo-e-negoziazione.md      quando chiuderla, e come si chiude bene
      │   ├─ penale-della-famiglia.md       i reati, da entrambi i lati
      │   ├─ prove-e-trappole.md            cosa prova cosa, e le nove trappole
      │   ├─ dopo-la-prima-udienza.md       reclamo, modifica, attuazione
      │   ├─ architettura-atto.md           la forma del deliverable
      │   ├─ rubrica-punteggio.md           cancello: sotto 90/100 non si consegna
      │   └─ checklist-qualita.md           cancello: un solo NO = si corregge
      └─ scripts/
          ├─ riferimenti.py                 gli estrattori, condivisi con gli hook
          ├─ verifica_caso.py               cancello A MONTE: i fatti, prima dell'atto
          ├─ verifica_atto.py               cancello su UNA versione
          └─ verifica_citazioni.py          conservazione fra DUE versioni

    difensore-famiglia-avversario/         1º liv. — l'avvocato della madre
    difensore-famiglia-giudice/            1º liv. — chi decide
    difensore-famiglia-pubblico-ministero/ 1º liv. — l'accusa
    difensore-famiglia-curatore-minore/    1º liv. — il bambino, contro entrambi
    difensore-famiglia-ctu/                1º liv. — lo psicologo che valuta
    difensore-famiglia-penalista/          1º liv. — l'esposizione penale
    difensore-famiglia-patrimoniale/       1º liv. — i numeri
    difensore-famiglia-prove/              1º liv. — ogni fatto ha il suo documento?
    difensore-famiglia-decadenze/          1º liv. — è stato proposto tutto, e in tempo?
    difensore-famiglia-negoziatore/        1º liv. — si può chiudere per accordo?
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
    scadenze.md                   i termini aperti. L'unica cosa che non si recupera
    deviazioni-dal-metodo.md      dove questo metodo è stato trovato sbagliato
  prove/                          i documenti del fascicolo
  _workflow/genera-difesa.workflow.js
  <pratica>/                      lavorazione, v1 → v7 + prove.md + briefing.md
```

## La pipeline — sei livelli e un cancello

Ruoli e livelli stanno in `fascicolo/_dati/livelli.json`: è l'unico file da toccare per spostare
un revisore.

1. **`strategia`** redige la v1 (atto + mappa delle prove + briefing).
2. **1º livello** — dodici lenti **in parallelo**: le persone vere che decideranno o attaccheranno
   — avvocato della madre, giudice, PM, curatore del minore, CTU, penalista, patrimoniale, prove,
   cliente, deontologia — più le due che non guardano il merito, **decadenze** e **negoziatore**
   → **v2**
3. **2º livello** — `fonti` **poi** `cassazione`, in quest'ordine → **v3**
4. **3º livello** — `coerenza`: contraddizioni interne, col fascicolo, fra civile e penale → **v4**
5. **4º livello** — `editor`: asciugatura → **v5**
6. **5º livello** — `chiarezza`: **riscrive l'atto da capo** in italiano leggibile → **v6**
7. **6º livello** — `italiano-giuridico`: la lingua, frase per frase → **v7**
8. **Cancello** — `collaudo`: citazioni e conservazione, contro la v5 → **depositabile**

### Perché il secondo livello è sequenziale

`fonti` **ripulisce**, `cassazione` **amplia**. Invertirli significa costruire su una base marcia
e raddoppiare il lavoro di entrambi. È l'unico livello che non gira in parallelo, ed è voluto.

### Perché decadenze e negoziatore sono di primo livello

Perché sono i due modi di perdere una causa che nessuna delle altre lenti guarda, e nessuno dei
due riguarda il merito.

**Decadenze.** Nel rito unificato quasi tutto va proposto nell'atto introduttivo o nella finestra
giusta, e ciò che non c'è non si recupera con nessun argomento. Un revisore di merito, davanti a
una domanda riservata, non vede niente di sbagliato: *«ci si riserva di»* ha l'aspetto della
prudenza. Serve una lente che legga l'atto **come lo legge il calendario**.

**Negoziatore.** La maggior parte di questi procedimenti finisce con un accordo, e un accordo in
tre mesi vale più di un provvedimento migliore in diciotto — perché l'assetto povero che regge due
anni diventa «consolidato» e rovescia l'onere. In un accordo si ottengono anche cose che un
giudice non concede: gli **automatismi a date certe**, che sono la partita di questo caso. La
lente non chiede di indebolire le domande, chiede che siano formulate in modo che l'altra parte
possa accettarle **senza dichiararsi perdente**.

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
**finale**. Gira in tre strati:

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

**(a-bis) Il cancello sulla finale da sola**, `verifica_atto.py`. I due comandi qui sopra
confrontano: vedono ciò che si è perso, non ciò che non c'è mai stato. Un atto può attraversare
tutta la catena conservando fedelmente un difetto che aveva dalla v1, e il collaudo di
conservazione gli darebbe ragione. Questo strato guarda il documento finito: il piede, le domande
numerate in prima pagina, la sezione sull'interesse del minore, la glossa di **ogni** etichetta,
l'indice degli allegati, gli allegati citati e non mappati in `prove.md`, il contenuto che il rito
pretende in un atto introduttivo — piano genitoriale, dichiarazioni dei redditi ed estratti conto
del triennio — le citazioni non `CONFERMATA`, la lunghezza. Esiste perché rubrica e checklist le
compilava lo stesso modello che aveva appena scritto l'atto: **un controllo che non può fallire
non è debole, è assente.**

**(b) Il collaudatore semantico**, che cerca ciò che nessun conteggio vede: etichette riancorate a
un altro fatto, allegati che ora sostengono un fatto diverso, informazione persa per assorbimento,
qualificazioni cadute, verbi irrigiditi, e **domande con la portata cambiata**.

Zero bloccanti, o non si deposita. Se le perdite sono diffuse si consegna la **v5**: meno
scorrevole, ma verificata. In un atto l'accuratezza sta sopra la leggibilità, sempre.

## Come si lancia

```bash
# collauda le protezioni prima di lavorare: 64 casi, e metà sono falsi positivi
./scripts/test-hooks.py

# e il fascicolo, prima di scrivere: i campi vuoti si chiedono, non si deducono
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_caso.py \
  fascicolo/_dati/caso.json --tipo ricorso
```

Poi, in sessione: `/fascicolo` → `/strategia` → `/atto` → `/penale` → `/accordo` → `/udienza`,
oppure `/tutto`. Prima di consegnare, `/verifica`. Se l'udienza va male, `/reclamo` — e la prima
cosa da fare sono i **dieci giorni**, non la decisione.

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

**E i termini che decidono le cause**, verificati il 24/08/2026 sul testo in Gazzetta Ufficiale e
registrati: contenuto obbligatorio dell'atto introduttivo — piano genitoriale, redditi ed estratti
conto del **triennio** (`artt. 473-bis.12` e `473-bis.16 c.p.c.`); memorie integrative a ritroso
dall'udienza, **20 · 10 · 5 giorni** (`art. 473-bis.17`); reclamo contro i provvedimenti provvisori,
**dieci giorni perentori** dalla pronuncia in udienza (`art. 473-bis.24`). Questo agente non calcola
termini come se fossero certi: indica la norma, e il conteggio lo verifica chi deposita.

## Note operative

- Le skill sono **project-scoped**: valgono solo dentro questa cartella.
- Il `name:` in ogni `SKILL.md` deve combaciare col nome della cartella.
- Le skill si caricano all'avvio: dopo modifiche strutturali **riavvia la sessione**.
- `registro-fonti.md` e `timeline.md` sono **solo append**: più agenti ci scrivono in parallelo.

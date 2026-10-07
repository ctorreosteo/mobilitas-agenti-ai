---
name: broll-regia-editoriale
description: Legge lo script di un video pubblicitario Mobilitas e decide DOVE mettere i B-roll, QUANTI, di QUALE TIPO, con quale GENERE del protagonista e in quale FORMATO, per ottenere la massima ritenzione e conversione. Non scrive prompt: produce il piano di regia che gli specialisti dei prompt eseguono. Attiva questa skill quando si deve pianificare la sequenza visiva di uno script pubblicitario, decidere il numero di b-roll, stabilire i punti di inserimento, scegliere uomo o donna, o valutare se un passaggio debba restare sul volto dell'osteopata.
---

# Regia editoriale dei B-roll — dove si compra l'attenzione

Questa skill decide **il piano**. Non scrive un solo prompt: quello è lavoro di
`broll-pain-point` e `broll-infografica-meccanismo`, che ricevono da qui un incarico
già circoscritto.

La divisione serve a una cosa sola. Chi scrive il prompt di una scena la guarda da
dentro e la vuole bella; chi fa la regia la guarda da fuori e si chiede se quella scena
guadagna il suo posto. Sono due giudizi diversi, e tenerli nella stessa testa produce
sempre lo stesso difetto: **sequenze di immagini belle che nessuno finisce di guardare.**

---

## VINCOLO ASSOLUTO

**Un B-roll non serve a illustrare quello che la voce sta dicendo. Serve a comprare i
tre secondi successivi.**

Da qui discende tutto il resto. Un'immagine che ripete il parlato è ridondanza: lo
spettatore ha già capito, e il video rallenta nel punto in cui doveva accelerare. Un
b-roll guadagna il suo posto solo se fa una di queste quattro cose:

1. **Ferma** — interrompe uno scroll o un calo di attenzione già iniziato.
2. **Fa riconoscere** — lo spettatore vede sé stesso e smette di valutare il video.
3. **Fa capire** — rende visibile una relazione che a parole richiederebbe venti secondi.
4. **Ritma** — rompe una permanenza troppo lunga sullo stesso quadro.

Se non ne fa nessuna, il b-roll non va tagliato dopo: **non va pianificato.**

---

## SECONDO VINCOLO ASSOLUTO

**Sulla prima frase del video non va mai un B-roll.**

Non è una preferenza e non si negozia con l'argomento «ma qui l'immagine sarebbe fortissima».
La prima frase resta sul volto, sempre. Il primo b-roll può entrare dalla seconda frase in poi.

Il motivo è che nel primo secondo lo spettatore non sta valutando il contenuto: sta
classificando il video. Se il primo fotogramma è una scena costruita, la classifica come
pubblicità e scorre prima di aver sentito l'hook. Se è una persona che parla, resta
abbastanza da ascoltare la prima frase — ed è la prima frase che deve fare il lavoro di
fermarlo, non l'immagine.

**Conseguenza operativa:** la prima frase dello script finisce **sempre** in `senza_broll`,
riportata alla lettera, e il campo `prima_frase` del piano la ripete. Nessun b-roll può
avere quella frase in `copre`. È l'unica regola del piano che si verifica contando, non
leggendo: il workflow la controlla da solo e rimanda indietro il piano che la viola.

---

## Il test del taglio, prima di ogni voce del piano

> *Se tolgo questa scena e lascio il parlato sul volto dell'osteopata, lo spettatore
> perde qualcosa che gli serve per continuare a guardare?*

Se la risposta è no, la voce esce dal piano e finisce in `senza_broll` con il motivo.
Quella lista non è uno scarto: è la parte del referto che Carlos legge per capire
dove il video regge da solo.

---

## Dove l'attenzione si perde davvero

Non è distribuita in modo uniforme. Su un video pubblicitario healthcare i punti di
fuga sono quattro, sempre gli stessi, e sono i posti in cui un b-roll vale il doppio:

| Punto | Cosa succede | Cosa ci vuole |
|---|---|---|
| **Subito dopo la prima frase** | L'hook è stato detto: o lo spettatore lo vede, o se ne va | Il pattern interrupt entra **qui**, mai prima: sulla prima frase c'è il volto |
| **Passaggio pain → meccanismo** | Cambia registro: dal «sono io» al «ora mi spiegano» | Un'infografica che sembra la RISPOSTA alla domanda del pain |
| **Meccanismo che si astrae** | Tre concetti in fila senza immagine: si abbandona | Un visual per ogni salto di scala anatomica, non per ogni frase |
| **Prima della CTA** | Il desiderio deve essere già visibile | Una scena aspirazionale, oppure nulla |

**La CTA quasi mai vuole un b-roll.** Lì il volto dell'osteopata vale più di qualunque
immagine: la fiducia si trasferisce da una faccia, non da una scena. Se piazzi un b-roll
sulla CTA, dichiara il motivo per iscritto o non piazzarlo.

---

## Quanti B-roll

Il principio è il **MINIMUM EFFECTIVE VISUAL SET**: il numero più basso che tiene il
video dinamico, comprensibile ed emotivamente progressivo. «Più b-roll» non è «video
migliore»: è più costo, più tempo di montaggio e più rischio di sequenze che si somigliano.

**Se Carlos ha fissato una quota** (per esempio: uno per il pain, due per il meccanismo),
la quota **non si discute**. Cambia però cosa fa questa skill:

- con la quota, il lavoro è tutto sul **piazzamento**: quale singolo momento merita
  l'unico b-roll disponibile;
- se la quota è **più bassa** di quello che lo script chiederebbe, si scrive in
  `avvertenze` *quale* passaggio resta scoperto e *cosa* costa. Una riga, fattuale;
- se la quota è **più alta**, non si riempie. Si dichiara che le voci oltre la soglia
  sarebbero ridondanti e si propone dove spenderle meglio (una variante alternativa
  dello stesso beat, non una scena in più che dice la stessa cosa).

**Mai inventare un beat per far quadrare un numero.**

---

## Aumenta · Riduci

Aumenta quando: cambia luogo, momento della giornata, comportamento o emozione ·
compare un oggetto che porta significato · emerge un pain point nuovo · la scena
precedente è rimasta in aria troppo a lungo · cambia la scala anatomica.

Riduci quando: due frasi dicono lo stesso concetto · due scene sarebbero quasi
identiche · una sola key visual sintetizza più comportamenti · il taglio
interromperebbe una buona performance dell'osteopata · il cambio non porta né
informazione né emozione.

---

## La decisione sul GENERE — e le sue conseguenze

È la prima cosa da stabilire, perché governa tutto il resto del piano.

**Regola:** guarda la condizione, non il tono dello script.

| Caso | Genere | Esempi |
|---|---|---|
| La condizione riguarda solo le donne | `donna` | ciclo doloroso, endometriosi, dolore pelvico post parto, gravidanza, menopausa, cicatrice da cesareo o da mastoplastica |
| La condizione riguarda solo gli uomini | `uomo` | prostatite, varicocele |
| La condizione riguarda entrambi | `entrambi` | lombalgia, cervicalgia, reflusso, acufeni, cefalea, bruxismo, colon irritabile, fascite plantare |

Una prevalenza non è un'esclusiva. L'emicrania colpisce più donne, la lombalgia più
uomini in certi lavori: restano **entrambi**. Si passa a un genere solo quando l'altro
genere *non può avere quella condizione*, o quando il copy parla esplicitamente a uno solo.

### Cosa cambia quando il genere è `entrambi`

Due conseguenze, entrambe decise da Carlos e non negoziabili qui:

1. **Ogni B-roll con persone si genera in due varianti**, donna e uomo. Stessa scena,
   stesso ambiente, stessa luce, stessa azione: cambia solo il protagonista. La simmetria
   è il punto — due scene diverse non sono due varianti, sono due b-roll.
2. **Il formato del video diventa 16:9** invece di 9:16.

### L'eccezione delle infografiche

Un'infografica di **regione locale** — diaframma, mandibola, tratto cervicale, piede —
non ha genere: variante **unica**, anche quando il piano è `entrambi`.

Un'infografica che mostra una **silhouette corporea riconoscibile** ne ha uno, e allora
segue il piano: due varianti quando il piano è `entrambi`. Generare un torso
inequivocabilmente maschile dentro la versione femminile del video è l'errore che
nessuno nota in fase di prompt e che salta agli occhi al montaggio.

---

## Il formato cambia la composizione, non solo il bordo

Va scritto nel piano perché gli specialisti dei prompt lo usano:

- **9:16** — il soggetto occupa l'altezza, l'ambiente si legge per frammenti, il volto
  sta nel terzo alto. Piani medi e ravvicinati. Il contesto si suggerisce, non si mostra.
- **16:9** — c'è spazio laterale: l'ambiente racconta insieme al soggetto. Piani più
  larghi, il soggetto decentrato, la profondità diventa disponibile.

Un prompt scritto per il verticale e generato in orizzontale produce un'immagine con il
soggetto solo al centro e due terzi di niente ai lati.

---

## Continuità del personaggio

Quando più scene appartengono alla **stessa persona nella stessa giornata**, il
personaggio non cambia. Il piano porta una `descrizione_fissa` — età, corporatura,
capelli, tratto distintivo — che gli specialisti copiano **alla lettera** in ogni prompt,
senza riformularla. È l'unico modo per avere continuità senza Soul ID.

Quando il volto deve essere lo stesso in modo verificabile, il piano segnala
`serve_soul_id: true`: il personaggio va addestrato una volta e riusato via
`custom_reference_id`. Costa un passaggio in più, ed è l'unica strada tecnica vera.

---

## Progressione

La sequenza racconta, non colleziona. Una progressione tipica:

PROBLEMA → RIPETIZIONE → CONSEGUENZA → IMPATTO EMOTIVO → DOMANDA → SPIEGAZIONE → DESIDERIO

Due controlli sul piano finito:

- **Alternanza.** Cinque scene umane di fila si appiattiscono. Alterna scena umana,
  dettaglio di gesto, oggetto, infografica.
- **La domanda aperta.** Il pain point lascia una domanda («perché torna sempre?»).
  La prima infografica del meccanismo deve essere la sua **risposta visiva**. Se non
  lo è, il video ha due metà che non si parlano, e si perde proprio nel punto di giunzione.

---

## Città di riferimento

Il piano riceve una città e la passa avanti, ma decide **quali** b-roll possono
ospitarla: solo quelli in cui uno sfondo esiste davvero (finestra, strada, terrazzo,
bar, auto). Su una scena in cucina o a letto, il campo resta vuoto.

**Massimo un landmark riconoscibile per video**, e solo su un'inquadratura di
ambientazione. Il resto lavora sul tessuto urbano. I dati stanno in
`broll-generati/_dati/citta.json`, che va letto: contiene anche cosa evitare.

---

## Output

Restituisci **solo** questo oggetto, in italiano, senza testo attorno.

```json
{
  "condizione": "slug o nome della condizione trattata dallo script",
  "genere": "donna | uomo | entrambi",
  "motivo_genere": "una riga: perché, riferita alla condizione",
  "aspect_ratio": "9:16 | 16:9",
  "citta": "chiave da citta.json, oppure null",
  "personaggio": {
    "descrizione_fissa": "età, corporatura, capelli, tratto distintivo — da copiare alla lettera",
    "serve_soul_id": false
  },
  "idea_centrale": "una frase: cosa vende davvero questo script",
  "prima_frase": "la prima frase dello script, riportata ALLA LETTERA: è quella che non si copre mai",
  "progressione": "la catena emotiva scelta, in cinque o sei parole separate da frecce",
  "broll": [
    {
      "id": "01-pain-sveglia-notte",
      "tipo": "pain | infografica",
      "copre": "la frase esatta dello script, fra virgolette",
      "posizione": "dopo quale frase entra e su quale esce",
      "funzione": "quale dei quattro lavori fa: fermare, far riconoscere, far capire, ritmare",
      "perche_qui": "una riga: cosa si perderebbe lasciando il volto",
      "secondi": 5,
      "varianti": ["donna", "uomo"],
      "citta_visibile": true,
      "note_per_lo_specialista": "cosa deve sapere chi scrive il prompt e non si legge dallo script"
    }
  ],
  "senza_broll": [
    { "passaggio": "frase o sezione", "perche": "una riga" }
  ],
  "avvertenze": [
    "cosa resta scoperto e cosa costa, se la quota imposta è più bassa del necessario"
  ]
}
```

Regole sul risultato:

- `id` in `NN-tipo-parolachiave`, numerati nell'ordine di montaggio. Diventa il nome
  dei file: niente spazi, niente accenti.
- `secondi` fra 3 e 15: è il limite di Kling. Sotto i 4 secondi un b-roll non si legge,
  sopra gli 8 su un pain point diventa un altro video.
- `varianti`: `["donna","uomo"]` quando il genere è `entrambi` e la scena ha persone;
  `["unica"]` in tutti gli altri casi.
- `senza_broll` non può essere vuoto su uno script completo. Se lo è, hai riempito
  invece di scegliere. E la **prima voce** di quella lista è sempre la prima frase del
  video, con il motivo «resta sul volto: è la regola d'apertura».

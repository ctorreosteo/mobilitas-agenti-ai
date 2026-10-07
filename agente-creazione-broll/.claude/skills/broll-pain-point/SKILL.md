---
name: broll-pain-point
description: Scrive i prompt Higgsfield Text-to-Image e Image-to-Video di UN singolo B-roll della sezione Hook / Pain Point di uno script pubblicitario Mobilitas — la scena in cui lo spettatore deve riconoscersi. Riceve un incarico già circoscritto dalla regia editoriale e restituisce i due prompt in inglese più i parametri di generazione. Attiva questa skill quando si deve produrre il prompt di una scena lifestyle con persone reali, di un dettaglio di comportamento, di un oggetto legato al problema o di una scena aspirazionale.
---

# B-roll del riconoscimento — la scena in cui lo spettatore vede sé stesso

Questa skill scrive **un B-roll per volta**, su incarico. Non decide quanti ne servono
né dove vanno: quello è già stato deciso da `broll-regia-editoriale`, che ti passa la
frase da coprire, la funzione editoriale, il formato, il genere e la città.

Ti arriva un incarico. Restituisci due prompt e i parametri. Niente altro.

> **Adattata da:** `higgsfield-performance-broll-director`. Restano il metodo di analisi
> del copy, i tipi di b-roll, il principio di recitazione e il livello di dettaglio del
> T2I. Sono stati tolti la fase che decide il numero di scene — ora è della regia — e
> l'output narrativo in italiano, sostituito da un oggetto che il workflow consuma.
> Sono stati aggiunti: formato che governa la composizione, doppia variante di genere,
> città di riferimento e i vincoli reali dei modelli Higgsfield.

---

## VINCOLO ASSOLUTO

**Il problema deve sembrare parte di una giornata normale, non un sintomo dimostrato
da un attore.**

È la regola che separa un b-roll che converte da uno che fa scorrere. Chi guarda ha
quel problema da anni: lo gestisce, lo minimizza, ci convive. Non si tiene la schiena
con la smorfia. Si appoggia al lavandino un secondo di troppo. Si siede con una mano
sul bracciolo. Guarda il telefono alle tre di notte con la faccia di chi ci è abituato.

Preferisci sempre: **disagio trattenuto · stanchezza sottile · frustrazione silenziosa ·
gesto inconsapevole · esitazione naturale.**

Vietati: smorfie, urla, mani che stringono la pancia, schiena tenuta a due mani,
tristezza teatrale, melodramma. Un solo gesto sopra le righe e lo spettatore smette di
riconoscersi e comincia a giudicare la recitazione.

---

## Cosa ti arriva

```json
{
  "id": "01-pain-sveglia-notte",
  "copre": "«Ti svegli alle tre e non riesci più a dormire»",
  "funzione": "far riconoscere",
  "perche_qui": "...",
  "secondi": 5,
  "aspect_ratio": "9:16",
  "genere": "entrambi",
  "varianti": ["donna", "uomo"],
  "personaggio": { "descrizione_fissa": "...", "serve_soul_id": false },
  "citta": "torino",
  "citta_visibile": false,
  "note_per_lo_specialista": "..."
}
```

Leggi anche lo script completo: serve a capire il tono, non a coprire altre frasi.
**Copri solo il tuo incarico.** Se pensi che serva un'altra scena, scrivilo in
`osservazioni` — non generarla.

**L'apertura non è mai tua.** Sulla prima frase del video non va nessun b-roll: resta sul
volto. Se il tuo incarico sembra coprirla, non scrivere il prompt: segnalalo in
`osservazioni`, perché è un errore della regia e va corretto lì.

---

## Scegli il tipo prima di scrivere

Non tutto è una persona in una stanza. Otto tipi, e la varietà della sequenza dipende
da questa scelta:

1. **Lifestyle umano** — persona dentro una situazione reale.
2. **Dettaglio di comportamento** — mano, telefono, postura, sguardo, esitazione.
3. **Oggetto / prodotto** — farmaci, bite, integratori, cerotti, computer.
4. **Racconto d'ambiente** — l'ambiente parla al posto della persona: il cassetto pieno
   di scatole, la camera alle tre di notte, il tavolo apparecchiato per uno.
5. **Key visual multi-momento** — la stessa persona in più momenti dentro UNA
   composizione. Da usare quando più frasi raccontano lo stesso comportamento ripetuto.
6. **Product shot premium** — oggetti sospesi su fondo cinematografico.
7. **Infografica medicale** — *non è tua*: è di `broll-infografica-meccanismo`.
8. **Desiderio** — ciò che la persona vuole tornare a fare: uscire, dormire, mangiare
   senza pensarci, muoversi.

Sulla key visual multi-momento: **niente split screen, niente riquadri, niente bordi.**
Le scene si fondono con foschia, ombre, profondità e caduta naturale della luce. Una
scena è HERO, le altre sono subordinate.

---

## Il formato decide l'inquadratura

| | **9:16** | **16:9** |
|---|---|---|
| Soggetto | occupa l'altezza, volto nel terzo alto | decentrato, spazio laterale che racconta |
| Piano | medio e ravvicinato | medio-largo, profondità disponibile |
| Ambiente | frammenti leggibili | ambiente che partecipa alla scena |
| Errore tipico | mettere troppa scena e perderla | soggetto al centro con due terzi di vuoto |

Scrivilo **dentro** il prompt: `vertical 9:16 composition, subject filling the frame
height` oppure `horizontal 16:9 composition, subject placed off-centre`.

### I terzi sono una guida per te, non parole da mettere nel prompt

**Mai nominare due o tre «thirds» nella stessa frase.** Un elenco come
*«her face in the upper third, the window in the middle third, nothing in the lower third»*
non viene letto come una composizione: viene letto come un **layout a tre pannelli**, e il
modello consegna un trittico a bande orizzontali con il soggetto tagliato in mezzo. È già
successo, e ha bruciato una generazione intera.

Un solo riferimento a un terzo si può usare (`her face high in the frame`). Per tutto il
resto si scrive in **linguaggio da macchina da presa** — piano, obiettivo, distanza,
profondità di campo — che è il linguaggio che il modello capisce davvero:

> medium shot on a 50mm lens at f/2.0, camera at eye level, she stands at camera left,
> the lit restaurant window twelve metres behind her thrown far out of focus, foreground
> and background separated by depth, not by bands

---

## Le due varianti, quando servono

Quando `varianti` contiene donna e uomo, produci **due prompt T2I** che differiscono
**solo** per il protagonista. Identici: ambiente, ora del giorno, luce, inquadratura,
azione, oggetti, atmosfera. Il guardaroba cambia quanto basta a essere plausibile, non
di più — stesso registro, stessi colori, stessa qualità.

Il prompt I2V è **uno solo** e vale per entrambe: descrive movimento, non soggetto.

Il senso è il montaggio. Le due versioni devono poter essere scambiate nello stesso
punto del video senza che cambi nient'altro. Due scene diverse con due persone diverse
non sono varianti: sono due b-roll, e mandano all'aria il lavoro della regia.

---

## La città

Se `citta_visibile` è `false`, la città **non entra**. Nessun accenno, nessuna finestra
aperta apposta.

Se è `true`, apri `broll-generati/_dati/citta.json` e prendi dal livello **tessuto** —
materiali, colore degli intonaci, tipo di finestra, alberi, arredo urbano, luce. È il
livello che funziona: chi vive lì si riconosce, chi non ci vive non nota niente di strano.

Il livello **landmark** si usa una sola volta per video, e solo se la regia lo ha
chiesto esplicitamente. La Mole in ogni scena non è ambientazione: è promozione turistica,
e sposta il registro da «questa è la mia vita» a «questa è una pubblicità».

Leggi anche `da_evitare`: è la lista degli errori che i modelli fanno da soli, a partire
dagli interni americani.

---

## Il prompt Text-to-Image

In inglese, dettagliatissimo. Descrivi a 360°: soggetto · fascia d'età · aspetto ·
espressione · postura esatta · posizione delle mani · sguardo · guardaroba con tessuti
e colori · accessori · ambiente · arredi · oggetti · architettura · attività sullo
sfondo · ora del giorno · luce (sorgente, direzione, temperatura) · posizione di camera ·
estetica dell'obiettivo · inquadratura · profondità di campo · atmosfera · tono emotivo ·
vincoli negativi.

Chiudi sempre con la qualità richiesta: *ultra-photorealistic, premium, cinematic,
believable, anatomically realistic, advertising quality*. E con i vincoli negativi:
*no stock photography look, no exaggerated expression, no visible logos or brand names,
no text overlays, no distorted hands, no plastic skin.*

Il dettaglio non è vezzo: è l'unica difesa contro la resa da stock. Per il guardaroba,
l'ambiente, la camera e la luce c'è `references/casting-e-guardaroba.md`, e va aperto.

**Mai marchi reali, mai persone reali riconoscibili, mai un'insegna che imita un marchio
esistente.** Se serve un prodotto, è un packaging europeo premium di fantasia.

---

## Il prompt Image-to-Video

Molto più corto: **70–160 parole**, e mai oltre 2.500 caratteri, che è il punto in cui
Kling tronca senza avvisare.

L'immagine sorgente contiene già personaggio, vestiti, ambiente, anatomia e oggetti.
**Non li ridiscutere.** Descrivi solo:

1. movimento di camera; 2. movimento del corpo; 3. micro-espressione; 4. movimento di
oggetti; 5. movimento dell'ambiente.

Preferisci: *slow cinematic zoom out · slow push-in · subtle five-degree orbit · subtle
parallax · natural breathing · small eye movements · restrained gestures · realistic
background motion.*

Evita: grandi trasformazioni del corpo, movimenti di camera bruschi, gesti eccessivi,
recitazione enfatica, deformazioni, morphing.

**Scrivilo senza aver visto l'immagine.** È la difficoltà vera di questo passaggio: il
prompt I2V nasce prima che l'immagine esista, quindi deve valere per l'immagine che il
tuo T2I descrive, non per una che speri. Se il movimento dipende da un dettaglio che il
T2I non nomina, quel dettaglio va aggiunto al T2I.

L'audio nativo resta **spento**: il parlato è della voce fuori campo, e l'audio generato
si butta comunque in montaggio.

---

## Output

Restituisci **solo** questo oggetto, senza testo attorno. I prompt sono in inglese, il
resto in italiano.

```json
{
  "id": "01-pain-sveglia-notte",
  "tipo_broll": "lifestyle umano | dettaglio di comportamento | oggetto | racconto d'ambiente | key visual multi-momento | product shot | desiderio",
  "copre": "la frase dello script",
  "cosa_deve_provare_lo_spettatore": "una frase",
  "prompt_t2i": { "donna": "...", "uomo": "..." },
  "prompt_i2v": "...",
  "durata": 5,
  "citta_usata": "torino — tessuto: portici, intonaci ocra. Nessun landmark.",
  "osservazioni": ["cosa hai notato e non era nel tuo incarico"]
}
```

`prompt_t2i` ha **una sola chiave `unica`** quando le varianti non servono:
`{ "unica": "..." }`. Il workflow si aspetta questa forma esatta e la usa per costruire
i file: una chiave in più diventa un b-roll fantasma, una in meno diventa una variante
mancante scoperta a generazione finita.

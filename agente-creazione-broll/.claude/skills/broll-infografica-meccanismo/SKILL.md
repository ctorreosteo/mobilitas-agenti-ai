---
name: broll-infografica-meccanismo
description: Scrive i prompt Higgsfield Text-to-Image e Image-to-Video di UNA singola infografica medicale 3D per la sezione Meccanismo Unico di uno script pubblicitario Mobilitas — l'immagine che rende comprensibile una relazione anatomica o funzionale. Riceve un incarico circoscritto dalla regia editoriale e restituisce i due prompt in inglese più i parametri. Attiva questa skill quando si deve produrre il prompt di una visualizzazione anatomica, di una relazione biomeccanica, di un movimento fisiologico o di un pattern di tensione con la palette Mobilitas.
---

# Infografica del meccanismo — l'immagine che risponde alla domanda del pain

Questa skill scrive **una infografica per volta**, su incarico. Il numero e la posizione
li ha già decisi `broll-regia-editoriale`.

> **Adattata da:** `mobilitas-scientific-mechanism-broll-director`. Restano la
> classificazione dei mechanism beat, il brand system, il controllo sui claim medici e
> la regola immagine-contro-animazione. Sono stati tolti la fase che decide quante
> infografiche servono — ora è della regia — e l'output narrativo, sostituito da un
> oggetto che il workflow consuma. Sono stati aggiunti: formato che governa la
> composizione, coerenza con le infografiche sorelle e i vincoli reali dei modelli.

---

## VINCOLO ASSOLUTO

**La rappresentazione visiva non può rendere l'affermazione medica più forte del copy.**

Se il copy dice *«può essere collegato a»*, l'immagine mostra una **relazione**, non una
causa. Se dice *«può influenzare»*, mostra un rapporto funzionale, non una struttura che
provoca la patologia. Se il copy usa una metafora — *«il sistema nervoso tiene la pancia
in allarme»* — non si disegnano allarmi, fulmini, intestini rossi o cervelli che
scaricano: si disegna una relazione nervosa, in forma medicalmente prudente.

Questo vincolo viene prima della bellezza dell'immagine, sempre. Un'infografica
spettacolare che afferma più del copy è un problema di compliance sanitaria con la
faccia di un problema estetico.

---

## Tensione non è patologia

Il secondo errore per frequenza. Se il copy parla di **tensione**, rappresenta:
coinvolgimento muscolare, mobilità ridotta, escursione limitata, sforzo muscolare
aumentato, compenso biomeccanico.

**Non** trasformarla in: infiammazione, danno tissutale, compressione nervosa,
ostruzione, degenerazione.

E non inventare fisiologia che nel copy non c'è — compressioni nervose, riduzioni di
flusso, alterazioni ormonali, blocchi articolari — solo perché renderebbero l'immagine
più interessante.

---

## Lo spettatore deve capire una RELAZIONE, non vedere anatomia

L'anatomia decorativa è tempo di video buttato. L'infografica costruisce una mappa
mentale: diaframma ↔ mobilità addominale, mandibola ↔ cranio ↔ collo ↔ spalle, bacino ↔
lombare ↔ diaframma, sistema nervoso ↔ regione intestinale.

**Il test dei cinque secondi:** *qual è la singola cosa che lo spettatore deve capire
guardando questo frame per due o cinque secondi?* Se la risposta contiene tre concetti,
l'immagine è sbagliata — non perché sia brutta, ma perché non ha una gerarchia.

Un'infografica premium non è quella con più anatomia. È quella con la gerarchia visiva
più chiara.

---

## Immagine o animazione: la regola che risparmia metà del lavoro

**Non usare una nuova immagine per qualcosa che l'animazione spiega meglio.**

Il diaframma che scende in inspirazione e risale in espirazione è **una** immagine più
un I2V, non due immagini. Generare «diaframma alto» e «diaframma basso» come due b-roll
produce due rendering che non combaciano, un salto visibile al montaggio e il doppio
dei crediti.

Se il tuo incarico ti sembra chiedere due immagini di cui una è un movimento, dillo in
`osservazioni`: la regia può trasformarlo in un'unica sorgente con due animazioni.

---

## Coerenza con le infografiche sorelle

Se il piano contiene altre infografiche dello stesso video, devono sembrare **frame
dello stesso sistema visivo**, non tavole prese da atlanti diversi.

Resta identico: corpo, livello di trasparenza, stile di rendering, illuminazione,
palette, atmosfera, orientamento di base.

Può cambiare: angolo di camera, inquadratura, punto di fuoco, profondità, strutture
evidenziate.

L'incarico ti dice quali altre infografiche esistono nel piano e cosa mostrano. Se sei
la seconda o la terza, **ripeti le formule di rendering e di luce della prima parola per
parola**: è l'unico modo per ottenere continuità da generazioni indipendenti.

---

## Il formato decide la composizione

- **9:16** — anatomia verticale (colonna, catena posteriore, rapporto cranio-bacino).
  La regione importante sta nel terzo centrale. Spazio negativo sopra e sotto.
- **16:9** — anatomia orizzontale o relazioni laterali (mandibola-collo-spalla,
  diaframma-addome). La struttura evidenziata sta su un terzo, lo spazio negativo
  sull'altro.

Scrivilo nel prompt. Un'anatomia progettata per il verticale e generata in orizzontale
esce piccola in mezzo a due terzi di fondo navy.

---

## Il brand system

Tre colori, e non uno di più. Il dettaglio sta in `references/brand-system.md`, che va
aperto: contiene le formule esatte da copiare.

| | Colore | Uso |
|---|---|---|
| Fondo | `#002552` navy profondo | background, gradiente atmosferico, ombre, volume |
| Anatomia neutra | `#F4F4F4` | ossa, tessuti non evidenziati, bordi, luce chiave |
| Struttura attiva | `#72FA93` verde menta | **solo** coinvolgimento biomeccanico, tensione rilevante, percorso funzionale, bersaglio del trattamento |

Il verde è **trattenuto, preciso, medico, premium**. Non neon, non cyberpunk, non
radioattivo, non elettrico.

**Vietati**, salvo necessità scientifica esplicita: punti rossi di dolore, anatomia
rossa luminosa, infiammazione arancione, zone di allarme gialle, fulmini, archi
elettrici, raggi laser, vene luminose, energia sci-fi, esplosioni, compressioni
drammatiche, ossa rotte, sangue, deformazioni esagerate, anatomia da cartone animato.

**E niente testo generato.** Nessuna etichetta, nessuna freccia, nessuna scritta: i
modelli li scrivono storti e in inglese maccheronico, e un'infografica medicale con una
parola sbagliata dentro è peggio di una senza parole. **L'immagine deve funzionare senza
testo.** Le etichette, se servono, si aggiungono in montaggio.

---

## Il prompt Text-to-Image

In inglese, dettagliato, in questa struttura — è l'ordine che i modelli seguono meglio:

```
CREATE / VISUAL PURPOSE / STRICT COLOR PALETTE / ANATOMICAL SUBJECT /
ANATOMICAL STRUCTURES / BODY ORIENTATION / TRANSPARENCY AND LAYERS /
PRIMARY HIGHLIGHT / SECONDARY STRUCTURES / BIOMECHANICAL RELATIONSHIP /
BACKGROUND / LIGHTING / CAMERA / RENDERING QUALITY / NEGATIVE CONSTRAINTS
```

Sii preciso su: quale parte del corpo · quali vertebre quando conta · quali ossa ·
quali articolazioni · quali muscoli · quali organi · quale orientamento · cosa deve
essere visibile · cosa resta neutro · cosa è evidenziato · intensità del verde ·
trasparenza · luce · camera · fondo.

Non scrivere «show neck tension». Scrivi quali strutture sono coinvolte, quando il copy
lo consente.

**Camera:** anteriore, posteriore, laterale, tre quarti anteriore o posteriore. Estetica
`85mm premium medical visualization`. La regione importante è il centro visivo.

**Anatomia:** medicalmente plausibile, proporzioni realistiche, coerente al suo interno,
pulita, didattica e mai grottesca. Torso semitrasparente, strati di tessuto, visibilità
muscolare selettiva, scheletro visibile, organi in posizione reale, inserzioni muscolari
e rapporti articolari veri.

---

## Il prompt Image-to-Video

Il T2I costruisce l'anatomia, l'I2V spiega il meccanismo. Quindi è **molto più corto**:
**70–150 parole**, mai oltre 2.500 caratteri.

Non ripetere l'anatomia. Descrivi solo: movimento di camera · attivazione delle
strutture evidenziate · movimento fisiologico o movimento ridotto · percorso funzionale ·
movimento atmosferico del fondo · vincoli di stabilità anatomica.

**Camera:** slow cinematic push-in, subtle five-degree orbit, slow controlled zoom,
gentle parallax, subtle drift. Mai zoom rapidi, rotazioni di 360 gradi, orbite
drammatiche, camera a mano, transizioni veloci.

**Il verde può** illuminarsi gradualmente, viaggiare lungo strutture connesse,
intensificarsi, pulsare lentamente, seguire le fibre muscolari, identificare un percorso
funzionale. Usa formule come *restrained medical illumination · subtle internal
mint-green glow · slow controlled pulsation · gradually activate the highlighted
muscular pattern*. Non deve sembrare elettricità, laser, energia radioattiva, magia o fuoco.

**Movimento fisiologico:** lento e plausibile. Se il concetto è mobilità ridotta, mostra
**escursione ridotta**, non organi deformati.

Chiudi sempre con i vincoli di stabilità, che in Higgsfield sono la differenza fra
un'infografica e un incubo:

> Keep all anatomy stable and medically realistic. No muscle deformation. No unnatural
> vertebral movement. No organ deformation. No bone displacement. No generated text,
> labels or arrows.

L'audio nativo resta spento.

---

## Prima e dopo

Evita le rappresentazioni miracolistiche: prima corpo bloccato rosso, dopo corpo
perfetto verde. Se serve mostrare un cambiamento, usa tensione evidenziata che si
riduce, escursione che aumenta, coinvolgimento muscolare più equilibrato, movimento più
fluido. **Il cambiamento resta moderato**, perché il copy promette un lavoro, non un
miracolo.

E quando il copy passa dal meccanismo al trattamento, non mettere automaticamente mani
osteopatiche dentro l'infografica. Quasi sempre basta animare la riduzione del pattern
di tensione, oppure è meglio tornare sul volto dell'osteopata.

---

## Output

Restituisci **solo** questo oggetto, senza testo attorno. I prompt in inglese, il resto
in italiano.

```json
{
  "id": "04-meccanismo-diaframma",
  "copre": "la frase dello script",
  "cosa_deve_capire_lo_spettatore": "UNA frase, non due",
  "beat": "relazione anatomica | movimento | tensione | connessione funzionale | bersaglio del trattamento | sequenza temporale",
  "prompt_t2i": { "unica": "..." },
  "prompt_i2v": "...",
  "durata": 6,
  "prudenza_claim": "cosa dice il copy e cosa hai rappresentato, in una riga: serve a dimostrare che non hai alzato l'affermazione",
  "osservazioni": ["per esempio: questa e la successiva possono condividere la stessa immagine sorgente"]
}
```

`prompt_t2i` usa la chiave `unica`, salvo che la regia abbia chiesto le due varianti —
cosa che accade solo quando l'infografica mostra una silhouette corporea riconoscibile.
Un'anatomia di regione locale non ha genere.

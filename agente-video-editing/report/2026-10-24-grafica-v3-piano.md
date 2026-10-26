# Grafica v3: piano (24/10/2026)

Richiesta di Carlos: infografiche, scritte, motion e transizioni "clamorose".
Banco di prova: `videos/YT_TOFU_02-v2` (pulito e sagome già sul disco).

## Cosa non va oggi (da `controlli/anteprima.jpg`)

- I titoli dietro si leggono male: la testa copre il centro delle parole
  («MECC▒NICO», «NON ME▒BOLICO», «NON R▒SOLVE», «POSTURA ▒CCUMULATA»).
  Il layout è uno solo (due righe centrate): se la testa sta al centro, non c'è scampo.
- Le card sono riquadri fermi: il numero compare e basta, nessun grafico.
- Sottotitoli in pillola navy, tutti uguali, nessuna gerarchia sulle frasi forti.
- Avanzamento, apertura, chip e chiusura: dissolvenze. Nessuna transizione di capitolo.

## Cosa cambia (tutto nel motore, regia.json resta compatibile)

1. **Titoli dietro 2.0**: tre layout candidati (centro, colonna a sinistra, colonna
   a destra) scelti sulla parola peggiore coperta; lettere che cadono una a una con
   rimbalzo, lama di luce menta che attraversa la stanza dietro di lei, filo menta
   che si disegna sotto, numero di capitolo nell'eyebrow (`02 · MECCANISMO`).
2. **Infografiche**: il numero conta da 0 al valore (o da `prima`, es. 3-4 → 1 cm),
   sotto c'è una scala misurata (%, cm, min) che si riempie insieme al numero,
   eyebrow battuto a macchina, glossa che sale parola per parola, lampo sul numero
   quando si ferma.
3. **Sottotitoli cinetici**: niente pillola; testo con contorno e ombra, le parole
   entrano quando vengono dette con un piccolo rimbalzo, la parola attiva sta su
   una pillola menta che scivola di parola in parola. Nelle frasi di enfasi il
   corpo cresce e la scena si vela ai bordi.
4. **Avanzamento a capitoli**: barra a segmenti, il segmento corrente acceso.
5. **Apertura, chip, chiusura animati**: tendine, scrittura a macchina, lettere che
   cadono, CTA con bordo che si disegna e pulsa.
6. **Suono**: tick del contatore che rallenta con il numero, lama di luce sui titoli.

## Come si verifica

`./mve grafica`, `inquadra`, `anteprima` (+ fogli di movimento), `suono`,
`finale --limite` su tratti con titoli e card, poi master e QC CONSEGNABILE.
Shorts: stessi sottotitoli, si controllano i fogli `short*.jpg`.

---

# v4 (stesso giorno): «ancora più clamoroso, molte più infografiche, molto più estetiche»

## Fondamenta

- **Compositore**: il renderer non disegna più un livello trasparente sopra il video, compone
  il fotogramma intero (legge il montato pulito da ffmpeg). Serve per tre cose:
  vetro smerigliato sotto i pannelli, colore che si spegne dietro di lei durante i titoli
  (lei resta a colori), spinta di camera (push-in) su titoli ed enfasi.
- **Icone**: Material Symbols Rounded (Apache 2.0), sottoinsieme in `risorse/fonts/`.
- **Pannelli in vetro**: sfondo sfocato + velo navy + bordo di luce + ombra.

## Tipi di infografica (tutti in `card` di regia, campo `tipo`; ogni voce si ancora a una frase e compare quando lei la dice)

| tipo | cosa | dove nel banco di prova |
|---|---|---|
| `numero` | contatore + `barra` / `anello` / `punti` (100 punti) / `batteria` | 20%, 30-40%, 50%, 20 min, metà giornata |
| `barre` | confronto di misure (anche assurde: 10 anni contro 10 secondi) | peso 2% / ossigeno 20%; l'elastico |
| `orologio` | quadrante che gira fino all'ora detta, settore del tempo che manca | le tre meno dieci; le quattro meno un quarto |
| `icone` | icone che si contano una a una, l'ultima a fantasma | quarto caffè, forse il quinto |
| `lista` | voci che entrano quando le dice; ✓ / ✗ / barrate tutte insieme | cosa ti hanno raccontato; cosa hai provato; non è metabolico/mentale/volontà; sintomatico / sistemico |
| `catena` | causa → effetto, nodo per nodo | la postura che chiude il torace; il caffè che attiva il simpatico |
| `citazione` | frase chiave a karaoke dentro le virgolette | la lucidità dipende da quanto respiri |
| `anatomia` | gabbia toracica, polmoni e diaframma che respira; zone che si accendono | 3-4 cm; 1 cm; dove si lavora in studio |
| `postura` | figura seduta che si affloscia, punti che si accendono | spalle, testa, zona lombare, bacino |
| `curva` | andamento disegnato nel tempo, con etichette | il caffè: spinta e crollo sotto la partenza |

Niente card sui risultati del trattamento ("respiro diversamente", "il calo si riduce",
"lavorare otto ore"): sono esiti riferiti, a schermo diventerebbero promesse.

---

# v5 (26/10/2026): «Motion in casa»

Carlos ha chiesto di integrare Claude Motion. Verificato: Motion è una funzione di claude.ai
(beta, Team/Enterprise, `/motion`), non raggiungibile da Claude Code né via API, e non attiva
sul suo account. Scelta di Carlos: **rifare in casa le sue capacità, tutto automatico**.

Il motore genera **scene a tutto schermo** (4-8 s) dalla regia, sincronizzate alla voce:

| tipo | cosa |
|---|---|
| `parole` | tipografia cinetica: la frase esplode parola per parola; parole chiave in menta con effetti (`spegne`, `barra`, `sottolinea`) |
| `numero` | numero eroe gigante che conta, con anello / cento punti / barra a scala di scena |
| `confronto` | schermo diviso, due lati che entrano quando li dice, barre proporzionali |

Ingresso: zoomata dentro il video che si sfoca e si vela di navy (lei continua a muoversi
dietro il vetro). Uscita: il contrario. Fondo vivo: bagliore menta che deriva, griglia di punti
in parallasse, vignetta. Regole: massimo una scena ogni 45 s, mai sopra un titolo, mai sui
risultati del trattamento.

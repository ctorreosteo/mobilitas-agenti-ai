---
progetto: YT_TOFU_02-v2
canale: youtube.com/@Studio_Mobilitas
girato: ../YT_TOFU_02/YT_TOFU_02.MOV (collegato come sorgente.MOV)
consegna: renders/YT_TOFU_02-v2_FINALE.mp4, 1920x1080 @ 29.97p
durata_sorgente: 19m44s
durata_montata: 13m27s
tipo: talking-head TOFU, divulgazione osteopatica
agente: v2 (motore ./mve), 20/10/2026
---

Secondo montaggio dello stesso girato di YT_TOFU_02, fatto con l'agente v2. Serve sia come video da pubblicare al posto della v1 sia come **banco di prova** dell'agente: della v1 conosciamo la verità, quindi si misura cosa trova in più.

## Consegne

| file | cosa |
|---|---|
| `renders/YT_TOFU_02-v2_FINALE.mp4` | **il video da pubblicare** |
| `shorts/YT_TOFU_02-v2_short1..4.mp4` | quattro Shorts 9:16 (37-53 s) |
| `miniature/miniatura-1..3.jpg` | tre miniature 1280x720 |
| `consegna/youtube.md` | titoli, descrizione con capitoli, tag |
| `consegna/YT_TOFU_02-v2.srt` | sottotitoli per la traccia YouTube |
| `controlli/QC.md` | **CONSEGNABILE**, 17 controlli su 17 |

## Cosa cambia rispetto alla v1

### Difetti della v1 che la v2 toglie

Il video v1 consegnato contiene quattro riprese doppie o attacchi monchi. Sono stati verificati con sonde brevi sul file v1:

| v1 | cosa si sente nel v1 |
|---|---|
| 1:05 | "mancano ancora due ore e… mancano ancora due ore e mezza" |
| 9:27 | "devi iniziare a pensare… devi iniziare a pensarlo come…" |
| 10:29 | "Si pa… no… si parte dal diaframma" |
| 11:36 | "si accorgono che il calo delle tre si è appiattito / si accorgono che il calo delle tre si appiattisce" |

A questi si aggiungono un "qua" e un "di" sospesi. Due testi a schermo della v1 avevano un problema di comunicazione sanitaria:

- la card **"IL RISULTATO: 8 ore"**, subito prima di "è quello che facciamo in studio", leggeva come una promessa del trattamento. È stata sostituita con la card del lato sintomatico ("20 min di lucidità apparente, nel migliore dei casi");
- la chiusura **"NON È ANSIA. È RESPIRAZIONE."** toglieva il "molte persone" che lei dice e negava una diagnosi. Ora è "ANSIA E RESPIRAZIONE".

Infine, nei sottotitoli v1 mancava la prima parola di molte frasi ("tuo cervello consuma"): erano 143 parole su 2161.

### Novità

- **Inquadrature dinamiche dal 4K**: 109 pezzi, taglio largo, medio o stretto centrato sul volto. A ogni giunta il taglio cambia: niente più dissolvenze.
- **Titoli dietro la presentatrice** per i 4 capitoli, posizionati sulla sagoma misurata.
- **8 enfasi** in taglio stretto sulle frasi della tesi.
- **Card** posizionate sul volto misurato, con glosse che tengono i qualificatori di lei ("circa", "fino al", "forse meno", "in molte persone").
- **Sound design** sintetizzato: whoosh, tick, colpi bassi sotto la voce. Niente musica: serve un brano con licenza in `assets/musica/`.
- **Coda muta di 4,8 s** per la chiusura: nella v1 la scheda finale copriva l'ultima frase.

## Montaggio

18 tagli di regia e 30 pause oltre 0,85 s accorciate a 0,45 s. Ogni taglio, con il motivo, sta in `regia.json` → `tagli`.

Ripetizioni tenute perché volute (`regia.json` → `scartati`):

- "ti sei convinto che sia normale… ti sei convinto che sia colpa tua";
- "cinque respiri profondi… cinque respiri profondi non lo decomprimono";
- "il tuo cervello non si stanca, soffoca… il tuo cervello alle tre non si sta stancando".

Le 46 giunte sono state riascoltate sul file finale con sonde da 4 s: nessuna ripetizione, nessuna parola monca. La giunta G05 resta segnalata, ma è la ripetizione retorica qui sopra.

## Revisione del regista (20/10)

Applicati: card del risultato tolta, chiusura riformulata, glosse con i qualificatori, apertura "sempre **allo** stesso punto", Shorts 2-4 rifatti (hook detti dentro lo short, attacchi che dicono di cosa si parla), un'enfasi spostata dove la card non la copriva. Tolta anche la correzione "calo dell'interesse" → "calo delle tre", che era un'ipotesi: le sonde dicono che lei ha detto "dell'interesse".

## Da decidere: Carlos

Queste sono scelte editoriali o di contenuto, non papere: l'agente le propone e non le applica.

1. **Cold open.** La prima tesi arriva a 1:25 ("Non è colpa tua"). Si potrebbe aprire con "Il tuo cervello non si stanca, soffoca." (1,8 s, sorgente 1031,8-1034,4), che è anche la miniatura, prima di "Le tre del pomeriggio". Per un pubblico freddo i primi 10 s contano.
2. **Passaggio ripetuto.** La descrizione del trattamento compare due volte, quasi con le stesse parole: 7:47 ("rilascio del diaframma, mobilità delle prime coste…") e 10:21 ("si parte dal diaframma… si rilascia il tratto cervico-dorsale…"). Togliere il secondo (sorgente 905-935) farebbe risparmiare circa 30 s.
3. **Frasi di risultato nel parlato** (non sono testo a schermo, ma restano comunicazione sanitaria): "due giorni dopo riporta che il calo… è ridotto" (8:08), "non l'hai persa per sempre… si recupera con un lavoro mirato" (10:50), "il calo delle tre si appiattisce, il quarto caffè non gli serve più" (11:31). Vengono subito dopo la presentazione del trattamento in studio. Tagliare 11:20-11:45 risolverebbe anche parte del punto 2.
4. **Musica**: serve un brano con licenza.

## Da sapere

- Nessun volto di terzi: i due campioni con "due volti" erano le mani giunte.
- I titoli dietro nascondono dietro la testa fra il 23 e il 30% della parola peggiore. È l'effetto copertina: si leggono perché lei pronuncia la frase in quel momento.
- `renders/pezzi/` (2,7 GB) e `renders/YT_TOFU_02-v2_pulito.mp4` (2,8 GB) si possono cancellare a lavoro chiuso: si rigenerano con `./mve monta`.

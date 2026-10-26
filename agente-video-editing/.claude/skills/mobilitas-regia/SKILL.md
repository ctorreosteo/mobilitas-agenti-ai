---
name: mobilitas-regia
description: Come si scrive regia.json per un video @Studio_Mobilitas — il file con tutte le decisioni del montaggio. Copre i tagli delle papere (come leggere il referto, quale ripresa tenere, quando un taglio è "esatto"), il ritmo, le enfasi, le card, i capitoli e i titoli dietro, gli Shorts, la miniatura e i testi YouTube. Usala ogni volta che scrivi o correggi regia.json, o quando devi giudicare un montaggio.
---

# mobilitas-regia

Il motore esegue, la regia decide. Tutte le decisioni di un video stanno in `videos/<slug>/regia.json`; lo schema completo è in `references/schema.md`, un esempio vero è `videos/YT_TOFU_02-v2/regia.json`.

Le decisioni si prendono in due momenti diversi, su due trascrizioni diverse:

1. **i tagli** si decidono sulla **sorgente** (`data/trascrizione.txt`, `controlli/papere.md`), con tempi in secondi sorgente;
2. **tutto il resto** (card, capitoli, enfasi, Shorts) si ancora a **frasi del montato** (`data/parole-montato.json`), dopo la fase `audio`.

## 1. I tagli

### Leggere

Leggi `data/trascrizione.txt` dall'inizio alla fine. È un blocco di parlato per riga, ognuno trascritto da solo, con inizio e fine misurati e la pausa che lo precede:

```
[   79.40-   83.54] ( 1.3) Guardi l'orologio, sono le 4 meno un quarto, mancano ancora due ore e...
[   84.97-   89.20] ( 1.4) Mancano ancora due ore e mezza alla fine della giornata e tu, dentro,
```

Poi leggi `controlli/papere.md`: le regioni sospette con i segnali, le sonde PRIMA/DOPO e i blocchi di quel tratto. Il referto non sostituisce la lettura: in YT_TOFU_02 un falso attacco ("Si par… no") non l'aveva segnalato nessun segnale.

Cosa si taglia:

| cosa | esempio | come |
|---|---|---|
| ciak e saluti in testa | "3, 2, 1, tofu 2" | `da: 0` fino al primo blocco buono |
| ripresa doppia | "mancano ancora due ore e…" / "Mancano ancora due ore e mezza…" | si tiene **la seconda**; si taglia dalla fine dell'ultima parola buona prima della ripresa monca all'inizio della ripresa buona |
| regia a voce | "ho sbagliato", "torna su", "stoppa", "vai ragazzi" | tutto il tratto fra l'ultima frase buona e la ripresa |
| attacco monco | "Si par…" / "no" / "si parte dal diaframma" | dal blocco monco alla ripartenza |
| interiezione o coda isolata | "qua", "ok", un "di" sospeso | il blocco e la pausa attorno |
| coda | "mi sa che abbiamo finito" | `a: null` |

Cosa **non** si taglia, e va in `scartati` con il motivo:

- la **ripetizione retorica**: "ti sei convinto che sia normale… ti sei convinto che sia colpa tua";
- l'**argomento ripreso**: "cinque respiri profondi sono meglio di zero… cinque respiri profondi non lo decomprimono";
- la **frase chiave e la sua spiegazione**: "il tuo cervello non si stanca, soffoca… il tuo cervello alle tre del pomeriggio non si sta stancando".

La domanda è sempre la stessa: *lei voleva dirlo due volte?* Se sì si tiene, se l'ha rifatto perché era venuto male si taglia.

### Gli ancoraggi

```json
{"da": 112.62, "a": 144.07, "motivo": "prima ripresa di 'Non sei pigro' + 'ho sbagliato, torna indietro'"}
```

- `da` = fine dell'ultimo blocco da tenere, `a` = inizio del blocco da cui si riprende. Usa i tempi dei **blocchi** (misurati), non quelli delle parole (il DTW a volte collassa più parole sullo stesso istante).
- Il motore aggancia l'ancoraggio al confine di blocco più vicino (entro 0,35 s), cerca il fondo di sala e sceglie il campione più silenzioso.
- **Taglio dentro un blocco** (la ripresa doppia inizia a metà frase): serve un micro-silenzio fra due parole. Lo trovi sull'inviluppo (vedi `references/schema.md`, "trovare un micro-silenzio") e marchi quel lato `"esatto": "da"` (o `"a"`, o `true` per entrambi).
- `motivo` lo leggi tu, lo legge Carlos nel BRIEF e lo stampa `dove`: scrivi cosa c'era, con le sue parole.

### Il ritmo

`"ritmo": "medio"` accorcia le pause oltre 0,85 s a 0,45 s. `"calmo"` (1,3 → 0,65) per un video riflessivo, `"serrato"` (0,6 → 0,32) per un video denso. Le pause che contano (dopo la frase chiave) vanno in `pause_da_tenere` con il tempo sorgente.

## 2. Le enfasi

Punch-in stretto sulle frasi che portano la tesi. Sono il modo di dire *questo conta* senza grafica.

- **5-9 in un video da 13 minuti.** Di più non sono più enfasi.
- Le frasi brevi e nette: "stai ventilando, non stai ossigenando", "il caffè delle tre non sta risolvendo il calo, lo sta scavando", "non è un problema di testa".
- La frase d'ancoraggio sono le prime 3-5 parole della frase, come le scrive `parole-montato.json`: lo stretto parte lì e finisce a fine frase.
- Una card vince su un'enfasi: se cadono insieme, il taglio resta largo per la card.

## 3. Le card

Una card per ogni **numero che lei dice**: percentuali, centimetri, minuti, ore. Niente card su concetti senza numero (quelli sono enfasi o capitoli).

- `valore` e `unita` sono le sue cifre; `glossa` riformula la sua frase, non aggiunge (mai "secondo gli studi" se lei non lo dice).
- **La glossa tiene i suoi qualificatori.** Riassumere toglie proprio quelli: "circa", "anche del", "forse meno", "in molte persone". Senza, il numero diventa più assoluto di come lei lo dice. Se dice "anche del 30 o 40%" l'eyebrow è `FINO AL`, non un dato medio.
- **Nessuna card sul risultato del trattamento.** Una frase come "ti restituisce la capacità di lavorare 8 ore" seguita da "è quello che facciamo in studio", scritta in grande sotto `IL RISULTATO`, diventa una promessa. Il numero va sul meccanismo, non sull'esito.
- `eyebrow` è un'etichetta di una o due parole, in maiuscolo: cosa misura il numero (`OSSIGENO`, `DOPO 5 ORE`, `IN STUDIO`).
- Il lato lo sceglie `inquadra` sul volto; tu scegli solo la frase.
- **Ogni card è un'infografica**: il numero conta, la scala sotto si riempie (`%`, `cm`, `min`). Quando lei confronta due misure ("3-4 centimetri… dopo 4-5 ore si muove di un centimetro"), sulla seconda card metti `"prima": "3-4"`: il numero scende e la scala tiene il fantasma del valore di partenza. È il momento più forte della grafica: cercalo. `prima` deve essere un numero che lei ha detto.
- **Il titolo corto rende di più.** Con la testa al centro il motore mette il titolo in colonna su un lato: lì il corpo dipende dalla parola più lunga ("METABOLICO" esce a ~100 px, "MASCHERA" a ~120). Due-tre parole per riga, parole brevi quando lei ne offre.

## 3 bis. Molte infografiche: dove cercarle

Le card non sono solo numeri. Rileggendo la trascrizione si cercano i momenti in cui il
discorso **ha una forma** e la si disegna, con le sue parole (tipi e campi: `references/schema.md`):

| quando lei… | tipo |
|---|---|
| dice un'ora ("sono le tre meno dieci") | `orologio`, con lo spicchio se dice quanto manca |
| conta qualcosa ("quarto caffè, o forse il quinto") | `icone` |
| elenca ("che è il pranzo, che è la glicemia…") | `lista`; se poi le smonta, `annulla` |
| nega ("non è metabolico, non è mentale") o contrappone ("se respiri bene… se respiri male") | `lista` con ✓ / ✗ |
| spiega una causa che ne porta un'altra | `catena` |
| dice la frase chiave | `citazione` (una o due per video, non di piu) |
| descrive il corpo: postura, diaframma, coste | `postura`, `anatomia` |
| descrive un andamento nel tempo ("ti dà una spinta… poi cadi piu in basso") | `curva` |
| mette a confronto due misure, anche per assurdo | `barre` |
| due approcci opposti | due `lista` con `lato` sinistra e destra |

Nel banco di prova sono 27, circa una ogni 30 s. Ogni voce si ancora alla frase in cui la dice:
la grafica segue la voce, non la anticipa. Le card lunghe (liste, catene) tengono il taglio largo
per tutto il tempo: non metterne due lunghe di fila senza respiro.

**Mai un'infografica sui risultati del trattamento** ("respiro diversamente", "il calo si riduce",
"lavorare otto ore"): sono esiti riferiti, disegnati diventano promesse. Si disegna il meccanismo,
e cosa si fa in studio (le zone), mai cosa si ottiene.

## 3 ter. Scene a tutto schermo: i momenti epici

La scena copre la presentatrice per qualche secondo e fa della sua frase la protagonista: è la
"Motion in casa" (Claude Motion vive solo in claude.ai e non è raggiungibile dal motore; il motore fa
lo stesso lavoro da solo, sincronizzato alla voce). Va usata poco, dove il video deve **colpire**:

- l'apertura, se le prime parole sono un gancio ("Le tre del pomeriggio, sempre allo stesso punto");
- la frase-tesi che rovescia qualcosa ("Stai ventilando, non stai ossigenando"), con `effetti`
  sulla parola che fa il lavoro: `spegne` su "si spegne", `barra` sulla parola negata, `sottolinea` sulla nuova;
- un confronto numerico che lascia a bocca aperta (2% del peso, 20% dell'ossigeno): `confronto`;
- il numero che regge tutto il video: `numero`.

Cinque-sei per 13 minuti, mai due a meno di 15 s, mai più di 8 s l'una (oltre, lei sparisce troppo a
lungo). Una scena sostituisce la card o l'enfasi che c'era su quella frase: non sovrapporle. Le parole
sono le sue, intere; niente scena sui risultati del trattamento.

## 4. Capitoli e titoli dietro

- **3-5 capitoli**, uno ogni 2-4 minuti, sulle frasi in cui il discorso cambia passo. Il titolo sono **le sue parole** ("MECCANICO, / NON METABOLICO").
- `"dietro": true` (il default da usare): il titolo passa dietro la presentatrice mentre lei dice la frase. Entra sulla parola d'ancoraggio, dura 2,6-4 s, e nascondi niente: i sottotitoli si spengono da soli durante il titolo.
- `titolo_youtube` è la riga del capitolo in descrizione: frase intera, minuscole, comprensibile da sola.
- `capitolo_iniziale` e `capitolo_finale` chiudono la lista dei capitoli YouTube (minimo tre, ognuno almeno 10 s: `consegna` lo controlla).

## 5. Apertura, chip, chiusura

- `apertura`: l'aggancio dei primi 5 s, con le sue parole d'attacco ("LE 3 DEL POMERIGGIO, / SEMPRE LO STESSO PUNTO").
- `chip`: nome e ruolo, letti da ciò che si vede in inquadratura (il cartoncino) o dati da Carlos. Si ancora alla prima frase dopo l'aggancio.
- `chiusura`: il prossimo video (con le parole con cui lei lo annuncia) e la CTA. Attenzione agli assoluti: lei dice "molte persone che soffrono di ansia non hanno un problema di ansia"; "NON È ANSIA. È RESPIRAZIONE." toglie "molte persone" e nega una diagnosi. Meglio il tema ("ANSIA E RESPIRAZIONE") che la tesi compressa.
- La chiusura è una scheda piena: parte dopo l'ultima parola. Lascia nell'ultimo taglio 4-5 s di coda muta (lei ferma in camera), o la scheda coprirebbe l'ultima frase.

## 6. Shorts

Da 3 a 5 momenti che **stanno in piedi da soli**:

- iniziano con una frase che apre una domanda o afferma qualcosa di netto; mai con "e", "quindi", "perché";
- finiscono su una chiusura (la frase che risolve), non a metà ragionamento;
- 25-75 s; il motore avvisa sopra i 3 minuti;
- `hook`: due righe brevi in maiuscolo, la seconda è quella in menta. È l'unico testo dello short che non è sottotitolo: **deve essere detto dentro lo short**, non altrove nel video. "ALLE 3 RESPIRI A METÀ" su uno short in cui lei dice "un centimetro, forse meno" è testo inventato. La scelta più sicura sono le sue parole: "STAI VENTILANDO, / NON OSSIGENANDO".
- L'attacco deve dire di cosa si parla: "Lo prendi perché funziona" senza aver nominato il caffè non sta in piedi.

## 7. Miniatura e YouTube

- `miniatura.righe`: due righe, massimo tre parole l'una, leggibili a 168 px. L'immagine la sceglie il motore (qualità del volto di Vision).
- `youtube.titoli`: tre proposte sotto i 70 caratteri. Curiosità + beneficio, nessuna promessa di guarigione.
- `youtube.descrizione`: 3-5 frasi che riassumono il meccanismo con le sue parole; i capitoli li aggiunge `consegna`.
- `glossario`: i termini tecnici del video. Aiutano whisper a scriverli bene.

## 8. Revisione del regista

Dopo aver scritto la regia editoriale lancia il subagente `regista`. Al collaudo su YT_TOFU_02 ha trovato due problemi di comunicazione sanitaria che la v1 aveva pubblicato, tre testi non detti e quattro glosse senza qualificatori. Le sue proposte sui contenuti (cold open, togliere un passaggio ripetuto, frasi promozionali nel parlato) **non si applicano da sole**: vanno nel BRIEF come decisioni per Carlos.

## 9. Correzioni

`correzioni` corregge **solo il testo** (sottotitoli, SRT), mai l'audio: `["gambia", "gabbia"]`. Una correzione deve correggere un errore di whisper, non quello che lei ha detto davvero: prima di scriverla verifica con una sonda da 2-3 s. "calo dell'interesse" in YT_TOFU_02 era stato "corretto" in "calo delle tre" per ipotesi; le sonde dicono che lei ha detto proprio "dell'interesse". Il QC elenca le parole che whisper ha perso nei sottotitoli: si recuperano qui (`["ti senti nuovo", "ti senti di nuovo"]`). Il primo elemento è una regex senza `\b` (le aggiunge il motore); più parole sono ammesse ("calopo meridiano"). Rileggi i sottotitoli dell'anteprima: i refusi ricorrenti di whisper su questo canale sono già nell'esempio di YT_TOFU_02-v2.

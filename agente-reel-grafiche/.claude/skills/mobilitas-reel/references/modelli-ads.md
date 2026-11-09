# I modelli degli ads 9:16: i dati

Sono i cinque modelli attivi per gli ads (catalogo del 04/11/2026). Sono nati sul video AD_CERVICALGIA_AI-Barontini, e i valori sotto sono quelli approvati da Riccardo. L'esempio completo è [esempio-piano-AD_CERVICALGIA.json](esempio-piano-AD_CERVICALGIA.json).

Regole che valgono per tutti i modelli:

- Ogni grafica è `{"modello": "<nome>_ads", "usa": [...], "s": 0, "e": <durata>, "dati": {...}}` dentro `elementi`.
- I tempi sono in secondi dall'inizio della pagina, cioè dal fotogramma `f0`.
- Coordinate in px del quadro 1080×1920.
- Corpo minimo 84 (1,5 volte i sottotitoli da 45 px).
- I campi `_cosa` sono commenti e il motore li ignora.

## `etichette-barrate-finestra`: modello `etichette_ads`, `usa: ["etichette_luce"]`, modo «finestra»

Due o tre cose che la voce nega («niente medicine», «niente esercizi a casa»).

| campo | cosa | AD_CERVICALGIA |
|---|---|---|
| `modo` | `"finestra"` | |
| `rett` | `rett_grafica` dell'inquadratura (radiografia) | `{x:28, y:373, w:1024, h:549, r:67}` |
| `x`, `y` | angolo della prima pillola | 153, 466 |
| `corpo`, `spazio` | corpo e spazio fra le pillole | 88, 30 |
| `voci` | `[{testo, t, barra_t, larg}]`: compare a `t`, barrata a `barra_t`; `larg` è la larghezza della pillola in px | «medicine» 0,067 / 0,867; «esercizi a casa» 1,367 / 2,433 |
| `luce`, `barra`, `barra_px`, `barra_resta`, `barrata` | `"forte"`, `"panna"`, 10, 0,85, 0,55 (approvati) | |

Pagina di 94 fotogrammi: la grafica finisce sull'ultimo, perché l'uscita deve chiudersi sull'ultimo fotogramma reso.

## `card-accese-9x16`: modello `card_accese_ads`, `usa: ["card_accese"]`, modo «tutto schermo»

Elenco di tre cose annunciate prima («ecco 3 motivi… primo… secondo… terzo»).

| campo | cosa | AD_CERVICALGIA |
|---|---|---|
| `apparizioni` | `[{s, e, esce: "taglio"}]`: la scena c'è solo qui, in mezzo il video base | 4 apparizioni: 0–3,57; 6,67–8,77; 12,07–14,77; 20,63–22,07 |
| `titolo` | `{cifra, testo, t}`: la cifra compare già giusta, mai decifrata | `{cifra:"3", testo:"motivi", t:0}` |
| `carte` | `[{num, t_num, chiave, t_chiave, t_stato}]`: `num` sul «primo/secondo/terzo» detto, `chiave` sulla frase; `t_stato` è quando le altre vanno sotto il velo | |
| `x, y, w, h, gap, rot` | card una sotto l'altra, inclinate | 70, 478, 940, 230, 36, 5 |
| `corpo`, `corpo_titolo`, `y_titolo` | testo ≤ ~730 px a corpo 87 | 87, 132, 300 |
| `t_entra`, `t_riepilogo`, `lucine`, `pulsa`, `velo` | entrata delle card spente, riepilogo, luci dell'apertura, velo 0,48 | |

## `equazione-finestra`: modello `equazione_ads`, modo «finestra»

La voce somma due cose che danno un risultato.

| campo | cosa | AD_CERVICALGIA |
|---|---|---|
| `rett` | `[{da, x, y, w, h, r}]`: cambia sul fotogramma del taglio d'inquadratura | inq. 3 `{da:0, 27,375,1026,550,67}`, inq. 4 `{da:2.4667, 28,373,1024,550,66}` |
| `righe` | `[{testo, t, y}]`, `{op:"+", t_op}`, `{op:"=", t_op, testo, t, chiave:true, luce}` | «sciogliere la tensione» + «liberare il movimento» = «sollievo» / «a lungo termine» |
| `centra` | `[{t, dy}]`: il blocco resta centrato quando arrivano le righe | |
| `barra` | `{t, y, larghezza}` sotto il risultato | |
| `corpo`, `entra_fr`, `sfalsa_fr`, `cancella_fr`, `t_via` | 84; uscita «cancella» che finisce sul fotogramma prima della grafica dopo | |

Termini ≤ ~930 px a corpo 84. Le decifrazioni usano solo lettere.

## `card-con-spessore-9x16`: modello `card_spessore_ads`, `usa: ["card_spessore", "card_accese"]`, modo «tutto schermo»

Tre frasi brevi non numerate (obiettivi, non garanzie), quando le card accese sono già state usate subito prima.

| campo | cosa | AD_CERVICALGIA |
|---|---|---|
| `apparizioni` | `[{s, e}]`, a taglio | 0–3,53; 4,43–6,67; 7,33–9,73 |
| `titolo` | `{testo, chiave:true, t, t_chiave, y, corpo, subito:true}`: l'ultima parola verde, che entra senza maschera | «il nostro obiettivo» |
| `carte` | `[{testo: "*verde*\|seconda riga", t, t_stato}]`: al massimo due righe | «*girare la testa*\|senza pensarci» |
| `x, y, larghezza, altezza, spazio, corpo` | | 70, 464, 940, 242, 24, 84 |
| `t_gusci`, `gusci_passo`, `guscio` | card vuote e spente (velo 0,6) dal primo fotogramma, a cascata | 0,967, 0,25, 0,6 |
| `velo`, `t_riepilogo` | velo delle card già dette (0,45), riepilogo con tutte piene | |

## `chiusura-9x16`: modello `chiusura_ads`, `usa: ["card_accese"]`, modo «tutto schermo» fino all'ultimo fotogramma

Chiamata all'azione con prezzo e modulo detti dalla voce. Quattro momenti in fila, e uno entra solo dopo che il precedente è uscito.

| momento | campi | AD_CERVICALGIA |
|---|---|---|
| `lista` | `{titolo:{testo, t, corpo, subito}, y, via, righe:[{testo, t, chiave, corpo, dopo}]}` | «stiamo riservando / gli ultimi / trattamenti / specifici / nel nostro studio» |
| `prezzo` | `{pre:{testo,t,corpo}, cifra:{testo,t,corpo}, y, su:{t, dy, scala}}`: la cifra compare già giusta, esattamente come detta | «a soli» «€49» |
| `modulo` | `{t, x, y, w, h, campo_y0, campo_passo, campo_h, campi:[t…], bottone:{testo, t, y, h, corpo}, via}`: campi vuoti senza etichette; il pulsante con una parola detta | «compila» |
| `marchio` | `{testo:{testo,t,corpo}, y, disco, disco_y, logo_t, logo_y, logo_w, bottone_y, freccia_t, freccia_y, freccia_w, freccia_tratto, rimbalzo}` | «ci vediamo», logo su «in Mobilitas», freccia verso il pulsante dell'ad |

Mai numeri di posti, mai prezzi barrati.

## Varianti in prova (fase 5, 04/11/2026)

Hanno gli stessi dati del modello di partenza: cambiano solo `modello` e `usa`. Si usano al posto del modello di partenza e diventano attive solo con l'ok di Riccardo.

| catalogo | `modello` | `usa` | cosa cambia |
|---|---|---|---|
| `equazione-finestra-v2` | `equazione_ads2` | `["equazione_ads"]` | il fondo pieno entra a taglio al primo fotogramma; nessun termine prima del fotogramma dopo (`attesa_fr`, 1) |
| `etichette-barrate-finestra-v2` | `etichette_ads2` | `["etichette_luce", "etichette_ads"]` | il fondo entra ed esce a taglio (si ignora `entra_fr`); le pillole entrano ed escono dentro il fondo pieno |
| `chiusura-9x16-v2` | `chiusura_ads2` | `["card_accese", "chiusura_ads"]` | «ci vediamo» entra intero senza maschera (opacità, salita, sfocatura); giro 3: anche le righe della lista e «a soli» |

Giro 3 (fase 5, 04/11/2026, ok di Riccardo per un ultimo giro):

- `equazione-finestra-v2`: l'uscita «cancella» va a parole intere e `t_via` lo calcola il modello (quello del piano si ignora): l'ultimo fotogramma mostra la prima parola della prima riga, mai una parola a metà né una finestra vuota;
- `etichette-barrate-finestra-v2`: le pillole restano nitide fino al taglio (niente uscita sfocata di `etichette_luce`);
- `chiusura-9x16-v2`: nessun testo sale da una maschera.

## «pensato per» nell'equazione

Una riga in più in `righe`, sopra il primo termine, non verde: `{"testo": "pensato per", "t": <parola>, "y": ...}` (sposta di una riga gli altri e i `centra`). Si mette quando la voce lo dice; è **obbligatoria** quando il risultato, letto da solo, sembra una promessa («ridurre gli attacchi»). Va in `testi_detti` come le altre.

## Modelli nuovi per gli ads (AD_REFLUSSO, 04/11/2026, tutti «in prova»)

I dati di ognuno sono descritti in testa al suo file `motore/inserti/scene/<modello>.js`; gli esempi veri sono nei piani di AD_REFLUSSO, AD_EMICRANIA e AD_BRUXISMO (`videos/<slug>/piano.json`).

| catalogo | `modello` | `usa` | modo | per |
|---|---|---|---|---|
| `connettore-finestra` | `connettore_ads` | `[]` | finestra | «pensato per» + due azioni legate da una linea con nodo, poi il risultato |
| `parole-finestra` | `parole_ads` | `[]` | finestra | una riga d'apertura e parole dette una per volta (una sola luce piena per volta; `attenua` 0,62) |
| `fumetto-finestra` | `fumetto_ads` | `[]` | finestra | una frase detta da altri («ci devi convivere»), con i puntini prima |
| `etichette-barrate-finestra-centrate` | `etichette_centrate_ads` | `["etichette_luce", "etichette_ads", "etichette_ads2"]` | finestra | due negazioni centrate; la prima pillola c'è dal primo fotogramma |
| `card-accese-9x16-carrello` | `card_carrello_ads` | `["card_accese", "card_accese_ads"]` | tutto schermo | tre motivi, una card grande per volta, frase su due righe |
| `riga-icone-9x16` | `riga_icone_ads` | `[]` | tutto schermo | tre obiettivi concreti con icone (letto, sveglia, pizza, calendario, valigia, lampadina, luna, alba, dente); `pannello.sopra` per metterlo sopra i riquadri |
| `anatomia-scena-9x16` | `anatomia_ads` | `[]` | tutto schermo | un disegno Servier con frecce generiche e righe dette |

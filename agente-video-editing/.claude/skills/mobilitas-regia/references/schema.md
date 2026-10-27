# regia.json: schema

Tutti i campi sono facoltativi tranne `tagli`. I tempi dei tagli sono in **secondi sorgente**; tutte le `frase` sono ancoraggi sul **montato** (`data/parole-montato.json`), confrontati senza accenti, senza punteggiatura e con cifre e lettere equivalenti ("otto" = "8").

```jsonc
{
  "titolo_lavoro": "…",                 // per il BRIEF
  "messaggio": "…",                     // la tesi in due righe: guida enfasi e Shorts
  "ritmo": "medio",                     // calmo | medio | serrato | {"pausa_max": 0.9, "resta": 0.5}
  "pause_da_tenere": [1031.5],          // tempi sorgente di pause da non accorciare
  "glossario": ["diaframma", "…"],      // prompt per whisper

  "tagli": [
    {"da": 0.0, "a": 14.21, "motivo": "ciak"},
    {"da": 82.10, "a": 84.97, "esatto": "da", "motivo": "ripresa doppia …"},
    {"da": 1161.43, "a": null, "motivo": "coda"}
  ],
  "scartati": [{"t": 97.2, "perche": "ripetizione retorica voluta"}],
  "giunte_ok": [5],                     // giunte segnalate dal QC ma volute (numero G..)

  "correzioni": [["gambia", "gabbia"], ["calopo meridiano", "calo pomeridiano"]],

  "enfasi":   [{"frase": "stai ventilando non stai ossigenando", "livello": "stretto", "max": 5.0}],
  "card":     [{"frase": "il tuo cervello consuma", "eyebrow": "OSSIGENO", "valore": "20", "unita": "%",
                "glossa": "dell'ossigeno che entra nel corpo se lo prende il cervello", "durata": 4.2},
              {"frase": "si muove di un", "eyebrow": "DOPO 4-5 ORE", "valore": "1", "unita": "cm",
               "prima": "3-4",          // il numero scende da 3-4 a 1, la scala mostra il confronto
               "glossa": "…"}],         // "grafico": "no" toglie la scala (%, cm, min)
  "capitoli": [{"frase": "meccanico non metabolico", "eyebrow": "MECCANISMO", "l1": "MECCANICO,",
                "l2": "NON METABOLICO", "titolo_youtube": "Il calo è meccanico, non metabolico", "dietro": true}],

  "apertura": {"eyebrow": "MOBILITAS · STUDIO OSTEOPATICO", "l1": "…", "l2": "…"},
  "chip":     {"frase": "adesso è diverso", "name": "MOBILITAS", "role": "STUDIO OSTEOPATICO"},
  "chiusura": {"eyebrow": "PROSSIMO VIDEO", "l1": "…", "l2": "…", "cta": "ISCRIVITI AL CANALE", "brand": "…"},
  "capitolo_iniziale": "Le 3 del pomeriggio",
  "capitolo_finale": {"frase": "nel prossimo video", "titolo": "Nel prossimo video: …"},

  "shorts": [{"da": "il tuo cervello consuma", "a": "fisiologia di base",
              "hook": ["IL TUO CERVELLO", "SI PRENDE IL 20%"], "titolo": "…"}],
  "miniatura": {"righe": ["IL CERVELLO", "SOFFOCA"], "eyebrow": "ALLE 3 DEL POMERIGGIO"},
  "youtube": {"titoli": ["…"], "descrizione": "…", "tag": ["…"]}
}
```

## Ancoraggi che non si trovano

La fase si ferma con `ancoraggio non trovato` e la frase. Cerca come whisper l'ha scritta:

```bash
python3 -c "import json;W=json.load(open('videos/<slug>/data/parole-montato.json'));print(' '.join(w[2] for w in W))" | grep -o '.\{40\}cervello.\{40\}'
```

Usa una sequenza **abbastanza specifica**: "il calo delle tre" compare quattro volte, "meccanico non metabolico" una.

## Trovare un micro-silenzio dentro un blocco

Quando la ripresa doppia comincia a metà frase ("…un quarto, mancano ancora due ore e…"), il taglio va nel buco fra due parole:

```bash
PYTHONPATH=motore .venv/bin/python -c "
from motore import audio as A
tg = A.Tagli('videos/<slug>/assets/audio-16k-mono.wav')
a, b = 81.4, 83.0                                  # il tratto attorno alla parola
i0, i1 = int(a/tg.HOP), int(b/tg.HOP)
for i in range(i0, i1):
    if tg.db[i] < tg.floor + 18: print(round(i*tg.HOP, 3), round(float(tg.db[i]), 1))
"
```

Un buco di 30-100 ms sotto `fondo + 12 dB` è un punto di taglio. Mettilo in `da` (o `a`) e marca quel lato `"esatto"`. L'EDL lo segnala come "da ascoltare" se resta sopra `fondo + 14 dB`: va ascoltato in `controlli/giunte.md`, non è un errore.

## Infografiche: i tipi di `card`

Ogni card ha `frase` (l'ingresso), `eyebrow`, e un `tipo` (default `numero`). Le voci con `frase`
entrano quando lei le dice; `coda` (default 2,6 s) e il tempo dopo l'ultima voce, `durata` lo
fissa. `lato: "sinistra" | "destra"` forza il lato, `larghezza` (default 560) lo stringe.
Due card a schermo insieme vanno da sole su lati opposti.

```jsonc
{"tipo": "numero", "frase": "…", "eyebrow": "OSSIGENO", "valore": "20", "unita": "%", "glossa": "…",
 "grafico": "punti",                                  // barra (default) | anello | punti | batteria | no
 "riferimento": {"valore": "20", "etichetta": "OSSIGENO"},   // solo punti: l'altra quantita, a contorno
 "prima": "3-4", "icona": "pulmonology"}              // prima: il numero scende; icona: dentro l'anello

{"tipo": "barre", "voci": [{"etichetta": "TIRATO PER", "testo": "10 ANNI", "misura": 315360000, "frase": "…"},
                           {"etichetta": "RILASCIATO PER", "testo": "10 SECONDI", "misura": 10, "frase": "…"}]}

{"tipo": "orologio", "ora": "15:45", "prima": "14:50", "fino": "18:15", "testo": "LE 4 MENO UN QUARTO",
 "settore_testo": "MANCANO ANCORA 2 ORE E MEZZA", "voci": [{"frase": "mancano ancora due ore"}]}

{"tipo": "icone", "icona": "local_cafe", "n": 4, "fantasma": 1, "testo": "QUARTO CAFFÈ, O FORSE IL QUINTO"}

{"tipo": "lista", "voci": [{"testo": "metabolico", "segno": "no", "frase": "…"}],   // segno: si | no | (numero)
 "annulla": "ti hanno detto tutte queste", "corpo": 32}                             // annulla: barra tutto

{"tipo": "catena", "voci": [{"testo": "…", "icona": "bolt", "frase": "…"}]}

{"tipo": "citazione", "frase": "la tua lucidità non dipende",
 "testo": "La tua lucidità non dipende da cosa pensi, ma dipende da quanto respiri."}   // parola per parola come la dice

{"tipo": "anatomia", "respiro": {"escursione": 0.28, "etichetta": "1 CM"},
 "fantasma": {"escursione": 1.0, "etichetta": "3-4 CM"}, "voci": [{"frase": "si muove di un"}],  // voci[0]: quando compare la misura
 "zone": [{"zona": "diaframma", "testo": "…", "frase": "…"}]}     // diaframma | coste | sterno | cervicale | polmoni_bassi

{"tipo": "postura", "zone": [{"zona": "spalle", "testo": "spalle proiettate in avanti", "frase": "…"}]}
                                                                 // testa | spalle | lombare | bacino | diaframma

{"tipo": "curva", "valori": [0.42, 0.44, 0.86, 0.84, 0.55, 0.26, 0.22], "base": 0.42, "base_testo": "PRIMA DEL CAFFÈ",
 "asse_x": "TEMPO", "asse_y": "LUCIDITÀ", "etichette": [{"x": 0.38, "testo": "40 MINUTI, FORSE UN'ORA", "frase": "…"}]}
```

Le icone sono Material Symbols: i nomi disponibili sono in `motore/motore/risorse/icone.txt`.
Per aggiungerne una va rifatto il sottoinsieme del font (vedi `risorse/fonts/MaterialSymbols-LICENZA.txt`).

## Scene a tutto schermo (`scene`)

Stacchi animati di 3-8 s che coprono il quadro mentre lei continua a parlare (la "Motion in casa").
Entrano 0,45 s prima della frase con una zoomata dentro il video; escono dopo l'ultima parola + `coda`
(default 0,8 s); `durata` le fissa. Mai sopra un titolo (la fase si ferma), almeno 15 s fra due scene.

```jsonc
"scene": [
  {"tipo": "parole", "frase": "se respiri bene il cervello",
   "testo": "Se respiri bene, il cervello funziona. Se respiri male, il cervello si spegne.",  // parola per parola come la dice
   "chiave": ["funziona."], "effetti": {"spegne.": "spegne"}, "eyebrow": "…"},   // effetti: spegne | barra | sottolinea
  {"tipo": "numero", "frase": "…", "valore": "30-40", "unita": "%", "testo": "di ossigeno in meno",
   "prima": "…", "grafico": "anello", "icona": "pulmonology", "voci": [{"frase": "…"}]},   // anello | punti; voci[0]: quando sale il testo
  {"tipo": "confronto", "frase": "…", "voci": [
     {"etichetta": "OSSIGENO", "testo": "20%", "sotto": "di tutto l'ossigeno", "misura": 20, "frase": "…"},
     {"etichetta": "PESO", "testo": "2%", "sotto": "del tuo peso corporeo", "misura": 2, "frase": "…"}]}  // segno: si | no
]
```

Tutte le scene accettano `lei` (`dietro` default, `finestra`, `davanti`), `lato` (dove sta lei:
`destra` default, `sinistra`), `ingresso: "frusta"` (solo `dietro`). Con `finestra` la scena puo durare
fino a ~28 s, con `davanti` ~22 s: il volto resta a schermo.

### Framework (Martell)

```jsonc
{"tipo": "passi", "id": "postura", "frase": "ecco cosa succede a quella postura", "eyebrow": "ORA DOPO ORA",
 "lei": "finestra", "voci": [{"testo": "spalle in avanti: torace alto chiuso", "frase": "le spalle in avanti chiudono"}]},
                                               // in colonna; a tutto quadro (lei dietro) fino a 4 passi vanno in fila
{"tipo": "ciclo", "frase": "…", "lei": "davanti", "voci": [{"testo": "…", "icona": "bolt", "frase": "…"}],
 "chiude": "lo sta scavando", "centro": "lo sta scavando"},  // l'anello si chiude su `chiude`, poi la luce gira
{"tipo": "matrice", "frase": "…", "asse_x": "…", "asse_y": "…",
 "voci": [{"testo": "…", "frase": "…"}, …, {"testo": "…", "frase": "…", "acceso": true}]},  // alto-sx, alto-dx, basso-sx, basso-dx
{"tipo": "piramide", "frase": "…", "voci": [{"testo": "la base", "frase": "…"}, …]},          // dal basso
{"tipo": "richiamo", "di": "postura", "acceso": 5, "frase": "il tuo diaframma è meccanicamente compresso",
 "durata": 3.2, "lei": "finestra"}            // stesse voci della scena `id`, gia tutte a schermo, acceso il pezzo 5
```

`titolo` (facoltativo) va sotto l'eyebrow di ogni framework. Il richiamo non conta nei 15 s fra due scene.

## Segni sopra il girato (`segni`)

```jsonc
"segni": [
  {"tipo": "parola", "frase": "non sei pigro e non è il pranzo", "testo": "pigro", "eyebrow": "NON SEI"},
        // `testo` dev'essere detto nella frase: sbatte quando lo dice; lato libero dal volto (inquadra)
  {"tipo": "freccia", "frase": "nella tua gabbia toracica non", "testo": "gabbia toracica",
   "dove": [0.40, 0.46, 0.60, 0.68], "etichetta_dove": [0.10, 0.36]},
        // dove: riquadro (x0, y0, x1, y1) o punto (x, y) in coordinate 0-1 della SORGENTE (./mve griglia)
  {"tipo": "cerchio", "frase": "…", "dove": [0.10, 0.80], "raggio": 120, "testo": "…"},
  {"tipo": "riquadro", "frase": "…", "dove": [0.84, 0.48, 1.0, 0.76]}
],
"finitura": {"grana": 0.45}     // pellicola su tutto il video, 0-1
```

I segni non stanno sotto una scena o un titolo (la fase si ferma) e tengono il taglio largo.

Le chiavi di `chiave` ed `effetti` si confrontano come gli ancoraggi (senza accenti né maiuscole), ma
con la punteggiatura attaccata alla parola come nella trascrizione ("spegne." non "spegne").

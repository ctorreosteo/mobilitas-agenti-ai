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
                "glossa": "dell'ossigeno che entra nel corpo se lo prende il cervello", "durata": 4.2}],
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

## Versione 2 della grafica (27/10/2026)

```jsonc
{
  "sottotitoli": "chiave",              // "parole" (default) | "chiave" = variante B: solo frasi_chiave
  "chip": {"frase": "sono nicolas ricciardi", "fino": "siamo lo studio", "name": "Nicolas Ricciardi",
           "role": "Direttore, Mobilitas", "stile": "v2"},
  "frasi_chiave": [{"frase": "ma ora parliamo di te", "testo": "Ma ora parliamo di te.", "chiave": "di te.",
                    "lato": "sx", "freccia": false, "max": 8.0}],   // lato del pannello; persona dall'altro
  "inserti": [{"modello": "numero", "frase": "su google trovi", "fino": "ma ora parliamo", "persona": "sx",
               "lato": "dx", "prefisso": "più di", "valore": 900, "etichetta": "recensioni su Google",
               "conta": {"frase": "più di 900"}}],
               // ogni dizionario con "frase" riceve "t" (relativo all'inizio); "fino": null = fino in fondo;
               // "persona_fino": la persona resta spostata solo fino a quella frase
  "broll": [{"frase": "a visite posturali", "fino": "e non ti lasciamo", "layout": "affiancati",
             "clip": ["broll/collo/V15_Farò-2.mp4", "broll/collo/V11_Jeann-1.mp4"]}],
             // layout: pieno | affiancati | sequenza; "tratto": [s] opzionale (default: il tratto stabile)
  "materiali_vietati": ["render_4.png"],   // fermano la fase inserti e il QC
  "etichette_strutturali": ["PRIMA", "DOPO", "Nome"]   // testi a schermo ammessi senza essere detti
}
```

Campi di ogni modello di inserto: `aggancio` (righe [{testo, chiave, frase}]), `numero` (prefisso, valore, etichetta, conta), `sagoma` (piega, chiave, gradi), `prodotto` (titolo, etichetta, etichetta_pos, voci, riduci), `telefono` (schermate [{file, tipo, frase}], chiave), `primadopo` (foto_prima, foto_dopo, etichette), `lista` (passi [{frase, testo, chiave, lista, primo, freccia}]), `scelte` (scelte [{frase, domanda, risposta}]), `modulo` (campi [{frase, etichetta}], freccia), `chiusura` (titolo, voci, pieno_dopo_ultima). Esempio completo: `videos/MR_POSTURA_01_v2/regia.json`.

`barra_avanzamento` (default `true`): `false` nei mid-roll.

Tempi: un elemento deve restare finché la frase che scrive è finita (`fino` sulla frase dopo, non `max`): una frase chiave che esce mentre dice la parola chiave («soluzione magica» su «magica») non si legge. Un inserto non entra sulla coda di una parola che gli cambia il senso (il prima/dopo su «magica»). Se una giunta cade a meno di ~0,6 s dall'inizio di un inserto con `persona`, si sposta l'inizio sulla giunta (`anticipo`): altrimenti `inquadra` produce un pezzo lampo. Il passaggio fra due elementi (pannello che resta, taglio netto, ritardo dopo lo stacco) lo decide `grafica` da solo.

Il QC (`controlli_contenuto`) confronta ogni testo a schermo con le parole dette nell'intorno di 15 s: non detto = ERRORE; detto in altro ordine = AVVISO.

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

## Tipo, anteprima e validazione (v1.0, 02/11/2026)

```jsonc
{
  "tipo": "mid-roll",                    // o "youtube"; se manca vale info.txt, poi "youtube".
                                          // mid-roll: in consegna/ solo video, SRT e la scheda di validazione
  "anteprima": {"da_decidere": [          // in cima a controlli/anteprima-momenti.md (finale --anteprima)
    {"t": "0:50", "cosa": "chip «…»", "perche": "grafia del cognome da confermare"}
  ]},
  "validazione": {                        // consegna/validazione-animazioni.md: testi su misura
    "meccanismo":   {"cosa": "il bacino evidenziato sullo scheletro", "domanda": "la zona corrisponde al bacino?"},
    "meccanismo#2": {"cosa": "…"}         // il secondo elemento anatomico dello stesso momento
  }
}
```

`./mve validazione <slug>` (e `consegna`) scrive la scheda una volta sola: se c'è già
non la riscrive, perché potrebbe essere firmata. `--rifai` la rifà (firme perse).

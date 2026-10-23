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

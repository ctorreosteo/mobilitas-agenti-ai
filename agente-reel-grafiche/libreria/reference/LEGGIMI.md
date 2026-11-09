# Reference: i video da cui l'agente impara

Sono esempi di grafiche che ti piacciono, scelti da te, per dare all'agente il **livello** da raggiungere. L'agente li studia,
non li copia: niente di questi video finisce nei nostri reel.

## Dove metterle

- **Video orizzontali** (YouTube, registrazioni dello schermo): in questa cartella, `libreria/reference/`.
- **Video verticali** (reel, TikTok, Shorts): in `libreria/reference/verticali/`.

Basta trascinare il file nella cartella giusta. Vanno bene `.mov`, `.mp4`, `.m4v`, `.webm`. Se vuoi dire all'agente cosa ti
piace di una reference, scrivilo in `libreria/reference/verticali/NOTE.md` (anche per le orizzontali).

## Il nome lo sistema l'agente

Non serve rinominare niente. L'agente usa nomi fissi: `<fonte>-NN` per le orizzontali (per esempio `gadzhi-24.mov`) e
`verticale-NN` per le verticali (per esempio `verticale-12.mp4`). Se un file ha un altro nome, lo rinomina lui e lo scrive nel
report del reel.

## Quando le studia

Al **reel successivo**, prima di cominciare: è la «tappa 0». Il motore si ferma finché ogni reference nuova non ha il suo
studio. Per ognuna l'agente scrive:

- una **scheda** in `schede/` (grafiche, ritmo, tipografia, transizioni, cosa si può prendere e cosa no);
- il **ritmo** in `ritmo/` (quanti cambi visivi ogni 10 secondi);
- una riga in `catalogo.md`;
- cosa cambia nel nostro linguaggio grafico.

Nel report del reel ti dice quali reference nuove ha studiato, cosa ne ha imparato e dove le ha usate.

## I modelli nuovi aspettano il tuo ok

Se da una reference nasce un modello di grafica nuovo, nasce «in prova»: lo vedi nell'anteprima del reel e diventa definitivo
solo quando lo approvi.

## Restano sul Mac

I video delle reference non entrano nel repository e non si caricano da nessuna parte: nel repository vanno solo schede,
ritmo, catalogo, `NOTE.md` e questo file. Su un altro Mac le schede bastano: una scheda senza il suo video non blocca niente.

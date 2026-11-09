# Installazione

Per un **Mac con chip Apple** (M1, M2, M3, M4, M5). Si fa una volta sola, da Terminale, nella cartella dell'agente:

```bash
./installa.sh
```

Lo script **controlla cosa c'è già** e per ogni pezzo che manca **chiede prima** di installarlo ([s/N]). Si può rilanciare
quante volte si vuole. Alla fine fa una prova di 30 secondi e mostra il riepilogo. Gli strumenti e le versioni sono gli stessi
dell'agente video YouTube: se sul Mac c'è già quello, quasi tutto risulta presente (il modello di whisper in
`~/.cache/hyperframes/whisper/models/` viene trovato e non si riscarica).

## Cosa installa

| # | cosa | a cosa serve | spazio (stima, salvo dove misurato) |
|---|---|---|---|
| 1 | Strumenti da riga di comando di Xcode | `swiftc`: compila i programmi che usano Apple Vision (volti, mani, sottotitoli) | qualche GB |
| 2 | Homebrew | installa gli strumenti sotto | ~0,5 GB |
| 3 | ffmpeg | legge, sovrappone e codifica i video | 52 MB più le dipendenze |
| 3 | whisper.cpp (`whisper-cli`) | ascolta la voce, per agganciare le grafiche alle parole | piccolo |
| 3 | Python 3.12 | il motore (`./mve`) | ~0,1 GB |
| 3 | Node 22 o più recente | fa girare HyperFrames | ~0,1 GB |
| 4 | `.venv` con pillow 13.0.0, numpy 2.5.4, fonttools 4.67.0, brotli 1.2.1 (`motore/requirements.lock`) | grafica, analisi audio e video, font | 81 MB |
| 5 | HyperFrames **0.8.204** (fissata da `motore/inserti/package-lock.json`) | le grafiche animate | 123 MB (misurato) |
| 6 | il browser di render (Chrome senza finestra), in `motore/inserti/.casa/` | disegna le grafiche HyperFrames | 198 MB (misurato) |
| 7 | il modello whisper **large-v3** (da Hugging Face, `ggerganov/whisper.cpp`), solo se non c'è già | la voce in italiano | 3,1 GB |

Telemetria e aggiornamenti automatici di HyperFrames restano spenti; nessun video o audio esce dal Mac.

La prova finale (`.lavoro/prova-installazione/`, si cancella da sola se va bene): voce sintetica italiana di 30 s →
trascrizione con whisper → video 1080×1920 di 30 s con ffmpeg → compilazione di Apple Vision → una grafica HyperFrames di 2 s.

## Requisiti

- **RAM**: 16 GB o più consigliati (una grafica HyperFrames usa ~3,3 GB, whisper large-v3 ~3,9 GB). Con 8 GB funziona, più lento.
- **Spazio su disco**: lo spazio di lavoro di un reel (`.lavoro/<NOME>/`) arriva a circa **30 GB** per un reel di 77 s rifatto
  più volte (misurato sul frontman AD_CERV_26 dopo otto render: 31 GB), più ~0,3 GB nella cartella del reel. Si svuota a
  consegna fatta (`./mve reel-pulisci <NOME>`). Servono quindi **50 GB liberi**.
- **Tempi** (M3 Max): radiografia 3–5 min, render con controlli circa 15 min per un reel di 77 s, voto del direttore 2 min.

## Se qualcosa non va

- Se la prova finale fallisce, i dettagli sono in `.lavoro/prova-installazione/log-*.txt`.
- Per rifare un pezzo, rilancia `./installa.sh`: salta quello che c'è già.
- Per rifare solo la prova di 30 secondi, senza controllare né installare: `./installa.sh --prova`.
- Per controllare che il motore dia gli stessi risultati di sempre: `./mve reel-regressione` (circa 15 minuti).

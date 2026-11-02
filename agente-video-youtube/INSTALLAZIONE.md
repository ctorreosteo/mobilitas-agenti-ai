# Installazione

Per un **Mac con chip Apple** (M1, M2, M3, M4, M5). Si fa una volta sola, da
Terminale, nella cartella `agente-video-youtube`:

```bash
cd ~/mobilitas-agenti-ai/agente-video-youtube
./installa.sh
```

Lo script **controlla cosa c'è già** e per ogni pezzo che manca **chiede prima**
di installarlo ([s/N]). Si può rilanciare quante volte si vuole. Alla fine fa una
prova di 30 secondi e mostra il riepilogo (`./mve stato`).

## Cosa installa

| # | cosa | a cosa serve | spazio (misurato dove c'è un numero preciso, altrimenti stima) |
|---|---|---|---|
| 1 | Strumenti da riga di comando di Xcode | `swiftc`: compila il programma che usa Apple Vision (volti, sagome) | qualche GB, stima (si installa da una finestra di macOS) |
| 2 | Homebrew | installa gli strumenti sotto | ~0,5 GB, stima |
| 3 | ffmpeg | taglia, monta e codifica audio e video | 52 MB più le dipendenze |
| 3 | whisper.cpp (`whisper-cli`) | trascrive il parlato | piccolo |
| 3 | Python 3.12 | il motore (`./mve`) | ~0,1 GB |
| 3 | Node 22 o più recente | fa girare HyperFrames | ~0,1 GB |
| 4 | `.venv` con pillow, numpy, fonttools, brotli (versioni fissate in `motore/requirements.lock`) | grafica, analisi audio, font | 81 MB |
| 5 | HyperFrames **0.8.204** (fissata da `motore/inserti/package-lock.json`) | le grafiche animate | 113 MB |
| 6 | il browser di render (Chrome senza finestra), in `motore/inserti/.casa/` | disegna le grafiche HyperFrames | 208 MB |
| 7 | il modello whisper **large-v3**, in `.modelli/` (da Hugging Face, `ggerganov/whisper.cpp`) | la trascrizione in italiano | 3,1 GB |

Totale: circa **4-6 GB** (stima), secondo quello che c'è già. Telemetria e aggiornamenti
automatici di HyperFrames restano spenti; nessun video o audio esce dal Mac.

La prova finale (`.lavoro/prova-installazione/`, si cancella da sola se va bene):
voce sintetica italiana di 30 s → trascrizione con whisper → video 1080p25 di 30 s
con ffmpeg → compilazione di Apple Vision → una grafica HyperFrames di 2 s.

## Requisiti

### RAM

Misurata il 02/11/2026 su un M3 Max con 36 GB:

| lavoro | memoria |
|---|---|
| whisper large-v3, una trascrizione | **3,9 GB** (il motore ne fa fino a 3 insieme: circa 12 GB) |
| una grafica HyperFrames con la composizione della scena | **3,3 GB** |

Il motore regola da solo quanti lavori pesanti fa insieme:

| RAM del Mac | trascrizioni insieme | render insieme | come va |
|---|---|---|---|
| 8 GB | 1 | 1 | funziona, ma lento; il Mac può rallentare durante la trascrizione |
| 16-24 GB | 2 | 1 | **minimo consigliato** |
| 32 GB e oltre | 3 | 2 | come in laboratorio |

Se il Mac rallenta molto o la trascrizione si interrompe, si rilancia la fase con
`MVE_LAVORI=1` davanti (un lavoro alla volta). La tabella viene dalle misure qui
sopra; su un M1 e su un M5 non è ancora stata provata.

### Spazio su disco

Oltre all'installazione, ogni video ha bisogno di spazio di lavoro (`.lavoro/`) e
della sua cartella (`videos/<NOME>/`). Misurato in laboratorio:

| video | video finito | girato | `.lavoro/` al massimo | cartella del video |
|---|---|---|---|---|
| YT_POSTURA_32 (YouTube) | 6:50 | 13 min | **103 GB** | 14 GB (con le versioni intermedie) |
| MR_POSTURA_01_v4 (mid-roll) | 1:52 | 2 min | 48 GB (con prove e regressione) | 1,8 GB |

**Requisito di oggi: circa 15 GB per minuto di video finito, più 20 GB.** Quindi
**150 GB liberi** per un video YouTube lungo (7-8 minuti) e **60 GB** per un
mid-roll. A consegna fatta l'agente svuota `.lavoro/` da solo; il girato in
`inbox/` non si tocca.

#### Perché così tanto, e come ridurlo (proposta per la versione successiva)

Quasi tutto lo spazio è nei **fotogrammi PNG** che il motore salva per comporre
ogni momento grafico: il quadro di lui ritagliato dal 4K, le sagome per i titoli
dietro, gli strati delle grafiche. Sono circa 10 MB per fotogramma di video
finito, cioè 250 MB per secondo. Restano su disco fino alla fine, così un momento
corretto si rifà più in fretta.

1. **Cancellare i fotogrammi di un momento appena il suo video è fatto e
   controllato** (resta solo il suo MP4). Il picco scenderebbe a un momento alla
   volta: stima 5-10 GB invece di 100. Costo: un momento da correggere si rifà da
   zero, circa 1-2 minuti in più l'uno. È la riduzione più grande.
2. **Salvare il quadro ritagliato come video ad alta qualità invece che come PNG**
   (stima: da 4 a 6 volte meno spazio), senza perdere la cache.
3. **Svuotare `.lavoro/` fra una versione e l'altra** e tenere in `renders/` solo
   il master e il montato pulito: oggi le versioni intermedie restano.

La 1 e la 2 sono modifiche al motore: si provano in laboratorio sul banco di prova
e arrivano con una versione nuova. Con la 1, il requisito scenderebbe a circa
**40 GB** per un video lungo (stima, da misurare).

### Tempi

In laboratorio (M3 Max), per 20 minuti di girato: preparazione 35 s, trascrizione
4 min, volti 45 s, papere 2 min, audio 2 min, montato 8-10 min, master 10-15 min;
la grafica di un video YouTube di 7 minuti richiede 1-2 ore di render. Su un M1
servirà di più (non ancora misurato). Ogni video scrive i suoi tempi veri in
`videos/<NOME>/tempi.md`.

## Se qualcosa non va

- `./mve stato` mostra cosa manca (✗) e dove guardare.
- Se la prova finale fallisce, i dettagli sono in `.lavoro/prova-installazione/log-*.txt`.
- Per rifare un pezzo, rilancia `./installa.sh`: salta quello che c'è già.

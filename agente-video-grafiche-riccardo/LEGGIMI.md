# Agente Video Grafiche (Riccardo)

Aggiunge grafiche e infografiche ai video di @Studio_Mobilitas **già montati**, sia **verticali 9:16** (reel e ads) sia
**orizzontali 16:9** (per esempio le VSL): ads con le finestre, ads con una persona in camera, reel con solo B-roll, VSL con le
finestre. Voce, musica, sottotitoli, tagli e colori restano quelli del tuo montaggio: l'agente mette solo le grafiche,
intorno alla persona e ai sottotitoli. Prima della consegna ti fa vedere un'anteprima e aspetta il tuo ok.

## Aggiornamento alla 1.1

Dalla versione 1.1 l'agente ha un nome nuovo e una cartella nuova: **`agente-video-grafiche-riccardo`** (prima era
`agente-reel-grafiche`). Se avevi già la versione 1.0:

1. **Fai Pull in Fork** del repository `mobilitas-agenti-ai`, come sempre.
2. **Apri in VS Code la cartella nuova** `mobilitas-agenti-ai/agente-video-grafiche-riccardo` (da lì in poi lavori solo in
   questa).
3. **Apri il Terminale in quella cartella e lancia `./installa.sh`.** Serve perché l'installazione (Python, HyperFrames, il
   browser di render) non viaggia con il repository: ti chiede il permesso per ogni pezzo e salta quello che hai già.
4. **Se nella cartella vecchia `agente-reel-grafiche` hai dei video tuoi**, spostali nella cartella nuova, nelle stesse
   cartelle: `inbox/` (i video da lavorare), `videos/` (il lavoro dell'agente), `consegne/` (i video finiti), `report/`, e il
   file `libreria/uso-modelli-reel.json` (lo storico dei video che hai fatto). Se in quella cartella nuova c'è già un file con
   lo stesso nome, tieni quello che c'è e chiedi a Riccardo.
5. **Poi cancella la cartella vecchia** `agente-reel-grafiche`, solo dopo aver controllato che i tuoi video siano nella nuova.

Dopo il Pull nella cartella vecchia restano solo le cose che non viaggiano con il repository: i tuoi video e la vecchia
installazione. Se la cartella vecchia non c'è proprio, va bene così: non c'era niente di tuo. Se non avevi la 1.0, ignora
questa sezione e parti dal passo 1 qui sotto.

## Come si usa, in 5 passi

**1. Installa (una volta sola).** Apri il Terminale nella cartella dell'agente e scrivi:

```bash
./installa.sh
```

Ti chiede il permesso prima di installare ogni cosa. Dettagli e requisiti in `INSTALLAZIONE.md`.

**2. Metti il video in `inbox/`.** Crea una cartella con il nome del video, per esempio `inbox/AD_SCHIENA_03/`, e mettici
dentro il video montato (verticale 1080×1920 oppure orizzontale 1920×1080, `.mp4` o `.mov`) e, se c'è, il file dei
sottotitoli (`.srt`). Le regole sono in `inbox/LEGGIMI.md`.

**3. Chiedi all'agente.** Apri Claude Code **in questa cartella** e scrivi:

> Fai le grafiche del video AD_SCHIENA_03

L'agente riconosce da solo se il video è verticale o orizzontale. Il lavoro dura circa un'ora per un video di un minuto
(di più per una VSL di due minuti e mezzo): lascia il Mac acceso.

**4. Guarda l'anteprima e dai l'ok.** L'agente si ferma e ti indica, in `videos/AD_SCHIENA_03/anteprime/`:

- il video con le grafiche, con e senza effetti sonori;
- l'affiancato originale | nuovo;
- la tavola che mette ogni scena accanto alla reference da cui viene.

Rispondi «ok» oppure scrivi cosa cambiare («a 0:12 la card copre la mano»). L'agente rifà un'anteprima nuova finché va bene.

**5. Prendi il video.** Dopo l'ok l'agente copia il file approvato in `videos/AD_SCHIENA_03/consegna/` e in `consegne/`,
con la versione senza effetti sonori. L'agente non pubblica niente: il caricamento lo fai tu.

## Da sapere

- **Sottotitoli**: quelli del tuo montaggio non vengono mai toccati. In pochi momenti brevi una grafica a schermo pieno li
  copre del tutto; l'elenco di quei momenti è nel report del video.
- **Disegni anatomici**: solo Servier Medical Art (licenza CC BY), con il credito a schermo.
- **L'agente non cambia sé stesso qui.** Se un video ha bisogno di qualcosa che l'agente non sa ancora fare (un controllo
  diverso, un modello nuovo, una reference nuova da studiare), l'agente si ferma e scrive «Serve una modifica all'agente: va
  fatta nel laboratorio.». Passa il messaggio a Riccardo: la modifica arriva con un aggiornamento del repository.
- **Modelli nuovi**: nascono «in prova» e diventano definitivi solo quando Riccardo li approva.
- I video, le anteprime e le reference restano sul tuo Mac: non vanno nel repository e non escono su internet.

Cosa contiene questa versione: `VERSIONE.md`. Come lavora l'agente: `CLAUDE.md`. (Per Riccardo: come si aggiorna questa
cartella dal laboratorio sta in `laboratorio/ESPORTAZIONE.md`, nel laboratorio.)

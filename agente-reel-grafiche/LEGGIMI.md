# Agente reel-grafiche

Aggiunge grafiche e infografiche ai reel verticali (9:16) di @Studio_Mobilitas **già montati**: ads con le finestre, ads con
una persona in camera, reel con solo B-roll. Voce, musica, sottotitoli, tagli e colori restano quelli del tuo montaggio:
l'agente mette solo le grafiche, intorno alla persona e ai sottotitoli. Prima della consegna ti fa vedere un'anteprima e
aspetta il tuo ok.

## Come si usa, in 5 passi

**1. Installa (una volta sola).** Apri il Terminale nella cartella dell'agente e scrivi:

```bash
./installa.sh
```

Ti chiede il permesso prima di installare ogni cosa. Dettagli e requisiti in `INSTALLAZIONE.md`.

**2. Metti il reel in `inbox/`.** Crea una cartella con il nome del reel, per esempio `inbox/AD_SCHIENA_03/`, e mettici
dentro il video montato (1080×1920, `.mp4` o `.mov`) e, se c'è, il file dei sottotitoli (`.srt`). Le regole sono in
`inbox/LEGGIMI.md`.

**3. Chiedi all'agente.** Apri Claude Code **in questa cartella** e scrivi:

> Fai le grafiche del reel AD_SCHIENA_03

Se hai aggiunto reference nuove in `libreria/reference/`, l'agente le studia prima di cominciare (vedi
`libreria/reference/LEGGIMI.md`). Il lavoro dura circa un'ora per un reel di un minuto: lascia il Mac acceso.

**4. Guarda l'anteprima e dai l'ok.** L'agente si ferma e ti indica, in `videos/AD_SCHIENA_03/anteprime/`:

- il reel con le grafiche, con e senza effetti sonori;
- l'affiancato originale | nuovo;
- la tavola che mette ogni scena accanto alla reference da cui viene.

Rispondi «ok» oppure scrivi cosa cambiare («a 0:12 la card copre la mano»). L'agente rifà un'anteprima nuova finché va bene.

**5. Prendi il video.** Dopo l'ok l'agente copia il file approvato in `videos/AD_SCHIENA_03/consegna/` e in `consegne/`,
con la versione senza effetti sonori. L'agente non pubblica niente: il caricamento lo fai tu.

## Da sapere

- **Sottotitoli**: quelli del tuo montaggio non vengono mai toccati. In pochi momenti brevi una grafica a schermo pieno li
  copre del tutto; l'elenco di quei momenti è nel report del reel.
- **Disegni anatomici**: solo Servier Medical Art (licenza CC BY), con il credito a schermo. Un disegno nuovo si scarica solo
  con il tuo ok.
- **Modelli nuovi**: nascono «in prova» e diventano definitivi solo quando li approvi in un'anteprima.
- I video, le anteprime e le reference restano sul tuo Mac: non vanno nel repository e non escono su internet.

## Aggiornare il repository condiviso

L'agente si condivide con Carlos nel repository `~/mobilitas-agenti-ai`, nella cartella `agente-reel-grafiche`. Questa
cartella (la 03) resta quella su cui lavori; il repository condiviso riceve una copia pulita.

1. **Fai il commit della 03 in Fork.** Lo script copia solo quello che è nel commit: se ci sono modifiche non salvate si
   ferma e te lo dice.
2. **Apri il Terminale in questa cartella e scrivi:**

   ```bash
   ./esporta-nel-repository.sh
   ```

   Copia i file dell'ultimo commit in `~/mobilitas-agenti-ai/agente-reel-grafiche`, al posto di quelli che c'erano: i file
   che hai tolto qui spariscono anche lì. Niente video, niente reel, niente di quello che resta solo sul tuo Mac. Le altre
   cartelle del repository non vengono toccate. Alla fine ti dice quanti file ha copiato, quanto pesano e che non ci sono
   video.
3. **Apri `mobilitas-agenti-ai` in Fork: Pull, Stage, Commit, Push.** Lo script non pubblica niente da solo.

Per vedere cosa verrebbe copiato senza toccare il repository condiviso: `./esporta-nel-repository.sh --prova` (la copia di
prova finisce in `.lavoro/esporta/`).

Cosa contiene questa versione: `VERSIONE.md`. Come lavora l'agente: `CLAUDE.md`.

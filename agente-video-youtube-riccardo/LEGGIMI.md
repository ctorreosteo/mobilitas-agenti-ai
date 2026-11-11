# Agente video YouTube

Monta i video di @Studio_Mobilitas: dal file della camera a un video pronto da
pubblicare. Toglie le papere, muove le inquadrature, mette la grafica, i suoni e
i sottotitoli. Prima del video finale ti fa vedere un'anteprima e aspetta il tuo
ok.

## Come si usa, in 5 passi

**1. Installa (una volta sola).** Apri il Terminale e scrivi:

```bash
cd ~/mobilitas-agenti-ai/agente-video-youtube-riccardo
./installa.sh
```

Ti chiede il permesso prima di installare ogni cosa. Dettagli e requisiti in
`INSTALLAZIONE.md`.

**Avevi già la versione 1.0?** Fino alla 1.0.1 la cartella si chiamava
`agente-video-youtube`. Dopo l'aggiornamento rilancia `./installa.sh` nella
cartella nuova: ti chiede se spostare B-roll, inbox e video dalla vecchia.

**2. Prepara la cartella del video.** In `inbox/` crea una cartella con il nome
del video, per esempio `inbox/YT_POSTURA_33/`, e mettici dentro:

- il **girato**, così come esce dalla camera;
- lo **script**, il testo del video (`.txt` o `.md`);
- un file **`info.txt`** con due righe:

  ```
  osteopata: Nome Cognome
  tipo: YouTube
  ```

  (oppure `tipo: mid-roll`);
- se servono, i **materiali** in `materiali/` (per esempio le schermate dell'app).

Le regole sono in `inbox/LEGGIMI.md`.

**3. Chiedi all'agente.** Apri Claude Code **in questa cartella**
(`agente-video-youtube-riccardo`) e scrivi:

> Edita il video YT_POSTURA_33

Se manca qualcosa te lo chiede. Il lavoro dura qualche ora: lascia il Mac acceso
e collegato alla corrente. Se si interrompe, riscrivi la stessa frase e l'agente
riparte da dove era arrivato.

**4. Guarda l'anteprima e dai l'ok.** L'agente si ferma e ti indica:

- `videos/YT_POSTURA_33/renders/YT_POSTURA_33_anteprima.mp4`, l'anteprima
  piccola (960x540);
- `videos/YT_POSTURA_33/controlli/anteprima-momenti.md`, l'elenco di cosa
  succede e quando, con i punti da decidere.

Rispondi «ok» oppure scrivi cosa cambiare («a 1:20 la scritta è sbagliata»).

**5. Prendi il video.** Dopo l'ok l'agente fa il video finale e lo mette in
`videos/YT_POSTURA_33/consegna/`:

- il **video** e i **sottotitoli** (`.srt`);
- per YouTube anche **`youtube.txt`**, con titoli e descrizione;
- **`validazione-animazioni.md`**: **falla firmare a un osteopata prima di
  pubblicare**.

L'agente non pubblica niente: il caricamento su YouTube lo fai tu.

## Da sapere

- **Musica**: solo se metti brani con licenza in `libreria/musica/` (per esempio
  dalla YouTube Audio Library). Senza, il video esce con voce ed effetti sonori.
- **B-roll**: metti le tue riprese in `libreria/broll/<tema>/`; l'agente le
  cataloga da solo. Regole in `libreria/broll/LEGGIMI.md`.
- **Foto prima e dopo**: solo con il consenso scritto del paziente, segnato in
  `libreria/catalogo.md`. Regole in `libreria/prima-dopo/LEGGIMI.md`.
- **Spazio**: servono circa 150 GB liberi per un video YouTube lungo, 60 GB per
  un mid-roll. A lavoro finito l'agente libera lo spazio da solo.
- I girati, i video e le foto restano sul tuo Mac: non vanno nel repository e
  non escono su internet.

Cosa contiene questa versione: `VERSIONE.md`. Come lavora l'agente: `CLAUDE.md`.

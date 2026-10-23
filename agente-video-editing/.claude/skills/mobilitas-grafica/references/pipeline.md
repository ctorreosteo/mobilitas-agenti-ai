# Dalla regia al master, comando per comando

Da dentro `agente-video-editing/`, con `regia.json` già scritto e `./mve audio <slug>` fatto:

```bash
./mve grafica   <slug>     # piano: sottotitoli, card, titoli, enfasi (secondi)
./mve inquadra  <slug>     # tagli di camera + lato delle card sul volto (secondi)
./mve monta     <slug>     # montato pulito dal 4K, a pezzi (6-10 min; poi cache)
./mve sagome    <slug>     # sagome per i titoli dietro (15 s)
./mve anteprima <slug>     # GUARDA controlli/anteprima.jpg prima di andare avanti
./mve suono     <slug>     # sound design + mix (20 s)
./mve finale    <slug> --limite 40   # prova: solo i primi 40 s
./mve finale    <slug>     # master (10-15 min)
./mve qc        <slug>     # deve dire CONSEGNABILE
./mve shorts    <slug>     # 1-2 min per short
./mve miniature <slug>
./mve consegna  <slug>
```

`./mve anteprima <slug> 12.5 170.3` compone solo quei tempi (secondi del montato).

## Cosa rifare quando cambia qualcosa

| cambia | rifai |
|---|---|
| un taglio in regia | `edl`, `audio`, poi tutto il resto (i pezzi video uguali restano in cache) |
| una card, un'enfasi, un capitolo | `grafica`, `inquadra`, `monta` (solo i pezzi cambiati), `sagome`, `anteprima`, `suono`, `finale` |
| solo il testo di una card o una correzione | `grafica`, `inquadra`, `anteprima`, `finale` |
| un'inquadratura sola | `monta --solo N`, `finale` |
| uno short | `shorts --solo N` |

`./mve stato <slug>` lo calcola guardando le date dei file.

## Il collo di bottiglia

Il renderer disegna un RGBA 1920x1080 per frame (8,3 MB) e lo scrive su stdout. Regge perché:

- gli sprite (card, stacchi, lockup, closing) si disegnano una volta;
- le bande di sottotitolo si disegnano una volta per parola attiva e restano in cache;
- la dissolvenza si fa con una LUT sul canale alfa, non ridisegnando;
- i titoli dietro sono l'unico punto costoso (maschera numpy a tutto schermo): pochi secondi in tutto.

Il generatore muore con `BrokenPipeError` quando ffmpeg chiude la pipe (con `--limite`): è normale.

## Errori già visti

- **Card sul viso.** Nella v1 il lato si stimava dall'occupazione dei pixel; ora si misura sul volto nel taglio d'uscita. Il riquadro della testa si allarga in proporzione al volto **mediano**, non all'unione dei campioni (che è larga perché lei si muove): con l'unione sei card su otto risultavano "sulla testa" senza esserlo.
- **Eyebrow tagliato nel lockup.** Il lockup non può superare la fascia libera: se l'eyebrow non entra si stringe la spaziatura, poi il corpo.
- **Ancoraggio che non si trova.** Il confronto ignora accenti e punteggiatura e tratta cifre e lettere come uguali ("otto" = "8"). Se manca ancora, whisper l'ha scritta diversa: cercala in `parole-montato.json`.
- **Sottotitolo che resta sotto il titolo.** Un gruppo iniziato prima del titolo restava a schermo: ora il renderer spegne i sottotitoli per tutta la finestra del titolo.
- **Titoli dietro illeggibili.** All'altezza del volto la testa mangia il centro delle parole: la posizione si cerca sulla sagoma, sulla parola peggiore.

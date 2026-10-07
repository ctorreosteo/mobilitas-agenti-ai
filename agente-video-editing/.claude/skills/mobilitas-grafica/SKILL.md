---
name: mobilitas-grafica
description: Come si costruiscono i sottotitoli karaoke e le infografiche impresse nei video @Studio_Mobilitas — pianificazione sul montato, renderer Pillow che scrive RGBA nella pipe di ffmpeg, ancoraggio delle card alle frasi. Usala quando un video deve uscire con sottotitoli o card a schermo.
---

# mobilitas-grafica

I video del canale escono con **sottotitoli impressi** (karaoke, parola attiva
in menta) e un pacchetto di infografiche: card dato, stacchi di capitolo,
lockup d'apertura, chip identita, closing, barra di avanzamento.
Lo stile lo detta `mobilitas-style`; qui c'e come si produce.

## Perche non un compositore headless

Questo `ffmpeg` non ha **ne `libass` ne `drawtext`**: il testo va comunque
rasterizzato fuori. Un compositore a browser su 24.000 frame sarebbe lento e
dipenderebbe dalla rete (GSAP da CDN al momento del render). Il livello grafico
si genera quindi con Pillow e va **dritto nella pipe di ffmpeg** come RGBA
grezzo, senza file intermedi e senza dipendenze esterne.

```
ffmpeg -i base.mp4 -f rawvideo -pix_fmt rgba -s 1920x1080 -r 30000/1001 -i - \
       -filter_complex "[0:v][1:v]overlay=shortest=1[v]" ...
```

Serve un venv nel progetto: `python3 -m venv .venv && .venv/bin/pip install pillow numpy fonttools brotli`
(il Python di sistema e protetto da PEP 668).

## Le tre fasi

1. **Trascrivi il montato, non la sorgente.** `whisper-cli -mc 0 -dtw large.v3 -ml 1 -sow`
   sull'audio gia tagliato: i tempi escono direttamente in tempo montato e non
   serve rimappare niente attraverso l'EDL. Rimappare a posteriori funziona ma
   sbaglia sulle giunte, perche l'allineamento si smargina nelle pause.
2. **Pianifica** con `scripts/build_overlay.py` -> `data/overlay.json`:
   gruppi di sottotitolo, card, stacchi, apertura, chiusura.
3. **Renderizza** con `scripts/render_overlay.py`, che espone una classe `Scene`
   con `frame(t)`: la stessa usata sia dallo stream sia dall'anteprima.

## Sottotitoli

Gruppi da 2-3 parole, chiusi da: punteggiatura di fine frase, pausa oltre
0,45 s, o 2,4 s di durata. Vengono circa 55 gruppi al minuto.

La parola attiva e in menta con una barretta menta sotto. **Ogni banda viene
disegnata una volta per parola attiva e tenuta in cache**: da un frame all'altro
cambia solo quale variante si incolla, quindi il costo per frame e una `paste`.
Senza cache il render non sta in piedi.

Correzioni di trascrizione: si correggono **solo i sottotitoli**, l'audio non si
tocca. La lista sta in `FIXES` dentro `build_overlay.py` (refusi ricorrenti:
"all'escrivania" -> "alla scrivania", "gambia" -> "gabbia", "calopo meridiano" ->
"calo pomeridiano", "cosse" -> "coste").

Oltre all'impresso si consegna sempre anche un **SRT a corredo**, che YouTube usa
come traccia sottotitoli.

## Card dato

Si **ancorano alla frase**, non a un tempo scritto a mano: `build_overlay.py`
cerca la sequenza di parole nella trascrizione e piazza la card 0,25 s prima.
Cosi restano sincronizzate se il montaggio cambia. Se un ancoraggio non si
trova lo script lo stampa: va corretto, non ignorato.

Normalizza gli accenti prima di confrontare (`caffè` vs `caffe`), altrimenti gli
ancoraggi falliscono in silenzio.

Contenuto: eyebrow mono, numero grande in menta, unita in paper, glossa in
muted. Il numero viene dalle sue parole ("il 20% dell'ossigeno", "3 o 4
centimetri", "ridotta di meta").

**Il lato si misura, non si assume**: `scripts/place_cards.py` campiona i frame
nella finestra della card e sceglie fra fascia sinistra e destra quella piu
libera. Nei primi secondi il soggetto si sporge e sporca la fascia alta: quella
finestra va sempre verificata a parte.

## Stacchi di capitolo

Scheda piena navy, 1,75 s, che entra 1,3 s **prima** della frase che annuncia:
cade sulla pausa, poi si alza mentre lei dice la battuta. Uno ogni 2-3 minuti,
mai di piu. Il titolo sono le sue parole ("MECCANICO, NON METABOLICO",
"NON RISOLVE, MASCHERA").

## Verifica

`scripts/preview_overlay.py` compone il livello sopra i frame veri e monta un
contact sheet. Guardalo **prima** di lanciare il render lungo: gli errori di
posizione (una card sul viso, un sottotitolo che esce dal safe) si vedono solo li.

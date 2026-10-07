# Pipeline grafica, comando per comando

Dal montato pulito al video con sottotitoli e infografiche impressi.

```bash
cd videos/<slug>

# 1. audio del montato, normalizzato per il riconoscimento
#    (assemblato dall'EDL con acrossfade, come il video)
ffmpeg -i assets/audio-16k-mono.wav -/filter_complex data/afilter.txt \
       -map '[aout]' -ar 16000 -ac 1 -c:a pcm_s16le -y assets/audio-cut-asr.wav

# 2. trascrizione parola per parola, gia in tempo montato
whisper-cli -m ~/.cache/hyperframes/whisper/models/ggml-large-v3.bin \
  -f assets/audio-cut-asr.wav -l it -t 8 -mc 0 -dtw large.v3 -ml 1 -sow -np \
  -oj -ojf -of data/words-cut

# 3. piano: gruppi di sottotitolo, card, stacchi
.venv/bin/python scripts/build_overlay.py

# 4. lato delle card, misurato sui frame veri
.venv/bin/python scripts/place_cards.py

# 5. anteprima: GUARDALA prima del render lungo
.venv/bin/python scripts/preview_overlay.py renders/<slug>_cut_clean.mp4 \
  1.6 36.5 174.0 296.0 461.5 817.0

# 6. render finale (livello grafico in pipe)
PRESET=slow CRF=18 .venv/bin/python scripts/build_master.py \
  renders/<slug>_FINAL_1080p.mp4 --overlay

# 7. a corredo
.venv/bin/python scripts/build_subs.py       # SRT
.venv/bin/python scripts/build_chapters.py   # capitoli YouTube
```

## Il collo di bottiglia

Il renderer disegna un RGBA 1920x1080 per frame e lo scrive su stdout: sono
circa 8,3 MB a frame, 200 GB in tutto su 24.500 frame. Non tocca il disco, va
in pipe, e regge perche:

- gli sprite (card, stacchi, lockup, closing) si disegnano **una volta sola**;
- le bande di sottotitolo si disegnano una volta **per parola attiva** e restano
  in cache: fra un frame e l'altro cambia solo quale variante si incolla;
- la dissolvenza si fa con una LUT sul canale alfa dello sprite, non ridisegnando.

Senza la cache delle bande il render non finisce in tempi utili.

## Prova rapida

`LIMIT_T=42` fa uscire solo i primi 42 secondi: serve a verificare il grafo dei
filtri e l'allineamento senza aspettare il render intero. Il generatore muore
con `BrokenPipeError` quando ffmpeg chiude la pipe — e normale, non un errore.

## Errori gia visti

- **La card finisce sul viso.** Il lato si misura, non si assume; e va misurato
  nella finestra della card, perche nei primi secondi il soggetto si sporge.
- **Il lockup e piu largo della fascia libera.** Il testo va mandato a capo
  dentro `CARD_BOX[2]`, non lasciato scorrere.
- **Ancoraggio che non si trova.** Normalizza gli accenti prima di confrontare
  (`caffè` -> `caffe`), e usa una sequenza abbastanza specifica: `"il calo delle
  tre"` compare quattro volte, `"meccanico non"` una sola.
- **`overlay=shortest=1` taglia la coda.** La durata del piano deve essere quella
  del montato (somma dei segmenti meno le dissolvenze), non quella dell'ultima
  parola trascritta.

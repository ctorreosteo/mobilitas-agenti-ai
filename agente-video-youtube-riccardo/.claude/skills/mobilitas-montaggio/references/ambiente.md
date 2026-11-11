# Ambiente: cosa c'e e cosa manca su questa macchina

## ffmpeg

Build Homebrew 9.0.2 (installata il 26/10/2026 in laboratorio). **Manca**:

- `zscale` (niente libzimg) e `libplacebo` -> l'HLG non si linearizza con i
  filtri; serve il LUT 3D precalcolato
- `libass`, `freetype`, `fontconfig` -> **niente `subtitles`, `ass`, `drawtext`**:
  il testo va rasterizzato fuori e composto con `overlay`
- `-filter_complex_script` e stato rimosso: si usa `-/filter_complex file`

C'e invece: `lut3d`, `overlay`, `xfade`, `acrossfade`, `silencedetect`,
`loudnorm`, `ebur128`, `afftdn`, `deesser`, `alimiter`, `adeclip`, videotoolbox.

## Trascrizione

`whisper-cli` (whisper.cpp) da Homebrew. Modello `ggml-large-v3.bin` (3,1 GB), cercato
in quest'ordine (v1.0, 02/11/2026): la variabile `MVE_WHISPER_MODEL`, `.modelli/` nella
cartella dell'agente (dove lo mette `installa.sh`), `~/.cache/hyperframes/whisper/models/`
(dove sta in laboratorio).

Flag che contano:

- `-mc 0` — niente riporto di contesto fra finestre. **Senza, degenera in loop**
  e puo lasciare meta file non trascritto.
- `-dtw large.v3` — timestamp per parola allineati, molto meglio della stima
  di default (che comunque si smargina dentro le pause lunghe)
- `-ml 1 -sow` — un segmento per parola
- `-oj -ojf` — JSON con i token

## Python

Il Python di sistema e protetto da PEP 668: `pip install` fallisce. C'e un solo
venv, nella cartella dell'agente, condiviso da tutti i video (`./mve` lo usa da solo):

```bash
python3 -m venv .venv
.venv/bin/pip install -r motore/requirements.txt
```

## Swift e Apple Vision

`swiftc` (Xcode Command Line Tools) compila `motore/swift/visione.swift` in
`.cache/visione` al primo uso, e lo ricompila se il sorgente cambia. Vision legge
direttamente l'HEVC HLG della camera e applica la rotazione. Volti: ~50 frame/s;
sagome della persona (qualita `accurate`): ~25 frame/s.

`numpy` serve all'analisi dell'inviluppo, `pillow` al renderer grafico,
`fonttools` a controllare la copertura dei font.

## Spazio disco

Un video da 20 minuti occupa circa 15 GB fra sorgente (9 GB, collegata e non
copiata), pezzi del montato (`renders/pezzi/`, 2,7 GB), montato pulito (2,7 GB)
e consegne. A lavoro chiuso `renders/pezzi/` si puo cancellare: si rigenera con
`./mve monta`. Non serve piu l'intermedio 1080p della v1: si lavora dal 4K.

Il lavoro di una scena (`.lavoro/scena/`) è molto più grande: fotogrammi PNG del
piatto, sagome e strati di ogni momento. Misurato: **103 GB** per YT_POSTURA_32
(6:50 finiti, 13 min di girato), **48 GB** per MR_POSTURA_01_v4 (1:52, con prove e
regressione). Regola pratica: circa 15 GB per minuto di video finito, più 20 GB.
Si svuota a consegna fatta (foto dei pazienti per prime). Ogni fase scrive in
`videos/<slug>/tempi.md` quanto è durata e quanto spazio occupano cartella del
video e `.lavoro` in quel momento.

## RAM e lavori in parallelo (v1.0, 02/11/2026)

Misurato su M3 Max 36 GB: whisper large-v3 **3,9 GB** per istanza (la trascrizione ne
lancia 3 insieme), un render HyperFrames con la composizione della scena **3,3 GB**.
`progetto.lavori(n)` riduce i lavori pesanti in parallelo secondo la RAM: da 32 GB in
su n, da 16 a 31 GB la metà (arrotondata in su), sotto i 16 GB uno alla volta.
`MVE_LAVORI=1 ./mve <fase> <slug>` lo forza (per esempio se il Mac rallenta o
whisper cade). `./mve stato` senza slug mostra RAM, lavori, disco e strumenti.

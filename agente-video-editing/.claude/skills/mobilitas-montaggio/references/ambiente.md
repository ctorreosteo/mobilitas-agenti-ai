# Ambiente: cosa c'e e cosa manca su questa macchina

## ffmpeg

Build Homebrew 9.0.1. **Manca**:

- `zscale` (niente libzimg) e `libplacebo` -> l'HLG non si linearizza con i
  filtri; serve il LUT 3D precalcolato
- `libass`, `freetype`, `fontconfig` -> **niente `subtitles`, `ass`, `drawtext`**:
  il testo va rasterizzato fuori e composto con `overlay`
- `-filter_complex_script` e stato rimosso: si usa `-/filter_complex file`

C'e invece: `lut3d`, `overlay`, `xfade`, `acrossfade`, `silencedetect`,
`loudnorm`, `ebur128`, `afftdn`, `deesser`, `alimiter`, videotoolbox.

## Trascrizione

`whisper-cli` (whisper.cpp) da Homebrew. Modello:
`~/.cache/hyperframes/whisper/models/ggml-large-v3.bin`.

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

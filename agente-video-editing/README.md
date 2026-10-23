# Agente video editing

Dal file della camera al video pubblicabile: montato senza papere, con inquadrature dinamiche dal 4K, titoli che passano dietro la presentatrice, card, sottotitoli, sound design; più Shorts verticali, miniature e pacchetto YouTube.

## Come si usa

1. Copia il girato in `inbox/` (es. `inbox/YT_TOFU_03.MOV`).
2. Apri Claude Code **in questa cartella** (`agente-video-editing/`), non in quella sopra: comandi, skill e revisori si caricano solo da qui.
3. Scrivi `/monta inbox/YT_TOFU_03.MOV`.

L'agente lavora da solo e ti riporta dove sono i file e cosa ha deciso. Ti chiede qualcosa solo se nel girato compaiono volti di altre persone.

| comando | quando |
|---|---|
| `/monta <file>` | un video nuovo |
| `/correggi <slug> <cosa e dove>` | hai visto un difetto: "a 4:32 una parola è tagliata" |
| `/rivedi <slug>` | vuoi una revisione completa con i tre revisori |
| `/shorts <slug>` | vuoi rifare o aggiungere Shorts |

## Cosa trovi alla fine, in `videos/<slug>/`

| file | cosa |
|---|---|
| `renders/<slug>_FINALE.mp4` | **il video da pubblicare** (1080p, −14 LUFS) |
| `shorts/<slug>_short1.mp4` … | Shorts e Reels 9:16 |
| `miniature/miniatura-1.jpg` … | tre miniature 1280x720 |
| `consegna/youtube.md` | titoli proposti, descrizione con capitoli, tag |
| `consegna/<slug>.srt` | sottotitoli da caricare su YouTube |
| `BRIEF.md` | cosa è stato tagliato e perché, decisioni, proposte che aspettano te |
| `controlli/QC.md` | i controlli automatici sul file consegnato |

**Musica**: per avere un sottofondo metti un brano con licenza in `videos/<slug>/assets/musica/` e chiedi di rifare il suono. Senza, il video esce con voce e sound design.

## Come è fatto

- `CLAUDE.md`: l'agente (fasi, cancelli, politiche)
- `mve` + `motore/`: il motore, un comando per fase (`./mve -h`)
- `.claude/skills/`: il sapere (regia, montaggio, grafica, stile)
- `.claude/agents/`: i revisori (cacciatore di papere, regista, revisore visivo)
- `videos/<slug>/regia.json`: le decisioni del singolo video, l'unico file che l'agente scrive a mano

Prima installazione (una volta): `python3 -m venv .venv && .venv/bin/pip install -r motore/requirements.txt`. Servono anche `ffmpeg`, `whisper-cli` (Homebrew) e gli strumenti da riga di comando di Xcode (`swiftc`).

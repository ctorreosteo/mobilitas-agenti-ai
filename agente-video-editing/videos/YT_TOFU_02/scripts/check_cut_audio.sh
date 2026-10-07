#!/bin/zsh
# Ritrascrive 14s attorno a ogni giunta del montato: verifica che ogni cucitura
# si richiuda in una frase intera.
W=${2:-/private/tmp/claude-501/-Users-carlitos-video-editing/7aa8e8d2-1fb8-440b-945d-2cd2fdeab552/scratchpad/cutcheck.wav}
S=/private/tmp/claude-501/-Users-carlitos-video-editing/7aa8e8d2-1fb8-440b-945d-2cd2fdeab552/scratchpad
M=/Users/carlitos/.cache/hyperframes/whisper/models/ggml-large-v3.bin
while read -r t label; do
  a=$(python3 -c "print(max(0,$t-7))")
  printf '%8.1f  %-56s : ' $t "$label"
  ffmpeg -hide_banner -loglevel error -ss $a -t 14 -i $W -c copy -y $S/cc.wav
  whisper-cli -m $M -f $S/cc.wav -l it -t 6 -mc 0 -np 2>/dev/null | sed 's/^\[[^]]*\]//' | tr -d '\n' | sed 's/  */ /g'
  echo
done

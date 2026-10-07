#!/bin/zsh
S=/private/tmp/claude-501/-Users-carlitos-video-editing/7aa8e8d2-1fb8-440b-945d-2cd2fdeab552/scratchpad
M=/Users/carlitos/.cache/hyperframes/whisper/models/ggml-large-v3.bin
V=renders/YT_TOFU_02_master_1080p.mp4
for t in "$@"; do
  a=$((t-7)); [ $a -lt 0 ] && a=0
  echo "----- montato ${t}s -----"
  ffmpeg -hide_banner -loglevel error -ss $a -t 14 -i $V -vn -ac 1 -ar 16000 -c:a pcm_s16le -y $S/mw.wav
  whisper-cli -m $M -f $S/mw.wav -l it -t 6 -mc 0 -np 2>/dev/null | sed 's/^\[[^]]*\]//' | tr -d '\n'
  echo
done

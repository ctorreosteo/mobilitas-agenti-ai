#!/bin/zsh
S=/private/tmp/claude-501/-Users-carlitos-video-editing/7aa8e8d2-1fb8-440b-945d-2cd2fdeab552/scratchpad
M=/Users/carlitos/.cache/hyperframes/whisper/models/ggml-large-v3.bin
for w in "$@"; do
  a=${w%%-*}; b=${w##*-}; d=$((b-a))
  echo "########## finestra ${a}s - ${b}s ##########"
  ffmpeg -hide_banner -loglevel error -ss $a -t $d -i assets/audio-16k-asr.wav -c copy -y $S/win.wav
  whisper-cli -m $M -f $S/win.wav -l it -t 6 -mc 0 -dtw large.v3 -ml 1 -sow -np 2>/dev/null \
    | python3 -c "
import sys,re
off=float('$a')
for l in sys.stdin:
    m=re.match(r'\[(\d+):(\d+):([\d.]+) --> (\d+):(\d+):([\d.]+)\]\s+(.*)',l.strip())
    if not m: continue
    s=int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3))
    e=int(m.group(4))*3600+int(m.group(5))*60+float(m.group(6))
    print(f'{s+off:8.2f} {e+off:8.2f}  {m.group(7)}')
"
done

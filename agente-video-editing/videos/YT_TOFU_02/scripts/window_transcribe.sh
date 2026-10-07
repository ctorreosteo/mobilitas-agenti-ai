#!/bin/zsh
# Trascrive la sorgente a finestre corte sovrapposte.
# Serve perche whisper, su un file intero, APPIANA le riprese doppie: riscrive
# una frase corretta al posto della papera. A finestra corta non puo farlo.
S=/private/tmp/claude-501/-Users-carlitos-video-editing/7aa8e8d2-1fb8-440b-945d-2cd2fdeab552/scratchpad/win
M=/Users/carlitos/.cache/hyperframes/whisper/models/ggml-large-v3.bin
WAV=assets/audio-16k-asr.wav
WIN=26; STEP=20; DUR=1185
mkdir -p $S
for ((a=0; a<DUR; a+=STEP)); do
  out=$S/w$(printf '%05d' $a).txt
  [ -s "$out" ] && continue
  ffmpeg -hide_banner -loglevel error -ss $a -t $WIN -i $WAV -c copy -y $S/cur.wav
  whisper-cli -m $M -f $S/cur.wav -l it -t 6 -mc 0 -dtw large.v3 -ml 1 -sow -np 2>/dev/null \
    | python3 -c "
import sys,re
off=float('$a')
for l in sys.stdin:
    m=re.match(r'\[(\d+):(\d+):([\d.]+) --> (\d+):(\d+):([\d.]+)\]\s+(.*)',l.strip())
    if not m: continue
    s=int(m.group(1))*3600+int(m.group(2))*60+float(m.group(3))
    e=int(m.group(4))*3600+int(m.group(5))*60+float(m.group(6))
    print(f'{s+off:.2f}\t{e+off:.2f}\t{m.group(7)}')
" > $out
  echo "finestra $a ok"
done
echo TUTTE_FATTE

#!/bin/zsh
# Trascrive separatamente i 9s prima e i 9s dopo una pausa.
# Due clip distinte: whisper non puo appianare la papera riscrivendo la frase,
# perche non vede mai le due riprese insieme.
S=/private/tmp/claude-501/-Users-carlitos-video-editing/7aa8e8d2-1fb8-440b-945d-2cd2fdeab552/scratchpad/gap
M=/Users/carlitos/.cache/hyperframes/whisper/models/ggml-large-v3.bin
mkdir -p $S
one() {  # $1=start $2=dur $3=tag
  ffmpeg -hide_banner -loglevel error -ss $1 -t $2 -i assets/audio-16k-asr.wav -c copy -y $S/$3.wav
  whisper-cli -m $M -f $S/$3.wav -l it -t 6 -mc 0 -np 2>/dev/null | sed 's/^\[[^]]*\]//' | tr -d '\n' | sed 's/  */ /g'
}
while read -r a z; do
  pre=$(python3 -c "print(max(0,$a-9))")
  echo "########## PAUSA ${a}s -> ${z}s ##########"
  printf 'PRIMA: '; one $pre 9 pre; echo
  printf 'DOPO : '; one $z 9 post; echo
done

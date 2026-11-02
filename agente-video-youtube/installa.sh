#!/bin/zsh
# installa.sh — prepara un Mac con chip Apple per l'agente video YouTube (v1.0.1).
#
# Controlla cosa c'è già e installa il resto SOLO dopo una conferma per ogni pezzo:
# Strumenti da riga di comando di Xcode, Homebrew, ffmpeg, whisper.cpp con il modello
# large-v3, Python 3.12 con il venv, Node e HyperFrames 0.8.204, il browser di render.
# Alla fine fa una prova di 30 secondi. Si può rilanciare quante volte si vuole:
# quello che c'è già non si tocca.
#
# Uso: apri il Terminale nella cartella dell'agente e scrivi  ./installa.sh
#      ./installa.sh --prova   rifà solo la prova finale, senza controllare né installare

set -u
DIR=${0:A:h}
cd "$DIR" || exit 1

HF_ENV=(DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 HYPERFRAMES_SKIP_SKILLS=1
        HYPERFRAMES_EXTRACT_CACHE_DIR=off HOME="$DIR/motore/inserti/.casa"
        XDG_CACHE_HOME="$DIR/motore/inserti/.casa/.cache" TMPDIR="$DIR/motore/inserti/.casa/tmp")
HF="$DIR/motore/inserti/node_modules/.bin/hyperframes"
hf() { env "${HF_ENV[@]}" "$HF" "$@"; }   # HyperFrames sempre con privacy e casa dentro la cartella
MODELLO="$DIR/.modelli/ggml-large-v3.bin"
MODELLO_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3.bin"
MODELLO_BYTE=3095033483
PROVA="$DIR/.lavoro/prova-installazione"

ok()    { print -P "  %F{green}✓%f $1"; }
manca() { print -P "  %F{yellow}✗%f $1"; }
errore(){ print -P "%F{red}!!! $1%f"; }
chiedi(){ local r; read "r?  → $1 [s/N] "; [[ $r == [sSyY]* ]]; }
titolo(){ print; print -P "%B$1%b"; }

# il modello whisper: dove lo cerca anche il motore (motore/motore/progetto.py)
trova_modello() {
  local p
  for p in "${MVE_WHISPER_MODEL:-}" "$MODELLO" "$HOME/.cache/hyperframes/whisper/models/ggml-large-v3.bin"; do
    [[ -n $p && -f $p ]] && { print -r -- "$p"; return 0; }
  done
  return 1
}

# Homebrew nel PATH anche se il profilo del Terminale non lo carica
[[ -x /opt/homebrew/bin/brew ]] && eval "$(/opt/homebrew/bin/brew shellenv)"

# ================================================================ controllo e installazione
installa() {
titolo "Agente video YouTube v1.0.1: controllo del Mac"
if [[ $(uname -s) != Darwin || $(uname -m) != arm64 ]]; then
  errore "serve un Mac con chip Apple (M1, M2, M3, M4, M5...)"; exit 1
fi
local RAM=$(( $(sysctl -n hw.memsize) / 1073741824 ))
local LIBERO=$(df -g "$DIR" | awk 'NR==2 {print $4}')
print "  $(sysctl -n machdep.cpu.brand_string), RAM $RAM GB, macOS $(sw_vers -productVersion), disco libero $LIBERO GB"
if (( RAM < 16 )); then
  manca "RAM sotto i 16 GB: l'agente funziona, ma fa un lavoro alla volta ed è più lento"
else
  ok "RAM sufficiente (sotto i 32 GB il motore fa da solo meno lavori in parallelo)"
fi
if (( LIBERO < 150 )); then
  manca "disco: $LIBERO GB liberi. Servono circa 15 GB per minuto di video finito + 20 GB (150 GB per un video YouTube lungo, 60 per un mid-roll)"
else
  ok "disco: $LIBERO GB liberi"
fi

# ---------------------------------------------------------------- Xcode
titolo "1. Strumenti da riga di comando di Xcode (swiftc, per Apple Vision)"
if xcode-select -p >/dev/null 2>&1 && command -v swiftc >/dev/null; then
  ok "presenti"
else
  manca "mancano"
  if chiedi "installarli? (si apre una finestra di macOS: segui le istruzioni, poi rilancia ./installa.sh)"; then
    xcode-select --install; exit 0
  fi
fi

# ---------------------------------------------------------------- Homebrew
titolo "2. Homebrew"
if command -v brew >/dev/null; then
  ok "presente ($(brew --version | head -1))"
else
  manca "manca"
  if chiedi "installare Homebrew (script ufficiale da brew.sh, chiede la password del Mac)?"; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || { errore "Homebrew non installato"; exit 1; }
    eval "$(/opt/homebrew/bin/brew shellenv)"
  else
    errore "senza Homebrew non si può andare avanti"; exit 1
  fi
fi

# ---------------------------------------------------------------- pacchetti
titolo "3. ffmpeg, whisper.cpp, Python 3.12, Node"
pacchetto() {   # $1 comando, $2 pacchetto brew, $3 descrizione
  if command -v "$1" >/dev/null; then ok "$3: $(command -v $1)"
  else
    manca "$3"
    chiedi "installare $2 con Homebrew?" && brew install "$2"
  fi
}
pacchetto ffmpeg ffmpeg "ffmpeg"
pacchetto whisper-cli whisper-cpp "whisper.cpp (whisper-cli)"
pacchetto python3.12 python@3.12 "Python 3.12"
if command -v node >/dev/null && (( ${$(node -v | tr -d v)%%.*} >= 22 )); then
  ok "Node $(node -v)"
else
  manca "Node 22 o più recente"
  chiedi "installare node con Homebrew?" && brew install node
fi

# ---------------------------------------------------------------- Python
titolo "4. Ambiente Python del motore (.venv)"
if [[ -x .venv/bin/python ]] && .venv/bin/python -c "import PIL, numpy, fontTools" 2>/dev/null; then
  ok "pronto ($(.venv/bin/python --version))"
else
  manca "manca"
  if chiedi "creare .venv e installare pillow, numpy, fonttools, brotli (versioni fissate)?"; then
    python3.12 -m venv .venv && .venv/bin/pip install --quiet -r motore/requirements.lock && ok "pronto"
  fi
fi

# ---------------------------------------------------------------- HyperFrames
titolo "5. HyperFrames 0.8.204 (grafiche animate)"
if [[ -x $HF ]] && [[ $(node -p "require('./motore/inserti/node_modules/hyperframes/package.json').version" 2>/dev/null) == 0.8.204 ]]; then
  ok "presente, versione 0.8.204"
else
  manca "manca"
  if chiedi "installarlo con npm (versione fissata da package-lock.json, circa 110 MB)?"; then
    mkdir -p motore/inserti/.casa/.cache motore/inserti/.casa/tmp
    (cd motore/inserti && env "${HF_ENV[@]}" npm ci --no-audit --no-fund --loglevel=error) && ok "installato"
  fi
fi

titolo "6. Browser di render (Chrome senza finestra, per HyperFrames)"
mkdir -p motore/inserti/.casa/.cache motore/inserti/.casa/tmp
if [[ -x $HF ]] && hf browser path >/dev/null 2>&1; then
  ok "presente"
elif [[ -x $HF ]]; then
  manca "manca"
  if chiedi "scaricarlo (circa 200 MB, in motore/inserti/.casa/)?"; then
    hf browser ensure && ok "scaricato"
  fi
else
  manca "prima serve HyperFrames (punto 5)"
fi

# ---------------------------------------------------------------- modello whisper
titolo "7. Modello di trascrizione whisper large-v3 (3,1 GB)"
local TROVATO
if TROVATO=$(trova_modello); then
  ok "presente: $TROVATO"
else
  manca "manca"
  if chiedi "scaricarlo da Hugging Face (ggerganov/whisper.cpp) in .modelli/?"; then
    mkdir -p .modelli
    curl -L --fail -o "$MODELLO.part" "$MODELLO_URL" && mv "$MODELLO.part" "$MODELLO"
    if [[ -f $MODELLO && $(stat -f %z "$MODELLO") == $MODELLO_BYTE ]]; then
      ok "scaricato e controllato ($MODELLO_BYTE byte)"
    else
      errore "il modello non ha la dimensione attesa ($MODELLO_BYTE byte): cancellalo e riprova"
    fi
  fi
fi

titolo "8. Prova di 30 secondi"
if ! chiedi "fare la prova (voce sintetica di 30 s, trascrizione, video, Apple Vision, una grafica HyperFrames)?"; then
  print; ./mve stato 2>/dev/null | tail -25; exit 0
fi
}

# ================================================================ prova di 30 secondi
# Ogni controllo è una funzione: i testi e i percorsi passano come argomenti fra
# virgolette, mai dentro un eval (un apostrofo nella frase o nel nome della
# cartella rompeva le virgolette: corretto nella v1.0.1).
TESTO="Ciao, questa è la prova dell'agente video di Mobilitas. Il bacino è la zona dei fianchi dove la schiena si unisce alle gambe. Oggi proviamo la trascrizione, il montaggio, la grafica e il suono. Se senti questa frase, il computer è pronto per lavorare sui video del canale. Grazie e buon lavoro."

controllo_voce() {
  local -a v=()
  local nome=$(say -v '?' | awk '/it_IT/ {print $1; exit}')   # la prima voce italiana
  [[ -n $nome ]] && v=(-v "$nome")
  say "${v[@]}" -r 150 -o "$PROVA/voce.aiff" "$TESTO" &&
  ffmpeg -v error -y -i "$PROVA/voce.aiff" -af apad=whole_dur=30 -t 30 -ac 1 -ar 16000 "$PROVA/voce.wav" &&
  [[ -s $PROVA/voce.wav ]]
}
controllo_trascrizione() {
  local mod
  mod=$(trova_modello) || { print "modello whisper large-v3 non trovato"; return 1; }
  whisper-cli -m "$mod" -f "$PROVA/voce.wav" -l it -t 4 -np -otxt -of "$PROVA/trascrizione" &&
  grep -qi -e bacino -e prova -e video "$PROVA/trascrizione.txt"
}
controllo_video() {
  ffmpeg -v error -y -f lavfi -i testsrc2=s=1920x1080:r=25:d=30 -i "$PROVA/voce.wav" \
    -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest "$PROVA/prova.mp4" || return 1
  local durata=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$PROVA/prova.mp4")
  print "durata: $durata s"
  (( ${durata%%.*} >= 29 ))
}
controllo_vision() {
  PYTHONPATH=motore .venv/bin/python -c 'from motore.visione import binario; binario()'
}
controllo_grafica() {
  cp motore/inserti/node_modules/hyperframes/dist/vendor/npm/gsap@3.15.0/dist/gsap.min.js "$PROVA/hf/assets/" || return 1
  cat > "$PROVA/hf/index.html" <<'HTML'
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>
      html, body { margin: 0; background: #002552; }
      #root { position: absolute; inset: 0; overflow: hidden; background: #002552; }
      #t { position: absolute; left: 0; right: 0; top: 470px; text-align: center; color: #F4F4F4;
           font: 800 120px sans-serif; opacity: 0; }
    </style>
  </head>
  <body>
    <script src="assets/gsap.min.js"></script>
    <div id="root" data-composition-id="prova" data-start="0" data-duration="2" data-width="1920" data-height="1080">
      <div id="scena" class="clip" data-start="0" data-duration="2"><div id="t">prova</div></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      tl.to('#t', { opacity: 1, duration: 0.8, ease: 'power3.out' });
      window.__timelines['prova'] = tl;
    </script>
  </body>
</html>
HTML
  hf render "$PROVA/hf" --fps 25 --format mov -o "$PROVA/grafica.mov" --quiet &&
  [[ -s $PROVA/grafica.mov ]]
}

RIUSCITE=0
FALLITE=0
prova() {   # $1 nome del controllo, $2 la funzione che lo fa
  if "$2" >"$PROVA/log-$1.txt" 2>&1; then
    ok "$1"; RIUSCITE=$((RIUSCITE+1))
  else
    errore "$1 non riuscita: vedi .lavoro/prova-installazione/log-$1.txt"; FALLITE=$((FALLITE+1))
  fi
}

if [[ ${1:-} == --prova ]]; then
  titolo "Prova di 30 secondi (senza controllare né installare)"
else
  installa
fi
rm -rf "$PROVA"; mkdir -p "$PROVA/hf/assets" motore/inserti/.casa/.cache motore/inserti/.casa/tmp
INIZIO=$SECONDS
prova "voce sintetica" controllo_voce
prova "trascrizione (whisper large-v3)" controllo_trascrizione
prova "video 30 s 1080p25 (ffmpeg)" controllo_video
prova "Apple Vision (swiftc)" controllo_vision
prova "grafica HyperFrames" controllo_grafica
PYTHONPATH=motore .venv/bin/python -c "from motore import inserti; inserti.dimentica()" >/dev/null 2>&1
print "  durata della prova: $(( SECONDS - INIZIO )) s"
if (( FALLITE == 0 )); then
  rm -rf "$PROVA"
  ok "prova riuscita: $RIUSCITE controlli su $((RIUSCITE+FALLITE))"
else
  errore "$RIUSCITE controlli su $((RIUSCITE+FALLITE)) riusciti: i dettagli sono in .lavoro/prova-installazione/"
fi

titolo "Riepilogo (./mve stato)"
./mve stato | sed -n '/strumenti:/,$p'

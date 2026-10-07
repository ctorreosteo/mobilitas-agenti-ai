# Trovare le papere quando il riconoscitore mente

## Il problema

Whisper, su un file lungo, **non trascrive quello che sente: trascrive quello
che ha senso**. Davanti a una ripresa doppia ("...un problema di postura. Devi
iniziare a pensarlo come quello che e davvero, un problema di postura
accumulata...") scrive la frase una volta sola, corretta. La papera sparisce dal
testo e il montaggio la lascia dentro.

Su YT_TOFU_02 e successo almeno tre volte. Una di quelle papere — "in modo
significativo... no, aspetta" a 13:39 — non compare in **nessuna** trascrizione
d'insieme, ne quella intera ne quelle a finestre da 26 s.

Il secondo modo di sbagliare e piu banale: al primo passaggio puo degenerare in
loop e ripetere la stessa frase per centinaia di battute, lasciando il 60% del
file non trascritto. Si evita normalizzando l'audio (`loudnorm=I=-20`) e
passando `-mc 0`.

## Il metodo che funziona

Sondare **le pause**, non il testo. Una ripresa doppia lascia sempre lo stesso
segno strutturale: parlato, silenzio lungo, ripartenza.

```bash
# tutte le pause sopra 1,5 s, dall'inviluppo RMS
.venv/bin/python -c "
import json
b=json.load(open('data/speech-blocks.json'))
for (s1,e1),(s2,_) in zip(b,b[1:]):
    if s2-e1>1.5: print(f'{e1:.2f} {s2:.2f}')
" > /tmp/gaps.txt

./scripts/gap_probe.sh < /tmp/gaps.txt > /tmp/gapreport.txt
```

`gap_probe.sh` trascrive **separatamente** i 9 secondi prima e i 9 dopo ogni
pausa. Due clip distinte: whisper non vede mai le due riprese insieme, quindi
non puo fonderle. Il referto si legge a colpo d'occhio:

```
########## PAUSA 631.75s -> 633.62s ##########
PRIMA:  ...l'escursione e ridotta di meta.
DOPO :  letteralmente meta e la persona non se ne accorge... No, ho sbagliato.
```

Se il "DOPO" ricomincia con le parole del "PRIMA", e una ripresa doppia. Se
contiene "ho sbagliato", "aspetta", "scusami", "torna su", "stoppa", e regia.

## Segnali di supporto

Utili per non perdere niente, ma nessuno basta da solo:

- **blocchi brevi e isolati**: parlato sotto 0,75 s con oltre 1,2 s di silenzio
  da entrambi i lati. E la firma degli a-parte ("ok", "scusami", "no").
- **n-grammi ripetuti** entro 90 s nella trascrizione a finestre corte.
- **token troncati** (`...`) e interiezioni nel testo.

## Attenzione ai buchi nel rilevatore

Una pausa puo non comparire nella lista perche un respiro di 50 ms la spezza in
due. Per la ricerca delle papere ignora i blocchi sotto 0,12 s; per i punti di
taglio invece tienili, o rischi di tagliare dentro un respiro.

## Verifica finale

Non fidarti dell'EDL: ricontrolla il **file consegnato**.

```bash
./scripts/check_cut_audio.sh < data/junctions.txt
```

Ritrascrive 14 s attorno a ogni giunta. Ognuna deve richiudersi in una frase
intera e grammaticale. Se una suona monca o ripetuta, il taglio e sbagliato.

---
name: mobilitas-montaggio
description: Pipeline di montaggio dei video @Studio_Mobilitas — dal .MOV di camera al master 1080p. Copre conversione HLG->BT.709 senza zscale, rilevamento delle papere e delle riprese doppie, EDL, punti di taglio, audio a -14 LUFS e verifica. Usala per qualsiasi montaggio del canale, prima di toccare ffmpeg.
---

# mobilitas-montaggio

Il girato del canale arriva come ripresa unica: la presentatrice si ferma, si
corregge a voce alta ("ho sbagliato", "torna su un pochettino") e rifa la
battuta. Montare vuol dire soprattutto **trovare e togliere quei punti**, e la
parte difficile e trovarli, non tagliarli.

## Ordine di lavoro

1. `ffprobe` sulla sorgente. Attese: 3840x2160 HEVC Main10 a 59.94, HLG BT.2020
   con RPU Dolby Vision, `rotation: -180`, audio AAC registrato **molto basso**
   (intorno a -29 LUFS con picchi gia in clipping).
2. Estrai l'audio: `audio-16k-mono.wav` per l'analisi, `audio-48k.wav` per il
   master, `audio-16k-asr.wav` normalizzato per il riconoscimento.
3. Genera il LUT colore e l'intermedio 1080p (vedi sotto).
4. Trascrivi, sonda le pause, costruisci l'EDL, verifica.
5. Renderizza il master, poi verifica **sul file consegnato**.

## Colore: HLG BT.2020 -> SDR BT.709

`ffmpeg` di Homebrew **non ha `zscale` ne `libplacebo`**, e il filtro
`colorspace` non conosce la curva `arib-std-b67`: con i filtri disponibili l'HLG
non si linearizza. La conversione si precalcola come LUT 3D
(`scripts/make_hlg_lut.py`): inverse-OETF HLG, OOTF con gamma di sistema 1.2,
normalizzazione sul bianco di riferimento HLG 0.75, tone map Hable, matrice
BT.2020 -> BT.709 con desaturazione dei fuori-gamut, OETF BT.1886.

```
-vf "fps=30000/1001,scale=1920:1080:flags=lanczos,format=gbrp16le,
     lut3d=file=assets/hlg2020-to-bt709.cube:interp=tetrahedral,format=yuv420p"
```

**I flag `-color_primaries`/`-color_trc` da soli non bastano**: i frame filtrati
si portano dietro i metadati d'ingresso e il file esce ancora taggato
`arib-std-b67`/`bt2020`. Serve `setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709`
in coda alla catena. Controllalo sempre con `ffprobe` dopo il render.

Il 59.94 si decima 2:1 esatto con `fps=30000/1001`: nessun judder.

## Trovare le papere

**Whisper appiana le riprese doppie.** Su file intero, al posto della papera
scrive una frase corretta che non e mai stata pronunciata: in YT_TOFU_02 lo ha
fatto almeno tre volte, e una di quelle papere non compare in **nessuna**
trascrizione lunga. Non fidarti mai di una trascrizione d'insieme per il
montaggio.

Il metodo che funziona e `scripts/gap_probe.sh`: per ogni pausa sopra 1,5 s
trascrivi **separatamente** i 9 secondi prima e i 9 dopo. Due clip distinte:
whisper non vede mai le due riprese insieme, quindi non puo fonderle. Il
risultato si legge a colpo d'occhio — se il "DOPO" ricomincia con le stesse
parole del "PRIMA", e una ripresa doppia.

Segnali collaterali utili: blocchi di parlato sotto 0,75 s isolati da oltre
1,2 s di silenzio (la firma degli a-parte tipo "ok", "scusami"), n-grammi
ripetuti entro 90 s, parole troncate con `...`.

Altro inciampo: al primo passaggio whisper puo degenerare in loop e lasciare
meta video non trascritto. Si evita normalizzando l'audio prima
(`loudnorm=I=-20`) e passando `-mc 0` per togliere il riporto di contesto.

## Punti di taglio

**Non tagliare sul confine del blocco di parlato.** Il confine cade dove
l'energia scende sotto soglia, ma la coda della sillaba continua a scendere per
altri 100-200 ms restando udibile: tagliare li tronca la parola. E successo, ed
e la prima cosa che l'utente ha sentito.

`scripts/cutpoints.py` cerca invece il primo istante in cui l'energia e tornata
al **fondo di sala** (percentile 12 dell'inviluppo, +10 dB), su una finestra di
5 ms con media mobile a 30 ms perche le occlusive lasciano micro-buchi dentro la
parola.

Dopo aver costruito l'EDL, `build_edl.py` stampa l'energia residua a ogni
giunta: **deve stare sotto -55 dB**. Se una giunta sfora, il punto va spostato.

Le giunte sono dissolvenze di 5 frame, non stacchi: la macchina e fissa e il
soggetto si muove durante le pause, quindi lo stacco secco si legge come uno
scatto. Nessun segmento sotto 1,4 s, o sarebbe quasi tutta dissolvenza.

## Audio

Catena: passa-alto 75 Hz, `afftdn` a -10 dB, de-esser, compressione 2,5:1 a
-20 dB, `loudnorm=I=-14:TP=-1.5:LRA=9`, limiter di sicurezza. La sorgente sta a
-29 LUFS: alzarla di 15 dB alza anche il fondo, per questo la riduzione di
rumore viene **prima** della normalizzazione.

## Verifica (obbligatoria, sul file consegnato)

- `scripts/check_cut_audio.sh` ritrascrive 14 s attorno a ogni giunta: ognuna
  deve richiudersi in una frase intera e grammaticale.
- `scripts/qc_junctions.py` monta i frame a ±0,5 s di ogni giunta in un contact
  sheet: inquadratura, colore ed esposizione devono restare costanti.
- `ffprobe` + `ebur128` sul master: durata, fps, tag colore, LUFS, true peak.

## Politiche di produzione

Decise una volta, non si richiedono a ogni video:

- **piena autonomia sui tagli**;
- asset delle card generati in casa, niente stock a pagamento;
- revisione solo sul video finale;
- `inbox/video_prova2.mov` e un test tecnico, non un formato da pubblicare.

L'unico stop assoluto e la presenza di **volti di terzi** nel girato. Su tutto
il resto: decidi, procedi, e documenta nel BRIEF del video.

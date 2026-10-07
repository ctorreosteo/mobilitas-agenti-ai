---
workflow: general-video
flow: automation
storyboard: no
message: "Il grasso sulla pancia non cede finché non sistemi il cortisolo, e il cortisolo si sistema dall'orario in cui vai a dormire"
destination: youtube
aspect: 3840x2160
language: it
length: 78s
angle: caso-clinico
---

## Intent

Talking-head di divulgazione clinica in italiano: un professionista spiega perché
lavorare solo sulla dieta non smuove la pancia, e perché l'orario del sonno —
via cortisolo — conta più della porzione pesata al grammo. Chiude con un caso
clinico (30 giorni, cambiato solo il sonno).

Tono: divulgativo e diretto, ritmo social, ma con credibilità clinica. Non
motivazionale, non allarmista: spiega un meccanismo.

## Assets

- assets/source-4k.mp4 — girato originale (video_prova.mov) ruotato, deinterlacciato
  di metadati, upscalato a 3840x2160 lanczos, H.264 CRF 18, audio AAC copiato bit-per-bit.
  È l'unica sorgente immagine e suono.
- data/transcript.srt — trascrizione fornita dall'utente, timing parola-per-parola,
  in tempo SORGENTE. Tre refusi corretti (vedi Notes).
- data/captions.json — compilato da scripts/build-captions.mjs: stessa trascrizione
  mappata in tempo COMPOSIZIONE, con l'EDL applicato e i tagli rimossi.

## Customizations

- **Tagli approvati dall'utente.** Rimossi: 3,7s di silenzio (src 52,7→56,0), il
  segmento di prova "Adesso proviamo a fare degli errori… questa parte è sbagliata"
  (src 56,5→60,0) e la papera con il primo ciak fallito "…una paziente? Un paziente.
  Ah no, ah, ok, riprendiamo" (src 60,0→64,48). Si tiene la seconda ripresa, buona.
- **Sottotitoli karaoke** a 2–3 parole, parola attiva evidenziata in accento con
  micro-pop; parole chiave (cortisolo, grasso viscerale, sonno, 30 giorni…) marcate `hot`.
- **Pacchetto grafico completo**: lockup d'apertura, chip identità, tre card concetto
  nel terzo destro, card di stacco "E COME?" sul giunto, closing card, progress bar.
- **Brand disattivato su richiesta dell'utente (21/08/2026).** Nessun dato reale fornito:
  `SHOW_BRAND = false` in `scripts/build-composition.mjs`. Il chip identità esce con
  `data-hidden` (reversibile in place) e la riga nome studio non viene emessa. Per
  riattivarli: `SHOW_BRAND = true`, rigenera, e passa i valori con `--variables`.

## Notes

- **Riferimento di editing**: youtube.com/@Studio_Mobilitas (divulgazione osteopatica).
  È un riferimento di STILE, non il brand del video: nessun logo e nessun nome di quel
  canale entra nella composizione. La palette navy/menta è derivata da lì come registro
  cromatico e resta sostituibile via variabili (`accent`, `brandName`, `speakerName`).
- **Correzioni di trascrizione** (solo sottotitoli, audio intatto):
  "contata **la** perfezione" → "contata **alla** perfezione";
  "che **sei** seguito le indicazioni" → "che **se hai** seguito le indicazioni";
  "continuare a **rimare** contro di te" → "continuare a **remare** contro di te".
- **4K è un upscale**: il girato nasce 1916x1078 (≈1080p) con rotation −90 nei metadati.
  Il master è portato a 3840x2160 con lanczos; il dettaglio ottico resta quello della
  sorgente, mentre tutta la grafica e i sottotitoli sono renderizzati nativi in 4K.
- Il soggetto sta stabilmente a sinistra/centro inquadratura: il terzo destro è la
  zona sicura per le card. Primi ~10s in corridoio buio, poi stanza chiara — i
  sottotitoli portano sempre uno scrim locale per reggere entrambe le luminanze.

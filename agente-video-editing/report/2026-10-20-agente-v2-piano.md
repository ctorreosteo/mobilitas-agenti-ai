# Agente video editing v2: piano

20/10/2026. Questo piano viene aggiornato mentre lavoro; la versione finale è quella che resta in questa cartella.

## Stato al 20/10, ore 17

Fatto e provato sul girato di YT_TOFU_02 (progetto `videos/YT_TOFU_02-v2`):

- **motore** completo, 19 fasi dietro `./mve`, nessuno script nella cartella del video;
- **cacciatore di papere v2**: trova da solo tutte le 13 papere che nella v1 erano state cercate a mano, **più 5 che la v1 aveva consegnato** senza vederle (verificate con sonde brevi sul file v1):
  - 1:05 "mancano ancora due ore e… / mancano ancora due ore e mezza"
  - 9:27 "devi iniziare a pensare… / devi iniziare a pensarlo"
  - 10:29 "Si pa… no… si parte dal diaframma"
  - 11:36 "si è appiattito / si appiattisce"
  - più un "qua" e un "di" sospesi;
- **sottotitoli**: la trascrizione del montato della v1 perdeva la prima parola di molte frasi; ora sono 2161 parole contro 2018 (143 parole che a schermo sarebbero mancate);
- **inquadrature dal 4K**: 108 pezzi, cambio di taglio a ogni giunta, render in 6 minuti con cache;
- **titoli dietro la presentatrice**, posizionati misurando la sagoma;
- **card** posizionate sul volto misurato: margine minimo 45 px dalla testa;
- sound design sintetizzato, Shorts, miniature, pacchetto YouTube, QC con cancello.

Il dettaglio di ogni decisione sta nelle skill e nel `BRIEF.md` del video.

## Dove eravamo

L'agente v1 sono tre skill (`mobilitas-style`, `mobilitas-montaggio`, `mobilitas-grafica`) più una ventina di script **copiati dentro il singolo video** (`videos/YT_TOFU_02/scripts/`). Ogni video nuovo ripartiva da capo:

- i tagli, le card e i capitoli erano scritti **dentro il codice** (`REMOVE = [...]`, `CARDS = [...]`);
- negli script c'erano percorsi assoluti a una cartella temporanea di una sessione vecchia;
- non c'era un `CLAUDE.md`: nessun punto d'ingresso, nessuna sequenza di fasi, nessun controllo che blocca la consegna;
- l'inquadratura restava fissa per 13 minuti e le giunte erano dissolvenze di 5 frame, che sulla macchina fissa si leggono come "salti morbidi";
- il video usciva **senza alcun suono** oltre alla voce;
- niente Shorts, niente miniature, niente titolo e descrizione;
- il controllo visivo lo faceva Carlos guardando il video finito.

Quello che funzionava va tenuto: il sondaggio delle pause per trovare le papere, i punti di taglio sul fondo di sala, il LUT HLG, il renderer Pillow in pipe e lo stile navy/menta.

## Cosa diventa

Il codice diventa **un motore unico e riusabile** (`motore/`). Ogni video ha **un solo file di decisioni**, scritto dall'agente: `videos/<slug>/regia.json`. Per un video nuovo non si scrive più codice.

```
agente-video-editing/
  CLAUDE.md                ← l'agente: fasi, cancelli, politiche
  mve                      ← comando unico: ./mve <fase> <slug>
  motore/                  ← il motore (Python + Swift/Vision)
  .claude/skills/          ← il sapere: stile, montaggio, grafica, + regia, shorts, packaging
  .claude/agents/          ← i revisori: papere, regista, visivo, audio
  .claude/commands/        ← /monta, /rivedi, /correggi, /shorts
  videos/<slug>/regia.json ← le decisioni del singolo video
```

## Le capacità nuove

| # | capacità | perché conta |
|---|---|---|
| 1 | **Inquadratura dinamica dal 4K**: tre tagli di camera (largo, medio, stretto) ricavati dal 4K senza perdita, centrati sul volto rilevato da Apple Vision | è il "doppia camera" dei canali grossi; nasconde i jump cut meglio della dissolvenza e dà ritmo |
| 2 | **Giunte a stacco con cambio di taglio** al posto delle dissolvenze | lo stacco secco con cambio di inquadratura è invisibile; la dissolvenza si vede |
| 3 | **Enfasi**: punch-in sulle frasi chiave scelte in regia | il pubblico capisce cosa conta senza grafica |
| 4 | **Titoli dietro la presentatrice** (sagoma da Vision) per gli stacchi di capitolo | effetto da motion designer, mai visto sul canale; non copre il volto per costruzione |
| 5 | **Card che sanno dov'è il volto**: posizione calcolata dalla traccia del volto, non stimata | elimina il difetto "card sul viso" alla radice |
| 6 | **Sound design sintetizzato in casa**: whoosh per le card, colpo sordo per gli stacchi, tick sui numeri, sotto la voce | il video smette di essere muto fra le parole; niente stock né licenze |
| 7 | **Cacciatore di papere v2**: sondaggio pause + a-parte + ripetizioni + **allineamento al copione** se c'è | trova le riprese doppie anche quando whisper le appiana |
| 8 | **Ascolto delle giunte prima del render**: monta solo l'audio e ritrascrive ogni cucitura | gli errori si trovano in 2 minuti invece che dopo un render da 10 |
| 9 | **QC automatico con cancello**: tag colore, LUFS, true peak, durata, frame neri/congelati, card sul volto, giunte | se un controllo fallisce, non si consegna |
| 10 | **Revisori in parallelo**: regista (ritmo, hook, ridondanze), visivo (guarda i fotogrammi), audio | il secondo parere che prima mancava |
| 11 | **Shorts 9:16 dal 4K** con volto inseguito, sottotitoli verticali e hook | un video lungo diventa 3-5 contenuti |
| 12 | **Miniature**: fotogrammi scelti con la qualità del volto di Vision, 3 varianti grafiche | la miniatura conta quanto il video |
| 13 | **Pacchetto YouTube**: titoli, descrizione con capitoli, tag, SRT | consegna pronta da caricare |

## Come lo verifico

Il banco di prova è **YT_TOFU_02**, di cui conosciamo la verità: 13 papere trovate a mano e due difetti segnalati da Carlos dopo la prima consegna.

1. Il cacciatore v2 gira da zero sulla sorgente: deve far emergere **tutte e 13** le papere fra i candidati.
2. Montaggio completo v2 di YT_TOFU_02 con le capacità nuove, renderizzato e controllato.
3. Shorts e miniature dallo stesso girato.
4. Controllo sul disco di ogni file consegnato (durata, tag, loudness), non sul valore di ritorno degli script.

## Cosa resta fuori, e perché

- **Musica di sottofondo**: il motore la supporta (con ducking sotto la voce), ma serve un brano con licenza. Si attiva mettendo un file in `assets/musica/`.
- **Cold open** (una frase forte spostata in apertura): il motore la supporta, ma riordinare il discorso è una scelta editoriale. L'agente la propone e non la applica da solo.
- **B-roll**: l'agente B-roll non ha ancora prodotto clip utilizzabili (l'ultima generazione è fallita). L'aggancio resta una fase successiva.

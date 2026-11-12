# inbox: dove si mettono i video da lavorare

Una cartella per ogni video, con il nome del video: lettere maiuscole, numeri, trattino e trattino basso, senza spazi. Per
esempio `inbox/AD_SCHIENA_03/`.

```
inbox/AD_SCHIENA_03/
  AD_SCHIENA_03.mp4    il video montato, verticale 1080×1920 o orizzontale 1920×1080 (.mp4 o .mov), così come esce
                       dal montaggio (uno solo)
  AD_SCHIENA_03.srt    (se c'è) i sottotitoli: aiutano a leggere il copy giusto
  AD_SCHIENA_03.mp3    (se c'è) la voce o l'audio del montaggio
  info.txt             (se serve) nomi propri da scrivere giusti, note per l'agente
```

## Regole

- Il video **non si sposta e non si cancella**: l'agente lo legge e non lo modifica.
- Senza SRT l'agente legge i sottotitoli impressi nel video, o ascolta la voce, e ti chiede di confermare il testo.
- Nomi propri (lo studio, le persone): l'agente li scrive solo se sono in un file qui dentro o glieli dici tu.
- Nel repository finisce solo questo file: i video restano sul vostro Mac.

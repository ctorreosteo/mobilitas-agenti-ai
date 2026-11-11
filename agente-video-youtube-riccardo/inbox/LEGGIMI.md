# inbox: dove si mette il girato

Una cartella per ogni video, con il nome del video: lettere maiuscole, numeri e
trattino basso, senza spazi. Per esempio `inbox/YT_POSTURA_33/` o
`inbox/MR_SCHIENA_02/`.

```
inbox/YT_POSTURA_33/
  C1234.MP4        il girato, così come esce dalla camera (uno solo)
  script.txt       il testo del video (uno solo, .txt o .md)
  info.txt         nome e cognome dell'osteopata e tipo di video
  materiali/       (se servono) cose usate solo in questo video
```

## info.txt

Due righe, scritte così:

```
osteopata: Nome Cognome
tipo: YouTube
```

- `osteopata`: nome e cognome di chi parla in camera, **scritti giusti**: vanno
  a schermo nel cartellino con il nome. L'agente non li prende mai dalla
  trascrizione automatica, che sbaglia i cognomi.
- `tipo`: `YouTube` (video del canale) oppure `mid-roll` (il pezzo pubblicitario
  che va dentro un altro video).
- facoltativa una terza riga `ruolo: Osteopata, Studio Osteopatico Mobilitas` se
  il ruolo nel cartellino deve essere diverso.

## materiali/

Cose che servono solo a questo video: le schermate dell'app (con un profilo di
prova, mai dati veri), una grafica fatta apposta, un documento. Quello che serve
a più video va in `libreria/`.

## Regole

- Il girato **non si sposta e non si cancella**: l'agente lo collega, non lo
  copia.
- Se manca qualcosa (girato, script, nome dell'osteopata, tipo di video),
  l'agente si ferma e lo chiede.
- Nel repository finisce solo questo file: i girati restano sul vostro Mac.

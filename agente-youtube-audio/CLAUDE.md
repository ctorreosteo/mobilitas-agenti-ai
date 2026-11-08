# Agente YouTube → audio + trascritto

Da un link YouTube metti in `~/Downloads` tre file con lo stesso nome:

- `<titolo>.mp3`, l'audio del video;
- `<titolo>.txt`, il trascritto di quell'audio, fatto **in locale** da Spokenly;
- `<titolo>_schema.docx`, lo schema di studio in italiano, in **Word**, che
  scrivi tu leggendo il trascritto (sezione «Lo schema di studio»).

In `~/Downloads` finiscono solo questi tre file: mai un `.md`.

## Quando ti attivi

Quando ti viene dato un link YouTube (youtube.com/watch, youtu.be, shorts). Se il
messaggio contiene più link, li fai **uno alla volta**, in fila.

## Come lavori

Un comando solo:

```
./yt2txt "<link>"              # trascritto semplice
./yt2txt "<link>" --speakers   # con le etichette di chi parla (interviste, podcast)
```

Usa `--speakers` solo se è richiesto o se il video è chiaramente un dialogo.

Lo script scarica l'audio con `yt-dlp`, poi chiama lo strumento `transcribe_file`
del server MCP di Spokenly (`localhost:51089`). Se Spokenly è chiuso lo apre da
solo e aspetta che risponda.

## Prima di dire «fatto»

Controlla sul disco, non fidarti dell'output dello script:

- i due file esistono in `~/Downloads`;
- il `.txt` non è vuoto e il numero di parole è sensato rispetto alla durata
  del video (un parlato normale va da 120 a 200 parole al minuto; molto sotto
  vuol dire musica, silenzi o un trascritto tagliato).

Poi passi allo schema.

## Lo schema di studio

Leggi **tutto** il trascritto, non solo l'inizio (se è lungo, a pezzi, ma
tutto). Lo schema serve per imparare tutto quello che dice il video senza
riascoltarlo.

**Come si produce il Word.** Scrivi lo schema in Markdown in
`lavoro/<titolo>_schema.md` (cartella dell'agente, fuori da Downloads), poi:

```
./schema2docx lavoro/<titolo>_schema.md ~/Downloads/<titolo>.mp3
```

Lo script crea `~/Downloads/<titolo>_schema.docx` con lo stile fisso di
`stile-schema.docx` (A4, Arial, titoli blu, tabelle con bordi e intestazione
colorata). Nel Markdown usa solo cose che Word rende bene: titoli `#`/`##`/`###`,
elenchi, elenchi numerati, **grassetto**, *corsivo*, tabelle a pipe, `---`.
Niente HTML (`<details>`, `<br>`): in Word non funziona. Il titolo del documento
è il primo `#`.

**Lingua.** Sempre italiano, anche se il video è in un'altra lingua. I termini
tecnici restano nella lingua originale la prima volta, tra parentesi
(«corrispondenza a frase (*phrase match*)»), se è così che si trovano negli
strumenti.

**Struttura**, in quest'ordine:

1. **Intestazione**: titolo originale, link, durata, autore (se si presenta),
   lingua del video.
2. **In breve**: 3-5 righe con l'idea centrale e cosa si sa fare dopo averlo
   studiato.
3. **Mappa**: l'elenco dei grandi temi, così si vede la struttura prima dei
   dettagli.
4. **Una sezione per tema**, ordinata per logica e non per minutaggio se il
   video salta da un argomento all'altro. Dentro: punti brevi; ogni regola con il
   suo *perché* quando il video lo dà; i passaggi operativi come lista numerata;
   ogni numero, cifra, soglia ed esempio citati; gli errori da evitare evidenziati
   (⚠️). Le tabelle vanno bene per i confronti (opzione A contro B).
5. **Errori da evitare**: tutti in un posto solo, con il motivo.
6. **Glossario** dei termini tecnici.
7. **Domande di ripasso**: 8-15 domande numerate, **senza** risposta sotto,
   così si prova a rispondere prima di guardare.
8. **Soluzioni**: le risposte, con lo stesso numero della domanda.
9. **Punti dubbi del trascritto**: dove il trascritto è palesemente sbagliato o
   ambiguo (cifre che non tornano, nomi storpiati), scrivi cosa c'è nel testo e
   l'interpretazione più probabile, segnata come tale.

**Regole.**

- Solo quello che dice il video. Niente aggiunte tue presentate come contenuto
  del video: se un contesto serve davvero, scrivilo in una nota «(nota, non dal
  video)».
- Non inventare cifre e non «correggere» in silenzio quelle strane: vanno nei
  punti dubbi.
- Autopromozione, call to action, «iscriviti» e saluti: al massimo una riga
  nell'intestazione.
- **Completo vuol dire completo.** Finito lo schema, ripassa il trascritto dall'inizio
  alla fine e verifica che ogni consiglio, numero, passaggio ed esempio concreto
  sia nello schema. Quello che manca lo aggiungi prima di consegnare.

Prima di consegnare controlla il `.docx` sul disco: `pandoc <file>.docx -t plain | head -60`
deve mostrare il testo, e il numero di parole stampato da `schema2docx` deve
essere vicino a quello del Markdown.

Alla fine rispondi con i tre percorsi, le prime righe del trascritto e la mappa
dello schema.

## Se qualcosa va storto

- **Download fallito**: video privato, rimosso o con limite d'età. Dillo, non
  cercare altre strade.
- **Spokenly non raggiungibile**: va attivato il server MCP nelle impostazioni
  di Spokenly. Dillo e fermati: non trascrivere con altri strumenti.
- **Manca `yt-dlp` o `ffmpeg`**: `brew install yt-dlp ffmpeg`.

Non modificare il `.txt`: è l'uscita grezza di Spokenly. Le correzioni e le
interpretazioni vanno solo nello schema.

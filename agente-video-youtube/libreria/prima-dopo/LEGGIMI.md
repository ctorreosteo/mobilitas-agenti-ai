# Prima-dopo: foto di pazienti

Foto di un paziente in piedi, nella stessa posizione, prima e dopo. Questa
cartella arriva **vuota**.

## Regole

- **Solo con il consenso scritto** del paziente, segnato in `libreria/catalogo.md`
  (sì e data), anche se il volto non si vede. Senza riga nel catalogo la foto non
  si usa.
- **Le foto non escono da questa cartella**: niente copie su altri dischi, chat,
  email o servizi online. Il repository non le prende (`.gitignore`).
- **Quale foto è "prima" e quale "dopo" lo dice solo la data di scatto** salvata
  dalla camera, mai l'aspetto della postura. Se la data manca o non è chiara,
  l'agente chiede.
- **Sulle foto a schermo si scrive solo PRIMA e DOPO.** Niente tempi, numero di
  sedute, riferimenti al percorso o ai risultati, a meno che la colonna "cosa c'è
  tra le due foto" del catalogo non lo dica. Mai "risolto", "corretto", "guarito".
- A video consegnato l'agente cancella da `.lavoro/` tutti i ritagli delle foto,
  per primi.

## Nomi dei file

`P001_prima_laterale.jpg`, `P001_dopo_laterale.jpg`. Il codice paziente è P + tre
cifre; la vista è `frontale`, `laterale` o `posteriore`. **Il vero nome del
paziente non va mai nel nome del file.**

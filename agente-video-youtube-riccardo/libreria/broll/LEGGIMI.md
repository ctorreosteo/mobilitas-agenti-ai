# B-roll: riprese di contorno

Brevi video senza nessuno che parla in camera: mani al lavoro, lo studio, un
trattamento. Questa cartella arriva **vuota**: ognuno ci mette i suoi.

## Come si mettono

Una sottocartella per tema, con un nome semplice in minuscolo: per esempio
`collo`, `schiena`, `gambe`, `braccia`, `pancia`, `atm` (testa, collo e mandibola),
`sala-attesa`.

Come devono essere le riprese:

- **orizzontali**, mai in verticale;
- **da 5 a 20 secondi** l'una: meglio tante brevi che una lunga;
- **4K, a 25 o 50 fotogrammi al secondo**, come il presentatore;
- **ferme**: cavalletto, gimbal o appoggio. Quelle a mano che tremano non si usano;
- il file **così come esce dalla camera** (`.MP4`, `.MOV`): non convertirlo e non
  comprimerlo. Gli zip vanno estratti prima;
- se si riconosce una persona serve il suo **consenso scritto**, segnato in
  `libreria/catalogo.md`.

Nel video il B-roll è **sempre senza audio**.

## Come le cataloga l'agente

La prima volta che serve un B-roll, e ogni volta che trova clip nuove (`./mve stato`
le conta), l'agente:

1. lancia `./mve libreria`, che misura ogni clip (durata, risoluzione, movimento di
   camera, tremolio, volti) e prepara dei fogli di fotogrammi in `.indice/fogli/`;
2. guarda i fogli e scrive una descrizione e un voto per ogni clip in
   `.indice/descrizioni/<tema>.json`;
3. esclude per sempre, in `.indice/esclusioni.json`, le clip con:
   - il marchio di un altro studio sulla divisa;
   - segni di penna sulla pelle;
   - glutei o slip in primo piano;
   - marchi commerciali leggibili su abiti, intimo o apparecchi;
4. rilancia `./mve libreria`: escono `indice.json` e `indice.md`.

Il motore sceglie il B-roll solo fra le clip descritte, con voto sufficiente e non
escluse. `.indice/`, `indice.json` e `indice.md` restano sul vostro Mac, come le
clip.

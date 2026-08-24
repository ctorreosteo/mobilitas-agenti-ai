# Il protocollo delle fonti

> **Leggi questo file prima di ogni altro.** È la regola che separa un atto depositabile da un
> atto che distrugge il proprio autore.

## Perché è la prima regola e non l'ultima

Un modello linguistico produce il numero di una sentenza con la stessa fluidità con cui produce
una virgola. Sette cifre, un anno, una sezione, una massima perfettamente plausibile e scritta
nella lingua giusta. È inesistente, e **non c'è modo di accorgersene rileggendo**: sembra vera
esattamente quanto quelle vere.

Poi succede questo: la controparte la cerca, non la trova, e lo scrive. Da quel momento il
giudice legge tutto il resto dell'atto sapendo che chi lo ha scritto cita sentenze inventate.
**Non perdi il punto: perdi i venti punti veri che stavano accanto.** È il danno più grande che
un difensore possa farsi da solo, e costa cinque minuti evitarlo.

C'è anche un profilo che riguarda l'avvocato che firma: depositare un atto con riferimenti
inesistenti è un problema suo, davanti al cliente e davanti al Consiglio dell'Ordine. Il
materiale che produci deve poter essere firmato senza che chi firma debba rifare il lavoro.

## Le tre domande, in quest'ordine

**1. Esiste?** Il riferimento è reale.

**2. Dice questo?** È la domanda che quasi nessuno fa, ed è quella che conta. L'allucinazione più
pericolosa non è la sentenza inventata — quella si scopre. È **la massima inventata attaccata a
una sentenza vera**: il numero regge al controllo, il principio no, e lo scopri in udienza.

**3. Vale ancora?** Le norme cambiano, gli orientamenti si rovesciano, le riforme entrano in
vigore a scaglioni e vengono prorogate. Una massima del 2019 su una norma riscritta nel 2022
non vale niente, ma sembra ottima.

## I tre livelli di conferma

| Livello | Quando | Cosa puoi scrivere in atto |
|---|---|---|
| **CONFERMATA** | Hai letto il testo ufficiale: Normattiva, Gazzetta Ufficiale, il sito della Cassazione, la banca dati ufficiale | Citazione piena, numero compreso |
| **PARZIALE** | Più fonti secondarie indipendenti e concordi, nessuna ufficiale | **Il principio sì, il numero no**: *«secondo l'orientamento consolidato di legittimità…»* |
| **NON TROVATA** | Nessun riscontro, o solo blog che si copiano | **Non si cita.** Resta nel registro come monito |

**Fonti secondarie indipendenti** significa testate e studi che citano la sentenza avendola letta,
non tre siti che riportano lo stesso identico paragrafo. Se il testo è identico, è **una** fonte.

## La regola del principio senza numero

È l'uscita onesta, ed è quasi sempre sufficiente. Un giudice italiano non ha bisogno che tu gli
numeri una sentenza per riconoscere un orientamento che conosce meglio di te.

| Invece di | Scrivi |
|---|---|
| «Cass. n. 12345/2023 ha stabilito che…» *(non verificata)* | «Secondo l'orientamento consolidato della giurisprudenza di legittimità…» |
| «la Suprema Corte con sentenza n. X ha affermato…» | «È principio affermato in sede di legittimità che…» |

**Non perdi quasi nulla, e non rischi niente.** Un atto costruito su principi corretti senza
numeri è più forte di un atto costruito su numeri inventati: il primo si discute, il secondo si
smonta.

## Il registro

Ogni fonte verificata va in `fascicolo/_dati/registro-fonti.md` **prima** di entrare in un atto.
Il registro è **solo append**: più agenti ci scrivono in parallelo, e riscriverlo perde il lavoro
degli altri.

Registra anche le fonti **non trovate**. Serve a impedire che qualcuno le riproponga a memoria
la settimana dopo, ed è successo abbastanza da meritare una sezione dedicata nel registro.

L'hook `blocca-citazioni-non-verificate.py` applica materialmente la regola: un riferimento
numerato che non compare nel registro non entra in un file di atto. **Se l'hook ti blocca, non
cercare una via alternativa**: significa che stavi per scrivere qualcosa che non hai verificato.
Verifica, registra, riscrivi.

## Le prassi locali — l'errore che nessuno prevede

Molto di ciò che decide l'esito **non è legge**: è la prassi dell'ufficio davanti al quale
discuti. I protocolli sulle spese straordinarie, le tabelle di riferimento per il contributo, i
calendari-tipo di frequentazione, la prassi sui pernottamenti sotto i tre anni: cambiano da
tribunale a tribunale, e a volte da sezione a sezione.

> **Non scrivere mai «i tribunali italiani ritengono».** Verifica il protocollo dell'ufficio
> davanti al quale stai discutendo, e cita quello.

Un protocollo locale citato per esteso vale, davanti a quel giudice, più di tre sentenze di
Cassazione: è il documento che lui stesso ha contribuito a scrivere.

## Le norme che si muovono sotto i piedi

Alcune voci vanno **riverificate a ogni atto**, non una volta per tutte. Sono quelle in
transizione:

- **Il Tribunale per le persone, per i minorenni e per le famiglie.** L'entrata in funzione è
  stata prorogata al **31 ottobre 2026** (`D.L. 117/2025`), ed è già la seconda proroga. Siamo a
  ridosso: quale ufficio è competente è la prima cosa da controllare prima di un atto
  introduttivo, e la risposta può essere cambiata dall'ultima volta. Un ricorso all'ufficio
  sbagliato costa mesi, e in una causa dove il bambino cresce, i mesi sono il vero costo.
- **Le disposizioni transitorie della riforma Cartabia**: quale rito si applica dipende da quando
  il procedimento è stato introdotto.
- **Gli interventi in materia di violenza domestica**, che si sono succeduti rapidamente e
  incidono su misure cautelari e tempi del penale.

## Il documento che non hai letto

Vale per il fascicolo quanto per la giurisprudenza: **non affermare il contenuto di un documento
che non hai aperto.** Se il cliente dice «nel referto c'è scritto che», il fatto è `ALLEGABILE`
finché non leggi il referto. Diventa `PROVATO` quando lo leggi e ci trovi quella frase — e
qualche volta non ce la trovi, ed è meglio scoprirlo adesso.

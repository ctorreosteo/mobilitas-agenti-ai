# Verifica, metriche e anti-pattern

---

# Parte 1 — Le metriche

## L'indice Gulpease

`89 + (300 × frasi − 10 × lettere) / parole` — Lucisano e Piemontese, 1988. L'unico indice di leggibilità costruito sull'italiano invece che tradotto dall'inglese.

| Punteggio | Chi ci arriva |
|---|---|
| **80-100** | licenza elementare ← **bersaglio quinta elementare** |
| 60-80 | licenza media |
| 40-60 | diploma superiore |
| sotto 40 | difficile per tutti |

**Come si alza, in ordine di resa.** La formula premia due cose: **più frasi** e **meno lettere per parola**.

1. **Spezzare le frasi** — l'intervento con l'effetto più forte, perché il numero di frasi è moltiplicato per 300.
2. **Sostituire le parole lunghe** con parole corte — agisce sul conteggio delle lettere.
3. Togliere gli aggettivi vuoti — agisce su entrambi i termini.

**I due limiti dell'indice, da conoscere.**

- **Non capisce il significato.** Un testo fatto di frasi corte e senza senso ottiene un Gulpease altissimo. Il punteggio è una condizione necessaria, mai sufficiente: **misura la forma, non la comprensione**.
- **Punisce le parole lunghe anche quando sono comuni.** *Responsabilità* pesa come un tecnicismo raro, ma è una parola che tutti capiscono. Non sacrificare una parola comune e chiara per guadagnare due punti.

**Quindi:** il Gulpease serve a trovare i punti da guardare e a dimostrare che il lavoro è stato fatto. Non a decidere se il testo è buono. Quello lo decide la verifica di equivalenza.

## Le altre misure

| Misura | Bersaglio | Perché |
|---|---|---|
| Parole per frase (media) | 12-15 | Sopra le 20 la memoria di lavoro di un lettore poco esperto si satura |
| Frase più lunga | max 25 | Una sola frase lunga può bloccare la lettura di un intero paragrafo |
| Parole fuori dal Vocabolario di Base | sotto il 5% | Oltre, il lettore incontra una parola sconosciuta ogni due righe |
| Subordinate per periodo | max 1 | |
| Frasi lasciate intatte | 30-50% | **Se è sotto il 30%, stai riscrivendo invece di semplificare** |

L'ultima riga è una metrica di **fedeltà**, non di leggibilità, ed è quella che si dimentica sempre.

---

# Parte 2 — La verifica di equivalenza

Il controllo che conta più di tutte le metriche messe insieme.

## Il metodo della lista dei fatti

1. **Prima** di semplificare, elenca ogni affermazione dell'originale in ordine, una riga ciascuna, in forma brevissima.
2. **Dopo**, spunta ogni riga sul testo nuovo.
3. Conta.

| Risultato | Significa | Cosa fare |
|---|---|---|
| Stesso numero, tutte spuntate | Equivalenza rispettata | Consegna |
| Righe non spuntate | Hai riassunto | Rimetti le informazioni mancanti |
| Fatti nuovi nel testo nuovo | Hai spiegato o interpretato | Toglili |
| Una riga spuntata "quasi" | **Il caso più pericoloso** | Vedi sotto |

## Il controllo delle sfumature

Per ogni affermazione che contiene una di queste, confronta parola per parola con l'originale:

- **Un numero o una quantità** → identico?
- **Una possibilità** (*può*, *potrebbe*) → è ancora una possibilità, o è diventata un fatto?
- **Una frequenza** (*spesso*, *a volte*) → stesso grado?
- **Una condizione** (*se*, *salvo*, *tranne*) → c'è ancora, ed è ancora legata alla stessa cosa?
- **Un obbligo** (*deve*) contro un consiglio (*è meglio*) → non si sono scambiati?
- **Un soggetto** → chi fa l'azione è la stessa persona di prima?

**Il test delle conseguenze:** una persona che legge solo la versione semplificata farebbe le stesse cose di una che legge l'originale? Prenderebbe le stesse decisioni? Avrebbe le stesse aspettative? Se anche una sola risposta è no, la semplificazione ha cambiato il testo.

---

# Parte 3 — Gli 11 anti-pattern

## 1. Il riassunto mascherato

**Sintomo:** il testo nuovo è più corto del 20% o più.
**Causa:** frasi dense trasformate in frasi corte **buttando via** invece di distribuire.
**Correzione:** un testo semplificato è di solito **più lungo** dell'originale. Se si è accorciato, cerca cosa manca con la lista dei fatti.

## 2. L'infantilizzazione

**Sintomo:** esclamativi, emoji, diminutivi, tono da maestra, "facilissimo!", "eccoci qua!".
**Causa:** confuso il *livello di lettura* con il *tono*.
**Correzione:** togli tutto quello che non c'era nell'originale. Il lettore è un adulto: semplice e rispettoso, non semplice e paternalistico.

## 3. L'arrotondamento delle sfumature

**Sintomo:** nessuno immediato. È il difetto più grave e il meno visibile.
**Causa:** *può* → *fa*, *spesso* → *sempre*, *alcuni* → *tutti*, *sembra* → *è*.
**Correzione:** le parole di grado sono dati. Trattale come numeri.

## 4. Il termine tecnico cancellato

**Sintomo:** il testo è più scorrevole e il lettore non sa più come si chiama la sua condizione.
**Causa:** sostituito un tecnicismo invece di spiegarlo.
**Correzione:** il termine resta e si spiega dentro la frase. Serve alla persona per cercarlo, riconoscerlo su un referto, parlarne col medico.

## 5. L'uniformazione

**Sintomo:** tutte le frasi hanno la stessa lunghezza e lo stesso ritmo. Il testo è piatto.
**Causa:** applicata la trasformazione anche dove non serviva — violato il livello 0.
**Correzione:** rimetti le frasi che andavano già bene. La varietà di ritmo aiuta la lettura, non la ostacola.

## 6. La spiegazione non richiesta

**Sintomo:** il testo nuovo contiene informazioni che l'originale non dava.
**Causa:** aggiunto contesto per "aiutare".
**Correzione:** toglilo. Se pensi che manchi qualcosa di importante, **dillo all'utente** invece di metterlo nel testo.

## 7. La struttura riorganizzata

**Sintomo:** paragrafi spostati, titoli cambiati, informazioni raggruppate diversamente.
**Causa:** confuso semplificazione con riprogettazione.
**Correzione:** l'ordine è dell'originale. Se l'ordine è il problema, segnalalo separatamente.

## 8. Il registro cambiato

**Sintomo:** l'originale dava del lei, il risultato dà del tu. O un testo formale è diventato colloquiale.
**Causa:** associato "semplice" a "informale".
**Correzione:** un testo può essere formale e semplice insieme, ed è quasi sempre quello che serve. Il registro è dell'originale.

## 9. La citazione semplificata

**Sintomo:** una testimonianza suona diversa da come parlerebbe quella persona.
**Causa:** applicate le regole anche dentro le virgolette.
**Correzione:** le parole di un'altra persona non si toccano mai. Semmai si aggiunge una spiegazione fuori dalle virgolette.

## 10. Il Gulpease inseguito

**Sintomo:** punteggio ottimo, testo peggiore.
**Causa:** ottimizzato il numero invece della comprensione: frasi mozzate, parole comuni sacrificate perché lunghe.
**Correzione:** il Gulpease trova i punti da guardare, non decide. Se una frase è chiara e l'indice non sale, la frase resta.

## 11. La persuasione spenta

**Sintomo:** un testo di marketing semplificato diventa un foglio informativo.
**Causa:** trattate come "complicazioni" gli elementi che facevano il lavoro: ganci, domande, contrasti, ripetizioni volute.
**Correzione:** la semplificazione tocca **la lingua**, non la funzione. Una domanda resta una domanda, un gancio resta un gancio. Si semplificano le parole con cui sono fatti.

---

# Parte 4 — Checklist finale

### Equivalenza
- [ ] Lista dei fatti compilata prima, spuntata dopo
- [ ] Nessuna informazione persa
- [ ] Nessuna informazione aggiunta
- [ ] Numeri, date, prezzi, misure identici
- [ ] Nomi propri e marchi identici
- [ ] Citazioni intatte
- [ ] Contatti, link e orari intatti

### Sfumature
- [ ] Possibilità e obblighi hanno lo stesso grado
- [ ] Frequenze e quantità hanno lo stesso grado
- [ ] Ogni condizione ed eccezione è ancora presente e legata alla stessa cosa
- [ ] Test delle conseguenze superato: chi legge farebbe le stesse cose

### Struttura
- [ ] Stesso ordine dei paragrafi
- [ ] Stessi titoli e sottotitoli
- [ ] Stessa formattazione (grassetti, elenchi, a capo)
- [ ] Call to action e condizioni dell'offerta invariate

### Lingua
- [ ] Gulpease ≥ 80
- [ ] Media 12-15 parole per frase
- [ ] Nessuna frase oltre le 25 parole
- [ ] Nessuna nominalizzazione rimasta senza motivo
- [ ] Nessun riferimento indietro non risolto (*il medesimo*, *tale*, *quest'ultimo*)
- [ ] Termini tecnici obbligatori: presenti e spiegati

### Tono
- [ ] Stesso registro (tu / lei / impersonale)
- [ ] Nessun esclamativo, emoji o diminutivo aggiunto
- [ ] Nessun tono paternalistico
- [ ] La funzione persuasiva è intatta

### Fedeltà
- [ ] Tra il 30% e il 50% delle frasi è rimasto intatto
- [ ] Meno del 20% delle frasi è stato riscritto da zero (livello 4)
- [ ] Il testo non si è accorciato in modo significativo

---

# Parte 5 — Quando fermarsi e chiedere

Non decidere da solo. Segnala all'utente e aspetta:

- **Una semplificazione cambierebbe cosa fa il lettore** (ambito sanitario, legale, finanziario).
- **Il testo ha valore legale.** Non si semplifica: si affianca una versione spiegata, dichiarata come non sostitutiva.
- **Un termine tecnico non ha spiegazione breve possibile** senza perdere precisione.
- **L'originale è ambiguo.** Semplificare costringe a scegliere un significato — e quella scelta è dell'autore, non tua.
- **Il bersaglio non è raggiungibile** senza superare il 20% di riscritture: il testo va forse riprogettato, e questo è un altro lavoro.

---
name: testo-semplice-quinta-elementare
description: Semplifica qualsiasi testo — email, pubblicità, copy di un sito, documento, articolo, contratto, post — portandolo al livello di lettura di un bambino di quinta elementare, senza cambiare il significato, senza tagliare informazioni e con il minimo intervento necessario. Usa il Vocabolario di Base di De Mauro, l'indice Gulpease e le regole del linguaggio chiaro. Attiva SEMPRE questa skill quando l'utente dice "semplifica", "rendi più semplice", "riscrivi in modo semplice", "linguaggio semplice", "quinta elementare", "più chiaro", "più leggibile", "troppo tecnico", "troppo difficile", "burocratese", "plain language", "spiegalo semplice", "che si capisca", oppure quando chiede di abbassare il livello di lettura di un testo o di renderlo comprensibile a tutti. Attiva anche quando il problema descritto è che "non si capisce", "è troppo complicato", "è scritto difficile", "la gente non lo legge".
---

# Testo semplice — traduzione a intervento minimo

Questa skill prende un testo qualsiasi — di qualsiasi lunghezza, di qualsiasi tipo — e ne abbassa il livello di lettura fino a quello di un bambino di quinta elementare.

**Non è una riscrittura. È una traduzione.** Il testo di arrivo deve dire *esattamente* le stesse cose del testo di partenza, nello stesso ordine, con la stessa struttura, con la stessa completezza e con lo stesso tono. Cambia una cosa sola: **quanto è difficile leggerlo.**

Questo mette due vincoli in tensione, ed è tutta qui la difficoltà del lavoro:

| | |
|---|---|
| **Massima semplicità** | Ogni frase deve essere comprensibile a un bambino di 10 anni |
| **Minimo intervento** | Non si tocca niente che non sia necessario toccare |

Chi tiene solo il primo produce un testo semplice che dice altro. Chi tiene solo il secondo produce un testo fedele che resta difficile. **Servono entrambi, e il secondo è quello che si perde più facilmente.**

---

## VINCOLO ASSOLUTO — l'equivalenza informativa

**Ogni informazione presente nell'originale deve essere presente nel risultato. Nessuna informazione nuova può comparire.**

Tre parti, nessuna negoziabile:

1. **Niente si perde.** Nessun taglio, nessun riassunto, nessuna sintesi. Se una frase è lunga si spezza in tre frasi, non si accorcia. **Semplificare non vuol dire abbreviare:** un testo semplificato è spesso *più lungo* dell'originale, perché le frasi corte occupano più spazio delle frasi dense.
2. **Niente si aggiunge.** Non si spiegano cose che l'originale dava per scontate, non si aggiungono esempi, non si commenta. L'unica aggiunta permessa è la spiegazione minima di un termine tecnico che non si può eliminare — e va tenuta dentro la frase, non in una nota.
3. **Niente cambia di grado.** *Può* non diventa *deve*. *Spesso* non diventa *sempre*. *Alcuni* non diventa *tutti*. Vedi la sezione sulle sfumature: è il punto in cui questo lavoro fa i danni peggiori.

**Test di controllo — la lista dei fatti.** Prima di consegnare, elenca ogni affermazione dell'originale e verifica che ci sia nel risultato. Se il numero di affermazioni cambia, hai riassunto o hai aggiunto. Entrambe le cose sono errori, non miglioramenti.

---

## Che cosa vuol dire "quinta elementare", in numeri

Non è un'impressione. È misurabile, e va misurato.

| Parametro | Obiettivo | Come si verifica |
|---|---|---|
| **Indice Gulpease** | **≥ 80** | `scripts/gulpease.py` |
| **Lunghezza media delle frasi** | **12-15 parole** | idem |
| **Frase più lunga** | **max 25 parole** | idem |
| **Parole fuori dal Vocabolario di Base** | **< 5%** | controllo manuale + `references/lessico-sostituzioni.md` |
| **Subordinate per periodo** | **max 1** | lettura |
| **Idee per frase** | **1** | lettura |

**L'indice Gulpease** (Lucisano e Piemontese, 1988) è l'unico indice di leggibilità costruito sulla lingua italiana, e non sull'inglese tradotto. Formula: `89 + (300 × frasi − 10 × lettere) / parole`. Scala 0-100.

- **sotto 40** → difficile anche per chi ha un diploma superiore
- **40-60** → accessibile con un diploma superiore
- **60-80** → accessibile con la licenza media
- **80-100** → **accessibile con la licenza elementare** ← il bersaglio

**Il Vocabolario di Base** (Tullio De Mauro) sono le circa 7.000 parole che un italiano con istruzione obbligatoria conosce con certezza. Si divide in *fondamentale* (~2.000 parole, il nucleo assoluto), *alto uso* (~2.900) e *alta disponibilità* (~1.900: parole comuni ma legate a oggetti concreti, come *forchetta* o *cuscino*). **Per la quinta elementare si punta al fondamentale**, si accetta l'alto uso, si usa il resto solo quando serve davvero.

**Esegui sempre lo script prima e dopo.** Un numero prima e un numero dopo sono l'unica prova che il lavoro è stato fatto:

```bash
python3 scripts/gulpease.py testo.txt
```

---

## La scala di intervento — il protocollo del minimo

Si lavora **frase per frase**, mai a paragrafi. Su ogni frase si parte dal livello 0 e si sale **solo se il livello precedente non basta**.

| Livello | Intervento | Quando fermarsi qui |
|---|---|---|
| **0** | **Non toccare** | La frase è già leggibile da un bambino di 10 anni |
| **1** | **Sostituire parole** | Il problema sono solo alcune parole difficili |
| **2** | **Spezzare la frase** | La frase è troppo lunga ma le parole vanno bene |
| **3** | **Riordinare** | Le informazioni ci sono ma l'ordine le rende difficili |
| **4** | **Riscrivere la frase** | Nessuno dei livelli precedenti basta |

**Regola di ferro:** il livello 4 su più del 20% delle frasi vuol dire che stai riscrivendo il testo, non semplificandolo. Fermati e ricomincia dal livello 1.

**Il livello 0 è un livello vero.** In un testo normale, tra il 30% e il 50% delle frasi non ha bisogno di niente. Toccarle comunque — per uniformità, per gusto, per "migliorarle" — è il modo più comune di rompere questo lavoro. Se una frase funziona, si lascia com'è, anche se tu l'avresti scritta diversamente.

---

## Che cosa non si tocca mai

Sono intoccabili. Passano nel testo nuovo identici, carattere per carattere.

- **Numeri, date, orari, prezzi, percentuali, misure.** Anche il formato: 41 € resta 41 €.
- **Nomi propri**: persone, aziende, marchi, prodotti, luoghi, vie.
- **Citazioni e testimonianze** tra virgolette. Le parole di un'altra persona non si semplificano.
- **Dati di contatto**: telefono, mail, indirizzi, link, orari.
- **Termini legali obbligatori** e formule di legge. Se una parola ha valore giuridico, resta, e semmai si spiega accanto.
- **Nomi di malattie, farmaci, esami, procedure.** Restano, e si spiegano accanto la prima volta.
- **La struttura**: titoli, sottotitoli, elenchi, ordine dei paragrafi, grassetti, a capo, formattazione.
- **Le call to action** e le condizioni di un'offerta.

---

## Le sfumature che non si perdono

**È la parte più pericolosa del lavoro.** Semplificando si tende ad "arrotondare", e arrotondare cambia il significato. In ambito sanitario, legale e finanziario può essere un danno serio.

Queste categorie di parole si semplificano **solo con un equivalente dello stesso grado**:

| Categoria | Nell'originale | Semplificato SÌ | Semplificato NO |
|---|---|---|---|
| **Possibilità** | può, potrebbe, è possibile | può | riesce a, fa |
| **Frequenza** | spesso, a volte, di solito, raramente | quasi sempre, a volte | sempre, mai |
| **Quantità** | alcuni, molti, la maggior parte | alcuni, quasi tutti | tutti |
| **Obbligo** | deve, è tenuto a | deve | è meglio che |
| **Condizione** | se, salvo, a patto che, tranne | solo se, ma non quando | *(togliere la condizione)* |
| **Causa incerta** | sembra, risulta, si ritiene | sembra, pare | è |
| **Approssimazione** | circa, fino a, in media | circa, al massimo | esatto |

**Regola pratica:** ogni parola che indica *quanto*, *quanto spesso*, *se* o *quanto è sicuro* è un dato, non uno stile. Si tratta come un numero: non si tocca, o si sostituisce con un equivalente esatto.

---

## Semplice non vuol dire infantile

L'errore più frequente, e il più facile da fare senza accorgersene. Il bersaglio è il **livello di lettura** di un bambino di quinta, non il **tono** con cui si parla a un bambino.

Chi legge resta un adulto. Va rispettato come tale.

| Sì | No |
|---|---|
| Frasi corte | Frasi da libro illustrato |
| Parole comuni | Parole vezzeggiative o buffe |
| Ordine chiaro | Tono da maestra |
| *"Il collo fa fatica a girare."* | *"Ehi! Il tuo collino è un po' bloccato!"* |
| Zero gergo | Zero esclamativi in più |

**Non si aggiungono:** punti esclamativi, emoji, domande retoriche, "ciao!", incoraggiamenti, faccine, "facilissimo!", diminutivi. Se non c'erano nell'originale, non entrano.

**E non si cambia il registro.** Se l'originale dà del *lei*, il risultato dà del *lei*. Se è formale, resta formale — un testo può essere formale e semplice insieme, e quasi sempre è quello che serve.

---

## Workflow — sempre in questo ordine

### Passo 1 — Misurare l'originale

Salva il testo in un file ed esegui:

```bash
python3 scripts/gulpease.py originale.txt
```

Annota: Gulpease, lunghezza media delle frasi, la frase più lunga, le parole difficili segnalate. **Questo è il tuo punto di partenza e lo mostrerai all'utente.**

### Passo 2 — Fare la lista dei fatti

Elenca ogni affermazione dell'originale, in ordine, in forma brevissima. Su un testo lungo, una riga per paragrafo. Serve a due cose: è il tuo controllo di equivalenza alla fine, ed è ciò che ti impedisce di riassumere senza accorgertene.

Segna anche gli **intoccabili** che hai trovato (numeri, nomi, citazioni, termini tecnici obbligatori).

### Passo 3 — Passare frase per frase con la scala

Per ogni frase, dal livello 0 al 4, fermandoti al primo livello che basta. Vedi `references/regole-sintassi.md` per le trasformazioni sintattiche e `references/lessico-sostituzioni.md` per il dizionario delle sostituzioni.

Ordine di attacco dentro la frase, sempre questo:
1. **Le parole** (livello 1) — è ciò che risolve la maggior parte dei casi
2. **La lunghezza** (livello 2) — spezzare dove c'è già una virgola o un "che"
3. **La forma** — passivo → attivo, negazione doppia → affermazione, nominalizzazione → verbo
4. **L'ordine** (livello 3) — soggetto, verbo, complemento
5. **La riscrittura** (livello 4) — solo se il resto non è bastato

### Passo 4 — Misurare il risultato

Ri-esegui lo script. Se il Gulpease non è ≥ 80, guarda le frasi più lunghe: quasi sempre il punteggio è tenuto giù da tre o quattro periodi, non da tutto il testo.

### Passo 5 — Verificare l'equivalenza

Riprendi la lista dei fatti del Passo 2 e spunta ogni voce sul testo nuovo.

- Manca qualcosa? Hai riassunto. **Rimettilo.**
- C'è qualcosa in più? Hai spiegato. **Toglilo.**
- Una sfumatura è cambiata di grado? **Ripristinala.**

Poi passa la checklist in `references/verifica-e-metriche.md`.

### Passo 6 — Consegnare

```
## MISURA

| | Prima | Dopo |
|---|---|---|
| Gulpease | [n] | [n] |
| Parole per frase (media) | [n] | [n] |
| Frase più lunga | [n] parole | [n] parole |
| Frasi toccate | — | [n] su [tot] ([%]) |

## TESTO SEMPLIFICATO

[il testo completo, con la stessa struttura dell'originale]

## COSA HO CAMBIATO
[le trasformazioni principali per categoria, non frase per frase]

## COSA HO LASCIATO COM'ERA
[gli intoccabili, e le frasi già leggibili — con il conteggio]

## DA CONTROLLARE
[termini tecnici che non si potevano togliere, punti dove la semplificazione
 rischiava di cambiare il senso e come li hai risolti]
```

---

## Casi particolari

- **Testo molto lungo** (oltre ~3.000 parole): lavora a blocchi, misura ogni blocco, e mantieni un glossario delle scelte fatte — la stessa parola difficile va sostituita sempre allo stesso modo in tutto il testo.
- **Testo di marketing**: la semplificazione tocca la lingua, **non la persuasione**. Ganci, promesse, ordine degli argomenti e call to action restano dove sono. Un'headline si semplifica come tutto il resto, ma non si spegne.
- **Testo tecnico o medico**: il termine tecnico resta e si spiega accanto, dentro la stessa frase. *"Il rachide cervicale"* → *"il rachide cervicale, cioè il collo"*. Mai toglierlo e basta: quel termine può servire alla persona per cercare, per parlare col medico, per riconoscerlo su un referto.
- **Testo legale o contrattuale**: **non si semplifica il testo con valore legale.** Si può affiancare una versione semplice, dichiarata come spiegazione e non sostitutiva. Dillo esplicitamente all'utente.
- **L'utente chiede un livello diverso** (terza media, adulto poco scolarizzato, bambino più piccolo): cambia solo il bersaglio numerico. Terza media = Gulpease ≥ 60, frasi 15-20 parole. Il metodo resta identico.

---

## Vincoli — non sono opzionali

- **Mai riassumere.** Se il testo diventa più corto in modo significativo, hai tagliato qualcosa. Controlla cosa.
- **Mai cambiare un grado, una condizione o una quantità.** Sono dati.
- **Mai togliere una condizione o un'eccezione** perché complica la frase. Si spezza in una frase a sé.
- **Mai togliere un termine tecnico obbligatorio.** Si spiega, non si sostituisce.
- **Mai infantilizzare.** Il lettore è un adulto con poca dimestichezza col testo scritto, non un bambino.
- **Mai semplificare le parole di un'altra persona** dentro una citazione.
- **In ambito sanitario, legale e finanziario**: se una semplificazione può cambiare cosa la persona farà, non è una semplificazione. Segnalala all'utente invece di deciderla da solo.

---

## Riferimenti

- `references/lessico-sostituzioni.md` — il dizionario delle sostituzioni: burocratese, marketing, medichese, latinismi, connettivi, verbi vuoti. **Leggilo al Passo 3.**
- `references/regole-sintassi.md` — le trasformazioni sintattiche dell'italiano, una per una, con esempi prima/dopo. **Leggilo al Passo 3.**
- `references/verifica-e-metriche.md` — Gulpease, checklist di equivalenza, anti-pattern, come si sbaglia questo lavoro. **Leggilo al Passo 5.**
- `scripts/gulpease.py` — misura Gulpease, lunghezza delle frasi, parole lunghe e frasi critiche. **Passi 1 e 4.**

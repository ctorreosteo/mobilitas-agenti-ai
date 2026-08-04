# Come si usa il sistema di revisione

## Le lenti, organizzate su cinque livelli

Il panel non è fisso: **quali skill rivedono, e a che livello, lo decide il manifesto** `bibbie-generate/_dati/livelli.json`.

| Skill | Liv. | Cosa attacca | La sua domanda |
|---|---|---|---|
| `specialista` | 1 | Storia naturale omessa, red flag, definizione superata, etichette troppo alte | *È corretto per questa condizione?* |
| `medico-generale` | 1 | Comorbilità, politerapia, ritardo diagnostico, invii | *Il mio paziente torna più sicuro o più a rischio?* |
| `sicurezza-tecniche` | 1 | Il pericolo dichiarato come conoscenza: cosa la Bibbia non avverte | *Chi ha letto solo questo, sa dove può far male?* |
| `fisioterapista-ebp` | 1 | Audit delle etichette, meccanismo spacciato per prova, citazioni fasulle | *Quale affermazione non sopravvive a 10 minuti su PubMed?* |
| `compliance` | 1 | Promesse, farmaci, scope, dati sanitari | *Cosa espone lo studio?* |
| `neolaureato` | 1 | Comprensibilità: cosa non si capisce alla prima lettura | *Quale frase ho dovuto rileggere?* |
| `sistema-dominante` | 1 | Il ragionamento del Motore Clinico: gerarchia, causa vs sintomo | *Insegna a trovare la causa o a rincorrere il sintomo?* |
| `modelli` | 1 | Uso e bilanciamento dei cinque modelli | *Quale modello è gonfiato, quale manca?* |
| `neuromodulazione` | 1 | Il meccanismo neurofisiologico invocato | *Il meccanismo è quello giusto, con tempi plausibili?* |
| `clinico-esperto` | 1 | Utilità reale della teoria | *Chi legge questo risolve il caso in poche sedute?* |
| `fedelta-bibbia` | 2 | Audit meccanico contro `architettura-bibbia.md` | *Ogni pezzo dello standard è presente e al posto giusto?* |
| `apprendimento` | 3 | La sequenza che insegna | *Il documento insegna o fa solo sapere?* |
| `editor` | 4 | Ridondanza e lunghezza | *Cosa si toglie senza perdere sostanza?* |
| `chiarezza` | 5 | **Riscrive tutto da capo, in chiaro** | *Un neolaureato la legge senza rileggere una frase?* |
| `collaudo` | **cancello** | **Conservazione**: v5 contro v6, script + semantica | *Cambiando tutte le parole, è cambiata qualche cosa detta?* |

Le lenti divergono per **tipo di attacco**, non per mestiere. È il motivo per cui sono queste e non venti.

Le coppie che sembrano vicine **non** sono duplicati:

- **Specialista vs medico generale** — il primo guarda **la condizione**, il secondo **la persona**.
- **Sistema-dominante vs fedelta-bibbia** — stesso dominio (il metodo), controlli opposti: il primo giudica la **logica**, il secondo fa un **audit testuale**.
- **Modelli vs fedelta-bibbia** — il primo giudica **come** i modelli sono usati, il secondo che **ci siano tutti** con la loro etichetta.
- **Neolaureato vs chiarezza** — il neolaureato **segnala** cosa non si capisce, in mezzo agli altri rilievi di contenuto; `chiarezza` **riscrive tutto**, alla fine, quando il contenuto è chiuso. Il primo è diagnosi, il secondo è cura.
- **Editor vs chiarezza** — l'editor **toglie** ciò che è ripetuto, senza toccare come è scritto il resto; `chiarezza` **riformula** ogni frase, senza togliere informazione. Uno accorcia, l'altro semplifica. Devono girare in quest'ordine: si semplifica un testo già asciutto, non si asciuga un testo già semplificato — l'asciugatura ri-comprimerebbe le frasi e annullerebbe il lavoro.

## Il flusso

Il ruolo di ogni skill è dichiarato in `bibbie-generate/_dati/livelli.json`, con le **chiavi** = la parte dopo `direttore-osteopatico-`. L'**esistenza** delle skill è auto-scoperta dalla cartella; il manifesto decide solo il livello. Una skill non elencata **non viene usata** (il workflow lo segnala).

1. **Draft (v1)** — l'autore redige Bibbia + Mappa.
2. **1º livello** — tutti i revisori di `primo_livello` attaccano la v1 **in parallelo**, ciascuno in contesto pulito.
3. **Sintesi v2** — l'autore pesa i feedback e riscrive.
4. **2º livello** — `fedelta-bibbia` audita la v2 → **sintesi v3**.
5. **3º livello** — `apprendimento` guarda la v3 come percorso didattico → **sintesi v4**.
6. **4º livello** — `editor` produce una mappa di taglio sulla v4 → **sintesi v5**.
7. **5º livello** — `chiarezza` **riscrive integralmente la v5** → **v6**.
8. **Cancello** — `collaudo` verifica che la riscrittura non abbia perso niente → **v6 consegnabile**.

Il quinto livello non è un revisore che consiglia: è un riscrittore che produce il deliverable. Non emette rilievi da pesare, emette il documento.

## Il cancello: perché la riscrittura va collaudata

La riscrittura integrale è il punto più pericoloso della catena, per una ragione strutturale: **è l'unico passaggio in cui ogni singola frase del documento cambia**. Tutti gli altri livelli producono rilievi puntuali su un testo che resta; questo produce un testo nuovo. Fino a ieri era anche l'unico passaggio che nessuno verificava — il documento consegnato era l'unica versione mai controllata, e l'unica garanzia era che il riscrittore dichiarasse da sé di non aver perso niente.

`collaudo` **non è un sesto revisore.** Non giudica la qualità: quella ha già avuto quattordici risposte ed è chiusa. Verifica la sola **conservazione** — che cambiando tutte le parole non sia cambiata nessuna cosa detta. Un collaudatore che apre rilievi nuovi riapre decisioni chiuse e fa ripartire un ciclo finito: è rotto, non severo.

Gira in due strati, e la divisione è deliberata:

- **Lo script `verifica_conservazione.py`.** Conta etichette, PMID, percentuali e misure, titoli, aperture, chiusure, bullet, colonne di tabella, delta di lunghezza, glossario, script al paziente, e cerca materiale operativo o promesse introdotte. È deterministico: **non può illudersi di aver controllato**, che è il difetto tipico di un revisore-modello messo a fare un compito di conteggio.
- **Il collaudatore semantico.** Cerca ciò che nessun conteggio vede: un'etichetta rimasta ma riancorata a un altro claim, due frasi diventate una che sembra completa, una qualificazione caduta, un verbo irrigidito, un numero riattribuito a un altro studio.

Quasi tutti i controlli sono **differenziali** (v5 contro v6), non assoluti: verificano che le due versioni dicano le stesse cose, senza dover sapere come è formattato il documento.

**Cosa succede quando trova qualcosa.** Fino a due giri di **riparazione chirurgica**: il riscrittore rimette le voci mancanti con il lessico della v6, toccando solo quelle righe. Se le perdite sono diffuse, il sistema **scarta la riscrittura e consegna la v5** — meno scorrevole, ma accurata. Non è un ripiego improvvisato: è la gerarchia dichiarata più sotto, dove l'accuratezza sta al punto 2 e la leggibilità al punto 5.

## La regola di triage (livelli 1-4)

- **ERRORE** → si corregge. È falso, pericoloso, o insostenibile con prova alla mano.
- **RISCHIO** → si valuta. Regge ma è attaccabile.
- **PREFERENZA** → **si ignora di default.** È qui che muoiono i documenti.

**Il feedback si pesa, non si somma.** Dieci revisori producono dieci liste di "aggiungerei anche". Se le applichi tutte, la Bibbia passa da 9.000 a 20.000 parole e nessuno la legge più: hai distrutto il documento per proteggerlo.

Se dopo una revisione la Bibbia è cresciuta **oltre il 20%**, hai sommato invece di pesare. Torna indietro.

## Conflitti tra lenti

- **EBP contro tutti** — vince l'EBP sul **claim**: se non è provato, l'etichetta scende. Non vince sul contenuto: un meccanismo IPOTESI resta nella Bibbia, etichettato.
- **Compliance contro voce** — vince il compliance su ciò che **arriva al paziente** (Capitolo 12); il registro interno resta.
- **Neolaureato contro specialista** — "non si capisce" vs "va detto con precisione". Non è un conflitto: si dice la cosa precisa, in parole semplici, e il termine entra nel Glossario. **La precisione non richiede periodi lunghi.**
- **Lenti-metodo (sistema-dominante, fedelta-bibbia, modelli) contro EBP/compliance** — pretendono **struttura e ragionamento**, non prove: si applicano entrambi i piani. L'elemento di metodo entra, etichettato RAGIONAMENTO.
- **Apprendimento contro editor** — l'apprendimento può chiedere righe in più, l'editor le toglie. È voluto: l'apprendimento gira **prima**, e i passaggi che marca *da proteggere* l'editor può classificarli al massimo come PREFERENZA.
- **Editor contro chiarezza** — non si incontrano mai, perché girano in sequenza. Se `chiarezza` allunga il documento riformulandolo, **è ammesso fino al +10%**: semplificare costa parole. Oltre, ha aggiunto contenuto e ha sbagliato mestiere.

## Quando il metodo stesso è sbagliato

Esiste un caso che non si compone:

> **Un elemento prescritto dall'architettura interna è contraddetto dalla fisiologia o dall'evidenza.**

**La gerarchia. Quando due piani confliggono davvero, vince quello più in alto:**

1. **Sicurezza del paziente.** Non si negozia con nulla.
2. **Accuratezza fisiologica e dell'evidenza.** **Batte la fedeltà al metodo interno.**
3. **Compliance legale e deontologica.** Governa *ciò che si promette*, non *ciò che è vero*.
4. **Fedeltà all'architettura del metodo.**
5. **Leggibilità.**
6. **Preferenze editoriali e di voce.**

> Nota sul punto 5: la leggibilità sta **sotto** l'accuratezza, non sopra. Non si semplifica al prezzo di dire una cosa falsa. Ma quasi sempre non serve: una cosa vera si può dire in parole semplici. Se `chiarezza` non ci riesce, il problema è che il concetto non era chiaro nemmeno all'autore.

**Cosa fa il direttore quando scatta il punto 2:**

1. **Corregge la Bibbia.** La versione corretta è quella accurata, non quella fedele.
2. **Dichiara la deviazione**, non la nasconde.
3. **Apre una voce in `bibbie-generate/_dati/deviazioni-dal-metodo.md`** con stato `PROPOSTA` e la fonte. Una deviazione senza fonte si scarta.
4. **Non modifica i documenti di metodo.** La ratifica è umana.

Questa regola **non** è una licenza per riscrivere il metodo ogni volta che una lente storce il naso. Scatta solo quando l'elemento è **fattualmente contraddetto** da una fonte verificabile.

## Revisione manuale, in chat

Quando non usi il workflow:

1. **Una chat nuova per ogni lente, possibilmente fuori dal progetto.** Un'istanza che non ha scritto la Bibbia è molto più severa.
2. **Allega il documento** e invoca la lente **con lo slash** (`/direttore-osteopatico-...`).
3. **Non dire chi l'ha scritta.** Il revisore deve trovare i problemi, non compiacere.
4. **Non discutere il verdetto nella stessa chat.** Prendi l'output e chiudi.
5. **Rispetta l'ordine dei cinque livelli.** In particolare: `chiarezza` per ultimo, sempre, su un documento già asciugato.

## Il tetto di questo sistema

Più istanze dello stesso modello condividono gli stessi priori. Il contesto pulito elimina il bias dell'autore, non i punti ciechi del modello. Il valore reale sta nel **mandato di ricerca**.

I revisori veri restano gli umani. Questo sistema serve a **far arrivare al revisore umano un documento già ripulito**, non a sostituirlo.

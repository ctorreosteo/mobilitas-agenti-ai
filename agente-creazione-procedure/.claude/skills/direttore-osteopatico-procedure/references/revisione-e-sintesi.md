# Come si usa il sistema di revisione

## Le 11 lenti, organizzate su tre livelli

Il panel non è più fisso: **quali skill rivedono, e a che livello, lo decide un manifesto** — `procedure-generate/_dati/livelli.json`. Le lenti oggi sono undici, distribuite su tre livelli.

| Skill | Livello | Cosa attacca | La sua domanda |
|---|---|---|---|
| `direttore-osteopatico-specialista` | 1 | Sconfinamento diagnostico, red flag, linee guida, evidenza gonfiata | *È corretto per questa condizione?* |
| `direttore-osteopatico-medico-generale` | 1 | Comorbilità, politerapia, controindicazioni, ritardo diagnostico, invii | *Il mio paziente torna più sicuro o più a rischio?* |
| `direttore-osteopatico-sicurezza-tecniche` | 1 | Eventi avversi del gesto, screening pre-manovra, stop-rule, dose di forza | *La manovra può far male con le mani, così com'è scritta?* |
| `direttore-osteopatico-fisioterapista-ebp` | 1 | Claim senza supporto, meccanismo spacciato per prova, citazioni fasulle | *Quale affermazione non sopravvive a 10 minuti su PubMed?* |
| `direttore-osteopatico-compliance` | 1 | Promesse, farmaci, scope, red flag, dati sanitari | *Cosa espone lo studio?* |
| `direttore-osteopatico-neolaureato` | 1 | Istruzioni non eseguibili, dosi assenti, punti decisionali mancanti | *Cosa non riesco a fare lunedì mattina?* |
| `direttore-osteopatico-sistema-dominante` | 1 | Ragionamento del Motore Clinico: modello dominante, gerarchia, causa vs sintomo (CC/CP) | *Sta trattando la lesione primaria o rincorre il sintomo?* |
| `direttore-osteopatico-modelli` | 1 | Uso e bilanciamento dei cinque modelli osteopatici; cosa eliminare/ribilanciare | *Quale modello domina, quale manca, cosa è gonfiato?* |
| `direttore-osteopatico-clinico-esperto` | 1 | Risultato clinico reale: la guida fa guarire o è solo difendibile; completezza dell'arsenale efficace | *Il paziente migliora davvero seguendo questa procedura?* |
| `direttore-osteopatico-fedelta-bibbia` | 2 | Audit meccanico elemento-per-elemento contro l'architettura (cinque modelli + Motore Clinico) | *Ogni pezzo dello standard è presente, al posto giusto, non inventato?* |
| `direttore-osteopatico-editor` | 3 | Asciugatura: ridondanza e lunghezza; mappa di taglio (INTOCCABILE = sicurezza/dosi/evidenza/voce) | *Cosa si può togliere senza perdere sostanza né voce?* |

Le otto lenti divergono per **tipo di attacco**, non per mestiere. È il motivo per cui sono otto e non venti: fisioterapista, kinesiologo e osteopata condividono lo stesso bacino di conoscenza e produrrebbero lo stesso feedback con parole diverse.

Le coppie che sembrano vicine **non** sono duplicati:

- **Specialista vs medico generale**: il primo guarda **la condizione** ("è corretto?"), il secondo guarda **la persona** ("è sicuro per il mio ottantenne in warfarin?"). Se li facessi entrambi "un medico", collasserebbero in uno.
- **Medico generale vs sicurezza-tecniche**: il MMG guarda la **fragilità sistemica del paziente** (una controindicazione cambia se cambia il paziente); sicurezza-tecniche guarda il **gesto in sé** (screening pre-manovra, stop-rule, dose di forza, evento avverso intra-seduta — resta identico su qualunque paziente). Regola: se il rilievo si sposta cambiando paziente è del MMG; se resta identico perché riguarda *come si esegue e cosa si sorveglia*, è di sicurezza-tecniche.
- **Sistema-dominante vs fedelta-bibbia**: stesso dominio (il metodo: cinque modelli + Motore Clinico), due controlli opposti. Il primo giudica la **logica** — la procedura ha davvero trovato il modello che sequestra il compenso, e tratta la causa? Il secondo fa un **audit testuale**: c'è la sezione X, è al posto giusto, non è stato inventato un elemento fuori standard? Uno può promuovere una procedura logicamente valida che la fedeltà boccia perché ha saltato un blocco previsto, e viceversa.
- **Modelli vs fedelta-bibbia**: entrambi guardano i cinque modelli, ma il primo giudica **come sono usati** (bilanciamento, cosa eliminare/ribilanciare) e può chiedere di potare; il secondo verifica solo che **ci siano tutti** con la loro evidenza dichiarata. Non è conflitto: il primo migliora l'uso, il secondo garantisce la completezza.

**Non aggiungere una lente "osteopata principiante":** è già `-neolaureato`, calibrato apposta come professionista competente che, quando si blocca, lo fa per colpa del documento. Renderlo più insicuro produrrebbe rumore (lacune sue) invece di segnale (buchi del documento).

## Configurazione dinamica: chi rivede, a che livello, quando

Il ruolo di ogni skill è dichiarato **esplicitamente** in `procedure-generate/_dati/livelli.json`. Si usano le **chiavi** = la parte dopo `direttore-osteopatico-` (es. `direttore-osteopatico-compliance` → `compliance`):

- `autore` — chi redige e sintetizza (di norma `procedure`).
- `primo_livello` — i revisori che attaccano la **prima bozza (v1)**.
- `secondo_livello` — i revisori che ricontrollano la **versione già riscritta (v2)** → produce la v3.
- `terzo_livello` — l'editor di asciugatura che gira **per ultimo, sulla v3 validata** → produce la v4 finale.

L'**esistenza** delle skill resta auto-scoperta dalla cartella `.claude/skills/`; il manifesto decide solo **il livello**. Una skill-revisore presente nella cartella ma non elencata in nessun livello **non viene usata** (il workflow lo segnala, così non ci sono cali silenziosi). Per spostare un revisore di livello — o toglierlo — si modifica **solo** questo file, niente codice.

Il flusso che ne consegue (lo esegue il workflow `genera-procedure.workflow.js`, ma è anche la logica da seguire a mano):

1. **Draft (v1)** — l'autore redige procedura + scheda.
2. **1º livello** — tutti i revisori di `primo_livello` attaccano la v1 **in parallelo**, ciascuno in contesto pulito.
3. **Sintesi intermedia (v2)** — l'autore pesa i feedback di 1º livello e riscrive.
4. **2º livello** — i revisori di `secondo_livello` ricontrollano la **v2** (non la v1: guardano il documento già indurito).
5. **Sintesi v3** — l'autore applica i feedback di 2º livello. Se `secondo_livello` è vuoto, la v2 è promossa a v3 senza riscrittura.
6. **3º livello** — l'editor di `terzo_livello` asciuga la **v3** (mappa di taglio, solo se necessario).
7. **Sintesi finale (v4)** — l'autore applica i tagli dell'editor e chiude. Se `terzo_livello` è vuoto, la v3 è la finale.

La configurazione attuale mette al **2º livello la sola `fedelta-bibbia`** (l'audit di fedeltà ha senso *dopo* che l'esterno ha rimodellato il documento) e al **3º livello il solo `editor`** (si asciuga per ultimo, sul documento già validato). Tutto il resto è 1º livello. È una scelta del manifesto, non una legge del sistema: si sposta un revisore di livello editando l'array.

## Procedura operativa (revisione manuale, in chat)

Quando non usi il workflow ma lanci le lenti a mano:

1. **Una chat nuova per ogni lente, possibilmente FUORI dal progetto.** È il punto centrale: un'istanza che non ha scritto la procedura, e non sa chi l'ha scritta, è molto più severa. Non usare la chat in cui la procedura è stata prodotta.
   **Attenzione ai file di progetto:** un documento caricato come file di progetto è visibile in *ogni* chat di quel progetto, e la lente rischia di revisionare quello invece del tuo allegato (è già successo due volte). Le skill ora contengono un vincolo esplicito che lo impedisce, ma girare fuori dal progetto elimina il problema alla radice.
2. **Allega la procedura** (il .docx o il markdown) e invoca la lente **con lo slash** (`/direttore-osteopatico-...`). Lo slash è il modo più sicuro: chiamando la lente per nome, nessun'altra skill può rubarle il turno.
3. **Non dire chi l'ha scritta**, non dire che è di Mobilitas, non chiedere "cosa ne pensi". Il revisore deve trovare i problemi, non compiacere.
4. **Non discutere il verdetto nella stessa chat.** Se ti metti a controbattere, l'istanza cede — è quello che fanno i modelli sotto pressione. Prendi l'output e chiudi.
5. **Rispetta i tre livelli anche a mano:** 1º livello sulla v1 → sintesi v2 → 2º livello sulla v2 → sintesi v3 → 3º livello (editor) sulla v3 → sintesi finale (v4).

## La regola di triage — la parte che protegge il documento

Ogni rilievo arriva classificato. La regola d'oro:

- **ERRORE** → si corregge. È falso, pericoloso, o insostenibile con prova alla mano.
- **RISCHIO** → si valuta. Regge ma è attaccabile: spesso basta un paragrafo che riconosca l'obiezione.
- **PREFERENZA** → **si ignora di default.** È qui che muoiono i documenti.

**Il feedback si pesa, non si somma.** Otto revisori producono otto liste di "aggiungerei anche...". Se le applichi tutte, la procedura passa da 5.300 a 12.000 parole e nessun osteopata la legge più: hai distrutto il documento per proteggerlo. Il direttore decide, i revisori consigliano.

Se dopo la revisione la procedura è **più lunga del 20%**, hai sommato invece di pesare. Torna indietro.

## Conflitti tra lenti

Succederà, ed è il segnale che il sistema funziona:

- **EBP contro Neolaureato**: "questa tecnica non ha evidenza" vs "questa tecnica è l'unica che so eseguire". Vince l'EBP sul *claim* (non scrivere che è provata), vince il neolaureato sull'*istruzione* (se resta, spiegala).
- **MMG contro Specialista**: "manca la lista controindicazioni" vs "i criteri sono corretti". Non è un conflitto: sono piani diversi, si applicano entrambi.
- **Compliance contro DNA editoriale**: "togli l'assertività" vs "senza assertività il team non legge". Vince il compliance solo su ciò che **arriva al paziente** (script, frasi da dire); il registro interno resta.
- **Specialista contro Fisioterapista**: se entrambi colpiscono lo stesso punto da direzioni diverse, quello è il vero difetto. Priorità massima.
- **Sicurezza-tecniche contro EBP/Neolaureato**: "questa manovra va ingabbiata con screening e stop-rule" vs "non ha evidenza" / "così non la eseguo lunedì". Non è conflitto: la sicurezza del gesto **non si negozia** con l'efficacia né con la comodità. Se la manovra resta, ci si mette lo screening e la stop-rule; se non regge alla sicurezza, si toglie la manovra, non il vincolo.
- **Sistema-dominante/Fedelta-bibbia/Modelli contro EBP/Compliance**: "manca l'elemento dell'architettura / il razionale sul modello dominante" vs "togli il claim non supportato". Le lenti-metodo pretendono **struttura e ragionamento**, non prove cliniche: si applicano entrambi i piani. Aggiungi l'elemento di metodo *e* smonta il claim — l'elemento di metodo si scrive come **ipotesi/ragionamento clinico**, non come efficacia dimostrata. Se le due si scontrano davvero (il metodo chiede di affermare ciò che l'evidenza vieta), **vince la compliance sul claim rivolto al paziente**; il metodo resta come cornice interna. È esattamente il "lucchetto della corazza": la struttura riconosciuta tiene solo se nessun claim è gonfiato.
- **Modelli vs Sistema-dominante — la parola "dominante" ha due metri diversi.** `modelli` sceglie il dominante **per evidenza/pertinenza** ("su cosa c'è più supporto per questa condizione"); `sistema-dominante` lo sceglie **per gerarchia di sopravvivenza** ("cosa sequestra il compenso e va toccato per primo"). Sullo stesso caso possono indicare modelli diversi, e **non è un conflitto**: rispondono a domande diverse. In vetrina (Parte 0) si dichiara l'evidenza per modello — metro di `modelli`; nel Motore Clinico si sceglie l'ordine d'azione — metro di `sistema-dominante`. Il direttore tiene entrambi: *su cosa c'è più supporto* e *cosa va toccato per primo* convivono.
- **Sistema-dominante contro MMG/Specialista**: "il sistema dominante qui è viscerale, tratta lì" vs "quella tecnica è a rischio su questo paziente". Vince la sicurezza sul *gesto* (controindicazione o cautela restano), vince il metodo sul *ragionamento* (l'ordine di comando resta corretto anche se la mano si ferma prima).

## Il tetto di questo sistema

Più istanze dello stesso modello, per quanto isolate, condividono gli stessi priori. Il contesto pulito elimina il bias dell'autore, non i punti ciechi del modello. Il valore reale sta nel **mandato di ricerca**: è cercando la letteratura critica che emerge ciò che nessuna simulazione produce. Le lenti-metodo (sistema-dominante, fedelta-bibbia) non ricercano letteratura ma proteggono la coerenza interna: sono un secondo tipo di garanzia, non lo stesso.

I revisori veri restano gli umani: il team, e — se possibile — uno specialista in carne e ossa. Questo sistema serve a **far arrivare al revisore umano un documento già ripulito**, non a sostituirlo.

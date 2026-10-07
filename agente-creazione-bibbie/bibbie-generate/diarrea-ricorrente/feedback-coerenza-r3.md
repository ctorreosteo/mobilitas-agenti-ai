# Feedback 3º livello — Coerenza interna (l'Ispettore delle Giunture)

**Documento revisionato:** `bibbie-generate/diarrea-ricorrente/v3-intermedia.md` (v3.0 intermedia, 25.414 parole), con `mappa-v3.md` come controprova.

LENTE: Coerenza interna — l'Ispettore delle Giunture
CONDIZIONE: Diarrea ricorrente

> **Nota sul formato.** Il mandato assegnato è la **coerenza**, e la SKILL della coerenza non ha sei fasi: ha **nove giunture**. La mappa qui sotto è quella delle nove giunture — è l'equivalente strutturale della mappa delle sei fasi, che appartiene al revisore *apprendimento*. Non ho inventato una rubrica per farla combaciare con un formato che non è il mio.

---

## LE NOVE GIUNTURE

| # | Giuntura | Esito | Nota |
|---|---|---|---|
| 1 | Ragionamento (C8) × Leve (C11) | **COERENTE** | Nessuna leva negata dal ragionamento. C8 attribuisce il distretto dorso-lombare/sacrale al **quinto** meccanismo e non al quarto, esattamente come C11; e non liquida l'attivazione ("è il bersaglio, non un capolinea"). È la giuntura che cede quasi sempre, e qui tiene. |
| 2 | Meccanismi (C5) × Leve (C11) | **INCOERENTE** | Il conteggio non torna: C11 dichiara "due meccanismi su sei ... sugli altri quattro", ma ha **cinque** sezioni di meccanismo e un solo meccanismo fuori portata. → ERRORE 2 |
| 3 | Meccanismi (C5) × Strumenti attivi (C12) | **DEBOLE** | Tutti e quattro gli strumenti agganciano un meccanismo per nome. Il **terzo meccanismo** (post-infettivo) non è agganciato da nessuno strumento e il silenzio non è dichiarato. → PREFERENZA 2 |
| 4 | Leve (C11) × Strumenti (seduta/ripetizione) | **COERENTE — ed è il punto più forte del documento** | Il DIMOSTRATO del respiro lento è tenuto alla pratica del paziente in C7, C8, C11, C12 e C14, senza una sola eccezione; il guadagno dell'attività fisica è attribuito all'allenamento, non alla tecnica. Nessuna Bibbia del corpus lo fa meglio. |
| 5 | Scienza (C10) × Etichette | **DEBOLE** | Regola del ponte quasi sempre rispettata (Laborde, Kaptchuk, Caldarella, Lembo, Horrocks portano il salto al punto d'uso). Due sfasamenti: la frase "non al cibo" di C6 contro l'Attenzione di C5 (→ ERRORE 4) e il ponte di Laborde monco in C11 rispetto a C7/C10/C12. |
| 6 | Limiti di campo (C9) × Cosa dire al paziente (C13) | **COERENTE** | La frase del GIALLO — *"il quadro intestinale va comunque inquadrato dal tuo medico, e nel frattempo io non aspetto"* — arriva allo script di C13 **con le stesse parole**. La convivenza reperto/inquadramento è detta al paziente ("Quello su cui lavoro è ... la componente meccanica che ho trovato"). I segni di disidratazione del consenso e dell'obiezione di C13 coincidono. |
| 7 | Gli slot «Perché ci sei tu», tutti e quindici in fila | **COERENTE** | Nessun dato ripetuto in due slot (Slattery solo in C6, Manabe solo in C2, Klem solo in C13, Horrocks solo in C14, Buffone solo in C10). **Cinque slot restringono** (C0, C1, C6, C8, C10): il documento non sta vendendo. Tutti hanno i tre elementi e il terzo non è generico. |
| 8 | Il lessico | **INCOERENTE (lieve)** | Nessuna variante di *marker* ("indicatore" = 0 occorrenze); *reperto disfunzionale*, *disfunzione somatica*, *sistema dominante* hanno una sola definizione ovunque. Ma il Glossario definisce **"fuori piano"** mentre il testo dice sempre **"fuori modello"** (→ RISCHIO 3), e **"compenso"** è definito due volte e non usato mai (→ PREFERENZA 1). |
| 9 | Sottotipi (C6) × Leve (C11) × Triage (C9) | **INCOERENTE** | Il pattern "Acidi biliari" si riconosce in C6 dalla risposta alla loperamide, che C5, C8 e il Glossario dichiarano esplicitamente **non** essere il segno (→ ERRORE 1); e la colonna "Niente — invio" della tabella dei pattern non parla la lingua del cancello, dove due dei tre cancelli restano **GIALLO** e non uscite (→ RISCHIO 1). |

---

## ERRORI — il documento afferma due cose incompatibili

### ERRORE 1 — Giuntura 9 · Il segno che riconosce il pattern degli acidi biliari
**Capitolo 6** (tabella dei pattern): *"Acidi biliari | Feci acquose, **ottima risposta alla loperamide**"*, e in prosa: *"Lo distingue dagli altri la sproporzione fra risposta al farmaco e risposta alla dieta: migliora nettamente con la loperamide"*.
**Capitolo 5**, primo meccanismo: *"la loperamide non è il segno. Agisce sui recettori oppioidi intestinali: rallenta il transito in **qualunque** diarrea funzionale ... un farmaco aspecifico non può essere il segno specifico di un meccanismo"*.
Corroborano il Capitolo 5: **Capitolo 8**, Paziente B — *"lo riconosci dalle feci acquose e dall'anamnesi, **non dalla risposta al farmaco**"*; il **Glossario** — *"la risposta a questo farmaco, non alla loperamide, è quella che discrimina il primo meccanismo"*; la **mappa-v3**, che scrive già *"Feci acquose, diete inutili, test mai fatto"*.

**QUALE LATO CORREGGERE: il Capitolo 6.** *Perché:* è solo contro tre punti del documento più la mappa, ed è il lato non ancorato — C5 porta il ragionamento farmacologico, C8 l'applicazione, il Glossario la definizione. Ed è il lato che il lettore ha in mano quando sceglie il pattern.
*Come:* nella cella, `Feci acquose, ottima risposta alla loperamide` → `Feci acquose, diete inutili, test mai fatto` (allineamento alla mappa, 0 parole nette). In prosa, sostituire la frase sulla sproporzione con: *"Lo distinguono le feci acquose, l'anamnesi — colecistectomia, resezione ileale, vecchia radioterapia pelvica — e il fatto che nessuna dieta di esclusione abbia cambiato niente. La risposta alla loperamide non lo distingue: si comunica al curante, non apre il cancello."*
**Costo: +15 parole.**

### ERRORE 2 — Giuntura 2 · Il conteggio dei meccanismi senza leva
**Capitolo 11**, In una riga: *"su **due meccanismi su sei** le mani non hanno nulla da offrire ... sugli **altri quattro** il razionale esiste"*, ripetuto nella chiusura: *"Su due meccanismi su sei le mani non hanno nulla"*.
**Lo stesso Capitolo 11**, nel corpo: la sezione "Cosa non possono fare le mani" dichiara fuori portata **un solo meccanismo** (il primo, gli acidi biliari) — le altre due voci sono esiti, non meccanismi (transito colico, consistenza delle feci) — e seguono **cinque** sezioni di meccanismo con leva dichiarata (2, 3, 4, 5, 6).

**QUALE LATO CORREGGERE: la riga di apertura e la chiusura (il conteggio).** *Perché:* cinque sezioni sostanziali battono un numero riassuntivo; e il secondo meccanismo "senza nulla" non esiste da nessuna parte nel documento. Se il "due" voleva includere il quinto, va detto altrimenti: il quinto **una leva ce l'ha** (dorso-lombare e sacro), ciò che gli manca è il bersaglio — ed è già scritto nel corpo.
*Come:* `su un meccanismo su sei le mani non hanno nulla da offrire, e va detto per primo; sugli altri cinque il razionale esiste — su uno dei cinque con il bersaglio che manca — con etichette che vanno da IPOTESI a PROBABILE e mai oltre`. Stessa correzione nella chiusura.
**Costo: +8 parole** (spostamento di una clausola già presente nella sezione del quinto meccanismo).

### ERRORE 3 — Giuntura 4 · Quanti strumenti attivi sono tuoi
**Capitolo 12**, In una riga: *"una sola delle quattro è **interamente tua da insegnare**"*, ripetuto nella chiusura: *"Una sola — il respiro — è tua da insegnare"*.
**Capitolo 10**, tabella degli studi cardine: *"Johannesson 2011 | ... | **Insegnare e monitorare il movimento**"*. **Capitolo 11**, quinto meccanismo: *"la leva più forte che hai non è manuale: **è la spiegazione**"*. **Capitolo 12 stesso**, slot «Perché ci sei tu»: *"sei nella posizione di **insegnarle**, di monitorarle e di mandare la persona giusta a chi le eroga per intero"* — al plurale. E il quarto strumento del capitolo, *L'educazione al meccanismo*, è per definizione erogato da te.

**QUALE LATO CORREGGERE: il Capitolo 12 (apertura e chiusura).** *Perché:* è un conteggio contraddetto da tre punti d'uso, uno dei quali è nello stesso capitolo a quaranta righe di distanza. La distinzione vera del documento non è *insegnare* — è **erogare per intero**: una sola delle quattro (le terapie psicologiche) non è tua in nessuna forma.
*Come:* In una riga → *"su questa condizione le leve con le prove migliori non sono le tue mani: una delle quattro non è tua da erogare in nessuna forma, e nessuna delle altre tre è tua da fare al posto del paziente."* Chiusura → *"Una sola — le terapie psicologiche — non è tua da erogare. Il respiro è tuo da insegnare, e nemmeno quello è tuo da erogare sul lettino."*
**Costo: +10 parole.**

### ERRORE 4 — Giuntura 5 · «non al cibo» contro «non al menu»
**Capitolo 6**, tabella: *"Postprandiale | Urgenza legata all'orario, **non al cibo**"*.
**Capitolo 5**, quinto meccanismo, Attenzione: *"È vero che **l'identità dell'alimento non predice** ... **Non è vero che il pasto non c'entri: carico di grassi e volume hanno una via misurata verso l'urgenza**. Detta nella forma sbagliata, quella frase crolla il giorno in cui il paziente nota di stare peggio dopo i pasti grassi — e con lei crolli tu."* La prosa dello stesso Capitolo 6 scrive correttamente *"L'orologio comanda più del **menu**"*, e la mappa-v3 scrive *"Comanda l'orologio, non il **menu**"*.

**QUALE LATO CORREGGERE: la cella del Capitolo 6.** *Perché:* è il lato che il documento stesso dichiara pericoloso, e contraddice la prosa che gli sta sotto e la mappa che il lettore consulta prima del paziente.
*Come:* `non al cibo` → `non al menu`.
**Costo: 0 parole.**

---

## RISCHI — non si contraddicono, ma si sfasano

### RISCHIO 1 — Giuntura 9 · «Niente — invio» non è la lingua del cancello
**Cosa non combacia.** La tabella dei pattern (C6) marca tre pattern `Niente — invio`, e il capitolo li chiama *"uscite"*. Ma nel cancello (C9) solo **uno** dei tre è un'uscita vera (il pattern con bandiera rossa → ROSSO): gli acidi biliari mai indagati e la terapia mai rivista sono due delle **cinque forme di inquadramento incompleto**, cioè **GIALLO — "si lavora, in parallelo"**. C8, Paziente B, lo dice esplicitamente (*"se coesiste una lombalgia meccanica autonoma, quella la tratti"*), ma la tabella no — ed è la tabella che il lettore ha davanti col paziente.
**Cosa lo allineerebbe.** Una riga sotto la tabella di C6, con materiale già presente in C9: *"«Invio» qui non significa dimissione: solo il pattern con bandiera rossa è ROSSO. Acidi biliari e iatrogeno sono due delle cinque forme di inquadramento incompleto, cioè **GIALLO** — comunicazione scritta al curante mentre il paziente resta con te, sul tuo reperto."*
**Costo: +15 parole.** Capitolo ospite: **6**, subito dopo la tabella dei pattern.

### RISCHIO 2 — Giuntura 1 · La leva di Attali è ristretta in C8 e non al suo punto d'uso in C11
**Cosa non combacia.** C11, secondo meccanismo, dichiara la leva *"sul livello di attivazione generale ... non su un accesso diretto al retto"*, ma la sostiene con **PROBABILE** su Attali 2013, che è un **trattamento viscerale addominale**. C8 pone la restrizione: *"la leva di Attali non entra in nessuno dei tre pazienti-tipo ... poggia su un trattamento viscerale addominale, e questo documento tiene l'addome fuori dalle prime mosse. Se entra, entra dopo il VERDE e come tentativo dichiarato."* Chi legge C11 da solo — ed è il capitolo che si rilegge prima di una seduta — non trova quella restrizione da nessuna parte.
**Cosa lo allineerebbe.** Portare la clausola di C8 al punto d'uso, dentro il box del secondo meccanismo di C11: *"— e quel trattamento è viscerale addominale: non entra nelle prime mosse, entra dopo il VERDE e come tentativo dichiarato (vedi «Come ragiono davanti a questo paziente»)."* C8 la mantiene, perché lì serve al ragionamento sui tre pazienti.
**Costo: +20 parole.** Capitolo ospite: **11**, box «Quanto è solido» del secondo meccanismo.

### RISCHIO 3 — Giuntura 8 · Il Glossario definisce un termine che il testo non usa
**Cosa non combacia.** Il Glossario porta *"**Fuori distretto / fuori piano**"*, mentre il testo dice sempre *"fuori **modello**"* — in C8 nel corpo del terzo marker, in C8 nella chiusura «Le tre cose da ricordare» (intoccabile) e nella mappa-v3. La formula "fuori piano" non compare mai nel documento. Una parola, un significato: qui il significato ha due parole.
**Cosa lo allineerebbe.** Voce di Glossario: `Fuori distretto / fuori modello — un marker è fuori distretto se lo misuri lontano da dove hai lavorato, fuori modello se appartiene a un piano diverso da quello che hai trattato. Non sono la stessa cosa.` Vince il testo, perché la formula sta dentro una chiusura intoccabile e dentro la mappa.
**Costo: 0 parole** (una sostituzione di parola in due punti della voce).

---

## PREFERENZE (max 3)

### PREFERENZA 1 — «Compenso» è definito due volte e non lavora mai
Il termine ha un box Definizione in C5 e una voce di Glossario, e **non compare in nessun altro punto del documento**. È una definizione che non aggancia niente — il contrario del difetto abituale, ma sempre una giuntura vuota. Due strade, entrambe legittime: agganciarlo dove il documento lo sta già descrivendo senza nominarlo (sesto meccanismo, *"il guinzaglio che si accorcia"*, che è un compenso che costa il raggio di vita) con **+6 parole**; oppure togliere il box da C5 e lasciare la sola voce di Glossario (**−45 parole**). Preferisco la prima: il termine è canonico e vale la pena farlo lavorare una volta.

### PREFERENZA 2 — Giuntura 3 · Il terzo meccanismo non è agganciato da nessuno strumento attivo
Gli strumenti di C12 dichiarano il meccanismo su cui agiscono: 6º+4º, 2º+4º, 4º, 5º+6º+4º. Il **terzo** (la reattività lasciata dall'infezione) non compare, e il silenzio si legge come dimenticanza — mentre C11 dice che lì si agisce *"sul livello di attivazione ... e sulla componente di sorveglianza che quasi sempre si è aggiunta negli anni"*. Mezza riga nel primo strumento, presa da C11: *"e sul terzo, per la sorveglianza che vi si è aggiunta negli anni."* **Costo: +12 parole.** Capitolo ospite: **12**, strumento 1, riga «Su quale meccanismo agisce».

### PREFERENZA 3 — Giuntura 5 · Il rinvio mancante da C5 al contro-dato di Stabell
C5, secondo meccanismo, giustifica l'algometro sul trapezio (*"spiega perché il marker di verifica di questo documento è un algometro su un muscolo lontano"*) senza il contro-dato che C8 sviluppa per esteso — Stabell 2013, 4.689 persone, nessuna differenza **alla pressione**. Non è una contraddizione: C5 afferma di meno di quanto Stabell smentisca. Ma il lettore incontra il razionale del marker qui, e la sua limitazione trecento righe più avanti. Un rinvio di dodici parole: *"— con un limite che vale la pena leggere subito, in «Come ragiono davanti a questo paziente»."* **Costo: +12 parole.**

---

## PROPOSTA DI DECIMA GIUNTURA

**«Le tabelle riassuntive» × «la prosa che le sta sotto».** Tre dei quattro errori di questo giro stanno in una **cella di tabella** (C6: loperamide, C6: "non al cibo") o in un **conteggio riassuntivo** (C11: due su sei; C12: una su quattro), mai nella prosa. È strutturale: la sintesi riscrive i paragrafi e non rigenera la tabella o la riga di apertura che li riassume, perché sembrano metadato e non contenuto. **Merita un controllo fisso**: ogni cella di tabella e ogni conteggio ("due su sei", "una su quattro", "tre su otto") va riletto contro il paragrafo che descrive la stessa cosa. Nota di conferma: la **mappa-v3** era già corretta su entrambe le celle sbagliate di C6 — la mappa viene rigenerata, la tabella dentro il capitolo no.

---

## DA PROTEGGERE DALL'EDITOR (4º livello)

Queste ripetizioni **non** sono ridondanza: sono le giunture che tengono. Toglierne una riapre una contraddizione.

1. **Il DIMOSTRATO del respiro lento ripetuto cinque volte** — C7 (Respiratorio), C8 (Paziente A), C11 (quarto meccanismo), C12 (strumento 2), C14. È la difesa della giuntura 4 (seduta contro ripetizione), il difetto che gli osteopati sbagliano più spesso. Va detto in **tutti e cinque** i punti, perché in tutti e cinque un lettore potrebbe attribuire quel DIMOSTRATO alle proprie mani.
2. **«Non spinge di più, trattiene di meno»**, in C4, C5, C8, C13, C14. È il refrain didattico del documento e la frase-chiave dello script al paziente: la ripetizione è la funzione.
3. **La frase del GIALLO, verbatim in C9 e C13.** La giuntura 6 richiede che arrivi al paziente **con le stesse parole**. Se l'editor la varia per evitare la ripetizione, la convivenza smette di essere una convivenza.
4. **La doppia spiegazione «quattro settimane vs tre mesi»**, in C2 (Attenzione al tempo) e in C9 (Tre righe hanno bisogno di una ragione). Sono due punti d'uso diversi — la definizione e il triage — e la riga della tabella non verrà applicata senza la sua ragione accanto.
5. **«Fuori distretto, non fuori modello»**, in C8 nel corpo e in C8 nella chiusura, più la mappa. Sembra una ripetizione a otto righe di distanza: è la sola cosa che impedisce di leggere l'algometro come prova di dominanza.
6. **Il triplo sdoppiamento delle etichette in C11** (*"Sono tre oggetti diversi"*): tre righe che dicono quasi la stessa cosa con soggetti diversi. È esattamente ciò che impedisce alla leva più debole di ereditare l'etichetta della più forte.
7. **L'Attenzione «la loperamide non è il segno» in C5 e la voce di Glossario del sequestrante.** Sono due, e devono restare due: sono la ridondanza che rende sicura la correzione dell'ERRORE 1.

---

## BILANCIO PAROLE

| Rilievo | Parole |
|---|---|
| ERRORE 1 — pattern acidi biliari, C6 | +15 |
| ERRORE 2 — conteggio dei meccanismi, C11 | +8 |
| ERRORE 3 — conteggio degli strumenti, C12 | +10 |
| ERRORE 4 — «non al menu», C6 | 0 |
| RISCHIO 1 — «Invio» ≠ dimissione, C6 | +15 |
| RISCHIO 2 — restrizione di Attali al punto d'uso, C11 | +20 |
| RISCHIO 3 — «fuori modello» nel Glossario | 0 |
| PREFERENZA 1 — agganciare «compenso», C5 | +6 (o −45) |
| PREFERENZA 2 — terzo meccanismo in C12 | +12 |
| PREFERENZA 3 — rinvio a Stabell, C5 | +12 |
| **Totale** | **+98 parole** |

Su 25.414 parole: **crescita netta +0,39%**, contro un budget del 5%. Nessun rilievo aggiunge contenuto clinico: tutto è spostamento, allineamento o correzione di un conteggio. Accettando la seconda opzione della PREFERENZA 1 il bilancio diventa **+47 parole (+0,18%)**.

---

## TIENE

Le giunture che il metodo considera più fragili sono le più solide di questo documento. La **prima** — il capitolo del ragionamento che nega una leva dichiarata altrove — non cede da nessuna parte: C8 attribuisce la leva dorso-lombare/sacrale al quinto meccanismo e non al quarto, esattamente come C11, e non liquida l'attivazione ma la chiama *"il bersaglio, non un capolinea"*. La **quarta** — effetto della seduta contro effetto della ripetizione — è tenuta in cinque capitoli senza una sola eccezione, e non ho visto una Bibbia del corpus farlo meglio. La **sesta** arriva al paziente verbatim. La **settima**: quindici slot, nessun dato ripetuto, cinque che restringono.

**VERDETTO: Sfasato.**
Quattro contraddizioni reali, tutte in celle di tabella o in conteggi riassuntivi, nessuna nel ragionamento clinico: è il profilo di un documento la cui sostanza è stata sintetizzata bene e i cui metadati non sono stati rigenerati con lei. Si chiudono con 33 parole.

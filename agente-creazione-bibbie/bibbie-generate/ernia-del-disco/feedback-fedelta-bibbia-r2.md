# LENTE: Fedeltà all'Architettura della Bibbia — audit di completezza (2ª passata, 2º livello)

**CONDIZIONE:** Ernia del disco lombare
**DOCUMENTI REVISIONATI:** `bibbie-generate/ernia-del-disco/v2-intermedia.md` (19.627 parole totali, 16.760 di corpo) e `bibbie-generate/ernia-del-disco/mappa-v2.md`
**Registro deviazioni letto prima dell'audit:** `_dati/deviazioni-dal-metodo.md` — nessuna voce `RATIFICATA`, nessuna `RESPINTA`, tutte `PROPOSTA`.

---

## CHECKLIST DI FEDELTÀ

```
A. I quindici capitoli .................. PRESENTE — 0→14 + Appendici A e B, nell'ordine, funzioni
                                          rispettate. Titoli-domanda, non etichette.
B. Griglia formale ...................... PARZIALE — 15/15 «In una riga», 15/15 chiusure con esattamente
                                          quattro bullet, 15/15 slot «Perché ci sei tu» a tre elementi e
                                          con dato sempre diverso. Ma tre tipi di box inventati, celle
                                          di tabella oltre le 8 parole, cinque rimandi per numero.
C. Etichette di solidità (il lucchetto) . PARZIALE — quattro etichette e solo quelle, ogni meccanismo,
                                          modello e leva ne porta una, nessun claim gonfiato nel corpo.
                                          Ma un box con tre etichette e zero glosse, due etichette
                                          inline fuori box, alcuni numeri in prosa senza la riga «Per te».
D. I cinque modelli (cap. 7) ............ PRESENTE — cinque sezioni brevi, quattro voci ciascuna,
                                          etichetta propria, nessun modello inventato, scope del
                                          Metabolico dichiarato, restrizione del Respiratorio motivata.
E. Motore Clinico (cap. 8) .............. PARZIALE — punta/sommerso, principio di regolazione, chiave di
                                          volta, marker fuori piano, road map a sette passi, tre stati,
                                          etichetta RAGIONAMENTO: tutti presenti. Ma la clausola di
                                          precedenza nega una leva che i capitoli 11 e 12 dichiarano, e
                                          la soglia del marker principale sta sotto l'errore di misura.
F. Confine teoria/procedura ............. RISPETTATO — nessuna sequenza, nessuna dose, nessun piano di
                                          sedute; i parametri di studio sono al passato e attribuiti;
                                          chiusura obbligatoria del cap. 11 presente; entrambe le voci
                                          del cap. 12 chiudono con la formula di confine.
G. Fabbricazioni/contraddizioni ......... PRESENTI — la Mappa contraddice la Bibbia su otto punti;
                                          «il nervo che ha smesso di scorrere» nel cap. 14 contraddice
                                          i capitoli 5, 10 e 12.
H. Tre cerchi + «Quando la scienza tace»  PARZIALE — tre cerchi dichiarati e distinti, cinque punti di
                                          «Quando la scienza tace» tutti presenti e nell'ordine, regola
                                          del ponte applicata su Ezzatvar, Gordon, Janssens, Löken,
                                          Traeger. Manca su Zaccaro 2018.
H. Cap. 12 strumenti attivi (condiz.) ... PRESENTE — condizione di attivazione soddisfatta (PROBABILE
                                          forte: 20 studi controllati, 877 partecipanti). Sei voci
                                          rispettate su entrambi gli strumenti. Fuori peso: 992 parole.
H-bis. Il cancello d'ingresso ........... PARZIALE — tre uscite, mandato a due piani con entrambi i
                                          corollari, contrappeso attaccato al principio, quattro
                                          condizioni del GIALLO, scadenza del GIALLO, scadenza
                                          dell'inquadramento, vincolo di documentazione, perimetro
                                          legale solo specifico. Mancano la ragione dichiarata del
                                          triage e il rispetto del vocabolario chiuso dei tempi.
H. Cap. 14 «Cosa fare adesso» ........... PARZIALE — filo ricucito, tre cose (guardi / dici / smetti),
                                          chiusura nella voce che motiva, 346 parole nei tre blocchi,
                                          nessuna promessa di esito, nessun lessico da brochure.
                                          Ma contiene un'affermazione che il documento smentisce.
Mappa concettuale ....................... CONTRADDICE — non rigenerata: byte-identica alla v1.
```

---

## ERRORI — elemento obbligatorio ASSENTE, invertito o inventato

### 1. [G — Fabbricazioni/contraddizioni · Mappa concettuale] La Mappa non è stata rigenerata: è byte-identica alla v1 e contraddice la Bibbia v2 in otto punti

`mappa-v2.md` e `v1-mappa.md` hanno lo stesso MD5 (`a27090e1…`), 5.799 byte, e l'intestazione dice ancora **v1.0**. Il primo livello ha riscritto la Bibbia; la Mappa è rimasta indietro. È il deliverable che si guarda a sei mesi e prima di un paziente: **oggi consegna al lettore la versione smentita.**

| Blocco della Mappa | Cosa dice | Cosa dice la Bibbia v2 |
|---|---|---|
| 3 · meccanismi | «La radice non scorre più — IPOTESI» | «La radice diventa dolente a un'escursione normale — PROBABILE»; lo scorrimento è stato misurato ed è risultato **non** ridotto (Ridehalgh 2015) |
| 3 · meccanismi | «risponde al cortisone» come segno del primo meccanismo | «è un dato anamnestico utile, **non un segno che identifica il meccanismo**» (e Goldberg 2015: nessuna riduzione del dolore alla gamba) |
| 4 · sottotipi | sei sottotipi | sette: manca **Post-discectomia e recidiva**, quello che cambia la soglia dell'invio |
| 4 · sottotipi | «Meccanico da distribuzione: peggio a tosse» | «**Il dolore alla tosse non è un segno di questo piano**»: è meccanosensibilità radicolare |
| 5 · bandiere | «Febbre con dolore alla schiena» | l'assenza di febbre **non** esclude l'infezione spinale (triade completa in un caso su dieci); mancano massa pulsante, anticoagulato, deficit importante recente |
| 6 · road map | sei passi, ultimo «il nervo scorre?» | sette passi; manca «**la fase chimica è accesa?**», che è la clausola che sospende la regola del monte |
| 6 · marker | quattro marker, «il marker che decide … qui è il quarto» | cinque marker; e la regola corretta è «**nessun marker lo è per sempre: lo diventa in funzione di cosa hai deciso di trattare**» |
| 7 · strumenti attivi | «Restare attivi e caricare — **DIMOSTRATO** che funziona quanto il resto e **più del riposo**» | PROBABILE; e a lettera: «**Non si può dire "più del riposo"**» (Dahm 2010, nessuna differenza) |

In più il blocco «Perché ci sei tu» della Mappa è la **copia verbatim** dello slot del Capitolo 13 (Mathieson/Pinto), mentre lo standard chiede un blocco unico, il più forte dei quindici.

**Correzione.** Rigenerare la Mappa dalla v2, riga per riga sulle otto voci qui sopra, cambiare l'intestazione in v2.0, e sostituire il blocco «Perché ci sei tu» con quello più forte del documento (Chiu 70%/96%, oppure Santilli 55% contro 20%: entrambi più forti del dato sul pregabalin e nessuno dei due già speso in un capitolo che la Mappa riproduce).

### 2. [E — Motore Clinico · Capitolo 8] La clausola di precedenza nega una leva che «Perché le mani possono cambiare qualcosa» e «Cosa può fare il paziente da solo» dichiarano

Riga 574: *«la fase chimica attiva sospende quella regola. Finché è accesa la radice non è un piano trattabile, e chi mobilizza anca e nervo trova quello che il documento gli ha promesso — tutto identico entro ventiquattro ore.»*

È il caso che lo standard classifica come **CONTRADDICE, non come omissione**:

- il Capitolo 11 chiude con lo slot su **Santilli 2006** — 102 pazienti **acuti** con protrusione, 55% senza dolore irradiato contro 20% del simulato — e scrive *«questo ti autorizza a proporre la leva manuale nel quadro acuto senza deficit»*. Quei pazienti erano in fase chimica;
- il Capitolo 12 dichiara la **mobilizzazione neurale** PROBABILE su 20 studi controllati e scrive *«negli studi la mobilizzazione era parte del trattamento fin dall'inizio, non un'aggiunta finale»*.

Il Capitolo 8 dice al lettore, col paziente davanti, che nella fase in cui quel paziente arriva **la mobilizzazione di anca e nervo non produce niente**. Il lettore crede al capitolo che ha in mano.

**Correzione.** Riscrivere la clausola separando ciò che è vero da ciò che è falso: la fase chimica sposta la **priorità** e cambia il **criterio di risultato** (distanza del sintomo, non sparizione del dolore; effetto dentro la seduta, tendenza su settimane — cose che il documento già scrive tre righe sopra), **non** rende il piano intrattabile. La riga deve finire con quello che si fa, non con quello che non tiene, e rimandare per nome a «Perché le mani possono cambiare qualcosa».

### 3. [E — Motore Clinico · Capitolo 8, tabella dei marker · e Capitolo 11] La soglia del marker principale è fissata sotto l'errore di misura dello strumento

La tabella dei marker fissa il Lasègue ad «Almeno 10 gradi», e il Capitolo 11 usa lo stesso numero come criterio di smentita: *«se non si sposta di almeno dieci gradi, l'ipotesi era sbagliata»*.

Il registro contiene una voce trasversale aperta il **2026-08-19** proprio su questo (*«Il "re-test immediato" senza soglia di misura non è interpretabile»*, condizione di emersione: sciatalgia): la differenza minima davvero rilevabile sul SLR è fra **13 e 20 gradi**, e gli autori concludono che l'errore di misura *«probabilmente impedisce di usare l'escursione del SLR per le decisioni cliniche»* (Nee, Coppieters e Boyd, *Musculoskelet Sci Pract* 2022, [PMID 35245880](https://pubmed.ncbi.nlm.nih.gov/35245880/)). La Bibbia sorella fissa la soglia a **≥ 20°** e scrive *«un guadagno di dieci gradi non è un risultato, è rumore dello strumento»*.

La voce è in stato `PROPOSTA`, ma il dato che la regge è verificato e trasversale: una soglia sotto l'errore trasforma la prova della chiave di volta — elemento obbligatorio di questo capitolo — in un auto-inganno, cioè esattamente ciò che la regola esiste per impedire. **Qui vince l'accuratezza scientifica sulla convenzione interna.**

**Correzione.** Portare la soglia del Lasègue a **≥ 20°** in tutti e due i punti (tabella dei marker e criterio di smentita del Capitolo 11), con la riga che dichiara perché — l'errore di misura noto — e mantenere l'ottima scelta già fatta di misurare il **punto di comparsa del sintomo distale** e non l'escursione massima. Se il numero cambia, va cambiato anche nella Mappa rigenerata.

### 4. [G — Fabbricazioni/contraddizioni · Capitolo 14] «Il nervo che ha smesso di scorrere» contraddice tre capitoli, e sta nel capitolo che vieta il contenuto nuovo

Riga 957: *«nasce dalla chimica che tocca una radice mal protetta, **dal nervo che ha smesso di scorrere**, dal carico che anca, respiro e pancia hanno smesso di dividersi…»*

- Capitolo 5, meccanismo 3: *«L'idea che il nervo abbia smesso di scorrere è stata misurata nell'uomo ed è risultata negativa»* (Ridehalgh 2015). *«Alterata è la soglia, non la corsa.»*
- Capitolo 10, «Non possiamo dire»: *«Che modifichiamo lo scorrimento della radice: nessuno l'ha misurato.»*
- Capitolo 12: *«che agiscano migliorando lo scorrimento resta IPOTESI»*.

Il filo ricucito del Capitolo 14 è ciò che resta a sei mesi: qui restituisce al lettore **la versione che il documento ha appena smontato**.

**Correzione.** Sostituire con la formulazione già usata nel documento: *«dalla soglia della radice che si è abbassata»* — nessuna parola in più, e il capitolo torna a riassumere invece di reintrodurre.

---

## RISCHI — elemento PARZIALE

### 1. [B — Griglia formale] Tre tipi di box inventati oltre i quattro previsti

- riga 181 — `> **Chicca.**` (l'innervazione che cresce dentro il disco degenerato)
- riga 432 — `> **Condizioni spesso associate.**` (rimando alle Bibbie di lombalgia e gluteo profondo)
- riga 556 — `> **La regola del marker fuori piano, in forma corretta.**`

Lo standard ammette **solo** Definizione / Quanto è solido / Attenzione / Cosa cambia per te: la prevedibilità grafica è metà della leggibilità, e tre eccezioni la annullano.

**Correzione.** «Chicca» → prosa in corsivo dentro la struttura in tre righe (contenuto invariato, è una delle parti migliori del capitolo). «Condizioni spesso associate» → prosa. «La regola del marker fuori piano» → è la conseguenza pratica di quello che il lettore ha appena letto: diventa `> **Cosa cambia per te.**`, che è l'unico dei quattro box mai usato in tutto il documento.

### 2. [C — Etichette di solidità · e H, regola del ponte] Glosse mancanti, etichette fuori box, una frase-ponte assente

- riga 357 — box con **tre etichette e zero glosse**: *«PROBABILE per il valore prognostico della centralizzazione… IPOTESI per la preferenza direzionale… RAGIONAMENTO per l'anatomia foraminale»*. La glossa è testo fisso, non prosa da variare.
- riga 351 — `*(RAGIONAMENTO: il razionale fisiologico regge, ma nessuno studio di accuratezza lo conferma.)*` e riga 422 — `*(RAGIONAMENTO.)*`: etichette **fuori dal box**, senza glossa.
- riga 457 — il secondo `**PROBABILE**` della sezione Neurologico è senza glossa (il primo e il terzo ce l'hanno).
- riga 747 — **Zaccaro 2018** è l'unica fonte del cerchio 2 senza la frase che dichiara il salto. Tutte le altre ce l'hanno.
- Numeri in prosa che portano un'affermazione e non hanno la riga **Per te**: Santilli 55% contro 20% nel cerchio 1 (riga 733), Goldberg 49,2% contro 23,9% (riga 666), la confidenza molto bassa di Zhu (riga 735).

**Correzione.** Riportare la glossa fissa nei quattro punti, trasformare le due parentesi in box `> **Quanto è solido:**`, aggiungere a Zaccaro *«misurato su soggetti sani, non su pazienti con ernia discale»*, e dare la riga **Per te** ai tre numeri elencati (una riga ciascuno, non un paragrafo).

### 3. [B/G — Griglia formale e lessico del metodo] Rimandi per numero, celle di tabella fuori misura, termini canonici non ridefiniti per capitolo

- **Cinque rimandi per numero** invece che per nome: righe 92 e 158 («le tabelle del Capitolo 9»), 355 e 489 («i numeri stanno nel Capitolo 12»), 615 («il paziente del Capitolo 1»). Lo standard vuole il nome: *««Dove finisce il nostro campo»»*, *««Cosa può fare il paziente da solo»»*.
- **Celle oltre le 8 parole**, tutte nelle tabelle delle bandiere rosse e in «Gli studi cardine»: *«Forza che cala di giorno in giorno, o deficit importante comparso nelle ultime settimane»* (15), *«Trauma anche lieve in osso fragile: osteoporosi nota, cortisone prolungato, menopausa precoce»* (12), *«Dolore o massa addominale pulsante, o dolore che nessuna posizione cambia»* (11), *«Proporre la leva nell'acuto senza deficit — un solo studio, solo protrusioni»* (12).
- **Termini canonici senza box `Definizione` alla prima comparsa nel capitolo**: `marker` è definito nel Capitolo 8 e poi usato nei capitoli 9, 10 e 14 senza box; `reperto disfunzionale` e `disfunzione somatica` compaiono nel Capitolo 9 senza box (definiti rispettivamente nell'8 e nel 7). Chi apre il documento a metà — che è il modo in cui questo capitolo verrà letto — non trova la definizione.

**Correzione.** Sostituire i cinque rimandi con il nome del capitolo; spezzare le quattro celle lunghe (la riga sul deficit motorio è già sdoppiata nel testo: basta portare lo sdoppiamento in tabella); ripetere i tre box `Definizione` a testo fisso alla prima comparsa nei capitoli 9, 10 e 14 — costa nove righe.

### 4. [H-bis — Il cancello d'ingresso] Manca la ragione dichiarata del triage, e il vocabolario dei tempi non è quello chiuso

- **La ragione non c'è.** Nessuna riga spiega perché il triage a tre uscite protegge **più** del cancello binario (*«una regola scritta e disattesa vale meno di nessuna regola»*). Senza, il GIALLO — la situazione più frequente, quella in cui questo lettore lavorerà quasi sempre — si legge come una concessione invece che come uno standard più alto.
- **Cinque righe usano «Stessa giornata»**, che è fuori dal vocabolario chiuso (`112` · `Urgente` · `Invio, non attendere` · `Invio` · `Invio programmato`). È una precisazione sensata, ma o si normalizza o si apre una voce nel registro: un vocabolario chiuso che ammette un sesto termine senza dichiararlo smette di essere chiuso alla prossima Bibbia.

**Correzione.** Aggiungere le tre righe della ragione dichiarata in coda al cancello. Per i tempi: portare le cinque righe a `Urgente`, oppure — se «Stessa giornata» è ritenuto clinicamente migliore, e su una finestra chirurgica tempo-dipendente lo è — aprire una voce di deviazione e usarlo in tutte le Bibbie.

---

## PREFERENZE

### 1. [Lunghezza] La deviazione registrata è applicata a metà

Il corpo è a **16.760 parole** contro le 8.000-13.000 dello standard, e il Capitolo 12 a **992** contro 600-900. La voce D-019 (`PROPOSTA`) copre esattamente questo conflitto e prescrive una forma: *«dichiara la lunghezza in testa al documento, con la ragione: il residuo è ampiezza, non ridondanza»*. **L'intestazione della v2 non la dichiara.** Una riga in testa costa nulla e impedisce che il 4º livello legga l'eccedenza come ridondanza da tagliare.

### 2. [G — Glossario e Appendice B] Manutenzione delle appendici

- **52 voci** contro le 40 del collaudo. Sono quasi tutte legittime (metà è vocabolario di lettura dell'evidenza: eterogeneità, bias di pubblicazione, intenzione di trattare, odds ratio), ma il numero va guardato.
- **Due voci orfane**, nel Glossario e mai nel testo: *Anni-persona*, *Essudato*.
- **Una variante lessicale**: il Glossario dice *Shift antalgico*, il testo dice *shift laterale*.
- **Due fonti in Appendice B mai citate nel corpo**: Krishnamohan 2014 ([25230605](https://pubmed.ncbi.nlm.nih.gov/25230605/)) e Glenn 2020 ([32703468](https://pubmed.ncbi.nlm.nih.gov/32703468/)). Hincapié 2018 è citato per nome nel Capitolo 13 ma senza link.

---

## DEVIAZIONI MOTIVATE — rilievi contro il documento di metodo, non contro la Bibbia

Nessuna voce del registro è `RATIFICATA`: tutte le seguenti sono `PROPOSTA`, quindi si segnalano e si passa oltre.

| Voce | Come la Bibbia la applica | Giudizio |
|---|---|---|
| **D-015** (cancello a tre uscite insufficiente) | Tre uscite conservate, con le bandiere rosse in **due blocchi** — la soluzione della cervicalgia, già annotata nel registro | Applicata a lettera |
| **D-016** (il mandato non nasce dalla diagnosi) | Mandato **clinico** e **cornice professionale** separati, entrambi i corollari conservati | Applicata a lettera |
| **D-017** (Respiratorio-Circolatorio non invocabile per intero) | *«Della metà circolatoria del modello qui non si parla: nessuno l'ha misurata su questa regione»* | Applicata a lettera |
| **D-011 / D-018** (blocchi mancanti nella Mappa) | Blocchi 6 e 7 presenti, deviazione dichiarata in coda alla pagina | Applicata — ma la Mappa è quella vecchia (vedi ERRORE 1) |
| **D-020** (resistenza a 24 ore come segno viscerale) | La ricomparsa a 24-48 ore è elencata fra i segni del **primo meccanismo**, non come segnale viscerale, e ripresa nel Capitolo 11 come *«la firma del meccanismo»* | Applicata a lettera |
| **D-014 / D-020** (non trattare il Centro di Percezione) | CC e CP non sono mai nominati; il principio compare nella **forma attenuata** — *«vale per la ricerca, non per la scelta del bersaglio»* — con il fatto scritto accanto (Santilli 2006) | Applicata, ma nella forma che D-020 dichiara insufficiente |

**Segnalazione sull'ultima riga.** D-020 (lombalgia, 2026-08-19) sostiene che la forma attenuata *«si annulla da sola»* e va sostituita dalla **rimozione dichiarata**. Entrambe le voci sono `PROPOSTA`: nessuna delle due è ancora lo standard, quindi la Bibbia non è in errore. Ma quando Carlos deciderà, le due Bibbie muscolo-scheletriche devono muoversi insieme, e questa oggi è indietro di una formulazione.

**Nessuna deviazione non registrata trovata**, con una possibile eccezione: il tempo `Stessa giornata` (vedi RISCHIO 4), che se conservato va aperto come voce.

---

## TIENE

I quindici capitoli ci sono tutti, nell'ordine, con la funzione giusta, e nessuno è accorciato. La griglia formale regge dove costa di più: **quindici aperture «In una riga», quindici chiusure con esattamente quattro bullet, quindici slot «Perché ci sei tu» con tutti e tre gli elementi e un dato diverso ogni volta** — compresi i due che restringono lo spazio invece di allargarlo (cauda equina nel Capitolo 6, probabilità di partenza bassa nel Capitolo 9), che è la prova che lo slot è stato capito e non riempito. Il Capitolo 7 sono cinque sezioni brevi e non una tabella-mostro, ogni modello ha la sua etichetta e il Metabolico dichiara di non avere leve. Il confine con la Procedura è rispettato senza una sola incrinatura, e l'eccezione sui parametri di studio è usata bene: i parametri sono al passato e attribuiti a chi li ha misurati. «Quando la scienza tace» ha tutti e cinque i punti nell'ordine, e i tre cerchi sono dichiarati fonte per fonte.

---

## PUNTEGGIO DI FEDELTÀ

**4 caselle piene su 11** (A, D, F, Capitolo 12), **6 PARZIALI** (B, C, E, H tre cerchi, H-bis cancello, H Capitolo 14), **1 CONTRADDICE** (G, per la Mappa non rigenerata e per «il nervo che ha smesso di scorrere»). Nessun capitolo assente, nessun modello inventato, nessun protocollo dentro la Bibbia.

**VERDETTO: Fedele con lacune — ma la Mappa non è consegnabile.**
La Bibbia riproduce l'architettura in modo più completo della media; i quattro errori sono tutti **localizzati e correggibili in mezza giornata**, e tre su quattro sono contraddizioni interne — cioè il documento sa già la cosa giusta e la scrive altrove.

---

## DA PROTEGGERE DALL'EDITOR

Le correzioni qui sopra introducono qualificazioni che al 4º livello sembreranno ridondanti perché ripetono qualcosa che sta già altrove. **Ripetono apposta.** Riga per riga:

1. **La frase-ponte da aggiungere a Zaccaro 2018** — *«misurato su soggetti sani, non su pazienti con ernia discale»*. È la regola del ponte: senza, la HRV diventa una prova sulla leva. Non è ripetizione delle altre frasi-ponte: ogni fonte del cerchio 2 porta la sua.
2. **La motivazione della soglia a 20°** — la riga che dichiara *perché* la soglia è 20 e non 10 (l'errore di misura noto del SLR). Senza quella riga resta un numero arbitrario, e il primo lettore che trova 20 troppo severo lo riabbassa.
3. **La riga «Le soglie dal secondo al quinto marker sono convenzioni interne, non dati di letteratura»** (già nel testo, riga 558) — è ciò che impedisce di leggere le altre soglie come dati pubblicati. Non si taglia.
4. **La ragione dichiarata del triage** da aggiungere al cancello — *«una regola scritta e disattesa vale meno di nessuna regola»*. Sembra un commento e non lo è: è ciò che fa accettare il GIALLO come standard più alto invece che come concessione.
5. **La riga «Per te» dei tre numeri** (Santilli, Goldberg, Zhu) — è la terza parte obbligatoria del formato del dato numerico, non un commento all'evidenza.
6. **La qualificazione già presente su Santilli** — *«un solo studio, solo protrusioni»* e *«quei pazienti in quello studio non c'erano»* — va conservata anche quando la clausola del Capitolo 8 verrà riscritta: la correzione dell'ERRORE 2 apre la leva nell'acuto, e questa è la sua unica recinzione.
7. **Le due frasi che restringono lo spazio negli slot «Perché ci sei tu»** dei capitoli 6 e 9 (*«Su questi due sottotipi non ci sei»*, *«quella probabilità bassa vale solo finché qualcuno continua a fare le domande»*) — sono slot corretti proprio perché non promettono niente. Un editor che cerca lo slot debole da tagliare parte da qui, e sbaglia bersaglio.
8. **La dichiarazione di lunghezza in testa al documento** (D-019) — è l'unica cosa che dice all'editor che l'eccedenza è ampiezza dichiarata e non ridondanza.

# Feedback — Fedeltà all'Architettura (SECONDA PASSATA, 2° livello)

**Documento revisionato:** `bibbie-generate/reflusso-gastrico/v2-intermedia.md` (con `mappa-v2.md` come secondo deliverable).
**Standard di audit:** `architettura-bibbia.md` (quindici capitoli, cinque regole di struttura, quattro etichette, eccezione di confine sui parametri di studio), `cinque-modelli-osteopatici.md`, `motore-clinico.md`, `ancore-scientifiche.md`, `mappa-concettuale.md`.
**Registro deviazioni:** letto prima di marcare le caselle. Nessun rilievo di questo audit contraddice una voce del registro.

**Ricerca web:** la mia skill non impone la ricerca sul web — sono l'ispettore di presenza, non il Ricercatore. **Non ho eseguito ricerche e non propongo alcuno studio nuovo.** Nessuna aggiunta di contenuto da parte mia, quindi nessuna aggiunta mia da proteggere; la sezione finale elenca invece le qualificazioni **già presenti** che l'editor di 4° livello non deve tagliare.

```
LENTE: Fedeltà all'Architettura della Bibbia — audit di completezza
CONDIZIONE: Malattia da reflusso gastroesofageo

CHECKLIST DI FEDELTÀ
A. I quindici capitoli .................. PRESENTE — 0-14 + Appendice A e B, tutti nell'ordine
                                          e con la funzione prevista. Nessun capitolo omesso, nessuna inversione.
B. Griglia formale ..................... PARZIALE — «In una riga» 15/15, «Le tre cose da
                                          ricordare» 15/15 con esattamente tre voci. Ma due box di un QUINTO tipo
                                          inventato, e più tabelle con celle oltre le 8 parole.
C. Etichette di solidità (il lucchetto) . PARZIALE — quattro etichette e solo quelle; tutti e
                                          sei i meccanismi e tutti e cinque i modelli etichettati. Una leva del
                                          Cap. 11 porta l'etichetta inline invece che nel box. Una scala validata
                                          è attribuita all'autore sbagliato; sei fonti stanno in Appendice B senza
                                          comparire nel testo.
D. I cinque modelli (cap. 7) ........... PRESENTE — tutti e cinque in sezioni brevi, ciascuno
                                          con cosa governa / attori / segnali / etichetta. Nota di scope viscerale
                                          presente ("il viscerale non è un modello a sé"). Scope del Metabolico
                                          presente ("si valuta, si segnala e si rinvia").
E. Motore Clinico (cap. 8) ............. PARZIALE — punta/sommerso, indagine da monte, prova
                                          della chiave di volta con marker su piano non toccato, Road Map a sei
                                          passi numerati, CC/CP di Stecco con la regola "non si tratta il CP",
                                          tre stati del paziente, etichetta RAGIONAMENTO in apertura. Manca la
                                          distinzione esplicita COMPENSO vs COMANDO.
F. Confine teoria/procedura ............ RISPETTATO — nessuna sequenza, nessuna dose da
                                          somministrare, nessun piano di sedute. I parametri degli studi sono al
                                          passato e attribuiti (eccezione di confine applicata correttamente).
                                          Chiusura obbligatoria del Cap. 11 presente alla lettera. Cap. 8 rinvia
                                          alla Procedura per cadenza e numero di tentativi.
G. Fabbricazioni/contraddizioni ........ PRESENTI solo nel Glossario — nessun "modello
                                          viscerale" inventato, Trauma trattato come modificatore nella Road Map,
                                          Sistema Dominante tenuto come strato di ragionamento e non come spina
                                          dorsale visibile. Il Glossario però non rispetta la regola "tutti i
                                          termini usati, e solo quelli".
H. Tre cerchi + «Quando la scienza tace» PRESENTE — i tre cerchi sono dichiarati, distinti e
                                          usati; la regola del ponte è enunciata e OGNI fonte del cerchio 2 porta
                                          la frase "misurato su X, non su questi pazienti"; i cinque punti di
                                          «Quando la scienza tace» ci sono tutti, nell'ordine.
H. Cap. 12 strumenti attivi (condiz.) .. PRESENTE — la condizione di attivazione è soddisfatta
                                          (PROBABILE forte per l'esercizio respiratorio, DIMOSTRATO per peso e
                                          terapia posizionale). Sei voci su sei. Peso 1.023 parole contro 600-900.
H. Cap. 14 «Cosa fare adesso» .......... PRESENTE — 395 parole, filo ricucito senza elenco di
                                          capitoli, esattamente tre cose (una che guardi, una che dici, una che
                                          smetti), chiusura nella voce che motiva. Nessun contenuto nuovo, nessuna
                                          promessa di esito, nessun lessico da brochure.
```

---

## ERRORI — elemento obbligatorio assente, invertito o inventato

### 1. B — Griglia formale | Capitoli «Cosa dice la scienza» e «Cosa può fare il paziente da solo» | Due box di un quinto tipo inventato

La regola 4 dell'architettura è esplicita: quattro soli tipi di blockquote — `Definizione` / `Quanto è solido` / `Attenzione` / `Cosa cambia per te` — e «non inventarne altri: la prevedibilità grafica è metà della leggibilità». La v2 ne introduce due nuovi:

- riga 828: `> **La regola del ponte.** Una fonte del cerchio 2 alza l'etichetta del meccanismo…`
- riga 1026: `> **Il dettaglio che il paziente ha già sbagliato.** Quello che ha provato è il cuscino…`

Le varianti `> **Quanto è solido, per l'allenamento:**` e `> **Quanto è solido, per il lavoro manuale:**` (righe 568 e 570) restano dentro lo standard: è lo stesso box con un qualificatore.

**Correzione.** Il contenuto di entrambi è intoccabile — si cambia solo il contenitore. Riga 828: trasformare in `> **Attenzione.** La regola del ponte: una fonte del cerchio 2 alza…`. Riga 1026: trasformare in `> **Attenzione.** Quello che il paziente ha provato è il cuscino…`. Zero parole perse, box conformi.

### 2. B — Griglia formale | Capitoli 0 e 10 | Tabelle con celle oltre le 8 parole

Regola 5: «Massimo 4 colonne. Massimo 8 parole per cella. **Nessuna eccezione.** Se il contenuto non ci sta, non è una tabella: è prosa.»

- **Cap. 0, tabella delle etichette** — cella DIMOSTRATO: *"RCT, revisioni sistematiche solide, coorti ampie con relazione dose-risposta, o misura sperimentale diretta nell'uomo"* = 16 parole, il doppio del tetto.
- **Cap. 10, tabella «Si può dire / Non si può dire»** — almeno sei celle fra 9 e 11 parole (*"Una delle due componenti dello sfintere è muscolo scheletrico: il crus"*, *"Che il trattamento manuale riduca l'ernia o riposizioni il cardias"*, *"L'ipervigilanza pesa sulla gravità riferita più dei parametri di reflusso"*, *"La pressione dentro l'addome è un determinante misurato del gradiente"*, *"Che il reflusso spieghi con certezza tosse cronica o voce roca"*). Per questa sezione l'architettura non chiede nemmeno una tabella: chiede **«due elenchi affiancati, brutalmente espliciti»**.
- **Cap. 10, tabella degli studi cardine** — *"Citare la testata alzata, con i suoi effetti avversi"* = 9 parole.

**Correzione.** Cap. 0: spezzare la cella DIMOSTRATO in *"RCT o revisioni sistematiche solide"* e portare l'estensione (coorti con dose-risposta, misura sperimentale diretta) in una riga di prosa **sotto** la tabella — dove peraltro va comunque, perché è una deviazione dichiarata dal metodo (vedi sotto). Cap. 10: convertire «Si può dire / Non si può dire» in due elenchi puntati affiancati, come prescritto, così le frasi possono restare intere.

### 3. Lunghezza e distribuzione | Tutto il documento | 16.377 parole di corpo contro un tetto di 13.000

L'architettura fissa **8.000-13.000 parole**, con il tetto già alzato a 13.000 proprio per fare posto ai due capitoli nuovi, e dichiara che «sopra le 14.000 nessuno la finisce». Il corpo della v2 (esclusi Glossario e Fonti, che non contano) è di **16.377 parole**: +26% sopra il limite invalicabile, +46% sopra il target.

Anche la distribuzione è fuori quota nei due capitoli più gonfi: «Dove finisce il nostro campo» pesa 1.641 parole, cioè il 10% contro il 7% previsto; «Cosa dice la scienza» 1.812, l'11% contro il 9%.

**Correzione.** Servono circa 3.400 parole in meno, e il taglio va indirizzato — non lasciato a caso — sui due capitoli sopra quota e sul Capitolo 5 (2.348 parole), dove i sotto-meccanismi hanno guadagnato prosa di raccordo. È lavoro dell'editor di 4° livello: qui si registra soltanto che lo scostamento dallo standard è misurato e non marginale. **Vedi la sezione finale per cosa non può essere toccato in quel taglio.**

### 4. G — Fabbricazioni | Appendice A | Il Glossario non copre tutti i termini usati, ne contiene uno non usato, e supera il tetto di collaudo

La regola è binaria: «Se un termine è nel testo e non è qui, o è qui e non è nel testo, il glossario è sbagliato». Entrambe le direzioni sono violate.

- **Nel testo, assenti dal Glossario:** RMSSD (Cap. 10), Valsalva (Capp. 5 e 8), agonista del recettore GLP-1 (Capp. 5, 8, 9), melena (Cap. 9), ponzamento (Capp. 5 e 8), guaina carotidea e riflesso senocarotideo (Cap. 11), plesso celiaco (Cap. 11), dispepsia funzionale (Cap. 5), sleeve gastrectomy e plastica antireflusso (Cap. 6), Lyon Consensus e criteri di Montreal (Cap. 2), crossover (Capp. 10 e 12), componente ad alta frequenza della variabilità (Cap. 10).
- **Nel Glossario, assente dal testo:** *Blocco colinergico*. Il corpo dice "via colinergica" e "anticolinergici", mai la locuzione definita.
- **Tetto di collaudo:** 50 voci contro le 40 oltre le quali l'architettura dichiara che «la Bibbia è scritta troppo tecnica».

**Correzione.** Non aggiungere quindici voci: peggiorerebbe il collaudo. Fare il contrario, e in questo ordine. (a) Eliminare dal **testo** i tecnicismi sostituibili senza perdita — RMSSD e "componente ad alta frequenza" diventano *"gli indici di variabilità del battito legati al vago"*; crossover diventa *"studio in cui ogni paziente riceve entrambe le condizioni"*; pragmatico e ponzamento hanno equivalenti comuni. (b) Aggiungere solo le voci irrinunciabili perché nominano un rischio o un farmaco: **melena**, **agonista GLP-1**, **guaina carotidea**, **Valsalva**. (c) Rimuovere *Blocco colinergico* o riportare la locuzione nel Capitolo 3, dove il concetto già c'è. Il netto riporta il Glossario sotto le 45 voci e chiude entrambe le direzioni della regola.

---

## RISCHI — elemento presente ma incompleto

### 1. E — Motore Clinico | «Come ragiono davanti a questo paziente» | Manca la distinzione compenso vs comando

L'iceberg c'è ed è ben applicato (punta = bruciore, sommerso diverso in tre pazienti-tipo), e il capitolo distingue con cura il *dominante* dal *piano su cui puoi agire*. Ma la parola **compenso** non compare nel capitolo — compare una sola volta in tutto il documento, al Capitolo 5, e in senso meccanico ("il crus la compensa"). Il lettore esce sapendo *chi comanda*, non sapendo **riconoscere una disfunzione che compensa da una che comanda**: cioè non sa che un reperto molto evidente può essere l'adattamento, non la causa.

**Correzione.** Due righe dentro «La punta e il sommerso», subito dopo i tre pazienti-tipo: *"Non tutto ciò che palpi disfunzionale comanda. Una parete addominale rigida può essere il compenso che regge un diaframma che non lavora, e trattarla toglie l'unico appoggio che il paziente aveva. Chi comanda si riconosce dal fatto che, trattandolo, cedono anche gli altri piani — è la prova della chiave di volta, qui sotto."* Il collegamento alla chiave di volta esiste già: manca solo il nome della distinzione.

### 2. C — Etichette | «Perché le mani possono cambiare qualcosa» | Una leva porta l'etichetta inline invece che nel box

La regola C vuole che **ogni leva** del Capitolo 11 porti il suo `> **Quanto è solido:**`. Sei leve su sette lo fanno. La settima — *"Sulla stessa soglia, per una via che non è il tocco"* (riga 950), che è la leva propria del modello Comportamentale, cioè la **spiegazione** — ha le etichette annegate nella prosa: *"PROBABILE per l'effetto dei fattori di contesto… IPOTESI per il trasferimento al viscerale"*. È esattamente il difetto capitale che la regola 3 dell'architettura combatte: claim, qualificazione e citazione nello stesso periodo.

Va notato che è anche l'unica leva che il Capitolo 7 rimanda esplicitamente qui (riga 604: *"Questo modello ha una leva propria, e sta in «Perché le mani possono cambiare qualcosa»"*), quindi il lettore ci arriva cercandola.

**Correzione.** Estrarre le due etichette in un box, senza cambiare una parola del contenuto: `> **Quanto è solido:** PROBABILE per l'effetto dei fattori di contesto sull'esito riferito, misurato però sul dolore muscolo-scheletrico (Rossettini 2018; Bialosky 2018). IPOTESI per il trasferimento al sintomo viscerale.` La prosa sopra resta ad affermare.

### 3. C — Etichette | «Come ragiono davanti a questo paziente» e Appendice B | Una scala validata attribuita all'autore sbagliato, e sei fonti in bibliografia che il testo non cita

Riga 665: *"la **Esophageal Hypervigilance and Anxiety Scale**, la scala di Wong 2021"*. La scala non è di Wong: è stata sviluppata e validata da **Taft e colleghi, Aliment Pharmacol Ther 2018** — che sta correttamente in Appendice B al numero 54, ma non compare mai nel testo. Wong 2021 è lo studio che l'ha *usata* su 105 pazienti, ed è citato bene ovunque altrove. La regola C chiede che ogni studio citato abbia autore, anno e link: qui lo strumento è attribuito a chi non l'ha costruito, e chi l'ha costruito è invisibile.

Lo stesso disallineamento riguarda altre cinque voci dell'Appendice B che non compaiono nel testo con autore e anno: Löken 2009 (le fibre C-tattili, evocate al Cap. 10 senza fonte), ACR 2023 sulla massa pulsante, *Cough* 2008 sulla pressione addominale durante la tosse, Riehl 2016 (l'ipnoterapia, citata al Cap. 6 come *"uno studio di fattibilità non controllato"* senza nome), Shibata 2023 (la dissezione carotidea dopo pressione sul collo, Cap. 11). Anche il Cureus 2023 sul cortisolo è citato con la sola rivista, senza autore.

**Correzione.** Riga 665: *"la **Esophageal Hypervigilance and Anxiety Scale** (Taft, *Aliment Pharmacol Ther* 2018), usata su 105 pazienti da Wong 2021"*. E, per le altre cinque, aggiungere il nome e l'anno nel punto in cui il testo già le usa — sono aggiunte di due parole ciascuna, non di righe. Una fonte che sta solo in bibliografia è un peso morto che un revisore scettico legge come riempitivo.

---

## PREFERENZE — raffinamenti di completezza

### 1. Peso del Capitolo 12 e formato della tabella degli studi cardine

Il Capitolo 12 pesa **1.023 parole** contro le 600-900 previste (+14%): non è un manuale di esercizi, ma è oltre il tetto, e il taglio più naturale è la terza fonte sul sonno, che ripete due volte lo stesso autore. Nel Capitolo 10 la tabella degli studi cardine ha **11 righe** contro le 4-7 previste, e la seconda colonna è diventata *"n e disegno"* invece di *"Cosa ha misurato"*. Le undici righe hanno una ragione difendibile — sono tutti e quattro gli studi controllati esistenti più le sintesi, incluso quello sfavorevole, e ometterne sarebbe peggio — ma la colonna cambiata fa perdere l'informazione che lo standard voleva lì. Suggerimento: mantenere le undici righe e fondere le due informazioni in una colonna sola (*"Cosa ha misurato, e su quanti"*), che costa meno spazio di quanto sembri.

### 2. La Mappa concettuale ha nove blocchi contro i sei previsti

`mappa-concettuale.md` prescrive **sei blocchi, sempre gli stessi, sempre in quest'ordine**, su una pagina. `mappa-v2.md` ne ha nove: aggiunge «Cosa fa il paziente da solo» (5), «Le zone che non si premono» (7) e «I tre limiti da dire ad alta voce» (8). Il blocco 5 è una deviazione fondata e va trattata come tale (sotto). I blocchi 7 e 8 sono aggiunte fuori standard: utili, ma sono contenuto della Bibbia riversato nella Mappa, che è ciò che la specifica vieta ("se non ci sta in una pagina, hai messo dentro la Bibbia invece della sua struttura"). Inoltre, nel blocco 3 la terza colonna deve portare **solo l'etichetta**: qui porta frasi (*"PROBABILE come bersaglio, non dimostrato come causa"*). Suggerimento: assorbire il blocco 7 dentro le bandiere rosse, che è dove il lettore lo cerca, e ridurre la terza colonna del blocco 3 alla sola etichetta.

---

## DEVIAZIONI MOTIVATE — rilievi contro il documento di metodo, non contro la Bibbia

Queste **non sono infedeltà**. Sono punti in cui la v2 si discosta dal metodo con fondamento, e vanno registrate perché non si riaprano su ogni condizione.

**Già registrate e correttamente applicate — nessuna azione.** Il documento rispetta tutte le voci `PROPOSTA` del registro: D-001 (frequenza respiratoria contro la baseline del paziente e non contro una soglia assoluta, Capp. 8 e 14), D-002 (la direzione della leva vagale non è stabilita, Capp. 3, 5 e 14), D-003 (stress amplificatore percettivo e non generatore, Capp. 5, 7 e 14), D-004 (down-regulation aspecifica, non meccanismo neuroendocrino dimostrato, Cap. 11), D-007 (T5-T9 via grande splancnico, con il frenico C3-C5 tenuto separato, Cap. 3), D-008 ("da monte sul piano funzionale", con la negazione esplicita della lettura anatomica, Cap. 8), D-009 (co-occorrenza e non causalità con la cervicalgia, e il dato dei 33,89 gradi dichiarato non citabile, Capp. 6 e 10). Su questo fronte la seconda passata è pulita.

**DEVIAZIONE MOTIVATA — non registrata (1): l'estensione della definizione di DIMOSTRATO.** Il Capitolo 0 definisce DIMOSTRATO come *"RCT, revisioni sistematiche solide, **coorti ampie con relazione dose-risposta, o misura sperimentale diretta nell'uomo**"*. L'architettura si ferma a «RCT o revisioni sistematiche solide». L'estensione è scientificamente fondata — su peso e reflusso l'evidenza causale migliore al mondo *è* una coorte con dose-risposta bidirezionale, e nessun RCT la sostituirà mai — ed è usata con disciplina: il Capitolo 7 se ne fa carico esplicitamente (*"DIMOSTRATO come fattore causale, nel senso che il Capitolo 0 dà a coorti ampie"*) e aggiunge *"Non sono RCT, e va detto"*. Va aperta una voce nel registro: senza, la prossima Bibbia con evidenza epidemiologica forte o declassa a PROBABILE un dato che regge, o estende la definizione da capo a modo suo.

**DEVIAZIONE MOTIVATA — non registrata (2): il blocco «Cosa fa il paziente da solo» nella Mappa.** `mappa-concettuale.md` ha sei blocchi e non è stato aggiornato quando l'architettura ha introdotto il Capitolo 12 condizionale. Su questa condizione le leve meglio documentate non sono manuali: una Mappa che le omette comunica il contrario di ciò che la Bibbia sa, che è esattamente il ragionamento di proporzione con cui l'architettura giustifica il Capitolo 12. Va aperta una voce: la specifica della Mappa dovrebbe prevedere un settimo blocco condizionale, attivo quando il Capitolo 12 è attivo.

---

## TIENE

Tutti e quindici i capitoli sono presenti, nell'ordine e con la funzione prevista, e i due capitoli nuovi sono i più fedeli del documento: i tre cerchi sono dichiarati e distinti, la regola del ponte è enunciata e **ogni singola fonte del cerchio 2 porta la frase che dichiara il salto**, i cinque punti di «Quando la scienza tace» ci sono tutti nell'ordine, e «Cosa fare adesso» sta dentro le 400 parole con le tre cose giuste — una che guardi, una che dici, una che smetti — senza una parola da brochure.

Il confine con la Procedura è rispettato senza sbavature, ed è il risultato più difficile: il documento porta parametri di studio in quantità (quattro settimane, cinque giorni a settimana, sei settimane a 20 cm) e li tiene **tutti** al passato e attribuiti, senza scivolare una volta nell'imperativo. La chiusura obbligatoria del Capitolo 11 è riprodotta alla lettera.

I cinque modelli sono cinque sezioni brevi con le quattro voci ciascuna, nessun modello viscerale inventato, il Trauma è un modificatore nella Road Map e non un livello della gerarchia, e il Sistema Dominante resta strato di ragionamento sotto l'impalcatura invece di tornare spina dorsale visibile.

---

## PUNTEGGIO DI FEDELTÀ

**7 caselle PRESENTI su 10.** Parziali: **B** (due box di un quinto tipo inventato; celle di tabella oltre le 8 parole), **C** (una leva del Cap. 11 con etichetta inline invece che nel box; una scala attribuita all'autore sbagliato; sei fonti in bibliografia mai citate nel testo), **E** (manca la distinzione compenso vs comando). Nessuna casella ASSENTE. Nessuna casella CONTRADDICE sul piano dei modelli o del confine; la sola contraddizione è il **Glossario**, che viola la regola in entrambe le direzioni ed è sopra il tetto di collaudo. Fuori specifica anche la **lunghezza**: 16.377 parole di corpo contro un tetto di 13.000.

**VERDETTO: Fedele con lacune.**
L'impalcatura c'è tutta e nei punti che decidono la credibilità — i tre cerchi, la regola del ponte, il confine con la Procedura, le etichette sui meccanismi e sui modelli — la v2 è più fedele della v1; quello che resta sono difetti di forma della griglia (box, tabelle, glossario) e un sovrappeso del 26% che va risolto prima della consegna.

---

## DA PROTEGGERE DALL'EDITOR

Non ho aggiunto contenuto e non ho proposto studi: non ho quindi aggiunte mie da proteggere. Ma tre dei quattro ERRORI qui sopra si correggono **dentro** passaggi che l'editor di 4° livello leggerà come ridondanza, e due dei rilievi chiedono di *estrarre* una cautela invece di toglierla. Se queste righe cadono nel taglio delle 3.400 parole, resta il PMID e sparisce il limite, che è il contrario di quello che serve.

**Frasi-ponte del cerchio 2 — intoccabili, una per una.** Ognuna è la condizione che rende citabile la fonte accanto:
- Cap. 10: *"Misurato su volontari e popolazioni miste, non su pazienti con reflusso."* (dopo Laborde 2022)
- Cap. 10: *"Sani, non pazienti con reflusso."* (dopo Ruffini 2015)
- Cap. 10: *"Entrambi sul dolore muscolo-scheletrico, non su quello viscerale."* (dopo Bialosky 2018 e Rossettini 2018)
- Cap. 10, box di chiusura del cerchio 2: *"IPOTESI che quella modulazione riduca il sintomo di un paziente con reflusso: il ponte fra i due enunciati non è stato attraversato da nessuno studio."*
- Cap. 7, Comportamentale: *"misurato però sul dolore muscolo-scheletrico (Rossettini 2018). IPOTESI per il trasferimento di quell'effetto al sintomo viscerale: nessuno l'ha misurato."*
- Cap. 11, leva della spiegazione: *"misurato però sul dolore muscolo-scheletrico; IPOTESI per il trasferimento al viscerale."* — questa va **estratta in un box**, non tagliata (Rischio 2).
- Cap. 10: l'enunciato stesso della regola del ponte (riga 828) — cambia il contenitore, non il testo (Errore 1).
- Cap. 12: il box sul cuscino contro il piano del letto (riga 1026) — cambia il contenitore, non il testo (Errore 1).

**Voci di «cosa non possiamo dire» e qualificazioni numeriche — intoccabili:**
- Cap. 2: la risposta al placebo del 18,85% su 24 studi e 9.989 pazienti, e la perdita spontanea del 2,32% l'anno. Sono il metro con cui si legge qualunque miglioramento.
- Cap. 10: i denominatori accanto ai due numeri favorevoli (dimensione dell'effetto 0,80 **su 38 pazienti**; la massima espiratoria dello stesso studio **non significativa**; il GerdQ senza differenza minima clinicamente rilevante pubblicata).
- Cap. 10: *"quel dato non si cita"* sui 33,89 gradi di mobilità cervicale. È l'applicazione di D-009.
- Cap. 10: cortisolo −0,10 µg/dl **non significativo**, su quattro studi e 135 partecipanti; fibre C-tattili mai studiate su un viscere; nessun follow-up manuale oltre le venti settimane.
- Cap. 10: la tabella delle **quattro revisioni sistematiche**, tre delle quali sfavorevoli, con il limite dichiarato della quarta (rivista di settore, non indipendente) e la conseguenza operativa *"nessuna etichetta PROBABILE di questa Bibbia poggia sul solo studio viscerale"*. È il passaggio che regge tutto il capitolo davanti a un collega scettico.
- Cap. 10: su Lynen 2022, *"Un documento che si vanta di dire i propri limiti non omette l'unico studio che non gli dà ragione"*.
- Cap. 11: *"gli studi di terapia manuale viscerale in larga parte non registrano affatto gli eventi avversi, e lì l'assenza di segnalazioni non è un dato di sicurezza"*.
- Cap. 11: *"Non chiamare «riflessa» quella modifica immediata: non esiste un arco somato-viscerale documentato verso lo sfintere."*
- Cap. 5: *"IPOTESI per la riduzione dei rilasciamenti con l'allenamento: dodici pazienti, uno studio, mai replicato. Si cita, non ci si conta sopra."*
- Cap. 12: le due correzioni in senso opposto — *"IPOTESI, non «non lo fa»"* sui rilasciamenti transitori, e *"IPOTESI in entrambe le direzioni"* sull'ernia.
- Cap. 6: *"razionale forte, prove dirette nessuna"* sul sottotipo pressorio-posturale, ed è l'unico punto in cui il documento dichiara la tensione fra plausibilità e prova.
- Cap. 8: *"I reperti palpatori con cui allochi il paziente in un sottotipo sono RAGIONAMENTO: su questa condizione non esiste alcun dato di affidabilità fra operatori."*
- Cap. 11: *"IPOTESI che la terza, da sola, cambi qualcosa in questo paziente"* con la controprova di Urnes 2007, il trial di educazione che non ha trovato effetto. È l'unico punto in cui la Bibbia porta la prova contro sé stessa.

**Regola sintetica per il taglio:** in questo documento la lunghezza è nelle **descrizioni**, non nelle cautele. Le 3.400 parole si trovano nei Capitoli 5, 9 e 10 comprimendo prosa esplicativa e ripetizioni fra sotto-meccanismi. Ogni riga che contiene un denominatore, un "non", un "misurato su", o un'etichetta, resta.

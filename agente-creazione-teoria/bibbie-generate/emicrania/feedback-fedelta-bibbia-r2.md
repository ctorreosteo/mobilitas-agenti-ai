LENTE: Fedeltà all'Architettura della Bibbia — audit di completezza (2ª passata, secondo livello)
CONDIZIONE: Emicrania
DOCUMENTO REVISIONATO: `bibbie-generate/emicrania/v2-intermedia.md` (17.885 parole totali, 16.244 di corpo).
**`mappa-v2.md` non esiste.** In cartella c'è solo `v1-mappa.md`, generata sulla v1. Il secondo deliverable della v2 manca, ed è il primo rilievo.

Nota di ruolo: questa skill non impone ricerca sul web. Non propongo studi nuovi e non ho verificato PMID in questa sessione: l'audit è di presenza, posizione e coerenza con lo standard, non di evidenza.

---

## CHECKLIST DI FEDELTÀ

```
A. I quindici capitoli .................. PARZIALE — tutti e 15 presenti, nell'ordine, con Appendici A e B.
                                          Mancano due elementi interni prescritti: «Le tre domande che ti farà»
                                          (Cap. 1) e la frase-cerniera fissa di chiusura del Cap. 4.
                                          Il secondo deliverable (Mappa concettuale v2) è ASSENTE.
B. Griglia formale ...................... PARZIALE — «In una riga» in tutti e 15 i capitoli; «Le tre cose da
                                          ricordare, più una» in tutti e 15, sempre a quattro bullet con lo slot
                                          in ultima posizione e tutti e tre gli elementi. Ma: cinque box di un
                                          quinto tipo inventato; 9 celle di tabella oltre le 8 parole; 5 rimandi
                                          a capitolo per numero; un dato di slot ripetuto (Varkey, Cap. 12 e 14).
C. Etichette di solidità (il lucchetto) . PARZIALE — quattro etichette e solo quelle; glossa fissa corretta in
                                          tutti i box tranne uno (Strumento 4, Cap. 12, etichetta fuori box e
                                          senza glossa). Cap. 0 ha i sei passi di studio, nessun triage di
                                          lettura. Nessun claim gonfiato: CC/CP, gel→sol, effetto vagale del
                                          tocco non compaiono o sono IPOTESI. Studi con autore/anno/PMID e
                                          ricompaiono in Appendice B.
D. I cinque modelli (cap. 7) ............ PRESENTE — cinque sezioni brevi, nessuna tabella unica; per ciascuno
                                          cosa governa, attori, segnali, etichetta. Viscerale non esiste come
                                          modello. Metabolico con lo scope («si rileva, si segnala, si rimanda»).
E. Motore Clinico (cap. 8) .............. PARZIALE — punta/sommerso con quattro pazienti-tipo, indagine da monte
                                          con la correzione «non è una coordinata anatomica», prova della chiave
                                          di volta con il marker fuori piano, Road Map numerata, tre stati,
                                          etichetta RAGIONAMENTO in testa. Manca la distinzione compenso vs
                                          comando; CC/CP di Stecco non nominati (il principio c'è, il lessico no).
F. Confine teoria/procedura ............. RISPETTATO — nessuna sequenza, nessuna dose al nostro paziente, nessun
                                          piano di sedute. I parametri («otto sedute in quattro settimane»,
                                          «40 minuti tre volte a settimana per tre mesi») sono al passato e
                                          attribuiti agli studi: eccezione di confine applicata correttamente.
                                          Chiusura obbligatoria del Cap. 11 presente alla lettera.
G. Fabbricazioni/contraddizioni ......... NESSUNA — nessun modello viscerale, Trauma trattato come modificatore
                                          in anamnesi, Sistema Dominante sotto e non in vetrina. Glossario a 40
                                          voci, con le quattro etichette e i sette termini del metodo. Marker
                                          nominati: sei, con misura e soglia (lo standard ne chiede da due a
                                          quattro). PARZIALE solo sui box `Definizione` per capitolo.
H. Tre cerchi + «Quando la scienza tace»  PRESENTE — tre cerchi dichiarati e distinti, regola del ponte scritta
                                          a lettera, frase «misurato su X, non su questi pazienti» attaccata a
                                          ogni fonte del cerchio 2 (Sterling, Gordon, Löken, Laborde). «Quando la
                                          scienza tace» con tutti e cinque i punti nell'ordine.
H. Cap. 12 strumenti attivi (condiz.) ... PRESENTE, DOVUTO — l'esercizio regge DIMOSTRATO sull'emicrania: il
                                          capitolo deve esserci. Struttura a sei voci completa su Strumenti 1-3,
                                          incompleta su Strumento 4. Peso 1.302 parole contro le 600-900 previste.
H. Cap. 14 «Cosa fare adesso» ........... PRESENTE — filo ricucito senza elenco di capitoli, esattamente tre cose
                                          (guarda / chiedi / smetti), chiusura in corsivo nella voce che motiva,
                                          nessuna promessa di esito, nessun lessico da brochure. 421 parole
                                          contro 250-400, e il dato dello slot ripete quello del Cap. 12.
```

---

## ERRORI (elemento obbligatorio ASSENTE, invertito o inventato)

**1. [A — secondo deliverable] | Mappa concettuale | La Mappa della v2 non esiste.**
In cartella c'è solo `v1-mappa.md`, costruita sulla v1. La Bibbia è stata riscritta — il collo è passato da innesco a candidato bidirezionale, sono comparsi le soglie dei marker, il cancello a tre uscite riscritto, il Cap. 12 a quattro strumenti — e la Mappa non ha seguito. In più il suo blocco «Perché ci sei tu» (Lipton 2007) è **lo stesso** del Capitolo 1 della Bibbia, mentre lo standard vuole che sia unico e il più forte dei quindici.
*Correzione:* generare `mappa-v2.md` allineata alla v2, e sostituire il blocco di chiusura con un dato non usato in nessuno dei quindici slot — il candidato naturale è Woldeamanuel/Varkey sull'esercizio, che è la leva più forte del documento e che nella Mappa non compare come chiusura.

**2. [H-bis — il cancello d'ingresso] | Capitolo 9 | Manca la ragione dichiarata del triage.**
Il capitolo ha tutto il resto del cancello — mandato clinico con il corollario simmetrico, contrappeso, ROSSO senza eccezioni, quattro condizioni del GIALLO, cosa succede se il GIALLO scade, scadenza dell'inquadramento, vincolo di documentazione — ma **non spiega perché il triage protegge di più del cancello binario**. La frase «una regola scritta e disattesa vale meno di nessuna regola» non compare da nessuna parte del documento (verificato per grep).
*Correzione:* aggiungere due righe subito prima di 🔴 ROSSO, nella forma prevista: il cancello vecchio dichiarava un requisito e veniva aggirato; una regola scritta e disattesa vale meno di nessuna regola; questo dichiara cosa fai davvero in ciascuna situazione, tiene il ROSSO rigido e mette per iscritto l'unica cosa che rende difendibile il GIALLO. Senza, il lettore legge le quattro condizioni del GIALLO come un permesso e non come uno standard più alto.

**3. [C + H — etichette e Capitolo 12] | Capitolo 12, Strumento 4 (le abitudini del sonno) | Etichetta fuori box, senza glossa, e chiusura di confine assente.**
È l'unico punto del documento dove il lucchetto si apre. Lo Strumento 4 sta in un paragrafo unico, l'etichetta è inline — `**Quanto è solido:** PROBABILE — studio pilota…` — non è un blockquote e **non porta la glossa fissa** *(razionale forte, prove parziali)*, che lo standard impone a ogni comparsa. In più manca la sesta voce obbligatoria: *«Come e quando consegnarlo al tuo paziente sta nella Procedura»*, presente sugli Strumenti 1, 2 e 3.
*Correzione:* portare l'etichetta in un box `> **Quanto è solido:** PROBABILE *(razionale forte, prove parziali)* — …` e chiudere lo strumento con la formula di confine alla lettera. Aggiungere la riga «in quanto tempo si vedrebbe» che gli altri tre strumenti hanno.

**4. [B — regola 4, quattro soli tipi di box] | Capitoli 6, 7, 8, 12 | Cinque box di un quinto tipo inventato.**
I box ammessi sono quattro: `Definizione` · `Quanto è solido` · `Attenzione` · `Cosa cambia per te`. Ne compaiono cinque che non sono nessuno dei quattro:
- Cap. 6, riga 324 — `> **E come lo distinguo da una cefalea cervicogenica?**`
- Cap. 7, riga 393 — `> **Due parole che si somigliano e non sono la stessa cosa.**`
- Cap. 8, riga 460 — `> **Quale marker è fuori piano dipende da cosa hai toccato…**`
- Cap. 8, riga 501 — `> **Quando più domande rispondono sì — ed è il caso frequente.**`
- Cap. 12, riga 786 — `> **L'obiezione che sentirai alla prima seduta: «io se faccio sport mi viene».**`
Il contenuto di tutti e cinque è buono e va conservato: il difetto è la forma, e la forma è metà della leggibilità perché il lettore impara a riconoscere quattro segnali grafici e non nove.
*Correzione:* riconvertirli. 324 e 786 diventano `> **Cosa cambia per te.**`; 393 diventa `> **Definizione.**` (è la distinzione fra attivazione simpatica immediata e livello di attivazione, ed è già a Glossario); 460 e 501 escono dal box e restano prosa in grassetto dentro il Capitolo 8.

---

## RISCHI (elemento PARZIALE)

**1. [A — Capitolo 1 e Capitolo 4] | Due elementi interni prescritti mancano.**
Il Capitolo 1 ha «Come lo racconta lui», «Cosa ha già fatto», «Cosa nessuno ha guardato», ma **non ha «Le tre domande che ti farà»** — le domande poste lì con la risposta rimandata al capitolo che la contiene. Il Capitolo 4 non chiude con la frase-cerniera fissa *«Questo è il sistema che funziona. Ora vediamo dove si rompe.»*
*Cosa lo renderebbe fedele:* tre domande vere di questo paziente (ne esistono già le risposte sparse: *«ma cosa ho, se la risonanza è normale?»* → Cap. 2; *«il collo c'entra?»* → Cap. 6 e 8; *«mi prometti che spariscono?»* → Cap. 13), e la cerniera in coda al Cap. 4, prima della chiusura in quattro bullet.

**2. [E — Motore Clinico] | Capitolo 8 | Manca la distinzione compenso vs comando.**
Il capitolo spiega perché si indaga da monte e ordina cinque piani, ma non dice mai la cosa che rende pericoloso sbagliare: che il piano che *compensa* non è il piano che *comanda*, e che trattare il compenso dà un miglioramento che dura una settimana e torna. La parola «compenso» compare due volte in tutto il documento — un rimando fra parentesi nel Cap. 5 e la voce a Glossario — e mai come concetto usato. Su questa condizione il rischio è concreto e il documento lo sfiora senza nominarlo: il collo dolente che in due casi su tre è *parte* dell'attacco è esattamente un compenso letto come comando.
Il lessico CC/CP di Stecco non compare; il principio sì (*«Il punto in cui fa male non è il punto da trattare»*). Non lo segno come infedeltà — sull'emicrania il bersaglio è davvero fuori dalla zona sintomatica e la regola discrimina — ma la scelta va dichiarata, non lasciata implicita.
*Cosa lo renderebbe fedele:* due righe in «Perché si indaga da monte» che agganciano il compenso al caso concreto di questa condizione, e una riga che dichiara che qui la regola di non trattare dove il paziente sente **si applica** e perché (in una condizione muscolo-scheletrica non si applicherebbe — vedi D-020/Lombalgia).

**3. [G + C — i termini canonici del metodo] | Tutto il documento | I box `Definizione` non ci sono alla prima comparsa in ogni capitolo, e il testo canonico è abbreviato a Glossario.**
Il documento dichiara la scelta a lettera in due punti — Cap. 3: *«Le altre parole del metodo stanno nel Glossario, e ciascuna compare per esteso una volta sola»*; Cap. 5: *«(«Compenso» e «catena» sono nel Glossario.)»*; Cap. 8: *«(«Lesione primaria», «reperto disfunzionale» e «marker» sono nel Glossario.)»*. Conseguenza: **`marker`, `reperto disfunzionale`, `compenso` e `lesione primaria` non hanno un box `Definizione` in nessun capitolo**, e `marker` regge tre regole del metodo (il mandato del GIALLO, la scadenza dell'uscita gialla, la prova della chiave di volta). In più le voci a Glossario sono **riformulate in forma abbreviata** rispetto al testo canonico di `lessico-del-metodo.md`: a `marker` manca *«per sapere se quello che hai fatto ha cambiato qualcosa»*; a `compenso` mancano *«comfort, efficienza, escursione»* e *«non dove il problema è nato»*; a `reperto disfunzionale` manca l'esemplificazione; a `lesione primaria` manca *«e non è una prova»*. Il testo fisso non si riformula.
Attenuante reale: le quattro condizioni di un marker che funziona sono scritte per intero nel Cap. 8, ed è la parte che regge le regole.
*Cosa lo renderebbe fedele:* riportare a Glossario il testo canonico esatto delle sette voci, e mettere il box `Definizione` di `marker` almeno nel Capitolo 8 (prima comparsa operativa) e nel Capitolo 9 (dove regge la quarta condizione del GIALLO). Se la rinuncia ai box ripetuti va tenuta per ragioni di lunghezza, **va aperta una voce nel registro delle deviazioni agganciata a D-019**: oggi è una scelta dichiarata nel testo e non registrata da nessuna parte.

---

## PREFERENZE (raffinamenti di completezza)

**1. [B — regole 1 e 5] | Quattro imprecisioni formali, tutte a costo quasi nullo.**
(a) Cinque rimandi a capitolo **per numero** invece che per nome — «le domande dell'arterite del Capitolo 2» (Cap. 5), «con l'etichetta modesta del Capitolo 11» (Cap. 6), «stanno nel Capitolo 12» (Cap. 7), e altri due; altrove il documento cita correttamente per nome, sette volte.
(b) Nove celle di tabella oltre le 8 parole: cinque nella tabella delle bandiere rosse, quattro in quella dei farmaci — la peggiore a 13 parole (*«Se ti dice che cerca un figlio, è una comunicazione da mandare oggi»*, riga 572).
(c) La tabella dei sottotipi ha 3 colonne e ha perso quella prescritta **«Meccanismo che comanda»**: oggi il collegamento sottotipo → meccanismo si ricostruisce solo leggendo i paragrafi.
(d) La tabella degli studi cardine porta 8 studi contro i 4-7 previsti.

**2. [Lunghezza e distribuzione] | Il corpo è a 16.244 parole contro un tetto di 13.000, e la deviazione D-019 è applicata a metà.**
Distribuzione fuori quota nei due capitoli più pesanti: Cap. 9 a 2.098 parole (12,9% contro ~7%) e Cap. 8 a 1.901 (11,7% contro ~8%). Il Cap. 12 sta a **1.302 parole contro le 600-900** che lo standard fissa espressamente, e il Cap. 14 a 421 contro 250-400. La voce D-019 (`PROPOSTA`) copre lo sforamento come ampiezza e non come ridondanza — ma prescrive che **la lunghezza sia dichiarata in testa al documento con la sua ragione**, e quella dichiarazione qui non c'è. Il taglio è mestiere dell'editor di 4º livello; quello che riguarda me è che il Cap. 12 ha un tetto suo, scritto, e lo supera del 45%.

---

## DEVIAZIONI MOTIVATE (non sono rilievi contro la Bibbia)

- **D-016 (`PROPOSTA`) — mandato a due piani.** Il Cap. 9 separa il mandato **clinico** (reperto + marker) dalla **cornice professionale** (DPR 131/2021, si opera in riferimento alla diagnosi di competenza medica), conservando entrambi i corollari. È esattamente la forma prescritta dalla voce. **Non è un'infedeltà: è la deviazione registrata, applicata bene.**
- **D-017 (`PROPOSTA`) — restrizione di scope del Respiratorio-Circolatorio.** Il Cap. 7 dichiara a lettera che si usa la sola metà ventilatoria e che la metà circolatoria qui non si invoca perché non ha misure. Corretto e conforme.
- **D-020/Emicrania (`PROPOSTA`) — il collo come candidato bidirezionale.** La v2 ha eliminato ovunque la lettura «collo = innesco»: la convergenza è scritta a doppio senso, la proporzione due su tre è dichiarata in tre punti, la palpazione sostenuta è usata come test di stratificazione e non come conferma di catena causale, e il Cap. 9 vieta esplicitamente di attribuire l'emicrania al collo. È la voce di registro applicata per intero, ed è il miglioramento più sostanziale rispetto alla v1.
- **D-020/Sciatalgia (`PROPOSTA`) — re-test contro soglia dichiarata.** Ogni marker del Cap. 8 porta la sua soglia, i 10° di rotazione in flessione sono giustificati sopra l'errore di misura (~7°) e il +20% è dichiarato come convenzione interna e non come dato. Conforme.
- **D-021 (`PROPOSTA`) — gel/sol dell'acido ialuronico.** Assente dal documento. Corretto.
- **D-011 / D-018 (`PROPOSTA`) — blocchi della Mappa.** Applicati nella v1-mappa (blocco 5 strumenti attivi, blocco 7 ragionamento e marker) e dichiarati in coda alla pagina. Vanno riportati nella `mappa-v2.md` da generare.
- **Deviazione non registrata, da aprire:** la sostituzione dei box `Definizione` ripetuti per capitolo con un rimando unico a Glossario (Capp. 3, 5, 8). È dichiarata nel testo, ha una ragione plausibile (lunghezza, D-019), ma **non è scientifica** e non è nel registro. O si riapre il box, o si apre la voce: oggi è una regola del metodo disattesa in silenzio, che è lo stato peggiore dei tre.

---

## TIENE

L'ossatura è quella giusta e regge in blocco: quindici capitoli nell'ordine, quindici aperture «In una riga», quindici chiusure a quattro bullet con lo slot «Perché ci sei tu» completo dei suoi tre elementi (dato · ti autorizza a · non ti autorizza a) e con la lacuna dichiarata anche quando restringe il campo (Cap. 6, Cap. 9, Cap. 11). Il lucchetto delle etichette è chiuso: nessun claim gonfiato, il contatto lento è IPOTESI e non «effetto vagale», i cinque meccanismi sono ordinati dal più solido al meno solido e ciascuno porta la sua metafora isolata. Il Capitolo 10 è il pezzo più fedele del documento — tre cerchi separati, regola del ponte scritta e applicata a tutte e quattro le fonti trasversali, «Quando la scienza tace» con i cinque punti nell'ordine. E il vicolo cieco non c'è: il Paziente B, il caso canonico del driver da livello di attivazione, finisce con *«è il paziente in cui hai più da fare, non meno»* e con la leva nominata e agganciata al Capitolo 11, che dichiara la stessa leva con la stessa etichetta.

## PUNTEGGIO DI FEDELTÀ

**7 caselle su 11 PRESENTI** (D, F, G-fabbricazioni, H-tre cerchi, H-cap. 12 dovuto e presente, H-cap. 14, più il confine rispettato).
PARZIALI: A (due elementi interni mancanti), B (quinto tipo di box, celle, rimandi, dato di slot ripetuto), C (una etichetta senza box né glossa), E (compenso vs comando).
ASSENTI: la **Mappa concettuale v2**, la **ragione dichiarata del triage** nel Cap. 9, la **chiusura di confine** dello Strumento 4.
CONTRADDICE: nulla.

## VERDETTO: Fedele con lacune

L'architettura è riprodotta e le deviazioni registrate sono applicate bene; quello che manca sono tre elementi obbligatori isolati e un deliverable intero — la Mappa — e nessuno dei quattro richiede di riaprire il contenuto.

---

## DA PROTEGGERE DALL'EDITOR

Non aggiungo studi né contenuto clinico. Aggiungo **quattro righe di struttura**, e sono tutte del tipo che il quarto livello legge come ridondanza e taglia. Vanno protette:

1. **La ragione dichiarata del triage** (Cap. 9, da aggiungere): *«una regola scritta e disattesa vale meno di nessuna regola»* con le due righe che la accompagnano. Sembra un commento sul metodo; è ciò che impedisce di leggere le quattro condizioni del GIALLO come una concessione. Non è meta-commento legale: non parla della posizione legale del documento, parla di come si comporta chi legge.
2. **La chiusura di confine dello Strumento 4** (Cap. 12): *«Come e quando consegnarlo al tuo paziente sta nella Procedura.»* È identica a quella degli altri tre strumenti e per questo sembra tagliabile. È la riga che tiene la Bibbia fuori dal territorio della Procedura, e va ripetuta quattro volte su quattro proprio perché è formula.
3. **La glossa fissa** *(razionale forte, prove parziali)* **da aggiungere allo Strumento 4**, e tutte le altre glosse già presenti nei box. Costano quattro parole a box e sono l'unica cosa che rende leggibile l'etichetta a pagina dodici. Non sono prosa da variare e non sono ripetizione da comprimere.
4. **Il testo canonico integrale delle sette voci del metodo a Glossario** (`marker`, `reperto disfunzionale`, `disfunzione somatica`, `compenso`, `catena`, `sistema dominante`, `lesione primaria`). Le parti che oggi mancano sono proprio le subordinate che un editor toglie per primo — *«per sapere se quello che hai fatto ha cambiato qualcosa»*, *«non dove il problema è nato»*, *«e non è una prova»*. Quelle subordinate sono il significato, non l'ornamento.

E vanno protette dalla stessa mano le qualificazioni **già presenti** nel documento, perché sono la parte che regge tutto l'impianto:

- Ogni frase-ponte del Cerchio 2, Cap. 10: *«su 30 soggetti con dolore cervicale medio-basso, non su emicranici e non sul collo alto»* (Sterling), *«su popolazioni miste»* (Gordon), *«su volontari sani»* (Löken), *«su soggetti sani»* (Laborde), e la riga che le governa: *«Tutto questo alza l'etichetta del meccanismo, mai quella della leva sull'emicrania. Nessuno di questi studi ha misurato un emicranico.»*
- Le stesse frasi-ponte ripetute nei punti d'uso: Cap. 7 Respiratorio *«— su soggetti sani»*; Cap. 11 meccanismo 1 *«— su soggetti con dolore cervicale medio-basso, non con emicrania»*.
- Le voci di «cosa non possiamo dire»: l'intera colonna destra della tabella «Puoi dire / Non puoi dire» (Cap. 10); l'apertura del Cap. 11 *«Cosa non possono fare le mani, detto per primo»*; il Cap. 13 *«Cosa non promettere mai»*; e la riga del Cap. 12 *«Cosa succede quando il paziente smette: non è documentato, e si dice come un limite, non come una minaccia.»*
- Le qualificazioni che accompagnano i numeri e che sembrano cautele di troppo: *«quel 100% non è il nostro 100%»* (García-Azorín, Cap. 9); *«quel 50% non è la prevalenza generale»* (Giffin, Cap. 4); *«è un'attribuzione riferita in intervista, non una misura»* (Pradhan, Cap. 6); *«il gruppo di controllo riceveva solo il farmaco, senza finto trattamento»* (Bevilaqua-Grossi, Capp. 8 e 11); *«quel numero non si converte in giorni, e non è confrontabile con il 3,55 del capitolo sull'esercizio»* (Rist, Cap. 10); *«su un solo paziente»* (Schulte & May, Capp. 3 e 5); *«di cui l'abstract non riporta la quota»* (Luedtke 2018, Cap. 3).
- Il **+20% dichiarato come convenzione interna e non come dato**, e la giustificazione dei 10° sopra l'errore di misura di 7° (Cap. 8): senza quelle due righe le soglie diventano numeri inventati che sembrano misurati.

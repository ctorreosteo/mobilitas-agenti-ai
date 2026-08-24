# Feedback — Medico Specialista (primo livello)

**LENTE:** Medico Specialista — Ortopedico / fisiatra specialista del rachide
**CONDIZIONE:** Iperlordosi lombare
**DOCUMENTO REVISIONATO:** `bibbie-generate/iperlordosi/v1-bibbia.md` (v1.0, agosto 2026), letto insieme a `v1-mappa.md`.

---

## RICERCA SVOLTA

Ho verificato in questa sessione **tutti e 42 i PMID** dell'Appendice B su PubMed (esummary + efetch): autore, anno, rivista e titolo corrispondono in tutti i casi. Nessuna citazione inventata, e questo va detto per primo perché è raro.

Ho poi letto gli **abstract** delle citazioni portanti e confrontato i numeri riportati nel testo: Herrington 2011 (85%/75%, n=120), Sorensen 2015 (4,4°, IC 0,9–7,8°, r=0,46, 24/57), Chun 2017 (13 studi, 796/927, SMD −0,33), Nelson-Wong 2014 (35,3% vs 23,1%), Preece 2021 (+2,6°, −1,2°, lordosi invariata, n=23), Nelson-Wong 2008 (65%, 76%, sens 0,87 spec 0,50), Nelson-Wong 2010 (8,93 vs 16,5 mm), Falk Brekke 2020 (2 RCT/72, <2°), Downie 2013 (9% / 33% / 62%), Sieper 2009 (79,6% / 72,4%), Chu 2023 (0,21/100.000), Heneghan 2018 (64,75 vs 74,96), Licciardone 2013 (RR 1,38 e 1,41), Barone Gibbs 2018 (8 punti ODI, n=27), Vialle 2005 (60±10, r=0,86), Harvie 2024 (κ 0,13 / 0,56), Azevedo 2014 (SDC 1,5–4,0), Walker 1987 (rho 0,18 e 0,06; r=0,32). **Tutti corrispondono, tranne uno: Youdas 1996.** Il testo gli attribuisce nello script al paziente una cosa che l'abstract dice al contrario per le donne (rilievo E-3).

Non ho potuto confermare nell'abstract il singolo numero "3,9 gradi di sottostima della goniometria" attribuito a Moreside e McGill 2011 (PMID 21546144): l'abstract riporta la normativa 3D su 77 maschi con 22 valutati al goniometro, ma non quel valore. Non lo segnalo come errore — probabilmente è nel corpo dell'articolo — ma va ricontrollato sul full text, perché regge una soglia di marker.

Ho infine cercato ciò che il documento **non** dice: linee guida e standard correnti sull'equilibrio sagittale (SRS-Schwab, PMID 22045006), la stadiazione e la finestra di guarigione della spondilolisi adolescenziale (Sairyo, PMID 16418642), la sindrome anca-rachide (Khoury, PMID 33948195), la prevalenza della diastasi dei retti nel post-partum (Sperstad, PMID 27324871), l'AAA come bandiera rossa del dolore lombare.

---

## ETICHETTE DA CORREGGERE — il mio strumento principale

**1. Preece 2021 non regge un DIMOSTRATO.**
Capitolo: «Cosa si rompe: i meccanismi», meccanismo 4 — e ripetuto identico in «Perché le mani possono cambiare qualcosa» e nella Mappa (§3).
Affermazione: *"Che allungare i flessori aumenti l'estensione d'anca e riduca l'inclinazione del bacino: DIMOSTRATO"*.
Etichetta corretta: **PROBABILE**.
Perché: il vostro Glossario definisce DIMOSTRATO come *"studi randomizzati o revisioni sistematiche solide sull'uomo"*. Preece 2021 (PMID 34090549) è uno studio **a braccio singolo, pre-post, 23 uomini sani, una sola sessione, nessun gruppo di controllo, nessun follow-up**. I 2,6° e gli 1,2° non sono mai stati confrontati con niente. È un ottimo studio per dire *cosa non succede* (la lordosi non si muove — e lì l'IPOTESI con prove contrarie è perfetta), ma non può reggere la metà positiva della stessa frase con l'etichetta più alta.

**2. Sorensen 2015 non regge un DIMOSTRATO — ed è il claim che tiene su tutto il documento.**
Capitolo: «Cosa si rompe: i meccanismi», meccanismo 2 — rimbalzato in «Che cos'è davvero» e nella Mappa (§3, *"DIMOSTRATO il legame col dolore"*).
Affermazione: *"Che chi sviluppa dolore in due ore di stazione eretta abbia in partenza una lordosi maggiore: DIMOSTRATO"*.
Etichetta corretta: **PROBABILE**, con glossa esplicita.
Perché: è **un solo studio trasversale osservazionale su 57 persone** (24 pain developer, 33 no), differenza media 4,4° con **intervallo di confidenza 0,9°–7,8°** — cioè un limite inferiore che sfiora lo zero — mai replicato da un gruppo indipendente. Da questa singola misura discendono nel documento: il sottotipo principale, la scelta dell'esito, la frase da dire al paziente e l'intero riquadro *"Perché ci sei tu"* del Capitolo 5. Non chiedo di toglierlo — chiedo che porti l'etichetta che gli spetta. Il documento non perde nulla: continua a dire che è un fattore di rischio su un sintomo preciso, che è vero, e diventa inattaccabile.

**3. Been e Kalichman 2014 è una revisione narrativa, non una revisione sistematica.**
Capitolo: «Cosa si rompe: i meccanismi», meccanismo 3.
Affermazione: *"Che una lordosi ampia si accompagni a spondilolisi e spondilolistesi istmica: DIMOSTRATO"*.
Etichetta corretta: **PROBABILE**, glossa *"associazione costante in una revisione narrativa di oltre 120 lavori; direzione causale non stabilita"*.
Perché: PMID 24095099 è indicizzata come *literature review*, riporta associazioni trasversali e non contiene meta-analisi. Il vostro DIMOSTRATO chiede randomizzati o revisioni sistematiche solide.

---

## ERRORI

**E-1 · Youdas 1996 è citato al contrario nello script al paziente — e proprio nel sesso in cui il dato esiste.**
Capitolo: «Cosa dire al paziente», obiezione *"Faccio addominali tutti i giorni"*.
Prova: l'abstract (PMID 8863760) dice testualmente *"Abdominal muscle performance was associated with angle of pelvic inclination for women (R2 = .23), but not for men"*. Il "nessuna correlazione" di Youdas riguarda un'altra coppia di variabili — inclinazione pelvica contro profondità della lordosi. Il documento scrive invece: *"in novanta adulti misurati con cura non è stata trovata nessuna relazione fra la forza degli addominali e l'inclinazione del bacino in piedi"*. La paziente-tipo di questa Bibbia è una donna: la frase da pronunciare ad alta voce è falsa esattamente sulla persona che l'ascolterà.
Correzione: riscrivere la risposta così — *"nelle novanta persone misurate, la relazione fra forza degli addominali e inclinazione del bacino era assente negli uomini e debole nelle donne: spiegava circa un quinto della variabilità. Non ha sbagliato a impegnarsi, e non le hanno dato un bersaglio sbagliato — le hanno dato un bersaglio piccolo, venduto come grande."* Correggere in parallelo «Cosa può fare il paziente da solo», dove *"rinforzare la parete anteriore non cambia l'inclinazione del bacino, ed è misurato"* va portato a *"non la sposta in misura utile"*: Youdas e Walker sono correlazioni trasversali (Walker: rho 0,18 con il bacino), non studi di intervento, e non possono dire cosa fa il rinforzo.

**E-2 · La bandiera rossa della spondilolisi ha il tempo sbagliato, e il documento se lo smentisce da solo dieci righe dopo.**
Capitolo: «Dove finisce il nostro campo», tabella delle bandiere rosse, riga *"Adolescente sportivo, dolore mediano in estensione"* — tempo attuale: **Invio**. Stessa riga nella Mappa (§6).
Prova: nello stesso capitolo, sotto *"Cosa succede se sbagli campo"*, scrivete che *"la lesione dell'istmo ha una finestra in cui guarisce e una in cui non guarisce più"*. È esatto, ed è misurato: con segnale osseo positivo alla STIR guarisce il 79% dei difetti trattati conservativamente, con segnale negativo lo **0%** (Sairyo, *Spine* 2006, PMID 16418642); i tassi di consolidazione per stadio scendono dal 62% delle lesioni precoci all'8,7% delle progressive allo 0% delle terminali. La finestra si misura in settimane, e un ragazzo che nel frattempo continua ginnastica, danza o tennis la sta consumando durante l'attesa. "Invio" è il penultimo gradino del vostro vocabolario e non contiene nessuna scadenza: è la sola riga della tabella in cui il ritardo è **causato** dal tempo che avete scritto.
Correzione: portare il tempo a **"Invio, non attendere"**; specificare nella riga che la domanda al medico è una **RM lombare con sequenze STIR** (la radiografia non vede lo stadio precoce, che è quello che guarisce); e aggiungere che nel frattempo il carico in estensione ripetuta si sospende — è l'unica cosa che protegge la finestra mentre l'imaging arriva, ed è conoscenza, non protocollo.

**E-3 · L'anca artrosica e il conflitto femoro-acetabolare non esistono in questo documento — e sono il differenziale del vostro segno centrale.**
Capitoli: «Cosa si rompe: i meccanismi» (meccanismo 4), «Non è una condizione sola: i sottotipi», «Dove finisce il nostro campo».
Prova: l'estensione d'anca limitata è il reperto attorno a cui ruota metà della Bibbia, e l'unico descrittore che fornite è *"arresto elastico e non doloroso"*. Non è mai detto cosa significa quando l'arresto è **duro**, quando è **doloroso**, quando si accompagna a **rotazione interna ridotta**, a dolore inguinale o a rigidità mattutina dell'anca: cioè coxartrosi o conflitto femoro-acetabolare. Non compare in «Cosa non è», non è un sottotipo, non ha una riga nella tabella. Chi studia questa Bibbia non saprà di doverlo cercare — che è esattamente il criterio con cui giudico un'omissione più grave in una Bibbia che in una procedura. E la leva che dichiarate *"la più diretta che hai"*, il lavoro sulla catena anteriore dell'anca, è proprio quella che in un conflitto anteriore irrita il quadro. La letteratura registra che nella sindrome anca-rachide l'anca è **sottodiagnosticata** mentre stenosi e sciatalgia sono sovradiagnosticate, e che la limitazione dell'escursione d'anca produce meccanica lombo-pelvica alterata (Khoury, *J Hip Preserv Surg* 2020, PMID 33948195). La vostra stessa fonte cardine apre dicendo che l'eccessiva antiversione pelvica è sospettata di causare conflitto femoro-acetabolare (Falk Brekke, PMID 32071772): il legame è già dentro il documento, e il documento non lo raccoglie.
Correzione: due aggiunte, entrambe brevi. **(a)** Nel meccanismo 4, la coppia che separa il tessuto dall'articolazione: *arresto elastico, indolore, simmetrico → tessuti anteriori, è tuo; arresto duro o doloroso, rotazione interna ridotta, dolore inguinale o gluteo profondo, rigidità dell'anca al risveglio → articolazione, non è tuo.* **(b)** Una riga nella tabella delle bandiere: *"Dolore inguinale con rotazione interna d'anca limitata e dolorosa | Curante per radiografia del bacino | Invio"*.

---

## RISCHI

**R-1 · Dite due volte che la soglia non esiste, e non date la regola che invece esiste.**
Capitoli: «Che cos'è davvero» (La definizione), «Le strutture in gioco».
Perché è attaccabile: date l'istruzione *"la lastra sotto carico si legge cercando l'incidenza pelvica prima della lordosi"* e non fornite mai il modo di leggerla. L'osteopata resta con due numeri e nessuna regola per metterli insieme. La regola è lo standard corrente del rachide: il disallineamento fra incidenza pelvica e lordosi, **PI − LL**, con soglia < 10° come assetto allineato, 10–20° e > 20° come disallineamento crescente (modificatore della classificazione SRS-Schwab; Schwab, *Spine* 2012, PMID 22045006). La frase *"non esiste un numero oltre il quale si è iperlordotici"* è vera per la soglia **assoluta** e falsa per quella **relativa**: la seconda esiste, è individualizzata su quel bacino, ed è esattamente ciò che il vostro capitolo promette e non consegna. Nella stessa direzione: eleggete Roussouly ad "ancora morfologica" e dite che i suoi quattro assetti sono *"la classificazione che rende leggibile una lastra"* — e poi i quattro assetti non li descrivete da nessuna parte.
Mitigazione: in «Che cos'è davvero», due righe che distinguono soglia assoluta (non esiste) da soglia relativa (PI − LL, con i tre scaglioni). In «Le strutture in gioco», quattro righe sui tipi di Roussouly. Sono conoscenza, non protocollo, e chiudono l'unico buco operativo dell'inquadramento.

**R-2 · La diastasi dei retti non è nominata una sola volta, e il profilo addominale è il motivo per cui la paziente paga la visita.**
Capitoli: «Che cos'è davvero» (Cosa non è), «Cosa si rompe» (meccanismo 5), «Cosa dire al paziente» (obiezione *"Dopo la gravidanza è normale"*).
Perché è attaccabile: spiegate il profilo interamente con la geometria del contenitore, etichetta IPOTESI, glossa *"nessuno l'ha quantificata"*. È onesto sulla vostra ipotesi, ma esiste una causa comune, misurabile in trenta secondi e con un nome, che il documento non pronuncia mai: la **diastasi dei retti**, presente nel **32,6% delle primipare a dodici mesi dal parto** in una coorte prospettica di 300 donne (Sperstad, *Br J Sports Med* 2016, PMID 27324871). Non è un driver di dolore — nello stesso studio il dolore lombo-pelvico non differiva, e questo va detto — ma è il differenziale del **sintomo per cui la paziente è venuta**. Un documento che dedica un meccanismo intero al profilo addominale post-partum e non nomina la diastasi è la cosa che mi farebbe alzare il sopracciglio più in fretta di ogni altra.
Mitigazione: una riga in «Cosa non è» e una nel meccanismo 5 — il profilo post-partum si separa in diastasi dei retti (distanza inter-retti palpata sopra l'ombelico, all'ombelico, sotto) e geometria del bacino, **prima** di attribuirlo alla seconda. E in «Dove finisce il nostro campo» la nota che una tumefazione riducibile sulla linea mediana è un'ernia ombelicale o ventrale, cioè un invio chirurgico, non un reperto disfunzionale.

**R-3 · Scrivete che sotto la vostra mano ci sono i grandi vasi, e non mettete lo screening che a quella frase corrisponde.**
Capitoli: «Dove finisce il nostro campo» (tabella), letto insieme al box *"il profilo di rischio del distretto"* in «Perché le mani possono cambiare qualcosa».
Perché è attaccabile: il box dice testualmente che *"l'accesso anteriore all'ileopsoas passa sopra i grandi vasi addominali e sopra l'intestino"*. È una frase corretta e coraggiosa, e resta orfana: nella tabella delle bandiere non c'è nessuna riga sull'**aneurisma dell'aorta addominale**, che si presenta con dolore lombare nella grande maggioranza dei casi e il cui segno da cercare è una **massa addominale pulsante**. Concedo che non sia la paziente-tipo — donna fra i trenta e i cinquanta — ma il documento copre esplicitamente anche il paziente anziano (osteoporosi, cortisone prolungato, claudicatio), e su quello il contatto anteriore profondo viene autorizzato con le stesse parole.
Mitigazione: una riga nella tabella — *"Massa addominale pulsante, o aneurisma aortico noto | Curante o pronto soccorso | Urgente"* — e una frase nel box: nessun contatto anteriore profondo prima di aver palpato l'addome e di aver escluso una pulsazione espansiva.

---

## PREFERENZE

**P-1 · La spondilolistesi degenerativa L4-L5 manca dal differenziale.** In «Che cos'è davvero» (Cosa non è) coprite la spondiloartrite assiale e la stenosi, e la listesi solo nella forma istmica dell'adolescente. La donna fra i cinquanta e i settanta con dolore in piedi che si allevia flettendosi è la presentazione classica della listesi **degenerativa**, che può stare senza claudicatio e quindi sfugge alla riga che avete. Una riga in «Cosa non è» chiude il quadro.

**P-2 · Il numero di Moreside e McGill 2011 va ricontrollato sul full text.** I "3,9 gradi di sottostima della goniometria" in «Come ragiono davanti a questo paziente» non compaiono nell'abstract (PMID 21546144). Non lo chiamo errore, ma regge la soglia di un marker: se non è verificabile, la soglia degli 8° va motivata altrimenti.

---

## REGGEREBBE SULLA MIA SCRIVANIA?

Se un mio paziente me lo portasse, la prima cosa che mi farebbe alzare un sopracciglio è che il documento sa che l'istmo ha una finestra di guarigione e poi scrive "Invio" senza scadenza sulla riga dell'adolescente: è l'unico punto in cui il ritardo diagnostico è generato dal documento stesso. La seconda è l'anca — costruite metà del ragionamento sull'estensione d'anca limitata e non dite mai che quel reperto, in un cinquantenne, è coxartrosi finché non si dimostra il contrario. La terza è la diastasi dei retti: un documento che tratta il profilo addominale post-partum per un capitolo intero e non la nomina mai sembra scritto da chi non riceve quelle pazienti.

Quello che invece mi farebbe pensare che in quello studio sanno di cosa parlano è che il documento **dichiara per primo di non poter fare la cosa per cui la paziente è venuta**. Il consenso che esclude il profilo dell'addome come esito, la frase "non ti autorizza a presentare la correzione posturale come un intervento efficace" messa a pagina uno, e Chun 2017 riportato per intero contro l'intuizione del proprio mestiere: quella è la prova che l'autore ha letto la letteratura e non l'ha selezionata. Non ho mai visto un documento osteopatico dichiarare in apertura che tutta la letteratura mondiale sul suo bersaglio sono due studi randomizzati e 72 persone.

---

## TIENE — da non toccare

Il cancello a tre uscite con le quattro condizioni verificabili del GIALLO, e in particolare la comunicazione **scritta** al curante e la revisione programmata: è più severo del binario che sostituisce e non ha eccezioni sul ROSSO. La separazione fra Chun (lombalgia cronica, meno curva) e Sorensen (dolore in piedi, più curva), che è la cosa clinicamente più intelligente del documento. La scelta del tempo cronometrato in piedi come esito al posto dei gradi, e il marker della prova collocato nel torace. Il riquadro *"il profilo di rischio del distretto"* con la forza di picco come variabile. E la nota sulla tabella delle bandiere come **rete e non filtro**, con l'obbligo di scrivere in cartella che l'hai passata e non che il paziente è negativo: è formulata meglio di quanto la trovo scritta in molti documenti medici.

---

## VERDETTO: **Da correggere**

L'impianto è solido e le fonti sono reali e verificate una per una — cosa che questa revisione trova quasi mai. Ma tre etichette DIMOSTRATO poggiano su studi singoli che il vostro stesso Glossario esclude, una citazione è riportata al contrario nella frase da dire al paziente, un tempo di invio contraddice la finestra di guarigione che il documento dichiara, e il differenziale dell'anca manca del tutto. Sono correzioni chirurgiche, non una riscrittura.

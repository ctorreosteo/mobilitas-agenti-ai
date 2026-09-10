# Piano — ripresa Bibbie (4 settembre 2026)

## Stato verificato sul disco, non dai report

Contate con uno script su `outputs/`, richiedendo **due `.docx` sopra i 10 KB** per dire «consegnata». Nessuna cartella e' risultata monca.

| | |
|---|---|
| Condizioni in `problemi.json` | 68 |
| Consegnate e verificate in `outputs/` | **46** |
| Da fare | **22** |
| In lavorazione | artrite |

## 1. Dove si e' fermata artrite

In `bibbie-generate/artrite/` ci sono quattro file, non di piu':

| file | peso | ora |
|---|---|---|
| `v1-bibbia.md` | 122 KB | 02/09 16:07 |
| `v1-mappa.md` | 6 KB | 02/09 15:52 |
| `feedback-sistema-dominante.md` | 12 KB | 02/09 18:58 |
| `feedback-specialista.md` | 19 KB | 02/09 20:04 |

La catena e' morta **dentro il primo livello**: la bozza c'e', ma dei revisori di 1o livello ne hanno risposto **2 su 11**. Mancano `medico-generale`, `sicurezza-tecniche`, `fisioterapista-ebp`, `compliance`, `neolaureato`, `modelli`, `neuromodulazione`, `clinico-esperto`, `strumenti-attivi`. Non esiste ancora nessuna `v2-intermedia.md`.

## 2. Come viene ripresa, senza buttare la v1

`genera-bibbie.workflow.js` accetta `args = { slugs, stati }`: ogni stadio il cui file di uscita e' gia' su disco viene saltato. Lo stato glielo passo io, ricavato con un `ls` — cioe' senza spendere un agente per scoprirlo.

```
{ slugs: ["artrite"],
  stati: { artrite: ["v1-bibbia.md", "v1-mappa.md",
                     "feedback-sistema-dominante.md",
                     "feedback-specialista.md"] } }
```

Effetto: il Draft viene saltato (122 KB di bozza restano), il primo livello riparte **solo sui nove revisori mancanti**, e da li' la catena prosegue intera fino alla consegna.

## 3. Coda successiva, una alla volta

piedi-gonfi · gonfiore-addominale · diarrea-ricorrente · sensazione-di-fiato-corto · dolore-al-coccige · labirintite · menopausa · diastasi · cicatrici-seno-rifatto · pubalgia · coxalgia · tendinite-d-achille · scoliosi · spalla-congelata-capsulite-adesiva · sindrome-di-arnold-nevralgia-occipitale · asma · spalla-dolorosa-periartrite-cuffia-dei-rotatori · dolore-sacroiliaco · trocanterite · distorsione-caviglia · tendinite-calcifica-spalla

## Come vengono lanciate

**Una invocazione per Bibbia, mai due insieme**: il parallelo brucia la quota prima che una arrivi in fondo. Ogni lancio si chiude con la verifica sul disco — `v7-finale.md`, `mappa-finale.md` e i due `.docx` in `outputs/<slug>/` — prima di far partire la successiva. Se un lancio muore a meta', la ripresa e' la stessa di artrite: `ls` sulla cartella, `stati` ricalcolato, rilancio.

---

# Esito — artrite CHIUSA (04/09, 13:32)

La catena e' ripartita dal punto giusto: `[ripresa] v1 gia' su disco, salto il draft`, `2/11 feedback gia' presenti`, poi **9/9** revisori mancanti, e da li' fino in fondo. 28 agenti, 4,7 milioni di token, 4 ore.

## Il verdetto era NON CONSEGNABILE, e aveva ragione

Stessa firma di fibromialgia — il collaudo semantico e' andato in **stallo tre volte** al terzo giro (1267 s, 467 s, 865 s) e il workflow ha chiuso con «4 violazioni ancora aperte dopo 2 riparazioni». Ma la consegna gira comunque per progetto, quindi i `.docx` erano usciti **con le violazioni dentro**.

Tre delle quattro erano reali, e tutte nello stesso punto: la **tabella delle bandiere rosse** del capitolo «Dove finisce il nostro campo». Il 6o livello, comprimendo le celle per rientrare nelle 8 parole, aveva tagliato i qualificatori:

| | v5 (corretta) | v7 consegnata |
|---|---|---|
| 1 | Una o piu' articolazioni calde e gonfie da pochi giorni, con o senza febbre | Articolazione calda e gonfia recente, anche senza febbre |
| 2 | Affanno da sforzo nuovo **o ingravescente**, tosse secca persistente | Affanno da sforzo nuovo, tosse secca persistente |
| 3 | **Dolore atraumatico** di calcagno, caviglia o gamba in metotrexato **di lunga durata** | Calcagno, caviglia o gamba senza trauma, in metotrexato |

Non sono sfumature. La riga 1 esiste apposta per smontare il riflesso «sono piu' articolazioni, quindi e' una riacutizzazione», e senza «una o piu'» non lo smonta. La riga 2, senza «o ingravescente», scatta solo su un affanno che prima non c'era — mentre l'interstiziopatia descritta tre righe sotto e' per definizione un affanno preesistente che peggiora. La riga 3 nominava tre distretti anatomici **e nessun segno**, e valeva per qualunque paziente in metotrexato.

La prova che fosse una perdita e non una scelta: la **Mappa portava ancora la formulazione piena**. I due documenti consegnati insieme si contraddicevano.

## La quarta violazione non andava riparata

`TABELLE_FUORI_SPECIFICA` e' il **falso positivo gia' visto su fibromialgia**: lo script conta le righe lunghe solo nel documento in uscita, senza confrontarle con l'ingresso. Le stesse 17 righe stanno identiche nella v5 — verificato per campione con `grep -c`. Il difetto appartiene al livello di asciugatura, non a chi ha riscritto. Il collaudo stesso lo dice, e aggiunge la cosa piu' utile: *«non riscrivere altre celle per rientrare nella specifica: e' esattamente l'operazione che ha prodotto le tre violazioni qui sopra»*.

## Riparazione applicata

Ripristinato il testo **esatto della v5** nelle tre celle, senza inseguire il limite di parole: l'accuratezza batte il formato, come prescrive la gerarchia del metodo. Le tre righe tornano fuori specifica — ma erano fuori specifica anche prima, e compaiono nell'elenco della v5.

Collaudo deterministico rilanciato sul passaggio di lingua: **identita' 98%**, delta +0,6%, e tutti i contatori fermi — 62 PMID, 15 etichette, 23 «Per te», 15 slot, 7 uscite. Nessun bloccante di conservazione.

`.docx` rigenerati e verificati aprendo l'XML: le tre formulazioni piene sono dentro. `Bibbia_Artrite.docx` (83 KB) e `Mappa_Artrite.docx` (17 KB).

## Segnali per Carlos, da leggere

Il 5o e il 6o livello concordano su **5 passaggi che restano oscuri perche' il pensiero sotto e' confuso, non la frase**. Sono contraddizioni di contenuto che nessuna riscrittura puo' chiudere:

1. **Cap. 8** — la regola del centro che coordina e' dichiarata «tolta e non attenuata», e nulla la sostituisce come criterio di scelta della sede. Il Glossario peggiora la cosa: definisce il termine e tre righe dopo ne dichiara la revoca.
2. **Cap. 7 / 11 / Road Map** — il modello Respiratorio e' insieme «accessorio e senza meccanismi propri» (7), portatore dell'unica etichetta che sale grazie alle mani (11, Elgayar 2026), e collocato al passo 7, cioe' *prima* dei compensi. Le tre cose non stanno insieme.
3. **Cap. 8, marker** — la soglia del 20% sulla forza di presa. Il testo scarta i 5,0-6,5 kg pubblicati perche' dodici mesi del programma migliore ne spostano 1,4; ma il 20% di una presa da venti chili sono quattro chili, cioe' quasi la soglia appena rifiutata. L'obiezione vale anche contro la soglia nuova.
4. **Cap. 5 / 6** — quattro pazienti su dieci soddisfano i criteri 2016 di fibromialgia, e su quel sottotipo il trattamento non ha dato sollievo; nello stesso capitolo il dolore residuo e' «il sottotipo portante, dove puoi molto». Non viene mai detto quanto resti del primo una volta tolto il secondo.
5. **Cap. 9 / 8** — il mandato a trattare oggi nasce da «un marker scelto prima che si e' mosso dopo», cioe' da una misura che alla prima seduta non esiste. Il Cap. 8 ci mette una nota per disinnescare l'ambiguita': e' il documento che commenta se stesso, e il circolo resta.

Il registro della lingua segnala inoltre che **«driver» e' la terza condizione di fila** in cui compare: merita la promozione a «Correzioni attive».

## Prossima

**piedi-gonfi**, lanciata. Restano 21.

---

# Esito — piedi-gonfi CHIUSA (04/09, 17:40)

31 agenti, 4,9 milioni di token, 4 ore. Uno stallo sulla sintesi v3 (1046 s), rientrato al primo retry. Anche qui verdetto **NON CONSEGNABILE** e `.docx` consegnati lo stesso — ma stavolta di tre violazioni una sola era reale.

## L'unica reale: di nuovo la tabella delle bandiere rosse

Blocco A, quarta riga — quella della **trombosi venosa profonda**, che il documento stesso definisce «l'unica cosa qui che si conta in ore».

| | testo |
|---|---|
| v5 e v6 | Una gamba sola gonfia in ore, **o bilaterale peggiorato in fretta da un lato** |
| v7 consegnata | Una gamba sola gonfia in ore |

Identica dinamica di artrite: il 6o livello accorcia la cella per rientrare nelle 8 parole e porta via il secondo innesco. E identica prova che fosse perdita: **la Mappa continuava a portare la clausola per esteso**, quindi i due documenti si contraddicevano sul punto piu' urgente della sicurezza.

## La riparazione, diversa da quella di artrite

Su artrite avevo rimesso il testo pieno nella cella. Qui **no**, e il motivo e' che il passaggio di lingua aveva fatto un buon lavoro: le 19 righe fuori specifica della v5 erano rientrate **tutte** nella v7. Riaprire la cella le avrebbe riportate fuori.

Il documento aveva gia' inventato la soluzione da solo: per le altre due righe accorciate il riscrittore aveva **compensato fuori dalla tabella**, nel paragrafo di apertura del blocco. Su questa se l'era dimenticato. Aggiunta la frase mancante nella stessa forma:

> «Nella prima riga la tosse con sangue conta quanto gli altri tre segnali. **E nella quarta riga vale allo stesso modo un bilaterale peggiorato in fretta da un lato.**»

Collaudo rilanciato: **CONSEGNABILE, 0 bloccanti**. `.docx` rigenerati e verificati aprendo l'XML.

## Le altre due violazioni: ereditate e gia' chiuse

`TABELLE_FUORI_SPECIFICA` (19 righe) e `SCRIPT_TROPPO_LUNGO` (107 parole contro 100) erano **entrambe gia' nella v5**, e la v7 le aveva gia' risolte da sola — le tabelle rientrate, lo script sceso a 100 parole esatte senza perdere nessuno dei sette contenuti. Nessun intervento. Il collaudo aggiunge l'avvertenza giusta: non usarle come giustificazione retroattiva del taglio sulla riga della trombosi.

## Segnali per Carlos

Cinque punti dove il contenuto si contraddice e nessuna riscrittura puo' chiudere:

1. **Cap. 8** — il titolo dice «perche' si indaga dall'alto», tre righe sotto il testo dichiara che la Road Map procede per frequenza e modificabilita' «e per questo parte dal basso». Il documento prova a salvarsi con «due ordini vanno tenuti separati»: in italiano piano, quella frase ammette che dichiara un ordine e ne segue un altro.
2. **Cap. 8, il caso di Anna** — la regola vuole il marker su un piano *non* trattato; con Anna sono stati trattati entrambi i piani e il marker scelto e' il delta mattina-sera della caviglia, che sta su uno dei due. La difesa («e' un reperto, non un sintomo») usa una distinzione diversa da quella che la regola chiede.
3. **Cap. 5 / 7 / 12** — «la disponibilita' del torace» non ha un referente misurato: non e' il flusso istantaneo (che e' una fase) ne' il bilancio netto (misurato, e non si muove). Eppure ci poggiano sopra il modello dichiarato piu' pertinente, il marker 4 e meta' dello script per il paziente.
4. **Cap. 8, marker 3** — la soglia di 2 cm sulla dorsiflessione e' piu' grande dell'estremo alto dell'effetto atteso (MD 0,91, IC 0,06-1,76). Il documento risolve spostando la lettura alla seduta dopo: cambia l'orologio, non la taglia.
5. **Cap. 9 contro Cap. 11** — in GIALLO, «la situazione piu' frequente su questa condizione», e' vietata ogni manovra ritmica sull'arto e sulla sua radice; la leva del secondo meccanismo *e'* una manovra ritmica sulla gamba e sulla radice dell'arto. Nel caso piu' frequente di quella leva resta solo lo sbocco al collo, e nessuno dei due capitoli lo scrive.

**«driver» e' alla quarta condizione di fila**, e qui e' peggio: il documento l'ha istituzionalizzato, dichiarando nel Glossario che sistema dominante, sommerso e driver sono «stessa cosa, tre nomi». Il 6o livello ha reso le sei occorrenze in prosa con «il sommerso» — il nome italiano che il documento si e' gia' dato — lasciando intatte Glossario e Definizione. Va promosso a «Correzioni attive».

Segnalato anche **«consistente» per «costante»** (3 occorrenze, tutte su Jung 2023, due dentro box «Quanto e' solido»): «nessun effetto ipoalgesico immediato consistente» si leggeva come «nessun effetto rilevante» invece di «nessun effetto costante» — cambiava la forza di un dato negativo.

## Prossima

**gonfiore-addominale**, lanciata. Restano 20.

---

# gonfiore-addominale — interrotta e ripresa (04/09, 22:57)

Il lancio delle 18:09 e' morto in un modo nuovo: **il computer e' andato in sospensione** durante la riscrittura di chiarezza. `rev5:chiarezza` ha fallito su tutti e sei i tentativi («Your computer went to sleep mid-response»), e il workflow ha restituito `consegnabili: []` — cioe' niente.

## Il report diceva niente, il disco diceva quasi tutto

Sul disco c'era `v6-chiarezza.md`, **140 KB, completa**. La riscrittura era finita; l'agente e' morto dopo. Verificato prima di fidarsene:

| | v5 | v6 |
|---|---|---|
| capitoli | 17 | 17 |
| PMID | 182 | 182 |
| «Per te» | 15 | 15 |
| «In una riga» | 15 | 15 |
| «Le tre cose da ricordare» | 15 | 15 |
| ultima riga | voce 45 di bibliografia | identica |

Collaudo deterministico v5→v6: **identita' 80,4%**, delta +0,4%, contatori invarianti (45 PMID, 13 etichette, 15 slot, 8 uscite). I due bloccanti — `TABELLE_FUORI_SPECIFICA` (9 righe) e `SCRIPT_TROPPO_LUNGO` (114 parole contro 100) — sono **ereditati**: rieseguito lo script su v4→v5, stesse identiche 9 righe e stesso script da 114 parole. Appartengono all'asciugatura, non alla riscrittura.

## Mancava solo la Mappa

`mappa-v6.md` non era stata scritta: l'agente e' morto fra la Bibbia e la Mappa. E il 6o livello si ferma senza — il prompt dice testualmente *«Leggi la v6 e la mappa-v6. Se non esistono, fermati e dillo»*.

Due strade: rilanciare la riscrittura intera, buttando 140 KB buoni e circa un milione di token, oppure **promuovere `mappa-v5` a `mappa-v6`**, che e' esattamente il fallback che il workflow applica da solo quando la riscrittura fallisce. Scelta la seconda, perche' la parte cara era gia' fatta e bene.

**Costo dichiarato, non nascosto:** la Mappa non ha ricevuto la semplificazione del 5o livello. Resta nel registro della v5 mentre la Bibbia e' semplificata. Il 6o livello ci passa sopra comunque e produce la `mappa-finale`, quindi la lingua e' coperta; la differenza e' solo di lessico, ed e' su una pagina di sintesi.

## Ripresa

Rilanciata con `stati` completo di tutti i 23 file gia' su disco: salta i primi cinque livelli e riparte dal **6o livello (lingua)**. Restano da fare lingua, collaudo e consegna.

---

# Esito — gonfiore-addominale CHIUSA (10/09, 12:29)

Il rilancio del 04/09 alle 22:57 non era mai partito davvero: sul disco, sei giorni dopo, c'erano ancora solo `v6-chiarezza.md` e la `mappa-v6` promossa a mano. Ripreso dallo stesso punto — 9 agenti, 728 mila token, 40 minuti, contro le 4 ore delle catene intere. La ripresa da `stati` ha fatto il suo mestiere: nessuno dei primi cinque livelli e' stato rieseguito.

## La compensazione fuori tabella e' diventata un comportamento del 6o livello

Verdetto **NON CONSEGNABILE**, ma per la prima volta con **una sola** violazione aperta invece di tre o quattro. Il conteggio delle righe fuori specifica, fatto a mano su entrambi i file:

| | righe fuori specifica |
|---|---|
| v5 | 9 |
| v7 consegnata | **1** |

Otto su nove rientrate **senza perdere una parola**. Ed e' rientrata la cosa che su artrite e piedi-gonfi si era persa due volte: la tabella delle bandiere rosse. Le due righe accorciate portano la loro compensazione nel paragrafo sotto, nella forma esatta che su piedi-gonfi avevo dovuto scrivere a mano:

> «Nella riga della distensione con gambe o caviglie gonfie vale anche **un peso in aumento**. La familiarita' da contare e' quella **di primo grado**.»

Non e' un caso fortunato: e' la stessa toppa, applicata stavolta dal livello che prima produceva il difetto.

## L'unica violazione, e perche' andava riparata comunque

Riga GLP-1, cella centrale: `Curante; 112 se alvo chiuso a feci e gas`, nove parole contro otto. **Era gia' fuori specifica nella v5** — quindi non e' una perdita di conservazione — e la Mappa portava la clausola per esteso, quindi i due documenti non si contraddicevano. Ma sta nella tabella di sicurezza e il codice la conta bloccante.

Riparata con la convenzione che il documento si e' gia' dato, non accorciando il contenuto:

| | testo |
|---|---|
| cella | `Curante; 112 se alvo chiuso` |
| paragrafo sotto | «Nella riga del GLP-1, "alvo chiuso" vuol dire chiuso **a feci e gas**: e' quella la condizione che fa scattare il 112.» |

Collaudo deterministico rilanciato su v6→v7: **CONSEGNABILE, 0 bloccanti**, identita' 98%, delta +1,0%, contatori tutti fermi (45 PMID, 13 etichette, 15 «Per te», 15 slot, 8 uscite). Restano tre avvisi, tutti ereditati dall'asciugatura e non dalla lingua: 19.140 parole contro un tetto di 13.000, glossario a 42 termini contro 40, un box «Condizioni associate» fuori dai quattro ammessi.

`.docx` rigenerati e verificati aprendo l'XML: la cella accorciata e la frase di compenso sono entrambe dentro. `Bibbia_Gonfiore_Addominale.docx` (73 KB) e `Mappa_Gonfiore_Addominale.docx` (17 KB).

## Segnali per Carlos

Cinque punti di contenuto che nessuna riscrittura chiude. Due sono recidive del corpus, non di questo documento:

1. **Cap. 8, «Perche' si indaga da monte» contro la Road Map** — la lista e' ordinata con due metri. Il testo dichiara la gerarchia (regolazione sopra, contenitore sotto, contenuto per ultimo), poi la Road Map mette al passo 1 la circonferenza, che e' il contenitore, e al passo 2 l'attivazione con dentro la frase «e' il piano piu' a monte, e per questo si interroga per primo» — scritta al secondo posto. O la numerazione segue la gerarchia, o il passo 1 esce dalla numerazione come gia' fa il filtro sul cibo.
2. **Cap. 8, la regola tolta e non attenuata** — identica per forma ad artrite: si dichiara inapplicabile la distinzione Centro di Coordinazione / Centro di Percezione e non si mette niente che scelga un bersaglio al suo posto. Resta scoperto il criterio con cui decidi dove metti le mani. **Terza condizione di fila** (reflusso-gastrico, artrite, gonfiore-addominale): non e' un difetto di questa Bibbia, e' un buco dell'impianto.
3. **Cap. 8, marker 5 contro il caso di Silvia** — sul secondo pattern nessun marker fuori piano sopravvive. Il dominante e' la soglia, la leva dichiarata e' attivazione piu' soglia, e i due marker scelti (algometro e giorni con cambio di vestito) stanno **entrambi dentro un piano trattato**. Tre riscritture hanno reso il giro piu' corto e la contraddizione piu' leggibile; nessuna l'ha sciolta.
4. **Cap. 8, il caso di Silvia, secondo buco** — il testo elenca come normali tutti e tre i reperti che il documento sa produrre con le mani (escursione del diaframma, parete, coste basse), e sette righe dopo pone come condizione del ciclo «un reperto muscolo-scheletrico tuo, documentato in cartella anche quando il metro non si muove». Non ne nomina uno che possa restare. Il lettore finisce il caso lavorato senza sapere se Silvia sia un ciclo o un invio.
5. **Cap. 6, cella «Abbastanza» contro Cap. 9, 11 e 12** — la tabella promette «Abbastanza» sul pattern «Gonfiore senza distensione»; ma il Cap. 9 rinvia lo strumento con l'etichetta piu' alta proprio «quando il metro non si muove», il Cap. 12 dice che lo strumento del metro fermo e' l'1b (IPOTESI, un solo randomizzato senza braccio placebo) e il Cap. 11 da' IPOTESI a entrambe le leve manuali. Le quattro affermazioni insieme promettono meno di quella parola. Non si riscrive senza decidere il merito.

## «driver»: quinta condizione di fila, e la tabella e' ancora vuota

Il 6o livello lo segnala di nuovo, insieme a *scope* (×2) e *claim*. La tabella «Correzioni attive» del registro porta ancora la riga `(vuoto)`, e la sua intestazione dice **«Pattern confermati da Carlos»**: non la riempio io. Ma cinque condizioni di fila sono un pattern confermato dai fatti, e finche' la riga non c'e' l'autore riparte ogni volta con lo stesso calco.

## Prossima

**diarrea-ricorrente**, lanciata. Restano 19.

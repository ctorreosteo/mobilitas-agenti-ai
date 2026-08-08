# Registro delle deviazioni dal metodo

**A cosa serve.** Quando un documento si discosta dall'architettura interna (i cinque modelli, il Motore Clinico, i documenti di metodo) **perché quell'elemento del metodo è fattualmente sbagliato**, la deviazione si annota qui.

Senza questo registro lo stesso conflitto si riapre **su ogni condizione**: 58 documenti che litigano 58 volte con lo stesso errore del metodo, ognuno risolvendolo a modo suo. Con il registro il conflitto si risolve **una volta**, e i documenti successivi nascono già allineati.

> **Nota sulle voci storiche.** Le voci nate prima della separazione fra Bibbie e Procedure sono state **riancorate ai documenti di metodo di questa cartella**: dove citavano `architettura-procedura.md` ora citano `architettura-bibbia.md`, e i riferimenti all'esempio canonico degli acufeni — file che qui non esiste — sono stati sostituiti con il capitolo della Bibbia in cui la stessa formulazione ricomparirebbe. La **sostanza** della deviazione resta invariata e vincolante.

## Come funziona

1. Un revisore (tipicamente `fisioterapista-ebp`, `neuromodulazione`, `specialista` o `modelli`) rileva che un elemento prescritto dal metodo è contraddetto dalla fisiologia o dall'evidenza.
2. Il direttore applica la correzione nel documento e **apre una voce qui**, con stato `PROPOSTA`.
3. `fedelta-bibbia` legge questo file **prima** di fare l'audit: una deviazione già registrata non è un'infedeltà da segnalare, è una decisione presa.
4. L'autore legge questo file **prima** di scrivere una nuova Bibbia: non reintroduce elementi già corretti.
5. **La ratifica è umana.** Solo Carlos porta una voce da `PROPOSTA` a `RATIFICATA` (e aggiorna il documento di metodo) o a `RESPINTA`. Nessun agente può ratificare da solo: il metodo è dello studio, non del sistema.

## Stati

| Stato | Significato |
|---|---|
| `PROPOSTA` | Il sistema ha rilevato il conflitto e corretto la Bibbia. In attesa di giudizio umano. |
| `RATIFICATA` | Carlos ha accettato: il documento di metodo va aggiornato (o è già aggiornato). Vincolante per le Bibbie future. |
| `RESPINTA` | Carlos ha deciso che vince il metodo. Le Bibbie tornano alla formulazione originale. |

## Formato di una voce

Una voce per deviazione. Sempre con una **fonte**: una deviazione senza fonte non si registra, si scarta.

---

## Voci

### D-001 · Soglia della frequenza respiratoria come segno di simpaticotonia

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-04 |
| **Condizione di emersione** | Reflusso gastroesofageo (v7) |
| **Ambito** | Trasversale — riguarda ogni condizione che usa il test del respiro |
| **Elemento del metodo** | Test del respiro nel Sistema Dominante: **>16 atti/min = simpaticotonia** |
| **Perché è sbagliato** | Il range fisiologico normale a riposo nell'adulto è ~12-20 atti/min. 16 cade **dentro** la norma e non è una soglia validata di attivazione simpatica: una soglia assoluta in quel punto classifica come "simpaticotonici" soggetti normali. |
| **Cosa fa la procedura** | Sostituisce la soglia assoluta con la **variazione intra-paziente sulla baseline** (conteggio su 60 s, senza avvisare il paziente), che è il confronto che regge. |
| **Se ratificata** | Aggiornare il documento del Sistema Dominante: soglia relativa alla baseline, non assoluta. |

---

### D-002 · Direzione della leva vagale sulle TLESr

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-04 |
| **Condizione di emersione** | Reflusso gastroesofageo (v5→v7) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui si invoca "aumentare il tono vagale" come leva terapeutica |
| **Elemento del metodo** | Modello Neurologico: l'aumento del tono vagale come leva per normalizzare la funzione viscerale. Vedi anche `direttore-osteopatico-modelli/references/cinque-modelli.md`, sezione 3. |
| **Perché è sbagliato** | Le TLESr sono un riflesso **vago-vagale a efferenza vagale inibitoria**: è il vago a comandare il rilasciamento dello sfintere. Il blocco colinergico (atropina) **riduce** le TLESr, e il picco post-prandiale coincide con tono vagale cardiaco **basso**. "Più vago = meno reflusso" non ha direzione stabilita e la farmacologia suggerisce il contrario. |
| **Cosa fa la procedura** | Riobiettiva il blocco su **down-regulation dell'arousal e dell'amplificazione del sintomo**, non sulla riduzione degli episodi. La leva difendibile resta l'**afferenza distensiva gastrica** più la **barriera crurale**. I sub-occipitali sono dichiarati down-regulation aspecifica, non accesso al vago (che esce dal forame giugulare). |
| **Se ratificata** | Rivedere la formulazione della leva vagale in `cinque-modelli.md` (modello Neurologico), che è il metro del revisore `modelli`. |

---

### D-003 · Ruolo dello stress nel sintomo viscerale funzionale

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-04 |
| **Condizione di emersione** | Reflusso gastroesofageo (v5→v7) |
| **Ambito** | Trasversale — riguarda ogni condizione funzionale con componente comportamentale |
| **Elemento del metodo** | Modello Comportamentale: lo stress come **generatore** di episodi per via motoria (stress → svuotamento rallentato → distensione → più episodi). |
| **Perché è sbagliato** | La catena motoria è in larga parte di derivazione animale. Nell'uomo lo stress acuto non aumenta il carico di reflusso, mentre nei pazienti sintomatici **riduce la latenza al sintomo e ne aumenta l'intensità**: agisce sulla **percezione**, non sull'esposizione. |
| **Cosa fa la procedura** | Riclassifica lo stress come **amplificatore percettivo, non generatore**. Conseguenza operativa dichiarata prima di iniziare: nel paziente stress-dominante l'esito atteso è **VAS giù a parità di numero di episodi**. |
| **Se ratificata** | Estendere la formulazione "amplificatore, non generatore" al modello Comportamentale in `cinque-modelli.md`. |

---

### D-004 · "Effetto neurobiologico del tocco" (ossitocina / cortisolo / filtro talamico) come meccanismo dimostrato

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-04 |
| **Condizione di emersione** | Acufene (v1) |
| **Ambito** | Trasversale — riguarda ogni procedura che usa la sezione "Perché l'osteopatia è superiore all'approccio standard" |
| **Elemento del metodo** | Il metodo indica come modello per l'acufene la tripletta *Decompressione fisica / Reset propriocettivo / **Effetto neurobiologico del tocco***, esplicitata come "l'OMT stimola il rilascio di ossitocina e abbassa il cortisolo, agendo **direttamente sul filtro talamico** dell'acufene". Nelle Bibbie la formulazione ricomparirebbe nel capitolo «Perché le mani possono cambiare qualcosa». |
| **Perché è sbagliato** | È un claim di meccanismo presentato come fatto. L'evidenza sulle variazioni ormonali dopo OMT è minima e di bassa qualità: la revisione sistematica dedicata (*Osteopathic Manipulation as a Method of Cortisol Modification: A Systematic Review*, Cureus 2023, [PMID 37123793](https://pubmed.ncbi.nlm.nih.gov/37123793/)) include **4 soli studi, 135 partecipanti totali** e non consente di quantificare l'effetto. Nessuno studio ha misurato ossitocina, cortisolo o attività talamica dopo trattamento manuale in pazienti con acufene, né alcun effetto "sul filtro talamico". |
| **Cosa fa la procedura** | Sostituisce il claim con **down-regulation aspecifica dell'attivazione**, dichiarata come parte del contesto terapeutico (contatto lento + respiro) e non come meccanismo neuroendocrino dimostrato. Coerente con D-002 (i sub-occipitali non sono un accesso al vago). |
| **Se ratificata** | Riformulare il terzo punto della tripletta in `architettura-bibbia.md` (es. *"Modulazione dell'attivazione attraverso il contatto — down-regulation aspecifica, dichiarata come tale"*), con etichetta non superiore a IPOTESI nel capitolo «Perché le mani possono cambiare qualcosa». |
| **Integrazione 2026-08-07** | Anche la formulazione **sostitutiva** («down-regulation aspecifica») ha ora un dato contro: la meta-analisi più ampia sugli effetti psicofisiologici dell'OMT — 20 RCT — non trova effetto su **ansia** e **stress** e trova la **conduttanza cutanea aumentata** (g=0,67, p=0,05), cioè nella direzione dell'attivazione (Gordon, *BMJ Open* 2025, [PMID 39920074](https://pubmed.ncbi.nlm.nih.gov/39920074/)). La voce non cambia stato: cambia il fatto che nemmeno la **direzione** dell'effetto è stabilita, e va scritto così in ogni Bibbia che invochi il contatto come modulatore dell'attivazione. |
| **Integrazione 2026-08-08** | Sul **rachide cervicale** la direzione non è più incerta, ed è nel verso opposto a quello che il metodo suppone. Dopo mobilizzazione cervicale, con disegno randomizzato **controllato con placebo e in doppio cieco** su 30 soggetti con dolore cervicale insidioso, la conduttanza cutanea **aumenta** (p<0,002) e la temperatura cutanea **scende** (p<0,02), insieme a ipoalgesia e riduzione dell'attività dei flessori superficiali (Sterling, *Man Ther* 2001, [PMID 11414776](https://pubmed.ncbi.nlm.nih.gov/11414776/)). Formulazione da usare, al posto di "la direzione non è stabilita": *"dove è stata misurata sulla cervicale, contro placebo e in cieco, la direzione va verso l'attivazione, non verso la calma."* Vale per ogni Bibbia che invochi il contatto cervicale come leva calmante. |

---

### D-005 · Lavoro suturale occipito-mastoideo come leva sul deflusso venoso giugulare

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-04 |
| **Condizione di emersione** | Acufene (v2) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui si invoca il "drenaggio venoso cranico" come leva manuale (acufene, cefalea, vertigini, congestione del distretto superiore) |
| **Elemento del metodo** | Modello Respiratorio-Circolatorio: la mobilizzazione della sutura occipito-mastoidea come tecnica per "liberare il forame giugulare" e favorire il deflusso venoso cranico. |
| **Perché è sbagliato** | È un'inferenza dalla topografia, non una misura: che la giugulare interna esca dal forame giugulare fra occipite e temporale non implica che la mobilità suturale nell'adulto modifichi il deflusso venoso. Nell'adulto le suture craniche sono in larga parte interdigitate e progressivamente obliterate, e **nessuno studio ha misurato deflusso venoso cranico o pressione perilinfatica prima e dopo un lavoro suturale**. Un razionale anatomico non giustifica una tecnica. |
| **Cosa fa la procedura** | Rimuove la tecnica e dichiara il perimetro (Parte IV, §Sistema Circolatorio-Idraulico, *Perimetro*). Il blocco C resta sul gradiente pressorio a valle — stretto toracico, prima costa, scaleni, diaframma — con effetto sull'acufene dichiarato **PLAUSIBILE, non validato**. |
| **Se ratificata** | Rimuovere il lavoro suturale drenante dai riferimenti al modello Respiratorio-Circolatorio, o riformularlo come tecnica senza claim di drenaggio. |

---

### D-006 · Il Nucleo Cocleare Dorsale invocato come bersaglio di un drive "tonico"

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-04 |
| **Condizione di emersione** | Acufene (v2) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui l'ipertono muscolare viene descritto come "rumore continuo in ingresso" su un nucleo del tronco (acufene, cefalea, vertigini cervicogeniche) |
| **Elemento del metodo** | Modello Neurologico: l'ipertono di sub-occipitali e masticatori come **drive tonico** che alimenta il nucleo cocleare dorsale e "tiene alto" il suono; il trattamento manuale come correzione della plasticità maladattiva. |
| **Perché è sbagliato** | La convergenza somatosensoriale sul DCN documentata nei modelli animali è **fasica e timing-dipendente**, non tonica: l'unica prova di concetto umana sulla stimolazione bimodale usa un **pairing a 5-10 ms, 30 min/die per 28 giorni, con ritorno al basale nel washout** (Shore, Roberts e Langguth, *Nat Rev Neurol* 2016 — [PMID 26868680](https://pubmed.ncbi.nlm.nih.gov/26868680/)). Un drive tonico dall'ipertono muscolare non è mai stato dimostrato, e nessuno ha misurato attività del DCN o guadagno centrale nell'uomo dopo trattamento manuale. Attribuire alle mani quel meccanismo è un claim di meccanismo presentato come fatto. |
| **Cosa fa la procedura** | Scrive **riduzione del drive nocicettivo cervico-trigeminale** (l'unico anello documentato nell'uomo) e dichiara la proiezione al nucleo cocleare come **inferenza a due anelli, non misura**. Nella lista "cosa non puoi dire" compare esplicitamente che "plasticità maladattiva" non è ciò che fanno le nostre mani (Parte 0 §Neurologico; Parte III §2). |
| **Se ratificata** | Correggere la formulazione del meccanismo cervico-uditivo nei documenti di metodo e nel capitolo «Cosa si rompe» di ogni Bibbia che lo tratti: convergenza fasica, non drive tonico. |

---

### D-007 · Segmento di proiezione viscero-somatica di stomaco ed esofago

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-04 |
| **Condizione di emersione** | Reflusso gastroesofageo (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui si cerca la zona riflessa dello stomaco o dell'esofago distale |
| **Elemento del metodo** | `motore-clinico.md`, §2, 4° Sistema Viscerale: *"Stomaco/esofago (catena anteriore, fascia pre-vertebrale, vago/frenico) → rigidità in flessione, **dolore a C6-C7, spalla sinistra**, chiusura anteriore."* |
| **Perché è sbagliato** | Confonde due vie distinte. Le afferenze spinali di stomaco ed esofago distale viaggiano con il **nervo grande splancnico, T5-T9**: la zona di riferimento è dorsale media ed epigastrica ([StatPearls, *Anatomy, Thorax, Greater Splanchnic Nerves*, NBK500026](https://www.ncbi.nlm.nih.gov/books/NBK500026/)). La proiezione **C3-C5 / apice della spalla** è un fenomeno **frenico**, generato dall'irritazione del peritoneo e della pleura diaframmatici (segno di Kehr), non dallo stomaco. C6-C7 non appartiene a nessuna delle due. Indirizzare l'indagine sulla cervicale bassa fa cercare la zona riflessa gastrica in un segmento che non la riceve. |
| **Cosa fa la Bibbia** | Scrive **T5-T9** come segmento di riferimento gastro-esofageo nel capitolo «Le strutture in gioco» e nel modello Neurologico, e mantiene il **frenico C3-C5** come collegamento collo-diaframma, dichiarato separatamente dalla proiezione gastrica. Formulazione usata: *"Lo stomaco proietta su T5-T9: se cerchi il reflusso in cervicale bassa, stai cercando nel posto sbagliato."* |
| **Se ratificata** | Correggere la riga "Stomaco/esofago" nella sezione Viscerale di `motore-clinico.md`: proiezione dorsale T5-T9 via grande splancnico; la via frenica C3-C5 va indicata a parte, come riferimento diaframmatico e non gastrico. |

---

### D-008 · "Si indaga dall'alto della piramide" letto come coordinata anatomica

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-04 |
| **Condizione di emersione** | Reflusso gastroesofageo (Bibbia v2, rilevata dall'audit di fedeltà sulla v2) |
| **Ambito** | Trasversale — riguarda ogni condizione sotto il diaframma, e in generale ogni uso del principio del Sistema Dominante |
| **Elemento del metodo** | `motore-clinico.md`, §1 e §3: *"il sistema dominante è, di norma, il più alto nella piramide che risulti disfunzionale"*, *"si indaga dall'alto verso il basso"*, *"Indaga dall'alto della piramide"*. |
| **Perché è ambiguo** | "Alto" è una parola con due significati: alto nella **gerarchia funzionale** (il senso voluto) e alto nel **corpo** (il senso che il lettore applica davanti a un paziente). Su una condizione viscerale sotto-diaframmatica la lettura anatomica porta a cercare in cervicale, che è esattamente l'errore corretto da D-007: lo stomaco proietta su T5-T9, non su C6-C7. L'ambiguità non è teorica — è la stessa che genera la riga sbagliata del metodo già registrata. |
| **Cosa fa la Bibbia** | Sostituisce "dall'alto della piramide" con **"da monte sul piano funzionale"**, e lo dichiara a lettera nel capitolo «Come ragiono davanti a questo paziente»: *"«A monte» non è una coordinata anatomica: non vuol dire più vicino alla testa"*. La gerarchia resta identica: cambia solo la parola che la nomina. |
| **Se ratificata** | Sostituire "più alto nella piramide" / "dall'alto verso il basso" con "più a monte sul piano funzionale" in `motore-clinico.md` (§1 e §3), mantenendo la piramide come immagine della gerarchia di comando. |

---

### D-009 · "Il reflusso causa la cervicalgia" come esempio canonico del Motore Clinico

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-07 |
| **Condizione di emersione** | Reflusso gastroesofageo (Bibbia v1, nuovo impianto) |
| **Ambito** | Trasversale — riguarda ogni Bibbia che colleghi un viscere a un dolore muscolo-scheletrico a distanza |
| **Elemento del metodo** | `motore-clinico.md`, §4: *"Esempio canonico: una **cervicalgia** (fascia = CP) può essere **causata** da un **reflusso** (viscerale), alimentato da uno stato d'ansia e mantenuto da un diaframma bloccato."* |
| **Perché è sbagliato** | La catena è presentata come nesso causale, e nessuno studio l'ha stabilita. L'unico dato disponibile che collega reflusso e collo è la mobilità cervicale in Eguaras 2019 ([PMID 31635110](https://pubmed.ncbi.nlm.nih.gov/31635110/)): una differenza fra gruppi di **33,89 gradi dopo una singola tecnica viscerale**, magnitudine implausibile per un'articolazione sana e più compatibile con un problema di misura che con un effetto. Le afferenze gastro-esofagee entrano in T5-T9 (vedi D-007), non in cervicale; il solo ponte anatomico verso il collo è il frenico C3-C5, che è una via **diaframmatica**, non gastrica. Presentare la catena come causale reintroduce, per la porta di servizio, l'errore che D-007 e D-008 hanno già corretto. |
| **Cosa fa la Bibbia** | Mantiene la co-occorrenza come **cross-reference clinico** in «Non è una condizione sola», con etichetta **IPOTESI** e la frase esplicita: *"che il reflusso **causi** una cervicalgia non è dimostrato"*. Usa la mobilità cervicale come marker solo dichiarandone il limite di misura, in «Come ragiono davanti a questo paziente». Il collegamento collo-diaframma resta descritto come frenico, e separato dalla proiezione gastrica. |
| **Se ratificata** | Riformulare l'esempio canonico di `motore-clinico.md` §4 come **co-occorrenza clinica su terreno comune** (diaframma, cerniera dorso-lombare, stato di attivazione), non come catena causale, e sostituire la parola "causata" con "che condivide il terreno con". |

---

### D-010 · L'etichetta DIMOSTRATO non copre l'evidenza epidemiologica causale

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-07 |
| **Condizione di emersione** | Reflusso gastroesofageo (Bibbia v2, rilevata dall'audit di fedeltà di 2° livello) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui il fattore causale meglio stabilito è epidemiologico e non sperimentale |
| **Elemento del metodo** | `architettura-bibbia.md`: DIMOSTRATO = *"RCT o revisioni sistematiche solide"*. |
| **Perché è incompleto** | Su alcuni fattori causali il livello di prova più alto che esisterà mai **non è un RCT**. Sul peso e il reflusso la prova migliore al mondo è una coorte con relazione dose-risposta **bidirezionale**: l'indice di massa corporea correla con i sintomi su 10.545 donne, un aumento di oltre 3,5 punti quasi triplica il rischio anche partendo da un peso normale (Jacobson, *N Engl J Med* 2006, [PMID 16738270](https://pubmed.ncbi.nlm.nih.gov/16738270/)), e perdere peso li riduce in proporzione alla perdita (Ness-Jensen, *Am J Gastroenterol* 2013, [PMID 23358462](https://pubmed.ncbi.nlm.nih.gov/23358462/)). Randomizzare le persone a ingrassare non è fattibile né etico. Con la definizione stretta, quel dato va declassato a PROBABILE e finisce sotto una leva manuale che ha prove molto più deboli: l'etichetta smette di ordinare la realtà. |
| **Cosa fa la Bibbia** | Estende DIMOSTRATO a **coorti ampie con relazione dose-risposta** e a **misura sperimentale diretta nell'uomo**, dichiarando l'estensione nel Capitolo 0 e ripetendola nel punto d'uso (*"DIMOSTRATO come fattore causale, nel senso che il Capitolo 0 dà a coorti ampie… Non sono RCT, e va detto"*). Le quattro etichette restano quattro. |
| **Se ratificata** | Riscrivere la riga DIMOSTRATO in `architettura-bibbia.md` come *"RCT o revisioni sistematiche solide; coorti ampie con relazione dose-risposta; misura sperimentale diretta nell'uomo — dichiarando quale dei tre"*. |

---

### D-011 · La Mappa concettuale non ha un blocco per gli strumenti attivi

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-07 |
| **Condizione di emersione** | Reflusso gastroesofageo (Mappa v2, rilevata dall'audit di fedeltà di 2° livello) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui il Capitolo 12 della Bibbia è attivo |
| **Elemento del metodo** | `mappa-concettuale.md`: *"Sei blocchi, sempre gli stessi, sempre in quest'ordine."* |
| **Perché è incompleto** | La specifica della Mappa non è stata aggiornata quando l'architettura ha introdotto il **Capitolo 12 condizionale**. Su questa condizione le leve meglio documentate — esercizio respiratorio, peso, posizione notturna — **non sono manuali**: una Mappa a sei blocchi le omette e comunica il contrario di ciò che la Bibbia sa, che è esattamente il ragionamento di proporzione con cui l'architettura giustifica il Capitolo 12. |
| **Cosa fa la Mappa** | Aggiunge un **settimo blocco condizionale**, «Cosa fa il paziente da solo», attivo solo quando il Capitolo 12 è attivo, e lo dichiara in coda alla pagina. I blocchi fuori standard della v2 («Le zone che non si premono», «I tre limiti da dire ad alta voce») sono invece **riassorbiti**: il primo dentro le bandiere rosse, il secondo in una riga sotto la tabella dei meccanismi. |
| **Se ratificata** | Aggiungere a `mappa-concettuale.md` un blocco condizionale fra il 4 e il 5, con la stessa condizione di attivazione del Capitolo 12 della Bibbia. |

---

### D-012 · Il "reset propriocettivo" come effetto dimostrato del trattamento manuale

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-08 |
| **Condizione di emersione** | Vertigini (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui si invoca la normalizzazione della propriocezione come effetto del gesto manuale (vertigini, cervicalgia, colpo di frusta, problemi posturali, scoliosi) |
| **Elemento del metodo** | La tripletta indicata dal metodo come modello di razionale (*Decompressione fisica / **Reset propriocettivo** / Effetto neurobiologico del tocco*), già in parte corretta da D-004 sul terzo termine. Nelle Bibbie la formulazione ricompare nel capitolo «Perché le mani possono cambiare qualcosa». |
| **Perché è sbagliato** | È l'unico dei tre termini che è stato misurato direttamente, e il risultato è negativo. Nell'unico RCT che ha valutato insieme escursione, riposizionamento del capo ed equilibrio in pazienti con vertigine cervicogenica (86 partecipanti, tre bracci, cieco sul valutatore, follow-up 12 settimane), la terapia manuale ha migliorato l'escursione cervicale in tutte e sei le direzioni e **non** ha prodotto effetti né sull'accuratezza di riposizionamento del capo né sull'equilibrio (Reid, *Arch Phys Med Rehabil* 2014, [PMID 24792139](https://pubmed.ncbi.nlm.nih.gov/24792139/)). Nello stesso programma di ricerca il sintomo migliorava (Reid, *Phys Ther* 2014, [PMID 24336477](https://pubmed.ncbi.nlm.nih.gov/24336477/)): l'effetto clinico esiste, ma **non passa** per la variabile propriocettiva che il metodo gli attribuisce. Ciò che sposta il riposizionamento del capo è l'esercizio sensomotorio, non la mano (Sremakaew, *Musculoskelet Sci Pract* 2023, [PMID 36414518](https://pubmed.ncbi.nlm.nih.gov/36414518/)). |
| **Cosa fa la Bibbia** | Scrive che la leva manuale agisce su **escursione, tono profondo e dolore**, con effetto misurato su **intensità e frequenza del sintomo**, ed etichetta PROBABILE. Dichiara esplicitamente, in «Come ragiono davanti a questo paziente» e in «Cosa dice la scienza», che riposizionamento del capo ed equilibrio **non** si sono mossi. Attribuisce la correzione propriocettiva allo strumento attivo (Capitolo 12), non alla mano. |
| **Se ratificata** | Sostituire "reset propriocettivo" con "recupero di escursione e riduzione del drive nocicettivo cervicale" nei documenti di metodo, e vietare l'uso di "ricalibrazione propriocettiva" come effetto attribuito al gesto manuale senza misura. |

---

### D-013 · Il vestibolo trattato come "inquinatore recettoriale" da normalizzare dal collo

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-08 |
| **Condizione di emersione** | Vertigini (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui il metodo elenca il vestibolo fra i recettori "inquinatori" (vertigini, labirintite, cefalea, acufeni, problemi posturali) |
| **Elemento del metodo** | `motore-clinico.md`, §2, 1° Sistema Neurologico: *"I tre «Inquinatori» (recettori): Occhio, ATM, **Vestibolo** — un micro-sbilanciamento usa i muscoli del collo come tiranti antigravitari."* Il vestibolo compare come input periferico da compensare lavorando sul collo. |
| **Perché è sbagliato sulla condizione in cui il vestibolo è il sintomo** | Sulla vertigine quel framing inverte la priorità clinica e produce due errori concreti. (1) **Triage:** la sindrome vestibolare acuta è la presentazione in cui va escluso un evento cerebrovascolare, con un esame oculomotore a tre passi che nella serie originale era 100% sensibile e 96% specifico per ictus (Kattah, *Stroke* 2009, [PMID 19762709](https://pubmed.ncbi.nlm.nih.gov/19762709/)); il 3,2% degli accessi in pronto soccorso per vertigine è un evento cerebrovascolare (Kerber, *Stroke* 2006, [PMID 16946161](https://pubmed.ncbi.nlm.nih.gov/16946161/)). Un "recettore da normalizzare" non è una categoria che porta a fermarsi. (2) **Efficacia:** la causa singola più comune ha un trattamento specifico e non manuale-osteopatico — la procedura di riposizionamento canalare, OR 4,92 per la risoluzione completa su 11 studi e 745 pazienti (Hilton & Pinder, *Cochrane* 2014, [PMID 25485940](https://pubmed.ncbi.nlm.nih.gov/25485940/)) — e il deficit vestibolare periferico ha come leva l'esercizio vestibolare, con evidenza da moderata a forte su 39 studi e 2.441 partecipanti (McDonnell & Hillier, *Cochrane* 2015, [PMID 25581507](https://pubmed.ncbi.nlm.nih.gov/25581507/)). Trattare il vestibolo come input da compensare dal collo porta a tenere in studio pazienti la cui leva efficace sta altrove. |
| **Cosa fa la Bibbia** | Non usa la categoria "inquinatore" per il vestibolo. Lo tratta come **sorgente primaria** in un sistema a tre ingressi, mette il pattern posizionale e la sindrome vestibolare acuta fra le uscite di triage, e dichiara che il peso del collo **cresce** quando il labirinto perde funzione (Bronstein & Hood, *Brain Res* 1986, [PMID 3487371](https://pubmed.ncbi.nlm.nih.gov/3487371/)) — il che rende il collo un bersaglio *dopo* l'inquadramento vestibolare, non al posto suo. |
| **Se ratificata** | In `motore-clinico.md` limitare la voce "Vestibolo" fra gli inquinatori alle condizioni in cui il sintomo **non** è vestibolare, e aggiungere la nota che, quando il sintomo presentato è vertigine o instabilità, il vestibolo è oggetto di triage medico e non di normalizzazione riflessa. |

---

### D-014 · «Non trattare quasi mai il Centro di Percezione» applicato alla cervicalgia

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-08 |
| **Condizione di emersione** | Cervicalgia (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione muscolo-scheletrica in cui l'intervento con la migliore evidenza si applica sulla regione sintomatica (cervicalgia, lombalgia, tendinopatie, spalla) |
| **Elemento del metodo** | `motore-clinico.md`, §2, 6° Sistema Fasciale: *"La regola d'oro: **NON trattare quasi mai il CP.** Cerca il **CC densificato** lungo la sequenza miofasciale."* |
| **Perché è sbagliato** | Presa alla lettera, la regola esclude proprio gli interventi che su questa condizione hanno le prove migliori al mondo, e che si applicano **esattamente sulla regione in cui il paziente sente male**. La terapia manipolativa cervicale e l'esercizio a basso carico dei flessori cervicali profondi riducono frequenza e intensità della cefalea cervicogenica con effetti mantenuti a 12 mesi su 200 pazienti randomizzati ([Jull, *Spine* 2002, PMID 12221344](https://pubmed.ncbi.nlm.nih.gov/12221344/)); manipolazione e mobilizzazione **cervicali** producono cambiamenti su dolore e funzione in 51 studi controllati ([Gross, *Cochrane Database Syst Rev* 2015, PMID 26397370](https://pubmed.ncbi.nlm.nih.gov/26397370/)); il rinforzo **cervico**-scapolo-toracico ha evidenza di qualità moderata sul dolore cervicale cronico ([Gross, *Cochrane* 2015, PMID 25629215](https://pubmed.ncbi.nlm.nih.gov/25629215/)). Una regola di metodo che vieta il bersaglio con la migliore evidenza disponibile non è una regola conservativa: è una regola falsificata dai dati. |
| **Cosa fa la Bibbia** | Restringe il principio all'**indagine** e non alla scelta del bersaglio, e lo dichiara a lettera nel capitolo «Come ragiono davanti a questo paziente»: *"quel principio vale per la ricerca, non per la scelta del bersaglio… Applicato alla lettera, «non trattare dove fa male» escluderebbe l'intervento con la migliore evidenza al mondo su questa condizione. Il principio serve a capire **da dove viene**; non decide dove metti le mani."* Il criterio di verifica resta intatto: il marker della prova della chiave di volta deve comunque appartenere a un piano non trattato. |
| **Se ratificata** | Riformulare la regola d'oro di `motore-clinico.md` §2 (6° Sistema Fasciale) come regola di **indagine** — *"cerca il CC a monte prima di concludere che la causa sia dove fa male"* — e non come divieto di trattamento della zona sintomatica. |

---

### D-015 · Il cancello d'ingresso a tre uscite non regge le condizioni con urgenze e invii programmati insieme

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-08 |
| **Condizione di emersione** | Vertigini (Bibbia v2, rilevata dall'audit di fedeltà di 2° livello) |
| **Ambito** | Trasversale — riguarda ogni condizione la cui tabella di bandiere rosse contiene sia urgenze (`112`, `Urgente`) sia invii differibili (`Invio`, `Invio programmato`) |
| **Elemento del metodo** | `architettura-bibbia.md`, il cancello d'ingresso: tre uscite, `ROSSO / GIALLO / VERDE`. |
| **Perché è insufficiente** | Dentro un ROSSO unico convivono due comportamenti opposti e si annullano: «il paziente non sale sul lettino» e «si può trattare altro, per iscritto, mentre l'invio segue il suo corso». Lo standard stesso li tiene insieme (*"Se coesiste una disfunzione muscolo-scheletrica autonoma la si può trattare"*), producendo l'ambiguità. Su questa condizione la tabella contiene sia righe `112` (deficit neurologico acuto, sospetta dissecazione) sia righe `Invio programmato` (trauma cervicale remoto senza segni), e la stessa etichetta produrrebbe due condotte incompatibili. |
| **Cosa fa la Bibbia** | Scrive quattro uscite: `ROSSO IMMEDIATO / ROSSO DIFFERITO / GIALLO / VERDE`. Il vincolo duro resta attaccato al ROSSO IMMEDIATO — *"Nessuna eccezione, e nessun reperto positivo scavalca questa uscita"* — e la possibilità di lavorare altrove è confinata al ROSSO DIFFERITO, con dichiarazione scritta che il sintomo è in attesa di inquadramento e non è il bersaglio. |
| **Se ratificata** | Riscrivere il cancello di `architettura-bibbia.md` a quattro uscite, con il criterio di separazione dichiarato: il vocabolario dei tempi (`112`/`Urgente` contro `Invio`/`Invio programmato`) decide in quale dei due ROSSI cade la riga. |
| **Integrazione 2026-08-08 (Cervicalgia, Bibbia v3)** | Sulla cervicalgia lo stesso problema è stato risolto per via della **tabella** invece che dell'uscita: le bandiere rosse stanno in **due blocchi** a tre colonne — Blocco A «rosso immediato, non si tratta nulla in nessun distretto», Blocco B «invio non differibile, si può trattare un altro distretto» — e il cancello resta a tre uscite, con l'uscita ROSSO che si comporta diversamente a seconda del blocco. Lo standard prescrive *una* tabella dedicata a tre colonne. La soluzione è equivalente nella sostanza e ha un vantaggio di lettura: il comportamento sta accanto alla riga che lo attiva, invece che in un'uscita più sotto. Se D-015 viene ratificata, le due formulazioni vanno unificate scegliendone una. |

---

### D-016 · «Il tuo mandato non nasce dalla diagnosi medica» è insostenibile come principio scritto in Italia

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-08 |
| **Condizione di emersione** | Vertigini (Bibbia v2, rilevata dall'audit di fedeltà di 2° livello) |
| **Ambito** | Trasversale — riguarda tutte le Bibbie |
| **Elemento del metodo** | `architettura-bibbia.md`, il blocco del mandato: *"Il tuo mandato non nasce dalla diagnosi medica."* |
| **Perché è sbagliato** | La formulazione secca confonde due piani. Il piano **clinico** — avere qualcosa da trattare oggi — nasce davvero dal reperto e dal marker. Il piano **professionale** no: il DPR 131/2021 riserva la diagnosi al medico e il DPCM 25 marzo 2026 (GU n. 117 del 22 maggio 2026) inquadra l'osteopata come professionista sanitario che opera in riferimento alla diagnosi di competenza medica. Scritta così in un documento interno, la frase è indifendibile davanti a un medico inviante e davanti a un contenzioso. |
| **Cosa fa la Bibbia** | Separa i due piani a lettera, in «Dove finisce il nostro campo»: *"Il mandato **clinico** … nasce da un reperto disfunzionale documentato e da un marker che si muove quando lo tratti. La **cornice professionale** resta quella del profilo: si opera in riferimento alla diagnosi di competenza medica, e quando l'inquadramento manca il canale medico si attiva **contestualmente** al tuo lavoro, non dopo."* Conserva entrambi i corollari: *"Senza reperto e marker non hai un motivo per lavorare nemmeno con la diagnosi in mano"* e *"un reperto positivo non sostituisce l'inquadramento. Hai qualcosa da trattare, non sai cosa ha il paziente."* |
| **Se ratificata** | Riscrivere il blocco del mandato in `architettura-bibbia.md` nella forma a due piani, mantenendo entrambi i corollari attaccati al principio. |

---

### D-017 · Il modello Respiratorio-Circolatorio non è invocabile per intero su ogni distretto

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-08 |
| **Condizione di emersione** | Cervicalgia (Bibbia v2, rilevata dall'audit di fedeltà di 2º livello) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui una delle due metà del modello non ha nessuna misura sul distretto trattato |
| **Elemento del metodo** | `cinque-modelli-osteopatici.md`: il modello Respiratorio-Circolatorio come modello unico, con meccanica ventilatoria e componente circolatoria (ritorno venoso e linfatico, gradienti pressori) invocate insieme. |
| **Perché è incompleto** | Sul rachide cervicale la metà **circolatoria** non ha nessuna misura: nessuno ha quantificato ritorno venoso o drenaggio linfatico cervicale prima e dopo un trattamento manuale. È la stessa famiglia di claim che D-005 ha già smontato sul deflusso giugulare. Invocare il modello intero significa portare dentro la Bibbia una componente senza dato né marker, e su un distretto in cui la metà **ventilatoria** ha invece dati veri (Kapreli, [PMID 19187335](https://pubmed.ncbi.nlm.nih.gov/19187335/); Dimitriadis, [PMID 23958733](https://pubmed.ncbi.nlm.nih.gov/23958733/)) e cinque studi controllati sull'intervento. |
| **Cosa fa la Bibbia** | Dichiara la restrizione a lettera nel Capitolo 7: *"Su questo distretto si usa la sola meccanica ventilatoria: la metà circolatoria del modello — ritorno venoso e linfatico, gradienti pressori — qui non è pertinente e non viene invocata."* Il modello resta uno dei cinque, con la sua etichetta e i suoi segnali; è lo **scope** a essere ristretto, non il modello a essere tolto. |
| **Se ratificata** | Aggiungere a `cinque-modelli-osteopatici.md` la possibilità di una **restrizione di scope dichiarata per distretto**, con la regola che la restrizione va scritta nel modello e motivata dall'assenza di misura, mai dall'assenza di interesse. |

---

### D-018 · La Mappa concettuale non ha un blocco per il ragionamento clinico

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-08 |
| **Condizione di emersione** | Cervicalgia (Mappa v3) |
| **Ambito** | Trasversale — riguarda tutte le Bibbie, perché tutte hanno il Capitolo 8 |
| **Elemento del metodo** | `mappa-concettuale.md`: *"Sei blocchi, sempre gli stessi, sempre in quest'ordine"* — condizione, catena, meccanismi, sottotipi, bandiere rosse, frase per il paziente (più il settimo condizionale sugli strumenti attivi, D-011). |
| **Perché è incompleto** | Nessuno dei sei blocchi contiene il **Motore Clinico**: né la road map, né i marker con le loro soglie, né la regola che il marker della prova appartiene a un piano non trattato. La Mappa è ciò che si riguarda a sei mesi prima di un paziente, ed è esattamente il momento in cui serve l'ordine delle domande e la misura da prendere prima di toccare. Una Mappa che porta i meccanismi e non porta come si sceglie fra loro riassume il **cosa** e perde il **come si decide**, che è il capitolo più caratteristico del metodo. |
| **Cosa fa la Mappa** | Aggiunge un blocco «Come decidi, e su cosa verifichi» fra le bandiere rosse e la frase per il paziente: la road map in sette passi su una riga, i quattro marker con la soglia in tabella, e la riga sulla relazione fra marker e piano trattato. La deviazione è dichiarata in coda alla pagina. |
| **Se ratificata** | Aggiungere a `mappa-concettuale.md` un blocco fisso per il ragionamento clinico, con il vincolo di stare in una riga di road map più una tabella di marker da due a quattro righe. |

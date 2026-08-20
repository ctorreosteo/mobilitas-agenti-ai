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

---

### D-019 · Il tetto di 8.000-13.000 parole non è compatibile con l'insieme delle protezioni dei livelli 2 e 3

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-08 |
| **Condizione di emersione** | Cervicalgia (v5, asciugatura di 4º livello) |
| **Ambito** | Trasversale — riguarda ogni Bibbia che attraversi l'intera catena a sei livelli |
| **Elemento del metodo** | `architettura-bibbia.md`: *"Lunghezza: 8.000-13.000 parole, appendici escluse."* |
| **Perché è incompleto** | La v4 arriva al 4º livello a 18.747 parole di corpo. La mappa di taglio dell'editor è stata applicata per intero — quindici voci RIDONDANTE e diciotto COMPRIMIBILE — e vale ~1.300 parole reali, non le ~4.900 stimate. La differenza non è pigrizia del taglio: è che gli elementi dichiarati **da proteggere** dai livelli 2 (`evidenza-estesa`, dodici voci) e 3 (`apprendimento`, dieci voci; `coerenza`, otto voci) più l'INTOCCABILE dell'editor stesso coprono il **38% del corpo** in blocchi misurabili (aperture, chiusure con i quindici slot «Perché ci sei tu», box di solidità, tabelle) e una quota ulteriore in prosa protetta (metafore, «Come si vede addosso», script al paziente, note di sicurezza). Il tetto e le protezioni sono due regole del metodo che, su una condizione ampia, non possono valere insieme. |
| **Cosa fa la Bibbia** | Dichiara la lunghezza in testa al documento, con la ragione: il residuo è **ampiezza**, non ridondanza. Non taglia una frase-ponte, un'etichetta, un PMID, una bandiera rossa o uno slot di chiusura per rientrare in un numero. |
| **Se ratificata** | O il tetto diventa **condizionato all'ampiezza dichiarata** (numero di meccanismi, di modelli con prove, di leve e di strumenti attivi), oppure la catena acquisisce un cancello di ampiezza **prima** del 1º livello, che fissi quanti meccanismi e quante leve la Bibbia sviluppa: sommare undici lenti che aggiungono e poi chiedere all'editor di togliere ~26% del corpo senza toccare niente di quello che hanno aggiunto è una richiesta che non si può soddisfare. |


---

### D-020 · La restrizione «il principio del Centro di Percezione vale per l'indagine» non discrimina, e va sostituita dalla rimozione dichiarata

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Lombalgia (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione muscolo-scheletrica in cui l'intervento con la migliore evidenza si applica sulla regione sintomatica (lombalgia, cervicalgia, tendinopatie, spalla) |
| **Elemento del metodo** | La correzione proposta in **D-014**: restringere *"NON trattare quasi mai il CP"* all'**indagine** e non alla scelta del bersaglio. |
| **Perché è insufficiente** | La formulazione attenuata è stata rilevata come **passaggio non semplificabile su tre condizioni su tre** (reflusso v6/v7, vertigini v6/v7, cervicalgia v6/v7 — vedi `registro-lingua.md`, «Passaggi che restano oscuri»). Scritta in italiano piano, la regola si annulla da sola: la ricerca va a monte, la mano resta dove fa male, e non resta nessun criterio che discrimini un comportamento da un altro. Una regola che, formulata in chiaro, non separa più due condotte non è una regola conservativa: è una regola che occupa spazio e non decide. |
| **Cosa fa la Bibbia** | Non attenua il principio: lo **toglie** da questa condizione, con il motivo scritto a lettera in «Come ragiono davanti a questo paziente» — *"la regola «non trattare il punto in cui il paziente sente» non si applica alla scelta del bersaglio, e non viene attenuata: viene tolta. Il motivo è un fatto — gli interventi con le prove migliori si applicano proprio sulla regione lombare e sul movimento che fa male."* Quello che resta, intatto e con potere di discriminare, è la regola di verifica: **il marker con cui rivaluti appartiene a un piano che non hai trattato.** |
| **Se ratificata** | In `motore-clinico.md` §2 (6° Sistema Fasciale), separare due regole distinte invece di una attenuata: (a) regola di **indagine** — *"cerca a monte prima di concludere che la causa sia dove fa male"*; (b) regola di **verifica** — *"il marker della prova appartiene a un piano non trattato"*. Il divieto di trattare la zona sintomatica sparisce come regola, e con lui la formulazione «in forma attenuata» che tre revisioni di lingua su tre hanno segnalato come non scrivibile in chiaro. |

---

### D-021 · La conversione gel→sol dell'acido ialuronico presentata come effetto del gesto manuale

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Lombalgia (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui si invoca la densificazione fasciale come bersaglio del trattamento manuale |
| **Elemento del metodo** | `motore-clinico.md`, §2, 6° Sistema Fasciale: *"Biochimica (sol/gel): stress, freddo, trauma, pH acido rendono l'acido ialuronico «appiccicoso»; la manipolazione (attrito → calore) lo riporta fluido."* Scritto come fatto, senza etichetta. |
| **Perché è sbagliato** | È un modello, non una misura. Nessuno ha misurato viscosità o stato dell'acido ialuronico nella fascia umana prima e dopo un trattamento manuale. Quello che **è** stato misurato sulla fascia toracolombare umana è altro: lo scorrimento fra gli strati è ridotto di circa un quinto nelle persone con lombalgia cronica rispetto a chi non ha dolore (Langevin, *BMC Musculoskelet Disord* 2011, [PMID 21929806](https://pubmed.ncbi.nlm.nih.gov/21929806/)) — un dato trasversale, che gli autori attribuiscono a schemi di movimento alterati **o** a una alterazione intrinseca del connettivo, senza stabilire la direzione né misurare l'effetto di un trattamento. E la sola cosa nota sull'innervazione utile a spiegare il dolore riguarda la distribuzione delle terminazioni nocicettive, confinate allo strato esterno e al sottocute (Tesarz, *Neuroscience* 2011, [PMID 21839150](https://pubmed.ncbi.nlm.nih.gov/21839150/)). |
| **Cosa fa la Bibbia** | Non usa la catena sol/gel. Scrive la fascia toracolombare come **tessuto innervato e come piano di scorrimento misurato**, con il dato di Langevin dichiarato come differenza fra gruppi e non come bersaglio che la mano ripristina. La leva manuale sul terzo meccanismo porta PROBABILE sull'effetto clinico e nessuna affermazione sul substrato biochimico. |
| **Se ratificata** | Riscrivere la riga «Biochimica (sol/gel)» di `motore-clinico.md` come **modello esplicativo con etichetta IPOTESI**, e sostituire il claim di effetto (*"la manipolazione lo riporta fluido"*) con la formulazione misurata: *"nelle persone con lombalgia cronica lo scorrimento fra gli strati della fascia toracolombare è ridotto; che il gesto manuale lo ripristini non è stato misurato."* |

---

### D-020 · La gerarchia del Motore Clinico mette in fondo il piano su cui, in questa condizione, poggia l'evidenza migliore

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Artrosi (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui l'intervento con la migliore evidenza agisce sul muscolo peri-articolare o sul carico, cioè sul piano esecutore (artrosi, tendinopatie, gonalgia, coxalgia, spalla, lombalgia da decondizionamento) |
| **Elemento del metodo** | `motore-clinico.md`, §1 e §3: *"il sistema dominante è, di norma, il più alto nella piramide che risulti disfunzionale"*, e §2, 6° Sistema Fasciale come ultimo livello di comando. Il muscolo esecutore non compare come piano autonomo e finisce, per costruzione, in fondo. |
| **Perché è incompleto** | Su questa condizione la leva con le prove migliori al mondo appartiene esattamente al piano che la gerarchia colloca in fondo. La debolezza degli estensori del ginocchio **precede** l'artrosi sintomatica su 46.819 persone in 11 studi longitudinali ([Øiestad, *Br J Sports Med* 2022, PMID 34916210](https://pubmed.ncbi.nlm.nih.gov/34916210/)); l'esercizio a terra riduce il dolore di 12 punti su 100 con prove di alta qualità su 54 studi ([Fransen, *Cochrane* 2015, PMID 25569281](https://pubmed.ncbi.nlm.nih.gov/25569281/)); e l'effetto **non dipende dalla gravità radiografica né dal dolore di partenza**, mentre dipende dalla supervisione e dalla specificità del bersaglio muscolare ([Juhl, *Arthritis Rheumatol* 2014, PMID 24574223](https://pubmed.ncbi.nlm.nih.gov/24574223/)). Applicata come regola di **priorità terapeutica** invece che di **ordine d'indagine**, la piramide porta a spendere il ciclo sui piani a monte e a lasciare fuori l'unico intervento con una revisione sistematica di alta qualità alle spalle. |
| **Cosa fa la Bibbia** | Separa i due usi della gerarchia e lo dichiara a lettera in «Come ragiono davanti a questo paziente»: *"la gerarchia ordina l'indagine, non la forza delle leve. Su questa condizione la leva con le prove migliori appartiene al piano esecutore, che nella gerarchia sta in fondo: il muscolo."* Mantiene la road map ordinata con **un solo metro** — quanto un piano sequestra la capacità di adattamento — e tiene le bandiere rosse **fuori** dalla lista, come cancello che la precede, per non mescolare due metri d'ordine nella stessa sequenza numerata. |
| **Se ratificata** | Aggiungere a `motore-clinico.md` §3 la distinzione fra **ordine d'indagine** (la piramide) e **ordine d'intervento** (la forza dell'evidenza disponibile su quella condizione), con la regola che quando le due divergono la Bibbia lo dichiara nel Capitolo 8 invece di lasciare che il lettore le confonda. |

---

### D-020 · La tensione cervicale trattata come innesco dell'attacco, quando in due casi su tre è parte dell'attacco

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Emicrania (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui un reperto muscolo-scheletrico co-occorrente viene assunto come causa del sintomo (emicrania, cefalea tensiva, acufene, vertigini, dolore facciale) |
| **Elemento del metodo** | La formulazione di partenza del problema (`problemi.json`, campo `meccanismo_causa`): *"gli attacchi partono più facilmente quando il sistema è già sotto pressione: collo rigido, mandibola serrata… sono la **legna sul fuoco**"*, e per estensione la logica del Motore Clinico che legge un ipertono periferico come ingresso che alimenta il sintomo. |
| **Perché è sbagliato** | Sull'emicrania la direzione prevalente è l'opposta. Su 391 emicranici, 166 riferivano dolore al collo durante l'attacco: in 53 (32%) il dolore al collo funzionava da innesco, in 113 (68%) era **parte** della sintomatologia dell'attacco ([Pradhan, *Neurol India* 2018, PMID 29547158](https://pubmed.ncbi.nlm.nih.gov/29547158/)). Con diario elettronico su 97 pazienti, il collo rigido compare nel **50%** degli attacchi preceduti da sintomi premonitori, terzo per frequenza dopo stanchezza e difficoltà di concentrazione: è quindi un fenomeno della fase premonitoria, cioè già l'attacco ([Giffin, *Neurology* 2003, PMID 12654956](https://pubmed.ncbi.nlm.nih.gov/12654956/)). E la fisiologia conferma la direzione testa→collo: la stimolazione nocicettiva della dura madre sensibilizza i neuroni di secondo ordine e **aumenta** le risposte all'ingresso cervicale, allargando il campo recettivo nel 71% dei neuroni ([Bartsch & Goadsby, *Brain* 2003, PMID 12821523](https://pubmed.ncbi.nlm.nih.gov/12821523/)). Scrivere la tensione cervicale come "legna sul fuoco" senza qualificarla porta a trattare un sintomo credendo di trattare una causa, e a promettere al paziente una riduzione degli attacchi che quel reperto non regge. È lo stesso errore che D-009 ha già corretto sul reflusso e il collo, in un'altra condizione. |
| **Cosa fa la Bibbia** | Scrive la convergenza come **bidirezionale** e dichiara la proporzione: *"il collo partecipa quasi sempre, ma in due casi su tre partecipa come sintomo e non come causa, e distinguere i due casi è il lavoro"*. Usa la palpazione sostenuta dei segmenti cervicali alti come **test di stratificazione** — 11% senza dolore, 42% dolore locale, 47% dolore riferito in testa ([Luedtke & May, *J Headache Pain* 2017, PMID 28952052](https://pubmed.ncbi.nlm.nih.gov/28952052/)) — invece che come conferma di una catena causale. Nel Capitolo 9 il confine di atto vieta esplicitamente la frase *"il suo mal di testa viene dalla cervicale"*, dichiarandola sia diagnosi sia affermazione falsa in due casi su tre. |
| **Se ratificata** | Riformulare il campo `meccanismo_causa` dell'emicrania e la logica generale del Motore Clinico sui reperti co-occorrenti: un reperto muscolo-scheletrico che accompagna un sintomo va classificato come **candidato bidirezionale** finché non è stato stratificato con un test di provocazione, e la Bibbia deve dichiararne la proporzione quando esiste un dato. Sostituire la metafora "legna sul fuoco" con una formulazione che non attribuisca la direzione prima di averla verificata. |
### D-020 · «Ogni cicatrice è una densificazione permanente e diventa il punto prioritario finché non la liberi»

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Cicatrici da cesareo (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui compare una cicatrice chirurgica in anamnesi |
| **Elemento del metodo** | `motore-clinico.md`, §2, 5° Trauma: *"**Cicatrici = tiranti invisibili:** ogni cicatrice è una densificazione permanente. «Tiri un filo della maglia sul fondo (addome), la scollatura (collo) si deforma.» Una cicatrice diventa il punto prioritario finché non la liberi."* |
| **Perché è sbagliato** | Tre affermazioni presentate come fatti, e nessuna delle tre regge. (1) **«Densificazione permanente»**: la differenza fra cicatrice da cesareo e pelle non cicatriziale della stessa donna è reale ma parziale e specifica — tono, rigidità, scorrimento viscoso e tempo di rilassamento meccanico differiscono, l'**elasticità no** (Gilbert, *Skin Res Technol* 2021, [PMID 33084197](https://pubmed.ncbi.nlm.nih.gov/33084197/)). Dire "densificazione" senza dire quale proprietà è cambiata rende il reperto non misurabile e non falsificabile. (2) **«Ogni cicatrice»**: la formazione di aderenze non è universale e dipende dalla propensione individuale più che dal numero di interventi — il 43% di 160 donne aveva aderenze importanti già dopo il primo cesareo, e chi le aveva alla seconda operazione aveva un rischio 1,88 volte maggiore alla terza (Herzberger, *Arch Gynecol Obstet* 2015, [PMID 25877223](https://pubmed.ncbi.nlm.nih.gov/25877223/)). (3) **«Diventa il punto prioritario finché non la liberi»**: è una regola di priorità scritta come fatto, e su questa condizione porta a un ritardo di invio. Oltre metà delle donne esaminate con dolore moderato o grave dopo incisione soprapubica trasversa aveva un **intrappolamento nervoso** (17 su 32), il cui percorso efficace è medico e chirurgico, non manuale (Loos, *Obstet Gynecol* 2008, [PMID 18378742](https://pubmed.ncbi.nlm.nih.gov/18378742/); Loos, *Ann Surg* 2008, [PMID 18948818](https://pubmed.ncbi.nlm.nih.gov/18948818/)). Infine, la trasmissione a distanza della tensione cicatriziale — «il collo si deforma» — non è mai stata misurata. |
| **Cosa fa la Bibbia** | Scrive la cicatrice come tessuto con differenze **misurate e parziali**, nominando quali proprietà cambiano e quale no. Mette il **nervo intrappolato come primo meccanismo da escludere**, non come ultimo. Etichetta l'aderenza dei piani PROBABILE e il compenso a distanza IPOTESI, dichiarando che nessuno ha misurato la relazione fra scorrimento della cicatrice e dolore lombare. E toglie la priorità dalla regola di metodo per rimetterla nel triage e nella road map, dove la decide il quadro della singola paziente. |
| **Se ratificata** | Riformulare la voce "Cicatrici" di `motore-clinico.md` §2 (5° Trauma) in tre punti: la cicatrice **può** avere proprietà meccaniche diverse dal tessuto vicino, e quali; la formazione di aderenze **non è universale** e dipende dalla propensione individuale; la cicatrice è **un bersaglio da valutare**, non un punto prioritario per definizione — e prima di trattarla va escluso l'intrappolamento nervoso quando il dolore ha un punto e un territorio. |

---


### D-020 · L'ATM e il bruxismo elencati fra gli "inquinatori recettoriali" che tengono il sistema in loop

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Bruxismo (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui il metodo elenca l'ATM o il bruxismo fra i recettori "inquinatori" (bruxismo, ATM, cefalea, acufeni, cervicalgia, problemi posturali) |
| **Elemento del metodo** | `motore-clinico.md`, §2, 1° Sistema Neurologico: *"I tre «Inquinatori» (recettori): Occhio, **ATM** (il nucleo del trigemino arriva alle prime cervicali C1-C3: **bruxismo o morso sbilanciato tengono il sistema in loop di contrazione**), Vestibolo."* Il bruxismo compare come input periferico che alimenta lo stato di allarme. |
| **Perché è sbagliato sulla condizione in cui il bruxismo è il sintomo** | Inverte la direzione della catena, e la direzione è misurata. Il bruxismo del sonno è un'attività oromotoria **secondaria** a una sequenza di riattivazione del sonno: l'aumento dell'attività simpatica comincia **8 minuti** prima dell'episodio, i microrisvegli 4 minuti prima, poi si attivano corteccia, cuore, sopraioidei e solo alla fine gli elevatori ([Huynh, *J Sleep Res* 2006, PMID 16911037](https://pubmed.ncbi.nlm.nih.gov/16911037/); [Lavigne, *Arch Oral Biol* 2007, PMID 17313939](https://pubmed.ncbi.nlm.nih.gov/17313939/)). Il masticatorio è l'**esecutore**, non la sorgente. Le sintesi cliniche collocano la regolazione del bruxismo del sonno a livello centrale e **non** nei fattori morfologici, cioè non nell'occlusione ([Yap & Chua, *J Conserv Dent* 2016, PMID 27656052](https://pubmed.ncbi.nlm.nih.gov/27656052/)); il consenso internazionale ha inoltre smesso di considerarlo un disturbo, definendolo un comportamento in un continuum ([Lobbezoo, *J Oral Rehabil* 2018, PMID 29926505](https://pubmed.ncbi.nlm.nih.gov/29926505/)). Conseguenza pratica dell'errore: chi legge "inquinatore" cerca la causa nel morso e nel muscolo, e non guarda l'unico piano su cui esistono studi controllati con effetto — quello comportamentale da sveglio e quello cervicale. Nota: la revisione Cochrane sull'aggiustamento occlusale (Koh & Robinson 2003) è stata **ritirata nel 2016** e non va citata a sostegno. |
| **Cosa fa la Bibbia** | Non usa la categoria "inquinatore" per l'ATM né per il bruxismo. Descrive il bruxismo del sonno come evento del sonno generato a monte, con il masticatorio come esecutore, e riserva la parola *ingresso* a ciò che è stato misurato come tale: l'acidificazione esofagea ([Ohmure, *J Dent Res* 2011, PMID 21248360](https://pubmed.ncbi.nlm.nih.gov/21248360/)), alcol, tabacco e caffeina ([Bertazzo-Silveira, *JADA* 2016, PMID 27522154](https://pubmed.ncbi.nlm.nih.gov/27522154/)) e alcuni antidepressivi ([Garrett & Hawley, *Neurol Clin Pract* 2018, PMID 29708207](https://pubmed.ncbi.nlm.nih.gov/29708207/)). L'occlusione è dichiarata non causa e non bersaglio. |
| **Se ratificata** | In `motore-clinico.md` §2 limitare la voce "ATM" fra gli inquinatori alle condizioni in cui il sintomo **non** è mandibolare, togliere "morso sbilanciato" dalla formulazione, e aggiungere che quando il sintomo presentato è il bruxismo il generatore è centrale e il masticatorio è l'esecutore. |

---

### D-020 · «Resistenza al trattamento entro 24 ore» come segno di dominanza viscerale

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Ernia del disco lombare (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione con una componente radicolare o neuropatica periferica (ernia discale, radicolopatia cervicale, sindromi da intrappolamento) |
| **Elemento del metodo** | `motore-clinico.md`, §2, 4° Sistema Viscerale: *"I tre segnali chiave di dominanza viscerale: … (3) **resistenza al trattamento** (hai trattato la struttura in modo perfetto, ma dopo 24 ore la contrattura è tornata **identica**)."* |
| **Perché è sbagliato** | Nella radicolopatia da ernia il ritorno della contrattura di difesa entro 24-48 ore è il **comportamento atteso di una radice chimicamente irritata**, non un segno viscerale. L'applicazione di nucleo polposo autologo alle radici della cauda equina, **senza nessuna compressione meccanica**, riduce la velocità di conduzione per giorni e produce danno istologico delle fibre (Olmarker, Rydevik e Nordborg, *Spine* 1993, [PMID 8235812](https://pubmed.ncbi.nlm.nih.gov/8235812/)); l'effetto è mediato dal TNF-alfa presente nelle cellule del nucleo, e bloccarlo impedisce il calo di conduzione (Olmarker e Larsson, *Spine* 1998, [PMID 9854752](https://pubmed.ncbi.nlm.nih.gov/9854752/)). Il segnale, preso come indicatore viscerale, porta a cercare un organo dove c'è una radice infiammata — e a spostare l'indagine su un piano che non contiene il driver, mentre il tempo su questa condizione è la variabile che produce il danno permanente. |
| **Cosa fa la Bibbia** | Elenca la ricomparsa identica a 24-48 ore fra i segni del **primo meccanismo** (la chimica sulla radice), in «Cosa si rompe», con la formulazione: *"la contrattura di difesa ritorna identica entro ventiquattro-quarantotto ore da qualunque cosa tu faccia"*, e la richiama in «Perché le mani possono cambiare qualcosa» come *"non un fallimento: la firma del meccanismo"*. Non usa la resistenza a 24 ore come segnale viscerale. |
| **Se ratificata** | In `motore-clinico.md` §2, 4° Sistema Viscerale, condizionare il terzo segnale: la resistenza al trattamento vale come indicatore viscerale **solo in assenza di una componente radicolare o neuropatica periferica documentata**; in presenza di quella, il segnale appartiene alla chimica perineurale e non all'organo. |

---

### D-020 · Il «re-test immediato» senza soglia di misura non è interpretabile

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Sciatalgia (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui la verifica poggia su un segno misurato in gradi, centimetri o millimetri di pressione |
| **Elemento del metodo** | `motore-clinico.md`, §2, 6° Sistema Fasciale: *"**Re-test immediato:** liberato il CC, il CP migliora *istantaneamente*. Se non migliora, hai sbagliato CC o piano di movimento."* |
| **Perché è sbagliato** | La regola è formulata come dicotomia — migliora / non migliora — su un segno che ha un errore di misura noto e grande. Sul test di elevazione della gamba tesa, la differenza minima davvero rilevabile è fra **13 e 20 gradi**, e gli autori concludono che l'errore di misura *"probabilmente impedisce di usare l'escursione del SLR per le decisioni cliniche"* (Nee, Coppieters e Boyd, *Musculoskelet Sci Pract* 2022, [PMID 35245880](https://pubmed.ncbi.nlm.nih.gov/35245880/)). Applicata alla lettera, la regola trasforma un'oscillazione dello strumento in una conferma del ragionamento: è il meccanismo con cui la prova della chiave di volta smette di essere una verifica e diventa un auto-inganno, cioè esattamente ciò che `lessico-del-metodo.md` chiede di evitare con la quarta condizione del marker. Il problema non è il re-test, che resta valido: è la sua formulazione senza soglia. |
| **Cosa fa la Bibbia** | Riformula il re-test come **confronto contro una soglia dichiarata prima**, e la scrive per ogni marker della condizione. Su questa Bibbia la soglia del SLR è fissata a **≥ 20°** — sopra l'estremo superiore dell'errore riportato — e le altre tre soglie sono dichiarate come convenzioni di misura del metodo, scelte sopra l'errore dello strumento e non desunte dalla letteratura. Formulazione usata in «Come ragiono davanti a questo paziente»: *"un guadagno di dieci gradi non è un risultato, è rumore dello strumento."* Inoltre il marker misurato è il **punto di comparsa del sintomo distale**, non l'escursione massima, perché la seconda dipende anche dalla catena posteriore. |
| **Se ratificata** | Riscrivere la voce del re-test in `motore-clinico.md` §2 come *"re-test immediato contro una soglia dichiarata prima di trattare: senza soglia, un re-test non distingue un effetto da un errore di misura"*, e aggiungere la stessa condizione alla descrizione della prova della chiave di volta in `architettura-bibbia.md`. |

### D-022 · Il reperto palpatorio come fondamento del mandato clinico e come marker

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Lombalgia (sintesi v3, 2º livello — `evidenza-estesa`) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui il mandato clinico e la verifica poggiano su un reperto trovato con le mani |
| **Elemento del metodo** | `architettura-bibbia.md`, cancello d'ingresso, e `motore-clinico.md`, regola sui marker: il mandato nasce da *"un reperto disfunzionale che hai trovato e documentato, e da un marker che si muove quando lo tratti"*, **senza distinguere fra tipi di reperto**. |
| **Perché è incompleto** | L'evidenza contraddice quell'indistinzione. Su 49 studi, fra quelli che usano il kappa hanno affidabilità accettabile fra esaminatori il 64% dei test di provocazione del dolore, il 58% dei test di movimento, il 33% dei punti di repere e lo **0%** dei test palpatori sui tessuti molli paraspinali; l'escursione regionale è più affidabile della segmentale, e disciplina, esperienza, consenso sulla procedura e training appena precedente **non migliorano** l'affidabilità (Seffinger, *Spine* 2004, [PMID 15454722](https://pubmed.ncbi.nlm.nih.gov/15454722/)). I test attivi di controllo del movimento reggono, ma non tutti: kappa 0,24-0,71, sei su dieci sopra 0,6 (Luomajoki, *BMC Musculoskelet Disord* 2007, [PMID 17850669](https://pubmed.ncbi.nlm.nih.gov/17850669/)). E scegliere il segmento "giusto" non cambia l'esito: certezza moderata di nessuna differenza fra manipolazione mirata e non mirata su 931 pazienti (Sørensen, *J Orthop Sports Phys Ther* 2023, [PMID 37506306](https://pubmed.ncbi.nlm.nih.gov/37506306/); corroborato da Nim, *Sci Rep* 2021, [PMID 34862434](https://pubmed.ncbi.nlm.nih.gov/34862434/)). Un mandato professionale che poggia su un reperto di cui non si dichiara la riproducibilità è una regola non verificabile. |
| **Cosa fa la Bibbia** | Dichiara il criterio invece di applicarlo in silenzio. Reggono come marker e come reperto documentato: provocazione del dolore con un carico definito, escursione **regionale** misurata, test di controllo del movimento, tempo su un compito funzionale, soglia algometrica. La palpazione dei tessuti molli e la valutazione della mobilità **segmentale** restano parte dell'esame e dell'orientamento, ma **non fondano il mandato e non funzionano da marker**. La stessa specificazione entra nella prima condizione del GIALLO. E il reperto viene dichiarato per quello che è: dice che hai qualcosa da trattare e dove il paziente tollera il contatto, non che quel segmento è la causa. |
| **Se ratificata** | Integrare la `regola sui marker` di `motore-clinico.md` con il criterio di **riproducibilità misurata**, e la descrizione del cancello d'ingresso in `architettura-bibbia.md` con la distinzione fra reperto che fonda il mandato e reperto che orienta soltanto. |

---

### D-023 · Il lavoro intra-orale sui masticatori come tecnica ammissibile

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Bruxismo (sintesi v3, 2º livello — `fedelta-bibbia` ed `evidenza-estesa`) |
| **Ambito** | Trasversale — riguarda ogni condizione del distretto orofacciale (bruxismo, dolori mandibolari, cefalea di origine masticatoria) |
| **Elemento del metodo** | La tradizione osteopatica sul distretto temporo-mandibolare, che prevede l'accesso intra-orale ai muscoli masticatori — in particolare allo pterigoideo laterale — come parte dell'arsenale. |
| **Perché è sbagliato** | Due ragioni indipendenti, e la prima da sola basta. **Normativa:** il DPR 131/2021, art. 2 co. 2 lett. a) definisce l'atto osteopatico come costituito da tecniche *esclusivamente manuali, non invasive ed **esterne***. Una manovra dentro la cavità orale non è esterna, e non esiste un consenso informato che renda ammissibile un atto fuori dal profilo professionale. **Tecnica:** il bersaglio non è raggiungibile. Lo pterigoideo laterale è praticamente irraggiungibile alla palpazione intra-orale, quello che si palpa è altro tessuto, la regione è dolente anche nei soggetti sani — quindi un reperto positivo è un falso positivo per costruzione — e gli autori concludono che la procedura va abbandonata (Türp & Minagi, *J Dent* 2001, [PMID 11809325](https://pubmed.ncbi.nlm.nih.gov/11809325/)). |
| **Cosa fa la Bibbia** | Dichiara il lavoro intra-orale **fuori perimetro in modo assoluto**, non rimandato a una valutazione caso per caso, e ne scrive entrambe le ragioni in «Dove finisce il nostro campo». Al paziente che lo chiede la risposta è che è fuori dal profilo professionale, non che è pericoloso. |
| **Se ratificata** | Rimuovere l'accesso intra-orale dall'arsenale dei documenti di metodo per il distretto orofacciale, e citare il vincolo normativo accanto all'esclusione. |

---

### D-024 · Il triangolo anteriore del collo e il pavimento della bocca come bersaglio

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Bruxismo (sintesi v3, 2º livello) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui i sopraioidei, gli scaleni anteriori o la regione sotto-mandibolare compaiono fra gli attori del meccanismo |
| **Elemento del metodo** | Il principio per cui una struttura che partecipa al meccanismo è, per ciò stesso, un candidato al trattamento. |
| **Perché è incompleto** | Il principio non distingue fra *attore* e *bersaglio*. Sul bruxismo i sopraioidei sono attori centrali — si attivano prima degli elevatori in ogni episodio notturno — ma la regione che li contiene contiene anche la guaina carotidea, e gli eventi avversi gravi dopo procedure fisiche sul collo sono vascolari nel 58% dei casi, alcuni dopo mobilizzazioni gentili e non solo dopo manipolazione ad alta velocità (Leung, *J Bodyw Mov Ther* 2025, [PMID 39663097](https://pubmed.ncbi.nlm.nih.gov/39663097/)). Non esiste nessuna misura di beneficio su quel distretto in questa condizione: il bilancio è rischio noto contro guadagno non misurato. |
| **Cosa fa la Bibbia** | Dichiara il triangolo anteriore del collo e il pavimento della bocca **non bersaglio** su questa condizione, pur tenendo i sopraioidei fra gli attori del meccanismo, e scrive la distinzione a lettera in «Le strutture in gioco» e in «Perché le mani possono cambiare qualcosa». Prevale la sicurezza sul completamento dell'arsenale. |
| **Se ratificata** | Aggiungere ai documenti di metodo la distinzione fra **attore del meccanismo** e **bersaglio del gesto**, con il criterio esplicito: una struttura diventa bersaglio quando esiste una misura di beneficio, non quando esiste un razionale. |

---

### D-025 · Il Capitolo 12 ammette solo strumenti provati sulla condizione stessa

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Bruxismo (sintesi v3, 2º livello) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui la migliore evidenza sullo strumento attivo viene da una popolazione vicina e non dalla condizione stessa |
| **Elemento del metodo** | `architettura-bibbia.md`, Capitolo 12: il capitolo esiste *"solo se uno strumento attivo regge DIMOSTRATO o PROBABILE forte"* — implicitamente, su questa condizione. |
| **Perché è incompleto** | Sul bruxismo l'informazione con autogestione ha uno studio randomizzato su dolore muscolare masticatorio (Michelotti, *JADA* 2012, [PMID 22207667](https://pubmed.ncbi.nlm.nih.gov/22207667/)) e una raccomandazione forte su dolore cronico temporo-mandibolare (Busse, *BMJ* 2023, [PMID 38101929](https://pubmed.ncbi.nlm.nih.gov/38101929/)), non sul bruxismo. La lettura stretta la escluderebbe dal capitolo, e terrebbe fuori dalla Bibbia una delle leve con le prove migliori dell'intero documento — che è esattamente l'errore che il Capitolo 12 condizionale è nato per correggere. |
| **Cosa fa la Bibbia** | Ammette lo strumento con l'**estrapolazione dichiarata** e l'etichetta tenuta a PROBABILE, e scrive nel box di solidità quale popolazione ha prodotto il dato e perché l'etichetta non sale. |
| **Se ratificata** | Aggiungere al Capitolo 12 la condizione: uno strumento attivo sostenuto da una popolazione vicina entra, purché il salto di popolazione sia dichiarato nel punto d'uso e l'etichetta non superi PROBABILE. |

---

### D-026 · Le leve di stile di vita appartengono per definizione al modello Metabolico-Energetico

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Bruxismo (sintesi v3, 2º livello — `fedelta-bibbia`) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui alcol, tabacco, caffeina, farmaci o alimentazione compaiono fra i fattori |
| **Elemento del metodo** | `cinque-modelli-osteopatici.md`: la checklist assegna al **Metabolico-Energetico** le leve di stile di vita, con lo scope *"si segnalano e si rinvia, non si prescrive"*. |
| **Perché è incompleto** | L'assegnazione è fatta per categoria di leva, non per meccanismo. Sul bruxismo alcol, tabacco, caffeina e farmaci non agiscono sul metabolismo del muscolo: agiscono sulla **soglia del microrisveglio**, cioè sul generatore neurologico (Bertazzo-Silveira, *JADA* 2016, [PMID 27522154](https://pubmed.ncbi.nlm.nih.gov/27522154/); de Baat, *J Oral Rehabil* 2021, [PMID 32716523](https://pubmed.ncbi.nlm.nih.gov/32716523/)). Lasciarle nel Metabolico-Energetico separa la leva dal meccanismo su cui agisce, ed è la stessa classe di errore che la checklist esiste per impedire. |
| **Cosa fa la Bibbia** | Colloca quelle leve nel modello **Neurologico**, come *modificatori esogeni del generatore*, con il motivo scritto nel punto d'uso, e **conserva per intero lo scope** prescritto dalla checklist: *"nessuno di loro si lavora con le mani: si valutano, si nominano, si rinviano"*. |
| **Se ratificata** | Riscrivere la voce in `cinque-modelli-osteopatici.md` come: *le leve di stile di vita appartengono al modello che governa il meccanismo su cui agiscono, non per definizione al Metabolico-Energetico; lo scope di segnalazione-e-rinvio le segue.* |

---

### D-027 · Il box `Definizione` alla prima comparsa **in ogni capitolo** non è sostenibile insieme al tetto di lunghezza

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Emicrania (Bibbia v3, rilevata dall'audit di fedeltà di 2º livello sulla v2) |
| **Ambito** | Trasversale — riguarda ogni Bibbia che usi i sette termini canonici del metodo |
| **Elemento del metodo** | `lessico-del-metodo.md`, «Come si usano», punto 1: *"Box `> **Definizione.**` alla prima comparsa in ogni capitolo in cui il termine appare. Non solo alla prima comparsa nel documento."* |
| **Perché è incompleto** | Sui sette termini canonici la regola produce, su una Bibbia ampia, fra dodici e venti box identici — `catena` compare in sei capitoli, `marker` in cinque, `compenso` in tre. Il costo è di 400-600 parole di testo letteralmente ripetuto, su un documento che l'editor di 4º livello deve già riportare sotto un tetto che D-019 dichiara non raggiungibile. Le due regole del metodo — testo fisso ripetuto per capitolo e tetto di 8.000-13.000 parole — non possono valere insieme sulle condizioni ampie. Il problema **non** è il testo canonico: quello resta intoccabile e va riportato per intero (è la parte che questa Bibbia aveva abbreviato a Glossario, ed è stata ripristinata). |
| **Cosa fa la Bibbia** | Riporta il **testo canonico integrale** delle sette voci in Appendice A, senza riformulazioni. Mette il box `Definizione` alla prima comparsa **operativa** del termine — quella in cui il termine regge una regola di condotta — e non in ogni capitolo: `catena` e `disfunzione somatica` nei capitoli in cui il concetto entra nel ragionamento, `sistema dominante` e `marker` nel capitolo del Motore Clinico. Dichiara la scelta nel testo (*"le altre parole del metodo stanno nel Glossario, e ciascuna compare per esteso una volta sola"*). |
| **Se ratificata** | Riscrivere il punto 1 di `lessico-del-metodo.md` come *"box `Definizione` alla prima comparsa **operativa** del termine — quella in cui regge una regola di condotta — più la voce integrale a Glossario; la ripetizione per capitolo resta obbligatoria solo per i termini che cambiano il significato di una regola di sicurezza"*. |

---

### D-028 · L'eccezione alla regola del ponte è scritta per il solo Capitolo 12

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Sciatalgia (sintesi v3, 2º livello — `fedelta-bibbia`) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui una leva, e non solo uno strumento attivo, poggia su un intervento a esito clinico testato su una popolazione contigua |
| **Elemento del metodo** | `ancore-scientifiche.md`, regola del ponte: l'evidenza trasversale alza l'etichetta del *meccanismo*, mai quella della *leva*. L'unica eccezione registrata, **D-025**, è scritta per il solo Capitolo 12. |
| **Perché è incompleto** | Sulla sciatalgia l'intervento con l'esito clinico migliore disponibile (Kent, *Lancet* 2023, [PMID 37146623](https://pubmed.ncbi.nlm.nih.gov/37146623/), 492 adulti con lombalgia cronica disabilitante) sostiene una **leva** dei Capitoli 7 e 11 — spiegazione ed esposizione graduata — prima ancora che uno strumento attivo del Capitolo 12. La lettura stretta di D-025 obbligherebbe a scrivere IPOTESI sulla stessa leva che nel Capitolo 12 regge PROBABILE, cioè due etichette diverse per lo stesso intervento a due pagine di distanza. |
| **Cosa fa la Bibbia** | Estende l'eccezione dichiarata a **qualunque leva** sostenuta da un intervento a esito clinico su popolazione contigua, con tre vincoli scritti nel punto d'uso: l'etichetta **scende di un grado** e non supera PROBABILE; la **popolazione si scrive accanto** ogni volta; **un indice fisiologico misurato in volontari sani non regge mai una leva** e resta meccanismo. La formulazione è nel capitolo «La lettura osteopatica». |
| **Se ratificata** | Riscrivere D-025 come regola generale: *l'eccezione alla regola del ponte vale per qualunque leva sostenuta da un intervento a esito clinico su popolazione contigua, non solo per gli strumenti attivi del Capitolo 12; l'etichetta scende di un grado, la popolazione si scrive accanto in ogni punto d'uso, e un indice fisiologico su volontari sani non regge mai una leva.* |

---

> **Nota di servizio al direttore — collisione di numerazione da sanare.** Il registro contiene **sette** voci distinte numerate `D-020` (cervicalgia/lombalgia, artrosi, emicrania, cicatrici, bruxismo, ernia, sciatalgia). Finché la collisione resta, ogni rimando a `D-020` è interpretabile solo con il registro aperto accanto, e le Bibbie devono citare la voce per titolo oltre che per numero. La rinumerazione è una decisione a monte: non la applico qui.

---

### D-029 · La misura con cui la letteratura documenta l'effetto immediato non soddisfa le condizioni del marker

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-19 |
| **Condizione di emersione** | Cervicobrachialgia (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui l'outcome misurato negli studi coincide con la struttura trattata (cervicobrachialgia, sciatalgia, tendinopatie, spalla, ATM) |
| **Elemento del metodo** | `lessico-del-metodo.md`, voce `marker`, condizione 3: *"Appartiene a un piano che non hai trattato. Se rimisuri quello su cui hai appena lavorato, stai misurando l'effetto immediato del tuo gesto, non il cambiamento del sistema."* |
| **Perché è incompleto** | Presa alla lettera, la condizione 3 esclude proprio la misura su cui poggia l'unico effetto immediato documentato su questa condizione. Nell'RCT che ha confrontato una mobilizzazione cervicale con un comparatore attivo, gli esiti misurati erano l'escursione al test neurodinamico dell'arto superiore, l'area del sintomo e il dolore — cioè esattamente il piano trattato (Coppieters, *JOSPT* 2003, [PMID 12918862](https://pubmed.ncbi.nlm.nih.gov/12918862/): estensione del gomito da 137,3° a 156,7°, area del sintomo −43,4%, nessun cambiamento con ultrasuoni). Applicare la regola senza distinguere porta a uno di due errori opposti: buttare via la misura che la letteratura valida, oppure usarla come prova della chiave di volta e prendere per conferma sistemica l'effetto meccanico immediato del gesto appena fatto. |
| **Cosa fa la Bibbia** | Separa due ruoli invece di sovrapporli. La misura sul piano trattato — punto di comparsa del sintomo distale, area e direzione del sintomo, escursione cervicale — è dichiarata **misura di effetto immediato del gesto**, con la soglia presa sotto il cambiamento riportato in letteratura e sopra l'errore dello strumento. La **prova della chiave di volta** poggia su una misura che appartiene a un piano non trattato: la **sensibilità al freddo su sito remoto**, confrontata col lato sano (Tampin, *Pain* 2012, [PMID 22980746](https://pubmed.ncbi.nlm.nih.gov/22980746/)). **Aggiornamento v2/v3:** la forza **non** è la chiave di volta ed è stata riclassificata come **misura di confine** — dipende da C8-T1 mentre le radici più colpite sono C7 e C6, e *"il numero che decide se invii non può essere lo stesso che ti dà ragione"*. La formulazione della v1, che assegnava alla forza di presa il ruolo di chiave di volta, è superata. |
| **Se ratificata** | Integrare la voce `marker` di `lessico-del-metodo.md` distinguendo due funzioni: la **misura di effetto immediato**, che può appartenere al piano trattato purché la soglia sia dichiarata, e il **marker della prova della chiave di volta**, per il quale la condizione 3 resta vincolante. Ogni Bibbia nomina almeno uno di ciascun tipo. |

---

### D-030 · «Ogni meccanismo porta **una** etichetta» produce un claim gonfiato quando i componenti hanno forza diversa

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-20 |
| **Condizione di emersione** | Cervicobrachialgia (sintesi v3, 2º livello — `fedelta-bibbia`) |
| **Ambito** | Trasversale — riguarda ogni meccanismo o strumento composto da più anelli con basi di prova diverse |
| **Elemento del metodo** | `architettura-bibbia.md` e SKILL: *«Ogni meccanismo, ogni modello e ogni leva ne porta una»* etichetta di solidità. |
| **Perché è incompleto** | La regola presuppone che un meccanismo sia un'affermazione sola. Non lo è quasi mai. Il primo meccanismo di questa condizione ne contiene tre con basi diverse: la **geometria** del forame è misurata direttamente nell'uomo (Yoo, *Spine* 1992, [PMID 1440000](https://pubmed.ncbi.nlm.nih.gov/1440000/)) e regge DIMOSTRATO; l'**anello vascolare** poggia su radici lombari animali (Olmarker 1989; Kobayashi 2008) e regge PROBABILE; il **passo clinico** — che sia questo a far male a questo paziente — poggia sullo Spurling a certezza da bassa a molto bassa e regge PROBABILE. Un'etichetta unica sui tre pezzi è per forza sbagliata: se prende la più alta gonfia il claim, se prende la più bassa butta via una misura diretta. Lo stesso vale per il Capitolo 12, dove scorrimento, educazione, gestione posizionale e rinforzo hanno quattro basi diverse e il rinforzo ha contro un randomizzato negativo. |
| **Cosa fa la Bibbia** | Quando i componenti di un'affermazione hanno forza diversa, **spezza l'etichetta** e ne assegna una per componente, dentro lo stesso box `Quanto è solido`, con l'apertura fissa *«l'etichetta si spezza, perché i pezzi non hanno la stessa forza»*. Il numero di etichette del documento non cambia il vincolo: nessuna quinta etichetta, glossa fissa su ognuna. Applicata al primo e al terzo meccanismo, al modello Metabolico-Energetico e al Capitolo 12. |
| **Se ratificata** | Integrare la regola come: *ogni meccanismo, modello e leva porta almeno un'etichetta; quando l'affermazione si scompone in componenti con basi di prova diverse, l'etichetta si spezza per componente e ciascuna porta la propria glossa fissa.* |

---

### D-031 · La scheda dei cinque modelli non ha una voce che agganci il modello ai meccanismi

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-20 |
| **Condizione di emersione** | Cervicobrachialgia (sintesi v3, 2º livello — `fedelta-bibbia`) |
| **Ambito** | Trasversale — riguarda il Capitolo 7 di ogni Bibbia |
| **Elemento del metodo** | `cinque-modelli-osteopatici.md`: ogni modello porta quattro voci — *Cosa governa qui*, *Gli attori*, *I segnali che pesa in questo paziente*, *Quanto è solido* — «e nient'altro». |
| **Perché è incompleto** | Con quelle quattro voci il Capitolo 7 resta una descrizione parallela al Capitolo 5, e nessun revisore può verificare che i cinque modelli coprano i meccanismi dichiarati né che un meccanismo non resti orfano. È il controllo che rende falsificabile l'intero capitolo, e con le quattro voci non è eseguibile. |
| **Cosa fa la Bibbia** | Aggiunge una quinta voce, **«Quali meccanismi governa»**, che nomina i meccanismi del Capitolo 5 per titolo. Costa una riga per modello e rende verificabile l'aggancio: sulla cervicobrachialgia mostra che il Metabolico-Energetico non governa nessun meccanismo in proprio — *«sposta la prognosi»* — che è un'informazione clinica, non una lacuna. |
| **Se ratificata** | Portare la scheda a cinque voci in `cinque-modelli-osteopatici.md`, con «Quali meccanismi governa» in seconda posizione. |

---

### D-032 · «Un blocco dorsale stimola costantemente l'allarme» — la catena del simpatico davanti alle teste costali come leva autonomica

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-20 |
| **Condizione di emersione** | Dorsalgia (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui il segmento dorsale viene invocato come via di regolazione del sistema nervoso autonomo (dorsalgia, reflusso, ansia, cefalea, sindromi funzionali) |
| **Elemento del metodo** | `motore-clinico.md`, §2, 1° Sistema Neurologico: *"**Catena del simpatico:** corre davanti alle teste delle coste. Un blocco dorsale stimola costantemente l'allarme → iperalgesia."* Scritto come fatto, senza etichetta, e usato per giustificare il lavoro dorsale come leva sull'attivazione. |
| **Perché è sbagliato** | Il contatto anatomico è reale e frequentissimo — osteofiti che comprimono le strutture simpatiche toraciche in **655 cadaveri su 1.000**, con picco a T8-T10 (Nathan, *Spine* 1987, [PMID 3660077](https://pubmed.ncbi.nlm.nih.gov/3660077/)) — ma è una topografia, non una misura di effetto. Dove l'effetto è stato misurato, non c'è: la revisione sistematica con meta-analisi dedicata alla mobilizzazione e alla manipolazione **dorsale** — 20 studi, 863 partecipanti, sintomatici e asintomatici — non trova nessun effetto sui marcatori del sistema nervoso autonomo (rapporto LF/HF, conduttanza cutanea, RMSSD), e conclude che **la direzione dei cambiamenti è ambigua** (Hansen, *J Man Manip Ther* 2025, [PMID 40232939](https://pubmed.ncbi.nlm.nih.gov/40232939/)). È il corrispettivo dorsale di quanto D-004 ha già stabilito sul tocco in generale e sulla cervicale: qui però la misura esiste, è specifica del distretto, ed è negativa. |
| **Cosa fa la Bibbia** | Tiene la relazione anatomica in «Le strutture in gioco» con l'etichetta spezzata — **DIMOSTRATO** il contatto, **IPOTESI** la rilevanza clinica — e scrive nel modello Neurologico e in «Perché le mani possono cambiare qualcosa» che l'effetto sui marcatori autonomici, dove è stato cercato su questo distretto, non è stato trovato. Nella lista «cosa non possiamo dire» compare a lettera: *"che il trattamento manuale dorsale regoli il sistema nervoso autonomo"*. La leva sull'attivazione resta dichiarata e usata, ma con etichetta IPOTESI e senza attribuirle il meccanismo simpatico. |
| **Se ratificata** | Riscrivere la voce «Catena del simpatico» di `motore-clinico.md` §2 come relazione **anatomica** con etichetta IPOTESI sull'effetto, e togliere la formulazione causale *"un blocco dorsale stimola costantemente l'allarme"*, sostituendola con: *"le strutture simpatiche toraciche sono a contatto con le teste costali; che il lavoro manuale dorsale ne modifichi l'attività non è stato trovato dove è stato misurato."* |

---

### D-033 · La postura seduta scritta come causa della dorsalgia

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-20 |
| **Condizione di emersione** | Dorsalgia (Bibbia v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui una postura o una posizione di lavoro viene assunta come causa del sintomo (dorsalgia, cervicalgia, lombalgia, spalla, cefalea tensiva) |
| **Elemento del metodo** | La formulazione di partenza del problema (`problemi.json`, campo `meccanismo_causa` della dorsalgia): *"Quando stai curvo per ore, il torace si chiude, le costole si muovono meno e le vertebre dorsali restano ferme. Il corpo scarica lì la tensione."* Scritta al presente indicativo, come catena causale stabilita. |
| **Perché è sbagliato** | La relazione fra postura e dolore è misurata, e non è causale. L'umbrella review su **41 revisioni sistematiche** valutate con i criteri di Bradford Hill conclude che non c'è consenso sulla causalità fra posture spinali o esposizione fisica e dolore, con associazioni sia positive sia nulle e prove miste sulla precedenza temporale e sulla relazione dose-risposta (Swain, *J Biomech* 2020, [PMID 31451200](https://pubmed.ncbi.nlm.nih.gov/31451200/)). Sulla regione dorsale in particolare, c'è un livello **moderato** di evidenza di **nessuna differenza** di cifosi toracica fra chi ha e chi non ha dolore di spalla, mentre resta forte l'evidenza che l'escursione disponibile cambia con l'assetto (Barrett, *Man Ther* 2016, [PMID 27475532](https://pubmed.ncbi.nlm.nih.gov/27475532/)). E il dato che collega sedentarietà e mobilità dorsale — 64,8 gradi di rotazione in chi sta seduto oltre sette ore contro 75,0 in chi è attivo — viene da uno studio **trasversale** su 92 giovani adulti, i cui autori chiedono esplicitamente ricerca sulla causalità (Heneghan, *BMJ Open* 2018, [PMID 29730619](https://pubmed.ncbi.nlm.nih.gov/29730619/)). Scritta come causa, la frase produce due danni: una promessa di risultato legata alla correzione posturale, e un paziente che si colpevolizza per come sta seduto. |
| **Cosa fa la Bibbia** | Separa la misura dall'attribuzione causale e lo dichiara nel punto d'uso, con l'etichetta spezzata sul primo meccanismo: **DIMOSTRATO** che la mobilità dorsale sia ridotta in chi sta seduto molto, **IPOTESI** che la riduzione causi il dolore. In «Cosa dice la scienza» la frase *"che la postura seduta causi la dorsalgia"* compare nell'elenco di ciò che non possiamo dire, e in «Cosa si rompe» lo slot di chiusura vieta a lettera di attribuirlo al paziente. La leva resta: cambia l'oggetto — si lavora sull'escursione disponibile e sulla durata della posizione, non sulla correzione della forma. |
| **Se ratificata** | Riformulare il campo `meccanismo_causa` della dorsalgia come **associazione misurata**, non come catena causale: *"chi passa molte ore fermo ha, in media, un torace che gira di meno; che sia quello a produrre il dolore non è stabilito"*. Estendere la regola a ogni condizione in cui la postura compare fra i fattori: si scrive cosa è stato misurato, e la direzione si dichiara solo se qualcuno l'ha stabilita. |

---

### D-036 · Il tetto «da 3 a 6 sottotipi» non distingue un pattern clinico da un cancello di condotta

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-20 |
| **Condizione di emersione** | Mal di testa tensivo (sintesi v3, 2º livello — `fedelta-bibbia`) |
| **Ambito** | Trasversale — riguarda ogni condizione la cui nosografia o il cui triage impongano divisioni che non sono varianti di presentazione |
| **Elemento del metodo** | `architettura-bibbia.md`, Capitolo 6 «Non è una condizione sola»: *"da 3 a 6 sottotipi"*, senza distinzione di natura fra le voci. |
| **Perché è incompleto** | Sulla cefalea di tipo tensivo il Capitolo 6 ha **otto** voci, e tre non sono varianti di pattern: sono cancelli imposti da fuori. «Senza dolorabilità pericranica» è la divisione che l'**ICHD-3** stabilisce con le mani, ed è l'unico elemento della classificazione internazionale delle cefalee che l'osteopata determina; «tensiva in chi ha anche emicrania» cambia il **metodo di misura dell'esito**, perché i giorni al mese vanno contati separati per tipo; «con uso eccessivo di farmaci» cambia l'**uscita del triage**. Comprimere a sei significherebbe togliere un cancello per rispettare un conteggio, cioè far pagare alla sicurezza e alla misura una regola di forma. |
| **Cosa fa la Bibbia** | Tiene le otto voci, e distingue nel testo le cinque che sono pattern clinici dalle tre che sono cancelli: ciascuna delle tre porta la propria etichetta **RAGIONAMENTO** *(cornice clinica, non una prova)* e dichiara cosa cambia — il mandato, il conteggio, l'uscita del triage. La tabella di apertura del capitolo resta a quattro colonne. |
| **Se ratificata** | Riscrivere il tetto del Capitolo 6 come: *"da 3 a 6 **pattern clinici**; un sottotipo che cambia l'uscita del triage, il mandato o il metodo di misura dell'esito non conta nel tetto, si dichiara come **cancello** e porta la sua etichetta"*. |

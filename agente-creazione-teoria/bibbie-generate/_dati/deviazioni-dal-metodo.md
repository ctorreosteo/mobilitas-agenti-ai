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

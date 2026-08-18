# Registro delle deviazioni dal metodo

**A cosa serve.** Quando una procedura si discosta dall'architettura interna (i cinque modelli, il Motore Clinico, i documenti di metodo) **perché quell'elemento del metodo è fattualmente sbagliato**, la deviazione si annota qui.

Senza questo registro lo stesso conflitto si riapre **su ogni condizione**: 58 procedure che litigano 58 volte con lo stesso errore del metodo, ognuna risolvendolo a modo suo. Con il registro il conflitto si risolve **una volta**, e le procedure successive nascono già allineate.

## Come funziona

1. Un revisore (tipicamente `fisioterapista-ebp`, `neuromodulazione`, `specialista` o `modelli`) rileva che un elemento prescritto dal metodo è contraddetto dalla fisiologia o dall'evidenza.
2. Il direttore applica la correzione nella procedura e **apre una voce qui**, con stato `PROPOSTA`.
3. `fedelta-bibbia` legge questo file **prima** di fare l'audit: una deviazione già registrata non è un'infedeltà da segnalare, è una decisione presa.
4. L'autore legge questo file **prima** di scrivere una nuova procedura: non reintroduce elementi già corretti.
5. **La ratifica è umana.** Solo Carlos porta una voce da `PROPOSTA` a `RATIFICATA` (e aggiorna il documento di metodo) o a `RESPINTA` (e la procedura torna alla versione del metodo). Nessun agente può ratificare da solo: il metodo è dello studio, non del sistema.

## Stati

| Stato | Significato |
|---|---|
| `PROPOSTA` | Il sistema ha rilevato il conflitto e corretto la procedura. In attesa di giudizio umano. |
| `RATIFICATA` | Carlos ha accettato: il documento di metodo va aggiornato (o è già aggiornato). Vincolante per le procedure future. |
| `RESPINTA` | Carlos ha deciso che vince il metodo. Le procedure tornano alla formulazione originale. |

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
| **Elemento del metodo** | `architettura-procedura.md`, sezione 4, indica come modello per l'acufene la tripletta *Decompressione fisica / Reset propriocettivo / **Effetto neurobiologico del tocco***; `esempio-canonico-acufeni.md` la esplicita come "l'OMT stimola il rilascio di ossitocina e abbassa il cortisolo, agendo **direttamente sul filtro talamico** dell'acufene". |
| **Perché è sbagliato** | È un claim di meccanismo presentato come fatto. L'evidenza sulle variazioni ormonali dopo OMT è minima e di bassa qualità: la revisione sistematica dedicata (*Osteopathic Manipulation as a Method of Cortisol Modification: A Systematic Review*, Cureus 2023, [PMID 37123793](https://pubmed.ncbi.nlm.nih.gov/37123793/)) include **4 soli studi, 135 partecipanti totali** e non consente di quantificare l'effetto. Nessuno studio ha misurato ossitocina, cortisolo o attività talamica dopo trattamento manuale in pazienti con acufene, né alcun effetto "sul filtro talamico". |
| **Cosa fa la procedura** | Sostituisce il claim con **down-regulation aspecifica dell'attivazione**, dichiarata come parte del contesto terapeutico (contatto lento + respiro) e non come meccanismo neuroendocrino dimostrato. Coerente con D-002 (i sub-occipitali non sono un accesso al vago). |
| **Se ratificata** | Riformulare il terzo punto della sezione 4 in `architettura-procedura.md` (es. *"Modulazione dell'attivazione attraverso il contatto — down-regulation aspecifica, dichiarata come tale"*) e marcare esplicitamente il passaggio corrispondente in `esempio-canonico-acufeni.md` fra i claim da non imitare. |

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
| **Se ratificata** | Correggere la formulazione del meccanismo cervico-uditivo nei documenti di metodo e in `esempio-canonico-acufeni.md`: convergenza fasica, non drive tonico. |

---

### D-070 · Il "morso sbilanciato" come Inquinatore che genera il loop di contrazione

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Bruxismo (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui il metodo invoca l'occlusione come causa (bruxismo, ATM, cefalea, cervicalgia, postura) |
| **Elemento del metodo** | `fase-0-piramide-del-comando.md`, §1° Sistema Neurologico, "i tre Inquinatori": *"ATM (il nucleo del trigemino arriva alle prime cervicali C1-C3: **bruxismo o morso sbilanciato** tengono il sistema in loop di contrazione)"*. |
| **Perché è sbagliato** | La convergenza trigemino-cervicale è reale; l'attribuzione causale all'occlusione no. Manfredini, Visscher, Guarda-Nardini e Lobbezoo, *Occlusal factors are not related to self-reported bruxism*, J Orofac Pain 2012;26(3):163-167 ([PMID 22838000](https://pubmed.ncbi.nlm.nih.gov/22838000/)): confronto di decine di parametri occlusali fra 67 bruxisti e 75 non bruxisti — il modello spiega il **4,6% della varianza**, con accuratezza predittiva del 59,2%, e gli autori concludono che *"the contribution of occlusion to the differentiation between bruxers and nonbruxers is negligible"*. Il consenso internazionale 2025 (Verhoeff, Lobbezoo et al., [PMID 40312776](https://pubmed.ncbi.nlm.nih.gov/40312776/)) colloca l'eziologia nel sistema nervoso centrale. |
| **Cosa fa la procedura** | Mantiene l'**ATM/masticatorio come ingresso somatosensoriale** al complesso trigemino-cervicale (anello documentato), ma **rimuove l'occlusione dalla catena causale**: il bersaglio sono il carico muscolare e l'ingresso cervicale, non il morso. Dichiara esplicitamente che l'osteopata non fa gnatologia e non cerca precontatti. |
| **Se ratificata** | Riformulare il terzo Inquinatore in `fase-0-piramide-del-comando.md`: l'ATM entra come ingresso trigeminale, non come "morso sbilanciato" causale. |

---

### D-071 · Il bruxismo trattato come disturbo da eliminare (e la soppressione come obiettivo)

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Bruxismo (v1) |
| **Ambito** | Bruxismo, ATM, disturbi del sonno — e, come principio, ogni condizione in cui il sintomo può essere un compenso protettivo |
| **Elemento del metodo** | L'impostazione standard dell'architettura (`architettura-procedura.md`, §1-§3) tratta la condizione come **disturbo da ridurre**, e i materiali di mercato (`problemi.json`, campo *benefici_trattamento*) promettono di "fermare" il digrignamento notturno. |
| **Perché è sbagliato** | Il consenso internazionale 2025 (Verhoeff, Lobbezoo, Manfredini et al., *Updating the Bruxism Definitions*, J Oral Rehabil 2025;52(9):1335-1342, [PMID 40312776](https://pubmed.ncbi.nlm.nih.gov/40312776/)) stabilisce che *"bruxism is not the disorder, neither in otherwise healthy individuals nor in non-healthy ones"*, che è un **comportamento motorio**, e che può essere **fattore di rischio, neutro o protettivo** — l'esempio citato è il mantenimento della pervietà delle vie aeree superiori nell'apnea ostruttiva. Porsi la soppressione come obiettivo in un paziente con disturbo respiratorio del sonno non valutato è quindi un potenziale danno, non solo un claim eccessivo. |
| **Cosa fa la procedura** | Riformula l'obiettivo terapeutico su **carico e conseguenze** (dolore al risveglio, rigidità, apertura, limitazione funzionale, sonno percepito), **mai** sul numero di episodi. Introduce come **primo passo della Road Map** lo screening del sonno con regola esplicita: *davanti a un sospetto disturbo respiratorio del sonno non valutato non ti poni l'obiettivo di ridurre il bruxismo — invii*. Il sottotipo corrispondente è graduato "NON DEFINITA — prima si invia". |
| **Se ratificata** | Aggiungere all'architettura il principio generale: quando il sintomo può essere un compenso protettivo, l'obiettivo si riformula sulle conseguenze e lo screening della funzione protetta precede il trattamento. |

---

### D-040 · La cicatrice come "densificazione permanente da liberare" e la profondità come leva

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Cicatrici da taglio cesareo (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui si lavora su una cicatrice chirurgica o su aderenze (cesareo, mastoplastica, laparotomie, artroprotesi, ernie) |
| **Elemento del metodo** | `fase-0-piramide-del-comando.md`, §5 Trauma: *"Cicatrici = tiranti invisibili: ogni cicatrice è una densificazione permanente… Una cicatrice diventa il punto prioritario finché non la liberi"*. La formulazione implica una **lisi meccanica** dell'aderenza e, per estensione operativa, che il lavoro debba andare **in profondità** per essere efficace. |
| **Perché è sbagliato** | (a) **Nessuno studio nell'uomo** ha documentato che la terapia manuale sciolga aderenze intra-addominali; la revisione sistematica dedicata riporta miglioramento **dei sintomi** correlati alle aderenze (forte-preliminare sull'acuto, moderata sul cronico post-chirurgico), non la loro lisi — Wasserman JB, Copeland M, Upp M, Abraham K, *J Bodyw Mov Ther* 2019;23(2):262-269, [PMID 31103106](https://pubmed.ncbi.nlm.nih.gov/31103106/). (b) L'unico RCT sul dolore cronico post-cesareo ha confrontato **massaggio superficiale + skin rolling** contro **lo stesso più release miofasciale profondo e mobilizzazione diretta della cicatrice**: entrambi i gruppi migliorano su dolore, soglia pressoria, ODI e mobilità della cicatrice, **senza differenza tra i gruppi** — Wasserman JB, Abraham K, Massery M, et al., *J Womens Health Phys Therap* 2018;42(3):111-119, DOI [10.1097/JWH.0000000000000103](https://doi.org/10.1097/JWH.0000000000000103) (rivista non indicizzata su PubMed). (c) Ciò che è stato **misurato** dopo mobilizzazione è il cambiamento delle proprietà viscoelastiche superficiali e delle soglie pressorie/tattili — Gilbert I, Gaudreault N, Gaboury I, *J Integr Complement Med* 2022;28(4):355-362, [PMID 35426735](https://pubmed.ncbi.nlm.nih.gov/35426735/). "Densificazione permanente" è inoltre smentito dall'esito: cicatrici di 6-9 anni rispondono. |
| **Cosa fa la procedura** | Sostituisce *"liberare / sciogliere l'aderenza"* con **"restituire scorrimento e innalzare la soglia"**, misurati (glide test 0-3 in 4 direzioni, area ipoestesica, algometria). Dichiara il perimetro aderenziale (Parte IV §Fasciale-Cicatriziale, "Il perimetro aderenziale") e la regola di dose: **il tessuto detta la profondità, non il protocollo** — nella paziente reattiva il livello superficiale è una scelta clinica, non un ripiego. |
| **Se ratificata** | Riformulare il punto "Cicatrici = tiranti invisibili" in `fase-0-piramide-del-comando.md` (§5 Trauma): tirante meccanico che riduce lo scorrimento fra piani, bersaglio = scorrimento e soglia, **non** lisi dell'aderenza; e togliere l'implicazione che la profondità sia la leva. |

---

### D-041 · La lesione "a distanza" della cicatrice presentata come causa del dolore lontano

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Cicatrici da taglio cesareo (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui una restrizione locale viene presentata come **causa** di un sintomo in sede lontana ("tiri un filo della maglia sul fondo, la scollatura si deforma") |
| **Elemento del metodo** | `fase-0-piramide-del-comando.md`, §5 Trauma e §6 Fasciale: la regola d'oro *"spesso il trauma è lontano dal dolore"* e la metafora del filo tirato, usate come **spiegazione causale** da comunicare (CP lombare ← CC cicatriziale). |
| **Perché è sbagliato** | Come **euristica d'indagine** è utile e va tenuta; come **claim causale** non regge. Non esiste alcuno studio che dimostri che la cicatrice da cesareo causi lombalgia, né che trattarla la risolva: la revisione narrativa più recente sul dolore post-cesareo dichiara che mancano perfino standard condivisi di trattamento fisioterapico della cicatrice (Bajerová M, Hruban L, *Ceska Gynekol* 2026;91(3):232-238, [PMID 42419951](https://pubmed.ncbi.nlm.nih.gov/42419951/)). Il proxy anatomico più vicino mai testato — la diastasi dei retti — è stato **misurato e non associato** al dolore lombo-pelvico: a 6 mesi dal parto le donne con diastasi non riportavano più dolore lombo-pelvico delle altre (Fernandes da Mota PG, Pascoal AG, Carita AI, Bø K, *Man Ther* 2015;20(1):200-205, [PMID 25282439](https://pubmed.ncbi.nlm.nih.gov/25282439/)). Annunciare il nesso al primo colloquio espone a una promessa che il re-test può smentire. |
| **Cosa fa la procedura** | Introduce un **"perimetro di onestà"** esplicito (Parte II): il nesso è un'**ipotesi testabile**, non un fatto — si misura la sede lontana, si tratta la cicatrice, **si ri-misura subito**; se cede, la prova vale *per quella paziente*, se non cede la sede lontana si tratta per sé. Frase autorizzata: *"proviamo se sono collegate e te lo dico dopo"*; frase vietata: *"il tuo mal di schiena viene dalla cicatrice"*. La diastasi si misura e non si presenta come causa del dolore. |
| **Se ratificata** | Marcare in `fase-0-piramide-del-comando.md` la regola "il trauma è lontano dal dolore" come **euristica d'indagine da confermare con re-test**, non come meccanismo da comunicare al paziente. |

---

### D-060 · Il re-test immediato di Stecco come prova che il bersaglio era sbagliato, applicato al dolore neuropatico/radicolare

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Sciatalgia (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione con componente neuropatica o radicolare (sciatalgia, cervicobrachialgia, ernia del disco, sindrome di Arnold, tunnel carpale, nevralgie) |
| **Elemento del metodo** | `fase-0-piramide-del-comando.md`, §2 Sistema Fasciale: *"Re-test immediato: liberato il CC, il CP migliora istantaneamente. Se non migliora, hai sbagliato CC o piano di movimento."* Ripreso in §3 come conferma obbligatoria della chiave di volta. |
| **Perché è sbagliato** | La regola è valida per il dolore di origine miofasciale, dove la variazione di tono e di scorrimento è immediata. **Non è valida per il tessuto nervoso.** Nelle neuropatie da intrappolamento e nel dolore radicolare i sintomi sono sostenuti da neuroinfiammazione locale e remota e, nelle forme con coinvolgimento assonale, da alterazioni della conduzione: il recupero segue tempi biologici di giorni-settimane, non di secondi (Schmid AB, Fundaun J, Tampin B. *Entrapment neuropathies: a contemporary approach to pathophysiology, clinical assessment, and management.* Pain Rep 2020;5(4):e829, [PMID 32766466](https://pubmed.ncbi.nlm.nih.gov/32766466/); Schmid AB, Hailey L, Tampin B. *Entrapment Neuropathies: Challenging Common Beliefs With Novel Evidence.* J Orthop Sports Phys Ther 2018;48(2):58-62, [PMID 29385943](https://pubmed.ncbi.nlm.nih.gov/29385943/)). Applicata qui, la regola produce due errori opposti e entrambi dannosi: far **abbandonare un bersaglio corretto** perché il re-test è piatto, o spingere il clinico ad **aumentare l'intensità** su un tessuto irritabile per "ottenere" la risposta immediata. |
| **Cosa fa la procedura** | Dichiara esplicitamente (Parte 0, §"Come decido", cautela sul re-test) che **nel dolore radicolare il re-test immediato è informazione, non verdetto**, e che un re-test piatto non autorizza né a cambiare bersaglio né ad aumentare la dose. Sposta la verifica del dominante su una finestra a **3 sedute** con parametri ripetibili (SLR in gradi + VAS gamba + centralizzazione), e mantiene il re-test immediato solo come segnale di responsività. |
| **Se ratificata** | Aggiungere in `fase-0-piramide-del-comando.md` (§Sistema Fasciale e §3) la qualificazione di scope: il re-test immediato vale per il tessuto miofasciale; nel tessuto nervoso la finestra di verifica è di giorni-settimane. |
| **Coerenza** | Complementare alle voci aperte su **Ernia del disco (v1)**: "Decompressione discale / riduzione dell'ernia come obiettivo del gesto manuale" e "Il modello Neurologico ridotto all'autonomico". La procedura Sciatalgia applica entrambe: nessun claim di decompressione della radice, modello Neurologico riscritto sull'asse neurale periferico (radice, DRG, meccanosensibilità), screening neurologico segmentario che **precede** il ragionamento sulla dominanza a ogni seduta. |

---

### D-030 · La regola "non trattare quasi mai il CP" applicata all'artrosi

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Artrosi (v1) |
| **Ambito** | Condizioni artrosiche e degenerative articolari (ginocchio, anca, mano, spalla); potenzialmente ogni condizione in cui il sito sintomatico è esso stesso il tessuto malato |
| **Elemento del metodo** | Motore Clinico, Sistema Fasciale/Stecco: *"La regola d'oro: NON trattare quasi mai il CP"* (`fase-0-piramide-del-comando.md`, §2, 6° Sistema Fasciale). |
| **Perché è sbagliato** | Nell'artrosi il Centro di Percezione **è** l'articolazione patologica, e l'unico approccio manuale con supporto in RCT la tratta direttamente. Deyle et al., *Ann Intern Med* 2000;132(3):173-181 ([PMID 10651597](https://pubmed.ncbi.nlm.nih.gov/10651597/)): il braccio attivo riceveva terapia manuale **applicata al ginocchio** oltre che a rachide lombare, anca e caviglia "as required" — non al posto loro. Lo stesso pacchetto è il braccio vincente in Deyle et al., *N Engl J Med* 2020;382(15):1420-1429 ([PMID 32268027](https://pubmed.ncbi.nlm.nih.gov/32268027/)). Applicare qui la regola "non trattare il CP" significa rinunciare alla componente testata dell'intervento. |
| **Cosa fa la procedura** | Dichiara esplicitamente l'inversione in Parte 0 (box "Un'inversione che questa condizione impone") e la ripete in Parte III, blocco B: si tratta **il bersaglio e la catena insieme**, non l'uno al posto dell'altra. Il ragionamento CC/CP resta come guida alla ricerca dei compensi (TFL/ileotibiale, vasto laterale, popliteo, tricipite surale, glutei), non come divieto di toccare il sito. |
| **Se ratificata** | Qualificare la regola in `fase-0-piramide-del-comando.md`: "non trattare *solo* il CP" anziché "non trattare il CP", con eccezione esplicita per le condizioni in cui il sito sintomatico è il tessuto patologico. |

---

### D-031 · "Perché l'osteopatia è superiore all'approccio standard" nell'artrosi

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Artrosi (v1) |
| **Ambito** | Trasversale — riguarda la sezione 4 dell'architettura in ogni condizione dove il comparatore ha evidenza superiore o pari alla nostra |
| **Elemento del metodo** | `architettura-procedura.md`, sezione 4: *"Perché l'osteopatia è superiore all'approccio standard"*, con 3 punti che rivendicano meccanismi che "solo le mani" possono attivare. |
| **Perché è sbagliato** | Sull'artrosi lo "standard" con la migliore evidenza non è un farmaco ma **l'esercizio terapeutico** (Fransen, Cochrane 2015, [PMID 25569281](https://pubmed.ncbi.nlm.nih.gov/25569281/): evidenza di alta qualità) e il **calo ponderale** (Messier, IDEA, *JAMA* 2013, [PMID 24065013](https://pubmed.ncbi.nlm.nih.gov/24065013/)). Rispetto ad esso, Runge, Aina e May (*J Orthop Sports Phys Ther* 2022;52(10):675-684, [PMID 35881705](https://pubmed.ncbi.nlm.nih.gov/35881705/)) riportano **certezza ALTA di nessun beneficio aggiuntivo della terapia manuale a lungo termine**. Un titolo che rivendica superiorità sarebbe un claim gonfiato contro un dato ad alta certezza — esattamente ciò che il lucchetto vieta. |
| **Cosa fa la procedura** | Rinomina la sezione in *"Cosa fanno le mani che il farmaco, l'infiltrazione e l'ausilio non fanno"* e sposta il confronto dal podio al **piano di lavoro**: ridistribuzione del carico, riattivazione dell'ammortizzatore muscolare, down-regulation aspecifica dichiarata come tale. Il confronto con Deyle 2020 (manuale + esercizio vs infiltrazione) è citato come dato reale, quello con l'esercizio come limite dichiarato. Coerente con D-004 (niente claim neuroendocrini sul tocco). |
| **Se ratificata** | Riformulare la sezione 4 di `architettura-procedura.md` come *"Cosa fanno le mani che l'approccio standard non fa"*, con l'obbligo di dichiarare il comparatore a evidenza superiore quando esiste. |

---

### D-032 · Il modello Respiratorio-Circolatorio applicato per intero (leva diaframmatica) nelle artrosi periferiche

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Artrosi di ginocchio e anca (v2 → registrata in v3) |
| **Ambito** | Artrosi periferiche in primis; da valutare per estensione alle altre condizioni articolari degli arti |
| **Elemento del metodo** | Modello Respiratorio-Circolatorio: va applicato per intero, con il **diaframma come pompa e regolatore pressorio** più la dinamica dei fluidi, e con una propria **procedura operativa** in Parte IV al pari degli altri modelli. |
| **Perché è sbagliato** | Su un'articolazione periferica non esiste una leva diaframmatica documentata: nessuno studio collega l'escursione del diaframma al versamento, al dolore o alla funzione nel ginocchio e nell'anca artrosici, e **nessuno ha misurato il volume articolare prima e dopo OMT** in questa condizione. Il carico ciclico che effettivamente nutre la cartilagine avascolare è quello **attivo** del paziente — Bricca A, Juhl CB, Steultjens M, Wirth W, Roos EM, *Impact of exercise on articular cartilage in people at risk of, or with established, knee osteoarthritis: a systematic review of randomised controlled trials*, Br J Sports Med 2019;53(15):940-947, [PMID 29934429](https://pubmed.ncbi.nlm.nih.gov/29934429/) — non l'oscillazione passiva della mano né una pompa toracica. Assegnare minuti di seduta a una leva senza resa misurabile è, per un junior, tempo sottratto ai due blocchi che il dato sostiene (carico attivo e counseling metabolico). |
| **Cosa fa la procedura** | Parte 0 §Respiratorio-Circolatorio e Parte IV §"Regola idraulica articolare": la componente diaframmatica è **omessa dichiaratamente**, il modello è ridotto alla dinamica dei fluidi periarticolare e vale come **regola di dosaggio del carico**, non come procedura ("non produce un effetto misurabile con le tue mani, quindi non merita minuti di seduta"). L'inibizione artrogenica è riattribuita al modello Neurologico, dove è un riflesso spinale. |
| **Se ratificata** | Introdurre nel metodo che ogni modello si applica **nella sola componente pertinente alla condizione e alla regione**, e che un modello senza leva documentata si dichiara come **regola di dosaggio** invece di ricevere d'ufficio una procedura operativa in Parte IV. |
| **Coerenza** | Stessa logica di **D-012** (componente circolatorio-linfatica non pertinente alla lombalgia) e di **D-005** (leva circolatoria usata solo dove documentata). Nota collegata: **D-008 · ernia** (modello Neurologico non riducibile all'autonomico) è registrata con ambito alle sole condizioni neuropatiche, ma l'artrosi la applica già estendendo il modello a nocicezione, segmenti e inibizione artrogenica — se ne propone l'estensione d'ambito alle condizioni muscoloscheletriche non neuropatiche. |

---

### D-020 · "Il diaframma massaggia il viscere: respiro corto = massaggio debole"

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Stitichezza cronica (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione addomino-viscerale in cui si invoca il diaframma come "pompa/massaggiatore" dei visceri e la distensione addominale come sintomo bersaglio (stitichezza, gonfiore addominale, colon irritabile, problemi digestivi, diastasi) |
| **Elemento del metodo** | Modello Respiratorio-Circolatorio: il diaframma come pompa premente/aspirante il cui **ipomobilità** produce stasi; corollario operativo "riattiva un diaframma pigro". Formulazione presente anche nel materiale di marketing (`problemi.json`, `meccanismo_causa`: *"il diaframma lo massaggia dall'alto a ogni respiro: respiro corto, massaggio debole"*). |
| **Perché è sbagliato** | Nella **distensione addominale funzionale** il reperto strumentale è l'opposto di un diaframma pigro: TC addomino-toracica ed EMG mostrano che durante gli episodi il diaframma **si contrae e discende** (+19% EMG, 12 mm di discesa) mentre la parete anteriore **si rilascia e protrude** (+32 mm di girth) — una **dissinergia addomino-frenica**, cioè un problema di *coordinazione*, non di *ipomobilità*. La correzione documentata è ottenuta con **biofeedback EMG mirato al respiro** (girth −25 mm), non con tecniche manuali. Fonte: Barba E, Burri E, Accarino A, … Azpiroz F. *Abdominothoracic mechanisms of functional abdominal distension and correction by biofeedback.* Gastroenterology 2015;148(4):732-9 — [PMID 25500424](https://pubmed.ncbi.nlm.nih.gov/25500424/). |
| **Cosa fa la procedura** | Riformula il bersaglio del modello respiratorio da *"riattivare un diaframma pigro"* a **"ricoordinare uno stantuffo che spinge nel verso sbagliato"**, con outcome atteso dichiarato sul **gonfiore/distensione e sulla qualità della spinta**, non sul transito. Dichiara esplicitamente che la correzione è documentata con biofeedback EMG e che la versione manuale è **PLAUSIBILE, non dimostrata**. Il "massaggio viscerale del respiro" resta scritto come razionale coerente **non misurato**. |
| **Se ratificata** | Aggiornare il modello Respiratorio-Circolatorio in `cinque-modelli.md` e `cinque-modelli-osteopatici.md`: sulle condizioni con distensione funzionale il bersaglio è la **coordinazione addomino-frenica**, non l'ipomobilità diaframmatica; citare Barba/Azpiroz come fonte del meccanismo. |

---

### D-021 · Il lavoro sub-occipitale come "accesso vagale" a un viscere sotto la flessura splenica

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Stitichezza cronica (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione del colon distale, del retto e del pavimento pelvico (stitichezza, colon irritabile, diarrea ricorrente, gonfiore addominale, dolore al coccige, ciclo doloroso) |
| **Elemento del metodo** | Motore Clinico / modello Neurologico: il **nervo vago** come "re del parasimpatico" e la base cranica (sub-occipitali, OA, forame giugulare) come **ingresso vagale** per la regolazione viscerale — applicato indistintamente a tutti i visceri addominali. Estende D-002 e D-004, che avevano già declassato la leva vagale su stomaco/esofago. |
| **Perché è sbagliato** | È un errore di **territorio anatomico**, non solo di grado di evidenza. L'innervazione parasimpatica vagale del tubo digerente si arresta **intorno alla flessura splenica**; **colon discendente, sigma e retto** — cioè esattamente i segmenti che determinano l'evacuazione — ricevono il parasimpatico dai **nervi splancnici pelvici (S2-S4)**, e la muscolatura striata del pavimento pelvico dal **pudendo (S2-S4)**. Anche concedendo un effetto vagale al contatto sub-occipitale (già dichiarato non dimostrato in D-002/D-004), quella via **non raggiunge il bersaglio**. Fonti: StatPearls, *Anatomy, Abdomen and Pelvis: Splanchnic Nerves* — [NBK560504](https://www.ncbi.nlm.nih.gov/books/NBK560504/); Bharucha AE, Lacy BE. *Mechanisms, Evaluation, and Management of Chronic Constipation.* Gastroenterology 2020;158(5):1232-1249 — [PMID 31945360](https://pubmed.ncbi.nlm.nih.gov/31945360/). |
| **Cosa fa la procedura** | Dichiara in Parte 0 (§Neurologico) e in Parte III (§3, *"Due centraline e nessun cavo diretto"*) che **il sub-occipitale non è un accesso al sigma**, e sposta il ragionamento parasimpatico sul **sacro e sul bacino** per il colon distale, mantenendolo come **razionale anatomico, non effetto misurato** (nessuno ha registrato attività colica dopo tecnica sacrale). Il lavoro cervicale alto resta ammesso solo come **down-regulation aspecifica**, con screening VBI obbligatorio. |
| **Se ratificata** | Aggiungere in `fase-0-piramide-del-comando.md` (§Sistema Neurologico, voce "Nervo Vago") e in `cinque-modelli.md` (modello Neurologico) il limite di territorio: vago fino alla flessura splenica, sacrale (S2-S4) da lì in giù. Il "vago" non è un sinonimo di "parasimpatico viscerale". |

---

### D-007 · "Decompressione discale" / riduzione dell'ernia come obiettivo del gesto manuale

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Ernia del disco (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui si invoca la "decompressione" di una struttura profonda come effetto del gesto manuale (ernia discale, stenosi, conflitto sub-acromiale) |
| **Elemento del metodo** | `architettura-procedura.md`, sezione 4, indica come modello la tripletta *Decompressione fisica / Reset propriocettivo / Effetto neurobiologico del tocco*: la "decompressione fisica" applicata al disco diventa il claim che pompage, trazione manuale e tecniche in decoaptazione **riducono l'ernia** o **decomprimono la radice**. |
| **Perché è sbagliato** | È un'inferenza dalla direzione della forza, non una misura. Nessuno studio ha misurato dimensione dell'ernia o spazio radicolare prima e dopo una seduta di terapia manuale; l'unico RCT che aveva incluso la riduzione della protrusione in RM fra gli outcome (Santilli 2006, [PMID 16517383](https://pubmed.ncbi.nlm.nih.gov/16517383/)) non riporta quel risultato fra gli effetti dimostrati, che restano sul dolore. Soprattutto, il riassorbimento è **il decorso naturale**: in trattamento conservativo la regressione spontanea è del 96% nelle ernie sequestrate, 70% nelle espulse, 41% nelle protrusioni (Chiu 2015, [PMID 25009200](https://pubmed.ncbi.nlm.nih.gov/25009200/)). Attribuire alle mani un fenomeno che avviene comunque è il claim gonfiato più facile da smontare per un medico. |
| **Cosa fa la procedura** | Sostituisce "decompressione / riduzione dell'ernia" con due obiettivi misurabili e difendibili: **riduzione dell'input meccanico sul segmento** e **riduzione della meccanosensibilità della radice con recupero di scorrimento** (parametro di re-test: gradi dello SLR + VAS gamba). Dichiara esplicitamente, nella sezione evidenza e nella scheda, che il gesto manuale non riduce l'ernia e che il riassorbimento è spontaneo. |
| **Se ratificata** | Riformulare il primo punto della tripletta in `architettura-procedura.md` (es. *"Modifica del carico meccanico sul segmento — effetto su input e sensibilità, non sulla lesione"*) e marcare "decompressione discale" fra i claim non utilizzabili. |

---

### D-008 · Il modello Neurologico ridotto all'autonomico, senza l'asse neurale periferico

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Ernia del disco (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione a dolore neuropatico periferico (ernia lombare e cervicale, cervicobrachialgia, tunnel carpale, sindromi da intrappolamento, dolore radicolare toracico) |
| **Elemento del metodo** | `cinque-modelli-osteopatici.md`, modello Neurologico: *"equilibrio autonomico, nocicezione, segmenti facilitati, riflessi viscero-somatici e somato-viscerali, nervo vago e frenico"*. Nel Motore Clinico (`fase-0-piramide-del-comando.md`) il sistema Neurologico è descritto come "Comandante Supremo" in chiave di **iper-ortosimpaticotonia**. |
| **Perché è sbagliato** | Non è falso, è **incompleto in modo clinicamente pericoloso**. Nel dolore spinale irradiato all'arto il generatore non è il tono autonomico: sono la radice e il **ganglio della radice dorsale**, con compressione, **neuroinfiammazione**, ischemia e perdita di scorrimento (Schmid, Fundaun, Tampin, *Pain Rep* 2020, [PMID 32766466](https://pubmed.ncbi.nlm.nih.gov/32766466/)). La stessa letteratura ha formalizzato la classificazione — dolore somatico riferito / radicolare / radicolopatia — e la gradazione del dolore neuropatico (NeuPSIG-IASP: Schmid et al., *Pain* 2023, [PMID 37235637](https://pubmed.ncbi.nlm.nih.gov/37235637/)). Un modello Neurologico che copre solo l'autonomico porta il junior a "calmare il sistema" con lavoro sub-occipitale e respiro mentre un deficit motorio segmentario non viene misurato. |
| **Cosa fa la procedura** | Dichiara esplicitamente, nella Parte 0, che *"in questa condizione il modello Neurologico non è primariamente l'autonomico"* e ne riscrive gli attori sull'**asse neurale periferico** (radice, DRG, interfacce meccaniche, sensibilizzazione centrale). Aggiunge una regola che sta **sopra** la gerarchia del Motore Clinico: lo **screening neurologico segmentario e della cauda equina precede il ragionamento sulla dominanza**, a ogni seduta. Il tocco sull'autonomico resta dichiarato PLAUSIBILE, non dimostrato (coerente con D-002 e D-004). |
| **Se ratificata** | Estendere la descrizione del modello Neurologico in `cinque-modelli-osteopatici.md` e in `direttore-osteopatico-modelli/references/cinque-modelli.md` all'asse neurale periferico (nervo, radice, DRG, mechanosensitivity, neuroinfiammazione) e alla gradazione NeuPSIG del dolore neuropatico; inserire in `fase-0-piramide-del-comando.md` la clausola di precedenza dello screening neurologico sulla ricerca del dominante. |

---

### D-007 · La diagnosi posizionale palpatoria come criterio decisionale

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Lombalgia (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione muscolo-scheletrica in cui il dominante viene identificato con la palpazione di reperi ossei ("bacino ruotato", "gamba corta", "vertebra fuori posto") o della qualità del tessuto ("densificazione", "glide", "tessuto freddo come plastica") |
| **Elemento del metodo** | Motore Clinico: i segnali di dominanza sono in larga parte **palpatori posizionali e di texture** (fasciale: mancanza di glide; trauma: tessuto inerte e freddo; viscerale: pelle spessa sopra il segmento), usati come criterio per decidere su cosa lavorare. |
| **Perché è sbagliato** | La revisione sistematica di riferimento sull'affidabilità della palpazione spinale (Seffinger MA et al., *Reliability of spinal palpation for diagnosis of back and neck pain: a systematic review of the literature*, Spine 2004;29(19):E413-25, [PMID 15454722](https://pubmed.ncbi.nlm.nih.gov/15454722/)) riporta che i test di **provocazione del dolore** raggiungono affidabilità accettabile nel 64% degli studi, i test di movimento nel 58%, la **localizzazione dei reperi nel 33%** e i **test palpatori sui tessuti molli paraspinali nello 0%**. L'esperienza, la disciplina, il training immediatamente precedente e il consenso sulla procedura **non migliorano** l'affidabilità. Un segnale che due operatori non riproducono non può essere il criterio che decide il trattamento. |
| **Cosa fa la procedura** | Mantiene la palpazione come **generatore di ipotesi**, mai come diagnosi. Il criterio decisionale diventa la triade **provocazione + misura oggettiva + re-test**: test funzionale guida con VAS, cluster di provocazione sacroiliaca di Laslett (≥3/5), gradi di rotazione interna d'anca, escursione costale, sit-to-stand. La "prova della chiave di volta" si conferma **ri-misurando due parametri insieme**, non riappoggiando le mani. Dichiarato esplicitamente in Parte 0 (§Biomeccanico, "Ciò che NON regge") e in Parte II §3. |
| **Se ratificata** | Riformulare i "segnali di dominanza" del Motore Clinico distinguendo i segnali **riproducibili** (provocazione, ROM misurato, modulazione del sintomo) da quelli **euristici** (texture, glide, temperatura), e vincolare la decisione ai primi. |

---

### D-008 · Il "riequilibrio dello schema motorio" e l'esercizio specifico come leva superiore

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Lombalgia (v1) |
| **Ambito** | Trasversale — riguarda ogni condizione muscolo-scheletrica in cui si prescrive un esercizio "specifico" (controllo motorio, core stability, stabilizzazione segmentale) presentandolo come più efficace dell'esercizio generico |
| **Elemento del metodo** | Modello Biomeccanico e narrativa di casa: "su uno schema di movimento sbagliato il rinforzo consolida l'errore", da cui l'implicazione che serva l'esercizio *corretto e specifico*. |
| **Perché è sbagliato** | La revisione Cochrane di Saragiotto BT, Maher CG, Yamato TP et al., *Motor control exercise for chronic non-specific low-back pain*, Cochrane Database Syst Rev 2016;(1):CD012004, [PMID 26742533](https://pubmed.ncbi.nlm.nih.gov/26742533/) (29 RCT, n=2.431) conclude che l'esercizio di controllo motorio **non è clinicamente superiore** ad altre forme di esercizio (evidenza da bassa a moderata) né alla terapia manuale (evidenza da moderata ad alta), e che la scelta dell'esercizio "dovrebbe dipendere da preferenze del paziente o del terapista, formazione, costi e sicurezza". L'effetto documentato è quello dell'esercizio **in quanto tale** rispetto all'intervento minimo (Hayden JA et al., Cochrane 2021, [PMID 34580864](https://pubmed.ncbi.nlm.nih.gov/34580864/), 249 trial). |
| **Cosa fa la procedura** | Sposta il claim dalla *specificità* all'*aderenza*: "nessun tipo di esercizio è superiore agli altri; l'esercizio giusto è quello che il paziente farà davvero" (Parte 0, §Metabolico-Energetico). Gli esercizi prescritti sono scelti perché **desensibilizzano il gesto temuto** e sono sostenibili, non perché correggano uno schema. Nella lista "cosa non puoi dire" compare esplicitamente che il core stability non è "l'esercizio corretto". |
| **Se ratificata** | Rimuovere dal linguaggio di metodo la promessa implicita di correzione dello schema motorio come leva specifica, e sostituirla con dose, aderenza ed esposizione graduata. |

---

### D-009 · L'apnea e il *bracing* nel gesto letti come causa meccanica del dolore lombare

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Lombalgia non specifica (v2 → registrata in v3) |
| **Ambito** | Trasversale — riguarda ogni condizione muscoloscheletrica del tronco in cui si insegna a "togliere l'apnea" o a "rilasciare il diaframma" come leva meccanica |
| **Elemento del metodo** | Modello Respiratorio-Circolatorio: il respiro trattenuto e la rigidità addominale nel gesto presentati come **generatori meccanici** del sovraccarico lombare, da eliminare. |
| **Perché è sbagliato** | La pressione intra-addominale **aumenta** la rigidità e la stabilità del rachide lombare: Hodges PW, Eriksson AEM, Shirley D, Gandevia SC. *Intra-abdominal pressure increases stiffness of the lumbar spine.* J Biomech 2005;38(9):1873-80, [PMID 16023475](https://pubmed.ncbi.nlm.nih.gov/16023475/) — la stimolazione frenica isolata, senza attività di addominali ed estensori, aumenta la rigidità a L2 e L4. Sotto carico elevato un *brace* breve e controllato è quindi la strategia **normale e corretta**, non un difetto da correggere. Ciò che è disadattivo è il **bracing indiscriminato e sostenuto a basso carico**, che è un **marcatore comportamentale** (evitamento, protezione appresa), non la causa meccanica del dolore. |
| **Cosa fa la procedura** | Nota di metodo in Parte 0 §Respiratorio: la regola è una **dose**, non un divieto (*a basso carico espira e lascia morbido; sotto carico alto il brace è fisiologico*). L'apnea a basso carico è elencata fra i segnali di dominanza del **solo modello Comportamentale**; i segnali del Respiratorio restano escursione costale bassa in cm, asimmetria e peggioramento sotto sforzo pressorio. |
| **Se ratificata** | Correggere nei documenti di metodo la lettura del respiro trattenuto come generatore meccanico, e distinguere esplicitamente *brace fisiologico sotto carico* da *bracing sostenuto a basso carico*. |
| **Coerenza** | Il segnale non può stare in due modelli: se decide il montaggio della seduta (blocco respiratorio vs blocco comportamentale), l'attribuzione dev'essere unica. |

---

### D-010 · La fascia toraco-lombare come organo propriocettivo ("fusi neuromuscolari fasciali")

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Lombalgia non specifica (v2 → registrata in v3) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui si giustifica il lavoro fasciale con la "ricchezza propriocettiva" della fascia |
| **Elemento del metodo** | Modello Neurologico / Sistema Fasciale: la fascia descritta come organo propriocettivo per la densità di **fusi neuromuscolari**, da cui l'idea che lavorarla "riprogrammi" l'informazione propriocettiva. |
| **Perché è sbagliato** | Il fuso neuromuscolare è un recettore **intramuscolare**: la capsula è incorporata nel perimisio e misura la lunghezza delle fibre muscolari, non la tensione della fascia. Chiamarlo "recettore fasciale" sposta a un tessuto una funzione che appartiene a un altro. Ciò che è documentato per la fascia toraco-lombare è invece l'innervazione **nocicettiva**: Schilder A, Hoheisel U, Magerl W, Benrath J, Klein T, Treede RD. *Sensory findings after stimulation of the thoracolumbar fascia with hypertonic saline suggest its contribution to low back pain.* Pain 2014;155(2):222-31, [PMID 24076047](https://pubmed.ncbi.nlm.nih.gov/24076047/) — la TLF è il tessuto profondo del dorso **più sensibile** alla stimolazione chimica, con descrittori (urente, pulsante, pungente) da fibre A e C e irradiazione maggiore di cute e muscolo. |
| **Cosa fa la procedura** | Parte 0 §Neurologico e Parte IV: la fascia toraco-lombare è dichiarata **fonte periferica nocicettiva plausibile, non organo propriocettivo**; il razionale del contatto è pressione bassa e sostenuta sotto soglia, non "riprogrammazione propriocettiva". |
| **Se ratificata** | Rimuovere dai documenti di metodo l'attribuzione dei fusi neuromuscolari alla fascia e riscrivere il razionale del lavoro fasciale su base nocicettiva. |

---

### D-011 · Il Centro di Coordinazione confermato dalla palpazione della densificazione

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Lombalgia non specifica (v2 → registrata in v3) |
| **Ambito** | Trasversale — riguarda ogni condizione in cui si usa il linguaggio CC/CP di Stecco |
| **Elemento del metodo** | Motore Clinico: il **Centro di Coordinazione** individuato e confermato con la palpazione della densificazione, che diventa il criterio decisionale del bersaglio. |
| **Perché è sbagliato** | Lo stesso motivo per cui è aperta **D-007 · lombalgia**: la palpazione dei tessuti molli paraspinali non è affidabile e sui reperi ossei è al più accettabile, comunque **inferiore ai test di provocazione del dolore** (Seffinger MA et al., *Reliability of spinal palpation for diagnosis of back and neck pain*, Spine 2004). Una procedura non può dichiarare non affidabile la palpazione in Parte 0 e poi usarla come conferma del bersaglio nel Motore Clinico: è una contraddizione interna prima ancora che un errore di evidenza. |
| **Cosa fa la procedura** | Il CC/CP è dichiarato **linguaggio euristico** per *nominare* la regione candidata a monte; la conferma è sempre il **re-test funzionale** su gesto guida più un parametro oggettivo, mai la palpazione. |
| **Se ratificata** | In `fase-0-piramide-del-comando.md`, sostituire la conferma palpatoria del CC con la conferma funzionale. |
| **Coerenza** | Coerente con **D-007 · lombalgia** e con la cautela di **D-060** sul valore del re-test immediato nel tessuto nervoso. |

---

### D-012 · La componente circolatorio-linfatica del modello Respiratorio-Circolatorio applicata alla lombalgia

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Lombalgia non specifica (v2 → registrata in v3) |
| **Ambito** | Lombalgia in primis; da valutare per estensione alle altre condizioni muscoloscheletriche del rachide |
| **Elemento del metodo** | Il modello Respiratorio-Circolatorio va applicato **per intero**, comprensivo della leva circolatorio-linfatica (drenaggio, "pompe", congestione tissutale), in ogni condizione. |
| **Perché è sbagliato** | Sulla lombalgia non specifica non esiste alcun dato che colleghi il drenaggio linfatico o venoso al dolore lombare, né come meccanismo né come esito. L'unica componente del modello con un dato pubblicato su questa condizione è la funzione **biomeccanica** del diaframma (Kolar P et al., *Postural function of the diaphragm in persons with and without chronic low back pain*, JOSPT 2012 — caso-controllo, escursione diaframmatica ridotta durante i compiti d'arto). Applicare la parte circolatorio-linfatica significherebbe importare un claim senza fonte in un documento che dichiara per ogni modello il proprio grado di evidenza: è esattamente il tipo di gonfiaggio che il "lucchetto della corazza" esiste per impedire. |
| **Cosa fa la procedura** | Parte 0 §Respiratorio-Circolatorio, "Limite di pertinenza dichiarato": si usa la sola funzione biomeccanica del diaframma e si **dichiara** che la componente circolatorio-linfatica non è pertinente a questa condizione. |
| **Se ratificata** | Introdurre nel metodo il principio che ogni modello si applica **nella sola componente pertinente alla condizione**, con il limite di pertinenza dichiarato nel testo — non per intero d'ufficio. |
| **Coerenza** | Stessa logica di **D-005** (lavoro suturale come leva sul deflusso venoso giugulare): una leva circolatoria si usa solo dove è documentata. |

---

### D-007 · La manipolazione spinale ad alta velocità come leva del modello Biomeccanico nell'emicrania

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Emicrania (v1) |
| **Ambito** | Emicrania in primis; da valutare per estensione alle altre cefalee primarie |
| **Elemento del metodo** | Modello Biomeccanico-Strutturale: il thrust/HVLA spinale come tecnica disponibile e legittima ovunque ci sia una restrizione articolare documentata. `cinque-modelli-osteopatici.md` non pone limiti di tecnica per condizione, e la Parte 0 dei modelli invita a lavorare sulla disfunzione somatica trovata. |
| **Perché è sbagliato** | Sull'emicrania il rapporto rischio/beneficio del thrust è **sfavorevole per dato pubblicato**. La revisione sistematica aggiornata *Spinal manipulations for migraine* (Posadzki, Klimek, Ernst — *Syst Rev* 2024;13:296, [PMID 39614402](https://pubmed.ncbi.nlm.nih.gov/39614402/)) su 6 RCT e 645 emicranici non trova effetto su intensità (SMD −0,22; IC −0,65/0,21), durata o qualità di vita emotiva, e la meta-analisi di due trial mostra un **aumento del rischio di eventi avversi (RR 2,06; IC 1,24-3,41; NNH ≈ 6)**. Un'evidenza nulla di beneficio accanto a un segnale positivo di danno non autorizza la tecnica, per quanto la restrizione articolare sia reale. La presenza dei segni cervicali (Luedtke 2018) giustifica il *bersaglio*, non quella *dose*. |
| **Cosa fa la procedura** | Esclude esplicitamente il **thrust cervicale ad alta velocità** dal repertorio su questa condizione, sia in Parte 0 (modello Biomeccanico) sia nel blocco Controindicazioni sia nella Scheda Operativa. Il repertorio dichiarato è mobilizzazione a bassa velocità entro il range indolore, inibizione, tessuti molli, energia muscolare. |
| **Se ratificata** | Introdurre nei documenti di metodo il principio che la scelta della **dose di tecnica** (thrust vs mobilizzazione) è vincolata all'evidenza *per condizione*, non solo alla disfunzione palpata, e registrare l'emicrania come condizione a esclusione del thrust cervicale. |

---

### D-072 · Il modello Respiratorio-Circolatorio applicato per intero (leva diaframmatica e circolatoria) nel bruxismo

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Bruxismo (v2 → registrata in v3) |
| **Ambito** | Bruxismo e disturbi temporomandibolari; da valutare per estensione a ogni condizione in cui il modello ha valore di **screening di sicurezza** più che di leva manuale |
| **Elemento del metodo** | Il modello Respiratorio-Circolatorio va applicato **per intero** — diaframma come pompa e regolatore pressorio, componente circolatorio-linfatica — con una propria **procedura operativa da 15 minuti** in Parte IV al pari degli altri modelli. |
| **Perché è sbagliato** | Sul carico masticatorio non esiste alcuna leva diaframmatica o circolatorio-linfatica documentata: nessuno studio collega l'escursione diaframmatica o il drenaggio al dolore dei masticatori, all'apertura o all'attività bruxante. Ciò che il dato sostiene su questo modello nel bruxismo è **l'opposto di una tecnica**: il consenso internazionale 2025 (Verhoeff, Lobbezoo, Manfredini et al., *J Oral Rehabil* 2025;52(9):1335-1342, [PMID 40312776](https://pubmed.ncbi.nlm.nih.gov/40312776/)) riconosce che l'attività masticatoria può agire da **fattore protettivo** sulla pervietà delle vie aeree superiori — cioè che il rapporto con il respiro è una **ragione per inviare**, non un bersaglio da trattare. Assegnare 15 minuti di Parte IV a una pompa diaframmatica non misurabile su questa condizione, mentre il vero contenuto del modello è uno screening che decide se il ciclo si apre, sposta il tempo dal punto che protegge il paziente a quello che non produce niente. |
| **Cosa fa la procedura** | Parte 0 §Respiratorio-Circolatorio e Parte IV §Sistema Respiratorio: il modello è **dichiaratamente ridotto a gate di sicurezza (STOP-BANG a ogni ciclo, invio con nota consegnata e verifica alla 2ª seduta) più un coadiuvante da massimo 5 minuti** dentro il blocco C, etichettato *PLAUSIBILE, non dimostrato*. La componente circolatorio-linfatica è omessa in modo esplicito. Nessuna procedura operativa da 15 minuti per questo modello. |
| **Se ratificata** | Introdurre nel metodo che un modello **privo di leva manuale documentata su quella condizione** si dichiara per la funzione che ha davvero — screening, gate di sicurezza o regola di dosaggio — invece di ricevere d'ufficio una procedura operativa in Parte IV. |
| **Coerenza** | Stessa logica di **D-012** (componente circolatorio-linfatica non pertinente alla lombalgia) e **D-032** (leva diaframmatica non pertinente alle artrosi periferiche): si propone di estendere l'ambito di entrambe, o di leggere le tre voci come un unico principio di pertinenza per componente. |

---

### D-073 · La regola "non trattare quasi mai il CP" applicata al massetere nel bruxismo

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Bruxismo (v2 → registrata in v3) |
| **Ambito** | Bruxismo e disturbi temporomandibolari; gemella di **D-030** — ogni condizione in cui il sito sintomatico è anche il tessuto testato dagli studi |
| **Elemento del metodo** | Motore Clinico, Sistema Fasciale/Stecco: *"La regola d'oro: NON trattare quasi mai il CP"* (`fase-0-piramide-del-comando.md`, §2, 6° Sistema Fasciale). |
| **Perché è sbagliato** | Nel bruxismo il Centro di Percezione — massetere e temporale — è esattamente il tessuto su cui esistono gli **unici RCT diretti su bruxisti**: Tütüneken et al., *Cranio* 2026;44(4):708-720 ([PMID 41414918](https://pubmed.ncbi.nlm.nih.gov/41414918/)), n=60, release miofasciale sui masticatori vs. rilasciamento post-isometrico vs. controllo, con riduzione di tono, rigidità e dolore e guadagno di apertura; ed El-Gendy et al., *Front Neurol* 2022;13:1041928 ([PMID 36570455](https://pubmed.ncbi.nlm.nih.gov/36570455/)), n=45, 12 sedute, con miglioramento di sonno percepito, mobilità mandibolare e soglia di dolore. Sull'ingresso a monte — il cervicale alto, cioè il candidato CC — i numeri disponibili (Lam et al., *Arch Rehabil Res Clin Transl* 2023;5(1):100242, [PMID 36968167](https://pubmed.ncbi.nlm.nih.gov/36968167/)) restano **sotto la soglia di rilevanza dichiarata dagli autori** e provengono da pazienti TMD, non da bruxisti. Applicare la regola alla lettera significherebbe rinunciare all'unica componente testata dell'intervento in favore di quella meno supportata. |
| **Cosa fa la procedura** | Parte 0 §"La prova della chiave di volta" e Parte IV §Fasciale-Posturale: la regola è riformulata in **"tratta il massetere *e* cerca il livello a monte"**, con criterio operativo di distinzione (denso al glide ma non riconosciuto = candidato CC; riproduce il dolore familiare = CP) e criterio di ritorno (quadro identico entro 24-48 h nonostante lo scarico = comanda il livello a monte). Il CC/CP resta dichiarato **ragionamento clinico non validato**, mai criterio diagnostico. |
| **Se ratificata** | Qualificare la regola in `fase-0-piramide-del-comando.md` come **"non trattare *solo* il CP"**, con eccezione esplicita per le condizioni in cui il sito sintomatico è il tessuto patologico o il tessuto testato dagli studi disponibili. |
| **Coerenza** | Identica a **D-030** (artrosi), il cui ambito già prevede "potenzialmente ogni condizione in cui il sito sintomatico è esso stesso il tessuto malato": qui si propone l'estensione al caso in cui il sito sintomatico è il **tessuto trattato negli unici RCT diretti**. |

### D-008 · emicrania · La presincope durante inibizione sub-occipitale letta come "accumulo di carico parasimpatico"

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Emicrania (v2 → registrata in v3) |
| **Ambito** | Trasversale — ogni condizione in cui si esegue inibizione sub-occipitale o contatto sostenuto sulla cerniera cranio-cervicale |
| **Elemento del metodo** | La reazione presincopale durante inibizione sub-occipitale prolungata è descritta come **"accumulo di carico parasimpatico"** prodotto dal contatto sulla regione, e quindi come segno che la tecnica "sta lavorando". |
| **Perché è sbagliato** | Non esiste alcuna via documentata per cui la pressione sui sub-occipitali aumenti l'efflusso vagale efferente: il nervo vago non ha afferenze somatiche in quella regione tali da produrre bradicardia riflessa per pressione miofasciale. Il quadro osservato — pallore, sudorazione fredda, nausea, capogiro, bradicardia — è quello classico della **sincope vasovagale (neuromediata)** innescata da dolore, ansia e ortostatismo/decubito prolungato, il meccanismo descritto nelle linee guida ESC sulla sincope (Brignole M et al., *2018 ESC Guidelines for the diagnosis and management of syncope*, Eur Heart J 2018;39:1883-1948, [PMID 29562304](https://pubmed.ncbi.nlm.nih.gov/29562304/)). La differenza non è nominalistica: se è "carico parasimpatico" si continua e si aspetta; se è presincope vasovagale si **interrompe, si mette il paziente supino con le gambe elevate e si sorveglia**, e si previene riducendo dolore e durata del contatto. |
| **Cosa fa la procedura** | Parte II §Controindicazioni e Scheda §1-bis: la reazione è nominata **presincope vasovagale**, con stop-rule dedicata (interrompi, supino, gambe elevate, sorveglianza; nessun recupero o dolore toracico/deficit/sincope → 112) e distinta esplicitamente dalla stop-rule vascolare, che ha condotta opposta. Il consenso scritto la elenca fra i rischi. |
| **Se ratificata** | Correggere nei documenti di metodo la descrizione degli effetti dell'inibizione sub-occipitale: rimuovere la "leva parasimpatica" come meccanismo, mantenere la sorveglianza come evento avverso benigno ma reale. |
| **Coerenza** | Stessa logica di **D-002** (direzione della leva vagale) e **D-021** (lavoro sub-occipitale come "accesso vagale"): la regione non è una manopola sull'autonomico. |

---

### D-009 · emicrania · La "sommazione periferica" come entità fisiologica

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Emicrania (v2 → registrata in v3) |
| **Ambito** | Trasversale — ogni condizione in cui si spiega l'effetto del lavoro manuale sul dolore persistente |
| **Elemento del metodo** | L'effetto atteso del trattamento manuale a medio termine è descritto come **riduzione della "sommazione periferica"** degli input nocicettivi. |
| **Perché è sbagliato** | La **sommazione temporale** è un fenomeno di *wind-up* dei neuroni di secondo ordine del corno dorsale, cioè **centrale** per definizione: è la misura psicofisica standard della facilitazione centrale nei protocolli QST (Arendt-Nielsen L, Yarnitsky D, *Experimental and clinical applications of quantitative sensory testing applied to skin, muscles and viscera*, J Pain 2009;10:556-572, [PMID 19380256](https://pubmed.ncbi.nlm.nih.gov/19380256/)). "Sommazione periferica" non nomina nulla che esista in periferia, e usarla fa passare per meccanismo misurato ciò che è un'inferenza. |
| **Cosa fa la procedura** | Parte I §Tabella e Parte III: l'effetto a 3-6 sedute è formulato come **"possibile riduzione dell'input nocicettivo periferico che alimenta la convergenza"** sui neuroni di secondo ordine, e si afferma **solo** se il FRT d'ingresso della seduta successiva è migliorato rispetto alla baseline della precedente (regola di carry-over). |
| **Se ratificata** | Eliminare "sommazione periferica" dal lessico dei documenti di metodo; usare "riduzione dell'input nocicettivo periferico" per l'anello che si tocca e riservare "sommazione temporale" al fenomeno centrale, mai attribuito alle proprie mani. |
| **Coerenza** | Stessa logica di **D-006**: si dichiara l'anello che si tocca, non quello che si spera di muovere. |

---

### D-010 · emicrania · Il modello Neurologico applicato come modello autonomico (vago, frenico, riflesso viscero-somatico)

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Emicrania (v2 → registrata in v3) |
| **Ambito** | Emicrania e cefalee primarie; **gemella di D-008 · ernia**, di cui condivide il principio |
| **Elemento del metodo** | Il modello Neurologico si applica d'ufficio nella sua declinazione **autonomica** — vago, frenico, riflessi viscero-somatici, facilitazione segmentale — in ogni condizione. |
| **Perché è sbagliato** | Nell'emicrania la neurologia che decide il caso non è autonomica: è la **convergenza trigemino-cervicale** sui neuroni di secondo ordine del corno dorsale cervicale alto (Bartsch T, Goadsby PJ, *Stimulation of the greater occipital nerve induces increased central excitability of dural afferent input*, Brain 2002;125:1496-1509, [PMID 12077000](https://pubmed.ncbi.nlm.nih.gov/12077000/)) e la **sensibilizzazione centrale** letta clinicamente come allodinia cutanea (Burstein R et al., Ann Neurol 2000;47:614-624, [PMID 10805332](https://pubmed.ncbi.nlm.nih.gov/10805332/)). Riempire il modello di contenuto autonomico significherebbe scrivere il modello meno pertinente e omettere quello che governa la dose: il triage del dolore fra nocicettivo, nociplastico e neuropatico. |
| **Cosa fa la procedura** | Parte 0 §Modello Neurologico: il modello è calato sul **complesso trigemino-cervicale**, sull'**allodinia (ASC-12)** e sul **triage del dolore che decide la dose**, senza sezione autonomica. Dichiara inoltre di non avere arsenale manuale proprio: le tecniche restano biomeccaniche e miofasciali con razionale neurologico. |
| **Se ratificata** | Come per **D-008 · ernia**: stabilire nel metodo che il modello Neurologico si cala sulla **neurologia della condizione** — autonomica, periferico-neurale o di elaborazione centrale — e non si applica d'ufficio nella sola versione autonomica. |
| **Coerenza** | Identica a **D-008 · ernia**; parallela a **D-012** e **D-072** sul principio di pertinenza per componente. |

---

### D-011 · emicrania · L'etichetta CC/CP e la regola "non trattare il CP" applicate all'emicrania

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Emicrania (v2 → registrata in v3) |
| **Ambito** | **Estensione di D-011 · lombalgia**, il cui ambito è già "ogni condizione in cui si usa il linguaggio CC/CP di Stecco" |
| **Elemento del metodo** | Motore Clinico, Sistema Fasciale: il bersaglio si nomina **Centro di Coordinazione**, si conferma con la palpazione della **densificazione**, e vale la regola *"non trattare quasi mai il CP"*. |
| **Perché è sbagliato** | Due ragioni, e la seconda è interna. **(1)** La palpazione di texture non è riproducibile fra operatori (Seffinger MA et al., *Reliability of spinal palpation for diagnosis of back and neck pain*, Spine 2004;29:E413-E425, [PMID 15454722](https://pubmed.ncbi.nlm.nih.gov/15454722/)), ed è la stessa ragione per cui questa procedura ha già sostituito "cedimento del tono" con un endpoint numerico. **(2)** Una procedura che pretende osservabili riproducibili non può poi definire il proprio bersaglio con un costrutto palpatorio: è una contraddizione interna prima che un problema di evidenza. Sul secondo punto, nell'emicrania il sito sintomatico — sub-occipitali, temporale, masticatori — è anche il tessuto su cui esistono gli unici dati diretti di terapia manuale (Falsiroli Maistrello 2018, trattamento dei trigger point): "non trattare il CP" imporrebbe di rinunciare all'unica componente misurata. |
| **Cosa fa la procedura** | L'etichetta CC/CP è **rimossa**; il contenuto operativo resta (*non inseguire il punto che duole, cerca a monte lungo la catena*) ma il bersaglio si chiama **"regione candidata a monte, confermata dai tre marker"**, e la palpazione è dichiarata linguaggio euristico per *nominare*, mai criterio per decidere. Il sito sintomatico si tratta, con dose e stop-rule dichiarate. |
| **Se ratificata** | Estendere l'ambito di **D-011 · lombalgia** e **D-073 · bruxismo**: conferma funzionale al posto di quella palpatoria, e regola riformulata in "non trattare *solo* il CP". |
| **Coerenza** | Coerente con **D-011 · lombalgia**, **D-007 · lombalgia**, **D-030** e **D-073**. |

---

### D-012 · emicrania · L'anello viscerale collocato d'ufficio nel modello Biomeccanico

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Emicrania (v2 → registrata in v3) |
| **Ambito** | Emicrania in primis; da valutare per ogni condizione priva di meccanica d'organo. **Estensione proposta il 2026-08-18 all'ernia del disco lombare** (v3): nessuna meccanica d'organo pertinente al dolore radicolare da ernia — il limite di pertinenza è dichiarato dentro il modello **Biomeccanico-Strutturale** e non esiste sezione viscerale in Parte IV. **Contro-esempio registrato il 2026-08-18 · sciatalgia (v3):** qui la meccanica d'organo **è** pertinente (rene e uretere sullo psoas, colon, pelvi, aderenze della fascia iliaca), quindi la componente viscerale **resta dentro il Biomeccanico-Strutturale** con nota di scope, segnali propri e lavoro manuale collocato nel Reset Fasciale-Posturale — **senza sezione autonoma in Parte IV**. Le due applicazioni sono la stessa regola: la componente si dichiara dentro il modello che la governa, con o senza pertinenza, e non diventa mai un modello a sé. |
| **Elemento del metodo** | La componente viscerale è un capitolo del modello **Biomeccanico-Strutturale** (mobilità e motilità d'organo, tensioni legamentose, sospensioni) e riceve una sezione propria in Parte IV. |
| **Perché è sbagliato** | Nell'emicrania non esiste meccanica d'organo da trattare: nessuno studio collega la mobilità viscerale alla frequenza, all'intensità o all'impatto dell'emicrania. Ciò che il dato sostiene è a monte del trattamento e riguarda il **terreno**: la gastroparesi emicranica e la nausea rallentano lo svuotamento gastrico e **condizionano l'assorbimento del sintomatico** (Aurora SK et al., *Gastric stasis in migraine: more than just a paroxysmal abnormality during a migraine attack*, Headache 2006;46:57-63, [PMID 16412152](https://pubmed.ncbi.nlm.nih.gov/16412152/)) — cioè è un'informazione da **annotare e riferire al medico**, non un bersaglio manuale. Assegnare una sezione di tecniche viscerali significherebbe importare un claim senza fonte in un documento che dichiara l'evidenza modello per modello. |
| **Cosa fa la procedura** | Parte 0 §Biomeccanico-Strutturale, "Limite di pertinenza dichiarato": si dichiara l'assenza di meccanica d'organo e si colloca l'anello viscerale nel modello **Metabolico-Energetico**, ridotto a segnali da annotare e segnalare (lateralità costante, aggancio ai pasti, nausea sproporzionata). Nessuna sezione viscerale autonoma in Parte IV. |
| **Se ratificata** | Stabilire nel metodo che la componente viscerale si applica **dove esiste meccanica d'organo pertinente**, e che altrove si dichiara come informazione di terreno da riferire, dentro il modello che la governa davvero. |
| **Coerenza** | Stessa logica di **D-012 · lombalgia** e **D-072 · bruxismo**: pertinenza per componente, con il limite dichiarato nel testo. |

---

### D-061 · sciatalgia · Il modello Metabolico-Energetico senza sezione operativa in Parte IV

| | |
|---|---|
| **Stato** | `PROPOSTA` |
| **Aperta il** | 2026-08-18 |
| **Condizione di emersione** | Sciatalgia (v2 → registrata in v3) |
| **Ambito** | Sciatalgia in primis; da valutare per ogni condizione in cui il Metabolico-Energetico non abbia una leva manuale documentata (dolore radicolare, ernia del disco, cervicobrachialgia) |
| **Elemento del metodo** | Ogni modello dei cinque riceve in Parte IV un Sistema corrispondente con **Procedura Operativa (15 min)** e tabella di sintesi. |
| **Perché è sbagliato** | Sulla sciatalgia la componente metabolica è **fattore di vulnerabilità e sospetto diagnostico**, non bersaglio manuale. Il dato disponibile è di **incidenza** — Shiri R, Falah-Hassani K, *The effect of smoking on the risk of sciatica: a meta-analysis*, Am J Med 2016;129(1):64-73.e20, [PMID 26403480](https://pubmed.ncbi.nlm.nih.gov/26403480/) (OR aggiustato 1,46; IC 95% 1,30-1,64 nel fumatore attivo) — e riguarda il rischio di **sviluppare** sciatalgia, non l'effetto di un gesto manuale su un episodio in corso. Nessuno studio ha testato una tecnica manuale sulla componente metabolica del dolore radicolare. Assegnare d'ufficio cinque passi operativi significherebbe inventare una procedura senza fonte in un documento che dichiara l'evidenza modello per modello, e mascherare la vera funzione clinica del modello: **counseling e rinvio**, con la radicoloplessopatia diabetica come sospetto da non mancare. |
| **Cosa fa la procedura** | Il Metabolico-Energetico resta **in vetrina in Parte 0** con cosa governa, attori, segnali di dominanza ed evidenza dichiarata; in Parte III è una riga del montaggio (**counseling 5' + rinvio, la seduta si monta sul secondo dominante**); in Parte IV **non ha sezione operativa**, e la mappa modello → sezione lo dichiara esplicitamente con il motivo. |
| **Se ratificata** | Stabilire nel metodo il principio di **pertinenza per componente** anche in senso forte: un modello privo di leva manuale documentata su quella condizione si dichiara **per la funzione che ha davvero** (counseling, rinvio, sorveglianza) invece di ricevere d'ufficio una Procedura Operativa, purché il motivo sia scritto nel testo e la mappa di Parte IV lo riporti. |
| **Coerenza** | Stessa logica di **D-032 · artrosi**, **D-072 · bruxismo**, **D-012 · lombalgia** e **D-012 · emicrania**, ma applicata per la prima volta al **Metabolico-Energetico**: nessuna di quelle voci ha ambito sulla sciatalgia né su questo modello. Le cinque si possono leggere come un unico principio generale ratificabile in blocco. |

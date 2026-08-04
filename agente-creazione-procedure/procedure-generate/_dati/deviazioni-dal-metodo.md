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

---
name: broll-modelli-higgsfield
description: Sceglie quali modelli di intelligenza artificiale usare su Higgsfield per generare le immagini e i video di un video pubblicitario, cercando il massimo risultato al costo minore, e verifica che gli endpoint dichiarati esistano ancora. Attiva questa skill prima di ogni generazione di B-roll, quando si deve decidere fra modelli immagine o video, quando il catalogo dei modelli ha superato la scadenza, o quando si vuole sapere quanto costerà un piano prima di spendere i crediti.
---

# Quali modelli usare, e quanto costano

Questa skill decide **con cosa** si genera. È la prima fase del workflow perché è
l'unica che può far risparmiare un ordine di grandezza: sui video il modello sbagliato
costa dieci volte l'immagine sbagliata, e si scopre solo dopo averlo pagato.

Il catalogo vive in `broll-generati/_dati/modelli-higgsfield.json`. **Questa skill non
ha modelli cablati dentro:** se un nome di modello compare in queste istruzioni è come
esempio, non come default. Il default sta nel file.

---

## VINCOLO ASSOLUTO

**Nessun credito si spende prima di una stima.**

`scripts/higgsfield.py stima` interroga l'endpoint `/estimate` con gli stessi parametri
della generazione vera e restituisce crediti e dollari **per il tuo account**. È il
numero che verrà addebitato, non un'approssimazione. Un piano da venti b-roll che
sembra ragionevole sulla carta può essere trecento crediti, e quella conversazione va
fatta prima, non dopo.

---

## L'ordine delle quattro domande

### 1. Carlos ha indicato dei modelli al lancio?

Se sì, **si usano quelli.** Non si discute la scelta, si verifica solo che esistano nel
catalogo, che siano `disponibile_su_api: true` e che supportino il formato richiesto. Se
uno dei tre controlli fallisce, si dice **quale** e si propone il ripiego — non si
sostituisce in silenzio.

### 2. Il catalogo è scaduto?

Guarda `aggiornato_il` e `scadenza_giorni`. Se sono passati più giorni della scadenza,
lancia:

```bash
python3 scripts/verifica_modelli.py
```

Lo script apre la documentazione viva di Higgsfield, verifica che ogni endpoint
dichiarato esista ancora e ti elenca le famiglie di modelli presenti nel catalogo
Higgsfield e assenti dal nostro file. **Referta, non aggiorna.** Se trovi qualcosa che
vale la pena cambiare — un modello nuovo più adatto, un endpoint sparito, un prezzo
diverso — lo proponi a Carlos con il motivo, e la modifica al file la decide lui.

Il catalogo autorevole sta in `console.higgsfield.ai`, dietro account: l'assenza di un
modello dalla documentazione pubblica **non prova** che non esista. Dove non puoi
verificare, dillo invece di concludere.

### 3. Che tipo di b-roll deve generare?

| Serve | Cosa guardare nel catalogo |
|---|---|
| Persone, con lo stesso volto su più scene | un modello che accetti `riferimento_personaggio` nella sua `mappa` |
| Persone, scena singola, resa da cinema | un modello immagine con `punti_di_forza` sulla luce e sull'atmosfera |
| Infografiche anatomiche con gerarchia precisa | un modello che segue prompt lunghi e strutturati: è scritto nei `punti_di_forza` |
| Oggetto reale, prodotto vero, scorcio fotografico | un modello con `immagini_riferimento` nella `mappa` |
| Movimento umano credibile | il predefinito video, e c'è un motivo scritto nel campo `perche_non_veo` |

### 4. Si può spendere meno senza perdere?

Tre leve, in ordine di resa:

1. **Il giro di prova.** Genera l'intero piano con `--solo-immagini`, guarda le scene,
   correggi i prompt che non reggono, **poi** paga i video. Un'immagine costa una
   frazione di un video: validare a monte è la singola decisione che risparmia di più.
2. **La variante economica dello stesso modello.** Le famiglie hanno spesso un livello
   turbo o standard accanto al pro. Su un b-roll da cinque secondi con movimento
   trattenuto la differenza spesso non si vede — ma va guardata una volta, non assunta.
3. **La durata.** I video si pagano a secondo. Un b-roll di cinque secondi ben montato
   batte uno di dieci che resta in aria: la durata giusta è quella che la regia ha
   scritto nel piano, non il massimo consentito.

Quello che **non** è una leva: abbassare la risoluzione delle immagini. L'immagine è la
sorgente del video, e un difetto lì si moltiplica nel movimento.

---

## Le cose dell'API che cambiano le decisioni

Il contratto completo e verificato sta in `references/api-higgsfield.md`. Le tre che
contano qui:

- **Le POST di generazione non hanno idempotenza.** Dopo un timeout ambiguo, ripetere la
  richiesta significa rischiare di pagare due volte. Il client scrive il `request_id` su
  disco prima di iniziare il polling, e una ripresa interroga quello. **Non aggirare mai
  questo meccanismo lanciando una generazione a mano su un id già in volo.**
- **I piani illimitati del sito non valgono sull'API.** Le generazioni comprese
  nell'abbonamento si applicano solo a `higgsfield.ai`. Ogni chiamata API consuma
  crediti a parte, e i crediti scadono dopo un anno.
- **L'output resta sul CDN almeno sette giorni**, poi può sparire. Il client scarica
  sempre, e la cartella `outputs/` è l'archivio vero.

---

## Output

Restituisci **solo** questo oggetto.

```json
{
  "immagine": "chiave del modello scelto",
  "video": "chiave del modello scelto",
  "perche": "due righe: cosa ha deciso la scelta per questo video specifico",
  "catalogo_scaduto": false,
  "giorni_dall_aggiornamento": 0,
  "verifica_endpoint": "esito di verifica_modelli.py, oppure 'non eseguita: catalogo nei termini'",
  "proposte_di_aggiornamento": [
    "modello nuovo o endpoint sparito, con il motivo. Vuoto se non c'è niente da proporre."
  ],
  "avvertenze": [
    "quello che Carlos deve sapere prima di autorizzare la spesa"
  ]
}
```

Le chiavi devono esistere in `modelli-higgsfield.json`. Se hai dovuto ripiegare su un
modello diverso da quello chiesto, **la prima riga di `avvertenze` dice quale e perché.**
Un ripiego silenzioso produce un video girato con un modello che nessuno ha scelto.

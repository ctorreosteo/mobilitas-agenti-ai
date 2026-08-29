# Il calibro della durata

Come si passa da "voglio una VSL da X minuti" a una scaletta che regge. **L'utente sceglie i minuti; la struttura si ricalibra, non si accorcia uniformemente.**

---

# 1. La costante

**150 parole al minuto.** È il ritmo di un testo scritto per essere ascoltato: più lento del parlato spontaneo (170-200), perché ogni parola deve arrivare la prima volta.

| Situazione | Parole/minuto |
|---|---|
| VSL con dimostrazioni o grafici a schermo | 130 |
| VSL standard, voce narrante | **150** |
| VSL a ritmo alto, pubblico giovane, short-form | 165 |
| Webinar dal vivo, con pause e interazione | 130 |

Lo script pratico: `python3 scripts/vsl-budget.py [minuti] [--freddo|--caldo|--webinar] [--wpm N]`

---

# 2. La regola che decide la durata

**Non la scegli tu: la sceglie il rapporto tra il claim e la prova.**

> Più grande è la promessa → più prova serve → più minuti servono.

Da qui le due diagnosi che vanno fatte *prima* di accettare la durata richiesta:

- **Claim grande + durata corta** = incredibile. Si accorcia la promessa o si allunga il video.
- **Claim piccolo + durata lunga** = noioso. La gente esce prima del pitch perché ha già capito.

E la variabile che pesa quanto il claim: **la consapevolezza del pubblico.** Più è freddo, più minuti servono per portarlo dove il caldo è già.

| Consapevolezza | Durata minima realistica |
|---|---|
| 5 — most aware | 60 secondi |
| 4 — product aware | 3 minuti |
| 3 — solution aware | 8 minuti |
| 2 — problem aware | 15 minuti |
| 1 — unaware | 25 minuti |

**Sotto questi minimi la VSL non è "snella": è muta.** Se l'utente chiede meno, dillo, e proponi le due strade — restringere il pubblico (retargeting, lista calda) o allungare il video.

---

# 3. Le cinque taglie

## 60-90 secondi — creatività per ads

**150-225 parole.** Non è una VSL: è un annuncio con struttura di VSL. Solo sei blocchi, compressi.

```
Cold open (12%) → Promessa (10%) → Mecc. problema (18%) → Mecc. soluzione (20%)
→ Prova (12%) → Prodotto+offerta (14%) → Garanzia (6%) → CTA (8%)
```

**Regola:** un solo meccanismo raccontato bene batte due accennati. La prova è **un elemento solo**, il più concreto che hai. Nessuna storia, nessuno stack.

**Chiusura asimmetrica:** l'annuncio chiude abbastanza da avere senso, ma il pagamento completo sta nella destinazione. Il clic è la chiusura.

## 3-5 minuti — lead gen, low ticket, retargeting

**450-750 parole.** Funziona su pubblico 3-4. Si aggiungono qualificazione e bullet; la storia resta un accenno di due frasi, non un blocco.

**L'errore tipico di questa taglia:** provare a metterci tutto. Con 600 parole, tre blocchi fatti bene battono dieci fatti a metà.

## 8-12 minuti — mid ticket, pubblico tiepido

**1.200-1.800 parole.** La prima taglia in cui la struttura completa ha senso. Compaiono storia vera (12-13%), stack, e la prima gestione delle obiezioni.

**Il punto critico:** il reversal a 4-6 minuti. Se arriva più tardi non c'è spazio per costruirci sopra.

## 20-30 minuti — high ticket, traffico freddo

**3.000-4.500 parole.** La taglia classica del direct response video. Tutti e 17 i blocchi, prova distribuita in almeno tre punti, 3-4 CTA.

**Qui il meccanismo del problema vale il 16-18%** — è il blocco più lungo dell'intera VSL, e deve esserlo.

## 45-90 minuti — webinar e offerte complesse

**6.750-13.500 parole.** Cambia la struttura interna: il blocco 8 si espande nei **tre segreti** (Brunson, Fladlien), ognuno dei quali smonta una credenza.

```
Segreto 1 → rompe la credenza sul VEICOLO   ("questo tipo di soluzione non funziona")
Segreto 2 → rompe la credenza INTERNA        ("non funzionerebbe per me")
Segreto 3 → rompe la credenza ESTERNA        ("non ho le condizioni: tempo, soldi, supporto")
```

Ogni segreto ha la sua micro-struttura: promessa → storia → meccanismo → prova → chiusura parziale. E ognuno finisce con una **chiusura di prova** (*trial close*): una domanda a cui il pubblico risponde sì mentalmente.

In questa taglia CTA e obiezioni salgono al 13% combinato: nel webinar la vendita è quasi tutta nella coda.

---

# 4. Cosa cade, e in che ordine

Quando si accorcia **non si riduce tutto in proporzione**. Si tolgono blocchi interi, in quest'ordine:

1. **Chiusure successive** (blocco 17)
2. **Obiezioni**
3. **Profondità della prova** — si tiene l'elemento più forte, si tolgono gli altri
4. **Storia** — da blocco a due frasi, poi via
5. **Bullet** — da 9 a 5, poi a 3
6. **Qualificazione**
7. **Anticipo di prova** — si fonde con la promessa

**Non cadono mai, a nessuna durata:**

- Cold open
- Meccanismo del problema
- Meccanismo della soluzione
- Offerta
- Inversione del rischio
- CTA

Sono i sei blocchi incomprimibili. Sotto i 90 secondi restano solo questi.

**Il contrario — cosa si aggiunge allungando**, in ordine: profondità della prova → storia → obiezioni → chiusure multiple → sotto-meccanismi → casi studio estesi.

**Regola:** allungare non vuol dire dire le stesse cose più lentamente. Vuol dire **aggiungere prova**. Una VSL da 30 minuti che dice quello che ne diceva una da 10 è una VSL da 10 minuti scritta male.

---

# 5. Allocazioni per modalità

Percentuali sulla durata totale. Sono quelle implementate nello script, con l'autoverifica che il reversal cada tra il 40% e il 55%.

| Blocco | Standard | Freddo | Caldo | Webinar |
|---|---|---|---|---|
| 1 Cold open | 3 | 3 | 4 | 2 |
| 2 Grande promessa | 3 | 3 | 5 | 3 |
| 3 Qualificazione | 3 | 2 | 2 | 3 |
| 4 Anticipo di prova | 3 | 3 | 4 | 2 |
| 5 Storia | 13 | 16 | 8 | 11 |
| 6 **Mecc. del problema** | **16** | **18** | **17** | **19** |
| 7 Reversal | 4 | 4 | 3 | 3 |
| 8 **Mecc. della soluzione** | **14** | **16** | **10** | **11** |
| 9 Prova | 10 | 12 | 10 | 10 |
| 10 Rivelazione prodotto | 4 | 3 | 6 | 3 |
| 11 Bullet | 7 | 6 | 9 | 5 |
| 12 Stack | 5 | 4 | 7 | 7 |
| 13 Ancoraggio e prezzo | 4 | 3 | 5 | 4 |
| 14 Inversione del rischio | 4 | 3 | 4 | 3 |
| 15 Urgenza | 2 | 1 | 2 | 1 |
| 16 CTA | 3 | 2 | 3 | 7 |
| 17 Obiezioni e chiusure | 2 | 1 | 1 | 6 |

**Come leggerle.** I due meccanismi valgono insieme il **30-34%** in ogni modalità: è la spina dorsale, e non si comprime. Su pubblico freddo salgono e la storia si allunga; su pubblico caldo scendono e crescono bullet, stack e prezzo.

**Correzione per sofisticazione.** Se il mercato è a stadio 4-5 (anche i meccanismi sono inflazionati), sposta 4-5 punti dalla storia ai due meccanismi: serve elaborare il meccanismo, non solo nominarlo.

---

# 6. Il budget è un vincolo

Un blocco che sfora ruba minuti a un altro, e **quasi sempre li ruba alla prova** — perché la prova è l'unica cosa che si può sempre "accorciare un po'". È esattamente il taglio che non va fatto: senza prova, la promessa resta scoperta e il prezzo arriva su un pubblico che non ci crede.

**Controllo prima di scrivere il copy:** somma le parole della scaletta. Se supera il budget del 10%, la scaletta è sbagliata, non il budget.

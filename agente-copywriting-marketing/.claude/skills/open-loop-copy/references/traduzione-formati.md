# Traduzione formato per formato

Come si applica l'architettura dei loop ai formati reali. Ogni formato ha **punti di ancoraggio** diversi (dove il loop può essere aperto e chiuso) e **punti di fuga** diversi (dove il lettore esce).

## Corrispondenze di base

| Narrativa seriale | Copy |
|---|---|
| Episodio | Singolo contenuto (email, video, ad, post) |
| Stagione | Sequenza / campagna |
| Serie | Relazione complessiva col pubblico |
| Cold open | Oggetto + prima riga / primi 4 secondi |
| Act-out | Ogni punto di possibile uscita interna |
| Cliffhanger di episodio | Chiusura del contenuto |
| Cliffhanger di stagione | Chiusura della sequenza |
| Tag / post-credit | **P.S.** |
| Previously on | Riga di rientro in apertura |
| A-story | Tema dello step |
| B-story | Filo su 3-4 step |
| C-story | Arco della sequenza |
| Season finale | Step di offerta / richiesta |
| Rinnovo | Residuo finale → campagna successiva |

---

# 1. Sequenza email

Il formato per cui questa skill è più adatta: gap temporali reali tra un contenuto e l'altro, quindi serialità vera.

## Punti di ancoraggio

| Punto | Funzione | Nota |
|---|---|---|
| **Oggetto** | Cold open | Deve aprire, non riassumere. Non deve mai promettere ciò che il corpo non paga |
| **Preheader** | Estensione del cold open | Non ripete l'oggetto: lo complica |
| **Prima riga** | Ingresso in medias res | Zero preamboli, zero saluti generici |
| **Riga di rientro** | Previously on | Solo dal secondo step in poi, max 2 righe |
| **Corpo** | A-story + B-story | Collegamenti in *ma*/*quindi* |
| **Ultima riga del corpo** | Cliffhanger di episodio | Tagliata una battuta prima della fine naturale |
| **P.S.** | Tag | Pianta il loop dello step successivo. **Non vende** |

## Struttura standard di uno step intermedio

```
[OGGETTO — apre un loop o paga quello aperto ieri, mai neutro]
[RIENTRO — 1-2 righe che riprendono la frase-chiave precedente, letterale]
[PAGAMENTO — chiude il debito aperto, in modo completo]
[CONSEGUENZA — "il che significa che..."]
[RESIDUO — la conseguenza contiene un problema nuovo]
[CLIFFHANGER — taglio una battuta prima]
[P.S. — dangling cause per lo step successivo]
```

## Regole specifiche

- **L'oggetto non è un titolo, è un act-out.** Deve funzionare fuori contesto e dentro contesto insieme.
- **Il P.S. viene letto anche da chi salta il corpo.** Statisticamente è la seconda zona più letta. Sprecarlo per ripetere la CTA è l'errore più diffuso del formato.
- **Un solo loop di tipo 9 (debito dichiarato) per sequenza.** Tutti gli altri devono generarsi dal contenuto.
- **La distanza tra invii detta l'ampiezza.** Vedi tabella emivita in SKILL.md. Se la sequenza ha invii irregolari, dimensiona ogni gancio sul suo gap specifico, non su una media.
- **Ogni email deve valere da sola.** Chi apre solo la quarta deve ricevere qualcosa di completo.

## Errore strutturale tipico di questo formato

La sequenza costruita per argomenti: *"Mail 1: il problema. Mail 2: le cause. Mail 3: la soluzione. Mail 4: l'offerta."* È una lista. Ogni mail chiude tutto quello che ha aperto e non lascia niente. L'open rate crolla dalla seconda perché non c'è motivo di tornare.

**Correzione:** la mail 1 apre l'arco e ne chiude una parte lasciando residuo; la mail 2 paga il residuo e apre una B-story; la mail 3 paga la B-story ma il pagamento produce il problema che rende l'offerta necessaria; la mail 4 chiude l'arco e lascia il residuo per la campagna successiva.

---

# 2. Funnel lungo di nurturing (settimane o mesi)

Il gap è troppo grande per un cliffhanger classico. Cambia il tipo di loop dominante.

**Loop che reggono gap lunghi:**
- **Tipo 6 (ironia drammatica)** — funziona meglio degli altri perché non richiede memoria di un dettaglio, richiede memoria di uno *stato* (io so, lui non sa).
- **Tipo 3 (identità)** — il lettore segue una persona, non un'informazione. La memoria di una persona è più resistente.
- **Tipo 5 (relazionale)** — un caso seguito nel tempo.

**Loop che NON reggono gap lunghi:** tipo 1 (gap informativo puro). Una domanda fattuale lasciata aperta per tre settimane non viene ricordata: viene sostituita da altre domande.

**Meccanica del gap lungo:**
1. Il rientro è obbligatorio e più esteso (3-4 righe, non 2).
2. Prima di pagare, **ricontestualizza**: aggiungi un elemento nuovo che rende la domanda vecchia più urgente. Poi chiudi.
3. Usa i **runner** con più densità: nel lungo periodo l'appartenenza sostiene più della tensione.
4. Struttura a **stagioni**: 5-7 step con arco proprio, chiusura netta, residuo verso la stagione successiva. Meglio tre archi chiusi che un arco unico da venti step.

---

# 3. Sequenza di annunci (ads)

Vincolo dominante: **non controlli l'ordine di visione** e ogni annuncio può essere il primo.

**Conseguenza:** i loop tra-annunci non funzionano come nelle email. Non puoi contare su una sequenza.

**Cosa funziona invece:**
- **Loop interni al singolo annuncio**, aperti nei primi secondi e chiusi prima della CTA. Il loop lavora sulla retention del singolo asset.
- **Loop di universo**: elementi ricorrenti (persone, luoghi, formule) che al secondo o terzo contatto producono riconoscimento. Non è tensione, è familiarità — ed è ciò che si può realmente costruire su una distribuzione non ordinata.
- **Loop tra fasi**: TOFU apre una categoria di domanda, BOFU la paga. Qui la sequenzialità è probabilistica ma il retargeting la rende sufficientemente affidabile.
- **Loop di continuazione asimmetrica**: l'annuncio chiude abbastanza da avere senso, ma il pagamento completo sta nella destinazione (landing, video lungo, form). Il clic diventa la chiusura.

**Da evitare in assoluto:** annunci numerati (*"parte 2 di 4"*). Chi vede la parte 3 per prima esce.

---

# 4. VSL / video lungo

Il formato con la curva di abbandono più ripida e i punti di fuga più densi.

**Punti di ancoraggio:**
- **Secondo 0-4**: cold open. In medias res o anomalia. Nessuna presentazione.
- **Cornice a flash-forward**: se il video è lungo (>10 min), aprire dall'esito e tornare indietro è la struttura più solida — dà al lettore una destinazione per cui restare.
- **Act-out ogni 90-120 secondi**: prima di ogni cambio di sezione, una riga che apre.
- **Reversal al centro**: il punto in cui il quadro si ribalta va posizionato tra il 40% e il 55%, non alla fine. Nei dati di retention è tipicamente lì che si trova il picco di re-engagement.
- **False close prima dell'offerta**: sembra concluso, poi si riapre. Recupera parte di chi stava uscendo.
- **Tag dopo la CTA**: l'ultima cosa detta dopo che il video sembra finito.

**Regola di dosaggio:** in video lungo, i loop di tipo 2 (suspense di esito) e 7 (orologio) reggono meglio dei tipo 1, perché il tipo 1 chiede pazienza mentre il tipo 2 e 7 danno una direzione.

---

# 5. Contenuto serializzato organico (canale, newsletter, profilo)

Qui non c'è un arco chiuso: la relazione è indefinita. Cambia l'obiettivo del loop — non condurre a una conversione, ma **rendere il ritorno un'abitudine**.

- **C-story permanente**: un arco lungo che non si chiude mai del tutto (un progetto in corso, un obiettivo dichiarato, una domanda di fondo). È il motivo per cui il pubblico segue *te* e non i *contenuti*.
- **A-story sempre autoconclusiva**: ogni pezzo deve pagare da solo. Su organico, il pubblico è meno tollerante di quanto sia una lista email.
- **Runner densi**: formule, rubriche, elementi fissi.
- **Planting su orizzonte lungo**: elementi piantati mesi prima e pagati dopo. È il segnale più forte di serietà strutturale che si possa dare a un pubblico.
- **Previously on leggero**: sul singolo pezzo, una riga che riconosce chi c'era già senza escludere chi arriva ora.

---

# 6. Sequenza di recupero (chi si è raffreddato)

Il loop è già decaduto. Non si riparte dal punto in cui si era interrotto.

**Procedura:**
1. **Non fingere continuità.** Il lettore sa che è passato del tempo. Fingere che non sia successo produce estraneità.
2. **Ricontestualizza il loop vecchio** con un elemento nuovo che ne cambia l'urgenza. Il loop vecchio ricontestualizzato è più forte di un loop nuovo, perché ha già una traccia di memoria.
3. **Paga subito e in modo sovradimensionato.** Chi rientra ha bisogno di una prova immediata che restare conviene. Qui, e solo qui, si paga più di quanto si era promesso.
4. **Riparti con un arco corto** (3-4 step), non con uno lungo. La fiducia va ricostruita su un ciclo breve completato.

---

# 7. Tabella di scelta rapida

| Se il formato ha... | Loop dominante | Tecniche principali |
|---|---|---|
| Gap di 24-48h e ordine garantito | Tipo 1, 8, 10 | Cliffhanger, dangling cause, tag/P.S. |
| Gap di settimane | Tipo 3, 5, 6 | Ironia drammatica, runner, ricontestualizzazione |
| Ordine non garantito | Loop interni + universo | Cold open forte, elementi ricorrenti |
| Consumo continuo (video lungo) | Tipo 2, 7 | In medias res, act-out ritmati, reversal centrale, false close |
| Relazione indefinita | C-story permanente | Planting a lungo raggio, runner, A-story autoconclusiva |
| Pubblico raffreddato | Loop vecchio ricontestualizzato | Ricontestualizzazione + pagamento sovradimensionato |

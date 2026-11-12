# Scelte approvate da Riccardo

Il direttore artistico resta **cieco** (Riccardo, 04/11/2026): non riceve questo elenco e giudica solo quello che vede. Questo file serve all'agente, dopo il voto, per dividere le osservazioni del direttore in due gruppi:

- **difetti di esecuzione**: cose che il modello o i dati fanno male, cioè fotogrammi sporchi, testo sopra il B-roll, doppie immagini, lettere tagliate, cifre provvisorie. Si correggono, con un giro 2 o una variante nuova, e si riportano;
- **scelte già approvate**: decisioni che Riccardo ha visto e approvato. Non si cambiano da soli. Nel report si scrivono a parte come «osservazione del direttore su una scelta approvata», e se il direttore insiste si chiede a Riccardo.

Un voto sotto 7 dato solo per scelte approvate non chiede un giro 2: si riporta a Riccardo così com'è, con la divisione.

## Regole generali (CLAUDE.md)

- «Tutto schermo» solo quando il contenuto riempie lo schermo; i contenuti piccoli vanno in «finestra».
- Il fondo vuoto sotto y 1248 è la zona dell'interfaccia Meta: nessun testo lì. Non è un difetto.
- Niente fascia trasparente per i sottotitoli dentro un «tutto schermo».
- Le grafiche si agganciano alla voce, non ai sottotitoli: un sottotitolo in anticipo o in ritardo resta com'è.
- Solo parole dette. Le riduzioni fatte con parole tutte dette vanno bene, per esempio «non solo il collo», «esercizi a casa», «girare la testa / senza pensarci».
- Il logo è quello ufficiale, MOBILITAS con la T stilizzata, e non si ridisegna.

## AD_CERVICALGIA_AI-Barontini (fasi 1–4)

| grafica | scelta approvata | quando |
|---|---|---|
| etichette barrate | V1 «finestra» nella finestra grande; barra panna piena che resta all'85%; pillola barrata al 55% | 03/11, fase 1 |
| etichette barrate | la barra arriva su «fare»; «medicine» compare 0,29 s prima della parola | 03/11, fase 1 |
| card dei 3 motivi | 4 apparizioni a tutto schermo; card in fila con il numero nel riquadro; velo blu al 45–50% | 03/11, fase 2 |
| card dei 3 motivi | «non solo il collo»; apparizione 2 così; il blocco 35,6–40,1 s (etichette e poi card 3) resta denso; l'alone della card 3 | 03/11, fase 2 |
| equazione | risultato tutto verde, anche «a lungo termine»; modo «finestra» con il rettangolo che cambia sul taglio | 04/11, fase 3 |
| obiettivo | «tutto schermo» a momenti, 3 apparizioni; card con spessore (non card accese); card vuote dal primo fotogramma che si accendono sulla loro frase; riepilogo con tutte piene | 04/11, fase 3 |
| obiettivo | «senza pensarci» si legge 0,9 s prima di sentirlo (l'apparizione chiude sul taglio) | 04/11, fase 3 |
| chiusura | «tutto schermo» fino alla fine; «€49» esattamente come detto; modulo con campi vuoti senza etichette; pulsante «compila» che resta sotto il logo; freccia verso il pulsante dell'ad; il pulsante compare 0,55 s dopo «compila» | 04/11, fase 3 |
| — | nessuna grafica su «ci devi convivere» (50 s) | 04/11, fase 3 |

## Difetti di esecuzione corretti con varianti nuove (fase 5)

Questi **non** sono scelte approvate: sono difetti che il direttore della fase 4 ha trovato e che ho verificato. Le varianti «in prova» li correggono.

| difetto | variante |
|---|---|
| equazione: la finestra entra sfumando e il primo termine compare sopra il B-roll (f377–380) | `equazione-finestra-v2` |
| etichette: il fondo entra ed esce sfumando, e il B-roll si vede attraverso le pillole (f1068–1070, f1156–1159) | `etichette-barrate-finestra-v2` |
| chiusura: «ci vediamo» sale da una maschera e per un fotogramma restano solo l'asta della «d» e il punto della «i» (f2028) | `chiusura-9x16-v2` |

## Decisioni di Riccardo dopo la fase 5 (04/11/2026)

- Render con la GPU come standard: le piccole differenze fra due render vanno bene, perché la consegna è la copia del file approvato.
- «pensato per» è un'opzione dell'equazione dove è detto; diventa obbligatorio quando il risultato, letto da solo, sembra una promessa. Un direttore che chiede «pensato per» su un risultato che non sembra una promessa fa una proposta, non trova un difetto.
- Un ultimo giro (giro 3) sulle varianti in prova, per i tre difetti di esecuzione nuovi:

| difetto (fase 5, giro 2) | correzione (giro 3) | voto giro 3 |
|---|---|---|
| etichette: le pillole escono sfocate fino al taglio (f1159) | pillole nitide fino al taglio | 7 |
| chiusura: «gli ultimi» tagliato dalla maschera (f1848) | righe della lista e «a soli» entrano intere, senza maschera | 7 |
| equazione: l'uscita finisce su «sciog» (f540) | uscita a parole intere, l'ultimo fotogramma mostra «sciogliere» | 6 |

Osservazioni del direttore al giro 3 che sono **scelte approvate** (non si toccano da soli): l'uscita «cancella» dell'equazione (il direttore la vorrebbe a taglio), il blocco che si ricentra, la barra sotto il risultato, le righe spente della chiusura prima della loro parola, il logo ufficiale (la T stilizzata che a 390 px ricorda un «7»), «medicine» che compare prima della parola.

Difetti di esecuzione visti al giro 3 e **non corretti** (il giro era uno solo): finestra vuota per 6–7 fotogrammi prima della prima pillola delle etichette (f1067–1073, entrata di `etichette_luce`); un provvisorio della decifrazione che forma una parola vera («sollieva», equazione f488–496); l'uscita in dissolvenza del primo blocco della chiusura (f1946–1947) e il vuoto fra «ci vediamo» e il logo (f2032–2044).

## Sistema di forme e frontman AD_CERV_26 (Riccardo, 07/11/2026)

Approvati («Molto molto meglio, finalmente!»): lo **stile** (forma blu con i puntini e il filo verde, card con spessore, disegni
Servier in chiaro, indicatore a trattini, barre con l'orologio, lista che si barra, parola chiave in gradiente, movimenti e
trasformazioni), le **forme** e i **sottotitoli** del frontman. Non si cambiano per un'osservazione del direttore; i difetti di
esecuzione sì.

| grafica | scelta approvata | data |
|---|---|---|
| tutto il reel | quattro forme per inquadratura: pannello sotto il volto, fascia alta su finestre e mani, tendina a tutto schermo solo su «tre benefici» (4,97–6,97 s, l'unico tratto senza sottotitoli), badge del passo accanto alla testa | 07/11 |
| tutto il reel | lo stampo «testo corto a sinistra, card con l'oggetto a destra» in tutte le forme (è lo stile fisso) | 07/11 |
| benefici | card dei muscoli che resta sotto «da solo non basta / secondo» fino al taglio sulla 3D; «il nostro / specifico» con la card del logo; tre card con la cifra nella tendina | 07/11 |
| differenze | «non trovi / tutto fare» con la sola riga barrata; barre e orologi; card del «?» su «il vero segreto» | 07/11 |
| offerta | (sì all'idea; esecuzione da approvare sull'anteprima) pannelli brevi sotto il volto a 55,5–61 s, sopra sottotitoli e banner; dopo 60,8 s le forme restano chiuse (banner e prezzo del montaggio) | 07/11 |
| terzo | (sì all'idea; esecuzione da approvare sull'anteprima) un disegno Servier di nervi o midollo per «il tuo sistema nervoso» | 07/11 |

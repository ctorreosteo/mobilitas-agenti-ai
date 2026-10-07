# INDICE DI MONTAGGIO — colon-irritabile-torino

> **STATO: COMPLETO.** 1 b-roll su 1, immagine + video. Verificato sul disco il 2026-09-29 alle 14:15.

| | |
|---|---|
| **Slug** | `colon-irritabile-torino` |
| **Formato** | 9:16 verticale |
| **Modello immagine** | `soul-cinema` (SOUL Cinema) |
| **Modello video** | `kling-3-std-i2v` (Kling 3.0 Standard, image-to-video) |
| **Condizione / citta** | colon irritabile — Torino |
| **Genere** | donna (imposto al lancio; la condizione da sola darebbe "entrambi") |
| **Costo reale** | 4,52 crediti — 0,28 USD (da `/estimate`, non dal catalogo) |
| **Piano** | `broll-generati/colon-irritabile-torino/piano.json` |

## I numeri veri, contati sul disco

| Cosa | Atteso | Trovato |
|---|---|---|
| Immagini | 1 | **1** — 3,3 MB, 1152x2048 (ratio 0,5625 = 9:16 esatto) |
| Video | 1 | **1** — 6,7 MB, 720x1280, 6,04 s, 145 fotogrammi |
| `manifest.json` | 1 | **1**, esito `completo` |

Nota tecnica: `01-pain-dieta-esclusione.jpg` ha estensione `.jpg` ma contiene dati **PNG**
(verificato con `file`). La maggior parte dei software di montaggio legge dal contenuto e
non dall'estensione, ma se un programma lo rifiuta basta rinominarlo `.png`.

## Tabella di montaggio

| id | tipo | copre | durata | variante | video | immagine |
|---|---|---|---|---|---|---|
| `01-pain-dieta-esclusione` | pain | "Hai tolto il glutine, il lattosio, mezzo mondo… e non è cambiato niente." | 6 s | unica | `video/01-pain-dieta-esclusione.mp4` | `immagini/01-pain-dieta-esclusione.jpg` |

## Mancanti

Nessuno. Il piano prevedeva un solo b-roll ed e stato prodotto.

## Come si monta

**Progressione dello script:** PROBLEMA → RIPETIZIONE FALLITA → INCOGNITA QUOTIDIANA →
NON CREDUTA → SPIEGAZIONE → DESIDERIO

Il b-roll entra **dalla seconda frase**, subito dopo "...togliendo un cibo alla volta", ed
esce prima di "Ti e mai capitato di mangiare una cosa e stare bene": il ritorno sul volto
deve coincidere con la domanda diretta in camera.

**Resta sul volto dell'osteopata** (7 passaggi, dal piano):

1. "Il colon irritabile non si risolve togliendo un cibo alla volta." — regola d'apertura.
2. "Ti e mai capitato... Non e colpa tua. C'e un motivo fisico preciso..." — domanda diretta
   piu assoluzione: un'immagine chiuderebbe il loop che deve restare aperto fino al meccanismo.
3. "Perche quando non c'e una regola, ogni giornata e un'incognita..." — **lo meriterebbe**:
   e il beat della vergogna sociale, quello che converte. Scoperto per quota, non per scelta.
4. "E gli esami? ...e lo stress, sei una persona ansiosa." — il colpo e nel tono di voce che
   cita il medico; un referto inquadrato lo indebolirebbe.
5. Tutto il blocco meccanismo — quota infografiche fissata a 0.
6. Desiderio latente — vale la faccia di chi contraddice il "deve conviverci".
7. CTA — la fiducia si trasferisce da un volto.

## Difetti osservati sul girato

Guardati immagine e primo/ultimo fotogramma del video:

1. **Il quaderno porta pseudo-lettere.** E esattamente il rischio che il collaudo aveva
   segnalato: il divieto di testo era esplicito nel prompt e il modello ha comunque disegnato
   forme che leggono come parole, nel terzo basso. Nel video la carrellata le porta quasi
   fuori campo verso la fine, ma nei primi secondi si vedono.
2. **La carrellata stringe molto piu del 5% chiesto.** Piatto e quaderno escono quasi del
   tutto dall'inquadratura: la natura morta delle diete fallite si perde a fine clip.
3. **La mano si appoggia sul petto, non sotto lo sterno.** Su un video di colon irritabile
   un gesto sul petto legge come cuore o respiro, non come pancia.
4. **Compare un secondo anello** sulla mano che sale, mentre nell'immagine sorgente ce n'e uno solo.
5. **La forchetta resta in mano** invece di essere posata sul bordo del piatto: il segnale di
   resa e piu debole di quanto il prompt chiedesse.
6. **Torino si vede poco.** Niente cortile ocra con persiane verdi dalla finestra; un
   elettrodomestico in acciaio sullo sfondo sposta l'ambiente verso il generico contemporaneo.
   Termosifone in ghisa, parquet e finestra alta reggono il registro europeo, ma il tessuto
   torinese resta implicito.

I punti 1, 3 e 5 sono correzioni di prompt: si sistemano in `piano.json` e si rigenera a 0,28 USD.

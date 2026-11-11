# Trovare le papere quando il riconoscitore mente

## Il problema

Whisper **non trascrive quello che sente: trascrive quello che ha senso**. Davanti a una ripresa doppia scrive la frase una volta sola, corretta. La papera sparisce dal testo e il montaggio la lascia dentro.

Lo fa su file intero, e lo fa anche su finestre da 9-14 secondi. In YT_TOFU_02 la v1 ha consegnato quattro difetti, tutti invisibili alle sue sonde:

| a (v1) | cosa | perché era sfuggita |
|---|---|---|
| 1:05 | "mancano ancora due ore e… / Mancano ancora due ore e mezza" | pausa di 1,4 s: sotto la soglia del ritmo, e la sonda da 9 s l'appianava |
| 9:27 | "devi iniziare a pensare… / devi iniziare a pensarlo come…" | il taglio della ripresa precedente ripartiva un blocco troppo presto |
| 10:29 | "Si pa… no… si parte dal diaframma" | nessun segnale guardava le parole troncate né i "no" isolati |
| 11:36 | "si accorgono che il calo delle tre si è appiattito / si accorgono che il calo delle tre si appiattisce" | pausa di 0,8 s, sotto la soglia della sonda delle pause |

La sonda da 14 s sul file v1 dava "Devi iniziare a pensarlo come quello che è davvero…": pulita. Quella da 2,6 s dava "a pensare… devi iniziare a pensare". **Per verificare un punto si usano clip da 2-4 s.**

## I nove segnali (`motore/papere.py`)

| # | segnale | peso | cosa prende |
|---|---|---|---|
| 1 | ripresa doppia (sonda pause > 1,2 s) | 3 | il DOPO ricomincia con le parole del PRIMA |
| 2 | regia | 1,5-2 | "ho sbagliato", "aspetta", "torna su", "stoppa", "ciak", conteggi |
| 3 | a-parte | 1,5 | blocco < 0,75 s con > 1,2 s di silenzio attorno |
| 4 | ripetizione | 1 | stesso 4-gramma (2+ parole piene) entro 90 s |
| 5 | appianata | 2 | ≥4 parole che le finestre hanno e la trascrizione intera no |
| 6 | copione | 3 | frase del copione detta più volte; parlato fuori copione |
| 7 | blocco ripetuto | 3 | un blocco ricomincia come uno dei due precedenti, o ne riprende la coda |
| 8 | troncata / attacco monco | 2,5 | blocco che finisce con "…"; blocco breve che è l'inizio di uno dei due successivi |
| 9 | interiezione / coda spuria | 1,5-2 | "no", "ok", "qua", "di" isolati da pause |

I segnali si fondono in regioni; ★★ da 2 punti, ★★★ da 4. Nessun segnale basta da solo, e nessuna combinazione sostituisce la lettura di `trascrizione.txt`.

## Cosa NON è una papera

Il segnale 7 e il 4 suonano anche sulle **ripetizioni retoriche**: "ti sei convinto che sia normale… ti sei convinto che sia colpa tua", "cinque respiri profondi… cinque respiri profondi non lo decomprimono". Si tengono: vanno in `scartati` con il motivo, e se il QC le segnala su una giunta, il numero della giunta va in `giunte_ok`.

## Quando aggiungere un segnale

Ogni difetto che arriva a Carlos è un segnale che mancava. Prima di correggere il video, chiediti quale controllo l'avrebbe trovato, aggiungilo a `papere.py` e verifica che sul banco di prova (`videos/YT_TOFU_02-v2`) trovi ancora tutte le 18 papere senza nuovi falsi allarmi forti.

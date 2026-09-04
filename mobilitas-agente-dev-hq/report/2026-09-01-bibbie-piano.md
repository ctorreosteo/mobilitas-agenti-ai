# Piano — ripresa generazione Bibbie (1 settembre 2026)

## Stato sul disco (verificato con `ls`, non dai report)

- `problemi.json`: **68** condizioni totali
- Consegnate in `outputs/`: **45**
- **Da fare: 23**

## 1. Fibromialgia — in chiusura

### Da dove ripartiva
Ferma a `v6-chiarezza.md` + `mappa-v6.md` (interrotta il 01/09 alle 09:44). Rilanciata alle 19:43 passando al workflow lo stato dei 28 file gia' su disco: stadi 1-7 saltati, nessun agente sprecato.

### Cos'e' andato a buon fine
| | |
|---|---|
| `v7-finale.md` | prodotta alle 19:55 — 37 frasi toccate su 1352, identita' 98%, 7 metafore di servizio |
| `mappa-finale.md` | prodotta alle 19:55 |
| `collaudo-chiarezza.json` | script deterministico, girato alle 20:51 |
| `collaudo-lingua.json` | script deterministico, girato alle 20:52 |

### Cos'e' fallito, e perche' non e' un difetto della Bibbia
Il **collaudo semantico** e' morto **sei volte di fila** sul guardiano dei 180 secondi del workflow. Non un errore degli agenti: dai transcript risulta che leggevano i due documenti capitolo per capitolo facendo lavoro vero, ma fra un passo e l'altro superavano il timeout. Sono 341 KB da inventariare, circa 1350 frasi.

Conseguenza a catena: lo stadio **Consegna** non e' mai partito, quindi `outputs/fibromialgia/` non esiste.

### I bloccanti dello script, esaminati
| codice | severita' | verdetto |
|---|---|---|
| `TABELLE_FUORI_SPECIFICA` (17 righe) | BLOCCANTE | **falso positivo di conservazione.** Lo script controlla solo il documento a valle; le righe segnalate stanno identiche nella v5 (verificato riga per riga). Il superamento c'era gia' in ingresso: appartiene al livello di asciugatura, non a chi ha riscritto |
| `BOX_NON_PREVISTI` (4 tipi) | AVVISO | ereditato dalla v5 |
| `PAROLE_FUORI_RANGE` (23.098 parole) | AVVISO | lo script stesso dichiara che non e' un difetto di conservazione |

Sinusite cronica e' uscita con la stessa classe di segnalazioni.

### Cosa resta
1. **Collaudo semantico** — rilanciato fuori dal workflow, dove il guardiano dei 180 secondi non c'e', con istruzione di lavorare a blocchi chiusi un capitolo per volta *(in corso)*
2. Riparazione chirurgica, **solo se** il collaudo apre bloccanti veri
3. `nota-di-lavorazione-fibromialgia.md`
4. I due `.docx` in `outputs/fibromialgia/` — `build_docx.py`, pandoc 3.10 presente

## 2. Coda successiva (ordine di `problemi.json`), una alla volta
artrite · piedi-gonfi · gonfiore-addominale · diarrea-ricorrente · sensazione-di-fiato-corto · dolore-al-coccige · labirintite · menopausa · diastasi · cicatrici-seno-rifatto · pubalgia · coxalgia · tendinite-d-achille · scoliosi · spalla-congelata-capsulite-adesiva · sindrome-di-arnold-nevralgia-occipitale · asma · spalla-dolorosa-periartrite-cuffia-dei-rotatori · dolore-sacroiliaco · trocanterite · distorsione-caviglia · tendinite-calcifica-spalla

## Come vengono lanciate

`genera-bibbie.workflow.js`, **una invocazione per Bibbia**, mai due insieme: il parallelo brucia la quota prima che una arrivi in fondo. Ogni lancio si chiude con la verifica sul disco (`v7-finale.md` + `mappa-finale.md` + i due `.docx`) prima di passare alla successiva.

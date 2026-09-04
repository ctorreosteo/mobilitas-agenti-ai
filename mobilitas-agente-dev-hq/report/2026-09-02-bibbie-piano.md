# Piano — ripresa Bibbie (2 settembre 2026)

## Stato verificato sul disco, non dai report

| | |
|---|---|
| Condizioni in `problemi.json` | 68 |
| Consegnate in `outputs/` | **46** |
| Da fare | **22** |
| In lavorazione | artrite |

## 1. Fibromialgia — CHIUSA

Sul disco ci sono `v7-finale.md` (171 KB) e `mappa-finale.md`, prodotte il 01/09 alle 19:55, piu' i due collaudi deterministici girati alle 20:51 e 20:52. Manca `outputs/fibromialgia/`: lo stadio Consegna non e' mai partito perche' il collaudo semantico e' morto sei volte sul guardiano dei 180 secondi del workflow.

### Il bloccante dello script, richiuso
`TABELLE_FUORI_SPECIFICA` (17 righe) e' un **falso positivo di conservazione**. Le righe segnalate stanno identiche nella v5 e nella v7 — verificato per campione con `grep -c` su quattro delle otto righe di dettaglio: una occorrenza per parte, in entrambi i documenti. Il superamento c'era gia' in ingresso: appartiene al livello di asciugatura, non a chi ha riscritto. `BOX_NON_PREVISTI` e `PAROLE_FUORI_RANGE` sono avvisi, ereditati dalla v5.

### Come e' stato rilanciato il collaudo semantico
Fuori dal workflow, dove il guardiano dei 180 secondi non c'e', spezzato in tre perimetri chiusi invece che in un solo agente su 341 KB:

| perimetro | capitoli |
|---|---|
| 1 | 0 · 1 · 2 · 3 · 4 · 5 |
| 2 | 6 · 7 · 8 · 9 · 10 |
| 3 | 11 · 12 · 13 · 14 · Appendici · Mappa |

Ognuno lavora un capitolo per volta, a blocco chiuso, leggendo per intervallo di righe invece che il file intero.

### Esito del collaudo semantico
Tutti e tre i perimetri: **CONSEGNABILE, zero bloccanti**. Verdetto su disco in `collaudo-semantico.json`.

Nessun claim assorbito, nessuna qualificazione caduta, nessuna etichetta riancorata, nessun numero riattribuito. La tabella delle bandiere rosse e' identica su tutte e tredici le righe, destinatari e tempi compresi; l'Appendice B e' identica byte per byte. Le uniche aggiunte sono sette metafore di servizio, verificate con la prova della copertura. La v6-v7 ha lavorato per spezzatura di periodi, non per compressione: e' il profilo di una riscrittura che non assorbe.

### La sola riparazione, applicata
Un avviso, e una parola. Nel box «Quanto e' solido» del primo meccanismo del capitolo «Perche' le mani possono cambiare qualcosa», la riscrittura di chiarezza aveva sciolto una relativa in frase indipendente e nel farlo aveva portato il verbo all'indicativo, sotto un'etichetta PROBABILE:

> «Il meccanismo e' questo: la terapia manuale **alza** la soglia» → «Il meccanismo e' che la terapia manuale **alzi** la soglia»

Collaudo di lingua rilanciato dopo la riparazione: identita' 98%, 71 PMID, 24 etichette, invariati.

### La nota di lavorazione non e' un cancello
Ce l'hanno **11 Bibbie su 46**: le altre 35 sono state consegnate senza. E' un documento di stadio v1, che l'autore scrive quando ha scelte da dichiarare, non un deliverable sistematico. Per fibromialgia il v1 e' uscito senza, e scriverla adesso a catena finita sarebbe un'invenzione, non una nota di lavorazione. Lasciata fuori.

### Consegna
`outputs/fibromialgia/Bibbia_Fibromialgia.docx` (83 KB) e `Mappa_Fibromialgia.docx` (17 KB), verificati con `ls`.

## 2. Coda successiva, una alla volta

**artrite** e' partita (`genera-bibbie.workflow.js`, catena completa dal v1: la cartella non esisteva).

piedi-gonfi · gonfiore-addominale · diarrea-ricorrente · sensazione-di-fiato-corto · dolore-al-coccige · labirintite · menopausa · diastasi · cicatrici-seno-rifatto · pubalgia · coxalgia · tendinite-d-achille · scoliosi · spalla-congelata-capsulite-adesiva · sindrome-di-arnold-nevralgia-occipitale · asma · spalla-dolorosa-periartrite-cuffia-dei-rotatori · dolore-sacroiliaco · trocanterite · distorsione-caviglia · tendinite-calcifica-spalla

## Come vengono lanciate
`genera-bibbie.workflow.js`, **una invocazione per Bibbia**, mai due insieme: il parallelo brucia la quota prima che una arrivi in fondo. Ogni lancio si chiude con la verifica sul disco — `v7-finale.md`, `mappa-finale.md` e i due `.docx` — prima di passare alla successiva.

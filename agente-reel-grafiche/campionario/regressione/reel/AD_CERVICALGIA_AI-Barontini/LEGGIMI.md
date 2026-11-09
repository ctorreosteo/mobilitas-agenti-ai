# Esempio fisso di non regressione dell'agente reel-grafiche: AD_CERVICALGIA_AI-Barontini

Il primo ad consegnato (fasi 0–4), rifatto da zero con il procedimento di oggi e confrontato con un riferimento. Serve a dimostrare che una modifica al motore dei reel non cambia quello che esce.

## Come si lancia

```bash
./mve reel-regressione                 # circa 13 minuti
./mve reel-regressione --riferimento   # solo dopo aver guardato un CAMBIATO voluto
```

**Quando:** dopo ogni modifica a `motore/motore/reel*.py`, `motore/motore/reel_dom.mjs`, `motore/swift/testo.swift`, ai modelli `motore/inserti/scene/*_ads*` o alle impostazioni del render (`reel_grafiche.WORKERS`, `reel_grafiche.GPU`).

**Cosa fa:**
1. crea lo slug temporaneo `videos/_regressione-reel-AD_CERVICALGIA_AI-Barontini/`;
2. rifà radiografia, 3D (dal caso), controllo del piano, approvazione del piano congelato (solo se l'md5 è quello di `caso.json`), render e controlli;
3. confronta con `riferimento/`;
4. scrive l'esito in `ultimo/` e cancella lo slug temporaneo e la sua `.lavoro/`.

## Esiti (`ultimo/ESITO.md`)

- **OK**: uguali al riferimento:
  - radiografia: tagli, schemi, finestre, sottotitoli, parole e tempi della voce;
  - controlli: errori, grafiche visibili, ingombro del testo, testi scritti, SSIM;
  - audio;
  - livelli delle grafiche.

  Sono ammessi solo gli **arrotondamenti**:
  - un fotogramma del livello di una grafica può differire dal riferimento, purché le medie dei blocchi 8×8 non si scostino di più di 2 livelli. È il render in un processo con la GPU: di solito 1 livello su poche decine di pixel nella chiusura e in 2 fotogrammi delle card;
  - nel video finale possono differire i fotogrammi dal punto in cui un livello si arrotonda, perché la codifica x264 propaga la differenza (fino a SSIM 0,998).
- **Vision**: le letture sbagliate (per esempio «€49» sfocato letto «673») cambiano da un'esecuzione all'altra e non si confrontano. Conta solo che, a parte quelle in `verifiche.json`, non resti niente da guardare. Le letture nuove finiscono in `ultimo/cifre-da-guardare/`: si guardano, e se sono letture sbagliate si aggiungono a `verifiche.json`.
- **CAMBIATO**: guarda `ultimo/ESITO.md`, `ultimo/video.mp4` (il video di questa esecuzione), `ultimo/livello-*.npz` (i livelli a blocchi), `ultimo/controlli.md` e `ultimo/tavola.jpg`, poi spiega ogni differenza nel report. Se il cambio è voluto, rifai il riferimento con `--riferimento`.
- **ROTTO**: una tappa fallisce o i controlli danno errori: si corregge subito.

**Da sapere (fase 5).** In una delle tre esecuzioni di confronto il livello della chiusura è cambiato fino a 6 livelli sulle medie 8×8, in 33 fotogrammi dal 2042, dove entra il logo. Non si è ripetuto e allora il video non veniva conservato: la causa non è nota. Se ricapita, ora `ultimo/video.mp4` permette di guardarlo.

## Cosa c'è qui

| file | cosa |
|---|---|
| `caso.json` | da dove viene il video (inbox/), le 3D (inquadrature 3 e 9), l'md5 del piano congelato |
| `piano.json` | il piano approvato da Riccardo (fasi 1–4), con i modelli di partenza e non le varianti in prova: misura il motore, non le grafiche nuove |
| `verifiche.json` | le letture di Vision già guardate: «?» letto «2», «€49» letto «349», «673», «67З» |
| `vision-letture-sbagliate-f1958-f2026.jpg` | i due fotogrammi guardati nella fase 5 |
| `riferimento/` | `radiografia.json`, `controlli.json`, `fotogrammi.md5` (md5 di ognuno dei 2075 fotogrammi), `video.json` e `riferimento.mp4` (render in un processo con la GPU, 04/11/2026 10:10) |
| `esempio/slug-prova-fase4/` | lo slug della prova della fase 4, spostato qui da `videos/`: radiografia, piano e tavola, anteprime (`…_lavoro-intero.mp4` è il video **approvato da Riccardo**, md5 `fd878e80…`), controlli, voti |
| `ultimo/` | l'esito dell'ultima esecuzione |

**Il riferimento e il video approvato non sono lo stesso file.** Il video approvato è stato reso con più processi, il riferimento con uno solo (fase 5). Differiscono in 655 fotogrammi, tutti dentro le grafiche, di sottopixel: SSIM 0,99929, differenza massima 53 livelli dopo la codifica. Il riferimento serve a confrontare il motore con sé stesso; la consegna dell'ad resta quella approvata.

---
name: mobilitas-montaggio
description: Il motore di montaggio dei video @Studio_Mobilitas (./mve), dal .MOV di camera al montato pulito — colore HLG->BT.709 senza zscale, trascrizione a blocchi, i nove segnali del cacciatore di papere, EDL sulla griglia dei frame, punti di taglio sul fondo di sala, ascolto delle giunte, inquadrature dinamiche dal 4K con il volto di Apple Vision, audio a -14 LUFS. Usala per qualsiasi montaggio del canale, prima di toccare ffmpeg o il motore.
---

# mobilitas-montaggio

Il girato del canale arriva come ripresa unica: la presentatrice si ferma, si corregge a voce ("ho sbagliato", "torna su un pochettino") e rifà la battuta. Montare vuol dire soprattutto **trovare e togliere quei punti**, e la parte difficile è trovarli, non tagliarli.

Tutto passa da `./mve <fase> <slug>`. Il codice sta in `motore/motore/`; un modulo per fase, con il perché scritto in testa al file.

## Sorgente e colore (`init`, `prep`)

Il motore non dà per scontata una camera: legge tutto dal file. Due sorgenti conosciute:

| | iPhone (girati di Carlos, YT_TOFU_02) | Sony A6700 (MR_POSTURA_01) |
|---|---|---|
| video | 3840x2160 HEVC Main10, 59,94p | 3840x2160 HEVC Main10, 50p |
| colore | HLG BT.2020 + RPU Dolby Vision → LUT | Rec.709 SDR, range `tv` → nessun LUT |
| rotazione | −180 | nessuna |
| audio | −26/−29 LUFS | **−13,9 LUFS, true peak +0,5, clipping** (LPCM 16 bit) |
| uscita | 29,97 | **25** |

`init <file> [slug] [--copione testo.md|.txt]` collega il file (non lo sposta) e scrive `meta.json`. Con una cartella, `init inbox/<SLUG>/`, lo slug è il nome della cartella e `init` trova da solo l'unico girato (`.mp4`/`.mov`/`.mxf`, non dentro `materiali/`), l'unico `.md`/`.txt` come copione (se `--copione` non c'è) e `materiali/` (in `meta.json` → `materiali`). Con più girati si ferma e chiede quale; con più testi non sceglie e avvisa; con `--copione` copia il testo in `copione.md` (prima riga → titolo `# …`, sezione "Descrizione YouTube" tolta) per il segnale "copione" di `papere`. `prep` estrae tre audio (analisi, riconoscimento normalizzato a −20, master 48k/24 bit), misura loudness e clipping e mappa i blocchi di parlato.

**Frame rate d'uscita** (`progetto.fps_uscita`, scritto da `init` in `meta.json` → `fps_uscita`): sopra i 30 fps la metà esatta, altrimenti uguale alla sorgente. 59,94 → 29,97, 50 → 25, 25/24/30 restano. Si decima 2:1 con `fps=`: un frame sì e uno no, nessun judder. Tutte le fasi lo leggono da `P.fps` / `P.fps_str` (GOP: `P.gop`, 2 s); il QC esige quello del progetto. I progetti nati prima senza `fps_uscita` lo ricavano con la stessa regola: a 59,94 nulla cambia.

**Gamma di ripresa.** Le Sony scrivono un XML (`NonRealTimeMeta`, box `meta/xml`) con camera, `captureFps` e `CaptureGammaEquation`: `init` lo legge (`camera`, `gamma_ripresa` in `meta.json`). Se la gamma non è `rec709` (per esempio S-Log; un HLG dichiarato anche nel flusso no, lì c'è il LUT) `init` e `prep` stampano un avviso a tutta riga: i tag del flusso possono dire bt709 anche su S-Log, e il motore la tratterebbe come Rec.709. Serve un LUT dedicato prima di montare.

**Audio alto e clipping.** `prep` cerca nella sorgente, nel formato nativo, i campioni a fondo scala (|x| ≥ −0,01 dBFS): due o più di fila sono una corsa (cima tosata), corse entro 0,5 s fanno un tratto. In `meta.json → clipping`: campioni (per canale), corse, tratti con inizio e fine. La A6700 di MR_POSTURA_01: 1469 campioni, 129 corse in 14 tratti, quasi tutti nei primi 29 s. La catena voce si adatta (`audio.catena_voce`, sezione Audio).

**Materiali.** Quelli di un solo video stanno in `inbox/<SLUG>/materiali/`, quelli comuni in `libreria/` (regole in `libreria/LEGGIMI.md`, note e consensi in `libreria/catalogo.md`). Le fasi li cercano con `P.materiale(nome)`: prima nei materiali del video (`meta.json` → `materiali`, altrimenti `inbox/<slug>/materiali/`), poi in libreria; per nome o percorso relativo, e un nome che compare più volte nella stessa cartella è un errore, non una scelta. `./mve materiali <slug>` elenca cosa c'è nell'ordine di ricerca.

**B-roll a 30 fps in un progetto a 25 (regola, decisione del 26/10/2026).** Le clip della libreria sono esportazioni 1080p a 30 fps. Non si decima (scartare 1 fotogramma su 6 fa scattare i movimenti): si **rallentano all'83%**, cioè i 30 fotogrammi di ogni secondo si riproducono a 25 (`setpts=PTS*30/25`, poi `fps=25` che non scarta niente), **sempre senza audio**. Una clip di 6 s occupa 7,2 s di montato. Si applicherà nella fase inserti. **Indice del B-roll: `./mve libreria`** (senza slug; `motore/libreria.py`). Per ogni clip di `libreria/broll/<tema>/`:
- **tecnica:** durata, risoluzione, fps, hash SHA-1. I file identici sono una clip sola (`doppioni`).
- **volti:** con Apple Vision ogni 0,5 s: quanti al massimo e altezza sul quadro.
- **movimento di camera e tremolio:** correlazione di fase fra fotogrammi a 320×180, in % della larghezza al secondo. Verificato su clip sintetiche: fermo 0, panoramica 6,7 contro 6,25 attesi, tremolio 26,6 contro 25.
- **altre misure:** differenza media fra fotogrammi, nitidezza (varianza del laplaciano) e il tratto più stabile di 3-6 s.

Rilanciabile: rifà solo i file nuovi o cambiati, e un file spostato o doppio si riconosce dall'hash. 856 clip in 3,4 min la prima volta, 0,7 s dopo.

Prepara anche i fogli 4×4 (`libreria/.indice/fogli/<tema>-NN.jpg`, fotogramma centrale con il numero, legenda in `<tema>.json`). Le descrizioni le scrive chi guarda i fogli, in `libreria/.indice/descrizioni/<tema>.json`: una voce per clip con `num`, `id`, `parte`, `azione`, `inquadratura` (dettaglio/medio/largo), `difetti` e `voto` 1-5. Sono legate all'`id` (hash), non al numero. Escono `libreria/indice.json` (per il motore) e `libreria/indice.md`. Le clip da non usare mai stanno in `libreria/.indice/esclusioni.json` (per id, con i motivi) e nell'indice hanno `esclusa`. Il B-roll si sceglie **solo** con `libreria.utilizzabili(voto_min, tema)`, che le scarta sempre insieme a quelle senza descrizione o con voto basso. Per una libreria grande le descrizioni si dividono per cartella fra agenti in parallelo, con il divieto di copiare immagini fuori dal laboratorio. Le foto di `prima-dopo/` si usano solo se il catalogo segna il consenso.

`ffmpeg` di Homebrew **non ha `zscale` né `libplacebo`** e `colorspace` non conosce l'HLG: la conversione è un LUT 3D precalcolato una volta sola (`motore/colore.py`, in `.cache/`). In coda alla catena serve `setparams=…bt709`: i flag `-color_*` da soli lasciano il file taggato `arib-std-b67`. Il QC controlla tag e range (`tv`).

**Versione di un video** (`./mve versione <slug> <slug_v2>`): un progetto nuovo dallo stesso girato e con gli stessi tagli (si copiano analisi, regia e audio montato, con le date: `stato` riparte da `grafica`). La versione di prima non si tocca. MR_POSTURA_01_v2: EDL identica byte per byte.

## Trascrivere (`trascrivi`)

Tre trascrizioni, per tre usi:

| file | come | serve a |
|---|---|---|
| `parole-sorgente.json` | intera, DTW | confronto (segnale "appianata") |
| `parole-finestre.json` | finestre 26 s ogni 20 s | ripetizioni, regia |
| `blocchi-testo.json` → `trascrizione.txt` | **ogni blocco di parlato da solo** | leggere, decidere, ancorare i tagli |

**Whisper appiana le riprese doppie** quando vede le due prese insieme: su file intero, e anche su finestre da 9-14 s, scrive una frase corretta mai pronunciata. Trascritto blocco per blocco (fra due pause misurate) non può farlo. I blocchi hanno inizio e fine misurati sull'inviluppo, quindi sono anche i punti a cui ancorare i tagli.

Flag che contano: `-mc 0` (senza, degenera in loop), `-dtw large.v3`, `-ml 1 -sow`. Su clip brevissime whisper scrive "Grazie." sui rumori: il motore li filtra.

## Volti (`volti`)

`motore/swift/visione.swift` (Apple Vision, compilato al primo uso) traccia il volto ogni 0,5 s: riquadro, qualità dello scatto, orientamento, apertura degli occhi. 20 minuti in 45 s. Serve a centrare le inquadrature, a mettere le card dalla parte libera e a scegliere le miniature.

È anche il **controllo terzi**: un secondo volto che resta in scena per almeno 1,5 s è STOP. I campioni isolati (in YT_TOFU_02: le mani giunte, due volte) vengono elencati come avviso: guardali comunque.

## Trovare le papere (`papere`)

Nove segnali indipendenti (dettaglio in `references/papere.md`):

1. sonda delle pause (PRIMA/DOPO trascritti da soli)
2. parole di regia
3. a-parte (blocco breve isolato)
4. ripetizioni (4-grammi entro 90 s)
5. appianamento (parole che solo le finestre hanno)
6. copione (se c'è `copione.md`)
7. **blocco contro blocco**: un blocco che ricomincia come uno dei due precedenti
8. parola troncata e attacco monco ("Si par…" / "si parte")
9. interiezione o coda spuria isolata ("no", "qua", un "di")

Banco di prova: YT_TOFU_02, 13 papere trovate a mano nella v1 più 5 che la v1 aveva consegnato senza vederle. Il cacciatore v2 le trova **tutte e 18** in automatico; restano 3 falsi allarmi forti, tutti ripetizioni retoriche, che l'agente scarta leggendo.

**Ripetizioni dentro un blocco (fase 7b rivista, YT_POSTURA_32, 29/10/2026)** (`motore/motore/ripetizioni.py`). Anche la trascrizione a blocchi appiana. Quando la ripresa riparte senza una pausa da 0,2 s, whisper scrive una frase sola pulita. In YT_POSTURA_32 sono uscite così nell'anteprima, e le ha trovate Riccardo:
- «Qui c'è un collega- / qui c'è un collegamento»;
- «magari la senti / magari la senti»;
- «si bruciano / si bruciano»;
- «un correttore / un correttore»;
- «quanto è inarcato la schiena / quanto è inarcata la schiena bassa».

Cosa si fa:
- **`sotto_blocchi`**: i blocchi si spezzano nei minimi dell'inviluppo, almeno 14-15 dB sotto i picchi a 300 ms a sinistra e a destra e non oltre 26 dB sopra il fondo, con pezzi di almeno 0,5 s. Ogni pezzo si trascrive da solo e va in `data/sottoblocchi-testo.json`. Una ripresa che riparte senza pausa lascia proprio un minimo così: a 243,37 s è a +23 dB.
- **Ricerca:** `dentro` cerca una sequenza di 2 o più parole ripetuta dentro un pezzo; `fra_blocchi` la cerca fra pezzi diversi entro 10 s. Conta solo se c'è almeno una parola piena.
- **Finestre corte** (`finestre`, 1,6 s ogni 0,6 s): servono da conferma. Da sole non bastano: appianano anche loro e, sovrapponendosi, confondono.
- **Per decidere un punto:** sonde di 0,4-1,3 s, che scrivono parole diverse a seconda di dove cominciano. Si incrociano più sonde con l'inviluppo a 10 ms.

Il pezzo tenuto è **l'ultima presa completa**: si toglie tutta la precedente, compreso l'inizio monco.

## Punti di taglio (`edl`)

**Non si taglia sul confine del blocco**: la coda della sillaba scende per 100-200 ms restando udibile ("toracica" troncata nella v1). L'ancoraggio di regia si aggancia al confine di blocco più vicino, poi si cerca il primo istante a fondo di sala (+10 dB, inviluppo 5 ms con media a 30 ms) e infine il campione più silenzioso entro ±60 ms. Dentro una pausa ci può essere un colpo sul tavolo (−37 dB a 3:24 di YT_TOFU_02): la rifinitura lo evita.

Ogni segmento si **quantizza sulla griglia dei frame**: inizio su un frame sorgente, durata in frame interi d'uscita. Audio e video durano uguale al campione e 46 giunte non accumulano deriva. Il QC controlla che i frame del file consegnato siano esattamente quelli dell'EDL.

Energia residua a ogni giunta: oltre `fondo + 14 dB` è "da ascoltare", oltre `fondo + 24 dB` è "dentro una parola" e la fase si ferma.

**Code e attacchi (regola, 27/10/2026)** (`edl.blocchi_solidi`). Un micro-blocco di parlato (sotto 0,25 s) che **segue** un blocco entro 0,4 s è la sua **coda**: appartiene a quel blocco, e tagli e pause accorciate partono dopo di lui. Allo stesso modo, un micro-blocco che **precede** un blocco entro 0,4 s è il suo **attacco**. Solo i micro-blocchi isolati sotto 0,12 s restano rumore. Vale per tagli, pause e pezzi da ritrascrivere (`blocchi_montato`). Perché: in MR_POSTURA_01 l'ultima sillaba di «postura» (59,87-59,95, 0,08 s) era scartata come rumore. La pausa sembrava quindi cominciare a 59,67 e il suo accorciamento tagliava a 59,84, buttando via «-ra». L'energia sulla giunta era a −49 dB, perfetta, e whisper trascriveva comunque «postura»: nessun controllo lo vedeva. Lo stesso schema a 87,88-88,04 era salvo solo perché quel micro-blocco durava 0,16 s.

**Controllo «parola tagliata»** (`edl.parole_tagliate`, in `edl`, `audio` e `qc`). Per ogni giunta si misura l'energia nel tratto **buttato**: 400 ms subito dopo la fine tenuta e 400 ms subito prima dell'inizio. Se c'è un frammento di voce oltre `fondo + 18 dB` per almeno **80 ms** e il frammento **si chiude dentro la finestra**, la giunta butta la coda o l'attacco di una parola. In quel caso `audio` si ferma e il QC dà ERRORE. Una voce che invece continua oltre la finestra è un'altra frase, cioè la ripresa scartata di un taglio di regia, e non conta. Taratura su MR_POSTURA_01 v1: la coda «-ra» dà 120 ms a +25 dB e va segnalata; uno schiocco a 260 ms dalla fine, prima della ripresa scartata (giunta 17), dà 50 ms e non va segnalato. Se la voce buttata è voluta, il numero della giunta va in `giunte_ok`. Whisper non serve a questo: completa la parola anche quando manca.

**Attacchi solo se attaccati (fase 7b rivista).** Un micro-blocco è l'attacco della parola dopo solo se le sta a meno di **0,15 s** (`ATTACCO`). Le code restano a 0,4 s. In YT_POSTURA_32 uno schiocco «T-» di una terza partenza (47,90 s, a 0,31 s dalla ripresa) veniva preso per l'attacco di «Ti alzi» e restava nel montato: si sentiva «T… Ti alzi».

**Respiri interi.** Quando una pausa si accorcia, un respiro (un tratto sopra fondo + 10 dB, `Tagli.respiro`) resta intero o si toglie intero, mai a metà. Agli estremi di un taglio di regia, la fine tenuta si allunga oltre il rumore e l'inizio tenuto parte prima del respiro: mai verso la parola.

**`oltre_soglia`** in un taglio: quando due parole sono attaccate e non c'è un punto sotto il limite duro («compra un correttore / un correttore posturale», 500,08 s a −32 dB), la regia può accettare il taglio con il motivo. La giunta va verificata con la sonda sul montato, e il controllo «ripetizioni» la ascolta.

Ritmo: le pause sopra `pausa_max` si accorciano a `resta` (profili in `mobilitas-regia`).

## Controllo «ripetizioni» (`qc`, fase 7b rivista)

`python -m motore.ripetizioni <slug>` (dalla cartella `motore/`; lo chiama anche `qc`) ritrascrive il montato pezzo per pezzo: i sotto-blocchi della sorgente riportati sul montato, ognuno da solo, dalla voce montata. Scrive `controlli/ripetizioni.md`.

È **NON CONSEGNABILE** se trova:
- una sequenza di 2 o più parole ripetuta entro 10 s che la regia non dichiara voluta in `ripetizioni_ok` (`[{parole, t sorgente, motivo}]`);
- una parola tagliata alla giunta;
- un pezzo a metà parola. Sopra fondo + 24 dB è sempre un errore. Fra +14 e +24 decide l'ascolto: l'ultima parola prima e la prima dopo la giunta, trascritte da sole sul montato e sulla sorgente, devono coincidere. Cifre e parole valgono uguale, e sul bordo della sonda c'è una parola di tolleranza.

Su YT_POSTURA_32 v2: 397 pezzi, 0 da correggere, 10 ripetizioni dichiarate volute (parole che tornano in frasi diverse, l'elenco «quanto è…, quanto è…»).

Se un lato della sorgente accanto alla giunta è tutto sotto il limite di ascolto (silenzio), quel lato non si confronta: lì non c'è una parola da troncare, e whisper sul vuoto inventa «Grazie». Succede quando la giunta cade dentro una pausa accorciata (G39 di YT_POSTURA_32, 29/10).

**Whisper inventa sui pezzi corti e sul silenzio.** Prima di tagliare una parola letta in `ripetizioni.md` o nelle giunte, sentila con 4-5 sonde da 0,6 a 4 s. In YT_POSTURA_32 il «Sì, certo» a 0:04,95 era il pezzo di 0,5 s «sera, hai», e il «Grazie» a 4:32 era silenzio a −75 dB. Si annota in `scartati`.

## Controllo «pause lunghe» (`qc`, fase 7b)

`edl.pause_lunghe` misura la **voce** montata (non il mix: i suoni riempirebbero il silenzio) con la soglia di parlato della sorgente (fondo + 22 dB). La soglia del montato sarebbe più alta, perché le pause accorciate alzano il suo fondo. Ogni silenzio oltre **0,9 s** non dichiarato è **NON CONSEGNABILE**. Quelli voluti vanno in `regia.json` → `pause_lunghe_ok: [{t: secondi sorgente, motivo}]`.

Il controllo è nato dai 4 s muti a 4:32 di YT_POSTURA_32. Un taglio «esatto» partiva dentro il silenzio dopo «cardio», e l'accorciamento delle pause saltava ogni pausa che attraversava un taglio. Ora la pausa si accorcia sul tratto tenuto.

**Attenzione:** quando una pausa nuova si accorcia, i numeri delle giunte dopo quel punto scalano di uno. Le `giunte_ok` vanno ricontrollate (G40 → G41).

**Dopo i tagli nuovi, con la fase `scena`, si rifanno `grafica`, `inquadra` e `monta`, in quest'ordine.**
- `inquadra` riaggancia le fini dei B-roll ai suoi pezzi e riscrive `grafica.json`. Se si rilancia `grafica` da sola, i B-roll si spostano di qualche frame e `scena` trova una sovrapposizione.
- `scena` prende i fotogrammi dei B-roll da `renders/<slug>_pulito_monta.mp4`. Ora si ferma se quel file non ha i frame dell'EDL di adesso: in YT_POSTURA_32 era rimasto quello della tappa 1, con 10.469 frame invece di 10.304.

## Ascoltare le giunte (`audio`)

`audio` monta solo la voce (catena sotto), la trascrive in tempo montato e ascolta ogni giunta **due volte**: 12 s attorno, e 4 s prima + 4 s dopo trascritti separatamente e confrontati (`riattacco`, ripetizioni, troncamenti). La finestra lunga da sola non basta: appiana. Esce `controlli/giunte.md`. Si fa **prima** del render video: un errore costa 2 minuti invece di 15.

Le parole del montato (per i sottotitoli) si trascrivono a pezzi da 10 s costruiti dai blocchi della sorgente: il DTW su file intero perde la prima parola di molte frasi ("tuo cervello consuma"), e i blocchi ricalcolati sull'audio montato si spezzano sugli attacchi deboli perché lì il fondo di sala è 30 dB più alto.

## Audio

Catena voce (`audio.CATENA_VOCE`): passa-alto 75 Hz, `afftdn`, EQ (−1,5 dB a 220 Hz, +1,5 dB a 3,2 kHz), de-esser, compressione 2,5:1, `loudnorm=I=-14:TP=-1.5:LRA=9`, limiter. La riduzione di rumore viene **prima** della normalizzazione: alzare di 15 dB alza anche il fondo. Ogni segmento ha una dissolvenza di 10 ms ai bordi: su fondo di sala non si sente, e toglie i click. `audio` misura la voce montata: se non dura quanto l'EDL (±0,05 s) si ferma.

La catena è tarata su voce a −26/−29 LUFS, e soglia del compressore e `afftdn` lavorano su livelli assoluti. `audio.catena_voce(meta)` la adatta alla sorgente, misurata da `prep`:

- **clipping** (almeno una corsa): `adeclip=threshold=5` in testa, sul segnale ancora intero. Con il default (10) sulla A6700 ricostruiva il 46% dei campioni tosati, con 5 l'80% (2: 90%, ma tocca il doppio dei campioni fuori dalle corse). All'avvio `adeclip` riscrive la prima finestra (~40 ms) anche senza clipping: 100 ms di silenzio davanti (`adelay`), tolti subito dopo (`atrim`), la lasciano intatta. Dentro il grafo di `audio` (dopo `concat`) `adeclip` emette timestamp che `atrim` scarta tutti: serve `asetpts=N/SR/TB` prima di `atrim`, o la voce montata esce vuota senza errori (MR_POSTURA_01). Costa ~7 s ogni 2,4 min di audio.
- **voce più alta di −26 LUFS**: un guadagno negativo fino a −26 prima del resto (A6700: −12,1 dB). Senza, il compressore schiaccia: sulla A6700 la catena vecchia dava LRA 3,5 contro 4,4.
- girati a −26 LUFS o più bassi, senza clipping: catena identica a prima.

Sull'audio intero della A6700 la catena esce a −15,6 LUFS (il `loudnorm` a un passaggio sbaglia il bersaglio); il mix finale si riporta comunque a −14 in `suono`, con guadagno lineare.

Il mix finale (voce + sound design + musica opzionale) si riporta a −14 con un guadagno lineare, non con un secondo `loudnorm`, e un limiter a −2,2 dBFS di campione (il true peak sfora il campione di circa mezzo dB).

**Tappa 3 (YT_POSTURA_32, 30/10/2026): il mix della scena usciva a −15,3 LUFS.** Guadagno e poi limitatore: il limitatore toglie i picchi e con loro 1,3 LU. `scena.mix` ora ripete guadagno + limitatore (a 192 kHz, cioè sul picco vero, tetto −3 dBFS: con −2 l AAC portava il master a −0,9 dBTP) finché la misura torna a −14 ±0,1 (al massimo 8 giri). Il master AAC esce sotto −1 dBTP. Con `scena.coda` (schermata finale) il mix dura anche la coda: solo effetti, niente voce.

**Correzioni e tempi.** Una correzione che non cambia il numero di parole («vetro partiamo» → «vetro. Partiamo») lascia a ogni parola il suo tempo; prima i tempi si spalmavano sul gruppo e le ancore dei momenti si spostavano di 0,2-0,8 s. Una correzione che cambia il numero di parole («si... Si» → «si») li spalma ancora: non metterla dentro un'ancora.

## Inquadrature (`inquadra`, `monta`)

Dal 4K si ricavano tre tagli senza perdita: largo (1,0), medio (1,28), stretto (1,62), più varianti (1,12 / 1,42 / 1,80) per quando due pezzi forzati allo stesso taglio si toccano su una giunta. Ogni ritaglio è centrato sul volto mediano del pezzo. La grammatica è in testa a `inquadra.py`: cambio di taglio a ogni giunta, largo per card e apertura, largo per i titoli dietro, stretto sulle enfasi, altrimenti alternanza largo/medio circa ogni 9 s su una pausa fra due frasi.

**Lo stacco con cambio di taglio sostituisce la dissolvenza della v1.** Sulla macchina fissa la dissolvenza di 5 frame si leggeva come un salto morbido; lo stacco fra due tagli diversi non si vede.

`monta` renderizza ogni pezzo da solo dal 4K (videotoolbox in decodifica, crop, lanczos, LUT, x264 CRF 14), due alla volta, con cache sul contenuto, e li concatena senza ricodifica. 13 minuti in 6 minuti. `--solo 3,7` rifà solo quei pezzi. Esce anche `controlli/inquadrature.jpg`, un fotogramma per pezzo.

**Taglio "lato"** (27/10/2026): dove c'è un pannello (frase chiave, inserto) `inquadra` mette la persona al terzo opposto (`lato_sx`/`lato_dx`, zoom 1,33, variante 1,42 sulle giunte). I confini di questi tratti e dei B-roll sono duri (la grafica entra lì), ma se cadono a meno di 0,3 s da una giunta si spostano sulla giunta, che nasconde il cambio; frasi chiave e B-roll seguono. Per ogni pezzo "lato" `inquadra` salva la testa in uscita (`testa`): il QC controlla che nessun pannello la copra.

**B-roll in `monta`**: i pezzi dentro un intervallo di B-roll vengono dalla libreria, non dal girato (`_broll_cmd`): pieno, o due clip affiancate (ritaglio centrale 960x1080, filetto blu notte di 6 px in mezzo). Un pezzo di B-roll diviso da una giunta continua la stessa clip (`offset`): non si vede. Il rallentamento (un fotogramma sorgente per fotogramma d'uscita) vale fino a 1,25x l'uscita; oltre, velocità normale.

**Anteprima da approvare**: `./mve finale <slug> --anteprima` → `renders/<slug>_anteprima.mp4` (960x540, intera, con grafica e suono), `controlli/anteprima.jpg` (un fotogramma per elemento), `controlli/anteprima-tempi.md` (dove compare ogni elemento), `controlli/contenuto.md` (controlli di contenuto). MR_POSTURA_01_v2: 16 s.

## Verifica (sul file consegnato)

`qc` controlla il master, non i dati, più i controlli di contenuto (B-roll solo fra le utilizzabili, testo a schermo detto o etichetta dichiarata, materiali vietati, SRT completo, nessun pannello sulla testa): codec, frame rate del progetto, tag e range colore, frame contro EDL, durata audio, loudness, true peak, frame neri, immagine ferma, card sul volto, sagome, copertura dei sottotitoli, **parole tagliate alle giunte** (energia nel tratto buttato, sopra), e **riascolta tutte le giunte sul file finale** con sonde da 4 s. Esce `controlli/QC.md` con CONSEGNABILE o NON CONSEGNABILE.

## Ingresso, stato e tempi (v1.0, 02/11/2026)

- `init inbox/<NOME>/` legge anche `info.txt` (righe `osteopata: Nome Cognome`,
  `tipo: YouTube` o `tipo: mid-roll`, facoltativo `ruolo: ...`) e lo mette in
  `meta.json → info`; non lo scambia per il copione. Se manca qualcosa lo dice:
  si chiede prima di andare avanti. Il tipo decide la consegna (`Progetto.tipo`;
  `regia.json → tipo` vince su info.txt).
- `./mve stato` **senza slug**: video, cartelle di inbox con quello che manca,
  strumenti, RAM, disco, B-roll da catalogare. Non scrive niente.
- Ogni fase che cambia un video aggiunge una riga a `videos/<slug>/tempi.md`:
  durata, esito, spazio della cartella del video e di `.lavoro`, disco libero.
- `./mve libreria` con `libreria/broll/` vuota non fallisce; `libreria.da_catalogare()`
  elenca le clip nuove o senza descrizione (prima di scegliere un B-roll vanno
  catalogate); senza indice `utilizzabili()` non restituisce niente.

## Ambiente

Cosa c'è e cosa manca su questa macchina, RAM e lavori in parallelo, spazio disco:
`references/ambiente.md`.

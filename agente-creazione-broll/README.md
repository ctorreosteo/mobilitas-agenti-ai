# Agente creazione B-roll — Higgsfield (Mobilitas / OsteoTouch)

Da uno **script pubblicitario** ai **B-roll montabili**: l'agente legge il copy, decide
dove servono le immagini, scrive i prompt, li collauda, stima il costo e — solo dopo
autorizzazione — genera davvero immagini e video chiamando l'API di Higgsfield.

## I due tipi di B-roll

| | **Riconoscimento** | **Comprensione** |
|---|---|---|
| Dove | sezione Hook + Pain Point | sezione Meccanismo Unico |
| Cosa fa | lo spettatore vede sé stesso e smette di valutare il video | rende visibile una relazione che a parole costerebbe venti secondi |
| Come | persone reali, dettagli di gesto, oggetti, ambienti | infografiche 3D anatomiche con la palette Mobilitas |
| Skill | `broll-pain-point` | `broll-infografica-meccanismo` |

Sopra entrambi c'è una regola che vale sempre: **il protagonista ha fra i 40 e i 60 anni**
(il pubblico va dai 35, ma si rappresenta il centro del bersaglio),
è vestito nella via di mezzo fra il professionale e il domestico, e la scena **dimostra**
una proposizione invece di illustrare il parlato. Le tre cose insieme decidono se il video
parla al pubblico che paga.

Sono due mestieri diversi. Il primo vive di verosimiglianza quotidiana, il secondo di
gerarchia visiva e prudenza sui claim medici. Tenerli in una skill sola produce
infografiche sentimentali e pain point didattici.

---

## Struttura

```
.env                                   LE TUE CHIAVI. Escluso da git, permessi 600
.env.esempio                           modello vuoto, versionato: dice quali variabili servono

.claude/skills/                        skill di progetto (attive lavorando in questa cartella)
  broll-modelli-higgsfield/            FASE 1 — quale AI, a quale prezzo
    ├─ SKILL.md
    └─ references/api-higgsfield.md       il contratto API verificato: endpoint, errori, costi
  broll-regia-editoriale/              FASE 3 — DOVE vanno i b-roll, quanti, che genere, che formato
    └─ SKILL.md
  broll-pain-point/                    FASE 4a — i prompt delle scene con persone
    ├─ SKILL.md
    └─ references/casting-e-guardaroba.md
  broll-infografica-meccanismo/        FASE 4b — i prompt delle infografiche
    ├─ SKILL.md
    └─ references/brand-system.md         palette, luce, vincoli negativi: formule da copiare

scripts/
  higgsfield.py                        il client API: stima, genera, riprende
  verifica_modelli.py                  controlla il catalogo contro la documentazione viva

broll-generati/
  _dati/modelli-higgsfield.json        catalogo dei modelli, costi, motivo della scelta
  _dati/citta.json                     Torino, Milano, Roma: landmark, tessuto, interni, luce
  _dati/registro-prompt.md             cosa hanno insegnato i video già girati
  _workflow/genera-broll.workflow.js
  <slug>/piano.json                    il piano eseguibile: un prompt per generazione

outputs/<slug>/
  immagini/  video/                    i file scaricati
  stato.json                           cosa è già stato chiesto e cosa è già arrivato
  manifest.json  stima.json  INDICE.md
```

---

## Come si lancia

```js
Workflow({ scriptPath: 'broll-generati/_workflow/genera-broll.workflow.js', args: {
  slug: 'lombalgia-settembre',
  script: '/percorso/allo/script.md',
  citta: 'torino',
  quote: { pain: 1, meccanismo: 2 },
  modelli: { immagine: 'soul-2', video: 'kling-3-std-i2v' },
  genere: 'entrambi',
  solo_immagini: false,
  autorizza_spesa: false
}})
```

Obbligatori solo `slug` e `script`. Tutto il resto ha un default, e ogni campo facoltativo
è un pezzo di decisione che togli all'agente:

| Campo | Se lo ometti |
|---|---|
| `citta` | **Torino**, che è il predefinito di `citta.json`. Non esiste il caso «nessuna città» |
| `quote` | il numero di b-roll lo decide la regia, con il minimum effective visual set |
| `modelli` | si usano i predefiniti del catalogo |
| `genere` | lo deduce dalla condizione |
| `solo_immagini` | genera anche i video |
| `autorizza_spesa` | **si ferma dopo la stima**: nessun credito speso |
| `provini` | 4 estrazioni per b-roll, fra cui il giudice sceglie. Con `1` si torna al tiro singolo |

### Il cancello della spesa

`autorizza_spesa: false` è il predefinito, ed è voluto. Il workflow arriva fino alla stima
e si ferma mostrando quanto costerebbe, con i numeri veri dell'endpoint `/estimate` sul
tuo account. Solo un secondo lancio con `true` genera davvero.

Il modo più economico di lavorare è in due tempi:

1. `autorizza_spesa: true, solo_immagini: true` — genera le sole immagini, che costano una
   frazione dei video. Guardale.
2. Correggi i prompt che non reggono e rilancia senza `solo_immagini`. Le immagini già
   scaricate non si ripagano.

---

## Le undici fasi

1. **Modelli** — quale AI per le immagini, quale per i video. Se il catalogo ha più di
   trenta giorni, `verifica_modelli.py` controlla che gli endpoint esistano ancora e
   segnala i modelli nuovi. La scelta si può imporre al lancio.
2. **Strategia** — un **marketer strategico** legge lo script e decide **cosa ogni scena
   deve dimostrare** perché qualcuno prenoti: la proposizione, non il soggetto. Il suo
   vincolo è **polarizzare**: per ogni momento deve saper dire chi si riconosce in modo
   violento e chi capisce che non lo riguarda, e se non esclude nessuno la scena è generica
   e va rifatta. Lavora dai **pain point specifici** — non «colon irritabile», che è una
   diagnosi, ma cosa quella persona non può più fare, a cosa rinuncia, cosa nasconde — e
   sceglie **un momento datato** della giornata, con il dettaglio privato che il target fa
   e non racconta a nessuno. Restituisce i momenti **in ordine di valore commerciale**: se
   la quota è 1, si compra il primo. Viene prima della regia di proposito: il regista sa
   dove si perde l'attenzione, non sa cosa conviene dimostrare per vendere.
3. **Regia** — un regista editoriale (marketing, vendita, copywriting, montaggio) legge lo
   script e decide **dove** i b-roll comprano attenzione, quanti, di che tipo, con quale
   genere e in quale formato. Produce anche la lista dei passaggi che **restano sul volto
   dell'osteopata**, che è la parte più informativa del piano.
4. **Prompt** — **un sottoagente per ogni b-roll, in parallelo.** Ognuno riceve un incarico
   già circoscritto e restituisce prompt T2I e I2V più i parametri.
5. **Collaudo** — un revisore guarda la **sequenza intera** prima che parta un solo credito:
   ridondanza, continuità del personaggio, claim gonfiati, palette, simmetria delle varianti,
   lunghezza dei prompt, formato, durate, testo generato. Un giro di riparazione chirurgica.
6. **Piano** — scrive `piano.json`: una riga per generazione, con le varianti già espanse.
7. **Stima** — costo reale, per b-roll e totale.
8. **Provini** — **più estrazioni della stessa scena, solo immagini.** Un'immagine costa
   ~0,006 USD e un video ~0,32: il video è il **98% del costo**. Ogni generazione è
   un'estrazione a sé, e giudicare una scena su una sola estrazione è il modo più caro di
   sbagliare. Quante ne fa lo decide `provini` (4 di default, 1 per disattivarle).
9. **Selezione** — un giudice **guarda** i provini e sceglie. Deve dare un motivo per ogni
   scartato (un provino senza motivo è un provino che non ha aperto) e dichiarare i difetti
   residui del vincitore invece di nasconderli. Se tutti hanno un difetto bloccante dice
   `nessuno_accettabile` e **il video non si paga**. Il vincitore viene messo al posto giusto
   su disco, così la fase dopo salta l'immagine e paga solo il video.
10. **Generazione** — il client chiama l'API con pool di worker che rispetta il limite di
   concorrenza dell'account.
11. **Consegna** — `INDICE.md` con l'ordine di montaggio, e i numeri **contati sul disco**,
   non dichiarati dagli agenti.

---

## Le regole che governano il piano

### La regola d'apertura

**Sulla prima frase del video non va mai un B-roll.** Resta sul volto, sempre, e il primo
b-roll entra dalla seconda frase in poi.

Nel primo secondo lo spettatore non valuta il contenuto: classifica il video. Se il primo
fotogramma è una scena costruita lo archivia come pubblicità e scorre prima di aver sentito
l'hook. Se è una persona che parla, resta abbastanza da ascoltare la prima frase — ed è la
frase che deve fermarlo, non l'immagine.

Non è una raccomandazione affidata alla buona volontà di un agente: il workflow la **verifica
contando**. Il piano dichiara la prima frase alla lettera, e se un b-roll la copre il piano
torna indietro alla regia con scritto quale. Se al secondo giro la viola ancora, il workflow
si ferma prima di spendere.

### Genere del protagonista

Si guarda la **condizione**, non il tono dello script.

- Condizione femminile (ciclo doloroso, endometriosi, gravidanza, menopausa, cicatrice da
  cesareo) → tutti i b-roll con donne.
- Condizione maschile (prostatite, varicocele) → tutti con uomini.
- Condizione di entrambi (lombalgia, cervicalgia, reflusso, acufeni, cefalea…) → **ogni
  b-roll con persone si genera in due versioni**, donna e uomo, identiche in tutto il resto.

Una prevalenza non è un'esclusiva: l'emicrania colpisce più donne e resta `entrambi`.

### Chi si vede in scena

Tre vincoli che valgono su ogni video e che il collaudo verifica uno per uno.

**Età: pubblico 35-60, in scena sempre 40-60.** Si rappresenta il centro del bersaglio, non
il suo bordo più giovane. È il pubblico che paga — chi convive con il problema da anni,
ha un lavoro, una famiglia e i soldi per un trattamento. Un protagonista più giovane sposta
il video su chi non prenota e fa leggere il problema come passeggero, che è esattamente
l'obiezione da disinnescare. Si scrive come numero (`a 52-year-old Italian woman`), perché
«middle-aged» produce trentacinquenni.

**Guardaroba: la via di mezzo.** Né tuta né completo: una persona curata in una giornata
normale, che fra un'ora esce di casa. L'errore controintuitivo è vestire male il
protagonista pensando di renderlo più vero: legge come persona che si è arresa, e una
persona arresa non è credibile come qualcuno che prenoterà. L'identificazione la dà la
situazione, non il degrado — il dolore si legge da postura, viso e luce.

**La casa è il secondo costume.** Uno sfondo piatto o anonimo abbassa il ceto percepito
quanto un capo sbagliato. Dietro il soggetto ci vuole qualcosa da guardare a fuoco morbido,
e quando la città deve vedersi il posto è la finestra: tessuto urbano sfocato ma leggibile.

E una regola sugli oggetti: **ognuno deve dimostrare qualcosa.** Un oggetto che non c'entra
con gli altri non è «vissuto», è disordine, e il disordine incoerente è uno dei segnali più
forti che l'immagine è generata.

### Formato

`9:16` in tutti i casi, **`16:9` quando il genere è `entrambi`**. È una regola di Carlos, e
il workflow la impone: se la regia scrive il formato sbagliato, viene corretto e lo dice.

Il formato non è un bordo, è una composizione. In verticale il soggetto occupa l'altezza e
l'ambiente si legge per frammenti; in orizzontale il soggetto si decentra e l'ambiente
racconta con lui. Le skill lo scrivono dentro il prompt.

### Città

**Il predefinito è Torino**, e non esiste il caso «nessuna città»: se al lancio non si passa
niente, vale il campo `predefinita` di `citta.json`. Un video Mobilitas è ambientato a
Torino salvo indicazione contraria.

La città entra su **due livelli, che si decidono separatamente**:

**Gli interni: sempre.** Case, uffici, auto, locali seguono il campo `interni` in *ogni*
b-roll, anche in quelli dove dalla finestra non si vede niente. È la parte che i modelli
sbagliano più spesso, perché ricadono sull'interno americano — e un ambiente non descritto
viene riempito da quel default. Vietare il disordine non basta a costruire un set.

**Gli esterni: dove uno sfondo si vede davvero.** È quello che dichiara `citta_visibile`:
una finestra, una vetrata, un parabrezza, una strada, un terrazzo. Una finestra che dà su
un muro anonimo è un'occasione buttata.

Sugli esterni il livello che funziona non sono i landmark ma il **tessuto**: intonaci ocra
e persiane verdi, portici, platani, tram che passa sfocato. Chi vive lì si riconosce, chi
non ci vive non nota niente di strano.

**Massimo un landmark riconoscibile per video.** Due sono promozione turistica, e spostano
il registro da «questa è la mia vita» a «questa è una pubblicità». Per Torino: Mole, Monte
dei Cappuccini, Superga, piazza San Carlo, via Roma, Gran Madre, piazza Vittorio, Valentino,
Murazzi.

### Prudenza sui claim

Il vincolo che viene prima di tutto nelle infografiche: **la rappresentazione non può
rendere l'affermazione medica più forte del copy.** «Può essere collegato a» si disegna
come relazione, non come causa. La tensione si disegna come coinvolgimento muscolare e
mobilità ridotta, mai come infiammazione, compressione o danno. Ogni infografica porta un
campo `prudenza_claim` che dice cosa afferma il copy e cosa è stato rappresentato: è la
riga che rende il controllo verificabile invece che dichiarato.

---

## Cosa serve per generare davvero

Le chiavi si creano su [console.higgsfield.ai](https://console.higgsfield.ai), sezione API
keys. Higgsfield ne dà due: un **ID** e un **segreto**.

Vanno nel file **`.env`** dentro questa cartella, già pronto con i due campi vuoti. Il client
lo legge da solo: non devi esportare niente a mano.

Il file è **escluso da git** (`.gitignore` alla radice del repo) e ha permessi `600`, cioè
leggibile solo dal tuo utente. Accanto c'è `.env.esempio`, versionato e sempre vuoto: serve
solo a documentare quali variabili servono. Se una chiave è anche nelle variabili d'ambiente,
quella vince — comodo per provare una chiave diversa senza toccare il file.

Verifica che siano arrivate:

```bash
python3 scripts/higgsfield.py credenziali
```

Ti dice se le ha trovate e **da dove**, e non stampa mai il segreto.

Il segreto si vede **una volta sola**, al momento della creazione. Se lo perdi non si
recupera: si crea una chiave nuova e si cancella la vecchia.

### Tre cose dell'API che cambiano il modo di lavorare

- **Le generazioni illimitate dell'abbonamento non valgono sull'API.** Si applicano solo a
  `higgsfield.ai`. Ogni chiamata qui consuma crediti acquistati a parte, che scadono dopo
  un anno. È il motivo per cui la stima è obbligatoria e il cancello della spesa è chiuso
  di default.
- **Le POST di generazione non hanno idempotenza.** Dopo un timeout ambiguo, ripetere la
  richiesta rischia di pagare due volte. Il client scrive il `request_id` su disco *prima*
  di iniziare il polling, e una ripresa interroga quello invece di inviarne uno nuovo.
- **Gli output restano sul CDN almeno sette giorni**, poi possono sparire. Il client scarica
  sempre: `outputs/<slug>/` è l'archivio vero.

---

## Nano Banana Pro: perché non è il predefinito

Verificato il **2026-09-29**: Nano Banana Pro **non ha un endpoint API su Higgsfield**.
Compare nel generatore del sito e nei piani a consumo di `higgsfield.ai`, non nel catalogo
di `docs.higgsfield.ai`. I modelli immagine esposti via API sono SOUL / SOUL V2 / SOUL
Cinema / Soul ID, Marketing Studio Image, Grok Image 2, Recraft V4.1, Qwen Image 3,
Ideogram 4, Z-Image Turbo.

Il catalogo lo registra comunque, con `disponibile_su_api: false`, il motivo scritto per
esteso e i suoi punti di forza. Il client **rifiuta** di inviargli richieste e dice perché.
`verifica_modelli.py` ricontrolla a ogni scadenza: appena compare un endpoint, il flag si
ribalta e diventa il candidato naturale per le infografiche — è il modello che ragiona sul
prompt prima di disegnare, che è esattamente ciò che serve a un'anatomia con una gerarchia.

Kling 3.0 invece c'è, in tre varianti (Standard, Pro, Turbo), ed è il predefinito video. Il
motivo per cui non si usa Google VEO è scritto nel catalogo, nel campo `perche_non_veo`:
non produce il realismo che serve, e su un pain point la credibilità è tutto il lavoro.

---

## Manutenzione

```bash
python3 scripts/verifica_modelli.py     # gli endpoint esistono ancora? cosa c'è di nuovo?
```

Lo script **referta, non aggiorna**. Il catalogo autorevole sta in console, dietro account:
l'assenza di un modello dalla documentazione pubblica non prova che non esista. Le modifiche
a `modelli-higgsfield.json` le decide Carlos.

Il `registro-prompt.md` accumula quello che i video girati hanno insegnato: i difetti
ricorrenti diventano **correzioni attive**, e regista e prompt writer le leggono prima di
lavorare. La promozione da osservazione a correzione è umana.

## Note operative

- Le skill sono **project-scoped**: valgono solo dentro questa cartella.
- Il `name:` in ogni `SKILL.md` combacia col nome della cartella.
- Le skill si caricano all'avvio sessione: dopo modifiche strutturali **riavvia la sessione**.
- `piano.json` è un artefatto leggibile e modificabile a mano: si può correggere un prompt e
  rilanciare solo il client, senza rifare il workflow.

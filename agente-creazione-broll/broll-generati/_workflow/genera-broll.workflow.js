export const meta = {
  name: 'genera-broll-higgsfield',
  description: 'Da uno script pubblicitario ai B-roll montabili: sceglie i modelli AI su Higgsfield al miglior rapporto resa/prezzo, fa decidere a un regista editoriale dove e quanti b-roll servono, scrive i prompt con un sottoagente in parallelo per ogni b-roll (pain point con persone, meccanismo con infografiche), li collauda PRIMA di spendere, stima il costo, e solo dopo autorizzazione genera immagini e video via API. Riprendibile: una generazione interrotta non ripaga quello che ha gia ottenuto',
  whenToUse: 'Trasforma lo script di una pubblicita Mobilitas nella sua sequenza di B-roll su Higgsfield',
  phases: [
    { title: 'Modelli', detail: 'quale AI per le immagini e quale per i video, al costo minore' },
    { title: 'Strategia', detail: 'un marketer decide cosa la scena deve DIMOSTRARE, prima che qualcuno la immagini' },
    { title: 'Regia', detail: 'dove vanno i b-roll, quanti, genere del protagonista, formato' },
    { title: 'Prompt', detail: 'un sottoagente per ogni b-roll, in parallelo: T2I + I2V' },
    { title: 'Collaudo', detail: 'la sequenza regge? cancello PRIMA di spendere crediti' },
    { title: 'Piano', detail: 'scrive piano.json, il file che il client esegue' },
    { title: 'Stima', detail: 'quanto costa, con i numeri veri di /estimate' },
    { title: 'Provini', detail: 'piu estrazioni della stessa scena, SOLO immagini: costano un centesimo di un video' },
    { title: 'Selezione', detail: 'un giudice guarda i provini e sceglie, prima che parta un solo video' },
    { title: 'Generazione', detail: 'immagini e video via API, con ripresa dallo stato su disco' },
    { title: 'Consegna', detail: 'indice di montaggio e verifica dei file sul disco' },
  ],
}

// ---- percorsi assoluti: i subagent non ereditano la working dir ----
const ROOT = '/Users/carlitos/mobilitas-agenti-ai/agente-creazione-broll'
const SK = ROOT + '/.claude/skills'
const OUT = ROOT + '/broll-generati'
const DATI = OUT + '/_dati'
const CATALOGO = DATI + '/modelli-higgsfield.json'
const CITTA = DATI + '/citta.json'
const REGISTRO = DATI + '/registro-prompt.md'
const CLIENT = ROOT + '/scripts/higgsfield.py'

const RETRIES = 3

// ============================ SCHEMI ============================

const MODELLI_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['immagine', 'video', 'perche'],
  properties: {
    immagine: { type: 'string', description: 'chiave del modello immagine dal catalogo' },
    video: { type: 'string', description: 'chiave del modello video dal catalogo' },
    perche: { type: 'string' },
    catalogo_scaduto: { type: 'boolean' },
    giorni_dall_aggiornamento: { type: 'number' },
    verifica_endpoint: { type: 'string' },
    proposte_di_aggiornamento: { type: 'array', items: { type: 'string' } },
    avvertenze: { type: 'array', items: { type: 'string' } },
  },
}

const STRATEGIA_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['promessa', 'target', 'momenti', 'cosa_non_mostrare'],
  properties: {
    promessa: { type: 'string', description: 'cosa compra davvero chi guarda: non la prestazione, il cambiamento di vita' },
    target: {
      type: 'object', additionalProperties: false,
      required: ['eta_pubblico', 'eta_in_scena', 'autoimmagine', 'pain_points'],
      properties: {
        eta_pubblico: { type: 'string', description: 'chi guarda. Per Mobilitas: 35-60 anni.' },
        eta_in_scena: { type: 'string', description: 'chi si vede. Per Mobilitas: SEMPRE 40-60 anni, il centro del bersaglio e non il suo bordo giovane.' },
        situazione: { type: 'string', description: 'vita reale: lavoro, famiglia, cosa la condizione gli impedisce' },
        autoimmagine: { type: 'string', description: 'come questa persona vuole vedersi rappresentata. Decide guardaroba e casa.' },
        pain_points: {
          type: 'array',
          description: 'i dolori SPECIFICI di questa condizione in questa fascia d eta. Non "sta male": cosa non puo piu fare, cosa rinuncia, cosa nasconde, cosa teme che gli altri pensino.',
          items: { type: 'string' },
        },
        nemico: { type: 'string', description: 'a cosa o a chi il target da la colpa oggi: la dieta, i medici, se stesso, lo stress' },
        obiezione: { type: 'string', description: 'la frase che si dice per NON prenotare' },
      },
    },
    momenti: {
      type: 'array',
      description: 'i punti dello script a piu alta leva commerciale, IN ORDINE DI VALORE. Il primo e quello che si compra per primo se la quota e 1.',
      items: {
        type: 'object', additionalProperties: false,
        required: ['frase', 'scena_quotidiana', 'cosa_deve_dimostrare', 'chi_dice_sono_io', 'chi_si_esclude'],
        properties: {
          frase: { type: 'string', description: 'la frase dello script, alla lettera' },
          scena_quotidiana: { type: 'string', description: 'UN momento concreto e datato della giornata del target: ora, luogo, decisione. Non uno stato d animo, non un sintomo.' },
          dettaglio_privato: { type: 'string', description: 'la cosa che il target FA ma non racconta a nessuno. E il dettaglio che produce "come fanno a saperlo".' },
          cosa_deve_dimostrare: { type: 'string', description: 'la PROPOSIZIONE che l immagine rende innegabile. Non un soggetto, un argomento.' },
          chi_dice_sono_io: { type: 'string', description: 'chi, vedendola, si riconosce in modo violento' },
          chi_si_esclude: { type: 'string', description: 'chi, vedendola, capisce che non lo riguarda. Se non escludi nessuno, la scena non polarizza e non vale niente.' },
          perche_vende: { type: 'string', description: 'cosa succede nella testa di chi guarda, in termini di decisione d acquisto' },
          prova_visiva: { type: 'string', description: 'l oggetto, il gesto o la situazione che PROVA la proposizione senza dirla' },
          da_evitare: { type: 'string', description: 'la versione ovvia, generica e muta della stessa scena' },
        },
      },
    },
    cosa_non_mostrare: { type: 'array', items: { type: 'string' }, description: 'scene che indebolirebbero la vendita, e perche' },
    registro_sociale: { type: 'string', description: 'come deve apparire la persona: ceto, cura di se, casa. La via di mezzo fra il professionale e il domestico.' },
    avvertenze: { type: 'array', items: { type: 'string' } },
  },
}

const PIANO_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['genere', 'aspect_ratio', 'broll', 'prima_frase'],
  properties: {
    condizione: { type: 'string' },
    genere: { type: 'string', enum: ['donna', 'uomo', 'entrambi'] },
    motivo_genere: { type: 'string' },
    aspect_ratio: { type: 'string', enum: ['9:16', '16:9'] },
    citta: { type: ['string', 'null'] },
    idea_centrale: { type: 'string' },
    prima_frase: { type: 'string', description: 'La prima frase dello script, ALLA LETTERA. Non puo essere coperta da nessun b-roll.' },
    progressione: { type: 'string' },
    personaggio: {
      type: 'object', additionalProperties: false,
      properties: {
        descrizione_fissa: { type: 'string' },
        serve_soul_id: { type: 'boolean' },
      },
    },
    broll: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['id', 'tipo', 'copre', 'funzione', 'secondi', 'varianti'],
        properties: {
          id: { type: 'string', description: 'NN-tipo-parolachiave, senza spazi ne accenti: diventa il nome del file' },
          tipo: { type: 'string', enum: ['pain', 'infografica'] },
          copre: { type: 'string' },
          posizione: { type: 'string' },
          funzione: { type: 'string' },
          perche_qui: { type: 'string' },
          secondi: { type: 'number', description: 'fra 3 e 15: limite di Kling' },
          varianti: { type: 'array', items: { type: 'string', enum: ['donna', 'uomo', 'unica'] } },
          citta_visibile: { type: 'boolean' },
          note_per_lo_specialista: { type: 'string' },
        },
      },
    },
    senza_broll: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['passaggio', 'perche'],
        properties: { passaggio: { type: 'string' }, perche: { type: 'string' } },
      },
    },
    avvertenze: { type: 'array', items: { type: 'string' } },
  },
}

const BROLL_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['id', 'prompt_t2i', 'prompt_i2v', 'durata'],
  properties: {
    id: { type: 'string' },
    tipo_broll: { type: 'string' },
    beat: { type: 'string' },
    copre: { type: 'string' },
    cosa_deve_provare_lo_spettatore: { type: 'string' },
    cosa_deve_capire_lo_spettatore: { type: 'string' },
    prompt_t2i: {
      type: 'object', additionalProperties: false,
      description: 'UNA chiave "unica", oppure le due chiavi "donna" e "uomo". Mai altre combinazioni.',
      properties: {
        unica: { type: 'string' },
        donna: { type: 'string' },
        uomo: { type: 'string' },
      },
    },
    prompt_i2v: { type: 'string', description: 'in inglese, 70-160 parole, mai oltre 2500 caratteri' },
    durata: { type: 'number' },
    citta_usata: { type: 'string' },
    prudenza_claim: { type: 'string', description: 'solo per le infografiche: cosa dice il copy e cosa hai rappresentato' },
    osservazioni: { type: 'array', items: { type: 'string' } },
  },
}

const PROVINI_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['gruppi'],
  properties: {
    gruppi: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['id', 'file'],
        properties: {
          id: { type: 'string', description: 'id del b-roll ORIGINALE, senza il suffisso --pN' },
          file: { type: 'array', items: { type: 'string' }, description: 'percorsi assoluti dei provini arrivati' },
        },
      },
    },
    mancanti: { type: 'array', items: { type: 'string' } },
  },
}

const SCELTA_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['vincitore', 'perche', 'scartati'],
  properties: {
    vincitore: { type: 'string', description: 'id del provino scelto, esattamente come si chiama il file senza estensione' },
    perche: { type: 'string', description: 'cosa ha questo che gli altri non hanno, in termini di cosa la scena deve dimostrare' },
    difetti_residui: { type: 'array', items: { type: 'string' }, description: 'cosa resta storto anche nel vincitore: va nell indice, non nascosto' },
    scartati: {
      type: 'array',
      description: 'ogni altro provino con il motivo dello scarto. Un provino senza motivo non e stato guardato.',
      items: {
        type: 'object', additionalProperties: false,
        required: ['id', 'motivo'],
        properties: { id: { type: 'string' }, motivo: { type: 'string' } },
      },
    },
    nessuno_accettabile: { type: 'boolean', description: 'true se TUTTI hanno un difetto bloccante: allora non si spende il video' },
  },
}

const COLLAUDO_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['esito', 'bloccanti'],
  properties: {
    esito: { type: 'string', enum: ['PRONTO', 'DA_CORREGGERE', 'DA_RIFARE'] },
    bloccanti: {
      type: 'array',
      description: 'Vuoto = si puo spendere. Ogni voce e una correzione da fare PRIMA di pagare.',
      items: {
        type: 'object', additionalProperties: false,
        required: ['id', 'tipo', 'correzione'],
        properties: {
          id: { type: 'string' },
          tipo: { type: 'string', description: 'RIDONDANZA / DISCONTINUITA_PERSONAGGIO / CLAIM_GONFIATO / PALETTE_VIOLATA / VARIANTI_ASIMMETRICHE / CHIAVI_SBAGLIATE / PROMPT_TROPPO_LUNGO / FORMATO_IGNORATO / DURATA_FUORI_LIMITE / TESTO_GENERATO / PRIMA_FRASE_COPERTA / ETA_FUORI_TARGET / REGISTRO_SOCIALE_SBAGLIATO / PROP_INCOERENTE / SCENA_CHE_ILLUSTRA / SCENA_GENERICA / CITTA_ASSENTE / COMPOSIZIONE_A_FASCE' },
          problema: { type: 'string' },
          correzione: { type: 'string', description: 'istruzione chirurgica, non una riscrittura' },
        },
      },
    },
    avvisi: { type: 'array', items: { type: 'string' } },
    giudizio: { type: 'string', description: 'una frase: la sequenza racconta una storia o e una raccolta di immagini?' },
  },
}

// ============================ PROMPT ============================

const modelliPrompt = (a) => `Devi scegliere i modelli di intelligenza artificiale con cui generare questo video su Higgsfield.

1. Leggi ${SK}/broll-modelli-higgsfield/SKILL.md e ${SK}/broll-modelli-higgsfield/references/api-higgsfield.md.
2. Leggi il catalogo ${CATALOGO}.
${a.modelli ? `3. Carlos ha INDICATO i modelli al lancio: immagine="${a.modelli.immagine || 'non indicato'}", video="${a.modelli.video || 'non indicato'}". Quelli indicati SI USANO: non discutere la scelta. Verifica solo che esistano nel catalogo, che abbiano disponibile_su_api=true e che supportino il formato. Se un controllo fallisce, dillo esplicitamente in avvertenze e proponi il ripiego. Per i modelli NON indicati, scegli tu.` : '3. Carlos non ha indicato modelli: scegli tu dai predefiniti del catalogo, valutando il tipo di b-roll che questo video richiede.'}
4. Guarda "aggiornato_il" e "scadenza_giorni". Se il catalogo e SCADUTO, esegui:
   python3 ${ROOT}/scripts/verifica_modelli.py
   e riporta l'esito in verifica_endpoint. Se trovi modelli nuovi piu adatti o endpoint spariti, mettili in proposte_di_aggiornamento CON IL MOTIVO. NON modificare il file: la decisione e di Carlos.

Questo video: ${a.descrizione}

Restituisci l'oggetto strutturato.`

const registraPrompt = () => `Leggi ${REGISTRO} (se esiste) e riporta in una riga le "Correzioni attive": sono difetti di prompt gia trovati su video precedenti. Se il file non esiste, rispondi "nessun registro".`

const strategiaPrompt = (a, scriptPath) => `Sei il marketer strategico di Mobilitas. Arrivi PRIMA del regista, e decidi una cosa sola: che lavoro commerciale deve fare l immagine.

Non scegli inquadrature e non scrivi prompt. Stabilisci **cosa la scena deve DIMOSTRARE** perche qualcuno prenoti.

## Lo script
${scriptPath}
Leggilo tutto, comprese le sezioni meccanismo, desiderio e CTA: la scena del pain deve preparare la vendita che avviene dopo.

## LA REGOLA CHE GOVERNA TUTTO IL TUO LAVORO: POLARIZZA

Una scena che piace a tutti non serve a nessuno. Se chiunque, guardandola, pensa "eh si,
capita", non hai fatto marketing: hai fatto una fotografia.

Per ogni momento devi poter dire **chi si riconosce in modo violento** e **chi capisce che non
lo riguarda**. Compila tutti e due i campi. Se non riesci a nominare qualcuno che si esclude,
la scena e generica e va rifatta: stai descrivendo un essere umano stanco, non il nostro target.

La misura di una buona scena e una sola: chi la guarda deve pensare **"come fanno a saperlo"**.
Quella reazione non nasce dalla rappresentazione del sintomo. Nasce da un dettaglio della
giornata che il target riconosce come proprio e che non ha mai raccontato a nessuno.

## COME SI TROVA QUELLA SCENA — il metodo, non l ispirazione

**1. Parti dai pain point specifici, non dalla condizione.**
"Colon irritabile" non e un pain point: e una diagnosi. I pain point sono cosa quella persona
non puo piu fare, a cosa rinuncia, cosa nasconde, cosa teme che gli altri pensino di lei.
Elencane almeno quattro nel campo "pain_points", e che siano di QUESTA fascia d eta: a
quarantacinque anni si rinuncia a cose diverse che a venticinque.

**2. Cerca la conseguenza sulla vita, non il sintomo.**
Il sintomo lo vedono tutti e non vende: e medicina. La conseguenza sociale, lavorativa e
famigliare vende, perche e quella che fa male davvero e che nessuno ha mai nominato ad alta voce.
Il dolore fisico e cio che il paziente racconta al medico. Quello che non racconta a nessuno e
la rinuncia.

**3. Scegli UN momento datato, non uno stato d animo.**
Un'ora, un luogo, una decisione. "Il momento in cui, prima di accettare l invito, controlla
mentalmente dove sono i bagni" e una scena. "Una donna che si sente in ansia" non lo e: non si
puo nemmeno inquadrare.

**4. Trova il dettaglio privato.**
La cosa che il target FA e non dice. E il gesto piccolo, la precauzione, la bugia sociale, la
cosa tenuta in borsa. E quasi sempre li che sta la scena piu forte del video, ed e quasi sempre
la cosa che nessun concorrente sta mostrando perche sembra troppo piccola.

**5. Verifica che non sia illustrazione.**
Una scena che ILLUSTRA il parlato non vende: raddoppia l audio e si puo togliere senza perdere
niente. Una scena che DIMOSTRA fa un'affermazione che la voce non sta facendo, e che chi guarda
accetta perche la vede invece di sentirsela dire.
Scrivi la PROPOSIZIONE, non il soggetto. Non "una donna stanca a tavola": "ci ha provato per
mesi, con metodo, e non e servito — quindi non e colpa sua e non e pigrizia".

## Ordine dei momenti
IN ORDINE DI VALORE COMMERCIALE. Se la quota fosse 1, si compra il primo.
Il beat che tocca la **vita sociale** — quello che fa perdere occasioni, non quello che fa male —
di solito vende piu del sintomo: valutalo davvero prima di scartarlo. La vergogna vende piu del
dolore, perche il dolore si sopporta e la vergogna no.

## Il target Mobilitas — non negoziabile
- **Chi guarda: 35-60 anni.**
- **Chi si vede in scena: SEMPRE 40-60 anni.** Si rappresenta il centro del bersaglio, non il suo
  bordo piu giovane. Chi paga un trattamento convive con il problema da anni, ha un lavoro, una
  famiglia e dei soldi. Un protagonista piu giovane fa leggere il problema come passeggero —
  "passera" — che e esattamente l obiezione da disinnescare.

Compila "autoimmagine" pensando a come questa persona vuole essere rappresentata. Nessuno si
riconosce volentieri in qualcuno piu trasandato di come si vede: una persona che si lascia
andare non e credibile come qualcuno che PROVERA a risolvere. L identificazione la da la
situazione, non il degrado.

Compila "registro_sociale" con la via di mezzo fra il professionale e il domestico: una persona
che fra un ora esce di casa, non una in tuta sul divano e nemmeno una in completo.

Compila "nemico" con cio a cui il target da la colpa oggi. E la cosa contro cui il video prende
posizione, ed e meta della polarizzazione.

## Quota che il regista dovra rispettare
${a.quote ? JSON.stringify(a.quote) : 'non fissata: il regista decidera'}
Proponi comunque i momenti in ordine: il regista taglia dalla coda.

## Cosa NON mostrare
Elenca le scene che indebolirebbero la vendita: quelle che fanno pena invece che riconoscere,
quelle che rispondono a una domanda che deve restare aperta fino al meccanismo, quelle che
spostano il registro su malattia grave o su pubblicita, e quelle cosi generiche che varrebbero
per qualunque condizione.

Restituisci l oggetto strutturato.`

const regiaPrompt = (a, scriptPath, strat) => `Sei il regista editoriale di una pubblicita Mobilitas. Devi decidere DOVE mettere i B-roll, quanti, di che tipo, con quale genere del protagonista e in quale formato.

## Istruzioni della skill — leggile e seguile INTEGRALMENTE
${SK}/broll-regia-editoriale/SKILL.md

## Lo script
${scriptPath}
Leggilo tutto. Se contiene le sezioni [HOOK + PAIN], [OSTEOPATA - MECCANISMO UNICO], [OSTEOPATA - DESIDERIO], [OSTEOPATA - CTA], analizzale tutte per capire la logica, ma progetta b-roll SOLO per pain point e meccanismo, salvo che una scena di desiderio prima della CTA guadagni davvero il suo posto.

## Citta di riferimento
${a.citta ? `Carlos ha indicato "${a.citta}".` : `NESSUNA citta indicata al lancio: si usa il PREDEFINITO, che sta nel campo "predefinita" di ${CITTA} ed e Torino. Non lasciare mai "citta" a null: un video Mobilitas e ambientato a Torino salvo indicazione contraria.`}

Apri ${CITTA} e leggi la voce. Se la citta non e nel file, ricostruiscila con gli stessi campi e segnalalo in avvertenze: la voce nuova la conferma Carlos.

La citta entra su DUE livelli, e si decidono separatamente:

**1. Gli INTERNI: sempre.** Case, uffici, auto, locali seguono SEMPRE il campo "interni" della
citta, in ogni b-roll, anche in quelli dove dalla finestra non si vede niente. Un interno non
descritto lo riempie il modello con il suo default, che e americano — ed e il difetto piu
frequente di tutti. Questo non dipende da "citta_visibile".

**2. Gli ESTERNI: dove uno sfondo si vede davvero.** Il campo "citta_visibile" dice solo questo:
se in quel b-roll c'e una finestra, una vetrata, un parabrezza, una strada o un terrazzo da cui
la citta si vede. Mettilo a true ovunque ci sia un esterno inquadrato, anche sfocato: una finestra
che da su un muro anonimo e un'occasione buttata.

Il livello che funziona e il **tessuto** (intonaci, persiane, portici, platani, tram sfocato), non
i landmark. **Massimo UN landmark riconoscibile in tutto il video**, e solo su un'inquadratura che
deve ambientare: due fanno promozione turistica. Leggi sempre "da_evitare".

## LA STRATEGIA — arriva dal marketer e viene PRIMA della tua regia
${strat ? `Promessa: ${strat.promessa}
Pubblico: ${(strat.target && strat.target.eta_pubblico) || '35-60 anni'} · In scena: ${(strat.target && strat.target.eta_in_scena) || '40-60 anni'}
Autoimmagine: ${(strat.target && strat.target.autoimmagine) || ''}
Pain point specifici: ${((strat.target && strat.target.pain_points) || []).join(' | ') || 'non dichiarati'}
Nemico (contro cosa prende posizione il video): ${(strat.target && strat.target.nemico) || 'non dichiarato'}
Obiezione da disinnescare: ${(strat.target && strat.target.obiezione) || 'non dichiarata'}
Registro sociale (decide guardaroba e casa): ${strat.registro_sociale || 'via di mezzo fra professionale e domestico'}

Momenti in ordine di valore commerciale — se la quota e 1, si compra il PRIMO:
${(strat.momenti || []).map((m, i) => `${i + 1}. "${m.frase}"
   scena quotidiana: ${m.scena_quotidiana}
   dettaglio privato: ${m.dettaglio_privato || '-'}
   deve dimostrare: ${m.cosa_deve_dimostrare}
   si riconosce: ${m.chi_dice_sono_io} · si esclude: ${m.chi_si_esclude}
   prova visiva: ${m.prova_visiva || 'da trovare'}
   da evitare: ${m.da_evitare || '-'}`).join('\n')}

Da NON mostrare: ${(strat.cosa_non_mostrare || []).join(' | ') || 'niente di dichiarato'}

Questo ordine NON si riscrive. Puoi spostare un momento solo se il test del taglio lo
smonta, e allora scrivi in avvertenze quale e perche.` : 'Nessuna strategia disponibile: decidi tu, ma resta sul target 40-60 anni.'}

## CASTING — il vincolo che scrivi tu, e che nessuno dopo di te puo correggere
La "descrizione_fissa" la scrivi qui, e gli specialisti la copiano alla lettera: se sbagli
eta o registro sociale, sbaglia tutto il video e non c e collaudo che lo recuperi.

- **Eta in scena: SEMPRE fra 40 e 60 anni.** Il pubblico va dai 35 ai 60, ma si rappresenta il
  CENTRO del bersaglio, non il suo bordo piu giovane. Mai un protagonista piu giovane, qualunque
  cosa suggerisca il tono dello script: fa leggere il problema come passeggero.
- **Guardaroba: la via di mezzo.** Non l abbigliamento da casa (felpa, tuta, pantaloni morbidi,
  capelli disfatti: legge come persona che si e arresa, e nessuno vuole riconoscersi li), non il
  completo da ufficio. Una persona curata in una giornata normale, che fra un ora esce.
- **La casa e il secondo costume.** Un ambiente brutto o anonimo abbassa il ceto percepito
  quanto un capo sbagliato. Descrivila come una casa di cui si e orgogliosi, vissuta ma bella.
- **Naturale, non premium.** Nessun look da catalogo, nessuna perfezione: pelle vera, oggetti
  usati, una sedia non allineata. Il bersaglio e "casa vera curata", non "servizio fotografico".

## Quota imposta da Carlos
${a.quote ? `Carlos ha fissato: ${JSON.stringify(a.quote)} (pain = b-roll di riconoscimento, meccanismo = infografiche).
LA QUOTA NON SI DISCUTE. Il tuo lavoro diventa il PIAZZAMENTO: quale momento merita i b-roll disponibili.
Se la quota lascia scoperto un passaggio che ne aveva bisogno, scrivilo in avvertenze con cosa costa. Se e piu alta del necessario, NON riempire: dillo e proponi dove spendere meglio.` : 'Nessuna quota imposta: decidi tu il numero, con il principio del minimum effective visual set.'}

## LA REGOLA D APERTURA — non negoziabile
Sulla PRIMA FRASE del video non va MAI un b-roll. Resta sul volto, sempre. Il primo b-roll
puo entrare dalla seconda frase in poi. Riporta la prima frase ALLA LETTERA nel campo
"prima_frase" e mettila come PRIMA voce di "senza_broll". Nessun b-roll puo averla in "copre".
Il workflow controlla questa regola contando, non leggendo: un piano che la viola torna indietro.

## Genere
${a.genere ? `Carlos ha forzato il genere a "${a.genere}". Usa quello e scrivi in motivo_genere che e stato imposto al lancio.` : 'Decidilo tu dalla condizione, con la tabella della skill. Una prevalenza non e un esclusiva.'}
Ricorda la conseguenza: genere "entrambi" significa DUE varianti per ogni b-roll con persone E formato 16:9. Un solo genere significa variante unica e 9:16.

## Correzioni attive dai video precedenti
${REGISTRO} — leggi la sezione "Correzioni attive" prima di pianificare, se il file esiste.

Restituisci l'oggetto strutturato del piano. "senza_broll" non puo essere vuoto su uno script completo: se lo e, hai riempito invece di scegliere.`

const painPrompt = (br, piano, a, scriptPath) => `Scrivi i prompt Higgsfield di UN SOLO b-roll della sezione pain point.

## Istruzioni della skill — leggile e seguile INTEGRALMENTE
${SK}/broll-pain-point/SKILL.md
e poi ${SK}/broll-pain-point/references/casting-e-guardaroba.md

## Il tuo incarico
${JSON.stringify(br, null, 2)}

## COSA LA SCENA DEVE DIMOSTRARE — dal marketer, viene prima dell estetica
${(() => {
  const m = ((a.strategia && a.strategia.momenti) || []).find((x) => br.copre && (br.copre.includes(x.frase) || x.frase.includes(br.copre.replace(/^"|"$/g, ''))))
  if (!m) return a.strategia ? `Nessun momento combacia esattamente con "${br.copre}". Registro sociale da tenere: ${a.strategia.registro_sociale || 'via di mezzo fra professionale e domestico'}.` : 'Nessuna strategia disponibile.'
  return `Scena quotidiana da rappresentare: ${m.scena_quotidiana}
Dettaglio privato — la cosa che il target fa e non racconta, e il cuore della scena: ${m.dettaglio_privato || 'non indicato'}
Proposizione da rendere innegabile: ${m.cosa_deve_dimostrare}
Chi si deve riconoscere: ${m.chi_dice_sono_io} — chi si deve escludere: ${m.chi_si_esclude}
Perche vende: ${m.perche_vende}
Prova visiva indicata: ${m.prova_visiva || 'da trovare tu'}
Versione ovvia da EVITARE: ${m.da_evitare || '-'}
Registro sociale: ${(a.strategia && a.strategia.registro_sociale) || 'via di mezzo fra professionale e domestico'}
Autoimmagine del target: ${(a.strategia && a.strategia.target && a.strategia.target.autoimmagine) || 'non dichiarata'}`
})()}

Ogni oggetto in scena o PROVA la proposizione o esce dall inquadratura. Un oggetto che non
c entra niente con gli altri (una tazzina sporca accanto a un piatto di riso in bianco) non
e "vissuto": e disordine, e fa sembrare la scena generata invece che vista.

## Il piano completo (per capire il contesto, NON per coprire altre frasi)
Idea centrale: ${piano.idea_centrale || 'non dichiarata'}
Progressione: ${piano.progressione || 'non dichiarata'}
Genere: ${piano.genere} · Formato: ${piano.aspect_ratio} · Citta: ${piano.citta || 'nessuna'}
Personaggio fisso: ${(piano.personaggio && piano.personaggio.descrizione_fissa) || 'non definito'}
Gli altri b-roll del video: ${piano.broll.map((b) => `${b.id} (${b.tipo}) — ${b.copre}`).join(' | ')}

## Lo script completo
${scriptPath}

## Citta
${piano.citta ? `Apri ${CITTA}, voce "${piano.citta}".

**Gli INTERNI la seguono sempre**, anche in questo b-roll: il campo "interni" descrive come sono
fatte DAVVERO le case, gli uffici e gli ambienti li, ed e la parte che i modelli sbagliano piu
spesso perche ricadono sull'interno americano. Descrivi l'ambiente, non limitarti a vietare il
disordine: un set non descritto viene riempito dal default del modello.

${br.citta_visibile ? `**E in questo b-roll un esterno SI VEDE**: finestra, vetrata, parabrezza o strada. Usa il livello TESSUTO — materiali, colore della pietra, persiane, alberi, arredo urbano, luce — non i landmark, salvo che l incarico dica il contrario. Sfocato ma leggibile: chi vive li si riconosce, chi non ci vive non nota niente di strano. Mai una finestra su un muro anonimo e mai una finestra bianca bruciata.` : 'In questo b-roll non c e un esterno inquadrato: la citta resta solo negli interni.'}

Leggi sempre "da_evitare".` : 'Nessuna citta nel piano.'}

## Modello immagine che genera davvero: ${a.modelloImmagine}
Apri ${CATALOGO} e leggi la sua voce: "punti_di_forza" e "limiti" ti dicono cosa quel modello sa e non sa fare. Scrivi il prompt per QUEL modello.

Restituisci l'oggetto strutturato. La chiave "prompt_t2i" deve avere ESATTAMENTE ${(br.varianti || ['unica']).join(' e ')}: ne una in piu ne una in meno.`

const infoPrompt = (br, piano, a, scriptPath) => `Scrivi i prompt Higgsfield di UNA SOLA infografica del meccanismo.

## Istruzioni della skill — leggile e seguile INTEGRALMENTE
${SK}/broll-infografica-meccanismo/SKILL.md
e poi ${SK}/broll-infografica-meccanismo/references/brand-system.md

## Il tuo incarico
${JSON.stringify(br, null, 2)}

## Le infografiche sorelle di questo video
${piano.broll.filter((b) => b.tipo === 'infografica').map((b) => `${b.id} — ${b.copre}`).join(' | ') || 'sei l unica'}
Se non sei la prima, RIPETI PAROLA PER PAROLA le sezioni palette, background, lighting e rendering della prima: la continuita fra generazioni indipendenti si ottiene ripetendo, non riformulando.

## La domanda che il pain point ha lasciato aperta
${piano.broll.filter((b) => b.tipo === 'pain').map((b) => b.copre).join(' | ') || 'nessun b-roll di pain in questo video'}
La tua infografica deve sembrare la RISPOSTA VISIVA a quella domanda, non un atlante.

## Formato: ${piano.aspect_ratio}
## Lo script completo
${scriptPath}

## Modello immagine che genera davvero: ${a.modelloImmagine}
Apri ${CATALOGO} e leggi la sua voce. Se i suoi "limiti" dicono che segue male i prompt lunghi e strutturati, semplifica la GERARCHIA dell immagine — non la precisione anatomica.

## IL VINCOLO CHE VIENE PRIMA DI TUTTO
La rappresentazione non puo rendere l affermazione medica piu forte del copy. Compila "prudenza_claim" con cosa dice il copy e cosa hai rappresentato: e la riga che dimostra che non hai alzato il claim.

Restituisci l oggetto strutturato.`

const collaudoPrompt = (piano, prompts) => `Sei il cancello prima della spesa. Da qui in poi ogni errore costa crediti veri, e un video girato con una sequenza sbagliata si rifa tutto.

Non giudichi la bellezza delle scene: verifichi che la SEQUENZA regga e che i prompt siano eseguibili.

## Il piano
${JSON.stringify(piano, null, 2)}

## I prompt prodotti
${JSON.stringify(prompts, null, 2)}

## Cosa devi verificare, uno per uno

1. RIDONDANZA — due b-roll che dicono la stessa cosa o che uscirebbero visivamente quasi identici.
2. DISCONTINUITA_PERSONAGGIO — la descrizione_fissa del piano deve comparire ALLA LETTERA in ogni prompt con la stessa persona. Due riformulazioni diverse producono due persone diverse.
3. CLAIM_GONFIATO — un infografica che rappresenta una causa dove il copy dice una relazione, o che inventa infiammazione, compressione, danno, ostruzione.
4. PALETTE_VIOLATA — nelle infografiche: colori fuori da #002552 / #F4F4F4 / #72FA93, verde su piu di un quinto del quadro, laboratori futuristici.
5. VARIANTI_ASIMMETRICHE — le due versioni donna e uomo devono differire SOLO per il protagonista. Stesso ambiente, stessa luce, stessa azione, stessa inquadratura. Se differiscono per altro, non sono varianti.
6. CHIAVI_SBAGLIATE — prompt_t2i deve avere le chiavi che il piano chiede: "unica", oppure "donna" e "uomo". Una chiave in piu e un b-roll fantasma, una in meno e una variante che si scopre mancante a generazione finita.
7. PROMPT_TROPPO_LUNGO — ogni prompt_i2v sopra i 2500 caratteri viene TRONCATO da Kling senza avvisare. Contali.
8. FORMATO_IGNORATO — il formato ${piano.aspect_ratio} deve essere scritto dentro ogni prompt T2I e deve aver cambiato l inquadratura, non solo il bordo.
9. DURATA_FUORI_LIMITE — ogni durata fra 3 e 15 secondi.
10. TESTO_GENERATO — nessun prompt puo chiedere etichette, frecce o scritte dentro l immagine.
11. PRIMA_FRASE_COPERTA — nessun b-roll puo coprire la prima frase del video: "${piano.prima_frase || 'non dichiarata'}". La prima frase resta sul volto, sempre. Se un b-roll la copre o entra prima che sia finita, e bloccante.

12. ETA_FUORI_TARGET — in scena SEMPRE 40-60 anni (il pubblico va dai 35, ma si rappresenta il
    centro del bersaglio). Ogni prompt con persone deve dichiarare un'eta dentro quella fascia. Un protagonista piu giovane e bloccante: sposta il
    video su un pubblico che non prenota. Contala, non fidarti dell'impressione.
13. REGISTRO_SOCIALE_SBAGLIATO — guardaroba e casa devono stare nella via di mezzo fra il
    professionale e il domestico. Sono bloccanti da un lato felpe, tute, pantaloni da casa,
    capelli disfatti, ciabatte (leggono come persona arresa, e nessuno vuole riconoscersi li);
    dall'altro completi, uffici e look da catalogo. Bloccante anche un ambiente anonimo o brutto:
    la casa e il secondo costume e abbassa il ceto percepito quanto un capo sbagliato.
14. PROP_INCOERENTE — ogni oggetto in scena o PROVA la proposizione o non ci sta. Oggetti che
    non c'entrano fra loro (una tazzina di caffe sporca accanto a un piatto di riso in bianco)
    non sono "vissuto": sono disordine, e fanno leggere la scena come generata. Passa in rassegna
    la lista degli oggetti di ogni prompt e chiedi di ciascuno: cosa dimostra?
15. SCENA_CHE_ILLUSTRA — il difetto piu caro di tutti. Se la scena raddoppia quello che la voce
    sta gia dicendo, si puo togliere senza perdere niente. Confronta "copre" con cio che la scena
    mostra: deve fare un'affermazione che la voce NON sta facendo.

16. SCENA_GENERICA — la prova del nove della polarizzazione. Prendi la scena e chiediti: **funzionerebbe
    identica per un'altra condizione?** Una persona stanca a tavola vale per la lombalgia, l'emicrania,
    la menopausa e la depressione: non e una scena, e uno stato d'animo. Bloccante se non contiene
    almeno un elemento che appartiene SOLO a questa condizione e a questa fascia d'eta. La domanda a
    cui la scena deve superare: chi la guarda pensa "come fanno a saperlo", o pensa "eh si, capita"?

17. CITTA_ASSENTE — la citta del piano (${piano.citta || 'nessuna'}) deve essere DENTRO i prompt, su
    due livelli distinti. (a) Gli INTERNI la seguono sempre: ogni ambiente chiuso — casa, ufficio,
    auto, locale — va DESCRITTO con i materiali di quella citta, in ogni b-roll, anche dove non si
    vede nessun esterno. Un set solo vietato ("niente disordine") e un set non descritto, e il
    modello lo riempie con il suo default americano. (b) Gli ESTERNI: dove il piano dichiara
    citta_visibile, oltre il vetro ci deve essere tessuto urbano riconoscibile e sfocato — mai un
    muro anonimo, mai una finestra bianca bruciata. Bloccante in entrambi i casi.

18. COMPOSIZIONE_A_FASCE — conta le occorrenze di "third" (o "band", "panel", "section") dentro
    ogni prompt_t2i. **Piu di UNA nella stessa frase e bloccante.** Un elenco come "face in the
    upper third, window in the middle third, nothing in the lower third" viene letto come layout
    a tre pannelli e consegna un trittico a bande orizzontali col soggetto tagliato: e gia
    successo e ha bruciato una generazione. La correzione e riscrivere quella parte in linguaggio
    da macchina da presa — piano, obiettivo, distanza in metri, profondita di campo.

E la domanda che tiene insieme tutto: la sequenza racconta una progressione, o e una raccolta di immagini indipendenti?

Esito PRONTO solo con ZERO bloccanti. Ogni bloccante porta una correzione CHIRURGICA: cosa cambiare e dove, non una riscrittura.`

const riparaPrompt = (bloccanti, prompts) => `Applica queste correzioni ai prompt. NON riscrivere quello che non e stato segnalato.

## Correzioni
${JSON.stringify(bloccanti, null, 2)}

## I prompt attuali
${JSON.stringify(prompts, null, 2)}

Restituisci l array completo dei prompt corretti, nello stesso formato, con TUTTI i b-roll (anche quelli non toccati).`

const scriviPianoPrompt = (contenuto, dest) => `Scrivi ESATTAMENTE questo contenuto JSON nel file ${dest}, creando le cartelle che servono. Non aggiungere, non riformattare, non commentare.

${contenuto}

Poi rileggi il file con python3 -c "import json;json.load(open('${dest}'));print('json valido')" e conferma in una riga.`

const stimaPrompt = (piano, dest) => `Esegui questo comando e riporta il totale:

python3 ${CLIENT} stima --piano ${piano} --catalogo ${CATALOGO} --out ${dest}

Se fallisce per credenziali assenti, dillo chiaramente: servono HF_API_KEY_ID e HF_API_KEY_SECRET nell ambiente, si creano su console.higgsfield.ai. Non inventare un costo.`

const provinniPrompt = (piano, dest, n) => `Genera i PROVINI: piu estrazioni della stessa scena, SOLO immagini.

Un'immagine costa circa 0.006 USD, un video circa 0.32: il video e il 98% del costo. Ogni generazione
e un'estrazione a se, e giudicare una scena su una sola estrazione e il modo piu caro di sbagliare.

1. Leggi ${piano}.
2. Scrivi ${dest}/piano-provini.json: stesso file, ma per OGNI b-roll ${n} righe identiche con id
   "<id-originale>--p1", "--p2", ... Non cambiare i prompt: le varianti le fa il modello da solo.
3. Esegui:
   python3 ${CLIENT} genera --piano ${dest}/piano-provini.json --catalogo ${CATALOGO} --out ${dest}/provini --solo-immagini
4. Elenca con ls i file davvero arrivati in ${dest}/provini/immagini/ e restituiscili raggruppati
   per b-roll originale. Se qualche provino manca, dillo: NON rilanciare da solo.

Restituisci l'oggetto strutturato con i percorsi assoluti.`

const sceltaPrompt = (bid, provini, piano, strat) => `Sei il giudice dei provini. Scegli quale immagine diventa un video, e da qui in poi ogni errore costa crediti veri.

## I provini del b-roll "${bid}"
${provini.map((f) => `- ${f}`).join('\n')}

**GUARDALI davvero, uno per uno, con lo strumento di lettura file.** Un provino che non hai aperto
non puoi scartarlo: lo schema ti obbliga a dare un motivo per ognuno.

## Cosa deve fare questa immagine
${(() => {
  const b = (piano.broll || []).find((x) => x.id === bid) || {}
  const m = ((strat && strat.momenti) || []).find((x) => b.copre && b.copre.includes(x.frase))
  return `Copre: ${b.copre || 'non dichiarato'}
${m ? `Deve dimostrare: ${m.cosa_deve_dimostrare}
Dettaglio privato: ${m.dettaglio_privato || '-'}
Si riconosce: ${m.chi_dice_sono_io} — si esclude: ${m.chi_si_esclude}
Come si capisce che e MANCATA: ${m.da_evitare || 'non dichiarato'}` : ''}`
})()}

## I criteri, in ordine di importanza
1. **Non e generica.** Funzionerebbe identica per un'altra condizione? Allora e sbagliata, per quanto
   sia bella. La bellezza non e un criterio: lo e il riconoscimento.
2. **Il gesto e l'oggetto ci sono** e leggono per quello che sono, non per altro.
3. **Nessuna lettura sbagliata**: gravidanza, malattia grave, attesa di qualcuno, dieta dimagrante,
   posa da catalogo. Se un'immagine si presta a una di queste, e fuori.
4. **Mani e anatomia corrette**, niente oggetti che levitano, niente cuciture o bande nel quadro.
5. **Eta 40-60 e guardaroba nella via di mezzo**, ambiente curato con profondita alle spalle.
6. **Nessun testo, nessuna lettera, nessuna insegna leggibile.**

Se TUTTI hanno un difetto bloccante metti "nessuno_accettabile": true e spiega. Meglio fermarsi che
pagare un video su un'immagine sbagliata — l'immagine si rifa per mezzo centesimo, il video no.

Compila "difetti_residui" anche per il vincitore: finiscono nell'indice, non si nascondono.`

const installaPrompt = (scelte, dest) => `Metti le immagini scelte al posto giusto, cosi che la generazione paghi SOLO i video.

Scelte (b-roll originale -> file del provino vincitore):
${scelte.map((x) => `- ${x.id}  <-  ${x.file}`).join('\n')}

Per ognuna:
1. Copia il file del provino in ${dest}/immagini/<id-originale>.jpg
2. In ${dest}/stato.json scrivi la voce "<id-originale>": {"immagine": {...}} copiando dalla voce del
   provino in ${dest}/provini/stato.json i campi "url", "status" e "request_id", e mettendo "file"
   uguale al nuovo percorso. Aggiungi "scelta_da": "<id del provino>".
   Crea il file se non esiste, e NON toccare eventuali voci "video" gia presenti.
3. Rileggi lo stato con python3 -c "import json;json.load(open('${dest}/stato.json'));print('ok')"

Serve perche il client salta una fase quando trova gia il file su disco: cosi l'immagine non si
rigenera e si paga solo il video. Conferma in una riga quante ne hai installate.`

const generaPrompt = (piano, dest, soloImmagini) => `Esegui questo comando e riporta l esito reale, compresi i falliti:

python3 ${CLIENT} genera --piano ${piano} --catalogo ${CATALOGO} --out ${dest}${soloImmagini ? ' --solo-immagini' : ''}

Puo durare a lungo: e asincrono e fa polling. Se qualche b-roll fallisce, NON rilanciare da solo: riporta quali e perche. Il comando e riprendibile, rilanciarlo non ripaga quello che ha gia ottenuto.`

const consegnaPrompt = (piano, dest, slug) => `Verifica sul DISCO cosa e stato prodotto davvero e scrivi l indice di montaggio.

1. Esegui: ls -la ${dest}/immagini ${dest}/video 2>/dev/null; cat ${dest}/manifest.json
2. Confronta con il piano ${piano}: quali b-roll hanno immagine E video, quali hanno solo l immagine, quali mancano del tutto.
3. Scrivi ${dest}/INDICE.md con:
   - una riga di intestazione: slug "${slug}", formato, modelli usati, data
   - una tabella in ordine di montaggio: id | tipo | copre (la frase dello script) | durata | variante | file video | file immagine
   - una sezione "Mancanti" con i b-roll non prodotti e il motivo dal manifest
   - una sezione "Come si monta": la progressione dal piano, e i passaggi che restano sul volto dell osteopata (senza_broll)
4. Riporta i NUMERI VERI contati sul disco, non quelli attesi dal piano.

Non dichiarare completo cio che non hai visto con ls.`

const registroPrompt = (esiti) => `Aggiorna ${REGISTRO} (crealo se non esiste) con quello che questo video ha insegnato.

Struttura del file:
# Registro dei prompt
## Correzioni attive
(difetti ricorrenti gia diventati regola: li legge il regista e chi scrive i prompt, PRIMA di lavorare)
## Osservazioni
(cose notate una volta sola: diventano correzioni attive solo quando si ripetono, e la promozione la decide Carlos)

Da questo video: ${JSON.stringify(esiti, null, 2)}

Aggiungi solo quello che vale per i PROSSIMI video: un difetto che si ripetera, una formula che ha funzionato, un limite di modello scoperto sul campo. Non un diario di questo video. Se non c e niente da aggiungere, dillo e non toccare il file.`

// ============================ RESILIENZA ============================

async function robustAgent(prompt, opts, tries = RETRIES) {
  for (let i = 0; i < tries; i++) {
    const label = i === 0 ? opts.label : `${opts.label}#retry${i}`
    const r = await agent(prompt, { ...opts, label })
    if (r) return r
    log(`  [resilienza] "${opts.label}" non ha risposto (${i + 1}/${tries})${i + 1 < tries ? ' — ritento' : ' — rinuncio'}`)
  }
  return null
}

// ============================ ORCHESTRAZIONE ============================

const a = (args && typeof args === 'object' && !Array.isArray(args)) ? args : {}
const slug = String(a.slug || '').trim()
const scriptPath = String(a.script || '').trim()

if (!slug || !scriptPath) {
  return {
    errore: 'Servono almeno "slug" e "script".',
    esempio: {
      slug: 'lombalgia-settembre',
      script: '/percorso/allo/script.md',
      citta: 'torino',
      quote: { pain: 1, meccanismo: 2 },
      modelli: { immagine: 'soul-2', video: 'kling-3-std-i2v' },
      genere: 'entrambi',
      provini: 4,
      solo_immagini: false,
      autorizza_spesa: false,
    },
    nota: 'autorizza_spesa=false (predefinito) ferma il workflow dopo la stima: nessun credito viene speso finche non lo rilanci con true.',
  }
}

const DEST = `${OUT}/${slug}`
const USCITA = `${ROOT}/outputs/${slug}`
const PIANO_FILE = `${DEST}/piano.json`

log(`B-roll per "${slug}" — script: ${scriptPath}`)
log(a.autorizza_spesa
  ? 'SPESA AUTORIZZATA: il workflow generera davvero e consumera crediti.'
  : 'Spesa NON autorizzata: mi fermo dopo la stima. Rilancia con autorizza_spesa=true per generare.')

// --- FASE 1: MODELLI ---
phase('Modelli')
const mod = await robustAgent(
  modelliPrompt({ ...a, descrizione: `slug "${slug}", script in ${scriptPath}${a.citta ? `, citta ${a.citta}` : ''}` }),
  { label: 'scegli-modelli', phase: 'Modelli', schema: MODELLI_SCHEMA, agentType: 'general-purpose' },
)
if (!mod) return { errore: 'scelta dei modelli fallita: senza modelli non si genera niente' }
log(`Modelli: immagine ${mod.immagine} · video ${mod.video} — ${mod.perche}`)
for (const x of (mod.avvertenze || [])) log(`  [avvertenza] ${x}`)
for (const x of (mod.proposte_di_aggiornamento || [])) log(`  [proposta catalogo] ${x}`)

// --- FASE 2: STRATEGIA ---
// Il regista sa DOVE si perde l attenzione, non COSA conviene dimostrare per vendere.
// Separare le due cose e l unico modo di avere una scena che argomenta invece di illustrare.
phase('Strategia')
const strat = await robustAgent(
  strategiaPrompt(a, scriptPath),
  { label: 'marketer-strategico', phase: 'Strategia', schema: STRATEGIA_SCHEMA, agentType: 'general-purpose' },
)
if (strat) {
  log(`Strategia: ${(strat.momenti || []).length} momenti — pubblico ${(strat.target && strat.target.eta_pubblico) || '?'}, in scena ${(strat.target && strat.target.eta_in_scena) || '?'}`)
  for (const x of ((strat.target && strat.target.pain_points) || [])) log(`  [pain point] ${x}`)
  for (const [i, m] of (strat.momenti || []).entries()) log(`  ${i + 1}. ${m.scena_quotidiana} -> ${m.cosa_deve_dimostrare}`)
  for (const x of (strat.avvertenze || [])) log(`  [avvertenza strategia] ${x}`)
} else {
  log('  [resilienza] nessuna strategia: la regia decide da sola, con il solo vincolo del target 40-60')
}

// --- FASE 3: REGIA ---
phase('Regia')
const piano = await robustAgent(
  regiaPrompt(a, scriptPath, strat),
  { label: 'regia-editoriale', phase: 'Regia', schema: PIANO_SCHEMA, agentType: 'general-purpose' },
)
if (!piano || !piano.broll || !piano.broll.length) {
  return { errore: 'la regia non ha prodotto un piano utilizzabile' }
}

// Il formato e il genere sono legati da una regola di Carlos: "entrambi" implica 16:9.
// Se la regia se ne dimentica, lo correggo qui e lo dico, invece di generare venti file storti.
let ratio = piano.aspect_ratio
if (piano.genere === 'entrambi' && ratio !== '16:9') {
  log(`  [correzione] genere "entrambi" impone 16:9, la regia aveva scritto ${ratio}`)
  ratio = '16:9'
} else if (piano.genere !== 'entrambi' && ratio !== '9:16') {
  log(`  [correzione] genere "${piano.genere}" impone 9:16, la regia aveva scritto ${ratio}`)
  ratio = '9:16'
}
piano.aspect_ratio = ratio

// LA REGOLA D APERTURA, VERIFICATA CONTANDO.
// Una regola dichiarata in una skill e una regola che l agente puo dimenticare. Questa
// si controlla qui, con un confronto fra stringhe normalizzate: se il piano la viola, la
// regia la rifa una volta sapendo esattamente cosa ha sbagliato, e se sbaglia ancora il
// workflow si ferma prima di spendere.
const norm = (x) => String(x || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim()
const violaApertura = (pi) => {
  const pf = norm(pi.prima_frase)
  if (pf.length < 12) return null // frase troppo corta per un confronto affidabile
  const colpevole = (pi.broll || []).find((b) => {
    const c = norm(b.copre)
    return c.length >= 12 && (c === pf || c.includes(pf) || pf.includes(c))
  })
  return colpevole ? colpevole.id : null
}

let colpevole = violaApertura(piano)
if (colpevole) {
  log(`  [regola d apertura] il b-roll "${colpevole}" copre la prima frase: rimando indietro il piano`)
  const rifatto = await robustAgent(
    regiaPrompt(a, scriptPath, strat) + `\n\n## IL PIANO PRECEDENTE E STATO RIFIUTATO\nIl b-roll "${colpevole}" copriva la prima frase del video ("${piano.prima_frase}"). La regola d apertura non si negozia: sposta quel b-roll alla frase successiva, oppure toglilo e metti la prima frase in senza_broll. Il resto del piano puoi tenerlo.`,
    { label: 'regia-editoriale#apertura', phase: 'Regia', schema: PIANO_SCHEMA, agentType: 'general-purpose' },
    2,
  )
  if (rifatto && rifatto.broll && rifatto.broll.length) {
    Object.assign(piano, rifatto)
    piano.aspect_ratio = ratio
    colpevole = violaApertura(piano)
  }
  if (colpevole) {
    return {
      errore: 'REGOLA D APERTURA VIOLATA',
      dettaglio: `Il b-roll "${colpevole}" copre ancora la prima frase ("${piano.prima_frase}"). Non genero: la prima frase resta sul volto.`,
      piano_scartato: piano,
    }
  }
  log('  [regola d apertura] rispettata dopo la ripianificazione')
}

log(`Piano: ${piano.broll.length} b-roll (${piano.broll.filter((b) => b.tipo === 'pain').length} pain, ${piano.broll.filter((b) => b.tipo === 'infografica').length} infografiche) · genere ${piano.genere} · ${ratio}`)
for (const s of (piano.senza_broll || [])) log(`  [resta sul volto] ${s.passaggio} — ${s.perche}`)
for (const x of (piano.avvertenze || [])) log(`  [avvertenza regia] ${x}`)

// --- FASE 4: PROMPT, UN SOTTOAGENTE PER B-ROLL, IN PARALLELO ---
// Qui il parallelo conviene davvero: ogni b-roll e indipendente dagli altri, e l unica
// cosa che devono condividere (personaggio, palette, progressione) gliela passa il piano.
phase('Prompt')
const ctx = { ...a, modelloImmagine: mod.immagine, strategia: strat }
let prompts = (await parallel(
  piano.broll.map((br) => () =>
    robustAgent(
      br.tipo === 'infografica' ? infoPrompt(br, piano, ctx, scriptPath) : painPrompt(br, piano, ctx, scriptPath),
      { label: `prompt:${br.id}`, phase: 'Prompt', schema: BROLL_SCHEMA, agentType: 'general-purpose' },
    ),
  ),
)).filter(Boolean)

if (prompts.length < piano.broll.length) {
  const mancanti = piano.broll.map((b) => b.id).filter((id) => !prompts.some((p) => p.id === id))
  log(`  ATTENZIONE: ${mancanti.length} b-roll senza prompt dopo i retry: ${mancanti.join(', ')}`)
}
if (!prompts.length) return { errore: 'nessun prompt prodotto' }

// --- FASE 5: COLLAUDO, PRIMA DI SPENDERE ---
phase('Collaudo')
let coll = await robustAgent(
  collaudoPrompt(piano, prompts),
  { label: 'collaudo-sequenza', phase: 'Collaudo', schema: COLLAUDO_SCHEMA, agentType: 'general-purpose' },
)
if (coll && (coll.bloccanti || []).length) {
  log(`  Collaudo: ${coll.bloccanti.length} bloccanti — riparo prima di spendere`)
  for (const b of coll.bloccanti) log(`    [${b.tipo}] ${b.id}: ${b.problema || ''}`)
  const fix = await robustAgent(
    riparaPrompt(coll.bloccanti, prompts),
    {
      label: 'ripara-prompt', phase: 'Collaudo', agentType: 'general-purpose',
      schema: { type: 'object', additionalProperties: false, required: ['prompts'], properties: { prompts: { type: 'array', items: BROLL_SCHEMA } } },
    },
  )
  if (fix && fix.prompts && fix.prompts.length) {
    prompts = fix.prompts
    coll = await robustAgent(
      collaudoPrompt(piano, prompts),
      { label: 'collaudo-sequenza#2', phase: 'Collaudo', schema: COLLAUDO_SCHEMA, agentType: 'general-purpose' },
    )
  } else {
    log('  [resilienza] riparazione non riuscita: i prompt restano quelli di prima')
  }
}
const bloccantiResidui = (coll && coll.bloccanti) || []
if (bloccantiResidui.length) {
  log(`  Collaudo NON superato: restano ${bloccantiResidui.length} bloccanti.`)
  log('  Non genero: spendere crediti su una sequenza che non regge e il modo piu caro di scoprirlo.')
}
if (coll && coll.giudizio) log(`  Giudizio: ${coll.giudizio}`)

// --- FASE 6: IL PIANO ESEGUIBILE ---
phase('Piano')
// Una riga per variante: e cosi che il client la vede come un b-roll a se, con il suo
// file e il suo stato. Le due varianti condividono il prompt I2V, che descrive movimento.
const righe = []
for (const p of prompts) {
  const meta = piano.broll.find((b) => b.id === p.id) || {}
  for (const [chiave, testo] of Object.entries(p.prompt_t2i || {})) {
    righe.push({
      id: chiave === 'unica' ? p.id : `${p.id}-${chiave}`,
      tipo: meta.tipo || 'pain',
      variante: chiave,
      copre: p.copre || meta.copre || '',
      prompt_t2i: testo,
      prompt_i2v: p.prompt_i2v,
      durata: Math.min(15, Math.max(3, Math.round(p.durata || meta.secondi || 5))),
    })
  }
}
const contenuto = JSON.stringify({
  slug,
  generato_da: 'genera-broll.workflow.js',
  condizione: piano.condizione || null,
  genere: piano.genere,
  aspect_ratio: ratio,
  citta: piano.citta || null,
  idea_centrale: piano.idea_centrale || null,
  prima_frase: piano.prima_frase || null,
  progressione: piano.progressione || null,
  personaggio: piano.personaggio || null,
  senza_broll: piano.senza_broll || [],
  modelli: { immagine: mod.immagine, video: mod.video },
  broll: righe,
}, null, 2)

const scritto = await robustAgent(
  scriviPianoPrompt(contenuto, PIANO_FILE),
  { label: 'scrivi-piano', phase: 'Piano', agentType: 'general-purpose' },
)
if (!scritto) return { errore: `piano non scritto su ${PIANO_FILE}`, piano_in_memoria: contenuto }
log(`Piano eseguibile: ${righe.length} generazioni (${prompts.length} b-roll x varianti) in ${PIANO_FILE}`)

// --- FASE 7: STIMA ---
phase('Stima')
const stima = await robustAgent(
  stimaPrompt(PIANO_FILE, USCITA),
  { label: 'stima-costo', phase: 'Stima', agentType: 'general-purpose' },
)

const base = {
  slug, piano: PIANO_FILE, uscita: USCITA,
  modelli: { immagine: mod.immagine, video: mod.video },
  genere: piano.genere, aspect_ratio: ratio,
  b_roll: prompts.length, generazioni: righe.length,
  collaudo: bloccantiResidui.length ? `NON superato (${bloccantiResidui.length} bloccanti)` : 'superato',
  bloccanti: bloccantiResidui,
  stima,
}

if (bloccantiResidui.length) {
  return { ...base, esito: 'FERMO AL COLLAUDO', cosa_fare: 'Correggi i bloccanti nel piano, poi rilancia con autorizza_spesa=true.' }
}

if (!a.autorizza_spesa) {
  return {
    ...base,
    esito: 'PRONTO — spesa non autorizzata',
    cosa_fare: `Guarda la stima. Poi rilancia lo stesso workflow con autorizza_spesa=true, oppure lancia a mano:\n  python3 ${CLIENT} genera --piano ${PIANO_FILE} --catalogo ${CATALOGO} --out ${USCITA} --solo-immagini`,
  }
}

// --- FASE 8: PROVINI E SELEZIONE ---
// Il video costa circa 54 volte l'immagine. Generare una sola immagine e mandarla in video
// significa scommettere 0.32 USD su una singola estrazione: i provini costano un decimo e
// tolgono la scommessa.
const NPROVINI = Math.max(1, Math.min(8, Number(a.provini) || 4))
let scelte = []
if (NPROVINI > 1 && !a.solo_immagini) {
  phase('Provini')
  const prov = await robustAgent(
    provinniPrompt(PIANO_FILE, USCITA, NPROVINI),
    { label: 'provini', phase: 'Provini', schema: PROVINI_SCHEMA, agentType: 'general-purpose' },
  )
  const gruppi = (prov && prov.gruppi) || []
  for (const x of ((prov && prov.mancanti) || [])) log(`  [provino mancante] ${x}`)
  if (!gruppi.length) {
    log('  [resilienza] nessun provino: si genera direttamente, come prima')
  } else {
    log(`Provini: ${gruppi.reduce((n, g) => n + (g.file || []).length, 0)} immagini su ${gruppi.length} b-roll`)

    phase('Selezione')
    const esiti = await parallel(gruppi.map((g) => () =>
      robustAgent(
        sceltaPrompt(g.id, g.file || [], piano, strat),
        { label: `scegli:${g.id}`, phase: 'Selezione', schema: SCELTA_SCHEMA, agentType: 'general-purpose' },
      ).then((r) => (r ? { ...r, id: g.id, file: (g.file || []).find((f) => f.includes(r.vincitore)) } : null)),
    ))
    for (const e of esiti.filter(Boolean)) {
      if (e.nessuno_accettabile || !e.file) {
        log(`  [${e.id}] NESSUN PROVINO ACCETTABILE — non si spende il video: ${e.perche}`)
        continue
      }
      log(`  [${e.id}] scelto ${e.vincitore} — ${e.perche}`)
      for (const d of (e.difetti_residui || [])) log(`      [difetto residuo] ${d}`)
      scelte.push(e)
    }
    if (scelte.length) {
      await robustAgent(
        installaPrompt(scelte, USCITA),
        { label: 'installa-scelte', phase: 'Selezione', agentType: 'general-purpose' },
      )
    }
  }
}

// --- FASE 9: GENERAZIONE ---
phase('Generazione')
const gen = await robustAgent(
  generaPrompt(PIANO_FILE, USCITA, !!a.solo_immagini),
  { label: 'genera', phase: 'Generazione', agentType: 'general-purpose' },
  1, // una sola volta: un retry cieco su una generazione e un retry a pagamento
)

// --- FASE 10: CONSEGNA, VERIFICATA SUL DISCO ---
phase('Consegna')
const cons = await robustAgent(
  consegnaPrompt(PIANO_FILE, USCITA, slug),
  { label: 'consegna', phase: 'Consegna', agentType: 'general-purpose' },
)
await robustAgent(
  registroPrompt({ collaudo: coll, avvertenze_modelli: mod.avvertenze, avvertenze_regia: piano.avvertenze }),
  { label: 'registro-prompt', phase: 'Consegna', agentType: 'general-purpose' },
  2,
)

return {
  ...base,
  esito: 'generato',
  generazione: gen || 'NON CONFERMATA: controlla il disco',
  consegna: cons || 'NON CONFERMATA: controlla il disco',
  avviso: 'Gli esiti qui sopra sono dichiarazioni degli agenti. La verita e in ' + USCITA + '/manifest.json e nei file.',
}

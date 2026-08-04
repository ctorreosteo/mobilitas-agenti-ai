export const meta = {
  name: 'genera-procedure-osteopatiche',
  description: 'Per ogni problema: draft con la skill autore, revisione su quattro livelli (1o parallelo, 2o fedelta, 3o logica dell apprendimento, 4o editor di asciugatura), sintesi finale. Resiliente: retry sugli agenti critici + fallback di promozione, un singolo fallimento non aborta la catena',
  whenToUse: 'Genera le procedure cliniche Mobilitas in batch a partire da PROBLEMI_OSTEOPATIA.xlsx',
  phases: [
    { title: 'Scoperta', detail: 'trova da solo le skill-revisore presenti nella cartella' },
    { title: 'Draft', detail: 'skill direttore-osteopatico-procedure redige v1 + scheda' },
    { title: 'Revisione', detail: 'TUTTI i revisori di 1o livello, in parallelo, feedback per severita' },
    { title: 'Sintesi intermedia', detail: 'skill autore pesa i feedback e riscrive la v2' },
    { title: 'Revisione 2o livello', detail: 'revisori di 2o livello (dal manifesto) sulla v2' },
    { title: 'Sintesi v3', detail: 'skill autore applica i feedback di 2o livello -> v3' },
    { title: 'Revisione 3o livello', detail: 'logica dell apprendimento (dal manifesto) sulla v3' },
    { title: 'Sintesi v4', detail: 'skill autore applica i rilievi di apprendimento -> v4' },
    { title: 'Revisione 4o livello', detail: 'editor di asciugatura (dal manifesto) sulla v4' },
    { title: 'Sintesi finale', detail: 'skill autore applica la mappa di taglio dell editor -> v5 finale' },
  ],
}

// ---- percorsi (assoluti: i subagent non ereditano la working dir) ----
const ROOT = '/Users/carlitos/mobilitas-agenti-ai/agente-creazione-procedure'
const SK = ROOT + '/.claude/skills'
const AUTORE = SK + '/direttore-osteopatico-procedure'
const OUT = ROOT + '/procedure-generate'
const DATA = OUT + '/_dati/problemi.json'

// ---- RUOLI E LIVELLI DECISI DAL MANIFESTO, NON DAL CODICE ----
// L'ESISTENZA dei revisori resta auto-scoperta dalla cartella .claude/skills.
// Il RUOLO e il LIVELLO (autore / 1o / 2o / 3o / 4o livello) li decide ESPLICITAMENTE
// procedure-generate/_dati/livelli.json: ogni revisore va elencato in "primo_livello",
// "secondo_livello", "terzo_livello" o "quarto_livello". Un revisore presente nella cartella
// ma non elencato NON viene usato. Cosi aggiungi/togli/sposti revisori modificando solo quel file.
const MANIFESTO = OUT + '/_dati/livelli.json'

// Schema della fase di scoperta: cartelle reali + ruoli/livelli espliciti dal manifesto.
const DISCOVERY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['tutte_le_skill', 'autore', 'primo_livello', 'secondo_livello', 'terzo_livello', 'quarto_livello'],
  properties: {
    tutte_le_skill: { type: 'array', items: { type: 'string' }, description: 'Chiavi (dopo "direttore-osteopatico-") di TUTTE le cartelle skill realmente presenti' },
    autore: { type: 'string', description: 'Chiave dell autore dal manifesto (di norma "procedure")' },
    primo_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di PRIMO livello dal manifesto' },
    secondo_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di SECONDO livello dal manifesto' },
    terzo_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di TERZO livello dal manifesto (di norma "apprendimento")' },
    quarto_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di QUARTO livello dal manifesto (di norma "editor")' },
  },
}

const discoveryPrompt = () => `Devi determinare ruoli e livelli delle skill di questo studio combinando la cartella reale e il manifesto.

1) Esegui: ls -1 ${SK}
   Prendi TUTTE le cartelle che iniziano con "direttore-osteopatico-" e per ognuna estrai la chiave = la parte dopo quel prefisso (es. "direttore-osteopatico-compliance" -> "compliance"). Questo e "tutte_le_skill".
2) Leggi il manifesto ${MANIFESTO} (JSON). Prendi "autore" (una chiave), "primo_livello", "secondo_livello", "terzo_livello" e "quarto_livello" (array di chiavi; un array puo mancare o essere vuoto -> restituisci []).

Restituisci l'oggetto strutturato con: tutte_le_skill, autore, primo_livello, secondo_livello, terzo_livello, quarto_livello.
Regole: usa SOLO cartelle realmente presenti; non inventare chiavi; se una chiave del manifesto non ha una cartella corrispondente, NON includerla; riporta i quattro livelli esattamente come stanno nel manifesto (filtrati sulle cartelle esistenti).`

// ---- schema del feedback strutturato di ogni revisore ----
const FEEDBACK_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['revisore', 'rilievi'],
  properties: {
    revisore: { type: 'string' },
    giudizio_sintetico: { type: 'string', description: 'Una frase: la procedura regge o no dal suo punto di vista' },
    rilievi: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['severita', 'sezione', 'problema', 'correzione'],
        properties: {
          severita: { type: 'string', enum: ['ERRORE', 'RISCHIO', 'PREFERENZA'] },
          sezione: { type: 'string', description: 'Sezione/numero del documento a cui si riferisce' },
          problema: { type: 'string' },
          correzione: { type: 'string', description: 'Cosa fare concretamente' },
        },
      },
    },
  },
}

// ============================ PROMPT ============================

const draftPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas (OsteoTouch). Devi redigere la procedura clinica per il problema con slug "${slug}".

## Istruzioni della skill (leggile e seguile INTEGRALMENTE, in quest'ordine)
1. Leggi ${AUTORE}/SKILL.md
2. Poi leggi i reference che la SKILL indica, ALMENO: dna-editoriale.md (voce, prima di scrivere), architettura-procedura.md (struttura fissa), cinque-modelli-osteopatici.md (impalcatura Parte 0, leggila per prima) e fase-0-piramide-del-comando.md (il Motore Clinico, ragionamento implicito), ancore-verificate.md e ancore-scientifiche.md (ancora scientifica), scheda-operativa.md, integrazione-gestionale.md, sistema-libreria.md, esempio-canonico-acufeni.md SOLO per voce/ritmo (precede l'inversione: NON copiarne i claim gonfiati) ed esempio-reflusso.md (voce, caso a evidenza sottile). Sono in ${AUTORE}/references/. Per l'IMPIANTO Parte 0 allineato allo standard (cinque modelli + Motore Clinico) il modello e' ${OUT}/reflusso/procedura-reflusso.md

## Dati del problema
Apri ${DATA}, trova l'oggetto con "slug": "${slug}" e usa TUTTI i suoi campi (sintomi, soluzioni_provate, farmaci, esami_strumentali, benefici_trattamento, ads_pain_points, red_flag, meccanismo_causa, meccanismo_trattamento, obiezioni_specifiche) come materia prima. Sono la voce del paziente e del mercato: la procedura deve rispondere a quei sintomi, smontare quelle obiezioni, gestire quei red flag.

## Ricerca scientifica — OBBLIGATORIA
Prima di scrivere la sezione evidenza DEVI cercare sul web e verificare ogni studio: titolo/autore/anno/PMID reali. Se non verifichi uno studio, non citarlo. Scegli l'ancora scientifica (un ricercatore reale, vivente, il piu autorevole al mondo in terapia manuale su questa condizione).

## Output
Scrivi in markdown, ~5.000-7.000 parole:
- ${OUT}/${slug}/v1-draft.md  → la procedura completa (architettura fissa Parte 0 + I-IV)
- ${OUT}/${slug}/v1-scheda.md → la Scheda Operativa (una pagina, sei blocchi)
Crea la cartella se non esiste. Non convertire in .docx (pandoc va invocato a parte): consegna markdown.

Alla fine restituisci SOLO: numero parole della procedura + ancora scientifica scelta + una riga di note. Il file e gia il deliverable.`

const reviewPrompt = (slug, r) => `Sei il revisore **${r.key}** del panel avversariale Mobilitas (PRIMO livello). Devi revisionare una procedura clinica osteopatica.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md (e i suoi reference se ne cita). Adotta esattamente quella prospettiva, con lo stesso obbligo di ricerca e la stessa severita.

## Documento da revisionare
Leggi ${OUT}/${slug}/v1-draft.md (la procedura) e ${OUT}/${slug}/v1-scheda.md (la scheda). Se non esistono, restituisci un rilievo ERRORE che dice che il draft manca.

## Output
Classifica OGNI rilievo per severita: ERRORE (fatto sbagliato/pericoloso, va corretto), RISCHIO (esposizione da valutare), PREFERENZA (gusto, ignorabile). Sii chirurgico: sezione precisa, problema, correzione concreta. Non riscrivere la procedura, non elogiare: solo rilievi azionabili.

Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa leggibile in ${OUT}/${slug}/feedback-${r.key}.md`

// SINTESI INTERMEDIA (v2): pesa i feedback di TUTTI i revisori di 1o livello e riscrive.
const synthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la versione INTERMEDIA (v2) della procedura "${slug}" sintetizzando i feedback dei revisori di 1o livello. NON e ancora la finale: dopo di te la v2 va al 2o livello.

## Metodo di sintesi (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Regola che protegge il documento: **il feedback si pesa, non si somma**. ERRORE si corregge; RISCHIO si valuta; PREFERENZA si ignora di default. Elimina i doppioni e i conflitti tra lenti. Se la procedura cresce oltre il 20%, hai sommato invece di pesare: ferma e ripesa.

## Input
- Draft: ${OUT}/${slug}/v1-draft.md e ${OUT}/${slug}/v1-scheda.md
- Feedback: leggi TUTTI i file ${OUT}/${slug}/feedback-*.md (uno per revisore, esclusi quelli che finiscono in -r2.md, -r3.md o -r4.md)

## Output
Riscrivi applicando il triage:
- ${OUT}/${slug}/v2-intermedia.md → procedura intermedia
- ${OUT}/${slug}/scheda-v2.md     → scheda intermedia

Restituisci SOLO: cosa hai corretto (ERRORI), cosa hai valutato (RISCHI), cosa hai ignorato (PREFERENZE), variazione % di lunghezza.`

// SECONDA REVISIONE: i revisori di 2o livello (dal manifesto), sulla v2.
const secondReviewPrompt = (slug, r) => `Sei il revisore di SECONDO LIVELLO **${r.key}** del panel Mobilitas. Questa e la SECONDA passata: la procedura e gia stata revisionata da tutti i revisori di 1o livello e riscritta una volta. Tu la guardi sulla versione aggiornata e indurita.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md (e i suoi reference se ne cita). Adotta esattamente quella prospettiva, con la stessa severita.

## Documento da revisionare
Leggi ${OUT}/${slug}/v2-intermedia.md e ${OUT}/${slug}/scheda-v2.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v2 manca.

## Output
Classifica OGNI rilievo per severita: ERRORE / RISCHIO / PREFERENZA. Sii chirurgico: sezione/elemento preciso, problema, correzione concreta. Non riscrivere la procedura.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${OUT}/${slug}/feedback-${r.key}-r2.md`

// SINTESI v3: applica i feedback di 2o livello alla v2. NON e la finale: dopo c'e il 3o livello (apprendimento) e poi il 4o (editor).
const thirdSynthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la v3 della procedura "${slug}", applicando i feedback della revisione di 2o livello alla v2. NON e ancora la finale: dopo di te la v3 va al revisore della logica dell'apprendimento (3o livello) e poi all'editor di asciugatura (4o livello).

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Vale la stessa regola: **il feedback si pesa, non si somma**. Parti dalla v2, non dalla bozza.

## Input
- Procedura intermedia: ${OUT}/${slug}/v2-intermedia.md e ${OUT}/${slug}/scheda-v2.md
- Feedback della 2a passata: leggi TUTTI i file ${OUT}/${slug}/feedback-*-r2.md

## Output
Riscrivi applicando il triage:
- ${OUT}/${slug}/v3-intermedia.md → procedura v3
- ${OUT}/${slug}/scheda-v3.md     → scheda v3

Restituisci SOLO: cosa hai corretto dalla 2a revisione, cosa hai valutato/ignorato, variazione % di lunghezza rispetto alla v2.`

// TERZA REVISIONE: la logica dell'apprendimento (dal manifesto), sulla v3. Non aggiunge clinica, non asciuga: riordina e pretende il senso.
const thirdReviewPrompt = (slug, r) => `Sei il revisore di TERZO LIVELLO **${r.key}** del panel Mobilitas — la logica dell'apprendimento. La procedura e gia stata validata dai revisori di 1o e 2o livello: contenuto, sicurezza, compliance e fedelta al metodo sono chiusi. Tu guardi il documento non come testo ma come PERCORSO DI APPRENDIMENTO, e rispondi a una domanda sola: chi legge impara davvero a fare, o impara solo a eseguire?

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md e il suo reference ${r.skill}/references/sei-fasi-apprendimento.md. La legge e la sequenza: **perche -> cosa -> come -> pratica -> feedback -> autonomia**. Il difetto capitale delle procedure e contenere solo il "come": passi corretti e nessun senso attorno, cosi il lettore esegue senza capire e crolla al primo caso fuori copione. Trova i gradini mancanti, invertiti o solo accennati, e di dove vanno rimessi.

## Tre confini rigidi
1. **Non aggiungi contenuto clinico**: niente tecniche, dosi, studi, red flag o cautele nuove. Se una fase manca, la costruisci con il materiale gia presente nel documento, spostandolo o esplicitandone il senso.
2. **Non asciughi**: dopo di te c'e l'editor (4o livello). Una ripetizione con funzione didattica e un pregio, non un difetto: segnalala tra le cose DA PROTEGGERE.
3. **Non gonfi**: preferisci lo spostamento all'aggiunta. Ogni rilievo che aggiunge testo dichiara quante parole costa. Budget complessivo: crescita netta **<= 5%**.

Rispetta l'INTOCCABILE (red flag, criteri di invio, controindicazioni, screening, stop-rule, dosi, PMID/dati, hedge di compliance, le tre voci, l'architettura fissa Parte 0/I/II/III/IV). Se il documento gia insegna, il verdetto legittimo e "Insegna": non inventare gradini mancanti.

## Documento da revisionare
Leggi ${OUT}/${slug}/v3-intermedia.md e ${OUT}/${slug}/scheda-v3.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v3 manca.

## Output
Mappa il tuo output sullo schema per severita: **ERRORE** = una fase e assente o invertita in modo che rompe l'apprendimento (il "come" prima del "perche", passi senza quadro d'insieme, nessun feedback intra-seduta, nessun criterio di autonomia). **RISCHIO** = la fase c'e ma e debole, implicita o lontana dal punto d'uso. **PREFERENZA** = gusto didattico (max 3). Per ogni rilievo: fase mancante, sezione OSPITE gia esistente dove rimetterla, cosa fare concretamente, costo in parole. Non riscrivere la procedura.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${OUT}/${slug}/feedback-${r.key}-r3.md, includendo la mappa delle sei fasi (presente/debole/assente), la sezione **Da proteggere dall'editor** e il bilancio parole.`

// SINTESI v4: applica i rilievi di apprendimento alla v3. NON e la finale: dopo c'e l'editor (4o livello).
const fourthSynthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la v4 della procedura "${slug}", applicando i rilievi del revisore della logica dell'apprendimento (3o livello) alla v3. NON e ancora la finale: dopo di te la v4 va all'editor di asciugatura (4o livello).

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Vale la stessa regola: **il feedback si pesa, non si somma**. Parti dalla v3, non dalle versioni precedenti.

Regola specifica di questo livello: **prima si sposta, poi si riscrive, solo in ultimo si aggiunge**. Quasi tutti i rilievi di apprendimento si chiudono riordinando materiale che c'e gia o attaccando il senso al passo che lo richiede. NON introdurre contenuto clinico nuovo (tecniche, dosi, studi, red flag): il contenuto e chiuso dai livelli 1 e 2. Crescita netta ammessa rispetto alla v3: **massimo 5%**; se la superi, hai aggiunto invece di riordinare.

## Input
- Procedura v3: ${OUT}/${slug}/v3-intermedia.md e ${OUT}/${slug}/scheda-v3.md
- Rilievi di apprendimento: leggi TUTTI i file ${OUT}/${slug}/feedback-*-r3.md

## Output
- ${OUT}/${slug}/v4-intermedia.md → procedura v4
- ${OUT}/${slug}/scheda-v4.md     → scheda v4

Restituisci SOLO: quali fasi dell'apprendimento hai colmato e come (spostamento / riscrittura / aggiunta), cosa hai ignorato, la variazione % di lunghezza rispetto alla v3, e l'elenco dei passaggi che il revisore ha marcato **da proteggere dall'editor** (riportalo, serve al livello successivo).`

// QUARTA REVISIONE: l'editor di asciugatura (dal manifesto), sulla v4. Produce una MAPPA DI TAGLIO, non riscrive.
const fourthReviewPrompt = (slug, r) => `Sei il revisore di QUARTO LIVELLO **${r.key}** del panel Mobilitas — l'editor di asciugatura. La procedura e gia stata validata dai revisori di 1o e 2o livello e riordinata dal revisore della logica dell'apprendimento (3o livello): contenuto, sicurezza, compliance, fedelta al metodo e impianto didattico sono chiusi. Tu NON aggiungi ne contesti la sostanza: produci una MAPPA DI TAGLIO per togliere ridondanza e riportare il documento nel range 5.000-7.000 parole, senza perdere informazione clinica/sicurezza/legale/metodo e senza spegnere la voce.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md. Rispetta l'INTOCCABILE (red flag, controindicazioni, screening, stop-rule, dosi, PMID/dati, hedge di compliance, le tre voci). Se il documento e gia tra 5.000 e 7.000 parole di PROSA (non contare le celle delle tabelle) e non trovi ridondanza vera, il verdetto legittimo e "Gia asciutta": non inventare tagli.

## Vincolo aggiuntivo: il lavoro del 3o livello
Leggi anche i file ${OUT}/${slug}/feedback-*-r3.md e in particolare la loro sezione **Da proteggere dall'editor**. Quei passaggi hanno funzione didattica: una ripetizione che ancora il senso al punto d'uso NON e ridondanza. Se ritieni comunque che uno di essi vada tagliato, classificalo al massimo come PREFERENZA e motiva perche il documento insegna lo stesso senza.

## Documento da revisionare
Leggi ${OUT}/${slug}/v4-intermedia.md e ${OUT}/${slug}/scheda-v4.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v4 manca.

## Output
Mappa il tuo output sullo schema per severita: **RIDONDANTE -> ERRORE** (taglio sicuro, l'info esiste identica altrove), **COMPRIMIBILE -> RISCHIO** (stessa sostanza in meno parole), **PREFERENZA -> PREFERENZA**. Per ogni rilievo indica sezione/passaggio, cosa tagliare o come comprimere, e dove resta l'informazione. Non riscrivere la procedura.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${OUT}/${slug}/feedback-${r.key}-r4.md`

// SINTESI FINALE (v5): applica la mappa di taglio dell'editor alla v4. Solo se strettamente necessario.
const finalSynthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi chiudere la versione FINALE (v5) della procedura "${slug}", applicando la mappa di taglio dell'editor (4o livello) alla v4.

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Regola: **si asciuga solo se strettamente necessario**. Applica i tagli RIDONDANTE (ex-ERRORE: ridondanza vera, informazione identica altrove); valuta i COMPRIMIBILE (ex-RISCHIO) solo se servono a rientrare nel range 5.000-7.000 parole di prosa; ignora le PREFERENZE di default. NON toccare l'INTOCCABILE (red flag, sicurezza, dosi, PMID, hedge, le tre voci) ne i passaggi marcati **da proteggere** nei feedback di 3o livello (${OUT}/${slug}/feedback-*-r3.md): sono le ripetizioni che tengono in piedi l'apprendimento. Se la v4 e gia asciutta, lasciala com'e: copia la v4 nella v5 senza modifiche.

## Input
- Procedura v4: ${OUT}/${slug}/v4-intermedia.md e ${OUT}/${slug}/scheda-v4.md
- Mappa di taglio: leggi TUTTI i file ${OUT}/${slug}/feedback-*-r4.md
- Da proteggere: la sezione omonima nei file ${OUT}/${slug}/feedback-*-r3.md

## Output
- ${OUT}/${slug}/v5-finale.md     → procedura FINALE da consegnare
- ${OUT}/${slug}/scheda-finale.md → scheda FINALE

Restituisci SOLO: cosa hai tagliato (RIDONDANTE), cosa hai compresso o lasciato, cosa hai protetto su indicazione del 3o livello, e la variazione di lunghezza rispetto alla v4.`

// promuovi un documento a versione successiva senza modifiche (quando un livello e vuoto)
const promotePrompt = (procIn, schedaIn, procOut, schedaOut) =>
  `Copia senza modifiche ${procIn} in ${procOut} e ${schedaIn} in ${schedaOut}. Poi conferma in una riga.`

// ============================ RESILIENZA ============================
// Un singolo agente che fallisce NON deve piu abortire l'intera catena.
// Due meccanismi:
//  1) robustAgent: ritenta l'agente critico fino a RETRIES volte (gestisce i fallimenti transienti, la causa piu comune di stallo).
//  2) promote: se una SINTESI non riesce anche dopo i retry, si promuove (copia) l'ultima versione buona alla successiva, cosi la catena PROSEGUE con il miglior documento disponibile invece di fermarsi. La procedura arriva comunque in fondo (con un warning), non si perde il lavoro dei livelli gia fatti.
const RETRIES = 3

async function robustAgent(prompt, opts, tries = RETRIES) {
  for (let i = 0; i < tries; i++) {
    const label = i === 0 ? opts.label : `${opts.label}#retry${i}`
    const r = await agent(prompt, { ...opts, label })
    if (r) return r
    log(`  [resilienza] "${opts.label}" non ha risposto (tentativo ${i + 1}/${tries})${i + 1 < tries ? ' — ritento' : ' — rinuncio'}`)
  }
  return null
}

// Copia una versione nella successiva senza modifiche. Usata come FALLBACK quando una sintesi fallisce, e nei livelli vuoti.
async function promote(procIn, schedaIn, procOut, schedaOut, motivo) {
  log(`  [resilienza] ${motivo}: promuovo ${procIn.split('/').pop()} -> ${procOut.split('/').pop()} senza modifiche`)
  const r = await robustAgent(
    promotePrompt(procIn, schedaIn, procOut, schedaOut),
    { label: `promuovi:${procOut.split('/').pop()}`, phase: 'Sintesi', agentType: 'general-purpose' },
    2
  )
  if (!r) log(`  [resilienza] ATTENZIONE: anche la promozione verso ${procOut.split('/').pop()} non ha confermato — controlla i file a mano`)
  return r
}

// ============================ ORCHESTRAZIONE ============================

// ---- DUE MODALITA D'USO ----
// A) Procedure SPECIFICHE: args = ["reflusso"] oppure ["reflusso","cervicalgia", ...]
// B) TUTTE le procedure: args = "tutte" (o "all" / "*") -> carica gli slug dal JSON
const raw = Array.isArray(args) ? args : (args ? [args] : [])
const wantAll = raw.length === 1 && ['tutte', 'tutti', 'all', '*'].includes(String(raw[0]).toLowerCase())

let slugs = raw
if (wantAll) {
  log('Modalita TUTTE: carico l\'elenco completo dei problemi dal JSON.')
  const list = await robustAgent(
    `Apri ${DATA} (un array JSON di problemi). Restituisci l'array "slugs" con TUTTI i valori del campo "slug", nell'ordine del file. Non inventare nulla.`,
    { label: 'carica-tutti-gli-slug', phase: 'Scoperta', agentType: 'general-purpose',
      schema: { type: 'object', additionalProperties: false, required: ['slugs'],
        properties: { slugs: { type: 'array', items: { type: 'string' } } } } }
  )
  slugs = (list && list.slugs) || []
}

if (!slugs.length) {
  log('Nessuno slug da generare. Passa es. ["reflusso"] (specifica) oppure "tutte" (batch completo).')
  return { errore: 'args vuoto: passa uno o piu slug, oppure "tutte"' }
}
log(`Genero ${slugs.length} procedure: ${slugs.join(', ')}`)

// --- FASE 0: SCOPERTA DINAMICA (cartella reale) + RUOLI (manifesto) ---
phase('Scoperta')
const disc = await robustAgent(discoveryPrompt(), { label: 'scopri-ruoli', phase: 'Scoperta', schema: DISCOVERY_SCHEMA, agentType: 'general-purpose' })
if (!disc) {
  log('ATTENZIONE: scoperta ruoli non riuscita dopo i retry. Interrompo: senza il manifesto non so chi rivede.')
  return { errore: 'scoperta ruoli fallita (manifesto ' + MANIFESTO + ' non leggibile dopo ' + RETRIES + ' tentativi)' }
}
const all = ((disc && disc.tutte_le_skill) || []).filter(Boolean)
const autore = (disc && disc.autore) || 'procedure'
// LIVELLI ESPLICITI dal manifesto, filtrati sulle cartelle realmente presenti e senza sovrapposizioni tra livelli.
const firstKeys = ((disc && disc.primo_livello) || []).filter((k) => all.includes(k) && k !== autore)
const secondKeys = ((disc && disc.secondo_livello) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k))
const thirdKeys = ((disc && disc.terzo_livello) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k))
const fourthKeys = ((disc && disc.quarto_livello) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k) && !thirdKeys.includes(k))

const mk = (k) => ({ key: k, skill: SK + '/direttore-osteopatico-' + k })
const REVIEWERS = firstKeys.map(mk)  // 1o livello
const SECOND = secondKeys.map(mk)    // 2o livello
const THIRD = thirdKeys.map(mk)      // 3o livello (logica dell'apprendimento)
const FOURTH = fourthKeys.map(mk)    // 4o livello (editor di asciugatura)

// Segnala eventuali skill-revisore presenti nella cartella ma non assegnate a nessun livello: niente cali silenziosi.
const assegnate = new Set([autore, ...firstKeys, ...secondKeys, ...thirdKeys, ...fourthKeys])
const nonAssegnate = all.filter((k) => !assegnate.has(k))
if (nonAssegnate.length) log(`ATTENZIONE: skill presenti ma non assegnate a nessun livello nel manifesto (ignorate): ${nonAssegnate.join(', ')}`)

if (!REVIEWERS.length && !SECOND.length && !THIRD.length && !FOURTH.length) {
  log('ATTENZIONE: nessun revisore dichiarato nel manifesto. Interrompo.')
  return { errore: 'nessun revisore in primo/secondo/terzo/quarto_livello del manifesto ' + MANIFESTO }
}
log(`Autore: ${autore} | 1o (${REVIEWERS.length}): ${REVIEWERS.map((r) => r.key).join(', ') || '—'} | 2o (${SECOND.length}): ${SECOND.map((r) => r.key).join(', ') || '—'} | 3o (${THIRD.length}): ${THIRD.map((r) => r.key).join(', ') || '—'} | 4o (${FOURTH.length}): ${FOURTH.map((r) => r.key).join(', ') || '—'}`)

const results = await pipeline(
  slugs,

  // --- STAGE 1: DRAFT (v1) ---
  async (slug) => {
    const r = await robustAgent(draftPrompt(slug), { label: `draft:${slug}`, phase: 'Draft', agentType: 'general-purpose' })
    // Il draft e l'unico stadio senza fallback: senza bozza non c'e nulla da revisionare.
    // Il throw qui, dentro pipeline(), scarta SOLO questo slug (gli altri proseguono) — non e un abort globale.
    if (!r) { log(`ATTENZIONE: draft non riuscito per ${slug} dopo ${RETRIES} tentativi — salto SOLO questo slug`); throw new Error(`draft fallito per ${slug}`) }
    log(`Draft pronto: ${slug}`)
    return slug
  },

  // --- STAGE 2: REVISIONE 1o LIVELLO (in parallelo, gia resiliente: un revisore che cade -> null, gli altri restano) ---
  async (slug) => {
    const fbs = await parallel(
      REVIEWERS.map((rv) => () =>
        agent(reviewPrompt(slug, rv), { label: `rev1:${rv.key}:${slug}`, phase: 'Revisione', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
      )
    )
    const ok = fbs.filter(Boolean).length
    log(`Revisione 1o livello ${slug}: ${ok}/${REVIEWERS.length}${ok === 0 ? ' — nessun feedback: la sintesi promuovera la v1' : ''}`)
    return slug
  },

  // --- STAGE 3: SINTESI INTERMEDIA (v2) — retry, poi fallback: promuove v1 se la sintesi non riesce ---
  async (slug) => {
    const r = await robustAgent(synthPrompt(slug), { label: `sintesi-v2:${slug}`, phase: 'Sintesi intermedia', agentType: 'general-purpose' })
    if (!r) await promote(`${OUT}/${slug}/v1-draft.md`, `${OUT}/${slug}/v1-scheda.md`, `${OUT}/${slug}/v2-intermedia.md`, `${OUT}/${slug}/scheda-v2.md`, `sintesi v2 non riuscita per ${slug}`)
    else log(`v2 pronta: ${slug}`)
    return slug
  },

  // --- STAGE 4: REVISIONE 2o LIVELLO -> SINTESI v3 (retry + fallback: promuove v2) ---
  async (slug) => {
    if (!SECOND.length) {
      await promote(`${OUT}/${slug}/v2-intermedia.md`, `${OUT}/${slug}/scheda-v2.md`, `${OUT}/${slug}/v3-intermedia.md`, `${OUT}/${slug}/scheda-v3.md`, `nessun 2o livello per ${slug}`)
      log(`v3 (= v2, nessun 2o livello): ${slug}`)
      return slug
    }
    const fbs = await parallel(
      SECOND.map((rv) => () =>
        agent(secondReviewPrompt(slug, rv), { label: `rev2:${rv.key}:${slug}`, phase: 'Revisione 2o livello', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
      )
    )
    log(`Revisione 2o livello ${slug}: ${fbs.filter(Boolean).length}/${SECOND.length}`)
    const r = await robustAgent(thirdSynthPrompt(slug), { label: `sintesi-v3:${slug}`, phase: 'Sintesi v3', agentType: 'general-purpose' })
    if (!r) await promote(`${OUT}/${slug}/v2-intermedia.md`, `${OUT}/${slug}/scheda-v2.md`, `${OUT}/${slug}/v3-intermedia.md`, `${OUT}/${slug}/scheda-v3.md`, `sintesi v3 non riuscita per ${slug}`)
    else log(`v3 pronta: ${slug}`)
    return slug
  },

  // --- STAGE 5: REVISIONE 3o LIVELLO (apprendimento) -> SINTESI v4 (retry + fallback: promuove v3) ---
  async (slug) => {
    if (!THIRD.length) {
      await promote(`${OUT}/${slug}/v3-intermedia.md`, `${OUT}/${slug}/scheda-v3.md`, `${OUT}/${slug}/v4-intermedia.md`, `${OUT}/${slug}/scheda-v4.md`, `nessun 3o livello per ${slug}`)
      log(`v4 (= v3, nessun 3o livello): ${slug}`)
      return slug
    }
    const fbs = await parallel(
      THIRD.map((rv) => () =>
        agent(thirdReviewPrompt(slug, rv), { label: `rev3:${rv.key}:${slug}`, phase: 'Revisione 3o livello', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
      )
    )
    log(`Revisione 3o livello ${slug}: ${fbs.filter(Boolean).length}/${THIRD.length}`)
    const r = await robustAgent(fourthSynthPrompt(slug), { label: `sintesi-v4:${slug}`, phase: 'Sintesi v4', agentType: 'general-purpose' })
    if (!r) await promote(`${OUT}/${slug}/v3-intermedia.md`, `${OUT}/${slug}/scheda-v3.md`, `${OUT}/${slug}/v4-intermedia.md`, `${OUT}/${slug}/scheda-v4.md`, `sintesi v4 non riuscita per ${slug}`)
    else log(`v4 pronta: ${slug}`)
    return slug
  },

  // --- STAGE 6: REVISIONE 4o LIVELLO (editor) -> SINTESI FINALE (v5) (retry + fallback: promuove v4) ---
  async (slug) => {
    if (!FOURTH.length) {
      await promote(`${OUT}/${slug}/v4-intermedia.md`, `${OUT}/${slug}/scheda-v4.md`, `${OUT}/${slug}/v5-finale.md`, `${OUT}/${slug}/scheda-finale.md`, `nessun 4o livello per ${slug}`)
      log(`FINALE (v5 = v4, nessun 4o livello): ${slug}`)
      return { slug, esito: 'completata (senza 4o livello)' }
    }
    const fbs = await parallel(
      FOURTH.map((rv) => () =>
        agent(fourthReviewPrompt(slug, rv), { label: `rev4:${rv.key}:${slug}`, phase: 'Revisione 4o livello', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
      )
    )
    log(`Revisione 4o livello ${slug}: ${fbs.filter(Boolean).length}/${FOURTH.length}`)
    const r = await robustAgent(finalSynthPrompt(slug), { label: `sintesi-finale:${slug}`, phase: 'Sintesi finale', agentType: 'general-purpose' })
    if (!r) {
      await promote(`${OUT}/${slug}/v4-intermedia.md`, `${OUT}/${slug}/scheda-v4.md`, `${OUT}/${slug}/v5-finale.md`, `${OUT}/${slug}/scheda-finale.md`, `sintesi finale non riuscita per ${slug}`)
      return { slug, esito: 'completata (v5=v4, sintesi finale promossa dopo i retry)' }
    }
    log(`FINALE (v5) pronta: ${slug}`)
    return { slug, esito: 'completata' }
  }
)

return results.filter(Boolean)

export const meta = {
  name: 'riprendi-procedura-osteopatica',
  description: 'Riprende UNA procedura interrotta dallo stato reale della cartella: rileva quali file esistono gia e riesegue SOLO gli stadi mancanti, fino alla v5 finale. Nessun lavoro gia fatto viene rifatto.',
  whenToUse: 'Quando una catena di genera-procedure.workflow.js si e interrotta (limite di sessione, errore, stop) e va ripresa da dove era arrivata. Un solo slug per volta.',
  phases: [
    { title: 'Stato', detail: 'ruoli dal manifesto + inventario dei file gia prodotti' },
    { title: 'Draft', detail: 'completa la v1 solo se manca (procedura e/o scheda)' },
    { title: 'Revisione', detail: 'solo i revisori di 1o livello il cui feedback manca' },
    { title: 'Sintesi intermedia', detail: 'v2 + scheda-v2, solo se mancanti' },
    { title: 'Revisione 2o livello', detail: 'fedelta al metodo sulla v2' },
    { title: 'Sintesi v3', detail: 'applica i feedback di 2o livello' },
    { title: 'Revisione 3o livello', detail: 'logica dell apprendimento sulla v3' },
    { title: 'Sintesi v4', detail: 'applica i rilievi di apprendimento' },
    { title: 'Revisione 4o livello', detail: 'editor di asciugatura sulla v4' },
    { title: 'Sintesi finale', detail: 'applica la mappa di taglio -> v5 finale' },
  ],
}

// ---- percorsi (assoluti: i subagent non ereditano la working dir) ----
const ROOT = '/Users/carlitos/mobilitas-agenti-ai/agente-creazione-procedure'
const SK = ROOT + '/.claude/skills'
const AUTORE = SK + '/direttore-osteopatico-procedure'
const OUT = ROOT + '/procedure-generate'
const DATA = OUT + '/_dati/problemi.json'
const DEVIAZIONI = OUT + '/_dati/deviazioni-dal-metodo.md'
const MANIFESTO = OUT + '/_dati/livelli.json'

// ---- NORMALIZZAZIONE ARGS ----
// Il bug che ha rotto il batch del 18/08: args arrivava come STRINGA JSON ('["lombalgia"]')
// invece che come array, quindi lo slug diventava letteralmente '["lombalgia"]' e le cartelle
// si chiamavano ["lombalgia"]. Qui la stringa viene riconosciuta e riportata a slug pulito.
function normalizeSlug(a) {
  let v = a
  if (Array.isArray(v)) v = v[0]
  if (typeof v !== 'string') return null
  v = v.trim()
  if (v.startsWith('[') || v.startsWith('"')) {
    try {
      const p = JSON.parse(v)
      v = Array.isArray(p) ? String(p[0]) : String(p)
    } catch (e) {
      v = v.replace(/^\[+/, '').replace(/\]+$/, '').replace(/^"+/, '').replace(/"+$/, '')
    }
  }
  return v.trim() || null
}

// args accetta due forme:
//   "lombalgia"                                  → lo stato lo scopre un agente
//   { slug: "lombalgia", stato: {...} }           → lo stato e' GIA' fornito dal chiamante
// La seconda forma esiste perche' l'agente di stato era un punto di rottura singolo: quando
// l'API rifiuta (529), tutta la catena si fermava prima di cominciare. Lo stato si ricava con
// un `ls`, cioe' senza consumare agenti: chi lancia il workflow puo' passarlo e saltare il giro.
const argObj = (args && typeof args === 'object' && !Array.isArray(args)) ? args : null
const statoFornito = argObj && argObj.stato ? argObj.stato : null
const slug = normalizeSlug(argObj ? argObj.slug : args)
if (!slug) {
  log('Nessuno slug. Passa args: "lombalgia" (una procedura per volta).')
  return { errore: 'args vuoto o non interpretabile' }
}
const DIR = OUT + '/' + slug

// ============================ SCHEMI ============================

const DISCOVERY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['tutte_le_skill', 'autore', 'primo_livello', 'secondo_livello', 'terzo_livello', 'quarto_livello', 'file_presenti'],
  properties: {
    tutte_le_skill: { type: 'array', items: { type: 'string' }, description: 'Chiavi (dopo "direttore-osteopatico-") di TUTTE le cartelle skill presenti' },
    autore: { type: 'string' },
    primo_livello: { type: 'array', items: { type: 'string' } },
    secondo_livello: { type: 'array', items: { type: 'string' } },
    terzo_livello: { type: 'array', items: { type: 'string' } },
    quarto_livello: { type: 'array', items: { type: 'string' } },
    file_presenti: { type: 'array', items: { type: 'string' }, description: 'Nomi esatti dei file presenti nella cartella della procedura (solo basename, non i path). Array vuoto se la cartella non esiste.' },
  },
}

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
          sezione: { type: 'string' },
          problema: { type: 'string' },
          correzione: { type: 'string' },
        },
      },
    },
  },
}

// ============================ PROMPT ============================

const statePrompt = () => `Devi fotografare lo stato di lavorazione di una procedura e i ruoli delle skill.

1) Esegui: ls -1 ${SK}
   Prendi TUTTE le cartelle che iniziano con "direttore-osteopatico-" e per ognuna estrai la chiave = la parte dopo quel prefisso (es. "direttore-osteopatico-compliance" -> "compliance"). Questo e "tutte_le_skill".
2) Leggi il manifesto ${MANIFESTO} (JSON). Prendi "autore", "primo_livello", "secondo_livello", "terzo_livello", "quarto_livello" (array di chiavi; un array mancante o vuoto -> []).
3) Esegui: ls -1 ${DIR}
   Restituisci in "file_presenti" i BASENAME esatti di tutti i file presenti (es. "v1-draft.md", "feedback-compliance.md"). Se la cartella non esiste, restituisci [].

Regole: usa SOLO cartelle skill realmente presenti; non inventare chiavi ne nomi di file; riporta i quattro livelli come stanno nel manifesto (filtrati sulle cartelle esistenti).`

const draftPrompt = () => `Sei il **Direttore Osteopatico** di Mobilitas (OsteoTouch). Devi redigere la procedura clinica per il problema con slug "${slug}".

## Istruzioni della skill (leggile e seguile INTEGRALMENTE, in quest'ordine)
1. Leggi ${AUTORE}/SKILL.md
2. Poi leggi i reference che la SKILL indica, ALMENO: dna-editoriale.md (voce, prima di scrivere), architettura-procedura.md (struttura fissa), cinque-modelli-osteopatici.md (impalcatura Parte 0, leggila per prima) e fase-0-piramide-del-comando.md (il Motore Clinico, ragionamento implicito), ancore-verificate.md e ancore-scientifiche.md (ancora scientifica), scheda-operativa.md, integrazione-gestionale.md, sistema-libreria.md, esempio-canonico-acufeni.md SOLO per voce/ritmo (precede l'inversione: NON copiarne i claim gonfiati) ed esempio-reflusso.md (voce, caso a evidenza sottile). Sono in ${AUTORE}/references/. Per l'IMPIANTO Parte 0 allineato allo standard il modello e' ${OUT}/reflusso/procedura-reflusso.md

## Precedenza scientifica — leggi PRIMA di scrivere
Apri ${DEVIAZIONI}. **L'accuratezza scientifica viene prima della fedelta' al metodo**: dove le due confliggono, scrivi la versione corretta, non quella fedele. Se ne trovi uno NUOVO: correggi e apri una voce con stato PROPOSTA e la fonte; NON modificare i documenti di metodo.

## Dati del problema
Apri ${DATA}, trova l'oggetto con "slug": "${slug}" e usa TUTTI i suoi campi come materia prima.

## Ricerca scientifica — OBBLIGATORIA
Prima di scrivere la sezione evidenza DEVI cercare sul web e verificare ogni studio: titolo/autore/anno/PMID reali. Se non verifichi uno studio, non citarlo. Scegli l'ancora scientifica (un ricercatore reale, vivente, il piu autorevole al mondo in terapia manuale su questa condizione).

## Output
- ${DIR}/v1-draft.md  → la procedura completa (architettura fissa Parte 0 + I-IV), ~5.000-7.000 parole
- ${DIR}/v1-scheda.md → la Scheda Operativa (una pagina, sei blocchi)
Non convertire in .docx. Alla fine restituisci SOLO: numero parole + ancora scientifica scelta + una riga di note.`

// Genera SOLO la Scheda Operativa da una procedura gia scritta. Serve quando la catena
// si e interrotta dopo la procedura ma prima della scheda: si recupera senza riscrivere la procedura.
const schedaPrompt = (procFile, schedaFile, etichetta) => `Sei il **Direttore Osteopatico** di Mobilitas. La procedura "${slug}" (versione ${etichetta}) e gia scritta, ma manca la sua **Scheda Operativa**: la catena si e interrotta a meta. Devi produrre SOLO la scheda, senza toccare la procedura.

## Metodo
Leggi ${AUTORE}/SKILL.md e soprattutto ${AUTORE}/references/scheda-operativa.md (la specifica: una pagina, sei blocchi fissi). Per voce e ritmo guarda una scheda gia approvata: ${OUT}/acufeni/scheda-finale.md.

## Input
La procedura da cui ricavare la scheda: ${DIR}/${procFile}. Leggila TUTTA. La scheda e l'estratto operativo di QUESTA versione: test, tecniche, dosi, red flag e scale devono combaciare esattamente con quello che c'e scritto li. Non inventare nulla che non sia gia nella procedura.

## Output
- ${DIR}/${schedaFile} → la Scheda Operativa (una pagina, sei blocchi)
NON modificare ${DIR}/${procFile}. Restituisci SOLO: numero di parole della scheda e i sei blocchi che hai prodotto, in una riga.`

const reviewPrompt = (r) => `Sei il revisore **${r.key}** del panel avversariale Mobilitas (PRIMO livello). Devi revisionare una procedura clinica osteopatica.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md (e i suoi reference se ne cita). Adotta esattamente quella prospettiva, con lo stesso obbligo di ricerca e la stessa severita.

## Documento da revisionare
Leggi ${DIR}/v1-draft.md (la procedura) e ${DIR}/v1-scheda.md (la scheda). Se non esistono, restituisci un rilievo ERRORE che dice che il draft manca.

## Output
Classifica OGNI rilievo per severita: ERRORE (fatto sbagliato/pericoloso, va corretto), RISCHIO (esposizione da valutare), PREFERENZA (gusto, ignorabile). Sii chirurgico: sezione precisa, problema, correzione concreta. Non riscrivere la procedura, non elogiare: solo rilievi azionabili.

Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa leggibile in ${DIR}/feedback-${r.key}.md`

const synthPrompt = () => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la versione INTERMEDIA (v2) della procedura "${slug}" sintetizzando i feedback dei revisori di 1o livello. NON e ancora la finale: dopo di te la v2 va al 2o livello.

## Metodo di sintesi (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Regola che protegge il documento: **il feedback si pesa, non si somma**. ERRORE si corregge; RISCHIO si valuta; PREFERENZA si ignora di default. Elimina i doppioni e i conflitti tra lenti. Se la procedura cresce oltre il 20%, hai sommato invece di pesare: ferma e ripesa.

## Input
- Draft: ${DIR}/v1-draft.md e ${DIR}/v1-scheda.md
- Feedback: leggi TUTTI i file ${DIR}/feedback-*.md (uno per revisore, esclusi quelli che finiscono in -r2.md, -r3.md o -r4.md)

## Output
- ${DIR}/v2-intermedia.md → procedura intermedia
- ${DIR}/scheda-v2.md     → scheda intermedia
Scrivi ENTRAMBI i file: una versione senza la sua scheda e incompleta.

Restituisci SOLO: cosa hai corretto (ERRORI), cosa hai valutato (RISCHI), cosa hai ignorato (PREFERENZE), variazione % di lunghezza.`

const secondReviewPrompt = (r) => `Sei il revisore di SECONDO LIVELLO **${r.key}** del panel Mobilitas. Questa e la SECONDA passata: la procedura e gia stata revisionata da tutti i revisori di 1o livello e riscritta una volta.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md (e i suoi reference se ne cita).

## Precedenza scientifica — vincolo che sovrascrive la fedelta' al metodo
Apri ${DEVIAZIONI} PRIMA di formulare rilievi. Stato RATIFICATA = la deviazione e lo standard. Stato PROPOSTA = marcala "DEVIAZIONE MOTIVATA" e passa oltre. Stato RESPINTA = vince il metodo.
Regola generale: **quando il metodo prescrive un contenuto contraddetto dalla fisiologia o dall'evidenza, vince l'accuratezza scientifica**. Se trovi una deviazione fondata ma NON registrata, marcala "DEVIAZIONE MOTIVATA — non registrata".

## Documento da revisionare
Leggi ${DIR}/v2-intermedia.md e ${DIR}/scheda-v2.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v2 manca.

## Output
Classifica OGNI rilievo per severita: ERRORE / RISCHIO / PREFERENZA. Sii chirurgico. Non riscrivere la procedura.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${DIR}/feedback-${r.key}-r2.md`

const thirdSynthPrompt = () => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la v3 della procedura "${slug}", applicando i feedback della revisione di 2o livello alla v2. NON e ancora la finale.

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. **Il feedback si pesa, non si somma**. Parti dalla v2, non dalla bozza.

## Input
- ${DIR}/v2-intermedia.md e ${DIR}/scheda-v2.md
- Feedback della 2a passata: leggi TUTTI i file ${DIR}/feedback-*-r2.md

## Output
- ${DIR}/v3-intermedia.md → procedura v3
- ${DIR}/scheda-v3.md     → scheda v3
Scrivi ENTRAMBI i file.

Restituisci SOLO: cosa hai corretto dalla 2a revisione, cosa hai valutato/ignorato, variazione % di lunghezza rispetto alla v2.`

const thirdReviewPrompt = (r) => `Sei il revisore di TERZO LIVELLO **${r.key}** del panel Mobilitas — la logica dell'apprendimento. Contenuto, sicurezza, compliance e fedelta al metodo sono chiusi. Tu guardi il documento come PERCORSO DI APPRENDIMENTO: chi legge impara davvero a fare, o impara solo a eseguire?

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md e il suo reference ${r.skill}/references/sei-fasi-apprendimento.md. La legge e la sequenza: **perche -> cosa -> come -> pratica -> feedback -> autonomia**. Trova i gradini mancanti, invertiti o solo accennati, e di dove vanno rimessi.

## Tre confini rigidi
1. **Non aggiungi contenuto clinico**: niente tecniche, dosi, studi, red flag o cautele nuove. Se una fase manca, la costruisci con il materiale gia presente, spostandolo.
2. **Non asciughi**: dopo di te c'e l'editor (4o livello). Una ripetizione con funzione didattica e un pregio: segnalala tra le cose DA PROTEGGERE.
3. **Non gonfi**: preferisci lo spostamento all'aggiunta. Ogni rilievo che aggiunge testo dichiara quante parole costa. Crescita netta **<= 5%**.

Rispetta l'INTOCCABILE (red flag, criteri di invio, controindicazioni, screening, stop-rule, dosi, PMID/dati, hedge di compliance, le tre voci, l'architettura fissa Parte 0/I/II/III/IV). Se il documento gia insegna, il verdetto legittimo e "Insegna".

## Documento da revisionare
Leggi ${DIR}/v3-intermedia.md e ${DIR}/scheda-v3.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v3 manca.

## Output
**ERRORE** = una fase e assente o invertita in modo che rompe l'apprendimento. **RISCHIO** = la fase c'e ma e debole o lontana dal punto d'uso. **PREFERENZA** = gusto didattico (max 3). Per ogni rilievo: fase mancante, sezione OSPITE gia esistente dove rimetterla, cosa fare, costo in parole.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${DIR}/feedback-${r.key}-r3.md, includendo la mappa delle sei fasi (presente/debole/assente), la sezione **Da proteggere dall'editor** e il bilancio parole.`

const fourthSynthPrompt = () => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la v4 della procedura "${slug}", applicando i rilievi del revisore della logica dell'apprendimento (3o livello) alla v3.

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Parti dalla v3.

Regola specifica di questo livello: **prima si sposta, poi si riscrive, solo in ultimo si aggiunge**. NON introdurre contenuto clinico nuovo. Crescita netta ammessa rispetto alla v3: **massimo 5%**.

## Input
- ${DIR}/v3-intermedia.md e ${DIR}/scheda-v3.md
- Rilievi di apprendimento: leggi TUTTI i file ${DIR}/feedback-*-r3.md

## Output
- ${DIR}/v4-intermedia.md → procedura v4
- ${DIR}/scheda-v4.md     → scheda v4
Scrivi ENTRAMBI i file.

Restituisci SOLO: quali fasi hai colmato e come (spostamento / riscrittura / aggiunta), cosa hai ignorato, la variazione % rispetto alla v3, e l'elenco dei passaggi marcati **da proteggere dall'editor**.`

const fourthReviewPrompt = (r) => `Sei il revisore di QUARTO LIVELLO **${r.key}** del panel Mobilitas — l'editor di asciugatura. Contenuto, sicurezza, compliance, fedelta al metodo e impianto didattico sono chiusi. Tu NON aggiungi ne contesti la sostanza: produci una MAPPA DI TAGLIO per riportare il documento nel range 5.000-7.000 parole senza perdere informazione clinica/sicurezza/legale/metodo e senza spegnere la voce.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md. Rispetta l'INTOCCABILE (red flag, controindicazioni, screening, stop-rule, dosi, PMID/dati, hedge di compliance, le tre voci). Se il documento e gia tra 5.000 e 7.000 parole di PROSA (non contare le celle delle tabelle) e non trovi ridondanza vera, il verdetto legittimo e "Gia asciutta".

## Vincolo aggiuntivo: il lavoro del 3o livello
Leggi anche i file ${DIR}/feedback-*-r3.md e in particolare la loro sezione **Da proteggere dall'editor**. Quei passaggi hanno funzione didattica: una ripetizione che ancora il senso al punto d'uso NON e ridondanza. Se ritieni comunque che vada tagliato, classificalo al massimo come PREFERENZA e motiva.

## Documento da revisionare
Leggi ${DIR}/v4-intermedia.md e ${DIR}/scheda-v4.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v4 manca.

## Output
**RIDONDANTE -> ERRORE** (taglio sicuro, l'info esiste identica altrove), **COMPRIMIBILE -> RISCHIO** (stessa sostanza in meno parole), **PREFERENZA -> PREFERENZA**. Per ogni rilievo indica sezione/passaggio, cosa tagliare o come comprimere, e dove resta l'informazione. Non riscrivere la procedura.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${DIR}/feedback-${r.key}-r4.md`

const finalSynthPrompt = () => `Sei il **Direttore Osteopatico** di Mobilitas. Devi chiudere la versione FINALE (v5) della procedura "${slug}", applicando la mappa di taglio dell'editor (4o livello) alla v4.

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Regola: **si asciuga solo se strettamente necessario**. Applica i tagli RIDONDANTE; valuta i COMPRIMIBILE solo se servono a rientrare nel range 5.000-7.000 parole di prosa; ignora le PREFERENZE di default. NON toccare l'INTOCCABILE (red flag, sicurezza, dosi, PMID, hedge, le tre voci) ne i passaggi marcati **da proteggere** nei feedback di 3o livello (${DIR}/feedback-*-r3.md). Se la v4 e gia asciutta, copiala nella v5 senza modifiche.

## Input
- ${DIR}/v4-intermedia.md e ${DIR}/scheda-v4.md
- Mappa di taglio: leggi TUTTI i file ${DIR}/feedback-*-r4.md
- Da proteggere: la sezione omonima nei file ${DIR}/feedback-*-r3.md

## Output
- ${DIR}/v5-finale.md     → procedura FINALE da consegnare
- ${DIR}/scheda-finale.md → scheda FINALE
Scrivi ENTRAMBI i file.

## Cancello di qualita — prima di chiudere
Applica ${AUTORE}/references/rubrica-punteggio.md (sotto 90/100 non si consegna) e ${AUTORE}/references/checklist-qualita.md. Se un punto fallisce, correggilo tu prima di consegnare.

Restituisci SOLO: cosa hai tagliato, cosa hai compresso o lasciato, cosa hai protetto su indicazione del 3o livello, il punteggio della rubrica e il conteggio parole finale.`

const promotePrompt = (procIn, schedaIn, procOut, schedaOut) =>
  `Copia senza modifiche ${procIn} in ${procOut} e ${schedaIn} in ${schedaOut}. Poi conferma in una riga.`

// ============================ RESILIENZA ============================
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

// Avvisi che DEVONO arrivare all'umano: ogni volta che un pezzo non e' stato prodotto,
// o e' stato prodotto senza conferma, qui resta la traccia. Il valore di ritorno del
// workflow non deve mai dichiarare "completata" cio' che non e' confermato.
const warnings = []

async function promote(procIn, schedaIn, procOut, schedaOut, motivo) {
  log(`  [resilienza] ${motivo}: promuovo ${procIn.split('/').pop()} -> ${procOut.split('/').pop()} senza modifiche`)
  const r = await robustAgent(
    promotePrompt(procIn, schedaIn, procOut, schedaOut),
    { label: `promuovi:${procOut.split('/').pop()}`, phase: 'Sintesi finale', agentType: 'general-purpose' },
    2
  )
  // BUG STORICO (18/08/2026, bruxismo): la promozione falliva e il workflow restituiva comunque
  // "completata (promossa dalla v4)". Il file non c'era. Da qui in poi il fallimento e' esplicito.
  if (!r) {
    const msg = `PROMOZIONE NON CONFERMATA verso ${procOut.split('/').pop()} (${motivo}) — il file potrebbe NON esistere: verificalo a mano`
    log(`  [resilienza] ATTENZIONE: ${msg}`)
    warnings.push(msg)
  }
  return r
}

// ============================ ORCHESTRAZIONE ============================

phase('Stato')
log(`Riprendo la procedura "${slug}" dallo stato reale della cartella.`)

let st = statoFornito
if (st) log('Stato fornito dal chiamante: salto l\'agente di scoperta (nessun token speso).')
else {
  st = await robustAgent(statePrompt(), { label: `stato:${slug}`, phase: 'Stato', schema: DISCOVERY_SCHEMA, agentType: 'general-purpose' })
  if (!st) {
    log('ATTENZIONE: non sono riuscito a leggere stato e manifesto. Interrompo.')
    log('Rimedio: rilancia passando lo stato a mano — args: { slug, stato: { tutte_le_skill, autore, primo_livello, secondo_livello, terzo_livello, quarto_livello, file_presenti } }')
    return { errore: 'lettura stato/manifesto fallita dopo ' + RETRIES + ' tentativi (puoi passare "stato" negli args per saltare questo agente)' }
  }
}

const all = (st.tutte_le_skill || []).filter(Boolean)
const autore = st.autore || 'procedure'
const firstKeys = (st.primo_livello || []).filter((k) => all.includes(k) && k !== autore)
const secondKeys = (st.secondo_livello || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k))
const thirdKeys = (st.terzo_livello || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k))
const fourthKeys = (st.quarto_livello || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k) && !thirdKeys.includes(k))

const mk = (k) => ({ key: k, skill: SK + '/direttore-osteopatico-' + k })
const REVIEWERS = firstKeys.map(mk)
const SECOND = secondKeys.map(mk)
const THIRD = thirdKeys.map(mk)
const FOURTH = fourthKeys.map(mk)

// --- inventario: cosa esiste gia ---
const files = new Set(st.file_presenti || [])
const has = (f) => files.has(f)
log(`File gia presenti in ${slug}/: ${files.size ? [...files].sort().join(', ') : '(cartella vuota o inesistente)'}`)
log(`Autore: ${autore} | 1o (${REVIEWERS.length}) | 2o (${SECOND.length}) | 3o (${THIRD.length}) | 4o (${FOURTH.length})`)

const fatto = []
const saltato = []

// --- STADIO 1: v1 (procedura + scheda) ---
phase('Draft')
if (!has('v1-draft.md')) {
  const r = await robustAgent(draftPrompt(), { label: `draft:${slug}`, phase: 'Draft', agentType: 'general-purpose' })
  if (!r) { log(`Draft non riuscito per ${slug}: senza bozza non c'e nulla da revisionare. Interrompo.`); return { slug, errore: 'draft fallito' } }
  fatto.push('v1 (procedura + scheda)')
} else if (!has('v1-scheda.md')) {
  // Caso tipico dell'interruzione: la procedura c'e, la scheda no.
  log('v1-draft.md c\'e ma manca v1-scheda.md: genero solo la scheda, senza riscrivere la procedura.')
  const r = await robustAgent(schedaPrompt('v1-draft.md', 'v1-scheda.md', 'v1'), { label: `scheda-v1:${slug}`, phase: 'Draft', agentType: 'general-purpose' })
  if (!r) { log('Scheda v1 non riuscita: la revisione di 1o livello la richiede. Interrompo.'); return { slug, errore: 'scheda v1 fallita' } }
  fatto.push('v1-scheda (recuperata)')
} else {
  saltato.push('Draft (v1 gia completa)')
  log('v1 gia completa: salto il draft.')
}

// --- STADIO 2: revisione 1o livello (solo i revisori il cui feedback manca) ---
phase('Revisione')
const mancanti1 = REVIEWERS.filter((rv) => !has(`feedback-${rv.key}.md`))
if (mancanti1.length) {
  log(`Revisione 1o livello: ${REVIEWERS.length - mancanti1.length}/${REVIEWERS.length} gia fatti, lancio i ${mancanti1.length} mancanti (${mancanti1.map((r) => r.key).join(', ')}).`)
  const fbs = await parallel(mancanti1.map((rv) => () =>
    agent(reviewPrompt(rv), { label: `rev1:${rv.key}:${slug}`, phase: 'Revisione', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
  ))
  log(`Revisione 1o livello completata: ${fbs.filter(Boolean).length}/${mancanti1.length} nuovi feedback.`)
  fatto.push(`revisione 1o livello (${mancanti1.length} revisori)`)
} else {
  saltato.push(`Revisione 1o livello (${REVIEWERS.length} feedback gia presenti)`)
  log(`Revisione 1o livello gia completa (${REVIEWERS.length} feedback): salto.`)
}

// --- STADIO 3: sintesi v2 ---
phase('Sintesi intermedia')
if (has('v2-intermedia.md') && has('scheda-v2.md')) {
  saltato.push('Sintesi v2 (gia completa)')
  log('v2 gia completa: salto la sintesi.')
} else if (has('v2-intermedia.md') && !has('scheda-v2.md')) {
  // Esattamente il punto in cui il limite di sessione ha troncato il batch del 18/08.
  log('v2-intermedia.md c\'e ma manca scheda-v2.md: genero solo la scheda, la procedura v2 resta intatta.')
  const r = await robustAgent(schedaPrompt('v2-intermedia.md', 'scheda-v2.md', 'v2'), { label: `scheda-v2:${slug}`, phase: 'Sintesi intermedia', agentType: 'general-purpose' })
  if (!r) await promote(`${DIR}/v2-intermedia.md`, `${DIR}/v1-scheda.md`, `${DIR}/v2-intermedia.md`, `${DIR}/scheda-v2.md`, 'scheda v2 non riuscita')
  fatto.push('scheda-v2 (recuperata)')
} else {
  const r = await robustAgent(synthPrompt(), { label: `sintesi-v2:${slug}`, phase: 'Sintesi intermedia', agentType: 'general-purpose' })
  if (!r) await promote(`${DIR}/v1-draft.md`, `${DIR}/v1-scheda.md`, `${DIR}/v2-intermedia.md`, `${DIR}/scheda-v2.md`, 'sintesi v2 non riuscita')
  fatto.push('v2')
}

// --- STADIO 4: 2o livello -> v3 ---
if (has('v3-intermedia.md') && has('scheda-v3.md')) {
  saltato.push('2o livello + v3 (gia fatti)')
  log('v3 gia presente: salto il 2o livello.')
} else if (!SECOND.length) {
  await promote(`${DIR}/v2-intermedia.md`, `${DIR}/scheda-v2.md`, `${DIR}/v3-intermedia.md`, `${DIR}/scheda-v3.md`, 'nessun 2o livello')
} else {
  phase('Revisione 2o livello')
  const mancanti2 = SECOND.filter((rv) => !has(`feedback-${rv.key}-r2.md`))
  if (mancanti2.length) {
    const fbs = await parallel(mancanti2.map((rv) => () =>
      agent(secondReviewPrompt(rv), { label: `rev2:${rv.key}:${slug}`, phase: 'Revisione 2o livello', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
    ))
    log(`Revisione 2o livello: ${fbs.filter(Boolean).length}/${mancanti2.length}`)
  } else log('Feedback di 2o livello gia presenti: salto la revisione, faccio solo la sintesi.')
  phase('Sintesi v3')
  const r = await robustAgent(thirdSynthPrompt(), { label: `sintesi-v3:${slug}`, phase: 'Sintesi v3', agentType: 'general-purpose' })
  if (!r) await promote(`${DIR}/v2-intermedia.md`, `${DIR}/scheda-v2.md`, `${DIR}/v3-intermedia.md`, `${DIR}/scheda-v3.md`, 'sintesi v3 non riuscita')
  fatto.push('2o livello + v3')
}

// --- STADIO 5: 3o livello (apprendimento) -> v4 ---
if (has('v4-intermedia.md') && has('scheda-v4.md')) {
  saltato.push('3o livello + v4 (gia fatti)')
  log('v4 gia presente: salto il 3o livello.')
} else if (!THIRD.length) {
  await promote(`${DIR}/v3-intermedia.md`, `${DIR}/scheda-v3.md`, `${DIR}/v4-intermedia.md`, `${DIR}/scheda-v4.md`, 'nessun 3o livello')
} else {
  phase('Revisione 3o livello')
  const mancanti3 = THIRD.filter((rv) => !has(`feedback-${rv.key}-r3.md`))
  if (mancanti3.length) {
    const fbs = await parallel(mancanti3.map((rv) => () =>
      agent(thirdReviewPrompt(rv), { label: `rev3:${rv.key}:${slug}`, phase: 'Revisione 3o livello', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
    ))
    log(`Revisione 3o livello: ${fbs.filter(Boolean).length}/${mancanti3.length}`)
  } else log('Feedback di 3o livello gia presenti: salto la revisione, faccio solo la sintesi.')
  phase('Sintesi v4')
  const r = await robustAgent(fourthSynthPrompt(), { label: `sintesi-v4:${slug}`, phase: 'Sintesi v4', agentType: 'general-purpose' })
  if (!r) await promote(`${DIR}/v3-intermedia.md`, `${DIR}/scheda-v3.md`, `${DIR}/v4-intermedia.md`, `${DIR}/scheda-v4.md`, 'sintesi v4 non riuscita')
  fatto.push('3o livello + v4')
}

// --- STADIO 6: 4o livello (editor) -> v5 finale ---
if (has('v5-finale.md') && has('scheda-finale.md')) {
  saltato.push('4o livello + v5 (gia fatti)')
  log('v5 finale gia presente: non c\'e nulla da riprendere.')
} else if (!FOURTH.length) {
  await promote(`${DIR}/v4-intermedia.md`, `${DIR}/scheda-v4.md`, `${DIR}/v5-finale.md`, `${DIR}/scheda-finale.md`, 'nessun 4o livello')
} else {
  phase('Revisione 4o livello')
  const mancanti4 = FOURTH.filter((rv) => !has(`feedback-${rv.key}-r4.md`))
  if (mancanti4.length) {
    const fbs = await parallel(mancanti4.map((rv) => () =>
      agent(fourthReviewPrompt(rv), { label: `rev4:${rv.key}:${slug}`, phase: 'Revisione 4o livello', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
    ))
    log(`Revisione 4o livello: ${fbs.filter(Boolean).length}/${mancanti4.length}`)
  } else log('Feedback dell\'editor gia presenti: salto la revisione, faccio solo la sintesi finale.')
  phase('Sintesi finale')
  const r = await robustAgent(finalSynthPrompt(), { label: `sintesi-finale:${slug}`, phase: 'Sintesi finale', agentType: 'general-purpose' })
  if (!r) {
    await promote(`${DIR}/v4-intermedia.md`, `${DIR}/scheda-v4.md`, `${DIR}/v5-finale.md`, `${DIR}/scheda-finale.md`, 'sintesi finale non riuscita')
    fatto.push('4o livello + v5 (promossa dalla v4)')
  } else fatto.push('4o livello + v5 finale')
}

// --- VERIFICA FINALE: i deliverable esistono davvero? ---
// Nessuno stadio sopra puo' garantirlo: gli agenti riferiscono, non provano. Qui si guarda il disco.
// Se la verifica stessa non gira, l'esito si dichiara NON VERIFICATO — mai "completata" per fede.
const VERIFY_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['presenti', 'mancanti'],
  properties: {
    presenti: { type: 'array', items: { type: 'string' } },
    mancanti: { type: 'array', items: { type: 'string' } },
    parole_v5: { type: 'integer', description: 'Conteggio parole di v5-finale.md, 0 se assente' },
  },
}
// BUG STORICO (18/08/2026, cicatrici-cesareo): la verifica controllava solo v5 + scheda finale.
// I livelli 2 e 3 erano caduti sui 529, la v3 e la v4 non esistevano, e la sintesi finale ha
// comunque prodotto una "v5" che era la v2 ritoccata — un documento che NON ha passato due
// revisioni obbligatorie, dichiarato completo. Da qui in poi si verifica la CATENA INTERA:
// se manca un anello intermedio, la v5 non e' una v5, e l'esito lo deve dire.
const atteso = ['v3-intermedia.md', 'scheda-v3.md', 'v4-intermedia.md', 'scheda-v4.md', 'v5-finale.md', 'scheda-finale.md']
const ver = await robustAgent(
  `Esegui: ls -1 ${DIR}
Poi, per ognuno di questi file attesi — ${atteso.join(', ')} — dì se e' PRESENTE o MANCANTE nella cartella.
Se v5-finale.md esiste, contane le parole con: wc -w ${DIR}/v5-finale.md (altrimenti 0).
Restituisci l'oggetto strutturato: "presenti" (gli attesi che ci sono), "mancanti" (gli attesi che non ci sono), "parole_v5". Non inventare: riporta solo cio' che ls mostra.`,
  { label: `verifica:${slug}`, phase: 'Sintesi finale', schema: VERIFY_SCHEMA, agentType: 'general-purpose' }, 2
)

let esito
if (!ver) {
  esito = 'NON VERIFICATO — la verifica finale non ha girato: controlla a mano che v5-finale.md e scheda-finale.md esistano'
  warnings.push(esito)
} else if ((ver.mancanti || []).length) {
  const finaliCiSono = !(ver.mancanti.includes('v5-finale.md') || ver.mancanti.includes('scheda-finale.md'))
  esito = finaliCiSono
    // Il caso peggiore: la v5 c'e' ma la catena sotto no. Il file esiste e sembra buono: non lo e'.
    ? `NON VALIDA — la v5 esiste ma la catena e' rotta, mancano: ${ver.mancanti.join(', ')}. Il documento NON ha passato tutti i livelli: non consegnarlo, rilancia dopo aver rimosso v5-finale.md e scheda-finale.md`
    : `INCOMPLETA — mancano sul disco: ${ver.mancanti.join(', ')}`
  warnings.push(esito)
} else {
  esito = `completata e verificata sul disco (v5: ${ver.parole_v5 || '?'} parole)`
}

return { slug, ripreso_da: [...files].sort(), fatto, saltato, esito, warnings, verifica: ver || 'non eseguita' }

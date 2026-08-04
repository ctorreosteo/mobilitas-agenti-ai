export const meta = {
  name: 'genera-bibbie-osteopatiche',
  description: 'Per ogni condizione: Bibbia teorica (~20 pagine) + Mappa concettuale, revisione su cinque livelli (1o parallelo sul contenuto, 2o fedelta all architettura, 3o logica dell apprendimento, 4o editor di asciugatura, 5o riscrittura integrale in linguaggio semplice), poi COLLAUDO DI CONSERVAZIONE della riscrittura con riparazione mirata. Nessuna versione arriva alla consegna senza cancello. Resiliente: retry sugli agenti critici + fallback di promozione, un singolo fallimento non aborta la catena',
  whenToUse: 'Genera le Bibbie teoriche Mobilitas in batch a partire da PROBLEMI_OSTEOPATIA.xlsx',
  phases: [
    { title: 'Scoperta', detail: 'trova da solo le skill-revisore presenti nella cartella' },
    { title: 'Draft', detail: 'skill direttore-osteopatico-teoria redige v1 Bibbia + Mappa' },
    { title: 'Revisione', detail: 'TUTTI i revisori di 1o livello, in parallelo, feedback per severita' },
    { title: 'Sintesi intermedia', detail: 'skill autore pesa i feedback e riscrive la v2' },
    { title: 'Revisione 2o livello', detail: 'fedelta all architettura della Bibbia, sulla v2' },
    { title: 'Sintesi v3', detail: 'skill autore applica i feedback di 2o livello -> v3' },
    { title: 'Revisione 3o livello', detail: 'logica dell apprendimento, sulla v3' },
    { title: 'Sintesi v4', detail: 'skill autore applica i rilievi di apprendimento -> v4' },
    { title: 'Revisione 4o livello', detail: 'editor di asciugatura, sulla v4' },
    { title: 'Sintesi v5', detail: 'skill autore applica la mappa di taglio dell editor -> v5' },
    { title: 'Riscrittura finale', detail: 'skill chiarezza riscrive TUTTO da capo in linguaggio semplice -> v6' },
    { title: 'Collaudo', detail: 'script deterministico + collaudatore semantico sulla coppia v5/v6; riparazione mirata se serve' },
  ],
}

// ---- percorsi (assoluti: i subagent non ereditano la working dir) ----
const ROOT = '/Users/carlitos/mobilitas-agenti-ai/agente-creazione-teoria'
const SK = ROOT + '/.claude/skills'
const AUTORE = SK + '/direttore-osteopatico-teoria'
const OUT = ROOT + '/bibbie-generate'
const DATA = OUT + '/_dati/problemi.json'
// Registro delle deviazioni dal metodo interno: dove l'architettura e' stata trovata
// fattualmente sbagliata, vince l'accuratezza scientifica. Trasversale a tutte le condizioni.
const DEVIAZIONI = OUT + '/_dati/deviazioni-dal-metodo.md'

// ---- RUOLI E LIVELLI DECISI DAL MANIFESTO, NON DAL CODICE ----
// L'ESISTENZA dei revisori resta auto-scoperta dalla cartella .claude/skills.
// Il RUOLO e il LIVELLO (autore / 1o / 2o / 3o / 4o / 5o livello) li decide ESPLICITAMENTE
// bibbie-generate/_dati/livelli.json. Un revisore presente nella cartella ma non elencato
// NON viene usato. Cosi aggiungi/togli/sposti revisori modificando solo quel file.
const MANIFESTO = OUT + '/_dati/livelli.json'

// Schema della fase di scoperta: cartelle reali + ruoli/livelli espliciti dal manifesto.
const DISCOVERY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['tutte_le_skill', 'autore', 'primo_livello', 'secondo_livello', 'terzo_livello', 'quarto_livello', 'quinto_livello', 'collaudo'],
  properties: {
    tutte_le_skill: { type: 'array', items: { type: 'string' }, description: 'Chiavi (dopo "direttore-osteopatico-") di TUTTE le cartelle skill realmente presenti' },
    autore: { type: 'string', description: 'Chiave dell autore dal manifesto (di norma "teoria")' },
    primo_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di PRIMO livello dal manifesto' },
    secondo_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di SECONDO livello dal manifesto' },
    terzo_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di TERZO livello dal manifesto (di norma "apprendimento")' },
    quarto_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di QUARTO livello dal manifesto (di norma "editor")' },
    quinto_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei riscrittori di QUINTO livello dal manifesto (di norma "chiarezza")' },
    collaudo: { type: 'array', items: { type: 'string' }, description: 'Chiavi del CANCELLO di conservazione dal manifesto (di norma "collaudo"). Non e un livello di revisione: verifica che la riscrittura non abbia perso niente' },
  },
}

const discoveryPrompt = () => `Devi determinare ruoli e livelli delle skill di questo studio combinando la cartella reale e il manifesto.

1) Esegui: ls -1 ${SK}
   Prendi TUTTE le cartelle che iniziano con "direttore-osteopatico-" e per ognuna estrai la chiave = la parte dopo quel prefisso (es. "direttore-osteopatico-compliance" -> "compliance"). Questo e "tutte_le_skill".
2) Leggi il manifesto ${MANIFESTO} (JSON). Prendi "autore" (una chiave), "primo_livello", "secondo_livello", "terzo_livello", "quarto_livello", "quinto_livello" e "collaudo" (array di chiavi; un array puo mancare o essere vuoto -> restituisci []).

Restituisci l'oggetto strutturato con: tutte_le_skill, autore, primo_livello, secondo_livello, terzo_livello, quarto_livello, quinto_livello, collaudo.
Regole: usa SOLO cartelle realmente presenti; non inventare chiavi; se una chiave del manifesto non ha una cartella corrispondente, NON includerla; riporta i livelli e il collaudo esattamente come stanno nel manifesto (filtrati sulle cartelle esistenti).`

// ---- schema del feedback strutturato di ogni revisore (livelli 1-4) ----
const FEEDBACK_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['revisore', 'rilievi'],
  properties: {
    revisore: { type: 'string' },
    giudizio_sintetico: { type: 'string', description: 'Una frase: la Bibbia regge o no dal suo punto di vista' },
    rilievi: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['severita', 'sezione', 'problema', 'correzione'],
        properties: {
          severita: { type: 'string', enum: ['ERRORE', 'RISCHIO', 'PREFERENZA'] },
          sezione: { type: 'string', description: 'Capitolo del documento a cui si riferisce' },
          problema: { type: 'string' },
          correzione: { type: 'string', description: 'Cosa fare concretamente' },
        },
      },
    },
  },
}

// ---- schema del rapporto di riscrittura (5o livello) ----
const RISCRITTURA_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['parole_prima', 'parole_dopo'],
  properties: {
    parole_prima: { type: 'number' },
    parole_dopo: { type: 'number' },
    variazione_percentuale: { type: 'string' },
    periodi_spezzati: { type: 'number', description: 'Quanti periodi sopra le 30 parole hai spezzato' },
    termini_definiti: { type: 'number', description: 'Quanti termini tecnici hai dovuto definire' },
    passaggi_incomprensibili: {
      type: 'array',
      items: { type: 'string' },
      description: 'Passaggi che non si riuscivano a semplificare perche il concetto sotto era confuso. E il segnale piu prezioso: vanno riportati a Carlos.',
    },
    informazioni_perse: { type: 'array', items: { type: 'string' }, description: 'Vuoto se la riscrittura e fedele. Qualunque voce qui e un errore da correggere.' },
  },
}

// ---- schema del COLLAUDO DI CONSERVAZIONE (cancello finale) ----
// Non giudica la qualita: quella e chiusa a monte. Verifica che la riscrittura
// integrale del 5o livello non abbia perso, alterato o gonfiato niente.
const COLLAUDO_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['esito', 'violazioni_bloccanti'],
  properties: {
    esito: { type: 'string', enum: ['CONSEGNABILE', 'DA_RIPARARE', 'DA_RIFARE'], description: 'CONSEGNABILE solo con ZERO bloccanti, del codice e del collaudatore' },
    bloccanti_dal_codice: { type: 'number', description: 'Quanti bloccanti ha trovato verifica_conservazione.py' },
    violazioni_bloccanti: {
      type: 'array',
      description: 'Ogni voce e una riparazione da fare. Vuoto = riscrittura fedele.',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['tipo', 'capitolo', 'riparazione'],
        properties: {
          tipo: { type: 'string', description: 'INFORMAZIONE_PERSA / QUALIFICAZIONE_CADUTA / ETICHETTA_RIANCORATA / ETICHETTA_ALZATA / VERBO_IRRIGIDITO / NUMERO_RIATTRIBUITO / PROMESSA_INTRODOTTA / MATERIALE_OPERATIVO / STRUTTURA_ALTERATA' },
          capitolo: { type: 'string', description: 'Nome del capitolo, mai il numero' },
          testo_v5: { type: 'string', description: 'Il passaggio come stava nella v5' },
          testo_v6: { type: 'string', description: 'Come sta nella v6, o "assente"' },
          riparazione: { type: 'string', description: 'Istruzione chirurgica: cosa rimettere e dove. Non una riscrittura.' },
        },
      },
    },
    avvisi: { type: 'array', items: { type: 'string' }, description: 'Sospetti non bloccanti: possono essere riformulazione legittima' },
    conservato: { type: 'string', description: 'Cosa la riscrittura ha portato intatto pur cambiando tutte le parole' },
  },
}

// ============================ PROMPT ============================

const draftPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas (OsteoTouch). Devi redigere la BIBBIA TEORICA della condizione con slug "${slug}".

## Che documento stai scrivendo — leggi prima di tutto
Una **Bibbia** e' ~20 pagine con TUTTO quello che un osteopata deve SAPERE su quella condizione per poterla risolvere in poche sedute. NON e' una procedura operativa: **niente tecniche, niente dosi, niente sequenze, niente minuti, niente piani di seduta, niente scheda operativa**. Quelli stanno in un documento separato di 2 pagine, scritto da un altro agente. Il tuo Capitolo 11 arriva fino al RAZIONALE della leva e si ferma li'.

## Istruzioni della skill (leggile e seguile INTEGRALMENTE, in quest'ordine)
1. Leggi ${AUTORE}/SKILL.md
2. Poi, in quest'ordine, i reference in ${AUTORE}/references/:
   - architettura-bibbia.md (la struttura fissa dei 13 capitoli e le cinque regole di struttura)
   - regole-di-scrittura.md (COME si scrive: la leggibilita' e' un requisito, non una preferenza)
   - cinque-modelli-osteopatici.md (impalcatura del Capitolo 7)
   - motore-clinico.md (il ragionamento del Capitolo 8)
   - ancore-verificate.md e ancore-scientifiche.md (ancora scientifica e protocollo di verifica)
   - mappa-concettuale.md (il secondo deliverable)
   - sistema-libreria.md (coerenza col corpus)

## Precedenza scientifica — leggi PRIMA di scrivere
Apri ${DEVIAZIONI}. Registra i punti in cui il metodo interno e' stato trovato fattualmente sbagliato, con la formulazione corretta da usare al suo posto. **L'accuratezza scientifica viene prima della fedelta' al metodo**. Se ne trovi uno NUOVO: correggi e apri una voce con stato PROPOSTA e la fonte; NON modificare i documenti di metodo (la ratifica e' umana).

## Dati del problema
Apri ${DATA}, trova l'oggetto con "slug": "${slug}" e usa TUTTI i suoi campi (sintomi, soluzioni_provate, farmaci, esami_strumentali, benefici_trattamento, ads_pain_points, red_flag, meccanismo_causa, meccanismo_trattamento, obiezioni_specifiche) come materia prima. Sono la voce del paziente e del mercato: il Capitolo 1 ("Chi ti trova davanti") nasce da li', e il Capitolo 12 risponde a quelle obiezioni.

## Ricerca scientifica — OBBLIGATORIA
Prima di scrivere qualunque affermazione di evidenza DEVI cercare sul web e verificare ogni studio: titolo/autore/anno/PMID reali. Se non verifichi uno studio, non citarlo. Scegli l'ancora scientifica (un ricercatore reale, vivente, il piu autorevole al mondo in terapia manuale su questa condizione).

## L'etichetta di solidita' — il dispositivo centrale
La prosa AFFERMA; l'onesta' la porta un box separato \`> **Quanto e solido:**\` con una di quattro etichette: DIMOSTRATO / PROBABILE / IPOTESI / RAGIONAMENTO. Ogni meccanismo, ogni modello e ogni leva ne porta una. Vietato qualificare dentro la frase ("potrebbe eventualmente", "pur con le dovute cautele").

## Output
Scrivi in markdown, **8.000-12.000 parole** (appendici escluse):
- ${OUT}/${slug}/v1-bibbia.md → la Bibbia completa (13 capitoli + Appendice A Glossario + Appendice B Fonti)
- ${OUT}/${slug}/v1-mappa.md  → la Mappa concettuale (una pagina, sei blocchi)
Crea la cartella se non esiste. Non convertire in .docx: consegna markdown.

Alla fine restituisci SOLO: numero parole della Bibbia + ancora scientifica scelta + una riga di note. I file sono gia' il deliverable.`

const reviewPrompt = (slug, r) => `Sei il revisore **${r.key}** del panel avversariale Mobilitas (PRIMO livello). Devi revisionare una BIBBIA TEORICA osteopatica.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md (e i suoi reference se ne cita). Adotta esattamente quella prospettiva, con lo stesso obbligo di ricerca e la stessa severita.

## Perimetro — non chiedere protocolli
Quella che rivedi e' una Bibbia teorica (~20 pagine: cos'e', perche' succede, quali meccanismi, quanto e' solido, perche' le mani possono agire). **Non contiene, e non deve contenere, tecniche, dosi, sequenze o piani di seduta**: quelli stanno in una Procedura separata di 2 pagine. Un rilievo che chieda un protocollo e' fuori perimetro: scartalo da solo. Se invece TROVI un protocollo dentro la Bibbia, quello si segnala come materiale fuori posto.
Nota sulle etichette: ogni affermazione importante porta un box \`> **Quanto e solido:**\` (DIMOSTRATO / PROBABILE / IPOTESI / RAGIONAMENTO). Un'affermazione diretta con etichetta corretta NON e' un claim gonfiato: e' la forma prevista. Il claim gonfiato e' l'etichetta troppo alta, o assente.

## Documento da revisionare
Leggi ${OUT}/${slug}/v1-bibbia.md (la Bibbia) e ${OUT}/${slug}/v1-mappa.md (la Mappa). Se non esistono, restituisci un rilievo ERRORE che dice che il draft manca.

## Output
Classifica OGNI rilievo per severita: ERRORE (fatto sbagliato/pericoloso, va corretto), RISCHIO (esposizione da valutare), PREFERENZA (gusto, ignorabile). Sii chirurgico: capitolo preciso, problema, correzione concreta. Non riscrivere la Bibbia, non elogiare: solo rilievi azionabili.

Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa leggibile in ${OUT}/${slug}/feedback-${r.key}.md`

// SINTESI INTERMEDIA (v2): pesa i feedback di TUTTI i revisori di 1o livello e riscrive.
const synthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la versione INTERMEDIA (v2) della Bibbia "${slug}" sintetizzando i feedback dei revisori di 1o livello. NON e' ancora la finale: dopo di te la v2 va al 2o livello.

## Metodo di sintesi (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Regola che protegge il documento: **il feedback si pesa, non si somma**. ERRORE si corregge; RISCHIO si valuta; PREFERENZA si ignora di default. Elimina i doppioni e i conflitti tra lenti. Se la Bibbia cresce oltre il 20%, hai sommato invece di pesare: ferma e ripesa.
**Scarta d'ufficio ogni rilievo che chieda tecniche, dosi, sequenze o piani di seduta:** sono fuori dal perimetro della Bibbia.

## Input
- Draft: ${OUT}/${slug}/v1-bibbia.md e ${OUT}/${slug}/v1-mappa.md
- Feedback: leggi TUTTI i file ${OUT}/${slug}/feedback-*.md (uno per revisore, esclusi quelli che finiscono in -r2.md, -r3.md o -r4.md)

## Output
Riscrivi applicando il triage:
- ${OUT}/${slug}/v2-intermedia.md → Bibbia intermedia
- ${OUT}/${slug}/mappa-v2.md      → Mappa intermedia

Restituisci SOLO: cosa hai corretto (ERRORI), cosa hai valutato (RISCHI), cosa hai ignorato (PREFERENZE), quanti rilievi hai scartato come fuori perimetro, variazione % di lunghezza.`

// SECONDA REVISIONE: fedelta all'architettura della Bibbia, sulla v2.
const secondReviewPrompt = (slug, r) => `Sei il revisore di SECONDO LIVELLO **${r.key}** del panel Mobilitas. Questa e' la SECONDA passata: la Bibbia e' gia' stata revisionata da tutti i revisori di 1o livello e riscritta una volta.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md (e i suoi reference se ne cita). Adotta esattamente quella prospettiva, con la stessa severita.
Lo standard contro cui auditi e' ${AUTORE}/references/architettura-bibbia.md (i 13 capitoli, le cinque regole di struttura, le quattro etichette), piu' ${AUTORE}/references/cinque-modelli-osteopatici.md e ${AUTORE}/references/motore-clinico.md.

## Precedenza scientifica — vincolo che sovrascrive la fedelta' al metodo
Apri ${DEVIAZIONI} PRIMA di formulare rilievi. Stato RATIFICATA = la deviazione e' lo standard. Stato PROPOSTA = marcala "DEVIAZIONE MOTIVATA" e passa oltre. Stato RESPINTA = vince il metodo.
Regola generale: **quando il metodo prescrive un contenuto contraddetto dalla fisiologia o dall'evidenza, vince l'accuratezza scientifica**. Se trovi una deviazione fondata ma NON registrata, marcala "DEVIAZIONE MOTIVATA — non registrata" e segnala che va aperta una voce nel registro.

## Documento da revisionare
Leggi ${OUT}/${slug}/v2-intermedia.md e ${OUT}/${slug}/mappa-v2.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v2 manca.

## Output
Classifica OGNI rilievo per severita: ERRORE / RISCHIO / PREFERENZA. Sii chirurgico: capitolo preciso, problema, correzione concreta. Non riscrivere la Bibbia.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${OUT}/${slug}/feedback-${r.key}-r2.md`

// SINTESI v3
const thirdSynthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la v3 della Bibbia "${slug}", applicando i feedback della revisione di 2o livello alla v2. NON e' ancora la finale: dopo di te la v3 va al revisore della logica dell'apprendimento (3o livello), poi all'editor (4o) e infine al riscrittore di chiarezza (5o).

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Vale la stessa regola: **il feedback si pesa, non si somma**. Parti dalla v2, non dalla bozza.

## Input
- Bibbia intermedia: ${OUT}/${slug}/v2-intermedia.md e ${OUT}/${slug}/mappa-v2.md
- Feedback della 2a passata: leggi TUTTI i file ${OUT}/${slug}/feedback-*-r2.md

## Output
- ${OUT}/${slug}/v3-intermedia.md → Bibbia v3
- ${OUT}/${slug}/mappa-v3.md      → Mappa v3

Restituisci SOLO: cosa hai corretto dalla 2a revisione, cosa hai valutato/ignorato, variazione % di lunghezza rispetto alla v2.`

// TERZA REVISIONE: la logica dell'apprendimento, sulla v3.
const thirdReviewPrompt = (slug, r) => `Sei il revisore di TERZO LIVELLO **${r.key}** del panel Mobilitas — la logica dell'apprendimento. La Bibbia e' gia' stata validata dai revisori di 1o e 2o livello: contenuto, sicurezza, compliance e fedelta' all'architettura sono chiusi. Tu guardi il documento non come testo ma come PERCORSO DI APPRENDIMENTO, e rispondi a una domanda sola: chi legge impara davvero a ragionare su questa condizione, o impara solo a sapere delle cose?

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md e il suo reference ${r.skill}/references/sei-fasi-apprendimento.md, **con l'adattamento alla Bibbia descritto nella SKILL**: in un documento teorico il "come" e' **come si riconosce**, la "pratica" e' **il ragionamento seguito su un caso**, il "feedback" e' **come si scopre di aver sbagliato ipotesi**. Non chiedere tecniche, dosi o esercizi: sono fuori perimetro.

## Tre confini rigidi
1. **Non aggiungi contenuto clinico**: niente meccanismi, studi, bandiere rosse o cautele nuove. Se una fase manca, la costruisci con il materiale gia' presente, spostandolo o esplicitandone il senso.
2. **Non asciughi**: dopo di te c'e' l'editor (4o livello). Una ripetizione con funzione didattica e' un pregio: segnalala tra le cose DA PROTEGGERE.
3. **Non gonfi**: preferisci lo spostamento all'aggiunta. Ogni rilievo che aggiunge testo dichiara quante parole costa. Budget complessivo: crescita netta **<= 5%**.

Rispetta l'INTOCCABILE (bandiere rosse, limiti di campo, etichette di solidita', PMID/dati, hedge di compliance, le tre voci, l'architettura dei 13 capitoli, le aperture "In una riga" e le chiusure "Le tre cose da ricordare"). Se il documento gia' insegna, il verdetto legittimo e' "Insegna".

## Documento da revisionare
Leggi ${OUT}/${slug}/v3-intermedia.md e ${OUT}/${slug}/mappa-v3.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v3 manca.

## Output
Mappa il tuo output sullo schema per severita: **ERRORE** = una fase e' assente o invertita in modo che rompe l'apprendimento. **RISCHIO** = la fase c'e' ma e' debole, implicita o lontana dal punto d'uso. **PREFERENZA** = gusto didattico (max 3). Per ogni rilievo: fase mancante, capitolo OSPITE gia' esistente dove rimetterla, cosa fare concretamente, costo in parole.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${OUT}/${slug}/feedback-${r.key}-r3.md, includendo la mappa delle sei fasi (presente/debole/assente), la sezione **Da proteggere dall'editor** e il bilancio parole.`

// SINTESI v4
const fourthSynthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la v4 della Bibbia "${slug}", applicando i rilievi del revisore della logica dell'apprendimento (3o livello) alla v3. NON e' ancora la finale: dopo di te la v4 va all'editor di asciugatura (4o livello) e poi al riscrittore di chiarezza (5o).

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Vale la stessa regola: **il feedback si pesa, non si somma**. Parti dalla v3.

Regola specifica di questo livello: **prima si sposta, poi si riscrive, solo in ultimo si aggiunge**. NON introdurre contenuto clinico nuovo: il contenuto e' chiuso dai livelli 1 e 2. Crescita netta ammessa rispetto alla v3: **massimo 5%**.

## Input
- Bibbia v3: ${OUT}/${slug}/v3-intermedia.md e ${OUT}/${slug}/mappa-v3.md
- Rilievi di apprendimento: leggi TUTTI i file ${OUT}/${slug}/feedback-*-r3.md

## Output
- ${OUT}/${slug}/v4-intermedia.md → Bibbia v4
- ${OUT}/${slug}/mappa-v4.md      → Mappa v4

Restituisci SOLO: quali fasi hai colmato e come (spostamento / riscrittura / aggiunta), cosa hai ignorato, la variazione % rispetto alla v3, e l'elenco dei passaggi marcati **da proteggere dall'editor** (riportalo, serve al livello successivo).`

// QUARTA REVISIONE: l'editor di asciugatura, sulla v4. Produce una MAPPA DI TAGLIO.
const fourthReviewPrompt = (slug, r) => `Sei il revisore di QUARTO LIVELLO **${r.key}** del panel Mobilitas — l'editor di asciugatura. La Bibbia e' gia' validata sul contenuto, sulla fedelta' all'architettura e sull'impianto didattico. Tu NON aggiungi ne' contesti la sostanza: produci una MAPPA DI TAGLIO per togliere ridondanza e riportare il documento nel range **8.000-12.000 parole**, senza perdere informazione e senza spegnere la voce.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md. Rispetta l'INTOCCABILE (bandiere rosse, limiti di campo, **etichette di solidita'**, PMID/dati, hedge di compliance, le tre voci, le aperture "In una riga" e le chiusure "Le tre cose da ricordare", Glossario e Fonti). Se il documento e' gia' nel range e non trovi ridondanza vera, il verdetto legittimo e' "Gia' asciutta".

## Cosa arriva dopo di te
Dopo di te gira il 5o livello (**chiarezza**), che riscrive tutto in linguaggio semplice e puo' allungare il testo fino al 10%. Due conseguenze: (a) **non e' compito tuo semplificare** — una frase corretta ma contorta la riscrive lui, tu tagli solo cio' che e' detto due volte; (b) **tieni un margine**: se il documento e' al limite alto del range, punta al centro, non al tetto.

## Vincolo aggiuntivo: il lavoro del 3o livello
Leggi anche i file ${OUT}/${slug}/feedback-*-r3.md, in particolare la sezione **Da proteggere dall'editor**. Quei passaggi hanno funzione didattica: una ripetizione che ancora il senso al punto d'uso NON e' ridondanza. Se ritieni comunque che uno vada tagliato, classificalo al massimo come PREFERENZA.

## Documento da revisionare
Leggi ${OUT}/${slug}/v4-intermedia.md e ${OUT}/${slug}/mappa-v4.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v4 manca.

## Output
Mappa il tuo output sullo schema per severita: **RIDONDANTE -> ERRORE** (taglio sicuro, l'info esiste identica altrove), **COMPRIMIBILE -> RISCHIO** (stessa sostanza in meno parole), **PREFERENZA -> PREFERENZA**. Per ogni rilievo indica capitolo/passaggio, cosa tagliare o come comprimere, e dove resta l'informazione. Segnala a parte eventuale materiale FUORI PERIMETRO (tecniche, dosi, sequenze in un documento teorico). Non riscrivere la Bibbia.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${OUT}/${slug}/feedback-${r.key}-r4.md`

// SINTESI v5: applica la mappa di taglio dell'editor alla v4.
const fifthSynthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la v5 della Bibbia "${slug}", applicando la mappa di taglio dell'editor (4o livello) alla v4. NON e' la versione consegnata: dopo di te la v5 va al riscrittore di chiarezza (5o livello), che la riscrive integralmente.

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Regola: **si asciuga solo se strettamente necessario**. Applica i tagli RIDONDANTE; valuta i COMPRIMIBILE solo se servono a rientrare nel range 8.000-12.000 parole; ignora le PREFERENZE di default. NON toccare l'INTOCCABILE (bandiere rosse, limiti di campo, etichette di solidita', PMID, hedge, le tre voci, Glossario e Fonti) ne' i passaggi marcati **da proteggere** nei feedback di 3o livello (${OUT}/${slug}/feedback-*-r3.md). Se la v4 e' gia' asciutta, copiala nella v5 senza modifiche.

## Input
- Bibbia v4: ${OUT}/${slug}/v4-intermedia.md e ${OUT}/${slug}/mappa-v4.md
- Mappa di taglio: leggi TUTTI i file ${OUT}/${slug}/feedback-*-r4.md
- Da proteggere: la sezione omonima nei file ${OUT}/${slug}/feedback-*-r3.md

## Output
- ${OUT}/${slug}/v5-intermedia.md → Bibbia v5
- ${OUT}/${slug}/mappa-v5.md      → Mappa v5

Restituisci SOLO: cosa hai tagliato (RIDONDANTE), cosa hai compresso o lasciato, cosa hai protetto su indicazione del 3o livello, e la lunghezza finale in parole.`

// QUINTO LIVELLO: NON e' una revisione. E' una RISCRITTURA INTEGRALE che produce il deliverable.
const rewritePrompt = (slug, r) => `Sei il revisore di QUINTO e ULTIMO livello del panel Mobilitas — **il Traduttore**. Non emetti rilievi: **riscrivi da capo l'intero documento**. Quello che produci e' la versione che si consegna.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md e il suo reference ${r.skill}/references/regole-di-chiarezza.md (i prima/dopo: leggili, sono il metodo).

Prima di te sono girati quattordici revisori: contenuto, sicurezza, compliance, fedelta' al metodo, impianto didattico e lunghezza sono chiusi. **Non tocchi niente di tutto questo.** Il tuo problema e' un altro: il documento e' giusto ma si legge male.

> Riscrivi l'intera Bibbia in modo che un osteopata neolaureato la legga dall'inizio alla fine **senza rileggere una sola frase**, e **senza che si perda una sola informazione**.

## Il metodo: si riscrive, non si corregge
1. Leggi tutto il documento senza scrivere niente.
2. Costruisci l'**inventario delle informazioni**: capitolo per capitolo, ogni fatto, numero, meccanismo, etichetta, bandiera rossa, citazione, definizione. E' il tuo contratto.
3. Riscrivi capitolo per capitolo **guardando l'inventario, non il vecchio testo**. Se hai il vecchio testo davanti mentre scrivi, ne copierai la sintassi.
4. Ricontrolla l'inventario alla fine: ogni voce non ricomparsa e' un'informazione persa, rimettila.

## Le regole
Frasi da 18-20 parole in media, 30 al massimo. Una subordinata per frase, mai una dentro l'altra. Prima la conclusione, poi la spiegazione. Voce attiva. Ogni termine tecnico spiegato dove compare e messo a Glossario. L'incertezza sta nell'etichetta \`> **Quanto e solido:**\`, mai nei giri di parole. Le catene causali diventano passaggi numerati. Lessico corto ("per" non "al fine di", "e'" non "risulta essere").

## L'INVIOLABILE
Riscrivi **come e' detto**, mai **cosa e' detto**. Restano identici: ogni numero, percentuale e misura; ogni PMID, autore, anno e titolo; **ogni etichetta di solidita' — non alzarne nessuna, mai**; ogni bandiera rossa, criterio di invio e limite di campo; ogni nome anatomico; l'architettura (capitoli, ordine, titoli, aperture "In una riga", chiusure "Le tre cose da ricordare", i quattro tipi di box); le tre voci e le frasi-firma dello studio.

## Lunghezza
Da **-5% a +10%** rispetto al testo che ricevi. Sotto -5% hai tagliato informazione. Sopra +10% hai aggiunto contenuto.

## Documento da riscrivere
Leggi ${OUT}/${slug}/v5-intermedia.md (la Bibbia) e ${OUT}/${slug}/mappa-v5.md (la Mappa). Se non esistono, fermati e dillo.

## Output — sono i deliverable
- ${OUT}/${slug}/v6-finale.md    → la Bibbia FINALE, riscritta integralmente
- ${OUT}/${slug}/mappa-finale.md → la Mappa FINALE, riscritta con lo stesso criterio

Scrivi **tutti** i capitoli e **tutte** le appendici. Non lasciare rimandi al vecchio testo: il file nuovo deve essere completo e autosufficiente.

Restituisci l'oggetto strutturato richiesto. In "passaggi_incomprensibili" metti i punti che non sei riuscito a semplificare perche' il concetto sotto era confuso: e' il segnale piu' prezioso di tutta la catena.`

const SCRIPT_COLLAUDO = AUTORE + '/scripts/verifica_conservazione.py'

const collaudoPrompt = (slug, g) => `Sei il **COLLAUDO DI CONSERVAZIONE** della Bibbia "${slug}" — l'ultimo cancello prima della consegna.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${g.skill}/SKILL.md.

Prima di te sono girati quattordici revisori su cinque livelli, e poi il quinto livello ha **riscritto da capo ogni singola frase** del documento. Quella riscrittura e' l'unico passaggio della catena in cui tutto il testo cambia. Tu verifichi che, cambiando tutte le parole, non sia cambiata nessuna cosa detta.

> **La v6 dice esattamente le stesse cose della v5, o per strada si e' perso, indebolito o gonfiato qualcosa?**

## LA REGOLA CHE TI DEFINISCE
**Non giudichi la qualita'.** Quella ha gia' avuto quattordici risposte. Giudichi solo la CONSERVAZIONE.
Se un contenuto ti sembra debole ma stava identico nella v5, **non e' un tuo rilievo: taci**. Un collaudatore che trova cose nuove riapre decisioni chiuse e fa ripartire un ciclo finito: e' rotto, non severo.
Uniche eccezioni, perche' nate qui: promesse di esito, materiale operativo (dosi, sequenze, minuti) e affermazioni rafforzate.

## PASSO 1 — fai girare il codice, prima di leggere
Esegui con Bash:
\`python3 ${SCRIPT_COLLAUDO} ${OUT}/${slug}/v5-intermedia.md ${OUT}/${slug}/v6-finale.md --json ${OUT}/${slug}/collaudo.json\`

Copre gia': etichette perse o alzate, PMID spariti o inventati, numeri persi o comparsi, titoli e struttura, aperture "In una riga" e chiusure "Le tre cose da ricordare", tabelle fuori specifica, delta di lunghezza, glossario, script, materiale operativo e promesse.
**Quello che lo script trova e' accertato: riportalo in "violazioni_bloccanti", non riverificarlo.** Metti il suo numero di bloccanti in "bloccanti_dal_codice".

## PASSO 2 — il tuo lavoro comincia dove il codice si ferma
Leggi ${OUT}/${slug}/v5-intermedia.md e ${OUT}/${slug}/v6-finale.md e cerca cio' che nessun conteggio vede:
1. **Etichetta riancorata** — la stessa etichetta ora qualifica un claim diverso. I conteggi tornano, il senso no.
2. **Informazione persa per assorbimento** — due frasi che dicevano due cose diventano una che ne dice una e sembra completa. Procedi per inventario, capitolo per capitolo.
3. **Qualificazione caduta** — "nella maggior parte dei casi", "se il paziente non ha X", l'urgenza o il destinatario di una bandiera rossa, il sottotipo su cui si poteva poco.
4. **Verbo irrigidito** — "puo' contribuire" -> "contribuisce". Frasi corte sono assertive per costruzione: e' l'effetto collaterale strutturale della semplificazione.
5. **Numero riattribuito** — il valore c'e' ancora ma appartiene a un altro studio.

Controlla anche ${OUT}/${slug}/mappa-v5.md contro ${OUT}/${slug}/mappa-finale.md con lo stesso criterio.

## Output
Ogni violazione porta una **riparazione chirurgica**: cosa rimettere e dove, non una riscrittura. Chi ripara e' il riscrittore, e deve poter agire senza toccare il resto.
Localizza i capitoli **per nome**, mai per numero.
"CONSEGNABILE" solo con ZERO bloccanti, del codice e tuoi. Non esiste il consegnabile con riserva.
Se non trovi niente, dillo: e' l'esito atteso di una riscrittura fatta bene.`

const riparaPrompt = (slug, r, viol, giro) => `Sei il **Traduttore** (5o livello) della Bibbia "${slug}". La tua riscrittura e' stata collaudata e ha ${viol.length} violazioni di conservazione. Questo e' il giro di riparazione ${giro}.

## Cosa NON devi fare
**Non riscrivere il documento. Non rileggerlo per migliorarlo. Non toccare una sola frase che non sia nell'elenco qui sotto.**
La v6 e' gia' buona: e' semplice, si legge, ed e' il risultato del tuo lavoro. Ha solo perso per strada delle cose che dovevano restare. Le rimetti, e basta.
Ogni modifica fuori dall'elenco riapre il collaudo e allunga il ciclo.

## Le violazioni da riparare
${viol.map((v, i) => `${i + 1}. [${v.tipo}] Capitolo «${v.capitolo}»
   v5 diceva: ${v.testo_v5 || '(vedi rapporto)'}
   v6 dice:   ${v.testo_v6 || 'assente'}
   RIPARAZIONE: ${v.riparazione}`).join('\n')}

## Come si ripara
Riapri ${OUT}/${slug}/v6-finale.md (e ${OUT}/${slug}/mappa-finale.md se la violazione e' li') e applica **solo** queste riparazioni.
Rimetti l'informazione **con il lessico e la sintassi della v6**, non copiando la frase della v5: il documento deve restare semplice. Frasi da 18-20 parole, una subordinata per frase, prima la conclusione.
Se una riparazione riguarda un'etichetta, rimetti **esattamente** l'etichetta che aveva la v5: non alzarla mai.
Se una riparazione riguarda una promessa o del materiale operativo introdotto, **toglilo**, non attenuarlo.

Salva sugli stessi file. Restituisci l'oggetto strutturato: in "informazioni_perse" lascia vuoto se hai riparato tutto, altrimenti elenca cosa non sei riuscito a rimettere e perche'.`

// promuovi un documento a versione successiva senza modifiche (quando un livello e' vuoto)
const promotePrompt = (bibIn, mappaIn, bibOut, mappaOut) =>
  `Copia senza modifiche ${bibIn} in ${bibOut} e ${mappaIn} in ${mappaOut}. Poi conferma in una riga.`

// ============================ RESILIENZA ============================
// Un singolo agente che fallisce NON deve abortire l'intera catena.
//  1) robustAgent: ritenta l'agente critico fino a RETRIES volte.
//  2) promote: se una SINTESI non riesce anche dopo i retry, si promuove (copia) l'ultima
//     versione buona alla successiva, cosi la catena PROSEGUE con il miglior documento disponibile.
const RETRIES = 3
// Quanti giri di riparazione mirata si concedono a una riscrittura che ha perso qualcosa.
// Oltre, il problema non e' un dettaglio sfuggito: si consegna la v5 o si ferma tutto.
const MAX_RIPARAZIONI = 2

async function robustAgent(prompt, opts, tries = RETRIES) {
  for (let i = 0; i < tries; i++) {
    const label = i === 0 ? opts.label : `${opts.label}#retry${i}`
    const r = await agent(prompt, { ...opts, label })
    if (r) return r
    log(`  [resilienza] "${opts.label}" non ha risposto (tentativo ${i + 1}/${tries})${i + 1 < tries ? ' — ritento' : ' — rinuncio'}`)
  }
  return null
}

async function promote(bibIn, mappaIn, bibOut, mappaOut, motivo) {
  log(`  [resilienza] ${motivo}: promuovo ${bibIn.split('/').pop()} -> ${bibOut.split('/').pop()} senza modifiche`)
  const r = await robustAgent(
    promotePrompt(bibIn, mappaIn, bibOut, mappaOut),
    { label: `promuovi:${bibOut.split('/').pop()}`, phase: 'Sintesi', agentType: 'general-purpose' },
    2
  )
  if (!r) log(`  [resilienza] ATTENZIONE: anche la promozione verso ${bibOut.split('/').pop()} non ha confermato — controlla i file a mano`)
  return r
}

// ============================ ORCHESTRAZIONE ============================

// ---- DUE MODALITA D'USO ----
// A) Bibbie SPECIFICHE: args = ["reflusso"] oppure ["reflusso","cervicalgia", ...]
// B) TUTTE: args = "tutte" (o "all" / "*") -> carica gli slug dal JSON
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
log(`Genero ${slugs.length} Bibbie: ${slugs.join(', ')}`)

// --- FASE 0: SCOPERTA DINAMICA (cartella reale) + RUOLI (manifesto) ---
phase('Scoperta')
const disc = await robustAgent(discoveryPrompt(), { label: 'scopri-ruoli', phase: 'Scoperta', schema: DISCOVERY_SCHEMA, agentType: 'general-purpose' })
if (!disc) {
  log('ATTENZIONE: scoperta ruoli non riuscita dopo i retry. Interrompo: senza il manifesto non so chi rivede.')
  return { errore: 'scoperta ruoli fallita (manifesto ' + MANIFESTO + ' non leggibile dopo ' + RETRIES + ' tentativi)' }
}
const all = ((disc && disc.tutte_le_skill) || []).filter(Boolean)
const autore = (disc && disc.autore) || 'teoria'
// LIVELLI ESPLICITI dal manifesto, filtrati sulle cartelle presenti e senza sovrapposizioni.
const firstKeys = ((disc && disc.primo_livello) || []).filter((k) => all.includes(k) && k !== autore)
const secondKeys = ((disc && disc.secondo_livello) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k))
const thirdKeys = ((disc && disc.terzo_livello) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k))
const fourthKeys = ((disc && disc.quarto_livello) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k) && !thirdKeys.includes(k))
const fifthKeys = ((disc && disc.quinto_livello) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k) && !thirdKeys.includes(k) && !fourthKeys.includes(k))
const gateKeys = ((disc && disc.collaudo) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k) && !thirdKeys.includes(k) && !fourthKeys.includes(k) && !fifthKeys.includes(k))

const mk = (k) => ({ key: k, skill: SK + '/direttore-osteopatico-' + k })
const REVIEWERS = firstKeys.map(mk)  // 1o livello
const SECOND = secondKeys.map(mk)    // 2o livello
const THIRD = thirdKeys.map(mk)      // 3o livello (logica dell'apprendimento)
const FOURTH = fourthKeys.map(mk)    // 4o livello (editor di asciugatura)
const FIFTH = fifthKeys.map(mk)      // 5o livello (riscrittura in chiaro)
const GATE = gateKeys.map(mk)        // CANCELLO: collaudo di conservazione v5 -> v6

// Segnala skill-revisore presenti ma non assegnate a nessun livello: niente cali silenziosi.
const assegnate = new Set([autore, ...firstKeys, ...secondKeys, ...thirdKeys, ...fourthKeys, ...fifthKeys, ...gateKeys])
const nonAssegnate = all.filter((k) => !assegnate.has(k))
if (nonAssegnate.length) log(`ATTENZIONE: skill presenti ma non assegnate a nessun livello nel manifesto (ignorate): ${nonAssegnate.join(', ')}`)

if (!REVIEWERS.length && !SECOND.length && !THIRD.length && !FOURTH.length && !FIFTH.length) {
  log('ATTENZIONE: nessun revisore dichiarato nel manifesto. Interrompo.')
  return { errore: 'nessun revisore nei livelli del manifesto ' + MANIFESTO }
}
log(`Autore: ${autore} | 1o (${REVIEWERS.length}): ${REVIEWERS.map((r) => r.key).join(', ') || '—'} | 2o (${SECOND.length}): ${SECOND.map((r) => r.key).join(', ') || '—'} | 3o (${THIRD.length}): ${THIRD.map((r) => r.key).join(', ') || '—'} | 4o (${FOURTH.length}): ${FOURTH.map((r) => r.key).join(', ') || '—'} | 5o (${FIFTH.length}): ${FIFTH.map((r) => r.key).join(', ') || '—'} | collaudo: ${GATE.map((r) => r.key).join(', ') || '— NESSUNO (la v6 andrebbe in consegna senza cancello)'}`)
if (!GATE.length) log('ATTENZIONE: nessun collaudo dichiarato nel manifesto. La riscrittura integrale del 5o livello non verra verificata da nessuno.')

const results = await pipeline(
  slugs,

  // --- STAGE 1: DRAFT (v1) ---
  async (slug) => {
    const r = await robustAgent(draftPrompt(slug), { label: `draft:${slug}`, phase: 'Draft', agentType: 'general-purpose' })
    // Il draft e l'unico stadio senza fallback: senza bozza non c'e nulla da revisionare.
    // Il throw qui, dentro pipeline(), scarta SOLO questo slug (gli altri proseguono).
    if (!r) { log(`ATTENZIONE: draft non riuscito per ${slug} dopo ${RETRIES} tentativi — salto SOLO questo slug`); throw new Error(`draft fallito per ${slug}`) }
    log(`Draft pronto: ${slug}`)
    return slug
  },

  // --- STAGE 2: REVISIONE 1o LIVELLO (in parallelo) ---
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

  // --- STAGE 3: SINTESI INTERMEDIA (v2) ---
  async (slug) => {
    const r = await robustAgent(synthPrompt(slug), { label: `sintesi-v2:${slug}`, phase: 'Sintesi intermedia', agentType: 'general-purpose' })
    if (!r) await promote(`${OUT}/${slug}/v1-bibbia.md`, `${OUT}/${slug}/v1-mappa.md`, `${OUT}/${slug}/v2-intermedia.md`, `${OUT}/${slug}/mappa-v2.md`, `sintesi v2 non riuscita per ${slug}`)
    else log(`v2 pronta: ${slug}`)
    return slug
  },

  // --- STAGE 4: REVISIONE 2o LIVELLO -> SINTESI v3 ---
  async (slug) => {
    if (!SECOND.length) {
      await promote(`${OUT}/${slug}/v2-intermedia.md`, `${OUT}/${slug}/mappa-v2.md`, `${OUT}/${slug}/v3-intermedia.md`, `${OUT}/${slug}/mappa-v3.md`, `nessun 2o livello per ${slug}`)
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
    if (!r) await promote(`${OUT}/${slug}/v2-intermedia.md`, `${OUT}/${slug}/mappa-v2.md`, `${OUT}/${slug}/v3-intermedia.md`, `${OUT}/${slug}/mappa-v3.md`, `sintesi v3 non riuscita per ${slug}`)
    else log(`v3 pronta: ${slug}`)
    return slug
  },

  // --- STAGE 5: REVISIONE 3o LIVELLO (apprendimento) -> SINTESI v4 ---
  async (slug) => {
    if (!THIRD.length) {
      await promote(`${OUT}/${slug}/v3-intermedia.md`, `${OUT}/${slug}/mappa-v3.md`, `${OUT}/${slug}/v4-intermedia.md`, `${OUT}/${slug}/mappa-v4.md`, `nessun 3o livello per ${slug}`)
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
    if (!r) await promote(`${OUT}/${slug}/v3-intermedia.md`, `${OUT}/${slug}/mappa-v3.md`, `${OUT}/${slug}/v4-intermedia.md`, `${OUT}/${slug}/mappa-v4.md`, `sintesi v4 non riuscita per ${slug}`)
    else log(`v4 pronta: ${slug}`)
    return slug
  },

  // --- STAGE 6: REVISIONE 4o LIVELLO (editor) -> SINTESI v5 ---
  async (slug) => {
    if (!FOURTH.length) {
      await promote(`${OUT}/${slug}/v4-intermedia.md`, `${OUT}/${slug}/mappa-v4.md`, `${OUT}/${slug}/v5-intermedia.md`, `${OUT}/${slug}/mappa-v5.md`, `nessun 4o livello per ${slug}`)
      log(`v5 (= v4, nessun 4o livello): ${slug}`)
      return slug
    }
    const fbs = await parallel(
      FOURTH.map((rv) => () =>
        agent(fourthReviewPrompt(slug, rv), { label: `rev4:${rv.key}:${slug}`, phase: 'Revisione 4o livello', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
      )
    )
    log(`Revisione 4o livello ${slug}: ${fbs.filter(Boolean).length}/${FOURTH.length}`)
    const r = await robustAgent(fifthSynthPrompt(slug), { label: `sintesi-v5:${slug}`, phase: 'Sintesi v5', agentType: 'general-purpose' })
    if (!r) await promote(`${OUT}/${slug}/v4-intermedia.md`, `${OUT}/${slug}/mappa-v4.md`, `${OUT}/${slug}/v5-intermedia.md`, `${OUT}/${slug}/mappa-v5.md`, `sintesi v5 non riuscita per ${slug}`)
    else log(`v5 pronta: ${slug}`)
    return slug
  },

  // --- STAGE 7: QUINTO LIVELLO — RISCRITTURA INTEGRALE -> v6 FINALE ---
  // Non e' una revisione seguita da una sintesi: il riscrittore PRODUCE il deliverable.
  async (slug) => {
    if (!FIFTH.length) {
      await promote(`${OUT}/${slug}/v5-intermedia.md`, `${OUT}/${slug}/mappa-v5.md`, `${OUT}/${slug}/v6-finale.md`, `${OUT}/${slug}/mappa-finale.md`, `nessun 5o livello per ${slug}`)
      log(`FINALE (v6 = v5, nessuna riscrittura di chiarezza): ${slug}`)
      return { slug, esito: 'completata (senza riscrittura finale)' }
    }
    // Un solo riscrittore per volta: due riscritture concorrenti sullo stesso file si sovrascriverebbero.
    // Se il manifesto ne dichiara piu d'uno, usa il primo e segnala gli altri.
    if (FIFTH.length > 1) log(`ATTENZIONE: piu di un riscrittore di 5o livello nel manifesto. Uso "${FIFTH[0].key}", ignoro: ${FIFTH.slice(1).map((r) => r.key).join(', ')}`)
    const rw = FIFTH[0]
    const rep = await robustAgent(rewritePrompt(slug, rw), { label: `rev5:${rw.key}:${slug}`, phase: 'Riscrittura finale', schema: RISCRITTURA_SCHEMA, agentType: 'general-purpose' })
    if (!rep) {
      await promote(`${OUT}/${slug}/v5-intermedia.md`, `${OUT}/${slug}/mappa-v5.md`, `${OUT}/${slug}/v6-finale.md`, `${OUT}/${slug}/mappa-finale.md`, `riscrittura finale non riuscita per ${slug}`)
      return { slug, esito: 'completata (v6=v5, riscrittura promossa dopo i retry)' }
    }
    if (rep.informazioni_perse && rep.informazioni_perse.length) {
      log(`ATTENZIONE ${slug}: la riscrittura dichiara ${rep.informazioni_perse.length} informazioni perse — vanno rimesse a mano`)
    }
    if (rep.passaggi_incomprensibili && rep.passaggi_incomprensibili.length) {
      log(`Segnale per Carlos (${slug}): ${rep.passaggi_incomprensibili.length} passaggi non semplificabili — probabile confusione di contenuto, non di forma`)
    }
    log(`v6 riscritta: ${slug} — ${rep.parole_prima} → ${rep.parole_dopo} parole (${rep.variazione_percentuale || 'n/d'}). Ora il collaudo.`)
    return { slug, esito: 'completata', riscrittura: rep }
  },

  // --- STAGE 8: COLLAUDO DI CONSERVAZIONE -> RIPARAZIONE MIRATA -> CONSEGNA ---
  // Il 5o livello riscrive OGNI frase del documento: e' l'unico punto della catena in cui
  // tutto il testo cambia, ed era l'unico mai verificato. Qui si chiude quel buco.
  // Non e' un sesto revisore: non giudica la qualita' (chiusa a monte), verifica la
  // CONSERVAZIONE — che cambiando tutte le parole non sia cambiata nessuna cosa detta.
  async (prev, slug) => {
    const base = prev && prev.slug ? prev : { slug, esito: 'sconosciuto' }

    if (!GATE.length) {
      log(`ATTENZIONE ${slug}: nessun collaudo nel manifesto — la v6 va in consegna senza cancello.`)
      return { ...base, collaudo: 'assente' }
    }
    // Se non c'e' stata riscrittura (v6 promossa uguale alla v5) non c'e' niente da conservare.
    if (!base.riscrittura) {
      log(`Collaudo non necessario per ${slug}: la v6 e' la v5 promossa senza riscrittura.`)
      return { ...base, collaudo: 'non necessario' }
    }

    const g = GATE[0]
    if (GATE.length > 1) log(`ATTENZIONE: piu di un collaudo nel manifesto. Uso "${g.key}", ignoro: ${GATE.slice(1).map((r) => r.key).join(', ')}`)

    let rap = null
    for (let giro = 1; giro <= MAX_RIPARAZIONI + 1; giro++) {
      rap = await robustAgent(collaudoPrompt(slug, g), {
        label: `collaudo:${slug}${giro > 1 ? `#giro${giro}` : ''}`,
        phase: 'Collaudo', schema: COLLAUDO_SCHEMA, agentType: 'general-purpose',
      })

      if (!rap) {
        log(`ATTENZIONE ${slug}: il collaudo non ha risposto dopo i retry. La v6 resta, ma NON e' stata verificata.`)
        return { ...base, collaudo: 'non eseguito' }
      }

      const viol = (rap.violazioni_bloccanti || []).filter(Boolean)
      const dalCodice = rap.bloccanti_dal_codice || 0

      if (rap.esito === 'CONSEGNABILE' && !viol.length) {
        log(`COLLAUDO SUPERATO ${slug}${giro > 1 ? ` (dopo ${giro - 1} riparazion${giro === 2 ? 'e' : 'i'})` : ''}: la riscrittura ha conservato tutto.`)
        return { ...base, esito: 'consegnabile', collaudo: 'superato', riparazioni: giro - 1, conservato: rap.conservato }
      }

      // Perdite cosi' diffuse che una riparazione chirurgica non basta.
      // Vince la gerarchia dichiarata dal metodo: l'ACCURATEZZA batte la LEGGIBILITA'.
      // Meglio consegnare la v5 (corretta, meno scorrevole) che una v6 che ha perso informazione.
      if (rap.esito === 'DA_RIFARE') {
        log(`COLLAUDO: ${slug} DA RIFARE (${viol.length} perdite diffuse). Ripristino la v5 come versione finale: l'accuratezza batte la leggibilita.`)
        await promote(`${OUT}/${slug}/v5-intermedia.md`, `${OUT}/${slug}/mappa-v5.md`, `${OUT}/${slug}/v6-finale.md`, `${OUT}/${slug}/mappa-finale.md`, `riscrittura di ${slug} non conservativa`)
        return { ...base, esito: 'consegnata la v5', collaudo: 'fallito — riscrittura scartata', violazioni: viol.length }
      }

      if (giro > MAX_RIPARAZIONI) {
        log(`ATTENZIONE ${slug}: ${viol.length} violazioni ancora aperte dopo ${MAX_RIPARAZIONI} riparazioni. NON CONSEGNABILE senza intervento umano.`)
        return { ...base, esito: 'NON CONSEGNABILE', collaudo: 'non superato', violazioni: viol, bloccanti_dal_codice: dalCodice }
      }

      log(`Collaudo ${slug}: ${viol.length} violazioni (${dalCodice} dal codice). Riparazione mirata, giro ${giro}.`)
      const fix = await robustAgent(riparaPrompt(slug, FIFTH[0] || g, viol, giro), {
        label: `ripara:${slug}#giro${giro}`, phase: 'Collaudo', schema: RISCRITTURA_SCHEMA, agentType: 'general-purpose',
      })
      if (!fix) {
        log(`ATTENZIONE ${slug}: la riparazione non ha risposto. Consegno la v5, che e' l'ultima versione verificata.`)
        await promote(`${OUT}/${slug}/v5-intermedia.md`, `${OUT}/${slug}/mappa-v5.md`, `${OUT}/${slug}/v6-finale.md`, `${OUT}/${slug}/mappa-finale.md`, `riparazione di ${slug} non riuscita`)
        return { ...base, esito: 'consegnata la v5', collaudo: 'riparazione fallita', violazioni: viol.length }
      }
      if (fix.informazioni_perse && fix.informazioni_perse.length) {
        log(`  ${slug}: la riparazione dichiara ${fix.informazioni_perse.length} voci non rimesse — il collaudo del giro dopo le ritrovera.`)
      }
    }

    return { ...base, esito: 'NON CONSEGNABILE', collaudo: 'non superato' }
  }
)

return results.filter(Boolean)

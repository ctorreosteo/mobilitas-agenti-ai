export const meta = {
  name: 'genera-bibbie-osteopatiche',
  description: 'Per ogni condizione: Bibbia teorica (~20 pagine) + Mappa concettuale, revisione su sei livelli (1o parallelo sul contenuto, 2o fedelta all architettura + ampliamento scientifico ai tre cerchi, 3o logica dell apprendimento, 4o editor di asciugatura, 5o riscrittura integrale in linguaggio semplice, 6o revisione di lingua italiana), poi COLLAUDO DI CONSERVAZIONE con riparazione mirata. Nessuna versione arriva alla consegna senza cancello. Resiliente: retry sugli agenti critici + fallback di promozione, un singolo fallimento non aborta la catena',
  whenToUse: 'Genera le Bibbie teoriche Mobilitas in batch a partire da PROBLEMI_OSTEOPATIA.xlsx',
  phases: [
    { title: 'Scoperta', detail: 'trova da solo le skill-revisore presenti nella cartella' },
    { title: 'Draft', detail: 'skill direttore-osteopatico-teoria redige v1 Bibbia + Mappa' },
    { title: 'Revisione', detail: 'TUTTI i revisori di 1o livello, in parallelo, feedback per severita' },
    { title: 'Sintesi intermedia', detail: 'skill autore pesa i feedback e riscrive la v2' },
    { title: 'Revisione 2o livello', detail: 'fedelta all architettura + evidenza estesa, sulla v2' },
    { title: 'Sintesi v3', detail: 'skill autore applica i feedback di 2o livello -> v3' },
    { title: 'Revisione 3o livello', detail: 'logica dell apprendimento, sulla v3' },
    { title: 'Sintesi v4', detail: 'skill autore applica i rilievi di apprendimento -> v4' },
    { title: 'Revisione 4o livello', detail: 'editor di asciugatura, sulla v4' },
    { title: 'Sintesi v5', detail: 'skill autore applica la mappa di taglio dell editor -> v5' },
    { title: 'Riscrittura finale', detail: 'skill chiarezza riscrive TUTTO da capo in linguaggio semplice -> v6' },
    { title: 'Revisione di lingua', detail: 'skill italiano toglie i calchi e raddrizza la sintassi -> v7 finale' },
    { title: 'Collaudo', detail: 'script deterministico + collaudatore semantico sulla coppia v5/v7; riparazione mirata se serve' },
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
// Registro della lingua: i calchi ricorrenti e i passaggi che restano oscuri. Lo scrivono
// il 5o e il 6o livello, lo legge l'autore prima di scrivere. Chiude il ciclo di
// apprendimento: senza, ogni Bibbia rinasce con i difetti di scrittura della precedente.
const REGISTRO_LINGUA = OUT + '/_dati/registro-lingua.md'

// ---- RUOLI E LIVELLI DECISI DAL MANIFESTO, NON DAL CODICE ----
// L'ESISTENZA dei revisori resta auto-scoperta dalla cartella .claude/skills.
// Il RUOLO e il LIVELLO (autore / 1o / 2o / 3o / 4o / 5o livello) li decide ESPLICITAMENTE
// bibbie-generate/_dati/livelli.json. Un revisore presente nella cartella ma non elencato
// NON viene usato. Cosi aggiungi/togli/sposti revisori modificando solo quel file.
const MANIFESTO = OUT + '/_dati/livelli.json'

// ---- NOMI DEI FILE DELLA CATENA ----
// v5 = ultima versione con il contenuto approvato dai livelli 1-4.
// v6 = riscrittura integrale in linguaggio semplice (5o livello).
// v7 = revisione di lingua italiana (6o livello). E' il DELIVERABLE.
// Il collaudo confronta v5 contro v7: cosi' verifica le due riscritture insieme.
const F = (slug) => ({
  v5: `${OUT}/${slug}/v5-intermedia.md`,
  m5: `${OUT}/${slug}/mappa-v5.md`,
  v6: `${OUT}/${slug}/v6-chiarezza.md`,
  m6: `${OUT}/${slug}/mappa-v6.md`,
  v7: `${OUT}/${slug}/v7-finale.md`,
  m7: `${OUT}/${slug}/mappa-finale.md`,
})

// Schema della fase di scoperta: cartelle reali + ruoli/livelli espliciti dal manifesto.
const DISCOVERY_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['tutte_le_skill', 'autore', 'primo_livello', 'secondo_livello', 'terzo_livello', 'quarto_livello', 'quinto_livello', 'sesto_livello', 'collaudo'],
  properties: {
    tutte_le_skill: { type: 'array', items: { type: 'string' }, description: 'Chiavi (dopo "direttore-osteopatico-") di TUTTE le cartelle skill realmente presenti' },
    autore: { type: 'string', description: 'Chiave dell autore dal manifesto (di norma "teoria")' },
    primo_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di PRIMO livello dal manifesto' },
    secondo_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di SECONDO livello dal manifesto' },
    terzo_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di TERZO livello dal manifesto (di norma "apprendimento")' },
    quarto_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di QUARTO livello dal manifesto (di norma "editor")' },
    quinto_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei riscrittori di QUINTO livello dal manifesto (di norma "chiarezza")' },
    sesto_livello: { type: 'array', items: { type: 'string' }, description: 'Chiavi dei revisori di SESTO livello dal manifesto (di norma "italiano"): la revisione della lingua' },
    collaudo: { type: 'array', items: { type: 'string' }, description: 'Chiavi del CANCELLO di conservazione dal manifesto (di norma "collaudo"). Non e un livello di revisione: verifica che le riscritture non abbiano perso niente' },
  },
}

const discoveryPrompt = () => `Devi determinare ruoli e livelli delle skill di questo studio combinando la cartella reale e il manifesto.

1) Esegui: ls -1 ${SK}
   Prendi TUTTE le cartelle che iniziano con "direttore-osteopatico-" e per ognuna estrai la chiave = la parte dopo quel prefisso (es. "direttore-osteopatico-compliance" -> "compliance"). Questo e "tutte_le_skill".
2) Leggi il manifesto ${MANIFESTO} (JSON). Prendi "autore" (una chiave), "primo_livello", "secondo_livello", "terzo_livello", "quarto_livello", "quinto_livello", "sesto_livello" e "collaudo" (array di chiavi; un array puo mancare o essere vuoto -> restituisci []).

Restituisci l'oggetto strutturato con: tutte_le_skill, autore, primo_livello, secondo_livello, terzo_livello, quarto_livello, quinto_livello, sesto_livello, collaudo.
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
          tipo: { type: 'string', description: 'INFORMAZIONE_PERSA / QUALIFICAZIONE_CADUTA / FRASE_PONTE_CADUTA / ETICHETTA_RIANCORATA / ETICHETTA_ALZATA / VERBO_IRRIGIDITO / NUMERO_RIATTRIBUITO / PROMESSA_INTRODOTTA / MATERIALE_OPERATIVO / STRUTTURA_ALTERATA / HA_RISCRITTO_INVECE_DI_CORREGGERE' },
          passaggio: { type: 'string', description: 'In quale delle due riscritture e nata: CHIAREZZA (v5->v6) / LINGUA (v6->v7) / INCERTO' },
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
Una **Bibbia** e' ~20 pagine con TUTTO quello che un osteopata deve SAPERE su quella condizione per poterla risolvere in poche sedute. NON e' una procedura operativa: **niente tecniche, niente dosi da somministrare, niente sequenze, niente minuti, niente piani di seduta, niente scheda operativa**. Quelli stanno in un documento separato di 2 pagine, scritto da un altro agente. Il tuo Capitolo 11 arriva fino al RAZIONALE della leva e si ferma li'.

**UNICA ECCEZIONE al confine, e va capita bene:** il parametro usato in uno STUDIO e' un dato di evidenza, non una prescrizione. *"Nello studio hanno svolto [l'esercizio] per [N] settimane"* sta nella Bibbia; *"fai fare [N] settimane al paziente"* sta nella Procedura. Il criterio e' il TEMPO VERBALE e il DESTINATARIO: passato e attribuito a uno studio = evidenza; imperativo e rivolto al nostro paziente = protocollo.

## Istruzioni della skill (leggile e seguile INTEGRALMENTE, in quest'ordine)
1. Leggi ${AUTORE}/SKILL.md
2. Poi, in quest'ordine, i reference in ${AUTORE}/references/:
   - architettura-bibbia.md (la struttura fissa dei 15 capitoli e le cinque regole di struttura)
   - lessico-del-metodo.md (le parole che ricorrono in TUTTE le Bibbie, con definizione A TESTO FISSO: marker, reperto disfunzionale, disfunzione somatica, compenso, catena, sistema dominante, lesione primaria. Si riportano, non si riformulano; box Definizione alla prima comparsa IN OGNI CAPITOLO in cui appaiono, e voce a Glossario. Nessuna variante lessicale.)
   - regole-di-scrittura.md (COME si scrive: la leggibilita' e' un requisito, non una preferenza)
   - cinque-modelli-osteopatici.md (impalcatura del Capitolo 7)
   - motore-clinico.md (il ragionamento del Capitolo 8)
   - ancore-verificate.md e ancore-scientifiche.md (ancora scientifica e protocollo di verifica)
   - mappa-concettuale.md (il secondo deliverable)
   - sistema-libreria.md (coerenza col corpus)

## Precedenza scientifica — leggi PRIMA di scrivere
Apri ${REGISTRO_LINGUA} e leggi la sezione **Correzioni attive**: sono errori di scrittura gia' corretti a valle su altre condizioni. Non rifarli nella v1 e' il modo piu' economico di averli risolti. Bastano trenta secondi.

Apri ${DEVIAZIONI}. Registra i punti in cui il metodo interno e' stato trovato fattualmente sbagliato, con la formulazione corretta da usare al suo posto. **L'accuratezza scientifica viene prima della fedelta' al metodo**. Se ne trovi uno NUOVO: correggi e apri una voce con stato PROPOSTA e la fonte; NON modificare i documenti di metodo (la ratifica e' umana).

## Dati del problema
Apri ${DATA}, trova l'oggetto con "slug": "${slug}" e usa TUTTI i suoi campi (sintomi, soluzioni_provate, farmaci, esami_strumentali, benefici_trattamento, ads_pain_points, red_flag, meccanismo_causa, meccanismo_trattamento, obiezioni_specifiche) come materia prima. Sono la voce del paziente e del mercato: il Capitolo 1 ("Chi ti trova davanti") nasce da li', e il Capitolo 13 risponde a quelle obiezioni.

## Ricerca scientifica — OBBLIGATORIA, e su TRE CERCHI
Prima di scrivere qualunque affermazione di evidenza DEVI cercare sul web e verificare ogni studio: titolo/autore/anno/PMID reali, e il risultato letto NELL'ABSTRACT. Se non verifichi uno studio, non citarlo.

Non fermarti al primo cerchio: e' l'errore che rendeva povere le Bibbie sulle condizioni poco studiate.
- **Cerchio 1 — specifico:** quell'intervento su questa condizione. Regge DIMOSTRATO su una LEVA. Quasi sempre e' il cerchio piu' povero.
- **Cerchio 2 — trasversale sul meccanismo:** tocco e sistema autonomico (HRV, conduttanza, fibre C-tattili), terapia manuale e modulazione del dolore, interocezione e percezione del sintomo, respiro e tono vagale, contesto/aspettativa/alleanza terapeutica, esercizio e carico sulla funzione coinvolta. Regge DIMOSTRATO su un MECCANISMO.
- **Cerchio 3 — fisiologico:** anatomia e fisiologia misurate. Regge il RAZIONALE, mai l'efficacia.

**REGOLA DEL PONTE, non negoziabile:** l'evidenza del cerchio 2 alza l'etichetta del MECCANISMO, mai quella della LEVA su questa condizione. Ogni fonte del cerchio 2 porta la frase che dichiara il salto: "misurato su X, non su pazienti con questa condizione". Senza questa regola scrivi mechanism-mongering, e un revisore evidence-based lo smonta in dieci minuti portandosi via anche le citazioni corrette.

Scegli **due ancore** se serve: quella clinica (chi ha fatto studi controllati su questa condizione, coi suoi limiti) e quella fisiologica (chi ha stabilito il meccanismo). Su molte condizioni la seconda e' molto piu' autorevole della prima, e dichiararlo e' piu' forte che gonfiare.

**Se la letteratura specifica e' sottile, la sezione «Quando la scienza tace» dentro il Capitolo 10 e' OBBLIGATORIA**, coi suoi cinque punti: assenza di prove non e' prova di assenza · perche' quella letteratura non esiste · su cosa ti basi (meccanismo, ragionamento dichiarato, verifica sul singolo paziente con un marker scelto PRIMA) · cosa lo separa dal pensiero magico (la verifica, e solo quella) · cosa non autorizza. Tono di un direttore che difende il suo mestiere con argomenti, mai di un documento che si scusa.

## Il Capitolo 12 e' CONDIZIONALE
"Cosa puo' fare il paziente da solo" esiste **se e solo se** almeno uno strumento attivo — respirazione, rinforzo e controllo posturale, carico ed esposizione graduata, educazione — regge su questa condizione un DIMOSTRATO o un PROBABILE forte con piu' studi controllati. Su molte condizioni e' la leva con la MIGLIORE evidenza di tutto il documento, e il vecchio impianto la espelleva perche' somigliava a un protocollo.
Se la condizione e' soddisfatta: capitolo di 600-900 parole con le sei voci previste dall'architettura. Se NON e' soddisfatta: il capitolo non deve esserci, e non e' un buco.

## IL MARKER VA DEFINITO E VANNO NOMINATI QUELLI DI QUESTA CONDIZIONE
"Marker" e' la parola piu' usata del metodo — regge il mandato del triage, la scadenza dell'uscita GIALLA e la prova della chiave di volta — ed e' quella che resta piu' spesso nuda. Definizione canonica a TESTO FISSO in ${AUTORE}/references/lessico-del-metodo.md, da riportare senza riformularla, con box Definizione alla prima comparsa in ogni capitolo e voce a Glossario.
**E nomina i marker DI QUESTA CONDIZIONE: da due a quattro, concreti**, ciascuno con come si misura e QUALE SOGLIA CONTA, e almeno uno che appartenga a un piano che non hai trattato. "Scegli un marker" senza dire quali lascia il lettore dov'era.
Lo stesso vale per gli altri termini canonici del metodo: reperto disfunzionale, disfunzione somatica, compenso, catena, sistema dominante, lesione primaria. Una parola, un significato, in tutto il corpus.

## LA PROVA DELL'ALTRA BIBBIA — il capitolo sui limiti non e' un disclaimer
**Se una riga sarebbe identica nella Bibbia di un'altra condizione, non appartiene a nessuna delle due.** Nel Capitolo 9 entra SOLO cio' che cambia con questa condizione.
**NON scrivere:** la meccanica del consenso informato (raccolta, documentazione, alternative, revocabilita', L. 219/2017); l'art. 9 GDPR, conservazione e condivisione dei dati; i requisiti di abilitazione e iscrizione — e MAI nella forma "verifica la tua", il lettore e' un collega del team, non un candidato da controllare; il testo di DPR 131/2021 e DPCM 2026 recitato per esteso (una riga di ancora, e basta).
**Scrivi invece:** COSA SI DICHIARA NEL CONSENSO SU QUESTA CONDIZIONE — le due o tre cose che qui aggiungi e in un'altra Bibbia non scriveresti; il confine di atto dove questa condizione lo mette alla prova; il rapporto con il prescrittore su questa terapia. E' l'unica parte che il lettore non sa gia'.
**E il capitolo non parla di se stesso:** niente frasi in cui il documento ragiona sulla propria posizione legale. Si scrive la cosa da dichiarare, non il ragionamento su perche' dichiararla.

## IL CANCELLO D'INGRESSO E' UN TRIAGE A TRE USCITE
Nel Capitolo 9 il cancello NON e' binario ("cosa deve essere gia' stato fatto dal medico"): e' un triage con tre uscite, perche' un cancello binario costringe a scegliere fra rimandare fuori tutti e non filtrare nessuno — e siccome nessuno rimanda fuori tutti, il comportamento reale resta non scritto, quindi senza reperto, senza paziente informato, senza canale medico, senza scadenza.
**Il principio che regge tutto, e va scritto per esteso:** il mandato NON nasce dalla diagnosi medica, nasce da un reperto disfunzionale documentato e da un marker che si muove quando lo tratti. **Col corollario simmetrico, che e' la parte che rende il triage piu' severo e non piu' permissivo: se non hai quelli, non hai un motivo per lavorare nemmeno con la diagnosi in mano.**
- **ROSSO — stop.** Anche una sola bandiera rossa. Indicazione medica esplicita e SCRITTA, tempi dichiarati. Nessuna eccezione, nessun reperto positivo la scavalca.
- **GIALLO — si lavora in parallelo.** Nessuna bandiera rossa, inquadramento assente o incompleto. E' LA SITUAZIONE PIU' FREQUENTE e non e' un motivo per rimandare fuori il paziente. Quattro condizioni: reperto tuo positivo e scritto in cartella · il paziente sa cosa tratti e cosa no · canale medico attivato con comunicazione SCRITTA al curante, non un rinvio del paziente · tempo definito, con revisione programmata. **E si scrive cosa succede se scade senza risposta:** non e' una rinuncia, e' un'informazione — il tuo reperto non era il driver, e la spinta sul canale medico diventa prioritaria.
- **VERDE — si procede** secondo Procedura.
- **La scadenza:** l'inquadramento decade se il sintomo cambia carattere, sede o intensita'. Un quadro che cambia forma torna al triage dall'inizio.
- **IL CONTRAPPESO, da scrivere attaccato al principio del mandato:** *un reperto positivo giustifica il tuo lavoro, NON sostituisce l'inquadramento medico. Trovare il reperto tipico non esclude nulla: significa che hai qualcosa da trattare, non che sai cosa ha il paziente. Le due cose CONVIVONO, e vanno dette al paziente come conviventi.* Senza questa riga il principio del mandato si legge come "il mio reperto rende superfluo l'accertamento", ed e' la lettura che espone davvero. La convivenza ricompare con le stesse parole nel Capitolo 13.
- **LA TABELLA DELLE BANDIERE ROSSE**, tre colonne: Bandiera rossa | A chi si manda | Tempi. **Si prendono da dove le LINEE GUIDA di riferimento della condizione indicano l'accertamento specialistico** — cercale e citale, non comporle a intuito e non copiarle da un'altra condizione. Tempi con vocabolario chiuso: 112 / Urgente / Invio, non attendere / Invio / Invio programmato.
- **PERCHE' PROTEGGE DI PIU', da scrivere:** il cancello vecchio dichiarava un requisito e nella pratica veniva aggirato — **una regola scritta e disattesa vale meno di nessuna regola**, perche' fa credere che un controllo esista. Questo dichiara cosa fai davvero in ciascuna situazione, tiene il ROSSO rigido, e mette per iscritto l'unico elemento che rende difendibile il GIALLO.
- **Il vincolo che non si negozia:** tutte e tre le uscite poggiano su qualcosa di SCRITTO. Quello che non e' scritto non esiste — un triage non documentato e' un'intenzione, e le intenzioni non reggono un perimetro professionale.
Lo SCHELETRO e' fisso, le CASELLE si compilano su questa condizione: bandiere rosse, cosa significa "inquadramento", quali accertamenti contano come coerenti. Non ricopiare la formulazione di un'altra condizione.

## LO SLOT «PERCHE' CI SEI TU» — quarto bullet di ogni capitolo
Ogni capitolo chiude con **«Le tre cose da ricordare, piu' una»**: QUATTRO bullet. I primi tre sono le cose che cambiano il comportamento in stanza. Il quarto e' uno slot fisso, sempre in ultima posizione:
**Perche' ci sei tu.** [Il dato, in parole semplici.] Questo ti autorizza a [cosa]. Non ti autorizza a [cosa].
E' una voce FATTUALE in un posto motivazionale. Il dato e' una **lacuna misurata**, mai un'opinione sull'utilita' del nostro lavoro, e deve **essere gia' nel documento**: lo slot sintetizza, non introduce.
**La terza parte non e' difensiva: e' cio' che rende credibile la prima.** Un'affermazione senza confine dichiarato viene letta come pubblicita' e scontata; col confine viene letta come una posizione.
Tre fonti valide, in ordine di forza: (1) il farmaco non copre tutto — quota di sintomatici in terapia; (2) il meccanismo e' nel nostro dominio — struttura muscolo-scheletrica dentro la fisiopatologia; (3) la leva con evidenza e' nostra da insegnare — esercizio, respiro, educazione, abitudini. Se per questa condizione non riesci a compilarne NESSUNA, quella e' l'informazione piu' importante del documento e va scritta.
**Una per capitolo, tutte DIVERSE:** nessun dato si ripete. Quindici volte lo stesso numero e' morto entro il quarto capitolo.
**Il dato puo' anche RESTRINGERE lo spazio, e la struttura non cambia** — es. "Su questo sottotipo non ci sei: [dato]. Questo ti autorizza a riconoscerlo e mandarlo, non a trattarlo." Un capitolo senza lacuna a nostro favore ne ha sempre una a nostro sfavore. **Almeno uno slot deve restringere**: se tutti allargano, il documento vende. Mai inventare uno slot debole per riempire la casella.
La **Mappa** porta un solo blocco «Perche' ci sei tu», il piu' forte dei quindici.

## Come si scrive un DATO NUMERICO — regola con potere di taglio
Ogni numero risponde a tre domande in quest'ordine: (1) percentuale DI COSA e SU CHI, in parole e non in gergo; (2) DA DOVE VIENE, cioe' quale tipo di paziente e' stato misurato; (3) COSA CAMBIA PER ME, la conseguenza in stanza.
**Il terzo e' obbligatorio. Un numero senza la riga "Per te" si TAGLIA**: se non riesci a scrivere cosa comporta, quel dato non serve al lettore, serve a far sembrare documentato il paragrafo.
Formato: [dato in parole semplici, con "su dieci" o "su cento"] [su chi e' stato misurato, una riga] **Per te:** [cosa ci fai] (Fonte, anno, PMID). "Per te:" sta IN LINEA, non e' un quinto tipo di box.
**Regola dei due numeri:** se due numeri dicono cose diverse, metti PER PRIMO quello vicino al nostro paziente; l'altro dopo come confronto, con il motivo della differenza in una frase. Mai affiancarli lasciando al lettore la scelta.
**Mai:** percentuali che non dicono di cosa; gergo di disegno sperimentale non tradotto ("pooled prevalence", "trial interventistici non randomizzati"); intervalli senza il perche' oscillano; un numero senza conseguenza operativa.
**In tabella i numeri IDENTIFICANO uno studio, in prosa AFFERMANO.** Solo i secondi chiedono il formato completo, e un numero che porta un'affermazione non puo' vivere solo in tabella.
**Quanti:** nessun tetto, ma ogni numero in prosa costa 60-80 parole. Se non riesci a scrivere il "Per te" senza ripetere quello di un altro numero, i due dicono la stessa cosa e ne resta uno.
**Prova finale:** chi legge deve poter chiudere il paragrafo e dire ad alta voce cosa fara' di diverso domani. Se non gli e' cambiato niente, il numero era decorazione.
Il dettaglio con il prima/dopo sta in ${AUTORE}/references/regole-di-scrittura.md.

## VIETATO il vicolo cieco
Nessuna frase che dice cosa NON funziona puo' restare da sola: nella stessa riga si dice quale leva tiene, o dove va il paziente.
La forma vietata e' il negativo troncato — "su un sistema in allarme nessun lavoro locale tiene", e punto. **NON e' una frase incompleta: e' una frase FALSA**, e lo e' proprio per la ragione che sembra giustificarla. Se il driver e' il livello di attivazione, allora l'attivazione E' IL BERSAGLIO, ed e' precisamente cio' che il contatto lento, il ritmo del respiro e il tempo dedicato modulano — il documento lo scrive tre capitoli dopo, e questa frase lo nega.
Sotto c'e' un vizio lessicale: **"lavoro locale" non e' "lavoro manuale"**. Lavorare sull'attivazione e' lavoro manuale a tutti gli effetti, mirato altrove. Ma chi legge non fa la distinzione: legge "le mie mani non servono qui" e manda via un paziente che poteva prendere.
**Un sintomo legato allo stato di attivazione non e' un capolinea: e' l'indicazione piu' chiara che esista per la leva che sull'attivazione agisce.** E' il paziente in cui hai PIU' da fare, non meno — con l'etichetta e i tempi reali di quella leva, ma con quella direzione.
**Ogni paziente-tipo del Capitolo 8 finisce con quello che fai**, mai con quello che non funziona. E il Capitolo 8 NON puo' negare una leva che il Capitolo 11 dichiara: se succede, uno dei due e' sbagliato.
Il caso che ricorre su ogni condizione: il paziente il cui driver e' il LIVELLO DI ATTIVAZIONE (allarme, ipervigilanza, sintomo agganciato a un evento di vita). Non e' un vicolo cieco, e' **l'indicazione della leva che agisce sull'attivazione** — con la sua etichetta reale, ne' una di piu' ne' una di meno. Non curare il pessimismo con l'ottimismo: il difetto e' l'omissione della leva, non la sua qualificazione.

## Il Capitolo 0 — come si STUDIA, non cosa si salta
Il Capitolo 0 contiene la sezione **«Come si studia questa Bibbia»** con i sei passi dell'architettura (lettura di fila senza appunti · seconda passata con un paziente in testa · la prova a documento chiuso · la Mappa prima del primo paziente · rilettura dei limiti dopo i primi tre · a sei mesi solo la Mappa). **VIETATO il triage di lettura** ("se hai venti minuti leggi questi otto capitoli"): e' un invito a non finire il documento e dichiara accessori i capitoli esclusi. Se un capitolo e' saltabile si toglie, non si declassa.

## Il Capitolo 14 e' OBBLIGATORIO
"Cosa fare adesso": 250-400 parole, tre blocchi — il filo del documento ricucito in cinque righe (non un elenco di capitoli), esattamente TRE cose che il lettore cambia da lunedi (una che guarda, una che dice, una che smette), e due o tre righe nella voce che motiva. Nessun contenuto nuovo, nessuna promessa di esito, nessun lessico da brochure.

## L'etichetta di solidita' — il dispositivo centrale
La prosa AFFERMA; l'onesta' la porta un box separato \`> **Quanto e solido:**\` con una di quattro etichette: DIMOSTRATO / PROBABILE / IPOTESI / RAGIONAMENTO. Ogni meccanismo, ogni modello e ogni leva ne porta una.
**Ogni etichetta porta la sua GLOSSA FISSA, ogni volta che compare**, con queste parole esatte: DIMOSTRATO *(studi sull'uomo, solidi)* · PROBABILE *(razionale forte, prove parziali)* · IPOTESI *(meccanismo coerente, nessuno studio)* · RAGIONAMENTO *(cornice clinica, non una prova)*. Spiegarle solo nel Capitolo 0 non funziona: il lettore le incontra trenta volte in venti pagine e a meta' documento non ricorda piu' la differenza. Le quattro etichette vanno anche a Glossario e nella Mappa. Vietato qualificare dentro la frase ("potrebbe eventualmente", "pur con le dovute cautele").

## Output
Scrivi in markdown, **8.000-13.000 parole** (appendici escluse):
- ${OUT}/${slug}/v1-bibbia.md → la Bibbia completa (capitoli 0-14, con il 12 condizionale, + Appendice A Glossario + Appendice B Fonti)
- ${OUT}/${slug}/v1-mappa.md  → la Mappa concettuale (una pagina, sei blocchi)
Crea la cartella se non esiste. Non convertire in .docx: consegna markdown.

Alla fine restituisci SOLO: numero parole della Bibbia + ancora scientifica scelta + una riga di note. I file sono gia' il deliverable.`

const reviewPrompt = (slug, r) => `Sei il revisore **${r.key}** del panel avversariale Mobilitas (PRIMO livello). Devi revisionare una BIBBIA TEORICA osteopatica.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md (e i suoi reference se ne cita). Adotta esattamente quella prospettiva, con lo stesso obbligo di ricerca e la stessa severita.

## Perimetro — non chiedere protocolli
Quella che rivedi e' una Bibbia teorica (~20 pagine: cos'e', perche' succede, quali meccanismi, quanto e' solido, perche' le mani possono agire, cosa puo' fare il paziente da solo se la scienza lo sostiene). **Non contiene, e non deve contenere, tecniche, dosi da somministrare, sequenze o piani di seduta**: quelli stanno in una Procedura separata di 2 pagine. Un rilievo che chieda un protocollo e' fuori perimetro: scartalo da solo. Se invece TROVI un protocollo dentro la Bibbia, quello si segnala come materiale fuori posto.

**Eccezione da conoscere prima di segnalare un falso positivo:** il parametro usato in uno STUDIO e' un dato di evidenza e sta legittimamente nella Bibbia ("nello studio hanno allenato per otto settimane"). Diventa protocollo quando cambia tempo verbale e destinatario ("fai fare otto settimane al paziente"). Il criterio e' passato-e-attribuito contro imperativo-e-rivolto-al-nostro-paziente. Allo stesso modo, il Capitolo 12 "Cosa puo' fare il paziente da solo" e' un capitolo previsto dall'architettura quando uno strumento attivo regge DIMOSTRATO o PROBABILE forte: non e' materiale fuori posto.

Nota sulle etichette: ogni affermazione importante porta un box \`> **Quanto e solido:**\` (DIMOSTRATO / PROBABILE / IPOTESI / RAGIONAMENTO). Un'affermazione diretta con etichetta corretta NON e' un claim gonfiato: e' la forma prevista. Il claim gonfiato e' l'etichetta troppo alta, o assente.

## Se la tua SKILL ti impone la ricerca sul web, falla
Alcune lenti di questo panel hanno un obbligo di ricerca (evidenza, strumenti attivi, specialista). Se e' il tuo caso: ogni studio che citi o proponi va verificato in questa sessione — autore, anno, titolo, PMID, e il risultato letto NELL'ABSTRACT. Uno studio non verificato non si propone. Se non hai accesso alla ricerca web, dichiaralo e declassa i tuoi rilievi.

## Documento da revisionare
Leggi ${OUT}/${slug}/v1-bibbia.md (la Bibbia) e ${OUT}/${slug}/v1-mappa.md (la Mappa). Se non esistono, restituisci un rilievo ERRORE che dice che il draft manca.

## Output
Classifica OGNI rilievo per severita: ERRORE (fatto sbagliato/pericoloso, va corretto), RISCHIO (esposizione da valutare), PREFERENZA (gusto, ignorabile). Sii chirurgico: capitolo preciso, problema, correzione concreta. Non riscrivere la Bibbia, non elogiare: solo rilievi azionabili.

Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa leggibile in ${OUT}/${slug}/feedback-${r.key}.md`

// SINTESI INTERMEDIA (v2): pesa i feedback di TUTTI i revisori di 1o livello e riscrive.
const synthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la versione INTERMEDIA (v2) della Bibbia "${slug}" sintetizzando i feedback dei revisori di 1o livello. NON e' ancora la finale: dopo di te la v2 va al 2o livello.

## Metodo di sintesi (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Regola che protegge il documento: **il feedback si pesa, non si somma**. ERRORE si corregge; RISCHIO si valuta; PREFERENZA si ignora di default. Elimina i doppioni e i conflitti tra lenti. Se la Bibbia cresce oltre il 20%, hai sommato invece di pesare: ferma e ripesa.
**Scarta d'ufficio ogni rilievo che chieda tecniche, dosi da somministrare, sequenze o piani di seduta:** sono fuori dal perimetro della Bibbia.
**NON scartare** i rilievi del revisore degli strumenti attivi che chiedono di riportare i parametri usati NEGLI STUDI, ne' quelli che chiedono il Capitolo 12: sono dentro il perimetro (dato di evidenza, non prescrizione — vedi architettura-bibbia.md, sezione sull'eccezione di confine).

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
Lo standard contro cui si audita e' ${AUTORE}/references/architettura-bibbia.md (i 15 capitoli con il 12 condizionale, le cinque regole di struttura, le quattro etichette, l'eccezione di confine sui parametri di studio), piu' ${AUTORE}/references/cinque-modelli-osteopatici.md, ${AUTORE}/references/motore-clinico.md e ${AUTORE}/references/ancore-scientifiche.md (i tre cerchi, la regola del ponte, «Quando la scienza tace»).

## Se la tua SKILL ti impone la ricerca sul web, falla
Il 2o livello ospita anche il Ricercatore, che NON cerca difetti ma la scienza che manca. Se e' il tuo caso: esplora i tre cerchi (specifico / trasversale sul meccanismo / fisiologico), e **ogni studio che proponi va verificato in questa sessione** — autore, anno, titolo, PMID, risultato letto NELL'ABSTRACT. Uno studio non verificato non si propone. Vale la REGOLA DEL PONTE: l'evidenza trasversale alza l'etichetta del meccanismo, mai quella della leva su questa condizione, e ogni aggiunta porta la frase "misurato su X, non su questi pazienti". Se non hai accesso alla ricerca web, dichiaralo e non proporre studi.

**Se aggiungi contenuto, devi anche proteggerlo.** Chiudi il tuo feedback con una sezione **Da proteggere dall'editor** che elenca, riga per riga: ogni **frase-ponte** che dichiara il limite di una fonte trasversale ("misurato su X, non su questi pazienti"), ogni voce nuova di "cosa non possiamo dire", e ogni qualificazione che accompagna un'aggiunta. Senza questa sezione le tue aggiunte arrivano nude all'editor di 4o livello, che legge una cautela come ridondanza e la taglia: resterebbe il PMID e sparirebbe il limite, cioe' il contrario di quello che volevi.

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

Restituisci SOLO: cosa hai corretto dalla 2a revisione, cosa hai valutato/ignorato, variazione % di lunghezza rispetto alla v2, e l'elenco dei passaggi marcati **da proteggere dall'editor** nei feedback di 2o livello (riportalo: serve ai livelli successivi).`

// TERZA REVISIONE: la logica dell'apprendimento, sulla v3.
const thirdReviewPrompt = (slug, r) => `Sei il revisore di TERZO LIVELLO **${r.key}** del panel Mobilitas. La Bibbia e' gia' stata validata dai revisori di 1o e 2o livello: contenuto, sicurezza, compliance, fedelta' all'architettura e base scientifica sono chiusi.

Il 3o livello e' l'unico in cui si guarda il documento **intero**, non attraverso una lente e non capitolo per capitolo. Ospita due mandati diversi, e il tuo lo porta la tua SKILL:
- **apprendimento** — il documento insegna a ragionare su questa condizione, o fa solo sapere delle cose?
- **coerenza** — l'ispettore delle giunture: tieni aperti DUE capitoli alla volta e verifichi che non si contraddicano. Le contraddizioni non nascono nella bozza, nascono nelle SINTESI: l'autore applica undici feedback capitolo per capitolo e patcha un capitolo senza rileggere quello che lo contraddice. Giri dopo l'ultima sintesi che cambia contenuto, ed e' per questo che sei qui.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md (e i suoi reference, se ne cita). Adotta esattamente quel mandato: la SKILL contiene il metodo, l'elenco dei controlli e il formato di output. Non chiedere tecniche, dosi o esercizi: sono fuori perimetro.

## Tre confini rigidi
1. **Non aggiungi contenuto clinico**: niente meccanismi, studi, bandiere rosse o cautele nuove. Se manca qualcosa, lo costruisci con il materiale gia' presente, spostandolo o esplicitandone il senso. Se stai riconciliando una contraddizione, **dichiara quale dei due lati va corretto**: un rilievo che dice solo 'questi due capitoli non concordano' scarica sulla sintesi una decisione che spetta a te, e la sintesi sceglie a caso.
2. **Non asciughi**: dopo di te c'e' l'editor (4o livello). Una ripetizione con funzione didattica e' un pregio: segnalala tra le cose DA PROTEGGERE.
3. **Non gonfi**: preferisci lo spostamento all'aggiunta. Ogni rilievo che aggiunge testo dichiara quante parole costa. Budget complessivo: crescita netta **<= 5%**.

Rispetta l'INTOCCABILE (bandiere rosse, limiti di campo, etichette di solidita', PMID/dati, hedge di compliance, le tre voci, l'architettura dei 15 capitoli, le aperture "In una riga" e le chiusure "Le tre cose da ricordare"). Se il documento gia' insegna, il verdetto legittimo e' "Insegna".

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
- Rilievi di 3o livello (apprendimento E coerenza): leggi TUTTI i file ${OUT}/${slug}/feedback-*-r3.md. **Le contraddizioni segnalate dalla coerenza si correggono sempre**, e sul lato che il revisore ha indicato: non sono preferenze, sono due affermazioni incompatibili nello stesso documento.

## Output
- ${OUT}/${slug}/v4-intermedia.md → Bibbia v4
- ${OUT}/${slug}/mappa-v4.md      → Mappa v4

Restituisci SOLO: quali fasi hai colmato e come (spostamento / riscrittura / aggiunta), cosa hai ignorato, la variazione % rispetto alla v3, e l'elenco dei passaggi marcati **da proteggere dall'editor** (riportalo, serve al livello successivo).`

// QUARTA REVISIONE: l'editor di asciugatura, sulla v4. Produce una MAPPA DI TAGLIO.
const fourthReviewPrompt = (slug, r) => `Sei il revisore di QUARTO LIVELLO **${r.key}** del panel Mobilitas — l'editor di asciugatura. La Bibbia e' gia' validata sul contenuto, sulla fedelta' all'architettura e sull'impianto didattico. Tu NON aggiungi ne' contesti la sostanza: produci una MAPPA DI TAGLIO per togliere ridondanza e riportare il documento nel range **8.000-13.000 parole**, senza perdere informazione e senza spegnere la voce.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md. Rispetta l'INTOCCABILE (bandiere rosse, limiti di campo, **etichette di solidita'**, PMID/dati, hedge di compliance, le tre voci, le aperture "In una riga" e le chiusure "Le tre cose da ricordare", Glossario e Fonti). Se il documento e' gia' nel range e non trovi ridondanza vera, il verdetto legittimo e' "Gia' asciutta".

## Cosa arriva dopo di te
Dopo di te girano il 5o livello (**chiarezza**), che riscrive tutto in linguaggio semplice e puo' allungare il testo fino al 10%, e il 6o (**italiano**), che raddrizza la lingua entro il +-3%. Tre conseguenze: (a) **non e' compito tuo semplificare** — una frase corretta ma contorta la riscrive il 5o, tu tagli solo cio' che e' detto due volte; (b) **non e' compito tuo far suonare italiana una frase** — se ne occupa il 6o; (c) **tieni un margine**: se il documento e' al limite alto del range, punta al centro, non al tetto.

## Vincolo aggiuntivo: cosa hanno protetto i livelli prima di te
Leggi la sezione **Da proteggere dall'editor** in DUE posti, ed entrambi sono vincolanti:

1. **${OUT}/${slug}/feedback-*-r3.md** (3o livello) — passaggi con funzione didattica. Una ripetizione che ancora il senso al punto d'uso NON e' ridondanza.
2. **${OUT}/${slug}/feedback-*-r2.md** (2o livello) — le **frasi-ponte** che dichiarano il limite di una fonte trasversale ("misurato su X, non su pazienti con questa condizione"), le voci di "cosa non possiamo dire", le qualificazioni che accompagnano una fonte aggiunta. Sembrano cautele ridondanti e non lo sono: sono l'unica cosa che impedisce a uno studio vero di sostenere un claim falso. **Tagliare la frase-ponte e lasciare il PMID e' la trasformazione piu' dannosa che tu possa fare a questo documento.**

Se ritieni comunque che uno di questi passaggi vada tagliato, classificalo al massimo come PREFERENZA.

## Documento da revisionare
Leggi ${OUT}/${slug}/v4-intermedia.md e ${OUT}/${slug}/mappa-v4.md. Se non esistono, restituisci un rilievo ERRORE che dice che la v4 manca.

## Output
Mappa il tuo output sullo schema per severita: **RIDONDANTE -> ERRORE** (taglio sicuro, l'info esiste identica altrove), **COMPRIMIBILE -> RISCHIO** (stessa sostanza in meno parole), **PREFERENZA -> PREFERENZA**. Per ogni rilievo indica capitolo/passaggio, cosa tagliare o come comprimere, e dove resta l'informazione. Segnala a parte eventuale materiale FUORI PERIMETRO (tecniche, dosi, sequenze in un documento teorico). Non riscrivere la Bibbia.
Restituisci l'oggetto strutturato richiesto. In parallelo salva la stessa cosa in ${OUT}/${slug}/feedback-${r.key}-r4.md`

// SINTESI v5: applica la mappa di taglio dell'editor alla v4.
const fifthSynthPrompt = (slug) => `Sei il **Direttore Osteopatico** di Mobilitas. Devi produrre la v5 della Bibbia "${slug}", applicando la mappa di taglio dell'editor (4o livello) alla v4. NON e' la versione consegnata: dopo di te la v5 va al riscrittore di chiarezza (5o livello), che la riscrive integralmente.

## Metodo (seguilo INTEGRALMENTE)
Leggi ${AUTORE}/SKILL.md e ${AUTORE}/references/revisione-e-sintesi.md. Regola: **si asciuga solo se strettamente necessario**. Applica i tagli RIDONDANTE; valuta i COMPRIMIBILE solo se servono a rientrare nel range 8.000-13.000 parole; ignora le PREFERENZE di default. NON toccare l'INTOCCABILE (bandiere rosse, limiti di campo, etichette di solidita', PMID, **frasi-ponte**, hedge, le tre voci, Glossario e Fonti) ne' i passaggi marcati **da proteggere** nei feedback di 2o livello (${OUT}/${slug}/feedback-*-r2.md) e di 3o livello (${OUT}/${slug}/feedback-*-r3.md). Se la v4 e' gia' asciutta, copiala nella v5 senza modifiche.

## Input
- Bibbia v4: ${OUT}/${slug}/v4-intermedia.md e ${OUT}/${slug}/mappa-v4.md
- Mappa di taglio: leggi TUTTI i file ${OUT}/${slug}/feedback-*-r4.md
- Da proteggere: la sezione omonima nei file ${OUT}/${slug}/feedback-*-r2.md e ${OUT}/${slug}/feedback-*-r3.md

## Output
- ${OUT}/${slug}/v5-intermedia.md → Bibbia v5
- ${OUT}/${slug}/mappa-v5.md      → Mappa v5

Restituisci SOLO: cosa hai tagliato (RIDONDANTE), cosa hai compresso o lasciato, cosa hai protetto su indicazione del 3o livello, e la lunghezza finale in parole.`

// QUINTO LIVELLO: NON e' una revisione. E' una RISCRITTURA INTEGRALE che produce il deliverable.
const rewritePrompt = (slug, r) => `Sei il revisore di QUINTO livello del panel Mobilitas — **il Traduttore**. Non emetti rilievi: **riscrivi da capo l'intero documento**.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md e il suo reference ${r.skill}/references/regole-di-chiarezza.md (i prima/dopo: leggili, sono il metodo).

Prima di te sono girati quindici revisori: contenuto, sicurezza, compliance, fedelta' al metodo, impianto didattico e lunghezza sono chiusi. **Non tocchi niente di tutto questo.** Il tuo problema e' un altro: il documento e' giusto ma si legge male.

Dopo di te c'e' il 6o livello (**italiano**), che toglie i calchi dall'inglese e raddrizza i nessi logici. Due conseguenze: **non fermarti su una frase perche' "non suona"** — se e' chiara va bene, la fa suonare lui; e **non alzare il registro** per farla sembrare piu' italiana, disferesti il tuo stesso lavoro. Tu lavori sulla complessita', lui sulla naturalezza.

> Riscrivi l'intera Bibbia in modo che un osteopata neolaureato la legga dall'inizio alla fine **senza rileggere una sola frase**, e **senza che si perda una sola informazione**.

## Il metodo: si riscrive, non si corregge
1. Leggi tutto il documento senza scrivere niente.
2. Costruisci l'**inventario delle informazioni**: capitolo per capitolo, ogni fatto, numero, meccanismo, etichetta, bandiera rossa, citazione, definizione. E' il tuo contratto.
3. Riscrivi capitolo per capitolo **guardando l'inventario, non il vecchio testo**. Se hai il vecchio testo davanti mentre scrivi, ne copierai la sintassi.
4. Ricontrolla l'inventario alla fine: ogni voce non ricomparsa e' un'informazione persa, rimettila.

## Le regole
Frasi da 18-20 parole in media, 30 al massimo. Una subordinata per frase, mai una dentro l'altra. Prima la conclusione, poi la spiegazione. Voce attiva. Ogni termine tecnico spiegato dove compare e messo a Glossario. L'incertezza sta nell'etichetta \`> **Quanto e solido:**\`, mai nei giri di parole. Le catene causali diventano passaggi numerati. Lessico corto ("per" non "al fine di", "e'" non "risulta essere").

## L'INVIOLABILE
Riscrivi **come e' detto**, mai **cosa e' detto**. Restano identici: ogni numero, percentuale e misura; ogni PMID, autore, anno e titolo; **ogni etichetta di solidita' — non alzarne nessuna, mai**; ogni bandiera rossa, criterio di invio e limite di campo; **ogni frase-ponte** che dichiara il limite di una fonte ("misurato su X, non su pazienti con questa condizione"); ogni nome anatomico; l'architettura (capitoli, ordine, titoli, aperture "In una riga", chiusure "Le tre cose da ricordare", i quattro tipi di box); le tre voci e le frasi-firma dello studio.

## Lunghezza
Da **-5% a +10%** rispetto al testo che ricevi. Sotto -5% hai tagliato informazione. Sopra +10% hai aggiunto contenuto.

## Documento da riscrivere
Leggi ${F(slug).v5} (la Bibbia) e ${F(slug).m5} (la Mappa). Se non esistono, fermati e dillo.

## Output
- ${F(slug).v6} → la Bibbia riscritta integralmente
- ${F(slug).m6} → la Mappa riscritta con lo stesso criterio

Scrivi **tutti** i capitoli e **tutte** le appendici. Non lasciare rimandi al vecchio testo: il file nuovo deve essere completo e autosufficiente.

## Prima di chiudere: deposita il segnale
Se hai trovato passaggi che non sei riuscito a semplificare perche' il concetto sotto era confuso, **aggiungili in fondo a ${REGISTRO_LINGUA}**, sezione «Osservazioni», in un blocco intitolato con la condizione "${slug}". Una riga per passaggio: capitolo per nome, di cosa si tratta, perche' non si lasciava semplificare.
**Solo append: aggiungi in fondo, non riscrivere il file.** Piu' Bibbie possono girare insieme, e riscrivendolo cancelleresti il blocco di un'altra.

Restituisci l'oggetto strutturato richiesto. In "passaggi_incomprensibili" metti gli stessi punti: e' il segnale piu' prezioso di tutta la catena.`

// ---- schema del rapporto di REVISIONE DI LINGUA (6o livello) ----
const LINGUA_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['frasi_toccate', 'frasi_totali'],
  properties: {
    frasi_toccate: { type: 'number', description: 'Quante frasi hai corretto' },
    frasi_totali: { type: 'number', description: 'Quante frasi ha il documento (stima)' },
    variazione_percentuale: { type: 'string', description: 'Delta di lunghezza. Deve stare entro +-3%' },
    calchi_piu_frequenti: {
      type: 'array', items: { type: 'string' },
      description: 'I tre calchi o difetti di lingua piu ricorrenti che hai trovato. Servono a migliorare i livelli a monte.',
    },
    passaggi_ancora_oscuri: {
      type: 'array', items: { type: 'string' },
      description: 'Punti che non sei riuscito a rendere in italiano vero perche il pensiero sotto era confuso. E il segnale piu prezioso: vanno riportati a Carlos.',
    },
    capitolo_finale: { type: 'string', description: 'Stato del capitolo «Cosa fare adesso»: PRESENTE_E_LAVORATO / PRESENTE_DEBOLE / ASSENTE' },
    metafore_inserite: {
      type: 'array', items: { type: 'string' },
      description: 'Le metafore di servizio che hai aggiunto, una riga ciascuna: capitolo + immagine usata. Da 0 a 8. Ognuna deve essere rimovibile senza perdere informazione.',
    },
  },
}

// SESTO LIVELLO: la revisione di lingua. NON riscrive: passa a setaccio e corregge le frasi difettose.
const linguaPrompt = (slug, r) => `Sei il revisore di SESTO e ULTIMO livello del panel Mobilitas — **il Revisore di Lingua**. Quello che produci e' la versione che si consegna.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md e il suo reference ${r.skill}/references/italiano-vero.md (il repertorio dei calchi, dei nessi e delle collocazioni: e' il metodo, leggilo prima di toccare una riga).

Prima di te sono girati quindici revisori e un riscrittore. Il contenuto e' corretto, sicuro, conforme, fedele al metodo, didatticamente ordinato, asciutto e semplificato. **Non tocchi niente di tutto questo.**

> **Il documento e' giusto, e' semplice, ed e' scritto in un italiano che non e' italiano.**

E' il difetto che sopravvive a tutta la catena, perche' nessun revisore prima di te ha la lingua come mandato. Una frase corta e semplice puo' essere un calco perfetto dall'inglese.

## Prima di iniziare: leggi il registro
Apri ${REGISTRO_LINGUA}. Le **Correzioni attive** e le **Osservazioni** dicono quali calchi ricorrono in questo studio: sai gia' cosa cercare, invece di scoprirlo da capo. Costa un minuto e rende la passata molto piu' rapida.

## I tre difetti che cerchi, e nient'altro
1. **Il calco.** La frase costruita con la sintassi di un'altra lingua e riempita di parole italiane. La **prova del traduttore inverso** li smaschera tutti: traduci la frase in inglese parola per parola; se l'inglese che ne esce e' perfetto, la frase italiana e' un calco.
2. **La sintassi che non segue la logica.** Connettivo che promette un rapporto e la frase ne fa un altro; nesso assente fra due frasi accostate; soggetto astratto che agisce ("la valutazione permette di identificare"); **pronome senza padrone** (questo / cio' / tale / il che appoggiati a una frase intera invece che a un sostantivo — e' la causa numero uno dei passaggi incomprensibili); ordine rovesciato (il nuovo prima del noto).
3. **La collocazione sbagliata.** Le parole italiane vanno a coppie fisse: un dolore si irradia, non viaggia; un farmaco agisce, non lavora.

## Il metodo: si passa a setaccio, non si riscrive
1. Leggi tutto il documento una volta senza toccare niente.
2. Passa **frase per frase**. Su ognuna, tre domande: e' un calco? il nesso logico regge? le parole stanno insieme? Se tutte e tre danno esito buono, **lasci la frase esattamente com'e'**.
3. Correggi solo quello che ha risposto male, con la correzione **minima**.
4. Rileggi ad alta voce ogni capitolo corretto.
5. Segna i punti che restano ASTRATTI anche dopo la correzione, e non intervenire subito. Alla fine torna sui punti segnati e scegli le 6-8 che meritano una metafora di servizio: sceglierle alla fine, e non mentre correggi, e' cio' che evita di riempirne il documento.
6. Se hai toccato piu' del 40% delle frasi, stai riscrivendo invece di correggere: fermati e dillo nel rapporto.

## L'INVIOLABILE
Restano identici: ogni numero, percentuale e misura; ogni PMID, autore, anno e titolo; **ogni etichetta di solidita' — non alzarne nessuna, mai**; ogni bandiera rossa, criterio di invio e limite di campo; **ogni frase-ponte** che dichiara il limite di una fonte; ogni nome anatomico; l'architettura (capitoli, ordine, titoli, aperture "In una riga", chiusure "Le tre cose da ricordare", i quattro tipi di box, le tabelle); le tre voci e le frasi-firma.

**Rischio che e' tuo e di nessun altro:** rendere una frase piu' scorrevole la rende piu' assertiva. "Puo' contribuire" che diventa "contribuisce" e' una violazione bloccante come alzare un'etichetta. Quando raddrizzi una frase cauta, ricontrolla che sia rimasta cauta.

## Il quarto compito: le metafore di servizio
E' la tua UNICA licenza di aggiungere qualcosa. Alcuni concetti restano difficili anche dopo la semplificazione, perche' sono ASTRATTI e il lettore non ha nulla nella sua esperienza a cui agganciarli. Li' una metafora della vita quotidiana fa quello che nessuna riformulazione puo' fare.

**La regola che la rende sicura, e che ti evita di far fallire il collaudo:** *se togliendo la metafora si perde un'informazione, non era una metafora — era contenuto nuovo, e va tolta.* Una metafora ripete, non estende.

Registri da cui pescare: **la macchina** (motore, freni, spia accesa, serbatoio), **la casa** (interruttore, rubinetto, salvavita, termostato, porta), **il lavoro** (scrivania piena, scadenza, turno coperto), **la cucina** (pentola che bolle, fuoco basso), **il denaro** (conto, debito, anticipo). Il criterio: **il lettore deve averla vissuta fisicamente**.

Le regole: **6-8 in tutto il documento**, massimo **una per capitolo**, **max 20 parole**, dentro la frase e mai in grassetto o isolata su una riga, **dopo** l'affermazione e mai prima, mai spiegata ("cioe' come quando..."), mai due immagini nello stesso passaggio. **MAI** dentro un box "Quanto e solido", su una bandiera rossa, su un criterio di invio o su un limite legale: li' il testo resta letterale, perche' un'immagine ammorbidisce un avvertimento. **Mai metafore militari.**

Non confonderle con le **metafore d'ancoraggio** del capitolo «Cosa si rompe» (una per meccanismo, in grassetto, isolate su una riga): quelle le sceglie l'autore, sono il cuore mnemonico del documento, e **non le tocchi ne' ne aggiungi**.

Gli esempi lavorati e le metafore da non usare stanno in ${r.skill}/references/italiano-vero.md, Parte 5.

## Il capitolo «Cosa fare adesso»
E' il capitolo che deve MUOVERE qualcuno, non informarlo: e' quello dove la lingua conta di piu'. Se c'e', lavoralo per primo — un finale motivante scritto in italiano tradotto suona come un opuscolo, e deve suonare come una persona che parla a un collega. **Se manca, NON scriverlo tu**: segnalalo nel rapporto (campo "capitolo_finale": ASSENTE). Aggiungere un capitolo qui farebbe fallire il collaudo di conservazione.

## Documento su cui lavorare
Leggi ${F(slug).v6} (la Bibbia) e ${F(slug).m6} (la Mappa). Se non esistono, fermati e dillo.

## Output — sono i deliverable
- ${F(slug).v7} → la Bibbia FINALE
- ${F(slug).m7} → la Mappa FINALE

Riporta **tutti** i capitoli e **tutte** le appendici, completi: i file nuovi sono autosufficienti, nessun rimando al testo precedente. Le parti che non hanno difetti di lingua le ricopi identiche.

Variazione di lunghezza ammessa: **da -3% a +5%**. Il margine in piu' esiste solo per le metafore di servizio. Oltre, non hai fatto una revisione di lingua: hai riscritto.

## Prima di chiudere: deposita il segnale
Aggiungi in fondo a ${REGISTRO_LINGUA}, sezione «Osservazioni», un blocco intitolato con la condizione "${slug}" che contenga: i **tre calchi piu' frequenti** che hai trovato (servono a correggere l'autore a monte, non a valle) e i **passaggi rimasti oscuri** anche dopo il tuo lavoro. Questi ultimi vanno anche nella sezione «Passaggi che restano oscuri», con condizione, capitolo per nome e di cosa si tratta.
**Solo append: aggiungi in fondo, non riscrivere il file.** Piu' Bibbie possono girare insieme, e riscrivendolo cancelleresti il blocco di un'altra. Non promuovere niente in «Correzioni attive»: quella e' una decisione di Carlos.

Restituisci l'oggetto strutturato richiesto. In "passaggi_ancora_oscuri" metti gli stessi punti: un passaggio che non si lascia rendere in italiano vero quasi sempre nasconde un pensiero confuso, non una parola sbagliata.`

const SCRIPT_COLLAUDO = AUTORE + '/scripts/verifica_conservazione.py'

const collaudoPrompt = (slug, g) => `Sei il **COLLAUDO DI CONSERVAZIONE** della Bibbia "${slug}" — l'ultimo cancello prima della consegna.

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${g.skill}/SKILL.md.

Prima di te sono girati quindici revisori su quattro livelli. Poi il 5o livello ha **riscritto da capo ogni singola frase** del documento, e il 6o ne ha raddrizzato la lingua. E' l'unico tratto della catena in cui tutto il testo cambia. Tu verifichi che, cambiando tutte le parole, non sia cambiata nessuna cosa detta.

Confronti la **v5** con la **versione FINALE**, non le due riscritture fra loro: la v5 e' l'ultima versione con il contenuto approvato, e cosi' collaudi i due passaggi insieme.

> **La versione finale dice esattamente le stesse cose della v5, o per strada si e' perso, indebolito o gonfiato qualcosa?**

## LA REGOLA CHE TI DEFINISCE
**Non giudichi la qualita'.** Quella ha gia' avuto quindici risposte. Giudichi solo la CONSERVAZIONE.
Se un contenuto ti sembra debole ma stava identico nella v5, **non e' un tuo rilievo: taci**. Un collaudatore che trova cose nuove riapre decisioni chiuse e fa ripartire un ciclo finito: e' rotto, non severo.
Uniche eccezioni, perche' nate qui: promesse di esito, materiale operativo (dosi da somministrare, sequenze, minuti) e affermazioni rafforzate.

## PASSO 1 — fai girare il codice, prima di leggere
**Due misurazioni separate, una per passaggio.** Misurare le due riscritture in blocco le lascia compensare a vicenda: se la prima perde e la seconda aggiunge, i conti tornano e la perdita non si vede.

Esegui con Bash, in quest'ordine:

1. La riscrittura di chiarezza — ogni frase cambia, nessuna identita' attesa:
\`python3 ${SCRIPT_COLLAUDO} ${F(slug).v5} ${F(slug).v6} --etichetta chiarezza --delta-min -5 --delta-max 10 --json ${OUT}/${slug}/collaudo-chiarezza.json\`

2. La revisione di lingua — doveva CORREGGERE, non riscrivere:
\`python3 ${SCRIPT_COLLAUDO} ${F(slug).v6} ${F(slug).v7} --etichetta lingua --delta-min -3 --delta-max 5 --min-identita 60 --json ${OUT}/${slug}/collaudo-lingua.json\`

La soglia di identita' del secondo comando e' il controllo che sostituisce l'autodichiarazione del sesto livello: se meno del 60% delle frasi e' rimasto identico, ha riscritto invece di correggere, e lo dice il conteggio invece dell'agente stesso. E' una violazione bloccante come le altre.

**Per ogni violazione che riporti, dichiara in quale dei due passaggi e' nata** (campo "passaggio"): serve a riparare nel punto giusto invece che a caso.
**Quello che gli script trovano e' accertato: riportalo in "violazioni_bloccanti", non riverificarlo.** Metti la somma dei bloccanti dei due comandi in "bloccanti_dal_codice".

Coprono gia': etichette perse o alzate, PMID spariti o inventati, numeri persi o comparsi, titoli e struttura, aperture "In una riga" e chiusure "Le tre cose da ricordare", tabelle fuori specifica, delta di lunghezza, identita' delle frasi, glossario, script, materiale operativo e promesse.

## PASSO 2 — il tuo lavoro comincia dove il codice si ferma
Leggi ${F(slug).v5} e ${F(slug).v7} e cerca cio' che nessun conteggio vede:
1. **Etichetta riancorata** — la stessa etichetta ora qualifica un claim diverso. I conteggi tornano, il senso no.
2. **Informazione persa per assorbimento** — due frasi che dicevano due cose diventano una che ne dice una e sembra completa. Procedi per inventario, capitolo per capitolo.
3. **Qualificazione caduta** — "nella maggior parte dei casi", "se il paziente non ha X", l'urgenza o il destinatario di una bandiera rossa, il sottotipo su cui si poteva poco.
4. **Verbo irrigidito** — "puo' contribuire" -> "contribuisce". Frasi corte sono assertive per costruzione: e' l'effetto collaterale strutturale della semplificazione.
5. **Numero riattribuito** — il valore c'e' ancora ma appartiene a un altro studio.

Controlla anche ${F(slug).m5} contro ${F(slug).m7} con lo stesso criterio.

## Output
Ogni violazione porta una **riparazione chirurgica**: cosa rimettere e dove, non una riscrittura. Chi ripara e' il riscrittore, e deve poter agire senza toccare il resto.
Localizza i capitoli **per nome**, mai per numero.
"CONSEGNABILE" solo con ZERO bloccanti, del codice e tuoi. Non esiste il consegnabile con riserva.
Se non trovi niente, dillo: e' l'esito atteso di una riscrittura fatta bene.`

const riparaPrompt = (slug, r, viol, giro) => `Sei chi ha prodotto la versione FINALE della Bibbia "${slug}" (skill ${r.key}). Il collaudo ha trovato ${viol.length} violazioni di conservazione. Questo e' il giro di riparazione ${giro}.

## Cosa NON devi fare
**Non riscrivere il documento. Non rileggerlo per migliorarlo. Non toccare una sola frase che non sia nell'elenco qui sotto.**
La versione finale e' gia' buona: e' semplice, si legge, suona italiana, ed e' il risultato del lavoro di due livelli. Ha solo perso per strada delle cose che dovevano restare. Le rimetti, e basta.
Ogni modifica fuori dall'elenco riapre il collaudo e allunga il ciclo.

## Le violazioni da riparare
${viol.map((v, i) => `${i + 1}. [${v.tipo}] Capitolo «${v.capitolo}»${v.passaggio ? ` — nata nel passaggio ${v.passaggio}` : ''}
   v5 diceva: ${v.testo_v5 || '(vedi rapporto)'}
   v6 dice:   ${v.testo_v6 || 'assente'}
   RIPARAZIONE: ${v.riparazione}`).join('\n')}

## Come si ripara
Riapri ${F(slug).v7} (e ${F(slug).m7} se la violazione e' li') e applica **solo** queste riparazioni.
Rimetti l'informazione **con il lessico e la sintassi della versione finale**, non copiando la frase della v5: il documento deve restare semplice e suonare italiano. Frasi da 18-20 parole, una subordinata per frase, prima la conclusione, nessun calco dall'inglese.
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

const PROMOZIONI_FALLITE = []

async function promote(bibIn, mappaIn, bibOut, mappaOut, motivo) {
  log(`  [resilienza] ${motivo}: promuovo ${bibIn.split('/').pop()} -> ${bibOut.split('/').pop()} senza modifiche`)
  const r = await robustAgent(
    promotePrompt(bibIn, mappaIn, bibOut, mappaOut),
    { label: `promuovi:${bibOut.split('/').pop()}`, phase: 'Sintesi', agentType: 'general-purpose' },
    2
  )
  // BUG STORICO (notte 18-19/08/2026): il limite di sessione ha fatto fallire promozioni e sintesi
  // di sette Bibbie, e il workflow ha comunque restituito "completata (v7=v6, lingua promossa)".
  // Sul disco non c'era nessuna v7. Da qui in poi la promozione fallita e' un fatto registrato,
  // e l'esito finale si decide guardando il disco, non i report degli agenti.
  if (!r) {
    const msg = `PROMOZIONE NON CONFERMATA verso ${bibOut.split('/').pop()} (${motivo}): il file potrebbe NON esistere`
    log(`  [resilienza] ATTENZIONE: ${msg}`)
    PROMOZIONI_FALLITE.push(msg)
  }
  return r
}

// ============================ ORCHESTRAZIONE ============================

// ---- DUE MODALITA D'USO ----
// A) Bibbie SPECIFICHE: args = ["reflusso"] oppure ["reflusso","cervicalgia", ...]
// B) TUTTE: args = "tutte" (o "all" / "*") -> carica gli slug dal JSON
// Se args arriva come stringa JSON ('["reflusso-gastrico"]' invece dell'array) lo slug
// diventerebbe il letterale con parentesi e virgolette, e la cartella si chiamerebbe cosi.
const parseArgs = (a) => {
  if (Array.isArray(a)) return a
  if (typeof a === 'string') {
    const s = a.trim()
    if (s.startsWith('[')) { try { const p = JSON.parse(s); if (Array.isArray(p)) return p } catch (e) { /* non e JSON: e uno slug singolo */ } }
    return s ? [s] : []
  }
  return a ? [a] : []
}
// ---- RIPRESA: stato precalcolato dal chiamante ----
// BUG STORICO (18-19/08/2026): il limite di sessione ha ucciso sette catene a meta'; rilanciarle
// da zero avrebbe buttato 15,6 milioni di token di lavoro gia' su disco. Da qui in poi args
// accetta anche { slugs: [...], stati: { slug: ["v1-bibbia.md", ...] } }: ogni stadio il cui
// file di uscita ESISTE GIA' viene saltato, e la catena riprende dal primo anello mancante.
// Lo stato si ricava con un `ls`, cioe' senza spendere un solo agente.
const argObj = (args && typeof args === 'object' && !Array.isArray(args)) ? args : null
const STATI = (argObj && argObj.stati) || {}
const fatto = (slug, file) => ((STATI[slug] || []).includes(file))
const raw = parseArgs(argObj ? argObj.slugs : args).map((s) => String(s).trim()).filter(Boolean)
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
const sixthKeys = ((disc && disc.sesto_livello) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k) && !thirdKeys.includes(k) && !fourthKeys.includes(k) && !fifthKeys.includes(k))
const gateKeys = ((disc && disc.collaudo) || []).filter((k) => all.includes(k) && k !== autore && !firstKeys.includes(k) && !secondKeys.includes(k) && !thirdKeys.includes(k) && !fourthKeys.includes(k) && !fifthKeys.includes(k) && !sixthKeys.includes(k))

const mk = (k) => ({ key: k, skill: SK + '/direttore-osteopatico-' + k })
const REVIEWERS = firstKeys.map(mk)  // 1o livello
const SECOND = secondKeys.map(mk)    // 2o livello
const THIRD = thirdKeys.map(mk)      // 3o livello (logica dell'apprendimento)
const FOURTH = fourthKeys.map(mk)    // 4o livello (editor di asciugatura)
const FIFTH = fifthKeys.map(mk)      // 5o livello (riscrittura in chiaro)
const SIXTH = sixthKeys.map(mk)      // 6o livello (revisione di lingua italiana)
const GATE = gateKeys.map(mk)        // CANCELLO: collaudo di conservazione v5 -> finale

// Segnala skill-revisore presenti ma non assegnate a nessun livello: niente cali silenziosi.
const assegnate = new Set([autore, ...firstKeys, ...secondKeys, ...thirdKeys, ...fourthKeys, ...fifthKeys, ...sixthKeys, ...gateKeys])
const nonAssegnate = all.filter((k) => !assegnate.has(k))
if (nonAssegnate.length) log(`ATTENZIONE: skill presenti ma non assegnate a nessun livello nel manifesto (ignorate): ${nonAssegnate.join(', ')}`)

if (!REVIEWERS.length && !SECOND.length && !THIRD.length && !FOURTH.length && !FIFTH.length && !SIXTH.length) {
  log('ATTENZIONE: nessun revisore dichiarato nel manifesto. Interrompo.')
  return { errore: 'nessun revisore nei livelli del manifesto ' + MANIFESTO }
}
log(`Autore: ${autore} | 1o (${REVIEWERS.length}): ${REVIEWERS.map((r) => r.key).join(', ') || '—'} | 2o (${SECOND.length}): ${SECOND.map((r) => r.key).join(', ') || '—'} | 3o (${THIRD.length}): ${THIRD.map((r) => r.key).join(', ') || '—'} | 4o (${FOURTH.length}): ${FOURTH.map((r) => r.key).join(', ') || '—'} | 5o (${FIFTH.length}): ${FIFTH.map((r) => r.key).join(', ') || '—'} | 6o (${SIXTH.length}): ${SIXTH.map((r) => r.key).join(', ') || '—'} | collaudo: ${GATE.map((r) => r.key).join(', ') || '— NESSUNO (la finale andrebbe in consegna senza cancello)'}`)
if (!SIXTH.length) log('ATTENZIONE: nessuna revisione di lingua dichiarata nel manifesto. Il documento uscira semplificato ma non ripulito dai calchi.')
if (!GATE.length) log('ATTENZIONE: nessun collaudo dichiarato nel manifesto. Le riscritture del 5o e 6o livello non verranno verificate da nessuno.')

const results = await pipeline(
  slugs,

  // --- STAGE 1: DRAFT (v1) ---
  async (slug) => {
    if (fatto(slug, 'v1-bibbia.md')) { log(`[ripresa] ${slug}: v1 gia' su disco, salto il draft`); return slug }
    const r = await robustAgent(draftPrompt(slug), { label: `draft:${slug}`, phase: 'Draft', agentType: 'general-purpose' })
    // Il draft e l'unico stadio senza fallback: senza bozza non c'e nulla da revisionare.
    // Il throw qui, dentro pipeline(), scarta SOLO questo slug (gli altri proseguono).
    if (!r) { log(`ATTENZIONE: draft non riuscito per ${slug} dopo ${RETRIES} tentativi — salto SOLO questo slug`); throw new Error(`draft fallito per ${slug}`) }
    log(`Draft pronto: ${slug}`)
    return slug
  },

  // --- STAGE 2: REVISIONE 1o LIVELLO (in parallelo) ---
  async (slug) => {
    if (fatto(slug, 'v2-intermedia.md')) { log(`[ripresa] ${slug}: v2 gia' su disco, salto il 1o livello`); return slug }
    const mancanti = REVIEWERS.filter((rv) => !fatto(slug, `feedback-${rv.key}.md`))
    if (mancanti.length < REVIEWERS.length) log(`[ripresa] ${slug}: ${REVIEWERS.length - mancanti.length}/${REVIEWERS.length} feedback di 1o livello gia' presenti`)
    if (!mancanti.length) return slug
    const fbs = await parallel(
      mancanti.map((rv) => () =>
        agent(reviewPrompt(slug, rv), { label: `rev1:${rv.key}:${slug}`, phase: 'Revisione', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })
      )
    )
    const ok = fbs.filter(Boolean).length
    log(`Revisione 1o livello ${slug}: ${ok}/${mancanti.length}${ok === 0 ? ' — nessun feedback: la sintesi promuovera la v1' : ''}`)
    return slug
  },

  // --- STAGE 3: SINTESI INTERMEDIA (v2) ---
  async (slug) => {
    if (fatto(slug, 'v2-intermedia.md')) { log(`[ripresa] ${slug}: v2 gia' su disco, salto la sintesi`); return slug }
    const r = await robustAgent(synthPrompt(slug), { label: `sintesi-v2:${slug}`, phase: 'Sintesi intermedia', agentType: 'general-purpose' })
    if (!r) await promote(`${OUT}/${slug}/v1-bibbia.md`, `${OUT}/${slug}/v1-mappa.md`, `${OUT}/${slug}/v2-intermedia.md`, `${OUT}/${slug}/mappa-v2.md`, `sintesi v2 non riuscita per ${slug}`)
    else log(`v2 pronta: ${slug}`)
    return slug
  },

  // --- STAGE 4: REVISIONE 2o LIVELLO -> SINTESI v3 ---
  async (slug) => {
    if (fatto(slug, 'v3-intermedia.md')) { log(`[ripresa] ${slug}: v3 gia' su disco, salto il 2o livello`); return slug }
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
    if (fatto(slug, 'v4-intermedia.md')) { log(`[ripresa] ${slug}: v4 gia' su disco, salto il 3o livello`); return slug }
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
    if (fatto(slug, 'v5-intermedia.md')) { log(`[ripresa] ${slug}: v5 gia' su disco, salto l'editor`); return slug }
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

  // --- STAGE 7: QUINTO LIVELLO — RISCRITTURA INTEGRALE -> v6 ---
  // Non e' una revisione seguita da una sintesi: il riscrittore PRODUCE il testo.
  async (slug) => {
    const f = F(slug)
    if (fatto(slug, 'v6-chiarezza.md')) { log(`[ripresa] ${slug}: v6 gia' su disco, salto la riscrittura di chiarezza`); return { slug, esito: 'ripresa: v6 gia presente' } }
    if (!FIFTH.length) {
      await promote(f.v5, f.m5, f.v6, f.m6, `nessun 5o livello per ${slug}`)
      log(`v6 (= v5, nessuna riscrittura di chiarezza): ${slug}`)
      return { slug, esito: 'completata (senza riscrittura di chiarezza)' }
    }
    // Un solo riscrittore per volta: due riscritture concorrenti sullo stesso file si sovrascriverebbero.
    // Se il manifesto ne dichiara piu d'uno, usa il primo e segnala gli altri.
    if (FIFTH.length > 1) log(`ATTENZIONE: piu di un riscrittore di 5o livello nel manifesto. Uso "${FIFTH[0].key}", ignoro: ${FIFTH.slice(1).map((r) => r.key).join(', ')}`)
    const rw = FIFTH[0]
    const rep = await robustAgent(rewritePrompt(slug, rw), { label: `rev5:${rw.key}:${slug}`, phase: 'Riscrittura finale', schema: RISCRITTURA_SCHEMA, agentType: 'general-purpose' })
    if (!rep) {
      await promote(f.v5, f.m5, f.v6, f.m6, `riscrittura di chiarezza non riuscita per ${slug}`)
      return { slug, esito: 'completata (v6=v5, riscrittura promossa dopo i retry)' }
    }
    if (rep.informazioni_perse && rep.informazioni_perse.length) {
      log(`ATTENZIONE ${slug}: la riscrittura dichiara ${rep.informazioni_perse.length} informazioni perse — vanno rimesse a mano`)
    }
    if (rep.passaggi_incomprensibili && rep.passaggi_incomprensibili.length) {
      log(`Segnale per Carlos (${slug}): ${rep.passaggi_incomprensibili.length} passaggi non semplificabili — probabile confusione di contenuto, non di forma`)
    }
    log(`v6 riscritta: ${slug} — ${rep.parole_prima} → ${rep.parole_dopo} parole (${rep.variazione_percentuale || 'n/d'}). Ora la lingua.`)
    return { slug, esito: 'completata', riscrittura: rep }
  },

  // --- STAGE 8: SESTO LIVELLO — REVISIONE DI LINGUA -> v7 FINALE ---
  // Il difetto che sopravviveva a tutta la catena: un documento giusto, semplice, e scritto
  // in un italiano tradotto. Nessun revisore precedente aveva la lingua come mandato.
  // Non e' una riscrittura: si passa frase per frase e si corregge solo cio' che ha un difetto.
  async (prev, slug) => {
    const base = prev && prev.slug ? prev : { slug, esito: 'sconosciuto' }
    const f = F(slug)

    if (fatto(slug, 'v7-finale.md')) { log(`[ripresa] ${slug}: v7 gia' su disco, salto la revisione di lingua`); return { ...base, esito: 'ripresa: v7 gia presente' } }
    if (!SIXTH.length) {
      await promote(f.v6, f.m6, f.v7, f.m7, `nessun 6o livello per ${slug}`)
      log(`FINALE (v7 = v6, nessuna revisione di lingua): ${slug}`)
      return { ...base, esito: 'completata (senza revisione di lingua)' }
    }
    if (SIXTH.length > 1) log(`ATTENZIONE: piu di un revisore di lingua nel manifesto. Uso "${SIXTH[0].key}", ignoro: ${SIXTH.slice(1).map((r) => r.key).join(', ')}`)
    const lr = SIXTH[0]
    const rep = await robustAgent(linguaPrompt(slug, lr), { label: `rev6:${lr.key}:${slug}`, phase: 'Revisione di lingua', schema: LINGUA_SCHEMA, agentType: 'general-purpose' })
    if (!rep) {
      await promote(f.v6, f.m6, f.v7, f.m7, `revisione di lingua non riuscita per ${slug}`)
      return { ...base, esito: 'completata (v7=v6, lingua promossa dopo i retry)' }
    }

    const tot = rep.frasi_totali || 0
    const quota = tot ? Math.round((100 * (rep.frasi_toccate || 0)) / tot) : null
    if (quota !== null && quota > 40) {
      log(`ATTENZIONE ${slug}: la revisione di lingua ha toccato il ${quota}% delle frasi. Oltre il 40% non e una revisione: o il 5o livello ha lavorato male, o il 6o ha riscritto.`)
    }
    if (rep.capitolo_finale === 'ASSENTE') {
      log(`ATTENZIONE ${slug}: manca il capitolo «Cosa fare adesso». Va aggiunto a monte (autore o 2o livello): il 6o livello non puo aggiungerlo senza far fallire il collaudo.`)
    }
    if (rep.passaggi_ancora_oscuri && rep.passaggi_ancora_oscuri.length) {
      log(`Segnale per Carlos (${slug}): ${rep.passaggi_ancora_oscuri.length} passaggi restano oscuri anche dopo la lingua — il pensiero sotto e confuso, non la frase`)
    }
    if (rep.calchi_piu_frequenti && rep.calchi_piu_frequenti.length) {
      log(`  ${slug} — calchi ricorrenti da correggere a monte: ${rep.calchi_piu_frequenti.join(' · ')}`)
    }
    const nMet = (rep.metafore_inserite || []).length
    if (nMet > 8) log(`ATTENZIONE ${slug}: ${nMet} metafore di servizio inserite, il tetto e 8. Oltre, distraggono invece di semplificare.`)
    log(`v7 FINALE pronta: ${slug} — ${rep.frasi_toccate}/${tot} frasi toccate, ${nMet} metafore di servizio (${rep.variazione_percentuale || 'n/d'}). Ora il collaudo.`)
    return { ...base, esito: 'completata', lingua: rep }
  },

  // --- STAGE 9: COLLAUDO DI CONSERVAZIONE -> RIPARAZIONE MIRATA -> CONSEGNA ---
  // Il 5o livello riscrive OGNI frase del documento e il 6o ne ritocca molte: e' l'unico
  // tratto della catena in cui tutto il testo cambia, ed era l'unico mai verificato.
  // Non e' un settimo revisore: non giudica la qualita' (chiusa a monte), verifica la
  // CONSERVAZIONE — che cambiando tutte le parole non sia cambiata nessuna cosa detta.
  // Confronta v5 contro la FINALE, cosi' collauda le due riscritture insieme.
  async (prev, slug) => {
    const base = prev && prev.slug ? prev : { slug, esito: 'sconosciuto' }
    const f = F(slug)

    if (!GATE.length) {
      log(`ATTENZIONE ${slug}: nessun collaudo nel manifesto — la finale va in consegna senza cancello.`)
      return { ...base, collaudo: 'assente' }
    }
    // Se non ha riscritto nessuno dei due livelli (finale = v5 promossa) non c'e' niente da conservare.
    if (!base.riscrittura && !base.lingua) {
      log(`Collaudo non necessario per ${slug}: la finale e' la v5 promossa senza riscritture.`)
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
        log(`ATTENZIONE ${slug}: il collaudo non ha risposto dopo i retry. La finale resta, ma NON e' stata verificata.`)
        return { ...base, collaudo: 'non eseguito' }
      }

      const viol = (rap.violazioni_bloccanti || []).filter(Boolean)
      const dalCodice = rap.bloccanti_dal_codice || 0

      if (rap.esito === 'CONSEGNABILE' && !viol.length) {
        log(`COLLAUDO SUPERATO ${slug}${giro > 1 ? ` (dopo ${giro - 1} riparazion${giro === 2 ? 'e' : 'i'})` : ''}: le riscritture hanno conservato tutto.`)
        return { ...base, esito: 'consegnabile', collaudo: 'superato', riparazioni: giro - 1, conservato: rap.conservato }
      }

      // Perdite cosi' diffuse che una riparazione chirurgica non basta.
      // Vince la gerarchia dichiarata dal metodo: l'ACCURATEZZA batte la LEGGIBILITA'.
      // Meglio consegnare la v5 (corretta, meno scorrevole) che una finale che ha perso informazione.
      if (rap.esito === 'DA_RIFARE') {
        log(`COLLAUDO: ${slug} DA RIFARE (${viol.length} perdite diffuse). Ripristino la v5 come versione finale: l'accuratezza batte la leggibilita.`)
        await promote(f.v5, f.m5, f.v7, f.m7, `riscritture di ${slug} non conservative`)
        return { ...base, esito: 'consegnata la v5', collaudo: 'fallito — riscritture scartate', violazioni: viol.length }
      }

      if (giro > MAX_RIPARAZIONI) {
        log(`ATTENZIONE ${slug}: ${viol.length} violazioni ancora aperte dopo ${MAX_RIPARAZIONI} riparazioni. NON CONSEGNABILE senza intervento umano.`)
        return { ...base, esito: 'NON CONSEGNABILE', collaudo: 'non superato', violazioni: viol, bloccanti_dal_codice: dalCodice }
      }

      log(`Collaudo ${slug}: ${viol.length} violazioni (${dalCodice} dal codice). Riparazione mirata, giro ${giro}.`)
      const fix = await robustAgent(riparaPrompt(slug, SIXTH[0] || FIFTH[0] || g, viol, giro), {
        label: `ripara:${slug}#giro${giro}`, phase: 'Collaudo', schema: RISCRITTURA_SCHEMA, agentType: 'general-purpose',
      })
      if (!fix) {
        log(`ATTENZIONE ${slug}: la riparazione non ha risposto. Consegno la v5, che e' l'ultima versione verificata.`)
        await promote(f.v5, f.m5, f.v7, f.m7, `riparazione di ${slug} non riuscita`)
        return { ...base, esito: 'consegnata la v5', collaudo: 'riparazione fallita', violazioni: viol.length }
      }
      if (fix.informazioni_perse && fix.informazioni_perse.length) {
        log(`  ${slug}: la riparazione dichiara ${fix.informazioni_perse.length} voci non rimesse — il collaudo del giro dopo le ritrovera.`)
      }
    }

    return { ...base, esito: 'NON CONSEGNABILE', collaudo: 'non superato' }
  }
)

// --- VERIFICA FINALE SUL DISCO ---
// L'unico giudice di "fatto" e' il file system. Gli agenti riferiscono, non provano: nella notte
// del 18/08 sette Bibbie si sono dichiarate completate ferme alla v2.
const esiti = results.filter(Boolean)
const VERIFICA_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['stato'],
  properties: {
    stato: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false, required: ['slug', 'ultima_versione', 'ha_v7', 'ha_mappa_finale'],
        properties: {
          slug: { type: 'string' },
          ultima_versione: { type: 'string', description: 'Il file di versione piu avanzato presente (es. v3-intermedia.md)' },
          ha_v7: { type: 'boolean' },
          ha_mappa_finale: { type: 'boolean' },
        },
      },
    },
  },
}
const ver = await robustAgent(
  `Per ognuno di questi slug — ${slugs.join(', ')} — esegui: ls -1 ${OUT}/<slug>
Riporta il file di versione piu avanzato presente, seguendo l'ordine v1-bibbia.md, v2-intermedia.md, v3-intermedia.md, v4-intermedia.md, v5-intermedia.md, v6-chiarezza.md, v7-finale.md, e di' se esistono v7-finale.md e mappa-finale.md.
Non inventare: riporta solo cio' che ls mostra.`,
  { label: 'verifica-finale-sul-disco', phase: 'Collaudo', schema: VERIFICA_SCHEMA, agentType: 'general-purpose' }, 2
)

if (!ver) {
  return { esiti, avviso: 'NON VERIFICATO sul disco: gli esiti qui sopra sono dichiarazioni degli agenti, non fatti. Controlla a mano.', promozioni_fallite: PROMOZIONI_FALLITE }
}
const perSlug = new Map((ver.stato || []).map((s) => [s.slug, s]))
const consegnabili = [], incomplete = []
for (const e of esiti) {
  const s = perSlug.get(e.slug)
  if (s && s.ha_v7 && s.ha_mappa_finale) consegnabili.push({ ...e, verificata: true })
  else incomplete.push({ slug: e.slug, dichiarato: e.esito, realta: s ? `ferma a ${s.ultima_versione}` : 'cartella non leggibile' })
}
if (incomplete.length) log(`ATTENZIONE: ${incomplete.length} Bibbie dichiarate completate NON hanno la v7 sul disco: ${incomplete.map((i) => i.slug).join(', ')}`)
return { consegnabili, incomplete, promozioni_fallite: PROMOZIONI_FALLITE }

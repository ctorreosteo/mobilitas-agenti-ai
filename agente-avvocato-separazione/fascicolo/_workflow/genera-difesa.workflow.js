export const meta = {
  name: 'genera-difesa-famiglia',
  description: 'Per ogni atto: redazione v1, panel avversariale di 1o livello in parallelo (avvocato della madre, giudice, PM, curatore del minore, CTU, penalista, patrimoniale, prove, decadenze, negoziatore, cliente, deontologia), 2o livello sulle fonti (prima verifica, poi ampliamento), 3o coerenza, 4o asciugatura, 5o riscrittura in chiaro, 6o revisione di lingua, poi COLLAUDO deterministico — conservazione lungo la catena PIU cancello sulla versione finale — con riparazione mirata. Nessun atto arriva alla consegna senza cancello. Resiliente: retry sugli agenti critici e promozione della versione precedente se una sintesi fallisce',
  whenToUse: 'Produce gli atti difensivi del fascicolo, uno o piu alla volta, con la catena completa di revisione',
  phases: [
    { title: 'Scoperta', detail: 'legge il manifesto dei livelli e le skill realmente presenti' },
    { title: 'Ricerca', detail: 'ricercatore-giurisprudenza verifica e registra le fonti che serviranno' },
    { title: 'Draft', detail: 'cancello sui fatti, poi la skill strategia redige la v1 dell atto' },
    { title: 'Revisione', detail: 'le dodici lenti di 1o livello, in parallelo' },
    { title: 'Sintesi v2', detail: 'l autore pesa i feedback e riscrive' },
    { title: 'Fonti', detail: '2o livello: prima verifica le citazioni, poi allarga la base' },
    { title: 'Sintesi v3', detail: 'applica i rilievi sulle fonti' },
    { title: 'Coerenza', detail: '3o livello: contraddizioni interne, col fascicolo, fra civile e penale' },
    { title: 'Sintesi v4', detail: 'armonizza' },
    { title: 'Asciugatura', detail: '4o livello: mappa di taglio' },
    { title: 'Sintesi v5', detail: 'applica i tagli. E la versione con il contenuto approvato' },
    { title: 'Riscrittura', detail: '5o livello: riscrive tutto in italiano leggibile -> v6' },
    { title: 'Lingua', detail: '6o livello: toglie il burocratese e raddrizza i nessi -> v7' },
    { title: 'Collaudo', detail: 'conservazione due volte + cancello sulla finale + collaudatore semantico; riparazione mirata' },
    { title: 'Consegna', detail: 'atto depositabile, mappa delle prove, briefing al cliente' },
  ],
}

// ---- percorsi (assoluti: i subagent non ereditano la working dir) ----
const ROOT = '/Users/carlitos/mobilitas-agenti-ai/agente-avvocato-separazione'
const SK = ROOT + '/.claude/skills'
const AUTORE = SK + '/difensore-famiglia-strategia'
const OUT = ROOT + '/fascicolo'
const DATI = OUT + '/_dati'
const CASO = DATI + '/caso.json'
const REGISTRO = DATI + '/registro-fonti.md'
const TIMELINE = DATI + '/timeline.md'
const DEVIAZIONI = DATI + '/deviazioni-dal-metodo.md'
const SCADENZE = DATI + '/scadenze.md'
const MANIFESTO = DATI + '/livelli.json'
const SCRIPT = AUTORE + '/scripts/verifica_citazioni.py'
const SCRIPT_ATTO = AUTORE + '/scripts/verifica_atto.py'
const SCRIPT_CASO = AUTORE + '/scripts/verifica_caso.py'

const RETRIES = 3
const MAX_RIPARAZIONI = 2

// I nomi dei file della catena. v5 = ultima versione col contenuto approvato;
// v7 = il deliverable. Il collaudo confronta v5 con v7, cosi verifica le due
// riscritture insieme invece di lasciarle compensare a vicenda.
const F = (slug) => ({
  dir: `${OUT}/${slug}`,
  v1: `${OUT}/${slug}/v1-atto.md`,
  v2: `${OUT}/${slug}/v2-intermedia.md`,
  v3: `${OUT}/${slug}/v3-intermedia.md`,
  v4: `${OUT}/${slug}/v4-intermedia.md`,
  v5: `${OUT}/${slug}/v5-intermedia.md`,
  v6: `${OUT}/${slug}/v6-chiarezza.md`,
  v7: `${OUT}/${slug}/v7-finale.md`,
  prove: `${OUT}/${slug}/prove.md`,
  briefing: `${OUT}/${slug}/briefing.md`,
})

// ---- schemi ----

const DISCOVERY_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['tutte_le_skill', 'autore', 'primo_livello', 'secondo_livello', 'terzo_livello', 'quarto_livello', 'quinto_livello', 'sesto_livello', 'collaudo'],
  properties: {
    tutte_le_skill: { type: 'array', items: { type: 'string' }, description: 'Chiavi (dopo "difensore-famiglia-") di TUTTE le cartelle skill realmente presenti' },
    autore: { type: 'string' },
    primo_livello: { type: 'array', items: { type: 'string' } },
    secondo_livello: { type: 'array', items: { type: 'string' }, description: 'ORDINE SIGNIFICATIVO: "fonti" prima di "cassazione"' },
    terzo_livello: { type: 'array', items: { type: 'string' } },
    quarto_livello: { type: 'array', items: { type: 'string' } },
    quinto_livello: { type: 'array', items: { type: 'string' } },
    sesto_livello: { type: 'array', items: { type: 'string' } },
    collaudo: { type: 'array', items: { type: 'string' } },
  },
}

const FEEDBACK_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['revisore', 'rilievi'],
  properties: {
    revisore: { type: 'string' },
    giudizio_sintetico: { type: 'string', description: 'Una frase: l atto regge o no dal suo punto di vista' },
    verdetto: { type: 'string' },
    rilievi: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['severita', 'sezione', 'problema', 'correzione'],
        properties: {
          severita: { type: 'string', enum: ['ERRORE', 'RISCHIO', 'PREFERENZA'] },
          sezione: { type: 'string' },
          problema: { type: 'string' },
          correzione: { type: 'string', description: 'Cosa fare concretamente. Per le lenti che devono proporre una riformulazione, il testo della riformulazione' },
        },
      },
    },
  },
}

const RISCRITTURA_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['parole_prima', 'parole_dopo'],
  properties: {
    parole_prima: { type: 'number' },
    parole_dopo: { type: 'number' },
    variazione_percentuale: { type: 'string' },
    frasi_totali: { type: 'number' },
    frasi_toccate: { type: 'number' },
    passaggi_non_semplificabili: { type: 'array', items: { type: 'string' }, description: 'Passaggi che non si riuscivano a semplificare perche il ragionamento sotto e confuso. E un problema di contenuto, non di forma: va riportato a chi ha scritto l atto' },
    calchi_ricorrenti: { type: 'array', items: { type: 'string' }, description: 'Difetti di lingua che si ripetono e che si correggono a monte una volta sola' },
    informazioni_perse: { type: 'array', items: { type: 'string' }, description: 'Vuoto se la riscrittura e fedele. Qualunque voce qui e un errore da correggere' },
  },
}

const COLLAUDO_SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['esito', 'violazioni_bloccanti'],
  properties: {
    esito: { type: 'string', enum: ['DEPOSITABILE', 'DA_RIPARARE', 'DA_RIFARE'], description: 'DEPOSITABILE solo con ZERO bloccanti, del codice e del collaudatore' },
    bloccanti_dal_codice: { type: 'number' },
    violazioni_bloccanti: {
      type: 'array',
      description: 'Ogni voce e una riparazione da fare. Vuoto = riscrittura fedele.',
      items: {
        type: 'object', additionalProperties: false,
        required: ['tipo', 'sezione', 'riparazione'],
        properties: {
          tipo: { type: 'string', description: 'INFORMAZIONE_PERSA / CITAZIONE_COMPARSA / CITAZIONE_PERSA / CITAZIONE_NON_REGISTRATA / CITAZIONE_NON_CONFERMATA / ETICHETTA_ALZATA / ETICHETTA_RIANCORATA / ETICHETTA_SENZA_GLOSSA / ALLEGATO_RIANCORATO / ALLEGATO_NON_MAPPATO / DOMANDA_CON_PORTATA_CAMBIATA / QUALIFICAZIONE_CADUTA / VERBO_IRRIGIDITO / DATA_PERSA / HA_RISCRITTO_INVECE_DI_CORREGGERE / PIEDE_MANCANTE / PAS_INVOCATA / ATTACCO_ALLA_PERSONA / PIANO_GENITORIALE_ASSENTE / DOCUMENTAZIONE_ECONOMICA_ASSENTE / DOMANDE_NON_IN_PRIMA_PAGINA' },
          passaggio: { type: 'string', description: 'In quale riscrittura e nata: CHIAREZZA (v5->v6) / LINGUA (v6->v7) / ORIGINE (c era gia prima della v5) / INCERTO' },
          sezione: { type: 'string' },
          v5: { type: 'string' },
          finale: { type: 'string' },
          riparazione: { type: 'string' },
        },
      },
    },
  },
}

// ---- prompt ----

const discoveryPrompt = () => `Devi determinare ruoli e livelli delle skill di questo studio combinando la cartella reale e il manifesto.

1) Esegui: ls -1 ${SK}
   Prendi TUTTE le cartelle che iniziano con "difensore-famiglia-" e per ognuna estrai la chiave = la parte dopo quel prefisso (es. "difensore-famiglia-giudice" -> "giudice"). Questo e "tutte_le_skill".
2) Leggi il manifesto ${MANIFESTO} (JSON). Prendi "autore" (una chiave) e gli array "primo_livello", "secondo_livello", "terzo_livello", "quarto_livello", "quinto_livello", "sesto_livello", "collaudo" (un array puo mancare o essere vuoto -> restituisci []).

IMPORTANTE: in "secondo_livello" l ORDINE e significativo e va conservato come sta nel manifesto: "fonti" gira PRIMA di "cassazione", perche si ripulisce la base prima di ampliarla.

Restituisci l oggetto strutturato. Regole: usa SOLO cartelle realmente presenti; non inventare chiavi; se una chiave del manifesto non ha una cartella corrispondente, NON includerla.`

const ricercaPrompt = (slug, tipo) => `Sei il RICERCATORE dello studio. Prima che l atto "${tipo}" venga scritto, procuragli le fonti verificate.

## Il tuo mandato
Leggi e segui INTEGRALMENTE ${SK}/difensore-famiglia-cassazione/SKILL.md per il metodo di ricerca, e ${AUTORE}/references/verifica-delle-fonti.md per il protocollo di verifica.

## La regola che ti definisce
Vali solo se cio che porti e VERO. Non riportare mai un riferimento che non hai verificato IN QUESTA ricerca: non da memoria, non "mi risulta che". Un ricercatore che porta dieci sentenze di cui due inventate ha fatto un danno netto, perche le due affondano le otto.

## Le priorita, in ordine
1) L ORIENTAMENTO SU ETA E PERNOTTAMENTI. E la ricerca a piu alto rendimento del fascicolo: provvedimenti che hanno concesso pernottamenti sotto i tre anni, o che hanno censurato il diniego motivato SOLO sull eta. Nel registro e PARZIALE: portalo a CONFERMATA, con i numeri.
2) LA COMPETENZA ATTUALE. L entrata in funzione del Tribunale per le persone, per i minorenni e per le famiglie e prorogata al 31 ottobre 2026 ed e gia la seconda proroga. Verifica sul web se la data regge ancora e quale ufficio e competente OGGI.
3) LE PRASSI LOCALI del tribunale competente: protocolli su spese straordinarie, calendari tipo. Valgono, davanti a quel giudice, piu di tre sentenze di legittimita.
4) Cio che serve alle domande specifiche di questo atto.

## Cerca anche contro di noi
Se trovi l orientamento SFAVOREVOLE dominante, portalo. Un atto che anticipa l orientamento contrario e lo distingue e molto piu forte di uno che finge che non esista.

## Output
Scrivi in APPEND (mai riscrivere il file) su ${REGISTRO}, nella sezione giusta, ogni fonte con: riferimento, cosa afferma in una riga, livello (CONFERMATA / PARZIALE / NON TROVATA), dove l hai verificata, data.

Restituisci SOLO: quante fonti hai confermato, quante parziali, quante non trovate, l esito della ricerca sull eta e i pernottamenti, e qual e l orientamento contrario che ci troviamo davanti.`

const draftPrompt = (slug, tipo) => `Sei IL DIFENSORE. Redigi la v1 dell atto "${tipo}" per la pratica "${slug}".

## Metodo — leggi tutto prima di scrivere una riga
${AUTORE}/SKILL.md, e nell ordine i reference: verifica-delle-fonti.md, quadro-normativo.md, rito-e-processo.md, termini-e-adempimenti.md, figlio-infra-triennale.md, affidamento-e-collocamento.md, mantenimento-e-spese.md, casa-familiare.md, convivenza-senza-matrimonio.md, accordo-e-negoziazione.md, penale-della-famiglia.md, prove-e-trappole.md, dopo-la-prima-udienza.md, architettura-atto.md.

## PRIMA DI TUTTO: il cancello sui fatti
Gli altri cancelli guardano l atto. Questo guarda da dove vengono i fatti, ed e l unico che puo fermarti PRIMA che il danno sia scritto:

python3 ${SCRIPT_CASO} ${CASO} --tipo ${tipo}

Se esce con BLOCCANTI, NON SCRIVERE L ATTO. Restituisci l elenco dei campi vuoti e delle incoerenze, e fermati: i campi si chiedono al cliente e si registrano in ${CASO}, non si riempiono con un valore verosimile. Un reddito plausibile in un ricorso e una busta paga in mano alla controparte, e vale come una sentenza inventata.

Gli AVVISI non ti fermano: leggili, perche sono i rischi che il fascicolo rende gia visibili — a cominciare dall art. 337-sexies c.c. sulla casa.

## I fatti — non inventarne altri
- ${CASO} : i fatti del caso. I campi null sono DA COMPILARE: non riempirli, elencali.
- ${TIMELINE} : le date. Una data che non e qui non entra in un atto.
- ${REGISTRO} : le UNICHE fonti citabili. Nessun numero di sentenza fuori da qui.
- ${DEVIAZIONI} : dove questo metodo e gia stato trovato sbagliato. Leggilo per non reintrodurre un errore gia corretto.
- ${SCADENZE} : i termini aperti. Se questo atto ne apre o ne consuma uno, la riga va scritta li.

## Le regole che non si negoziano
- Le DOMANDE in prima pagina, numerate, formulate in modo da poter essere COPIATE nel dispositivo. Se il giudice deve riformularle, lo fara al ribasso.
- Un paragrafo, un fatto, un allegato.
- Ogni fatto porta l etichetta di prova con la glossa: PROVATO (documento in atti), DOCUMENTABILE (documento esistente, da acquisire), ALLEGABILE (da provare per testi o presunzioni). NESSUN "NON SOSTENIBILE" entra in un atto.
- Ogni domanda ha la sua traduzione in INTERESSE DEL MINORE. Se non riesci a scriverla, la domanda esce.
- Si attaccano le condotte con le date, MAI la persona della madre. E si riconosce cio che ha fatto bene: e la mossa che sblocca i provvedimenti.
- Niente PAS. Si scrivono condotte ostative documentate.
- Il piede obbligatorio sulla revisione del difensore iscritto all albo.
- Lunghezza 8-15 pagine, allegati esclusi.
- SE E UN ATTO INTRODUTTIVO (ricorso o comparsa di risposta), il rito pretende dentro l atto, non come allegati facoltativi: il PIANO GENITORIALE, le DICHIARAZIONI DEI REDDITI DEGLI ULTIMI TRE ANNI, la documentazione patrimoniale, gli ESTRATTI CONTO DEGLI ULTIMI TRE ANNI, e l indicazione di altri procedimenti pendenti (artt. 473-bis.12 e 473-bis.16 c.p.c., verificati). Il piano genitoriale non si compila in tre righe perche il bambino ha un anno: e il documento in cui si MOSTRA di sapere com e fatta la giornata di suo figlio, ed e la risposta migliore alla tesi dell assenza di accudimento paterno.
- Niente domande RISERVATE. "Ci si riserva di" ha l aspetto della prudenza ed e il modo principale in cui in questo rito si perde una domanda per sempre.

## Il nodo di questo caso
Il bambino ha un anno e la convivenza e cessata a quattro mesi dal parto. NON chiedere il collocamento paritetico: chiedi il CALENDARIO PROGRESSIVO CON AUTOMATISMI a date certe. E la domanda che un giudice concede, e toglie al tempo il potere di lavorare contro di noi.

## Output
- ${F(slug).v1}  -> l atto v1
- ${F(slug).prove} -> la mappa delle prove: ogni fatto, il documento che lo prova, il numero di allegato
- ${F(slug).briefing} -> il briefing al cliente, in italiano NON giuridico, con le sezioni "cosa fare", "cosa non fare mai", "cosa procurarmi" e "cosa non ti prometto"

Restituisci SOLO: le domande formulate, cosa e rimasto ALLEGABILE e perche, quali fonti ti sono mancate, e quali domande hai tolto perche non si traducevano nell interesse del minore.`

const reviewPrompt = (slug, r, versione, fase) => `Sei il revisore ${r.key} del panel difensivo. Rivedi l atto della pratica "${slug}".

## Il tuo ruolo e metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md. Rispetta il tuo LIMITE dichiarato nella skill: e la parte che impedisce alla tua lente di degenerare, ed e vincolante quanto il resto.

## Contesto del caso
Leggi ${CASO} e ${TIMELINE}. Padre, convivenza di fatto mai formalizzata, figlio di circa un anno, rottura a quattro mesi dal parto.

## Documento da revisionare
${versione}
Se non esiste, restituisci un rilievo ERRORE che dice che la versione manca.
Leggi anche ${F(slug).prove} (mappa delle prove) e ${F(slug).briefing} (briefing al cliente) se esistono: alcune lenti li devono guardare.

## Output
Restituisci l oggetto strutturato richiesto, mappando i tuoi rilievi sulle severita ERRORE / RISCHIO / PREFERENZA. Ogni ERRORE indica il punto preciso e propone la RIFORMULAZIONE, non solo la cancellazione.
In parallelo salva la tua revisione, nel formato di output della tua skill, in ${OUT}/${slug}/feedback-${r.key}${fase}.md`

const synthPrompt = (slug, da, a, fase, istruzioni) => `Sei IL DIFENSORE. Produci la nuova versione dell atto della pratica "${slug}".

## Metodo
Leggi ${AUTORE}/SKILL.md. La regola che protegge l atto: IL FEEDBACK SI PESA, NON SI SOMMA. ERRORE si corregge, RISCHIO si valuta, PREFERENZA si ignora di default. Se l atto cresce oltre il 20%, hai sommato invece di pesare — e un atto gonfio viene letto in diagonale proprio nelle parti che contano.

${istruzioni}

## Input
- Versione da lavorare: ${da}
- Rilievi: leggi TUTTI i file ${OUT}/${slug}/feedback-*${fase}.md
- Fonti citabili: ${REGISTRO}. Se un revisore chiede una fonte che non c e, NON inventare il numero: scrivi il principio senza numero.

## Output
- ${a}

Restituisci SOLO: cosa hai corretto, cosa hai ignorato e perche, la variazione percentuale di lunghezza, e gli eventuali conflitti fra revisori che hai dovuto sciogliere indicando come.`

const rewritePrompt = (slug, r) => `Sei il riscrittore di QUINTO livello — la chiarezza. Non emetti rilievi: RISCRIVI DA CAPO l intero atto.

## Metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md.

Prima di te sono girati dodici revisori: contenuto, fonti, esposizione penale, coerenza e lunghezza sono CHIUSI. Non tocchi niente di tutto questo. Il tuo problema e un altro: l atto e giusto e si legge male.

> Riscrivi l atto in modo che un giudice lo capisca ALLA PRIMA LETTURA, IN VENTI MINUTI, senza tornare indietro su una sola frase, e SENZA che si perda una sola informazione.

## Il metodo: si riscrive, non si corregge
1. Leggi tutto senza scrivere niente.
2. Costruisci l INVENTARIO delle informazioni: ogni fatto, data, numero, etichetta, richiamo ad allegato, citazione, domanda, istanza. E il tuo contratto.
3. Riscrivi sezione per sezione GUARDANDO L INVENTARIO, non il vecchio testo. Se hai il vecchio testo davanti mentre scrivi, ne copierai la sintassi.
4. Ricontrolla l inventario alla fine: ogni voce non ricomparsa e un informazione persa, rimettila.

## L INVIOLABILE
Ogni data, numero, importo, percentuale. Ogni etichetta di prova (NON alzarne nessuna). Ogni richiamo ad allegato col suo numero. Ogni riferimento normativo e giurisprudenziale esattamente come sta — e se una fonte e citata come principio SENZA NUMERO, resta senza numero: aggiungerne uno e la violazione piu grave che tu possa commettere. Ogni domanda e conclusione, nella portata. Ogni dettaglio del calendario. I cinque elementi della clausola sulle spese straordinarie. Ogni qualificazione ("nella maggior parte dei casi", "salvo verifica"). Il riconoscimento dell accudimento materno. Il piede.

## Il pericolo strutturale
Le frasi corte sono piu assertive per costruzione: "puo aver contribuito" diventa "ha contribuito", "risulterebbe" diventa "risulta". Dopo ogni sezione rileggi i VERBI e riporta indietro quelli che si sono induriti.

## Lunghezza
Da -5% a +10%. Sotto -5% hai tagliato informazione, sopra +10% hai aggiunto contenuto.

## Input / Output
- Da: ${F(slug).v5}
- A:  ${F(slug).v6}

Restituisci l oggetto strutturato richiesto.`

const linguaPrompt = (slug, r) => `Sei il revisore di SESTO livello — la lingua. NON riscrivi: passi frase per frase e correggi SOLO quelle che hanno un difetto di italiano.

## Metodo
Leggi e segui INTEGRALMENTE ${r.skill}/SKILL.md.

Il quinto livello lavora sulla complessita, tu sulla NATURALEZZA. Una frase puo essere corta, chiara e semplice, e restare scritta in un italiano che nessun madrelingua scriverebbe: quello e il tuo bersaglio, e nient altro.

## Cosa correggi
Burocratese inutile ("in ordine a", "porre in essere", "si rappresenta che", "provvedere al versamento"), nessi logici mancanti o sbagliati, pronomi vaghi appesi a un intera frase, collocazioni improprie, sintassi rovesciata. NON tocchi le formule tecniche corrette ("ricorre", "chiede e conclude").

## I vincoli misurabili
Delta di lunghezza da -3% a +5%. Frasi toccate: MASSIMO IL 40%. Se tocchi piu del 40%, non hai fatto una revisione: hai riscritto, e una seconda riscrittura integrale raddoppia la deriva che il collaudo esiste per fermare.

## L INVIOLABILE
Identico al livello prima. In particolare: NON alzare nessuna etichetta di prova, e NON AGGIUNGERE MAI UN NUMERO DI SENTENZA. Se una fonte e citata come principio senza numero, resta senza numero.

## Il controllo finale
Prima di consegnare rileggi SOLO i verbi delle affermazioni di fatto: una correzione di lingua puo irrigidirli senza volerlo. Se l etichetta e rimasta ma il verbo si e indurito, l atto afferma piu di quanto provi.

## Input / Output
- Da: ${F(slug).v6}
- A:  ${F(slug).v7}

Restituisci l oggetto strutturato richiesto.`

const collaudoPrompt = (slug, g, tipo) => `Sei IL CANCELLO — il collaudo di conservazione e integrita delle citazioni della pratica "${slug}".

## Metodo
Leggi e segui INTEGRALMENTE ${g.skill}/SKILL.md.

## Prima di leggere: fai girare il codice, DUE VOLTE
Buona parte del collaudo e meccanica, e una macchina non puo illudersi di aver controllato. Due riscritture misurate in blocco si compensano a vicenda, quindi si misurano separatamente:

python3 ${SCRIPT} ${F(slug).v5} ${F(slug).v6} --registro ${REGISTRO} --delta-min -5 --delta-max 10 --passaggio CHIAREZZA

python3 ${SCRIPT} ${F(slug).v6} ${F(slug).v7} --registro ${REGISTRO} --delta-min -3 --delta-max 5 --min-identita 60 --passaggio LINGUA

## Poi il cancello sulla versione FINALE, da sola
I due comandi qui sopra confrontano versioni: vedono cosa si e perso, non cosa non c e mai stato. Un atto puo attraversare tutta la catena conservando fedelmente un difetto che aveva dalla v1.

python3 ${SCRIPT_ATTO} ${F(slug).v7} --tipo ${tipo} --registro ${REGISTRO} --prove ${F(slug).prove} --timeline ${TIMELINE}

Riporta i suoi BLOCCANTI come violazioni con passaggio "ORIGINE" (non sono nate in una riscrittura: c erano prima). I suoi AVVISI non sono violazioni: elencali a parte, sono le cose che una macchina non puo decidere.

Quello che gli script trovano e GIA ACCERTATO: non riverificarlo, riportalo, e per ogni violazione dichiara in quale passaggio e nata.

## Poi la lettura semantica, sull intera catena: ${F(slug).v5} contro ${F(slug).v7}
Cerca cio che nessun conteggio vede: etichette riancorate a un altro fatto, allegati che ora sostengono un fatto diverso, informazione persa per ASSORBIMENTO (due frasi che ne diventano una che sembra completa), qualificazioni cadute, verbi irrigiditi, e — la piu grave, specifica degli atti — DOMANDE CON LA PORTATA CAMBIATA: una domanda riformulata per chiarezza puo diventare piu ampia o piu stretta senza che nessuno se ne accorga.

## La regola che ti definisce
CONSERVAZIONE, NON QUALITA. Se un argomento ti sembra debole ma c era identico nella v5, NON e un tuo rilievo: taci. Un collaudatore che trova cose nuove non e piu severo: e rotto.

Le sole eccezioni sono le tre cose che una riscrittura puo INTRODURRE: un affermazione piu forte di quella che sostituisce, una citazione che prima non c era, un impegno che l atto prima non conteneva.

Restituisci l oggetto strutturato richiesto. DEPOSITABILE solo con ZERO bloccanti, del codice e tuoi.`

const riparaPrompt = (slug, viol) => `Sei chi ha prodotto la versione finale dell atto "${slug}". Il collaudo ha trovato violazioni. Fai una RIPARAZIONE CHIRURGICA: rimetti a posto SOLO i punti indicati, senza toccare il resto e senza riscrivere.

## Violazioni da riparare
${viol.map((v, i) => `${i + 1}. [${v.tipo}] (nata in: ${v.passaggio || 'INCERTO'}) — sezione "${v.sezione}"
   v5: ${v.v5 || '(non riportato)'}
   FINALE: ${v.finale || '(non riportato)'}
   Riparazione: ${v.riparazione}`).join('\n')}

## Regole
- Riparazione CHIRURGICA: tocchi solo le frasi indicate. Una nuova riscrittura integrale raddoppierebbe la deriva.
- Se devi rimettere un informazione, riprendila dalla v5 ${F(slug).v5} e riformulala nello stile della finale.
- Se la violazione e CITAZIONE_COMPARSA o CITAZIONE_NON_REGISTRATA: TOGLI il numero e lascia il principio. Non cercare di verificarla adesso.
- Se la violazione e ETICHETTA_ALZATA: riporta l etichetta a quella della v5. Sempre verso il basso, mai verso l alto.
- Se e DOMANDA_CON_PORTATA_CAMBIATA: riporta la domanda alla portata esatta della v5.
- Se il passaggio e ORIGINE, il difetto non viene da una riscrittura: c era gia. Non cercarlo nella v5 — va aggiunto o corretto adesso. Vale per il piede mancante, la glossa di un etichetta, l indice degli allegati, il piano genitoriale e la documentazione economica di un atto introduttivo.
- Se e PAS_INVOCATA o ATTACCO_ALLA_PERSONA: riscrivi il passaggio come CONDOTTA CON LA DATA e l allegato. Non attenuare l aggettivo: toglilo.

## Output
Riscrivi ${F(slug).v7} con le riparazioni applicate.
Restituisci SOLO: quante violazioni hai riparato, quali non hai potuto riparare e perche.`

// ============================ RESILIENZA ============================

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

async function promuovi(da, a, motivo) {
  log(`  [resilienza] ${motivo}: promuovo ${da.split('/').pop()} -> ${a.split('/').pop()} senza modifiche`)
  const r = await robustAgent(
    `Copia INTEGRALMENTE il contenuto di ${da} in ${a}, senza modificare una sola parola. Se ${da} non esiste, dillo e non creare nulla. Restituisci solo: "copiato" oppure "sorgente assente".`,
    { label: `promuovi:${a.split('/').pop()}`, phase: 'Sintesi v2', agentType: 'general-purpose' }, 2
  )
  // Gli agenti riferiscono, non provano: una promozione fallita e un fatto registrato,
  // e l esito finale si decide guardando il disco.
  if (!r) {
    const msg = `PROMOZIONE NON CONFERMATA verso ${a.split('/').pop()} (${motivo}): il file potrebbe NON esistere`
    log(`  [resilienza] ATTENZIONE: ${msg}`)
    PROMOZIONI_FALLITE.push(msg)
  }
  return r
}

// ============================ ORCHESTRAZIONE ============================

// args accetta:
//   ["ricorso-affidamento"]                          una o piu pratiche
//   { pratiche: ["..."], tipo: "ricorso", stati: {} } con tipo di atto e stato di ripresa
const argObj = (args && typeof args === 'object' && !Array.isArray(args)) ? args : null
const STATI = (argObj && argObj.stati) || {}
const fatto = (slug, file) => ((STATI[slug] || []).includes(file))
const TIPO = (argObj && argObj.tipo) || 'ricorso'

const parseArgs = (a) => {
  if (Array.isArray(a)) return a
  if (typeof a === 'string') {
    const s = a.trim()
    if (s.startsWith('[')) { try { const p = JSON.parse(s); if (Array.isArray(p)) return p } catch (e) { /* slug singolo */ } }
    return s ? [s] : []
  }
  return a ? [a] : []
}

const slugs = parseArgs(argObj ? argObj.pratiche : args).map((s) => String(s).trim()).filter(Boolean)

if (!slugs.length) {
  log('Nessuna pratica indicata. Passa es. ["ricorso-affidamento"] oppure { pratiche: [...], tipo: "memoria" }.')
  return { errore: 'args vuoto' }
}
log(`Genero ${slugs.length} atto/i (tipo: ${TIPO}): ${slugs.join(', ')}`)

// --- FASE 0: SCOPERTA ---
phase('Scoperta')
const disc = await robustAgent(discoveryPrompt(), { label: 'scopri-ruoli', phase: 'Scoperta', schema: DISCOVERY_SCHEMA, agentType: 'general-purpose' })
if (!disc) {
  log('ATTENZIONE: scoperta ruoli non riuscita. Interrompo: senza il manifesto non so chi rivede.')
  return { errore: 'scoperta ruoli fallita (manifesto ' + MANIFESTO + ' non leggibile dopo ' + RETRIES + ' tentativi)' }
}

const all = ((disc && disc.tutte_le_skill) || []).filter(Boolean)
const autore = (disc && disc.autore) || 'strategia'
const usate = new Set([autore])
const filtra = (arr) => ((arr) || []).filter((k) => {
  if (!all.includes(k) || usate.has(k)) return false
  usate.add(k); return true
})
const mk = (k) => ({ key: k, skill: SK + '/difensore-famiglia-' + k })

const L1 = filtra(disc.primo_livello).map(mk)
const L2 = filtra(disc.secondo_livello).map(mk)   // ORDINE conservato: fonti prima di cassazione
const L3 = filtra(disc.terzo_livello).map(mk)
const L4 = filtra(disc.quarto_livello).map(mk)
const L5 = filtra(disc.quinto_livello).map(mk)
const L6 = filtra(disc.sesto_livello).map(mk)
const GATE = filtra(disc.collaudo).map(mk)

const nonAssegnate = all.filter((k) => !usate.has(k))
if (nonAssegnate.length) log(`ATTENZIONE: skill presenti ma non assegnate a nessun livello nel manifesto (ignorate): ${nonAssegnate.join(', ')}`)
if (!L1.length && !L2.length && !L3.length) {
  log('ATTENZIONE: nessun revisore dichiarato nel manifesto. Interrompo.')
  return { errore: 'nessun revisore nei livelli del manifesto' }
}
log(`Autore: ${autore} | 1o (${L1.length}): ${L1.map(r => r.key).join(', ') || '—'} | 2o (${L2.length}): ${L2.map(r => r.key).join(', ') || '—'} | 3o: ${L3.map(r => r.key).join(', ') || '—'} | 4o: ${L4.map(r => r.key).join(', ') || '—'} | 5o: ${L5.map(r => r.key).join(', ') || '—'} | 6o: ${L6.map(r => r.key).join(', ') || '—'} | collaudo: ${GATE.map(r => r.key).join(', ') || '— NESSUNO'}`)
if (!GATE.length) log('ATTENZIONE: nessun collaudo nel manifesto. Le citazioni della versione finale non verranno verificate da nessuno.')

// --- catena, una pratica alla volta attraverso tutti gli stadi ---
const results = await pipeline(
  slugs,

  // STAGE 1: ricerca delle fonti + draft
  async (slug) => {
    if (!fatto(slug, 'v1-atto.md')) {
      await robustAgent(ricercaPrompt(slug, TIPO), { label: `ricerca:${slug}`, phase: 'Ricerca', agentType: 'ricercatore-giurisprudenza' }, 2)
      const r = await robustAgent(draftPrompt(slug, TIPO), { label: `draft:${slug}`, phase: 'Draft', agentType: 'general-purpose' })
      // Il draft e l unico stadio senza fallback: senza bozza non c e nulla da revisionare.
      // Il throw dentro pipeline() scarta SOLO questa pratica, le altre proseguono.
      if (!r) { log(`ATTENZIONE: draft non riuscito per ${slug} — salto SOLO questa pratica`); throw new Error(`draft fallito per ${slug}`) }
      log(`Draft pronto: ${slug}`)
    } else log(`[ripresa] ${slug}: v1 gia su disco, salto ricerca e draft`)
    return slug
  },

  // STAGE 2: 1o livello in parallelo -> sintesi v2
  async (slug) => {
    if (fatto(slug, 'v2-intermedia.md')) { log(`[ripresa] ${slug}: v2 gia su disco`); return slug }
    const f = F(slug)
    if (L1.length) {
      const fbs = await parallel(L1.map((rv) => () =>
        agent(reviewPrompt(slug, rv, f.v1, ''), { label: `rev1:${rv.key}:${slug}`, phase: 'Revisione', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })))
      log(`Revisione 1o livello ${slug}: ${fbs.filter(Boolean).length}/${L1.length} lenti`)
    }
    const r = await robustAgent(synthPrompt(slug, f.v1, f.v2, '',
      `## Il conflitto tipico di questo livello
"avversario" e "penalista" chiedono di togliere un passaggio esposto, "cliente" lo vuole tenere. Vince chi parla la lingua del giudice: se il passaggio non serve a ottenere un provvedimento, ESCE — e la ragione si spiega nel briefing, non nell atto.
Aggiorna anche ${f.briefing} con cio che le lenti "cliente" e "penalista" hanno chiesto di prevenire.

## Le due lenti che non discutono il merito
"decadenze" non esprime preferenze: se dice che una domanda e riservata invece che formulata, o che manca un contenuto che il rito pretende, e sempre un ERRORE e si corregge. Non e un parere.
"negoziatore" non chiede di indebolire le domande, chiede di renderle accettabili a parita di sostanza. Se un suo rilievo riduce cio che il cliente otterrebbe, e un rilievo sbagliato: scarta quello, tieni la riformulazione. E se ha prodotto una proposta conciliativa, salvala in ${OUT}/${slug}/proposta.md: non entra nell atto, ma e materiale che vale quanto l atto.`),
      { label: `sintesi-v2:${slug}`, phase: 'Sintesi v2', agentType: 'general-purpose' })
    if (!r) await promuovi(f.v1, f.v2, `sintesi v2 non riuscita per ${slug}`)
    else log(`v2 pronta: ${slug}`)
    return slug
  },

  // STAGE 3: 2o livello (fonti POI cassazione) -> sintesi v3
  async (slug) => {
    if (fatto(slug, 'v3-intermedia.md')) { log(`[ripresa] ${slug}: v3 gia su disco`); return slug }
    const f = F(slug)
    if (!L2.length) { await promuovi(f.v2, f.v3, `nessun 2o livello per ${slug}`); return slug }
    // SEQUENZIALI, non in parallelo: si ripulisce la base prima di ampliarla.
    for (const rv of L2) {
      await robustAgent(reviewPrompt(slug, rv, f.v2, '-r2'), { label: `rev2:${rv.key}:${slug}`, phase: 'Fonti', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' }, 2)
    }
    log(`Revisione 2o livello ${slug}: ${L2.map(r => r.key).join(' poi ')}`)
    const r = await robustAgent(synthPrompt(slug, f.v2, f.v3, '-r2',
      `## Vincolo assoluto di questo livello
Nessuna citazione entra nell atto se non e in ${REGISTRO} come CONFERMATA. Una fonte PARZIALE si cita come PRINCIPIO SENZA NUMERO. Se "cassazione" ha proposto fonti, verifica che siano state registrate: se non lo sono, usale come principio senza numero.`),
      { label: `sintesi-v3:${slug}`, phase: 'Sintesi v3', agentType: 'general-purpose' })
    if (!r) await promuovi(f.v2, f.v3, `sintesi v3 non riuscita per ${slug}`)
    else log(`v3 pronta: ${slug}`)
    return slug
  },

  // STAGE 4: 3o livello (coerenza) -> sintesi v4
  async (slug) => {
    if (fatto(slug, 'v4-intermedia.md')) { log(`[ripresa] ${slug}: v4 gia su disco`); return slug }
    const f = F(slug)
    if (!L3.length) { await promuovi(f.v3, f.v4, `nessun 3o livello per ${slug}`); return slug }
    const fbs = await parallel(L3.map((rv) => () =>
      agent(reviewPrompt(slug, rv, f.v3, '-r3'), { label: `rev3:${rv.key}:${slug}`, phase: 'Coerenza', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })))
    log(`Revisione 3o livello ${slug}: ${fbs.filter(Boolean).length}/${L3.length}`)
    const r = await robustAgent(synthPrompt(slug, f.v3, f.v4, '-r3',
      `## Regola di questo livello
Le contraddizioni segnalate SI CORREGGONO SEMPRE, e sul lato che il revisore ha indicato: non sono preferenze, sono due affermazioni incompatibili nello stesso fascicolo. Una divergenza fra fronte civile e fronte penale ha priorita su tutto il resto.`),
      { label: `sintesi-v4:${slug}`, phase: 'Sintesi v4', agentType: 'general-purpose' })
    if (!r) await promuovi(f.v3, f.v4, `sintesi v4 non riuscita per ${slug}`)
    else log(`v4 pronta: ${slug}`)
    return slug
  },

  // STAGE 5: 4o livello (editor) -> sintesi v5
  async (slug) => {
    if (fatto(slug, 'v5-intermedia.md')) { log(`[ripresa] ${slug}: v5 gia su disco`); return slug }
    const f = F(slug)
    if (!L4.length) { await promuovi(f.v4, f.v5, `nessun 4o livello per ${slug}`); return slug }
    const fbs = await parallel(L4.map((rv) => () =>
      agent(reviewPrompt(slug, rv, f.v4, '-r4'), { label: `rev4:${rv.key}:${slug}`, phase: 'Asciugatura', schema: FEEDBACK_SCHEMA, agentType: 'general-purpose' })))
    log(`Revisione 4o livello ${slug}: ${fbs.filter(Boolean).length}/${L4.length}`)
    const r = await robustAgent(synthPrompt(slug, f.v4, f.v5, '-r4',
      `## Regola di questo livello
Si asciuga solo se necessario per rientrare nelle 8-15 pagine. NON toccare l INTOCCABILE: domande, conclusioni, etichette di prova, richiami ad allegato, sezione sull interesse del minore, riconoscimento dell accudimento materno, DETTAGLI DEL CALENDARIO (orari, scambi, festivita con anni pari e dispari), i cinque elementi delle spese straordinarie, date, numeri, qualificazioni, piede.
Il taglio piu dannoso possibile e togliere il dettaglio del calendario perche "si puo concordare": e esattamente la clausola che genera dieci anni di liti.`),
      { label: `sintesi-v5:${slug}`, phase: 'Sintesi v5', agentType: 'general-purpose' })
    if (!r) await promuovi(f.v4, f.v5, `sintesi v5 non riuscita per ${slug}`)
    else log(`v5 pronta: ${slug}`)
    return slug
  },

  // STAGE 6: 5o livello (riscrittura) e 6o (lingua)
  async (slug) => {
    const f = F(slug)
    if (!fatto(slug, 'v6-chiarezza.md')) {
      if (!L5.length) { await promuovi(f.v5, f.v6, `nessuna riscrittura di chiarezza per ${slug}`) }
      else {
        if (L5.length > 1) log(`ATTENZIONE: piu di un riscrittore di 5o livello. Uso "${L5[0].key}", ignoro: ${L5.slice(1).map(r => r.key).join(', ')}`)
        const rep = await robustAgent(rewritePrompt(slug, L5[0]), { label: `chiarezza:${slug}`, phase: 'Riscrittura', schema: RISCRITTURA_SCHEMA, agentType: 'general-purpose' })
        if (!rep) await promuovi(f.v5, f.v6, `riscrittura non riuscita per ${slug}`)
        else {
          if (rep.informazioni_perse && rep.informazioni_perse.length)
            log(`ATTENZIONE ${slug}: la riscrittura dichiara ${rep.informazioni_perse.length} informazioni perse — il collaudo le ritrovera`)
          if (rep.passaggi_non_semplificabili && rep.passaggi_non_semplificabili.length)
            log(`Segnale: ${slug} — ${rep.passaggi_non_semplificabili.length} passaggi non semplificabili. Non e un problema di forma: il ragionamento sotto e confuso`)
          log(`v6 riscritta: ${slug} — ${rep.parole_prima} → ${rep.parole_dopo} parole (${rep.variazione_percentuale || 'n/d'})`)
        }
      }
    } else log(`[ripresa] ${slug}: v6 gia su disco`)

    if (!fatto(slug, 'v7-finale.md')) {
      if (!L6.length) { await promuovi(f.v6, f.v7, `nessuna revisione di lingua per ${slug}`) }
      else {
        const rep = await robustAgent(linguaPrompt(slug, L6[0]), { label: `lingua:${slug}`, phase: 'Lingua', schema: RISCRITTURA_SCHEMA, agentType: 'general-purpose' })
        if (!rep) await promuovi(f.v6, f.v7, `revisione di lingua non riuscita per ${slug}`)
        else {
          const tot = rep.frasi_totali || 0, toc = rep.frasi_toccate || 0
          const quota = tot ? Math.round(toc / tot * 100) : 0
          if (quota > 40) log(`ATTENZIONE ${slug}: la revisione di lingua ha toccato il ${quota}% delle frasi. Oltre il 40% non e una revisione: o il 5o livello ha lavorato male, o il 6o ha riscritto`)
          if (rep.calchi_ricorrenti && rep.calchi_ricorrenti.length)
            log(`  ${slug} — difetti di lingua ricorrenti da correggere a monte: ${rep.calchi_ricorrenti.join(' · ')}`)
          log(`v7 FINALE pronta: ${slug} — ${toc}/${tot} frasi toccate (${rep.variazione_percentuale || 'n/d'})`)
        }
      }
    } else log(`[ripresa] ${slug}: v7 gia su disco`)
    return slug
  },

  // STAGE 7: COLLAUDO con riparazione mirata
  async (slug) => {
    const base = { slug, tipo: TIPO }
    if (!GATE.length) {
      log(`ATTENZIONE ${slug}: nessun collaudo nel manifesto — la finale va in consegna senza cancello`)
      return { ...base, esito: 'NON COLLAUDATA' }
    }
    const g = GATE[0]
    for (let giro = 1; giro <= MAX_RIPARAZIONI + 1; giro++) {
      const c = await robustAgent(collaudoPrompt(slug, g, TIPO), { label: giro === 1 ? `collaudo:${slug}` : `collaudo:${slug}#giro${giro}`, phase: 'Collaudo', schema: COLLAUDO_SCHEMA, agentType: 'general-purpose' }, 2)
      if (!c) {
        log(`ATTENZIONE ${slug}: il collaudo non ha risposto. La finale resta, ma NON e stata verificata`)
        return { ...base, esito: 'NON COLLAUDATA' }
      }
      const viol = (c.violazioni_bloccanti || []).filter(Boolean)
      if (c.esito === 'DEPOSITABILE' && !viol.length) {
        log(`COLLAUDO SUPERATO ${slug}${giro > 1 ? ` (dopo ${giro - 1} riparazion${giro === 2 ? 'e' : 'i'})` : ''}`)
        return { ...base, esito: 'DEPOSITABILE', riparazioni: giro - 1 }
      }
      if (c.esito === 'DA_RIFARE') {
        // L accuratezza batte la leggibilita: si consegna la v5, meno scorrevole e verificata.
        log(`COLLAUDO ${slug}: DA RIFARE (${viol.length} perdite diffuse). Consegno la v5: l accuratezza batte la leggibilita`)
        await promuovi(F(slug).v5, F(slug).v7, `perdite diffuse nella riscrittura di ${slug}`)
        return { ...base, esito: 'CONSEGNATA LA v5', violazioni: viol.length }
      }
      if (giro > MAX_RIPARAZIONI) {
        log(`ATTENZIONE ${slug}: ${viol.length} violazioni ancora aperte dopo ${MAX_RIPARAZIONI} riparazioni. NON DEPOSITABILE senza intervento umano`)
        return { ...base, esito: 'NON DEPOSITABILE', violazioni: viol.length }
      }
      log(`Collaudo ${slug}: ${viol.length} violazioni (${c.bloccanti_dal_codice || 0} dal codice). Riparazione mirata, giro ${giro}`)
      const fix = await robustAgent(riparaPrompt(slug, viol), { label: `ripara:${slug}#${giro}`, phase: 'Collaudo', agentType: 'general-purpose' }, 2)
      if (!fix) {
        log(`ATTENZIONE ${slug}: la riparazione non ha risposto. Consegno la v5, ultima versione verificata`)
        await promuovi(F(slug).v5, F(slug).v7, `riparazione non riuscita per ${slug}`)
        return { ...base, esito: 'CONSEGNATA LA v5' }
      }
    }
    return { ...base, esito: 'NON DEPOSITABILE' }
  },
)

// --- VERIFICA FINALE SUL DISCO ---
// L unico giudice di "fatto" e il file system: gli agenti riferiscono, non provano.
phase('Consegna')
const esiti = results.filter(Boolean)
const VERIFICA_SCHEMA = {
  type: 'object', additionalProperties: false, required: ['stato'],
  properties: {
    stato: {
      type: 'array',
      items: {
        type: 'object', additionalProperties: false,
        required: ['slug', 'ultima_versione', 'ha_v7', 'ha_prove', 'ha_briefing'],
        properties: {
          slug: { type: 'string' },
          ultima_versione: { type: 'string' },
          ha_v7: { type: 'boolean' },
          ha_prove: { type: 'boolean' },
          ha_briefing: { type: 'boolean' },
        },
      },
    },
  },
}
const ver = await robustAgent(
  `Per ognuna di queste pratiche — ${slugs.join(', ')} — esegui: ls -1 ${OUT}/<pratica>
Riporta il file di versione piu avanzato presente, seguendo l ordine v1-atto.md, v2-intermedia.md, v3-intermedia.md, v4-intermedia.md, v5-intermedia.md, v6-chiarezza.md, v7-finale.md, e di se esistono v7-finale.md, prove.md e briefing.md.
Non inventare: riporta solo cio che ls mostra.`,
  { label: 'verifica-sul-disco', phase: 'Consegna', schema: VERIFICA_SCHEMA, agentType: 'general-purpose' }, 2
)

if (!ver) {
  return { esiti, avviso: 'NON VERIFICATO sul disco: gli esiti qui sopra sono dichiarazioni degli agenti, non fatti. Controlla a mano.', promozioni_fallite: PROMOZIONI_FALLITE }
}
const perSlug = new Map((ver.stato || []).map((s) => [s.slug, s]))
const consegnabili = [], incomplete = []
for (const e of esiti) {
  const s = perSlug.get(e.slug)
  if (s && s.ha_v7) consegnabili.push({ ...e, verificata: true, ha_prove: s.ha_prove, ha_briefing: s.ha_briefing })
  else incomplete.push({ slug: e.slug, dichiarato: e.esito, realta: s ? `ferma a ${s.ultima_versione}` : 'cartella non leggibile' })
}
if (incomplete.length) log(`ATTENZIONE: ${incomplete.length} atti dichiarati completati NON hanno la v7 sul disco: ${incomplete.map(i => i.slug).join(', ')}`)
const senzaBriefing = consegnabili.filter((c) => !c.ha_briefing)
if (senzaBriefing.length) log(`ATTENZIONE: ${senzaBriefing.length} atti senza briefing al cliente. In questa materia il briefing pesa piu dell atto: ${senzaBriefing.map(c => c.slug).join(', ')}`)

log('PROMEMORIA: questo materiale va rivisto, sottoscritto e depositato da un avvocato iscritto all albo. Nessun atto e stato depositato.')
return { consegnabili, incomplete, promozioni_fallite: PROMOZIONI_FALLITE }

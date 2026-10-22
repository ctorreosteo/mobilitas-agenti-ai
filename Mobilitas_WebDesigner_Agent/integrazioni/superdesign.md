# Integrazione Superdesign

Superdesign genera una bozza HTML da un brief testuale. Nel laboratorio è servito come riferimento visivo per le landing più riuscite. È un servizio esterno a pagamento, a crediti.

## Installazione e accesso

- **Programma:** CLI `@superdesign/cli` 0.14.0, installata in locale da `tools/setup/installa.sh` in `tools/superdesign/node_modules`.
- **Lanciatore:** si usa solo `tools/superdesign/sd.sh`, che:
  - tiene configurazione e credenziali in `<lavoro>/.stato/superdesign/` (permessi 700), fuori dalla cartella dell'agente;
  - spegne la telemetria;
  - blocca `init`, che scriverebbe file di configurazione nel progetto;
  - lascia partire i comandi che possono consumare crediti solo con `integrazioni.superdesign.abilitato: true` **e** la variabile `SD_TETTO_CREDITI`;
  - li registra in `<lavoro>/.stato/superdesign-registro.log`.
- **Accesso:** lo fa una persona, non l'agente, con `tools/superdesign/sd.sh login`. Le credenziali non vanno mai copiate né spostate con il pacchetto.

## Comandi

| Comando | Costo | Uso |
|---|---|---|
| `sd.sh --version`, `--help` | gratuito | verifica |
| `sd.sh create-project --title "<titolo>" --no-open --json` | gratuito | un progetto per incarico |
| `sd.sh get-design --draft-id <id> --json` | gratuito | scarica l'HTML della bozza (`htmlContent`) |
| `sd.sh fetch-design-nodes --project-id <id> --json` | gratuito | elenco delle bozze di un progetto |
| `SD_TETTO_CREDITI=<n> sd.sh create-design-draft --project-id <id> --model <modello> -p "$(cat brief.txt)" --json` | **a crediti** | genera una bozza |
| `SD_TETTO_CREDITI=<n> sd.sh iterate-design-draft …` | **a crediti** | varianti o correzioni di una bozza |

Le opzioni esatte dei comandi si leggono con `sd.sh <comando> --help`, che è gratuito.

**Saldo** (`sd.sh generate-image … --json`). Nel laboratorio il saldo si leggeva gratis da un preventivo di immagine, senza mai eseguire `confirm-generation`. È un'abitudine non documentata da Superdesign: trattalo come comando a crediti (serve il tetto) e non confermare mai la generazione.

## Autorizzazione (obbligatoria, ogni volta)

Prima di ogni generazione chiedi al titolare, in un unico messaggio:

- che cosa genererai e con quale modello;
- **il costo atteso**, dai dati osservati qui sotto, perché Superdesign non dà preventivi per le bozze;
- il tetto che proponi;
- il saldo, se lo conosci.

Esempio: «1 bozza GPT-5.6 Sol, costo atteso 70–85 crediti, tetto 90: autorizzi?». Senza un sì esplicito non si genera. Se il costo previsto supera il tetto, ci si ferma.

**Costi osservati nel laboratorio (ottobre 2026, piano Pro):**

| Bozza | Crediti | Esito |
|---|---|---|
| GPT-5.6 Sol, pagina completa, brief di 6–13 kB | 67–80 | Bozze complete, le migliori come riferimento |
| Claude Sonnet 5, brief lungo | 12–21 | Spesso incompleta: solo le prime sezioni |
| Claude Sonnet 5 | 6 | In un caso pagina di rifiuto |
| Modello predefinito di allora (gemini-3.1-pro), piano gratuito | 18–25 | Un errore di tempo del server non ha consumato crediti |
| `iterate-design-draft --mode branch`, 2 varianti | 45 | |

Il costo sembra crescere con la lunghezza del brief. Dopo un errore del server, prima di riprovare controlla con `fetch-design-nodes` e con il saldo se la bozza esiste già, poi chiedi di nuovo.

## Brief

Modello: `templates/brief/prompt-superdesign.txt`. Regole:

- **Solo testo.** Mai foto, file del progetto o dati personali.
- **Foto come segnaposto:** `https://placehold.co/<L>x<A>/<fondo>/<testo>?text=<nome-file>`. Il server rifiuta i percorsi locali.
- **Testi esatti** di ogni sezione, con la frase «usa ESATTAMENTE questi testi, non inventare dati, recensioni, prezzi barrati, scarsità o scadenze».
- **Indicazioni visive:** palette con i ruoli, tipografia con misure mobile e desktop, griglia, composizione della prima schermata mobile e desktop, divieti contro i cliché (`regole/direzione-estetica.md`).
- **«Genera la pagina COMPLETA, tutte le N sezioni»**, con il codice compatto: niente SVG decorativi né librerie. Riduce le bozze tronche.

## Dopo la generazione

1. Salva la risposta JSON in `INC/bozze/` e l'HTML in `INC/bozze/<nome>.html`.
2. Prepara il visore:
   - `INC/visore/vendor` è già pronto (lo copia `tools/incarico/nuovo.sh`);
   - metti le foto reali, già ritagliate, in `INC/visore/foto/<nome-file>.jpg`, e le recensioni in `recensioni/`.
3. Localizza la bozza: `python3 -I tools/superdesign/localizza-bozza.py INC/bozze/<nome>.html INC/visore/<nome>.html`. Lo script sostituisce i segnaposto con le foto locali e Tailwind, Iconify e Montserrat con le copie locali.
4. Cattura: `tools/sito/avvia.sh INC --visore`, poi `node tools/playwright/cattura-bozza.cjs --incarico INC --pagina <nome>.html --prefisso bozza`.
5. **Confronta i testi della bozza con il brief:** le bozze possono inventare frasi, dati o recensioni. Nella landing si usano solo i testi approvati.
6. Mostra le catture al titolare, se la bozza deve essere approvata come riferimento.

## Licenze

- La CLI è MIT.
- L'uso del servizio segue i termini di Superdesign e il piano dell'account del titolare.
- Le bozze generate sono riferimenti di lavoro: la landing finale è scritta in React nel sito.

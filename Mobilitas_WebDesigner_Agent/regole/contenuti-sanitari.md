# Contenuti: verità, prudenza sanitaria, conversione

Mobilitas è uno studio sanitario (osteopatia, Torino). Ogni landing deve convertire ed essere credibile. Una frase non verificabile fa perdere più fiducia di quanta conversione porti.

## Dati: solo verificati

| Dato | Dove si verifica | Se non torna |
|---|---|---|
| Offerta (prezzo, durata, cosa comprende) | Codice del sito (pagine, popup di prenotazione, testi), con `grep` in sola lettura | Mostra le varianti trovate e chiedi quale usare |
| Numero di recensioni | Codice del sito; il titolare può decidere un valore diverso | Chiedi |
| Sedi, indirizzi, telefono, WhatsApp | Codice del sito (Footer, pagine dei servizi) | Chiedi |
| Qualifiche, anni di esperienza, team | Documentazione aziendale (`documentazione.cartella`) o titolare | Non scriverli |
| Recensioni e testimonianze | Solo screenshot reali presenti nel progetto; l'OCR locale (`tools/immagini/ocr.sh`) aiuta a trovarle per tema | Nessuna recensione |

Annota la fonte di ogni dato nel brief dell'incarico (modello `templates/brief/strategia-e-copy.md`, tabella «Verifica dei dati») e, come commento, accanto al dato nel file dei testi della landing.

## Mai inventare

Non si inventano:

- recensioni, testimonianze, nomi di pazienti, casi, statistiche, percentuali;
- risultati clinici, tempi di guarigione, garanzie («risolvi», «elimina», «per sempre»);
- prezzi barrati, sconti, scarsità («solo 15 posti»), scadenze, urgenze artificiali;
- qualifiche, premi, citazioni di medici o enti;
- fotografie: si usano solo foto reali dello studio o fornite dal titolare. Le immagini generate non vanno nelle landing.

Se un'informazione manca, si lascia un segnaposto visibile e marcato `.pm-verify`, e la si chiede.

## Prudenza sanitaria (scrittura)

**Formulazioni assolute da ammorbidire:**

| Invece di | Usa |
|---|---|
| «la maggior parte», «sempre» | «spesso», «in molti casi» |
| «sblocco», «rimettere a posto» | «mobilizzazione dolce», «lavoro su…» |
| «risolviamo» | «lavoriamo su», «ti aiutiamo a capire» |
| «senza farmaci» come alternativa al medico | «in affiancamento al tuo medico» |

**Altre regole di scrittura:**

- **Farmaci:** nessun nome commerciale. Non suggerire di sospendere terapie: si consiglia di parlarne con il medico.
- **Segnali d'allarme:** quando il tema li prevede (mal di testa, dolore toracico, formicolii, traumi…), una sezione sobria «Quando andare dal medico» è obbligatoria.
- **Obiettivi del percorso:** si presentano come obiettivi, non come garanzie. Per esempio: «Sono obiettivi, non garanzie: ogni persona è diversa».
- **Testimonianze sui risultati:** usarle in una comunicazione sanitaria va verificato rispetto alle regole della pubblicità sanitaria. In attesa della verifica:
  - si mostrano solo come screenshot;
  - si trascrivono solo frasi che non dichiarano un esito;
  - il punto va segnalato in consegna.

## Copy a risposta diretta (stile Dan Kennedy, versione sanitaria)

**Struttura che ha funzionato:**

1. promessa concreta, senza garanzia;
2. riconoscimento: l'utente si rivede nei sintomi e nelle scene quotidiane;
3. «hai già provato tutto, e aveva senso»;
4. il meccanismo spiegato semplice;
5. cosa succede nella prima visita;
6. obiettivi;
7. prove reali;
8. obiezioni e domande frequenti;
9. segnali medici;
10. chiusura con l'offerta e P.S.

**Tono:** caldo, concreto, in seconda persona, mai freddo-clinico e mai urlato. Frasi brevi; numeri veri in evidenza.

**Interazione utile, non decorativa.** Per esempio un autotest dei segnali con contatore e invito a prenotare dopo alcune risposte.

**Azioni:**

- una principale, la prima visita;
- una secondaria, il consulto telefonico gratuito, se esiste nel sito;
- il pulsante principale sta nella prima schermata anche a 375×667.

## Decisioni già prese dal titolare (al 19/10/2026)

Riconfermale se passano più di qualche settimana o se il codice del sito dice altro:

- **Recensioni:** «900+ recensioni Google». Le pagine del sito riportavano 850, una pagina 900; il titolare ha scelto 900+.
- **Offerta:** solo «Prima visita 49€ · circa 1 ora». Niente prezzo barrato (90€ compariva in una sola pagina) e niente «posti limitati».
- **Sedi:** due, San Donato (Via Peyron 54) e Crocetta (Via Lamarmora 35), come nella pagina Emicrania del sito.

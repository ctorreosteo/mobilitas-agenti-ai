# Il piano d'azione

Il piano è ciò che separa "ho capito il task" da "credo di aver capito il task". Nella lista HQ la specifica è un titolo: **il piano è il primo documento in cui il lavoro esiste davvero.**

---

## Il problema che il piano risolve

Un task reale, per intero:

> `Pagamenti - bug note che non si cancellano`

Quattro parole e nessun contesto. Domande senza risposta: quali note — quelle sul pagamento o quelle sul paziente? "Non si cancellano" in UI, o tornano dopo un refresh? Per tutti i ruoli? Da quando?

Se cominci a scrivere codice adesso, stai indovinando. Il piano è dove smetti di indovinare: leggi il codice, riproduci, e **scopri** la risposta invece di sceglierla.

---

## I cinque passi

### 1. Spremi il task

Titolo, descrizione, commenti, subtask, checklist, allegati, task collegati. Gli allegati contano: uno screenshot di un bug spesso è la specifica migliore che riceverai.

Aspettati poco. Se il task è solo un titolo, prendine atto in una riga e passa al passo 2 — non fabbricare contesto che non c'è.

### 2. Ricostruisci l'intento dal codice

**Questo è il passo che sostituisce la specifica mancante.**

Il titolo nomina quasi sempre un dominio e un sintomo. `Pagamenti` è un dominio: c'è `pagamento-details-sheet.tsx`, `pagamenti-list.tsx`, `pagamenti-service.ts`, e un `PagamentoController` con i suoi service. Vai a leggerli.

Cerca in entrambi i repo. Quando trovi il punto, chiedi:

- Come funziona **adesso**? Descrivilo in una frase.
- Cosa dovrebbe fare secondo il task?
- Il delta fra le due frasi **è** il lavoro.

**Cerca anche i fratelli morti.** Prima di introdurre un concetto o un nome nuovo, controlla se ne esiste già uno vicino — magari non più usato. Nel task 869cng430 il frontend conteneva rami per uno stato `SPOSTATA` in una decina di punti, mentre nel backend quel valore **non esisteva più**: residuo di uno stato rimosso. "Spostata" e "Rimandato" sono la stessa idea con due nomi, e aggiungendo il secondo accanto ai rami morti del primo il codice si ritrova con due vocaboli per un concetto solo.

```bash
grep -rn "<concetto vicino>" /Users/carlitos/mobilitas-frontend/src | head
```

Se trovi un fratello morto: o lo riusi, o dichiari in «Cosa NON faccio» che resta lì e perché.

**Se il task tocca un enum di dominio, leggi [ricetta-enum.md](ricetta-enum.md) prima di scrivere il piano.** È la classe di task che dimentica più pezzi, e contiene la verifica del vincolo `CHECK` a database — quella che alla prima esecuzione ha fatto bocciare il piano.

Se non trovi il dominio, il problema è di vocabolario: il task usa la parola del business, il codice quella del dominio tecnico. Cerca per stringhe UI italiane — le label sono in italiano e sono il ponte più veloce fra le due lingue.

### 2-bis. Se c'è di mezzo un servizio di terzi, cerca la documentazione di oggi

**Quello che sai delle API altrui è un ricordo, non un fatto.** La tua conoscenza si ferma a una certa data; le API dei vendor no. Un endpoint deprecato, un campo rinominato, un modello di autenticazione cambiato, un parametro diventato obbligatorio: sono tutte cose che accadono dopo la tua data di addestramento e che nessun file di questo repo può dirti.

È l'unica classe di informazione che **non si trova né nel codice né nei doc interni**, e per questo è l'unico caso in cui esci a cercare.

**Quando si applica.** Ogni volta che il task porta dentro **un software che non è nostro**. Sono due casi, e il secondo è quello che conta di più:

| Caso | Esempio | Dove sei |
|---|---|---|
| **Vendor che già usiamo** | «Qonto — i bonifici non si riconciliano» | Hai il nostro codice come rete: c'è un service, una config, una versione appuntata |
| **Vendor nuovo** | «Integrare un servizio di firma digitale», «mandare le notifiche su Telegram» | **Non hai niente.** Nessun codice nostro, nessuna versione, nessuna convenzione: solo la documentazione del vendor |

Il primo elenco — i ventuno vendor già in casa — sta nella matrice di `mobilitas-backend/docs/guides/INTEGRATIONS.md`. **Non è l'elenco di quando devi cercare: è solo l'elenco di quelli su cui parti avvantaggiato.**

Vale anche per una libreria di terzi che stai per aggiungere, o che stai per usare in un modo nuovo.

**Quando non si applica.** Un task che tocca solo codice nostro. Non cercare su internet come si scrive un `useEffect` o come funziona il soft delete di questo backend: quello sta nel codice, ed è più affidabile.

#### I tre passi, in quest'ordine

**1. Guarda cosa usiamo davvero, prima di cercare.** È il passo che salta la maggior parte degli errori. Trova la versione appuntata:

- backend: `mobilitas-backend/pom.xml` — le versioni sono esplicite, es. `google-api-services-calendar` a `v3-rev20250404-2.0.0`, `jjwt` a `0.11.5`;
- frontend: `mobilitas-frontend/package.json`;
- e la riga del vendor in `docs/guides/INTEGRATIONS.md`, che dice quali secret e quali config usiamo.

Cercare la documentazione dell'ultima versione e progettare su quella, mentre il `pom.xml` è fermo a due major indietro, produce un piano che **non compila**. Peggio di non aver cercato.

**2. Cerca la documentazione ufficiale corrente**, e cerca in particolare:

| Cosa | Perché conta |
|---|---|
| L'endpoint o il metodo che ti serve, **oggi** | Il nome può essere cambiato |
| **Deprecazioni e date di dismissione** | È l'informazione più preziosa: costruire su qualcosa che chiude fra tre mesi è lavoro da rifare |
| **Breaking change** fra la nostra versione e quella corrente | Dice se il piano deve includere un aggiornamento, o aggirarlo |
| Autenticazione, scope, permessi | Cambia più spesso di quanto sembri, e fallisce solo in produzione |
| Limiti di frequenza e quote | Un job che gira su tutti i pazienti li incontra, il tuo test manuale no |

Preferisci **sempre** la fonte ufficiale del vendor a un blog o a una risposta di forum. Un post del 2023 che spiega come si fa una cosa è esattamente il tipo di fonte che ti fa scrivere codice deprecato con sicurezza.

**3. Diffida di quello che leggi, quanto di quello che ricordi.** Se la documentazione online e il codice del repo si contraddicono, non hai una risposta: hai una **domanda**. Scrivila nel piano come tale. Può voler dire che siamo indietro, oppure che stai leggendo la doc di un'altra versione.

#### Se il vendor è nuovo, la ricerca è un'altra cosa

Qui non stai aggiornando un ricordo: stai **decidendo di far entrare un pezzo di software altrui** in un gestionale che tratta dati sanitari. La ricerca è la parte principale del piano, non un contorno.

**Prima domanda, e viene prima di tutte: ce l'abbiamo già?** Il gestionale parla già con ventuno servizi. Un task che dice «manda una notifica» non dice «aggiungi Twilio»: abbiamo già SMSHosting, Mailchimp, Gmail. Prima di introdurre un vendor, **cerca nella matrice se qualcosa di già in casa fa quel lavoro.**

Se un vendor esistente basta, usalo e scrivi nel piano che hai scartato l'alternativa nuova. Introdurre un fornitore è una **decisione di prodotto** — vale la regola delle ambiguità strutturali qui sotto: prendi la strada più corta e reversibile, e dichiara il bivio.

Se serve davvero qualcosa di nuovo, cerca **anche** questo, oltre ai punti della tabella sopra:

| Cosa | Perché può far fallire il task |
|---|---|
| **Esiste un'API pubblica?** Quale modello di auth? | Alcuni servizi non ne hanno, o la danno solo su piani alti |
| **Quale SDK, quale versione, è mantenuto?** | Una libreria ferma da tre anni è un debito che nasce già vecchio |
| **Costo e limiti del piano** | Un'integrazione che richiede un piano enterprise è un task diverso, e non lo decidi tu |
| **Dove vengono trattati i dati** — UE o extra-UE | Vedi qui sotto: è il punto che può fermare tutto |
| **Sandbox o ambiente di prova** | Senza, ogni verifica manuale tocca dati veri |

**Il punto che nessun altro task ha: i dati personali.** Questo backend ha un fascicolo privacy vero — registro dei trattamenti, DPIA, DPA, TIA per l'extra-UE — e la sua stessa documentazione dice cosa serve, nella «Checklist nuova integrazione» di `INTEGRATIONS.md`: service dedicato, properties e `env.example`, chiavi `config` e `CONFIG_KEYS`, sandbox per gli effetti irreversibili, aggiornamento di `INTEGRATIONS.md`, **e l'aggiornamento del fascicolo privacy se ci passano dati personali o sanitari.**

Quindi, nel piano, per un vendor nuovo:

- **di' esplicitamente quali dati gli arrivano** — nessuno, personali, o clinici;
- se sono personali o clinici, **dillo in evidenza e mettilo fra le cose che richiedono una decisione di Carlos**: un fornitore nuovo che tratta dati sanitari è un responsabile del trattamento nuovo, e questo non si risolve scrivendo codice;
- se il vendor è **extra-UE**, scrivilo. È la differenza fra una riga di config e una valutazione formale.

Non ti fermi comunque — pianifichi la strada più piccola e lo dichiari — ma questa è la cosa che deve saltare all'occhio nel report, non stare in fondo.

**Nota pratica:** il dominio di un vendor nuovo **non sarà fra quelli consentiti** in `.claude/settings.json`. Vale il ripiego descritto più sotto: usi quello che vedi dalla ricerca senza aprire la pagina, lo dichiari, e segnali il dominio nel report perché venga aggiunto.

#### Cosa finisce nel piano

Una sezione dedicata, con le **fonti citate e datate**. Senza date, fra un mese nessuno sa se quella riga era aggiornata.

```markdown
## Documentazione di terzi consultata
- **Qonto — API bonifici**, https://... (consultata il 2026-08-31)
  - Versione che usiamo: <dal pom/package.json, o "chiamate HTTP diritte">
  - Rilevante: il campo `X` è obbligatorio da giugno 2026; il nostro client non lo manda.
  - Deprecazioni: nessuna che riguardi questo endpoint.
```

Se hai cercato e **non hai trovato** niente di rilevante, scrivilo lo stesso in una riga: «cercata la doc Qonto, nessun cambiamento rilevante per questo endpoint». Vale quanto un ritrovamento — dice al revisore che il controllo è stato fatto, e distingue «non c'era niente» da «non ho guardato».

#### Se la rete non risponde, o il dominio non è consentito

I domini dei vendor del gestionale sono già autorizzati in `.claude/settings.json`, e la ricerca pure. Ma un vendor nuovo, o una redirezione su un host che non è in elenco, **chiederebbe un permesso** — e una domanda di permesso ferma la giornata esattamente come una domanda a Carlos.

Quindi, in quest'ordine: prova la ricerca; se un dominio non passa, **prendi quello che la ricerca stessa ti mostra** senza aprire la pagina, e nel piano scrivi che la fonte non è stata aperta per intero.

**Se non ottieni niente affatto**, non ti fermi e non tiri a indovinare: lo dichiari nel piano fra le assunzioni, con scritto che l'integrazione è progettata **sulla base di conoscenza potenzialmente non aggiornata**, e quali punti sarebbero da verificare. È un rischio che Carlos deve poter leggere nel report, non un motivo per bloccare la giornata.

E quando il dominio mancante è di un vendor che useremo ancora, **segnalalo nel report**: aggiungerlo ai permessi è una riga, e la volta dopo non si ripresenta.

### 3. Riproduci, se è un bug

Non progettare la cura di un male che non hai visto: la metà dei "bug" è un malinteso su come dovrebbe funzionare.

Se non riesci a riprodurlo, **dillo nel piano** con cosa hai provato. È un risultato — spesso significa che il bug dipende da dati o da un ruolo che non hai sottomano, e serve una domanda a Carlos, non un fix a caso.

### 4. Scrivi il piano

```markdown
## Task
<id> — <titolo> — <url ClickUp>

## Cosa ho capito
Una frase. Il problema o la funzionalità, in italiano, come lo spiegheresti a voce.

## Com'è adesso
Come si comporta oggi il codice, con i file che lo determinano.

## Cosa cambio
### Backend
- `path/File.java` — cosa e perché
### Frontend
- `path/file.tsx` — cosa e perché

## Ordine
1. …  2. …  3. …
Il backend di solito precede: il frontend consuma un contratto che deve già esistere.

## Come si verifica
Passi concreti nell'app. Non "testare che funzioni", ma:
apri X → filtra per Y → premi Z → deve succedere W.
Serve a Carlos per il collaudo manuale — non esistono test automatici.

## Documentazione di terzi consultata
Solo se il task tocca un vendor esterno. Fonte ufficiale, url, data di consultazione,
versione che usiamo noi, deprecazioni trovate. Se non c'era niente di rilevante,
scrivilo: «cercata, nessun cambiamento». Vedi il passo 2-bis.

## Assunzioni
- Ho assunto che «note» siano quelle sul pagamento, non sul paziente,
  perché il task sta nel dominio Pagamenti. Se è sbagliato, cambia il file X.

## Cosa NON faccio
Il confine. Quello che il task potrebbe far pensare e che non è compreso.

## Rischio di regressione
Cosa altro tocca il codice che sto cambiando. Serve al revisore regressioni.
```

### 5. Separa le assunzioni

Ogni buco del task che hai colmato con un'ipotesi va **scritto come ipotesi**, in `Assunzioni`, con la conseguenza se è sbagliata.

Un'assunzione nascosta in una frase affermativa è il modo standard di far passare inosservato un salto logico. E siccome nessuno approva il piano prima che tu parta, quella sezione è l'unico posto dove le tue ipotesi restano visibili: se non le scrivi lì, non le legge più nessuno.

---

## La scala delle ambiguità

Non tutte le ambiguità meritano la stessa reazione.

| Livello | Esempio | Cosa fai |
|---------|---------|----------|
| **Cosmetica** | Il testo esatto di un toast | Decidi, non menzionarlo nemmeno |
| **Locale** | Quale delle due liste note; se il campo è obbligatorio | Decidi, scrivi l'assunzione, vai avanti |
| **Strutturale** | "Sistemare gli enum duplicati": unificare a database o solo nascondere in UI? | **Scegli la strada più corta e reversibile**, dichiara il bivio nel piano e in Fase 6 |
| **Di prodotto** | Il task implica una decisione su come lavora il team | **Fai la scelta meno impegnativa**, e in Fase 6 scrivi che è una decisione da confermare |

Il criterio: *se sbaglio a indovinare, butto via un'ora o una settimana?* Un'ora la rischi. Una settimana no.

**In nessuna delle quattro righe ti fermi a chiedere.** Decidi sempre — cambia solo quanto lo dichiari.

Nelle prime due decidi e vai avanti senza nemmeno menzionarlo. Nelle ultime due il criterio è **la reversibilità**: fra due letture, prendi quella che impegna di meno — la più piccola, quella che non tocca lo schema né i dati, quella che si disfa in un pomeriggio.

Poi **rendi visibile il bivio**: quale lettura hai preso, quale hai scartato, e cosa comporterebbe l'altra. Va nel piano e va ripetuto in Fase 6.

Il ragionamento dietro: se indovini, ottimo. Se sbagli, hai speso un pomeriggio invece di due settimane, e Carlos scopre il bivio leggendo il report — mentre fermarsi a chiedere avrebbe bloccato la giornata su una domanda che forse non serviva.

Errore da evitare in entrambe le direzioni: fermarsi vanifica l'autonomia che ti è stata data; scegliere la strada lunga e irreversibile su un'ambiguità vera è consegnare due settimane di lavoro sbagliato con sicurezza.

---

## Verifica quello che puoi verificare, invece di assumerlo

Il revisore boccia le assunzioni che il codice — o il database — potevano smentire in due minuti. È il rilievo più frequente, e il più facile da evitare.

Alla prima esecuzione il piano affermava «estendere l'enum è sicuro, nessuna migrazione serve». Era **falso**, e bastava una query per scoprirlo: il vincolo `CHECK` esisteva. Quell'affermazione era scritta come fatto, non come ipotesi, e sarebbe passata in produzione.

Regola pratica: prima di scrivere nel piano una frase che comincia con «non serve», «è sicuro», «è già gestito» — **vai a verificarla**. Hai a disposizione i due repo, i doc, e il database (vedi [verifiche.md](verifiche.md)). Se la verifichi, scrivila come fatto e cita la prova. Se non puoi verificarla, scrivila fra le assunzioni.

## Il piano si salva, non si fa approvare

**Non aspettare nessun via libera.** Scrivi il piano, salvalo, mostrane un riassunto e passa subito allo sviluppo.

```bash
mkdir -p /tmp/dev-hq-piani
# il piano va in /tmp/dev-hq-piani/<task-id>.md
```

Il file su disco non è burocrazia: ha **due lettori veri**.

- **Il revisore logica**, in Fase 4, lo legge per giudicare se hai fatto la cosa giusta. È il suo metro: senza, può dirti solo se il codice è scritto bene, non se è il codice che serviva.
- **Carlos**, in Fase 6, ci cerca le assunzioni. È lì che si scopre in trenta secondi se una era sbagliata — a lavoro fatto, non prima.

Se durante lo sviluppo il piano cambia, **aggiorna il file**. Un piano fermo a un'idea che hai già abbandonato fa giudicare il revisore logica sul metro sbagliato, ed è peggio che non averlo.

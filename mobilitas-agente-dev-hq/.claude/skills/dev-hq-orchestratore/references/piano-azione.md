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

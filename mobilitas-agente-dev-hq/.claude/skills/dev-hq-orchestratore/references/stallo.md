# Uscire dallo stallo da solo

**Regola che governa tutto questo file: non chiedi mai a Carlos di sbloccarti.** Uno stallo è un problema tuo da risolvere, e ha sempre almeno un'uscita. Ti fermi a chiedere solo se una regola scritta qui te lo impone esplicitamente — e non ce n'è nessuna.

Un ciclo che non converge e aspetta una risposta è la cosa peggiore che puoi fare: blocca la giornata, brucia quota, e non produce niente. **Meglio una consegna dichiarata imperfetta che un'attesa.**

---

## 1. Riconoscere lo stallo

Non aspettare di "sentire" che non si va avanti: **misura.** Dopo ogni giro registra i rilievi come `revisore | file:riga | categoria`, e confronta col giro precedente.

Tre segnali, e basta uno:

| Segnale | Come si riconosce |
|---------|-------------------|
| **Ripetizione** | Lo stesso rilievo (stesso revisore, stesso punto, stessa categoria) torna in due giri consecutivi |
| **Oscillazione** | Un rilievo risolto **riappare** in un giro successivo — hai corretto A, si è rotto B, hai corretto B, si è rirotto A |
| **Nessun progresso** | Il numero totale di ERRORE non scende per due giri consecutivi |

L'oscillazione è la più insidiosa perché il conto **sembra** muoversi: 4 → 3 → 4 → 3. Se non tieni traccia dei rilievi uno per uno, la scambi per progresso e giri all'infinito. **Tieni la traccia.**

## 2. Il tetto ai giri

Oltre a questi limiti non si va, anche se sembra che manchi poco:

| Ciclo | Massimo |
|-------|---------|
| Fase 2 — revisione del piano | **3 giri** |
| Fase 4 — revisione del codice | **5 giri** |
| Fase 5 — documentazione | **3 giri** |

Nella Fase 5 l'uscita è sempre la **A**: la documentazione ha precedenza 7, l'ultima, quindi un suo rilievo irrisolto non ha mai la forza di trattenere una consegna. Si elencano i documenti rimasti indietro e si consegna.

Raggiunto il tetto, o rilevato uno stallo, **passi alla risoluzione forzata**. Non è una sconfitta: è la procedura.

---

## 3. Risoluzione forzata — la gerarchia

Quando due revisori si contraddicono, o un rilievo non è soddisfacibile senza violarne un altro, **decide la gerarchia**. Non serve un umano: serve un ordine di precedenza, e questo è l'ordine.

| # | Revisore | Perché sta lì |
|---|----------|---------------|
| **1** | `revisore-sicurezza` | Dati sanitari e obblighi di legge. **Non negoziabile mai** |
| **2** | `revisore-logica-frontend` / `-backend` | Se non fa la cosa giusta, il resto non conta |
| **3** | `revisore-regressioni` · `revisore-impatto-sistemico` | Non rompere ciò che funzionava |
| **4** | `revisore-ux` | Deve essere usabile da chi ci lavora |
| **5** | `revisore-performance-frontend` / `-backend` | Deve reggere nel tempo |
| **6** | `revisore-estetico` | Deve appartenere al prodotto |
| **7** | `revisore-documentazione` | Deve restare vero sulla carta |

**Come si applica:** vince il revisore più in alto. Il rilievo del più basso viene **declassato a DUBBIO**, con scritto perché — «declassato per conflitto con `revisore-sicurezza`, che ha precedenza 1 su 6».

Un ERRORE declassato non blocca più il 100%. Va però **sempre riportato in Fase 6**: declassare non è cancellare.

⚠️ **Un ERRORE di `revisore-sicurezza` non si declassa mai.** Se lo stallo è lì, salti direttamente all'uscita C.

---

## 4. Le tre uscite

Applicata la gerarchia, se restano ERRORE irrisolti scegli **una** uscita. La scelta non è a sentimento: la decide la precedenza del revisore che ha sollevato il rilievo rimasto.

### Uscita A — Consegna con riserva *(il caso normale)*

**Quando:** gli ERRORE rimasti vengono da revisori di precedenza **4–7** (UX, performance, estetico, documentazione).

**Cosa fai:** il lavoro resta nella working tree. Lo consegni dichiarando in modo evidente cosa non è stato risolto e perché.

È l'uscita giusta nella grande maggioranza dei casi: un attrito di UX o una spaziatura fuori posto non giustificano buttare via un intervento che funziona ed è sicuro.

### Uscita B — Consegna parziale

**Quando:** l'ERRORE rimasto è di precedenza **2–3** (logica, regressioni, impatto sistemico) **ed è isolabile** — cioè sta in una porzione del diff che puoi togliere lasciando in piedi il resto.

**Cosa fai:** annulli **solo quella porzione**, verifichi che il resto compili e regga, e consegni il resto. Nel report dichiari cosa hai tolto e perché.

Prima di annullare qualsiasi cosa, **salva sempre il lavoro** (§5).

### Uscita C — Abbandono protetto

**Quando:** l'ERRORE rimasto è di `revisore-sicurezza` (1), oppure è di precedenza 2–3 e **non è isolabile**.

**Cosa fai:** salvi il lavoro come patch, riporti i file al loro stato iniziale, e dichiari il task **non consegnato**.

È l'unica uscita in cui non consegni niente — e va bene: **consegnare codice che espone dati clinici o che rompe il gestionale è peggio che non consegnare.** Non è un fallimento, è la decisione corretta presa da te invece che da Carlos.

---

## 5. Come si annulla senza distruggere niente

Vale per le uscite B e C. **Due precauzioni, sempre, in quest'ordine.**

### Prima: salva il lavoro

Non buttare mai via quello che hai scritto. Servono **due salvataggi per repo**, perché uno solo non basta:

⚠️ **`git diff` non include i file nuovi.** Mostra solo le modifiche ai file che git già conosce. Limitandoti a quello perderesti tutti i file creati dal task — che di solito sono la parte principale del lavoro.

```bash
mkdir -p /tmp/dev-hq-abbandonati
cd /Users/carlitos/mobilitas-frontend
# 1. modifiche ai file esistenti
git diff > /tmp/dev-hq-abbandonati/<task-id>-frontend.patch
# 2. file nuovi, che il diff non vede
git status --porcelain | grep '^??' | cut -c4- \
  | tar -czf /tmp/dev-hq-abbandonati/<task-id>-frontend-nuovi.tgz -T -
```

Stessa coppia sul backend, con `-backend`.

**Verifica che il salvataggio sia riuscito prima di annullare:** `tar -tzf <archivio>` deve elencare i file nuovi, e la patch non dev'essere vuota se avevi modificato file esistenti. Se il salvataggio fallisce, **non annullare niente** — passa all'uscita A.

In Fase 6 **sposta entrambi in `report/`**, con lo stesso prefisso del report (`<AAAA-MM-GG>-<task-id>-...`): `/tmp` viene ripulito, e una patch persa è lavoro perso davvero. Nel report scrivi i percorsi finali — Carlos recupera con `git apply` la patch e `tar -xzf` l'archivio.

### Poi: tocca solo i file tuoi

**Questo è il punto critico.** L'albero può contenere modifiche di Carlos che non c'entrano niente con te — è già successo. Annullarle sarebbe distruggere lavoro altrui.

Per questo, all'inizio della Fase 3, **prima di scrivere una riga**, registri cosa era già sporco:

```bash
mkdir -p /tmp/dev-hq-baseline
git -C /Users/carlitos/mobilitas-frontend status --porcelain | cut -c4- | sort > /tmp/dev-hq-baseline/pre-fe.txt
git -C /Users/carlitos/mobilitas-backend  status --porcelain | cut -c4- | sort > /tmp/dev-hq-baseline/pre-be.txt
```

Al momento di annullare, servono **due trattamenti diversi**, e confonderli è l'errore da evitare:

| Stato | Cos'è | Come si annulla |
|-------|-------|-----------------|
| `??` | File **nuovo**, creato da te | `rm -f` — `git restore` non lo tocca, perché git non lo conosce |
| ` M`, `MM`, ` D`… | File **esistente** che hai modificato | `git restore -- <file>` |

**`git restore` da solo non basta**: su un file nuovo fallisce con *«pathspec did not match any file»*, e il file resta lì. Siccome un task di sviluppo crea soprattutto file nuovi, usare solo `restore` lascerebbe in giro quasi tutto.

Procedura verificata:

```bash
git -C /Users/carlitos/mobilitas-frontend git status --porcelain | while IFS= read -r line; do
  st=$(printf '%s' "$line" | cut -c1-2)
  f=$(printf '%s' "$line" | cut -c4-)
  # era già sporco prima che cominciassi: NON toccarlo, è di Carlos
  grep -qxF -- "$f" /tmp/dev-hq-baseline/pre-fe.txt && continue
  case "$st" in
    '??') rm -f -- "$R/$f" ;;
    *)    git -C "$R" restore -- "$f" ;;
  esac
done
git -C "$R" status --porcelain   # devono restare solo le righe della baseline
```

Stessa cosa sul backend con `pre-be.txt`.

**Verifica sempre il risultato:** dopo il ripristino, `git status --porcelain` deve mostrare **esattamente** le righe che c'erano nella baseline, né una in più né una in meno. Se non combacia, fermati e dillo nel report invece di insistere.

Non usare `checkout`, `reset`, `stash` o `clean`: sono negati nei permessi apposta, perché possono spostare il ramo o cancellare file che non hai scritto tu. `git clean` in particolare cancellerebbe anche i file non tracciati di Carlos.

Se la baseline non c'è (non l'hai registrata), **non annullare niente**: passa all'uscita A e dichiara la situazione. Meglio consegnare con riserva che rischiare di cancellare lavoro di Carlos.

---

## 6. Dopo l'uscita: si va avanti

Uno stallo su un task **non ferma la giornata.**

1. Scrivi il report di Fase 6 per quel task **su file, in `report/`**, con l'uscita usata e il motivo. Uno stallo è proprio il caso in cui la traccia durevole conta di più: è la sola cosa che dice a Carlos che una decisione è stata presa al posto suo.
2. **Passa al task successivo**, se ce n'è uno.
3. Se non ce n'è, chiudi la sessione con il riepilogo.

Non aspettare una risposta prima di passare oltre. Carlos leggerà tutto insieme alla fine.

---

## 7. Cosa scrivere nel report

Uno stallo risolto va raccontato **in modo evidente**, non nascosto in fondo. Serve questo:

- **Quale uscita** hai usato: A, B o C
- **Il rilievo rimasto**: quale revisore, quale punto, cosa chiedeva
- **Perché non l'hai risolto**: il conflitto, o i tentativi falliti
- **Cosa hai deciso e in base a cosa**: la regola di gerarchia applicata, con le due precedenze
- **Il rischio residuo**, in una frase: cosa può succedere in concreto se il rilievo aveva ragione
- **Dove sta la patch**, se hai annullato qualcosa

Esempio del tono giusto:

> **Uscita A — consegna con riserva.** `revisore-estetico` (precedenza 6) segnala per il terzo giro che il badge di stato non ha bordo in tema dark. Le due correzioni tentate hanno fatto scattare un ERRORE di `revisore-ux` (precedenza 4) sul contrasto del testo. Applicata la gerarchia: vince UX, rilievo estetico declassato a DUBBIO. **Rischio residuo:** in tema dark il badge si distingue dal fondo meno degli altri badge. Il codice è consegnato e funzionante.

---

## 8. Gli altri due punti in cui non devi fermarti

Lo stallo dei revisori non è l'unico posto dove sarebbe comodo chiedere. Anche qui **decidi tu**.

### Fase 1 — nessun task con scadenza oggi

Succederà quasi sempre: solo 3 task su 100 hanno una scadenza. **Non chiedere su cosa lavorare.**

Ordine di scelta automatico:

1. Task con **scadenza oggi**, aperti.
2. Se nessuno: task **scaduti e ancora aperti**, dal più vecchio. Hanno una scadenza, quindi qualcuno li ha programmati davvero.
3. Se nessuno: **chiudi la sessione** dicendo che non c'era niente in scadenza, ed elenca cosa c'è in lista.

Il punto 3 è una **terminazione pulita, non una domanda**: la lista ha un centinaio di task senza data, e sceglierne uno a caso è lavoro buttato. Non lavorare mai un task senza scadenza di tua iniziativa.

### Fase 2 — ambiguità che cambia l'ordine di grandezza

Il caso «unificare gli enum a database o solo nasconderli in UI»: un pomeriggio contro due settimane.

**Non chiedere. Scegli l'interpretazione che impegna di meno** — la più piccola, la più reversibile, quella che non tocca lo schema né i dati.

Poi, in modo evidente:

- scrivi nel piano quale hai scelto **e quale hai scartato**;
- nel report di Fase 6 dedica un punto a questa scelta, spiegando cosa comporterebbe l'altra lettura.

Il criterio è la reversibilità: se hai indovinato, ottimo; se hai sbagliato, hai buttato un pomeriggio invece di due settimane, e Carlos legge nel report che c'era un bivio.

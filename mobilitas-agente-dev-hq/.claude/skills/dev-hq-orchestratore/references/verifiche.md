# Le verifiche meccaniche — e come leggerle

## Il fatto da sapere prima di lanciarle

**I gate del frontend sono già rossi su albero pulito.** Misurato su `main` senza modifiche:

| Comando | Esito su albero pulito |
|---------|------------------------|
| `npm run typecheck` | **318 errori** (301 fuori da `src/test/`, 17 dentro) |
| `npm run lint` | **894 problemi** — 785 errori, 109 warning |
| `./mvnw -q -DskipTests compile` | **pulito** |

La maggior parte sono `TS6133` (import dichiarati e mai usati) e regole ESLint accumulate nel tempo. `src/test/` aggiunge i suoi perché importa `vitest`, che non è installato.

**Conseguenza operativa:** «ho lanciato typecheck e ci sono errori» non è un rilievo. Se un revisore riportasse l'output grezzo, produrrebbe ~1200 falsi positivi a ogni revisione, e alla terza volta nessuno leggerebbe più i report.

La domanda giusta non è *«ci sono errori?»* ma **«ce ne sono di nuovi, causati da questo diff?»**

---

## Il metodo: fotografa prima, confronta dopo

L'orchestratore controlla i tempi, quindi può fare la cosa semplice: **registrare la linea di base quando l'albero è ancora pulito**, prima di scrivere una riga.

### Prima di sviluppare (fine Fase 2, prima della Fase 3)

```bash
BASE=/tmp/dev-hq-baseline
mkdir -p $BASE

( cd /Users/carlitos/mobilitas-frontend && npm run typecheck 2>&1 | grep -E '^src/' | sort > $BASE/typecheck.txt )
( cd /Users/carlitos/mobilitas-frontend && npm run lint 2>&1 | grep -E '^\s+[0-9]+:[0-9]+' | sort > $BASE/lint.txt )
( cd /Users/carlitos/mobilitas-backend  && ./mvnw -q -DskipTests compile 2>&1 | sort > $BASE/compile.txt )

# e i file gia' sporchi, per non toccare mai il lavoro di Carlos in un eventuale rollback
git -C /Users/carlitos/mobilitas-frontend status --porcelain | cut -c4- | sort > $BASE/pre-fe.txt
git -C /Users/carlitos/mobilitas-backend  status --porcelain | cut -c4- | sort > $BASE/pre-be.txt

wc -l $BASE/*.txt
```

Fallo **una volta per sessione**, con l'albero pulito. Se l'albero non è pulito quando parti, dillo: la linea di base include già modifiche non tue, e va detto nel report.

### Dopo aver sviluppato

**Confronta per testo, non per numero di riga.** Se il diff sposta delle righe, tutti gli errori sotto il punto di modifica cambiano numero e `comm` li segnala come nuovi: sono falsi positivi.

Misurato sul task 869cng430: il confronto per riga dava **3 errori nuovi, di cui 2 falsi**. Il confronto per testo ne dava **1 — quello vero**.

```bash
BASE=/tmp/dev-hq-baseline

( cd /Users/carlitos/mobilitas-frontend && npm run typecheck 2>&1 | grep -E '^src/' | sort > /tmp/tc-dopo.txt )

echo "=== ERRORI TYPECHECK NUOVI ==="
comm -13 <(sed -E 's/\([0-9]+,[0-9]+\)//' $BASE/typecheck.txt | sort) \
         <(sed -E 's/\([0-9]+,[0-9]+\)//' /tmp/tc-dopo.txt  | sort)
```

Il `sed` toglie `(riga,colonna)` e lascia `file: messaggio`: due errori identici in posizioni diverse si annullano, e resta solo ciò che il diff ha davvero introdotto.

Per il **lint**, che non ha un formato altrettanto regolare, confronta il **conteggio per regola**:

```bash
( cd /Users/carlitos/mobilitas-frontend && npm run lint 2>&1 | grep -E '^\s+[0-9]+:[0-9]+' \
  | awk '{print $NF}' | sort | uniq -c | sort -rn > /tmp/lr-post.txt )
awk '{print $NF}' $BASE/lint.txt | sort | uniq -c | sort -rn > /tmp/lr-pre.txt
diff /tmp/lr-pre.txt /tmp/lr-post.txt && echo "IDENTICO — nessun problema di lint nuovo"
```

Se il conteggio per regola è identico, non hai introdotto niente: le differenze di riga sono spostamenti.

Backend, dove la compilazione parte pulita e ogni output è tuo:

```bash
( ./mvnw -q -DskipTests compile )
```

**Quando resta un errore vero, cerca la causa dove non appare.** Sempre sul task 869cng430, l'unico errore reale diceva *«questo confronto non ha sovrapposizione»* in un componente — ma la causa era una **union di tipo in un service**, che non era stata estesa. Il punto in cui TypeScript protesta è spesso l'ultimo anello, non il primo.

### Se la linea di base non c'è

Un revisore che arriva a modifiche già fatte non ha la fotografia. Allora:

1. **Filtra ai soli file toccati dal diff.** Un errore in un file che non hai aperto non è tuo.

   ```bash
   cd /Users/carlitos/mobilitas-frontend
   git diff --name-only > /tmp/toccati.txt
   npm run typecheck 2>&1 | grep -E '^src/' | grep -Ff /tmp/toccati.txt
   ```

2. **Per ogni errore residuo, decidi se il diff lo può aver causato.** Un `TS6133` su un import che il diff non ha toccato è pregresso. Un errore di tipo su una riga che il diff ha scritto è tuo.

3. Nel dubbio, marca **DUBBIO** e dillo. Non marcare ERRORE un problema che potrebbe essere lì da mesi.

---

## Il database si può interrogare

Non è un dettaglio operativo: è uno strumento di verifica che cambia il tipo di domande a cui puoi rispondere **prima** di scrivere codice.

Postgres gira in un container e risponde:

```bash
docker exec postgres psql -U admin -d mobilitashq -tAc "SELECT 1;"
```

Serve per le domande che il codice non risponde: quali vincoli `CHECK` esistono su una colonna, che valori ci sono davvero a database, se un dato reale rispetta l'assunzione che stai facendo.

```bash
# i vincoli CHECK di una tabella
docker exec postgres psql -U admin -d mobilitashq -tAc \
  "SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint
   WHERE conrelid='visite'::regclass AND contype='c';"
```

**Prova le migrazioni in una transazione che poi annulli** — verifichi davvero senza toccare i dati:

```bash
docker exec -i postgres psql -U admin -d mobilitashq <<'SQL'
BEGIN;
-- ...la migrazione...
SELECT pg_get_constraintdef(oid) FROM pg_constraint WHERE conname='...';
ROLLBACK;
SQL
```

**Solo lettura e transazioni annullate.** Niente `INSERT`, `UPDATE`, `DELETE` o DDL permanente sul database di sviluppo: contiene dati veri e non è tuo da modificare.

## Il backend è la vera rete

`./mvnw -q -DskipTests compile` è **pulito** sul backend. Vuol dire che lì qualsiasi output è un segnale vero: un errore di compilazione dopo il tuo diff è tuo, senza bisogno di confronti.

Trattalo come tale: se il backend non compila, è **ERRORE**, viene prima di ogni altro rilievo e si corregge subito.

---

## Cosa questi comandi non dicono

Anche a gate verdi, restano invisibili:

- Un colore che sparisce in un tema
- Un flusso senza stato di errore
- Un chiamante non aggiornato che compila lo stesso
- Un campo DTO rinominato che il frontend legge come `undefined`
- Un enum esteso da un lato solo

`typecheck` verifica che i tipi tornino **dentro** un repo. Non attraversa il confine fra i due, e non sa niente di semantica.

**Non esistono test automatici** — 0 file di test nel backend, Vitest non installato nel frontend. Quello che le macchine non vedono lo vedono solo i revisori leggendo, e Carlos collaudando a mano. Per questo la Fase 6 deve sempre contenere i passi di verifica manuale.

---

## `src/test/` — non gira, ma si legge

I file in `src/test/` importano `vitest`, che non è nelle dipendenze e non ha script `test`. Non sono eseguibili.

Sono però **specifiche scritte da chi conosceva il dominio**: cache osteopati, integrazione spese, placeholder messaggi, WhatsApp, orario fine visita, stanze default, update visite, reset password.

Se il diff tocca uno di quei domini, apri il test corrispondente e verifica **a mano** che lo scenario descritto valga ancora. È la cosa più vicina a una suite di regressione che questo repo possieda.

# Ricetta: aggiungere un valore a un enum di dominio

Sembra il task più semplice che esista — una riga in un `enum` — ed è invece quello che si dimentica più pezzi. Ricavata dal task **869cng430 "Aggiungere visita rimandata"**, dove il revisore del piano ha bocciato la prima stesura e i punti mancanti erano sei.

Usala quando il task dice «aggiungere uno stato/tipo/categoria», o quando il piano tocca un `enum` in `models/`.

---

## Il punto che si dimentica sempre: il vincolo a database

**Prima di scrivere il piano**, controlla se la colonna ha un `CHECK`.

Lo schema di questo progetto è nato da Hibernate `ddl-auto`, che genera un vincolo `CHECK` con l'elenco dei valori ammessi su ogni colonna `@Enumerated(EnumType.STRING)`. Quel vincolo **non è definito da nessuna migrazione**: esiste solo nel database.

```bash
docker exec postgres psql -U admin -d mobilitashq -tAc \
  "SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint
   WHERE conrelid='<tabella>'::regclass AND contype='c';"
```

Se il vincolo c'è e non contiene il valore nuovo, **serve una migrazione Flyway**. Se non ne aggiungi una:

| Ambiente | `ddl-auto` | Cosa succede |
|----------|-----------|--------------|
| local · dev · uat | `update` | Non riscrive i CHECK esistenti — ma spesso non te ne accorgi subito |
| **prod** | **`validate`** | Non tocca né verifica i CHECK: l'app parte, e **il primo salvataggio del valore nuovo fallisce** |

È il difetto peggiore possibile: passa ogni collaudo e si rompe solo dai clienti.

Il modello da copiare è `V245__add_sdd_to_acquisti_metodo_pagamento_check.sql`:

```sql
ALTER TABLE <tabella> DROP CONSTRAINT IF EXISTS <nome_vincolo>;
ALTER TABLE <tabella>
    ADD CONSTRAINT <nome_vincolo>
    CHECK (<colonna>::text = ANY (ARRAY[ ...tutti i valori, incluso quello nuovo... ]));
```

Usa il **nome reale** del vincolo letto dal database, altrimenti il `DROP ... IF EXISTS` è un no-op silenzioso e l'`ADD` fallisce per duplicato. Numera la migrazione dopo l'ultima presente (`ls src/main/resources/db/migration/ | sort -V | tail -1`).

**Provala prima di consegnare**, dentro una transazione che poi annulli — così verifichi davvero senza toccare i dati:

```bash
docker exec -i postgres psql -U admin -d mobilitashq <<'SQL'
BEGIN;
-- ...la migrazione...
SELECT pg_get_constraintdef(oid) FROM pg_constraint WHERE conname='<nome_vincolo>';
ROLLBACK;
SQL
```

---

## L'elenco dei posti da toccare

Un enum di dominio è duplicato in molti più punti di quanti il nome suggerisca. **Cercali tutti prima di scrivere il piano**, non durante lo sviluppo.

### Backend

1. **L'enum** — spesso annidato nell'entity (es. `Visita.StatusVisita`), non in un file suo. Cercalo con `grep -rn "enum <Nome>" src/main/java`.
2. **La migrazione Flyway** per il CHECK (sopra).
3. **`EnumController`** — attenzione: gli elenchi serviti alla UI sono **scritti a mano**, non derivati dall'enum. Aggiungere il valore all'enum **non** lo fa comparire nel menu.
4. **Le query che ragionano per esclusione.** Sono il vero rischio: una allowlist ignora il valore nuovo, una **denylist lo include senza che nessuno l'abbia deciso**.
   ```bash
   grep -rn "getStatus.*() *!=\|statusX <>\|NOT IN" src/main/java --include='*.java'
   ```
   Per ognuna chiediti: *il valore nuovo deve stare dentro o fuori?* È una domanda di dominio, e va nel piano come assunzione.
5. **I job schedulati** che filtrano su quel campo.
6. **`docs/reference/DATABASE_DOCUMENTATION.md`**, che elenca i valori.

### Frontend

7. **Le union di tipo TypeScript** — di solito nei service (es. `visite-service.ts`), spesso **duplicate due volte nello stesso file**. Se le dimentichi, TypeScript segnala l'errore in un punto lontano e fuorviante: «questo confronto non ha sovrapposizione». La causa non è dove appare l'errore.
8. **Gli array di default hardcoded** nei componenti (filtri, opzioni, fallback per quando l'API non risponde).
9. **I badge**: label **e** colore, in **ogni** file che li disegna. Sono tanti e sparsi — nel caso visite erano sei file.
10. **Le catene di colore nei dettagli**, che spesso sono `if/else` o ternari annidati con fallback vuoto: il valore nuovo esce **senza stile** invece che sbagliato, quindi non lo noti guardando di fretta.
11. **`docs/`** — cataloghi e schede che elencano i valori.

### La ricerca che li trova

Prendi un valore **già esistente** dello stesso enum e cercalo ovunque: dove compare quello, deve comparire il tuo.

```bash
grep -rn "VALORE_ESISTENTE" /Users/carlitos/mobilitas-backend/src/main/java
grep -rn "VALORE_ESISTENTE" /Users/carlitos/mobilitas-frontend/src
```

È il modo più affidabile di costruire l'elenco: molto meglio che ragionare su dove *dovrebbe* essere.

---

## Prima di dare un nome al valore nuovo: cerca i fratelli morti

Nel task 869cng430 il frontend conteneva già rami per uno stato **`SPOSTATA`** — badge, label, union di tipo, una decina di punti — che nel **backend non esiste più**: residuo di uno stato rimosso.

"Spostata" e "Rimandato" sono la stessa idea con due nomi. Aggiungendo il secondo accanto ai rami morti del primo, il codice si ritrova con due vocaboli per un concetto solo, e chi legge domani non sa quale sia vivo.

Quindi, prima di scegliere il nome:

```bash
grep -rn "<concetto simile>" /Users/carlitos/mobilitas-frontend/src | head
```

Se trovi un fratello morto, mettilo nel piano: o lo riusi, o dichiari esplicitamente in «Cosa NON faccio» che resta lì e perché.

---

## Il collaudo minimo

1. Il valore **compare nel menu** (dipende dal punto 3, non dall'enum).
2. **Si salva senza errori a database** — è il punto che smaschera il CHECK mancante.
3. Il **badge** ha label e colore in **tutti e tre i temi**.
4. Compare nei **filtri** — con i filtri azzerati: quelli salvati in `localStorage` congelano la lista vecchia e ti fanno leggere un falso negativo.
5. Le **query per esclusione** del punto 4 si comportano come deciso nel piano.

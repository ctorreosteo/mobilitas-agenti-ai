---
description: Ciclo completo — fascicolo, strategia, atto con tutti i livelli di revisione, penale, collaudo
---

Esegui l'intero ciclo difensivo, nell'ordine, senza saltare passaggi.

1. **`/fascicolo`** — fatti, documenti, cronologia, buchi probatori, fronte penale.
2. **`/strategia`** — i nove blocchi, con il caso avversario scritto prima delle leve.
3. **`/atto`** — redazione e sei livelli di revisione fino al collaudo.
4. **`/penale`** — esposizione, coordinamento, regole per il cliente.
5. **`/udienza`** — se c'è una data fissata.

## Controlli obbligatori prima di consegnare

```bash
# le protezioni funzionano?
./scripts/test-hooks.py

# ogni citazione dell'atto finale è verificata?
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_citazioni.py \
  <v5> <v7> --registro fascicolo/_dati/registro-fonti.md \
  --delta-min -3 --delta-max 5 --min-identita 60 --passaggio LINGUA
```

**Zero bloccanti, o non si consegna.** Non esiste il «depositabile con riserva».

E un controllo che nessuno script può fare: **guarda sul disco che i file ci siano.** Gli agenti
riferiscono, non provano.

## Riepilogo finale all'utente

1. **Cosa si chiede**, in elenco numerato, nella forma in cui sta nell'atto.
2. **Cosa è provato e cosa no**: tabella per etichetta.
3. **Cosa manca**, con priorità e scadenza. Le voci che il tempo rende impossibili per prime.
4. **L'esposizione penale**, e le regole immediate per il cliente.
5. **Le domande al cliente**, numerate.
6. **L'esito del collaudo**, con i numeri.
7. **Il promemoria**: questo materiale va rivisto, sottoscritto e depositato da un avvocato
   iscritto all'albo. Nessun atto è stato depositato.

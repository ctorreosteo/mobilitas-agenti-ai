---
description: Ciclo completo — fascicolo, strategia, atto con tutti i livelli di revisione, penale, collaudo
---

Esegui l'intero ciclo difensivo, nell'ordine, senza saltare passaggi.

1. **`/fascicolo`** — fatti, documenti, cronologia, buchi probatori, fronte penale.
2. **`/strategia`** — i nove blocchi, con il caso avversario scritto prima delle leve.
3. **`/atto`** — redazione e sei livelli di revisione fino al collaudo.
4. **`/penale`** — esposizione, coordinamento, regole per il cliente.
5. **`/accordo`** — la proposta conciliativa. Si costruisce **prima** dell'udienza, non dopo che è
   andata male: portarne una ragionevole è quasi sempre conveniente, e in molti casi diventa il
   provvedimento.
6. **`/udienza`** — se c'è una data fissata.
7. **`/verifica`** — tutti i cancelli deterministici, prima di consegnare.

E se l'udienza va male: **`/reclamo`**, entro **dieci giorni perentori** dalla pronuncia.

## Controlli obbligatori prima di consegnare

```bash
# le protezioni funzionano? 50 casi, metà falsi positivi da non commettere
./scripts/test-hooks.py

# l'atto finale, da solo: piede, domande, glosse, allegati, adempimenti, citazioni
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_atto.py \
  <v7> --tipo ricorso --registro fascicolo/_dati/registro-fonti.md \
  --prove <prove.md> --timeline fascicolo/_dati/timeline.md

# la conservazione lungo la catena, due volte, una per passaggio
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_citazioni.py \
  <v5> <v6> --registro fascicolo/_dati/registro-fonti.md \
  --delta-min -5 --delta-max 10 --passaggio CHIAREZZA
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_citazioni.py \
  <v6> <v7> --registro fascicolo/_dati/registro-fonti.md \
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
7. **I termini aperti**, dal più vicino: quale, da cosa decorre, quando scade, cosa si perde.
8. **Il promemoria**: questo materiale va rivisto, sottoscritto e depositato da un avvocato
   iscritto all'albo. Nessun atto è stato depositato.

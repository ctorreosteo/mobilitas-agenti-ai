---
description: Fa girare tutti i cancelli deterministici su una pratica — fatti, protezioni, atto, conservazione
argument-hint: "[pratica]"
---

Fai girare tutto ciò che si può verificare contando, prima di guardare l'atto con gli occhi.

**L'ordine non è casuale.** Prima i **fatti**, perché un atto costruito su un fascicolo bucato è
già sbagliato quando arriva ai cancelli che lo collaudano. Poi le **protezioni**: se non funzionano,
tutto il resto è un'opinione.

## 1. I fatti

```bash
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_caso.py \
  fascicolo/_dati/caso.json --tipo ricorso \
  --atto fascicolo/<pratica>/v7-finale.md
```

Va per primo perché è l'unico cancello che guarda **a monte**: tutti gli altri collaudano un atto
già scritto, e un atto scritto su un fascicolo bucato è già il danno. I campi che quel deliverable
pretende, le date che non si contraddicono, l'età del minore contro la sua data di nascita — e, se
gli passi l'atto, se i valori che contiene abbiano una fonte nel fascicolo o siano stati dedotti.

**Un campo vuoto non si riempie con un valore verosimile: si chiede al cliente.** Un reddito
plausibile in un ricorso vale quanto una sentenza inventata, e si smonta con la stessa facilità.

## 2. Le protezioni

```bash
./scripts/test-hooks.py
```

Blocca ciò che deve bloccare e — la metà che conta — **non blocca il lavoro legittimo**. Se anche
un solo caso fallisce, fermati: l'agente sta lavorando senza rete e non lo sa.

## 3. L'atto finale, da solo

```bash
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_atto.py \
  fascicolo/<pratica>/v7-finale.md --tipo ricorso \
  --registro fascicolo/_dati/registro-fonti.md \
  --prove fascicolo/<pratica>/prove.md \
  --timeline fascicolo/_dati/timeline.md
```

Piede, domande in prima pagina, glossa di ogni etichetta, indice degli allegati, allegati citati e
non mappati, piano genitoriale e documentazione economica del triennio, citazioni non `CONFERMATA`,
lunghezza.

**Nessun bloccante si supera con una motivazione.** Gli avvisi sì: sono le cose che una macchina
non può decidere, e vanno guardate a mano, una per una.

## 4. La conservazione lungo la catena

```bash
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_citazioni.py \
  fascicolo/<pratica>/v5-intermedia.md fascicolo/<pratica>/v6-chiarezza.md \
  --registro fascicolo/_dati/registro-fonti.md \
  --delta-min -5 --delta-max 10 --passaggio CHIAREZZA

python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_citazioni.py \
  fascicolo/<pratica>/v6-chiarezza.md fascicolo/<pratica>/v7-finale.md \
  --registro fascicolo/_dati/registro-fonti.md \
  --delta-min -3 --delta-max 5 --min-identita 60 --passaggio LINGUA
```

**Due volte, una per passaggio.** Misurate in blocco, le due riscritture si compensano: se la prima
perde e la seconda aggiunge, i conti tornano e la perdita non si vede.

## 5. Il disco

```bash
ls -1 fascicolo/<pratica>/
```

Gli agenti riferiscono, non provano. Un atto «completato» che non ha la `v7` sul disco non è
completato.

## 6. Le scadenze

Apri `fascicolo/_dati/scadenze.md` e controlla che non ci sia un termine aperto in scadenza. È
l'unica parte della difesa che non si recupera con un buon argomento.

## Chiusura

Riporta, in questo ordine: **fatti** (campi vuoti e incoerenze del fascicolo), **protezioni**
(quanti casi, quanti falliti), **atto** (bloccanti e avvisi, con il testo di ciascuno),
**conservazione** (i numeri dei due passaggi), **disco** (quali file esistono davvero),
**scadenze** (il primo termine in ordine di data).

E una riga sola, in fondo: **depositabile o no.** Non esiste il «depositabile con riserva».

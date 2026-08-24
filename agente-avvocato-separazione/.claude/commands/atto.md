---
description: Redige un atto civile e lo porta attraverso tutti i livelli di revisione fino al collaudo
argument-hint: "[tipo: ricorso|memoria|comparsa|istanza] [pratica]"
---

Redigi l'atto indicato in `$ARGUMENTS` e portalo fino al collaudo.

**Precondizione**: strategia esistente. Un atto senza strategia è una domanda senza un piano.

## Procedura

1. **Verifica la competenza.** Prima di ogni altra cosa, e prima di ogni atto introduttivo:
   l'entrata in funzione del *Tribunale per le persone, per i minorenni e per le famiglie* è
   prorogata al **31 ottobre 2026**, ed è già la seconda proroga. **Riverificala sul web adesso**:
   è la voce che si muove, e un ricorso all'ufficio sbagliato costa mesi.

2. **Ricerca delle fonti.** Lancia `ricercatore-giurisprudenza` per ciò che serve alle domande e
   non è ancora nel registro. Priorità assoluta all'orientamento sull'età e i pernottamenti.

3. **Redazione v1.** Con `redattore-atti`, o direttamente seguendo `architettura-atto.md`.

4. **Primo livello** — lancia **in parallelo, nello stesso messaggio**, le dieci lenti:
   `avversario`, `giudice`, `pubblico-ministero`, `curatore-minore`, `ctu`, `penalista`,
   `patrimoniale`, `prove`, `cliente`, `deontologia`. → sintesi **v2**.

5. **Secondo livello** — `fonti` **poi** `cassazione`. L'ordine conta: si ripulisce prima di
   ampliare. → **v3**.

6. **Terzo livello** — `coerenza`. → **v4**.

7. **Quarto livello** — `editor`. → **v5**.

8. **Quinto livello** — `chiarezza` riscrive. → **v6**.

9. **Sesto livello** — `italiano-giuridico`. → **v7**.

10. **Collaudo** — `collaudo`, con lo script eseguito **due volte**:

```bash
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_citazioni.py \
  v5.md v6.md --registro fascicolo/_dati/registro-fonti.md \
  --delta-min -5 --delta-max 10 --passaggio CHIAREZZA

python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_citazioni.py \
  v6.md v7.md --registro fascicolo/_dati/registro-fonti.md \
  --delta-min -3 --delta-max 5 --min-identita 60 --passaggio LINGUA
```

## La regola della sintesi

**Il feedback si pesa, non si somma.** ERRORE si corregge, RISCHIO si valuta, PREFERENZA si ignora
di default. Se dopo una revisione l'atto è cresciuto oltre il 20%, hai sommato.

## Cancello

Prima di consegnare: **rubrica** (sotto 90/100 non si consegna; verificabilità sotto 16 è uno stop
indipendente) e **checklist** (un solo NO, si corregge).

## Chiusura

Riporta: le domande formulate, cosa è `PROVATO` e cosa no, le fonti usate con il livello, l'esito
del collaudo, e **cosa manca al cliente** perché l'atto regga in udienza.

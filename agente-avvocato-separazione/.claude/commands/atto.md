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

3. **Il cancello sui fatti** — prima di scrivere una riga:

   ```bash
   python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_caso.py \
     fascicolo/_dati/caso.json --tipo <tipo>
   ```

   Se esce con bloccanti, **fermati e chiedi**: i campi vuoti si domandano al cliente e si
   registrano in `caso.json`, non si riempiono con un valore verosimile. Un reddito dedotto in un
   ricorso si smonta con una busta paga, e porta con sé la credibilità di tutto l'atto.

4. **Redazione v1.** Con `redattore-atti`, o direttamente seguendo `architettura-atto.md`.

5. **Primo livello** — lancia **in parallelo, nello stesso messaggio**, le dodici lenti:
   `avversario`, `giudice`, `pubblico-ministero`, `curatore-minore`, `ctu`, `penalista`,
   `patrimoniale`, `prove`, `decadenze`, `negoziatore`, `cliente`, `deontologia`.
   → sintesi **v2**.

   Le ultime due non guardano il merito e non si pesano come le altre: `decadenze` non esprime
   preferenze — una domanda riservata invece che formulata è sempre un ERRORE — e `negoziatore`
   non chiede mai di indebolire una domanda, chiede di renderla accettabile a parità di sostanza.

6. **Secondo livello** — `fonti` **poi** `cassazione`. L'ordine conta: si ripulisce prima di
   ampliare. → **v3**.

7. **Terzo livello** — `coerenza`. → **v4**.

8. **Quarto livello** — `editor`. → **v5**.

9. **Quinto livello** — `chiarezza` riscrive. → **v6**.

10. **Sesto livello** — `italiano-giuridico`. → **v7**.

11. **Collaudo** — `collaudo`, con due script e tre esecuzioni.

**La conservazione lungo la catena**, due volte, una per passaggio — misurate in blocco le due
riscritture si compensano, e la perdita non si vede:

```bash
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_citazioni.py \
  v5.md v6.md --registro fascicolo/_dati/registro-fonti.md \
  --delta-min -5 --delta-max 10 --passaggio CHIAREZZA

python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_citazioni.py \
  v6.md v7.md --registro fascicolo/_dati/registro-fonti.md \
  --delta-min -3 --delta-max 5 --min-identita 60 --passaggio LINGUA
```

**E il cancello sulla finale da sola.** I due comandi qui sopra confrontano: vedono cosa si è
perso, non cosa non c'è mai stato. Un atto può attraversare tutta la catena conservando
fedelmente un difetto che aveva dalla v1:

```bash
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_atto.py \
  v7.md --tipo ricorso --registro fascicolo/_dati/registro-fonti.md \
  --prove prove.md --timeline fascicolo/_dati/timeline.md
```

## La regola della sintesi

**Il feedback si pesa, non si somma.** ERRORE si corregge, RISCHIO si valuta, PREFERENZA si ignora
di default. Se dopo una revisione l'atto è cresciuto oltre il 20%, hai sommato.

## Cancello

`verifica_atto.py` per primo — non dipende da chi ha scritto l'atto. Poi **rubrica** (sotto 90/100
non si consegna; verificabilità sotto 16 è uno stop indipendente) e **checklist** (un solo NO, si
corregge).

**Zero bloccanti, o non si consegna.** Non esiste il «depositabile con riserva».

## Chiusura

Riporta: le domande formulate, cosa è `PROVATO` e cosa no, le fonti usate con il livello, l'esito
del collaudo, **quali termini questo atto apre o consuma** (e la riga aperta in
`fascicolo/_dati/scadenze.md`), e **cosa manca al cliente** perché l'atto regga in udienza.

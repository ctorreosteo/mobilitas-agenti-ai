# Procedure — Skill Direttore Osteopatico (Mobilitas / OsteoTouch)

Cartella di lavoro per la redazione e revisione delle **procedure cliniche osteopatiche**.

## Struttura

```
.claude/skills/            ← skill di progetto (attive quando lavori in questa cartella)
  direttore-osteopatico-procedure/        AUTORE — redige la procedura + Scheda Operativa
    ├─ SKILL.md
    ├─ references/         materiale di supporto (DNA editoriale, rubrica, esempi, ecc.)
    └─ scripts/            build_docx.py
  direttore-osteopatico-specialista/      REVISORE — medico specialista di riferimento
  direttore-osteopatico-medico-generale/  REVISORE — MMG che invia i pazienti
  direttore-osteopatico-fisioterapista-ebp/ REVISORE — fisioterapista evidence-based (scettico)
  direttore-osteopatico-compliance/       REVISORE — legale / deontologia / GDPR
  direttore-osteopatico-neolaureato/      REVISORE — usabilità in stanza il lunedì mattina
  direttore-osteopatico-apprendimento/    REVISORE 3° liv. — logica dell'apprendimento
docs/
  agent-teams.md           documentazione team di agenti Claude Code
procedure-generate/
  _dati/livelli.json       manifesto: chi è autore e chi revisore di 1°/2°/3°/4° livello
  _workflow/genera-procedure.workflow.js
```

## Pipeline editoriale

Ruoli e livelli sono dichiarati in `procedure-generate/_dati/livelli.json`: è l'unico file
da toccare per aggiungere, togliere o spostare un revisore.

1. **`procedure`** redige la v1 (procedura + Scheda Operativa).
2. **1° livello** — panel avversariale in parallelo sul contenuto (specialista, MMG, EBP,
   sicurezza, compliance, usabilità, modelli, sistema dominante, clinico esperto) → **v2**.
3. **2° livello** — fedeltà al metodo / Bibbia → **v3**.
4. **3° livello** — **logica dell'apprendimento**: il documento insegna o fa solo eseguire?
   Verifica la sequenza *perché → cosa → come → pratica → feedback → autonomia*. Non aggiunge
   clinica e non asciuga: riordina, esplicita il senso mancante, pretende criteri di
   padronanza (crescita netta ≤ 5%) → **v4**.
5. **4° livello** — editor di asciugatura: toglie ridondanza e riporta il documento nel range
   5.000-7.000 parole, rispettando i passaggi che il 3° livello ha marcato *da proteggere*
   → **v5 finale**.

L'apprendimento sta **prima** dell'editor apposta: può chiedere qualche riga in più, e
l'editor asciuga il risultato.

## Note operative

- Le skill sono **project-scoped**: valgono solo dentro questa cartella. Per renderle
  globali andrebbero spostate in `~/.claude/skills/`.
- Il `name:` in ogni `SKILL.md` deve combaciare col nome della cartella (già verificato).
- Le skill vengono caricate all'avvio sessione: dopo modifiche strutturali **riavvia la
  sessione** perché Claude Code le rilevi.

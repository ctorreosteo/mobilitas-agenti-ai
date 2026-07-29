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
docs/
  agent-teams.md           documentazione team di agenti Claude Code
```

## Pipeline editoriale

1. **`procedure`** redige o aggiorna il documento clinico.
2. I **5 revisori** lo attaccano ciascuno da una prospettiva diversa (specialista, MMG,
   EBP, compliance, usabilità) — pensati come panel avversariale.
3. **`procedure`** sintetizza i feedback e chiude la versione finale.

## Note operative

- Le skill sono **project-scoped**: valgono solo dentro questa cartella. Per renderle
  globali andrebbero spostate in `~/.claude/skills/`.
- Il `name:` in ogni `SKILL.md` deve combaciare col nome della cartella (già verificato).
- Le skill vengono caricate all'avvio sessione: dopo modifiche strutturali **riavvia la
  sessione** perché Claude Code le rilevi.

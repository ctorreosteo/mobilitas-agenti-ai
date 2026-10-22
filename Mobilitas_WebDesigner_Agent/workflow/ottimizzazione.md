# Workflow · Ottimizzazione

**Richieste tipiche:**
- «Migliora la landing del reflusso»;
- «Non converte da mobile»;
- «Rendila più veloce».

**Il principio:** la rifinitura conserva l'identità esistente: aspetto, comportamento, testi, integrazioni. Si migliora ciò che limita la conversione, la leggibilità, l'accessibilità o la velocità. I testi con dati non si cambiano senza chiedere. Se il problema è il mondo visivo stesso, proponi un redesign.

**Dove si lavora:**
- **Su richiesta diretta** («migliora la landing X»): sui file esclusivi della landing X, nel sito.
- **Dopo una duplicazione:** solo sulla copia.

I componenti condivisi non si toccano.

**Fasi:** F0, diagnosi, proposta ⛔, correzioni, F6–F9.

## Passi

1. **F0.** Incarico, dipendenze della landing (file esclusivi e condivisi), sito in prova.
2. **Diagnosi**, in `INC/brief/diagnosi.md`.
   - **Misure:**
     - `cattura.cjs`: prima schermata, testi sotto 14 px, bersagli sotto 44 px, sbordamenti, errori;
     - `controlli.cjs`: popup, domande frequenti, tastiera, barra mobile, rete;
     - `prestazioni.cjs`.
   - **Design:** procedure `audit` e `critique` di Impeccable (`AG/skills/impeccable/reference/audit.md`, `critique.md`), più `AG/tools/impeccable.sh SITO detect --json <file>`.
   - **Movimento:** `find-animation-opportunities` e `review-animations`. Spesso il guadagno sta nel togliere animazioni che ritardano il contenuto.
   - **Copy e conversione:** gerarchia d'azione, prove, obiezioni scoperte, offerta poco chiara, prudenza sanitaria.
   - **Problemi in ordine di impatto sulla prenotazione:** per ciascuno, dove sta, perché pesa e quale correzione propone.
3. **Proposta** ⛔.
   - Le correzioni tecniche, cioè accessibilità, misure, errori e prestazioni, si applicano subito: dillo.
   - Testi, dati e struttura richiedono l'approvazione.
   - Se una correzione tocca un componente condiviso, proponi una variante locale oppure chiedi.
4. **Correzioni** in un unico blocco, poi F6, con un solo giro di verifica.
5. **F7–F9**, con il confronto prima e dopo (`confronto.cjs`) e le misure prima e dopo.

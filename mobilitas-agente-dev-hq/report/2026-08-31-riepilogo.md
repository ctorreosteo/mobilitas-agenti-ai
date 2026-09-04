# Riepilogo giornata — 2026-08-31

Un solo task aveva scadenza oggi nella lista HQ, e l'ho lavorato. Non è stato necessario il fallback sui
task scaduti.

| Task | Titolo | Esito | Giri di revisione | Stato ClickUp |
|---|---|---|---|---|
| [869erahk4](https://app.clickup.com/t/869erahk4) | Whatsapp nel gestionale | **Consegnato** | Codice **4** (16 → 3 → 1 → 0 ERRORE), documentazione **3** (13 → 2 → 0) | `review` |

Nessun commit, nessun push, nessun branch. Il lavoro è nella working tree dei due repo.

## In due righe

La feature è **completa in codice ma spenta**. C'è tutto — pagina, dominio, persistenza, API, ingestione
webhook, invio — dietro l'interruttore `WHATSAPP_INTEGRAZIONE_ABILITATA`, che è `false`: nessun byte parte
verso Meta. Accenderla non è lavoro di sviluppo.

## Cosa richiede una tua decisione

1. **Prima di accendere servono cose che non sono codice**: onboarding Coexistence tramite un BSP o come
   Tech Provider Meta, DPA firmato con Meta e con l'eventuale partner, DPIA e scheda di registro. Il
   fascicolo privacy dichiarava in cinque punti che questa integrazione non esiste: le ho corrette tutte,
   e ora subordinano esplicitamente l'attivazione a quegli atti.
2. **Quanti numeri WhatsApp Business ha lo studio?** È una domanda da due minuti. Ho assunto uno solo; con
   due, una segreteria vedrebbe la corrispondenza dell'altra sede.
3. **«Manager» include `MANAGER_OSTEOPATI`?** Oggi no — solo `MANAGER`, `ADMIN`, `SEGRETERIA`.
4. **Retention della corrispondenza e cancellazione paziente**: i messaggi non sono collegati all'entità
   `Paziente`, quindi una richiesta di oblio eseguita secondo la procedura scritta non li raggiunge.
5. **Gli accessi alla inbox vanno nell'audit clinico?** Oggi no. Va deciso, in un senso o nell'altro.

## Un file nell'albero che non è mio

`mobilitas-backend/src/main/resources/db/migration/V369__corso_contabilita_daily_31_agosto_2026.sql` —
lezione del corso Contabilità, comparsa alle 18:35, dopo che avevo fotografato la linea di base (vuota) e
mentre il task era in lavorazione. **Non l'ho scritto e non l'ho toccato.** Va committato per conto suo.

## File

- Report completo: [2026-08-31-869erahk4.md](./2026-08-31-869erahk4.md)
- Piano d'azione: [2026-08-31-869erahk4-piano.md](./2026-08-31-869erahk4-piano.md)

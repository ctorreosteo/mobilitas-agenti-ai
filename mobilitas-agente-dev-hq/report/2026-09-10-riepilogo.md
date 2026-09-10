# Riepilogo — 2026-09-10

Un solo task in scadenza oggi nella lista HQ. Lavorato per intero.

| Task | Titolo | Esito | Giri di revisione | ClickUp |
|---|---|---|---|---|
| [`869ezy4ac`](https://app.clickup.com/t/869ezy4ac) | Filtri estratto Qonto | **Consegnato con riserva** (uscita A) | Piano: 3 · Codice: 5 (tetto) · Doc: 2 | `to do` → `review` |

Report completo: [2026-09-10-869ezy4ac.md](./2026-09-10-869ezy4ac.md) · Piano: [2026-09-10-869ezy4ac-piano.md](./2026-09-10-869ezy4ac-piano.md)

---

## Cosa richiede una tua decisione

1. **L'endpoint dell'estratto conto non ha permessi.** Qualunque utente autenticato — tirocinante,
   marketer, token dell'app paziente — scarica l'estratto integrale dello studio: nomi dei pazienti
   nelle causali, stipendi, IBAN. **Preesistente**, non introdotto da me, e la scelta dei ruoli
   ammessi è tua. Ma `docs/privacy/01-ruoli-e-responsabilita.md` dichiara che quel limite è già
   attivo, e non lo è.
2. **Il termine cercato finisce in chiaro in `audit_attivita_api`.** Sistemico su ogni endpoint di
   ricerca del gestionale; la lacuna è nella misura, non in questo path.
3. **`HIDDEN_ROW_KEYWORDS`**: ora che si può cercare, il nascondimento client-side e il filtro
   backend si contraddicono a schermo. O il filtro esclude quelle parole a monte, o l'empty state
   ammette che qualcosa è nascosto.
4. **Il tuo lavoro non committato.** Il frontend non era pulito: 764 righe tue sul POS Qonto, in tre
   dei file che ho toccato. Nel frontend l'indice contiene il tuo lavoro e la working tree il mio
   (`git diff` = mio, `git diff --cached` = tuo). Nel backend parte dei miei file è **finita in
   staging senza che l'abbia fatto io**: guarda prima di committare.

## Il punto da guardare per primo, al collaudo

`?stato=declined&campoData=emitted_at`. Se torna vuoto, l'assunzione che `emitted_at` sia popolato
su tutti gli stati è sbagliata, e per quello stato il filtro va su `updated_at`.

## Una nota sul ciclo

Cinque giri di revisione, ERRORE per giro **1 → 1 → 0 → 1 → 1**: un ciclo che non converge.
La causa non erano difetti nuovi ogni volta, ma **due classi di difetto di cui correggevo
un'istanza per giro** — quindici punti che affermavano fatti non verificati, e un guard messo su una
porta di tre. La lezione, e il motivo per cui la scrivo qui: quando un rilievo torna cambiando solo
indirizzo, la correzione giusta non è nel punto segnalato.

L'ultima correzione è stata applicata **dopo il tetto dei cinque giri**, quindi nessun revisore l'ha
vista. È l'unica parte del task priva del 100%, ed è dichiarata nel report.

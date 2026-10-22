# Test dell'agente

I comandi si lanciano dalla cartella dell'agente.

**Garanzie:**
- nessun test usa crediti Superdesign, fa deploy o invia dati a servizi reali;
- nessun test scrive nella cartella dell'agente, nel sito o nella configurazione reale;
- tutto avviene in cartelle temporanee, indicate a fine esecuzione.

| Test | Comando | Cosa verifica | Costi |
|---|---|---|---|
| Verifica dell'installazione | `test/verifica-installazione.sh` | Integrità rispetto a `MANIFESTO.sha256`, nessun file estraneo, nessun percorso assoluto, skill e agenti, dipendenze, nessun segreto, configurazione. **Nessun file caricato in automatico** da Cursor o Claude Code; skill di richiamo corretta | nessuno |
| Funzionamento | `test/test-funzionamento.sh` | Incarico fuori dall'agente; dipendenze di una landing; duplicazione simulata con originale preservato e rilevamento delle modifiche vietate; catture e controlli con protezione iniettata; prova negativa; configurazione Vite di prova; blocchi Superdesign; Impeccable; installazione della skill di richiamo; sola lettura sul disco; **cartella dell'agente invariata** | nessuno |
| Sito reale | `test/test-sito-reale.sh <cartella-sito> --percorsi /reflusso,/cervicalgia` | Il sito vero, avviato in prova senza modificarlo: landing esistenti con popup reale provato a campi vuoti, nessuna scrittura partita, build di prova, sito e agente invariati | nessuno (servono le dipendenze già installate nel sito) |
| Attivazione in Claude Code | `test/test-attivazione-claude.sh --esegui` | Senza comando il sistema non si attiva; con `/webdesigner` legge `ISTRUZIONI.md` e sceglie il workflow; le skill interne non sono registrate | tre brevi sessioni di Claude |
| Politica dei riferimenti | `node test/test-politica-riferimenti.mjs` | Decisioni della guardia di Taste | nessuno |

## Dopo una modifica voluta al pacchetto

Esegui `tools/setup/manifesto.sh`, poi `test/verifica-installazione.sh`. Se la cartella è protetta, prima esegui `tools/setup/proteggi.sh off`.

## Prova manuale in Cursor (da fare dopo il collegamento)

Cursor non ha un'interfaccia a riga di comando su questa macchina: la prova va fatta da una persona.

1. **Installa la skill di richiamo** in una sola delle posizioni descritte in `integrazioni/cursor-e-claude-code.md` (`tools/setup/collega.sh … --scrivi`).
2. **Apri il workspace** con il sito e la cartella degli agenti aziendali. Ricarica la finestra.
3. **Controlla le impostazioni:** in Impostazioni → Rules/Skills compare `webdesigner`, e **non** compaiono `impeccable`, `taste` né le skill di Emil.
4. **Prova senza attivazione:** «Rendi più grande il titolo della landing del reflusso. Non modificare nulla: dimmi solo cosa faresti.»
   **Atteso:** risposta normale, nessuna lettura di `ISTRUZIONI.md`, nessun riferimento al WebDesigner.
5. **Prova con attivazione:** «/webdesigner duplica la landing del reflusso e migliorala. Non modificare nulla: dimmi quale workflow useresti e cosa mi chiederesti.»
   **Atteso:**
   - legge `ISTRUZIONI.md`;
   - usa `duplicazione.md`, poi `ottimizzazione.md`;
   - propone una route distinta;
   - chiede solo informazioni e autorizzazioni.
6. **Facoltativo:** «Usa l'agente WebDesigner per…» senza comando. Con la variante «comando» non deve attivarsi; con la variante «nominato» sì.

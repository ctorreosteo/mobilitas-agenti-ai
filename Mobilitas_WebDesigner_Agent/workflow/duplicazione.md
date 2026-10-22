# Workflow · Duplicazione

**Richieste tipiche:**
- «Duplica la landing del reflusso e usa il WebDesigner per migliorarla»;
- «Fai una versione B della landing X».

**Il principio:** la landing originale resta identica e funzionante. Si crea una copia nel sito, con un percorso distinto, che mantiene copy, offerta e integrazioni, salvo istruzioni diverse. Il workflow WebDesigner (ottimizzazione o redesign) si applica **solo alla copia**.

## Passi

1. **Individua l'originale.**
   - Cerca la pagina e la sua route: `grep -rn` sul nome nel file di routing e in `src/pages`.
   - Se ci sono più candidati, ad esempio una landing e una sua variante, chiedi quale ⛔.
2. **Dipendenze.**
   ```sh
   node AG/tools/sito/dipendenze.mjs SITO <file-originale> --json INC/brief/dipendenze-originale.json
   ```
   - **File esclusivi:** quelli che si copiano.
   - **File condivisi** (popup di prenotazione, Header, Footer, dati delle recensioni, componenti usati anche altrove): **non si copiano e non si modificano**. La copia li importa come l'originale.
   - **Foto in `public/`:** la copia le usa dagli stessi percorsi. Le foto nuove o modificate vanno in una cartella nuova.
3. **Proteggi l'originale.** Registra i file da preservare: la pagina originale, i suoi file esclusivi e il file di routing per le righe dell'originale.
   ```sh
   node AG/tools/incarico/registro.cjs preserva INC <file-originale> <file-esclusivi…>
   ```
   Il file di routing cambierà per la nuova route: la verifica finale controlla a parte che la riga dell'originale sia invariata (vedi punto 7).
4. **Percorso e nomi distinti.** Proponi la route della copia, ad esempio `/reflusso-v2` o `/reflusso-b`, e il nome del componente, ad esempio `ReflussoV2`. Chiedine conferma insieme alle altre domande ⛔. Senza indicazioni, usa il suffisso `-v2`.
5. **Crea la copia nel sito:**
   - nuovo file di pagina copiato dall'originale, con il nome del componente cambiato;
   - copie dei soli file esclusivi in una cartella propria, con gli import aggiornati verso le copie;
   - gli import dei condivisi restano invariati;
   - **una** route nuova nel file di routing, montata con lo stesso wrapper dell'originale, per esempio `Layout`, più il suo import.

   Testi, offerta, popup di prenotazione, WhatsApp e tracciamento restano gli stessi dell'originale. Se l'originale contiene identificativi che devono distinguere le due versioni, segnalali senza cambiarli: ne fanno parte i nomi di eventi di tracciamento e la sorgente inviata al gestionale.
6. **Verifica che la copia sia identica all'originale** prima di migliorarla. Cattura le due route e confrontale con `confronto.cjs`: devono coincidere.
   ```sh
   node AG/tools/playwright/cattura.cjs --incarico INC --percorso /originale,/copia --prefisso prima
   ```
7. **Applica il workflow WebDesigner alla sola copia:** `workflow/ottimizzazione.md` oppure `workflow/redesign.md`.
8. **Verifica finale delle due landing:**
   - `cattura.cjs` e `controlli.cjs` con `--percorso /originale,/copia`: entrambe devono aprirsi senza errori e il popup di prenotazione deve funzionare in entrambe;
   - `registro.cjs verifica INC`: l'originale e i suoi file esclusivi devono risultare preservati;
   - `git diff -U0 <file-di-routing>`: la sola differenza deve essere l'aggiunta della route e dell'import della copia;
   - `build-prova.sh INC`: il sito deve compilare.

## Consegna

Indica:
- le due route;
- i file creati;
- la riga aggiunta al routing;
- la conferma che l'originale è invariato, cioè l'esito di `registro.cjs verifica`;
- le differenze tra copia e originale;
- i punti da decidere per la pubblicazione, per esempio se la copia debba avere un tracciamento distinto.

# Studio formazione — piano

**Richiesta (Carlos, 22/10/2026):** manager, direttore e admin creano corsi, moduli e lezioni. Video: si carica il file, il gestionale lo mette su Cloudflare e recupera i dati. Lezioni scritte: qualsiasi documento, il backend (AI o altro) lo converte nel formato più estetico/corretto o in quello scelto. Pagina di creazione ultra estetica.

Repo: `/Users/carlitos/mobilitas-hq/mobilitas-{backend,frontend}` (la mappa in `references/mappa-gestionale.md` punta ancora a `/Users/carlitos/mobilitas-*`: è vecchia).

## Stato di partenza (letto dal codice)

- Esistono `Corso → Modulo → Lezione` (VIDEO / DOCUMENTO a capitoli markdown / HTML su GCS). API solo per **creare/modificare lezioni e sezioni**; **nessuna API per creare corsi e moduli**.
- Video: si inserisce a mano il `cloudflareUid`. **Nessuna chiamata API a Cloudflare** nel backend.
- Permessi: `canManageFormazione` = **qualsiasi utente del gestionale** lato backend; il frontend mostra "Nuova lezione" solo all'admin. Incoerente.

## Interventi

### Backend
1. **Permessi** — `canManageFormazione`: solo `ADMIN`, `MANAGER`, `DIRETTORE` (lettura letterale della richiesta; `MANAGER_OSTEOPATI`/`MANAGER_SEGRETERIA` esclusi — bivio dichiarato). Chi gestisce vede tutti i corsi, anche quelli riservati a un ruolo.
2. **CRUD corsi e moduli** + riordino moduli/lezioni + copertina caricabile (GCS bucket lezioni, `copertine/`, URL firmato in risposta).
3. **Cloudflare Stream** (`CloudflareStreamService`, doc verificata 22/10/2026):
   - upload **tus diretto dal browser** (`POST /accounts/{id}/stream?direct_user=true`, header `Tus-Resumable`, `Upload-Length`, `Upload-Metadata`; UID da `stream-media-id`, URL monouso da `Location`). Il file non passa dal backend: niente limite dei 100 MB multipart.
   - sincronizzazione: `GET /accounts/{id}/stream/{uid}` → `readyToStream`, `status.state`, `pctComplete`, `duration`, `thumbnail` → salvati su lezione (durata, copertina, stato).
   - credenziali: `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_STREAM_API_TOKEN` (env / properties, come ElevenLabs).
4. **Conversione documenti** (`LezioneConversioneService`, asincrona):
   - formati: PDF (diviso in blocchi di pagine con PDFBox e mandato nativo a Claude: legge anche scansioni e tabelle), DOCX/DOC, PPTX, XLSX (POI), RTF, TXT/MD, HTML, immagini.
   - l'AI restituisce markdown pulito per blocco; la struttura (capitoli `#`, sottocapitoli `##`) si ricava **in modo deterministico**.
   - destinazione: **Automatico** (HTML resta HTML, tutto il resto → guida a capitoli), **Guida a capitoli** (DOCUMENTO), **Pagina HTML** (markdown → template HTML curato, commonmark con HTML grezzo escapato; nessun HTML scritto dall'AI).
   - MD e HTML con AI spenta: nessuna chiamata AI.
   - originale conservato su GCS (`originali/`) per riconvertire in un altro formato.
   - stato su lezione: `IN_CORSO / COMPLETATA / ERRORE`; una conversione ferma da > 45 min è mostrata come interrotta.
5. **Migrazione V464**: colonne di stato video e conversione su `lezioni`.
6. Dipendenze: `org.commonmark:commonmark` + `commonmark-ext-gfm-tables` 0.24.0.

### Frontend
1. `lib/formazione-access.ts`: `canManageFormazione` (ADMIN, MANAGER, DIRETTORE), allineato al backend.
2. **Pagina `/formazione/studio`** (+ `/formazione/studio/corsi/:corsoId`): catalogo con copertine, builder del corso con moduli e lezioni riordinabili, sheet laterali per corso/modulo/lezione.
3. **Wizard lezione** in sheet: tipo (video / documento) → upload con progresso reale (tus a blocchi da 50 MiB, client minimale senza nuove dipendenze) → elaborazione Cloudflare con polling e anteprima → pronto. Documento: dropzone multi-formato → scelta formato a tile → avanzamento → anteprima.
4. Entry point "Studio" nell'hero della Formazione per chi gestisce.
5. CSS `lux-formazione-studio.css` solo su token `--vl-*` (tre temi).

## Fuori scope, dichiarato
- URL firmati Cloudflare (`richiedeToken` resta com'è; i video si caricano con `requireSignedURLs=false` per restare riproducibili dal player attuale).
- Cancellazione del video su Cloudflare quando si sostituisce (un UID può essere condiviso con il sito).
- Bozza/pubblicato per i corsi.

## Privacy
- Anthropic e Cloudflare sono già in matrice. Nuovo trattamento: video di formazione su Stream e documenti formativi ad Anthropic. Avviso in UI: niente dati di pazienti nei documenti.

# API Higgsfield — contratto verificato

Verificato il **2026-09-29** contro `docs.higgsfield.ai`. Questo file esiste per non
rifare la ricerca a ogni sessione. Quando `verifica_modelli.py` segnala una differenza,
si aggiorna qui e si ridata l'intestazione.

Indice vivo della documentazione: <https://docs.higgsfield.ai/docs/llms.txt>
Catalogo autorevole dei modelli: <https://console.higgsfield.ai> (dietro account)

---

## Autenticazione

```
Authorization: Key ${HF_API_KEY_ID}:${HF_API_KEY_SECRET}
```

Le chiavi si creano in console. Stanno nell'ambiente, **mai in un file del repo**.
Esistono ancora gli header storici `hf-api-key` e `hf-secret`: non usarli.

---

## Il ciclo di una generazione

Tutto è asincrono. Non esiste una chiamata che restituisce il file.

1. **POST** `https://api.higgsfield.ai/<endpoint>` con il body del modello.
   Risponde subito con `status`, `request_id`, `status_url`, `cancel_url`.
2. **GET** `https://api.higgsfield.ai/requests/<request_id>/status` fino a uno stato
   terminale: `completed`, `failed`, `nsfw`, `canceled`.
   Polling consigliato: 2 secondi, crescita graduale fino a 10, con jitter.
3. L'esito completato porta `images: [{url}]` per le immagini, `video: {url}` per i video.
4. **Scarica.** I file restano sul CDN almeno sette giorni.

### Stima preventiva

```
POST https://api.higgsfield.ai/estimate/<endpoint>   →  {"credits": "1.500", "usd": "0.094"}
```

Stesso body della generazione. È il costo reale per quell'account.

### Caricare un file di input

Serve quando l'input non è già a un URL pubblico (una foto di riferimento, un prodotto).

1. `POST /files/generate-upload-url` con `{"content_type": "image/jpeg"}` →
   `{public_url, upload_url, upload_headers}`
2. `PUT` del file su `upload_url` con **tutti** gli header restituiti. Nessuna credenziale
   Higgsfield verso lo storage.
3. Passa `public_url` al campo del modello (`image_url`, `video_url`, `audio_url`).

L'upload URL scade dopo un'ora. Tipi accettati: `image/jpeg`, `image/jpg`, `image/png`,
`image/webp`, `image/gif`, `audio/wav`, `audio/x-wav`, `video/mp4`.

---

## Errori

| Codice | Significato | Si ritenta? |
|---|---|---|
| `400` | parametri invalidi, input rifiutato, **oppure concorrenza raggiunta** | solo nel caso concorrenza, dopo attesa |
| `401` | credenziali mancanti o sbagliate | no |
| `403` | crediti insufficienti | no, serve ricaricare |
| `404` | richiesta o modello non disponibili per questo account | no |
| `422` | body non valido | no |
| `423` | modello temporaneamente bloccato | più tardi |
| `500` | errore server | sì, con backoff |
| `503` | modello disabilitato o non pronto | più tardi |

Il limite di concorrenza è **per account** e si legge in console. Superarlo dà `400` con
`"Maximum number of concurrent requests (N) has been reached"`. Non esistono header di
rate limit né `Retry-After`.

**`failed` e `nsfw` non vengono addebitati**, e i crediti riservati tornano indietro. Una
richiesta si può annullare solo prima che inizi l'elaborazione.

**Nessuna chiave di idempotenza sulle POST.** È il motivo per cui il client persiste il
`request_id` prima del polling: dopo un timeout ambiguo si interroga, non si rinvia.

Ogni risposta porta `X-Correlation-ID`: va registrato insieme al `request_id` se si apre
un ticket.

---

## Endpoint verificati il 2026-09-29

### Immagine

| Modello | Endpoint | Note sui parametri |
|---|---|---|
| SOUL V2 | `higgsfield-ai/soul/v2/standard` | `prompt` · `aspect_ratio` (9:16, 16:9, 4:3, 3:4, 1:1, 2:3, 3:2) · `resolution` (720p, 1080p) · `custom_reference_id` (personaggio Soul ID) · `custom_reference_strength` · `seed` · `batch_size` (1 o 4) |
| SOUL Cinema | `higgsfield-ai/soul/cinema` | come sopra, senza `style_id` |
| SOUL standard | `higgsfield-ai/soul/standard` | `prompt` · `num_images` (1-4) · `resolution` (2K, 4K) · `aspect_ratio` |
| Soul ID (addestra un personaggio) | `v1/custom-references` | `name` · `input_images` · `model_version`. Restituisce l'id da passare come `custom_reference_id` |
| Grok Image 2.0 | `xai/grok-imagine-image-2.0` | `prompt` · `image_urls` (fino a 10 riferimenti) · `quality` · `resolution` · `aspect_ratio` |

Altre famiglie documentate: Marketing Studio Image, Recraft V4.1 (quattro varianti),
Qwen Image 3, Ideogram 4, Z-Image Turbo, Wan 2.6.

**Nano Banana Pro non ha un endpoint API.** Compare nel generatore del sito e nei piani
a consumo di `higgsfield.ai`, non nel catalogo di `docs.higgsfield.ai`. Verificato il
2026-09-29. Se compare, `verifica_modelli.py` lo segnala come famiglia nuova.

### Video

| Modello | Endpoint | Note sui parametri |
|---|---|---|
| Kling 3.0 Standard i2v | `kling-video/v3.0/std/image-to-video` | `prompt` (≤ 2.500 caratteri, oltre tronca) · `image_url` **obbligatorio** · `duration` 3-15 · `cfg_scale` 0-1 · `sound` on/off · `last_image_url` · `multi_shots` con 1-6 `multi_prompt` |
| Kling 3.0 Pro i2v | `kling-video/v3.0/pro/image-to-video` | come sopra |
| Kling 3.0 Turbo i2v | `kling-video/v3.0-turbo/image-to-video` | come sopra |
| Kling 3.0 t2v | `kling-video/v3.0/std/text-to-video` | senza `image_url` |
| Kling 2.5 Turbo Pro i2v | `kling-video/v2.5-turbo/pro/image-to-video` | `duration` solo 5 o 10 · `negative_prompt` |
| Minimax Hailuo 2.3 | `minimax/hailuo-2.3/standard/image-to-video` | — |

Altre famiglie documentate: Cinema Studio 4, Genjutsu, Grok Video 1.5, Happy Horse,
Kling 2.6 e Omni, LTX 2.5, Minimax H3, Pixverse V6, Seedance 2 e 2.5, Wan 2.6 / 2.7 / 3.

**I video non hanno `aspect_ratio` nell'image-to-video:** il formato lo eredita
dall'immagine sorgente. È il motivo per cui l'aspect ratio si decide nel piano e si
applica alla generazione dell'immagine.

---

## Costo: l'unico numero che conta

I crediti per modello cambiano nel tempo e per piano. I valori nel catalogo sono ordini
di grandezza. **Il numero vero lo dà `/estimate` sull'account che genera.**

Le generazioni illimitate dei piani valgono **solo** su `higgsfield.ai` e non si
estendono all'API: ogni chiamata qui consuma crediti acquistati, che scadono dopo un anno.

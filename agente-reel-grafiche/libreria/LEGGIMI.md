# La libreria dei materiali

Quello che serve a più reel. Ogni file con una licenza ha la sua riga in `catalogo.md`.

| cartella | cosa | regole |
|---|---|---|
| `anatomia/` | disegni di **Servier Medical Art** (smart.servier.com, CC BY 4.0) | si scarica il PNG originale dalla pagina ufficiale, solo con l'ok di Riccardo (se il sito chiede registrazione o pagamento, niente); nome `servier_<nome-della-pagina>.png`; riga nel catalogo con pagina, file, data; il ricolore nel brand si fa al render, mai sul file; credito a schermo quando il disegno c'è; niente anatomia generata dall'AI o disegnata da noi |
| `logo/` | il logo Mobilitas | nei reel il logo intero, grande, in una card |
| `sfx/` | 19 effetti sonori Pixabay (`CREDITS.md`, `manifest.json`) | bassi, solo su aperture e trasformazioni importanti |
| `reference/` | i video di riferimento, con schede, ritmo, catalogo e `NOTE.md` | come aggiungerne: `reference/LEGGIMI.md`; si studiano prima del reel successivo (tappa 0) |
| `uso-modelli-reel.json` | lo storico dei modelli usati in ogni reel consegnato | lo scrive il motore (`reel-consegna`): serve alla varietà fra i reel; non entra nel repository |

## Cosa non mettere

- Foto di pazienti, B-roll da aggiungere ai reel, musica: l'agente non ne usa.
- Materiali senza licenza scritta nel catalogo.
- Niente di questa cartella si carica su servizi esterni.

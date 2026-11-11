# La libreria dei materiali

Qui sta tutto quello che serve a **più video**. Quello che serve a un video solo
(le schermate dell'app per quel video, un documento) va in
`inbox/<NOME>/materiali/`, accanto al girato.

Quando monta un video, l'agente cerca **prima** nei materiali del video e **poi**
qui. Se lo stesso nome c'è in tutti e due, vince quello del video. Per vedere
cosa trova: `./mve materiali <NOME>`.

## Le cartelle

| cartella | cosa c'è | chi la riempie |
|---|---|---|
| `logo/` | logo verde (fondi blu), logo blu (fondi chiari), pittogramma | già pronta |
| `anatomia/` | disegni di Servier Medical Art, con attribuzione | già pronta |
| `sfx/` | effetti sonori con licenza (crediti in `sfx/CREDITS.md`) | già pronta |
| `broll/` | riprese di contorno, **senza audio** nel video | ogni collaboratore, con le sue |
| `prima-dopo/` | foto prima e dopo di pazienti, **solo con consenso scritto** | ogni collaboratore |
| `musica/` | brani **con licenza** (per esempio YouTube Audio Library) | ogni collaboratore |
| `reference/` | il catalogo delle reference e il linguaggio grafico (senza i video) | arriva con le versioni nuove |

Ogni cartella ha il suo `LEGGIMI.md` con le regole.

## Il catalogo

Ogni materiale che ha bisogno di una nota, di un consenso o di una licenza si
scrive in **`catalogo.md`**. Una foto prima-dopo senza riga nel catalogo, o con il
consenso vuoto, **non si usa**. Un brano senza licenza nel catalogo non si usa.

`uso-modelli.json` lo scrive il motore: quali modelli grafici ha usato ogni video.

## Cosa non mettere

- Materiale scaricato da internet senza una licenza scritta nel catalogo, o da
  archivi a pagamento.
- Foto o video di pazienti senza consenso scritto.
- Schermate con dati personali veri: per l'app si usa un profilo di prova.

Nel repository finiscono solo i `LEGGIMI.md` di `broll/`, `prima-dopo/` e
`musica/`: i file che ci mettete restano sul vostro Mac (lo dice `.gitignore`).

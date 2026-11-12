# Catalogo della libreria

Ogni materiale con una licenza o una nota sta qui. Un materiale nuovo entra solo con la sua riga (pagina, file, data,
licenza). In questa cartella non ci sono foto di pazienti né B-roll: l'agente non ne aggiunge ai reel.

## Anatomia

Illustrazioni di **Servier Medical Art** (smart.servier.com), licenza
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): uso commerciale e
modifiche ammessi, **con attribuzione**. Nel video e in descrizione:
"Illustrazioni adattate da Servier Medical Art (smart.servier.com), CC BY 4.0".
Scaricate il 28/10/2026 (PNG originali, non modificati: il ricolore nel brand si
fa al render). Ogni animazione che le usa va validata da un osteopata (scheda nel
piano grafico del video). Regole in `motore/motore/brand.json`, voce
`video.animazioni_anatomiche`, e in `CLAUDE.md`.

| file | titolo e pagina Servier | immagine scaricata | note |
|---|---|---|---|
| `anatomia/servier_adult-human.png` | Adult - Premenopause, [smart_image/adult-human](https://smart.servier.com/smart_image/adult-human/) | `wp-content/uploads/2016/10/Adulte03.png`, 626×1703 | adulto di profilo, scheletro con colonna e bacino dentro la sagoma: la base delle animazioni di YT_POSTURA_32 |
| `anatomia/servier_vertebral-column.png` | Vertebral column, [smart_image/vertebral-column](https://smart.servier.com/smart_image/vertebral-column/) | `colonne_01.png`, 172×922 | colonna di profilo |
| `anatomia/servier_vertebral-column-side.png` | Normal vertebral column, [smart_image/vertebral-column-side](https://smart.servier.com/smart_image/vertebral-column-side/) | `Colonne_normale2.png`, 138×824 | parte di una tavola con figura di **bambino**: usare solo la colonna |
| `anatomia/servier_vertebral-column-man.png` | Vertebral column disorders - Lordosis, [smart_image/vertebral-column-man](https://smart.servier.com/smart_image/vertebral-column-man/) | `Colonne_lordose.png`, 138×824 | come sopra (bambino); "lordosi" è una diagnosi: non si usa per dire "la schiena si inarca" se lui non dice la parola |
| `anatomia/servier_skeleton-and-cartilage-profile.png` | Skeleton and cartilage, [smart_image/skeleton-and-cartilage-profile](https://smart.servier.com/smart_image/skeleton-and-cartilage-profile/) | `squelette_05.png`, 179×1164 | scheletro di profilo, senza sagoma |
| `anatomia/servier_coxal-bone.png` | Pelvis - Coxal bone, [smart_image/coxal-bone](https://smart.servier.com/smart_image/coxal-bone/) | `bassin_04.png`, 367×667 | osso dell'anca isolato |
| `anatomia/servier_musculature-front.png` | Musculature front, [smart_image/musculature-front](https://smart.servier.com/smart_image/musculature-front/) | `wp-content/uploads/2016/10/Monsieur_muscles_face.png`, 516×1356, scaricato il 28/10/2026 | **uomo** di fronte, muscoli superficiali: l'unica figura maschile utile (Servier non ha un uomo di profilo). Si ricolora in modo `muscoli` |
| `anatomia/servier_disc-herniation.png` | Disc herniation, [smart_image/disc-herniation](https://smart.servier.com/smart_image/disc-herniation/) | `Hernie_discale.png`, 440×528 | ernia del disco: **non** si usa in YT_POSTURA_32 (lui non ne parla); tenuta per altri video |
| `anatomia/servier_smart-stomach.png` | Stomach, [smart_image/smart-stomach](https://smart.servier.com/smart_image/smart-stomach/) | `wp-content/uploads/2016/10/estomac_01.png`, 822×790, scaricato il 04/11/2026 dal sito ufficiale (licenza CC BY 4.0 dichiarata sulla pagina; download autorizzato da Riccardo in chat, 04/11/2026) | stomaco intero dall'esterno, con l'esofago, senza persone. Per gli ads (AD_REFLUSSO, «cosa schiaccia lo stomaco da fuori»). Il diaframma non è stato scaricato (non serviva) |
| `anatomia/servier_nervous-system.png` | Nervous system, [smart_image/nervous-system](https://smart.servier.com/smart_image/nervous-system/) | `wp-content/uploads/2016/10/Systeme_nerveux.png`, 501×1303, md5 d7800e8bcac1980277cee8e0b1578fa5, scaricato il 07/11/2026 dal sito ufficiale (licenza CC BY 4.0 dichiarata sulla pagina, senza registrazione né pagamento; download chiesto da Riccardo in chat, 07/11/2026) | figura intera di fronte (testa di profilo) con cervello, midollo e nervi. Si usa **solo la parte alta** (testa, collo, spalle: `ritaglio` [100, 0, 400, 240]), mai il corpo intero. Per gli ads (AD_CERV_26, «il tuo sistema nervoso»); il midollo nel collo si può accendere con una linea sopra (forma semplice), niente nervi disegnati da noi |

Limite noto: su smart.servier.com (controllato il 28/10/2026) l'uomo c'è solo di fronte (corpo nudo, muscoli di fronte e di schiena); di profilo ci sono solo la donna («Adult - Premenopause») e lo scheletro, che è neutro. Fra i disegni Servier gratuiti non c'è l'ileopsoas né un
"flessore dell'anca" isolato. Per i flessori si evidenzia la zona sul disegno
dell'adulto, non si disegna il muscolo.

## Logo

| file | note |
|---|---|
| `logo/` | il logo Mobilitas: verde sui fondi blu, blu sui fondi chiari. Nei reel si usa il **logo intero** (la scritta MOBILITAS) in una card grande: il pittogramma da solo, a 390 px, si legge «7» |

## Icone

| cartella | origine e licenza | note |
|---|---|---|
| `motore/inserti/icone/tabler-3.49.0/` | Tabler Icons 3.49.0, licenza MIT (file `LICENSE` nella cartella), solo i file SVG, scaricati dal registro npm con l'impronta verificata (05/11/2026, ok di Riccardo) | mai icone con figure umane, mai spunte, mai organi |

## Effetti sonori

| file | origine e licenza | note |
|---|---|---|
| `sfx/*.mp3` (19 file: chime, click, click-soft, error, glitch-1/2/3, impact-bass-1/2, key-press, notification, ping, pop, riser, sparkle, typing, whoosh, whoosh-short, whoosh-cinematic) | Pixabay, [Pixabay Content License](https://pixabay.com/service/license-summary/): uso commerciale e non, modifiche e uso dentro un video, senza obbligo di attribuzione. Erano nella skill `media-use` (vedi `sfx/CREDITS.md`); spostati qui su richiesta di Riccardo il 27/10/2026 | `sfx/manifest.json`: durata e uso consigliato di ogni file. Nel motore si usano solo quelli scelti nel confronto con i suoni sintetizzati (`motore/motore/sfx.py`, voce `LIBRERIA_SFX`) |

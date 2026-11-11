# Catalogo della libreria

Una riga per ogni materiale che ha bisogno di una nota, di un consenso o di una
licenza. Si compilano le caselle vuote e si aggiungono righe; non si cancella
niente senza chiedere.

**Consenso.** Un materiale con persone riconoscibili (B-roll, foto) entra solo
con il consenso scritto segnato qui: sì, data, chi lo ha raccolto.

## B-roll

L'indice clip per clip lo fa l'agente (`./mve libreria`, regole in
`broll/LEGGIMI.md`). Qui una riga per cartella, solo dove serve una nota.

| cartella | consenso scritto delle persone riprese (sì + data) | note |
|---|---|---|
| | | |

## Prima-dopo

Una riga per paziente. "Prima" e "dopo" si stabiliscono dalla data di scatto,
mai dall'aspetto della postura. **Sulle foto a schermo si scrive solo PRIMA e
DOPO**, a meno che la colonna "cosa c'è tra le due foto" non dica altro.

| codice | vista | consenso scritto (sì + data) | tempo tra le due foto | cosa c'è tra le due foto | note |
|---|---|---|---|---|---|
| | | | | | |

## Musica

Solo brani con licenza per YouTube (per esempio YouTube Audio Library).

| file | da dove viene | licenza (o link) | data | note |
|---|---|---|---|---|
| | | | | |

## Anatomia

Illustrazioni di **Servier Medical Art** (smart.servier.com), licenza
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): uso commerciale e
modifiche ammessi, **con attribuzione**. Nel video e in descrizione:
"Illustrazioni adattate da Servier Medical Art (smart.servier.com), CC BY 4.0".
Scaricate il 28/10/2026 (PNG originali, non modificati: il ricolore nel brand si
fa al render). Ogni animazione che le usa va validata da un osteopata
(`videos/<NOME>/consegna/validazione-animazioni.md`). Regole in
`motore/motore/brand.json`, voce `video.animazioni_anatomiche`.

| file | titolo e pagina Servier | immagine scaricata | note |
|---|---|---|---|
| `anatomia/servier_adult-human.png` | Adult - Premenopause, [smart_image/adult-human](https://smart.servier.com/smart_image/adult-human/) | `wp-content/uploads/2016/10/Adulte03.png`, 626×1703 | adulto di profilo, scheletro con colonna e bacino dentro la sagoma |
| `anatomia/servier_vertebral-column.png` | Vertebral column, [smart_image/vertebral-column](https://smart.servier.com/smart_image/vertebral-column/) | `colonne_01.png`, 172×922 | colonna di profilo |
| `anatomia/servier_vertebral-column-side.png` | Normal vertebral column, [smart_image/vertebral-column-side](https://smart.servier.com/smart_image/vertebral-column-side/) | `Colonne_normale2.png`, 138×824 | parte di una tavola con figura di **bambino**: usare solo la colonna |
| `anatomia/servier_vertebral-column-man.png` | Vertebral column disorders - Lordosis, [smart_image/vertebral-column-man](https://smart.servier.com/smart_image/vertebral-column-man/) | `Colonne_lordose.png`, 138×824 | come sopra (bambino); "lordosi" è una diagnosi: non si usa per dire "la schiena si inarca" se lui non dice la parola |
| `anatomia/servier_skeleton-and-cartilage-profile.png` | Skeleton and cartilage, [smart_image/skeleton-and-cartilage-profile](https://smart.servier.com/smart_image/skeleton-and-cartilage-profile/) | `squelette_05.png`, 179×1164 | scheletro di profilo, senza sagoma |
| `anatomia/servier_coxal-bone.png` | Pelvis - Coxal bone, [smart_image/coxal-bone](https://smart.servier.com/smart_image/coxal-bone/) | `bassin_04.png`, 367×667 | osso dell'anca isolato |
| `anatomia/servier_musculature-front.png` | Musculature front, [smart_image/musculature-front](https://smart.servier.com/smart_image/musculature-front/) | `wp-content/uploads/2016/10/Monsieur_muscles_face.png`, 516×1356, scaricato il 28/10/2026 | **uomo** di fronte, muscoli superficiali: l'unica figura maschile utile (Servier non ha un uomo di profilo). Si ricolora in modo `muscoli` |
| `anatomia/servier_disc-herniation.png` | Disc herniation, [smart_image/disc-herniation](https://smart.servier.com/smart_image/disc-herniation/) | `Hernie_discale.png`, 440×528 | ernia del disco |

Limite noto: su smart.servier.com (controllato il 28/10/2026) l'uomo c'è solo di fronte (corpo nudo, muscoli di fronte e di schiena); di profilo ci sono solo la donna («Adult - Premenopause») e lo scheletro, che è neutro. Fra i disegni Servier gratuiti non c'è l'ileopsoas né un
"flessore dell'anca" isolato. Per i flessori si evidenzia la zona sul disegno
dell'adulto, non si disegna il muscolo.

## Effetti sonori

| file | origine e licenza | note |
|---|---|---|
| `sfx/*.mp3` (19 file: chime, click, click-soft, error, glitch-1/2/3, impact-bass-1/2, key-press, notification, ping, pop, riser, sparkle, typing, whoosh, whoosh-short, whoosh-cinematic) | Pixabay, [Pixabay Content License](https://pixabay.com/service/license-summary/): uso commerciale e non, modifiche e uso dentro un video, senza obbligo di attribuzione. Crediti in `sfx/CREDITS.md` | `sfx/manifest.json`: durata e uso consigliato di ogni file. Nel motore si usano solo quelli scelti nel confronto con i suoni sintetizzati (`motore/motore/sfx.py`, voce `LIBRERIA_SFX`) |

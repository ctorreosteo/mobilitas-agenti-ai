# Font: dove prenderli e cosa non usare

## Cosa serve

- **Montserrat** variabile (asse Weight 100-900) — la voce parlata
- **IBM Plex Mono** Bold e SemiBold — la voce dello strumento

```bash
curl -L -o assets/fonts/Montserrat-VF.ttf \
  "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf"
curl -L -o assets/fonts/IBMPlexMono-Bold.ttf \
  "https://github.com/google/fonts/raw/main/ofl/ibmplexmono/IBMPlexMono-Bold.ttf"
```

In Pillow il peso si sceglie sull'asse:

```python
f = ImageFont.truetype('assets/fonts/Montserrat-VF.ttf', 62)
f.set_variation_by_axes([900])
```

## Cosa NON usare

**I woff2 in `~/.cache/hyperframes/fonts/`.** Sono sottoinsiemi generati per una
pagina specifica: hanno 130-150 glifi invece di 700+, e mancano lettere comuni
(`J`, `K` in IBMPlexMono-700) e i trattini lunghi. Peggio, i file di pesi diversi
possono avere lo stesso contenuto: `900-normal-*.woff2` e `700-normal-*.woff2`
misurano identico e disegnano identico.

Il guaio e che **Pillow non protesta**: i glifi mancanti escono come spazi vuoti,
e te ne accorgi solo guardando il render. Prima di usare un font nuovo,
controlla la copertura:

```python
from fontTools.ttLib import TTFont
cmap = TTFont(path).getBestCmap()
need = "abc...ABC...0123456789àèéìòùÀÈÉÌÒÙ.,!?:;'\"%()-–—…"
print([c for c in need if ord(c) not in cmap])   # deve essere vuoto
```

## Accenti

Le etichette vanno scritte con gli accenti veri (`CAPACITÀ`, `IL CAFFÈ`,
`NON È ANSIA`), non con l'apostrofo. Il font li ha; usarli e questione di
correttezza tipografica, non di disponibilita.

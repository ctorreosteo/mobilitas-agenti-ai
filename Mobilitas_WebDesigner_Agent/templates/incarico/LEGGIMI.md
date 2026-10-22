# Incarico WebDesigner

Cartella di lavoro di un incarico, creata da `tools/incarico/nuovo.sh`. Sito, porte e impronta iniziale sono in `incarico.json`.

**La landing non sta qui:** è nel progetto del sito, in `src/pages/…`, con la sua route.

| Cartella | Contenuto |
|---|---|
| `brief/` | Verifica dei dati, strategia e copy, direzione, brief Superdesign, inventario delle dipendenze |
| `bozze/` | Bozze Superdesign (HTML) e registro delle chiamate |
| `visore/` | Bozze rese visibili in locale con le foto reali |
| `report/` | Resoconto, `modifiche.txt` (cosa è cambiato nel sito), controlli, `screenshot/` |
| `scartate/` | Materiale scartato (foto, varianti): si sposta qui, non si cancella |
| `runtime/` | Log e pid dei servizi, registro dello stato del sito, cache di Vite |

**Comandi**, dalla cartella dell'agente:

| Cosa | Comando |
|---|---|
| Avvia il sito in prova | `tools/sito/avvia.sh <incarico>` |
| Fermalo | `tools/sito/ferma.sh <incarico>` |
| Verifica delle modifiche al sito | `node tools/incarico/registro.cjs verifica <incarico>` |

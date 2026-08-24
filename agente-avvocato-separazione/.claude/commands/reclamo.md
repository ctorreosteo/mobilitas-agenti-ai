---
description: Decide e redige il reclamo contro i provvedimenti provvisori — dieci giorni, perentori
argument-hint: "[data dell'udienza o della comunicazione]"
---

Il giudice ha emesso i provvedimenti provvisori. **Hai dieci giorni.**

## Prima di ogni altra cosa: conta i giorni

L'`art. 473-bis.24 c.p.c.` dà un **termine perentorio di dieci giorni**, che decorre dalla
**pronuncia del provvedimento in udienza**, oppure dalla **comunicazione**, oppure dalla
**notificazione se anteriore**.

Il tranello è il primo dei tre: se l'ordinanza è stata pronunciata in udienza, il termine è partito
quel giorno — non quando la cancelleria ha comunicato il testo, non quando il cliente l'ha letta.

1. **Stabilisci da quale dei tre eventi decorre**, e con quale data.
2. **Apri subito la riga in `fascicolo/_dati/scadenze.md`**, prima di decidere se reclamare.
3. **Riverifica la norma sul web adesso**: il termine, la decorrenza e il regime della sospensione
   feriale. Questo agente non calcola termini processuali come se fossero certi.

Il metodo completo è in
`.claude/skills/difensore-famiglia-strategia/references/dopo-la-prima-udienza.md`.

## La prima domanda: è davvero un reclamo?

| Cos'è successo | Strada | Perché |
|---|---|---|
| Il provvedimento era sbagliato **sui fatti già acquisiti** | **Reclamo**, `473-bis.24` | Dieci giorni |
| Sono sopravvenuti **fatti nuovi** | **Modifica**, `473-bis.29` | La norma manda le circostanze sopravvenute davanti al giudice di merito: un reclamo su fatti nuovi sbaglia porta e consuma il termine |
| Il provvedimento va bene, **non viene rispettato** | **Attuazione**, `473-bis.39` | Si contesta per iscritto, si costruisce la serie |

Se la risposta non è la prima riga, **fermati e dillo**: il lavoro è un altro atto.

## Procedura, se si reclama

1. **Leggi l'ordinanza riga per riga** e isola i punti reclamabili. Non «l'ordinanza è ingiusta»:
   il fatto pacifico ignorato, il documento non considerato, il calendario motivato **solo**
   sull'età, il reddito attribuito e non documentato.
2. **Valuta il costo.** Il giudice che ha emesso il provvedimento resta il giudice della causa per
   anni. Si reclama su punti verificabili, freddo, e senza una riga sul giudice.
3. **Valuta il costo di non farlo.** Ciò che regge due anni diventa «l'assetto consolidato», e da
   lì in poi non basta più che un assetto migliore sia migliore: bisogna dimostrare che quello in
   piedi danneggia il bambino. L'onere si rovescia.
4. **Redigi**, con la revisione ridotta: il panel completo in dieci giorni non ci sta. Il manifesto
   `livelli.json` ha l'esempio `reclamo_ex_473_bis_24_dieci_giorni` — `giudice`, `avversario`,
   `decadenze`, `prove`, poi `fonti`, e si salta la riscrittura di chiarezza.
5. **Collauda comunque.** Il termine breve non sospende il cancello:

```bash
python3 .claude/skills/difensore-famiglia-strategia/scripts/verifica_atto.py \
  <reclamo.md> --tipo reclamo --registro fascicolo/_dati/registro-fonti.md \
  --prove <prove.md> --timeline fascicolo/_dati/timeline.md
```

6. **Apri la riga «decisione del collegio»**: sessanta giorni dal deposito.

## Chiusura

Riporta: **da quale evento decorre il termine e quando scade**, la raccomandazione (reclamare o
no) con una riga di motivazione, i punti reclamabili in elenco, cosa serve al cliente **entro
domani**, e — se la raccomandazione è di non reclamare — quale fatto sopravvenuto stiamo
costruendo per l'istanza di modifica, e con che tempi.

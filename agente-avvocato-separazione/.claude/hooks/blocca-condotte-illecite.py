#!/usr/bin/env python3
"""
Hook PreToolUse (Write|Edit|MultiEdit).

Blocca la redazione di materiale che CONSIGLIA all'assistito una delle condotte
che il perimetro dell'agente vieta.

Non e' moralismo: sono le sei condotte che trasformano un padre con ragione in un
indagato, e ognuna ha rovinato la causa di qualcuno. Un agente che le suggerisce
in un briefing fa un danno molto piu' grande di un atto scritto male.

Il controllo e' volutamente stretto: cerca la FORMA CONSIGLIO (imperativi e
suggerimenti rivolti al cliente), non la semplice menzione. Un file che SPIEGA
perche' non si sospende il mantenimento deve poter essere scritto: e' esattamente
il contenuto che serve.
"""

import json
import re
import sys

# (etichetta, pattern, perche')
REGOLE = [
    ('SOSPENSIONE DEL MANTENIMENTO',
     r'(?:puoi|potresti|conviene|ti consiglio di|sospendi|smetti di|blocca)\s+'
     r'(?:\w+\s+){0,3}(?:sospendere\s+|interrompere\s+|bloccare\s+|non\s+)?'
     r'(?:il\s+)?(?:versament|bonific|mantenimento|assegno|paga)',
     "art. 570-bis c.p., applicabile anche ai genitori non coniugati. "
     "Le visite negate e il mantenimento sono obbligazioni indipendenti: chi le compensa "
     "perde entrambe le partite, e la seconda in sede penale."),

    ('REGISTRAZIONE O ACCESSO ILLECITO',
     r'(?:puoi|potresti|conviene|ti consiglio di|installa|metti|piazza|entra)\s+'
     r'(?:\w+\s+){0,4}(?:telecamer|microfon|registrator|nel suo (?:telefono|account|profilo)|'
     r'nelle sue (?:mail|email|chat)|spyware|localizzator)',
     "artt. 615-bis e 615-ter c.p. E' reato, ed e' anche la prova che serviva a lei: "
     "la produzione rivela come e' stata ottenuta."),

    ('TRATTENIMENTO DEL MINORE',
     r'(?:puoi|potresti|conviene|ti consiglio di|tienilo|trattieni|non riportar|non consegnar|portalo)\s*'
     r'(?:\w+\s+){0,4}(?:oltre|piu\'? a lungo|non lo riporti|all\'estero|via|con te e non)',
     "artt. 574, 574-bis e 388 c.p., e in sede civile la fine dell'affidamento condiviso."),

    ('OCCULTAMENTO DI REDDITI',
     r'(?:puoi|potresti|conviene|ti consiglio di|non dichiarar|nascond|occulta|non deposit|ometti)\s*'
     r'(?:\w+\s+){0,4}(?:redditi|guadagni|conto|estratti conto|dichiarazion|beni|patrimonio)',
     "Il giudice ha poteri officiosi e puo' ordinare indagini di polizia tributaria. "
     "L'occultamento scoperto non fa perdere solo sul mantenimento: fa perdere la credibilita' "
     "su tutto, affidamento compreso."),

    ('DENUNCIA STRUMENTALE',
     r'(?:denuncia|querela|sporgi)\s+(?:\w+\s+){0,4}'
     r'(?:per (?:fare |mettere )?pressione|come leva|per ritorsione|tanto poi|anche se non)',
     "art. 368 c.p., e davanti al giudice civile il conflittuale diventa lui."),

    ('PROVE FABBRICATE',
     r'(?:crea|costruisci|prepara|inventa|modifica|ritocca|falsific)\s+(?:\w+\s+){0,3}'
     r'(?:un[a]? )?(?:prova|testimonianza|messaggio|screenshot|cronologia|documento)\s+'
     r'(?:fals|finto|ad hoc|retroattiv)',
     "Fine della causa e reato. Non si fa mai, per nessun motivo, nemmeno come bozza."),
]

COMPILATE = [(nome, re.compile(p, re.IGNORECASE), perche) for nome, p, perche in REGOLE]


def contenuto(tool: str, ti: dict) -> str:
    if tool == 'Write':
        return ti.get('content', '') or ''
    if tool == 'Edit':
        return ti.get('new_string', '') or ''
    if tool in ('MultiEdit', 'NotebookEdit'):
        parti = [e.get('new_string', '') or e.get('new_source', '') or ''
                 for e in ti.get('edits', [])]
        return '\n'.join(parti) + (ti.get('new_source', '') or '')
    return ''


def main():
    try:
        dati = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    testo = contenuto(dati.get('tool_name', ''), dati.get('tool_input', {}) or {})
    if not testo:
        sys.exit(0)

    trovate = []
    for nome, rx, perche in COMPILATE:
        m = rx.search(testo)
        if m:
            trovate.append((nome, m.group(0).strip()[:120], perche))

    if not trovate:
        sys.exit(0)

    righe = [f"  - {n}\n    Passaggio: \"{t}\"\n    {p}" for n, t, p in trovate]
    msg = (
        "CONDOTTA FUORI PERIMETRO nel materiale che stai scrivendo:\n\n"
        + '\n\n'.join(righe)
        + "\n\nQueste condotte non si consigliano mai. Non e' una questione morale: sono le "
          "condotte che trasformano un padre con ragione in un indagato, e sono anche quelle "
          "che funzionano peggio.\n\n"
          "Per ciascuna esiste una mossa legittima che ottiene lo stesso risultato, ed e' piu' "
          "efficace: ricorso d'urgenza invece del trattenimento, art. 473-bis.39 c.p.c. invece "
          "della compensazione, ricorso per la modifica invece della sospensione del "
          "mantenimento, conservazione dei messaggi ricevuti invece dell'accesso abusivo.\n\n"
          "Se stai SPIEGANDO al cliente perche' non deve farlo, riformula in forma negativa "
          "esplicita: \"non sospendere\", \"mai registrare in sua assenza\". Non aggirare "
          "questo blocco."
    )
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny',
            'permissionDecisionReason': msg,
        }
    }))
    sys.exit(0)


if __name__ == '__main__':
    main()

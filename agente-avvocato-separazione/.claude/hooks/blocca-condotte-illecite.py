#!/usr/bin/env python3
"""
Hook PreToolUse (Write|Edit|MultiEdit|NotebookEdit).

Blocca la redazione di materiale che CONSIGLIA all'assistito una delle condotte
che il perimetro dell'agente vieta.

Non e' moralismo: sono le condotte che trasformano un padre con ragione in un
indagato, e ognuna ha rovinato la causa di qualcuno. Un agente che le suggerisce
in un briefing fa un danno molto piu' grande di un atto scritto male, perche' il
briefing e' l'unico documento che il cliente legge davvero e mette in pratica.

Il controllo cerca la FORMA CONSIGLIO — imperativi e suggerimenti rivolti al
cliente — non la semplice menzione. Un file che SPIEGA perche' non si sospende
il mantenimento deve poter essere scritto: e' esattamente il contenuto che
serve, ed e' il motivo per cui ogni regola porta accanto i suoi casi di prova
in scripts/test-hooks.py.
"""

import json
import re
import sys

# La forma consiglio: chi la scrive sta dicendo al cliente di fare qualcosa.
CONSIGLIO = (r'(?:puoi|potresti|conviene|ti\s+conviene|ti\s+consiglio\s+di|consiglio\s+di|'
             r'valuta\s+di|prova\s+a|meglio\s+se|basta\s+che|fai\s+in\s+modo\s+di|'
             r'devi|dovresti|e[\'’]?\s+opportuno\s+che)')


def regola(verbi, imperativi, oggetti, distanza=6):
    """Costruisce il pattern di una condotta.

    Due rami, e la differenza fra i due e' tutto il mestiere di questo hook.

    Il ramo CONSIGLIO e' permissivo: dopo "potresti" o "ti conviene", accetta la
    radice del verbo con qualunque desinenza, perche' li' il consiglio c'e' gia'
    e la forma non cambia la sostanza.

    Il ramo IMPERATIVO e' letterale: accetta solo le forme esatte che si usano
    per dire a qualcuno di fare una cosa. Se accettasse le radici, la frase
    "la sospensione del mantenimento e' reato" verrebbe bloccata — cioe' l'hook
    impedirebbe di scrivere esattamente il contenuto che deve esistere.
    """
    return (r'(?:' + CONSIGLIO + r'\s+(?:\w+\s+){0,4}(?:' + '|'.join(verbi) + r')\w*'
            r'|\b(?:' + '|'.join(imperativi) + r')\b)'
            r'(?:\W+\w+){0,' + str(distanza) + r'}?\W+(?:' + '|'.join(oggetti) + r')')


# (etichetta, pattern, perche')
REGOLE = [
    ('SOSPENSIONE DEL MANTENIMENTO',
     regola(
         verbi=['sospend', 'interromp', 'blocc', 'ridur', 'trattien'],
         imperativi=['sospendi', 'interrompi', 'blocca', 'riduci',
                     r'smetti\s+di\s+(?:pagare|versare|bonificare)',
                     r'non\s+(?:versare|pagare|bonificare)\s+piu[\'’]?'],
         oggetti=['versament', 'bonific', 'mantenimento', 'assegno', 'contributo',
                  'pagament', 'rata']),
     "art. 570-bis c.p., applicabile anche ai genitori non coniugati. "
     "Le visite negate e il mantenimento sono obbligazioni indipendenti: chi le compensa "
     "perde entrambe le partite, e la seconda in sede penale. "
     "La mossa legittima e' il ricorso per la modifica delle condizioni, ex art. 473-bis.29 "
     "c.p.c., mentre si continua a versare."),

    ('REGISTRAZIONE O ACCESSO ILLECITO',
     regola(
         verbi=['install', 'mett', 'piazz', 'nascond', 'entr', 'acced', 'registr',
                'riprend', 'controll', 'legg'],
         imperativi=['installa', 'installagli', 'metti', 'piazza', 'nascondi', 'entra',
                     'accedi', 'registra', 'riprendi', 'controllale', 'controllagli',
                     'guardale', 'leggile', 'aprile'],
         oggetti=['telecamer', 'microfon', 'registrator', 'spyware', 'localizzator', 'gps',
                  r'nel\s+suo\s+(?:telefono|account|profilo|computer|pc)',
                  r'nelle\s+sue\s+(?:mail|email|chat|conversazioni)',
                  r'(?:il\s+)?suo\s+(?:telefono|account|profilo|cellulare)',
                  r'in\s+casa\s+(?:sua|di\s+lei)', r'a\s+casa\s+(?:sua|di\s+lei)']),
     "artt. 615-bis e 615-ter c.p. E' reato, ed e' anche la prova che serviva a lei: "
     "la produzione in giudizio rivela come e' stata ottenuta. "
     "Resta lecito registrare le conversazioni A CUI SI PARTECIPA e conservare i messaggi "
     "ricevuti."),

    ('TRATTENIMENTO DEL MINORE',
     regola(
         verbi=['tener', 'trattener', r'non\s+riportar', r'non\s+consegnar', 'portar',
                'ten', 'tienil'],
         imperativi=['tienilo', 'trattienilo', 'trattieni', 'portalo', 'portatelo',
                     r'non\s+riportarlo', r'non\s+consegnarlo', r'non\s+riportare',
                     r'non\s+consegnare'],
         oggetti=['oltre', r'piu[\'’]?\s+a\s+lungo', r'qualche\s+giorno',
                  r'all[\'’]?estero', r'da\s+te', r'con\s+te', 'via',
                  r'un[\'’]?altra\s+settimana', r'fino\s+a\s+quando',
                  r'finche[\'’]?']),
     "artt. 574, 574-bis e 388 c.p., e in sede civile la fine dell'affidamento condiviso. "
     "La mossa legittima e' il ricorso d'urgenza e l'art. 473-bis.39 c.p.c."),

    ('OCCULTAMENTO DI REDDITI',
     regola(
         verbi=[r'non\s+dichiarar', 'nascond', 'occulta', r'non\s+deposit', 'omett',
                'intestar', 'spostar', 'svuotar', 'alleggerir'],
         imperativi=[r'non\s+dichiarare', 'nascondi', 'occulta', r'non\s+depositare',
                     'ometti', 'intesta', 'sposta', 'svuota',
                     r'fatti\s+pagare\s+in\s+(?:contanti|nero)'],
         oggetti=['redditi', 'guadagni', 'conto', r'estratti\s+conto', 'dichiarazion',
                  'beni', 'patrimonio', 'fatturat', 'compens', 'risparmi', 'quote']),
     "Il giudice ha poteri officiosi e puo' ordinare indagini di polizia tributaria. "
     "L'occultamento scoperto non fa perdere solo sul mantenimento: fa perdere la credibilita' "
     "su tutto, affidamento compreso. Si documenta tutto e si argomenta sulla proporzione."),

    ('DENUNCIA STRUMENTALE',
     regola(
         verbi=['denunc', 'querel', 'sporg'],
         imperativi=['denunciala', 'querelala', 'sporgi', 'denuncia', 'querela'],
         oggetti=[r'per\s+(?:fare\s+|mettere\s+)?pressione', r'come\s+leva',
                  r'per\s+ritorsione', r'per\s+bilanciare', r'tanto\s+poi',
                  r'anche\s+se\s+non', r'cosi[\'’]?\s+(?:si\s+calma|la\s+fermi)',
                  r'per\s+rispondere\s+alla\s+sua', r'per\s+controbilanciare']),
     "art. 368 c.p., e davanti al giudice civile il conflittuale diventa lui. "
     "Si costruisce prima l'archiviazione, e la controdenuncia si valuta a freddo con il "
     "provvedimento in mano."),

    ('PROVE FABBRICATE',
     regola(
         verbi=['cre', 'costruisc', 'prepar', 'invent', 'modific', 'ritocc', 'falsific',
                'ricostruisc', 'antedat', 'retrodat'],
         imperativi=['crea', 'costruisci', 'prepara', 'inventa', 'modifica', 'ritocca',
                     'falsifica', 'ricostruisci', 'antedata', 'retrodata'],
         oggetti=[r'prov[ae]\b', 'testimonianz', 'messagg', 'screenshot', 'cronologia',
                  'document', 'chat', 'conversazion'],
         distanza=4)
     + r'(?:\W+\w+){0,3}?\W*(?:fals|finto|finta|ad\s+hoc|retroattiv|che\s+non\s+(?:c[\'’]|e|ha)|'
       r'come\s+se)',
     "Fine della causa e reato. Non si fa mai, per nessun motivo, nemmeno come bozza."),

    # --- le due condotte che mancavano, e sono fra le piu' frequenti ---

    ('ISTRUZIONE DI UN TESTIMONE',
     regola(
         verbi=[r'far\s+dire', r'dirgli\s+di', r'dirle\s+di', 'convinc', 'accordar',
                'concordar', 'prepar', 'istruir'],
         imperativi=[r'digli\s+di\s+dire', r'dille\s+di\s+dire', r'fagli\s+dire',
                     r'falle\s+dire', r'fatti\s+dire', r'mettetevi\s+d[\'’]accordo',
                     'accordatevi', 'concordate', r'fatti\s+scrivere'],
         oggetti=[r'che\s+(?:ha|hai|era|eri|c[\'’]eri|non|ti)', 'testimoni',
                  'dichiarazion', r'in\s+udienza', r'al\s+giudice',
                  r'davanti\s+al\s+giudice', r'la\s+stessa\s+(?:cosa|versione)',
                  r'la\s+versione'],
         distanza=8),
     "art. 377 c.p. (subornazione) e art. 372 c.p. per chi depone. "
     "E' anche la mossa che si smonta piu' facilmente: due testimoni con la stessa versione "
     "imparata a memoria distruggono la credibilita' di chi li ha portati. "
     "Un teste si sente su CIO' CHE HA VISTO, e lo si sceglie per quello."),

    ('DISTRUZIONE DI PROVE',
     regola(
         verbi=['cancell', 'elimin', 'distrugg', 'svuot', 'resett', 'disinstall',
                r'sbarazzar'],
         imperativi=['cancella', 'cancellale', 'cancellali', 'elimina', 'distruggi',
                     'svuota', 'resetta', 'disinstalla', r'sbarazzati\s+di'],
         oggetti=['messagg', 'chat', 'conversazion', 'cronologia', 'email', r'mail\b',
                  'foto', 'registrazion', r'prov[ae]\b', 'documenti', 'account',
                  'profilo']),
     "Cancellare non ripulisce niente: i messaggi stanno anche sul telefono di lei, e la "
     "cancellazione e' un fatto che si accerta e che pesa. In sede penale puo' integrare "
     "condotte proprie, e in sede civile racconta al giudice esattamente cio' che si voleva "
     "nascondere. La regola da dare al cliente e' l'opposta: NON CANCELLARE NIENTE, e "
     "conservare tutto in copia."),
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
            trovate.append((nome, ' '.join(m.group(0).split())[:120], perche))

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
          "efficace: la trovi scritta qui sopra, accanto alla condotta.\n\n"
          "Se stai SPIEGANDO al cliente perche' non deve farlo, riformula in forma negativa "
          "esplicita: \"non sospendere\", \"mai registrare in sua assenza\", \"non cancellare "
          "niente\". Non aggirare questo blocco."
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

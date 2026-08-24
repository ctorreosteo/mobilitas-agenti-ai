#!/usr/bin/env python3
"""
Hook PreToolUse (Write|Edit|MultiEdit|NotebookEdit).

Blocca le tre cose che il metodo vieta in un atto e che finora nessuno
impediva: la PAS, l'etichetta NON SOSTENIBILE, l'attacco alla persona.

Erano gia' scritte nella costituzione dell'agente, in tre file di riferimento e
in due checklist. Ma una regola ripetuta in cinque documenti e verificata da
nessuno e' una regola che vale finche' il modello se la ricorda — cioe' finche'
il contesto non si riempie, che e' esattamente il momento in cui si scrive
l'atto finale.

## Perche' proprio queste tre

**La PAS.** Non ha ingresso nel processo italiano. Invocarla non fa perdere il
punto: colloca l'atto, e chi lo firma, dalla parte di chi psicologizza invece di
documentare. Al suo posto si scrivono condotte ostative con le date.

**NON SOSTENIBILE.** E' l'etichetta che significa "il cliente lo afferma, nulla
lo sorregge". In un atto e' la cosa che perde le cause: la controparte la
smonta e con quella contamina i fatti veri che le stanno accanto.

**L'attacco alla persona.** «madre manipolatrice» sposta il giudizio dal
comportamento documentato alla persona, e il giudice difende la persona. Il tono
di un atto, in questa materia, e' materiale probatorio a carico di chi lo
deposita.

## Il perimetro del controllo

Vale SOLO sui file destinati al deposito. La strategia, i briefing e gli appunti
restano liberi: una strategia deve poter scrivere "questo e' NON SOSTENIBILE" e
"non invocare la PAS", e un controllo che glielo impedisse verrebbe spento.

E si controlla solo cio' che il testo CONTIENE, mai cio' che gli manca: un hook
vede un frammento di Edit, non il documento finito. Le assenze — il piede, le
domande in prima pagina, il piano genitoriale — le verifica verifica_atto.py,
che il documento intero ce l'ha davanti.
"""

import json
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]
SCRIPTS = RADICE / '.claude' / 'skills' / 'difensore-famiglia-strategia' / 'scripts'

CARTELLE_SORVEGLIATE = ('/atti/', '/penale/', '/consegna/')
NOMI_SORVEGLIATI = ('ricorso', 'memoria', 'comparsa', 'istanza', 'atto',
                    'nota-pm', 'querela', 'reclamo', 'accordo')


def blocca(msg: str):
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny',
            'permissionDecisionReason': msg,
        }
    }))
    sys.exit(0)


sys.path.insert(0, str(SCRIPTS))
try:
    import riferimenti as R
except Exception as e:  # pragma: no cover
    blocca(f"PROTEZIONE NON DISPONIBILE: {SCRIPTS}/riferimenti.py non caricabile ({e}). "
           f"Ripristina il modulo e rilancia ./scripts/test-hooks.py.")


def sorvegliato(path: str) -> bool:
    p = path.replace('\\', '/').lower()
    if any(c in p for c in CARTELLE_SORVEGLIATE):
        return True
    nome = p.rsplit('/', 1)[-1]
    return any(n in nome for n in NOMI_SORVEGLIATI)


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

    ti = dati.get('tool_input', {}) or {}
    path = ti.get('file_path', '') or ti.get('notebook_path', '')
    if not path or not sorvegliato(path):
        sys.exit(0)

    testo = contenuto(dati.get('tool_name', ''), ti)
    if not testo:
        sys.exit(0)

    trovati = []

    m = R.RE_PAS.search(testo)
    if m:
        trovati.append((
            'PAS / ALIENAZIONE PARENTALE', m.group(0),
            "La sindrome di alienazione parentale non ha ingresso nel processo italiano: un "
            "provvedimento sull'affidamento non puo' fondarsi su una consulenza che si limiti a "
            "diagnosticarla. Invocarla brucia la credibilita' dell'intero atto e colloca chi la "
            "invoca fra chi psicologizza invece di documentare.\n"
            "    Al suo posto: le CONDOTTE OSTATIVE DOCUMENTATE, una per una, con le date e gli "
            "allegati, e la richiesta ex art. 473-bis.39 c.p.c. Una tabella con dieci date e "
            "dieci allegati ottiene cio' che la parola PAS fa perdere."))

    if 'NON SOSTENIBILE' in testo:
        trovati.append((
            'ETICHETTA NON SOSTENIBILE IN UN ATTO', 'NON SOSTENIBILE',
            "NON SOSTENIBILE significa: il cliente lo afferma, nulla lo sorregge. In un atto e' "
            "la cosa che perde le cause — la controparte lo smonta e con quello contamina i fatti "
            "veri che gli stanno accanto. Un'affermazione falsa costa piu' di dieci affermazioni "
            "mancanti.\n"
            "    Le uscite: togli il fatto dall'atto e tienilo nella strategia come rischio; "
            "oppure procurati il documento e portalo a DOCUMENTABILE con l'istanza di "
            "acquisizione accanto."))

    m = R.RE_PERSONA.search(testo)
    if m:
        trovati.append((
            'ATTACCO ALLA PERSONA', ' '.join(m.group(0).split())[:120],
            "In questa materia il tono dell'atto e' materiale probatorio, e un atto astioso verso "
            "la madre e' la prova che il padre e' conflittuale — prodotta e depositata da noi. Una "
            "qualificazione della persona sposta il giudizio dal comportamento documentato alla "
            "persona, e il giudice difende la persona.\n"
            "    Si riscrive come CONDOTTA CON LA DATA: non \"madre ostruttiva\" ma \"in data X e "
            "in data Y il minore non e' stato consegnato all'orario previsto (all. 4, 5)\". Il "
            "fatto resta, l'aggettivo esce, e l'atto diventa piu' difficile da attaccare."))

    if not trovati:
        sys.exit(0)

    righe = [f"  - {n}\n    Passaggio: \"{t}\"\n    {p}" for n, t, p in trovati]
    blocca(
        "DIFETTO CHE NON PUO' STARE IN UN ATTO:\n\n" + '\n\n'.join(righe)
        + "\n\nQuesti tre difetti non si negoziano e non hanno eccezioni d'urgenza: sono i modi "
          "in cui un atto forte nel merito viene perso sulla forma.\n\n"
          "Se stai scrivendo una STRATEGIA, un BRIEFING o degli APPUNTI, il controllo non si "
          "applica: spostali fuori dalle cartelle /atti/, /penale/ e /consegna/ e da un nome di "
          "file che sembri un atto. Non aggirare questo blocco riformulando il difetto."
    )


if __name__ == '__main__':
    main()

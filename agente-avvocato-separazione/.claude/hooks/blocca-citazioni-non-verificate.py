#!/usr/bin/env python3
"""
Hook PreToolUse (Write|Edit|MultiEdit|NotebookEdit).

Impedisce che una citazione giurisprudenziale NON verificata finisca in un file
destinato al deposito.

E' la regola piu' importante dell'agente, applicata materialmente invece che
raccomandata: il numero di una sentenza e' il punto in cui un modello
linguistico inventa con la massima verosimiglianza, e una citazione inesistente
in un atto non fa perdere quel punto — fa perdere la credibilita' su tutto
l'atto, comprese le venti affermazioni vere.

Due cose che questo hook fa e che vale la pena sapere:

1. Riconosce la citazione nella forma in cui gli atti italiani la scrivono
   davvero — "Cass. civ., sez. I, 12 marzo 2020, n. 9764" — e non solo nella
   forma comoda "Cass. n. 9764/2019". La forma comoda e' quella che un
   controllo ingenuo intercetta; l'altra e' quella che passa.

2. Pretende il livello CONFERMATA, non la semplice presenza nel registro. Una
   fonte PARZIALE e' una fonte di cui conosciamo il principio e non il testo
   ufficiale: il principio si cita, il numero no.

Se l'hook blocca, la strada NON e' aggirarlo: e' verificare la fonte sul web,
registrarla in append nel registro, e riscrivere.
"""

import json
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]
REGISTRO = RADICE / 'fascicolo' / '_dati' / 'registro-fonti.md'
SCRIPTS = RADICE / '.claude' / 'skills' / 'difensore-famiglia-strategia' / 'scripts'

# Solo i file che sono ATTI o materiale destinato al deposito.
# La strategia, i briefing e gli appunti restano liberi: e' li' che si ragiona,
# ed e' giusto poter scrivere "da verificare: Cass. 9764/2019".
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
    # Fallire aperto qui significherebbe che, il giorno in cui il modulo si
    # rompe, ogni citazione inventata passa in silenzio. Si fallisce chiusi.
    blocca(
        f"PROTEZIONE NON DISPONIBILE: non riesco a caricare {SCRIPTS}/riferimenti.py ({e}).\n\n"
        f"Finche' il controllo sulle citazioni non funziona, nessun atto puo' essere scritto. "
        f"Ripristina il modulo e rilancia ./scripts/test-hooks.py."
    )


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

    tool = dati.get('tool_name', '')
    ti = dati.get('tool_input', {}) or {}
    path = ti.get('file_path', '') or ti.get('notebook_path', '')

    if not path or not sorvegliato(path):
        sys.exit(0)

    testo = contenuto(tool, ti)
    if not testo:
        sys.exit(0)

    citate = R.citazioni(testo)
    if not citate:
        sys.exit(0)

    livelli = R.registro_livelli(REGISTRO)
    if livelli is None:
        blocca(
            f"Registro delle fonti non trovato ({REGISTRO}). "
            f"Nessuna citazione numerata puo' entrare in un atto finche' non esiste il registro."
        )

    problemi = []
    for c in sorted(citate):
        liv = livelli.get(c)
        if c.endswith('/senza-anno'):
            problemi.append((c, "citata senza anno: e' inverificabile per costruzione"))
        elif liv is None:
            problemi.append((c, 'non compare nel registro delle fonti'))
        elif liv == 'PARZIALE':
            problemi.append((c, 'registrata come PARZIALE: il principio si cita, il numero no'))
        elif liv != 'CONFERMATA':
            problemi.append((c, f'registrata come {liv}'))

    if problemi:
        elenco = '\n'.join(f"  - n. {c} — {perche}" for c, perche in problemi)
        blocca(
            f"CITAZIONE NON CITABILE IN UN ATTO:\n\n{elenco}\n\n"
            f"Nel registro (fascicolo/_dati/registro-fonti.md) puo' entrare in un atto CON IL "
            f"NUMERO solo cio' che e' registrato come CONFERMATA, cioe' di cui e' stato letto il "
            f"testo o la massima ufficiale.\n\n"
            f"Il numero di una sentenza e' il punto in cui si inventa con la massima "
            f"verosimiglianza, e una citazione inesistente non fa perdere quel punto: fa perdere "
            f"la credibilita' su tutto l'atto, comprese le venti affermazioni vere.\n\n"
            f"Le tre uscite, in ordine:\n"
            f"  1. Cercala sul web, verifica CHE ESISTE e CHE DICE QUELLO, e registrala in "
            f"append nel registro con livello CONFERMATA.\n"
            f"  2. Se trovi solo fonti secondarie concordi: registrala come PARZIALE e scrivi "
            f"nell'atto il PRINCIPIO SENZA IL NUMERO "
            f"(\"secondo l'orientamento consolidato di legittimita'...\").\n"
            f"  3. Se non trovi conferma: non citarla, e annotala fra le fonti NON trovate.\n\n"
            f"Non aggirare questo blocco."
        )
    sys.exit(0)


if __name__ == '__main__':
    main()

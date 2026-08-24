#!/usr/bin/env python3
"""
Hook PreToolUse (Write|Edit|MultiEdit).

Impedisce che un numero di sentenza NON presente nel registro delle fonti
verificate finisca in un file di atto.

E' la regola piu' importante dell'agente, applicata materialmente invece che
raccomandata: il numero di una sentenza e' il punto in cui un modello linguistico
inventa con la massima verosimiglianza, e una citazione inesistente in un atto
non fa perdere quel punto — fa perdere la credibilita' su tutto l'atto.

Se l'hook blocca, la strada NON e' aggirarlo: e' verificare la fonte sul web,
registrarla in append nel registro, e riscrivere.
"""

import json
import re
import sys
from pathlib import Path

REGISTRO = Path(__file__).resolve().parents[2] / 'fascicolo' / '_dati' / 'registro-fonti.md'

# Solo i file che sono ATTI o materiale destinato al deposito.
# La strategia, i briefing e gli appunti restano liberi: e' li' che si ragiona.
CARTELLE_SORVEGLIATE = ('/atti/', '/penale/', '/consegna/')
NOMI_SORVEGLIATI = ('ricorso', 'memoria', 'comparsa', 'istanza', 'atto', 'nota-pm', 'querela')

RE_SENTENZA = re.compile(
    r'(?:Cass(?:azione)?\.?(?:\s+(?:civ|pen|SS\.?UU|Sez\.?\s*Un)\.?)?|sent(?:enza)?\.?|ord(?:inanza)?\.?)'
    r'[\s,]*n?\.?\s*(\d{1,6})\s*/\s*(\d{4})',
    re.IGNORECASE)


def sorvegliato(path: str) -> bool:
    p = path.replace('\\', '/').lower()
    if any(c in p for c in CARTELLE_SORVEGLIATE):
        return True
    nome = p.rsplit('/', 1)[-1]
    return any(n in nome for n in NOMI_SORVEGLIATI)


def verificate():
    """Numeri di sentenza presenti nel registro, esclusa la sezione NON trovate."""
    if not REGISTRO.exists():
        return set(), False
    testo = REGISTRO.read_text(encoding='utf-8')
    testo = re.split(r'^##\s+Fonti cercate e NON trovate', testo, flags=re.MULTILINE)[0]
    return {f"{m.group(1)}/{m.group(2)}" for m in RE_SENTENZA.finditer(testo)}, True


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


def blocca(msg: str):
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny',
            'permissionDecisionReason': msg,
        }
    }))
    sys.exit(0)


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

    citate = {f"{m.group(1)}/{m.group(2)}" for m in RE_SENTENZA.finditer(testo)}
    if not citate:
        sys.exit(0)

    ok, esiste = verificate()
    if not esiste:
        blocca(
            f"Registro delle fonti non trovato ({REGISTRO}). "
            f"Nessuna citazione numerata puo' entrare in un atto finche' non esiste il registro."
        )

    mancanti = sorted(citate - ok)
    if mancanti:
        elenco = ', '.join(f"n. {m}" for m in mancanti)
        blocca(
            f"CITAZIONE NON VERIFICATA: {elenco}\n\n"
            f"Questi riferimenti non compaiono nel registro delle fonti verificate "
            f"(fascicolo/_dati/registro-fonti.md) e non possono entrare in un atto.\n\n"
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

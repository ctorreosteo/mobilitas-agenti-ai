"""Catalogo dei modelli grafici (fase 7c, regola di Riccardo del 01/11/2026: nessun modello si dimentica).

Fonte: `motore/inserti/CATALOGO-MODELLI.json` (lo legge il motore); `CATALOGO-MODELLI.md` si
rigenera da qui. Stati: `attivo` (si usa), `variante` (versione precedente di un modello
migliorato, resta disponibile), `vietato` (solo la sagoma vettoriale e il telefono con la
sagoma: restano nel codice, mai nei video nuovi). Si aggiunge e basta: niente si cancella
o si declassa senza l'ok di Riccardo.

Il motore lo usa in `scena`:
- un momento che usa un modello vietato -> errore;
- lo stesso modello in due momenti di fila (camera viva esclusa) -> errore;
- a fine `scena`, i modelli usati vanno in `libreria/uso-modelli.json`, per variare fra un
  video e l'altro (`./mve catalogo <slug>` mostra cosa e stato usato di recente).
"""
import json
import subprocess
import sys
from pathlib import Path

from .progetto import AGENTE, LIBRERIA

CATALOGO = AGENTE / 'motore' / 'inserti' / 'CATALOGO-MODELLI.json'
ESEMPI = AGENTE / 'motore' / 'inserti' / 'catalogo'
USO = LIBRERIA / 'uso-modelli.json'


def carica():
    return json.loads(CATALOGO.read_text(encoding='utf-8'))


def per_id():
    return {m['id']: m for m in carica()['modelli']}


def identifica(x):
    """l'id del catalogo per un elemento di un momento (modello + opzioni che fanno la variante)"""
    mod, d = x.get('modello'), x.get('dati', {})
    if mod == 'etichette_luce':
        return 'etichette-barrate-classiche' if d.get('luce') == 'classica' else 'etichette-barrate'
    if mod == 'etichette_ads':   # laboratorio (fase 1, 03/11/2026): solo in aggiunta
        if d.get('modo') == 'finestra':
            return 'etichette-barrate-finestra'
        return 'etichette-barrate-9x16-sottotitoli' if d.get('fascia') else 'etichette-barrate-9x16'
    if mod == 'card_accese_ads':  # laboratorio (fase 2, 03/11/2026): solo in aggiunta
        return 'card-accese-9x16'
    if mod in ('equazione_ads2', 'chiusura_ads2'):  # laboratorio (fase 5, 04/11/2026): varianti 2, solo in aggiunta
        return {'equazione_ads2': 'equazione-finestra-v2', 'chiusura_ads2': 'chiusura-9x16-v2'}[mod]
    if mod == 'etichette_ads2':
        return 'etichette-barrate-finestra-v2' if d.get('modo') == 'finestra' else 'etichette-barrate-pieno-v2'
    nuovi_ads = {'connettore_ads': 'connettore-finestra', 'card_carrello_ads': 'card-accese-9x16-carrello',
                 'etichette_centrate_ads': 'etichette-barrate-finestra-centrate', 'parole_ads': 'parole-finestra',
                 'anatomia_ads': 'anatomia-scena-9x16', 'fumetto_ads': 'fumetto-finestra', 'riga_icone_ads': 'riga-icone-9x16'}
    if mod == 'persona_reel':   # agente reel-grafiche (fase 6, 05/11/2026): modelli sulla persona in 9:16, in prova
        return {'titolo': 'titolo-dietro-9x16', 'numero': 'numero-dietro-9x16', 'frase': 'frase-sul-corpo-9x16', 'card': 'card-mani-9x16',
                'cerchio': 'cerchio-9x16'}[d.get('tipo', 'titolo')]
    if mod == 'micro_reel':     # agente reel-grafiche (fase 6, 05/11/2026): micro-grafiche, in prova, solo in aggiunta
        return 'micro-' + d.get('tipo', 'parola')
    if mod == 'infografica_reel':   # fase 6, giro 4 (05/11/2026): infografiche vere, in prova, solo in aggiunta
        if d.get('modo') == 'palco':   # 07/11/2026 («nuova direzione»): il palco del reel, in prova
            return 'palco-fascia-alta'
        if d.get('modo') == 'libero':
            return 'infografica-persona' if d.get('dietro') else 'infografica-sopra'
        if d.get('modo') == 'tutto':
            return 'infografica-cerchio-9x16' if d.get('foro') else 'infografica-9x16'
        return 'infografica-finestra'
    # fase 6, giro 4: le etichette barrate e le parole con un'icona per voce (varianti in prova, solo in aggiunta)
    if mod == 'etichette_centrate_ads' and any(v.get('icona') for v in d.get('voci', [])):
        return 'etichette-barrate-finestra-centrate-icone'
    if mod == 'parole_ads' and any(v.get('icona') for v in d.get('parole', [])):
        return 'parole-finestra-icone'
    if mod == 'aggancio_ads':   # prova dell'aggancio su AD_COLON (04/11/2026), in prova
        return 'aggancio-finestra' if d.get('modo') == 'finestra' else 'aggancio-9x16'
    if mod in nuovi_ads:   # laboratorio (collaudo AD_REFLUSSO, 04/11/2026): modelli nuovi in prova, solo in aggiunta
        return nuovi_ads[mod]
    if mod in ('equazione_ads', 'chiusura_ads', 'card_spessore_ads'):  # laboratorio (fase 3, 04/11/2026): solo in aggiunta
        return {'equazione_ads': 'equazione-finestra', 'chiusura_ads': 'chiusura-9x16', 'card_spessore_ads': 'card-con-spessore-9x16'}[mod]
    if mod == 'schermata':
        return 'schermata-velo' if d.get('fondo') == 'velo' else 'schermata'
    if mod == 'frase_luce':
        v = d.get('vetro')
        return 'frase-chiave-vetro' if v and v.get('forte') else 'frase-chiave-vetro-classico'
    if mod == 'titolo_dietro' and d.get('forma') == 'maiuscolo':
        return 'titolo-dietro-maiuscolo'
    if mod in ('cta', 'lista_attesa', 'chiusura') and d.get('forma') == 'classica':
        return {'cta': 'cta-link-classica', 'lista_attesa': 'lista-attesa-classica', 'chiusura': 'chiusura-classica'}[mod]
    if mod == 'telefono3d':
        if any(s.get('genera') == 'foto_sagoma' for s in d.get('schermate', [])):
            return 'telefono-sagoma'
        return 'telefono-prospettiva'
    if mod == 'card':
        return 'card-dietro-la-spalla' if any(c.get('dietro') for c in d.get('card', [])) else 'card-fluttuanti'
    if mod == 'anatomia':
        p = d.get('pannello') or {}
        return 'anatomia-scena' if (not p or p.get('larghezza', 1920) >= 1900) else 'anatomia-card'
    nomi = {'parole': 'frase-sul-corpo', 'numero_dietro': 'numero-dietro', 'titolo_dietro': 'titolo-dietro',
            'frase_chiave': 'frase-chiave-pannello', 'equazione': 'equazione', 'connettore': 'connettore',
            'linea_tempo': 'linea-tempo', 'tentativi': 'tentativi', 'riga_icone': 'riga-icone',
            'card_accese': 'card-accese', 'card_spessore': 'card-con-spessore', 'fumetti': 'fumetti',
            'lista_attesa': 'lista-attesa', 'cta': 'cta-link', 'chiusura': 'chiusura', 'foto_card': 'foto-card',
            'confronto': 'prima-dopo-cursore', 'sagoma': 'sagoma-vettoriale', 'fine_youtube': 'schermata-finale-youtube'}
    return nomi.get(mod, mod)


def modelli_del_momento(m):
    ids = [identifica(x) for x in m.get('elementi', []) if x.get('modello') != 'etichetta']
    for p in m.get('piatto', []):
        if p.get('tipo') == 'finestra':
            ids.append('lui-nel-cerchio' if p.get('cerchio') else 'finestra-inclinata')
    return ids


def controlla(momenti):
    """vietati e ripetizioni di fila: torna l'elenco dei problemi (vuoto = va bene)"""
    cat = per_id()
    prob, prima = [], None
    for m in momenti:
        ids = modelli_del_momento(m)
        for i in ids:
            if cat.get(i, {}).get('stato') == 'vietato':
                prob.append(f"{m['id']}: modello vietato «{i}» (bocciato da Riccardo)")
            if i not in cat:
                prob.append(f"{m['id']}: modello «{i}» non e nel catalogo: aggiungilo prima di usarlo")
        prin = ids[0] if ids else None
        if prin and prin == prima:
            prob.append(f"{m['id']}: «{prin}» due volte di fila")
        if prin:
            prima = prin
    return prob


def registra_uso(slug, momenti):
    uso = json.loads(USO.read_text(encoding='utf-8')) if USO.exists() else {}
    conta = {}
    for m in momenti:
        for i in modelli_del_momento(m):
            conta[i] = conta.get(i, 0) + 1
    uso[slug] = conta
    USO.write_text(json.dumps(uso, ensure_ascii=False, indent=1), encoding='utf-8')


def catalogo(slug=None):
    """./mve catalogo [slug]: i modelli attivi per famiglia, con l'uso nei video precedenti"""
    cat = carica()['modelli']
    uso = json.loads(USO.read_text(encoding='utf-8')) if USO.exists() else {}
    fam = {}
    for m in cat:
        fam.setdefault(m['famiglia'], []).append(m)
    for f, ms in fam.items():
        print(f"== {f}")
        for m in ms:
            usi = [v for v, c in uso.items() if m['id'] in c and v != slug]
            print(f"  {m['stato']:<8} {m['id']:<30} voto {str(m['ultimo_voto'])[:28]:<28} usato in: {', '.join(usi) or '-'}"
                  + (f"  [condizioni: {', '.join(m['condizioni'])}]" if m['condizioni'] else ''))


def esempi():
    """estrae il fotogramma d'esempio di ogni modello (motore/inserti/catalogo/<id>.jpg)"""
    ESEMPI.mkdir(parents=True, exist_ok=True)
    for m in carica()['modelli']:
        e = m.get('esempio_da')
        if not e:
            continue
        src, t = AGENTE / e[0], e[1]
        out = ESEMPI / f"{m['id']}.jpg"
        if not src.exists():
            print(f"  manca {e[0]}")
            continue
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f"{t:.2f}", '-i', str(src), '-frames:v', '1',
                        '-vf', 'scale=960:-2,format=yuvj420p', '-q:v', '3', str(out)], check=True)
        m['esempio'] = f"motore/inserti/catalogo/{out.name}"


def md():
    """CATALOGO-MODELLI.md dal json"""
    C = carica()
    L = ['# Catalogo dei modelli grafici', '',
         "Generato da `CATALOGO-MODELLI.json` (`python -m motore.catalogo md`). **Nessun modello si dimentica** "
         "(Riccardo, 01/11/2026): si aggiunge e basta; niente si cancella o si declassa senza l'ok di Riccardo.", '',
         '- **attivo**: si usa;', '- **variante**: versione precedente di un modello migliorato, resta disponibile;',
         '- **vietato**: solo la sagoma vettoriale e il telefono con la sagoma (bocciati da Riccardo): restano nel codice, mai nei video nuovi.', '',
         "Ogni piano grafico parte dal catalogo **intero**: si sceglie per occasione, si mescolano le famiglie, non si usa tutto in "
         "ogni video, mai lo stesso modello due volte di fila (lo controlla `scena`). L'uso per video è in `libreria/uso-modelli.json`. "
         "Gli esempi di non regressione sono in `campionario/regressione/`.", '']
    n = {s: sum(1 for m in C['modelli'] if m['stato'] == s) for s in ('attivo', 'variante', 'vietato')}
    L += [f"**{len(C['modelli'])} modelli**: {n['attivo']} attivi, {n['variante']} varianti, {n['vietato']} vietati.", '']
    fam = {}
    for m in C['modelli']:
        fam.setdefault(m['famiglia'], []).append(m)
    for f, ms in fam.items():
        L += [f"## {f}", '']
        for m in ms:
            L += [f"### {m['nome']} (`{m['id']}`, {m['stato']})", '']
            if m.get('esempio'):
                L += [f"![{m['id']}](catalogo/{Path(m['esempio']).name})", '']
            L += [f"- **Cosa fa:** {m['cosa_fa']}", f"- **Quando:** {m['quando']}", f"- **Quando no:** {m['quando_no']}"]
            if m['condizioni']:
                L += [f"- **Condizioni (controllate dal motore):** {', '.join(m['condizioni'])}"]
            L += [f"- **Reference:** {m['reference']}", f"- **Ultimo voto:** {m['ultimo_voto']}",
                  f"- **Nel motore:** `{json.dumps(m['motore'], ensure_ascii=False)}`", f"- **Origine:** {m['origine']}"]
            if m.get('variante_di'):
                L += [f"- **Variante di:** `{m['variante_di']}`"]
            if m.get('nota'):
                L += [f"- **Nota:** {m['nota']}"]
            L += ['']
    (CATALOGO.with_suffix('.md')).write_text('\n'.join(L) + '\n', encoding='utf-8')


if __name__ == '__main__':
    {'md': md, 'esempi': esempi}[sys.argv[1]]()

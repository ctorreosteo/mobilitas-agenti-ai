"""Procedura «studio reference» (agente reel-grafiche, fase 6, 05/11/2026).

Le reference stanno in `libreria/reference/` (orizzontali) e `libreria/reference/verticali/` (le aggiunge Riccardo,
anche in futuro, sia orizzontali sia verticali). Servono solo a studiare: niente di loro finisce nei nostri video.

Per ogni reference nuova (procedura, skill `mobilitas-reel`, «Studio reference»):
1. si guarda fotogramma per fotogramma (fogli a 4 fps, 12 fps sulle entrate) e si contano gli eventi visivi con la
   stessa definizione (taglio, camera, entrata, stato; le uscite a parte), ignorando sottotitoli di YouTube,
   barra del player, mouse, gesti della persona -> `libreria/reference/ritmo/<clip>.json`;
2. si scrive la scheda `libreria/reference/schede/<clip>.md` (grafiche, ritmo, tipografia, transizioni, cosa si può
   adattare, modelli nuovi possibili) e la riga di `libreria/reference/catalogo.md`;
3. `./mve reel-ritmo-reference` rifà la misura d'insieme (`libreria/reference/ritmo.json`): da lì viene l'obiettivo
   del ritmo dei piani;
4. si aggiorna il linguaggio grafico (skill `mobilitas-reel`, «Linguaggio») e si propongono i modelli nuovi: nascono
   «in prova» e diventano attivi solo con l'ok di Riccardo.

`./mve reel-reference` dice quali reference hanno già scheda e conteggio e quali no.

TAPPA 0, obbligatoria (Riccardo, 07/11/2026): prima di ogni reel (o del primo della coda) si lancia `./mve reel-reference`;
se ci sono reference non studiate, o file con il nome fuori regola, prima si fa lo studio completo (scheda, ritmo, catalogo,
linguaggio, modelli nuovi «in prova») e solo dopo si parte. `./mve reel-init` (e `reel-coda --avanza`) si
fermano con un messaggio chiaro finché resta qualcosa da studiare (`tappa0`).
- Una scheda senza il suo video va bene (per esempio su un altro Mac: i video delle reference non vanno nel repository):
  non conta come reference mancante.
- Nomi: `<fonte>-NN` per le orizzontali (minuscole, due cifre: `gadzhi-24.mov`), `verticale-NN` per le verticali
  (`verticale-12.mp4`), estensione in minuscolo. Un file fuori regola lo rinomina l'agente (e lo scrive nel report del
  reel); il motore propone il nome.
"""
import json
import re
import statistics

from . import reel_comune as C

REF = C.AGENTE / 'libreria' / 'reference'
EST = ('.mov', '.mp4', '.m4v', '.webm')


def clip():
    out = []
    for d in (REF, REF / 'verticali'):
        if d.exists():
            out += sorted(p for p in d.iterdir() if p.suffix.lower() in EST)
    return out


NOME_ORIZ = re.compile(r'^[a-z][a-z0-9]*-\d{2,}$')
NOME_VERT = re.compile(r'^verticale-\d{2,}$')
# file che stanno nelle cartelle delle reference e non sono reference
NON_REF = {'LEGGIMI.md', 'NOTE.md', 'catalogo.md', 'ritmo.json', '.DS_Store'}


def _nome_proposto(p, presi):
    """il prossimo nome libero secondo la regola (per le orizzontali la fonte è il nome di prima, ripulito)"""
    if p.parent.name == 'verticali':
        base = 'verticale'
    else:
        base = re.sub(r'[^a-z0-9]+', '', re.sub(r'[-_ ]*\d+$', '', p.stem.lower())) or 'fonte'
    k = 1 + max([int(m.group(1)) for x in presi for m in [re.match(rf'^{base}-(\d+)$', x)] if m] or [0])
    return f"{base}-{k:02d}{p.suffix.lower()}"


def esame():
    """lo stato delle reference: da studiare, nomi fuori regola, file non riconosciuti, schede senza video (vanno bene)"""
    cat = (REF / 'catalogo.md').read_text(encoding='utf-8') if (REF / 'catalogo.md').exists() else ''
    righe, mancano, nomi, strani = [], [], [], []
    presi = {p.stem for p in clip()} | {p.stem for p in (REF / 'schede').glob('*.md')} if (REF / 'schede').exists() else {p.stem for p in clip()}
    for p in clip():
        n = p.stem
        sc = (REF / 'schede' / f"{n}.md").exists()
        ev = (REF / 'ritmo' / f"{n}.json").exists()
        rg = f"`{n}`" in cat
        regola = NOME_VERT if p.parent.name == 'verticali' else NOME_ORIZ
        if not regola.match(n) or p.suffix != p.suffix.lower():
            nuovo = _nome_proposto(p, presi)
            presi.add(nuovo.rsplit('.', 1)[0])
            nomi.append((C.rel(p), nuovo))
        if not (sc and ev and rg):
            mancano.append(n)
        righe.append((n, p.parent.name, sc, ev, rg))
    for d in (REF, REF / 'verticali'):
        if d.exists():
            strani += [C.rel(p) for p in sorted(d.iterdir()) if p.is_file() and p.suffix.lower() not in EST and p.name not in NON_REF]
    con_video = {p.stem for p in clip()}
    senza_video = sorted(p.stem for p in (REF / 'schede').glob('*.md') if p.stem not in con_video) if (REF / 'schede').exists() else []
    return {'righe': righe, 'da_studiare': mancano, 'nomi_fuori_regola': nomi, 'file_non_riconosciuti': strani, 'schede_senza_video': senza_video}


def stato():
    E = esame()
    print("| clip | cartella | scheda | conteggio eventi | riga nel catalogo |")
    print("|---|---|---|---|---|")
    for n, cart, sc, ev, rg in E['righe']:
        print(f"| {n} | {cart} | {'sì' if sc else 'NO'} | {'sì' if ev else 'NO'} | {'sì' if rg else 'NO'} |")
    print()
    if E['schede_senza_video']:
        print(f"schede senza il loro video (vanno bene: i video delle reference non viaggiano con il repository): {len(E['schede_senza_video'])}")
    for vecchio, nuovo in E['nomi_fuori_regola']:
        print(f"NOME FUORI REGOLA: {vecchio} -> rinominalo (proposta: {nuovo}) e scrivilo nel report del reel")
    for x in E['file_non_riconosciuti']:
        print(f"file non riconosciuto nelle reference (non è un video .mov/.mp4/.m4v/.webm): {x}")
    print(f"da studiare: {', '.join(E['da_studiare'])}" if E['da_studiare'] else "tutte le reference hanno scheda, conteggio e riga nel catalogo")
    print("TAPPA 0: " + ("OK, si può partire con il reel" if not (E['da_studiare'] or E['nomi_fuori_regola'])
                         else "PRIMA lo studio delle reference (skill mobilitas-reel, «Studio reference»), poi il reel"))


def tappa0():
    """si ferma (SystemExit) se ci sono reference da studiare o con il nome fuori regola: chiamata da reel-init e
    reel-coda --avanza"""
    E = esame()
    if not (E['da_studiare'] or E['nomi_fuori_regola']):
        return E
    righe = ["", "STOP, TAPPA 0: ci sono reference nuove da studiare prima di cominciare un reel."]
    for vecchio, nuovo in E['nomi_fuori_regola']:
        righe.append(f"  - nome fuori regola: {vecchio} -> rinominalo in {nuovo} (e scrivilo nel report del reel)")
    if E['da_studiare']:
        righe.append(f"  - senza studio completo (scheda, conteggio del ritmo, riga del catalogo): {', '.join(E['da_studiare'])}")
    righe += ["Cosa fare: ./mve reel-reference per l'elenco; poi lo studio completo di ognuna (skill mobilitas-reel, «Studio reference»:",
              "scheda, ritmo, riga del catalogo, ./mve reel-ritmo-reference, linguaggio, modelli nuovi «in prova»); poi si rilancia reel-init.",
              "Una scheda senza il suo video va bene e non blocca."]
    raise SystemExit("\n".join(righe))


def misura(d, fusione=0.25):
    """dagli eventi di una clip, con la stessa regola dei piani (reel_piano.eventi): eventi principali (senza le uscite),
    quelli a meno di 0,25 s l'uno dall'altro contano una volta; pause fra un evento e il successivo (i bordi della clip
    sono tagli di chi l'ha registrata e non contano)"""
    ev = [e for e in d['eventi'] if e.get('tipo') != 'uscita']
    tt = sorted(float(e['t']) for e in ev)
    fusi = []
    for t in tt:
        if not fusi or t - fusi[-1] >= fusione:
            fusi.append(t)
    micro = sum(1 for e in ev if e.get('livello') == 'micro')
    pause = [b - a for a, b in zip(fusi, fusi[1:])]
    return {'eventi': len(ev), 'eventi_fusi': len(fusi), 'ogni_10s': round(len(fusi) / d['durata_s'] * 10, 2), 'micro': micro,
            'quota_micro': round(micro / max(1, len(ev)), 2),
            'pausa_media_s': round(sum(pause) / len(pause), 2) if pause else None, 'pausa_max_s': round(max(pause), 2) if pause else None}


def ritmo():
    righe = []
    for p in clip():
        f = REF / 'ritmo' / f"{p.stem}.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text())
        m = misura(d)
        righe.append(dict({'clip': p.stem, 'cartella': p.parent.name, 'durata_s': d['durata_s'],
                           'conteggio_agente': {'principali': d['principali'], 'ogni_10s': d['principali_ogni_10s'], 'pausa_max_s': d['pausa_max_s']}}, **m))
    if not righe:
        raise SystemExit("nessun conteggio in libreria/reference/ritmo/")
    v = sorted(r['ogni_10s'] for r in righe)
    pm = sorted(r['pausa_max_s'] for r in righe if r['pausa_max_s'] is not None)
    q = lambda a, k: statistics.quantiles(a, n=4)[k]
    tot_s = sum(r['durata_s'] for r in righe)
    out = {'_cosa': "ritmo delle reference (./mve reel-ritmo-reference): eventi visivi contati sui fotogrammi (un file per clip in "
                    "libreria/reference/ritmo/), misurati con la regola dei piani (reel_piano). L'obiettivo dei piani a densità «piena» "
                    "viene da qui (regola di Riccardo, 05/11/2026).",
           'clip': righe,
           'insieme': {'clip': len(righe), 'secondi': round(tot_s, 1), 'ogni_10s_complessivo': round(sum(r['eventi_fusi'] for r in righe) / tot_s * 10, 2),
                       'ogni_10s_mediana': round(statistics.median(v), 2), 'ogni_10s_quartili': [round(q(v, 0), 2), round(q(v, 2), 2)],
                       'ogni_10s_min_max': [v[0], v[-1]], 'pausa_max_mediana_s': round(statistics.median(pm), 2),
                       'pausa_max_quartili_s': [round(q(pm, 0), 2), round(q(pm, 2), 2)],
                       'quota_micro': round(sum(r['micro'] for r in righe) / max(1, sum(r['eventi'] for r in righe)), 2)}}
    print(json.dumps(out['insieme'], ensure_ascii=False, indent=1))
    for r in righe:
        print(f"  {r['clip']:11s} {r['ogni_10s']:5.1f} ogni 10 s, micro {r['quota_micro']:.0%}, pausa max {r['pausa_max_s']}")
    vecchio = json.loads((REF / 'ritmo.json').read_text()) if (REF / 'ritmo.json').exists() else {}
    if vecchio.get('obiettivo'):
        out['obiettivo'] = vecchio['obiettivo']
        print(f"obiettivo (scritto dall'agente, invariato): {out['obiettivo']}")
    else:
        print("obiettivo non ancora scritto: lo fissa l'agente in ritmo.json («obiettivo»: ogni_10s, pausa_max_s, fonte), dai numeri sopra")
    C.scrivi(REF / 'ritmo.json', out)

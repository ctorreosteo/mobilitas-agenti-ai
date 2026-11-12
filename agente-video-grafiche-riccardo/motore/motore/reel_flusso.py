"""Il flusso dell'agente reel-grafiche (fase 4, 04/11/2026): nuovo reel, stato, coda, approvazioni, voti, consegna.

    ./mve reel-reference                    tappa 0 (obbligatoria, 07/11/2026): reference nuove studiate prima di ogni reel;
                                            reel-init e reel-coda --avanza si fermano se ne resta una da studiare
    ./mve reel-init inbox/<SLUG>/ [slug]    nuovo ad (videos/<slug>/reel.json): video, SRT e mp3 restano in inbox/
    ./mve reel-radiografia <slug>           tappa 1 (motore), poi l'agente segna le 3D: ./mve reel-3d <slug> 3,9|nessuna
    ./mve reel-piano <slug>                 tappa 2: controlla piano.json (scritto dall'agente) e fa la tavola
                                            (fase 6, giro 4, Riccardo 05/11/2026: niente fermata sul piano)
    ./mve reel-approva <slug> piano         facoltativo: un ok di Riccardo sul piano, se lo chiede (legato all'md5)
    ./mve reel-rendi <slug>                 tappa 3: render, anteprime, controlli; poi il voto del direttore     -> FERMO
                                            sull'ANTEPRIMA: Riccardo la guarda e dice cosa migliorare; si rifà
                                            un'anteprima nuova finché la approva
    ./mve reel-voto <slug> <grafica> <voto> [--giro 1] [--nota ...]
    ./mve reel-guardato <slug> "f1959:3" "€ sfocato letto come 3"  una lettura di Vision guardata sull'immagine
    ./mve reel-approva <slug> anteprime     l'ok di Riccardo sulle anteprime (legato all'md5 del video di lavoro)
    ./mve reel-consegna <slug>              tappa 4: copia in consegna/ + consegna.md
    ./mve reel-stato [slug]                 dove sta un ad e cosa viene dopo; senza slug, tutta la coda di inbox/
    ./mve reel-coda [--avanza]              la coda di inbox/; con --avanza il motore fa le tappe automatiche, un ad
                                            dopo l'altro, fino al primo punto che tocca all'agente o a Riccardo
    ./mve reel-pulisci <slug>               svuota .lavoro/<slug>/ (solo quella)
"""
import datetime
import shutil
import sys

from . import reel_comune as C

VOTO_MIN = 7
GIRI_MAX = 2


def init(sorgente, slug=None):
    from pathlib import Path
    # tappa 0 (Riccardo, 07/11/2026): prima di ogni reel le reference nuove si studiano; altrimenti ci si ferma qui
    from .reel_reference import tappa0
    tappa0()
    p = Path(sorgente)
    p = p if p.is_absolute() else C.AGENTE / p
    d = p if p.is_dir() else p.parent
    slug = slug or d.name
    trovati = [x for x in C.trova_inbox() if x['cartella'] == d]
    if not trovati:
        sys.exit(f"{C.rel(d)}: nessun video 1080x1920 o 1920x1080 (.mp4/.mov) qui dentro")
    x = trovati[0]
    if p.is_file():
        x['video'] = p
    D = C.cartella(slug)
    if (D / 'reel.json').exists():
        print(f"{slug}: c'è già ({C.rel(D / 'reel.json')})")
        return slug
    if D.exists() and any(D.iterdir()):
        sys.exit(f"{C.rel(D)} esiste già senza reel.json (lavoro fatto a mano?): scegli un altro slug")
    if not x['srt']:
        # fase 6 (05/11/2026): un reel può arrivare senza SRT; la radiografia legge i sottotitoli impressi o usa la voce
        print(f"  {C.rel(d)}: manca l'SRT: il copy si legge dai sottotitoli impressi (Vision) o dalla voce, e va confermato")
    D.mkdir(parents=True, exist_ok=True)
    C.scrivi(D / 'reel.json', {'_cosa': "video con infografiche dell'Agente Video Grafiche (Riccardo). Il girato resta in inbox/ e non si tocca.",
                              'slug': slug, 'formato': x['formato'], 'creato': f"{datetime.datetime.now():%d/%m/%Y %H:%M}",
                              'sorgente': {'video': C.rel(x['video']), 'srt': C.rel(x['srt']) if x['srt'] else None, 'mp3': C.rel(x['mp3']) if x['mp3'] else None}})
    print(f"{slug}: creato {C.rel(D / 'reel.json')} (formato {x['formato']}, video {C.rel(x['video'])}, SRT {C.rel(x['srt']) if x['srt'] else 'nessuno'})")
    return slug


# ---------------------------------------------------------------- stato

def nome_consegna(slug):
    """il nome dei file consegnati: `nome_consegna` in videos/<slug>/reel.json (per esempio senza «-prova_…» nello slug di
    lavoro; Riccardo, 08/11/2026), altrimenti lo slug"""
    a = C.cartella(slug) / 'reel.json'
    return (C.leggi(a).get('nome_consegna') if a.exists() else None) or slug


def _stato(slug):
    """(tappa, chi, cosa) - chi: motore | agente | riccardo | fatto"""
    D = C.cartella(slug)
    if not (D / 'reel.json').exists():
        if (D / 'consegna').exists() and any((D / 'consegna').glob('*.mp4')):
            return ('consegnato', 'fatto', 'consegnato a mano (fasi 0-3, prima dell\'agente)')
        return ('nuovo', 'motore', f"./mve reel-init inbox/{slug}/ e ./mve reel-radiografia {slug}")
    if not (D / 'radiografia.json').exists():
        return ('radiografia', 'motore', f"./mve reel-radiografia {slug}")
    R = C.leggi(D / 'radiografia.json')
    if (R.get('animazioni_3d') or {}).get('stato') != 'segnate':
        return ('3D', 'agente', f"guardare radiografia/inquadrature-*.jpg e segnare: ./mve reel-3d {slug} <n,n|nessuna>")
    if not (D / 'piano.json').exists():
        return ('piano', 'agente', "scrivere piano.json (skill mobilitas-reel)")
    ctl = C.leggi(D / 'piano' / 'controllo.json', {}) if (D / 'piano' / 'controllo.json').exists() else {}
    md5p = C.md5_file(D / 'piano.json')
    if ctl.get('md5_piano') != md5p:
        return ('piano', 'motore', f"./mve reel-piano {slug}")
    if ctl.get('errori'):
        return ('piano', 'agente', f"correggere il piano: {len(ctl['errori'])} errori in piano/piano.md")
    ap = C.leggi(D / 'approvazioni.json', {}) if (D / 'approvazioni.json').exists() else {}
    if C.leggi(D / 'piano.json').get('laboratorio'):
        k = C.leggi(D / 'controlli' / 'controlli.json', {}) if (D / 'controlli' / 'controlli.json').exists() else {}
        if k.get('md5_piano') != md5p:
            return ('laboratorio', 'motore', f"./mve reel-rendi {slug} --laboratorio")
        return ('laboratorio', 'riccardo', "piano di laboratorio: anteprime, controlli e voti da guardare (non si consegna)")
    # fase 6, giro 4 (Riccardo, 05/11/2026): niente fermata sul piano, nemmeno per i tipi di reel nuovi: radiografia -> piano
    # -> render -> controlli -> direttore -> ANTEPRIMA. Riccardo guarda l'anteprima e descrive cosa migliorare; si rifà
    # un'altra anteprima; quando la approva si fa la consegna
    k = C.leggi(D / 'controlli' / 'controlli.json', {}) if (D / 'controlli' / 'controlli.json').exists() else {}
    full = D / 'anteprime' / f"{slug}_lavoro-intero.mp4"
    if k.get('md5_piano') != md5p or not full.exists() or k.get('md5_video') != C.md5_file(full):
        return ('rendi', 'motore', f"./mve reel-rendi {slug}")
    if k.get('errori'):
        return ('rendi', 'agente', f"correggere: {len(k['errori'])} errori in controlli/controlli.md")
    ver = C.leggi(D / 'verifiche.json', {}) if (D / 'verifiche.json').exists() else {}
    dg = [q for q in k['vision']['da_guardare'] if q['chiave'] not in ver.get('cifre', {})]
    if dg:
        return ('rendi', 'agente', f"guardare {len(dg)} letture di Vision (controlli/cifre-da-guardare/) e segnarle con ./mve reel-guardato")
    voti = C.leggi(D / 'voti.json', {}) if (D / 'voti.json').exists() else {}
    # produzione (04/11/2026): un voto sotto 7 dopo due giri lo decide Riccardo; il suo ok alle anteprime (sullo stesso
    # video) vale come decisione
    deciso = (ap.get('anteprime') or {}).get('md5') == k['md5_video']
    if C.leggi(D / 'piano.json').get('densita') == 'piena':
        k['grafiche']['_insieme'] = {'hash_pagina': k['md5_video']}      # fase 6: il voto del reel intero
    for n in k['grafiche']:
        v = [x for x in voti.get(n, []) if x.get('hash_pagina') == k['grafiche'][n]['hash_pagina']]   # vale per la grafica votata
        if not v:
            giri = len(voti.get(n, []))
            if giri >= GIRI_MAX and voti[n][-1]['voto'] < VOTO_MIN:
                if deciso:
                    continue
                return ('voto', 'riccardo', f"{n}: sotto {VOTO_MIN} dopo {GIRI_MAX} giri: decide Riccardo")
            if giri >= GIRI_MAX:
                # 09/11/2026: dopo due giri non c'è un giro 3; i ritocchi di esecuzione restano «non rivotati» e li
                # giudica Riccardo sull'anteprima (il suo ok sullo stesso video vale come decisione)
                if deciso:
                    continue
                return ('voto', 'riccardo', f"{n}: ritoccata dopo {GIRI_MAX} giri, non rivotata: decide Riccardo")
            return ('voto', 'agente', f"voto del direttore per «{n}» (giro {giri + 1}): .lavoro/{slug}/direttore/{n}/PROMPT.md")
        if v[-1]['voto'] < VOTO_MIN:
            if len(voti[n]) >= GIRI_MAX:
                if deciso:
                    continue
                return ('voto', 'riccardo', f"{n}: voto {v[-1]['voto']} dopo {GIRI_MAX} giri: decide Riccardo")
            return ('voto', 'agente', f"{n}: voto {v[-1]['voto']}: correggere il piano (giro {len(voti[n]) + 1})")
    if (ap.get('anteprime') or {}).get('md5') != k['md5_video']:
        return ('anteprime', 'riccardo', f"approvare le anteprime: anteprime/{slug}_lavoro-intero.mp4 (e -ZONE-META), "
                                         f"controlli/controlli.md (poi ./mve reel-approva {slug} anteprime)")
    c = D / 'consegna' / f"{nome_consegna(slug)}_infografiche.mp4"
    if not c.exists() or C.md5_file(c) != k['md5_video']:
        return ('consegna', 'motore', f"./mve reel-consegna {slug}")
    return ('consegnato', 'fatto', f"consegna/{c.name}")


def stato(slug=None):
    if slug:
        t, chi, cosa = _stato(slug)
        print(f"{slug}: tappa {t}; tocca a {chi}: {cosa}")
        return
    coda()


def coda(avanza=False):
    reel_ = C.trova_inbox()
    if not reel_:
        print("inbox/: nessun reel 1080x1920 o 1920x1080")
        return
    if avanza:
        from .reel_reference import tappa0
        tappa0()                            # tappa 0 prima del primo della coda
    for x in reel_:
        slug = x['slug']
        if avanza and x['formato'] != C.FORMATO:
            # 11/11/2026: W, H e la zona sicura valgono per tutto un processo: un reel di un altro formato fa le sue tappe
            # in un ./mve a parte (ogni tappa legge il formato da reel.json)
            import subprocess
            for _ in range(6):
                t, chi, cosa = _stato(slug)
                if chi != 'motore' or t == 'consegna':
                    break
                print(f"== {slug} ({x['formato']}): {t}", flush=True)
                fasi = {'nuovo': [['reel-init', str(x['cartella']), slug], ['reel-radiografia', slug]],
                        'radiografia': [['reel-radiografia', slug]], 'piano': [['reel-piano', slug]], 'rendi': [['reel-rendi', slug]]}
                for argv in fasi.get(t, []):
                    subprocess.run([str(C.AGENTE / 'mve')] + argv)
                if _stato(slug)[0] == t:
                    break
            continue
        if avanza:
            for _ in range(6):
                t, chi, cosa = _stato(slug)
                if chi != 'motore':
                    break
                print(f"== {slug}: {t}", flush=True)
                if t == 'nuovo':
                    init(x['cartella'], slug)
                    from .reel_radiografia_base import radiografia
                    radiografia(slug)
                elif t == 'radiografia':
                    from .reel_radiografia_base import radiografia
                    radiografia(slug)
                elif t == 'piano':
                    from .reel_piano_base import piano
                    try:
                        piano(slug)
                    except SystemExit:
                        pass
                elif t == 'rendi':
                    from .reel_rendi import rendi
                    try:
                        rendi(slug)
                    except SystemExit:
                        pass
                elif t == 'consegna':
                    break                   # la consegna si lancia a mano, dopo l'ok di Riccardo
    print('\n| ad | tappa | tocca a | cosa |\n|---|---|---|---|')
    for x in reel_:
        t, chi, cosa = _stato(x['slug'])
        print(f"| {x['slug']} | {t} | {chi} | {cosa} |")
    prove = sorted(d.name for d in C.AGENTE.joinpath('videos').iterdir() if (d / 'reel.json').exists()
                   and d.name not in {x['slug'] for x in reel_})
    for s in prove:
        t, chi, cosa = _stato(s)
        print(f"| {s} (da {C.leggi(C.cartella(s) / 'reel.json')['sorgente']['video'].split('/')[1]}) | {t} | {chi} | {cosa} |")


# ---------------------------------------------------------------- approvazioni, voti, verifiche

def piano_approvato(slug):
    """(vale, perche): l'ok di Riccardo vale per l'md5 del piano che ha visto, o per un piano con la stessa firma
    (stessi tempi, testi e modo: cambiati solo gli elementi dei modelli costruiti dopo l'ok). Se la firma cambia, ci si
    ferma e si chiede."""
    D = C.cartella(slug)
    ap = (C.leggi(D / 'approvazioni.json', {}) if (D / 'approvazioni.json').exists() else {}).get('piano') or {}
    md5p = C.md5_file(D / 'piano.json')
    if not ap:
        return False, None
    if ap.get('md5') == md5p:
        return True, 'piano approvato'
    ctl = C.leggi(D / 'piano' / 'controllo.json', {}) if (D / 'piano' / 'controllo.json').exists() else {}
    if not ap.get('firma') or ctl.get('md5_piano') != md5p or ctl.get('errori'):
        return False, None
    from .reel_piano_base import firma
    ora = firma(C.leggi(D / 'piano.json'), C.leggi(D / 'radiografia.json')['fps'])
    if ora == ap['firma']:
        return True, "piano approvato (ok tenuto: tempi, testi e modo uguali al piano visto da Riccardo)"
    diversi = [a['nome'] for a, b in zip(ora, ap['firma']) if a != b] or ['numero di grafiche']
    return False, (f"il piano è cambiato in tempi, testi o modo ({', '.join(diversi)}) rispetto a quello approvato: "
                   "FERMARSI e chiedere a Riccardo (regola del 04/11/2026)")


def approva(slug, cosa, da=None):
    D = C.cartella(slug)
    if cosa == 'piano':
        f = D / 'piano.json'
        ctl = C.leggi(D / 'piano' / 'controllo.json')
        if ctl['md5_piano'] != C.md5_file(f) or ctl['errori']:
            sys.exit(f"{slug}: il piano va prima controllato senza errori (./mve reel-piano {slug})")
    elif cosa == 'anteprime':
        f = D / 'anteprime' / f"{slug}_lavoro-intero.mp4"
        t, chi, _ = _stato(slug)
        if t != 'anteprime' and not (t == 'voto' and chi == 'riccardo'):
            sys.exit(f"{slug}: le anteprime non sono pronte da approvare (tappa {t}, tocca a {chi}: ./mve reel-stato {slug})")
    else:
        sys.exit("si approvano solo «piano» e «anteprime»")
    ap = C.leggi(D / 'approvazioni.json', {}) if (D / 'approvazioni.json').exists() else {}
    prima = ap.get(cosa) or {}
    ap[cosa] = {'md5': C.md5_file(f), 'file': C.rel(f), 'da': da or prima.get('da') or 'Riccardo (in chat)',
                'data': prima['data'] if prima.get('md5') == C.md5_file(f) and prima.get('data') else f"{datetime.datetime.now():%d/%m/%Y %H:%M}"}
    # fase 6: con gli effetti sonori l'ok vale per le due versioni (con e senza effetti)
    fs = D / 'anteprime' / f"{slug}_lavoro-intero-senza-effetti.mp4"
    if cosa == 'anteprime' and fs.exists():
        ap[cosa]['md5_senza_effetti'] = C.md5_file(fs)
    if cosa == 'piano':
        # regola del 04/11/2026: l'ok vale anche per il piano con i modelli costruiti, se tempi, testi e modo restano
        from .reel_piano_base import firma
        ap[cosa]['firma'] = firma(C.leggi(f), C.leggi(D / 'radiografia.json')['fps'])
        shutil.copy2(f, D / 'piano' / 'approvato.json')
    C.scrivi(D / 'approvazioni.json', ap)
    print(f"{slug}: {cosa} approvato ({ap[cosa]['da']}, md5 {ap[cosa]['md5']})")
    if cosa == 'piano' and not C.leggi(f).get('laboratorio'):
        # produzione (04/11/2026): la varietà si misura su tutti gli ads precedenti, anche quelli non ancora consegnati
        _storico(slug, 'piano approvato')


def voto(slug, grafica, voto, giro=None, nota=None, vale_per=None):
    D = C.cartella(slug)
    k = C.leggi(D / 'controlli' / 'controlli.json')
    # fase 6: «_insieme» è il voto del reel intero (densità piena), legato all'md5 del video di lavoro
    if grafica == '_insieme':
        k['grafiche']['_insieme'] = {'hash_pagina': k['md5_video']}
    if grafica not in k['grafiche']:
        sys.exit(f"grafica «{grafica}» non c'è: {list(k['grafiche'])}")
    voti = C.leggi(D / 'voti.json', {}) if (D / 'voti.json').exists() else {}
    lista = voti.setdefault(grafica, [])
    g = int(giro) if giro else len(lista) + 1
    e = {'giro': g, 'voto': float(voto), 'nota': nota or '', 'md5_video': k['md5_video'],
         'hash_pagina': k['grafiche'][grafica]['hash_pagina'], 'data': f"{datetime.datetime.now():%d/%m/%Y %H:%M}"}
    if vale_per:
        e['vale_per'] = vale_per
    lista.append(e)
    C.scrivi(D / 'voti.json', voti)
    print(f"{slug}: {grafica} voto {voto} (giro {g})" + ('' if float(voto) >= VOTO_MIN else f": sotto {VOTO_MIN}"))


def guardato(slug, chiave, motivo):
    D = C.cartella(slug)
    v = C.leggi(D / 'verifiche.json', {}) if (D / 'verifiche.json').exists() else {}
    v.setdefault('cifre', {})[chiave] = f"{motivo} (guardato il {datetime.datetime.now():%d/%m/%Y %H:%M})"
    C.scrivi(D / 'verifiche.json', v)
    print(f"{slug}: {chiave} -> {motivo}")


# ---------------------------------------------------------------- consegna

def consegna(slug, prova=False):
    D = C.cartella(slug)
    k = C.leggi(D / 'controlli' / 'controlli.json')
    full = D / 'anteprime' / f"{slug}_lavoro-intero.mp4"
    ap = C.leggi(D / 'approvazioni.json', {}) if (D / 'approvazioni.json').exists() else {}
    if not prova and C.leggi(D / 'piano.json').get('laboratorio'):
        sys.exit(f"{slug}: è un piano di laboratorio: non si consegna")
    if not prova:
        t, chi, cosa = _stato(slug)
        if t not in ('consegna', 'consegnato'):
            sys.exit(f"{slug}: non si consegna (tappa {t}, tocca a {chi}: {cosa})")
        out = D / 'consegna'
    else:
        out = C.lavoro(slug, 'consegna-prova')
        print(f"  prova del comando: niente approvazione richiesta, si scrive in {C.rel(out)}")
    out.mkdir(parents=True, exist_ok=True)
    dest = out / f"{nome_consegna(slug)}_infografiche.mp4"
    shutil.copy2(full, dest)
    m1, m2 = C.md5_file(full), C.md5_file(dest)
    if m1 != m2 or m1 != k['md5_video']:
        sys.exit(f"copia non identica: {m1} / {m2} / controlli {k['md5_video']}")
    pr = C.probe(dest)
    voti = C.leggi(D / 'voti.json', {}) if (D / 'voti.json').exists() else {}
    R = C.leggi(D / 'radiografia.json')
    fps = R['fps']
    L = [f"# Consegna: {slug} con infografiche", '',
         f"**Approvato da {(ap.get('anteprime') or {}).get('da', '—')} il {(ap.get('anteprime') or {}).get('data', '—')}** "
         f"(anteprime); piano {('approvato il ' + ap['piano']['data']) if ap.get('piano') else 'controllato dal motore (dal 05/11/2026 il piano non si approva a parte: si approva l anteprima)'}." + (' **PROVA DEL COMANDO: non è una consegna.**' if prova else ''), '',
         '## Il file', '', '| | |', '|---|---|', f"| file | `{dest.name}` |", f"| copiato da | `{C.rel(full)}` (il file approvato, copiato e non rifatto) |",
         f"| md5 del file | `{m2}`, uguale al file approvato (`{m1}`) e a quello dei controlli |", f"| peso | {pr['byte']:,} byte |".replace(',', '.'),
         f"| video | {pr['video']['codec_name']} {pr['video']['profile']}, {pr['larghezza']}×{pr['altezza']}, {pr['fps']:g} fps, {pr['fotogrammi']} fotogrammi, "
         f"{pr['video']['pix_fmt']}, {pr['video']['color_space']}, range {pr['video']['color_range']} |",
         (f"| audio | originale con {len(k['effetti_sonori']['effetti'])} effetti sonori (AAC); la versione senza effetti ha l'audio copiato |"
          if k.get('effetti_sonori') else f"| audio | copiato dall'originale: md5 del flusso `{k['audio']['md5_finale']}` = originale `{k['audio']['md5_originale']}` |"),
         f"| durata | {pr['durata']:.3f} s |".replace('.', ',', 1), '', '## Le grafiche', '',
         '| # | grafica | modello del catalogo | modo | fotogrammi | tempi | voto del direttore |', '|---|---|---|---|---|---|---|']
    for i, (n, g) in enumerate(sorted(k['grafiche'].items(), key=lambda x: x[1]['visibile'][0][0]), 1):
        v = voti.get(n, [])
        L.append(f"| {i} | {n} | `{g['catalogo']}` | {g['modo']} | " + ', '.join(f"{a}–{b}" for a, b in g['visibile']) + ' | '
                 + ', '.join(f"{a:.3f}–{b:.3f} s" for a, b in g['tempi']).replace('.', ',') + ' | '
                 + (' → '.join(f"{x['voto']:g}" for x in v) or '—') + ' |')
    L += ['', '## Controlli superati', '', f"Da `controlli/controlli.md` ({k['data']}).", '',
          f"- audio identico all'originale (md5 del flusso);",
          f"- video uguale fuori dalle grafiche: " + '; '.join(f"{n} SSIM {s['medio']:.5f}" for n, s in k['ssim'].items() if s) + ';',
          '- nessuna sovrapposizione fra grafiche; niente «tutto schermo» sulle animazioni 3D; niente «finestra» fuori dalla finestra;',
          '- testi interi e nella zona sicura Meta in ogni fotogramma (variante «solo testo»): ' + '; '.join(
              f"{n} {g['testo_ingombro']}" for n, g in k['grafiche'].items()) + ';',
          f"- nessuna cifra non detta: dalla pagina, su ogni fotogramma; Apple Vision su {k['vision']['fotogrammi_letti']} fotogrammi "
          f"({k['vision']['spiegate']} letture spiegate dalla pagina; {len(k['vision']['guardate'])} gruppi di letture sbagliate guardati sull'immagine: "
          + '; '.join(f"{q['chiave']} {q['guardato']}" for q in k['vision']['guardate']) + ');',
          '- solo parole dette: ogni parola scritta è nell\'SRT;']
    if k.get('passaggi'):
        L.append('- passaggi fra grafiche vicine: ' + '; '.join(f"{p['da']} → {p['a']} {p['ultimo']} → {p['primo']}" for p in k['passaggi']) + '.')
    (out / 'consegna.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    if not prova:
        _storico(slug, 'consegnato')
        # Riccardo (04/11/2026): una copia di ogni video finito anche in consegne/, in cima al laboratorio, stesso nome e md5
        comune = C.AGENTE / 'consegne'
        comune.mkdir(exist_ok=True)
        c2 = comune / dest.name
        shutil.copy2(dest, c2)
        if C.md5_file(c2) != m2:
            sys.exit(f"copia in consegne/ non identica: {C.md5_file(c2)} / {m2}")
        print(f"  copia anche in {C.rel(c2)} (md5 uguale)")
    if k.get('video_senza_effetti'):
        # fase 6: la versione senza effetti sonori (audio copiato dall'originale) accanto a quella con gli effetti
        fs = C.AGENTE / k['video_senza_effetti']
        d2 = out / f"{nome_consegna(slug)}_infografiche_senza-effetti.mp4"
        shutil.copy2(fs, d2)
        if C.md5_file(d2) != k['md5_video_senza_effetti'] or (not prova and (ap.get('anteprime') or {}).get('md5_senza_effetti') != k['md5_video_senza_effetti']):
            sys.exit(f"versione senza effetti: copia non identica o non approvata ({C.md5_file(d2)} / {k['md5_video_senza_effetti']})")
        if not prova:
            shutil.copy2(d2, C.AGENTE / 'consegne' / d2.name)
            if C.md5_file(C.AGENTE / 'consegne' / d2.name) != k['md5_video_senza_effetti']:
                sys.exit("copia in consegne/ della versione senza effetti non identica")
        with open(out / 'consegna.md', 'a', encoding='utf-8') as fh:
            fh.write(f"\n## Versione senza effetti sonori\n\n`{d2.name}`, md5 `{k['md5_video_senza_effetti']}` (stesso video, audio copiato "
                     f"dall'originale: md5 del flusso `{k['audio']['md5_finale']}`). Il file principale ha gli effetti sonori: "
                     f"{len(k['effetti_sonori']['effetti'])} effetti; tolti gli effetti, residuo {k['effetti_sonori']['residuo_senza_effetti_db']} dB "
                     f"contro {k['effetti_sonori']['rumore_della_sola_ricodifica_db']} dB della sola ricodifica.\n")
        print(f"  versione senza effetti: {C.rel(d2)} (md5 uguale al file approvato)")
    print(f"{slug}: {C.rel(dest)} (md5 {m2}, uguale al file approvato) + consegna.md")


def _storico(slug, stato='consegnato'):
    """collaudo (04/11/2026): l'ad consegnato entra nello storico dei modelli (libreria/uso-modelli-reel.json)"""
    from .reel_piano_base import STORICO
    if slug.startswith('_'):
        return          # fase 6: gli slug di regressione e di prova (_...) non entrano nello storico della varietà
    P = C.leggi(C.cartella(slug) / 'piano.json')
    S = C.leggi(STORICO, {}) if STORICO.exists() else {}      # con il commento «_cosa»
    S[slug] = {'data': f"{datetime.datetime.now():%d/%m/%Y}", 'stato': stato,
               'grafiche': [{k: g.get(k, '') for k in ('momento', 'nome', 'catalogo', 'modo', 'impaginazione', 'voce')}
                            for g in sorted(P['grafiche'], key=lambda g: g['f0'])],
               'senza_grafica': P.get('senza_grafica', [])}
    C.scrivi(STORICO, S)
    print(f"  storico dei modelli aggiornato: {C.rel(STORICO)}")


def pulisci(slug):
    d = C.AGENTE / '.lavoro' / slug
    if d.exists():
        shutil.rmtree(d)
    hist = C.AGENTE / 'motore' / 'inserti' / '.casa' / '.cache' / 'hyperframes' / 'history'
    n = len([p for p in hist.iterdir() if not p.name.startswith('.')]) if hist.exists() else 0   # .last-prune non è una voce
    print(f"{slug}: .lavoro/{slug}/ svuotata; cronologia HyperFrames: {n} voci")

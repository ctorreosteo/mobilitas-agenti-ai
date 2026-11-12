"""Il sistema delle grafiche del reel: stile fisso, più forme (Riccardo, 07/11/2026).

Prima regola del 07/11/2026 (mattina): UN palco per reel. Correzione della sera, dopo l'anteprima del frontman (stile APPROVATO:
colori, card, disegni Servier, indicatore, barre, lista barrata, movimenti e trasformazioni restano così): il pannello fisso è
UNA delle forme, non l'unica. Le reference ne usano diverse (fascia alta, pannello sotto il volto, schermo diviso, tendina che
diventa tutto schermo, badge in un angolo, card di vetro, dati sopra il video); un reel ne usa di solito 2 o 3, sceglie la forma
per ogni momento secondo l'inquadratura e quello che si dice, e i passaggi sono legati (tendina, spinta, zoom).

I SOTTOTITOLI impressi non si toccano mai (niente ritagli, copie, spostamenti, ingrandimenti, sfocature, veli, ridisegni): o la
fascia resta identica all'originale (VIDEO FERMO, le grafiche le stanno intorno) o è coperta del tutto (GRAFICA PIENA, brevi).
Il video non si abbassa più e le lettere non si ricompongono: tolti `stato`, `componi`, `applica`, `lettere`, `verifica`
(07/11/2026). Il controllo che blocca il render è in `reel_sottotitoli.py`.

Le grafiche sono `infografica_reel` con `dati.modo = "palco"`; `dati.stati` = [{da, forma, x, y, w, h, r, entra}], uno per
ogni forma che la grafica attraversa (entra: «taglio», «seme» = cresce dal suo bordo verso il contenuto, «tendina» = si allarga
dalla forma di prima saltando la fascia dei sottotitoli). Nel piano (`piano.json`, chiave `palco`):

    {"nome": ..., "tipo": ..., "forme": [{"nome": "fascia alta", "video": "fermo", "reference": [...], "quando": ...},
                                           {"nome": "pannello basso", "video": "fermo", ...},
                                           {"nome": "tutto schermo", "video": "pieno", ...}, {"nome": "badge", "video": "fermo"}],
     "famiglie": [...], "struttura": {...}, "reference": [...], "perche": "..."}
"""
import math
import subprocess

from . import reel_comune as C
from .reel_comune import W, H, SAFE

REF = C.AGENTE / 'libreria' / 'reference'


def video_reference(clip):
    """il video di una reference, se c'è su questo Mac (le verticali in verticali/, le orizzontali in reference/), o None"""
    for p in (REF / 'verticali' / f"{clip}.mp4", REF / f"{clip}.mp4", REF / f"{clip}.mov"):
        if p.exists():
            return p
    return None


def reference_valida(clip):
    """una reference vale se ha la scheda (i video non viaggiano con il repository: 11/11/2026) o il video. Il reel verticale
    cita le verticali; quello orizzontale anche le orizzontali (gadzhi-NN, martell-NN)"""
    if not clip or (not C.ORIZZONTALE and not clip.startswith('verticale-')):
        return False
    return (REF / 'schede' / f"{clip}.md").exists() or video_reference(clip) is not None


def forme_orizzontali():
    """le forme del 16:9, per i prompt del direttore (Riccardo, 11/11/2026)"""
    return ("IN QUESTO REEL ORIZZONTALE 16:9 (visto a tutto schermo): le forme a video fermo sono la COLONNA LATERALE accanto alle "
            "finestre del montaggio (le finestre lasciano libere due colonne ai lati), il PANNELLO AL POSTO DI UNA FINESTRA, il BADGE "
            "in un angolo alto e la FASCIA ALTA; le grafiche piene (tendina, schermo diviso, vetro) restano brevi. Il foglio «a misura "
            "di telefono» è il telefono girato in orizzontale (390 px di altezza).")


def tratti(P):
    """[(f0, f1, nome)] delle grafiche del palco, in ordine"""
    return sorted((g['f0'], g['f0'] + g['frames'] - 1, g['nome']) for g in P.get('grafiche', []) if g.get('modo') == 'palco')


def stati_di(g):
    """gli stati (forme) di una grafica del palco, con il tempo di fine"""
    for x in g.get('elementi') or []:
        d = x.get('dati') or {}
        if d.get('modo') == 'palco':
            st = sorted(d.get('stati') or [], key=lambda q: q.get('da', 0))
            dur = g['frames'] / 30.0
            return [dict(q, a=(st[i + 1]['da'] if i + 1 < len(st) else dur)) for i, q in enumerate(st)], d
    return [], {}


MAX_TUTTO_SCHERMO = 3
MAX_TUTTO_SCHERMO_S = 4.0
MAX_FAMIGLIE = 5
OMBRA_ALTO_PX = 64        # quanto scende sotto la forma l'ombra «alto» (0 22px 40px, più il margine della fascia)


def _tocca(a, b, m=0):
    return a[0] < b[2] + m and a[2] > b[0] - m and a[1] < b[3] + m and a[3] > b[1] - m


def _dentro(a, b):
    return a[0] >= b[0] and a[1] >= b[1] and a[2] <= b[2] and a[3] <= b[3]


def controlla(P, R):
    """errori e avvisi del sistema delle forme (Riccardo, 07/11/2026)"""
    err, avv = [], []
    pal = P.get('palco')
    G = P.get('grafiche') or []
    if not pal:
        if any(g.get('modo') == 'palco' for g in G):
            err.append("grafiche con modo «palco» ma il piano non ha la chiave «palco»")
        return err, avv
    for k in ('nome', 'tipo', 'forme', 'perche', 'famiglie', 'reference'):
        if not pal.get(k):
            err.append(f"palco: manca «{k}»")
    if err:
        return err, avv
    fps = R['fps']
    forme = {f['nome']: f for f in pal['forme']}
    # 1. un sistema: niente elementi sparsi fuori dalle forme
    for g in G:
        if g.get('modo') in ('micro', 'persona'):
            err.append(f"{g['nome']}: modo «{g['modo']}» con il palco: niente elementi sparsi; va in una delle forme")
    # 2. famiglie poche e dichiarate; ogni scena dice la sua famiglia, da dove nasce e a quale reference somiglia
    fam = pal['famiglie']
    if len(fam) > MAX_FAMIGLIE:
        err.append(f"palco: {len(fam)} famiglie di oggetti (al massimo {MAX_FAMIGLIE}: poche, sempre le stesse)")
    nomi_fam = {x['nome'] if isinstance(x, dict) else x for x in fam}
    righe_s = [(rg['fotogrammi_misurati'], rg['box_lettere']) for rg in (R['sottotitoli'].get('righe') or [])
               if rg.get('fotogrammi_misurati') and rg.get('box_lettere')]
    pers_p = C.cartella(P['slug']) / 'radiografia' / 'persona.json' if P.get('slug') else None
    pers = C.leggi(pers_p) if pers_p and pers_p.exists() else None
    tre = {f for a, b in (R.get('animazioni_3d') or {}).get('fotogrammi', []) for f in range(a, b + 1)}
    inq_di = {f: s_ for s_ in R['inquadrature'] for f in range(s_['f0'], s_['f1'] + 1)}
    usate, piene = set(), []
    for g in G:
        if g.get('modo') != 'palco':
            continue
        sc = g.get('scene') or []
        if not sc:
            err.append(f"{g['nome']}: grafica del palco senza «scene» (t, cosa, famiglia, nasce_da, reference)")
        for i, s in enumerate(sc):
            if s.get('famiglia') not in nomi_fam:
                err.append(f"{g['nome']}: scena {i + 1} con famiglia «{s.get('famiglia')}» che non è fra quelle del palco ({', '.join(sorted(nomi_fam))})")
            if i > 0 and not s.get('nasce_da'):
                err.append(f"{g['nome']}: scena {i + 1} senza «nasce_da» (gli oggetti si trasformano uno nell'altro, non compaiono a caso)")
            clip = str(s.get('reference') or '').split('@')[0]
            if not reference_valida(clip):
                err.append(f"{g['nome']}: scena {i + 1} senza una reference valida con la sua scheda («verticale-NN@secondi»"
                           + (" o «gadzhi-NN@secondi», «martell-NN@secondi»" if C.ORIZZONTALE else '') + ")")
        st, d = stati_di(g)
        if not st:
            err.append(f"{g['nome']}: grafica del palco senza dati.stati (le forme che attraversa)")
            continue
        for q in st:
            fo = forme.get(q.get('forma'))
            if not fo:
                err.append(f"{g['nome']}: forma «{q.get('forma')}» non dichiarata in palco.forme ({', '.join(forme)})")
                continue
            usate.add(q['forma'])
            r = [q['x'], q['y'], q['x'] + q['w'], q['y'] + q['h']]
            f0 = g['f0'] + round(q['da'] * fps)
            f1 = min(g['f0'] + g['frames'] - 1, g['f0'] + round(q['a'] * fps) - 1)
            fr = range(f0, f1 + 1)
            if set(fr) & tre:
                err.append(f"{g['nome']}: forma «{q['forma']}» aperta sulle animazioni 3D (fotogrammi {min(set(fr) & tre)}-{max(set(fr) & tre)})")
            if fo.get('video') == 'pieno':
                piene.append((g['nome'], q['forma'], (f1 - f0 + 1) / fps))
                for fm, bx in righe_s:
                    if fm[1] >= f0 and fm[0] <= f1 and not _dentro([bx[0] - 12, bx[1] - 14, bx[2] + 18, bx[3] + 20], r):
                        err.append(f"{g['nome']}: forma piena «{q['forma']}» che non copre tutta la riga di sottotitolo (y {bx[1]}–{bx[3]}): "
                                   "o la fascia resta identica o è coperta del tutto")
                        break
                continue
            # video fermo: la forma non tocca la fascia dei sottotitoli né i volti
            for fm, bx in righe_s:
                if fm[1] >= f0 and fm[0] <= f1 and _tocca(r, [bx[0] - 12, bx[1] - 14, bx[2] + 18, bx[3] + 20], 4):
                    err.append(f"{g['nome']}: la forma «{q['forma']}» {r} tocca la fascia dei sottotitoli (riga y {bx[1]}–{bx[3]}, fotogrammi "
                               f"{max(fm[0], f0)}-{min(fm[1], f1)}): con il video fermo la fascia resta identica")
                    break
            # 11/11/2026 (VSL_BRUXISMO_AI_01, render: alfa 35 sulla riga a due righe): l'ombra «alto» scende di ~60 px sotto la
            # forma (0 22px 40px); se sotto c'è una riga di sottotitolo più vicina, la vela. Lì si usa l'ombra «basso» o «no»
            if (q.get('ombra') or 'alto') == 'alto':
                for fm, bx in righe_s:
                    if (fm[1] >= f0 and fm[0] <= f1 and bx[1] >= r[3] and bx[1] - 4 - r[3] < OMBRA_ALTO_PX
                            and r[0] < bx[2] + 18 and r[2] > bx[0] - 12):
                        err.append(f"{g['nome']}: l'ombra «alto» della forma «{q['forma']}» (fondo y {r[3]}) arriva sulla riga di sottotitolo "
                                   f"(lettere da y {bx[1]}, fotogrammi {max(fm[0], f0)}-{min(fm[1], f1)}): usare \"ombra\": \"basso\" o \"no\"")
                        break
            if pers:
                # il volto della persona in camera non si copre mai; sul B-roll una forma può prendere il posto di una finestra
                # intera (Riccardo, 07/11/2026): lì è un avviso da guardare
                for f in fr:
                    if f >= len(pers):
                        break
                    tocca_v = [v for v in pers[f].get('volti') or [] if _tocca(r, v, 12)]
                    if tocca_v:
                        s_ = inq_di.get(f) or {}
                        if s_.get('tipo') == 'persona in camera':
                            err.append(f"{g['nome']}: la forma «{q['forma']}» {r} tocca il volto {tocca_v[0]} al fotogramma {f}")
                        else:
                            avv.append(f"{g['nome']}: la forma «{q['forma']}» copre un volto del B-roll al fotogramma {f} (inquadratura {s_.get('n')}): "
                                       "va bene solo se prende il posto di una finestra intera")
                        break
        for x in g.get('elementi') or []:
            d_ = x.get('dati') or {}
            if d_.get('attribuzione'):
                # 11/11/2026: anche la firma Servier è testo e sta nella zona sicura (il render la misurava, il piano no)
                for k_, (xa, ya) in enumerate([(d_.get('attr_x', 70), d_.get('attr_y', 893))] + [(q_[1], q_[2]) for q_ in d_.get('attr_pos') or []]):
                    if not (SAFE[0] <= xa <= SAFE[2] and SAFE[1] <= ya <= SAFE[3]):
                        err.append(f"{g['nome']}: la firma Servier in ({xa}, {ya}) è fuori dalla zona sicura (x {SAFE[0]}–{SAFE[2]}, y {SAFE[1]}–{SAFE[3]})")
                        break
            for p in d_.get('pezzi') or []:
                if p.get('tipo') == 'etichetta' and not (SAFE[0] <= p.get('x', 0) <= SAFE[2] and SAFE[1] <= p.get('y', 0) <= SAFE[3]):
                    err.append(f"{g['nome']}: etichetta «{p.get('testo')}» in ({p.get('x')}, {p.get('y')}) fuori dalla zona sicura (x {SAFE[0]}–{SAFE[2]}, y {SAFE[1]}–{SAFE[3]})")
    # 3. tutto schermo (forme piene e grafiche «tutto schermo»): solo scene complesse, brevi
    for g in G:
        if g.get('modo') == 'tutto schermo':
            piene.append((g['nome'], 'tutto schermo', g['frames'] / fps))
    if len(piene) > MAX_TUTTO_SCHERMO:
        err.append(f"{len(piene)} momenti a forma piena: al massimo {MAX_TUTTO_SCHERMO} (solo scene complesse, brevi)")
    for n, fo, s in piene:
        if s > MAX_TUTTO_SCHERMO_S:
            err.append(f"{n}: forma piena «{fo}» per {s:.1f} s (al massimo {MAX_TUTTO_SCHERMO_S:.0f} s, poi si torna alla forma di prima)")
    # 4. più forme quando l'inquadratura lo permette
    if len(usate) == 1 and len({s_.get('tipo') for s_ in R['inquadrature'] if s_.get('tipo')}) > 1:
        avv.append(f"il reel usa una sola forma ({', '.join(usate)}): di solito 2 o 3, secondo l'inquadratura (Riccardo, 07/11/2026)")
    # 5. struttura: se il copy ne ha una, l'indicatore
    if pal.get('struttura') and not any(p.get('tipo') == 'indicatore' for g in G for x in (g.get('elementi') or [])
                                        for p in ((x.get('dati') or {}).get('pezzi') or [])):
        err.append("palco: il copy ha una struttura (palco.struttura) ma nessuna grafica ha l'indicatore")
    return err, avv


# ---------------------------------------------------------------- tavola scena ↔ reference

def ritaglio_reference(clip):
    """il riquadro del reel dentro la registrazione dal browser (il palco delle reference; misurato sul movimento, 07/11/2026);
    None per le orizzontali (si prende tutto il quadro)"""
    if not clip.startswith('verticale-'):
        return None
    tab = {'01': (108, 252, 960), '02': (108, 236, 972), '03': (44, 245, 896), '04': (44, 245, 896), '05': (44, 245, 896),
           '06': (44, 245, 896), '07': (44, 245, 896), '08': (112, 273, 964), '09': (136, 252, 984), '10': (108, 252, 956),
           '11': (108, 252, 960)}
    n = clip.split('-')[-1]
    x0, y0, x1 = tab.get(n, (108, 252, 960))
    return (x0, y0, x1, min(1920, y0 + round((x1 - x0) * 16 / 9)))


def tavola(slug, video, out, solo=None):
    """per ogni scena del palco: il fotogramma nostro accanto al fotogramma della reference verticale da cui nasce
    (solo: il nome di una grafica, per il pacco del direttore)"""
    from PIL import Image, ImageDraw, ImageFont
    import io
    D = C.cartella(slug)
    P = C.leggi(D / 'piano.json')
    fps = C.leggi(D / 'radiografia.json')['fps']
    scene = []
    for g in sorted(P['grafiche'], key=lambda g: g['f0']):
        if solo and g['nome'] != solo:
            continue
        for s in g.get('scene') or []:
            scene.append((g, s))
    if not scene:
        return None
    fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 22)
    fnt2 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 19)
    cw, ch = (480, 270) if C.ORIZZONTALE else (300, 533)
    col = 2
    rw = 2 * cw + 30
    righe = math.ceil(len(scene) / col)
    hh = ch + 110
    tav = Image.new('RGB', (col * rw + 20, righe * hh + 70), (245, 245, 240))
    d = ImageDraw.Draw(tav)
    d.text((14, 16), f"{slug}: ogni scena del palco (sinistra, nostra) accanto alla reference da cui nasce (destra)", font=fnt, fill='black')
    for i, (g, s) in enumerate(scene):
        X = 10 + (i % col) * rw; Y = 60 + (i // col) * hh
        t = s.get('t_tavola', s['t'])
        f = min(g['f0'] + g['frames'] - 1, max(g['f0'], g['f0'] + round(t * fps)))
        b = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-vf', f'select=eq(n\\,{f}),scale={cw}:{ch}', '-frames:v', '1',
                            '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
        if b:
            tav.paste(Image.open(io.BytesIO(b)).convert('RGB'), (X, Y))
        clip, _, sec = str(s['reference']).partition('@')
        src = video_reference(clip)
        rt = ritaglio_reference(clip)
        crop = f'crop={rt[2] - rt[0]}:{rt[3] - rt[1]}:{rt[0]}:{rt[1]},' if rt else ''
        b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', sec or '0', '-i', str(src), '-frames:v', '1', '-vf',
                            f'{crop}scale={cw}:{ch}:force_original_aspect_ratio=decrease,pad={cw}:{ch}:-1:-1', '-f', 'image2pipe',
                            '-vcodec', 'png', '-'], capture_output=True).stdout if src else b''
        if b:
            tav.paste(Image.open(io.BytesIO(b)).convert('RGB'), (X + cw + 10, Y))
        else:
            # il video della reference non è su questo Mac: si rimanda alla scheda
            d.rectangle([X + cw + 10, Y, X + 2 * cw + 10, Y + ch], fill=(225, 225, 220))
            d.text((X + cw + 24, Y + 20), f"{clip}: video non presente", font=fnt, fill=(90, 90, 90))
            d.text((X + cw + 24, Y + 50), f"scheda: libreria/reference/schede/{clip}.md", font=fnt2, fill=(90, 90, 90))
        d.text((X, Y + ch + 6), f"{g['nome']} · {s['t'] + g['f0'] / fps:.2f} s · {s.get('famiglia', '')}", font=fnt, fill='black')
        d.text((X, Y + ch + 34), (s.get('cosa') or '')[:62], font=fnt2, fill=(40, 40, 40))
        d.text((X, Y + ch + 58), f"← {s['reference']}: {(s.get('come_la_reference') or '')[:44]}", font=fnt2, fill=(20, 80, 160))
    tav.save(out, quality=86)
    return out


# ---------------------------------------------------------------- direttore

REGOLE_PALCO = (
    "IL SISTEMA (Riccardo, 07/11/2026): stile fisso (lo stile del frontman è approvato) e PIÙ FORME: fascia alta, pannello sotto il "
    "volto (fra il mento e i sottotitoli, video fermo), badge in un angolo, pannello al posto di una finestra; brevi e solo per "
    "scene complesse: tendina che diventa tutto schermo, schermo diviso, card di vetro sul video sfocato. Un reel ne usa di solito "
    "2 o 3, scelte per inquadratura, con passaggi legati: un reel con UNA sola forma quando l'inquadratura ne permette altre è un "
    "difetto di impostazione. SOTTOTITOLI: quelli impressi nel montaggio non si toccano mai; o la fascia è identica "
    "all'originale (video fermo, grafiche intorno) o è coperta del tutto (grafica piena); segnala come difetto grave sottotitoli "
    "ritagliati o rimessi, doppi (una copia spostata visibile), tagliati da un bordo (mezza riga), velati, sfocati o scuriti. "
    "Niente elementi sparsi. Poche famiglie di oggetti-prova riconoscibili, grandi e curate (card, finestre, schemi, "
    "contatori, liste che si barrano, disegni Servier); gli oggetti si trasformano uno nell'altro invece di comparire e sparire a caso. "
    "Indicatore di struttura quando il copy ne ha una (1-2-3, passi). Tutto schermo solo per le scene complesse, brevi, poi si torna "
    "al palco. NON vale più la regola «copertura 85% e una novità ogni 2-3 s»: un tratto senza grafiche va bene se il palco è chiuso "
    "per un motivo (animazioni del montaggio, banner del montaggio). Il volto non si copre mai; le grafiche e le animazioni del "
    "montaggio (3D, pastiglie, banner, prezzo) non si coprono né si duplicano. I sottotitoli impressi restano visibili e fuori dalle "
    "zone Meta.")
REGOLE_SEMPRE = (
    f"Restano: testi nella zona sicura (x {SAFE[0]}–{SAFE[2]}, y {SAFE[1]}–{SAFE[3]}); lettere almeno 1,5 volte i sottotitoli; solo parole dette; mai "
    "cifre non dette; brand blu notte, verde #72FA93, panna, parola chiave in gradiente verde→azzurro; solo Montserrat; professionisti "
    "sanitari: niente promesse; mai «il tuo/la tua» insieme al disturbo; niente spunte, niente figure umane disegnate, anatomia solo "
    "Servier; mai card vuote; ogni segno si capisce subito a 390 px (un segno che sembra una cifra è grave); SOLO TESTO = BOCCIATO "
    "(una parola o una frase da sola non è una grafica: ogni scena deve MOSTRARE il concetto con un oggetto).")


def _fogli_reference(d, clips):
    """per le reference verticali citate: un foglio di 16 fotogrammi del reel (ritagliato dall'interfaccia di Instagram)"""
    from PIL import Image
    import io
    out = []
    for clip in clips:
        src = video_reference(clip)
        if not src:
            continue
        dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(src)],
                                   capture_output=True, text=True).stdout.strip() or 0)
        rt = ritaglio_reference(clip) or (0, 0, 0, 0)
        crop = f'crop={rt[2] - rt[0]}:{rt[3] - rt[1]}:{rt[0]}:{rt[1]},' if any(rt) else ''
        n = 16 if dur > 3 else 6
        tiles = []
        for k in range(n):
            b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f"{dur * (k + 0.5) / n:.2f}", '-i', str(src), '-frames:v', '1', '-vf',
                                f'{crop}scale=220:-2', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
            if b:
                tiles.append(Image.open(io.BytesIO(b)).convert('RGB'))
        if not tiles:
            continue
        tw, th = tiles[0].size
        sh = Image.new('RGB', (8 * (tw + 4), math.ceil(len(tiles) / 8) * (th + 4)), 'white')
        for i, t in enumerate(tiles):
            sh.paste(t, ((i % 8) * (tw + 4), (i // 8) * (th + 4)))
        p = d / f"reference-{clip}.jpg"
        sh.save(p, quality=85)
        out.append(p)
    return out


def prompt_grafica(slug, g, info_g, d, final, vis, fps, provini, telefono, interi):
    """il PROMPT.md del direttore per una grafica del palco"""
    P = C.leggi(C.cartella(slug) / 'piano.json')
    pal = P['palco']
    tav = d / f"{g['nome']}_scene-reference.jpg"
    tavola(slug, final, tav, solo=g['nome'])
    clips = sorted({str(s.get('reference', '')).split('@')[0] for s in g.get('scene') or [] if s.get('reference')})
    refs = _fogli_reference(d, clips)
    a, b = min(vis), max(vis)
    righe = [f"Sei il DIRETTORE ARTISTICO dei video di Studio Mobilitas (osteopatia). Voti UNA apertura del PALCO («{g['nome']}», "
             f"{a / fps:.2f}–{(b + 1) / fps:.2f} s) in un reel {'orizzontale 16:9' if C.ORIZZONTALE else 'verticale'} già montato. Rispondi in italiano.", '',
             "REGOLE (obbligatorie): sola lettura (non creare, modificare o cancellare file); non installare nulla; niente web né "
             f"caricamenti; niente git; non usare /tmp. Solo dentro {C.AGENTE}. Immagini con Read. Le persone non vanno descritte oltre "
             "il necessario.", '', REGOLE_PALCO] + ([forme_orizzontali()] if C.ORIZZONTALE else []) + ['', REGOLE_SEMPRE, '',
             f"IL SISTEMA DI QUESTO REEL: {pal['tipo']}; forme: " + '; '.join(f"{x['nome']} ({x.get('video', '')}): {x.get('quando', '')}" for x in pal.get('forme') or [])
             + "; famiglie: "
             + '; '.join((x['nome'] if isinstance(x, dict) else x) for x in pal['famiglie']) + '.',
             f"Voce: {g.get('voce', '')}", f"Che cosa dichiara di mostrare il piano: {g.get('mostra', '')}", '', 'LE SCENE (dal piano):']
    for s in g.get('scene') or []:
        righe.append(f"- {s['t'] + g['f0'] / fps:.2f} s · {s.get('famiglia')} · nasce da: {s.get('nasce_da', '—')} · reference {s.get('reference')}: "
                     f"{s.get('cosa')}")
    righe += ['', 'DA GUARDARE (Read):',
              f"- tavola scena ↔ reference (a sinistra la nostra scena, a destra il fotogramma della reference verticale da cui nasce): {C.rel(tav)}"]
    righe += [f"- provino ogni 0,25 s: {C.rel(p)}" for p in provini]
    righe += [f"- telefono 390 px (12 momenti): {C.rel(p)}" for p in telefono]
    righe += ['- piena risoluzione: ' + ', '.join(C.rel(p) for p in interi)]
    righe += [f"- reference {p.stem.replace('reference-', '')} (16 fotogrammi del reel; scheda in libreria/reference/schede/): {C.rel(p)}" for p in refs]
    senza = [c for c in clips if not video_reference(c)]
    righe += [f"- reference {c}: il video non è su questo Mac, leggi la scheda libreria/reference/schede/{c}.md" for c in senza]
    righe += ['', "RESTITUISCI: voto 1–10 (minimo 7). Giudica PRIMA DI TUTTO: (1) la coerenza del palco (zona e stile fissi, poche famiglie, "
              "oggetti che si trasformano invece di comparire a caso, indicatore quando serve); (2) per ogni scena, a quale clip verticale "
              "assomiglia ed è allo stesso livello? (di' cosa manca per arrivarci); poi leggibilità sul telefono, ritmo sulla voce, tono "
              "sanitario. Motivo in 4–6 frasi, difetti con il fotogramma o il tempo (esecuzione o impostazione), al massimo 3 correzioni "
              "concrete. Severo e preciso; non inventare."]
    (d / 'PROMPT.md').write_text('\n'.join(righe) + '\n', encoding='utf-8')
    return d / 'PROMPT.md'


def pacco_insieme(slug, full, tav):
    """il voto del reel intero con il palco: coerenza del palco in tutto il reel e confronto con le reference verticali"""
    from PIL import Image, ImageDraw, ImageFont
    import shutil
    D = C.cartella(slug)
    R = C.leggi(D / 'radiografia.json')
    P = C.leggi(D / 'piano.json')
    fps, nf = R['fps'], R['fotogrammi']
    d = C.lavoro(slug, 'direttore') / '_insieme'
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    passo = round(fps / 2)
    fs = list(range(0, nf, passo))
    tw, th = C.mini(390)
    im = C.estrai(full, fs, (tw, th))
    fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20)
    fogli = []
    nc, nr = (4, 6) if C.ORIZZONTALE else (8, 3)
    for k in range(0, len(fs), 24):
        sh = Image.new('RGB', (nc * (tw + 6), nr * (th + 6)), 'white')
        for i, f in enumerate(fs[k:k + 24]):
            x = im[f]; dr = ImageDraw.Draw(x); dr.rectangle([0, 0, 110, 26], fill=(255, 230, 0)); dr.text((4, 2), f'{f / fps:.1f}s', font=fnt, fill='black')
            sh.paste(x, ((i % nc) * (tw + 6), (i // nc) * (th + 6)))
        p = d / f"reel-390px-{fs[k] / fps:04.1f}s.jpg"
        sh.save(p, quality=85); fogli.append(p)
    citate = sorted({str(s.get('reference', '')).split('@')[0] for g in P['grafiche'] for s in g.get('scene') or [] if s.get('reference')})
    refs = _fogli_reference(d, citate or ['verticale-03', 'verticale-06', 'verticale-08', 'verticale-09'])
    pal = P['palco']
    chiusi = '; '.join(f"{x.get('momento')}: {x.get('perche')}" for x in P.get('senza_grafica') or [])
    righe = [f"Sei il DIRETTORE ARTISTICO dei reel di Studio Mobilitas (osteopatia). Questa volta voti il REEL INTERO «{slug}» (non una "
             "grafica): il palco in tutto il reel. Rispondi in italiano.", '',
             "REGOLE (obbligatorie): sola lettura; non installare nulla; niente web né caricamenti; niente git; non usare /tmp. Solo dentro "
             f"{C.AGENTE}. Immagini con Read.", '', REGOLE_PALCO] + ([forme_orizzontali()] if C.ORIZZONTALE else []) + ['', REGOLE_SEMPRE, '',
             f"IL SISTEMA DI QUESTO REEL: {pal['tipo']}; forme: " + '; '.join(f"{x['nome']} ({x.get('video', '')}): {x.get('quando', '')}" for x in pal.get('forme') or [])
             + f". Perché: {pal['perche']}", f"Dove il palco resta chiuso e perché: {chiusi}", '',
             'DA GUARDARE (Read):', f"- tavola scena ↔ reference: {C.rel(tav)}"]
    righe += [f"- un fotogramma ogni 0,5 s a misura di telefono: {C.rel(p)}" for p in fogli]
    righe += [f"- reference {p.stem.replace('reference-', '')}: {C.rel(p)}" for p in refs]
    righe += [f"- reference {c}: il video non è su questo Mac, leggi la scheda libreria/reference/schede/{c}.md" for c in citate if not video_reference(c)]
    righe += ['', "RESTITUISCI: voto 1–10 (minimo 7) del reel intero. Prima di tutto: i sottotitoli impressi sono intatti in ogni "
              "fotogramma (fascia identica o coperta del tutto; niente copie, mezze righe, veli)? Le forme sono scelte bene per "
              "inquadratura (2-3, passaggi legati) e lo stile resta uno solo, o sembra un collage? Regge il confronto con le reference citate (quali, e a che "
              "livello)? Poi: la persona resta leggibile e il volto mai coperto? I sottotitoli restano visibili? I tratti col palco chiuso "
              "sono giustificati? Si legge sul telefono? Tono sanitario. Motivo in 4–6 frasi, i momenti problematici con il tempo, al "
              "massimo 3 correzioni concrete. Severo e preciso; non inventare."]
    (d / 'PROMPT.md').write_text('\n'.join(righe) + '\n', encoding='utf-8')
    return d / 'PROMPT.md'

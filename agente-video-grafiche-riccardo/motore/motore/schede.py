"""Le due schede per le persone (v1.0, 02/11/2026).

- `controlli/anteprima-momenti.md` (+ `controlli/anteprima-momenti.jpg`): i momenti
  dell'anteprima 960x540, con i tempi, i modelli del catalogo e le parole a schermo,
  per guardarla con il piano accanto. La scrive `finale --anteprima` quando il video
  ha la scena (regia.json -> scena). In cima i punti «da decidere» presi da
  regia.json -> anteprima.da_decidere: [{"t": 50.0 | "0:50", "cosa": ..., "perche": ...}].
- `consegna/validazione-animazioni.md`: una voce per ogni animazione anatomica
  (modello `anatomia`), con il fotogramma, la frase detta, il disegno Servier di
  partenza, la domanda e la casella da firmare; in fondo la firma sul video intero.
  Si fa sempre, anche senza animazioni. La scrive `consegna` (o `./mve validazione`).
  Domande e descrizioni su misura: regia.json -> validazione:
  {"<id del momento>": {"cosa": ..., "domanda": ...}} (per il secondo elemento
  anatomico dello stesso momento: "<id>#2").

Prima di questo modulo le due schede si scrivevano con uno script fatto a mano per
ogni video (YT_POSTURA_32): ora le fa il motore, sempre uguali.
"""
import re
import subprocess

from .progetto import LIBRERIA, Progetto, ffmpeg

DOMANDA = ("il disegno, le zone evidenziate e i movimenti corrispondono a quello che dice? "
           "C'è qualcosa di sbagliato o di esagerato?")


def mm(s):
    """secondi -> m:ss,d"""
    return f"{int(s // 60)}:{s % 60:04.1f}".replace('.', ',')


def _secondi(t):
    if isinstance(t, (int, float)):
        return float(t)
    m, s = str(t).replace(',', '.').split(':')
    return int(m) * 60 + float(s)


def _video(P, slug):
    """il video da cui prendere i fotogrammi: consegnato, master, anteprima"""
    for p in (P.p('consegna', f"{slug}.mp4"), P.render(f"{slug}_FINALE.mp4"), P.render(f"{slug}_anteprima.mp4")):
        if p.exists():
            return p
    return None


def _fotogramma(video, t, out, larghezza=1280):
    out.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg('-ss', f"{t:.3f}", '-i', video, '-frames:v', '1', '-vf', f"scale={larghezza}:-2,format=yuvj420p",
           '-q:v', '3', out)
    return out


def _detto(parole, a, b, n=40):
    ws = [w[2] for w in parole if a <= w[0] < b]
    return ' '.join(ws[:n]) + (' …' if len(ws) > n else '')


def _servier(nome):
    """la riga di libreria/catalogo.md per un disegno: «titolo, pagina (file)»"""
    cat = LIBRERIA / 'catalogo.md'
    if not cat.exists():
        return nome
    for riga in cat.read_text(encoding='utf-8').splitlines():
        if nome in riga and riga.startswith('|'):
            col = [c.strip() for c in riga.strip('|').split('|')]
            if len(col) >= 2:
                titolo = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\2', col[1])
                return f"{titolo} ({nome})"
    return f"{nome} (non trovato in libreria/catalogo.md: aggiungilo)"


# ------------------------------------------------------------------ anteprima
def anteprima_momenti(P, video=None):
    """controlli/anteprima-momenti.md e .jpg dai momenti risolti (data/scena.json)"""
    from PIL import Image, ImageDraw
    from . import catalogo as CAT
    slug = P.slug
    S = P.leggi('scena.json')
    R = P.regia()
    G = P.leggi('grafica.json', {}) if P.data('grafica.json').exists() else {}
    per_id = {m['id']: m for m in R.get('scena', {}).get('momenti', [])}
    video = video or P.render(f"{slug}_anteprima.mp4")
    righe = []
    for m in S['momenti']:
        a, b = m['pezzo']
        mods = CAT.modelli_del_momento(per_id[m['id']]) if m['id'] in per_id else []
        cosa = []
        for x in m.get('testi', []):
            parole = ' / '.join(t for t in x['testi'] if t)[:160]
            cosa.append(f"{x['modello']} {mm(x['s'])}–{mm(x['e'])}" + (f" «{parole}»" if parole else ''))
        righe.append((a, b, m['id'], ', '.join(mods) or 'camera-viva', '; '.join(cosa) or 'lui a tutto schermo'))
    if G.get('chip'):
        c = G['chip']
        righe.append((c['s'], c['e'], 'chip', 'chip', f"«{c.get('name', '')} · {c.get('role', '')}»"))
    for x in G.get('broll', []):
        righe.append((x['s'], x['e'], 'b-roll', 'b-roll', ' + '.join(c['file'].split('/')[-1] for c in x['clip'])
                      + ' (senza audio)'))
    righe.sort(key=lambda r: r[0])
    fine = max((r[1] for r in righe), default=0)
    L = [f"# {slug}: i momenti dell'anteprima", '',
         f"Per guardare `renders/{slug}_anteprima.mp4` (960x540) con il piano accanto. "
         f"I tempi sono quelli dell'anteprima, uguali a quelli del video finale. Fotogrammi: `controlli/anteprima-momenti.jpg`.", '']
    dd = R.get('anteprima', {}).get('da_decidere', [])
    L += ['## Da decidere guardando l\'anteprima', '']
    if dd:
        L += ['| tempo | cosa | perché |', '|---|---|---|']
        L += [f"| {mm(_secondi(d['t']))} | {d['cosa']} | {d.get('perche', '')} |" for d in dd]
    else:
        L += ['Niente da segnalare (regia.json → anteprima.da_decidere è vuoto).']
    L += ['', '## I momenti', '', '| da | a | momento | modelli del catalogo | cosa si vede |', '|---|---|---|---|---|']
    L += [f"| {mm(a)} | {mm(b)} | {i} | {mo} | {c} |" for a, b, i, mo, c in righe]
    if S.get('coda'):
        L += [f"| {mm(fine)} | fine | coda | schermata-finale-youtube | schermata finale dopo l'ultima parola |"]
    P.controllo('anteprima-momenti.md').write_text('\n'.join(L) + '\n', encoding='utf-8')
    # un fotogramma per momento, a meta
    if video.exists():
        W, H, cols = 384, 216, 5
        tmp = P.controllo('anteprima-momenti')
        tmp.mkdir(exist_ok=True)
        tiles = []
        for k, (a, b, i, mo, _) in enumerate(righe):
            f = _fotogramma(video, (a + b) / 2, tmp / f"m{k:03d}.jpg", larghezza=W)
            tiles.append((f, f"{mm(a)} {i} · {mo}"[:58]))
        rows = -(-len(tiles) // cols)
        foglio = Image.new('RGB', (cols * W, rows * (H + 20)), 'white')
        d = ImageDraw.Draw(foglio)
        for k, (f, lab) in enumerate(tiles):
            im = Image.open(f).convert('RGB')
            im.thumbnail((W, H))
            x, y = (k % cols) * W, (k // cols) * (H + 20)
            foglio.paste(im, (x, y + 20))
            d.text((x + 4, y + 4), lab, fill='black')
        foglio.save(P.controllo('anteprima-momenti.jpg'), quality=85)
        for f, _ in tiles:
            f.unlink()
        tmp.rmdir()
    print(f"-> controlli/anteprima-momenti.md ({len(righe)} righe)" + (", controlli/anteprima-momenti.jpg" if video.exists() else ''))


# ------------------------------------------------------------------ validazione
def validazione(slug, rifai=False):
    """consegna/validazione-animazioni.md: da far firmare a un osteopata prima di pubblicare"""
    P = Progetto(slug)
    out = P.p('consegna', 'validazione-animazioni.md')
    out.parent.mkdir(exist_ok=True)
    if out.exists() and not rifai:
        print("   consegna/validazione-animazioni.md c'e gia (forse e firmata): non la riscrivo (--rifai per rifarla)")
        return out
    R = P.regia()
    video = _video(P, slug)
    parole = P.leggi('parole-montato.json', []) if P.data('parole-montato.json').exists() else []
    su_misura = R.get('validazione', {})
    voci = []
    if P.data('scena.json').exists():
        per_id = {m['id']: m for m in R.get('scena', {}).get('momenti', [])}
        for m in P.leggi('scena.json')['momenti']:
            spec = [x for x in per_id.get(m['id'], {}).get('elementi', []) if x.get('modello') == 'anatomia']
            ana = [x for x in m.get('testi', []) if x['modello'] == 'anatomia']
            for j, x in enumerate(ana):
                chiave = m['id'] + (f"#{j + 1}" if j else '')
                dati = spec[j].get('dati', {}) if j < len(spec) else {}
                voci.append({'momento': m['id'], 'chiave': chiave, 's': x['s'], 'e': x['e'],
                             'etichette': [t for t in x['testi'] if t], 'disegno': dati.get('disegno'),
                             **su_misura.get(chiave, {})})
    cart = P.controllo('validazione-animazioni')
    L = [f"# Validazione delle animazioni anatomiche: {slug}", '',
         "**Stato: da firmare.** Da far vedere a un osteopata dello studio **prima** di pubblicare il video. "
         "Un'animazione esce solo con il campo «approvato da» compilato; se l'osteopata chiede correzioni, "
         "si correggono e si rifà la scheda (`./mve validazione " + slug + " --rifai`).", '',
         f"Video: `{video.relative_to(P.dir) if video else 'non ancora renderizzato'}`; fotogrammi in "
         "`controlli/validazione-animazioni/`.", '',
         "Regole: ogni animazione parte da un disegno di **Servier Medical Art** (smart.servier.com, CC BY 4.0, "
         "voce in `libreria/catalogo.md`), ricolorato nel brand e inquadrato, mai deformato. Sopra solo forme "
         "semplici disegnate da noi (assi, frecce, aloni, contorni). Si mostra solo quello che il presentatore "
         "dice, mentre lo dice. L'attribuzione compare su ogni grafica con un disegno Servier.", '']
    if not voci:
        L += ["**In questo video non ci sono animazioni anatomiche.** Resta da firmare il video intero (sotto).", '']
    for k, v in enumerate(voci, 1):
        id_ = f"A{k}"
        t = v['s'] + (v['e'] - v['s']) * 0.6
        img = ''
        if video:
            f = _fotogramma(video, t, cart / f"{id_}.jpg")
            img = f"![{id_}](../controlli/validazione-animazioni/{f.name})"
        cosa = v.get('cosa') or (' / '.join(v['etichette'][:4]) if v['etichette'] else 'animazione senza testo')
        L += [f"## {id_}: {cosa}", '']
        if img:
            L += [img, '']
        L += [f"- **Nel video:** {mm(v['s'])}–{mm(v['e'])} (fotogramma a {mm(t)}, momento «{v['momento']}»)",
              f"- **Frase detta:** «{_detto(parole, v['s'], v['e'])}»",
              f"- **Disegno di partenza:** {_servier(v['disegno']) if v['disegno'] else 'non indicato'}",
              f"- **Parole a schermo:** {' / '.join(v['etichette']) or 'nessuna'}",
              f"- **Domanda:** {v.get('domanda') or DOMANDA}", '',
              '| approvato da | data | correzioni |', '|---|---|---|', '| | | |', '']
    L += ['## Il video intero', '',
          "L'osteopata ha guardato il video intero: testi a schermo, grafiche e sottotitoli non dicono cose "
          "sbagliate, non promettono risultati e non contraddicono il medico.", '',
          '| approvato da | data | correzioni |', '|---|---|---|', '| | | |', '']
    out.write_text('\n'.join(L) + '\n', encoding='utf-8')
    print(f"-> consegna/validazione-animazioni.md ({len(voci)} animazioni anatomiche"
          + ("" if video else "; nessun video: fotogrammi assenti") + ")")
    return out

"""Fase `consegna` (tappa 3, 30/10/2026): in consegna/ solo video, SRT e youtube.txt.

- `consegna/<slug>.srt`: sottotitoli a corredo per la traccia YouTube, a frasi,
  con le correzioni di regia (il file dice quello che si sente);
- `consegna/youtube.md`: titoli proposti, descrizione con i capitoli, tag;
- `consegna/capitoli.txt`: i capitoli da incollare in descrizione.

YouTube pretende che il primo capitolo parta da 0:00, che siano almeno tre e
che ognuno duri almeno 10 s: qui si controlla.
"""
import re
import shutil

from .progetto import Progetto, ts
from .grafica import piano as GP

MAX_CHARS, MAX_LINES, MAX_DUR, MIN_DUR, GAP = 42, 2, 3.6, 1.0, 0.55


def _srt_ts(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace('.', ',')


def _wrap(text):
    lines, cur = [], ''
    for w in text.split():
        cand = (cur + ' ' + w).strip()
        if len(cand) > MAX_CHARS and cur:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines


def srt(W, total):
    cues, cur = [], []
    for w in W:
        if cur:
            gap = w['s'] - cur[-1]['e']
            dur = cur[-1]['e'] - cur[0]['s']
            text = ' '.join(x['t'] for x in cur + [w])
            if (re.search(r'[.!?]$', cur[-1]['t']) or len(_wrap(text)) > MAX_LINES or dur >= MAX_DUR
                    or gap > GAP or (re.search(r'[,;:]$', cur[-1]['t']) and dur >= 1.7)):
                cues.append(cur)
                cur = []
        cur.append(w)
    if cur:
        cues.append(cur)
    # mai una battuta di una parola sola: si unisce alla precedente (o alla
    # successiva) se il testo unito sta in MAX_LINES righe e non scavalca una pausa lunga
    entra = lambda a, b: len(_wrap(' '.join(x['t'] for x in a + b))) <= MAX_LINES and b[0]['s'] - a[-1]['e'] <= 2 * GAP
    i = 0
    while i < len(cues):
        if len(cues[i]) == 1 and len(cues) > 1:
            if i > 0 and entra(cues[i - 1], cues[i]):
                cues[i - 1] += cues.pop(i)
                continue
            if i + 1 < len(cues) and entra(cues[i], cues[i + 1]):
                cues[i] += cues.pop(i + 1)
        i += 1
    out, nuova = [], True
    for i, c in enumerate(cues):
        s, e = c[0]['s'], max(c[-1]['e'], c[0]['s'] + MIN_DUR)
        if i + 1 < len(cues):
            e = min(e, cues[i + 1][0]['s'] - 0.04)
        e = min(max(e, s + 0.5), total - 0.05)
        text = ' '.join(x['t'] for x in c)
        if nuova and text:
            text = text[0].upper() + text[1:]
        nuova = bool(re.search(r'[.!?]$', text))
        out.append(f"{i + 1}\n{_srt_ts(s)} --> {_srt_ts(e)}\n" + '\n'.join(_wrap(text)))
    return '\n\n'.join(out) + '\n', len(cues)


def capitoli(G):
    rows = [(0.0, G.get('capitolo_iniziale', 'Introduzione'))]
    for c in G['capitoli']:
        if c.get('titolo_youtube'):
            rows.append((c['s'] + (0.0 if c['dietro'] else 1.3), c['titolo_youtube']))
    if G.get('finale'):
        rows.append((G['finale']['s'], G['finale']['titolo']))
    rows.sort()
    ok = [rows[0]]
    for t, title in rows[1:]:
        if t - ok[-1][0] >= 10:
            ok.append((t, title))
    problemi = []
    if len(ok) < 3:
        problemi.append("meno di tre capitoli: YouTube non li mostra")
    if G['duration'] - ok[-1][0] < 10:
        problemi.append("l'ultimo capitolo dura meno di 10 s")
    fmt = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
    return '\n'.join(f"{fmt(t)} {title}" for t, title in ok) + '\n', problemi


def capitoli_scena(P, R, durata):
    """capitoli YouTube allineati ai titoli a schermo (tappa 3): regia.json -> youtube.capitoli
    [{titolo, a_schermo}], dove `a_schermo` e il testo di un titolo dietro della scena (null =
    il primo, a 00:00). Il tempo e l'istante in cui il titolo entra, arrotondato al secondo sotto."""
    import math
    titoli = {}
    for m in P.leggi('scena.json')['momenti']:
        for x in m.get('testi', []):
            if x['modello'] in ('titolo_dietro', 'schermata'):
                titoli.setdefault(' '.join(x['testi']).lower(), x['s'])
    rows, problemi = [], []
    for c in R.get('youtube', {}).get('capitoli', []):
        if c.get('a_schermo') is None:
            rows.append((0.0, c['titolo']))
            continue
        k = c['a_schermo'].lower()
        if k not in titoli:
            problemi.append(f"il titolo a schermo «{c['a_schermo']}» non c'e nella scena")
            continue
        rows.append((float(math.floor(titoli[k])), c['titolo']))
    rows.sort()
    if not rows or rows[0][0] != 0:
        problemi.append("il primo capitolo non parte da 00:00")
    if len(rows) < 3:
        problemi.append("meno di tre capitoli: YouTube non li mostra")
    for (a, ta), (b, _) in zip(rows, rows[1:] + [(durata, '')]):
        if b - a < 10:
            problemi.append(f"il capitolo «{ta}» dura {b - a:.0f} s (minimo 10)")
    return rows, problemi


AMMESSI = {'youtube.txt', 'validazione-animazioni.md'}     # piu <slug>.mp4 e <slug>.srt


def consegna(slug, rifai=False):
    """tappa 3 (Riccardo, 30/10/2026): in consegna/ solo il video finale, l'SRT e youtube.txt
    (titoli, descrizione con i capitoli e le attribuzioni). Niente Shorts, niente miniature.
    v1.0 (02/11/2026): un mid-roll (info.txt o regia.json -> tipo) esce senza youtube.txt;
    sempre validazione-animazioni.md, da far firmare a un osteopata (una scheda gia
    esistente non si riscrive: potrebbe essere firmata; --rifai la rifa)."""
    import os
    import subprocess
    P = Progetto(slug)
    R = P.regia()
    G = P.leggi('grafica.json')
    dst = P.p('consegna')
    dst.mkdir(exist_ok=True)
    final = P.render(f"{slug}_FINALE.mp4")
    if not final.exists():
        raise SystemExit("manca il master: lancia prima ./mve finale " + slug)
    durata = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                   str(final)], capture_output=True, text=True).stdout.strip())
    # SRT sui tempi del montato finale, con le correzioni di regia
    W = GP.parole(P, R)
    testo, n = srt(W, G['duration'])
    (dst / f"{slug}.srt").write_text(testo, encoding='utf-8')
    righe = [r for r in testo.split('\n') if r.strip() and '-->' not in r and not r.strip().isdigit()]
    lunghe = [r for r in righe if len(r) > MAX_CHARS + 4]
    tipo = P.tipo
    problemi, cap = [], ''
    if tipo == 'youtube':
        # capitoli
        Y = R.get('youtube', {})
        if Y.get('capitoli'):
            rows, problemi = capitoli_scena(P, R, durata)
        else:
            cap_, problemi = capitoli(G)
            rows = [(sum(int(x) * 60 ** i for i, x in enumerate(reversed(r.split()[0].split(':')))), r.split(' ', 1)[1])
                    for r in cap_.strip().split('\n')]
        fmt = lambda t: f"{int(t // 60):02d}:{int(t % 60):02d}"
        cap = '\n'.join(f"{fmt(t)} {titolo}" for t, titolo in rows)
        titoli = Y.get('titoli', [])
        if len(titoli) != 3:
            problemi.append(f"{len(titoli)} titoli proposti invece di 3")
        problemi += [f"titolo oltre 70 caratteri: {t}" for t in titoli if len(t) > 70]
        txt = ["TITOLO (tre proposte, scegline una)", ""]
        txt += [f"{i + 1}. {t}" for i, t in enumerate(titoli)]
        txt += ["", "", "DESCRIZIONE (da copiare così com'è)", "", Y.get('descrizione', '').strip(), "", "Capitoli", cap]
        if Y.get('in_fondo'):
            txt += ["", Y['in_fondo'].strip()]
        corpo = '\n'.join(txt) + '\n'
        if '<' in corpo or '>' in corpo:
            problemi.append("la descrizione contiene < o >: YouTube li rifiuta")
        (dst / 'youtube.txt').write_text(corpo, encoding='utf-8')
    elif (dst / 'youtube.txt').exists():
        (dst / 'youtube.txt').unlink()          # mid-roll: niente pacchetto YouTube
    # il video: collegamento fisico al master (stesso file, niente copia da 1 GB)
    v = dst / f"{slug}.mp4"
    if v.exists():
        v.unlink()
    try:
        os.link(final, v)
    except OSError:
        shutil.copy2(final, v)
    for vecchio in ('youtube.md', 'capitoli.txt'):
        if (dst / vecchio).exists():
            (dst / vecchio).unlink()
    altri = [p.name for p in dst.iterdir() if p.name not in AMMESSI | {f"{slug}.mp4", f"{slug}.srt"}]
    print(f"{n} battute -> consegna/{slug}.srt" + (f"  ! {len(lunghe)} righe oltre {MAX_CHARS + 4} caratteri" if lunghe else ''))
    from .schede import validazione
    validazione(slug, rifai=rifai)
    if tipo == 'youtube':
        print(f"capitoli:\n{cap}")
        print(f"-> consegna/youtube.txt, consegna/{v.name} ({durata:.2f} s)")
    else:
        print(f"mid-roll: niente youtube.txt -> consegna/{v.name} ({durata:.2f} s)")
    for p in problemi:
        print(f"  ! {p}")
    if altri:
        print(f"  ! in consegna/ c'e altro oltre a video, SRT, youtube.txt e validazione: {', '.join(sorted(altri))}")
    if problemi or altri:
        raise SystemExit(1)

"""Fase `consegna`: tutto quello che serve per caricare il video.

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


def consegna(slug):
    P = Progetto(slug)
    R = P.regia()
    G = P.leggi('grafica.json')
    dst = P.p('consegna')
    dst.mkdir(exist_ok=True)
    W = GP.parole(P, R)
    testo, n = srt(W, G['duration'])
    (dst / f"{slug}.srt").write_text(testo, encoding='utf-8')
    cap, problemi = capitoli(G)
    (dst / 'capitoli.txt').write_text(cap, encoding='utf-8')
    Y = R.get('youtube', {})
    md = [f"# {slug}: pacchetto YouTube", "", "## Titoli proposti", ""]
    md += [f"{i + 1}. {t}  ({len(t)} caratteri)" for i, t in enumerate(Y.get('titoli', []))]
    md += ["", "## Descrizione", "", Y.get('descrizione', ''), "", cap.strip(), "",
           "## Tag", "", ', '.join(Y.get('tag', [])), "", "## File", "",
           f"- video: `renders/{slug}_FINALE.mp4`",
           f"- sottotitoli: `consegna/{slug}.srt` (da caricare come traccia, italiano)",
           "- miniature: `miniature/miniatura-1.jpg` … `-3.jpg`",
           "- shorts: `shorts/`"]
    titoli = {}
    for i, sh in enumerate(R.get('shorts', [])):
        titoli[f"{slug}_short{i + 1}.mp4"] = sh.get('titolo', '')
    files = sorted(P.p('shorts').glob('*.mp4')) if P.p('shorts').is_dir() else []
    for p in files:
        md.append(f"  - `{p.name}` — titolo: {titoli.get(p.name, '')}")
    if len(files) != len(titoli):
        print(f"  ! shorts in regia: {len(titoli)}, file in shorts/: {len(files)}")
    (dst / 'youtube.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
    final = P.render(f"{slug}_FINALE.mp4")
    print(f"{n} battute -> consegna/{slug}.srt")
    print(f"capitoli:\n{cap}", end='')
    for p in problemi:
        print(f"  ! {p}")
    print("-> consegna/youtube.md")
    if not final.exists():
        print("  ! manca ancora il master: renders/" + final.name)

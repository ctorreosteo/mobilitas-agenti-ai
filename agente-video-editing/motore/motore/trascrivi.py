"""Trascrizione con whisper.cpp, in tre modi per tre usi diversi.

1. **Intera** (`parole-sorgente.json`): una passata su tutto il file. Ha il
   contesto migliore, ma APPIANA le riprese doppie: al posto della papera
   scrive una frase corretta mai pronunciata. Non va usata da sola per tagliare.
2. **A finestre** (`parole-finestre.json`): finestre da 26 s ogni 20 s, ricucite
   tenendo di ognuna solo la parte centrale. Una finestra corta non vede le due
   riprese insieme e quindi non le fonde.
3. **Sonde**: clip brevi trascritte da sole (prima/dopo una pausa, attorno a
   una giunta). Servono come prova indipendente.

Flag che contano: `-mc 0` (senza, degenera in loop e lascia mezzo file vuoto),
`-dtw large.v3` (tempi per parola allineati), `-ml 1 -sow` (una parola per segmento).
"""
import concurrent.futures as cf
import json
import os
import re
import subprocess
import tempfile

from .progetto import Progetto, WHISPER_MODEL, ffmpeg
from . import audio

WIN, STEP, EDGE = 26.0, 20.0, 3.0
PARALLELO = 3

# frasi che whisper inventa sul silenzio
ALLUCINAZIONI = re.compile(r"amara\.org|sottotitoli (creati|a cura)|grazie per la visione|"
                           r"iscriviti al canale e attiva", re.I)


def _whisper(wav, prefix, dtw=True, threads=4, prompt=None):
    cmd = ['whisper-cli', '-m', str(WHISPER_MODEL), '-f', str(wav), '-l', 'it',
           '-t', str(threads), '-mc', '0', '-np', '-oj', '-ojf', '-of', str(prefix)]
    if dtw:
        cmd += ['-dtw', 'large.v3', '-ml', '1', '-sow']
    if prompt:
        cmd += ['--prompt', prompt]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    with open(str(prefix) + '.json', encoding='utf-8') as fh:
        return json.load(fh)


def parole(wav, offset=0.0, threads=4, prompt=None):
    """[[inizio, fine, parola], ...] in secondi, gia spostati di offset"""
    with tempfile.TemporaryDirectory() as tmp:
        d = _whisper(wav, os.path.join(tmp, 'w'), threads=threads, prompt=prompt)
    W = []
    for seg in d['transcription']:
        t = seg['text'].strip()
        if not t or t.startswith('[') or ALLUCINAZIONI.search(t):
            continue
        W.append([round(seg['offsets']['from'] / 1000 + offset, 3),
                  round(seg['offsets']['to'] / 1000 + offset, 3), t])
    return W


def testo(wav, threads=4):
    with tempfile.TemporaryDirectory() as tmp:
        d = _whisper(wav, os.path.join(tmp, 'w'), dtw=False, threads=threads)
    s = ' '.join(seg['text'].strip() for seg in d['transcription'])
    s = re.sub(r'\s+', ' ', s).strip()
    return '' if ALLUCINAZIONI.search(s) and len(s) < 80 else s


def clip(src, a, d, out):
    ffmpeg('-ss', f"{max(0.0, a):.3f}", '-t', f"{d:.3f}", '-i', src,
           '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', out)


def sonda(src, a, d, threads=4):
    """trascrive da sola la clip [a, a+d] di src"""
    with tempfile.TemporaryDirectory() as tmp:
        w = os.path.join(tmp, 'c.wav')
        clip(src, a, d, w)
        return testo(w, threads)


def sonde(src, finestre, threads=4, parallelo=PARALLELO):
    """[(a, d), ...] -> [testo, ...], in parallelo"""
    with cf.ThreadPoolExecutor(parallelo) as ex:
        return list(ex.map(lambda x: sonda(src, x[0], x[1], threads), finestre))


def a_finestre(src, durata, parallelo=PARALLELO, prompt=None):
    starts = []
    a = 0.0
    while a < durata:
        starts.append(a)
        a += STEP

    def one(a):
        with tempfile.TemporaryDirectory() as tmp:
            w = os.path.join(tmp, 'c.wav')
            clip(src, a, WIN, w)
            return a, parole(w, offset=a, prompt=prompt)

    with cf.ThreadPoolExecutor(parallelo) as ex:
        res = sorted(ex.map(one, starts))
    # l'ordine e quello di whisper, non quello dei tempi: dentro una finestra il
    # DTW a volte da tempi non monotoni, e riordinare mescola le parole
    W = []
    for i, (a, words) in enumerate(res):
        lo = a if i == 0 else a + EDGE
        hi = 1e9 if i == len(res) - 1 else a + STEP + EDGE
        W += [w for w in words if lo <= w[0] < hi]
    return W


def pulisci(W, tagli):
    """toglie le parole che cadono su silenzio vero: sono invenzioni del modello"""
    out = []
    for s, e, t in W:
        if e - s > 0.05 and tagli.silenzio(s, e) > 0.92:
            continue
        out.append([s, e, t])
    return out


def trascrivi(slug):
    P = Progetto(slug)
    asr = P.asset('audio-16k-asr.wav')
    dur = P.meta()['durata']
    tg = audio.Tagli(P.asset('audio-16k-mono.wav'))
    prompt = _prompt(P)
    if not P.data('parole-sorgente.json').exists():
        print("trascrizione intera (DTW)...")
        W = pulisci(parole(asr, threads=8, prompt=prompt), tg)
        P.scrivi('parole-sorgente.json', W)
        print(f"  {len(W)} parole, fino a {W[-1][1]:.1f}s")
        if W[-1][1] < dur * 0.85:
            print("  ! la trascrizione intera si ferma prima della fine: probabile loop del modello")
    if not P.data('parole-finestre.json').exists():
        print(f"trascrizione a finestre ({WIN:.0f}s ogni {STEP:.0f}s)...")
        W = pulisci(a_finestre(asr, dur, prompt=prompt), tg)
        P.scrivi('parole-finestre.json', W)
        print(f"  {len(W)} parole")
    if not P.data('blocchi-testo.json').exists():
        blocco_per_blocco(P)
    _testo_leggibile(P)


def _prompt(P):
    """il glossario del video (regia.json -> glossario) aiuta il modello sui termini"""
    try:
        g = P.regia().get('glossario', [])
    except SystemExit:
        g = []
    return ', '.join(g) if g else None


def parole_a_blocchi(wav, blocchi, prompt=None, parallelo=4):
    """parole con tempi DTW, trascrivendo ogni blocco di parlato da solo.

    Su un file lungo il DTW con -ml 1 PERDE la prima parola di molte frasi
    ("tuo cervello consuma" invece di "Il tuo cervello consuma"): nei
    sottotitoli v1 quelle parole mancavano. Blocco per blocco escono tutte.
    """
    def one(b):
        s, e = b
        with tempfile.TemporaryDirectory() as tmp:
            w = os.path.join(tmp, 'c.wav')
            clip(wav, s - 0.06, e - s + 0.12, w)
            ws = parole(w, offset=s - 0.06, threads=3, prompt=prompt)
        if e - s < 0.45 and len(ws) == 1 and re.fullmatch(r"(grazie|mh+|eh|ah)[.!]?", ws[0][2], re.I):
            return []
        # dentro il blocco e in ordine: il DTW a volte sfora di qualche decimo
        for x in ws:
            x[0] = round(min(max(x[0], s - 0.05), e), 3)
            x[1] = round(min(max(x[1], x[0] + 0.04), e + 0.1), 3)
        return ws

    with cf.ThreadPoolExecutor(parallelo) as ex:
        res = list(ex.map(one, blocchi))
    return [w for ws in res for w in ws]


def blocco_per_blocco(P):
    """Ogni blocco di parlato (fra due pause misurate sull'inviluppo) trascritto
    da solo. E la trascrizione piu affidabile che abbiamo, per due motivi:

    - whisper non vede mai due blocchi insieme, quindi non puo appianare una
      ripresa doppia nemmeno quando la pausa e di 0,8 s (in YT_TOFU_02 "si
      accorgono che il calo delle tre si e appiattito / si accorgono che il calo
      delle tre si appiattisce" stava proprio cosi, ed e uscita nel v1);
    - inizio e fine di ogni blocco sono misurati, non stimati dal DTW: sono i
      punti a cui ancorare i tagli.
    """
    bl = [b for b in P.leggi('blocchi.json') if b[1] - b[0] >= 0.12]
    asr = P.asset('audio-16k-asr.wav')
    print(f"trascrizione blocco per blocco ({len(bl)} blocchi, ognuno da solo)...")
    testi = sonde(asr, [(s - 0.05, e - s + 0.10) for s, e in bl], threads=3, parallelo=4)
    # sui rumori brevissimi whisper scrive "Grazie." o "mh": non e parlato
    out = [[s, e, '' if (e - s < 0.45 and re.fullmatch(r"(grazie|mh+|eh|ah)[.!]?", t.strip(), re.I)) else t]
           for (s, e), t in zip(bl, testi)]
    P.scrivi('blocchi-testo.json', out)
    vuoti = sum(1 for x in out if not x[2])
    print(f"  {len(out) - vuoti} blocchi con parlato, {vuoti} senza (respiri, rumori)")


def _testo_leggibile(P):
    """la trascrizione che l'agente legge: un blocco per riga, con inizio e fine
    misurati e la pausa che lo precede"""
    B = P.leggi('blocchi-testo.json')
    prev = 0.0
    with open(P.data('trascrizione.txt'), 'w', encoding='utf-8') as fh:
        fh.write("# un blocco di parlato per riga: [inizio-fine] (pausa prima) testo\n")
        for s, e, t in B:
            if t:
                fh.write(f"[{s:8.2f}-{e:8.2f}] ({s - prev:4.1f}) {t}\n")
            prev = e
    print(f"  -> data/trascrizione.txt ({sum(1 for b in B if b[2])} blocchi)")

"""Fasi `init` e `prep`: dal file di camera a un progetto pronto da analizzare."""
import datetime
import json
import os
import re
import struct
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from .progetto import VIDEOS, Progetto, scrivi, ffmpeg, esegui, fps_uscita
from . import audio, colore


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_streams',
                          '-show_format', str(path)], capture_output=True, text=True)
    d = json.loads(out.stdout)
    v = next(s for s in d['streams'] if s['codec_type'] == 'video')
    a = next((s for s in d['streams'] if s['codec_type'] == 'audio'), None)
    rot = 0
    for sd in v.get('side_data_list', []):
        if 'rotation' in sd:
            rot = int(sd['rotation'])
    w, h = int(v['width']), int(v['height'])
    if abs(rot) % 180 == 90:
        w, h = h, w
    num, den = (int(x) for x in v['r_frame_rate'].split('/'))
    trc = v.get('color_transfer', '')
    colore_ = 'hlg' if trc == 'arib-std-b67' else 'pq' if trc == 'smpte2084' else 'sdr'
    return {
        'larghezza': w, 'altezza': h, 'rotazione': rot,
        'fps': round(num / den, 3), 'fps_raw': v['r_frame_rate'],
        'codec': v['codec_name'], 'profilo': v.get('profile'), 'pix_fmt': v.get('pix_fmt'),
        'colore': colore_, 'trc': trc, 'primarie': v.get('color_primaries', ''),
        'durata': float(d['format']['duration']),
        'audio': bool(a), 'audio_canali': a.get('channels') if a else 0,
        'audio_sr': int(a['sample_rate']) if a else 0, 'audio_formato': a.get('codec_name') if a else None,
        'peso_gb': round(int(d['format']['size']) / 1e9, 2),
    }


# ---- XML Sony (NonRealTimeMeta) ----------------------------------------------
_CONTENITORI = {b'moov', b'udta', b'meta'}


def _xml_mp4(path, limite=50_000_000):
    """il box `xml ` dentro `meta` (in testa o in `moov`): li le Sony (XAVC, A6700, FX)
    scrivono NonRealTimeMeta. Si salta `mdat` senza leggerlo."""
    with open(path, 'rb') as fh:
        fine_file = os.fstat(fh.fileno()).st_size

        def giro(off, fine):
            while off + 8 <= fine:
                fh.seek(off)
                h = fh.read(16)
                size, tipo = struct.unpack('>I4s', h[:8])
                hdr = 8
                if size == 1:
                    size, hdr = struct.unpack('>Q', h[8:16])[0], 16
                elif size == 0:
                    size = fine - off
                if size < hdr:
                    return None
                if tipo == b'xml ' and size < limite:
                    fh.seek(off + hdr + 4)          # FullBox: versione e flag
                    return fh.read(size - hdr - 4)
                if tipo in _CONTENITORI and size < limite:
                    dentro = off + hdr
                    if tipo == b'meta':
                        fh.seek(dentro + 4)
                        if fh.read(4) != b'hdlr':   # MP4: FullBox; QuickTime: no
                            dentro += 4
                    r = giro(dentro, off + size)
                    if r:
                        return r
                off += size
            return None
        return giro(0, fine_file)


def camera(path):
    """camera, gamma di ripresa e frame rate dall'XML Sony, se c'e; altrimenti {}"""
    try:
        raw = _xml_mp4(path)
    except (OSError, struct.error):
        return {}
    if not raw or b'NonRealTimeMeta' not in raw:
        return {}
    try:
        root = ET.fromstring(raw.decode('utf-8', 'replace').strip().strip('\x00'))
    except ET.ParseError:
        return {}
    ns = {'n': root.tag.split('}')[0].strip('{')} if root.tag.startswith('{') else {}
    p = 'n:' if ns else ''
    out = {}
    dev = root.find(f'{p}Device', ns)
    if dev is not None:
        out['camera'] = ' '.join(x for x in (dev.get('manufacturer'), dev.get('modelName')) if x)
    vf = root.find(f'{p}VideoFormat/{p}VideoFrame', ns)
    if vf is not None:
        out['camera_fps'] = vf.get('captureFps')
    for it in root.iter(f"{{{ns['n']}}}Item" if ns else 'Item'):
        k = {'CaptureGammaEquation': 'gamma_ripresa', 'CaptureColorPrimaries': 'primarie_ripresa',
             'CodingEquations': 'matrice_ripresa'}.get(it.get('name'))
        if k:
            out[k] = it.get('value')
    return out


def _avviso_gamma(info):
    """None se la gamma di ripresa e quella che il motore sa trattare"""
    g = (info.get('gamma_ripresa') or '').lower()
    if not g or g == 'rec709':
        return None
    if 'hlg' in g and info['colore'] == 'hlg':
        return None                 # HLG dichiarato anche nel flusso: c'e il LUT
    return (f"gamma di ripresa '{info['gamma_ripresa']}' (dall'XML della camera), non rec709: "
            f"il motore la tratterebbe come Rec.709 ({info['colore'].upper()} secondo i tag del flusso) "
            f"e i colori uscirebbero sbagliati. Serve un LUT dedicato prima di montare.")


# ---- copione ------------------------------------------------------------------
_DESCRIZIONE = re.compile(r'^descrizione( per)? (youtube|yt)\b', re.I)


def copia_copione(src, dst):
    """copione .md o .txt -> copione.md: la prima riga diventa il titolo `# ...`
    (papere.py salta le righe con #) e la sezione "Descrizione YouTube" si toglie:
    non e parlato, e il segnale "copione" la cercherebbe nel girato.

    La sezione finisce al titolo markdown successivo dello stesso livello o piu alto;
    se e una riga di testo semplice, alla fine del file. Torna le righe tolte."""
    righe = Path(src).read_text(encoding='utf-8-sig').replace('\r\n', '\n').replace('\r', '\n').split('\n')
    righe = [r.rstrip() for r in righe]
    i = next((k for k, r in enumerate(righe) if r.strip()), None)
    if i is None:
        sys.exit(f"copione vuoto: {src}")
    titolo = righe[i].lstrip('#').strip()
    out, tolte, salta, livello = [], 0, False, None
    for r in righe[i + 1:]:
        h = re.match(r'^(#{1,6})\s', r)
        lv = len(h.group(1)) if h else None
        nome = re.sub(r'[#*_:]+', ' ', r).strip()
        if _DESCRIZIONE.match(nome):
            salta, livello = True, lv
            tolte += 1
            continue
        if salta and lv is not None and (livello is None or lv <= livello):
            salta = False
        if salta:
            tolte += bool(r.strip())
        else:
            out.append(r)
    while out and not out[0]:
        out.pop(0)
    while out and not out[-1]:
        out.pop()
    Path(dst).write_text(f"# {titolo}\n\n" + '\n'.join(out) + '\n', encoding='utf-8')
    return titolo, tolte


GIRATO = {'.mp4', '.mov', '.mxf', '.m4v'}
TESTO = {'.md', '.txt'}
INFO = 'info.txt'
TIPI = {'youtube': 'youtube', 'yt': 'youtube', 'mid-roll': 'mid-roll', 'midroll': 'mid-roll',
        'mid roll': 'mid-roll'}


def leggi_info(cartella):
    """inbox/<NOME>/info.txt: righe «chiave: valore». Servono `osteopata` (nome e
    cognome, per il chip) e `tipo` (YouTube o mid-roll); `ruolo` e facoltativo.
    Torna (info, mancanti)."""
    p = Path(cartella) / INFO
    info = {}
    if p.is_file():
        for riga in p.read_text(encoding='utf-8', errors='replace').splitlines():
            if ':' in riga and not riga.lstrip().startswith('#'):
                k, v = riga.split(':', 1)
                k, v = k.strip().lower(), v.strip()
                if k in ('osteopata', 'nome', 'presentatore'):
                    k = 'osteopata'
                if k == 'tipo':
                    v = TIPI.get(v.lower(), v)
                if v:
                    info[k] = v
    mancanti = [k for k in ('osteopata', 'tipo') if not info.get(k)]
    if info.get('tipo') and info['tipo'] not in ('youtube', 'mid-roll'):
        mancanti.append(f"tipo («{info['tipo']}»: si scrive YouTube o mid-roll)")
    return info, mancanti


def _dalla_cartella(cartella, copione):
    """inbox/<SLUG>/ -> (girato, copione). Il girato e l'unico video nella cartella
    (non in materiali/); il copione l'unico .md/.txt, se non e gia stato indicato.
    Piu candidati: ci si ferma, non si sceglie a caso."""
    girati = sorted(p for p in cartella.iterdir() if p.is_file() and p.suffix.lower() in GIRATO)
    if not girati:
        sys.exit(f"nessun girato (.mp4, .mov, .mxf) in {cartella}")
    if len(girati) > 1:
        sys.exit(f"piu girati in {cartella}: " + ', '.join(p.name for p in girati)
                 + "\n  indica quale: ./mve init <file> [slug]")
    if copione is None:
        testi = sorted(p for p in cartella.iterdir() if p.is_file() and p.suffix.lower() in TESTO
                       and not p.name.startswith('.') and p.name.lower() not in (INFO, 'leggimi.md'))
        if len(testi) == 1:
            copione = testi[0]
        elif len(testi) > 1:
            print(f"  ! piu testi in {cartella} ({', '.join(p.name for p in testi)}): nessun copione scelto, "
                  f"indicalo con --copione")
    return girati[0], copione


def init(file, slug=None, copione=None):
    src = Path(file).expanduser().resolve()
    if not src.exists():
        sys.exit(f"file non trovato: {src}")
    if src.is_dir():
        slug = slug or src.name
        src, copione = _dalla_cartella(src, copione)
    if copione and not Path(copione).expanduser().is_file():
        sys.exit(f"copione non trovato: {copione}")
    slug = slug or re.sub(r'[^\w-]+', '-', src.stem).strip('-')
    d = VIDEOS / slug
    d.mkdir(parents=True, exist_ok=True)
    link = d / f"sorgente{src.suffix}"
    if src.parent != d:
        if link.is_symlink() or link.exists():
            link.unlink()
        os.symlink(src, link)            # mai spostare il girato: si collega
    else:
        link = src
    info = probe(src)
    info['fps_uscita'] = fps_uscita(info['fps_raw'])
    info.update(camera(src))
    avviso = _avviso_gamma(info)
    meta = {'slug': slug, 'sorgente': link.name, 'originale': str(src),
            'creato': datetime.datetime.now().isoformat(timespec='seconds'), **info}
    if avviso:
        meta['avviso_gamma'] = avviso
    if copione:
        titolo, tolte = copia_copione(Path(copione).expanduser(), d / 'copione.md')
        meta['copione'] = {'origine': str(Path(copione).expanduser().resolve()), 'righe_tolte': tolte}
    if (src.parent / 'materiali').is_dir():
        meta['materiali'] = str(src.parent / 'materiali')
    info_, mancanti = leggi_info(src.parent)
    if info_:
        meta['info'] = info_
    scrivi(d / 'meta.json', meta)
    print(f"progetto {slug}: {info['larghezza']}x{info['altezza']} {info['fps']}p "
          f"{info['codec']} {info['colore'].upper()}, {info['durata']/60:.1f} min, "
          f"rotazione {info['rotazione']}")
    print(f"  uscita a {info['fps_uscita']} fps"
          + (" (sorgente oltre 30: un frame si e uno no)" if info['fps_uscita'] != info['fps_raw'] else ""))
    if info.get('camera'):
        print(f"  camera {info['camera']}, gamma di ripresa {info.get('gamma_ripresa', '?')}")
    if copione:
        print(f"  copione «{titolo}» -> copione.md"
              + (f" ({tolte} righe di descrizione YouTube tolte)" if tolte else ""))
    if meta.get('materiali'):
        n = sum(1 for p in Path(meta['materiali']).rglob('*') if p.is_file() and not p.name.startswith('.'))
        print(f"  materiali del video: {n} file in {meta['materiali']}")
    if info_:
        print(f"  info.txt: " + ', '.join(f"{k} {v}" for k, v in info_.items()))
    if mancanti:
        print(f"  ! manca in {src.parent.name}/info.txt: {', '.join(mancanti)} (chiedilo prima di andare avanti)")
    if not copione:
        print("  ! nessun copione: chiedilo prima di andare avanti")
    if info['altezza'] < 2160:
        print("  ! sorgente sotto il 4K: i punch-in verranno limitati per non ingrandire oltre i pixel nativi")
    if avviso:
        _strillo(avviso)
    return slug


def _strillo(testo):
    riga = '!' * 78
    print(f"\n{riga}\n!!! ATTENZIONE: {testo}\n{riga}\n", file=sys.stderr)


def materiali(slug):
    """elenca i materiali che le fasi possono usare, nell'ordine in cui li cercano"""
    P = Progetto(slug)
    cartelle = P.cartelle_materiali()
    if not cartelle:
        print("nessuna cartella di materiali (inbox/<slug>/materiali/, libreria/)")
    for i, c in enumerate(cartelle, 1):
        files = sorted(p for p in c.rglob('*') if p.is_file() and not p.name.startswith('.'))
        print(f"{i}. {c}  ({len(files)} file)")
        gruppi = {}
        for p in files:
            gruppi.setdefault(str(p.parent.relative_to(c)), []).append(p.name)
        for g, nomi in sorted(gruppi.items()):
            print(f"     {g + '/' if g != '.' else '':<24} {len(nomi):4d}  " + ', '.join(nomi[:4])
                  + (' ...' if len(nomi) > 4 else ''))


def prep(slug):
    P = Progetto(slug)
    src = P.sorgente
    m = P.meta()
    # analisi: mono 16k grezzo (per l'inviluppo il livello vero conta)
    if not P.asset('audio-16k-mono.wav').exists():
        ffmpeg('-i', src, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le',
               P.asset('audio-16k-mono.wav'))
    # riconoscimento: normalizzato a -20, o whisper puo degenerare in loop
    if not P.asset('audio-16k-asr.wav').exists():
        ffmpeg('-i', src, '-vn', '-af', 'highpass=f=70,loudnorm=I=-20:TP=-2', '-ac', '1',
               '-ar', '16000', '-c:a', 'pcm_s16le', P.asset('audio-16k-asr.wav'))
    # master: 48k a 24 bit, nessun trattamento (la catena voce sta nel montaggio)
    if not P.asset('audio-48k.wav').exists():
        ffmpeg('-i', src, '-vn', '-ac', '2', '-ar', '48000', '-c:a', 'pcm_s24le',
               P.asset('audio-48k.wav'))
    if m['colore'] == 'hlg':
        print(f"LUT HLG -> BT.709: {colore.lut_hlg()}")
    if m.get('avviso_gamma'):
        _strillo(m['avviso_gamma'])
    blocchi, floor, thr = audio.blocchi(P.asset('audio-16k-mono.wav'))
    P.scrivi('blocchi.json', blocchi)
    lufs = audio.loudness(P.asset('audio-48k.wav'))
    # il clipping si misura sulla sorgente, nel suo formato: audio-48k.wav potrebbe
    # essere ricampionato
    clip = audio.clipping(src, m['audio_canali'], m['audio_sr']) if m.get('audio_sr') else None
    m.update({'fondo_sala_db': round(floor, 1), 'soglia_parlato_db': round(thr, 1),
              'lufs_sorgente': lufs, 'clipping': clip})
    scrivi(P.p('meta.json'), m)
    print(f"audio: {lufs['I']} LUFS, true peak {lufs['TP']} dBTP; fondo di sala {floor:.1f} dBFS")
    if clip is None:
        print("  ! clipping non misurato: meta.json non ha audio_sr (progetto creato prima: rilancia init)")
    elif clip['corse']:
        print(f"  ! clipping: {clip['campioni_fondo_scala']} campioni a fondo scala, {clip['corse']} corse "
              f"(la piu lunga {clip['corsa_max_istanti']} istanti) in {clip['tratti_totali']} tratti:")
        for t in clip['tratti'][:12]:
            print(f"      {t['s']:8.2f} - {t['e']:8.2f} s  {t['corse']} corse, {t['istanti']} istanti")
        if clip['tratti_totali'] > 12:
            print(f"      ... (tutti in meta.json -> clipping)")
    else:
        print(f"  clipping: nessuno ({clip['campioni_fondo_scala']} campioni isolati a fondo scala)")
    prima = audio.catena_voce(m)[:-len(audio.CATENA_VOCE)].rstrip(',')
    print(f"  catena voce: {prima + ' + ' if prima else ''}standard")
    print(f"{len(blocchi)} blocchi di parlato -> data/blocchi.json")

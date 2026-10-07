#!/usr/bin/env python3
"""Client Higgsfield per la generazione dei B-roll.

Fa tre cose e nient'altro: stima quanto costa un piano, lo genera, lo riprende dove
si era fermato. Non decide niente di editoriale: i prompt arrivano gia' scritti nel
piano, i modelli arrivano dal catalogo. Se questo file contiene una scelta creativa,
e' un bug.

Due vincoli dell'API che spiegano meta' del codice:

1. Le POST di generazione NON accettano una chiave di idempotenza. Dopo un timeout
   ambiguo non si puo' ripetere la POST: si rischia di pagare due volte la stessa
   immagine. Per questo il request_id finisce su disco PRIMA di iniziare il polling,
   e una ripresa interroga quel request_id invece di inviarne uno nuovo.

2. Il limite di concorrenza e' per account (400 "Maximum number of concurrent
   requests"). Il pool di worker e' il rispetto di quel limite: un worker per volta
   tiene al massimo una richiesta in volo, quindi worker = concorrenza.

Uso:
    higgsfield.py credenziali
    higgsfield.py stima    --piano piano.json --catalogo modelli-higgsfield.json
    higgsfield.py genera   --piano piano.json --catalogo modelli-higgsfield.json --out DIR
    higgsfield.py genera   ... --solo-immagini      # valida le scene prima di pagare i video
    higgsfield.py genera   ... --rigenera 03-pain-cena
"""

import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock

# Senza questo, un banale `| head` chiude la pipe e il client muore con un traceback
# che sembra un errore di generazione. Non lo e' mai.
try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (ImportError, AttributeError, ValueError):
    pass

TERMINALI = {"completed", "failed", "nsfw", "canceled"}
_stampa = Lock()


def log(msg):
    with _stampa:
        print(msg, flush=True)


class Fermata(Exception):
    """Errore che non ha senso ritentare: credenziali, crediti, modello assente."""


# --------------------------------------------------------------------------- HTTP

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"

# Il bordo Cloudflare davanti a api.higgsfield.ai rifiuta lo User-Agent di urllib.
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) mobilitas-broll/1.0"


def carica_env():
    """Legge le chiavi dal file .env dell'agente, se c'e'.

    Il file e' escluso da git e ha permessi 600: e' il posto giusto per un segreto su
    una macchina personale. L'ambiente ha comunque la precedenza, cosi' una chiave
    esportata a mano per una prova batte quella scritta nel file senza doverlo toccare.
    """
    if not ENV_FILE.exists():
        return
    for riga in ENV_FILE.read_text().splitlines():
        riga = riga.strip()
        if not riga or riga.startswith("#") or "=" not in riga:
            continue
        chiave, _, valore = riga.partition("=")
        chiave = chiave.strip()
        valore = valore.strip().strip('"').strip("'")
        if chiave and valore and not os.environ.get(chiave):
            os.environ[chiave] = valore


def credenziali():
    carica_env()
    kid = os.environ.get("HF_API_KEY_ID", "").strip()
    sec = os.environ.get("HF_API_KEY_SECRET", "").strip()
    # La console mostra le due chiavi vicine e si incolla facilmente la coppia intera
    # nel campo del segreto. In quel caso l'header uscirebbe "Key id:id:segreto" e
    # l'API risponde 401. Se il segreto porta gia' l'id davanti, si tiene la coda.
    if kid and sec.startswith(kid + ":"):
        sec = sec[len(kid) + 1:]
    if not kid or not sec:
        mancanti = [n for n, v in (("HF_API_KEY_ID", kid), ("HF_API_KEY_SECRET", sec)) if not v]
        raise Fermata(
            f"Credenziali assenti: manca {' e '.join(mancanti)}.\n"
            f"Aprile in {ENV_FILE} e incolla i valori dopo l'uguale.\n"
            f"{'Quel file non esiste: copialo da .env.esempio.' if not ENV_FILE.exists() else 'Il file esiste ma il valore e vuoto.'}\n"
            "Le chiavi si creano su https://console.higgsfield.ai, sezione API keys."
        )
    return f"Key {kid}:{sec}"


def chiama(url, auth, corpo=None, tentativi=5):
    """POST se c'e' un corpo, GET altrimenti. Ritenta solo cio' che ha senso ritentare."""
    dati = json.dumps(corpo).encode() if corpo is not None else None
    attesa = 2.0
    ultimo = None
    for i in range(tentativi):
        req = urllib.request.Request(url, data=dati, method="POST" if dati else "GET")
        req.add_header("Authorization", auth)
        # Senza User-Agent parte "Python-urllib/3.x", che il bordo Cloudflare davanti
        # all'API rifiuta con 403 "error code: 1010" prima ancora di arrivare a
        # Higgsfield. Il 403 sembra allora un problema di crediti e non lo e'.
        req.add_header("User-Agent", UA)
        if dati:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            testo = e.read().decode(errors="replace")[:400]
            ultimo = f"HTTP {e.code}: {testo}"
            if e.code in (401, 403, 404, 422):
                # 401 credenziali, 403 rifiuto del bordo o permesso negato,
                # 404 modello non nel tuo account, 422 body invalido.
                # Ritentare non cambia niente e su 403 brucia tempo.
                # NB: un 403 con "error code: 1010" e' Cloudflare che blocca lo
                # User-Agent, NON i crediti finiti.
                raise Fermata(f"{url}\n{ultimo}")
            if e.code == 400 and "concurrent" in testo.lower():
                log(f"  [attesa] limite di concorrenza raggiunto, riprovo fra {attesa:.0f}s")
            elif e.code in (423, 503):
                log(f"  [attesa] modello non disponibile ({e.code}), riprovo fra {attesa:.0f}s")
            elif e.code == 400:
                raise Fermata(f"{url}\n{ultimo}")
        except Exception as e:  # rete, timeout, DNS
            ultimo = f"{type(e).__name__}: {e}"
        if i + 1 < tentativi:
            time.sleep(attesa + random.uniform(0, 0.5))
            attesa = min(attesa * 1.8, 30.0)
    raise RuntimeError(f"{url} — fallito dopo {tentativi} tentativi. Ultimo errore: {ultimo}")


def attendi(base, request_id, auth, scadenza_s):
    """Polling con backoff, come raccomanda la documentazione: 2s -> 10s con jitter."""
    url = f"{base}/requests/{request_id}/status"
    attesa, limite = 2.0, time.time() + scadenza_s
    while True:
        st = chiama(url, auth)
        stato = st.get("status")
        if stato in TERMINALI:
            return st
        if time.time() > limite:
            return {"status": "timeout", "request_id": request_id,
                    "error": f"nessuno stato terminale entro {scadenza_s}s"}
        time.sleep(attesa + random.uniform(0, 0.5))
        attesa = min(attesa * 1.5, 10.0)


def scarica(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as r, open(dest, "wb") as f:
        while True:
            pezzo = r.read(1 << 16)
            if not pezzo:
                break
            f.write(pezzo)
    return dest


# ------------------------------------------------------------------------ CATALOGO

def modello(catalogo, chiave, tipo):
    m = catalogo["modelli"].get(chiave)
    if not m:
        raise Fermata(f"Modello '{chiave}' assente dal catalogo. Presenti: {', '.join(catalogo['modelli'])}")
    if m.get("tipo") != tipo:
        raise Fermata(f"Modello '{chiave}' e' di tipo '{m.get('tipo')}', ne serviva uno '{tipo}'.")
    if not m.get("disponibile_su_api") or not m.get("endpoint"):
        raise Fermata(
            f"Modello '{chiave}' ({m.get('nome')}) non ha un endpoint API.\n"
            f"Motivo registrato nel catalogo: {m.get('limiti', 'non dichiarato')}\n"
            f"Usa uno dei ripieghi: {', '.join(catalogo.get('ripieghi', {}).get(tipo, []))}"
        )
    return m


def corpo(m, valori):
    """Traduce i nomi del piano nei nomi che quel modello si aspetta, via 'mappa'."""
    body = dict(m.get("parametri") or {})
    mappa = m.get("mappa") or {}
    for interno, valore in valori.items():
        if valore in (None, "", []):
            continue
        campo = mappa.get(interno)
        if campo:
            body[campo] = valore
    return body


def controlla_ratio(m, ratio):
    consentiti = m.get("aspect_ratio_supportati") or []
    if consentiti and ratio not in consentiti:
        raise Fermata(
            f"Il modello '{m['nome']}' non supporta l'aspect ratio {ratio}. Supportati: {', '.join(consentiti)}"
        )


def controlla_durata(m, durata):
    lo, hi = m.get("durata_min"), m.get("durata_max")
    if lo and hi and not (lo <= durata <= hi):
        raise Fermata(f"Durata {durata}s fuori dai limiti di '{m['nome']}' ({lo}-{hi}s).")


# --------------------------------------------------------------------------- STATO

class Stato:
    """stato.json: cosa e' gia' stato chiesto e cosa e' gia' arrivato.

    E' l'unica difesa contro il pagare due volte. Si scrive dopo ogni evento, non
    alla fine: una sessione che muore a meta' deve lasciare il disco veritiero.
    """

    def __init__(self, percorso):
        self.percorso = Path(percorso)
        self.lock = Lock()
        self.dati = json.loads(self.percorso.read_text()) if self.percorso.exists() else {}

    def get(self, bid, fase):
        return (self.dati.get(bid) or {}).get(fase) or {}

    def segna(self, bid, fase, **campi):
        with self.lock:
            self.dati.setdefault(bid, {}).setdefault(fase, {}).update(campi)
            self.percorso.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.percorso.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.dati, indent=2, ensure_ascii=False))
            tmp.replace(self.percorso)

    def dimentica(self, bid):
        with self.lock:
            self.dati.pop(bid, None)
            self.percorso.write_text(json.dumps(self.dati, indent=2, ensure_ascii=False))


# ------------------------------------------------------------------------ GENERAZIONE

def una_fase(base, auth, stato, bid, fase, endpoint, body, scadenza, campo_esito, dest, dry):
    """Una generazione: riusa cio' che c'e', altrimenti invia, aspetta, scarica.

    Le tre uscite corrispondono ai tre stati possibili su disco:
      - file gia' scaricato        -> non si tocca niente
      - request_id senza risultato -> si interroga QUELLO, non se ne invia un altro
      - niente                     -> si invia
    """
    prec = stato.get(bid, fase)
    if prec.get("file") and Path(prec["file"]).exists():
        log(f"  [{bid}/{fase}] gia' su disco, salto")
        return prec

    if dry:
        log(f"  [{bid}/{fase}] DRY-RUN POST {base}/{endpoint}\n      {json.dumps(body, ensure_ascii=False)[:500]}")
        return {"status": "dry-run"}

    rid = prec.get("request_id")
    if rid and prec.get("status") not in TERMINALI:
        log(f"  [{bid}/{fase}] ripresa: interrogo la richiesta {rid} invece di rinviarla")
    else:
        risp = chiama(f"{base}/{endpoint}", auth, body)
        rid = risp.get("request_id")
        if not rid:
            raise RuntimeError(f"[{bid}/{fase}] risposta senza request_id: {risp}")
        # Su disco PRIMA del polling: e' il momento in cui i crediti sono gia' impegnati.
        stato.segna(bid, fase, request_id=rid, status=risp.get("status"), endpoint=endpoint)
        log(f"  [{bid}/{fase}] inviata ({rid})")

    esito = attendi(base, rid, auth, scadenza)
    stato.segna(bid, fase, status=esito.get("status"), errore=esito.get("error"))
    if esito.get("status") != "completed":
        raise RuntimeError(f"[{bid}/{fase}] esito '{esito.get('status')}': {esito.get('error') or 'nessun dettaglio'}")

    media = esito.get(campo_esito)
    if isinstance(media, list):
        media = media[0] if media else None
    url = (media or {}).get("url")
    if not url:
        raise RuntimeError(f"[{bid}/{fase}] completata ma senza '{campo_esito}': {esito}")

    # Il CDN Higgsfield tiene i file almeno sette giorni. Scaricare non e' un extra.
    scarica(url, dest)
    stato.segna(bid, fase, url=url, file=str(dest))
    log(f"  [{bid}/{fase}] pronto -> {dest.name}")
    return stato.get(bid, fase)


def lavora(br, ctx):
    bid = br["id"]
    try:
        img = una_fase(
            ctx["base"], ctx["auth"], ctx["stato"], bid, "immagine",
            ctx["mi"]["endpoint"],
            corpo(ctx["mi"], {
                "prompt": br["prompt_t2i"],
                "aspect_ratio": ctx["ratio"],
                "riferimento_personaggio": br.get("riferimento_personaggio"),
                "immagini_riferimento": br.get("immagini_riferimento"),
            }),
            ctx["scad_img"], "images", ctx["out"] / "immagini" / f"{bid}.jpg", ctx["dry"],
        )
        if ctx["solo_immagini"]:
            return {"id": bid, "esito": "immagine", "immagine": img.get("file")}

        url_img = img.get("url")
        if not url_img and not ctx["dry"]:
            raise RuntimeError(f"[{bid}] nessun URL immagine da passare al video")

        vid = una_fase(
            ctx["base"], ctx["auth"], ctx["stato"], bid, "video",
            ctx["mv"]["endpoint"],
            corpo(ctx["mv"], {
                "prompt": br["prompt_i2v"],
                "immagine": url_img,
                "durata": br.get("durata", 5),
            }),
            ctx["scad_vid"], "video", ctx["out"] / "video" / f"{bid}.mp4", ctx["dry"],
        )
        return {"id": bid, "esito": "completo", "immagine": img.get("file"), "video": vid.get("file")}
    except Fermata:
        raise
    except Exception as e:
        log(f"  [{bid}] FALLITO: {e}")
        return {"id": bid, "esito": "fallito", "errore": str(e)}


# ---------------------------------------------------------------------------- COMANDI

def cmd_stima(args):
    piano = json.loads(Path(args.piano).read_text())
    cat = json.loads(Path(args.catalogo).read_text())
    base, auth = cat["api"]["base_url"], credenziali()
    mi = modello(cat, piano["modelli"]["immagine"], "immagine")
    mv = modello(cat, piano["modelli"]["video"], "video")
    ratio = piano["aspect_ratio"]
    controlla_ratio(mi, ratio)

    tot_c, tot_u, righe = 0.0, 0.0, []
    for br in piano["broll"]:
        for etichetta, m, valori in (
            ("immagine", mi, {"prompt": br["prompt_t2i"], "aspect_ratio": ratio}),
            ("video", mv, {"prompt": br["prompt_i2v"], "immagine": "https://example.com/x.jpg",
                           "durata": br.get("durata", 5)}),
        ):
            if etichetta == "video" and args.solo_immagini:
                continue
            try:
                e = chiama(f"{base}/estimate/{m['endpoint']}", auth, corpo(m, valori))
                c, u = float(e.get("credits", 0)), float(e.get("usd", 0))
            except Exception as err:
                log(f"  stima non riuscita per {br['id']}/{etichetta}: {err}")
                c = float(m.get("crediti_indicativi") or 0)
                u = 0.0
            tot_c += c
            tot_u += u
            righe.append((br["id"], etichetta, c, u))

    for bid, et, c, u in righe:
        print(f"  {bid:<28} {et:<9} {c:>8.2f} crediti  {u:>7.3f} USD")
    print(f"\n  TOTALE {len(piano['broll'])} b-roll: {tot_c:.2f} crediti — {tot_u:.2f} USD")
    print("  (numeri dell'endpoint /estimate sul tuo account: sono quelli che verranno addebitati)")
    Path(args.out or ".").mkdir(parents=True, exist_ok=True)
    Path(args.out or ".", "stima.json").write_text(json.dumps(
        {"crediti": round(tot_c, 2), "usd": round(tot_u, 2),
         "voci": [{"id": b, "fase": e, "crediti": c, "usd": u} for b, e, c, u in righe]},
        indent=2, ensure_ascii=False))
    return 0


def cmd_genera(args):
    piano = json.loads(Path(args.piano).read_text())
    cat = json.loads(Path(args.catalogo).read_text())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    mi = modello(cat, piano["modelli"]["immagine"], "immagine")
    mv = modello(cat, piano["modelli"]["video"], "video")
    ratio = piano["aspect_ratio"]
    controlla_ratio(mi, ratio)
    for br in piano["broll"]:
        controlla_durata(mv, br.get("durata", 5))

    stato = Stato(out / "stato.json")
    for bid in (args.rigenera or []):
        stato.dimentica(bid)
        log(f"  [{bid}] stato azzerato: verra' rigenerato e RIPAGATO")

    broll = piano["broll"]
    if args.solo:
        broll = [b for b in broll if b["id"] in set(args.solo)]

    conc = args.concorrenza or cat["api"].get("concorrenza_massima", 3)
    log(f"Genero {len(broll)} b-roll — immagine: {mi['nome']} · video: {mv['nome']} · {ratio} · concorrenza {conc}")
    if args.dry_run:
        log("DRY-RUN: nessuna chiamata, nessun credito speso.")

    ctx = {
        "base": cat["api"]["base_url"], "auth": credenziali() if not args.dry_run else "dry",
        "stato": stato, "mi": mi, "mv": mv, "ratio": ratio, "out": out,
        "scad_img": args.scadenza_immagine, "scad_vid": args.scadenza_video,
        "solo_immagini": args.solo_immagini, "dry": args.dry_run,
    }
    with ThreadPoolExecutor(max_workers=conc) as pool:
        esiti = list(pool.map(lambda b: lavora(b, ctx), broll))

    falliti = [e for e in esiti if e["esito"] == "fallito"]
    manifesto = {
        "slug": piano.get("slug"), "aspect_ratio": ratio,
        "modelli": {"immagine": mi["nome"], "video": mv["nome"]},
        "generato_il": time.strftime("%Y-%m-%d %H:%M"),
        "broll": esiti,
    }
    (out / "manifest.json").write_text(json.dumps(manifesto, indent=2, ensure_ascii=False))
    log(f"\nCompletati {len(esiti) - len(falliti)}/{len(esiti)} — manifest in {out / 'manifest.json'}")
    if falliti:
        log("Falliti (rilancia lo stesso comando: riprende da qui senza ripagare il resto):")
        for f in falliti:
            log(f"  - {f['id']}: {f['errore']}")
    return 1 if falliti else 0


def cmd_credenziali(_):
    prima = bool(os.environ.get("HF_API_KEY_ID"))
    auth = credenziali()
    print("Credenziali trovate.")
    print(f"  origine: {'variabili d ambiente' if prima else ENV_FILE}")
    print(f"  chiave:  {auth.split(':')[0].replace('Key ', '')[:8]}… (il segreto non si stampa mai)")
    return 0


def main():
    p = argparse.ArgumentParser(description="Client Higgsfield per i B-roll Mobilitas")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("credenziali", help="verifica che le chiavi siano nell'ambiente").set_defaults(f=cmd_credenziali)

    def comuni(sp):
        sp.add_argument("--piano", required=True)
        sp.add_argument("--catalogo", required=True)

    s = sub.add_parser("stima", help="quanto costa questo piano, prima di spendere")
    comuni(s)
    s.add_argument("--out")
    s.add_argument("--solo-immagini", action="store_true")
    s.set_defaults(f=cmd_stima)

    g = sub.add_parser("genera", help="genera immagini e video del piano")
    comuni(g)
    g.add_argument("--out", required=True)
    g.add_argument("--concorrenza", type=int)
    g.add_argument("--solo-immagini", action="store_true", help="ferma prima dei video: si validano le scene a costo basso")
    g.add_argument("--solo", nargs="*", help="genera solo questi id")
    g.add_argument("--rigenera", nargs="*", help="azzera lo stato di questi id e li rifa' (RIPAGA)")
    g.add_argument("--scadenza-immagine", type=int, default=600)
    g.add_argument("--scadenza-video", type=int, default=1800)
    g.add_argument("--dry-run", action="store_true")
    g.set_defaults(f=cmd_genera)

    a = p.parse_args()
    try:
        return a.f(a)
    except Fermata as e:
        print(f"\nSTOP — {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

"""Animazioni anatomiche (fase 7b, 28/10/2026): disegni Servier Medical Art
adattati al brand, e le «foto» di sagoma per il telefono.

Regole in `brand.json` → `video.animazioni_anatomiche`:
- solo disegni di `libreria/anatomia/` (Servier, CC BY 4.0, licenza nel catalogo);
- il disegno si ricolora e si ritaglia, non si deforma; sopra si disegnano
  solo forme semplici (assi, frecce, linee, aloni), nel modello `anatomia`;
- niente anatomia generata dall'AI; si mostra solo quello che lui dice.

Il ricolore si fa al render: il file in libreria resta l'originale.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from .progetto import LIBRERIA

PANNA = (244, 244, 244)
CORPO = (40, 92, 160)
ATTRIBUZIONE = "Illustrazioni adattate da Servier Medical Art (smart.servier.com), CC BY 4.0"
# tappa 3: nelle card e nei pannelli stretti la versione lunga non entra in una riga leggibile
ATTRIBUZIONE_BREVE = "Adattato da Servier Medical Art, CC BY 4.0"


def ricolora(nome, alto, taglio=None, sfuma=140, ritaglio=None, modo='ossa', sfuma_bordi=0):
    """libreria/anatomia/<nome> -> RGBA nel brand, alto `alto` px (riferito al disegno
    intero, prima del taglio). Ossa panna, contorni panna 85%, corpo blu velato.
    `taglio`: riga del disegno originale dove si ferma (la figura «Adult» cammina:
    si inquadra fino a meta coscia), con una dissolvenza di `sfuma` px originali.
    Torna (immagine, scala) con scala = px resi per px originali."""
    src = LIBRERIA / 'anatomia' / nome
    if not src.exists():
        raise SystemExit(f"anatomia: {src} non c'e (solo disegni di libreria/anatomia, con licenza nel catalogo)")
    im = Image.open(src).convert('RGBA')
    if ritaglio:
        # una parte del disegno (fase 7b rivista: card con il bacino, la colonna...):
        # [x0, y0, x1, y1] in pixel ORIGINALI; `alto` e l'altezza resa del ritaglio
        im = im.crop(tuple(int(v) for v in ritaglio))
    s = alto / im.height
    im = im.resize((max(1, int(round(im.width * s))), int(alto)), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    osso = (r > 0.75) & (g > 0.62) & (b < 0.78) & (r - b > 0.12)
    linea = (lum < 0.62) & ~osso
    out = np.zeros_like(a)
    out[..., :3] = np.array(CORPO) / 255
    out[..., 3] = al * 0.55
    oc = np.array(PANNA) / 255 * (0.82 + 0.18 * lum[..., None])
    out[osso, :3] = oc[osso]
    out[osso, 3] = al[osso] * 0.96
    out[linea, :3] = np.array(PANNA) / 255
    out[linea, 3] = al[linea] * 0.85
    if modo == 'muscoli':
        # tavole dei muscoli (rosso/rosa): i ventri muscolari diventano blu con il
        # loro chiaroscuro, i tendini e le fasce (chiari) panna velata: le forme si
        # leggono, nessun colore fuori dal brand
        rosso = (r - b > 0.18) & ~linea
        sh = np.clip((lum - 0.25) / 0.6, 0, 1)[..., None]
        blu_s, blu_c = np.array([22, 60, 120]) / 255, np.array([86, 140, 205]) / 255
        out[rosso, :3] = (blu_s + (blu_c - blu_s) * sh)[rosso]
        out[rosso, 3] = al[rosso] * 0.92
        chiaro = (lum > 0.80) & ~rosso & ~linea & (al > 0.5)
        out[chiaro, :3] = np.array(PANNA) / 255 * 0.9
        out[chiaro, 3] = al[chiaro] * 0.75
    if sfuma_bordi:
        # taglio voluto (fase 7b rivista): il ritaglio sfuma in alto e in basso
        f = max(1, int(sfuma_bordi * s))
        r_ = np.linspace(0, 1, f, dtype=np.float32)[:, None]
        out[:f, :, 3] *= r_
        out[-f:, :, 3] *= r_[::-1]
    if taglio:
        y = int(taglio * s)
        out = out[:y].copy()
        f = max(1, int(sfuma * s))
        out[y - f:, :, 3] *= np.linspace(1, 0, f, dtype=np.float32)[:, None]
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)), s


# ------------------------------------------------------------------ sagoma posturale
# Profilo di una figura in piedi che guarda a destra (unita: 0-300 x 0-800).
# Forme semplici, non anatomia: lo schema del concetto, non un paziente.
# Ogni punto ha due posizioni: pancia in dentro (0) e pancia in avanti (1);
# cambiano solo i punti dell'addome: il bacino e la schiena restano dove sono.
TESTA = (150, 62, 48)                    # cx, cy, r
NASO = [(192, 52), (212, 72), (192, 80)]
PROFILO = [  # (x0, y, x1): x con la pancia dentro, y, x con la pancia in avanti
    (130, 112, 130), (120, 150, 120), (112, 200, 112), (114, 260, 114), (128, 320, 128), (124, 370, 124),
    (104, 420, 104), (100, 462, 100), (114, 502, 114), (124, 560, 124), (130, 640, 130), (124, 700, 124),
    (130, 762, 130), (128, 792, 128), (134, 802, 134), (222, 802, 222), (214, 784, 214), (176, 772, 176),
    (166, 760, 166), (160, 700, 160), (168, 640, 168), (178, 560, 178), (182, 500, 182), (186, 468, 206),
    (190, 430, 238), (190, 392, 246), (188, 352, 228), (186, 318, 200), (194, 280, 194), (202, 232, 202),
    (194, 176, 194), (170, 142, 170), (162, 112, 162)]
BRACCIO = [(146, 168), (152, 296), (164, 418)]
LINEA_BACINO = ((92, 452), (186, 430))    # asse del bacino, inclinato in avanti: resta fermo


def profilo(pancia):
    return [(x0 + (x1 - x0) * pancia, y) for x0, y, x1 in PROFILO]


def liscia(pts, passi=8):
    """Catmull-Rom chiusa -> polilinea morbida"""
    out, n = [], len(pts)
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        for k in range(passi):
            t = k / passi
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out


def _sagoma(d, x0, y0, k, colore, pancia=1.0):
    P = lambda x, y: (x0 + x * k, y0 + y * k)
    cx, cy, r = TESTA
    d.ellipse([*P(cx - r, cy - r), *P(cx + r, cy + r)], fill=colore)
    d.polygon([P(*q) for q in NASO], fill=colore)
    d.polygon([P(*q) for q in liscia(profilo(pancia))], fill=colore)
    chiaro = tuple(min(255, c + 34) for c in colore)
    d.line([P(*q) for q in BRACCIO], fill=chiaro, width=int(34 * k), joint='curve')
    for q in (BRACCIO[0], BRACCIO[-1]):
        c = P(*q)
        d.ellipse([c[0] - 17 * k, c[1] - 17 * k, c[0] + 17 * k, c[1] + 17 * k], fill=chiaro)


# ------------------------------------------------------------------ foto di sagoma (telefono)
def foto_sagoma(dst, anelli=False, w=600, h=1200):
    """la «foto di lato» per il telefono: schermo chiaro con la sagoma, nessuna
    persona vera. Con `anelli` due cerchi menta dove «l'occhio va subito lì»:
    la pancia che sporge e la schiena inarcata."""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 70, fill=(12, 16, 24, 255))
    d.rounded_rectangle([18, 18, w - 19, h - 19], 56, fill=(0, 30, 68, 255))     # schermo blu: il verde solo sul blu
    d.rounded_rectangle([w // 2 - 70, 34, w // 2 + 70, 62], 14, fill=(12, 16, 24, 255))
    k = 1.2
    x0, y0 = w / 2 - 165 * k, 150
    _sagoma(d, x0, y0, k, (200, 214, 232), pancia=1.0)
    if anelli:
        P = lambda x, y: (x0 + x * k, y0 + y * k)
        for cx, cy, rx, ry in ((228, 395, 70, 92), (110, 360, 52, 80)):
            c = P(cx, cy)
            d.ellipse([c[0] - rx, c[1] - ry, c[0] + rx, c[1] + ry], outline=(114, 250, 147, 255), width=12)
    im.save(dst)
    return dst

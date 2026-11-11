"""Colore: da quello che esce dalla camera all'SDR BT.709 del canale.

Questo ffmpeg non ha `zscale` ne `libplacebo`, e il filtro `colorspace` non
conosce la curva HLG (`arib-std-b67`): l'HLG non si linearizza con i filtri.
La conversione si precalcola come LUT 3D, una volta per tutte (non dipende dal
video, dipende dalla camera).

Catena, per ogni nodo del cubo:
  1. inverse-OETF HLG  -> luce di scena normalizzata
  2. OOTF (gamma 1.2)  -> luce di display HDR
  3. normalizzazione su HLG 0.75 = bianco di riferimento (100 nit)
  4. tone map Hable    -> comprime cio che sta sopra il bianco
  5. matrice BT.2020 -> BT.709 + desaturazione dei fuori-gamut
  6. OETF BT.1886 (gamma 1/2.4) -> segnale SDR
"""
import numpy as np

from .progetto import CACHE

N = 65
A, B, C = 0.17883277, 0.28466892, 0.55991073
LUMA_2020 = np.array([0.2627, 0.6780, 0.0593])
M_2020_709 = np.array([
    [1.6605, -0.5876, -0.0728],
    [-0.1246, 1.1329, -0.0083],
    [-0.0182, -0.1006, 1.1187],
])

# i flag -color_* da soli non bastano: i frame filtrati si portano dietro i
# metadati d'ingresso e il file uscirebbe taggato arib-std-b67/bt2020
TAG_709 = "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"


def _hlg_inv(e):
    return np.where(e <= 0.5, (e * e) / 3.0, (np.exp((e - C) / A) + B) / 12.0)


def _hable(x):
    a, b, c, d, e, f = 0.15, 0.50, 0.10, 0.20, 0.02, 0.30
    return ((x * (a * x + c * b) + d * e) / (x * (a * x + b) + d * f)) - e / f


def lut_hlg():
    path = CACHE / 'hlg2020-to-bt709-65.cube'
    if path.exists():
        return path
    CACHE.mkdir(exist_ok=True)
    grid = np.linspace(0.0, 1.0, N)
    r, g, b = np.meshgrid(grid, grid, grid, indexing="ij")
    rgb = np.stack([b, g, r], axis=-1).reshape(-1, 3)      # .cube: il rosso varia piu in fretta
    scene = _hlg_inv(rgb)
    y = np.clip(scene @ LUMA_2020, 1e-6, None)[:, None]
    disp = scene * np.power(y, 0.2)
    ref_scene = _hlg_inv(np.array(0.75))
    disp = disp / (ref_scene * ref_scene ** 0.2)
    peak = max(disp.max(), 1.0)
    disp = _hable(disp) / _hable(np.array(peak))
    lin = disp @ M_2020_709.T
    ylin = np.clip(lin @ np.array([0.2126, 0.7152, 0.0722]), 0.0, None)[:, None]
    over = np.clip(-lin.min(axis=1), 0.0, None)[:, None]
    k = over / np.clip(ylin + over, 1e-6, None)
    lin = np.clip(lin * (1.0 - k) + ylin * k, 0.0, 1.0)
    out = np.power(lin, 1.0 / 2.4)
    tmp = str(path) + '.tmp'
    with open(tmp, 'w') as fh:
        fh.write(f"# HLG BT.2020 -> SDR BT.709\nLUT_3D_SIZE {N}\n")
        fh.write("DOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n")
        np.savetxt(fh, out, fmt='%.6f')
    import os
    os.replace(tmp, path)
    return path


def catena(meta):
    """filtri colore da inserire DOPO il ridimensionamento (costa meno su 1080p)"""
    if meta['colore'] == 'hlg':
        return f"format=gbrp16le,lut3d=file={lut_hlg()}:interp=tetrahedral"
    if meta['colore'] == 'pq':
        raise SystemExit("sorgente PQ/HDR10: non gestita, serve un LUT dedicato")
    return ""


def filtro_finale():
    return f"format=yuv420p,{TAG_709}"

#!/usr/bin/env python3
"""Genera un 3D LUT (.cube) HLG BT.2020 -> SDR BT.709.

Catena, per ogni nodo del cubo:
  1. inverse-OETF HLG  -> luce di scena normalizzata
  2. OOTF (gamma 1.2)  -> luce di display HDR
  3. normalizzazione su HLG 0.75 = bianco di riferimento (100 nit)
  4. tone map Hable    -> comprime cio che sta sopra il bianco
  5. matrice BT.2020 -> BT.709 + desaturazione dei fuori-gamut
  6. OETF BT.1886 (gamma 1/2.4) -> segnale SDR
"""
import numpy as np

N = 65  # nodi per lato

A, B, C = 0.17883277, 0.28466892, 0.55991073


def hlg_inverse_oetf(e):
    """segnale HLG [0,1] -> luce di scena [0,1]"""
    return np.where(e <= 0.5, (e * e) / 3.0, (np.exp((e - C) / A) + B) / 12.0)


# luminanza BT.2020
LUMA_2020 = np.array([0.2627, 0.6780, 0.0593])

# BT.2020 -> BT.709 (lineare, D65)
M_2020_709 = np.array([
    [1.6605, -0.5876, -0.0728],
    [-0.1246, 1.1329, -0.0083],
    [-0.0182, -0.1006, 1.1187],
])


def hable(x):
    a, b, c, d, e, f = 0.15, 0.50, 0.10, 0.20, 0.02, 0.30
    return ((x * (a * x + c * b) + d * e) / (x * (a * x + b) + d * f)) - e / f


def main():
    grid = np.linspace(0.0, 1.0, N)
    r, g, b = np.meshgrid(grid, grid, grid, indexing="ij")
    # ordine .cube: red varia piu velocemente
    rgb = np.stack([b, g, r], axis=-1).reshape(-1, 3)

    # 1. HLG -> scena
    scene = hlg_inverse_oetf(rgb)

    # 2. OOTF: display = Y^(gamma-1) * scene, gamma di sistema 1.2
    y = np.clip(scene @ LUMA_2020, 1e-6, None)[:, None]
    disp = scene * np.power(y, 0.2)

    # 3. bianco di riferimento: HLG 0.75 (dopo OOTF) -> 1.0
    ref_scene = hlg_inverse_oetf(np.array(0.75))
    ref = ref_scene * (ref_scene ** 0.2)
    disp = disp / ref

    # 4. tone map su cio che eccede il bianco
    peak = disp.max() if disp.max() > 1.0 else 1.0
    disp = hable(disp) / hable(np.array(peak))

    # 5. gamut BT.2020 -> BT.709, i negativi rientrano desaturando verso il grigio
    lin = disp @ M_2020_709.T
    ylin = np.clip(lin @ np.array([0.2126, 0.7152, 0.0722]), 0.0, None)[:, None]
    over = np.clip(-lin.min(axis=1), 0.0, None)[:, None]
    k = over / np.clip(ylin + over, 1e-6, None)
    lin = lin * (1.0 - k) + ylin * k
    lin = np.clip(lin, 0.0, 1.0)

    # 6. OETF BT.1886
    out = np.power(lin, 1.0 / 2.4)

    path = "assets/hlg2020-to-bt709.cube"
    with open(path, "w") as fh:
        fh.write("# HLG BT.2020 -> SDR BT.709 (YT_TOFU_02)\n")
        fh.write(f"LUT_3D_SIZE {N}\n")
        fh.write("DOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n")
        for px in out:
            fh.write(f"{px[0]:.6f} {px[1]:.6f} {px[2]:.6f}\n")
    print(f"scritto {path}  ({N}^3 = {N**3} nodi)")


if __name__ == "__main__":
    main()

"""Odečet křivek z podkladového grafu Portfolio 10 vs. WOOD (Datawrapper, výřez 1416 × 786 px) do CSV.

Kalibrace podle mřížky a popisků v obrázku:
  osa y: 0 % = y 742 px, 70 % = y 53,5 px (mřížka po 10 % á 98,4 px → 1 px ≈ 0,1 p. b.)
  osa x: 1. 1. 2024 = x 299 px, 1. 1. 2026 = x 992,5 px (≈ 0,95 px na den)
  koncové tečky (x ≈ 1262 px) a počáteční tečka (x ≈ 96 px) se neodečítají – hodnoty z popisků
  v obrázku: start 0,0 % u obou, konec 68,9 % (Portfolio 10) a 28,0 % (WOOD).
Postup: v každém sloupci pixelů úsek čáry navazující na předchozí sloupec; bod = střed čáry,
u lokálního vrcholu/dna krajní okraj čáry (aby se neztratily špičky).
Spouštěj z kořene repozitáře:
  python3 vystupy/grafy/2026-10-16-portu10-vs-wood-odecet.py podklady/grafy/2026-10-16-portu10-vs-wood-podklad.png vystupy/grafy/2026-10-16-portu10-vs-wood.csv
"""
import csv
import datetime as dt
import sys

from PIL import Image

im = Image.open(sys.argv[1]).convert("RGB")
X_2024, X_2026 = 299.0, 992.5
D_2024 = dt.datetime(2024, 1, 1)
PX_NA_DEN = (X_2026 - X_2024) / (dt.datetime(2026, 1, 1) - D_2024).days
Y_0, Y_70 = 742.0, 53.5
X_START, X_KONEC = 96.0, 1262.0          # středy počáteční a koncových teček
X_OD, X_DO = 106, 1249                   # odečítaný úsek (mimo tečky)
KONCE = {"portu_10": 68.9, "wood_opf": 28.0}
BARVY = {"portu_10": (0x00, 0x52, 0x7A), "wood_opf": (0x18, 0xA1, 0xCD)}
TL = 4  # tloušťka čáry v px


def hodnota(y):
    return (Y_0 - y) / (Y_0 - Y_70) * 70


def datum(x):
    return D_2024 + dt.timedelta(days=(x - X_2024) / PX_NA_DEN)


def blizko(p, c, tolerance=110):
    return sum(abs(a - b) for a, b in zip(p, c)) < tolerance


def odecti(barva):
    sloupce, prev = [], None
    for x in range(X_OD, X_DO + 1):
        ys = [y for y in range(0, 760) if blizko(im.getpixel((x, y)), barva)]
        if not ys:
            continue
        useky, s, p = [], ys[0], ys[0]
        for y in ys[1:]:
            if y - p > 6:  # mezery do 6 px = stále tatáž čára (ostré špičky)
                useky.append((s, p))
                s = y
            p = y
        useky.append((s, p))
        s, p = min(useky, key=lambda u: abs((u[0] + u[1]) / 2 - prev)) if prev is not None else useky[-1]
        sloupce.append((x, s, p))
        prev = (s + p) / 2
    body = []
    for i, (x, s, p) in enumerate(sloupce):
        y = (s + p) / 2
        if 0 < i < len(sloupce) - 1 and p - s > 2 * TL:
            (_, s1, p1), (_, s2, p2) = sloupce[i - 1], sloupce[i + 1]
            if s <= s1 and s <= s2 and (s < s1 or s < s2):
                y = s + TL / 2  # vrchol
            elif p >= p1 and p >= p2 and (p > p1 or p > p2):
                y = p - TL / 2  # dno
        body.append((x, hodnota(y)))
    return body


with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["datum", "rada", "hodnota_pct"])
    for rada, barva in BARVY.items():
        body = [(X_START, 0.0)] + odecti(barva) + [(X_KONEC, KONCE[rada])]
        for x, v in body:
            w.writerow([datum(x).strftime("%Y-%m-%d %H:%M"), rada, round(v, 2)])
        hodnoty = [v for _, v in body]
        print(rada, "bodů", len(body), "| od", datum(body[0][0]).date(), "do", datum(body[-1][0]).date(),
              "| min", round(min(hodnoty), 1), "max", round(max(hodnoty), 1),
              "| předposlední", round(body[-2][1], 1))

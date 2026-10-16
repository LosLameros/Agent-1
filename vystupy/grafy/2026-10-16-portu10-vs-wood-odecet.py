"""Odečet křivek z podkladového grafu Portfolio 10 vs. WOOD (Datawrapper, výřez 1354 × 768 px) do CSV.

Kalibrace podle mřížky a popisků v obrázku:
  osa y: 0 % = y 735 px, 70 % = y 70 px (mřížka po 10 % á 95 px → 1 px ≈ 0,105 p. b.)
  osa x: 1. 1. 2024 = x 301,5 px, 1. 1. 2026 = x 973,5 px (≈ 0,92 px na den)
  počáteční tečka (x ≈ 106,5 px) a koncové tečky (x ≈ 1238 px) se neodečítají – hodnoty z popisků:
  start 0,0 %, konec 68,9 % (Portfolio 10) a 28,0 % (WOOD).
Postup:
  WOOD (schodovitý vývoj): v každém sloupci pixelů střed vodorovné čáry; sloupce se svislou hranou
  skoku se vynechají a graf řadu kreslí schodovitě → skoky jsou svislé, rovné úseky rovné.
  Portfolio 10: v každém sloupci pixelů střed čáry (přesný u šikmých úseků), u lokálního vrcholu/dna
  krajní okraj čáry, u velkých pohybů (úsek > 3× tloušťka čáry) vstupní a výstupní bod – prudké
  propady a růsty tak zůstanou svislé.
  Nakonec zjednodušení Ramer–Douglas–Peucker (tolerance 0,5 px) – tvar stejný, bez nadbytečných bodů.
Spouštěj z kořene repozitáře:
  python3 vystupy/grafy/2026-10-16-portu10-vs-wood-odecet.py podklady/grafy/2026-10-16-portu10-vs-wood-podklad.png vystupy/grafy/2026-10-16-portu10-vs-wood.csv [kontrola.png]
"""
import csv
import datetime as dt
import sys

from PIL import Image, ImageDraw

im = Image.open(sys.argv[1]).convert("RGB")
X_2024, X_2026 = 301.5, 973.5
D_2024 = dt.datetime(2024, 1, 1)
PX_NA_DEN = (X_2026 - X_2024) / (dt.datetime(2026, 1, 1) - D_2024).days
Y_0, Y_70 = 735.0, 70.0
X_START, X_KONEC = 106.5, 1238.0
X_OD, X_DO = 116, 1228
KONCE = {"portu_10": (68.9, 80.0), "wood_opf": (28.0, 469.0)}   # hodnota a y středu koncové tečky
BARVY = {"portu_10": (0x00, 0x52, 0x7A), "wood_opf": (0x18, 0xA1, 0xCD)}
TL = 4.5      # tloušťka čáry v px
POLOVINA = TL / 2


def hodnota(y):
    return (Y_0 - y) / (Y_0 - Y_70) * 70


def datum(x):
    return D_2024 + dt.timedelta(days=(x - X_2024) / PX_NA_DEN)


def useky(x, barva):
    ys = [y for y in range(0, 745) if sum(abs(a - b) for a, b in zip(im.getpixel((x, y)), barva)) < 110]
    out = []
    if ys:
        s = p = ys[0]
        for y in ys[1:]:
            if y - p > 6:  # mezery do 6 px = stále tatáž čára
                out.append((s, p))
                s = y
            p = y
        out.append((s, p))
    return out


def sloupce(barva):
    """Pro každý sloupec úsek čáry navazující na předchozí sloupec: {x: (horní, dolní)}."""
    vysledek, stred = {}, None
    for x in range(X_OD, X_DO + 1):
        u = useky(x, barva)
        if not u:
            continue
        s, p = min(u, key=lambda a: abs((a[0] + a[1]) / 2 - stred)) if stred is not None else u[-1]
        if stred is not None and abs((s + p) / 2 - stred) > 60 and len(u) == 1 and p - s < 2 * TL:
            continue  # osamocený kus jiné čáry
        vysledek[x] = (s, p)
        stred = (s + p) / 2
    return vysledek


def wood(barva):
    body = []
    for x, (s, p) in sorted(sloupce(barva).items()):
        if p - s <= TL + 2:  # jen vodorovná čára, svislé hrany skoků vynechat
            y = (s + p) / 2
            if body and x - body[-1][0] > 1 and abs(y - body[-1][1]) > 1:
                body.append(((body[-1][0] + x) / 2, y))  # skok doprostřed vynechané svislé hrany
            body.append((x, y))
    return body


def tah_pera(barva, tloustka=5.0):
    """Střed čáry v každém sloupci; u vrcholu/dna krajní okraj; u velkého pohybu (úsek > 3× tloušťka)
    vstupní a výstupní bod, aby prudké propady a růsty zůstaly svislé."""
    sl = sloupce(barva)
    xs = sorted(sl)
    stredy = {x: (sl[x][0] + sl[x][1]) / 2 for x in xs}
    pul = tloustka / 2
    body = []
    for i, x in enumerate(xs):
        s, p = sl[x]
        y_pred = stredy[xs[i - 1]] if i > 0 else None
        y_dal = stredy[xs[i + 1]] if i + 1 < len(xs) else None
        if p - s > 3 * tloustka and y_pred is not None and y_dal is not None:
            horni, dolni = s + pul, p - pul
            vstup = horni if abs(y_pred - horni) < abs(y_pred - dolni) else dolni
            vyst = horni if abs(y_dal - horni) < abs(y_dal - dolni) else dolni
            if vstup == vyst:  # špička: vstup → opačný kraj → zpět
                body += [(x - 0.33, vstup), (x, dolni if vstup == horni else horni), (x + 0.33, vyst)]
            else:
                body += [(x - 0.25, vstup), (x + 0.25, vyst)]
            continue
        y = stredy[x]
        if y_pred is not None and y_dal is not None and p - s > tloustka + 2:
            s1, p1 = sl[xs[i - 1]]
            s2, p2 = sl[xs[i + 1]]
            if s <= s1 and s <= s2 and (s < s1 or s < s2):
                y = s + pul  # vrchol
            elif p >= p1 and p >= p2 and (p > p1 or p > p2):
                y = p - pul  # dno
        body.append((x, y))
    return body


def zjednodus(body, tolerance=0.5):
    """Ramer–Douglas–Peucker: vynechá body, které od výsledné čáry neodchýlí víc než tolerance (px)."""
    if len(body) < 3:
        return body
    (x1, y1), (x2, y2) = body[0], body[-1]
    dx, dy = x2 - x1, y2 - y1
    delka = (dx * dx + dy * dy) ** 0.5 or 1.0
    vzdalenosti = [abs(dy * x - dx * y + x2 * y1 - y2 * x1) / delka for x, y in body[1:-1]]
    i = max(range(len(vzdalenosti)), key=vzdalenosti.__getitem__)
    if vzdalenosti[i] <= tolerance:
        return [body[0], body[-1]]
    return zjednodus(body[: i + 2], tolerance)[:-1] + zjednodus(body[i + 1:], tolerance)


sys.setrecursionlimit(10000)
vystupy = {"portu_10": zjednodus(tah_pera(BARVY["portu_10"])), "wood_opf": wood(BARVY["wood_opf"])}
with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["datum", "rada", "hodnota_pct"])
    for rada, body in vystupy.items():
        konec, y_konec = KONCE[rada]
        cela = [(X_START, Y_0)] + body + [(X_KONEC, y_konec)]
        for x, y in cela:
            v = 0.0 if x == X_START else konec if x == X_KONEC else hodnota(y)
            w.writerow([datum(x).strftime("%Y-%m-%d %H:%M:%S"), rada, round(v, 2)])
        hodnoty = [hodnota(y) for _, y in body]
        print(rada, "bodů", len(cela), "| min", round(min(hodnoty), 2), "max", round(max(hodnoty), 2))

if len(sys.argv) > 3:  # kontrolní obrázek: odečtené body červeně přes podklad
    kontrola = im.copy()
    d = ImageDraw.Draw(kontrola)
    for rada, body in vystupy.items():
        if rada == "wood_opf":  # schodovitě
            schody = []
            for (x1, y1), (x2, _) in zip(body, body[1:]):
                schody += [(x1, y1), (x2, y1)]
            body = schody
        d.line(body, fill=(230, 0, 0), width=1)
    kontrola.save(sys.argv[3])

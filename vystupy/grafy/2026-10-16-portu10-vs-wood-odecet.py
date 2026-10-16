"""Odečet křivek z podkladového grafu Portfolio 10 vs. WOOD (Datawrapper, výřez 1354 × 768 px) do CSV.

Kalibrace podle mřížky a popisků v obrázku:
  osa y: 0 % = y 735 px, 70 % = y 70 px (mřížka po 10 % á 95 px → 1 px ≈ 0,105 p. b.)
  osa x: 1. 1. 2024 = x 301,5 px, 1. 1. 2026 = x 973,5 px (≈ 0,92 px na den)
  počáteční tečka (x ≈ 106,5 px) a koncové tečky (x ≈ 1238 px) se neodečítají – hodnoty z popisků:
  start 0,0 %, konec 68,9 % (Portfolio 10) a 28,0 % (WOOD).
Postup:
  WOOD (schodovitý vývoj): v každém sloupci pixelů střed vodorovné čáry; sloupce se svislou hranou
  skoku se vynechají a graf řadu kreslí schodovitě → skoky jsou svislé, rovné úseky rovné.
  Portfolio 10: v každém sloupci pixelů bod, při kterém čára o skutečné tloušťce (4,2 px) pokryje
  přesně ten úsek, který pokrývá v podkladu (okraje s přesností na zlomky pixelu); body se dolaďují
  opakovaně se sousedy, takže sedí šikmé úseky, ostré špičky i prudké propady. Nakonec se každý bod
  doladí přímo podle vykreslení: zkusí se polohy ±3 px po 0,25 px a zůstane ta, při které se vykreslená
  čára odstínem pixelů nejvíc shoduje s podkladem.
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
HLADKOST = 0.0  # vyzkoušeno 0–0,4: každé vyhlazení překryv s podkladem zhoršuje
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


def pokryti(barva):
    """Pro každý pixel podíl, jak moc ho zakrývá čára dané barvy (0–1), z vyhlazených okrajů."""
    br, bg, bb = barva
    wr, wg, wb = 255 - br, 255 - bg, 255 - bb
    norma = wr * wr + wg * wg + wb * wb

    def a(p):
        r, g, b = p
        dr, dg, db = 255 - r, 255 - g, 255 - b
        # jen pixely v odstínu dané čáry (ne šedá mřížka, ne druhá čára)
        if abs(dr * wg - dg * wr) + abs(dg * wb - db * wg) > 0.25 * norma:
            return 0.0
        return max(0.0, min(1.0, (dr * wr + dg * wg + db * wb) / norma))
    return a


def tah_pera(barva, tloustka=4.2, pruchody=8, hladkost=HLADKOST):
    """Střed čáry v každém sloupci pixelů tak, aby čára o skutečné tloušťce pokryla v daném sloupci
    přesně ten svislý úsek, který pokrývá v podkladu (horní a dolní okraj s přesností na zlomky pixelu).
    V každém sloupci prochází čára od poloviny cesty k předchozímu bodu přes svůj bod k polovině cesty
    k dalšímu bodu; body se dolaďují opakovaně, protože každý ovlivňuje i sousední sloupce."""
    a = pokryti(barva)
    sl = sloupce(barva)
    xs = sorted(sl)
    okraje = []
    for x in xs:
        s, p = sl[x]
        sloupec = [(y, a(im.getpixel((x, y)))) for y in range(s - 2, p + 3)]
        nad = [y for y, v in sloupec if v >= 0.5] or [s, p]
        horni = nad[0] - 0.5 + (1 - a(im.getpixel((x, nad[0] - 1)))) * 0.5
        dolni = nad[-1] + 0.5 - (1 - a(im.getpixel((x, nad[-1] + 1)))) * 0.5
        okraje.append((horni, dolni))
    pul = tloustka / 2
    y = [(h + d) / 2 for h, d in okraje]
    n = len(y)

    def predpoved(i):
        m1 = (y[i - 1] + y[i]) / 2 if i > 0 else y[i]
        m2 = (y[i] + y[i + 1]) / 2 if i < n - 1 else y[i]
        sklon = abs(m2 - m1)
        h = pul * min((1 + sklon * sklon) ** 0.5, 2.0)
        return min(m1, y[i], m2) - h, max(m1, y[i], m2) + h

    def chyba(i):
        e = 0.0
        for j in (i - 1, i, i + 1):
            if 0 <= j < n:
                h, d = predpoved(j)
                e += (h - okraje[j][0]) ** 2 + (d - okraje[j][1]) ** 2
                if 0 < j < n - 1:  # mírná penalizace kmitání: ze stejně dobrých řešení vyhraje rovnější čára
                    e += hladkost * (y[j] - (y[j - 1] + y[j + 1]) / 2) ** 2
        return e

    for _ in range(pruchody):
        for i in range(n):
            horni, dolni = okraje[i]
            nejlepsi, nejmensi = y[i], chyba(i)
            kandidat = horni - 1
            while kandidat <= dolni + 1:
                y[i] = kandidat
                e = chyba(i)
                if e < nejmensi:
                    nejlepsi, nejmensi = kandidat, e
                kandidat += 0.25
            y[i] = nejlepsi
    return list(zip(xs, y))


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
def dolad_vykreslenim(body, barva, sirka=4.2, pruchody=4, rozsah=3.0, krok=0.25, nasobek=8):
    """Každý bod doladí přímo podle vykreslení: v okolí ±rozsah px zkusí polohy po krok px, vykreslí
    okolní kus čáry (vyhlazeně, nasobek× zvětšený a zmenšený) a nechá polohu s nejmenším rozdílem
    odstínu proti podkladu."""
    import numpy as np
    a = pokryti(barva)
    w, h = im.size
    podklad = np.array([[a(im.getpixel((x, y))) for x in range(w)] for y in range(h)], dtype=np.float32)
    xs = [x for x, _ in body]
    ys = [y for _, y in body]
    n = len(body)
    sirka_px = int(round(sirka * nasobek))
    for _ in range(pruchody):
        for i in range(n):
            j0, j1 = max(0, i - 5), min(n, i + 6)
            x0, x1 = int(xs[max(0, i - 3)]) - 1, int(xs[min(n - 1, i + 3)]) + 2
            okno_y = ys[j0:j1]
            y0 = int(min(okno_y) - rozsah - sirka - 2)
            y1 = int(max(okno_y) + rozsah + sirka + 3)
            cil = podklad[y0:y1, x0:x1]
            puvodni = ys[i]
            nejlepsi, nejmensi = puvodni, None
            kandidat = puvodni - rozsah
            while kandidat <= puvodni + rozsah + 1e-9:
                ys[i] = kandidat
                obr = Image.new("L", ((x1 - x0) * nasobek, (y1 - y0) * nasobek), 0)
                ImageDraw.Draw(obr).line([((xs[j] - x0 + 0.5) * nasobek, (ys[j] - y0 + 0.5) * nasobek) for j in range(j0, j1)],
                                         fill=255, width=sirka_px, joint="curve")
                vykres = np.asarray(obr.resize((x1 - x0, y1 - y0), Image.BOX), dtype=np.float32) / 255
                e = float(np.abs(vykres - cil).sum())
                if nejmensi is None or e < nejmensi:
                    nejlepsi, nejmensi = kandidat, e
                kandidat += krok
            ys[i] = nejlepsi
    return list(zip(xs, ys))


vystupy = {"portu_10": dolad_vykreslenim(tah_pera(BARVY["portu_10"]), BARVY["portu_10"]),
           "wood_opf": wood(BARVY["wood_opf"])}
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

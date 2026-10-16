"""Výhled světové ekonomiky: projekce růstu – tabulka v Portu vzhledu.

Data: Mezinárodní měnový fond, World Economic Outlook (říjen 2026), převzato z podkladové
tabulky; světové hodnoty (3,5 / 3,1 / 3,4 %) potvrzují zprávy o říjnovém WEO.
Vzhled: oficiální barvy Portu fialová #4840BB a zelená #00AA3C (+ jejich tmavší a světlé
odstíny pro buňky projekcí), písmo Rethink Sans (pevné řezy v nastroje/fonty/).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-vyhled-mmf-tabulka.py
"""
import csv
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-16-vyhled-mmf-tabulka"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
MEDIUM = font_manager.FontProperties(fname=F + "-Medium.ttf")
SEMIBOLD = font_manager.FontProperties(fname=F + "-SemiBold.ttf")
BOLD = font_manager.FontProperties(fname=F + "-Bold.ttf")

FIALOVA, ZELENA = pg.FIALOVA, pg.ZELENA
FIALOVA_TMAVA = "#3A33A0"   # buňky projekcí v řádcích skupin
ZELENA_TMAVA = "#008C32"    # buňky projekcí v řádku světa (odstín z brand manuálu Portu)
ZELENA_SVETLA = "#EBF8EF"   # sloupce projekcí – lichý řádek
ZELENA_PRUH = "#DDF2E4"     # sloupce projekcí – sudý (pruhovaný) řádek
SEDA_PRUH = "#F4F4F7"
CARA = "#E7E7EB"
TEXT = "#202020"
ZAPORNA = "#BE0000"

W, DPI = 1100, 200
PT = DPI / 72

radky = []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        radky.append((r["oblast"], r["typ"], [float(r[k]) for k in ("2025", "2026", "2027")]))

# výška: hlavička 250, řádky světa/skupin 74, ostatní 56, patička 120
H = 250 + sum(74 if t in ("svet", "skupina") else 56 for _, t, _ in radky) + 130
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


L, P = 30, 1070
SLOUPCE = [600, 770, 920, P]  # hranice sloupců 2025 | 2026 | 2027
STREDY = [(a + b) / 2 for a, b in zip(SLOUPCE, SLOUPCE[1:])]

# nadpis, akcent, podtitulek
text(L, 62, "Výhled světové ekonomiky: projekce růstu", 40, pg.TEXT_TMAVY, REGULAR, va="baseline")
ax.add_patch(FancyBboxPatch((L, 82), 110, 9, boxstyle="round,pad=0,rounding_size=4.5", facecolor=ZELENA, edgecolor="none"))
text(L, 132, "(Reálné HDP, meziroční změna v %)", 24, FIALOVA, MEDIUM, va="baseline")

# hlavička tabulky
text((SLOUPCE[1] + SLOUPCE[3]) / 2, 180, "PROJEKCE", 20, ZELENA, BOLD, ha="center", va="baseline")
ax.add_patch(Rectangle((SLOUPCE[1], 194), SLOUPCE[3] - SLOUPCE[1], 52, facecolor=ZELENA_SVETLA, edgecolor="none"))
for stred, rok in zip(STREDY, ("2025", "2026", "2027")):
    text(stred, 230, rok, 26, TEXT, BOLD, ha="center", va="baseline")
ax.plot([L, P], [247, 247], color=pg.TEXT_TMAVY, linewidth=2.5 / PT * 72 / 72)


def hodnota(v):
    return pg.cislo(v, 1, "")


y = 250
pruh = False
for nazev, typ, hodnoty in radky:
    if typ in ("svet", "skupina"):
        v = 74
        zaklad, tmava = (ZELENA, ZELENA_TMAVA) if typ == "svet" else (FIALOVA, FIALOVA_TMAVA)
        top, h = y + 9, v - 18
        ax.add_patch(FancyBboxPatch((L, top), P - L, h, boxstyle="round,pad=0,rounding_size=10",
                                    facecolor=zaklad, edgecolor="none", zorder=1))
        ax.add_patch(Rectangle((SLOUPCE[1], top), SLOUPCE[3] - SLOUPCE[1] - 10, h, facecolor=tmava, edgecolor="none", zorder=2))
        ax.add_patch(FancyBboxPatch((SLOUPCE[3] - 20, top), 20, h, boxstyle="round,pad=0,rounding_size=10",
                                    facecolor=tmava, edgecolor="none", zorder=2))
        for x in SLOUPCE[1:3]:  # tenké světlé dělení buněk projekcí
            ax.plot([x, x], [top, top + h], color="white", linewidth=1.5 / PT, alpha=0.35, zorder=3)
        stred_y = top + h / 2
        text(L + 22, stred_y, nazev, 25, "white", BOLD, va="center_baseline", zorder=4)
        for stred, hv in zip(STREDY, hodnoty):
            text(stred, stred_y, hodnota(hv), 25, "white", BOLD, ha="center", va="center_baseline", zorder=4)
        pruh = True  # první řádek pod skupinou je pruhovaný
    else:
        v = 56
        if pruh:
            ax.add_patch(Rectangle((L, y), SLOUPCE[1] - L, v, facecolor=SEDA_PRUH, edgecolor="none", zorder=0))
        ax.add_patch(Rectangle((SLOUPCE[1], y), SLOUPCE[3] - SLOUPCE[1], v,
                               facecolor=ZELENA_PRUH if pruh else ZELENA_SVETLA, edgecolor="none", zorder=0))
        ax.plot([L, P], [y + v, y + v], color=CARA, linewidth=1.5 / PT, zorder=1)
        stred_y = y + v / 2
        odsazeni, font = {"zeme": (22, MEDIUM), "ostatni": (22, REGULAR), "podrizena": (62, REGULAR)}[typ]
        text(L + odsazeni, stred_y, nazev, 23, TEXT, font, va="center_baseline", zorder=2)
        for stred, hv in zip(STREDY, hodnoty):
            zaporna = hv < 0
            text(stred, stred_y, hodnota(hv), 23, ZAPORNA if zaporna else TEXT, BOLD if zaporna else MEDIUM,
                 ha="center", va="center_baseline", zorder=2)
        pruh = not pruh
    y += v

# patička se zdrojem
y += 50
t = text(L, y, "Zdroj:", 19, pg.TEXT_SEDY, BOLD, va="baseline")
sirka = t.get_window_extent(renderer=fig.canvas.get_renderer()).width
text(L + sirka + 4, y, "Mezinárodní měnový fond (MMF), World Economic Outlook, říjen 2026.", 19, pg.TEXT_SEDY,
     REGULAR, va="baseline")
text(L, y + 32, "Tabulka byla vytvořena pomocí AI.", 19, pg.TEXT_SEDY, REGULAR, va="baseline")

os.makedirs(os.path.dirname(ZAKLAD), exist_ok=True)
fig.savefig(ZAKLAD + ".png", dpi=DPI, facecolor="white")

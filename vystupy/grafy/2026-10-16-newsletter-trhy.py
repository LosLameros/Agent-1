"""Přehled trhů za týden – tabulka do newsletteru v Portu vzhledu.

Data: týdenní podklad (tabulka od redakce), uložená v CSV vedle skriptu.
Vzhled: Rethink Sans, barvy Portu (fialová #4840BB, zelená #00AA3C), jako tabulka výhledu MMF.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-newsletter-trhy.py
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

ZAKLAD = "vystupy/grafy/2026-10-16-newsletter-trhy"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
MEDIUM = font_manager.FontProperties(fname=F + "-Medium.ttf")
BOLD = font_manager.FontProperties(fname=F + "-Bold.ttf")

TEXT = "#202020"
SEDA_PRUH = "#F4F4F7"
CARA = "#E7E7EB"
FIALOVA_SVETLA = "#ECEBF8"  # zvýraznění řádku Portu (odstín z brand manuálu Portu)
ZAPORNA = "#BE0000"
W, DPI = 1200, 200
PT = DPI / 72

radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))
RADEK = 62
H = 150 + len(radky) * RADEK + 40
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


L, P = 30, 1170
X_HODNOTA, X_MENA, X_TYDEN, X_YTD = 640, 690, 960, P - 20

text(L, 58, "Přehled trhů za uplynulý týden", 40, pg.TEXT_TMAVY, REGULAR, va="baseline")
ax.add_patch(FancyBboxPatch((L, 76), 110, 9, boxstyle="round,pad=0,rounding_size=4.5", facecolor=pg.ZELENA,
                            edgecolor="none"))

# hlavička
Y_HL = 132
for x, nazev, zarovnani in ((L + 18, "Index", "left"), (X_HODNOTA, "Hodnota", "right"), (X_MENA, "Měna", "left"),
                            (X_TYDEN, "Týdenní změna", "right"), (X_YTD, "Výnos YTD", "right")):
    text(x, Y_HL, nazev, 22, TEXT, BOLD, ha=zarovnani, va="baseline")
ax.plot([L, P], [146, 146], color=pg.TEXT_TMAVY, linewidth=2.5 / PT)


def zmena(v):
    return pg.cislo(v, 1, "%")


y = 150
for i, r in enumerate(radky):
    portu = r["skupina"] == "portu"
    if portu:
        ax.add_patch(Rectangle((L, y), P - L, RADEK, facecolor=FIALOVA_SVETLA, edgecolor="none", zorder=0))
        ax.add_patch(Rectangle((L, y), 6, RADEK, facecolor=pg.FIALOVA, edgecolor="none", zorder=1))
    elif i % 2 == 0:
        ax.add_patch(Rectangle((L, y), P - L, RADEK, facecolor=SEDA_PRUH, edgecolor="none", zorder=0))
    ax.plot([L, P], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    text(L + 18, stred, r["nazev"], 23, pg.FIALOVA if portu else TEXT, BOLD if portu else MEDIUM,
         va="center_baseline", zorder=2)
    hodnota = pg.cislo(float(r["hodnota"]), int(r["mista"])) if r["hodnota"] else "–"
    text(X_HODNOTA, stred, hodnota, 23, TEXT, REGULAR, ha="right", va="center_baseline", zorder=2)
    text(X_MENA, stred, r["mena"] or "–", 23, pg.TEXT_SEDY, REGULAR, va="center_baseline", zorder=2)
    for x, klic in ((X_TYDEN, "tydenni_zmena_pct"), (X_YTD, "vynos_ytd_pct")):
        v = float(r[klic])
        text(x, stred, zmena(v), 23, ZAPORNA if v < 0 else pg.ZELENA, BOLD if portu else MEDIUM,
             ha="right", va="center_baseline", zorder=2)
    y += RADEK

os.makedirs(os.path.dirname(ZAKLAD), exist_ok=True)
fig.savefig(ZAKLAD + ".png", dpi=DPI, facecolor="white")

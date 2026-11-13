"""S&P 500 – meziroční růst zisků na akcii (EPS) a tržeb podle sektorů. Tabulka s pruhy v Portu vzhledu.

Data: převzato 1:1 z podkladové tabulky (řazeno podle růstu EPS, řádek S&P 500 celkem na svém místě v pořadí).
Vzhled: jako vystupy/grafy/2026-11-13-skandaly-ceo.png – fialová hlavička, zvýrazněný řádek, pruh podle růstu EPS.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-13-sp500-sektory-eps.py
"""
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-13-sp500-sektory-eps"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
MEDIUM = font_manager.FontProperties(fname=F + "-Medium.ttf")
SEMIBOLD = font_manager.FontProperties(fname=F + "-SemiBold.ttf")

TEXT = "#202020"
CARA = "#E7E7EB"
ZAPORNA = "#BE0000"
FIALOVA_SVETLA = "#ECEBF8"   # podklad zvýrazněného řádku
PRUH_SVETLY = "#D3CFF2"      # pruhy sektorů (světlý odstín fialové Portu)
W, DPI = 1200, 200
PT = DPI / 72

radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))
eps = [float(r["rust_eps_pct"]) for r in radky]

RADEK = 46
Y_HL = 128
VYSKA_HL = 56
Y_PRVNI = Y_HL + VYSKA_HL
H = Y_PRVNI + len(radky) * RADEK + 84
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


def zmena(v):
    return ("+" if v > 0 else "") + pg.cislo(v, 1, "%")


L, P = 30, 1170
X_SEKTOR, X_EPS, X_TRZBY = L + 18, 560, 760
X_PRUH, KONEC_PRUHU = 800, P - 16

text(L, 48, "S&P 500: meziroční růst zisků a tržeb podle sektorů", 34, pg.TEXT_TMAVY, REGULAR, va="baseline")
text(L, 90, "Srovnání růstu zisku na akcii (EPS) a tržeb", 20, pg.TEXT_SEDY, REGULAR, va="baseline")

ax.add_patch(Rectangle((L, Y_HL), P - L, VYSKA_HL, facecolor=pg.FIALOVA, edgecolor="none"))
stred_hl = Y_HL + VYSKA_HL / 2
for x, nazev, zarovnani in ((X_SEKTOR, "Sektor", "left"), (X_EPS, "Růst zisku (EPS)", "right"),
                            (X_TRZBY, "Růst tržeb", "right")):
    text(x, stred_hl, nazev, 20, "white", MEDIUM, ha=zarovnani, va="center_baseline")

y = Y_PRVNI
for r, v in zip(radky, eps):
    celkem = r["celkem"] == "1"
    if celkem:
        ax.add_patch(Rectangle((L, y), P - L, RADEK, facecolor=FIALOVA_SVETLA, edgecolor="none", zorder=0))
    ax.plot([L, P], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    text(X_SEKTOR, stred, r["sektor"], 21, pg.FIALOVA if celkem else TEXT, SEMIBOLD if celkem else REGULAR,
         va="center_baseline")
    for x, h in ((X_EPS, v), (X_TRZBY, float(r["rust_trzeb_pct"]))):
        text(x, stred, zmena(h), 21, ZAPORNA if h < 0 else pg.ZELENA, SEMIBOLD, ha="right", va="center_baseline")
    delka = max((KONEC_PRUHU - X_PRUH) * max(v, 0) / max(eps), 3)
    ax.add_patch(FancyBboxPatch((X_PRUH, stred - 11), delka, 22, boxstyle="round,pad=0,rounding_size=3",
                                facecolor=pg.FIALOVA if celkem else PRUH_SVETLY, edgecolor="none", zorder=2))
    y += RADEK

text(P, y + 52, "Tabulka: Portu", 18, pg.TEXT_SEDY, REGULAR, ha="right", va="baseline")
fig.savefig(ZAKLAD + ".png", dpi=DPI, facecolor="white")

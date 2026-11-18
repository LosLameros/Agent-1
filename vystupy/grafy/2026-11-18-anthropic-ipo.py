"""Anthropic – IPO v kostce: klíčové parametry očekávaného vstupu na burzu (Nasdaq: ANT). Tabulka v Portu vzhledu.

Data: převzato 1:1 z předlohy (zdroj Anthropic). Kontrola: 825 mil. akcií × 78 USD = 64,35 mld. USD (horní hranice rozpětí).
Uloženo ostře ve dvojnásobném rozlišení (2400 px na šířku).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-18-anthropic-ipo.py
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

ZAKLAD = "vystupy/grafy/2026-11-18-anthropic-ipo"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
MEDIUM = font_manager.FontProperties(fname=F + "-Medium.ttf")
SEMIBOLD = font_manager.FontProperties(fname=F + "-SemiBold.ttf")

TEXT = "#202020"
CARA = "#E7E7EB"
FIALOVA_SVETLA = "#ECEBF8"   # podklad zvýrazněného řádku
W, DPI = 1200, 200           # rozvržení v bodech jako u ostatních tabulek
VYSTUP_DPI = 400             # uložení ve dvojnásobném rozlišení → 2400 px
PT = DPI / 72

radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))

RADEK = 60
Y_HL = 142
VYSKA_HL = 54
Y_PRVNI = Y_HL + VYSKA_HL + 4
H = Y_PRVNI + len(radky) * RADEK + 84
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


L, P = 30, 1170
X_PARAMETR, X_UDAJ = L + 28, 680

text(L, 52, "IPO v kostce", 38, pg.TEXT_TMAVY, REGULAR, va="baseline")
text(L, 98, "Přehled klíčových parametrů očekávaného vstupu na burzu (Nasdaq: ANT)", 20, pg.TEXT_SEDY, REGULAR,
     va="baseline")

ax.add_patch(FancyBboxPatch((L, Y_HL), P - L, VYSKA_HL, boxstyle="round,pad=0,rounding_size=7",
                            facecolor=pg.FIALOVA, edgecolor="none"))
stred_hl = Y_HL + VYSKA_HL / 2
for x, nazev in ((X_PARAMETR, "Parametr"), (X_UDAJ, "Údaj")):
    text(x, stred_hl, nazev, 20, "white", MEDIUM, va="center_baseline")

y = Y_PRVNI
for r in radky:
    zvyraznit = r["zvyraznit"] == "1"
    if zvyraznit:
        ax.add_patch(Rectangle((L, y), P - L, RADEK, facecolor=FIALOVA_SVETLA, edgecolor="none", zorder=0))
    ax.plot([L, P], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    text(X_PARAMETR, stred, r["parametr"], 22, pg.FIALOVA if zvyraznit else TEXT, SEMIBOLD if zvyraznit else REGULAR,
         va="center_baseline", zorder=2)
    text(X_UDAJ, stred, r["udaj"], 22, pg.FIALOVA if zvyraznit else TEXT, SEMIBOLD, va="center_baseline", zorder=2)
    y += RADEK

text(P, y + 50, "Tabulka: Portu, zdroj: Anthropic", 18, pg.TEXT_SEDY, REGULAR, ha="right", va="baseline")
fig.savefig(ZAKLAD + ".png", dpi=VYSTUP_DPI, facecolor="white")

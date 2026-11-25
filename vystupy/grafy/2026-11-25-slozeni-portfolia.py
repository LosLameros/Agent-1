"""Složení portfolia – váhy jednotlivých firem a hotovosti. Tabulka s pruhy v Portu vzhledu.

Data: převzato 1:1 z podkladové tabulky (Firma / Váha); váhy dávají dohromady 100 %. Název a podnadpis v předloze
nebyly, doplněno neutrálně. Hotovost má světlejší pruh než firmy.
Uloženo ostře ve dvojnásobném rozlišení (2400 px na šířku).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-25-slozeni-portfolia.py
"""
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-25-slozeni-portfolia"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
MEDIUM = font_manager.FontProperties(fname=F + "-Medium.ttf")
SEMIBOLD = font_manager.FontProperties(fname=F + "-SemiBold.ttf")

TEXT = "#202020"
CARA = "#E7E7EB"
PRUH_SVETLY = "#D3CFF2"      # pruh hotovosti (světlý odstín fialové Portu)
W, DPI = 1200, 200           # rozvržení v bodech jako u ostatních tabulek
VYSTUP_DPI = 400             # uložení ve dvojnásobném rozlišení → 2400 px
PT = DPI / 72

radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))
vahy = [float(r["vaha_pct"]) for r in radky]
assert abs(sum(vahy) - 100) < 1e-9, "váhy musí dávat 100 %"

RADEK = 56
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
X_FIRMA, X_VAHA = L + 28, 620
X_PRUH, KONEC_PRUHU = 690, P - 24

text(L, 52, "Složení portfolia", 38, pg.TEXT_TMAVY, REGULAR, va="baseline")
text(L, 98, "Váha jednotlivých firem a hotovosti v portfoliu", 20, pg.TEXT_SEDY, REGULAR, va="baseline")

ax.add_patch(FancyBboxPatch((L, Y_HL), P - L, VYSKA_HL, boxstyle="round,pad=0,rounding_size=7",
                            facecolor=pg.FIALOVA, edgecolor="none"))
stred_hl = Y_HL + VYSKA_HL / 2
for x, nazev, zarovnani in ((X_FIRMA, "Firma", "left"), (X_VAHA, "Váha", "right")):
    text(x, stred_hl, nazev, 20, "white", MEDIUM, ha=zarovnani, va="center_baseline")

y = Y_PRVNI
for r, v in zip(radky, vahy):
    hotovost = r["firma"] == "Hotovost"
    ax.plot([L, P], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    text(X_FIRMA, stred, r["firma"], 22, TEXT, REGULAR, va="center_baseline")
    text(X_VAHA, stred, pg.cislo(v, 0, "%"), 22, TEXT, SEMIBOLD, ha="right", va="center_baseline")
    delka = (KONEC_PRUHU - X_PRUH) * v / max(vahy)
    ax.add_patch(FancyBboxPatch((X_PRUH, stred - 11), delka, 22, boxstyle="round,pad=0,rounding_size=3",
                                facecolor=PRUH_SVETLY if hotovost else pg.FIALOVA, edgecolor="none", zorder=2))
    y += RADEK

text(P, y + 50, "Tabulka: Portu", 18, pg.TEXT_SEDY, REGULAR, ha="right", va="baseline")
fig.savefig(ZAKLAD + ".png", dpi=VYSTUP_DPI, facecolor="white")

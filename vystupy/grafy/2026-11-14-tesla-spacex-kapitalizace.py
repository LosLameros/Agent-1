"""Nejhodnotnější společnosti světa, kdyby Tesla a SpaceX byly jedna firma – tabulka v Portu vzhledu, česky.

Data: převzato 1:1 z předlohy (slovenská verze tabulky, zdroj companiesmarketcap.com), tržní kapitalizace v bilionech
USD; u spojené firmy je sečtená hodnota Tesly a SpaceX. Řazeno podle hodnoty, spojená firma je 5.
Výstup 2400 px na šířku (2× rozlišení ostatních tabulek), aby šel použít i do tisku a na velké obrazovky.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-14-tesla-spacex-kapitalizace.py
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

ZAKLAD = "vystupy/grafy/2026-11-14-tesla-spacex-kapitalizace"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
MEDIUM = font_manager.FontProperties(fname=F + "-Medium.ttf")
SEMIBOLD = font_manager.FontProperties(fname=F + "-SemiBold.ttf")

TEXT = "#202020"
CARA = "#E7E7EB"
FIALOVA_SVETLA = "#ECEBF8"   # podklad zvýrazněného řádku
PRUH_SVETLY = "#D3CFF2"      # pruhy ostatních firem (světlý odstín fialové Portu)
W, DPI = 1200, 200           # rozvržení v bodech jako u ostatních tabulek
VYSTUP_DPI = 400             # uložení ve dvojnásobném rozlišení → 2400 px
PT = DPI / 72

radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))
hodnoty = [float(r["kapitalizace_bil_usd"]) for r in radky]

RADEK = 54
Y_HL = 214                  # horní hrana fialové hlavičky
VYSKA_HL = 52
Y_PRVNI = Y_HL + VYSKA_HL + 8
H = Y_PRVNI + len(radky) * RADEK + 84
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


L, P = 30, 1170
X_PORADI, X_FIRMA, X_HODNOTA = L + 70, L + 130, 640
X_PRUH, KONEC_PRUHU = 690, P - 20

text(L, 52, "Nejhodnotnější společnosti světa, kdyby", 38, pg.TEXT_TMAVY, REGULAR, va="baseline")
text(L, 100, "Tesla a SpaceX byly jedna firma", 38, pg.TEXT_TMAVY, REGULAR, va="baseline")
text(L, 150, "Tržní kapitalizace v bilionech amerických dolarů.", 20, pg.TEXT_SEDY, REGULAR, va="baseline")
text(L, 180, "U spojené firmy je sečtená hodnota Tesly a SpaceX.", 20, pg.TEXT_SEDY, REGULAR, va="baseline")

# fialová hlavička se zaoblenými rohy
ax.add_patch(FancyBboxPatch((L, Y_HL), P - L, VYSKA_HL, boxstyle="round,pad=0,rounding_size=7",
                            facecolor=pg.FIALOVA, edgecolor="none"))
stred_hl = Y_HL + VYSKA_HL / 2
for x, nazev, zarovnani in ((X_PORADI, "Pořadí", "center"), (X_FIRMA, "Společnost", "left"),
                            (X_HODNOTA, "Tržní kapitalizace", "right")):
    text(x, stred_hl, nazev, 20, "white", MEDIUM, ha=zarovnani, va="center_baseline")

y = Y_PRVNI
for r, v in zip(radky, hodnoty):
    zvyraznit = r["zvyraznit"] == "1"
    if zvyraznit:
        ax.add_patch(Rectangle((L, y), P - L, RADEK, facecolor=FIALOVA_SVETLA, edgecolor="none", zorder=0))
    ax.plot([L, P], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    text(X_PORADI, stred, r["poradi"], 21, pg.FIALOVA if zvyraznit else pg.TEXT_SEDY, REGULAR, ha="center",
         va="center_baseline")
    t = text(X_FIRMA, stred, r["spolecnost"], 22, pg.FIALOVA if zvyraznit else TEXT,
             SEMIBOLD if zvyraznit else REGULAR, va="center_baseline")
    sirka = t.get_window_extent(renderer=fig.canvas.get_renderer()).width
    text(X_FIRMA + sirka + 14, stred, r["ticker"], 15, pg.TEXT_SEDY, REGULAR, va="center_baseline")
    text(X_HODNOTA, stred, f"{pg.cislo(v, 2)} bil. USD", 22, pg.FIALOVA if zvyraznit else TEXT, SEMIBOLD,
         ha="right", va="center_baseline")
    delka = (KONEC_PRUHU - X_PRUH) * v / max(hodnoty)
    ax.add_patch(FancyBboxPatch((X_PRUH, stred - 11), delka, 22, boxstyle="round,pad=0,rounding_size=3",
                                facecolor=pg.FIALOVA if zvyraznit else PRUH_SVETLY, edgecolor="none", zorder=2))
    y += RADEK

text(P, y + 50, "Tabulka: Portu, zdroj: companiesmarketcap.com", 18, pg.TEXT_SEDY, REGULAR, ha="right", va="baseline")
fig.savefig(ZAKLAD + ".png", dpi=VYSTUP_DPI, facecolor="white")

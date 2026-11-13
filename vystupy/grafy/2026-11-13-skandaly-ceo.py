"""Největší firmy se skandálem CEO – tržní hodnota před propuknutím skandálu. Tabulka v Portu vzhledu.

Data: převzato z podkladové tabulky (zdroj SEC Filings / Yahoo Finance) – tržní hodnota při posledním závěru
obchodování před propuknutím osobního skandálu CEO. Kontrola nadpisu: firmy 2–10 dohromady 1 094 mld. USD,
Nvidia 4 500 mld. USD = 4,1×.
Vzhled: jako tabulka do newsletteru (Rethink Sans, fialová #4840BB, zelená #00AA3C).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-13-skandaly-ceo.py
"""
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle  # noqa: E402

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-13-skandaly-ceo"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
MEDIUM = font_manager.FontProperties(fname=F + "-Medium.ttf")
BOLD = font_manager.FontProperties(fname=F + "-Bold.ttf")

TEXT = "#202020"
SEDA_PRUH = "#F4F4F7"
CARA = "#E7E7EB"
FIALOVA_SVETLA = "#ECEBF8"  # zvýraznění řádku (odstín z brand manuálu Portu)
W, DPI = 1200, 200
PT = DPI / 72

radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))
ostatni = sum(float(r["trzni_hodnota_mld_usd"]) for r in radky[1:])
nasobek = float(radky[0]["trzni_hodnota_mld_usd"]) / ostatni

RADEK = 62
Y_TAB = 236
H = Y_TAB + 46 + len(radky) * RADEK + 70
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


L, P = 30, 1170
X_PORADI, X_FIRMA, X_HODNOTA = L + 40, L + 110, P - 20

text(L, 58, f"Nvidia má {nasobek:.0f}× vyšší hodnotu než 9 největších", 40, pg.TEXT_TMAVY, REGULAR, va="baseline")
text(L, 108, "firem se skandálem CEO dohromady", 40, pg.TEXT_TMAVY, REGULAR, va="baseline")
ax.add_patch(FancyBboxPatch((L, 126), 110, 9, boxstyle="round,pad=0,rounding_size=4.5", facecolor=pg.ZELENA,
                            edgecolor="none"))
text(L, 176, "Tržní hodnota při posledním závěru obchodování před propuknutím osobního skandálu CEO", 22,
     pg.FIALOVA, MEDIUM, va="baseline")

# hlavička
for x, nazev, zarovnani in ((X_PORADI, "Pořadí", "center"), (X_FIRMA, "Společnost a rok", "left"),
                            (X_HODNOTA, "Tržní hodnota", "right")):
    text(x, Y_TAB + 26, nazev, 22, TEXT, BOLD, ha=zarovnani, va="baseline")
ax.plot([L, P], [Y_TAB + 42, Y_TAB + 42], color=pg.TEXT_TMAVY, linewidth=2.5 / PT)

y = Y_TAB + 46
for i, r in enumerate(radky):
    prvni = i == 0
    if prvni:
        ax.add_patch(Rectangle((L, y), P - L, RADEK, facecolor=FIALOVA_SVETLA, edgecolor="none", zorder=0))
        ax.add_patch(Rectangle((L, y), 6, RADEK, facecolor=pg.FIALOVA, edgecolor="none", zorder=1))
    elif i % 2 == 0:
        ax.add_patch(Rectangle((L, y), P - L, RADEK, facecolor=SEDA_PRUH, edgecolor="none", zorder=0))
    ax.plot([L, P], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    ax.add_patch(Circle((X_PORADI, stred), 19, facecolor=pg.FIALOVA if prvni else FIALOVA_SVETLA, edgecolor="none",
                        zorder=2))
    text(X_PORADI, stred, r["poradi"], 19, "white" if prvni else pg.FIALOVA, BOLD, ha="center",
         va="center_baseline", zorder=3)
    t = text(X_FIRMA, stred, r["spolecnost"], 23, pg.FIALOVA if prvni else TEXT, BOLD, va="center_baseline", zorder=2)
    sirka = t.get_window_extent(renderer=fig.canvas.get_renderer()).width
    text(X_FIRMA + sirka + 2, stred, f", {r['rok']}", 23, pg.FIALOVA if prvni else pg.TEXT_SEDY,
         BOLD if prvni else REGULAR, va="center_baseline", zorder=2)
    text(X_HODNOTA, stred, r["trzni_hodnota_text"], 23, pg.FIALOVA if prvni else TEXT, BOLD,
         ha="right", va="center_baseline", zorder=2)
    y += RADEK

text(L, y + 46, "Zdroj:", 19, pg.TEXT_SEDY, BOLD, va="baseline")
text(L + 62, y + 46, "SEC Filings, Yahoo Finance. Graf: Portu", 19, pg.TEXT_SEDY, REGULAR, va="baseline")
fig.savefig(ZAKLAD + ".png", dpi=DPI, facecolor="white")

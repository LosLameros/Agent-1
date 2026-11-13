"""Největší firmy se skandálem CEO – tržní hodnota před propuknutím skandálu. Tabulka s pruhy v Portu vzhledu.

Data: převzato z podkladové tabulky (zdroj SEC Filings / Yahoo Finance) – tržní hodnota při posledním závěru
obchodování před propuknutím osobního skandálu CEO. Kontrola nadpisu: firmy 2–10 dohromady 1 094 mld. USD,
Nvidia 4 500 mld. USD = 4,1×.
Vzhled: podle tabulky „Nejhodnotnější společnosti světa…“ – fialová hlavička s bílým textem, pruh u každé firmy
(světle fialový, zvýrazněná firma plnou fialovou #4840BB), Rethink Sans, zdroj vpravo dole.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-13-skandaly-ceo.py
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

ZAKLAD = "vystupy/grafy/2026-11-13-skandaly-ceo"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
MEDIUM = font_manager.FontProperties(fname=F + "-Medium.ttf")
SEMIBOLD = font_manager.FontProperties(fname=F + "-SemiBold.ttf")

TEXT = "#202020"
CARA = "#E7E7EB"
FIALOVA_SVETLA = "#ECEBF8"   # podklad zvýrazněného řádku
PRUH_SVETLY = "#D3CFF2"      # pruhy ostatních firem (světlý odstín fialové Portu)
W, DPI = 1200, 200
PT = DPI / 72

radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))
hodnoty = [float(r["trzni_hodnota_mld_usd"]) for r in radky]
nasobek = hodnoty[0] / sum(hodnoty[1:])

RADEK = 46
Y_HL = 168                   # horní hrana fialové hlavičky
VYSKA_HL = 50
Y_PRVNI = Y_HL + VYSKA_HL    # horní hrana prvního řádku
H = Y_PRVNI + len(radky) * RADEK + 84
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


L, P = 30, 1170
X_PORADI, X_FIRMA, X_HODNOTA = L + 70, L + 110, 690
X_PRUH, KONEC_PRUHU = 720, P - 16

text(L, 48, f"Nvidia má {nasobek:.0f}× vyšší hodnotu než 9 největších firem", 34, pg.TEXT_TMAVY, REGULAR,
     va="baseline")
text(L, 92, "se skandálem CEO dohromady", 34, pg.TEXT_TMAVY, REGULAR, va="baseline")
text(L, 134, "Tržní hodnota při posledním závěru obchodování před propuknutím osobního skandálu CEO", 20,
     pg.TEXT_SEDY, REGULAR, va="baseline")

# fialová hlavička
ax.add_patch(Rectangle((L, Y_HL), P - L, VYSKA_HL, facecolor=pg.FIALOVA, edgecolor="none"))
stred_hl = Y_HL + VYSKA_HL / 2
for x, nazev, zarovnani in ((X_PORADI, "Pořadí", "right"), (X_FIRMA, "Společnost a rok", "left"),
                            (X_HODNOTA, "Tržní hodnota", "right")):
    text(x, stred_hl, nazev, 20, "white", MEDIUM, ha=zarovnani, va="center_baseline")

y = Y_PRVNI
for i, (r, v) in enumerate(zip(radky, hodnoty)):
    prvni = i == 0
    if prvni:
        ax.add_patch(Rectangle((L, y), P - L, RADEK, facecolor=FIALOVA_SVETLA, edgecolor="none", zorder=0))
    ax.plot([L, P], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    text(X_PORADI, stred, r["poradi"], 21, pg.TEXT_SEDY, REGULAR, ha="right", va="center_baseline")
    t = text(X_FIRMA, stred, r["spolecnost"], 21, TEXT, SEMIBOLD if prvni else REGULAR, va="center_baseline")
    sirka = t.get_window_extent(renderer=fig.canvas.get_renderer()).width
    text(X_FIRMA + sirka + 12, stred, r["rok"], 16, pg.TEXT_SEDY, REGULAR, va="center_baseline")
    text(X_HODNOTA, stred, r["trzni_hodnota_text"], 21, TEXT, SEMIBOLD, ha="right", va="center_baseline")
    delka = max((KONEC_PRUHU - X_PRUH) * v / max(hodnoty), 3)
    ax.add_patch(FancyBboxPatch((X_PRUH, stred - 11), delka, 22, boxstyle="round,pad=0,rounding_size=3",
                                facecolor=pg.FIALOVA if prvni else PRUH_SVETLY, edgecolor="none", zorder=2))
    y += RADEK

text(P, y + 52, "Tabulka: Portu, zdroj: SEC Filings, Yahoo Finance", 18, pg.TEXT_SEDY, REGULAR, ha="right",
     va="baseline")
fig.savefig(ZAKLAD + ".png", dpi=DPI, facecolor="white")

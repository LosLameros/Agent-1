"""Meziroční růst zisků S&P 500 ve 3. čtvrtletí 2026 – verze v barvách ZFP akademie.

Rozvržení 1:1 podle podkladového grafu (1920 × 1032 px), změněné jen barvy a písmo
(styl ZFP akademie, viz nastroje/zfpa_grafy.py) a všechna písma o 2 body větší.
Data: podkladový graf (zdroj FactSet), uložená v CSV vedle skriptu.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-14-zisky-sp500-3q2026-zfpa.py
"""
import csv
import sys

from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, "nastroje")
from zfpa_grafy import (BOLD, LEGENDA, MEDIUM, MRIZKA, NADPIS, ORANZOVA, OSA, PT, REGULAR,  # noqa: E402
                        SEDA, SEDA_POPISEK, TEXT, ZDROJ, cislo, platno, uloz)
import zfpa_grafy as z  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-14-zisky-sp500-3q2026-zfpa"

# --- data ---------------------------------------------------------------------
kategorie, aktualni, cerven = [], [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        kategorie.append(r["sektor"])
        aktualni.append(float(r["aktualni_odhad_pct"]))
        cerven.append(float(r["odhad_k_30_6_2026_pct"]))

fig, ax = platno()


def text(*args, **kw):
    return z.text(ax, *args, **kw)


def sirka_textu(t):
    return z.sirka_textu(ax, t)


def sloupec(x, y_vrch, sirka, vyska, barva):
    z.sloupec(ax, x, y_vrch + vyska, sirka, vyska, barva)


# nadpis, legenda
text(32, 74, "Meziroční růst zisků S&P 500 ve 3. čtvrtletí 2026", 44, NADPIS, REGULAR, va="baseline")
x = 33
for barva, popis in ((ORANZOVA, "Aktuální odhad"), (SEDA, "Odhad k 30. 6. 2026")):
    ax.add_patch(FancyBboxPatch((x, 115), 22, 22, boxstyle="round,pad=0,rounding_size=3",
                                facecolor=barva, edgecolor="none"))
    t = text(x + 36, 126, popis, 23, LEGENDA, MEDIUM, va="center_baseline")
    x += 36 + sirka_textu(t) + 60

# osa y a mřížka: 0 % na y = 863, 25 % = 132 px
NULA, KROK_PX = 863.5, 132
LEVA, PRAVA = 92, 1890
for i, hodnota in enumerate(range(0, 126, 25)):
    y = NULA - i * KROK_PX
    ax.plot([LEVA, PRAVA], [y, y], color=MRIZKA, linewidth=2 / PT * 72 / 72, zorder=1)
    text(76, y, f"{hodnota} %", 21, OSA, REGULAR, ha="right", va="center_baseline")

# sloupce: dvojice 61 px + mezera 6 px, rozteč 150 px, první začíná na x = 104
SIRKA, MEZERA, ROZTEC, START = 61, 6, 149.8, 104
popisky_kategorii = []
for k, (kat, a, c) in enumerate(zip(kategorie, aktualni, cerven)):
    x0 = START + k * ROZTEC
    popisky = []
    for x, hodnota, barva, popisek in ((x0, a, ORANZOVA, ORANZOVA), (x0 + SIRKA + MEZERA, c, SEDA, SEDA_POPISEK)):
        vyska = hodnota / 25 * KROK_PX
        sloupec(x, NULA - vyska, SIRKA, vyska, barva)
        popisky.append([x + SIRKA / 2, NULA - vyska - 12, cislo(hodnota), popisek])
    # popisky hodnot: větší písmo je širší než sloupec – když by se dva vedle sebe překrývaly,
    # zvedni popisek vyššího sloupce nad popisek nižšího (oba zůstanou u svých sloupců)
    (xl, yl, tl, cl), (xp, yp, tp, cp) = popisky
    t_l = text(xl, yl, tl, 18, cl, BOLD, ha="center", va="baseline", zorder=3)
    t_p = text(xp, yp, tp, 18, cp, BOLD, ha="center", va="baseline", zorder=3)
    if (sirka_textu(t_l) + sirka_textu(t_p)) / 2 > xp - xl - 4:
        vyska_textu = t_l.get_window_extent(renderer=fig.canvas.get_renderer()).height + 4
        if abs(yl - yp) < vyska_textu:
            if yl <= yp:
                t_l.set_y(yp - vyska_textu)
            else:
                t_p.set_y(yl - vyska_textu)
    stred = x0 + SIRKA + MEZERA / 2
    je_index = kat == "S&P 500"
    radky = kat.split(" ", 1) if (" " in kat and len(kat) > 10 and not je_index) else [kat]
    texty = [text(stred, 916 + j * 36, radek, 21.5, NADPIS if je_index else TEXT, BOLD if je_index else REGULAR,
                  ha="center", va="baseline") for j, radek in enumerate(radky)]
    popisky_kategorii.append([stred, max(sirka_textu(t) for t in texty), texty])

# popisky kategorií: když se dva sousední překrývají, odsuň je od sebe (min. mezera 14 px)
for _ in range(5):
    for levy, pravy in zip(popisky_kategorii, popisky_kategorii[1:]):
        prekryv = (levy[0] + levy[1] / 2 + 14) - (pravy[0] - pravy[1] / 2)
        if prekryv > 0:
            levy[0] -= prekryv / 2
            pravy[0] += prekryv / 2
for stred, _, texty in popisky_kategorii:
    for t in texty:
        t.set_x(stred)

# zdroj
text(32, 1003, "Zdroj: FactSet, vytvořeno AI", 26, ZDROJ, MEDIUM, va="baseline")

uloz(fig, ZAKLAD + ".png")

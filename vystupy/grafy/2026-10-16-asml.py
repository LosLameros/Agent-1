"""ASML Holding N.V. (ASML) – tržby, čistý zisk a provozní marže, roční údaje v mil. eur.

Data: výkazy ASML podle US GAAP – roky 2017–2025 z výročních zpráv (20-F, SEC XBRL),
posledních 12 měsíců = rok 2025 − 1.–3. čtvrtletí 2025 + 1.–3. čtvrtletí 2026 (6-K ze 14. 10. 2026).
Provozní marže = provozní zisk (income from operations) / celkové tržby.
Vzhled: nástroj nastroje/portu_grafy.py (barvy, písmo Rethink Sans, legenda a zdroj dole).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-asml.py
"""
import csv
import sys
from decimal import ROUND_HALF_UP, Decimal

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-16-asml"
BOLD = font_manager.FontProperties(fname="nastroje/fonty/RethinkSans-Bold.ttf")
CARA_MARZE = pg.TEXT_TMAVY

obdobi, trzby, zisk, marze = [], [], [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        obdobi.append(r["obdobi"])
        trzby.append(float(r["trzby_mil_eur"]))
        zisk.append(float(r["cisty_zisk_mil_eur"]))
        marze.append(float(r["provozni_marze_pct"]))


def cele(v):
    """Zaokrouhlení 13 978,5 → 13 979 (ne bankovní) a mezera v tisících."""
    return pg.cislo(float(Decimal(str(v)).quantize(Decimal("1"), ROUND_HALF_UP)), 0)


# plátno 1370 × 830 px: nadpis, podtitulek, graf, osa x, legenda + zdroj
W, H = pg.SIRKA_PX, 830
fig = plt.figure(figsize=(W / pg.DPI, H / pg.DPI), dpi=pg.DPI, facecolor="white")
LEVA, PRAVA, HORNI, DOLNI = 98, pg.GRAF_PRAVA, 150, 700
ax = fig.add_axes([LEVA / W, 1 - DOLNI / H, (PRAVA - LEVA) / W, (DOLNI - HORNI) / H])
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0, colors=pg.TEXT_SEDY, labelsize=pg.PISMO_OSA)
ax.grid(axis="y", color=pg.MRIZKA, linewidth=1.4 * 72 / pg.DPI)
ax.set_axisbelow(True)

fig.text(11 / W, 1 - 40 / H, "ASML Holding N.V. (ASML)", fontsize=pg.PISMO_NADPIS, color=pg.TEXT_TMAVY, va="center")
fig.text(11 / W, 1 - 86 / H, "Roční údaje v milionech eur", fontsize=pg.PISMO_LEGENDA, color=pg.FIALOVA, va="center")

# osa y (mil. eur)
ax.set_ylim(0, 48000)
ax.set_yticks(range(0, 48001, 8000))
ax.set_yticklabels([pg.cislo(v, 0) for v in range(0, 48001, 8000)])
ax.tick_params(axis="y", pad=20 / pg.PT)
ax.axhline(0, color=pg.NULOVA_CARA, linewidth=2 * 72 / pg.DPI, zorder=3)

# sloupce: tržby zeleně, čistý zisk fialově (jako v podkladu)
n = len(obdobi)
ax.set_xlim(-0.5, n - 0.5)
SIRKA, MEZERA = 0.28, 0.12  # mezera, aby popisky zisku nezasahovaly do sloupců tržeb
odsazeni = 8 / (DOLNI - HORNI) * 48000
for posun, hodnoty, barva in ((-(SIRKA + MEZERA) / 2, trzby, pg.ZELENA), ((SIRKA + MEZERA) / 2, zisk, pg.FIALOVA)):
    xs = [i + posun for i in range(n)]
    ax.bar(xs, hodnoty, width=SIRKA, color=barva, zorder=2, linewidth=0)
    for x, v in zip(xs, hodnoty):
        ax.text(x, v + odsazeni, cele(v), ha="center", va="bottom", fontsize=pg.PISMO_HODNOTA, color=pg.TEXT_TMAVY, zorder=4)

ax.set_xticks(range(n))
ax.set_xticklabels(obdobi, fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
ax.tick_params(axis="x", pad=24 / pg.PT)

# provozní marže: čára s body na vlastní (skryté) ose, popisky tučně nad body
ax2 = ax.twinx()
ax2.set_ylim(-30, 43)  # čára marže nad sloupci a jejich popisky
ax2.axis("off")
ax2.plot(range(n), marze, color=CARA_MARZE, linewidth=3 / pg.PT, marker="o", markersize=8 / pg.PT, zorder=5)
for i, m in enumerate(marze):
    ax2.text(i, m + 2.2, pg.cislo(round(m), 0, "%"), ha="center", va="bottom", fontsize=pg.PISMO_LEGENDA,
             color=pg.TEXT_TMAVY, fontproperties=BOLD, zorder=6,
             bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))

# legenda vlevo dole (čtverečky pro sloupce, čára s bodem pro marži), zdroj vpravo dole
y_leg = 1 - 795 / H
x = pg.GRAF_LEVA + 3
renderer = fig.canvas.get_renderer()
for popis, barva, typ in (("Celkové tržby", pg.ZELENA, "ctverec"), ("Čistý zisk", pg.FIALOVA, "ctverec"),
                          ("Provozní zisková marže", CARA_MARZE, "cara")):
    if typ == "ctverec":
        fig.patches.append(FancyBboxPatch((x / W, y_leg - 10 / H), 20 / W, 20 / H, boxstyle="round,pad=0,rounding_size=0.003",
                                          transform=fig.transFigure, facecolor=barva, edgecolor="none"))
        sirka_znacky = 20
    else:
        fig.add_artist(Line2D([x / W, (x + 34) / W], [y_leg, y_leg], transform=fig.transFigure, color=barva,
                              linewidth=3 / pg.PT))
        fig.add_artist(Line2D([(x + 17) / W], [y_leg], transform=fig.transFigure, color=barva, marker="o",
                              markersize=8 / pg.PT, linestyle="none"))
        sirka_znacky = 34
    t = fig.text((x + sirka_znacky + 13) / W, y_leg, popis, fontsize=pg.PISMO_LEGENDA, color=pg.TEXT_TMAVY,
                 va="center_baseline")
    x += sirka_znacky + 13 + t.get_window_extent(renderer).width + 37
fig.text(PRAVA / W, y_leg, "Graf: Portu, zdroj: ASML", fontsize=pg.PISMO_ZDROJ, color=pg.TEXT_SEDY, ha="right",
         va="center_baseline")

fig.savefig(ZAKLAD + ".png", dpi=pg.DPI, facecolor="white")

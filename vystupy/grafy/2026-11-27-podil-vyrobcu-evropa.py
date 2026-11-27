"""Podíl výrobců na registracích nových osobních aut v západní Evropě, první tři čtvrtletí 2025 vs. 2026, v %.

Data: převzato 1:1 z předlohy (zdroj ACEA). Hvězdička = součet všech značek výrobce; čínští výrobci = Geely Group,
BYD, SAIC Motor, Chery Automobile. Pozn.: VW + Škoda + Audi dávají 22,0 % (2025) a 20,9 % (2026); 26,7 % a 25,3 %
za celou skupinu Volkswagen v podnadpisu jsou z předlohy a zahrnují i další značky skupiny.
Nový design Portu: 2025 fialová, 2026 zelená (oficiální barvy Portu pro dvě řady).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-27-podil-vyrobcu-evropa.py
"""
import csv
import sys

from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-27-podil-vyrobcu-evropa"
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    r = list(csv.DictReader(f))
vyrobci = [x["vyrobce"].replace("Mercedes-Benz", "Mercedes-\nBenz").replace("Čínští výrobci*", "Čínští\nvýrobci*")
           for x in r]
p25 = [float(x["podil_2025_pct"]) for x in r]
p26 = [float(x["podil_2026_pct"]) for x in r]

OSA = (0, 16, 2)
DOLNI = pg.GRAF_DOLNI_2RADKY - 36          # místo na poznámku pod legendou
LEGENDA_Y = pg.LEGENDA_STRED_Y - 36
POZNAMKA_Y = pg.LEGENDA_STRED_Y + 4
fig, ax = pg._platno(
    DOLNI, nadpis="Evropští výrobci ztrácejí podíl ve prospěch čínských",
    podnadpis=("Podíl na registracích nových osobních aut v západní Evropě za prvních devět měsíců roku, v %.",
               "Podíl čínských výrobců vzrostl ze 7,4 % na 11,9 %. Celá skupina Volkswagen klesla z 26,7 % na 25,3 %."))
fy = fig._portu["fy"]
pg._osa_y(ax, OSA, "", 0)
n = len(vyrobci)
ax.set_xlim(-0.5, n - 0.5)
SIRKA, MEZERA = 0.32, 0.04
odsazeni = 8 / (DOLNI - pg.GRAF_HORNI) * (OSA[1] - OSA[0])
for posun, hodnoty, barva in ((-(SIRKA + MEZERA) / 2, p25, pg.FIALOVA), ((SIRKA + MEZERA) / 2, p26, pg.ZELENA)):
    xs = [i + posun for i in range(n)]
    ax.bar(xs, hodnoty, width=SIRKA, color=barva, zorder=2, linewidth=0)
    for x, h in zip(xs, hodnoty):
        ax.text(x, h + odsazeni, pg.cislo(h, 1), ha="center", va="bottom", fontsize=pg.PISMO_HODNOTA * 0.95,
                color=pg.TEXT_TMAVY)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=3)
ax.set_xticks([])
VYSKA = DOLNI - pg.GRAF_HORNI
for i, nazev in enumerate(vyrobci):  # každý řádek popisku na stejné účaří (diakritika jinak posouvá popisky)
    for k, radek in enumerate(nazev.split("\n")):
        ax.text(i, -(40 + k * 30) / VYSKA, radek, transform=ax.get_xaxis_transform(), ha="center", va="baseline",
                fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)

renderer = fig.canvas.get_renderer()
fig.canvas.draw()
leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
pos = ax.get_position()
ax.set_position([pg._fx(leva), pos.y0, pg._fx(pg.GRAF_PRAVA - leva), pos.height])

# legenda a zdroj o řádek výš, pod nimi poznámka s hvězdičkou
x = pg.GRAF_LEVA + 3
for nazev, barva in (("2025", pg.FIALOVA), ("2026", pg.ZELENA)):
    fig.patches.append(FancyBboxPatch(
        (pg._fx(x), fy(LEGENDA_Y + pg.CTVEREC / 2)), pg._fx(pg.CTVEREC), fy(LEGENDA_Y - pg.CTVEREC / 2) - fy(LEGENDA_Y + pg.CTVEREC / 2),
        boxstyle="round,pad=0,rounding_size=0.003", transform=fig.transFigure, facecolor=barva, edgecolor="none"))
    t = fig.text(pg._fx(x + pg.CTVEREC + 13), fy(LEGENDA_Y), nazev, fontsize=pg.PISMO_LEGENDA, color=pg.TEXT_TMAVY,
                 ha="left", va="center_baseline")
    x += pg.CTVEREC + 13 + t.get_window_extent(renderer=renderer).width + 37
fig.text(pg._fx(pg.GRAF_PRAVA), fy(LEGENDA_Y), "Graf: Portu, zdroj: ACEA", fontsize=pg.PISMO_ZDROJ, color=pg.TEXT_SEDY,
         ha="right", va="center_baseline")
fig.text(pg._fx(pg.GRAF_LEVA - 80), fy(POZNAMKA_Y),
         "*Součet podílů všech značek, které výrobce vlastní. Čínští výrobci: Geely Group, BYD, SAIC Motor, "
         "Chery Automobile.", fontsize=pg.PISMO_ZDROJ * 0.92, color=pg.TEXT_SEDY, ha="left", va="center_baseline")
pg.uloz(fig, ZAKLAD + ".png", zvetseni=2)

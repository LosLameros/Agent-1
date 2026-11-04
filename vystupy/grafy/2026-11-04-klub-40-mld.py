"""Nejrychlejší firmy na 40 mld. USD ročního hrubého zisku – počet let od založení. Portu vzhled.

Data: převzato z grafu „Anthropic is the Fastest Growing Company of All Time“ (Fiscal.ai): 26 firem, rok založení
a rok, kdy annualizovaný hrubý zisk poprvé dosáhl 40 mld. USD; počet let = rozdíl roků (všechny řádky sedí).
Medián 26 firem = 42 let. Vyšší graf než standardních 722 px kvůli 26 řádkům; jinak písmo, barvy a rozvržení
podle nastroje/portu_grafy.py.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-04-klub-40-mld.py
"""
import csv
import statistics
import sys

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-04-klub-40-mld"

with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    firmy = list(csv.DictReader(f))
let = [int(r["let"]) for r in firmy]
median = statistics.median(let)
meta = next(r for r in firmy if r["firma"] == "Meta")

RADEK = 34
Y_KPI = 142                      # řádek s velkými čísly
Y_HLAVICKA = 244                 # záhlaví tabulky
Y_PRVNI = 276                    # střed prvního řádku
Y_OSA = Y_PRVNI + len(firmy) * RADEK - RADEK / 2   # spodní hrana sloupců
LEGENDA_Y = Y_OSA + 92
VYSKA = int(LEGENDA_Y + 24)
X_FIRMA, X_ROKY, X_GRAF, X_KONEC = 11, 330, 560, 1290
OSA_MAX = 100

fig = plt.figure(figsize=(pg.SIRKA_PX / pg.DPI, VYSKA / pg.DPI), dpi=pg.DPI, facecolor=pg.POZADI)
plna = fig.add_axes([0, 0, 1, 1])
plna.set_xlim(0, pg.SIRKA_PX)
plna.set_ylim(VYSKA, 0)
plna.axis("off")


def text(x, y, s, px, barva, font=None, **kw):
    return plna.text(x, y, s, fontsize=px / pg.PT, color=barva, fontproperties=font, **kw)


# nadpis a podnadpis jako u ostatních grafů Portu
text(X_FIRMA, 30, "Anthropic je nejrychleji rostoucí firma v historii", 36, pg.TEXT_TMAVY, va="center")
text(X_FIRMA, 76, "Počet let od založení do 40 mld. USD ročního hrubého zisku (annualizovaně)", 24.5, pg.FIALOVA,
     pg._STREDNI, va="center")

# tři velká čísla
for x, cislo, popis, barva in ((X_FIRMA, "5 let", "Anthropic, 2021 → 2026", pg.ZELENA),
                               (330, f"{meta['let']} let", "nejrychlejší kótovaná firma (Meta)", pg.TEXT_TMAVY),
                               (760, f"{median:.0f} let", f"medián všech {len(firmy)} firem", pg.TEXT_TMAVY)):
    text(x, Y_KPI + 20, cislo, 48, barva, pg._TUCNE, va="baseline")
    text(x, Y_KPI + 52, popis, 21.5, pg.TEXT_SEDY, va="center")
plna.plot([X_FIRMA, X_KONEC + 60], [Y_HLAVICKA - 26] * 2, color=pg.MRIZKA, linewidth=1.5 / pg.PT)

# záhlaví tabulky
for x, s in ((X_FIRMA, "Firma"), (X_ROKY, "Založení → 40 mld."), (X_GRAF, "Počet let")):
    text(x, Y_HLAVICKA, s, 19, pg.TEXT_SEDY, pg._STREDNI, va="center")

# graf: sloupce v ose, která zabírá pravou část řádků
ax = fig.add_axes([X_GRAF / pg.SIRKA_PX, 1 - Y_OSA / VYSKA, (X_KONEC - X_GRAF) / pg.SIRKA_PX,
                   (Y_OSA - (Y_PRVNI - RADEK / 2)) / VYSKA])
ax.set_xlim(0, OSA_MAX)
ax.set_ylim(len(firmy) - 0.5, -0.5)
for strana in ax.spines.values():
    strana.set_visible(False)
ax.set_facecolor("none")
ax.grid(axis="x", color=pg.MRIZKA, linewidth=1.4 * 72 / pg.DPI)
ax.set_axisbelow(True)
ax.set_yticks([])
ax.set_xticks(range(0, OSA_MAX + 1, 10))
ax.set_xticklabels([str(t) for t in range(0, OSA_MAX + 1, 10)], fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
ax.tick_params(length=0, axis="x", pad=14 / pg.PT)

for i, r in enumerate(firmy):
    y = Y_PRVNI + i * RADEK
    anthropic = r["firma"] == "Anthropic"
    if i % 2 == 0:  # pruhované řádky jako v tabulkách Portu
        plna.add_patch(FancyBboxPatch((X_FIRMA - 6, y - RADEK / 2), X_KONEC + 66 - X_FIRMA, RADEK,
                                      boxstyle="square,pad=0", facecolor="#F4F4F7", edgecolor="none", zorder=0))
    text(X_FIRMA, y, r["firma"], 22, pg.TEXT_TMAVY, pg._TUCNE if anthropic else pg._STREDNI, va="center_baseline")
    sirka_nazvu = plna.texts[-1].get_window_extent(renderer=fig.canvas.get_renderer()).width
    text(X_FIRMA + sirka_nazvu + 8, y, f"({r['ticker']})", 19, pg.TEXT_SEDY, va="center_baseline")
    text(X_ROKY, y, f"{r['zalozeni']} → {r['rok_40_mld']}", 21, pg.TEXT_SEDY, va="center_baseline")
    barva = pg.ZELENA if anthropic else pg.FIALOVA
    ax.barh(i, int(r["let"]), height=0.62, color=barva, zorder=2, linewidth=0)
    ax.text(int(r["let"]) + 0.8, i, f"{r['let']} let", ha="left", va="center", fontsize=pg.PISMO_HODNOTA,
            color=pg.TEXT_TMAVY, fontproperties=pg._TUCNE if anthropic else pg._STREDNI)

# legenda vlevo dole a zdroj vpravo dole (stejně jako _legenda_a_zdroj, jen na vyšším plátně)
x = X_FIRMA + 3
for nazev, barva in (("Anthropic", pg.ZELENA), ("Ostatní firmy", pg.FIALOVA)):
    plna.add_patch(FancyBboxPatch((x, LEGENDA_Y - pg.CTVEREC / 2), pg.CTVEREC, pg.CTVEREC,
                                  boxstyle="round,pad=0,rounding_size=3", facecolor=barva, edgecolor="none"))
    t = text(x + pg.CTVEREC + 13, LEGENDA_Y, nazev, 24.5, pg.TEXT_TMAVY, va="center_baseline")
    x += pg.CTVEREC + 13 + t.get_window_extent(renderer=fig.canvas.get_renderer()).width + 37
text(X_KONEC + 60, LEGENDA_Y, "Graf: Portu, zdroj: Fiscal.ai", 21.5, pg.TEXT_SEDY, ha="right", va="center_baseline")

fig.savefig(ZAKLAD + ".png", dpi=pg.DPI, facecolor=pg.POZADI)

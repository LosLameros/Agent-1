"""České dividendy vs. WOOD PX ETF – srovnávací tabulka v Portu vzhledu.

Data: převzato 1:1 z podkladové tabulky. Kontrola: banky a pojišťovny 52 % = Komerční banka 20 + Moneta 18 +
Vienna Insurance Group 9 + Erste 5 z tabulky složení portfolia (vystupy/grafy/2026-11-25-slozeni-portfolia.csv).
Bez nadpisu a podnadpisu (tabulka se vkládá pod vlastní nadpis), s minimálními okraji nahoře a dole; záhlaví
sloupců je větším písmem než text tabulky.
Uloženo velmi ostře: PNG ve trojnásobném rozlišení (3600 px na šířku) a vektorové SVG (písmo převedené na křivky).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-25-ceske-dividendy-vs-wood.py
"""
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["svg.fonttype"] = "path"  # SVG nezávislé na nainstalovaném písmu
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-25-ceske-dividendy-vs-wood"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
MEDIUM = font_manager.FontProperties(fname=F + "-Medium.ttf")
SEMIBOLD = font_manager.FontProperties(fname=F + "-SemiBold.ttf")

TEXT = "#202020"
CARA = "#E7E7EB"
W, DPI = 1200, 200           # rozvržení v bodech jako u ostatních tabulek
VYSTUP_DPI = 600             # uložení ve trojnásobném rozlišení → 3600 px
PT = DPI / 72

radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))

L, P = 30, 1170
X_PARAMETR, X_A, X_B = L + 28, 400, 790
SIRKA_SLOUPCE = 340
PISMO, RADKOVANI, VYPLN = 21, 31, 24


def zalom(textu):
    """Zalomí text na řádky podle šířky v px; nezlomitelná mezera za jednopísmenným předložkou/spojkou."""
    slova = textu.split()
    radky_textu, aktualni = [], ""
    for slovo in slova:
        zkus = f"{aktualni} {slovo}".strip()
        if aktualni and pg._sirka_textu(zkus, PISMO, REGULAR) > SIRKA_SLOUPCE:
            radky_textu.append(aktualni)
            aktualni = slovo
        else:
            aktualni = zkus
    radky_textu.append(aktualni)
    return radky_textu


zalomene = [(zalom(r["ceske_dividendy"]), zalom(r["wood_px_etf"])) for r in radky]
vysky = [2 * VYPLN + RADKOVANI * max(len(a), len(b)) - (RADKOVANI - PISMO) for a, b in zalomene]

Y_HL, VYSKA_HL = 12, 62
Y_PRVNI = Y_HL + VYSKA_HL + 4
H = Y_PRVNI + sum(vysky) + 50
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


ax.add_patch(FancyBboxPatch((L, Y_HL), P - L, VYSKA_HL, boxstyle="round,pad=0,rounding_size=7",
                            facecolor=pg.FIALOVA, edgecolor="none"))
for x, nazev in ((X_A, "České dividendy"), (X_B, "WOOD PX ETF")):
    text(x, Y_HL + VYSKA_HL / 2, nazev, 28, "white", SEMIBOLD, va="center_baseline")

y = Y_PRVNI
for r, (a, b), v in zip(radky, zalomene, vysky):
    ax.plot([L, P], [y + v, y + v], color=CARA, linewidth=1.5 / PT, zorder=1)
    horni = y + VYPLN + PISMO * 0.78
    text(X_PARAMETR, horni, r["parametr"], PISMO, TEXT, MEDIUM, va="baseline")
    for x, radky_bunky in ((X_A, a), (X_B, b)):
        for k, s in enumerate(radky_bunky):
            text(x, horni + k * RADKOVANI, s, PISMO, TEXT, REGULAR, va="baseline")
    y += v

text(P, y + 34, "Tabulka: Portu", 17, pg.TEXT_SEDY, REGULAR, ha="right", va="baseline")
fig.savefig(ZAKLAD + ".png", dpi=VYSTUP_DPI, facecolor="white")
fig.savefig(ZAKLAD + ".svg", facecolor="white")

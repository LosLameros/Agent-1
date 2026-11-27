"""Mzdové náklady v automobilovém sektoru – průměrné hodinové náklady práce v eurech a poměr k Německu. Tabulka Portu.

Data: převzato 1:1 z předlohy (zdroj Kielský institut pro světové hospodářství, IfW), hodnoty přibližné.
Kontrola poměrů: 42/65 = 65 %, 23/65 = 35 %, 20–21/65 = 31–32 %.
Výchozí podoba tabulek: bez nadpisu, minimální okraje, větší záhlaví, PNG 3600 px + SVG s písmem v křivkách.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-27-mzdove-naklady-auta.py
"""
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["svg.fonttype"] = "path"  # SVG nezávislé na nainstalovaném písmu
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-27-mzdove-naklady-auta"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
SEMIBOLD = font_manager.FontProperties(fname=F + "-SemiBold.ttf")

TEXT = "#202020"
CARA = "#E7E7EB"
FIALOVA_SVETLA = "#ECEBF8"   # podklad zvýrazněného řádku
PRUH_SVETLY = "#D3CFF2"      # pruhy ostatních zemí
W, DPI = 1200, 200
VYSTUP_DPI = 600             # → 3600 px na šířku
PT = DPI / 72

radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))

RADEK = 60
Y_HL, VYSKA_HL = 12, 62
Y_PRVNI = Y_HL + VYSKA_HL + 4
H = Y_PRVNI + len(radky) * RADEK + 50
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


L, P = 30, 1170
X_ZEME, X_NAKLADY = L + 28, 640
X_PRUH, KONEC_PRUHU, X_POMER = 700, 1040, P - 26

ax.add_patch(FancyBboxPatch((L, Y_HL), P - L, VYSKA_HL, boxstyle="round,pad=0,rounding_size=7",
                            facecolor=pg.FIALOVA, edgecolor="none"))
stred_hl = Y_HL + VYSKA_HL / 2
for x, nazev, zarovnani in ((X_ZEME, "Země", "left"), (X_NAKLADY, "Hodinové náklady práce", "right"),
                            (X_PRUH, "Poměr k Německu", "left")):
    text(x, stred_hl, nazev, 28, "white", SEMIBOLD, ha=zarovnani, va="center_baseline")

y = Y_PRVNI
for r in radky:
    zvyraznit = r["zvyraznit"] == "1"
    if zvyraznit:
        ax.add_patch(Rectangle((L, y), P - L, RADEK, facecolor=FIALOVA_SVETLA, edgecolor="none", zorder=0))
    ax.plot([L, P], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    barva = pg.FIALOVA if zvyraznit else TEXT
    text(X_ZEME, stred, r["zeme"], 21, barva, SEMIBOLD if zvyraznit else REGULAR, va="center_baseline")
    text(X_NAKLADY, stred, r["naklady_text"], 21, barva, SEMIBOLD, ha="right", va="center_baseline")
    delka = (KONEC_PRUHU - X_PRUH) * float(r["pomer_pct"]) / 100
    ax.add_patch(FancyBboxPatch((X_PRUH, stred - 11), delka, 22, boxstyle="round,pad=0,rounding_size=3",
                                facecolor=pg.FIALOVA if zvyraznit else PRUH_SVETLY, edgecolor="none", zorder=2))
    text(X_POMER, stred, r["pomer_text"], 21, barva, SEMIBOLD, ha="right", va="center_baseline")
    y += RADEK

text(L, y + 34, "Hodnoty jsou přibližné.", 17, pg.TEXT_SEDY, REGULAR, va="baseline")
text(P, y + 34, "Tabulka: Portu, zdroj: Kielský institut pro světové hospodářství (IfW)", 17, pg.TEXT_SEDY, REGULAR,
     ha="right", va="baseline")
fig.savefig(ZAKLAD + ".png", dpi=VYSTUP_DPI, facecolor="white")
fig.savefig(ZAKLAD + ".svg", facecolor="white")

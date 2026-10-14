"""Meziroční růst zisků S&P 500 ve 3. čtvrtletí 2026 – verze v barvách ZFP akademie.

Rozvržení 1:1 podle podkladového grafu (1920 × 1032 px). Změněné jsou jen barvy a písmo:
- barvy ZFP akademie (zfpa.cz): oranžová #ED6D09 (logo), šedá #9C9C9C (šedá z webu ZFPA;
  šedá z loga #D6D6D6 je na bílém pozadí příliš světlá), popisky šedých sloupců tmavší
  #6F6F6F kvůli čitelnosti, téměř černá #0F0F0F
  místo tmavě modré Portu v nadpisu,
- písmo: Fedra Sans Pro (písmo ZFPA), když jsou jeho soubory v podklady/zfpa-pismo/
  (FedraSansPro-Normal/Medium/Demi/Bold.otf nebo .ttf); jinak zástupné Fira Sans.
Data: podkladový graf (zdroj FactSet), uložená v CSV vedle skriptu.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-14-zisky-sp500-3q2026-zfpa.py
"""
import csv
import glob
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyBboxPatch, PathPatch  # noqa: E402
from matplotlib.path import Path  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-14-zisky-sp500-3q2026-zfpa"
W, H, DPI = 1920, 1032, 200
PT = DPI / 72

ORANZOVA = "#ED6D09"
SEDA = "#9C9C9C"
SEDA_POPISEK = "#6F6F6F"  # tmavší šedá pro popisky hodnot, #9C9C9C je na bílé málo čitelná
NADPIS = "#0F0F0F"
TEXT = "#202020"
LEGENDA = "#2B2B2B"
OSA = "#5D5D5D"
ZDROJ = "#3D3D3D"
MRIZKA = "#DEDEDE"


# --- písmo: Fedra Sans Pro, když je k dispozici, jinak Fira Sans --------------
def pismo(*vzory):
    for vzor in vzory:
        nalez = sorted(glob.glob(vzor))
        if nalez:
            return font_manager.FontProperties(fname=nalez[0])
    raise FileNotFoundError(vzory)


F = "podklady/zfpa-pismo/FedraSans*"
FIRA = "nastroje/fonty/fira/FiraSans-"
FEDRA = bool(glob.glob(F + "*"))
REGULAR = pismo(F + "*Normal.*", F + "*Book.*", FIRA + "Regular.ttf")
MEDIUM = pismo(F + "*Medium.*", FIRA + "Medium.ttf")
DEMI = pismo(F + "*Demi.*", FIRA + "SemiBold.ttf")
BOLD = pismo(F + "*Bold.*", FIRA + "Bold.ttf")

# --- data ---------------------------------------------------------------------
kategorie, aktualni, cerven = [], [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        kategorie.append(r["sektor"])
        aktualni.append(float(r["aktualni_odhad_pct"]))
        cerven.append(float(r["odhad_k_30_6_2026_pct"]))

# --- plátno v pixelech (osa y dolů) -------------------------------------------
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


VETSI = 2  # všechna písma o 2 body větší než v podkladu (čitelnost)


def text(x, y, s, px, barva, font, **kw):
    """px = velikost písma v podkladovém grafu; vykreslí se o VETSI bodů větší."""
    return ax.text(x, y, s, fontsize=px / PT + VETSI, color=barva, fontproperties=font, **kw)


def sirka_textu(t):
    return t.get_window_extent(renderer=fig.canvas.get_renderer()).width


def sloupec(x, y_vrch, sirka, vyska, barva, r=4):
    """Sloupec se zaobleným jen horním okrajem – jeden tvar, bez švu."""
    r = min(r, vyska / 2, sirka / 2)
    y0 = y_vrch + vyska
    body = [(x, y0), (x, y_vrch + r), (x, y_vrch), (x + r, y_vrch), (x + sirka - r, y_vrch),
            (x + sirka, y_vrch), (x + sirka, y_vrch + r), (x + sirka, y0), (x, y0)]
    kody = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO,
            Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(body, kody), facecolor=barva, edgecolor="none", zorder=2))


def cislo(v, mista=1):
    return f"{v:.{mista}f}".replace(".", ",") + " %"


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

os.makedirs(os.path.dirname(ZAKLAD), exist_ok=True)
fig.savefig(ZAKLAD + ".png", dpi=DPI, facecolor="white")
print("písmo:", "Fedra Sans Pro" if FEDRA else "Fira Sans (zástupné)")

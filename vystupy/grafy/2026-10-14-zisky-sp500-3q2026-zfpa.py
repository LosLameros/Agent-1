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


def text(x, y, s, px, barva, font, **kw):
    ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


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
for x, barva, popis in ((33, ORANZOVA, "Aktuální odhad"), (308, SEDA, "Odhad k 30. 6. 2026")):
    ax.add_patch(FancyBboxPatch((x, 117), 18, 18, boxstyle="round,pad=0,rounding_size=3",
                                facecolor=barva, edgecolor="none"))
    text(x + 32, 126, popis, 23, LEGENDA, MEDIUM, va="center_baseline")

# osa y a mřížka: 0 % na y = 863, 25 % = 132 px
NULA, KROK_PX = 863.5, 132
LEVA, PRAVA = 92, 1890
for i, hodnota in enumerate(range(0, 126, 25)):
    y = NULA - i * KROK_PX
    ax.plot([LEVA, PRAVA], [y, y], color=MRIZKA, linewidth=2 / PT * 72 / 72, zorder=1)
    text(76, y, f"{hodnota} %", 21, OSA, REGULAR, ha="right", va="center_baseline")

# sloupce: dvojice 61 px + mezera 6 px, rozteč 150 px, první začíná na x = 104
SIRKA, MEZERA, ROZTEC, START = 61, 6, 149.8, 104
for k, (kat, a, c) in enumerate(zip(kategorie, aktualni, cerven)):
    x0 = START + k * ROZTEC
    for x, hodnota, barva, popisek in ((x0, a, ORANZOVA, ORANZOVA), (x0 + SIRKA + MEZERA, c, SEDA, SEDA_POPISEK)):
        vyska = hodnota / 25 * KROK_PX
        sloupec(x, NULA - vyska, SIRKA, vyska, barva)
        text(x + SIRKA / 2, NULA - vyska - 12, cislo(hodnota), 18, popisek, BOLD, ha="center", va="baseline", zorder=3)
    stred = x0 + SIRKA + MEZERA / 2
    je_index = kat == "S&P 500"
    radky = kat.split(" ", 1) if (" " in kat and len(kat) > 10 and not je_index) else [kat]
    for j, radek in enumerate(radky):
        text(stred, 911 + j * 29, radek, 21.5, NADPIS if je_index else TEXT, BOLD if je_index else MEDIUM,
             ha="center", va="baseline")

# zdroj
text(32, 1003, "Zdroj: FactSet, vytvořeno AI", 26, ZDROJ, MEDIUM, va="baseline")

os.makedirs(os.path.dirname(ZAKLAD), exist_ok=True)
fig.savefig(ZAKLAD + ".png", dpi=DPI, facecolor="white")
print("písmo:", "Fedra Sans Pro" if FEDRA else "Fira Sans (zástupné)")

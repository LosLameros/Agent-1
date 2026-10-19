"""Grafy ve stylu ZFP akademie (barvy a písmo ZFPA, rozvržení podle grafu zisků S&P 500).

Plátno 1920 × 1032 px (200 dpi) se souřadnicemi v pixelech (osa y dolů), nadpis vlevo nahoře,
zdroj vlevo dole, sloupce se zaobleným vrškem, hodnoty tučně v barvě sloupce.
- barvy ZFP akademie (zfpa.cz): oranžová #ED6D09 (logo), šedá #9C9C9C (šedá z webu ZFPA;
  šedá z loga #D6D6D6 je na bílém pozadí příliš světlá), popisky šedých sloupců tmavší
  #6F6F6F kvůli čitelnosti, téměř černá #0F0F0F na nadpis,
- písmo: Fedra Sans Pro (písmo ZFPA), když jsou jeho soubory v podklady/zfpa-pismo/
  (FedraSansPro-Normal/Medium/Demi/Bold.otf nebo .ttf; komerční, do gitu nepatří);
  jinak zástupné Fira Sans,
- všechna písma jsou o VETSI bodů větší než v podkladovém grafu (čitelnost).

Použití: viz vystupy/grafy/2026-10-14-*-zfpa.py
"""
import glob
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import PathPatch  # noqa: E402
from matplotlib.path import Path  # noqa: E402

W, H, DPI = 1920, 1032, 200
PT = DPI / 72
VETSI = 2

ORANZOVA = "#ED6D09"
SEDA = "#9C9C9C"
SEDA_POPISEK = "#6F6F6F"
NADPIS = "#0F0F0F"
TEXT = "#202020"
LEGENDA = "#2B2B2B"
OSA = "#5D5D5D"
ZDROJ = "#3D3D3D"
MRIZKA = "#DEDEDE"
NULOVA_CARA = "#B4B4B4"
POZADI_RAMECKU = "#F5F5F5"


def _pismo(*vzory):
    for vzor in vzory:
        nalez = sorted(glob.glob(vzor))
        if nalez:
            return font_manager.FontProperties(fname=nalez[0])
    raise FileNotFoundError(vzory)


_F = "podklady/zfpa-pismo/FedraSans*"
_FIRA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonty", "fira", "FiraSans-")
FEDRA = bool(glob.glob(_F + "*"))
REGULAR = _pismo(_F + "*Normal.*", _F + "*Book.*", _FIRA + "Regular.ttf")
MEDIUM = _pismo(_F + "*Medium.*", _FIRA + "Medium.ttf")
DEMI = _pismo(_F + "*Demi.*", _FIRA + "SemiBold.ttf")
BOLD = _pismo(_F + "*Bold.*", _FIRA + "Bold.ttf")


def platno():
    fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(H, 0)
    ax.axis("off")
    return fig, ax


def text(ax, x, y, s, px, barva, font, **kw):
    """px = velikost písma v podkladovém grafu; vykreslí se o VETSI bodů větší."""
    return ax.text(x, y, s, fontsize=px / PT + VETSI, color=barva, fontproperties=font, **kw)


def sirka_textu(ax, t):
    return t.get_window_extent(renderer=ax.figure.canvas.get_renderer()).width


def vyska_textu(ax, t):
    return t.get_window_extent(renderer=ax.figure.canvas.get_renderer()).height


def sloupec(ax, x, y_nula, sirka, vyska_px, barva, r=4):
    """Sloupec od y_nula; kladná výška nahoru, záporná dolů. Zaoblený je jen volný konec – jeden tvar, bez švu."""
    v = abs(vyska_px)
    r = min(r, v / 2, sirka / 2)
    s = -1 if vyska_px >= 0 else 1  # směr od nuly (osa y míří dolů)
    konec = y_nula + s * v
    body = [(x, y_nula), (x, konec - s * r), (x, konec), (x + r, konec), (x + sirka - r, konec),
            (x + sirka, konec), (x + sirka, konec - s * r), (x + sirka, y_nula), (x, y_nula)]
    kody = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO,
            Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(body, kody), facecolor=barva, edgecolor="none", zorder=2))


def cislo(v, mista=1):
    """Český formát: desetinná čárka, pravé minus, pevná mezera před %."""
    t = f"{abs(v):.{mista}f}".replace(".", ",")
    return ("−" if v < 0 and float(t.replace(",", ".")) != 0 else "") + t + " %"


def uloz(fig, cesta):
    os.makedirs(os.path.dirname(os.path.abspath(cesta)), exist_ok=True)
    fig.savefig(cesta, dpi=DPI, facecolor="white")
    plt.close(fig)
    print("písmo:", "Fedra Sans Pro" if FEDRA else "Fira Sans (zástupné)")

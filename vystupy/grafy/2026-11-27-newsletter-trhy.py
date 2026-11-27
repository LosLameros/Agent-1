"""Přehled trhů za týden – tabulka do newsletteru podle předlohy redakce, s písmem o 2 body větším.

Data: týdenní podklad (tabulka od redakce), uložená v CSV vedle skriptu; u Nikkei opravena měna JPN → JPY.
Vzhled podle předlohy: fialová hlavička přes celou šířku s bílým textem, ikonky (vlajky a symboly) u názvů, číselné
sloupce na střed, pruhované řádky, změny zeleně / červeně, nula tmavě. Ikonky jsou z písma Noto Color Emoji (licence OFL).
Písmo oproti předloze o 2 body větší (čitelnost na mobilu), ostrý výstup PNG 3600 px + SVG.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-27-newsletter-trhy.py
"""
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
plt.rcParams["svg.fonttype"] = "path"  # SVG nezávislé na nainstalovaném písmu
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-27-newsletter-trhy"
F = "nastroje/fonty/RethinkSans"
REGULAR = font_manager.FontProperties(fname=F + ".ttf")
SEMIBOLD = font_manager.FontProperties(fname=F + "-SemiBold.ttf")
EMOJI_PISMO = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

TEXT = "#202020"
SEDA_PRUH = "#F4F4F7"
CARA = "#E7E7EB"
ZAPORNA = "#BE0000"
W, DPI = 1200, 200
PT = DPI / 72
VETSI = 2 * PT  # písmo o 2 body větší než v předloze

IKONY = {"S&P 500": "🇺🇸", "Nasdaq-100": "🇺🇸", "Euro Stoxx 50": "🇪🇺", "Nikkei 225": "🇯🇵", "CSI 300": "🇨🇳",
         "PX": "🇨🇿", "Zlato": "💰", "Bitcoin": "📊", "Portu Portfolio 10": "🌍", "EUR/CZK": "💶", "USD/CZK": "💵"}


def emoji_obrazek(znak):
    """Barevná ikonka z Noto Color Emoji jako RGBA pole (písmo má jen bitmapy 109 px)."""
    pismo = ImageFont.truetype(EMOJI_PISMO, 109)
    platno = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(platno).text((10, 10), znak, font=pismo, embedded_color=True)
    return np.asarray(platno.crop(platno.getbbox()))


radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))
RADEK = 66
VYSKA_HL = 66
H = VYSKA_HL + len(radky) * RADEK + 4
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, px, barva, font, **kw):
    return ax.text(x, y, s, fontsize=px / PT, color=barva, fontproperties=font, **kw)


SLOUPCE = [0, 300, 525, 735, 970, W]                  # hranice sloupců
STREDY = [(a + b) / 2 for a, b in zip(SLOUPCE[1:], SLOUPCE[2:])]

ax.add_patch(Rectangle((0, 0), W, VYSKA_HL, facecolor=pg.FIALOVA, edgecolor="none"))
for x in SLOUPCE[1:-1]:  # jemné dělení sloupců v hlavičce jako v předloze
    ax.plot([x, x], [0, VYSKA_HL], color="white", alpha=0.25, linewidth=1.2 / PT)
text(18, VYSKA_HL / 2, "Index", 22 + VETSI, "white", SEMIBOLD, va="center_baseline")
for x, nazev in zip(STREDY, ("Hodnota", "Měna", "Týdenní změna", "Výnos YTD")):
    text(x, VYSKA_HL / 2, nazev, 22 + VETSI, "white", SEMIBOLD, ha="center", va="center_baseline")


def zmena(v):
    return pg.cislo(v, 1, "%")


y = VYSKA_HL
for i, r in enumerate(radky):
    if i % 2:
        ax.add_patch(Rectangle((0, y), W, RADEK, facecolor=SEDA_PRUH, edgecolor="none", zorder=0))
    ax.plot([0, W], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    ikona = emoji_obrazek(IKONY[r["nazev"]])
    # ikonky různé šířky (vlajka × pytel peněz) vystředit do stejného pole, ať názvy začínají pod sebou
    POLE, VYSKA_IKONY = 46, 30
    sirka_ikony = min(VYSKA_IKONY * ikona.shape[1] / ikona.shape[0], POLE)
    vyska_ikony = sirka_ikony * ikona.shape[0] / ikona.shape[1]
    x0 = 18 + (POLE - sirka_ikony) / 2
    stred_ikony = stred + 3  # opticky na střed s písmem
    ax.imshow(ikona, extent=(x0, x0 + sirka_ikony, stred_ikony + vyska_ikony / 2, stred_ikony - vyska_ikony / 2),
              zorder=3, interpolation="lanczos")
    text(18 + POLE + 14, stred, r["nazev"], 23 + VETSI, TEXT, SEMIBOLD, va="center_baseline", zorder=2)
    hodnota = pg.cislo(float(r["hodnota"]), int(r["mista"])) if r["hodnota"] else "–"
    text(STREDY[0], stred, hodnota, 23 + VETSI, TEXT, REGULAR, ha="center", va="center_baseline", zorder=2)
    text(STREDY[1], stred, r["mena"] or "–", 23 + VETSI, TEXT, REGULAR, ha="center", va="center_baseline", zorder=2)
    for x, klic in ((STREDY[2], "tydenni_zmena_pct"), (STREDY[3], "vynos_ytd_pct")):
        v = float(r[klic])
        text(x, stred, zmena(v), 23 + VETSI, ZAPORNA if v < 0 else pg.ZELENA if v > 0 else TEXT, REGULAR,
             ha="center", va="center_baseline", zorder=2)
    y += RADEK

ax.set_aspect("auto")
fig.savefig(ZAKLAD + ".png", dpi=600, facecolor="white")
fig.savefig(ZAKLAD + ".svg", facecolor="white")

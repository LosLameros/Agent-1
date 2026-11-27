"""Přehled trhů za týden – tabulka do newsletteru přesně podle předlohy redakce, jen s písmem o 1 bod větším.

Data: týdenní podklad (tabulka od redakce), uložená v CSV vedle skriptu; u Nikkei opravena měna JPN → JPY.
Rozvržení 1:1 podle předlohy: 2000 × 736 px, hlavička 78 px, 11 řádků po ≈ 59,8 px, hranice sloupců 388 / 808 /
1215 / 1625 px, číselné sloupce na střed, pruhované řádky, ikonky u názvů (Noto Color Emoji, licence OFL),
prázdné buňky „/“. Písmo předlohy má výšku číslic 22 px, což v Rethink Sans odpovídá ≈ 31,5 px; tady o 1 bod větší
(1 bod = 200/72 px při 200 dpi), výška číslic ≈ 24 px.
Výstup ve stejném rozlišení jako předloha (2000 × 736 px), vykreslený ostře z vektorů, plus SVG.
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
CARA = "#E3E3E8"
ZAPORNA = "#C8102E"
W, H, DPI = 2000, 736, 200   # stejné rozlišení jako předloha
PT = DPI / 72
PISMO = 31.5 + 1 * PT        # stejná výška číslic jako v předloze (22 px) + 1 bod

IKONY = {"S&P 500": "🇺🇸", "Nasdaq-100": "🇺🇸", "Euro Stoxx 50": "🇪🇺", "Nikkei 225": "🇯🇵", "CSI 300": "🇨🇳",
         "PX": "🇨🇿", "Zlato": "💰", "Bitcoin": "📊", "Portu Portfolio 10": "🌍", "EUR/CZK": "💶", "USD/CZK": "💵"}


def emoji_obrazek(znak):
    """Barevná ikonka z Noto Color Emoji jako RGBA pole (písmo má jen bitmapy 109 px)."""
    pismo = ImageFont.truetype(EMOJI_PISMO, 109)
    platno = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(platno).text((10, 10), znak, font=pismo, embedded_color=True)
    return np.asarray(platno.crop(platno.getbbox()))


radky = list(csv.DictReader(open(ZAKLAD + ".csv", encoding="utf-8")))
VYSKA_HL = 78
RADEK = (H - VYSKA_HL) / len(radky)
fig = plt.figure(figsize=(W / DPI, H / DPI), dpi=DPI, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(H, 0)
ax.axis("off")


def text(x, y, s, barva, font, **kw):
    return ax.text(x, y, s, fontsize=PISMO / PT, color=barva, fontproperties=font, **kw)


SLOUPCE = [0, 388, 808, 1215, 1625, W]
STREDY = [(a + b) / 2 for a, b in zip(SLOUPCE[1:], SLOUPCE[2:])]

ax.add_patch(Rectangle((0, 0), W, VYSKA_HL, facecolor=pg.FIALOVA, edgecolor="none"))
for x in SLOUPCE[1:-1]:  # jemné dělení sloupců v hlavičce jako v předloze
    ax.plot([x, x], [0, VYSKA_HL], color="white", alpha=0.18, linewidth=1.5 / PT)
text(20, VYSKA_HL / 2, "Index", "white", SEMIBOLD, va="center_baseline")
for x, nazev in zip(STREDY, ("Hodnota", "Měna", "Týdenní změna", "Výnos YTD")):
    text(x, VYSKA_HL / 2, nazev, "white", SEMIBOLD, ha="center", va="center_baseline")

y = VYSKA_HL
for i, r in enumerate(radky):
    if i % 2:
        ax.add_patch(Rectangle((0, y), W, RADEK, facecolor=SEDA_PRUH, edgecolor="none", zorder=0))
    ax.plot([0, W], [y + RADEK, y + RADEK], color=CARA, linewidth=1.5 / PT, zorder=1)
    stred = y + RADEK / 2
    # ikonky různé šířky vystředit do stejného pole, ať názvy začínají pod sebou
    ikona = emoji_obrazek(IKONY[r["nazev"]])
    POLE, VYSKA_IKONY = 38, 27
    sirka_ikony = min(VYSKA_IKONY * ikona.shape[1] / ikona.shape[0], POLE)
    vyska_ikony = sirka_ikony * ikona.shape[0] / ikona.shape[1]
    x0 = 18 + (POLE - sirka_ikony) / 2
    ax.imshow(ikona, extent=(x0, x0 + sirka_ikony, stred + 5 + vyska_ikony / 2, stred + 5 - vyska_ikony / 2),
              zorder=3, interpolation="lanczos")
    text(18 + POLE + 12, stred, r["nazev"], TEXT, SEMIBOLD, va="center_baseline", zorder=2)
    hodnota = pg.cislo(float(r["hodnota"]), int(r["mista"])) if r["hodnota"] else "/"
    text(STREDY[0], stred, hodnota, TEXT, REGULAR, ha="center", va="center_baseline", zorder=2)
    text(STREDY[1], stred, r["mena"] or "/", TEXT, REGULAR, ha="center", va="center_baseline", zorder=2)
    for x, klic in ((STREDY[2], "tydenni_zmena_pct"), (STREDY[3], "vynos_ytd_pct")):
        v = float(r[klic])
        text(x, stred, pg.cislo(v, 1, "%"), ZAPORNA if v < 0 else pg.ZELENA if v > 0 else TEXT, REGULAR,
             ha="center", va="center_baseline", zorder=2)
    y += RADEK

ax.set_aspect("auto")
fig.savefig(ZAKLAD + ".png", dpi=DPI, facecolor="white")
fig.savefig(ZAKLAD + ".svg", facecolor="white")

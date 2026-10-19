"""Anualizovaný růst americké ekonomiky (2Q 2021 – 2Q 2026) – styl ZFP akademie.

Data: U.S. Bureau of Economic Analysis přes FRED – reálný HDP, anualizovaná mezičtvrtletní
změna, sezónně očištěno (A191RL1Q225SBEA). Pro kontrolu je v CSV i meziroční růst
(A191RO1Q156NBEA) – ten zobrazoval podkladový graf, přestože se jmenoval „anualizovaný“.
Styl: nastroje/zfpa_grafy.py (barvy a písmo ZFPA, písma o 2 body větší než v podkladu).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-14-hdp-usa-anualizovany-zfpa.py
"""
import csv
import sys

from matplotlib.patches import Rectangle

sys.path.insert(0, "nastroje")
import zfpa_grafy as z  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-14-hdp-usa-anualizovany-zfpa"

ctvrtleti, hodnoty = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        ctvrtleti.append(r["ctvrtleti"])
        hodnoty.append(float(r["anualizovany_rust_qoq_pct"]))

fig, ax = z.platno()


def text(*args, **kw):
    return z.text(ax, *args, **kw)


# nadpis
text(32, 74, "Anualizovaný růst americké ekonomiky", 44, z.NADPIS, z.REGULAR, va="baseline")

# vysvětlující rámeček: světle šedé pozadí, oranžový pruh vlevo, tučný úvod + text se zalomením
RAM_X, RAM_Y, RAM_W = 32, 104, 1856
UVOD = "Co znamená anualizovaný růst?"
VYSVETLENI = ("Vyjadřuje, jakým tempem by ekonomika vzrostla za celý rok, pokud by si během všech "
              "4 čtvrtletí udržela stejnou rychlost mezičtvrtletního růstu. Umožňuje tak snáze "
              "porovnávat krátkodobý vývoj s ročními cíli.")
RADEK, PISMO_RAM, ODSAZENI = 36, 21, 30
x_text, y_text = RAM_X + ODSAZENI, RAM_Y + 44
t = text(x_text, y_text, UVOD, PISMO_RAM, z.TEXT, z.BOLD, va="baseline", zorder=3)
x = x_text + z.sirka_textu(ax, t) + 10
radky = 1
for slovo in VYSVETLENI.split():
    t = text(x, y_text, slovo, PISMO_RAM, z.TEXT, z.REGULAR, va="baseline", zorder=3)
    sirka = z.sirka_textu(ax, t)
    if x + sirka > RAM_X + RAM_W - ODSAZENI:  # zalomit na další řádek
        y_text += RADEK
        x = x_text
        radky += 1
        t.set_position((x, y_text))
    x += sirka + z.sirka_textu(ax, text(0, -100, "a a", PISMO_RAM, z.TEXT, z.REGULAR)) \
        - 2 * z.sirka_textu(ax, text(0, -100, "a", PISMO_RAM, z.TEXT, z.REGULAR))
RAM_H = 44 + (radky - 1) * RADEK + 26
ax.add_patch(Rectangle((RAM_X, RAM_Y), RAM_W, RAM_H, facecolor=z.POZADI_RAMECKU, edgecolor="none", zorder=1))
ax.add_patch(Rectangle((RAM_X, RAM_Y), 6, RAM_H, facecolor=z.ORANZOVA, edgecolor="none", zorder=2))

# osa y: −2 % až 8 %, krok 2 %
NULA, PX_NA_PROCENTO = 735, 56
LEVA, PRAVA = 92, 1890
for hodnota in range(-2, 9, 2):
    y = NULA - hodnota * PX_NA_PROCENTO
    ax.plot([LEVA, PRAVA], [y, y], color=z.NULOVA_CARA if hodnota == 0 else z.MRIZKA,
            linewidth=2 / z.PT, zorder=3 if hodnota == 0 else 1)
    text(76, y, z.cislo(hodnota, 0), 21, z.OSA, z.REGULAR, ha="right", va="center_baseline")

# sloupce: kladné oranžově, záporné šedě
ROZTEC = (PRAVA - LEVA - 12) / len(hodnoty)
SIRKA = 56
for i, (q, h) in enumerate(zip(ctvrtleti, hodnoty)):
    barva = z.ORANZOVA if h >= 0 else z.SEDA
    x = LEVA + 6 + i * ROZTEC + (ROZTEC - SIRKA) / 2
    vyska = h * PX_NA_PROCENTO
    z.sloupec(ax, x, NULA, SIRKA, vyska, barva)
    if h >= 0:
        text(x + SIRKA / 2, NULA - vyska - 12, z.cislo(h), 18, z.ORANZOVA,
             z.BOLD, ha="center", va="baseline", zorder=4)
    else:
        text(x + SIRKA / 2, NULA - vyska + 12, z.cislo(h), 18, z.SEDA_POPISEK,
             z.BOLD, ha="center", va="top", zorder=4)

# popisky osy x: čtvrtletí malým písmem pod sloupcem, rok vycentrovaný pod svými čtvrtletími
Y_OSA = NULA + 2 * PX_NA_PROCENTO
roky = {}
for i, q in enumerate(ctvrtleti):
    stred = LEVA + 6 + i * ROZTEC + ROZTEC / 2
    text(stred, Y_OSA + 40, q.split()[0], 18, z.OSA, z.REGULAR, ha="center", va="baseline")
    roky.setdefault(q.split()[1], []).append(stred)
for i, (rok, stredy) in enumerate(roky.items()):
    text(sum(stredy) / len(stredy), Y_OSA + 82, rok, 21.5, z.TEXT, z.MEDIUM, ha="center", va="baseline")
    if i:  # tenká dělicí čára mezi roky
        x = stredy[0] - ROZTEC / 2
        ax.plot([x, x], [Y_OSA + 14, Y_OSA + 90], color=z.MRIZKA, linewidth=2 / z.PT)

# zdroj
text(32, 1003, "Zdroj: U.S. Bureau of Economic Analysis, vytvořeno AI", 26, z.ZDROJ, z.MEDIUM, va="baseline")

z.uloz(fig, ZAKLAD + ".png")

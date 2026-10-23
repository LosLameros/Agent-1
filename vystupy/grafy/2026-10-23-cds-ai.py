"""Úvěrové riziko v AI: pětileté CDS hyperscalerů a výrobců čipů (8/2025 – 20. 10. 2026), bazické body.

Data: PŘIBLIŽNÉ hodnoty odečtené z grafu Bloomberg „Credit Risk Rises in AI Ecosystem“ (zdroj ICE Data
Services) – ICE data nejsou veřejně dostupná. Křivky odečtené po pixelech (≈ 2 dny na pixel), kalibrace
podle mřížky 100/200/300 b. b. a značek měsíců; přesnost zhruba ±3 b. b. Kde je čára v originálu schovaná
pod jinou (AMD a Nvidia v hustém shluku dole), je hodnota dopočítaná lineárně mezi viditelnými úseky.
Devět řad je výjimka z pravidla „nejvýš dvě řady“ (výslovné přání) – zvýrazněný Oracle (fialová) a SpaceX
(zelená), ostatní v odvozených odstínech; jména firem jsou u konců čar.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-23-cds-ai.py [cs|sk]
"""
import csv
import datetime as dt
import sys

import matplotlib.dates as mdates
import matplotlib.ticker
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-23-cds-ai"

RADY = [  # (sloupec v CSV, název, barva čáry, barva popisku) – odshora podle poslední hodnoty
    ("oracle", "Oracle", pg.FIALOVA, pg.FIALOVA),
    ("spacex", "SpaceX", pg.ZELENA, pg.ZELENA),
    ("broadcom", "Broadcom", pg.SVETLE_ZELENA, "#3DAA62"),
    ("meta", "Meta", pg.SVETLE_FIALOVA, "#7C76D6"),
    ("nvidia", "Nvidia", pg.TMAVE_SEDA, pg.TMAVE_SEDA),
    ("amd", "AMD", pg.SEDA, "#8A8C99"),
    ("amazon", "Amazon", "#2E2880", "#2E2880"),
    ("alphabet", "Alphabet", "#006B26", "#006B26"),
    ("microsoft", "Microsoft", "#C9CAD3", "#9C9EAB"),
]

datumy, hodnoty = [], {s: [] for s, *_ in RADY}
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["datum"]))
        for s, *_ in RADY:
            hodnoty[s].append(float(r[s]) if r[s] else None)

TEXTY = {
    "cs": {"nadpis": "Úvěrové riziko v AI roste",
           "podnadpis": "Cena pětiletého pojištění proti nesplácení dluhu (CDS) v bazických bodech",
           "zdroj": "Přibližné hodnoty z grafu Bloombergu. Graf: Portu, zdroj: ICE Data Services"},
    "sk": {"nadpis": "Úverové riziko v AI rastie",
           "podnadpis": "Cena päťročného poistenia proti nesplácaniu dlhu (CDS) v bázických bodoch",
           "zdroj": "Približné hodnoty z grafu Bloombergu. Graf: Portu, zdroj: ICE Data Services"},
}
jazyk = sys.argv[1] if len(sys.argv) > 1 else "cs"  # python3 … sk → slovenská verze (soubor …-sk.png)
T = TEXTY[jazyk]

PODNADPIS_PX = 44
DOLNI = pg.GRAF_DOLNI_1RADEK - 38  # místo na druhý řádek legendy
LEGENDA_Y = (pg.LEGENDA_STRED_Y - 38, pg.LEGENDA_STRED_Y)
OSA = (0, 350, 50)

fig, ax = pg._platno(DOLNI, nadpis=T["nadpis"], navic=PODNADPIS_PX)
vyska, fy = fig._portu["vyska"], fig._portu["fy"]
fig.text(pg._fx(pg.GRAF_LEVA - 80), 1 - 78 / vyska, T["podnadpis"], fontsize=pg.PISMO_LEGENDA, color=pg.TEXT_SEDY,
         va="center")
pg._osa_y(ax, OSA, "", 0)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=2)

for i, (s, _, barva, _) in reversed(list(enumerate(RADY))):  # Oracle a SpaceX navrchu
    ax.plot(datumy, hodnoty[s], color=barva, linewidth=2.5 / pg.PT, solid_joinstyle="round", zorder=3 + len(RADY) - i)

# koncové popisky „Oracle 314“ v barvě řady, blízké hodnoty odsunuté od sebe (min. 25 px)
konce = [[v for v in hodnoty[s] if v is not None][-1] for s, *_ in RADY]
mezera = 25 / (DOLNI - pg.GRAF_HORNI) * (OSA[1] - OSA[0])
poradi = sorted(range(len(konce)), key=lambda k: konce[k])
pozice = {k: konce[k] for k in poradi}
for a, b in zip(poradi, poradi[1:]):
    if pozice[b] - pozice[a] < mezera:
        pozice[b] = pozice[a] + mezera
shluk = [k for k in poradi if konce[k] < 130]  # spodní shluk vyrovnej kolem skutečných hodnot
posun = (sum(pozice[k] for k in shluk) - sum(konce[k] for k in shluk)) / len(shluk)
popisky = []
for k, (_, nazev, _, barva_textu) in enumerate(RADY):
    y = pozice[k] - (posun if k in shluk else 0)
    popisky.append(ax.annotate(f"{nazev} {pg.cislo(konce[k], 0)}", (datumy[-1], y), xytext=(12 / pg.PT, 0),
                               textcoords="offset points", ha="left", va="center", fontsize=pg.PISMO_HODNOTA,
                               color=barva_textu, fontproperties=pg._STREDNI, annotation_clip=False))

ax.set_xlim(datumy[0], datumy[-1])
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
    lambda v, _: f"{pg.MESICE[jazyk][mdates.num2date(v).month - 1]} {mdates.num2date(v).year % 100:02d}"))
for t in ax.get_xticklabels():
    t.set_fontsize(pg.PISMO_OSA)
    t.set_color(pg.TEXT_SEDY)
ax.tick_params(axis="x", pad=29 / pg.PT)

# okraje podle popisků osy y a koncových popisků
renderer = fig.canvas.get_renderer()
fig.canvas.draw()
leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
prava = pg.GRAF_PRAVA - max(t.get_window_extent(renderer).width for t in popisky) - 22
pos = ax.get_position()
ax.set_position([pg._fx(leva), pos.y0, pg._fx(prava - leva), pos.height])

# legenda vlevo dole ve dvou řádcích (6 + 3), zdroj vpravo na spodním řádku
for radek, polozky in zip(LEGENDA_Y, (RADY[:6], RADY[6:])):
    x = pg.GRAF_LEVA + 3
    for _, nazev, barva, _ in polozky:
        fig.patches.append(FancyBboxPatch(
            (pg._fx(x), fy(radek + pg.CTVEREC / 2)), pg._fx(pg.CTVEREC), fy(radek - pg.CTVEREC / 2) - fy(radek + pg.CTVEREC / 2),
            boxstyle="round,pad=0,rounding_size=0.003", transform=fig.transFigure, facecolor=barva, edgecolor="none"))
        t = fig.text(pg._fx(x + pg.CTVEREC + 13), fy(radek), nazev, fontsize=pg.PISMO_LEGENDA, color=pg.TEXT_TMAVY,
                     ha="left", va="center_baseline")
        x += pg.CTVEREC + 13 + t.get_window_extent(renderer=renderer).width + 37
fig.text(pg._fx(pg.GRAF_PRAVA), fy(LEGENDA_Y[1]), T["zdroj"], fontsize=pg.PISMO_ZDROJ, color=pg.TEXT_SEDY,
         ha="right", va="center_baseline")
pg.uloz(fig, ZAKLAD + ("" if jazyk == "cs" else "-" + jazyk) + ".png")

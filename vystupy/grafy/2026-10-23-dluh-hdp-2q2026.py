"""Hrubý dluh vládních institucí v poměru k HDP, 2. čtvrtletí 2026 – státy EU, EU a eurozóna.

Data: Eurostat, gov_10q_ggdebt (sektor S13, ukazatel GD, % HDP), zveřejněno 21. 10. 2026, předběžné
údaje. Eurozóna = 21 zemí (od 2026 včetně Bulharska), EU = 27 zemí.
Zvýraznění: v české verzi Česko, ve slovenské Slovensko, v obou EU a eurozóna (zelená), ostatní fialová.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-23-dluh-hdp-2q2026.py [cs|sk]
"""
import csv
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-23-dluh-hdp-2q2026"

TEXTY = {
    "cs": {"nadpis": "Hrubý dluh vládních institucí v poměru k HDP, 2. čtvrtletí 2026", "podnadpis": "v % HDP",
           "sloupec": "zeme", "domov": "CZ", "ostatni": "Ostatní země", "zvyraznene": "Česko, EU a eurozóna",
           "zdroj": "Předběžné údaje. Graf: Portu, zdroj: Eurostat"},
    "sk": {"nadpis": "Hrubý dlh verejnej správy v pomere k HDP, 2. štvrťrok 2026", "podnadpis": "v % HDP",
           "sloupec": "zeme_sk", "domov": "SK", "ostatni": "Ostatné krajiny", "zvyraznene": "Slovensko, EÚ a eurozóna",
           "zdroj": "Predbežné údaje. Graf: Portu, zdroj: Eurostat"},
}
jazyk = sys.argv[1] if len(sys.argv) > 1 else "cs"  # python3 … sk → slovenská verze (soubor …-sk.png)
T = TEXTY[jazyk]

kody, zeme, hodnoty = [], [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        kody.append(r["kod"])
        zeme.append(r[T["sloupec"]])
        hodnoty.append(float(r["dluh_pct_hdp_2026q2"]))
zvyraznit = [k in (T["domov"], "EU27_2020", "EA21") for k in kody]

PODNADPIS_PX = 36
DOLNI = 528  # místo pod plochou na popisky zemí šikmo
OSA = (0, 160, 20)

fig, ax = pg._platno(DOLNI, nadpis=T["nadpis"], navic=PODNADPIS_PX)
vyska = fig._portu["vyska"]
fig.text(pg._fx(pg.GRAF_LEVA - 80), 1 - 76 / vyska, T["podnadpis"], fontsize=pg.PISMO_LEGENDA, color=pg.FIALOVA,
         fontproperties=pg._STREDNI, va="center")
pg._osa_y(ax, OSA, "", 0)

n = len(zeme)
ax.set_xlim(-0.5, n - 0.5)
barvy = [pg.ZELENA if z else pg.FIALOVA for z in zvyraznit]
ax.bar(range(n), hodnoty, width=0.6, color=barvy, zorder=2, linewidth=0)
odsazeni = 8 / (DOLNI - pg.GRAF_HORNI) * (OSA[1] - OSA[0])
for i, (h, z) in enumerate(zip(hodnoty, zvyraznit)):  # celá čísla (92,5 → 93) – s desetinou by se popisky 29 sloupců slily
    cele = float(Decimal(str(h)).quantize(Decimal("1"), ROUND_HALF_UP))
    ax.text(i, h + odsazeni, pg.cislo(cele, 0), ha="center", va="bottom", fontsize=pg.PISMO_HODNOTA,
            color=pg.TEXT_TMAVY, fontproperties=pg._STREDNI if z else None)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=3)

ax.set_xticks(range(n))
ax.set_xticklabels(zeme, rotation=45, ha="right", rotation_mode="anchor", fontsize=pg.PISMO_OSA)
for t, z in zip(ax.get_xticklabels(), zvyraznit):
    t.set_color(pg.TEXT_TMAVY if z else pg.TEXT_SEDY)
    if z:
        t.set_fontproperties(pg._TUCNE)
        t.set_fontsize(pg.PISMO_OSA)
ax.tick_params(axis="x", pad=14 / pg.PT)

# levý okraj podle popisků osy y
renderer = fig.canvas.get_renderer()
fig.canvas.draw()
leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
pos = ax.get_position()
ax.set_position([pg._fx(leva), pos.y0, pg._fx(pg.GRAF_PRAVA - leva), pos.height])

pg._legenda_a_zdroj(fig, [(T["ostatni"], pg.FIALOVA), (T["zvyraznene"], pg.ZELENA)], T["zdroj"])
pg.uloz(fig, ZAKLAD + ("" if jazyk == "cs" else "-" + jazyk) + ".png")

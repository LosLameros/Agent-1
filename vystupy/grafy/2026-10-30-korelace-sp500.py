"""Rozdělení párových korelací akcií v S&P 500 – současný stav vs. průměr od roku 1995.

Data: SG Cross Asset Research / Equity Quant – podíl ze 124 750 párových kombinací akcií (500 × 499 / 2)
podle 260denní korelace, v %. Hodnoty odečtené z podkladového grafu (sloupce po 0,1 bodu korelace,
přesnost na 0,1 p. b.; součet obou řad 99,4 %). Koše −1,0 až −0,8 jsou v obou řadách nulové, a proto vynechané.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-30-korelace-sp500.py
"""
import csv
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-30-korelace-sp500"

kose, soucasny, prumer = [], [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        kose.append(float(r["korelace"]))
        soucasny.append(float(r["soucasny_stav_pct"]))
        prumer.append(float(r["prumer_od_1995_pct"]))

OSA = (0, 14, 2)
fig, ax = pg._platno(pg.GRAF_DOLNI_1RADEK, nadpis="Vysoký podíl negativní korelace akcií v S&P 500",
                     podnadpis="Rozdělení 124 750 párů akcií podle 260denní korelace, podíl v %")
pg._osa_y(ax, OSA, "%", 0)

n = len(kose)
ax.set_xlim(-0.5, n - 0.5)
SIRKA, MEZERA = 0.34, 0.04  # dva sloupce v koši těsně vedle sebe
for posun, hodnoty, barva in ((-(SIRKA + MEZERA) / 2, soucasny, pg.FIALOVA), ((SIRKA + MEZERA) / 2, prumer, pg.ZELENA)):
    ax.bar([i + posun for i in range(n)], hodnoty, width=SIRKA, color=barva, zorder=2, linewidth=0)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=3)
ax.set_xticks(range(n))
ax.set_xticklabels([pg.cislo(k, 1) for k in kose], fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
ax.tick_params(axis="x", pad=27 / pg.PT)

renderer = fig.canvas.get_renderer()
fig.canvas.draw()
leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
pos = ax.get_position()
ax.set_position([pg._fx(leva), pos.y0, pg._fx(pg.GRAF_PRAVA - leva), pos.height])

pg._legenda_a_zdroj(fig, [("Současný stav", pg.FIALOVA), ("Průměr od roku 1995", pg.ZELENA)],
                    "Graf: Portu, zdroj: SG Cross Asset Research / Equity Quant")
pg.uloz(fig, ZAKLAD + ".png")

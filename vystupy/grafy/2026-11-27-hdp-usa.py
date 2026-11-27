"""USA: anualizovaný růst HDP po čtvrtletích (4Q 2021 – 3Q 2026), v %. Nový design Portu.

Data: Trading Economics (GDP CQOQ, BEA; změna proti předchozímu čtvrtletí přepočtená na roční tempo), stav k 25. 11. 2026.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-27-hdp-usa.py
"""
import csv
import sys

from matplotlib.lines import Line2D

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-27-hdp-usa"
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    r = list(csv.DictReader(f))
roky = [int(x["rok"]) for x in r]
ctvrtleti = [int(x["ctvrtleti"]) for x in r]
hodnoty = [float(x["anualizovany_rust_pct"]) for x in r]

# nejvyšší hodnota od … (hledá zpět první vyšší čtvrtletí)
posledni = hodnoty[-1]
od = next(i for i in range(len(hodnoty) - 2, -1, -1) if hodnoty[i] >= posledni)

OSA = (-2, 8, 1)
VYSKA_PLOCHY = pg.GRAF_DOLNI_2RADKY - pg.GRAF_HORNI
fig, ax = pg._platno(
    pg.GRAF_DOLNI_2RADKY, nadpis="USA: anualizovaný růst HDP",
    podnadpis=("Čtvrtletní údaje v %.",
               "Anualizovaný růst přepočítá změnu HDP za jedno čtvrtletí na celý rok, jako by stejné tempo trvalo "
               f"12 měsíců. Posledních {pg.cislo(posledni, 1, '%')} je nejvíce od {ctvrtleti[od]}. čtvrtletí "
               f"{roky[od]}."))
pg._osa_y(ax, OSA, "", 0)
n = len(hodnoty)
ax.set_xlim(-0.6, n - 0.4)
ax.bar(range(n), hodnoty, width=0.62, color=pg.FIALOVA, zorder=2, linewidth=0)
odsazeni = 8 / VYSKA_PLOCHY * (OSA[1] - OSA[0])
for i, h in enumerate(hodnoty):
    ax.text(i, h + (odsazeni if h >= 0 else -odsazeni), pg.cislo(h, 1), ha="center", va="bottom" if h >= 0 else "top",
            fontsize=pg.PISMO_HODNOTA, color=pg.TEXT_TMAVY)
ax.axhline(0, color=pg.NULOVA_CARA, linewidth=2 * 72 / pg.DPI, zorder=3)

# osa x: čtvrtletí a pod nimi roky uprostřed svých čtvrtletí, mezi roky dělicí čárka
ax.set_xticks(range(n))
ax.set_xticklabels([f"Q{c}" for c in ctvrtleti], fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
ax.tick_params(axis="x", pad=14 / pg.PT)
zacatky = [i for i, y in enumerate(roky) if i == 0 or y != roky[i - 1]]
for k, z in enumerate(zacatky):
    konec = (zacatky[k + 1] if k + 1 < len(zacatky) else n) - 1
    ax.text((z + konec) / 2, -52 / VYSKA_PLOCHY, str(roky[z]), transform=ax.get_xaxis_transform(), ha="center",
            va="top", fontsize=pg.PISMO_OSA, color=pg.TEXT_TMAVY, fontproperties=pg._STREDNI)
    if k:
        ax.add_line(Line2D([z - 0.5] * 2, [0, -40 / VYSKA_PLOCHY], transform=ax.get_xaxis_transform(),
                           color=pg.ZAKLADNA, linewidth=1.5 * 72 / pg.DPI, clip_on=False))

renderer = fig.canvas.get_renderer()
fig.canvas.draw()
leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
pos = ax.get_position()
ax.set_position([pg._fx(leva), pos.y0, pg._fx(pg.GRAF_PRAVA - leva), pos.height])
pg._legenda_a_zdroj(fig, [("HDP USA (anualizovaný růst, %)", pg.FIALOVA)], "Graf: Portu, zdroj: Trading Economics")
pg.uloz(fig, ZAKLAD + ".png", zvetseni=2)

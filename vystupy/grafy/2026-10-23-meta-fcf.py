"""Meta: volný cash flow po čtvrtletích (1Q 2015 – 3Q 2026), mld. USD.

Data: výkazy Meta Platforms (10-Q, 10-K; SEC XBRL), u přepočtených období poslední vykázané hodnoty
(2016 po přechodu na ASU 2016-09); rok 2015 v původním vykázání, protože Meta zpětně přepočetla jen celý rok.
Volný cash flow podle definice Mety = peněžní tok z provozní činnosti − nákupy pozemků, budov a zařízení
(capex) − splátky jistiny finančního leasingu (vykazované od 2019). Čtvrtletí = rozdíl kumulativních údajů
od začátku roku. 3Q 2026 z 10-Q podaného 22. 10. 2026.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-23-meta-fcf.py
"""
import csv
import sys

from matplotlib.lines import Line2D

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-23-meta-fcf"

roky, hodnoty = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        roky.append(int(r["rok"]))
        hodnoty.append(float(r["volny_cf_mld_usd"]))

OSA = (-4, 20, 2)
fig, ax = pg._platno(pg.GRAF_DOLNI_1RADEK, nadpis="Meta: volný cash flow",
                     podnadpis="Čtvrtletní údaje v miliardách USD")
pg._osa_y(ax, OSA, "", 0)

n = len(hodnoty)
ax.set_xlim(-0.6, n - 0.4)
ax.bar(range(n), hodnoty, width=0.62, color=pg.FIALOVA, zorder=2, linewidth=0)
ax.axhline(0, color=pg.NULOVA_CARA, linewidth=2 * 72 / pg.DPI, zorder=3)

# hodnoty nad sloupci svisle – 47 sloupců je na vodorovné popisky moc úzkých
odsazeni = 7 / (pg.GRAF_DOLNI_1RADEK - pg.GRAF_HORNI) * (OSA[1] - OSA[0])
for i, h in enumerate(hodnoty):
    ax.text(i, h + (odsazeni if h >= 0 else -odsazeni), pg.cislo(h, 1), rotation=90, ha="center",
            va="bottom" if h >= 0 else "top", fontsize=pg.PISMO_HODNOTA, color=pg.TEXT_TMAVY)

# osa x: roky uprostřed svých čtvrtletí, mezi roky krátká dělicí čárka
zacatky = [i for i, r in enumerate(roky) if i == 0 or r != roky[i - 1]]
ax.set_xticks([(z + (zacatky[k + 1] if k + 1 < len(zacatky) else n) - 1) / 2 for k, z in enumerate(zacatky)])
ax.set_xticklabels([str(roky[z]) for z in zacatky], fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
ax.tick_params(axis="x", pad=27 / pg.PT)
vyska_plochy = pg.GRAF_DOLNI_1RADEK - pg.GRAF_HORNI
for z in zacatky[1:]:
    ax.add_line(Line2D([z - 0.5] * 2, [0, -12 / vyska_plochy], transform=ax.get_xaxis_transform(),
                       color=pg.ZAKLADNA, linewidth=1.5 * 72 / pg.DPI, clip_on=False))

renderer = fig.canvas.get_renderer()
fig.canvas.draw()
leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
pos = ax.get_position()
ax.set_position([pg._fx(leva), pos.y0, pg._fx(pg.GRAF_PRAVA - leva), pos.height])

pg._legenda_a_zdroj(fig, [("Volný cash flow (mld. USD)", pg.FIALOVA)], "Graf: Portu, zdroj: Meta")
pg.uloz(fig, ZAKLAD + ".png")

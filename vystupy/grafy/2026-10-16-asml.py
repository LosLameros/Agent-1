"""ASML Holding N.V. (ASML) – tržby, čistý zisk a provozní marže, roční údaje v mil. eur.

Data: výkazy ASML podle US GAAP – roky 2017–2025 z výročních zpráv (20-F, SEC XBRL),
posledních 12 měsíců = rok 2025 − 1.–3. čtvrtletí 2025 + 1.–3. čtvrtletí 2026 (6-K ze 14. 10. 2026).
Provozní marže = provozní zisk (income from operations) / celkové tržby.
Vzhled: stejný jako grafy inflace a SOX – nadpis, osy, legenda a zdroj z nastroje/portu_grafy.py.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-asml.py
"""
import csv
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-16-asml"

obdobi, trzby, zisk, marze = [], [], [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        obdobi.append(r["obdobi"])
        trzby.append(float(r["trzby_mil_eur"]))
        zisk.append(float(r["cisty_zisk_mil_eur"]))
        marze.append(float(r["provozni_marze_pct"]))


def cele(v):
    """Zaokrouhlení 13 978,5 → 13 979 (ne bankovní) a mezera v tisících."""
    return pg.cislo(float(Decimal(str(v)).quantize(Decimal("1"), ROUND_HALF_UP)), 0)


# plátno, nadpis, osa y a mřížka stejně jako u grafů inflace a SOX
fig, ax = pg._platno(pg.GRAF_DOLNI_1RADEK, nadpis="ASML Holding N.V. (ASML)")
OSA = (0, 48000, 8000)
pg._osa_y(ax, OSA, "", 0)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=3)

# sloupce: tržby zeleně, čistý zisk fialově; hodnoty nad sloupci jako u sloupcových grafů Portu
n = len(obdobi)
ax.set_xlim(-0.5, n - 0.5)
SIRKA, MEZERA = 0.28, 0.12  # mezera, aby popisky zisku nezasahovaly do sloupců tržeb
odsazeni = 8 / (pg.GRAF_DOLNI_1RADEK - pg.GRAF_HORNI) * OSA[1]
for posun, hodnoty, barva in ((-(SIRKA + MEZERA) / 2, trzby, pg.ZELENA), ((SIRKA + MEZERA) / 2, zisk, pg.FIALOVA)):
    xs = [i + posun for i in range(n)]
    ax.bar(xs, hodnoty, width=SIRKA, color=barva, zorder=2, linewidth=0)
    for x, v in zip(xs, hodnoty):
        ax.text(x, v + odsazeni, cele(v), ha="center", va="bottom", fontsize=pg.PISMO_HODNOTA,
                color=pg.TEXT_TMAVY, zorder=4)
ax.set_xticks(range(n))
ax.set_xticklabels(obdobi, fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
ax.tick_params(axis="x", pad=29 / pg.PT)

# provozní marže: čára s body na vlastní skryté ose nad sloupci, hodnota nad bodem
ax2 = ax.twinx()
ax2.set_ylim(-30, 43)
ax2.axis("off")
ax2.plot(range(n), marze, color=pg.FIALOVA, linewidth=3 / pg.PT, marker="o", markersize=8 / pg.PT, zorder=5)
for i, m in enumerate(marze):
    ax2.text(i, m + 2.2, pg.cislo(round(m), 0, "%"), ha="center", va="bottom", fontsize=pg.PISMO_HODNOTA,
             color=pg.TEXT_TMAVY, zorder=6, bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))

# levý okraj podle nejdelšího popisku osy y („48 000“), jako u grafu SOX
renderer = fig.canvas.get_renderer()
fig.canvas.draw()
leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
pos = ax.get_position()
for a in (ax, ax2):
    a.set_position([pg._fx(leva), pos.y0, pg._fx(pg.GRAF_PRAVA - leva), pos.height])

pg._legenda_a_zdroj(fig, [("Celkové tržby (mil. eur)", pg.ZELENA), ("Čistý zisk (mil. eur)", pg.FIALOVA),
                          ("Provozní zisková marže", pg.FIALOVA, "cara")], "Graf: Portu, zdroj: ASML")
pg.uloz(fig, ZAKLAD + ".png")

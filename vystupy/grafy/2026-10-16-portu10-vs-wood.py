"""Portfolia od Portu 10 a 5 vs. WOOD realitní OPF – kumulativní zhodnocení v %, Portu vzhled.

Data: excel PortuCZK_ModelPortfolios_26.xlsx (od redakce) – denní hodnoty modelových portfolií
(list „Portfolio values“, 1. 6. 2023 = 1,0000) a kumulativní výnos fondu WOOD (list „Cumulative
return“), 1. 6. 2023 – 16. 10. 2026; převedené do vystupy/grafy/2026-10-16-portu10-vs-wood.csv.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-portu10-vs-wood.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-16-portu10-vs-wood"
RADY = [("portfolio_10_pct", "Portfolio 10", pg.FIALOVA),
        ("portfolio_5_pct", "Portfolio 5", pg.SVETLE_FIALOVA),
        ("wood_opf_pct", "WOOD realitní OPF", pg.ZELENA)]

datumy, data = [], {sloupec: [] for sloupec, _, _ in RADY}
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["datum"]))
        for sloupec, _, _ in RADY:
            data[sloupec].append(float(r[sloupec]))

fig = pg.spojnicovy(
    datumy, {nazev: data[sloupec] for sloupec, nazev, _ in RADY},
    osa_y=(0, 80, 10), jednotka="%", barvy=[barva for _, _, barva in RADY],
    format_x="%m/%Y", interval_mesicu=6, prvni_mesic=1, rozsah_x=(datumy[0], datumy[-1]),
    popisky_konec=True, mista_konec=1,
    schody=("WOOD realitní OPF",),  # fond roste skokově – svislé skoky, rovné úseky
    tloustka_cary=2.5,
    zdroj="Graf: Portu, zdroj: Portu, WOOD & Company",
    nadpis="Portfolia od Portu 10 a 5 vs. WOOD realitní OPF",
)
pg.uloz(fig, ZAKLAD + ".png")

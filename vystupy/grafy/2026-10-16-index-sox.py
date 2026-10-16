"""Vývoj polovodičového indexu SOX za poslední rok (15. 10. 2025 – 15. 10. 2026).

Data: PHLX Semiconductor Index (^SOX, index Nasdaq), denní uzavírací hodnoty z Yahoo Finance.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-index-sox.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-16-index-sox"

datumy, hodnoty = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["datum"]))
        hodnoty.append(float(r["sox_close"]))

fig = pg.spojnicovy(
    datumy, {"PHLX Semiconductor Index (SOX)": hodnoty},
    osa_y=(6000, 15000, 1000), jednotka="",
    format_x="mesic", interval_mesicu=1, rozsah_x=(datumy[0], datumy[-1]),
    popisky_konec=True, mista_konec=0, jednotka_konec="b.",
    zdroj="Graf: Portu, zdroj: Nasdaq",
    nadpis="Vývoj polovodičového indexu SOX za poslední rok",
)
pg.uloz(fig, ZAKLAD + ".png")

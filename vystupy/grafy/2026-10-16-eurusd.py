"""Euro / americký dolar (EUR/USD) za poslední rok – referenční kurzy ECB.

Data: ECB, denní referenční kurz EUR/USD (EXR/D.USD.EUR.SP00.A), 15. 10. 2025 – poslední zveřejněný den.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-eurusd.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-16-eurusd"

datumy, kurz = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["datum"]))
        kurz.append(float(r["eurusd_ecb"]))
zmena_pct = (kurz[-1] / kurz[0] - 1) * 100
zmena = kurz[-1] - kurz[0]
sipka = "▼" if zmena < 0 else "▲"
den = datumy[-1]

fig = pg.spojnicovy(
    datumy, {"Kurz EUR/USD": kurz},
    osa_y=(1.10, 1.20, 0.02), jednotka="", mista_osa=2,
    format_x="mesic", interval_mesicu=1, rozsah_x=(datumy[0], datumy[-1]),
    popisky_konec=True, mista_konec=4, vypln=True,
    hlavicka=(pg.cislo(kurz[-1], 4),
              f"{sipka} {pg.cislo(zmena_pct, 2, '%')} ({pg.cislo(zmena, 4)}) za 1 rok",
              f"Referenční kurz ECB k {den.day}. {den.month}. {den.year}"),
    zdroj="Graf: Portu, zdroj: ECB",
    nadpis="Euro / americký dolar (EUR/USD)",
)
pg.uloz(fig, ZAKLAD + ".png")

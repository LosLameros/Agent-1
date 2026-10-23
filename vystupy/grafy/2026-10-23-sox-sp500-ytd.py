"""Polovodičový index SOX a S&P 500 od začátku roku 2026 (31. 12. 2025 – 22. 10. 2026), zhodnocení v %.

Data: Yahoo Finance (^SOX – PHLX Semiconductor Index, Nasdaq; ^GSPC – S&P 500), denní uzavírací hodnoty;
zhodnocení = uzavírací hodnota / uzavírací hodnota 31. 12. 2025 − 1 (cenové indexy bez dividend).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-23-sox-sp500-ytd.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-23-sox-sp500-ytd"

datumy, sox, sp500 = [], [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["datum"]))
        sox.append(float(r["sox_ytd_pct"]))
        sp500.append(float(r["sp500_ytd_pct"]))

fig = pg.spojnicovy(
    datumy, {"Polovodičový index SOX": sox, "S&P 500": sp500},
    osa_y=(-20, 120, 20), jednotka="%", format_x="mesic", interval_mesicu=1, rozsah_x=(datumy[0], datumy[-1]),
    popisky_konec=True, mista_konec=1, tloustka_cary=3,
    zdroj="Graf: Portu, zdroj: Nasdaq, S&P Dow Jones Indices",
    nadpis="Polovodiče vs. S&P 500 od začátku roku", podnadpis="Zhodnocení od 31. 12. 2025, v %",
)
pg.uloz(fig, ZAKLAD + ".png")

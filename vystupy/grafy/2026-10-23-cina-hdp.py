"""Čína: meziroční růst HDP za posledních 10 let (4Q 2016 – 3Q 2026), čtvrtletně, v %.

Data: Trading Economics (CNGDPYOY, Národní statistický úřad Číny), poslední údaj za 3Q 2026 ze 19. 10. 2026.
Body jsou vyneseny ke konci čtvrtletí.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-23-cina-hdp.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-23-cina-hdp"

datumy, hodnoty = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["ctvrtleti_konec"]))
        hodnoty.append(float(r["hdp_rust_yoy_pct"]))


def bod(datum, smer):
    h = hodnoty[datumy.index(datum)]
    return (datum, h, pg.cislo(h, 1, "%"), smer)


fig = pg.spojnicovy(
    datumy, {"Meziroční růst HDP Číny": hodnoty},
    osa_y=(-12, 24, 4), jednotka="", format_x="%Y", rozsah_x=(dt.date(2016, 12, 31), datumy[-1]),
    anotace=[bod(dt.date(2020, 3, 31), "pod"), bod(dt.date(2021, 3, 31), "nad"), bod(dt.date(2022, 6, 30), "pod")],
    popisky_konec=True, mista_konec=1, jednotka_konec="%",
    zdroj="Graf: Portu, zdroj: Trading Economics",
    nadpis="Čína: meziroční růst HDP", podnadpis="Čtvrtletní údaje, v %, za posledních 10 let",
)
pg.uloz(fig, ZAKLAD + ".png")

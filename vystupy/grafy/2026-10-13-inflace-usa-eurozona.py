"""Meziroční inflace v USA a eurozóně (9/2016 – 9/2026).

Data: USA – BLS, CPI-U bez sezónního očištění (FRED CPIAUCNS), meziroční změna dopočtená
z indexu a zaokrouhlená na 0,1 (shoduje se s čísly BLS). Eurozóna – Eurostat, HICP
(prc_hicp_minr, unit=RCH_A, coicop18=TOTAL, geo=EA); září 2026 je předběžný odhad.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-13-inflace-usa-eurozona.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZACATEK, KONEC = dt.date(2016, 9, 1), dt.date(2026, 10, 1)
ZAKLAD = "vystupy/grafy/2026-10-13-inflace-usa-eurozona"

rady = {"USA": ([], []), "Eurozóna": ([], [])}
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rok, mesic = map(int, r["mesic"].split("-"))
        datum = dt.date(rok, mesic, 15)
        if datum < ZACATEK:
            continue
        for nazev, sloupec in (("USA", "usa_cpi_mezirocne_pct"), ("Eurozóna", "eurozona_hicp_mezirocne_pct")):
            if r[sloupec]:
                rady[nazev][0].append(datum)
                rady[nazev][1].append(float(r[sloupec]))

fig = pg.spojnicovy(
    rady["USA"][0], rady,
    osa_y=(-2, 12, 2), jednotka="%",
    format_x="%Y", interval_let=2, rozsah_x=(ZACATEK, KONEC), popisky_konec=True,
    zdroj="Eurozóna 9/2026: předběžný odhad. Graf: Portu, zdroj: BLS, Eurostat",
)
pg.uloz(fig, ZAKLAD + ".png")

"""Vývoj meziroční inflace v USA (1/2000 – 9/2026).

Data: BLS, CPI-U bez sezónního očištění (FRED CPIAUCNS), meziroční změna dopočtená z indexu
a zaokrouhlená na 0,1 – shoduje se s čísly BLS i Trading Economics (ověřeno 16. 10. 2026).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-inflace-usa.py [cs|sk]
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-16-inflace-usa"

datumy, inflace = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rok, mesic = map(int, r["mesic"].split("-"))
        datumy.append(dt.date(rok, mesic, 15))
        inflace.append(float(r["mezirocni_inflace_pct"]))

TEXTY = {
    "cs": {"rada": "Meziroční inflace", "nadpis": "Vývoj meziroční inflace v USA"},
    "sk": {"rada": "Medziročná inflácia", "nadpis": "Vývoj medziročnej inflácie v USA"},
}
jazyk = sys.argv[1] if len(sys.argv) > 1 else "cs"  # python3 … sk → slovenská verze (soubor …-sk.png)
T = TEXTY[jazyk]

fig = pg.spojnicovy(
    datumy, {T["rada"]: inflace},
    osa_y=(-3, 10, 1), jednotka="%", barvy=[pg.FIALOVA],
    format_x="%Y", interval_let=2, rozsah_x=(dt.date(2000, 1, 1), dt.date(2026, 10, 1)),
    popisky_konec=True,
    zdroj="Graf: Portu, zdroj: BLS",
    nadpis=T["nadpis"],
)
pg.uloz(fig, ZAKLAD + ("" if jazyk == "cs" else "-" + jazyk) + ".png")

"""Czechoslovak Group (CSG) – vývoj ceny akcie od vstupu na burzu (23. 1. 2026 – 13. 11. 2026), EUR. Nový design Portu.

Data: Yahoo Finance (CSG.AS, Euronext Amsterdam), týdenní ceny = poslední uzavírací cena týdne; poslední bod je
cena z 13. 11. 2026 během obchodování (14:52 SEČ), ne uzavírací. Upisovací cena IPO 25 EUR převzata z předlohy.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-14-csg.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-14-csg"
IPO = 25.0

datumy, ceny = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["datum"]))
        ceny.append(float(r["csg_close_eur"]))

od_zacatku = (1 - ceny[-1] / ceny[0]) * 100
pod_ipo = (1 - ceny[-1] / IPO) * 100
prvni_pod = next(d for d, c in zip(datumy, ceny) if c < IPO)


def datum(d):
    return f"{d.day}. {d.month}. {d.year}"


fig = pg.spojnicovy(
    datumy, {"Akcie CSG (EUR)": ceny},
    osa_y=(0, 35, 5), jednotka="", format_x="mesic", interval_mesicu=1,
    rozsah_x=(datumy[0] - dt.timedelta(days=14), datumy[-1]),
    popisky_konec=True, vrchol=True, mista_konec=2, jednotka_konec="€", tloustka_cary=2.5,
    hladina=(IPO, f"Upisovací cena IPO ({pg.cislo(IPO, 2, '€')})"),
    zdroj="Graf: Portu, zdroj: Yahoo Finance, Euronext Amsterdam",
    nadpis="Vývoj ceny akcií Czechoslovak Group (CSG) od vstupu na burzu",
    podnadpis=("Týdenní ceny v EUR za akcii na burze Euronext Amsterdam.",
               f"Od vstupu na burzu {datum(datumy[0])} cena klesla o {pg.cislo(od_zacatku, 1, '%')} "
               f"(z {pg.cislo(ceny[0], 2, '€')} na {pg.cislo(ceny[-1], 2, '€')}). Pod upisovací cenu IPO "
               f"{pg.cislo(IPO, 0, '€')} spadla koncem března a je teď pod ní o {pg.cislo(pod_ipo, 1, '%')}."),
)
pg.uloz(fig, ZAKLAD + ".png")

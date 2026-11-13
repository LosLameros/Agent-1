"""Akcie Take-Two Interactive (TTWO), vydavatele GTA VI – týdenní uzavírací ceny za posledních 10 let, USD.

Data: Yahoo Finance (TTWO, Nasdaq), týdenní uzavírací ceny, týden označený pátkem; poslední týden k 12. 11. 2026.
Vzor nového designu grafů Portu (examples/grafy/vzor-take-two.png): velký nadpis, šedý podnadpis s tučnou první
větou a čísly, jemná fialová výplň pod čarou, vyznačené maximum a poslední hodnota s datem.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-13-take-two.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-13-take-two"

datumy, ceny = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["tyden_konec"]))
        ceny.append(float(r["ttwo_close_usd"]))

i_max = max(range(len(ceny)), key=ceny.__getitem__)
rust = (ceny[-1] / ceny[0] - 1) * 100
od_max = (1 - ceny[-1] / ceny[i_max]) * 100
d = datumy[i_max]

fig = pg.spojnicovy(
    datumy, {"Akcie Take-Two (USD)": ceny},
    osa_y=(0, 300, 50), jednotka="", format_x="%Y", rozsah_x=(datumy[0], datumy[-1]),
    popisky_konec=True, vrchol=True, mista_konec=1, jednotka_konec="$", tloustka_cary=2.5,
    zdroj="Graf: Portu, zdroj: Yahoo Finance",
    nadpis="Akcie Take-Two Interactive, vydavatele GTA VI",
    podnadpis=("Týdenní uzavírací ceny v USD za akcii.",
               f"Za posledních 10 let cena akcie vzrostla o {pg.cislo(rust, 1, '%')} (ze {pg.cislo(ceny[0], 1, '$')} "
               f"na {pg.cislo(ceny[-1], 1, '$')}). Od maxima {pg.cislo(ceny[i_max], 1, '$')} z {d.day}.\u00a0{d.month}.\u00a0"
               f"{d.year} je teď níže o {pg.cislo(od_max, 1, '%')}."),
)
pg.uloz(fig, ZAKLAD + ".png")

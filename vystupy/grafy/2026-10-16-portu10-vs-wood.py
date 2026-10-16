"""Portfolio od Portu 10 vs. WOOD realitní OPF – kumulativní zhodnocení v %, Portu vzhled.

Data: odečtená po pixelech z podkladového grafu (Datawrapper, výřez 1416 × 786 px) skriptem
vystupy/grafy/2026-10-16-portu10-vs-wood-odecet.py do vystupy/grafy/2026-10-16-portu10-vs-wood.csv
(sloupce datum s časem, rada portu_10 / wood_opf, hodnota_pct). Přesnost zhruba ±0,1 p. b.;
konce 68,9 % a 28,0 % z popisků v podkladu.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-portu10-vs-wood.py [cesta_k_csv]
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

VSTUP = sys.argv[1] if len(sys.argv) > 1 else "vystupy/grafy/2026-10-16-portu10-vs-wood.csv"
ZAKLAD = "vystupy/grafy/2026-10-16-portu10-vs-wood"
NAZVY = ["Portfolio od Portu 10", "WOOD & Company realitní OPF"]


KONEC = dt.datetime(2026, 10, 16, 23, 59)  # pojistka: konec čáry nesmí přesáhnout datum grafu
rady = {nazev: ([], []) for nazev in NAZVY}
klic = {"portu_10": NAZVY[0], "wood_opf": NAZVY[1]}
with open(VSTUP, encoding="utf-8") as f:
    for r in csv.DictReader(f):
        cas = min(dt.datetime.fromisoformat(r["datum"]), KONEC)
        rady[klic[r["rada"]]][0].append(cas)
        rady[klic[r["rada"]]][1].append(float(r["hodnota_pct"]))
datumy = sorted(set(rady[NAZVY[0]][0]) | set(rady[NAZVY[1]][0]))
print("období:", datumy[0], "–", datumy[-1])

osa = (0, 80, 10)
fig = pg.spojnicovy(
    datumy, rady, osa_y=osa, jednotka="%",
    format_x="%m/%Y", interval_mesicu=6, prvni_mesic=1, rozsah_x=(datumy[0], datumy[-1]),
    popisky_konec=True, mista_konec=1,
    zdroj="Graf: Portu, zdroj: Portu, WOOD & Company",
    nadpis="Portfolio od Portu 10 vs. WOOD realitní OPF",
)
pg.uloz(fig, ZAKLAD + ".png")

"""Portfolio od Portu 10 vs. WOOD realitní OPF – kumulativní zhodnocení v %, Portu vzhled.

Data: CSV z Datawrapperu („Get the data“ pod původním grafem) uložené jako
podklady/grafy/portu10-vs-wood.csv. Skript načte první sloupec jako datum a další dva sloupce
jako řady (Portu CZK Model Portfolio 10, WOOD and Co Realitní OPF) v pořadí, v jakém v CSV jsou.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-16-portu10-vs-wood.py [cesta_k_csv]
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

VSTUP = sys.argv[1] if len(sys.argv) > 1 else "podklady/grafy/portu10-vs-wood.csv"
ZAKLAD = "vystupy/grafy/2026-10-16-portu10-vs-wood"
NAZVY = ["Portfolio od Portu 10", "WOOD & Company realitní OPF"]


def datum(text):
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d. %m. %Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return dt.datetime.strptime(text.strip(), fmt).date()
        except ValueError:
            pass
    raise ValueError(f"Neznámý formát data: {text!r}")


def cislo(text):
    text = text.strip().replace(" ", "").replace(" ", "").replace("%", "").replace(",", ".")
    return float(text) if text not in ("", "-", "–") else None


with open(VSTUP, encoding="utf-8-sig") as f:
    oddelovac = ";" if ";" in f.readline() else ","
    f.seek(0)
    radky = list(csv.reader(f, delimiter=oddelovac))
hlavicka, data = radky[0], [r for r in radky[1:] if r and r[0].strip()]
datumy = [datum(r[0]) for r in data]
rady = {}
for k, nazev in enumerate(NAZVY, start=1):
    body = [(d, cislo(r[k])) for d, r in zip(datumy, data) if len(r) > k and cislo(r[k]) is not None]
    rady[nazev] = ([d for d, _ in body], [v for _, v in body])
print("sloupce v CSV:", hlavicka, "| období:", datumy[0], "–", datumy[-1])

maximum = max(max(v) for _, v in rady.values())
minimum = min(min(v) for _, v in rady.values())
krok = 10
osa = (min(0, krok * (minimum // krok)), krok * (maximum // krok + 1), krok)
fig = pg.spojnicovy(
    datumy, rady, osa_y=osa, jednotka="%",
    format_x="%m/%Y", interval_mesicu=6, rozsah_x=(datumy[0], datumy[-1]),
    popisky_konec=True, mista_konec=1,
    zdroj="Graf: Portu, zdroj: Portu, WOOD & Company",
    nadpis="Portfolio od Portu 10 vs. WOOD realitní OPF",
)
pg.uloz(fig, ZAKLAD + ".png")

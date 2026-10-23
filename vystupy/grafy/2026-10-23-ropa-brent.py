"""Cena ropy Brent za posledních 5 let (22. 10. 2021 – 22. 10. 2026), USD za barel.

Data: Trading Economics, symbol CO1:COM (front-month futures Brent), denní uzavírací ceny;
poslední hodnota = uzavírací cena 22. 10. 2026 (poslední celý obchodní den).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-23-ropa-brent.py [cs|sk]
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-23-ropa-brent"

datumy, hodnoty = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["datum"]))
        hodnoty.append(float(r["brent_close_usd"]))

NADPIS = {"cs": "Cena ropy Brent za posledních 5 let",
          "sk": "Cena ropy Brent za posledných 5 rokov"}
jazyk = sys.argv[1] if len(sys.argv) > 1 else "cs"  # python3 … sk → slovenská verze (soubor …-sk.png)

fig = pg.spojnicovy(
    datumy, {"Ropa Brent (USD za barel)": hodnoty},
    osa_y=(40, 140, 20), jednotka="",
    format_x="%m/%Y", interval_mesicu=6, prvni_mesic=1, rozsah_x=(datumy[0], datumy[-1]), jazyk=jazyk,
    popisky_konec=True, mista_konec=2, jednotka_konec="USD", tloustka_cary=2.5,
    zdroj="Graf: Portu, zdroj: Trading Economics",
    nadpis=NADPIS[jazyk],
)
pg.uloz(fig, ZAKLAD + ("" if jazyk == "cs" else "-" + jazyk) + ".png")

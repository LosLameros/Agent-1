"""Vývoj akcie Volvo Car AB (VOLCAR-B, Nasdaq Stockholm) za poslední rok (23. 10. 2025 – 23. 10. 2026), SEK.

Data: Yahoo Finance (VOLCAR-B.ST), denní uzavírací ceny; poslední hodnota je cena během obchodování
23. 10. 2026 v 11:31 SELČ (ten den akcie spadla o 27 %), po uzávěrce ji případně aktualizujte.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-23-volvo-cars.py [cs|sk]
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-10-23-volvo-cars"

datumy, hodnoty = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        datumy.append(dt.date.fromisoformat(r["datum"]))
        hodnoty.append(float(r["volcar_b_close_sek"]))

NADPIS = {"cs": "Vývoj akcie Volvo Cars za poslední rok",
          "sk": "Vývoj akcie Volvo Cars za posledný rok"}
jazyk = sys.argv[1] if len(sys.argv) > 1 else "cs"  # python3 … sk → slovenská verze (soubor …-sk.png)

fig = pg.spojnicovy(
    datumy, {"Volvo Car AB, akcie B (SEK)": hodnoty},
    osa_y=(0, 40, 5), jednotka="",
    format_x="mesic", interval_mesicu=1, rozsah_x=(datumy[0], datumy[-1]), jazyk=jazyk,
    popisky_konec=True, mista_konec=2, jednotka_konec="SEK",
    zdroj="Graf: Portu, zdroj: Nasdaq Stockholm",
    nadpis=NADPIS[jazyk],
)
pg.uloz(fig, ZAKLAD + ("" if jazyk == "cs" else "-" + jazyk) + ".png")

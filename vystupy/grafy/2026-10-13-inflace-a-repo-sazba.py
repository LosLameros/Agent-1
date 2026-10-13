"""Vývoj meziroční inflace ČR a dvoutýdenní repo sazby ČNB (1/2000 – 10/2026).

Data: ČSÚ DataStat, výběr CEN0101HT02 (přírůstek indexu spotřebitelských cen ke stejnému
měsíci předchozího roku, ukazatel 6134J05); ČNB, historie 2T repo sazby
(https://www.cnb.cz/cs/casto-kladene-dotazy/.galleries/vyvoj_repo_historie.txt).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-13-inflace-a-repo-sazba.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZACATEK, KONEC = dt.date(2000, 1, 1), dt.date(2026, 10, 13)
ZAKLAD = "vystupy/grafy/2026-10-13-inflace-a-repo-sazba"

inflace_x, inflace = [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["mezirocni_inflace_pct"]:
            r_, m_ = map(int, r["mesic"].split("-"))
            inflace_x.append(dt.date(r_, m_, 15))
            inflace.append(float(r["mezirocni_inflace_pct"]))

repo_x, repo = [], []
with open(ZAKLAD + "-repo-zmeny.csv", encoding="utf-8") as f:
    zmeny = [(dt.date.fromisoformat(r["platna_od"]), float(r["repo_sazba_pct"])) for r in csv.DictReader(f)]
platna = [s for d, s in zmeny if d <= ZACATEK][-1]
repo_x, repo = [ZACATEK], [platna]
for d, s in zmeny:
    if ZACATEK < d <= KONEC:
        repo_x.append(d)
        repo.append(s)
repo_x.append(KONEC)
repo.append(repo[-1])

fig = pg.spojnicovy(
    inflace_x,
    {"Meziroční inflace": (inflace_x, inflace), "2T repo sazba ČNB": (repo_x, repo)},
    osa_y=(-2, 20, 2), jednotka="%", barvy=[pg.ZELENA, pg.FIALOVA],
    format_x="%Y", interval_let=2, rozsah_x=(ZACATEK, KONEC),
    schody=("2T repo sazba ČNB",), popisky_konec=True,
    zdroj="Graf: Portu, zdroj: ČSÚ, ČNB",
)
pg.uloz(fig, ZAKLAD + ".png")

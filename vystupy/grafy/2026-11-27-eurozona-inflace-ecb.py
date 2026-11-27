"""Inflace v eurozóně (HICP, meziročně) a depozitní sazba ECB za 10 let (10/2016 – 10/2026), v %. Nový design Portu.

Data: Trading Economics – ECCPEMUY (meziroční inflace HICP, měsíčně, ke konci měsíce) a EUROAREADEPINTRAT (depozitní
sazba ECB, schodovitě od data rozhodnutí; poslední bod 31. 10. 2026 jen prodlužuje platnou sazbu na konec grafu).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-27-eurozona-inflace-ecb.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-27-"

with open(ZAKLAD + "eurozona-inflace.csv", encoding="utf-8") as f:
    r = list(csv.DictReader(f))
mesice = [dt.date.fromisoformat(x["mesic_konec"]) for x in r]
inflace = [float(x["hicp_mezirocne_pct"]) for x in r]
with open(ZAKLAD + "ecb-depozitni-sazba.csv", encoding="utf-8") as f:
    r = list(csv.DictReader(f))
dny = [dt.date.fromisoformat(x["datum"]) for x in r]
sazba = [float(x["depozitni_sazba_pct"]) for x in r]

i_max = max(range(len(inflace)), key=inflace.__getitem__)

fig = pg.spojnicovy(
    mesice,
    {"Inflace (HICP, meziročně)": inflace, "Depozitní sazba ECB": (dny, sazba)},
    osa_y=(-2, 12, 2), jednotka="%", format_x="%Y", rozsah_x=(dt.date(2016, 10, 1), mesice[-1]),
    schody=("Depozitní sazba ECB",), popisky_konec=True, mista_konec=1, tloustka_cary=3,
    anotace=[(mesice[i_max], inflace[i_max], f"{pg.cislo(inflace[i_max], 1, '%')} (říj 2022)", "nad"),
            ],
    zdroj="Graf: Portu, zdroj: Trading Economics",
    nadpis="Inflace v eurozóně a úroková sazba ECB",
    podnadpis=("Meziroční inflace (HICP) a depozitní sazba ECB za 10 let, v %.",
               "Inflace v říjnu 2026 dosáhla 4,0 %, nejvíce od září 2023. ECB letos zvýšila depozitní sazbu dvakrát, "
               "na 2,5 %."),
)
pg.uloz(fig, ZAKLAD + "eurozona-inflace-ecb.png", zvetseni=2)

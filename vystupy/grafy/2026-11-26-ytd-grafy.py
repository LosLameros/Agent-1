"""Nvidia, Nasdaq-100 a Anthropic (ANT) – zhodnocení od začátku roku, tři samostatné grafy v novém designu Portu.

Data: Yahoo Finance, denní uzavírací ceny (NVDA, ^NDX, ANT) do 25. 11. 2026. Nvidia a Nasdaq-100: změna oproti uzavírací
ceně 31. 12. 2025 („YTD“). Anthropic je na burze od 19. 11. 2026, proto je základ cena IPO 83 USD (stanovena 18. 11.
2026, podle zpráv ITV, Constellation Research a dalších) a graf ukazuje první obchodní dny; do roku se přepočítat nedá.
Cenové indexy bez dividend. Uloženo ostře ve dvojnásobném rozlišení.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-26-ytd-grafy.py
"""
import csv
import datetime as dt
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-26-ytd-"


def nacti(nazev):
    with open(ZAKLAD + nazev + ".csv", encoding="utf-8") as f:
        r = list(csv.DictReader(f))
    return ([dt.date.fromisoformat(x["datum"]) for x in r], [float(x["zmena_pct"]) for x in r],
            [float(x["close"]) for x in r], float(r[0]["zaklad"]))


def datum(d):
    return f"{d.day}. {d.month}. {d.year}"


def graf(nazev, serie, osa_y, nadpis, podnadpis, **kw):
    d, zmena, ceny, zaklad = nacti(nazev)
    fig = pg.spojnicovy(d, {serie: zmena}, osa_y=osa_y, jednotka="%", popisky_konec=True, vrchol=True,
                        mista_konec=1, jednotka_konec="%", nadpis=nadpis, podnadpis=podnadpis(d, zmena, ceny, zaklad),
                        **kw)
    pg.uloz(fig, ZAKLAD + nazev + ".png", zvetseni=2)


def znamenko(v):
    return ("+" if v > 0 else "") + pg.cislo(v, 1, "%")


def pod_ytd(jmeno, mena):
    def f(d, zmena, ceny, zaklad):
        i = max(range(len(zmena)), key=zmena.__getitem__)
        return (f"Zhodnocení od začátku roku (od 31. 12. 2025), v %.",
                f"{jmeno} je letos {znamenko(zmena[-1])} ({pg.cislo(zaklad, 2)} → {pg.cislo(ceny[-1], 2)} {mena}). "
                f"Maximum bylo {znamenko(zmena[i])} dne {datum(d[i])}, od něj je akcie níže o "
                f"{pg.cislo((1 - ceny[-1] / ceny[i]) * 100, 1, '%')}.")
    return f


def pod_nasdaq(d, zmena, ceny, zaklad):
    i = max(range(len(zmena)), key=zmena.__getitem__)
    return ("Zhodnocení od začátku roku (od 31. 12. 2025), v %.",
            f"Index je letos {znamenko(zmena[-1])} ({pg.cislo(zaklad, 0)} → {pg.cislo(ceny[-1], 0)} b.). "
            f"Maximum bylo {znamenko(zmena[i])} dne {datum(d[i])}, od něj je index níže o "
            f"{pg.cislo((1 - ceny[-1] / ceny[i]) * 100, 1, '%')}.")


def pod_ant(d, zmena, ceny, zaklad):
    return ("Zhodnocení od ceny IPO 83 $ (obchodování od 19. 11. 2026), v %.",
            f"Akcie první den zavřela na {pg.cislo(ceny[0], 2, '$')}, tedy {znamenko(zmena[0])} nad cenou IPO. "
            f"Od té doby ztratila {pg.cislo(abs(zmena[-1] - zmena[0]), 1)} procentního bodu a je na {pg.cislo(ceny[-1], 2, '$')} "
            f"({znamenko(zmena[-1])} oproti ceně IPO).")


graf("nvidia", "Nvidia (NVDA)", (-40, 40, 10), "Nvidia od začátku roku", pod_ytd("Nvidia", "$"),
     format_x="mesic", interval_mesicu=1, zdroj="Graf: Portu, zdroj: Yahoo Finance", tloustka_cary=2.5)
graf("nasdaq100", "Nasdaq-100", (-10, 30, 10), "Nasdaq-100 od začátku roku", pod_nasdaq,
     format_x="mesic", interval_mesicu=1, zdroj="Graf: Portu, zdroj: Yahoo Finance", tloustka_cary=2.5)
graf("anthropic", "Anthropic (ANT)", (-5, 20, 5), "Anthropic od vstupu na burzu", pod_ant,
     format_x="den", rozsah_x=(dt.date(2026, 11, 18), dt.date(2026, 11, 26)),
     hladina=(0, "Cena IPO 83,00 $", "vlevo-pod"), zdroj="Graf: Portu, zdroj: Yahoo Finance, Nasdaq")

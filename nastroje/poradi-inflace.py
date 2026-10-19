#!/usr/bin/env python3
"""Pořadí evropských států podle meziroční inflace pro tiskovou zprávu o inflaci.

Použití:
    python3 -I nastroje/poradi-inflace.py podklady-inflace.csv [--mesic RRRR-MM]

Vstupní CSV (UTF-8, oddělovač čárka) s hlavičkou:
    zeme,hodnota,predchozi,obdobi
    Czech Republic,2.5,1.9,2026-09
    ...
- zeme       = anglický název přesně jako na Trading Economics („Inflation Rate – Europe“)
- hodnota    = sloupec Last
- predchozi  = sloupec Previous (nepovinné, může být prázdné)
- obdobi     = referenční měsíc údaje (sloupec Reference / LatestValueDate) ve tvaru RRRR-MM

Skript sám vyřadí Turecko, Faerské ostrovy a agregát eurozóny, seřadí státy
přesně podle hodnoty (bez zaokrouhlení), spočítá pořadí ČR od nejnižší inflace
(shodné hodnoty sdílejí pořadí: pořadí = počet států s nižší inflací + 1)
a vypíše vše, co potřebuje odstavec s evropským srovnáním.
"""
import csv
import sys

VYRAZENE = {"Turkey", "Faroe Islands", "Euro Area", "European Union"}
SOUSEDE = ["Slovakia", "Poland", "Germany", "Austria"]

CESKY = {
    "Albania": "Albánie", "Austria": "Rakousko", "Belarus": "Bělorusko", "Belgium": "Belgie",
    "Bosnia and Herzegovina": "Bosna a Hercegovina", "Bulgaria": "Bulharsko", "Croatia": "Chorvatsko",
    "Cyprus": "Kypr", "Czech Republic": "Česko", "Denmark": "Dánsko", "Estonia": "Estonsko",
    "Finland": "Finsko", "France": "Francie", "Germany": "Německo", "Greece": "Řecko",
    "Hungary": "Maďarsko", "Iceland": "Island", "Ireland": "Irsko", "Italy": "Itálie",
    "Kosovo": "Kosovo", "Latvia": "Lotyšsko", "Liechtenstein": "Lichtenštejnsko",
    "Lithuania": "Litva", "Luxembourg": "Lucembursko", "Macedonia": "Severní Makedonie",
    "North Macedonia": "Severní Makedonie", "Malta": "Malta", "Moldova": "Moldavsko",
    "Montenegro": "Černá Hora", "Netherlands": "Nizozemsko", "Norway": "Norsko", "Poland": "Polsko",
    "Portugal": "Portugalsko", "Romania": "Rumunsko", "Russia": "Rusko", "Serbia": "Srbsko",
    "Slovakia": "Slovensko", "Slovenia": "Slovinsko", "Spain": "Španělsko", "Sweden": "Švédsko",
    "Switzerland": "Švýcarsko", "Ukraine": "Ukrajina", "United Kingdom": "Spojené království",
    "Andorra": "Andorra", "Monaco": "Monako", "San Marino": "San Marino", "Gibraltar": "Gibraltar",
    "Isle of Man": "Ostrov Man", "Jersey": "Jersey", "Guernsey": "Guernsey",
}


def cz(zeme):
    return CESKY.get(zeme, zeme)


def fmt(x):
    # české desetinné číslo s jedním až dvěma desetinnými místy podle zdroje
    s = f"{x:.2f}".rstrip("0")
    if s.endswith("."):
        s += "0"
    return s.replace(".", ",")


def poradi(staty, klic, zeme):
    hodnota = next(s[klic] for s in staty if s["zeme"] == zeme)
    return sum(1 for s in staty if s[klic] < hodnota) + 1


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mesic = None
    if "--mesic" in sys.argv:
        mesic = sys.argv[sys.argv.index("--mesic") + 1]

    staty, vyrazene = [], []
    with open(sys.argv[1], encoding="utf-8") as f:
        for r in csv.DictReader(f):
            zeme = r["zeme"].strip()
            if not zeme:
                continue
            if zeme in VYRAZENE:
                vyrazene.append(zeme)
                continue
            pred = (r.get("predchozi") or "").strip()
            staty.append({
                "zeme": zeme,
                "hodnota": float(r["hodnota"].replace(",", ".")),
                "predchozi": float(pred.replace(",", ".")) if pred else None,
                "obdobi": (r.get("obdobi") or "").strip(),
            })

    jmena = [s["zeme"] for s in staty]
    duplicity = {z for z in jmena if jmena.count(z) > 1}
    if duplicity:
        sys.exit(f"CHYBA: duplicitní řádky {sorted(duplicity)}")
    if "Czech Republic" not in jmena:
        sys.exit("CHYBA: v datech chybí Czech Republic")

    staty.sort(key=lambda s: (s["hodnota"], cz(s["zeme"])))
    n = len(staty)
    cr = next(s for s in staty if s["zeme"] == "Czech Republic")
    p = poradi(staty, "hodnota", "Czech Republic")
    shoda = [cz(s["zeme"]) for s in staty if s["hodnota"] == cr["hodnota"] and s["zeme"] != "Czech Republic"]

    print(f"Vyřazeno: {', '.join(vyrazene) or 'nic'}")
    print(f"Počet sledovaných evropských států: {n}")
    print(f"ČR: {fmt(cr['hodnota'])} % ({cr['obdobi']}) -> {p}. nejnižší inflace"
          + (f", shodná hodnota jako: {', '.join(shoda)}" if shoda else ""))

    if all(s["predchozi"] is not None for s in staty):
        pp = poradi(staty, "predchozi", "Czech Republic")
        print(f"Pořadí ČR podle sloupce Previous: {pp}. (jen kontrola, viz prompt agenta)")

    print("\nSousedé:")
    for z in SOUSEDE:
        s = next((s for s in staty if s["zeme"] == z), None)
        if s is None:
            print(f"  {cz(z)}: CHYBÍ V DATECH")
            continue
        vztah = "vyšší" if s["hodnota"] > cr["hodnota"] else ("stejná" if s["hodnota"] == cr["hodnota"] else "nižší")
        print(f"  {cz(z)}: {fmt(s['hodnota'])} % ({s['obdobi']}), oproti ČR {vztah}")

    print("\nNejvyšší inflace (3 + případné shody):")
    hranice = staty[-3]["hodnota"] if n >= 3 else staty[0]["hodnota"]
    for s in reversed(staty):
        if s["hodnota"] >= hranice:
            print(f"  {cz(s['zeme'])}: {fmt(s['hodnota'])} % ({s['obdobi']})")
    print("\nNejnižší inflace (3 + případné shody):")
    hranice = staty[2]["hodnota"] if n >= 3 else staty[-1]["hodnota"]
    for s in staty:
        if s["hodnota"] <= hranice:
            print(f"  {cz(s['zeme'])}: {fmt(s['hodnota'])} % ({s['obdobi']})")

    print("\nCelé pořadí od nejnižší inflace:")
    for s in staty:
        r = poradi(staty, "hodnota", s["zeme"])
        znacka = "  <-- ČR" if s["zeme"] == "Czech Republic" else ""
        print(f"  {r:>2}. {cz(s['zeme']):<24} {fmt(s['hodnota']):>6} %  {s['obdobi']}{znacka}")

    if mesic:
        jine = [f"{cz(s['zeme'])} ({s['obdobi'] or '?'})" for s in staty if s["obdobi"] != mesic]
        if jine:
            print(f"\nPOZOR – údaj není za {mesic}: {', '.join(jine)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Načte Excel (nebo CSV) s klienty, kteří mají narozeniny, pro agenta prani-k-narozeninam.

Použití:
    python3 -I nastroje/narozeniny-z-excelu.py <soubor.xlsx|.csv> [--mesic RRRR-MM]

Skript sám najde řádek s hlavičkou a sloupce podle názvu (na velikosti písmen
a diakritice nezáleží):
    jméno, příjmení, celé jméno (když jméno a příjmení nejsou zvlášť),
    e-mail, datum narození (nebo den/měsíc narozenin), pohlaví/oslovení, titul.

Výstup je JSON na stdout: seznam klientů seřazený podle dne narozenin
a seznam upozornění (chybí e-mail, neplatný e-mail, duplicita, chybí datum,
narozeniny mimo zadaný měsíc, 29. 2. v nepřestupném roce).

Bez --mesic bere u každého klienta nejbližší narozeniny od dnešního dne.
S --mesic RRRR-MM počítá datum narozenin v tom měsíci a klienty z jiných
měsíců jen označí upozorněním (nevyřazuje je, rozhodne agent).

Vokativ a rod skript neurčuje, to dělá agent podle pravidel v promptu.
Skript jen přidá nápovědu `rod_napoveda` podle příjmení (-ová / -á) a sloupce pohlaví.
"""
import csv
import datetime as dt
import json
import re
import sys
import unicodedata

DNY = ["pondělí", "úterý", "středa", "čtvrtek", "pátek", "sobota", "neděle"]


def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z]", "", s.lower())


# klíč -> funkce, která pozná název sloupce (po norm)
SLOUPCE = {
    "prijmeni": lambda h: h.startswith("prijmeni") or h in {"surname", "lastname", "priezvisko", "clientlastname", "contactlastname"},
    "jmeno": lambda h: h in {"jmeno", "krestnijmeno", "firstname", "name", "meno", "krstnemeno", "clientfirstname"},
    "cele_jmeno": lambda h: h in {"jmenoaprijmeni", "celejmeno", "klient", "jmenoklienta",
                                  "fullname", "menoapriezvisko", "kontakt"},
    "email": lambda h: "mail" in h,
    "datum_narozeni": lambda h: h.startswith("datumnaroz") or h in {"narozeni", "narozen", "narozeniny",
                                                                    "birthday", "birthdate", "dateofbirth",
                                                                    "datumnarodenia", "dennarozeni"},
    "pohlavi": lambda h: h in {"pohlavi", "rod", "gender", "sex", "oslovení", "osloveni", "pohlavie"},
    "titul": lambda h: h in {"titul", "titulpred", "title", "tituly"},
    "poradce": lambda h: h in {"poradce", "advisername", "adviser", "advisor", "advisorname", "konzultant"},
}


def najdi_hlavicku(radky):
    for i, radek in enumerate(radky[:20]):
        mapa = {}
        for j, bunka in enumerate(radek):
            h = norm(bunka)
            if not h:
                continue
            for klic, test in SLOUPCE.items():
                if klic not in mapa and test(h):
                    mapa[klic] = j
                    break
        if "email" in mapa and ("prijmeni" in mapa or "cele_jmeno" in mapa or "jmeno" in mapa
                                or "datum_narozeni" in mapa):
            return i, mapa
    return None, {}


def nacti(cesta):
    if cesta.lower().endswith((".csv", ".txt")):
        with open(cesta, encoding="utf-8-sig", newline="") as f:
            vzorek = f.read(4096)
            f.seek(0)
            try:
                dialekt = csv.Sniffer().sniff(vzorek, delimiters=",;\t")
            except csv.Error:
                dialekt = csv.excel
            return {"CSV": [list(r) for r in csv.reader(f, dialekt)]}
    import openpyxl
    wb = openpyxl.load_workbook(cesta, data_only=True, read_only=True)
    return {ws.title: [list(r) for r in ws.iter_rows(values_only=True)] for ws in wb.worksheets}


def parsuj_datum(v):
    """Vrátí (den, měsíc, rok nebo None) nebo None."""
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v.day, v.month, v.year
    if isinstance(v, dt.date):
        return v.day, v.month, v.year
    if isinstance(v, (int, float)) and 1 < v < 80000:  # sériové číslo Excelu
        d = dt.date(1899, 12, 30) + dt.timedelta(days=int(v))
        return d.day, d.month, d.year
    s = str(v).strip()
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        return int(m.group(3)), int(m.group(2)), int(m.group(1))
    m = re.match(r"^(\d{1,2})\s*[./-]\s*(\d{1,2})\s*[./-]?\s*(\d{2,4})?", s)
    if m:
        rok = m.group(3)
        if rok and len(rok) == 2:
            rok = "19" + rok if int(rok) > 30 else "20" + rok
        return int(m.group(1)), int(m.group(2)), int(rok) if rok else None
    return None


def datum_narozenin(den, mesic, rok_cil):
    try:
        return dt.date(rok_cil, mesic, den), None
    except ValueError:
        if den == 29 and mesic == 2:
            return dt.date(rok_cil, 2, 28), "narozen(a) 29. 2., v roce %d přání posílám 28. 2." % rok_cil
        raise


def main():
    args = sys.argv[1:]
    if not args or args[0] in {"-h", "--help"}:
        print(__doc__)
        sys.exit(0 if args else 1)
    cesta = args[0]
    mesic_cil = None
    if "--mesic" in args:
        r, m = args[args.index("--mesic") + 1].split("-")
        mesic_cil = (int(r), int(m))
    dnes = dt.date.today()

    listy = nacti(cesta)
    klienti, upozorneni, prectene_listy = [], [], []
    for list_nazev, radky in listy.items():
        i, mapa = najdi_hlavicku(radky)
        if i is None:
            continue
        prectene_listy.append({"list": list_nazev, "hlavicka": [str(x) for x in radky[i] if x is not None],
                               "rozpoznane_sloupce": {k: str(radky[i][j]) for k, j in mapa.items()}})
        for cislo, radek in enumerate(radky[i + 1:], start=i + 2):
            def bunka(k):
                j = mapa.get(k)
                if j is None or j >= len(radek) or radek[j] is None:
                    return ""
                return radek[j] if k == "datum_narozeni" else str(radek[j]).strip()

            if not any(str(x).strip() for x in radek if x is not None):
                continue
            k = {
                "radek": f"{list_nazev}!{cislo}",
                "titul": bunka("titul"),
                "jmeno": bunka("jmeno"),
                "prijmeni": bunka("prijmeni"),
                "cele_jmeno": bunka("cele_jmeno"),
                "email": bunka("email").lower(),
                "pohlavi_ze_souboru": bunka("pohlavi"),
                "poradce": bunka("poradce"),
            }
            if not (k["jmeno"] or k["prijmeni"] or k["cele_jmeno"]):
                k["prijmeni_odhadni_z_emailu"] = k["email"].split("@")[0]
            kdo = " ".join(x for x in [k["jmeno"], k["prijmeni"]] if x) or k["cele_jmeno"] or k["email"]
            prijmeni = k["prijmeni"] or (k["cele_jmeno"].split()[-1] if k["cele_jmeno"] else "")
            p = norm(k["pohlavi_ze_souboru"])
            if p.startswith(("z", "f", "pani", "w")):
                k["rod_napoveda"] = "žena (ze souboru)"
            elif p.startswith(("m", "pan")):
                k["rod_napoveda"] = "muž (ze souboru)"
            elif prijmeni.lower().endswith(("ová", "á")):
                k["rod_napoveda"] = "pravděpodobně žena (příjmení na -ová/-á), ověř podle křestního jména"
            else:
                k["rod_napoveda"] = "urči podle křestního jména (žena může mít i příjmení bez -ová)"

            if not k["email"]:
                upozorneni.append(f"{kdo} ({k['radek']}): chybí e-mail")
            elif not re.fullmatch(r"[^@\s]+@[^@\s]+\.[a-z]{2,}", k["email"]):
                upozorneni.append(f"{kdo} ({k['radek']}): podezřelý e-mail „{k['email']}“")

            d = parsuj_datum(bunka("datum_narozeni"))
            if d is None:
                k["narozeniny"] = None
                upozorneni.append(f"{kdo} ({k['radek']}): chybí nebo nečitelné datum narození")
            else:
                den, mesic, rok_nar = d
                if mesic_cil:
                    rok = mesic_cil[0]
                else:
                    rok = dnes.year if (mesic, den) >= (dnes.month, dnes.day) else dnes.year + 1
                datum, pozn = datum_narozenin(den, mesic, rok)
                if pozn:
                    upozorneni.append(f"{kdo}: {pozn}")
                k["narozeniny"] = datum.isoformat()
                k["den_v_tydnu"] = DNY[datum.weekday()]
                k["vikend"] = datum.weekday() >= 5
                if mesic_cil and mesic != mesic_cil[1]:
                    upozorneni.append(f"{kdo} ({k['radek']}): narozeniny {den}. {mesic}. nejsou v měsíci "
                                      f"{mesic_cil[1]}/{mesic_cil[0]}")
            klienti.append(k)

    if not prectene_listy:
        print(json.dumps({"chyba": "Nenašel jsem hlavičku se sloupci e-mail a jméno/příjmení. "
                                   "Vypiš první řádky souboru a sloupce urči ručně.",
                          "listy": list(listy)}, ensure_ascii=False, indent=2))
        sys.exit(2)

    videne = {}
    for k in klienti:
        if k["email"]:
            if k["email"] in videne:
                upozorneni.append(f"duplicitní e-mail {k['email']} (řádky {videne[k['email']]} a {k['radek']})")
            videne[k["email"]] = k["radek"]

    klienti.sort(key=lambda k: (k["narozeniny"] or "9999", k["prijmeni"] or k["cele_jmeno"]))
    print(json.dumps({"soubor": cesta, "dnes": dnes.isoformat(),
                      "mesic": f"{mesic_cil[0]}-{mesic_cil[1]:02d}" if mesic_cil else None,
                      "listy": prectene_listy, "pocet_klientu": len(klienti),
                      "klienti": klienti, "upozorneni": upozorneni}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

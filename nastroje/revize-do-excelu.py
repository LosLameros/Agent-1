#!/usr/bin/env python3
# Použití: python3 nastroje/revize-do-excelu.py <vstup.json> <vystup.xlsx>
# Sestaví Excel revize klientských portfolií ve formátu vzoru
# examples/revize-portfolii/Revize_portfolia_vzor.xlsx (listy Přehled, Detail, Překryvy, Kurzy).
# Všechny CZK hodnoty a procenta jsou vzorce (odkazy na list Kurzy a na CELKEM v Přehledu),
# takže změna kurzu v listu Kurzy přepočítá celý sešit. Skript zároveň vypíše spočtené
# hodnoty pro textovou část revize. Struktura vstupního JSON je popsaná
# v .claude/agents/revize-portfolia.md (kapitola 5).
import json
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

ZELENA = "FF00A03C"     # záhlaví a titulek
MANTINEL = "FFD9EAD3"   # mantinely (nedotýkat se)
PREKRYV = "FFFFF3CD"    # překryvy / duplicitní expozice
CELKEM = "FFE9E2F3"     # součtové řádky
NEUVEDENO = "neuvedeno"

TENKA = Side(style="thin", color="FFBFBFBF")
RAMECEK = Border(top=TENKA, bottom=TENKA, left=TENKA, right=TENKA)


def vypln(barva):
    return PatternFill("solid", fgColor=barva)


def font(**kw):
    return Font(name="Arial", size=kw.pop("size", 10), **kw)


def titulek(ws, text, sloupcu):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=sloupcu)
    c = ws.cell(1, 1, text)
    c.font = font(size=14, bold=True, color="FFFFFFFF")
    c.fill = vypln(ZELENA)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 24


def podtitulek(ws, text, sloupcu, vyska=30):
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=sloupcu)
    c = ws.cell(2, 1, text)
    c.font = font(size=9, color="FF333333")
    c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws.row_dimensions[2].height = vyska


def zahlavi(ws, radek, nazvy):
    for i, n in enumerate(nazvy, 1):
        c = ws.cell(radek, i, n)
        c.font = font(bold=True, color="FFFFFFFF")
        c.fill = vypln(ZELENA)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = RAMECEK


def bunka(ws, r, s, hodnota, fmt=None, zarovnani="left", barva=None, tucne=False):
    c = ws.cell(r, s, hodnota)
    c.font = font(bold=tucne)
    c.border = RAMECEK
    c.alignment = Alignment(horizontal=zarovnani, vertical="center", wrap_text=zarovnani == "left")
    if fmt:
        c.number_format = fmt
    if barva:
        c.fill = vypln(barva)
    return c


def poznamky(ws, od_radku, texty, sloupcu):
    r = od_radku
    for t in texty:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=sloupcu)
        c = ws.cell(r, 1, t)
        c.font = font(size=9, color="FF333333")
        c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws.row_dimensions[r].height = max(15, 13 * (len(t) // 120 + 1))
        r += 1
    return r


def sirky(ws, hodnoty):
    for pismeno, w in zip("ABCDEFG", hodnoty):
        ws.column_dimensions[pismeno].width = w
    # tisk na šířku, všechny sloupce na jednu stránku
    ws.page_setup.orientation = "landscape"
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0


def main(vstup, vystup):
    d = json.load(open(vstup, encoding="utf-8"))
    kurzy = {k.upper(): float(v) for k, v in d["kurzy"]["hodnoty"].items()}
    kurzy["CZK"] = 1.0

    def czk(mena, hodnota):
        if hodnota is None:
            return None
        mena = mena.upper()
        if mena not in kurzy:
            sys.exit(f"Chybí kurz pro měnu {mena} (doplň ho do kurzy.hodnoty).")
        return hodnota * kurzy[mena]

    wb = Workbook()
    prehled = wb.active
    prehled.title = "Přehled"
    detail = wb.create_sheet("Detail")
    prekryvy = wb.create_sheet("Překryvy")
    list_kurzy = wb.create_sheet("Kurzy")

    # ---------- Kurzy ----------
    k = d["kurzy"]
    list_kurzy["A1"] = "Přepočet měn – použité kurzy"
    list_kurzy["A1"].font = font(size=12, bold=True)
    radky_kurzu = {}
    r = 3
    list_kurzy.cell(r, 1, "Datum").font = font(bold=True)
    list_kurzy.cell(r, 2, k["datum"]).font = font()
    r += 1
    for mena in [m for m in ["USD", "EUR"] if m in kurzy] + sorted(m for m in kurzy if m not in ("USD", "EUR", "CZK")):
        list_kurzy.cell(r, 1, f"1 {mena} =").font = font(bold=True)
        c = list_kurzy.cell(r, 2, kurzy[mena])
        c.font = font()
        c.number_format = '#,##0.000 "Kč"'
        c.alignment = Alignment(horizontal="left")
        radky_kurzu[mena] = r
        r += 1
    list_kurzy.cell(r, 1, "Měna přepočtu").font = font(bold=True)
    list_kurzy.cell(r, 2, "CZK").font = font()
    r += 1
    list_kurzy.cell(r, 1, "Zdroj").font = font(bold=True)
    c = list_kurzy.cell(r, 2, k["zdroj"])
    c.font = font()
    c.alignment = Alignment(wrap_text=True, vertical="top")
    r += 2
    for t in d.get("poznamky_kurzy", []):
        c = list_kurzy.cell(r, 1, t)
        c.font = font(size=9, color="FF333333")
        r += 1
    sirky(list_kurzy, [16, 70])

    def vzorec_czk(mena, adresa_hodnoty):
        mena = mena.upper()
        if mena == "CZK":
            return f"={adresa_hodnoty}"
        return f"={adresa_hodnoty}*Kurzy!$B${radky_kurzu[mena]}"

    # ---------- Přehled ----------
    pozice = d["pozice"]
    for p in pozice:
        p["_czk"] = czk(p["mena"], p.get("hodnota"))
    pozice.sort(key=lambda p: (p["_czk"] is None, -(p["_czk"] or 0)))
    celkem = sum(p["_czk"] or 0 for p in pozice)

    titulek(prehled, f"Portu – přehled všech portfolií a přímých pozic (přepočet k {k['datum']})", 6)
    meny = ", ".join(f"1 {m} = {kurzy[m]} Kč" for m in radky_kurzu)
    podtitulek(prehled, f"Kurzy: {meny} ({k.get('zdroj_kratce', k['zdroj'])}). Setříděno od nejvyšší hodnoty. "
                        "Desetinná tečka; % na 1 des. místo.", 6)
    zahlavi(prehled, 4, ["Portfolio", "Instrument (název + ticker/ISIN)", "Původní měna",
                         "Hodnota (pův. měna)", "Hodnota v CZK", "Podíl na celku"])
    prvni = 5
    radek_celkem = prvni + len(pozice)
    adresa_pozice = {}
    for i, p in enumerate(pozice):
        r = prvni + i
        barva = MANTINEL if p.get("mantinel") else (PREKRYV if p.get("prekryv") else None)
        bunka(prehled, r, 1, p["portfolio"], barva=barva)
        bunka(prehled, r, 2, p["instrument"], barva=barva)
        bunka(prehled, r, 3, p["mena"].upper(), zarovnani="center", barva=barva)
        if p.get("hodnota") is None:
            for s in (4, 5, 6):
                bunka(prehled, r, s, NEUVEDENO, zarovnani="right", barva=barva)
        else:
            bunka(prehled, r, 4, p["hodnota"], "#,##0.00", "right", barva)
            bunka(prehled, r, 5, vzorec_czk(p["mena"], f"D{r}"), "#,##0.00", "right", barva)
            bunka(prehled, r, 6, f"=E{r}/$E${radek_celkem}", "0.0%", "right", barva)
        if p.get("id"):
            adresa_pozice[p["id"]] = f"'Přehled'!E{r}"
    for s in range(1, 7):
        bunka(prehled, radek_celkem, s, None, barva=CELKEM, tucne=True)
    prehled.cell(radek_celkem, 1, "CELKEM")
    prehled.cell(radek_celkem, 5, f"=SUM(E{prvni}:E{radek_celkem - 1})").number_format = "#,##0.00"
    prehled.cell(radek_celkem, 6, f"=SUM(F{prvni}:F{radek_celkem - 1})").number_format = "0.0%"
    for s in (5, 6):
        prehled.cell(radek_celkem, s).alignment = Alignment(horizontal="right")
    poz = ["Zeleně = MANTINELY (nedotýkat se; do součtu a % se ale počítají)."]
    if any(p.get("hodnota") is None for p in pozice):
        poz.append("Pozor: některé hodnoty nejsou na printscreenech čitelné (neuvedeno) – CELKEM je proto neúplný.")
    poznamky(prehled, radek_celkem + 2, poz + d.get("poznamky_prehled", []), 6)
    sirky(prehled, [26, 42, 12, 20, 18, 14])
    prehled.freeze_panes = "A5"
    CELEK = f"'Přehled'!$E${radek_celkem}"

    # ---------- Detail ----------
    poradi = {}
    for p in pozice:
        poradi.setdefault(p["portfolio"], len(poradi))
    slozky = d.get("slozky", [])
    for s in slozky:
        s["_czk"] = czk(s["mena"], s.get("hodnota"))
    slozky.sort(key=lambda s: (poradi.get(s["portfolio"], 999), s["portfolio"],
                               s["_czk"] is None, -(s["_czk"] or 0)))

    titulek(detail, "Detail viditelných složek portfolií", 7)
    podtitulek(detail, d.get("upozorneni_detail",
                             "POZOR: zobrazeny jen složky viditelné na printscreenech. Hodnoty složek jsou "
                             "vnitřní podíly portfolií – NEsčítají se do celku znovu, celkovou hodnotu drží list Přehled."),
               7, vyska=42)
    zahlavi(detail, 4, ["Portfolio", "Instrument / složka", "Původní měna", "Hodnota (pův. měna)",
                        "Hodnota v CZK", "Zastoupení v portfoliu", "Podíl na celku"])
    adresa_slozky = {}
    for i, s in enumerate(slozky):
        r = 5 + i
        barva = PREKRYV if s.get("prekryv") else None
        bunka(detail, r, 1, s["portfolio"], barva=barva)
        bunka(detail, r, 2, s["instrument"], barva=barva)
        bunka(detail, r, 3, s["mena"].upper(), zarovnani="center", barva=barva)
        if s.get("hodnota") is None:
            bunka(detail, r, 4, NEUVEDENO, zarovnani="right", barva=barva)
            bunka(detail, r, 5, NEUVEDENO, zarovnani="right", barva=barva)
            bunka(detail, r, 7, NEUVEDENO, zarovnani="right", barva=barva)
        else:
            bunka(detail, r, 4, s["hodnota"], "#,##0.00", "right", barva)
            bunka(detail, r, 5, vzorec_czk(s["mena"], f"D{r}"), "#,##0.00", "right", barva)
            bunka(detail, r, 7, f"=E{r}/{CELEK}", "0.0%", "right", barva)
        z = s.get("zastoupeni")
        bunka(detail, r, 6, NEUVEDENO if z is None else z, None if z is None else "0.0%", "right", barva)
        if s.get("id"):
            adresa_slozky[s["id"]] = f"Detail!E{r}"
    poznamky(detail, 5 + len(slozky) + 1,
             ["Žlutě = složka, která se objevuje i v jiném portfoliu / jako přímá pozice (překryv – viz list Překryvy)."]
             + d.get("poznamky_detail", []), 7)
    sirky(detail, [22, 40, 12, 20, 18, 20, 14])
    detail.freeze_panes = "A5"

    # ---------- Překryvy ----------
    adresy = {**adresa_pozice, **adresa_slozky}
    hodnoty = {p["id"]: p["_czk"] for p in pozice if p.get("id")}
    hodnoty.update({s["id"]: s["_czk"] for s in slozky if s.get("id")})

    def soucet(refs):
        chybi = [x for x in refs if x not in adresy]
        if chybi:
            sys.exit(f"Překryvy odkazují na neznámá id: {', '.join(chybi)}")
        platne = [x for x in refs if hodnoty[x] is not None]
        vzorec = "=" + "+".join(adresy[x] for x in platne) if platne else NEUVEDENO
        return vzorec, sum(hodnoty[x] for x in platne), len(platne) < len(refs)

    titulek(prekryvy, "Překryvy a duplicitní expozice napříč portfolii", 4)
    podtitulek(prekryvy, "Stejný / velmi podobný instrument sečtený napříč portfolii. CZK přes kurzy z listu Kurzy. "
                         "% z celku (list Přehled).", 4)
    zahlavi(prekryvy, 4, ["Instrument / expozice", "Ve kterých portfoliích (počet)",
                          "Hodnota v CZK (součet)", "Podíl na celku"])
    vypis = []
    radky = []
    for p in d.get("prekryvy", []):
        f, v, neuplne = soucet(p["refs"])
        radky.append((v, p, f, neuplne))
    radky.sort(key=lambda x: -x[0])
    r = 5
    for v, p, f, neuplne in radky:
        bunka(prekryvy, r, 1, p["expozice"], barva=PREKRYV)
        bunka(prekryvy, r, 2, p["portfolia"])
        bunka(prekryvy, r, 3, f, "#,##0.00", "right")
        bunka(prekryvy, r, 4, f"=C{r}/{CELEK}" if f != NEUVEDENO else NEUVEDENO, "0.0%", "right")
        vypis.append((p["expozice"], v, neuplne))
        r += 1
    for blok in d.get("tematicke_bloky", []):
        r += 1
        prekryvy.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
        c = bunka(prekryvy, r, 1, blok["nazev"].upper(), barva=PREKRYV, tucne=True)
        r += 1
        od = r
        polozky = []
        for pol in blok["polozky"]:
            f, v, neuplne = soucet(pol["refs"])
            polozky.append((v, pol, f))
        polozky.sort(key=lambda x: -x[0])
        for v, pol, f in polozky:
            bunka(prekryvy, r, 1, "   " + pol["popis"])
            bunka(prekryvy, r, 2, pol["portfolia"])
            bunka(prekryvy, r, 3, f, "#,##0.00", "right")
            bunka(prekryvy, r, 4, f"=C{r}/{CELEK}" if f != NEUVEDENO else NEUVEDENO, "0.0%", "right")
            r += 1
        for s in range(1, 5):
            bunka(prekryvy, r, s, None, barva=CELKEM, tucne=True)
        prekryvy.cell(r, 1, f"{blok['nazev_celkem']}")
        prekryvy.cell(r, 3, f"=SUM(C{od}:C{r - 1})").number_format = "#,##0.00"
        prekryvy.cell(r, 4, f"=C{r}/{CELEK}").number_format = "0.0%"
        for s in (3, 4):
            prekryvy.cell(r, s).alignment = Alignment(horizontal="right")
        vypis.append((blok["nazev_celkem"], sum(x[0] for x in polozky), False))
        r += 1
    poznamky(prekryvy, r + 1, d.get("poznamky_prekryvy", []), 4)
    sirky(prekryvy, [46, 52, 24, 14])
    prekryvy.freeze_panes = "A5"

    wb.save(vystup)

    # ---------- Kontrolní výpis pro textovou část revize ----------
    print(f"Uloženo: {vystup}")
    print(f"CELKEM: {celkem:,.2f} CZK")
    print("\nPřehled (od největší):")
    for p in pozice:
        v = p["_czk"]
        print(f"  {p['portfolio']} | {p['instrument']} | "
              + (NEUVEDENO if v is None else f"{v:,.2f} CZK | {v / celkem:.1%}")
              + (" | MANTINEL" if p.get("mantinel") else ""))
    print("\nPřekryvy:")
    for nazev, v, neuplne in vypis:
        print(f"  {nazev} | {v:,.2f} CZK | {v / celkem:.1%}" + (" | NEÚPLNÉ (část neuvedeno)" if neuplne else ""))
    soucty = {}
    for s in slozky:
        soucty[s["portfolio"]] = soucty.get(s["portfolio"], 0) + (s["_czk"] or 0)
    print("\nKontrola: viditelné složky vs. hodnota portfolia v Přehledu:")
    for p in pozice:
        if p["portfolio"] in soucty and p["_czk"]:
            print(f"  {p['portfolio']}: složky {soucty[p['portfolio']]:,.2f} / portfolio {p['_czk']:,.2f} CZK "
                  f"({soucty[p['portfolio']] / p['_czk']:.1%})")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Použití: python3 nastroje/revize-do-excelu.py <vstup.json> <vystup.xlsx>")
    main(sys.argv[1], sys.argv[2])

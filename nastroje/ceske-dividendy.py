#!/usr/bin/env python3
# Použití: python3 nastroje/ceske-dividendy.py podklady/ceske-dividendy/data.json \
#              podklady/ceske-dividendy/vesmir.json vystupy/ceske-dividendy/Ceske-dividendy-vypocet.xlsx
# Sestaví Excel s výpočtem strategie České dividendy: filtry, skóre, stropy, váhy, historii dividend,
# historické výnosy, kalendář výplat a likviditu. Všechny výpočty jsou v sešitu jako vzorce nad listem
# Vstupy a Dividendy, takže změna ceny, dividendy nebo parametru přepočítá celý sešit.
# Skript stejné hodnoty spočítá i sám a vypíše je, aby šly porovnat s přepočteným sešitem.
import datetime
import json
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L

PORTU = "FF4840BB"
SVETLA = "FFE9E2F3"
VSTUP = "FF0000FF"      # modré písmo = ručně zadaný vstup
TENKA = Side(style="thin", color="FFBFBFBF")
RAM = Border(top=TENKA, bottom=TENKA, left=TENKA, right=TENKA)
PCT1, PCT2, KC, KC2, CISLO = "0.0%", "0.00%", "#,##0", "#,##0.00", "0.00"
ROKY = list(range(2000, 2027))
R0 = 5                    # první datový řádek tabulek
POSL = 2026


def font(**kw):
    return Font(name="Rethink Sans", size=kw.pop("size", 10), **kw)


def titulek(ws, text, pod, sloupcu):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=sloupcu)
    c = ws.cell(1, 1, text)
    c.font = font(size=14, bold=True, color="FFFFFFFF")
    c.fill = PatternFill("solid", fgColor=PORTU)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 26
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=sloupcu)
    c = ws.cell(2, 1, pod)
    c.font = font(size=9, color="FF333333")
    c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True, indent=1)
    ws.row_dimensions[2].height = 42


def zahlavi(ws, radek, nazvy, vyska=44, od=1):
    for i, n in enumerate(nazvy, od):
        c = ws.cell(radek, i, n)
        c.font = font(bold=True, color="FFFFFFFF")
        c.fill = PatternFill("solid", fgColor=PORTU)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = RAM
    ws.row_dimensions[radek].height = vyska


def bunka(ws, r, c, v, fmt=None, vstup=False, tucne=False, vypln=None, zarovnat=None, zalomit=False):
    x = ws.cell(r, c, v)
    x.font = font(bold=tucne, color=VSTUP if vstup else "FF000000")
    x.border = RAM
    if fmt:
        x.number_format = fmt
    if vypln:
        x.fill = PatternFill("solid", fgColor=vypln)
    if zarovnat or zalomit:
        x.alignment = Alignment(horizontal=zarovnat, vertical="center", wrap_text=zalomit)
    return x


def sirky(ws, s):
    for i, w in enumerate(s, 1):
        ws.column_dimensions[L(i)].width = w


def mezititulek(ws, r, text):
    c = ws.cell(r, 1, text)
    c.font = font(bold=True, size=11, color=PORTU)


def main():
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    vesmir = json.load(open(sys.argv[2], encoding="utf-8"))
    out = sys.argv[3]
    T = data["tituly"]
    ids = [t["id"] for t in T]
    n = len(T)
    P = data["parametry"]
    eur = data["eurczk"]
    d = datetime.date.fromisoformat(data["datum"])
    datum = f"{d.day}. {d.month}. {d.year}"
    RK = R0 + n - 1          # poslední řádek tabulek s tituly

    # ------------------------------------------------------------------ výpočet v Pythonu (kontrola)
    def fx(t):
        return eur if t["mena_div"] == "EUR" else 1.0

    def rada(i):
        prvni = data["prvni_rok"][i]
        return {y: (data["dividendy"][i].get(str(y), 0.0) if y >= prvni else None) for y in ROKY}

    vyp = {}
    px_vynos = sum(t["px"] * t["div12m"] * fx(t) / t["cena"] for t in T)
    for t in T:
        i = t["id"]
        r = rada(i)
        p10 = [r[y] for y in range(POSL - 9, POSL + 1)]
        let10 = sum(1 for v in p10 if v)
        bez = sum(1 for y in range(POSL - 9, POSL + 1)
                  if r[y] and r[y] >= (r[y - 1] or 0) * (1 - P["tolerance_snizeni"]))
        let5 = sum(1 for y in range(POSL - 4, POSL + 1) if r[y])
        S = (let10 + bez) * 5
        stare = [r[y] for y in (2017, 2018, 2019)]
        rust = None
        if all(stare):
            rust = (sum(r[y] for y in (2024, 2025, 2026)) / sum(stare)) ** (1 / 7) - 1
        bp = 0
        if t["pomer"]:
            bp = next((b for h, b in P["body_vyplatni_pomer"] if t["pomer"] <= h), 0)
        br = 0 if rust is None else next((b for h, b in P["body_rust"] if rust >= h), 0)
        q = 0.5 + (S + bp + br) / 200
        hruby12 = t["div12m"] * fx(t) / t["cena"]
        dostupne = min(5, POSL - data["prvni_rok"][i] + 1)
        f_div = t["div12m"] > 0 and let5 >= max(2, min(P["min_vyplat_z_5_let"], dostupne))
        f_lik = t["objem"] >= P["min_objem_mil"] and t["dnu"] >= P["min_dnu_obchodovani"]
        f_vyn = hruby12 >= P["podil_vynosu_px"] * px_vynos
        ok = f_div and f_lik and f_vyn
        c26 = t["div2026"] * fx(t) / t["cena"] * (1 - t["srazka"])
        c27 = t["div2027"] * fx(t) / t["cena"] * (1 - t["srazka"])
        strop_l = next((s for h, s in P["pasma_likvidity"] if t["objem"] >= h), 0)
        strop_h = P["strop_novacek"] if POSL - data["prvni_rok"][i] + 1 < P["novacek_let"] else P["strop_titul"]
        vyp[i] = dict(let10=let10, bez=bez, let5=let5, S=S, rust=rust, bp=bp, br=br, q=q, hruby12=hruby12,
                      f_div=f_div, f_lik=f_lik, f_vyn=f_vyn, ok=ok, c26=c26, c27=c27,
                      skore=(c26 + c27) / 2 * q if ok else 0.0, strop=min(P["strop_titul"], strop_l, strop_h))
    celkem = sum(v["skore"] for v in vyp.values())
    w = {i: vyp[i]["skore"] / celkem for i in ids}
    pred = dict(w)
    zastropovane = set()
    for _ in range(10):
        nad = [i for i in ids if i not in zastropovane and w[i] > vyp[i]["strop"] + 1e-9]
        if not nad:
            break
        zastropovane |= set(nad)
        zbyva = 1 - sum(vyp[i]["strop"] for i in zastropovane)
        zaklad = sum(vyp[i]["skore"] for i in ids if i not in zastropovane)
        w = {i: (vyp[i]["strop"] if i in zastropovane else vyp[i]["skore"] / zaklad * zbyva) for i in ids}
    # zaokrouhlení na celá procenta metodou největších zbytků
    cele = {i: int(w[i] * 100) for i in ids}
    for i in sorted(ids, key=lambda k: -(w[k] * 100 - cele[k]))[:100 - sum(cele.values())]:
        cele[i] += 1
    cil = {i: cele[i] / 100 for i in ids}

    wb = Workbook()

    # ------------------------------------------------------------------ list Vstupy
    wv = wb.active
    wv.title = "Vstupy"
    titulek(wv, "Vstupy a parametry",
            f"Ceny, počty akcií, free float a váhy indexu PX: pse.cz k {datum}. Dividendy: Fio banka a stránky emitentů. "
            "Modré hodnoty jsou ručně zadané vstupy, černé jsou vzorce. Zdroje jsou na listu Zdroje.", 22)
    par = [
        ("eur", "Kurz EUR/CZK (ČNB)", eur, CISLO, f"Kurz devizového trhu ČNB k {datum}"),
        ("min_objem", "Minimální medián denního objemu (mil. Kč)", P["min_objem_mil"], CISLO,
         "Filtr likvidity. Index PX požaduje průměr 2 mil. Kč nebo kapitalizaci nad 0,5 mld. Kč"),
        ("min_dnu", "Minimální podíl dnů s obchodem", P["min_dnu_obchodovani"], PCT1, "Stejně jako pravidla indexu PX"),
        ("min5", "Minimální počet let s výplatou z posledních 5", P["min_vyplat_z_5_let"], "0", "Obdoba pravidla polského indexu WIGdiv"),
        ("podil_px", "Práh výnosu jako podíl výnosu indexu PX", P["podil_vynosu_px"], PCT1,
         "Titul musí za 12 měsíců vyplatit aspoň polovinu toho, co trh"),
        ("tol", "Tolerance poklesu dividendy", P["tolerance_snizeni"], PCT1, "Pokles do 5 % nepočítám jako snížení"),
        ("strop", "Strop na jeden titul", P["strop_titul"], PCT1, "Stejný strop má index PX"),
        ("strop_nov", "Strop pro nováčka", P["strop_novacek"], PCT1, "Titul s krátkou dividendovou historií"),
        ("nov_let", "Nováček: dividendová historie kratší než (let)", P["novacek_let"], "0", ""),
        ("strop_fin", "Strop pro finanční sektor", P["strop_finance"], PCT1, "Banky a pojišťovny dohromady"),
        ("aum", "Referenční objem strategie (mil. Kč)", P["referencni_aum_mil"], KC,
         "Můj předpoklad pro nastavení pásem likvidity. Upravte podle očekávání Portu"),
        ("podil_obj", "Podíl na denním objemu při obchodování", P["podil_na_objemu"], PCT1,
         "Kolik denního objemu lze zobchodovat bez pohybu ceny"),
        ("rok", "Poslední rok výplat", POSL, "0", ""),
    ]
    mezititulek(wv, 4, "Parametry metodiky")
    A = {}
    for k, (kod, popis, hod, fmt, pozn) in enumerate(par):
        r = 5 + k
        bunka(wv, r, 1, popis)
        bunka(wv, r, 2, hod, fmt, vstup=True)
        wv.cell(r, 3, pozn).font = font(size=9, color="FF555555")
        A[kod] = f"Vstupy!$B${r}"
    r = 5 + len(par) + 1
    mezititulek(wv, r, "Pásma likvidity: medián denního objemu od (mil. Kč) a strop váhy")
    pas = []
    for k, (h, s) in enumerate(P["pasma_likvidity"]):
        bunka(wv, r + 1 + k, 1, h, CISLO, vstup=True)
        bunka(wv, r + 1 + k, 2, s, PCT1, vstup=True)
        pas.append((f"Vstupy!$A${r + 1 + k}", f"Vstupy!$B${r + 1 + k}"))
    r += len(pas) + 2
    mezititulek(wv, r, "Body za výplatní poměr: poměr do a počet bodů (nad poslední hranici 0 bodů)")
    bpom = []
    for k, (h, b) in enumerate(P["body_vyplatni_pomer"]):
        bunka(wv, r + 1 + k, 1, h, PCT1, vstup=True)
        bunka(wv, r + 1 + k, 2, b, "0", vstup=True)
        bpom.append((f"Vstupy!$A${r + 1 + k}", f"Vstupy!$B${r + 1 + k}"))
    r += len(bpom) + 2
    mezititulek(wv, r, "Body za růst dividendy: růst ročně od a počet bodů (pod poslední hranici 0 bodů)")
    brus = []
    for k, (h, b) in enumerate(P["body_rust"]):
        bunka(wv, r + 1 + k, 1, h, PCT1, vstup=True)
        bunka(wv, r + 1 + k, 2, b, "0", vstup=True)
        brus.append((f"Vstupy!$A${r + 1 + k}", f"Vstupy!$B${r + 1 + k}"))
    r += len(brus) + 2
    mezititulek(wv, r, f"Tituly, které prošly filtrem trhu a likvidity (ceny k {datum})")
    VH = r + 1
    V0 = VH + 1
    VK = V0 + n - 1
    hl = ["Titul", "ISIN", "Trh", "Sektor", "Země emitenta", "Finanční sektor (1 = ano)", "Cena (Kč)", "Měna dividendy",
          "Počet akcií", "Tržní kapitalizace (mil. Kč)", "Free float podle indexu PX",
          "Medián denního objemu za 6 měsíců (mil. Kč)", "Podíl dnů s obchodem", "Srážková daň u zdroje",
          "Řádná dividenda 2026 (v měně dividendy)", "Mimořádná dividenda 2026", "Dividendy za posledních 12 měsíců",
          "Odhad dividendy 2027", "Výplatní poměr z posledního zisku", "Váha v indexu PX", "Váha v ETF při startu (září 2026)",
          "Z čeho odhad 2027 vychází"]
    zahlavi(wv, VH, hl, 58)
    pole = ["nazev", "isin", "trh", "sektor", "zeme", "finance", "cena", "mena_div", "akcii", None, "ff", "objem", "dnu",
            "srazka", "div2026", "div2026_mimo", "div12m", "div2027", "pomer", "px", "etf_start", "pozn2027"]
    fmts = [None, None, None, None, None, "0", KC2, None, KC, KC, PCT1, CISLO, PCT1, PCT1, KC2, KC2, KC2, KC2, PCT1, PCT2, PCT1, None]
    for k, t in enumerate(T):
        r = V0 + k
        for c, (p, f) in enumerate(zip(pole, fmts), 1):
            if p is None:
                bunka(wv, r, c, f"=G{r}*I{r}/1000000", f)
            else:
                v = t[p]
                if p == "pomer" and not v:
                    v = None
                bunka(wv, r, c, v, f, vstup=c > 5, zalomit=(p == "pozn2027"))
    VS = {p: L(c) for c, p in enumerate(pole, 1) if p}

    def vst(pole_, k, abs_=True):
        return f"Vstupy!${VS[pole_]}${V0 + k}" if abs_ else f"Vstupy!{VS[pole_]}{V0 + k}"

    def vrozsah(pole_):
        return f"Vstupy!${VS[pole_]}${V0}:${VS[pole_]}${VK}"

    def kurz(k):
        return f'IF({vst("mena_div", k)}="EUR",{A["eur"]},1)'

    sirky(wv, [34, 15, 10, 16, 13, 10, 11, 9, 14, 13, 10, 13, 10, 10, 13, 11, 12, 10, 11, 9, 11, 70])
    wv.freeze_panes = wv.cell(V0, 2)

    # ------------------------------------------------------------------ list Dividendy
    wd = wb.create_sheet("Dividendy")
    titulek(wd, "Historie dividend na akcii",
            "Hrubá dividenda podle roku, kdy se akcie začala obchodovat bez nároku. Erste a VIG v EUR, ostatní v Kč. "
            "KB přepočtena na štěpení 1:5 (2016), Erste na štěpení 1:4 (2004). Prázdné pole = titul se ještě neobchodoval "
            "nebo starší data nemám, nula = nevyplaceno.", n + 1)
    nazvy = [t["nazev"] + (" (EUR)" if t["mena_div"] == "EUR" else "") for t in T]
    NR = len(ROKY)
    B1, B2, B3 = R0, R0 + NR + 3, R0 + 2 * (NR + 3)           # řádné, mimořádné, celkem
    B4 = B3 + NR + 3                                          # bez snížení (posledních 10 let)
    B5 = B4 + 10 + 3                                          # řada let s výplatou
    bloky = [(B1, "Řádná dividenda"), (B2, "Mimořádná dividenda (výplata z nerozděleného zisku minulých let)"),
             (B3, "Celkem vyplaceno"), (B4, "Rok bez snížení řádné dividendy (1 = ano), posledních 10 let"),
             (B5, "Počet let s výplatou v řadě")]
    for b, text in bloky:
        mezititulek(wd, b - 2, text)
        zahlavi(wd, b - 1, ["Rok"] + nazvy, 40)
    mezititulek(wd, B1 - 2, "Řádná dividenda")
    for k, t in enumerate(T):
        i, c = t["id"], k + 2
        col = L(c)
        r_ = rada(i)
        for j, y in enumerate(ROKY):
            if k == 0:
                for b in (B1, B2, B3, B5):
                    bunka(wd, b + j, 1, y, "0")
            bunka(wd, B1 + j, c, r_[y], KC2, vstup=True)
            bunka(wd, B2 + j, c, data["mimoradne"].get(i, {}).get(str(y)), KC2, vstup=True)
            bunka(wd, B3 + j, c, f'=IF(AND({col}{B1 + j}="",{col}{B2 + j}=""),"",N({col}{B1 + j})+N({col}{B2 + j}))', KC2)
            cur = f"{col}{B1 + j}"
            if j == 0:
                bunka(wd, B5 + j, c, f"=IF(AND(ISNUMBER({cur}),{cur}>0),1,0)", "0")
            else:
                bunka(wd, B5 + j, c, f"=IF(AND(ISNUMBER({cur}),{cur}>0),{col}{B5 + j - 1}+1,0)", "0")
        for j, y in enumerate(range(POSL - 9, POSL + 1)):
            if k == 0:
                bunka(wd, B4 + j, 1, y, "0")
            rr = B1 + (y - ROKY[0])
            bunka(wd, B4 + j, c,
                  f'=IF(AND(ISNUMBER({col}{rr}),{col}{rr}>0,{col}{rr}>=N({col}{rr - 1})*(1-{A["tol"]})),1,0)', "0")
    sirky(wd, [8] + [15] * n)
    wd.freeze_panes = "B5"

    def drow(y):
        return B1 + (y - ROKY[0])

    # ------------------------------------------------------------------ list Spolehlivost
    wsp = wb.create_sheet("Spolehlivost")
    titulek(wsp, "Spolehlivost a udržitelnost dividendy",
            "Spolehlivost (0–100 bodů): 5 bodů za každý z posledních 10 let s výplatou a 5 bodů za každý rok bez snížení řádné "
            "dividendy. Udržitelnost (0–100 bodů): body za výplatní poměr a za růst dividendy (průměr 2024–2026 proti průměru "
            "2017–2019). Koeficient = 0,5 + (spolehlivost + udržitelnost) / 200, tedy od 0,5 do 1,5.", 16)
    zahlavi(wsp, 4, ["Titul", "První rok výplaty v datech", "Let s výplatou celkem", "Let s výplatou v řadě",
                     "Let s výplatou z posledních 10", "Let bez snížení z posledních 10", "Let s výplatou z posledních 5",
                     "Body: spolehlivost", "Průměrná dividenda 2024–2026", "Průměrná dividenda 2017–2019",
                     "Růst dividendy ročně", "Výplatní poměr", "Body: výplatní poměr", "Body: růst",
                     "Body: udržitelnost", "Koeficient spolehlivosti"], 58)
    for k, t in enumerate(T):
        r, col = R0 + k, L(k + 2)
        dl = lambda a, b: f"Dividendy!${col}${drow(a)}:${col}${drow(b)}"
        bunka(wsp, r, 1, f"={vst('nazev', k)}")
        bunka(wsp, r, 2, data["prvni_rok"][t["id"]], "0", vstup=True)
        bunka(wsp, r, 3, f'=COUNTIF({dl(ROKY[0], POSL)},">0")', "0")
        bunka(wsp, r, 4, f"=Dividendy!{col}{B5 + NR - 1}", "0")
        bunka(wsp, r, 5, f'=COUNTIF({dl(POSL - 9, POSL)},">0")', "0")
        bunka(wsp, r, 6, f"=SUM(Dividendy!{col}{B4}:{col}{B4 + 9})", "0")
        bunka(wsp, r, 7, f'=COUNTIF({dl(POSL - 4, POSL)},">0")', "0")
        bunka(wsp, r, 8, f"=(E{r}+F{r})*5", "0")
        bunka(wsp, r, 9, f'=IF(COUNTIF({dl(2017, 2019)},">0")=3,AVERAGE({dl(2024, 2026)}),"")', KC2)
        bunka(wsp, r, 10, f'=IF(COUNTIF({dl(2017, 2019)},">0")=3,AVERAGE({dl(2017, 2019)}),"")', KC2)
        bunka(wsp, r, 11, f'=IF(ISNUMBER(J{r}),(I{r}/J{r})^(1/7)-1,"krátká historie")', PCT1, zarovnat="right")
        bunka(wsp, r, 12, f'=IF(ISNUMBER({vst("pomer", k)}),{vst("pomer", k)},"")', PCT1)
        f = "0"
        for h, b in reversed(bpom):
            f = f"IF(L{r}<={h},{b},{f})"
        bunka(wsp, r, 13, f"=IF(ISNUMBER(L{r}),{f},0)", "0")
        f = "0"
        for h, b in reversed(brus):
            f = f"IF(K{r}>={h},{b},{f})"
        bunka(wsp, r, 14, f"=IF(ISNUMBER(K{r}),{f},0)", "0")
        bunka(wsp, r, 15, f"=M{r}+N{r}", "0")
        bunka(wsp, r, 16, f"=0.5+(H{r}+O{r})/200", "0.000", tucne=True)
    sirky(wsp, [26] + [12] * 15)
    wsp.freeze_panes = "B5"

    # ------------------------------------------------------------------ list Výpočet vah
    wvv = wb.create_sheet("Výpočet vah")
    titulek(wvv, "Výpočet vah",
            "Postup: 1) filtry (dividenda, likvidita, výnos), 2) skóre = čistý dividendový výnos × koeficient spolehlivosti, "
            "3) váha podle skóre, 4) stropy (titul, likvidita, nováček) a rozdělení přebytku mezi nezastropované tituly "
            "ve stejném poměru (pět kol), 5) zaokrouhlení na celá procenta. Cílová váha je ruční vstup.", 30)
    hl = ["Titul", "Dividendy za 12 měsíců (Kč)", "Hrubý výnos za 12 měsíců", "Let s výplatou z posledních 5",
          "Filtr: dividenda", "Filtr: likvidita", "Filtr: výnos", "Prošel filtry", "Čistý výnos 2026 (řádná dividenda)",
          "Čistý výnos 2027 (odhad)", "Výnos pro váhu (průměr)", "Koeficient spolehlivosti", "Skóre (výnos × koeficient)",
          "Váha před stropy", "Strop: likvidita", "Strop: historie", "Výsledný strop"]
    for kolo in range(1, 6):
        hl += [f"Kolo {kolo}: na stropu", f"Kolo {kolo}: váha"]
    hl += ["Váha podle modelu", "Cílová váha", "Rozdíl proti modelu"]
    zahlavi(wvv, 4, hl, 58)
    VV = "'Výpočet vah'"
    rng = lambda c: f"${c}${R0}:${c}${RK}"
    for k, t in enumerate(T):
        r = R0 + k
        bunka(wvv, r, 1, f"={vst('nazev', k)}")
        bunka(wvv, r, 2, f"={vst('div12m', k)}*{kurz(k)}", KC2)
        bunka(wvv, r, 3, f"=B{r}/{vst('cena', k)}", PCT2)
        bunka(wvv, r, 4, f"=Spolehlivost!G{r}", "0")
        bunka(wvv, r, 5, f"=IF(AND(B{r}>0,D{r}>=MAX(2,MIN({A['min5']},{A['rok']}-Spolehlivost!B{r}+1))),1,0)", "0")
        bunka(wvv, r, 6, f"=IF(AND({vst('objem', k)}>={A['min_objem']},{vst('dnu', k)}>={A['min_dnu']}),1,0)", "0")
        bunka(wvv, r, 7, f"=IF(C{r}>={A['podil_px']}*$C${RK + 3},1,0)", "0")
        bunka(wvv, r, 8, f"=E{r}*F{r}*G{r}", "0", tucne=True)
        bunka(wvv, r, 9, f"={vst('div2026', k)}*{kurz(k)}/{vst('cena', k)}*(1-{vst('srazka', k)})", PCT2)
        bunka(wvv, r, 10, f"={vst('div2027', k)}*{kurz(k)}/{vst('cena', k)}*(1-{vst('srazka', k)})", PCT2)
        bunka(wvv, r, 11, f"=AVERAGE(I{r}:J{r})", PCT2)
        bunka(wvv, r, 12, f"=Spolehlivost!P{r}", "0.000")
        bunka(wvv, r, 13, f"=H{r}*K{r}*L{r}*100", "0.00")
        bunka(wvv, r, 14, f"=M{r}/SUM({rng('M')})", PCT1)
        f = "0"
        for h, s in reversed(pas):
            f = f"IF({vst('objem', k)}>={h},{s},{f})"
        bunka(wvv, r, 15, f"={f}", PCT1)
        bunka(wvv, r, 16, f"=IF({A['rok']}-Spolehlivost!B{r}+1<{A['nov_let']},{A['strop_nov']},{A['strop']})", PCT1)
        bunka(wvv, r, 17, f"=MIN({A['strop']},O{r},P{r})", PCT1, tucne=True)
        predchozi = "N"
        for kolo in range(5):
            cf, cw = L(18 + 2 * kolo), L(19 + 2 * kolo)
            if kolo == 0:
                bunka(wvv, r, 18, f"=IF(N{r}>$Q{r}+0.0000001,1,0)", "0")
            else:
                pf = L(16 + 2 * kolo)
                bunka(wvv, r, 18 + 2 * kolo, f"=IF(OR({pf}{r}=1,{predchozi}{r}>$Q{r}+0.0000001),1,0)", "0")
            bunka(wvv, r, 19 + 2 * kolo,
                  f"=IF($M{r}=0,0,IF({cf}{r}=1,$Q{r},IFERROR($M{r}*(1-SUMPRODUCT({rng(cf)},{rng('Q')}))"
                  f"/SUMPRODUCT((1-{rng(cf)})*{rng('M')}),0)))", PCT2)
            predchozi = cw
        bunka(wvv, r, 28, f"=AA{r}", PCT2, tucne=True)
        bunka(wvv, r, 29, cil[t["id"]], "0%", vstup=True, tucne=True, vypln=SVETLA)
        bunka(wvv, r, 30, f"=AC{r}-AB{r}", "+0.0%;-0.0%;0.0%")
    r = RK + 1
    bunka(wvv, r, 1, "Celkem", tucne=True, vypln=SVETLA)
    for c in (8, 13, 14, 19, 21, 23, 25, 27, 28, 29):
        col = L(c)
        bunka(wvv, r, c, f"=SUM({col}{R0}:{col}{RK})", {8: "0", 13: "0.00", 29: "0%"}.get(c, PCT1), tucne=True, vypln=SVETLA)
    r = RK + 3
    bunka(wvv, r, 1, "Dividendový výnos indexu PX za 12 měsíců")
    bunka(wvv, r, 3, f"=SUMPRODUCT({vrozsah('px')},{rng('C')})", PCT2)
    wvv.cell(r, 4, "Váhy indexu PX × hrubé výnosy. Čtyři nejmenší emise indexu (0,6 % váhy) počítám s nulou.").font = font(size=9, color="FF555555")
    bunka(wvv, r + 1, 1, "Práh hrubého výnosu pro zařazení")
    bunka(wvv, r + 1, 3, f"={A['podil_px']}*C{r}", PCT2)
    bunka(wvv, r + 2, 1, "Váha finančního sektoru (cílové váhy)")
    bunka(wvv, r + 2, 3, f"=SUMPRODUCT({vrozsah('finance')},{rng('AC')})", PCT1)
    bunka(wvv, r + 3, 1, "Kontrola: finanční sektor do stropu")
    bunka(wvv, r + 3, 3, f'=IF(C{r + 2}<={A["strop_fin"]}+0.0000001,"v pořádku","překročen")', zarovnat="right")
    bunka(wvv, r + 4, 1, "Kontrola: cílové váhy dávají 100 %")
    bunka(wvv, r + 4, 3, f'=IF(ABS(AC{RK + 1}-1)<0.0000001,"v pořádku","nesedí")', zarovnat="right")
    bunka(wvv, r + 5, 1, "Kontrola: žádná cílová váha nad stropem")
    bunka(wvv, r + 5, 3, f'=IF(SUMPRODUCT(--({rng("AC")}>{rng("Q")}+0.0000001))=0,"v pořádku","překročen")', zarovnat="right")
    sirky(wvv, [38, 12, 11, 10, 9, 9, 9, 9, 12, 12, 11, 11, 11, 10, 10, 10, 10] + [8, 9] * 5 + [11, 10, 11])
    wvv.freeze_panes = "B5"

    # ------------------------------------------------------------------ list Složení
    ws = wb.create_sheet("Složení", 0)
    titulek(ws, "České dividendy: navržené složení",
            f"Ceny k {datum}. Výnos 2026 = dividendy vyplacené v roce 2026 (včetně mimořádných) k dnešní ceně. Čistý výnos = po "
            "srážkové dani u zdroje (ČR 15 %, Rakousko 27,5 %). Výnos 2027 je odhad. Váha ETF je odhad z dnešních vah indexu PX, "
            "fond drží deset největších emisí indexu.", 15)
    zahlavi(ws, 4, ["Titul", "ISIN", "Trh", "Sektor", "Cena (Kč)", "Váha: České dividendy", "Váha: WOOD PX ETF (odhad)",
                    "Rozdíl (p. b.)", "Dividenda 2026 (Kč)", "Hrubý výnos 2026", "Čistý výnos 2026",
                    "Odhad dividendy 2027 (Kč)", "Hrubý výnos 2027 (odhad)", "Čistý výnos 2027 (odhad)",
                    "Medián denního objemu (mil. Kč)"], 58)
    for k, t in enumerate(T):
        r = R0 + k
        bunka(ws, r, 1, f"={vst('nazev', k)}", tucne=cil[t["id"]] > 0)
        bunka(ws, r, 2, f"={vst('isin', k)}")
        bunka(ws, r, 3, f"={vst('trh', k)}")
        bunka(ws, r, 4, f"={vst('sektor', k)}")
        bunka(ws, r, 5, f"={vst('cena', k)}", KC2)
        bunka(ws, r, 6, f"={VV}!AC{r}", "0%", tucne=True, vypln=SVETLA)
        bunka(ws, r, 7, f"={vst('px', k)}/SUM({vrozsah('px')})", PCT1)
        bunka(ws, r, 8, f"=(F{r}-G{r})*100", "+0.0;-0.0;0.0")
        bunka(ws, r, 9, f"=({vst('div2026', k)}+{vst('div2026_mimo', k)})*{kurz(k)}", KC2)
        bunka(ws, r, 10, f"=I{r}/E{r}", PCT2)
        bunka(ws, r, 11, f"=J{r}*(1-{vst('srazka', k)})", PCT2)
        bunka(ws, r, 12, f"={vst('div2027', k)}*{kurz(k)}", KC2)
        bunka(ws, r, 13, f"=L{r}/E{r}", PCT2)
        bunka(ws, r, 14, f"=M{r}*(1-{vst('srazka', k)})", PCT2)
        bunka(ws, r, 15, f"={vst('objem', k)}", CISLO)
    r = RK + 1
    sr = lambda c: f"${c}${R0}:${c}${RK}"
    bunka(ws, r, 1, "České dividendy celkem", tucne=True, vypln=SVETLA)
    bunka(ws, r + 1, 1, "WOOD PX ETF pro srovnání", tucne=True, vypln=SVETLA)
    for c in range(2, 16):
        bunka(ws, r, c, None, vypln=SVETLA)
        bunka(ws, r + 1, c, None, vypln=SVETLA)
    bunka(ws, r, 6, f"=SUM({sr('F')})", "0%", tucne=True, vypln=SVETLA)
    bunka(ws, r + 1, 7, f"=SUM({sr('G')})", PCT1, tucne=True, vypln=SVETLA)
    for c in (10, 11, 13, 14):
        col = L(c)
        bunka(ws, r, c, f"=SUMPRODUCT({sr('F')},{sr(col)})", PCT2, tucne=True, vypln=SVETLA)
        bunka(ws, r + 1, c, f"=SUMPRODUCT({sr('G')},{sr(col)})", PCT2, tucne=True, vypln=SVETLA)
    r += 3
    ukaz = [
        ("Počet titulů", f'=COUNTIF({sr("F")},">0")', f'=COUNTIF({sr("G")},">0")', "0"),
        ("Váha pěti největších pozic", "=" + "+".join(f"LARGE({sr('F')},{j})" for j in range(1, 6)),
         "=" + "+".join(f"LARGE({sr('G')},{j})" for j in range(1, 6)), PCT1),
        ("Váha finančního sektoru (banky a pojišťovny)", f"=SUMPRODUCT({vrozsah('finance')},{sr('F')})",
         f"=SUMPRODUCT({vrozsah('finance')},{sr('G')})", PCT1),
        ("Váha zahraničních emitentů", f'=SUMPRODUCT(--({vrozsah("zeme")}<>"ČR"),{sr("F")})',
         f'=SUMPRODUCT(--({vrozsah("zeme")}<>"ČR"),{sr("G")})', PCT1),
        ("Odlišnost složení od ETF (polovina součtu rozdílů vah)", f"=SUMPRODUCT(ABS({sr('F')}-{sr('G')}))/2", None, PCT1),
        ("Hrubý výnos 2026 bez mimořádné části u Doosanu",
         f"=SUMPRODUCT({sr('F')},{vrozsah('div2026')}*IF({vrozsah('mena_div')}=\"EUR\",{A['eur']},1)/{vrozsah('cena')})",
         None, PCT2),
    ]
    zahlavi(ws, r, ["Ukazatel", "České dividendy", "WOOD PX ETF"], 30)
    for k, (popis, f1, f2, fmt) in enumerate(ukaz, 1):
        bunka(ws, r + k, 1, popis)
        bunka(ws, r + k, 2, f1, fmt)
        bunka(ws, r + k, 3, f2, fmt)
    sirky(ws, [52, 16, 12, 16, 11, 11, 11, 9, 11, 10, 10, 11, 10, 10, 12])
    ws.freeze_panes = "B5"

    # ------------------------------------------------------------------ list Historie výnosů
    wh = wb.create_sheet("Historie výnosů")
    titulek(wh, "Historický dividendový výnos",
            "Hrubý výnos = dividendy vyplacené v roce (včetně mimořádných) k ceně akcie na konci předchozího roku. Dividendy v EUR "
            "přepočteny kurzem v den výplaty. Řádky strategie a ETF používají dnešní váhy přepočtené jen na tituly, které se tehdy "
            "obchodovaly. Nejde o zpětný test výkonnosti, jen o ukázku, jak kolísá příjem z dividend.", n + 4)
    cr = list(range(2015, 2026))
    H1 = R0
    mezititulek(wh, H1 - 2, "Cena na konci roku (Kč)")
    zahlavi(wh, H1 - 1, ["Rok"] + [t["nazev"] for t in T] + ["Kurz EUR/CZK v den výplaty"], 40)
    for j, y in enumerate(cr):
        bunka(wh, H1 + j, 1, y, "0")
        for k, t in enumerate(T):
            bunka(wh, H1 + j, k + 2, data["ceny_konec_roku"].get(t["id"], {}).get(str(y)), KC2, vstup=True)
        bunka(wh, H1 + j, n + 2, data["eurczk_ex"].get(str(y)), CISLO, vstup=True)
    bunka(wh, H1 + len(cr), 1, 2026, "0")
    bunka(wh, H1 + len(cr), n + 2, data["eurczk_ex"]["2026"], CISLO, vstup=True)
    for k in range(n):
        bunka(wh, H1 + len(cr), k + 2, None)
    H2 = H1 + len(cr) + 4
    vr = list(range(2017, 2027))
    mezititulek(wh, H2 - 2, "Hrubý dividendový výnos podle roku výplaty")
    zahlavi(wh, H2 - 1, ["Rok"] + [t["nazev"] for t in T] + ["České dividendy (hrubý)", "České dividendy (čistý)",
                                                              "WOOD PX ETF (hrubý)"], 44)
    HW = H2 + len(vr) + 3        # pomocné řádky s vahami a srážkou
    fc, lc = "B", L(n + 1)
    for j, y in enumerate(vr):
        r = H2 + j
        bunka(wh, r, 1, y, "0")
        pr = H1 + (y - 1 - 2015)
        kr = H1 + (y - 2015)
        for k, t in enumerate(T):
            col = L(k + 2)
            dv = f"Dividendy!{col}{B3 + (y - ROKY[0])}"
            fxs = f"${L(n + 2)}${kr}" if t["mena_div"] == "EUR" else "1"
            bunka(wh, r, k + 2, f'=IF(AND(ISNUMBER({col}{pr}),ISNUMBER({dv})),{dv}*{fxs}/{col}{pr},"")', PCT1)
        yr = f"{fc}{r}:{lc}{r}"
        den = lambda wr: f"SUMPRODUCT(${fc}${wr}:${lc}${wr}*ISNUMBER({yr}))"
        bunka(wh, r, n + 2, f"=SUMPRODUCT(${fc}${HW}:${lc}${HW},{yr})/{den(HW)}", PCT1, tucne=True, vypln=SVETLA)
        bunka(wh, r, n + 3, f"=SUMPRODUCT(${fc}${HW}:${lc}${HW},{yr},${fc}${HW + 2}:${lc}${HW + 2})/{den(HW)}", PCT1,
              tucne=True, vypln=SVETLA)
        bunka(wh, r, n + 4, f"=SUMPRODUCT(${fc}${HW + 1}:${lc}${HW + 1},{yr})/{den(HW + 1)}", PCT1, tucne=True, vypln=SVETLA)
    r = H2 + len(vr)
    bunka(wh, r, 1, "Průměr 2017–2026", tucne=True)
    bunka(wh, r + 1, 1, "Průměr 2022–2026", tucne=True)
    for c in range(2, n + 5):
        col = L(c)
        bunka(wh, r, c, f'=IFERROR(AVERAGE({col}{H2}:{col}{H2 + 9}),"")', PCT1, tucne=True)
        bunka(wh, r + 1, c, f'=IFERROR(AVERAGE({col}{H2 + 5}:{col}{H2 + 9}),"")', PCT1, tucne=True)
    bunka(wh, HW, 1, "Váha: České dividendy")
    bunka(wh, HW + 1, 1, "Váha: WOOD PX ETF")
    bunka(wh, HW + 2, 1, "Podíl po srážkové dani")
    for k in range(n):
        bunka(wh, HW, k + 2, f"={VV}!AC{R0 + k}", "0%")
        bunka(wh, HW + 1, k + 2, f"=Složení!G{R0 + k}", PCT1)
        bunka(wh, HW + 2, k + 2, f"=1-{vst('srazka', k)}", PCT1)
    sirky(wh, [22] + [13] * n + [14, 14, 14])
    wh.freeze_panes = "B5"

    # ------------------------------------------------------------------ list Kalendář výplat
    wk = wb.create_sheet("Kalendář výplat")
    titulek(wk, "Kalendář výplat a příjem z dividend",
            "Kolik by strategie vyplatila do peněženky z investice v buňce B4 při dnešních cenách a vahách. Data výplat jsou "
            "skutečná data roku 2026, v dalších letech se o dny až týdny liší. Po srážce = po srážkové dani u zdroje.", 8)
    bunka(wk, 4, 1, "Investovaná částka (Kč)", tucne=True)
    bunka(wk, 4, 2, 100000, KC, vstup=True)
    KH = 6
    zahlavi(wk, KH, ["Titul", "Datum výplaty 2026", "Měsíc", "Váha", "Dividenda 2026 hrubá (Kč)", "Dividenda 2026 po srážce (Kč)",
                     "Odhad 2027 hrubá (Kč)", "Odhad 2027 po srážce (Kč)"], 44)
    poradi = sorted([k for k, t in enumerate(T) if cil[t["id"]] > 0], key=lambda k: data["vyplaty_2026"][T[k]["id"]])
    for j, k in enumerate(poradi):
        r = KH + 1 + j
        sl = R0 + k
        bunka(wk, r, 1, f"={vst('nazev', k)}")
        bunka(wk, r, 2, datetime.date.fromisoformat(data["vyplaty_2026"][T[k]["id"]]), "d. m. yyyy", vstup=True)
        bunka(wk, r, 3, f"=MONTH(B{r})", "0")
        bunka(wk, r, 4, f"=Složení!F{sl}", "0%")
        bunka(wk, r, 5, f"=$B$4*D{r}*Složení!J{sl}", KC)
        bunka(wk, r, 6, f"=$B$4*D{r}*Složení!K{sl}", KC)
        bunka(wk, r, 7, f"=$B$4*D{r}*Složení!M{sl}", KC)
        bunka(wk, r, 8, f"=$B$4*D{r}*Složení!N{sl}", KC)
    k0, k1 = KH + 1, KH + len(poradi)
    r = k1 + 1
    bunka(wk, r, 1, "Celkem za rok", tucne=True, vypln=SVETLA)
    for c in (2, 3):
        bunka(wk, r, c, None, vypln=SVETLA)
    bunka(wk, r, 4, f"=SUM(D{k0}:D{k1})", "0%", tucne=True, vypln=SVETLA)
    for c in range(5, 9):
        col = L(c)
        bunka(wk, r, c, f"=SUM({col}{k0}:{col}{k1})", KC, tucne=True, vypln=SVETLA)
    bunka(wk, r + 1, 1, "Výnos z investované částky")
    for c in range(5, 9):
        bunka(wk, r + 1, c, f"={L(c)}{r}/$B$4", PCT2)
    r += 4
    zahlavi(wk, r, ["Měsíc výplaty", "Číslo měsíce", "Podíl na roční výplatě", "", "Dividenda 2026 hrubá (Kč)",
                    "Dividenda 2026 po srážce (Kč)"], 44)
    for j, (cm, nm) in enumerate([(5, "květen"), (7, "červenec"), (8, "srpen")]):
        rr = r + 1 + j
        bunka(wk, rr, 1, nm)
        bunka(wk, rr, 2, cm, "0", vstup=True)
        bunka(wk, rr, 5, f"=SUMIF($C${k0}:$C${k1},B{rr},E${k0}:E${k1})", KC)
        bunka(wk, rr, 6, f"=SUMIF($C${k0}:$C${k1},B{rr},F${k0}:F${k1})", KC)
        bunka(wk, rr, 3, f"=E{rr}/E${k1 + 1}", PCT1)
        bunka(wk, rr, 4, None)
    sirky(wk, [30, 13, 12, 9, 14, 14, 14, 14])

    # ------------------------------------------------------------------ list Likvidita
    wl = wb.create_sheet("Likvidita")
    titulek(wl, "Likvidita a kapacita strategie",
            "Za kolik burzovních dnů lze celou pozici koupit nebo prodat, když Portu zobchoduje nejvýš daný podíl mediánu denního "
            "objemu (list Vstupy). Objemy strategie v řádku 4 jsou vstupy. U VIG počítám jen pražský objem, hlavní trh ve Vídni "
            "je řádově likvidnější.", 10)
    bunka(wl, 4, 1, "Objem strategie (mil. Kč)", tucne=True)
    for j, a in enumerate([100, P["referencni_aum_mil"], 1000]):
        bunka(wl, 4, 5 + 2 * j, a, KC, vstup=True, tucne=True)
        bunka(wl, 4, 6 + 2 * j, None)
    zahlavi(wl, 5, ["Titul", "Váha", "Medián denního objemu (mil. Kč)", "Strop podle likvidity", "Pozice (mil. Kč)",
                    "Dnů na zobchodování", "Pozice (mil. Kč)", "Dnů na zobchodování", "Pozice (mil. Kč)", "Dnů na zobchodování"], 44)
    akt = [k for k, t in enumerate(T) if cil[t["id"]] > 0]
    for j, k in enumerate(akt):
        r = 6 + j
        bunka(wl, r, 1, f"={vst('nazev', k)}")
        bunka(wl, r, 2, f"=Složení!F{R0 + k}", "0%")
        bunka(wl, r, 3, f"={vst('objem', k)}", CISLO)
        bunka(wl, r, 4, f"={VV}!O{R0 + k}", PCT1)
        for jj in range(3):
            ca, cd = L(5 + 2 * jj), L(6 + 2 * jj)
            bunka(wl, r, 5 + 2 * jj, f"={ca}$4*$B{r}", "0.0")
            bunka(wl, r, 6 + 2 * jj, f"={ca}{r}/({A['podil_obj']}*$C{r})", "0", tucne=True)
    sirky(wl, [30, 9, 14, 12, 11, 13, 11, 13, 11, 13])

    # ------------------------------------------------------------------ list Filtry
    wf = wb.create_sheet("Filtry")
    titulek(wf, "Celý trh: které emise prošly a proč ostatní ne",
            f"Všech {len(vesmir)} akciových emisí na trzích Prime, Standard a Free pražské burzy k {datum}. Z trhu Free beru jen "
            "emise s vazbou na ČR (báze indexu PX, sídlo nebo provozní centrála v ČR). Medián denního objemu je za 6 měsíců.", 7)
    zahlavi(wf, 4, ["Emise", "ISIN", "Trh", "Vazba na ČR", "Dividenda za 12 měsíců", "Medián denního objemu (mil. Kč)",
                    "Výsledek"], 44)
    pozn = {
        "CZ0008019106": ("ano", "95,60 Kč", 94.88, "zařazena"),
        "CZ0008040318": ("ano", "15,50 Kč (11,50 řádná + 4,00 mimořádná)", 44.86, "zařazena"),
        "CZ0005112300": ("ano", "42 Kč", 119.57, "zařazena"),
        "CZ0009008942": ("ano", "30 Kč", 12.69, "zařazena"),
        "AT0000908504": ("ano (index PX)", "1,73 EUR", 3.24, "zařazena"),
        "CS0008418869": ("ano", "1 100 Kč", 3.37, "zařazena"),
        "CZ0009000121": ("ano", "21 Kč", 1.20, "zařazena"),
        "CZ1008000310": ("ano", "28 Kč", 3.58, "zařazena, strop 5 % pro nováčka"),
        "AT0000652011": ("ano (index PX)", "0,75 EUR", 62.47, "vyřazena: výnos 0,6 % je pod prahem, čekatelka"),
        "NL0015073TS8": ("ano (index PX)", "žádná", 54.69, "vyřazena: dividendu zatím nevyplatila, čekatelka"),
        "CZ0005135970": ("ano", "návrh 13 Kč, schválení neověřeno", 0.90, "vyřazena: likvidita, bez dividendové historie"),
        "SK1000025322": ("ano (index PX)", "žádná", 0.20, "vyřazena: bez dividendy, likvidita"),
        "CZ0009008819": ("ano", "žádná", 0.26, "vyřazena: bez dividendy, likvidita"),
        "SK1120010287": ("ne", "žádná", 0.00, "vyřazena: bez dividendy, likvidita"),
        "CZ0005123620": ("ano", "40 Kč", 0.13, "vyřazena: likvidita (dotace končí 2028–2029)"),
        "CS0008419750": ("ano", "160 Kč", 0.00, "vyřazena: likvidita (obchod jen v 8 % dnů)"),
        "CZ0009011474": ("ano", "žádná", None, "vyřazena: bez dividendy"),
        "NL0010391108": ("ano (index PX)", "žádná", 0.07, "vyřazena: bez dividendy, likvidita"),
        "CS0008416251": ("ano", "žádná", None, "vyřazena: bez dividendy"),
        "CZ0009009940": ("ano", "95,57 Kč", 0.10, "vyřazena: likvidita"),
        "CZ0005088559": ("ano", "37 Kč", 0.00, "vyřazena: likvidita (obchod v 54 % dnů)"),
        "NL00150006R6": ("ano (největší trh ČR)", "ano, v EUR, standardně v akciích", 0.25, "vyřazena: likvidita v Praze"),
        "US6687711084": ("částečně (centrála Praha a Tempe)", "ano, čtvrtletně v USD", 0.06, "vyřazena: likvidita v Praze"),
        "GB00BLGXWY71": ("ano (centrála Praha)", "žádná", 0.01, "vyřazena: bez dividendy, likvidita"),
    }
    for j, e in enumerate(vesmir):
        r = 5 + j
        p = pozn.get(e["isin"], ("ne", "neposuzuji", None, "vyřazena: zahraniční emise bez vazby na ČR"))
        zar = p[3].startswith("zařazena")
        for c, v in enumerate([e["nazev"], e["isin"], e["trh"], p[0], p[1], p[2], p[3]], 1):
            bunka(wf, r, c, v, CISLO if c == 6 else None, tucne=zar, vypln=SVETLA if zar else None)
    sirky(wf, [24, 16, 10, 30, 38, 14, 52])
    wf.freeze_panes = "B5"

    # ------------------------------------------------------------------ list Zdroje
    wz = wb.create_sheet("Zdroje")
    titulek(wz, "Zdroje a předpoklady", "Odkud jsou čísla a co je můj odhad.", 3)
    zahlavi(wz, 4, ["Údaj", "Zdroj", "Odkaz nebo poznámka"], 30)
    zdroje = [
        ("Ceny, počty akcií, tržní segment, poslední dividenda", f"Burza cenných papírů Praha, detail emise, {datum}", "https://www.pse.cz/udaje-o-trhu/akcie/prime-market"),
        ("Váhy a free float v indexu PX", f"Burza cenných papírů Praha, báze indexu PX, {datum}", "https://www.pse.cz/indexy/hodnoty-indexu/detail/XC0009698371"),
        ("Pravidla indexu PX (strop 20 %, kritéria likvidity)", "Pravidla pro výpočet indexů PX, PX-TR a PX-TRnet", "https://www.pse.cz/userfiles/related_documents/cs/CZ-Pravidla-pro-vypocet-indexu-PX-PX-TR-a-PX-TRnet.pdf"),
        ("Složení WOOD PX ETF při startu 7. 9. 2026", "Kurzy.cz, Forbes, CzechCrunch", "https://zpravy.kurzy.cz/873731-na-prazske-burze-v-pondeli-startuje-etf-na-index-px-ceske-akcie-bude-mozne-koupit-v-jedinem-titulu/"),
        ("Dividendy 2008–2026 a data výplat", "Fio banka, přehled dividend českých akcií", "https://www.fio.cz/zpravodajstvi/dividendy"),
        ("Dividendy před rokem 2008, ceny na konci roku, denní objemy", "Yahoo Finance, pražské tickery (CEZ.PR, KOMB.PR, TABAK.PR…)", "U Colt CZ chybí objemy za květen až srpen 2026, medián je ze dnů s daty"),
        ("Dividendy ČEZ 2009–2025", "ČEZ, stránka pro investory", "https://www.cez.cz/cs/pro-investory/akcie/dividendy"),
        ("Kurz EUR/CZK", f"ČNB, kurzy devizového trhu, {datum}", "https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/"),
        ("Srážková daň z dividend (ČR 15 %, Rakousko 27,5 %, Nizozemsko 15 %)", "Patria Finance, sazby srážkových daní, říjen 2026", "https://cdn.patria.cz/Sazby-srazkovych-dani-na-dividendove-prijmy.pdf"),
        ("Odhad dividendy 2027: ČEZ, KB, Moneta, Colt, Kofola", "Fio banka, komentáře analytiků k dividendám 2026", "https://www.fio.cz/zpravodajstvi/zpravy-z-burzy/324230-dividenda-cez-v-roce-2026-a-pristim-roce-komentar-analytika"),
        ("Výhled ČEZ 2026 (očištěný zisk 31–35 mld. Kč)", "Pololetní výsledky ČEZ, 11. 8. 2026", "https://www.proinvestory.cz/cez-pololetni-vysledky-2026-vyhled-dividenda-stat/"),
        ("Erste: dividenda 0,75 EUR, výplatní poměr 9,1 %", "Erste Group, valná hromada 17. 4. 2026", "https://www.erstegroup.com/en/news-media/press-releases/2026/04/17/results-annual-general-meeting"),
        ("VIG: dividenda 1,73 EUR, zisk na akcii 6,46 EUR, cíl 2026", "Vienna Insurance Group, valná hromada 2026", "https://group.vig/en/investor-relations/ir-news/ir-meldungen/vienna-insurance-group-annual-general-meeting-2026/"),
        ("Doosan Škoda Power: 28 Kč, z toho 15,29 Kč ze zisku 2025", "Oznámení o výplatě dividendy za rok 2025", "https://www.doosanskodapower.com/download/pdf/en/Notice of Dividend Payment for 2025.pdf"),
        ("Kofola: čistý zisk 2025 586 mil. Kč", "Komerční banka, komentář k výsledkům, 24. 4. 2026", "https://zpravy.kurzy.cz/857134-kofola-finalni-vysledky-lepsi-nez-predbezna-cisla-indikace-silneho-1q26-dividenda-21-czk/"),
        ("CSG: cíl 30–40 % čistého zisku, první výplata 2027", "Reuters, oznámení IPO, leden 2026", "https://www.marketscreener.com/news/czech-defence-firm-csg-announces-amsterdam-ipo-ce7e58d8dd81fe20"),
        ("Odhady dividend 2027 u VIG, Philip Morris ČR, Doosanu a Erste", "Můj odhad z dividendové politiky a posledních výsledků", "Zdůvodnění je u každého titulu na listu Vstupy, sloupec V"),
        ("Referenční objem strategie 300 mil. Kč", "Můj předpoklad", "Určuje pásma likvidity. Při jiném očekávaném objemu je potřeba pásma přenastavit (list Likvidita)"),
    ]
    for j, z in enumerate(zdroje):
        for c, v in enumerate(z, 1):
            bunka(wz, 5 + j, c, v, zalomit=True)
    r = 5 + len(zdroje) + 1
    mezititulek(wz, r, "Barvy v sešitu")
    bunka(wz, r + 1, 1, "Modré písmo", vstup=True)
    bunka(wz, r + 1, 2, "Ručně zadaný vstup (cena, dividenda, parametr, cílová váha). Tyto buňky se upravují.")
    bunka(wz, r + 2, 1, "Černé písmo")
    bunka(wz, r + 2, 2, "Vzorec. Přepočítá se sám.")
    sirky(wz, [52, 52, 90])

    poradi_listu = ["Složení", "Výpočet vah", "Spolehlivost", "Dividendy", "Historie výnosů", "Kalendář výplat",
                    "Likvidita", "Filtry", "Vstupy", "Zdroje"]
    wb._sheets = [wb[x] for x in poradi_listu]
    wb.active = 0
    for list_ in wb.worksheets:           # tisk: na šířku, celá šířka listu na jednu stránku
        list_.page_setup.orientation = "landscape"
        list_.page_setup.fitToWidth = 1
        list_.page_setup.fitToHeight = 0
        list_.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(out)

    # ------------------------------------------------------------------ výpis pro kontrolu a pro text
    print(f"Dividendový výnos indexu PX za 12 měsíců: {px_vynos:.4%}, práh {P['podil_vynosu_px'] * px_vynos:.4%}")
    print(f"{'titul':10s} let10 bez let5   S  rust   bp br     q  hruby12 div lik vyn  cisty26 cisty27  skore  pred  strop  model  cil")
    for t in T:
        i = t["id"]
        v = vyp[i]
        rust = "   -  " if v["rust"] is None else f"{v['rust']:6.1%}"
        print(f"{i:10s} {v['let10']:5d} {v['bez']:3d} {v['let5']:4d} {v['S']:3d} {rust} {v['bp']:3d} {v['br']:2d} {v['q']:6.3f} "
              f"{v['hruby12']:7.2%} {int(v['f_div']):3d} {int(v['f_lik']):3d} {int(v['f_vyn']):3d}  {v['c26']:7.2%} {v['c27']:7.2%} "
              f"{v['skore'] * 100:6.2f} {pred[i]:6.1%} {v['strop']:5.0%} {w[i]:7.2%} {cil[i]:4.0%}")
    hr26 = sum(cil[t["id"]] * (t["div2026"] + t["div2026_mimo"]) * fx(t) / t["cena"] for t in T)
    ci26 = sum(cil[t["id"]] * (t["div2026"] + t["div2026_mimo"]) * fx(t) / t["cena"] * (1 - t["srazka"]) for t in T)
    hr27 = sum(cil[t["id"]] * t["div2027"] * fx(t) / t["cena"] for t in T)
    ci27 = sum(cil[t["id"]] * t["div2027"] * fx(t) / t["cena"] * (1 - t["srazka"]) for t in T)
    spx = sum(t["px"] for t in T)
    e26 = sum(t["px"] / spx * (t["div2026"] + t["div2026_mimo"]) * fx(t) / t["cena"] for t in T)
    en26 = sum(t["px"] / spx * (t["div2026"] + t["div2026_mimo"]) * fx(t) / t["cena"] * (1 - t["srazka"]) for t in T)
    e27 = sum(t["px"] / spx * t["div2027"] * fx(t) / t["cena"] for t in T)
    en27 = sum(t["px"] / spx * t["div2027"] * fx(t) / t["cena"] * (1 - t["srazka"]) for t in T)
    act = sum(abs(cil[t["id"]] - t["px"] / spx) for t in T) / 2
    print(f"Strategie: hrubý 2026 {hr26:.2%}, čistý 2026 {ci26:.2%}, hrubý 2027 {hr27:.2%}, čistý 2027 {ci27:.2%}")
    print(f"ETF:       hrubý 2026 {e26:.2%}, čistý 2026 {en26:.2%}, hrubý 2027 {e27:.2%}, čistý 2027 {en27:.2%}")
    print(f"Odlišnost složení od ETF: {act:.1%}, finance {sum(cil[t['id']] for t in T if t['finance']):.0%}")
    print("Uloženo:", out)


if __name__ == "__main__":
    main()

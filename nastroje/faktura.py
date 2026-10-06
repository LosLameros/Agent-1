#!/usr/bin/env python3
"""Vygeneruje PDF fakturu s platebním QR kódem podle vzoru faktur Marka Pokorného.

Použití:
    python3 nastroje/faktura.py <faktura.json> [vystup.pdf]

Bez výstupní cesty se PDF uloží do vystupy/faktury/Faktura_<cislo>.pdf.
Dodavatel se načítá z fakturace/dodavatel.json.

Vstupní JSON:
{
  "cislo": "26050",
  "rezim": "CZ",                       // CZ | EU | EXPORT
  "datum_vystaveni": "2026-10-06",     // nepovinné, výchozí dnes
  "splatnost_dni": 10,                 // nebo "datum_splatnosti": "2026-10-16"
  "duzp": "2026-10-06",                // nepovinné, výchozí = datum vystavení
  "odberatel": {
    "nazev": "JETI model s.r.o.",
    "adresa": ["Lomená 1530", "74258 Příbor", "Česká republika"],
    "ico": "26825147",                 // nepovinné
    "dic": "CZ26825147",               // nepovinné
    "kontakt": "venpor@seznam.cz"      // nepovinné
  },
  "polozky": [
    {"pocet": 1000, "jednotka": "ks", "popis": "Hlava knypliku V5", "cena": "42.00"}
  ],
  "poznamka": "..."                    // nepovinné; u EU/EXPORT je výchozí důvod osvobození od DPH
}

Ceny jsou vždy bez DPH. U CZ se DPH 21 % počítá po řádcích a zaokrouhluje na haléře.
QR kód: CZ = QR Platba + F (SPAYD s X-INV), EU/EXPORT = SEPA platba (EPC QR).
"""
import json
import re
import sys
import unicodedata
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Flowable, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle, KeepTogether)
from reportlab.pdfgen import canvas as pdfcanvas

ROOT = Path(__file__).resolve().parent.parent
DPH_SAZBA = Decimal("21")
HALER = Decimal("0.01")

INK = HexColor("#111827")      # hlavní text
MUTED = HexColor("#6B7280")    # popisky
LINE = HexColor("#E5E7EB")     # vlasové linky
ACCENT = HexColor("#135C9E")   # modrá z původních faktur, o odstín sytější
ACCENT_SOFT = HexColor("#EFF4FA")

PAGE_W, PAGE_H = A4
OKRAJ = 40
SIRKA = PAGE_W - 2 * OKRAJ

TEXTY = {
    "CZ": {
        "druh": "FAKTURA – DAŇOVÝ DOKLAD", "cislo": "č. {}",
        "dodavatel": "DODAVATEL", "odberatel": "ODBĚRATEL", "ico": "IČO", "dic": "DIČ",
        "platce": "Plátce DPH", "kontakt": "Kontakt",
        "ucet": "Číslo účtu", "forma": "Forma úhrady",
        "prevod": "Převodem", "vs": "Variabilní symbol", "qr": "QR Platba + F",
        "vystaveni": "Datum vystavení", "splatnost": "Datum splatnosti", "duzp": "Datum zd. plnění",
        "splatnost_kratce": "Splatnost {}",
        "pocet": "POČET", "popis": "POPIS", "cena": "JEDN. CENA", "sazba": "DPH %",
        "zaklad": "ZÁKLAD", "dph": "DPH", "celkem": "CELKEM",
        "rekap_sazba": "Sazba DPH", "rekap_zaklad": "Základ", "rekap_dph": "DPH", "rekap_celkem": "Celkem",
        "k_uhrade": "Celkem k úhradě", "vystavil": "Vystavil(a) {}", "strana": "Strana {} z {}",
        "titul_pdf": "Faktura - daňový doklad č. {}",
    },
    "EN": {
        "druh": "INVOICE", "cislo": "No. {}",
        "dodavatel": "SUPPLIER", "odberatel": "CUSTOMER", "ico": "Company ID", "dic": "VAT ID",
        "platce": "VAT registered", "kontakt": "Contact",
        "ucet": "IBAN", "forma": "Payment method",
        "prevod": "Bank transfer", "vs": "Variable symbol", "qr": "SEPA payment",
        "vystaveni": "Issue date", "splatnost": "Due date", "duzp": "Date of taxable supply",
        "splatnost_kratce": "Due {}",
        "pocet": "QTY", "popis": "DESCRIPTION", "cena": "UNIT PRICE", "celkem": "TOTAL",
        "k_uhrade": "Total due", "vystavil": "Issued by {}", "strana": "Page {} of {}",
        "titul_pdf": "Invoice no. {}",
    },
}

POZNAMKA_DPH = {
    "EU": "VAT exempt – intra-Community supply of goods (Art. 138 Directive 2006/112/EC, § 64 Czech VAT Act).",
    "EXPORT": "VAT exempt – export of goods (Art. 146 Directive 2006/112/EC, § 66 Czech VAT Act).",
}

FONTY = ROOT / "nastroje" / "fonts"
FONT_CANDIDATES = [
    # regular, medium, bold
    (FONTY / "Roboto-Regular.ttf", FONTY / "Roboto-Medium.ttf", FONTY / "Roboto-Bold.ttf"),
    (Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
     Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
     Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")),
    (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/arialbd.ttf"), Path("C:/Windows/Fonts/arialbd.ttf")),
]


class ChybaVstupu(Exception):
    pass


def registruj_fonty():
    for trojice in FONT_CANDIDATES:
        if all(p.exists() for p in trojice):
            for nazev, p in zip(("F", "FM", "FB"), trojice):
                pdfmetrics.registerFont(TTFont(nazev, str(p)))
            return
    raise ChybaVstupu("Chybí písmo Roboto v nastroje/fonts/ a nenašel jsem ani náhradní TTF s diakritikou.")



# --- formátování ---------------------------------------------------------

def cislo_cz(x, des=2):
    s = f"{x:,.{des}f}" if des else f"{x:,.0f}"
    return s.replace(",", " ").replace(".", ",")


def cislo_en(x, des=2):
    return f"{x:.{des}f}"


def mnozstvi(x):
    x = Decimal(x)
    if x == x.to_integral_value():
        return cislo_cz(x, 0)
    return cislo_cz(x, 2).rstrip("0").rstrip(",")


def datum_txt(d):
    return d.strftime("%d. %m. %Y")


def bez_diakritiky(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def parse_datum(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


# --- kontroly ------------------------------------------------------------

def ico_ok(ico):
    if not re.fullmatch(r"\d{8}", ico):
        return False
    s = sum(int(c) * w for c, w in zip(ico[:7], range(8, 1, -1)))
    kontrola = (11 - s % 11) % 10
    return kontrola == int(ico[7])


def iban_ok(iban):
    iban = iban.replace(" ", "")
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{8,30}", iban):
        return False
    prevod = "".join(str(int(c, 36)) for c in iban[4:] + iban[:4])
    return int(prevod) % 97 == 1


def zkontroluj(f, dod):
    chyby = []
    if not re.fullmatch(r"\d{1,10}", str(f["cislo"])):
        chyby.append("Číslo faktury musí mít 1–10 číslic (slouží zároveň jako variabilní symbol).")
    if f["rezim"] not in ("CZ", "EU", "EXPORT"):
        chyby.append("Režim musí být CZ, EU nebo EXPORT.")
    o = f.get("odberatel") or {}
    if not o.get("nazev") or not o.get("adresa"):
        chyby.append("Odběratel musí mít název a adresu.")
    ico = o.get("ico")
    if ico and f["rezim"] == "CZ" and not ico_ok(ico):
        chyby.append(f"IČO odběratele {ico} nemá platný kontrolní součet.")
    dic = o.get("dic")
    if dic:
        if f["rezim"] == "CZ" and not re.fullmatch(r"CZ\d{8,10}", dic):
            chyby.append(f"DIČ odběratele „{dic}“ nemá tvar CZ + 8–10 číslic.")
        if f["rezim"] == "EU" and not re.fullmatch(r"[A-Z]{2}[0-9A-Z]{2,13}", dic):
            chyby.append(f"VAT ID odběratele z EU „{dic}“ musí začínat kódem státu (např. PL…).")
    if not f.get("polozky"):
        chyby.append("Faktura nemá žádné položky.")
    for p in f.get("polozky", []):
        if not p.get("popis"):
            chyby.append("Položka bez popisu.")
        try:
            if Decimal(str(p["pocet"])) <= 0 or Decimal(str(p["cena"])) < 0:
                chyby.append(f"Položka „{p.get('popis')}“ má nekladný počet nebo zápornou cenu.")
        except Exception:
            chyby.append(f"Položka „{p.get('popis')}“ nemá platný počet nebo cenu.")
    for k in ("iban_czk", "iban_eur"):
        if not iban_ok(dod[k]):
            chyby.append(f"IBAN dodavatele {k} = {dod[k]} není platný.")
    if chyby:
        raise ChybaVstupu("\n".join(chyby))


# --- výpočet -------------------------------------------------------------

def spocitej(f):
    s_dph = f["rezim"] == "CZ"
    radky, zaklad_sum, dph_sum = [], Decimal(0), Decimal(0)
    for p in f["polozky"]:
        pocet = Decimal(str(p["pocet"]))
        cena = Decimal(str(p["cena"])).quantize(HALER, ROUND_HALF_UP)
        zaklad = (pocet * cena).quantize(HALER, ROUND_HALF_UP)
        dph = (zaklad * DPH_SAZBA / 100).quantize(HALER, ROUND_HALF_UP) if s_dph else Decimal(0)
        radky.append({"pocet": pocet, "jednotka": p.get("jednotka", "ks"), "popis": p["popis"],
                      "cena": cena, "zaklad": zaklad, "dph": dph, "celkem": zaklad + dph})
        zaklad_sum += zaklad
        dph_sum += dph
    return radky, zaklad_sum, dph_sum, zaklad_sum + dph_sum


# --- QR ------------------------------------------------------------------

def spayd(f, dod, celkem, zaklad, dph, d_vyst, d_splat, d_duzp):
    """QR Platba + F ve stejném tvaru, jaký generuje FakturaOnline, doplněný o DT, VII, TB0 a T0."""
    o = f["odberatel"]
    ymd = lambda d: d.strftime("%Y%m%d")
    sid = ["SID", "1.0", f"ID:{f['cislo']}", f"DD:{ymd(d_vyst)}", f"AM:{celkem:.2f}",
           f"VS:{f['cislo']}", f"VII:{dod['dic']}", f"INI:{dod['ico']}"]
    if o.get("dic"):
        sid.append(f"VIR:{o['dic']}")
    if o.get("ico"):
        sid.append(f"INR:{o['ico']}")
    sid += [f"DUZP:{ymd(d_duzp)}", f"DPPD:{ymd(d_duzp)}", f"TB0:{zaklad:.2f}", f"T0:{dph:.2f}"]
    pole = ["SPD", "1.0", f"ACC:{dod['iban_czk']}", f"AM:{celkem:.2f}", "CC:CZK",
            f"DT:{ymd(d_splat)}", f"MSG:{f['cislo']}", f"X-VS:{f['cislo']}",
            "X-INV:" + "%2A".join(sid)]
    return "*".join(pole)


def epc(f, dod, celkem):
    """SEPA QR (EPC069-12, verze 002) – stejný obsah jako na faktuře 26042."""
    return "\n".join(["BCD", "002", "1", "SCT", dod.get("bic_eur", ""), dod["jmeno"],
                      dod["iban_eur"], f"EUR{celkem:.2f}", "", "", f"{f['cislo']}"])


# --- grafické bloky ------------------------------------------------------

def nakresli_qr(c, data, x, y, size):
    """QR jako jedna vektorová cesta – bez světlých spár mezi moduly, ostrý v každém prohlížeči."""
    qr = QrCodeWidget(data, barLevel="M").qr
    qr.make()
    n = qr.getModuleCount()
    m = size / n
    p = c.beginPath()
    for r, row in enumerate(qr.modules):
        col = 0
        while col < n:
            if row[col]:
                start = col
                while col < n and row[col]:
                    col += 1
                p.rect(x + start * m, y + size - (r + 1) * m, (col - start) * m, m)
            else:
                col += 1
    c.saveState()
    c.setFillColor(HexColor("#000000"))
    c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


class Hlavicka(Flowable):
    """Druh dokladu a číslo vlevo, částka k úhradě a splatnost vpravo."""

    def __init__(self, t, cislo, castka, splatnost):
        super().__init__()
        self.t, self.cislo, self.castka, self.splatnost = t, cislo, castka, splatnost
        self.width, self.height = SIRKA, 58

    def draw(self):
        c, h = self.canv, self.height
        c.setFillColor(ACCENT)
        c.setFont("FM", 8)
        c.drawString(0, h - 8, self.t["druh"], charSpace=1.2)
        c.setFillColor(INK)
        c.setFont("FB", 26)
        c.drawString(0, h - 40, self.t["cislo"].format(self.cislo))
        c.setFillColor(MUTED)
        c.setFont("F", 8)
        c.drawRightString(SIRKA, h - 8, self.t["k_uhrade"])
        c.setFillColor(INK)
        c.setFont("FB", 20)
        c.drawRightString(SIRKA, h - 34, self.castka)
        c.setFillColor(MUTED)
        c.setFont("F", 8)
        c.drawRightString(SIRKA, h - 50, self.t["splatnost_kratce"].format(self.splatnost))


class Linka(Flowable):
    def __init__(self, barva=LINE, tloustka=0.6):
        super().__init__()
        self.barva, self.tloustka = barva, tloustka
        self.width, self.height = SIRKA, self.tloustka

    def draw(self):
        self.canv.setStrokeColor(self.barva)
        self.canv.setLineWidth(self.tloustka)
        self.canv.line(0, 0, SIRKA, 0)


class PlatebniKarta(Flowable):
    """Světlá karta: účet, VS, forma úhrady, data a QR kód."""

    def __init__(self, t, ucet, cislo, d_vyst, d_splat, d_duzp, qr_data):
        super().__init__()
        self.t, self.qr_data = t, qr_data
        self.bunky = [
            [(t["ucet"], ucet), (t["vs"], str(cislo)), (t["forma"], t["prevod"])],
            [(t["vystaveni"], d_vyst), (t["splatnost"], d_splat), (t["duzp"], d_duzp)],
        ]
        self.width, self.height = SIRKA, 112

    def draw(self):
        c, h = self.canv, self.height
        c.setFillColor(ACCENT_SOFT)
        c.roundRect(0, 0, SIRKA, h, 8, stroke=0, fill=1)
        qr_box, qr_size = 88, 78
        bx, by = SIRKA - qr_box - 12, h - qr_box - 10
        c.setFillColor(white)
        c.roundRect(bx, by, qr_box, qr_box, 6, stroke=0, fill=1)
        nakresli_qr(c, self.qr_data, bx + (qr_box - qr_size) / 2, by + (qr_box - qr_size) / 2, qr_size)
        c.setFillColor(MUTED)
        c.setFont("FM", 6.5)
        c.drawCentredString(bx + qr_box / 2, 6, self.t["qr"])
        sloupec = (bx - 18 - 12) / 3
        for r, radek in enumerate(self.bunky):
            y = h - 24 - r * 44
            for i, (label, hodnota) in enumerate(radek):
                x = 18 + i * sloupec
                c.setFillColor(MUTED)
                c.setFont("F", 7)
                c.drawString(x, y, label)
                c.setFillColor(INK)
                c.setFont("FB", 10)
                c.drawString(x, y - 15, hodnota)


class CelkemBlok(Flowable):
    def __init__(self, label, castka, sirka=270):
        super().__init__()
        self.label, self.castka = label, castka
        self.blok = sirka
        self.width, self.height = SIRKA, 46

    def draw(self):
        c = self.canv
        x = SIRKA - self.blok
        c.setFillColor(ACCENT)
        c.roundRect(x, 0, self.blok, self.height, 8, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("FM", 9)
        c.drawString(x + 16, 18, self.label)
        c.setFont("FB", 16)
        c.drawRightString(SIRKA - 16, 16, self.castka)


def pata_factory(t, dod):
    class CislovanyCanvas(pdfcanvas.Canvas):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self._stavy = []

        def showPage(self):
            self._stavy.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            n = len(self._stavy)
            for stav in self._stavy:
                self.__dict__.update(stav)
                self.setFillColor(ACCENT)
                self.rect(0, PAGE_H - 6, PAGE_W, 6, stroke=0, fill=1)
                self.setStrokeColor(LINE)
                self.setLineWidth(0.6)
                self.line(OKRAJ, 46, PAGE_W - OKRAJ, 46)
                self.setFont("F", 7)
                self.setFillColor(MUTED)
                self.drawString(OKRAJ, 32, t["vystavil"].format(dod["jmeno"]) +
                                f"  ·  {t['ico']} {dod['ico']}  ·  {t['dic']} {dod['dic']}")
                self.drawRightString(PAGE_W - OKRAJ, 32, t["strana"].format(self._pageNumber, n))
                super().showPage()
            super().save()
    return CislovanyCanvas


# --- sestavení PDF -------------------------------------------------------

def vytvor(f, dod, vystup):
    rezim = f["rezim"]
    cz = rezim == "CZ"
    t = TEXTY["CZ" if cz else "EN"]
    fmt = cislo_cz if cz else cislo_en

    d_vyst = parse_datum(f["datum_vystaveni"]) if f.get("datum_vystaveni") else date.today()
    if f.get("datum_splatnosti"):
        d_splat = parse_datum(f["datum_splatnosti"])
    else:
        d_splat = d_vyst + timedelta(days=int(f.get("splatnost_dni", 10)))
    d_duzp = parse_datum(f["duzp"]) if f.get("duzp") else d_vyst
    if d_splat < d_vyst:
        raise ChybaVstupu("Datum splatnosti je dřív než datum vystavení.")

    radky, zaklad, dph, celkem = spocitej(f)
    if celkem <= 0:
        raise ChybaVstupu("Celková částka musí být kladná.")

    if cz:
        qr_data = spayd(f, dod, celkem, zaklad, dph, d_vyst, d_splat, d_duzp)
        castka = f"{fmt(celkem)} Kč"
    else:
        qr_data = epc(f, dod, celkem)
        castka = f"€{fmt(celkem)}"

    def st(name, font="F", size=8.5, leading=12.5, color=INK, **kw):
        return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading, textColor=color, **kw)

    s_txt = st("txt")
    s_muted = st("muted", color=MUTED, size=8)
    s_label = st("label", font="FM", size=7, leading=10, color=ACCENT)
    s_name = st("name", font="FB", size=11, leading=15)
    s_th = st("th", font="FM", size=6.8, leading=9, color=MUTED)
    s_thr = st("thr", font="FM", size=6.8, leading=9, color=MUTED, alignment=TA_RIGHT)
    s_td = st("td", size=8.5, leading=11.5)
    s_tdr = st("tdr", size=8.5, leading=11.5, alignment=TA_RIGHT)
    s_tdmr = st("tdmr", font="FM", size=8.5, leading=11.5, alignment=TA_RIGHT)
    s_rl = st("rl", size=8, leading=11, color=MUTED, alignment=TA_RIGHT)
    s_rv = st("rv", size=8.5, leading=11, alignment=TA_RIGHT)
    s_rb = st("rb", font="FB", size=8.5, leading=11, alignment=TA_RIGHT)

    def idy(ico, dic):
        casti = []
        if ico:
            casti.append(f"<font color='#6B7280'>{t['ico']}</font>&nbsp;&nbsp;<font name='FM'>{ico}</font>")
        if dic:
            casti.append(f"<font color='#6B7280'>{t['dic']}</font>&nbsp;&nbsp;<font name='FM'>{dic}</font>")
        return Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;".join(casti), s_txt)

    story = [Spacer(1, 6),
             Hlavicka(t, f["cislo"], castka, datum_txt(d_splat)),
             Spacer(1, 18), Linka(), Spacer(1, 18)]

    zeme = dod["zeme_cz"] if cz else dod["zeme_en"]
    dod_bl = [Paragraph(t["dodavatel"], s_label), Spacer(1, 5),
              Paragraph(dod["jmeno"], s_name), Spacer(1, 2),
              Paragraph(dod["ulice"], s_txt), Paragraph(dod["psc_mesto"], s_txt),
              Paragraph(zeme, s_txt), Spacer(1, 7), idy(dod["ico"], dod["dic"])]
    if dod.get("platce_dph"):
        dod_bl.append(Paragraph(t["platce"], s_muted))
    o = f["odberatel"]
    odb_bl = [Paragraph(t["odberatel"], s_label), Spacer(1, 5),
              Paragraph(o["nazev"], s_name), Spacer(1, 2)]
    odb_bl += [Paragraph(r, s_txt) for r in o["adresa"]]
    if o.get("ico") or o.get("dic"):
        odb_bl += [Spacer(1, 7), idy(o.get("ico"), o.get("dic"))]
    if o.get("kontakt"):
        odb_bl += [Paragraph(f"<font color='#6B7280'>{t['kontakt']}</font>&nbsp;&nbsp;{o['kontakt']}", s_txt)]
    strany = Table([[dod_bl, odb_bl]], colWidths=[SIRKA / 2, SIRKA / 2])
    strany.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                ("RIGHTPADDING", (0, 0), (-1, -1), 12)]))
    story += [strany, Spacer(1, 22)]

    ucet = dod["ucet_czk"] if cz else dod["iban_eur"]
    story += [PlatebniKarta(t, ucet, f["cislo"], datum_txt(d_vyst), datum_txt(d_splat),
                            datum_txt(d_duzp), qr_data), Spacer(1, 22)]

    # položky
    if cz:
        hlavicka = [Paragraph(t["pocet"], s_th), Paragraph(t["popis"], s_th), Paragraph(t["cena"], s_thr),
                    Paragraph(t["sazba"], s_thr), Paragraph(t["zaklad"], s_thr), Paragraph(t["dph"], s_thr),
                    Paragraph(t["celkem"], s_thr)]
        sloupce = [52, SIRKA - 360, 62, 44, 72, 62, 68]
        data = [hlavicka] + [[
            Paragraph(f"{mnozstvi(r['pocet'])} {r['jednotka']}", s_td), Paragraph(r["popis"], s_td),
            Paragraph(fmt(r["cena"]), s_tdr), Paragraph(f"{DPH_SAZBA:.0f} %", s_tdr),
            Paragraph(fmt(r["zaklad"]), s_tdr), Paragraph(fmt(r["dph"]), s_tdr),
            Paragraph(fmt(r["celkem"]), s_tdmr)] for r in radky]
    else:
        hlavicka = [Paragraph(t["pocet"], s_th), Paragraph(t["popis"], s_th),
                    Paragraph(t["cena"], s_thr), Paragraph(t["celkem"], s_thr)]
        sloupce = [52, SIRKA - 52 - 70 - 74, 70, 74]
        data = [hlavicka] + [[
            Paragraph(f"{mnozstvi(r['pocet'])} {r['jednotka']}", s_td), Paragraph(r["popis"], s_td),
            Paragraph(fmt(r["cena"]), s_tdr), Paragraph(fmt(r["celkem"]), s_tdmr)] for r in radky]
    tab = Table(data, colWidths=sloupce, repeatRows=1)
    styl = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (0, -1), 0), ("RIGHTPADDING", (-1, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LINEBELOW", (0, 0), (-1, 0), 0.9, INK)]
    for i in range(1, len(data)):
        styl.append(("LINEBELOW", (0, i), (-1, i), 0.5, LINE))
    tab.setStyle(TableStyle(styl))
    story += [tab, Spacer(1, 14)]

    konec = []
    if cz:
        rekap = Table([
            [Paragraph(t["rekap_sazba"], s_rl), Paragraph(t["rekap_zaklad"], s_rl),
             Paragraph(t["rekap_dph"], s_rl), Paragraph(t["rekap_celkem"], s_rl)],
            [Paragraph(f"{DPH_SAZBA:.0f} %", s_rv), Paragraph(fmt(zaklad), s_rv),
             Paragraph(fmt(dph), s_rv), Paragraph(fmt(celkem), s_rv)],
            [Paragraph(t["rekap_celkem"], s_rb), Paragraph(fmt(zaklad), s_rb),
             Paragraph(fmt(dph), s_rb), Paragraph(fmt(celkem), s_rb)],
        ], colWidths=[60, 75, 60, 75], hAlign="RIGHT")
        rekap.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                                   ("RIGHTPADDING", (-1, 0), (-1, -1), 0),
                                   ("LINEABOVE", (0, 2), (-1, 2), 0.5, LINE)]))
        konec += [rekap, Spacer(1, 12)]
    konec.append(CelkemBlok(t["k_uhrade"], castka))
    poznamka = f.get("poznamka", POZNAMKA_DPH.get(rezim, ""))
    if poznamka:
        konec += [Spacer(1, 18), Paragraph(poznamka, s_muted)]
    story.append(KeepTogether(konec))

    vystup.parent.mkdir(parents=True, exist_ok=True)
    # rámec má vnitřní odsazení 6 pt, obsah tak začíná přesně na OKRAJ
    doc = SimpleDocTemplate(str(vystup), pagesize=A4, leftMargin=OKRAJ - 6, rightMargin=OKRAJ - 6,
                            topMargin=38, bottomMargin=60,
                            title=t["titul_pdf"].format(f["cislo"]), author=dod["jmeno"])
    doc.build(story, canvasmaker=pata_factory(t, dod))

    return {
        "cislo": f["cislo"], "rezim": rezim, "odberatel": o["nazev"],
        "datum_vystaveni": datum_txt(d_vyst), "datum_splatnosti": datum_txt(d_splat),
        "duzp": datum_txt(d_duzp), "zaklad": f"{zaklad:.2f}", "dph": f"{dph:.2f}",
        "celkem": f"{celkem:.2f}", "mena": "CZK" if cz else "EUR", "qr": qr_data, "pdf": str(vystup),
    }



def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    vstup = Path(sys.argv[1])
    f = json.loads(vstup.read_text(encoding="utf-8"))
    f["cislo"] = str(f.get("cislo", ""))
    f["rezim"] = f.get("rezim", "CZ")
    dod = json.loads((ROOT / "fakturace" / "dodavatel.json").read_text(encoding="utf-8"))
    vystup = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "vystupy" / "faktury" / f"Faktura_{f['cislo']}.pdf"
    try:
        zkontroluj(f, dod)
        registruj_fonty()
        souhrn = vytvor(f, dod, vystup)
    except ChybaVstupu as e:
        print(f"CHYBA:\n{e}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(souhrn, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

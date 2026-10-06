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
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
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

MODRA = HexColor("#0F5A8C")
NADPIS = HexColor("#1B6CA8")
SEDA = HexColor("#9AA3B5")
PRUH = HexColor("#F3F5F8")
LINKA = HexColor("#E3E7ED")

PAGE_W, PAGE_H = A4
OKRAJ = 42

TEXTY = {
    "CZ": {
        "titulek": "FAKTURA - DAŇOVÝ DOKLAD č. {}", "evidencni": "Evidenční č. {}",
        "dodavatel": "DODAVATEL", "odberatel": "ODBĚRATEL", "ico": "IČO", "dic": "DIČ",
        "platce": "Plátce DPH", "kontakt": "Kontaktní údaje",
        "platebni": "Platební údaje", "ucet": "Číslo účtu", "forma": "Forma úhrady",
        "prevod": "Převodem", "vs": "Variabilní symbol", "qr": "QR Platba + F",
        "vystaveni": "Datum vystavení", "splatnost": "Datum splatnosti", "duzp": "Datum zd. plnění",
        "pocet": "Počet", "popis": "Popis", "cena": "Jedn. cena", "sazba": "Sazba DPH",
        "zaklad": "Základ daně", "dph": "DPH", "celkem": "Celkem", "zaklad_r": "Základ",
        "k_uhrade": "Celkem k úhradě", "vystavil": "Vystavil(a) {}", "strana": "Strana {} z {}",
    },
    "EN": {
        "titulek": "INVOICE no. {}", "evidencni": None,
        "dodavatel": "SUPPLIER", "odberatel": "CUSTOMER", "ico": "Company ID", "dic": "VAT ID",
        "platce": "VAT registered", "kontakt": "Contact",
        "platebni": "Payment info", "ucet": "IBAN", "forma": "Payment method",
        "prevod": "Bank transfer", "vs": "Variable symbol", "qr": "SEPA payment",
        "vystaveni": "Issue date", "splatnost": "Due date", "duzp": "Date of taxable supply",
        "pocet": "Quantity", "popis": "Description", "cena": "Unit price", "celkem": "Total",
        "k_uhrade": "Total due", "vystavil": "Issued by {}", "strana": "Page {} of {}",
    },
}

POZNAMKA_DPH = {
    "EU": "VAT exempt – intra-Community supply of goods (Art. 138 Directive 2006/112/EC, § 64 Czech VAT Act).",
    "EXPORT": "VAT exempt – export of goods (Art. 146 Directive 2006/112/EC, § 66 Czech VAT Act).",
}

FONT_CANDIDATES = [
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
     "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial.ttf",
     "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/Library/Fonts/Arial.ttf", "/Library/Fonts/Arial Bold.ttf"),
    ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
]


class ChybaVstupu(Exception):
    pass


def registruj_fonty():
    for reg, bold in FONT_CANDIDATES:
        if Path(reg).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("F", reg))
            pdfmetrics.registerFont(TTFont("FB", bold))
            return
    raise ChybaVstupu("Nenašel jsem žádný TTF font s českou diakritikou (Liberation Sans, DejaVu Sans, Arial).")


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


class QR(Flowable):
    def __init__(self, data, size):
        super().__init__()
        self.data, self.size = data, size
        self.width = self.height = size

    def draw(self):
        w = QrCodeWidget(self.data, barLevel="M", barBorder=0)
        x0, y0, x1, y1 = w.getBounds()
        d = Drawing(self.size, self.size,
                    transform=[self.size / (x1 - x0), 0, 0, self.size / (y1 - y0), 0, 0])
        d.add(w)
        renderPDF.draw(d, self.canv, 0, 0)


# --- grafické bloky ------------------------------------------------------

class PlatebniPas(Flowable):
    """Modrý pás s platebními údaji, QR kódem a daty – jako na vzorových fakturách."""

    def __init__(self, t, ucet_label, ucet, cislo, qr_data, data_radky, sirka):
        super().__init__()
        self.t, self.ucet_label, self.ucet, self.cislo = t, ucet_label, ucet, cislo
        self.qr_data, self.data_radky = qr_data, data_radky
        self.width, self.height = sirka, 100

    def draw(self):
        c = self.canv
        pas_r = self.width * 0.755
        c.setFillColor(MODRA)
        c.rect(-OKRAJ, 0, OKRAJ + pas_r, self.height, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("FB", 7.5)
        c.drawString(0, self.height - 22, self.t["platebni"])
        c.setFont("F", 7.5)
        c.drawString(0, self.height - 38, self.ucet_label)
        c.drawString(160, self.height - 38, self.t["forma"])
        c.drawString(160, self.height - 52, self.t["vs"])
        c.setFont("FB", 7.5)
        c.drawString(52, self.height - 38, self.ucet)
        c.drawString(240, self.height - 38, self.t["prevod"])
        c.drawString(240, self.height - 52, str(self.cislo))
        # QR na bílém podkladu přesahujícím pás
        qr_size, pad = 66, 5
        qx = pas_r - qr_size - 2 * pad - 6
        qy = self.height - qr_size - 2 * pad - 10
        c.setFillColor(white)
        c.setStrokeColor(MODRA)
        c.rect(qx, qy - 6, qr_size + 2 * pad, qr_size + 2 * pad + 6, stroke=1, fill=1)
        QR(self.qr_data, qr_size).drawOn(c, qx + pad, qy + pad)
        c.setFillColor(HexColor("#333333"))
        c.setFont("F", 5)
        c.drawCentredString(qx + pad + qr_size / 2, qy - 2, self.t["qr"])
        # data vpravo
        dx = pas_r + 8
        y = self.height - 30
        for label, hodnota in self.data_radky:
            c.setFont("F", 7)
            c.setFillColor(HexColor("#222222"))
            c.drawString(dx, y, label)
            c.setFont("FB", 7)
            c.drawRightString(self.width, y, hodnota)
            y -= 15


class CelkemPas(Flowable):
    def __init__(self, label, castka, sirka):
        super().__init__()
        self.label, self.castka = label, castka
        self.width, self.height = sirka, 38

    def draw(self):
        c = self.canv
        x = self.width * 0.53
        c.setFillColor(MODRA)
        c.rect(x, 0, self.width - x + OKRAJ, self.height, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("FB", 11)
        c.drawString(x + 12, 14, self.label)
        c.drawRightString(self.width, 14, self.castka)


def pata_factory(t, jmeno):
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
                self.setFont("F", 7)
                self.setFillColor(HexColor("#333333"))
                self.drawString(OKRAJ, 28, t["vystavil"].format(jmeno))
                self.drawCentredString(PAGE_W / 2, 28, t["strana"].format(self._pageNumber, n))
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
    else:
        qr_data = epc(f, dod, celkem)

    st = lambda name, **kw: ParagraphStyle(name, fontName=kw.pop("font", "F"), fontSize=kw.pop("size", 7.5),
                                           leading=kw.pop("leading", 10.5), **kw)
    s_txt = st("txt")
    s_b = st("b", font="FB")
    s_head = st("head", font="FB", size=13, leading=16, textColor=NADPIS)
    s_titul = st("titul", font="FB", size=15, leading=19, alignment=TA_RIGHT)
    s_evid = st("evid", font="FB", size=10.5, leading=14, alignment=TA_RIGHT, textColor=SEDA)
    s_th = st("th", font="FB", size=7)
    s_thr = st("thr", font="FB", size=7, alignment=TA_RIGHT)
    s_td = st("td", size=7.5)
    s_tdr = st("tdr", size=7.5, alignment=TA_RIGHT)
    s_tdbr = st("tdbr", font="FB", size=7.5, alignment=TA_RIGHT)

    sirka = PAGE_W - 2 * OKRAJ
    story = [Paragraph(t["titulek"].format(f["cislo"]), s_titul)]
    if t["evidencni"]:
        story.append(Paragraph(t["evidencni"].format(f["cislo"]), s_evid))
    story.append(Spacer(1, 22))

    zeme = dod["zeme_cz"] if cz else dod["zeme_en"]
    dod_bl = [Paragraph(t["dodavatel"], s_head), Spacer(1, 8),
              Paragraph(dod["jmeno"], s_b), Paragraph(dod["ulice"], s_txt),
              Paragraph(dod["psc_mesto"], s_txt), Paragraph(zeme, s_txt), Spacer(1, 8),
              Paragraph(f"<font name='FB'>{t['ico']}</font> {dod['ico']}&nbsp;&nbsp;&nbsp;"
                        f"<font name='FB'>{t['dic']}</font> {dod['dic']}", s_txt)]
    if dod.get("platce_dph"):
        dod_bl.append(Paragraph(t["platce"], s_b))
    o = f["odberatel"]
    odb_bl = [Paragraph(t["odberatel"], s_head), Spacer(1, 8), Paragraph(o["nazev"], s_b)]
    odb_bl += [Paragraph(r, s_txt) for r in o["adresa"]]
    ids = []
    if o.get("ico"):
        ids.append(f"<font name='FB'>{t['ico']}</font> {o['ico']}")
    if o.get("dic"):
        ids.append(f"<font name='FB'>{t['dic']}</font> {o['dic']}")
    if ids:
        odb_bl += [Spacer(1, 8), Paragraph("&nbsp;&nbsp;&nbsp;".join(ids), s_txt)]
    if o.get("kontakt"):
        odb_bl += [Spacer(1, 8), Paragraph(t["kontakt"], s_b), Paragraph(o["kontakt"], s_txt)]
    strany = Table([[dod_bl, odb_bl]], colWidths=[sirka / 2, sirka / 2])
    strany.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    story += [strany, Spacer(1, 40)]

    data_radky = [(t["vystaveni"], datum_txt(d_vyst)), (t["splatnost"], datum_txt(d_splat)),
                  (t["duzp"], datum_txt(d_duzp))]
    ucet = dod["ucet_czk"] if cz else dod["iban_eur"]
    story += [PlatebniPas(t, t["ucet"], ucet, f["cislo"], qr_data, data_radky, sirka), Spacer(1, 10)]

    # položky
    if cz:
        hlavicka = [Paragraph(t["pocet"], s_th), Paragraph(t["popis"], s_th), Paragraph(t["cena"], s_thr),
                    Paragraph(t["sazba"], s_thr), Paragraph(t["zaklad"], s_thr), Paragraph(t["dph"], s_thr),
                    Paragraph(t["celkem"], s_thr)]
        sloupce = [50, 140, 60, 52, 75, 62, sirka - 439]
        data = [hlavicka] + [[
            Paragraph(f"{mnozstvi(r['pocet'])} {r['jednotka']}", s_td), Paragraph(r["popis"], s_td),
            Paragraph(fmt(r["cena"]), s_tdr), Paragraph(f"{DPH_SAZBA:.0f} %", s_tdr),
            Paragraph(fmt(r["zaklad"]), s_tdr), Paragraph(fmt(r["dph"]), s_tdr),
            Paragraph(fmt(r["celkem"]), s_tdr)] for r in radky]
    else:
        hlavicka = [Paragraph(t["pocet"], s_th), Paragraph(t["popis"], s_th),
                    Paragraph(t["cena"], s_thr), Paragraph(t["celkem"], s_thr)]
        sloupce = [58, sirka - 58 - 70 - 70, 70, 70]
        data = [hlavicka] + [[
            Paragraph(f"{mnozstvi(r['pocet'])} {r['jednotka']}", s_td), Paragraph(r["popis"], s_td),
            Paragraph(fmt(r["cena"]), s_tdr), Paragraph(fmt(r["celkem"]), s_tdr)] for r in radky]
    tab = Table(data, colWidths=sloupce, repeatRows=1)
    styl = [("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LINEBELOW", (0, 0), (-1, 0), 0.6, LINKA),
            ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    for i in range(1, len(data)):
        if i % 2 == 1:
            styl.append(("BACKGROUND", (0, i), (-1, i), PRUH))
        styl.append(("LINEBELOW", (0, i), (-1, i), 0.4, LINKA))
    tab.setStyle(TableStyle(styl))
    story += [tab, Spacer(1, 14)]

    konec = []
    if cz:
        rekap = Table([
            [Paragraph(t["sazba"], s_thr), Paragraph(t["zaklad_r"], s_thr), Paragraph(t["dph"], s_thr),
             Paragraph(t["celkem"], s_thr)],
            [Paragraph(f"{DPH_SAZBA:.0f} %", s_tdr), Paragraph(fmt(zaklad), s_tdr), Paragraph(fmt(dph), s_tdr),
             Paragraph(fmt(celkem), s_tdr)],
            [Paragraph(t["celkem"], s_tdbr), Paragraph(fmt(zaklad), s_tdbr), Paragraph(fmt(dph), s_tdbr),
             Paragraph(fmt(celkem), s_tdbr)],
        ], colWidths=[70, 90, 70, 90], hAlign="RIGHT")
        rekap.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        konec += [rekap, Spacer(1, 10)]
        castka = f"{fmt(celkem)} Kč"
    else:
        castka = f"€{fmt(celkem)}"
    konec.append(CelkemPas(t["k_uhrade"], castka, sirka))
    poznamka = f.get("poznamka", POZNAMKA_DPH.get(rezim, ""))
    if poznamka:
        konec += [Spacer(1, 16), Paragraph(poznamka, s_txt)]
    story.append(KeepTogether(konec))

    vystup.parent.mkdir(parents=True, exist_ok=True)
    # rámec má vnitřní odsazení 6 pt, obsah tak začíná přesně na OKRAJ
    doc = SimpleDocTemplate(str(vystup), pagesize=A4, leftMargin=OKRAJ - 6, rightMargin=OKRAJ - 6,
                            topMargin=40, bottomMargin=55,
                            title=t["titulek"].format(f["cislo"]), author=dod["jmeno"])
    doc.build(story, canvasmaker=pata_factory(t, dod["jmeno"]))

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

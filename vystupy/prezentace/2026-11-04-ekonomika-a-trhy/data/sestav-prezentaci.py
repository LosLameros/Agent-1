"""Sestaví prezentaci Ekonomika a trhy – listopad 2026 z původní šablony hlavního ekonoma."""
import csv
import copy
import datetime as dt
import sys

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION, XL_TICK_MARK
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

SRC, DATA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

DARK = RGBColor(0x1F, 0x38, 0x64)
GRAY = RGBColor(0xA6, 0xA6, 0xA6)
UP = RGBColor(0xC5, 0x5A, 0x11)
MUTED = RGBColor(0x59, 0x59, 0x59)
BLACK = RGBColor(0, 0, 0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HEAD = RGBColor(0xE7, 0xE6, 0xE6)
ROW = RGBColor(0xF7, 0xF7, 0xF7)
GOOD = RGBColor(0xE2, 0xF0, 0xD9)
BAD = RGBColor(0xFB, 0xE5, 0xD6)

L, W = 0.92, 11.5  # levý okraj a šířka obsahu jako v šabloně

prs = Presentation(SRC)
LAY = {l.name: l for l in prs.slide_layouts}

# --- titulní slajd: jen datum -------------------------------------------------
s1 = prs.slides[0]
for ph in s1.placeholders:
    if ph.placeholder_format.idx == 1:
        ph.text_frame.paragraphs[0].runs[0].text = "Listopad 2026"

# --- smazat původní slajdy 2–17 -----------------------------------------------
lst = prs.slides._sldIdLst
for sid in list(lst)[1:]:
    prs.part.drop_rel(sid.rId)
    lst.remove(sid)


# --- pomocné funkce -------------------------------------------------------------
def new_slide(layout, title):
    s = prs.slides.add_slide(LAY[layout])
    s.shapes.title.text = title
    s.shapes.title.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    return s


def set_bullet(p, level_indent=0.3):
    pPr = p._p.get_or_add_pPr()
    pPr.set("marL", str(Inches(level_indent)))
    pPr.set("indent", str(-Inches(level_indent)))
    for tag in ("a:buFont", "a:buChar"):
        old = pPr.find(qn(tag))
        if old is not None:
            pPr.remove(old)
    bf = etree.SubElement(pPr, qn("a:buFont"))
    bf.set("typeface", "Arial")
    bc = etree.SubElement(pPr, qn("a:buChar"))
    bc.set("char", "•")


def fill_paragraphs(tf, items, size, bullets=True, space=8, color=None):
    """items: list of str or list of (text, bold) runs."""
    tf.word_wrap = True
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        runs = [(it, False)] if isinstance(it, str) else it
        for text, bold in runs:
            r = p.add_run()
            r.text = text
            r.font.size = Pt(size)
            r.font.bold = bold
            if color is not None:
                r.font.color.rgb = color
        p.space_after = Pt(space)
        if bullets:
            set_bullet(p)
    return tf


def textbox(s, x, y, w, h, items, size, bullets=False, space=6, color=None, anchor=MSO_ANCHOR.TOP, align=None, name=None):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.vertical_anchor = anchor
    fill_paragraphs(tf, items, size, bullets=bullets, space=space, color=color)
    if align is not None:
        for p in tf.paragraphs:
            p.alignment = align
    return tb


def meaning(s, text, y=6.2, label="Co to znamená: "):
    return textbox(s, L, y, W, 0.5, [[(label, True), (text, False)]], 16, name="Co to znamená")


def source(s, text, y=6.82):
    return textbox(s, L, y, W, 0.3, [text], 11, color=MUTED, name="Zdroj")


def style_chart_common(chart, size=12):
    chart.font.size = Pt(size)


def cell_text(cell, runs, size, bold=False, color=BLACK, align=PP_ALIGN.LEFT):
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    for text, b in ([(runs, bold)] if isinstance(runs, str) else runs):
        r = p.add_run()
        r.text = text
        r.font.size = Pt(size)
        r.font.bold = b
        r.font.color.rgb = color
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = cell.margin_right = Inches(0.1)
    cell.margin_top = cell.margin_bottom = Inches(0.05)


def table(s, x, y, colw, rowh, data, size, fills):
    shp = s.shapes.add_table(len(data), len(colw), Inches(x), Inches(y), Inches(sum(colw)), Inches(sum(rowh)))
    t = shp.table
    t.first_row = True
    t.horz_banding = False
    for i, w in enumerate(colw):
        t.columns[i].width = Inches(w)
    for i, h in enumerate(rowh):
        t.rows[i].height = Inches(h)
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = fills(r, c)
            bold = r == 0 or c == 0
            cell_text(cell, val, size, bold=bold)
    return shp


# --- data ---------------------------------------------------------------------
perf = list(csv.DictReader(open(f"{DATA}/vykonnost-trhu.csv")))
brent = [(dt.date.fromisoformat(r["datum"]), float(r["brent_usd"])) for r in csv.DictReader(open(f"{DATA}/brent-2026.csv"))]
yields = list(csv.DictReader(open(f"{DATA}/vynosy-10y.csv")))

PCT = '+0.0" %";"−"0.0" %";0.0" %"'
BP = '+0" bb";"−"0" bb";0" bb"'

# ============================================================================
# 2 – Časová osa
# ============================================================================
s = new_slide("Title Only", "Co se stalo od začátku října")
events = [
    ("6. 10.", "Americké akcie na historickém maximu", False),
    ("23. 10.", "Ropa Brent nejdražší za čtyři roky", False),
    ("28.–29. 10.", "Fed a ECB nechaly sazby beze změny", False),
    ("28.–30. 10.", "Výsledky velkých firem z USA, výprodej technologií", False),
    ("2. 11.", "Naděje na dohodu USA a Íránu, ropa zlevnila", False),
    ("3. 11.", "Volby do Kongresu USA", False),
    ("5. 11.", "ČNB rozhoduje o sazbách", True),
]
y_line = 3.45
x0, x1 = 1.55, 11.79
ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x0 - 0.35), Inches(y_line), Inches(x1 + 0.35), Inches(y_line))
ln.line.color.rgb = GRAY
ln.line.width = Pt(2)
ln.name = "Časová osa"
step = (x1 - x0) / (len(events) - 1)
for i, (d, txt, future) in enumerate(events):
    cx = x0 + i * step
    r = 0.13
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - r), Inches(y_line - r), Inches(2 * r), Inches(2 * r))
    dot.name = f"Bod {i + 1}"
    dot.shadow.inherit = False
    if future:
        dot.fill.solid()
        dot.fill.fore_color.rgb = WHITE
        dot.line.color.rgb = DARK
        dot.line.width = Pt(2)
    else:
        dot.fill.solid()
        dot.fill.fore_color.rgb = DARK
        dot.line.fill.background()
    bw = 1.62
    textbox(s, cx - bw / 2, 2.55, bw, 0.6, [[(d, True)]], 18, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM,
            color=MUTED if future else BLACK, name=f"Datum {i + 1}")
    textbox(s, cx - bw / 2, 3.75, bw, 1.6, [txt + (" (čeká se)" if future else "")], 15, align=PP_ALIGN.CENTER,
            color=MUTED if future else BLACK, name=f"Událost {i + 1}")
textbox(s, L, 5.75, W, 0.5,
        [[("Dnes: ", True), ("jak se dařilo trhům · energie · centrální banky · výsledky firem a technologie · "
                             "dluhopisy a Francie · scénáře vývoje", False)]], 16, align=PP_ALIGN.CENTER, name="Osnova")

# ============================================================================
# 3 – Výkonnost trhů
# ============================================================================
s = new_slide("Title Only", "Technologie dolů, Praha v plusu")


def perf_chart(x, title, kl, kc, vmin, vmax):
    cd = CategoryChartData()
    cd.categories = [r["index"] for r in perf]
    cd.add_series("v místní měně", [round(float(r[kl]), 1) for r in perf])
    cd.add_series("v korunách", [round(float(r[kc]), 1) for r in perf])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(x), Inches(1.85), Inches(5.6), Inches(4.25), cd)
    gf.name = title
    ch = gf.chart
    style_chart_common(ch, 12)
    ch.has_title = True
    ch.chart_title.text_frame.text = title
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(14)
    ch.chart_title.text_frame.paragraphs[0].runs[0].font.bold = True
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(12)
    pl = ch.plots[0]
    pl.gap_width = 55
    pl.overlap = 0
    pl.has_data_labels = True
    dl = pl.data_labels
    dl.number_format = PCT
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(11)
    for ser, col in zip(pl.series, (GRAY, DARK)):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = col
        ser.invert_if_negative = False
    ca = ch.category_axis
    ca.reverse_order = True
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.has_major_gridlines = False
    ca.format.line.color.rgb = GRAY
    ca.tick_labels.font.size = Pt(12)
    va = ch.value_axis
    va.minimum_scale = vmin
    va.maximum_scale = vmax
    va.has_major_gridlines = False
    va.visible = False
    return gf


perf_chart(L, "Poslední měsíc (2. 10. – 2. 11. 2026)", "1M_lokalne_%", "1M_CZK_%", -13, 6)
perf_chart(L + 5.9, "Poslední 3 měsíce (31. 7. – 2. 11. 2026)", "3M_lokalne_%", "3M_CZK_%", -6, 7.5)
meaning(s, "za měsíc kurz koruny skoro nehrál roli. Za tři měsíce dražší dolar výnos v korunách zvýšil.")
source(s, "Zdroj: Trading Economics, zavírací ceny; přepočet do CZK kurzy USD, EUR a JPY ke stejným dnům. Nasdaq 100 podle indexu US100.")

# ============================================================================
# 4 – Energie
# ============================================================================
s = new_slide("Title Only", "Ropa: rekord, pak naděje na dohodu")
cd = CategoryChartData()
cd.categories = [d for d, _ in brent]
cd.add_series("Brent (USD za barel)", [v for _, v in brent])
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(L), Inches(1.85), Inches(6.4), Inches(4.25), cd)
gf.name = "Ropa Brent 2026"
ch = gf.chart
style_chart_common(ch, 12)
ch.has_title = True
ch.chart_title.text_frame.text = "Ropa Brent v roce 2026 (USD za barel)"
ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(14)
ch.chart_title.text_frame.paragraphs[0].runs[0].font.bold = True
ch.has_legend = False
ser = ch.plots[0].series[0]
ser.smooth = False
ser.format.line.color.rgb = DARK
ser.format.line.width = Pt(2)

from pptx.enum.chart import XL_MARKER_STYLE  # noqa: E402

ser.marker.style = XL_MARKER_STYLE.NONE
labels = {dt.date(2026, 10, 23): "116,72 (23. 10.)", dt.date(2026, 11, 2): "104,77"}
dates = [d for d, _ in brent]
for d, txt in labels.items():
    i = dates.index(d)
    pt = ser.points[i]
    pt.data_label.has_text_frame = True
    pt.data_label.text_frame.text = txt
    pt.data_label.text_frame.paragraphs[0].runs[0].font.size = Pt(11)
    pt.data_label.position = XL_LABEL_POSITION.ABOVE if d != dt.date(2026, 11, 2) else XL_LABEL_POSITION.BELOW
    pt.marker.style = XL_MARKER_STYLE.CIRCLE
    pt.marker.size = 6
    pt.marker.format.fill.solid()
    pt.marker.format.fill.fore_color.rgb = DARK
    pt.marker.format.line.color.rgb = DARK
va = ch.value_axis
va.minimum_scale = 50
va.maximum_scale = 130
va.major_unit = 20
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = RGBColor(0xE7, 0xE7, 0xEB)
va.format.line.fill.background()
va.tick_labels.font.size = Pt(11)
ca = ch.category_axis
ca.tick_labels.font.size = Pt(11)
ca.major_tick_mark = XL_TICK_MARK.NONE
ca.format.line.color.rgb = GRAY
ca.tick_labels.number_format = '[$-405]mmm'
ca.tick_labels.number_format_is_linked = False
# měsíční popisky datové osy
dax = ch._chartSpace.find(".//" + qn("c:dateAx"))
for tag in ("c:majorUnit", "c:majorTimeUnit", "c:baseTimeUnit"):
    e = dax.find(qn(tag))
    if e is not None:
        dax.remove(e)
anchor = dax.find(qn("c:lblOffset"))
idx = list(dax).index(anchor) + 1
for k, (tag, val) in enumerate((("c:baseTimeUnit", "days"), ("c:majorUnit", "1"), ("c:majorTimeUnit", "months"))):
    el = etree.Element(qn(tag))
    el.set("val", val)
    dax.insert(idx + k, el)

textbox(s, L + 6.65, 1.95, 4.85, 4.2, [
    "Hormuzský průliv je od března téměř zavřený, útoky na lodě pokračují",
    "Před válkou (konec února) stál Brent 73 USD",
    "23. 10. Brent nejdražší za čtyři roky",
    "2. 11. naděje na dohodu USA a Íránu: ropa za den −7,6 %",
    "3. 11. hlášen úder USA na íránský ostrov Kešm",
    "Plyn v Evropě minulý týden nad 100 EUR/MWh, poprvé od roku 2022; zásobníky jsou pod průměrem",
], 16, bullets=True, space=10, name="Body")
meaning(s, "drahé energie drží inflaci nahoře, Evropě hrozí dražší energie i v příštím roce.")
source(s, "Zdroj: Trading Economics (Brent, denní zavírací ceny 2. 1. – 2. 11. 2026; plyn TTF; zprávy k 3. 11. 2026)")

# ============================================================================
# 5 – Centrální banky
# ============================================================================
s = new_slide("Title Only", "Sazby: pauza, ne konec zvyšování")
data = [
    ["Banka", "Poslední rozhodnutí", "Co dál"],
    ["Fed (USA)", "28. 10.: beze změny, 3,75–4,00 %", "Trh čeká zvýšení 9. 12. Inflace drží nahoře, ekonomika roste."],
    ["ECB (eurozóna)", "29. 10.: beze změny, 2,50 %", "O zvýšení se jednalo, trh s ním dál počítá. Lagardeová odejde z čela ECB předčasně."],
    ["ČNB", "drží 3,75 %", "5. 11. analytici čekají zvýšení na 4,00 %. Inflace v září 2,5 %, zdražují hlavně služby."],
]
table(s, L, 2.0, [2.4, 3.6, 5.5], [0.6, 1.05, 1.05, 1.05], data, 17,
      lambda r, c: HEAD if r == 0 else (ROW if r % 2 == 0 else WHITE))
meaning(s, "sazby spíš ještě porostou. Vyšší úroky z vkladů a nových dluhopisů, tlak na drahé akcie.")
source(s, "Zdroj: Fed, ECB, ČNB, Trading Economics, ČTK (odhady analytiků), k 3. 11. 2026")

# ============================================================================
# 6 – Výsledková sezóna a technologie
# ============================================================================
s = new_slide("Comparison", "Zisky rostou, trh trestá sázky na AI")
ph = {p.placeholder_format.idx: p for p in s.placeholders}
for idx, txt in ((1, "Výsledková sezóna v USA"), (3, "Proč klesaly technologie")):
    tf = ph[idx].text_frame
    tf.text = txt
    tf.paragraphs[0].runs[0].font.size = Pt(22)
    tf.paragraphs[0].runs[0].font.bold = True
left = [
    "Zisky firem dál rostou rychle, většina firem překonává odhady",
    "Daří se napříč odvětvími, nejvíc energetice a technologiím",
    "Firmy ale odhady překonávají o méně než dřív, trh je vybíravější",
    "Ocenění akcií je pod průměrem posledních let, akcie nejsou přehnaně drahé",
]
right = [
    "Firmy utrácejí za AI a datová centra víc, než trh čekal",
    "Investoři pochybují, kdy se tyto investice vrátí",
    "Část firem zklamala výhledem, některé si na investice půjčují nebo vydávají nové akcie",
    "Po velkém růstu stačilo málo, výprodej se přelil i do Asie",
]
for idx, items in ((2, left), (4, right)):
    p_ = ph[idx]
    p_.left, p_.top, p_.width, p_.height = (Inches(0.92) if idx == 2 else Inches(6.75)), Inches(2.74), (Inches(5.64) if idx == 2 else Inches(5.67)), Inches(3.3)
    tf = p_.text_frame
    tf.clear()
    fill_paragraphs(tf, items, 18, bullets=False, space=10)
    bp = tf._txBody.find(qn("a:bodyPr"))
    for child in list(bp):
        bp.remove(child)
    etree.SubElement(bp, qn("a:normAutofit"))
meaning(s, "nejde o krach firem, ale o přecenění očekávání. Zbytek trhu přitom držel.")
source(s, "Zdroj: FactSet (Earnings Insight, 30. 10. 2026), Trading Economics, výsledky firem")

# ============================================================================
# 7 – Dluhopisy a Francie
# ============================================================================
s = new_slide("Title Only", "Dluhopisy tlumily pokles akcií")
cd = CategoryChartData()
cd.categories = [f"{r['zeme']} ({float(r['vynos_10y_2026-11-03_%']):.2f} %)".replace(".", ",") for r in yields]
cd.add_series("Změna za měsíc (bb)", [int(r["zmena_bb"]) for r in yields])
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(L), Inches(1.85), Inches(6.0), Inches(4.25), cd)
gf.name = "Změna výnosů 10Y"
ch = gf.chart
style_chart_common(ch, 12)
ch.has_title = True
ch.chart_title.text_frame.text = "Změna výnosu 10letých dluhopisů za měsíc"
ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(14)
ch.chart_title.text_frame.paragraphs[0].runs[0].font.bold = True
ch.has_legend = False
pl = ch.plots[0]
pl.gap_width = 60
pl.has_data_labels = True
pl.data_labels.number_format = BP
pl.data_labels.number_format_is_linked = False
pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
pl.data_labels.font.size = Pt(12)
ser = pl.series[0]
ser.invert_if_negative = False
ser.format.fill.solid()
ser.format.fill.fore_color.rgb = DARK
for i, r in enumerate(yields):
    if int(r["zmena_bb"]) > 0:
        pt = ser.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = UP
ca = ch.category_axis
ca.reverse_order = True
ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
ca.major_tick_mark = XL_TICK_MARK.NONE
ca.format.line.color.rgb = GRAY
ca.tick_labels.font.size = Pt(12)
va = ch.value_axis
va.minimum_scale = -50
va.maximum_scale = 20
va.has_major_gridlines = False
va.visible = False
textbox(s, L + 6.3, 1.95, 5.2, 4.2, [
    "Při výprodeji technologií hledali investoři bezpečí: výnosy klesly, ceny dluhopisů vzrostly",
    "Česko: výnosy nespadly, trh čeká zvýšení sazeb ČNB",
    "Francie: příplatek proti Německu nejvyšší od roku 2012, Fitch zhoršil výhled ratingu",
    "Do Itálie ani Německa se francouzské problémy zatím nešíří",
], 16, bullets=True, space=10, name="Body")
meaning(s, "dluhopisy fungovaly jako polštář. Výnosy kolem 5 % (USA, Česko) jsou i slušný příjem.")
source(s, "Zdroj: Trading Economics, výnosy 10letých dluhopisů 3. 11. 2026 proti stavu před měsícem; v závorce výnos; bb = setina p. b.")

# ============================================================================
# 8 – Shrnutí
# ============================================================================
s = new_slide("Title and Content", "Shrnutí: kde jsou trhy teď")
body = [p for p in s.placeholders if p.placeholder_format.idx == 1][0]
body.left, body.top, body.width, body.height = Inches(0.92), Inches(2.0), Inches(11.5), Inches(4.6)
tf = body.text_frame
items = [
    [("Energie: ", True), ("ropa a plyn jsou drahé, spor USA a Íránu kolísá mezi jednáním a údery", False)],
    [("Inflace a sazby: ", True), ("energie drží inflaci nahoře, centrální banky spíš ještě zvýší", False)],
    [("Akcie: ", True), ("zisky rostou, trh ale trestá drahé sázky na AI, zbytek trhu drží", False)],
    [("Dluhopisy: ", True), ("výnosy kolem 5 % dávají příjem i ochranu při poklesu akcií", False)],
    [("Evropa: ", True), ("hlavní rizika jsou drahé energie a Francie", False)],
    [("Volby v USA: ", True), ("krátkodobý šum; od roku 1950 byl S&P 500 rok po volbách do Kongresu vždy výš", False)],
]
fill_paragraphs(tf, items, 22, bullets=False, space=12)
bp = tf._txBody.find(qn("a:bodyPr"))
for child in list(bp):
    bp.remove(child)
etree.SubElement(bp, qn("a:normAutofit"))
source(s, "Zdroj: Trading Economics, FactSet, centrální banky; historie voleb: U.S. Bank, BNY. Minulý vývoj není zárukou budoucího.")

# ============================================================================
# 9 – Scénáře
# ============================================================================
s = new_slide("Title Only", "Možné scénáře vývoje")
data = [
    ["", "Lepší scénář", "Základní scénář", "Horší scénář"],
    ["Írán a energie", "Dohoda, Hormuz se otevře, ropa a plyn rychle zlevní", "Jednání se táhnou, energie zůstávají drahé", "Nové údery, ropa nad říjnovým maximem"],
    ["Inflace a sazby", "Inflace polevuje, zvyšování sazeb končí", "Ještě jedno zvýšení (ČNB, Fed), pak pauza", "Banky zvyšují dál, výnosy dluhopisů rostou"],
    ["Akcie", "Růst se rozšíří, technologie se vzpamatují", "Kolísání, oporou jsou zisky, peníze se přelévají mimo technologie", "Zklamání z AI se prohloubí, akcie klesají"],
    ["Dluhopisy", "Výnosy klesají, dluhopisy zdražují", "Stabilní příjem kolem 5 %", "Další ztráty u dlouhých splatností"],
]


def scen_fill(r, c):
    if c == 0:
        return HEAD
    if r == 0:
        return {1: GOOD, 2: HEAD, 3: BAD}[c]
    return WHITE if r % 2 else ROW


table(s, L, 1.95, [2.2, 3.1, 3.1, 3.1], [0.55, 0.9, 0.9, 0.9, 0.75], data, 16, scen_fill)
meaning(s, "výsledek voleb do Kongresu (4. 11.), ČNB (5. 11.), jednání s Íránem, Fed (9. 12.)", y=6.2, label="Co sledovat: ")

# ============================================================================
# 10 – Závěr
# ============================================================================
s = new_slide("Comparison", "Co z toho plyne pro investory")
ph = {p.placeholder_format.idx: p for p in s.placeholders}
for idx, txt in ((1, "Diverzifikace se vyplatila"), (3, "S čím pracovat")):
    tf = ph[idx].text_frame
    tf.text = txt
    tf.paragraphs[0].runs[0].font.size = Pt(22)
    tf.paragraphs[0].runs[0].font.bold = True
left = [
    "Za měsíc: Nasdaq 100 −9 %, PX +0,8 %, americké a německé dluhopisy zdražily",
    "Kdo sázel na jedno téma, ztratil nejvíc",
    "Časovat trh nejde: 6. 10. rekord, o měsíc později korekce",
    "Výkyvy k investování patří: investovat dál a pravidelně",
]
right = [
    "Naše široce diverzifikovaná portfolia: varianty podle rizika a horizontu",
    "Nově WOOD PX ETF: index pražské burzy PX jedním nákupem, v korunách",
    "PX se pohybuje jinak než světové akcie, ne vždy ale lépe (3 měsíce v CZK: PX −2,6 %, S&P 500 +4,2 %)",
    "ČEZ a finanční firmy tvoří téměř 90 % indexu: doplněk v přiměřené váze",
]
for idx, items in ((2, left), (4, right)):
    p_ = ph[idx]
    p_.left, p_.top, p_.width, p_.height = (Inches(0.92) if idx == 2 else Inches(6.75)), Inches(2.74), (Inches(5.64) if idx == 2 else Inches(5.67)), Inches(3.6)
    tf = p_.text_frame
    tf.clear()
    fill_paragraphs(tf, items, 18, bullets=False, space=10)
    bp = tf._txBody.find(qn("a:bodyPr"))
    for child in list(bp):
        bp.remove(child)
    etree.SubElement(bp, qn("a:normAutofit"))
source(s, "Nejde o investiční doporučení. Hodnota investice může kolísat, minulá výkonnost není zárukou budoucích výnosů. "
          "Data: Trading Economics k 2. 11. 2026.", y=6.6)

prs.save(OUT)
print("uloženo", OUT, "slajdů:", len(prs.slides))

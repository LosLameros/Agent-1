"""Prezentace Ekonomika a trhy – listopad 2026 v šabloně WOOD & Company.

Použití: python3 build_wood.py <šablona.pptx> <složka data> <výstup.pptx>
"""
import copy
import csv
import datetime as dt
import math
import sys

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import (XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_MARKER_STYLE,
                             XL_TICK_LABEL_POSITION, XL_TICK_MARK)
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

TPL, DATA, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

RED = RGBColor(0xEE, 0x4F, 0x46)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xC1, 0xCB, 0xCB)
MID = RGBColor(0x85, 0x99, 0x9A)
LINE = RGBColor(0x5B, 0x77, 0x78)
GRID = RGBColor(0x2E, 0x56, 0x58)
ROW_A = RGBColor(0x17, 0x46, 0x47)
ROW_B = RGBColor(0x0F, 0x37, 0x38)
BOLD_FONT = "Atyp Wood Bold"

L, W = 0.41, 12.52   # okraje obsahu podle layoutu šablony

prs = Presentation(TPL)
LAY = {l.name: l for l in prs.slide_layouts}

# červená šipka (SVG) ze vzorového slajdu šablony
src = prs.slides[0]
caret_pic = None
for sh in src.shapes:
    if sh.shape_type == 13 and "Caret" in (sh._element.nvPicPr.cNvPr.get("descr") or ""):
        caret_pic = sh._element
        break
svg_rid = caret_pic.find(".//{http://schemas.microsoft.com/office/drawing/2016/SVG/main}svgBlip").get(qn("r:embed"))
caret_part = src.part.related_part(svg_rid)

# smazat vzorové slajdy šablony
lst = prs.slides._sldIdLst
for sid in list(lst):
    prs.part.drop_rel(sid.rId)
    lst.remove(sid)


# ---------------------------------------------------------------- pomocné funkce
def remove_placeholder(s, idx):
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == idx:
            ph._element.getparent().remove(ph._element)


def content_slide(title, subtitle):
    s = prs.slides.add_slide(LAY["1_Title and Content"])
    t = s.shapes.title
    t.text = title
    t.text_frame.paragraphs[0].runs[0].font.size = Pt(30)
    for ph in s.placeholders:
        if ph.placeholder_format.idx == 15:
            ph.text = subtitle
    remove_placeholder(s, 16)
    return s


def run_fmt(r, size, bold=False, color=WHITE):
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.color.rgb = color
    if bold:
        r.font.name = BOLD_FONT


def textbox(s, x, y, w, h, paras, size, color=WHITE, align=None, anchor=MSO_ANCHOR.TOP, space=4, name=None, margin=0):
    """paras: list of str or list of (text, bold[, color]) runs."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(margin)
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        runs = [(para, False)] if isinstance(para, str) else para
        for run in runs:
            text, bold = run[0], run[1]
            col = run[2] if len(run) > 2 else color
            r = p.add_run()
            r.text = nb(text)
            run_fmt(r, size, bold, col)
        p.space_after = Pt(space)
        if align is not None:
            p.alignment = align
    return tb


def caret(s, x, y, size=0.36):
    el = copy.deepcopy(caret_pic)
    rid = s.part.relate_to(caret_part, RT.IMAGE)
    el.find(".//{http://schemas.microsoft.com/office/drawing/2016/SVG/main}svgBlip").set(qn("r:embed"), rid)
    off = el.find(".//" + qn("a:off"))
    ext = el.find(".//" + qn("a:ext"))
    off.set("x", str(Inches(x)))
    off.set("y", str(Inches(y)))
    ext.set("cx", str(Inches(size)))
    ext.set("cy", str(Inches(size)))
    cnv = el.find(".//" + qn("p:cNvPr"))
    cnv.set("id", str(1000 + len(s.shapes._spTree)))
    s.shapes._spTree.append(el)


def est_lines(text, width_in, size):
    cpl = max(10, int(width_in * 72 / (size * 0.52)))
    return max(1, math.ceil(len(text) / cpl))


CARET_PNG = sys.argv[4] if len(sys.argv) > 4 else "caret.png"


def nb(t):
    return t.replace(" %", "\u00a0%").replace(" USD", "\u00a0USD").replace(" bb", "\u00a0bb")


def caret_list(s, x, y, w, items, size=15, gap=0.16, max_y=6.3):
    """Odrážky s červenou šipkou ze šablony (obrázková odrážka), jedno textové pole na sloupec."""
    _, rid = s.part.get_or_add_image_part(CARET_PNG)
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(max_y - y))
    tb.name = "Odrážky"
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, it in enumerate(items):
        runs = [(it, False)] if isinstance(it, str) else it
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        for run in runs:
            r = p.add_run()
            r.text = nb(run[0])
            run_fmt(r, size, run[1], run[2] if len(run) > 2 else WHITE)
        p.space_after = Pt(gap * 72)
        p.line_spacing = 1.05
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(Inches(0.42)))
        pPr.set("indent", str(-Inches(0.42)))
        sz = etree.SubElement(pPr, qn("a:buSzPct"))
        sz.set("val", "140000")
        bb = etree.SubElement(pPr, qn("a:buBlip"))
        bl = etree.SubElement(bb, qn("a:blip"))
        bl.set(qn("r:embed"), rid)
    return tb


def header(s, x, y, w, text, size=16):
    return textbox(s, x, y, w, 0.35, [[(text, True, RED)]], size, name="Mezititulek")


def meaning(s, text, y=6.4, label="Co to znamená: "):
    return textbox(s, L, y, W, 0.45, [[(label, True, RED), (text, False)]], 14, name="Co to znamená")


def source(s, text, y=7.0):
    return textbox(s, L, y, W, 0.3, [text], 9, color=LIGHT, name="Zdroj")


def dark_chart(ch, size=11):
    ch.font.size = Pt(size)
    ch.font.color.rgb = WHITE


def chart_title(ch, text, size=13):
    ch.has_title = True
    ch.chart_title.text_frame.text = text
    r = ch.chart_title.text_frame.paragraphs[0].runs[0]
    run_fmt(r, size, True, WHITE)


def set_borders(cell, color=LINE, w=9525):
    tcPr = cell._tc.get_or_add_tcPr()
    for i, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        old = tcPr.find(qn(tag))
        if old is not None:
            tcPr.remove(old)
        ln = etree.Element(qn(tag), w=str(w))
        sf = etree.SubElement(ln, qn("a:solidFill"))
        etree.SubElement(sf, qn("a:srgbClr"), val=str(color))
        tcPr.insert(i, ln)


def table(s, x, y, colw, rowh, data, size, head_fill=RED, first_col_bold=True, fills=None):
    shp = s.shapes.add_table(len(data), len(colw), Inches(x), Inches(y), Inches(sum(colw)), Inches(sum(rowh)))
    t = shp.table
    t.first_row = True
    t.horz_banding = False
    for i, w_ in enumerate(colw):
        t.columns[i].width = Inches(w_)
    for i, h_ in enumerate(rowh):
        t.rows[i].height = Inches(h_)
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.fill.solid()
            if fills:
                cell.fill.fore_color.rgb = fills(r, c)
            else:
                cell.fill.fore_color.rgb = head_fill if r == 0 else (ROW_A if r % 2 else ROW_B)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            rr = p.add_run()
            rr.text = nb(val)
            run_fmt(rr, size, r == 0 or (first_col_bold and c == 0), WHITE)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.margin_left = cell.margin_right = Inches(0.12)
            cell.margin_top = cell.margin_bottom = Inches(0.05)
            set_borders(cell)
    return shp


def red_box(s, x, y, w, h, title, text):
    b = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    b.adjustments[0] = 0.11
    b.fill.solid()
    b.fill.fore_color.rgb = RED
    b.line.color.rgb = LINE
    b.line.width = Pt(0.6)
    b.shadow.inherit = False
    tf = b.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.16)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = title
    run_fmt(r, 15, True)
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
    r2 = p2.add_run()
    r2.text = nb(text)
    run_fmt(r2, 13)
    return b


# ---------------------------------------------------------------- data
perf = list(csv.DictReader(open(f"{DATA}/vykonnost-trhu.csv")))
brent = [(dt.date.fromisoformat(r["datum"]), float(r["brent_usd"])) for r in csv.DictReader(open(f"{DATA}/brent-2026.csv"))]
yields = [r for r in csv.DictReader(open(f"{DATA}/vynosy-10y.csv")) if r["zeme"] != "Česko"]
PCT = '+0.0"\u00a0%";"−"0.0"\u00a0%";0.0"\u00a0%"'
BP = '+0"\u00a0bb";"−"0"\u00a0bb";0"\u00a0bb"'

# ================================================================ 1 Titulní
s = prs.slides.add_slide(LAY["Title Slide"])
s.shapes.title.text = "Ekonomika a trhy"
for ph in list(s.placeholders):
    idx = ph.placeholder_format.idx
    if idx == 1:
        ph.text = "Listopad 2026"
        ph.text_frame.paragraphs[0].runs[0].font.size = Pt(14)
    elif idx == 10:
        ph._element.getparent().remove(ph._element)

# ================================================================ 2 Časová osa
s = content_slide("Co se stalo od začátku října", "Měsíc rekordů, výprodeje technologií a nadějí na mír")
events = [
    ("6. 10.", "Americké akcie na historickém maximu", False),
    ("23. 10.", "Ropa Brent nejdražší za čtyři roky", False),
    ("28.–29. 10.", "Fed a ECB nechaly sazby beze změny", False),
    ("28.–30. 10.", "Výsledky tech gigantů, výprodej technologií", False),
    ("2. 11.", "Naděje na dohodu USA a Íránu, ropa zlevnila", False),
    ("3. 11.", "Volby do Kongresu USA, nový úder na Írán", False),
    ("17. 11.", "Nvidia uzavře výsledkovou sezónu 3Q (zatím 82 % firem nad odhady)", True),
]
y_line = 3.55
x0, x1 = 1.25, 12.08
ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x0 - 0.45), Inches(y_line), Inches(x1 + 0.45), Inches(y_line))
ln.line.color.rgb = LIGHT
ln.line.width = Pt(1.5)
step = (x1 - x0) / (len(events) - 1)
for i, (d, txt, future) in enumerate(events):
    cx = x0 + i * step
    r = 0.13
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - r), Inches(y_line - r), Inches(2 * r), Inches(2 * r))
    dot.shadow.inherit = False
    dot.fill.solid()
    dot.fill.fore_color.rgb = ROW_B if future else RED
    dot.line.color.rgb = RED
    dot.line.width = Pt(2)
    bw = 1.7
    textbox(s, cx - bw / 2, 2.6, bw, 0.6, [[(d, True, RED)]], 18, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM, name=f"Datum {i + 1}")
    textbox(s, cx - bw / 2, 3.85, bw, 1.9, [txt], 14, color=LIGHT if future else WHITE, align=PP_ALIGN.CENTER, name=f"Událost {i + 1}")
textbox(s, L, 6.15, W, 0.45, [[("Dnes: ", True, RED), ("trhy · energie · sazby · výsledky firem a technologie · dluhopisy · výhled", False)]],
        15, align=PP_ALIGN.CENTER, name="Osnova")

# ================================================================ 3 Výkonnost trhů
s = content_slide("USA rostou navzdory poklesu technologií",
                  "Výprodej zasáhl technologie a AI infrastrukturu, široký americký trh drží")


def perf_chart(x, w, title, kl, kc, vmin, vmax):
    cd = CategoryChartData()
    cd.categories = [r["index"] for r in perf]
    cd.add_series("v místní měně", [round(float(r[kl]), 1) for r in perf])
    cd.add_series("v korunách", [round(float(r[kc]), 1) for r in perf])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(x), Inches(1.75), Inches(w), Inches(4.5), cd)
    gf.name = title
    ch = gf.chart
    dark_chart(ch, 11)
    chart_title(ch, title, 13)
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(11)
    ch.legend.font.color.rgb = WHITE
    pl = ch.plots[0]
    pl.gap_width = 50
    pl.overlap = 0
    pl.has_data_labels = True
    dl = pl.data_labels
    dl.number_format = PCT
    dl.number_format_is_linked = False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size = Pt(10)
    dl.font.color.rgb = WHITE
    for ser, col in zip(pl.series, (MID, RED)):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = col
        ser.invert_if_negative = False
    ca = ch.category_axis
    ca.reverse_order = True
    ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    ca.major_tick_mark = XL_TICK_MARK.NONE
    ca.format.line.color.rgb = LINE
    ca.tick_labels.font.size = Pt(11)
    ca.tick_labels.font.color.rgb = WHITE
    va = ch.value_axis
    va.minimum_scale = vmin
    va.maximum_scale = vmax
    va.has_major_gridlines = False
    va.visible = False


cw = 4.1
perf_chart(L, cw, "Poslední měsíc", "1M_lokalne_%", "1M_CZK_%", -16, 8)
perf_chart(L + cw + 0.11, cw, "Poslední 3 měsíce", "3M_lokalne_%", "3M_CZK_%", -7, 9)
perf_chart(L + 2 * (cw + 0.11), cw, "Od začátku roku", "YTD_lokalne_%", "YTD_CZK_%", -16, 42)
meaning(s, "za měsíc kurz koruny skoro nehrál roli, od začátku roku dražší dolar výnos v korunách zvýšil.")
source(s, "Zdroj: Trading Economics, zavírací ceny k 2. 11. 2026 (měsíc od 2. 10., 3 měsíce od 31. 7., rok od 31. 12. 2025); přepočet do CZK kurzy ke stejným dnům. Nasdaq 100 = US100.")

# ================================================================ 4 Ropa
s = content_slide("Naděje na dohodu stáhly ropu ke 100 USD", "Ropa je ale pořád o 42 % dražší než před válkou")
cd = CategoryChartData()
cd.categories = [d for d, _ in brent]
cd.add_series("Brent (USD za barel)", [v for _, v in brent])
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(L), Inches(1.75), Inches(6.2), Inches(4.5), cd)
gf.name = "Ropa Brent 2026"
ch = gf.chart
dark_chart(ch, 11)
chart_title(ch, "Ropa Brent v roce 2026 (USD za barel)", 13)
ch.has_legend = False
ser = ch.plots[0].series[0]
ser.smooth = False
ser.format.line.color.rgb = RED
ser.format.line.width = Pt(2.25)
ser.marker.style = XL_MARKER_STYLE.NONE
dates = [d for d, _ in brent]
for d, txt, pos in ((dt.date(2026, 11, 3), "103 (3. 11.)", XL_LABEL_POSITION.BELOW),):
    pt = ser.points[dates.index(d)]
    pt.data_label.has_text_frame = True
    pt.data_label.text_frame.text = txt
    run_fmt(pt.data_label.text_frame.paragraphs[0].runs[0], 11, True)
    pt.data_label.position = pos
    pt.marker.style = XL_MARKER_STYLE.CIRCLE
    pt.marker.size = 7
    pt.marker.format.fill.solid()
    pt.marker.format.fill.fore_color.rgb = WHITE
    pt.marker.format.line.color.rgb = WHITE
va = ch.value_axis
va.minimum_scale = 50
va.maximum_scale = 130
va.major_unit = 20
va.has_major_gridlines = True
va.major_gridlines.format.line.color.rgb = GRID
va.format.line.fill.background()
va.tick_labels.font.color.rgb = LIGHT
ca = ch.category_axis
ca.tick_labels.number_format = '[$-405]mmm'
ca.tick_labels.number_format_is_linked = False
ca.tick_labels.font.color.rgb = LIGHT
ca.major_tick_mark = XL_TICK_MARK.NONE
ca.format.line.color.rgb = LINE
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
caret_list(s, 6.95, 1.85, 5.95, [
    [("Hormuz není zavřený, ale ani volný: ", True), ("tankery plují s doprovodem USA, Írán na ně dál útočí", False)],
    [("Teče jím asi 80 % předválečného objemu ", True), ("ropy a paliv (konec září), paliv samotných jen pětina", False)],
    [("Trump střídá hrozby s nabídkou jednání: ", True), ("2. 11. ropa za den −7,6 %, 3. 11. USA znovu udeřily na Írán", False)],
    [("Brent 103 USD proti 73 USD před válkou ", True), ("(+42 %)", False)],
    [("Plyn v Evropě minulý týden nad 100 EUR/MWh, ", True), ("poprvé od roku 2022", False)],
], size=14, gap=0.14)
meaning(s, "drahé energie drží inflaci nahoře, Evropě hrozí dražší energie i v příštím roce.")
source(s, "Zdroj: Trading Economics (Brent: denní zavírací ceny, 3. 11. průběžná cena; plyn TTF), Kpler podle CNBC (toky přes Hormuz, 28. 9. 2026), hormuz.now")

# ================================================================ 5 Centrální banky
s = content_slide("Sazby: pauza, ne konec zvyšování", "Fed i ECB v říjnu čekaly, trh počítá s dalším zvýšením")
data = [
    ["Banka", "Poslední rozhodnutí", "Co dál"],
    ["Fed (USA)", "28. 10.: beze změny, 3,75–4,00 %", "Trh čeká zvýšení 9. 12. Inflace drží nahoře, ekonomika roste."],
    ["ECB (eurozóna)", "29. 10.: beze změny, 2,50 %", "O zvýšení se jednalo, trh s ním dál počítá. Lagardeová odejde z čela ECB předčasně."],
    ["ČNB", "drží 3,75 %", "5. 11. analytici čekají zvýšení na 4,00 %. Inflace v září 2,5 %, zdražují hlavně služby."],
]
table(s, L, 1.85, [2.6, 3.9, 6.02], [0.6, 1.1, 1.1, 1.1], data, 16)
meaning(s, "sazby spíš ještě porostou. Vyšší úroky z vkladů a nových dluhopisů, tlak na drahé akcie.")
source(s, "Zdroj: Fed, ECB, ČNB, Trading Economics, ČTK (odhady analytiků), k 3. 11. 2026")

# ================================================================ 6 Výsledková sezóna a technologie
s = content_slide("Zisky rostou, trh trestá sázky na AI", "Výsledková sezóna 3Q: 82 % firem nad odhady, zisky +30 %")
colw = 6.0
header(s, L, 1.8, colw, "Výsledková sezóna v USA")
caret_list(s, L + 0.05, 2.3, colw, [
    "Výsledky zveřejnilo 60 % firem z S&P 500 (k 30. 10.)",
    "82 % překonalo odhady zisků, dlouhodobý průměr je 78 %",
    "Zisky rostou o 30 %, už třetí čtvrtletí v řadě přes 25 %",
    "Firmy ale odhady překonávají o méně než dřív, trh je vybíravější",
], size=15)
x2 = L + colw + 0.5
header(s, x2, 1.8, colw, "Proč klesaly technologie")
caret_list(s, x2 + 0.05, 2.3, colw, [
    "Firmy utrácejí za AI a datová centra víc, než trh čekal",
    "Tech gigantům dochází volný cash flow: Alphabet, Amazon a Meta jsou v minusu, Microsoftu klesl o víc než čtvrtinu",
    "Investoři pochybují, kdy se investice vrátí, část firem si na ně půjčuje",
    "Výprodej se přelil i do Asie",
], size=15)
meaning(s, "nejde o krach firem, ale o přecenění očekávání. Zbytek trhu přitom držel.")
source(s, "Zdroj: FactSet Earnings Insight (30. 10. 2026), výsledky firem za 3Q 2026, Trading Economics")

# ================================================================ 7 Dluhopisy
s = content_slide("Dluhopisy tlumily pokles akcií", "Výnosy klesají z nejvyšších úrovní od roku 2007")
cd = CategoryChartData()
cd.categories = [f"{r['zeme']} ({float(r['vynos_10y_2026-11-03_%']):.2f} %)".replace(".", ",") for r in yields]
cd.add_series("Změna za měsíc (bb)", [int(r["zmena_bb"]) for r in yields])
gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(L), Inches(1.75), Inches(5.6), Inches(4.5), cd)
gf.name = "Změna výnosů 10Y"
ch = gf.chart
dark_chart(ch, 11)
chart_title(ch, "Změna výnosu 10letých dluhopisů za měsíc", 13)
ch.has_legend = False
pl = ch.plots[0]
pl.gap_width = 70
pl.has_data_labels = True
pl.data_labels.number_format = BP
pl.data_labels.number_format_is_linked = False
pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
pl.data_labels.font.size = Pt(12)
pl.data_labels.font.color.rgb = WHITE
ser = pl.series[0]
ser.invert_if_negative = False
ser.format.fill.solid()
ser.format.fill.fore_color.rgb = LIGHT
for i, r in enumerate(yields):
    if int(r["zmena_bb"]) > 0:
        p_ = ser.points[i]
        p_.format.fill.solid()
        p_.format.fill.fore_color.rgb = RED
ca = ch.category_axis
ca.reverse_order = True
ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
ca.major_tick_mark = XL_TICK_MARK.NONE
ca.format.line.color.rgb = LINE
ca.tick_labels.font.size = Pt(12)
ca.tick_labels.font.color.rgb = WHITE
va = ch.value_axis
va.minimum_scale = -50
va.maximum_scale = 20
va.has_major_gridlines = False
va.visible = False
caret_list(s, 6.35, 1.85, 6.55, [
    [("Dluhopisy byly dlouho otloukánkem: ", True), ("výnosy rostly kvůli drahé ropě a inflaci, zvyšování sazeb a obavám z deficitů", False)],
    [("V říjnu se to otočilo: ", True), ("investoři utíkali z technologií do bezpečí, 10letý výnos USA klesl z 5,31 % na 4,96 %", False)],
    [("Francie je výjimka: ", True), ("příplatek proti Německu nejvyšší od roku 2012, Itálie a Německo bez nákazy", False)],
    [("Hraje to do karet konzervativním portfoliím", True)],
], size=15)
meaning(s, "dluhopisy znovu fungují jako polštář a zároveň nesou slušný příjem.")
source(s, "Zdroj: Trading Economics, výnosy 10letých státních dluhopisů k 3. 11. 2026 proti stavu před měsícem; v závorce výnos; bb = setina procentního bodu; maximum USA 5,31 % (5. 10. 2026)")

# ================================================================ 8 Shrnutí
s = content_slide("Shrnutí: kde jsou trhy teď", "Krátkodobě nervózní trhy, firmy ale dál vydělávají")
caret_list(s, L + 0.1, 1.9, 12.2, [
    [("Energie: ", True), ("ropa zlevnila ke 100 USD, je ale dál dražší než před válkou; spor USA a Íránu kolísá mezi jednáním a údery", False)],
    [("Inflace a sazby: ", True), ("energie drží inflaci nahoře, centrální banky spíš ještě zvýší", False)],
    [("Akcie: ", True), ("zisky rostou kolem 30 %, trh ale trestá drahé sázky na AI, zbytek trhu drží", False)],
    [("Dluhopisy: ", True), ("výnosy klesají z nejvyšších úrovní od roku 2007, dluhopisy zdražují a dál nesou slušný příjem", False)],
    [("Evropa: ", True), ("hlavní rizika jsou drahé energie a Francie", False)],
    [("Volby v USA: ", True), ("krátkodobý šum; od roku 1950 byl S&P 500 rok po volbách do Kongresu vždy výš", False)],
], size=19, gap=0.24)
source(s, "Zdroj: Trading Economics, FactSet, centrální banky; historie voleb: U.S. Bank, BNY. Minulý vývoj není zárukou budoucího.")

# ================================================================ 9 Výhled
s = content_slide("Výhled: pokles technologií je dočasný", "Pro pasivního investora rozhodují zisky firem, ne denní zprávy")
header(s, L, 1.8, 6.6, "Proč zůstáváme optimističtí")
caret_list(s, L + 0.05, 2.3, 6.6, [
    [("Cloud zrychluje: ", True), ("Microsoft Azure +48 %, Amazon AWS +39 %, zakázky nasmlouvané na roky dopředu", False)],
    [("Zisky rostou kolem 30 %, ", True), ("analytici čekají podobné tempo i ve 4. čtvrtletí", False)],
    [("Akcie nejsou drahé: ", True), ("ocenění je pod průměrem posledních 10 let", False)],
    [("Dluhopisy ", True), ("znovu nesou slušný výnos a tlumí výkyvy akcií", False)],
    [("Pasivní investor drží celý trh: ", True), ("nemusí hádat vítěze ani správný okamžik", False)],
], size=15, gap=0.16)
xb = 7.45
header(s, xb, 1.8, 5.4, "Co bude důležité")
items = [
    ("Hormuz", "Dohoda by rychle zlevnila energie, nové útoky by je zdražily"),
    ("Proinflační rizika", "Dražší energie se v Evropě propíšou do cen v příštím roce"),
    ("Riziko vyšších sazeb", "Fed, ECB i ČNB mohou ještě přitlačit"),
    ("Francie", "Dluhopisy jako riziko výprodeje evropských aktiv"),
]
for i, (t_, tx) in enumerate(items):
    red_box(s, xb, 2.3 + i * 0.98, 5.45, 0.84, t_, tx)
source(s, "Zdroj: výsledky Microsoftu a Amazonu za 3Q 2026, FactSet Earnings Insight (30. 10. 2026). Nejde o investiční doporučení.")

# ================================================================ 10 Závěr
s = content_slide("Co z toho plyne pro investory", "Investovat dál, široce rozloženě a s rozmyslem")
header(s, L, 1.8, 6.0, "Diverzifikace se vyplatila")
caret_list(s, L + 0.05, 2.3, 6.0, [
    "Za měsíc Nasdaq 100 −9 %, PX +0,8 %, dluhopisy zdražily",
    "Kdo vsadil vše na technologie, nemá teď v portfoliu hezký pohled. Dlouhodobě jim ale věříme",
    "Časovat trh je těžké, v době Trumpa, drahé ropy a geopolitiky obzvlášť",
    "Výkyvy k investování patří a poslední krize byly krátké: po začátku války s Íránem byl S&P 500 dva týdny ode dna zpět nad předválečnou úrovní",
], size=16, gap=0.18)
x2 = L + 6.5
header(s, x2, 1.8, 6.0, "S čím pracovat")
caret_list(s, x2 + 0.05, 2.3, 6.0, [
    [("Naše široce diverzifikovaná ETF portfolia: ", True), ("konzervativní, vyvážené, dynamické a další varianty podle rizika a horizontu", False)],
    [("Nebát se diverzifikovat i mimo světové trhy, třeba do Prahy s WOOD PX ETF: ", True),
     ("bez měnového rizika, firmy, které klienti znají, silný výkon (PX za 5 let skoro +100 %)", False)],
    [("Myslet na koncentraci: ", True), ("česká burza je malá, proto jako doplněk v přiměřené váze", False)],
], size=16, gap=0.18)
source(s, "Nejde o investiční doporučení. Hodnota investice může kolísat, minulá výkonnost není zárukou budoucích výnosů. "
          "Data: Trading Economics k 2. 11. 2026 (PX bez dividend, 2. 11. 2021 – 2. 11. 2026).")

prs.save(OUT)
print("uloženo", OUT, "slajdů:", len(prs.slides))

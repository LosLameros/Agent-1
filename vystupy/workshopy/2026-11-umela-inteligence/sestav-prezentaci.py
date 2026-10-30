"""Doplní obsah workshopu AI do šablony Portu.

Postup (skill pptx):
1. Z podklady/workshopy/sablona/sablona-workshop.pptx zduplikovat slajdy 14, 22 a 13 (add_slide.py),
   v ppt/presentation.xml nechat pořadí 2, 23, 15, 19, 13, 14, 20, 24, 40, 56, 35, 57, 22, 58, 25, 36, 44, 45, 48, 52,
   spustit clean.py a zabalit jako stage3.pptx.
2. python3 -I sestav-prezentaci.py stage3.pptx "AI jako váš investiční asistent - workshop.pptx"
   (fotky řečníků ve složce foto/ ze staré prezentace, slajd 2).
"""
import copy, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.oxml.ns import qn

SRC, OUT = sys.argv[1], sys.argv[2]
FOTO = 'foto/'
FOOTER = 'AI jako váš investiční asistent  ·  listopad 2026'

prs = Presentation(SRC)
S = list(prs.slides)


def sh(slide, sid):
    for s in slide.shapes:
        if s.shape_id == sid:
            return s
    raise KeyError(sid)


def delete(slide, *ids):
    for i in ids:
        e = sh(slide, i)._element
        e.getparent().remove(e)


def set_runs(p, texts):
    """Keep paragraph formatting, map texts onto existing runs (first run formatting reused)."""
    runs = p.findall(qn('a:r'))
    if isinstance(texts, str):
        texts = [texts]
    while len(runs) < len(texts):
        new = copy.deepcopy(runs[-1])
        runs[-1].addnext(new)
        runs.append(new)
    for r, t in zip(runs, texts):
        r.find(qn('a:t')).text = t
    for r in runs[len(texts):]:
        p.remove(r)


def fill(slide, sid, paras, tmpl=None):
    """paras: list of paragraph specs (str or list of run strings). tmpl: index of template paragraph per new paragraph."""
    s = sh(slide, sid)
    body = s.text_frame._txBody
    ps = body.findall(qn('a:p'))
    out = []
    for i, spec in enumerate(paras):
        src = ps[min(i, len(ps) - 1)] if tmpl is None else ps[tmpl[i]]
        p = copy.deepcopy(src)
        set_runs(p, spec)
        out.append(p)
    for p in ps:
        body.remove(p)
    for p in out:
        body.append(p)
    return s


def run_style(slide, sid, para_idx, run_idx=0, bold=None, color=None):
    s = sh(slide, sid)
    r = s.text_frame.paragraphs[para_idx].runs[run_idx]
    if bold is not None:
        r.font.bold = bold
    if color is not None:
        r.font.color.theme_color = color


def materialize(s):
    l, t, w, h = s.left, s.top, s.width, s.height
    s.left, s.top, s.width, s.height = l, t, w, h


def geom(slide, sid, x=None, y=None, w=None, h=None):
    s = sh(slide, sid)
    materialize(s)
    if x is not None: s.left = Inches(x)
    if y is not None: s.top = Inches(y)
    if w is not None: s.width = Inches(w)
    if h is not None: s.height = Inches(h)
    return s


def move(slide, ids, dx=0, dy=0):
    for i in ids:
        s = sh(slide, i)
        materialize(s)
        s.left = s.left + Inches(dx)
        s.top = s.top + Inches(dy)


def clone_text(slide, sid, x, y, w, h, paras, name):
    """Copy an existing text shape (keeps its fonts/colors), place it and fill it."""
    src = sh(slide, sid)._element
    new = copy.deepcopy(src)
    src.addnext(new)
    ids = [s.shape_id for s in slide.shapes]
    new.find('.//' + qn('p:cNvPr')).set('id', str(max(ids) + 1))
    new.find('.//' + qn('p:cNvPr')).set('name', name)
    ph = new.find('.//' + qn('p:ph'))
    if ph is not None:
        ph.getparent().remove(ph)
    shape = [s for s in slide.shapes if s._element is new][0]
    shape.left, shape.top, shape.width, shape.height = Inches(x), Inches(y), Inches(w), Inches(h)
    fill(slide, shape.shape_id, paras)
    return shape


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def footer(slide):
    for s in slide.shapes:
        if s.name == 'Patička':
            fill(slide, s.shape_id, [FOOTER])
        if s.name == 'Štítek' and s.has_text_frame and s.top < Inches(3):
            n = len(s.text_frame.text)
            need = Inches(0.11 * n + 0.35)
            if s.width < need:
                materialize(s)
                s.width = need


from PIL import ImageFont
from pptx.enum.text import PP_ALIGN
_FONT = ImageFont.truetype('/home/user/Agent-1/nastroje/fonty/RethinkSans-SemiBold.ttf', 1000)


def text_width_in(shape):
    """Width of the pill text in inches (caps, size and letter spacing from the run)."""
    r = shape.text_frame.paragraphs[0].runs[0]._r
    rpr = r.find(qn('a:rPr'))
    sz = int(rpr.get('sz', '1000')) / 100
    spc = int(rpr.get('spc', '0')) / 100
    t = shape.text_frame.text
    if rpr.get('cap') == 'all':
        t = t.upper()
    pts = _FONT.getlength(t) / 1000 * sz + spc * len(t)
    return pts / 72


def fit_pill(shape, align='left', right=None):
    materialize(shape)
    bp = shape.text_frame._txBody.find(qn('a:bodyPr'))
    ins = (int(bp.get('lIns', '91440')) + int(bp.get('rIns', '91440'))) / 914400
    w = Inches(text_width_in(shape) + ins + 0.10)
    if align == 'center':
        shape.left = int((prs.slide_width - w) / 2)
    elif right is not None:
        shape.left = Inches(right) - w
    shape.width = w
    for p_ in shape.text_frame.paragraphs:
        p_.alignment = PP_ALIGN.CENTER


def pills():
    centred = {6, 14}            # slides whose label sits above a centred title
    for i, sl in enumerate(S):
        for x in sl.shapes:
            if x.name == 'Štítek' and x.has_text_frame and x.top < Inches(3) and x.left < Inches(9):
                fit_pill(x, 'center' if i in centred else 'left')
    tags = S[16]
    for sid in (9, 14, 19, 24):
        fit_pill(sh(tags, sid), right=12.5)


# ---------- 1 Titulní ----------
s = S[0]
fill(s, 3, ['WEBINÁŘ · INVESTIČNÍ KONZULTACE'])
fill(s, 4, ['AI jako váš investiční asistent'])
fill(s, 5, ['Co za vás zvládne a jak se jí ptát. Ukážeme naživo.'])
fill(s, 7, ['Marek Pokorný', 'Investiční konzultant a analytik'])
fill(s, 9, ['Marek Malina', 'Investiční konzultant a analytik'])
geom(s, 7, w=2.45)
geom(s, 9, x=4.79, w=2.45)
for sid, f, x in ((6, 'Obrázek_1.png', 0.83), (8, 'Obrázek_7.png', 4.15)):
    ph = sh(s, sid)
    l, t, w, h = ph.left, ph.top, ph.width, ph.height
    pic = ph.insert_picture(FOTO + f)
    pic.left, pic.top, pic.width, pic.height = Inches(x), t, w, h
delete(s, 10, 11)
fill(s, 13, ['listopad 2026'])
geom(s, 13, w=1.6)
notes(s, 'Každý řečník jedna věta o sobě: „Já AI používám hlavně na…“ (do 30 sekund). '
         'Moderátor napíše do chatu: dotazy jsou vítané kdykoli, pište je do chatu.')

# ---------- 2 Čísla ----------
s = S[1]
fill(s, 3, ['AI A PENÍZE'])
fill(s, 4, ['Ve světě se na peníze ptá AI už polovina lidí. V Česku zatím každý pátý.'])
geom(s, 4, h=1.2)
fill(s, 5, ['49 %', 'lidí ve světě použilo za posledních 6 měsíců AI při rozhodování o spoření a investicích'])
fill(s, 7, ['32 %', 'Čechů používá nástroje AI typu ChatGPT'])
fill(s, 9, ['19 %', 'Čechů využívá AI při správě svých financí'])
for i in (5, 7, 9):
    geom(s, i, h=1.6)
geom(s, 6, h=1.6)
geom(s, 8, h=1.6)
fill(s, 10, ['Zdroje: EY Global AI Sentiment Survey, duben 2026 (18 000+ lidí, 23 zemí); ČSÚ, šetření ICT v domácnostech 2025; Ipsos pro Zlatou korunu, Finance a AI 2025.'])
geom(s, 10, w=11.67)
notes(s, 'Nejdřív anketa v Teams: „Ptali jste se už AI na něco kolem peněz? Ano / ne / pravidelně.“ Pak odhalit čísla. '
         'Ústně: 18 % lidí ve světě používá AI na rozpočet a domácí finance (EY 2026). '
         'Přechod: „Dnes vám ukážeme, jak AI na peníze využít, s prompty, které si zkopírujete.“')

# ---------- 3 Tipy ----------
s = S[2]
fill(s, 3, ['JAK NA TO'])
fill(s, 4, ['6 tipů, jak se AI ptát, aby odpověď stála za to'])
tips = [
    ('Řekněte, kdo jste.', '„Je mi 40, investuju 5 000 Kč měsíčně, peníze budu potřebovat za 20 let.“'),
    ('Chtějte možnosti i protiargumenty.', '„Dej mi 3 varianty a ke každé, co by se mohlo pokazit.“'),
    ('Chtějte počty se vším.', '„Započítej inflaci a daně a napiš, s jakými předpoklady počítáš.“'),
    ('Chtějte zdroj a datum.', '„Ke každému číslu napiš, odkud je a k jakému datu.“'),
    ('Ať se zeptá ona vás.', '„Než odpovíš, zeptej se mě na všechno, co potřebuješ vědět.“'),
    ('Ať zkontroluje sama sebe.', '„Projdi svou odpověď a najdi v ní chyby.“'),
]
for (t, d), sid in zip(tips, (6, 8, 10, 12, 14, 16)):
    fill(s, sid, [t, d])
dy = 0.12
delete(s, 22)
fill(s, 18, ['BEZPEČNOST'])
fill(s, 19, ['Rodné číslo, čísla účtů a hesla do AI nedávejte',
             'V nastavení vypněte, aby se AI učila na vašich konverzacích',
             'Platí to i pro placené verze'])
fill(s, 21, ['Nastavení zabere', '2 minuty'])
geom(s, 17, h=3.2)
geom(s, 19, h=1.45)
move(s, (20, 21), dy=0.2)
notes(s, 'U tipu 2: AI ráda přitakává, proto chtějte i protiargumenty. '
         'Tipy 3 a 4: AI umí napsat přesvědčivé číslo, které neplatí. Proto předpoklady a zdroj s datem.')

# ---------- 4 Nástroje ----------
s = S[3]
fill(s, 3, ['NÁSTROJE'])
fill(s, 4, ['Který nástroj na co'])
fill(s, 5, ['ChatGPT', 'Počítání, tabulky a grafy', 'Práce s nahranými soubory'])
fill(s, 6, ['Claude', 'Dlouhé dokumenty', 'Projekty, které si pamatují vaše cíle'])
fill(s, 7, ['NotebookLM', 'Odpovídá jen z vašich dokumentů', 'Udělá z nich i podcast'])
fill(s, 8, ['Perplexity a Google Finance', 'Aktuální dění na trzích', 'Odkazy na zdroje'])
geom(s, 5, h=1.3); geom(s, 6, h=1.3)
geom(s, 7, y=3.45, h=1.3); geom(s, 8, y=3.45, h=1.3)
clone_text(s, 4, 0.83, 5.15, 11.67, 0.9,
           ['Největší výhoda pro českého investora: AI vám česky vysvětlí cokoli, co je jen v angličtině.'],
           'Hlavní sdělení')
nb = clone_text(s, 9, 0.83, 6.15, 8.0, 0.25, ['Na většinu věcí stačí verze zdarma.'], 'Poznámka')
from pptx.enum.text import PP_ALIGN
nb.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT
for r in nb.text_frame.paragraphs[0].runs:
    r.font.size = Pt(12)
notes(s, 'Řekněte na rovinu, co sami používáte nejčastěji. Přechod: „A teď to ukážeme naživo.“ Přepnout na sdílení obrazovky. '
         'Před workshopem ověřit, co je zdarma (Projekty v Claude a ChatGPT, NotebookLM) a jestli Google Finance s AI funguje česky.')

# ---------- 5 Předěl ----------
s = S[4]
fill(s, 4, ['01', 'Praktická část', 'Co za vás AI udělá. Ukážeme naživo.'])
notes(s, 'Každá další ukázka: prompt je na slajdu, ukážeme ho naživo. Záložní screenshot je připravený, kdyby nástroj nefungoval.')


def text_image(s, label, title, perex, prompt, items, note):
    fill(s, 3, [label])
    fill(s, 4, [title])
    fill(s, 5, [perex])
    geom(s, 5, h=0.6)
    fill(s, 6, [prompt])
    geom(s, 6, y=3.35, h=0.95)
    pairs = [(7, 8), (9, 10), (11, 12), (13, 14), (15, 16), (17, 18)]
    y = 4.55
    for (ic, tx), it in zip(pairs, items):
        fill(s, tx, [it])
        geom(s, ic, y=y + 0.01)
        geom(s, tx, y=y, h=0.3)
        y += 0.42
    for ic, tx in pairs[len(items):]:
        delete(s, ic, tx)
    notes(s, note)


# ---------- 6 Dokumenty ----------
text_image(S[5], '1 · DOKUMENTY', 'Přečte za vás 80 stran za minutu',
           'Výroční zprávy a dokumenty k fondům bývají dlouhé a anglicky. AI je shrne česky.',
           'Prompt: „Shrň mi tento dokument česky do 5 bodů pro člověka, který není odborník. Do čeho fond investuje, '
           'jak funguje a jaká jsou 3 největší rizika? U každého bodu uveď stranu.“',
           ['Doplňující otázka: „Co je P/E? Vysvětli to na pekárně.“',
            'Nástroj: Claude nebo ChatGPT',
            'Bonus: NotebookLM z dokumentu udělá krátký podcast'],
           'Živá ukázka na anglickém dokumentu k fondu (KID nebo měsíční přehled). Jedno číslo ze shrnutí ukázat přímo v dokumentu (tip 4 v praxi). '
           'Vpravo vložit záložní screenshot shrnutí. Češtinu podcastu v NotebookLM ověřit.')

# ---------- 7 Projekt ----------
s = S[6]
fill(s, 3, ['2 · VÁŠ PLÁN'])
fill(s, 4, ['Stejná otázka, mnohem lepší odpověď'])
fill(s, 6, ['S trvalými instrukcemi', 'S Projektem'])
fill(s, 7, ['Projekt si pamatuje vaše cíle. Pak se jen ptáte: Stihnu to? Co když přidám 1 000 Kč?'])
geom(s, 7, h=0.45)
for k, sid in enumerate((9, 11, 13, 15)):
    fill(s, sid, [['„Je mi 40 a investuju 5 000 Kč měsíčně.“',
                   '„Mám 300 000 Kč, cíl je 3 mil. Kč do 60 let.“',
                   '„Počítej s inflací a daněmi, piš předpoklady.“',
                   '„Zeptej se, co ti chybí. Nedoporučuj akcie.“'][k]])
move(s, (8, 9, 10, 11, 12, 13, 14, 15), dy=0.25)
fill(s, 17, ['Jedna věta zadání', 'Bez kontextu'])
fill(s, 18, ['„Navrhni mi investiční portfolio na 10 let a zdůvodni ho.“'])
geom(s, 18, h=0.45)
for k, sid in enumerate((20, 22, 24, 26)):
    fill(s, sid, [['AI neví, kolik vám je',
                   'Neví, kolik máte a kdy budete peníze potřebovat',
                   'Neví, jak snesete propad',
                   'Odpověď je proto obecná'][k]])
delete(s, 19, 21, 23, 25)
for sid in (20, 22, 24, 26):
    geom(s, sid, x=7.12)
move(s, (20, 22, 24, 26), dy=0.25)
A = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
B = [16, 17, 18, 20, 22, 24, 26, 27]
move(s, A, dx=5.95)
move(s, B, dx=-5.95)
notes(s, 'Vlevo: starý prompt ze slajdu 9, česky. Vpravo: Projekt „Moje investice“ s trvalými instrukcemi, pak doplňující otázky: '
         'Stihnu svůj cíl? Co když přidám 1 000 Kč měsíčně? Co když trh 2 roky klesá? '
         'Vysvětlit, co je Projekt („AI si pamatuje vaše cíle, nemusíte je psát znovu“). Výraz „system prompt“ nepoužívat. Klient je vymyšlený. '
         'Celé znění instrukce: Je mi 40, mám 300 000 Kč a investuju 5 000 Kč měsíčně. Cíl: 3 mil. Kč do 60 let. Propad o 30 % bych ustál, ale nerad. '
         'Počítej s inflací a daněmi, piš předpoklady a zeptej se, když ti něco chybí. Nedoporučuj mi konkrétní akcie.')

# ---------- 8 Rentgen ----------
s = S[7]
fill(s, 3, ['3 · PORTFOLIO'])
fill(s, 4, ['Rentgen vašeho portfolia'])
fill(s, 5, ['Tři různé fondy můžou být třikrát totéž. AI to odhalí za minutu.',
            'Prompt: „Mám ETF na MSCI World, S&P 500 a Nasdaq 100 a k tomu akcie Nvidie. Jak je moje portfolio rozložené podle regionů, sektorů a měn? Kolik mám celkem v 10 největších firmách? Kde se fondy překrývají?“',
            'Tip: místo „Je moje portfolio dobré?“ se ptejte „Kde je moje portfolio nejvíc zranitelné?“'])
geom(s, 5, y=3.3, h=2.9)
geom(s, 3, y=1.17); geom(s, 4, y=1.65)
s5 = sh(s, 5).text_frame.paragraphs
for p in s5[1:]:
    p.space_before = Pt(10)
fill(s, 7, [['40 ', '%'], 'tvoří 10 největších firem v indexu S&P 500', 'Kdo má tři „různé“ fondy, má často třikrát totéž.'])
notes(s, '30vteřinová ukázka: „Je moje portfolio dobré?“ (AI pochválí) vs. „Kde je moje portfolio nejvíc zranitelné?“ (užitečná odpověď). '
         'Číslo 40 % ověřit těsně před workshopem (podíl 10 největších firem v S&P 500). Rentgen hodnotí fakta, ne poradce. '
         'Doplňující dotaz (podnět kolegy): „Co se změní v rozložení mého portfolia, když přidám ETF X?“ Ptát se na regiony, sektory a měny, ne na výnos ani náklady. '
         'Přechod: „A teď si z toho necháme postavit vlastní přehled.“')


# ---------- 9 Vlastní nástroje ----------
s = S[8]
fill(s, 3, ['4 · VLASTNÍ NÁSTROJE'])
fill(s, 4, ['Postaví vám vlastní nástroj. Bez programování.'])
delete(s, 6, 18)
fill(s, 7, ['Kalkulačka na míru'])
geom(s, 7, y=2.42)
fill(s, 19, ['Přehled portfolia'])
geom(s, 19, y=2.42)
clone_text(s, 9, 1.17, 2.82, 5.0, 0.3, ['„Udělej mi kalkulačku na pravidelné investování.“'], 'Prompt A')
clone_text(s, 21, 7.36, 2.82, 5.0, 0.3, ['„Udělej mi z mých investic přehled s grafy.“'], 'Prompt B')
for x in s.shapes:
    if x.name in ('Prompt A', 'Prompt B'):
        for r in x.text_frame.paragraphs[0].runs:
            r.font.italic = True
            r.font.size = Pt(12)
for sid, t in zip((9, 11, 13, 15), ('Posuvníky pro vklad, počet let a zhodnocení',
                                   'Graf: kolik jsou vklady a kolik výnos',
                                   'Výsledek i v dnešních penězích po inflaci',
                                   'Uložíte si ji a použijete znovu')):
    fill(s, sid, [t])
for sid, t in zip((21, 23, 25, 27), ('Stačí seznam investic a částek',
                                    'Grafy podle regionů, sektorů a měn',
                                    '10 největších firem napříč fondy',
                                    'Příště jen přepíšete čísla')):
    fill(s, sid, [t])
move(s, (8, 9, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 24, 25, 26, 27), dy=0.1)
fill(s, 28, ['Claude, ChatGPT nebo Gemini vám ho postaví za minutu. Jeden výpočet si ověřte ručně a do přehledu dávejte jen názvy a částky.'])
sh(s, 7).click_action.hyperlink.address = 'kalkulacka-ukazka.html'
for x in s.shapes:
    if x.name == 'Prompt A':
        x.click_action.hyperlink.address = 'kalkulacka-ukazka.html'
# plus: replace text placeholder with a geometrically centred circle + plus sign
pl = sh(s, 16)
cx, cy, d = pl.left + pl.width // 2, pl.top + pl.height // 2, pl.width
pl._element.getparent().remove(pl._element)
from pptx.enum.shapes import MSO_SHAPE
circ = s.shapes.add_shape(MSO_SHAPE.OVAL, cx - d // 2, cy - d // 2, d, d)
circ.name = 'Plus – kruh'
circ.fill.solid(); circ.fill.fore_color.theme_color = MSO_THEME_COLOR.ACCENT_1
circ.line.fill.background(); circ.shadow.inherit = False
k = int(d * 0.5)
plus = s.shapes.add_shape(MSO_SHAPE.MATH_PLUS, cx - k // 2, cy - k // 2, k, k)
plus.name = 'Plus – znak'
plus.adjustments[0] = 0.16
plus.fill.solid(); plus.fill.fore_color.theme_color = MSO_THEME_COLOR.BACKGROUND_1
plus.line.fill.background(); plus.shadow.inherit = False
for shp in (circ, plus):
    st = shp._element.find(qn('p:style'))
    if st is not None:
        shp._element.remove(st)
notes(s, 'Podnět kolegy: AI jako tvůrce vlastních nástrojů. Živě v Claude (Artifacts), ChatGPT nebo Gemini (Canvas). '
         'Prompt A: „Udělej mi kalkulačku, kolik budu mít, když budu každý měsíc investovat určitou částku. Chci posuvníky pro počáteční vklad, měsíční vklad, počet let, roční zhodnocení a inflaci, graf vkladů a výnosu a výsledek i v dnešních penězích.“ '
         'Prompt B: „Z tohoto seznamu mých investic a částek mi udělej přehled s grafy podle regionů, sektorů a měn a s 10 největšími firmami napříč fondy.“ (vymyšlené portfolio, žádná čísla účtů) '
         'ZÁLOHA: klik na nadpis „Kalkulačka na míru“ otevře hotovou kalkulačku kalkulacka-ukazka.html v prohlížeči (soubor musí ležet ve stejné složce jako prezentace). '
         'Jeden výpočet ukázat ručně (tip 4).')

# ---------- 9b Zprávy ----------
text_image(S[9], '5 · ZPRÁVY', 'Zprávy z anglických webů česky za 2 minuty',
           'Místo hodiny na zpravodajských webech dvě minuty, a s odkazy na zdroje.',
           'Prompt: „Proč akcie X minulý týden klesly o 8 %? Odpověz česky a uveď zdroje.“',
           ['Nástroj: Perplexity nebo Google Finance s AI',
            'Každé tvrzení má odkaz, který si můžete ověřit'],
           'Vpravo vložit záložní screenshot odpovědi se zdroji. Pokud tlačí čas, projít rychle.')

# ---------- 10 Témata ----------
s = S[10]
fill(s, 3, ['6 · TÉMATA'])
fill(s, 4, ['Najde firmy k tématu, kterému věříte'])
fill(s, 5, ['ZEPTEJTE SE', 'Kdo vyrábí čipy?', '„Jaké firmy na burze vyrábějí čipy? Kolik tržeb z toho mají? A existuje ETF na celé téma?“'])
fill(s, 7, ['AI NAJDE', 'Firmy a souvislosti', 'Přehled firem, čím se liší a kolik vydělávají na čipech. Za minutu místo večera.'])
fill(s, 9, ['VY ROZHODNETE', 'Co s tím uděláte', 'Seznam je začátek rešerše, ne nákupní seznam. Rozhodnutí je vaše.'])
fill(s, 10, ['Často se ukáže, že téma jde koupit šířeji přes ETF.'])
notes(s, 'Živá ukázka promptu. Příklad s čipy navrhl odborník na AI. Zdůraznit: seznam od AI není tip na nákup.')

# ---------- 11 Pět akcií ----------
s = S[12]
fill(s, 3, ['TAKHLE NE'])
fill(s, 4, ['„Na kterých pěti akciích vydělám v příštích 5 letech nejvíc?“'])
geom(s, 4, w=11.67, h=1.15)
cards = [
    (6, 7, 8, 'ODPOVĚĎ 1', 'Sázka na čipy', ['TSMC', 'ASML', 'Broadcom', 'Vistra / Constellation', 'Micron']),
    (13, 14, 15, 'ODPOVĚĎ 2', 'Obranné jistoty', ['Microsoft', 'Berkshire Hathaway', 'Alphabet', 'JPMorgan', 'Johnson & Johnson']),
    (20, 21, 22, 'ODPOVĚĎ 3', 'Všechno do AI', ['Nvidia', 'TSMC', 'Broadcom', 'Meta', 'SK Hynix']),
]
for a, b, c, t1, t2, stocks in cards:
    fill(s, a, [t1]); fill(s, b, [t2]); fill(s, c, stocks)
    geom(s, c, h=1.35)
    for i, st in enumerate(stocks):
        if st in ('TSMC', 'Broadcom'):
            run_style(s, c, i, bold=True, color=MSO_THEME_COLOR.ACCENT_1)
delete(s, 9, 10, 16, 17, 23, 24)
clone_text(s, 4, 0.83, 5.55, 11.67, 0.8,
           ['Tři nástroje, tři různé odpovědi. AI není věštkyně, je to skvělý analytik. Tak se jí tak ptejte.'],
           'Pointa')
for x in s.shapes:
    if x.name == 'Pointa':
        for r in x.text_frame.paragraphs[0].runs:
            r.font.size = Pt(18)
notes(s, 'Nejdřív anketa: „Které akcie AI podle vás jmenuje?“ Pak odhalení. Zeleně: akcie, které se opakují (TSMC, Broadcom). '
         'Ústně: v pokusu Alpha Arena (Seznam Zprávy, květen 2026) obchodovalo 8 velkých AI modelů dva týdny a v zisku skončilo jen 6 z 32 výsledků. '
         'Odpověď na otázku, jestli AI portfoliu věřit: „Jako inspiraci ano, jako hotový plán ne. Každý nástroj odpoví jinak a vás nezná.“ '
         'Postřeh odborníka: když už o akcii píše AI, rychlý boom jste nejspíš propásli. '
         'Přechod: „Jak se tedy na firmy ptát? Ukážeme vám, jak to děláme my.“ '
         'PŘED WORKSHOPEM: odpovědi vygenerovat znovu (tyto jsou z léta 2026), místo „Odpověď 1–3“ napsat názvy nástrojů a doplnit datum.')


# ---------- Předěl 02 ----------
s = S[13]
fill(s, 4, ['02', 'Jak to děláme my', 'Jak se na firmy díváme my dva. Naživo, na skutečné firmě.'])
notes(s, 'Druhá část: náš osobní postup, ne oficiální postup Portu.')

# ---------- 12 Jak to děláme my ----------
s = S[14]
fill(s, 3, ['JAK TO DĚLÁME MY'])
geom(s, 3, x=5.6, w=2.13)
fill(s, 4, ['Analýza firmy ve čtyřech krocích'])
px = clone_text(s, 8, 0.6, 2.5, 12.13, 0.35, ['Náš osobní postup, když se chceme rychle zorientovat ve firmě.'], 'Perex')
for r in px.text_frame.paragraphs[0].runs:
    r.font.size = Pt(14)
steps = [(7, 8, 'Výsledky česky', 'Hodinový anglický hovor k výsledkům shrne AI za minutu česky.'),
         (10, 11, 'Očima Buffetta', 'Rozumím byznysu? Má firma trvalou výhodu? Je cena rozumná?'),
         (13, 14, 'Tři scénáře', 'Optimistický, střední a pesimistický. A co by se muselo stát.'),
         (16, 17, 'Ověříme a rozhodneme', 'Klíčová čísla zkontrolujeme v originále. Rozhodnutí je naše.')]
for t, d, tt, dd in steps:
    fill(s, t, [tt]); fill(s, d, [dd])
    geom(s, d, h=0.7)
notes(s, 'Krok 4 doplněn: čísla od AI ověřujeme v originále (tip 4). Mluvit za sebe („my dva“), ne za Portu. Celé naživo na jedné firmě, ideálně té, ke které jsme naposledy psali komentář k výsledkům. '
         'Přepis hovoru z veřejného webu firmy pro investory. '
         'Krok 2 stojí i na rámci analýz Morningstar (konkurenční výhoda, férová cena, nejistota); jejich placené analýzy do AI nenahráváme. DCF a porovnání ETF jsou na dalším slajdu. Prompty: '
         '1) „Tady je přepis hovoru k výsledkům. Shrň česky: co se firmě dařilo, co ne, co řekl management o výhledu a na co se ptali analytici.“ '
         '2) „Posuď tuto firmu, jak by ji posuzovali Warren Buffett a Charlie Munger: rozumím byznysu? Má trvalou konkurenční výhodu? Je management poctivý a schopný? Je cena rozumná? Nepřisuzuj jim žádné citáty.“ '
         '3) „Napiš optimistický, střední a pesimistický scénář pro tuto firmu na 3 roky. Ke každému napiš, co by se muselo stát, a jaké jsou hlavní předpoklady.“')

# ---------- 13 Na doma ----------
s = S[11]
fill(s, 3, ['7 · NA DOMA'])
fill(s, 4, ['AI jako váš osobní finanční asistent'])
cards = [
    (6, 7, 8, 'PROJEKT', 'Moje finance', 'Cíle, horizonty a přehled smluv na jednom místě. Na podmínky se zeptáte, místo hledání v šuplíku.'),
    (13, 14, 15, 'KONTROLA VÝDAJŮ', 'Kam mizí peníze', 'Výpis z banky jako tabulka, jen datum, popis a částka. „Kde jsem utratil víc, než jsem chtěl?“'),
    (20, 21, 22, 'NOVÝ CÍL', 'Zapadá do plánu?', '„Chci za 3 roky auto za 600 000 Kč. Jak to zapadá do mého plánu?“'),
]
for a, b, c, t1, t2, d in cards:
    fill(s, a, [t1]); fill(s, b, [t2]); fill(s, c, [d])
    geom(s, c, h=1.2)
delete(s, 9, 10, 16, 17, 23, 24)
for card in (5, 11, 12, 18, 19, 25):
    geom(s, card, h=2.1)
notes(s, 'Osobní postup odborníka na AI, kterého jsme se ptali. Citlivé údaje ve smlouvách a výpisech začernit nebo smazat.')

# ---------- 16 DCF a ETF ----------
s = S[15]
fill(s, 3, ['JAK TO DĚLÁME MY'])
fill(s, 4, ['DCF a porovnání ETF'])
fill(s, 5, ['Pokročilejší věci, které si od AI necháváme spočítat. S rozumem.',
            'DCF = odhad hodnoty firmy z peněz, které podle předpokladů vydělá v budoucnu.'])
geom(s, 3, y=2.2); geom(s, 4, y=2.69, h=0.85)
geom(s, 5, y=3.6, h=1.6)
for p_ in sh(s, 5).text_frame.paragraphs[1:]:
    p_.space_before = Pt(8)
fill(s, 7, ['Co nám AI ušetří'])
fill(s, 19, ['Na co si dát pozor'])
yes = ['DCF model firmy za pár minut', 'Dopad jiného růstu nebo sazby',
       'ETF: složení, regiony, měny', 'Překryv nového ETF s portfoliem',
       'Chování portfolia v minulosti']
no = ['DCF stojí na předpokladech', 'Není to cílová cena ani tip',
      'Minulost nezaručuje budoucnost']
for sid, t in zip((9, 11, 13, 15, 17), yes):
    fill(s, sid, [t]); geom(s, sid, w=3.0)
for sid, t in zip((21, 23, 25), no):
    fill(s, sid, [t]); geom(s, sid, w=3.0)
notes(s, 'Podnět kolegy. Disclaimery říct nahlas: DCF stojí na předpokladech (růst tržeb, marže, diskontní sazba, konečný růst); '
         'malá změna předpokladu udělá velkou změnu výsledku. Výsledek není cílová cena ani doporučení ke koupi či prodeji. '
         'U ETF: srovnání historie ukazuje minulost, ne budoucnost; simulace není předpověď. '
         'Prompt DCF: „Spočítej DCF pro firmu X. Vypiš všechny předpoklady (růst tržeb, marže, diskontní sazba, konečný růst) a ukaž, jak se výsledek změní, když každý posunu o 1 procentní bod. Neuváděj doporučení.“ '
         'Prompt ETF: „Porovnej ETF A a ETF B: co drží, regiony, sektory a měny, jak moc se překrývají s mým portfoliem a jak by se portfolio s každým z nich chovalo v minulosti. Neuváděj doporučení.“ '
         'Poplatky na slajdu záměrně nejsou.')

# ---------- 14 Dnes večer ----------
s = S[16]
fill(s, 3, ['SHRNUTÍ'])
fill(s, 4, ['Vyzkoušejte ještě dnes večer'])
fill(s, 5, ['Všechny prompty z dnešního webináře vám pošleme e-mailem.'])
rows = [(8, 9, 'Vypněte učení na svých datech', 'V nastavení soukromí ve vašem AI nástroji.', '2\u00a0MIN'),
        (13, 14, 'Nechte si shrnout dokument', 'Anglický dokument k vaší investici, česky do 5 bodů.', '5\u00a0MIN'),
        (18, 19, 'Rentgen a přehled portfolia', 'Překryvy fondů a vlastní přehled s grafy.', '10\u00a0MIN'),
        (23, 24, 'Založte si Projekt', 'S vašimi cíli, horizontem a pravidly.', '10\u00a0MIN')]
for t, tag, a, b, c in rows:
    fill(s, t, [a, b])
    geom(s, t, w=5.6)
    fill(s, tag, [c])
delete(s, 10, 15, 20, 25)
notes(s, 'Po webináři poslat e-mailem tahák na jednu stranu A4 se všemi prompty ze slajdů 3, 6, 7, 8, 9, 10 a 12.')

# ---------- 15 Q&A ----------
s = S[17]
for sid, q in zip((8, 12, 16, 20), ('Která AI je na investice nejlepší?', 'Potřebuju placenou verzi?',
                                    'Můžu AI dát přístup ke svému účtu?', 'Nahradí AI poradce?')):
    fill(s, sid, [q])
notes(s, 'Odpověď na otázku o účtu: „V USA už ano: ChatGPT umí číst bankovní účty a u brokera Robinhood můžete napojit AI agenta, který obchoduje. '
         'V Česku zatím ne, a my bychom AI peníze do ruky zatím nedávali.“ '
         'Placená verze: na většinu ukázaných věcí stačí verze zdarma, placená má víc dotazů a silnější modely.')

# ---------- 16, 17 ----------
notes(S[18], 'Jedna věta: „Za investiční rozhodnutí odpovídáte vy. Rádi vám s ním pomůžeme. Ozvěte se, když budete chtít výstup z AI probrat s člověkem.“')

for sl in S:
    footer(sl)
pills()

prs.save(OUT)
print('saved', OUT)

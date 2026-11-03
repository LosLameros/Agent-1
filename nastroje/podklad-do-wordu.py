"""Převede podklad v Markdownu do Wordu (.docx), který jde nahrát do Google Docs.

Umí: # a ## nadpisy, odrážky (i vnořené po 2 mezerách), **tučně**, *kurzívou*, tabulky |…|,
řádek **[GRAF n: …]** nahradí obrázkem z mapy GRAFY (číslo grafu → cesta k PNG).
Použití: python3 nastroje/podklad-do-wordu.py <vstup.md> <výstup.docx> [graf1.png graf2.png …]
"""
import re
import sys

from docx import Document
from docx.shared import Cm, Pt, RGBColor

FIALOVA = RGBColor(0x48, 0x40, 0xBB)


def runs(odstavec, text):
    for kus in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not kus:
            continue
        if kus.startswith("**"):
            odstavec.add_run(kus[2:-2]).bold = True
        elif kus.startswith("*"):
            odstavec.add_run(kus[1:-1]).italic = True
        else:
            odstavec.add_run(kus)


def main(vstup, vystup, grafy):
    doc = Document()
    styl = doc.styles["Normal"]
    styl.font.name = "Arial"
    styl.font.size = Pt(11)
    radky = open(vstup, encoding="utf-8").read().splitlines()
    i = 0
    while i < len(radky):
        r = radky[i].rstrip()
        if not r:
            i += 1
            continue
        if r.startswith("# "):
            h = doc.add_heading(r[2:], level=0)
        elif r.startswith("## "):
            h = doc.add_heading(r[3:], level=1)
            for run in h.runs:
                run.font.color.rgb = FIALOVA
        elif m := re.match(r"\*\*\[GRAF (\d+):", r):
            cesta = grafy[int(m.group(1)) - 1]
            doc.add_picture(cesta, width=Cm(16))
        elif r.startswith("|"):
            tab = []
            while i < len(radky) and radky[i].startswith("|"):
                bunky = [b.strip() for b in radky[i].strip("|").split("|")]
                if not all(re.fullmatch(r"-+", b) for b in bunky):
                    tab.append(bunky)
                i += 1
            t = doc.add_table(rows=len(tab), cols=len(tab[0]))
            t.style = "Table Grid"
            for ri, radek in enumerate(tab):
                for ci, text in enumerate(radek):
                    p = t.cell(ri, ci).paragraphs[0]
                    runs(p, f"**{text}**" if ri == 0 else text)
            continue
        elif m := re.match(r"( *)- (.*)", r):
            uroven = len(m.group(1)) // 2
            p = doc.add_paragraph(style="List Bullet" if uroven == 0 else "List Bullet 2")
            runs(p, m.group(2))
        else:
            runs(doc.add_paragraph(), r)
        i += 1
    doc.save(vystup)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3:])

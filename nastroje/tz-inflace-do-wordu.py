#!/usr/bin/env python3
"""Převede tiskovou zprávu o inflaci z Markdownu do Wordu v šabloně Portu.

Použití:
    python3 -I nastroje/tz-inflace-do-wordu.py <vstup.md> <vystup.docx> [--autor "Jméno Příjmení"] [--aum 76] [--sablona <sablona.docx>]

--aum = objem zainvestovaných peněz v miliardách Kč z portu.cz (zjistí ho `node nastroje/portu-aum.js`),
        doplní se do věty „pod správou má … miliard Kč“ v odstavci o Portu.

Šablona = poslední vydaná tisková zpráva (výchozí: abecedně poslední soubor
v examples/tiskove-zpravy-inflace/). Ze šablony zůstane hlavička „TISKOVÁ ZPRÁVA“,
nadpis, podpis s kontakty a odstavec „Portu je česká robo-advisory platforma…“.
Nahradí se datum a celé tělo zprávy, případně podpis jiného autora.

Formát Markdownu:
    (Praha, 12. 10. 2026)            <- řádek s datem
    **Tučný úvod** pokračování…      <- odstavce oddělené prázdným řádkem, **…** = tučně
    ## Inflace ve světě              <- mezititulek sekce
    # INTERNÍ ČÁST                   <- vše od tohoto řádku dál se do Wordu nepřevádí
"""
import copy
import glob
import os
import re
import sys

import docx
from docx.oxml.ns import qn

AUTORI = {
    "Marek Pokorný": {"telefon": "730 909 459", "email": "marek.pokorny"},
    "Lukáš Raška": {"telefon": "606 576 875", "email": "lukas.raska"},
}
VYCHOZI_AUTOR = "Marek Pokorný"


MESICE = ["leden", "únor", "březen", "duben", "květen", "červen",
          "červenec", "srpen", "září", "říjen", "listopad", "prosinec"]


def obdobi_sablony(cesta):
    """Období zprávy z názvu souboru: „TZ inflace - září 2026.docx“ nebo „2026-09-TZ-inflace.docx“."""
    nazev = os.path.basename(cesta).lower()
    m = re.search(r"(\d{4})-(\d{2})", nazev)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    m = re.search(r"(" + "|".join(MESICE) + r")\s+(\d{4})", nazev)
    if m:
        return (int(m.group(2)), MESICE.index(m.group(1)) + 1)
    return (0, 0)


def argument(nazev, vychozi=None):
    if nazev in sys.argv:
        return sys.argv[sys.argv.index(nazev) + 1]
    return vychozi


def nacti_md(cesta):
    text = open(cesta, encoding="utf-8").read()
    text = re.split(r"^# INTERNÍ", text, flags=re.M)[0]
    bloky = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    datum, telo = None, []
    for b in bloky:
        b = " ".join(radek.strip() for radek in b.splitlines())
        if b.startswith("# ") or b == "---":
            continue
        if datum is None and b.startswith("(Praha"):
            datum = b
            continue
        if b.startswith("## "):
            telo.append(("mezititulek", b[3:].strip()))
        else:
            telo.append(("odstavec", b))
    if datum is None:
        sys.exit("CHYBA: v Markdownu chybí řádek s datem „(Praha, D. M. RRRR)“")
    return datum, telo


def nastav_text_odstavce(p, text):
    """Nahradí text odstavce, formát převezme z prvního běhu."""
    runs = p._p.findall(qn("w:r"))
    prvni = runs[0]
    for r in runs[1:]:
        p._p.remove(r)
    for t in prvni.findall(qn("w:t")):
        prvni.remove(t)
    t = prvni.makeelement(qn("w:t"), {})
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    prvni.append(t)


def nahrad_v_odstavci(d, vzor, novy):
    """Nahradí text, který může být rozdělený do více běhů, a zachová formát prvního z nich."""
    for p in d.paragraphs:
        ts = list(p._p.iter(qn("w:t")))
        celek = "".join(t.text or "" for t in ts)
        m = re.search(vzor, celek)
        if not m:
            continue
        pozice = 0
        hotovo = False
        for t in ts:
            s = t.text or ""
            zac, kon = pozice, pozice + len(s)
            pozice = kon
            if kon <= m.start() or zac >= m.end():
                continue
            pred = s[: max(0, m.start() - zac)]
            za = s[max(0, m.end() - zac):] if kon > m.end() else ""
            t.text = pred + ("" if hotovo else novy) + za
            t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            hotovo = True
        return True
    sys.exit(f"CHYBA: v šabloně nenalezeno {vzor!r}")


def beh(vzor_rpr, text, tucne):
    r = docx.oxml.parse_xml(f'<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
    rpr = copy.deepcopy(vzor_rpr)
    for tag in ("w:b", "w:bCs"):
        for el in rpr.findall(qn(tag)):
            rpr.remove(el)
    if tucne:
        rpr.insert(0, rpr.makeelement(qn("w:bCs"), {}))
        rpr.insert(0, rpr.makeelement(qn("w:b"), {}))
    r.append(rpr)
    t = r.makeelement(qn("w:t"), {})
    t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
    r.append(t)
    return r


def odstavec(vzor_ppr, vzor_rpr, text):
    p = docx.oxml.parse_xml(f'<w:p xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
    p.append(copy.deepcopy(vzor_ppr))
    for i, kus in enumerate(re.split(r"\*\*", text)):
        if kus:
            p.append(beh(vzor_rpr, kus, tucne=(i % 2 == 1)))
    return p


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    md, out = sys.argv[1], sys.argv[2]
    koren = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sablony = sorted(glob.glob(os.path.join(koren, "examples", "tiskove-zpravy-inflace", "*.docx")), key=obdobi_sablony)
    sablona = argument("--sablona", sablony[-1] if sablony else None)
    autor = argument("--autor", VYCHOZI_AUTOR)
    if not sablona:
        sys.exit("CHYBA: chybí šablona (examples/tiskove-zpravy-inflace/*.docx)")
    if autor not in AUTORI:
        sys.exit(f"CHYBA: neznámý autor {autor!r}, doplň ho do AUTORI v {__file__}")

    datum, telo = nacti_md(md)
    d = docx.Document(sablona)
    ps = d.paragraphs

    # Kotvy v šabloně
    i_datum = next(i for i, p in enumerate(ps) if p.text.strip().startswith("(Praha"))
    i_svet = next(i for i, p in enumerate(ps) if p.text.strip() == "Inflace ve světě")
    i_podpis = next(i for i, p in enumerate(ps) if p.text.strip() == "analytik Portu") - 1
    puvodni_autor = ps[i_podpis].text.strip()
    if puvodni_autor not in AUTORI:
        sys.exit(f"CHYBA: v šabloně nepoznávám autora {puvodni_autor!r}")

    # Vzory formátu: běžný odstavec (první neprázdný po datu), mezititulek a prázdné řádky kolem něj
    i_vzor = next(i for i in range(i_datum + 1, i_svet) if ps[i].text.strip())
    vzor_ppr = ps[i_vzor]._p.find(qn("w:pPr"))
    vzor_rpr = next(r for r in ps[i_vzor]._p.iter(qn("w:r")) if r.find(qn("w:rPr")) is not None).find(qn("w:rPr"))
    prazdny_po_datu = copy.deepcopy(ps[i_datum + 1]._p)
    prazdny_bezny = copy.deepcopy(ps[i_svet - 1]._p)
    mezititulek = copy.deepcopy(ps[i_svet]._p)
    prazdny_po_mezititulku = copy.deepcopy(ps[i_svet + 1]._p)

    # Datum
    nastav_text_odstavce(ps[i_datum], datum)

    # Smaž staré tělo (od prázdného řádku po datu po prázdný řádek před podpisem)
    konec = i_podpis - 1  # prázdný odstavec před podpisem zůstává
    for p in ps[i_datum + 1:konec]:
        p._p.getparent().remove(p._p)

    # Vlož nové tělo
    kotva = ps[konec]._p
    nove = [copy.deepcopy(prazdny_po_datu)]
    for druh, text in telo:
        if druh == "mezititulek":
            m = copy.deepcopy(mezititulek)
            t = m.findall(".//" + qn("w:t"))
            t[0].text = text
            for navic in t[1:]:
                navic.text = ""
            nove += [copy.deepcopy(prazdny_bezny), m, copy.deepcopy(prazdny_po_mezititulku)]
        else:
            nove.append(odstavec(vzor_ppr, vzor_rpr, text))
    for el in nove:
        kotva.addprevious(el)

    # Podpis a kontakty
    if autor != puvodni_autor:
        stary, novy = AUTORI[puvodni_autor], AUTORI[autor]
        nahrady = {puvodni_autor: autor, stary["telefon"]: novy["telefon"], stary["email"]: novy["email"]}
        for t in d.element.body.iter(qn("w:t")):
            for a, b in nahrady.items():
                if t.text and a in t.text:
                    t.text = t.text.replace(a, b)
        for rel in d.part.rels.values():
            if rel.is_external and stary["email"] in rel.target_ref:
                rel._target = rel.target_ref.replace(stary["email"], novy["email"])
    # Pozice v podpisu: fialově a bez tučného, stejná velikost jako řádky s kontakty
    for t in d.element.body.iter(qn("w:t")):
        if t.text and t.text.strip() == "Financial Markets Analyst":
            rpr = t.getparent().find(qn("w:rPr"))
            for tag in ("w:b", "w:bCs", "w:sz", "w:szCs", "w:color"):
                for el in rpr.findall(qn(tag)):
                    rpr.remove(el)
            barva = rpr.makeelement(qn("w:color"), {qn("w:val"): "9646AA"})
            velikost = rpr.makeelement(qn("w:szCs"), {qn("w:val"): "18"})
            lang = rpr.find(qn("w:lang"))
            for el in (barva, velikost):
                if lang is not None:
                    lang.addprevious(el)
                else:
                    rpr.append(el)

    # Objem majetku pod správou z portu.cz (nastroje/portu-aum.js)
    aum = argument("--aum")
    if aum:
        nahrad_v_odstavci(d, r"pod správou má (přes )?\d+(,\d+)? miliard Kč", f"pod správou má {aum.replace('.', ',')} miliard Kč")
    else:
        print("POZOR: bez --aum zůstává objem majetku pod správou ze šablony")

    d.core_properties.author = autor

    d.save(out)
    print("ok", out, "| šablona:", os.path.basename(sablona), "| autor:", autor)


if __name__ == "__main__":
    main()

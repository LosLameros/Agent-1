#!/usr/bin/env python3
"""Pomocný nástroj pro učení z newsletterů Portu (viz prompts/uceni-z-newsletteru.md).

Podpříkazy:

  archiv <RRRR-MM-DD> <typ>
      Připíše odstavce ze stdin (jeden odstavec = jeden řádek) do
      vystupy/newsletter-uceni/navrhy/<RRRR-MM-DD>.md. Datum je pátek, na který karta míří
      (název karty „DD.MM.RRRR - číslo“). Typ: tip | makro | ranni-prehled | patecni-uprava.
      Tohle volá monitoring po každém zápisu do Google dokumentu.

  rozbor <RRRR-MM-DD> <soubor-s-finalnim-textem.txt>
      Porovná původní návrhy z monitoringu s finálním textem karty (export z Google
      dokumentu jako txt) a vypíše: u každého návrhu co s ním kolegové udělali
      (beze změny / drobné úpravy / přepsáno / vyřazeno), změny slov a délek a odstavce,
      které v návrzích nebyly. Výstup čte pondělní analýza.
"""
import difflib
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
DIR = ROOT / "vystupy" / "newsletter-uceni"
TYPY = {"tip", "makro", "ranni-prehled", "patecni-uprava"}


def archiv(datum, typ):
    if typ not in TYPY:
        sys.exit(f"Neznámý typ {typ}, povolené: {', '.join(sorted(TYPY))}")
    odstavce = [r.strip() for r in sys.stdin.read().split("\n") if r.strip()]
    if not odstavce:
        sys.exit("Na vstupu nejsou žádné odstavce")
    (DIR / "navrhy").mkdir(parents=True, exist_ok=True)
    soubor = DIR / "navrhy" / f"{datum}.md"
    cas = datetime.now(ZoneInfo("Europe/Prague")).strftime("%Y-%m-%dT%H:%M")
    with soubor.open("a", encoding="utf-8") as f:
        for o in odstavce:
            f.write(f"## {cas} | {typ}\n{o}\n\n")
    print(f"Archivováno {len(odstavce)} odstavců do {soubor.relative_to(ROOT)}")


def nacti_navrhy(datum):
    soubor = DIR / "navrhy" / f"{datum}.md"
    text = soubor.read_text(encoding="utf-8")
    bloky = re.findall(r"^## (\S+) \| (\S+)\n(.+?)\n(?=\n|$)", text, flags=re.M)
    return [{"cas": c, "typ": t, "text": x.strip()} for c, t, x in bloky]


def opener_a_telo(odstavec):
    """Opener je první věta (do první tečky/otazníku/vykřičníku), pokud je krátká."""
    m = re.match(r"^(.{3,80}?[.?!])\s+(.*)$", odstavec)
    return (m.group(1), m.group(2)) if m else ("", odstavec)


def podobnost(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def slovni_zmeny(a, b, limit=14):
    wa, wb = a.split(), b.split()
    sm = difflib.SequenceMatcher(None, wa, wb)
    zmeny = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        zmeny.append(f"„{' '.join(wa[i1:i2]) or '∅'}“ → „{' '.join(wb[j1:j2]) or '∅'}“")
    return zmeny[:limit], max(0, len(zmeny) - limit)


def rozbor(datum, final_soubor):
    navrhy = nacti_navrhy(datum)
    final_text = Path(final_soubor).read_text(encoding="utf-8-sig")
    final = [p.strip() for p in final_text.split("\n") if len(p.strip()) > 80]
    # poslední verze každého odstavce (páteční úprava přepisuje dřívější návrh, klíč = opener)
    posledni = {}
    for n in navrhy:
        if n["typ"] == "ranni-prehled":
            continue
        op, telo = opener_a_telo(n["text"])
        klic = (op or telo[:40]).lower()
        # páteční verze nahradí dřívější návrh stejného tématu (shoda těla nad 0.5)
        nahrazeno = None
        for k, v in posledni.items():
            if podobnost(opener_a_telo(v["text"])[1][:200], telo[:200]) > 0.5:
                nahrazeno = k
                break
        if nahrazeno:
            del posledni[nahrazeno]
        posledni[klic] = n
    pouzite = set()
    stat = {"beze změny": 0, "drobné úpravy": 0, "přepsáno": 0, "vyřazeno": 0}
    delky_m, delky_f = [], []
    print(f"# Rozbor vydání {datum}: {len(posledni)} návrhů, {len(final)} odstavců ve finále\n")
    for klic, n in posledni.items():
        mine = n["text"]
        tel_m = opener_a_telo(mine)[1]
        nej = max(range(len(final)), key=lambda i: podobnost(opener_a_telo(final[i])[1][:300], tel_m[:300]))
        r = podobnost(opener_a_telo(final[nej])[1], tel_m)
        if r >= 0.995:
            stav = "beze změny"
        elif r >= 0.80:
            stav = "drobné úpravy"
        elif r >= 0.45:
            stav = "přepsáno"
        else:
            stav = "vyřazeno"
        stat[stav] += 1
        print(f"## [{stav}, shoda {r:.2f}] {n['cas']} {n['typ']}: {mine[:60]}…")
        if stav == "vyřazeno":
            print("   (v finále toto téma není)\n")
            continue
        pouzite.add(nej)
        fin = final[nej]
        delky_m.append(len(mine))
        delky_f.append(len(fin))
        om, ofn = opener_a_telo(mine)[0], opener_a_telo(fin)[0]
        if om != ofn:
            print(f"   opener: „{om}“ → „{ofn}“")
        print(f"   délka: {len(mine)} → {len(fin)} znaků")
        if stav != "beze změny":
            zm, zbytek = slovni_zmeny(opener_a_telo(mine)[1], opener_a_telo(fin)[1])
            for z in zm:
                print("   -", z)
            if zbytek:
                print(f"   … a dalších {zbytek} změn")
        print()
    chybi = [f for i, f in enumerate(final) if i not in pouzite]
    print("## Odstavce ve finále, které v návrzích nebyly (psali kolegové nebo jiný zdroj)")
    for f in chybi:
        print("  *", f[:110].replace("\n", " "))
    print("\n## Souhrn")
    for k, v in stat.items():
        print(f"  {k}: {v}")
    if delky_m:
        print(f"  průměrná délka návrhu {sum(delky_m)//len(delky_m)} znaků, finální {sum(delky_f)//len(delky_f)} znaků")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "archiv":
        archiv(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 4 and sys.argv[1] == "rozbor":
        rozbor(sys.argv[2], sys.argv[3])
    else:
        print(__doc__)
        sys.exit(1)

#!/usr/bin/env python3
"""Stáhne názorové články hlavního ekonoma z Portu Magazínu jako vzory.

Použití:
    python3 -I nastroje/nazorove-clanky-z-magazinu.py [cílová složka] [--seznam]

- Výchozí cílová složka je examples/nazorove-clanky/.
- Bez přepínače stáhne články s názvem „Názor hlavního ekonoma: …“, které ve složce
  ještě nejsou (pozná je podle odkazu v hlavičce souboru), a převede je do Markdownu.
- --seznam jen vypíše posledních 15 článků série (datum, název, odkaz), nic neukládá.
  Hodí se ke kontrole, o čem hlavní ekonom psal naposledy.

Seznam článků bere z WordPress API magazínu (magazin.portu.cz/wp-json), text článku
ze stránky článku, protože API tělo článku nevrací. Grafy se do textu nepřenesou,
v Markdownu je místo nich značka [GRAF].
"""
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

API = "https://magazin.portu.cz/wp-json/wp/v2/posts"
PREFIX = "názor hlavního ekonoma"
UA = {"User-Agent": "Mozilla/5.0 (Agent-1)"}


def stahni(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read().decode("utf-8")


def seznam_clanku():
    clanky, strana = [], 1
    while True:
        dotaz = urllib.parse.urlencode({
            "search": "hlavního ekonoma", "per_page": 100, "page": strana,
            "_fields": "id,date,slug,title,link",
        })
        try:
            data = json.loads(stahni(f"{API}?{dotaz}"))
        except urllib.error.HTTPError as e:
            if e.code == 400:  # za poslední stránkou
                break
            raise
        if not data:
            break
        clanky += data
        if len(data) < 100:
            break
        strana += 1
    clanky = [c for c in clanky if html.unescape(c["title"]["rendered"]).lower().startswith(PREFIX)]
    return sorted(clanky, key=lambda c: c["date"], reverse=True)


class Markdown(HTMLParser):
    def __init__(self):
        super().__init__()
        self.out, self.href, self.skip = [], None, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        elif self.skip:
            return
        elif tag == "p":
            self.out.append("\n\n")
        elif tag in ("strong", "b"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("_")
        elif tag in ("h2", "h3", "h4"):
            self.out.append("\n\n**")
        elif tag == "li":
            self.out.append("\n- ")
        elif tag == "br":
            self.out.append("\n")
        elif tag == "a":
            self.href = a.get("href")
            self.out.append("[")
        elif tag == "img":
            self.out.append("\n\n[GRAF]\n\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip -= 1
        elif self.skip:
            return
        elif tag in ("strong", "b", "h2", "h3", "h4"):
            self.out.append("**")
        elif tag in ("em", "i"):
            self.out.append("_")
        elif tag == "a":
            self.out.append(f"]({self.href})" if self.href else "]")
        elif tag in ("ul", "ol"):
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def prevod(stranka):
    titulek = re.search(r'<h1 class="article-intro__title">(.*?)</h1>', stranka, re.S)
    titulek = html.unescape(re.sub("<[^>]+>", "", titulek.group(1))).strip()
    autor = re.search(r'article-intro-meta">\s*<span><a[^>]*>(.*?)</a>', stranka, re.S).group(1).strip()
    datum = re.search(r'article-intro-meta">.*?<span>(\d{1,2}\.\d{1,2}\.\d{4})</span>', stranka, re.S).group(1)
    perex = re.search(r'<p class="article-intro__subtitle">(.*?)</p>', stranka, re.S)
    perex = html.unescape(re.sub("<[^>]+>", "", perex.group(1))).replace("\xa0", " ").strip() if perex else ""

    # tělo článku: novější šablona má <div class="first-p-0">, starší začíná hned v sekci obsahu
    zacatek = stranka.find('<div class="first-p-0">')
    if zacatek < 0:
        zacatek = stranka.find(">", stranka.find("section-article-content--post")) + 1
    konec = stranka.find('<div class="highlight-box', zacatek)
    if konec < 0:
        konec = stranka.find('class="writter-box"', zacatek)
    p = Markdown()
    p.feed(stranka[zacatek:konec])
    text = "".join(p.out).replace("\xa0", " ")
    text = re.sub(r"\*\*\s*\*\*", "", text)
    text = re.sub(r"(\n\n\[GRAF\]){2,}", "\n\n[GRAF]", text)  # obrázek a jeho <noscript> kopie
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return titulek, autor, datum, perex, text


def nazev_souboru(clanek):
    slug = re.sub(r"^(nazor|sloupek)-hlavniho-ekonoma-", "", clanek["slug"])[:60].rstrip("-")
    return f"{clanek['date'][:10]}-{slug}.md"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cil = args[0] if args else os.path.join(os.path.dirname(__file__), "..", "examples", "nazorove-clanky")
    clanky = seznam_clanku()

    if "--seznam" in sys.argv:
        for c in clanky[:15]:
            print(c["date"][:10], html.unescape(c["title"]["rendered"]), c["link"])
        return

    os.makedirs(cil, exist_ok=True)
    ulozene = set()
    for f in os.listdir(cil):
        if f.endswith(".md"):
            ulozene |= set(re.findall(r"\*\*Odkaz:\*\* (\S+)", open(os.path.join(cil, f), encoding="utf-8").read()))

    nove = [c for c in clanky if c["link"] not in ulozene]
    for c in nove:
        titulek, autor, datum, perex, text = prevod(stahni(c["link"]))
        d, m, r = (int(x) for x in datum.split("."))
        znaky = len(re.sub(r"\[GRAF\]|\*\*|\]\([^)]*\)|[\[\]_]", "", text).strip())
        hlavicka = (f"# {titulek}\n\n- **Autor:** {autor}\n- **Vyšlo na Portu Magazínu:** {d}. {m}. {r}\n"
                    f"- **Odkaz:** {c['link']}\n- **Délka:** {znaky} znaků včetně mezer\n\n---\n\n")
        telo = (f"**Perex:** {perex}\n\n" if perex else "") + text + "\n"
        with open(os.path.join(cil, nazev_souboru(c)), "w", encoding="utf-8") as fh:
            fh.write(hlavicka + telo)
        print("nový vzor:", nazev_souboru(c), f"({znaky} znaků)")
    print(f"Hotovo. Článků v sérii: {len(clanky)}, nově staženo: {len(nove)}.")


if __name__ == "__main__":
    main()

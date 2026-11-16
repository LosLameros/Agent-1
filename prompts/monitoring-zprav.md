# Monitoring zpráv pro newsletter Portu

Automatická úloha běží 4× denně (8:30, 11:30, 14:30 a 17:30 pražského času). Do Google dokumentu „Newsletter Portu v2“ připisuje tipy na zprávy, o kterých by se v pátečním newsletteru dalo psát.

## Kam psát

- Dokument: `11dCllxM5wgdFW6etivphnbV-7blr2JpL9-4NHvoME3w` (Google Docs `read_doc` / `update_doc`).
- Karta: vždy ta na **pozici 0**, tedy nejnovější („DD.MM.RRRR - číslo“, např. „20.11.2026 - 467“). Novou kartu zakládá jiná úloha každý pátek ve 20:00.
- Výstup `read_doc` je velký a uloží se do souboru. Zpracuj ho přes `jq`: ID a názvy karet, text karty a `endIndex` posledního odstavce.
- Text karty jde stáhnout i veřejným exportem: `curl -sSL "https://docs.google.com/document/d/<ID>/export?format=txt&tab=<tabId>"`.

## Co hlídat

Projdi tyto zdroje a vyber zprávy od posledního vydání newsletteru, tedy od pátku 18:00:

- **Yahoo Finance, HN, E15:** stránky jdou stáhnout přímo (`curl` nebo WebFetch).
- **Patria, Seznam Zprávy:** při stahování následuj přesměrování (`curl -L`). Plné články Patrie bývají za placenou zdí, perex ale stačí.
- **Bloomberg, CNBC:** přímo nejdou otevřít (403), hledej je přes WebSearch s `allowed_domains`.
- **XTB, Ranní shrnutí (důležité, každý den):** seznam článků je na https://www.xtb.com/cz/trzni-analyzy/zpravy-z-trhu. Každý den najdi dnešní „Ranní shrnutí“, přečti ho celé a zapiš **vždy** jeden souhrnný tip: titulek plus stručně všechna témata, která shrnutí pokrývá (indexy, měny, komodity, firmy, makrodata, události dne), a odkaz přímo na článek. Tento tip se zapisuje i tehdy, když se témata překrývají s tím, co v kartě už je, a nepočítá se do limitů níže. Zapisuje ho první běh dne, ve kterém už je shrnutí venku (obvykle 8:30, jinak 11:30). Pokud tip s dnešním Ranním shrnutím v kartě už je, znovu ho nepiš.

## Co vybírat

Newsletter má **maximálně 13 odstavců**, takže do dokumentu patří jen opravdu důležité zprávy:

- velké pohyby trhů a indexů (S&P 500, Nasdaq, Euro Stoxx, DAX, PX, Nikkei, bitcoin, zlato, ropa)
- centrální banky a klíčová makrodata (Fed, ECB, ČNB, inflace, HDP, trh práce v USA, ČR a eurozóně)
- výsledky a zásadní zprávy velkých firem (Big Tech, Nvidia, velké IPO, megafúze) a českých titulů (ČEZ, KB, Moneta, CSG, Colt…)
- AI boom a jeho financování, geopolitika s dopadem na trhy, regulace, daně a novinky pro drobné investory (DIP apod.)

Nevybírej drobné firemní zprávy, analytické cílové ceny ani spekulace bez potvrzení.

Pravidla:

- **Max. 3 nové tipy za jeden běh.** Častěji 0–2. Když nic důležitého nového není, nepiš nic.
- **Celkem max. 20 tipů na kartu (týden), bez tipů z Ranního shrnutí XTB.** Když už jich tam tolik je, přidej nový jen tehdy, když je důležitější než většina stávajících.
- **Žádné duplicity.** Před zápisem porovnej téma se vším, co v kartě už je: s odstavci kolegů, jejich odkazy i s dřívějšími tipy. Shoda tématu stačí, i když je jiný zdroj nebo jiná formulace. Pokud téma dostalo zásadní nový vývoj (např. IPO má stanovenou cenu), smíš přidat nový tip, ale napiš v něm, co je nového.
- **Jen ověřená fakta.** Klíčové číslo ověř aspoň ve druhém zdroji, pokud to jde. Nic si nedomýšlej. Když si nejsi jistý, tip nepiš.
- U zpráv o Anthropicu buď čistě věcný, protože jde o firmu, která tě vyvinula.

## Formát zápisu

- Na konec karty jednou přidej tučný řádek **„Tipy na témata (Claude)“**, pokud tam ještě není. Pod něj piš tipy.
- U Ranního shrnutí XTB je formát `Po 16. 11., ráno · Ranní shrnutí XTB: <titulek>. <témata oddělená středníkem>`, odkaz na celý text za tečkou s mezerou; může mít až cca 500 znaků.
- Každý tip je jeden odstavec: `Po 16. 11., ráno · ` a pak 1–2 české věty, max. cca 250 znaků, s klíčovým číslem. Den v týdnu piš zkratkou, část dne „ráno / odpoledne / večer“.
- Celý text tipu za tečkou s mezerou je **hypertextový odkaz** na zdrojový článek. Odkazuj na nejlepší dostupný původní zdroj z výše uvedených.
- Písmo Rethink Sans (weight 400), netučné.
- Vkládej přes `insertText` s `endOfSegmentLocation` (`tabId` karty), pak nastav styl a odkaz podle indexů. Použij `requiredRevisionId` z posledního `read_doc`.
- **Nic jiného v dokumentu neměň ani nemaž.**

Na konci běhu odpověz v chatu jedním řádkem: kolik tipů jsi přidal a o čem byly, nebo „nic nového“.

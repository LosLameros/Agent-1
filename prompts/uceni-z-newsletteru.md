# Co jsme se naučili z finálních newsletterů

Tenhle soubor je „paměť stylu“. Monitoring ho čte před psaním odstavců (viz `prompts/monitoring-zprav.md`). Každé pondělí ho aktualizuje pondělní analýza: porovná, co monitoring do karty navrhl (archiv `vystupy/newsletter-uceni/navrhy/`), s tím, co kolegové nakonec odeslali (`vystupy/newsletter-uceni/finalni/`), a zapíše, co se opakuje. Cíl: aby kolegové odstavce museli přepisovat co nejméně.

Pravidla zde **doplňují** pravidla v `prompts/monitoring-zprav.md`, nepřebíjejí je: délka odstavce, žádné „podle…“, odkaz na slovese a čeští zdroje platí vždy.

## Pravidla naučená z úprav kolegů

(Číslo v závorce = kolik vydání to potvrdilo. Pravidlo se přidá z jednoho rozboru, ale když ho další vydání vyvrátí, zruší se.)

1. **Spisovněji a neutrálněji (1×).** Kolegové mění hovorové „víc“ na „více“ (7× za jedno vydání), „kterékoli“ na „kterékoliv“, „Pár z nich“ na „Několik z nich“, „Za první den“ na „Během prvního dne“. Piš rovnou „více“, „kterékoliv“, „několik“.
2. **Přesná zaokrouhlení (1×).** „přes 10 %“ → „zhruba 10 %“, „skoro čtvrtinu“ → „více než čtvrtinu“, „skoro 40 %“ → „přes 40 %“. Slovo „přes“ nebo „skoro“ používej jen tehdy, když je to doslova pravda, jinak „zhruba“, „téměř“, „více než“.
3. **Čísla trhů musí být z doby odeslání (1×).** Při úpravách kolegové přepisují ceny a hodnoty podle aktuálního stavu (zlato 3 800 → 3 550 dolarů, bitcoin 64 → 61 tisíc, hodnota Anthropicu 1,5 → 1,3 bilionu). Ceny aktiv, které se rychle mění, ověř těsně před zápisem a v pátek ráno obnov.
4. **Opener říká, o čem odstavec je (1×).** „Jestřábi v přesile“ → „Jestřábi zvyšují sazby“, „Hit bez potlesku“ → „Hit bez zisků“, „Mrak plný peněz“ → „Mraky peněz“. Metafora, která nic nesděluje, se opravuje na konkrétnější. Hříčka je v pořádku, když je krátká a jasná („Křemíková kocovina“, „Deutsche Leaks“, „Mír na papíře“ prošly), a odstavec bez openeru kolegové vždy doplnili.
5. **Pointa na konci je kratší a prostší (1×).** Moje „Klasika: kupuj fámy, prodávej zprávy“ → „Prostě akciová loupež za bílého dne“, „…zjistil, že nejistota je on sám“ → „…s tím to letos vypadá nejistě“. Příliš chytré nebo hlubokomyslné pointy kolegové střídají jednoduchým hovorovým rýpnutím. Nemáš-li dobrou, nech odstavec bez ní (AMD a „Mír na papíře“ prošly bez změny).
6. **Plné věty místo telegrafických (1×).** „Anthropic prodal akcie za 83 dolarů, nad plánovaným rozpětím 70–78 dolarů, a získal přes 81 miliard“ → „stanovil cenu jedné akcie na 83 dolarů, což bylo nad očekávaným rozmezím 70–78 dolarů. Získal tak přes 81 miliard…“. Čísla spojuj do souvětí se „což“, „totiž“, „při této ceně“ a „tak“, nesypej je za sebou v úsečných větách.
7. **Škrtají se drobnosti, přidává se kontext (1×).** Pryč šly ticker („Obchoduje se pod zkratkou ANT“), pohyb indexu v tentýž den v odstavci o jiném tématu a analytická laťka (1,9 mld. u GTA). Přidal se kontext, který dává čísla smysl („12. nejhodnotnější společnost světa“, hodnota firmy). Vynech tickery a okrajová čísla, raději přidej, kam se věc řadí.
8. **Délka je v pořádku (1×).** Průměr mých návrhů 478 znaků, finále 484, rozpětí finálních odstavců 398–515. Nezkracuj pod 450 znaků bez důvodu a když odstavec přeroste 515, škrtni vedlejší fakt, ne slova.
9. **Témata, která jsem minul (1×, archiv pokrývá jen 19.–20. 11.).** Kolegové do vydání dopsali makro (inflace v EU 4 %), regulaci (americké exportní licence na čipy), bankovní M&A (UniCredit a Commerzbank), výsledky Nvidie a „Bring back Jensen“. Hlídej víc regulaci čipů a exportní omezení, evropskou inflaci a velké bankovní fúze (viz i sekci Makrozprávy v monitoringu).

## Příklady před/po (nejpoučnější úpravy)

**Pointa (GTA, vydání 467)**
- Moje: „…Analytici přitom za laťku spokojenosti brali 1,9 miliardy. Klasika: kupuj fámy, prodávej zprávy.“
- Finále: „…od začátku roku jsou zhruba o 18 % níž. Prostě akciová loupež za bílého dne.“

**Struktura věty (Anthropic IPO)**
- Moje: „Anthropic prodal akcie za 83 dolarů, nad plánovaným rozpětím 70–78 dolarů, a získal přes 81 miliard dolarů. Překonal tak dosavadní rekord SpaceX.“
- Finále: „Anthropic při svém vstupu na burzu stanovil cenu jedné akcie na 83 dolarů, což bylo nad očekávaným rozmezím 70–78 dolarů. Získal tak přes 81 miliard dolarů a překonal dosavadní rekord SpaceX.“

**Opener a aktualizace čísla (Fed)**
- Moje: „Jestřábi v přesile. … Pár z nich by v prosinci přidal rovnou víc než čtvrt bodu … srazily zlato poprvé od září 2025 pod 3 800 dolarů za unci.“
- Finále: „Jestřábi zvyšují sazby. … Několik z nich by v prosinci přidalo rovnou více než čtvrt bodu … srazily zlato až k 3 550 dolarům za unci, více než třetinu pod lednovým rekordem.“

**Pointa (bitcoin)**
- Moje: „Kdo bral bitcoin jako pojistku proti nejistotě, letos zjistil, že nejistota je on sám.“
- Finále: „Kdo bral bitcoin jako pojistku proti nejistotě, s tím to letos vypadá nejistě.“

## Historie analýz

| Vydání | Návrhů | Beze změny | Drobné úpravy | Přepsáno | Vyřazeno | Poznámka |
|---|---|---|---|---|---|---|
| 2026-11-20 (#467) | 9 | 1 | 6 | 2 | 0 | První rozbor, zpětně z uloženého přepisu session; archiv jen od 19. 11. |

## Jak tento soubor aktualizovat (pondělní analýza)

- Rozbor spusť přes `python3 -I nastroje/newsletter-uceni.py rozbor <datum pátku> <finální text.txt>`.
- Pravidla slučuj, nenarůstej: celkem nejvýš kolem 12 pravidel. Když se pravidlo potvrdí podruhé, zvyš číslo v závorce. Když ho nové vydání vyvrátí (kolegové dělají opak), pravidlo uprav nebo smaž. Pravidlo nezobecňuj z jedné drobnosti, potřebuje jasný vzorec (opakování nebo zřetelný rozdíl).
- Příklady před/po drž na 4–6 nejpoučnějších, starší vyměň za lepší.
- Do tabulky doplň jeden řádek za vydání.
- Nic z tohoto souboru nesmí rozvolnit tvrdá pravidla z `prompts/monitoring-zprav.md` (délka, „podle…“, odkazy, Novinky.cz, Slack kontrola). Když by rozbor naznačoval jejich změnu, napiš to uživateli do odpovědi jako návrh, ne do pravidel.

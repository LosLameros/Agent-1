# Prompt – článek pro Portu Magazín, typ 2: nová nabídka

Druhý typ článku pro Portu Magazín. Použij ho, když článek oznamuje **novinku v nabídce Portu**: nový instrument (akcie, ETF), sadu nových instrumentů, novou strategii nebo modelové portfolio v Portfoliu podle vás, případně novou funkci produktu.

Pro běžné články o trzích, firmách a ekonomice (typ 1) platí `prompts/clanky-portu.md`. Z něj tento prompt přebírá **roli (ROLE A KONTEXT), rešerši (KROK 1), stylistická pravidla (KROK 3) a compliance (KROK 5)**. Liší se struktura, práce s produktem, povinné tabulky a výstup.

Vzorový výstup: `vystupy/clanky/2026-11-23-ceske-dividendy-portfolio-podle-vas.md` (strategie České dividendy, srovnání s WOOD PX ETF).

## VSTUPNÍ PROMĚNNÉ (vyplň před spuštěním)

- **NOVINKA:** [co přibylo – název instrumentu, strategie nebo funkce]
- **DRUH:** [nový instrument / sada instrumentů / nová strategie nebo modelové portfolio / nová funkce]
- **STAV:** [schváleno ke spuštění k datu X / interní návrh]. Dokud není schváleno, článek nepíše „nově najdete“ ani „spouštíme“ a celý výstup je označený jako návrh ke schválení.
- **DATUM SPUŠTĚNÍ:** [datum]
- **KDE V APLIKACI:** [produkt a postup – Portfolio podle vás, Brokerage režim, DIP…]
- **MINIMÁLNÍ INVESTICE A POPLATKY:** [částka, poplatek produktu, TER instrumentu, akce s datem konce]
- **SROVNÁVACÍ NABÍDKA:** [co podobného už Portu nabízí a s čím čtenář novinku srovná – např. WOOD PX ETF, Portfolio od Portu, jiná strategie]
- **PODKLADY:** [metodika, interní tabulka, tisková zpráva, Q&A]
- **CO NEPSAT:** [interní informace z podkladů, které do článku nepatří]
- **DEADLINE DAT:** [datum, ke kterému platí všechna čísla]

## JAK PORTU MAGAZÍN O NOVINKÁCH PSAL (rozbor 2019–2026)

Rozbor 12 článků: spuštění strategií (2019), Světová špička a Odpovědná budoucnost (2019), 8 nových ETF (2020), Akcie rozvojových zemí (2021), Nově na Portu: české akcie a Pražská špička (2022), VWCE (2023), Nové příležitosti na Portu (2025), Nové názvy produktů (2025), 6 nových ETF (březen 2026), CSG a modelové portfolio Bezpečnost a obrana (únor 2026), 187 nových ETF a akcií (červen 2026), WOOD PX ETF (září 2026).

**Co se opakuje a zachováváme:**

- **Titulek s rámcem novinky:** „Nově na Portu: …“, „Rozšiřujeme nabídku …: …“, „Představení strategie: …“, „X nových ETF na Portu: …“. Za dvojtečkou konkrétně, co přibylo.
- **Perex jednou až dvěma větami** říká, co přibylo a kde to čtenář najde. Konkrétní číslo (počet instrumentů, minimální částka, nákladovost) je výhoda.
- **Hlas:** „my“ za Portu („přidali jsme“, „rozšiřujeme“), vykání čtenáři. Starší články psaly o Portu ve třetí osobě, novější ne.
- **Kostra:** co přibylo → proč a pro koho → co v tom je (složení, parametry) → kde to najdete a za kolik → standardní blok upozornění.
- **Standardní blok na konci** „Na co si dát po přečtení tohoto článku pozor?“ (znění níže).
- **Citace vedení** jen u novinek s externím partnerem (WOOD & Company, burza). U běžného rozšíření nabídky ne.

**Co dřív chybělo a teď to chceme:**

- **Tabulky.** Žádný z článků neměl tabulku: složení strategií bylo v textu nebo na obrázku, TER a tickery chyběly. U strategie a modelového portfolia je tabulka složení povinná (viz KROK 3).
- **Srovnání s existující nabídkou.** Čtenář se ptá „čím je to jiné než to, co už máte?“. Starší články to řešily jednou větou nebo vůbec.
- **Rizika v textu, ne jen v patičce.** Většina článků spoléhala na standardní blok. Dobrým vzorem je článek o CSG (únor 2026): konkrétní riziko a věta, že sektorová sázka má být jen doplňkem širšího portfolia.
- **Kde a za kolik.** Minimální investice a poplatky byly zmíněné jen v části článků. Patří do každého.
- **Kontrola čísel.** Ve starších článcích nesedí součty vah (98 %), počty („187 nových“ v titulku, „téměř 200“ v textu) a jsou tam překlepy v názvech firem. Součty a názvy vždy přepočítej a zkontroluj.

**Čemu se vyhnout:** marketingovým superlativům ze starších textů („revoluční“, „ideální řešení“), výzvám s vykřičníkem („Vyzkoušejte … ještě dnes!“) a obecným frázím („může oslovit investory“, „zajímavý doplněk“) bez konkrétního důvodu.

## KROK 0 – MYŠLENKOVÁ PŘÍPRAVA

Odpověz si pro sebe:

1. **Co přesně přibylo, jednou větou?** Bez přívlastků. Tahle věta je základ perexu.
2. **Pro koho to je a pro koho ne?** Novinka má smysl pro určitého investora. Řekni to a řekni i, komu stačí stávající nabídka.
3. **Čím se to liší od toho, co už nabízíme?** Najdi nejbližší existující produkt nebo instrument a sepiš 4–8 rozdílů, které čtenáře zajímají (co dostane, co platí, jaké riziko nese, jak se zdaní).
4. **Co z podkladů do článku nepatří?** Interní varianty, kapacity, jména kolegů, provozní otázky, rušené produkty. Vyřaď je dřív, než začneš psát.

## KROK 1 – REŠERŠE A OVĚŘENÍ

Platí KROK 1 z `prompts/clanky-portu.md`. Navíc:

- Všechna čísla z interních podkladů přepočítej: součty vah (musí dát 100 %), podíly sektorů, rozdíly proti srovnávací nabídce, příkladové částky.
- Tvrzení v podkladech („nejvíc nadvážený“, „třetí snížení po sobě“) ověř proti datům. Co nesedí, do článku nepiš a uveď v poznámkách pro autora.
- Parametry srovnávací nabídky ber z primárního zdroje (stránka fondu, portu.cz) k datu psaní.
- Poplatky, minimální částku a dostupnost v produktech (Portfolio podle vás, Brokerage, DIP) nikdy nedomýšlej. Když nejsou v zadání, napiš [DOPLNIT].

## KROK 2 – STRUKTURA ČLÁNKU

1. **Titulek** – 3 varianty. Aspoň jedna v rámci „Nově v/na …: …“ nebo „Rozšiřujeme nabídku …: …“. Žádné procento výnosu v titulku.
2. **Perex (2–3 věty)** – co přibylo, kde to je a v čem je hlavní rozdíl proti stávající nabídce.
3. **Úvod bez mezititulku** – novinka, datum, produkt, 2–3 nejdůležitější fakta (největší pozice, nákladovost, minimum). Druhý odstavec: proč novinka vznikla a jak navazuje na stávající nabídku.
4. **Tělo (3–6 sekcí s mezititulky)**, podle druhu novinky:
   - **Strategie / modelové portfolio:** Co ve strategii je (tabulka složení) → Jak jsme vybírali (filtry jako číslovaný seznam otázek) → Jak jsme určili váhy (a proč ne jinak) → Co čtenář dostane (výnos, příjem, příklad na 100 000 Kč, odhady jako tabulka) → Srovnání se stávající nabídkou (srovnávací tabulka) → Na co myslet (rizika).
   - **Jeden instrument:** Co to je a co sleduje → Složení a parametry (tabulka) → Čím se liší od podobných instrumentů v nabídce → Rizika.
   - **Sada instrumentů:** krátký úvod, pak pro každý instrument mezititulek s tématem a 1–2 odstavci (co sleduje, proč může dávat smysl, hlavní riziko). Na konci přehledová tabulka.
   - **Nová funkce:** co se mění → jak to funguje (postup krok za krokem) → kolik to stojí → co když nechci nic měnit.
5. **Jak novinku najdete** – produkt, postup v aplikaci, minimální investice, poplatek. Pokud čtenář už drží podobný instrument, napiš, jestli musí něco prodávat.
6. **Standardní blok upozornění** – doslova:

   > **Na co si dát po přečtení tohoto článku pozor?**
   > - Článek není investičním doporučením.
   > - Historická výnosnost není nikdy zárukou budoucích výnosů.
   > - Investice na kapitálových trzích jsou vždy rizikové.
   > - Portu negarantuje dosažení výnosů z investice na kapitálových trzích.
   > - Nejste si jistí, jaký rizikový profil je pro vás vhodný, nebo jestli je pro vás vhodné například tematické investování? Vyplňte si náš investiční dotazník a my vám poradíme.

**Délka:** 900–1 300 slov bez tabulek (sada instrumentů může být delší).

## KROK 3 – POVINNÉ TABULKY

Tabulky jsou v tomto typu článku hlavní nosič informací. Pod každou tabulkou kurzívou zdroj a datum.

1. **Složení** (u strategie a modelového portfolia povinně): Firma / instrument | Váha | Váha ve srovnávací nabídce | Proč má takovou váhu (jedna srozumitelná věta). Poslední řádek hotovost. Součet 100 %.
2. **Srovnání se stávající nabídkou** (povinně, pokud existuje podobný produkt): řádky podle toho, co čtenáře zajímá – co se děje s výnosem (vyplácí / reinvestuje), počet titulů, jak se určují váhy, největší sektor, měna a měnové riziko, výnos, zdanění, náklady, kde se dá koupit.
3. **Odhady a výhled** (jen když jsou v podkladech): vždy nadepsat a pod tabulkou výslovně „odhad, ne údaj firem ani slib výnosu“.
4. **Parametry instrumentu** (u ETF): název, co sleduje, nákladovost (TER), akumulační / distribuční, měna, počet titulů, největší pozice.

Pod tabulkou vždy jeden až dva odstavce, které z ní vytáhnou to podstatné. Tabulka nesmí být jediné místo, kde je hlavní pointa.

## KROK 4 – STYL

Platí KROK 3 z `prompts/clanky-portu.md` (otvírák odstavce do 8 slov, aktivní rod, odstavec max. 4 věty, vysvětlit pojmy, české formátování čísel, zakázané obraty). Navíc:

- **Piš přirozeně, bez příkras.** Žádné metafory a efektní otvíráky, žádné „představujeme vám“. Věcně, jako když kolega vysvětluje klientovi, co je nového.
- **Nevysvětluj přehnaně.** Pojem vysvětli jednou krátce a jdi dál. Čtenář Portu není začátečník ve všem.
- **Tučně jen klíčové informace** – hlavní čísla a rozdíly, ne celé věty.
- **„My“ za Portu, vykání čtenáři.**
- **Žádné vykřičníky, emoji ani superlativy** („nejlepší“, „unikátní“, „revoluční“).

## KROK 5 – PRODUKT A COMPLIANCE

Pravidlo „maximálně jedna zmínka produktu“ z typu 1 tady neplatí: produkt je téma článku. Platí ale:

- Popisuj, neprodávej. Novinku vysvětli tak, aby se čtenář mohl rozhodnout sám, včetně toho, komu nedává smysl.
- Žádné „kupte“, „ideální řešení“, „teď je ten správný čas“.
- **Žádné historické výnosy nové strategie** zpětně dopočítané s dnešními vahami. Není to výkonnost, kterou by kdo reálně dosáhl.
- Odhady budoucích dividend a výnosů výslovně označ jako odhad, s datem a zdrojem.
- U strategie z jednoho trhu nebo sektoru zmiň riziko koncentrace, u cizích měn měnové riziko, u dividend zdanění.
- Interní informace z podkladů (varianty návrhu, kapacity, provozní detaily, jména kolegů, rušené produkty, komentáře nadřízených) do článku nikdy nepiš.
- Platí KROK 5 z `prompts/clanky-portu.md`.

## VÝSTUP

1. Upozornění na začátku, pokud je novinka zatím interní návrh nebo chybí údaje ([DOPLNIT] / [OVĚŘIT]).
2. 3 návrhy titulku.
3. Perex.
4. Hotový článek s mezititulky a tabulkami, včetně standardního bloku upozornění.
5. Poznámky pro autora:
   - co doplnit před publikací (datum, poplatky, minimum, postup v aplikaci),
   - rozpory v podkladech, které jsi nepřevzal, a proč,
   - co jsi vědomě vynechal (interní informace),
   - návrh 1 grafu (typicky váhy novinky vedle vah srovnávací nabídky; kreslí agent portu-grafy).

Text odevzdej jako běžný text, ne v bloku kódu.

## SEBEKONTROLA PŘED ODEVZDÁNÍM

- [ ] Je z perexu jasné, co přibylo, kde to je a čím se to liší od stávající nabídky?
- [ ] Dávají váhy v tabulce dohromady 100 % a sedí každé číslo v textu s tabulkou?
- [ ] Je ve srovnávací tabulce to, co čtenáře opravdu zajímá (výnos, zdanění, náklady, riziko)?
- [ ] Je každý odhad označený jako odhad, s datem a zdrojem?
- [ ] Nejsou v článku historické výnosy strategie ani slib výnosu?
- [ ] Jsou rizika v textu, ne jen v patičce?
- [ ] Nejsou v článku interní informace z podkladů?
- [ ] Je uvedeno, kde novinku najdu a za kolik (nebo [DOPLNIT])?
- [ ] Začíná každý odstavec větou do 8 slov, bez trpného rodu a zakázaných obratů?
- [ ] Přečetl jsi po poslední úpravě celý text znovu a opravil i místa, na která tě nikdo neupozornil?

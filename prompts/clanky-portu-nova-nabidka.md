# Prompt – článek pro Portu Magazín, typ 2: nová nabídka

Druhý typ článku pro Portu Magazín. Použij ho, když článek oznamuje **novinku v nabídce Portu**: nový instrument (akcie, ETF), sadu nových instrumentů, nový tematický balíček (modelové portfolio) v Portfoliu podle vás, případně novou funkci produktu.

Pro běžné články o trzích, firmách a ekonomice (typ 1) platí `prompts/clanky-portu.md`. Z něj tento prompt přebírá **roli (ROLE A KONTEXT), rešerši (KROK 1), stylistická pravidla (KROK 3) a compliance (KROK 5)**. Liší se struktura, práce s produktem, povinné tabulky a výstup.

**Vzor pro nový tematický balíček nebo investiční strategii v Portfoliu podle vás:** `examples/clanky/2026-11-ceske-dividendy-finalni-verze.md` – finální, redakcí schválená verze článku o balíčku České dividendy a seznam toho, co redakce změnila oproti návrhu agenta. Než začneš psát, přečti si ho celý. Článek o dalším balíčku nebo strategii má vypadat podobně (stavba níže v kapitole VZOR).

## VSTUPNÍ PROMĚNNÉ (vyplň před spuštěním)

- **NOVINKA:** [co přibylo – název instrumentu, tematického balíčku nebo funkce]
- **DRUH:** [nový instrument / sada instrumentů / nový tematický balíček / nová funkce]
- **STAV:** [schváleno ke spuštění k datu X / interní návrh]. Dokud není schváleno, článek nepíše „nově najdete“ ani „spouštíme“ a celý výstup je označený jako návrh ke schválení.
- **DATUM SPUŠTĚNÍ:** [datum]
- **KDE V APLIKACI:** [produkt a postup – Portfolio podle vás, Brokerage režim, DIP…]
- **MINIMÁLNÍ INVESTICE A POPLATKY:** [částka, poplatek produktu, TER instrumentu, akce s datem konce]
- **SROVNÁVACÍ NABÍDKA:** [co podobného už Portu nabízí a s čím čtenář novinku srovná – např. WOOD PX ETF, Portfolio od Portu, jiný tematický balíček]
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

- **Tabulky.** Žádný z článků neměl tabulku: složení strategií bylo v textu nebo na obrázku, TER a tickery chyběly. U tematického balíčku je tabulka složení povinná (viz KROK 3).
- **Srovnání s existující nabídkou.** Čtenář se ptá „čím je to jiné než to, co už máte?“. Starší články to řešily jednou větou nebo vůbec.
- **Rizika v textu, ne jen v patičce.** Většina článků spoléhala na standardní blok. Dobrým vzorem je článek o CSG (únor 2026): konkrétní riziko a věta, že sektorová sázka má být jen doplňkem širšího portfolia.
- **Kde a za kolik.** Minimální investice a poplatky byly zmíněné jen v části článků. Patří do každého.
- **Kontrola čísel.** Ve starších článcích nesedí součty vah (98 %), počty („187 nových“ v titulku, „téměř 200“ v textu) a jsou tam překlepy v názvech firem. Součty a názvy vždy přepočítej a zkontroluj.

**Čemu se vyhnout:** marketingovým superlativům ze starších textů („revoluční“, „ideální řešení“), výzvám s vykřičníkem („Vyzkoušejte … ještě dnes!“) a obecným frázím („může oslovit investory“, „zajímavý doplněk“) bez konkrétního důvodu.

## TERMINOLOGIE PORTU

- Modelová portfolia v Portfoliu podle vás se na webu i v aplikaci jmenují **tematické balíčky** („Nechte se inspirovat tematickým investováním … S tematickými balíčky nemusíte trávit hodiny analyzováním jednotlivých akcií“). V článku piš „tematický balíček“ nebo krátce „balíček“, **nikdy „strategie“**. „Strategie“ je starý název produktu (do roku 2025).
- Produkty: Portfolio podle vás (dřív Strategie a Portu Crypto), Portfolio od Portu (dřív portfolia na míru).

## VZOR: ČLÁNEK O NOVÉM TEMATICKÉM BALÍČKU NEBO STRATEGII

Podle finální verze článku o balíčku České dividendy (listopad 2026). Platí pro každý nový tematický balíček nebo investiční strategii v Portfoliu podle vás.

**Stavba (zhruba 800–1 000 slov včetně tabulek):**

1. **Titulek:** „Název balíčku: nový tematický balíček + čím je zajímavý“ (vzor: „České dividendy: nový tematický balíček českých firem se spolehlivou dividendou“). Autorovi nabídni i 5 atraktivnějších variant (viz KROK 2).
2. **Tučný perex, tři věty, bez samostatného úvodu:** co přibylo a kde („V Portfoliích podle vás přibyla novinka: …“), co v tom čtenář dostane (počet firem nebo instrumentů a 3–4 známá jména), pro koho to je.
3. **Sekce 1 – složení** (nadpis typu „Devět známých firem v jedné investici“): věta „Portfolio tvoří X firem a Y % hotovosti:“, tabulka **Firma | Váha** včetně řádku Hotovost (součet 100 %, bez vah srovnávacího produktu). Pod ní krátce: jaké typy firem v balíčku jsou (např. vysoká dividenda dnes vs. dividenda, která roste), k čemu je hotovost (vklady, výběry, automatická rebalance, připisování dividend) a v jaké měně se nakupuje (např. vše v korunách na pražské burze, výjimka rakouských firem s podílem v % a vazbou na euro).
4. **Sekce 2 – jak jsme vybírali a vážili** (nadpis popisuje princip vah, např. „Zastoupení společností odpovídající dividendovému potenciálu a spolehlivosti výplaty“): jedna věta, z čeho jsme vybírali; podmínky jako číslovaný seznam s tučnou oznamovací větou („Vyplácejí dividendu pravidelně, …“), ne otázky; výjimky dvěma větami (proč tam firma je a proč má menší váhu); jeden odstavec o vahách (podle čeho, strop na firmu, strop na sektor, příklad firmy, kterou strop drží); že složení pravidelně kontrolujeme a při velké změně upravíme, **a že taková změna se týká jen nově založených portfolií**.
5. **Sekce 3 – co balíček přináší, s číslem v nadpisu** (např. „Více než 4 % na dividendách“): hlavní číslo tučně, příklad na 100 000 Kč tučně, z čeho a k jakému datu je číslo spočítané, jedna až dvě věty o riziku (dividendy se mohou snížit, cena akcií jde nahoru i dolů).
6. **Sekce 4 – připravovaná funkce, pokud je** (např. „Brzy: dividendy rovnou na vaši peněženku“): kdy přijde, co umožní, praktický přehled (kalendář výplat po měsících v odrážkách s tučným měsícem), jak to funguje do té doby, že dáme vědět. Jen pokud termín potvrdil Portu.
7. **Sekce 5 – srovnání se stávající nabídkou** (nadpis jako otázka, např. „Vyplácet, nebo reinvestovat? České dividendy vs. WOOD PX ETF“): jedna věta, co je srovnávací produkt, jeden odstavec o překryvu a hlavním rozdílu (kolik % portfolia je rozloženo jinak, kam jde víc a kam méně peněz), tabulka (viz KROK 3) včetně řádku **Míra kontroly** (balíček: váhy si můžete upravit a doplnit; fond: investuje podle své metodiky).
8. **Sekce 6 – výzva a upozornění** (nadpis typu „Založte si České dividendy během chvilky“): postup v aplikaci krok za krokem (přihlášení, nabídka investic, výběr balíčku, úprava vah, první vklad nebo trvalý příkaz), pak odstavec o rizicích (malý a koncentrovaný trh, málo firem, převaha jednoho sektoru) a že balíček je spíš doplněk dobře diverzifikovaného portfolia.

**Co ve finální verzi není a nepiš to:** detailní kritéria spolehlivosti (počet let, výplatní poměr), limity podle objemu obchodů, odhady dividend na další roky a pokrytí analytiky, historické epizody (rok 2020), konkrétní částky dividend na akcii, odstavec „Proč se váhy liší“, zvažované varianty, interní podmínky návrhu, poznámky pro autora v textu, standardní blok upozornění. Pokud je máš z podkladů, dej je do poznámek pro autora v odpovědi.

**Mezititulky** jsou krátké a říkají čtenáři, co z toho má: počet a výhoda („Devět známých firem v jedné investici“), číslo („Více než 4 % na dividendách“), novinka („Brzy: …“), otázka ke srovnání („Vyplácet, nebo reinvestovat?“), výzva („Založte si … během chvilky“).

## PODKLAD A ČÍSLA

- **Dohodnutý podklad je závazný pro fakta.** Pokud autor dodá dokument odsouhlasený s nadřízeným, čísla, složení a postup výběru musí s ním sedět. Do článku z něj ale převezmi jen to, co klient potřebuje (stavba podle kapitoly VZOR); zvažované varianty a detailní metodiku dej do poznámek pro autora. Při přesunech a úpravách textu na žádost autora nevynechávej informace bez jeho souhlasu. Po napsání projdi podklad bod po bodu a v odpovědi napiš, jestli nějaká informace chybí. Obrázky v Google Dokumentu (tabulky složení) stáhni přes `export?format=zip` a přečti, text z `read_file_content` je neobsahuje.
- **Podklad může mít víc verzí složení** (např. sloupce Původní návrh, Final). Do článku patří vždy to, co autor označí jako finální, včetně hotovosti. Když si nejsi jistý, které je finální, napiš to do odpovědi.
- **Složení srovnávacího ETF bere agent z wood.cz** (`https://www.wood.cz/produkty/wood-px-etf/`), ne z vah indexu PX, a podle něj přepočítá text i tabulky (váhy ve fondu, podíl bank a pojišťoven, odlišnost od fondu, výnos). Čísla z podkladu, která vycházela z indexu PX, přepočítej a rozdíly napiš do poznámek pro autora.
- **Odhady budoucích dividend a výnosů se v článku nepíšou jako čísla ani tabulky.** Váhy popiš přes spolehlivost a růst dividendy (vzor: „Váhy jsme nastavili tak, aby rozhodovala nejen výše dividendy, ale i to, jak spolehlivě ji firma vyplácí a jestli roste.“). Výslovnou zmínku o odhadech přidej, jen když o ni autor požádá.
- **Výjimky z pravidel výběru popiš otevřeně.** Když firma v novince je, ačkoli nesplňuje jedno z pravidel (např. Erste: letos vyplatila zhruba 0,6 %, protože peníze použila na koupi polské banky), napiš proč, co se od ní čeká a proč má menší váhu.
- **Neověřitelná tvrzení z podkladu do článku nepiš** (např. že je firma „nejvíc nadvážená“, když čísla říkají jinak). Důvod patří do poznámek pro autora.
- **Datum spuštění „dnes“ piš jako „od dnešního dne“.** Termíny výplat dividend ověř (např. Erste platí v dubnu) a piš je tak, jak skutečně jsou.
- **Daně z dividend a srážkovou daň v článku nerozebírej.** Klienti dostávají každý rok daňové podklady. Čísla „před zdaněním“ a „po zdanění“ uvést lze.
- **U firem s probíhajícími výsledky nepiš nic aktuálního**, jen obecně (např. u CSG, že dividendu zatím nevyplatila).

## KOMU NOVINKA SLOUŽÍ

Pro koho novinka je, řekni už v perexu jednou větou (vzor: „Je určený všem, kdo chtějí investovat do českých firem a mít ze své investice příjem.“). Rozdíl proti stávající nabídce (např. WOOD PX ETF dividendy znovu investuje) patří až do srovnávací sekce ke konci. Funkce, které ještě neběží (např. výplata dividend na peněženku), popiš jen jako připravovanou novinku s termínem, nikdy jako hotovou věc.

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

1. **Titulek** – hlavní varianta ve tvaru „Název: nový tematický balíček + čím je zajímavý“ a k tomu 5 atraktivnějších variant (konkrétní počet, známá jména, otázka, výhoda pro čtenáře). Bez klikbejtu a bez slibu výnosu; procento výnosu v titulku jen jako aktuální údaj a s upozorněním pro autora na compliance riziko.
2. **Perex (3 věty, tučně)** – co přibylo a kde, co v tom čtenář dostane (počty, známá jména), pro koho to je.
3. **Úvod bez mezititulku** – jen u jednoho instrumentu, sady instrumentů nebo funkce: novinka, datum, produkt, 2–3 nejdůležitější fakta. U tematického balíčku úvod nahrazuje perex a hned následuje sekce se složením.
4. **Tělo (3–6 sekcí s mezititulky)**, podle druhu novinky:
   - **Tematický balíček nebo strategie:** přesně podle kapitoly VZOR (složení → výběr a váhy → co přináší s číslem → připravovaná funkce → srovnání se stávající nabídkou → založení a upozornění).
   - **Jeden instrument:** Co to je a co sleduje → Složení a parametry (tabulka) → Čím se liší od podobných instrumentů v nabídce → Rizika.
   - **Sada instrumentů:** krátký úvod, pak pro každý instrument mezititulek s tématem a 1–2 odstavci (co sleduje, proč může dávat smysl, hlavní riziko). Na konci přehledová tabulka.
   - **Nová funkce:** co se mění → jak to funguje (postup krok za krokem) → kolik to stojí → co když nechci nic měnit.
5. **Jak novinku najdete** – produkt, postup v aplikaci (krok za krokem), minimální investice a poplatek, pokud jsou známé. U balíčku je to závěrečná sekce s výzvou a upozorněním (VZOR, bod 8).
6. **Standardní blok upozornění** – finální verze článku o balíčku ho v textu neměla. Přidej ho jen na žádost autora, doslova:

   > **Na co si dát po přečtení tohoto článku pozor?**
   > - Článek není investičním doporučením.
   > - Historická výnosnost není nikdy zárukou budoucích výnosů.
   > - Investice na kapitálových trzích jsou vždy rizikové.
   > - Portu negarantuje dosažení výnosů z investice na kapitálových trzích.
   > - Nejste si jistí, jaký rizikový profil je pro vás vhodný, nebo jestli je pro vás vhodné například tematické investování? Vyplňte si náš investiční dotazník a my vám poradíme.

**Délka:** tematický balíček zhruba 800–1 000 slov včetně tabulek, ostatní 700–1 200 slov (sada instrumentů může být delší). Kratší a čtivější je lepší než úplný.

## KROK 3 – POVINNÉ TABULKY

Tabulky jsou v tomto typu článku hlavní nosič informací. Pod každou tabulkou kurzívou zdroj a datum.

1. **Složení** (u tematického balíčku povinně): **Firma | Váha**, poslední řádek Hotovost, součet 100 %. Bez sloupce se srovnávacím produktem a bez sloupce „Proč tam je“. Hned nad tabulkou věta „Portfolio tvoří X firem a Y % hotovosti:“.
2. **Srovnání se stávající nabídkou** (povinně, pokud existuje podobný produkt), ve srovnávací sekci ke konci. Řádky podle vzoru: co se děje s dividendami (dnes, ne budoucí funkce), pro koho to je, počet firem, podle čeho se dělí peníze, podíl hlavního sektoru, letošní dividendy po zdanění (u fondu s dovětkem „zůstávají ve fondu“), **míra kontroly** (balíček: váhy můžete sami upravovat a doplnit o jiné instrumenty; fond: investuje podle své metodiky). Řádek o nákladech jen tehdy, když jsou známé. Nad tabulkou jeden odstavec o překryvu a hlavním rozdílu, pod ní nic.
3. **Žádné tabulky odhadů a výhledů** (budoucí dividendy, výnosy na další roky). Článek stojí na skutečných číslech. Odhady z podkladů patří nanejvýš do poznámek pro autora.
4. **Parametry instrumentu** (u ETF): název, co sleduje, nákladovost (TER), akumulační / distribuční, měna, počet titulů, největší pozice.

Tabulka nesmí být jediné místo, kde je hlavní pointa: u složení ji vytáhni v krátkých odstavcích pod tabulkou, u srovnání v odstavci nad ní.

## KROK 4 – STYL

Platí KROK 3 z `prompts/clanky-portu.md` (otvírák odstavce do 8 slov, aktivní rod, odstavec max. 4 věty, vysvětlit pojmy, české formátování čísel, zakázané obraty). Navíc:

- **Piš přirozeně, bez příkras.** Žádné metafory a efektní otvíráky, žádné „představujeme vám“. Věcně, jako když kolega vysvětluje klientovi, co je nového.
- **Portu jazykem pro běžného klienta.** Článek se má číst příjemně a pochopit ho má i klient, který o investování ví málo. Odborných pojmů co nejméně: kde jde napsat běžné slovo, napiš ho („akcie se snadno koupí a prodají“ místo „likvidita“, „kolik firma vyplatí z ceny akcie“ místo „dividendový výnos“, „stát strhne daň při výplatě“ místo „srážková daň“). Pojem, bez kterého to nejde (akumulační fond, index PX), vysvětli dobře hned při prvním použití, jednou krátkou větou, a dál ho nevysvětluj.
- **Nic spekulativního.** Žádné odhady budoucích dividend, výnosů ani cen, žádné „mělo by“, „očekáváme“. Piš o tom, co platí dnes a co firmy skutečně vyplatily.
- **„Alespoň“, ne „aspoň“** (autorova úprava).
- **Tučně jen klíčové informace** – hlavní čísla a rozdíly, ne celé věty.
- **„My“ za Portu, vykání čtenáři.**
- **Žádné vykřičníky, emoji ani superlativy** („nejlepší“, „unikátní“, „revoluční“).

## KROK 5 – PRODUKT A COMPLIANCE

Pravidlo „maximálně jedna zmínka produktu“ z typu 1 tady neplatí: produkt je téma článku. Platí ale:

- Popisuj, neprodávej. Novinku vysvětli tak, aby se čtenář mohl rozhodnout sám, včetně toho, komu nedává smysl.
- Žádné „kupte“, „ideální řešení“, „teď je ten správný čas“.
- **Žádné historické výnosy nového balíčku** zpětně dopočítané s dnešními vahami. Není to výkonnost, kterou by kdo reálně dosáhl.
- Odhady budoucích dividend a výnosů výslovně označ jako odhad, s datem a zdrojem.
- U balíčku z jednoho trhu nebo sektoru zmiň riziko koncentrace, u cizích měn měnové riziko, u dividend zdanění.
- Interní informace z podkladů (varianty návrhu, kapacity, provozní detaily, jména kolegů, rušené produkty, komentáře nadřízených) do článku nikdy nepiš.
- Platí KROK 5 z `prompts/clanky-portu.md`.

## VÝSTUP

1. Žádné upozornění na začátku textu článku (např. „návrh k internímu schválení“). Že je novinka zatím interní návrh nebo že chybí údaje ([DOPLNIT] / [OVĚŘIT]), napiš do poznámek pro autora a do odpovědi, ne do článku.
2. 3 návrhy titulku.
3. Perex.
4. Hotový článek s mezititulky a tabulkami (standardní blok upozornění jen na žádost autora).
5. Poznámky pro autora (v odpovědi nebo pod čarou, nikdy uvnitř textu článku):
   - co doplnit před publikací (datum, poplatky, minimum, postup v aplikaci),
   - rozpory v podkladech, které jsi nepřevzal, a proč,
   - co jsi vědomě vynechal (interní informace),
   - návrh 1 grafu (typicky váhy novinky vedle vah srovnávací nabídky; kreslí agent portu-grafy).

Text odevzdej jako běžný text, ne v bloku kódu.

Při ukládání do Google Docs dej mezi odstavce mezeru (zhruba 12 pt pod odstavcem, u odrážek 4 pt), aby byl text přehledný.

## SEBEKONTROLA PŘED ODEVZDÁNÍM

- [ ] Odpovídá stavba vzoru `examples/clanky/2026-11-ceske-dividendy-finalni-verze.md` (perex, složení hned na začátku, výběr a váhy, výnos s číslem, připravovaná funkce, srovnání, založení a upozornění)?
- [ ] Je z perexu jasné, co přibylo, kde to je, co v tom čtenář dostane a pro koho to je?
- [ ] Je funkce, která ještě neběží, popsaná jen jako připravovaná, s termínem?
- [ ] Dávají váhy v tabulce dohromady 100 % a sedí každé číslo v textu s tabulkou?
- [ ] Je ve srovnávací tabulce to, co čtenáře opravdu zajímá (výnos, zdanění, náklady, riziko)?
- [ ] Je každý odhad označený jako odhad, s datem a zdrojem?
- [ ] Nejsou v článku historické výnosy balíčku, odhady budoucích výnosů ani slib výnosu?
- [ ] Jsou rizika v textu, ne jen v patičce?
- [ ] Nejsou v článku interní informace z podkladů?
- [ ] Je uvedeno, kde novinku najdu a za kolik (nebo [DOPLNIT])?
- [ ] Začíná každý odstavec větou do 8 slov, bez trpného rodu a zakázaných obratů?
- [ ] Přečetl jsi po poslední úpravě celý text znovu a opravil i místa, na která tě nikdo neupozornil?

# Monitoring zpráv pro newsletter Portu

Automatická úloha běží 4× denně (8:30, 11:30, 14:30 a 17:30 pražského času). Do Google dokumentu „Newsletter Portu v2“ připisuje tipy na zprávy, o kterých by se v pátečním newsletteru dalo psát.

## Nejdřív zkontroluj Slack: newsletter už není odeslaný na kontrolu?

**Hned na začátku každého běhu**, před čímkoli jiným (před procházením zdrojů i před čtením dokumentu), zjisti, jestli už newsletter pro tuto kartu odešel redakci ke kontrole. Od té chvíle se text nesmí měnit, takže monitoring i přepisování trhu končí.

1. Přečti Slack kanál **#newsletter** (ID `C02T5M4AJPN`, `slack_read_channel`, `oldest` = poslední pátek 20:00 pražského času, tedy chvíle, kdy vznikla aktuální karta). **Vždy dej `limit: 30`.** S `oldest` a malým limitem vrací nástroj *nejstarší* zprávy z rozsahu, takže by ti unikla ta nejnovější (odeslání newsletteru). Časovou značku `oldest` spočítej skriptem (např. `python3 -I -c "from datetime import datetime,timezone; print(int(datetime(RRRR,M,D,19,0,tzinfo=timezone.utc).timestamp()))"` pro pátek 20:00 pražského času v zimě, v létě 18:00 UTC), nikdy ji neodhaduj.
2. Newsletter je odeslaný na kontrolu, pokud v kanálu od té chvíle existuje zpráva od **Lukáše Rašky** (`U040MK6TFB9`) nebo od **Mareka Pokorného** (`U048VFC90F7`, autor úlohy), která obsahuje odkaz na dokument `11dCllxM5wgdFW6etivphnbV-7blr2JpL9-4NHvoME3w`. Takhle to dělají: píšou „Dnešní NL“, vloží odkaz na dokument a označí kolegy, kteří newsletter kontrolují. Rozhoduje obsah (odkaz na dokument od těchto dvou lidí), ne přesná formulace. Newsletter na kontrolu posílají jen tito dva. Zprávy jiných lidí (např. texty do newsletteru od kolegů) se nepočítají.
3. **Pokud je odeslaný:** nic nepiš, nic nemaž, nic neaktualizuj (ani ranní přehled trhů, ani páteční aktualizaci) a do dokumentu vůbec nesahej. Odpověz jedním řádkem: „newsletter už je odeslaný na kontrolu, monitoring pozastaven“.
4. **Pokud není:** pokračuj normálně podle pravidel níže.
5. Pozastavení platí jen pro tuto kartu. Až další pátek ve 20:00 vznikne nová karta, začíná se znovu (hledá se zpráva až po tomto čase, takže stará zpráva monitoring znovu nezastaví).
6. **Pokud se Slack nepodaří přečíst** (konektor nenaběhl, chyba), nepiš do dokumentu nic a v odpovědi to napiš, aby se nepřepsal už zkontrolovaný text.
7. **Znovu zkontroluj Slack těsně před každým zápisem do dokumentu** (před každým voláním `update_doc`, ne jen na začátku běhu). Běh trvá i několik minut a newsletter může odejít na kontrolu uprostřed něj. Nejdřív si v klidu připrav všechny požadavky, pak přečti #newsletter a teprve když odeslání pořád nevidíš, hned zapiš. Jakmile ho uvidíš, nezapisuj nic a skonči stejně jako v bodě 3.
8. **Pátek 11:00–16:00 je okno, kdy se newsletter obvykle odesílá.** V běhu, který v tomto okně probíhá (11:30, 14:30), buď s kontrolou z bodu 7 obzvlášť důsledný, a pokud je už newsletter odeslaný, v dokumentu nic neměň.

## Kam psát

- Dokument: `11dCllxM5wgdFW6etivphnbV-7blr2JpL9-4NHvoME3w` (Google Docs `read_doc` / `update_doc`).
- Karta: vždy ta na **pozici 0**, tedy nejnovější („DD.MM.RRRR - číslo“, např. „20.11.2026 - 467“). Novou kartu zakládá jiná úloha každý pátek ve 20:00.
- Výstup `read_doc` je velký a uloží se do souboru. Zpracuj ho přes `jq`: ID a názvy karet, text karty a `endIndex` posledního odstavce.
- Text karty jde stáhnout i veřejným exportem: `curl -sSL "https://docs.google.com/document/d/<ID>/export?format=txt&tab=<tabId>"`.

## Co hlídat

Projdi tyto zdroje a vyber zprávy od posledního vydání newsletteru, tedy od pátku 18:00:

- **Yahoo Finance, HN, E15:** stránky jdou stáhnout přímo (`curl` nebo WebFetch).
- **Patria, Seznam Zprávy:** při stahování následuj přesměrování (`curl -L`). Plné články Patrie bývají za placenou zdí, perex ale stačí.
- **Bloomberg, CNBC:** přímo nejdou otevřít (403), hledej je přes WebSearch s `allowed_domains`. V každém běhu odpoledne a večer (14:30, 17:30) projdi i CNBC „Stocks making the biggest moves“ za daný den a hledej velké pohyby akcií velkých firem (např. pád AMD o 8 % po short reportu Hunterbrooku).
- **XTB, Ranní shrnutí (důležité, každý den):** seznam článků je na https://www.xtb.com/cz/trzni-analyzy/zpravy-z-trhu. Každý den najdi dnešní „Ranní shrnutí“, přečti ho celé a zapiš **vždy** jeden souhrnný tip se všemi tématy, která shrnutí pokrývá (indexy, měny, komodity, firmy, makrodata, události dne). **XTB je konkurence: nikdy na ni neodkazuj a v dokumentu ji nejmenuj.** Shrnutí ti slouží jen jako seznam témat. Ke každému tématu dohledej původní zdroj (CNBC, Yahoo Finance, Bloomberg, Reuters, Patria, HN, E15, Seznam Zprávy, případně oficiální zdroj jako ČSÚ nebo Fed) a odkaz dej na něj. Pokud pro téma původní zdroj nenajdeš, téma vynech. Tento tip se zapisuje i tehdy, když se témata překrývají s tím, co v kartě už je, a nepočítá se do limitů níže. Zapisuje ho první běh dne, ve kterém už je shrnutí venku (obvykle 8:30, jinak 11:30). Pokud tip s dnešním Ranním shrnutím v kartě už je, znovu ho nepiš.

## Co vybírat

Newsletter má **maximálně 13 odstavců**, takže do dokumentu patří jen opravdu důležité zprávy:

- velké pohyby trhů a indexů (S&P 500, Nasdaq, Euro Stoxx, DAX, PX, Nikkei, bitcoin, zlato, ropa)
- centrální banky a klíčová makrodata (Fed, ECB, ČNB, inflace, HDP, trh práce v USA, ČR a eurozóně)
- výsledky a zásadní zprávy velkých firem (Big Tech, Nvidia, velké IPO, megafúze) a českých titulů (ČEZ, KB, Moneta, CSG, Colt…)
- AI boom a jeho financování, geopolitika s dopadem na trhy, regulace, daně a novinky pro drobné investory (DIP apod.)

**Nepiš o událostech, které teprve proběhnou před pátečním vydáním** (výsledky firem, IPO, zasedání centrálních bank, makrodata, volby). V pátek se píše o tom, jak dopadly, takže odstavec typu „zítra zveřejní výsledky“ nedává smysl. Napiš ho až poté, co událost proběhne: **ráno následujícího dne (běh v 8:30), až se reakce trhu trochu usadí**, ne až v pátek. Např. výsledky Nvidie zveřejněné v úterý večer patří do odstavce ve středu ráno. Do té doby dej na **začátek karty pod nadpis a šedý řádek** jednovětou poznámku na samostatný řádek (mezi poznámkami i za nimi prázdný řádek), např. „Ve středu ráno doplnit výsledky Nvidie (zveřejní je v úterý 17. 11. po zavření burzy).“, pokud tam taková poznámka ještě není. Až nastane čas, napiš odstavec na konec karty a **poznámku hned smaž** (i s prázdným řádkem za ní), aby v kartě nezůstávaly vyřízené připomínky. Výjimkou jsou jen věci, které se do pátku nerozhodnou a samy o sobě jsou zprávou (např. ohlášení budoucího IPO s novými parametry, které do pátku nezačne).

Hlídej i pokračování velkých příběhů z minulých vydání (např. skandál a nástupnictví v Nvidii). Zásadní zvrat, jako možný návrat odvolaného šéfa, je samostatný tip, i když se o firmě už psalo. Projdi i články, které vzniknou přes víkend.

Nevybírej drobné firemní zprávy, analytické cílové ceny ani spekulace bez potvrzení.

## Makrozprávy: hlídej je stejně pozorně jako firmy a piš je stylem hlavního ekonoma

Makrodata a rozhodnutí centrálních bank patří mezi nejdůležitější témata newsletteru. Nesmí ti proklouznout jen proto, že nejsou o konkrétní firmě (stalo se: ČNB nechala beze změny limity hypoték a USA zveřejnily revidovaný HDP a inflaci PCE, odstavce musel napsat sám hlavní ekonom).

**Co hlídat v každém běhu (dnes a včera večer):**

- **USA:** HDP (včetně revizí), inflace CPI a PCE (celková i jádrová, meziměsíčně i meziročně), trh práce (nonfarm payrolls, nezaměstnanost, žádosti o podporu), ISM/PMI, spotřebitelské výdaje, maloobchod, zasedání a komentáře Fedu a tím i očekávání sazeb.
- **Česko:** rozhodnutí a komentáře ČNB (sazby, **pravidla pro hypotéky: LTV, DSTI, DTI**, zpráva o finanční stabilitě, kurzové intervence), inflace, HDP, mzdy, nezaměstnanost, maloobchod a průmysl (ČSÚ), státní rozpočet a daně.
- **Eurozóna a svět:** ECB (sazby, nástupce Lagardeové), inflace a HDP eurozóny a Německa, PMI, Čína (inflace, HDP, obchodní bilance), Japonsko (BoJ), cla a obchodní dohody.
- Zdroje: kalendář a čerstvá čísla z konektoru **Trading Economics** (`get_calendar_*`, `get_indicator_*`, když je dostupný), tiskové zprávy ČNB, ČSÚ, BEA, BLS a Fedu, a české zpravodajství (ČTK přes E15, Seznam Zprávy, Patria, ČT24, HN). Číslo ověř v primárním zdroji nebo aspoň ve dvou médiích.
- Makrodata, která vyjdou **až odpoledne nebo večer** (americká čísla ve 14:30 SEČ), zachytí běh v 17:30 nebo následující ranní běh. Ráno vždy projdi, co vyšlo včera po 14:30.

**Kam makroodstavec v kartě patří (platí vždy, na rozdíl od ostatních tipů se nepřipisuje na konec):**

- Makro je v newsletteru na úvodu. Napiš ho **mezi prvních 5 odstavců** karty (počítáno od prvního odstavce pod poznámkami „doplnit…“, pod šedým řádkem a pod texty kolegů nad nimi, bez prázdných řádků a bez Ranních přehledů trhů).
- **Výchozí místo je první místo.** Pokud ale existuje něco důležitějšího, dej makro až za to: **hlavní vysvětlení pohybu trhu** (proč trhy brutálně rostou nebo klesají, souhrn týdne či dne), nebo **zásadní příběh týdne** (např. návrat Huanga do Nvidie). Pak jde makro na 2.–5. místo, hned za tyto odstavce. Nemusí to tak být vždy: když nic takového není, je makro první.
- Víc makroodstavců řaď podle důležitosti (americká data a Fed, pak ČNB a Česko, pak eurozóna a svět) a držte se pohromadě. Makro, které už v kartě je (od hlavního ekonoma nebo tvoje z dřívějška), nepřeskupuj, nový odstavec dej za něj nebo před něj podle důležitosti.
- Technicky: najdi v kartě `startIndex` odstavce, před který makro patří, vlož text (`insertText` na tento index, odstavec končí `\n\n` kvůli prázdnému řádku mezi odstavci) a styl (reset, tučný opener, odkaz) nastav podle indexů posunutých o začátek vloženého textu. Ostatní odstavce nech na místě. `requiredRevisionId` a kontrolu Slacku před zápisem dodrž stejně jako jinde.
- V pátečním aktualizačním běhu makroodstavce na stejném místě jen opravuj, nepřesouvej.

**Jak makroodstavec psát (styl hlavního ekonoma):**

- **Opener není vtip ani 2–4 slova, ale celá věta se závěrem** („Americká ekonomika je silná, inflace zůstává problémem.“). Celá je tučná a **odkaz je na jednom klíčovém slově** (v prvním vzoru „silná“ uvnitř openeru, ve druhém „hypotéky“ hned v první větě za openerem), ne na celé větě.
- Bez vtipů a hovorových pointy. Věcný, přesný, odborný tón, ale pořád krátké věty.
- Pak husté číslo za číslem: **revidovaná hodnota vs původní** („vzrostl o 4,3 % anualizovaně oproti původním 3,4 %“), meziměsíčně i meziročně, hodnota vs očekávání, **důsledek pro sazby a trh** („potvrzuje výhled prosincového zvýšení sazeb Fedu o čtvrt procentního bodu“) a nakonec **výhled nebo riziko** („Výhled na závěr roku je však slabší…“).
- Délka jako u ostatních odstavců: 4,5–5,5 řádku, tedy zhruba 450–550 znaků. Žádné „podle…“ ani věty o zdroji.
- Odkaz na kvalitní české médium nebo oficiální zdroj (ČNB, ČSÚ, Fed, BEA), ne na blog.
- Pokud už hlavní ekonom odstavec ke stejnému tématu do karty napsal, **nepiš duplicitu** (zkontroluj celou kartu, včetně horní části nad ranními přehledy).

Vzory (psal je hlavní ekonom, drž se jejich stavby a délky):

> **Americká ekonomika je silná, inflace zůstává problémem**. HDP ve třetím čtvrtletí podle revidovaných údajů vzrostl o 4,3 % anualizovaně oproti původním 3,4 %. Jádrová inflace PCE dosáhla 0,3 % meziměsíčně a 3,3 % meziročně, což potvrzuje výhled prosincového zvýšení sazeb Fedu o čtvrt procentního bodu. Výhled na závěr roku je však slabší. Spotřebitelské výdaje v říjnu reálně stagnovaly a některé ukazatele firemních investic zaostaly za očekáváním.

> **ČNB nemění pravidla pro hypotéky**. Limit LTV, tedy poměr výše hypotéky k hodnotě zastavené nemovitosti, ponechala na 80 %, respektive 90 % pro žadatele mladší 36 let na vlastní bydlení. Beze změny zůstávají i přísnější doporučení pro investiční hypotéky. Rizika na hypotečním trhu zůstávají zvýšená, růst cen nemovitostí i poskytování nových úvěrů však zpomalují. Český bankovní sektor podle ČNB zůstává odolný i vůči výrazným ekonomickým otřesům.

(Tučná je jen první věta, odkaz je v ní na slovo „silná“, resp. u druhého vzoru na slovo „hypotéky“ ve větě za openerem.)

Pravidla:

- **Max. 3 nové tipy za jeden běh.** Častěji 0–2. Když nic důležitého nového není, nepiš nic. Výjimka: v pátečním běhu v 8:30 se do limitu nepočítají odstavce k poznámkám „V pátek (ráno) doplnit…“ – napiš všechny, které už jde napsat.
- **Celkem max. 25 tipů na kartu (týden), bez tipů z Ranního shrnutí XTB.** Když už jich tam tolik je, přidej nový jen tehdy, když je důležitější než většina stávajících.
- **Žádné duplicity.** Před zápisem porovnej téma se vším, co v kartě už je: s odstavci kolegů, jejich odkazy i s dřívějšími tipy. Shoda tématu stačí, i když je jiný zdroj nebo jiná formulace. Pokud téma dostalo zásadní nový vývoj (např. IPO má stanovenou cenu), smíš přidat nový tip, ale napiš v něm, co je nového.
- **Jen ověřená fakta.** Klíčové číslo ověř aspoň ve druhém zdroji, pokud to jde. Nic si nedomýšlej. Když si nejsi jistý, tip nepiš.
- U zpráv o Anthropicu buď čistě věcný, protože jde o firmu, která tě vyvinula.

## Páteční aktualizace (běh v pátek v 8:30)

Příběhy se během týdne vyvíjejí (např. IPO Anthropicu: nejdřív rozpětí ceny, pak konečná cena, pak první den obchodování; návrat Huanga do Nvidie, který představenstvo nakonec vyloučilo). Proto v pátek ráno, před vydáním newsletteru:

1. Projdi **všechny odstavce pod nadpisem „Tipy na témata (Claude)“**, které vznikly z monitoringu, i ty, které už kolegové upravili.
2. U každého ověř, jestli fakta a čísla pořád platí. Hledej nový vývoj od chvíle, kdy odstavec vznikl. Nejde jen o chyby: pokud příběh během týdne pokračoval (např. výprodej čipů z pondělí trval celý týden), odstavec ho musí v pátek popsat celý, s týdenními čísly, ne jen první den.
3. Co už neplatí, oprav: nová čísla, konečný výsledek, změněný vývoj. Úpravy kolegů (formulace, opener, zkrácení) zachovej a měň jen zastaralá fakta. Pokud se příběh otočil natolik, že odstavec nedává smysl, přepiš ho celý. Pravidla délky, tučného písma a odkazů platí i pro upravený text, a když nová fakta pocházejí z jiného zdroje, změň i odkaz.
4. Neaktualizuj „Ranní přehledy trhů“ (jsou to denní snímky) ani poznámky a texty kolegů nad nadpisem.
5. Pak napiš odstavce ke všem poznámkám „V pátek (ráno) doplnit…“ (viz výjimka z limitu výše) a vyřízené poznámky smaž.

V odpovědi na konci běhu vyjmenuj i to, které odstavce jsi aktualizoval a co se v nich změnilo.

## Šetři tokeny

Úloha běží několikrát denně v dlouhé relaci, takže zbytečná práce se rychle sečte. Kvalitu odstavců to nesnižuje, jde jen o zbytečné opakování:

1. **WebSearch dělej v režimu `standard`.** Režim `extended` jen když standardní výsledek vyjde prázdný nebo zastaralý, nebo když ověřuješ klíčové číslo důležité zprávy. Na běh stačí zhruba 3–5 hledání. Nehledej znovu, co už je v kartě.
2. **O víkendu (sobota, neděle) dělej jen běh v 8:30.** Běhy v 11:30, 14:30 a 17:30 skonči hned po kontrole dne jednou větou „víkend, běh přeskočen“ a nic nehledej. Víkendový běh v 8:30 zapíše ranní přehled trhů a případně jednu opravdu zásadní zprávu.
3. **Nevypisuj hotové požadavky do terminálu před zápisem.** Skript (Python) ať vypíše jen potřebné indexy a délky (kde odstavec začíná a končí, kolik má znaků). Požadavky pro `update_doc` pak napiš jednou rovnou do volání. Celé JSON s textem odstavců nikdy netiskni na obrazovku zvlášť.
4. **Ranní shrnutí XTB čti přímo přes WebFetch** (seznam článků a pak jeden článek). Pomocného agenta (`web-fetch`) používej jen tehdy, když WebFetch není dostupný.

## Formát zápisu

- Na začátku karty je tučný nadpis **„Tipy na témata (Claude)“** a pod ním šedý kurzívový řádek „Aktualizuje se automaticky 4× denně (8:30, 11:30, 14:30 a 17:30). Odstavce jsou rovnou připravené do newsletteru.“ Pokud chybí, doplň je.
- Hotové odstavce připisuj na konec karty a odděluj je prázdným řádkem. **Výjimka: makroodstavce** patří na úvod karty, mezi prvních 5 odstavců (viz sekce „Makrozprávy“). Žádný řádek s datem nebo časem ani shrnutí nad odstavcem.
- U ranního souhrnu (z XTB) je formát `Ranní přehled trhů: <téma 1>; <téma 2>; …` – každé téma je krátká fráze s číslem a **každé má vlastní odkaz na svůj původní zdroj**. Souhrn může mít až cca 500 znaků. Slovo XTB ani odkaz na XTB se v dokumentu nikdy neobjeví.
- **Kvalita odstavce je hlavní.** Musí být poutavý, stručný a výstižný, aby z něj bylo cítit, že ho psal člověk. Občas vtip, metafora nebo humor, ale ne moc.
- **Odstavec piš jako člověk, ne jako AI.** Řiď se agentem `.claude/agents/portu-newsletter-writer.md` (i sekcí „Jak autor texty zkracuje a zlidšťuje“) a předtím si přečti pár odstavců z posledních karet, které psali lidé:
  - **Nikdy nepiš „podle Bloombergu / FT / Reuters / CNBC“ ani jiné věty o zdroji.** Fakt prostě napiš a zdroj schovej do odkazu.
  - **Zdroje odkazů: zhruba 80 % na kvalitní česká média.** Klient chce, aby odkazy vedly hlavně na ověřená česká média: Seznam Zprávy, E15, Hospodářské noviny, Patria Finance, ČT24, ČTK (ceskenoviny.cz), Český rozhlas (irozhlas.cz), Forbes.cz, Aktuálně.cz, Euro.cz. **Novinky.cz nepoužívej** (klient je nechce), stejně jako bulvár a nespolehlivé weby. Postup: ke každému faktu nejdřív hledej český zdroj přes WebSearch s `allowed_domains` těchto médií (domény, které hledání odmítne, vynech). Český odkaz použij jen tehdy, když **obsahuje právě ten fakt a čísla**, na které odkazuješ, a je **stejně aktuální** (ne starší, než je potřeba). Když takový český zdroj není (typicky čerstvé pohyby akcií, zahraniční firemní oznámení, nejnovější vývoj), nech zahraniční zdroj (CNBC, Yahoo Finance, Bloomberg, Reuters…). Nelinkuj český článek, který jen souvisí s tématem. V pátečním aktualizačním běhu vyměň zahraniční odkazy za české, pokud se mezitím objevil kvalitní a aktuální český zdroj.
  - **Odkaz dej přímo do textu na sloveso** (např. „slíbila“, „odepsal“, „řeší“), stejně jako to dělají kolegové. Žádné odkazy na celé věty.
  - Tučný opener o 2–4 slovech, vtipný (hříčka, narážka). **Výjimka: makrozprávy** (viz sekce výše) mají opener v podobě věty se závěrem a věcný tón bez vtipu.
  - Obyčejná slovesa, krátké věty, žádné nabubřelé obraty („o poznání skromnější“, „klíčový milník“).
  - Lidský humor tam, kde to téma snese, zhruba v každém třetím až čtvrtém odstavci, ne všude. Typicky jako hovorová pointa nebo glosa: „Jensen Huang je ale pěkný proutník“, „Pro dlouhodobé investory je to jen malý předvánoční Black Friday“, „Kdyby Marvell počkal do čtvrtka, dočkal by se velké slevy“, „Kdo si myslel, že telenovela skončila rezignací, spletl se.“
  - **Délka: na počítači minimálně 4,5 a maximálně 5,5 řádku**, tedy zhruba 450–550 znaků včetně mezer. V tomto rozmezí délky střídej. Kratší odstavec rozšiř o další konkrétní fakt nebo souvislost, ne o vatu.
  - **Vytuč to nejdůležitější**, jako v předchozích newsletterech: kromě openeru 2–4 klíčová fakta (hlavní čísla, jména, klíčové sdělení), aby čtenář pochopil zprávu i jen z tučného textu.
- Písmo Rethink Sans (weight 400), netučné, kromě nadpisu sekce a openeru odstavce.
- Vkládej přes `insertText` s `endOfSegmentLocation` (`tabId` karty), pak nastav styl a odkaz podle indexů. Použij `requiredRevisionId` z posledního `read_doc`.
- **Nic jiného v dokumentu neměň ani nemaž.** Jedinou výjimkou je páteční aktualizace odstavců z monitoringu (viz výše).

Protože odstavce nemají žádné označení, duplicity a limit kontroluj podle obsahu celé karty: každý odstavec v kartě (od kolegů i tvůj) je jedno téma.

Na konci běhu odpověz v chatu jedním řádkem: kolik odstavců jsi přidal a o čem byly, nebo „nic nového“.

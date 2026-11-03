// Pomocný materiál k prezentaci Ekonomika a trhy – listopad 2026 (Word)
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, LevelFormat,
  Footer, PageNumber, BorderStyle,
} = require("docx");

const OUT = process.argv[2];
const GREEN = "0F3738", RED = "EE4F46", GRAY = "5F6B6B";

const slides = [
  {
    n: 1, title: "Ekonomika a trhy", min: "0,5 min",
    msg: "Úvod",
    say: [
      "Dobrý den, děkuji za pozvání. Za WOOD & Company vás dnes provedu tím, co se na finančních trzích stalo za poslední měsíc a co to znamená pro investice vašich klientů.",
      "Uplynulé týdny byly hodně rušné. Ropa byla nejdražší za čtyři roky, technologické akcie prošly výprodejem, centrální banky řešily, jestli dál zvyšovat sazby, a v USA se právě volilo do Kongresu. Projdeme si, co se stalo, proč se to stalo a co z toho plyne pro dlouhodobého investora.",
      "Zabere to zhruba dvacet minut a na konci rád odpovím na vaše dotazy.",
    ],
    reserve: [],
  },
  {
    n: 2, title: "Co se stalo od začátku října", min: "2 min",
    msg: "Měsíc rekordů, výprodeje technologií a nadějí na mír",
    say: [
      "Začnu časovou osou, protože za poslední měsíc se toho stalo opravdu hodně a jednotlivé události na sebe navazují.",
      "Šestého října byly americké akcie na historickém maximu. Index S&P 500 i technologický Nasdaq zapsaly rekord a nálada na trzích byla velmi dobrá.",
      "Zároveň ale dál zdražovala ropa. Dvacátého třetího října byla ropa Brent nejdražší za čtyři roky, protože trh se bál, že Spojené státy znovu zaútočí na Írán a omezí se dodávky z Perského zálivu.",
      "Na konci října zasedaly centrální banky. Americký Fed i Evropská centrální banka nechaly sazby beze změny, daly ale najevo, že zvyšování sazeb nemusí být u konce.",
      "Ve stejných dnech zveřejnili výsledky technologičtí giganti. Čísla měli dobrá, přesto jejich akcie výrazně zlevnily. Trh je potrestal hlavně za to, kolik peněz utrácejí za umělou inteligenci. Za chvíli vysvětlím proč.",
      "Druhého listopadu se objevila naděje na dohodu mezi USA a Íránem a ropa za jediný den výrazně zlevnila. Hned následující den, třetího listopadu, ale USA znovu udeřily na Írán. Ve stejný den se ve Spojených státech volilo do Kongresu.",
      "Poslední bod je ještě před námi. Sedmnáctého listopadu zveřejní výsledky Nvidia, největší výrobce čipů pro umělou inteligenci, a tím výsledková sezóna za třetí čtvrtletí v podstatě skončí. Zatím je velmi silná: 82 procent firem překonalo odhady analytiků.",
      "Dnes tedy projdeme, jak se dařilo trhům, co se děje s energiemi a se sazbami, jak dopadly výsledky firem a proč klesaly technologie, co se stalo s dluhopisy, a na konci se podíváme na výhled.",
    ],
    reserve: [
      "S&P 500: historické maximum 7 844,67 bodu 6. 10. 2026 (Trading Economics).",
      "Brent: 116,72 USD 23. 10. 2026, nejvýš za čtyři roky (Trading Economics).",
      "Nvidia zveřejní výsledky 17. 11. kolem 22:20 SEČ, konferenční hovor ve 23:00 SEČ (oznámení Nvidie).",
      "Výsledková sezóna k 30. 10.: výsledky má 60 % firem z S&P 500, 82 % z nich nad odhady zisků (FactSet).",
    ],
  },
  {
    n: 3, title: "USA rostou navzdory poklesu technologií", min: "2,5 min",
    msg: "Výprodej zasáhl technologie a AI infrastrukturu, široký americký trh drží",
    say: [
      "Na tomto slajdu je výkonnost hlavních akciových indexů za poslední měsíc, za tři měsíce a od začátku roku. Šedý sloupec je výnos v místní měně, červený výnos v korunách, tedy to, co skutečně vidí český investor.",
      "Za poslední měsíc je hlavní příběh jasný. Výprodej zasáhl technologie a firmy napojené na infrastrukturu pro umělou inteligenci, tedy výrobce čipů, pamětí a datových center. Technologický index Nasdaq 100 ztratil zhruba 9 procent a dostal se do takzvané technické korekce, tedy víc než 10 procent pod svůj rekord. Podobně ztratilo Japonsko, kde je hodně firem napojených na výrobu čipů.",
      "Důležité ale je, že široký americký trh drží. Index S&P 500 ztratil jen kolem 2 procent a Dow Jones, ve kterém je technologií méně, za měsíc dokonce mírně přidal. Pražská burza byla za měsíc také v plusu, protože technologické firmy v ní téměř nejsou.",
      "Za tři měsíce a hlavně od začátku roku je obrázek pořád dobrý. Americké akcie jsou letos v korunách zhruba o 16 procent výš, Nasdaq 100 o 17 procent a japonské akcie dokonce o víc než 30 procent. Evropa přidala kolem 7 procent. Pražská burza je od začátku roku mírně v minusu.",
      "Pro korunového investora hraje roli i kurz. Za poslední měsíc se koruna vůči dolaru skoro nepohnula, takže výnos v korunách je prakticky stejný jako v dolarech. Od začátku roku ale dolar vůči koruně posílil zhruba o 6 procent, a to výnos amerických akcií v korunách výrazně zvýšilo.",
    ],
    reserve: [
      "Měsíc (2. 10.–2. 11.), místní měna / CZK: S&P 500 −2,4 / −2,2 %; Dow Jones +1,6 / +1,8 %; Nasdaq 100 −9,2 / −9,0 %; Euro Stoxx 50 −1,0 / −1,4 %; Nikkei 225 −7,7 / −7,5 %; PX +0,8 %.",
      "3 měsíce (31. 7.–2. 11.): S&P 500 +0,7 / +4,2 %; Dow Jones −0,9 / +2,5 %; Nasdaq 100 −1,0 / +2,5 %; Euro Stoxx 50 −2,8 / −2,4 %; Nikkei 225 −2,0 / +1,1 %; PX −2,6 %.",
      "Od začátku roku (31. 12. 2025–2. 11. 2026): S&P 500 +10,2 / +16,4 %; Dow Jones +8,2 / +14,3 %; Nasdaq 100 +10,8 / +17,1 %; Euro Stoxx 50 +6,7 / +7,4 %; Nikkei 225 +25,3 / +31,4 %; PX −1,9 %.",
      "USD/CZK: 20,58 (31. 12. 2025) → 21,74 (2. 11. 2026), +5,7 %. Zdroj: Trading Economics, zavírací ceny.",
    ],
  },
  {
    n: 4, title: "Naděje na dohodu stáhly ropu ke 100 USD", min: "3 min",
    msg: "Ropa je ale pořád o 42 % dražší než před válkou",
    say: [
      "Teď k ropě, která je pro inflaci a sazby asi nejdůležitější proměnnou.",
      "Graf ukazuje cenu ropy Brent od začátku roku. Na konci února, těsně před začátkem války s Íránem, stál barel 73 dolarů. Pak cena prudce vyskočila a od té doby se drží vysoko. Tento týden ropa zlevnila zhruba ke 100 dolarům, protože se objevila naděje na dohodu.",
      "Jak je to s Hormuzským průlivem, kterým za normálních okolností odtéká velká část ropy z Perského zálivu? Průliv není zavřený, ale ani volný. Tankery plují s doprovodem amerického námořnictva a Írán na lodě dál útočí. Podle dat společnosti Kpler teklo průlivem na konci září asi 80 procent předválečného objemu ropy a paliv. Samotná ropa už byla zhruba na normální úrovni, paliv, tedy nafty, benzinu nebo leteckého paliva, ale jen asi pětina. Svět se navíc naučil průliv obcházet: asi 40 procent ropy z Perského zálivu dnes jde ropovody mimo Hormuz, před válkou to bylo 17 procent.",
      "Trh přitom reaguje na každé slovo z Washingtonu a Teheránu, protože prezident Trump střídá hrozby s nabídkami jednání. V pondělí druhého listopadu íránský nejvyšší vůdce povolil vládě jednat o ukončení konfliktu a Trump řekl, že Írán chce dohodu. Ropa za jediný den zlevnila o 7,6 procenta. V noci na úterý ale USA znovu udeřily na íránský ostrov Kešm v Hormuzském průlivu. Podle amerického ministra energetiky útok toky ropy neovlivnil a ropa se drží kolem 103 dolarů.",
      "I po tomto poklesu je ale ropa o 42 procent dražší než před válkou. Týká se to i plynu. Evropský plyn minulý týden poprvé od roku 2022 překonal 100 eur za megawatthodinu a zásobníky jsou před zimou naplněné výrazně méně než obvykle.",
      "Co to znamená? Drahé energie drží inflaci nahoře. V Evropě se dražší energie do cen pro domácnosti a firmy promítne hlavně v příštím roce, až dodavatelé přecení své ceníky.",
    ],
    reserve: [
      "Brent: 72,87 USD (27. 2., před válkou) → 116,72 USD (23. 10., maximum) → 104,77 USD (2. 11., −7,6 % za den) → kolem 103,4 USD (3. 11. odpoledne); od začátku roku zhruba +70 % (Trading Economics).",
      "Hormuz, Kpler podle CNBC (týdenní průměr k 28. 9. 2026): ropa 13,5 mil. barelů denně, tedy předválečná úroveň; paliva 0,68 mil. proti 3,6 mil. (19 %); celkem 14,2 mil. proti zhruba 17 mil. (asi 80 %). Mimo Hormuz jde asi 40 % ropy z Perského zálivu, před válkou 17 %.",
      "Za říjen spolehlivá čísla o objemech nejsou. Počty lodí z AIS (IMF PortWatch) jsou velmi nízké, ale nezachytí lodě s vypnutým vysílačem. Američtí představitelé uvádějí přes 10 mil. barelů denně, nezávislí analytici jsou opatrnější. Stav průlivu „omezený“ (hormuz.now, 3. 11.).",
      "Plyn TTF: minulý týden nad 100 EUR/MWh, 3. 11. kolem 91 EUR/MWh (+24 % za měsíc). Zásobníky EU 74,6 %, Německo 61 % proti cíli 70 % (2. 11., Trading Economics).",
    ],
  },
  {
    n: 5, title: "Sazby: pauza, ne konec zvyšování", min: "2 min",
    msg: "Fed i ECB v říjnu čekaly, trh počítá s dalším zvýšením",
    say: [
      "Drahé energie nás přivádějí k centrálním bankám.",
      "Americký Fed v září poprvé po třech letech zvýšil sazby. Na konci října je nechal beze změny v pásmu 3,75 až 4 procenta. Dva členové bankovní rady ale chtěli sazby zvýšit už teď a trh počítá s tím, že Fed přitlačí na prosincovém zasedání devátého prosince. Důvod je jednoduchý: americká ekonomika roste rychle a inflace drží nahoře.",
      "Evropská centrální banka nechala depozitní sazbu na 2,5 procenta. Šéfka ECB Christine Lagardeová ale přiznala, že se o zvýšení jednalo, a trh s ním dál počítá. Lagardeová navíc oznámila, že z čela banky odejde předčasně, takže ECB čeká změna ve vedení.",
      "Česká národní banka drží sazby na 3,75 procenta a rozhoduje už tento čtvrtek pátého listopadu. Analytici čekají zvýšení na 4 procenta. Celková inflace byla v září 2,5 procenta, tedy nedaleko cíle, rychle ale zdražují hlavně služby, a to centrální banku znepokojuje.",
      "Pro klienty to znamená, že sazby spíš ještě porostou, než že by klesaly. Pro konzervativní investory je to dobrá zpráva, protože dostanou vyšší úrok z vkladů a z nových dluhopisů. Pro drahé akcie je to naopak tlak, protože vyšší sazby snižují jejich atraktivitu.",
    ],
    reserve: [
      "Fed 28. 10.: 3,75–4,00 %, hlasování 10:2 (Cook a Hammack pro zvýšení) [ověřit ve statementu Fedu]. Trh přikládá zvýšení 9. 12. asi 75% pravděpodobnost (CME FedWatch podle Trading Economics, 2. 11.). HDP USA ve 3Q +3,4 % anualizovaně, ceny PCE v září +0,5 % za měsíc.",
      "ECB 29. 10.: depozitní sazba 2,50 %; trh čeká 2,73 % v prosinci a 3,23 % koncem roku 2027 (Trading Economics, 29. 10.).",
      "ČNB: 3,75 %, rozhodnutí 5. 11. ve 14:30, analytici čekají 4,00 % (ČTK). Inflace v září 2,5 %, jádrová přes 3 %, služby přes 4 %.",
    ],
  },
  {
    n: 6, title: "Zisky rostou, trh trestá sázky na AI", min: "2,5 min",
    msg: "Výsledková sezóna 3Q: 82 % firem nad odhady, zisky +30 %",
    say: [
      "Teď k výsledkové sezóně a k tomu, proč klesaly technologie, i když firmy vydělávají.",
      "Začnu výsledky. Do třicátého října zveřejnilo výsledky za třetí čtvrtletí 60 procent firem z indexu S&P 500 a 82 procent z nich překonalo odhady analytiků. Dlouhodobý průměr je přitom 78 procent, takže jde o nadprůměrně dobrou sezónu. Zisky firem rostou meziročně zhruba o 30 procent a je to už třetí čtvrtletí v řadě, kdy rostou o víc než 25 procent.",
      "Má to ale háček. Firmy překonávají odhady o méně než dřív. Trh je proto vybíravější a co nesplní velmi vysoká očekávání, to potrestá.",
      "Přesně to se stalo technologickým gigantům. Firmy jako Alphabet, Amazon, Meta nebo Microsoft utrácejí za umělou inteligenci a datová centra ještě víc, než trh čekal. Vidět je to na volném cash flow, tedy na penězích, které firmě zbudou po zaplacení provozu a investic. Alphabet, Amazon i Meta jsou kvůli investicím v minusu a Microsoftu volný cash flow meziročně klesl o víc než čtvrtinu.",
      "Investoři se proto ptají, kdy a jestli se jim tyto obří investice vrátí. Část firem si na ně navíc začíná půjčovat nebo vydávat nové akcie. Po velkém růstu technologií pak stačilo málo a přišel výprodej. Ten se přelil i do Asie, hlavně k výrobcům čipů a pamětí v Japonsku, Koreji a na Tchaj-wanu.",
      "Je ale důležité říct, co to znamená. Nejde o krach firem, jejich tržby i zisky dál rostou. Trh jen přeceňuje očekávání, která byla velmi vysoká. A zbytek trhu, tedy firmy mimo technologie, přitom držel.",
    ],
    reserve: [
      "FactSet 30. 10. 2026: výsledky má 60 % firem; 82 % nad odhady zisků (5letý průměr 78 %, 10letý 77 %); o kolik firmy odhady překonaly: o 1,9 % (5letý průměr 7,5 %), nejméně od 4Q 2022; růst zisků 30,2 %, tržeb 13,4 %.",
      "Volný cash flow 3Q 2026: Meta −2,1 mld. USD (před rokem +10,6); Alphabet kolem −9 mld. USD [sekundární zdroje, ověřit]; Amazon −42,4 mld. USD za posledních 12 měsíců (před rokem +14,8); Microsoft +18,6 mld. USD proti 25,7 (−28 %, bez finančních leasingů).",
      "Reakce akcií: Alphabet 29. 10. −12,6 %, Intel 30. 10. −28,6 %, Amazon 30. 10. −1,4 %; za měsíc Korea (KOSPI) −18,6 %, Tchaj-wan −12,9 % (Trading Economics).",
    ],
  },
  {
    n: 7, title: "Dluhopisy tlumily pokles akcií", min: "2 min",
    msg: "Výnosy klesají z nejvyšších úrovní od roku 2007",
    say: [
      "Dobrou zprávou posledního měsíce jsou dluhopisy.",
      "Dluhopisy byly letos dlouho otloukánkem. Jejich výnosy rostly ze tří hlavních důvodů. Za prvé drahá ropa zvedla inflační očekávání. Za druhé centrální banky začaly zvyšovat sazby. A za třetí trh znervózňují vysoké deficity, hlavně ve Spojených státech, kde veřejný dluh v srpnu překonal 40 bilionů dolarů. Když výnosy rostou, cena dluhopisů, které už investoři drží, klesá.",
      "V říjnu se to otočilo. Když se prodávaly technologie, investoři hledali bezpečí a nakupovali státní dluhopisy. Výnos desetiletého amerického dluhopisu klesl z 5,31 procenta, což bylo nejvíc od roku 2007, na 4,96 procenta. Klesly i výnosy v Německu a v Itálii. Pro majitele dluhopisů to znamená, že jejich dluhopisy zdražily.",
      "Výjimkou je Francie. Tam výnosy naopak mírně vzrostly a příplatek, který Francie platí navíc proti Německu, je nejvyšší od roku 2012. Ratingová agentura Fitch na konci října zhoršila výhled francouzského ratingu. Dobrá zpráva je, že se francouzské problémy zatím nepřelévají do Itálie ani do Německa.",
      "Celé to hraje do karet konzervativním portfoliím. Dluhopisy znovu fungují jako polštář, který tlumí výkyvy akcií, a zároveň nesou slušný příjem.",
    ],
    reserve: [
      "10leté výnosy k 3. 11. proti stavu před měsícem: USA 4,96 % (−36 bb), Německo 3,32 % (−17 bb), Itálie 4,46 % (−18 bb), Francie 4,94 % (+7 bb); bb = setina procentního bodu (Trading Economics).",
      "Maximum USA 5,31 % 5. 10. 2026. Rozdíl Francie–Německo 162 bb, začátkem října 127 bb.",
      "Fitch zhoršil výhled francouzského ratingu na negativní (konec října); HDP Francie ve 3Q −0,1 %; prezidentské volby na jaře 2027. Dluh USA překonal 40 bilionů USD 18. 8. 2026.",
    ],
  },
  {
    n: 8, title: "Shrnutí: kde jsou trhy teď", min: "2 min",
    msg: "Krátkodobě nervózní trhy, firmy ale dál vydělávají",
    say: [
      "Než se podíváme dopředu, shrnu, kde trhy teď jsou. Krátkodobě jsou nervózní, firmy ale dál vydělávají.",
      "Energie: ropa zlevnila zhruba ke 100 dolarům, pořád je ale výrazně dražší než před válkou. Spor mezi USA a Íránem kolísá mezi jednáním a údery a trh bude dál citlivě reagovat na každou zprávu.",
      "Inflace a sazby: drahé energie drží inflaci nahoře, a centrální banky proto spíš ještě zvýší sazby, než aby je snižovaly.",
      "Akcie: zisky firem rostou kolem 30 procent. Trh ale trestá drahé sázky na umělou inteligenci. Zbytek trhu drží.",
      "Dluhopisy: výnosy klesají z nejvyšších úrovní od roku 2007. Dluhopisy díky tomu zdražují a pořád nesou slušný příjem.",
      "Evropa: hlavním rizikem jsou drahé energie a Francie.",
      "A nakonec volby v USA. Výsledky přinesou krátkodobý šum na trzích. Historie je ale uklidňující: od roku 1950 byl index S&P 500 rok po volbách do Kongresu vždy výš. Záruka do budoucna to samozřejmě není.",
    ],
    note: "Ráno doplnit výsledek voleb (Sněmovna a Senát). Před volbami byli favority pro Sněmovnu demokraté, Senát byl nejistý. Rozdělený Kongres obvykle znamená méně nových výdajů, což bývá pro dluhopisy spíš dobrá zpráva.",
    reserve: [
      "S&P 500 byl rok po volbách do Kongresu výš ve všech případech od roku 1950, průměrně o 12–18 % podle zdroje (U.S. Bank, BNY, Deutsche Bank).",
    ],
  },
  {
    n: 9, title: "Výhled: pokles technologií je dočasný", min: "3 min",
    msg: "Pro pasivního investora rozhodují zisky firem, ne denní zprávy",
    say: [
      "Teď k výhledu. Pro pasivního investora, který drží celý trh dlouhodobě, nerozhodují denní zprávy, ale zisky firem. A ty vypadají dobře.",
      "Pokles technologií považujeme za dočasný. Hlavním důvodem je cloud, tedy pronájem výpočetního výkonu a služeb přes internet, na kterém stojí i umělá inteligence. Ten zrychluje. Cloudová služba Microsoftu Azure roste o 48 procent, Amazon Web Services o 39 procent a obě firmy mají zakázky nasmlouvané na roky dopředu. Investice do umělé inteligence se tedy už začínají vracet v tržbách. Trh jen chce vidět, že tržby porostou rychleji než náklady.",
      "Druhým důvodem je růst zisků. Zisky amerických firem rostou kolem 30 procent a analytici čekají podobné tempo i ve čtvrtém čtvrtletí.",
      "Za třetí akcie nejsou drahé. Poměr ceny akcií k očekávaným ziskům je pod průměrem posledních deseti let, protože zisky rostly rychleji než ceny.",
      "Za čtvrté dluhopisy znovu nesou slušný výnos a tlumí výkyvy akcií.",
      "A konečně pasivní investor drží celý trh. Nemusí hádat, která firma vyhraje, ani trefovat správný okamžik pro nákup nebo prodej.",
      "Co bude v příštích měsících důležité? Za prvé Hormuz: dohoda s Íránem by energie rychle zlevnila, nové útoky by je naopak zdražily. Za druhé proinflační rizika, protože dražší energie se v Evropě propíšou do cen hlavně v příštím roce. Za třetí riziko vyšších sazeb, protože Fed, ECB i ČNB mohou ještě přitlačit. A za čtvrté Francie, jejíž dluhopisy jsou rizikem výprodeje evropských aktiv, tedy akcií, dluhopisů i eura.",
    ],
    reserve: [
      "Azure +48 % (33,2 mld. USD), nasmlouvané zakázky Microsoftu 677 mld. USD (+73 %).",
      "AWS +39 % (46,0 mld. USD), nasmlouvané zakázky 578 mld. USD, víc než dvojnásobek; vedení čeká v letech 2027 a 2028 růst přes 40 %.",
      "FactSet 30. 10.: očekávaný růst zisků ve 4Q 2026 +28,4 %, za celý rok 2026 +32,9 %; forward P/E 18,7 (5letý průměr 19,8, 10letý 19,1).",
    ],
  },
  {
    n: 10, title: "Co z toho plyne pro investory", min: "3 min",
    msg: "Investovat dál, široce rozloženě a s rozmyslem",
    say: [
      "Na závěr to nejdůležitější: co z toho plyne pro vaše klienty.",
      "Poslední měsíc ukázal, že diverzifikace se vyplatila. Technologický Nasdaq 100 ztratil 9 procent, pražská burza přitom byla v plusu a dluhopisy zdražily. Kdo měl peníze rozložené do různých regionů a tříd aktiv, pokles skoro necítil.",
      "Kdo naopak vsadil všechno na technologie, nemá teď v portfoliu hezký pohled. Dlouhodobě ale technologiím věříme. Důvody jsem ukázal ve výhledu: rychle rostoucí cloud, silné zisky a rozumné ocenění.",
      "Časovat trh je těžké vždycky, ale dnes, kdy trhy hýbou Trumpova prohlášení, cena ropy a geopolitika, obzvlášť. Šestého října byl rekord a o měsíc později korekce technologií. Odhadnout takový zvrat předem se nedaří ani profesionálům.",
      "Výkyvy k investování patří a poslední krize byly krátké. Když letos začala válka s Íránem, index S&P 500 do konce března spadl zhruba o 8 procent. Za dva týdny ode dna byl ale zpět nad předválečnou úrovní. Kdo tehdy prodal, přišel o návrat trhu.",
      "S čím tedy pracovat? Základem jsou naše široce diverzifikovaná ETF portfolia. Máme konzervativní, vyvážené, dynamické a další varianty podle toho, jaké riziko je klient ochotný nést a na jak dlouho investuje.",
      "Druhá myšlenka: nebát se diverzifikovat i mimo světové trhy, například do Prahy přes WOOD PX ETF. Je v korunách, takže klient nenese měnové riziko. Jde o firmy, které klienti znají z každodenního života. A pražská burza má za sebou silný výkon: index PX za posledních pět let vzrostl skoro o 100 procent, a to bez dividend. Navíc se pohybuje jinak než světové technologie, jak ukázal poslední měsíc.",
      "Je ale potřeba myslet na koncentraci. Česká burza je malá a stojí na několika velkých firmách. Proto PX ETF patří do portfolia jako doplněk v přiměřené váze, ne jako náhrada široce rozloženého světového portfolia.",
      "Shrnuto: investovat dál, široce rozloženě a s rozmyslem. Děkuji za pozornost a rád odpovím na vaše dotazy.",
    ],
    note: "Na slajdu je upozornění: nejde o investiční doporučení, hodnota investice může kolísat a minulá výkonnost není zárukou budoucích výnosů.",
    reserve: [
      "S&P 500: 6 878,88 (27. 2.) → 6 343,72 (30. 3., −7,8 %) → 6 967,38 (14. 4.) (Trading Economics).",
      "PX: 1 329,42 (2. 11. 2021) → 2 636,01 (2. 11. 2026), +98 % bez dividend; od začátku roku 2026 −1,9 %, za 3 měsíce −2,6 % (Trading Economics).",
      "WOOD PX ETF: na pražské burze od 7. 9. 2026, sleduje index PX (drží 10 největších firem), v korunách, dividendy reinvestuje; ČEZ a finanční firmy tvoří téměř 90 % indexu (Finex, CzechCrunch).",
    ],
  },
];

const check = [
  "Výsledek voleb do Kongresu a reakce trhů (slajd 8).",
  "Írán: nové údery, nebo posun v jednání; ranní cena ropy Brent a plynu (slajd 4).",
  "Hlasování Fedu 10:2 (Cook a Hammack) ve statementu Fedu (slajd 5).",
  "Volný cash flow Alphabetu za 3Q, kolem −9 mld. USD, je jen ze sekundárních zdrojů (slajd 6). Kdyby nesedělo, upravit i bod „Alphabet, Amazon a Meta jsou v minusu“.",
];

const sources = [
  "Trading Economics: indexy, kurzy, výnosy dluhopisů, ropa Brent, plyn TTF a zprávy k pohybům, data k 2.–3. 11. 2026",
  "FactSet, S&P 500 Earnings Season Update, 30. 10. 2026",
  "Kpler podle CNBC (30. 9. 2026) a hormuz.now: toky ropy přes Hormuz",
  "Nvidia: oznámení termínu výsledků za 3Q fiskálního roku 2027",
  "Výsledky Microsoftu, Mety, Amazonu a Alphabetu za 3Q 2026",
  "ČTK: odhady analytiků k zasedání ČNB",
  "Finex, CzechCrunch: WOOD PX ETF",
  "U.S. Bank, BNY: akcie po volbách do Kongresu",
];

// ------------------------------------------------------------- stavba dokumentu
const body = (t) => new Paragraph({ children: [new TextRun(t)], spacing: { after: 140, line: 300 } });
const children = [];

children.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Ekonomika a trhy – listopad 2026")] }));
children.push(new Paragraph({
  spacing: { after: 120 },
  children: [new TextRun({ text: "Pomocný materiál k prezentaci, 4. 11. 2026", color: RED, bold: true, size: 26 })],
}));
children.push(new Paragraph({
  spacing: { after: 240 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RED, space: 6 } },
  children: [new TextRun({
    text: "Ke každému slajdu je souvislý text, co říct, a pod ním menším písmem čísla v záloze pro případ dotazu. Celkem zhruba 22 minut. Data k 2.–3. 11. 2026.",
    color: GRAY, size: 20,
  })],
}));

slides.forEach((s, i) => {
  children.push(new Paragraph({
    heading: HeadingLevel.HEADING_1,
    pageBreakBefore: i > 0,
    children: [
      new TextRun({ text: `Slajd ${s.n}  `, color: RED }),
      new TextRun(s.title),
    ],
  }));
  children.push(new Paragraph({
    spacing: { after: 200 },
    children: [
      new TextRun({ text: s.msg, italics: true, color: RED }),
      new TextRun({ text: `   ·   zhruba ${s.min}`, color: GRAY, size: 20 }),
    ],
  }));
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun("Co říct")] }));
  s.say.forEach((t) => children.push(body(t)));
  if (s.note) {
    children.push(new Paragraph({
      spacing: { before: 60, after: 160 },
      shading: { fill: "FDECEB", type: "clear", color: "auto" },
      children: [new TextRun({ text: "Poznámka: ", bold: true, color: RED }), new TextRun(s.note)],
    }));
  }
  if (s.reserve.length) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun("Čísla v záloze")] }));
    s.reserve.forEach((t) => children.push(new Paragraph({
      numbering: { reference: "bullets", level: 0 },
      spacing: { after: 60 },
      children: [new TextRun({ text: t, size: 18, color: GRAY })],
    })));
  }
});

children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: true, children: [new TextRun("Ověřit ráno před prezentací")] }));
check.forEach((t) => children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 80 }, children: [new TextRun(t)] })));
children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Zdroje")] }));
sources.forEach((t) => children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 }, children: [new TextRun({ text: t, size: 20 })] })));

const doc = new Document({
  creator: "WOOD & Company",
  title: "Ekonomika a trhy – pomocný materiál",
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal",
        run: { font: "Arial", size: 44, bold: true, color: GREEN }, paragraph: { spacing: { before: 0, after: 120 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Arial", size: 32, bold: true, color: GREEN }, paragraph: { spacing: { before: 120, after: 80 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Arial", size: 24, bold: true, color: GREEN }, paragraph: { spacing: { before: 120, after: 100 }, keepNext: true, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Arial", size: 20, bold: true, color: GRAY }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 360, hanging: 260 } } } }] }],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1300, left: 1300, right: 1300 } } },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
        new TextRun({ text: "Ekonomika a trhy – pomocný materiál   ·   strana ", color: GRAY, size: 16 }),
        new TextRun({ children: [PageNumber.CURRENT], color: GRAY, size: 16 }),
      ] })] }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then((b) => { fs.writeFileSync(OUT, b); console.log("uloženo", OUT); });

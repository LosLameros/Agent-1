// Pomocný materiál k prezentaci Aktuální vývoj na trzích – listopad 2026 (Word), mluvená řeč
const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Footer, PageNumber, BorderStyle } = require("docx");

const OUT = process.argv[2];
const GREEN = "0F3738", RED = "EE4F46", GRAY = "5F6B6B";

const slides = [
  { n: 1, title: "Aktuální vývoj na trzích", min: "0,5 min", say: [
    "Dobrý den, děkuji za pozvání. Jsem z WOOD & Company a dnes bych vás rád provedl tím, co se na trzích dělo za poslední měsíc a co to znamená pro vaše klienty.",
    "Musím říct, že to byl hodně rušný měsíc. Ropa byla nejdražší za čtyři roky, technologické akcie prošly pořádným výprodejem, centrální banky řešily, jestli ještě zvedat sazby, a v Americe se volilo do Kongresu. Projdeme si, co se stalo, proč se to stalo a hlavně co si z toho má odnést dlouhodobý investor.",
    "Zabere nám to zhruba dvacet minut a na konci rád odpovím na vaše otázky.",
  ]},
  { n: 2, title: "Co se stalo od začátku října", min: "2 min", say: [
    "Začnu časovou osou, protože se toho za ten měsíc stalo opravdu hodně a jedno navazuje na druhé.",
    "Na začátku října byla nálada skvělá. Šestého října byly americké akcie na historickém maximu, rekord zapsal jak index S&P 500, tak technologický Nasdaq.",
    "Zároveň ale pořád zdražovala ropa. Kolem 23. října byla nejdražší za čtyři roky, protože se trh bál, že Amerika znovu zaútočí na Írán a dodávky z Perského zálivu se ještě víc omezí.",
    "Na konci října pak zasedaly centrální banky. Americký Fed i Evropská centrální banka nechaly sazby, kde byly, ale daly jasně najevo, že se zvyšováním možná ještě neskončily.",
    "Ve stejných dnech zveřejnili výsledky technologičtí giganti. A tady je zajímavé, že čísla měli dobrá, a přesto jejich akcie výrazně zlevnily. Trh je potrestal hlavně za to, kolik peněz utrácejí za umělou inteligenci. K tomu se ještě dostanu.",
    "Na začátku listopadu se objevila naděje na dohodu s Íránem a ropa za jediný den výrazně zlevnila. Hned další den ale Amerika na Írán znovu udeřila. Ve stejný den se v USA volilo do Kongresu a demokraté získali většinu v obou komorách. I k tomu se ještě vrátím.",
    "A poslední bod je teprve před námi. Sedmnáctého listopadu zveřejní výsledky Nvidia, tedy největší výrobce čipů pro umělou inteligenci, a tím výsledková sezóna v podstatě skončí. Zatím je mimochodem hodně silná, 82 procent firem překonalo odhady analytiků.",
    "Dnes se tedy podíváme na to, jak se dařilo trhům, co se děje s ropou a se sazbami, proč padaly technologie a co se stalo s dluhopisy. Na konci si řekneme, co čekáme dál.",
  ]},
  { n: 3, title: "USA rostou navzdory poklesu technologií", min: "2,5 min", say: [
    "Teď se pojďme podívat na čísla. Na slajdu vidíte, jak si vedly hlavní akciové indexy za poslední měsíc, za tři měsíce a od začátku roku. Šedý sloupec je výnos v místní měně, červený výnos v korunách, tedy to, co reálně vidí český investor.",
    "Za poslední měsíc je příběh docela jasný. Výprodej zasáhl hlavně technologie a firmy, které stojí za infrastrukturou pro umělou inteligenci, tedy výrobce čipů, pamětí a datových center. Technologický Nasdaq 100 ztratil skoro 9 procent a je víc než 10 procent pod rekordem, tedy v takzvané technické korekci. Podobně dopadlo Japonsko, kde je hodně firem napojených na čipy.",
    "Důležité ale je, že zbytek amerického trhu drží. S&P 500 ztratil jen kolem 2 procent a Dow Jones, kde je technologií méně, dokonce mírně přidal. V plusu byla i pražská burza, protože technologie v ní skoro nejsou.",
    "Když se podíváme na delší období, obrázek je pořád dobrý. Od začátku roku jsou americké akcie v korunách zhruba o 16 procent výš a japonské dokonce o víc než 30 procent. Evropa přidala kolem 7 procent, jen Praha je letos mírně v minusu.",
    "A ještě poznámka ke kurzu, protože ten u nás hraje roli. Za poslední měsíc se koruna vůči dolaru skoro nehnula, takže výnos v korunách je prakticky stejný jako v dolarech. Od začátku roku ale dolar posílil zhruba o 6 procent, a to korunovým investorům výnos z amerických akcií pěkně zvedlo.",
  ]},
  { n: 4, title: "Naděje na dohodu stáhly ropu ke 100 USD", min: "3 min", say: [
    "A teď k ropě, protože ta je pro inflaci a sazby asi nejdůležitější.",
    "Na grafu vidíte cenu ropy Brent od začátku roku. Na konci února, těsně před válkou s Íránem, stál barel kolem 73 dolarů. Pak cena vystřelila a od té doby se drží vysoko. Tento týden ropa zlevnila zhruba ke 100 dolarům, protože se objevila naděje na dohodu.",
    "Často dostávám otázku, jestli je Hormuzský průliv zavřený. Odpověď je, že zavřený není, ale volný taky ne. Tankery plují s doprovodem amerického námořnictva a Írán na ně pořád útočí. Podle dat společnosti Kpler teklo průlivem na konci září zhruba 80 procent toho, co před válkou. Samotná ropa se vrátila skoro na normál, ale paliv, tedy nafty, benzinu nebo leteckého paliva, proudí jen asi pětina. A svět se mezitím naučil průliv obcházet, zhruba 40 procent ropy z Perského zálivu dnes jde ropovody jinudy.",
    "Trh přitom reaguje na každé slovo z Washingtonu a z Teheránu, protože Trump střídá hrozby s nabídkami jednání. V pondělí íránský nejvyšší vůdce povolil vládě vyjednávat, Trump řekl, že Írán chce dohodu, a ropa za jediný den zlevnila o víc než 7 procent. V noci na úterý ale Amerika znovu udeřila na íránský ostrov Kešm. Americký ministr energetiky pak uklidňoval, že to toky ropy neovlivnilo, a ropa se drží kolem 103 dolarů.",
    "I tak je ale pořád o 42 procent dražší než před válkou. A týká se to i plynu. Ten v Evropě minulý týden poprvé od roku 2022 překonal 100 eur za megawatthodinu a zásobníky jsou před zimou plné méně než obvykle.",
    "Co si z toho vzít? Drahé energie drží inflaci nahoře. A v Evropě se do cen pro domácnosti a firmy promítnou hlavně v příštím roce, až dodavatelé přecení své ceníky.",
  ]},
  { n: 5, title: "Sazby: pauza, ne konec zvyšování", min: "2 min", say: [
    "Drahé energie nás přivádějí k centrálním bankám.",
    "Začnu Amerikou. Fed v září poprvé po třech letech zvedl sazby a na konci října je nechal beze změny, v pásmu 3,75 až 4 procenta. Dva členové bankovní rady ale chtěli zvyšovat už teď a trh počítá s tím, že Fed v prosinci přitlačí. Důvod je jednoduchý: americká ekonomika roste rychle a inflace neklesá.",
    "V Evropě je situace podobná. Evropská centrální banka nechala sazbu na 2,5 procenta, ale šéfka ECB Christine Lagardeová přiznala, že se o zvýšení mluvilo, takže trh s ním dál počítá. Navíc oznámila, že z čela banky odejde předčasně, takže ECB čeká i změna ve vedení.",
    "Co se týče ČNB, ta rozhoduje hned zítra a analytici čekají zvýšení ze 3,75 na 4 procenta. Inflace byla v září 2,5 procenta, tedy vlastně nedaleko cíle. Centrální banku ale trápí hlavně služby, které zdražují rychle.",
    "Pro klienty to znamená, že sazby spíš ještě porostou, než že by klesaly. Konzervativní investory to může potěšit, protože dostanou vyšší úrok z vkladů a z nových dluhopisů. Pro drahé akcie je to naopak spíš tlak.",
  ]},
  { n: 6, title: "Zisky rostou, trh trestá sázky na AI", min: "2,5 min", say: [
    "Teď se dostávám k tomu, co asi zajímá nejvíc, tedy proč klesaly technologie, když firmy vydělávají.",
    "Nejdřív k výsledkům. Do konce října zveřejnilo výsledky 60 procent firem z indexu S&P 500 a 82 procent z nich překonalo odhady analytiků. Normálně to bývá kolem 78 procent, takže je to nadprůměrná sezóna. Zisky rostou meziročně zhruba o 30 procent a je to už třetí čtvrtletí v řadě, kdy rostou o víc než 25 procent.",
    "Má to ale háček. Firmy sice odhady překonávají, ale o méně než dřív. Trh je proto vybíravější a co nesplní hodně vysoká očekávání, to potrestá.",
    "A přesně to se stalo technologickým gigantům. Alphabet, Amazon, Meta i Microsoft utrácejí za umělou inteligenci a datová centra ještě víc, než trh čekal. Nejlíp je to vidět na volném cash flow, tedy na penězích, které firmě zbudou, když zaplatí provoz a investice. Alphabet, Amazon i Meta se kvůli investicím dostaly do minusu a Microsoftu volný cash flow klesl o víc než čtvrtinu.",
    "Investoři se tak logicky ptají, kdy a jestli se jim tyhle obří investice vrátí. Navíc si na ně část firem začíná půjčovat nebo vydávat nové akcie. A když technologie předtím tolik vyrostly, stačilo málo a přišel výprodej, který se přelil i do Asie, hlavně k výrobcům čipů v Japonsku, Koreji a na Tchaj-wanu.",
    "Chci ale zdůraznit jednu věc. Nejde o žádný krach firem, jejich tržby i zisky dál rostou. Trh jen přeceňuje očekávání, která byla hodně vysoko. A zbytek trhu přitom držel.",
  ]},
  { n: 7, title: "Dluhopisy tlumily pokles akcií", min: "2 min", say: [
    "Teď jedna dobrá zpráva, a to jsou dluhopisy.",
    "Ty byly letos dlouho otloukánkem. Jejich výnosy rostly, a to hlavně ze tří důvodů. Drahá ropa zvedla obavy z inflace, centrální banky začaly zvedat sazby a trh navíc znervózňují vysoké deficity, hlavně v Americe, kde dluh v srpnu překonal 40 bilionů dolarů. A když výnosy rostou, dluhopisy, které už lidé drží, ztrácejí na ceně.",
    "V říjnu se to ale otočilo. Když se prodávaly technologie, investoři hledali bezpečí a kupovali státní dluhopisy. Výnos desetiletého amerického dluhopisu klesl z 5,31 procenta, což bylo nejvíc od roku 2007, na necelých 5 procent. Klesly i výnosy v Německu a v Itálii. Pro majitele dluhopisů to znamená, že jejich dluhopisy zdražily.",
    "Výjimkou je Francie. Tam výnosy naopak mírně vzrostly a Francie si dnes ve srovnání s Německem půjčuje nejdráž od roku 2012. Na konci října jí navíc ratingová agentura Fitch zhoršila výhled. Dobrá zpráva je, že se to zatím nepřelévá do Itálie ani do Německa.",
    "A co z toho plyne? Že to hraje do karet konzervativním portfoliím. Dluhopisy zase fungují jako polštář, který tlumí výkyvy akcií, a k tomu nesou slušný příjem.",
  ]},
  { n: 8, title: "Shrnutí: kde jsou trhy teď", min: "3 min", say: [
    "Než se podíváme dopředu, pojďme si to krátce shrnout. Trhy jsou krátkodobě nervózní, ale firmy dál vydělávají.",
    "Ropa zlevnila zhruba ke 100 dolarům, pořád je ale výrazně dražší než před válkou a spor Ameriky s Íránem se houpe mezi jednáním a údery. Drahé energie drží inflaci nahoře, a proto centrální banky spíš ještě zvýší sazby. U akcií zisky rostou kolem 30 procent, trh ale trestá drahé sázky na umělou inteligenci, zatímco zbytek trhu drží. Výnosy dluhopisů klesají z nejvyšších úrovní od roku 2007, takže dluhopisy zdražují a pořád nesou slušný příjem. A v Evropě jsou hlavním rizikem drahé energie a Francie.",
    "A teď k americkým volbám, které už jsou sečtené. Pro republikány to byl debakl. Demokraté získali většinu v obou komorách Kongresu a vyhrávali i v nejkonzervativnějších baštách. Symbolem je Texas, kde demokrat poprvé od roku 1988 vyhrál křeslo v Senátu a demokratka porazila i dlouholetého guvernéra Grega Abbotta. V Kansasu budou mít demokratického senátora poprvé po 94 letech.",
    "Rozhodla hlavně ekonomika. Pro 39 procent voličů to bylo nejdůležitější téma a skoro 70 procent Američanů hodnotí špatně, jak Trump bojuje s drahotou. Lidé ji nejvíc cítí u benzinu a jeho zdražení si spojují s válkou v Íránu.",
    "Co to znamená? Trump má na zbytek mandátu hodně svázané ruce a prezident s Kongresem se budou dva roky navzájem blokovat. Demokraté chtějí rušit Trumpova cla a obnovit dotace na zdravotní péči, jejich zákony ale může Trump vetovat. Dohodnout se dá spíš u cen léků, bydlení nebo datových center pro umělou inteligenci. Hlavně ale přichází éra vyšetřování a bez demokratů neprojde rozpočet, takže hrozí další uzavření vlády.",
    "Trhy to přesto vzaly v klidu. Výsledek se čekal, byl v cenách a akciím se po volbách dařilo. Víc než Washington teď trhem hýbe umělá inteligence. Po prudkém výprodeji, kdy Nasdaq 100 za tři dny odepsal přes 6 procent, znovu přilákala kupce.",
    "Pro dlouhodobé investory jsou tak volby spíš krátkodobý šum. Od roku 1950 byl index S&P 500 rok po volbách do Kongresu vždycky výš. O směru trhu budou rozhodovat hlavně zisky firem a cena ropy, se kterou hýbou jednání s Íránem.",
  ]},
  { n: 9, title: "Výhled: pokles technologií je dočasný", min: "3 min", say: [
    "A teď to podstatné, tedy co čekáme dál. Pro pasivního investora, který drží celý trh dlouhodobě, nerozhodují denní zprávy, ale zisky firem. A ty vypadají dobře.",
    "Pokles technologií proto bereme jako dočasný. Hlavním důvodem je cloud, tedy pronájem výpočetního výkonu a služeb přes internet, na kterém stojí i umělá inteligence. A ten zrychluje. Cloud Microsoftu roste o 48 procent, Amazonu o 39 procent a obě firmy mají zakázky nasmlouvané na roky dopředu. Investice do umělé inteligence se tedy už začínají vracet v tržbách, trh jen chce vidět, že tržby porostou rychleji než náklady.",
    "Druhým důvodem jsou zisky. Rostou kolem 30 procent a analytici čekají podobné tempo i ve čtvrtém čtvrtletí.",
    "Zatřetí, akcie nejsou drahé. Když porovnáte cenu akcií s tím, kolik mají firmy vydělat, jsme pod průměrem posledních deseti let. Zisky totiž rostly rychleji než ceny.",
    "Začtvrté, dluhopisy zase nesou slušný výnos a tlumí výkyvy akcií.",
    "A nakonec, pasivní investor drží celý trh. Nemusí hádat, která firma vyhraje, ani trefovat správný okamžik, kdy nakoupit nebo prodat.",
    "Na co si ale dát pozor? Zaprvé Hormuz. Dohoda s Íránem by energie rychle zlevnila, nové útoky by je naopak zdražily. Zadruhé inflace, protože dražší energie se v Evropě propíšou do cen hlavně v příštím roce. Zatřetí sazby, protože Fed, ECB i ČNB můžou ještě přitlačit. A začtvrté Francie, jejíž dluhopisy můžou spustit výprodej evropských aktiv, tedy akcií, dluhopisů i eura.",
  ]},
  { n: 10, title: "Co z toho plyne pro investory", min: "3 min", say: [
    "Na závěr to nejdůležitější, tedy co z toho plyne pro vaše klienty.",
    "Poslední měsíc ukázal, že se diverzifikace vyplácí. Když padaly technologie, pražská burza byla v plusu a dluhopisy zdražily. Kdo měl peníze rozložené do různých regionů a tříd aktiv, pokles skoro necítil.",
    "Kdo naopak nedávno vsadil všechno na technologie, nemá teď v portfoliu zrovna hezký pohled. Dlouhodobě ale technologiím věříme a důvody jsem ukazoval před chvílí: rychle rostoucí cloud, silné zisky a rozumné ocenění.",
    "Časovat trh je těžké vždycky, ale dnes, kdy trhy hýbou Trumpova prohlášení, ropa a geopolitika, obzvlášť. Šestého října byl rekord a o měsíc později korekce. Tohle dopředu neodhadnou ani profesionálové.",
    "Výkyvy k investování prostě patří. Dobrá zpráva je, že poslední krize byly krátké. Když letos začala válka s Íránem, americké akcie do konce března spadly zhruba o 8 procent. Za dva týdny ode dna už ale byly zpátky nad předválečnou úrovní. Kdo tehdy prodal, o tenhle návrat přišel.",
    "S čím tedy pracovat? Základem jsou naše široce diverzifikovaná ETF portfolia. Máme konzervativní, vyvážené, dynamické a další varianty podle toho, kolik rizika je klient ochotný nést a na jak dlouho investuje.",
    "A druhá věc: nebát se diverzifikovat i mimo světové trhy, třeba do Prahy přes WOOD PX ETF. Je v korunách, takže klient nemá měnové riziko, a jde o firmy, které zná z běžného života. Pražská burza má navíc za sebou silné roky, index PX za posledních pět let vyrostl skoro o 100 procent, a to ještě bez dividend. A jak ukázal poslední měsíc, pohybuje se jinak než světové technologie.",
    "Jen je potřeba myslet na koncentraci. Česká burza je malá a stojí na pár velkých firmách, takže PX ETF patří do portfolia jako doplněk v rozumné váze, ne jako náhrada světového portfolia.",
    "Kdybych to měl shrnout jednou větou: investovat dál, široce rozloženě a s rozmyslem. Jen pro pořádek dodám, že nejde o investiční doporučení. Děkuji za pozornost a rád odpovím na vaše otázky.",
  ]},
];

const children = [];
children.push(new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun("Aktuální vývoj na trzích – listopad 2026")] }));
children.push(new Paragraph({ spacing: { after: 120 },
  children: [new TextRun({ text: "Pomocný materiál k prezentaci, 4. 11. 2026", color: RED, bold: true, size: 26 })] }));
children.push(new Paragraph({ spacing: { after: 240 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: RED, space: 6 } },
  children: [new TextRun({ text: "Text ke každému slajdu je psaný tak, aby se dal číst nahlas. Celkem zhruba 24 minut.", color: GRAY, size: 20 })] }));

slides.forEach((s, i) => {
  children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: i > 0,
    children: [new TextRun({ text: `Slajd ${s.n}  `, color: RED }), new TextRun(s.title)] }));
  children.push(new Paragraph({ spacing: { after: 200 },
    children: [new TextRun({ text: `zhruba ${s.min}`, color: GRAY, size: 20, italics: true })] }));
  s.say.forEach((t) => children.push(new Paragraph({ spacing: { after: 160, line: 320 }, children: [new TextRun({ text: t, size: 24 })] })));
});

const doc = new Document({
  creator: "WOOD & Company",
  title: "Aktuální vývoj na trzích – pomocný materiál",
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal",
        run: { font: "Arial", size: 44, bold: true, color: GREEN }, paragraph: { spacing: { before: 0, after: 120 }, keepNext: true } },
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: "Arial", size: 32, bold: true, color: GREEN }, paragraph: { spacing: { before: 120, after: 60 }, keepNext: true, outlineLevel: 0 } },
    ],
  },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1300, left: 1300, right: 1300 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [
      new TextRun({ text: "Aktuální vývoj na trzích – pomocný materiál   ·   strana ", color: GRAY, size: 16 }),
      new TextRun({ children: [PageNumber.CURRENT], color: GRAY, size: 16 }),
    ] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((b) => {
  fs.writeFileSync(OUT, b);
  // stejný text i jako Markdown
  const md = ["# Aktuální vývoj na trzích – pomocný materiál (4. 11. 2026)", "",
    "Text ke každému slajdu je psaný tak, aby se dal číst nahlas. Celkem zhruba 24 minut.", ""];
  slides.forEach((s) => { md.push(`## Slajd ${s.n}: ${s.title} (zhruba ${s.min})`, ""); s.say.forEach((t) => md.push(t, "")); });
  fs.writeFileSync(process.argv[3], md.join("\n"));
  console.log("uloženo", OUT);
});

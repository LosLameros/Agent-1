# Podklad pro článek do Portu Magazínu: strategie České dividendy

Vlož agentovi pro články spolu s master promptem (`prompts/clanky-portu.md`). Je to shrnutí dohod z interní práce, ne hotový text. Kde je `[DOPLNIT]`, musí rozhodnout člověk před psaním.

## Vstupní proměnné master promptu

- **ZPRÁVA / TÉMA:** Jak se vybírají dividendové akcie z pražské burzy a proč nestačí dívat se jen na dividendový výnos. Příklad: jak jsme v Portu poskládali nápad na dividendovou strategii z české burzy.
- **ÚHEL POHLEDU:** Vysoká dividenda ještě neznamená dobrou investici. Záleží, jestli ji firma dokáže platit i příště a jestli jí roste hodnota. Čtenář si odnese tři otázky, které si může položit u kterékoli dividendové akcie.
- **TYP:** edukativní vysvětlovák
- **DÉLKA:** 600–800 slov
- **DEADLINE DAT:** [DOPLNIT: datum psaní]. Čísla níže jsou k 10. 11. 2026 (ceny, váhy indexu PX) a 12. 11. 2026 (cílové ceny). Před publikací je obnovit.
- **CÍLOVÝ ČTENÁŘ:** člověk bez finančního vzdělání, který přemýšlí o pravidelném příjmu z investic
- **STAV STRATEGIE:** [DOPLNIT: strategie je schválená a spouští se k datu X / je to zatím interní návrh]. Dokud to není potvrzené, nepsat „spouštíme" ani „nabízíme" a neuvádět konkrétní váhy (viz Compliance).

## Co strategie je

Tematická strategie z dividendových akcií pražské burzy. Dividendy se vyplácejí klientovi na peněženku, na rozdíl od akumulačního WOOD PX ETF, které je reinvestuje. Musí mít jiné složení než ETF, aby měla smysl vedle něj.

## Jak jsme vybírali

1. **Celá burza.** Na trzích Prime, Standard a Free je 52 akciových emisí. Zahraniční akcie bez vazby na Česko (např. Shell, Volkswagen) jsme vyřadili.
2. **Dividenda.** Firma ji vyplatila v posledním roce a aspoň ve třech z posledních pěti let.
3. **Obchodovatelnost.** Medián denního objemu aspoň 1 mil. Kč a obchod aspoň v 90 % dnů. Menší firmy mimo index (E4U, SAB Finance, Toma) dividendu platí, ale nedají se rozumně koupit ani prodat.
4. **Výnos.** Hrubý výnos za 12 měsíců aspoň polovina výnosu indexu PX (dnes zhruba 2,2 %).
5. Zbylo devět firem. Všechny jsou v indexu PX.

## Jak se počítají váhy

Skóre firmy se skládá ze dvou polovin:

- **50 % výše a kvalita dividendy.** Čistý dividendový výnos po dani (letošní skutečný a odhad na příští rok), upravený podle spolehlivosti: kolik let z posledních 10 firma platila, jestli dividendu snižovala, jakou část zisku rozdává a jestli dividenda roste.
- **50 % celkový očekávaný výnos.** Čistý dividendový výnos plus očekávaný dlouhodobý růst dividendy. Růst dividendy bereme jako odhad růstu ceny akcie, protože při stabilním podílu zisku, který se vyplácí, roste cena akcie obvykle podobně jako dividenda. Odhad růstu vychází z dividendové politiky a výhledu zisku každé firmy. Cílové ceny analytiků jsme nepoužili.

**Limity:** nejvýš 20 % na jednu firmu. Nižší strop u akcií, se kterými se málo obchoduje (20, 15, 10 nebo 5 % podle denního objemu). Nejvýš 5 % u firem s dividendovou historií kratší než 3 roky. Banky a pojišťovny dohromady nejvýš 55 %. Hotovost 2 %.

**Tři podmínky, které návrh měl splnit:**
1. Čistý dividendový výnos vyšší než u WOOD PX ETF. Za rok 2026 je 4,5 % proti 3,4 %. Za rok 2027 (odhad) je rozdíl menší: 4,2 % proti 3,7 %.
2. Aspoň 30 % portfolia rozloženo jinak než v ETF. Vychází těsně pod hranicí (29,8 %).
3. Banky a pojišťovny nejvýš 55 %. Vychází 52 % (ETF 68 %).

**Pozor:** interní zdroje se liší v tom, jak podmínku 1 formulují (rozdíl aspoň 1 procentní bod, nebo aspoň o 10 %) a jestli podmínku 2 splnila. Nepsat do článku, že všechny podmínky jsou splněné.

## Finální složení (zdroj: interní tabulka, sloupec Final)

| Titul | Váha | WOOD PX ETF | Proč |
|---|---|---|---|
| Komerční banka | 20 % | 18,0 % | Nejvyšší výnos, drží ji strop na jednu firmu |
| Moneta | 18 % | 13,5 % | Druhý nejvyšší výnos |
| ČEZ | 17 % | 20,4 % | Navýšeno oproti modelu, ale ne na strop: výnos je nízký a kolísavý |
| Philip Morris ČR | 10 % | 2,3 % | Vysoký výnos, drží ho limit obchodovatelnosti |
| VIG | 9 % | 16,4 % | Méně kvůli malému obchodu v Praze a optimistickému odhadu růstu |
| Colt CZ | 9 % | 3,6 % | Je nejvíc nadvážený proti ETF |
| Kofola | 5 % | 0,8 % | Limit obchodovatelnosti |
| Erste | 5 % | 20,0 % | Letos vyplatila málo, od příštího roku se má vracet k vyšším výplatám |
| Doosan Škoda Power | 5 % | 0,9 % | Strop pro nováčky, polovina letošní dividendy byla mimořádná |
| CSG | 0 % | 3,9 % | Zatím nevyplatila dividendu |
| Hotovost | 2 % | 0 % | Rezerva |

Banky a pojišťovny 52 %, dvě české banky dohromady 38 %. Zahraniční emitenti (VIG, Erste) 14 %.

## Výhled čistého dividendového výnosu (odhad, k dnešním cenám)

Výnos po dani (15 % u českých firem, 27,5 % u rakouských).

| Titul | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|
| Komerční banka | 6,3 % | 6,8 % | 7,0 % | 7,3 % |
| Moneta | 5,5 % | 5,8 % | 6,1 % | 6,5 % |
| Philip Morris ČR | 5,0 % | 4,9 % | 4,7 % | 4,6 % |
| Kofola | 3,6 % | 3,6 % | 3,7 % | 3,8 % |
| ČEZ | 3,1 % | 3,2 % | 3,4 % | 3,5 % |
| Colt CZ | 3,1 % | 3,2 % | 3,4 % | 3,5 % |
| Erste | 2,4–3,0 % | 3,3 % | 3,6 % | 3,7 % |
| VIG | 1,8 % | 1,9 % | 2,1 % | 2,2 % |

Odhady na rok 2027 u VIG, Philip Morris ČR, Doosanu a Erste jsou vlastní (z dividendové politiky a posledních výsledků), u ostatních se opírají o analytiky Fio banky. Po roce 2028 jsou hlavně vlastní. Je to odhad, ne údaj firem.

**Příklad pro čtenáře:** ze 100 000 Kč by strategie podle letošních dividend vyplatila zhruba 5 300 Kč hrubého a 4 500 Kč po dani. Výplaty chodí jen mezi dubnem a srpnem.

## Zvažované varianty a proč jsme je nevzali

- **Varianta A, čistě dividendová.** Dívala se jen na výši dividendy, ne na to, jestli firma poroste. Vynechala Erste. Vyplácela by o 0,2 procentního bodu víc (4,7 %), ale s horším výhledem růstu.
- **Varianta B, s cílovými cenami analytiků.** Pražské akcie sleduje jen pár analytiků, cílové ceny se často mění a váhy by byly nestabilní. ČEZ by měl jen 6 % a Philip Morris 17 %, skoro jako banky, přestože mu klesá dividenda i zisk.
- **Alternativní návrh kolegy (interní).** Finální složení je kompromis mezi modelem a tímto návrhem (ČEZ vyšší, Doosan nechán na 5 %).

## Co z toho plyne pro čtenáře (čemu učit)

1. **Dividendová past.** Nejvyšší dividendu platí Philip Morris ČR a Komerční banka, ale první má klesající zisk i dividendu a druhá rozdávala celý zisk a letos jej sníží. Otázky: Z čeho se dividenda platí? Dokáže firma platit i příští rok? Roste hodnota firmy?
2. **Celkový výnos = dividenda + růst ceny.** Vysoká dividenda a vysoký celkový výnos nejsou totéž.
3. **Koncentrace.** Pražská burza má málo firem a jsou v ní hlavně banky. Dvě české banky jsou 38 % návrhu.
4. **Malý trh.** Proč se u některých firem nedá koupit moc: denní obchod u Kofoly je zhruba 1 mil. Kč.
5. **Daně.** Z českých dividend se sráží 15 %. U rakouských firem (VIG, Erste) se sráží 27,5 %, část si klient může nechat vrátit. Dividendy se zdaňují každý rok, na rozdíl od akumulačního ETF.
6. **Dividenda není bonus.** O vyplacenou částku klesne cena akcie.

## Rizika (smí do článku jako vysvětlení)

- Příjem kolísá. V roce 2020 by klesl zhruba na polovinu, protože banky nevyplatily nic.
- Dvě české banky sdílejí stejného regulátora i riziko sektorové daně.
- Philip Morris ČR snižuje dividendu třetí období po sobě.
- Plán státu na plné ovládnutí ČEZ.

## Compliance a co NEPSAT

- **Žádné doporučení.** Nepsat „kupte", neslibovat výnos, neuvádět váhy jako návod na portfolio. Odhady výnosů výslovně označit jako odhady.
- **Interní věci do článku nepatří:** zrušení Pražské špičky a její objem, kapacita strategie (300 mil. Kč), doby prodeje, otázky pro operations, jména kolegů, komentáře nadřízených.
- **Historické výnosy strategie neuvádět.** Není to zpětný test výkonnosti: váhy jsou zvolené s dnešní znalostí.
- **Cílové ceny analytiků** zmínit nanejvýš jako příklad, proč se na ně nespoléhá.
- **Ověřit před publikací** všechna čísla k datu psaní, zejména ceny, kurz EUR/CZK (24,335 Kč k 10. 11. 2026), nové dividendy a výsledky CSG za 3. čtvrtletí.
- **Zmínka produktu Portu** podle KROKU 4 master promptu: maximálně jedna, dvě věty, jen pokud je strategie schválená. Jinak vynechat.

## Zdroje čísel

Burza cenných papírů Praha (ceny, váhy indexu PX, pravidla indexu), Fio banka (dividendy a odhady), ČNB (kurz), Patria Finance (srážkové daně), stránky firem. Úplný výpočet je v `vystupy/ceske-dividendy/Ceske-dividendy-vypocet.xlsx`, ale ten odpovídá dřívější verzi vah (čistě dividendové). Finální váhy jsou z interní tabulky výše.

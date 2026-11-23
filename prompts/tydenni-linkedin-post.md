# Týdenní LinkedIn post k aktuální tržní situaci

Spouští se automaticky každé pondělí ráno (naplánovaný úkol). Cíl: navrhnout autorovi (analytik investiční platformy Portu, píše pod svým jménem) nový LinkedIn post, který reaguje na to, co se skutečně dělo na trzích minulý týden, a čtenáři řekne něco, co se jinde nedozví. Autor návrh dostane jako notifikaci, upraví ho a zveřejní sám.

## 1. Příprava

Přečti si:
- `CLAUDE.md` (pravidla repozitáře),
- `.claude/agents/linkedin-posty.md` (pravidla pro LinkedIn posty: srozumitelnost, přesné pojmy, compliance, pokročilý analytický pohled),
- všechny vzory v `examples/linkedin-posty/`, hlavně `inspirace-tydenni-trh.md` (stavba posta, ke které se máme blížit) a `inspirace-odborny-styl.md`.

Zjisti dnešní datum. „Minulý týden“ je pondělí až pátek před ním.

## 2. Monitoring trhu za minulý týden

Zmapuj, co se dělo, a hledej **rozpor** mezi náladou a čísly:

- **Akcie:** S&P 500, Nasdaq-100, Euro Stoxx 50, PX, největší pohyby sektorů a velkých firem.
- **Sazby a makro:** výnosy státních dluhopisů, sazby ČNB / Fed / ECB (rozhodnutí a výhled), inflace, trh práce, dolar a koruna.
- **Komodity a ostatní:** zlato, ropa, bitcoin, volatilita (VIX).
- **Firmy:** výsledky hospodaření, které hýbaly trhem, a výsledky, které se chystají tento týden.
- **Kalendář na nadcházející týden:** co může hýbat trhem.
- **Ocenění:** forward P/E hlavních indexů a jak se liší od obvyklé úrovně (posledních 10 let).

Zdroje: nástroje `mcp__Portfolio__*` (ceny a konsenzus amerických firem), Trading Economics (pokud je dostupný), WebSearch (kalendář, titulky, ocenění indexů). Každé číslo ověř ve zdroji. Čísla, která ověřit nejde, vynech. Nepřebírej čísla z cizích postů.

## 3. Výběr tématu

Vyber **jedno** téma týdne, ne souhrn všeho. Nejlepší témata mají jednu z těchto podob:

- **Titulky vs. čísla:** trh reaguje na zprávu, ale čísla (zisky, ocenění, konsenzus) říkají něco jiného.
- **Co trh započítává do ceny:** jaký scénář cena předpokládá a jak je podle nás pravděpodobný.
- **Mýtus k vyvrácení:** populární vysvětlení pohybu, které čísla nepotvrzují.
- **Zajímavý historický rozměr:** nejvíc / nejméně od roku X, vůči posledním 10 letům.
- **Jeden mechanismus, který většina nevidí** (např. jak sazby ovlivňují ocenění, proč se přelévá kapitál mezi sektory).

Klidný týden bez výrazného pohybu je také téma: napiš, proč je klid zajímavý (co se pod povrchem hýbe).

## 4. Psaní posta

Stavba podle `inspirace-tydenni-trh.md`:

1. Hook: silné hodnocení týdne + jedno konkrétní číslo ve srovnání.
2. Teze: co trh hledá a co z toho je skutečný důvod. Odmítni populární vysvětlení, pokud nesedí.
3. Jedno fundamentální riziko nebo jeden mechanismus, vysvětlený lidsky.
4. Co trh podle cen započítává a jak pravděpodobné to podle autora je (vlastní analytický názor).
5. Pointa jednou větou (nebo to, co autor bude sledovat tento týden).

Pravidla:
- Krátké odstavce, bez odrážek, mezititulků, šipek, emoji, hashtagů a disclaimeru.
- Odborné pojmy vysvětli v téže větě (forward P/E = cena vůči očekávaným ziskům).
- Piš silně a konkrétně. Žádné „uvidíme“, žádné obecné fráze, žádný souhrn týdne po bodech.
- Čísla vždy ve srovnání. U cen akcií a indexů uveď v poznámkách, k jakému dni platí.
- **Compliance:** žádné „kupte“, „příležitost“, „ideální čas“, žádné vlastní pozice, žádný slib výnosu. Nízké ocenění popiš jako pozorování a vlastní názor, ne jako výzvu.
- Délku řiď tématem (obvykle kratší, do ~1 500 znaků).

## 5. Graf (návrh)

Navrhni jeden graf, který celé sdělení ukáže na první pohled (např. ocenění indexů vůči posledním 10 letům, vývoj ukazatele, srovnání dvou čísel): co na osách, jaká data a odkud. Pokud máš ověřená data, graf vykresli přes `nastroje/portu_grafy.py` (pravidla subagenta `portu-grafy`) do `vystupy/grafy/`.

## 6. Výstup

- Ulož návrh do `vystupy/linkedin/RRRR-MM-DD-tydenni-trh.md`: post, 2 alternativní hooky, 2 alternativní úhly na jiné téma týdne, poznámky (čísla a zdroje s datem, co se nepodařilo ověřit, compliance riziko).
- Zprávu o dokončení začni **jednou větou**, o čem návrh je (úhel a hlavní číslo), protože ji autor uvidí v notifikaci. Pod ní uveď celý post k zkopírování a poznámky.
- Nezakládej pull request. Návrh stačí uložit a commitnout na větev session.

# Archiv názorových článků

Vzorové názorové články hlavního ekonoma Portu Jana Berky ze série **„Názor hlavního ekonoma: …“** na [Portu Magazínu](https://magazin.portu.cz/). Slouží subagentovi `nazorove-clanky` (`.claude/agents/nazorove-clanky.md`) jako závazný vzor pro délku, stavbu, tón a způsob, jakým autor dojde k pointě. Rozbor stylu je v kapitole 2 promptu agenta.

Články jsou uložené **doslova**, ve verzi z magazínu (text bez grafů, místo obrázku je značka `[GRAF]`). Stáhl je skript `python3 -I nastroje/nazorove-clanky-z-magazinu.py`. Stejným příkazem se doplní nové články série, které ve složce ještě nejsou. Přepínač `--seznam` jen vypíše posledních 15 článků.

Na magazínu vycházejí články s nadpisem „Názor hlavního ekonoma: …“, s automatickým boxem upozornění (není investiční doporučení…) a s profilem autora. Nic z toho autor nepíše do textu.

## Hlavní vzory

Pokud nestihneš přečíst všechny, přečti aspoň tyto. Pokrývají typy článků, které se v sérii opakují.

| Soubor | Proč je vzorem |
|---|---|
| `2026-01-16-muze-americka-centralni-banka-prijit-o-svou-kredibilitu.md` | Otázka v titulku, teze hned ve 2. odstavci („Podle mého názoru…“), dva argumenty „Zaprvé, zadruhé“, závěr s historickou paralelou. |
| `2026-06-04-lepsi-prilezitosti-pro-reformu-duchodu-jsme-uz-promarnili.md` | Česká politika srozumitelně pro každého, teze v první větě, zahraniční srovnání s číslem, úderná poslední věta. |
| `2026-05-11-ucetni-upravy-ceske-vlady-investory-neoklamou.md` | Titulek jako teze, vyvracení rozšířených argumentů („Často zaznívá… To je pravda. … však…“), mechanismus v krocích. |
| `2026-08-18-proc-akcie-nepadaji-kdyz-vynosy-rostou.md` | Odpověď na otázku, kterou si klade každý investor, srovnání s rokem 2022, práce s grafem. |
| `2025-10-03-zlato-pojd-na-to.md` | Slovní hříčka v titulku, příčiny růstu jedna po druhé, osobní pohled autora na vlastní portfolio. |
| `2025-09-19-kdyz-je-centralni-banker-v-roli-ornitologa.md` | Vtipný obrazný úvod (holubice, jestřáb, andulka), který se vrátí v závěru. |
| `2026-02-06-oo-aneb-ozdravne-odpakovani.md` | Nejkratší článek série (1 300 znaků): tři odstavce a jasné poselství pro dlouhodobého investora. |
| `2026-10-14-rekordni-index-jeste-neznamena-silny-trh.md` | Nejdelší a nejnovější, s mezititulky a závěrečným oddílem „Jak přemýšlíme v Portu“ (ten patří jen do verze pro magazín). |

## Všechny články

| Soubor | Vyšlo | Titulek (bez „Názor hlavního ekonoma:“) | Znaků |
|---|---|---|---|
| `2026-10-14-rekordni-index-jeste-neznamena-silny-trh.md` | 14. 10. 2026 | Rekordní index ještě neznamená silný trh | 6 272 |
| `2026-09-15-jen-aby-trh-nedohnal-fed-k-menovepoliticke-chybe.md` | 15. 9. 2026 | Jen aby trh nedohnal Fed k měnověpolitické chybě | 1 614 |
| `2026-09-09-a-jsme-zpatky-u-inflace.md` | 9. 9. 2026 | A jsme zpátky u inflace | 2 136 |
| `2026-08-31-nastrahy-ceskeho-dluhu.md` | 31. 8. 2026 | Nástrahy českého dluhu | 2 185 |
| `2026-08-24-debasement-trade-vol-2.md` | 24. 8. 2026 | Debasement trade vol. 2 | 3 323 |
| `2026-08-18-proc-akcie-nepadaji-kdyz-vynosy-rostou.md` | 18. 8. 2026 | Proč akcie nepadají  když výnosy rostou? | 2 345 |
| `2026-08-04-spolecna-obrana-jenu-zrodil-se-novy-intervencni-rezim.md` | 4. 8. 2026 | Společná obrana jenu. Zrodil se nový intervenční režim? | 5 867 |
| `2026-06-26-trhy-zatim-recesi-nevidi-co-ukazuje-cross-asset-pohled.md` | 26. 6. 2026 | Trhy zatím recesi nevidí. Co ukazuje cross-asset pohled | 2 760 |
| `2026-06-17-novy-sef-americke-centralni-banky-trhy-nezaujal.md` | 17. 6. 2026 | Nový šéf americké centrální banky trhy nezaujal | 2 880 |
| `2026-06-04-lepsi-prilezitosti-pro-reformu-duchodu-jsme-uz-promarnili.md` | 4. 6. 2026 | Lepší příležitosti pro reformu důchodů jsme už promarnili | 2 290 |
| `2026-05-20-co-stoji-za-posilovanim-americkeho-dolaru.md` | 20. 5. 2026 | Co stojí za posilováním amerického dolaru? | 2 434 |
| `2026-05-11-ucetni-upravy-ceske-vlady-investory-neoklamou.md` | 11. 5. 2026 | Účetní úpravy české vlády investory neoklamou | 2 822 |
| `2026-04-21-bude-svet-potrebovat-jeste-vic-dolaru.md` | 21. 4. 2026 | Bude svět potřebovat ještě víc dolarů? | 4 718 |
| `2026-04-02-trhy-jsou-jako-john-travolta.md` | 2. 4. 2026 | Trhy jsou jako John Travolta | 3 342 |
| `2026-03-20-trhy-otocily-misto-poklesu-sazeb-cekaji-rust.md` | 20. 3. 2026 | Trhy otočily. Místo poklesu sazeb čekají růst | 2 878 |
| `2026-03-09-proc-tentokrat-bezpecne-pristavy-selhavaji.md` | 9. 3. 2026 | Proč tentokrát bezpečné přístavy selhávají | 5 340 |
| `2026-03-04-volatilita-a-trump-na-tenkem-lede.md` | 4. 3. 2026 | Volatilita a Trump na tenkém ledě | 2 268 |
| `2026-02-23-slabe-misto-trumpovych-cel.md` | 23. 2. 2026 | Slabé místo Trumpových cel? | 2 915 |
| `2026-02-19-jak-by-mohla-vypadat-spoluprace-fedu-a-ministerstva-financi.md` | 19. 2. 2026 | Jak by mohla vypadat spolupráce Fedu a ministerstva financí? | 4 205 |
| `2026-02-13-japonsko-zeme-vychazejiciho-slunce-rustu-a-zisku.md` | 13. 2. 2026 | Japonsko – země vycházejícího slunce  růstu a zisků? | 5 149 |
| `2026-02-06-oo-aneb-ozdravne-odpakovani.md` | 6. 2. 2026 | „OO“ aneb Ozdravné odpákování | 1 317 |
| `2026-01-29-povede-dolarove-deja-vu-od-buy-america-k-bye-america.md` | 29. 1. 2026 | Povede dolarové déjà vu od Buy America k Bye America? | 3 455 |
| `2026-01-21-problem-japonskeho-dluhopisoveho-trhu.md` | 21. 1. 2026 | Problém japonského dluhopisového trhu | 4 135 |
| `2026-01-16-muze-americka-centralni-banka-prijit-o-svou-kredibilitu.md` | 16. 1. 2026 | Může americká centrální banka přijít o svou kredibilitu? | 2 100 |
| `2026-01-09-za-posledni-rok-si-pujcujeme-draz-bude-hur.md` | 9. 1. 2026 | Za poslední rok si půjčujeme dráž. Bude hůř? | 3 395 |
| `2025-12-17-pokud-technologiim-dojde-dech-americka-ekonomika-bude-mit-pr.md` | 17. 12. 2025 | Pokud technologiím dojde dech  americká ekonomika bude mít problém | 4 087 |
| `2025-12-11-jeste-silnejsi-a-produktivnejsi-americka-ekonomika-nez-jsme.md` | 11. 12. 2025 | Ještě silnější a produktivnější americká ekonomika než jsme čekali | 3 087 |
| `2025-12-05-americka-centralni-banka-zacne-opet-nakupovat-aktiva.md` | 5. 12. 2025 | Americká centrální banka začne opět nakupovat aktiva | 4 426 |
| `2025-11-28-co-by-vydesilo-veritele-ceskeho-statniho-dluhu.md` | 28. 11. 2025 | Co by vyděsilo věřitele českého státního dluhu? | 3 579 |
| `2025-11-21-trump-data-neschovava-byl-by-sam-proti-sobe.md` | 21. 11. 2025 | Trump data neschovává. Byl by sám proti sobě | 4 619 |
| `2025-11-13-ukonceni-shutdownu-muze-do-hry-vratit-sazky-na-slaby-dolar.md` | 13. 11. 2025 | Konec shutdownu může do hry vrátit sázky na slabý dolar | 4 484 |
| `2025-11-06-vyrazne-mene-prifouknuta-bublina.md` | 6. 11. 2025 | Výrazně méně přifouknutá bublina? | 3 501 |
| `2025-10-30-kdyz-jsou-si-trhy-az-prilis-jiste-prekvapeni-boli-nejvic.md` | 30. 10. 2025 | Když jsou si trhy až příliš jisté  překvapení bolí nejvíc | 2 608 |
| `2025-10-24-co-je-jinak-na-dluhopisovem-trhu.md` | 24. 10. 2025 | Co je jinak na dluhopisovém trhu | 3 041 |
| `2025-10-17-co-bude-motorem-dalsiho-rustu-americkych-akcii.md` | 17. 10. 2025 | Co bude motorem dalšího růstu amerických akcií? | 3 723 |
| `2025-10-10-po-volbach-s-vetsim-dluhem-a-vyssimi-sazbami.md` | 10. 10. 2025 | Po volbách s větším dluhem a vyššími sazbami? | 2 443 |
| `2025-10-03-zlato-pojd-na-to.md` | 3. 10. 2025 | Zlato  pojď na to! | 4 021 |
| `2025-09-26-bude-silna-koruna-stacit-ke-snizeni-sazeb.md` | 26. 9. 2025 | Bude silná koruna stačit ke snížení sazeb? | 2 513 |
| `2025-09-19-kdyz-je-centralni-banker-v-roli-ornitologa.md` | 19. 9. 2025 | Když je centrální bankéř v roli ornitologa | 2 337 |
| `2025-09-05-akcie-ani-dluhopisy-v-zari-prilis-nezari.md` | 5. 9. 2025 | Akcie ani dluhopisy v září příliš nezáří | 3 461 |
| `2025-08-27-sazka-na-krizi-ktera-se-nevyplaci.md` | 28. 8. 2025 | Sázka na krizi  která se nevyplácí | 3 491 |
| `2025-08-22-vesteni-z-kristalove-koule-americkeho-trhu-prace.md` | 22. 8. 2025 | Věštění z křišťálové koule amerického trhu práce | 3 442 |
| `2025-08-15-na-levnejsi-uvery-si-budeme-muset-pockat.md` | 15. 8. 2025 | Na levnější úvěry si budeme muset počkat | 3 987 |
| `2025-08-07-kdo-bude-pristim-sefem-americke-centralni-banky.md` | 7. 8. 2025 | Kdo bude příštím šéfem americké centrální banky? | 3 407 |
| `2025-08-01-historie-nahrava-rebelujicim-centralnim-bankerum.md` | 1. 8. 2025 | Historie nahrává „rebelujícím“ centrálním bankéřům | 3 322 |
| `2025-07-24-trh-sazi-na-to-ze-donald-trump-vymekne.md` | 24. 7. 2025 | Trh sází na to  že Donald Trump vyměkne | 3 130 |
| `2025-07-18-kdyz-politik-keca-do-prace-centralnim-bankerum-nevesti-to-ni.md` | 18. 7. 2025 | Když politik kecá do práce centrálním bankéřům  nevěstí to nic dobrého | 2 981 |

Nové hotové články ukládá agent do `vystupy/nazorove-clanky/`. Když článek vyjde, doplní ho sem skript, případně finální verzi z médií uloží agent ručně (s médiem a datem vydání).

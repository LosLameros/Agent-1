# Rešerše: jak se AI používá při investování (stav k 29. 10. 2026)

Podklad pro nový obsah workshopu. Zdroje: přepisy YouTube videí (2 přepisy, pak YouTube další stahování zablokoval), přehled ~100 letošních videí podle sledovanosti, průzkumy a články. U každého čísla je zdroj; co je označené „ověřit“, se mění rychle a před workshopem se musí zkontrolovat.

## 1. Kolik lidí AI používá (jen nezávislé zdroje, zaměřené na ČR)

- **ČSÚ, šetření ICT v domácnostech (2025):** nástroje AI pro tvorbu obsahu používalo 32 % Čechů starších 16 let. Ve věku 16–24 let 78 %, nad 65 let 4 %. Mezi vysokoškoláky v produktivním věku 60 %.
- **Ipsos / Zlatá koruna (červenec 2025, 1 010 lidí):** AI ve financích využívá 19 % Čechů. 70 % vidí přínos v jednoduchém vysvětlení finančních pojmů. 49 % si myslí, že AI může nahradit poradce, 25 % by dalo přednost AI poradci před lidským.
- **Deloitte TMT Highlights ČR 2026 (květen 2026):** AI aspoň občas používá 78 % Čechů, víc než trojnásobek proti roku 2023. Nejpoužívanější je ChatGPT. Pozor, vzorek je jen 341 lidí.
- **Vyřazeno, protože jde o konkurenci:** Amundi (správce fondů), eToro a XTB (brokeři), OVB (poradenská firma), Raiffeisenbank (banka). Investing.com vyřazen, je to americký vzorek.

## 2. Co lidé s AI při investování skutečně dělají (nejčastější scénáře z videí a návodů)

| Scénář | Typický nástroj | Poznámka |
|---|---|---|
| Shrnutí dlouhých dokumentů (výroční zprávy, výsledky firem, dokumenty k fondům) | Claude, ChatGPT, NotebookLM | Nejčastější a nejspolehlivější použití. Doporučený postup: dát AI originální dokument a úzkou otázku, chtít odkaz na stranu. |
| Vysvětlení pojmů a souvislostí | všechny | Ipsos: 70 % Čechů v tom vidí přínos. |
| Kontrola poplatků a hledání levnější alternativy | Claude, ChatGPT | Příběh z podcastu s CEO Robinhoodu (Iced Coffee Hour, 2026): moderátor nahrál portfolio do Claude, AI našla fond s vyšším poplatkem, než má téměř stejný levnější fond. Úspora 16 000 USD ročně. |
| Modelování budoucího vývoje (spoření, renta, cíle) | ChatGPT (počítá v Pythonu), Claude | Bez instrukcí AI často zapomíná na poplatky (podnět odborníka). |
| Trvalé instrukce a projekty („Projects“, „Gems“) | Claude, ChatGPT, Gemini | AI si pamatuje cíle, horizont a pravidla. Claude má Projekty i ve verzi zdarma od února 2026 (ověřit). |
| Proč se hýbe akcie, zprávy se zdroji | Perplexity Finance, Google Finance (Gemini Deep Search) | Google Finance s AI spuštěn v Evropě 11. 5. 2026 s místními jazyky (češtinu ověřit). Perplexity Finance: aktuální kurzy, výsledky, odkazy na podání firem. |
| Hledání firem k tématu | všechny s webem | Výstup je začátek rešerše, ne seznam k nákupu. |
| Rentgen portfolia (překryvy ETF, koncentrace) | ChatGPT, Claude s webem | Mark Tilbury (2,95 mil. zhlédnutí): 10 největších firem tvoří asi 40 % S&P 500, Nvidia sama 7–8 % (ověřit aktuální váhy). |
| Analýza výdajů z výpisu | ChatGPT, Claude | Stačí CSV se sloupci datum, popis, částka. Osobní údaje smazat. Součty kontrolovat. |

## 3. Novinky a trendy 2026

- **AI napojená na účty:** ChatGPT „Finances“ (od května 2026, jen USA, Plus/Pro) propojí přes Plaid banky i brokery a jen čte: výdaje, čisté jmění, rozložení portfolia. Peníze hýbat nemůže.
- **AI agenti, kteří obchodují:** Robinhood (květen 2026) „agentic trading“. Uživatel napojí vlastního AI agenta (Claude, Codex…), přes 100 000 lidí si takový účet založilo. CEO Vlad Tenev: největší změna přijde u aktivního obchodování, u pasivního dlouhodobého investování podle něj „moc ne, rozložení portfolia už je dobře zautomatizované“. Lidé AI používají hlavně jako „sanity check“ rady poradce.
- **Brokeři mají vlastní AI asistenty:** Robinhood Cortex, Public Alpha, eToro, Schwab, Fidelity.
- **Google Finance s AI** (Deep Search s citacemi, „Key Moments“, data z predikčních trhů): v Evropě od května 2026.
- **NotebookLM:** z nahraných dokumentů udělá audio i video shrnutí, myšlenkovou mapu a kvíz (asi 80 jazyků). Odpovídá jen z vašich zdrojů a cituje je.
- **Anthropic pro finanční firmy (květen 2026):** 10 šablon agentů, Claude v Excelu. Je to pro profesionály, ne pro drobné investory. Ukazuje ale, že i profesionálové používají AI na rešerše a shrnutí.
- **Pokusy „AI investuje za mě“:** Alpha Arena (Seznam Zprávy, 8. 5. 2026): 8 modelů, dva týdny, americké technologické akcie, v zisku jen 6 z 32 výsledků. Pokus Forbes.cz s fiktivním milionem (vyhodnocení 7/2026, za paywallem). YouTube je plný videí typu „Dal jsem AI 1 000 dolarů“. Shoda: AI je silná v rešerši, ne ve věštění.

## 4. Bezpečnost (jako tipy, ne jako strašení)

- ChatGPT, Gemini i spotřebitelský Claude se mohou učit na konverzacích **i u placených verzí**. Rozhoduje přepínač v nastavení (ChatGPT: Data Controls → „Improve the model for everyone“; Claude: Privacy → „Help improve Claude“). Firemní verze se neučí. Ověřeno ze sekundárních zdrojů, před workshopem zkontrolovat.
- Deepfake investiční podvody: ČNB varuje před videi se známými osobnostmi vyrobenými pomocí AI. Případ z Nového Jičína: seniorka přišla o 3,2 mil. Kč. Ověření poskytovatele v registru ČNB.

## 5. YouTube: co se letos sleduje (výběr)

| Video | Kanál | Zhlédnutí | Stáří |
|---|---|---|---|
| I'm Changing How I Invest My Money Because of AI | Mark Tilbury | 2,95 mil. | 7 měs. |
| Claude Just Changed the Stock Market Forever! (Tutorial) | Samin Yasar | 1,82 mil. | 6 měs. |
| This Gemini/NotebookLM System Will Make You SO Smart… | Sandeep Swadia | 1,48 mil. | 6 měs. |
| Complete Guide to building an AI Trading Bot with Claude | Ray Fu | 491 tis. | 1 měs. |
| I Let AI Invest for Me on Trading 212 | Financial Interest | 486 tis. | 2 měs. |
| This Perplexity + NotebookLM Workflow Is Incredible! | Paul J Lipsky | 271 tis. | 9 měs. |
| Claude's New Trading Agent Is Insane! | Samin Yasar | 260 tis. | 3 měs. |
| Everything I've Learned Trading With Claude In 18 Minutes | AI Pathways | 203 tis. | 5 měs. |
| Robinhood's CEO Explains How AI Will CHANGE Investing | Iced Coffee Hour | 180 tis. | 1 měs. |
| How we use AI in practice (AI Summit 2026) | Norges Bank Investment Management | 79 tis. | 7 měs. |
| How to Use ChatGPT's NEW Personal Finance Feature | Chris Verzwyvelt | 30 tis. | 5 měs. |
| I Gave ChatGPT Complete Control Of My Stock Trades | Ryan Scribner | 63 tis. | 2 týd. |
| Jak používám umělou inteligenci při investování do akcií | Jindřich Pokora | 4,4 tis. | 10 měs. |
| AI v investování: Co funguje a co je slepá cesta? | ValueClub | 1,3 tis. | 2 měs. |
| AI mění investování. Rozhoduje ale pořád lidský důvtip | Investicniweb | 1,2 tis. | 5 měs. |

Co z toho plyne pro workshop:
- Nejsledovanější jsou **konkrétní návody krok za krokem** („Tutorial“, „Workflow“, „System“) a **osobní příběhy** („I'm changing how I invest“, „Everything I've learned“).
- Obecné povídání o AI se nesleduje.
- Česká videa o *používání* AI k investování mají jednotky tisíc zhlédnutí. Česky tohle téma skoro nikdo pořádně nedělá, a to je pro Portu příležitost.

## Zdroje

- ČSÚ: https://csu.gov.cz/produkty/umelou-inteligenci-pouziva-tretina-populace
- Deloitte TMT Highlights ČR 2026: https://www.deloitte.com/cz-sk/cs/about/press-room/ai-se-stava-beznou-soucasti-zivota-cechu.html
- Ipsos / Zlatá koruna: https://www.ipsos.com/sites/default/files/ct/news/documents/2025-08/Vyzkum_Zlata-koruna_2025.pdf
- ChatGPT Finances: https://help.openai.com/en/articles/20001222-finances-in-chatgpt
- Robinhood agenti a asistenti brokerů: https://walnutinvest.com/resources/which-brokers-have-an-ai-assistant
- Rozhovor s CEO Robinhoodu: https://www.youtube.com/watch?v=McuukLvvMX4
- Mark Tilbury: https://www.youtube.com/watch?v=O8t50OxsfB8
- Google Finance v Evropě: https://ppc.land/google-finance-ai-lands-in-europe-with-deep-search-now-global/
- Perplexity Finance: https://helmterminal.dev/blog/perplexity-stock-research
- Srovnání nástrojů: https://helmterminal.dev/blog/best-ai-for-stock-research
- Claude postupy pro rešerše: https://helmterminal.dev/blog/claude-stock-analysis
- NotebookLM 2026: https://glasp.ai/articles/notebooklm-2026
- Anthropic pro finanční služby: https://www.marketsmedia.com/anthropic-introduces-agents-for-financial-services/
- Claude zdarma s Projekty: https://ivee.jobs/blog/free-ai-tools-claude-gemini-chatgpt
- Učení na datech: https://www.techcrunch.com/2025/08/28/anthropic-users-face-a-new-choice-opt-out-or-share-your-data-for-ai-training
- Alpha Arena: https://www.seznamzpravy.cz/clanek/ekonomika-umela-inteligence-trh-neporazila-pri-pokusu-na-burzach-modely-prodelaly-305739
- Výpisy z účtu: https://thesolocreators.com/prompts/spending-habits-hiding-in-statements/
- ČNB deepfake: https://www.cnb.cz/cs/cnb-news/aktuality/Upozorneni-Podvodne-video-zneuziva-podvrzene-zabery-guvernera.-Pokud-naletite-muzete-prijit-o-vsechno

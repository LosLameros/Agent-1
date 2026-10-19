# Agent-1 — Portu newsletter

Repozitář slouží ke psaní newsletterů pro Portu (česko-slovenská investiční platforma) ve stálém, zavedeném stylu.

## Struktura

- `examples/newsletters/` — archiv 10 vydání (`.docx`), reálné podklady pro styl. Čísla v názvech souborů (443–452) **neodpovídají 1:1** číslu vydání psanému uvnitř dokumentu (např. `446.docx` obsahuje vydání „#445“, `452.docx` obsahuje „#451“). Soubory `444.docx`/`445.docx` a `450.docx`/`451.docx` jsou vzájemné duplicity — reálně jde o 8 unikátních vydání.
- `.claude/agents/portu-newsletter-writer.md` — subagent, který na základě dodaných faktů/zpráv napíše nové vydání v tomto stylu. Použij ho příkazem přes Agent tool (`subagent_type: portu-newsletter-writer`) nebo o něj požádej přímo.
- `.claude/agents/Čtvrtletní zprávy.md` — subagent `ctvrtletni-zpravy`, píše čtvrtletní zprávu „Komentář k vývoji portfolií“ za poslední uzavřené čtvrtletí. Vzorové zprávy (2Q 2025 – 3Q 2026) jsou v `examples/quarterly-reports/`. Grafy za aktuální čtvrtletí patří do `podklady/RRRR-Qn/`, hotové zprávy agent ukládá do `vystupy/ctvrtletni-zpravy/`.
- `.claude/agents/linkedin-posty.md` — subagent `linkedin-posty`, píše krátké a úderné LinkedIn příspěvky (1. osoba, česky) o autorových výstupech v TV/rádiu/podcastech, článcích a komentářích v médiích: hook → kontext → shrnutí → takeaway → odkaz (bez šipek, mezititulků a hashtagů). Hotové posty (na požádání) ukládá do `vystupy/linkedin/`.
- `.claude/agents/tv-vystupy.md` — subagent `tv-vystupy`, připravuje na výstupy v TV/rádiu: na okruhy od redakce (a případné poznámky hlavního ekonoma, které ověří) napíše srozumitelné mluvené odpovědi pro běžné diváky a pod každou otázku shrnutí v bodech na naučení. Podklady ukládá do `vystupy/tv/`.
- `.claude/agents/komentare-do-medii.md` — subagent `komentare-do-medii`, píše odborné komentáře pro novináře (odpověď na otázku, sadu otázek, komentář k události, komentář ke čtvrtletním výsledkům firem) a kontroluje uživatelem přepsané verze. Vzory jsou v `examples/komentare/` (uložené doslova, i s chybami, které agent nemá opakovat), hotové komentáře ukládá do `vystupy/komentare/`. U čtvrtletních výsledků navazuje na komentář ke stejné firmě z minulého čtvrtletí.
- `.claude/agents/Tisková zpráva o inflaci.md` — subagent `tiskova-zprava-inflace`, píše měsíční tiskovou zprávu o inflaci (ČR + evropské srovnání, „Inflace ve světě“: eurozóna + ECB, USA + Fed, Čína) za poslední ukončený měsíc, vše z Trading Economics. Vzory jsou v `examples/tiskove-zpravy-inflace/` (nejnovější slouží i jako šablona Wordu), hotové zprávy ukládá do `vystupy/tiskove-zpravy-inflace/`. Pořadí ČR v Evropě počítá `nastroje/poradi-inflace.py`, Word vyrábí `nastroje/tz-inflace-do-wordu.py`.
- `prompts/clanky-portu.md` — master prompt pro články do Portu Magazínu (vstupní proměnné, rešerše, struktura, styl, produktové napojení, compliance, sebekontrola).

## Styl newsletteru Portu

Vychází z analýzy 8 unikátních vydání (#443–#451, ~1300 slov/vydání). Kompletní pravidla viz system prompt agenta; shrnutí:

- **Formát:** na prvním řádku `Návrhy na nadpis: xxx // xxx // xxx // xxx` (čtyři kandidáti na název vydání), pak `#číslo - opener`, pak odstavec s týdenním shrnutím trhů (nálada týdne jednou větou → konkrétní % pohyby indexů), pak 12–20 samostatných zpráv, sekce „Co nového v Portu?“ na konci, sign-off „Hezký víkend!“.
- **Zprávy:** jedno téma = právě jeden odstavec (nikdy nerozdělovat ani neslučovat). Každý odstavec **max. 700 znaků včetně mezer** (medián v archivu je 554, 92 % odstavců je pod 700).
- **Opener:** úderný nadpis odstavce, ideálně 2–3 slova, **maximálně 4 slova**, ideálně vtipný (hříčka, otázka, narážka) a musí okamžitě shrnout celý odstavec.
- **Věty:** krátké, aktivní rod (trpný rod prakticky nepoužívat), vzorec fakt/číslo → kontext/příčina → důsledek nebo odlehčený komentář.
- **Čísla:** vysoká hustota (cca 1 číslo na 2 věty), vždy v kontextu srovnání (meziročně, „nejvíce od...“, vs. konkurence), ne holá čísla.
- **Tón:** věcný, mírně ironický/vtipný, nikdy bulvární ani vulgární. Žádná přímá investiční doporučení („kupte/prodejte“), žádné emoji, žádný žargon bez vysvětlení v téže větě, žádné dlouhé souvětí.

## Články pro Portu Magazín

Při psaní článků pro Portu Magazín vždy dodržuj strukturu a pravidla ze souboru `prompts/clanky-portu.md`.

## Spolupráce

- Čtvrtletní zprávy existují ve dvou verzích (`.md` a `.docx` ve `vystupy/ctvrtletni-zpravy/`). Každou úpravu textu proveď v `.md` a hned znovu vygeneruj Word přes `node nastroje/zprava-do-wordu.js <md> <podklady/RRRR-Qn> <docx>`, aby byly obě verze vždy stejné.
- Tiskové zprávy o inflaci platí totéž: každou úpravu proveď v `.md` ve `vystupy/tiskove-zpravy-inflace/` a hned znovu vygeneruj Word přes `python3 -I nastroje/tz-inflace-do-wordu.py <md> "<TZ inflace - měsíc RRRR.docx>" --autor "Jméno Příjmení" --aum $(node nastroje/portu-aum.js)` (číslo `--aum` je aktuální objem zainvestovaných peněz z portu.cz).
- Před odesláním čtvrtletní zprávy i každé navržené úpravy (i jen jedné věty) ji zkontroluj podle odborné revize v kapitole 8a promptu `.claude/agents/Čtvrtletní zprávy.md`.
- Připomínka nebo dotaz od uživatele **neznamená automaticky požadavek na změnu**. Uživatel chce kritický názor a samostatný postoj: nejdřív posuď, zda má připomínka pravdu, a obhaj nebo uprav své řešení podle faktů. Měň jen to, co je opravdu potřeba, a když nesouhlasíš, řekni proč.

## Poznámka

Newsletter vždy píšeme v češtině.

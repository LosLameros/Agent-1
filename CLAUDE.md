# Agent-1 — Portu newsletter

Repozitář slouží ke psaní newsletterů pro Portu (česko-slovenská investiční platforma) ve stálém, zavedeném stylu.

## Struktura

- `examples/newsletters/` — archiv 10 vydání (`.docx`), reálné podklady pro styl. Čísla v názvech souborů (443–452) **neodpovídají 1:1** číslu vydání psanému uvnitř dokumentu (např. `446.docx` obsahuje vydání „#445“, `452.docx` obsahuje „#451“). Soubory `444.docx`/`445.docx` a `450.docx`/`451.docx` jsou vzájemné duplicity — reálně jde o 8 unikátních vydání.
- `.claude/agents/portu-newsletter-writer.md` — subagent, který na základě dodaných faktů/zpráv napíše nové vydání v tomto stylu. Použij ho příkazem přes Agent tool (`subagent_type: portu-newsletter-writer`) nebo o něj požádej přímo.
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

## Poznámka

Newsletter vždy píšeme v češtině.

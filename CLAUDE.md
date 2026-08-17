# Agent-1 — Porto newsletter

Repozitář slouží ke psaní newsletterů pro Portu (česko-slovenská investiční platforma) ve stálém, zavedeném stylu.

## Struktura

- `examples/newsletters/` — archiv 10 vydání (`.docx`), reálné podklady pro styl. Čísla v názvech souborů (443–452) **neodpovídají 1:1** číslu vydání psanému uvnitř dokumentu (např. `446.docx` obsahuje vydání „#445“, `452.docx` obsahuje „#451“). Soubory `444.docx`/`445.docx` a `450.docx`/`451.docx` jsou vzájemné duplicity — reálně jde o 8 unikátních vydání.
- `.claude/agents/porto-newsletter-writer.md` — subagent, který na základě dodaných faktů/zpráv napíše nové vydání v tomto stylu. Použij ho příkazem přes Agent tool (`subagent_type: porto-newsletter-writer`) nebo o něj požádej přímo.

## Styl newsletteru Portu

Vychází z analýzy 8 unikátních vydání (#443–#451, ~1300 slov/vydání). Kompletní pravidla viz system prompt agenta; shrnutí:

- **Formát:** `#číslo - úderný titulek (2–4 slova)`, pak odstavec s týdenním shrnutím trhů (nálada týdne jednou větou → konkrétní % pohyby indexů), pak 12–20 samostatných zpráv (tučný/úderný nadpis, často otázka nebo slovní hříčka + 3–6 vět), sekce „Co nového v Portu?“ na konci, sign-off „Hezký víkend!“.
- **Věty:** krátké, aktivní rod (trpný rod prakticky nepoužívat), vzorec fakt/číslo → kontext/příčina → důsledek nebo odlehčený komentář.
- **Čísla:** vysoká hustota (cca 1 číslo na 2 věty), vždy v kontextu srovnání (meziročně, „nejvíce od...“, vs. konkurence), ne holá čísla.
- **Tón:** věcný, mírně ironický/vtipný, nikdy bulvární ani vulgární. Žádná přímá investiční doporučení („kupte/prodejte“), žádné emoji, žádný žargon bez vysvětlení v téže větě, žádné dlouhé souvětí.

## Poznámka

Newsletter vždy píšeme v češtině.

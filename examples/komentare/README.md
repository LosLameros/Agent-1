# Archiv komentářů do médií

Vzorové komentáře, které analytik Portu poslal do redakcí. Slouží subagentovi `komentare-do-medii` (`.claude/agents/komentare-do-medii.md`) jako podklad pro styl a strukturu.

Texty jsou uložené **doslova**. Slouží k tomu, aby agent poznal, na jaké typy otázek se média ptají a jak na ně analytik odpovídá (typologie je v kapitole 3a promptu agenta). Agent z nich přebírá stavbu a způsob uvažování.

| Soubor | Typ | Téma |
|---|---|---|
| `2026-09-volkswagen-dodavatele.md` | odpověď na otázku novináře | Kolik vyváží Česko do koncernu VW a kdo jsou hlavní dodavatelé |
| `2026-09-volkswagen-zavirani-tovaren.md` | obecný komentář k události | Zavírání továren VW v Německu, německý průmysl a dopad na Česko |
| `2026-08-vysledky-nvidia-microsoft-alphabet.md` | komentář ke čtvrtletním výsledkům | Nvidia, Microsoft, Alphabet |
| `2026-e15-jednorozci-cee.md` | sada otázek (E15) | Žebříček technologických jednorožců v CEE, kritické čtení žebříčku |
| `2026-idnes-ipo-spacex.md` | sada otázek k IPO (iDNES) | Úpis SpaceX: vhodnost, přístup drobných investorů, indexy |

Nové hotové komentáře ukládá agent do `vystupy/komentare/`. Když uživatel potvrdí, že text odešel do redakce v dané podobě, přesuň nebo zkopíruj jeho finální verzi sem, aby archiv vzorů rostl.

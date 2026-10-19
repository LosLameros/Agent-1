# Podklady pro čtvrtletní zprávy

Pro každé čtvrtletí založ složku `RRRR-Qn` (např. `2026-Q3/`) a nahraj do ní dva hotové grafy jako PNG, JPG nebo PDF pod těmito názvy:

- `zhodnoceni-trid-aktiv.png` – „Zhodnocení vybraných tříd aktiv: nQ RRRR"
- `portfolia-v-roce.png` – „Portfolia od Portu v roce RRRR" (nebo „Portfolia na míru v roce RRRR")

Agent `ctvrtletni-zpravy` je odsud načte. Přílohy z chatu sám nevidí.

## Nový vzhled grafů

Grafy ve starém vzhledu (nadpis, logo, tabulka) převádí do nového vzhledu agent `grafy-ctvrtletni-zpravy`. Pošli mu staré grafy (cestu k souborům) nebo čísla. Agent:

- uloží staré grafy jako `puvodni-zhodnoceni-trid-aktiv.*` a `puvodni-portfolia-v-roce.*`,
- zapíše čísla do `grafy-data.json`,
- vykreslí nové grafy pod standardními názvy příkazem `node nastroje/grafy-ctvrtletni-zpravy.js podklady/RRRR-Qn/grafy-data.json`.

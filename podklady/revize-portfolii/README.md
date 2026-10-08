# Podklady pro revize klientských portfolií

Pro každou revizi založ složku `RRRR-MM-DD-<klient>` (např. `2026-10-08-novak/`) a nahraj do ní printscreeny všech klientových portfolií na Portu (PNG/JPG). Pokud jedno portfolio zabírá víc screenů, nahraj všechny. Přidej i printscreeny **daňového přehledu** klienta (časově osvobozené instrumenty a jejich hodnota), klidně do podsložky `dane/`. Bez nich agent daňový dopad prodejů neposoudí.

Agent `revize-portfolia` je odsud načte. Přílohy z chatu sám nevidí. Hotový Excel a textovou revizi uloží do `vystupy/revize-portfolii/`.

Obsah této složky i `vystupy/revize-portfolii/` je v `.gitignore` – klientská data se do repozitáře necommitují.

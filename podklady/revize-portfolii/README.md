# Podklady pro revize klientských portfolií

Pro každou revizi založ složku `RRRR-MM-DD-<jmeno-prijmeni>` (např. `2026-10-08-tomas-foldyna/`) a nahraj do ní printscreeny všech klientových portfolií na Portu (PNG/JPG). Pokud jedno portfolio zabírá víc screenů, nahraj všechny. Přidej i printscreeny **daňového přehledu** klienta (časově osvobozené instrumenty a jejich hodnota), klidně do podsložky `dane/`. Bez nich agent daňový dopad prodejů neposoudí.

Agent `revize-portfolia` je odsud načte. Přílohy z chatu sám nevidí. Výstupy uloží do `vystupy/revize-portfolii/RRRR-MM-DD-<jmeno-prijmeni>/`: `Revize portfolia <Jméno Příjmení>.xlsx`, `revize.md`, `email.md` a `revize.json`.

Obsah této složky i `vystupy/revize-portfolii/` je v `.gitignore` – klientská data se do repozitáře necommitují.

# Podklady pro přání k narozeninám

Sem nahraj Excel (nebo CSV) s klienty, kteří mají narozeniny v příštím měsíci, pod názvem `RRRR-MM.xlsx` (měsíc narozenin, např. `2026-12.xlsx`).

Potřebné sloupce (názvy může mít Excel libovolně podobné, skript je pozná): **jméno**, **příjmení** (nebo jeden sloupec „jméno a příjmení“), **e-mail**, **datum narození**. Volitelně **pohlaví** – zpřesní oslovení u jmen, ze kterých rod nepoznáš.

Agent `prani-k-narozeninam` soubor načte skriptem `nastroje/narozeniny-z-excelu.py`. Přílohy z chatu sám nevidí. Hotová přání uloží do `vystupy/narozeniny/RRRR-MM-narozeniny.md`.

Obsah této složky i `vystupy/narozeniny/` je v `.gitignore` – klientská data se do repozitáře necommitují.

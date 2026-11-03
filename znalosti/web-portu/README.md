# Znalostní základ: web Portu

Text nápovědy (FAQ) a produktových stránek portu.cz, jak je vidí návštěvník webu. Používá ho agent `dotazy-klientu`, když odpovídá na dotazy klientů.

- `faq-*.txt` – sekce Častých dotazů (https://www.portu.cz/o-nas/faq/…). Na konci každého souboru jsou všechny otázky i s rozbalenými odpověďmi (blok „OTÁZKY A ODPOVĚDI“).
- `stranka-*.txt` – produktové stránky (Portfolio od Portu, Portfolio podle vás, Investiční rezerva, Dětský účet, DIP, Portu < 26, realitní fond, Brokerage, ESG, firemní účet, investiční metodika, poplatky, bezpečnost, výnosy, konzultace).
- `magazin-dane.txt` – článek „Portu – vše, co potřebujete vědět o daních“ z Portu Magazínu.

Na druhém řádku každého souboru je datum načtení (`NAČTENO:`). První stažení: 3. 11. 2026.

## Aktualizace

```bash
bash nastroje/aktualizuj-znalosti-portu.sh
```

Jednu stránku lze načíst i samostatně: `node nastroje/portu-stranka.js <URL portu.cz>`.

Sazby (Investiční rezerva), poplatky a výkonnost se mění často. Agent je proto před odpovědí klientovi vždy ověřuje přímo na webu, snímek tady slouží jako rychlý přehled a záloha.

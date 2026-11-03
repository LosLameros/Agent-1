# Vzory: dotazy klientů a odpovědi poradce

Sem patří dřívější dotazy klientů a odpovědi poradce (např. historie konverzací z Claude Projects). Subagent `dotazy-klientu` z nich bere fakta o fungování Portu, postoje poradce a styl odpovědí.

- Jedna konverzace nebo jedno téma = jeden soubor `RRRR-MM-DD-kratke-tema.md` (např. `2026-10-20-vyber-z-dip.md`).
- Nahoře krátce: na co se klient ptal a v jaké situaci byl. Pod tím dotaz a finální odpověď, kterou poradce opravdu poslal.
- Ukládej doslova, i s chybami. Chyby, které agent nemá opakovat, se zapíšou do promptu agenta (kap. 8).
- Vzory jsou v gitu, proto je **anonymizuj**: bez jmen, e-mailů, telefonů, čísel smluv a účtů (jméno nahraď `[klient]`).
- Fakta, která z konverzací vyplynou (jak funguje funkce, interní postup, postoj poradce), se přenesou i do kap. 8 promptu `.claude/agents/Dotazy klientů.md`, aby je agent měl po ruce.

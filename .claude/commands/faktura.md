---
description: Vystaví fakturu (PDF s QR platbou) z názvu odběratele a položek s cenou
argument-hint: <odběratel> <položky s počtem a cenou>
---

Vystav fakturu podle `.claude/agents/fakturace.md` (sekce „Rychlé zadání“ a „Postup“) z tohoto zadání:

$ARGUMENTS

Odběratele, přesné texty položek, splatnost a číslo faktury doplň z `fakturace/`. Zadané ceny jsou bez DPH. PDF vygeneruj přes `python3 nastroje/faktura.py vystupy/faktury/<číslo>.json`, zapiš fakturu do `fakturace/vydane-faktury.md` a pošli mi PDF. Odpověz souhrnem: číslo, odběratel, celkem k úhradě, splatnost a „K ověření“. Doptej se jen tehdy, když bez odpovědi nejde fakturu správně vystavit.

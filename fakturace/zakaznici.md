# Databáze odběratelů

Zdroj: tabulka zákazníků od uživatele (stav 10/2026) + vydané faktury v `examples/faktury/`.
Údaje z faktury mají přednost před tabulkou: faktura je to, co skutečně odešlo. Rozpory jsou u každého odběratele uvedené v „Poznámkách“.

Legenda režimů (podrobně v `.claude/agents/fakturace.md`):
- **CZ** – tuzemsko, česká šablona „FAKTURA – DAŇOVÝ DOKLAD“, Kč, DPH 21 %, účet 295661016/0300
- **EU** – plátce DPH v jiném státě EU, anglická šablona „INVOICE“, EUR, bez DPH (dodání zboží do JČS), IBAN
- **EXPORT** – mimo EU, anglická šablona „INVOICE“, EUR, bez DPH (vývoz zboží), IBAN

---

## JETI model s.r.o.
- **Kontakt:** Zdeněk Raška · tel. 603 709 212 · e-mail neúplný (začíná `zraska@`)
- **Adresa:** Lomená 1530, 742 58 Příbor, Česká republika
- **IČO:** 26825147 · **DIČ:** CZ26825147
- **Režim:** CZ · **Splatnost:** 10 dní · **Doprava:** na faktuře 26049 nebyla
- **Fakturované položky:** Hlava knypliku V5 – 42,00 Kč/ks bez DPH
- **Faktury:** 26049 (21. 09. 2026, 1 000 ks, 50 820,00 Kč s DPH)
- **Poznámky:** Na faktuře 26049 je DIČ vytištěné dvakrát („CZ26825147CZ26825147“). Jde o chybu v adresáři FakturaOnline a je potřeba ji tam opravit.

## Tomáš Trnka
- **Kontakt:** tel. 618 919 200 · e-mail neúplný (začíná `tom.148`)
- **Adresa:** Miskovice 148, 285 01 Miskovice, Česká republika
- **IČO / DIČ:** neuvedeno (pravděpodobně fyzická osoba nepodnikatel)
- **Režim:** CZ · **Splatnost:** neznámá, výchozí 10 dní
- **Faktury:** zatím žádná v podkladech
- **Poznámky:** Předvolba 618 neodpovídá běžnému českému mobilnímu číslu. Telefon ověřit.

## HPH models s.r.o.
- **Kontakt:** Hodan · tel. 777 304 120 · e-mail neúplný (začíná `jirka@h`)
- **Adresa:** Čáslavská 257, 284 01 Kutná Hora, Česká republika
- **IČO:** 27221334 · **DIČ:** chybí (u s.r.o. plátce DPH bývá CZ27221334, ale ověřit)
- **Režim:** CZ · **Splatnost:** neznámá, výchozí 10 dní
- **Faktury:** zatím žádná v podkladech

## Owl models s.r.o.
- **Kontakt:** Hobža · tel. 603 728 096 · e-mail neúplný (začíná `owl@ow`)
- **Adresa:** Mánesova 321/6, 746 01 Opava, Česká republika
- **IČO / DIČ:** chybí
- **Režim:** CZ · **Splatnost:** neznámá, výchozí 10 dní
- **Faktury:** zatím žádná v podkladech

## PJB Hobby Sp. z o.o.
- **Kontakt:** Pawel Buchaniec · tel. +48 122 848 328 · e-mail neúplný (začíná `pawel.b`)
- **Oficiální název (na faktuře):** PJB HOBBY SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ
- **Adresa:** Koźmice Wielkie 781, 32-020 Wieliczka, Polsko (na faktuře 26038: „781, 32020 Koźmice Wielkie, Poland“)
- **REGON (Company ID):** 388878489 · **NIP:** 6832114740 → **VAT ID pro EU:** PL6832114740
- **Režim:** EU · **Měna:** EUR · **Splatnost:** 10 dní · **Doprava:** Shipping and packing 10,00 EUR
- **Fakturované položky:** MTC díly dle `fakturace/cenik.md`
- **Faktury:** 26038 (21. 07. 2026, 206,00 EUR)
- **Poznámky:** Na faktuře 26038 je VAT ID bez prefixu PL. Pro osvobození dodání do EU musí být uvedeno DIČ s kódem státu, ověřené ve VIES.

## STROZATECH s.r.o.
- **Kontakt:** Pravoslav Kyselák · tel. 737 258 723 · e-mail neúplný (začíná `kyselak`)
- **Adresa:** Dvořákova 588/13, 602 00 Brno, Česká republika
- **IČO / DIČ:** chybí
- **Režim:** CZ · **Splatnost:** neznámá, výchozí 10 dní
- **Faktury:** zatím žádná v podkladech

## Josef Choreň
- **Kontakt:** tel. 777 095 481 · e-mail neúplný (začíná `chory-m`)
- **Adresa:** Skršín 70, 434 01 Skršín, Česká republika
- **IČO / DIČ:** chybí
- **Režim:** CZ · **Splatnost:** neznámá, výchozí 10 dní
- **Faktury:** zatím žádná v podkladech

## VenPor s.r.o.
- **Kontakt:** tel. 724 502 382 · venpor@seznam.cz · https://venpor.cz
- **Adresa:** Na Hlavaticích 521, 583 01 Chotěboř, Česká republika
- **IČO:** 03321169 · **DIČ:** CZ03321169
- **Režim:** CZ · **Splatnost:** 30 dní · **Doprava:** na faktuře 26048 nebyla
- **Fakturované položky:** Silové sloupky PBS08012024-P002 – 60,00 Kč/ks bez DPH
- **Faktury:** 26048 (09. 09. 2026, 300 ks, 21 780,00 Kč s DPH)
- **Poznámky:** Na faktuře jsou uvedené i kontaktní údaje (e-mail a web). Zachovat.

## Attack HK
- **Kontakt:** e-mail neúplný (začíná `obchod`)
- **Adresa:** Kodymova 2539/8, Stodůlky, 158 00 Praha 5, Česká republika
- **IČO / DIČ / právní forma:** chybí
- **Režim:** CZ · **Splatnost:** neznámá, výchozí 10 dní
- **Faktury:** zatím žádná v podkladech
- **Poznámky:** Bez IČO nejde ověřit, kdo je skutečný odběratel (obchodní název ≠ firma). Před první fakturou doplnit.

## MyJa Tech s.r.o.
- **Kontakt:** e-mail neúplný (začíná `info@m`)
- **Adresa:** Libomyšl 55, 267 23 Libomyšl, Česká republika
- **IČO:** 02566435 · **DIČ:** CZ02566435
- **Režim:** CZ · **Splatnost:** neznámá, výchozí 10 dní
- **Faktury:** zatím žádná v podkladech
- **Poznámky:** V tabulce je IČO „2566435“, protože tabulka zahodila úvodní nulu. IČO má vždy 8 číslic a odpovídá DIČ CZ02566435.

## STRANKA s.r.o.
- **Adresa:** Tylova 1347/14, Předměstí, 412 01 Litoměřice, Česká republika
- **IČO:** 07992424 · **DIČ:** CZ07992424
- **Režim:** CZ · **Splatnost:** 10 dní · **Doprava:** Poštovné a balné 180,00 Kč bez DPH
- **Fakturované položky:** Osa L45 – 74,00 Kč · Osa L40 – 80,00 Kč · Osa L75 – 73,00 Kč (vše za ks bez DPH)
- **Faktury:** 26046 (02. 09. 2026, 13 597,98 Kč s DPH)
- **Poznámky:** V tabulce zákazníků chybí. Kontakt doplnit.

## H.G. Hannant Ltd
- **Adresa:** Unit 35, Harbour Road, Oulton Road, Lowestoft, Suffolk, NR32 3LZ, United Kingdom
- **Company ID (dle faktury):** 104980771000 · **VAT ID:** GB104980771
- **Režim:** EXPORT · **Měna:** EUR · **Splatnost:** 14 dní · **Doprava:** Shipping and packing 15,00 EUR
- **Fakturované položky:** MTC díly dle `fakturace/cenik.md`
- **Faktury:** 26042 (18. 08. 2026, 676,00 EUR)
- **Poznámky:** V tabulce zákazníků chybí. „Company ID“ 104980771000 je jen VAT ID s koncovkou 000, ne číslo z Companies House (to má 8 znaků). Ověřit.

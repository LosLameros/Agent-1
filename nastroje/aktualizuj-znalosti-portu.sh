#!/usr/bin/env bash
# Znovu stáhne text nápovědy (FAQ) a produktových stránek portu.cz do znalosti/web-portu/.
# Používá ho agent dotazy-klientu jako znalostní základ. Spusť z kořene repozitáře:
#   bash nastroje/aktualizuj-znalosti-portu.sh
# Trvá to několik minut (každá stránka se načítá v Chromiu).
set -euo pipefail
cd "$(dirname "$0")/.."
D=znalosti/web-portu
mkdir -p "$D"

FAQ=(o-portu jak-zacit bezpecnost portfolia-od-portu portfolio-podle-vas realitni-fond
     dlouhodoby-investicni-produkt-dip ucty-pro-deti ucty-pro-mlade investicni-rezerva brokerage
     firemni-ucty ucet-v-eur vklady-vybery-a-prevody poplatky dane slevove-programy darkove-poukazy
     prevody-cennych-papir%C5%AF zmena-osobnich-udaju dip-pro-zamestnavatele dalsi)
STRANKY=(o-nas/kolik-to-stoji investice/portfolio-od-portu investice/portfolio-podle-vas
     investice/investicni-rezerva investice/pro-deti investice/dlouhodoby-investicni-produkt
     investice/pro-mlade investice/realitni-fond investice/jednotlive-akcie-etf
     investice/odpovedne-investovani-esg investice/pro-firmy o-nas/investicni-metodika
     o-nas/bezpecnost lepsi-vynosy o-nas/investicni-konzultace)

for s in "${FAQ[@]}"; do
  n=${s//%C5%AF/u}
  node nastroje/portu-stranka.js "https://www.portu.cz/o-nas/faq/$s" > "$D/faq-$n.txt" || echo "CHYBA: faq/$s" >&2
  echo "faq-$n: $(grep -c '^OTÁZKA' "$D/faq-$n.txt" || true) otázek"
done
for u in "${STRANKY[@]}"; do
  n=${u##*/}
  node nastroje/portu-stranka.js "https://www.portu.cz/$u" > "$D/stranka-$n.txt" || echo "CHYBA: $u" >&2
  echo "stranka-$n"
done
node nastroje/portu-stranka.js "https://magazin.portu.cz/portu-vse-co-potrebujete-vedet-o-danich/" > "$D/magazin-dane.txt" \
  || echo "CHYBA: magazin-dane" >&2
echo "Hotovo: $D (datum načtení je na 2. řádku každého souboru)"

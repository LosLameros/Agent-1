"""Prodeje vozů Mercedes-Benz Group – osobní vozy a dodávky, miliony kusů (2018 – LTM). Nový design Portu.

Data: převzato 1:1 z předlohy (zdroj Mercedes-Benz Group); LTM = posledních 12 měsíců. Jediná nesrovnalost
v předloze: u roku 2019 dávají zobrazené složky 2,39 + 0,44 = 2,83, celek je uvedený 2,82 (zaokrouhlení),
popisek celku proto zůstává podle předlohy.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-14-mercedes-prodeje.py
"""
import csv
import sys

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-14-mercedes-prodeje"

roky, auta, dodavky, celkem = [], [], [], []
with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        roky.append(r["rok"])
        auta.append(float(r["osobni_vozy_mil"]))
        dodavky.append(float(r["dodavky_mil"]))
        celkem.append(float(r["celkem_mil"]))

zmena_celkem = (celkem[-1] / celkem[0] - 1) * 100
zmena_auta = (auta[-1] / auta[0] - 1) * 100
OSA = (0, 3, 0.5)
VYSKA_PLOCHY = pg.GRAF_DOLNI_1RADEK - pg.GRAF_HORNI

fig, ax = pg._platno(
    pg.GRAF_DOLNI_1RADEK, nadpis="Prodeje vozů Mercedes-Benz Group",
    podnadpis=("Počet prodaných osobních vozů a dodávek v milionech kusů.",
               f"Celkové prodeje klesly z {pg.cislo(celkem[0], 2)} mil. v roce {roky[0]} na {pg.cislo(celkem[-1], 2)} mil. "
               f"za posledních 12 měsíců (LTM), tedy o {pg.cislo(abs(zmena_celkem), 1, '%')}. U osobních vozů je "
               f"propad {pg.cislo(abs(zmena_auta), 1, '%')}."))
pg._osa_y(ax, OSA, "", 1)
labels = ax.get_yticklabels()
labels[0].set_text("0")
ax.set_yticklabels([t.get_text() for t in labels])

n = len(roky)
ax.set_xlim(-0.6, n - 0.4)
SIRKA = 0.56
ax.bar(range(n), auta, width=SIRKA, color=pg.FIALOVA, zorder=2, linewidth=0)
ax.bar(range(n), dodavky, bottom=auta, width=SIRKA, color=pg.SVETLE_FIALOVA, zorder=2, linewidth=0)
odsazeni = 8 / VYSKA_PLOCHY * (OSA[1] - OSA[0])
for i in range(n):
    ax.text(i, auta[i] / 2, pg.cislo(auta[i], 2), ha="center", va="center", fontsize=pg.PISMO_HODNOTA, color="white",
            fontproperties=pg._STREDNI, zorder=4)
    ax.text(i, auta[i] + dodavky[i] / 2, pg.cislo(dodavky[i], 2), ha="center", va="center", fontsize=pg.PISMO_HODNOTA,
            color=pg.TEXT_TMAVY, zorder=4)
    ax.text(i, auta[i] + dodavky[i] + odsazeni, f"{pg.cislo(celkem[i], 2)} mil.", ha="center", va="bottom",
            fontsize=pg.PISMO_HODNOTA, color=pg.TEXT_TMAVY, fontproperties=pg._TUCNE, zorder=4)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=3)
ax.set_xticks(range(n))
ax.set_xticklabels(roky, fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
ax.tick_params(axis="x", pad=27 / pg.PT)

renderer = fig.canvas.get_renderer()
fig.canvas.draw()
leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
pos = ax.get_position()
ax.set_position([pg._fx(leva), pos.y0, pg._fx(pg.GRAF_PRAVA - leva), pos.height])

pg._legenda_a_zdroj(fig, [("Osobní vozy (Cars)", pg.FIALOVA), ("Dodávky (Vans)", pg.SVETLE_FIALOVA)],
                    "Graf: Portu, zdroj: Mercedes-Benz Group")
pg.uloz(fig, ZAKLAD + ".png")

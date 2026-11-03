"""Alphabet po výsledcích 3Q 2026 – 3 grafy v Portu vzhledu k podkladu pro rozhovor.

1) Růst tržeb Google Search & other meziročně (1Q 2022 – 3Q 2026)
2) Provozní zisk segmentů Google Services a Google Cloud za čtvrtletí
3) Capex vs. provozní cash flow hyperscalerů (Microsoft, Amazon, Alphabet, Meta) od 2018

Data: tiskové zprávy Alphabetu k výsledkům (8-K, exhibit 99.1, SEC); růst Search počítaný ze srovnatelných čísel
v téže zprávě. Provozní zisk segmentů ve verzi ze zprávy o rok později (po přepočtu segmentů v roce 2023).
Capex = nákupy pozemků, budov a zařízení, provozní cash flow = peněžní tok z provozní činnosti (SEC XBRL,
čtvrtletí jako rozdíl kumulativních údajů; Microsoft fiskální čtvrtletí končící ve stejných měsících).
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-03-alphabet.py
"""
import csv
import datetime as dt
import sys

from matplotlib.lines import Line2D

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-03-alphabet"
VYSKA_PLOCHY = pg.GRAF_DOLNI_1RADEK - pg.GRAF_HORNI

with open(ZAKLAD + ".csv", encoding="utf-8") as f:
    a = list(csv.DictReader(f))
datumy = [dt.date.fromisoformat(r["ctvrtleti_konec"]) for r in a]
search = [float(r["search_rust_pct"]) for r in a]
services = [int(r["provozni_zisk_services_mil_usd"]) / 1000 for r in a]
cloud = [int(r["provozni_zisk_cloud_mil_usd"]) / 1000 for r in a]


def bod(i, smer):
    return (datumy[i], search[i], pg.cislo(search[i], 1, "%"), smer)


# --- 1) Search ----------------------------------------------------------------
maximum_2026 = max(range(len(search)), key=lambda i: search[i] if datumy[i].year == 2026 else -99)
fig = pg.spojnicovy(
    datumy, {"Google Search & other, meziroční růst tržeb": search},
    osa_y=(-5, 30, 5), jednotka="%", format_x="%Y", rozsah_x=(dt.date(2021, 12, 31), datumy[-1]),
    anotace=[bod(0, "nad"), bod(search.index(min(search)), "pod"), bod(maximum_2026, "nad")],
    popisky_konec=True, mista_konec=1, jednotka_konec="%",
    zdroj="Graf: Portu, zdroj: Alphabet",
    nadpis="Google Search zase zpomaluje", podnadpis="Tržby Google Search & other, meziroční růst za čtvrtletí",
)
pg.uloz(fig, ZAKLAD + "-search.png")

# --- 2) Provozní zisk segmentů -------------------------------------------------
OSA = (0, 60, 10)
podil = cloud[-1] / (services[-1] + cloud[-1]) * 100
fig, ax = pg._platno(pg.GRAF_DOLNI_1RADEK, nadpis=f"Cloud už dělá {pg.cislo(podil, 1, '%')} provozního zisku Googlu",
                     podnadpis="Provozní zisk segmentů za čtvrtletí, mld. USD")
pg._osa_y(ax, OSA, "", 0)
n = len(a)
ax.set_xlim(-0.6, n - 0.4)
SIRKA = 0.66
# ztráty Cloudu v roce 2022 (pod 1 mld. USD) kreslí sloupec pod nulou
ax.bar(range(n), services, width=SIRKA, color=pg.FIALOVA, zorder=2, linewidth=0)
ax.bar(range(n), [max(c, 0) for c in cloud], bottom=services, width=SIRKA, color=pg.ZELENA, zorder=2, linewidth=0)
ax.bar(range(n), [min(c, 0) for c in cloud], width=SIRKA, color=pg.ZELENA, zorder=2, linewidth=0)
odsazeni = 8 / VYSKA_PLOCHY * (OSA[1] - OSA[0])
for i, (s, c) in enumerate(zip(services, cloud)):
    ax.text(i, s + max(c, 0) + odsazeni, pg.cislo(s + c, 1), ha="center", va="bottom", fontsize=pg.PISMO_HODNOTA,
            color=pg.TEXT_TMAVY)
    if c >= 5:  # hodnota Cloudu uvnitř zeleného dílu, kde je dost místa
        ax.text(i, s + c / 2, pg.cislo(c, 1), ha="center", va="center", fontsize=pg.PISMO_HODNOTA, color="white",
                fontproperties=pg._STREDNI)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=3)
roky = [d.year for d in datumy]
zacatky = [i for i, r in enumerate(roky) if i == 0 or r != roky[i - 1]]
ax.set_xticks([(z + (zacatky[k + 1] if k + 1 < len(zacatky) else n) - 1) / 2 for k, z in enumerate(zacatky)])
ax.set_xticklabels([str(roky[z]) for z in zacatky], fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
ax.tick_params(axis="x", pad=27 / pg.PT)
for z in zacatky[1:]:
    ax.add_line(Line2D([z - 0.5] * 2, [0, -12 / VYSKA_PLOCHY], transform=ax.get_xaxis_transform(),
                       color=pg.ZAKLADNA, linewidth=1.5 * 72 / pg.DPI, clip_on=False))
renderer = fig.canvas.get_renderer()
fig.canvas.draw()
leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
pos = ax.get_position()
ax.set_position([pg._fx(leva), pos.y0, pg._fx(pg.GRAF_PRAVA - leva), pos.height])
pg._legenda_a_zdroj(fig, [("Google Services", pg.FIALOVA), ("Google Cloud", pg.ZELENA)], "Graf: Portu, zdroj: Alphabet")
pg.uloz(fig, ZAKLAD + "-provozni-zisk.png")

# --- 3) Capex vs. provozní cash flow hyperscalerů ------------------------------
with open("vystupy/grafy/2026-11-03-hyperscalery-capex.csv", encoding="utf-8") as f:
    h = list(csv.DictReader(f))
hd = [dt.date.fromisoformat(r["ctvrtleti_konec"]) for r in h]
capex = [int(r["capex_celkem_mil_usd"]) / 1000 for r in h]
ocf = [int(r["ocf_celkem_mil_usd"]) / 1000 for r in h]
fig = pg.spojnicovy(
    hd, {"Capex": capex, "Provozní cash flow": ocf},
    osa_y=(0, 250, 50), jednotka="", format_x="%Y", rozsah_x=(dt.date(2018, 1, 1), hd[-1]),
    popisky_konec=True, mista_konec=0, jednotka_konec="mld.",
    zdroj="Graf: Portu, zdroj: výkazy firem (SEC)",
    nadpis="Capex hyperscalerů poprvé převýšil provozní cash flow",
    podnadpis="Microsoft, Amazon, Alphabet a Meta dohromady, mld. USD za čtvrtletí",
)
pg.uloz(fig, "vystupy/grafy/2026-11-03-hyperscalery-capex.png")

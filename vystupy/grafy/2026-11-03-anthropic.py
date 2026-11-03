"""Anthropic: tržby vs. náklady na výpočetní kapacitu, jejich podíl a závazky vs. hotovost – 3 grafy v Portu vzhledu.

Data: neauditované čtvrtletní údaje Anthropicu, převzato z lab.brycht.app (3. 11. 2026).
- Podíl výpočtů na tržbách (251,1 % … 58,2 %), tržby 2Q/3Q 2026 (11,6 / 17,0 mld. USD) a závazky vs. hotovost
  jsou přesné hodnoty z popisků. Leasingy v užívání = celkové závazky − cloud − nezahájené leasingy.
- Tržby 1Q 2025 – 1Q 2026 odečtené z výšky sloupců a sladěné s přesným podílem (±0,1 mld. USD); 1Q 2026 podle
  růstu tržeb ve 2Q o 144,2 %. Náklady na výpočty = podíl × tržby.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-11-03-anthropic.py
"""
import csv
import sys
from decimal import ROUND_HALF_UP, Decimal

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

ZAKLAD = "vystupy/grafy/2026-11-03-anthropic"
ZDROJ = "Graf: Portu, zdroj: Anthropic"
VYSKA_PLOCHY = pg.GRAF_DOLNI_1RADEK - pg.GRAF_HORNI

ctvrtleti, trzby, vypocty, podil = [], [], [], []
with open(ZAKLAD + "-trzby-vypocty.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        ctvrtleti.append(r["ctvrtleti"])
        trzby.append(float(r["trzby_mld_usd"]))
        vypocty.append(float(r["vypocty_mld_usd"]))
        podil.append(float(r["vypocty_podil_trzeb_pct"]))
with open(ZAKLAD + "-zavazky.csv", encoding="utf-8") as f:
    zavazky = list(csv.DictReader(f))


def jedno_misto(v):
    """1 desetinné místo, 0,85 → 0,9 (ne bankovní zaokrouhlení)."""
    return pg.cislo(float(Decimal(str(v)).quantize(Decimal("0.1"), ROUND_HALF_UP)), 1)


def okraje(fig, ax):
    """Levý okraj podle nejdelšího popisku osy y (jako u ostatních grafů Portu)."""
    renderer = fig.canvas.get_renderer()
    fig.canvas.draw()
    leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
    pos = ax.get_position()
    ax.set_position([pg._fx(leva), pos.y0, pg._fx(pg.GRAF_PRAVA - leva), pos.height])


def osa_x(ax, popisky):
    ax.set_xticks(range(len(popisky)))
    ax.set_xticklabels(popisky, fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
    ax.tick_params(axis="x", pad=27 / pg.PT)


# --- 1) Tržby vs. náklady na výpočty -------------------------------------------
OSA = (0, 20, 5)
fig, ax = pg._platno(pg.GRAF_DOLNI_1RADEK, nadpis="Tržby Anthropicu ve 3Q +46,7 %, náklady na výpočty +77,5 %",
                     podnadpis="Tržby vs. náklady na výpočetní kapacitu a infrastrukturu, mld. USD za čtvrtletí, neauditované")
pg._osa_y(ax, OSA, "", 0)
n = len(ctvrtleti)
ax.set_xlim(-0.5, n - 0.5)
SIRKA, MEZERA = 0.3, 0.04
odsazeni = 8 / VYSKA_PLOCHY * (OSA[1] - OSA[0])
for posun, hodnoty, barva in ((-(SIRKA + MEZERA) / 2, trzby, pg.FIALOVA), ((SIRKA + MEZERA) / 2, vypocty, pg.ZELENA)):
    xs = [i + posun for i in range(n)]
    ax.bar(xs, hodnoty, width=SIRKA, color=barva, zorder=2, linewidth=0)
    for x, h in zip(xs, hodnoty):
        ax.text(x, h + odsazeni, jedno_misto(h), ha="center", va="bottom", fontsize=pg.PISMO_HODNOTA, color=pg.TEXT_TMAVY)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=3)
osa_x(ax, ctvrtleti)
okraje(fig, ax)
pg._legenda_a_zdroj(fig, [("Tržby", pg.FIALOVA), ("Výpočetní kapacita a infrastruktura", pg.ZELENA)], ZDROJ)
pg.uloz(fig, ZAKLAD + "-trzby-vypocty.png")

# --- 2) Výpočty jako podíl na tržbách ------------------------------------------
OSA = (0, 300, 50)
fig, ax = pg._platno(pg.GRAF_DOLNI_1RADEK, nadpis="Výpočetní kapacita jako podíl na tržbách",
                     podnadpis="Náklady na výpočetní kapacitu a infrastrukturu v % tržeb, za čtvrtletí, neauditované")
pg._osa_y(ax, OSA, "%", 0)
ax.set_xlim(-0.4, n - 0.6)
ax.plot(range(n), podil, color=pg.FIALOVA, linewidth=3.5 / pg.PT, marker="o", markersize=9 / pg.PT,
        solid_joinstyle="round", zorder=3)
odsazeni = 14 / VYSKA_PLOCHY * (OSA[1] - OSA[0])
for i, h in enumerate(podil):
    pod = 0 < i < n - 1 and h < podil[i - 1] and h < podil[i + 1]  # u lokálního dna popisek pod bodem
    vpravo = not pod and i < n - 1  # nad bodem vpravo, aby popisek neležel na klesající čáře
    ax.text(i + (0.07 if vpravo else 0), h - odsazeni if pod else h + odsazeni, pg.cislo(h, 1, "%"),
            ha="left" if vpravo else "center", va="top" if pod else "bottom", fontsize=pg.PISMO_HODNOTA, color=pg.TEXT_TMAVY, zorder=4)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=2)
osa_x(ax, ctvrtleti)
okraje(fig, ax)
pg._legenda_a_zdroj(fig, [("Výpočetní kapacita a infrastruktura / tržby", pg.FIALOVA)], ZDROJ)
pg.uloz(fig, ZAKLAD + "-podil-vypoctu.png")

# --- 3) Závazky vs. hotovost ---------------------------------------------------
OSA = (0, 800, 200)
fig, ax = pg._platno(pg.GRAF_DOLNI_1RADEK, nadpis="Závazky Anthropicu na výpočty ve 3Q +30,9 % na 771,2 mld. USD",
                     podnadpis="Závazky vs. hotovost a investice ke konci čtvrtletí, mld. USD, neauditované")
pg._osa_y(ax, OSA, "", 0)
ax.set_xlim(-0.6, len(zavazky) - 0.4)
SIRKA = 0.36
SLOZKY = [("cloud_a_jine_nakupy_mld_usd", "Cloud a nákupy", pg.FIALOVA, "white"),
          ("leasingy_nezahajene_mld_usd", "Nezahájené leasingy", pg.SVETLE_FIALOVA, pg.TEXT_TMAVY),
          ("leasingy_v_uzivani_mld_usd", "Běžící leasingy", pg.TMAVE_SEDA, None)]
odsazeni = 8 / VYSKA_PLOCHY * (OSA[1] - OSA[0])
for i, r in enumerate(zavazky):
    x_zav, x_hot = i - SIRKA / 2, i + SIRKA / 2
    dole = 0.0
    for klic, _, barva, barva_textu in SLOZKY:
        v = float(r[klic])
        ax.bar(x_zav, v, bottom=dole, width=SIRKA, color=barva, zorder=2, linewidth=0)
        if barva_textu:  # leasingy v užívání (2–6 mld.) jsou na popisek moc tenké
            ax.text(x_zav, dole + v / 2, pg.cislo(v, 1), ha="center", va="center", fontsize=pg.PISMO_HODNOTA,
                    color=barva_textu, fontproperties=pg._STREDNI, zorder=4)
        dole += v
    ax.text(x_zav, dole + odsazeni, pg.cislo(float(r["zavazky_celkem_mld_usd"]), 1), ha="center", va="bottom",
            fontsize=pg.PISMO_HODNOTA, color=pg.TEXT_TMAVY, fontproperties=pg._STREDNI)
    hotovost = float(r["hotovost_a_investice_mld_usd"])
    ax.bar(x_hot, hotovost, width=SIRKA, color=pg.ZELENA, zorder=2, linewidth=0)
    ax.text(x_hot, hotovost + odsazeni, pg.cislo(hotovost, 1), ha="center", va="bottom", fontsize=pg.PISMO_HODNOTA,
            color=pg.TEXT_TMAVY, fontproperties=pg._STREDNI)
ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=3)
osa_x(ax, [r["datum"] for r in zavazky])
okraje(fig, ax)
pg._legenda_a_zdroj(fig, [(nazev, barva) for _, nazev, barva, _ in SLOZKY] + [("Hotovost", pg.ZELENA)], ZDROJ)
pg.uloz(fig, ZAKLAD + "-zavazky.png")

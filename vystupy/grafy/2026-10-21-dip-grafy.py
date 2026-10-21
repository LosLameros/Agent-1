"""DIP – Kolik můžete mít za 10, 20 a 30 let: tři grafy v Portu vzhledu.

Data: model vystupy/grafy/2026-10-21-dip-model.xlsx (list „Roky“, hodnoty ke konci roku; předpoklady
a jejich zdroje na listu „Předpoklady“). Po změně předpokladů excel přepočítejte a skript spusťte znovu.
Spouštěj z kořene repozitáře: python3 vystupy/grafy/2026-10-21-dip-grafy.py
"""
import sys

import openpyxl

sys.path.insert(0, "nastroje")
import portu_grafy as pg  # noqa: E402

MODEL = "vystupy/grafy/2026-10-21-dip-model.xlsx"
wb = openpyxl.load_workbook(MODEL, data_only=True)
pred = wb["Předpoklady"]
VKLAD, VYNOS, USPORA = pred["B4"].value, pred["B5"].value, pred["B14"].value
POPLATEK_DIP, SLEVA = pred["B9"].value, pred["B10"].value
POPLATEK_FIX = pred["C18"].value  # poplatek mimo DIP po slevě v nejnižším pásmu (do 0,5 mil. Kč)
roky = [r for r in wb["Roky"].iter_rows(min_row=2, max_row=32, values_only=True)]
if any(v is None for r in roky for v in r[:8]):
    sys.exit("Excel nemá spočítané hodnoty – nejdřív ho přepočítejte (otevřít a uložit, nebo recalc.py).")

RADY = [  # (sloupec v listu Roky, název, barva čáry) – v pořadí odshora
    (5, "DIP + reinvestovaná úspora", pg.ZELENA),
    (4, "DIP + daňová úspora", pg.SVETLE_ZELENA),
    (3, "Bez DIP s fixací", pg.FIALOVA),
]
POPISEK = {pg.SVETLE_ZELENA: "#3DAA62"}  # světle zelená je jako text málo čitelná – popisek tmavší


def kc(v):
    return pg.cislo(round(v), 0) + " Kč"


def graf(horizont, krok_x, osa_y):
    data = roky[: horizont + 1]
    let = [r[0] for r in data]
    fig, ax = pg._platno(pg.GRAF_DOLNI_1RADEK, nadpis=f"Kolik můžete mít za {horizont} let", navic=122)
    vyska = fig._portu["vyska"]
    x_text = pg._fx(pg.GRAF_LEVA - 80)
    fig.text(x_text, 1 - 84 / vyska,
             f"Při investici {pg.cislo(VKLAD, 0)} Kč měsíčně • výnos {pg.cislo(VYNOS * 100, 0, '%')} p. a. • "
             f"daňová úspora {pg.cislo(USPORA, 0)} Kč ročně", fontsize=pg.PISMO_LEGENDA, color=pg.TEXT_SEDY,
             va="center")
    fig.text(x_text, 1 - 120 / vyska,
             f"Poplatky: DIP {pg.cislo(POPLATEK_DIP * 100, 1, '%')} ročně • mimo DIP s fixací "
             f"{pg.cislo(POPLATEK_FIX * 100, 1, '%')} ročně (sleva {pg.cislo(SLEVA * 100, 0, '%')}), s objemem klesá",
             fontsize=pg.PISMO_LEGENDA, color=pg.TEXT_SEDY, va="center")
    vyhoda, vyhoda_reinv = data[-1][6], data[-1][7]
    fig.text(x_text, 1 - 164 / vyska,
             f"Výhoda DIPu: +{kc(vyhoda)}   •   s reinvestovanou úsporou: +{kc(vyhoda_reinv)}",
             fontsize=pg.PISMO_LEGENDA, color=pg.ZELENA, fontproperties=pg._STREDNI, va="center")

    pg._osa_y(ax, osa_y, "", 0)
    ax.axhline(0, color=pg.ZAKLADNA, linewidth=2 * 72 / pg.DPI, zorder=2)
    ax.set_xlim(0, horizont)
    ax.set_xticks(range(0, horizont + 1, krok_x))
    ax.set_xticklabels([f"{t} let" if t == horizont else str(t) for t in range(0, horizont + 1, krok_x)],
                       fontsize=pg.PISMO_OSA, color=pg.TEXT_SEDY)
    ax.tick_params(axis="x", pad=24 / pg.PT)

    # pás výhody DIPu mezi investicí bez DIPu a DIPem s reinvestovanou úsporou
    ax.fill_between(let, [r[3] for r in data], [r[5] for r in data], color=pg.ZELENA, alpha=0.10, linewidth=0, zorder=1)
    body = list(range(0, horizont + 1, krok_x))
    for sloupec, nazev, barva in reversed(RADY):
        hodnoty = [r[sloupec] for r in data]
        ax.plot(let, hodnoty, color=barva, linewidth=3.5 / pg.PT, solid_joinstyle="round", zorder=3)
        ax.plot(body, [hodnoty[t] for t in body], linestyle="none", marker="o", markersize=7 / pg.PT, color=barva, zorder=4)

    # koncové hodnoty vpravo, v barvě řady, odsunuté od sebe (min. 28 px)
    rozsah = osa_y[1] - osa_y[0]
    mezera = 28 / (pg.GRAF_DOLNI_1RADEK - pg.GRAF_HORNI) * rozsah
    pozice, posledni = [], None
    for sloupec, _, barva in RADY:  # odshora dolů
        y = data[-1][sloupec]
        if posledni is not None and posledni - y < mezera:
            y = posledni - mezera
        pozice.append((y, data[-1][sloupec], barva))
        posledni = y
    for y, hodnota, barva in pozice:
        ax.annotate(kc(hodnota), (horizont, y), xytext=(12 / pg.PT, 0), textcoords="offset points", ha="left",
                    va="center", fontsize=pg.PISMO_HODNOTA, color=POPISEK.get(barva, barva), fontproperties=pg._STREDNI,
                    annotation_clip=False)

    # okraje podle popisků (osa y vlevo, koncové hodnoty vpravo)
    renderer = fig.canvas.get_renderer()
    fig.canvas.draw()
    leva = max(pg.GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
    prava = pg.GRAF_PRAVA - max(t.get_window_extent(renderer).width for t in ax.texts) - 22
    pos = ax.get_position()
    ax.set_position([pg._fx(leva), pos.y0, pg._fx(prava - leva), pos.height])

    pg._legenda_a_zdroj(fig, [(n, b) for _, n, b in RADY], "Graf: Portu, modelový výpočet")
    cesta = f"vystupy/grafy/2026-10-21-dip-{horizont}-let.png"
    pg.uloz(fig, cesta)
    print(cesta, "|", " | ".join(f"{n}: {kc(data[-1][s])}" for s, n, _ in RADY))


graf(10, 1, (0, 1_000_000, 200_000))
graf(20, 2, (0, 2_500_000, 500_000))
graf(30, 5, (0, 6_000_000, 1_000_000))

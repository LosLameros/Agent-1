"""Grafy v jednotném vzhledu Portu.

Vzorem vzhledu jsou grafy v examples/grafy/ (meziroční inflace ČR a repo sazba ČNB,
meziroční inflace v USA a eurozóně). Barvy a písmo jsou oficiální podle brand manuálu
Portu (https://guidelines.portu.cz/barvy/): fialová #4840BB, zelená #00AA3C, písmo Rethink Sans.
Rozměry jsou v pixelech výsledného PNG 1370 × 722 px (200 dpi, 6,85 × 3,61 palce).

Použití:
    import sys; sys.path.insert(0, 'nastroje')
    import portu_grafy as pg
    fig = pg.sloupcovy(['Americké akcie', 'Zlato'], {'USD nebo EUR': [2.9, 1.9], 'CZK': [4.1, 3.2]},
                       osa_y=(-2, 6, 2), jednotka='%')
    pg.uloz(fig, 'vystupy/grafy/priklad.png')
"""
from __future__ import annotations

import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

# --- Barvy --------------------------------------------------------------------
FIALOVA = "#4840BB"        # oficiální fialová Portu – 1. řada
ZELENA = "#00AA3C"         # oficiální zelená Portu – 2. řada
# Doplňkové barvy pro 3. a další řadu – odvozené ze dvou hlavních (světlejší odstíny
# a neutrální šedé). Používej jen výjimečně.
SVETLE_FIALOVA = "#A39EE3"
SVETLE_ZELENA = "#7FD99E"
TMAVE_SEDA = "#2B2B2B"
SEDA = "#A0A2AE"
BARVY = [FIALOVA, ZELENA, SVETLE_FIALOVA, SVETLE_ZELENA, TMAVE_SEDA, SEDA]

TEXT_TMAVY = "#2B2B2B"     # hodnoty u sloupců, legenda, popisky anotací, nadpis
TEXT_SEDY = "#606271"      # popisky os, kategorie, zdroj
MRIZKA = "#E7E7EB"         # vodorovné pomocné čáry
NULOVA_CARA = "#3A3A3A"    # čára nuly u sloupcových grafů
ZAKLADNA = "#616161"       # spodní osa u spojnicových grafů
ANOTACE_CARA = "#8A8A8A"   # svislá linka od bodu k popisku události
POZADI = "#FFFFFF"

# --- Rozměry (px při 200 dpi) -------------------------------------------------
DPI = 200
SIRKA_PX, VYSKA_PX = 1370, 722
PT = DPI / 72  # px na 1 bod písma

PISMO_OSA = 22 / PT        # ≈ 7,9 pt – popisky os a kategorií
PISMO_HODNOTA = 21.5 / PT  # ≈ 7,7 pt – hodnoty u sloupců
PISMO_LEGENDA = 24.5 / PT  # ≈ 8,8 pt – legenda
PISMO_ZDROJ = 21.5 / PT    # ≈ 7,7 pt – „Graf: Portu, zdroj: …“
PISMO_NADPIS = 36 / PT     # ≈ 13 pt – jen u varianty s nadpisem v obrázku

GRAF_LEVA, GRAF_PRAVA = 91, 1358   # okraje kreslicí plochy
POPISKY_Y_PRAVA = 71               # popisky osy y zarovnané vpravo k tomuto x
GRAF_HORNI = 37                    # horní mřížka
GRAF_DOLNI_1RADEK = 598            # spodní hrana plochy, popisky osy x na 1 řádek
GRAF_DOLNI_2RADKY = 556            # spodní hrana plochy, kategorie na 2 řádky
LEGENDA_STRED_Y = 698              # svislý střed legendy a zdroje
CTVEREC = 20                       # značka v legendě (zaoblený čtverec)

ZDROJ = "Graf: Portu, zdroj: Bloomberg"

_ADRESAR = os.path.dirname(os.path.abspath(__file__))
_PISMO = os.path.join(_ADRESAR, "fonty", "RethinkSans.ttf")
font_manager.fontManager.addfont(_PISMO)
_RODINA = font_manager.FontProperties(fname=_PISMO).get_name()
_TUCNE = font_manager.FontProperties(fname=os.path.join(_ADRESAR, "fonty", "RethinkSans-Bold.ttf"))
_STREDNI = font_manager.FontProperties(fname=os.path.join(_ADRESAR, "fonty", "RethinkSans-Medium.ttf"))
plt.rcParams.update({
    "font.family": _RODINA,
    "axes.unicode_minus": True,
    "svg.fonttype": "none",
})

MINUS = "−"
NBSP = " "
MESICE = {
    "cs": ["led", "úno", "bře", "dub", "kvě", "čvn", "čvc", "srp", "zář", "říj", "lis", "pro"],
    "sk": ["jan", "feb", "mar", "apr", "máj", "jún", "júl", "aug", "sep", "okt", "nov", "dec"],
}


# --- Formát čísel -------------------------------------------------------------
def cislo(hodnota: float, mista: int = 1, jednotka: str = "") -> str:
    """Český formát: desetinná čárka, pravé minus, mezera před %, tisíce s mezerou."""
    text = f"{abs(hodnota):,.{mista}f}".replace(",", NBSP).replace(".", ",")
    if hodnota < 0 and float(text.replace(NBSP, "").replace(",", ".")) != 0:
        text = MINUS + text
    if jednotka == "%":
        text += NBSP + "%"
    elif jednotka:
        text += jednotka if jednotka == "x" else NBSP + jednotka
    return text


def _fx(px: float) -> float:
    return px / SIRKA_PX


def _fy(px_shora: float) -> float:
    return 1 - px_shora / VYSKA_PX


PODNADPIS_PX = 36  # výška řádku s podnadpisem pod nadpisem


def _platno(dolni_px: float, horni_px: float = GRAF_HORNI, nadpis: str | None = None, navic: int = 0,
            podnadpis: str | None = None):
    """navic = další výška hlavičky pod nadpisem (např. pro velké číslo, viz _hlavicka_cislo).
    podnadpis = jednotka/upřesnění pod nadpisem fialově („v % HDP“, „Čtvrtletní údaje v miliardách USD“)."""
    posun = (70 if nadpis else 0) + (PODNADPIS_PX if podnadpis else 0) + navic
    vyska = VYSKA_PX + posun
    fig = plt.figure(figsize=(SIRKA_PX / DPI, vyska / DPI), dpi=DPI, facecolor=POZADI)

    def fy(px):
        return 1 - (px + posun) / vyska

    ax = fig.add_axes([_fx(GRAF_LEVA), fy(dolni_px), _fx(GRAF_PRAVA - GRAF_LEVA), fy(horni_px) - fy(dolni_px)])
    ax.set_facecolor(POZADI)
    for strana in ax.spines.values():
        strana.set_visible(False)
    ax.tick_params(length=0, colors=TEXT_SEDY, labelsize=PISMO_OSA)
    ax.grid(axis="y", color=MRIZKA, linewidth=1.0 * 72 / DPI * 1.4)
    ax.set_axisbelow(True)
    fig._portu = {"fy": fy, "vyska": vyska}
    if nadpis:
        if podnadpis:
            fig.text(_fx(GRAF_LEVA - 80), 1 - 76 / vyska, podnadpis, fontsize=PISMO_LEGENDA, color=FIALOVA,
                     fontproperties=_STREDNI, va="center")
        fig.text(_fx(GRAF_LEVA - 80), 1 - 30 / vyska, nadpis, fontsize=PISMO_NADPIS, color=TEXT_TMAVY,
                 ha="left", va="center")
    return fig, ax


HLAVICKA_PX = 110  # výška hlavičky s velkým číslem


def _hlavicka_cislo(fig, hodnota, zmena, popis, barva_zmeny=None):
    """Velké číslo s poslední hodnotou, vedle změna (např. „▼ −3,56 % (−0,0414) za 1 rok“), pod tím popis."""
    vyska = fig._portu["vyska"]
    x = _fx(GRAF_LEVA - 80)
    t = fig.text(x, 1 - 122 / vyska, hodnota, fontsize=64 / PT, color=TEXT_TMAVY, fontproperties=_TUCNE,
                 ha="left", va="baseline")
    sirka = t.get_window_extent(renderer=fig.canvas.get_renderer()).width
    barva = barva_zmeny or ZELENA
    x_zmena = x + _fx(sirka + 24)
    if zmena[:1] in ("▼", "▲"):  # Rethink Sans šipky nemá – trojúhelník jako tvar
        fig.add_artist(Line2D([x_zmena + _fx(9)], [1 - 111 / vyska], transform=fig.transFigure, linestyle="none",
                              marker="v" if zmena[0] == "▼" else "^", markersize=13 / PT, color=barva))
        zmena, x_zmena = zmena[1:].lstrip(), x_zmena + _fx(28)
    fig.text(x_zmena, 1 - 120 / vyska, zmena, fontsize=26 / PT, color=barva,
             fontproperties=_STREDNI, ha="left", va="baseline")
    fig.text(x, 1 - 160 / vyska, popis, fontsize=PISMO_LEGENDA, color=FIALOVA, ha="left", va="center_baseline")


def _vypln(ax, xs, hodnoty, barva, dolni):
    """Barevný přechod pod čarou: u čáry 35 % krytí, dole do bílé."""
    import numpy as np
    from matplotlib.colors import to_rgb
    from matplotlib.patches import Polygon
    xn = mdates.date2num(xs)
    body = [(xn[0], dolni)] + list(zip(xn, hodnoty)) + [(xn[-1], dolni)]
    tvar = Polygon(body, closed=True, facecolor="none", edgecolor="none")
    ax.add_patch(tvar)
    r, g, b = to_rgb(barva)
    prechod = np.zeros((256, 1, 4))
    prechod[:, 0, 0], prechod[:, 0, 1], prechod[:, 0, 2] = r, g, b
    prechod[:, 0, 3] = np.linspace(0.35, 0.0, 256)
    obr = ax.imshow(prechod, aspect="auto", extent=[xn[0], xn[-1], dolni, max(hodnoty)], origin="upper", zorder=1)
    obr.set_clip_path(tvar)


def _osa_y(ax, osa_y, jednotka, mista_osa):
    dolni, horni, krok = osa_y
    hodnoty = []
    v = dolni
    while v <= horni + 1e-9:
        hodnoty.append(round(v, 10))
        v += krok
    ax.set_ylim(dolni, horni)
    ax.set_yticks(hodnoty)
    ax.set_yticklabels([cislo(h, mista_osa, jednotka) for h in hodnoty])
    # popisky zarovnané vpravo, 20 px vlevo od plochy
    for t in ax.get_yticklabels():
        t.set_horizontalalignment("right")
    ax.tick_params(axis="y", pad=(GRAF_LEVA - POPISKY_Y_PRAVA) / PT)


def _legenda_a_zdroj(fig, polozky, zdroj):
    """polozky: (název, barva) = zaoblený čtvereček, (název, barva, 'cara') = čára s bodem."""
    fy = fig._portu["fy"]
    x = GRAF_LEVA + 3
    for polozka in polozky:
        nazev, barva = polozka[0], polozka[1]
        if len(polozka) > 2 and polozka[2] == "cara":
            sirka_znacky = 34
            fig.add_artist(Line2D([_fx(x), _fx(x + sirka_znacky)], [fy(LEGENDA_STRED_Y)] * 2, transform=fig.transFigure,
                                  color=barva, linewidth=3 / PT))
            fig.add_artist(Line2D([_fx(x + sirka_znacky / 2)], [fy(LEGENDA_STRED_Y)], transform=fig.transFigure,
                                  color=barva, marker="o", markersize=8 / PT, linestyle="none"))
        else:
            sirka_znacky = CTVEREC
            fig.patches.append(FancyBboxPatch(
                (_fx(x), fy(LEGENDA_STRED_Y + CTVEREC / 2)), _fx(CTVEREC), fy(LEGENDA_STRED_Y - CTVEREC / 2) - fy(LEGENDA_STRED_Y + CTVEREC / 2),
                boxstyle="round,pad=0,rounding_size=0.003", transform=fig.transFigure,
                facecolor=barva, edgecolor="none"))
        t = fig.text(_fx(x + sirka_znacky + 13), fy(LEGENDA_STRED_Y), nazev, fontsize=PISMO_LEGENDA,
                     color=TEXT_TMAVY, ha="left", va="center_baseline")
        sirka = t.get_window_extent(renderer=fig.canvas.get_renderer()).width
        x += sirka_znacky + 13 + sirka + 37
    if zdroj:
        fig.text(_fx(GRAF_PRAVA), fy(LEGENDA_STRED_Y), zdroj, fontsize=PISMO_ZDROJ, color=TEXT_SEDY,
                 ha="right", va="center_baseline")


# --- Sloupcový graf (svislé sloupce, seskupené řady) --------------------------
def sloupcovy(kategorie, rady: dict, osa_y, jednotka="%", mista=1, mista_osa=0,
              zdroj=ZDROJ, barvy=None, nadpis=None, sirka_zalomeni=None, legenda=True):
    """Seskupené svislé sloupce s hodnotami nad/pod sloupcem (styl „Zhodnocení tříd aktiv“).

    kategorie  – popisky pod sloupci (dlouhé se zalomí na 2 řádky)
    rady       – {název řady: [hodnoty v pořadí kategorií]}, max. 2–3 řady
    osa_y      – (min, max, krok)
    sirka_zalomeni – max. znaků na řádek popisku; None = podle šířky sloupce
    """
    barvy = barvy or BARVY
    if sirka_zalomeni is None:  # kolik znaků se vejde pod jeden sloupec (≈ 11,5 px na znak)
        sirka_zalomeni = max(6, int((GRAF_PRAVA - GRAF_LEVA) / len(kategorie) * 0.92 / 11.5))
    zalomene = [textwrap.fill(k, sirka_zalomeni) for k in kategorie]
    dva_radky = any("\n" in k for k in zalomene)
    fig, ax = _platno(GRAF_DOLNI_2RADKY if dva_radky else GRAF_DOLNI_1RADEK, nadpis=nadpis)
    _osa_y(ax, osa_y, jednotka, mista_osa)

    n_kat, n_rad = len(kategorie), len(rady)
    slot_px = (GRAF_PRAVA - GRAF_LEVA) / n_kat
    sloupec_px = min(0.24 * slot_px, 85) if n_rad > 1 else min(0.4 * slot_px, 110)
    mezera_px = 14
    ax.set_xlim(-0.5, n_kat - 0.5)
    sloupec = sloupec_px / slot_px
    mezera = mezera_px / slot_px
    skupina = n_rad * sloupec + (n_rad - 1) * mezera
    rozsah = osa_y[1] - osa_y[0]
    vyska_plochy_px = (GRAF_DOLNI_2RADKY if dva_radky else GRAF_DOLNI_1RADEK) - GRAF_HORNI
    odsazeni = 8 / vyska_plochy_px * rozsah

    for i, (nazev, hodnoty) in enumerate(rady.items()):
        xs = [k - skupina / 2 + i * (sloupec + mezera) + sloupec / 2 for k in range(n_kat)]
        ax.bar(xs, hodnoty, width=sloupec, color=barvy[i], zorder=2, linewidth=0)
        for x, h in zip(xs, hodnoty):
            if h is None:
                continue
            ax.text(x, h + (odsazeni if h >= 0 else -odsazeni), cislo(h, mista, jednotka),
                    ha="center", va="bottom" if h >= 0 else "top", fontsize=PISMO_HODNOTA, color=TEXT_TMAVY)
    if osa_y[0] < 0 < osa_y[1]:
        ax.axhline(0, color=NULOVA_CARA, linewidth=2 * 72 / DPI, zorder=3)
    ax.set_xticks(range(n_kat))
    ax.set_xticklabels(zalomene, fontsize=PISMO_OSA, color=TEXT_SEDY, linespacing=1.3)
    ax.tick_params(axis="x", pad=(580 - GRAF_DOLNI_2RADKY) / PT if dva_radky else 27 / PT)
    if legenda:
        _legenda_a_zdroj(fig, [(n, barvy[i]) for i, n in enumerate(rady)], zdroj)
    else:
        _legenda_a_zdroj(fig, [], zdroj)
    return fig


# --- Vodorovný sloupcový graf (pořadí, žebříčky) -------------------------------
def vodorovny(kategorie, hodnoty, osa_x, jednotka="%", mista=1, mista_osa=0, zdroj=ZDROJ,
              barva=FIALOVA, barvy_sloupcu=None, nazev_rady=None, nadpis=None):
    """Vodorovné sloupce seřazené shora dolů (žebříčky sektorů, akcií, zemí).

    osa_x         – (min, max, krok); nech rezervu, aby se hodnota u nejdelšího sloupce vešla
    barvy_sloupcu – volitelně barva pro každý sloupec (např. zvýraznění jedné položky zelenou)
    """
    levy_okraj, pravy_okraj = 300, GRAF_PRAVA - 30
    fig, ax = _platno(GRAF_DOLNI_1RADEK, nadpis=nadpis)
    fy = fig._portu["fy"]
    ax.set_position([_fx(levy_okraj), fy(GRAF_DOLNI_1RADEK), _fx(pravy_okraj - levy_okraj),
                     fy(GRAF_HORNI) - fy(GRAF_DOLNI_1RADEK)])
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=MRIZKA, linewidth=1.4 * 72 / DPI)
    dolni, horni, krok = osa_x
    ticks = []
    v = dolni
    while v <= horni + 1e-9:
        ticks.append(round(v, 10))
        v += krok
    ax.set_xlim(dolni, horni)
    ax.set_xticks(ticks)
    ax.set_xticklabels([cislo(t, mista_osa, jednotka) for t in ticks])
    ax.tick_params(axis="x", pad=27 / PT)
    n = len(kategorie)
    ys = list(range(n))[::-1]
    barvy = barvy_sloupcu or [barva] * n
    ax.barh(ys, hodnoty, height=0.62, color=barvy, zorder=2, linewidth=0)
    ax.set_yticks(ys)
    ax.set_yticklabels(kategorie, fontsize=PISMO_OSA, color=TEXT_SEDY)
    ax.tick_params(axis="y", pad=20 / PT)
    odsazeni = (horni - dolni) * 0.008
    for y, h in zip(ys, hodnoty):
        ax.text(h + (odsazeni if h >= 0 else -odsazeni), y, cislo(h, mista, jednotka),
                ha="left" if h >= 0 else "right", va="center", fontsize=PISMO_HODNOTA, color=TEXT_TMAVY)
    if dolni < 0 < horni:
        ax.axvline(0, color=NULOVA_CARA, linewidth=2 * 72 / DPI, zorder=3)
    _legenda_a_zdroj(fig, [(nazev_rady, barvy[0])] if nazev_rady else [], zdroj)
    return fig


# --- Spojnicový graf (časové řady) --------------------------------------------
def spojnicovy(x, rady: dict, osa_y, jednotka="", mista_osa=0, zdroj=ZDROJ, barvy=None,
               format_x="%m/%Y", interval_mesicu=6, interval_let=1, anotace=None, nadpis=None,
               rozsah_x=None, schody=(), popisky_konec=False, mista_konec=None, jednotka_konec=None,
               jazyk="cs", hlavicka=None, vypln=False, prvni_mesic=None,
               tloustka_cary=3.5, podnadpis=None):
    """Časové řady (styl „Ropa WTI a Brent“, „Forward P/E“).

    x            – seznam datumů (datetime/date) společný všem řadám
    rady         – {název řady: [hodnoty]} nebo {název: (vlastní datumy, hodnoty)};
                   pořadí určuje barvu (1. fialová, 2. zelená)
    osa_y        – (min, max, krok); jednotka '%', 'x' (násobky) nebo '' (prosté číslo)
    format_x     – '%m/%Y' (12/2024) pro víceleté řady po půlroce, '%Y' pro roky, '%-d. %-m.' pro dny,
                   'mesic' pro zkratky měsíců („lis 25“, slovensky „nov 25“) u řad za poslední rok (interval_mesicu=1)
    jazyk        – 'cs' nebo 'sk' (zkratky měsíců na ose x)
    prvni_mesic  – u format_x='%m/%Y' měsíc, od kterého se popisky počítají (1 → 01/2024, 07/2024 …)
    podnadpis    – řádek pod nadpisem fialově (jednotka, frekvence dat), jen spolu s nadpisem
    tloustka_cary – v px (výchozí 3,5); u hustých denních řad za více let 2,5, aby se čára neslévala
    hlavicka     – (velké číslo, změna, popis[, barva změny]) pod nadpisem, např. kurz a změna za rok
    vypln        – barevný přechod pod čarou první řady (jen na výslovné přání, Portu ho jinak nepoužívá)
    interval_let – u format_x='%Y' popisek každý n-tý rok (u řad přes 10 let 2)
    anotace      – [(datum, hodnota, 'text', 'pod'|'nad'), …] – bod na čáře + svislá linka + popisek
    schody       – názvy řad kreslených schodovitě (sazby centrálních bank platné do další změny)
    popisky_konec – poslední hodnota každé řady vpravo za koncem čáry („3,75 %“); u více řad
                    v barvě řady a blízké hodnoty automaticky odsunuté od sebe
    mista_konec  – desetinná místa koncového popisku; None = 1, u hodnot typu 3,75 dvě
    jednotka_konec – jednotka koncového popisku, když se liší od osy (např. 'b.' u indexu – mezeru před ní doplní cislo())
    """
    barvy = barvy or BARVY
    fig, ax = _platno(GRAF_DOLNI_1RADEK, nadpis=nadpis, navic=HLAVICKA_PX if hlavicka else 0, podnadpis=podnadpis)
    if hlavicka:
        _hlavicka_cislo(fig, *hlavicka)
    _osa_y(ax, osa_y, jednotka, mista_osa)
    konce = []
    for i, (nazev, data) in enumerate(rady.items()):
        xs, hodnoty = data if isinstance(data, tuple) else (x, data)
        ax.plot(xs, hodnoty, color=barvy[i], linewidth=tloustka_cary / PT, solid_joinstyle="round",
                drawstyle="steps-post" if nazev in schody else "default", zorder=3 + len(rady) - i)
        if vypln and i == 0:
            _vypln(ax, xs, hodnoty, barvy[i], osa_y[0])
        if popisky_konec:
            konce.append([h for h in hodnoty if h is not None][-1])
    if konce:
        # popisky blízkých hodnot od sebe odsuň, aby se nepřekrývaly (min. 26 px)
        mezera = 26 / (GRAF_DOLNI_1RADEK - GRAF_HORNI) * (osa_y[1] - osa_y[0])
        poradi = sorted(range(len(konce)), key=lambda k: konce[k])
        pozice = {k: konce[k] for k in poradi}
        for a, b in zip(poradi, poradi[1:]):
            if pozice[b] - pozice[a] < mezera:
                pozice[b] = pozice[a] + mezera
        posun = (sum(pozice.values()) - sum(konce)) / len(konce)  # vyrovnej kolem skutečných hodnot
        popisky = []
        for k, h in enumerate(konce):
            if mista_konec is None:  # 1 desetinné místo, u sazeb typu 3,75 % dvě
                mista = 2 if round(h, 1) != h and round(h, 2) == h else 1
            else:
                mista = mista_konec
            popisky.append(ax.annotate(cislo(h, mista, jednotka if jednotka_konec is None else jednotka_konec), (rozsah_x[1] if rozsah_x else x[-1], pozice[k] - posun),
                        xytext=(12 / PT, 0), textcoords="offset points", ha="left", va="center",
                        fontsize=PISMO_HODNOTA, annotation_clip=False,
                        color=barvy[k] if len(konce) > 1 else TEXT_TMAVY))  # u více řad v barvě řady
    # tmavá spodní osa; když řada klesá pod nulu, je tmavá místo ní čára nuly
    ax.axhline(0 if osa_y[0] < 0 < osa_y[1] else osa_y[0], color=ZAKLADNA, linewidth=2 * 72 / DPI, zorder=2)
    if rozsah_x:
        ax.set_xlim(*rozsah_x)
    else:
        ax.set_xlim(x[0], x[-1])
    if format_x == "mesic":
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval_mesicu, bymonthday=1))
    elif format_x == "%Y":
        ax.xaxis.set_major_locator(mdates.YearLocator(interval_let))
    else:
        # popisky od prvního měsíce řady (12/2024, 06/2025, 12/2025 …)
        prvni = prvni_mesic or (rozsah_x[0] if rozsah_x else x[0]).month
        mesice = sorted({(prvni - 1 + k * interval_mesicu) % 12 + 1 for k in range(max(1, 12 // interval_mesicu))})
        ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=mesice))
    if format_x == "mesic":
        ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
            lambda v, _: f"{MESICE[jazyk][mdates.num2date(v).month - 1]} {mdates.num2date(v).year % 100:02d}"))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter(format_x))
    for t in ax.get_xticklabels():
        t.set_fontsize(PISMO_OSA)
        t.set_color(TEXT_SEDY)
    ax.tick_params(axis="x", pad=29 / PT)
    rozsah = osa_y[1] - osa_y[0]
    vyska_px = GRAF_DOLNI_1RADEK - GRAF_HORNI
    for datum, hodnota, text, smer in anotace or []:
        ax.plot([datum], [hodnota], marker="o", markersize=6 / PT, color=FIALOVA, zorder=10)
        delka = 55 / vyska_px * rozsah
        konec = hodnota - delka if smer == "pod" else hodnota + delka
        ax.plot([datum, datum], [hodnota, konec], color=ANOTACE_CARA, linewidth=1.5 * 72 / DPI, zorder=9)
        ax.text(datum, konec + (-6 if smer == "pod" else 6) / vyska_px * rozsah, text,
                ha="center", va="top" if smer == "pod" else "bottom", fontsize=PISMO_OSA, color=TEXT_TMAVY)
    # okraje podle nejdelších popisků: osa y vlevo (např. „15 000“) a koncové popisky vpravo („11 581 b.“)
    renderer = fig.canvas.get_renderer()
    fig.canvas.draw()
    leva = max(GRAF_LEVA, max(t.get_window_extent(renderer).width for t in ax.get_yticklabels()) + 31)
    rezerva = 0
    if konce:
        rezerva = max(85, max(t.get_window_extent(renderer).width for t in popisky) + 22)
    pos = ax.get_position()
    ax.set_position([_fx(leva), pos.y0, _fx(GRAF_PRAVA - rezerva - leva), pos.height])
    _legenda_a_zdroj(fig, [(n, barvy[i]) for i, n in enumerate(rady)], zdroj)
    return fig


def uloz(fig, cesta: str):
    """Uloží PNG 1370 × 722 px (200 dpi). Neořezávat – rozměr je součástí vzhledu."""
    os.makedirs(os.path.dirname(os.path.abspath(cesta)), exist_ok=True)
    fig.savefig(cesta, dpi=DPI, facecolor=POZADI)
    plt.close(fig)
    return cesta

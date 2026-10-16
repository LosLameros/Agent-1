"""Odečet křivek z podkladového grafu Portfolio 10 vs. WOOD (Datawrapper, 1200 × 819 px) do CSV.

Kalibrace: osa y 0 % = y 659,5 px, 70 % = y 112,5 px; osa x 1. 7. 2023 = x 89,5 px, 1. 10. 2026 = x 1048 px.
Spouštěj z kořene repozitáře:
  python3 vystupy/grafy/2026-10-16-portu10-vs-wood-odecet.py podklady/grafy/2026-10-16-portu10-vs-wood-podklad.png vystupy/grafy/2026-10-16-portu10-vs-wood.csv
"""
from PIL import Image
import datetime as dt, csv, sys
im=Image.open(sys.argv[1]).convert('RGB')
X0,D0=89.5,dt.datetime(2023,7,1); X1,D1=1048.0,dt.datetime(2026,10,1)
ppd=(X1-X0)/(D1-D0).days
Y0,Y70=659.5,112.5
def val(y): return (Y0-y)/(Y0-Y70)*70
def near(p,c,t): return sum(abs(a-b) for a,b in zip(p,c))<t
TM=(0x00,0x52,0x7A); SV=(0x18,0xA1,0xCD)
TL=4
def trace(col):
    # 1) pro každý sloupec pixelů úsek čáry (horní a dolní okraj), navazující na předchozí sloupec
    sloupce=[]; prev=None
    for x in range(40,1075):
        ys=[y for y in range(60,668) if near(im.getpixel((x,y)),col,110)]
        if not ys: continue
        useky=[]; s=ys[0]; p=ys[0]
        for y in ys[1:]:
            if y-p>6: useky.append((s,p)); s=y  # mezery do 6 px = stále tatáž čára (ostré špičky)
            p=y
        useky.append((s,p))
        if prev is not None:
            s,p=min(useky,key=lambda u: abs((u[0]+u[1])/2-prev))
        else:
            s,p=useky[0]
        sloupce.append((x,s,p)); prev=(s+p)/2
    # 2) jeden bod na sloupec: střed čáry, u lokálního vrcholu/dna krajní okraj (aby se neztratily špičky)
    pts=[]
    for i,(x,s,p) in enumerate(sloupce):
        y=(s+p)/2
        if 0<i<len(sloupce)-1 and p-s>2*TL:
            (_,s1,p1),(_,s2,p2)=sloupce[i-1],sloupce[i+1]
            if s<=s1 and s<=s2 and (s<s1 or s<s2): y=s+TL/2      # vrchol
            elif p>=p1 and p>=p2 and (p>p1 or p>p2): y=p-TL/2    # dno
        pts.append((x,val(y)))
    return pts
tm=trace(TM); sv=trace(SV)
def datum(x): return D0+dt.timedelta(days=(x-X0)/ppd)
with open(sys.argv[2],'w',newline='') as f:
    w=csv.writer(f); w.writerow(['datum','rada','hodnota_pct'])
    for nazev,pts in (('portu_10',tm),('wood_opf',sv)):
        for x,v in pts: w.writerow([datum(x).strftime('%Y-%m-%d %H:%M'), nazev, round(v,2)])
print('body', len(tm), len(sv))
print('portu konec', round(tm[-1][1],2), datum(tm[-1][0]).date(), '| min duben 2025', min((round(v,2),str(datum(x).date())) for x,v in tm if 560<x<640), '| max', max((round(v,2),str(datum(x).date())) for x,v in tm))
print('wood konec', round(sv[-1][1],2), '| start', [(str(datum(x).date()),round(v,2)) for x,v in sv[:2]])

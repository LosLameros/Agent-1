const fs=require('fs'), path=require('path');
const {chromium}=require('playwright');
// Použití: node nastroje/grafy-ctvrtletni-zpravy.js podklady/RRRR-Qn/grafy-data.json
// Vykreslí dva úvodní grafy čtvrtletní zprávy v novém vzhledu Portu (bez nadpisu, logu a tabulky)
// do složky, ve které leží JSON: zhodnoceni-trid-aktiv.png a portfolia-v-roce.png (2000 × 1055 px).
// Vzor JSON: nastroje/grafy-ctvrtletni-zpravy.vzor.json

const W=2000, H=1055, LEFT=133, RIGHT=1983, TOP=55;
const C={rada1:'#4840BA', rada2:'#06B33F', grid:'#EAEAEA', nula:'#333333', osa:'#5C5D66', hodnota:'#282828', legenda:'#242424'};
// Rozvržení podle vzorových grafů: tříd aktiv je 7 (popisky na dva řádky), portfolií 3 (popisky na jeden řádek).
const PRESET={
  tridyAktiv:{soubor:'zhodnoceni-trid-aktiv.png', dolni:812, sirka:66, mezera:20, popisky:[881,937]},
  portfolia:{soubor:'portfolia-v-roce.png', dolni:862, sirka:127, mezera:14, popisky:[931]},
};
const MINUS='−', NBSP=' ';
const pct=v=>(v<0?MINUS:'')+Math.abs(v).toFixed(1).replace('.',',')+NBSP+'%';
const tick=v=>(v<0?MINUS:'')+String(Math.abs(Math.round(v*10)/10)).replace('.',',')+NBSP+'%';
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

function osaY(hodnoty,dolni,rucne){
  const vys=dolni-TOP, LABEL=55; // px rezerva pro popisek hodnoty nad/pod sloupcem
  const lo0=Math.min(0,...hodnoty), hi0=Math.max(0,...hodnoty);
  for(const krok of [1,2,5,10,20,25,50]){
    let lo=Math.floor(lo0/krok)*krok, hi=Math.ceil(hi0/krok)*krok;
    for(let i=0;i<4;i++){ const px=vys/(hi-lo);
      if(hi0>0&&(hi-hi0)*px<LABEL) hi+=krok; else if(lo0<0&&(lo0-lo)*px<LABEL) lo-=krok; else break; }
    if((hi-lo)/krok<=10) return {lo,hi,krok};
  }
  throw new Error('Rozsah hodnot je příliš velký.');
}

function zaobleny(x,y0,y1,w,r){ // sloupec od y0 (nula) k y1 (konec hodnoty), zaoblený jen na konci hodnoty
  const d=y1<y0?1:-1; r=Math.min(r,Math.abs(y1-y0)/2,w/2);
  return `M${x},${y0} L${x},${y1+d*r} Q${x},${y1} ${x+r},${y1} L${x+w-r},${y1} Q${x+w},${y1} ${x+w},${y1+d*r} L${x+w},${y0} Z`;
}

function svg(typ,g){
  const p=PRESET[typ];
  if(!g.kategorie||!g.hodnoty||g.kategorie.length!==g.hodnoty.length) throw new Error(typ+': počet kategorií a hodnot nesedí.');
  const vse=g.hodnoty.flat(); if(vse.some(v=>typeof v!=='number'||!isFinite(v))) throw new Error(typ+': každá hodnota musí být číslo.');
  const {lo,hi,krok}=g.osa||osaY(vse,p.dolni);
  const y=v=>TOP+(hi-v)*(p.dolni-TOP)/(hi-lo);
  const out=[];
  for(let t=hi;t>=lo-1e-9;t-=krok){ const yy=y(t);
    if(Math.abs(t)>1e-9) out.push(`<line x1="${LEFT}" x2="${RIGHT}" y1="${yy}" y2="${yy}" stroke="${C.grid}" stroke-width="2"/>`);
    out.push(`<text x="105" y="${yy+11}" text-anchor="end" font-size="32" fill="${C.osa}">${tick(t)}</text>`); }
  const sk=(RIGHT-LEFT)/g.kategorie.length;
  g.kategorie.forEach((kat,i)=>{
    const cx=LEFT+sk*(i+0.5), n=g.hodnoty[i].length, celk=n*p.sirka+(n-1)*p.mezera;
    g.hodnoty[i].forEach((v,j)=>{
      const x=cx-celk/2+j*(p.sirka+p.mezera), y0=y(0), y1=y(v);
      if(Math.abs(y1-y0)>=1) out.push(`<path d="${zaobleny(x,y0,y1,p.sirka,5)}" fill="${j?C.rada2:C.rada1}"/>`);
      const ly=v>=0?y1-19:y1+43;
      out.push(`<text class="val" data-g="${i}" x="${x+p.sirka/2}" y="${ly}" text-anchor="middle" font-size="30" fill="${C.hodnota}">${pct(v)}</text>`);
    });
    let radky=String(kat).split('\n');
    if(radky.length===1&&p.popisky.length===2){ const s=kat.split(' '); radky=s.length>1?[s.slice(0,-1).join(' '),s[s.length-1]]:[kat]; }
    radky.forEach((r,k)=>out.push(`<text x="${cx}" y="${p.popisky[k]}" text-anchor="middle" font-size="32" fill="${C.osa}">${esc(r)}</text>`));
  });
  out.push(`<line x1="${LEFT}" x2="${RIGHT}" y1="${y(0)}" y2="${y(0)}" stroke="${C.nula}" stroke-width="2.5"/>`);
  g.legenda.forEach((l,j)=>out.push(`<g class="leg"><rect x="137" y="1006" width="28" height="28" rx="5" fill="${j?C.rada2:C.rada1}"/><text x="184" y="1032" font-size="36" fill="${C.legenda}">${esc(l)}</text></g>`));
  out.push(`<text x="${RIGHT}" y="1032" text-anchor="end" font-size="32" fill="${C.osa}">${esc(g.zdroj||'Graf: Portu, zdroj: Bloomberg')}</text>`);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#fff"/>${out.join('')}</svg>`;
}

(async()=>{
  const json=process.argv[2]; if(!json){ console.error('Použití: node nastroje/grafy-ctvrtletni-zpravy.js <cesta k grafy-data.json>'); process.exit(1); }
  const data=JSON.parse(fs.readFileSync(json,'utf8')), dir=path.dirname(json);
  const F=path.join(__dirname,'fonty','rethink-sans');
  const face=(f,w,r)=>`@font-face{font-family:'Rethink Sans';font-weight:${w};src:url(data:font/woff2;base64,${fs.readFileSync(path.join(F,f)).toString('base64')}) format('woff2');unicode-range:${r};}`;
  const LAT='U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD';
  const EXT='U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF';
  const css=face('rethink-sans-latin-400-normal.woff2',400,LAT)+face('rethink-sans-latin-ext-400-normal.woff2',400,EXT)+
    `html,body{margin:0;background:#fff}svg{display:block;font-family:'Rethink Sans';font-weight:400}`;
  const browser=await chromium.launch(); const page=await browser.newPage({viewport:{width:W,height:H}});
  for(const typ of ['tridyAktiv','portfolia']){
    if(!data[typ]) continue;
    await page.setContent(`<!doctype html><meta charset="utf-8"><style>${css}</style>${svg(typ,data[typ])}`);
    await page.evaluate(async()=>{ await document.fonts.ready;
      if(!document.fonts.check("36px 'Rethink Sans'")) throw new Error('Písmo Rethink Sans se nenačetlo.');
      let x=137; for(const g of document.querySelectorAll('g.leg')){ const r=g.querySelector('rect'), t=g.querySelector('text');
        r.setAttribute('x',x); t.setAttribute('x',x+47); x+=47+t.getComputedTextLength()+68; }
      // Popisky dvou sloupců ve stejné výšce se nesmí překrývat: odsuň je od sebe do stran.
      const vals=[...document.querySelectorAll('text.val')];
      for(let i=1;i<vals.length;i++){ const a=vals[i-1], b=vals[i]; if(a.dataset.g!==b.dataset.g) continue;
        const ba=a.getBBox(), bb=b.getBBox(), prekryv=ba.x+ba.width+8-bb.x;
        if(prekryv>0&&Math.abs(ba.y-bb.y)<0.7*ba.height){ a.setAttribute('x',+a.getAttribute('x')-prekryv/2); b.setAttribute('x',+b.getAttribute('x')+prekryv/2); } } });
    const out=path.join(dir,PRESET[typ].soubor);
    await page.screenshot({path:out,clip:{x:0,y:0,width:W,height:H}}); console.log('ok',out);
  }
  await browser.close();
})().catch(e=>{console.error('Chyba:',e.message);process.exit(1);});

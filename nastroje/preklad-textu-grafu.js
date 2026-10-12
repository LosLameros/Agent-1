const fs=require('fs'), path=require('path');
const {chromium}=require('playwright');
// Použití: node nastroje/preklad-textu-grafu.js preklad.json
// Přepíše texty v hotovém grafu nového vzhledu (např. do polštiny), aniž by se měnila data:
// staré texty zabělí a nové vykreslí písmem Rethink Sans na stejné místo.
// JSON: {"vstup":"graf.webp","vystup":"graf-pl.png","texty":[{"smaz":[x0,y0,x1,y1],"text":"…","x":184,"y":1032,
//        "velikost":36,"barva":"#242424","zarovnani":"start|middle|end"}]}
// Souřadnice jsou v pixelech obrázku, y je účaří textu. Cesty jsou relativní ke složce JSON.

(async()=>{
  const json=process.argv[2]; if(!json){ console.error('Použití: node nastroje/preklad-textu-grafu.js <preklad.json>'); process.exit(1); }
  const d=JSON.parse(fs.readFileSync(json,'utf8')), dir=path.dirname(json), abs=p=>path.resolve(dir,p);
  const F=path.join(__dirname,'fonty','rethink-sans');
  const face=(f,r)=>`@font-face{font-family:'Rethink Sans';font-weight:400;src:url(data:font/woff2;base64,${fs.readFileSync(path.join(F,f)).toString('base64')}) format('woff2');unicode-range:${r};}`;
  const css=face('rethink-sans-latin-400-normal.woff2','U+0000-00FF,U+2000-206F,U+2212')+face('rethink-sans-latin-ext-400-normal.woff2','U+0100-02BA,U+1E00-1EFF')+
    'html,body{margin:0;background:#fff}svg{display:block;font-family:"Rethink Sans";font-weight:400}';
  const browser=await chromium.launch(), page=await browser.newPage();
  const ext=path.extname(d.vstup).slice(1).replace('jpg','jpeg');
  const img=`data:image/${ext};base64,${fs.readFileSync(abs(d.vstup)).toString('base64')}`;
  await page.setContent(`<!doctype html><meta charset="utf-8"><style>${css}</style><img id="i" src="${img}" style="display:none">`);
  const [W,H]=await page.evaluate(async()=>{ const i=document.getElementById('i'); await i.decode(); return [i.naturalWidth,i.naturalHeight]; });
  const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');
  const parts=d.texty.map(t=>(t.smaz?`<rect x="${t.smaz[0]}" y="${t.smaz[1]}" width="${t.smaz[2]-t.smaz[0]}" height="${t.smaz[3]-t.smaz[1]}" fill="#fff"/>`:'')+
    `<text x="${t.x}" y="${t.y}" font-size="${t.velikost}" fill="${t.barva||'#242424'}" text-anchor="${t.zarovnani||'start'}">${esc(t.text)}</text>`);
  await page.setViewportSize({width:W,height:H});
  await page.setContent(`<!doctype html><meta charset="utf-8"><style>${css}</style><svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}"><image href="${img}" width="${W}" height="${H}"/>${parts.join('')}</svg>`);
  if(d.texty.length) await page.evaluate(async()=>{ await document.fonts.ready; if(!document.fonts.check("32px 'Rethink Sans'")) throw new Error('Písmo Rethink Sans se nenačetlo.'); });
  await page.screenshot({path:abs(d.vystup),clip:{x:0,y:0,width:W,height:H}}); console.log('ok',abs(d.vystup));
  await browser.close();
})().catch(e=>{console.error('Chyba:',e.message);process.exit(1);});

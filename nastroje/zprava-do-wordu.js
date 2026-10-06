const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,AlignmentType,ImageRun,LevelFormat,BorderStyle}=require('docx');
// Použití: node nastroje/zprava-do-wordu.js vystupy/ctvrtletni-zpravy/RRRR-Qn.md podklady/RRRR-Qn vystupy/ctvrtletni-zpravy/RRRR-Qn-Ctvrtletni-zprava-Portu.docx
// Převede publikovatelnou část zprávy (od „# ČTVRTLETNÍ ZPRÁVA“ po „# INTERNÍ ČÁST“) do Wordu a vloží oba grafy z podkladů.
const [MD,CHARTS,OUT]=process.argv.slice(2);
const all=fs.readFileSync(MD,'utf8');
const lines=all.slice(all.indexOf('# ČTVRTLETNÍ ZPRÁVA'), all.indexOf('# INTERNÍ ČÁST')>0?all.indexOf('# INTERNÍ ČÁST'):undefined).split('\n');
const qm=all.match(/# ČTVRTLETNÍ ZPRÁVA (Q\d \d{4})/); const QLABEL=qm?qm[1]:'';
const GREEN='1A9E4B', DARK='1F1F1F';
function pngSize(f){const b=fs.readFileSync(f);return [b.readUInt32BE(16),b.readUInt32BE(20)];}
function imgFor(l){
  if(l.startsWith('**[GRAF V PŘÍLOZE: Zhodnocení vybraných tříd aktiv')) return CHARTS+'/zhodnoceni-trid-aktiv.png';
  if(l.startsWith('**[GRAF V PŘÍLOZE: Portfolia')) return CHARTS+'/portfolia-v-roce.png';
  return null;}
function runs(text,opts={}){
  // handle **bold** and *italic* segments minimally
  const out=[]; const re=/(\*\*[^*]+\*\*|\*[^*]+\*)/g; let last=0,m;
  while((m=re.exec(text))){ if(m.index>last) out.push(new TextRun({text:text.slice(last,m.index),...opts}));
    const t=m[0]; if(t.startsWith('**')) out.push(new TextRun({text:t.slice(2,-2),bold:true,...opts})); else out.push(new TextRun({text:t.slice(1,-1),italics:true,...opts}));
    last=m.index+t.length;}
  if(last<text.length) out.push(new TextRun({text:text.slice(last),...opts}));
  return out;
}
const kids=[];
let signature=false;
for(let raw of lines){
  const l=raw.trimEnd();
  if(!l||l==='---') continue;
  if(l.startsWith('# ')){ kids.push(new Paragraph({children:[new TextRun({text:'ČTVRTLETNÍ ZPRÁVA',bold:true,size:44,color:GREEN})]}));
    kids.push(new Paragraph({children:[new TextRun({text:QLABEL,bold:true,size:44,color:GREEN})]})); continue;}
  if(l==='**Komentář k vývoji portfolií**'){ kids.push(new Paragraph({spacing:{after:360},children:[new TextRun({text:'Komentář k vývoji portfolií',size:22,color:'666666'})]})); continue;}
  if(l.startsWith('## ')){ const first=kids.length<4; kids.push(new Paragraph({heading:first?HeadingLevel.HEADING_1:HeadingLevel.HEADING_2,children:[new TextRun(l.slice(3))]})); continue;}
  if(l.startsWith('- ')){ kids.push(new Paragraph({numbering:{reference:'b',level:0},children:runs(l.slice(2))})); continue;}
  const f0=imgFor(l); if(f0){ const f=f0; const [w,h]=pngSize(f); const W=600; kids.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:120,after:120},children:[new ImageRun({type:'png',data:fs.readFileSync(f),transformation:{width:W,height:Math.round(W*h/w)}})]})); continue;}
  if(l.startsWith('**[DOPLŇKOVÝ GRAF:')){ const [t,d='',src='']=l.slice('**[DOPLŇKOVÝ GRAF:'.length,-3).split('|').map(x=>x.trim()); const bd={style:BorderStyle.SINGLE,size:6,color:GREEN,space:4};
    const box={border:{top:bd,bottom:bd,left:bd,right:bd},shading:{fill:'F1F8F3',type:'clear',color:'auto'}};
    kids.push(new Paragraph({...box,spacing:{before:120},children:[new TextRun({text:'[NÁVRH GRAFU PRO SAZBU] Doplňkový graf: '+t,bold:true})]}));
    kids.push(new Paragraph({...box,children:[new TextRun(d)]}));
    kids.push(new Paragraph({...box,spacing:{after:120},children:[new TextRun({text:src,italics:true})]})); continue;}
  if(l.startsWith('[DOPLNIT')){ kids.push(new Paragraph({children:[new TextRun({text:l,highlight:'yellow'})]})); continue;}
  if(l==='Radim Krejčí'){ kids.push(new Paragraph({spacing:{before:480},children:[new TextRun({text:l,bold:true})]})); continue;}
  if(l==='CEO Portu'){ kids.push(new Paragraph({spacing:{after:240},children:[new TextRun(l)]})); continue;}
  if(l.startsWith('*\\*')){ kids.push(new Paragraph({children:[new TextRun({text:l.slice(1,-1).replace('\\*','*'),italics:true,size:18,color:'555555'})]})); continue;}
  if(l.startsWith('*')&&l.endsWith('*')){ kids.push(new Paragraph({children:[new TextRun({text:l.slice(1,-1),italics:true,size:18,color:'555555'})]})); continue;}
  kids.push(new Paragraph({children:runs(l)}));
}
const doc=new Document({
 styles:{default:{document:{run:{font:'Arial',size:22,color:DARK},paragraph:{spacing:{after:160,line:300}}}},
  paragraphStyles:[
   {id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,run:{size:32,bold:true,color:DARK,font:'Arial'},paragraph:{spacing:{before:120,after:200},outlineLevel:0}},
   {id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',quickFormat:true,run:{size:26,bold:true,color:GREEN,font:'Arial'},paragraph:{spacing:{before:320,after:140},outlineLevel:1}}]},
 numbering:{config:[{reference:'b',levels:[{level:0,format:LevelFormat.BULLET,text:'•',alignment:AlignmentType.LEFT,style:{paragraph:{indent:{left:720,hanging:360}}}}]}]},
 sections:[{properties:{page:{margin:{top:1134,bottom:1134,left:1247,right:1247}}},children:kids}]
});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT,b);console.log('ok',OUT)});

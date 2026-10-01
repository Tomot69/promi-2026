# PEUT-ON MÉLANGER LES MATIÈRES DANS UN MÊME PAVAGE ?
#  1 · Toile.preview engendre-t-elle une Toile neuve pour une boîte, et que publie-t-elle dans __c ?
#  2 · Toile.repaint(cv) respecte-t-elle __c.th (donc : mêmes germes, autre monde) ?
#  3 · les germes portent-ils leur POIDS (il faut la règle exacte du moteur : distance MOINS poids) ?
#  4 · la palette suit-elle le Studio, quel que soit le monde ?
import json
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/app.html'
Q=r"""()=>{
  const o={}, W=346, H=206, dpr=2;
  function neuf(){ const c=document.createElement('canvas'); c.width=W*dpr; c.height=H*dpr; return c; }
  const A=neuf();
  try{ window.Toile.preview(A,'encre',W,H); }catch(e){ o.previewErr=String(e); }
  o.aDesGermes = !!(A.__c && A.__c.seeds);
  if(A.__c){ o.n=A.__c.seeds.length; o.th=A.__c.th; o.champs=Object.keys(A.__c.seeds[0]);
    o.exemples=A.__c.seeds.slice(0,3).map(s=>({x:+s.x.toFixed(1),y:+s.y.toFixed(1),w:s.w,ci:s.ci,kind:s.kind,gray:s.gray}));
    o.colores=A.__c.seeds.filter(s=>s.kind!=='gray').length;
    o.poids=A.__c.seeds.map(s=>s.w); o.poidsDistincts=[...new Set(o.poids)].length; }
  /* 2 · les mêmes germes, un autre monde */
  const B=neuf();
  B.__c = A.__c ? {seeds:A.__c.seeds.map(s=>Object.assign({},s)), th:'sillons', pw:W, ph:H} : null;
  let rep=false; try{ window.Toile.repaint(B); rep=true; }catch(e){ o.repaintErr=String(e); }
  o.repaint=rep;
  if(rep){ const ga=A.getContext('2d').getImageData(0,0,A.width,A.height).data;
           const gb=B.getContext('2d').getImageData(0,0,B.width,B.height).data;
    let s=0,n=0, vides=0;
    for(let i=0;i<ga.length;i+=64){ s+=Math.abs(ga[i]-gb[i])+Math.abs(ga[i+1]-gb[i+1])+Math.abs(ga[i+2]-gb[i+2]); n++;
      if(gb[i+3]<10) vides++; }
    o.ecartAB=+(s/3/n).toFixed(1); o.videsB=+(100*vides/n).toFixed(1); }
  /* 3 · repaintWorld, la porte officielle */
  const C=neuf(); C.__c = A.__c ? {seeds:A.__c.seeds.map(s=>Object.assign({},s)), th:'encre', pw:W, ph:H} : null;
  let rw=false; try{ window.Toile.repaintWorld(C,'terrazzo'); rw=true; }catch(e){ o.rwErr=String(e); }
  o.repaintWorld=rw; if(rw) o.thApres=C.__c.th;
  /* 4 · la palette */
  try{ o.palette=window.Toile.getPalette&&window.Toile.getPalette(); }catch(e){ o.palette='?'; }
  try{ o.cols=(window.Toile.cols()||[]).length; }catch(e){ o.cols='?'; }
  try{ o.monde=window.Toile.mondeCourant(); }catch(e){}
  return o; }"""
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
    pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.wait_for_timeout(500)
    print(json.dumps(pg.evaluate(Q), ensure_ascii=False, indent=1)[:2600])
    br.close()

# CE QUE LA TOILE PERMET RÉELLEMENT — on énumère TOUTES les fenêtres et on rend la distribution,
# au lieu de choisir des seuils au jugé.
import json
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile3.html'
Q=r"""()=>{
  const CADW=346, CADH=206;
  const ids=(typeof promises!=='undefined'?promises:[]).filter(p=>!p.draft&&!p.req).map(p=>p.id);
  try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(e){}
  const base=(window.Toile.mondeCourant()||{}).m;
  function mat(id){ const c=document.createElement('canvas');
    let k=false; try{ k=window.Toile.dalleTrame(c,id,1,undefined); }catch(e){} return (k&&c.width)?c:null; }
  function teinte(cv){ const g=cv.getContext('2d'), d=g.getImageData(0,0,cv.width,cv.height).data;
    let r=0,v=0,b=0,n=0; for(let i=0;i<d.length;i+=16){ if(d[i+3]<40) continue; r+=d[i];v+=d[i+1];b+=d[i+2];n++; }
    return n?[r/n,v/n,b/n]:[0,0,0]; }
  const SEUIL=55;   /* deux dalles sont « de couleurs différentes » au-delà de 55 de distance RGB */
  function grappes(ts){ const c=[];
    for(const t of ts){ let pris=false;
      for(const g of c){ if(Math.hypot(t[0]-g[0][0],t[1]-g[0][1],t[2]-g[0][2])<SEUIL){ g.push(t); pris=true; break; } }
      if(!pris) c.push([t]); }
    return c.length; }
  const cells=[];
  ids.forEach(id=>{ let d=null; try{ d=window.Toile.dalleAbs(id); }catch(e){}
    if(d&&d.w>0){ const cv=mat(id); cells.push({id, x:d.minx,y:d.miny,w:d.w,h:d.h, t:cv?teinte(cv):null}); } });
  const BW=390, BH=844, S0=CADW/390, out=[];
  const groupesTotal=grappes(cells.filter(c=>c.t).map(c=>c.t));
  [S0,S0*1.06,S0*1.14,S0*1.23,S0*1.33,S0*1.45].forEach(s=>{
    const vw=CADW/s, vh=CADH/s; if(vw>BW+0.5||vh>BH+0.5) return;
    for(let ox=0; ox<=Math.max(0,BW-vw); ox+=12)
      for(let oy=0; oy<=Math.max(0,BH-vh); oy+=12){
        let n=0, aire=0; const ts=[];
        for(const c of cells){ const ix=Math.min(c.x+c.w,ox+vw)-Math.max(c.x,ox), iy=Math.min(c.y+c.h,oy+vh)-Math.max(c.y,oy);
          if(ix>0&&iy>0){ n++; aire+=ix*iy; if(c.t) ts.push(c.t); } }
        out.push({n, couv:aire/(vw*vh), g:grappes(ts)});
      } });
  return {cells:cells.length, groupesTotal, fenetres:out.length,
    max:{n:Math.max(...out.map(o=>o.n)), couv:Math.max(...out.map(o=>o.couv)), g:Math.max(...out.map(o=>o.g))},
    combos:[[7,0.34,5],[7,0.34,4],[7,0.30,4],[7,0.25,4],[8,0.34,4],[8,0.30,5],[9,0.30,4],[6,0.25,5]]
      .map(([a,b,c])=>({regle:a+'/'+b+'/'+c, n:out.filter(o=>o.n>=a&&o.couv>=b&&o.g>=c).length}))}; }"""
with sync_playwright() as p:
    br=p.chromium.launch()
    for th in ('light','dark'):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",th); pg.wait_for_timeout(600)
        pg.evaluate("()=>{ try{closeAll();}catch(e){} const b=document.querySelector('.set-cercle'); if(b) b.click(); }")
        pg.wait_for_timeout(2200)
        R=pg.evaluate(Q)
        print('══',th,'· %d dalles · %d fenêtres énumérées'%(R['cells'],R['fenetres']))
        print('   grappes de couleur de TOUTE la Toile :', R['groupesTotal'])
        print('   maxima atteignables : n=%d · couverture=%.2f · groupes=%d' % (R['max']['n'],R['max']['couv'],R['max']['g']))
        for c in R['combos']: print('     règle %-14s → %4d fenêtres' % (c['regle'], c['n']))
        pg.context.close()
    br.close()

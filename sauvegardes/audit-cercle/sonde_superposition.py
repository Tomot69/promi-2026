# DES DALLES QUI SE SUPERPOSENT (Tom, 12 sept.) — de GROSSES dalles empilées, pas un pavage plus fin.
# Chaque dalle est une VRAIE dalle du moteur : dalleTrame(cv, id, k, monde) — sa forme, ses contours, sa matière.
# On mesure : le coût, et ce qui reste du fond.
import json
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile9.html'
Q=r"""([N,COTE])=>{
  const W=346,H=206,dpr=Math.min(2,window.devicePixelRatio||1);
  const MONDES=['encre','mosaique','touffe','braille','pixel','sillons','gravure','terrazzo'];
  const ids=(typeof promises!=='undefined'?promises:[]).filter(p=>!p.draft&&!p.req).map(p=>p.id);
  try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(e){}
  const base=window.Toile.mondeCourant()||{};
  const cache={};
  function dalle(id, monde, cote){
    const cle=id+'|'+monde+'|'+cote; if(cache[cle]!==undefined) return cache[cle];
    let d=null; try{ d=window.Toile.dalleAbs(id); }catch(e){}
    if(!d||!d.w) return (cache[cle]=null);
    const k=cote/Math.max(d.w,d.h);
    const cv=document.createElement('canvas');
    let ok=false; try{ ok=window.Toile.dalleTrame(cv,id,k,{m:monde,p:base.p,h:base.h}); }catch(e){}
    return (cache[cle]=(ok&&cv.width)?cv:null);
  }
  const cible=document.createElement('canvas'); cible.width=Math.round(W*dpr); cible.height=Math.round(H*dpr);
  const G=cible.getContext('2d'); G.setTransform(dpr,0,0,dpr,0,0);
  const t0=performance.now(); let posees=0;
  for(let i=0;i<N;i++){
    const id=ids[(Math.random()*ids.length)|0], m=MONDES[(Math.random()*MONDES.length)|0];
    const cote=COTE*(0.72+Math.random()*0.62);
    const cv=dalle(id,m,Math.round(cote)); if(!cv) continue;
    const w=cv.width/dpr, h=cv.height/dpr;
    G.drawImage(cv, Math.random()*(W+w)-w/2, Math.random()*(H+h)-h/2, w, h);
    posees++;
  }
  const ms=Math.round(performance.now()-t0);
  const d=G.getImageData(0,0,cible.width,cible.height).data;
  let vide=0,n=0; for(let i=3;i<d.length;i+=32){ n++; if(d[i]<20) vide++; }
  return {N, cote:COTE, posees, rendus:Object.keys(cache).length, ms, fondVisible:+(100*vide/n).toFixed(2)}; }"""
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
    pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('light')"); pg.wait_for_timeout(500)
    print('  N dalles posées · côté visé · rendus distincts · coût · FOND VISIBLE')
    for N,cote in ((40,70),(80,70),(120,70),(160,70),(120,52),(200,52),(300,40)):
        print('   ', json.dumps(pg.evaluate(Q,[N,cote]), ensure_ascii=False))
    br.close()

# UNE COLLECTION DE VRAIES DALLES, RENDUE UNE FOIS, POSÉE DES CENTAINES DE FOIS.
# Chaque dalle : dalleTrame(cv, id, k, monde) — sa forme, ses contours, sa matière, à une bonne taille.
# La variété vient de la position, de la ROTATION et de l'ordre ; le recouvrement supprime le fond.
import json
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/scratchpad/app-vend-toile9.html'
Q=r"""([NID,NTAILLE,NPOSE,COTE])=>{
  const W=346,H=206,dpr=Math.min(2,window.devicePixelRatio||1);
  const MONDES=['encre','mosaique','touffe','braille','pixel','sillons','gravure','terrazzo'];
  const ids=(typeof promises!=='undefined'?promises:[]).filter(p=>!p.draft&&!p.req).map(p=>p.id);
  try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(e){}
  const base=window.Toile.mondeCourant()||{};
  const t0=performance.now();
  /* LA COLLECTION : NID Promi × 8 mondes × NTAILLE tailles, rendus UNE fois par le moteur */
  const COLL=[];
  const choisis=[]; for(let i=0;i<NID&&i<ids.length;i++) choisis.push(ids[(i*7)%ids.length]);
  const tailles=[]; for(let t=0;t<NTAILLE;t++) tailles.push(Math.round(COTE*(0.8+0.5*t/Math.max(1,NTAILLE-1))));
  choisis.forEach(id=>{
    let d=null; try{ d=window.Toile.dalleAbs(id); }catch(e){}
    if(!d||!d.w) return;
    MONDES.forEach(m=>{ tailles.forEach(cote=>{
      const k=cote/Math.max(d.w,d.h), cv=document.createElement('canvas');
      let ok=false; try{ ok=window.Toile.dalleTrame(cv,id,k,{m:m,p:base.p,h:base.h}); }catch(e){}
      if(ok&&cv.width) COLL.push({cv:cv, w:cv.width/dpr, h:cv.height/dpr, m:m});
    }); });
  });
  const msRendu=Math.round(performance.now()-t0);
  const t1=performance.now();
  const cible=document.createElement('canvas'); cible.width=Math.round(W*dpr); cible.height=Math.round(H*dpr);
  const G=cible.getContext('2d'); G.setTransform(dpr,0,0,dpr,0,0);
  for(let i=0;i<NPOSE;i++){
    const d=COLL[(Math.random()*COLL.length)|0]; if(!d) continue;
    const x=Math.random()*(W+d.w)-d.w/2, y=Math.random()*(H+d.h)-d.h/2;
    G.save(); G.translate(x+d.w/2, y+d.h/2); G.rotate(Math.random()*6.2832);
    G.drawImage(d.cv, -d.w/2, -d.h/2, d.w, d.h); G.restore();
  }
  const msPose=Math.round(performance.now()-t1);
  const px=G.getImageData(0,0,cible.width,cible.height).data;
  let vide=0,n=0; for(let i=3;i<px.length;i+=32){ n++; if(px[i]<20) vide++; }
  return {collection:COLL.length, rendus_ms:msRendu, poses:NPOSE, pose_ms:msPose,
          total_ms:msRendu+msPose, fondVisible:+(100*vide/n).toFixed(2)}; }"""
with sync_playwright() as p:
    br=p.chromium.launch(); pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
    pg.goto(URL,timeout=90000); pg.wait_for_timeout(7000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("()=>setTheme('light')"); pg.wait_for_timeout(500)
    print('  ids × tailles → collection · coût des rendus · poses · coût des poses · FOND VISIBLE')
    for NID,NT,NP,C in ((2,2,200,70),(3,2,300,70),(3,3,400,70),(4,3,600,70),(3,3,600,58),(4,3,900,58)):
        r=pg.evaluate(Q,[NID,NT,NP,C])
        print('   %d id × %d tailles → %3d dalles · %4d ms · %4d poses · %3d ms · total %4d ms · fond %5.2f %%'
              % (NID,NT,r['collection'],r['rendus_ms'],r['poses'],r['pose_ms'],r['total_ms'],r['fondVisible']))
    br.close()

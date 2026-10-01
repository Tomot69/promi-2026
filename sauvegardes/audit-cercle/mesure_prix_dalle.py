# LE PRIX D'UNE DALLE SELON SA TAILLE — c'est lui qui dimensionne la collection.
# Processeur ×1 puis ×4 (substitut de Lighthouse, pas un appareil).
import json
from playwright.sync_api import sync_playwright
URL='http://127.0.0.1:8752/scratchpad/app-vend-toileA.html'
Q=r"""(cotes)=>{
  const MONDES=['encre','mosaique','touffe','braille','pixel','sillons','gravure','terrazzo'];
  const ids=(typeof promises!=='undefined'?promises:[]).filter(p=>!p.draft&&!p.req).map(p=>p.id);
  try{ if(window.Toile.sync && !window.Toile.dalleAbs(ids[0])) window.Toile.sync(ids); }catch(e){}
  const base=window.Toile.mondeCourant()||{}, dpr=Math.min(2,window.devicePixelRatio||1);
  const out=[];
  cotes.forEach(cote=>{
    let t=0, n=0, px=0;
    MONDES.forEach(m=>{
      const id=ids[0]; let d=null; try{ d=window.Toile.dalleAbs(id); }catch(e){}
      if(!d||!d.w) return;
      const k=cote/Math.max(d.w,d.h), cv=document.createElement('canvas');
      const t0=performance.now();
      let ok=false; try{ ok=window.Toile.dalleTrame(cv,id,k,{m:m,p:base.p,h:base.h}); }catch(e){}
      t+=performance.now()-t0; n++;
      if(ok&&cv.width) px=Math.round(cv.width/dpr)+'×'+Math.round(cv.height/dpr);
    });
    out.push({cote, ms:+(t/Math.max(1,n)).toFixed(1), rendu:px});
  });
  return out; }"""
with sync_playwright() as p:
    br=p.chromium.launch()
    for ral in (1,4):
        pg=br.new_context(viewport={'width':430,'height':932},device_scale_factor=2).new_page()
        cdp=pg.context.new_cdp_session(pg); cdp.send('Emulation.setCPUThrottlingRate',{'rate':ral})
        pg.goto(URL,timeout=180000); pg.wait_for_timeout(9000 if ral==1 else 26000)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.wait_for_timeout(600)
        R=pg.evaluate(Q,[50,70,90,110,130,150])
        print('══ processeur ×%d — coût MOYEN d’une dalle (8 mondes), et sa taille rendue' % ral)
        for e in R: print('     côté %3d → %6.1f ms   (%s)' % (e['cote'], e['ms'], e['rendu']))
        # budget : combien de dalles pour 1,5 s
        for e in R:
            if e['ms']>0: print('        à ce prix, 1,5 s permet %d dalles' % int(1500/e['ms']))
        cdp.send('Emulation.setCPUThrottlingRate',{'rate':1}); pg.context.close()
    br.close()

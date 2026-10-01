# Banc d'expérience : dessin forcé (10 canevas distincts) d'un monde sous différents drapeaux window._X
import sys, json
from playwright.sync_api import sync_playwright
APP, MONDE = sys.argv[1], sys.argv[2]; VARS = json.loads(sys.argv[3]); WK = '--webkit' in sys.argv; RATE=4 if '--x4' in sys.argv else 1
JS = r"""async (a)=>{ Toile.setTheme(a.m); await new Promise(r=>setTimeout(r,800)); const o={};
 for(const v of a.vars){ window._X=v.x; window._shLabels=false; window._MS=0; window._MDc=0; window._MDh=0; const M=[],Q=[];
  for(let r=0;r<5;r++){ const cs=[]; for(let k=0;k<10;k++){ const c=document.createElement('canvas'); c.width=780;c.height=1688; c.getContext('2d',v.wrf?{willReadFrequently:true}:undefined).getImageData(0,0,1,1); cs.push(c);}
   const t0=performance.now(); for(const c of cs){ Toile.renderTo(c,2);} Q.push((performance.now()-t0)/10); for(const c of cs) c.getContext('2d').getImageData(0,0,1,1); M.push((performance.now()-t0)/10);}
  M.sort((x,y)=>x-y);
  const d=[]; let n=0, t0=performance.now(); window._shLabels=undefined;
  await new Promise(res=>{ function f(t){ d.push(t-t0); t0=t; Toile.refigeCouleurs(); if(++n<50) requestAnimationFrame(f); else res(); } requestAnimationFrame(f); });
  d.splice(0,6); Q.sort((x,y)=>x-y); const _cnt={seule:window._MS,md:window._MDc,hit:window._MDh}; o[v.n]={cnt:_cnt, calcul:+Q[2].toFixed(1), dessin:+M[2].toFixed(1), ecran:+(d.reduce((x,y)=>x+y,0)/d.length).toFixed(1)}; }
 window._X=null; window._shLabels=undefined; return o; }"""
with sync_playwright() as p:
    b=(p.webkit if WK else p.chromium).launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2); pg=ctx.new_page()
    pg.goto('http://127.0.0.1:8752/'+APP); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    if RATE>1: ctx.new_cdp_session(pg).send('Emulation.setCPUThrottlingRate',{'rate':RATE})
    print(('webkit' if WK else 'chromium×%d'%RATE), json.dumps(pg.evaluate(JS,{'m':MONDE,'vars':VARS}))); b.close()

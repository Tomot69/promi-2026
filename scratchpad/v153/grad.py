import sys, math; sys.path.insert(0,'.')
import numpy as np, banc_tom as B
from playwright.sync_api import sync_playwright
pol, gr, car = sys.argv[1:4]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-trace-lettres.html'); pg.wait_for_timeout(1200)
    pg.add_script_tag(url='http://127.0.0.1:8752/variantes/trace-chemins-atkinson.js'); pg.wait_for_timeout(300)
    r=pg.evaluate("""async a=>{ const [pol,gr,car]=a; TraceLettres._debug=1; TraceLettres._cache={}; const el=document.createElement('div'); el.style.cssText='position:fixed;left:60px;top:80px;font:'+gr+' 150px/180px '+pol+';color:#291547;z-index:60'; el.textContent=car; document.body.appendChild(el);
      await document.fonts.load(gr+' 150px '+pol); const c=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await c.pret; c.va(0.5); const d=TraceLettres._derniere;
      return {w:d.w,h:d.h,T:Array.from(d.T),own:Array.from(d.own),bouts:d.bouts}; }""",[pol,gr,car])
    b.close()
w,h=r['w'],r['h']; T=np.array(r['T']).reshape(h,w); own=np.array(r['own']).reshape(h,w)
gy,gx=np.gradient(T); mag=np.hypot(gx,gy)
ok=(own>=0)&(mag>0.3)&(mag<3)
# erode: interior
m=ok.copy()
for dy in (-2,-1,0,1,2):
    for dx in (-2,-1,0,1,2): m&=np.roll(np.roll(ok,dy,0),dx,1)
ys,xs=np.nonzero(m)
ang=np.degrees(np.arctan2(gy[m],gx[m]))
# compare gradient direction with local direction estimated by T iso: the gradient IS along path if front perpendicular; compare to path tangent: approximate path tangent by direction toward higher-T neighbors along the medial... use own trait endpoints unknown -> report spread of gradient direction vs neighbor gradient smoothness
print('pixels', len(xs))
# local consistency: gradient direction vs its 7x7 neighbourhood mean direction
import scipy

import sys, json; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx)
    pg.evaluate("()=>{ closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
    c=pg.evaluate("()=>{const e=document.querySelector('#studioScreen .stp-ton'); const r=e.getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    pg.touchscreen.tap(c[0],c[1]); pg.wait_for_timeout(1200)
    print(json.dumps(pg.evaluate("""()=>{ const D=document.getElementById('device').getBoundingClientRect(), k=D.width/390;
      const R=e=>{ if(!e) return null; const r=e.getBoundingClientRect(); return [Math.round((r.left-D.left)/k*10)/10, Math.round((r.top-D.top)/k*10)/10, Math.round(r.width/k*10)/10, Math.round(r.height/k*10)/10]; };
      const ps=[...document.querySelectorAll('#stpPals .st3-p')]; const last=ps.slice(-6).map(R);
      const cs=e=>{const c=getComputedStyle(e); return [c.position,c.zIndex,c.overflow,c.pointerEvents];};
      return {spec:R(document.getElementById('st3spec')), thumb:R(document.getElementById('st3thumb')), nb:R(document.querySelector('.stp-nb')), nbcs:cs(document.querySelector('.stp-nb')), pn:R(document.getElementById('st3pn')), pals:R(document.getElementById('stpPals')), palscs:cs(document.getElementById('stpPals')), last:last, pcs:cs(ps[0]), speccs:cs(document.getElementById('st3spec')),
        bas:R(document.getElementById('stpBas')), buy:R(document.getElementById('stLockBuy')), sibs:[...document.getElementById('stpPals').children].map(e=>(e.id||e.className)+':'+JSON.stringify(R(e))) }; }"""), indent=0))
    b.close()

import sys, time; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b); pg=B.ouvre(ctx)
    pg.evaluate("()=>{ window._onbCompteFait=()=>true; closeAll(); document.getElementById('studioBtn').click(); }"); pg.wait_for_timeout(2500)
    for i in range(12):
        lk=pg.evaluate("()=>({w:window._lockedWorld, lock:document.getElementById('studioScreen').classList.contains('world-locked'), m:Toile.mondeCourant().m})")
        if lk['lock']: break
        B.glisse(pg, B.droite([300,330],[80,330],10), pas=18); pg.wait_for_timeout(1500)
    print(lk)
    B.capture(pg,'scratchpad/v155/u0.png')
    c=pg.evaluate("()=>{const r=document.getElementById('stLockBuy').getBoundingClientRect(); return [r.left+r.width/2,r.top+r.height/2];}")
    t=time.time(); pg.touchscreen.tap(c[0],c[1])
    for k in range(6):
        B.capture(pg,'scratchpad/v155/u%d.png'%(k+1)); print(k+1, round((time.time()-t)*1000))
    print(pg.evaluate("()=>({w:window._lockedWorld, lock:document.getElementById('studioScreen').classList.contains('world-locked'), m:Toile.mondeCourant().m})"))
    b.close()

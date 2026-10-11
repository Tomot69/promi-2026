import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=contexte(b,sombre=len(sys.argv)>1); pg=ouvre(ctx)
    tap_sel(pg,'#studioBtn'); pg.wait_for_timeout(6000)
    for k in range(14):
        glisse(pg, droite((320,300),(80,300),10), pas=16); pg.wait_for_timeout(1600)
        if 'world-locked' in pg.evaluate("()=>document.getElementById('studioScreen').className"): break
    pg.wait_for_timeout(2000)
    print(pg.evaluate("""()=>{ const dv=document.getElementById('device').getBoundingClientRect(),k=dv.width/390; const o=[]; [...document.querySelectorAll('#studioScreen *')].forEach(e=>{ const r=e.getBoundingClientRect(), c=getComputedStyle(e); if(r.height<2||c.display==='none'||c.visibility==='hidden') return; const t=[...e.childNodes].filter(n=>n.nodeType===3).map(n=>n.textContent.trim()).join(''); if(!t) return; o.push((e.id||e.className)+' «'+t.slice(0,24)+'» ['+[r.left-dv.left,r.top-dv.top,r.width,r.height].map(v=>Math.round(v/k)).join(',')+'] col '+c.color+' sh '+c.textShadow+' pe '+c.pointerEvents+' fs '+c.fontSize); }); const R=s=>{const e=document.querySelector(s); if(!e) return s+':absent'; const r=e.getBoundingClientRect(); return s+' ['+[r.left-dv.left,r.top-dv.top,r.width,r.height].map(v=>Math.round(v/k)).join(',')+'] pe '+getComputedStyle(e).pointerEvents+' ta '+getComputedStyle(e).touchAction}; return o.join('\\n')+'\\n'+['#stBg','#stpBas','#stLockBuy','#stLockCta','#studioScreen .enh','#accRappelCompte','#stcCadre'].map(R).join('\\n'); }"""))
    b.close()

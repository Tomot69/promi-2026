import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx)
    B.plante(pg, 'rendre le livre'); pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(3000)
    pg.evaluate("""()=>{ window.__L=[]; document.addEventListener('touchend',()=>{ const t0=performance.now(); (function f(){ const cv=document.getElementById('tenirMaree'), it=document.getElementById('instTenue'), dp=document.getElementById('detailPoster');
      window.__L.push([Math.round(performance.now()-t0), !!cv, cv?cv.getAttribute('aria-label'):null, it?it.textContent:null, dp.classList.contains('inst-referme'), it?getComputedStyle(it).display:null, it?Math.round(it.getBoundingClientRect().width):null, window._instant]); if(performance.now()-t0<1500) requestAnimationFrame(f); })(); },{capture:true}); }""")
    z = pg.evaluate("()=>{ const c=document.getElementById('tenirZone'), r=c.getBoundingClientRect(), d=document.getElementById('device').getBoundingClientRect(), k=d.width/390; return [(r.top-d.top)/k, r.height/k]; }")
    B.glisse(pg, [[200 + 150 * i / 10, z[0] + z[1] * 0.45] for i in range(11)], pas=30, tenue=380); pg.wait_for_timeout(1800)
    L = pg.evaluate("()=>window.__L"); prev = None
    for l in L:
        k = l[1:]
        if k != prev: print(l); prev = k
    b.close()

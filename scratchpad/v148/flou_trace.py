import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
LIT = """()=>{ const D=document.getElementById('device'); const out=[]; D.querySelectorAll('*').forEach(e=>{ const c=getComputedStyle(e); if((c.filter&&c.filter!=='none')||(c.backdropFilter&&c.backdropFilter!=='none')||(c.webkitBackdropFilter&&c.webkitBackdropFilter!=='none')){ const r=e.getBoundingClientRect(); if(r.width>20&&r.height>20) out.push([e.id||e.className.toString().slice(0,30), c.filter, c.backdropFilter||c.webkitBackdropFilter, +c.opacity]); } }); return {poster:document.getElementById('detailPoster').className, f:out.slice(0,12)}; }"""
for F in ('app.html', 'zz-av147.html'):
    with sync_playwright() as p:
        b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx, F)
        B.plante(pg, 'rendre le livre', qui='Marion'); pg.wait_for_timeout(800)
        pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(3000)
        z = pg.evaluate("()=>{ const v=(document.getElementById('dpTrameCv').getAttribute('data-trait')||'').split(','); return +v[0]; }")
        P = [list(B.pt(pg, 200 + 150 * i / 16, z + 8)) for i in range(17)]
        pg.evaluate("(a)=>{ window.__gl=(" + B.GLISSE + ")(a); return 1; }", [P, 95, 380, 11, 11])
        for _ in range(60):
            pg.wait_for_timeout(80)
            if pg.evaluate("()=>!!document.querySelector('#tenirZone.atteint')"): break
        pg.wait_for_timeout(250); print(F, pg.evaluate(LIT)); b.close()

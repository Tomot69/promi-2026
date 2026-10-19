import sys; sys.path.insert(0,'.')
import banc_tom as B
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.webkit.launch()
    for et in ('studio','plus'):
      for s in (False,True):
        ctx = B.contexte(b, sombre=s); pg = B.ouvre(ctx, 'app.html', attente=6000)
        pg.evaluate("e=>_guide.montre(e,true)", et)
        for t in range(10):
            pg.wait_for_timeout(1000)
            if pg.evaluate("()=>!!document.getElementById('guidePhrase')"): break
        pg.wait_for_timeout(3000)
        print(et, s, pg.evaluate("()=>[...document.querySelectorAll('#guidePhrase i')].map(e=>[e.textContent, getComputedStyle(e).webkitTextFillColor, e.className])"), pg.evaluate("()=>{const p=document.getElementById('guidePhrase'); return p&&[p.textContent, getComputedStyle(p).webkitTextFillColor]}"))
        ctx.close()
    b.close()

import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
E = "()=>{ const g=document.getElementById('guide'), p=document.getElementById('guidePhrase'); return [g?g.getAttribute('data-guide'):null, g?+(g.getAttribute('data-rappels')||0):0, p?p.textContent.slice(0,20):null]; }"
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = B.ouvre(ctx)
    pg.evaluate("()=>{ localStorage.removeItem('promi_guide'); _guide.attend(false); }")
    for _ in range(80):
        pg.wait_for_timeout(150)
        if pg.evaluate("()=>{ const e=_guide.etat(); return e.etat==='studio' && e.net>=1; }"): break
    print('départ', pg.evaluate(E))
    for x, y in ((195, 250), (195, 760), (300, 500)):
        B.tap(pg, x, y); pg.wait_for_timeout(900); print('toucher', (x, y), pg.evaluate(E))
    b.close()

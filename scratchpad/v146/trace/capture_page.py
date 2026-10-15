# capture_page.py — la page de démonstration comme Tom la voit (WebKit, 390 × 844, échelle 3, doigt) : quelques états, enregistrés ici
import sys; sys.path.insert(0, '../../..')
from playwright.sync_api import sync_playwright
import banc_tom as B
URL = 'http://127.0.0.1:8752/promi-trace-lettres.html'
quoi = sys.argv[1] if len(sys.argv) > 1 else 'tout'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = ctx.new_page(); err = []
    pg.on('pageerror', lambda e: err.append(str(e)[:300])); pg.on('console', lambda m: err.append(m.text[:300]) if m.type == 'error' else None)
    pg.goto(URL + '?vitesse=0.05'); pg.wait_for_timeout(1500)
    pg.screenshot(path='page-1-haut.png')
    r = pg.evaluate("()=>{const r=document.getElementById('scene').getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]}")
    pg.touchscreen.tap(r[0], r[1]); pg.wait_for_timeout(2600); pg.screenshot(path='page-2-titre-mi-trace.png')
    pg.evaluate("()=>{ _demo.E.vitesse=1; }")
    for i in range(2): pg.touchscreen.tap(r[0], r[1]); pg.wait_for_timeout(1500)
    pg.evaluate("()=>{ _demo.E.vitesse=0.25; }"); pg.touchscreen.tap(r[0], r[1]); pg.wait_for_timeout(5200); pg.screenshot(path='page-3-texte-mi-trace.png')
    pg.wait_for_timeout(7000); pg.screenshot(path='page-4-texte-fini.png')
    # la loupe, avec les chemins
    pg.evaluate("()=>{ _demo.E.vitesse=0.05; document.getElementById('bChemins').click(); document.querySelector('.loupes').scrollIntoView({block:'start'}); window.scrollBy(0,-90); }"); pg.wait_for_timeout(500)
    pg.screenshot(path='page-5-loupe-chemins.png')
    r2 = pg.evaluate("()=>{const r=_demo.loupes[0].getBoundingClientRect(); return [r.left+r.width/2, r.top+r.height/2]}"); pg.touchscreen.tap(r2[0], r2[1]); pg.wait_for_timeout(5200); pg.screenshot(path='page-6-loupe-mi-trace.png')
    pg.evaluate("()=>{ document.getElementById('bSombre').click(); document.getElementById('tout').scrollIntoView({block:'start'}); window.scrollBy(0,-60); _demo.E.vitesse=0.25; }"); pg.wait_for_timeout(300)
    r3 = pg.evaluate("()=>{const r=document.getElementById('tout').getBoundingClientRect(); return [r.left+r.width/2, r.top+120]}"); pg.touchscreen.tap(r3[0], r3[1]); pg.wait_for_timeout(4200); pg.screenshot(path='page-7-alphabet-sombre.png')
    print('erreurs :', err); print(pg.evaluate("()=>document.getElementById('mesure').textContent"))
    b.close()

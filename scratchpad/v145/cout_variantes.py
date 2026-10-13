import sys, io, json; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 760}, device_scale_factor=3, has_touch=True, is_mobile=True, user_agent=B.UA)
    print('charge', B.charge())
    for v in 'ABC':
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-guide-variantes.html?v=%s' % v); pg.wait_for_timeout(5500)
        pg.evaluate("()=>window._avance()"); pg.wait_for_timeout(4200); pg.evaluate("()=>window._avance()"); pg.wait_for_timeout(1600)
        r = pg.evaluate("()=>window._mesureDerniere"); print('guide', v, {k: r[k] for k in ('images', 'sup20', 'sup33', 'pire', 'dessin_p50', 'dessin_p95', 'dessin_max')} if r else None, flush=True); pg.close()
    for v in 'ABC':
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-tenir-variantes.html?v=%s' % v); pg.wait_for_timeout(3000)
        pg.evaluate("()=>window._joue()"); pg.wait_for_timeout(4200)
        print('tenir', v, pg.evaluate("()=>document.getElementById('mes').textContent").replace('\n', ' | '), flush=True); pg.close()
    b.close()

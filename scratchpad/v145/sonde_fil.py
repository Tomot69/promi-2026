import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import banc_tom as B
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); B.toile_pleine(ctx, 10); pg = B.ouvre(ctx)
    r = B.tap_sel(pg, '#filBtn'); pg.wait_for_timeout(2500)
    print('tap', r, pg.evaluate("""()=>{ var fv=document.getElementById('feedView'); var L=document.querySelectorAll('#feedList > *'); return {cls:fv&&fv.className, n:L.length, premier:L[0]&&L[0].className, items:document.querySelectorAll('#feedList .fd-item').length, minis:document.querySelectorAll('#feedList canvas.mini-dalle').length, txt:(document.getElementById('feedList').textContent||'').slice(0,160)}; }"""))
    b.close()

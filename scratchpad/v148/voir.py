import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
def dev(pg): return pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
def shot(pg, y0=0, y1=844):
    d = dev(pg); k = d[2] / 390.0
    return Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0], 'y': d[1] + y0 * k, 'width': d[2], 'height': (y1 - y0) * k})))
page = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
th = sys.argv[2] if len(sys.argv) > 2 else 'light'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, sombre=(th=='dark')); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + page); pg.wait_for_timeout(7000)
    B.plante(pg, 'rendre le livre', qui='Marion'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2500)
    shot(pg).save('scratchpad/v148/fiche-%s.png' % th)
    pg.evaluate("()=>{ try{ window._peaufSortie&&window._peaufSortie(); }catch(e){} closeAll(); }"); pg.wait_for_timeout(800)
    B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(1200)
    pg.evaluate("()=>{ const x=[...document.querySelectorAll('#createSheet .tile')][0]||[...document.querySelectorAll('.acc-un')][0]; x&&x.click(); }"); pg.wait_for_timeout(2500)
    shot(pg).save('scratchpad/v148/plus-%s.png' % th)
    b.close()

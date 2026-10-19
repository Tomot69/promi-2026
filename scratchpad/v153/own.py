import sys; sys.path.insert(0, '.')
import numpy as np
from PIL import Image
import banc_tom as B
from playwright.sync_api import sync_playwright
pol, gr, car = sys.argv[1], sys.argv[2], sys.argv[3]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/promi-trace-lettres.html'); pg.wait_for_timeout(1200)
    pg.add_script_tag(url='http://127.0.0.1:8752/variantes/trace-chemins-atkinson.js'); pg.wait_for_timeout(300)
    r = pg.evaluate("""async a=>{ const [pol,gr,car]=a; TraceLettres._debug=1; TraceLettres._cache={}; let el=document.createElement('div'); el.style.cssText='position:fixed;left:60px;top:80px;font:'+gr+' 150px/180px '+pol+';color:#291547;z-index:60'; el.textContent=car; document.body.appendChild(el);
      await document.fonts.load(gr+' 150px '+pol); const c=TraceLettres.trace(el,null,{manuel:true,respecteReduire:false}); await c.pret; c.va(0.5); const d=TraceLettres._derniere; return {w:d.w,h:d.h,own:Array.from(d.own),T:Array.from(d.T)}; }""", [pol, gr, car])
    w, h = r['w'], r['h']; own = np.array(r['own']).reshape(h, w); T = np.array(r['T']).reshape(h, w)
    cols = {-1: (0, 0, 0), -2: (255, 255, 255), 0: (255, 60, 60), 1: (60, 200, 60), 2: (60, 100, 255), 3: (230, 200, 0), 4: (200, 0, 200)}
    im = np.zeros((h, w, 3), np.uint8)
    for k, c in cols.items(): im[own == k] = c
    Image.fromarray(im).save('scratchpad/v153/own-%s%s.png' % (pol[0], car))
    tm = T.copy(); tm[T <= 0] = 0; tm = (255 * tm / max(1, tm.max())).astype(np.uint8)
    Image.fromarray(tm).save('scratchpad/v153/T-%s%s.png' % (pol[0], car))
    b.close()

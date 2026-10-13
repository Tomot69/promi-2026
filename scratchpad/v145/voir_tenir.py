import sys, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
import banc_tom as B
v = sys.argv[1]; nat = sys.argv[2] if len(sys.argv) > 2 else 'promi'; th = sys.argv[3] if len(sys.argv) > 3 else 'clair'
T = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else [-1, 150, 400, 700, 1100, 1600, 1900, 2150, 9000]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 760}, device_scale_factor=2, has_touch=True, is_mobile=True, user_agent=B.UA)
    pg = ctx.new_page(); err = []; pg.on('pageerror', lambda e: err.append(str(e)[:300])); pg.on('console', lambda m: err.append('console: ' + m.text[:200]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:8752/promi-tenir-variantes.html?v=%s&nat=%s&th=%s' % (v, nat, th)); pg.wait_for_timeout(2500)
    ims = []
    for t in T:
        pg.evaluate("t=>window._fige(t)", t); pg.wait_for_timeout(250)
        r = pg.evaluate("()=>{ var q=document.getElementById('toile').getBoundingClientRect(); return [q.left,q.top,q.width,q.height]; }")
        ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x': r[0], 'y': r[1], 'width': r[2], 'height': r[3]}))).convert('RGB'))
    w, h = ims[0].size; k = 300.0 / w; out = Image.new('RGB', (int(len(ims) * 306), int(h * k)), '#777')
    for i, im in enumerate(ims): out.paste(im.resize((300, int(h * k))), (i * 306, 0))
    out.save('scratchpad/v145/tenir-%s-%s-%s.png' % (v, nat, th)); print('erreurs', err[:4], out.size)
    b.close()

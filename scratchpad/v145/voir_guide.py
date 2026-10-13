import sys, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
import banc_tom as B
th = sys.argv[1] if len(sys.argv) > 1 else 'clair'
POSES = [('studio', 0), ('studio', 500), ('studio', 1100), ('studio', 2600), ('studio', 6000), ('plus', 500), ('plus', 1100), ('plus', 2400), ('plus', 6000)]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 760}, device_scale_factor=2, has_touch=True, is_mobile=True, user_agent=B.UA)
    pg = ctx.new_page(); err = []; pg.on('pageerror', lambda e: err.append(str(e)[:300]))
    pg.goto('http://127.0.0.1:8752/promi-guide-variantes.html?th=%s' % th); pg.wait_for_timeout(3000)
    rows = []
    for v in ('A', 'B', 'C'):
        ims = []
        for et, ms in POSES:
            n = pg.evaluate("a=>window._fige(a[0],a[1],a[2])", [v, et, ms]); pg.wait_for_timeout(200)
            r = pg.evaluate("()=>{ var q=document.getElementById('scene').getBoundingClientRect(); return [q.left,q.top,q.width,q.height]; }")
            ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x': r[0], 'y': r[1], 'width': r[2], 'height': r[3]}))).convert('RGB'))
        rows.append(ims)
    w, h = rows[0][0].size; k = 220.0 / w; out = Image.new('RGB', (len(POSES) * 226, 3 * (int(h * k) + 6)), '#777')
    for j, ims in enumerate(rows):
        for i, im in enumerate(ims): out.paste(im.resize((220, int(h * k))), (i * 226, j * (int(h * k) + 6)))
    out.save('scratchpad/v145/guide-%s.png' % th); print('erreurs', err[:4], out.size, pg.evaluate("()=>window._etat()"))
    b.close()

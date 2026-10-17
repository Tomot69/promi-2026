import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
def shot(pg):
    d = B.dev(pg); return Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]})))
with sync_playwright() as p:
    b = p.webkit.launch(); ims = []
    for th in ('light', 'dark'):
        ctx = B.contexte(b, sombre=(th == 'dark')); pg = B.ouvre(ctx)
        B.plante(pg, 'rendre le livre', qui='Marion'); pg.wait_for_timeout(800)
        pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(3000)
        ims.append(shot(pg))
        z = pg.evaluate("()=>{ const v=(document.getElementById('dpTrameCv').getAttribute('data-trait')||'').split(','); return +v[0]; }")
        P = [list(B.pt(pg, 200 + 150 * i / 16, z + 8)) for i in range(17)]
        pg.evaluate("(a)=>{ window.__gl=(" + B.GLISSE + ")(a); return 1; }", [P, 95, 380, 11, 11])
        for _ in range(60):
            pg.wait_for_timeout(80)
            if pg.evaluate("()=>!!(window._ruban && window._ruban.etat().actif)"): break
        pg.wait_for_timeout(250); ims.append(shot(pg)); ctx.close()
    w, h = ims[0].size; o = Image.new('RGB', (w * 4 + 60, h), (255, 255, 255))
    for i, im in enumerate(ims): o.paste(im, (i * (w + 20), 0))
    o = o.resize((o.width // 3, o.height // 3)); o.save('scratchpad/v148/ruban_vue.png'); print('ok')
    b.close()

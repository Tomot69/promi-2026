import sys; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
import io
with sync_playwright() as p:
    b = p.webkit.launch()
    for th in ('light', 'dark'):
        ctx = B.contexte(b, sombre=(th == 'dark')); pg = B.ouvre(ctx)
        pg.evaluate("()=>{ _guide.montre('studio', true); }"); pg.wait_for_timeout(700)
        ims = []
        for t in (500, 5000):
            pg.wait_for_timeout(t if not ims else t - 500)
            d = B.dev(pg); r = pg.evaluate("()=>{const p=document.getElementById('guidePhrase'), D=document.getElementById('device').getBoundingClientRect(); const q=p.getBoundingClientRect(); return [q.left-D.left-6,q.top-D.top-6,q.width+12,q.height+12];}")
            im = Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0] + r[0], 'y': d[1] + r[1], 'width': r[2], 'height': r[3]})))
            ims.append(im)
        # comparer la fin du tracé au texte rendu sans tracé
        pg.evaluate("()=>{ _guide.finir(); }"); pg.wait_for_timeout(2500)
        W = max(i.size[0] for i in ims); H = sum(i.size[1] for i in ims)
        pl = Image.new('RGB', (W, H), 'white'); y = 0
        for i in ims: pl.paste(i, (0, y)); y += i.size[1]
        pl.save('scratchpad/v148/guide_gras_%s.png' % th); ctx.close()
    b.close()

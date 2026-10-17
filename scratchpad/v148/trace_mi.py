import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image
def shot(pg):
    d = B.dev(pg); return Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0], 'y': d[1], 'width': d[2], 'height': d[3]})))
th = sys.argv[1] if len(sys.argv) > 1 else 'light'; quoi = sys.argv[2] if len(sys.argv) > 2 else 'fiche'; page = sys.argv[3] if len(sys.argv) > 3 else 'app.html'
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = B.contexte(b, sombre=(th == 'dark')); pg = B.ouvre(ctx, page)
    ims = []
    if quoi == 'fiche':
        B.plante(pg, 'rendre le livre', qui='Marion'); pg.wait_for_timeout(800)
        pg.evaluate("()=>{ closeAll(); openDetail(promises[promises.length-1].id); }"); pg.wait_for_timeout(2600)
        z = pg.evaluate("()=>{ const e=document.getElementById('tenirZone'), D=document.getElementById('device').getBoundingClientRect(), k=D.width/390, r=e.getBoundingClientRect(); return [(r.top-D.top)/k,(r.height)/k]; }")
        y = z[0] + z[1] * 0.45
    else:
        B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(700)
        B.tap_sel(pg, '.acc-pil[data-k=promi]'); pg.wait_for_timeout(2500)
        pg.evaluate("()=>{ document.getElementById('fTitle').value='lire un livre'; }")
        y = pg.evaluate("()=>_ppEcran().base")
    ims.append(shot(pg))
    X0 = 60 if quoi == 'plus' else 200
    P = [list(B.pt(pg, X0 + 150 * i / 16, y)) for i in range(17)]
    pg.evaluate("(a)=>{ window.__gl=(" + B.GLISSE + ")(a); return 1; }", [P, 70, 380, 11, 11])
    pg.wait_for_timeout(1050); ims.append(shot(pg))
    pg.wait_for_timeout(150); ims.append(shot(pg))
    w, h = ims[0].size; o = Image.new('RGB', (w * 3 + 40, h), (255, 255, 255))
    for i, im in enumerate(ims): o.paste(im, (i * (w + 20), 0))
    o = o.resize((o.width // 4, o.height // 4)); o.save('scratchpad/v148/trace-%s-%s.png' % (quoi, th)); print('ok', y)
    b.close()

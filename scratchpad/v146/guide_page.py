# v146 — la page du guide : une planche d'états arrêtés (clair et sombre), et une séquence filmée image par image
import sys, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
ET = [('couvre', 0.08, None), ('couvre', 0.22, None), ('couvre', 0.42, None), ('couvre', 0.65, None), ('couvre', 0.88, None), ('net', 0.3, 'studio'), ('net', 0.65, 'studio'), ('net', 1, 'studio'), ('net', 0.4, 'plus'), ('net', 1, 'plus')]
with sync_playwright() as p:
    b = p.webkit.launch(); errs = []
    for th in ('clair', 'sombre'):
        ctx = b.new_context(viewport={'width': 390, 'height': 892}, device_scale_factor=3, has_touch=True, is_mobile=True); pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:8752/promi-guide-variantes.html?fige=1&th=' + th); pg.wait_for_timeout(1500)
        ims = []
        for quoi, u, cible in ET:
            r = pg.evaluate("a=>window._guidePage.fige(a[0], a[1], a[2])", [quoi, u, cible]); pg.wait_for_timeout(250)
            ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x': 0, 'y': 48, 'width': 390, 'height': 844}))).convert('RGB'))
        W = Image.new('RGB', (5 * (ims[0].width + 30), 2 * (ims[0].height + 30)), (40, 40, 40))
        for i, im in enumerate(ims): W.paste(im, ((i % 5) * (im.width + 30), (i // 5) * (im.height + 30)))
        W.save('planche-v146/PLANCHE-4-guide-flaques-%s.png' % th); W.resize((W.width // 4, W.height // 4)).save('scratchpad/v146/pl4-%s.png' % th)
        # la zone du Studio et celle du +, à pleine résolution
        z = Image.new('RGB', (3 * 420 + 20, 330), (40, 40, 40))
        for k, i in enumerate((7, 9)): z.paste(ims[i].crop((0, 2532 - 420, 1170, 2532 - 90)).resize((620, 175)), (k * 640, 0))
        ims[7].crop((60, 2532 - 400, 480, 2532 - 130)).save('scratchpad/v146/pl4-zoom-studio-%s.png' % th); ims[9].crop((380, 2532 - 440, 800, 2532 - 110)).save('scratchpad/v146/pl4-zoom-plus-%s.png' % th)
        ctx.close()
    print('erreurs', errs[:3]); b.close()

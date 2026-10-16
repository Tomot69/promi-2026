"""le guide, figé : la couverture à plusieurs instants, la zone nette du Studio et du + — python3 scratchpad/v147/guide_vue.py DOSSIER"""
import sys, io; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
OUT = sys.argv[1]
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','light');}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html?gfige=200'); pg.wait_for_timeout(7000)
    ims = []
    for ms in (150, 300, 450, 600, 800, 1000, 1200):
        pg.evaluate("ms=>window._guide.figeA(ms)", ms); pg.wait_for_timeout(150); ims.append(Image.open(io.BytesIO(pg.screenshot())).convert('RGB').resize((195, 422)))
    for ms in (120, 280, 450, 700):
        pg.evaluate("ms=>window._guide.figeNet('studio', ms)", ms); pg.wait_for_timeout(200); ims.append(Image.open(io.BytesIO(pg.screenshot())).convert('RGB').resize((195, 422)))
    print(pg.evaluate("()=>window._guide.etat()"))
    pg.evaluate("ms=>window._guide.figeNet('studio', 700)", 700); pg.wait_for_timeout(300); pg.screenshot(path=OUT + '/guide-studio.png')
    pg.evaluate("ms=>window._guide.figeNet('plus', 700)", 700); pg.wait_for_timeout(300); pg.screenshot(path=OUT + '/guide-plus.png')
    b.close()
c = Image.new('RGB', (195 * len(ims), 422)); [c.paste(im, (i * 195, 0)) for i, im in enumerate(ims)]; c.save(OUT + '/guide-seq.png')

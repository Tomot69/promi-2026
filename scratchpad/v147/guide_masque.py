"""le masque de l'eau du guide (le canevas #guideEau), figé à plusieurs instants : noir = eau, blanc = net — python3 scratchpad/v147/guide_masque.py DOSSIER"""
import sys, io, base64; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
OUT = sys.argv[1]
MASQ = "()=>{ const c=document.getElementById('guideEau'); return c.toDataURL('image/png'); }"
with sync_playwright() as p:
    b = p.webkit.launch(); ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_theme','light');}catch(e){}")
    pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html?gfige=200'); pg.wait_for_timeout(7000)
    ims = []
    for ms in (80, 160, 240, 320, 400, 480, 560, 700, 900, 1100):
        pg.evaluate("ms=>window._guide.figeA(ms)", ms); pg.wait_for_timeout(80)
        im = Image.open(io.BytesIO(base64.b64decode(pg.evaluate(MASQ).split(',')[1]))).convert('RGBA'); a = im.split()[3].point(lambda v: 0 if v > 10 else 255)
        ims.append(a.resize((195, 422)))
    c = Image.new('L', (195 * len(ims) + 4 * len(ims), 422), 128); [c.paste(im, (i * 199, 0)) for i, im in enumerate(ims)]; c.save(OUT + '/masque-couv.png')
    Z = []
    for ms in (60, 140, 220, 300, 400, 520, 700):
        pg.evaluate("ms=>window._guide.figeNet('studio', ms)", ms); pg.wait_for_timeout(80)
        im = Image.open(io.BytesIO(base64.b64decode(pg.evaluate(MASQ).split(',')[1]))).convert('RGBA'); a = im.split()[3].point(lambda v: 0 if v > 10 else 255)
        Z.append(a.crop((10 * 2, 700 * 2, 110 * 2, 810 * 2)).resize((200, 220)))
    c = Image.new('L', (204 * len(Z), 220), 128); [c.paste(im, (i * 204, 0)) for i, im in enumerate(Z)]; c.save(OUT + '/masque-studio.png')
    b.close()

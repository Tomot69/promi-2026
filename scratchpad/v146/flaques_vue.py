import sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
q = sys.argv[1] if len(sys.argv) > 1 else ''
nom = sys.argv[2] if len(sys.argv) > 2 else 'flaques'
with sync_playwright() as p:
    b = p.webkit.launch(); pg = b.new_page(viewport={'width': 1640, 'height': 900}, device_scale_factor=2); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:8752/scratchpad/v146/flaques-essai.html' + q); pg.wait_for_function('()=>window.__pret===true', timeout=30000)
    print('flou fait en %.0f ms' % pg.evaluate('()=>window.__floute'), pg.evaluate('()=>window.__ms'), errs)
    pg.screenshot(path='scratchpad/v146/%s.png' % nom, full_page=True); b.close()
from PIL import Image
im = Image.open('scratchpad/v146/%s.png' % nom); im.resize((im.width // 2, im.height // 2)).save('scratchpad/v146/%s-vue.png' % nom); print(im.size)

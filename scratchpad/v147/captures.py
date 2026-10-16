import sys, io; sys.path.insert(0, '.')
import banc_tom as B
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
def dev(pg): return pg.evaluate("()=>{const r=document.getElementById('device').getBoundingClientRect(); return [r.left,r.top,r.width,r.height];}")
def shot(pg, y0=0, y1=844):
    d = dev(pg); k = d[2] / 390.0
    return Image.open(io.BytesIO(pg.screenshot(clip={'x': d[0], 'y': d[1] + y0 * k, 'width': d[2], 'height': (y1 - y0) * k})))
quoi = sys.argv[1:] or ['menu', 'onb', 'guide']
with sync_playwright() as p:
    b = p.webkit.launch()
    if 'menu' in quoi:
        ims = []
        for page in ('zz-av146.html', 'app.html'):
            ctx = B.contexte(b); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/' + page); pg.wait_for_timeout(7000)
            pg.evaluate("()=>{ try{ if(typeof setTheme==='function') setTheme('light'); }catch(e){} }"); pg.wait_for_timeout(600)
            B.tap_sel(pg, '#createBtn'); pg.wait_for_timeout(1200); ims.append(shot(pg, 400, 820)); ctx.close()
        w, h = ims[0].size; out = Image.new('RGB', (w * 2 + 24, h), (255, 255, 255)); out.paste(ims[0], (0, 0)); out.paste(ims[1], (w + 24, 0))
        out.save('planche-v147/1-menu-plus-avant-apres.png'); print('menu', out.size)
    if 'onb' in quoi:
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=3, has_touch=True)
        ctx.add_init_script("try{ localStorage.setItem('promi_theme','light'); }catch(e){}")
        pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(9000)
        pg.evaluate("()=>{ const e=document.getElementById('onbPh'); e&&e.click(); }"); pg.wait_for_timeout(400)
        pg.keyboard.type('Camille', delay=30); pg.keyboard.press('Enter'); pg.wait_for_timeout(5000)
        pg.keyboard.type('marcher une heure', delay=25); pg.keyboard.press('Enter'); pg.wait_for_timeout(6000)
        shot(pg).save('planche-v147/2-premier-promi-clair.png'); print('onb ok', pg.evaluate("()=>!!document.getElementById('onbTrait')")); ctx.close()
    if 'guide' in quoi:
        ctx = B.contexte(b); pg = ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(7000)
        pg.evaluate("()=>{ try{ if(typeof setTheme==='function') setTheme('light'); }catch(e){} }"); pg.wait_for_timeout(600)
        pg.evaluate("()=>{ _guide.montre('studio'); }"); pg.wait_for_timeout(9000)
        shot(pg).save('planche-v147/3-guide-studio-clair.png'); print('guide', pg.evaluate("()=>{ const p=document.getElementById('guidePhrase'); return p&&p.textContent; }")); ctx.close()
    b.close()

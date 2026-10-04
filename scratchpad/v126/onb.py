# captures de chaque diapositive de l'onboarding, clair et sombre (@3x), + contraste mesuré des mots en couleur
import sys, io, json
from playwright.sync_api import sync_playwright
from PIL import Image
OUT='planche-v126/onb'+(sys.argv[1] if len(sys.argv)>1 else '')
import os; os.makedirs(OUT, exist_ok=True)
def lum(c):
    f=lambda v:(v/255/12.92 if v/255<=0.04045 else ((v/255+0.055)/1.055)**2.4); return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])
def cr(a,b): x,y=lum(a),lum(b); return (max(x,y)+0.05)/(min(x,y)+0.05)
MOTS = r"""()=>{ const dv=document.getElementById('device').getBoundingClientRect(); return [...document.querySelectorAll('#onbV .onbv-nat')].filter(e=>e.getBoundingClientRect().height>0 && +getComputedStyle(e.closest('.onbv-f')||e).opacity>0.5).map(e=>{ const r=e.getBoundingClientRect(); return {mot:e.textContent, col:getComputedStyle(e).color.match(/\d+/g).slice(0,3).map(Number), x:r.left, y:r.top, w:r.width, h:r.height}; }); }"""
with sync_playwright() as p:
    b = p.webkit.launch(); res=[]
    for th in ('light','dark'):
        ctx = b.new_context(viewport={'width':430,'height':932}, device_scale_factor=3)
        ctx.add_init_script("try{localStorage.setItem('promi_theme','%s')}catch(e){}" % th)
        pg = ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:200]))
        pg.goto('http://127.0.0.1:8752/app.html'+(('?voisines='+sys.argv[1]) if len(sys.argv)>1 else '')); pg.wait_for_timeout(7000)
        pg.evaluate("(t)=>{ try{setTheme(t)}catch(e){} try{ window._onbNat&&_onbNat(); }catch(e){} }", th); pg.wait_for_timeout(800)
        def cap(nom):
            f='%s/onb-%s-%s.png' % (OUT, nom, th); pg.screenshot(path=f, clip={'x':20,'y':44,'width':390,'height':844})
            im=Image.open(f).convert('RGB'); px=im.load()
            for m in pg.evaluate(MOTS):
                # le fond réellement peint autour du mot : la couleur la plus fréquente de sa boîte élargie
                h={}; x0=int((m['x']-20)*3); y0=int((m['y']-44)*3); 
                for y in range(max(0,y0-6), min(im.size[1], y0+int(m['h']*3)+6), 2):
                    for x in range(max(0,x0-6), min(im.size[0], x0+int(m['w']*3)+6), 2):
                        c=px[x,y]; h[c]=h.get(c,0)+1
                fond=max(h, key=h.get)
                res.append((nom, th, m['mot'], '#%02X%02X%02X' % tuple(m['col']), '#%02X%02X%02X' % fond, round(cr(m['col'], fond),2)))
        cap('1-prenom')
        pg.mouse.click(20+195, 44+260); pg.wait_for_timeout(300); pg.keyboard.type('Tom', delay=40); pg.wait_for_timeout(400); cap('1b-prenom-saisi')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(900); cap('2-parole')
        pg.keyboard.type('appeler Mamie dimanche', delay=25); pg.wait_for_timeout(500); cap('2b-parole-saisie')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(900); cap('3-trait')
        # tracer la moitié du trait
        r = pg.evaluate("()=>{const c=document.getElementById('onbTrait').getBoundingClientRect(); return [c.left,c.top,c.width,c.height]}")
        y = r[1]+r[3]*0.6; pg.mouse.move(r[0]+r[2]*0.11, y); pg.mouse.down()
        for i in range(1,26): pg.mouse.move(r[0]+r[2]*(0.11+0.42*i/25), y); pg.wait_for_timeout(16)
        pg.mouse.up(); pg.wait_for_timeout(3400); cap('4-fin')
        pg.wait_for_timeout(3200); pg.mouse.click(20+195, 44+420); pg.wait_for_timeout(1200); cap('5-compte')
        ctx.close()
    for r in res: print(r)
    b.close()

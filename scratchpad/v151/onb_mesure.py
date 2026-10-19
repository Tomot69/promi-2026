# v151 §5 §6 §7 : en sombre, la couleur de « trace pour planter » (page du trait) et de Primo/Deuxio/Tertio (fin), le fond réel sous eux (pixels)
import io, sys; sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
from PIL import Image
exec(open('redteam_onb_sorties.py', encoding='utf-8').read().split('with sync_playwright() as p:')[0].replace("R6 = '--r6' in sys.argv", "R6 = True").replace("res = []; sorties = []", "sorties = []"))
F = sys.argv[1] if len(sys.argv) > 1 else 'app.html'
URL='http://127.0.0.1:8752/' + F
def L(c):
    c=[x/255 for x in c]; c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]; return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b): la,lb=sorted([L(a),L(b)],reverse=True); return (la+0.05)/(lb+0.05)
def fond(png, box, k):
    im=Image.open(png).convert('RGB'); x0,y0,x1,y1=[int(v*k) for v in box]
    # le fond : la couleur la plus fréquente dans une bande de 6 pt autour de la boîte (le texte exclu)
    from collections import Counter
    C=Counter()
    for y in range(max(0,y0-int(6*k)), min(im.height,y1+int(6*k))):
        for x in range(max(0,x0-int(6*k)), min(im.width,x1+int(6*k))):
            if x0<=x<x1 and y0<=y<y1: continue
            C[im.getpixel((x,y))]+=1
    return C.most_common(1)[0][0]
BOX = """s=>[...document.querySelectorAll(s)].filter(e=>e.getBoundingClientRect().width>2).map(e=>{ const r=document.createRange(); r.selectNodeContents(e); const b=r.getBoundingClientRect(); const c=getComputedStyle(e).webkitTextFillColor||getComputedStyle(e).color; return [e.textContent.trim().slice(0,24), c, [b.left,b.top,b.right,b.bottom]]; })"""
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=metal', '--enable-gpu', '--ignore-gpu-blocklist'])
    for th in (sys.argv[2:] or ['dark']):
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, has_touch=True, color_scheme=th)
        if th == 'dark': ctx.add_init_script("try{ if(!sessionStorage.getItem('_t')){ sessionStorage.setItem('_t','1'); localStorage.setItem('promi_theme','dark'); } }catch(e){}")
        pg = ctx.new_page(); pg.goto(URL); pg.wait_for_timeout(6500); cdp = ctx.new_cdp_session(pg)
        prenom(pg, cdp); parole(pg); pg.wait_for_timeout(1500); saisie(pg); pg.wait_for_timeout(3000)
        png='scratchpad/v151/onb_trait_%s.png' % th; pg.screenshot(path=png)
        for t, c, bx in pg.evaluate(BOX, '#onbTrace'):
            f=fond(png, bx, 2); rgb=[int(v) for v in c[c.index('(')+1:c.index(')')].split(',')[:3]]
            print(th, 'TRACE', t, c, 'fond', f, 'contraste %.2f' % cr(rgb, f))
        trace(pg, cdp); pg.wait_for_timeout(5200)
        for _ in range(3): toucher(cdp, pg, 195, 260); pg.wait_for_timeout(3600)
        png='scratchpad/v151/onb_fin_%s.png' % th; pg.screenshot(path=png)
        for t, c, bx in pg.evaluate(BOX, '#onbV .onbv-fin .onbv-k'):
            f=fond(png, bx, 2); rgb=[int(v) for v in c[c.index('(')+1:c.index(')')].split(',')[:3]]
            print(th, 'MOT', t, c, 'fond', f, 'contraste %.2f' % cr(rgb, f))
        print(th, 'FIN', pg.evaluate(BOX, '#onbV .onbv-fin .onbv-l-fin, #onbV .onbv-fin .onbv-l-der'))
        ctx.close()
    b.close()

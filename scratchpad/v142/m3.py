import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image
L=[]
with sync_playwright() as p:
    b=p.webkit.launch()
    for sombre in (False,True):
        ctx=contexte(b,sombre=sombre, stockage={'promi_murs':'{"n":3,"t":%d,"der":2,"decouvert":1}'%(__import__('time').time()*1000)}); pg=ouvre(ctx)
        tap_sel(pg,'#studioBtn'); pg.wait_for_timeout(6000)
        for k in range(14):
            glisse(pg, droite((320,300),(80,300),10), pas=16); pg.wait_for_timeout(1600)
            if 'world-locked' in pg.evaluate("()=>document.getElementById('studioScreen').className"): break
        pg.wait_for_timeout(2000)
        for (x,y) in [(195,220),(195,640)]:
            tap(pg,x,y); pg.wait_for_timeout(800); L.append(image(pg)); pg.evaluate("()=>_murBaisse()"); pg.wait_for_timeout(500)
        ctx.close()
    b.close()
W=Image.new('RGB',(400*len(L),844),'white')
for i,im in enumerate(L): W.paste(im,(i*400,0))
W.save('scratchpad/v142/m3-vue.png')

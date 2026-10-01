# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright
from PIL import Image
import io as _io
SEL={'fil':'#feedView .fd-h2','studio':'#stpHaut .stp-t','index':'#indexSheet .scr-ti',
     'aura':'#auraScreen .scr-t','partage':'#shareScreen .scr-t','reglages':'#settingsScreen .scr-ti'}
res={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=3)
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(600)
    for nom,js,wt in (('fil',"()=>{closeAll(); document.getElementById('filBtn').click();}",3200),
                      ('studio',"()=>{closeAll(); document.getElementById('studioBtn').click();}",2800),
                      ('index',"()=>{closeAll(); if(window.ouvrirIndex)ouvrirIndex();}",3000),
                      ('aura',"()=>{closeAll(); document.getElementById('souffleBtn').click();}",5000),
                      ('partage',"()=>{closeAll(); document.getElementById('shareBtn').click();}",3600),
                      ('reglages',"()=>{closeAll(); document.getElementById('settingsBtn').click();}",2600)):
        pg.evaluate(js); pg.wait_for_timeout(wt)
        el=pg.query_selector(SEL[nom])
        if el:
            bx=el.bounding_box()
            png=pg.screenshot(clip={'x':bx['x'],'y':bx['y']-6,'width':max(20,bx['width']),'height':bx['height']+12})
            im=Image.open(_io.BytesIO(png)).convert('L')
            W,H=im.size; px=im.load()
            # fond = coin haut gauche
            f=px[1,1]; ys=[]
            for y in range(H):
                for x in range(W):
                    if abs(px[x,y]-f)>60: ys.append(y); break
            hauteur=(max(ys)-min(ys)+1)/3.0 if ys else 0
            res[nom]=(round(hauteur,1), round(bx['width'],1), round(bx['height'],1), round(bx['y'],1))
            im.save('scratchpad/s27/ti-%s.png'%nom)
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(500)
    b.close()
print('%-10s %-10s %-9s %-9s %s'%('ecran','encre h','boite w','boite h','y'))
for k,v in res.items(): print('%-10s %-10s %-9s %-9s %s'%(k,v[0],v[1],v[2],v[3]))

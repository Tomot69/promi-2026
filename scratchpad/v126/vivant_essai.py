# C-028 — un mouvement forcé, monde par monde : avant / pendant / après (captures @3x) et ce qui bouge
import sys, io, json
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
MONDES = (sys.argv[1] if len(sys.argv)>1 else 'encre,touffe,mosaique,braille,pixel,halin,esquille,madrure,ritournelle,bobinette,terrazzo,gravure,sillons,brouillamini,chamade,volubilis,guingois,chantourne,mascaret,ramage').split(',')
import os; os.makedirs('planche-v126/vivant', exist_ok=True)
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}; window._vivantOff=true;")
    pg=ctx.new_page(); pg.on('pageerror', lambda e: print('ERR', str(e)[:160]))
    pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
    clip={'x':20,'y':44,'width':390,'height':844}; cap=lambda: Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert('RGB')
    for m in MONDES:
        pg.evaluate("m=>{ try{closeAll()}catch(e){} Toile.setTheme(m); }", m); pg.wait_for_timeout(6500)
        a=cap(); pg.wait_for_timeout(300); a2=cap()
        pg.evaluate("()=>{ window._vivantOff=false; Toile.vivant.force(); window._vivantOff=true; }")
        j=pg.evaluate("()=>Toile.vivant.journal().slice(-1)[0]")
        mx=0; pend=None
        for k in range(4):
            pg.wait_for_timeout(180); c=cap(); d=ImageChops.difference(a,c).convert('L').point(lambda v:255 if v>14 else 0); n=sum(d.resize((195,422)).point(lambda v:1 if v>0 else 0).getdata())
            if n>=mx: mx=n; pend=c; bb=d.getbbox()
        pg.wait_for_timeout(2600); z=cap()
        apres=sum(ImageChops.difference(a,z).convert('L').point(lambda v:255 if v>14 else 0).resize((195,422)).point(lambda v:1 if v>0 else 0).getdata())
        bruit=sum(ImageChops.difference(a,a2).convert('L').point(lambda v:255 if v>14 else 0).resize((195,422)).point(lambda v:1 if v>0 else 0).getdata())
        print('%-13s dalles %s · durée %s ms · pendant : %.2f %% de la Toile change (boîte %s) · après : %.2f %% · bruit %.2f %%' % (m, j and j['n'], j and j['d'], 100*mx/(195*422), bb, 100*apres/(195*422), 100*bruit/(195*422)), flush=True)
        W,H=a.size; o=Image.new('RGB',(3*(W//2)+40,H//2),(128,128,128)); o.paste(a.resize((W//2,H//2)),(0,0)); o.paste(pend.resize((W//2,H//2)),(W//2+20,0)); o.paste(z.resize((W//2,H//2)),(W+40,0)); o.save('planche-v126/vivant/%s.png'%m)
        a.save('planche-v126/vivant/%s-avant.png'%m); pend.save('planche-v126/vivant/%s-pendant.png'%m); z.save('planche-v126/vivant/%s-apres.png'%m)
    b.close()

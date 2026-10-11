import sys; sys.path.insert(0,'.')
from banc_tom import *
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
import io as _io
R={}
with sync_playwright() as p:
    b=p.webkit.launch()
    for F in ('zz-av142.html','app.html'):
        for sombre in (False,True):
            ctx=contexte(b,sombre=sombre); pg=ouvre(ctx,F); L=[]
            for t in ['boire un verre','appeler Mamie','courir dimanche']: plante(pg,t)
            for k in range(5):
                if k: pg.reload(); pg.wait_for_timeout(6500)
                tap_sel(pg,'#souffleBtn'); pg.wait_for_timeout(4200)
                d=dev(pg); e=d[4]; im=Image.open(_io.BytesIO(pg.screenshot(clip={'x':d[0]+30*e,'y':d[1]+104*e,'width':330*e,'height':310*e}))).convert('RGB').resize((495,465)); L.append(im)
                print(F,sombre,pg.evaluate("()=>JSON.stringify(_aura.corps())"))
            R[(F,sombre)]=L; ctx.close()
    b.close()
for sombre in (False,True):
    W=Image.new('RGB',(5*505+10,2*475+70),(255,255,255) if not sombre else (20,16,12)); dr=ImageDraw.Draw(W)
    for r,F in enumerate(('zz-av142.html','app.html')):
        dr.text((10,5+r*500),('AVANT (v141)' if r==0 else 'APRES (v142)')+' — cinq ouvertures, Ingenu, '+('sombre' if sombre else 'clair'),fill=(0,0,0) if not sombre else (240,235,220))
        for i,im in enumerate(R[(F,sombre)]): W.paste(im,(10+i*505,25+r*500))
    W.save('planche-v142/PLANCHE-1-pelote-ingenu-%s.png'%('sombre' if sombre else 'clair'))

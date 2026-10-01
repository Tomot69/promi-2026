# Le CLIGNOTEMENT tel qu'il est PEINT : pour chaque lettre, 24 images (100 ms), couleur moyenne des pixels du glyphe
# (ceux qui s'écartent du fond). Même couleur, même rythme, même intensité = mêmes courbes.
import sys, io
from playwright.sync_api import sync_playwright
from PIL import Image
ECR=[('i de PROMI', "closeAll()", '#accPlat .acc-mm i'),
     ('S de RÉGLAGES', "closeAll(); document.querySelector('#accPlat [aria-label=Réglages], #accPlat .acc-reg, #settingsBtn').click()", '#settingsScreen h1.scr-ti .ti-x'),
     ('R de PARTAGER', "closeAll(); openShare()", '#shareScreen h2.scr-t .ti-x')]
TH=(sys.argv[1:] or ['dark'])[0]; PL=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for nom,js,sel in ECR:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6800)
        pg.evaluate("(t)=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} setTheme(t);}", TH); pg.wait_for_timeout(500)
        try: pg.evaluate("()=>{"+js+"}")
        except Exception as e: print(nom, 'ouverture', str(e)[:80])
        pg.wait_for_timeout(1800)
        r=pg.evaluate("(s)=>{const e=[...document.querySelectorAll(s)].find(x=>{const r=x.getBoundingClientRect();return r.width>0});if(!e)return null;const r=e.getBoundingClientRect();return [r.left,r.top,r.width,r.height, getComputedStyle(e).fontSize]}", sel)
        if not r: print(nom, 'introuvable'); pg.close(); continue
        x,y,w,h,fs=r; fond=None; serie=[]; frames=[]
        for k in range(24):
            im=Image.open(io.BytesIO(pg.screenshot(clip={'x':x,'y':y,'width':w,'height':h}))).convert('RGB')
            px=list(im.getdata())
            if fond is None:
                # le fond : le pixel le plus fréquent du coin
                from collections import Counter
                fond=Counter(px[:len(px)//8]).most_common(1)[0][0]
            gl=[q for q in px if sum(abs(q[i]-fond[i]) for i in range(3))>60]
            m=tuple(round(sum(q[i] for q in gl)/max(1,len(gl))) for i in range(3))
            serie.append(m); frames.append(im); pg.wait_for_timeout(100)
        lum=[round(0.2126*m[0]+0.7152*m[1]+0.0722*m[2]) for m in serie]
        print('%-14s %s · %s · fond %s\n   couleur max %s · min %s\n   luminance %s'%(nom, TH, fs, fond, max(serie,key=sum), min(serie,key=sum), lum))
        lum2=[0.2126*m[0]+0.7152*m[1]+0.0722*m[2] for m in serie]
        hi=frames[lum2.index(max(lum2))]; lo=frames[lum2.index(min(lum2))]
        PL.append((nom,hi,lo))
        pg.close()
    b.close()
from PIL import ImageDraw
Hh=max(max(a.size[1],b_.size[1]) for _,a,b_ in PL)*3; Wt=sum(max(a.size[0],b_.size[0])*3*2+40 for _,a,b_ in PL)
pl=Image.new('RGB',(Wt,Hh+30),(255,255,255)); d=ImageDraw.Draw(pl); x=0
for nom,a,b_ in PL:
    for im,lab in [(a,'allumé'),(b_,'éteint')]:
        pl.paste(im.resize((im.size[0]*3,im.size[1]*3)),(x,30)); d.text((x,5),nom+' · '+lab,fill=(0,0,0)); x+=im.size[0]*3+10
    x+=20
pl.save('sauvegardes/v47/clignotement_%s.png'%TH)

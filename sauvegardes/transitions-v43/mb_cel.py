from playwright.sync_api import sync_playwright
from PIL import Image
import io
INST=[0,350,550,750,1000,1300,2300,2600,2950]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1180,'height':1100},device_scale_factor=1)
    pg.goto('http://127.0.0.1:8752/moodboard-celebration.html'); pg.wait_for_timeout(1500)
    for th in ['sombre','clair']:
        pg.evaluate("t=>{document.querySelector('[data-v='+t+']').click(); pause=true; toiles.forEach(function(X){X.T=new Toile(1);X.T.h=3999;});}",th)
        ims=[]; h=0
        for t in INST:
            pg.evaluate("n=>{for(var i=0;i<n;i++) toiles.forEach(function(X){X.T.avance(1/240);});}", int(round((t-h+ (1 if h==0 else 0))/1000*240)) or 1); h=t
            pg.wait_for_timeout(120)
            el=pg.query_selector_all('.tel canvas')[1]
            ims.append(Image.open(io.BytesIO(el.screenshot())).convert('RGB'))
        w,hh=ims[0].size; s=Image.new('RGB',(w*len(ims)+8*len(ims),hh),(255,255,255))
        for i,im in enumerate(ims): s.paste(im,(i*(w+8),0))
        s.save('sauvegardes/transitions-v43/mb_%s.png'%th)
    print(pg.evaluate("()=>JSON.stringify(window.__err||null)"))
    b.close()

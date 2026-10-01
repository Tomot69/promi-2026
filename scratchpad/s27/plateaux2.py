from playwright.sync_api import sync_playwright
from PIL import Image
import io as _io, json
ORD=[('fil','#feedView .enh',"()=>{document.getElementById('filBtn').click();}",3200),
     ('studio','#stpHaut',"()=>{document.getElementById('studioBtn').click();}",2800),
     ('index','#indexSheet .enh',"()=>{if(window.ouvrirIndex)ouvrirIndex();}",3000),
     ('aura','#auraScreen .enh',"()=>{document.getElementById('souffleBtn').click();}",5000),
     ('partage','#shareScreen .enh',"()=>{document.getElementById('shareBtn').click();}",3600),
     ('reglages','#settingsScreen .enh',"()=>{document.getElementById('settingsBtn').click();}",2600)]
ims=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    for nom,sel,js,wt in ORD:
        pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=3)
        pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
        pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}")
        pg.evaluate("(t)=>setTheme(t)",'dark'); pg.wait_for_timeout(500)
        pg.evaluate(js); pg.wait_for_timeout(wt)
        el=pg.query_selector(sel); bx=el.bounding_box()
        png=pg.screenshot(clip=bx)
        im=Image.open(_io.BytesIO(png)).convert('RGB'); ims.append((nom,im))
        pg.close()
    b.close()
W=max(i.width for _,i in ims); H=sum(i.height for _,i in ims)+8*len(ims)
out=Image.new('RGB',(W,H),(255,0,0)); y=0
for nom,i in ims: out.paste(i,(0,y)); y+=i.height+8
out.save('scratchpad/s27/plateaux2.png'); print('ok', [ (n,i.size) for n,i in ims])

from playwright.sync_api import sync_playwright
from PIL import Image
import io as _io
CAP={}
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':430,'height':932},device_scale_factor=2)
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
        CAP[nom]=pg.query_selector('#device').screenshot()
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(500)
    b.close()
ims=[]
for nom in ('fil','studio','index','aura','partage','reglages'):
    im=Image.open(_io.BytesIO(CAP[nom])).convert('RGB')
    ims.append(im.crop((60,140,700,290)))
W=max(i.width for i in ims); H=sum(i.height for i in ims)
out=Image.new('RGB',(W,H),(20,16,10)); y=0
for i in ims: out.paste(i,(0,y)); y+=i.height
out.save('scratchpad/s27/bandeaux.png')
print('ok')

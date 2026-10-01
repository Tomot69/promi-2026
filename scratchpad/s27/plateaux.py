from playwright.sync_api import sync_playwright
from PIL import Image
import io as _io, json
SEL={'fil':'#feedView .enh','studio':'#stpHaut','index':'#indexSheet .enh',
     'aura':'#auraScreen .enh','partage':'#shareScreen .enh','reglages':'#settingsScreen .enh'}
ims=[]; info={}
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
            info[nom]={'plateau':[round(bx['x'],1),round(bx['y'],1),round(bx['width'],1),round(bx['height'],1)]}
            f=pg.evaluate("(s)=>{var p=document.querySelector(s); var c=p&&p.querySelector('.closeb,[data-close]'); if(!c) return null; var r=c.getBoundingClientRect(); return [+r.left.toFixed(1),+r.width.toFixed(1)];}", SEL[nom])
            info[nom]['fermer']=f
            png=pg.screenshot(clip=bx)
            ims.append(Image.open(_io.BytesIO(png)).convert('RGB'))
        pg.evaluate("()=>{closeAll();}"); pg.wait_for_timeout(500)
    b.close()
W=max(i.width for i in ims); H=sum(i.height for i in ims)+10*len(ims)
out=Image.new('RGB',(W,H),(255,0,0)); y=0
for i in ims: out.paste(i,(0,y)); y+=i.height+10
out.save('scratchpad/s27/plateaux.png')
print(json.dumps(info,indent=1))

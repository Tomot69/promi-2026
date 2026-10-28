import sys, io; sys.path.insert(0,'.')
from playwright.sync_api import sync_playwright
import banc_tom as B
from PIL import Image
quoi=sys.argv[1]; ts=[int(x) for x in sys.argv[2].split(',')]
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=B.contexte(b, vw=390, vh=651); pg=B.ouvre(ctx,'app.html',attente=7000,q='?tlv=0.05'); er=[]; pg.on('pageerror',lambda e: er.append(str(e)[:200]))
    pg.evaluate("()=>{var o=document.getElementById('promiOnb'); if(o){o.classList.add('gone');o.style.display='none';} try{closeAll()}catch(e){} }"); pg.wait_for_timeout(300)
    pg.evaluate("q=>{ _guide.montre(q); }", quoi); t0=0; ims=[]
    for t in ts:
        pg.wait_for_timeout(t-t0); t0=t
        r=pg.evaluate("()=>{const p=document.getElementById('guidePhrase'); const r=p.getBoundingClientRect(); return [r.left,r.top,r.width,r.height]}")
        ims.append(Image.open(io.BytesIO(pg.screenshot(clip={'x':max(0,r[0]-6),'y':max(0,r[1]-6),'width':min(390,r[2]+12),'height':r[3]+12}))).convert('RGB'))
    H=sum(i.height for i in ims); o=Image.new('RGB',(max(i.width for i in ims),H),'white'); y=0
    for i in ims: o.paste(i,(0,y)); y+=i.height
    o.save('scratchpad/v170/ral2-%s.png'%quoi); print(er, o.size); b.close()

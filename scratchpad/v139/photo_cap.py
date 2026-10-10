from playwright.sync_api import sync_playwright
from PIL import Image
PHOTO = r"""()=>{ const c=document.createElement('canvas'); c.width=900; c.height=600; const g=c.getContext('2d'); const G=g.createLinearGradient(0,0,0,600); G.addColorStop(0,'#7FB6E8'); G.addColorStop(.55,'#F3D9A8'); G.addColorStop(.56,'#3F7D4E'); G.addColorStop(1,'#1E4B2C'); g.fillStyle=G; g.fillRect(0,0,900,600); g.fillStyle='#F7E36B'; g.beginPath(); g.arc(650,170,70,0,7); g.fill(); g.fillStyle='#5A3A22'; g.fillRect(250,250,40,200); g.fillStyle='#2E6B3A'; g.beginPath(); g.arc(270,220,110,0,7); g.fill(); return c.toDataURL('image/jpeg',0.9); }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=3)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');['tenir','chiche','planter','bande'].forEach(g=>localStorage.setItem('geste_vu_'+g,'1'));}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6000)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';}}"); src=pg.evaluate(PHOTO); ims=[]
    r=pg.evaluate("()=>{var r=document.getElementById('device').getBoundingClientRect();return [r.left,r.top]}")
    for c in (None,{'z':0.55,'dx':0,'dy':10},{'z':2.4,'dx':-60,'dy':40}):
        pg.evaluate("()=>{ try{closeAll()}catch(e){} }"); pg.wait_for_timeout(1000); pg.evaluate("([s,c])=>{ const q=promises.find(p=>p.title==='planter un arbre'); q.photo=s; if(c){ c.n=s.length; q.photoCadre=c; } else delete q.photoCadre; openDetail(q.id); }",[src,c]); pg.wait_for_timeout(3000)
        pg.screenshot(path='/tmp/ph.png',clip={'x':r[0],'y':r[1],'width':390,'height':844}); ims.append(Image.open('/tmp/ph.png').convert('RGB').resize((585,1266)))
    cx=pg.evaluate("()=>{const c=window._photoCentre, cv=document.getElementById('dpTrameCv'), r=cv.getBoundingClientRect(); return [r.left+c.x*r.width/390, r.top+c.y*r.width/390]}")
    pg.mouse.click(cx[0],cx[1]); pg.wait_for_timeout(900); pg.screenshot(path='/tmp/ph.png',clip={'x':r[0],'y':r[1],'width':390,'height':844}); ims.append(Image.open('/tmp/ph.png').convert('RGB').resize((585,1266)))
    W=Image.new('RGB',(4*605,1266),'#F7F0DE')
    for i,im in enumerate(ims): W.paste(im,(i*605,0))
    W.save('planche-v139/photo-cadre.png'); b.close()

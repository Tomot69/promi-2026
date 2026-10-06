import re
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
SC='/private/tmp/claude-501/-Users-macbookpro-Documents-IA-projetcs-Promi-Promi-App-Promi-2026/0f3b2d08-7c5e-419f-b53b-a791ff620663/scratchpad/'
G=r"""()=>{ const cv=document.getElementById('toileCv'), r=cv.getBoundingClientRect(), dv=document.getElementById('device').getBoundingClientRect(); const kx=cv.clientWidth/r.width, ky=cv.clientHeight/r.height; const out=[];
  for(let y=dv.top+4;y<dv.bottom-4;y+=8) for(let x=dv.left+4;x<dv.right-4;x+=8){ let h=null; try{ h=Toile.hit((x-r.left)*kx,(y-r.top)*ky); }catch(e){} out.push([x-dv.left,y-dv.top, h?(h.pid!=null?h.pid:(h.kind==='nuee'?-2:-1)):-9]); } return out; }"""
with sync_playwright() as p:
    b=p.webkit.launch(); ctx=b.new_context(viewport={'width':430,'height':932},device_scale_factor=2,has_touch=True)
    ctx.add_init_script("try{localStorage.setItem('promi_onb','1');localStorage.setItem('promi_rappel_n','9')}catch(e){}")
    pg=ctx.new_page(); pg.goto('http://127.0.0.1:8752/app.html'); pg.wait_for_timeout(6500)
    pg.evaluate("()=>{var o=document.getElementById('promiOnb');if(o){o.classList.add('gone');o.style.display='none';} try{setPremium(true)}catch(e){} }")
    ims=[]
    for m in ('ramage','encre','chamade','volubilis'):
        pg.evaluate("(m)=>{closeAll(); Toile.setTheme(m);}", m); pg.wait_for_timeout(3500)
        pg.screenshot(path=SC+'t-%s.png'%m, clip={'x':20,'y':44,'width':390,'height':844}); pts=pg.evaluate(G)
        im=Image.open(SC+'t-%s.png'%m).convert('RGB'); d=ImageDraw.Draw(im); cols={}
        import random; random.seed(3)
        n={'parole':0,'vide':0,'cercle':0,'rien':0}
        for x,y,pid in pts:
            if pid==-9: n['rien']+=1; continue
            if pid==-1: n['vide']+=1; d.point((x*2,y*2),fill=(0,0,0)); continue
            if pid==-2: n['cercle']+=1
            else: n['parole']+=1
            c=cols.setdefault(pid,(random.randint(60,255),random.randint(0,255),random.randint(0,255))); d.rectangle((x*2-3,y*2-3,x*2+3,y*2+3),fill=c,outline=(0,0,0))
        print(m, n, 'paroles distinctes', len([k for k in cols if k>=0])); ims.append(im)
    P=Image.new('RGB',(4*400,844),(255,255,255))
    for i,im in enumerate(ims): P.paste(im.resize((390,844)),(i*400,0))
    P.save(SC+'touche-carte.png'); b.close()
